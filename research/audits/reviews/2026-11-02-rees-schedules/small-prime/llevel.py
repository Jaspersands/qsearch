"""L-level collision tensor with a universal contraction: verifier, solver, SAT search.

Objects.  A level-l object is a family of cell vectors T_I in F_p^r,
I in Z_k^l, with pairwise disjoint column supports, nonzero root weights,
nonempty cell 0, and every axis fibre in W = ker z^T (so T in W^{(x)l} (x) F^r).
A level-0 object is one input column with root weight 1.  Level l+1 takes
(k-1)^l r + 1 level-l objects, finds a linear dependence of their interior
cells (all indices >= 1; the projection W^{(x)l} -> F^{(k-1)^l} is injective
because z_0 != 0), normalises one nonzero coefficient to 1, writes each
coefficient as z_i b^k and appends axis index i.  Arity
M_L = prod_{l<L} ((k-1)^l r + 1).

Contraction.  C in P^{Z_k^L} (P = k-th powers with 0), C_0 != 0, with
<C, w_1 (x) ... (x) w_L> = 0 for all w_t in W.  Then sum_I C_I T_I = 0 and
s_col = C_I^{1/k} * root_col is a nonzero witness of sum s^k v = 0.

Border form.  With u_m = z_m / z_0 and basis e_m - u_m e_0 of W, the
annihilator condition says every interior entry is forced:
C_m = sum_{0 != S subset [L]} (-1)^{|S|+1} prod_{t in S} u_{m_t} C_{m with S -> 0}.

Usage:
  python llevel.py sat p k L       # SAT search for a contraction (pycosat)
  python llevel.py solve p k L r N  # find a contraction, run N random instances
"""
import sys
import itertools
import random
from sympy import primitive_root


class Field:
    def __init__(self, p, k):
        assert (p - 1) % k == 0
        self.p, self.k, self.h = p, k, (p - 1) // k
        self.g = primitive_root(p)
        self.z = [pow(self.g, i, p) for i in range(k)]          # z_i in Q_i, z_0 = 1
        self.root = {}
        for y in range(1, p):
            self.root.setdefault(pow(y, k, p), y)                 # k-th root table
        self.P = sorted([0] + list(self.root.keys()))
        self.Pset = set(self.P)
        w = pow(self.g, self.h, p)
        self.ind = {}
        for y in range(1, p):
            self.ind[y] = [pow(w, m, p) for m in range(k)].index(pow(y, self.h, p))

    def inP(self, y):
        return y % self.p in self.Pset


def interior_formula(F, L):
    """For each interior m, list of (coef, border index) with C_m = sum coef*C_b."""
    p, k = F.p, F.k
    u = [F.z[m] * pow(F.z[0], -1, p) % p for m in range(k)]
    out = {}
    for m in itertools.product(range(1, k), repeat=L):
        terms = []
        for size in range(1, L + 1):
            for S in itertools.combinations(range(L), size):
                c = 1 if size % 2 == 1 else p - 1
                for t in S:
                    c = c * u[m[t]] % p
                b = tuple(0 if t in S else m[t] for t in range(L))
                terms.append((c, b))
        out[m] = terms
    return out


def verify_contraction(F, L, C):
    p, k = F.p, F.k
    if C[(0,) * L] % p == 0:
        return False
    if not all(F.inP(v) for v in C.values()):
        return False
    u = [F.z[m] * pow(F.z[0], -1, p) % p for m in range(k)]
    # pair with every basis tensor of W^{(x)L} directly
    for m in itertools.product(range(1, k), repeat=L):
        s = 0
        for I in itertools.product(range(k), repeat=L):
            coef = 1
            for t in range(L):
                if I[t] == m[t]:
                    pass
                elif I[t] == 0:
                    coef = coef * (p - u[m[t]]) % p
                else:
                    coef = 0
                    break
            if coef:
                s += coef * C[I]
        if s % p:
            return False
    return True


def sat_search(F, L, timeout_note=""):
    """Find C (or prove none) by SAT.  One-hot border values in P; chained
    one-hot partial sums for each interior entry; interior value in P."""
    import pycosat
    p, k = F.p, F.k
    form = interior_formula(F, L)
    border = [I for I in itertools.product(range(k), repeat=L) if 0 in I]
    nv = [0]

    def new():
        nv[0] += 1
        return nv[0]

    clauses = []
    bvar = {}
    for I in border:
        vals = [1] if I == (0,) * L else F.P            # C_0 = 1 WLOG (H-scaling)
        vs = {v: new() for v in vals}
        bvar[I] = vs
        clauses.append(list(vs.values()))
        for a, b in itertools.combinations(vs.values(), 2):
            clauses.append([-a, -b])
    for m, terms in form.items():
        # partial sum after first term
        cur = {}
        c0, b0 = terms[0]
        for v, var in bvar[b0].items():
            cur.setdefault(c0 * v % p, []).append(var)
        # cur maps value -> list of vars implying it; make one-hot partial vars
        part = {val: new() for val in range(p)}
        for val, vs in cur.items():
            for var in vs:
                clauses.append([-var, part[val]])
        for val in range(p):
            if val not in cur:
                clauses.append([-part[val]])
        for a, b in itertools.combinations(part.values(), 2):
            clauses.append([-a, -b])
        for c, b in terms[1:]:
            nxt = {val: new() for val in range(p)}
            for val, pv in part.items():
                for v, var in bvar[b].items():
                    clauses.append([-pv, -var, nxt[(val + c * v) % p]])
            clauses.append(list(nxt.values()))
            for a2, b2 in itertools.combinations(nxt.values(), 2):
                clauses.append([-a2, -b2])
            part = nxt
        for val, pv in part.items():
            if not F.inP(val):
                clauses.append([-pv])
    sol = pycosat.solve(clauses)
    if sol == "UNSAT":
        return None, nv[0], len(clauses)
    sset = set(x for x in sol if x > 0)
    C = {}
    for I in border:
        C[I] = next(v for v, var in bvar[I].items() if var in sset)
    for m, terms in form.items():
        C[m] = sum(c * C[b] for c, b in terms) % p
    return C, nv[0], len(clauses)


