import os
import win32com.client
import pandas as pd

def build_excel_dashboard():
    # File paths
    raw_path = os.path.abspath(os.path.join("data", "raw_sales_data.xlsx"))
    cleaned_path = os.path.abspath(os.path.join("data", "cleaned_sales_data.xlsx"))
    output_path = os.path.abspath(os.path.join("excel", "Sales_Analysis.xlsx"))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Verify input files exist
    if not os.path.exists(raw_path) or not os.path.exists(cleaned_path):
        print("Error: Source data files not found. Run generate_data.py and clean_data.py first.")
        return
        
    print("Launching Excel Application...")
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    
    try:
        # Open source data workbooks
        print("Opening raw and cleaned data files...")
        raw_wb = excel.Workbooks.Open(raw_path)
        cleaned_wb = excel.Workbooks.Open(cleaned_path)
        
        # Create final analysis workbook
        print("Creating final analysis workbook...")
        new_wb = excel.Workbooks.Add()
        
        # Copy Raw Data and Cleaned Data worksheets
        raw_wb.Sheets(1).Copy(Before=new_wb.Sheets(1))
        new_wb.Sheets(1).Name = "Raw Data"
        
        cleaned_wb.Sheets(1).Copy(Before=new_wb.Sheets(1))
        new_wb.Sheets(1).Name = "Cleaned Data"
        
        # Clean up default sheets in new workbook
        for sheet in list(new_wb.Sheets):
            if sheet.Name not in ["Raw Data", "Cleaned Data"]:
                sheet.Delete()
                
        # Close source workbooks without saving changes
        raw_wb.Close(False)
        cleaned_wb.Close(False)
        
        # Add Power Query M Code to the workbook queries
        print("Injecting Power Query M Code...")
        raw_abs_path_escaped = raw_path.replace("\\", "\\\\")
        m_code = f"""let
    Source = Excel.Workbook(File.Contents("{raw_abs_path_escaped}"), null, true),
    #"Raw Sales Data_Sheet" = Source{{[Item="Raw Sales Data",Kind="Sheet"]}}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Raw Sales Data_Sheet", [PromoteAllScalars=true]),
    #"Removed Duplicates" = Table.Distinct(#"Promoted Headers"),
    #"Trimmed Text" = Table.TransformColumns(#"Removed Duplicates",{{
        {{"Order ID", Text.Trim, type text}},
        {{"Customer ID", Text.Trim, type text}},
        {{"Customer Name", Text.Trim, type text}},
        {{"Region", Text.Trim, type text}},
        {{"State", Text.Trim, type text}},
        {{"City", Text.Trim, type text}},
        {{"Category", Text.Trim, type text}},
        {{"Sub-Category", Text.Trim, type text}},
        {{"Product ID", Text.Trim, type text}},
        {{"Product Name", Text.Trim, type text}},
        {{"Salesperson", Text.Trim, type text}},
        {{"Payment Method", Text.Trim, type text}}
    }}),
    #"Cleaned Casing" = Table.TransformColumns(#"Trimmed Text",{{
        {{"Region", Text.Proper, type text}},
        {{"Category", Text.Proper, type text}},
        {{"Sub-Category", Text.Proper, type text}},
        {{"State", Text.Proper, type text}},
        {{"City", Text.Proper, type text}}
    }}),
    #"Filtered Rows" = Table.SelectRows(#"Cleaned Casing", each ([Sales] > 0) and ([Quantity] <> null)),
    #"Corrected Quantity" = Table.TransformColumns(#"Filtered Rows", {{"Quantity", Number.Abs, Int64.Type}}),
    #"Calculated Lead Time" = Table.AddColumn(#"Corrected Quantity", "Lead Time (Days)", each Number.Abs(Duration.Days([Ship Date] - [Order Date])), Int64.Type),
    #"Calculated Profit Margin" = Table.AddColumn(#"Calculated Lead Time", "Profit Margin %", each [Profit] / [Sales], Percentage.Type),
    #"Calculated Year" = Table.AddColumn(#"Calculated Profit Margin", "Order Year", each Date.Year([Order Date]), Int64.Type),
    #"Calculated Month No" = Table.AddColumn(#"Calculated Year", "Order Month Number", each Date.Month([Order Date]), Int64.Type),
    #"Calculated Month Name" = Table.AddColumn(#"Calculated Month No", "Order Month", each Date.ToText([Order Date], "MMM"), type text)
in
    #"Calculated Month Name"
"""
        try:
            new_wb.Queries.Add("CleanSalesData", m_code, "Power Query formula used to clean raw sales data and load to report")
        except Exception as e:
            print("Could not add query to Excel (non-critical):", e)
            
        # Determine cleaned data source range
        cleaned_ws = new_wb.Sheets("Cleaned Data")
        last_row = cleaned_ws.Cells(cleaned_ws.Rows.Count, 1).End(-4162).Row # -4162 is xlUp
        last_col = cleaned_ws.Cells(1, cleaned_ws.Columns.Count).End(-4159).Column # -4159 is xlToLeft
        source_range = cleaned_ws.Range(cleaned_ws.Cells(1, 1), cleaned_ws.Cells(last_row, last_col))
        
        # Create worksheets for Pivot Tables and Dashboard
        print("Creating Pivot Tables and Slicers...")
        pivot_ws = new_wb.Sheets.Add(Before=new_wb.Sheets(1))
        pivot_ws.Name = "Pivot Tables"
        
        dashboard_ws = new_wb.Sheets.Add(Before=new_wb.Sheets(1))
        dashboard_ws.Name = "Dashboard"
        
        # Create Pivot Cache
        # xlDatabase = 1
        pc = new_wb.PivotCaches().Create(SourceType=1, SourceData=source_range)
        
        # Pivot Table definitions
        # Format: (table_name, row_fields, data_fields, cell_addr, sort_field, sort_type, top_n_field, top_n_val, is_top)
        # xlSum = -4157, xlCount = -4112, xlDescending = 2, xlAscending = 1
        
        # PT1: Sales & Profit by Region
        pt_region = pc.CreatePivotTable(TableDestination=pivot_ws.Range("A3"), TableName="RegionPivot")
        pt_region.PivotFields("Region").Orientation = 1 # xlRowField
        pt_region.PivotFields("Region").Position = 1
        pt_region.AddDataField(pt_region.PivotFields("Sales"), "Total Sales", -4157).NumberFormat = "$#,##0"
        pt_region.AddDataField(pt_region.PivotFields("Profit"), "Total Profit", -4157).NumberFormat = "$#,##0"
        
        # PT2: Sales & Profit by Category
        pt_cat = pc.CreatePivotTable(TableDestination=pivot_ws.Range("E3"), TableName="CategoryPivot")
        pt_cat.PivotFields("Category").Orientation = 1
        pt_cat.PivotFields("Category").Position = 1
        pt_cat.AddDataField(pt_cat.PivotFields("Sales"), "Total Sales", -4157).NumberFormat = "$#,##0"
        pt_cat.AddDataField(pt_cat.PivotFields("Profit"), "Total Profit", -4157).NumberFormat = "$#,##0"
        
        # PT3: Sales & Profit by Sub-Category
        pt_subcat = pc.CreatePivotTable(TableDestination=pivot_ws.Range("E15"), TableName="SubCategoryPivot")
        pt_subcat.PivotFields("Category").Orientation = 1
        pt_subcat.PivotFields("Category").Position = 1
        pt_subcat.PivotFields("Sub-Category").Orientation = 1
        pt_subcat.PivotFields("Sub-Category").Position = 2
        pt_subcat.AddDataField(pt_subcat.PivotFields("Sales"), "Total Sales", -4157).NumberFormat = "$#,##0"
        pt_subcat.AddDataField(pt_subcat.PivotFields("Profit"), "Total Profit", -4157).NumberFormat = "$#,##0"
        
        # PT4: Monthly Sales & Profit Trend
        pt_month = pc.CreatePivotTable(TableDestination=pivot_ws.Range("I3"), TableName="MonthlyTrendPivot")
        pt_month.PivotFields("Order Year").Orientation = 1
        pt_month.PivotFields("Order Year").Position = 1
        pt_month.PivotFields("Order Month").Orientation = 1
        pt_month.PivotFields("Order Month").Position = 2
        # Sort months manually by order month number
        pt_month.PivotFields("Order Month").AutoSort(1, "Order Month Number")
        pt_month.AddDataField(pt_month.PivotFields("Sales"), "Total Sales", -4157).NumberFormat = "$#,##0"
        pt_month.AddDataField(pt_month.PivotFields("Profit"), "Total Profit", -4157).NumberFormat = "$#,##0"
        
        # PT5: Top 10 Products by Sales
        pt_top10 = pc.CreatePivotTable(TableDestination=pivot_ws.Range("M3"), TableName="Top10Products")
        pt_top10.PivotFields("Product Name").Orientation = 1
        pt_top10.PivotFields("Product Name").Position = 1
        pt_top10.AddDataField(pt_top10.PivotFields("Sales"), "Total Sales", -4157).NumberFormat = "$#,##0"
        pt_top10.PivotFields("Product Name").AutoSort(2, "Total Sales") # descending
        # Use modern PivotFilters.Add2 instead of legacy AutoShow
        pf_top = pt_top10.PivotFields("Product Name")
        pf_top.ClearAllFilters()
        try:
            pf_top.PivotFilters.Add2(1, pt_top10.DataFields(1), 10) # xlTopCount = 1
        except Exception as filter_ex:
            print("Could not apply Top 10 filter via COM, fallback to sorting only:", filter_ex)
        
        # PT6: Bottom 10 Products by Sales
        pt_bot10 = pc.CreatePivotTable(TableDestination=pivot_ws.Range("M20"), TableName="Bottom10Products")
        pt_bot10.PivotFields("Product Name").Orientation = 1
        pt_bot10.PivotFields("Product Name").Position = 1
        pt_bot10.AddDataField(pt_bot10.PivotFields("Sales"), "Total Sales", -4157).NumberFormat = "$#,##0"
        pt_bot10.PivotFields("Product Name").AutoSort(1, "Total Sales") # ascending
        pf_bot = pt_bot10.PivotFields("Product Name")
        pf_bot.ClearAllFilters()
        try:
            pf_bot.PivotFilters.Add2(2, pt_bot10.DataFields(1), 10) # xlBottomCount = 2
        except Exception as filter_ex:
            print("Could not apply Bottom 10 filter via COM, fallback to sorting only:", filter_ex)
        
        # PT7: Salesperson Performance
        pt_salesperson = pc.CreatePivotTable(TableDestination=pivot_ws.Range("R3"), TableName="SalespersonPivot")
        pt_salesperson.PivotFields("Salesperson").Orientation = 1
        pt_salesperson.PivotFields("Salesperson").Position = 1
        pt_salesperson.AddDataField(pt_salesperson.PivotFields("Sales"), "Total Sales", -4157).NumberFormat = "$#,##0"
        pt_salesperson.AddDataField(pt_salesperson.PivotFields("Profit"), "Total Profit", -4157).NumberFormat = "$#,##0"
        pt_salesperson.PivotFields("Salesperson").AutoSort(2, "Total Sales")
        
        # PT8: Payment Method Analysis
        pt_payment = pc.CreatePivotTable(TableDestination=pivot_ws.Range("V3"), TableName="PaymentPivot")
        pt_payment.PivotFields("Payment Method").Orientation = 1
        pt_payment.PivotFields("Payment Method").Position = 1
        pt_payment.AddDataField(pt_payment.PivotFields("Sales"), "Total Sales", -4157).NumberFormat = "$#,##0"
        pt_payment.AddDataField(pt_payment.PivotFields("Order ID"), "Order Count", -4112).NumberFormat = "#,##0" # xlCount
        pt_payment.PivotFields("Payment Method").AutoSort(2, "Total Sales")
        
        # Format Pivot Table Sheets (Compact and styled)
        print("Formatting Pivot Tables worksheets...")
        pivot_ws.Columns("A:Z").AutoFit()
        
        # Add Slicers to the Dashboard tab
        # Slicers to create: Year, Region, Category, Salesperson
        print("Adding interactive slicers...")
        
        # Add slicer caches and slicers
        slicer_cache_yr = new_wb.SlicerCaches.Add2(pt_region, "Order Year", "YearCache")
        slicer_yr = slicer_cache_yr.Slicers.Add(dashboard_ws, Name="Year", Caption="Year Filter", Top=30, Left=30, Width=100, Height=100)
        
        slicer_cache_reg = new_wb.SlicerCaches.Add2(pt_region, "Region", "RegionCache")
        slicer_reg = slicer_cache_reg.Slicers.Add(dashboard_ws, Name="Region", Caption="Region Filter", Top=150, Left=30, Width=100, Height=120)
        
        slicer_cache_cat = new_wb.SlicerCaches.Add2(pt_region, "Category", "CategoryCache")
        slicer_cat = slicer_cache_cat.Slicers.Add(dashboard_ws, Name="Category", Caption="Category Filter", Top=290, Left=30, Width=100, Height=100)
        
        # Connect slicer caches to other pivot tables so they filter together
        for sc in [slicer_cache_yr, slicer_cache_reg, slicer_cache_cat]:
            for pt in [pt_cat, pt_subcat, pt_month, pt_top10, pt_bot10, pt_salesperson, pt_payment]:
                try:
                    sc.PivotTables.AddPivotTable(pt)
                except Exception as ex:
                    print(f"Connection failed for {pt.Name}: {ex}")
                    
        # Add Dashboard Charts linked to the Pivot Tables
        # Place them on the Dashboard worksheet starting at Column E
        print("Creating and placing dashboard charts...")
        
        # Chart 1: Monthly Sales Trend Line Chart (linked to pt_month)
        chart_trend = dashboard_ws.Shapes.AddChart2(227, 4) # 227 = xlLine, 4 = Line Chart style
        chart_trend.Chart.SetSourceData(pt_month.TableRange1)
        chart_trend.Top = 30
        chart_trend.Left = 160
        chart_trend.Width = 320
        chart_trend.Height = 180
        chart_trend.Chart.ChartTitle.Text = "Monthly Revenue Trend"
        
        # Chart 2: Regional Sales vs Profit Clustered Column (linked to pt_region)
        chart_region = dashboard_ws.Shapes.AddChart2(201, 1) # 201 = xlColumnClustered
        chart_region.Chart.SetSourceData(pt_region.TableRange1)
        chart_region.Top = 30
        chart_region.Left = 500
        chart_region.Width = 300
        chart_region.Height = 180
        chart_region.Chart.ChartTitle.Text = "Regional Performance (Sales vs Profit)"
        
        # Chart 3: Category Performance Stacked Bar (linked to pt_cat)
        chart_cat = dashboard_ws.Shapes.AddChart2(209, 1) # 209 = xlBarClustered
        chart_cat.Chart.SetSourceData(pt_cat.TableRange1)
        chart_cat.Top = 230
        chart_cat.Left = 160
        chart_cat.Width = 320
        chart_cat.Height = 180
        chart_cat.Chart.ChartTitle.Text = "Sales & Profit by Category"
        
        # Chart 4: Payment Method Distribution Donut Chart (linked to pt_payment)
        chart_pay = dashboard_ws.Shapes.AddChart2(251, 1) # 251 = xlDoughnut
        chart_pay.Chart.SetSourceData(pt_payment.TableRange1)
        chart_pay.Top = 230
        chart_pay.Left = 500
        chart_pay.Width = 300
        chart_pay.Height = 180
        chart_pay.Chart.ChartTitle.Text = "Payment Method Share"
        
        # Chart 5: Salesperson Performance Bar (linked to pt_salesperson)
        chart_sp = dashboard_ws.Shapes.AddChart2(209, 2) # xlBarClustered
        chart_sp.Chart.SetSourceData(pt_salesperson.TableRange1)
        chart_sp.Top = 430
        chart_sp.Left = 160
        chart_sp.Width = 640
        chart_sp.Height = 180
        chart_sp.Chart.ChartTitle.Text = "Salesperson Revenue Rankings"
        
        # Set up a beautiful header on the Dashboard
        print("Styling the Excel Dashboard sheet...")
        dashboard_ws.Range("B1").Value = "SALES PERFORMANCE DASHBOARD"
        dashboard_ws.Range("B1").Font.Size = 18
        dashboard_ws.Range("B1").Font.Bold = True
        dashboard_ws.Range("B1").Font.Color = 0x5b3100 # Dark Navy / Indigo (represented in hex/RGB)
        
        # Highlight metrics summary in the grid (KPIs)
        # We can write formulas to reference the Grand Totals of Pivot Tables to create KPI Cards
        dashboard_ws.Range("I1").Value = "Total Revenue:"
        dashboard_ws.Range("I1").Font.Bold = True
        # B2 contains total sales formula referencing Region Pivot Table grand total
        # The region pivot table starts at A3, so Grand Total of Sales is in B7, and Profit in C7
        # But cell references might change if columns/rows shift.
        # It's safer to use GETPIVOTDATA or standard formulas pointing to the cell.
        dashboard_ws.Range("J1").Formula = "=GETPIVOTDATA(\"Total Sales\", 'Pivot Tables'!$A$3)"
        dashboard_ws.Range("J1").NumberFormat = "$#,##0"
        dashboard_ws.Range("J1").Font.Bold = True
        
        dashboard_ws.Range("L1").Value = "Total Net Profit:"
        dashboard_ws.Range("L1").Font.Bold = True
        dashboard_ws.Range("M1").Formula = "=GETPIVOTDATA(\"Total Profit\", 'Pivot Tables'!$A$3)"
        dashboard_ws.Range("M1").NumberFormat = "$#,##0"
        dashboard_ws.Range("M1").Font.Bold = True
        dashboard_ws.Range("M1").Font.Color = 0x008000 # Green
        
        # Auto-fit dashboard columns to make it look clean
        dashboard_ws.Columns("A").ColumnWidth = 18
        dashboard_ws.Columns("B:Z").AutoFit()
        
        # Gridlines setting (hide gridlines on dashboard for premium app look)
        excel.ActiveWindow.DisplayGridlines = False
        
        # Save and close
        print(f"Saving final workbook to: {output_path}...")
        new_wb.SaveAs(output_path)
        new_wb.Close()
        print("Excel workbook created successfully!")
        
    except Exception as e:
        print("An error occurred during Excel building:")
        import traceback
        traceback.print_exc()
        
    finally:
        excel.Quit()

if __name__ == "__main__":
    build_excel_dashboard()
