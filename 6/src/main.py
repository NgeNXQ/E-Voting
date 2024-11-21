from services import VotingHandlerServie
from models import User, Candidate, Credentials
from controllers import RegistrationCommissionController, ElectionCommissionController

if __name__ == '__main__':
    candidate_1 = Candidate()
    candidate_2 = Candidate()

    user_1 = User(True)
    user_2 = User(True)
    user_3 = User(True)
    user_4 = User(False)

    # setup
    registration_commission = RegistrationCommissionController(User.get_users_total_count())
    election_commission = ElectionCommissionController(registration_commission.get_voters_ids(), [candidate_1, candidate_2])
    registration_commission.setup_voters_tokens(election_commission.get_voters_tokens())
    voting_handler = VotingHandlerServie(registration_commission.get_voters(), election_commission)

    print("\n|REGISTRATION|\n")

    # OK
    credentials_1: Credentials = registration_commission.register_user(user_1)

    # 2nd reg attempt
    _ = registration_commission.register_user(user_1)

    # OK
    credentials_2: Credentials = registration_commission.register_user(user_2)

    # OK
    credentials_3: Credentials = registration_commission.register_user(user_3)

    # Not eligible voter
    _ = registration_commission.register_user(user_4)

    print("\n|VOTING|\n")

    # OK
    voting_handler.login(credentials_1.get_username(), credentials_1.get_password())
    voting_handler.vote(candidate_1, credentials_1.get_auth_token())

    print('\n', end = '')

   # 2nd voting attempt
    voting_handler.login(credentials_1.get_username(), credentials_1.get_password())
    voting_handler.vote(candidate_1, credentials_1.get_auth_token())

    print('\n', end = '')

   # Invalid username
    voting_handler.login("TEST_USERNAME", credentials_2.get_password())
    voting_handler.vote(candidate_1, credentials_2.get_auth_token())

    print('\n', end = '')

   # Invalid password
    voting_handler.login(credentials_2.get_username(), "TEST_PASSWORD")
    voting_handler.vote(candidate_1, credentials_2.get_auth_token())

    print('\n', end = '')

    # OK
    voting_handler.login(credentials_2.get_username(), credentials_2.get_password())
    voting_handler.vote(candidate_1, credentials_2.get_auth_token())

    print('\n', end = '')

    # Invalid candidate
    voting_handler.login(credentials_3.get_username(), credentials_3.get_password())
    voting_handler.vote(Candidate(), credentials_3.get_auth_token())

    print('\n', end = '')

    # Invalid vote payload (structure)

    from models import Vote
    from utilities import bbs
    from elgamal import elgamal

    encrypted_candidate_id: int = bbs.encrypt(candidate_1.get_id(), credentials_3.get_auth_token().get_bbs_keys().get_seed(), credentials_3.get_auth_token().get_bbs_keys().get_public_key())
    payload: bytes = encrypted_candidate_id.to_bytes() + Vote.DELIMITER_BYTE + credentials_3.get_auth_token().get_bbs_keys().get_seed().to_bytes()
    encrypted_payload: elgamal.CipherText = elgamal.Elgamal.encrypt(payload, credentials_3.get_auth_token().get_elgamal_public_key())

    election_commission.register_vote(Vote(encrypted_payload), credentials_3.get_auth_token().get_elgamal_public_key())

    print('\n', end = '')

    # OK
    voting_handler.login(credentials_3.get_username(), credentials_3.get_password())
    voting_handler.vote(candidate_2, credentials_3.get_auth_token())

    print('\n', end = '')

    # Unknown voter

    elgamal_public_key, elgamal_private_key = elgamal.Elgamal.newkeys(32)
    election_commission.register_vote(Vote(encrypted_payload), elgamal_public_key)

    election_commission.print_results()
