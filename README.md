# 6ID SDK

![Status: Private Beta](https://img.shields.io/badge/Status-Private%20Beta-yellow)
![Proof: Execution Speed](https://img.shields.io/badge/Proof-Execution%20Speed-brightgreen)

Official client libraries for the **Intelexta Identity (IXI)** platform.
Verify Non-Human Identity (NHI) through cryptographic Execution Proofs against the Intelexta Causality Kernel.

## How It Works

An agent proves its machine identity by completing a three-step handshake in under 30 ms:

1. **Request challenge** — reserve a certification slot on the Kernel
2. **Sign challenge** — sign the challenge bytes with Ed25519
3. **Submit proof** — commit the signed proof and receive a verifiable receipt

## SDKs

| Language | Status | Path |
|---|---|---|
| Python | Available | [python/](./python) |
| TypeScript | Coming Soon | [typescript/](./typescript) |

## Quick Start (Python)

```bash
cd python
pip install -e .
```

```python
from sixid import SixID

agent = SixID(
    api_url="https://kernel.intelexta.com",
    private_key_hex="your_ed25519_key_hex",
    agent_id="agent:demo_01",
)

result = agent.certify_machinehood()
print(result)
# {'status': 'CERTIFIED', 'proof_type': 'execution_speed', 'latency_ms': '12.50', 'receipt': '...'}
```

## Documentation

- [SDK Specification](./docs/SPEC_v0.1.md)
- [Developer Portal](https://gaugefreedom.github.io/6id-sdk/)

## License

Apache 2.0 — see [LICENSE](./LICENSE).
