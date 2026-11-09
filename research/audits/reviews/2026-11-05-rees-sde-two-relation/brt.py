"""Block-refined triangular solver (BRT) for the diagonal SDE, with steering.

Problem: columns lambda_1..lambda_M in F_p^a, kappa | p-1, P = (F_p^*)^kappa,
Sq = P U {0}.  Find x in Sq^M, x != 0, with sum x_i lambda_i = 0.

Rounds (forward pass, deterministic linear algebra):
  U_0 = 0.  Round l takes q+1 fresh columns, q = a - dim U_{l-1}, and a
  dependency delta with e_l = sum delta_i lambda_i in U_{l-1}.  If delta is
  monochromatic (one coset) it is a stop round.  Otherwise the support is
  split into E' = max(E, #classes) blocks (capped by the support size), each
  inside one class set of delta; W_b = sum_{i in G_b} delta_i lambda_i.
  The W_b (b != b_0) are added to the basis of U.  When U = F_p^a one more
  column is the top round (weight y in P).

Back substitution (randomised, Las Vegas):
  tau = -(top value).  For l = L..1 write tau = sum_b beta_b W_b + tau'
  (beta_{b_0} = 0, tau' in U_{l-1}), draw s uniformly from
  Good(beta) = {s : beta_b + s in Q_{-c_b} U {0} for all b}, put
  x_i = delta_i (beta_{b(i)} + s) on round l, and tau <- tau' - s e_l.
  Failure (Good empty) restarts the back substitution with fresh coins.

The steering forms of (ND') are computed by `nd_report`.
"""
import random

from common import F, inv, rank, check_witness


# ----------------------------------------------------------------- linear algebra mod p

def solve_basis(B, v, p):
    """Coordinates c with sum c_j B[j] = v (B a list of independent vectors), or None."""
    n = len(B)
    a = len(v)
    # augmented matrix rows = coordinates, columns = basis vectors + rhs
    A = [[B[j][i] % p for j in range(n)] + [v[i] % p] for i in range(a)]
    piv_cols, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, a) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = inv(A[r][c], p)
        A[r] = [(x * iv) % p for x in A[r]]
        for i in range(a):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(xi - f * xr) % p for xi, xr in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
    for i in range(r, a):
        if A[i][n]:
            return None
    coords = [0] * n
    for i, c in enumerate(piv_cols):
        coords[c] = A[i][n]
    return coords


def kernel_vectors(vecs, p):
    """Basis of {z : sum z_j vecs[j] = 0}."""
    from common import kernel
    return kernel(vecs, p) if vecs else []


# ----------------------------------------------------------------- the solver

class Round:
    pass


def forward(Fd, cols, E, rng, split="random"):
    """Build the rounds.  Returns (rounds, basis, top, used, status)."""
    p, k = Fd.p, Fd.k
    a = len(cols[0])
    basis = []           # global basis of U, in round order
    rounds = []
    ptr = 0
    while True:
        q = a - len(basis)
        if q == 0:
            if ptr >= len(cols):
                return rounds, basis, None, ptr, "budget"
            top = Round()
            top.kind = "top"
            top.idx = [ptr]
            top.vec = cols[ptr]
            ptr += 1
            return rounds, basis, top, ptr, "ok"
        if ptr + q + 1 > len(cols):
            return rounds, basis, None, ptr, "budget"
        idx = list(range(ptr, ptr + q + 1))
        ptr += q + 1
        vecs = [cols[i] for i in idx] + basis
        K = kernel_vectors(vecs, p)
        Kd = [z[:q + 1] for z in K if any(z[:q + 1])]
        # generic combination of the delta-parts (maximal support)
        best = None
        for _ in range(8):
            coef = [rng.randrange(1, p) for _ in Kd]
            d = [sum(c * z[t] for c, z in zip(coef, Kd)) % p for t in range(q + 1)]
            if best is None or sum(1 for x in d if x) > sum(1 for x in best if x):
                best = d
        delta = best
        # normalise: first nonzero entry = 1
        nz = next(x for x in delta if x)
        iv = inv(nz, p)
        delta = [(x * iv) % p for x in delta]
        e = [sum(delta[t] * cols[idx[t]][j] for t in range(q + 1)) % p for j in range(a)]
        sup = [t for t in range(q + 1) if delta[t]]
        cls = {t: Fd.cls(delta[t]) for t in sup}
        R = Round()
        R.idx, R.delta, R.e, R.sup, R.cls = idx, delta, e, sup, cls
        if len(set(cls.values())) == 1:
            R.kind = "stop"
            rounds.append(R)
            return rounds, basis, None, ptr, "stop"
        # blocks: one per class, then split the largest until E' blocks
        byc = {}
        for t in sup:
            byc.setdefault(cls[t], []).append(t)
        blocks = [byc[c] for c in sorted(byc)]
        target = min(max(E, len(blocks)), len(sup))
        while len(blocks) < target:
            j = max(range(len(blocks)), key=lambda b: len(blocks[b]))
            G = blocks[j]
            if split == "random":
                G = G[:]
                rng.shuffle(G)
            h = len(G) // 2
            blocks[j:j + 1] = [sorted(G[:h]), sorted(G[h:])]
        W = []
        for G in blocks:
            W.append([sum(delta[t] * cols[idx[t]][j] for t in G) % p for j in range(a)])
        # add W_b (b >= 1) that are independent of the current basis
        added = []
        for b in range(1, len(blocks)):
            if rank(basis + [W[b]], p) > len(basis):
                basis.append(W[b])
                added.append(b)
        R.kind = "level"
        R.blocks, R.W, R.added = blocks, W, added
        R.bclass = [cls[G[0]] for G in blocks]
        R.basis_pos = list(range(len(basis) - len(added), len(basis)))
        rounds.append(R)


