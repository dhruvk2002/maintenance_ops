from __future__ import annotations

CITY_ALIASES = {
    "BLR": "Bengaluru",
    "Bengaluru": "Bengaluru",
    "NCR": "Delhi/NCR",
    "Delhi/NCR": "Delhi/NCR",
    "HYD": "Hyderabad",
    "CHN": "Chennai",
    "PUN": "Pune",
    "MUM": "Mumbai",
}

FREQUENCY_TO_DAYS = {
    "Weekly": 7,
    "Monthly": 30,
    "Qtrly": 90,
    "Quarterly": 90,
    "Half-Yearly": 182,
    "6 month": 182,
    "Yearly": 365,
}

DEFAULT_PRIORITY_BY_FREQUENCY = {
    "Weekly": "Medium",
    "Monthly": "Medium",
    "Qtrly": "High",
    "Quarterly": "High",
    "Half-Yearly": "High",
    "6 month": "High",
    "Yearly": "High",
}

REACTIVE_PRIORITY_BY_CATEGORY = {
    "Fire Extinguisher": "Critical",
    "DG Set & AMF Panel": "High",
    "AC": "High",
}
