import time
import requests
import ed25519
from sixid import SixID

# 1. Setup
priv, pub = ed25519.create_keypair()
priv_hex = priv.to_ascii(encoding='hex').decode('utf-8')

# UPDATED: Port 9000 (Python Gateway)
agent = SixID("http://localhost:9000", priv_hex, "agent:machine_speed")

print("🤖 SYSTEM: Initiating Agent Verification Protocol...")
print("------------------------------------------------")

# 2. Run the Handshake
try:
    # The SDK handles the 3-step handshake internally for maximum speed
    proof = agent.certify_machinehood()

    print("1. Challenge Received.")
    print("2. Agent Auto-Signed (0ms delay).")
    print("------------------------------------------------")

    if proof['status'] == 'CERTIFIED':
        latency = float(proof['latency_ms'])
        print(f"✅ SUCCESS ({latency:.2f}ms)")
        print(f"   Limit:      30.0ms")
        print(f"   Status:     CERTIFIED_MACHINE")
        print(f"   Receipt:    {proof['receipt'][:16]}...")
    else:
        print(f"❌ FAILED: {proof}")

except Exception as e:
    print(f"\n❌ CRASH: {e}")
