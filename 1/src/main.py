from models import Candidate
from controllers import VoterController, VoterDebugMode, CommissionController

if __name__ == "__main__":
    candidate_1 = Candidate(1)
    candidate_2 = Candidate(2)
    commission = CommissionController([candidate_1, candidate_2])

    voter_1 = VoterController(1, True)
    voter_2 = VoterController(2, True)
    voter_3 = VoterController(3, True, VoterDebugMode.MISSING_SIGNATURE)
    voter_4 = VoterController(4, True)
    voter_5 = VoterController(5, True, VoterDebugMode.VOTE_RECORD_SUBSTITUTION)
    voter_6 = VoterController(6, True)
    voter_7 = VoterController(7, True, VoterDebugMode.MISSING_GAMMA_ENCRYPTION)
    voter_8 = VoterController(8, True)
    voter_9 = VoterController(9, False)

    commission.process_voter(voter_1, candidate_1)
    commission.process_voter(voter_1, candidate_1)
    commission.process_voter(voter_2, candidate_1)
    commission.process_voter(voter_3, candidate_1)
    commission.process_voter(voter_4, candidate_1)
    commission.process_voter(voter_5, candidate_1)
    commission.process_voter(voter_6, candidate_2)
    commission.process_voter(voter_7, candidate_2)
    commission.process_voter(voter_8, candidate_2)
    commission.process_voter(voter_9, candidate_2)

    voter_0 = VoterController(0, True)
    print(f"voter #{voter_0.get_id()} ", end = '')

    vote_record_0 = voter_0.vote(candidate_1)
    signed_vote_record_0 = voter_0.sign(vote_record_0)
    signed_vote_record_0.toggle_gamma_encryption(commission.get_gamma_key())
    commission.register_vote(signed_vote_record_0, voter_0.get_public_key())

    commission.print_results()