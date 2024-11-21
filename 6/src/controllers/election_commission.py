from uuid import UUID
from elgamal import elgamal
from utilities import bbs
from helpers.codicons import *
from models import Vote, AuthToken, Candidate

class ElectionCommissionController:

    def __init__(self, voters_ids: list[UUID], candidates: list[Candidate]) -> 'ElectionCommissionController':
        self._voted_voters: set[bytes] = set()
        self._bbs_keys: bbs.KeysPair = bbs.new_keys()
        self._voters_tokens: dict[UUID, AuthToken] = dict()
        self._results = {candidate.get_id(): 0 for candidate in candidates}
        self._voters_elgamal_keys: dict[elgamal.PublicKey, elgamal.PrivateKey] = dict()

        for voter_id in voters_ids:
            elgamal_public_key, elgamal_private_key = elgamal.Elgamal.newkeys(32)
            self._voters_elgamal_keys[elgamal_public_key] = elgamal_private_key
            self._voters_tokens[voter_id] = AuthToken(voter_id, elgamal_public_key, self._bbs_keys)

    def get_voters_tokens(self) -> list[AuthToken]:
        return list(self._voters_tokens.values())

    def register_vote(self, vote: Vote, elgamal_public_key: elgamal.PublicKey) -> None:
        if vote is None:
            raise ValueError("vote cannot be None")

        print(f"|LOG| [vote] {{{vote.get_id()}}} ", end = '')

        if elgamal_public_key not in self._voters_elgamal_keys.keys():
            print(f"{STATUS_ICON_FAILURE} (Unknown voter)")
            return

        decrypted_message: bytearray = elgamal.Elgamal.decrypt(vote.get_payload(), self._voters_elgamal_keys[elgamal_public_key])
        message_slices: list[bytearray] = decrypted_message.split(Vote.DELIMITER_BYTE)

        if len(message_slices) != Vote.CHUNKS_COUNT:
            print(f"{STATUS_ICON_FAILURE} (Invalid message)")
            return

        seed: int = int.from_bytes(message_slices[Vote.CHUNK_SEED_INDEX])
        voter_id: bytes = bytes(message_slices[Vote.CHUNK_VOTER_ID_INDEX])

        if voter_id in self._voted_voters:
            print(f"{STATUS_ICON_FAILURE} (Voter has already voted)")
            return False

        candidate_id: int = bbs.decrypt(int.from_bytes(message_slices[Vote.CHUNK_CANDIDATE_ID_INDEX]), seed, self._bbs_keys.get_public_key())

        if candidate_id not in self._results.keys():
            print(f"{STATUS_ICON_FAILURE} (Invalid candidate)")
            return False

        print(STATUS_ICON_SUCCESS)
        self._results[candidate_id] += 1
        self._voted_voters.add(voter_id)

    def print_results(self) -> None:
        print("\n|RESULTS|\n")

        for candidate_id, vote_count in sorted(self._results.items(), key = lambda item: item[1], reverse = True):
            print(f"|REPORT| #{candidate_id}: {vote_count} votes")
