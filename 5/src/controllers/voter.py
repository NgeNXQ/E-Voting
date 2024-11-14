import random
import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from helpers.divisors import get_factors_pairs
from models import Candidate, PartialVote, SignedPartialVote

class VoterController:

    def __init__(self, id: int) -> 'VoterController':
        self._id = id
        self._dsa_private_key: dsa.DSAPrivateKey = dsa.generate_private_key(key_size = 1024)
        self._dsa_public_key: dsa.DSAPublicKey = self._dsa_private_key.public_key()

    def get_id(self) -> int:
        return self._id

    def get_dsa_public_key(self) -> dsa.DSAPublicKey:
        return self._dsa_public_key

    def vote(self, candidate: Candidate, rsa_public_key: rsa.PublicKey) -> tuple[SignedPartialVote, SignedPartialVote]:
        if candidate is None:
            raise ValueError("candidate cannot be None.")

        if rsa_public_key is None:
            raise ValueError("rsa_public_key cannot be None.")

        factors_pairs: list[tuple[int, int]] = get_factors_pairs(candidate.get_id(), is_prime_factor_allowed = False)
        candidate_id_factors_pair: tuple[int, int] = random.choice(factors_pairs)

        vote_first = PartialVote(self._id, candidate_id_factors_pair[0])
        vote_second = PartialVote(self._id, candidate_id_factors_pair[1])

        vote_first.encrypt(rsa_public_key)
        vote_second.encrypt(rsa_public_key)

        signed_vote_first = SignedPartialVote(vote_first, self._dsa_private_key.sign(hash(vote_first.get_voter_id()).to_bytes(length = 32), hashes.SHA256()))
        signed_vote_second = SignedPartialVote(vote_second, self._dsa_private_key.sign(hash(vote_second.get_voter_id()).to_bytes(length = 32), hashes.SHA256()))

        return signed_vote_first, signed_vote_second
