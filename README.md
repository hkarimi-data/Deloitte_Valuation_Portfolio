# Deloitte Valuation Portfolio

A quantitative valuation portfolio demonstrating **Discounted Cash Flow (DCF) analysis, financial modeling, market-data analysis, SQL database integration, Python-based valuation calculations, and Excel reporting.**

---

## Project Overview

### Primary Objective

Demonstrate the application of **valuation methodologies, quantitative analysis, financial modeling, data processing, and technology-enabled workflows** relevant to corporate finance and valuation consulting.

### Core Framework

The portfolio uses a **Discounted Cash Flow (DCF)** framework to estimate intrinsic value by projecting future free cash flows, discounting those cash flows using a selected discount rate, and incorporating terminal value assumptions.

### Project Highlights

- Built a **Python-based DCF valuation engine** for Microsoft Corporation
- Developed five-year **Free Cash Flow (FCF) projections**
- Calculated **Enterprise Value, Equity Value, and Implied Share Price**
- Implemented **WACC and terminal-growth sensitivity analysis**
- Built a **MySQL market-data warehouse** and SQL querying workflow
- Retrieved and processed historical market data using **Python and yfinance**
- Generated an **Excel-based valuation deliverable** with analytical outputs and visualizations
- Integrated **Python, SQL/MySQL, Pandas, and Excel** into a reproducible valuation workflow

---

## Project 1 — Microsoft DCF Valuation Model

The project develops an **integrated quantitative valuation workflow** for Microsoft Corporation.

### Valuation Methodology

The DCF model incorporates:

- Five-year free cash flow projections
- Free cash flow growth assumptions
- Discount rate / WACC assumptions
- Terminal growth assumptions
- Gordon Growth terminal value methodology
- Present value of projected cash flows
- Present value of terminal value
- Enterprise value
- Equity value
- Implied share price
- Market price comparison
- WACC and terminal-growth sensitivity analysis

The model evaluates how changes in key valuation assumptions affect estimated intrinsic value.

---

## Data & Technology Workflow

The project combines financial valuation techniques with data and technology workflows:

**Market Data → SQL/MySQL → Python/Pandas → DCF Valuation → Excel Reporting**

This workflow integrates **data processing, database management, quantitative valuation, and financial reporting** into a structured analytical process.

---

## Python

Python is used for:

- Data retrieval and processing
- Structured data transformation
- DCF valuation calculations
- Quantitative analysis
- Excel output generation

### Key Libraries & Technologies

- **Pandas**
- **NumPy**
- **SQLAlchemy**
- **yfinance**
- **OpenPyXL**

---

## SQL & MySQL

A **MySQL database** is used to store and query structured market data.

The SQL workflow supports:

- Database loading
- Structured data storage
- SQL querying
- Pandas integration
- Downstream quantitative analysis

---

## Market Data Pipeline

The project uses Python and **yfinance** to retrieve historical market data across a multi-company ticker universe.

The resulting data is transformed into a structured dataset for database storage and analytical use.

---

## Excel Valuation Deliverable

The project generates an **Excel-based valuation workbook** designed to organize analytical results and communicate valuation outputs.

The workbook includes:

- Valuation summary
- DCF analysis
- Five-year FCF projections
- WACC / terminal-growth sensitivity analysis
- Historical market data
- Lookup formulas
- Aggregated analytical tables
- FCF visualization

---

## Repository Structure

```text
Project_1_DCF_Model/
│
├── src/
│   ├── dcf_valuation_engine.py
│   ├── dcf_valuation_engine01.py
│   ├── load_to_sql.py
│   ├── query_warehouse.py
│   └── export_to_excel.py
│
├── outputs/
│   └── valuation and analytical outputs
│
└── README.md
