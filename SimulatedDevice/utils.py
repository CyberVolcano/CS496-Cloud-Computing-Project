import time, urllib.parse, hmac, hashlib, base64

def make_sas(hostname: str, device_id: str, key: str, expiry: int=3600) -> str:
    # Resource URI
    uri = urllib.parse.quote_plus(f"{hostname}/devices/{device_id}")

    # Expiry timestamp
    expiry_time = int(time.time()) + expiry
    to_sign = f"{uri}\n{expiry_time}".encode("utf-8")

    # HMAC-SHA256 of key over the string
    signature = base64.b64encode(
        hmac.new(base64.b64decode(key), to_sign, hashlib.sha256).digest()
    )
    
    # Build the SAS token
    sas_token = (
        f"SharedAccessSignature sr={uri}"
        f"&sig={urllib.parse.quote_plus(signature.decode())}"
        f"&se={expiry_time}"
    )
    return sas_token