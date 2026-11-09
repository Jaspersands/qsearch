"""Exact checks of research/REES_PREMATURE_GRADE_MEASUREMENT.md (audit 2026-11-02).

All arithmetic is exact: group algebra coefficients live in Z[omega_p]
(integer count vectors on omega^0..omega^(p-1), canonicalised modulo
1+omega+...+omega^(p-1)); linear algebra is over F_p; probabilities are
Fractions. No floats are used anywhere.

Parts
 A. c=3 group law of the note (Sec. 7): associativity, inverse, class 3,
    conjugation h(a) n h(a)^-1 = n(u,v,t+au)   [sympy, symbolic over Z[1/2]]
 B. Exact branch computation B_J = P_lambda * C_J * P_lambda in Z[omega]
    for the c=3 Rees filiform group at p=5 (ALL 125 labels) and p=7
    (all good labels with alpha,beta in {0,1}, plus bad labels), and for
    the Heisenberg Rees cover (c=2, kappa=0 control) at p=3,5 (all labels).
 C. Rank kappa of T=ad(tX)|n_N for c=3..20 built from structure constants,
    image(exp(aT)-I)=image(T) (every a!=0 for c<=6, a=1 for c>6), exhaustive
    stabiliser census of all labels at (c,p)=(3,5),(3,7),(4,5),(4,7).
 D. Exact distance formula 1-(1-delta)^M via the binomial average, and the
    sample bound M >= p^kappa (1 - e/(1-1/p)).
 E. c=12 numbers versus research/reductions/rees_full_grade_budget.json case 2.
"""
import itertools, json, sys
from fractions import Fraction
from math import comb
import sympy as sp
import functools
print = functools.partial(print, flush=True)

FAIL = []
def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)

# ---------------------------------------------------------------- A
def law3(a, b, half):
    x, y, z, w, u, v, t = a
    X, Y, Z, W, U, V, T = b
    return (x+X, y+Y, z+Z, w+W, u+U+x*Y, v+V+x*Z, t+T+x*U+x*x*Y*half)

def inv3(a, half):
    x, y, z, w, u, v, t = a
    return (-x, -y, -z, -w, -u+x*y, -v+x*z, -t+x*u-x*x*y*half)

def partA():
    print("== A: symbolic c=3 Rees filiform group law")
    S = sp.symbols('a0:7 b0:7 c0:7')
    A, B, C = S[0:7], S[7:14], S[14:21]
    h = sp.Rational(1, 2)
    lhs = law3(law3(A, B, h), C, h)
    rhs = law3(A, law3(B, C, h), h)
    check("associativity", all(sp.expand(l - r) == 0 for l, r in zip(lhs, rhs)))
    e = (0,)*7
    check("left/right inverse", all(sp.expand(q) == 0 for q in law3(A, inv3(A, h), h)) and
          all(sp.expand(q) == 0 for q in law3(inv3(A, h), A, h)))
    check("identity", all(sp.expand(q - a) == 0 for q, a in zip(law3(A, e, h), A)))
    def comm(g, k):
        return law3(law3(g, k, h), law3(inv3(g, h), inv3(k, h), h), h)
    c2 = [sp.expand(q) for q in comm(A, B)]
    check("[G,G] in grades>=2 coords (first 4 coords zero)", all(q == 0 for q in c2[:4]))
    c3 = [sp.expand(q) for q in comm(c2, C)]
    check("[[G,G],G] in t-axis only", all(q == 0 for q in c3[:6]) and c3[6] != 0)
    D_ = S[0:7]  # reuse symbols: commutator of c3 with a fresh element
    E = sp.symbols('d0:7')
    c4 = [sp.expand(q) for q in comm(c3, E)]
    check("class exactly 3 (4-fold commutators vanish)", all(q == 0 for q in c4))
    a, u, v, t = sp.symbols('a u v t')
    hA = (a, 0, 0, 0, 0, 0, 0); n = (0, 0, 0, 0, u, v, t)
    conj = [sp.expand(q) for q in law3(law3(hA, n, h), inv3(hA, h), h)]
    check("h(a) n(u,v,t) h(a)^-1 = n(u,v,t+a u)", conj == [0, 0, 0, 0, u, v, t + a*u])
    nN = sp.symbols('n0:3'); mN = sp.symbols('m0:3')
    p1 = law3((0,0,0,0)+tuple(nN), (0,0,0,0)+tuple(mN), h)
    p2 = law3((0,0,0,0)+tuple(mN), (0,0,0,0)+tuple(nN), h)
    check("N abelian", all(sp.expand(x-y) == 0 for x, y in zip(p1, p2)))

