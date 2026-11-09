"""Exact S-boundary terms of the separable-type Fourier coefficients (kappa = 4, 5).

Normal form s_0 = inf, s_1 = 0, s_2 = 1 (all labelled S mod PGL_2 exactly once), T a labelled
kappa-tuple inside one S-bucket v (weight (b_v)_kappa), z in F_p minus (S u T).  With
  Gt_c(x) = prod_{j>=1} chi^{c_j}(s_j - x),   chi(x) = zeta^{ind x},
the invariant decomposition (topic note section 11) is
  n Fhat(r,c)/Fhat(0) = A(r,c) - bS(r) - bS(c),
  bS(c) = E_C1[ conj Gt_c(B_T) * ( sum_{j>=1, c_j=0} Gt_c(s_j) + [c_0 = 0] ) ],
and the one-sided check  f(c) = n Fhat(0,c)/Fhat(0) = a(c) - kappa - bS(c) with
  a(c) = E_C1[ conj Gt_c(B_T) * Lambda_c ],  Lambda_c = sum_{x in P^1 \ supp c} G_c(x).
Outputs, per labelled c (one per multiset is enough; all labellings are printed as a check):
  bS, a, f_check.   Usage: python bdry_terms.py k p1 [p2 ...]"""
import sys, os, itertools, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'osc-k5'))
from osc_k5 import primroot

def run(k, p):
    g = primroot(p)
    ind = np.full(p, -1, dtype=np.int64); x = 1
    for e in range(p - 1):
        ind[x] = e % k; x = x * g % p
    zeta = np.exp(2j * np.pi / k)
    K = k ** (k - 1)
    ms = sorted({tuple(sorted(v)) for v in itertools.product(range(k), repeat=k) if sum(v) % k == 0})
    # all labelled c with sum 0, grouped by multiset; use every labelling (checks label-independence)
    cs = [c for c in itertools.product(range(k), repeat=k) if sum(c) % k == 0 and any(c)]
    cs = np.array(cs, dtype=np.int64)                      # (nc, k)
    nc = len(cs)
    # character table on profiles v in Z_k^{k-1}: phase[c, v] = zeta^{<c', v>}
    allv = np.array(list(itertools.product(range(k), repeat=k - 1)), dtype=np.int64)  # v[0] = v_1 ...
    vidx = (allv * (k ** np.arange(k - 1))).sum(1)
    order = np.argsort(vidx); allv = allv[order]          # allv[key] has key = sum v_j k^(j-1)
    ph = zeta ** ((cs[:, 1:] @ allv.T) % k)                # (nc, K)
    num_b = np.zeros(nc, dtype=complex); num_a = np.zeros(nc, dtype=complex); num_inf = np.zeros(nc, dtype=complex)
    den = 0.0
    xs = np.arange(p)
    s3_range = range(2, p)
    if k == 4:
        forms = [(s3,) for s3 in s3_range]
    for s3 in s3_range:
        if k == 4:
            S4 = np.array([[s3]])                          # one form per s3
        else:
            s4 = np.array([t for t in range(2, p) if t != s3]); S4 = s4[:, None]
        nf = S4.shape[0]
        Sfin = np.concatenate([np.zeros((nf, 1), np.int64), np.ones((nf, 1), np.int64), np.full((nf, 1), s3)] + ([S4] if k == 5 else []), 1)  # (nf, k-1)
        # profiles of all x: ind(s_j - x)
        prof = ind[(Sfin[:, None, :] - xs[None, :, None]) % p]   # (nf, p, k-1)
        ok = (prof >= 0).all(2)
        key = (np.where(prof < 0, 0, prof) * (k ** np.arange(k - 1))).sum(2)
        key = np.where(ok, key, K)
        cnt = np.zeros((nf, K + 1))
        np.add.at(cnt, (np.repeat(np.arange(nf), p), key.ravel()), 1)
        b = cnt[:, :K]
        w = b * (b - 1) * (b - 2) * (b - 3) * (b - 4 if k == 5 else 1)
        if k == 4:
            w = b * (b - 1) * (b - 2) * (b - 3)
        den += w.sum()
        Wc = w @ ph.conj().T                               # (nf, nc): sum_v w_v conj zeta^{<c',v>}
        bhat = b @ ph.T                                    # (nf, nc): sum_v b_v zeta^{<c',v>}
        # Gt_c(s_j) for finite s_j with c_j = 0: prod_{j' != j, j'>=1} chi^{c_j'}(s_j' - s_j)
        beta = np.zeros((nf, nc), dtype=complex)
        for j in range(1, k):
            dif = ind[(Sfin[:, :, None] - Sfin[:, None, j - 1:j]) % p][:, :, 0]   # (nf, k-1): ind(s_j' - s_j)
            # phase prod over j' != j of zeta^{c_j' * ind(s_j' - s_j)}
            e = np.zeros((nf, nc), dtype=np.int64)
            for jp in range(1, k):
                if jp == j: continue
                e = e + dif[:, jp - 1:jp] * cs[None, :, jp]
            val = zeta ** (e % k)
            beta += np.where(cs[None, :, j] == 0, val, 0)
        inf_term = np.where(cs[None, :, 0] == 0, 1.0, 0.0)  # [c_0 = 0] * Gt_c(inf) with Gt_c(inf) = 1
        Lam = bhat + beta                                   # affine complete sum over F_p (z = s_j with c_j != 0 give 0)
        num_b += (Wc * (beta + inf_term)).sum(0)
        num_a += (Wc * (Lam + inf_term)).sum(0)             # P^1 complete sum = affine + [c_0 = 0] * 1
    bS = num_b / den; a = num_a / den
    f_check = a - k - bS                                    # = n Fhat(0,c)/Fhat(0) if the bookkeeping is right
    name = lambda m: ''.join(str(x) for x in m if x) or '0'
    out = {}
    for i, c in enumerate(cs):
        out.setdefault(name(tuple(sorted(c))), []).append((complex(bS[i]), complex(a[i]), complex(f_check[i])))
    res = {}
    for m, L in out.items():
        B = np.array([l[0] for l in L]); A = np.array([l[1] for l in L]); Fc = np.array([l[2] for l in L])
        res[m] = dict(bS=[B.mean().real, B.mean().imag], bS_spread=float(abs(B - B.mean()).max()),
                      a=[A.mean().real, A.mean().imag], a_spread=float(abs(A - A.mean()).max()),
                      f=[Fc.mean().real, Fc.mean().imag])
    return res

if __name__ == '__main__':
    k = int(sys.argv[1])
    for p in map(int, sys.argv[2:]):
        r = run(k, p)
        print(json.dumps(dict(k=k, p=p, cls=r)), flush=True)
