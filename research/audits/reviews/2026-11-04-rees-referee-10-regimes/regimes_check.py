"""Independent re-derivation of tab:fcs-budget and the filiform zero-sum numbers.
Exact rationals where it matters; log2 via mpmath-free float on big ints."""
from fractions import Fraction as Fr
from math import gcd, log2, ceil, log
import itertools, sys

def lg(x):
    # log2 of a positive Fraction or int, robust for huge ints
    if isinstance(x, Fr):
        return lg(x.numerator) - lg(x.denominator)
    x = int(x)
    b = x.bit_length()
    if b < 1000:
        return log2(x)
    s = b - 60
    return log2(x >> s) + s

def ceil_log(base, x):
    """least j>=0 with base^j >= x (x Fraction)"""
    j = 0; v = Fr(1)
    while v < x:
        v *= base; j += 1
    return j

def beta(p, kappa, M, n0, a):
    h = (p - 1) // kappa
    q = Fr(h + 1, p)
    L = M - n0
    return Fr(4, 1) / (Fr(h) ** (n0 - 1) * q ** a) + Fr(p ** a - 1, (p - 1) * p ** L)

def least_fcs(p, kappa, g, tau):
    """least M with some 1<=n0<=M, beta<=tau.  For fixed M, beta first term decreasing in n0,
    second increasing; scan."""
    h = (p - 1) // kappa
    q = Fr(h + 1, p)
    # lower bound for M: need second term <= tau with L>=0 and first <= tau
    M = 1
    while True:
        for n0 in range(1, M + 1):
            if beta(p, kappa, M, n0, g) <= tau:
                return M, n0
        M += 1

