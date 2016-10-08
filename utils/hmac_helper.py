import hmac
from hashlib import sha256


def make_hmac(key, message):
    return hmac.new(key, message, sha256).hexdigest()


# hmac_package compare
def compare_hmac(hmac1, hmac2):
    return compare_digest(hmac1, hmac2)


def compare_digest(x, y):
    if not (isinstance(x, bytes) and isinstance(y, bytes)):
        raise TypeError("both inputs should be instances of bytes")
    if len(x) != len(y):
        return False
    result = 0
    for a, b in zip(x, y):
        result |= ord(a) ^ ord(b)
    return result == 0
