"""Lemma G check [sampled]: on random banks, no fresh set of at most codim(U) columns
is dependent modulo an adaptively built realised space U, at a large prime; at small
primes this fails (small circuits mod U appear), so the large-prime hypothesis is needed.

For each run: random bank of M = M_J(a) + 20 columns, the block-refined forward pass of
brt.forward (random scan order, random split) builds U_1, U_2, ...  At every intermediate
U_l we (i) test N random fresh q-subsets (q = codim U_l) for independence mod U_l and
(ii) exhaustively search fresh subsets of size <= 3 (when q >= 3) for a dependency mod U_l.
"""
import itertools
import random
import sys

from subB import F, BigF, rank, brt

def run(p, k, a, J, runs, nsub, rng):
    Fd = F(p, k) if p < 10**5 else BigF(p, k)
    M = brt.arity(a, J) + 20
    dep_sub = tot_sub = small_found = small_checked = 0
    for _ in range(runs):
        cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
        rng.shuffle(cols)
        rounds, basis, top, used, status = brt.forward(Fd, cols, J, rng, split="random")
        fresh = cols[used:]
        # prefixes of the basis after each level round
        pref = []
        n = 0
        for R in rounds:
            if R.kind == "level":
                n += len(R.added)
                pref.append(n)
        for n in pref:
            U = basis[:n]
            q = a - n
            if q <= 0:
                continue
            for _ in range(nsub):
                T = rng.sample(fresh, min(q, len(fresh)))
                tot_sub += 1
                if rank(U + T, p) < n + len(T):
                    dep_sub += 1
            if q >= 3 and len(fresh) <= 40:
                for sz in (1, 2, 3):
                    for T in itertools.combinations(fresh, sz):
                        small_checked += 1
                        if rank(U + list(T), p) < n + sz:
                            small_found += 1
    return dict(dep_q_subsets=f"{dep_sub}/{tot_sub}", small_dep=f"{small_found}/{small_checked}")


if __name__ == "__main__":
    rng = random.Random(20261107)
    for (p, k, a, J, runs) in [(2**31 - 1, 2, 10, 3, 6), (2**31 - 1, 2, 14, 4, 4),
                               ((2**31 - 1), 3, 10, 3, 4) if (2**31 - 2) % 3 == 0 else (1000000009, 3, 10, 3, 4),
                               (13, 2, 10, 3, 6), (29, 2, 10, 3, 6), (31, 3, 10, 3, 4)]:
        if (p - 1) % k:
            continue
        print(f"p={p} kappa={k} a={a} J={J} runs={runs}:", run(p, k, a, J, runs, 30, rng), flush=True)
