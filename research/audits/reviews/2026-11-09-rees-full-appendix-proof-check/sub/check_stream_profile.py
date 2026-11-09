"""Independent exact checks (sub, 2026-11-09):
 (1) Prop. app-sub-stream(a): exact tail P(attempts > r^2 B) of the level chain with
     p_k = (r-k)/(r(k+1)), against r 2^-B (r = 2..10, B = 1..8), Fractions.
 (2) Remark app-sub-profile and the last paragraph of Section sec:subspace:
     B_leaf, t, b, ell, T, B, N, raw copies, M*ell, the multiple-of-p route; exact
     big-integer arithmetic.
 (3) Remark app-sub-sharper inequalities on a grid.
 (4) Remark rem:mixed-source(i) rounding identities on random spectra (exact Fractions).
"""
import math, random
from fractions import Fraction as F

print('(1) streaming tails')
worst = (0, None)
for r in range(2, 11):
    for B in range(1, 9):
        exact = (r <= 4 and B <= 4)
        one = F(1) if exact else 1.0
        pk = [(F(r - k, r * (k + 1)) if exact else (r - k) / (r * (k + 1))) for k in range(1, r)]
        N = r * r * B
        # level chain: state k in 1..r, start at 1 (exact Fractions only for small cases)
        dist = [one * 0] * (r + 1)
        dist[1] = one
        for _ in range(N):
            new = [one * 0] * (r + 1)
            new[r] = dist[r]
            for k in range(1, r):
                new[k + 1] += dist[k] * pk[k - 1]
                new[k] += dist[k] * (1 - pk[k - 1])
            dist = new
        tail = 1 - dist[r]
        bound = r / 2 ** B
        ratio = float(tail) / bound
        if ratio > worst[0]:
            worst = (ratio, (r, B))
        assert ratio <= 1 - 1e-9, (r, B, float(tail), bound)
print(f'   all tails <= r 2^-B (exact for r,B <= 4, float otherwise); largest ratio tail/bound = '
      f'{float(worst[0]):.4f} at (r,B) = {worst[1]}')
# product of p_k equals r^-r
for r in range(1, 12):
    prod = F(1)
    for k in range(1, r):
        prod *= F(r - k, r * (k + 1))
    assert prod == F(1, r ** r)
print('   prod_{k<r} p_k = r^-r for r = 1..11: ok')

print('(2) profile p=43, c=9, m=19, n=97, delta=1/10, eps=1/3')
p, c, m = 43, 9, 19
g = {2: 17, 3: 16, 4: 14, 5: 12, 6: 9, 7: 6, 8: 3, 9: 1}
n = m + sum(g.values())
eps = F(1, 3)
delta = F(1, 10)


def ceil_log(x, base):
    # smallest integer t >= 0 with base^t >= x (x rational > 0)
    t = 0
    while F(base) ** t < x:
        t += 1
    return t


def Bd(d, a):
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** math.ceil(math.log2(d + 1))


# careful: ceil(log2(d+1)) for d+1 a power of two (d = 3, 7) must be exact
def clog2_int(x):
    return (x - 1).bit_length()


def Bd_exact(d, a):
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** clog2_int(d + 1)


assert all(Bd(d, a) == Bd_exact(d, a) for d in range(2, 10) for a in range(0, 20))
prodB = 1
for d in range(2, c + 1):
    prodB *= Bd_exact(d, g[d])
t = ceil_log(12 / eps, p)          # B_leaf at eps/4: t = ceil(log_p(3/(eps/4)))
Bleaf = (m + t) * prodB
tau = ceil_log(3 / eps, p)
Qq = c * (m + tau) * prodB


def log2big(x):
    # float log2 of a big positive integer or Fraction
    if isinstance(x, F):
        return log2big(x.numerator) - log2big(x.denominator)
    L = x.bit_length()
    if L < 1000:
        return math.log2(x)
    return (L - 60) + math.log2(x >> (L - 60))


