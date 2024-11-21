from .auth_token import AuthToken

class Credentials:

    def __init__(self, username: str, password: str, auth_token: AuthToken) -> 'Credentials':
        self._username = username
        self._password = password
        self._auth_token = auth_token

    def get_username(self) -> str:
        return self._username

    def get_password(self) -> str:
        return self._password

    def get_auth_token(self) -> str:
        return self._auth_token