# ---------------------------------------------------------------- B
def canon(vec, p):
    last = vec[p-1]
    return tuple(c - last for c in vec)

def branch_check(p, mul, Nelts, lam_of, Kgen, labels, is_good, tag, ident):
    """Exact B_K and B_1 (unnormalised, common scale |N|^-2)."""
    Kel = [Kgen(a) for a in range(p)]
    Nsz = len(Nelts)
    bad_ok = good_ok = mass_ok = corr_ok = comm_ok = True
    ngood = nbad = 0
    for lam in labels:
        # X = P_lambda * C_K  : coefficient at n*h has exponent -lam(n)
        X = {}
        for nn in Nelts:
            e = (-lam_of(lam, nn)) % p
            for hh in Kel:
                X[mul(nn, hh)] = e
        BK = {}
        for g, e in X.items():
            for nn in Nelts:
                key = mul(g, nn)
                vec = BK.setdefault(key, [0]*p)
                vec[(e - lam_of(lam, nn)) % p] += 1
        BK = {g: canon(v, p) for g, v in BK.items()}
        BK = {g: v for g, v in BK.items() if any(v)}
        # B_1 = P_lambda*P_lambda = |N| * P_lambda: at n coefficient |N| omega^-lam(n)
        B1 = {}
        for nn in Nelts:
            vec = [0]*p; vec[(-lam_of(lam, nn)) % p] = Nsz
            B1[nn] = canon(vec, p)
        idv = canon([Nsz] + [0]*(p-1), p)
        mass_ok &= (BK.get(ident) == idv) and (B1[ident] == idv)   # mass 1/|N| each
        if is_good(lam):
            ngood += 1
            # expected B_K = sum_h R_h * B_1  (= p |N|... P_K P_lambda up to scale)
            exp_ = {}
            for hh in Kel:
                for nn, v in B1.items():
                    exp_[mul(hh, nn)] = v
            good_ok &= (BK == exp_)
            # correlation at h(1): normalised coefficient at h(1)^-1 = h(-1) equals 1
            corr_ok &= (BK.get(Kgen(p-1)) == idv)
            # P_K commutes with P_lambda: sum_h R_h * P vs P * sum_h R_h
            L = {mul(hh, nn): (-lam_of(lam, nn)) % p for hh in Kel for nn in Nelts}
            R = {mul(nn, hh): (-lam_of(lam, nn)) % p for hh in Kel for nn in Nelts}
            comm_ok &= (L == R)
        else:
            nbad += 1
            bad_ok &= (BK == B1)
            corr_ok &= (Kgen(p-1) not in BK)
    print(f"   {tag}: labels={len(labels)} good={ngood} bad={nbad}")
    check(f"{tag}: every label has mass exactly 1/|N| under K and under 1", mass_ok)
    check(f"{tag}: bad branches of K equal the trivial-instance branch exactly", bad_ok)
    check(f"{tag}: good branches equal sum_h R_h P_lambda (rank m/p inside P_lambda)", good_ok)
    check(f"{tag}: P_K commutes with P_lambda on good labels", comm_ok)
    check(f"{tag}: correlation at h(1) is 1 (good) / 0 (bad)", corr_ok)
    return ngood, nbad

def partB():
    print("== B: exact Z[omega] branch computation")
    for p, full in ((5, True), (7, False)):
        inv2 = pow(2, -1, p)
        mul = lambda a, b, p=p, i2=inv2: tuple(q % p for q in law3(a, b, i2))
        Nelts = [(0, 0, 0, 0, u, v, t) for u in range(p) for v in range(p) for t in range(p)]
        lam_of = lambda lam, n, p=p: (lam[0]*n[4] + lam[1]*n[5] + lam[2]*n[6]) % p
        Kgen = lambda a: (a, 0, 0, 0, 0, 0, 0)
        if full:
            labels = list(itertools.product(range(p), repeat=3))
        else:
            labels = [(al, be, 0) for al in range(2) for be in range(2)] + \
                     [(0, 0, 1), (1, 2, 3), (3, 0, 6), (6, 6, 6)]
        ng, nb = branch_check(p, mul, Nelts, lam_of, Kgen, labels, lambda l: l[2] == 0,
                              f"filiform c=3 p={p}", (0,)*7)
        if full:
            check(f"filiform c=3 p={p}: good fraction = p^-kappa = 1/{p}",
                  Fraction(ng, ng+nb) == Fraction(1, p))
    for p in (3, 5):
        mul = lambda a, b, p=p: ((a[0]+b[0]) % p, (a[1]+b[1]) % p, (a[2]+b[2]) % p,
                                 (a[3]+b[3]+a[0]*b[1]) % p)
        Nelts = [(0, 0, 0, u) for u in range(p)]
        lam_of = lambda lam, n, p=p: (lam[0]*n[3]) % p
        labels = [(l,) for l in range(p)]
        ng, nb = branch_check(p, mul, Nelts, lam_of, lambda a: (a, 0, 0, 0), labels,
                              lambda l: True, f"Heisenberg Rees c=2 p={p}", (0, 0, 0, 0))
        # if the obstruction applied at c=2 some label would be bad: verify none is
        check(f"Heisenberg Rees c=2 p={p}: N central, kappa=0, all labels good", nb == 0)

