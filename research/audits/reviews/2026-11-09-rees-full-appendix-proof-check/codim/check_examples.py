# Exact checks of the explicit examples in appendix-codimension.tex (codim checker, 9 Nov 2026).
# Run: /opt/anaconda3/bin/python -I check_examples.py   (from this folder; imports only liealg.py)
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from liealg import *

out = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); out.append(s)

def g6(p):
    # e1..e6 -> 0..5 ; [e1,ei]=e_{i+1} (2<=i<=5), [e2,e3]=e5, [e2,e4]=e6, [e2,e5]=-e6, [e3,e4]=e6
    br = {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (0, 4): {5: 1},
          (1, 2): {4: 1}, (1, 3): {5: 1}, (1, 4): {5: -1}, (2, 3): {5: 1}}
    return Lie.from_dict(6, p, br)

def five(p):
    # [e1,ei]=e_{i+1} for 2<=i<=4, [e2,e3]=e5
    br = {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (1, 2): {4: 1}}
    return Lie.from_dict(5, p, br)

def filiform(m, p):
    # basis x=0, e_i = i (1..m-1); [x,e_i]=e_{i+1}, i<=m-2
    br = {(0, i): {i + 1: 1} for i in range(1, m - 1)}
    return Lie.from_dict(m, p, br)

def heis(p):
    return Lie.from_dict(3, p, {(0, 1): {2: 1}})

def ideal_all_runs_unique(L, trials=4, seed=1):
    """Check that at every step dim(V_j/I_j) <= 1 (so the result is choice-independent),
    and return the ideal; also run random choices."""
    xs, ext = ideal_construction(L, None)
    I0 = span(xs, L.p)
    uniq = all(e <= 1 for e in ext)
    rng = random.Random(seed)
    same = True
    for t in range(trials):
        xs2, _ = ideal_construction(L, rng)
        if not subspace_eq(span(xs2, L.p), I0, L.p):
            same = False
    return I0, ext, uniq, same

# ---- g6 ----
for p in [3, 5, 7, 11, 13]:
    L = g6(p)
    jac = L.check_jacobi()
    g = lcs(L)
    dims = [len(x) for x in g]
    cl = nil_class(L)
    I, ext, uniq, same = ideal_all_runs_unique(L)
    Iexp = [L.e(3), L.e(4), L.e(5)]
    C = centralizer(L, I)
    # formulas [y,e4] = y1 e5 + (y2+y3) e6 ; [y,e5] = (y1 - y2) e6
    ok_f = True
    rng = random.Random(p)
    for _ in range(200):
        y = tuple(rng.randrange(p) for _ in range(6))
        a = L.br(y, L.e(3)); b = L.br(y, L.e(4))
        if a != (0, 0, 0, 0, y[0] % p, (y[1] + y[2]) % p): ok_f = False
        if b != (0, 0, 0, 0, 0, (y[0] - y[1]) % p): ok_f = False
    log(f"g6 p={p}: jacobi={jac} lcs dims={dims} class={cl} filiform={dims[1]==4 and cl==5} "
        f"ext(V_j/I_j)={ext} unique-choice={uniq} random-runs-same={same} I==span(e4,e5,e6)={subspace_eq(I,Iexp,p)} "
        f"C(I)==I={subspace_eq(C,I,p)} formulas={ok_f} b={len(I)} dim<=b(b+1)/2:{6<=len(I)*(len(I)+1)//2} class<=2b-1:{cl<=2*len(I)-1}")

# Jacobi over Z: structure constants are 0,+-1; check Jacobi with a large prime (no wrap-around possible
# because every Jacobi sum is an integer of absolute value < 10 < 1009)
log("g6 Jacobi mod 1009 (integer identity):", g6(1009).check_jacobi())

# ---- five-dimensional example ----
for p in [5, 7, 11]:
    L = five(p)
    I, ext, uniq, same = ideal_all_runs_unique(L)
    log(f"5-dim p={p}: jacobi={L.check_jacobi()} class={nil_class(L)} ext={ext} unique={uniq} same={same} "
        f"I==span(e3,e4,e5)={subspace_eq(I,[L.e(2),L.e(3),L.e(4)],p)} b={len(I)} C(I)==I={subspace_eq(centralizer(L,I),I,p)}")

