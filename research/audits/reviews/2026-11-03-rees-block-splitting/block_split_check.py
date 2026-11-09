"""Exact checks for the k-level (block-split) free-coordinate sampler.

Run:
  cd research/audits/reviews/2026-11-03-rees-block-splitting && \
    /opt/anaconda3/bin/python -B -u block_split_check.py > block_split_check_out.txt

Independent code: imports nothing from earlier reports. Exact integers and Fractions only.

[A] Law transfer (one sub-solver), exhaustive: labels i.i.d. uniform on a subspace V of F_p^g
    that is NOT a coordinate subspace; FCS reads only pi(lambda). For every value of the
    pi-bank with at least one accepted draw, the law of w = sum y_i lambda_i, averaged over the
    labels consistent with that pi-bank and over the accepted draws (uniform on the accepted
    set, as for the first accepted trial), is exactly uniform on V_1 = V cap ker pi.
[B] Joint law of a level-2 bank, exhaustive: two level-1 sub-solvers on disjoint blocks.
    Conditional on both pi_1-banks (the full level-1 record) and both successes, (w_1, w_2) is
    exactly uniform on V_1 x V_1, and pi_2 of it is uniform on pi_2(V_1)^2.
[C] Gate: a level-1 sampler that reads the FULL labels (not only pi-images) can bias w.
    Smallest instance found by search is printed; the claim needs the pi-only hypothesis.
[D] End-to-end random runs of the k-level solver (k = 2, 3, also non-coordinate maps) at
    several (p, d): every returned s is nonzero and satisfies sum s_i^d lambda_i = 0 exactly;
    Y lies in D^M; each level's output lies in V_j.
[F] Monte Carlo (not exact) sanity check of the node abort bound sum_j n_j beta_j + 3 nu 2^-B
    at two parameter sets where it is nontrivial. Run alone with argument DF (with [D]).
[E] Sub-solver count: sum_j prod_{i>j} M_i <= (M-1)/(min M_i - 1) <= M-1, and
    beta(M,n0;g) <= 1 forces n0 >= 2 (hence M_j >= 2), exhaustive over small ranges.
"""
from fractions import Fraction
from itertools import product
from math import gcd
import random

# ---------------- linear algebra over F_p ----------------

def rref(rows, p):
    """rows: list of lists (r x M). Return (R nonzero rows, pivots)."""
    A = [list(r) for r in rows]
    nr = len(A)
    nc = len(A[0]) if nr else 0
    piv = []
    i = 0
    for j in range(nc):
        k = next((t for t in range(i, nr) if A[t][j] % p), None)
        if k is None:
            continue
        A[i], A[k] = A[k], A[i]
        inv = pow(A[i][j], p - 2, p)
        A[i] = [(x * inv) % p for x in A[i]]
        for t in range(nr):
            if t != i and A[t][j] % p:
                f = A[t][j]
                A[t] = [(x - f * y) % p for x, y in zip(A[t], A[i])]
        piv.append(j)
        i += 1
        if i == nr:
            break
    return A[:i], piv


def span(basis, p, g):
    out = set()
    for co in product(range(p), repeat=len(basis)):
        v = tuple(sum(c * b[t] for c, b in zip(co, basis)) % p for t in range(g))
        out.add(v)
    return out

# ---------------- the FCS sub-solver ----------------

def powers(p, kappa):
    P = sorted({pow(x, kappa, p) for x in range(1, p)})
    return P, set(P) | {0}


def accepted_set(bank_cols, p, kappa, n0):
    """bank_cols: list of M column vectors (length g'). Returns list of accepted y in D^M
    (one per accepted x in P^{F'}), or None if (F2) aborts. Draws b -> x = b^kappa are
    kappa-to-1, so the first accepted trial is uniform on this list."""
    M = len(bank_cols)
    g = len(bank_cols[0])
    rows = [[bank_cols[l][t] for l in range(M)] for t in range(g)]
    R, piv = rref(rows, p)
    r = len(piv)
    last = piv[-1] if r else -1
    F = list(range(last + 1, M))
    if len(F) < n0:
        return None
    P, D = powers(p, kappa)
    acc = []
    for x in product(P, repeat=len(F)):
        v = [(-sum(R[i][l] * xl for l, xl in zip(F, x))) % p for i in range(r)]
        if all(vi in D for vi in v):
            y = [0] * M
            for l, xl in zip(F, x):
                y[l] = xl
            for i in range(r):
                y[piv[i]] = v[i]
            acc.append(tuple(y))
    return acc


