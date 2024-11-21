from uuid import UUID, uuid4

class User:

    _next_id = 0

    def __init__(self, is_eligible_voter: bool) -> 'User':
        User._next_id += 1
        self._id = User._next_id
        self._passport_id: UUID = uuid4()
        self._is_eligible_voter = is_eligible_voter

    @classmethod
    def get_users_total_count(cls) -> int:
        return User._next_id

    def get_id(self) -> int:
        return self._id

    def get_passport_id(self) -> UUID:
        return self._passport_id

    def get_is_eligible_voter(self) -> bool:
        return self._is_eligible_voter
