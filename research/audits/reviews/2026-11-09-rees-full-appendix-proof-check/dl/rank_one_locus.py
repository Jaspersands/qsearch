# Rank-one locus check (checker id: dl, 9 Nov 2026), independent of earlier scripts.
# For every projective point x of L/gamma_2 = span(e1..e4) over a finite field K containing i = sqrt(-1)
# (K = F_p if p = 1 mod 4, K = F_p[i] = F_{p^2} if p = 3 mod 4), compute r(x) = dim ([x,L]+gamma_3)/gamma_3
# (= rank of y |-> W-part of [x,y], y in span(e1..e4); [x,gamma_2] lies in gamma_3) and compare
# {r(x) = 1} with P(U+) u P(U-), U+ = span(i e1+e4, e3-i e2), U- = span(e4-i e1, e3+i e2).
# Also: r(x) does not change when a random gamma_2-component is added to x (sampled).
import sys, itertools, random
TABLE = {(1,2):{5:1},(1,3):{6:1},(1,4):{7:1},(1,5):{8:-1},(2,3):{8:1},
         (2,4):{6:1},(2,6):{7:-1},(3,4):{5:-1},(3,5):{7:-1},(4,6):{8:-1}}
def brb(i,j):
    if (i,j) in TABLE: return TABLE[(i,j)]
    if (j,i) in TABLE: return {k:-c for k,c in TABLE[(j,i)].items()}
    return {}
def run(p):
    if p%4==1:
        ii=next(x for x in range(p) if (x*x+1)%p==0)
        els=[(a,0) for a in range(p)]
        def mul(x,y): return ((x[0]*y[0])%p,0)
        I=(ii,0)
    else:
        els=[(a,b) for a in range(p) for b in range(p)]
        def mul(x,y): return ((x[0]*y[0]-x[1]*y[1])%p,(x[0]*y[1]+x[1]*y[0])%p)
        I=(0,1)
    def add(x,y): return ((x[0]+y[0])%p,(x[1]+y[1])%p)
    def neg(x): return ((-x[0])%p,(-x[1])%p)
    def sc(c,x): return (((c%p)*x[0])%p,((c%p)*x[1])%p)
    Z=(0,0); ONE=(1,0)
    q=len(els)
    def inv(x):
        # brute force inverse (small fields)
        for y in els:
            if mul(x,y)==ONE: return y
    def bracketW(x,y):  # W-part (e5,e6) of [x,y], x,y in K^8
        out=[Z,Z]
        for a in range(8):
            if x[a]==Z: continue
            for b in range(8):
                if y[b]==Z: continue
                for k,c in brb(a+1,b+1).items():
                    if k in (5,6): out[k-5]=add(out[k-5],sc(c,mul(x[a],y[b])))
        return out
    def rank2x4(cols):  # rank of 2x4 matrix over K given as 4 columns (pairs)
        nz=[c for c in cols if c!=[Z,Z]]
        if not nz: return 0
        c0=nz[0]
        for c in nz[1:]:
            det=add(mul(c0[0],c[1]),neg(mul(c0[1],c[0])))
            if det!=Z: return 2
        return 1
    E=[[ONE if k==j else Z for k in range(8)] for j in range(8)]
    def r_of(x8): return rank2x4([bracketW(x8,E[j]) for j in range(4)])
    # projective points: first nonzero coordinate = 1
    pts=[]
    for lead in range(4):
        for rest in itertools.product(els,repeat=3-lead):
            v=[Z]*lead+[ONE]+list(rest)
            pts.append(v)
    u1=[I,Z,Z,ONE]; u2=[Z,neg(I),ONE,Z]; u3=[neg(I),Z,Z,ONE]; u4=[Z,I,ONE,Z]
    def inspan(v,a,b):
        # v in span(a,b)?  check rank of [a,b,v] (4x3) < 3 via 3x3 minors
        cols=[a,b,v]
        for rows in itertools.combinations(range(4),3):
            m=[[cols[c][r] for c in range(3)] for r in rows]
            d=Z
            for perm,sgn in [((0,1,2),1),((1,2,0),1),((2,0,1),1),((0,2,1),-1),((2,1,0),-1),((1,0,2),-1)]:
                t=mul(mul(m[0][perm[0]],m[1][perm[1]]),m[2][perm[2]])
                d=add(d,t if sgn==1 else neg(t))
            if d!=Z: return False
        return True
    n1=0; agree=True; cnt={0:0,1:0,2:0}
    for v in pts:
        r=r_of(v+[Z]*4); cnt[r]+=1
        inU=inspan(v,u1,u2) or inspan(v,u3,u4)
        if (r==1)!=inU: agree=False; print('DISAGREE at',v,r,inU)
    random.seed(p)
    stable=True
    for _ in range(300):
        v=random.choice(pts); w=[random.choice(els) for _ in range(4)]
        if r_of(v+[Z]*4)!=r_of(v+w): stable=False
    print(f'p={p}, |K|={q}: {len(pts)} projective points, rank counts {cnt}; expected rank-1 count 2(|K|+1) = {2*(q+1)}; '
          f'rank-1 locus == P(U+) u P(U-): {agree}; r(x) unchanged by adding gamma_2 parts (300 samples): {stable}')
for p in map(int,sys.argv[1:]): run(p)
