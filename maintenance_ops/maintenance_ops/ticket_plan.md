# Reactive Ticket Workflow

## Objective
Capture breakdowns and route them to the correct maintenance team member.

## Lifecycle
1. User raises a ticket for an outlet and optionally links an asset.
2. System classifies issue by department, category, and sub-category.
3. Assignment is suggested from city, zonal office, and reporting chain.
4. Technician accepts and works the ticket.
5. Resolution notes and parts recommendations are added.
6. Ticket is closed after verification.

## Routing principle
Ticket assignment should be data-driven:
- outlet city determines zonal office
- zonal office determines maintenance group
- reporting chain determines final assignee

## Spare parts linkage
If a ticket taxonomy maps to a spare-part code, the system should surface that suggestion.

## Exception handling
If taxonomy or outlet mapping is missing, create an exception record instead of blocking the user without explanation.
