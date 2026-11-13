"""Second, independent check of every stored certificate (certs_stage1.json, tierB_witnesses.json).
Membership test written differently from certs.check_rc: x lies in xi^m P_D iff (x g^{-m})^{(p-1)/D} = 1,
with g recomputed here by trial (least primitive root via full order check)."""
import json, sys
def is_prim(g, p):
    x, n = 1, 0
    for n in range(1, p):
        x = x * g % p
        if x == 1: return n == p - 1
    return False
_g = {}
def lpr(p):
    if p not in _g:
        if p > 200000:   # full order check too slow; use factor test of p-1 instead
            n, fs, q = p - 1, [], 2
            while q * q <= n:
                if n % q == 0:
                    fs.append(q)
                    while n % q == 0: n //= q
                q += 1
            if n > 1: fs.append(n)
            g = 2
            while any(pow(g, (p - 1) // f, p) == 1 for f in fs): g += 1
        else:
            g = 2
            while not is_prim(g, p): g += 1
        _g[p] = g
    return _g[p]
def in_coset(x, m, D, p, g):
    return pow(x * pow(g, (-m) % (p - 1), p) % p, (p - 1) // D, p) == 1
def ok(p, g0, D, R, K, alpha, beta):
    g = lpr(p)
    if g != g0: return False
    if (alpha[0] + beta[0]) % p == 0 or not in_coset((alpha[0] + beta[0]) % p, 0, D, p, g): return False
    for i in R:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if v and not any(in_coset(v, (k - i - j) % D, D, p, g) for k in K): return False
    return True
C = json.load(open('certs_stage1.json'))
tot = bad = 0
for name, v in C.items():
    D, R = v['D'], v['R']
    for p, w in v['found'].items():
        p = int(p); be = {int(i): x for i, x in w['beta'].items()}
        Rl = sorted(be); tot += 1
        if sorted(set(r % D for r in R)) != Rl or not ok(p, w['g'], D, Rl, w['K'], w['alpha'], be): bad += 1; print('BAD', name, p)
    print(name, 'checked', len(v['found']), flush=True)
W = json.load(open('tierB_witnesses.json'))
for w in W:
    tot += 1
    be = {int(i): x for i, x in w['beta'].items()}
    if sorted(be) != sorted(w['R']) or not ok(w['p'], w['g'], w['D'], w['R'], w['K'], w['alpha'], be): bad += 1; print('BAD tierB', w)
print('total', tot, 'rejected', bad)
