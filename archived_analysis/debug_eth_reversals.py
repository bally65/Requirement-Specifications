import pandas as pd
df = pd.read_csv("/home/aa598/.openclaw/workspace/singularity/project/v2/dataset_ethusdt.csv", names=['ts', 'ts2', 'p', 'q', 'm'])
df['dt'] = pd.to_datetime(df['ts'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Taipei')
# 檢查 05:00 前後的異常
v1 = df[(df['dt'] >= '2026-02-16 05:01:00') & (df['dt'] <= '2026-02-16 05:02:00') & (df['p'] > 0)]
# 檢查 05:32 前後的異常
v2 = df[(df['dt'] >= '2026-02-16 05:32:00') & (df['dt'] <= '2026-02-16 05:33:00') & (df['p'] > 0)]

print("--- 05:01 Reversal Detail ---")
print(v1[['dt', 'p', 'q', 'm']].tail(5))
print("--- 05:32 Reversal Detail ---")
print(v2[['dt', 'p', 'q', 'm']].tail(5))
