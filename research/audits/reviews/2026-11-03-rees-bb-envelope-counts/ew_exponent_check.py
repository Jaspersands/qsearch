"""Exact checks for the counts of Theorem bb-envelope (referee 2, items 2.5 / P10).

Run from the repo root:
  /opt/anaconda3/bin/python -B research/audits/reviews/2026-11-03-rees-bb-envelope-counts/ew_exponent_check.py

Exact integers throughout; logarithms are printed only.  Sections:
  A. E_W(c) and E_1(c) for c = 2..9 by the analytic rule of the report (Section 3.2):
     E_W(c) = E_1(c) if some prime p < 1024 has lcm(2..c) | p-1, else E_1(c) - 2.
     Cross-checked by a scan over every prime c < p < PRIME_LIMIT.
  B. The constant K_c and log2(c K_c); the inequality prod_d M_d <= K_c (m+1)^{E_W(c)-1}
     on exact profiles.
  C. Monotonicity of Q_core in m and superadditivity of phi(x) = x(x+t)(x+1)^{E-1}.
  D. The all-exponent-p bound  sum_p psi(n_p) <= 2^E (L+t)(L+1)^{E-1}  on random partitions.
  E. Counterexample to the displayed inequality n_p^2 <= k d in thm:bb-envelope(ii):
     cyclic Sylow subgroups with s = 1.
  F. The chart-acquisition group-oracle calls omitted from thm:bb-envelope(iii): G = C_3,
     c = 2, s redundant generators.
"""
from fractions import Fraction
from math import gcd, log2
from random import Random

PRIME_LIMIT = 200_000


def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n + 1) if sieve[i]]


PRIMES = primes_upto(PRIME_LIMIT)
PRIME_SET = set(PRIMES)


def bitlen(x):
    """ceil(log2(x+1)) for x >= 0; equals ceil(log2(d+1)) for d = x."""
    return x.bit_length()


def ceil_log(base, x):
    """Least k >= 0 with base**k >= x, for x > 0 (Fraction or int)."""
    x = Fraction(x)
    k, v = 0, 1
    while v < x:
        v *= base
        k += 1
    return k


def B(d, a):
    """Ivanyos--Santha sufficient arity B_d(a) = [d^{d(d-1)/2} (a+1)^d]^{ceil log2(d+1)}."""
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** bitlen(d)


def grade_rule(p, d):
    """Combined rule of rem:combined-schedule at grade d: ('lin'|'two'|'S1', kappa_d)."""
    k = gcd(d, p - 1)
    if k == 1:
        return "lin", 1
    if p >= 16 * k ** (2 * k + 2):
        return "two", k
    return "S1", k


def arity_W(p, d, g):
    rule, k = grade_rule(p, d)
    if rule == "lin":
        return g + 1
    if rule == "two":
        return (g + 1) * ((k - 1) * g + 1)
    return B(k, g)


def e_d(p, d):
    rule, k = grade_rule(p, d)
    return {"lin": 1, "two": 2, "S1": k * bitlen(k)}[rule]


def E1(c):
    return 1 + sum(d * bitlen(d) for d in range(2, c + 1))


def EW_scan(c):
    best, arg = -1, None
    for p in PRIMES:
        if p <= c:
            continue
        e = 1 + sum(e_d(p, d) for d in range(2, c + 1))
        if e > best:
            best, arg = e, p
    return best, arg


def lcm(a, b):
    return a * b // gcd(a, b)


def EW_analytic(c):
    """Section 3.2 of the report: the max over ALL primes p > c.

    e_d(p) <= d ceil(log2(d+1)) for every p, with equality iff kappa_d = d and
    p < 16 d^{2d+2}.  The binding threshold is d = 2 (16 * 2^6 = 1024); all other
    thresholds exceed 1024.  So E_W(c) = E_1(c) iff some prime p < 1024 has
    lcm(2..c) | p - 1.  Otherwise every prime loses at least 2 (the smallest possible
    loss, at grade 2 via the two-level schedule), and the loss 2 is attained by any
    prime p >= 1024 with lcm(2..c) | p - 1, which exists by Dirichlet; the first one is
    returned as witness."""
    L = 1
    for d in range(2, c + 1):
        L = lcm(L, d)
    small = [p for p in range(L + 1, 1024, L) if p in PRIME_SET]
    if small:
        return E1(c), small[0], "E_1 attained"
    p = L + 1
    while p not in PRIME_SET or p < 1024:
        p += L
    return E1(c) - 2, p, "E_1 - 2 (grade 2 two-level, all other grades at Schedule 1)"


