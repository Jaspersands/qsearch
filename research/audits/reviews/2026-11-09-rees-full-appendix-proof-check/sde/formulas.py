"""Exact checks of closed forms in appendix-sde-side.tex and main.tex 645-763.

(1) M_J(a) (rem:sde-block-steered) against its derivation and the stated
    special cases J=2 and J=3.
(2) D_J(q) (rem:sde-worst-case(b)): D_3(q) = floor((q+2)^2/4) and the bound
    D_J(q) <= q^2/(2(J-1)) + q(1/(J-1)+5/2) for J >= 3.
(3) Schedule-1 query exponent 1 + sum_d d*ceil(log2(d+1)) (=145 at c=9) and the
    combined-rule exponent max over primes (claims: unchanged for c<=7, -2 at
    c=8,9, 143 at c=9).
(4) Run-count arithmetic r_run (rem:is-runtime).
(5) Misc numbers: B_4(2), G(kappa,1) sizes, Psde column counts.
"""
from math import ceil, log2, gcd, comb, floor
from fractions import Fraction
import sympy

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
        print("FAIL:", msg)

# (1) M_J(a)
def M_formula(J, a):
    mu, r0 = divmod(a, J - 1)
    return 1 + mu * (a + 1) - (J - 1) * mu * (mu - 1) // 2 + ((r0 + 1) if r0 > 0 else 0)

def M_derived(J, a):
    # rounds: dim U grows by J-1 per round while possible; a round at dim U = u
    # takes a-u+1 columns; final partial round adds r0 dims with r0+1 columns;
    # then one finishing column.
    u, cols = 0, 0
    while a - u >= J - 1:
        cols += a - u + 1
        u += J - 1
    if a - u > 0:
        cols += a - u + 1
        u = a
    return cols + 1

for J in range(2, 12):
    for a in range(0, 200):
        check(M_formula(J, a) == M_derived(J, a), f"M_J formula J={J} a={a}")
for a in range(0, 300):
    check(M_formula(2, a) == (a + 1) * (a + 2) // 2, f"M_2 a={a}")
    check(M_formula(3, a) == (a + 2) ** 2 // 4 + (a % 2), f"M_3 a={a}")
# asymptotic a^2/(2(J-1)) + O(a)
for J in range(3, 10):
    worst = max(abs(M_formula(J, a) - a * a / (2 * (J - 1))) / max(a, 1) for a in range(1, 2000))
    print(f"M_J: J={J}  max |M_J(a)-a^2/(2(J-1))|/a over a<2000 = {worst:.3f}")

# (2) D_J(q)
def D_table(J, qmax):
    D = [0] * (qmax + 1)
    for q in range(1, qmax + 1):
        D[q] = max(k + 1 + D[q - min(J - 1, k)] for k in range(1, q + 1))
    return D

D3 = D_table(3, 600)
for q in range(1, 601):
    check(D3[q] == (q + 2) ** 2 // 4, f"D_3({q})={D3[q]} vs {(q+2)**2//4}")
worst_slack = {}
for J in range(3, 25):
    D = D_table(J, 800)
    s = min(Fraction(q * q, 2 * (J - 1)) + q * (Fraction(1, J - 1) + Fraction(5, 2)) - D[q] for q in range(1, 801))
    worst_slack[J] = float(s)
    check(s >= 0, f"D_J bound fails for J={J}")
print("D_J bound: min slack over q<=800 per J:", {J: round(v, 2) for J, v in worst_slack.items()})
# D_J(a)+a vs M_J(a): how they compare (both quadratic/(2(J-1)))
print("D_3(a)+a vs M_3(a) for a=2..10:", [(a, D3[a] + a, M_formula(3, a)) for a in range(2, 11)])

# (3) exponents
def sched1_exp(c):
    return 1 + sum(d * ceil(log2(d + 1)) for d in range(2, c + 1))
check(sched1_exp(9) == 145, "ReesClassNineQueryExp")

def combined_exp(p, c):
    e = 1
    for d in range(2, c + 1):
        k = gcd(d, p - 1)
        if k == 1:
            e += 1
        elif p >= 16 * k ** (2 * k + 2):
            e += 2
        else:
            e += k * ceil(log2(k + 1))
    return e

primes = list(sympy.primerange(3, 400000))
for c in range(2, 10):
    best = max((combined_exp(p, c), p) for p in primes if p > c)
    print(f"c={c}: Schedule-1 exponent {sched1_exp(c)}, combined max over p<4e5: {best[0]} at p={best[1]}, drop {sched1_exp(c)-best[0]}")
# argument that p < 4e5 suffices: for p >= 4e5 grade 2 and grade 3 (if kappa=3) are at
# exponent 2, so the max over larger p is at most the max with those grades fixed, which is
# attained already by a smaller prime of the same residue pattern if one exists; we just
# also report the value at the first prime = 1 mod 2520.
print("2521 prime:", sympy.isprime(2521), " combined_exp(2521,9) =", combined_exp(2521, 9))

# (4) r_run arithmetic
def v(q, n):
    c = 0
    while n % q == 0:
        n //= q; c += 1
    return c
for kappa in range(2, 61):
    qs = sympy.primefactors(kappa)
    for p in sympy.primerange(3, 20000):
        if (p - 1) % kappa:
            continue
        nu = sum(v(q, p - 1) for q in qs)
        rrun = nu - min(v(q, (p - 1) // kappa) for q in qs)
        if len(qs) == 1:
            check(rrun == v(qs[0], kappa), f"r_run=e kappa={kappa} p={p}")
        else:
            check(1 + max(v(q, p - 1) for q in qs) <= rrun <= nu, f"r_run bounds kappa={kappa} p={p}")
        check(nu <= ceil(log2(p)) - 1, f"nu<=b-1 kappa={kappa} p={p}")

# (5) misc numbers
G = lambda d, a: d ** (d * (d - 1) // 2) * (a + 1) ** d
B = lambda d, a: G(d, a) ** ceil(log2(d + 1))
print("B_4(2) =", B(4, 2), f"= {B(4,2):.3e}")
print("G(4,1) =", G(4, 1), " G(4,1)^2 =", G(4, 1) ** 2, " G(5,1) =", G(5, 1), " G(3,1)^2 =", G(3, 1) ** 2)
msym = lambda k, a: (a + 1) * ((k - 1) * a + 1)
check(msym(5, 2) == 27 and msym(5, 8) == 297 and msym(4, 3) == 40 and msym(2, 3) == 16, "Psde columns")
# profile bound: prod (d-1)(g+1)^2 with g_d <= r-d+2 vs r!((r+1)!)^2 (main.tex 712)
import math, itertools
for r in range(1, 15):
    for c in range(2, r + 2):
        lhs = math.factorial(c - 1) * (math.factorial(r + 1) // math.factorial(r - c + 2)) ** 2
        check(lhs <= math.factorial(r) * math.factorial(r + 1) ** 2, f"profile bound r={r} c={c}")
# E_2 scale ratios quoted in main.tex 721/726
for k, pmax in [(4, 53), (5, 181), (6, 859), (7, 3221)]:
    print(f"kappa={k}: max E_2 / kappa^((kappa+1)/2) = {pmax / k ** ((k + 1) / 2):.3f}")
print("14281/8^4.5 =", 14281 / 8 ** 4.5, " 20107/9^5 =", 20107 / 9 ** 5)
print("kappa^2-3kappa+3:", {k: k * k - 3 * k + 3 for k in range(2, 13)})
print("ALL OK" if ok else "SOME CHECK FAILED")
