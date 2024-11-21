import string
import random
from uuid import UUID, uuid4
from helpers.codicons import *
from models import User, Voter, AuthToken, Credentials

class RegistrationCommissionController:

    _PASSPORT_ID_PLACEHOLDER: UUID = None
    _CREDENTIALS_CONTENT: str = string.ascii_letters + string.digits

    def __init__(self, voters_count: int) -> 'RegistrationCommissionController':
        self._voter_index: int = -1
        self._usernames: set[str] = set()
        self._voters: list[Voter] = list()
        self._voters_data: dict[UUID, UUID] = dict()
        self._voters_tokens: dict[UUID, AuthToken] = dict()

        for _ in range(voters_count):
            self._voters_data[uuid4()] = RegistrationCommissionController._PASSPORT_ID_PLACEHOLDER

    def get_voters(self) -> list[Voter]:
        return self._voters

    def get_voters_ids(self) -> list[UUID]:
        return list(self._voters_data.keys())

    def setup_voters_tokens(self, auth_tokens: list[AuthToken]) -> None:
        if auth_tokens is None:
            raise ValueError("auth_tokens cannot be None")

        for auth_token in auth_tokens:
            self._voters_tokens[auth_token.get_voter_id()] = auth_token

    def register_user(self, user: User) -> Credentials:
        if user is None:
            raise ValueError("user cannot be None")

        print(f"|LOG| [registration] {{{user.get_id()}}} ", end = '')

        if not user.get_is_eligible_voter():
            print(f"{STATUS_ICON_FAILURE} (User is not able to vote)")
            return

        self._voter_index += 1

        if user.get_passport_id() in self._voters_data.values():
            print(f"{STATUS_ICON_FAILURE} (User has already been registered)")
            return

        username: str = self._generate_username()
        password: str = self._generate_password()

        print(STATUS_ICON_SUCCESS)

        id: UUID = list(self._voters_data.keys())[self._voter_index]
        self._voters_data[id] = user.get_passport_id()
        auth_token: AuthToken = self._voters_tokens[id]
        self._voters.append(Voter(id, username, hash(password)))
        return Credentials(username, password, auth_token)

    def _generate_username(self) -> str:
        USERNAME_CHARACTERS_COUNT: int = 10
        username = self._generate_random_string(USERNAME_CHARACTERS_COUNT)

        while username in self._usernames:
            username = self._generate_random_string(USERNAME_CHARACTERS_COUNT)

        self._usernames.add(username)

        return username

    def _generate_password(self) -> str:
        PASSWORD_CHARACTERS_COUNT: int = 10
        return self._generate_random_string(PASSWORD_CHARACTERS_COUNT)

    def _generate_random_string(self, length: int) -> str:
        return ''.join(random.choice(RegistrationCommissionController._CREDENTIALS_CONTENT) for _ in range(length))
