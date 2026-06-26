from __future__ import annotations

from datetime import date

from .api import pm_due_date


def is_due(last_done: date | None, frequency: str, as_of: date | None = None) -> bool:
    as_of = as_of or date.today()
    due = pm_due_date(last_done, frequency)
    return bool(due and due <= as_of)


def is_overdue(last_done: date | None, frequency: str, as_of: date | None = None) -> bool:
    return is_due(last_done, frequency, as_of=as_of)
