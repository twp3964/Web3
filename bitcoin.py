import requests
import json

import config

# API Key (replace with your actual key)
API_KEY = config.COINALYZE_API_KEY

# API Endpoint
BASE_URL = "https://api.coinalyze.net/v1/open-interest"

# List of symbols (split into batches of 20 due to API limits)
symbols_list = [
    [
        "BTCUSD_PERP.A",
        "BTCUSDT.6",
        "BTCUSD.6",
        "BTCUSDC_PERP.A",
        "BTCUSDT_PERP.A",
        "PERP_BTC_USDT.W",
        "BTCUSD_PERP.4",
        "BTC-7MAR25.2",
        "pf_xbtusd.K",
        "BTC-28FEB25.2",
        "BTC_USDT.Y",
        "BTCUSDC_PERP.3",
        "ff_xbtusd_250328.K",
        "XBTU25.0",
        "BTC-28MAR25.2",
        "BTCUSD_PERP.3",
        "BTCUSDT_PERP.4",
        "BTCUSDT_PERP.F",
        "XBTG25.0",
        "XBTUSDTH25.0",
    ],
    [
        "fi_xbtusd_250328.K",
        "BTCUSDT_PERP.0",
        "BTC_USDC-PERPETUAL.2",
        "BTCUSD_PERP.K",
        "fi_xbtusd_250627.K",
        "BTC-26DEC25.2",
        "BTCUSDT_PERP.3",
        "BTCETH_PERP.0",
        "ff_xbtusd_250926.K",
        "BTC.H",
        "BTC-USD.8",
        "BTCUSDH25.6",
        "fi_xbtusd_250228.K",
        "BTCEUR_PERP.0",
        "XBTM25.0",
        "BTCUSD.7",
        "BTC-26SEP25.2",
        "BTCUSDM25.6",
        "ff_xbtusd_250228.K",
        "BTCPERP.6",
    ],
    [
        "BTC-27JUN25.2",
        "ff_xbtusd_250627.K",
        "BTC-PERPETUAL.2",
        "BTC_USD.Y",
        "BTC-PERP.V",
        "BTCUSD_PERP.0",
        "XBTH25.0",
    ],
]

#Store responses & missing symbols
full_response_data = []
missing_symbols = []

# Function to fetch OI data
def fetch_open_interest(symbols):
    params = {
        "symbols": ",".join(symbols),
        "convert_to_usd": "true",
        "api_key": API_KEY  # Include API Key in query params
    }
    
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        full_response_data.extend(data)  # Store full response

        # Identify missing symbols (not in response)
        received_symbols = {item["symbol"] for item in data}
        for symbol in symbols:
            if symbol not in received_symbols:
                missing_symbols.append(symbol)

        return sum(item["value"] for item in data)  # Summing OI values
    else:
        print(f"Error fetching data: {response.status_code}, Response: {response.text}")
        return 0

# Get total OI in USD
total_oi = sum(fetch_open_interest(batch) for batch in symbols_list)

# Save full response to a JSON file
with open("open_interest_data.json", "w") as file:
    json.dump(full_response_data, file, indent=4)

# Save missing symbols to a log file
if missing_symbols:
    with open("missing_symbols.log", "w") as file:
        file.write("\n".join(missing_symbols))
    print(f"\n⚠️ Missing Symbols Logged: {len(missing_symbols)} symbols saved in missing_symbols.log")
    print("Missing Symbols:", missing_symbols)

print(f"\n✅ Total Open Interest: {total_oi:,.2f} USD")
print("📂 Full response saved in open_interest_data.json")
