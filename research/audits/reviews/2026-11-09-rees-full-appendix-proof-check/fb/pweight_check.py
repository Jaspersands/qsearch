"""fb check 3: the p-weight paragraph of app:filters-applications and the linearization sentence of rem:filters(ii).

Claim A (stated as proved): for G = exp(L) <= UT_D(F_p), D <= p, nu the nilpotency index of L,
delta(F) <= dhat and p > max((nu-1) dhat, dhat) (exactness), p^K > deg F, log H is the kernel of the
F_p-linear map A -> A.R_F, where R_F is the polynomial of degree <= delta(F) that agrees with F on the
F_p-points of F_{p^K}^D.  We test it with K = 2: (A.R_F)(y) is the s-coefficient of the interpolant of
s -> F(x + s A x), s in F_p (a polynomial of degree <= delta(F) < p), and A.R_F = 0 iff it vanishes at
every x in F_{p^2}^D (degree < p).  H is computed by brute force over G as functional invariance on
F_{p^2}^D, which equals formal invariance because deg F < p^2.
Claim B: "first-order linearization is proved under p > max(D, (D-1)Delta) ...; Delta < p is not enough":
we search for F of degree Delta < p (formal) with ker(A -> A.F) != log H at p = 5, D = 3.
Finite checks only.
"""
import itertools, random, sys
import numpy as np

class Fq:
    """F_{p^2} = F_p[th]/(th^2 - nr), elements encoded as a + b p."""
    def __init__(self, p):
        self.p = p
        self.nr = next(a for a in range(2, p) if pow(a, (p - 1) // 2, p) == p - 1)
        q = p * p
        self.q = q
        A = np.arange(q) % p; B = np.arange(q) // p
        self.add = ((A[:, None] + A[None, :]) % p) + p * ((B[:, None] + B[None, :]) % p)
        self.mul = ((A[:, None] * A[None, :] + self.nr * B[:, None] * B[None, :]) % p) + \
                   p * ((A[:, None] * B[None, :] + B[:, None] * A[None, :]) % p)
        self.neg = ((-A) % p) + p * ((-B) % p)
        # scalar (F_p) times element
        self.smul = np.array([[(c * a % p) + p * (c * b % p) for a, b in zip(A, B)] for c in range(p)])

    def pow_table(self, e_max):
        T = np.zeros((e_max + 1, self.q), dtype=np.int64)
        T[0] = 1
        for e in range(1, e_max + 1):
            T[e] = self.mul[T[e - 1], np.arange(self.q)]
        return T

def digit_sum(n, p):
    s = 0
    while n:
        s += n % p; n //= p
    return s

def exps_with_weight(p, wmax, emax):
    return [e for e in range(emax + 1) if digit_sum(e, p) <= wmax]

def random_poly(p, D, wmax, emax, nterms, rnd, total_weight=True):
    """random F = sum c * x^alpha with p-weight(alpha) <= wmax and each exponent <= emax."""
    ex = exps_with_weight(p, wmax, emax)
    terms = {}
    while len(terms) < nterms:
        alpha = tuple(rnd.choice(ex) for _ in range(D))
        if sum(digit_sum(a, p) for a in alpha) <= wmax and 0 < sum(alpha) <= emax:
            terms[alpha] = rnd.randrange(1, p)
    return terms

def lin_sub(terms, M, p):
    """F(M x) as a dict, by expansion over F_p (small exponents)."""
    D = M.shape[0]
    out = {}
    def mul(P, Q):
        R = {}
        for a, ca in P.items():
            for b, cb in Q.items():
                k = tuple(x + y for x, y in zip(a, b))
                R[k] = (R.get(k, 0) + ca * cb) % p
        return {k: v for k, v in R.items() if v}
    lin = []
    for i in range(D):
        L = {}
        for j in range(D):
            if M[i, j] % p:
                e = [0] * D; e[j] = 1
                L[tuple(e)] = int(M[i, j] % p)
        lin.append(L)
    cache = {}
    def power(i, e):
        if (i, e) not in cache:
            if e == 0:
                cache[(i, e)] = {tuple([0] * D): 1}
            else:
                cache[(i, e)] = mul(power(i, e - 1), lin[i])
        return cache[(i, e)]
    for alpha, c in terms.items():
        P = {tuple([0] * D): c}
        for i, a in enumerate(alpha):
            P = mul(P, power(i, a))
        for k, v in P.items():
            out[k] = (out.get(k, 0) + v) % p
    return {k: v for k, v in out.items() if v}

def add_polys(P, Q, p):
    R = dict(P)
    for k, v in Q.items():
        R[k] = (R.get(k, 0) + v) % p
    return {k: v for k, v in R.items() if v}

def mat_exp(x, p):
    N = x.shape[0]
    out = np.eye(N, dtype=np.int64); term = np.eye(N, dtype=np.int64); fact = 1
    for j in range(1, p):
        term = (term @ x) % p; fact = fact * j % p
        out = (out + term * pow(fact, p - 2, p)) % p
    return out

def subalgebra_elements(basis, p):
    for c in itertools.product(range(p), repeat=len(basis)):
        yield sum(ci * b for ci, b in zip(c, basis)) % p

def nil_index(basis, p):
    N = basis[0].shape[0]
    nu = 1
    for x in subalgebra_elements(basis, p):
        y = x.copy(); k = 1
        while np.any(y % p):
            y = (y @ x) % p; k += 1
        nu = max(nu, k)
    return nu

def kernel_mod_p(Mat, p):
    """kernel of Mat (rows x cols) over F_p, as a list of basis vectors."""
    A = np.array(Mat, dtype=np.int64) % p
    rows, cols = A.shape
    piv = []; r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i, c]), None)
        if pr is None:
            continue
        A[[r, pr]] = A[[pr, r]]
        A[r] = A[r] * pow(int(A[r, c]), p - 2, p) % p
        for i in range(rows):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        piv.append(c); r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64); v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i, f]) % p
        basis.append(v)
    return basis

