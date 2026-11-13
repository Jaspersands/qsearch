"""Referee: independent re-implementation of Schedule 1H+ degrees (Def. def:schedule1hplus of fragment.tex),
written from the fragment text, NOT from rule.py.  Uses only certificates/witnesses re-checked by chk_ref.py.
Class sumsets by cyclotomic data S_delta = {cl(1+y): y in Q_delta}, different method from halved_schedule.py."""
import json, math, os, sys
import numpy as np
from chk_ref import check, least_prim_root
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-13-rees-headline-below-38')
SMALL = 4 * 9 ** 4
TEX = {'TL3': 430, 'TL4': 9395, 'TL5': 99745, 'TW9': 1124521, 'U7': 1995734}   # recomputed by thr_ref.py
LIMIT = 2 * 10 ** 6
LMAX = int(os.environ.get('LMAX', '3'))

def sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return [int(x) for x in np.nonzero(s)[0]]

# ---------- certificates ----------
C = json.load(open(os.path.join(SRC, 'certs_stage1.json')))
NAME = {'two-level 3': ('TL3', 3, [0, 1, 2]), 'two-level 4': ('TL4', 4, [0, 1, 2, 3]),
        'two-level 5': ('TL5', 5, [0, 1, 2, 3, 4]), 'tower (9;{0,3,6})': ('TW9', 9, [0, 3, 6]),
        'union (7;Z7->{0,m})': ('U7', 7, list(range(7)))}
CERT = {}
for nm, v in C.items():
    tag, D, R = NAME[nm]; CERT[tag] = {}
    for ps, w in v['found'].items():
        p = int(ps); beta = {int(i): x for i, x in w['beta'].items()}
        assert check(p, w['g'], D, R, w['K'], w['alpha'], beta) is None
        CERT[tag][p] = w['K']
W = json.load(open(os.path.join(SRC, 'tierB_witnesses.json')))
EDGES = {}   # p -> set of (D, R, K)
for w in W:
    beta = {int(i): x for i, x in w['beta'].items()}
    if check(w['p'], w['g'], w['D'], w['R'], w['K'], w['alpha'], beta) is None:
        EDGES.setdefault(w['p'], set()).add((w['D'], frozenset(w['R']), frozenset(w['K'])))
TB_PRIMES = sorted({int(k.split('|')[0]) for k in json.load(open(os.path.join(SRC, 'tierB.json')))})

def avail(tag, p):
    if p >= TEX[tag]: return True
    return CERT[tag].get(p)          # K list or None

# ---------- class arithmetic ----------
class Cyc:
    def __init__(self, p):
        self.p = p; g = least_prim_root(p)
        lg = np.zeros(p, dtype=np.int64); x = 1
        for k in range(p - 1): lg[x] = k; x = x * g % p
        self.lg = lg; self.cache = {}
    def data(self, kap):
        if kap not in self.cache:
            p, lg = self.p, self.lg
            ys = np.arange(1, p); cl = lg[ys] % kap
            S, Z = [], []
            for d in range(kap):
                y = ys[cl == d]; z = (1 + y) % p
                Z.append(bool(np.any(z == 0)))
                S.append(frozenset(int(c) for c in np.unique(lg[z[z != 0]] % kap)))
            self.cache[kap] = (S, Z)
        return self.cache[kap]
    def add(self, kap, A, B):
        S, Z = self.data(kap)
        (CA, zA), (CB, zB) = A, B
        out, zero = set(), zA and zB
        for a in CA:
            for b in CB:
                out |= {(a + c) % kap for c in S[(b - a) % kap]}
                zero = zero or Z[(b - a) % kap]
        if zB: out |= CA
        if zA: out |= CB
        return (frozenset(out), zero)

def t_len(cyc, kap):
    P = (frozenset([0]), False); S = P
    for t in range(2, kap + 3):
        S = cyc.add(kap, S, P)
        if S[1]: return t
    raise AssertionError('Chevalley-Warning')

def T_list(cyc, kap, epscl):
    T = (frozenset([0]), False); out = []
    while True:
        eT = (frozenset((x + epscl) % kap for x in T[0]), T[1])
        s = cyc.add(kap, T, eT)
        T2 = (T[0] | eT[0] | s[0], T[1] or eT[1] or s[1])
        if out and T2 == out[-1]: return out
        out.append(T2); T = T2

