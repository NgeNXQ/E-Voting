from elgamal import elgamal     # xdd
from models import VoteDTO

class VoteCipherUtility:

    @staticmethod
    def encrypt(vote: VoteDTO, public_key: elgamal.PublicKey) -> VoteDTO:
        if vote is None:
            raise ValueError("vote cannot be None")

        if public_key is None:
            raise ValueError("public_key cannot be None")

        voter_custom_id = elgamal.Elgamal.encrypt(vote.get_voter_custom_id().to_bytes(length = 32), public_key)
        voter_registration_id = elgamal.Elgamal.encrypt(vote.get_voter_registration_id().to_bytes(length = 32), public_key)

        return VoteDTO(voter_custom_id, voter_registration_id, vote.get_vote_payload(), vote.get_signature())

    @staticmethod
    def decrypt(vote: VoteDTO, private_key: elgamal.PrivateKey) -> VoteDTO:
        if vote is None:
            raise ValueError("vote cannot be None")

        if private_key is None:
            raise ValueError("private_key cannot be None")

        voter_custom_id = int.from_bytes(elgamal.Elgamal.decrypt(vote.get_voter_custom_id(), private_key))
        voter_registration_id = int.from_bytes(elgamal.Elgamal.decrypt(vote.get_voter_registration_id(), private_key))

        return VoteDTO(voter_custom_id, voter_registration_id, vote.get_vote_payload(), vote.get_signature())