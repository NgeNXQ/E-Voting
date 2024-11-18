
class KeysPair:

    def __init__(self, public_key: int, private_key: tuple[int, int], seed: int) -> 'KeysPair':
        self._seed = seed
        self._public_key = public_key
        self._private_key = private_key

    def get_seed(self) -> int:
        return self._seed

    def get_public_key(self) -> int:
        return self._public_key

    def get_private_key(self) -> int:
        return self._private_key

def new_keys() -> KeysPair:
    p = 11
    q = 23
    seed = 3
    return KeysPair((p * q), (p, q), seed)

def generate_bits_sequence(keys: KeysPair, length: int) -> int:
    result: int = 0
    x = keys.get_seed()

    for _ in range(length):
        x = x ** 2 % keys.get_public_key()
        result = result << 1 | (x & 1)

    return result

def encrypt(message: int, )