def K(c):
    out = 1
    for d in range(2, c + 1):
        out *= d ** (d * (d - 1) * bitlen(d) // 2)
    return out


def Q_core(c, p, grades, t):
    """c (m + t) prod_{d=2}^c M_d with M_d from the combined rule; grades = (g_1..g_c)."""
    m = grades[0]
    P = 1
    for d in range(2, c + 1):
        P *= arity_W(p, d, grades[d - 1])
    return c * (m + t) * P


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


# ------------------------------------------------------------------ A. exponents
say("== A. E_1(c), E_W(c) for c = 2..9: analytic rule vs scan over primes <", PRIME_LIMIT, "==")
expected_EW = {2: 5, 3: 11, 4: 23, 5: 38, 6: 56, 7: 77, 8: 107, 9: 143}
expected_E1 = {2: 5, 3: 11, 4: 23, 5: 38, 6: 56, 7: 77, 8: 109, 9: 145}
for c in range(2, 10):
    e1 = E1(c)
    ew_an, p_an, why = EW_analytic(c)
    ew_sc, p_sc = EW_scan(c)
    say(f"c={c}: E_1={e1}  E_W(analytic)={ew_an} at p={p_an} [{why}]  E_W(scan)={ew_sc} first at p={p_sc}")
    assert e1 == expected_E1[c], (c, e1)
    assert ew_an == ew_sc == expected_EW[c], (c, ew_an, ew_sc)
    # the attaining prime of the analytic rule attains the scan value
    assert 1 + sum(e_d(p_an, d) for d in range(2, c + 1)) == ew_an
# grade-2 threshold is binding: all other thresholds exceed 1024
assert 16 * 2 ** 6 == 1024 and all(16 * d ** (2 * d + 2) > 1024 for d in range(3, 10))
# monotonicity used in the proof: x -> x ceil(log2(x+1)) nondecreasing, and >= 2 for x >= 2
assert all(k * bitlen(k) <= d * bitlen(d) for d in range(2, 10) for k in range(1, d + 1))
assert all(d * bitlen(d) >= 2 for d in range(2, 10))
say("A passed: E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143; E_1(c) = ..., 109, 145.")

# ------------------------------------------------------------------ B. constants
say("\n== B. K_c, log2(c K_c), and prod M_d <= K_c (m+1)^{E_W-1} ==")
for c in range(2, 10):
    say(f"c={c}: log2 K_c = {log2(K(c)):.1f}   log2(c K_c) = {log2(c * K(c)):.1f}")
assert round(log2(9 * K(9))) == 1206
rng = Random(20261103)
checks = 0
for c in range(2, 10):
    Kc, E = K(c), expected_EW[c]
    for p in [q for q in PRIMES if q > c][:40] + [2521, 104729, 199999]:
        if p not in PRIME_SET or p <= c:
            continue
        for _ in range(6):
            m = rng.randint(1, 60)
            grades = [m] + sorted((rng.randint(0, m) for _ in range(c - 1)), reverse=True)
            P = 1
            for d in range(2, c + 1):
                P *= arity_W(p, d, grades[d - 1])
            # per-grade: M_d <= C_d (g_d+1)^{e_d} with C_d <= d^{d(d-1)ceil log2(d+1)/2}
            for d in range(2, c + 1):
                g = grades[d - 1]
                assert arity_W(p, d, g) <= d ** (d * (d - 1) * bitlen(d) // 2) * (g + 1) ** e_d(p, d)
            assert P <= Kc * (m + 1) ** (E - 1)
            checks += 1
say(f"B passed on {checks} exact profiles.")

# ------------------------------------------------------------------ C. monotone, superadditive
say("\n== C. Q_core increasing in m; phi superadditive ==")
for c in (2, 3, 5, 9):
    for p in (c + 1 if (c + 1) in PRIME_SET else 11, 43, 2521):
        t = 7
        prev = 0
        for m in range(0, 25):
            q = Q_core(c, p, (m,) * c, t)
            assert q >= prev
            prev = q
# phi(x) = x (x+t) (x+1)^(E-1): superadditive on integers >= 0 (convex with phi(0)=0)
for E in (1, 2, 5, 11, 143):
    for t in (0, 1, 7, 50):
        phi = lambda x: x * (x + t) * (x + 1) ** (E - 1)
        for a in range(0, 30):
            for b in range(0, 30):
                assert phi(a) + phi(b) <= phi(a + b)
say("C passed.")

# ------------------------------------------------------------------ D. all exponent p
say("\n== D. all e_p = 1: sum_p (n_p+t)(n_p+1)^(E-1) <= 2^E (L+t)(L+1)^(E-1) ==")
for E in (5, 11, 143):
    for t in (1, 7, 300):
        for _ in range(300):
            r = rng.randint(1, 12)
            parts = [rng.randint(1, 8) for _ in range(r)]
            L = sum(parts)
            lhs = sum((n + t) * (n + 1) ** (E - 1) for n in parts)
            assert lhs <= 2 ** E * (L + t) * (L + 1) ** (E - 1)
say("D passed.")

# ------------------------------------------------------------------ E. n_p^2 <= k d fails
say("\n== E. Counterexample to the displayed chain in (ii): n_p^2 <= k d ==")
def k_samples(p, ell, eps):
    return ell // int(log2(p)) if False else (int(Fraction(ell) / Fraction(log2(p)))) + ceil_log(p, Fraction(8 * ell) / eps)

for (p, e, eps) in [(3, 3, Fraction(1, 2)), (5, 3, Fraction(1, 2)), (3, 3, Fraction(1, 3)), (3, 4, Fraction(1, 2))]:
    # G = C_{p^e}, s = 1, c = 2 (class 1 <= 2): F_{1,2} = Z/p^e, d = 1, n_p = e, ell = bits of p^e
    order = p ** e
    ell = (order - 1).bit_length()  # unique ell-bit encodings of order elements
    d, n_p = 1, e
    import math
    k = math.floor(ell / math.log2(p)) + ceil_log(p, Fraction(8 * ell) / eps)
    say(f"G=C_{p}^{e}: ell={ell}, d={d}, n_p={n_p}, k={k}: n_p^2={n_p**2} {'>' if n_p**2 > k*d else '<='} k d={k*d};"
        f" true support bound min(d,n_p)^2={min(d,n_p)**2} <= k d")
    assert min(d, n_p) ** 2 <= k * d
assert 3 ** 2 > (math.floor(5 / math.log2(3)) + ceil_log(3, 80)) * 1  # C_27, eps = 1/2
say("E: the displayed inequality fails at G = C_27 (p=3, e=3, s=1, eps=1/2); the cost bound with min(d, n_p) holds.")

# ------------------------------------------------------------------ F. chart gates omitted
say("\n== F. Chart-acquisition oracle calls vs the stated gate term, G = C_3, c = 2, s redundant generators ==")
p, c, ell, eps, w = 3, 2, 2, Fraction(1, 2), 1
t = ceil_log(2, Fraction(12 * ell) / eps)              # thm:bb-envelope's t
Qf = c * (1 + ceil_log(p, Fraction(12 * ell) / eps))   # one core call, m = 1, no grades with g_d > 0
stated = Qf * (ell ** 3 + w)                            # the (iii) term without its O_c and polylog
k = math.floor(ell / math.log2(p)) + ceil_log(p, Fraction(8 * ell) / eps)
bM = (p).bit_length()
for s in (2, 10, 100, 1000):
    d = s + s * (s - 1) // 2                           # rank F_{s,2} = s + C(s,2)
    # multiplication-oracle calls of chart acquisition, each counted once as a gate,
    # with the word constants m_+, q_+, m_[], q_[] set to 1 (their smallest conceivable value)
    A_c = 1 + 2 * bM * 1
    chart_calls = (d - s) * (1 + 2 * bM * 1) + 2 * k * d * (2 * bM + A_c)
    say(f"s={s}: d={d}, k={k}, Q_f={Qf}, Q_f(ell^3+w)={stated}, chart oracle calls >= {chart_calls}"
        f" (ratio {chart_calls / stated:.1f}); plus k d = {k*d} single-coordinate QFTs over Z/3")
say("F: the chart term grows like s^2 and is unbounded relative to Q_f (ell^3 + w); (iii) must add it.")
say("\nALL CHECKS PASSED")
