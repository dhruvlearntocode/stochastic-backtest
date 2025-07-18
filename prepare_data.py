import pandas as pd
import pytz

df = pd.read_csv("SPY_1min_data_max_history.csv", parse_dates=["timestamp"])
df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert("US/Eastern")

df = df[df["timestamp"].dt.time.between(
    pd.to_datetime("09:30").time(), pd.to_datetime("16:00").time())]

df.set_index("timestamp", inplace=True)

df_5min = df.resample("5min").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum",
    "trade_count": "sum",
    "vwap": "mean"
}).dropna()

df_5min.to_csv("SPY_5min_prepared.csv")
