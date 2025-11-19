from src.rules import evaluate

def test_rain_rule():
    hourly = [{"precip_prob": 70}] + [{"precip_prob":0}] * 23
    daily = [{"uv_max": 2, "tmax_c": 30}, {"uv_max": 2, "tmax_c": 31}]
    alerts = evaluate(hourly, daily)
    assert any(a["code"]=="RAIN_SOON" for a in alerts)
