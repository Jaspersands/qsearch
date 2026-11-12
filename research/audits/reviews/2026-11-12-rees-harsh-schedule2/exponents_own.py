"""Exponent of m in Q = c(m+tau) prod_d M_d under per-grade solver rules (own code).

E(c,p) = 1 + sum_{d=2}^c e_d(p), e_d = degree in g_d of the arity chosen at grade d,
kappa = gcd(d, p-1).  Per-grade options (each available only where stated):
  LIN : kappa = 1                          -> 1            (lem:bezout / thm:power-sde(i))
  S1  : always                             -> k*ceil(log2(k+1))   (core Schedule 1, B_k)
  S1t : always (core 'Shorter zero sums')  -> k*ceil(log2 t(p,k))
  S2  : p >= 16 k^(2k+2)                   -> 2            (thm:power-sde(ii))
  TRI : p not in E_2(k)                    -> 2            (prop:triangular-sde)
Rules:  PAPER = {LIN,S1,S2};  TRI = PAPER+TRI;  TRIZS = TRI+S1t;  ZS = {LIN,S1,S1t,S2}.
E_2 membership comes from my own runs (*.out of e2dfs in this folder) and from T_A(k)
(prop:app-s2-TA, recomputed in thresholds.py).  Unknown membership is evaluated both ways:
'hi' treats unknown as member (upper bound on the worst case), 'lo' as non-member.
Usage: exponents_own.py PMAX
"""
import glob, math, os, sys
from math import gcd, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
TA = {2: 8.42358904396, 3: 79.0393961837, 4: 868.996497241, 5: 12657.5921642, 6: 233577.026543,
      7: 4941830.29927, 8: 117441562.029, 9: 3099365718.7}


def load_membership():
    mem = {k: {} for k in range(2, 10)}
    for fn in glob.glob(os.path.join(HERE, '*.out')):
        b = os.path.basename(fn)
        if not (b.startswith('ex_k') or b.startswith('hunt_k') or b.startswith('resolve_k') or b.startswith('bench')):
            continue
        k = None
        if not b.startswith('bench'):
            k = int(b.split('_')[1].split('.')[0][1:])
        for line in open(fn):
            parts = line.split()
            if len(parts) < 2 or parts[1] not in ('MEMBER', 'NONMEMBER'):
                continue
            p = int(parts[0])
            if b.startswith('bench'):
                continue  # raw benchmark mixes kappas; superseded by ex_/hunt_ files
            st = parts[1] == 'MEMBER'
            if p in mem[k] and mem[k][p] != st:
                raise SystemExit('conflict %d %d' % (k, p))
            mem[k][p] = st
    return mem


MEM = load_membership()


def _missing(fn):
    try:
        line = open(os.path.join(HERE, fn)).read().split('\n')[1]
    except OSError:
        return None
    return {int(x) for x in line.split(':')[1].split()}


# Witness coverage computed by my checker wcheck.c on stored repo witnesses (+ my own):
#   k=8: every prime = 1 mod 8 in (14281, ceil T_A(8)] has a verified witness;
#        in (4400, 20000] exactly the primes listed in wcheck_k8_low.out lack one.
#   k=9: in (6000, 9^9/2] exactly the primes listed in wcheck_k9_repo.out lack one.
MISS8 = _missing('wcheck_k8_low.out')
MISS9 = _missing('wcheck_k9_repo.out')
USE_REPO_WITNESSES = os.environ.get('OWN_ONLY') is None


def in_e2(k, p):
    """True / False / None (unknown)."""
    if k < 2:
        return False
    if p > TA[k]:
        return False
    v = MEM[k].get(p)
    if v is not None or not USE_REPO_WITNESSES:
        return v
    if k == 8 and p > 14281:
        return False
    if k == 8 and 4400 < p <= 20000 and MISS8 is not None:
        return None if p in MISS8 else False
    if k == 9 and 6000 < p <= 9 ** 9 // 2 and MISS9 is not None:
        return None if p in MISS9 else False
    return None


