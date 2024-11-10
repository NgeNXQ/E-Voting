import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from models import Candidate, User, SignedPartialVote
from controllers import VoterController, CentralCommissionController, ElectionCommissionController

if __name__ == "__main__":
    central_commission = CentralCommissionController()
    election_commissions: list[ElectionCommissionController] = central_commission.init_election_commissions(2)

    print("\nREGISTRATION\n")

    user_0 = User(False, True)
    user_1 = User(False, True)

    candidate_1: Candidate = central_commission.register_candidate(user_0)
    candidate_2: Candidate = central_commission.register_candidate(user_1)

    user_2 = User(True, False)
    user_3 = User(True, False)
    user_4 = User(True, False)
    user_5 = User(True, False)
    user_6 = User(False, False)

    voter_1: VoterController = central_commission.register_voter(user_2)
    voter_2: VoterController = central_commission.register_voter(user_3)
    voter_3: VoterController = central_commission.register_voter(user_4)
    voter_4: VoterController = central_commission.register_voter(user_5)
    # Second registration
    voter_0: VoterController = central_commission.register_voter(user_5)
    # Not eligible for voting
    voter_0: VoterController = central_commission.register_voter(user_6)

    print("\nVOTING\n")

    # OK
    voter_1.vote(candidate_1, central_commission.get_rsa_public_key(), central_commission.get_dsa_private_key())

    # Second attempt
    voter_1.vote(candidate_1, central_commission.get_rsa_public_key(), central_commission.get_dsa_private_key())

    # Invalid encryption
    rsa_public_key, _ = rsa.newkeys(128)
    voter_2.vote(candidate_2, rsa_public_key, central_commission.get_dsa_private_key())

    # Invalid signature
    dsa_private_key: dsa.DSAPrivateKey = dsa.generate_private_key(key_size = 1024)
    dsa_public_key: dsa.DSAPublicKey = dsa_private_key.public_key()
    dsa_private_key.sign(hash(1).to_bytes(length = 32), hashes.SHA256())
    voter_3.vote(candidate_2, central_commission.get_rsa_public_key(), dsa_private_key)

    # Unknown voter
    unknown_voter = VoterController(0, election_commissions)
    unknown_voter.vote(candidate_1, central_commission.get_rsa_public_key(), central_commission.get_dsa_private_key())

    # OK
    voter_3.vote(candidate_2, central_commission.get_rsa_public_key(), central_commission.get_dsa_private_key())

    # OK
    voter_4.vote(candidate_1, central_commission.get_rsa_public_key(), central_commission.get_dsa_private_key())
