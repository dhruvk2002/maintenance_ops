from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass(slots=True)
class City:
    name: str
    short_code: str
    active: bool = True


@dataclass(slots=True)
class ZonalOffice:
    name: str
    city: str
    manager: Optional[str] = None
    active: bool = True


@dataclass(slots=True)
class Outlet:
    outlet_code: str
    outlet_name: str
    city: str
    zonal_office: Optional[str] = None
    active: bool = True


@dataclass(slots=True)
class AssetCategory:
    name: str
    description: str = ""
    active: bool = True


@dataclass(slots=True)
class Asset:
    asset_name: str
    outlet: str
    category: str
    asset_code: Optional[str] = None
    serial_no: Optional[str] = None
    install_date: Optional[date] = None
    status: str = "Active"


@dataclass(slots=True)
class MaintenanceTask:
    task_name: str
    checklist_instructions: str = ""
    expected_result: str = ""
    mandatory: bool = True
    sort_order: int = 0


@dataclass(slots=True)
class MaintenanceProgram:
    program_name: str
    asset_category: str
    frequency: str
    lead_time_days: int = 0
    active: bool = True
    description: str = ""
    tasks: list[MaintenanceTask] = field(default_factory=list)


@dataclass(slots=True)
class TeamMember:
    employee_no: str
    employee_name: str
    job_title: str
    department: str
    email: str = ""
    mobile: str = ""
    reports_to: Optional[str] = None
    home_office: Optional[str] = None
    active: bool = True


@dataclass(slots=True)
class WorkOrder:
    work_order_type: str
    outlet: str
    asset: str
    asset_category: str
    status: str = "Draft"
    source_program: Optional[str] = None
    source_ticket: Optional[str] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    assigned_to: Optional[str] = None
    priority: str = "Medium"
    remarks: str = ""
    completion_notes: str = ""
    outcome: str = ""


@dataclass(slots=True)
class Ticket:
    outlet: str
    issue_summary: str
    department: str = ""
    category: str = ""
    sub_category_1: str = ""
    sub_category_2: str = ""
    asset: Optional[str] = None
    priority: str = "Medium"
    status: str = "Open"
    linked_work_order: Optional[str] = None
    suggested_spare_parts: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ExceptionRecord:
    source_file: str
    source_row_number: int
    issue_type: str
    issue_message: str
    source_payload: str
    status: str = "Open"
