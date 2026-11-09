"""Structured-family and random attacks on Theorem A with the strict solver (all invariants
asserted).  Every instance has exactly m = ceil(closed_form(n)) columns, so "exhausted" is a
refutation.  Families (each padded with the family's own generator, never random filler unless the
family says so, so that the adversarial structure persists through the whole run):

  random            uniform columns
  dualdist3         pool blocks = the columns of a parity-check matrix of a ternary Hamming code
                    (all projective points of PG(t-1,3)), repeated and sign-flipped: dual distance
                    exactly 3 everywhere, every low-weight dependency (weight 3) forced
  golay             ternary Golay [11,6,5] / [12,6,6] generator columns embedded in blocks
  series_pairs      every column duplicated (classes of size exactly 2: Var = 4N/9 attained)
  series_pairs_neg  every column followed by its negative
  chains            long chains e_i - e_{i+1} (series classes of size L, peeled every round)
  lowrank           columns in a subspace of dimension n/3
  lowrank_grow      columns in a subspace whose dimension grows with the stream index
  two_subspaces     alternating between two complementary subspaces
  sparse            weight-1 and weight-2 columns only
  weight2_lines     e_i + e_j for all pairs then e_i (complete graph: all triangles are dependencies)
  triples           blocks a, b, -(a+b): every block is a weight-3 dependency
  repeated          the same 2n vectors cycled
  signed_blocks     +v, +v, -v blocks
  dup_pool_order    adversarial ORDER: the pool at each stage is pairs of proportional columns
                    interleaved with a basis, so after peeling the code has many size-2 classes

For n in a grid up to 100 (proof variant); the code variant is run at n <= 40.
"""
import math, sys, time, itertools
import numpy as np
from strict_wnest import solve_checked, guarantee, closed_form, kernel, rank

def ham_points(t):
    pts = []
    for c in itertools.product(range(3), repeat=t):
        v = np.array(c, dtype=np.int64)
        nz = np.nonzero(v)[0]
        if len(nz) and v[nz[0]] == 1:
            pts.append(v)
    return pts

def fam_random(n, m, rng):
    return [rng.integers(0, 3, n) for _ in range(m)]

def fam_dualdist3(n, m, rng):
    t = max(2, min(n, 5))
    pts = ham_points(t)
    out = []
    while len(out) < m:
        off = int(rng.integers(0, max(1, n - t + 1)))
        order = rng.permutation(len(pts))
        for i in order:
            v = np.zeros(n, dtype=np.int64); v[off:off + t] = pts[i] * int(rng.integers(1, 3))
            out.append(v)
    return out[:m]

def golay_generator():
    # extended ternary Golay [12,6,6]: G = [I | A], A circulant-based (standard construction)
    A = np.array([[0, 1, 1, 1, 1, 1],
                  [1, 0, 1, 2, 2, 1],
                  [1, 1, 0, 1, 2, 2],
                  [1, 2, 1, 0, 1, 2],
                  [1, 2, 2, 1, 0, 1],
                  [1, 1, 2, 2, 1, 0]], dtype=np.int64)
    G = np.hstack([np.eye(6, dtype=np.int64), A]) % 3
    return G

def fam_golay(n, m, rng):
    G = golay_generator()                   # 6 x 12 ; its 12 columns live in F_3^6
    t = min(6, n)
    cols = [G[:t, j] for j in range(12)]
    out = []
    while len(out) < m:
        off = int(rng.integers(0, max(1, n - t + 1)))
        for j in rng.permutation(12):
            v = np.zeros(n, dtype=np.int64); v[off:off + t] = cols[j] * int(rng.integers(1, 3)); out.append(v)
        if rng.random() < 0.3:              # also Golay codewords themselves as columns (weight 6)
            x = rng.integers(0, 3, 6); cw = (x @ G) % 3
            v = np.zeros(n, dtype=np.int64); v[off:off + min(12, n - off)] = cw[:min(12, n - off)]; out.append(v)
    return out[:m]

def fam_series_pairs(n, m, rng, neg=False):
    out = []
    while len(out) < m:
        v = rng.integers(0, 3, n); out.append(v); out.append((2 * v) % 3 if neg else v.copy())
    return out[:m]

def fam_chains(n, m, rng, L):
    out = []
    while len(out) < m:
        start = int(rng.integers(0, n))
        v = np.zeros(n, dtype=np.int64); v[start] = 1; out.append(v)
        for j in range(1, L):
            v = np.zeros(n, dtype=np.int64); v[(start + j) % n] = 1; v[(start + j - 1) % n] = 2; out.append(v)
    return out[:m]

def fam_lowrank(n, m, rng, k):
    out = []
    while len(out) < m:
        v = np.zeros(n, dtype=np.int64); v[:k] = rng.integers(0, 3, k); out.append(v)
    return out[:m]

