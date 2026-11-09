"""Check the kernel identity for the (C1) count, with exact zero-cell / degenerate weights.

For e in Z_k^{k x k} put S_e = sum_{(alpha,beta) in F_p^{2k}} prod_{ij} chi^{e_ij}(alpha_j + beta_i),
convention chi^0(0) = 1, chi^s(0) = 0 (s != 0).  ker = {e : all row sums and column sums = 0 mod k}.

Claimed identities (the osc-N report (returned as text to the parent; no REPORT.md written) section 1):
 (I1)  k^{-(k-1)^2} sum_{e in ker} S_e = sum_{(alpha,beta)} k^{c(G)-1-z} [P separable on G]
       G = K_{k,k} minus the z zero cells, c(G) = number of components (isolated vertices included),
       P_ij = ind(alpha_j + beta_i) on nonzero cells.
 (I2)  k^{-(k-1)^2} sum_{e in ker} S_e = sum_{alpha in F_p^k} sum_{c in G_k} b_c(alpha)^k,
       b_c(alpha) = sum_t mu_t(c), mu_t = push-forward to Z_k^k/diag of (delta on coords with
       alpha_j != t) x (uniform on coords with alpha_j = t).
 (I3)  the open stratum count (alpha distinct, beta distinct, no zero cell, separable) is
       sum_{alpha distinct} sum_c (b'_c)_k, b'_c = #{t not in alpha : profile class c}.
Also prints the O1-N comparison: L1' = sum_{e in ker, e != 0}|S_e| versus S_0 - k^{(k-1)^2} W_deg etc.
Usage: python kernel_identity.py k p [skip]   (skip: omit the brute-force (I1); then W, W_deg print 0)
"""
import sys, itertools, math
import numpy as np


def primroot(p):
    n = p - 1; fac = []; d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac): return g


