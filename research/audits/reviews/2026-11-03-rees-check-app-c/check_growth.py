"""Item 3 (campaign 4): Lemmas app-sub-antisym, app-sub-growth, app-sub-lcu.

Part 1 (exact, Fractions): antisymmetrizer identities (a), (b), (c) for real
rational subspaces W (Pi_W = Y (Y^T Y)^{-1} Y^T is rational).
Part 2 (complex128 and mpmath 30 digits): the LCU realization with recovery,
on random densities supported in range(P_k (x) I) and in wedge^k V (x) V,
for several completions J; state independence of p_k; support invariants;
the failure of the invariant without recovery.
Part 3: an adversarial growth tree: after every reject/accept history of depth
<= 4 the next acceptance probability is exactly p_k.

Run: /opt/anaconda3/bin/python check_growth.py
"""
import itertools
import random
from fractions import Fraction as F

import numpy as np
from mpmath import mp

random.seed(7)
rng = np.random.default_rng(7)


# ---------- permutation operators ----------
def perm_sign(p):
    s, seen = 1, [False] * len(p)
    for i in range(len(p)):
        if not seen[i]:
            j, ln = i, 0
            while not seen[j]:
                seen[j], j, ln = True, p[j], ln + 1
            if ln % 2 == 0:
                s = -s
    return s


