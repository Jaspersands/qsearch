"""End-to-end exact simulation of Algorithm HSP23 (report sec. C) for EVERY subgroup type of free23 over F_p.
AI-written 2026-11-13, pending human review.  Finite check only (falsification): 0 wrong outputs is required, and
proves nothing beyond these instances.

Model: standard HSP oracle.  f is an explicit table on G = (L, BCH) (f(g) = label of the left coset gH, computed
by connected components of right multiplication by generators of H).  The algorithm sees only f:
  * coset states are prepared from f (uniform random coset of f restricted to the domain), counted as QUANTUM
    queries;
  * classical queries f(g) == f(1) certify candidate elements, counted as CLASSICAL queries.
The truth H is used only (a) inside e2e.Run / e2e.etac_step of the second referee (read-only import), which build
the same coset states of H directly instead of through f (equal in distribution), and (b) for diagnostics.

Branches (report sec. C):
  AbHSP(a, C): abelian HSP on exp(a)/exp(C) (C an ideal contained in h, [a,a] in C), Las Vegas: samples lie in
               (h cap a / C)^perp always; the null space is certified element by element with classical queries.
  F23:  hard cyclic branch = Route A of Theorem F23 (e2e.Run, unconditioned labels) + eta_c step; certification
        by one classical query instead of quantum verification.
  IS:   Ivanyos-Santha degree reduction (HPGP', their Thm 5 / Prop 7) in the quotient G/C, C = F_p q (fil4) or
        gamma_3 (heis), with chart n * b^x over the abelian normal N = exp(F_p g0 + gamma_2)/C; Lemma-B weights.
Usage: python hsp_all.py p n_per_type seed [types]
"""
import sys, os, time, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-13-rees-free23-theorem-referee'))
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import ref_core as rc
import e2e

