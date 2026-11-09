"""Exact checks of REES_FULL_GRADE_PARAMETER_BOUND.md, sections 1, 2, 4, 6.

Item 8 of REES_FULL_CAMPAIGN_2.md. Recomputes the note's arithmetic from its
formulas, independently of qsearch code, and compares with
research/reductions/rees_full_grade_budget.json.
"""
import itertools, json, math, sys
from math import gcd, factorial

ROOT = "/Users/jaspersands/Developer/qsearch/"
fails = 0
def check(cond, msg):
    global fails
    if not cond:
        fails += 1
        print("FAIL", msg)

# --- 1. Bezout lift: s = x^u with d*u = g (mod p-1) gives s^d = x^g, s=0 iff x=0
cnt = 0
for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 61, 73, 97, 101]:
    for d in range(2, p):
        g = gcd(d, p - 1)
        u = next(u for u in range(1, p) if (d * u - g) % (p - 1) == 0)
        for x in range(p):
            s = pow(x, u, p) if x else 0
            check(pow(s, d, p) == pow(x, g, p), f"bezout p={p} d={d} x={x}")
            check((s == 0) == (x == 0), "zero")
            cnt += 1
print("bezout lift: checked", cnt, "triples (p,d,x)")

# --- 2. arity bound M_d <= (d-1)(r_d+1)^2 and product bounds over all strictly
# decreasing profiles r = r_2 > r_3 > ... > r_c >= 1, all g_d in [1, d]
def M(a, g):
    return a + 1 if g == 1 else (a + 1) * ((g - 1) * a + 1)

