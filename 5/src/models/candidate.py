class Candidate:

    def __init__(self, id: int) -> 'Candidate':
        self._id = id

    def get_id(self) -> int:
        return self._id