from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from src.db_utils import get_conn
from src.rules import evaluate

DB = "db/weather.db"
app = FastAPI(title="Weather Forecast & Alerts API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def query(sql, params=()):
    con = get_conn(DB)
    rows = con.execute(sql, params).fetchall()
    con.close()
    return [dict(r) for r in rows]

@app.get("/locations")
def get_locations():
    return query("SELECT * FROM locations ORDER BY name")

@app.get("/forecast/hourly")
def forecast_hourly(location_id: int = Query(...), hours: int = 24):
    rows = query("""SELECT * FROM weather_hourly WHERE location_id=? AND ts >= datetime('now') ORDER BY ts LIMIT ?""", (location_id, hours))
    return rows

@app.get("/forecast/daily")
def forecast_daily(location_id: int = Query(...), days: int = 7):
    rows = query("""SELECT * FROM weather_daily WHERE location_id=? AND date >= date('now') ORDER BY date LIMIT ?""", (location_id, days))
    return rows

@app.get("/alerts")
def alerts(location_id: int = Query(...)):
    hourly = query("""SELECT location_id, ts, temp_c, feels_c, humidity, wind_ms, wind_gust_ms, precip_mm, precip_prob, cloud_pct, uv, pressure_hpa, visibility_km, weather_code FROM weather_hourly WHERE location_id=? AND ts>=datetime('now') ORDER BY ts LIMIT 48""", (location_id,))
    daily = query("""SELECT location_id, date, tmax_c, tmin_c, rain_mm, rain_prob, wind_max_ms, uv_max, sunrise, sunset FROM weather_daily WHERE location_id=? AND date>=date('now') ORDER BY date LIMIT 3""", (location_id,))
    fired = evaluate(hourly, daily)
    return {"alerts": fired}

# Optional scheduler (APScheduler)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)
