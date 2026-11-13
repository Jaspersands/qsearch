"""Referee (2026-11-13), independent end-to-end check of Algorithm HSP23 over EVERY subgroup of free23 at a prime p.
AI-written, pending human review.  Imports nothing from the audited folders (optional --routeA uses the F23 referee's
e2e.py, read-only, for genuine Route-A runs on hard cyclic H; that part is NOT independent of the audited checks).
Finite check only (falsification).

Model: standard oracle f(g) = label of the left coset gH (explicit table).  The algorithm sees f and public data only:
  * AbHSP(a, C): Fourier sampling of t -> f(exp t) on a complement of C in a (exact outcome law of one coset state),
    Las Vegas certification of the null space by classical queries f(exp v) == f(1);
  * IS branch in Q = G/C: coset states of H built from f (one random level set), mapped to IS chart (x, n) with
    g = n * b^x, n in N = exp(F_p g0 + gamma_2), b = exp(x'); the state is CHECKED to be an IS level-set state
    sum_x |x>|u + v(x)> with v(x) = sum_{i<x} B^i v(1) whenever H/C has order p and is not in N/C (the IS promise);
    the HPGP' solver is replaced by a small-p brute-force candidate elimination that uses only exact measurement
    statistics of the true states (NOT IS Thm 5; the theorem itself is cited, not tested);
  * Route A: replaced by a stand-in (cited Theorem F23'), which returns the true generator with prob 1/2 per attempt
    if H is hard cyclic and an adversarial random candidate otherwise; certification by one classical query.
Usage: python hsp23_indep.py p seed [max subgroups per type]
"""
import sys, itertools, time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

p = int(sys.argv[1]); SEED = int(sys.argv[2]); MAXH = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
rng = np.random.default_rng(SEED)
i2 = pow(2, -1, p); i12 = pow(12, -1, p)
N5 = p ** 5
PW = np.array([p ** 4, p ** 3, p ** 2, p, 1], dtype=np.int64)
ALL = np.indices((p,) * 5).reshape(5, -1).T.astype(np.int64)

def br(a, b):
    a = np.asarray(a, dtype=np.int64); b = np.asarray(b, dtype=np.int64)
    out = np.zeros(np.broadcast(a, b).shape, dtype=np.int64)
    out[..., 2] = a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]
    out[..., 3] = a[..., 0] * b[..., 2] - a[..., 2] * b[..., 0]
    out[..., 4] = a[..., 1] * b[..., 2] - a[..., 2] * b[..., 1]
    return out % p

def mul(a, b):  # exp(a) exp(b) = exp(mul(a,b)), class-3 BCH
    a = np.asarray(a, dtype=np.int64) % p; b = np.asarray(b, dtype=np.int64) % p
    ab = br(a, b)
    return (a + b + i2 * ab + i12 * (br(a, ab) + br(b, (-ab) % p))) % p

def idx(v): return (np.asarray(v, dtype=np.int64) % p) @ PW

