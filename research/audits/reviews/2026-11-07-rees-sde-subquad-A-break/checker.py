"""Independent checker (pure python ints, no numpy, no code shared with algt.py or subquad.py).

check_leaf verifies, directly from the definitions in subquad-A section 1 / Q1 section 1:
  rounds: disjoint supports, delta nonzero on the support, blocks partition the support,
  every block inside one class; (F1) block sums W_{l,b}, b>=1, independent mod U_{l-1};
  (F2) e_l in U_{l-1}; Src nonempty, outside every support, span(Src) in U_L;
  (S) for every cross-class pair (j,b,b') the functional
      phi = (coord_b - coord_b') o (Omega_j-coordinates) o Pi_j     (coord_0 = 0)
  is nonzero on span(Src) + span(e_l : l > j);
  block counts: <= E = 3J-2 per round; lower rounds <= J + c, top rounds <= J - 1;
  rho <= E * dim(U_L) / 2.
check_witness verifies x in (P u {0})^M, x != 0, sum x_i lambda_i = 0.
"""


def _red(rows, v, p):
    """rows: dict pivot -> normalized row (RREF).  Returns reduced v."""
    v = [x % p for x in v]
    for j, row in rows.items():
        f = v[j]
        if f:
            v = [(x - f * y) % p for x, y in zip(v, row)]
    return v


def _add(rows, v, p):
    v = _red(rows, v, p)
    j = next((i for i, x in enumerate(v) if x), None)
    if j is None:
        return False
    inv = pow(v[j], p - 2, p)
    v = [x * inv % p for x in v]
    for k in list(rows):
        f = rows[k][j]
        if f:
            rows[k] = [(x - f * y) % p for x, y in zip(rows[k], v)]
    rows[j] = v
    return True


def rank(vecs, p):
    rows = {}
    n = 0
    for v in vecs:
        n += _add(rows, list(v), p)
    return n


def in_span(vecs, v, p):
    rows = {}
    for w in vecs:
        _add(rows, list(w), p)
    return not any(_red(rows, list(v), p))


def coords_in_basis(basis, vecs, p):
    """Coordinates of each v in vecs w.r.t. the independent list basis (None if outside)."""
    n = len(basis)
    if n == 0:
        return [None if any(x % p for x in v) else [] for v in vecs]
    a = len(basis[0])
    # Solve by Gaussian elimination on the augmented matrix [basis^T | v^T].
    # Build matrix A (a x n) with columns = basis vectors.
    out = []
    # precompute an elimination of A with recorded row ops
    A = [[basis[j][i] % p for j in range(n)] for i in range(a)]
    ops = []           # list of row-op records to replay on each rhs
    piv_rows = []
    row = 0
    for col in range(n):
        pr = next((i for i in range(row, a) if A[i][col]), None)
        if pr is None:
            raise ValueError("basis dependent")
        A[row], A[pr] = A[pr], A[row]
        ops.append(("swap", row, pr))
        inv = pow(A[row][col], p - 2, p)
        A[row] = [x * inv % p for x in A[row]]
        ops.append(("scale", row, inv))
        for i in range(a):
            if i != row and A[i][col]:
                f = A[i][col]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[row])]
                ops.append(("sub", i, row, f))
        piv_rows.append(row)
        row += 1
    for v in vecs:
        b = [x % p for x in v]
        for op in ops:
            if op[0] == "swap":
                _, i, j = op
                b[i], b[j] = b[j], b[i]
            elif op[0] == "scale":
                _, i, s = op
                b[i] = b[i] * s % p
            else:
                _, i, j, f = op
                b[i] = (b[i] - f * b[j]) % p
        if any(b[n:]):
            out.append(None)
        else:
            out.append(b[:n])
    return out


