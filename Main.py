import requests
import pandas as pd

if __name__ == '__main__':
    # Alpha Vantage API details
    API_KEY = "VEV44TIRFGC4AVR7"
    SYMBOL = "BTC"  # Replace with your stock symbol
    ALPHA_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}&outputsize=compact"

    # Fetch stock data
    response = requests.get(ALPHA_URL)
    data = response.json()

    # Extract last 10 days of closing prices
    time_series = data.get("Time Series (Daily)", {})

    if not time_series:
        print("❌ No data received from Alpha Vantage. Check API key or symbol.")
        exit()

    df = pd.DataFrame.from_dict(time_series, orient="index")
    df = df.rename(columns={"4. close": "Close Price"})[["Close Price"]]
    df.index = pd.to_datetime(df.index)
    df = df.sort_index().tail(10)  # Get the last 10 days

    # Save to Excel
    excel_filename = "stock_prices.xlsx"
    df.to_excel(excel_filename, sheet_name="Stock Data")

    print(f"✅ Stock data saved to {excel_filename}. Now uploading to API Rows...")

    # API Rows (Replace with your API Rows table URL)
    API_ROWS_URL = "https://api.apirows.com/v1/sheets/YOUR_SHEET_ID/rows"  # ✅ Fixed URL
    API_ROWS_HEADERS = {
        "Authorization": "Bearer YOUR_ROWS_API_KEY_HERE",
        "Content-Type": "application/json"
    }

    # ---------------- PUSH DATA TO API ROWS ----------------
    df_combined = df.reset_index()
    df_combined.columns = ["Date", "Close Price"]  # Rename index column
    df_combined["Date"] = df_combined["Date"].astype(str)  # Convert dates to string
    data_to_push = df_combined.to_dict(orient="records")  # Convert DataFrame to JSON

    try:
        response = requests.post(API_ROWS_URL, json=data_to_push, headers=API_ROWS_HEADERS)

        if response.status_code == 200:
            print("✅ Data successfully uploaded to API Rows!")
        else:
            print(f"❌ Failed to upload data. Status Code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
