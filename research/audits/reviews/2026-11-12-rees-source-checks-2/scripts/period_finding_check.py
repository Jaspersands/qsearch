# Falsification check for the core's use of Mosca-Ekert Sect. 4.2 (main-core.tex l.826):
# f: Z -> X has least period e <= R = 2^b and is injective on a period; run on 0 <= t < Q = 2^(2b+1).
# Exact outcome distribution P(x) after QFT_Q; for each x list continued-fraction convergent
# denominators d <= R; "accepted" if some such d is a multiple of e (the test f(I+dE)=f(I)).
# Checks: (1) every good outcome x (|x/Q - k/e| <= 1/(2Q) for some k) has k/e (reduced) among
# its convergents; (2) per-run acceptance probability, min over e <= R.
import numpy as np, math, sys
from fractions import Fraction
def convergent_dens(a,b,R):
    out=[]; h0,h1=0,1; k0,k1=1,0
    while b:
        q=a//b; a,b=b,a-q*b
        h0,h1=h1,q*h1+h0; k0,k1=k1,q*k1+k0
        if k1>R: break
        out.append((h1,k1))
    return out
bmax=int(sys.argv[1]) if len(sys.argv)>1 else 7
bmin=int(sys.argv[2]) if len(sys.argv)>2 else 1
elist=[int(t) for t in sys.argv[3].split(',')] if len(sys.argv)>3 else None
for b in range(bmin,bmax+1):
    R=2**b; Q=2**(2*b+1); x=np.arange(Q)
    worst=(2.0,None); goodfail=0; mingood=(2.0,None)
    for e in (elist if elist else range(1,R+1)):
        P=np.zeros(Q)
        for j in range(e):
            N=(Q-1-j)//e+1
            th=np.pi*x*e/Q
            s=np.sin(th); num=np.sin(N*th)
            with np.errstate(divide='ignore',invalid='ignore'):
                a=np.where(np.abs(s)<1e-15, float(N*N), (num/s)**2)
            P+=a
        P/=Q*Q
        acc=0.0; pg=0.0
        for xi in range(Q):
            if P[xi]<1e-15: continue
            dens=convergent_dens(xi,Q,R)
            if any(d%e==0 for _,d in dens): acc+=P[xi]
            k=round(xi*e/Q)
            if abs(Fraction(xi,Q)-Fraction(k,e))<=Fraction(1,2*Q):
                pg+=P[xi]
                fr=Fraction(k,e)
                if (xi==0 and fr!=0) or (xi>0 and (fr.numerator,fr.denominator) not in dens and fr!=0):
                    goodfail+=1
        if acc<worst[0]: worst=(acc,e)
        if pg<mingood[0]: mingood=(pg,e)
    print(f"b={b} R={R} Q={Q}: min_e P(accept per run)={worst[0]:.4f} at e={worst[1]}; min_e P(good)={mingood[0]:.4f} at e={mingood[1]}; good outcomes missing k/e: {goodfail}")
