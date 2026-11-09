import math, sys
def isprime(n):
    if n<2: return False
    i=2
    while i*i<=n:
        if n%i==0: return False
        i+=1
    return True
def AB(p):
    for B in range(1,int(math.isqrt(p//3))+1):
        A2=p-3*B*B
        A=math.isqrt(A2)
        if A*A==A2: return A,B
def phi(p):
    A,B=AB(p); th=math.degrees(math.atan2(B*math.sqrt(3),A)) % 60
    return A,B,min(th,60-th)
if sys.argv[1]=='list':
    for p in map(int,sys.argv[2:]):
        A,B,f=phi(p); print(p, 'lam=%.3f'%(p/7776), 'A=%d B=%d'%(A,B), 'phi=%.1f deg'%f)
else:
    lo,hi=map(int,sys.argv[1:3])
    for p in range(lo,hi):
        if p%6==1 and isprime(p):
            A,B,f=phi(p); print(p,'lam=%.3f'%(p/7776),'A=%d B=%d phi=%.1f'%(A,B,f))
