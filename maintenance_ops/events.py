from __future__ import annotations

from .services import create_reactive_work_order_from_ticket


def on_ticket_after_insert(doc, method=None):
    if not getattr(doc, "linked_work_order", None):
        work_order = create_reactive_work_order_from_ticket(doc)
        doc.db_set("linked_work_order", work_order.name)


def on_work_order_validate(doc, method=None):
    if doc.work_order_type == "Preventive" and doc.status == "Draft":
        doc.status = "Open"
