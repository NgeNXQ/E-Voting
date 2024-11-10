class User:

    _next_id: int = -1

    def __init__(self, is_eligible_voter: bool, is_eligible_candidate: bool) -> 'User':
        User._next_id += 1
        self._id = User._next_id
        self._is_eligible_voter = is_eligible_voter
        self._is_eligible_candidate = is_eligible_candidate

    def get_id(self) -> int:
        return self._id

    def get_is_eligible_voter(self) -> bool:
        return self._is_eligible_voter

    def get_is_eligible_candidate(self) -> bool:
        return self._is_eligible_candidate