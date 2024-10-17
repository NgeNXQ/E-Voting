import random
from enum import Enum
import rsa
from colorama import Fore, Style
from controllers import VoterController
from models import Candidate, VotePayload, VotePool, VotePoolsCluster, SignedVote

class VoterStatus(Enum):
    IDLE = 0
    VOTED = 1
    ECHOED = 2
    VERIFIED = 3

class CommissionController:

    VOTE_POOLS_CLUSTER_SIZE = 10
    VOTE_POOLS_CLUSTER_PEEK_SIZE = 9

    def __init__(self, candidates: list[Candidate], voters: list[VoterController]) -> None:
        self._public_results = {}
        self._candidates = candidates
        (self._public_key, self._private_key) = rsa.newkeys(nbits = 512)
        self._results = {candidate.get_id(): 0 for candidate in candidates}
        self._voters_registry = {voter.get_id(): VoterStatus.IDLE for voter in voters}

    def get_public_key(self) -> bytes:
        return self._public_key

    def process(self, voter: VoterController, vote_pools_cluster: VotePoolsCluster) -> list[SignedVote]:
        if voter is None:
            raise ValueError("voter cannot be None")

        if vote_pools_cluster is None:
            raise ValueError("vote_pools_cluster cannot be None")

        print(f"{Fore.YELLOW}PROCESSING{Style.RESET_ALL} #{voter.get_id()} | ", end = '')

        if not self._verify_voter(voter):
            return None

        is_valid_cluster, out_vote_pool = self._validate_vote_pools_cluster(vote_pools_cluster)

        if not is_valid_cluster:
            return None

        self._voters_registry[voter.get_id()] = VoterStatus.ECHOED
        signed_vote_pool = self._sign_vote_pool(out_vote_pool)
        return signed_vote_pool

    def _verify_voter(self, voter: VoterController) -> bool:
        if voter is None:
            raise ValueError("voter cannot be None")

        print("1st VERIFICATION: ", end = '')

        if voter.get_id() not in self._voters_registry:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Unknown voter")
            return False

        if not voter.get_is_able_to_vote():
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Voter is not able to vote")
            return False

        if self._voters_registry[voter.get_id()] == VoterStatus.VOTED:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Voter has already voted")
            return False

        if self._voters_registry[voter.get_id()] == VoterStatus.ECHOED:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Voter has already been verified")
            return False

        self._voters_registry[voter.get_id()] = VoterStatus.VERIFIED
        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL} | ", end = '')
        return True

    def _validate_vote_pools_cluster(self, vote_pools_cluster: VotePoolsCluster) -> tuple[bool, VotePool]:
        if vote_pools_cluster is None:
            raise ValueError("vote_records_pools_cluste cannot be None")

        print("CLUSTER VALIDATION: ", end = '')

        if vote_pools_cluster.get_size() != CommissionController.VOTE_POOLS_CLUSTER_SIZE:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Invalid cluster size")
            return False, None

        pool:VotePool = None
        pools: list[VotePool] = [vote_pools_cluster.get_vote_pool(i) for i in range(vote_pools_cluster.get_size())]

        while len(pools) != 1:
            while True:
                pool = vote_pools_cluster.get_vote_pool(random.randint(0, CommissionController.VOTE_POOLS_CLUSTER_PEEK_SIZE))

                if pool not in pools:
                    continue
                else:
                    pools.remove(pool)
                    break

            if not self._validate_vote_pool(pool):
                return False, None

        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL} | ", end = '')
        return True, pools[0]

    def _validate_vote_pool(self, vote_pool: VotePool) -> bool:
        if vote_pool is None:
            raise ValueError("vote_records_pool cannot be None")

        if vote_pool.get_size() != len(self._candidates):
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Invalid pool's size")
            return False

        for i in range(0, len(self._candidates)):
            vote_pool.get_vote_payload(i).unmask()

            if vote_pool.get_vote_payload(i).get_candidate_id() != (i + 1):
                print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Invalid pool's content")
                return False

            if not self._validate_vote_payload(vote_pool.get_vote_payload(i)):
                return False

        return True

    def _validate_vote_payload(self, vote_payload: VotePayload) -> bool:
        if vote_payload.get_uuid() not in self._voters_registry:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Unknown voter")
            return False

        if self._voters_registry[vote_payload.get_uuid()] in (VoterStatus.VOTED, VoterStatus.IDLE):
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Invalid voter")
            return False

        return True

    def _sign_vote_pool(self, vote_pool: VotePool) -> VotePool:
        if vote_pool is None:
            raise ValueError("vote_pool cannot be None")

        signed_votes: list[SignedVote] = []

        for i in range(0, len(self._candidates)):
            vote_payload = vote_pool.get_vote_payload(i)
            signature = rsa.sign(f"{hash(vote_payload)}".encode(), self._private_key, "SHA-256")
            signed_votes.append(SignedVote(vote_payload, signature))

        return VotePool(signed_votes)

    def register_final_vote(self, signed_vote: SignedVote) -> None:
        if signed_vote is None:
            return

        print("2nd VERIFICATION: ", end = '')

        if not signed_vote.get_is_encrypted():
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Signature verification failed")
            return

        try:
            signed_vote.decrypt(self._private_key)
        except rsa.DecryptionError:
            print(f"{Fore.RED}FAILURE{Style.RESET_ALL} | Signature verification failed")
            return

        if not self._validate_vote_payload(signed_vote.get_vote_payload()):
            return

        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL} | ", end = '')

        self._results[signed_vote.get_vote_payload().get_candidate_id()] += 1
        self._voters_registry[signed_vote.get_vote_payload().get_uuid()] = VoterStatus.VOTED
        self._public_results[signed_vote.get_vote_payload().get_uuid()] = signed_vote.get_vote_payload().get_candidate_id()

        print(f"{Fore.YELLOW}DONE{Style.RESET_ALL}")

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