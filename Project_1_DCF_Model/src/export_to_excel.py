import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import BarChart, Reference

# 1. Connect to MySQL database and pull live historical records
db_user = 'root'
db_password = '' # Update with your local MySQL password if needed
db_host = 'localhost'
db_name = 'enterprise_valuation'

connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

try:
    engine = create_engine(connection_string)
    query = """
        SELECT Ticker, Date, Open, High, Low, Close, Volume, Daily_Return 
        FROM market_warehouse 
        WHERE Ticker = 'MSFT' 
        ORDER BY Date ASC;
    """
    df_historical = pd.read_sql(query, con=engine)
    print(f"Connected to MySQL database successfully! Loaded {len(df_historical)} live records.")
except Exception as e:
    print(f"Database connection notice ({e}). Generating fallback dataframe.")
    data = {
        'Ticker': ['MSFT'] * 100,
        'Date': pd.date_range(end='2026-09-06', periods=100, freq='B'),
        'Open': [410.0 + i * 0.1 for i in range(100)],
        'High': [415.0 + i * 0.15 for i in range(100)],
        'Low': [408.0 + i * 0.05 for i in range(100)],
        'Close': [412.5 + i * 0.1 for i in range(100)],
        'Volume': [25000000 + i * 1000 for i in range(100)],
        'Daily_Return': [0.001] * 100
    }
    df_historical = pd.DataFrame(data)

# 2. Create Workbook & Set Professional Metadata
excel_filename = "MSFT_Valuation_Deliverable.xlsx"
wb = Workbook()

wb.properties.creator = "Habibullah Karimi"
wb.properties.last_modified_by = "Habibullah Karimi"
wb.properties.title = "MSFT Equity Valuation & Quantitative Advisory Report"
wb.properties.company = "Deloitte Valuation Services"

# Setup sheets (Stock Visuals sheet removed)
ws_cover = wb.active
ws_cover.title = "Cover & Contents"
ws_summary = wb.create_sheet(title="Summary Dashboard")
ws_dcf = wb.create_sheet(title="DCF & Sensitivity")
ws_history = wb.create_sheet(title="Historical Data")

# --- STYLING DEFINITIONS ---
navy_header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
zebra_fill = PatternFill(start_color="F9FAFC", end_color="F9FAFC", fill_type="solid")

title_font = Font(name="Calibri", size=16, bold=True, color="1B365D")
subtitle_font = Font(name="Calibri", size=12, italic=True, color="555555")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
data_font = Font(name="Calibri", size=11)
bold_font = Font(name="Calibri", size=11, bold=True)
kpi_font = Font(name="Calibri", size=12, bold=True, color="1B365D")

thin_border = Border(
    left=Side(style='thin', color='D3D3D3'), right=Side(style='thin', color='D3D3D3'),
    top=Side(style='thin', color='D3D3D3'), bottom=Side(style='thin', color='D3D3D3')
)

# ==========================================
# TAB 1: COVER & CONTENTS
# ==========================================
ws_cover.views.sheetView[0].showGridLines = True
ws_cover['B2'] = "DELOITTE VALUATION SERVICES"
ws_cover['B2'].font = Font(name="Calibri", size=20, bold=True, color="1B365D")

ws_cover['B3'] = "Enterprise Valuation & Quantitative Advisory Deliverable"
ws_cover['B3'].font = subtitle_font

ws_cover['B5'] = "Target Company:"
ws_cover['C5'] = "Microsoft Corporation (NASDAQ: MSFT)"
ws_cover['B6'] = "Prepared By:"
ws_cover['C6'] = "Habibullah Karimi, Financial Engineering & Data Advisory"
ws_cover['B7'] = "Date:"
ws_cover['C7'] = "September 2026"
ws_cover['B8'] = "Advisory Scope:"
ws_cover['C8'] = "Quantitative DCF Modeling, XLOOKUP/VLOOKUP Formulas & Pivot Summaries"

ws_cover['B11'] = "Table of Contents & Workbook Structure"
ws_cover['B11'].font = Font(name="Calibri", size=14, bold=True, color="1B365D")

toc_rows = [
    ["Tab Name", "Description & Architectural Overview"],
    ["Summary Dashboard", "High-level valuation metrics, XLOOKUP/VLOOKUP formulas, and advisory recommendations."],
    ["DCF & Sensitivity", "5-year free cash flow projections, enterprise value bridging, and dynamic sensitivity matrix."],
    ["Historical Data", "Raw market data warehouse ingestion and Pivot Summary aggregation tables."]
]

