from __future__ import annotations

from pathlib import Path
from collections import defaultdict

try:
    import frappe
except Exception:
    frappe = None

from .api import normalize_city_code
from .importers import extract_pm_tracker, import_outlets, import_team_members


def _upsert(doctype: str, key_field: str, payload: dict, skip_validate: bool = False):
    if frappe is None:
        return None
    existing = frappe.get_all(doctype, filters={key_field: payload[key_field]}, fields=["name"], limit=1)
    if existing:
        doc = frappe.get_doc(doctype, existing[0].name)
        doc.update(payload)
        if skip_validate:
            doc.flags.ignore_validate = True
        doc.save(ignore_permissions=True)
        return doc
    doc = frappe.get_doc({"doctype": doctype, **payload})
    if skip_validate:
        doc.flags.ignore_validate = True
    doc.insert(ignore_permissions=True)
    return doc


def seed_from_datasets(dataset_dir: str) -> dict:
    if frappe is None:
        return {"seeded": False, "reason": "frappe_not_available"}

    base = Path(dataset_dir)
    outlets_path = base / "PM_Case_Outlets.xlsx"
    users_path = base / "PM_Case_User_Master.csv"
    pm_path = base / "PM_Case_Before.xlsx"

    outlet_rows, outlet_ex = import_outlets(str(outlets_path))
    team_rows, team_ex = import_team_members(str(users_path))
    pm_rows, pm_ex = extract_pm_tracker(str(pm_path))

    city_names = sorted({normalize_city_code(row.city) for row in outlet_rows if row.city})
    city_docs = {name: _upsert("City", "city_name", {"city_name": name, "short_code": name[:3].upper(), "active": 1}) for name in city_names}

    office_names = sorted({(row.home_office or "").strip() for row in team_rows if row.home_office})
    for office in office_names:
        city_guess = next((c for c in city_names if c.lower() in office.lower()), city_names[0] if city_names else "Unknown")
        _upsert("Zonal Office", "office_name", {"office_name": office, "city": city_docs[city_guess].name if city_guess in city_docs else None, "active": 1})

    for outlet in outlet_rows:
        city_doc = city_docs.get(outlet.city)
        _upsert(
            "Outlet",
            "outlet_code",
            {
                "outlet_code": outlet.outlet_code,
                "outlet_name": outlet.outlet_name,
                "city": city_doc.name if city_doc else None,
                "active": 1,
            },
        )

    asset_categories = sorted({row["asset_category"] for row in pm_rows if row.get("asset_category")})
    for category in asset_categories:
        _upsert(
            "Asset Category",
            "category_name",
            {
                "category_name": category,
                "description": "Seeded from PM tracker",
                "active": 1,
            },
        )

    seen_assets: set[tuple[str, str]] = set()
    for row in pm_rows:
        outlet_code = row["outlet_code"]
        category = row["asset_category"]
        key = (outlet_code, category)
        if key in seen_assets:
            continue
        seen_assets.add(key)

        outlet_doc = frappe.get_all("Outlet", filters={"outlet_code": outlet_code}, fields=["name"], limit=1)
        category_doc = frappe.get_all("Asset Category", filters={"category_name": category}, fields=["name"], limit=1)
        if not outlet_doc or not category_doc:
            continue

        _upsert(
            "Asset",
            "asset_name",
            {
                "asset_name": f"{outlet_code}-{category}",
                "asset_code": f"{outlet_code}-{category}"[:140],
                "outlet": outlet_doc[0].name,
                "category": category_doc[0].name,
                "status": "Active",
            },
            skip_validate=True,
        )

    program_groups: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in pm_rows:
        category = row.get("asset_category", "")
        frequency = row.get("frequency", "") or "Monthly"
        task = row.get("task", "")
        if not category:
            continue
        program_groups[(category, frequency)].add(task)

    program_count = 0
    for (category, frequency), tasks in program_groups.items():
        category_doc = frappe.get_all("Asset Category", filters={"category_name": category}, fields=["name"], limit=1)
        if not category_doc:
            continue
        program_name = f"{category} - {frequency}"[:140]
        program_doc = _upsert(
            "Maintenance Program",
            "program_name",
            {
                "program_name": program_name,
                "asset_category": category_doc[0].name,
                "frequency": frequency if frequency in {"Weekly", "Monthly", "Quarterly", "Half-Yearly", "Yearly"} else "Monthly",
                "lead_time_days": 2,
                "active": 1,
                "description": "Seeded from PM_Case_Before.xlsx",
            },
        )

        if program_doc:
            program_doc.tasks = []
            sort_order = 1
            for task in sorted(t for t in tasks if t):
                program_doc.append(
                    "tasks",
                    {
                        "task_name": task[:140],
                        "checklist_instructions": task,
                        "expected_result": "Completed",
                        "mandatory": 1,
                        "sort_order": sort_order,
                    },
                )
                sort_order += 1
            program_doc.save(ignore_permissions=True)
            program_count += 1

    for member in team_rows:
        _upsert(
            "Maintenance Team Member",
            "employee_no",
            {
                "employee_no": member.employee_no,
                "employee_name": member.employee_name,
                "job_title": member.job_title,
                "department": member.department,
                "email": member.email,
                "mobile": member.mobile,
                "active": 1,
            },
        )

    member_name_by_employee_no = {
        row.employee_no: frappe.get_all(
            "Maintenance Team Member",
            filters={"employee_no": row.employee_no},
            fields=["name"],
            limit=1,
        )[0].name
        for row in team_rows
        if frappe.get_all(
            "Maintenance Team Member",
            filters={"employee_no": row.employee_no},
            fields=["name"],
            limit=1,
        )
    }

    office_name_to_doc = {
        row.office_name: row.name
        for row in frappe.get_all("Zonal Office", filters={"active": 1}, fields=["name", "office_name"])
    }

    member_doc_by_display_name = {
        row.employee_name.strip(): row.name
        for row in frappe.get_all("Maintenance Team Member", filters={"active": 1}, fields=["name", "employee_name"])
        if row.employee_name
    }

    for member in team_rows:
        docname = member_name_by_employee_no.get(member.employee_no)
        if not docname:
            continue
        doc = frappe.get_doc("Maintenance Team Member", docname)

        if member.home_office:
            doc.home_office = office_name_to_doc.get(member.home_office.strip())

        if member.reports_to:
            manager_name = member.reports_to.strip()
            doc.reports_to = member_doc_by_display_name.get(manager_name)

        doc.save(ignore_permissions=True)

    for ex in [*outlet_ex, *team_ex, *pm_ex]:
        frappe.get_doc(
            {
                "doctype": "Exception Record",
                "source_file": ex.source_file,
                "source_row_number": ex.source_row_number,
                "source_payload": ex.source_payload,
                "issue_type": ex.issue_type,
                "issue_message": ex.issue_message,
                "status": ex.status,
            }
        ).insert(ignore_permissions=True)

    return {
        "seeded": True,
        "cities": len(city_names),
        "outlets": len(outlet_rows),
        "asset_categories": len(asset_categories),
        "assets": len(seen_assets),
        "maintenance_programs": program_count,
        "team_members": len(team_rows),
        "exceptions": len(outlet_ex) + len(team_ex) + len(pm_ex),
    }
