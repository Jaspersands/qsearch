"""Referee re-derivation (independent code) of the finite claims in 2026-11-08-rees-sde-p3.md.

A. Lemma 2: every t-dim subspace of F_3^N has <= 2^t zero-one vectors; > (3/4)2^t forces a
   partition subspace.  Exhaustive over ALL subspaces of F_3^N, N <= 6.
B. Theorem 2: the defect set E_2 in F_3^6; |E_2|; does E_2 contain a 2-dim LINEAR subspace
   (independent pair a, b with all xa+yb in E_2)?  Plus a direct brute force on the generic
   8-class piece (one column per nonzero pattern).
C. Theorem 3: 2-dim K in F_3^5 with {0,1}^5 + K = F_3^5 ; also (t,k) = (4,2),(3,1),(2,1).
D. Theorem 5: all pattern sets T subset F_3^2\\0 admitting a 2-dim gain-or-zero-sum realization,
   split into 'trivial' (some nonzero a*delta+b*delta' is {0,1}-valued on T, i.e. a zero-sum set
   is already a dependency) and non-trivial.
E. Theorem 4: the eight class-union identities modulo the two relations, by an independent
   method, plus the empty-class degeneracies.
Pure Python, exact arithmetic mod 3."""
import itertools

def add(u, v, a=1, b=1): return tuple((a * x + b * y) % 3 for x, y in zip(u, v))
def smul(u, a): return tuple((a * x) % 3 for x in u)

# ---------------- generic subspace enumeration via RREF ----------------
def rref_subspaces(N, t):
    """yield each t-dim subspace of F_3^N once, as a list of basis rows in RREF."""
    for piv in itertools.combinations(range(N), t):
        free = [(i, c) for i in range(t) for c in range(N) if c > piv[i] and c not in piv]
        for vals in itertools.product(range(3), repeat=len(free)):
            rows = [[0] * N for _ in range(t)]
            for i in range(t): rows[i][piv[i]] = 1
            for (i, c), v in zip(free, vals): rows[i][c] = v
            yield [tuple(r) for r in rows]

def span(rows):
    N = len(rows[0]); out = []
    for co in itertools.product(range(3), repeat=len(rows)):
        v = [0] * N
        for c, r in zip(co, rows):
            if c:
                for j in range(N): v[j] = (v[j] + c * r[j]) % 3
        out.append(tuple(v))
    return out

def is_partition_subspace(elems, t):
    """spanned by indicator vectors of t disjoint nonempty sets?"""
    zo = [v for v in elems if all(x in (0, 1) for x in v) and any(v)]
    # minimal 0/1 vectors (by support inclusion)
    mins = [v for v in zo if not any(w != v and all((not w[j]) or v[j] for j in range(len(v))) for w in zo)]
    if len(mins) != t: return False
    supp = [set(j for j, x in enumerate(v) if x) for v in mins]
    if any(supp[i] & supp[j] for i in range(t) for j in range(i + 1, t)): return False
    return set(span(mins)) == set(elems)

print("== A. Lemma 2 (0/1 points of subspaces), exhaustive")
for N in range(1, 7):
    for t in range(1, N + 1):
        if N == 6 and t > 3: continue  # keep runtime small; t>3 at N=6 checked via duality-free bound below
        mx = 0; viol = 0; cnt = 0; part_bad = 0
        for rows in rref_subspaces(N, t):
            el = span(rows); cnt += 1
            z = sum(1 for v in el if all(x in (0, 1) for x in v))
            mx = max(mx, z)
            if z > 2 ** t: viol += 1
            if 4 * z > 3 * 2 ** t and not is_partition_subspace(el, t): part_bad += 1
        print(f"  N={N} t={t}: subspaces {cnt}, max #0/1 points {mx} (2^t={2**t}), violations of <=2^t: {viol}, "
              f">3/4*2^t but not partition: {part_bad}")

# ---------------- B. E_2 ----------------
print("== B. Theorem 2: defect set E_2")
alph = [a for a in itertools.product(range(3), repeat=2) if any(a)]
units = [(1, 0), (0, 1)]
others = [a for a in alph if a not in units]
def defect(y):  # y: dict alpha->bit
    return tuple((y[a] - a[0] * y[(1, 0)] - a[1] * y[(0, 1)]) % 3 for a in others)
E2 = {}
for bits in itertools.product((0, 1), repeat=8):
    y = dict(zip(alph, bits)); E2.setdefault(defect(y), []).append(bits)
