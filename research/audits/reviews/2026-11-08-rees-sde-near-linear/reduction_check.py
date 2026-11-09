"""Dead-pair padding reduction: power-residue PRF key recovery -> diagonal SDE
at arity M = 2a - m + 4 (m = number of PRF queries).  Exact arithmetic mod p.

Instance (kappa, p, theta secret):
  queries gamma_1..gamma_m distinct uniform; eps_i = cos(theta+gamma_i) in Z_kappa.
  Phi: (s, t0, t_1..t_k) -> x = ( g^{-eps_i} (s + gamma_i t0) )_{i<=m}, (t_j)_j, (c t_j)_j
  with the kernel ratio c = d not in P (equivalently the pair of columns is (mu, -mu/d), a dead pair).  Bank Lambda = basis of (im Phi)^perp, a = m+k-2 rows, M = m+2k cols.
Checks: (1) ker Lambda = im Phi exactly; (2) exhaustive kernel enumeration on tiny
instances: every nonzero kernel vector in (P u 0)^M has t=0 and s/t0 solves the
pattern (or anti-pattern); (3) brute-force LP solver on larger p extracts theta.
"""
import sys, random, math

def is_prime(n):
    if n < 2: return False
    for q in range(2, int(n**0.5)+1):
        if n % q == 0: return False
    return True

def gen(p):
    # primitive root
    phi = p-1; fac = []; n = phi; q = 2
    while q*q <= n:
        if n % q == 0:
            fac.append(q)
            while n % q == 0: n //= q
        q += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, phi//q, p) != 1 for q in fac): return g
    raise ValueError

def cos_table(p, kappa, g):
    """cos(y) = index of coset of y mod P (kappa-th powers); -1 for y=0."""
    t = [-1]*p
    h = (p-1)//kappa
    y = 1
    for e in range(p-1):
        t[y] = e % kappa
        y = y*g % p
    return t

def nullspace_rows(cols, p, M):
    """Given list of column vectors (length M each) spanning V, return rows spanning V^perp."""
    # row-reduce the matrix whose rows are the given vectors (as vectors in F_p^M)
    rows = [list(c) for c in cols]
    piv = []
    r = 0
    for c in range(M):
        pr = None
        for i in range(r, len(rows)):
            if rows[i][c] % p: pr = i; break
        if pr is None: continue
        rows[r], rows[pr] = rows[pr], rows[r]
        inv = pow(rows[r][c], p-2, p)
        rows[r] = [v*inv % p for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [(a - f*b) % p for a, b in zip(rows[i], rows[r])]
        piv.append(c); r += 1
    rows = rows[:r]
    free = [c for c in range(M) if c not in piv]
    # null space of the row space: for each free column build vector
    out = []
    for f in free:
        v = [0]*M; v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-rows[i][f]) % p
        out.append(v)
    return out, r

def build(p, kappa, g, cos, theta, m, k, rng):
    gam = rng.sample(range(p), m)
    eps = []
    for ga in gam:
        y = (theta + ga) % p
        if y == 0: return None  # oracle returned 0: key known directly
        eps.append(cos[y])
    eta = [pow(g, (-e) % kappa, p) for e in eps]       # eta_i in g^{-eps_i} P
    c = None
    for cand in range(2, p):
        if cos[cand] != 0: c = cand; break             # kernel ratio d not in P (column ratio -1/d, so -(-1/d)=1/d not in P)
    M = m + 2*k
    # columns of Phi as vectors in F_p^M (params: s, t0, t_1..t_k)
    phi_s  = [eta[i] % p for i in range(m)] + [0]*(2*k)
    phi_t0 = [eta[i]*gam[i] % p for i in range(m)] + [0]*(2*k)
    phis = [phi_s, phi_t0]
    for j in range(k):
        v = [0]*M; v[m+j] = 1; v[m+k+j] = c; phis.append(v)
    rows, rk = nullspace_rows(phis, p, M)              # rows span (im Phi)^perp
    assert rk == k+2, rk
    a = M - rk
    assert len(rows) == a == m + k - 2
    return dict(gam=gam, eps=eps, eta=eta, c=c, M=M, a=a, m=m, k=k, Lam=rows, Phi=phis)

def Lam_apply(Lam, x, p):
    return [sum(r[i]*x[i] for i in range(len(x))) % p for r in Lam]

def in_P0(cos, y):
    return y == 0 or cos[y] == 0