# ---- minimality: in dim <= 4 class <= b (all runs) : check on all filiform/standard small algebras is
# covered by the proof; here we only spot-check the dim-4 filiform and dim-4 algebras below.

# ---- filiform family, Prop. app-codim-filiform ----
def nextprime_ge(m):
    q = m
    while True:
        if all(q % d for d in range(2, int(q ** 0.5) + 1)) and q >= 2:
            return q
        q += 1

for m in range(3, 11):
    for p in sorted(set([nextprime_ge(m)] + ([101] if m <= 7 else []))):
        L = filiform(m, p)
        ok = L.check_jacobi()
        g = lcs(L)
        cl = nil_class(L)
        gam_ok = all(subspace_eq(g[d - 1], [L.e(i) for i in range(d, m)], p) for d in range(2, m))
        h = [L.e(i) for i in range(1, m - 1)]
        codim = m - len(h)
        ad = []
        for d in range(2, m):
            gd = g[d - 1]
            ad.append(len(gd) - len(intersect(h, gd, m, p)))
        I, ext, uniq, same = ideal_all_runs_unique(L)
        Iexp = [L.e(i) for i in range(1, m)]
        N = normalizer(L, h)
        # loose-k example: h' = span(x, e2..e_{m-1}), B = span(e2..e_{m-2})
        hp = [L.e(0)] + [L.e(i) for i in range(2, m)]
        Bsp = [L.e(i) for i in range(2, m - 1)]
        loose_ok = (is_subalgebra(L, hp) and len(hp) == m - 1 and
                    len(Bsp) == (m - 1) - 2 and contains(intersect(hp, Iexp, m, p), Bsp, p) and
                    len(intersect(hp, Iexp, m, p)) == m - 2 and
                    not contains(normalizer(L, Bsp), [L.e(0)], p)) if m >= 4 else None
        # Span(x, e_{m-1}) abelian, self-centralizing, not an ideal
        A = [L.e(0), L.e(m - 1)]
        sc_ok = (is_abelian(L, A) and subspace_eq(centralizer(L, A), A, p) and not is_ideal(L, A))
        log(f"filiform m={m} p={p}: jacobi={ok} class={cl} gamma_d ok={gam_ok} codim h={codim} a_d={ad} "
            f"ideal ext={ext} unique={uniq} randomsame={same} I==span(e1..e_{m-1})={subspace_eq(I,Iexp,p)} "
            f"N(h)==I={subspace_eq(N,Iexp,p)} loose-k example ok={loose_ok} span(x,e_last) abelian selfcentral nonideal={sc_ok}")

# ---- Heisenberg: no homomorphic section of Heis -> Heis/Z (group level, brute force) ----
for p in [3, 5]:
    L = heis(p)
    bch = make_bch(L, 2)
    G = list(itertools.product(range(p), repeat=3))
    # a homomorphic section sigma: F_p^2 -> Heis with pi(sigma(q)) = q is determined by
    # a = sigma(1,0), b = sigma(0,1); hom from the abelian group F_p^2 needs a*b == b*a
    found = 0
    for z1 in range(p):
        for z2 in range(p):
            a = (1, 0, z1); b = (0, 1, z2)
            if bch(a, b) == bch(b, a):
                found += 1
    # also: every subgroup of order p^2 contains the centre (enumerate subgroups generated by 2 elements)
    def gen_subgroup(gens):
        S = {(0, 0, 0)}
        frontier = list(S)
        while frontier:
            new = []
            for s in frontier:
                for g_ in gens:
                    t = bch(s, g_)
                    if t not in S:
                        S.add(t); new.append(t)
            frontier = new
        return S
    bad = 0; cnt = 0
    seen = set()
    for a in G:
        for b in G:
            if a >= b: continue
            S = frozenset(gen_subgroup([a, b]))
            if len(S) == p * p and S not in seen:
                seen.add(S); cnt += 1
                if not all(((0, 0, z) in S) for z in range(p)):
                    bad += 1
    log(f"Heisenberg p={p}: commuting lifts (homomorphic sections) found={found}; subgroups of order p^2={cnt}, "
        f"not containing centre={bad}")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_examples.out"), "w") as fh:
    fh.write("\n".join(out) + "\n")
