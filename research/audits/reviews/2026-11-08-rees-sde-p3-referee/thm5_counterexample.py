"""Explicit counterexample to Theorem 5 of 2026-11-08-rees-sde-p3.md.
T = {(0,1),(1,1),(1,2),(2,0),(2,1)} meets all four lines of F_3^2 (so no combination of
delta, delta' has full support, T is in none of T_1..T_4), no combination is {0,1}-valued (no
trivial zero-sum), yet a 2-dim subgroup is realized for EVERY choice of columns with these
dependencies.  We find C and local assignments, build random instances with D(X) = <delta,delta'>
exactly, and verify by direct summation that h1, h2 are independent and all 9 combinations are
subset sums of X."""
import itertools, random

def add(u, v, a=1, b=1): return tuple((a * x + b * y) % 3 for x, y in zip(u, v))
alph = [a for a in itertools.product(range(3), repeat=2) if any(a)]
others = [a for a in alph if a not in ((1, 0), (0, 1))]
E2 = {}
for bits in itertools.product((0, 1), repeat=8):
    y = dict(zip(alph, bits))
    e = tuple((y[a] - a[0] * y[(1, 0)] - a[1] * y[(0, 1)]) % 3 for a in others)
    E2.setdefault(e, []).append(y)
T = [(0, 1), (1, 1), (1, 2), (2, 0), (2, 1)]
assert not any(all((a * p[0] + b * p[1]) % 3 in (0, 1) for p in T) for (a, b) in alph), "trivial"
lines = [{(0, 1), (0, 2)}, {(1, 0), (2, 0)}, {(1, 1), (2, 2)}, {(1, 2), (2, 1)}]
assert all(set(T) & L for L in lines)
found = None
for u in itertools.product(range(3), repeat=6):
    for v in itertools.product(range(3), repeat=6):
        if not any(u) or not any(v) or v == u or v == add(u, u, 2, 0): continue
        if all(add(u, v, p[0], p[1]) in E2 for p in T):
            # choose per class a list of local assignments covering all alpha
            opts = {p: E2[add(u, v, p[0], p[1])] for p in T}
            cov = set(a for p in T for y in opts[p] for a in alph if y[a])
            if cov == set(alph): found = (u, v, opts); break
    if found: break
u, v, opts = found
print("C e1 =", u, " C e2 =", v)
# minimal set of (class, assignment) columns covering all alphas (greedy)
need = set(alph); chosen = []
while need:
    best = max(((p, y) for p in T for y in opts[p]), key=lambda py: len([a for a in need if py[1][a]]))
    chosen.append(best); need -= {a for a in alph if best[1][a]}
for p in T:  # every class nonempty
    if not any(c[0] == p for c in chosen): chosen.append((p, opts[p][0]))
print("columns (pattern, local assignment y(alpha) for alpha in", alph, "):")
for p, y in chosen: print("  ", p, [y[a] for a in alph])

def nullspace(M, ncols):
    """M: list of rows (length ncols) over F_3; return basis of right kernel."""
    M = [list(r) for r in M]; piv = []; r = 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(M)) if M[i][c] % 3), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]; inv = M[r][c] % 3
        M[r] = [(x * inv) % 3 for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % 3:
                f = M[i][c]; M[i] = [(a - f * b) % 3 for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    basis = []
    for f in [c for c in range(ncols) if c not in piv]:
        x = [0] * ncols; x[f] = 1
        for i, c in enumerate(piv): x[c] = (-M[i][f]) % 3
        basis.append(x)
    return basis

rng = random.Random(5)
trials = 0; okc = 0
for q in (12, 20, 40):
    for rep in range(10):
        cols_spec = chosen + [rng.choice([(p, y) for p in T for y in opts[p]]) for _ in range(rng.randint(0, 6))]
        N = len(cols_spec)
        dl = [p[0] for p, _ in cols_spec]; dl2 = [p[1] for p, _ in cols_spec]
        # random q x N matrix whose kernel is exactly <dl, dl2>: rows = random combos of a basis of the
        # orthogonal complement of <dl,dl2> (dimension N-2); need q >= N-2.
        comp = nullspace([dl, dl2], N)
        assert len(comp) == N - 2 and q >= N - 2
        rows = []
        for _ in range(q):
            co = [rng.randrange(3) for _ in comp]
            rows.append([sum(c * b[j] for c, b in zip(co, comp)) % 3 for j in range(N)])
        ker = nullspace(rows, N)
        if len(ker) != 2: continue  # rows did not span the complement; skip
        trials += 1
        colv = [tuple(rows[i][j] for i in range(q)) for j in range(N)]
        def S(sel): return tuple(sum(colv[j][i] for j in sel) % 3 for i in range(q))
        ysets = {a: [j for j, (p, y) in enumerate(cols_spec) if y[a]] for a in alph}
        h1, h2 = S(ysets[(1, 0)]), S(ysets[(0, 1)])
        good = all(S(ysets[a]) == add(h1, h2, a[0], a[1]) for a in alph)
        indep = all(any(add(h1, h2, a[0], a[1])) for a in alph)
        okc += good and indep
print(f"random instances with D(X)=<delta,delta'> exactly: {okc}/{trials} realize a 2-dim subgroup <h1,h2> (all 8 unions verified by summation)")