def fam_lowrank_grow(n, m, rng):
    out = []
    for i in range(m):
        k = max(1, min(n, 1 + i * n // (m // 2 + 1)))
        v = np.zeros(n, dtype=np.int64); v[:k] = rng.integers(0, 3, k); out.append(v)
    return out

def fam_two_subspaces(n, m, rng):
    out = []; h = n // 2
    for i in range(m):
        v = np.zeros(n, dtype=np.int64)
        if i % 2 == 0: v[:h] = rng.integers(0, 3, h)
        else: v[h:] = rng.integers(0, 3, n - h)
        out.append(v)
    return out

def fam_sparse(n, m, rng):
    out = []
    while len(out) < m:
        v = np.zeros(n, dtype=np.int64)
        if rng.random() < 0.3:
            v[int(rng.integers(0, n))] = int(rng.integers(1, 3))
        else:
            i, j = rng.choice(n, 2, replace=False); v[i] = int(rng.integers(1, 3)); v[j] = int(rng.integers(1, 3))
        out.append(v)
    return out[:m]

def fam_weight2_lines(n, m, rng):
    out = []
    pairs = list(itertools.combinations(range(n), 2))
    while len(out) < m:
        for idx in rng.permutation(len(pairs)):
            i, j = pairs[idx]
            v = np.zeros(n, dtype=np.int64); v[i] = 1; v[j] = 1; out.append(v)
            if len(out) >= m: break
        for i in range(n):
            v = np.zeros(n, dtype=np.int64); v[i] = 1; out.append(v)
    return out[:m]

def fam_triples(n, m, rng):
    out = []
    while len(out) < m:
        a = rng.integers(0, 3, n); b = rng.integers(0, 3, n); c = (-(a + b)) % 3
        out += [a, b, c]
    return out[:m]

def fam_repeated(n, m, rng):
    base = [rng.integers(0, 3, n) for _ in range(2 * n)]
    return [base[i % len(base)].copy() for i in range(m)]

def fam_signed_blocks(n, m, rng):
    out = []
    while len(out) < m:
        v = rng.integers(0, 3, n); out += [v, v.copy(), (2 * v) % 3]
    return out[:m]

def fam_dup_pool_order(n, m, rng):
    """blocks of 1.5n+: a random basis-ish set of n columns then pairs (v, 2v) so that each pool
    has as many size-2 classes as possible."""
    out = []
    while len(out) < m:
        for _ in range(n):
            out.append(rng.integers(0, 3, n))
        for _ in range(n):
            v = rng.integers(0, 3, n); out += [v, (2 * v) % 3]
    return out[:m]

FAMILIES = {
    "random": fam_random,
    "dualdist3": fam_dualdist3,
    "golay": fam_golay,
    "series_pairs": lambda n, m, r: fam_series_pairs(n, m, r, False),
    "series_pairs_neg": lambda n, m, r: fam_series_pairs(n, m, r, True),
    "chains_L5": lambda n, m, r: fam_chains(n, m, r, 5),
    "chains_Lhalf": lambda n, m, r: fam_chains(n, m, r, max(3, n // 2)),
    "lowrank_third": lambda n, m, r: fam_lowrank(n, m, r, max(1, n // 3)),
    "lowrank_grow": fam_lowrank_grow,
    "two_subspaces": fam_two_subspaces,
    "sparse": fam_sparse,
    "weight2_lines": fam_weight2_lines,
    "triples": fam_triples,
    "repeated": fam_repeated,
    "signed_blocks": fam_signed_blocks,
    "dup_pool_order": fam_dup_pool_order,
}

def run_family(name, n, variant, rng, brute=True):
    m = math.ceil(closed_form(n))
    vecs = FAMILIES[name](n, m, rng)
    assert len(vecs) == m
    t0 = time.time()
    try:
        sol, R, err = solve_checked(n, vecs, variant, brute_var=brute)
    except AssertionError as e:
        return dict(name=name, n=n, m=m, status="ASSERT " + str(e)[:200], vecs=vecs)
    if err:
        return dict(name=name, n=n, m=m, status="EXHAUSTED " + err, vecs=vecs)
    two = [c for c in R.costs if c[1] == 2]
    return dict(name=name, n=n, m=m, status="ok", needed=R.m_needed, guar=guarantee(n, variant),
                pieces=len(R.costs), two=len(two), max_slack=R.max_slack, max_over_q=R.max_over_q,
                max_z=round(R.max_zsig, 3), max_class=R.stats.get("max_class", 0),
                peeled=R.stats.get("peeled_classes", 0), wit=len(sol), secs=round(time.time() - t0, 1))

if __name__ == "__main__":
    rng = np.random.default_rng(1108)
    ns = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [4, 5, 6, 7, 8, 9, 10, 12, 16, 20, 25, 30, 40, 60, 80, 100]
    variant = sys.argv[2] if len(sys.argv) > 2 else "proof"
    reps = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    print(f"variant={variant}; m = ceil(closed_form(n)) for every instance; strict asserts on")
    print("family              n   m     status  needed  guar  pieces(2d)  max wt-(r*+2)  max|X|-q  max z  maxclass peeled  |witness| s")
    fails = []
    for n in ns:
        for name in FAMILIES:
            for rep in range(reps):
                res = run_family(name, n, variant, rng, brute=(n <= 40))
                if res["status"] != "ok":
                    fails.append(res)
                    print(f"{name:18s} {n:3d} {res['m']:5d}  {res['status']}")
                    np.save(f"FAIL_{name}_n{n}_rep{rep}.npy", np.array(res["vecs"]))
                else:
                    print(f"{name:18s} {n:3d} {res['m']:5d}  ok      {res['needed']:5d}  {res['guar']:5d}  {res['pieces']:3d}({res['two']:3d})   "
                          f"{res['max_slack']:3d}            {res['max_over_q']:3d}      {res['max_z']:6.3f}  {res['max_class']:3d}    {res['peeled']:3d}   {res['wit']:4d}  {res['secs']}")
                sys.stdout.flush()
    print(f"\nfailures: {len(fails)}")
    for f in fails:
        print(" ", f["name"], f["n"], f["status"])
