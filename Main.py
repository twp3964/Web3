import requests
import pandas as pd

if __name__ == '__main__':
    # Alpha Vantage API details
    API_KEY = " VEV44TIRFGC4AVR7"
    SYMBOL = "BTC"  # Replace with your stock symbol
    ALPHA_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}&outputsize=compact"

    # Fetch stock data
    response = requests.get(ALPHA_URL)
    data = response.json()

    # Extract last 10 days of closing prices
    time_series = data.get("Time Series (Daily)", {})
    df = pd.DataFrame.from_dict(time_series, orient="index")
    df = df.rename(columns={"4. close": "Close Price"})[["Close Price"]]
    df.index = pd.to_datetime(df.index)
    df = df.sort_index().tail(10)  # Get the last 10 days

    # Save to Excel
    excel_filename = "stock_prices.xlsx"
    df.to_excel(excel_filename, sheet_name="Stock Data")

    print(f"Stock data saved to {excel_filename}. You can upload this file to Google Sheets.")

