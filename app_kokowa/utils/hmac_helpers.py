import hmac
import hashlib
from django.conf import settings

def compute_hmac_hex(secret: str, payload: bytes) -> str:
    if isinstance(secret, str):
        secret = secret.encode()
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()

def verify_hmac(secret: str, payload: bytes, signature: str) -> bool:
    expected = compute_hmac_hex(secret, payload)
    # use compare_digest to prevent timing attacks
    return hmac.compare_digest(expected, signature)
