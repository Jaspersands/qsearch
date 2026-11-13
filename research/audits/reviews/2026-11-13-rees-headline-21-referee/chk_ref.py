"""Referee: third independent checker of every RC certificate/witness (Definition def:rc of fragment.tex).
Own primitive-root test, own class function (discrete log in the order-D subgroup by table of g^{(p-1)D^-1 c})."""
import json, sys, os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-13-rees-headline-below-38')

def pfactors(n):
    f, q = [], 2
    while q * q <= n:
        if n % q == 0:
            f.append(q)
            while n % q == 0: n //= q
        q += 1 if q == 2 else 2
    if n > 1: f.append(n)
    return f

LPR = {}
def least_prim_root(p):
    if p not in LPR:
        fs = pfactors(p - 1)
        g = 2
        while any(pow(g, (p - 1) // q, p) == 1 for q in fs): g += 1
        LPR[p] = g
    return LPR[p]

def class_table(p, g, D):
    z = pow(g, (p - 1) // D, p)
    return {pow(z, c, p): c for c in range(D)}

def check(p, g, D, R, K, alpha, beta):
    if (p - 1) % D: return 'D does not divide p-1'
    if g != least_prim_root(p): return 'g is not the least primitive root'
    R = sorted(set(R)); K = set(K)
    if 0 not in R or 0 not in K: return '0 missing'
    if len(alpha) != D or sorted(beta) != R: return 'shape'
    tab = class_table(p, g, D)
    e = (p - 1) // D
    a00 = (alpha[0] + beta[0]) % p
    if a00 == 0 or pow(a00, e, p) != 1: return 'alpha0+beta0 not in P_D'
    for i in R:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if v == 0: continue
            c = tab[pow(v, e, p)]
            if (c + i + j) % D not in K: return f'cell ({i},{j}) class {c}'
    return None

def main():
    C = json.load(open(os.path.join(SRC, 'certs_stage1.json')))
    expect = {'two-level 3': (3, list(range(3)), 'K1'), 'two-level 4': (4, list(range(4)), 'K1'),
              'two-level 5': (5, list(range(5)), 'K1'), 'tower (9;{0,3,6})': (9, [0, 3, 6], 'K1'),
              'union (7;Z7->{0,m})': (7, list(range(7)), 'K2')}
    tot = bad = 0
    for name, v in C.items():
        D, R, kk = expect[name]
        for ps, w in v['found'].items():
            p = int(ps); tot += 1
            K = w['K']
            if kk == 'K1' and K != [0]: bad += 1; print('K wrong', name, p, K); continue
            if kk == 'K2' and (len(K) != 2 or 0 not in K): bad += 1; print('K wrong', name, p, K); continue
            beta = {int(i): x for i, x in w['beta'].items()}
            r = check(p, w['g'], D, R, K, w['alpha'], beta)
            if r: bad += 1; print('REJECT', name, p, r)
        print(name, 'certs', len(v['found']), 'missing', v['missing'][:20] if isinstance(v['missing'], list) else v['missing'])
    W = json.load(open(os.path.join(SRC, 'tierB_witnesses.json')))
    for w in W:
        tot += 1
        beta = {int(i): x for i, x in w['beta'].items()}
        r = check(w['p'], w['g'], w['D'], w['R'], w['K'], w['alpha'], beta)
        if r: bad += 1; print('REJECT W', w['p'], w['D'], w['R'], w['K'], r)
    print('total', tot, 'rejected', bad)

if __name__ == '__main__':
    main()