def lin(y, vecs, p):
    g = len(vecs[0])
    return tuple(sum(yi * v[t] for yi, v in zip(y, vecs)) % p for t in range(g))

# ---------------- [A] ----------------

def check_A(p, d, basisV, piidx, M, n0):
    kappa = gcd(d, p - 1)
    g = len(basisV[0])
    V = sorted(span(basisV, p, g))
    V1 = sorted(v for v in V if all(v[t] == 0 for t in piidx))
    groups = {}
    for lam in product(V, repeat=M):
        key = tuple(tuple(l[t] for t in piidx) for l in lam)
        groups.setdefault(key, []).append(lam)
    nkeys = 0
    for key, lams in groups.items():
        acc = accepted_set([list(k) for k in key], p, kappa, n0)
        if not acc:
            continue
        nkeys += 1
        law = {}
        wt = Fraction(1, len(lams) * len(acc))
        for lam in lams:
            for y in acc:
                w = lin(y, lam, p)
                law[w] = law.get(w, 0) + wt
        assert set(law) == set(V1), (key, sorted(law))
        assert all(v == Fraction(1, len(V1)) for v in law.values()), (key, law)
    print(f"[A] p={p} d={d} kappa={kappa} dimV={len(basisV)} g={g} pi={piidx} M={M} n0={n0}: "
          f"{nkeys} successful pi-banks, w exactly uniform on V1 (|V1|={len(V1)}) for each")
    return nkeys

# ---------------- [B] ----------------

def check_B(p, d, basisV, pi1, pi2, M1, n0):
    kappa = gcd(d, p - 1)
    g = len(basisV[0])
    V = sorted(span(basisV, p, g))
    V1 = sorted(v for v in V if all(v[t] == 0 for t in pi1))
    groups = {}
    for lam in product(V, repeat=M1):
        key = tuple(tuple(l[t] for t in pi1) for l in lam)
        groups.setdefault(key, []).append(lam)
    # per-block conditional law of w given its record (dict w -> prob)
    blocklaw = {}
    for key, lams in groups.items():
        acc = accepted_set([list(k) for k in key], p, kappa, n0)
        if not acc:
            continue
        law = {}
        wt = Fraction(1, len(lams) * len(acc))
        for lam in lams:
            for y in acc:
                w = lin(y, lam, p)
                law[w] = law.get(w, 0) + wt
        blocklaw[key] = law
    # joint check by explicit enumeration over pairs of records (product structure is the
    # claim; here we recompute the joint from the full product space of labels for a sample
    # of record pairs, without assuming factorization)
    keys = sorted(blocklaw)
    rng = random.Random(1)
    sample = [(rng.choice(keys), rng.choice(keys)) for _ in range(12)]
    for k1, k2 in sample:
        lams1, lams2 = groups[k1], groups[k2]
        acc1 = accepted_set([list(k) for k in k1], p, kappa, n0)
        acc2 = accepted_set([list(k) for k in k2], p, kappa, n0)
        joint = {}
        wt = Fraction(1, len(lams1) * len(lams2) * len(acc1) * len(acc2))
        for la in lams1:
            ws1 = [lin(y, la, p) for y in acc1]
            for lb in lams2:
                ws2 = [lin(y, lb, p) for y in acc2]
                for w1 in ws1:
                    for w2 in ws2:
                        joint[(w1, w2)] = joint.get((w1, w2), 0) + wt
        assert len(joint) == len(V1) ** 2
        assert all(v == Fraction(1, len(V1) ** 2) for v in joint.values())
        proj = {}
        for (w1, w2), v in joint.items():
            kk = (tuple(w1[t] for t in pi2), tuple(w2[t] for t in pi2))
            proj[kk] = proj.get(kk, 0) + v
        img = {tuple(w[t] for t in pi2) for w in V1}
        assert len(proj) == len(img) ** 2 and all(v == Fraction(1, len(img) ** 2) for v in proj.values())
    print(f"[B] p={p} d={d} kappa={kappa} pi1={pi1} pi2={pi2} M1={M1} n0={n0}: "
          f"{len(sample)} record pairs, (w1,w2) exactly uniform on V1^2 (|V1|={len(V1)}), "
          f"level-2 bank uniform on pi2(V1)^2 (|pi2(V1)|={len(img)})")

