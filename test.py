# import requests
# from datetime import datetime, timedelta, UTC


# def get_coinalyze_data(endpoint, symbols, api_key, interval="daily"):
#     """Fetches data from Coinalyze API for the given endpoint and symbol."""
#     base_url = "https://api.coinalyze.net/v1/"

#     # Define the time range (last 24 hours)
#     today = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
#     yesterday = today - timedelta(days=1)

#     from_timestamp = int(yesterday.timestamp())
#     to_timestamp = int(today.timestamp())

#     # Construct URL with query parameters
#     url = (
#         f"{base_url}{endpoint}?api_key={api_key}"
#         f"&symbols={symbols}&interval={interval}&from={from_timestamp}&to={to_timestamp}"
#     )

#     response = requests.get(url)
#     return response.json()


# API_KEY = "742b4f4f-eaad-481b-a8f3-299a23d403ca"

# # 1) Normal Futures OI
# oi_normal_data = get_coinalyze_data("open-interest-history", "BTCUSD_PERP.0", API_KEY)

# # 2) PERP OI
# oi_perp_data = get_coinalyze_data("open-interest-history", "BTCUSDT_PERP.A", API_KEY)

# # 3) Normal Futures Close Price
# close_normal_data = get_coinalyze_data("ohlcv-history", "BTCUSD_PERP.0", API_KEY)

# # 4) PERP Close Price
# close_perp_data = get_coinalyze_data("ohlcv-history", "BTCUSDT_PERP.A", API_KEY)

# print("\n Normal Futures OI:", oi_normal_data)
# print("\n PERP OI:", oi_perp_data)
# print("\n Normal Futures Close Price:", close_normal_data)
# print("\n PERP Close Price:", close_perp_data)


