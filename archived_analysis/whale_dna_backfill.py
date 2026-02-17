import json
import os
import pandas as pd
from io import StringIO

"""
Whale DNA Backfiller (V1.0)
Analyzes historical datasets to find past whale moves and their outcomes.
Populates whale_tactical_memory.json with proven '规律' (regularities).
"""

DATA_DIR = '/home/aa598/.openclaw/workspace/singularity/project/v2'
MEMORY_PATH = '/home/aa598/.openclaw/workspace/singularity/project/v1/whale_tactical_memory.json'

IMPACT_COEFF = {
    "BTCUSDT": 0.0005,
    "ETHUSDT": 0.0015,
    "SOLUSDT": 0.0050 
}

def backfill():
    memory = {}
    print("🧬 Starting Historical DNA Analysis (Backfilling Patterns)...")

    for symbol in IMPACT_COEFF.keys():
        path = os.path.join(DATA_DIR, f"dataset_{symbol.lower()}.csv")
        if not os.path.exists(path): continue
        
        # Read a larger chunk of history (last 10k trades)
        df = pd.read_csv(path, names=['ts_now', 'ts_event', 'price', 'qty', 'maker']).tail(10000)
        df['usd_val'] = df['price'] * df['qty']
        
        threshold = 500000 if "BTC" in symbol else 200000 if "ETH" in symbol else 50000
        
        # Find Whale Events
        whales = df[df['usd_val'] >= threshold]
        
        for idx, row in whales.iterrows():
            # Intent: maker=False is Buy, maker=True is Sell
            intent = "ACCUMULATION" if not row['maker'] else "DISTRIBUTION"
            entry_price = row['price']
            
            # Look ahead ~500 trades for outcome (approx 5-10 mins)
            lookahead = df.loc[idx+1:idx+500]
            if len(lookahead) < 100: continue
            
            exit_price = lookahead['price'].iloc[-1]
            pnl = (exit_price - entry_price) / entry_price
            if intent == "DISTRIBUTION": pnl = -pnl
            
            pattern_key = f"{symbol}_{intent}"
            if pattern_key not in memory:
                memory[pattern_key] = {"success_count": 0, "fail_count": 0, "avg_pnl": 0.0}
            
            stats = memory[pattern_key]
            if pnl > 0.0005: stats['success_count'] += 1
            else: stats['fail_count'] += 1
            stats['avg_pnl'] = (stats['avg_pnl'] * 0.95) + (pnl * 0.05)

    with open(MEMORY_PATH, 'w') as f:
        json.dump(memory, f, indent=2)
    print(f"✅ DNA Backfill Complete. {len(memory)} patterns identified.")

if __name__ == "__main__":
    backfill()
