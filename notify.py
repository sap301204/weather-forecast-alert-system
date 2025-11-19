import datetime as dt
import requests
from src.db_utils import get_conn

DB = "db/weather.db"

def telegram_send(bot_token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        requests.get(url, params={"chat_id": chat_id, "text": text}, timeout=10)
    except Exception as e:
        print("Telegram send failed:", e)

def dispatch_if_new(location_id: int, alerts: list, db_path: str = DB, tg_token: str=None, tg_chat_id: str=None):
    con = get_conn(db_path)
    cur = con.cursor()
    for a in alerts:
        recent = cur.execute(
            "SELECT 1 FROM alert_log WHERE location_id=? AND code=? AND sent_at >= datetime('now','-12 hours')",
            (location_id, a["code"])
        ).fetchone()
        if recent:
            continue
        if tg_token and tg_chat_id:
            telegram_send(tg_token, tg_chat_id, f"⚠️ {a['label']} ({a['severity'].upper()}) for location {location_id}")
        cur.execute("INSERT INTO alert_log(location_id, code, sent_at) VALUES (?, ?, datetime('now'))",
                    (location_id, a["code"]))
    con.commit()
    con.close()
