import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import config

SHEET_ID = config.GSHEET_ID

# Authenticate using JSON key
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_file("gsheet_key.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open Google Sheet
sheet = client.open_by_key(SHEET_ID).worksheet("Sheet1")

# Read existing data
existing_data = get_as_dataframe(sheet).dropna(how="all")

# Load new Excel data (excluding the first column)
try:
    new_data = pd.read_excel(
        "merged_data.xlsx", usecols=lambda x: x not in [0]
    )  # Skip first column by index
except FileNotFoundError:
    print("Error: merged_data.xlsx not found.")
    exit()

# Ensure 'Date' column exists
if "Date" not in existing_data.columns or "Date" not in new_data.columns:
    print("Error: 'Date' column is missing in the dataset.")
    exit()

# Convert "Date" column to datetime for proper sorting
existing_data["Date"] = pd.to_datetime(existing_data["Date"], errors="coerce")
new_data["Date"] = pd.to_datetime(new_data["Date"], errors="coerce")

# Remove existing rows with the same date
existing_data = existing_data[~existing_data["Date"].isin(new_data["Date"])]

# Append new data
updated_data = pd.concat([existing_data, new_data])

# Drop duplicate dates while keeping the latest data
updated_data = updated_data.sort_values("Date", ascending=False).drop_duplicates(
    subset=["Date"], keep="last"
)

# Keep only the last 10 days
updated_data = updated_data.head(10)

# Convert Date column to string format (YYYY-MM-DD)
updated_data["Date"] = updated_data["Date"].dt.strftime("%Y-%m-%d")

# Ensure all columns are strings before uploading
updated_data = updated_data.astype(str)

# Upload to Google Sheets
sheet.update([updated_data.columns.values.tolist()] + updated_data.values.tolist())

print("Data uploaded successfully.")
