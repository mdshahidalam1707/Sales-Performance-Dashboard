import os
import random
import datetime
import pandas as pd
import numpy as np

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Define geographical hierarchy
geo_data = {
    "West": {
        "California": ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose"],
        "Washington": ["Seattle", "Spokane", "Tacoma"],
        "Oregon": ["Portland", "Eugene", "Salem"],
        "Arizona": ["Phoenix", "Tucson", "Mesa"]
    },
    "East": {
        "New York": ["New York City", "Buffalo", "Rochester", "Syracuse"],
        "Pennsylvania": ["Philadelphia", "Pittsburgh", "Allentown"],
        "Massachusetts": ["Boston", "Worcester", "Springfield"],
        "Ohio": ["Columbus", "Cleveland", "Cincinnati"]
    },
    "Central": {
        "Texas": ["Houston", "San Antonio", "Dallas", "Austin", "Fort Worth"],
        "Illinois": ["Chicago", "Aurora", "Rockford"],
        "Michigan": ["Detroit", "Grand Rapids", "Warren"],
        "Minnesota": ["Minneapolis", "St. Paul", "Duluth"]
    },
    "South": {
        "Florida": ["Miami", "Jacksonville", "Tampa", "Orlando"],
        "Georgia": ["Atlanta", "Augusta", "Columbus"],
        "North Carolina": ["Charlotte", "Raleigh", "Greensboro"],
        "Tennessee": ["Nashville", "Memphis", "Knoxville"]
    }
}

# Regional Salespeople mapping
salespeople = {
    "West": ["Michael Chang", "Emily Wong"],
    "East": ["Sarah Connor", "John Davis"],
    "Central": ["David Miller", "Amanda Johnson"],
    "South": ["Robert Jackson", "Maria Rodriguez"]
}

