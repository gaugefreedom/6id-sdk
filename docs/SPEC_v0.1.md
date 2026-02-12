# 6ID SDK — Specification v0.1 (MVP)

**Component:** Client Library & Developer Portal
**Repository:** `6id-sdk`
**License:** Apache 2.0
**Status:** Private Beta / Preview

---

## 1. Overview

This repository hosts the official client libraries for the **Intelexta Identity (IXI)** platform.
The v0.1 release focuses on the **Execution Proof** ("IXI-Lite"), allowing agents to connect to the Intelexta Causality Kernel (IXC) to perform a "Reverse Turing Test" (cryptographic handshake < 30ms).

## 2. Repository Structure (Monorepo)

The repository uses a monorepo pattern to support multiple languages and documentation site generation.

```text
/
├── python/                     # Python SDK (Active)
│   ├── src/sixid/              # Source code
│   ├── tests/                  # Unit tests
│   └── pyproject.toml          # Build config
│
├── typescript/                 # TypeScript SDK (Placeholder)
│   └── README.md               # "Coming Soon"
│
├── docs/                       # Developer Portal (GitHub Pages)
│   ├── index.html              # Landing Page
│   └── assets/                 # Images/Video
│
├── LICENSE                     # Apache 2.0
└── README.md                   # Universal entry point

```

---

## 3. Python SDK Specification

**Package Name:** `sixid`
**Version:** `0.1.0-beta`

### 3.1 Dependencies

* `requests >= 2.31.0` (HTTP Client)
* `ed25519 >= 1.5` (Signing Library)

### 3.2 Class: `SixID`

**Constructor:**
`__init__(self, api_url: str, private_key_hex: str, agent_id: str)`

* `api_url`: The endpoint of the Verification Kernel (e.g., `https://kernel.intelexta.com`).
* `private_key_hex`: The 32-byte Ed25519 private key (hex string).
* `agent_id`: The 6ID handle or agent reference (e.g., `agent:demo_01`).

**Method:**
`certify_machinehood(self) -> dict`

**Logic Flow (The "Handshake"):**

1. **Start Timer.**
2. **Request Challenge:** Call `POST {api_url}/v1/reserve` with `{resource_id: "cert:slot", qty: 1}`.
* *Error Handling:* Raise exception on network failure.


3. **Sign Challenge:**
* Extract `challenge.message_b64` from response.
* Sign the UTF-8 bytes of the message using `self.signer`.
* Encode signature as URL-safe Base64 string.


4. **Submit Proof:** Call `POST {api_url}/v1/commit` with `proof: {type: "ed25519", signature_b64: ...}`.
5. **Stop Timer.** Calculate `latency_ms`.

**Return Value (Success):**

```python
{
    "status": "CERTIFIED",
    "proof_type": "execution_speed",
    "latency_ms": "12.50",
    "receipt": "sha256:..." # The Commit Receipt Hash
}

```

**Return Value (Failure):**

```python
{
    "status": "FAILED",
    "reason": "Too Slow (>30ms) or Invalid Signature"
}

```

---

## 4. Developer Portal Specification (`docs/`)

The `docs/` folder contains a static site to be served via GitHub Pages.

**Page:** `index.html`
**Theme:** Dark Mode (Black background, Green accents, Monospace fonts).

**Sections:**

1. **Hero:**
* Title: "6ID Developer Center"
* Subtitle: "The Standard for Non-Human Identity (NHI)."


2. **Demo:**
* Embed Container: `<div id="demo-video"></div>` (Placeholder for Ray's video).
* Caption: "Live Verification: Human (450ms) vs. Agent (12ms)."


3. **Quick Start:**
* Code Block (Python):
```python
from sixid import SixID
agent = SixID(key="...", id="agent:01")
print(agent.certify_machinehood())

```


4. **Footer:**
* "Contact sales@intelexta.com for Private Beta Keys."


---

## 5. Future Roadmap (Non-Normative)

* **v0.2:** TypeScript SDK support.
* **v0.3:** Full 6ID Registry integration (Policy checks, Reputation scores).