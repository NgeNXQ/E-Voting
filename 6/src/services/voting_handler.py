from elgamal import elgamal
from helpers.codicons import *
from .database import DatabaseService
from controllers import ElectionCommissionController
from models import Vote, AuthToken, Candidate, VoterEntry

class VotingHandlerServie:

    def __init__(self, database: DatabaseService, election_commission: ElectionCommissionController) -> 'VotingHandlerServie':
        self._active_session: VoterEntry = None
        self._database: DatabaseService = database
        self._election_commission: ElectionCommissionController = election_commission

    def login(self, username: str, password: str) -> None:
        self._active_session = self._database.get_entry(username)

        if self._active_session is None:
            print(f"{STATUS_ICON_FAILURE} Invalid username.")
            return

        if hash(password) != self._active_session.get_password_hash():
            print(f"{STATUS_ICON_FAILURE} Invalid password.")
            return

    def vote(self, candidate: Candidate, auth_token: AuthToken) -> None:
        if candidate is None:
            raise ValueError("candidate cannot be None")

        if auth_token is None:
            raise ValueError("auth_token cannot be None")

        if self._active_session is None:
            print(f"{STATUS_ICON_FAILURE} Invalid user.")
            return

        if auth_token.get_voter_id() != self._active_session.get_voter_id():
            print(f"{STATUS_ICON_FAILURE} Invalid token.")
            return

        vote_payload: bytes = elgamal.Elgamal.encrypt(data, auth_token.get_elgamal_public_key())
        self._election_commission.register_vote(Vote())
