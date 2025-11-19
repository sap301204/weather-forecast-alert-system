import streamlit as st
import requests

API_ROOT = "http://127.0.0.1:8000"

st.title("Weather Forecast & Alerts — Demo")

try:
    locs = requests.get(f"{API_ROOT}/locations", timeout=5).json()
except Exception:
    st.error("API not reachable at http://127.0.0.1:8000")
    st.stop()

if not locs:
    st.warning("No locations found. Seed database first.")
    st.stop()

sel = st.selectbox("Location", options=[(l["id"], l["name"]) for l in locs], format_func=lambda x: x[1])
loc_id = sel[0]

hourly = requests.get(f"{API_ROOT}/forecast/hourly", params={"location_id": loc_id, "hours": 48}).json()
daily = requests.get(f"{API_ROOT}/forecast/daily", params={"location_id": loc_id, "days": 7}).json()
alerts = requests.get(f"{API_ROOT}/alerts", params={"location_id": loc_id}).json().get("alerts", [])

st.subheader("Alerts")
for a in alerts:
    st.error(f"{a['severity'].upper()} — {a['label']} ({a['code']})")

st.subheader("Next 24 hours (table)")
st.table(hourly[:24])

st.subheader("7-day Forecast")
st.table(daily)
