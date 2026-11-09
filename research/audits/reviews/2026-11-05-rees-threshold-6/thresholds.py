"""Thresholds for rectangular contractions RC(D, rows R), |R| = r, R a subgroup of Z_D
(or any subset containing 0).  W(D,r): Weil with beta fixed (every distinct beta works);
T_R(D,r): second moment over beta + union bound over the D columns (some beta works).
Both are 'for every prime p > threshold'; monotonicity is proved in the report (Lemma 3.3)."""
from mpmath import mp, mpf, sqrt, exp
mp.dps = 40

def W(D, r):
    A = mpf(r - 1 - mpf(r)/D) * D**r + 1
    c = mpf(r) * D**(r - 1)
    return ((A + sqrt(A*A + 4*c))/2)**2

def lhs(D, r, p):
    p = mpf(p)
    Delta = ((D-1)*(D-2)*sqrt(p) + 2*(D-1))/(p - D - 1)
    first = mpf(D)**r * p**(r-1)/(p-1)**r
    E = (r-1)*Delta**2 + (1+Delta)*exp((r-1)*Delta)*(r-1)**2*Delta**2/2
    return first + E

def TR(D, r):
    target = mpf(1)/(D-1)
    lo, hi = mpf(D+2), mpf(10)**30
    if lhs(D, r, hi) >= target: return None
    for _ in range(300):
        mid = sqrt(lo*hi)
        if lhs(D, r, mid) < target: hi = mid
        else: lo = mid
    return hi

if __name__ == "__main__":
    print("D r   W(D,r)          T_R(D,r)        min")
    for D, r in [(4,2),(6,2),(6,3),(8,2),(8,4),(9,3),(12,2),(12,3),(12,4),(12,6),(16,2),(16,4),(18,2),(18,3),(24,2),(27,3),(32,2),(64,2),(128,2)]:
        w = W(D, r); t = TR(D, r)
        m = min(w, t) if t is not None else w
        print(f"{D:3d} {r:2d}  {float(w):14.6g}  {float(t) if t else float('nan'):14.6g}  {float(m):14.6g}")
    print("bound ((D-1)^2+1)^2 vs W(D,2):")
    for D in [4,8,16,32,64,128,256,1024]:
        print(D, float(W(D,2)), ((D-1)**2+1)**2, W(D,2) < ((D-1)**2+1)**2)

# ---------------------------------------------------------------------------
# Union targets (Lemma 3.4 of the report): rows R (|R| = l), each cell must lie in a
# union of k cosets of Q_0 (index kappa); beta fixed with column 0 satisfied.
import cmath
def union_consts(kappa, K, l):
    """returns (c0, G, B, C): count >= c0^l (p - l) - B sqrt(p) - C"""
    c = [abs(sum(cmath.exp(-2j*cmath.pi*m*s/kappa) for m in K))/kappa for s in range(kappa)]
    c0 = mpf(c[0]); G = mpf(sum(c[1:])); F = c0 + G
    B = l*G*F**(l-1) - (F**l - c0**l)
    C = l*(F**l - c0**l) - l*G*F**(l-1)
    return c0, G, B, C

def Wunion(kappa, K, l):
    c0, G, B, C = union_consts(kappa, K, l)
    a = c0**l; # a p - B sqrt p - (C + a l) > 0
    cc = C + a*l
    s = (B + sqrt(B*B + 4*a*cc))/(2*a)
    return s*s

if __name__ == "__main__":
    print("union step 1 (rows Z_kappa, target K), Weil threshold:")
    for kappa, K in [(5,[0,1]),(5,[0,1,2]),(7,[0,1]),(7,[0,1,2]),(7,[0,1,2,3]),(7,[0,1,3])]:
        print(kappa, K, float(Wunion(kappa, K, kappa)))
    # sanity: K = [0] must reproduce T_W(kappa)
    for kappa in [3,4,5]:
        A = (kappa-2)*kappa**kappa + 1
        TW = ((A + sqrt(A*A + 4*kappa**kappa))/2)**2
        print("check T_W", kappa, float(Wunion(kappa,[0],kappa)), float(TW))
