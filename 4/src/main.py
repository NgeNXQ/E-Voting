from copy import deepcopy
from models import Candidate, VoteOnion
from controllers import VoterController

def main() -> None:
    candidate_1 = Candidate()
    candidate_2 = Candidate()

    voter_0 = VoterController()     # A
    voter_1 = VoterController()     # B
    voter_2 = VoterController()     # C
    voter_3 = VoterController()     # D

    voter_0.generate_rsa_keys_pairs()
    voter_1.generate_rsa_keys_pairs()
    voter_2.generate_rsa_keys_pairs()
    voter_3.generate_rsa_keys_pairs()

    vote_0 = voter_0.vote(candidate_1)
    vote_1 = voter_1.vote(candidate_2)
    vote_2 = voter_2.vote(candidate_1)
    vote_3 = voter_3.vote(candidate_1)

    votes:list[VoteOnion] = [vote_0, vote_1, vote_2, vote_3]

    # External part
    voter_0.decrypt_external_part(votes)
    voter_1.decrypt_external_part(votes)
    # voter_1.decrypt_external_part([vote_0, vote_1, deepcopy(vote_1), vote_2, vote_3])     # Extra vote
    voter_2.decrypt_external_part(votes)
    voter_3.decrypt_external_part(votes)

    # Internal part
    voter_0.decrypt_internal_part(votes)
    voter_1.decrypt_internal_part(votes)
    voter_2.decrypt_internal_part(votes)
    # voter_2.decrypt_internal_part([vote_1, vote_2, deepcopy(vote_2), vote_3])               # Vote duplication & removal
    voter_3.decrypt_internal_part(votes)

    print_results([candidate_1, candidate_2], votes)

def print_results(candidates: list[Candidate], votes: list[VoteOnion]) -> None:
    results = { candidate.get_id(): 0 for candidate in candidates }

    for vote in votes:
        vote.remove_initial_noise()
        results[int.from_bytes(vote.get_buffer())] += 1

    sorted_results = sorted(results.items(), key = lambda item: item[1], reverse = True)
    max_votes = sorted_results[0][1] if sorted_results else 0

    for candidate, count in sorted_results:
        print(f"\nCandidate #{candidate}: {count} vote(s)", end = '')

    winners = [candidate for candidate, count in sorted_results if count == max_votes]

    if len(winners) == 1:
        print(f"\nWINNER is candidate #{winners[0]} with {max_votes} vote(s).")
    else:
        print("\nDRAW between ", end = '')

        for candidate in winners:
            print(f"candidate #{candidate} with {max_votes} vote(s) ", end = '')

if __name__ == "__main__":
    main()
