PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS locations(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  lat REAL NOT NULL,
  lon REAL NOT NULL,
  tz TEXT NOT NULL,
  UNIQUE(lat, lon)
);

CREATE TABLE IF NOT EXISTS weather_raw(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  location_id INTEGER,
  fetched_at TEXT,
  scope TEXT,
  provider TEXT,
  payload TEXT,
  FOREIGN KEY(location_id) REFERENCES locations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS weather_hourly(
  location_id INTEGER,
  ts TEXT,
  temp_c REAL,
  feels_c REAL,
  humidity REAL,
  wind_ms REAL,
  wind_gust_ms REAL,
  precip_mm REAL,
  precip_prob REAL,
  cloud_pct REAL,
  uv REAL,
  pressure_hpa REAL,
  visibility_km REAL,
  weather_code INTEGER,
  PRIMARY KEY(location_id, ts),
  FOREIGN KEY(location_id) REFERENCES locations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS weather_daily(
  location_id INTEGER,
  date TEXT,
  tmax_c REAL,
  tmin_c REAL,
  rain_mm REAL,
  rain_prob REAL,
  wind_max_ms REAL,
  uv_max REAL,
  sunrise TEXT,
  sunset TEXT,
  PRIMARY KEY(location_id, date),
  FOREIGN KEY(location_id) REFERENCES locations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS alert_log(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  location_id INTEGER,
  code TEXT,
  sent_at TEXT,
  FOREIGN KEY(location_id) REFERENCES locations(id) ON DELETE CASCADE
);
