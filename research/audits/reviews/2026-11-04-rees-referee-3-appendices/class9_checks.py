"""Referee 3: independent recomputation of the class-nine numbers quoted in
appendix-free-coordinate.tex (Section app:fc-numbers) and appendix-schedule3.tex
(paragraph after Proposition prop:mixed-schedule), and of Table tab:fcs-budget.

Written from the statements in the appendices only; imports nothing from the
repository. Exact Fractions for every comparison that decides an arity; floats
only for the reported log2 values.

Run: /opt/anaconda3/bin/python -I class9_checks.py
"""
from fractions import Fraction as Fr
from math import gcd, log2, log, ceil
import sys

g = {1: 19, 2: 17, 3: 16, 4: 14, 5: 12, 6: 9, 7: 6, 8: 3, 9: 1}
m, c = 19, 9
eps = Fr(1, 3)
PRIMES = [11, 1031, 5281, 2**31 - 1, 2**61 - 1, 2**127 - 1]

def is_prime(n):
    if n < 2: return False
    small = [2,3,5,7,11,13,17,19,23,29,31,37]
    for q in small:
        if n % q == 0: return n == q
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

def clog2(x):
    x = Fr(x); k = 0
    while Fr(2) ** k < x: k += 1
    while k > 0 and Fr(2) ** (k - 1) >= x: k -= 1
    return k

def clogp(p, x):  # least j>=0 with p^j >= x
    j = 0
    while Fr(p) ** j < x: j += 1
    return j

def lg(x):  # log2 of a positive Fraction / int, float
    x = Fr(x)
    return log2(x.numerator) - log2(x.denominator)

