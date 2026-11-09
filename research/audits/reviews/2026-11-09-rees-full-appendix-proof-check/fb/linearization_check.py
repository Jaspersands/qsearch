"""fb check 4: first-order linearization for polynomial symmetries (rem:filters (ii) last sentence;
app:filters-applications second paragraph).

For A = J_D (nilpotency index nu = D) acting by F -> F(exp(-tA) x) on homogeneous forms of degree Delta
in D variables over F_p (p >= D), compare
   Fix  = {F : F(exp(-A) x) = F(x)}       (F fixed by exp(A), hence by the whole one-parameter group)
   Ker  = {F : A.F = sum_k dF/dx_k (A x)_k = 0}  (first-order condition)
exactly, by linear algebra on the monomial basis.  The paper: equality (for every F) when
p > max(D, (D-1) Delta); "Delta < p is not enough".  Any F in Fix \\ Ker or Ker \\ Fix is a polynomial of
degree Delta < p on which the first-order Lie method returns a subgroup too small, resp. too large, for
G = exp(F_p A).  Since the forms of degree Delta < p in KD variables are exactly the R_F of p-weight
Delta (Frobenius-twisted coordinates), the same table also witnesses failures of the R_F method when
p <= (nu-1) delta.
"""
import itertools
import numpy as np

def monomials(D, Delta):
    return [a for a in itertools.product(range(Delta + 1), repeat=D) if sum(a) == Delta]

def poly_mul(P, Q, p):
    R = {}
    for a, ca in P.items():
        for b, cb in Q.items():
            k = tuple(x + y for x, y in zip(a, b))
            R[k] = (R.get(k, 0) + ca * cb) % p
    return {k: v for k, v in R.items() if v}

def subst(alpha, M, p):
    """x^alpha evaluated at M x (M over F_p), as dict."""
    D = len(alpha)
    P = {tuple([0] * D): 1}
    for i, a in enumerate(alpha):
        lin = {}
        for j in range(D):
            if M[i, j] % p:
                e = [0] * D; e[j] = 1; lin[tuple(e)] = int(M[i, j] % p)
        for _ in range(a):
            P = poly_mul(P, lin, p)
    return P

def rank_mod(A, p):
    A = np.array(A, dtype=np.int64) % p
    r = 0
    for c in range(A.shape[1]):
        pr = next((i for i in range(r, A.shape[0]) if A[i, c]), None)
        if pr is None:
            continue
        A[[r, pr]] = A[[pr, r]]
        A[r] = A[r] * pow(int(A[r, c]), p - 2, p) % p
        for i in range(A.shape[0]):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
    return r

def mat_exp(x, p):
    N = x.shape[0]
    out = np.eye(N, dtype=np.int64); term = np.eye(N, dtype=np.int64); fact = 1
    for j in range(1, p):
        term = (term @ x) % p; fact = fact * j % p
        out = (out + term * pow(fact, p - 2, p)) % p
    return out

def study(p, D, Delta):
    A = np.eye(D, k=1, dtype=np.int64)
    ginv = mat_exp((-A) % p, p)
    mons = monomials(D, Delta)
    idx = {m: i for i, m in enumerate(mons)}
    n = len(mons)
    T = np.zeros((n, n), dtype=np.int64)    # column i: image of monomial i under F -> F(g^-1 x)
    Dm = np.zeros((n, n), dtype=np.int64)   # column i: A.(x^alpha)
    for i, m in enumerate(mons):
        for k, v in subst(m, ginv, p).items():
            T[idx[k], i] = (T[idx[k], i] + v) % p
        # derivative: sum_k alpha_k x^(alpha - e_k) (A x)_k, (A x)_k = x_{k+1}
        for kk in range(D - 1):
            if m[kk]:
                b = list(m); b[kk] -= 1; b[kk + 1] += 1
                Dm[idx[tuple(b)], i] = (Dm[idx[tuple(b)], i] + m[kk]) % p
    I = np.eye(n, dtype=np.int64)
    fix_dim = n - rank_mod((T - I) % p, p)
    ker_dim = n - rank_mod(Dm, p)
    inter_dim = n - rank_mod(np.concatenate([(T - I) % p, Dm], axis=0), p)
    return n, fix_dim, ker_dim, inter_dim

if __name__ == "__main__":
    for p, D in [(3, 3), (5, 3), (5, 4), (5, 5), (7, 3), (7, 4)]:
        for Delta in range(1, p):
            n, f, k, i = study(p, D, Delta)
            hyp = p > max(D, (D - 1) * Delta)
            status = "equal" if f == k == i else f"DIFFER (Fix\\Ker dim {f - i}, Ker\\Fix dim {k - i})"
            print(f"p={p} D={D} Delta={Delta} hyp p>max(D,(D-1)Delta)={hyp}: forms={n} dimFix={f} dimKer={k} dimFix∩Ker={i} -> {status}")
