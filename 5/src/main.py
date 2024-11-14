import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from models import Candidate, User
from controllers import VoterController, CentralCommissionController

if __name__ == "__main__":
    central_commission = CentralCommissionController()
    election_commission_0, election_commission_1 = central_commission.init_election_commissions(2)

    print("\nREGISTRATION\n")

    user_0 = User(False, True)
    user_1 = User(False, True)

    candidate_1: Candidate = central_commission.register_candidate(user_0)
    candidate_2: Candidate = central_commission.register_candidate(user_1)

    user_2 = User(True, False)
    user_3 = User(True, False)
    user_4 = User(True, False)
    user_5 = User(True, False)
    user_6 = User(True, False)
    user_7 = User(True, False)
    user_8 = User(False, False)

    voter_1: VoterController = central_commission.register_voter(user_2)
    voter_2: VoterController = central_commission.register_voter(user_3)
    voter_3: VoterController = central_commission.register_voter(user_4)
    voter_4: VoterController = central_commission.register_voter(user_5)
    voter_5: VoterController = central_commission.register_voter(user_6)
    voter_6: VoterController = central_commission.register_voter(user_7)

    # Second registration
    voter_test_1: VoterController = central_commission.register_voter(user_7)
    # Not eligible for voting
    voter_test_2: VoterController = central_commission.register_voter(user_8)

    print("\nVOTING\n")

    # OK
    votes_1 = voter_1.vote(candidate_1, central_commission.get_rsa_public_key())
    election_commission_0.register_vote(votes_1[0], voter_1.get_dsa_public_key())
    election_commission_1.register_vote(votes_1[1], voter_1.get_dsa_public_key())

    # Second attempt
    votes_1 = voter_1.vote(candidate_1, central_commission.get_rsa_public_key())
    election_commission_0.register_vote(votes_1[0], voter_1.get_dsa_public_key())
    election_commission_1.register_vote(votes_1[1], voter_1.get_dsa_public_key())

    # Invalid encryption
    rsa_public_key, _ = rsa.newkeys(128)
    votes_2 = voter_2.vote(candidate_2, rsa_public_key)
    election_commission_0.register_vote(votes_2[0], voter_2.get_dsa_public_key())
    election_commission_1.register_vote(votes_2[1], voter_2.get_dsa_public_key())

    # Invalid signature
    dsa_private_key: dsa.DSAPrivateKey = dsa.generate_private_key(key_size = 1024)
    dsa_public_key: dsa.DSAPublicKey = dsa_private_key.public_key()
    dsa_private_key.sign(hash(1).to_bytes(length = 32), hashes.SHA256())
    votes_3 = voter_3.vote(candidate_2, central_commission.get_rsa_public_key())
    election_commission_0.register_vote(votes_3[0], dsa_public_key)
    election_commission_1.register_vote(votes_3[1], dsa_public_key)

    # Unknown voter
    unknown_voter = VoterController(0)
    unknown_votes = unknown_voter.vote(candidate_1, central_commission.get_rsa_public_key())
    election_commission_0.register_vote(unknown_votes[0], unknown_voter.get_dsa_public_key())
    election_commission_1.register_vote(unknown_votes[1], unknown_voter.get_dsa_public_key())

    # Invalid procedure # 1
    votes_4 = voter_4.vote(candidate_2, central_commission.get_rsa_public_key())
    election_commission_0.register_vote(votes_4[0], voter_4.get_dsa_public_key())

    # OK
    votes_5 = voter_5.vote(candidate_2, central_commission.get_rsa_public_key())
    election_commission_0.register_vote(votes_5[0], voter_5.get_dsa_public_key())
    election_commission_1.register_vote(votes_5[1], voter_5.get_dsa_public_key())

    # OK
    votes_6 = voter_6.vote(candidate_1, central_commission.get_rsa_public_key())
    election_commission_0.register_vote(votes_6[0], voter_6.get_dsa_public_key())
    election_commission_1.register_vote(votes_6[1], voter_6.get_dsa_public_key())

    election_commission_0.print_results()
    election_commission_1.print_results()

    central_commission.finish_election([election_commission_0.get_votes() + election_commission_1.get_votes()])
    central_commission.print_results()
