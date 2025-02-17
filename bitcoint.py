import requests

API_KEY = "5df4d80f-4dc2-4103-b3c7-76ceea28b8dc"
url = f"https://api.coinalyze.net/v1/future-markets?api_key={API_KEY}"

response = requests.get(url)
if response.status_code == 200:
    markets = response.json()
    for market in markets:
        if "BTC" in market["symbol"]:  # Adjust if needed
            print(market)
else:
    print(f"Error {response.status_code}: {response.text}")
