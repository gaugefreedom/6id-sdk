# 6ID SDK

![Status: Private Beta](https://img.shields.io/badge/Status-Private%20Beta-yellow)
![Proof: Execution Speed](https://img.shields.io/badge/Proof-Execution%20Speed-brightgreen)

Official client libraries for the **Intelexta Identity (IXI)** platform.
Verify Non-Human Identity (NHI) through cryptographic Execution Proofs against the Intelexta Gateway.

## How It Works

An agent proves its machine identity by completing a three-step handshake in under 30 ms:

1. **Request challenge** — reserve a certification slot on the Gateway (`/v1/a2a/reserve`)
2. **Sign challenge** — sign the challenge bytes with Ed25519
3. **Submit proof** — commit the signed proof and receive a verifiable receipt (`/v1/a2a/commit`)

## SDKs

| Language | Status | Path |
|---|---|---|
| Python | Available | [python/](./python) |
| TypeScript | Coming Soon | [typescript/](./typescript) |

## Quick Start (Python)

```bash
# Clone the repository
git clone https://github.com/gaugefreedom/6id-sdk.git
cd 6id-sdk/python

# Install in editable mode
pip install -e .
```

```python
from sixid import SixID

agent = SixID(
    api_url="https://api.6id.com",
    private_key_hex="your_ed25519_key_hex",
    agent_id="agent:demo_01",
)

result = agent.certify_machinehood()
print(result)
# {'status': 'CERTIFIED', 'proof_type': 'execution_speed', 'latency_ms': '12.50', 'receipt': '...'}
```
**Note:** Access to the Gateway (`api_url`) is currently restricted to Private Beta partners.
To provision an Agent ID and Key Pair for your team, please contact **sales@intelexta.com**.

## Documentation

- [SDK Specification](./docs/SPEC_v0.1.md)
- [Developer Portal](https://identity.intelexta.com/)

## License

Apache 2.0 — see [LICENSE](./LICENSE).
