"""Item 7(b): exact checks of Proposition conjugation and Remark filters.

All arithmetic is exact over F_p (numpy int64 with explicit reduction, or
Python integers / Fractions). Run from the repo root:

    /opt/anaconda3/bin/python -B research/audits/reviews/2026-11-02-rees-compilation-filters/classical_filters_check.py

Sections:
 A. exp(x) M exp(-x) versus exp(ad_x) M over F_p (the 10-31 correction):
    exact witness for EVERY N <= p <= 2N-2 (N = 2..7), identity for p >= 2N-1.
 B. Proposition conjugation: brute-force stabilizers and transporters versus
    the linear-algebra formula, exhaustive where feasible.
 C. Same commutant argument for the anchored 2-jet quadratic stabilizer with
    SINGULAR B in the range N <= p < 2N-1.
 D. Remark (ii) controls: the UT_4(F_5) cubic (Delta < p is not enough) and a
    non-fixed anchor whose 2-jet "certifies" H = 1 although H = G.
"""
import itertools
import random
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

import numpy as np

rng = random.Random(1102)


def primes_upto(n):
    return [q for q in range(2, n + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1))]


def mm(A, B, p):
    return (A @ B) % p


def mexp(X, p):
    N = X.shape[0]
    out, power = np.eye(N, dtype=np.int64), np.eye(N, dtype=np.int64)
    for j in range(1, N):
        power = mm(power, X, p)
        out = (out + power * pow(factorial(j), -1, p)) % p
    return out


def mlog(G, p):
    N = G.shape[0]
    Y = (G - np.eye(N, dtype=np.int64)) % p
    out, power = np.zeros((N, N), dtype=np.int64), np.eye(N, dtype=np.int64)
    for j in range(1, N):
        power = mm(power, Y, p)
        out = (out + power * ((-1) ** (j + 1) * pow(j, -1, p))) % p
    return out


def upper_positions(N):
    return [(i, j) for i in range(N) for j in range(i + 1, N)]


def from_coords(v, N):
    X = np.zeros((N, N), dtype=np.int64)
    for (i, j), a in zip(upper_positions(N), v):
        X[i, j] = a
    return X


def nullspace_mod_p(A, p):
    """Basis of {x : A x = 0} over F_p (A: rows x cols, python ints)."""
    A = [list(map(lambda t: int(t) % p, r)) for r in A]
    rows, cols = len(A), len(A[0]) if A else 0
    piv, r = [], 0
    for c in range(cols):
        k = next((i for i in range(r, rows) if A[i][c]), None)
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [a * inv % p for a in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(a - f * b) % p for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        v = [0] * cols
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][f]) % p
        basis.append(v)
    return basis


def span(basis, p):
    if not basis:
        return {tuple([0] * 0)}
    n = len(basis[0])
    out = set()
    for coeffs in itertools.product(range(p), repeat=len(basis)):
        out.add(tuple(sum(c * b[i] for c, b in zip(coeffs, basis)) % p for i in range(n)))
    return out


# ---------------------------------------------------------------- A
def section_A(out):
    out("== A. exp(x)M exp(-x) vs exp(ad_x)M = sum_{k<p} ad_x^k M / k!  (ad_x^p = ad_{x^p} = 0 in char p)")
    for N in range(2, 8):
        J = np.zeros((N, N), dtype=np.int64)
        for i in range(N - 1):
            J[i, i + 1] = 1
        M = np.zeros((N, N), dtype=np.int64)
        M[N - 1, 0] = 1
        verdicts = []
        for p in primes_upto(2 * N + 3):
            if p < N:
                continue
            conj = mm(mm(mexp(J, p), M, p), mexp((-J) % p, p), p)
            ad = M.copy()
            tot = M.copy()
            for k in range(1, p):
                ad = (mm(J, ad, p) - mm(ad, J, p)) % p
                tot = (tot + ad * pow(factorial(k), -1, p)) % p
            adp = (mm(J, ad, p) - mm(ad, J, p)) % p  # ad^p M must vanish mod p
            assert not adp.any()
            fails = bool(((conj - tot) % p).any())
            expected_fail = p <= 2 * N - 2
            assert fails == expected_fail, (N, p)
            # random controls in the identity range
            if not expected_fail:
                for _ in range(20):
                    x = from_coords([rng.randrange(p) for _ in upper_positions(N)], N)
                    A = np.array([[rng.randrange(p) for _ in range(N)] for _ in range(N)], dtype=np.int64)
                    c2 = mm(mm(mexp(x, p), A, p), mexp((-x) % p, p), p)
                    a2, t2 = A.copy(), A.copy()
                    for k in range(1, p):
                        a2 = (mm(x, a2, p) - mm(a2, x, p)) % p
                        t2 = (t2 + a2 * pow(factorial(k), -1, p)) % p
                    assert not ((c2 - t2) % p).any()
            verdicts.append(f"p={p}:{'FAILS' if fails else 'holds'}")
        out(f" N={N} (x=J_N, M=E_N1): " + " ".join(verdicts) + f"   [fails exactly for {N}<=p<={2*N-2}]")
    out("   smallest witness N=p=2: x=E12, M=E21: conj-trunc = -x M x = E12 (nonzero mod 2)")


