# s2a: an independent implementation of the algorithm of Theorem thm:app-s2-main
# (Phase 0 symmetric scalars with J = kappa(k+3), K_j = ceil(2 kappa^{j+1} tau);
# Phase 1 = Lemma lem:app-s2-tensor + Lemma lem:app-s2-witness + Bezout + exact check),
# run on random and adversarial columns.  Finite check only (falsification).
# Run: nice -n 19 timeout 900 /opt/anaconda3/bin/python -I schedule2_run.py
import random, math, sys
import sympy
from sympy.ntheory.residue_ntheory import nthroot_mod
random.seed(9112026)

def nullvec(cols, p):
    """nonzero c with sum_b c_b cols[b] = 0 (cols: list of length-n vectors), or None."""
    n = len(cols[0]) if cols else 0
    m = len(cols)
    # matrix A (n x m), columns = cols; row reduce
    A = [[cols[b][r] % p for b in range(m)] for r in range(n)]
    piv = []; row = 0
    for col in range(m):
        pr = None
        for r in range(row, n):
            if A[r][col]:
                pr = r; break
        if pr is None: continue
        A[row], A[pr] = A[pr], A[row]
        inv = pow(A[row][col], p-2, p)
        A[row] = [(x*inv) % p for x in A[row]]
        for r in range(n):
            if r != row and A[r][col]:
                f = A[r][col]
                A[r] = [(x - f*y) % p for x, y in zip(A[r], A[row])]
        piv.append(col); row += 1
        if row == n: break
    free = [c for c in range(m) if c not in piv]
    if not free: return None
    fc = free[0]
    c = [0]*m; c[fc] = 1
    for r, pc in enumerate(piv):
        c[pc] = (-A[r][fc]) % p
    return c

