from common import IGammaEncryptor

class VoteRecordPayload(IGammaEncryptor):

    def __init__(self, candidate_id: int) -> None:
        self._is_encrypted = False
        self._candidate_id = candidate_id
        self._control_hash_sum = hash(candidate_id)

    def get_candidate_id(self) -> int:
        return self._candidate_id

    def set_candidate_id(self, value: int) -> None:     # demo purposes only :)
        self._candidate_id = value

    def get_is_encrypted(self) -> bool:
        return self._is_encrypted

    def get_control_hash_sum(self) -> int:
        return self._control_hash_sum

    def toggle_gamma_encryption(self, xor_key: bytes) -> None:
        self._is_encrypted = not self._is_encrypted
        xor_key_value = int.from_bytes(xor_key)
        self._candidate_id ^= xor_key_value
        self._control_hash_sum ^= xor_key_value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, VoteRecordPayload):
            return (self._is_encrypted == other._is_encrypted and
                    self._candidate_id == other._candidate_id and
                    self._control_hash_sum == other._control_hash_sum)
        return False

    def __hash__(self):
        return hash(self._candidate_id)

class SignedVoteRecord(IGammaEncryptor):

    def __init__(self, vote_record: VoteRecordPayload, signature: bytes) -> None:
        self._is_encrypted = False
        self._signature = signature
        self._vote_record = vote_record

    def get_signature(self) -> bytes:
        return self._signature

    def get_vote_record(self) -> VoteRecordPayload:
        return self._vote_record

    def get_is_encrypted(self) -> bool:
        return self._is_encrypted and self._vote_record.get_is_encrypted()

    def toggle_gamma_encryption(self, xor_key: bytes) -> None:
        self._is_encrypted = not self._is_encrypted

        self._vote_record.toggle_gamma_encryption(xor_key)

        key_length = len(xor_key)
        signature_length = len(self._signature)
        self._signature = bytes([self._signature[i] ^ xor_key[i % key_length] for i in range(signature_length)])