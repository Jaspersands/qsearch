"""Item 3 (campaign 4): Lemma app-sub-character, exact over F_p.

For explicit Lazard groups of class <= 4 (truncated BCH written out), check:
  * group axioms on random triples;
  * the conjugation identity x * y * (-x) = e^{ad x} y (Step 2) on all or random pairs;
  * for the whole algebra and for every subalgebra k found by closing random
    spans: the group commutator subgroup [K,K] equals the span [k,k], and
    x * y - (x + y) lies in [k,k].  Then every homomorphism K -> C^x factors
    through the additive group k/[k,k], i.e. is omega^lambda with lambda linear
    and zero on [k,k] (the Lemma), and the number of homomorphisms is
    p^{dim k - dim [k,k]}.
Run: /opt/anaconda3/bin/python check_character.py
"""
import itertools
import random

random.seed(3)


class Lie:
    def __init__(self, p, dim, brackets, name, cls):
        assert cls < p and cls <= 4
        self.p, self.n, self.name, self.cls = p, dim, name, cls
        self.T = {}
        for (i, j), vec in brackets.items():
            self.T[(i, j)] = {k: c % p for k, c in vec.items()}
            self.T[(j, i)] = {k: (-c) % p for k, c in vec.items()}
        self.inv = {k: pow(k, p - 2, p) for k in range(1, p)}

    def br(self, x, y):
        p = self.p
        out = [0] * self.n
        for i, a in enumerate(x):
            if a:
                for j, b in enumerate(y):
                    if b and (i, j) in self.T:
                        for k, c in self.T[(i, j)].items():
                            out[k] = (out[k] + a * b * c) % p
        return tuple(out)

    def add(self, *vs):
        return tuple(sum(c) % self.p for c in zip(*vs))

    def sc(self, a, v):
        return tuple((a * x) % self.p for x in v)

    def frac(self, a, b):
        return (a * self.inv[b % self.p]) % self.p

    def bch(self, x, y):
        """truncated BCH through degree 4 (exact for class <= 4, p > 4)."""
        b = self.br
        xy = b(x, y)
        terms = [x, y, self.sc(self.frac(1, 2), xy)]
        if self.cls >= 3:
            terms += [self.sc(self.frac(1, 12), b(x, xy)), self.sc(self.frac(-1, 12), b(y, xy))]
        if self.cls >= 4:
            terms.append(self.sc(self.frac(-1, 24), b(y, b(x, xy))))
        return self.add(*terms)

    def neg(self, x):
        return self.sc(-1, x)

    def ad_exp(self, x, y, cls):
        out, term, fact = y, y, 1
        for k in range(1, cls):
            term = self.br(x, term)
            fact *= k
            out = self.add(out, self.sc(self.frac(1, fact), term))
        return out


def span(L, vecs):
    """row-reduced basis over F_p."""
    p = L.p
    rows = []
    for v in vecs:
        v = list(v)
        for r, piv in rows:
            if v[piv]:
                f = v[piv]
                v = [(a - f * b) % p for a, b in zip(v, r)]
        nz = next((i for i, a in enumerate(v) if a), None)
        if nz is not None:
            inv = pow(v[nz], p - 2, p)
            v = [(a * inv) % p for a in v]
            new = []
            for r, piv in rows:
                if r[nz]:
                    f = r[nz]
                    r = [(a - f * b) % p for a, b in zip(r, v)]
                new.append((r, piv))
            rows = new + [(v, nz)]
    return rows


def elements(L, basis):
    p = L.p
    out = set()
    for coeffs in itertools.product(range(p), repeat=len(basis)):
        v = [0] * L.n
        for c, (r, _) in zip(coeffs, basis):
            if c:
                v = [(a + c * b) % p for a, b in zip(v, r)]
        out.add(tuple(v))
    return out


def subalgebra_closure(L, gens):
    B = span(L, gens)
    while True:
        vecs = [tuple(r) for r, _ in B]
        new = vecs + [L.br(a, b) for a in vecs for b in vecs]
        B2 = span(L, new)
        if len(B2) == len(B):
            return B
        B = B2


