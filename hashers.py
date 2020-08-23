import hashlib
import secrets


# @profile
def hash_sha512():
    seed = secrets.token_bytes(32)
    m = hashlib.sha256(seed)
    m.hexdigest()


if __name__ == '__main__':
    hash_sha512()