E2s = set(E2)
print(f"  |E_2| = {len(E2s)} (0 in E_2: {(0,)*6 in E2s}; assignments with defect 0: {E2[(0,)*6]})")
lines = [e for e in E2s if any(e) and smul(e, 2) in E2s]
print(f"  nonzero e with e and 2e in E_2: {len(lines)} (= {len(lines)//2} lines)")
indep_pairs = 0
for a in lines:
    for b in lines:
        if b in (a, smul(a, 2)): continue
        if all(add(a, b, x, y) in E2s for x in range(3) for y in range(3)): indep_pairs += 1
print(f"  ordered independent pairs (a,b) spanning a 2-dim subspace inside E_2: {indep_pairs}")
# direct brute force: generic piece with one column per nonzero pattern pi in F_3^2\0.
# K = span of the two pattern rows on 8 coordinates; need y_e1,y_e2 in {0,1}^8 such that every coset
# alpha1*y_e1+alpha2*y_e2+K (alpha != 0) contains a 0/1 vector that is NOT in K (else phi(y)=0, no 2-dim gain).
pats = alph
k1 = tuple(p[0] for p in pats); k2 = tuple(p[1] for p in pats)
K = set(span([k1, k2]))
zo = [z for z in itertools.product((0, 1), repeat=8)]
zoset = set(zo)
good = 0
for y1 in zo:
    for y2 in zo:
        ok = True
        for al in alph:
            base = add(y1, y2, al[0], al[1])
            if not any(add(base, kk) in zoset for kk in K): ok = False; break
        if ok and not (set([y1, y2]) & K) and add(y1, y2, 1, 1) not in K:
            # also require the 9 cosets alpha.y + K distinct, i.e. no nonzero alpha.y in K
            if all(add(y1, y2, a0, a1) not in K for (a0, a1) in alph): good += 1
print(f"  brute force, one column per pattern (8 columns, D = 2-dim generic): pairs (y_e1,y_e2) giving a 2-dim realization: {good}")

# ---------------- C. Theorem 3 ----------------
print("== C. Theorem 3: 0/1-complete k-dim subspaces K of F_3^t ({0,1}^t + K = F_3^t)")
for (t, k) in ((2, 1), (3, 1), (4, 2), (5, 2), (5, 1)):
    n = 0; comp = 0
    zo_t = list(itertools.product((0, 1), repeat=t))
    for rows in rref_subspaces(t, k):
        Kel = span(rows); n += 1
        hit = set(add(z, kk) for z in zo_t for kk in Kel)
        if len(hit) == 3 ** t: comp += 1
    print(f"  t={t} k={k}: subspaces {n}, 0/1-complete {comp}")

# ---------------- D. Theorem 5 ----------------
print("== D. Theorem 5: pattern sets T admitting a 2-dim realization (gain or zero-sum)")
zero6 = (0,) * 6
# per defect e: the set of alphas coverable (some assignment with y(alpha)=1)
cover = {e: set(a for bits in E2[e] for a, bit in zip(alph, bits) if bit) for e in E2s}
vecs6 = list(itertools.product(range(3), repeat=6))
feasible = set()
allT = [frozenset(T) for r in range(1, 9) for T in itertools.combinations(alph, r)]
# for each rank-2 C=[u v], G(C) = {pi: C pi in E_2}; T feasible iff T subset G(C) and union of cover over T = all 8
Gsets = {}
for u in vecs6:
    if u == zero6: continue
    for v in vecs6:
        if v == zero6 or v == u or v == smul(u, 2): continue
        G = frozenset(pi for pi in alph if add(u, v, pi[0], pi[1]) in E2s)
        if len(G) < 3: continue
        cv = {pi: cover[add(u, v, pi[0], pi[1])] for pi in G}
        Gsets.setdefault(G, []).append(cv)
for T in allT:
    for G, cvs in Gsets.items():
        if T <= G and any(set().union(*[cv[pi] for pi in T]) >= set(alph) for cv in cvs):
            feasible.add(T); break
def trivial(T):  # some nonzero (a,b): a*p0+b*p1 in {0,1} for all patterns in T  => 0/1 dependency
    return any(all((a * p[0] + b * p[1]) % 3 in (0, 1) for p in T) for (a, b) in alph)
