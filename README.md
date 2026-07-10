# Maintenance Ops

A custom Frappe / ERPNext app for California Burrito's maintenance operations.
It manages outlets, assets, preventive-maintenance (PM) programs, reactive tickets, and work orders.

---

## Live Site

| Item                  | Value                                         |
| --------------------- | --------------------------------------------- |
| **Cloud URL**   | https://maintainance.m.frappe.cloud           |
| Email                 | deepikasinghns1@gmail.com                     |
| **Password**    | Cbassesment@2026                              |
| **GitHub Repo** | https://github.com/dhruvk2002/maintenance_ops |

---

## Tech Stack

- Frappe v15 + ERPNext v15
- Custom app: `maintenance_ops` v0.0.1
- MariaDB 12.3 (local) / Frappe Cloud managed DB
- Python 3.11

---

## App Structure

```
maintenance_ops/
├── maintenance_ops/          # Python package
│   ├── doctype/              # 12 custom DocTypes
│   │   ├── asset/
│   │   ├── asset_category/
│   │   ├── city/
│   │   ├── exception_record/
│   │   ├── maintenance_program/
│   │   ├── maintenance_program_task/
│   │   ├── maintenance_team_member/
│   │   ├── maintenance_ticket/
│   │   ├── maintenance_work_order/
│   │   ├── outlet/
│   │   ├── work_order_checklist_result/
│   │   └── zonal_office/
│   ├── report/               # 2 custom Reports
│   │   ├── due_overdue_work_orders/
│   │   └── ticket_aging_summary/
│   ├── bootstrap.py          # Seed data from datasets
│   ├── services.py           # PM generation + escalation logic
│   ├── events.py             # Doc event hooks
│   ├── routing.py            # Team assignment logic
│   ├── scheduling.py         # PM due-date scheduling
│   └── hooks.py
```

---

## Local Setup (from scratch)

### Prerequisites

- Python 3.11, Node 18, MariaDB (running on port 3307 with socket `/tmp/mariadb3307.sock`)
- Frappe Bench installed

### 1 – Clone the app

```bash
cd frappe-bench/apps
git clone https://github.com/dhruvk2002/maintenance_ops
```

### 2 – Create & configure the site

```bash
bench new-site maintenanceops.localhost \
  --db-port 3307 \
  --db-root-username <mariadb_user> \
  --mariadb-root-password <mariadb_password>
```

### 3 – Install ERPNext + maintenance_ops

```bash
bench get-app erpnext --branch version-15
bench --site maintenanceops.localhost install-app erpnext
bench --site maintenanceops.localhost install-app maintenance_ops
bench --site maintenanceops.localhost migrate
```

### 4 – Load seed data

```bash
bench --site maintenanceops.localhost console
```

Inside the console:

```python
from maintenance_ops.bootstrap import seed_from_datasets
seed_from_datasets("/path/to/datasets")
# Expected output:
# cities=5, zonal_offices=?, outlets=133, asset_categories=19,
# assets=142, maintenance_programs=35, team_members=41, exceptions=18
```

### 5 – Start bench

```bash
bench start
```

Open http://maintenanceops.localhost:8000 and log in as **Administrator**.

---

## Testing Guide (Cloud Site)

Open https://assesment.m.frappe.cloud and log in with the credentials from the table above.

---

### Test 1 – Verify Seed Data

1. Go to **Maintenance Ops > Masters > Outlet** → expect **133 records**
2. Go to **Maintenance Ops > Masters > Asset** → expect **142 records**
3. Go to **Maintenance Ops > Masters > Maintenance Program** → expect **35 records**
4. Go to **Maintenance Ops > Masters > Maintenance Team Member** → expect **41 records**
5. Go to **Maintenance Ops > Masters > City** → expect **5 records**

---

### Test 2 – Create a Maintenance Ticket (Reactive)

1. Go to **Maintenance Ops > Transactions > Maintenance Ticket**
2. Click **New**
3. Fill in:
   - **Outlet**: pick any outlet (e.g. `CB-001`)
   - **Asset**: pick any asset linked to that outlet
   - **Description**: `AC unit not cooling`
   - **Reported By**: any name
