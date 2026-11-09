"""Exact feasibility of a universal two-level contraction at (p, kappa).

A two-level contraction is a kappa x kappa matrix C with entries in
P = {0} U (F_p^*)^kappa, C_00 != 0, annihilating W (x) W, W = ker z^T.
Ann(W (x) W) = {z a^T + b z^T}, so C_ij = z_i z_j (alpha_j + beta_i) with
alpha_j = a_j/z_j, beta_i = b_i/z_i.  With z_i in the coset Q_i = g^i H,
C_ij in P iff alpha_j + beta_i in A_{-(i+j)} := Q_{-(i+j)} U {0}; the choice
of representatives z_i is irrelevant.  WLOG beta_0 = 0 (translation
alpha -> alpha + c, beta -> beta - c) and alpha_0 = 1 (scaling by H).

Modes
  general : alpha, beta free (zeros allowed in C)          [exact DFS]
  sym     : alpha = beta = t (the note's form), zeros allowed
  symnz   : alpha = beta = t, every C_ij nonzero (the note's actual sampler
            target; distinctness of t is implied by C_ij != 0 off-diagonal? no:
            t_i + t_j != 0 only; we do not impose distinctness)

Usage: python two_level.py KMIN KMAX PMAX [mode]
Prints, per kappa, every prime p = 1 mod kappa, p <= PMAX, that is
INFEASIBLE, plus the count of feasible primes.  Exact: the DFS is complete.
"""
import sys
import numpy as np
from sympy import primerange, primitive_root


def coset_index(p, k):
    """Array idx[x] = discrete log of x mod k for x in 1..p-1 (idx[0] = -1)."""
    g = primitive_root(p)
    h = (p - 1) // k
    x = np.arange(p, dtype=np.int64)
    # x^h mod p, vectorised square-and-multiply
    res = np.ones(p, dtype=np.int64)
    base = x.copy()
    e = h
    while e:
        if e & 1:
            res = res * base % p
        base = base * base % p
        e >>= 1
    w = pow(g, h, p)  # primitive k-th root of unity
    table = {}
    v = 1
    for m in range(k):
        table[v] = m
        v = v * w % p
    idx = np.full(p, -1, dtype=np.int64)
    for val, m in table.items():
        idx[res == val] = m
    idx[0] = -1
    return idx


def bitsets(p, k, idx):
    """A[m] = bitset (python int, bit x) of Q_m U {0}."""
    out = []
    for m in range(k):
        arr = (idx == m)
        arr[0] = True
        out.append(int.from_bytes(np.packbits(arr, bitorder="little").tobytes(), "little"))
    return out


def shift_down(A, b, p, mask):
    """{x : x + b in A} as bitset, for 0 <= b < p (rotate right by b)."""
    b %= p
    if b == 0:
        return A
    return ((A >> b) | (A << (p - b))) & mask


def members(A):
    x = 0
    while A:
        if A & 1:
            yield x
        A >>= 1
        x += 1


def feasible_general(p, k, A, mask, want_witness=False):
    # beta_0 = 0, alpha_0 = 1.
    # S_j (j>=1) starts as A_{-j}; adding beta_i intersects with A_{-(i+j)} - beta_i.
    S0 = [A[(-j) % k] for j in range(k)]
    # beta_i candidates: 1 + beta_i in A_{-i}  <=> beta_i in A_{-i} - 1
    cand = [shift_down(A[(-i) % k], 1, p, mask) for i in range(k)]
    beta = [0] * k

    def dfs(i, S):
        if i == k:
            return True
        for b in members(cand[i]):
            T = list(S)
            ok = True
            for j in range(1, k):
                T[j] = S[j] & shift_down(A[(-(i + j)) % k], b, p, mask)
                if T[j] == 0:
                    ok = False
                    break
            if ok:
                beta[i] = b
                if dfs(i + 1, T):
                    if want_witness and i == k - 1:
                        pass
                    return True
        return False

    ok = dfs(1, S0)
    if not ok:
        return None
    if not want_witness:
        return True
    # reconstruct alphas
    alpha = [1] + [0] * (k - 1)
    for j in range(1, k):
        S = A[(-j) % k]
        for i in range(1, k):
            S &= shift_down(A[(-(i + j)) % k], beta[i], p, mask)
        alpha[j] = next(members(S))
    return alpha, beta


def feasible_sym(p, k, A, mask, nonzero):
    # t_0 = 1/2 (so 2 t_0 = 1 in H).  Candidates for t_j: 2x in A_{-2j},
    # x + t_i in A_{-(i+j)} (minus 0 if nonzero) for i < j.
    inv2 = pow(2, -1, p)
    Ann = [a & ~1 if nonzero else a for a in A]  # drop 0 from Q_m U {0}
    # {x : 2x in B} for bitset B: x = y/2
    def halve(B):
        out = 0
        for y in members(B):
            out |= 1 << (y * inv2 % p)
        return out
    diag = [halve(Ann[(-2 * j) % k]) for j in range(k)]
    t = [inv2] + [0] * (k - 1)

    def dfs(j):
        if j == k:
            return True
        S = diag[j]
        for i in range(j):
            S &= shift_down(Ann[(-(i + j)) % k], t[i], p, mask)
            if not S:
                return False
        for x in members(S):
            t[j] = x
            if dfs(j + 1):
                return True
        return False

    return dfs(1)


def check_witness(p, k, alpha, beta, idx):
    for i in range(k):
        for j in range(k):
            v = (alpha[j] + beta[i]) % p
            if v and idx[v] != (-(i + j)) % k:
                return False
    return (alpha[0] + beta[0]) % p != 0


def run_list(k, primes, limit):
    """Exact DFS on a given list of primes, with a per-prime alarm (seconds)."""
    import signal

    class Timeout(Exception):
        pass

    def on_alarm(*_):
        raise Timeout()

    signal.signal(signal.SIGALRM, on_alarm)
    for p in primes:
        idx = coset_index(p, k)
        A = bitsets(p, k, idx)
        mask = (1 << p) - 1
        signal.alarm(limit)
        try:
            w = feasible_general(p, k, A, mask, want_witness=True)
            res = "FEASIBLE" if w is not None else "INFEASIBLE"
            if w is not None:
                assert check_witness(p, k, w[0], w[1], idx)
        except Timeout:
            res = "TIMEOUT"
        signal.alarm(0)
        print(f"list kappa={k} p={p} {res}", flush=True)


def main():
    if sys.argv[1] == "list":
        k, limit = int(sys.argv[2]), int(sys.argv[3])
        primes = [int(x) for x in sys.argv[4:]]
        return run_list(k, primes, limit)
    kmin, kmax, pmax = map(int, sys.argv[1:4])
    mode = sys.argv[4] if len(sys.argv) > 4 else "general"
    for k in range(kmin, kmax + 1):
        bad, good = [], 0
        for p in primerange(3, pmax + 1):
            if (p - 1) % k:
                continue
            idx = coset_index(p, k)
            A = bitsets(p, k, idx)
            mask = (1 << p) - 1
            if mode == "general":
                w = feasible_general(p, k, A, mask, want_witness=True)
                if w is not None:
                    assert check_witness(p, k, w[0], w[1], idx)
                ok = w is not None
            else:
                ok = feasible_sym(p, k, A, mask, nonzero=(mode == "symnz"))
            if ok:
                good += 1
            else:
                bad.append(p)
        print(f"mode={mode} kappa={k} pmax={pmax} infeasible={bad} "
              f"largest_infeasible={max(bad) if bad else None} feasible_count={good}",
              flush=True)


if __name__ == "__main__":
    main()
