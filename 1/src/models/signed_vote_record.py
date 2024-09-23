from common import GammaEncryptor
from .vote_record import VoteRecord

class SignedVoteRecord(GammaEncryptor):

    def __init__(self, vote_record: VoteRecord, signature: bytes) -> None:
        self._is_encrypted = False
        self._signature = signature
        self._vote_record = vote_record

    def get_signature(self) -> bytes:
        return self._signature

    def get_vote_record(self) -> 'VoteRecord':
        return self._vote_record

    def get_is_encrypted(self) -> bool:
        return self._is_encrypted and self._vote_record.get_is_encrypted()

    def toggle_gamma_encryption(self, xor_key: bytes) -> None:
        self._is_encrypted = not self._is_encrypted

        self._vote_record.toggle_gamma_encryption(xor_key)

        key_length = len(xor_key)
        signature_length = len(self._signature)
        self._signature = bytes([self._signature[i] ^ xor_key[i % key_length] for i in range(signature_length)])