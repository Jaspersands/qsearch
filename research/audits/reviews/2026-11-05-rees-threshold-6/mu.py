"""Random-model count of normalised two-level contractions (beta_0 = 0, alpha_0 = 1):
mu(p) = p^(2k-2) * q^(k^2-1), q = ((p-1)/k + 1)/p (each of the k^2-1 free cells lands in
its coset or at 0).  Evaluated at the largest known exceptional prime of E_2(k); the
crossover mu = 1 is near k^((k+1)/2).  Used for the route-(4) calibration in the report."""
from mpmath import mp, mpf, log
mp.dps = 30
known = {4: 53, 5: 181, 6: 859, 7: 3221, 8: 12377, 9: 17929}
def mu(k, p):
    p = mpf(p); q = ((p-1)/k + 1)/p
    return p**(2*k-2) * q**(k*k-1)
print("k  p_max  mu(p_max)  p_max/k^((k+1)/2)  crossover p (mu=1)")
for k, p in known.items():
    lo, hi = mpf(k+1), mpf(10)**12
    for _ in range(200):
        m = (lo+hi)/2
        if mu(k, m) < 1: lo = m
        else: hi = m
    print(k, p, float(mu(k, p)), float(p/mpf(k)**((k+1)/mpf(2))), float(hi))
