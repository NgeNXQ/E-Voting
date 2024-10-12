import copy
from cryptography.fernet import Fernet

class VotePayload:

    def __init__(self, candidate_id: int, uuid: int, mask_key: bytes) -> None:
        self._uuid = uuid
        self._cipher = Fernet(mask_key)
        self._candidate_id = candidate_id

    def get_uuid(self) -> int:
        return self._uuid

    def get_candidate_id(self) -> int:
        return self._candidate_id

    def set_candidate_id(self, value: int) -> None:     # demo purposes only :)
        self._candidate_id = value

    def mask(self) -> None:
        self._candidate_id = self._cipher.encrypt(str(self._candidate_id).encode())

    def unmask(self) -> None:
        self._candidate_id = int(self._cipher.decrypt(self._candidate_id))

class SignedVote:

    def __init__(self, vote_payload: VotePayload, signature: bytes) -> None:
        self._signature = signature
        self._vote_payload = vote_payload

    def get_signature(self) -> bytes:
        return self._signature

    def get_vote_payload(self) -> VotePayload:
        return self._vote_payload

class VotePool:

    def __init__(self, votes: list[VotePayload | SignedVote]) -> None:
        self._votes = votes
        self._size = len(votes)

    def get_size(self) -> int:
        return self._size

    def get_vote_payload(self, index: int) -> VotePayload | SignedVote:
        if index < 0 or index >= self._size:
            raise IndexError("Invalid index argument")
        return self._votes[index]

class VotePoolsCluster:

    def __init__(self, vote_pool: VotePool, cluster_size: int) -> None:
        self._size = cluster_size
        self._vote_pools = [copy.deepcopy(vote_pool) for _ in range(0, cluster_size)]

    def get_size(self) -> int:
        return self._size

    def get_vote_pool(self, index: int) -> VotePool:
        if index < 0 or index >= self._size:
            raise IndexError("Invalid index argument")
        return self._vote_pools[index]