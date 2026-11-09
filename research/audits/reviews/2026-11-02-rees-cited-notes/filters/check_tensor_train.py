"""Item (iii): tensor-train filter, exact small checks over F_p.

1. Gram falsifier: Gram-based support recovery fails over F_5.
2. Gauge invariance of the prefix contraction spaces U_i (exact flattening).
3. A CANONICAL gauge exists over F_p: a local echelon sweep (no full tensor)
   returns identical cores for gauge-equivalent and redundant-bond TTs.
4. Staged subspace stabilizers: exhaustive comparison of K_N with H, both with
   the global prefix condition and the local (R_{i-1}(g) tensor g_i) condition.
5. p-group premise: a non-p scalar action preserves every U_i but not A.
6. Repo solver (read-only import): agrees with exhaustive H on a p=5 case;
   on the note's p=3 control the SITE index is 3 <= p but stage 2 has index > p.
"""
import os
import random
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fp import rref, rank, matmul, inverse, identity, kron, coords, ut_group  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, *[".."] * 5))


# ---------- tensor trains ----------

def contract(cores, p):
    dims = [len(c[0]) for c in cores]
    A = {}
    for x in product(*[range(d) for d in dims]):
        v = [1]
        for c, xi in zip(cores, x):
            v = [sum(v[l] * c[l][xi][r] for l in range(len(v))) % p for r in range(len(c[0][0]))]
        A[x] = v[0] % p
    return A, dims


def random_tt(dims, bonds, p, rng):
    b = [1] + bonds + [1]
    return [[[[rng.randrange(p) for _ in range(b[i + 1])] for _ in range(dims[i])]
             for _ in range(b[i])] for i in range(len(dims))]


def random_invertible(n, p, rng):
    while True:
        m = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
        if rank(m, p) == n:
            return m


def regauge(cores, p, rng):
    out = [c for c in cores]
    for i in range(len(cores) - 1):
        b = len(cores[i][0][0])
        M = random_invertible(b, p, rng)
        Mi = inverse(M, p)
        out[i] = [[[sum(out[i][l][j][k] * M[k][r] for k in range(b)) % p for r in range(b)]
                   for j in range(len(out[i][0]))] for l in range(len(out[i]))]
        out[i + 1] = [[[sum(Mi[l][k] * out[i + 1][k][j][r] for k in range(b)) % p
                        for r in range(len(out[i + 1][0][0]))] for j in range(len(out[i + 1][0]))]
                      for l in range(b)]
    return out


def add_dead_bond(cores, p, rng, site=0):
    """Append a bond direction at the right of `site` that the suffix kills."""
    c, nxt = cores[site], cores[site + 1]
    c2 = [[row + [rng.randrange(p)] for row in mat] for mat in c]
    n2 = [mat for mat in nxt] + [[[0] * len(nxt[0][0]) for _ in range(len(nxt[0]))]]
    out = list(cores)
    out[site], out[site + 1] = c2, n2
    return out


def prefix_space(A, dims, i, p):
    """Column space of the flattening P_i x Q_i, as an RREF row basis in P_i coordinates."""
    pre = list(product(*[range(d) for d in dims[:i]]))
    suf = list(product(*[range(d) for d in dims[i:]]))
    cols = [[A[a + s] for a in pre] for s in suf]
    return rref(cols, p)[0] if any(any(c) for c in cols) else []


# ---------- canonical echelon gauge (local, no full tensor) ----------

def canonical_tt(cores, p):
    N = len(cores)
    b = [len(c) for c in cores] + [1]
    d = [len(c[0]) for c in cores]
    def gmul(c, j, s):
        return [sum(c[l][j][r] * s[r] for r in range(len(s))) % p for l in range(len(c))]
    S = [None] * (N + 1)
    S[N] = [[1]]
    for i in range(N, 0, -1):
        vecs = [gmul(cores[i - 1], j, s) for s in S[i] for j in range(d[i - 1])]
        S[i - 1] = rref(vecs, p)[0] if any(any(v) for v in vecs) else []
    if not S[0]:
        return "ZERO"
    C = [[1]]  # coordinate map on S_0
    out = []
    for i in range(1, N + 1):
        c = cores[i - 1]
        def phi(s):
            w = []
            for k in range(len(C)):
                for j in range(d[i - 1]):
                    t = gmul(c, j, s)
                    w.append(sum(C[k][l] * t[l] for l in range(len(t))) % p)
            return w
        if i == N:
            w = phi([1])
            out.append([[[w[k * d[i - 1] + j]] for j in range(d[i - 1])] for k in range(len(C))])
            break
        imgs = [phi(s) for s in S[i]]
        basis, piv = rref(imgs, p)
        r_prev = len(C)
        out.append([[[basis[q][k * d[i - 1] + j] for q in range(len(basis))]
                     for j in range(d[i - 1])] for k in range(r_prev)])
        # C_i: row q is the pivot-coordinate functional of phi, as a matrix on F^{b_i}
        Phi_cols = [phi([int(r == t) for r in range(b[i])]) for t in range(b[i])]
        C = [[Phi_cols[t][pc] for t in range(b[i])] for pc in piv]
    return out


