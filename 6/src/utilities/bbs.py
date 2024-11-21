class KeysPair:
    def __init__(self, public_key: int, private_key: tuple[int, int], seed: int):
        self._seed: int = seed
        self._public_key: int = public_key
        self._private_key: tuple[int, int] = private_key

    def get_seed(self) -> int:
        return self._seed

    def get_public_key(self) -> int:
        return self._public_key

    def get_private_key(self) -> tuple[int, int]:
        return self._private_key

def new_keys() -> KeysPair:
    p: int = 11
    q: int = 23
    seed: int = 7
    return KeysPair((p * q), (p, q), seed)

def encrypt(message: int, seed: int, public_key: int) -> int:
    random_bits = _generate_bits(message.bit_length(), seed, public_key)
    return message ^ random_bits

def decrypt(ciphertext: int, seed: int, public_key: int) -> int:
    random_bits = _generate_bits(ciphertext.bit_length(), seed, public_key)
    return ciphertext ^ random_bits

def _generate_bits(length: int, seed: int, public_key: int) -> int:
    result: int = 0
    x: int = (seed ** 2) % public_key

    for _ in range(length):
        x = (x ** 2) % public_key
        result = (result << 1) | (x & 1)

    return result
