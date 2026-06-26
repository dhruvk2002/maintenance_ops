from frappe.model.document import Document

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
