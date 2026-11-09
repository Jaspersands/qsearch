"""Independent checks (sub, 2026-11-09) of Lemmas app-sub-antisym, app-sub-growth,
app-sub-lcu and the no-recovery leak values of appendix-subspace.tex.

Float linear algebra (numpy), small (d, r, k). Prints residuals; a residual
> 1e-9 is a falsification.
"""
import itertools, math, sys
import numpy as np

rng = np.random.default_rng(20261109)


def perm_op(d, k, perm):
    """P_pi on (C^d)^{(x)k}: factor i of the input goes to position perm[i]."""
    D = d ** k
    P = np.zeros((D, D))
    for idx in itertools.product(range(d), repeat=k):
        out = [0] * k
        for i in range(k):
            out[perm[i]] = idx[i]
        a = np.ravel_multi_index(idx, (d,) * k)
        b = np.ravel_multi_index(tuple(out), (d,) * k)
        P[b, a] = 1.0
    return P


def sign(perm):
    s, seen = 1, [False] * len(perm)
    for i in range(len(perm)):
        if not seen[i]:
            j, L = i, 0
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                L += 1
            if L % 2 == 0:
                s = -s
    return s


def antisym(d, k):
    D = d ** k
    A = np.zeros((D, D))
    for perm in itertools.permutations(range(k)):
        A += sign(perm) * perm_op(d, k, perm)
    return A / math.factorial(k)


def swap(d, k, i, j):
    perm = list(range(k))
    perm[i], perm[j] = perm[j], perm[i]
    return perm_op(d, k, perm)


def kron_all(ms):
    out = np.array([[1.0 + 0j]])
    for m in ms:
        out = np.kron(out, m)
    return out


def rand_subspace(d, r):
    X = rng.normal(size=(d, r)) + 1j * rng.normal(size=(d, r))
    Q, _ = np.linalg.qr(X)
    return Q  # d x r orthonormal frame


def ptrace_last(M, dims_keep, d_last):
    Dk = int(np.prod(dims_keep))
    M4 = M.reshape(Dk, d_last, Dk, d_last)
    return np.einsum('ajbj->ab', M4)


def rand_density_in(Pk, rank=3):
    """Random density supported in range(Pk) (Pk a projector)."""
    D = Pk.shape[0]
    X = rng.normal(size=(D, rank)) + 1j * rng.normal(size=(D, rank))
    X = Pk @ X
    rho = X @ X.conj().T
    return rho / np.trace(rho).real


def rand_unitary_completion(L):
    """Random unitary J with J|0> = L^{-1/2} sum_j |j>."""
    f = np.ones(L) / math.sqrt(L)
    X = rng.normal(size=(L, L)) + 1j * rng.normal(size=(L, L))
    X[:, 0] = f
    Q, R = np.linalg.qr(X)
    # fix phase so that first column is exactly f
    ph = Q[:, 0].conj() @ f
    Q[:, 0] *= ph / abs(ph)
    Q[:, 0] = f  # exact
    # re-orthonormalize the remaining columns against f
    for c in range(1, L):
        v = Q[:, c]
        for c2 in range(c):
            v = v - (Q[:, c2].conj() @ v) * Q[:, c2]
        Q[:, c] = v / np.linalg.norm(v)
    assert np.allclose(Q.conj().T @ Q, np.eye(L))
    return Q


worst = {}


def rec(name, val):
    worst[name] = max(worst.get(name, 0.0), float(val))


