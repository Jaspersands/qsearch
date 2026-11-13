# Thresholds of Lemma plus-sm / Table tab:plus-thresholds, written from the text only.
# Phi, Psi as defined in Lemma plus-sm, evaluated with mpmath at 80 digits.
import mpmath as mp
from sympy import isprime, nextprime
mp.mp.dps = 80
def parts(p, D, r, w):
    p = mp.mpf(p); h = (p-1)/D
    gam = (1 + (D-1)**2/mp.sqrt(p)) * p**2/(p-1)**2
    mu0 = h*(w*h/p)**(r-1); mu1 = w*h*(w*h/p)**(r-1)
    rho0 = 1/mu0 + gam**(r-1); rho1 = 1/mu1 + gam**(r-1)
    Phi = (1-1/rho0) + (D-1)*(1-1/rho1)
    Psi = 4*(rho0-1) + 4*(D-1)*(rho1-1)
    return Phi, Psi, mu0
def thresh(f, lo, hi):
    # least integer p in [lo,hi] with f(p) true, f monotone
    assert f(hi) and not f(lo)
    while hi-lo > 1:
        mid=(lo+hi)//2
        if f(mid): hi=mid
        else: lo=mid
    return hi
steps = [('TL3',3,3,1),('TL4',4,4,1),('TL5',5,5,1),('TL6',6,6,1),('TW',9,3,1),('Um',7,7,2),('TL7',7,7,1),('TL8',8,8,1),('TL9',9,9,1)]
res={}
for name,D,r,w in steps:
    Te = thresh(lambda p: parts(p,D,r,w)[0] < 1, 3, 10**11)
    Ts = thresh(lambda p: parts(p,D,r,w)[1] <= mp.mpf(1)/2, 3, 10**13)
    pD = Te
    while not (isprime(pD) and pD % D == 1): pD += 1
    one_minus = 1 - parts(pD,D,r,w)[0]
    band = D*r*Ts/one_minus
    samp = mp.mpf(8)/3*(r + D*r*mp.ceil(2*(2*D)**r*mp.log(4*D)))
    # monotonicity spot check on primes >= pD (1-Phi increasing)
    print(f"{name:4s} D={D} r={r} w={w} T_exist={Te} T_samp={Ts} p_D={pD} 1-Phi(p_D)={mp.nstr(one_minus,6)} band DrT_samp/(1-Phi)={mp.nstr(band,6)} samp_bound={mp.nstr(samp,6)}")