# ---------------------------------------------------------------- B
def rank_mod_p(rows, p):
    return len(rows[0]) - len(nullspace_mod_p(rows, p)) if rows else 0


def in_span(vec, basis, p):
    if not basis:
        return not any(v % p for v in vec)
    return rank_mod_p([list(b) for b in basis] + [list(vec)], p) == rank_mod_p([list(b) for b in basis], p)


def bracket_coords(u, v, N, p):
    X, Y = from_coords(u, N), from_coords(v, N)
    Z = (mm(X, Y, p) - mm(Y, X, p)) % p
    return [int(Z[i, j]) for i, j in upper_positions(N)]


def stab_basis(L_basis, As, N, p):
    """Basis of L cap (cap ker ad_A) in coordinates."""
    dim = len(upper_positions(N))
    rows = []
    for A in As:
        cols = []
        for b in L_basis:
            X = from_coords(b, N)
            cols.append(((mm(X, A, p) - mm(A, X, p)) % p).reshape(-1))
        rows.extend(np.array(cols).T.tolist())
    kern = nullspace_mod_p(rows, p)
    return [[sum(c * b[i] for c, b in zip(kv, L_basis)) % p for i in range(dim)] for kv in kern]


def section_B(out):
    out("== B. Proposition conjugation: Stab_{exp L}(A_1..A_k) = exp(L cap cap ker ad_A_i)")
    for N, p, mode in [(2, 2, "all"), (3, 3, "all"), (3, 5, "sample"), (4, 5, "sample"), (5, 5, "sample")]:
        dim = len(upper_positions(N))
        full = [[int(i == j) for j in range(dim)] for i in range(dim)]
        algebras, tries = [full], 0
        while len(algebras) < 6 and tries < 400:
            tries += 1
            b = [[rng.randrange(p) for _ in range(dim)] for _ in range(rng.randint(1, dim))]
            red = nullspace_mod_p(nullspace_mod_p(b, p), p)
            if red and all(in_span(bracket_coords(u, v, N, p), red, p) for u in red for v in red):
                algebras.append(red)
        n_checks = 0
        for L in algebras:
            if p ** len(L) <= 3000:
                elems = [tuple(sum(c * b[i] for c, b in zip(cs, L)) % p for i in range(dim))
                         for cs in itertools.product(range(p), repeat=len(L))]
            else:
                elems = []
                for _ in range(1500):
                    cs = [rng.randrange(p) for _ in L]
                    elems.append(tuple(sum(c * b[i] for c, b in zip(cs, L)) % p for i in range(dim)))
            G = [mexp(from_coords(e, N), p) for e in elems]
            for _ in range(30):  # exp(L) is closed under products
                lg = mlog(mm(rng.choice(G), rng.choice(G), p), p)
                assert not np.tril(lg).any()
                assert in_span([int(lg[i, j]) for i, j in upper_positions(N)], L, p)
            if mode == "all" and len(L) == dim:
                tuples = [(np.array(a, dtype=np.int64).reshape(N, N),)
                          for a in itertools.product(range(p), repeat=N * N)]
            else:
                tuples = []
                for _ in range(40):
                    As = []
                    for _ in range(rng.randint(1, 2)):
                        if rng.random() < 0.5:  # large centralizer: a polynomial in a random x
                            x = from_coords([rng.randrange(p) for _ in range(dim)], N)
                            A = (np.eye(N, dtype=np.int64) * rng.randrange(p) + x + mm(x, x, p) * rng.randrange(p)) % p
                        else:
                            A = np.array([[rng.randrange(p) for _ in range(N)] for _ in range(N)], dtype=np.int64)
                        As.append(A)
                    tuples.append(tuple(As))
            for As in tuples:
                S = stab_basis(L, As, N, p)
                for e, g in zip(elems, G):
                    ginv = mexp((-from_coords(e, N)) % p, p)
                    fixes = all(not ((mm(mm(g, A, p), ginv, p) - A) % p).any() for A in As)
                    assert fixes == in_span(e, S, p), (N, p, e)
                    n_checks += 1
        out(f" N={N} p={p}: {len(algebras)} Lie subalgebras (incl. n_N), {n_checks} (g, tuple) pairs agree")

    out("   transporter for L = n_N: brute force vs the linear system X A - B X = B - A")
    for N, p in [(2, 2), (3, 3), (3, 5)]:
        dim = len(upper_positions(N))
        Xs = [from_coords(v, N) for v in itertools.product(range(p), repeat=dim)]
        cnt = 0
        for _ in range(60):
            A = np.array([[rng.randrange(p) for _ in range(N)] for _ in range(N)], dtype=np.int64)
            g0 = np.eye(N, dtype=np.int64) + Xs[rng.randrange(len(Xs))]
            B = mm(mm(g0, A, p), mexp((-mlog(g0, p)) % p, p), p) if rng.random() < 0.7 else \
                np.array([[rng.randrange(p) for _ in range(N)] for _ in range(N)], dtype=np.int64)
            for X in Xs:
                g = (np.eye(N, dtype=np.int64) + X) % p
                brute = not ((mm(g, A, p) - mm(B, g, p)) % p).any()
                lin = not ((mm(X, A, p) - mm(B, X, p) - (B - A)) % p).any()
                assert brute == lin
                cnt += 1
        out(f"   N={N} p={p}: {cnt} candidate g agree")

    out("   beyond the Proposition (N > p, exp undefined): Stab_{UT_N}(A) = I + (n_N cap commutant A), exhaustive")
    for N, p in [(3, 2), (4, 3)]:
        dim = len(upper_positions(N))
        Xs = [from_coords(v, N) for v in itertools.product(range(p), repeat=dim)]
        cnt = 0
        for _ in range(25):
            A = np.array([[rng.randrange(p) for _ in range(N)] for _ in range(N)], dtype=np.int64)
            for X in Xs:
                g = (np.eye(N, dtype=np.int64) + X) % p
                brute = not ((mm(g, A, p) - mm(A, g, p)) % p).any()
                lin = not ((mm(X, A, p) - mm(A, X, p)) % p).any()
                assert brute == lin
                cnt += 1
        out(f"   N={N} p={p}: {cnt} pairs agree (linear in X for every N, p)")


