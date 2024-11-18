import uuid

class User:

    _next_id = 0

    def __init__(self) -> 'User':
        User._next_id += 1
        self._id = User._next_id
        self._passport_id: int = uuid.uuid4().int

    def get_id(self) -> int:
        return self._id

    def get_passport_id(self) -> int:
        return self._passport_id
