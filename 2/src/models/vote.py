import copy
import rsa
from cryptography.fernet import Fernet
from common import IEncryptorRSA, IMask

class VotePayload(IEncryptorRSA, IMask):

    def __init__(self, candidate_id: int, uuid: int, mask_key: bytes) -> None:
        self._uuid = uuid
        self._is_masked = False
        self._is_encrypted = False
        self._cipher = Fernet(mask_key)
        self._candidate_id = candidate_id

    def get_uuid(self) -> int:
        return self._uuid

    def get_candidate_id(self) -> int:
        return self._candidate_id

    def get_is_masked(self) -> bool:
        return self._is_masked

    def get_is_encrypted(self) -> bool:
        return self._is_encrypted

    def mask(self) -> None:
        self._is_masked = True
        self._uuid = self._cipher.encrypt(self._uuid.to_bytes(16))

    def unmask(self) -> None:
        self._is_masked = False
        self._uuid = int.from_bytes((self._cipher.decrypt(self._uuid)))

    def encrypt(self, public_key: rsa.PublicKey) -> None:
        self._is_encrypted = True
        self._uuid = rsa.encrypt(self._uuid.to_bytes(16), public_key)
        self._candidate_id = rsa.encrypt(self._candidate_id.to_bytes(), public_key)

    def decrypt(self, private_key: rsa.PrivateKey) -> None:
        self._is_encrypted = False
        self._uuid = int.from_bytes(rsa.decrypt(self._uuid, private_key))
        self._candidate_id = int.from_bytes(rsa.decrypt(self._candidate_id, private_key))

class SignedVote(IEncryptorRSA):

    def __init__(self, vote_payload: VotePayload, signature: bytes) -> None:
        self._is_encrypted = False
        self._signature = signature
        self._vote_payload = vote_payload

    def get_signature(self) -> bytes:
        return self._signature

    def get_is_encrypted(self) -> bool:
        return self._is_encrypted

    def get_vote_payload(self) -> VotePayload:
        return self._vote_payload

    def encrypt(self, public_key: rsa.PublicKey) -> None:
        self._is_encrypted = True
        self._vote_payload.encrypt(public_key)

    def decrypt(self, private_key: rsa.PrivateKey) -> None:
        self._is_encrypted = False
        self._vote_payload.decrypt(private_key)

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