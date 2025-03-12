import requests
from tqdm import tqdm
import config
import time
import pandas as pd
from datetime import datetime, timedelta, timezone


COINALYZE_API_KEY = config.COINALYZE_API_KEY


def get_coinalyze_data(
    endpoint,
    symbols,
    api_key,
    interval="daily",
):
    """Fetches data from Coinalyze API for the given endpoint and symbol."""
    base_url = "https://api.coinalyze.net/v1/"

    # Define the time range (last 24 hours)
    today = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    yesterday = today - timedelta(days=1)

    from_timestamp = int(yesterday.timestamp())
    to_timestamp = int(today.timestamp())

    # Construct URL with query parameters
    url = (
        f"{base_url}{endpoint}?api_key={api_key}"
        f"&symbols={symbols} "
        f"&interval={interval}"
        f"&from={from_timestamp}"
        f"&to={to_timestamp}"
    )

    # Include convert_to_usd if true
    if endpoint == "open-interest-history":
        url += "&convert_to_usd=true"

    response = requests.get(url)
    return response.json()


# 1) Normal[PERP + Future] Daily Closing Price(CP):
CP_NORMAL_daily = get_coinalyze_data(
    "ohlcv-history", "SPOT_BTC_USDT.W", COINALYZE_API_KEY
)

# 2) PERP Daily Closing Price(CP):
CP_PERP_Daily = get_coinalyze_data("ohlcv-history", "BTCUSD_PERP.A", COINALYZE_API_KEY)


# 3) PERP Open Interest (OI)
perp_symbols = "BTCUSD_PERP.A, BTCUSDT.6, BTCUSD.6, BTCUSDC_PERP.A, BTCUSDT_PERP.A, PERP_BTC_USDT.W, BTCUSD_PERP.4, pf_xbtusd.K, BTC_USDT.Y, BTCUSDC_PERP.3, XBTU25.0, BTCUSD_PERP.3, BTCUSDT_PERP.4, BTCUSDT_PERP.F, XBTUSDTH25.0, BTCUSDT_PERP.0, BTC_USDC-PERPETUAL.2, BTCUSD_PERP.K, BTCUSDT_PERP.3, BTCETH_PERP.0, BTC.H, BTC-USD.8, BTCUSDH25.6, BTCEUR_PERP.0, XBTM25.0, XBTJ25.0, BTCUSD.7, BTCUSDM25.6, BTCPERP.6, BTC-PERPETUAL.2, BTC_USD.Y, BTC-PERP.V, BTCUSD_PERP.0, XBTH25.0"

OI_PERP_Daily = get_coinalyze_data(
    "open-interest-history", perp_symbols, COINALYZE_API_KEY
)

# Introduce a 70 sec delay for 40 requests per minute limit
print("Waiting for 70 seconds to comply with API rate limits...")
for _ in tqdm(range(70), desc="Sleeping", unit="sec"):
    time.sleep(1)

print("Resuming data fetch after delay.")


# 4) Futures Daily Open Interest (OI)
futures_symbols = "BTC-7MAR25.2, ff_xbtusd_250328.K, XBTU25.0, BTC-28MAR25.2, XBTUSDTH25.0, fi_xbtusd_250328.K, fi_xbtusd_250627.K, BTC-26DEC25.2, ff_xbtusd_250926.K, BTC-14MAR25.2, BTCUSDH25.6, XBTM25.0, XBTJ25.0, BTC-26SEP25.2, ff_xbtusd_250307.K, BTCUSDM25.6, BTC-27JUN25.2, ff_xbtusd_250627.K, fi_xbtusd_250926.K, BTC-25APR25.2, XBTH25.0"
daily_OI_Futures = get_coinalyze_data(
    "open-interest-history", futures_symbols, COINALYZE_API_KEY
)


# Function to sum up Open Interest (OI) for a given dataset
def calculate_total_OI(oi_data):
    total_OI = {}

    for entry in oi_data:
        for record in entry["history"]:
            timestamp = record["t"]
            if timestamp not in total_OI:
                total_OI[timestamp] = 0
            total_OI[timestamp] += record["c"]  # Using closing OI

    return [{"t": t, "OI": oi} for t, oi in total_OI.items()]


# Calculate total PERP OI
total_perp_oi = calculate_total_OI(OI_PERP_Daily)

# Calculate total Futures OI
total_futures_oi = calculate_total_OI(daily_OI_Futures)

# Merge PERP + Futures OI for Normal OI Calculation
normal_oi = {}

for entry in total_perp_oi:
    t = entry["t"]
    normal_oi[t] = entry["OI"]

for entry in total_futures_oi:
    t = entry["t"]
    if t in normal_oi:
        normal_oi[t] += entry["OI"]
    else:
        normal_oi[t] = entry["OI"]

# Convert Normal OI to list format
total_normal_oi = [{"t": t, "OI": oi} for t, oi in normal_oi.items()]


# Print the result
# # Print the results
print("\nPERP OI:", total_perp_oi)
print("\nNORMAL Close Price:", CP_NORMAL_daily)
print("\nPERP Close Price:", CP_PERP_Daily)
print("\nNORMAL OI:", total_normal_oi)


# Extracting Data
perp_oi = total_perp_oi
normal_oi = total_normal_oi
normal_close = CP_NORMAL_daily
perp_close = CP_PERP_Daily


data = []
for i in range(len(perp_oi)):
    timestamp = perp_oi[i]["t"]

    # Convert timestamp to readable date
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")

    # Fetch values
    perp_oi_val = round(perp_oi[i]["OI"], 2)  # Round to 2 decimal places
    normal_oi_val = round(normal_oi[i]["OI"], 2)
    normal_close_price = round(
        normal_close[0]["history"][i]["c"], 0
    )  # Round to nearest integer
    perp_close_price = round(perp_close[0]["history"][i]["c"], 0)

    # Append row data
    data.append(
        {
            # "Timestamp": timestamp,
            "Date": date,
            "PERP OI (USD)": perp_oi_val,
            "NORMAL OI (USD)": normal_oi_val,
            "NORMAL Close Price (USD)": f"{normal_close_price:,}",  # Format with commas
            "PERP Close Price (USD)": f"{perp_close_price:,}",
        }
    )

# Convert data to DataFrame
df = pd.DataFrame(data)

# Save as Excel
df.to_excel("coinalyze_data.xlsx", index=False)
print("✅ Coinalyze data saved!")

# Load both Excel files
coinalyze_df = pd.read_excel("coinalyze_data.xlsx")
stock_df = pd.read_excel("stock_prices.xlsx")

# Trim stock_df to match coinalyze_df row count (only keep first two rows)
stock_df = stock_df.iloc[: len(coinalyze_df)]

# Merge DataFrames (side by side)
merged_df = pd.concat([coinalyze_df, stock_df], axis=1)

# Save merged data
merged_excel_filename = "merged_data.xlsx"
merged_df.to_excel(merged_excel_filename, index=False)

print(f"✅ Merged data saved as '{merged_excel_filename}'!")
