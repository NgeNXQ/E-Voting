from elgamal import elgamal

class Vote:

    DELIMITER_BYTE: bytes = b'\xFF'

    CHUNKS_COUNT: int = 3
    CHUNK_CANDIDATE_ID_INDEX: int = 0
    CHUNK_SEED_INDEX: int = 1
    CHUNK_VOTER_ID_INDEX: int = 2

    _next_id: int = -1

    def __init__(self, payload: elgamal.CipherText) -> 'Vote':
        Vote._next_id += 1
        self._payload = payload
        self._id = Vote._next_id

    def get_id(self) -> int:
        return self._id

    def get_payload(self) -> elgamal.CipherText:
        return self._payload

