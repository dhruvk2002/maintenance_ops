from __future__ import annotations

PM_WORKFLOW = [
    "Draft",
    "Open",
    "Due",
    "Overdue",
    "In Progress",
    "Completed",
    "Closed",
    "Cancelled",
]

TICKET_WORKFLOW = [
    "Open",
    "Assigned",
    "In Progress",
    "Resolved",
    "Closed",
    "Cancelled",
]

EXCEPTION_WORKFLOW = [
    "Open",
    "Review",
    "Resolved",
]


def next_status(current_status: str, work_order_type: str) -> str:
    if work_order_type == "Preventive":
        transitions = {
            "Draft": "Open",
            "Open": "Due",
            "Due": "Overdue",
            "Overdue": "In Progress",
            "In Progress": "Completed",
            "Completed": "Closed",
        }
        return transitions.get(current_status, current_status)

    if work_order_type == "Reactive":
        transitions = {
            "Open": "Assigned",
            "Assigned": "In Progress",
            "In Progress": "Resolved",
            "Resolved": "Closed",
        }
        return transitions.get(current_status, current_status)

    return current_status
