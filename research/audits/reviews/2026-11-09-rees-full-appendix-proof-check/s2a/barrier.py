# s2a: finite checks of Lemma lem:app-s2-kwise, Prop. prop:app-s2-barrier (iii) and the
# bracket of Remark rem:app-s2-joint-moments on the exact law of n_0, the four-cycle
# formulas of Remark rem:app-s2-four-cycle, and the example p = 196681 of
# Remark rem:app-s2-chebotarev-scope.  Falsification only.
# Run: nice -n 19 timeout 900 /opt/anaconda3/bin/python -I barrier.py
import itertools, math, cmath, random
from fractions import Fraction as Fr
import numpy as np
import sympy
random.seed(11)

def log(*a): print(*a, flush=True)

# ---------- Lemma kwise ----------
viol = []
for k in range(2, 9):
    for th in [Fr(0), Fr(1, 10), Fr(1, 3), Fr(1, 2)]:
        P = {}
        for x in itertools.product((0, 1), repeat=k):
            s = sum(x)
            P[x] = th**s*(1-th)**(k-s) - (-1)**(k-s)*th**k
        if any(v < 0 for v in P.values()) or sum(P.values()) != 1 or P[(1,)*k] != 0:
            viol.append(('law', k, th))
        for drop in range(k):  # marginal on the complement of {drop}
            for y in itertools.product((0, 1), repeat=k-1):
                tot = sum(P[y[:drop] + (b,) + y[drop:]] for b in (0, 1))
                s = sum(y)
                if tot != th**s*(1-th)**(k-1-s): viol.append(('marg', k, th, drop))
    th = Fr(3, 5)
    x = (1,)*(k-2) + (0, 0)
    if not (th**(k-2)*(1-th)**2 - th**k) < 0: viol.append(('converse', k))
log("Lemma kwise: violations", viol)

# ---------- exact law of n_0 and the brackets ----------
def setup(p, k):
    g = int(sympy.primitive_root(p))
    ind = np.full(p, -1, dtype=np.int64); x = 1
    for n in range(p-1):
        ind[x] = n % k; x = x*g % p
    return g, ind

def Ecoef(k, m):  # E_kappa(m,p) = c_m sqrt p + d_m
    c = Fr(m)*(1 - Fr(1, k)) - 1 + Fr(1, k**m)
    d = Fr(m, k) - m*Fr(1, k**m)
    return c, d

def eta(k, m, p):
    c, d = Ecoef(k, m)
    return k**m*(float(c)*math.sqrt(p) + float(d))/(p - m)

def rho(k, m, p):
    return (p - m)/(p*k**m)

def joint_counts(p, k):
    """array n[j][y] for all y in {0} x F_p^{k-1} (flattened)."""
    g, ind = setup(p, k)
    h = (p-1)//k
    ys = np.arange(p)
    out = []
    for j in range(k):
        Xs = [x for x in range(1, p) if ind[x] == (-j) % k]
        tot = np.zeros((p,)*(k-1), dtype=np.int64)
        for x in Xs:
            vecs = [(ind[(x + ys) % p] == (-(i+j)) % k).astype(np.int64) for i in range(1, k)]
            t = vecs[0]
            for v in vecs[1:]:
                t = np.multiply.outer(t, v)
            tot += t
        out.append(tot.reshape(-1))
    return out, h