def kernel_vector(rows, ncols, p):
    """Nonzero x with sum_j rows[i][j] x_j = 0 for all i (ncols > rank)."""
    A = [list(r) for r in rows]
    piv_cols, r = [], 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
    free = next(c for c in range(ncols) if c not in piv_cols)
    x = [0] * ncols
    x[free] = 1
    for i, c in enumerate(piv_cols):
        x[c] = (-A[i][free]) % p
    return x


def build(F, objs, level, r):
    """objs: list of level-`level` objects; object = dict I -> (vec, {col: root})."""
    p, k = F.p, F.k
    interior = list(itertools.product(range(1, k), repeat=level))
    need = (k - 1) ** level * r + 1
    assert len(objs) >= need
    objs = objs[:need]
    rows = []
    for I in interior:
        for coord in range(r):
            rows.append([o[I][0][coord] if I in o else 0 for o in objs])
    alpha = kernel_vector(rows, need, p)
    star = next(b for b, a in enumerate(alpha) if a)
    sc = pow(alpha[star], -1, p)
    alpha = [a * sc % p for a in alpha]
    new = {}
    for b, a in enumerate(alpha):
        if not a:
            continue
        i = F.ind[a]
        q = a * pow(F.z[i], -1, p) % p          # in H
        root = F.root[q]                          # root^k = q, a = z_i root^k
        for I, (vec, supp) in objs[b].items():
            J = I + (i,)
            if J not in new:
                new[J] = ([0] * r, {})
            vv, ss = new[J]
            qk = pow(root, k, p)
            for t in range(r):
                vv[t] = (vv[t] + qk * vec[t]) % p
            for col, rt in supp.items():
                ss[col] = rt * root % p
    assert (0,) * (level + 1) in new
    return new


def solve_instance(F, L, C, cols):
    r = len(cols[0])
    objs = [{(): (list(v), {j: 1})} for j, v in enumerate(cols)]
    for level in range(L):
        need = (F.k - 1) ** level * r + 1
        nxt = []
        while len(objs) >= need:
            nxt.append(build(F, objs[:need], level, r))
            objs = objs[need:]
        objs = nxt
    top = objs[0]
    s = [0] * len(cols)
    for I, (vec, supp) in top.items():
        cI = C[I]
        if cI == 0:
            continue
        rt = F.root[cI]
        for col, b in supp.items():
            s[col] = rt * b % F.p
    return s


def check_witness(F, cols, s):
    p, k = F.p, F.k
    r = len(cols[0])
    tot = [sum(pow(si, k, p) * v[t] for si, v in zip(s, cols)) % p for t in range(r)]
    return any(s) and not any(tot)


def arity(k, L, r):
    M = 1
    for l in range(L):
        M *= (k - 1) ** l * r + 1
    return M


def main():
    mode = sys.argv[1]
    p, k, L = map(int, sys.argv[2:5])
    F = Field(p, k)
    C, nv, nc = sat_search(F, L)
    print(f"sat p={p} k={k} L={L} vars={nv} clauses={nc} result={'SAT' if C else 'UNSAT'}", flush=True)
    if C:
        assert verify_contraction(F, L, C), "contraction failed direct check"
        print("  direct annihilator check passed; nonzero entries:",
              sum(1 for v in C.values() if v), "of", k ** L)
    if mode == "solve" and C:
        r, N = int(sys.argv[5]), int(sys.argv[6])
        M = arity(k, L, r)
        rnd = random.Random(1)
        ok = 0
        for trial in range(N):
            kind = trial % 3
            if kind == 0:
                cols = [[rnd.randrange(p) for _ in range(r)] for _ in range(M)]
            elif kind == 1:   # repeated basis columns (zero-sum adversary)
                cols = [[1 if t == j % r else 0 for t in range(r)] for j in range(M)]
            else:             # few distinct columns, scaled by random elements
                base = [[rnd.randrange(p) for _ in range(r)] for _ in range(2)]
                cols = [[rnd.randrange(1, p) * x % p for x in base[j % 2]] for j in range(M)]
            s = solve_instance(F, L, C, cols)
            ok += check_witness(F, cols, s)
        print(f"  solve r={r} M={M}: {ok}/{N} exact witnesses")


if __name__ == "__main__":
    main()
