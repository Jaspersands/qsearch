"""Small exact Lazard rings over mixed Z/p^e moduli, for brute-force checks.

Elements are coordinate tuples; coordinate i lives in Z/p^{e_i}. Brackets come
from integer structure constants. BCH is implemented through class 3 (enough
for every ring used here). Read-only helper for the App D check.
"""
from fractions import Fraction
from itertools import product


class Ring:
    def __init__(self, p, exps, const, cls):
        self.p, self.exps, self.cls = p, tuple(exps), cls
        self.mods = tuple(p**e for e in exps)
        self.M = max(self.mods)
        self.n = len(exps)
        self.const = {}  # (i,j) -> tuple of coefficients
        for (i, j), v in const.items():
            self.const[i, j] = tuple(v)
            self.const[j, i] = tuple(-x for x in v)
        self.zero = (0,) * self.n
        # well-definedness: p^{e_i} e_i bracket e_j must vanish
        for (i, j), v in self.const.items():
            for k in range(self.n):
                assert (self.mods[i] * v[k]) % self.mods[k] == 0, ("ill-defined", i, j, k)

    def red(self, v):
        return tuple(x % m for x, m in zip(v, self.mods))

    def add(self, x, y):
        return self.red([a + b for a, b in zip(x, y)])

    def smul(self, r, x):
        if isinstance(r, Fraction):
            r = r.numerator * pow(r.denominator, -1, self.M)
        return self.red([r * a for a in x])

    def neg(self, x):
        return self.smul(-1, x)

    def br(self, x, y):
        out = [0] * self.n
        for (i, j), v in self.const.items():
            a = x[i] * y[j]
            if a:
                for k in range(self.n):
                    out[k] += a * v[k]
        return self.red(out)

    def bch(self, x, y):
        out = self.add(x, y)
        if self.cls >= 2:
            xy = self.br(x, y)
            out = self.add(out, self.smul(Fraction(1, 2), xy))
        if self.cls >= 3:
            out = self.add(out, self.smul(Fraction(1, 12), self.br(x, xy)))
            out = self.add(out, self.smul(Fraction(-1, 12), self.br(y, xy)))
        assert self.cls <= 3
        return out

    def elements(self):
        return [tuple(t) for t in product(*[range(m) for m in self.mods])]

    def additive_span(self, gens):
        S = {self.zero}
        frontier = [self.zero]
        gens = list(gens)
        while frontier:
            new = []
            for s in frontier:
                for g in gens:
                    t = self.add(s, g)
                    if t not in S:
                        S.add(t); new.append(t)
            frontier = new
        return frozenset(S)

    def subring(self, gens):
        S = self.additive_span(gens)
        gens = list(gens)
        while True:
            extra = {self.br(a, b) for a in S for b in gens} - S
            if not extra:
                return S
            S = self.additive_span(set(S) | extra)

    def group_closure(self, gens):
        S = {self.zero}
        frontier = [self.zero]
        while frontier:
            new = []
            for s in frontier:
                for g in gens:
                    t = self.bch(s, g)
                    if t not in S:
                        S.add(t); new.append(t)
            frontier = new
        return frozenset(S)

    def is_subring(self, S):
        return all(self.add(a, b) in S and self.br(a, b) in S for a in S for b in S)

    def lcs_dims(self, S):
        """log_p sizes of gamma_j(S) for j=1.. until 0 (S a subring)."""
        out, cur = [], S
        while len(cur) > 1:
            out.append(len(cur))
            cur = self.additive_span({self.br(a, b) for a in S for b in cur})
        return out

    def cyc_rank(self, A):
        """d(A) = dim_Fp A[p] for an additive subgroup A."""
        k = sum(1 for a in A if self.smul(self.p, a) == self.zero)
        d = 0
        while self.p**d < k:
            d += 1
        assert self.p**d == k
        return d


def logp(n, p):
    d = 0
    while p**d < n:
        d += 1
    assert p**d == n
    return d
