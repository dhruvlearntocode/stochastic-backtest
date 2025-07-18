import pandas as pd
import numpy as np
import ta
import vectorbt as vbt

df = pd.read_csv("SPY_5min_prepared.csv", index_col="timestamp", parse_dates=True)

def stochastic_strategy(df, length=3, d_length=3, overbought=70, oversold=30, reverse=False):
    k = ta.momentum.stoch(df['high'], df['low'], df['close'], window=length, smooth_window=1)
    d = k.rolling(d_length).mean()
    entry = (k < d) & (k > overbought) & (d > overbought)
    exit = (k >= d) & (k < oversold) & (d < oversold)
    if reverse:
        entry, exit = exit, entry
    return entry, exit

entry, exit = stochastic_strategy(df)
pf = vbt.Portfolio.from_signals(df['close'], entry, exit, init_cash=10000, fees=0.001)
pf.stats().to_csv("backtest_stats.csv")
