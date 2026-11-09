"""Exact checks for the Rees application report (item 12, 2026-11-02).

Run:  /opt/anaconda3/bin/python -I phase_state_checks.py > phase_state_checks.out

These are finite sanity checks of algebraic identities proved in
../2026-11-02-rees-application.md. They are not evidence for all n or p.

1. Line step (Section 4.2): sum_i P(z_i + delta_i t v) has no t^d term when
   sum_i delta_i^d = 0, and its t^(d-1) coefficient depends on the top form
   of P whenever v has full support.  Exact integer arithmetic mod p.
2. State vectors: k copies of psi_P plus |+_t>, the register shift
   x_i -> x_i - delta_i t v, and a computational measurement of z give
   (a) uniform outcomes and (b) exactly the predicted univariate phase state.
3. Ray stabilizer and gap of psi_P (cubic P) in G_2 = F_p^n x| Pol_{<=2}:
   exactly p^n unit-modulus overlaps (one per shift a), all others at most
   p^(-1/2).  Exhaustive over the group modulo scalars.
4. Subspace-stabilizer lemma (Section 3.1): for L <= n_N(F_p), N <= p,
   Stab_{exp L}(W) = exp{x in L : xW <= W}.  Exhaustive over exp(L).
"""

import itertools
import random

import numpy as np

RNG = random.Random(20261102)


# ---------------------------------------------------------------- polynomials
def monomials(n, d):
    """Exponent vectors of total degree 1..d in n variables."""
    out = []
    for deg in range(1, d + 1):
        for c in itertools.combinations_with_replacement(range(n), deg):
            e = [0] * n
            for i in c:
                e[i] += 1
            out.append(tuple(e))
    return out


def random_poly(n, d, p, full_top=True):
    P = {m: RNG.randrange(p) for m in monomials(n, d)}
    if full_top:
        for m in P:
            if sum(m) == d and P[m] == 0:
                P[m] = RNG.randrange(1, p)
    return P


def peval(P, x, p):
    s = 0
    for m, c in P.items():
        t = c
        for xi, ei in zip(x, m):
            t = t * pow(xi, ei, p) % p
        s += t
    return s % p


def interpolate(vals, p):
    """Coefficients (mod p) of the unique poly of degree < p with given values at 0..p-1."""
    # Solve Vandermonde exactly mod p.
    A = [[pow(t, j, p) for j in range(p)] for t in range(p)]
    b = list(vals)
    n = p
    M = [row[:] + [bb] for row, bb in zip(A, b)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] % p)
        M[col], M[piv] = M[piv], M[col]
        inv = pow(M[col][col], p - 2, p)
        M[col] = [v * inv % p for v in M[col]]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]
                M[r] = [(vr - f * vc) % p for vr, vc in zip(M[r], M[col])]
    return [M[j][n] for j in range(n)]


def line_coeffs(P, zs, deltas, v, p):
    vals = []
    for t in range(p):
        s = 0
        for z, dl in zip(zs, deltas):
            pt = [(zi + dl * t * vi) % p for zi, vi in zip(z, v)]
            s += peval(P, pt, p)
        vals.append(s % p)
    return interpolate(vals, p)


def zero_moment(d, p, k):
    """Nonzero delta in F_p^k with sum delta_i^d = 0 (small brute force)."""
    for dl in itertools.product(range(p), repeat=k):
        if any(dl) and sum(pow(x, d, p) for x in dl) % p == 0 and dl[0] == 1:
            return dl
    return None


