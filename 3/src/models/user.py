class User:

    _next_id = -1

    def __init__(self, is_able_to_vote: bool) -> None:
        User._next_id += 1
        self._id = User._next_id
        self._is_able_to_vote = is_able_to_vote

    def get_id(self) -> int:
        return self._id

    def get_is_able_to_vote(self) -> bool:
        return self._is_able_to_vote