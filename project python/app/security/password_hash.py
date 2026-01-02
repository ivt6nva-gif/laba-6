import hashlib
import secrets
from typing import Tuple, Optional

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    to_hash = (salt + password).encode("utf-8")
    pwd_hash = hashlib.sha256(to_hash).hexdigest()
    return salt, pwd_hash