def B_IS(d, a):
    G = d ** (d * (d - 1) // 2) * (a + 1) ** d
    return G ** ceil(log2(d + 1)) if d > 1 else (a + 1)

def ceil_log2_frac(x):
    # least integer B with 2^B >= x
    B = 0
    while Fr(2) ** B < x:
        B += 1
    return B

def run_iii(p, gs, eps, zero_sum=False):
    """gs: dict d->g_d for d=2..c ; m = g_1"""
    m = gs[1]; c = max(gs)
    t = ceil_log(p, Fr(3) / eps); S = m + t
    Ms = {}; types = {}; taus = {}
    n = 1
    nd = {}
    for d in range(2, c + 1):
        k = gcd(d, p - 1); nd[d] = n
        g = gs[d]
        if k == 1:
            Ms[d] = g + 1; types[d] = 'lin'
        elif k == p - 1:
            if zero_sum:
                Ms[d] = g * (p - 1) + 1; types[d] = 'zs'
            else:
                Ms[d] = B_IS(d, g); types[d] = 'S1'
        else:
            tau = eps / (9 * (c - 1) * S * n)
            M, n0 = least_fcs(p, k, g, tau)
            Ms[d] = M; types[d] = 'F'; taus[d] = (tau, n0)
        n *= Ms[d]
    P = n
    Q = c * S * P
    N = S * sum(nd[d] for d in Ms if types[d] == 'F')
    out = dict(logQ=lg(Q), types=types, Ms=Ms)
    if N:
        B = ceil_log2_frac(Fr(27) * N / eps)
        caps = {}
        tot = 0
        for d in Ms:
            if types[d] == 'F':
                k = gcd(d, p - 1); h = (p - 1) // k; q = Fr(h + 1, p)
                x = 2 * B * log(2) * float(lg(1 / q ** gs[d]) and 2 ** (lg(1 / q ** gs[d])))
                cap = ceil(x)
                caps[d] = cap
                tot += S * nd[d] * cap
        out.update(B=B, maxcap=log2(max(caps.values())), argmax=max(caps, key=caps.get), total=lg(tot))
    return out

def combined(p, gs, eps):
    m = gs[1]; c = max(gs)
    S = m + ceil_log(p, Fr(3) / eps)
    P = 1
    for d in range(2, c + 1):
        k = gcd(d, p - 1); g = gs[d]
        if k == 1:
            M = g + 1
        elif p >= 16 * k ** (2 * k + 2):
            M = (g + 1) * ((k - 1) * g + 1)
        else:
            M = B_IS(k, g)
        P *= M
    return lg(c * S * P)

def mixed(p, gs, eps):
    m = gs[1]; c = max(gs)
    mp = m + ceil_log2_frac(Fr(3) / eps)
    Ms = {}; typ = {}
    for d in range(2, c + 1):
        k = gcd(d, p - 1); g = gs[d]
        if k == 1:
            M = g + 1; t = 'lin'
        elif p >= 16 * k ** (2 * k + 2):
            M = (g + 1) * ((k - 1) * g + 1); t = 'S2'
        else:
            M = B_IS(k, g); t = 'S1'
        u = max(2, k, g + 1)
        if p >= 16 * u * u and 4 * u < M:
            M = 4 * u; t = 'S3'
        Ms[d] = M; typ[d] = t
    if 'S3' not in typ.values():
        return None
    # bank condition
    def nds():
        n = 1; r = {}
        for d in range(2, c + 1):
            r[d] = n; n *= Ms[d]
        return r, n
    while True:
        nd, P = nds()
        terms = {}
        for d in Ms:
            if typ[d] == 'S3':
                k = gcd(d, p - 1); h = (p - 1) // k; g = gs[d]; M = Ms[d]
                bd = Fr(4 * h * p ** g, (h + 1) ** M - 1) + Fr(p ** g - 1, (p - 1) * p ** M)
                terms[d] = nd[d] * bd
        if sum(terms.values()) <= Fr(1, 64):
            break
        dmax = max(terms, key=terms.get); Ms[dmax] += 1
    nS3 = sum(nd[d] for d in Ms if typ[d] == 'S3'); nS2 = sum(nd[d] for d in Ms if typ[d] == 'S2')
    B = ceil_log2_frac(Fr(64) * max(1, 3 * nS3 + nS2))
    Q = 4 * mp * c * P
    trials = max(lg(4 * gcd(d, p - 1) ** Ms[d] * B) for d in Ms if typ[d] == 'S3')
    bank = sum(terms.values())
    abort = bank + (3 * nS3 + nS2) * Fr(1, 2 ** B)
    return dict(logQ=lg(Q), trials=trials, typ=typ, Ms=Ms, bank=lg(bank) if bank else None, abort=lg(abort))

if __name__ == '__main__':
    eps = Fr(1, 3)
    prof = [19, 17, 16, 14, 12, 9, 6, 3, 1]
    gs = {i + 1: g for i, g in enumerate(prof)}
    for p in [11, 1031, 5281, 2 ** 31 - 1, 2 ** 61 - 1, 2 ** 127 - 1]:
        r = run_iii(p, gs, eps)
        cmb = combined(p, gs, eps)
        mx = mixed(p, gs, eps)
        print('p=%s combined=%.1f' % (p if p < 10**6 else 'M%d' % p.bit_length(), cmb),
              'mixed=' + ('%.1f trials=%.1f abort=2^%.2f bank=2^%s' % (mx['logQ'], mx['trials'], mx['abort'], mx['bank']) if mx else '-'),
              '(iii) Q=%.1f maxcap=%.2f@d%s total=%.1f B=%s' % (r['logQ'], r['maxcap'], r['argmax'], r['total'], r['B']))
    # filiform zero-sum numbers
    for rr in [3, 5, 9]:
        c = rr + 1; p = c + 1; m = rr + 2
        gsf = {1: m}
        for d in range(2, c + 1):
            gsf[d] = rr - d + 2
        a = run_iii(p, gsf, eps, zero_sum=True); b = run_iii(p, gsf, eps, zero_sum=False)
        print('filiform r=%d p=%d: zero-sum logQ=%.1f, S1 logQ=%.1f types=%s' % (rr, p, a['logQ'], b['logQ'], a['types']))
