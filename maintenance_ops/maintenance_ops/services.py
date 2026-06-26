from __future__ import annotations

from datetime import date
from typing import Iterable

try:
    import frappe
except Exception:
    frappe = None

from .api import default_priority_for_asset_category, pm_due_date
from .models import ExceptionRecord
from .routing import choose_technician, route_by_city
from .scheduling import is_due


def build_pm_work_order_seed(*, outlet: str, asset: str, asset_category: str, frequency: str, last_done: date | None = None, source_program: str | None = None) -> dict:
    baseline_date = last_done or date.today()
    computed_due = pm_due_date(baseline_date, frequency)
    return {
        "work_order_type": "Preventive",
        "status": "Due" if is_due(last_done, frequency) else "Open",
        "outlet": outlet,
        "asset": asset,
        "asset_category": asset_category,
        "source_program": source_program,
        "due_date": computed_due,
        "priority": default_priority_for_asset_category(asset_category),
    }


def classify_reactive_ticket(*, outlet_city: str, city_to_office: dict[str, str], team_members: Iterable[dict]) -> dict:
    office = route_by_city(outlet_city, city_to_office)
    assignee = choose_technician(team_members, city=outlet_city, home_office=office)
    return {
        "zonal_office": office,
        "assignee": assignee.get("employee_name") if assignee else None,
        "assignee_employee_no": assignee.get("employee_no") if assignee else None,
        "assignee_role": assignee.get("job_title") if assignee else None,
    }


def build_exception(*, source_file: str, row_number: int, issue_type: str, message: str, payload: str) -> ExceptionRecord:
    return ExceptionRecord(
        source_file=source_file,
        source_row_number=row_number,
        issue_type=issue_type,
        issue_message=message,
        source_payload=payload,
    )


def create_reactive_work_order_from_ticket(ticket_doc):
    assigned_to = None
    if frappe is not None and ticket_doc.outlet:
        outlet = frappe.get_doc("Outlet", ticket_doc.outlet)
        outlet_city_name = ""
        if outlet.city:
            city_doc = frappe.get_doc("City", outlet.city)
            outlet_city_name = city_doc.city_name or city_doc.name

        city_to_office = _city_to_office_map()
        team_members = frappe.get_all(
            "Maintenance Team Member",
            filters={"active": 1},
            fields=["name", "employee_no", "employee_name", "job_title", "home_office"],
        )
        routed = classify_reactive_ticket(
            outlet_city=outlet_city_name,
            city_to_office=city_to_office,
            team_members=team_members,
        )
        if routed.get("assignee_employee_no"):
            member = frappe.get_all(
                "Maintenance Team Member",
                filters={"employee_no": routed["assignee_employee_no"]},
                fields=["name"],
                limit=1,
            )
            assigned_to = member[0].name if member else None

    work_order = frappe.get_doc(
        {
            "doctype": "Maintenance Work Order",
            "work_order_type": "Reactive",
            "status": "Open",
            "outlet": ticket_doc.outlet,
            "asset": ticket_doc.asset,
            "asset_category": ticket_doc.asset_category,
            "source_ticket": ticket_doc.name,
            "priority": ticket_doc.priority,
            "assigned_to": assigned_to,
            "remarks": ticket_doc.issue_summary,
        }
    )
    work_order.insert(ignore_permissions=True)
    return work_order


def _city_to_office_map() -> dict[str, str]:
    if frappe is None:
        return {}
    rows = frappe.get_all("Zonal Office", filters={"active": 1}, fields=["name", "office_name", "city"])
    result: dict[str, str] = {}
    for row in rows:
        if not row.city:
            continue
        city_doc = frappe.get_doc("City", row.city)
        city_name = city_doc.city_name or city_doc.name
        office_name = row.office_name or row.name
        result[city_name] = office_name
    return result


def generate_due_pm_work_orders() -> list[dict]:
    if frappe is None:
        return []

    created: list[dict] = []
    active_programs = frappe.get_all(
        "Maintenance Program",
        filters={"active": 1},
        fields=["name", "asset_category", "frequency"],
    )

    for program in active_programs:
        assets = frappe.get_all(
            "Asset",
            filters={"category": program.asset_category, "status": "Active"},
            fields=["name", "outlet", "category"],
        )

        for asset in assets:
            existing = frappe.get_all(
                "Maintenance Work Order",
                filters={
                    "source_program": program.name,
                    "asset": asset.name,
                    "status": ["not in", ["Completed", "Closed", "Cancelled"]],
                },
                fields=["name"],
                limit=1,
            )
            if existing:
                continue

            seed = build_pm_work_order_seed(
                outlet=asset.outlet,
                asset=asset.name,
                asset_category=asset.category,
                frequency=program.frequency,
                last_done=None,
                source_program=program.name,
            )
            work_order = frappe.get_doc({"doctype": "Maintenance Work Order", **seed})
            work_order.insert(ignore_permissions=True)
            created.append({"work_order": work_order.name, "asset": asset.name, "program": program.name})

    return created


def escalate_overdue_work_orders() -> list[dict]:
    if frappe is None:
        return []

    updates: list[dict] = []
    overdue = frappe.get_all(
        "Maintenance Work Order",
        filters={
            "work_order_type": "Preventive",
            "status": ["in", ["Open", "Due", "In Progress"]],
            "due_date": ["<", frappe.utils.nowdate()],
        },
        fields=["name", "due_date", "assigned_to", "outlet"],
    )

    for row in overdue:
        doc = frappe.get_doc("Maintenance Work Order", row.name)
        doc.status = "Overdue"
        note = f"Auto-escalated on {frappe.utils.nowdate()}"
        doc.remarks = f"{doc.remarks}\n{note}".strip() if doc.remarks else note
        doc.save(ignore_permissions=True)
        updates.append({"work_order": doc.name, "status": doc.status, "assigned_to": doc.assigned_to, "outlet": doc.outlet})

    return updates
