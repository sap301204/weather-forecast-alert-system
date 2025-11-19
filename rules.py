from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Alert:
    code: str
    label: str
    severity: str

DEFAULT_RULES = [
    {
        "code": "RAIN_SOON",
        "label": "Rain likely in next 12 hours",
        "severity": "warn",
        "condition": lambda ctx: any((p or 0) >= 60 for p in ctx.get("precip_prob_next_12h", []))
    },
    {
        "code": "HEAT_WAVE",
        "label": "High heat tomorrow (>=40°C)",
        "severity": "critical",
        "condition": lambda ctx: (ctx.get("tmax_c_tomorrow") or 0) >= 40
    },
    {
        "code": "WIND_HIGH",
        "label": "High wind gusts (>=15 m/s) next 24h",
        "severity": "warn",
        "condition": lambda ctx: any((g or 0) >= 15 for g in ctx.get("gust_next_24h", []))
    },
    {
        "code": "UV_HIGH",
        "label": "High UV index today (>=8)",
        "severity": "warn",
        "condition": lambda ctx: (ctx.get("uv_max_today") or 0) >= 8
    }
]

def evaluate(hourly_rows: List[Dict[str,Any]], daily_rows: List[Dict[str,Any]]):
    precip_prob_next_12h = [r.get("precip_prob") for r in hourly_rows[:12]]
    gust_next_24h = [r.get("wind_gust_ms") for r in hourly_rows[:24]]
    ctx_h = {"precip_prob_next_12h": precip_prob_next_12h, "gust_next_24h": gust_next_24h}
    ctx_d = {
        "tmax_c_tomorrow": daily_rows[1]["tmax_c"] if len(daily_rows) > 1 else None,
        "uv_max_today": daily_rows[0]["uv_max"] if len(daily_rows) > 0 else None
    }
    fired = []
    for rule in DEFAULT_RULES:
        try:
            if rule["code"] == "RAIN_SOON":
                if rule["condition"](ctx_h):
                    fired.append({"code": rule["code"], "label": rule["label"], "severity": rule["severity"]})
            else:
                if rule["condition"](ctx_d):
                    fired.append({"code": rule["code"], "label": rule["label"], "severity": rule["severity"]})
        except Exception:
            continue
    return fired
