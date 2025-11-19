import time
from src.db_utils import get_conn
from src.ingest import fetch_open_meteo, persist_raw, upsert_series

DB = "db/weather.db"

def refresh_all(db=DB):
    con = get_conn(db)
    rows = con.execute("SELECT id, lat, lon, tz FROM locations").fetchall()
    con.close()
    for r in rows:
        loc_id = r["id"]
        lat = r["lat"]
        lon = r["lon"]
        tz = r["tz"] or "UTC"
        try:
            payload = fetch_open_meteo(lat, lon, tz)
            persist_raw(db, loc_id, payload, scope="full", provider="open-meteo")
            upsert_series(db, loc_id, payload)
            print(f"Refreshed {loc_id}")
        except Exception as e:
            print(f"Failed to refresh {loc_id}: {e}")

if __name__ == '__main__':
    refresh_all()