def exhaustive_kernel(inst, p, cos):
    """Enumerate im Phi fully (p^{k+2} vectors); check structure of every P0-solution."""
    k, m, M = inst['k'], inst['m'], inst['M']
    Phi = inst['Phi']
    nsol = 0; bad = 0; keys = set()
    import itertools
    for params in itertools.product(range(p), repeat=k+2):
        if not any(params): continue
        x = [sum(params[j]*Phi[j][i] for j in range(k+2)) % p for i in range(M)]
        if all(in_P0(cos, xi) for xi in x):
            nsol += 1
            s, t0 = params[0], params[1]; t = params[2:]
            if any(t): bad += 1; continue
            if t0 == 0: bad += 1; continue
            keys.add(s * pow(t0, p-2, p) % p)
            assert Lam_apply(inst['Lam'], x, p) == [0]*inst['a']
    return nsol, bad, keys

def lp_bruteforce(inst, p, cos, g, kappa):
    """The only solver we have: for each coset class of t0 and each s, test x in (P u 0)^M.
    Returns list of (s, t0) with x nonzero.  Vectorised with numpy on the Legendre table."""
    import numpy as np
    gam = np.array(inst['gam'], dtype=np.int64); eta = np.array(inst['eta'], dtype=np.int64)
    ok = np.array([1 if (y == 0 or cos[y] == 0) else 0 for y in range(p)], dtype=np.int8)
    sols = []
    s = np.arange(p, dtype=np.int64)
    for e in range(kappa):
        t0 = pow(g, e, p)
        good = np.ones(p, dtype=bool)
        for i in range(len(gam)):
            xi = (eta[i] * ((s + gam[i]*t0) % p)) % p
            good &= ok[xi].astype(bool)
        for sv in np.nonzero(good)[0]:
            sols.append((int(sv), t0))
    return sols

def main():
    rng = random.Random(20261108)
    out = []
    # ---- (2) exhaustive tiny instances
    for (kappa, p, m, k) in [(2, 29, 6, 2), (2, 37, 7, 2), (3, 31, 5, 2), (3, 43, 6, 2), (4, 29, 6, 2)]:
        assert is_prime(p) and (p-1) % kappa == 0
        g = gen(p); cos = cos_table(p, kappa, g)
        for trial in range(3):
            theta = rng.randrange(p)
            inst = build(p, kappa, g, cos, theta, m, k, rng)
            if inst is None: out.append(f"exh kappa={kappa} p={p}: oracle hit zero, key direct"); continue
            nsol, bad, keys = exhaustive_kernel(inst, p, cos)
            # anti-pattern keys: those K' != theta are allowed only if they match pattern shifted by a constant class
            shifted = set()
            for K in keys:
                d = set()
                for ga, e in zip(inst['gam'], inst['eps']):
                    y = (K + ga) % p
                    if y: d.add((cos[y] - e) % kappa)
                shifted.add((K, tuple(sorted(d))))
            out.append(f"exh kappa={kappa} p={p} m={m} k={k} a={inst['a']} M={inst['M']} theta={theta}: "
                       f"P0-kernel-solutions={nsol} with_t_nonzero_or_t0_zero={bad} keys={sorted(keys)} "
                       f"shift-classes={sorted(shifted)}")
            assert bad == 0 and theta in keys
            for K, d in shifted: assert len(d) <= 1, (K, d)
    # ---- (3) brute-force solver on larger p, extraction of theta
    for (kappa, p, lam, k) in [(2, 1000003, 4, 40), (2, 2000003, 6, 200), (3, 1000033, 4, 60), (4, 1000037, 3, 30)]:
        assert is_prime(p) and (p-1) % kappa == 0, (p, kappa)
        g = gen(p); cos = cos_table(p, kappa, g)
        m = math.ceil(math.log(p, kappa)) + lam
        for trial in range(3):
            theta = rng.randrange(p)
            inst = build(p, kappa, g, cos, theta, m, k, rng)
            if inst is None: out.append("oracle zero"); continue
            sols = lp_bruteforce(inst, p, cos, g, kappa)
            keys = set()
            for s, t0 in sols:
                x = [inst['eta'][i]*((s + inst['gam'][i]*t0) % p) % p for i in range(m)] + [0]*(2*inst['k'])
                assert any(x) and all(in_P0(cos, xi) for xi in x)
                assert Lam_apply(inst['Lam'], x, p) == [0]*inst['a']
                keys.add(s*pow(t0, p-2, p) % p)
            out.append(f"bf kappa={kappa} p={p} m={m} k={k} a={inst['a']} M={inst['M']} 2a-M={2*inst['a']-inst['M']} "
                       f"theta={theta}: solver-solutions={len(sols)} recovered-keys={sorted(keys)} ok={theta in keys}")
            assert theta in keys
    print("\n".join(out))

if __name__ == "__main__":
    main()
