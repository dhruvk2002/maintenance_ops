from __future__ import annotations

try:
    import frappe
except Exception:
    frappe = None

from .bootstrap import seed_from_datasets
from .reports import get_dashboard_summary, get_due_overdue_work_orders
from .services import escalate_overdue_work_orders, generate_due_pm_work_orders


def _as_json_response(payload):
    if frappe is None:
        return payload
    return payload


if frappe:

    @frappe.whitelist()
    def seed_data(dataset_dir: str):
        return _as_json_response(seed_from_datasets(dataset_dir))


    @frappe.whitelist()
    def run_pm_generation():
        return _as_json_response(generate_due_pm_work_orders())


    @frappe.whitelist()
    def run_overdue_escalation():
        return _as_json_response(escalate_overdue_work_orders())


    @frappe.whitelist()
    def due_overdue_report():
        return _as_json_response(get_due_overdue_work_orders())


    @frappe.whitelist()
    def dashboard_summary():
        return _as_json_response(get_dashboard_summary())


    @frappe.whitelist()
    def ticket_aging_report():
        from maintenance_ops.report.ticket_aging_summary.ticket_aging_summary import execute

        columns, data = execute()
        return _as_json_response({"columns": columns, "data": data})


    @frappe.whitelist()
    def generate_fixtures():
        """Export all master data as Frappe fixture JSON files into maintenance_ops/fixtures/."""
        import json, os
        from pathlib import Path

        fixture_dir = Path(frappe.get_app_path("maintenance_ops")) / "fixtures"
        fixture_dir.mkdir(exist_ok=True)

        doctypes = [
            ("City", ["city_name", "short_code", "active"]),
            ("Zonal Office", ["office_name", "city", "active"]),
            ("Outlet", ["outlet_code", "outlet_name", "city", "zonal_office", "active"]),
            ("Asset Category", ["category_name", "description", "active"]),
            ("Asset", ["asset_code", "asset_name", "asset_category", "outlet", "active"]),
            ("Maintenance Program", ["program_name", "asset_category", "frequency", "active"]),
            ("Maintenance Team Member", ["employee_id", "full_name", "role", "home_office", "active"]),
            ("Exception Record", ["exception_code", "exception_description", "active"]),
        ]

        counts = {}
        for doctype, fields in doctypes:
            meta = frappe.get_meta(doctype)
            available = {f.fieldname for f in meta.fields}
            safe_fields = [f for f in fields if f in available]
            records = frappe.get_all(doctype, fields=["name"] + safe_fields, limit_page_length=0)
            data = [{"doctype": doctype, **{k: v for k, v in r.items()}} for r in records]
            fname = doctype.lower().replace(" ", "_") + ".json"
            with open(fixture_dir / fname, "w") as f:
                json.dump(data, f, indent=2, default=str)
            counts[doctype] = len(data)

        return counts
