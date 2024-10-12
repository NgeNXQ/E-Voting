import colorama
from models import Candidate, VotePoolsCluster
from controllers import VoterController, VoterDebugMode, CommissionController

if __name__ == "__main__":

    colorama.init(autoreset = True)

    candidate_1 = Candidate(1)
    candidate_2 = Candidate(2)

    voter_1 = VoterController(True)
    voter_2 = VoterController(True)
    voter_3 = VoterController(True, VoterDebugMode.MISSING_SIGNATURE)
    voter_4 = VoterController(True)
    voter_5 = VoterController(True, VoterDebugMode.VOTE_RECORD_SUBSTITUTION)
    voter_6 = VoterController(True)
    voter_7 = VoterController(True)
    voter_8 = VoterController(True)
    voter_9 = VoterController(False)

    candidates = [candidate_1, candidate_2]
    voters = [voter_1, voter_2, voter_3, voter_4, voter_5, voter_6, voter_7, voter_8, voter_9]

    commission = CommissionController(candidates, voters)

    vote_pools_cluster_1 = voter_1.create_vote_pools_cluster(candidates, CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    sgined_votes_1 = commission.process(voter_1, vote_pools_cluster_1)

    if sgined_votes_1 is not None:
        signed_vote_1 = voter_1.vote(candidate_1, sgined_votes_1)
        commission.register_final_vote(signed_vote_1)

    # commission.process_voter(voter_1, candidate_1)
    # commission.process_voter(voter_2, candidate_1)
    # commission.process_voter(voter_3, candidate_1)
    # commission.process_voter(voter_4, candidate_1)
    # commission.process_voter(voter_5, candidate_1)
    # commission.process_voter(voter_6, candidate_2)
    # commission.process_voter(voter_7, candidate_2)
    # commission.process_voter(voter_8, candidate_2)
    # commission.process_voter(voter_9, candidate_2)

    # voter_0 = VoterController(0, True)
    # print(f"voter #{voter_0.get_id()} ", end = '')

    # vote_record_0 = voter_0.vote(candidate_1)
    # signed_vote_record_0 = voter_0.sign(vote_record_0)
    # signed_vote_record_0.toggle_gamma_encryption(commission.get_gamma_key())
    # commission.register_vote(signed_vote_record_0, voter_0.get_public_key())

    # commission.print_results()