def group_commutator_subgroup(L, K):
    Kl = list(K)
    comms = set()
    sample = Kl if len(Kl) <= 130 else random.sample(Kl, 130)
    for x in sample:
        for y in sample:
            c = L.bch(L.bch(L.neg(x), L.neg(y)), L.bch(x, y))
            comms.add(c)
    # closure under *
    S = set(comms) | {tuple([0] * L.n)}
    frontier = list(S)
    gens = list(comms)
    while frontier:
        nf = []
        for a in frontier:
            for g in gens:
                c = L.bch(a, g)
                if c not in S:
                    S.add(c)
                    nf.append(c)
        frontier = nf
    return S


def check(L, cls, n_sub=6, extra=()):
    p, n = L.p, L.n
    zero = tuple([0] * n)
    allv = list(itertools.product(range(p), repeat=n))
    # group axioms
    for _ in range(300):
        x, y, z = (random.choice(allv) for _ in range(3))
        assert L.bch(L.bch(x, y), z) == L.bch(x, L.bch(y, z)), "assoc"
        assert L.bch(x, L.neg(x)) == zero
        assert L.bch(x, L.sc(2, x)) == L.sc(3, x)
    # Step 2 identity
    pairs = [(x, y) for x in allv for y in allv] if len(allv) <= 130 else [(random.choice(allv), random.choice(allv)) for _ in range(4000)]
    for x, y in pairs:
        assert L.bch(L.bch(x, y), L.neg(x)) == L.ad_exp(x, y, cls), "conj identity"
    # subalgebras: whole algebra plus closures of random spans
    subs = [list(map(tuple, [[int(i == j) for j in range(n)] for i in range(n)]))]
    for _ in range(n_sub):
        k = random.randint(1, n - 1)
        subs.append([tuple(random.randrange(p) for _ in range(n)) for _ in range(k)])
    subs += [list(g) for g in extra]
    seen = set()
    results = []
    for gens in subs:
        B = subalgebra_closure(L, gens)
        key = tuple(tuple(r) for r, _ in sorted(B, key=lambda t: t[1]))
        if key in seen or not B:
            continue
        seen.add(key)
        K = elements(L, B)
        vecs = [tuple(r) for r, _ in B]
        D = span(L, [L.br(a, b) for a in vecs for b in vecs])
        Dset = elements(L, D) if D else {zero}
        Cg = group_commutator_subgroup(L, K)
        assert Cg == Dset, ("[K,K] != [k,k]", L.name, len(B))
        Kl = list(K)
        for _ in range(500):
            x, y = random.choice(Kl), random.choice(Kl)
            diff = L.add(L.bch(x, y), L.neg(L.add(x, y)))
            assert diff in Dset, "x*y - (x+y) not in [k,k]"
        results.append((len(B), len(D)))
    return results


def heis(p):
    return Lie(p, 3, {(0, 1): {2: 1}}, f"Heis(F_{p})", 2)


def filiform(p, n):
    return Lie(p, n, {(0, i): {i + 1: 1} for i in range(1, n - 1)}, f"filiform{n}(F_{p})", n - 1)


def free23(p):
    # x=0, y=1, [x,y]=2, [x,[x,y]]=3, [y,[x,y]]=4
    return Lie(p, 5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}}, f"free(2,3)(F_{p})", 3)


if __name__ == "__main__":
    cases = [(heis(3), 2), (heis(5), 2), (filiform(5, 4), 3), (filiform(7, 4), 3),
             (free23(5), 3), (filiform(5, 5), 4), (filiform(7, 5), 4)]
    def e(n, *idx):
        return [tuple(int(j == i) for j in range(n)) for i in idx]
    extras = {
        "free(2,3)(F_5)": [e(5, 0, 2), e(5, 1, 2), e(5, 0, 3, 4)],
        "filiform5(F_5)": [e(5, 0, 2), e(5, 0, 3), e(5, 1, 2, 3)],
        "filiform5(F_7)": [e(5, 0, 2), e(5, 0, 3)],
        "filiform4(F_7)": [e(4, 0, 2), e(4, 1, 2, 3)],
    }
    for L, cls in cases:
        res = check(L, cls, extra=extras.get(L.name, ()))
        print(f"{L.name:18s} class {cls}: axioms, conjugation identity ok; "
              f"(dim k, dim [k,k]) checked: {sorted(set(res))}; homomorphism count p^(dim k - dim[k,k]) follows")
    print("ALL OK")
