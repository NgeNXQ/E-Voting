import rsa
import uuid
from colorama import Fore, Style
from cryptography.fernet import Fernet
from models import Candidate, VotePayload, VotePool, VotePoolsCluster

class VoterController:

    def __init__(self, is_able_to_vote: bool) -> None:
        self._id = uuid.uuid4().int
        self._mask_key = Fernet.generate_key()
        self._is_able_to_vote = is_able_to_vote

    def get_id(self) -> int:
        return self._id

    def get_mask_key(self) -> bytes:
        return self._mask_key

    def get_is_able_to_vote(self) -> bool:
        return self._is_able_to_vote

    def create_vote_pools_cluster(self, candidates: list[Candidate], size: int) -> VotePoolsCluster:
        vote_payloads = [VotePayload(candidate.get_id(), self._id, self._mask_key) for candidate in candidates]
        [vote_payload.mask() for vote_payload in vote_payloads]
        cluster = VotePoolsCluster(VotePool(vote_payloads), size)
        return cluster

    def process_commission_response(self, signed_vote_pool: VotePool, candidate: Candidate, comission_public_key: rsa.PublicKey) -> None:
        if signed_vote_pool is None:
            return None

        signed_vote = signed_vote_pool.get_vote_payload(candidate.get_id() - 1)

        try:
            rsa.verify(f"{hash(signed_vote.get_vote_payload())}".encode(), signed_vote.get_signature(), comission_public_key)
        except rsa.VerificationError:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Invalid signature")
            return

        signed_vote.get_vote_payload().unmask()
        signed_vote.encrypt(comission_public_key)
        return signed_vote