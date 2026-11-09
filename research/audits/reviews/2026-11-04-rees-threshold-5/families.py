"""First-moment (independent-cell) counts of normalised contractions in the full problem
and in the symmetric families of section 2.  [float, exact formulas]
  G  : full problem, strict cells:      mu_G  = p^(2K-2) (h/p)^(K^2-1)
  H  : half-shift family (K, h even):    mu_H  = p^(K-1) (h/p)^(K^2/2-1)
  P  : Paley transpose family (h even): mu_P  = (K-1) p^(K-2) (h/p)^(K(K-1)/2-1)  (K zero cells)
  T1 : symmetric transpose family:       mu_T1 = K p^(K-1) (h/p)^(K(K+1)/2-1)
  So : shift family with orbit length o (g = K/o amplitudes): p^(2g-1)(h/p)^(Kg-1) per (r,t,lambda)
Also prints mu_G at the largest known exceptional primes."""
from math import log
def mus(K, p):
    h = (p - 1) / K; q = h / p
    d = {"G": p ** (2*K-2) * q ** (K*K-1), "T1": K * p ** (K-1) * q ** (K*(K+1)//2 - 1)}
    if (h % 2 == 0):
        d["P"] = (K-1) * p ** (K-2) * q ** (K*(K-1)//2 - 1)
        if K % 2 == 0:
            d["H"] = p ** (K-1) * q ** (K*K//2 - 1)
    return d
def cross(K, fam, par):
    # smallest p (real, p = 1 mod 2K for h even, p = K+1 mod 2K for h odd) with mu >= 1, by bisection on p
    lo, hi = K + 1.0, 1e40
    f = lambda p: mus(K, p if par == 0 else p).get(fam)
    for _ in range(200):
        mid = (lo * hi) ** 0.5
        h = (mid - 1) / K; q = h / mid
        if fam == "G": v = (2*K-2)*log(mid) + (K*K-1)*log(q)
        elif fam == "H": v = (K-1)*log(mid) + (K*K//2-1)*log(q)
        elif fam == "P": v = log(K-1) + (K-2)*log(mid) + (K*(K-1)//2-1)*log(q)
        else: v = log(K) + (K-1)*log(mid) + (K*(K+1)//2-1)*log(q)
        if v >= 0: hi = mid
        else: lo = mid
    return hi
print("crossing points p* (mu = 1), and p*/K^((K+1)/2)")
for K in range(4, 11):
    row = [f"K={K}", f"K^((K+1)/2)={K**((K+1)/2):.4g}"]
    for fam in ("G", "H", "P", "T1"):
        if fam == "H" and K % 2: row.append("H: -"); continue
        c = cross(K, fam, 0)
        row.append(f"{fam}: {c:.4g} ({c / K**((K+1)/2):.3f})")
    print("  ".join(row))
print()
print("exponents e with p* ~ K^e: G (K+1)/2, H (K^2-2)/(2K-2), P (K+1)/2, T1 (K+2)/2")
print()
largest = {4: 53, 5: 181, 6: 859, 7: 3221, 8: 8377, 9: 17551}
print("mu at the largest known exceptional primes (8377, 17551: lower bounds, scans running)")
for K, p in largest.items():
    d = mus(K, p)
    print(f"K={K} p={p} h={'even' if ((p-1)//K) % 2 == 0 else 'odd'} " + " ".join(f"mu_{k}={v:.3g}" for k, v in d.items()))