class Evaluator:
    def __init__(self, p, D, emax):
        self.p, self.D = p, D
        self.F = Fq(p)
        self.P = self.F.pow_table(emax)
        q = self.F.q
        self.pts = np.array(list(itertools.product(range(q), repeat=D)), dtype=np.int64)   # q^D x D

    def eval_points(self, terms, pts):
        F = self.F
        acc = np.zeros(len(pts), dtype=np.int64)
        for alpha, c in terms.items():
            v = np.full(len(pts), 1, dtype=np.int64)
            for i, a in enumerate(alpha):
                if a:
                    v = F.mul[v, self.P[a][pts[:, i]]]
            v = F.smul[c][v]
            acc = F.add[acc, v]
        return acc

    def index(self, pts):
        q = self.F.q
        idx = np.zeros(len(pts), dtype=np.int64)
        for i in range(self.D):
            idx = idx * q + pts[:, i]
        return idx

    def act(self, M, pts):
        """(M x) for x in pts, M over F_p."""
        F = self.F
        out = np.zeros_like(pts)
        for i in range(self.D):
            acc = np.zeros(len(pts), dtype=np.int64)
            for j in range(self.D):
                if M[i, j] % self.p:
                    acc = F.add[acc, F.smul[int(M[i, j] % self.p)][pts[:, j]]]
            out[:, i] = acc
        return out

def interp_linear_coeff(vals, p):
    """vals[s] for s = 0..p-1 (arrays over F_q): coefficient of s^1 of the degree < p interpolant.
    Over F_p: c_1 = -sum_{s != 0} vals[s] * s^{-1} ... use Lagrange: c_1 = sum_s vals[s] * l_s'(0) where
    l_s(t) = prod_{r != s}(t - r)/(s - r). Computed with F_p weights, F_q values."""
    # weights w_s = coefficient of t^1 in l_s(t)
    w = []
    for s in range(p):
        # polynomial prod_{r != s} (t - r) coefficients
        poly = [1]
        den = 1
        for r in range(p):
            if r == s:
                continue
            poly = [(a - r * b) % p for a, b in zip([0] + poly, poly + [0])]  # multiply by (t - r)
            den = den * (s - r) % p
        w.append(poly[1] * pow(den, p - 2, p) % p)
    return w

