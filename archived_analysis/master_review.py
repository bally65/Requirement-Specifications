import re
import json
import os
import pandas as pd
from datetime import datetime

log_path = "/home/aa598/.openclaw/workspace/singularity/project/v1/challenge_multi.log"
starting_balance = 281.25
trades = []
balance_history = [starting_balance]

# Regex for parsing
entry_pattern = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(.+?)\] (.+?) @ ([\d.]+) \| Margin: ([\d.]+) \| (WinRate: [\d.]+%|Est\. Lift: .+%)"
exit_pattern = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] 🏁 \[EXIT\] (.+?) @ ([\d.]+) \| Side: (.+?) \| PNL: ([-+]?[\d.]+)% \| Reason: (.+)"
simple_exit_pattern = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] 🏁 \[EXIT\] (.+?) @ ([\d.]+) \| PNL: ([-+]?[\d.]+)% \| Reason: (.+)"
stop_pattern = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] 🛑 \[(STOP|STOP LOSS)\] (.+?) @ ([\d.]+) \| (Loss: ([-+]?[\d.]+)%|Loss: -0\.50%)"

active_trades = {}

if os.path.exists(log_path):
    with open(log_path, 'r') as f:
        for line in f:
            # Entry
            e_match = re.search(entry_pattern, line)
            if e_match:
                ts, mode, symbol, price, margin, intel = e_match.groups()
                active_trades[symbol] = {
                    "entry_ts": ts,
                    "entry_price": float(price),
                    "margin": float(margin),
                    "mode": mode,
                    "intel": intel
                }
                continue
            
            # Complex Exit
            ex_match = re.search(exit_pattern, line)
            if ex_match:
                ts, symbol, price, side, pnl, reason = ex_match.groups()
                if symbol in active_trades:
                    t = active_trades.pop(symbol)
                    t.update({
                        "exit_ts": ts,
                        "exit_price": float(price),
                        "side": side,
                        "pnl_pct": float(pnl),
                        "reason": reason,
                        "profit_usdt": t['margin'] * (float(pnl)/100.0)
                    })
                    trades.append(t)
                continue
                
            # Simple Exit
            se_match = re.search(simple_exit_pattern, line)
            if se_match:
                ts, symbol, price, pnl, reason = se_match.groups()
                if symbol in active_trades:
                    t = active_trades.pop(symbol)
                    t.update({
                        "exit_ts": ts,
                        "exit_price": float(price),
                        "pnl_pct": float(pnl),
                        "reason": reason,
                        "profit_usdt": t['margin'] * (float(pnl)/100.0)
                    })
                    trades.append(t)
                continue

            # Stop
            s_match = re.search(stop_pattern, line)
            if s_match:
                # [2026-02-14 21:33:08] 🛑 [STOP] BTCUSDT @ 0.00 | Loss: -1.00%
                ts, kind, symbol, price, loss_str, pnl_raw = s_match.groups()
                pnl = float(pnl_raw) if pnl_raw else -0.5
                if symbol in active_trades:
                    t = active_trades.pop(symbol)
                    t.update({
                        "exit_ts": ts,
                        "exit_price": float(price),
                        "pnl_pct": pnl,
                        "reason": "Hard Stop/Zero Noise",
                        "profit_usdt": t['margin'] * (pnl/100.0)
                    })
                    trades.append(t)

# Stats Calculation
df = pd.DataFrame(trades)
if not df.empty:
    total_profit = df['profit_usdt'].sum()
    win_rate = (df['pnl_pct'] > 0).mean() * 100
    avg_pnl = df['pnl_pct'].mean()
    total_trades = len(df)
    
    print(f"--- GLOBAL TRADE REVIEW ---")
    print(f"Total Trades: {total_trades}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Total Realized Profit: {total_profit:.2f} USDT")
    print(f"Average PNL per trade: {avg_pnl:.2f}%")
    print(f"Starting balance: {starting_balance} USDT")
    print(f"Final Projected Equity: {starting_balance + total_profit:.2f} USDT")
    
    print("\n--- PERFORMANCE BY ASSET ---")
    print(df.groupby('symbol')['pnl_pct'].agg(['count', 'mean', 'sum']))
    
    print("\n--- REASON BREAKDOWN ---")
    print(df['reason'].value_counts())
    
    print("\n--- LATEST 10 TRADES ---")
    print(df[['entry_ts', 'symbol', 'pnl_pct', 'reason']].tail(10))
else:
    print("No closed trades found in log.")
