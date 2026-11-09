# independent brute-force: count normalised open C1 configs (beta0=0,beta1=1) and Rees configs
import sys, itertools
from collections import defaultdict
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from sep_types import primroot
k=int(sys.argv[1]); p=int(sys.argv[2])
g=primroot(p); ind={}
x=1
for e in range(p-1): ind[x]=e%k; x=x*g%p
c1=0; rees=0
for rest in itertools.permutations(range(2,p),k-2):
    beta=(0,1)+rest
    cls=defaultdict(list)
    for x in range(p):
        if any((x+b)%p==0 for b in beta): continue
        w=tuple(ind[(x+b)%p] for b in beta)
        key=tuple((wi-w[0])%k for wi in w)
        cls[key].append((x,w[0]))
    for key,L in cls.items():
        n=len(L)
        if n>=k:
            c1+= n*(n-1)*(n-2)*(n-3) if k==4 else (n*(n-1)*(n-2) if k==3 else 0)
        # Rees: column j needs profile w_i = -(i+j) + a: key must be (-i)%k, and w0 = -j + a distinct over j
        if key==tuple((-i)%k for i in range(k)):
            vals=set(v for _,v in L)
            if len(vals)==k: rees+=1  # counts betas*shift-classes, not configs
print('k',k,'p',p,'C1 normalised labeled =',c1,' #(beta,class) admitting Rees =',rees)
