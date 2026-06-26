"""Import seeded fixture data during migrate with safe upserts."""

from __future__ import annotations

import json
from pathlib import Path

import frappe


KEY_FIELDS = {
    "City": "city_name",
    "Zonal Office": "office_name",
    "Outlet": "outlet_code",
    "Asset Category": "category_name",
    "Asset": "asset_code",
    "Maintenance Program": "program_name",
    "Maintenance Team Member": "employee_id",
    "Exception Record": "exception_code",
}


def _upsert_record(payload: dict):
    doctype = payload.get("doctype")
    key_field = KEY_FIELDS.get(doctype)
    if not doctype or not key_field or key_field not in payload:
        return

    existing = frappe.get_all(
        doctype,
        filters={key_field: payload[key_field]},
        fields=["name"],
        limit=1,
    )

    if existing:
        doc = frappe.get_doc(doctype, existing[0].name)
        doc.update(payload)
        if doctype == "Asset":
            doc.flags.ignore_validate = True
        doc.save(ignore_permissions=True)
        return

    doc = frappe.get_doc(payload)
    if doctype == "Asset":
        doc.flags.ignore_validate = True
    doc.insert(ignore_permissions=True)


def execute():
    fixture_dir = Path(frappe.get_app_path("maintenance_ops")) / "fixtures"
    if not fixture_dir.exists():
        return

    ordered_files = [
        "city.json",
        "zonal_office.json",
        "outlet.json",
        "asset_category.json",
        "asset_seed.data",
        "maintenance_program.json",
        "maintenance_team_member.json",
        "exception_record.json",
    ]

    for filename in ordered_files:
        path = fixture_dir / filename
        if not path.exists():
            continue
        rows = json.loads(path.read_text())
        for row in rows:
            _upsert_record(row)

    frappe.db.commit()
