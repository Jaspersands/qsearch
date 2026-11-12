"""Classical step of the zero-sum route: find a nonempty subset of measured central
frequencies k_i in Z_W, W = 2^m, with sum = 0 mod W.  Wagner k-tree with + only
(the endomorphisms x -> x^j scale the centre by j^2 >= 0, so no signs are free).

Run: nice -n 19 /opt/anaconda3/bin/python zero_sum_sieve.py
Finite demonstration only: it shows the step is the random modular subset-sum /
generalized-birthday problem, solvable with about 2^ell * 2^{m/(ell+1)} samples
at depth ell; it says nothing about lower bounds.
"""
import random
from collections import defaultdict

def merge(A, B, mod_bits, W):
    """A, B: lists of (value mod W, index tuple). Keep pairs with value sum = 0 mod 2^mod_bits."""
    M = 1 << mod_bits
    table = defaultdict(list)
    for val, idx in B:
        table[val % M].append((val, idx))
    out = []
    for val, idx in A:
        for val2, idx2 in table.get((-val) % M, []):
            out.append(((val + val2) % W, idx + idx2))
    return out

def ktree(m, ell, rng):
    W = 1 << m
    L = 1 << ((m + ell) // (ell + 1))
    lists = [[(rng.randrange(W), (i * L + j,)) for j in range(L)] for i in range(1 << ell)]
    step = m // (ell + 1)
    for level in range(1, ell + 1):
        bits = m if level == ell else step * level
        lists = [merge(lists[2 * i], lists[2 * i + 1], bits, W) for i in range(len(lists) // 2)]
    sols = [idx for val, idx in lists[0] if val == 0]
    return W, L * (1 << ell), sols, lists

if __name__ == "__main__":
    rng = random.Random(11)
    for m, ell in [(24, 2), (32, 3), (40, 3), (48, 4)]:
        W, nsamp, sols, _ = ktree(m, ell, rng)
        print(f"W = 2^{m}, depth {ell}: {nsamp} samples, {len(sols)} zero-sum subsets of size {2 ** ell} found", flush=True)
