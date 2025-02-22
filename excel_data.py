import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import config


def get_coinalyze_data(endpoint, symbols, api_key, interval="daily"):
    base_url = "https://api.coinalyze.net/v1/"
    today = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    yesterday = today - timedelta(days=1)
    from_timestamp = int(yesterday.timestamp())
    to_timestamp = int(today.timestamp())
    url = (
        f"{base_url}{endpoint}?api_key={api_key}"
        f"&symbols={symbols}&interval={interval}&from={from_timestamp}&to={to_timestamp}"
    )
    if endpoint == "open-interest-history":
        url += "&convert_to_usd=true"
    response = requests.get(url)
    return response.json()


COINALYZE_API_KEY = config.COINALYZE_API_KEY

data = {
    "Date": [],
    "Normal Futures CP ($)": [],
    "Normal Futures OI ($)": [],
    "Normal Futures OI (B)": [],
    "PERP CP ($)": [],
    "PERP OI ($)": [],
    "PERP OI (B)": [],
    "Total OI ($)": [],
    "Total OI (B)": [],
}


def extract_values(data_list):
    if data_list and "history" in data_list[0]:
        latest_entry = data_list[0]["history"][-1]
        return latest_entry["c"]
    return None


def format_value(value):
    if value and value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B", value
    return f"{value:.2f}", value


daily_CP_TF = get_coinalyze_data("ohlcv-history", "BTCUSD.A", COINALYZE_API_KEY)
daily_OI_TF = get_coinalyze_data(
    "open-interest-history", "BTCUSDH25.6", COINALYZE_API_KEY
)
daily_CP_PERP = get_coinalyze_data("ohlcv-history", "BTCUSD_PERP.A", COINALYZE_API_KEY)
daily_OI_PERP = get_coinalyze_data(
    "open-interest-history", "BTCUSD_PERP.A", COINALYZE_API_KEY
)

data["Date"].append(datetime.now().strftime("%Y-%m-%d"))

cp_tf = extract_values(daily_CP_TF)
oi_tf = extract_values(daily_OI_TF)
cp_perp = extract_values(daily_CP_PERP)
oi_perp = extract_values(daily_OI_PERP)

total_oi = (oi_tf or 0) + (oi_perp or 0)

formatted_oi_tf, actual_oi_tf = format_value(oi_tf)
formatted_oi_perp, actual_oi_perp = format_value(oi_perp)
formatted_total_oi, actual_total_oi = format_value(total_oi)

data["Normal Futures CP ($)"].append(cp_tf)
data["Normal Futures OI ($)"].append(actual_oi_tf)
data["Normal Futures OI (B)"].append(formatted_oi_tf)
data["PERP CP ($)"].append(cp_perp)
data["PERP OI ($)"].append(actual_oi_perp)
data["PERP OI (B)"].append(formatted_oi_perp)
data["Total OI ($)"].append(actual_total_oi)
data["Total OI (B)"].append(formatted_total_oi)

df = pd.DataFrame(data)
df.to_excel("coinalyze_data.xlsx", index=False)

print("Data saved to coinalyze_data.xlsx")
