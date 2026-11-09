"""Exact checks for the free-coordinate kernel sampler (FCS), Schedule 3 replacement.

Companion to research/audits/reviews/2026-11-02-rees-schedule3-cost.md.

Notation: kappa | p-1, h = (p-1)/kappa, P = kappa-th powers in F_p^x (|P| = h), D = P u {0},
q = (h+1)/p = Pr[uniform element of F_p lies in D].

FCS at one node: RREF of the measured label matrix, rank r, pivots p_1 < ... < p_r.
Free set F' = columns after p_r (n' = M - p_r of them; abort if n' < n0).  A trial draws
x uniform in P^{n'}, sets y = x on F', 0 on the other free columns, and y_{p_i} = (C x)_i with
C = -R[:, F'].  Accept iff every y_{p_i} lies in D.

Parts
  A  exhaustive over all C in F_p^{r x n}: E N = h^n q^r, Var N <= h E N, bad fraction <= 4/mu,
     and the oblivious identity Pr_C[C x in D^r] = q^r for every fixed x != 0.
  B  exhaustive over all banks A in F_p^{a x M}: pivot-pattern uniformity of R[:, F'], exact
     per-bank acceptance, bad-bank fraction against the public bound beta.
  C  end-to-end on random label banks (labels uniform on a random subspace V of F_p^g): FCS plus
     kappa-th roots and the Bezout lift, verified at the true degree d; trial counts against 1/q^r;
     the original uniform-kernel design's acceptance on the same banks.
  D  two-level FCS: exact law of the level-one outputs (uniform on V cap ker pi2) and end-to-end
     witnesses at degree d.
"""
from fractions import Fraction as Fr
from itertools import product
from math import gcd
import random
import sys

import numpy as np
from sympy.ntheory.residue_ntheory import nthroot_mod


def powers(p, k):
    return sorted({pow(b, k, p) for b in range(1, p)})


def in_D_table(p, k):
    P = set(powers(p, k))
    return np.array([1 if (v == 0 or v in P) else 0 for v in range(p)], dtype=np.int64)


def rref(A, p):
    """Row-reduce a list-of-rows matrix mod p. Returns (R rows (r of them), pivots)."""
    A = [list(row) for row in A]
    nr, nc = len(A), len(A[0]) if A else 0
    piv, row = [], 0
    for col in range(nc):
        sel = next((i for i in range(row, nr) if A[i][col] % p), None)
        if sel is None:
            continue
        A[row], A[sel] = A[sel], A[row]
        inv = pow(A[row][col], p - 2, p)
        A[row] = [(v * inv) % p for v in A[row]]
        for i in range(nr):
            if i != row and A[i][col] % p:
                f = A[i][col]
                A[i] = [(vi - f * vr) % p for vi, vr in zip(A[i], A[row])]
        piv.append(col)
        row += 1
        if row == nr:
            break
    return A[:row], piv


def mu_bound(p, k, n0, a):
    h = (p - 1) // k
    q = Fr(h + 1, p)
    return Fr(h) ** (n0 - 1) * q ** a


def beta_bound(p, k, n0, a, M):
    """Public per-node bank bound: 4/mu + Pr[rank of first M-n0 columns < a]."""
    L = M - n0
    return 4 / mu_bound(p, k, n0, a) + Fr(p ** a - 1, (p - 1) * p ** L)