floor_nlog = (p ** n).bit_length() - 1      # floor(n log2 p)
arg = 8 * Bleaf / eps                        # Fraction
ceil_arg = clog2_int(math.ceil(arg))         # ceil(log2(8 B_leaf/eps)); arg is an integer here
assert arg.denominator == 1
b = floor_nlog + 1 + ceil_arg
gamma = delta ** 2 / 2
ell = math.ceil(F(b) / gamma)
M = 14
T = M * ell * Bleaf
print(f'   n={n}, t={t}, tau={tau}, log2 B_leaf={log2big(Bleaf):.2f}, log2 Q_q={log2big(Qq):.2f}')
print(f'   floor(n log2 p)={floor_nlog}, ceil(log2(8B_leaf/eps))={ceil_arg}, b={b}, ell={ell}, '
      f'M*ell={M*ell}, log2 T={log2big(T):.2f}')
for r in (1, 2, 8, 32):
    if r == 1:
        print(f'   r=1: N=0, raw copies = T = 2^{log2big(T):.2f}')
        continue
    x = 8 * r * T / eps
    assert x.denominator == 1
    Bc = clog2_int(int(x))
    N = r * r * Bc
    print(f'   r={r}: B={Bc}, N={N}, raw copies T(N+1) = 2^{log2big(T*(N+1)):.2f}')
ellp = p * math.ceil(F(ell, p))
print(f'   multiple-of-p route: ell -> {ellp}, c*ell = {c*ellp}; check c*p*ceil(ell/p) <= c(ell+p): '
      f'{c*ellp <= c*(ell+p)}; crossover M*ell/c = {M*ell/c:.1f}')
# step (3) alone: smallest ell' with (1-gamma)^ell' * p^{n/2}/2 * B_leaf <= eps/16 (the Run-1 share)
need = math.log(16 * float(F(1, 2)) * 1) # placeholder (not used)
ell_alt = math.ceil((b * math.log(2)) / float(gamma))
print(f'   ell*ln2 = {ell*math.log(2):.0f}; ceil(b ln2/gamma) = {ell_alt}')

print('(3) Remark app-sub-sharper')
bad = 0
for i in range(1, 2001):
    y = i / 100.0
    if 1 - math.exp(-y) < min(y / 2, 0.5) - 1e-15:
        bad += 1
for r in range(1, 65):
    for j in range(1, 501):
        dl = j / 500.0
        g_r = 1 - (1 - dl * dl) ** (r / 2)
        if g_r < min(r * dl * dl / 4, 0.5) - 1e-15:
            bad += 1
        if (1 - dl * dl) ** (r / 2) > 1 - dl * dl / 2 + 1e-15:
            bad += 1
print(f'   violations: {bad}')

print('(4) Remark mixed-source(i) rounding identities (exact)')
random.seed(7)
viol = 0
for trial in range(60):
    rbar = random.randint(1, 6)
    dl = F(random.randint(25, 100), 100)
    w = dl / (16 * rbar)
    J = math.ceil(1 / w)
    M0 = 1
    while M0 < 8 * rbar * 2:   # beta = 1/2 (keeps the exact loop small)
        M0 *= 2
    rank = random.randint(1, rbar)
    cuts = sorted(F(random.randint(1, 999), 1000) for _ in range(rank - 1))
    lams = [b2 - a2 for a2, b2 in zip([F(0)] + cuts, cuts + [F(1)])]
    lams = [l for l in lams if l > 0]
    bad_a = 0
    for a in range(M0):
        th = [w * (1 + F(a, M0) + j) for j in range(J)]
        rt = [w * sum(1 for t_ in th if lam >= t_) for lam in lams]
        for lam, x in zip(lams, rt):
            if not (lam - 2 * w < x <= lam):
                viol += 1
            if x != w * max(0, math.floor(lam / w - F(a, M0))):
                viol += 1
        if not (sum(l - x for l, x in zip(lams, rt)) < dl / 8):
            viol += 1
        ranks = sorted({sum(1 for lam in lams if lam >= t_) for t_ in th} - {0}, reverse=True)
        if len(ranks) > rbar or sum(ranks) > min(F(rbar * (rbar + 1), 2), 16 * rbar / dl):
            viol += 1
        if min(abs(t_ - lam) for t_ in th for lam in lams) < w / (4 * M0):
            bad_a += 1
    if bad_a > len(set(lams)):
        viol += 1
print(f'   violations: {viol}')