for r_idx, row in enumerate(toc_rows, start=12):
    ws_cover.cell(row=r_idx, column=2, value=row[0]).font = bold_font
    ws_cover.cell(row=r_idx, column=3, value=row[1]).font = data_font

ws_cover['B17'] = "DISCLAIMER: This report is generated via an automated quantitative data pipeline for portfolio demonstration purposes."
ws_cover['B17'].font = Font(name="Calibri", size=9, italic=True, color="777777")

# ==========================================
# TAB 2: SUMMARY DASHBOARD (With XLOOKUP & VLOOKUP)
# ==========================================
ws_summary.views.sheetView[0].showGridLines = True
ws_summary['A1'] = "EXECUTIVE SUMMARY: MSFT Valuation Report"
ws_summary['A1'].font = title_font

ws_summary.append([]) 
ws_summary.append(["Valuation Metric", "Baseline Estimate", "Advisory Notes / Dynamic Logic"])

summary_rows = [
    ["Target Ticker", "MSFT", "Primary Equity Coverage (NASDAQ)"],
    ["Current Share Price", 415.50, "Market Close as of Valuation Date"],
    ["Implied Share Price (DCF)", "='DCF & Sensitivity'!H15", "Intrinsic Value Linked Directly from DCF Model"],
    ["Implied Upside / (Downside)", "=B6/B5 - 1", "Total Return Potential Based on Intrinsic Value"],
    ["Valuation Status", "Undervalued / Buy", "Advisory Recommendation (Target Price Premium)"],
    ["Fully Diluted Shares Outstanding (M)", 7430.0, "Company SEC Filings (Q4 2026)"],
    ["Market Capitalization ($M)", "=B5*B9", "Current Equity Market Value"],
    ["Total Debt ($M)", 62540.0, "Balance Sheet Total Debt (Short & Long-Term)"],
    ["Cash & Cash Equivalents ($M)", 80800.0, "Liquid Assets & Short-Term Investments"],
    ["Net Debt ($M)", "=B11-B12", "Total Debt Less Cash (Net Cash Position)"],
    ["Weighted Average Cost of Capital (WACC)", 0.085, "Discount Rate based on Capital Asset Pricing Model"],
    ["Terminal Growth Rate", 0.025, "Long-term Perpetual Growth Rate (GDP Anchor)"],
    ["Implied Enterprise Value ($M)", 3120450, "Present Value of FCF + Terminal Value Bridge"],
    ["Implied Equity Value ($M)", "=B15-B13", "Enterprise Value Less Net Debt Adjustments"],
    ["Implied EV / LTM EBITDA Multiple", 18.5, "Implied Valuation Multiple vs. Tech Sector Peers"],
    ["XLOOKUP Test (Find Net Debt)", '=XLOOKUP("Net Debt ($M)", A6:A20, B6:B20)', "Dynamic XLOOKUP retrieval from summary table"],
    ["VLOOKUP Test (Find WACC)", '=VLOOKUP("Weighted Average Cost of Capital (WACC)", A6:C21, 2, FALSE)', "Dynamic VLOOKUP retrieval from summary table"]
]

for row in summary_rows:
    ws_summary.append(row)

# ==========================================
# TAB 3: DCF & SENSITIVITY ANALYSIS + CHART
# ==========================================
ws_dcf.views.sheetView[0].showGridLines = True
ws_dcf['A1'] = "DISCOUNTED CASH FLOW (DCF) & SENSITIVITY ANALYSIS"
ws_dcf['A1'].font = title_font

ws_dcf.append([])
ws_dcf.append(["5-Year Free Cash Flow Projections ($M)", "2026P", "2027P", "2028P", "2029P", "2030P"])
ws_dcf.append(["Free Cash Flow (FCF)", 105000, 118000, 132000, 149000, 168000])

ws_dcf.append([])
ws_dcf.append(["WACC / Terminal Growth Sensitivity Matrix", "2.0%", "2.25%", "2.5%", "2.75%", "3.0%"])

sensitivity_matrix = [
    ["7.5%", 485.20, 502.10, 520.40, 541.00, 564.20],
    ["8.0%", 445.10, 459.30, 474.50, 491.00, 509.00],
    ["8.5% (Base)", 412.50, 424.20, 442.80, 451.00, 465.30],
    ["9.0%", 385.00, 394.80, 405.50, 417.20, 430.10],
    ["9.5%", 361.20, 369.50, 378.50, 388.30, 399.00]
]

for row in sensitivity_matrix:
    ws_dcf.append(row)

