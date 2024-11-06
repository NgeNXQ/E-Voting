import random
import string
import rsa
from elgamal import elgamal
from errors import VoteProtocolError
from models import Candidate, VoteOnion

class VoterController:

    _BITS_IN_BYTE_COUNT: int = 8
    _OFFSET_RSA_SIZE_BYTES: int = 11
    _BUFFER_NOISE_SIZE_BYTES: int = 5
    _ELGAMAL_SIGNATURE_PAYLOAD_LENGTH = 32
    _BUFFER_NOISE_CONTENT: str = string.ascii_letters + string.digits
    _OFFSET_RSA_SIZE_BITS: int = _OFFSET_RSA_SIZE_BYTES * _BITS_IN_BYTE_COUNT
    _BUFFER_NOISE_SIZE_BITS: int = _BUFFER_NOISE_SIZE_BYTES * _BITS_IN_BYTE_COUNT
    _BUFFER_PAYLOAD_SIZE_BITS = len(Candidate._next_id.to_bytes()) * _BITS_IN_BYTE_COUNT

    _next_id: int = 0
    _voters: list['VoterController'] = list()
    _shared_rsa_internal_public_keys: list[rsa.PublicKey] = list()
    _shared_rsa_external_public_keys: list[rsa.PublicKey] = list()

    def __init__(self) -> 'VoterController':
        VoterController._next_id += 1
        self._id = VoterController._next_id
        self._dumps: list[bytes] = list()
        VoterController._voters.append(self)
        self._elgamal_private_key, self._elgamal_public_key = elgamal.Elgamal.newkeys(VoterController._ELGAMAL_SIGNATURE_PAYLOAD_LENGTH)

    def get_id(self) -> int:
        return self._custom_id

    def get_rsa_public_key(self) -> rsa.PublicKey:
        return self._rsa_public_key

    def get_elgamal_public_key(self) -> elgamal.PublicKey:
        return self._elgamal_public_key

    def generate_rsa_keys_pairs(self) -> None:
        reversed_id: int = VoterController._next_id - self._id + 1

        internal_keys_size_bits = VoterController._BUFFER_PAYLOAD_SIZE_BITS + VoterController._BUFFER_NOISE_SIZE_BITS + (VoterController._OFFSET_RSA_SIZE_BITS * reversed_id)
        (self._rsa_internal_public_key, self._rsa_internal_private_key) = rsa.newkeys(nbits = internal_keys_size_bits)
        VoterController._shared_rsa_internal_public_keys.insert(0, self._rsa_internal_public_key)

        largest_keys_size_bits = VoterController._BUFFER_PAYLOAD_SIZE_BITS + VoterController._BUFFER_NOISE_SIZE_BITS + (VoterController._OFFSET_RSA_SIZE_BITS * VoterController._next_id)
        external_keys_size_bits = largest_keys_size_bits + (VoterController._BUFFER_NOISE_SIZE_BITS * reversed_id) + (VoterController._OFFSET_RSA_SIZE_BITS * reversed_id)
        (self._rsa_external_public_key, self._rsa_external_private_key) = rsa.newkeys(nbits = external_keys_size_bits)
        VoterController._shared_rsa_external_public_keys.insert(0, self._rsa_external_public_key)

    def vote(self, candidate: Candidate) -> VoteOnion:
        if candidate is None:
            raise ValueError("candidate cannot be None")

        vote_onion = VoteOnion(candidate.get_id(), self._generate_random_buffer_payload())
        self._dumps.append(vote_onion.get_buffer())

        for rsa_public_key in VoterController._shared_rsa_internal_public_keys:
            vote_onion.push_layer(rsa_public_key)
            self._dumps.append(vote_onion.get_buffer())

        for rsa_public_key in VoterController._shared_rsa_external_public_keys:
            buffer_noise = self._generate_random_buffer_payload()
            vote_onion.push_layer(rsa_public_key, buffer_noise)
            self._dumps.append(vote_onion.get_buffer())

        return vote_onion

    def _generate_random_buffer_payload(self) -> bytes:
        return (''.join(random.choice(VoterController._BUFFER_NOISE_CONTENT) for _ in range(VoterController._BUFFER_NOISE_SIZE_BYTES))).encode()

    def decrypt_external_part(self, votes: list[VoteOnion]) -> None:
        for vote in votes:
            vote.pop_layer(self._rsa_external_private_key)

        if not self._validate_votes(votes):
            raise VoteProtocolError("Fraud attempt has been detected.")

        random.shuffle(votes)

    def decrypt_internal_part(self, votes: list[VoteOnion]) -> None:
        for vote in votes:
            vote.pop_layer(self._rsa_internal_private_key)
            vote.set_signature(elgamal.Elgamal.sign(vote.get_buffer()[:VoterController._ELGAMAL_SIGNATURE_PAYLOAD_LENGTH], self._elgamal_private_key))

        if not self._validate_votes(votes):
            raise VoteProtocolError("Fraud attempt has been detected.")

        other_voters = [voter for voter in VoterController._voters if voter != self]

        for voter in other_voters:
            voter.verify_signatures(votes, self._elgamal_public_key)

    def _validate_votes(self, votes: list[VoteOnion]) -> bool:
        if votes is None:
            raise ValueError("votes cannot be None")

        is_own_vote_inside: bool = False
        self._dumps = self._dumps[:random.choice(votes).get_layers_count()]

        if len(votes) != VoterController._next_id:
            return False

        for vote in votes:
            if self._dumps[-1] == vote.get_buffer():
                is_own_vote_inside = True

        return is_own_vote_inside

    def verify_signatures(self, votes: list[VoteOnion], elgamal_public_key: elgamal.PublicKey) -> None:
        if votes is None:
            raise ValueError("votes cannot be None")

        if elgamal_public_key is None:
            raise ValueError("elgamal_public_key cannot be None")

        for vote in votes:
            try:
                elgamal.Elgamal.verify(vote.get_signature(), elgamal_public_key)
            except:
                raise VoteProtocolError("Fraud attempt has been detected.")

        if not self._validate_votes(votes):
            raise VoteProtocolError("Fraud attempt has been detected.")