# Maintenance Ops

A standard Frappe-style custom app for maintenance operations.

## Scope
This app models:
- outlets and cities
- assets and asset categories
- preventive maintenance programs
- unified maintenance work orders
- reactive tickets
- exception handling for bad source rows

## Design principles
- master data separated from transactions
- planned and reactive work share a common operational model
- routing and scheduling are configuration-driven
- ambiguous source data goes to an exception queue

## Build priorities
1. core doctypes
2. preventive maintenance generation
3. ticket intake and routing
4. exception review and cleanup
5. basic reports

## Quick demo commands (bench console)
- Seed masters from datasets:
	- `from maintenance_ops.bootstrap import seed_from_datasets`
	- `seed_from_datasets("/Users/I747860/Desktop/Assesment/datasets")`
	- output now includes `asset_categories`, `assets`, and `maintenance_programs`
- Generate PM work orders:
	- `from maintenance_ops.services import generate_due_pm_work_orders`
	- `generate_due_pm_work_orders()`
- Escalate overdue PM work orders:
	- `from maintenance_ops.services import escalate_overdue_work_orders`
	- `escalate_overdue_work_orders()`
- Get dashboard summary:
	- `from maintenance_ops.reports import get_dashboard_summary`
	- `get_dashboard_summary()`