# ---------------------------------------------------------------- Part A
def part_A():
    print("== Part A: exhaustive over C in F_p^{r x n}")
    cases = [(5, 2, 1, 3), (5, 2, 2, 3), (7, 2, 1, 3), (7, 2, 2, 3), (7, 3, 2, 3), (7, 3, 3, 2),
             (11, 2, 2, 2), (11, 5, 2, 3), (13, 3, 2, 2), (13, 4, 1, 3), (13, 2, 2, 2), (13, 6, 2, 2)]
    for p, k, r, n in cases:
        h = (p - 1) // k
        q = Fr(h + 1, p)
        inD = in_D_table(p, k)
        P = powers(p, k)
        X = np.array(list(product(P, repeat=n)), dtype=np.int64)          # h^n x n
        allC = np.array(list(product(range(p), repeat=r * n)), dtype=np.int64).reshape(-1, r, n)
        Y = np.einsum("crn,xn->crx", allC, X) % p                          # (#C, r, h^n)
        ok = inD[Y].prod(axis=1)                                             # (#C, h^n)
        N = ok.sum(axis=1)
        tot = len(allC)
        EN = Fr(int(N.sum()), tot)
        EN2 = Fr(int((N * N).sum()), tot)
        Var = EN2 - EN * EN
        pred = Fr(h) ** n * q ** r
        mu = EN / h
        bad = sum(1 for v in N.tolist() if Fr(v) < EN / 2)
        assert EN == pred, (p, k, r, n, EN, pred)
        assert Var <= h * EN
        assert Fr(bad, tot) <= 4 / mu or 4 / mu >= 1
        # oblivious identity, for fixed x != 0 (in P^n and outside it)
        xs = [tuple(X[0]), tuple(X[-1]), tuple([1] + [0] * (n - 1)), tuple(range(1, n + 1)),
              tuple([p - 1] * n)]
        for x in xs:
            xv = np.array(x, dtype=np.int64)
            frac = Fr(int(inD[(allC @ xv) % p].prod(axis=1).sum()), tot)
            assert frac == q ** r, (x, frac, q ** r)
        print(f"   p={p:2d} kappa={k} h={h:2d} r={r} n={n}: #C={tot:6d} E N={float(EN):8.3f} (= h^n q^r exact) "
              f"Var={float(Var):8.3f} <= h E N={float(h * EN):8.3f}; bad fraction={bad / tot:.4f} "
              f"vs 4/mu={float(4 / mu):.3f}; oblivious Pr_C[Cx in D^r]=q^r={float(q ** r):.4f} for {len(xs)} x")


# ---------------------------------------------------------------- Part B
def accept_count(Cmat, p, k, inD, cache):
    r = len(Cmat)
    n = len(Cmat[0]) if r else 0
    key = (n,)
    if key not in cache:
        cache[key] = np.array(list(product(powers(p, k), repeat=n)), dtype=np.int64)
    X = cache[key]
    if r == 0:
        return len(X), len(X)
    C = np.array(Cmat, dtype=np.int64)
    ok = inD[(C @ X.T) % p].prod(axis=0)
    return int(ok.sum()), len(X)


def part_B():
    print("== Part B: exhaustive over all banks A in F_p^{a x M} (columns i.i.d. uniform)")
    cases = [(5, 2, 1, 4, 2), (7, 3, 1, 4, 2), (7, 2, 1, 5, 3), (11, 2, 1, 4, 2), (5, 2, 2, 4, 2),
             (13, 2, 1, 5, 3), (31, 3, 1, 4, 3)]
    for p, k, a, M, n0 in cases:
        h = (p - 1) // k
        q = Fr(h + 1, p)
        inD = in_D_table(p, k)
        cache = {}
        tot = p ** (a * M)
        pivfail = bad = nowit = 0
        minacc = Fr(1)
        cell = {}  # (pivots) -> counts of R[:, F'] tuples, for uniformity
        for flat in product(range(p), repeat=a * M):
            A = [list(flat[i * M:(i + 1) * M]) for i in range(a)]
            R, piv = rref(A, p)
            r = len(piv)
            last = piv[-1] if piv else -1
            nprime = M - 1 - last
            if nprime < n0:
                pivfail += 1
                continue
            Cm = [[(-R[i][j]) % p for j in range(last + 1, M)] for i in range(r)]
            cell.setdefault(tuple(piv), {}).setdefault(tuple(map(tuple, Cm)), 0)
            cell[tuple(piv)][tuple(map(tuple, Cm))] += 1
            Nacc, Nx = accept_count(Cm, p, k, inD, cache)
            acc = Fr(Nacc, Nx)
            minacc = min(minacc, acc)
            if Nacc == 0:
                nowit += 1
            if acc < q ** r / 2:
                bad += 1
        # uniformity of R[:, F'] given the pivot pattern
        unif = True
        for piv, d in cell.items():
            r = len(piv)
            n = M - 1 - (piv[-1] if piv else -1)
            if len(d) != p ** (r * n) or len(set(d.values())) != 1:
                unif = False
        beta = beta_bound(p, k, n0, a, M)
        frac = Fr(pivfail + bad, tot)
        flag = frac <= beta
        print(f"   p={p:2d} kappa={k} a={a} M={M} n0={n0}: banks={tot:7d} pivot-fail={pivfail} "
              f"low-acceptance={bad} no-witness={nowit}; bad fraction={float(frac):.4f} <= beta={float(beta):.3f}: {flag}; "
              f"R[:,F'] uniform per pivot pattern: {unif}; min acceptance (non-failed)={float(minacc):.4f} vs q^a/2={float(q ** a / 2):.4f}")
        assert unif and flag


