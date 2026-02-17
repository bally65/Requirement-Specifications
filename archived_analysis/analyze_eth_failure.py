import pandas as pd
import numpy as np
from io import StringIO
import os

path = "/home/aa598/.openclaw/workspace/singularity/project/v2/dataset_ethusdt.csv"
# Read last 5000 rows to cover the early morning period
df = pd.read_csv(path, names=['ts_now', 'ts_event', 'price', 'qty', 'maker'])
# Convert ts_now to readable time (assuming ms)
df['time'] = pd.to_datetime(df['ts_now'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Taipei')

# Filter for the failure windows: 04:55-05:10 and 05:25-05:40
window1 = df[(df['time'] >= '2026-02-16 04:55:00') & (df['time'] <= '2026-02-16 05:10:00')]
window2 = df[(df['time'] >= '2026-02-16 05:25:00') & (df['time'] <= '2026-02-16 05:40:00')]

def analyze_window(df_win, label):
    if df_win.empty: 
        print(f"Window {label} is empty.")
        return
    start_p = df_win['price'].iloc[0]
    max_p = df_win['price'].max()
    min_p = df_win['price'].min()
    end_p = df_win['price'].iloc[-1]
    vol = df_win['qty'].sum()
    # Buy vs Sell pressure (maker=False is Aggressive Buy)
    buys = df_win[df_win['maker'] == False]['qty'].sum()
    sells = df_win[df_win['maker'] == True]['qty'].sum()
    
    print(f"--- Analysis: {label} ---")
    print(f"Price Range: {start_p:.2f} -> {end_p:.2f} (High: {max_p:.2f}, Low: {min_p:.2f})")
    print(f"Volatility (Max Swing): {((max_p - min_p)/min_p)*100:.4f}%")
    print(f"Aggressive Buys: {buys:.2f} | Aggressive Sells: {sells:.2f}")
    print(f"Net Pressure: {buys - sells:.2f}")

analyze_window(window1, "05:00 Failure")
analyze_window(window2, "05:32 Failure")

