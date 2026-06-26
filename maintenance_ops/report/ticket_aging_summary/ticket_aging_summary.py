from __future__ import annotations


def execute(filters=None):
    import frappe

    columns = [
        {"label": "Ticket", "fieldname": "name", "fieldtype": "Link", "options": "Maintenance Ticket", "width": 170},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
        {"label": "Outlet", "fieldname": "outlet", "fieldtype": "Link", "options": "Outlet", "width": 120},
        {"label": "Asset", "fieldname": "asset", "fieldtype": "Link", "options": "Asset", "width": 130},
        {"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 130},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 95},
        {"label": "Age (Days)", "fieldname": "age_days", "fieldtype": "Int", "width": 95},
        {"label": "Created On", "fieldname": "creation", "fieldtype": "Datetime", "width": 165},
    ]

    conditions = ["status in ('Open', 'Assigned', 'In Progress')"]
    values = {}

    if filters and filters.get("outlet"):
        conditions.append("outlet = %(outlet)s")
        values["outlet"] = filters["outlet"]

    if filters and filters.get("priority"):
        conditions.append("priority = %(priority)s")
        values["priority"] = filters["priority"]

    query = f"""
        select
            name,
            status,
            outlet,
            asset,
            category,
            priority,
            timestampdiff(day, creation, now()) as age_days,
            creation
        from `tabMaintenance Ticket`
        where {' and '.join(conditions)}
        order by age_days desc, modified desc
    """

    data = frappe.db.sql(query, values=values, as_dict=True)
    return columns, data
