import json
import pandas as pd
import numpy as np
import requests
import config  # Import the config file

# Load Excel file without automatic headers
excel_filename = "merged_data.xlsx"
df = pd.read_excel(excel_filename, header=None)  # Read without headers

# Set the first row as column headers and reset the DataFrame
df.columns = df.iloc[0]  # Assign first row as headers
df = df[1:].reset_index(drop=True)  # Remove first row from data

# Drop unnecessary columns
df = df.drop(columns=["Timestamp", "Unnamed: 0"], errors="ignore")

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
API_URL = f"https://api.rows.com/v1/spreadsheets/{config.SPREADSHEET_ID}/tables/{config.TABLE_ID}/values/{config.RANGE}:append"

# API Headers
HEADERS = {
    "Authorization": f"Bearer {config.API_TOKEN}",
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
