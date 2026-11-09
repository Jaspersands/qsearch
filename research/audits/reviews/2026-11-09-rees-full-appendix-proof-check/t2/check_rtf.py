"""t2 check 2: Algorithm RtF (prop:tb-recursion) with the public arithmetic (N1)-(N6) of
lem:tb-howell-rounds over Z/p^e, on charts L = F_{s,c}(Z/p^e)/I acquired by Lemma tb-chart
(check_chart.py), against brute force.

Truth solver: returns a basis of U = {x in F_p^{m0} : sigma(iota_M(x)) in log H} (oracle-free
stand-in for Theorem thm:main).  Adversarial solver: random vectors (sometimes more than
dim Omega), as an erring call may return.
Per round (truth solver) it checks: K <= log H <= S, K ideal of S, |S/K| = prod p^{d_i},
the (N3) socle-tensor formula against the direct bracket, the coordinate map of (N2), the
idealizer (N6) against the brute-force idealizer, and k_j <= rk(L), dim[Omega,Omega] <= rk[L,L].
At the end: output = log H, calls <= b.  Adversarial runs: calls <= b and well-definedness.
Finite checks only.
"""
import random
import sys
import time
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zmod import Ring, howell, member, left_kernel, matmul, eye, span_bf, FreeLieZ  # noqa
import check_chart as cc  # noqa: E402

rng = random.Random(1109)
cc.rng = random.Random(911)
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def smith_rows(R, C, nu):
    """(P4) for an a x nu matrix given by rows (a may be 0)."""
    if not C:
        return eye(0), eye(nu), eye(nu), [R.e] * nu
    from zmod import smith
    P, Q, Qi, exps, D = smith(R, C)
    return P, Q, Qi, exps