def main(k, p):
    g = primroot(p)
    ind = [-1] * p
    x = 1
    for e in range(p - 1):
        ind[x] = e % k; x = x * g % p
    om = np.exp(2j * np.pi / k)
    chi = np.zeros((k, p), dtype=complex)
    for s in range(k):
        for x in range(p):
            chi[s, x] = (1.0 if s == 0 else 0.0) if x == 0 else om ** ((s * ind[x]) % k)
    alphas = np.array(list(itertools.product(range(p), repeat=k)), dtype=np.int64)  # (p^k, k)
    rows = [r for r in itertools.product(range(k), repeat=k) if sum(r) % k == 0]
    ridx = {r: n for n, r in enumerate(rows)}
    # R[r, alpha] = sum_b prod_j chi^{r_j}(alpha_j + b)
    R = np.zeros((len(rows), len(alphas)), dtype=complex)
    for n, r in enumerate(rows):
        acc = np.zeros(len(alphas), dtype=complex)
        for b in range(p):
            pr = np.ones(len(alphas), dtype=complex)
            for j in range(k):
                pr = pr * chi[r[j], (alphas[:, j] + b) % p]
            acc += pr
        R[n] = acc
    # kernel frequencies: rows 0..k-2 free (row-sum 0), last row = -(sum) (automatically row-sum 0)
    tot = 0.0 + 0j
    L1 = 0.0
    S0 = None
    nker = 0
    for combo in itertools.product(range(len(rows)), repeat=k - 1):
        last = tuple((-sum(rows[c][j] for c in combo)) % k for j in range(k))
        pr = R[ridx[last]].copy()
        for c in combo:
            pr = pr * R[c]
        Se = pr.sum()
        nker += 1
        tot += Se
        if all(rows[c] == tuple([0] * k) for c in combo):
            S0 = Se
        else:
            L1 += abs(Se)
    assert nker == k ** ((k - 1) ** 2)
    lhs = tot / k ** ((k - 1) ** 2)
    # (I1) weighted count by brute force over F_p^{2k}
    W = 0.0; Wopen = 0; Wdeg = 0.0
    for a in (itertools.product(range(p), repeat=k) if not SKIP else []):
        for b in itertools.product(range(p), repeat=k):
            # union-find with potentials on 2k vertices: rows i -> i, cols j -> k+j
            par = list(range(2 * k)); pot = [0] * (2 * k)

            def find(v):
                if par[v] == v: return v, 0
                r, pv = find(par[v])
                par[v] = r; pot[v] = (pot[v] + pv) % k
                return r, pot[v]
            ok = True; z = 0
            for i in range(k):
                for j in range(k):
                    u = (a[j] + b[i]) % p
                    if u == 0:
                        z += 1; continue
                    # want U_i + V_j = ind(u); store potential phi(v) with phi(row)=U, phi(col)= -V
                    # constraint phi(i) - phi(k+j) = ind(u)
                    ri, pi_ = find(i); rj, pj = find(k + j)
                    if ri == rj:
                        if (pi_ - pj - ind[u]) % k != 0: ok = False
                    else:
                        par[ri] = rj; pot[ri] = (pj + ind[u] - pi_) % k
            if not ok: continue
            comps = len(set(find(v)[0] for v in range(2 * k)))
            w = float(k) ** (comps - 1 - z)
            W += w
            if z == 0 and len(set(a)) == k and len(set(b)) == k:
                Wopen += 1
            else:
                Wdeg += w
    # (I2)/(I3) bucket forms
    D = k ** (k - 1)
    pw = k ** np.arange(k)

    def cls(v):  # v: profile in Z_k^k -> class mod diagonal, index in [0, D)
        v = [(vi - v[0]) % k for vi in v]
        return sum(v[j] * k ** (j - 1) for j in range(1, k))
    I2 = 0.0; I3 = 0
    for a in itertools.product(range(p), repeat=k):
        bc = np.zeros(D)
        bint = np.zeros(D, dtype=np.int64)
        for t in range(p):
            zero = [j for j in range(k) if a[j] == t]
            base = [ind[(a[j] - t) % p] if a[j] != t else 0 for j in range(k)]
            if not zero:
                bc[cls(base)] += 1.0
                if len(set(a)) == k: bint[cls(base)] += 1
            else:
                wgt = float(k) ** (-len(zero))
                for fill in itertools.product(range(k), repeat=len(zero)):
                    v = list(base)
                    for jj, f in zip(zero, fill): v[jj] = f
                    bc[cls(v)] += wgt
        I2 += (bc ** k).sum()
        if len(set(a)) == k:
            ff = np.ones(D, dtype=np.int64)
            for s in range(k): ff = ff * (bint - s)
            I3 += int(ff.sum())
    mu_prime = p ** (2 * k) / k ** ((k - 1) ** 2)
    print(f'k={k} p={p}: |ker|={nker}  S_0={S0.real:.6g}  sum_ker S_e / k^((k-1)^2) = {lhs.real:.6f} (imag {lhs.imag:.1e})')
    print(f'  (I1) weighted count W = {W:.6f}   (I2) sum_alpha sum_c b_c^k = {I2:.6f}')
    print(f'  (I3) open C1 (labelled) = {Wopen}  bucket form = {I3}   W_deg = {Wdeg:.4f}')
    print(f'  mu\' = p^(2k)/k^((k-1)^2) = {mu_prime:.4f};  L1\' = {L1:.6g};  k^((k-1)^2)*(mu\'-W_deg) = {k**((k-1)**2)*(mu_prime-Wdeg):.6g}')
    print(f'  term-by-term lower bound on open count: k^-(k-1)^2 (S_0 - L1\') - W_deg = {(S0.real - L1)/k**((k-1)**2) - Wdeg:.4f}  (true {Wopen})')
    print(f'  barrier check: W_deg >= mu\' ? {Wdeg >= mu_prime}   p(p-1)^k = {p*(p-1)**k}')


SKIP = len(sys.argv) > 3  # third arg: skip the O(p^{2k}) brute force for (I1)
if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