viol = []; report = []
def combsum(arr, m):
    a = arr.astype(object) if m > 3 else arr.astype(np.int64)
    if m == 1: return int(a.sum())
    if m == 2: return int((a*(a-1)//2).sum())
    if m == 3: return int((a*(a-1)*(a-2)//6).sum())
    return sum(math.comb(int(v), m) for v in arr)
for (k, p) in [(3, 7), (3, 13), (4, 5), (4, 13), (4, 17), (4, 29), (4, 37), (4, 41), (4, 53), (4, 61), (4, 97), (4, 101), (4, 109), (4, 113), (5, 11), (5, 31)]:
    assert p <= k**k/2 and p % k == 1
    n, h = joint_counts(p, k)
    N = n[0]
    Ny = len(N)
    # every n_j has the law of n_0
    for j in range(1, k):
        if sorted(n[j].tolist()) != sorted(N.tolist()): viol.append(('law n_j', k, p, j))
    theta = Fr(int((N > 0).sum()), Ny)
    En = Fr(int(N.sum()), Ny)
    if not (theta <= En < Fr(p, k**k) <= Fr(1, 2)): viol.append(('theta', k, p))
    # eta_{k-1} > 1
    if not eta(k, k-1, p) > 1: viol.append(('eta_{k-1}', k, p))
    ms = [m for m in range(1, k) if eta(k, m, p) < 1]
    if any(m > k-2 for m in ms): viol.append(('m<=k-2', k, p))
    # e_a under N
    e = {a: Fr(combsum(N, a) if a else Ny, Ny) for a in range(0, k+1)}
    # true joint law bracket (Remark joint-moments) for every S and m with eta_m < 1, and L-bracket (Prop barrier (iii))
    for r in range(1, k+1):
        for S in itertools.combinations(range(k), r):
            MS = sum(n[j] for j in S)
            for m in ms:
                lo = math.comb(r*h, m)*rho(k, m, p)**(k-1)*(1 - eta(k, m, p))**(k-1)
                hi = math.comb(r*h, m)*rho(k, m, p)**(k-1)*(1 + eta(k, m, p))**(k-1)
                true = combsum(MS, m)/Ny
                if not (lo - 1e-12 <= true <= hi + 1e-12): viol.append(('true bracket', k, p, S, m))
                # under L: sum over compositions of prod e_{m_j}
                EL = Fr(0)
                for comp in itertools.product(range(m+1), repeat=r):
                    if sum(comp) != m: continue
                    t = Fr(1)
                    for a in comp: t *= e[a]
                    EL += t
                if not (lo - 1e-12 <= float(EL) <= hi + 1e-12): viol.append(('L bracket', k, p, S, m, float(EL), lo, hi))
    # Is the all-positive event under the TRUE law positive?  (for information)
    allpos = int(np.all(np.array([nj > 0 for nj in n]), axis=0).sum())
    report.append((k, p, 'theta=%.4f' % float(theta), 'ms=%s' % ms, 'true #y all nonempty=%d' % allpos))
log("Prop barrier / bracket checks: violations", viol)
for r in report: log("   ", r)

# explicit law L at (3,7): check (i) and (ii) directly
k, p = 3, 7
n, h = joint_counts(p, k)
N = n[0]; Ny = len(N)
vals = sorted(set(N.tolist()))
pN = {v: Fr(int((N == v).sum()), Ny) for v in vals}
theta = 1 - pN.get(0, Fr(0))
cond = {v: pN[v]/theta for v in vals if v > 0}
PB = {}
for x in itertools.product((0, 1), repeat=k):
    s = sum(x); PB[x] = theta**s*(1-theta)**(k-s) - (-1)**(k-s)*theta**k
L = {}
for x, pb in PB.items():
    for ms_ in itertools.product(*[list(cond.items()) if b else [(0, Fr(1))] for b in x]):
        key = tuple(v for v, _ in ms_); w = pb
        for _, q in ms_: w *= q
        L[key] = L.get(key, 0) + w
okii = sum(w for key, w in L.items() if all(v > 0 for v in key)) == 0
oki = True
for keep in itertools.combinations(range(k), k-1):
    marg = {}
    for key, w in L.items():
        kk = tuple(key[i] for i in keep); marg[kk] = marg.get(kk, 0) + w
    for kk, w in marg.items():
        if w != math.prod(pN.get(v, 0) for v in kk): oki = False
log("explicit L at (3,7): (i) marginals:", oki, " (ii) all-positive mass 0:", okii, " total:", sum(L.values()))

# ---------- four-cycle formulas ----------
def chi_table(p, k):
    g, ind = setup(p, k)
    w = cmath.exp(2j*math.pi/k)
    return [0 if x == 0 else w**int(ind[x]) for x in range(p)], ind
viol = []; ncheck = 0
for (k, p) in [(3, 7), (3, 13), (4, 13), (5, 11), (6, 13)]:
    chi, ind = chi_table(p, k)
    def cpow(x, s):
        s %= k
        if s == 0: return 1
        return 0 if x == 0 else chi[x]**s
    def Jac(a, b):
        return sum(cpow(w, a)*cpow((1-w) % p, b) for w in range(p))
    for e1, e2, e3, e4 in itertools.product(range(1, k), repeat=4):
        if (e1+e2+e3+e4) % k: continue
        # brute force over alpha_j, alpha_j', beta_i, beta_i' (other coords give p^{2k-4})
        tot = 0
        for aj in range(p):
            for aj2 in range(p):
                r1 = sum(cpow((aj+b) % p, e1)*cpow((aj2+b) % p, e2) for b in range(p))
                r2 = sum(cpow((aj+b) % p, e3)*cpow((aj2+b) % p, e4) for b in range(p))
                tot += r1*r2
        Se = tot*p**(2*k-4)
        if (e1+e2) % k:
            pred = p**(2*k-3)*(p-1)*cpow(p-1, e2+e4)*Jac(e1, e2)*Jac(e3, e4)
        else:
            pred = p**(2*k-2)*(p-1)
        ncheck += 1
        if abs(Se - pred) > 1e-6*abs(pred): viol.append((k, p, (e1, e2, e3, e4)))
        if abs(abs(Se) - p**(2*k-2)*(p-1)) > 1e-6*p**(2*k-2)*(p-1): viol.append(('mod', k, p, (e1, e2, e3, e4)))
log("four-cycle formulas: checked", ncheck, "violations", viol[:5])
# vanishing claims on full brute force at (3,7)
k, p = 3, 7
chi, ind = chi_table(p, k)
def cpow(x, s):
    s %= k
    if s == 0: return 1
    return 0 if x == 0 else chi[x]**s
pts = list(itertools.product(range(p), repeat=2*k))
bad = 0; tested = 0
for _ in range(40):
    e = [[random.randrange(k) for _ in range(k)] for _ in range(k)]
    rows1 = any(sum(1 for x in row if x) == 1 for row in e)
    cols1 = any(sum(1 for i in range(k) if e[i][j]) == 1 for j in range(k))
    sumnz = sum(map(sum, e)) % k != 0
    if not (rows1 or cols1 or sumnz): continue
    tested += 1
    S = 0
    for pt in pts:
        al, be = pt[:k], pt[k:]
        t = 1
        for i in range(k):
            for j in range(k):
                if e[i][j]:
                    t *= cpow((al[j]+be[i]) % p, e[i][j])
                    if t == 0: break
            if t == 0: break
        S += t
    if abs(S) > 1e-6: bad += 1
log("four-cycle vanishing claims at (3,7): tested", tested, "nonzero:", bad)

# ---------- Chebotarev scope example ----------
p = 196681
ok = sympy.isprime(p) and p % 4 == 1 and all(pow(u % p, (p-1)//4, p) == 1 for u in list(range(1, 17)) + [-u for u in range(1, 17)])
log("p = 196681 prime, every 1 <= |u| <= 16 a fourth power:", ok, " p mod 8 =", p % 8)