class Field:
    def __init__(self, p, kappa):
        self.p = p; self.k = kappa; self.h = (p-1)//kappa
        self.primes_k = sympy.primefactors(kappa)
    def is_coset_gen(self, x):
        zeta = pow(x, self.h, self.p)
        return all(pow(zeta, self.k//q, self.p) != 1 for q in self.primes_k), zeta
    def set_gen(self, xi):
        self.xi = xi; self.zeta = pow(xi, self.h, self.p)
        self.zpow = {pow(self.zeta, m, self.p): m for m in range(self.k)}
        self.z = [pow(xi, m, self.p) for m in range(self.k)]
    def ind(self, x):
        x %= self.p
        if x == 0: return None
        return self.zpow[pow(x, self.h, self.p)]
    def root(self, w):
        w %= self.p
        if w == 0: return 0
        r = nthroot_mod(w, self.k, self.p)
        assert r is not None and pow(r, self.k, self.p) == w
        return r

def phase0(F, k, stats):
    p, kap = F.p, F.k
    J = kap*(k+3)
    xi = None
    for _ in range(J):
        x = random.randrange(1, p)
        ok, _z = F.is_coset_gen(x)
        if ok: xi = x; break
    if xi is None:
        stats['abort_xi'] += 1; return None
    F.set_gen(xi)
    tau = k + 3 + math.ceil(math.log2(kap))
    t = [pow(2, p-2, p)]
    for j in range(1, kap):
        Kj = math.ceil(2*kap**(j+1)*tau)
        acc = None
        for _ in range(Kj):
            c = random.randrange(p)
            if c in t: continue
            if F.ind(2*F.z[j]*F.z[j]*c) != 0: continue
            if all(F.ind(F.z[i]*F.z[j]*(c + t[i])) == 0 for i in range(j)): acc = c; break
        if acc is None:
            stats['abort_stage'] += 1; return None
        t.append(acc)
    C = [[(F.z[i]*F.z[j]*(t[i]+t[j])) % p for j in range(kap)] for i in range(kap)]
    assert C[0][0] == 1 and all(F.ind(C[i][j]) == 0 for i in range(kap) for j in range(kap))
    return C

def tensor(F, lam, a):
    p, kap = F.p, F.k
    N = (kap-1)*a + 1
    blocks = [list(range(nu*(a+1), (nu+1)*(a+1))) for nu in range(N)]
    cells = []  # per block: dict i -> list of (b, omega)
    Tv = []
    for B in blocks:
        c = nullvec([lam[b] for b in B], p)
        assert c is not None
        bstar = next(x for x in range(len(B)) if c[x])
        inv = pow(c[bstar], p-2, p)
        c = [(x*inv) % p for x in c]
        cl = {i: [] for i in range(kap)}
        for x, b in enumerate(B):
            if c[x] == 0: continue
            i = F.ind(c[x])
            om = 1 if x == bstar else F.root(c[x]*pow(F.z[i], p-2, p))
            assert (F.z[i]*pow(om, kap, p) - c[x]) % p == 0
            cl[i].append((b, om))
        assert any(b == B[bstar] for b, _ in cl[0])
        T = {i: [sum(pow(om, kap, p)*lam[b][r] for b, om in cl[i]) % p for r in range(a)] for i in range(kap)}
        for r in range(a):
            assert sum(F.z[i]*T[i][r] for i in range(kap)) % p == 0
        cells.append(cl); Tv.append(T)
    V = [[Tv[nu][i][r] for i in range(1, kap) for r in range(a)] for nu in range(N)]
    eta = nullvec(V, p)
    assert eta is not None
    nst = next(x for x in range(N) if eta[x])
    inv = pow(eta[nst], p-2, p)
    eta = [(x*inv) % p for x in eta]
    S = {(i, j): [] for i in range(kap) for j in range(kap)}  # (b, omega')
    for nu in range(N):
        if eta[nu] == 0: continue
        jn = F.ind(eta[nu])
        vp = 1 if nu == nst else F.root(eta[nu]*pow(F.z[jn], p-2, p))
        for i in range(kap):
            for b, om in cells[nu][i]:
                S[(i, jn)].append((b, (vp*om) % p))
    return S

def schedule2(p, d, k, lam, a, stats):
    kap = math.gcd(d, p-1)
    F = Field(p, kap)
    C = phase0(F, k, stats)
    if C is None: return None
    S = tensor(F, lam, a)
    used = [b for v in S.values() for b, _ in v]
    assert len(used) == len(set(used)), "cells not disjoint"
    assert len(S[(0, 0)]) > 0
    u = [0]*len(lam)
    for (i, j), lst in S.items():
        th = F.root(C[i][j])
        for b, om in lst:
            u[b] = (th*om) % p
    # Bezout exponent
    dp, qp = d//kap, (p-1)//kap
    t = pow(dp, -1, qp) if qp > 1 else 1
    if t == 0: t = qp
    s = [pow(x, t, p) for x in u]
    ok = any(s) and all(sum(pow(sb, d, p)*lam[b][r] for b, sb in enumerate(s)) % p == 0 for r in range(a))
    if not ok:
        stats['WRONG'] += 1
        return None
    return s

def gen_columns(kind, M, a, p):
    if kind == 'random': return [[random.randrange(p) for _ in range(a)] for _ in range(M)]
    if kind == 'zero': return [[0]*a for _ in range(M)]
    if kind == 'repeat':
        v = [random.randrange(p) for _ in range(a)]; return [v[:] for _ in range(M)]
    if kind == 'e1': return [[1] + [0]*(a-1) for _ in range(M)]
    if kind == 'rank1':
        v = [random.randrange(1, p) for _ in range(a)]
        return [[(random.randrange(p)*x) % p for x in v] for _ in range(M)]
    if kind == 'sparse':
        return [[(random.randrange(p) if random.random() < 0.2 else 0) for _ in range(a)] for _ in range(M)]
    if kind == 'basis':  # e_1..e_a repeated, the Theorem power-sde(iii)-type pattern
        return [[1 if r == (b % a) else 0 for r in range(a)] for b in range(M)]
    if kind == 'smallvals':
        return [[random.choice([0, 1, p-1]) for _ in range(a)] for _ in range(M)]
    raise ValueError(kind)

def run(p, d, k, a, kinds, reps, stats):
    kap = math.gcd(d, p-1)
    M = (a+1)*((kap-1)*a + 1)
    for kind in kinds:
        for _ in range(reps):
            lam = gen_columns(kind, M, a, p)
            stats['runs'] += 1
            s = schedule2(p, d, k, lam, a, stats)
            if s is not None: stats['ok'] += 1

def first_prime(lo, cond):
    p = sympy.nextprime(lo - 1)
    while not cond(p): p = sympy.nextprime(p)
    return p

kinds = ['random', 'zero', 'repeat', 'e1', 'rank1', 'sparse', 'basis', 'smallvals']
cases = []
# kappa = 2 at 16 kappa^{2kappa+2} = 1024 and at 4 kappa^{2kappa+2} = 256 (Remark rem:app-s2-four)
cases.append(('k2-16', first_prime(1024, lambda p: True), 2))
cases.append(('k2-4', first_prime(256, lambda p: True), 2))
cases.append(('k2-d4', first_prime(1024, lambda p: p % 4 == 3), 4))      # kappa = gcd(4,p-1) = 2 < d
cases.append(('k2-d6', first_prime(1024, lambda p: p % 3 == 2), 6))      # kappa = 2, d = 6
# kappa = 3
cases.append(('k3-16', first_prime(16*3**8, lambda p: p % 3 == 1 and p % 2 == 1), 3))
cases.append(('k3-4', first_prime(4*3**8, lambda p: p % 3 == 1), 3))
cases.append(('k3-d9', first_prime(4*3**8, lambda p: p % 9 in (4, 7)), 9))  # kappa = 3, d = 9
# kappa = 4
cases.append(('k4-4', first_prime(4*4**10, lambda p: p % 4 == 1 and p % 8 != 1 or (p % 8 == 1 and math.gcd(4, p-1) == 4)), 4))
cases.append(('k4-16', first_prime(16*4**10, lambda p: p % 4 == 1), 4))
cases.append(('k6-d6', first_prime(4*6**14, lambda p: p % 6 == 1), 6))     # kappa = 6 at 4 kappa^{2kappa+2}

for name, p, d in cases:
    kap = math.gcd(d, p-1)
    stats = {'runs': 0, 'ok': 0, 'WRONG': 0, 'abort_xi': 0, 'abort_stage': 0}
    avals = [1, 2, 3] if kap <= 3 else [1, 2]
    reps = 6 if kap <= 3 else (3 if kap == 4 else 1)
    if kap == 6:
        kk = ['random', 'zero', 'basis']
    else:
        kk = kinds
    for a in avals:
        run(p, d, 1, a, kk, reps, stats)
    print(name, 'p =', p, 'd =', d, 'kappa =', kap, 'p/(16k^(2k+2)) =', round(p/(16*kap**(2*kap+2)), 3), stats, flush=True)
