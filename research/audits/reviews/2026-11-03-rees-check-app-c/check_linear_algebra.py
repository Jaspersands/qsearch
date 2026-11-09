"""Item 3 (campaign 4): high-precision checks of the linear algebra in appendix-subspace.tex.

Covers Lemma app-sub-gram (a)-(c), Lemma app-sub-angles (three identities) and
Proposition app-sub-ray (a)-(c), in mpmath at 40 digits on random complex data.
Also checks that phi(g) = <Omega_V|U^{(x)r}|Omega_V> = det(Y^dag U Y), the
closed form used by check_lift.py.

Run: /opt/anaconda3/bin/python check_linear_algebra.py
"""
import itertools
import random
import sys

from mpmath import mp, mpc, mpf, matrix, sqrt, fabs, log10

mp.dps = 40
random.seed(20261103)
TOL = mpf(10) ** -30


def rand_c():
    return mpc(random.gauss(0, 1), random.gauss(0, 1))


def rand_mat(a, b):
    return matrix([[rand_c() for _ in range(b)] for _ in range(a)])


def orthonormal_frame(d, r):
    q, _ = mp.qr(rand_mat(d, r))
    return q[:, :r] if q.cols > r else q


def dag(x):
    return x.H


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


def kron_vecs(vs):
    out = [mpc(1)]
    for v in vs:
        out = [a * v[i] for a in out for i in range(len(v))]
    return out


def wedge(vs):
    """(k!)^{-1/2} sum_pi sgn(pi) v_pi(1) x ... x v_pi(k), as a flat list."""
    k = len(vs)
    n = len(vs[0]) ** k
    acc = [mpc(0)] * n
    for p in itertools.permutations(range(k)):
        t = kron_vecs([vs[p[i]] for i in range(k)])
        sg = perm_sign(p)
        acc = [a + sg * b for a, b in zip(acc, t)]
    f = 1 / sqrt(mp.factorial(k))
    return [f * a for a in acc]


def ip(u, w):
    return sum(mp.conj(a) * b for a, b in zip(u, w))


def col(m, j):
    return [m[i, j] for i in range(m.rows)]