def B_is(k, a):
    return (k ** (k * (k - 1) // 2) * (a + 1) ** k) ** clog2(k + 1)

def combined_arity(p, d):
    k = gcd(d, p - 1)
    if k == 1:
        return g[d] + 1, 'lin'
    if p >= 16 * k ** (2 * k + 2):
        return (g[d] + 1) * ((k - 1) * g[d] + 1), 'S2'
    return B_is(k, g[d]), 'S1'

def beta_fc(p, k, M, n0, a):
    h = (p - 1) // k
    q = Fr(h + 1, p)
    L = M - n0
    return Fr(4) / (Fr(h) ** (n0 - 1) * q ** a) + Fr(p ** a - 1, (p - 1) * p ** L)

def least_fc(p, k, ga, tau):
    """least M (and some n0) with beta(M,n0;ga) <= tau"""
    M = 1
    while True:
        for n0 in range(1, M + 1):
            if beta_fc(p, k, M, n0, ga) <= tau:
                return M, n0
        M += 1

def explicit_fc(p, k, ga, tau):
    h = (p - 1) // k
    q = Fr(h + 1, p)
    target = Fr(8) * q ** (-ga) / tau
    kk = 0
    while Fr(h) ** kk < target: kk += 1
    n0 = 1 + kk
    M = n0 + ga + clogp(p, Fr(2) / tau)
    assert beta_fc(p, k, M, n0, ga) <= tau
    return M, n0

def fc_iii(p, explicit=False):
    S = m + clogp(p, Fr(3) / eps)
    Ms, kinds, nd, n = {}, {}, {}, 1
    for d in range(2, c + 1):
        nd[d] = n
        k = gcd(d, p - 1)
        if k == 1:
            Ms[d], kinds[d] = g[d] + 1, 'lin'
        elif k == p - 1:
            Ms[d], kinds[d] = B_is(d, g[d]), 'S1'
        else:
            tau = eps / (9 * (c - 1) * S * n)
            Ms[d] = (explicit_fc if explicit else least_fc)(p, k, g[d], tau)[0]
            kinds[d] = 'F'
        n *= Ms[d]
    P = n
    N = S * sum(nd[d] for d in nd if kinds[d] == 'F')
    B = clog2(27 * N / eps) if N else 0
    caps, total = {}, 0.0
    for d in nd:
        if kinds[d] != 'F': continue
        k = gcd(d, p - 1); h = (p - 1) // k; q = Fr(h + 1, p)
        x = 2 * B * log(2) * float(q) ** (-g[d])  # cap ceil(x)
        caps[d] = log2(ceil(x))
        total += S * nd[d] * ceil(x)
    Q = c * S * P
    return dict(S=S, M=Ms, kinds=kinds, B=B, N=N, logQ=lg(Q),
                maxcap=max(caps.values()) if caps else None,
                argmax=max(caps, key=caps.get) if caps else None,
                logtotal=log2(total) if total else None)

def combined_Q(p):
    S = m + clogp(p, Fr(3) / eps)
    P = 1
    for d in range(2, c + 1):
        P *= combined_arity(p, d)[0]
    return lg(c * S * P)

def beta_s3(p, k, M, ga):
    h = (p - 1) // k
    return Fr(4 * h * p ** ga, (h + 1) ** M - 1) + Fr(p ** ga - 1, (p - 1) * p ** M)

def mixed_rule(p, force=None):
    """Instance of Prop. mixed-schedule described after it. Returns dict."""
    Ms, kinds = {}, {}
    for d in range(2, c + 1):
        Ms[d], kinds[d] = combined_arity(p, d)
        k = gcd(d, p - 1)
        u = max(2, k, g[d] + 1)
        if p >= 16 * u * u and 4 * u < Ms[d]:
            Ms[d], kinds[d] = 4 * u, 'S3'
    if force:
        for d, M in force.items():
            Ms[d], kinds[d] = M, 'S3'
    def nds():
        out, n = {}, 1
        for d in range(2, c + 1):
            out[d] = n; n *= Ms[d]
        return out, n
    added = {d: 0 for d in Ms}
    while True:
        nd, P = nds()
        terms = {d: nd[d] * beta_s3(p, gcd(d, p - 1), Ms[d], g[d]) for d in Ms if kinds[d] == 'S3'}
        lhs = sum(terms.values(), Fr(0))
        if lhs <= Fr(1, 64):
            break
        dmax = max(terms, key=terms.get)
        if sum(added.values()) == 0:
            first_lhs = lhs
        Ms[dmax] += 1; added[dmax] += 1
    nS3 = sum(nd[d] for d in Ms if kinds[d] == 'S3')
    nS2 = sum(nd[d] for d in Ms if kinds[d] == 'S2')
    B = clog2(64 * max(1, 3 * nS3 + nS2))
    mprime = m + clog2(Fr(3) / eps)
    Q = 4 * mprime * c * P
    trials = [log2(4 * B) + Ms[d] * log2(gcd(d, p - 1)) for d in Ms if kinds[d] == 'S3']
    abort = lhs + (3 * nS3 + nS2) * Fr(1, 2 ** B)
    return dict(M=Ms, kinds=kinds, added=added, lhs=lhs, B=B, logQ=lg(Q),
                logQ_cSP=lg(c * (m + clogp(p, Fr(3) / eps)) * P),
                trials=max(trials) if trials else None, abort=abort, nS3=nS3, nS2=nS2)

if __name__ == '__main__':
    print("=== Table tab:fcs-budget recomputation ===")
    for p in PRIMES:
        assert is_prime(p)
        r = fc_iii(p)
        re = fc_iii(p, explicit=True)
        mr = mixed_rule(p)
        print(f"p={p if p < 10**6 else 'log2~%.0f' % log2(p)}: combined logQ={combined_Q(p):.1f}")
        print(f"   (iii) least: logQ={r['logQ']:.1f} maxcap={r['maxcap']:.2f} at d={r['argmax']} B={r['B']} total={r['logtotal']:.1f} kinds={r['kinds']} M={r['M']}")
        print(f"   (iii) explicit: logQ={re['logQ']:.1f} (+{re['logQ']-r['logQ']:.2f}) maxcap={re['maxcap']:.2f} dM={ {d: re['M'][d]-r['M'][d] for d in r['M']} }")
        nS3 = [d for d in mr['kinds'] if mr['kinds'][d] == 'S3']
        if nS3:
            print(f"   mixed: S3 grades={nS3} logQ(4m'cP)={mr['logQ']:.1f} logQ(cSP)={mr['logQ_cSP']:.1f} trials={mr['trials']:.1f} B={mr['B']} lhs=2^{lg(mr['lhs']) if mr['lhs'] else float('-inf'):.1f} abort=2^{lg(mr['abort']):.2f} added={sum(mr['added'].values())} S2 grades={[d for d in mr['kinds'] if mr['kinds'][d]=='S2']}")
        else:
            print(f"   mixed: no S3 grade; S2 grades={[d for d in mr['kinds'] if mr['kinds'][d]=='S2']} abort=2^{lg(mr['abort']) if mr['abort'] else float('-inf'):.2f}")
    print("=== p=151, M_9 = 12 forced ===")
    p = 151
    Ms = {d: combined_arity(p, d)[0] for d in range(2, c + 1)}
    n9 = 1
    for d in range(2, 9): n9 *= Ms[d]
    lhs0 = n9 * beta_s3(p, gcd(9, p - 1), 12, g[9])
    print("lhs at M9=12: 2^%.1f" % lg(lhs0))
    mr = mixed_rule(p)
    print("rule at 151:", mr['kinds'], "added", mr['added'])
    print("=== primes below 3600 with a column added ===")
    cnt, lst = 0, []
    for p in range(11, 3600):
        if not is_prime(p): continue
        mr = mixed_rule(p)
        if sum(mr['added'].values()) > 0:
            cnt += 1; lst.append(p)
    print("count", cnt, "first few", lst[:10], "last", lst[-5:])
    print("=== part (ii): u=18, M=72, n0=37 ===")
    u, M, n0 = 18, 72, 37
    B = clog2(64 * Fr(4 * u) ** (c - 1))
    print("B =", B)
    for p in [5281, 105019, 2**31 - 1, 2**61 - 1, 194522647344910884721, 2**127 - 1]:
        print(" prime?", is_prime(p), end='')
        best, bank = 0, Fr(0)
        for d in range(2, c + 1):
            k = gcd(d, p - 1); h = (p - 1) // k; q = Fr(h + 1, p)
            capx = 2 * B * log(2) * float(q) ** (-g[d])
            best = max(best, log2(ceil(capx)))
            bank += Fr(M) ** (d - 2) * beta_fc(p, k, M, n0, g[d])
        print(f" p~2^{log2(p):.1f}: max cap 2^{best:.2f}, bank sum 2^{lg(bank):.2f}")