def good_set(Fd, beta, bclass, rng, exhaustive_limit=20000, trials=4000):
    p, k = Fd.p, Fd.k

    def ok(s):
        for b, c in zip(beta, bclass):
            y = (b + s) % p
            if y and Fd.cls(y) != (-c) % k:
                return False
        return True

    if p <= exhaustive_limit:
        G = [s for s in range(p) if ok(s)]
        return G
    out = []
    for _ in range(trials):
        s = rng.randrange(p)
        if ok(s):
            out.append(s)
            if len(out) >= 1:
                break
    return out


def backward(Fd, cols, rounds, basis, top, rng):
    """One randomised back substitution.  Returns x or None."""
    p, k = Fd.p, Fd.k
    M, a = len(cols), len(cols[0])
    x = [0] * M
    levels = [R for R in rounds if R.kind == "level"]
    if top is not None:
        y = rng.choice(Fd.P)
        x[top.idx[0]] = y
        tau = [(-y * v) % p for v in top.vec]
    else:
        R = rounds[-1]
        assert R.kind == "stop"
        c0 = next(iter(R.cls.values()))
        zeta = (Fd.rep((-c0) % k) * rng.choice(Fd.P)) % p
        for t in R.sup:
            x[R.idx[t]] = (zeta * R.delta[t]) % p
        tau = [(-zeta * v) % p for v in R.e]
    for R in reversed(levels):
        coords = solve_basis(basis, tau, p)
        if coords is None:
            return None, "not-in-U"
        beta = [0] * len(R.blocks)
        for b, pos in zip(R.added, R.basis_pos):
            beta[b] = coords[pos]
        # tau' = tau - sum beta_b W_b
        taup = [(tau[j] - sum(beta[b] * R.W[b][j] for b in range(len(R.blocks)))) % p for j in range(a)]
        G = good_set(Fd, beta, R.bclass, rng)
        if not G:
            return None, "good-empty"
        s = rng.choice(G)
        for b, blk in enumerate(R.blocks):
            for t in blk:
                x[R.idx[t]] = (R.delta[t] * (beta[b] + s)) % p
        tau = [(taup[j] - s * R.e[j]) % p for j in range(a)]
    if any(tau):
        return None, "residual"
    return x, "ok"


def reduce_rank(cols, p):
    """Coordinates of the columns in a basis of their span (rank r <= a)."""
    from common import rref
    a = len(cols[0])
    Rr, piv = rref([list(c) for c in cols], p)   # row space of the column vectors
    r = len(piv)
    if r == a:
        return cols, a
    B = Rr  # r basis vectors (rows), reduced
    out = []
    for c in cols:
        # coordinates w.r.t. reduced basis: read off pivot entries
        out.append([c[j] % p for j in piv])
    return out, r


def solve(Fd, cols, E, rng, restarts=50, split="random", reduce=True):
    if reduce:
        cols2, r = reduce_rank(cols, Fd.p)
        if r == 0:
            x = [0] * len(cols)
            x[0] = 1
            return x, dict(status="ok", used=1, restarts=0, rounds=0)
        cols = cols2
    rounds, basis, top, used, status = forward(Fd, cols, E, rng, split)
    if status == "budget":
        return None, dict(status="budget", used=used)
    for r in range(restarts):
        x, st = backward(Fd, cols, rounds, basis, top, rng)
        if x is not None:
            assert check_witness(Fd, cols, x), "invalid witness"
            return x, dict(status="ok", used=used, restarts=r, rounds=len(rounds))
    return None, dict(status="fail:" + st, used=used, rounds=len(rounds))


def nd_report(Fd, cols, rounds, basis, top):
    """(ND'): for every level j and cross-class block pair (b, b'), is some steering
    coefficient nonzero?  Steering vectors: e_l for later levels l (and the stop
    round), and the top column.  Returns list of failing (level, b, b')."""
    p = Fd.p
    levels = [R for R in rounds if R.kind == "level"]
    steer = []  # vectors whose projections steer level j: e of later rounds, top
    fails = []
    later = [R.e for R in rounds]  # e_l for every round (index-aligned with rounds)
    for jdx, R in enumerate(levels):
        ridx = rounds.index(R)
        vecs = [rounds[l].e for l in range(ridx + 1, len(rounds))]
        if top is not None:
            vecs.append(top.vec)
        coordss = [solve_basis(basis, v, p) for v in vecs]
        for b in range(len(R.blocks)):
            for bp in range(b + 1, len(R.blocks)):
                if R.bclass[b] == R.bclass[bp]:
                    continue
                nonzero = False
                for co in coordss:
                    if co is None:
                        continue
                    beta = [0] * len(R.blocks)
                    for bb, pos in zip(R.added, R.basis_pos):
                        beta[bb] = co[pos]
                    if (beta[b] - beta[bp]) % p:
                        nonzero = True
                        break
                if not nonzero:
                    fails.append((jdx, b, bp))
    return fails


def arity(a, E):
    """M_E(a): columns used when every round has a full-support circuit and
    min(E, q+1) blocks (no early stop)."""
    q, M = a, 0
    while q >= 1:
        M += q + 1
        q -= min(E - 1, q)
    return M + 1


if __name__ == "__main__":
    import sys
    for E in (2, 3, 4, 5):
        print(E, [arity(a, E) for a in range(1, 13)])
