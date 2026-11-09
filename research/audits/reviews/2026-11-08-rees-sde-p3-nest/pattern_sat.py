"""Which pattern sets T of a k-dimensional dependency bundle admit a d-dimensional realization
for EVERY column set carrying those patterns?  Own SAT encoding (pycosat), used to (i) re-check
the d = 2 facts (Theorem 2, Theorem 4, the referee's 82 non-trivial sets), (ii) settle d = 3
from k = 3 for the pattern sets that worst-case-findable mechanisms produce (projective point
sets of PG(2,3) up to PGL(3,3)), in particular the nested chain and 'all points off a line'.

Encoding.  Column i has pattern pi_i in F_3^k \\ 0 and unit values s_i in {0,1}^d; with a map
C = (c_alpha)_{alpha in A'} (A' = F_3^d minus 0 and the unit vectors), its local assignment is
y_i(e_j) = s_j, y_i(alpha) = <c_alpha, pi_i> + alpha.s_i, which must lie in {0,1}.  Then
y_alpha - sum_j alpha_j y_{e_j} is the combination of the k dependencies with coefficients c_alpha,
so sum(y_alpha) = alpha.h.  Feasible(T) iff some C admits, for every pi in T, at least one s, and
the used (pi, s) cover every alpha (some y_i(alpha) = 1).  Trivial(T): some nonzero combination
of the dependencies is {0,1}-valued on T (a zero-sum set for free); counted separately.
"""
import itertools, sys, time
import numpy as np
try:
    import pycosat
except ImportError:      # the k = 4 check below uses cadical instead
    pycosat = None
import os, subprocess, tempfile, shutil