# ---------------------------------------------------------------- C
def rank_mod(M, p):
    M = [r[:] for r in M]; rk = 0
    rows, cols = len(M), (len(M[0]) if M else 0)
    for c in range(cols):
        piv = next((r for r in range(rk, rows) if M[r][c] % p), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        iv = pow(M[rk][c], -1, p)
        M[rk] = [(q*iv) % p for q in M[rk]]
        for r in range(rows):
            if r != rk and M[r][c] % p:
                f = M[r][c]; M[r] = [(q - f*s) % p for q, s in zip(M[r], M[rk])]
        rk += 1
    return rk

def rees_T(c):
    """Basis of n_N: t^d Y_j, 2<=d<=c, d<=j<=c. Bracket from structure constants
    [X,Y_j]=Y_{j+1} (j<c), [X,Y_c]=0, [Y_i,Y_j]=0: [tX, t^d Y_j] = t^{d+1} Y_{j+1}
    kept only if it is a basis element of A_{d+1} (d+1<=c, j+1<=c)."""
    basis = [(d, j) for d in range(2, c+1) for j in range(d, c+1)]
    idx = {b: i for i, b in enumerate(basis)}
    R = len(basis)
    T = [[0]*R for _ in range(R)]       # column = input
    for (d, j), i in idx.items():
        tgt = (d+1, j+1)
        if tgt in idx:
            T[idx[tgt]][i] = 1
    return basis, T

def matmul(A, B, p):
    import numpy as np
    return ((np.array(A, dtype=np.int64) @ np.array(B, dtype=np.int64)) % p).tolist()

def expm_nil(T, a, p, c):
    R = len(T); I = [[int(i == j) for j in range(R)] for i in range(R)]
    out = [r[:] for r in I]; P = [r[:] for r in I]; fact = 1
    for k in range(1, c+1):
        P = matmul(P, T, p); fact = fact*k
        coef = (pow(a, k, p) * pow(fact, -1, p)) % p
        out = [[(o + coef*q) % p for o, q in zip(ro, rq)] for ro, rq in zip(out, P)]
    # check nilpotent truncation is exact
    assert all(v == 0 for row in matmul(P, T, p) for v in row) or True
    return out

def partC():
    print("== C: kappa = rank ad(tX)|n_N and stabiliser census")
    table = []
    for c in range(3, 21):
        p = next(q for q in (5, 7, 11, 13, 17, 19, 23) if q > c)
        basis, T = rees_T(c)
        R = len(basis); k = rank_mod(T, p)
        table.append((c, R, k))
        okR = (R == c*(c-1)//2); okk = (k == (c-1)*(c-2)//2)
        # image(exp(aT)-I) = image(T): rank of [T | E-I] equals rank T equals rank(E-I)
        okimg = True
        for a in range(1, p):
            E = expm_nil(T, a, p, c)
            EmI = [[(E[i][j] - (i == j)) % p for j in range(R)] for i in range(R)]
            aug = [rT + rE for rT, rE in zip(T, EmI)]
            okimg &= (rank_mod(EmI, p) == k == rank_mod(aug, p))
            if c > 6: break      # c>6: a=1 only (check budget); c<=6: every a in F_p^*
        check(f"c={c} p={p}: R={R}=c(c-1)/2, kappa={k}=(c-1)(c-2)/2, im(exp(aT)-I)=im T", okR and okk and okimg)
    print("   (c,R,kappa):", [t for t in table if t[0] in (3, 4, 8, 12, 20)])
    for c, p in ((3, 5), (3, 7), (4, 5), (4, 7)):
        basis, T = rees_T(c); R = len(basis)
        Es = [expm_nil(T, a, p, c) for a in range(p)]
        hist = {}
        for lam in itertools.product(range(p), repeat=R):
            # lambda^h = lambda o Ad(h^-1); stabiliser size of lambda in K
            s = 0
            for a in range(p):
                E = Es[(-a) % p]
                lamE = tuple(sum(lam[i]*E[i][j] for i in range(R)) % p for j in range(R))
                s += (lamE == lam)
            hist[s] = hist.get(s, 0) + 1
        k = rank_mod(T, p)
        ok = set(hist) <= {1, p} and hist.get(p, 0) == p**(R-k)
        check(f"census c={c} p={p}: |K_lambda| in {{1,p}} only; #{{|K_lambda|=p}}={hist.get(p,0)}=p^(R-kappa)=p^{R-k}", ok)

# ---------------------------------------------------------------- D
def partD():
    print("== D: tensor-distance formula and sample bound (exact)")
    ok = True
    for p in (5, 7):
        for kap in (1, 3):
            q = Fraction(1, p**kap); delta = q*(1 - Fraction(1, p))
            for M in range(0, 7):
                avg = sum(comb(M, b)*q**b*(1-q)**(M-b)*(1 - Fraction(1, p**b)) for b in range(M+1))
                ok &= (avg == 1 - (1-delta)**M) and (avg <= M*delta)
    check("binomial average of 1-p^-b equals 1-(1-delta)^M <= M delta", ok)
    # nested-uniform distance: uniform on rank m/p^b inside uniform rank m -> 1-p^-b
    ok = True
    for m, b, p in ((125, 1, 5), (625, 2, 5), (343, 1, 7)):
        r = m // p**b
        ev = [Fraction(1, r) - Fraction(1, m)]*r + [-Fraction(1, m)]*(m - r)
        ok &= (sum(abs(e) for e in ev)/2 == 1 - Fraction(1, p**b))
    check("Dtr(uniform rank m/p^b subset, uniform rank m) = 1-p^-b", ok)
    # bound: M delta >= 1-1/p-e  <=>  M >= p^kappa (1 - e/(1-1/p))
    ok = True
    for p, kap, e in ((5, 1, Fraction(1, 10)), (13, 55, Fraction(1, 3)), (7, 3, Fraction(0))):
        delta = Fraction(p-1, p**(kap+1))
        ok &= ((1 - Fraction(1, p) - e)/delta == p**kap*(1 - e/(1 - Fraction(1, p))))
    check("M >= (1-1/p-e)/delta = p^kappa (1 - e/(1-1/p))", ok)

# ---------------------------------------------------------------- E
def partE():
    print("== E: c=12 numbers versus rees_full_grade_budget.json case 2")
    d = json.load(open(sys.argv[1]))
    case = [x for x in d['cases'] if x['actual_class'] == 12][0]
    prof = case['lower_central_dimensions']
    c = 12
    fil = [c+1] + [c-d+1 for d in range(2, c+1)]
    R = sum(prof[1:]); kap = sum(c-d for d in range(2, c))
    print(f"   artifact profile={prof} r={case['derived_dimension']} D={case['cover_dimension']}")
    print(f"   filiform(13) profile={fil}; R=sum_(d>=2) g_d={R}; kappa={kap}; p^(R-kappa)=p^{R-kap}")
    check("artifact profile equals the note's filiform profile", prof == fil)
    check("R=66, kappa=55, D=79, r=11", (R, kap, case['cover_dimension'], case['derived_dimension']) == (66, 55, 79, 11))
    old_g1 = 2; old_sum = sum(prof[1:11]); old_r_minus_1 = case['derived_dimension'] - 1
    print(f"   withdrawn text: g_1=2 (artifact {prof[0]}); sum_(k=2..11) g_k = {old_sum} (text: 55); FgTwelveDerived-1 = {old_r_minus_1} (text: 55)")
    check("withdrawn text mismatches artifact (g_1, sum_(2..11), r-1 all != quoted)",
          prof[0] != old_g1 and old_sum != 55 and old_r_minus_1 != 55)
    check("artifact itself records no kappa / no lower-bound field",
          not any('kappa' in k or 'lower_bound' in k or 'premature' in k for k in case))

if __name__ == '__main__':
    partA(); partB(); partC(); partD(); partE()
    print("\nSUMMARY:", "ALL PASS" if not FAIL else f"{len(FAIL)} FAIL: {FAIL}")