cases = [(3, 2, 1), (3, 2, 2), (3, 3, 2), (3, 3, 1), (4, 3, 2), (4, 3, 1), (4, 4, 3), (4, 4, 2), (4, 2, 1)]
leaks = []
for (d, r, k) in cases:
    if k >= r:
        continue
    Y = rand_subspace(d, r)
    PiV = Y @ Y.conj().T
    Pk = antisym(d, k)
    Pk1 = antisym(d, k + 1)
    I_d = np.eye(d)
    PkI = np.kron(Pk, I_d)
    # (a)
    rec('antisym(a)', np.abs(PkI @ Pk1 - Pk1).max())
    rec('antisym(a)', np.abs(Pk1 @ PkI - Pk1).max())
    # (b)
    S = sum(swap(d, k + 1, j, k) for j in range(k))
    rhs = (np.eye(d ** (k + 1)) - S) @ PkI / (k + 1)
    rec('antisym(b)', np.abs(Pk1 @ PkI - rhs).max())
    # (c)
    PVk = kron_all([PiV] * k) @ Pk
    PVk1 = kron_all([PiV] * (k + 1)) @ Pk1
    tr = ptrace_last(PVk1, [d] * k, d)
    rec('antisym(c)', np.abs(tr - (r - k) / (k + 1) * PVk).max())
    # growth (a)-(c)
    rho = PiV / r
    for trial in range(3):
        vr = rand_density_in(PVk)
        nu = np.kron(vr, rho)
        pacc = np.trace(Pk1 @ nu).real
        rec('growth(a) p_k', abs(pacc - (r - k) / (r * (k + 1))))
        acc = Pk1 @ nu @ Pk1
        PVk1_ = PVk1
        rec('growth(b) support', np.abs(acc - PVk1_ @ acc @ PVk1_).max())
        rej = (np.eye(d ** (k + 1)) - Pk1) @ nu @ (np.eye(d ** (k + 1)) - Pk1)
        rej_k = ptrace_last(rej, [d] * k, d)
        rec('growth(c) support', np.abs(rej_k - PVk @ rej_k @ PVk).max())
        if k + 1 == r:
            # accepted state equals Omega_V
            w = np.zeros(d ** r, dtype=complex)
            # Omega_V = P_r applied to y1 x ... x yr times sqrt(r!)
            prod = kron_all([Y[:, [i]] for i in range(r)])
            Om = math.sqrt(math.factorial(r)) * (Pk1 @ prod)
            Om = Om / np.linalg.norm(Om)
            rec('growth(b) = Omega', np.abs(acc / pacc - Om @ Om.conj().T).max())
    # LCU (Lemma app-sub-lcu)
    L = k + 1
    for trial in range(3):
        J = rand_unitary_completion(L)
        Dreg = d ** (k + 1)
        Sel = np.zeros((L * Dreg, L * Dreg), dtype=complex)
        for j in range(L):
            Pj = np.zeros((L, L)); Pj[j, j] = 1
            Sel += np.kron(Pj, np.eye(Dreg) if j == 0 else -swap(d, k + 1, j - 1, k))
        W = np.kron(J.conj().T, np.eye(Dreg)) @ Sel @ np.kron(J, np.eye(Dreg))
        rec('W unitary', np.abs(W.conj().T @ W - np.eye(L * Dreg)).max())
        P0 = np.zeros((L, L)); P0[0, 0] = 1
        M0 = np.kron(P0, np.eye(Dreg)); M1 = np.eye(L * Dreg) - M0
        nu_full = rand_density_in(PkI, rank=4)  # any density in range(P_k x I)
        inp = np.kron(P0, nu_full)
        accb = M0 @ W @ inp @ W.conj().T @ M0
        rejb = W.conj().T @ M1 @ W @ inp @ W.conj().T @ M1 @ W
        IP = np.eye(Dreg) - Pk1
        rec('LCU accept branch', np.abs(accb - np.kron(P0, Pk1 @ nu_full @ Pk1)).max())
        rec('LCU reject branch (recovery)', np.abs(rejb - np.kron(P0, IP @ nu_full @ IP)).max())
        # Off-domain: accept Kraus operator vs P_{k+1}
        A = (np.eye(Dreg) - sum(swap(d, k + 1, j, k) for j in range(k))) / (k + 1)
        dist = np.linalg.norm(A - Pk1, 2)
        rec(f'offdomain ||A-P_k+1|| k={k} (claim k/(k+1)={k/(k+1):.4f} for k>=2)', dist)
        # No recovery: weight outside wedge^k V of the retained state on rejection
        vr = rand_density_in(PVk)
        nu = np.kron(vr, rho)
        inp = np.kron(P0, nu)
        rej_noR = M1 @ W @ inp @ W.conj().T @ M1
        # trace out ancilla
        R4 = rej_noR.reshape(L, Dreg, L, Dreg)
        rej_reg = np.einsum('aiaj->ij', R4)
        prej = np.trace(rej_reg).real
        rej_k = ptrace_last(rej_reg, [d] * k, d) / prej
        leak = 1 - np.trace(PVk @ rej_k).real
        leaks.append((d, r, k, trial, prej, leak))
        rec(f'reject prob vs 1-p_k (d,r,k)=({d},{r},{k})', abs(prej - (1 - (r - k) / (r * (k + 1)))))

for kk, v in worst.items():
    print(f'{kk:70s} {v:.3e}')
print('No-recovery leak (normalized weight outside wedge^k V on rejection); predicted (k-1)/k:')
for (d, r, k, t, prej, leak) in leaks:
    print(f'  d={d} r={r} k={k} J-trial={t}  P(reject)={prej:.6f}  leak={leak:.6f}  (k-1)/k={(k-1)/k:.6f}')
