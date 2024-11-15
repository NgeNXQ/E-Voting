from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from helpers.codicons import *
from models import PartialVote, SignedPartialVote

class ElectionCommissionController:

    def __init__(self, id: int, voters_ids: list[int]) -> 'ElectionCommissionController':
        if voters_ids is None:
            raise ValueError("voters_ids cannot be None")

        self._id: int = id
        self._voters_ids: list[int] = voters_ids
        self._results: list[PartialVote] = list()

    def get_votes(self) -> list[PartialVote]:
        return self._results

    def register_vote(self, vote: SignedPartialVote, dsa_public_key: dsa.DSAPublicKey) -> None:
        if vote is None:
            raise ValueError("vote cannot be None")

        if dsa_public_key is None:
            raise ValueError("dsa_public_key cannot be None")

        print(f"\t[{self}] |PROCESSING| #{vote.get_partial_vote().get_voter_id()} ", end = '')

        if not self._verify_signature(vote, dsa_public_key):
            return

        if not self._verify_voter(vote.get_partial_vote().get_voter_id()):
            return

        self._results.append(vote.get_partial_vote())
        print(f"\r{STATUS_ICON_APPROVED}", end = '\n')

    def _verify_signature(self, vote: SignedPartialVote, dsa_public_key: dsa.DSAPublicKey) -> bool:
        print(f"|SIGNATURE VERIFICATION|: ", end = '')

        try:
            dsa_public_key.verify(vote.get_signature(), hash(vote.get_partial_vote().get_voter_id()).to_bytes(length = 32), hashes.SHA256())
        except Exception:
            print(f"{STATUS_ICON_FAILURE} (Invalid signature)", end = '')
            print(f"\r{STATUS_ICON_REJECTED}")
            return False

        print(f"{STATUS_ICON_SUCCESS} ", end = '')
        return True

    def _verify_voter(self, voter_id: int) -> bool:
        print(f"|VOTER VERIFICATION|: ", end = '')

        if voter_id not in self._voters_ids:
            print(f"{STATUS_ICON_FAILURE} (Unknown voter)", end = '')
            print(f"\r{STATUS_ICON_REJECTED}")
            return False

        if any(vote.get_voter_id() == voter_id for vote in self._results):
            print(f"{STATUS_ICON_FAILURE} (Voter has already voted)", end = '')
            print(f"\r{STATUS_ICON_REJECTED}")
            return False

        print(f"{STATUS_ICON_SUCCESS}", end = '')
        return True

    def print_results(self) -> None:
        MARKER_SIZE: int = 15

        print(f"\nINTERMEDIATE VOTES ({self._id})\n")

        for vote in self._results:
            print(f"{vote.get_voter_id()}: {str(vote.get_partial_candidate_id())[:MARKER_SIZE]}")

    def __repr__(self) -> str:
        return f"ElectionCommissionController_{self._id}"
