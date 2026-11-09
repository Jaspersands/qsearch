"""Numerical check of a class-constant gadget on real column sets.

For (p, S, k, d, L) solve the feasibility CNF once, then on random instances:
  (A) random columns: X = q + k uniformly random columns of F_p^q; compute a basis of D(X)
      (dim k generically), the labels, the class sums w_ell, h_j = sum Phi_j(ell) w_ell, and
      check for every alpha != 0 that y_alpha in S^X, sum_i y_alpha(i) v_i == alpha . h, and
      that either h_1..h_d are independent (gain d) or some nonzero y_alpha is a zero-sum.
  (B) adversarial label multiplicities: a column set whose labels cover every label of L
      with random multiplicities, with random columns consistent with the prescribed dependencies.
Every arithmetic step is exact in F_p (numpy int64).
"""
import sys, itertools
import numpy as np
from gadget_sat import parse_S, parse_L
from gadget_cnf import solve

rng = np.random.default_rng(20261108)


def rank_mod(M, p):
    M = M.copy() % p
    r = 0
    rows, cols = M.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i, c]), None)
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[r]) % p
        r += 1
        if r == rows:
            break
    return r


def nullspace_mod(A, p):
    """Basis of {x : A x = 0} over F_p, A is q x N."""
    A = A.copy() % p
    q, N = A.shape
    pivcols = []
    r = 0
    for c in range(N):
        piv = next((i for i in range(r, q) if A[i, c]), None)
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        for i in range(q):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        pivcols.append(c)
        r += 1
        if r == q:
            break
    free = [c for c in range(N) if c not in pivcols]
    basis = []
    for f in free:
        x = np.zeros(N, dtype=np.int64)
        x[f] = 1
        for i, pc in enumerate(pivcols):
            x[pc] = (-A[i, f]) % p
        basis.append(x)
    return np.array(basis, dtype=np.int64).reshape(len(basis), N)


def apply_gadget(V, p, S, k, d, Phi, gamma, deps):
    """V: q x N columns; deps: k x N dependency basis.  Returns ('gain', H) or ('zero', y)."""
    q, N = V.shape
    Sset = set(S)
    labels = [tuple(int(deps[j, i]) for j in range(k)) for i in range(N)]
    assert all(any(l) for l in labels), 'a column outside every support'
    H = np.zeros((d, q), dtype=np.int64)
    for i, l in enumerate(labels):
        for j in range(d):
            H[j] = (H[j] + Phi[l][j] * V[:, i]) % p
    for a in itertools.product(range(p), repeat=d):
        if not any(a):
            continue
        y = np.array([(sum(a[j] * Phi[l][j] for j in range(d)) + sum(gamma[a][t] * l[t] for t in range(k))) % p
                      for l in labels], dtype=np.int64)
        assert all(int(v) in Sset for v in y), 'coefficient outside S'
        target = sum(a[j] * H[j] for j in range(d)) % p
        assert np.array_equal((V @ y) % p, target), 'realizer does not realize alpha.h'
        assert y.any(), 'degenerate realizer'
        if not target.any():
            return 'zero', y
    assert rank_mod(H, p) == d
    return 'gain', H


def main():
    p, Sspec, k, d, Lspec = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    trials = int(sys.argv[6]) if len(sys.argv) > 6 else 200
    S = parse_S(p, Sspec)
    L = parse_L(p, k, Lspec)
    r, sol, dt = solve(p, S, k, d, L)
    assert r == 'sat', r
    Phi, gamma = sol
    Lset = set(L)
    print(f'p={p} S={S} k={k} d={d} L={Lspec}: gadget found [{dt:.1f}s]; trials={trials}')
    gains = zeros = skipped = 0
    for q in (4, 6, 10, 20, 40):
        for _ in range(trials):
            # (A) random columns, N = q + k
            V = rng.integers(0, p, size=(q, q + k)).astype(np.int64)
            D = nullspace_mod(V, p)
            if D.shape[0] != k:
                skipped += 1
                continue
            labels = [tuple(int(D[j, i]) for j in range(k)) for i in range(q + k)]
            if not all(l in Lset for l in labels):
                skipped += 1
                continue
            res, _ = apply_gadget(V, p, S, k, d, Phi, gamma, D)
            gains += res == 'gain'
            zeros += res == 'zero'
    print(f' (A) random q+k columns, q in 4..40: gain {gains}, zero-sum {zeros}, skipped(label outside L or dim != k) {skipped}')
    gains = zeros = 0
    for q in (6, 10, 20):
        for _ in range(trials):
            # (B) every label of L present, random multiplicities; columns consistent with k prescribed deps
            mult = rng.integers(1, 4, size=len(L))
            labels = [l for l, m in zip(L, mult) for _ in range(m)]
            N = len(labels)
            Dm = np.array(labels, dtype=np.int64).T  # k x N
            # columns: V = M * B where B is a basis of the orthogonal complement of rowspace(Dm): V Dm^T = 0
            B = nullspace_mod(Dm, p)                 # (N-k) x N, rows orthogonal to Dm rows
            M = rng.integers(0, p, size=(q, B.shape[0])).astype(np.int64)
            V = (M @ B) % p
            assert not ((V @ Dm.T) % p).any()
            # D(X) may be larger than span(Dm) (q < N-k); the gadget only uses the two prescribed deps
            res, _ = apply_gadget(V, p, S, k, d, Phi, gamma, Dm)
            gains += res == 'gain'
            zeros += res == 'zero'
    print(f' (B) all labels, random multiplicities, q in 6..20: gain {gains}, zero-sum {zeros}')


if __name__ == '__main__':
    main()
