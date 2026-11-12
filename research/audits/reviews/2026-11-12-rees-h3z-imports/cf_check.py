# Falsification check: Kuperberg step 5 denoising with an UPPER BOUND n' >= n.
# True entry a/b with b < 2^n; observed x with |x - a/b| < 1/R^2, R = 2^(2n'+1).
# Claim: the last continued-fraction convergent of x with denominator <= R is a/b.
import random, sys
from fractions import Fraction as F
def convergents(x):
    h0,h1,k0,k1=0,1,1,0
    y=x
    while True:
        a=y.numerator//y.denominator
        h0,h1=h1,a*h1+h0; k0,k1=k1,a*k1+k0
        yield F(h1,k1)
        r=y-a
        if r==0: return
        y=1/r
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
bad=0;N=0
for trial in range(20000):
    n=random.randint(1,12); nprime=n+random.randint(0,6)
    R=2**(2*nprime+1)
    b=random.randint(1,2**n-1); a=random.randint(-5*b,5*b)
    eps=F(random.randint(-10**6+1,10**6-1),10**6)/R**2
    x=F(a,b)+eps
    last=None
    for c in convergents(x):
        if c.denominator<=R: last=c
        else: break
    N+=1
    if last!=F(a,b): bad+=1
print("trials",N,"failures",bad)
# box arithmetic for Theorem A step 2: entries of (e*al, be, ga+e*al*be)
worst=0
for b in range(1,30):
    for P in (1,5,40,200):
        e=2**(3*b+1)-1; m=2**P-1
        v=max(e*m, m, m+e*m*m)
        assert v < 2**(2*P+3*b+2), (b,P)
print("box arithmetic ok: max entry < 2^(2P+3b+2) for tested b,P")
