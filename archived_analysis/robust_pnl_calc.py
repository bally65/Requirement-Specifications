import re
import os

log_path = "/home/aa598/.openclaw/workspace/singularity/project/v1/challenge_multi.log"
starting_balance = 281.25
realized_profit = 0.0
active_margins = {}

if os.path.exists(log_path):
    with open(log_path, 'r') as f:
        for line in f:
            entry_match = re.search(r"\[(STABLE|LEV|SCALP).+\] (.+?) @ .+? \| Margin: ([-+]?\d*\.\d+|\d+)", line)
            if entry_match:
                symbol = entry_match.group(2)
                active_margins[symbol] = float(entry_match.group(3))
            
            exit_match = re.search(r"🏁 \[EXIT\] (.+?) @ .+? \| PNL: ([-+]?\d*\.\d+|\d+)%", line)
            if exit_match:
                symbol = exit_match.group(1)
                pnl_pct = float(exit_match.group(2)) / 100.0
                margin = active_margins.get(symbol, 65.0)
                realized_profit += (margin * pnl_pct)

current_equity = starting_balance + realized_profit
total_pnl_pct = (realized_profit / starting_balance) * 100
print(f"Profit: {realized_profit:.4f} USDT | Equity: {current_equity:.2f} USDT | ROI: {total_pnl_pct:.2f}%")
