# Runbook - Maintenance Ops (Frappe Bench)

## 1) Place app in bench
Copy this app folder into your bench `apps` directory as `maintenance_ops`.

## 2) Install app on site
Run:
- `bench --site <your-site> install-app maintenance_ops`
- `bench --site <your-site> migrate`

## 3) Verify doctypes
Open desk and confirm these doctypes exist:
- City
- Zonal Office
- Outlet
- Asset Category
- Asset
- Maintenance Team Member
- Maintenance Program
- Maintenance Program Task
- Maintenance Work Order
- Work Order Checklist Result
- Maintenance Ticket
- Exception Record

## 4) Validate reactive flow
1. Create `City`, `Zonal Office`, `Outlet`, `Asset Category`, `Asset`.
2. Create `Maintenance Ticket` with outlet + asset + asset category.
3. Save ticket.
4. Verify `linked_work_order` is populated and a `Maintenance Work Order` exists with type `Reactive`.

## 5) Validate PM flow basics
1. Create `Maintenance Program` and add tasks in child table.
2. Create `Maintenance Work Order` with type `Preventive` and status `Draft`.
3. Save and verify status auto-changes to `Open` (validate hook).

## 6) Notes
- Scheduler hooks are registered via `scheduler_events` in hooks.
- Daily jobs are implemented in `maintenance_ops/services.py`.
- Import helpers are available in `maintenance_ops/importers.py` for bootstrapping records from source files.

## 7) Due/Overdue report
- Report name: `Due Overdue Work Orders`
- Type: Script Report
- Ref doctype: `Maintenance Work Order`
- Path: `maintenance_ops/maintenance_ops/report/due_overdue_work_orders`

Open from Desk Reports and optionally filter by `outlet`.

## 8) Ticket aging report
- Report name: `Ticket Aging Summary`
- Type: Script Report
- Ref doctype: `Maintenance Ticket`
- Path: `maintenance_ops/maintenance_ops/report/ticket_aging_summary`

Use this report to show reactive backlog and aging by priority/outlet.

## 9) Optional API calls (whitelisted)
Use `bench execute` or REST endpoint dispatch:
- `maintenance_ops.api_endpoints.seed_data`
- `maintenance_ops.api_endpoints.run_pm_generation`
- `maintenance_ops.api_endpoints.run_overdue_escalation`
- `maintenance_ops.api_endpoints.due_overdue_report`
- `maintenance_ops.api_endpoints.dashboard_summary`
- `maintenance_ops.api_endpoints.ticket_aging_report`
