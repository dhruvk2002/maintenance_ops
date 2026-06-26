from __future__ import annotations

try:
    import frappe
except Exception:
    frappe = None


def get_due_overdue_work_orders() -> dict:
    if frappe is None:
        return {"due": [], "overdue": [], "counts": {"due": 0, "overdue": 0}}

    due = frappe.get_all(
        "Maintenance Work Order",
        filters={"status": "Due"},
        fields=["name", "outlet", "asset", "assigned_to", "due_date", "priority"],
        order_by="due_date asc",
    )
    overdue = frappe.get_all(
        "Maintenance Work Order",
        filters={"status": "Overdue"},
        fields=["name", "outlet", "asset", "assigned_to", "due_date", "priority"],
        order_by="due_date asc",
    )

    return {
        "due": due,
        "overdue": overdue,
        "counts": {"due": len(due), "overdue": len(overdue)},
    }


def get_dashboard_summary() -> dict:
    if frappe is None:
        return {
            "open_tickets": 0,
            "reactive_open_work_orders": 0,
            "pm_due": 0,
            "pm_overdue": 0,
        }

    open_tickets = frappe.db.count("Maintenance Ticket", {"status": ["in", ["Open", "Assigned", "In Progress"]]})
    reactive_open_work_orders = frappe.db.count(
        "Maintenance Work Order",
        {"work_order_type": "Reactive", "status": ["in", ["Open", "Due", "In Progress"]]},
    )
    pm_due = frappe.db.count("Maintenance Work Order", {"work_order_type": "Preventive", "status": "Due"})
    pm_overdue = frappe.db.count("Maintenance Work Order", {"work_order_type": "Preventive", "status": "Overdue"})

    aging_0_2 = frappe.db.sql(
        """
        select count(*) as cnt
        from `tabMaintenance Ticket`
        where status in ('Open', 'Assigned', 'In Progress')
          and timestampdiff(day, creation, now()) between 0 and 2
        """,
        as_dict=True,
    )[0]["cnt"]
    aging_3_7 = frappe.db.sql(
        """
        select count(*) as cnt
        from `tabMaintenance Ticket`
        where status in ('Open', 'Assigned', 'In Progress')
          and timestampdiff(day, creation, now()) between 3 and 7
        """,
        as_dict=True,
    )[0]["cnt"]
    aging_gt_7 = frappe.db.sql(
        """
        select count(*) as cnt
        from `tabMaintenance Ticket`
        where status in ('Open', 'Assigned', 'In Progress')
          and timestampdiff(day, creation, now()) > 7
        """,
        as_dict=True,
    )[0]["cnt"]

    return {
        "open_tickets": open_tickets,
        "reactive_open_work_orders": reactive_open_work_orders,
        "pm_due": pm_due,
        "pm_overdue": pm_overdue,
        "ticket_aging": {
            "0_2_days": aging_0_2,
            "3_7_days": aging_3_7,
            "gt_7_days": aging_gt_7,
        },
    }
