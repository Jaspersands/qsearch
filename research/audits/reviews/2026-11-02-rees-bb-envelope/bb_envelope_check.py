"""Exponent arithmetic for the black-box free-pullback envelope (Rees round 2, item 7).

Exact integers throughout (logs are only printed). Run from the repo root:
  /opt/anaconda3/bin/python -B research/audits/reviews/2026-11-02-rees-bb-envelope/bb_envelope_check.py

Checks, in order:
  A. Reproduce the recorded class-9 numbers (core 145 / 2^1573; old envelope b(b+1)=10920,
     exponent 147, 2^2194) from the formulas, and against the repo functions if importable.
  B. Worst-case m-exponents E_1(c) (Schedule 1) and E_W(c) (combined rule W) for c = 2..9,
     by scanning every prime c < p < PRIME_LIMIT, and confirming them as leading exponents.
  C. New envelope: per-Sylow f-query bound for the chart route, e = 1 (exponent E) and
     e > 1 (whole-socle recursion, <= n calls, exponent E + 1); old vs new at b = 104.
  D. Class-9 profile run as a black box (p = 43, s = 2, n = 19): direct free pullback on
     F_{2,9} (d = 127) against the chart route.
  E. Imran-Ivanyos bounded-prime exponents read from their proofs, against E_W(c) + 1.
"""
from fractions import Fraction
from math import gcd, log2
import sys

sys.path.insert(0, ".")
PRIME_LIMIT = 200_000


def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n + 1) if sieve[i]]


PRIMES = primes_upto(PRIME_LIMIT)


def bitlen(x):
    return x.bit_length()  # ceil(log2(x+1))


def ceil_log(base, x):
    """Least k with base**k >= x, for a Fraction or int x > 0."""
    x = Fraction(x)
    k, v = 0, 1
    while v < x:
        v *= base
        k += 1
    return k


def B(d, a):
    """Ivanyos-Santha sufficient arity B_d(a); B_1(a) = a + 1."""
    if d == 1:
        return a + 1
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** bitlen(d)


def arity(rule, p, d, g):
    """Arity at grade d with g = dim gamma_d; a grade with g = 0 is skipped (arity 1)."""
    if g == 0:
        return 1
    if rule == "S1":
        return B(d, g)
    k = gcd(d, p - 1)
    if k == 1:
        return g + 1
    if p >= 16 * k ** (2 * k + 2):
        return (g + 1) * ((k - 1) * g + 1)
    return B(k, g)


def grade_exponent(rule, p, d):
    if rule == "S1":
        return d * bitlen(d)
    k = gcd(d, p - 1)
    if k == 1:
        return 1
    if p >= 16 * k ** (2 * k + 2):
        return 2
    return k * bitlen(k)


def core_queries(rule, p, grades, t):
    """Q = c (m + t) prod_d M_d: one Thm-main call, grades = (g_1, ..., g_c), t extra samples."""
    c, m = len(grades), grades[0]
    P = 1
    for d in range(2, c + 1):
        P *= arity(rule, p, d, grades[d - 1])
    return c * (m + t) * P


def flat(m, c):
    return (m,) * c


def lg(x):
    return log2(x) if x > 0 else float("-inf")


out = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    out.append(s)


# ---------------------------------------------------------------- A. reproduce
say("== A. Reproduce recorded class-9 numbers ==")
P43, M19, C9 = 43, 19, 9
PROFILE = (19, 17, 16, 14, 12, 9, 6, 3, 1)
eps = Fraction(1, 3)
S_art = M19 + ceil_log(P43, 3 / eps)        # recovery_budget convention: m + ceil(log_p(3/eps)) = 20
Q_core_S1 = core_queries("S1", P43, PROFILE, S_art - M19)
say("profile S =", S_art, " ceil log2 Q_core(S1) =", bitlen(Q_core_S1 - 1), "(recorded 1573)")
assert S_art == 20 and bitlen(Q_core_S1 - 1) == 1573
E1_9 = 1 + sum(d * bitlen(d) for d in range(2, 10))
assert E1_9 == 145
b = bitlen(P43 ** M19 - 1)
cap = b * (b + 1)
slack_old = ceil_log(2, 12 * cap / eps)
Q_old = cap * C9 * (b + slack_old)
for d in range(2, C9 + 1):
    Q_old *= B(d, b)
