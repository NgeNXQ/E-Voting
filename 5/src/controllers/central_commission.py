import random
from collections import Counter
import rsa
from helpers.codicons import *
from .voter import VoterController
from models import User, Candidate, PartialVote
from .election_commission import ElectionCommissionController

class CentralCommissionController:

    def __init__(self) -> 'CentralCommissionController':
        self._voters: dict[User, int] = dict()
        self._results: dict[int, int] = dict()
        self._candidates: dict[User, int] = dict()
        self._rsa_public_key, self._rsa_private_key = rsa.newkeys(nbits = 1024)
        self._election_commissions: list[ElectionCommissionController] = list()

    def get_voters(self) -> list[int]:
        return list(self._voters.values())

    def get_candidates(self) -> list[int]:
        return list(self._candidates.values())

    def get_rsa_public_key(self) -> rsa.PublicKey:
        return self._rsa_public_key

    def get_election_commissions(self) -> list[ElectionCommissionController]:
        return self._election_commissions

    def init_election_commissions(self, election_commissions_count: int) -> list[ElectionCommissionController]:
        if election_commissions_count <= 1:
            raise ValueError("Invalid value of election_commission_count argument.")

        for i in range(election_commissions_count):
            self._election_commissions.append(ElectionCommissionController(i, self._voters.values()))

        return self._election_commissions

    def finish_election(self, commissions_results: list[PartialVote]) -> None:
        if commissions_results is None:
            raise ValueError("commission_results cannot be None.")

        print("\nMERGING\n")

        for local_results in commissions_results:
            self._merge_votes(local_results)

    def _merge_votes(self, commission_results: list[PartialVote]) -> None:
        for vote in commission_results:
            print(f"{vote.get_voter_id()}: ", end = '')

            if vote.get_voter_id() not in self._voters.values():
                print(f"{STATUS_ICON_REJECTED} (Invalid voter)")
                continue

            voter_votes_count: int = sum(1 for vote_payload in commission_results if vote_payload.get_voter_id() == vote.get_voter_id())

            if voter_votes_count != len(self._election_commissions):
                print(f"{STATUS_ICON_REJECTED} (Voting procedure violation)")
                continue

            try:
                vote.decrypt(self._rsa_private_key)
            except Exception:
                print(f"{STATUS_ICON_REJECTED} (Decryption failed)")
                continue

            print(STATUS_ICON_APPROVED)
            self._results[vote.get_voter_id()] = vote.get_partial_candidate_id() * (self._results[vote.get_voter_id()] if vote.get_voter_id() in self._results.keys() else 1)

    def print_results(self) -> None:
        print("\nFINAL VOTES\n")

        for voter_id, candidate_id in self._results.items():
            print(f"#{voter_id}: {candidate_id}")

        print("\nRESULTS\n")

        results = Counter(self._results.values())

        for candidate_id, vote_count in results.items():
            print(f"#{candidate_id}: {vote_count} votes")

    def register_voter(self, user: User) -> VoterController:
        if user is None:
            raise ValueError("user cannot be None")

        print(f"VOTER REGISTRATION #{user.get_id()}: ", end = '')

        if not user.get_is_eligible_voter():
            print(f"{STATUS_ICON_FAILURE} (User is not able to vote)")
            return None

        if user in self._voters.keys():
            print(f"{STATUS_ICON_FAILURE} (User has been already registered as voter)")
            return None

        voter_controller = VoterController((len(self._voters) + 1))
        print(f"{STATUS_ICON_SUCCESS} ({voter_controller.get_id()})")
        self._voters[user] = voter_controller.get_id()
        return voter_controller

    def register_candidate(self, user: User) -> Candidate:
        if user is None:
            raise ValueError("user cannot be None")

        print(f"CANDIDATE REGISTRATION #{user.get_id()}: ", end = '')

        if not user.get_is_eligible_candidate():
            print(f"{STATUS_ICON_FAILURE} (User is not able to be a candidate)")
            return None

        if user in self._candidates.keys():
            print(f"{STATUS_ICON_FAILURE} (User has been already registered)")
            return None

        candidate = Candidate(self._generate_candidate_id())
        self._candidates[user] = candidate.get_id()
        print(f"{STATUS_ICON_SUCCESS} ({candidate.get_id()})")
        return candidate

    def _generate_candidate_id(self) -> int:
        CANDIDATE_ID_LOWER_BOUND: int = 2
        CANDIDATE_ID_UPPER_BOUND: int = 10

        number: int = 0
        factor1: int = 0
        factor2: int = 0

        while True:
            factor1 = random.randint(CANDIDATE_ID_LOWER_BOUND, CANDIDATE_ID_UPPER_BOUND)
            factor2 = random.randint(CANDIDATE_ID_LOWER_BOUND, CANDIDATE_ID_UPPER_BOUND)
            number = factor1 * factor2

            if number not in self._candidates.values():
                break

        return number