# ---------- linear algebra mod p ----------
def rref(M):
    M = [[int(x) % p for x in r] for r in M]; r = 0; piv = []
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        q = next((i for i in range(r, len(M)) if M[i][c]), None)
        if q is None: continue
        M[r], M[q] = M[q], M[r]; iv = pow(M[r][c], -1, p); M[r] = [x * iv % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    return M[:r], piv

def span(vs):
    vs = [list(v) for v in vs if any(int(x) % p for x in v)]
    return tuple(tuple(r) for r in rref(vs)[0]) if vs else ()

def inspan(B, v): return len(span(list(B) + [v])) == len(span(B))
def subset(A, B): return all(inspan(B, a) for a in A)

def nullspace(A, n):
    if not A: return [tuple(int(i == j) for j in range(n)) for i in range(n)]
    R, piv = rref(A); out = []
    for fv in [j for j in range(n) if j not in piv]:
        x = [0] * n; x[fv] = 1
        for row, pc in zip(R, piv): x[pc] = (-row[fv]) % p
        out.append(tuple(x))
    return out

def intersect(A, B):
    """basis of span(A) cap span(B) in F_p^5"""
    A = list(span(A)); B = list(span(B))
    if not A or not B: return ()
    M = [[A[i][k] for i in range(len(A))] + [(-B[j][k]) % p for j in range(len(B))] for k in range(5)]
    ns = nullspace(M, len(A) + len(B))
    return span([tuple(sum(c[i] * A[i][k] for i in range(len(A))) % p for k in range(5)) for c in ns])

E = [tuple(int(i == j) for j in range(5)) for i in range(5)]
GAMMA2 = span(E[2:]); GAMMA3 = span(E[3:])

# ---------- subalgebras (all subspaces in RREF, closure test) ----------
def all_subalgebras():
    out = []
    for k in range(6):
        for piv in itertools.combinations(range(5), k):
            free = [(i, c) for i in range(k) for c in range(piv[i] + 1, 5) if c not in piv]
            for vals in itertools.product(range(p), repeat=len(free)):
                B = [[0] * 5 for _ in range(k)]
                for i in range(k): B[i][piv[i]] = 1
                for (i, c), x in zip(free, vals): B[i][c] = x
                ok = all(inspan(B, br(B[i], B[j])) for i in range(k) for j in range(i + 1, k))
                if ok: out.append(tuple(tuple(r) for r in B))
    return out

def classify(h):
    """type number 1..13 of Lemma T, computed from the subalgebra directly"""
    s = intersect(h, GAMMA2); s3 = intersect(h, GAMMA3); d1 = len(h) - len(s)
    if d1 == 2: return 13
    if d1 == 0:
        return {(0, 0): 1, (1, 1): 2, (1, 0): 3, (2, 2): 4, (2, 1): 5, (3, 2): 6}[(len(s), len(s3))]
    eta = next(v for v in h if not inspan(GAMMA2, v))
    eZ = br(eta, E[2])
    if len(s) == 0: return 7
    if len(s) == 1: return 9 if inspan(s, eZ) else 8
    if len(s) == 2: return 10 if len(s3) == 2 else 11
    return 12

def group_check(h):
    """exp(h) is a subgroup: closed under right multiplication by exp(basis)"""
    pts = np.array(list(itertools.product(range(p), repeat=len(h))), dtype=np.int64) @ np.array(h, dtype=np.int64) % p \
        if h else np.zeros((1, 5), dtype=np.int64)
    S = set(idx(pts).tolist())
    for b in h:
        if not set(idx(mul(pts, np.broadcast_to(np.array(b), pts.shape))).tolist()) <= S: return False
    return len(S) == p ** len(h)

# ---------- oracle ----------
class Oracle:
    def __init__(s, h):
        rows, cols = [], []
        for b in h:
            rows.append(np.arange(N5)); cols.append(idx(mul(ALL, np.broadcast_to(np.array(b), ALL.shape))))
        if rows:
            A = coo_matrix((np.ones(N5 * len(rows)), (np.concatenate(rows), np.concatenate(cols))), shape=(N5, N5))
            _, s.lab = connected_components(A, directed=True, connection='weak')
        else:
            s.lab = np.arange(N5)
        s.one = s.lab[0]; s.nq = 0; s.nc = 0
    def f(s, V): return s.lab[idx(V)]
    def member(s, v): s.nc += 1; return bool(s.lab[idx(v)] == s.one)
    def level_set(s, V, rng):
        """one quantum query: random level set of f restricted to the point list V (indices into V)"""
        s.nq += 1
        vals = s.f(V); x = int(rng.integers(len(V)))
        return np.nonzero(vals == vals[x])[0]

def complement(a, C):
    cur = list(span(C)); comp = []
    for v in span(a):
        if not inspan(cur, v): comp.append(v); cur = list(span(cur + [v]))
    return comp

def ab_hsp(O, a, C, stats):
    comp = complement(a, C); k = len(comp)
    if k == 0: return span(C)
    T = np.indices((p,) * k).reshape(k, -1).T.astype(np.int64)
    V = T @ np.array(comp, dtype=np.int64) % p
    samples = []
    for it in range(200):
        L = O.level_set(V, rng)
        ind = np.zeros(p ** k); ind[L] = 1
        pr = np.abs(np.fft.fftn(ind.reshape((p,) * k))) ** 2; pr = pr.ravel() / pr.sum()
        y = np.unravel_index(int(rng.choice(p ** k, p=pr)), (p,) * k)
        samples.append([int(t) for t in y])
        cand = [tuple(int(x) for x in (np.array(t) @ np.array(comp, dtype=np.int64)) % p) for t in nullspace(samples, k)]
        if all(O.member(v) for v in cand):
            return span(list(C) + cand)
    raise RuntimeError('AbHSP did not certify')

# ---------- IS branch in Q = G/C ----------
def is_branch(O, C, g0, h_true, stats):
    """IS chart over N = exp(F_p g0 + gamma_2)/C, b = exp(x').  Returns a certified element or None."""
    M = span([g0] + list(GAMMA2))
    xp = E[0] if not inspan([g0] + list(GAMMA2), E[0]) else E[1]
    ncomp = complement(M, C)                       # coordinates of N/C (additive, since [M,M] in C)
    m = len(ncomp)
    # coordinates of Lie vectors in M modulo C, w.r.t. ncomp: t -> (t @ Pm)[:m], via an invertible minor
    Bas = [list(v) for v in ncomp] + [list(c) for c in C]; r = len(Bas)
    cols = next(cs for cs in itertools.combinations(range(5), r)
                if len(span([[Bas[i][c] for c in cs] for i in range(r)])) == r)
    S = [[Bas[i][c] for c in cols] + [int(i == j) for j in range(r)] for i in range(r)]
    Sinv = np.array([row[r:] for row in rref(S)[0]], dtype=np.int64)        # S^{-1}: rows of rref([S|I])
    Pm = np.zeros((5, r), dtype=np.int64)
    for a, c in enumerate(cols): Pm[c, :] = Sinv[a, :]
    def ncoord_v(T):
        T = np.atleast_2d(np.asarray(T, dtype=np.int64) % p)
        co = (T @ Pm) % p
        assert np.array_equal((co @ np.array(Bas, dtype=np.int64)) % p, T), 'not in M'
        return co[:, :m]
    def ncoord(t): return tuple(int(x) for x in ncoord_v(t)[0])
    det = (g0[0] * xp[1] - g0[1] * xp[0]) % p; idet = pow(det, -1, p)
    Xall = ((g0[0] * ALL[:, 1] - g0[1] * ALL[:, 0]) * idet) % p
    Nall = ncoord_v(mul(ALL, (-Xall[:, None] * np.array(xp, dtype=np.int64)[None, :]) % p))
    def chart(i): return int(Xall[i]), tuple(int(x) for x in Nall[i])
    # B = conjugation by b on N/C, columns B e_j
    Bm = np.zeros((m, m), dtype=np.int64)
    for j in range(m):
        conj = mul(mul(np.array(xp), np.array(ncomp[j])), (-np.array(xp)) % p)
        Bm[:, j] = ncoord(conj)
    Hbar_ok = None
    # promise status (truth, diagnostics only): |H/C| and whether H/C is inside N/C
    hC = span(list(h_true) + list(C)); ordbar = len(hC) - len(C)
    promise = (ordbar == 1 and not subset(h_true, M))
    stats['is_calls'] = stats.get('is_calls', 0) + 1
    stats['is_promise'] = stats.get('is_promise', 0) + int(promise)
    if not promise:
        stats['is_nonpromise_trivial'] = stats.get('is_nonpromise_trivial', 0) + int(ordbar == 0)
        stats['is_nonpromise_other'] = stats.get('is_nonpromise_other', 0) + int(ordbar != 0)
    # coset states from f, mapped to the chart; check IS level-set form
    states = []
    def fresh():
        L = O.level_set(ALL, rng)
        cnt = {}
        for i in L:
            key = chart(i); cnt[key] = cnt.get(key, 0) + 1
        return cnt
    def check_is_form(cnt):
        xs = {}
        for (x, n), c in cnt.items(): xs.setdefault(x, []).append((n, c))
        if sorted(xs) != list(range(p)) or any(len(v) != 1 for v in xs.values()): return None
        mult = {v[0][1] for v in xs.values()}
        if len(mult) != 1: return None
        u = np.array(xs[0][0][0]); v1 = (np.array(xs[1][0][0]) - u) % p
        acc = np.zeros(m, dtype=np.int64); Bi = np.eye(m, dtype=np.int64)
        for x in range(p):
            if tuple((u + acc) % p) != xs[x][0][0]: return False
            acc = (acc + Bi @ v1) % p; Bi = (Bm @ Bi) % p
        return True
    # brute-force candidate elimination with exact measurement statistics (small p only)
    cands = [np.array(c, dtype=np.int64) for c in itertools.product(range(p), repeat=m)]
    def vpoly(v1):
        out = []; acc = np.zeros(m, dtype=np.int64); Bi = np.eye(m, dtype=np.int64)
        for x in range(p):
            out.append(acc.copy()); acc = (acc + Bi @ v1) % p; Bi = (Bm @ Bi) % p
        return out
    VP = [vpoly(c) for c in cands]
    alive = list(range(len(cands))); used = 0
    while len(alive) > 1 and used < 60 * len(cands):
        cnt = fresh(); used += 1
        form = check_is_form(cnt)
        if promise:
            stats['is_form_checked'] = stats.get('is_form_checked', 0) + 1
            stats['is_form_fail'] = stats.get('is_form_fail', 0) + int(form is not True)
        # state as dict (x, n) -> amplitude
        tot = sum(cnt.values()); amp = {k: np.sqrt(c / tot) for k, c in cnt.items()}
        ci = alive[int(rng.integers(len(alive)))]
        # projector onto span{ |psi_u^{v'}> : u }, |psi_u> = p^-1/2 sum_x |x>|u + v'(x)>
        # <psi_u|state> = p^-1/2 sum_x amp[(x, u + v'(x))]; group amplitudes by u = n - v'(x)
        byu = {}
        for (x, n), a in amp.items():
            u = tuple((np.array(n) - VP[ci][x]) % p); byu[u] = byu.get(u, 0) + a
        ppass = sum(abs(a) ** 2 for a in byu.values()) / p
        if rng.random() >= ppass: alive.remove(ci)
    stats['is_copies'] = stats.get('is_copies', 0) + used
    c = cands[alive[int(rng.integers(len(alive)))]]
    hh = mul(np.array([int(x) for x in (np.array(ncomp, dtype=np.int64).T @ c) % p]), np.array(xp))  # n_c * b
    if O.member(hh): return tuple(int(x) for x in hh)
    return None

# ---------- Route A stand-in ----------
def routeA_standin(O, h_true, stats, R=6):
    hard = (len(h_true) == 1 and not inspan(GAMMA2, h_true[0]))
    stats['A_calls'] = stats.get('A_calls', 0) + 1; stats['A_hard'] = stats.get('A_hard', 0) + int(hard)
    for att in range(R):
        if hard and rng.random() < 0.5: cand = h_true[0]
        else:
            cand = tuple(int(x) for x in rng.integers(p, size=5))
            if cand[0] == 0 and cand[1] == 0: cand = (1,) + cand[1:]
        if O.member(cand): return cand
    return None

def hsp23(O, h_true, stats):
    s = ab_hsp(O, GAMMA2, (), stats); s3 = intersect(s, GAMMA3)
    if len(s3) == 0:
        if len(s) == 1: return s, 'P1'
        assert len(s) == 0
        c = routeA_standin(O, h_true, stats)
        return (span([c]) if c else ()), 'RouteA'
    if len(s3) == 1:
        q = s3[0]; g0 = (q[3], q[4], 0, 0, 0)
        M = span([g0] + list(GAMMA2))
        T = ab_hsp(O, M, [q], stats)
        if not subset(T, GAMMA2): return T, 'M/q'
        if len(s) == 2: return s, 'plane'
        c = is_branch(O, [q], g0, h_true, stats)
        return (span([c, q]) if c else s), 'IS-fil4'
    if len(s) == 3:
        return ab_hsp(O, E, GAMMA2, stats), 'G/gamma2'
    while True:
        g0 = tuple(int(x) for x in rng.integers(p, size=2)) + (0, 0, 0)
        if g0[0] or g0[1]: break
    M = span([g0] + list(GAMMA2))
    T = ab_hsp(O, M, GAMMA3, stats)
    if not subset(T, GAMMA2): return T, 'M/gamma3'
    c = is_branch(O, list(GAMMA3), g0, h_true, stats)
    return (span([c] + list(GAMMA3)) if c else GAMMA3), 'IS-heis'

def main():
    t0 = time.time()
    subs = all_subalgebras()
    print('p=%d subalgebras=%d (%.1fs)' % (p, len(subs), time.time() - t0), flush=True)
    by = {}
    for h in subs: by.setdefault(classify(h), []).append(h)
    print('type counts:', {t: len(v) for t, v in sorted(by.items())}, flush=True)
    order = []
    for t, v in sorted(by.items()):
        sel = rng.permutation(len(v))[:MAXH]
        order += [subs.index(v[j]) for j in sel]
    res = {}; gfail = 0
    for n, i in enumerate(order):
        h = subs[i]; t = classify(h)
        if not group_check(h): gfail += 1
        O = Oracle(h); st = {}
        out, br_ = hsp23(O, h, st)
        ok = span(out) == span(h)
        key = (t, br_)
        r = res.setdefault(key, dict(n=0, ok=0, nq=0, nc=0))
        r['n'] += 1; r['ok'] += int(ok); r['nq'] += O.nq; r['nc'] += O.nc
        for k, v in st.items(): r[k] = r.get(k, 0) + v
        if not ok: print('WRONG', t, br_, h, out, st, flush=True)
        if n % 500 == 0: print('..', n, '%.0fs' % (time.time() - t0), flush=True)
    print('group_check failures:', gfail)
    print('SUMMARY (type, branch): n ok mean_quantum mean_classical extra')
    for k in sorted(res):
        r = res[k]
        extra = {a: b for a, b in r.items() if a not in ('n', 'ok', 'nq', 'nc')}
        print(k, r['n'], r['ok'], '%.1f' % (r['nq'] / r['n']), '%.1f' % (r['nc'] / r['n']), extra)
    print('WRONG total:', sum(r['n'] - r['ok'] for r in res.values()), ' time %.0fs' % (time.time() - t0))

if __name__ == '__main__':
    main()
