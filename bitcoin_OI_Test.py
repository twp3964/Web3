import requests
import json
import time
import config


# API Key
API_KEY = "dc429e6f-b506-49a3-b2b3-15e55291b5b4"

# API Endpoint
BASE_URL = "https://api.coinalyze.net/v1/open-interest"

# List of symbols (split into batches due to API limits)
symbols_list = [
    [
        "BTC-25APR25.2",
        "fi_xbtusd_250926.K",
        "BTC-7MAR25.2",
        "ff_xbtusd_250328.K",
        "BTC-28MAR25.2",
        "fi_xbtusd_250328.K",
        "fi_xbtusd_250627.K",
        "BTC-26DEC25.2",
        "ff_xbtusd_250926.K",
        "BTC-14MAR25.2",
        "BTC-26SEP25.2",
        "ff_xbtusd_250307.K",
        "BTC-27JUN25.2",
        "ff_xbtusd_250627.K",
        "BTC-25APR25.2",
    ],
    [
        "BTCUSD_PERP.A",
        "BTCUSDT.6",
        "BTCUSD.6",
        "BTCUSDC_PERP.A",
        "BTCUSDT_PERP.A",
        "PERP_BTC_USDT.W",
        "BTCUSD_PERP.4",
        "pf_xbtusd.K",
        "BTC_USDT.Y",
        "BTCUSDC_PERP.3",
        "XBTU25.0",
        "BTCUSD_PERP.3",
        "BTCUSDT_PERP.4",
        "BTCUSDT_PERP.F",
        "XBTUSDTH25.0",
        "BTCUSDT_PERP.0",
        "BTC_USDC-PERPETUAL.2",
        "BTCUSD_PERP.K",
        "BTCUSDT_PERP.3",
        "BTCETH_PERP.0",
        "BTC.H",
        "BTC-USD.8",
        "BTCUSDH25.6",
        "BTCEUR_PERP.0",
    ],
    [
        "XBTM25.0",
        "XBTJ25.0",
        "BTCUSD.7",
        "BTCUSDM25.6",
        "BTCPERP.6",
        "BTC-PERPETUAL.2",
        "BTC_USD.Y",
        "BTC-PERP.V",
        "BTCUSD_PERP.0",
        "XBTH25.0",
    ],
]

# Store responses & missing symbols
full_response_data = []
missing_symbols = []


# Function to fetch OI data
def fetch_open_interest(symbols):
    params = {
        "symbols": ",".join(symbols),
        "convert_to_usd": "true",
        "api_key": API_KEY,  # Include API Key in query params
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


# Get total OI in USD with rate limiting
total_oi = 0
for i, batch in enumerate(symbols_list):
    print(f"Processing batch {i + 1} of {len(symbols_list)}...")
    total_oi += fetch_open_interest(batch)

    # Add a delay to comply with 40 requests per minute
    if (i + 1) % 2 == 0:  # Adjust based on your batch size and rate limit
        print("Waiting for 60 seconds to comply with rate limit...")
        time.sleep(60)  # Wait for 60 seconds after every 2 batches (40 symbols)

# Save full response to a JSON file
with open("open_interest_data.json", "w") as file:
    json.dump(full_response_data, file, indent=4)

# Save missing symbols to a log file
if missing_symbols:
    with open("missing_symbols.log", "w") as file:
        file.write("\n".join(missing_symbols))
    print(
        f"\n⚠️ Missing Symbols Logged: {len(missing_symbols)} symbols saved in missing_symbols.log"
    )
    print("Missing Symbols:", missing_symbols)

print(f"\n✅ Total Open Interest: {total_oi:,.2f} USD")
print("📂 Full response saved in open_interest_data.json")