# ---------------------------------------------------------------- C
def section_C(out):
    out("== C. 2-jet quadratic stabilizer, singular B allowed, N <= p < 2N-1:")
    out("   {g in UT_N : g^T B g = B, b^T g = b^T} == exp{X in n_N : X^T B + B X = 0, b^T X = 0}")
    for N, p, mode in [(3, 3, "all"), (4, 5, "sample"), (5, 5, "sample")]:
        pos = upper_positions(N)
        dim = len(pos)
        if mode == "all":
            Xc = list(itertools.product(range(p), repeat=dim))
        else:
            Xc = [tuple(rng.randrange(p) for _ in range(dim)) for _ in range(1500)]
        sym_idx = [(i, j) for i in range(N) for j in range(i, N)]
        Bs = []
        if mode == "all":
            for vals in itertools.product(range(p), repeat=len(sym_idx)):
                B = np.zeros((N, N), dtype=np.int64)
                for (i, j), a in zip(sym_idx, vals):
                    B[i, j] = B[j, i] = a
                Bs.append(B)
        else:
            for _ in range(300):
                # low rank symmetric B = sum_r c_r w_r w_r^T, often singular
                B = np.zeros((N, N), dtype=np.int64)
                for _ in range(rng.randint(0, N)):
                    w = np.array([rng.randrange(p) for _ in range(N)], dtype=np.int64)
                    B = (B + rng.randrange(1, p) * np.outer(w, w)) % p
                Bs.append(B)
        singular = mismatch = 0
        exps = [(X, from_coords(X, N)) for X in Xc]
        exps = [(X, Xm, mexp(Xm, p)) for X, Xm in exps]
        for B in Bs:
            b = np.array([rng.randrange(p) if rng.random() < 0.3 else 0 for _ in range(N)], dtype=np.int64)
            if round(np.linalg.det(B)) % p == 0:
                singular += 1
            for X, Xm, g in exps:
                grp = not ((g.T @ B @ g - B) % p).any() and not ((b @ g - b) % p).any()
                lie = not ((Xm.T @ B + B @ Xm) % p).any() and not ((b @ Xm) % p).any()
                mismatch += grp != lie
        assert mismatch == 0
        out(f"   N={N} p={p}: {len(Bs)} forms ({singular} singular) x {len(exps)} X: 0 mismatches")


# ---------------------------------------------------------------- D
def poly_mul(a, b, p):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            out[e] = (out.get(e, 0) + ca * cb) % p
    return {e: c for e, c in out.items() if c}


def poly_add(a, b, p, s=1):
    out = dict(a)
    for e, c in b.items():
        out[e] = (out.get(e, 0) + s * c) % p
    return {e: c for e, c in out.items() if c}


