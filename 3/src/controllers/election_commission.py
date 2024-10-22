import copy
from elgamal import elgamal
from colorama import Fore, Style
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from models import Candidate, VoteDTO
from utilities import VoteCipherUtility

class ElectionCommissionController:

    def __init__(self, candidates: list[Candidate], voters_registration_ids: list[int]) -> None:
        self._public_results = dict()
        self._voters = copy.deepcopy(voters_registration_ids)
        self._results = {candidate.get_id(): 0 for candidate in candidates}

    def register_vote(self, vote: VoteDTO, dsa_public_key: dsa.DSAPublicKey, elgamal_private_key: elgamal.PrivateKey) -> None:
        if vote is None:
            raise ValueError("vote cannot be None")

        if dsa_public_key is None:
            raise ValueError("dsa_public_key cannot be None")

        try:
            decrypted_vote = VoteCipherUtility.decrypt(vote, elgamal_private_key)
        except Exception:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} (Invalid encryption)")
            return

        print(f"{Fore.YELLOW}PROCESSING{Style.RESET_ALL} #{decrypted_vote.get_voter_registration_id()} | ", end = '')

        if not self._verify_signature(vote, dsa_public_key):
            return

        if not self._validate_vote(decrypted_vote):
            return

        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL} | ", end = '')

        self._voters.remove(decrypted_vote.get_voter_registration_id())
        self._results[decrypted_vote.get_vote_payload().get_candidate_id()] += 1
        self._public_results[decrypted_vote.get_voter_custom_id()] = decrypted_vote.get_vote_payload().get_candidate_id()

        print(f"{Fore.YELLOW}DONE{Style.RESET_ALL}")

    def _verify_signature(self, vote: VoteDTO, dsa_public_key: dsa.DSAPublicKey) -> bool:
        print(f"{Fore.YELLOW}SIGNATURE_VALIDATION{Style.RESET_ALL}: ", end = '')

        try:
            dsa_public_key.verify(vote.get_signature(), hash(vote.get_vote_payload().get_candidate_id()).to_bytes(length = 32), hashes.SHA256())
        except Exception:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} (Invalid signature)")
            return False

        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL} | ", end = '')
        return True

    def _validate_vote(self, vote: VoteDTO) -> bool:
        print(f"{Fore.YELLOW}VOTE_VALIDATION{Style.RESET_ALL}: ", end = '')

        if vote.get_voter_registration_id() not in self._voters:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} (Invalid voter)")
            return False

        if vote.get_vote_payload().get_candidate_id() not in self._results.keys():
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} (Invalid candidate)")
            return False

        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL} | ", end = '')
        return True

    def print_results(self) -> None:
        print(f"\n{Fore.YELLOW}RESULTS{Style.RESET_ALL}")

        print()

        sorted_results = sorted(self._results.items(), key = lambda item: item[1], reverse = True)
        max_votes = sorted_results[0][1]

        for key, value in self._public_results.items():
            print(f"{key}: {value}")

        print()

        for candidate, count in sorted_results:
            print(f"Candidate #{candidate}: {count} vote(s)")

        winners = [candidate for candidate, count in sorted_results if count == max_votes]

        if len(winners) == 1:
            print(f"\nWINNER is candidate #{winners[0]} with {max_votes} vote(s).")
        else:
            print("\nDRAW between ", end='')

            for candidate in winners:
                print(f"candidate #{candidate} with {max_votes} vote(s) ", end = '')