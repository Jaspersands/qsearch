# Exact arithmetic checks for appendix-codimension.tex and main.tex lines 1155-1197 (codim checker).
import sys, os, math
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from liealg import primes_upto, bch_coeffs

out = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); out.append(s)

# 1. Birthday branch constants (Prop. app-codim-birthday and part (ii) from FC(iii)).
P = primes_upto(64 * 60 * 60 + 10)
bad = []
for k in range(1, 61):
    lim = 64 * k * k
    plist = [p for p in P if p < lim]
    pmax = plist[-1]
    for p in [pmax, plist[0]]:
        I = p ** k
        B = math.isqrt(2 * I) + 2
        if not (B * (B - 1) > 2 * I): bad.append(("collision", k, p))
        if not (B * B <= 16 * I): bad.append(("B<=4p^{k/2}", k, p))      # B <= 4 p^{k/2}
        if not (B <= 4 * (8 * k) ** k): bad.append(("log2B<=k(3+log2k)+2", k, p))
    # p <= 2k branch: B <= 4 (2k)^{k/2}  <=>  B^2 <= 16 (2k)^k
    for p in [q for q in P if q <= 2 * k]:
        B = math.isqrt(2 * p ** k) + 2
        if not (B * B <= 16 * (2 * k) ** k): bad.append(("p<=2k", k, p))
log("birthday constant checks k=1..60, failures:", bad)

# 2. BCH coefficients: denominators of z/(1-e^{-z}) below degree c (thm:uniform-compilation(i))
for c in range(2, 9):
    b = bch_coeffs(c)
    dens = [x.denominator for x in b]
    mx = max(dens)
    primes_ok = all(all(q <= c for q in range(2, d + 1) if d % q == 0 and all(q % r for r in range(2, q))) for d in dens)
    log(f"c={c}: coefficients {[str(x) for x in b]}; max denominator {mx} (> c: {mx > c}); prime factors <= c: {primes_ok}")

# 3. inequality x^r <= max(r^{2r}, 2^16, 2^x) (proof of cor:fpt-r(i)); grid check in logs
worst = None
for r in range(1, 60):
    for i in range(1, 4000):
        x = 1 + i * 0.05
        lhs = r * math.log2(x)
        rhs = max(2 * r * math.log2(r) if r > 1 else 0.0, 16.0, x)
        if lhs > rhs + 1e-9:
            worst = (r, x, lhs, rhs); break
    if worst: break
log("x^r <= max(r^{2r},2^16,2^x) grid r<60, 1<=x<=201: counterexample:", worst)

# 4. cor:fpt-r filiform profiles r=3,5,9 at p=c+1, eps=1/3, least public arities of (R1)
def kappa(d, p): return math.gcd(d, p - 1)
def beta(M, n0, a, p, kap):
    h = (p - 1) // kap
    q = Fraction(h + 1, p)
    return Fraction(4, h ** (n0 - 1)) / q ** a + Fraction(p ** a - 1, (p - 1) * p ** (M - n0))
def least_M(a, p, kap, tau):
    M = 1
    while True:
        for n0 in range(1, M + 1):
            if beta(M, n0, a, p, kap) <= tau:
                return M, n0
        M += 1
def B_is(d, a):
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** math.ceil(math.log2(d + 1))
for r in [3, 5, 9]:
    m, c, p = r + 2, r + 1, r + 2
    eps = Fraction(1, 3)
    # S = m + ceil(log_p(3/eps)) = m + ceil(log_p 9)
    t = 0
    while p ** t < 9: t += 1
    S = m + t
    g = {d: r - d + 2 for d in range(2, c + 1)}
    Ms = {}; n = 1; log2Q_zs = None
    for d in range(2, c + 1):
        kap = kappa(d, p)
        if kap == 1:
            Ms[d] = g[d] + 1
        elif kap == p - 1:
            Ms[d] = ('ZS', g[d] * (p - 1) + 1, 'S1', B_is(d, g[d]))
        else:
            tau = eps / (9 * (c - 1) * S * n)
            Ms[d] = least_M(g[d], p, kap, tau)[0]
        n *= Ms[d] if not isinstance(Ms[d], tuple) else 1
    prod_rest = 1
    for d in range(2, c + 1):
        if not isinstance(Ms[d], tuple): prod_rest *= Ms[d]
    zs = [v for v in Ms.values() if isinstance(v, tuple)][0]
    Qzs = c * S * prod_rest * zs[1]; Qs1 = c * S * prod_rest * zs[3]
    log(f"fpt-r filiform r={r}: p={p} S={S} arities={Ms}; log2 Q (zero-sum)={math.log2(Qzs):.2f}, (Schedule 1)={math.log2(Qs1):.2f}")
# NOTE: n_d for grades after the zero-sum grade does not arise (it is the last grade d=c).

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_arith.out"), "w") as fh:
    fh.write("\n".join(out) + "\n")
