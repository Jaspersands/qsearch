"""Zero-sum grade (kappa = p-1) of Rees Schedule 3: finders, reductions, exact checks.

Companion of research/audits/reviews/2026-11-04-rees-s3-zero-sum.md.
Pure Python integers only (no floats in any decision). A "bank" is a list of
label vectors, each a tuple of ints in [0, p).  A witness is a nonempty sorted
list T of indices with sum_{i in T} bank[i] = 0 in F_p^g.

Contents
  linear algebra mod p ..... rref_rows, kernel_vector, coords_in_basis
  exact searches ........... brute_force_zero_sum, reachable_sums_zero_sum
  finders .................. p3_two_level (deterministic, arity (g+1)^2, p = 3)
                             block_recursion (deterministic, arity prod_j (k_j(p-1)+1))
  reductions ............... zs_from_binsis (split bank + coordinates), binsis_from_zs
  two-level contraction .... contraction_at_zero_sum_grade (kappa = p-1, all C)
  Rees instances ........... filiform_sum_structure, lower_central_dims
"""

from itertools import product


# ---------------------------------------------------------------- linear algebra

def rref_rows(rows, p):
    """Reduced row echelon form of a list of rows over F_p. Returns (R, pivots)."""
    R = [list(r) for r in rows]
    nrows = len(R)
    ncols = len(R[0]) if nrows else 0
    pivots = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, nrows):
            if R[i][c] % p:
                piv = i
                break
        if piv is None:
            continue
        R[r], R[piv] = R[piv], R[r]
        inv = pow(R[r][c], p - 2, p)
        R[r] = [(x * inv) % p for x in R[r]]
        for i in range(nrows):
            if i != r and R[i][c] % p:
                f = R[i][c]
                R[i] = [(a - f * b) % p for a, b in zip(R[i], R[r])]
        pivots.append(c)
        r += 1
        if r == nrows:
            break
    return R[:r], pivots


def kernel_vector(cols, p):
    """A nonzero x with sum_i x_i cols[i] = 0 over F_p, or None if the columns are independent."""
    M = len(cols)
    if M == 0:
        return None
    g = len(cols[0])
    rows = [[cols[i][j] % p for i in range(M)] for j in range(g)]
    R, piv = rref_rows(rows, p) if g else ([], [])
    free = [c for c in range(M) if c not in piv]
    if not free:
        return None
    f = free[0]
    x = [0] * M
    x[f] = 1
    for r, pc in enumerate(piv):
        x[pc] = (-R[r][f]) % p
    return x


def vec_add(u, v, p):
    return tuple((a + b) % p for a, b in zip(u, v))


def subset_sum(bank, T, p):
    g = len(bank[0])
    s = (0,) * g
    for i in T:
        s = vec_add(s, bank[i], p)
    return s


def is_witness(bank, T, p):
    return len(T) > 0 and len(set(T)) == len(T) and all(0 <= i < len(bank) for i in T) \
        and not any(subset_sum(bank, T, p))


# ---------------------------------------------------------------- exact searches

def brute_force_zero_sum(bank, p):
    """Exhaustive search over the masks 1..2^M-1 (the reference oracle of the tests)."""
    M = len(bank)
    g = len(bank[0])
    sums = [(0,) * g] * (1 << M)
    for mask in range(1, 1 << M):
        low = mask & (-mask)
        i = low.bit_length() - 1
        sums[mask] = vec_add(sums[mask ^ low], bank[i], p)
        if not any(sums[mask]):
            return [j for j in range(M) if mask >> j & 1]
    return None


def reachable_sums_zero_sum(bank, p):
    """Lemma fc-zero-sum(c): reachable sums with one representative subset per value."""
    reach = {}  # value -> (prev_value or None, index)
    for j, lam in enumerate(bank):
        lam = tuple(x % p for x in lam)
        new = {}
        if lam not in reach:
            new[lam] = (None, j)
        for val in list(reach.keys()):
            w = vec_add(val, lam, p)
            if w not in reach and w not in new:
                new[w] = (val, j)
        reach.update(new)
        z = (0,) * len(lam)
        if z in reach:
            T = []
            v = z
            while v is not None:
                prev, idx = reach[v]
                T.append(idx)
                v = prev
            return sorted(T)
    return None


