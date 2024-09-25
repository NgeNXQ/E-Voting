import rsa
from controllers import VoterController, VoterDebugMode
from models import Candidate, VoteRecordPayload, SignedVoteRecord

class CommissionController:

    def __init__(self, candidates: list[Candidate]) -> None:
        self._gamma_key = "1Q2W3E".encode()
        self._vote_records = {}
        self._verified_voters_keys = []
        self._results = {candidate.get_id(): 0 for candidate in candidates}

    def get_gamma_key(self) -> bytes:
        return self._gamma_key

    def process_voter(self, voter: VoterController, candidate: Candidate) -> None:
        if voter is None:
            raise ValueError("voter is None")

        if candidate is None:
            raise ValueError("candidate is None")

        print(f"Processing voter #{voter.get_id()} | ", end = '')

        if self._verify_voter(voter):
            vote_record = self._create_protocol(voter, candidate)
            self.register_vote(vote_record, voter.get_public_key())

    def _verify_voter(self, voter: VoterController) -> bool:
        if not voter.get_is_able_to_vote():
            print(f"ABORTED. Voter is not able to vote.")
            return False

        if voter.get_public_key() in self._vote_records:
            print(f"ABORTED. Voter has already voted.")
            return False

        self._verified_voters_keys.append(voter.get_public_key())
        return True

    def _create_protocol(self, voter: VoterController, candidate: Candidate) -> VoteRecordPayload | SignedVoteRecord:
        vote_record = voter.vote(candidate)

        if voter.get_debug_mode() is VoterDebugMode.VOTE_RECORD_SUBSTITUTION:
            FAKE_CANDIDATE_ID = 0
            vote_record.set_candidate_id(FAKE_CANDIDATE_ID)

        if voter.get_debug_mode() is not VoterDebugMode.MISSING_SIGNATURE:
            vote_record = voter.sign(vote_record)

        if voter.get_debug_mode() is not VoterDebugMode.MISSING_GAMMA_ENCRYPTION:
            vote_record.toggle_gamma_encryption(self._gamma_key)

        return vote_record

    def register_vote(self, signed_vote_record: SignedVoteRecord, public_key: rsa.PublicKey) -> None:
        if signed_vote_record is None:
            raise ValueError("signed_vote_record is None")

        if not signed_vote_record.get_is_encrypted():
            print("ABORTED. Vote record must be encrypted.")
            return

        if isinstance(signed_vote_record, VoteRecordPayload):
            print("ABORTED. Vote record must be signed.")
            return

        if public_key not in self._verified_voters_keys:
            print("ABORTED. Voter must be validated.")
            return

        signed_vote_record.toggle_gamma_encryption(self._gamma_key)

        if hash(signed_vote_record.get_vote_record()) != signed_vote_record.get_vote_record().get_control_hash_sum():
            print("ABORTED. Hash control sum check failed.")
            return

        try:
            rsa.verify(int.to_bytes(signed_vote_record.get_vote_record().get_candidate_id()), signed_vote_record.get_signature(), public_key)
        except rsa.VerificationError:
            print(f"ABORTED. Signature verification failed.")
            return

        self._verified_voters_keys.remove(public_key)
        self._results[signed_vote_record.get_vote_record().get_candidate_id()] += 1
        self._vote_records[public_key] = signed_vote_record.get_vote_record().get_candidate_id()

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