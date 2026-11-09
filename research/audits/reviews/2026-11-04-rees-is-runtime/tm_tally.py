# Unit-constant tally of the non-arithmetic head movement of one run (report section 4),
# divided by kappa^3 * N * b^2 * (a^2 + b^2).  Exact integer arithmetic.
from math import log2, ceil
from fractions import Fraction as Fr
def omega(k):
    s,f=0,2
    while f*f<=k:
        if k%f==0:
            s+=1
            while k%f==0: k//=f
        f+=1
    return s+(k>1)
worst=(0,None)
for k in range(2,13):
    beta=k.bit_length(); w=omega(k)
    for a in (1,2,3,5,10,30,100,1000):
        G=k**(k*(k-1)//2)*(a+1)**k
        B=[1]+[k**(l*(l-1)//2)*(a+1)**l for l in range(1,k+1)]
        for ell in (2,k+1):           # zero-sum length range
            L=ceil(log2(ell)); N=G**L
            I=sum(G**(L-j+1) for j in range(1,L+1)); calls=I//G
            logN=N.bit_length()
            for b in (2,3,8,32,128):
                for nu in sorted({0,1,b-1}):
                    per_call=0
                    for l in range(1,k+1):
                        R=k**(l-1)*a; E=k**(l-1)*(a+1); nodes=G//B[l]
                        per_call+=nodes*(R*E*b + 4*R*R*E*b + E*k**l*a*b + 2*k**l*a*b
                                         + E*(nu*k*(b+beta) + (nu+w+1)*b*b))
                        per_call+=G*(k*beta+b) + (G//B[l-1])*(beta+b+logN)
                    per_call+=k**k*(k*k*beta+a*b) + G*k*k*beta
                    D=calls*per_call + L*N*(L+b) + I*logN
                    r=Fr(D, k**3*N*b*b*(a*a+b*b))
                    if r>worst[0]: worst=(r,(k,a,ell,b,nu))
print("max movement / (kappa^3 N b^2 (a^2+b^2)) per run =", float(worst[0]), "at (kappa,a,ell,b,nu) =", worst[1])
