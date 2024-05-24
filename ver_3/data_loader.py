import yfinance as yf
import pandas as pd

def load_stock_data(ticker, period="3y"):
    data = yf.download(ticker, period=period)
    data["Date"] = data.index
    data["Date"] = data["Date"].apply(lambda dt: dt.replace(tzinfo=None))
    data = data.resample("5min", on="Date", label="right").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }).reset_index().dropna()
    return data
