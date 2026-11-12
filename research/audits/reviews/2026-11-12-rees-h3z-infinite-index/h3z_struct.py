"""Finite checks (exact integer arithmetic) of the structural lemmas for
subgroups of H_3(Z).  Elements are triples (a,b,c) = matrix [[1,a,c],[0,1,b],[0,0,1]],
(a,b,c)(a',b',c') = (a+a', b+b', c+c'+ab').
Checks only; they can falsify, not prove.
Usage: nice -n 19 /opt/anaconda3/bin/python h3z_struct.py [trials] [bits] [seed]
"""
import random, sys
from math import gcd

def mul(g, h): return (g[0]+h[0], g[1]+h[1], g[2]+h[2]+g[0]*h[1])
def inv(g): return (-g[0], -g[1], -g[2]+g[0]*g[1])
def pw(g, t): return (t*g[0], t*g[1], t*g[2] + (t*(t-1)//2)*g[0]*g[1])
def comm(g, h): return mul(mul(inv(g), inv(h)), mul(g, h))
ONE = (0, 0, 0)

class Sub:
    """Induced polycyclic sequence X (a>0), Y (a=0,b>0), Z (a=b=0,c>0)."""
    def __init__(self, gens):
        self.X = self.Y = self.Z = None
        self.gens = list(gens)
        changed = True
        while changed:
            old = (self.X, self.Y, self.Z)
            for g in self.gens: self._ins(g)
            for u in (self.X, self.Y):
                if u is None: continue
                for v in (self.X, self.Y, self.Z):
                    if v is not None: self._ins(comm(u, v))
            # conjugates of Y by X are Y*[Y,X]; covered by commutators
            changed = (self.X, self.Y, self.Z) != old
    def _ins(self, g):
        if g[0] != 0:
            if self.X is None:
                self.X = g if g[0] > 0 else inv(g); return
            if g[0] % self.X[0] == 0:
                self._ins(mul(pw(self.X, -(g[0] // self.X[0])), g)); return
            u, v = self.X, g
            while v[0] != 0:
                q = u[0] // v[0]
                u, v = v, mul(pw(v, -q), u)
            self.X = u if u[0] > 0 else inv(u)
            self._ins(v); return
        if g[1] != 0:
            if self.Y is None:
                self.Y = g if g[1] > 0 else inv(g); return
            if g[1] % self.Y[1] == 0:
                self._ins(mul(pw(self.Y, -(g[1] // self.Y[1])), g)); return
            u, v = self.Y, g
            while v[1] != 0:
                q = u[1] // v[1]
                u, v = v, mul(pw(v, -q), u)
            self.Y = u if u[1] > 0 else inv(u)
            self._ins(v); return
        if g[2] != 0:
            if self.Z is None: self.Z = (0, 0, abs(g[2])); return
            self.Z = (0, 0, gcd(self.Z[2], g[2]))
    def contains(self, g):
        for slot, i in ((self.X, 0), (self.Y, 1), (self.Z, 2)):
            if g[i] == 0: continue
            if slot is None or g[i] % slot[i]: return False
            g = mul(pw(slot, -(g[i] // slot[i])), g)
        return g == ONE
    def e(self): return 0 if self.Z is None else self.Z[2]   # H cap Z = <z^e>, 0 means trivial
    def basis(self): return [s for s in (self.X, self.Y, self.Z) if s is not None]

def rand_elt(B): return tuple(random.randrange(-2**B + 1, 2**B) for _ in range(3))

def rand_word(gens, L):
    g = ONE
    for _ in range(L):
        x = random.choice(gens); g = mul(g, x if random.random() < .5 else inv(x))
    return g

def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    bits = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    stats = dict(trivZ=0, cyclic_ok=0, ebound_ok=0, eZ=0, member_fail=0,
                 rank1_e=0, absA_ok=0, Av_ok=0, fin_index_rank2=0)
    worst_e_ratio = 0.0
    for tr in range(trials):
        b = random.randint(1, bits)
        m = random.randint(1, 3)
        kind = random.random()
        if kind < 0.3:        # force rank-1 projection: multiples of one direction
            v = (random.randint(-3, 3), random.randint(-3, 3))
            if v == (0, 0): v = (1, 0)
            gens = []
            for _ in range(m):
                k = random.randint(-2**b // 4 - 1, 2**b // 4 + 1)
                gens.append((k*v[0], k*v[1], random.randrange(-2**b + 1, 2**b)))
        else:
            gens = [rand_elt(b) for _ in range(m)]
        gens = [g for g in gens if max(abs(x) for x in g) < 2**b] or [(0, 0, 1)]
        H = Sub(gens)
        # membership self-test: random words must sift
        for _ in range(20):
            if not H.contains(rand_word(gens, 8)): stats['member_fail'] += 1
        for s in H.basis():
            assert H.contains(s)
        e = H.e()
        if e == 0:
            stats['trivZ'] += 1
            # Lemma C: H cap Z = 1 implies H cyclic (basis length <= 1)
            if len(H.basis()) <= 1: stats['cyclic_ok'] += 1
            else: print('CYCLIC FAIL', gens, H.basis())
            continue
        stats['eZ'] += 1
        # Lemma E: e <= 2^(4b+3)
        if e <= 2**(4*b + 3): stats['ebound_ok'] += 1
        else: print('EBOUND FAIL', b, gens, e)
        worst_e_ratio = max(worst_e_ratio, e.bit_length() / max(b, 1))
        rank = (H.X is not None) + (H.Y is not None)
        if rank == 1:
            stats['rank1_e'] += 1
            # Lemma A (e>=1, rank 1): A = <x^e, y, z>; A/<z^e> abelian, coords (alpha,beta,gamma mod e)
            # H cap A has rank 1; its generator gives direction v; H <= A_v and H finite index in A_v.
            # (a) coordinate map is a homomorphism mod e on random elements of A
            ok = True
            for _ in range(10):
                g1 = (e*random.randint(-5, 5), random.randint(-9, 9), random.randint(-50, 50))
                g2 = (e*random.randint(-5, 5), random.randint(-9, 9), random.randint(-50, 50))
                def co(g):  # g = x^{e al} y^be z^ga  => matrix (e al, be, ga + e al be)
                    al, be = g[0] // e, g[1]; return (al, be, (g[2] - g[0]*g[1]) % e)
                p = co(mul(g1, g2)); q = co(g1); r = co(g2)
                ok &= (p == (q[0]+r[0], q[1]+r[1], (q[2]+r[2]) % e))
            # (b) direction from H cap A
            u = H.X if H.X is not None else H.Y
            # smallest power of u lying in A: need t*u.a = 0 mod e
            t = e // gcd(e, u[0]) if u[0] else 1
            hm = pw(u, t)
            ok &= (hm[0] % e == 0) and H.contains(hm)
            d = gcd(hm[0], hm[1]); v = (hm[0] // d, hm[1] // d)
            # every basis element projects into Z v
            ok2 = all(s[0]*v[1] - s[1]*v[0] == 0 for s in H.basis())
            stats['absA_ok'] += ok; stats['Av_ok'] += ok2
            if not (ok and ok2): print('LEMMA A FAIL', gens, H.basis(), e)
        elif rank == 2:
            stats['fin_index_rank2'] += 1
    print('trials', trials, 'bits<=', bits)
    for k, v in stats.items(): print(f'  {k}: {v}')
    print('  max bitlen(e)/b over instances with e>=1:', round(worst_e_ratio, 3))

if __name__ == '__main__':
    main()
