from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "maintenance_ops" / "doctype"
MODULE = "Maintenance Ops"

DOCTYPES = {
    "city": {
        "name": "City",
        "fields": [
            {"fieldname": "city_name", "fieldtype": "Data", "label": "City Name", "req": 1},
            {"fieldname": "short_code", "fieldtype": "Data", "label": "Short Code"},
            {"fieldname": "active", "fieldtype": "Check", "label": "Active", "default": "1"},
        ],
    },
    "zonal_office": {
        "name": "Zonal Office",
        "fields": [
            {"fieldname": "office_name", "fieldtype": "Data", "label": "Office Name", "req": 1},
            {"fieldname": "city", "fieldtype": "Link", "label": "City", "options": "City", "req": 1},
            {"fieldname": "manager", "fieldtype": "Link", "label": "Manager", "options": "Maintenance Team Member"},
            {"fieldname": "active", "fieldtype": "Check", "label": "Active", "default": "1"},
        ],
    },
    "outlet": {
        "name": "Outlet",
        "fields": [
            {"fieldname": "outlet_code", "fieldtype": "Data", "label": "Outlet Code", "req": 1},
            {"fieldname": "outlet_name", "fieldtype": "Data", "label": "Outlet Name", "req": 1},
            {"fieldname": "city", "fieldtype": "Link", "label": "City", "options": "City", "req": 1},
            {"fieldname": "zonal_office", "fieldtype": "Link", "label": "Zonal Office", "options": "Zonal Office"},
            {"fieldname": "active", "fieldtype": "Check", "label": "Active", "default": "1"},
        ],
    },
    "asset_category": {
        "name": "Asset Category",
        "fields": [
            {"fieldname": "category_name", "fieldtype": "Data", "label": "Category Name", "req": 1},
            {"fieldname": "description", "fieldtype": "Small Text", "label": "Description"},
            {"fieldname": "active", "fieldtype": "Check", "label": "Active", "default": "1"},
        ],
    },
    "asset": {
        "name": "Asset",
        "fields": [
            {"fieldname": "asset_name", "fieldtype": "Data", "label": "Asset Name", "req": 1},
            {"fieldname": "asset_code", "fieldtype": "Data", "label": "Asset Code"},
            {"fieldname": "outlet", "fieldtype": "Link", "label": "Outlet", "options": "Outlet", "req": 1},
            {"fieldname": "category", "fieldtype": "Link", "label": "Category", "options": "Asset Category", "req": 1},
            {"fieldname": "serial_no", "fieldtype": "Data", "label": "Serial No"},
            {"fieldname": "install_date", "fieldtype": "Date", "label": "Install Date"},
            {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Active\nInactive\nUnder Repair\nRetired", "default": "Active"},
        ],
    },
    "maintenance_team_member": {
        "name": "Maintenance Team Member",
        "fields": [
            {"fieldname": "employee_no", "fieldtype": "Data", "label": "Employee No", "req": 1},
            {"fieldname": "employee_name", "fieldtype": "Data", "label": "Employee Name", "req": 1},
            {"fieldname": "job_title", "fieldtype": "Data", "label": "Job Title"},
            {"fieldname": "department", "fieldtype": "Data", "label": "Department"},
            {"fieldname": "email", "fieldtype": "Data", "label": "Email"},
            {"fieldname": "mobile", "fieldtype": "Data", "label": "Mobile"},
            {"fieldname": "reports_to", "fieldtype": "Link", "label": "Reports To", "options": "Maintenance Team Member"},
            {"fieldname": "home_office", "fieldtype": "Link", "label": "Home Office", "options": "Zonal Office"},
            {"fieldname": "active", "fieldtype": "Check", "label": "Active", "default": "1"},
        ],
    },
    "maintenance_program": {
        "name": "Maintenance Program",
        "fields": [
            {"fieldname": "program_name", "fieldtype": "Data", "label": "Program Name", "req": 1},
            {"fieldname": "asset_category", "fieldtype": "Link", "label": "Asset Category", "options": "Asset Category", "req": 1},
            {"fieldname": "frequency", "fieldtype": "Select", "label": "Frequency", "options": "Weekly\nMonthly\nQuarterly\nHalf-Yearly\nYearly", "req": 1},
            {"fieldname": "lead_time_days", "fieldtype": "Int", "label": "Lead Time Days", "default": 0},
            {"fieldname": "active", "fieldtype": "Check", "label": "Active", "default": "1"},
            {"fieldname": "description", "fieldtype": "Small Text", "label": "Description"},
        ],
        "children": [
            {
                "child_doctype": "Maintenance Program Task",
                "name": "tasks",
                "fields": [
                    {"fieldname": "task_name", "fieldtype": "Data", "label": "Task Name", "req": 1},
                    {"fieldname": "checklist_instructions", "fieldtype": "Small Text", "label": "Checklist Instructions"},
                    {"fieldname": "expected_result", "fieldtype": "Data", "label": "Expected Result"},
                    {"fieldname": "mandatory", "fieldtype": "Check", "label": "Mandatory", "default": "1"},
                    {"fieldname": "sort_order", "fieldtype": "Int", "label": "Sort Order", "default": 0},
                ],
            }
        ],
    },
    "maintenance_work_order": {
        "name": "Maintenance Work Order",
        "fields": [
            {"fieldname": "work_order_type", "fieldtype": "Select", "label": "Work Order Type", "options": "Preventive\nReactive", "req": 1},
            {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nOpen\nDue\nOverdue\nIn Progress\nCompleted\nClosed\nCancelled", "default": "Draft"},
            {"fieldname": "outlet", "fieldtype": "Link", "label": "Outlet", "options": "Outlet", "req": 1},
            {"fieldname": "asset", "fieldtype": "Link", "label": "Asset", "options": "Asset", "req": 1},
            {"fieldname": "asset_category", "fieldtype": "Link", "label": "Asset Category", "options": "Asset Category", "req": 1},
            {"fieldname": "source_program", "fieldtype": "Link", "label": "Source Program", "options": "Maintenance Program"},
            {"fieldname": "source_ticket", "fieldtype": "Link", "label": "Source Ticket", "options": "Maintenance Ticket"},
            {"fieldname": "due_date", "fieldtype": "Date", "label": "Due Date"},
            {"fieldname": "completed_date", "fieldtype": "Date", "label": "Completed Date"},
            {"fieldname": "assigned_to", "fieldtype": "Link", "label": "Assigned To", "options": "Maintenance Team Member"},
            {"fieldname": "priority", "fieldtype": "Select", "label": "Priority", "options": "Low\nMedium\nHigh\nCritical", "default": "Medium"},
            {"fieldname": "remarks", "fieldtype": "Small Text", "label": "Remarks"},
            {"fieldname": "completion_notes", "fieldtype": "Small Text", "label": "Completion Notes"},
            {"fieldname": "outcome", "fieldtype": "Select", "label": "Outcome", "options": "Pass\nFail\nPartial\nNot Applicable"},
        ],
        "children": [
            {
                "child_doctype": "Work Order Checklist Result",
                "name": "checklist_results",
                "fields": [
                    {"fieldname": "checklist_item", "fieldtype": "Data", "label": "Checklist Item", "req": 1},
                    {"fieldname": "result", "fieldtype": "Select", "label": "Result", "options": "Pass\nFail\nPartial\nNot Applicable", "req": 1},
                    {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
                    {"fieldname": "failed", "fieldtype": "Check", "label": "Failed", "default": "0"},
                ],
            }
        ],
    },
    "maintenance_ticket": {
        "name": "Maintenance Ticket",
        "fields": [
            {"fieldname": "ticket_no", "fieldtype": "Data", "label": "Ticket No"},
            {"fieldname": "outlet", "fieldtype": "Link", "label": "Outlet", "options": "Outlet", "req": 1},
            {"fieldname": "asset", "fieldtype": "Link", "label": "Asset", "options": "Asset"},
            {"fieldname": "asset_category", "fieldtype": "Link", "label": "Asset Category", "options": "Asset Category"},
            {"fieldname": "department", "fieldtype": "Data", "label": "Department"},
            {"fieldname": "category", "fieldtype": "Data", "label": "Category"},
            {"fieldname": "sub_category_1", "fieldtype": "Data", "label": "Sub Category 1"},
            {"fieldname": "sub_category_2", "fieldtype": "Data", "label": "Sub Category 2"},
            {"fieldname": "issue_summary", "fieldtype": "Data", "label": "Issue Summary", "req": 1},
            {"fieldname": "issue_details", "fieldtype": "Small Text", "label": "Issue Details"},
            {"fieldname": "priority", "fieldtype": "Select", "label": "Priority", "options": "Low\nMedium\nHigh\nCritical", "default": "Medium"},
            {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Open\nAssigned\nIn Progress\nResolved\nClosed\nCancelled", "default": "Open"},
            {"fieldname": "linked_work_order", "fieldtype": "Link", "label": "Linked Work Order", "options": "Maintenance Work Order"},
        ],
    },
    "exception_record": {
        "name": "Exception Record",
        "fields": [
            {"fieldname": "source_file", "fieldtype": "Data", "label": "Source File", "req": 1},
            {"fieldname": "source_row_number", "fieldtype": "Int", "label": "Source Row Number", "req": 1},
            {"fieldname": "source_payload", "fieldtype": "Long Text", "label": "Source Payload", "req": 1},
            {"fieldname": "issue_type", "fieldtype": "Data", "label": "Issue Type", "req": 1},
            {"fieldname": "issue_message", "fieldtype": "Small Text", "label": "Issue Message", "req": 1},
            {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Open\nReview\nResolved", "default": "Open"},
        ],
    },
}


def _doctype_json(name: str, fields: list[dict], istable: bool = False) -> dict:
    naming_by_doctype = {
        "City": "field:city_name",
        "Zonal Office": "field:office_name",
        "Outlet": "field:outlet_code",
        "Asset Category": "field:category_name",
        "Asset": "field:asset_name",
        "Maintenance Team Member": "field:employee_no",
        "Maintenance Program": "field:program_name",
        "Maintenance Program Task": "hash",
        "Work Order Checklist Result": "hash",
        "Maintenance Work Order": "hash",
        "Maintenance Ticket": "hash",
        "Exception Record": "hash",
    }
    return {
        "doctype": "DocType",
        "name": name,
        "module": MODULE,
        "custom": 0,
        "istable": 1 if istable else 0,
        "editable_grid": 1 if istable else 0,
        "fields": fields,
        "autoname": naming_by_doctype.get(name, "hash"),
        "track_changes": 1,
    }


def _controller_py(name: str) -> str:
    class_name = name.replace(" ", "")
    if name == "Maintenance Work Order":
        return '''from frappe.model.document import Document
from frappe.utils import nowdate

from maintenance_ops.api import default_priority_for_asset_category


class MaintenanceWorkOrder(Document):
    def validate(self):
        if self.work_order_type == "Reactive" and not self.priority and self.asset_category:
            self.priority = default_priority_for_asset_category(self.asset_category)
        if self.work_order_type == "Preventive" and self.status == "Draft":
            self.status = "Open"

    def mark_completed(self):
        self.status = "Completed"
        if not self.completed_date:
            self.completed_date = nowdate()
'''
    if name == "Maintenance Ticket":
        return '''from frappe.model.document import Document

from maintenance_ops.api import default_priority_for_asset_category


class MaintenanceTicket(Document):
    def validate(self):
        if self.asset_category and not self.priority:
            self.priority = default_priority_for_asset_category(self.asset_category)

    def create_work_order_seed(self):
        return {
            "work_order_type": "Reactive",
            "outlet": self.outlet,
            "asset": self.asset,
            "asset_category": self.asset_category or "",
            "source_ticket": self.name,
            "priority": self.priority,
            "status": "Open",
        }
'''
    return f'''from frappe.model.document import Document\n\n\nclass {class_name}(Document):\n    pass\n'''


def write_doctype(base: Path, folder: str, spec: dict) -> None:
    doctype_dir = base / folder
    doctype_dir.mkdir(parents=True, exist_ok=True)
    (doctype_dir / "__init__.py").write_text("\n", encoding="utf-8")
    meta_fields = list(spec["fields"])
    for child in spec.get("children", []):
        meta_fields.append(
            {
                "fieldname": child["name"],
                "fieldtype": "Table",
                "label": child["child_doctype"],
                "options": child["child_doctype"],
            }
        )
    meta = _doctype_json(spec["name"], meta_fields)
    (doctype_dir / f"{folder}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (doctype_dir / f"{folder}.py").write_text(_controller_py(spec["name"]), encoding="utf-8")

    for child in spec.get("children", []):
        child_dir = base / child["child_doctype"].lower().replace(" ", "_")
        child_dir.mkdir(parents=True, exist_ok=True)
        (child_dir / "__init__.py").write_text("\n", encoding="utf-8")
        child_meta = _doctype_json(child["child_doctype"], child["fields"], istable=True)
        (child_dir / f"{child_dir.name}.json").write_text(json.dumps(child_meta, indent=2) + "\n", encoding="utf-8")
        (child_dir / f"{child_dir.name}.py").write_text(_controller_py(child["child_doctype"]), encoding="utf-8")


def main() -> None:
    for folder, spec in DOCTYPES.items():
        write_doctype(ROOT, folder, spec)


if __name__ == "__main__":
    main()
