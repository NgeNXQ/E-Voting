import uuid
import string
import random
from services import DatabaseService
from models import User, AuthToken, VoterEntry

class RegistrationCommissionController:

    _AUTH_TOKEN_ID_PLACEHOLDER: int = -1
    _CREDENTIALS_CONTENT: str = string.ascii_letters + string.digits

    def __init__(self, voters_count: int, database: DatabaseService) -> 'RegistrationCommissionController':
        self._database = database
        self._voters_ids:list[int] = list()
        self._voters_count:int = voters_count
        self._voters_tokens:dict[int, AuthToken] = dict()

        for i in range(voters_count):
            self._voters_ids[i] = uuid.uuid4().int

    def setup_voters_tokens(self, auth_tokens: list[AuthToken]) -> None:
        if auth_tokens is None:
            raise ValueError("auth_tokens cannot be None")

        for auth_token in auth_tokens:
            self._voters_tokens[auth_token.get_voter_id()] = auth_token

    def get_voters_ids(self) -> list[int]:
        return self._voters_ids

    def register_user(self, user: User) -> AuthToken:
        if user is None:
            raise ValueError("user cannot be None")

        username: str = self._generate_username()
        password: str = self._generate_password()

        self._database.add_entry(VoterEntry(username, hash(password)))
        return self._voters_tokens[self._voters_ids[self._database.get_entries_count()]]

    def _generate_username(self) -> str:
        USERNAME_CHARACTERS_COUNT: int = 10
        return ''.join(random.choice(RegistrationCommissionController._CREDENTIALS_CONTENT) for _ in range(USERNAME_CHARACTERS_COUNT))

    def _generate_password(self) -> str:
        PASSWORD_CHARACTERS_COUNT: int = 10
        return ''.join(random.choice(RegistrationCommissionController._CREDENTIALS_CONTENT) for _ in range(PASSWORD_CHARACTERS_COUNT))
