"""New per-grade degrees (proved nodes only) and the class-c exponent E_new(c).
AI-written 2026-11-13, pending human review.  Finite computation plus the residue-class tail.

Candidates at (p, kappa), kappa | p-1, kappa <= 9, computed in increasing kappa:
  S1        Lemma rounds (core): kappa * ceil(log2 t_{p,kappa})                (kappa >= 2)
  GE        kappa = 1: 1
  TL        two-level contraction at kappa (Lemma C of the fragment, L = 1): 2
            kappa in {3,4,5}: certificate (checked) for p < T_exist(kappa), Lemma SM above
  TOWER     D | kappa, D-solver of degree e(D), step RC(kappa; D Z_kappa -> {0}): e(D) + 1
            implemented: (9; D = 3): certificate for p < 1124521, Lemma SM above
  STAGE     two-class node with classes {0, m} and degree e_m, then s stages and finish
            F0 (0 in T_s): s e_m ;  F1 (T_s contains F_p^*): s e_m + 1   (Lemmas S, F of the fragment;
            for kappa even and m = kappa/2 the node is the kappa/2-solver: the core's halving)
            p >= 4 kappa^4: only (1, F1), valid by the core's Lemma two-term (any eps).
            two-class nodes: kappa even: (kappa/2, e(kappa/2));  kappa = 7: union step
            RC(7; Z_7 -> {0,m}) of degree 2 (certificate for p < 1995734, Lemma SM above).
  Tier B (extra, only at the primes listed in tierB.json): chains with union targets, F_K finishes.
"""
import json, math, os, sys
from functools import lru_cache
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '2026-11-13-rees-headline-38-applied'))
import halved_schedule as HS   # read-only import: Field, t_len, tables_for_prime (core rule)

T_EXIST = {'TL3': 430, 'TL4': 9395, 'TL5': 99745, 'TW9': 1124521, 'U7': 1995734}
LIMIT = 2 * 10 ** 6   # above LIMIT (> every T_EXIST, > 26244) the residue-class tail applies
SMALL = 26244


def load_certs():
    C = json.load(open(os.path.join(HERE, 'certs_stage1.json')))
    key = {'two-level 3': 'TL3', 'two-level 4': 'TL4', 'two-level 5': 'TL5',
           'tower (9;{0,3,6})': 'TW9', 'union (7;Z7->{0,m})': 'U7'}
    out = {}
    for name, v in C.items():
        out[key[name]] = {int(p): w for p, w in v['found'].items()}
    return out


CERTS = None
TIERB = {}
# Lemmas K and D of 2026-11-13-rees-linear-arity.md (proved pending referee; bookkeeping variant only).
USE_KD = False
D_EXC = {4: {5: None, 13: None, 29: 4}, 5: {11: None}, 6: {7: None, 13: None, 19: None, 31: None, 43: None},
         7: {29: None, 71: None, 43: 7}, 8: {17: None, 41: None, 73: None, 89: None, 97: None, 137: None, 233: 5, 761: 5},
         9: {19: None, 37: None, 73: None, 109: 9, 163: 9}}   # degree m*+1 from tower_coverage.out
def D_deg(p, kappa):
    m = math.ceil(math.log2(kappa))
    if p >= 4 * kappa ** 4: return m + 1
    return D_EXC.get(kappa, {}).get(p, m + 1)
def avail(tag, p):
    """returns certificate dict / True if the node exists at p by Lemma SM, else None."""
    if p >= T_EXIST[tag]: return True
    return CERTS[tag].get(p)


