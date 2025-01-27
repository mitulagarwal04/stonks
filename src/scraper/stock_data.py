# src/scraper/stock_data.py

import yfinance as yfinance
import pandas as pd 
from datetime import datetime, timedelta

def fetch_stock_data(symbol = "", days=365):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    data = yf.download(
        symbol,
        start_date = start_date.strftime("%Y-%m-%d"),
        end_date = end_date.strftime("%Y-%m-%d"),
        interval = '1d'
    )

    data.to_csv(f"data/raw/stocks/{symbol}.csv", index=False)
    print(f"Saved {symbol} data ({len(data)} rows.)")

if __name__=="__main__":
    fetch_stock_data()

    