class Chart:
    def __init__(self, p, exps, cst):
        self.p, self.exps, self.m = p, exps, len(exps)
        self.e = max(exps)
        self.R = Ring(p, self.e)
        self.M = self.R.M
        self.cst = cst

    def psi(self, t):
        return tuple(t[i] * self.p ** (self.e - self.exps[i]) % self.M for i in range(self.m))

    def psinv(self, v):
        return [(v[i] // self.p ** (self.e - self.exps[i])) % self.p ** self.exps[i]
                for i in range(self.m)]

    def brt(self, x, y):  # chart coordinates
        m, out = self.m, [0] * self.m
        for i in range(m):
            if x[i]:
                for j in range(m):
                    if y[j]:
                        for k in range(m):
                            out[k] += x[i] * y[j] * self.cst[i, j][k]
        return [out[k] % self.p ** self.exps[k] for k in range(m)]

    def br(self, x, y):  # psi coordinates
        return self.psi(self.brt(self.psinv(x), self.psinv(y)))

    def elements(self):
        return [self.psi(t) for t in product(*[range(self.p ** a) for a in self.exps])]


def closure_subring(L, gens):
    S = {tuple([0] * L.m)}
    todo = [tuple(g) for g in gens]
    gens_all = []
    while todo:
        g = todo.pop()
        if g in S and g in gens_all:
            continue
        if g not in gens_all:
            gens_all.append(g)
        newS = span_bf(L.R, gens_all, L.m)
        # brackets of generators
        for a in gens_all:
            for b in gens_all:
                c = L.br(a, b)
                if c not in newS and c not in todo:
                    todo.append(c)
        S = newS
    return S


def hset(L, rows):
    return span_bf(L.R, [r for (_, _, r) in rows], L.m)


def rtf(L, H, solver, checks=True, stats=None, on_socle=None):
    """Algorithm RtF with (N1)-(N6).  H: set (psi-coordinates) of the hidden subring, or None."""
    R, p, e, m, M = L.R, L.p, L.e, L.m, L.M
    Srows, _ = howell(R, [[p ** (e - a) if i == j else 0 for i in range(m)] for j, a in enumerate(L.exps)], m)
    Krows = []
    calls = 0
    b = sum(L.exps)
    while True:
        s = [r for (_, _, r) in Srows]
        kap = [r for (_, _, r) in Krows]
        mu, beta = len(s), len(kap)
        # (N1)
        if all(member(R, Krows, v) is not None for v in s):
            return Krows, calls
        # (N2)
        lk = left_kernel(R, s + kap, m)
        Rgen = [lam[:mu] for lam in lk]
        Rgen = [g for g in Rgen if any(g)]
        P, Q, Qi, dexp = smith_rows(R, Rgen, mu)
        I = [i for i in range(mu) if dexp[i] >= 1]
        u = {i: [sum(Qi[i][j] * s[j][x] for j in range(mu)) % M for x in range(m)] for i in I}

        def coord(y):
            lam = member(R, Srows, y)
            assert lam is not None
            lq = [sum(lam[j] * Q[j][i] for j in range(mu)) % M for i in range(mu)]
            return {i: lq[i] % p ** dexp[i] for i in I}

        cbar = {(i, j): coord(L.br(u[i], u[j])) for i in I for j in I}
        if checks:
            Sset, Kset = hset(L, Srows), hset(L, Krows)
            assert Kset <= Sset
            if H is not None and solver == "truth":
                assert Kset <= H <= Sset, "invariant K <= H <= S"
            for a in Sset:  # K ideal of S (on generators of K)
                for kv in kap:
                    assert L.br(a, kv) in Kset
            order = 1
            for i in I:
                order *= p ** dexp[i]
            assert order * len(Kset) == len(Sset), "|S/K| = prod p^{d_i}"
            # coordinates reproduce y modulo K
            for y in rng.sample(sorted(Sset), min(8, len(Sset))):
                t = coord(y)
                z = [0] * m
                for i in I:
                    z = [(a + t[i] * c) % M for a, c in zip(z, u[i])]
                assert tuple((a - c) % M for a, c in zip(y, z)) in Kset
        # (N3) socle
        m0 = len(I)
        omega = {i: [x * p ** (dexp[i] - 1) % M for x in u[i]] for i in I}
        tensor = {}
        for a, i in enumerate(I):
            for bb, j in enumerate(I):
                vec = []
                for c_, k in enumerate(I):
                    val = (p ** (dexp[i] + dexp[j] - 2) * cbar[i, j][k]) % p ** dexp[k]
                    assert val % p ** (dexp[k] - 1) == 0
                    vec.append(val // p ** (dexp[k] - 1))
                tensor[a, bb] = vec
                if checks:  # compare with the direct bracket of the socle elements
                    direct = coord(L.br(omega[i], omega[j]))
                    dv = []
                    for k in I:
                        assert direct[k] % p ** (dexp[k] - 1) == 0
                        dv.append((direct[k] // p ** (dexp[k] - 1)) % p)
                    assert dv == [x % p for x in vec], "(N3) tensor formula"
        if stats is not None:
            stats["max_k_over_rank"] = max(stats.get("max_k_over_rank", 0), m0 - stats["rank"])
            # dim [Omega, Omega] over F_p
            Rp = Ring(p, 1)
            rows_ = [tensor[a, bb] for a in range(m0) for bb in range(m0)]
            hp, _ = howell(Rp, rows_, m0) if m0 else ([], 0)
            stats["max_der_over_R"] = max(stats.get("max_der_over_R", 0), len(hp) - stats["R"])

        if on_socle is not None:
            on_socle(tensor, m0, p)

        def sig_iota(x):
            v = [0] * m
            for a, i in enumerate(I):
                v = [(z + (x[a] % p) * w) % M for z, w in zip(v, omega[i])]
            return tuple(v)

        calls += 1
        # Solve
        if solver == "truth":
            Ub = []
            Uset = []
            for x in product(range(p), repeat=m0):
                if sig_iota(x) in H:
                    Uset.append(x)
            hp, _ = howell(Ring(p, 1), [list(x) for x in Uset], m0) if m0 else ([], 0)
            Ub = [r for (_, _, r) in hp]
        else:
            cnt = rng.randrange(0, m0 + 2)
            Ub = [[rng.randrange(p) for _ in range(m0)] for _ in range(cnt)]
            if len(Ub) > m0:
                Ub = []  # "returns more than dim Omega vectors counts as returning nothing"
        # (N4) stop rule 2
        Rp = Ring(p, 1)
        hp, _ = howell(Rp, Ub, m0) if (m0 and Ub) else ([], 0)
        basis = [r for (_, _, r) in hp]
        if not basis:
            return Krows, calls

        def tbr(x, y):
            out = [0] * m0
            for a in range(m0):
                if x[a]:
                    for bb in range(m0):
                        if y[bb]:
                            out = [(o + x[a] * y[bb] * t) % p for o, t in zip(out, tensor[a, bb])]
            return out

        closed = all(member(Rp, hp, tbr(x, y)) is not None for x in basis for y in basis)
        if not closed:
            return Krows, calls
        # (N5) K' = q^{-1}(U)
        Kp_rows, _ = howell(R, kap + [list(sig_iota(x)) for x in basis], m)
        kp = [r for (_, _, r) in Kp_rows]
        # (N6) idealizer via theta
        P2, Q2, Q2i, aexp = smith_rows(R, kp, m)

        def theta(v):
            vq = [sum(v[i] * Q2[i][l] for i in range(m)) % M for l in range(m)]
            return [p ** (e - aexp[l]) * vq[l] % M for l in range(m)]

        rows_ = []
        for i in range(mu):
            row = []
            for kv in kp:
                row += theta(L.br(s[i], kv))
            rows_.append(row)
        lk2 = left_kernel(R, rows_, len(kp) * m) if kp else [[1 if a == b_ else 0 for b_ in range(mu)] for a in range(mu)]
        img = [[sum(lam[i] * s[i][x] for i in range(mu)) % M for x in range(m)] for lam in lk2]
        Sp_rows, _ = howell(R, img, m)
        if checks:
            Kpset, Sset = hset(L, Kp_rows), hset(L, Srows)
            assert hset(L, Krows) < Kpset, "K strictly inside K'"
            # theta kernel = psi(K')
            for v in rng.sample(L.elements(), min(30, len(L.elements()))):
                assert (not any(theta(v))) == (tuple(v) in Kpset), "theta(v)=0 iff v in K'"
            bf = {y for y in Sset if all(L.br(y, z) in Kpset for z in kp)}
            assert hset(L, Sp_rows) == bf, "(N6) idealizer"
            assert Kpset <= bf
            if H is not None and solver == "truth":
                assert Kpset <= H <= bf
        Krows, Srows = Kp_rows, Sp_rows
        if calls > b:
            raise AssertionError("more than b calls")


NONAB, EXPGT, SIZES = [0], [0], []


def main():
    t0 = time.time()
    cases = [(3, 2, 2, 2), (5, 2, 2, 3), (5, 2, 2, 2), (3, 3, 2, 2), (7, 2, 2, 3), (5, 3, 1, 3), (3, 2, 3, 2)]
    nH = ok = adv = 0
    maxcalls_ratio = 0
    for (p, e, s, c) in cases:
        R = Ring(p, e)
        FL = FreeLieZ(s, c)
        d = FL.d
        made = 0
        tries = 0
        while made < 6 and tries < 200:
            tries += 1
            I_lat = cc.random_ideal(FL, R, rng.randrange(1, 4))
            idx, n = I_lat.index(), 0
            while idx % p == 0:
                idx //= p
                n += 1
            if not (2 <= n <= 6) or p ** n > 3000:
                continue
            Ncols = cc.dual_generators(I_lat)
            Y = cc.sample_perp(Ncols, R, d, n + 3)
            if cc.span_order(Y, d, R.M) != p ** n:
                continue
            ch = cc.chart(R, FL, Y)
            if max(ch["exps"]) < 2 and e > 1 and rng.random() < 0.7:
                continue  # prefer exponent > p
            L = Chart(p, ch["exps"], ch["c"])
            elems = L.elements()
            rank = L.m
            # rank of [L, L]
            der = span_bf(L.R, [L.br(a, b_) for a in [L.psi([1 if t == i else 0 for t in range(L.m)]) for i in range(L.m)]
                                for b_ in [L.psi([1 if t == i else 0 for t in range(L.m)]) for i in range(L.m)]], L.m)
            dh, _ = howell(L.R, [list(x) for x in der], L.m)
            Rk = len([1 for (_, a, _) in dh])  # number of cyclic factors = Howell rows? (upper bound)
            # exact number of cyclic factors of [L,L]: dim of (D/pD)
            Dset = der
            pD = {tuple(x * p % L.M for x in v) for v in Dset}
            import math
            Rk = round(math.log(len(Dset) // len(pD), p)) if Dset else 0
            made += 1
            NONAB[0] += any(any(v) for v in L.cst.values())
            EXPGT[0] += max(L.exps) > 1
            SIZES.append((L.exps, len(elems)))
            Hs = [{tuple([0] * L.m)}, set(elems)]
            for _ in range(6):
                gens = [rng.choice(elems) for _ in range(rng.randrange(1, 3))]
                Hs.append(closure_subring(L, gens))
            for H in Hs:
                stats = {"rank": rank, "R": Rk}
                Kout, calls = rtf(L, H, "truth", True, stats)
                good = hset(L, Kout) == H and calls <= sum(L.exps)
                # enlarging calls <= log_p |H|, plus at most one final call
                import math as _m
                good &= calls <= round(_m.log(len(H), p)) + 1
                good &= stats.get("max_k_over_rank", 0) <= 0 and stats.get("max_der_over_R", 0) <= 0
                nH += 1
                ok += good
                maxcalls_ratio = max(maxcalls_ratio, calls / max(1, sum(L.exps)))
                if not good:
                    log("  FAIL", (p, e, s, c), L.exps, len(H), calls, stats)
            for _ in range(10):
                Kout, calls = rtf(L, None, "adv", True)
                assert calls <= sum(L.exps)
                adv += 1
        log(f"  {(p, e, s, c)}: {made} charts; cumulative truth runs ok {ok}/{nH}, adversarial runs {adv}")
    log(f"charts: {sum(1 for _ in SIZES)}, nonabelian {NONAB[0]}, exponent > p {EXPGT[0]}; (e_i, |L|): {SIZES}")
    log(f"RESULT truth {ok}/{nH}, adversarial {adv} (all within b calls), max calls/b {maxcalls_ratio:.2f}, "
        f"time {time.time() - t0:.1f}s")
    (Path(__file__).resolve().parent / "check_rtf.out").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
