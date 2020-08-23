"""Contains hashers that generate unique transaction id."""

import hashlib
import secrets


def generate_unique_sha_512() -> str(64):
    """Generate unique sha512."""
    seed = secrets.token_bytes(32)
    m = hashlib.sha256(seed)
    return m.hexdigest()
