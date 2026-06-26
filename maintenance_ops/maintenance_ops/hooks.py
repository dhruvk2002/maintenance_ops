app_name = "maintenance_ops"
app_title = "Maintenance Ops"
app_publisher = "California Burrito"
app_description = "Maintenance operations management"
app_email = ""
app_license = "MIT"

scheduler_events = {
	"daily": [
		"maintenance_ops.services.generate_due_pm_work_orders",
		"maintenance_ops.services.escalate_overdue_work_orders",
	]
}

doc_events = {
	"Maintenance Ticket": {
		"after_insert": "maintenance_ops.events.on_ticket_after_insert",
	},
	"Maintenance Work Order": {
		"validate": "maintenance_ops.events.on_work_order_validate",
	},
}
