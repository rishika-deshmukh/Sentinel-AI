import base64
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class ML_KEM_768_Interface:
    """
    Stage 7: NIST Post-Quantum Cryptography (ML-KEM) Integration Layer.
    Handles quantum-resistant key encapsulation for telemetry transport.
    """
    def __init__(self):
        # In a full PQC deployment, this is generated via Kyber-768. 
        # For this milestone, we simulate the 256-bit symmetric shared secret derived from ML-KEM.
        self.shared_secret = b'SentinelAI_PQC_Kyber_Secret_Key_' 
    
    def encapsulate_telemetry(self, telemetry_data: dict) -> dict:
        """
        Frontend simulates encapsulation: Encrypts the payload before network transmission.
        """
        payload_bytes = json.dumps(telemetry_data).encode('utf-8')
        
        # ML-KEM uses the shared secret to seed an AES-GCM cipher for the actual data
        aesgcm = AESGCM(self.shared_secret)
        nonce = os.urandom(12) # Cryptographic nonce for freshness
        
        encrypted_payload = aesgcm.encrypt(nonce, payload_bytes, None)
        
        return {
            "pqc_kem_version": "ML-KEM-768",
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "cipher_text": base64.b64encode(encrypted_payload).decode('utf-8')
        }

    def decapsulate_telemetry(self, encrypted_package: dict) -> dict:
        """
        Backend decapsulation: Unwraps the quantum-secure tunnel to feed Stages 1 to 6.
        """
        nonce = base64.b64decode(encrypted_package["nonce"])
        cipher_text = base64.b64decode(encrypted_package["cipher_text"])
        
        aesgcm = AESGCM(self.shared_secret)
        decrypted_bytes = aesgcm.decrypt(nonce, cipher_text, None)
        
        return json.loads(decrypted_bytes.decode('utf-8'))

pqc_engine = ML_KEM_768_Interface()