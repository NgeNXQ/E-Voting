from enum import Enum
import rsa
import uuid
from cryptography.fernet import Fernet
from models import Candidate, VotePayload, VotePool, SignedVote, VotePoolsCluster

class VoterDebugMode(Enum):
    NONE = 0
    MISSING_SIGNATURE = 1
    VOTE_RECORD_SUBSTITUTION = 3

class VoterController:

    def __init__(self, is_able_to_vote: bool, debug_mode: VoterDebugMode = VoterDebugMode.NONE) -> None:
        self._id = uuid.uuid4().int
        self._debug_mode = debug_mode
        self._mask_key = Fernet.generate_key()
        self._is_able_to_vote = is_able_to_vote
        (self._public_key, self._private_key) = rsa.newkeys(nbits = 512)

    def get_id(self) -> int:
        return self._id

    def get_mask_key(self) -> bytes:
        return self._mask_key

    def get_is_able_to_vote(self) -> bool:
        return self._is_able_to_vote

    def get_public_key(self) -> rsa.PublicKey:
        return self._public_key

    def get_debug_mode(self) -> VoterDebugMode:
        return self._debug_mode

    def create_vote_pools_cluster(self, candidates: list[Candidate], size: int) -> VotePoolsCluster:
        if candidates is None or len(candidates) < 1:
            raise ValueError("Invalid candidates value")

        vote_payloads = [VotePayload(candidate.get_id(), self._id, self._mask_key) for candidate in candidates]
        [vote_payload.mask() for vote_payload in vote_payloads]
        cluster = VotePoolsCluster(VotePool(vote_payloads), size)
        return cluster

    def vote(self, candidate: Candidate, signed_vote_pool: VotePool) -> SignedVote:
        if candidate is None:
            raise ValueError("candidate cannot be None.")

        signed_vote_pool.get_vote_payload(candidate.get_id() - 1).get_vote_payload().unmask()
        return signed_vote_pool.get_vote_payload(candidate.get_id() - 1)