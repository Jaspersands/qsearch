"""Adaptive (triangular) chain solver of the report, Theorem 2.2, with exact end-to-end checks.

A chain is a list of steps (D, R, K): modulus D | kappa, input classes R subset Z_D (0 in R),
output classes K subset Z_D (0 in K).  Step t needs an RC(D; R -> K) pair (alpha, beta):
  alpha_j + beta_i in {0} u U_{k in K} Q^{(D)}_{k-i-j}  (i in R, j in Z_D),  alpha_0 = 1, beta_0 = 0.
Admissibility: the D_t-classes of a coefficient whose D_{t-1}-class lies in K_{t-1} lie in R_t.
The solver uses at most C(a+L+1, L+1) columns.  Level 0 = a plain dependency modulo U.

The pair finder samples beta as in the second-moment proofs (random beta, then each alpha_j is
any element of X_j found by scanning F_p).  The checker `check_pair` is written separately and
uses only pow(), not the index table.  The final solution is checked with pow() as well.

Usage:
  python adaptive_chain.py demo            # all test cases of report Section 5.2
  python adaptive_chain.py one p kappa a trials CHAIN   CHAIN like "2:0,1:0;4:0,2:0"
Interpreter: /opt/anaconda3/bin/python.
"""
import sys, random, math
import numpy as np
from math import comb

# ---------------------------------------------------------------- field
def prime_factors(n):
    f, d = [], 2
    while d*d <= n:
        if n % d == 0:
            f.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: f.append(n)
    return f