def part_B2(rng):
    print("== Part B2: random banks, exact per-bank acceptance (enumerating all x in P^{n'})")
    cases = [(13, 3, 2, 7, 5, 4000), (13, 2, 2, 6, 4, 4000), (31, 3, 2, 6, 4, 4000), (7, 2, 3, 9, 6, 2000),
             (61, 6, 2, 6, 4, 4000), (31, 5, 3, 8, 5, 1500)]
    for p, k, a, M, n0, nb in cases:
        h = (p - 1) // k
        q = Fr(h + 1, p)
        inD = in_D_table(p, k)
        cache = {}
        pivfail = bad = 0
        accs = []
        for _ in range(nb):
            A = [[rng.randrange(p) for _ in range(M)] for _ in range(a)]
            R, piv = rref(A, p)
            r = len(piv)
            last = piv[-1] if piv else -1
            if M - 1 - last < n0:
                pivfail += 1
                continue
            Cm = [[(-R[i][j]) % p for j in range(last + 1, M)] for i in range(r)]
            Nacc, Nx = accept_count(Cm, p, k, inD, cache)
            acc = Fr(Nacc, Nx)
            accs.append(float(acc / q ** r))
            if acc < q ** r / 2:
                bad += 1
        beta = beta_bound(p, k, n0, a, M)
        frac = (pivfail + bad) / nb
        print(f"   p={p:2d} kappa={k} a={a} M={M} n0={n0}: {nb} banks; pivot-fail={pivfail} low-acceptance={bad}; "
              f"bad fraction={frac:.4f} vs beta={float(beta):.4f}; acceptance/q^r: mean {sum(accs) / len(accs):.3f} "
              f"min {min(accs):.3f}")


# ---------------------------------------------------------------- samplers
def random_subspace(p, g, a, rng):
    while True:
        E = [[rng.randrange(p) for _ in range(a)] for _ in range(g)]
        Et = [[E[i][j] for i in range(g)] for j in range(a)]
        if len(rref(Et, p)[1]) == a:
            return E  # g x a, columns span V


def bank(p, E, M, rng):
    g, a = len(E), len(E[0])
    cols = []
    for _ in range(M):
        al = [rng.randrange(p) for _ in range(a)]
        cols.append([sum(E[i][j] * al[j] for j in range(a)) % p for i in range(g)])
    return cols  # M columns in F_p^g


def fcs(cols, p, k, n0, rng, cap):
    """Free-coordinate sampler on columns (each in F_p^g). Returns (y, trials) or (None, trials)."""
    M, g = len(cols), len(cols[0])
    Lam = [[cols[j][i] for j in range(M)] for i in range(g)]
    R, piv = rref(Lam, p)
    r = len(piv)
    last = piv[-1] if piv else -1
    Fp = list(range(last + 1, M))
    if len(Fp) < n0:
        return None, 0
    h = (p - 1) // k
    for t in range(1, cap + 1):
        x = [pow(rng.randrange(1, p), k, p) for _ in Fp]
        y = [0] * M
        for j, xv in zip(Fp, x):
            y[j] = xv
        good = True
        for i, pc in enumerate(piv):
            v = (-sum(R[i][j] * xv for j, xv in zip(Fp, x))) % p
            if v and pow(v, h, p) != 1:
                good = False
                break
            y[pc] = v
        if good:
            return y, t
    return None, cap