def check_line_step():
    print("== 1. line step identity")
    cases = [(2, 3, 7, 2), (3, 3, 11, 2), (2, 4, 13, 3), (3, 4, 13, 3), (2, 5, 11, 2)]
    for n, d, p, k in cases:
        dl = zero_moment(d, p, k)
        ok_top, ok_dep, trials = 0, 0, 20
        for _ in range(trials):
            P = random_poly(n, d, p)
            zs = [[RNG.randrange(p) for _ in range(n)] for _ in range(k)]
            v = [RNG.randrange(1, p) for _ in range(n)]
            c = line_coeffs(P, zs, dl, v, p)
            if all(x == 0 for x in c[d:]):
                ok_top += 1
            # t^(d-1) coefficient as a linear functional of the TOP coefficients:
            # perturb one top monomial and see whether c_{d-1} moves.
            top = [m for m in P if sum(m) == d]
            moved = False
            for m in top:
                P2 = dict(P)
                P2[m] = (P2[m] + 1) % p
                c2 = line_coeffs(P2, zs, dl, v, p)
                if c2[d - 1] != c[d - 1]:
                    moved = True
                    break
            ok_dep += moved
        print(f"n={n} d={d} p={p} delta={dl}: no t^>=d term {ok_top}/{trials}; "
              f"t^(d-1) depends on top form {ok_dep}/{trials}")


# ------------------------------------------------------------- state vectors
def phase_state(P, n, p):
    pts = list(itertools.product(range(p), repeat=n))
    om = np.exp(2j * np.pi / p)
    return np.array([om ** peval(P, x, p) for x in pts]) / np.sqrt(p ** n), pts


def check_state_vectors():
    print("== 2. state-vector line step")
    for n, d, p, k in [(2, 3, 7, 2), (1, 4, 13, 3), (1, 3, 11, 2)]:
        dl = zero_moment(d, p, k)
        P = random_poly(n, d, p)
        psi, pts = phase_state(P, n, p)
        idx = {x: i for i, x in enumerate(pts)}
        v = tuple(RNG.randrange(1, p) for _ in range(n))
        N = p ** n
        # joint amplitude after the shift, indexed by (z_1..z_k, t)
        om = np.exp(2j * np.pi / p)
        shape = (N,) * k + (p,)
        amp = np.zeros(shape, dtype=complex)
        for xs in itertools.product(range(N), repeat=k):
            a0 = np.prod([psi[x] for x in xs]) / np.sqrt(p)
            for t in range(p):
                zs = tuple(idx[tuple((pts[x][j] - dl[i] * t * v[j]) % p for j in range(n))]
                           for i, x in enumerate(xs))
                amp[zs + (t,)] += a0
        probs = np.sum(np.abs(amp) ** 2, axis=-1)
        unif = np.max(np.abs(probs - 1.0 / N ** k))
        worst = 1.0
        for zs in itertools.product(range(N), repeat=k):
            post = amp[zs] / np.linalg.norm(amp[zs])
            r = [sum(peval(P, [(pts[z][j] + dl[i] * t * v[j]) % p for j in range(n)], p)
                     for i, z in enumerate(zs)) % p for t in range(p)]
            pred = np.array([om ** rt for rt in r]) / np.sqrt(p)
            worst = min(worst, abs(np.vdot(pred, post)))
        print(f"n={n} d={d} p={p} k={k} delta={dl}: max|prob-1/N^k|={unif:.2e}; "
              f"min fidelity to predicted univariate state={worst:.12f}")


# --------------------------------------------------------- ray stabilizer gap
def check_ray_stabilizer(n=2, p=7):
    print("== 3. ray stabilizer and gap of a cubic phase state in G_2")
    P = random_poly(n, 3, p)
    pts = list(itertools.product(range(p), repeat=n))
    om = np.exp(2j * np.pi / p)
    Pv = np.array([peval(P, x, p) for x in pts])
    qmons = monomials(n, 2)  # linear and quadratic monomials (constants are scalars)
    # all Q modulo constants
    Qs = list(itertools.product(range(p), repeat=len(qmons)))
    unit, maxother, predicted_ok = 0, 0.0, True
    for a in pts:
        xa = [tuple((x[j] - a[j]) % p for j in range(n)) for x in pts]
        Pxa = np.array([peval(P, y, p) for y in xa])
        base = (Pxa - Pv) % p  # P(x-a) - P(x)
        # Q(x-a) for every Q: matrix of monomials at x-a
        mon = np.array([[np.prod([pow(y[j], m[j], p) for j in range(n)]) % p for m in qmons]
                        for y in xa])  # (p^n, |qmons|)
        Qarr = np.array(Qs)  # (#Q, |qmons|)
        expo = (Qarr @ mon.T + base[None, :]) % p
        ov = np.abs(np.sum(om ** expo, axis=1)) / p ** n
        isunit = ov > 1 - 1e-9
        unit += int(isunit.sum())
        maxother = max(maxother, float(ov[~isunit].max()))
        # predicted member: Q(y) = P(y+a) - P(y) without constant, evaluated in y = x - a
        if isunit.sum() != 1:
            predicted_ok = False
    print(f"n={n} p={p}: unit-modulus elements (mod scalars) = {unit} (expected p^n={p**n}); "
          f"one per shift: {predicted_ok}; max other overlap = {maxother:.6f} "
          f"(bound p^-1/2 = {p**-0.5:.6f})")


