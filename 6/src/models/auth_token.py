from uuid import UUID
from elgamal import elgamal
from utilities import bbs

class AuthToken:

    def __init__(self, voter_id: UUID, elgamal_public_key: elgamal.PublicKey, bbs_keys: bbs.KeysPair) -> 'AuthToken':
        self._bbs_keys = bbs_keys
        self._voter_id = voter_id
        self._elgamal_public_key = elgamal_public_key

    def get_voter_id(self) -> UUID:
        return self._voter_id

    def get_bbs_keys(self) -> bbs.KeysPair:
        return self._bbs_keys

    def get_elgamal_public_key(self) -> elgamal.PublicKey:
        return self._elgamal_public_key