# ---------------------------------------------------------------- p = 3 two-level finder

def p3_two_level(bank, g):
    """Deterministic zero-sum finder over F_3 from any (g+1)^2 labels in F_3^g.

    Level 1: each of g+1 blocks of g+1 columns has a kernel vector w over F_3.
    With T1 = {w = 1}, T2 = {w = 2 = -1}: sum_{T1} = sum_{T2} =: u_b.
    If a class is empty or u_b = 0, a class is already a zero-sum subset.
    Then u_b has realizations of 0, 1*u_b (T1) and 2*u_b (T1 u T2): all of F_3.
    Level 2: a kernel vector c of [u_1 .. u_{g+1}] gives the zero-sum subset
    union_b R_b(c_b).  Returns a witness list of indices (never None when the
    arity holds).
    """
    p = 3
    n = g + 1
    assert len(bank) >= n * n, "arity (g+1)^2 required"
    blocks = []
    for b in range(n):
        idx = list(range(b * n, (b + 1) * n))
        w = kernel_vector([bank[i] for i in idx], p)
        assert w is not None  # g+1 vectors in F_3^g are dependent
        T1 = [idx[k] for k in range(n) if w[k] == 1]
        T2 = [idx[k] for k in range(n) if w[k] == 2]
        if not T1:
            return sorted(T2)          # 2*sum_{T2} = 0  =>  sum_{T2} = 0
        if not T2:
            return sorted(T1)
        u = subset_sum(bank, T1, p)
        if not any(u):
            return sorted(T1)
        blocks.append((u, T1, T2))
    c = kernel_vector([u for (u, _, _) in blocks], p)
    assert c is not None
    T = []
    for cb, (_, T1, T2) in zip(c, blocks):
        if cb == 1:
            T += T1
        elif cb == 2:
            T += T1 + T2
    return sorted(T)


# ---------------------------------------------------------------- block recursion (any p)

