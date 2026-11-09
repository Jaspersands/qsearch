"""Exact check: a merged column stays uniform and independent of the merge record.

Setting: children z_1..z_m i.i.d. uniform on F_p^2 (coordinate 1 is killed, coordinate 2
is the residual).  The merge rule reads only the first coordinates c = (z_l[0]) and
returns y(c) in D^m \\ 0 (deterministic: lexicographically first nonzero solution, with
a fixed tie order), or aborts.  Claim (Lemma-split-law argument): conditional on any
non-aborting record (c, y), the residual coordinate sum_l y_l z_l[1] is uniform on F_p.

Enumerates all p^m choices of c and all p^m residual tuples, for m = 2 (pair, may abort)
and m = 3 (triple).  Also checks the abort probability of the pair rule.
Usage: python uniformity_exact.py p kappa
"""
import itertools
import sys
from collections import Counter
from common import Field


def first_solution(Fd, c):
    p = Fd.p
    Dl = [0] + sorted(x for x in range(1, p) if Fd.inD(x))
    for y in itertools.product(Dl, repeat=len(c)):
        if any(y) and sum(yi * ci for yi, ci in zip(y, c)) % p == 0:
            return y
    return None


def main():
    p, k = map(int, sys.argv[1:3])
    Fd = Field(p, k)
    for m in (2, 3):
        aborts, bad, recs = 0, 0, 0
        for c in itertools.product(range(p), repeat=m):
            y = first_solution(Fd, c)
            if y is None:
                aborts += 1
                continue
            recs += 1
            cnt = Counter(sum(yi * ri for yi, ri in zip(y, r)) % p
                          for r in itertools.product(range(p), repeat=m))
            if len(cnt) != p or len(set(cnt.values())) != 1:
                bad += 1
        print(f"p={p} kappa={k} fan-in m={m}: records {recs}, aborts {aborts}/{p**m} "
              f"({aborts/p**m:.4f}), records with non-uniform residual: {bad}")


if __name__ == "__main__":
    main()