def method_kernel(ev, terms, Lbasis, base=None):
    """columns: (A_j . R_F)(y) over all points y; returns kernel basis (coefficient vectors)."""
    p = ev.p; Fq_ = ev.F
    w = interp_linear_coeff(None, p)
    cols = []
    for A in Lbasis:
        Ax = ev.act(A, ev.pts)
        acc = np.zeros(len(ev.pts), dtype=np.int64)
        for s in range(p):
            if w[s] == 0:
                continue
            xs = np.zeros_like(ev.pts)
            for i in range(ev.D):
                xs[:, i] = Fq_.add[ev.pts[:, i], Fq_.smul[s][Ax[:, i]]]
            v = base[ev.index(xs)]
            acc = Fq_.add[acc, Fq_.smul[w[s]][v]]
        cols.append(acc)
    # linear map c -> sum c_j col_j over F_p, with F_q values split into 2 F_p coordinates
    rows = []
    C = np.array(cols)  # d x npts
    a = C % p; b = C // p
    Mat = np.concatenate([a, b], axis=1).T   # (2 npts) x d
    # reduce rows: keep a random subset for speed plus full check later
    return kernel_mod_p(Mat, p)

def true_H(ev, terms, Gel, base):
    H = []
    for x, g in Gel:
        ginv = mat_exp((-x) % ev.p, ev.p)
        if np.array_equal(base[ev.index(ev.act(ginv, ev.pts))], base):
            H.append(x)
    return H

def span_set(vecs, Lbasis, p):
    out = set()
    for c in itertools.product(range(p), repeat=len(vecs)):
        coef = sum(ci * v for ci, v in zip(c, vecs)) % p if vecs else np.zeros(len(Lbasis), dtype=np.int64)
        x = sum(int(cj) * b for cj, b in zip(coef, Lbasis)) % p
        out.add(tuple(x.flatten().tolist()))
    return out

def E(i, j, D=3):
    M = np.zeros((D, D), dtype=np.int64); M[i, j] = 1; return M

def run_claim_A(p, dhat_list, n_cases, rnd, emax):
    D = 3
    ev = Evaluator(p, D, emax)
    algebras = {"n_3": [E(0, 1), E(0, 2), E(1, 2)], "<E12,E13>": [E(0, 1), E(0, 2)],
                "<E12+E23,E13>": [(E(0, 1) + E(1, 2)) % p, E(0, 2)], "<E13>": [E(0, 2)]}
    summary = []
    for name, Lb in algebras.items():
        nu = nil_index(Lb, p)
        Gel = [(x, mat_exp(x, p)) for x in subalgebra_elements(Lb, p)]
        for dhat in dhat_list:
            in_hyp_exact = p > max((nu - 1) * dhat, dhat)
            in_hyp_full = p > max((nu - 1) * dhat, 2 * dhat)
            mism = 0; nontriv = 0
            for t in range(n_cases):
                F0 = random_poly(p, D, dhat, emax, 1 + t % 3, rnd)
                # orbit sum over a random subgroup S = exp(span of random elements of L) (contained in H)
                k = rnd.randrange(0, len(Lb) + 1)
                gens = [sum(rnd.randrange(p) * b for b in Lb) % p for _ in range(k)]
                # close gens under brackets inside L
                Sb = []
                for gen in gens:
                    Sb.append(gen)
                Sel = {tuple(np.zeros((D, D), dtype=np.int64).flatten())}
                # build subgroup generated by exp(gens) by closure
                elems = [np.eye(D, dtype=np.int64)]
                seen = {tuple(elems[0].flatten())}
                frontier = list(elems)
                gmats = [mat_exp(gn, p) for gn in gens]
                while frontier:
                    nf = []
                    for a in frontier:
                        for gm in gmats:
                            c = (a @ gm) % p
                            kk = tuple(c.flatten())
                            if kk not in seen:
                                seen.add(kk); nf.append(c)
                    frontier = nf; elems += nf
                Fsum = {}
                for s in elems:
                    # s^{-1}: inverse of unitriangular
                    sinv = np.round(np.linalg.inv(s)).astype(np.int64) % p
                    Fsum = add_polys(Fsum, lin_sub(F0, sinv, p), p)
                if not Fsum:
                    continue
                assert max(sum(a) for a in Fsum) < p * p
                w = max(sum(digit_sum(a, p) for a in alpha) for alpha in Fsum)
                assert w <= dhat
                base = ev.eval_points(Fsum, ev.pts)
                H = true_H(ev, Fsum, Gel, base)
                Hset = {tuple(x.flatten().tolist()) for x in H}
                kv = method_kernel(ev, Fsum, Lb, base)
                Mset = span_set(kv, Lb, p)
                nontriv += (len(Hset) > 1)
                if Hset != Mset:
                    mism += 1
            summary.append((p, name, nu, dhat, in_hyp_exact, in_hyp_full, n_cases, nontriv, mism))
            print(f"[A] p={p} L={name:14s} nu={nu} dhat={dhat} exact-hyp={in_hyp_exact} full-hyp={in_hyp_full}: "
                  f"cases={n_cases} nontrivial H={nontriv} mismatches={mism}", flush=True)
    return summary

