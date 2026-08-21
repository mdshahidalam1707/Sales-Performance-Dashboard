# Data Dictionary: Sales Performance Database

This document defines the schema of the **Sales Performance Dashboard** dataset, detailing the columns, data types, descriptions, and examples of original ("dirty") and transformed ("cleaned") values.

---

## Schema Reference

| Column Name | Data Type (Raw) | Data Type (Cleaned) | Description | Example (Dirty) | Example (Cleaned) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Order ID** | Text | Text (Standardized) | Unique identifier for each sales transaction. | `  CA-2023-100234 ` | `CA-2023-100234` |
| **Order Date** | Date / Text | Date (`YYYY-MM-DD`) | The date when the order was placed by the customer. | `12/15/2023` | `2023-12-15` |
| **Ship Date** | Date / Text | Date (`YYYY-MM-DD`) | The date when the order was shipped. | `None` (Null) | `2023-12-19` (Imputed) |
| **Customer ID** | Text | Text (Standardized) | Unique identifier for the customer. | `CS-10234` | `CS-10234` |
| **Customer Name** | Text | Text (Standardized) | First and last name of the customer. | `  john smith ` | `John Smith` |
| **Region** | Text | Text (Standardized) | Geographical business region (East, West, Central, South). | `west` or `  EAST ` | `West` or `East` |
| **State** | Text | Text (Standardized) | US state where the order was shipped. | `california` | `California` |
| **City** | Text | Text (Standardized) | City where the order was shipped. | `los angeles` | `Los Angeles` |
| **Category** | Text | Text (Standardized) | High-level product category (Technology, Furniture, Office Supplies). | `technology` | `Technology` |
| **Sub-Category** | Text | Text (Standardized) | Mid-level product classification (e.g., Phones, Chairs, Binders). | `  PHONES ` | `Phones` |
| **Product ID** | Text | Text (Standardized) | Unique identifier for the specific product sold. | `TEC-PH-1000001` | `TEC-PH-1000001` |
| **Product Name** | Text | Text (Standardized) | Full commercial name of the product. | ` Apple iPhone 14 Pro   ` | `Apple iPhone 14 Pro` |
| **Sales** | Decimal / Text | Currency (Double) | Revenue generated (Quantity * Price * (1 - Discount)). | `0.00` (Outlier) | `999.00` |
| **Quantity** | Integer / Text | Integer | Number of units purchased in the order. | `-2` (Outlier) | `2` (Absolute value) |
| **Discount** | Decimal / Text | Percentage (Double) | Percentage discount applied (0.0 to 0.5). | `0.2` | `0.2` (20%) |
| **Profit** | Decimal / Text | Currency (Double) | Net profit or loss (Sales - Cost). | `-50.00` | `249.50` |
| **Salesperson** | Text | Text (Standardized) | Sales representative assigned to the regional territory. | `michael chang` | `Michael Chang` |
| **Payment Method** | Text | Text (Standardized) | Payment option used (Credit Card, PayPal, Bank Transfer, Cash). | `nan` (Null) | `Credit Card` (Imputed) |
| **Lead Time (Days)** | *None* | Integer | *Calculated:* Number of days between Order Date and Ship Date. | *N/A* | `4` |
| **Profit Margin %** | *None* | Percentage (Double) | *Calculated:* Profit divided by Sales. | *N/A* | `0.25` (25.0%) |
| **Order Year** | *None* | Integer | *Calculated:* Calendar year extracted from Order Date. | *N/A* | `2023` |
| **Order Month** | *None* | Text | *Calculated:* Three-letter month abbreviation. | *N/A* | `Dec` |
| **Order Month Number**| *None* | Integer | *Calculated:* Numerical month representation (1-12) for sorting. | *N/A* | `12` |

---

## Domain Values & Validations

### 1. Categories & Sub-Categories
*   **Technology:** `Phones`, `Copiers`, `Accessories`, `Machines`
*   **Furniture:** `Chairs`, `Tables`, `Bookcases`, `Furnishings`
*   **Office Supplies:** `Paper`, `Binders`, `Storage`, `Appliances`, `Art`, `Fasteners`, `Envelopes`, `Labels`

### 2. Regions & Sales Representatives
*   **West:** `Michael Chang`, `Emily Wong`
*   **East:** `Sarah Connor`, `John Davis`
*   **Central:** `David Miller`, `Amanda Johnson`
*   **South:** `Robert Jackson`, `Maria Rodriguez`

### 3. Numerical Business Rules
*   **Quantity:** Must be integer $> 0$.
*   **Discount:** Must be between $0.00$ ($0\%$) and $0.50$ ($50\%$).
*   **Sales:** Must be decimal $> 0$. Formula: $\text{Quantity} \times \text{Unit Price} \times (1 - \text{Discount})$.
*   **Profit:** Formula: $\text{Sales} - (\text{Quantity} \times \text{Unit Cost})$. Can be negative (losses are expected on heavily discounted furniture like Tables).
*   **Lead Time:** Formula: $\text{Ship Date} - \text{Order Date}$. Range is typically 1 to 7 days.
