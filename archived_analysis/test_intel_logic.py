import json
import os

path = "/home/aa598/.openclaw/workspace/singularity/project/v1/world_intel.json"
with open(path, 'r') as f:
    data = json.load(f)

mult = data['intel_index']
intel_adj = 1.0 / (mult + 1e-6)
base_threshold = 0.004
final_threshold = base_threshold * intel_adj

print(f"Current Intel Index: {mult}")
print(f"Current Intel Adjustment: {intel_adj:.2f}x")
print(f"Original Threshold: {base_threshold}")
print(f"Crisis Threshold: {final_threshold:.4f}")
if final_threshold > 0.015:
    print("🛡️ VERDICT: System is in PROTECTIVE mode. Blocking risky trades.")