def kclass(y, p, k):
    """Return y^((p-1)/k), a k-th root of unity identifying the class of y != 0."""
    return pow(y % p, (p - 1) // k, p)


def check_witness(bank, p, k, x):
    """x: dict index -> value.  Returns list of problems (empty = valid)."""
    probs = []
    if not any(v % p for v in x.values()):
        probs.append("zero witness")
    for i, v in x.items():
        v %= p
        if v and pow(v, (p - 1) // k, p) != 1:
            probs.append("x_%d not in P u {0}" % i)
    a = len(bank[0])
    s = [0] * a
    for i, v in x.items():
        for t in range(a):
            s[t] = (s[t] + v * bank[i][t]) % p
    if any(s):
        probs.append("sum x_i lambda_i != 0")
    return probs


def check_leaf(bank, p, k, J, leaf, c=None):
    """Returns (problems, info)."""
    E = 3 * J - 2
    c = 2 * (J - 1) if c is None else c
    probs = []
    rounds = leaf["rounds"]
    src = list(leaf["src"])
    a = len(bank[0])
    seen = set()
    for l, rnd in enumerate(rounds):
        S = list(rnd["S"])
        d = rnd["delta"]
        if len(S) < 2:
            probs.append("round %d support < 2" % l)
        if len(set(S)) != len(S) or set(S) & seen:
            probs.append("round %d support not disjoint" % l)
        seen |= set(S)
        if any(d[i] % p == 0 for i in S) or set(d) != set(S):
            probs.append("round %d delta not nonzero exactly on S" % l)
        bl = rnd["blocks"]
        flat = [i for G in bl for i in G]
        if sorted(flat) != sorted(S) or any(len(G) == 0 for G in bl):
            probs.append("round %d blocks do not partition S" % l)
        for G in bl:
            if len({kclass(d[i], p, k) for i in G}) != 1:
                probs.append("round %d block not inside a class" % l)
        n = len(bl)
        if n > E:
            probs.append("round %d has %d > E blocks" % (l, n))
        if rnd.get("kind") == "top":
            if n > J - 1:
                probs.append("top round %d has %d > J-1 blocks" % (l, n))
            if any(len(G) != 1 for G in bl):
                probs.append("top round %d not singleton-blocked" % l)
        else:
            if n > J + c:
                probs.append("lower round %d has %d > J+c blocks" % (l, n))
    if not src:
        probs.append("Src empty")
    if set(src) & seen:
        probs.append("Src meets a round")
    # flag
    rows = {}
    Wall, slots, es = [], [], []
    for l, rnd in enumerate(rounds):
        d = rnd["delta"]
        Ws = []
        for G in rnd["blocks"]:
            w = [0] * a
            for i in G:
                for t in range(a):
                    w[t] = (w[t] + d[i] * bank[i][t]) % p
            Ws.append(w)
        e = [sum(w[t] for w in Ws) % p for t in range(a)]
        # e also equals Lambda delta
        e2 = [sum(d[i] * bank[i][t] for i in rnd["S"]) % p for t in range(a)]
        if e != e2:
            probs.append("round %d e mismatch" % l)
        if any(_red(rows, e, p)):
            probs.append("(F2) fails at round %d" % l)
        sl = []
        for w in Ws[1:]:
            if not _add(rows, w, p):
                probs.append("(F1) fails at round %d" % l)
            sl.append(len(Wall))
            Wall.append(w)
        slots.append(sl)
        es.append(e)
    dimU = len(rows)
    for s in src:
        if any(_red(rows, bank[s], p)):
            probs.append("Src column %d outside U_L" % s)
            break
    info = dict(dimU=dimU, nrounds=len(rounds), maxblocks=max([len(r["blocks"]) for r in rounds],
                                                               default=0))
    if probs:
        return probs, info
    # (S)
    cs = coords_in_basis(Wall, [bank[s] for s in src] + es, p)
    sc, ec = cs[:len(src)], cs[len(src):]
    rho, bad = 0, 0
    for j, rnd in enumerate(rounds):
        d = rnd["delta"]
        cl = [kclass(d[G[0]], p, k) for G in rnd["blocks"]]
        for b in range(len(cl)):
            for b2 in range(b + 1, len(cl)):
                if cl[b] == cl[b2]:
                    continue
                rho += 1

                def phi(v):
                    x = v[slots[j][b - 1]] if b >= 1 else 0
                    y = v[slots[j][b2 - 1]] if b2 >= 1 else 0
                    return (x - y) % p
                ok = any(phi(v) for v in sc) or any(phi(ec[l]) for l in range(j + 1, len(rounds)))
                if not ok:
                    bad += 1
    if bad:
        probs.append("(S) fails for %d cross pairs" % bad)
    if 2 * rho > E * dimU:
        probs.append("rho > E dim/2")
    info.update(rho=rho, bad=bad)
    return probs, info


def F_count(r, J, C=None):
    C = max(2, 2 * J - 4) if C is None else C
    if r == 0:
        return 0
    D = [0]
    for x in range(1, r + 1):
        D.append(max(kk + 1 + D[x - min(J - 1, kk)] for kk in range(1, x + 1)))
    return D[r] + C * r