say("b =", b, " cap b(b+1) =", cap, " slack =", slack_old, " ceil log2 Q_old =", bitlen(Q_old - 1),
    " exponent 3+sum =", 3 + sum(d * bitlen(d) for d in range(2, 10)), "(recorded 104, 10920, 19, 2194, 147)")
assert (b, cap, slack_old, bitlen(Q_old - 1)) == (104, 10920, 19, 2194)
try:
    from theorems.rees_hsp_reduction import black_box_large_prime_budget
    from theorems.full_jet_resource_certificate import sde_arity
    repo = black_box_large_prime_budget(104, 9)
    assert repo["large_prime_original_query_bound"] == Q_old
    assert all(sde_arity(d, a) == B(d, a) for d in range(1, 10) for a in (0, 1, 7, 104))
    say("repo functions agree: black_box_large_prime_budget(104, 9) and sde_arity")
except ImportError as exc:  # pragma: no cover
    say("repo import skipped:", exc)

# ---------------------------------------------------------------- B. exponents
say("\n== B. Worst-case m-exponents over all primes c < p <", PRIME_LIMIT, "==")
E1, EW, argW = {}, {}, {}
for c in range(2, 10):
    E1[c] = 1 + sum(d * bitlen(d) for d in range(2, c + 1))
    best, arg = -1, None
    for p in PRIMES:
        if p <= c:
            continue
        e = 1 + sum(grade_exponent("W", p, d) for d in range(2, c + 1))
        if e > best:
            best, arg = e, p
    EW[c], argW[c] = best, arg
    say(f"c={c}: E_1={E1[c]}  E_W={EW[c]} (first attained at p={arg})")
assert [E1[c] for c in range(2, 10)] == [5, 11, 23, 38, 56, 77, 109, 145]
assert [EW[c] for c in range(2, 10)] == [5, 11, 23, 38, 56, 77, 107, 143]
# Above 16*3^8 = 104976 both kappa=2 and kappa=3 grades are past their thresholds, and grades with
# kappa >= 4 are below 16 kappa^(2kappa+2) <= 16*9^20 only through B_kappa; the scan covers p < 2e5.
# Leading-exponent check: log(Q(2m)/Q(m)) / log 2 -> E at large m (flat profile g_d = m).
say("leading exponent of one core call, flat profile, m = 2^20 -> 2^21:")
for c in (3, 5, 9):
    for rule, p in (("S1", argW[c]), ("W", argW[c])):
        m = 2 ** 20
        q1 = core_queries(rule, p, flat(m, c), 0)
        q2 = core_queries(rule, p, flat(2 * m, c), 0)
        slope = lg(q2) - lg(q1)
        target = E1[c] if rule == "S1" else EW[c]
        say(f"  c={c} rule={rule} p={p}: slope={slope:.4f} (E={target})")
        assert abs(slope - target) < 0.01

# ---------------------------------------------------------------- C. new envelope
say("\n== C. Sylow envelope for the chart route ==")


def sylow_queries(rule, p, n, c, e_gt_1, t):
    """f-queries for one Sylow subgroup of composition length n, flat worst-case grades.

    e = 1: one Thm-main call on the chart (dimension n).
    e > 1: whole-socle recursion with stop rules; call j acts on a section of
    log-order <= n - j, so its socle has dimension <= n - j; at most n calls.
    """
    if not e_gt_1:
        return core_queries(rule, p, flat(n, c), t)
    return sum(core_queries(rule, p, flat(n - j, c), t) for j in range(n))


def sylow_simple(rule, p, n, c, t):
    return n * core_queries(rule, p, flat(n, c), t)


for c in (3, 5, 9):
    p = argW[c]
    for rule in ("S1", "W"):
        n = 2 ** 14
        a2 =sylow_simple(rule, p, 2 * n, c, 0)
        a1 = sylow_simple(rule, p, n, c, 0)
        slope = lg(a2) - lg(a1)
        target = (E1[c] if rule == "S1" else EW[c]) + 1
        say(f"  e>1 c={c} rule={rule} p={p}: slope of n*Q_core(n) = {slope:.4f} (E+1={target})")
        assert abs(slope - target) < 0.01

