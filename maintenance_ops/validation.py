from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ValidationIssue:
    issue_type: str
    message: str
    row_number: int | None = None
    payload: str | None = None


def require_value(value: object, issue_type: str, message: str, row_number: int | None = None, payload: str | None = None) -> ValidationIssue | None:
    if value is None or value == "":
        return ValidationIssue(issue_type=issue_type, message=message, row_number=row_number, payload=payload)
    return None


def normalize_text(value: object) -> str:
    return str(value).strip() if value is not None else ""