4. Click **Save**
5. **Expected**: A **Maintenance Work Order** is automatically created (type = `Reactive`) and linked to the ticket. Check the linked Work Order field on the ticket form.

---

### Test 3 – Manually Generate PM Work Orders

1. Go to **Maintenance Ops > Transactions > Maintenance Work Order**
2. Note the current count
3. Open **bench console** (local) or use the Frappe API endpoint:

```bash
bench --site maintenanceops.localhost console
```

```python
from maintenance_ops.services import generate_due_pm_work_orders
result = generate_due_pm_work_orders()
print(result)
```

4. Refresh the Work Order list → new **Preventive** type work orders should appear for programs that are due today.

---

### Test 4 – Work Order Lifecycle

1. Open any **Maintenance Work Order**
2. Walk through status transitions:
   - `Draft` → **Submit** → `Open`
   - Open → set **Assigned To** (team member) → **Start** → `In Progress`
   - In Progress → fill **Completion Notes** → **Complete** → `Completed`
3. **Expected**: Status field updates correctly at each step; `completed_on` date is set when completed.

---

### Test 5 – Escalation Logic

1. Open **bench console** (local):

```python
from maintenance_ops.services import escalate_overdue_work_orders
result = escalate_overdue_work_orders()
print(result)   # returns count of work orders escalated
```

2. Any Work Order with `due_date < today` and status `Open` or `In Progress` should have its **priority** bumped to `High` (or `Critical` if already `High`).

---

### Test 6 – Due / Overdue Work Orders Report

1. Go to **Maintenance Ops > Reports > Due Overdue Work Orders**
2. Apply filters (optional: filter by outlet or date range)
3. **Expected**: Table showing work orders with columns — Outlet, Asset, Type, Due Date, Status, Days Overdue, Priority

---

### Test 7 – Ticket Aging Summary Report

1. Go to **Maintenance Ops > Reports > Ticket Aging Summary**
2. **Expected**: Grouped summary of tickets by age bucket (e.g. 0–7 days, 8–15 days, 15+ days), showing open vs closed counts.

---

### Test 8 – Exception Records

1. Go to **Maintenance Ops > Masters > Exception Record**
2. **Expected**: ~18 records representing rows from the source dataset that could not be cleanly mapped (duplicate assets, missing outlets, etc.)
3. Each record has a **reason** field explaining why it was flagged.

---

## Scheduler Events (Auto-runs daily on production)

| Event | Function                                  | What it does                                   |
| ----- | ----------------------------------------- | ---------------------------------------------- |
| Daily | `services.generate_due_pm_work_orders`  | Creates PM work orders for programs due today  |
| Daily | `services.escalate_overdue_work_orders` | Escalates priority on overdue open work orders |

---

## Key Business Rules

| Rule                                         | Implementation                              |
| -------------------------------------------- | ------------------------------------------- |
| Reactive ticket → auto work order           | `events.on_ticket_after_insert`           |
| Work order priority from asset category      | `api.default_priority_for_asset_category` |
| PM due date from last completion + frequency | `api.pm_due_date`                         |
| Team member routing by outlet/zone           | `routing.py`                              |
| City code normalisation (aliases)            | `config.CITY_ALIASES`                     |

---

## DocTypes Reference

| DocType                     | Type        | Purpose                             |
| --------------------------- | ----------- | ----------------------------------- |
| City                        | Master      | City master                         |
| Zonal Office                | Master      | Zone grouping for outlets           |
| Outlet                      | Master      | Individual restaurant/outlet        |
| Asset Category              | Master      | Category of equipment               |
| Asset                       | Master      | Individual piece of equipment       |
| Maintenance Team Member     | Master      | Technician/engineer                 |
| Maintenance Program         | Master      | PM schedule (asset × frequency)    |
| Maintenance Program Task    | Child       | Task checklist for a program        |
| Maintenance Ticket          | Transaction | Reactive fault report               |
| Maintenance Work Order      | Transaction | Planned or reactive work item       |
| Work Order Checklist Result | Child       | Checklist completion per work order |
| Exception Record            | Log         | Bad/unmappable rows from seed data  |
