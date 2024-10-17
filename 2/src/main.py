import colorama
from models import Candidate, VotePayload, SignedVote
from controllers import VoterController, CommissionController

if __name__ == "__main__":

    colorama.init(autoreset = True)

    candidate_1 = Candidate(1)
    candidate_2 = Candidate(2)

    voter_1 = VoterController(True)
    voter_2 = VoterController(False)
    voter_3 = VoterController(True)
    voter_4 = VoterController(True)
    voter_5 = VoterController(True)
    voter_6 = VoterController(True)
    voter_7 = VoterController(True)

    candidates = [candidate_1, candidate_2]
    voters = [voter_1, voter_2, voter_3, voter_4, voter_5, voter_6, voter_7]

    commission = CommissionController(candidates, voters)

    # voter0 Unknown voter
    print("voter #0 ", end = '')
    voter_0 = VoterController(True)
    vote_pools_cluster = voter_0.create_vote_pools_cluster(candidates, CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    signed_vote_pool = commission.process(voter_0, vote_pools_cluster)
    final_vote = voter_0.process_commission_response(signed_vote_pool, candidate_1, commission.get_public_key())
    commission.register_final_vote(final_vote)

    # voter1 OK
    print("voter #1 ", end = '')
    vote_pools_cluster = voter_1.create_vote_pools_cluster(candidates, CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    signed_vote_pool = commission.process(voter_1, vote_pools_cluster)
    final_vote = voter_1.process_commission_response(signed_vote_pool, candidate_1, commission.get_public_key())
    commission.register_final_vote(final_vote)

    # voter2 Not able to vote
    print("voter #2 ", end = '')
    vote_pools_cluster = voter_2.create_vote_pools_cluster(candidates, CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    signed_vote_pool = commission.process(voter_2, vote_pools_cluster)
    final_vote = voter_2.process_commission_response(signed_vote_pool, candidate_1, commission.get_public_key())
    commission.register_final_vote(final_vote)

    # voter3 Invalid cluster (empty)
    print("voter #3 ", end = '')
    vote_pools_cluster = voter_3.create_vote_pools_cluster([], CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    signed_vote_pool = commission.process(voter_3, vote_pools_cluster)
    final_vote = voter_3.process_commission_response(signed_vote_pool, candidate_1, commission.get_public_key())
    commission.register_final_vote(final_vote)

    # voter3 Invalid cluster (wrong payload)
    print("voter #3 ", end = '')
    vote_pools_cluster = voter_3.create_vote_pools_cluster([candidate_2, candidate_1], CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    signed_vote_pool = commission.process(voter_3, vote_pools_cluster)
    final_vote = voter_3.process_commission_response(signed_vote_pool, candidate_1, commission.get_public_key())
    commission.register_final_vote(final_vote)

    # voter3 Invalid cluster (wrong payload from voter_1)
    print("voter #3 ", end = '')
    vote_pools_cluster = voter_1.create_vote_pools_cluster(candidates, CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    signed_vote_pool = commission.process(voter_3, vote_pools_cluster)
    final_vote = voter_3.process_commission_response(signed_vote_pool, candidate_1, commission.get_public_key())
    commission.register_final_vote(final_vote)

    # voter4 OK
    print("voter #4 ", end = '')
    vote_pools_cluster = voter_4.create_vote_pools_cluster(candidates, CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    signed_vote_pool = commission.process(voter_4, vote_pools_cluster)
    final_vote = voter_4.process_commission_response(signed_vote_pool, candidate_2, commission.get_public_key())
    commission.register_final_vote(final_vote)

    # voter4 Second attempt
    print("voter #4 ", end = '')
    vote_pools_cluster = voter_4.create_vote_pools_cluster(candidates, CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    signed_vote_pool = commission.process(voter_4, vote_pools_cluster)
    final_vote = voter_4.process_commission_response(signed_vote_pool, candidate_1, commission.get_public_key())
    commission.register_final_vote(final_vote)

    # voter5 Without verification
    print("voter #5 ", end = '')
    fake_vote = SignedVote(VotePayload(candidate_1.get_id().to_bytes(), voter_5.get_id(), voter_5.get_mask_key()), commission.get_public_key())
    commission.register_final_vote(fake_vote)

    # voter6 Invalid cluster
    print("voter #6 ", end = '')
    vote_pools_cluster = voter_6.create_vote_pools_cluster(candidates, 1)
    signed_vote_pool = commission.process(voter_6, vote_pools_cluster)
    final_vote = voter_6.process_commission_response(signed_vote_pool, candidate_1, commission.get_public_key())
    commission.register_final_vote(final_vote)

    # voter9 OK
    print("voter #9 ", end = '')
    vote_pools_cluster = voter_7.create_vote_pools_cluster(candidates, CommissionController.VOTE_POOLS_CLUSTER_SIZE)
    signed_vote_pool = commission.process(voter_7, vote_pools_cluster)
    final_vote = voter_7.process_commission_response(signed_vote_pool, candidate_1, commission.get_public_key())
    commission.register_final_vote(final_vote)

    commission.print_results()