# exact sum vs n*Q_core(n): ratio tends to 1/(E+1)
for c, p in ((3, argW[3]), (5, argW[5])):
    for n in (50, 400):
        s_ex = sylow_queries("W", p, n, c, True, 0)
        s_si = sylow_simple("W", p, n, c, 0)
        say(f"  c={c} p={p} n={n}: exact sum / (n Q_core(n)) = {s_ex / s_si:.4f}  vs 1/(E_W+1) = {1 / (EW[c] + 1):.4f}")

# Old envelope convention (composition length bound b = 104, base-2 slack) against the new count.
say("old vs new at b = 104 (composition length bound n <= b, same slack convention):")
calls_new = b
slack_new = ceil_log(2, 12 * calls_new / eps)
for rule, p in (("S1", P43), ("W", P43), ("W", argW[9])):
    q_simple = sylow_simple(rule, p, b, 9, slack_new)
    q_exact = sylow_queries(rule, p, b, 9, True, slack_new)
    say(f"  rule={rule} p={p}: calls <= {calls_new}, slack={slack_new}, log2 n*Q(n) = {lg(q_simple):.1f},"
        f" log2 exact sum = {lg(q_exact):.1f}  (old 2194, exponent 147 -> new {(E1[9] if rule == 'S1' else EW[9]) + 1}"
        f"{' worst p' if p == argW[9] else ''})")
# With the true composition length n_p <= floor(l / log2 p) at p = 43, l = 104:
n43 = 104 * 1000 // int(1000 * log2(43))
assert n43 == 19 and 43 ** 19 < 2 ** 104 < 43 ** 20
for rule in ("S1", "W"):
    t = ceil_log(P43, 12 * 104 / eps)   # t = ceil(log_p(12 l / eps)), core share eps/4 over <= l calls
    q1 = core_queries(rule, P43, PROFILE, t)
    q2 = sylow_queries(rule, P43, 19, 9, True, t)
    say(f"  p=43, l=104 -> n_p<=19, t={t}: rule={rule}: e=1 profile call log2 Q = {lg(q1):.1f};"
        f" e>1 flat worst case log2 Q = {lg(q2):.1f}")

# ---------------------------------------------------------------- D. free pullback vs chart
say("\n== D. Class-9 profile as a black box: p = 43, s = 2, e = 1 ==")


def mobius(n):
    res, k, x = 1, 2, n
    while k * k <= x:
        if x % k == 0:
            x //= k
            if x % k == 0:
                return 0
            res = -res
        k += 1
    return -res if x > 1 else res