lines_F32 = [frozenset([(a, b), ((2 * a) % 3, (2 * b) % 3)]) for (a, b) in [(0, 1), (1, 0), (1, 1), (1, 2)]]
def misses_line(T): return any(not (T & L) for L in lines_F32)
nontriv = [T for T in feasible if not trivial(T)]
print(f"  feasible T (with trivial ones): {len(feasible)}; trivial (a 0/1 dependency exists): {sum(trivial(T) for T in feasible)}; non-trivial: {len(nontriv)}")
print(f"  non-trivial feasible T that miss a line of F_3^2 (= some dependency has full support): {sum(misses_line(T) for T in nontriv)}")
print(f"  non-trivial feasible T hitting all four lines: {[sorted(T) for T in nontriv if not misses_line(T)]}")
print(f"  min |T| non-trivial: {min(len(T) for T in nontriv)}; sizes: { {s: sum(len(T)==s for T in nontriv) for s in range(1,9)} }")
cand = set(T for T in allT if misses_line(T) and len(T) >= 4 and not trivial(T))
print(f"  subsets of a line-complement with |T|>=4, non-trivial: {len(cand)}; equal to non-trivial feasible family: {cand == set(nontriv)}")
cand_all = set(T for T in allT if misses_line(T) and len(T) >= 4)
print(f"  subsets of a line-complement with |T|>=4 (incl. trivial): {len(cand_all)}; all feasible? {cand_all <= feasible}")
print(f"  number of feasible T NOT inside any of the four 6-sets T_1..T_4: {sum(1 for T in feasible if not misses_line(T))}")

# ---------------- E. Theorem 4 ----------------
print("== E. Theorem 4 (nested-support gadget), independent check")
cls = [(a, b) for a in (1, 2) for b in range(3)]
# relations as linear forms on class-sum space F_3^6 (coordinates w_ab): delta: sum a*w_ab ; delta': sum b*w_ab
r1 = tuple(a % 3 for (a, b) in cls); r2 = tuple(b % 3 for (a, b) in cls)
R = set(span([r1, r2]))
U = {(0, 1): [(1, 1), (1, 2), (2, 2)], (0, 2): [(1, 2), (2, 1), (2, 2)], (1, 0): [(1, 0), (1, 1), (2, 0)],
     (1, 1): [(1, 0), (2, 0), (2, 1)], (1, 2): cls, (2, 0): [(1, 1), (2, 0), (2, 2)],
     (2, 1): [(2, 0), (2, 1), (2, 2)], (2, 2): [(1, 0), (1, 2), (2, 1)]}
ind = lambda L: tuple(1 if c in L else 0 for c in cls)
h1, h2 = ind(U[(1, 0)]), ind(U[(0, 1)])
ok = all(add(ind(U[al]), add(h1, h2, al[0], al[1]), 1, 2) in R for al in alph)
print(f"  all 8 identities union_alpha == alpha1 h1 + alpha2 h2 modulo <delta, delta'>: {ok}")
print(f"  h1,h2 independent modulo relations: {all(add(h1, h2, a, b) not in R for (a, b) in alph)}")
# by exhaustive search: all class-union gadgets (choices of 8 unions) for T = T_1
sols = 0
subsets = list(itertools.product((0, 1), repeat=6))
for y1 in subsets:
    for y2 in subsets:
        if all(any(add(add(y1, y2, al[0], al[1]), z, 2, 1) in R and any(z) for z in subsets) for al in alph) \
           and all(add(y1, y2, a, b) not in R for (a, b) in alph):
            sols += 1
print(f"  exhaustive: class-level (y_e1,y_e2) pairs for T_1 giving a genuine 2-dim realization: {sols}")
# degeneracies: which patterns of empty classes make some listed union empty, and is a zero-sum then forced?
bad = []
for nonempty in itertools.product((0, 1), repeat=6):
    ne = {c for c, f in zip(cls, nonempty) if f}
    if not any(c[1] for c in ne): continue          # delta' = 0
    if ne <= {(1, 1), (2, 2)} or ne <= {(1, 2), (2, 1)}: continue  # delta' proportional to delta
    empties = [al for al in alph if not (set(U[al]) & ne)]
    if empties:
        # forced zero-sum: a nonempty union of nonempty classes whose indicator lies in R restricted to ne
        Rr = set(tuple(x if c in ne else 0 for x, c in zip(r, cls)) for r in R)
        forced = [tuple(int(c in L) for c in cls) for rr in range(1, len(ne) + 1)
                  for L in itertools.combinations(sorted(ne), rr) if tuple(int(c in L) for c in cls) in Rr]
        bad.append((sorted(ne), empties, len(forced) > 0))
print(f"  class-nonemptiness patterns (delta' indep. of delta) with an EMPTY listed union: {len(bad)}")
for b in bad: print("    nonempty classes", b[0], "empty unions for alpha", b[1], "zero-sum class union forced:", b[2])