def run_claim_B(p, Delta_list, n_cases, rnd):
    """direct first-order linearization on F (formal degree Delta < p), D = 3, L = n_3."""
    D = 3
    Lb = [E(0, 1), E(0, 2), E(1, 2)]
    Gel = [(x, mat_exp(x, p)) for x in subalgebra_elements(Lb, p)]
    pts = np.array(list(itertools.product(range(p), repeat=D)), dtype=np.int64)
    def ev(terms, P):
        acc = np.zeros(len(P), dtype=np.int64)
        for alpha, c in terms.items():
            v = np.full(len(P), c, dtype=np.int64)
            for i, a in enumerate(alpha):
                v = v * pow_mod_arr(P[:, i], a, p) % p
            acc = (acc + v) % p
        return acc
    def pow_mod_arr(a, e, p):
        return np.array([pow(int(x), e, p) for x in a], dtype=np.int64)
    found = []
    for Delta in Delta_list:
        mism = 0
        for t in range(n_cases):
            # random F of total degree <= Delta (formal), orbit-summed over a random subgroup
            terms = {}
            for _ in range(1 + t % 4):
                alpha = None
                while alpha is None or sum(alpha) == 0 or sum(alpha) > Delta:
                    alpha = tuple(rnd.randrange(0, Delta + 1) for _ in range(D))
                terms[alpha] = rnd.randrange(1, p)
            k = rnd.randrange(0, 3)
            gens = [sum(rnd.randrange(p) * b for b in Lb) % p for _ in range(k)]
            elems = [np.eye(D, dtype=np.int64)]; seen = {tuple(elems[0].flatten())}; frontier = list(elems)
            gmats = [mat_exp(gn, p) for gn in gens]
            while frontier:
                nf = []
                for a in frontier:
                    for gm in gmats:
                        c = (a @ gm) % p; kk = tuple(c.flatten())
                        if kk not in seen:
                            seen.add(kk); nf.append(c)
                frontier = nf; elems += nf
            Fs = {}
            for s in elems:
                sinv = np.round(np.linalg.inv(s)).astype(np.int64) % p
                Fs = add_polys(Fs, lin_sub(terms, sinv, p), p)
            if not Fs:
                continue
            assert max(sum(a) for a in Fs) <= Delta < p
            base = ev(Fs, pts)
            H = {tuple(x.flatten().tolist()) for x, g in Gel
                 if np.array_equal(ev(Fs, (pts @ mat_exp((-x) % p, p).T) % p), base)}
            # A.F(x) = sum_k dF/dx_k (x) (A x)_k : formal derivative, degree <= Delta < p, test on F_p^3
            def dF(k):
                out = {}
                for alpha, c in Fs.items():
                    if alpha[k]:
                        b = list(alpha); b[k] -= 1
                        out[tuple(b)] = (out.get(tuple(b), 0) + c * alpha[k]) % p
                return {a: v for a, v in out.items() if v}
            grads = [ev(dF(k), pts) for k in range(D)]
            cols = []
            for A in Lb:
                Ax = (pts @ A.T) % p
                cols.append(sum(grads[k] * Ax[:, k] for k in range(D)) % p)
            kv = kernel_mod_p(np.array(cols).T, p)
            Mset = span_set(kv, Lb, p)
            if H != Mset:
                mism += 1
                if len(found) < 3:
                    found.append((Delta, Fs, sorted(H), sorted(Mset)))
        print(f"[B] p={p} D=3 L=n_3 Delta={Delta} (D-1)Delta={(D-1)*Delta}: cases={n_cases} mismatches={mism}", flush=True)
    for Delta, Fs, H, M in found[:2]:
        print(f"   example Delta={Delta}: F={Fs}\n     |H|={len(H)} |exp(ker)|={len(M)}")
    return found

if __name__ == "__main__":
    rnd = random.Random(20261109)
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("A", "all"):
        run_claim_A(5, [1, 2], 12, rnd, emax=24)
        run_claim_A(5, [3], 12, rnd, emax=24)       # outside the hypothesis when nu = 3
    if which in ("A7",):
        run_claim_A(7, [2, 3], 8, rnd, emax=48)
    if which in ("B", "all"):
        run_claim_B(5, [2, 3, 4], 60, rnd)
