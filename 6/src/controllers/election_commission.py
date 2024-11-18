from elgamal import elgamal
from models import Vote, AuthToken

class ElectionCommissionController:

    def __init__(self, voters_ids: list[int]) -> 'ElectionCommissionController':
        # self._voters: dict[int, ]
        self._elgamal_public_key, self._elgamal_private_key = elgamal.Elgamal.newkeys(16)
        # self._voters_tokens: dict[int, ]
        self._voters_tokens: dict[int, AuthToken] = dict()

        for voter_id in voters_ids:
            # generate bb's
            # self._voters: dict[int, ]
            self._voters_tokens[voter_id] = AuthToken(voter_id)
            pass

        # voter_custom_id = elgamal.Elgamal.encrypt(vote.get_voter_custom_id().to_bytes(length = 32), public_key)

    def get_auth_token(self, voter_id) -> AuthToken:
        if voter_id is not self._voters_tokens.keys():
            raise ValueError("Invalid voter_id value")

        return self._voters_tokens[voter_id]

    def register_vote(self, vote: Vote)