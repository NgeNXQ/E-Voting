class VoterEntry:

    def __init__(self, voter_id: int, username: str, password_hash: int) -> 'VoterEntry':
        self._voter_id = voter_id
        self._username = username
        self._password_hash = password_hash

    def get_voter_id(self) -> int:
        return self._voter_id

    def get_username(self) -> str:
        return self._username

    def get_password_hash(self) -> int:
        return self._password_hash
