import sys; sys.path.insert(0, '.')
import cert
orig = cert.up
def up(k, p, m, mode):
    if m >= 3: return float('inf')
    return orig(k, p, m, mode)
cert.up = up
def best(k, p):
    b = (0, None)
    for M in range(2, k):
        lo = cert.low(k, p, M)
        for m in (1, 2):
            if m >= M: continue
            c = cert.ff(k - 1 - m, M - m); u = up(k, p, m, 'ref')
            if c > 0: 
                r = float(lo / (c * u))
                if r > b[0]: b = (r, (m, M))
    return b
for k, a, z in [(5, 1300, 3000), (6, 19000, 40000)]:
    first = None; fails = []
    for p in range(a, z):
        if p % k == 1 and cert.isprime(p):
            r, mM = best(k, p)
            if r > 1 and first is None: first = (p, mM)
            elif r <= 1 and first: fails.append(p)
    print(k, 'Weil-free first certified', first, 'later failures', fails[:5])
