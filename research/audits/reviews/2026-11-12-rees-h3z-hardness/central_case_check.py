"""Finite checks for the H cap Z != 1 reduction and the root count (H_3(Z)).

Run: nice -n 19 /opt/anaconda3/bin/python central_case_check.py
Finite checks only: they can falsify, never prove.

Elements are matrix triples (a, b, c) = [[1,a,c],[0,1,b],[0,0,1]],
(a,b,c)(a',b',c') = (a+a', b+b', c+c'+ab'). x=(1,0,0), y=(0,1,0), z=(0,0,1).

Check A (Prop E, step 2): for H containing z^k, phi(a,b,c) = x^{ka} y^{kb} z^c
satisfies  phi(u)^{-1} phi(u') in H  <=>  phi(u'-u) in H, and Lambda = phi^{-1}(H)
is closed under addition, on a box.  Membership in H = <h, z^k> or <z^k> or a
finite-index H = <h1, h2, z^k> is decided exactly (see member()).

Check B (classical bound): for random g, the number of noncentral h in the box
family with g in <h> is at most 2 * tau(gcd(pi(g))) (unique roots).
"""
import random
from math import gcd

def mul(g, h):
    return (g[0] + h[0], g[1] + h[1], g[2] + h[2] + g[0] * h[1])

def inv(g):
    return (-g[0], -g[1], g[0] * g[1] - g[2])

def power(g, m):
    a, b, c = g
    # g^m = (ma, mb, mc + C(m,2) ab) for every integer m
    return (m * a, m * b, m * c + (m * (m - 1) // 2) * a * b)

def xpow(t): return (t, 0, 0)
def ypow(t): return (0, t, 0)
def zpow(t): return (0, 0, t)

def member_rank1(g, h, k):
    """g in <h, z^k> (k >= 1) or <h> (k = 0), h noncentral."""
    v1, v2 = h[0], h[1]
    a, b = g[0], g[1]
    # need (a,b) = m (v1,v2)
    if v1 != 0:
        if a % v1: return False
        m = a // v1
    else:
        if b % v2: return False
        m = b // v2
    if (m * v1, m * v2) != (a, b): return False
    r = mul(g, inv(power(h, m)))
    assert r[0] == 0 and r[1] == 0
    return r[2] == 0 if k == 0 else r[2] % k == 0

def member_central(g, k):
    return g[0] == 0 and g[1] == 0 and (g[2] == 0 if k == 0 else g[2] % k == 0)

def member_fi(g, h1, h2, k):
    """g in <h1, h2, z^k>, pi(h1), pi(h2) independent. H contains z^d with
    d = gcd(k, det), det = det(pi h1, pi h2), since [h1,h2] = z^det."""
    a1, b1 = h1[0], h1[1]; a2, b2 = h2[0], h2[1]
    det = a1 * b2 - a2 * b1
    d = gcd(k, abs(det))
    # solve (a,b) = s pi(h1) + t pi(h2) over Z
    a, b = g[0], g[1]
    sn = a * b2 - a2 * b; tn = a1 * b - a * b1
    if sn % det or tn % det: return False
    s, t = sn // det, tn // det
    r = mul(g, inv(mul(power(h1, s), power(h2, t))))
    assert r[0] == 0 and r[1] == 0
    return r[2] % d == 0

def phi(u, k):
    a, b, c = u
    return mul(mul(xpow(k * a), ypow(k * b)), zpow(c))

def check_A(trials, rng):
    bad = 0; n = 0
    for _ in range(trials):
        k = rng.randint(1, 6)
        kind = rng.choice(["central", "rank1", "fi"])
        if kind == "central":
            mem = lambda g: member_central(g, k)
        elif kind == "rank1":
            while True:
                h = (rng.randint(-4, 4), rng.randint(-4, 4), rng.randint(-6, 6))
                if (h[0], h[1]) != (0, 0): break
            mem = lambda g, h=h: member_rank1(g, h, k)
        else:
            while True:
                h1 = (rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-5, 5))
                h2 = (rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-5, 5))
                if h1[0] * h2[1] - h2[0] * h1[1] != 0: break
            mem = lambda g, h1=h1, h2=h2: member_fi(g, h1, h2, k)
        R = 3
        box = [(a, b, c) for a in range(-R, R + 1) for b in range(-R, R + 1)
               for c in range(-2 * R, 2 * R + 1)]
        sample = rng.sample(box, 40)
        for u in sample:
            for w in sample:
                n += 1
                lhs = mem(mul(inv(phi(u, k)), phi(w, k)))
                diff = tuple(w[i] - u[i] for i in range(3))
                rhs = mem(phi(diff, k))
                if lhs != rhs: bad += 1
                # closure of Lambda
                if mem(phi(u, k)) and mem(phi(w, k)):
                    s = tuple(w[i] + u[i] for i in range(3))
                    if not mem(phi(s, k)): bad += 1
    return n, bad

def divisors_count(n):
    n = abs(n); c = 0
    for d in range(1, n + 1):
        if n % d == 0: c += 1
    return c

def check_B(trials, rng, Bx=6):
    """Family F: h = (v1, v2, c) with |v_i| <= Bx, |c| <= Bx, (v1,v2) != 0.
    Count h in F with g in <h>; compare with 2*tau(gcd(pi g))."""
    fam = [(v1, v2, c) for v1 in range(-Bx, Bx + 1) for v2 in range(-Bx, Bx + 1)
           for c in range(-Bx, Bx + 1) if (v1, v2) != (0, 0)]
    worst = 0; bad = 0
    for _ in range(trials):
        h0 = rng.choice(fam); m = rng.randint(1, 4)
        g = mul(power(h0, m), zpow(0)) if rng.random() < 0.7 else \
            (rng.randint(-20, 20), rng.randint(-20, 20), rng.randint(-60, 60))
        if (g[0], g[1]) == (0, 0): continue
        cnt = sum(1 for h in fam if member_rank1(g, h, 0))
        bound = 2 * divisors_count(gcd(g[0], g[1]))
        worst = max(worst, cnt)
        if cnt > bound: bad += 1
    return worst, bad

if __name__ == "__main__":
    rng = random.Random(20261112)
    n, bad = check_A(60, rng)
    print(f"Check A (phi hides phi^-1(H), Lambda closed): {n} pairs, {bad} failures")
    worst, bad = check_B(400, rng)
    print(f"Check B (#h in family with g in <h> <= 2 tau(gcd pi g)): worst count {worst}, {bad} failures")
