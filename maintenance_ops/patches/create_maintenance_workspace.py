from __future__ import annotations

import json

import frappe


WORKSPACE_NAME = "Maintenance Ops Home"
HOME_ROUTE = "/app/maintenance-ops-home"


def _build_content() -> str:
    blocks = [
        {
            "id": "mo-header-actions",
            "type": "header",
            "data": {"text": "<span class=\"h4\"><b>Quick Actions</b></span>", "col": 12},
        },
        {"id": "mo-shortcut-ticket-new", "type": "shortcut", "data": {"shortcut_name": "Create Ticket", "col": 3}},
        {"id": "mo-shortcut-wo-list", "type": "shortcut", "data": {"shortcut_name": "Work Orders", "col": 3}},
        {"id": "mo-shortcut-ticket-list", "type": "shortcut", "data": {"shortcut_name": "Tickets", "col": 3}},
        {"id": "mo-shortcut-pm-list", "type": "shortcut", "data": {"shortcut_name": "PM Programs", "col": 3}},
        {"id": "mo-shortcut-asset-list", "type": "shortcut", "data": {"shortcut_name": "Assets", "col": 3}},
        {"id": "mo-shortcut-outlet-list", "type": "shortcut", "data": {"shortcut_name": "Outlets", "col": 3}},
        {"id": "mo-shortcut-team-list", "type": "shortcut", "data": {"shortcut_name": "Team Members", "col": 3}},
        {"id": "mo-shortcut-exception-list", "type": "shortcut", "data": {"shortcut_name": "Exceptions", "col": 3}},
        {"id": "mo-spacer-1", "type": "spacer", "data": {"col": 12}},
        {
            "id": "mo-header-cards",
            "type": "header",
            "data": {"text": "<span class=\"h4\"><b>Browse</b></span>", "col": 12},
        },
        {"id": "mo-card-operations", "type": "card", "data": {"card_name": "Operations", "col": 4}},
        {"id": "mo-card-masters", "type": "card", "data": {"card_name": "Masters", "col": 4}},
        {"id": "mo-card-reports", "type": "card", "data": {"card_name": "Reports", "col": 4}},
    ]
    return json.dumps(blocks)


def _apply_shortcuts(workspace):
    workspace.set("shortcuts", [])
    shortcuts = [
        {
            "label": "Create Ticket",
            "type": "DocType",
            "link_to": "Maintenance Ticket",
            "doc_view": "New",
            "color": "red",
        },
        {
            "label": "Work Orders",
            "type": "DocType",
            "link_to": "Maintenance Work Order",
            "doc_view": "List",
            "color": "orange",
        },
        {
            "label": "Tickets",
            "type": "DocType",
            "link_to": "Maintenance Ticket",
            "doc_view": "List",
            "color": "blue",
        },
        {
            "label": "PM Programs",
            "type": "DocType",
            "link_to": "Maintenance Program",
            "doc_view": "List",
            "color": "green",
        },
        {
            "label": "Assets",
            "type": "DocType",
            "link_to": "Asset",
            "doc_view": "List",
            "color": "cyan",
        },
        {
            "label": "Outlets",
            "type": "DocType",
            "link_to": "Outlet",
            "doc_view": "List",
            "color": "yellow",
        },
        {
            "label": "Team Members",
            "type": "DocType",
            "link_to": "Maintenance Team Member",
            "doc_view": "List",
            "color": "light-blue",
        },
        {
            "label": "Exceptions",
            "type": "DocType",
            "link_to": "Exception Record",
            "doc_view": "List",
            "color": "pink",
        },
    ]
    for row in shortcuts:
        workspace.append("shortcuts", row)


def _apply_links(workspace):
    workspace.set("links", [])
    links = [
        {"type": "Card Break", "label": "Operations"},
        {"type": "Link", "label": "Maintenance Tickets", "link_type": "DocType", "link_to": "Maintenance Ticket"},
        {"type": "Link", "label": "Maintenance Work Orders", "link_type": "DocType", "link_to": "Maintenance Work Order"},
        {"type": "Link", "label": "Maintenance Programs", "link_type": "DocType", "link_to": "Maintenance Program"},
        {"type": "Card Break", "label": "Masters"},
        {"type": "Link", "label": "Outlets", "link_type": "DocType", "link_to": "Outlet"},
        {"type": "Link", "label": "Assets", "link_type": "DocType", "link_to": "Asset"},
        {"type": "Link", "label": "Asset Categories", "link_type": "DocType", "link_to": "Asset Category"},
        {"type": "Link", "label": "Cities", "link_type": "DocType", "link_to": "City"},
        {"type": "Link", "label": "Zonal Offices", "link_type": "DocType", "link_to": "Zonal Office"},
        {"type": "Link", "label": "Team Members", "link_type": "DocType", "link_to": "Maintenance Team Member"},
        {"type": "Link", "label": "Exceptions", "link_type": "DocType", "link_to": "Exception Record"},
        {"type": "Card Break", "label": "Reports"},
        {
            "type": "Link",
            "label": "Due Overdue Work Orders",
            "link_type": "Report",
            "link_to": "Due Overdue Work Orders",
            "is_query_report": 0,
        },
        {
            "type": "Link",
            "label": "Ticket Aging Summary",
            "link_type": "Report",
            "link_to": "Ticket Aging Summary",
            "is_query_report": 0,
        },
    ]
    for row in links:
        workspace.append("links", row)


def _apply_roles(workspace):
    workspace.set("roles", [])
    for role in ("Desk User", "System Manager"):
        workspace.append("roles", {"role": role})


def _set_home_page_for_users():
    users = frappe.get_all(
        "User",
        filters={"enabled": 1, "user_type": "System User", "name": ["not in", ["Administrator", "Guest"]]},
        pluck="name",
    )
    for user in users:
        if "Desk User" in frappe.get_roles(user):
            frappe.defaults.set_user_default("desktop:home_page", HOME_ROUTE, user=user)


def execute():
    if frappe.db.exists("Workspace", WORKSPACE_NAME):
        workspace = frappe.get_doc("Workspace", WORKSPACE_NAME)
    else:
        workspace = frappe.new_doc("Workspace")
        workspace.label = WORKSPACE_NAME

    workspace.title = WORKSPACE_NAME
    workspace.module = "Maintenance Ops"
    workspace.public = 1
    workspace.is_hidden = 0
    workspace.hide_custom = 1
    workspace.content = _build_content()

    _apply_shortcuts(workspace)
    _apply_links(workspace)
    _apply_roles(workspace)

    workspace.flags.ignore_permissions = True
    workspace.save()

    _set_home_page_for_users()
    frappe.db.commit()
