import cmath, math
from itertools import product
exec(open('square_gap_checks.py').read().split('# ---------- A ----------')[0])  # helpers only
def chi_table(p, kappa):
    g = next(g for g in range(2, p) if all(pow(g, (p-1)//f, p) != 1 for f in range(2, p) if (p-1) % f == 0 and is_prime(f)))
    ind = {}; x = 1
    for k in range(p-1): ind[x] = k; x = x*g % p
    om = cmath.exp(2j*math.pi/kappa)
    def chi(s,u):
        u %= p
        if u == 0: return 1.0 if s % kappa == 0 else 0.0
        return om ** ((s*ind[u]) % kappa)
    return chi
print("B'. 4-cycle sub-case e1+e2 = e3+e4 = 0: Sigma should equal p^2(p-1) exactly")
for kappa,p in ((3,7),(4,13),(5,11),(6,13)):
    chi = chi_table(p,kappa)
    for e1 in range(1,kappa):
        for e3 in (1,):
            e2, e4 = (-e1) % kappa, (-e3) % kappa
            S = 0
            for aj,ajp,bi,bip in product(range(p),repeat=4):
                S += chi(e1,aj+bi)*chi(e2,ajp+bi)*chi(e3,aj+bip)*chi(e4,ajp+bip)
            print(f"  kappa={kappa} p={p} e=({e1},{e2},{e3},{e4}): Sigma={S.real:.3f}{S.imag:+.1e}i, p^2(p-1)={p*p*(p-1)}")
            break
print("C'. larger sample for the Chebotarev illustration")
X = 400000
sieve = bytearray([1])*(X+1); sieve[0]=sieve[1]=0
for i in range(2,int(X**0.5)+1):
    if sieve[i]: sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
for kappa in (4,5):
    ps = [p for p in range(kappa+1,X) if p%kappa==1 and sieve[p]]
    kp = lambda a,p: pow(a,(p-1)//kappa,p)==1
    f2 = sum(kp(2,p) for p in ps); f235 = sum(kp(2,p) and kp(3,p) and kp(5,p) for p in ps)
    big = [p for p in ps if all(kp(a,p) for a in (2,3,5,7,11,13))]
    print(f"  kappa={kappa}: {len(ps)} primes; 2 power: {f2/len(ps):.4f} (exp {1/kappa:.4f}); 2,3,5: {f235/len(ps):.5f} (exp {kappa**-3:.5f}, count {f235}); 2..13 all powers: {big[:4]}")
