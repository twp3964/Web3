

# Convert to DataFrame
df = pd.DataFrame(data)

# Keep only the first two rows
df = df.iloc[:2]

# Save as Excel
df.to_excel("coinalyze_data.xlsx", index=False)

print("✅ Data successfully converted and saved!")

# Load both Excel files
coinalyze_df = pd.read_excel("coinalyze_data.xlsx")
stock_df = pd.read_excel("stock_prices.xlsx")

# Merge both DataFrames (side by side)
merged_df = pd.concat([coinalyze_df, stock_df], axis=1)

# Save the merged data to a new Excel file
merged_excel_filename = "merged_data.xlsx"
merged_df.to_excel(merged_excel_filename, index=False)

print(f"✅ Merged data saved to {merged_excel_filename}")