# ---------------- linear algebra mod p ----------------
def rref(M, p):
    M = [[int(x) % p for x in r] for r in M]; rows = len(M); cols = len(M[0]) if rows else 0; r = 0; piv = []
    for c in range(cols):
        q = next((i for i in range(r, rows) if M[i][c]), None)
        if q is None: continue
        M[r], M[q] = M[q], M[r]; iv = pow(M[r][c], -1, p); M[r] = [x * iv % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    return M[:r], piv

def span(vs, p, n=5):
    vs = [list(v) for v in vs if any(int(x) % p for x in v)]
    return [tuple(r) for r in rref(vs, p)[0]] if vs else []

def nullspace(A, n, p):
    """basis of {x in F_p^n : A x = 0}"""
    if len(A) == 0: return [tuple(int(i == j) for j in range(n)) for i in range(n)]
    R, piv = rref(A, p); out = []
    for fv in [j for j in range(n) if j not in piv]:
        x = [0] * n; x[fv] = 1
        for row, pc in zip(R, piv): x[pc] = (-row[fv]) % p
        out.append(tuple(x))
    return out

def same_space(A, B, p): return span(A, p) == span(B, p)

def coords_in(basis, v, p):
    """coefficients of v in the (independent) basis, or None"""
    k = len(basis)
    A = [[int(basis[j][i]) for j in range(k)] + [int(v[i])] for i in range(len(v))]
    R, piv = rref(A, p)
    if k in piv: return None
    x = [0] * k
    for row, pc in zip(R, piv): x[pc] = row[k]
    return x

# ---------------- the oracle ----------------
class Oracle:
    def __init__(s, F, G, hbasis):
        s.F, s.G, p = F, G, F.p
        n = p ** 5; rows = []; cols = []
        for b in hbasis:
            img = G.idx(rc.bch(G.ALL, np.broadcast_to(np.asarray(b) % p, G.ALL.shape), F))
            rows.append(np.arange(n)); cols.append(img)
        if rows:
            A = coo_matrix((np.ones(n * len(rows)), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
            _, s.lab = connected_components(A, directed=True, connection='weak')
        else:
            s.lab = np.arange(n)
        s.nq = 0; s.nc = 0
        s.one = s.lab[G.idx(np.zeros(5, dtype=np.int64))]
    def classical_in_H(s, v):
        s.nc += 1
        return s.lab[s.G.idx(np.asarray(v, dtype=np.int64) % s.F.p)] == s.one
    def coset_state(s, idxs, rng):
        """one quantum query: sum_x |x>|f(x)> on the domain idxs (list of G-indices), measure f.  Returns the
        indicator (normalised) of the observed level set, as a vector over positions in idxs."""
        s.nq += 1
        vals = s.lab[idxs]
        x = int(rng.integers(len(idxs)))
        v = (vals == vals[x]).astype(float)
        return v / np.linalg.norm(v)

# ---------------- abelian HSP on exp(a)/exp(C) ----------------
def ab_hsp(O, a_basis, C_basis, rng, max_samples=60):
    F = O.F; p = F.p
    C_sp = span(C_basis, p)
    # complement of C in a
    comp = []; cur = list(C_sp)
    for v in span(a_basis, p):
        if len(span(cur + [v], p)) > len(cur): comp.append(v); cur = span(cur + [v], p)
    k = len(comp)
    if k == 0: return C_sp
    T = np.indices((p,) * k).reshape(k, -1).T
    lie = (T @ np.array(comp, dtype=np.int64)) % p
    idxs = O.G.idx(lie)
    samples = []
    for it in range(max_samples):
        st = O.coset_state(idxs, rng).reshape((p,) * k)
        pr = np.abs(np.fft.fftn(st)) ** 2; pr = pr.ravel() / pr.sum()
        y = np.unravel_index(int(rng.choice(p ** k, p=pr)), (p,) * k)
        samples.append([int(t) for t in y])
        ns = nullspace(samples, k, p)
        cand = [tuple(int(x) % p for x in (np.array(t) @ np.array(comp, dtype=np.int64))) for t in ns]
        if all(O.classical_in_H(v) for v in cand):
            return span(list(C_sp) + cand, p)
    raise RuntimeError('ab_hsp did not certify')

# ---------------- hard cyclic branch: Route A (Theorem F23) ----------------
def f23_branch(O, eta_true, rng, R=6, stats=None):
    F, G, p = O.F, O.G, O.F.p
    for att in range(R):
        eqs = []
        for _ in range(2):
            Rr = e2e.Run(F, G, rng, eta_true, stats).go()
            stats['f23_runs'] = stats.get('f23_runs', 0) + 1
            if Rr['ok']:
                eqs.append(Rr['ell']); stats['f23_eq_wrong'] = stats.get('f23_eq_wrong', 0) + int(not Rr['holds'])
        if len(eqs) == 2:
            x = np.cross(eqs[0], eqs[1]) % p
            if x[0] or x[1]:
                etac = e2e.etac_step(F, G, rng, eta_true, x, stats)
                if etac is not None:
                    etah = np.array([x[0], x[1], x[2], etac[0], etac[1]]) % p
                    if O.classical_in_H(etah): return [tuple(int(v) for v in etah)], att + 1
    return [], R

# ---------------- IS branch in Q = G/C ----------------
class SemiQuot:
    """Q = G/exp(C), C a subspace of gamma_3 (dim 1 or 2), with N = exp(F_p g0 + gamma_2)/C abelian, b = exp(x')."""
    def __init__(s, F, G, C_basis, g0, rng):
        p = F.p; s.F, s.G, s.p = F, G, p
        s.C = span(C_basis, p)
        R = []; cur = list(s.C)
        for v in [(0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]:
            if len(span(cur + [v], p)) > len(cur): R.append(v); cur = span(cur + [v], p)
        s.R = R; s.m = 2 + len(R)
        s.g0 = (int(g0[0]) % p, int(g0[1]) % p)
        while True:
            xp = tuple(int(v) for v in rng.integers(0, p, 2))
            if (s.g0[0] * xp[1] - s.g0[1] * xp[0]) % p: break
        s.xp = xp; s.xpL = np.array([xp[0], xp[1], 0, 0, 0], dtype=np.int64)
        # N basis as Lie vectors: g0, Z, R...
        s.Nb = [np.array([s.g0[0], s.g0[1], 0, 0, 0])] + [np.array([0, 0, 1, 0, 0])] + [np.array(r) for r in R]
        # enumerate Q via section: coefficients on X0, X1, Z, R
        dims = 3 + len(R)
        T = np.indices((p,) * dims).reshape(dims, -1).T
        lift = np.zeros((len(T), 5), dtype=np.int64); lift[:, :3] = T[:, :3]
        for i, r in enumerate(R): lift = (lift + np.outer(T[:, 3 + i], r)) % p
        s.lift = lift % p; s.lift_idx = G.idx(s.lift)
        # chart: v = alpha g0 + x x'
        M = np.array([[s.g0[0], xp[0]], [s.g0[1], xp[1]]]); det = int(round(np.linalg.det(M))) % p; iv = F.inv(det)
        Minv = (np.array([[M[1, 1], -M[0, 1]], [-M[1, 0], M[0, 0]]]) * iv) % p
        ax = (s.lift[:, :2] @ Minv.T) % p
        s.x = ax[:, 1]
        nl = rc.bch(s.lift, (-s.x[:, None] * s.xpL[None]) % p, F)
        s.ncoord = np.array([s.ncoords(v) for v in nl], dtype=np.int64)
        cnt = np.zeros((p,) * s.m + (p,), dtype=np.int64)
        np.add.at(cnt, tuple(s.ncoord.T) + (s.x,), 1); assert (cnt == 1).all(), 'chart not a bijection'
        # conjugation matrix B on N-coordinates: b n b^-1
        B = np.zeros((s.m, s.m), dtype=np.int64)
        for i, nb in enumerate(s.Nb):
            c = rc.bch(rc.bch(s.xpL, nb % p, F), (-s.xpL) % p, F)
            B[:, i] = s.ncoords(c)
        s.B = B % p
        s.BI = (s.B - np.eye(s.m, dtype=np.int64)) % p
    def ncoords(s, v):
        """coordinates (alpha, z, r...) of a Lie vector v in span(g0, Z, R) + C (asserts membership)"""
        p = s.p
        basis = [tuple(int(t) for t in b) for b in s.Nb] + list(s.C)
        c = coords_in(basis, [int(t) % p for t in v], p)
        assert c is not None, 'not in N'
        return c[:s.m]
    def phase_forms(s, y, D):
        """public coefficient vectors a_1..a_D (phase = sum_j x^j a_j . n0) of the front-end state with outcome y,
        sign convention -1 (numpy FFT orientation; asserted on the true states)"""
        p = s.p; F = s.F; y = np.asarray(y, dtype=np.int64)
        cks = []; Mk = np.eye(s.m, dtype=np.int64)
        for k in range(1, 4):
            cks.append((-(Mk.T @ y)) % p); Mk = (Mk @ s.BI) % p
        c1, c2, c3 = cks
        a3 = (c3 * F.i6) % p; a2 = ((c2 - c3) * F.i2) % p; a1 = (c1 - c2 * F.i2 + c3 * pow(3, -1, p)) % p
        return [a1, a2, a3][:D] if D == 3 else [a1, (c2 * F.i2) % p]

def is_branch(O, Q, D, rng, stats, eta_true=None, max_eq=None, max_copies=20000):
    """IS HPGP' degree reduction in Q.  Returns a certified generator (Lie vector in L) of H mod C, or None."""
    F, p, m = O.F, O.F.p, Q.m
    n0_true = None
    if eta_true is not None:
        et = np.asarray(eta_true, dtype=np.int64) % p
        xe = None
        # scale eta so that its chart x-coordinate is 1
        M = np.array([[Q.g0[0], Q.xp[0]], [Q.g0[1], Q.xp[1]]]); iv = F.inv(int(round(np.linalg.det(M))) % p)
        xe = ((-M[1, 0] * et[0] + M[0, 0] * et[1]) * iv) % p
        if xe:
            et1 = (et * F.inv(int(xe))) % p
            n0_true = np.array(Q.ncoords(rc.bch(et1, (-Q.xpL) % p, F)), dtype=np.int64)
    g3 = rc.g3(p)
    N1 = g3 if D == 3 else 3                    # copies per top-degree merge (one diagonal equation)
    copies0 = O.nq
    def fresh_state():
        vec = O.coset_state(Q.lift_idx, rng)
        arr = np.zeros((p,) * m + (p,), dtype=complex); arr[tuple(Q.ncoord.T) + (Q.x,)] = vec
        Fy = np.fft.fftn(arr, axes=tuple(range(m)))
        pr = (np.abs(Fy) ** 2).sum(axis=m).ravel(); pr = pr / pr.sum()
        y = np.unravel_index(int(rng.choice(p ** m, p=pr)), (p,) * m)
        psi = Fy[y]; psi = psi / np.linalg.norm(psi)
        forms = Q.phase_forms(y, D)
        if n0_true is not None:
            E = rc.phase_exponents(psi, F)
            pred = np.array([sum(int(forms[j] @ n0_true) * pow(x, j + 1, p) for j in range(D)) % p for x in range(p)])
            stats['is_frontend_fail'] = stats.get('is_frontend_fail', 0) + int(((E - pred) % p).any())
        return dict(psi=psi, a=[np.asarray(a, dtype=np.int64) % p for a in forms], D=D)
    def merge(sts, dl):
        use = [(s_, d) for s_, d in zip(sts, dl) if d % p]
        Dg = use[0][0]['D']
        xs = [int(rng.choice(p, p=np.abs(s_['psi']) ** 2 / (np.abs(s_['psi']) ** 2).sum())) for s_, _ in use]
        t0 = xs[0] * F.inv(use[0][1]) % p
        x0 = [(x - t0 * d) % p for x, (_, d) in zip(xs, use)]
        ts = np.arange(p); psi = np.ones(p, dtype=complex)
        for (s_, d), xo in zip(use, x0): psi = psi * s_['psi'][(xo + d * ts) % p]
        psi = psi / np.linalg.norm(psi)
        newa = []
        from math import comb
        for j in range(1, Dg + 1):
            v = np.zeros(m, dtype=np.int64)
            for (s_, d), xo in zip(use, x0):
                for jp in range(j, Dg + 1):
                    v = (v + comb(jp, j) * pow(xo, jp - j, p) * pow(d, j, p) * s_['a'][jp - 1]) % p
            newa.append(v)
        assert not newa[-1].any(), 'top coefficient not cancelled'
        return dict(psi=psi, a=newa[:-1], D=Dg - 1)
    def weights(cols, d):
        """nonzero dl with sum dl_i^d cols_i = 0 (cols in F_p^m), Lemma B; returns None if more states needed"""
        nz = [tuple(int(x) for x in c) for c in cols]
        bas = span(nz, p, m); r = len(bas)
        if r == 0: return [1] + [0] * (len(cols) - 1)
        cc = [coords_in(bas, c, p) for c in nz]
        if r == 1:
            need = 3 if d == 2 else g3
            if len(cols) < need: return None
            w = rc.solve1([c[0] for c in cc[:need]], d, F, rng); return w + [0] * (len(cols) - need)
        if r == 2:
            g = 3 if d == 2 else g3
            if len(cols) < g * g: return None
            w = rc.solve2([tuple(c) for c in cc[:g * g]], d, g, F, rng); return w + [0] * (len(cols) - g * g)
        raise RuntimeError('rank %d top coefficients' % r)
    def reduce_to(Dtarget):
        """produce one state of degree Dtarget from fresh copies"""
        if Dtarget == D: return fresh_state()
        sts = []
        while True:
            sts.append(reduce_to(Dtarget + 1))
            w = weights([s_['a'][Dtarget] for s_ in sts], Dtarget + 1)
            if w is not None: return merge(sts, w)
    eqs = []; rhs = []
    max_eq = max_eq or 4 * m
    while len(eqs) < max_eq and O.nq - copies0 < max_copies:
        st = reduce_to(1)
        a1 = st['a'][0]
        pr = np.abs(np.fft.fft(st['psi'])) ** 2; pr = pr / pr.sum()
        z = int(rng.choice(p, p=pr))
        if n0_true is not None:
            stats['is_eq_wrong'] = stats.get('is_eq_wrong', 0) + int((int(a1 @ n0_true) - z) % p != 0)
        eqs.append([int(x) for x in a1]); rhs.append(z)
        if len(span(eqs, p, m)) == m:
            sol = rc.solve_mod(eqs, rhs, p)
            if sol is None: break
            nvec = np.zeros(5, dtype=np.int64)
            for c, b in zip(sol, Q.Nb): nvec = (nvec + c * b) % p
            h = rc.bch(nvec, Q.xpL, F) % p                 # n0 * b, lifted (any lift: C lies in H)
            stats['is_equations'] = stats.get('is_equations', 0) + len(eqs)
            return tuple(int(v) for v in h) if O.classical_in_H(h) else None
    stats['is_equations'] = stats.get('is_equations', 0) + len(eqs)
    return None

# ---------------- Algorithm HSP23 ----------------
GAMMA2 = [(0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
GAMMA3 = [(0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
L_ALL = [tuple(int(i == j) for j in range(5)) for i in range(5)]

def hsp23(O, rng, stats, eta_true=None):
    F, p = O.F, O.F.p
    s = ab_hsp(O, GAMMA2, [], rng)                              # s = h cap gamma_2
    s3 = intersect(s, GAMMA3, p)
    branch = None
    if len(s3) == 0:
        if len(s) == 1: branch = 'gamma2 line (P1)'; out = s
        else:
            branch = 'F23'
            if eta_true is None: out = []; stats['f23_not_simulated_trivial'] = stats.get('f23_not_simulated_trivial', 0) + 1
            else:
                gen, att = f23_branch(O, eta_true, rng, stats=stats); out = gen
                stats['f23_attempts'] = stats.get('f23_attempts', 0) + att
    elif len(s3) == 1:
        q = s3[0]; g0 = (q[3], q[4])
        T = ab_hsp(O, [(g0[0], g0[1], 0, 0, 0)] + GAMMA2, [q], rng)
        if any(v[0] or v[1] for v in T): branch = 'AbHSP on M_g0/<q>'; out = T
        elif len(s) == 2: branch = 'plane (P3)'; out = s
        else:
            branch = 'IS fil4'
            Q = SemiQuot(F, O.G, [q], g0, rng)
            h = is_branch(O, Q, 3, rng, stats, eta_true=eta_true)
            out = span([h, q], p) if h is not None else s
    else:
        if len(s) == 3: branch = 'AbHSP on G/gamma2'; out = ab_hsp(O, L_ALL, GAMMA2, rng)
        else:
            while True:
                g0 = tuple(int(v) for v in rng.integers(0, p, 2))
                if any(g0): break
            T = ab_hsp(O, [(g0[0], g0[1], 0, 0, 0)] + GAMMA2, GAMMA3, rng)
            if any(v[0] or v[1] for v in T): branch = 'AbHSP on M_g0/gamma3'; out = T
            else:
                branch = 'IS heis'
                Q = SemiQuot(F, O.G, GAMMA3, g0, rng)
                h = is_branch(O, Q, 2, rng, stats, eta_true=eta_true)
                out = span([h] + GAMMA3, p) if h is not None else s
    return span(out, p), branch

def intersect(A, B, p):
    if not A or not B: return []
    # x = sum a_i A_i in span(B): solve
    k = len(A); Bm = [list(b) for b in B]
    basis = []
    for t in itertools.product(range(p), repeat=k):
        v = [int(x) % p for x in np.array(t) @ np.array(A)]
        if any(v) and len(span(Bm + [v], p)) == len(span(Bm, p)): basis.append(v)
    return span(basis, p)

# ---------------- random subgroup of each type ----------------
def rand_type(t, p, rng):
    def nz2():
        while True:
            v = rng.integers(0, p, 2)
            if v.any(): return [int(x) for x in v]
    e = nz2(); eta = e + [int(x) for x in rng.integers(0, p, 3)]
    ez = [0, 0, 0, e[0], e[1]]
    q = [0, 0, 0] + nz2(); c = [int(x) for x in rng.integers(0, p, 2)]
    zc = [0, 0, 1] + c
    if t == 'trivial': return [], None
    if t == 'central line': return [q], None
    if t == 'line Z+c': return [zc], None
    if t == 'gamma3': return GAMMA3, None
    if t == 'plane Z+c,q': return [zc, q], None
    if t == 'gamma2': return GAMMA2, None
    if t == 'hard cyclic': return [eta], eta
    if t == '(b) generic':
        while (q[3] * e[1] - q[4] * e[0]) % p == 0: q = [0, 0, 0] + nz2()
        return [eta, q], eta
    if t == '(b) special': return [eta, ez], eta
    if t == '(c)': return [eta] + GAMMA3, eta
    if t == '(d)': return [eta, zc, ez], eta
    if t == '(e)': return [eta] + GAMMA2, eta
    if t == 'G': return L_ALL, None

TYPES = ['trivial', 'central line', 'line Z+c', 'gamma3', 'plane Z+c,q', 'gamma2', 'hard cyclic', '(b) generic',
         '(b) special', '(c)', '(d)', '(e)', 'G']

def is_subalgebra(B, p):
    sp = span(B, p)
    for a in B:
        for b in B:
            v = [int(x) for x in rc.br(np.array(a)[None], np.array(b)[None], p)[0]]
            if len(span(sp + [v], p)) > len(sp): return False
    return True

def main():
    p, nper, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    types = sys.argv[4].split(',') if len(sys.argv) > 4 else TYPES
    F = rc.Field(p); G = rc.Group(F); rng = np.random.default_rng(seed)
    print('p = %d, %d instances per type' % (p, nper), flush=True)
    tot = {}
    for t in types:
        for it in range(nper):
            hb, eta = rand_type(t, p, rng)
            assert is_subalgebra(hb, p)
            O = Oracle(F, G, hb); stats = dict(copies=0, inadmissible_batches=0, spoiled_copies=0)
            t0 = time.time()
            out, branch = hsp23(O, rng, stats, eta_true=eta)
            ok = same_space(out, hb, p) if hb else (out == [])
            if t == 'trivial': ok = (out == [])
            qq = O.nq + stats.get('copies', 0)       # e2e copies are counted in stats['copies']
            key = (t, branch)
            d = tot.setdefault(key, dict(n=0, correct=0, wrong=0, quantum=0, classical=0))
            d['n'] += 1; d['correct'] += int(ok); d['wrong'] += int(not ok)
            d['quantum'] += qq; d['classical'] += O.nc
            diag = {k: v for k, v in stats.items() if k not in ('copies', 'inadmissible_batches', 'spoiled_copies', 'etac_maxprob')}
            print('  %-14s branch %-22s correct %-5s quantum queries %6d classical %3d  %s  (%.1f s)' %
                  (t, branch, ok, qq, O.nc, diag, time.time() - t0), flush=True)
    print('SUMMARY p=%d' % p)
    for (t, b), d in tot.items():
        print('  %-14s %-22s instances %d correct %d WRONG %d  mean quantum %.0f  mean classical %.1f' %
              (t, b, d['n'], d['correct'], d['wrong'], d['quantum'] / d['n'], d['classical'] / d['n']))

if __name__ == '__main__':
    main()
