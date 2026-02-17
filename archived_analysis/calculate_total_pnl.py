import re

log_path = "/home/aa598/.openclaw/workspace/singularity/project/v1/challenge_multi.log"
starting_balance = 281.25
realized_profit = 0.0

with open(log_path, 'r') as f:
    for line in f:
        # Match PNL: +x.xx% or -x.xx%
        match = re.search(r"PNL: ([-+]?\d*\.\d+|\d+)%", line)
        if match:
            pnl_pct = float(match.group(1)) / 100.0
            # Margin is now 25% of balance at entry time, roughly 70 USDT on average
            # Let's use a more accurate estimate based on the log's margin info if available
            margin_match = re.search(r"Margin: ([-+]?\d*\.\d+|\d+)", line)
            margin = float(margin_match.group(1)) if margin_match else 65.0
            realized_profit += (margin * pnl_pct)

total_pnl_pct = (realized_profit / starting_balance) * 100
current_equity = starting_balance + realized_profit

print(f"Total Realized Profit: {realized_profit:.2f} USDT")
print(f"Total Return Percentage: {total_pnl_pct:.2f}%")
print(f"Current Estimated Equity: {current_equity:.2f} USDT")