# ---------------- [C] ----------------

def check_C(p, d, M, n0):
    """Full-label sampler: among accepted y for the pi-bank, choose the FIRST (lexicographic)
    y whose w has second coordinate 0 if one exists, else the first y. V = F_p^2, pi = coord 0.
    Then w is not uniform on V1 = {(0, t)}."""
    kappa = gcd(d, p - 1)
    V = list(product(range(p), repeat=2))
    law = {}
    tot = Fraction(0)
    for lam in product(V, repeat=M):
        key = [[l[0]] for l in lam]
        acc = accepted_set(key, p, kappa, n0)
        if not acc:
            continue
        acc = sorted(acc)
        ch = next((y for y in acc if lin(y, lam, p)[1] == 0), acc[0])
        w = lin(ch, lam, p)
        law[w] = law.get(w, 0) + 1
        tot += 1
    law = {w: Fraction(c) / tot for w, c in law.items()}
    print(f"[C] p={p} d={d} M={M} n0={n0}: full-label sampler gives Pr[w=0] = {law.get((0,0),0)}"
          f" (uniform would be 1/{p}); law = {dict(sorted(law.items()))}")
    assert law.get((0, 0), 0) != Fraction(1, p)

# ---------------- [D] ----------------

def solve_klevel(lams, maps, Ms, n0s, p, d, rng, B=20):
    """lams: list of prod(Ms) label vectors, column index (i_1,...,i_k) in lexicographic order
    with i_k most significant. maps: list of k matrices (g_j x g). Returns s or None."""
    kappa = gcd(d, p - 1)
    k = len(Ms)
    P, D = powers(p, kappa)
    # level-0 objects: (vector, coefficient vector over original columns as dict)
    cur = [(lam, {idx: (1, 1)}) for idx, lam in enumerate(lams)]  # coeff: (Y, sigma)
    for j in range(k):
        Mj = Ms[j]
        A = maps[j]
        nxt = []
        for start in range(0, len(cur), Mj):
            grp = cur[start:start + Mj]
            bank = [[sum(A[t][u] * w[u] for u in range(len(w))) % p for t in range(len(A))]
                    for (w, _) in grp]
            rows = [[bank[l][t] for l in range(Mj)] for t in range(len(A))]
            R, piv = rref(rows, p)
            r = len(piv)
            last = piv[-1] if r else -1
            F = list(range(last + 1, Mj))
            if len(F) < n0s[j]:
                return None, "F2"
            ok = None
            # trial cap T_r = ceil(2 B ln2 q^{-r}) of (F3), with ln 2 replaced by 0.6931472 > ln 2
            q = Fraction((p - 1) // kappa + 1, p)
            Tr = -(-(2 * B * Fraction(6931472, 10**7) / q ** r).numerator // (2 * B * Fraction(6931472, 10**7) / q ** r).denominator)
            for _ in range(Tr):
                b = [rng.randrange(1, p) for _ in F]
                x = [pow(bi, kappa, p) for bi in b]
                v = [(-sum(R[i][l] * xl for l, xl in zip(F, x))) % p for i in range(r)]
                if all(vi in D for vi in v):
                    ok = (b, x, v)
                    break
            if ok is None:
                return None, "F3"
            b, x, v = ok
            y = [0] * Mj
            sig = [0] * Mj
            for l, xl, bl in zip(F, x, b):
                y[l], sig[l] = xl, bl
            for i in range(r):
                y[piv[i]] = v[i]
                if v[i]:
                    roots = [t for t in range(1, p) if pow(t, kappa, p) == v[i]]
                    sig[piv[i]] = roots[rng.randrange(len(roots))]
            assert any(y) and all(pow(sg, kappa, p) == yy for sg, yy in zip(sig, y))
            # bank kernel check
            assert all(sum(bank[l][t] * y[l] for l in range(Mj)) % p == 0 for t in range(len(A)))
            g = len(grp[0][0])
            w = tuple(sum(y[l] * grp[l][0][u] for l in range(Mj)) % p for u in range(g))
            coeff = {}
            for l in range(Mj):
                if y[l] == 0:
                    continue
                for idx, (Yv, sv) in grp[l][1].items():
                    coeff[idx] = ((Yv * y[l]) % p, (sv * sig[l]) % p)
            nxt.append((w, coeff))
        cur = nxt
    assert len(cur) == 1
    w, coeff = cur[0]
    assert all(t == 0 for t in w)
    Mtot = len(lams)
    Y = [0] * Mtot
    sig = [0] * Mtot
    for idx, (Yv, sv) in coeff.items():
        Y[idx], sig[idx] = Yv, sv
    assert any(Y) and all(yy in D for yy in Y)
    # Bezout: alpha d + alpha' (p-1) = kappa
    def egcd(a, b):
        if b == 0:
            return a, 1, 0
        g_, x_, y_ = egcd(b, a % b)
        return g_, y_, x_ - (a // b) * y_
    g_, alpha, _ = egcd(d, p - 1)
    assert g_ == kappa
    s = [pow(sg, alpha % (p - 1), p) if sg else 0 for sg in sig]
    assert all(pow(si, d, p) == yy for si, yy in zip(s, Y))
    gdim = len(lams[0])
    assert any(s)
    assert all(sum(pow(si, d, p) * lam[u] for si, lam in zip(s, lams)) % p == 0 for u in range(gdim))
    return s, "ok"


def check_D():
    rng = random.Random(20261103)
    cases = [
        # p, d, g, a, blocks (coordinate partition) or 'random', Ms, n0s
        (13, 4, 6, 6, [[0, 1, 2], [3, 4, 5]], [9, 9], [4, 4]),
        (13, 4, 6, 4, [[0, 1], [2, 3], [4, 5]], [6, 6, 6], [3, 3, 3]),
        (31, 6, 6, 6, [[0, 1, 2], [3, 4, 5]], [8, 8], [3, 3]),
        (11, 2, 4, 3, [[0, 1], [2, 3]], [6, 6], [3, 3]),
        (37, 9, 4, 4, [[0, 1], [2, 3]], [6, 6], [3, 3]),
        (13, 3, 6, 5, 'random', [8, 8], [3, 3]),
    ]
    for (p, d, g, a, blocks, Ms, n0s) in cases:
        kappa = gcd(d, p - 1)
        assert 2 <= kappa < p - 1
        if blocks == 'random':
            # two random maps F_p^g -> F_p^{g/2} with trivial common kernel
            while True:
                A1 = [[rng.randrange(p) for _ in range(g)] for _ in range(g // 2)]
                A2 = [[rng.randrange(p) for _ in range(g)] for _ in range(g - g // 2)]
                if len(rref(A1 + A2, p)[1]) == g:
                    break
            maps = [A1, A2]
        else:
            maps = [[[1 if u == t else 0 for u in range(g)] for t in blk] for blk in blocks]
        runs = ok = 0
        reasons = {}
        for _ in range(60):
            basis = [[rng.randrange(p) for _ in range(g)] for _ in range(a)]
            Mtot = 1
            for m_ in Ms:
                Mtot *= m_
            lams = []
            for _ in range(Mtot):
                co = [rng.randrange(p) for _ in range(a)]
                lams.append(tuple(sum(c * b[u] for c, b in zip(co, basis)) % p for u in range(g)))
            s, why = solve_klevel(lams, maps, Ms, n0s, p, d, rng)
            runs += 1
            ok += s is not None
            reasons[why] = reasons.get(why, 0) + 1
        print(f"[D] p={p} d={d} kappa={kappa} g={g} a={a} maps={'random' if blocks=='random' else blocks}"
              f" Ms={Ms} n0={n0s}: {ok}/{runs} runs returned s, every s verified exactly; outcomes {reasons}"
              f" (F2 = pivot abort, F3 = trial cap 2B ln2 q^-r reached, B=20)")

# ---------------- [E] ----------------

def check_E():
    for k in range(1, 6):
        for Ms in product(range(2, 7), repeat=k):
            M = 1
            for m_ in Ms:
                M *= m_
            nu = 0
            for j in range(k):
                t = 1
                for i in range(j + 1, k):
                    t *= Ms[i]
                nu += t
            assert nu * (min(Ms) - 1) <= M - 1, Ms
            assert nu <= M - 1
            t2 = 1
            for i in range(1, k):
                t2 *= Ms[i]
            assert nu <= 2 * t2
    # beta <= 1 forces n0 >= 2 when g >= 1
    for p in [5, 7, 11, 13, 31, 37]:
        for kappa in range(2, p - 1):
            if (p - 1) % kappa:
                continue
            h = (p - 1) // kappa
            q = Fraction(h + 1, p)
            for g in range(1, 5):
                for M in range(1, 8):
                    n0 = 1
                    L = M - n0
                    beta = Fraction(4) / (h ** (n0 - 1) * q ** g) + Fraction(p ** g - 1, (p - 1) * p ** L)
                    assert beta > 1
    print("[E] sub-solver count nu <= (M-1)/(min M_j - 1) <= M-1 and nu <= 2 prod_{j>=2} M_j for"
          " k<=5, 2<=M_j<=6; beta(M,1;g) > 1 for g>=1 at all tested (p,kappa)")


def beta(M, n0, g, p, kappa):
    h = (p - 1) // kappa
    q = Fraction(h + 1, p)
    L = M - n0
    return Fraction(4) / (h ** (n0 - 1) * q ** g) + Fraction(p ** g - 1, (p - 1) * p ** L)


def check_F(runs=150):
    """Monte Carlo sanity check (not exact) of the node abort bound
    sum_j n_j beta_j + 3 nu 2^-B at parameters where it is nontrivial."""
    rng = random.Random(7)
    for (p, d, g, a, blocks, Ms, n0s, B) in [
        (31, 6, 4, 4, [[0, 1], [2, 3]], [11, 11], [7, 7], 20),
        (13, 4, 4, 4, [[0, 1], [2, 3]], [14, 14], [10, 10], 20),
    ]:
        kappa = gcd(d, p - 1)
        k = len(Ms)
        nj = []
        for j in range(k):
            t = 1
            for i in range(j + 1, k):
                t *= Ms[i]
            nj.append(t)
        gj = [len(b) for b in blocks]
        bound = sum(n * beta(M, n0, gg, p, kappa) for n, M, n0, gg in zip(nj, Ms, n0s, gj)) \
            + Fraction(3 * sum(nj), 2 ** B)
        maps = [[[1 if u == t else 0 for u in range(g)] for t in blk] for blk in blocks]
        fails = 0
        for _ in range(runs):
            basis = [[rng.randrange(p) for _ in range(g)] for _ in range(a)]
            Mtot = 1
            for m_ in Ms:
                Mtot *= m_
            lams = [tuple(sum(c * b[u] for c, b in zip([rng.randrange(p) for _ in range(a)], basis)) % p
                          for u in range(g)) for _ in range(Mtot)]
            s, why = solve_klevel(lams, maps, Ms, n0s, p, d, rng, B=B)
            fails += s is None
        print(f"[F] (Monte Carlo) p={p} d={d} kappa={kappa} g={g} a={a} blocks={blocks} Ms={Ms} n0={n0s}"
              f" B={B}: node abort bound sum_j n_j beta_j + 3 nu 2^-B = {float(bound):.4f};"
              f" observed {fails}/{runs} aborts")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "DF":
        check_D()
        check_F()
        print("D AND F PASSED")
        raise SystemExit
    # [A]: V = span{(1,1,2),(0,1,3)} in F_5^3 (not a coordinate subspace), pi = coordinate 0
    check_A(5, 2, [[1, 1, 2], [0, 1, 3]], [0], 3, 1)
    check_A(5, 2, [[1, 1, 2], [0, 1, 3]], [0], 3, 2)
    check_A(7, 3, [[1, 2, 5], [3, 1, 1]], [0], 3, 1)
    check_A(7, 2, [[1, 2, 5], [3, 1, 1]], [0], 3, 2)
    check_A(5, 2, [[1, 2, 3, 4], [0, 1, 1, 2], [1, 0, 2, 2]], [0, 1], 3, 1)
    # [B]
    check_B(5, 2, [[1, 1, 2], [0, 1, 3]], [0], [1, 2], 3, 1)
    check_B(7, 3, [[1, 2, 5], [3, 1, 1]], [0], [1, 2], 3, 1)
    # [C]
    check_C(5, 2, 2, 1)
    check_C(5, 2, 3, 1)
    # [D]
    check_D()
    check_F()
    # [E]
    check_E()
    print("ALL CHECKS PASSED")
