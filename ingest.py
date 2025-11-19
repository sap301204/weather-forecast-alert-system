import httpx
import json
import datetime as dt
from src.db_utils import get_conn
from typing import Dict, Any

OPEN_METEO_TEMPLATE = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&hourly=temperature_2m,relative_humidity_2m,precipitation,precipitation_probability,"
    "wind_speed_10m,wind_gusts_10m,cloud_cover,uv_index,pressure_msl,visibility"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,"
    "wind_speed_10m_max,uv_index_max,sunrise,sunset"
    "&current_weather=true&timezone={tz}"
)

def fetch_open_meteo(lat: float, lon: float, tz: str = "UTC") -> Dict[str, Any]:
    url = OPEN_METEO_TEMPLATE.format(lat=lat, lon=lon, tz=tz)
    with httpx.Client(timeout=20) as c:
        r = c.get(url)
        r.raise_for_status()
        return r.json()

def persist_raw(db_path: str, loc_id: int, payload: dict, scope: str, provider: str="open-meteo"):
    con = get_conn(db_path)
    con.execute(
        "INSERT INTO weather_raw(location_id, fetched_at, scope, provider, payload) VALUES (?, ?, ?, ?, ?)",
        (loc_id, dt.datetime.utcnow().isoformat(), scope, provider, json.dumps(payload))
    )
    con.commit()
    con.close()

def upsert_series(db_path: str, loc_id: int, data: dict):
    con = get_conn(db_path)
    cur = con.cursor()
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    n = len(times)
    def safe_get(arr, i):
        try:
            return arr[i]
        except Exception:
            return None

    for i, ts in enumerate(times):
        cur.execute(""" 
        INSERT OR REPLACE INTO weather_hourly
         (location_id, ts, temp_c, feels_c, humidity, wind_ms, wind_gust_ms, precip_mm, precip_prob, cloud_pct, uv, pressure_hpa, visibility_km, weather_code)
         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            loc_id, ts,
            safe_get(hourly.get("temperature_2m", []), i),
            None,
            safe_get(hourly.get("relative_humidity_2m", []), i),
            safe_get(hourly.get("wind_speed_10m", []), i),
            safe_get(hourly.get("wind_gusts_10m", []), i),
            safe_get(hourly.get("precipitation", []), i),
            safe_get(hourly.get("precipitation_probability", []), i),
            safe_get(hourly.get("cloud_cover", []), i),
            safe_get(hourly.get("uv_index", []), i),
            safe_get(hourly.get("pressure_msl", []), i),
            (safe_get(hourly.get("visibility", []), i) or 0) / 1000.0,
            None
        ))
    daily = data.get("daily", {})
    dtimes = daily.get("time", [])
    for i, date in enumerate(dtimes):
        cur.execute(""" 
        INSERT OR REPLACE INTO weather_daily
         (location_id, date, tmax_c, tmin_c, rain_mm, rain_prob, wind_max_ms, uv_max, sunrise, sunset)
         VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            loc_id, date,
            safe_get(daily.get("temperature_2m_max", []), i),
            safe_get(daily.get("temperature_2m_min", []), i),
            safe_get(daily.get("precipitation_sum", []), i),
            safe_get(daily.get("precipitation_probability_max", []), i),
            safe_get(daily.get("wind_speed_10m_max", []), i),
            safe_get(daily.get("uv_index_max", []), i),
            safe_get(daily.get("sunrise", []), i),
            safe_get(daily.get("sunset", []), i)
        ))
    con.commit()
    con.close()
