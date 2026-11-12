#!/opt/anaconda3/bin/python
r"""Exact computation for Schedule 1H (Schedule 1 with halving) as written into the core paper
on 2026-11-13 (AI-run, pending human review). Finite computation: it can falsify, it proves
nothing asymptotic by itself.

Rule (exactly the paper's Definition of Schedule 1H):
  kappa = 1: Gaussian elimination, arity a+1, degree 1, constant 1.
  kappa >= 2, kappa | p-1: Schedule 1 at kappa, arity G(kappa,a)^L, L = ceil(log2 t_{p,kappa}),
      degree kappa*L, constant kappa^{kappa(kappa-1)L/2}.
  kappa even, D = kappa/2, inner solver = Schedule 1H at D (arity A(D,a), degree e(D)):
      if p >= 4 kappa^4: one stage + finish F1 (valid by Hasse-Weil), arity (a+1)A(D,a),
                         degree e(D)+1;
      if p <  4 kappa^4: s >= 1 stages + finish F0 (if 0 in T_s) or F1 (if T_s contains F_p^*),
                         arity A(D,a)^s or A(D,a)^s (a+1), degree s e(D) (+1 for F1),
      where T_0 = P (nonzero kappa-th powers), T_s = T_{s-1} u eps T_{s-1} u (T_{s-1}+eps T_{s-1}),
      eps = -1/q, q any element of class kappa/2 (q^{(p-1)/kappa} = -1).
  Arity A(kappa,a) = least arity over the plans (computed with the inner A(D,a));
  degree e(kappa) = least degree over the plans (computed with the inner e(D));
  constant K(kappa) = least constant over the degree-optimal plans (K(D)^s for halving plans).
Exponent E_H(c) = 1 + max_{p>c} sum_{d=2}^c e(gcd(d,p-1)).
Exact class sumsets for every prime p < 26244 = 4*9^4; for p >= 26244 all kappa <= 9 are in the
Hasse-Weil regime and the values depend only on p mod 5040 (all 1152 units evaluated).
Also: exact check of T_1 = F_p^* and of t <= 3 on every prime in [4 kappa^4, 30000] (falsifier of
the Weil step), the crossover table (classical_lb.py imported read-only), the class-9 profile.

Run: nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-headline-38-applied/halved_schedule.py
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SMALL = 4 * 9 ** 4  # 26244
CHECK_TO = 30000
AS = [1, 2, 3, 4, 6, 9, 12, 14, 16, 17]


def sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return [int(x) for x in np.nonzero(s)[0]]


PRIMES = sieve(CHECK_TO)


def prim_root(p):
    m, fac, q = p - 1, [], 2
    while q * q <= m:
        if m % q == 0:
            fac.append(q)
            while m % q == 0: m //= q
        q += 1
    if m > 1: fac.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // f, p) != 1 for f in fac):
            return g
    return 1  # p = 2, 3 handled (p=3 -> g=2 found above)


class Field:
    def __init__(self, p):
        self.p = p
        g = prim_root(p)
        self.log = np.zeros(p, dtype=np.int64)
        self.pw = np.zeros(p - 1, dtype=np.int64)
        x = 1
        for k in range(p - 1):
            self.log[x] = k; self.pw[k] = x; x = x * g % p
        self.ar = np.arange(p)

    def mask(self, kappa, cls, zero):
        m = np.zeros(self.p, dtype=bool)
        if cls:
            m[1:] = np.isin(self.log[1:] % kappa, sorted(cls))
        m[0] = zero
        return m

    def sumset(self, kappa, A, B):
        """A, B: (frozenset of classes mod kappa, zero flag), P_kappa-invariant sets. Returns A+B."""
        mA, mB = self.mask(kappa, *A), self.mask(kappa, *B)
        cls = set()
        for j in range(kappa):
            eta = int(self.pw[j])
            if np.any(mA & mB[(eta - self.ar) % self.p]): cls.add(j)
        zero = bool(np.any(mA & mB[(-self.ar) % self.p]))
        return (frozenset(cls), zero)


def t_len(F, kappa):
    P = (frozenset([0]), False)
    S, t = P, 1
    while True:
        S = F.sumset(kappa, S, P); t += 1
        if S[1]: return t
        if t > kappa + 1: raise RuntimeError("Chevalley-Warning violated")


def G(k, a): return k ** (k * (k - 1) // 2) * (a + 1) ** k


def cconst(k):  # d^{d(d-1) ceil(log2(d+1))/2}, the per-grade constant of thm:main(4)
    return k ** (k * (k - 1) * math.ceil(math.log2(k + 1)) // 2)


def T_sequence(F, kappa, smax):
    """T_1..T_smax as (classes, zero) for the type sequence c -> (c, eps c)."""
    p = F.p
    cl_m1 = ((p - 1) // 2) % kappa
    cl_eps = (cl_m1 - kappa // 2) % kappa
    T = (frozenset([0]), False)
    out = []
    for _ in range(smax):
        sh = (frozenset((x + cl_eps) % kappa for x in T[0]), T[1])
        ss = F.sumset(kappa, T, sh)
        T2 = (T[0] | sh[0] | ss[0], T[1] or sh[1] or ss[1])
        if out and T2 == out[-1]:
            break  # stabilized: larger s only adds arity
        T = T2
        out.append(T)
    return out


def tables_for_prime(p, F=None, exact_all=False):
    """Return dict kappa -> {'t','e','K','plan','A':{a:arity},'Aplan':{a:plan}} for kappa | p-1, kappa<=9.
    exact_all: use the exact T_s rule also for p >= 4 kappa^4 (consistency check only)."""
    need_F = (p < SMALL) or exact_all
    if F is None and need_F: F = Field(p)
    res = {}
    for kappa in range(1, 10):
        if (p - 1) % kappa: continue
        if kappa == 1:
            res[1] = {'t': None, 'e': 1, 'K': 1, 'plan': 'GE', 'A': {a: a + 1 for a in AS},
                      'Aplan': {a: 'GE' for a in AS}}
            continue
        if F is not None:
            t = t_len(F, kappa)
        else:  # p >= 26244: Lemma zero-sum-length (ii),(iii)
            t = 2 if ((p - 1) // kappa) % 2 == 0 else 3
        L = math.ceil(math.log2(t))
        e_best, K_best, plan = kappa * L, kappa ** (kappa * (kappa - 1) * L // 2), 'S1'
        A = {a: G(kappa, a) ** L for a in AS}
        Aplan = {a: 'S1' for a in AS}
        if kappa % 2 == 0:
            D = kappa // 2
            inner = res[D]
            if p >= 4 * kappa ** 4 and not exact_all:
                cand = [(1, 'F1')]
                if F is not None:  # exact falsifier of the Hasse-Weil step below 26244
                    T1 = T_sequence(F, kappa, 1)[0]
                    assert len(T1[0]) == kappa, ("Weil step falsified", p, kappa)
            else:
                if F is None: F = Field(p)
                smax = 40
                Ts = T_sequence(F, kappa, smax)
                cand = []
                for s, T in enumerate(Ts, start=1):
                    if T[1]: cand.append((s, 'F0'))
                    if len(T[0]) == kappa: cand.append((s, 'F1'))
                if p >= 4 * kappa ** 4:  # Weil prediction must hold
                    assert len(Ts[0][0]) == kappa, ("Weil step falsified", p, kappa)
            for s, fin in cand:
                deg = s * inner['e'] + (1 if fin == 'F1' else 0)
                Kc = inner['K'] ** s
                if deg < e_best or (deg == e_best and Kc < K_best):
                    e_best, K_best, plan = deg, Kc, f'{s}x{fin}'
                for a in AS:
                    ar = inner['A'][a] ** s * ((a + 1) if fin == 'F1' else 1)
                    if ar < A[a]:
                        A[a], Aplan[a] = ar, f'{s}x{fin}'
        res[kappa] = {'t': t, 'e': e_best, 'K': K_best, 'plan': plan, 'A': A, 'Aplan': Aplan}
    return res


def tail_tables(r):
    """Tables for a prime p > 26244 with p = r (mod 5040). Uses only p-1 mod 5040."""
    pm1 = (r - 1) % 5040
    fake_p = 5040 * 10 + r  # any representative >= 26244 with the same residue (used only via p-1)
    # tables_for_prime only uses (p-1) % kappa and ((p-1)//kappa) % 2 when F is None and p >= SMALL
    assert fake_p >= SMALL and (fake_p - 1) % 5040 == pm1
    return tables_for_prime(fake_p)


PROFILES = [("Heisenberg", 2, 3, {2: 1}), ("filiform", 3, 4, {2: 2, 3: 1}),
            ("free, two generators", 3, 5, {2: 3, 3: 2}), ("Dixmier--Lister", 3, 8, {2: 4, 3: 2}),
            ("class-9 profile", 9, 19, {2: 17, 3: 16, 4: 14, 5: 12, 6: 9, 7: 6, 8: 3, 9: 1})]


def main():
    E = {c: [0, []] for c in range(2, 10)}
    Eold = {c: [0, []] for c in range(2, 10)}
    prof = {name: [0, []] for name, *_ in PROFILES}
    Kviol, smax_used, weil_fail, t_fail = [], 0, [], []
    plan_examples = {}
    for p in PRIMES:
        if p < 3: continue
        if p < SMALL:
            tab = tables_for_prime(p)
        else:
            # exact consistency check in [26244, 30000]: exact rule must agree with the formula
            tab = tables_for_prime(p)
            ex = tables_for_prime(p, exact_all=True)
            for k in tab:
                if k > 1 and (tab[k]['e'] != ex[k]['e'] or tab[k]['t'] != ex[k]['t']):
                    weil_fail.append((p, k, tab[k]['e'], ex[k]['e'], tab[k]['t'], ex[k]['t']))
        for k, v in tab.items():
            if k > 1 and v['K'] > cconst(k): Kviol.append((p, k, v['K']))
            if 'x' in v['plan']: smax_used = max(smax_used, int(v['plan'].split('x')[0]))
            if k > 1 and p >= 4 * k ** 4 and v['t'] is not None and v['t'] > 3: t_fail.append((p, k))
        if p in (3, 5, 7, 13, 17, 31, 37, 41, 61, 73, 2521):
            plan_examples[p] = {k: (v['e'], v['plan']) for k, v in tab.items()}
        for c in range(2, 10):
            if p <= c: continue
            val = 1 + sum(tab[math.gcd(d, p - 1)]['e'] for d in range(2, c + 1))
            old = 1 + sum((math.gcd(d, p - 1) * math.ceil(math.log2(tab[math.gcd(d, p - 1)]['t'])))
                          if math.gcd(d, p - 1) > 1 else 1 for d in range(2, c + 1))
            for store, v in ((E, val), (Eold, old)):
                if v > store[c][0]: store[c] = [v, [p]]
                elif v == store[c][0]: store[c][1].append(p)
        if p >= 11:
            for name, c, m, g in PROFILES:
                Q = c * (m + 1) * math.prod(tab[math.gcd(d, p - 1)]['A'][g[d]] for d in range(2, c + 1))
                if Q > prof[name][0]: prof[name] = [Q, [p]]
                elif Q == prof[name][0] and len(prof[name][1]) < 50: prof[name][1].append(p)
        if p % 5000 < 3: print('p =', p, flush=True)
    # tail: p >= 26244 (in fact > 30000 beyond the checked range), residues mod 5040
    tailE = {c: [0, []] for c in range(2, 10)}
    tailP = {name: [0, []] for name, *_ in PROFILES}
    for r in range(1, 5040):
        if math.gcd(r, 5040) != 1: continue
        tab = tail_tables(r)
        for k, v in tab.items():
            if k > 1 and v['K'] > cconst(k): Kviol.append(('tail', r, k, v['K']))
        for c in range(2, 10):
            val = 1 + sum(tab[math.gcd(d, (r - 1) % 5040 or 5040)]['e'] for d in range(2, c + 1))
            if val > tailE[c][0]: tailE[c] = [val, [r]]
            elif val == tailE[c][0]: tailE[c][1].append(r)
        for name, c, m, g in PROFILES:
            Q = c * (m + 1) * math.prod(tab[math.gcd(d, (r - 1) % 5040 or 5040)]['A'][g[d]]
                                        for d in range(2, c + 1))
            if Q > tailP[name][0]: tailP[name] = [Q, [r]]
            elif Q == tailP[name][0]: tailP[name][1].append(r)
    EH = {c: max(E[c][0], tailE[c][0]) for c in E}
    out = {'E_H_exact_range': E, 'E_H_tail_residues': {c: [v[0], v[1][:6], len(v[1])] for c, v in tailE.items()},
           'E_H': EH, 'E_1_control': {c: Eold[c][0] for c in Eold},
           'E_1_control_attained_9': Eold[9][1],
           'constant_violations_K_gt_cd': Kviol[:20], 'n_constant_violations': len(Kviol),
           'max_stages_in_degree_optimal_plans': smax_used,
           'weil_regime_exact_disagreements_26244_30000': weil_fail[:10],
           't_gt_3_above_4kappa4': t_fail[:10],
           'plan_examples': plan_examples}
    # crossover table
    spec = importlib.util.spec_from_file_location(
        "classical_lb", ROOT / "research/audits/reviews/2026-11-02-rees-classical-lower-bound/classical_lb.py")
    CL = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(Path(spec.origin).parent))
    spec.loader.exec_module(CL)

    def closed_Q_int(p, m, eps_num=1, eps_den=3):  # copy of birthday_crossover.closed_Q_int (8 ln 6 -> 15)
        t = 0
        while p ** t * eps_num < 2 * eps_den:
            t += 1
        ln = math.log(2 * eps_den / eps_num)
        w = max(2 * (1 + t), 15)
        return 5 * (m + t) + 16 * math.ceil(ln) + CL.isqrt_ceil(2 * w * p ** (m - 1))

    def closed_Q_exact8l(p, m):
        return CL.closed_form_Q(p, m, __import__('fractions').Fraction(1, 3))

    rows = []
    for name, c, m, g in PROFILES:
        Qe, Pe = prof[name]
        Qt, Rt = tailP[name]
        Qq = max(Qe, Qt)
        where = {'exact_range_max': str(Qe), 'exact_range_primes': Pe[:12], 'n_exact_range_primes': len(Pe),
                 'tail_max': str(Qt), 'tail_residues_mod5040': Rt[:12], 'n_tail_residues': len(Rt)}

        def ok(x):
            return CL.classical_lb(x, m) > Qq
        hi = 11
        while not ok(hi): hi *= 2
        lo = 11
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid): hi = mid
            else: lo = mid + 1
        px = lo
        while not CL.is_prime(px): px += 1
        lo2, hi2 = 11, 11
        while closed_Q_int(hi2, m) < Qq: hi2 *= 2
        while lo2 < hi2:
            mid = (lo2 + hi2) // 2
            if closed_Q_int(mid, m) >= Qq: hi2 = mid
            else: lo2 = mid + 1
        row = {'family': name, 'Q_q': str(Qq), 'log2_Q_q': round(math.log2(Qq), 2), 'where': where,
               'LB_crossover_prime': str(px) if px < 10 ** 12 else None, 'log2_LB_crossover': round(math.log2(px), 2),
               'birthday_below': str(lo2) if lo2 < 10 ** 12 else None, 'log2_birthday_below': round(math.log2(lo2), 2)}
        if m <= 8:
            q = 11
            while closed_Q_exact8l(q, m) < Qq: q += 1
            qq = q - 1
            while not CL.is_prime(qq): qq -= 1
            row['exact_8l_first_integer'] = q
            row['exact_8l_largest_prime_below'] = qq
        if m <= 8 or px < 2 ** 200:
            row['ehk_copies_at_crossover'] = CL.ehk_copies(px, m)
        rows.append(row)
    out['crossover'] = rows
    (HERE / 'halved_schedule.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'plan_examples'}, indent=1, default=str))
    print(json.dumps(out['plan_examples'], default=str))


if __name__ == '__main__':
    main()
