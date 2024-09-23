import rsa
from controllers import VoterController
from models import Candidate, VoteRecord, SignedVoteRecord

class CommissionController:

    _ENABLE_FAKE_SIGNATURE = False
    _ENABLE_SIGNATURE_VALIDATION = True
    _ENABLE_GAMMA_ENCRYPTION_VALIDATION = True

    def __init__(self, candidates: list['Candidate']) -> None:
        self._candidates = candidates
        self._gamma_key = "1Q2W3E".encode()
        self._voted_public_keys = []
        self._validated_public_keys = []
        self._results = {candidate.get_id(): 0 for candidate in self._candidates}

    def get_gamma_key(self) -> bytes:
        return self._gamma_key

    def process_voter(self, voter: 'VoterController', candidate: 'Candidate') -> None:
        if voter is None:
            raise ValueError("voter is None")

        if candidate is None:
            raise ValueError("candidate is None")

        print(f"Processing voter #{voter.get_id()} | ", end = '')

        if not voter.get_is_able_to_vote():
            print(f"ABORTED. Voter is not able to vote.")
            return

        if voter.get_public_key() in self._voted_public_keys:
            print(f"ABORTED. Voter has already voted.")
            return

        vote_record = voter.vote(candidate)
        self._validated_public_keys.append(voter.get_public_key())

        if self._ENABLE_SIGNATURE_VALIDATION:
            vote_record = voter.sign(vote_record)

        if self._ENABLE_GAMMA_ENCRYPTION_VALIDATION:
            vote_record.toggle_gamma_encryption(self._gamma_key)

        self.register_vote(vote_record)

    def register_vote(self, signed_vote_record: 'SignedVoteRecord') -> None:
        if signed_vote_record is None:
            raise ValueError("signed_vote_record is None")

        if not signed_vote_record.get_is_encrypted():
            print("ABORTED. Vote record must be encrypted.")
            return

        if isinstance(signed_vote_record, VoteRecord):
            print("ABORTED. Vote record must be signed.")
            return

        if signed_vote_record.get_vote_record().get_public_key() not in self._validated_public_keys:
            print("ABORTED. Voter must be validated.")
            return

        signed_vote_record.toggle_gamma_encryption(self._gamma_key)
        vote_record = signed_vote_record.get_vote_record()

        try:
            if self._ENABLE_FAKE_SIGNATURE:
                rsa.verify(int.to_bytes(vote_record.get_candidate_id()), bytes(), vote_record.get_public_key())
            else:
                rsa.verify(int.to_bytes(vote_record.get_candidate_id()), signed_vote_record.get_signature(), vote_record.get_public_key())
        except rsa.VerificationError:
            print(f"ABORTED. Signature verification failed.")
            return

        self._results[signed_vote_record.get_vote_record().get_candidate_id()] += 1
        self._voted_public_keys.append(signed_vote_record.get_vote_record().get_public_key())
        self._validated_public_keys.remove(signed_vote_record.get_vote_record().get_public_key())
        print(f"DONE. Registered vote for candidate #{signed_vote_record.get_vote_record().get_candidate_id()}.")

    def print_results(self) -> None:
        print(f"RESULTS")

        sorted_results = sorted(self._results.items(), key = lambda item: item[1], reverse = True)
        max_votes = sorted_results[0][1]

        for candidate, count in sorted_results:
            print(f"Candidate #{candidate}: {count} vote(s)")

        winners = [candidate for candidate, count in sorted_results if count == max_votes]

        if len(winners) == 1:
            print(f"WINNER is candidate #{winners[0]} with {max_votes} vote(s).")
        else:
            print("DRAW between ", end = '')

            for candidate in winners:
                print(f"candidate #{candidate} wtih {max_votes} vote(s) ", end = '')