# ---------- group actions ----------

def apply_group(g, A, dims, p):
    out = {}
    for y in A:
        v = 0
        for x, a in A.items():
            if a:
                prod_ = a
                for k in range(len(dims)):
                    prod_ = prod_ * g[k][y[k]][x[k]] % p
                    if not prod_:
                        break
                v += prod_
        out[y] = v % p
    return out


def kron_all(mats, p):
    M = [[1]]
    for m in mats:
        M = kron(M, m, p)
    return M


def preserves(Mat, basis_rows, p):
    """Does the matrix Mat (acting on columns) preserve span(basis_rows)?"""
    if not basis_rows:
        return True
    imgs = [[sum(Mat[r][c] * v[c] for c in range(len(v))) % p for r in range(len(Mat))] for v in basis_rows]
    return rank(basis_rows + imgs, p) == len(basis_rows)


def staged_check(name, cores, group, p):
    A, dims = contract(cores, p)
    N = len(dims)
    U = [None] + [prefix_space(A, dims, i, p) for i in range(1, N + 1)]
    # U_i <= U_{i-1} tensor V_i, with E_i coordinates; local actions R_i
    basis_prev = [[1]]
    E = []
    for i in range(1, N + 1):
        prod_basis = [[a * int(j == jj) for a in u for jj in range(dims[i - 1])] for u in basis_prev for j in range(dims[i - 1])]
        # NB: P_i index = (prefix, x_i) with x_i fastest, matching product() order
        Ei = [coords(prod_basis, u, p) for u in U[i]]
        assert all(e is not None for e in Ei), "U_i not inside U_{i-1} (x) V_i"
        E.append(Ei)
        basis_prev = U[i]
    H = {tuple(map(lambda m: tuple(map(tuple, m)), g)) for g in group if apply_group(g, A, dims, p) == A}
    K = list(group)
    Kloc = list(group)
    for i in range(1, N + 1):
        K = [g for g in K if preserves(kron_all(g[:i], p), U[i], p)]
        def local_ok(g):
            # R_{i-1}(g): coordinates of g_P(U_{i-1} basis) in U_{i-1} basis
            if i == 1:
                R = [[1]]
            else:
                gP = kron_all(g[:i - 1], p)
                cols = [coords(U[i - 1], [sum(gP[r][c] * u[c] for c in range(len(u))) % p
                                          for r in range(len(gP))], p) for u in U[i - 1]]
                R =[[cols[c][r] for c in range(len(cols))] for r in range(len(cols))]
            return preserves(kron(R, g[i - 1], p), E[i - 1], p)
        Kloc = [g for g in Kloc if local_ok(g)]
    Kset = {tuple(map(lambda m: tuple(map(tuple, m)), g)) for g in K}
    Klocset = {tuple(map(lambda m: tuple(map(tuple, m)), g)) for g in Kloc}
    print(f"{name}: |Gamma|={len(group)} prefix ranks={[len(u) for u in U[1:]]} |H|={len(H)} "
          f"|K_N global|={len(Kset)} |K_N local|={len(Klocset)} K_N==H: {Kset == H == Klocset}")
    return Kset == H == Klocset, H


def product_group(local_groups):
    return [list(g) for g in product(*local_groups)]


