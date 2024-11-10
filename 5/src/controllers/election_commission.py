from typing import Callable
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from helpers.codicons import *
from models import PartialVote, SignedPartialVote

class ElectionCommissionController:

    def __init__(self, id: int, dsa_public_key: dsa.DSAPublicKey, voters_ids: list[int], election_finished: Callable[[int, dict[int, PartialVote]], None]) -> 'ElectionCommissionController':
        if dsa_public_key is None:
            raise ValueError("dsa_public_key cannot be None")

        if voters_ids is None:
            raise ValueError("voters_ids cannot be None")

        if election_finished is None:
            raise ValueError("election_finished cannot be None")

        self._id: int = id
        self._voters_ids: list[int] = voters_ids
        self._election_finished = election_finished
        self._votes: dict[int, PartialVote] = dict()
        self._dsa_public_key: dsa.DSAPublicKey = dsa_public_key

    def register_vote(self, vote: SignedPartialVote) -> None:
        if vote is None:
            raise ValueError("vote cannot be None")

        print(f"\t[{self}] |PROCESSING| #{vote.get_partial_vote().get_voter_id()} ", end = '')

        if not self._verify_signature(vote):
            return

        if not self._verify_voter(vote.get_partial_vote().get_voter_id()):
            return

        print(f"\r{STATUS_ICON_APPROVED}", end = '\n')
        self._votes[vote.get_partial_vote().get_voter_id()] = vote.get_partial_vote()

        if len(self._votes) == len(self._voters_ids):
            self._election_finished(self._id, self._votes)

    def _verify_signature(self, vote: SignedPartialVote) -> bool:
        print(f"|SIGNATURE VERIFICATION|: ", end = '')

        try:
            self._dsa_public_key.verify(vote.get_signature(), hash(vote.get_partial_vote().get_voter_id()).to_bytes(length = 32), hashes.SHA256())
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

        if voter_id in self._votes.keys():
            print(f"{STATUS_ICON_FAILURE} (Voter has already voted)", end = '')
            print(f"\r{STATUS_ICON_REJECTED}")
            return False

        print(f"{STATUS_ICON_SUCCESS}", end = '')
        return True

    def print_intermediate_results(self) -> None:
        MARKER_SIZE: int = 15

        print(f"\nINTERMEDIATE VOTES ({self._id})\n")

        for key, value in self._votes.items():
            print(f"{key}: {value.get_partial_candidate_id()[:MARKER_SIZE]}")

    def __repr__(self) -> str:
        return f"ElectionCommissionController_{self._id}"
