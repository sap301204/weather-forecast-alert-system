import sqlite3
from pathlib import Path

DB_PATH = Path("db/weather.db")
SCHEMA = Path("db/schema.sql").read_text()

def init_db(db_path=DB_PATH):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.executescript(SCHEMA)
    con.commit()
    con.close()

def get_conn(db=DB_PATH):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    return con