if __name__ == "__main__":
    rng = random.Random(2026)
    allok = True
    print("== 1. Gram falsifier over F_5")
    p = 5
    M = [[1, 2], [2, 4]]
    MMt = matmul(M, [list(r) for r in zip(*M)], p)
    print("M=[[1,2],[2,4]]: rank(M) =", rank(M, p), " M M^T =", MMt, " rank(M M^T) =", rank(MMt, p) if any(any(r) for r in MMt) else 0)
    print("(1,2).(1,2) mod 5 =", (1 + 4) % 5)

    print("\n== 2/3. Gauge invariance of U_i and a canonical echelon gauge (local sweep)")
    for (p, dims, bonds) in [(3, [2, 2, 2, 2], [2, 3, 2]), (5, [2, 3, 2], [2, 2]), (2, [2, 2, 2, 2], [2, 2, 2]), (7, [3, 3, 3], [2, 2])]:
        cores = random_tt(dims, bonds, p, rng)
        g1 = regauge(cores, p, rng)
        g2 = add_dead_bond(regauge(cores, p, rng), p, rng, site=1)
        A, _ = contract(cores, p)
        same_tensor = all(contract(c, p)[0] == A for c in (g1, g2))
        same_U = all(prefix_space(contract(c, p)[0], dims, i, p) == prefix_space(A, dims, i, p)
                     for c in (g1, g2) for i in range(1, len(dims)))
        can = [canonical_tt(c, p) for c in (cores, g1, g2)]
        identical = can[0] == can[1] == can[2]
        if can[0] == "ZERO":
            reproduces, bonds_can = not any(A.values()), "zero tensor"
        else:
            reproduces = contract(can[0], p)[0] == A
            bonds_can = [len(c[0][0]) for c in can[0][:-1]]
        print(f"p={p} dims={dims} bonds={bonds}: tensors equal={same_tensor} U_i equal={same_U} "
              f"canonical cores identical={identical} canonical reproduces A={reproduces} canonical bonds={bonds_can}")
        allok &= same_tensor and same_U and identical and reproduces

    print("\n== 4. Staged subspace stabilizers vs exhaustive H")
    p = 3
    ut3 = list(ut_group(3, p))
    ut2 = list(ut_group(2, p))
    cases = [
        ("UT3(F3)^2, d=3, bond 2", random_tt([3, 3], [2], p, rng), product_group([ut3, ut3])),
        ("UT3(F3)^2, d=3, bond 1 (e2 x e2)", [[[[0], [0], [1]]], [[[0], [0], [1]]]], product_group([ut3, ut3])),
        ("UT2(F3)^3, d=2, bonds 2,2", random_tt([2, 2, 2], [2, 2], p, rng), product_group([ut2, ut2, ut2])),
    ]
    # correlated (diagonal) action: g -> (g, g) for g in UT3(F3)
    corr = [[g, g] for g in ut3]
    A_sym = [[[[1, 0, 0], [0, 1, 0], [0, 0, 1]]], [[[1], [0], [0]], [[0], [1], [0]], [[0], [0], [1]]]]
    cases.append(("diagonal UT3(F3) on identity TT sum e_k x e_k", A_sym, corr))
    cases.append(("diagonal UT3(F3), random bond 2", random_tt([3, 3], [2], p, rng), corr))
    for name, cores, group in cases:
        ok, _ = staged_check(name, cores, group, p)
        allok &= ok

    print("\n== 5. p-group premise: scalar 2 on site 1 over F_5 (order 4, not a 5-group)")
    p = 5
    cores = random_tt([2, 2], [2], p, rng)
    A, dims = contract(cores, p)
    g = [[[2, 0], [0, 2]], identity(2)]
    U = [prefix_space(A, dims, i, p) for i in (1, 2)]
    keeps = all(preserves(kron_all(g[:i], p), U[i - 1], p) for i in (1, 2))
    print("preserves every U_i:", keeps, " fixes A:", apply_group(g, A, dims, p) == A)

    print("\n== 6. Repo solver (read-only import) vs exhaustive reference")
    sys.path.insert(0, REPO)
    sys.dont_write_bytecode = True
    from theorems.tensor_train_pgroup_stabilizer import recover_tensor_train_stabilizer as solve
    p = 5
    ut3_5 = list(ut_group(3, p))
    cores = random_tt([3, 3], [2], p, rng)
    gens_local = [[[1, 1, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 1], [0, 0, 1]]]
    gens = [tuple(tuple(map(tuple, m)) for m in (gl, identity(3))) for gl in gens_local] + \
           [tuple(tuple(map(tuple, m)) for m in (identity(3), gl)) for gl in gens_local]
    tcores = tuple(tuple(tuple(tuple(r) for r in mat) for mat in c) for c in cores)
    res = solve(p, tcores, tuple(gens))
    ok, H = staged_check("UT3(F5)^2, d=3, bond 2 (reference)", cores, product_group([ut3_5, ut3_5]), p)
    allok &= ok
    if res["generators"] is not None:
        # close the returned generators under multiplication
        def key(g):
            return tuple(tuple(map(tuple, m)) for m in g)
        start = key([identity(3), identity(3)])
        seen = {start}
        frontier = [start]
        gl = [key(g) for g in res["generators"]]
        while frontier:
            new = []
            for h in frontier:
                for s in gl:
                    prod_ = key([matmul([list(r) for r in s[k]], [list(r) for r in h[k]], p) for k in range(2)])
                    if prod_ not in seen:
                        seen.add(prod_)
                        new.append(prod_)
            frontier = new
        print(f"repo solver status={res['status']} generated |H|={len(seen)} equals exhaustive H: {seen == H}")
        allok &= seen == H
    else:
        print("repo solver status:", res["status"])
    jordan = ((1, 1, 0), (0, 1, 1), (0, 0, 1))
    I3 = tuple(tuple(r) for r in identity(3))
    idtt = ((I3,), tuple(tuple((x,) for x in row) for row in I3))
    res3 = solve(3, idtt, ((jordan, I3), (I3, jordan)))
    print("note's p=3 control (Jordan block, site index 3 <= p): status", res3["status"],
          "failed stage", res3.get("failed_stage"),
          "stage indices", [c["common_nilpotency_index"] for c in res3["stage_certificates"]])
    print("ALL_PASS" if allok else "FAILURE")
