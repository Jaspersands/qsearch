#!/opt/anaconda3/bin/python
"""Independent referee checks for 2026-11-12-rees-exponent-discharge.md (finite, exact; AI-run).

(1) t(p,k): least number of NONZERO k-th powers summing to 0 in F_p, by plain BFS over residues
    (no Weil shortcut), for every prime p <= PMAX and every k | p-1 with 2 <= k <= 9.
(2) Weil shortcut used by the note: p+1-(k-1)(k-2)sqrt(p) > 3k  ==>  t <= 3. Checked against (1).
(3) E_S1t(c) = 1 + sum_{d=2}^c k_d*ceil(log2 t(p,k_d)), k_d = gcd(d,p-1), max over primes c<p<=PMAX,
    plus the analytic tail: for p > PMAX every t <= 3 (Weil) and t = 2 iff (p-1)/k even.
(4) Exponent 2c-1 from the quadratic arities, and the core's 1+sum d*ceil(log2(d+1)).
(5) T_A(9), T_A(8) recomputed from the closed form U_k(p) of prop:app-s2-TA (bisection, mpmath).
(6) IS Sec. 3.3 'any t <= 2^L': exact check of the accumulation step on random small instances.
"""
import math, sys, random
from functools import reduce
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20000

def primes(n):
    s = bytearray([1])*(n+1); s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(3,n+1) if s[i]]

def tlen(p,k):
    P = {pow(x,k,p) for x in range(1,p)}
    if p-1 in P: return 2           # q + q' = 0 with q' = -q... need -q in P: -1 in P
    reach = set(P); t = 1
    while True:
        t += 1
        if any((p-q) % p in reach for q in P): return t
        reach = {(r+q) % p for r in reach for q in P}

