import uuid
from elgamal import elgamal
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from utilities import VoteCipherUtility
from models import Candidate, VotePayload, VoteDTO

class VoterController:

    def __init__(self, registration_id: int) -> None:
        self._custom_id = uuid.uuid4().int
        self._registration_id = registration_id
        self._dsa_private_key = dsa.generate_private_key(key_size = 1024)
        self._dsa_public_key = self._dsa_private_key.public_key()
        self._elgamal_public_key, self._elgamal_private_key = elgamal.Elgamal.newkeys(10)

    def get_custom_id(self) -> int:
        return self._custom_id

    def get_registration_id(self) -> int:
        return self._registration_id

    def get_dsa_public_key(self) -> dsa.DSAPublicKey:
        return self._dsa_public_key

    def get_elgamal_private_key(self) -> elgamal.PrivateKey:
        return self._elgamal_private_key

    def vote(self, candidate: Candidate) -> VoteDTO:
        vote_payload = VotePayload(candidate.get_id())
        signature = self._dsa_private_key.sign(hash(vote_payload.get_candidate_id()).to_bytes(length = 32), hashes.SHA256())
        vote_dto = VoteDTO(self._custom_id, self._registration_id, vote_payload, signature)
        encrypted_vote_dto = VoteCipherUtility.encrypt(vote_dto, self._elgamal_public_key)
        return encrypted_vote_dto