def apply_tensor(U, vec, k):
    """U^{(x)k} applied to a flat vector on (C^d)^{(x)k}."""
    d = U.rows
    cur = list(vec)
    for pos in range(k):
        new = [mpc(0)] * len(cur)
        stride = d ** (k - 1 - pos)
        for idx in range(len(cur)):
            if cur[idx] == 0:
                continue
            digit = (idx // stride) % d
            base = idx - digit * stride
            for e in range(d):
                new[base + e * stride] += U[e, digit] * cur[idx]
        cur = new
    return cur


def trace_norm_herm(x):
    ev = mp.eighe(x)[0]
    return sum(fabs(e) for e in ev)


def random_unitary(d):
    q, _ = mp.qr(rand_mat(d, d))
    return q


worst = {}


def rec(name, val):
    worst[name] = max(worst.get(name, mpf(0)), fabs(val))


def main():
    n_cases = 0
    for d in range(2, 6):
        for r in range(1, d + 1):
            if d ** r > 1100:
                continue
            for _ in range(6):
                n_cases += 1
                k = r
                # Lemma gram (a): two arbitrary k-tuples.
                us = [col(rand_mat(d, 1), 0) for _ in range(k)]
                ws = [col(rand_mat(d, 1), 0) for _ in range(k)]
                G = matrix([[ip(us[i], ws[j]) for j in range(k)] for i in range(k)])
                rec("gram_a", ip(wedge(us), wedge(ws)) - mp.det(G))
                # Lemma gram (b): arbitrary linear X.
                X = rand_mat(d, d)
                lhs = apply_tensor(X, wedge(ws), k)
                Xw = [col(X * matrix(w), 0) for w in ws]
                rhs = wedge(Xw)
                rec("gram_b", max(fabs(a - b) for a, b in zip(lhs, rhs)))
                # Lemma gram (c): frame change by an arbitrary k x k matrix Z.
                Z = rand_mat(k, k)
                ys = ws
                comb = [[sum(Z[i, j] * ys[i][e] for i in range(k)) for e in range(d)] for j in range(k)]
                lhs = wedge(comb)
                rhs = [mp.det(Z) * a for a in wedge(ys)]
                rec("gram_c", max(fabs(a - b) for a, b in zip(lhs, rhs)))

                # Lemma angles, Prop ray.
                Y = orthonormal_frame(d, r)
                U = random_unitary(d)
                Yp = U * Y  # frame of UV
                M = dag(Y) * Yp
                sv = mp.svd_c(M, compute_uv=False)
                cos = [min(mpf(1), fabs(s)) for s in sv]
                PV = Y * dag(Y)
                # sin(theta_i) = singular values of (I - Pi_V) Y' (no cancellation near theta = 0)
                svs = mp.svd_c((mp.eye(d) - PV) * Yp, compute_uv=False)
                sin = sorted([fabs(s) for s in svs], reverse=True)
                rec("sin2_plus_cos2", max(fabs(a * a + b * b - 1) for a, b in zip(sorted(cos), sin)))
                PW = Yp * dag(Yp)
                td_proj = trace_norm_herm(PV - PW) / 2
                rec("angles_td", td_proj - sum(sin))
                rec("angles_tr", mp.re(sum((PV * PW)[i, i] for i in range(d))) - sum(c * c for c in cos))
                Om = wedge([col(Y, j) for j in range(r)])
                Omp = wedge([col(Yp, j) for j in range(r)])
                prod_cos = mpf(1)
                for c in cos:
                    prod_cos *= c
                rec("angles_det", fabs(ip(Om, Omp)) - prod_cos)
                # Prop ray (a): U^{(x)r} Omega_V = phase * Omega_{UV}
                UOm = apply_tensor(U, Om, r)
                ov = ip(Omp, UOm)
                rec("ray_a_phase", fabs(ov) - 1)
                # phi(g) closed form
                phi = ip(Om, UOm)
                rec("phi_det_form", phi - mp.det(dag(Y) * U * Y))
                # Prop ray (c) chain: prod cos <= (1-mu)^{r/2} <= sqrt(1-TD^2) <= 1-TD^2/2
                mu = 1 - mp.re(sum((PV * U * PV * dag(U))[i, i] for i in range(d))) / r
                td = td_proj / r
                rec("mu_vs_mean_sin2", mu - sum(s * s for s in sin) / r)
                chain = [prod_cos, (1 - mu) ** (mpf(r) / 2), sqrt(1 - td ** 2), 1 - td ** 2 / 2]
                for a, b in zip(chain, chain[1:]):
                    if a > b + TOL:
                        print("CHAIN VIOLATION", d, r, chain)
                        sys.exit(1)
                if mu + TOL < td ** 2:
                    print("mu < TD^2 VIOLATION", d, r)
                    sys.exit(1)

                # Prop ray (a) in the stabilizer: U = block unitary preserving V.
                if r < d:
                    full, _ = mp.qr(rand_mat(d, d))
                    Yfull = full  # columns: first r span V
                    A = random_unitary(r)
                    Bm = random_unitary(d - r)
                    blk = mp.zeros(d, d)
                    for i in range(r):
                        for j in range(r):
                            blk[i, j] = A[i, j]
                    for i in range(d - r):
                        for j in range(d - r):
                            blk[r + i, r + j] = Bm[i, j]
                    Ust = Yfull * blk * dag(Yfull)
                    Yv = Yfull[:, :r]
                    Omv = wedge([col(Yv, j) for j in range(r)])
                    UO = apply_tensor(Ust, Omv, r)
                    chi = mp.det(dag(Yv) * Ust * Yv)
                    rec("ray_a_stab_phase", max(fabs(a - chi * b) for a, b in zip(UO, Omv)))
                    rec("ray_a_det_eq_detA", chi - mp.det(A))
    print(f"cases: {n_cases} (d = 2..5, r <= d, d^r <= 1100), mp.dps = {mp.dps}")
    ok = True
    for k, v in worst.items():
        flag = "ok" if v < TOL else "FAIL"
        ok &= v < TOL
        print(f"  {k:20s} max |err| = {mp.nstr(v, 3)}  {flag}")
    print("ALL OK" if ok else "SOME FAILURES")


if __name__ == "__main__":
    main()
