import requests
import time
import base64
try:
    from ed25519 import SigningKey
except ImportError:
    SigningKey = None


class SixID:
    """
    SixID Client: The Standard for Non-Human Identity (NHI).
    Connects to the Intelexta Causality Kernel to perform the 'Reverse Turing Test'.
    """
    def __init__(self, api_url, private_key_hex, agent_id):
        self.api_url = api_url
        if private_key_hex and SigningKey:
            self.signer = SigningKey(bytes.fromhex(private_key_hex))
        self.agent_id = agent_id

    def certify_machinehood(self):
        """
        Performs the <30ms Execution Proof handshake.
        1. Requests a challenge (High-speed reservation slot).
        2. Signs it instantly (Physics check).
        3. Commits the proof to receive a receipt.
        """
        start_time = time.time()

        # 1. REQUEST CHALLENGE
        try:
            res = requests.post(f"{self.api_url}/v1/reserve", json={
                "buyer_ref": self.agent_id,
                "resource_id": "cert:slot",
                "qty": 1
            }, timeout=2)
            res.raise_for_status()
        except Exception as e:
            return {"status": "ERROR", "reason": f"Network unavailable: {e}"}

        data = res.json()
        challenge_b64 = data['challenge']['message_b64']
        reservation_id = data['reservation_id']

        # 2. PROVE IDENTITY (Sign the bytes)
        try:
            message_bytes = challenge_b64.encode('utf-8')
            signature_bytes = self.signer.sign(message_bytes)
            signature_b64 = base64.b64encode(signature_bytes).decode('utf-8')
        except Exception as e:
            return {"status": "FAILED", "reason": f"Signing error: {e}"}

        # 3. SUBMIT PROOF
        commit_res = requests.post(f"{self.api_url}/v1/commit", json={
            "reservation_id": reservation_id,
            "buyer_ref": self.agent_id,
            "proof": {
                "type": "ed25519",
                "signature_b64": signature_b64
            }
        })

        latency_ms = (time.time() - start_time) * 1000

        if commit_res.status_code == 200:
            return {
                "status": "CERTIFIED",
                "proof_type": "execution_speed",
                "latency_ms": f"{latency_ms:.2f}",
                "receipt": commit_res.json()['receipt_hash']
            }
        elif commit_res.status_code == 409:
            return {"status": "FAILED", "reason": "Too Slow (>30ms) or Replay Attack"}
        else:
            return {"status": "FAILED", "reason": f"Kernel Reject: {commit_res.text}"}
