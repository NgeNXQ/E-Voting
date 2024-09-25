from enum import Enum
import rsa
from models import Candidate, VoteRecordPayload, SignedVoteRecord

class VoterDebugMode(Enum):
    NONE = 0
    MISSING_SIGNATURE = 1
    MISSING_GAMMA_ENCRYPTION = 2
    VOTE_RECORD_SUBSTITUTION = 3

class VoterController:

    def __init__(self, id: int, is_able_to_vote: bool, debug_mode: VoterDebugMode = VoterDebugMode.NONE) -> None:
        self._id = id
        self._debug_mode = debug_mode
        self._is_able_to_vote = is_able_to_vote
        (self._public_key, self._private_key) = rsa.newkeys(nbits = 512)

    def get_id(self) -> int:
        return self._id

    def get_debug_mode(self) -> VoterDebugMode:
        return self._debug_mode

    def get_is_able_to_vote(self) -> bool:
        return self._is_able_to_vote

    def get_public_key(self) -> rsa.PublicKey:
        return self._public_key

    def vote(self, candidate: Candidate) -> VoteRecordPayload:
        if candidate is None:
            raise ValueError("candidate is None.")

        return VoteRecordPayload(candidate.get_id())

    def sign(self, vote_record: VoteRecordPayload) -> SignedVoteRecord:
        if vote_record is None:
            raise ValueError("vote_record is None.")

        signature = rsa.sign(vote_record.get_candidate_id().to_bytes(), self._private_key, "SHA-256")
        return SignedVoteRecord(vote_record, signature)