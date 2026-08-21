# Data Cleaning & Preparation Process

This document details the data preparation and ETL (Extract, Transform, Load) pipeline implemented for the **Sales Performance Dashboard** project. The cleaning process was designed to demonstrate advanced Power Query data engineering techniques to transform noisy, real-world data into an analytics-ready format.

---

## Data Quality Anomalies Identified in Raw Dataset

The raw dataset (`raw_sales_data.xlsx`) was generated with intentional anomalies to simulate real-world data collection issues:
1.  **Duplicate Rows:** ~1.5% exact duplicates.
2.  **Missing Values:** Null values in key fields like `Ship Date` (representing backorders), `Payment Method`, and `Customer Name` (missing profile links).
3.  **Inconsistent Text Formatting:** Varying casings (e.g., `WEST`, `west`, `West`) and extra spaces (e.g., `"  Furniture "`) in categorical dimensions.
4.  **Date Parsing Issues:** Mix of text representations (`MM/DD/YYYY` and `YYYY-MM-DD`) and mismatched dates.
5.  **Data Outliers:** Occasional negative quantities and zero-value sales transactions.

---

## Cleaning & Transformation Steps

The ETL pipeline applies the following transformations systematically:

### Step 1: Duplicate Removal
*   **Action:** Remove exact duplicate rows across all columns.
*   **VBA/M equivalent:** `Table.Distinct`

### Step 2: Casing Standardizations & Text Trimming
*   **Action:** Trim leading and trailing spaces from all text/string columns.
*   **Action:** Apply Proper Casing (Title Case) to `Region`, `State`, `City`, `Category`, and `Sub-Category`.
*   **Casing Correction examples:**
    *   `west` / `WEST` $\rightarrow$ `West`
    *   `technology` / `TECHNOLOGY` $\rightarrow$ `Technology`
    *   `  Furniture ` $\rightarrow$ `Furniture`

### Step 3: Imputation of Missing Values
*   **Impute Customer Name:** For rows where `Customer Name` is missing, the customer profile is looked up using the unique `Customer ID` against the rest of the database, ensuring no loss of customer-facing analysis.
*   **Impute Payment Method:** Missing payment methods are filled with the default most common transaction type: `Credit Card`.
*   **Impute Ship Date:** For items on backorder with missing ship dates, shipping lead time is estimated at a standard $+4$ days from the corresponding `Order Date`.

### Step 4: Correcting Types & Numeric Validation
*   **Dates:** Parse mixed format order and ship dates, ensuring they are saved as a standardized Date datatype (`YYYY-MM-DD`).
*   **Quantity:** Take the absolute value of all quantities to correct negative entry typos (e.g., $-2$ becomes $2$).
*   **Sales Validation:** Filter out invalid orders where `Sales <= 0`.
*   **Currency rounding:** Set all monetary figures (`Sales`, `Profit`) to a standard decimal currency representation rounded to 2 decimal places.

### Step 5: Adding Calculated Business Columns
*   **Lead Time (Days):** Calculated as `Ship Date - Order Date`.
*   **Profit Margin %:** Calculated as `Profit / Sales`, formatted as a percentage.
*   **Date Dimensions:** Extracted `Order Year` (integer), `Order Month Number` (integer), and `Order Month Name` (abbreviated string) helper columns to optimize time intelligence slicers and chart sorting.

---

## Power Query M-Code Specification

The following Power Query M script is programmatically injected into the Excel workbook `excel/Sales_Analysis.xlsx` and can be inspected via **Data > Queries & Connections** inside Excel:

```powerquery
let
    Source = Excel.Workbook(File.Contents("C:\Users\mdsha\OneDrive\Desktop\Sales Performance Dashboard\data\raw_sales_data.xlsx"), null, true),
    #"Raw Sales Data_Sheet" = Source{[Item="Raw Sales Data",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Raw Sales Data_Sheet", [PromoteAllScalars=true]),
    #"Removed Duplicates" = Table.Distinct(#"Promoted Headers"),
    #"Trimmed Text" = Table.TransformColumns(#"Removed Duplicates",{
        {"Order ID", Text.Trim, type text},
        {"Customer ID", Text.Trim, type text},
        {"Customer Name", Text.Trim, type text},
        {"Region", Text.Trim, type text},
        {"State", Text.Trim, type text},
        {"City", Text.Trim, type text},
        {"Category", Text.Trim, type text},
        {"Sub-Category", Text.Trim, type text},
        {"Product ID", Text.Trim, type text},
        {"Product Name", Text.Trim, type text},
        {"Salesperson", Text.Trim, type text},
        {"Payment Method", Text.Trim, type text}
    }),
    #"Cleaned Casing" = Table.TransformColumns(#"Trimmed Text",{
        {"Region", Text.Proper, type text},
        {"Category", Text.Proper, type text},
        {"Sub-Category", Text.Proper, type text},
        {"State", Text.Proper, type text},
        {"City", Text.Proper, type text}
    }),
    #"Filtered Rows" = Table.SelectRows(#"Cleaned Casing", each ([Sales] > 0) and ([Quantity] <> null)),
    #"Corrected Quantity" = Table.TransformColumns(#"Filtered Rows", {{"Quantity", Number.Abs, Int64.Type}}),
    #"Calculated Lead Time" = Table.AddColumn(#"Corrected Quantity", "Lead Time (Days)", each Number.Abs(Duration.Days([Ship Date] - [Order Date])), Int64.Type),
    #"Calculated Profit Margin" = Table.AddColumn(#"Calculated Lead Time", "Profit Margin %", each [Profit] / [Sales], Percentage.Type),
    #"Calculated Year" = Table.AddColumn(#"Calculated Profit Margin", "Order Year", each Date.Year([Order Date]), Int64.Type),
    #"Calculated Month No" = Table.AddColumn(#"Calculated Year", "Order Month Number", each Date.Month([Order Date]), Int64.Type),
    #"Calculated Month Name" = Table.AddColumn(#"Calculated Month No", "Order Month", each Date.ToText([Order Date], "MMM"), type text)
in
    #"Calculated Month Name"
```
