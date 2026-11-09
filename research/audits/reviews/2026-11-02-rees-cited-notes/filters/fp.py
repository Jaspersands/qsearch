"""Exact F_p helpers for the filter audit: sparse polynomials and linear algebra.

Polynomials are dicts {exponent tuple: residue}. Independent of theorems/.
"""
from itertools import product


def padd(a, b, p, s=1):
    out = dict(a)
    for m, c in b.items():
        v = (out.get(m, 0) + s * c) % p
        if v:
            out[m] = v
        else:
            out.pop(m, None)
    return out


def pmul(a, b, p, maxdeg=None):
    out = {}
    for m1, c1 in a.items():
        d1 = sum(m1)
        for m2, c2 in b.items():
            if maxdeg is not None and d1 + sum(m2) > maxdeg:
                continue
            m = tuple(x + y for x, y in zip(m1, m2))
            v = (out.get(m, 0) + c1 * c2) % p
            if v:
                out[m] = v
            else:
                out.pop(m)
    return out


def pscale(a, c, p):
    return {m: (v * c) % p for m, v in a.items() if (v * c) % p}


def pconst(c, n, p):
    return {(0,) * n: c % p} if c % p else {}


def pvar(i, n):
    return {tuple(int(j == i) for j in range(n)): 1}


def ppow(a, e, p, n, maxdeg=None):
    result, base = pconst(1, n, p), a
    while e:
        if e & 1:
            result = pmul(result, base, p, maxdeg)
        e >>= 1
        if e:
            base = pmul(base, base, p, maxdeg)
    return result


def substitute(f, images, p, n_out, maxdeg=None):
    """f(images[0], ..., images[n-1]); images are polys in n_out variables."""
    out = {}
    cache = {}
    for m, c in f.items():
        term = pconst(c, n_out, p)
        for i, e in enumerate(m):
            if e:
                key = (i, e)
                if key not in cache:
                    cache[key] = ppow(images[i], e, p, n_out, maxdeg)
                term = pmul(term, cache[key], p, maxdeg)
        out = padd(out, term, p)
    return out


def homogeneous_part(f, d):
    return {m: c for m, c in f.items() if sum(m) == d}


def linear_form(row, n):
    return {tuple(int(j == i) for j in range(n)): c for i, c in enumerate(row) if c}


def act(f, g_inv, p):
    """(T_g f)(x) = f(g^{-1} x); g_inv given as a matrix (rows)."""
    n = len(g_inv)
    return substitute(f, [linear_form(row, n) for row in g_inv], p, n)


# ---------- linear algebra over F_p ----------

def rref(rows, p):
    rows = [list(r) for r in rows]
    piv = []
    r = 0
    ncols = len(rows[0]) if rows else 0
    for c in range(ncols):
        k = next((i for i in range(r, len(rows)) if rows[i][c] % p), None)
        if k is None:
            continue
        rows[r], rows[k] = rows[k], rows[r]
        inv = pow(rows[r][c], p - 2, p)
        rows[r] = [(x * inv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p:
                f = rows[i][c]
                rows[i] = [(x - f * y) % p for x, y in zip(rows[i], rows[r])]
        piv.append(c)
        r += 1
    return rows[:r], piv


def rank(rows, p):
    return len(rref(rows, p)[0]) if rows else 0


def matmul(a, b, p):
    return [[sum(x * y for x, y in zip(row, col)) % p for col in zip(*b)] for row in a]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def inverse(a, p):
    n = len(a)
    aug = [list(a[i]) + identity(n)[i] for i in range(n)]
    red, piv = rref(aug, p)
    assert piv[:n] == list(range(n)), "singular"
    return [row[n:] for row in red]


def ut_group(b, p):
    """All b x b upper unitriangular matrices over F_p."""
    slots = [(i, j) for i in range(b) for j in range(i + 1, b)]
    for vals in product(range(p), repeat=len(slots)):
        g = identity(b)
        for (i, j), v in zip(slots, vals):
            g[i][j] = v
        yield g


def block_diag(blocks):
    n = sum(len(b) for b in blocks)
    out = [[0] * n for _ in range(n)]
    o = 0
    for b in blocks:
        for i in range(len(b)):
            for j in range(len(b)):
                out[o + i][o + j] = b[i][j]
        o += len(b)
    return out


def kron(a, b, p):
    return [[(a[i][j] * b[k][l]) % p for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def coords(basis_rows, v, p):
    """Solve v = sum c_i basis_rows[i] (basis independent); None if not in span."""
    k = len(basis_rows)
    n = len(v)
    # columns are basis vectors: solve via rref of [B^T | v]
    aug = [[basis_rows[i][j] for i in range(k)] + [v[j]] for j in range(n)]
    red, piv = rref(aug, p)
    if k in piv:
        return None
    c = [0] * k
    for row, pc in zip(red, piv):
        c[pc] = row[k]
    return c
