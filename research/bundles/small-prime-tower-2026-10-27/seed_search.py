"""Bounded Paley-biclique discovery; only exact certificates carry evidence."""

import argparse
import heapq
import json
import random

from flint import fmpz


def prime_check(p):
    if type(p) is not int or p < 3 or p % 4 != 3 or not fmpz(p).is_prime():
        raise ValueError("an odd prime congruent to 3 modulo 4 is required")


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def search(p, *, width=300, seed=0, rounds=1):
    """Seek eleven x values with at least thirteen common square predecessors.

    Translation allows the first x to be zero. Randomized beam tie-breaking
    is a discovery heuristic, not a completeness or asymptotic guarantee.
    """
    prime_check(p)
    if any(type(v) is not int or v < 1 for v in (width, rounds)):
        raise ValueError("positive beam width and round count required")
    if type(seed) is not int:
        raise ValueError("integer replay seed required")
    squares = {a*a % p for a in range(1, p)}
    neighbors = [sum(1 << ((x-a) % p) for a in squares) for x in range(p)]
    rng = random.Random(seed)
    examined, best = 0, None
    for trial in range(rounds):
        beam = [((0,), neighbors[0])]
        for size in range(2, 12):
            frontier = []
            seen = set()
            for xs, mask in beam:
                for x in range(xs[-1]+1, p):
                    common = mask & neighbors[x]
                    examined += 1
                    count = common.bit_count()
                    if count < 13 or common in seen:
                        continue
                    seen.add(common)
                    item = (count, rng.random(), xs+(x,), common)
                    if len(frontier) < width:
                        heapq.heappush(frontier, item)
                    elif item[:2] > frontier[0][:2]:
                        heapq.heapreplace(frontier, item)
            if not frontier:
                break
            beam = [(item[2], item[3]) for item in frontier]
            best = max(frontier)
            if size == 11:
                xs, common = best[2:]
                return {"status": "EXACT_SEED_FOUND", "prime": p,
                        "branches": list(bits(common))[:13], "splitting_x": list(xs),
                        "intersections_examined": examined, "round": trial+1,
                        "seed": seed, "width": width,
                        "smallest_prime_claimed": False}
    return {"status": "UNKNOWN_SEARCH_CAP", "prime": p,
            "intersections_examined": examined, "seed": seed, "width": width,
            "best_partial_x": list(best[2]) if best else [],
            "nonexistence_established": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prime", type=int)
    parser.add_argument("--width", type=int, default=300)
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(search(args.prime, width=args.width, rounds=args.rounds,
                            seed=args.seed), indent=2))
