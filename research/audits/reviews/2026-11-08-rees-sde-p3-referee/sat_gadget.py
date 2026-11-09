"""SAT test (pycosat) for 'generic' d-dimensional realizations from a k-dimensional bundle K of
dependencies with pattern set T in F_3^k (one class per pattern, any number of columns per class).

A realization: for each column i a local assignment y_i: F_3^d\\0 -> {0,1}, and a linear map
C: F_3^k -> F_3^{A'} (A' = F_3^d minus 0 and the unit vectors) with
   y_i(alpha) - sum_j alpha_j y_i(e_j) = <c_alpha, pi_i>   for all alpha in A'   (defect = C pi_i),
and every alpha != 0 covered (some column has y(alpha) = 1).  Then y_alpha - alpha.y lies in K, so
sum(y_alpha) = alpha.h for every choice of columns whose dependency space contains K; if moreover
no nonzero element of K is {0,1}-valued on T, then D(X) = K forces h_1..h_d independent: a genuine
d-dimensional gain for EVERY such column set.  Columns of one class may carry different y's.

Validation: reproduces the d = 2 facts (all 8 patterns UNSAT = Theorem 2; T_1 SAT = Theorem 4;
the 5-set counterexample to Theorem 5 SAT; d = 3 from k = 2 UNSAT = Theorem 3).
Main question: d = k = 3 with T = {pi : pi_1 != 0} ('nested': delta_1 has full support)."""
import itertools, sys
import pycosat

def solve(d, k, T, want_model=False):
    alph = [a for a in itertools.product(range(3), repeat=d) if any(a)]
    units = [tuple(1 if j == i else 0 for j in range(d)) for i in range(d)]
    Ap = [a for a in alph if a not in units]
    opts = list(itertools.product(range(3), repeat=k))
    S = list(itertools.product((0, 1), repeat=d))
    nv = [0]
    def new():
        nv[0] += 1; return nv[0]
    x = {(a, c): new() for a in Ap for c in opts}
    u = {(p, s): new() for p in T for s in S}
    cl = []
    for a in Ap:
        cl.append([x[(a, c)] for c in opts])
        for c1, c2 in itertools.combinations(opts, 2): cl.append([-x[(a, c1)], -x[(a, c2)]])
    dot = lambda v, w: sum(i * j for i, j in zip(v, w)) % 3
    for p in T:
        cl.append([u[(p, s)] for s in S])
        for s in S:
            for a in Ap:
                for c in opts:
                    if (dot(c, p) + dot(a, s)) % 3 == 2: cl.append([-u[(p, s)], -x[(a, c)]])
    for j, e in enumerate(units):
        cl.append([u[(p, s)] for p in T for s in S if s[j] == 1])
    for a in Ap:
        cov = []
        for p in T:
            for s in S:
                good = [x[(a, c)] for c in opts if (dot(c, p) + dot(a, s)) % 3 == 1]
                if not good: continue
                v = new(); cov.append(v)
                cl.append([-v, u[(p, s)]]); cl.append([-v] + good)
        cl.append(cov)
    sol = pycosat.solve(cl)
    if sol == "UNSAT": return False, None
    if not want_model: return True, None
    sset = set(l for l in sol if l > 0)
    Cmap = {a: next(c for c in opts if x[(a, c)] in sset) for a in Ap}
    used = {p: [s for s in S if u[(p, s)] in sset] for p in T}
    return True, (Cmap, used)

def trivial(T, k):
    return any(all(sum(f * q for f, q in zip(fn, p)) % 3 in (0, 1) for p in T)
               for fn in itertools.product(range(3), repeat=k) if any(fn))

if __name__ == "__main__":
    nz2 = [p for p in itertools.product(range(3), repeat=2) if any(p)]
    T1 = [p for p in nz2 if p[0] != 0]
    T5 = [(0, 1), (1, 1), (1, 2), (2, 0), (2, 1)]
    print("validation d=2,k=2: all 8 patterns:", solve(2, 2, nz2)[0], "| T_1:", solve(2, 2, T1)[0],
          "| 5-set counterexample:", solve(2, 2, T5)[0])
    feas = [T for r in range(1, 9) for T in itertools.combinations(nz2, r) if solve(2, 2, list(T))[0]]
    print(f"validation d=2,k=2: feasible T {len(feas)}, non-trivial {sum(not trivial(T,2) for T in feas)}  (structure_checks.py: 218 / 82)")
    print("validation d=3,k=2 (Theorem 3): all 8 patterns:", solve(3, 2, nz2)[0], "| T_1:", solve(3, 2, T1)[0])
    nz3 = [p for p in itertools.product(range(3), repeat=3) if any(p)]
    N3 = [p for p in nz3 if p[0] != 0]
    sys.stdout.flush()
    ok, model = solve(3, 3, N3, want_model=True)
    print("MAIN d=3,k=3, T = {pi_1 != 0} (18 patterns, delta_1 full support):", ok, "| T trivial:", trivial(N3, 3))
    if ok:
        Cmap, used = model
        print("  local s-vectors used per class (number of columns needed):", {p: len(v) for p, v in used.items()})
    print("d=3,k=3, all 26 patterns:", solve(3, 3, nz3)[0])
    print("d=2,k=3, all 26 patterns:", solve(2, 3, nz3)[0])
    sys.stdout.flush()
    nz4 = [p for p in itertools.product(range(3), repeat=4) if any(p)]
    N4 = [p for p in nz4 if p[0] != 0]
    print("d=4,k=4, T = {pi_1 != 0} (54 patterns):", solve(4, 4, N4)[0])
    print("d=3,k=4, T = {pi_1 != 0}:", solve(3, 4, N4)[0])
