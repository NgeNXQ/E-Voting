class Candidate:

    _next_id = 0

    def __init__(self) -> None:
        Candidate._next_id += 1
        self._id = Candidate._next_id

    def get_id(self) -> int:
        return self._id