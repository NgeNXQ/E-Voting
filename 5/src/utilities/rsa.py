from sympy import mod_inverse
from Crypto.Util.number import getPrime

class PublicKey:

    def __init__(self, e: int, n: int) -> 'PublicKey':
        self._e = e
        self._n = n

    def get_e(self) -> int:
        return self._e

    def get_n(self) -> int:
        return self._n

class PrivateKey:

    def __init__(self, d: int, n: int) -> 'PublicKey':
        self._d = d
        self._n = n

    def get_d(self) -> int:
        return self._d

    def get_n(self) -> int:
        return self._n

def generate_keys(key_size: int) -> tuple[PublicKey, PrivateKey]:
    e: int = 65537
    p: int = getPrime(key_size // 2)
    q: int = getPrime(key_size // 2)
    n: int = p * q
    phi: int = (p - 1) * (q - 1)
    d: int = mod_inverse(e, phi)
    return PublicKey(e, n), PrivateKey(d, n)

def encrypt(message: int, public_key: PublicKey) -> int:
    return pow(message, public_key.get_e(), public_key.get_n())

def decrypt(ciphertext: int, private_key: PrivateKey) -> int:
    return pow(ciphertext, private_key.get_d(), private_key.get_n())
