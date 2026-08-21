import os
import pandas as pd
import numpy as np

def clean_sales_data():
    raw_path = os.path.join("data", "raw_sales_data.xlsx")
    cleaned_path = os.path.join("data", "cleaned_sales_data.xlsx")
    
    if not os.path.exists(raw_path):
        print(f"Error: Raw data file {raw_path} not found. Please run the generator first.")
        return
        
    print(f"Loading raw sales data from: {raw_path}")
    df = pd.read_excel(raw_path)
    initial_rows = len(df)
    
    # 1. Remove exact duplicates
    df = df.drop_duplicates()
    dups_removed = initial_rows - len(df)
    print(f"Removed {dups_removed} duplicate records.")
    
    # 2. Text Cleaning & Standardization
    # Trim leading/trailing spaces
    text_cols = ["Order ID", "Customer ID", "Customer Name", "Region", "State", "City", 
                 "Category", "Sub-Category", "Product ID", "Product Name", "Salesperson", "Payment Method"]
    
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    # Standardize casing
    df["Region"] = df["Region"].str.capitalize()  # "west" -> "West", "WEST" -> "West"
    df["Category"] = df["Category"].str.title()  # "technology" -> "Technology"
    df["Sub-Category"] = df["Sub-Category"].str.title()
    df["State"] = df["State"].str.title()
    df["City"] = df["City"].str.title()
    
    # Replace any standard casing abnormalities in Region/Category
    region_mapping = {"East": "East", "West": "West", "Central": "Central", "South": "South"}
    df["Region"] = df["Region"].map(lambda x: region_mapping.get(x, x))
    
    # 3. Handle Missing Values
    # Impute missing Customer Name using Customer ID
    cust_id_map = df[df["Customer Name"].notna() & (df["Customer Name"] != "None") & (df["Customer Name"] != "")].set_index("Customer ID")["Customer Name"].to_dict()
    
    def fill_customer_name(row):
        name = row["Customer Name"]
        c_id = row["Customer ID"]
        if pd.isna(name) or name == "None" or name == "":
            return cust_id_map.get(c_id, "Unknown Customer")
        return name
        
    df["Customer Name"] = df.apply(fill_customer_name, axis=1)
    
    # Handle missing Payment Method
    df["Payment Method"] = df["Payment Method"].fillna("Credit Card")
    df.loc[df["Payment Method"] == "None", "Payment Method"] = "Credit Card"
    
    # 4. Correct Data Types & Formats
    # Clean and parse Dates
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    
    # Handle missing Ship Date: Impute as Order Date + 4 days
    def fill_ship_date(row):
        order_d = row["Order Date"]
        ship_d = row["Ship Date"]
        if pd.isna(ship_d) or ship_d == "None" or ship_d == "":
            if not pd.isna(order_d):
                return order_d + pd.Timedelta(days=4)
            return pd.NaT
        return pd.to_datetime(ship_d, errors="coerce")
        
    df["Ship Date"] = df.apply(fill_ship_date, axis=1)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    
    # Drop rows with invalid Order Dates (if any)
    df = df.dropna(subset=["Order Date"])
    
    # 5. Numerical Validations & Filtering
    # Quantity must be positive - take absolute value to correct typos
    df["Quantity"] = df["Quantity"].astype(float).abs().astype(int)
    
    # Filter out rows with zero or negative Sales (invalid entries)
    df = df[df["Sales"] > 0]
    
    # Ensure Discount is a float
    df["Discount"] = df["Discount"].astype(float)
    
    # Ensure Sales, Profit are rounded floats
    df["Sales"] = df["Sales"].astype(float).round(2)
    df["Profit"] = df["Profit"].astype(float).round(2)
    
    # 6. Calculated Columns
    # Lead Time (Days)
    df["Lead Time (Days)"] = (df["Ship Date"] - df["Order Date"]).dt.days
    # If lead time is negative due to date issues, set to 0 or absolute
    df["Lead Time (Days)"] = df["Lead Time (Days)"].abs()
    
    # Profit Margin %
    df["Profit Margin %"] = (df["Profit"] / df["Sales"]).round(4)
    
    # Date helper columns for Excel and Power BI modeling
    df["Order Year"] = df["Order Date"].dt.year
    df["Order Month Number"] = df["Order Date"].dt.month
    df["Order Month"] = df["Order Date"].dt.strftime("%b") # Jan, Feb, etc.
    
    # Save cleaned data to Excel
    df.to_excel(cleaned_path, index=False, sheet_name="Cleaned Sales Data")
    
    # Save cleaned data to JSON for React app consumption
    json_dir = os.path.join("src", "data")
    os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, "cleaned_sales_data.json")
    
    df_json = df.copy()
    df_json["Order Date"] = df_json["Order Date"].dt.strftime("%Y-%m-%d")
    df_json["Ship Date"] = df_json["Ship Date"].dt.strftime("%Y-%m-%d")
    
    df_json.to_json(json_path, orient="records", date_format="iso")
    
    print(f"Data cleaning complete. Cleaned data saved to: {cleaned_path} and {json_path}")
    print(f"Final records in cleaned dataset: {len(df)}")
    
if __name__ == "__main__":
    clean_sales_data()