def perm_op_index(d, k, p):
    """P_pi maps e_{i_1}x...x e_{i_k} to the tensor whose factor p[j] is e_{i_j}."""
    n = d ** k
    img = [0] * n
    for idx in range(n):
        digs = [(idx // d ** (k - 1 - t)) % d for t in range(k)]
        new = [0] * k
        for j in range(k):
            new[p[j]] = digs[j]
        img[idx] = sum(new[t] * d ** (k - 1 - t) for t in range(k))
    return img


def antisym(d, k, dtype=object):
    n = d ** k
    P = np.zeros((n, n), dtype=dtype)
    if dtype is object:
        P[:, :] = F(0)
    kf = 1
    for i in range(2, k + 1):
        kf *= i
    for p in itertools.permutations(range(k)):
        img = perm_op_index(d, k, p)
        sg = perm_sign(p)
        for idx in range(n):
            P[img[idx], idx] += (F(sg, kf) if dtype is object else sg / kf)
    return P


def swap_op(d, k, i, j, dtype=float):
    p = list(range(k))
    p[i], p[j] = p[j], p[i]
    img = perm_op_index(d, k, p)
    n = d ** k
    S = np.zeros((n, n), dtype=dtype)
    for idx in range(n):
        S[img[idx], idx] = 1
    return S


def kron(*ms):
    out = ms[0]
    for m in ms[1:]:
        out = np.kron(out, m)
    return out


def ptrace_last(X, d, k):
    """trace out the last factor of (C^d)^{(x)k}."""
    n = d ** (k - 1)
    X4 = X.reshape(n, d, n, d)
    if X.dtype == object:
        out = np.empty((n, n), dtype=object)
        for a in range(n):
            for b in range(n):
                out[a, b] = sum((X4[a, e, b, e] for e in range(d)), F(0))
        return out
    return np.einsum("aebe->ab", X4)


def ptrace_first(X, dims, keep_from):
    """trace out the first factor of dimension dims[0]."""
    a = dims[0]
    n = X.shape[0] // a
    X4 = X.reshape(a, n, a, n)
    return np.einsum("ixiy->xy", X4)


# ---------- part 1: exact ----------
def rational_projector(d, r):
    while True:
        Y = np.array([[F(random.randint(-3, 3)) for _ in range(r)] for _ in range(d)], dtype=object)
        G = Y.T.dot(Y)
        try:
            Gi = exact_inverse(G)
        except ZeroDivisionError:
            continue
        return Y.dot(Gi).dot(Y.T)


def exact_inverse(A):
    n = A.shape[0]
    M = [[A[i, j] for j in range(n)] + [F(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            raise ZeroDivisionError
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return np.array([row[n:] for row in M], dtype=object)


def part1():
    cases = [(3, 1), (3, 2), (4, 1), (4, 2), (5, 1), (5, 2)]  # (d, k), k+1 <= 3
    checked = 0
    for d, k in cases:
        Pk = antisym(d, k)
        Pk1 = antisym(d, k + 1)
        I = np.empty((d, d), dtype=object)
        for i in range(d):
            for j in range(d):
                I[i, j] = F(int(i == j))
        PkI = kron(Pk, I)
        # (a)
        assert (PkI.dot(Pk1) == Pk1).all() and (Pk1.dot(PkI) == Pk1).all(), ("a", d, k)
        # (b)
        n1 = d ** (k + 1)
        Ssum = np.zeros((n1, n1), dtype=object)
        Ssum[:, :] = F(0)
        for j in range(k):
            Ssum = Ssum + swap_op(d, k + 1, j, k, dtype=object)
        Id = np.empty((n1, n1), dtype=object)
        for i in range(n1):
            for j in range(n1):
                Id[i, j] = F(int(i == j))
        rhs = (Id - Ssum).dot(PkI) * F(1, k + 1)
        assert (Pk1.dot(PkI) == rhs).all(), ("b", d, k)
        # (c) for every rank r > k
        for r in range(k + 1, d + 1):
            PW = rational_projector(d, r)
            PWk = kron(*([PW] * k)) if k > 1 else PW
            PWk1 = kron(*([PW] * (k + 1)))
            PkW = Pk.dot(PWk)
            Pk1W = Pk1.dot(PWk1)
            assert (PkW == PWk.dot(Pk)).all()
            lhs = ptrace_last(Pk1W, d, k + 1)
            assert (lhs == PkW * F(r - k, k + 1)).all(), ("c", d, k, r)
            checked += 1
    print(f"part 1 exact: antisymmetrizer (a), (b) on {len(cases)} (d,k); (c) on {checked} (d,k,r) rational W: ok")


# ---------- part 2/3: LCU ----------
def haar_unitary(n):
    z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    return q * (np.diag(r) / abs(np.diag(r)))


def completion(L, kind):
    """unitary J with J|0> = L^{-1/2} sum_j |j>."""
    f = np.ones(L) / np.sqrt(L)
    if kind == "dft":
        w = np.exp(2j * np.pi / L)
        return np.array([[w ** (a * b) for b in range(L)] for a in range(L)]) / np.sqrt(L)
    if kind == "householder":
        u = np.zeros(L, complex)
        u[0] = 1
        v = u - f
        return np.eye(L) - 2 * np.outer(v, v.conj()) / (v.conj() @ v)
    # random completion: first column f, rest random orthonormal
    M = np.column_stack([f] + [rng.normal(size=L) + 1j * rng.normal(size=L) for _ in range(L - 1)])
    q, r = np.linalg.qr(M)
    q = q * (np.diag(r) / abs(np.diag(r)))
    q[:, 0] = f  # QR keeps the first column up to phase; restore it exactly
    return q


def build_W(d, k, J):
    L = k + 1
    n = d ** (k + 1)
    Sel = np.zeros((L * n, L * n), complex)
    Sel[:n, :n] = np.eye(n)
    for j in range(1, L):
        Sel[j * n:(j + 1) * n, j * n:(j + 1) * n] = -swap_op(d, k + 1, j - 1, k)
    JI = np.kron(J, np.eye(n))
    return JI.conj().T @ Sel @ JI


def random_density_in(Pproj, rank):
    """random density supported in range(Pproj)."""
    n = Pproj.shape[0]
    X = rng.normal(size=(n, rank)) + 1j * rng.normal(size=(n, rank))
    X = Pproj @ X
    rho = X @ X.conj().T
    return rho / np.trace(rho).real


def frame(d, r):
    return haar_unitary(d)[:, :r]


def lcu_branches(nu, d, k, J, recover=True):
    L = k + 1
    n = d ** (k + 1)
    W = build_W(d, k, J)
    e0 = np.zeros((L, L))
    e0[0, 0] = 1
    st = np.kron(e0, nu)
    st = W @ st @ W.conj().T
    P0 = np.kron(e0, np.eye(n))
    acc = P0 @ st @ P0
    rej = (np.eye(L * n) - P0) @ st @ (np.eye(L * n) - P0)
    if recover:
        rej = W.conj().T @ rej @ W
    return acc, rej


def part2():
    worst = 0.0
    worst_noRec = {}
    count = 0
    for d in (2, 3, 4):
        for k in (1, 2, 3):
            if d ** (k + 1) > 256 or k >= d:
                continue
            Pk = antisym(d, k, dtype=float)
            Pk1 = antisym(d, k + 1, dtype=float)
            PkI = np.kron(Pk, np.eye(d))
            n = d ** (k + 1)
            L = k + 1
            e0 = np.zeros((L, L))
            e0[0, 0] = 1
            for kind in ("dft", "householder", "random"):
                J = completion(L, kind)
                assert np.allclose(J[:, 0], np.ones(L) / np.sqrt(L)) and np.allclose(J.conj().T @ J, np.eye(L))
                for _ in range(3):
                    nu = random_density_in(PkI, rank=3)
                    acc, rej = lcu_branches(nu, d, k, J)
                    tgt_a = np.kron(e0, Pk1 @ nu @ Pk1)
                    Q = np.eye(n) - Pk1
                    tgt_r = np.kron(e0, Q @ nu @ Q)
                    worst = max(worst, abs(acc - tgt_a).max(), abs(rej - tgt_r).max())
                    count += 1
                # without recovery, inside the growth setting d >= r > k
                for r in range(k + 1, d + 1):
                    Y = frame(d, r)
                    PV = Y @ Y.conj().T
                    PVk = PV if k == 1 else np.kron(*([PV] * k)) if k == 2 else np.kron(np.kron(PV, PV), PV)
                    PkV = Pk @ PVk
                    vr = random_density_in(PkV, rank=1)
                    rho = PV / r
                    acc, rej = lcu_branches(np.kron(vr, rho), d, k, J, recover=False)
                    # discard ancilla and fresh register; renormalize reject branch
                    pr = np.trace(rej).real
                    kept = ptrace_last(ptrace_first(rej, (L,), 1), d, k + 1) / pr
                    out = 1 - np.trace(PkV @ kept).real
                    key = (d, r, k, kind)
                    worst_noRec[key] = max(worst_noRec.get(key, 0), out)
    print(f"part 2 LCU with recovery: {count} random inputs in range(P_k x I), max entry error {worst:.1e}")
    print("  without recovery, weight of the kept k registers outside wedge^k V (reject branch, normalized, pure input):")
    for key, v in sorted(worst_noRec.items()):
        if v > 1e-12:
            print(f"    d={key[0]} r={key[1]} k={key[2]} J={key[3]:11s}: {v:.3f}")
    ks1 = [v for key, v in worst_noRec.items() if key[2] == 1]
    print(f"  k = 1 cases without recovery: max weight outside V = {max(ks1):.1e}")
    return worst


def part3():
    """growth tree: every history of accepts/rejects of depth <= 4."""
    worst_p = 0.0
    worst_supp = 0.0
    nodes = 0
    for d, r in ((3, 3), (4, 3), (4, 4), (3, 2)):
        Y = frame(d, r)
        PV = Y @ Y.conj().T
        rho = PV / r
        J_by_L = {L: completion(L, "random") for L in range(2, r + 1)}

        def PkV(k):
            Pk = antisym(d, k, dtype=float)
            PVk = PV
            for _ in range(k - 1):
                PVk = np.kron(PVk, PV)
            return Pk @ PVk

        def rec(state, k, depth):
            nonlocal worst_p, worst_supp, nodes
            nodes += 1
            if k == r:
                Om = PkV(r)
                worst_supp = max(worst_supp, abs(state - Om).max())  # rank-1 projector
                return
            if depth == 0:
                return
            L = k + 1
            acc, rej = lcu_branches(np.kron(state, rho), d, k, J_by_L[L])
            pa = np.trace(acc).real
            pk = (r - k) / (r * (k + 1))
            worst_p = max(worst_p, abs(pa - pk))
            accS = ptrace_first(acc, (L,), 1) / pa
            rejS = ptrace_last(ptrace_first(rej, (L,), 1), d, k + 1) / (1 - pa)
            worst_supp = max(worst_supp, 1 - np.trace(PkV(k + 1) @ accS).real, 1 - np.trace(PkV(k) @ rejS).real)
            rec(accS, k + 1, depth - 1)
            rec(rejS, k, depth - 1)

        rec(rho, 1, 4)
    print(f"part 3 growth tree: {nodes} nodes, max |P(accept) - p_k| = {worst_p:.1e}, max support leak = {worst_supp:.1e}")


def part_mp():
    """mpmath 30-digit replay of the LCU identity at d = r = 3, k = 2, J = DFT."""
    mp.dps = 30
    d, k = 3, 2
    L = k + 1
    n = d ** (k + 1)
    w = mp.exp(2j * mp.pi / L)
    J = mp.matrix([[w ** (a * b) / mp.sqrt(L) for b in range(L)] for a in range(L)])
    Sel = mp.zeros(L * n, L * n)
    for i in range(n):
        Sel[i, i] = 1
    for j in range(1, L):
        S = swap_op(d, k + 1, j - 1, k)
        for a in range(n):
            for b in range(n):
                if S[a, b]:
                    Sel[j * n + a, j * n + b] = -1
    JI = mp.zeros(L * n, L * n)
    for a in range(L):
        for b in range(L):
            for i in range(n):
                JI[a * n + i, b * n + i] = J[a, b]
    W = JI.H * Sel * JI
    def to_mp(A):
        return mp.matrix([[mp.mpf(x.numerator) / x.denominator for x in row] for row in A])
    Pk = antisym(d, k)
    Ifr = np.empty((d, d), dtype=object)
    for i in range(d):
        for j in range(d):
            Ifr[i, j] = F(int(i == j))
    PkI = to_mp(kron(Pk, Ifr))
    Pk1 = to_mp(antisym(d, k + 1))
    worst = mp.mpf(0)
    for _ in range(3):
        x = mp.matrix([mp.mpc(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(n)])
        psi = PkI * x
        big = mp.zeros(L * n, 1)
        for i in range(n):
            big[i] = psi[i]
        out = W * big
        tgt = Pk1 * psi
        worst = max(worst, max(abs(out[i] - tgt[i]) for i in range(n)))
        rest = out - mp.matrix([out[i] if i < n else 0 for i in range(L * n)])
        back = W.H * rest
        tgt_r = psi - tgt
        worst = max(worst, max(abs(back[i] - tgt_r[i]) for i in range(n)), max(abs(back[i]) for i in range(n, L * n)))
    print(f"part 2 (mpmath 30 digits, d=3, k=2, J=DFT): max error {mp.nstr(worst, 3)}")


if __name__ == "__main__":
    part1()
    part2()
    part_mp()
    part3()
