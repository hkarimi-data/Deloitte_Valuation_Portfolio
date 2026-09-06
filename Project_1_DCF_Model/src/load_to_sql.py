import getpass
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def load_ticker_data_from_db(ticker: str) -> pd.DataFrame:
    """Connects to the enterprise_valuation MySQL database and fetches historical data."""
    password = getpass.getpass("Enter your MySQL root password: ")
    connection_string = f"mysql+pymysql://root:{password}@localhost:3306/enterprise_valuation"
    engine = create_engine(connection_string)
    
    query = f"""
        SELECT Ticker, Date, Open, High, Low, Close, Volume, Daily_Return 
        FROM market_warehouse 
        WHERE Ticker = '{ticker}' 
        ORDER BY Date ASC;
    """
    df = pd.read_sql(query, engine)
    return df

def run_dcf_valuation(ticker: str):
    print(f"\n=== Running DCF Valuation Engine for {ticker} ===")
    
    # 1. Fetch live data from MySQL
    df = load_ticker_data_from_db(ticker)
    
    if df.empty:
        print(f"[Error] No data found for ticker: {ticker}")
        return
        
    print(f"Successfully loaded {len(df):,} rows from MySQL for {ticker}.")
    
    # 2. Extract key market data metrics
    latest_close = float(df.iloc[-1]['Close'])
    avg_volume = float(df.mean(numeric_only=True)['Volume'])
    print(f"Latest Closing Price: ${latest_close:.2f}")
    print(f"Historical Average Volume: {avg_volume:,.0f}")
    
    # 3. DCF Assumptions & Inputs (Standard Valuation Parameters)
    # (Note: Using standard institutional assumptions for portfolio demonstration)
    base_fcf = 75_000_000_000  # Estimated base Free Cash Flow ($75B for mega-cap tech baseline)
    growth_rate = 0.10         # Projected FCF growth rate (10% for next 5 years)
    discount_rate = 0.09       # WACC (Weighted Average Cost of Capital = 9%)
    terminal_growth = 0.025    # Terminal growth rate (2.5%)
    projection_years = 5
    shares_outstanding = 7_400_000_000  # Approximate share count for large cap baseline
    
    print("\n--- Projecting Free Cash Flows ({projection_years} Years) ---")
    discounted_cash_flows = []
    current_fcf = base_fcf
    
    for year in range(1, projection_years + 1):
        current_fcf *= (1 + growth_rate)
        discounted_fcf = current_fcf / ((1 + discount_rate) ** year)
        discounted_cash_flows.append(discounted_fcf)
        print(f"Year {year} Projected FCF: ${current_fcf:,.2f} | Discounted: ${discounted_fcf:,.2f}")
        
    sum_pv_fcf = sum(discounted_cash_flows)
    
    # 4. Terminal Value Calculation (Gordon Growth Model)
    terminal_value = (current_fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    pv_terminal_value = terminal_value / ((1 + discount_rate) ** projection_years)
    
    # 5. Enterprise Value & Implied Share Price Output
    enterprise_value = sum_pv_fcf + pv_terminal_value
    net_debt = 10_000_000_000  # Estimated net cash/debt adjustment
    equity_value = enterprise_value - net_debt
    implied_share_price = equity_value / shares_outstanding
    
    print("\n=== VALUATION RESULTS ===")
    print(f"Sum of PV of Cash Flows: ${sum_pv_fcf:,.2f}")
    print(f"Present Value of Terminal Value: ${pv_terminal_value:,.2f}")
    print(f"Implied Enterprise Value: ${enterprise_value:,.2f}")
    print(f"Implied Equity Value: ${equity_value:,.2f}")
    print(f"Implied Share Price: ${implied_share_price:.2f}")
    print(f"Actual Current Price: ${latest_close:.2f}")
    
    diff_pct = ((implied_share_price - latest_close) / latest_close) * 100
    print(f"Valuation Variance: {diff_pct:+.2f}% vs Market Price")
    print("==========================================")

if __name__ == "__main__":
    run_dcf_valuation("MSFT")