# from elgamal import elgamal
# from utilities import bbs
# from models import Vote, AuthToken

# class VoteWizardUtility:

#     DELIMITER: bytes = b'\x00'

#     _instance: 'VoteWizardUtility' = None

#     def __init__(self) -> 'VoteWizardUtility':
#         if VoteWizardUtility._instance is not None:
#             raise PermissionError("Attempt to initialize singleton class externally")

#     @classmethod
#     def get_instance(cls) -> 'VoteWizardUtility':
#         if cls._instance is None:
#             cls._instance = cls.__new__(cls)
#             cls._instance.__init__()
#         return cls._instance

#     @staticmethod
#     def pack(candidate_id: int, auth_token: AuthToken) -> Vote:
#         encrypted_candidate_id: int = bbs.encrypt(candidate_id, auth_token.get_bbs_seed(), auth_token.get_bbs_public_key())
#         payload: bytes = encrypted_candidate_id.to_bytes() + VoteWizardUtility.DELIMITER + auth_token.get_bbs_seed().to_bytes() + VoteWizardUtility.DELIMITER + auth_token.get_voter_id().bytes
#         encrypted_payload = elgamal.Elgamal.encrypt(payload, auth_token.get_elgamal_public_key())
#         return Vote(encrypted_payload)

#     @staticmethod
#     def unpack(vote: Vote, elgamal_private_key: elgamal.PrivateKey) -> int:
#         decrypted_message: bytes = elgamal.Elgamal.decrypt(vote.get_payload())
#         return -1

#         # encrypted_candidate_id: int = bbs.encrypt(candidate_id, auth_token.get_bbs_seed(), auth_token.get_bbs_public_key())
#         # payload: bytes = encrypted_candidate_id.to_bytes() + VoteWizardUtility.DELIMITER + auth_token.get_bbs_seed().to_bytes() + VoteWizardUtility.DELIMITER + auth_token.get_voter_id().bytes
#         # encrypted_payload: tuple[int, int] = Elgamal.encrypt(payload, auth_token.get_elgamal_public_key()).get()
#         # return Vote(encrypted_payload)
