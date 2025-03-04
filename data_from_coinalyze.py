import requests
from datetime import datetime, timedelta, timezone
import config

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
        f"&symbols={symbols}&interval={interval}&from={from_timestamp}&to={to_timestamp}"
    )

    # Include convert_to_usd if true
    # if endpoint == "open-interest-history":
    #     url += "&convert_to_usd=true"

    response = requests.get(url)
    return response.json()


# Sum up the Open Interest (OI) for all PERP symbols
def calculate_total_perp_oi(perp_data):
    total_perp_oi = {}

    for entry in perp_data:
        for record in entry["history"]:
            timestamp = record["t"]
            if timestamp not in total_perp_oi:
                total_perp_oi[timestamp] = 0

            total_perp_oi[timestamp] += record["o"]  # Only summing 'o'

    return [{"t": t, "total_OI": oi} for t, oi in total_perp_oi.items()]


# 1) Daily Closing Price(CP) for Traditional Futures(TF)
daily_CP_TF = get_coinalyze_data("ohlcv-history", "BTCUSD.A", COINALYZE_API_KEY)

# 2) Daily Open Interest (OI) for Traditional Futures
futures_symbols = "BTCUSD.A, BTCUSDT.A, BTCUSDC.A, BTCUSD_PERP.A, BTCUSDT_PERP.A, BTCUSDC_PERP.A, BTCUSDT.B, BTCUSDC.B, BTCUSD_PERP.B, BTCUSDT_PERP.B, BTCUSDC_PERP.B, BTCUSDT.C, BTCUSD_PERP.C, BTCUSDT_PERP.C, BTCDOMUSDT_PERP.A"
daily_OI_Futures = get_coinalyze_data(
    "open-interest-history", futures_symbols, COINALYZE_API_KEY
)


# 3) Daily Closing Price(CP) for Perpetual Contracts (PERP):
daily_CP_PERP = get_coinalyze_data("ohlcv-history", "BTCUSD_PERP.A", COINALYZE_API_KEY)

# 4) PERP Open Interest (OI)
perp_symbols = "BTCUSD_PERP.A,BTCUSDC_PERP.A"
daily_OI_PERP = get_coinalyze_data(
    "open-interest-history", perp_symbols, COINALYZE_API_KEY
)

# Print the results
print("\nNormal Futures Close Price:", daily_CP_TF)
print("\nNormal Futures OI:", daily_OI_Futures)
print("\nPERP Close Price:", daily_CP_PERP)
print("\nPERP OI:", daily_OI_PERP)


# Calculate total PERP OI
total_perp_oi = calculate_total_perp_oi(daily_OI_PERP)

# Print the result
print("\nTotal PERP OI:", total_perp_oi)
