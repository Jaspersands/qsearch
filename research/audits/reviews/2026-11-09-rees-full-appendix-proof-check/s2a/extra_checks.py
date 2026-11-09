# s2a: (a) sampler of Prop. prop:app-s2-TA(iii) / Cor. cor:app-s2-decoupled at the first primes above T_S;
# (d) eta_{kappa-1} > 1 for p <= kappa^kappa/2 and the smallest p at which a merge (eta_2 < 1) occurs.
import math, random, sympy
import numpy as np
random.seed(5)
def E(k, m, p):
    c = m*(1-1/k) - 1 + k**(-m); d = m/k - m*k**(-m)
    return c*math.sqrt(p) + d
def eta(k, m, p): return k**m*E(k, m, p)/(p-m)
# (d)
out = []
for k in range(3, 11):
    lim = min(k**k//2, 2*10**6)
    ps = [p for p in sympy.primerange(k+1, lim+1) if p % k == 1]
    bad = [p for p in ps if not eta(k, k-1, p) > 1]
    merge = [p for p in ps if eta(k, 2, p) < 1]
    out.append((k, len(ps), 'eta_{k-1}<=1 at', bad[:3], 'smallest p with eta_2<1:', merge[0] if merge else None, '(k-1)^4 =', (k-1)**4))
for o in out: print(*o)
# (a) sampler rounds: K = ceil(2 (p/h)^k ln(4k)) draws per column
def sampler_round(p, k, ind):
    h = (p-1)//k
    y = [0] + [random.randrange(p) for _ in range(k-1)]
    K = math.ceil(2*(p/h)**k*math.log(4*k))
    alpha = []
    for j in range(k):
        found = None
        for _ in range(K):
            x = random.randrange(p)
            if all(ind[(x + y[i]) % p] == (-(i+j)) % k for i in range(k)):
                found = x; break
        if found is None: return False
        alpha.append(found)
    return True
for k, p in [(3, 739), (4, 8597), (2, 71)]:
    assert sympy.isprime(p) and p % k == 1
    g = int(sympy.primitive_root(p)); ind = np.full(p, -1); x = 1
    for n in range(p-1): ind[x] = n % k; x = x*g % p
    ind = ind.tolist()
    R = 150; s = sum(sampler_round(p, k, ind) for _ in range(R))
    print('sampler', (k, p), 'success rate', s/R, '(claimed >= 3/8)')
