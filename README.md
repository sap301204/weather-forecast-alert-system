
# Weather Forecast & Alert Application

A complete end-to-end Weather Intelligence System designed using **Python**, **FastAPI**, **SQLite**, **Streamlit**, and **Docker**, built for real-world industry use cases such as logistics, agriculture, construction, and public safety.

This project fetches live weather forecasts, normalizes time-series data, evaluates risk alerts (Rain, Heat, Wind, UV), exposes APIs, visualizes data, and fires smart notifications.

---

## 🚀 Features

- Real-time weather ingestion (Open-Meteo API)
- Hourly + Daily forecasts (48h/7-day)
- Alert Engine (Rain / Heat / Wind / UV)
- FastAPI backend (locations, forecasts, alerts)
- Streamlit dashboard
- Optional Next.js Frontend
- Notification system (Telegram/SMS)
- Docker + docker-compose support
- SQLite persistent storage
- Fully production-oriented structure

---

## 🧱 Tech Stack

**Backend:** Python, FastAPI, httpx  
**DB:** SQLite  
**Frontend:** Streamlit / Next.js  
**Notifications:** Telegram API  
**Containerization:** Docker  
**Scheduler:** Cron / APScheduler  

---

## 📁 Folder Structure



weather-alert-app/
├─ api/ # FastAPI backend
├─ src/ # Ingestion, rules, notify, db utils
├─ jobs/ # Scheduler jobs
├─ web/ # Streamlit dashboard
├─ frontend/ # Optional Next.js app
├─ docker/ # Docker files
├─ db/ # Schema + seed
├─ tests/ # Unit tests
├─ .github/workflows/ # CI pipeline
└─ docker-compose.yml


---

## ⚙️ Setup Instructions

### 1️⃣ Create environment


python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


### 2️⃣ Initialize DB


python -c "from src.db_utils import init_db; init_db()"
sqlite3 db/weather.db < db/seed.sql


### 3️⃣ Fetch weather data


python jobs/refresh.py


### 4️⃣ Start backend


uvicorn api.app:app --reload


### 5️⃣ Start dashboard


streamlit run web/streamlit_app.py


---

## 🐳 Docker (Production)



docker-compose up --build


---

## 🧪 Tests


pytest -q


---

## 📄 License
MIT License — free to use, modify, distribute.

---

## ✨ Author
Developed by Sayli — Electrical Engineering | Python Developer | Industry Projects