def witt(s, k):
    return sum(mobius(j) * s ** (k // j) for j in range(1, k + 1) if k % j == 0) // k


W2 = [witt(2, k) for k in range(1, 10)]
d127 = sum(W2)
gF = tuple(sum(W2[k - 1:]) for k in range(1, 10))
say("Witt ranks W(2,k) =", W2, " d = rank F_{2,9} =", d127, " lower-central dims of F:", gF)
assert d127 == 127 and gF[0] == 127 and gF[-1] == 56
for rule in ("S1", "W"):
    qF = core_queries(rule, P43, gF, 1)
    qC = core_queries(rule, P43, PROFILE, 1)
    say(f"  rule={rule}: direct pullback on F_(2,9)(F_43): log2 Q = {lg(qF):.1f};"
        f" chart route (dim 19): log2 Q = {lg(qC):.1f}; ratio 2^{lg(qF) - lg(qC):.1f}")
# s-exponent of the direct route: g_k(F_{s,c}) = Theta(s^c) at every grade, so exponent c*E.
for rule, E in (("S1", E1[9]), ("W", EW[9])):
    p = argW[9]
    s1, s2 = 2 ** 6, 2 ** 7
    g1 = tuple(sum(witt(s1, k) for k in range(j, 10)) for j in range(1, 10))
    g2 = tuple(sum(witt(s2, k) for k in range(j, 10)) for j in range(1, 10))
    slope = lg(core_queries(rule, p, g2, 0)) - lg(core_queries(rule, p, g1, 0))
    say(f"  direct route s-exponent, rule={rule}, p={p}: slope s=2^6->2^7 = {slope:.2f} (c*E = {9 * E})")
    assert abs(slope - 9 * E) < 0.2 * 9
# Chart acquisition: Phi evaluations, zero f queries.
# (ker pi)^perp is dual to the additive group of L(G_p), whose rank is the number of cyclic factors
# (n_p = 19 at e = 1), not s: Lie generation by s elements does not bound module rank.
for p in (P43,):
    k_rows = 104 * 1000 // int(1000 * log2(p))        # n_p is unknown before the chart: use floor(l / log2 p)
    t1 = ceil_log(p, 8 * 104 / eps)                   # chart share eps/4, half rank and half approximation, <= l primes
    say(f"  chart acquisition at p={p}: abelian HSP samples floor(l/log2 p) + t' = {k_rows} + {t1};"
        f" Phi evaluations on F_(2,9) (d = {d127}) per sample: 1 coherent; zero f queries")

# ---------------------------------------------------------------- E. Imran-Ivanyos
say("\n== E. Imran-Ivanyos (arXiv:2304.08376v1) bounded-prime exponents, read from the proofs ==")


def sigma(p, ceil_reading=False):
    """n-exponent of S(p,n) = S_pm(p,n)^ceil(log2 p) (Props 4-5); p = 2 is linear (n+1)."""
    if p == 2:
        return 1
    d0 = (p - 1) // 2
    j = (d0 - 1).bit_length() if ceil_reading else d0.bit_length() - 1   # ceil / floor of log2 d0
    return 2 ** j * (p - 1).bit_length()                                 # (p-1).bit_length() = ceil(log2 p) for odd p


for p in (2, 3, 5, 7, 11, 13):
    assert (p - 1).bit_length() == (p.bit_length() if p & (p - 1) else p.bit_length() - 1) or p == 2
say("sigma_p (floor reading, as the induction gives) / (ceil reading, as printed):",
    {p: (sigma(p), sigma(p, True)) for p in (2, 3, 5, 7)})
for c in range(2, 10):
    small = [p for p in (2, 3, 5, 7) if p <= c]
    ii = {p: 2 + (c - 1) * sigma(p) for p in small}
    iic = {p: 2 + (c - 1) * sigma(p, True) for p in small}
    say(f"c={c}: II f-query n-exponent 2+(c-1)sigma_p (+alpha_22): {ii} (ceil reading {iic});"
        f" large primes: E_W+1 = {EW[c] + 1}, E_1+1 = {E1[c] + 1}")
# Hypothetical: II's zero-sum layer at the first prime above c, against Rees grade exponents.
for c in (3, 5, 9):
    q = next(p for p in PRIMES if p > c)
    say(f"  c={c}: II layer exponent at p={q} would be (c-1)*sigma = {(c - 1) * sigma(q)}"
        f" vs Rees sum_d e_d <= {E1[c] - 1} (E_W-1 = {EW[c] - 1})")

# ---------------------------------------------------------------- F. explicit constant
say("\n== F. Constant K_c with prod_d M_d(p, g) <= K_c (g+1)^(sum_d e_d(p)) ==")


def K(c):
    out_k = 1
    for d in range(2, c + 1):
        out_k *= d ** (d * (d - 1) // 2 * bitlen(d))
    return out_k


for c in range(2, 10):
    say(f"c={c}: log2 K_c = {lg(K(c)):.1f}")
for c in (3, 5, 9):
    for p in [q for q in PRIMES if c < q < 6000] + [194522647344910884721, 2 ** 61 - 1]:
        for g in (0, 1, 19, 104):
            lhs = 1
            for d in range(2, c + 1):
                lhs *= arity("W", p, d, g)
            ex = sum(grade_exponent("W", p, d) for d in range(2, c + 1)) if g else 0
            assert lhs <= K(c) * (g + 1) ** ex, (c, p, g)
say("inequality holds for c in {3,5,9}, all primes c < p < 6000 and two large primes, g in {0,1,19,104}")
say("Q_large <= c K_c (L+t)(L+1)^(E_W) with L = sum_{p>c} n_p <= l / log2(c+1); for c = 9:",
    f"log2(c K_c) = {lg(9 * K(9)):.1f}")

say("\nALL ASSERTIONS PASSED")
