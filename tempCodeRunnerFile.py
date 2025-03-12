import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

import config  # Ensure this file contains GSHEET_ID

SHEET_ID = config.GSHEET_ID  # Your Google Sheet ID

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
existing_data = get_as_dataframe(sheet, evaluate_formulas=True).dropna(how="all")

# Ensure first row is treated as column names
if not existing_data.empty:
    existing_data.columns = existing_data.iloc[0]  # Set first row as headers
    existing_data = existing_data[1:].reset_index(
        drop=True
    )  # Remove the old header row

# Strip column names of spaces
existing_data.columns = existing_data.columns.str.strip()

# Ensure "Date" column exists
if "Date" not in existing_data.columns:
    print("Error: 'Date' column not found in Google Sheet!")
    print(existing_data.head())  # Debugging output
    exit()

# Convert Date column to datetime format
existing_data["Date"] = pd.to_datetime(existing_data["Date"], errors="coerce")

# Load new Excel data
new_data = pd.read_excel("merged_data.xlsx")  # Ensure this matches your file path

# Strip column names of spaces
new_data.columns = new_data.columns.str.strip()

# Ensure "Date" exists in new data
if "Date" not in new_data.columns:
    print("Error: 'Date' column not found in Excel file!")
    print(new_data.head())  # Debugging output
    exit()

# Convert Date column to datetime
new_data["Date"] = pd.to_datetime(new_data["Date"], errors="coerce")

# Combine old and new data, remove duplicates for the same Date
updated_data = pd.concat([existing_data, new_data]).drop_duplicates(
    subset=["Date"], keep="last"
)

# Keep only the last 10 unique days
updated_data = updated_data.sort_values("Date").tail(10)

# Upload back to Google Sheet
sheet.clear()  # Clear existing data
set_with_dataframe(sheet, updated_data)  # Write updated data back

print("✅ Google Sheet updated successfully with the last 10 days of data.")
