from __future__ import annotations


def execute(filters=None):
    import frappe

    columns = [
        {"label": "Work Order", "fieldname": "name", "fieldtype": "Link", "options": "Maintenance Work Order", "width": 160},
        {"label": "Type", "fieldname": "work_order_type", "fieldtype": "Data", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Outlet", "fieldname": "outlet", "fieldtype": "Link", "options": "Outlet", "width": 120},
        {"label": "Asset", "fieldname": "asset", "fieldtype": "Link", "options": "Asset", "width": 140},
        {"label": "Assigned To", "fieldname": "assigned_to", "fieldtype": "Link", "options": "Maintenance Team Member", "width": 130},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 110},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 90},
    ]

    conditions = ["status in ('Due', 'Overdue')"]
    values = {}
    if filters and filters.get("outlet"):
        conditions.append("outlet = %(outlet)s")
        values["outlet"] = filters["outlet"]

    query = f"""
        select
            name,
            work_order_type,
            status,
            outlet,
            asset,
            assigned_to,
            due_date,
            priority
        from `tabMaintenance Work Order`
        where {' and '.join(conditions)}
        order by
            case when status = 'Overdue' then 0 else 1 end,
            due_date asc,
            modified desc
    """
    data = frappe.db.sql(query, values=values, as_dict=True)

    return columns, data