def block_sizes(g, k):
    """Split g coordinates into ceil(g/k) blocks of sizes floor/ceil."""
    L = max(1, -(-g // k))
    base, extra = divmod(g, L)
    return [base + (1 if j < extra else 0) for j in range(L)]


def block_recursion_arity(p, g, k):
    a = 1
    for kj in block_sizes(g, k):
        a *= kj * (p - 1) + 1
    return a


def block_recursion(bank, p, g, k):
    """Deterministic coordinate-block recursion.

    Level j kills the j-th block of k_j coordinates: consecutive groups of
    D_j = k_j(p-1)+1 current items each contain (Chevalley-Warning / Davenport
    constant of C_p^{k_j}) a nonempty subfamily whose sum vanishes on that block;
    reachable sums over the block projection find it in D_j * p^{k_j} steps.
    The merged item is the sum, with the disjoint union of supports.  Works for
    every bank of length >= prod_j D_j.  Returns a witness.
    """
    sizes = block_sizes(g, k)
    need = block_recursion_arity(p, g, k)
    assert len(bank) >= need
    items = [(tuple(x % p for x in bank[i]), [i]) for i in range(need)]
    start = 0
    for kj in sizes:
        coords = list(range(start, start + kj))
        D = kj * (p - 1) + 1
        new_items = []
        for gstart in range(0, len(items) - D + 1, D):
            group = items[gstart:gstart + D]
            proj = [tuple(v[c] for c in coords) for (v, _) in group]
            T = reachable_sums_zero_sum(proj, p)
            assert T is not None  # Davenport constant of C_p^{kj} is kj(p-1)+1
            v = (0,) * g
            sup = []
            for t in T:
                v = vec_add(v, group[t][0], p)
                sup += group[t][1]
            new_items.append((v, sup))
        items = new_items
        start += kj
    v, sup = items[0]
    assert not any(v)
    return sorted(sup)


# ---------------------------------------------------------------- reductions

def coords_in_basis(basis_rref, pivots, v, p):
    """Coordinates of v in the row space whose RREF is basis_rref (v must lie in it)."""
    x = [v[c] % p for c in pivots]
    # check membership
    recon = [0] * len(v)
    for coef, row in zip(x, basis_rref):
        recon = [(a + coef * b) % p for a, b in zip(recon, row)]
    if tuple(recon) != tuple(x_ % p for x_ in v):
        return None
    return tuple(x)


def zs_from_binsis(bank, p, t, binsis_solver):
    """Zero-sum finder for a bank uniform on an unknown subspace V, from a solver
    of average-case binary SIS on uniform matrices.

    The first t labels fix a basis of their span W (RREF, a public function of
    those labels only).  The other labels are written in W-coordinates; when
    W = V this is a uniform matrix independent of the first block, of size
    dim V x (M - t).  A solution x in {0,1}^{M-t} gives the witness t + supp(x).
    Returns (witness or None, matrix handed to the solver or None).
    """
    first, rest = bank[:t], bank[t:]
    if not rest:
        return None, None
    R, piv = rref_rows([list(v) for v in first], p)
    X = []
    for v in rest:
        x = coords_in_basis(R, piv, v, p)
        if x is None:          # label outside W: W != V (the event bounded in the note)
            return None, None
        X.append(x)
    if not piv:                # W = 0: every remaining label is 0
        return [t], []
    sol = binsis_solver(X, p)  # columns X[i] in F_p^{dim W}
    if sol is None:
        return None, X
    return sorted(t + i for i in sol), X


def binsis_from_zs(A_cols, p, zs_finder):
    """Binary SIS solution of a uniform matrix with columns A_cols, from a zero-sum
    finder (the columns are handed over as the bank, with V = F_p^n)."""
    T = zs_finder(A_cols, p)
    if T is None:
        return None
    x = [0] * len(A_cols)
    for i in T:
        x[i] = 1
    return x


# ---------------------------------------------------------------- two-level contraction at kappa = p-1

def primitive_root(p):
    for xi in range(2, p):
        if all(pow(xi, (p - 1) // q, p) != 1 for q in prime_factors(p - 1)):
            return xi
    return 1  # p = 2


def prime_factors(n):
    f, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            f.add(d)
            n //= d
        d += 1
    if n > 1:
        f.add(n)
    return f


def contraction_at_zero_sum_grade(p):
    """All two-level contractions at (p, kappa = p-1): matrices C in {0,1}^{k x k}
    with C_00 = 1 and sum C_ij X_ij = 0 for all X in W (x) W, W = z^perp,
    z_m = xi^m.  Since the annihilator of W (x) W is {z a^T + b z^T} and z_0 = 1,
    a member of it is determined by its first row and column:
        C_ij = z_i C_0j + z_j C_i0 - z_i z_j C_00.
    Enumerate first row and column in {0,1} and keep those with every entry in {0,1}.
    Returns the list of contractions (as tuples of rows)."""
    k = p - 1
    xi = primitive_root(p)
    z = [pow(xi, m, p) for m in range(k)]
    out = []
    for row in product((0, 1), repeat=k - 1):
        r = (1,) + row
        for col in product((0, 1), repeat=k - 1):
            cc = (1,) + col
            ok = True
            C = []
            for i in range(k):
                Ci = []
                for j in range(k):
                    v = (z[i] * r[j] + z[j] * cc[i] - z[i] * z[j]) % p
                    if v > 1:
                        ok = False
                        break
                    Ci.append(v)
                if not ok:
                    break
                C.append(tuple(Ci))
            if ok:
                out.append(tuple(C))
    return out


def contraction_bruteforce_direct(p):
    """Independent check for small p: every C in {0,1}^{k x k} with C_00 = 1, tested
    directly against a basis of W (x) W (no normal form used)."""
    k = p - 1
    xi = primitive_root(p)
    z = [pow(xi, m, p) for m in range(k)]
    # basis of W = z^perp: w^(m) = e_m - z_m * inv(z_0) e_0 ... with z_0 = 1: e_m - z_m e_0 (m >= 1)
    Wb = []
    for m in range(1, k):
        w = [0] * k
        w[m] = 1
        w[0] = (-z[m]) % p
        Wb.append(w)
    found = []
    for bits in product((0, 1), repeat=k * k - 1):
        C = [[0] * k for _ in range(k)]
        C[0][0] = 1
        for t, b in enumerate(bits, start=1):
            C[t // k][t % k] = b
        ok = True
        for u in Wb:
            for v in Wb:
                s = sum(C[i][j] * u[i] * v[j] for i in range(k) for j in range(k)) % p
                if s:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            found.append(tuple(tuple(r) for r in C))
    return found


# ---------------------------------------------------------------- Rees instances

def filiform_sum_structure(c, g):
    """Structure constants of the direct sum of g filiform algebras of class c.
    Copy t has basis e_{t,0..c} with [e_{t,0}, e_{t,i}] = e_{t,i+1} for 1 <= i < c.
    Returns (dim, bracket) with bracket[(i,j)] = {k: coeff} for i < j."""
    n = c + 1
    dim = g * n
    br = {}
    for t in range(g):
        o = t * n
        for i in range(1, c):
            br[(o, o + i)] = {o + i + 1: 1}
    return dim, br


def bracket_vec(u, v, br, dim, p):
    out = [0] * dim
    for i in range(dim):
        if not u[i]:
            continue
        for j in range(dim):
            if not v[j] or i == j:
                continue
            if i < j and (i, j) in br:
                for k_, cf in br[(i, j)].items():
                    out[k_] = (out[k_] + u[i] * v[j] * cf) % p
            elif j < i and (j, i) in br:
                for k_, cf in br[(j, i)].items():
                    out[k_] = (out[k_] - u[i] * v[j] * cf) % p
    return out


def lower_central_dims(dim, br, p, cmax=50):
    """Dimensions of gamma_1 = L, gamma_2 = [L,L], ... over F_p until 0."""
    basis = [[1 if i == j else 0 for i in range(dim)] for j in range(dim)]
    dims = [dim]
    cur = basis
    while cur and len(dims) <= cmax:
        prods = []
        for u in basis:
            for v in cur:
                w = bracket_vec(u, v, br, dim, p)
                if any(w):
                    prods.append(w)
        if not prods:
            break
        R, piv = rref_rows(prods, p)
        cur = R
        dims.append(len(R))
    return dims


def jacobi_ok(dim, br, p):
    E = [[1 if i == j else 0 for i in range(dim)] for j in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                x = bracket_vec(E[a], bracket_vec(E[b], E[c], br, dim, p), br, dim, p)
                y = bracket_vec(E[b], bracket_vec(E[c], E[a], br, dim, p), br, dim, p)
                z = bracket_vec(E[c], bracket_vec(E[a], E[b], br, dim, p), br, dim, p)
                if any((x[i] + y[i] + z[i]) % p for i in range(dim)):
                    return False
    return True


# ---------------------------------------------------------------- arity baselines

def is_arity(d, a):
    """Schedule 1 arity B_d(a) = [d^{d(d-1)/2} (a+1)^d]^{ceil(log2(d+1))} (thm:is-import)."""
    G = d ** (d * (d - 1) // 2) * (a + 1) ** d
    L = (d + 1 - 1).bit_length()  # ceil(log2(d+1)) for d >= 1
    # ceil(log2(n)) for n = d+1: (n-1).bit_length()
    return G ** L