def t_value(p, kappa, F):
    if F is not None: return HS.t_len(F, kappa)
    return 2 if ((p - 1) // kappa) % 2 == 0 else 3       # core Lemma zero-sum-length (ii),(iii)


def T_seq(F, kappa, eps_cls, smax=40):
    T = (frozenset([0]), False); out = []
    for _ in range(smax):
        sh = (frozenset((x + eps_cls) % kappa for x in T[0]), T[1])
        ss = F.sumset(kappa, T, sh)
        T2 = (T[0] | sh[0] | ss[0], T[1] or sh[1] or ss[1])
        if out and T2 == out[-1]: break
        T = T2; out.append(T)
    return out


def stage_plans(p, kappa, m, e_m, F, e, new=True):
    """least degree of the plans (s, F0 / F_K) over a {0,m}-node of degree e_m.
    Finishes F_K: a node whose relations have kappa-classes in K (0 in K), shifted by any c, with
    c + K inside the classes of T_s minus 0 (Lemma F of the fragment).  K-nodes used: D'-solvers for
    D' | kappa, D' < kappa (K = D' Z_kappa, degree e(D'); D' = 1 is Gaussian elimination = F1) and the
    Tier B chain K-nodes."""
    if p >= 4 * kappa ** 4:
        return e_m + 1, '1xF1'
    eps_cls = (((p - 1) // 2) - m) % kappa      # eps = -xi^{-m}, ind(-1) = (p-1)/2 w.r.t. a generator
    knodes = [(frozenset((Dp * i) % kappa for i in range(kappa // Dp)), e[Dp][0], f'S{Dp}')
              for Dp in range(1, kappa) if kappa % Dp == 0 and (new or Dp == 1)]
    for Kstr, dk in (TIERB.get((p, kappa, 'FK'), {}) if new else {}).items():
        knodes.append((frozenset(int(x) for x in Kstr.split(',')), dk, 'K' + Kstr))
    best, plan = 10 ** 9, None
    Ts = T_seq(F, kappa, eps_cls)
    for s, T in enumerate(Ts, start=1):
        if T[1] and s * e_m < best: best, plan = s * e_m, f'{s}xF0'
        C = set(T[0])
        for K, dk, nm in knodes:
            if s * e_m + dk >= best: continue
            if any({(c + k) % kappa for k in K} <= C for c in range(kappa)):
                best, plan = s * e_m + dk, f'{s}xF[{nm}]'
    return best, plan


def degrees(p, new=True, tierB=True):
    """dict kappa -> (degree, plan) for kappa | p-1, kappa <= 9."""
    F = HS.Field(p) if p < SMALL else None
    e = {}
    for kappa in range(1, 10):
        if (p - 1) % kappa: continue
        if kappa == 1: e[1] = (1, 'GE'); continue
        t = t_value(p, kappa, F)
        cands = [(kappa * math.ceil(math.log2(t)), 'S1')]
        two_class = []
        if USE_KD:
            if kappa == 3: cands.append((2, 'LemmaK'))
            dd = D_deg(p, kappa)
            if dd is not None: cands.append((dd, 'LemmaD'))
        if kappa % 2 == 0: two_class.append((kappa // 2, e[kappa // 2][0], 'half'))
        if new:
            if kappa in (3, 4, 5) and avail(f'TL{kappa}', p): cands.append((2, 'TL'))
            if kappa == 9 and avail('TW9', p): cands.append((e[3][0] + 1, 'TOWER3'))
            if kappa == 7:
                c7 = avail('U7', p)
                if c7 is True:
                    if p >= 4 * 7 ** 4: cands.append((3, 'U7+1xF1'))
                elif c7:
                    two_class.append((c7['K'][1], 2, 'U7'))
            if tierB:
                for (deg, plan) in TIERB.get((p, kappa, 'NODE0'), []): cands.append((deg, plan))
                for (m, deg, how) in TIERB.get((p, kappa, 'TWO'), []): two_class.append((m, deg, how))
        for m, e_m, how in two_class:
            if True:
                d, pl = stage_plans(p, kappa, m, e_m, F, e, new)
                cands.append((d, f'{how}:{pl}'))
        e[kappa] = min(cands)
    return e


def E_of(e, p, c):
    return 1 + sum(e[math.gcd(d, p - 1)][0] for d in range(2, c + 1))


TAIL = {1: 1, 2: 2, 3: 2, 4: 2, 5: 2, 6: 3, 7: 3, 8: 3, 9: 3}


def tail_check():
    """For p > LIMIT: e(kappa) = TAIL[kappa] (every node above its threshold, p >= 4*9^4), so E depends
    only on p mod 2520; returns c -> (max, residues mod 2520 attaining it)."""
    res = {}
    for c in range(2, 10):
        best, arg = 0, []
        for r in range(1, 2521):
            if math.gcd(r, 2520) != 1: continue
            v = 1 + sum(TAIL[math.gcd(d, r - 1 if r > 1 else 2520)] for d in range(2, c + 1))
            if v > best: best, arg = v, [r]
            elif v == best: arg.append(r)
        res[c] = (best, arg)
    return res


def main(limit=LIMIT, tierB=True, regress_to=SMALL):
    global CERTS, TIERB
    CERTS = load_certs()
    if tierB and os.path.exists(os.path.join(HERE, 'tierB.json')):
        raw = json.load(open(os.path.join(HERE, 'tierB.json')))
        for k, v in raw.items():
            p, kappa, kind = k.split('|'); TIERB[(int(p), int(kappa), kind)] = v
    # regression: with new=False the rule must reproduce the core's Schedule 1H degrees
    bad = []
    for p in HS.sieve(regress_to):
        if p < 3: continue
        old = HS.tables_for_prime(p)
        mine = degrees(p, new=False)
        for k in old:
            if old[k]['e'] != mine[k][0]: bad.append((p, k, old[k]['e'], mine[k][0]))
    print('regression vs core Schedule 1H below', regress_to, ': disagreements', bad[:10], len(bad), flush=True)
    Emax = {c: [0, []] for c in range(2, 10)}
    top9 = []
    for p in HS.sieve(limit) if limit <= 30000 else __import__('certs').primes_upto(limit):
        if p < 3: continue
        e = degrees(p, tierB=tierB)
        for c in range(2, 10):
            if p <= c: continue
            v = E_of(e, p, c)
            if v > Emax[c][0]: Emax[c] = [v, [p]]
            elif v == Emax[c][0]: Emax[c][1].append(p)
        if p > 9: top9.append((E_of(e, p, 9), p, {k: v for k, v in e.items()}))
    top9.sort(key=lambda x: -x[0])
    tail = tail_check()
    print('exact range max (p <', limit, '):', {c: (v[0], v[1][:12], len(v[1])) for c, v in Emax.items()})
    print('tail (p >', limit, '):', {c: (v[0], v[1][:6], len(v[1])) for c, v in tail.items()})
    print('E_new(c) =', {c: max(Emax[c][0], tail[c][0]) for c in range(2, 10)})
    print('class 9, top primes:')
    for v, p, e in top9[:40]:
        print(' ', v, p, {k: x for k, x in e.items()})
    return Emax, tail, top9


if __name__ == '__main__':
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else LIMIT
    tb = (sys.argv[2] != 'noB') if len(sys.argv) > 2 else True
    main(lim, tb)
