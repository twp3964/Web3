import json
import pandas as pd
import numpy as np
import requests

# Load Excel file without automatic headers
excel_filename = "merged_data.xlsx"
df = pd.read_excel(excel_filename, header=None)  # Read without headers

# Set the first row as column headers and reset the DataFrame
df.columns = df.iloc[0]  # Assign first row as headers
df = df[1:].reset_index(drop=True)  # Remove first row from data

# Drop the first column (if it's Timestamp)
df = df.drop(columns=["Timestamp"], errors="ignore")
# Drop the first column (if it's Timestamp)
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

# Select first two data rows (excluding column names)
df = df.iloc[:2]

# Convert all datetime columns to string (ISO 8601 format)
for col in df.select_dtypes(include=["datetime64", "object"]).columns:
    df[col] = df[col].astype(str)

# Replace NaN and infinite values with None
df = df.replace([np.nan, np.inf, -np.inf], None)


# Convert DataFrame to JSON (list of lists format)
data_to_push = {"values": [df.columns.tolist()] + df.values.tolist()}  # Include headers

# Print for debugging
print(json.dumps(data_to_push, indent=2))


# API details
SPREADSHEET_ID = "4gLJ1FDpsOkZhNWBETlIrv"  # Replace with your actual spreadsheet ID
TABLE_ID = "46e19e71-799d-4a03-a91a-470c0abba8f4"  # Replace with your actual table ID
RANGE = "A1:G3"
API_URL = f"https://api.rows.com/v1/spreadsheets/{SPREADSHEET_ID}/tables/{TABLE_ID}/values/{RANGE}:append"

# API Headers
HEADERS = {
    "Authorization": "Bearer rows-1esfw14lTgg20nbKC0hLsdShm9mRljSWR4Ut0YHsAjTB",  # Replace with your actual API token
    "Content-Type": "application/json",
}

# Upload data
try:
    response = requests.post(API_URL, json=data_to_push, headers=HEADERS)

    if response.status_code == 202:
        print("✅ Data successfully appended to Rows Spreadsheet!")
        print(response.json())  # Print API response for debugging
    else:
        print(f"❌ Failed to append data. Status Code: {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
