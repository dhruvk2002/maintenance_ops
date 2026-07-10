from __future__ import annotations

import frappe

HOME_ROUTE = "/app/maintenance-ops-home"


def set_maintenance_home_page(_login_manager=None):
    user = frappe.session.user
    if user in ("Guest", "Administrator"):
        return

    roles = frappe.get_roles(user)
    if "Desk User" not in roles or "System Manager" in roles:
        return

    frappe.defaults.set_user_default("desktop:home_page", HOME_ROUTE, user=user)
