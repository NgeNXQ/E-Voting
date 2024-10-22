import colorama
from models import Candidate, User
from controllers import VoterController, ElectionCommissionController, RegistrationBureauController

if __name__ == "__main__":
    colorama.init(autoreset = True)

    candidate_1 = Candidate()
    candidate_2 = Candidate()

    user_0 = User(False)
    user_1 = User(True)
    user_2 = User(True)
    user_3 = User(True)
    user_4 = User(True)

    registration_bureau = RegistrationBureauController()

    voter_0 = registration_bureau.register(user_0)
    voter_1 = registration_bureau.register(user_1)
    voter_2 = registration_bureau.register(user_2)
    voter_3 = registration_bureau.register(user_3)
    voter_4 = registration_bureau.register(user_4)

    election_commission = ElectionCommissionController([candidate_1, candidate_2], registration_bureau.get_voters())

    # Without registration
    voter_0 = VoterController(101010)
    vote_0 = voter_0.vote(candidate_1)
    election_commission.register_vote(vote_0, voter_0.get_dsa_public_key(), voter_0.get_elgamal_private_key())

    # OK
    vote_1 = voter_1.vote(candidate_1)
    election_commission.register_vote(vote_1, voter_1.get_dsa_public_key(), voter_1.get_elgamal_private_key())

    # Second attempt
    vote_1 = voter_1.vote(candidate_1)
    election_commission.register_vote(vote_1, voter_1.get_dsa_public_key(), voter_1.get_elgamal_private_key())

    # OK
    vote_2 = voter_2.vote(candidate_1)
    election_commission.register_vote(vote_2, voter_2.get_dsa_public_key(), voter_2.get_elgamal_private_key())

    # Invalid signature
    vote_3 = voter_3.vote(candidate_1)
    election_commission.register_vote(vote_3, voter_2.get_dsa_public_key(), voter_3.get_elgamal_private_key())

    # Invalid candidate
    vote_4 = voter_4.vote(Candidate())
    election_commission.register_vote(vote_4, voter_4.get_dsa_public_key(), voter_4.get_elgamal_private_key())

    election_commission.print_results()