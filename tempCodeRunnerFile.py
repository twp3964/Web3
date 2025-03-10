# API details
# SPREADSHEET_ID = "4gLJ1FDpsOkZhNWBETlIrv"  # Replace with your actual spreadsheet ID
# TABLE_ID = "46e19e71-799d-4a03-a91a-470c0abba8f4"  # Replace with your actual table ID
# RANGE = "A1:H3"
# API_URL = f"https://api.rows.com/v1/spreadsheets/{SPREADSHEET_ID}/tables/{TABLE_ID}/values/{RANGE}:append"

# # API Headers
# HEADERS = {
#     "Authorization": "Bearer rows-1esfw14lTgg20nbKC0hLsdShm9mRljSWR4Ut0YHsAjTB",  # Replace with your actual API token
#     "Content-Type": "application/json",
# }

# # Upload data
# try:
#     response = requests.post(API_URL, json=data_to_push, headers=HEADERS)

#     if response.status_code == 200:
#         print("✅ Data successfully appended to Rows Spreadsheet!")
#         print(response.json())  # Print API response for debugging
#     else:
#         print(f"❌ Failed to append data. Status Code: {response.status_code}")
#         print(f"Response: {response.text}")

# except requests.exceptions.RequestException as e:
#     print(f"❌ Request failed: {e}")
