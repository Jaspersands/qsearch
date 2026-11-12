"""Exact probability that n i.i.d. uniform labels in F_p^g have NO nonempty zero-sum subset
(binary weights), by dynamic programming over the set of achievable subset sums.
Compared with the Chebyshev bound p^g/(2^n - 1) (pairwise independence of distinct subset sums)
and with the Davenport constant g(p-1)+1 (every sequence that long has a zero-sum). Finite check."""
import sys, itertools
from fractions import Fraction
def run(p, g, nmax):
    els = list(itertools.product(range(p), repeat=g)); idx = {e: i for i, e in enumerate(els)}
    N = len(els); zero = idx[(0,) * g]
    add = [[idx[tuple((a + b) % p for a, b in zip(els[i], els[j]))] for j in range(N)] for i in range(N)]
    def shift(mask, j):
        out = 0; m = mask
        while m:
            b = m & -m; i = b.bit_length() - 1; out |= 1 << add[i][j]; m ^= b
        return out
    states = {0: 1}
    for n in range(1, nmax + 1):
        new = {}
        for S, c in states.items():
            for j in range(N):
                S2 = S | (1 << j) | shift(S, j)
                if S2 >> zero & 1: continue
                new[S2] = new.get(S2, 0) + c
        states = new
        free = sum(states.values()); P = Fraction(free, N ** n)
        cheb = Fraction(N, 2 ** n - 1)
        print(f'p={p} g={g} n={n}: P[no zero-sum] = {float(P):.6g}  (Chebyshev bound {float(min(cheb, 1)):.4g})  states={len(states)}', flush=True)
        if free == 0:
            print(f'  every sequence of length {n} has a zero-sum; Davenport g(p-1)+1 = {g*(p-1)+1}'); break
if __name__ == '__main__':
    run(5, 1, 6); run(7, 1, 8); run(5, 2, 10)
