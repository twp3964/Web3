import requests
from datetime import datetime, timedelta, timezone
import config


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
    if endpoint == "open-interest-history":
        url += "&convert_to_usd=true"

    response = requests.get(url)
    return response.json()


API_KEY = config.COINALYZE_API_KEY

# 1) Daily Closing Price(CP) for Traditional Futures(TF)
daily_CP_TF = get_coinalyze_data("ohlcv-history", "BTCUSD.A", API_KEY)

# 2) Daily Open Interest (OI) for Traditional Futures
daily_OI_TF = get_coinalyze_data("open-interest-history", "BTCUSD_PERP.A", API_KEY)

# 3) Daily Closing Price(CP) for Perpetual Contracts (PERP):
daily_CP_PERP = get_coinalyze_data("ohlcv-history", "BTCUSD_PERP.A", API_KEY)

# 4) PERP Open Interest (OI)
daily_OI_PERP = get_coinalyze_data("open-interest-history", "BTCUSD_PERP.A", API_KEY)

# Print the results
print("\nNormal Futures Close Price:", daily_CP_TF)
print("\nNormal Futures OI:", daily_OI_TF)
print("\nPERP Close Price:", daily_CP_PERP)
print("\nPERP OI:", daily_OI_PERP)