def sieve(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return s


def primroot(p):
    n, fs, d = p - 1, [], 2
    while d * d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fs.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // f, p) != 1 for f in fs):
            return g


_tcache = {}


def zero_sum_len(p, k):
    """Least t >= 2 with 0 a sum of t nonzero k-th powers (k | p-1, k < p-1 or not)."""
    key = (p, k)
    if key in _tcache:
        return _tcache[key]
    h = (p - 1) // k
    if h % 2 == 0:
        t = 2          # -1 = g^((p-1)/2) is a k-th power iff k | (p-1)/2
    elif p + 1 - (k - 1) * (k - 2) * math.sqrt(p) > 3 * k and k < p - 1:
        t = 3          # Weil bound on the Fermat curve x^k + y^k + z^k = 0 (t = 2 excluded above)
    else:
        g = primroot(p)
        gk = pow(g, k, p)
        P, x = [], 1
        for _ in range(h):
            P.append(x)
            x = x * gk % p
        reach = set(P)
        t = 1
        while 0 not in reach:
            reach = {(r + q) % p for r in reach for q in P}
            t += 1
        # t counts summands
    _tcache[key] = t
    return t


def clog2(n):
    return (n - 1).bit_length()


def grade_options(p, d):
    k = gcd(d, p - 1)
    if k == 1:
        return {'LIN': 1}
    o = {'S1': k * clog2(k + 1)}
    if p >= 16 * k ** (2 * k + 2):
        o['S2'] = 2
    o['S1t'] = k * clog2(zero_sum_len(p, k))
    m = in_e2(k, p)
    o['TRI'] = m  # membership flag
    return o


RULES = {'PAPER': ('LIN', 'S1', 'S2'), 'ZS': ('LIN', 'S1', 'S1t', 'S2'),
         'TRI': ('LIN', 'S1', 'S2', 'TRI'), 'TRIZS': ('LIN', 'S1', 'S1t', 'S2', 'TRI')}


def e_grade(p, d, rule, mode):
    o = grade_options(p, d)
    best = 10 ** 9
    for name in RULES[rule]:
        if name not in o:
            continue
        if name == 'TRI':
            m = o['TRI']
            if m is False or (m is None and mode == 'lo'):
                best = min(best, 2)
        else:
            best = min(best, o[name])
    return best


def main():
    s = sieve(PMAX)
    primes = [p for p in range(3, PMAX + 1) if s[p]]
    print('PMAX', PMAX)
    combos = [(r, m) for r in RULES for m in (('hi', 'lo') if 'TRI' in r else ('hi',))]
    best = {(r, m, c): (-1, None) for (r, m) in combos for c in range(2, 10)}
    for p in primes:
        for (r, m) in combos:
            E = 1
            for d in range(2, 10):
                E += e_grade(p, d, r, m)
                c = d
                if p > c and E > best[(r, m, c)][0]:
                    best[(r, m, c)] = (E, p)
    for (r, m) in combos:
        print(r, m, ' '.join('%d@%d' % best[(r, m, c)] for c in range(2, 10)))
    # specific primes
    for p in (41, 73, 1009, 2521):
        for rule in RULES:
            es = [e_grade(p, d, rule, 'hi') for d in range(2, 10)]
            print('p=%d %s hi e=%s E=%d' % (p, rule, es, 1 + sum(es)))
        print('p=%d kappas=%s t=%s E2=%s' % (p, [gcd(d, p - 1) for d in range(2, 10)],
              [zero_sum_len(p, gcd(d, p - 1)) if gcd(d, p - 1) > 1 else '-' for d in range(2, 10)],
              [in_e2(gcd(d, p - 1), p) for d in range(2, 10)]))
    # unknown-membership inventory up to PMAX
    for k in range(2, 10):
        unk = [p for p in primes if (p - 1) % k == 0 and p > 2 and in_e2(k, p) is None]
        mem = sorted(p for p, v in MEM[k].items() if v)
        print('k=%d members(own)=%d max=%s unknown<=PMAX=%d first_unknown=%s' %
              (k, len(mem), mem[-1] if mem else None, len(unk), unk[:3]))


if __name__ == '__main__':
    main()