def lift(y, p, d):
    """kappa-th roots and Bezout lift: s with s_i^d = y_i."""
    k = gcd(d, p - 1)
    h = (p - 1) // k
    t = pow((d // k) % h, -1, h) if h > 1 else 1
    s = []
    for v in y:
        if v == 0:
            s.append(0)
            continue
        sig = nthroot_mod(v, k, p) if k > 1 else v
        assert pow(sig, k, p) == v
        s.append(pow(sig, t, p))
    return s


def check_witness(cols, s, p, d):
    g = len(cols[0])
    assert any(s)
    for i in range(g):
        assert sum(pow(si, d, p) * c[i] for si, c in zip(s, cols)) % p == 0


def old_design_acceptance(cols, p, k, rng, trials):
    """Original Schedule 3: uniform kernel vector, accept if nonzero and every entry in D."""
    M, g = len(cols), len(cols[0])
    Lam = [[cols[j][i] for j in range(M)] for i in range(g)]
    R, piv = rref(Lam, p)
    free = [j for j in range(M) if j not in piv]
    h = (p - 1) // k
    acc = 0
    for _ in range(trials):
        x = {j: rng.randrange(p) for j in free}
        y = [0] * M
        for j in free:
            y[j] = x[j]
        for i, pc in enumerate(piv):
            y[pc] = (-sum(R[i][j] * x[j] for j in free)) % p
        if any(y) and all(v == 0 or pow(v, h, p) == 1 for v in y):
            acc += 1
    return acc / trials


def part_C(rng):
    print("== Part C: end-to-end FCS on random banks (labels uniform on a random a-dim V in F_p^g)")
    cases = [(13, 4, 4, 3, 7, 3), (31, 3, 5, 4, 8, 3), (61, 6, 4, 3, 7, 3), (1031, 2, 6, 5, 8, 2),
             (2521, 5, 5, 4, 7, 2), (2521, 9, 3, 2, 5, 2), (7, 2, 4, 3, 9, 5), (5, 2, 3, 3, 9, 6),
             (2521, 4, 8, 8, 11, 2), (11, 5, 3, 2, 8, 4)]
    for p, d, g, a, M, n0 in cases:
        k = gcd(d, p - 1)
        h = (p - 1) // k
        q = (h + 1) / p
        E = random_subspace(p, g, a, rng)
        nb, tr, fails, olds = 40, [], 0, []
        for b in range(nb):
            cols = bank(p, E, M, rng)
            y, t = fcs(cols, p, k, n0, rng, cap=200000)
            if y is None:
                fails += 1
                continue
            s = lift(y, p, d)
            check_witness(cols, s, p, d)
            tr.append(t)
            if b < 8 and M <= 9:
                olds.append(old_design_acceptance(cols, p, k, rng, 20000))
        mean = sum(tr) / len(tr)
        oldtxt = (f"; original design acceptance (MC, 8 banks x 2e4) mean {sum(olds) / len(olds):.2e} vs q^M={q ** M:.2e}"
                  if olds else "")
        beta = float(min(1, beta_bound(p, k, n0, a, M)))
        print(f"   p={p:5d} d={d} kappa={k} g={g} a={a} M={M} n0={n0} (bank bound beta={beta:.3f}): {nb - fails}/{nb} banks gave a witness "
              f"verified at degree d; mean trials {mean:8.2f} vs 1/q^a={1 / q ** a:8.2f} (kappa^a={k ** a}){oldtxt}")


# ---------------------------------------------------------------- Part D
def fcs2(cols, p, k, g2, M1, n01, n02, rng, cap):
    """Two-level FCS. Level one: blocks of M1 columns solved on the first g2 coordinates.
    Level two: FCS on the block outputs w_k (which lie in V cap ker pi2)."""
    M = len(cols)
    blocks = [cols[i:i + M1] for i in range(0, M, M1)]
    ws, ys, trials = [], [], 0
    for blk in blocks:
        proj = [c[:g2] for c in blk]
        y, t = fcs(proj, p, k, n01, rng, cap)
        trials += t
        if y is None:
            return None, trials
        ys.append(y)
        ws.append([sum(yi * c[i] for yi, c in zip(y, blk)) % p for i in range(len(blk[0]))])
    z, t = fcs(ws, p, k, n02, rng, cap)
    trials += t
    if z is None:
        return None, trials
    out = []
    for zk, y in zip(z, ys):
        out.extend((zk * yi) % p for yi in y)
    return out, trials


def part_D(rng):
    print("== Part D: two-level FCS")
    # exact law of a level-one output: p=5, kappa=2, V=F_5^2 (a=2), pi2 = first coordinate,
    # block of M1=3 columns, n0=2.  Enumerate all banks and all accepted x (first acceptance
    # is uniform on the accepted set).  w must be uniform on V cap ker pi2 = {(0, v)}.
    for p, k, M1, n0 in [(5, 2, 3, 2), (7, 3, 3, 2), (7, 2, 3, 2), (11, 2, 3, 2)]:
        P = powers(p, k)
        dist = {}
        per_gamma_ok = True
        for gam in product(range(p), repeat=M1):           # first coordinates (pi2 part)
            R, piv = rref([list(gam)], p)
            last = piv[-1] if piv else -1
            Fp = list(range(last + 1, M1))
            if len(Fp) < n0:
                continue
            acc = []
            for x in product(P, repeat=len(Fp)):
                y = [0] * M1
                for j, xv in zip(Fp, x):
                    y[j] = xv
                good = True
                for i, pc in enumerate(piv):
                    v = (-sum(R[i][j] * xv for j, xv in zip(Fp, x))) % p
                    if v and v not in P:
                        good = False
                        break
                    y[pc] = v
                if good:
                    acc.append(y)
            if not acc:
                continue
            loc = {}
            for bet in product(range(p), repeat=M1):           # second coordinates (V1 part)
                for y in acc:
                    w = sum(yi * bi for yi, bi in zip(y, bet)) % p
                    loc[w] = loc.get(w, 0) + Fr(1, len(acc))
            vals = set(loc.values())
            if len(loc) != p or len(vals) != 1:
                per_gamma_ok = False
            for w, c in loc.items():
                dist[w] = dist.get(w, 0) + c
        print(f"   exact law p={p} kappa={k} M1={M1} n0={n0}: level-one output second coordinate uniform on F_p "
              f"for every first-coordinate bank with a witness: {per_gamma_ok}")
        assert per_gamma_ok
    cases = [(2521, 4, 6, 6, 3, 6, 2, 6, 2), (1031, 2, 8, 8, 4, 7, 2, 7, 2), (61, 6, 4, 4, 2, 5, 2, 5, 2),
             (2521, 5, 6, 5, 3, 6, 2, 6, 2)]
    for p, d, g, a, g2, M1, n01, M2, n02 in cases:
        k = gcd(d, p - 1)
        h = (p - 1) // k
        q = (h + 1) / p
        E = random_subspace(p, g, a, rng)
        nb, tr, fails = 20, [], 0
        for _ in range(nb):
            cols = bank(p, E, M1 * M2, rng)
            y, t = fcs2(cols, p, k, g2, M1, n01, n02, rng, cap=200000)
            if y is None:
                fails += 1
                continue
            s = lift(y, p, d)
            check_witness(cols, s, p, d)
            tr.append(t)
        print(f"   p={p:5d} d={d} kappa={k} g={g} a={a} split {g2}+{g - g2} arity {M1}x{M2}={M1 * M2}: "
              f"{nb - fails}/{nb} witnesses verified at degree d; mean trials {sum(tr) / len(tr):8.1f} "
              f"vs single-level 1/q^a={1 / q ** a:8.1f}")


if __name__ == "__main__":
    rng = random.Random(20261102)
    part_A()
    sys.stdout.flush()
    part_B()
    sys.stdout.flush()
    part_B2(rng)
    sys.stdout.flush()
    part_C(rng)
    sys.stdout.flush()
    part_D(rng)
    print("ALL CHECKS PASSED")
