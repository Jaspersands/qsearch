"""(a) Actual realizable sets of q+2 random columns: does R(X) contain a 2-dim subgroup?
(b) Exact small-case calibration of the KOW algorithm: n=2 exhaustive, n=3..8 adversarial."""
import itertools, sys, time
import numpy as np
from kow_p3 import solve, verify, recursion_table, nullspace3, FAMS, fam_random

rng = np.random.default_rng(7)

def subset_sums(cols):
    """all subset sums as a set of ints (base-3 encoding)."""
    q = len(cols[0]); pw = 3 ** np.arange(q)
    sums = {0}
    cur = np.zeros((1, q), dtype=np.int64)
    for v in cols:
        cur = np.vstack([cur, (cur + v) % 3])
    enc = (cur @ pw)
    return set(enc.tolist()), pw

def has_2dim_subgroup(cols):
    q = len(cols[0]); S, pw = subset_sums(cols)
    def dec(x):
        out = []
        for _ in range(q): out.append(x % 3); x //= 3
        return np.array(out)
    pts = [dec(x) for x in S if x != 0]
    enc = lambda v: int((v % 3) @ pw)
    # quotient by sign: keep one of v, 2v
    reps = [v for v in pts if enc(v) < enc(2 * v)]
    for i, a in enumerate(reps):
        for b in reps[i + 1:]:
            ok = True
            for ca in range(3):
                for cb in range(3):
                    if (ca, cb) == (0, 0): continue
                    if enc(ca * a + cb * b) not in S: ok = False; break
                if not ok: break
            if ok: return True
    return False

print("== (a) actual realizable set of q+2 random columns (rank q): 2-dim subgroup inside R(X)?")
for q in (4, 5, 6, 7, 8, 9, 10):
    hits = 0; trials = 30 if q <= 8 else 10
    for _ in range(trials):
        while True:
            cols = [rng.integers(0, 3, q) for _ in range(q + 2)]
            A = np.array(cols).T % 3
            if len(nullspace3(A)) == 2: break
        hits += has_2dim_subgroup(cols)
    print(f"  q={q}: {hits}/{trials} instances have a 2-dim subgroup inside R(X) (|R| ~ 2^{q+2}/3^q density)")

print("== (b) exact small cases for the implemented KOW algorithm")
tab = recursion_table(10)
# n = 2 exhaustive: all multisets of m vectors in F_3^2 (as sorted tuples)
vecs2 = [np.array(v) for v in itertools.product(range(3), repeat=2)]
for m in (5, 6):
    fails = 0; total = 0
    for combo in itertools.combinations_with_replacement(range(9), m):
        inst = [vecs2[i] for i in combo]
        total += 1
        S = solve(inst)
        if S is None: fails += 1
        else: verify(inst, S)
    print(f"  n=2, m={m}: multisets {total}, algorithm failures {fails}  (2n+1={5}, m_2={tab[2]})")
# n = 3: all multisets of 7 vectors from 27 is C(33,7)=4.3M -- too many for python; random + adversarial
def adversarial(n, m, iters, rng):
    """hill-climb on an instance to make the algorithm fail (score = depth reached before running out)."""
    best_fail = None
    for start in range(iters):
        inst = [rng.integers(0, 3, n) for _ in range(m)]
        S = solve(inst)
        if S is None: return inst
        # local search: perturb one vector, accept if solve returns None or the total consumed grows
        def score(ins):
            st = []; r = solve(ins, st)
            return (10**6 if r is None else sum(w for (_, w, _) in st))
        sc = score(inst)
        for step in range(60):
            j = rng.integers(0, m); old = inst[j].copy(); inst[j] = rng.integers(0, 3, n)
            s2 = score(inst)
            if s2 >= 10**6: return inst
            if s2 >= sc: sc = s2
            else: inst[j] = old
    return None
for n in (3, 4, 5, 6, 7, 8):
    for m in range(2 * n + 1, tab[n] + 1):
        t0 = time.time()
        bad = adversarial(n, m, iters=25 if n <= 5 else 10, rng=rng)
        if bad is None:
            print(f"  n={n}, m={m}: no failure found (random+climb); m_n={tab[n]}"); break_at = m
            if m >= tab[n]: break
            # continue upwards only to report the smallest m with no failure found
            break
        else:
            print(f"  n={n}, m={m}: FAILURE instance found for the algorithm: {[tuple(int(x) for x in v) for v in bad][:12]}{'...' if m>12 else ''}")
