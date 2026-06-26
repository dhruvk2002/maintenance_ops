from frappe.model.document import Document
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
