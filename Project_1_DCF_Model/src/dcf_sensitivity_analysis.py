import os
import pandas as pd
import yfinance as yf

def generate_million_row_warehouse():
    # Expanding the universe to hundreds of tickers (or use an S&P 500 list)
    tickers = [
        "MSFT", "AAPL", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "AMD", "INTC",
        "JPM", "BAC", "WMT", "COST", "JNJ", "PFE", "XOM", "CVX", "NFLX",
        "DIS", "BA", "CAT", "GS", "MS", "UNH", "HD", "VZ", "T", "PYPL",
        "SPY", "QQQ", "V", "MA", "UNH", "JNJ", "XOM", "WMT", "PG", "JPM"
    ]
    
    print(f"=== Initializing Million-Row Quantitative Market Warehouse ===")
    
    master_records = []
    
    # Pulling maximum available daily history (10+ years per ticker)
    for ticker in tickers:
        try:
            print(f"Downloading daily historical market data for {ticker}...")
            stock = yf.Ticker(ticker)
            df_history = stock.history(period="max")
            
            if df_history.empty:
                continue
                
            # Reset index to turn the Date into a column
            df_history = df_history.reset_index()
            
            for _, row in df_history.iterrows():
                master_records.append({
                    "Ticker": ticker,
                    "Date": str(row['Date']).split()[0],
                    "Open": row['Open'],
                    "High": row['High'],
                    "Low": row['Low'],
                    "Close": row['Close'],
                    "Volume": row['Volume'],
                    "Daily_Return": row['Close'] - row['Open'] # Simple intraday delta example
                })
                
        except Exception as e:
            print(f"-> Note for {ticker}: {e}")
            
    df_warehouse = pd.DataFrame(master_records)
    
    if df_warehouse.empty:
        print("\n[Error] No records captured.")
        return
        
    output_dir = os.path.join("..", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "Million_Row_Market_Warehouse.csv")
    df_warehouse.to_csv(output_file, index=False)
    
    print(f"\n[Success] Massive quantitative dataset compiled!")
    print(f"Total Rows Generated: {len(df_warehouse):,}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    generate_million_row_warehouse()
