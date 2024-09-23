from rsa import PublicKey
from common import GammaEncryptor

class VoteRecord(GammaEncryptor):

    def __init__(self, public_key: 'PublicKey', candidate_id: int) -> None:
        self._is_encrypted = False
        self._public_key = public_key
        self._candidate_id = candidate_id

    def get_candidate_id(self) -> int:
        return self._candidate_id

    def get_is_encrypted(self) -> bool:
        return self._is_encrypted

    def get_public_key(self) -> 'PublicKey':
        return self._public_key

    def toggle_gamma_encryption(self, xor_key: bytes) -> None:
        self._is_encrypted = not self._is_encrypted
        self._candidate_id ^= int.from_bytes(xor_key)