#!/opt/anaconda3/bin/python
"""Finite exact check: can one set of measured targets feed TWO address registers?

Heisenberg group over F_p (p = 3, 5), coordinates (a,b,c), product
(a,b,c)*(a',b',c') = (a+a', b+b', c+c'+(ab'-ba')/2), dilation delta_s(a,b,c) = (sa, sb, s^2 c),
centre Z = {(0,0,c)}, Q = G/Z = F_p^2, section sigma(a,b) = (a,b,0).
Hidden subgroups: H = <x> = {(a,0,0)} (non-normal, H cap Z = 1) and others.

Single-register channel (core Prop. prop:descent): uniform |q>, apply R_{delta_{s_i}(sigma(q))} to each
active target, trace targets.  Expected output rho_{HZ/Z}.
Two-register variant: registers q, q'; target i gets R_{delta_{s_i}(sigma(q))} then
R_{delta_{s'_i}(sigma(q'))}, where s, s' are two solutions with a rank-2 matrix [s; s'].
Question: is the output rho_{HZ/Z} (x) rho_{HZ/Z}?  Finite check only.
"""
import itertools, sys
import numpy as np


def run(p, Hgens_kind):
    inv2 = pow(2, p - 2, p)
    G = [(a, b, c) for a in range(p) for b in range(p) for c in range(p)]
    idx = {g: i for i, g in enumerate(G)}

    def mul(x, y):
        return ((x[0] + y[0]) % p, (x[1] + y[1]) % p, (x[2] + y[2] + (x[0] * y[1] - x[1] * y[0]) * inv2) % p)

    def inv(x):
        return ((-x[0]) % p, (-x[1]) % p, (-x[2]) % p)

    def dil(s, x):
        return ((s * x[0]) % p, (s * x[1]) % p, (s * s * x[2]) % p)

    n = len(G)

    def R(g):  # |x> -> |x g>
        M = np.zeros((n, n), dtype=complex)
        for x in G:
            M[idx[mul(x, g)], idx[x]] = 1
        return M

    Rc = {g: R(g) for g in G}
    # hidden subgroup
    if Hgens_kind == 'x':
        H = {(a, 0, 0) for a in range(p)}
    elif Hgens_kind == 'x+y':
        H = {(a, a, 0) for a in range(p)}
    elif Hgens_kind == 'xz':  # <x, z>, normal, contains Z
        H = {(a, 0, c) for a in range(p) for c in range(p)}
    elif Hgens_kind == 'trivial':
        H = {(0, 0, 0)}
    rhoH = sum(Rc[h] for h in H) / n
    om = np.exp(2j * np.pi / p)

    def Pi(lam):
        return sum(om ** (-(lam * c) % p) * Rc[(0, 0, c)] for c in range(p)) / p

    rho_lab = {}
    for lam in range(p):
        P = Pi(lam)
        t = np.trace(P @ rhoH).real
        if t > 1e-12:
            rho_lab[lam] = (P @ rhoH @ P) / t
    Qs = [(a, b) for a in range(p) for b in range(p)]
    Hbar = {(h[0], h[1]) for h in H}
    nq = len(Qs)

    def RQ(qq):
        M = np.zeros((nq, nq), dtype=complex)
        for x in Qs:
            M[Qs.index(((x[0] + qq[0]) % p, (x[1] + qq[1]) % p)), Qs.index(x)] = 1
        return M

    rhoHbar = sum(RQ(h) for h in Hbar) / nq
    sig = lambda q: (q[0], q[1], 0)
    squares = {(x * x) % p for x in range(1, p)}
    labels = sorted(rho_lab)
    res = {'single_max_err': 0.0, 'double_min_err': None, 'double_max_err': 0.0, 'double_cases': 0}
    # all label pairs, all nonzero solution pairs on two targets
    for l1, l2 in itertools.product(labels, repeat=2):
        sols = [s for s in itertools.product(range(p), repeat=2) if s != (0, 0)
                and (s[0] * s[0] * l1 + s[1] * s[1] * l2) % p == 0]
        rl = [rho_lab[l1], rho_lab[l2]]
        # f_t(g) = tr(R_g rho_t); with R_g|x> = |xg>, R_a R_b = R_{ba}, R_a^dag = R_{a^-1}
        f = [{g: np.trace(Rc[g] @ rl[t]) for g in G} for t in range(2)]
        for s in sols:
            out = np.zeros((nq, nq), dtype=complex)
            for i, q in enumerate(Qs):
                for j, r in enumerate(Qs):
                    val = 1.0 + 0j
                    for t in range(2):
                        if s[t] == 0:
                            continue
                        u, v = dil(s[t], sig(q)), dil(s[t], sig(r))
                        val *= f[t][mul(u, inv(v))]
                    out[i, j] = val / nq
            res['single_max_err'] = max(res['single_max_err'], np.abs(out - rhoHbar).max())
        for s, s2 in itertools.product(sols, repeat=2):
            if (s[0] * s2[1] - s[1] * s2[0]) % p == 0:
                continue  # need rank 2
            target = np.kron(rhoHbar, rhoHbar)
            out = np.zeros((nq * nq, nq * nq), dtype=complex)
            pairs = [(q, q2) for q in Qs for q2 in Qs]
            for i, (q, q2) in enumerate(pairs):
                for j, (r, r2) in enumerate(pairs):
                    val = 1.0 + 0j
                    for t in range(2):
                        # Uq = R_{u2} R_{u1} = R_{u1 u2}; Ur^dag Uq = R_{u1 u2 (v1 v2)^-1}
                        u = mul(dil(s[t], sig(q)), dil(s2[t], sig(q2)))
                        v = mul(dil(s[t], sig(r)), dil(s2[t], sig(r2)))
                        val *= f[t][mul(u, inv(v))]
                    out[i, j] = val / (nq * nq)
            err = np.abs(out - target).max()
            overlap = any(s[t] and s2[t] for t in range(2))
            if overlap:
                tdist = float(0.5 * np.abs(np.linalg.eigvalsh(out - target)).sum())
                res.setdefault('overlap', []).append((l1, l2, s, s2, round(tdist, 4)))
            res['double_cases'] += 1
            res['double_max_err'] = max(res['double_max_err'], err)
            res['double_min_err'] = err if res['double_min_err'] is None else min(res['double_min_err'], err)
            # is it even a product state / does its trace-norm distance vanish?
            if res['double_cases'] == 1:
                res['example'] = (l1, l2, s, s2, float(0.5 * np.abs(np.linalg.eigvalsh(out - target)).sum()))
    return res


if __name__ == '__main__':
    todo = [(3, k) for k in ('x', 'x+y', 'xz', 'trivial')]  # p = 5 too slow in pure Python; not run
    for p, kind in todo:
        if True:
            r = run(p, kind)
            print('p=%d H=%-7s single-register max|out - rho_Hbar| = %.2e ; two-register cases=%d, '
                  'min/max entrywise err = %s/%.3f ; first case (l1,l2,s,s2,trace dist) = %s'
                  % (p, kind, r['single_max_err'], r['double_cases'],
                     None if r['double_min_err'] is None else '%.3f' % r['double_min_err'],
                     r['double_max_err'], r.get('example')))
            ov = r.get('overlap', [])
            bad = [o for o in ov if o[4] > 1e-9]
            print('   overlapping-support rank-2 pairs: %d, with trace distance > 1e-9 from rho(x)rho: %d; max %.4f; sample %s'
                  % (len(ov), len(bad), max([o[4] for o in ov] or [0]), bad[:3]))
            sys.stdout.flush()
