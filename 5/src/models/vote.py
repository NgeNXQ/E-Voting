from utilities import rsa

class PartialVote:

    def __init__(self, voter_id: int, partial_candidate_id: int) -> 'PartialVote':
        self._voter_id: int = voter_id
        self._partial_candidate_id: int = partial_candidate_id

    def get_voter_id(self) -> int:
        return self._voter_id

    def get_partial_candidate_id(self) -> int:
        return self._partial_candidate_id

    def encrypt(self, rsa_public_key: rsa.PublicKey) -> None:
        if rsa_public_key is None:
            raise ValueError("rsa_public_key cannot be None.")

        self._partial_candidate_id = rsa.encrypt(self._partial_candidate_id, rsa_public_key)

    def decrypt(self, rsa_private_key: rsa.PrivateKey) -> None:
        if rsa_private_key is None:
            raise ValueError("rsa_public_key cannot be None.")

        self._partial_candidate_id = rsa.decrypt(self._partial_candidate_id, rsa_private_key)

class SignedPartialVote:

    def __init__(self, partial_vote: PartialVote, signature: bytes) -> 'SignedPartialVote':
        if partial_vote is None:
            raise ValueError("partial_vote cannot be None.")

        if signature is None:
            raise ValueError("signature cannot be None.")

        self._signature = signature
        self._partial_vote = partial_vote

    def get_signature(self) -> bytes:
        return self._signature

    def get_partial_vote(self) -> PartialVote:
        return self._partial_vote