def var(i, n):
    return {tuple(int(k == i) for k in range(n)): 1}


def lin(row, n, p):
    out = {}
    for i, a in enumerate(row):
        if a % p:
            out = poly_add(out, {tuple(int(k == i) for k in range(n)): a % p}, p)
    return out


def substitute(F, rows, n, p):
    """F(g x) where (g x)_i = sum_j rows[i][j] x_j."""
    images = [lin(r, n, p) for r in rows]
    out = {}
    for e, c in F.items():
        term = {tuple([0] * n): c}
        for i, k in enumerate(e):
            for _ in range(k):
                term = poly_mul(term, images[i], p)
        out = poly_add(out, term, p)
    return out


def section_D(out):
    out("== D. Remark (ii) controls")
    p, n = 5, 4
    x = [var(i, n) for i in range(n)]
    F = poly_add(poly_add(poly_mul(poly_mul(x[0], x[1], p), x[3], p),
                          poly_mul(poly_mul({tuple([0]*n): 2}, x[0], p), poly_mul(x[2], x[2], p), p), p),
                 poly_mul(poly_mul(x[1], x[1], p), x[2], p), p, -1)
    Nm = np.zeros((4, 4), dtype=np.int64)
    Nm[0, 1] = Nm[1, 2] = Nm[2, 3] = 1
    # infinitesimal: R(x) = grad F(x) . (N x)
    Nx = [lin(Nm[i].tolist(), n, p) for i in range(n)]
    R = {}
    for i in range(n):
        dF = {}
        for e, c in F.items():
            if e[i]:
                e2 = list(e); e2[i] -= 1
                dF = poly_add(dF, {tuple(e2): c * e[i] % p}, p)
        R = poly_add(R, poly_mul(dF, Nx[i], p), p)
    assert R == {}
    g = mexp(Nm, p)
    diff = poly_add(substitute(F, g.tolist(), n, p), F, p, -1)
    out(f"   UT_4(F_5), F=x0x1x3+2x0x2^2-x1^2x2 (Delta=3<5), N=E01+E12+E23: grad F.(Nx)=0 formally;"
        f" F(exp(N)x)-F(x) = {diff}  (nonzero; so Delta<p is not enough)")
    assert diff == {(0, 0, 0, 3): 1}
    import sympy as sp
    t = sp.symbols("t")
    xs = sp.symbols("x0:4")
    E = sp.zeros(4, 4)
    for i in range(4):
        for j in range(i, 4):
            E[i, j] = t ** (j - i) / sp.factorial(j - i)
    gx = E * sp.Matrix(xs)
    Fs = lambda v: v[0]*v[1]*v[3] + 2*v[0]*v[2]**2 - v[1]**2*v[2]
    dq = sp.expand(Fs(list(gx)) - Fs(list(xs)))
    out(f"   over Q: F(exp(tN)x)-F(x) = {dq}  (every other coefficient is divisible by 5; mod 5 it is t^5 x3^3/6 = t^5 x3^3, i.e. t*x3^3 for t in F_5)")
    # Non-fixed anchor: p=3, f = u^3 v - u v^3 is GL_2(F_3)-invariant; anchor a=(0,1) is moved by UT_2.
    p, n = 3, 2
    u, w = var(0, n), var(1, n)
    f = poly_add(poly_mul(poly_mul(poly_mul(u, u, p), u, p), w, p),
                 poly_mul(u, poly_mul(poly_mul(w, w, p), w, p), p), p, -1)
    for t in range(p):
        assert substitute(f, [[1, t], [0, 1]], n, p) == f
    shifted = substitute(f, [[1, 0], [0, 1]], n, p)
    # f(a + y) with a = (0,1): substitute v -> v + 1
    fa = {}
    for e, c in f.items():
        term = {tuple([0]*n): c}
        for _ in range(e[0]):
            term = poly_mul(term, u, p)
        for _ in range(e[1]):
            term = poly_mul(term, poly_add(w, {(0, 0): 1}, p), p)
        fa = poly_add(fa, term, p)
    jet = {e: c for e, c in fa.items() if sum(e) <= 2}
    K = [t for t in range(p) if substitute(jet, [[1, t], [0, 1]], n, p) == jet]
    out(f"   p=3, f=u^3v-uv^3 (H = UT_2(F_3), order 3); 2-jet at non-fixed anchor (0,1) = {jet};"
        f" its stabilizer K = {{t: {K}}} = 1, so K does not contain H")
    assert K == [0] and shifted == f


def main():
    lines = []
    out = lines.append
    section_A(out)
    section_B(out)
    section_C(out)
    section_D(out)
    text = "\n".join(lines)
    print(text)
    Path(__file__).with_suffix(".out").write_text(text + "\n")


if __name__ == "__main__":
    main()
