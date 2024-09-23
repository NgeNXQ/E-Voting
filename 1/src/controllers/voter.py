import rsa
from models import Candidate, VoteRecord, SignedVoteRecord

class VoterController:

    def __init__(self, id: int, is_able_to_vote: bool) -> None:
        self._id = id
        self._is_able_to_vote = is_able_to_vote
        (self._public_key, self._private_key) = rsa.newkeys(nbits = 512)

    def get_id(self) -> int:
        return self._id

    def get_is_able_to_vote(self) -> bool:
        return self._is_able_to_vote

    def get_public_key(self) -> rsa.PublicKey:
        return self._public_key

    def vote(self, candidate: 'Candidate') -> 'VoteRecord':
        if candidate is None:
            raise ValueError("candidate is None.")

        return VoteRecord(self._public_key, candidate.get_id())

    def sign(self, vote_record: 'VoteRecord') -> 'SignedVoteRecord':
        if vote_record is None:
            raise ValueError("vote_record is None.")

        signature = rsa.sign(vote_record.get_candidate_id().to_bytes(), self._private_key, "SHA-256")
        return SignedVoteRecord(vote_record, signature)