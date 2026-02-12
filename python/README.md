# 6ID Python SDK

Python client for the Intelexta Identity (IXI) platform.
Performs the **Execution Proof** handshake against the Intelexta Causality Kernel in < 30 ms.

## Install

```bash
cd python
pip install -e .
```

## Quick Start

```python
from sixid import SixID

agent = SixID(
    api_url="https://kernel.intelexta.com",
    private_key_hex="your_ed25519_private_key_hex",
    agent_id="agent:demo_01",
)

result = agent.certify_machinehood()
print(result)
# {'status': 'CERTIFIED', 'proof_type': 'execution_speed', 'latency_ms': '12.50', 'receipt': 'sha256:...'}
```

## API Reference

### `SixID(api_url, private_key_hex, agent_id)`

| Parameter | Type | Description |
|---|---|---|
| `api_url` | `str` | Verification Kernel endpoint |
| `private_key_hex` | `str` | 32-byte Ed25519 private key (hex) |
| `agent_id` | `str` | 6ID handle or agent reference |

### `certify_machinehood() -> dict`

Runs the three-step Reverse Turing Test:

1. **Request challenge** — reserves a certification slot on the Kernel.
2. **Sign challenge** — signs the challenge bytes with Ed25519.
3. **Submit proof** — commits the signed proof; receives a receipt hash.

Returns a dict with `status`, `proof_type`, `latency_ms`, and `receipt` on success.

## Requirements

- Python >= 3.9
- `requests >= 2.31.0`
- `ed25519 >= 1.5`

## License

Apache 2.0
