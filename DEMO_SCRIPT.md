# Demo Script (7-10 min) - Maintenance Ops

## Objective
Show a working v1 that covers PM + reactive maintenance with assignment and reporting.

## 0) One-time setup (before call)
1. Install app on site.
2. Run data seed.
3. Generate PM work orders.

## 1) Seed data (1 min)
In bench console:
- `from maintenance_ops.bootstrap import seed_from_datasets`
- `seed_from_datasets("/Users/I747860/Desktop/Assesment/datasets")`

What to say:
- "This creates cities, zonal offices, outlets, maintenance team members, asset categories, assets, and PM programs with tasks from the source files."

## 2) Show model shape (1 min)
Open these doctypes in Desk:
- `Maintenance Program` (template)
- `Maintenance Work Order` (transaction)
- `Maintenance Ticket` (reactive intake)

What to say:
- "Planned and unplanned maintenance share the same work-order backbone for unified status, assignment, and reporting."

## 3) PM generation + overdue handling (2 min)
In bench console:
- `from maintenance_ops.services import generate_due_pm_work_orders, escalate_overdue_work_orders`
- `generate_due_pm_work_orders()`
- `escalate_overdue_work_orders()`

Then open report:
- `Due Overdue Work Orders`

What to say:
- "PM programs are defined once and rolled across assets. Due/overdue are visible as operational queue."

## 4) Reactive flow and auto-assignment (2 min)
Create one `Maintenance Ticket` in Desk with outlet + asset category.
Save the ticket.

Show:
- `linked_work_order` auto-populated on ticket
- created `Maintenance Work Order` has `work_order_type = Reactive`
- assignee populated by city -> zonal office -> technician routing

What to say:
- "Ticket creation triggers work-order creation and assignment using org structure."

## 5) Reactive operations view (1 min)
Open report:
- `Ticket Aging Summary`

What to say:
- "This gives backlog aging by priority/outlet for day-to-day control."

## 6) Dashboard API summary (1 min)
In bench console:
- `from maintenance_ops.reports import get_dashboard_summary`
- `get_dashboard_summary()`

What to say:
- "This gives PM due/overdue plus reactive open and aging buckets for lightweight dashboard cards."

## 7) Scope cuts (30 sec)
Say clearly:
- "I intentionally cut inventory/procurement and advanced SLA escalation to keep v1 stable and demonstrable."

## 8) Assumptions to mention (30 sec)
- Outlet code is stable primary identifier.
- Frequency values from source are normalized into supported set.
- Ambiguous rows are logged to `Exception Record` instead of silent failure.
