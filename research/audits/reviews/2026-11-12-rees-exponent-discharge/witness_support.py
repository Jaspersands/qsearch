#!/opt/anaconda3/bin/python
"""Finite sampled check: support of the Schedule 2 two-level witness on uniform random columns.

The pool lemma (note, section 5.1) says that targets with weight 0 can be kept for the next merge,
so the amortised cost of one merge is the witness SUPPORT, not the arity.  This script measures
the support of the two-level construction of appendix-schedule2 Lemma app-s2-tensor (level-one
dependence in each block of a+1 columns, level-two dependence among the (kappa-1)a+1 blocks);
the support is the set of columns with c_b != 0 in blocks with eta_nu != 0, independent of the
contraction C when every C_ij != 0 (symmetric form).  Sampled computation; proves nothing.
"""
import random, sys


def nullvec(rows, ncols, p):
    """A nonzero vector x with rows @ x = 0 (rows: list of lists, mod p); assumes ncols > rank."""
    A = [r[:] for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = pow(A[r][c], p - 2, p)
        A[r] = [x * iv % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in piv][0]
    x = [0] * ncols
    x[free] = 1
    for i, c in enumerate(piv):
        x[c] = (-A[i][free]) % p
    return x


def coset(x, p, k, g):
    h = (p - 1) // k
    y = pow(x, h, p)
    z = pow(g, h, p)
    t = 1
    for m in range(k):
        if t == y:
            return m
        t = t * z % p
    raise ValueError


def trial(p, k, a, g, rng):
    N = (k - 1) * a + 1
    M = (a + 1) * N
    cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
    blocks, V = [], []
    for nu in range(N):
        B = list(range(nu * (a + 1), (nu + 1) * (a + 1)))
        rows = [[cols[b][i] for b in B] for i in range(a)]
        cvec = nullvec(rows, a + 1, p)
        T = [[0] * a for _ in range(k)]
        for j, b in enumerate(B):
            if cvec[j]:
                m = coset(cvec[j], p, k, g)
                # T_m += c_b lambda_b (weights omega^k = c_b / z_m; only the coset sum matters here)
                for i in range(a):
                    T[m][i] = (T[m][i] + cvec[j] * cols[b][i]) % p
        blocks.append((B, cvec))
        V.append([T[m][i] for m in range(1, k) for i in range(a)])
    rows = [[V[nu][r] for nu in range(N)] for r in range((k - 1) * a)]
    eta = nullvec(rows, N, p)
    supp = sum(sum(1 for x in cvec if x) for (B, cvec), e in zip(blocks, eta) if e)
    return supp, M


if __name__ == '__main__':
    rng = random.Random(20261112)
    for p, k, g in ((10007, 2, 5), (10009, 3, 11), (10009, 4, 11)):
        assert (p - 1) % k == 0
        for a in (2, 4, 6, 8):
            res = [trial(p, k, a, g, rng) for _ in range(40)]
            mins = min(s for s, M in res)
            M = res[0][1]
            mean = sum(s for s, _ in res) / len(res)
            print('p=%d kappa=%d a=%d arity M=%d support mean=%.2f min=%d (mean/M=%.4f)' % (p, k, a, M, mean, mins, mean / M))
            sys.stdout.flush()
