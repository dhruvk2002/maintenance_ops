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