LRAT_CHECK = os.environ.get('LRAT_CHECK', os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-09-lrat-checker-fix', 'lrat-check')))   # fixed build (9 Nov); run its build.sh


_LRAT_SOUND = {}


def lrat_check_is_sound(checker):
    """Preflight added 9 Nov 2026 (research/audits/reviews/2026-11-09-lrat-checker-fix/): the upstream
    lrat-check accepted an empty clause without a conflict, so any CNF 'verified' with a one-line proof.
    True iff `checker` rejects two such proofs of a satisfiable CNF and verifies a correct proof of an
    unsatisfiable one. Cached per checker path."""
    if checker not in _LRAT_SOUND:
        d = tempfile.mkdtemp()

        def verified(cnf, prf):
            a, b = os.path.join(d, 'c.cnf'), os.path.join(d, 'c.lrat')
            with open(a, 'w') as f:
                f.write(cnf)
            with open(b, 'w') as f:
                f.write(prf)
            r = subprocess.run([checker, a, b], capture_output=True, text=True)
            return r.returncode == 0 and 'c VERIFIED' in r.stdout.splitlines()
        try:
            _LRAT_SOUND[checker] = (not verified('p cnf 1 1\n1 0\n', '2 0 0\n')
                                    and not verified('p cnf 1 1\n1 0\n', '2 0 1 -1 0\n')
                                    and verified('p cnf 1 2\n1 0\n-1 0\n', '3 0 1 2 0\n'))
        finally:
            shutil.rmtree(d, ignore_errors=True)
    return _LRAT_SOUND[checker]


def require_sound_lrat_check(checker):
    if not lrat_check_is_sound(checker):
        raise RuntimeError(f'{checker} failed the lrat-check negative control (it verifies a bogus proof); '
                           'use the fixed build, research/audits/reviews/2026-11-09-lrat-checker-fix/build.sh')

def cadical_solve(nvars, cl):
    """DIMACS -> cadical with an LRAT proof; an UNSAT answer is accepted only after lrat-check
    prints 'c VERIFIED'.  Returns 'UNSAT' or a list of signed literals."""
    work = tempfile.mkdtemp()
    cnf, prf = os.path.join(work, 'p.cnf'), os.path.join(work, 'p.lrat')
    with open(cnf, 'w') as f:
        f.write(f'p cnf {nvars} {len(cl)}\n')
        for c in cl:
            f.write(' '.join(map(str, c)) + ' 0\n')
    r = subprocess.run(['cadical', '--lrat=true', '--binary=false', cnf, prf], capture_output=True, text=True)
    if r.returncode == 20:
        require_sound_lrat_check(LRAT_CHECK)
        ch = subprocess.run([LRAT_CHECK, cnf, prf], capture_output=True, text=True)
        assert ch.returncode == 0 and 'c VERIFIED' in ch.stdout and 'failed' not in ch.stdout, ch.stdout[-300:]
        print('   [cadical UNSAT, LRAT VERIFIED]', flush=True)
        return 'UNSAT'
    assert r.returncode == 10, r.stdout[-300:]
    lits = []
    for line in r.stdout.splitlines():
        if line.startswith('v'):
            lits += [int(x) for x in line.split()[1:] if x != '0']
    return lits

def feasible(d, k, T, model=False, solver='pycosat'):
    T = [tuple(p) for p in T]
    alph = [a for a in itertools.product(range(3), repeat=d) if any(a)]
    units = [tuple(1 if j == i else 0 for j in range(d)) for i in range(d)]
    Ap = [a for a in alph if a not in units]
    opts = list(itertools.product(range(3), repeat=k))
    Svals = list(itertools.product((0, 1), repeat=d))
    cnt = [0]
    def nv():
        cnt[0] += 1
        return cnt[0]
    cvar = {(a, c): nv() for a in Ap for c in opts}          # c_alpha = c (one-hot)
    uvar = {(p, s): nv() for p in T for s in Svals}           # class p uses unit values s
    cl = []
    dot = lambda v, w: sum(i * j for i, j in zip(v, w)) % 3
    for a in Ap:
        cl.append([cvar[(a, c)] for c in opts])
        for c1, c2 in itertools.combinations(opts, 2):
            cl.append([-cvar[(a, c1)], -cvar[(a, c2)]])
    for p in T:
        cl.append([uvar[(p, s)] for s in Svals])                              # class nonempty
        for s in Svals:
            for a in Ap:
                for c in opts:
                    if (dot(c, p) + dot(a, s)) % 3 == 2:                      # value 2 forbidden
                        cl.append([-uvar[(p, s)], -cvar[(a, c)]])
    for j in range(d):                                                        # cover unit alphas
        cl.append([uvar[(p, s)] for p in T for s in Svals if s[j] == 1])
    for a in Ap:                                                              # cover other alphas
        cov = []
        for p in T:
            for s in Svals:
                good = [cvar[(a, c)] for c in opts if (dot(c, p) + dot(a, s)) % 3 == 1]
                if not good:
                    continue
                v = nv(); cov.append(v)
                cl.append([-v, uvar[(p, s)]]); cl.append([-v] + good)
        cl.append(cov)
    if solver == 'cadical':
        sol = cadical_solve(cnt[0], cl)
    else:
        sol = pycosat.solve(cl)
    if sol == "UNSAT":
        return False, None
    if not model:
        return True, None
    pos = set(l for l in sol if l > 0)
    C = {a: next(c for c in opts if cvar[(a, c)] in pos) for a in Ap}
    used = {p: [s for s in Svals if uvar[(p, s)] in pos] for p in T}
    return True, (C, used)

def trivial(T, k):
    for f in itertools.product(range(3), repeat=k):
        if any(f) and all(sum(x * y for x, y in zip(f, p)) % 3 in (0, 1) for p in T):
            return True
    return False

def nz(k):
    return [p for p in itertools.product(range(3), repeat=k) if any(p)]

# ---- PG(2,3): 13 points, PGL(3,3) orbits on point sets
def pg2_points():
    pts = []
    for v in itertools.product(range(3), repeat=3):
        if any(v) and v[next(i for i, x in enumerate(v) if x)] == 1:
            pts.append(v)
    return pts

def gl3():
    mats = []
    for entries in itertools.product(range(3), repeat=9):
        M = np.array(entries, dtype=np.int64).reshape(3, 3)
        if round(np.linalg.det(M)) % 3 != 0:
            mats.append(M)
    return mats

def point_perms(pts):
    index = {p: i for i, p in enumerate(pts)}
    perms = set()
    for M in gl3():
        perm = []
        for p in pts:
            w = tuple(int(x) for x in (M @ np.array(p)) % 3)
            nzi = next(i for i, x in enumerate(w) if x)
            s = w[nzi]
            w = tuple((x * s) % 3 for x in w)
            perm.append(index[w])
        perms.add(tuple(perm))
    return sorted(perms)

def orbits_of_pointsets(pts, perms):
    seen = set()
    reps = []
    for mask in range(1, 1 << 13):
        if mask in seen:
            continue
        orb = set()
        for perm in perms:
            m2 = 0
            for i in range(13):
                if mask >> i & 1:
                    m2 |= 1 << perm[i]
            orb.add(m2)
        seen |= orb
        reps.append((min(orb), len(orb)))
    return reps

def mask_to_T(mask, pts):
    T = []
    for i in range(13):
        if mask >> i & 1:
            p = pts[i]
            T.append(p); T.append(tuple((2 * x) % 3 for x in p))
    return T

def lines_pg2(pts):
    lines = []
    for f in pts:  # dual points = lines
        lines.append(frozenset(i for i, p in enumerate(pts) if sum(a * b for a, b in zip(f, p)) % 3 == 0))
    return lines

if __name__ == "__main__":
    t0 = time.time()
    nz2 = nz(2)
    T1 = [p for p in nz2 if p[0] != 0]
    T5 = [(0, 1), (1, 1), (1, 2), (2, 0), (2, 1)]
    print("d=2,k=2: all 8 patterns:", feasible(2, 2, nz2)[0], "| T_1 (nested):", feasible(2, 2, T1)[0],
          "| referee 5-set:", feasible(2, 2, T5)[0])
    feas = [T for r in range(1, 9) for T in itertools.combinations(nz2, r) if feasible(2, 2, list(T))[0]]
    print(f"d=2,k=2: feasible T: {len(feas)}; non-trivial: {sum(not trivial(T, 2) for T in feas)} (referee: 218 / 82)")
    print("d=3,k=2 (Theorem 3): all 8:", feasible(3, 2, nz2)[0], "| T_1:", feasible(3, 2, T1)[0])
    nz3 = nz(3)
    t1 = time.time()
    print("d=3,k=3: all 26 patterns:", feasible(3, 3, nz3)[0], f"  [{time.time()-t1:.1f}s]")
    off = [p for p in nz3 if p[0] != 0]
    print("d=3,k=3: delta_1 full support (9 points off a line, 18 patterns):", feasible(3, 3, off)[0])
    chain = [p for p in nz3 if p[0] != 0 and (p[2] == 0 or p[1] != 0)]
    print("d=3,k=3: nested chain supp d3 <= supp d2 <= supp d1 = X (14 patterns, 7 points):",
          feasible(3, 3, chain)[0], "| trivial:", trivial(chain, 3))
    fork = [p for p in nz3 if p[0] != 0 and (p[1] == 0 or p[2] == 0)]
    print("d=3,k=3: d2, d3 disjoint supports inside supp d1 (10 patterns, 5 points):",
          feasible(3, 3, fork)[0], "| trivial:", trivial(fork, 3))
    nest_plus = [p for p in nz3 if (p[0] != 0 and p[2] == 0) or (p[0] == 0 and p[1] == 0 and p[2] != 0)]
    print("d=3,k=3: nested pair + disjoint third (sanity, must be SAT):", feasible(3, 3, nest_plus)[0])
    sys.stdout.flush()
    # orbit enumeration of projective point sets
    pts = pg2_points()
    perms = point_perms(pts)
    print(f"PGL(3,3) acting on PG(2,3): {len(perms)} permutations of 13 points")
    reps = orbits_of_pointsets(pts, perms)
    print(f"orbits of nonempty point sets: {len(reps)}")
    lines = lines_pg2(pts)
    feas_reps = []
    for mask, size in reps:
        T = mask_to_T(mask, pts)
        if trivial(T, 3):
            continue
        ok, _ = feasible(3, 3, T)
        if ok:
            npts = bin(mask).count("1")
            # structure: does T miss a whole line? how many lines does it miss / meet in <= 1 point?
            missed = sum(1 for L in lines if not any(mask >> i & 1 for i in L))
            onept = sum(1 for L in lines if sum(mask >> i & 1 for i in L) <= 1)
            feas_reps.append((npts, mask, size, missed, onept))
    feas_reps.sort()
    print(f"d=3,k=3: non-trivial feasible point-set orbits: {len(feas_reps)}; by |points|:",
          {n_: sum(1 for f in feas_reps if f[0] == n_) for n_ in sorted(set(f[0] for f in feas_reps))})
    print("largest feasible point sets (|pts|, mask, orbit size, #lines missed, #lines met in <=1 point):")
    for f in feas_reps[-12:]:
        print("   ", f, "points:", [pts[i] for i in range(13) if f[1] >> i & 1])
    print(f"total time {time.time()-t0:.0f}s")
