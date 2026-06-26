from __future__ import annotations

from collections.abc import Iterable


def choose_technician(team_members: Iterable[dict], *, city: str | None = None, home_office: str | None = None, role_priority: tuple[str, ...] = ("Maintenance Incharge", "Assistant Manager", "Senior Executive", "Executive")) -> dict | None:
    """Pick the best technician from a list of team member records.

    This is a simple deterministic rule set:
    1. Prefer members matching the outlet city / home office.
    2. Prefer higher responsibility roles.
    3. Fall back to the first available record.
    """
    members = list(team_members)
    if not members:
        return None

    filtered = members
    if home_office:
        filtered = [m for m in filtered if (m.get("home_office") or "") == home_office] or filtered
    if city:
        filtered = [m for m in filtered if city.lower() in (m.get("home_office") or "").lower()] or filtered

    role_rank = {role: idx for idx, role in enumerate(role_priority)}
    return sorted(filtered, key=lambda m: role_rank.get(m.get("job_title") or "", len(role_priority)))[0]


def route_by_city(outlet_city: str, city_to_office: dict[str, str]) -> str | None:
    return city_to_office.get(outlet_city)
