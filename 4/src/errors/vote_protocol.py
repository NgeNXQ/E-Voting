class VoteProtocolError(Exception):

    def __init__(self, message: str) -> 'VoteProtocolError':
        self.message = message
        super().__init__(self.message)