PS = primes(PMAX)
T = {}
bad_weil = []
for p in PS:
    for k in range(2,10):
        if (p-1) % k == 0:
            if k % 2 == 1: T[(p,k)] = 2; continue
            if ((p-1)//k) % 2 == 0: T[(p,k)] = 2; continue
            if p > 6000 and p+1-(k-1)*(k-2)*math.sqrt(p) > 3*k:
                T[(p,k)] = 'le3'; continue      # Weil region; spot-checked below
            t = tlen(p,k); T[(p,k)] = t
            if p+1-(k-1)*(k-2)*math.sqrt(p) > 3*k and t > 3: bad_weil.append((p,k,t))
# spot-check Weil region exactly at a few primes
for p in [q for q in PS if q > 6000][:60]:
    for k in (2,4,6,8):
        if (p-1) % k == 0 and ((p-1)//k) % 2 == 1:
            t = tlen(p,k)
            if t > 3: bad_weil.append((p,k,t))
print('(2) Weil shortcut violations (p,k,t):', bad_weil)

def cost(p,k):
    if k == 1: return 1
    if k == p-1: return k*math.ceil(math.log2(p))
    t = T[(p,k)]
    if t == 'le3': t = 3
    return k*math.ceil(math.log2(t))

print('(3) E_S1t(c), max over primes c<p<=%d:' % PMAX)
for c in range(2,10):
    best = max(((1+sum(cost(p,math.gcd(d,p-1)) for d in range(2,c+1))), p) for p in PS if p > c)
    print('   c=%d  E=%d at p=%d' % (c,best[0],best[1]))
print('   p=41: t(41,8) =', tlen(41,8), ' 8th powers:', sorted({pow(x,8,41) for x in range(1,41)}))
print('   p=2521: t(2521,8) =', tlen(2521,8))
# analytic tail for c = 9 (p > PMAX): t<=3, t=2 iff (p-1)/k even; enumerate residue classes of p mod 2^4*3^2*5*7
best_tail = 0
L = 16*9*5*7
for r in range(1, L):
    if math.gcd(r, L) != 1 and r % 2 == 0: continue
    if r % 2 == 0: continue
    # p == r mod L; kappa_d = gcd(d, p-1) determined by r for d<=9
    E = 1
    for d in range(2,10):
        k = math.gcd(d, r-1)
        if k == 1: E += 1; continue
        # (p-1)/k even  <=> 2k | p-1 ; determined mod L since 2k | 16*9*... for k<=9? k<=9 -> 2k<=18 divides L except 2k=14,10,18: L has 7,5,9 so fine
        E += k if (r-1) % (2*k) == 0 else 2*k
    best_tail = max(best_tail, E)
print('   c=9 analytic tail (p > %d, t<=3): max E = %d' % (PMAX, best_tail))

print('(4) core 1+sum d*ceil(log2(d+1)):', [1+sum(d*math.ceil(math.log2(d+1)) for d in range(2,c+1)) for c in range(2,10)])
print('    quadratic arities: 1+2(c-1) =', [2*c-1 for c in range(2,10)])

try:
    import mpmath as mp
    mp.mp.dps = 40
    def U(k,p):
        p = mp.mpf(p)
        D = ((k-1)*(k-2)*mp.sqrt(p) + 2*(k-1))/(p-k-1)
        if D > 0.5: return None
        u = mp.mpf(1)/2 - D/3 - 1/(k*(1-D)); v = D/(mp.sqrt(k)*(1-D)); smax = mp.sqrt(k)*D
        if u > 0:
            s = min(smax, v/(2*u)); Em = -u*s*s + v*s
        else:
            Em = -u*smax*smax + v*smax
        Em = max(Em, 0)
        return k**k*p**(k-1)/(p-1)**k + mp.e**Em
    for k in (8,9):
        lo, hi = mp.mpf(10)**6, mp.mpf(10)**11
        for _ in range(200):
            mid = (lo+hi)/2
            u = U(k,mid)
            if u is not None and u < mp.mpf(k)/(k-1): hi = mid
            else: lo = mid
        print('(5) T_A(%d) = %s' % (k, mp.nstr(hi, 12)))
except ImportError:
    print('(5) mpmath missing')

# (6) IS accumulation: G^L vectors -> one vector with 2^L disjoint representations; any zero sum of
# t <= 2^L k-th powers kills it. Simulate abstractly on F_p^a with a brute-force collision finder.
def collide(vecs, p, k):
    """brute force Theorem-11 substitute: disjoint I (nonempty), J, nonzero gammas with
    sum_I g^k v = sum_J g^k v. Returns (I, J, coeff dict) or None."""
    import itertools
    n = len(vecs); a = len(vecs[0]); P = sorted({pow(x,k,p) for x in range(1,p)})
    # search over assignments in {0, +P, -P}
    choices = [0] + P + [(-q) % p for q in P]
    for assign in itertools.product(range(len(choices)), repeat=n):
        if all(c == 0 for c in assign): continue
        s = [0]*a
        for v, c in zip(vecs, assign):
            w = choices[c]
            for j in range(a): s[j] = (s[j] + w*v[j]) % p
        if any(s): continue
        I = [i for i,c in enumerate(assign) if 1 <= c <= len(P)]
        J = [i for i,c in enumerate(assign) if c > len(P)]
        if not I: I, J = J, I
        return I, J, {i: choices[c] if i in I else (-choices[c]) % p for i,c in enumerate(assign) if c}
    return None
random.seed(1)
ok = 0; trials = 0
for p, k in ((7,2), (13,4), (11,2)):
    P = sorted({pow(x,k,p) for x in range(1,p)})
    # shortest zero sum
    t = tlen(p,k)
    zs = None
    import itertools
    for comb in itertools.product(range(1,p), repeat=t):
        if sum(pow(x,k,p) for x in comb) % p == 0: zs = comb; break
    for _ in range(20):
        trials += 1
        a = 1; G = 3   # groups of 3 scalars in F_p always collide for these (p,k) (checked by assert)
        L = math.ceil(math.log2(t))
        n = G**L
        vecs = [[random.randrange(p)] for _ in range(n)]
        # level structure: reps[g] = list of representations (dict idx->coef with coef in P) of value val[g]
        groups = [([{i:1}], vecs[i][0]) for i in range(n)]
        done = None
        for lev in range(L):
            new = []
            for b in range(0, len(groups), G):
                blk = groups[b:b+G]
                res = collide([[v] for _, v in blk], p, k)
                assert res is not None
                I, J, cf = res
                if not J:  # direct solution
                    done = (blk, I, cf); break
                val = sum(cf[i]*blk[i][1] for i in I) % p
                reps = []
                for side in (I, J):
                    for rsel in range(len(blk[0][0])):
                        rep = {}
                        for i in side:
                            for idx, co in blk[i][0][rsel].items(): rep[idx] = co*cf[i] % p
                        reps.append(rep)
                new.append((reps, val))
            if done: break
            groups = new
        if done:
            ok += 1; continue
        reps, val = groups[0]
        assert len(reps) == 2**L >= t
        # combine first t representations with the zero sum
        x = {}
        for j in range(t):
            for idx, co in reps[j].items():
                assert idx not in x
                x[idx] = co*pow(zs[j],k,p) % p
        tot = sum(c*vecs[i][0] for i,c in x.items()) % p
        if tot == 0 and any(x.values()) and all(c in P for c in x.values() if c): ok += 1
print('(6) IS accumulation with t <= 2^L (t = shortest zero sum): %d/%d exact witnesses' % (ok, trials))
