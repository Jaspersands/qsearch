# Falsification check of appendix-free-coordinate.tex line 315 (A17):
# for y != 0, #{(u,v) in P_k^2 : u - v = y} >= (p - (k-1)(k-2)sqrt(p) - 3k + 1)/k^2,
# and if sqrt(p) >= 2(k-1)(k-2)+4 then count/h >= 1/(2k).
import math, sys
def primes(n):
    s=bytearray([1])*(n+1); s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]
N=int(sys.argv[1]) if len(sys.argv)>1 else 3000
bad1=bad2=0; cases=0; minratio=None
for p in primes(N):
    if p<3: continue
    for k in range(2,p):
        if (p-1)%k: continue
        h=(p-1)//k
        P=set(pow(x,k,p) for x in range(1,p))
        # count is the same for y in one coset of P; check one y per coset
        reps=[]; seen=set()
        for y in range(1,p):
            if y in seen: continue
            reps.append(y); seen |= {(y*t)%p for t in P}
        bound=(p-(k-1)*(k-2)*math.sqrt(p)-3*k+1)/k**2
        for y in reps:
            c=sum(1 for u in P if (u-y)%p in P)
            cases+=1
            if c < bound-1e-9: bad1+=1; print('BOUND FAIL',p,k,y,c,bound)
            if math.sqrt(p) >= 2*(k-1)*(k-2)+4:
                r=c/h
                minratio=r*2*k if minratio is None else min(minratio,r*2*k)
                if r < 1/(2*k)-1e-12: bad2+=1; print('PROB FAIL',p,k,y,c,h)
print('cases',cases,'bound failures',bad1,'prob failures',bad2,'min (count/h)*(2k) where hyp holds',minratio)