# Product hierarchy and baseline unit prices
product_catalog = {
    "Technology": {
        "Phones": [
            ("TEC-PH-1000001", "Apple iPhone 14 Pro", 999.00),
            ("TEC-PH-1000002", "Samsung Galaxy S23", 799.00),
            ("TEC-PH-1000003", "Google Pixel 7", 599.00),
            ("TEC-PH-1000004", "Motorola Edge", 499.00)
        ],
        "Copiers": [
            ("TEC-CP-1000001", "Canon ImageCLASS Printer", 1499.00),
            ("TEC-CP-1000002", "HP LaserJet Pro Copier", 1899.00),
            ("TEC-CP-1000003", "Brother Monochrome Copier", 1299.00),
            ("TEC-CP-1000004", "Xerox VersaLink Multi", 2499.00)
        ],
        "Accessories": [
            ("TEC-AC-1000001", "Logitech MX Master 3 Mouse", 99.00),
            ("TEC-AC-1000002", "Anker USB-C Hub 8-in-1", 49.00),
            ("TEC-AC-1000003", "SanDisk 128GB Flash Drive", 19.99),
            ("TEC-AC-1000004", "Apple Magic Keyboard", 129.00)
        ],
        "Machines": [
            ("TEC-MA-1000001", "Epson EcoTank Pro Scanner", 799.00),
            ("TEC-MA-1000002", "Zebra Thermal Label Printer", 349.00),
            ("TEC-MA-1000003", "Star Micronics POS Receipt Printer", 289.00),
            ("TEC-MA-1000004", "HP DesignJet Large Plotter", 3999.00)
        ]
    },
    "Furniture": {
        "Chairs": [
            ("FUR-CH-1000001", "Herman Miller Aeron Chair", 1199.00),
            ("FUR-CH-1000002", "Steelcase Gesture Chair", 999.00),
            ("FUR-CH-1000003", "Hon Exposure Mesh Chair", 249.00),
            ("FUR-CH-1000004", "Office Star Ergonomic Chair", 189.00)
        ],
        "Tables": [
            ("FUR-TA-1000001", "Bush Furniture Computer Desk", 349.00),
            ("FUR-TA-1000002", "Coaster Alder Writing Desk", 499.00),
            ("FUR-TA-1000003", "Sauder Edge Water Executive Desk", 699.00),
            ("FUR-TA-1000004", "Z-Line Designs Glass L-Desk", 279.00)
        ],
        "Bookcases": [
            ("FUR-BO-1000001", "IKEA Billy Bookcase 5-Shelf", 89.00),
            ("FUR-BO-1000002", "Sauder 5-Shelf Wood Bookcase", 149.00),
            ("FUR-BO-1000003", "Bush Furniture 3-Shelf Bookcase", 119.00),
            ("FUR-BO-1000004", "Ameriwood Home Glass Bookcase", 229.00)
        ],
        "Furnishings": [
            ("FUR-FU-1000001", "DAX Black Framed Wall Clock", 29.99),
            ("FUR-FU-1000002", "Kenroy Home Rustic Table Lamp", 89.00),
            ("FUR-FU-1000003", "Howard Miller Wall Clock", 149.00),
            ("FUR-FU-1000004", "Tensor Halogen Desk Lamp", 19.99)
        ]
    },
    "Office Supplies": {
        "Paper": [
            ("OFF-PA-1000001", "Hammermill Copy Paper Case", 54.00),
            ("OFF-PA-1000002", "HP Multipurpose Paper Ream", 8.50),
            ("OFF-PA-1000003", "Xerox Business Paper Ream", 7.99),
            ("OFF-PA-1000004", "Mead College Ruled Notebook", 2.49)
        ],
        "Binders": [
            ("OFF-BI-1000001", "Avery Durable 3-Ring Binder 2-inch", 6.99),
            ("OFF-BI-1000002", "Wilson Jones Ring Binder 3-inch", 12.50),
            ("OFF-BI-1000003", "Universal View Binder 1-inch", 3.29),
            ("OFF-BI-1000004", "Samsill Leather Presentation Binder", 24.99)
        ],
        "Storage": [
            ("OFF-ST-1000001", "Bankers Box Storage Boxes 10-Pack", 39.00),
            ("OFF-ST-1000002", "Iris 3-Drawer Plastic Rolling Cart", 45.00),
            ("OFF-ST-1000003", "Sterilite 64-Quart Latch Box", 15.99),
            ("OFF-ST-1000004", "Akro-Mils Small Parts Organizer", 29.99)
        ],
        "Appliances": [
            ("OFF-AP-1000001", "Keurig K-Classic Coffee Maker", 119.00),
            ("OFF-AP-1000002", "Black+Decker Compact Refrigerator", 199.00),
            ("OFF-AP-1000003", "Honeywell Digital Ceramic Heater", 69.00),
            ("OFF-AP-1000004", "Lasko Oscillating Table Fan", 39.00)
        ],
        "Art": [
            ("OFF-AR-1000001", "Prismacolor Colored Pencils 72-Pack", 49.00),
            ("OFF-AR-1000002", "Crayola Washable Markers 24-Pack", 8.99),
            ("OFF-AR-1000003", "Sharpie Permanent Markers 12-Pack", 11.50),
            ("OFF-AR-1000004", "Fiskars Ergonomic Scissors", 9.99)
        ],
        "Fasteners": [
            ("OFF-FA-1000001", "Swingline Desktop Stapler & Staples", 15.99),
            ("OFF-FA-1000002", "ACCO Jumbo Paper Clips 1000-Pack", 7.50),
            ("OFF-FA-1000003", "Gorilla Super Glue 2-Pack", 5.99),
            ("OFF-FA-1000004", "Scotch Heavy Duty Packing Tape", 12.99)
        ],
        "Envelopes": [
            ("OFF-EN-1000001", "Mead Self-Seal Envelopes 100-Pack", 9.99),
            ("OFF-EN-1000002", "Quality Park Catalog Clasp Envelopes", 18.50),
            ("OFF-EN-1000003", "Columbian Double Window Envelopes", 14.29)
        ],
        "Labels": [
            ("OFF-LA-1000001", "Avery Laser Address Labels 3000-Pack", 27.99),
            ("OFF-LA-1000002", "Dymo LetraTag Plastic Label Tape", 6.99),
            ("OFF-LA-1000003", "Brother P-touch Standard Laminated Tape", 14.50)
        ]
    }
}

# Generate Customer Pool
customer_first = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
                  "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
                  "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth",
                  "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob",
                  "Lisa", "Nancy", "Sandra", "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Carol", "Amanda"]
customer_last = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
                 "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White",
                 "Lopez", "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall",
                 "Young", "Allen", "Sanchez", "Wright", "King", "Scott", "Green", "Baker", "Adams", "Nelson",
                 "Hill", "Ramirez", "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Turner", "Torres"]

customer_pool = []
for i in range(1, 601):
    c_id = f"CS-{10000 + i}"
    c_name = f"{random.choice(customer_first)} {random.choice(customer_last)}"
    customer_pool.append((c_id, c_name))

payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Cash"]

def generate_records(num_records=7500):
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    delta_days = (end_date - start_date).days
    
    records = []
    
    for i in range(1, num_records + 1):
        # 1. Order ID (Superstore style, e.g. CA-2023-104921)
        # We will assign the year based on the order date generated below
        # Let's generate order date first, with seasonal probabilities
        while True:
            rand_days = random.randint(0, delta_days)
            ord_date = start_date + datetime.timedelta(days=rand_days)
            month = ord_date.month
            
            # Apply seasonality weights: Q4 (Nov, Dec) high, Q1 (Jan, Feb) low
            weights = {1: 0.6, 2: 0.7, 3: 0.9, 4: 1.0, 5: 1.0, 6: 1.1, 7: 1.0, 8: 1.0, 9: 1.1, 10: 1.2, 11: 1.5, 12: 1.8}
            if random.random() <= (weights[month] / 1.8):
                break
                
        year = ord_date.year
        ord_id = f"CA-{year}-{100000 + i}"
        
        # 2. Shipping Date (Order date + 1 to 7 days)
        ship_days = random.randint(1, 7)
        ship_date = ord_date + datetime.timedelta(days=ship_days)
        
        # 3. Customer Selection
        cust_id, cust_name = random.choice(customer_pool)
        
        # 4. Geography Selection (Strict hierarchy)
        region = random.choice(list(geo_data.keys()))
        state = random.choice(list(geo_data[region].keys()))
        city = random.choice(geo_data[region][state])
        
        # 5. Category/Sub-category/Product selection
        category = random.choice(list(product_catalog.keys()))
        sub_cat = random.choice(list(product_catalog[category].keys()))
        prod = random.choice(product_catalog[category][sub_cat])
        prod_id, prod_name, unit_price = prod
        
        # 6. Salesperson
        salesperson = random.choice(salespeople[region])
        
        # 7. Quantity & Discount
        quantity = random.randint(1, 10)
        
        # Office Supplies typically have small quantities but high volumes
        if category == "Office Supplies":
            quantity = random.randint(1, 15)
        # Technology (e.g. Copiers, Phones) typically have smaller quantities
        elif category == "Technology":
            quantity = random.choices([1, 2, 3, 4, 5], weights=[60, 25, 10, 4, 1])[0]
            
        # Discount logic (discounts of 0%, 10%, 20%, 30%, 50%)
        # Office Supplies and Technology have low discounts on average. Furniture (particularly Tables) has high discounts.
        if sub_cat == "Tables":
            discount = random.choices([0.0, 0.1, 0.2, 0.3, 0.5], weights=[20, 20, 20, 20, 20])[0]
        elif category == "Furniture":
            discount = random.choices([0.0, 0.1, 0.2], weights=[60, 30, 10])[0]
        elif category == "Technology":
            discount = random.choices([0.0, 0.1, 0.15, 0.2], weights=[70, 15, 10, 5])[0]
        else: # Office Supplies
            discount = random.choices([0.0, 0.1, 0.2, 0.5], weights=[80, 10, 8, 2])[0]
            
        # 8. Pricing & Profit calculations
        # Sales = Quantity * Unit Price * (1 - Discount)
        sales = round(quantity * unit_price * (1.0 - discount), 2)
        
        # Define base cost margin (cost as a percentage of price)
        # Tech: 45%-60% cost (high profit margins: 40%-55%)
        # Office Supplies: 50%-70% cost (moderate margins: 30%-50%)
        # Furniture: 75%-95% cost (thin margins: 5%-25%)
        # Tables and Copiers are complex: Copiers are highly profitable, Tables are often loss-makers due to discounts.
        if sub_cat == "Tables":
            cost_pct = random.uniform(0.85, 0.98) # very high cost
        elif sub_cat == "Copiers":
            cost_pct = random.uniform(0.35, 0.45) # low cost, high margin
        elif category == "Technology":
            cost_pct = random.uniform(0.45, 0.60)
        elif category == "Office Supplies":
            cost_pct = random.uniform(0.50, 0.70)
        else: # Furniture
            cost_pct = random.uniform(0.70, 0.85)
            
        unit_cost = round(unit_price * cost_pct, 2)
        total_cost = round(quantity * unit_cost, 2)
        
        profit = round(sales - total_cost, 2)
        
        # 9. Payment Method
        pay_method = random.choice(payment_methods)
        
        records.append({
            "Order ID": ord_id,
            "Order Date": ord_date,
            "Ship Date": ship_date,
            "Customer ID": cust_id,
            "Customer Name": cust_name,
            "Region": region,
            "State": state,
            "City": city,
            "Category": category,
            "Sub-Category": sub_cat,
            "Product ID": prod_id,
            "Product Name": prod_name,
            "Sales": sales,
            "Quantity": quantity,
            "Discount": discount,
            "Profit": profit,
            "Salesperson": salesperson,
            "Payment Method": pay_method
        })
        
    df = pd.DataFrame(records)
    
    # Introduce "Dirty Data" anomalies
    # A. Duplicates (duplicate ~120 rows exactly)
    dup_indices = np.random.choice(df.index, size=120, replace=False)
    df_dups = df.loc[dup_indices].copy()
    # Reset order ID slightly to represent exact duplicates
    df = pd.concat([df, df_dups], ignore_index=True)
    
    # B. Missing/Null values (~70 rows with missing Ship Date, ~70 rows with missing Payment Method, ~50 with missing Customer Name)
    ship_null_idx = np.random.choice(df.index, size=70, replace=False)
    df.loc[ship_null_idx, "Ship Date"] = None
    
    pay_null_idx = np.random.choice(df.index, size=70, replace=False)
    df.loc[pay_null_idx, "Payment Method"] = None
    
    cust_null_idx = np.random.choice(df.index, size=50, replace=False)
    df.loc[cust_null_idx, "Customer Name"] = None
    
    # C. Inconsistent Casing in Region and Category
    # Vary Region to: uppercase, lowercase, mixed case
    region_mix_idx = np.random.choice(df.index, size=200, replace=False)
    for idx in region_mix_idx:
        val = df.loc[idx, "Region"]
        df.loc[idx, "Region"] = random.choice([val.upper(), val.lower(), f" {val} "]) # add extra spaces too
        
    category_mix_idx = np.random.choice(df.index, size=200, replace=False)
    for idx in category_mix_idx:
        val = df.loc[idx, "Category"]
        df.loc[idx, "Category"] = random.choice([val.upper(), val.lower(), f" {val} "])
        
    # D. Spacing issues (leading/trailing spaces in Product Name, Customer Name, and Sub-Category)
    spacing_idx = np.random.choice(df.index, size=300, replace=False)
    for idx in spacing_idx:
        if df.loc[idx, "Customer Name"] is not None:
            df.loc[idx, "Customer Name"] = f"  {df.loc[idx, 'Customer Name']} "
        df.loc[idx, "Product Name"] = f" {df.loc[idx, 'Product Name']}   "
        df.loc[idx, "Sub-Category"] = f" {df.loc[idx, 'Sub-Category']} "
        
    # E. Mix Date Formats (format a subset of dates as strings)
    # Order Dates: make some string formats like "MM/DD/YYYY" or "YYYY/MM/DD"
    date_str_idx = np.random.choice(df.index, size=400, replace=False)
    for idx in date_str_idx:
        d = df.loc[idx, "Order Date"]
        if isinstance(d, datetime.date):
            fmt = random.choice(["%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y"])
            df.loc[idx, "Order Date"] = d.strftime(fmt)
            
    # F. Anomalies / Outliers (invalid numeric values for validation checking)
    # 10 negative quantities, 10 records with Sales = 0
    neg_qty_idx = np.random.choice(df.index, size=15, replace=False)
    df.loc[neg_qty_idx, "Quantity"] = -df.loc[neg_qty_idx, "Quantity"]
    
    zero_sales_idx = np.random.choice(df.index, size=15, replace=False)
    df.loc[zero_sales_idx, "Sales"] = 0.00
    df.loc[zero_sales_idx, "Profit"] = -50.00 # representing direct loss
    
    # Shuffle the dataset to mix duplicates and anomalies
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Ensure directories exist
    os.makedirs("data", exist_ok=True)
    
    # Save raw sales data to Excel (using openpyxl engine)
    raw_path = os.path.join("data", "raw_sales_data.xlsx")
    df.to_excel(raw_path, index=False, sheet_name="Raw Sales Data")
    print(f"Generated raw data and saved to: {raw_path}")
    print(f"Total records generated (with duplicates/anomalies): {len(df)}")
    
if __name__ == "__main__":
    generate_records()
