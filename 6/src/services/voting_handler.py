from elgamal import elgamal
from helpers.codicons import *
from utilities import bbs
from controllers import ElectionCommissionController
from models import Vote, AuthToken, Candidate, Voter

class VotingHandlerServie:

    def __init__(self, voters: list[Voter], election_commission: ElectionCommissionController) -> 'VotingHandlerServie':
        self._active_session: Voter = None
        self._voters: list[Voter] = voters
        self._active_session_index: int = 0
        self._election_commission: ElectionCommissionController = election_commission

    def login(self, username: str, password: str) -> None:
        print(f"|LOG| [auth] {{{self._active_session_index}}} ", end = '')

        for voter in self._voters:
            if voter.get_username() == username:
                self._active_session = voter
                break

        if self._active_session is None:
            print(f"{STATUS_ICON_FAILURE} (Invalid username)")
            return

        if hash(password) != self._active_session.get_password_hash():
            print(f"{STATUS_ICON_FAILURE} (Invalid password)")
            self._active_session = None
            return

        print(STATUS_ICON_SUCCESS)
        self._active_session_index += 1

    def vote(self, candidate: Candidate, auth_token: AuthToken) -> None:
        if candidate is None:
            raise ValueError("candidate cannot be None")

        if auth_token is None:
            raise ValueError("auth_token cannot be None")

        if self._active_session is None:
            return

        if self._active_session is None:
            print(f"{STATUS_ICON_FAILURE} (Invalid user)")
            return

        if auth_token.get_voter_id() != self._active_session.get_voter_id():
            print(f"{STATUS_ICON_FAILURE} (Invalid token)")
            return

        self._active_session = None
        vote: Vote = self._pack_vote_payload(candidate.get_id(), auth_token)
        self._election_commission.register_vote(vote, auth_token.get_elgamal_public_key())

    def _pack_vote_payload(self, candidate_id: int, auth_token: AuthToken) -> Vote:
        encrypted_candidate_id: int = bbs.encrypt(candidate_id, auth_token.get_bbs_keys().get_seed(), auth_token.get_bbs_keys().get_public_key())
        payload: bytes = encrypted_candidate_id.to_bytes() + Vote.DELIMITER_BYTE + auth_token.get_bbs_keys().get_seed().to_bytes() + Vote.DELIMITER_BYTE + auth_token.get_voter_id().bytes
        encrypted_payload: elgamal.CipherText = elgamal.Elgamal.encrypt(payload, auth_token.get_elgamal_public_key())
        return Vote(encrypted_payload)
