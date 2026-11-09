"""fb check 2: Remark rem:filters item (i) example "F = x_{D-2} under UT_D(F_p): dim W = 2, ker rho_W of index p".

F is a linear form c.x; the action is (g.F)(x) = F(g^{-1} x) (the convention of app:filters-applications,
H = {g : F(g^{-1}x) = F(x)}), g upper unitriangular.  W = span of the orbit; rho_W(g) = action on W.
We report dim W and [G : ker rho_W] for the variable called x_{D-2} under 1-based indexing
(x_1..x_D, as in app:filters-applications) and under 0-based indexing (x_0..x_{D-1}),
and also for the transposed (lower-triangular) action.
"""
import itertools
import numpy as np

def inv_mod(a, p):
    return pow(int(a) % p, p - 2, p)

def rank_mod(rows, p):
    A = np.array(rows, dtype=np.int64) % p
    r = 0
    for c in range(A.shape[1]):
        pr = next((i for i in range(r, A.shape[0]) if A[i, c]), None)
        if pr is None:
            continue
        A[[r, pr]] = A[[pr, r]]
        A[r] = A[r] * inv_mod(A[r, c], p) % p
        for i in range(A.shape[0]):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
    return r

def ut_elements(D, p):
    pos = [(i, j) for i in range(D) for j in range(i + 1, D)]
    for vals in itertools.product(range(p), repeat=len(pos)):
        g = np.eye(D, dtype=np.int64)
        for (i, j), v in zip(pos, vals):
            g[i, j] = v
        yield g

def inv_unitri(g, p):
    D = g.shape[0]
    n = (g - np.eye(D, dtype=np.int64)) % p
    out = np.eye(D, dtype=np.int64); term = np.eye(D, dtype=np.int64)
    for k in range(1, D):
        term = (term @ n) % p
        out = (out + (term if k % 2 == 0 else -term)) % p
    return out

def study(D, p, idx0, transpose):
    c = np.zeros(D, dtype=np.int64); c[idx0] = 1
    orbit = {}
    G = list(ut_elements(D, p))
    for g in G:
        gi = inv_unitri(g, p)
        if transpose:
            gi = gi.T
        orbit[tuple(((c @ gi) % p).tolist())] = 1
    O = [list(v) for v in orbit]
    dimW = rank_mod(O, p)
    # kernel of rho_W: g acts trivially on W iff it fixes every orbit vector (they span W)
    ker = 0
    for g in G:
        gi = inv_unitri(g, p)
        if transpose:
            gi = gi.T
        if all(tuple(((np.array(v) @ gi) % p).tolist()) == tuple(v) for v in O):
            ker += 1
    return dimW, len(G) // ker

if __name__ == "__main__":
    p = 3
    for D in (4, 5):
        for label, idx0 in (("1-based x_{D-2} (0-based index D-3)", D - 3), ("0-based x_{D-2} (0-based index D-2)", D - 2)):
            for tr in (False, True):
                dimW, index = study(D, p, idx0, tr)
                print(f"D={D} p={p} {label:38s} action={'transpose' if tr else 'F(g^-1 x)'}: dim W = {dimW}, [G:ker rho_W] = {index} = p^{round(np.log(index)/np.log(p))}")