def lift(K, D, D2): return frozenset(x for x in range(D2) if x % D in K)

def chains(p, kap, e):
    """Shortest-degree chain nodes (D,K) -> degree, over re-checked witnesses, at most LMAX steps."""
    E = EDGES.get(p, set())
    best = {(1, frozenset([0])): 1}
    for D in range(2, kap):
        if kap % D == 0: best[(D, frozenset([0]))] = min(best.get((D, frozenset([0])), 99), e[D])
    front = dict(best)
    for _ in range(LMAX):
        new = {}
        for (D, K), dg in front.items():
            for (D2, R, K2) in E:
                if kap % D2 or D2 % D or D2 < 2: continue
                if R != lift(K, D, D2) or len(R) < 2: continue
                if dg + 1 < min(best.get((D2, K2), 99), new.get((D2, K2), 99)): new[(D2, K2)] = dg + 1
        front = new; best.update(new)
        if not new: break
    return {K: dg for (D, K), dg in best.items() if D == kap}

def degrees(p, new=True):
    cyc = Cyc(p) if p < SMALL else None
    e, plan = {}, {}
    for kap in range(1, 10):
        if (p - 1) % kap: continue
        if kap == 1: e[1] = 1; plan[1] = 'GE'; continue
        t = t_len(cyc, kap) if p < SMALL else (2 if ((p - 1) // kap) % 2 == 0 else 3)
        cands = [(kap * math.ceil(math.log2(t)), 'S1')]
        two, knodes = [], []
        if kap % 2 == 0: two.append((kap // 2, e[kap // 2], 'half'))
        knodes.append((frozenset(range(kap)), 1, 'GE'))
        if new:
            for Dp in range(2, kap):
                if kap % Dp == 0: knodes.append((frozenset(range(0, kap, Dp)), e[Dp], f'S{Dp}'))
            if kap in (3, 4, 5) and avail(f'TL{kap}', p): cands.append((2, 'TL'))
            if kap == 9 and avail('TW9', p): cands.append((e[3] + 1, 'TW'))
            if kap == 7:
                a = avail('U7', p)
                if a is True: two.append((1, 2, 'U7sm'))
                elif a: two.append(([x for x in a if x][0], 2, 'U7'))
            if p in TB_PRIMES and kap >= 4:
                ch = chains(p, kap, e)
                for K, dg in ch.items():
                    if K == frozenset([0]): cands.append((dg, 'chain0'))
                    if len(K) == 2: two.append((max(K), dg, 'chain{0,%d}' % max(K)))
                    knodes.append((K, dg, 'K' + ','.join(map(str, sorted(K)))))
        for m, em, how in two:
            if p >= 4 * kap ** 4:
                cands.append((em + 1, how + ':1F1')); continue
            epscl = ((p - 1) // 2 - m) % kap
            for s, T in enumerate(T_list(cyc, kap, epscl), start=1):
                if T[1]: cands.append((s * em, f'{how}:{s}F0'))
                for K, dk, nm in knodes:
                    if any(all((u + k) % kap in T[0] for k in K) for u in range(kap)):
                        cands.append((s * em + dk, f'{how}:{s}F[{nm}]'))
        e[kap], plan[kap] = min(cands)
    return e, plan

def Eval(e, p, c): return 1 + sum(e[math.gcd(d, p - 1)] for d in range(2, c + 1))

if __name__ == '__main__':
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else LIMIT
    for new in (False, True):
        Em = {c: (0, []) for c in range(2, 10)}
        tops = []
        for p in sieve(lim):
            if p < 3: continue
            e, pl = degrees(p, new)
            for c in range(2, 10):
                if p <= c: continue
                v = Eval(e, p, c)
                if v > Em[c][0]: Em[c] = (v, [p])
                elif v == Em[c][0]: Em[c][1].append(p)
            if new and p > 9 and Eval(e, p, 9) >= 21 and p < 3000: tops.append((p, e, pl))
        print('new' if new else 'core-only', 'exact max p <', lim, {c: (v, ps[:8], len(ps)) for c, (v, ps) in Em.items()}, flush=True)
        if new:
            for p, e, pl in tops: print('  ', p, e, pl)
