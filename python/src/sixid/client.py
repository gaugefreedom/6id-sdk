import requests
import time
import base64
import uuid
try:
    from ed25519 import SigningKey
except ImportError:
    SigningKey = None

class SixID:
    """
    SixID Client: The Standard for Non-Human Identity (NHI).
    Connects to the Intelexta Gateway (v0.1).
    """
    def __init__(self, api_url, private_key_hex, agent_id):
        self.api_url = api_url.rstrip('/')
        if private_key_hex and SigningKey:
            self.signer = SigningKey(bytes.fromhex(private_key_hex))
        self.agent_id = agent_id

    def certify_machinehood(self):
        """
        Performs the <30ms Execution Proof handshake.
        """
        start_time = time.time()
        
        # 1. REQUEST CHALLENGE
        reserve_idem_key = str(uuid.uuid4())
        
        try:
            res = requests.post(
                f"{self.api_url}/v1/a2a/reserve", 
                json={
                    "buyer_sixid": self.agent_id,   # <--- FIXED: Matches engine.py
                    "resource_id": "cert:slot",     # <--- FIXED: Matches engine.py
                    "qty": 1
                }, 
                headers={"Idempotency-Key": reserve_idem_key},
                timeout=2
            )
            
            if res.status_code != 200:
                return {"status": "FAILED", "reason": f"Reserve Failed ({res.status_code}): {res.text}"}
                
        except Exception as e:
            return {"status": "ERROR", "reason": f"Network unavailable: {e}"}
            
        data = res.json()
        
        # Check for logic errors (e.g. {ok: False})
        if not data.get('ok', True): 
             return {"status": "FAILED", "reason": f"Gateway Reject: {data}"}

        # Handle Challenge
        challenge_data = data.get('challenge') or data
        if 'message_b64' not in challenge_data:
             return {"status": "FAILED", "reason": f"No Challenge: {data}"}

        challenge_b64 = challenge_data['message_b64']
        reservation_id = data['reservation_id']
        
        # 2. PROVE IDENTITY (Sign)
        try:
            message_bytes = challenge_b64.encode('utf-8')
            signature_bytes = self.signer.sign(message_bytes)
            signature_b64 = base64.b64encode(signature_bytes).decode('utf-8')
        except Exception as e:
            return {"status": "FAILED", "reason": f"Signing error: {e}"}
        
        # 3. SUBMIT PROOF
        commit_idem_key = str(uuid.uuid4())
        
        commit_res = requests.post(
            f"{self.api_url}/v1/a2a/commit", 
            json={
                "reservation_id": reservation_id,
                "buyer_sixid": self.agent_id,     # <--- FIXED
                "resource_id": "cert:slot",       # <--- FIXED
                "proof": {
                    "type": "ed25519",
                    "signature_b64": signature_b64
                }
            },
            headers={"Idempotency-Key": commit_idem_key}
        )
        
        latency_ms = (time.time() - start_time) * 1000
        
        if commit_res.status_code == 200:
            receipt = commit_res.json().get('receipt', {}).get('id', 'mock-hash')
            return {
                "status": "CERTIFIED",
                "proof_type": "execution_speed",
                "latency_ms": f"{latency_ms:.2f}",
                "receipt": receipt
            }
        else:
            return {"status": "FAILED", "reason": f"Commit Failed: {commit_res.text}"}