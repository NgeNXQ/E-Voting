from datetime import datetime

class VotePayload:

    def __init__(self, candidate_id: int) -> None:
        self._timestamp = datetime.now()
        self._candidate_id = candidate_id

    def get_candidate_id(self) -> int:
        return self._candidate_id

    def __hash__(self) -> int:
        return hash(self._candidate_id) ^ hash(self._timestamp)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VotePayload):
            return False
        return (self._candidate_id == other._candidate_id and self._timestamp == other._timestamp)

class VoteDTO:

    def __init__(self, voter_custom_id: int, voter_registration_id: int, vote_payload: VotePayload, signature: bytes) -> None:
        self._signature = signature
        self._vote_payload = vote_payload
        self._voter_custom_id = voter_custom_id
        self._voter_registration_id = voter_registration_id

    def get_signature(self) -> bytes:
        return self._signature

    def get_voter_custom_id(self) -> int:
        return self._voter_custom_id

    def get_voter_registration_id(self) -> int:
        return self._voter_registration_id

    def get_vote_payload(self) -> VotePayload:
        return self._vote_payload