worst = {}
nprof = 0
for r in range(1, 15):
    for c in range(2, r + 2):
        # choose r_3..r_c as a strictly decreasing subset of {1..r-1} of size c-2
        for rest in itertools.combinations(range(r - 1, 0, -1), c - 2):
            prof = (r,) + rest
            nprof += 1
            # worst case over g_d: M is increasing in g, so g_d = d maximises
            P = 1
            for d, a in zip(range(2, c + 1), prof):
                check(M(a, d) <= (d - 1) * (a + 1) ** 2, f"Md {d},{a}")
                check(a <= r - d + 2, "r_d bound")
                P *= M(a, d)
            b1 = factorial(c - 1) * (factorial(r + 1) // factorial(r - c + 2)) ** 2
            b2 = factorial(r) * factorial(r + 1) ** 2
            b3 = (r + 1) ** (3 * r)
            check(P <= b1 <= b2 <= b3, f"P chain r={r} prof={prof} {P} {b1} {b2} {b3}")
            worst[r] = max(worst.get(r, 0), P)
print("profiles checked:", nprof)
for r in sorted(worst):
    print(f"r={r:2d} max P (g_d=d) = {worst[r]}  r!((r+1)!)^2 = {factorial(r)*factorial(r+1)**2}  ratio = {factorial(r)*factorial(r+1)**2/worst[r]:.3g}")

# --- 4/6. Recompute artifact cases
art = json.load(open(ROOT + "research/reductions/rees_full_grade_budget.json"))
for case in art["cases"]:
    dims = case["lower_central_dimensions"]; p = case["supplied_prime"]
    c = case["actual_class"]; n = dims[0]
    r = dims[1] if c >= 2 else 0
    P = 1; S = 1
    for d in range(2, c + 1):
        a = dims[d - 1]; g = gcd(d, p - 1)
        P *= M(a, g)
        S *= (2 if g == 1 else g + 1) ** a   # one central line at a time, arity g+1 (g=1: 2)
    eps_slack = math.ceil(math.log2(3 / (1 / 3)))  # eps = 1/3
    m = n + eps_slack
    D = n + sum(dims[1:])
    rows = {
        "cover_dimension": D,
        "final_fourier_samples": m,
        "leaves_per_terminal": P,
        "scalar_flag_leaves_per_terminal": S,
        # the artifact records the class-dependent middle bound (c-1)! [(r+1)!/(r-c+2)!]^2
        "derived_parameter_leaf_bound": factorial(c - 1) * (factorial(r + 1) // factorial(r - c + 2)) ** 2 if r else 1,
        "source_preparations": m * P,
        "original_inputs": c * m * P,
    }
    for k, v in rows.items():
        ok = case[k] == v
        check(ok, f"artifact {dims} {k}: artifact {case[k]} recomputed {v}")
    # forest counts T <= mP - m, I <= 2mP
    check(case["complete_instrument_calls"] <= 2 * m * P, "I bound")
    print(f"case dims={dims} p={'2^127-1' if p == 2**127-1 else p}: P={P} scalar={S} m={m} D={D}"
          f" I={case['complete_instrument_calls']} <= 2mP={2*m*P}: all fields match = {all(case[k]==v for k,v in rows.items())}")
    if c >= 2:
        print("   g_d =", [gcd(d, p - 1) for d in range(2, c + 1)],
              " guard p >= 16 g^(2g+2) for g>=2:",
              all(p >= 16 * g ** (2 * g + 2) for g in [gcd(d, p - 1) for d in range(2, c + 1)] if g >= 2))

# rank failure bound: Pr[m uniform vectors fail to span F_p^t] <= (p^t-1)/(p-1) p^-m
# exact check small cases by counting
def nonspan_prob(p, t, m):
    # exact probability that m iid uniform vectors in F_p^t span: prod_{i<t}(1-p^{i-m})
    from fractions import Fraction
    pr = Fraction(1)
    for i in range(t):
        pr *= 1 - Fraction(p) ** (i - m)
    return 1 - pr
from fractions import Fraction
for p in [2, 3, 5, 7]:
    for t in range(1, 5):
        for m in range(t, t + 5):
            q = nonspan_prob(p, t, m)
            check(q <= Fraction(1, (p - 1) * p ** (m - t)), f"rank p={p} t={t} m={m}")
print("rank-failure bound 1/((p-1)p^(m-t)) verified exactly for p<=7, t<=4, m<=t+4")

# Q <= g^g poly: sum_{j=1}^{g-1} 2 g^{j+1} <= 4 g^g for g >= 2
for g in range(2, 40):
    check(sum(2 * g ** (j + 1) for j in range(1, g)) <= 4 * g ** g, f"geom g={g}")
print("geometric sum bound checked g<=39")
print("TOTAL FAILURES:", fails)

# --- 3. Randomness caps of section 3, recomputed per grade and summed (classical work is a SUM)
def clog2(x):
    return (x - 1).bit_length()  # ceil(log2 x) for integer x >= 1
for case in art["cases"]:
    dims = case["lower_central_dimensions"]; p = case["supplied_prime"]; c = case["actual_class"]
    if c < 2:
        continue
    n = dims[0]; m = n + 4
    Ms = {d: M(dims[d - 1], gcd(d, p - 1)) for d in range(2, c + 1)}
    calls = {d: m * math.prod(Ms[e] for e in range(2, d)) for d in range(2, c + 1)}
    sde = sum(calls.values())
    nonlin = sum(calls[d] for d in calls if gcd(d, p - 1) >= 2)
    # k = ceil(log2(3 T_rand / eps)), eps = 1/3  ->  ceil(log2(9 T_rand))
    k = clog2(9 * nonlin)
    draws = bits = 0
    for d in calls:
        g = gcd(d, p - 1); a = dims[d - 1]
        if g < 2:
            continue
        h = (g - 1) * a + 1
        R = h * (a + 3) + g * (g + 1) // 2
        U = g + R * (g - 1)
        B = k + 1 + clog2(U)
        J = g * B; K = 3 * B
        Q = J + sum(2 * g ** (j + 1) * B for j in range(1, g)) + R * g * (g - 1) * K
        L = k + 1 + clog2(Q)
        draws += calls[d] * Q
        bits += calls[d] * Q * L * clog2(p)
    res = {"sde_calls": sde, "nonlinear_sde_calls": nonlin, "solver_failure_bits_per_call": k,
           "classical_uniform_draw_cap": draws, "classical_fair_bit_cap": bits}
    for key, v in res.items():
        check(case[key] == v, f"cap {dims} {key}: artifact {case[key]} recomputed {v}")
    print(f"caps dims={dims}: " + ", ".join(f"{key} {'ok' if case[key]==v else 'MISMATCH'}" for key, v in res.items()))
print("TOTAL FAILURES (after caps):", fails)
