"""Check of the splitting argument for Aut(L_DL) on the centre (exact, mod p with p = 1 mod 4).
Verifies: the bracket table in the basis u1..u4, v+, v-, e7, e8; that the rank-1 locus of ad: V -> W
is U+ u U-; and that D = diag(1,-1,1,-1,-1,1,-1,-1) is an automorphism acting as -1 on Z."""
import itertools, sys
br = [(1,2,5,1),(1,3,6,1),(1,4,7,1),(1,5,8,-1),(2,3,8,1),(2,4,6,1),(2,6,7,-1),(3,4,5,-1),(3,5,7,-1),(4,6,8,-1)]
def run(p, i):
    assert (i*i + 1) % p == 0
    S = {}
    for a,b,k,c in br:
        S[(a-1,b-1)] = (k-1, c % p); S[(b-1,a-1)] = (k-1, (-c) % p)
    def lie(x, y):
        z = [0]*8
        for (a,b),(k,c) in S.items():
            if x[a] and y[b]: z[k] = (z[k] + x[a]*y[b]*c) % p
        return z
    def vec(d):
        z = [0]*8
        for k, c in d.items(): z[k-1] = c % p
        return z
    u1 = vec({1:i, 4:1}); u2 = vec({2:-i, 3:1}); u3 = vec({1:-i, 4:1}); u4 = vec({2:i, 3:1})
    vp = vec({5:1, 6:i}); vm = vec({5:1, 6:-i}); e7 = vec({7:1}); e8 = vec({8:1})
    sc = lambda c, v: [(c*x) % p for x in v]
    eq = lambda a, b: all((x-y) % p == 0 for x, y in zip(a, b))
    zero = [0]*8
    checks = {
        '[u1,u2]=2v+': eq(lie(u1,u2), sc(2,vp)), '[u3,u4]=2v-': eq(lie(u3,u4), sc(2,vm)),
        '[u1,u3]=2i e7': eq(lie(u1,u3), sc(2*i,e7)), '[u2,u4]=-2i e8': eq(lie(u2,u4), sc(-2*i,e8)),
        '[u1,u4]=0': eq(lie(u1,u4), zero), '[u2,u3]=0': eq(lie(u2,u3), zero),
        '[u1,v+]=-2i e8': eq(lie(u1,vp), sc(-2*i,e8)), '[u2,v+]=-2e7': eq(lie(u2,vp), sc(-2,e7)),
        '[u3,v-]=2i e8': eq(lie(u3,vm), sc(2*i,e8)), '[u4,v-]=-2e7': eq(lie(u4,vm), sc(-2,e7)),
        '[U+,v-]=0': eq(lie(u1,vm), zero) and eq(lie(u2,vm), zero),
        '[U-,v+]=0': eq(lie(u3,vp), zero) and eq(lie(u4,vp), zero),
        '[v+,v-]=0': eq(lie(vp,vm), zero),
    }
    # rank-1 locus of x -> (y -> W-part of [x,y]) on V
    def rank_w(x):
        rows = [lie(x, [1 if k == j else 0 for k in range(8)])[4:6] for j in range(4)]
        # rank of 4x2 matrix mod p
        m = [r[:] for r in rows]; r = 0
        for c in range(2):
            piv = next((t for t in range(r, 4) if m[t][c] % p), None)
            if piv is None: continue
            m[r], m[piv] = m[piv], m[r]; inv = pow(m[r][c], p-2, p)
            m[r] = [(v*inv) % p for v in m[r]]
            for t in range(4):
                if t != r and m[t][c]: m[t] = [(a - m[t][c]*b) % p for a, b in zip(m[t], m[r])]
            r += 1
        return r
    def inspan(x, a, b):
        return any(eq(x[:4], [(s*a[k] + t*b[k]) % p for k in range(4)]) for s in range(p) for t in range(p))
    low = [x for x in itertools.product(range(p), repeat=4) if any(x) and rank_w(list(x)+[0]*4) < 2]
    checks['rank<2 locus = (U+ u U-)\\0'] = all(inspan(list(x)+[0]*4, u1, u2) or inspan(list(x)+[0]*4, u3, u4) for x in low) \
        and len(low) == 2*(p*p-1)
    d = [1,-1,1,-1,-1,1,-1,-1]
    checks['D=diag(1,-1,1,-1,-1,1,-1,-1) is an automorphism'] = all(
        (d[k-1] - d[a-1]*d[b-1]) == 0 for a,b,k,c in br)
    bad = [k for k, v in checks.items() if not v]
    print(f"p={p} i={i}: {len(checks)} checks, failures: {bad}")
    return not bad
ok = run(13, 5) & run(5, 2) & run(17, 4) & run(29, 12)
print("ALL OK" if ok else "FAIL")
