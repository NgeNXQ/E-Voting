class Vote:

    def __init__(self, payload: bytes) -> 'Vote':
        self._payload = payload

    def get_payload(self) -> bytes:
        return self._payload