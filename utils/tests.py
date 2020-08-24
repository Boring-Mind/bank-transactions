import re

from .hashers import generate_unique_sha_512


def test_generate_unique_sha_512_returns_random_hashes():
    """Check that function returns two random sha-512 hashes."""
    hash1 = generate_unique_sha_512()
    hash2 = generate_unique_sha_512()

    assert re.fullmatch(r'[\da-f]{64}', hash1)
    assert re.fullmatch(r'[\da-f]{64}', hash2)

    assert hash1 != hash2
