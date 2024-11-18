from elgamal import elgamal

class AuthToken:

    def __init__(self, voter_id: int, elgamal_public_key: elgamal.PublicKey) -> 'AuthToken':
        self._voter_id = voter_id
        self._elgamal_public_key = elgamal_public_key

    def get_voter_id(self) -> int:
        return self._voter_id

    def get_elgamal_public_key(self) -> elgamal.PublicKey:
        return self._elgamal_public_key