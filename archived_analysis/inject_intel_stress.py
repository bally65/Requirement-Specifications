import json
import time

path = "/home/aa598/.openclaw/workspace/singularity/project/v1/world_intel.json"

def inject_crisis():
    print("🚨 INJECTING SIMULATED GLOBAL CRISIS...")
    stress_data = {
        "intel_index": 0.2, # Massive instability
        "stablecoin_status": "DEPEGGING_WARNING",
        "geopolitical_level": "CRITICAL",
        "timestamp": time.time(),
        "source": "STRESS_TEST_INJECTOR"
    }
    with open(path, 'w') as f:
        json.dump(stress_data, f, indent=2)
    print("✅ System now perceives a CRITICAL global threat.")

if __name__ == "__main__":
    inject_crisis()