# ------------------------------------------------- subspace stabilizer lemma
def mat_exp(x, p, N):
    I = np.eye(N, dtype=np.int64)
    out, term = I.copy(), I.copy()
    fact = 1
    for j in range(1, N):
        term = term @ x % p
        fact = fact * j % p
        out = (out + term * pow(fact, p - 2, p)) % p
    return out


def rank_mod(M, p):
    M = [list(map(int, r)) for r in M]
    r = 0
    rows, cols = len(M), len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [v * inv % p for v in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r


def preserves(A, W, p):
    """A W <= W for W given by columns."""
    return rank_mod(np.hstack([W, A @ W % p]), p) == rank_mod(W, p)


def check_subspace_lemma(N=4, p=5):
    print("== 4. subspace-stabilizer lemma in exp(L), L <= n_N(F_p)")
    basis = []
    for i in range(N):
        for j in range(i + 1, N):
            E = np.zeros((N, N), dtype=np.int64)
            E[i, j] = 1
            basis.append(E)
    # L1 = n_N; L2 = a proper subalgebra: matrices with (0,1) entry zero... use span of
    # E_{i,j} with j-i>=2 plus E_{01}+E_{23}+... (closed under brackets? check).
    L2 = [basis[k] for k in range(len(basis))
          if not (k == 0)]  # drop E_{01}: span of remaining E_ij is a subalgebra
    for name, L in [("n_4", basis), ("n_4 minus E01", L2)]:
        for trial in range(3):
            W = np.array([[RNG.randrange(p) for _ in range(2)] for _ in range(N)])
            lie, grp = 0, 0
            for coeffs in itertools.product(range(p), repeat=len(L)):
                x = sum(c * B for c, B in zip(coeffs, L)) % p
                a = preserves(x, W, p)
                b = preserves(mat_exp(x, p, N), W, p)
                if a != b:
                    print("  MISMATCH", name, coeffs)
                lie += a
                grp += b
            print(f"{name}: dim W={rank_mod(W, p)}: |{{x: xW<=W}}|={lie}, "
                  f"|Stab_exp(L)(W)|={grp}, equal={lie == grp}")


def check_twisted_code(n=2, p=7, d=3, k_copies=2):
    """rho_{U,P} = average over lam in U^perp of |psi_{P+lam.x}><...|, U = F_p*u0 (dim 1).

    (a) |Tr(rho R(a,Q))| = 1 exactly for one Q per a in U, 0 for a not in U, and at
        most p^-1/2 otherwise (exhaustive over G_2 mod scalars).
    (b) largest nontrivial Weyl characteristic value |Tr(rho X_a Z_b)|.
    (c) IS line step on k copies: conditional t-state is I/p for v not in U and pure
        for v in U.
    """
    print("== 5. twisted translation code rho_{U,P}")
    P = random_poly(n, d, p)
    pts = list(itertools.product(range(p), repeat=n))
    idx = {x: i for i, x in enumerate(pts)}
    om = np.exp(2j * np.pi / p)
    u0 = (1, RNG.randrange(p))
    lams = [lam for lam in pts if (lam[0] * u0[0] + lam[1] * u0[1]) % p == 0]
    comps = []
    for lam in lams:
        Pl = dict(P)
        for j in range(n):
            e = tuple(1 if i == j else 0 for i in range(n))
            Pl[e] = (Pl.get(e, 0) + lam[j]) % p
        comps.append(phase_state(Pl, n, p)[0])
    rho = sum(np.outer(c, c.conj()) for c in comps) / len(comps)
    U = {tuple((t * u0[j]) % p for j in range(n)) for t in range(p)}
    qmons = monomials(n, 2)
    Qs = np.array(list(itertools.product(range(p), repeat=len(qmons))))
    unit, max_other, nonU_max = 0, 0.0, 0.0
    for a in pts:
        xa = [tuple((x[j] - a[j]) % p for j in range(n)) for x in pts]
        mon = np.array([[np.prod([pow(y[j], m[j], p) for j in range(n)]) % p for m in qmons]
                        for y in xa])
        expo = (Qs @ mon.T) % p                     # Q(x-a), shape (#Q, p^n)
        # Tr(rho D_Q X_a) = sum_x rho[x-a, x] * omega^{Q(x-a)}... use (D_Q X_a psi)(x)=w^{Q(x-a)}psi(x-a)
        cols = np.array([rho[idx[xa[i]], i] for i in range(len(pts))])  # <x|...: rho_{x-a? }
        # Tr(rho R) = sum_{x} <x| R rho |x> = sum_x w^{Q(x-a)} rho[x-a, x]
        tr = np.abs((om ** expo) @ cols)
        if a in U:
            isu = tr > 1 - 1e-9
            unit += int(isu.sum())
            max_other = max(max_other, float(tr[~isu].max()))
        else:
            nonU_max = max(nonU_max, float(tr.max()))
    # Weyl characteristic function: Q linear only
    weyl = 0.0
    for a in pts:
        for b in pts:
            if a == (0, 0) and b == (0, 0):
                continue
            val = sum(rho[idx[tuple((x[j] - a[j]) % p for j in range(n))], i]
                      * om ** (sum(b[j] * x[j] for j in range(n)) % p) for i, x in enumerate(pts))
            weyl = max(weyl, abs(val))
    print(f"n={n} p={p} U=F_p*{u0}: unit G_2 elements over a in U = {unit} (expected p={p}); "
          f"max other (a in U) = {max_other:.6f}; max over a not in U = {nonU_max:.2e}; "
          f"max nontrivial Weyl |Tr(rho W)| = {weyl:.6f}")
    # (c) line step on k copies
    dl = zero_moment(d, p, k_copies)
    for v, label in [(u0, "v in U"), (next(w for w in pts if w not in U and w[0] and w[1]), "v not in U")]:
        worst_dev, max_purity, min_purity = 0.0, 0.0, 1.0
        zsamples = [tuple(RNG.randrange(len(pts)) for _ in range(k_copies)) for _ in range(40)]
        acc = {z: np.zeros((p, p), dtype=complex) for z in zsamples}
        for combo in itertools.product(range(len(comps)), repeat=k_copies):
            for zs in zsamples:
                amp = np.zeros(p, dtype=complex)
                for t in range(p):
                    a0 = 1.0 / np.sqrt(p)
                    for i, z in enumerate(zs):
                        x = tuple((pts[z][j] + dl[i] * t * v[j]) % p for j in range(n))
                        a0 *= comps[combo[i]][idx[x]]
                    amp[t] = a0
                acc[zs] += np.outer(amp, amp.conj())
        for zs in zsamples:
            M = acc[zs] / np.trace(acc[zs])
            worst_dev = max(worst_dev, float(np.abs(M - np.eye(p) / p).max()))
            pur = float(np.real(np.trace(M @ M)))
            max_purity, min_purity = max(max_purity, pur), min(min_purity, pur)
        print(f"  line step k={k_copies} delta={dl}, {label}: max|rho_t - I/p| = {worst_dev:.2e}; "
              f"purity range [{min_purity:.6f}, {max_purity:.6f}] (I/p has {1/p:.6f})")


if __name__ == "__main__":
    check_line_step()
    check_state_vectors()
    check_ray_stabilizer()
    check_subspace_lemma()
    check_twisted_code()