ws_dcf.cell(row=15, column=1, value="Selected Intrinsic Share Price (Base Case Lookup):").font = bold_font
ws_dcf.cell(row=15, column=8, value="=D9").font = kpi_font 

# Embed FCF Bar Chart
chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "5-Year Free Cash Flow Projections ($M)"
chart.y_axis.title = "FCF ($M)"
chart.x_axis.title = "Projections Year"

data_ref = Reference(ws_dcf, min_col=2, min_row=4, max_col=6, max_row=4)
cats_ref = Reference(ws_dcf, min_col=2, min_row=3, max_col=6, max_row=3)
chart.add_data(data_ref, from_rows=True, titles_from_data=False)
chart.set_categories(cats_ref)
chart.width = 15
chart.height = 8
ws_dcf.add_chart(chart, "H3")

# ==========================================
# TAB 4: HISTORICAL DATA & PIVOT SUMMARY TABLE
# ==========================================
ws_history.views.sheetView[0].showGridLines = True

for row in dataframe_to_rows(df_historical, index=False, header=True):
    ws_history.append(row)

start_pivot_row = len(df_historical) + 4
ws_history.cell(row=start_pivot_row, column=1, value="Market Data Pivot Summary (Aggregates)").font = title_font

pivot_headers = ["Metric Description", "Value / Aggregation Formula"]
ws_history.cell(row=start_pivot_row + 2, column=1, value=pivot_headers[0]).font = header_font
ws_history.cell(row=start_pivot_row + 2, column=2, value=pivot_headers[1]).font = header_font

pivot_rows = [
    ["Total Trading Days Analyzed", f"=COUNTA(A2:A{len(df_historical)+1})"],
    ["Average Daily Close Price", f"=AVERAGE(F2:F{len(df_historical)+1})"],
    ["Maximum High Price", f"=MAX(D2:D{len(df_historical)+1})"],
    ["Minimum Low Price", f"=MIN(E2:E{len(df_historical)+1})"],
    ["Total Traded Volume (Sum)", f"=SUM(G2:G{len(df_historical)+1})"]
]

for idx, p_row in enumerate(pivot_rows, start=start_pivot_row + 3):
    ws_history.cell(row=idx, column=1, value=p_row[0]).font = bold_font
    ws_history.cell(row=idx, column=2, value=p_row[1]).font = data_font

# Helper function for professional table styling
def apply_table_styles(ws, header_row_idx, max_r=None):
    max_row_to_style = max_r if max_r else ws.max_row
    for col_num in range(1, ws.max_column + 1):
        cell = ws.cell(row=header_row_idx, column=col_num)
        if cell.value is not None:
            cell.fill = navy_header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border
        
    for row_num in range(header_row_idx + 1, max_row_to_style + 1):
        is_even = (row_num % 2 == 0)
        for col_num in range(1, ws.max_column + 1):
            cell = ws.cell(row=row_num, column=col_num)
            if cell.value is not None:
                cell.font = data_font
                cell.border = thin_border
                if is_even:
                    cell.fill = zebra_fill
                
                if ws.title == "Summary Dashboard" and col_num == 2 and isinstance(cell.value, (int, float)):
                    metric_name = str(ws.cell(row=row_num, column=1).value)
                    if "Price" in metric_name:
                        cell.number_format = "$#,##0.00"
                    elif "Rate" in metric_name or "Upside" in metric_name:
                        cell.number_format = "0.0%"
                    elif "Capitalization" in metric_name or "Value" in metric_name or "Debt" in metric_name:
                        cell.number_format = "$#,##0"
                    elif "Shares" in metric_name:
                        cell.number_format = "#,##0.0"

# Apply table formatting across tabs
apply_table_styles(ws_summary, header_row_idx=3)
apply_table_styles(ws_dcf, header_row_idx=3)   
apply_table_styles(ws_dcf, header_row_idx=6)   
apply_table_styles(ws_history, header_row_idx=1, max_r=len(df_historical)+1)
apply_table_styles(ws_history, header_row_idx=start_pivot_row+2, max_r=start_pivot_row+len(pivot_rows)+2)

# Auto-fit column widths cleanly
for sheet in wb.worksheets:
    for col in sheet.columns:
        max_len = 0
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) < 80:
                max_len = max(max_len, len(val_str))
        col_letter = get_column_letter(col[0].column)
        sheet.column_dimensions[col_letter].width = max(max_len + 4, 18)

wb.save(excel_filename)
print(f"Success! Advisory report saved to: {excel_filename}")