def primroot(p):
    fs = prime_factors(p-1)
    for g in range(2, p):
        if all(pow(g, (p-1)//q, p) != 1 for q in fs): return g

class Field:
    def __init__(self, p):
        self.p = p
        self.g = primroot(p)
        ind = np.full(p, -1, dtype=np.int64)
        x = 1
        for e in range(p-1):
            ind[x] = e; x = x*self.g % p
        self.ind = ind
    def cls(self, x, D):
        x %= self.p
        assert x != 0
        return int(self.ind[x]) % D

def cls_pow(p, g, x, D):
    """independent class computation: the m with (x g^{-m})^{(p-1)/D} = 1"""
    x %= p; assert x
    e = (p-1)//D
    gi = pow(g, p-2, p)
    y = x
    for m in range(D):
        if pow(y, e, p) == 1: return m
        y = y*gi % p
    raise ValueError("no class")

# ---------------------------------------------------------------- pair finder / checker
def find_pair(F, D, R, K, tries=2000, rng=random, zeros=True):
    p = F.p
    xs = np.arange(p, dtype=np.int64)
    Kset = set(k % D for k in K)
    clsD = np.where(F.ind >= 0, F.ind % D, -1)
    Rnz = [i for i in R if i != 0]
    for _ in range(tries):
        beta = {0: 0}
        for i in Rnz: beta[i] = rng.randrange(p)
        alpha = [None]*D
        ok = True
        for j in (list(range(1, D)) + [0]):
            good = np.ones(p, dtype=bool)
            for i in R:
                y = (xs + beta[i]) % p
                cy = clsD[y]
                allowed = np.zeros(D, dtype=bool)
                if i == 0 and j == 0:
                    allowed[0] = True
                    cond = (cy >= 0) & allowed[np.maximum(cy, 0)]
                else:
                    for k in Kset: allowed[(k - i - j) % D] = True
                    cond = ((cy >= 0) & allowed[np.maximum(cy, 0)]) | ((y == 0) & zeros)
                good &= cond
                if not good.any(): break
            idx = np.flatnonzero(good)
            if len(idx) == 0: ok = False; break
            alpha[j] = int(idx[rng.randrange(len(idx))])
        if not ok: continue
        # normalise alpha_0 = 1 (alpha_0 + beta_0 = alpha_0 lies in Q^{(D)}_0, dividing keeps every class)
        s = pow(alpha[0], p-2, p)
        alpha = [a*s % p for a in alpha]
        beta = {i: b*s % p for i, b in beta.items()}
        return alpha, beta
    return find_pair_complete(F, D, R, K)

def find_pair_complete(F, D, R, K):
    """fallback: complete DFS of rectu.c (copied from threshold-6, compiled here); output re-checked by check_pair"""
    import subprocess, os
    here = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ); env['ALLOWDUP'] = '0' if sorted(K) == [0] else '1'
    out = subprocess.run([os.path.join(here, 'rectu'), str(D), ','.join(map(str, R)), ','.join(map(str, K)),
                          str(F.p), str(F.p), '1', '1'], capture_output=True, text=True, env=env).stdout.split()
    if len(out) < 2 or out[1] != 'FEASIBLE': return None
    assert int(out[2].split('=')[1]) == F.g
    bi = out.index('beta'); ai = out.index('alpha')
    beta = dict(zip(R, map(int, out[bi+1:ai]))); alpha = list(map(int, out[ai+1:ai+1+D]))
    return alpha, beta

def check_pair(p, g, D, R, K, alpha, beta):
    if alpha[0] != 1 or beta[0] != 0: return False
    for i in R:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if i == 0 and j == 0:
                if v == 0 or cls_pow(p, g, v, D) != 0: return False
                continue
            if v == 0: continue
            if (cls_pow(p, g, v, D) + i + j) % D not in set(k % D for k in K): return False
    return True

# ---------------------------------------------------------------- linear algebra mod p
class Subspace:
    """echelon basis; reduce(v) is v minus its projection along pivot coordinates"""
    def __init__(self, p, a, vecs=()):
        self.p, self.a = p, a
        self.rows, self.piv, self.raw = [], [], []
        for v in vecs: self.add(v)
    def reduce(self, v):
        p = self.p
        v = [x % p for x in v]
        for r, c in zip(self.rows, self.piv):
            if v[c]:
                f = v[c]; v = [(x - f*y) % p for x, y in zip(v, r)]
        return v
    def contains(self, v): return not any(self.reduce(v))
    def add(self, v):
        w = self.reduce(v)
        if not any(w): return False
        c = next(i for i, x in enumerate(w) if x)
        inv = pow(w[c], self.p-2, self.p); w = [x*inv % self.p for x in w]
        # keep rows fully reduced
        new_rows = []
        for r in self.rows:
            if r[c]:
                f = r[c]; r = [(x - f*y) % self.p for x, y in zip(r, w)]
            new_rows.append(r)
        self.rows = new_rows + [w]; self.piv = self.piv + [c]; self.raw.append(list(v))
        return True
    def dim(self): return len(self.rows)
    def copy(self):
        s = Subspace(self.p, self.a); s.rows = [list(r) for r in self.rows]; s.piv = list(self.piv); s.raw = [list(r) for r in self.raw]
        return s

def nullvec(cols, p):
    """nonzero delta with sum delta_b cols[b] = 0; cols: list of equal-length vectors, more cols than rank"""
    n = len(cols[0]) if cols else 0; m = len(cols)
    A = [[cols[b][i] % p for b in range(m)] for i in range(n)]
    piv, row = [], 0
    for col in range(m):
        pr = next((r for r in range(row, n) if A[r][col]), None)
        if pr is None: continue
        A[row], A[pr] = A[pr], A[row]
        inv = pow(A[row][col], p-2, p); A[row] = [x*inv % p for x in A[row]]
        for r in range(n):
            if r != row and A[r][col]:
                f = A[r][col]; A[r] = [(x - f*y) % p for x, y in zip(A[r], A[row])]
        piv.append(col); row += 1
        if row == n: break
    free = next(c for c in range(m) if c not in piv)
    d = [0]*m; d[free] = 1
    for r, c in enumerate(piv): d[c] = (-A[r][free]) % p
    return d

def solve_coords(basis, tau, p):
    """unique y with sum y_l basis[l] = tau (basis linearly independent); returns y"""
    k = len(basis); a = len(tau)
    A = [[basis[l][i] % p for l in range(k)] + [tau[i] % p] for i in range(a)]
    piv, row = [], 0
    for col in range(k):
        pr = next((r for r in range(row, a) if A[r][col]), None)
        assert pr is not None, "basis dependent"
        A[row], A[pr] = A[pr], A[row]
        inv = pow(A[row][col], p-2, p); A[row] = [x*inv % p for x in A[row]]
        for r in range(a):
            if r != row and A[r][col]:
                f = A[r][col]; A[r] = [(x - f*y) % p for x, y in zip(A[r], A[row])]
        piv.append(col); row += 1
    for r in range(row, a): assert A[r][k] == 0, "tau not in span"
    return [A[r][k] for r in range(k)]

def lin(p, a, weights, lam):
    s = [0]*a
    for b, w in weights.items():
        if w:
            for i in range(a): s[i] = (s[i] + w*lam[b][i]) % p
    return s

# ---------------------------------------------------------------- adaptive chain
class ChainSolver:
    def __init__(self, F, steps, pairs, lam):
        self.F, self.p, self.steps, self.pairs, self.lam = F, F.p, steps, pairs, lam
        self.a = len(lam[0]); self.next = 0; self.M = len(lam)
    def take(self, n):
        if self.next + n > self.M: raise RuntimeError("out of columns")
        cols = list(range(self.next, self.next + n)); self.next += n
        return cols
    def relation(self, t, U):
        """weights w (dict) with sum w_b lam_b in U, classes (mod D_t) in K_t, and a designated b* with w_{b*} = 1"""
        p, a = self.p, self.a
        if t == 0:
            m = a - U.dim()
            cols = self.take(m + 1)
            red = [U.reduce(self.lam[b]) for b in cols]
            d = nullvec(red, p) if m > 0 else [1]
            bstar = next(cols[i] for i, x in enumerate(d) if x)
            s = pow(d[cols.index(bstar)], p-2, p)
            w = {b: x*s % p for b, x in zip(cols, d) if x}
            return w, bstar
        D, R, K = self.steps[t-1]
        alpha, beta = self.pairs[t-1]
        V = U.copy(); outer = [list(r) for r in U.raw]
        rounds = []
        while True:
            c, bstar = self.relation(t-1, V)
            ic = {b: self.F.cls(x, D) for b, x in c.items()}
            assert all(i in R for i in ic.values()), "admissibility violated"
            e = lin(p, a, c, self.lam)
            v = lin(p, a, {b: beta[ic[b]]*x % p for b, x in c.items()}, self.lam)
            if V.contains(v):
                W = {}
                for b, x in c.items():
                    y = x*(alpha[0] + beta[ic[b]]) % p
                    if y: W[b] = y
                rho = [(x + y) % p for x, y in zip(e, v)]
                assert W.get(bstar) == 1
                break
            rounds.append((c, ic, e, v)); V.add(v)
        tau = [(-x) % p for x in rho]
        for l in range(len(rounds), 0, -1):
            basis = outer + [rounds[q][3] for q in range(l)]
            y = solve_coords(basis, tau, p)
            zeta = y[-1]
            if zeta:
                c, ic, e, v = rounds[l-1]
                n = self.F.cls(zeta, D)
                for b, x in c.items():
                    wv = zeta*x*(alpha[n] + beta[ic[b]]) % p
                    if wv: W[b] = wv
                tau = [(tt - zeta*(alpha[n]*ee + vv)) % p for tt, ee, vv in zip(tau, e, v)]
        assert U.contains(tau), "back substitution left U"
        return W, bstar

def run_case(p, kappa, a, steps, pairs, F, lam):
    L = len(steps)
    S = ChainSolver(F, steps, pairs, lam)
    W, bstar = S.relation(L, Subspace(p, a))
    used = S.next
    # independent exact checks with pow()
    g = F.g
    assert any(W.values())
    for b, w in W.items():
        assert w % p and pow(w, (p-1)//kappa, p) == 1, "weight not a kappa-th power"
    s = lin(p, a, W, lam)
    assert not any(s), "not a relation"
    # kappa-th roots and the final identity
    gk = pow(g, kappa, p)
    u = {}
    for b, w in W.items():
        e = int(F.ind[w]); assert e % kappa == 0
        u[b] = pow(g, e//kappa, p)
        assert pow(u[b], kappa, p) == w
    s2 = lin(p, a, {b: pow(x, kappa, p) for b, x in u.items()}, lam)
    assert not any(s2)
    return used

def parse_chain(s):
    steps = []
    for part in s.split(';'):
        D, R, K = part.split(':')
        steps.append((int(D), [int(x) for x in R.split(',')], [int(x) for x in K.split(',')]))
    return steps

def admissible(steps, kappa):
    """check R_1 = Z_{D_1} and R_t = preimage of K_{t-1}, last K = {0} at D = kappa"""
    D0, K0 = 1, [0]
    for (D, R, K) in steps:
        if D % D0: return False
        pre = sorted(set(x for x in range(D) if (x % D0) in set(k % D0 for k in K0)))
        if sorted(R) != pre: return False
        D0, K0 = D, K
    return D0 == kappa and sorted(K0) == [0]

def columns(p, a, M, rng, mode):
    if mode == 'random':
        return [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
    if mode == 'adversarial':
        out = []
        for b in range(M):
            r = rng.random()
            if r < 0.15: out.append([0]*a)
            elif r < 0.35 and out: out.append(list(out[rng.randrange(len(out))]))
            elif r < 0.55:
                v = [0]*a; v[rng.randrange(a)] = rng.randrange(1, p); out.append(v)
            elif r < 0.75 and a > 1:
                v = [rng.randrange(p) for _ in range(a)]; v[-1] = 0; out.append(v)   # a hyperplane
            else: out.append([rng.randrange(p) for _ in range(a)])
        return out
    raise ValueError

def test(p, kappa, chain, avals, trials, rng, label=""):
    steps = parse_chain(chain)
    assert admissible(steps, kappa), "chain not admissible"
    F = Field(p)
    pairs = []
    for (D, R, K) in steps:
        pr = find_pair(F, D, R, K, rng=rng)
        if pr is None: return "%s p=%d kappa=%d chain=%s: NO PAIR found for step %s" % (label, p, kappa, chain, (D, R, K))
        assert check_pair(p, F.g, D, R, K, *pr), "pair check failed"
        pairs.append(pr)
    L = len(steps); n_ok = 0; maxratio = 0
    for a in avals:
        M = comb(a + L + 1, L + 1)
        for tr in range(trials):
            mode = 'random' if tr % 2 == 0 else 'adversarial'
            lam = columns(p, a, M, rng, mode)
            used = run_case(p, kappa, a, steps, pairs, F, lam)
            assert used <= M
            maxratio = max(maxratio, used / M)
            n_ok += 1
    return "%s p=%d kappa=%d chain=%s L=%d a=%s: %d runs OK (columns used <= C(a+L+1,L+1); max used/M = %.3f)" % (
        label, p, kappa, chain, L, list(avals), n_ok, maxratio)

if __name__ == "__main__":
    rng = random.Random(20261105)
    if sys.argv[1] == 'one':
        p, kappa, a, trials = map(int, sys.argv[2:6]); chain = sys.argv[6]
        print(test(p, kappa, chain, [a], trials, rng)); sys.exit()
    E2_4 = [17, 37, 53]
    cases = []
    # kappa = 4: chain 2 -> 4 at the E_2(4) primes the tower covers, plus controls
    for p in E2_4 + [41, 61]:
        cases.append((p, 4, "2:0,1:0;4:0,2:0", "tower k=4"))
    # kappa = 6: both chains at E_2(6) primes outside the tower-exceptional set
    for p in [37, 61, 73, 97, 181, 379, 859]:
        cases.append((p, 6, "3:0,1,2:0;6:0,3:0", "tower k=6 (3,6)"))
        cases.append((p, 6, "2:0,1:0;6:0,2,4:0", "tower k=6 (2,6)"))
    # kappa = 8: chain 2 -> 4 -> 8 at E_2(8) primes, including 11689 and 12809
    for p in [97, 113, 193, 257, 11689, 12809]:
        cases.append((p, 8, "2:0,1:0;4:0,2:0;8:0,4:0", "tower k=8"))
    # prime kappa: union chains at E_2(kappa) primes
    for p in [31, 41, 61, 71, 101, 131, 151, 181]:
        cases.append((p, 5, "5:0,1,2,3,4:0,1;5:0,1:0", "union k=5"))
    for p in [281, 379, 421, 1009, 3221]:
        cases.append((p, 7, "7:0,1,2,3,4,5,6:0,1,2,3;7:0,1,2,3:0", "union k=7"))
    # L = 1 sanity: the triangular solver itself at p outside E_2
    cases.append((41, 4, "4:0,1,2,3:0", "triangular k=4"))
    cases.append((11, 5, "5:0,1,2,3,4:0,1;5:0,1:0", "expected failure k=5 p=11"))
    cases.append((13, 4, "2:0,1:0;4:0,2:0", "expected failure k=4 p=13"))
    for (p, kappa, chain, label) in cases:
        av = [1, 2, 3] if (kappa == 8 or p > 5000) else [1, 2, 3, 4]
        tr = 4 if p > 5000 else 6
        print(test(p, kappa, chain, av, tr, rng, label), flush=True)
