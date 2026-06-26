from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from .config import CITY_ALIASES, DEFAULT_PRIORITY_BY_FREQUENCY, FREQUENCY_TO_DAYS, REACTIVE_PRIORITY_BY_CATEGORY


def normalize_city_code(value: str) -> str:
    text = (value or "").strip()
    return CITY_ALIASES.get(text, text)


def pm_due_date(last_done: Optional[date], frequency: str) -> Optional[date]:
    if not last_done:
        return None
    days = FREQUENCY_TO_DAYS.get(frequency)
    if not days:
        return None
    return last_done + timedelta(days=days)


def default_priority_for_frequency(frequency: str) -> str:
    return DEFAULT_PRIORITY_BY_FREQUENCY.get(frequency, "Medium")


def default_priority_for_asset_category(category: str) -> str:
    return REACTIVE_PRIORITY_BY_CATEGORY.get(category, "Medium")


def build_work_order_seed(*, work_order_type: str, outlet: str, asset: str, asset_category: str, source_ref: str | None = None, due: Optional[date] = None) -> dict:
    priority = default_priority_for_asset_category(asset_category) if work_order_type == "Reactive" else default_priority_for_frequency("Monthly")
    return {
        "work_order_type": work_order_type,
        "outlet": outlet,
        "asset": asset,
        "asset_category": asset_category,
        "source_ref": source_ref,
        "due_date": due,
        "priority": priority,
        "status": "Draft" if work_order_type == "Preventive" else "Open",
    }
