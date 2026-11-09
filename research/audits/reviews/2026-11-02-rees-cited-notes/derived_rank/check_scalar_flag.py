"""Exact check of the scalar-flag source bound of research/DERIVED_RANK_REES_EXTENSION.md, Sec. 2:
P_p = prod_d (gcd(d,p-1)+1)^{r_d} <= P_scalar = prod_d (d+1)^{r_d} <= (r+2)^{r(r+1)/2},
over every strictly decreasing profile r = r_2 > ... > r_c >= 1 with r <= 14, and every
prime p in a test list with p > c. Also checks the node identities against the full-grade artifact."""
import itertools, json
from math import gcd
primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 61, 65537]
fails = n = 0
for r in range(1, 15):
    for c in range(2, r + 2):
        for rest in itertools.combinations(range(r - 1, 0, -1), c - 2):
            prof = (r,) + rest
            Ps = 1
            for d, a in zip(range(2, c + 1), prof):
                Ps *= (d + 1) ** a
            if not Ps <= (r + 2) ** (r * (r + 1) // 2):
                fails += 1; print("FAIL scalar", prof)
            for p in primes:
                if p <= c:
                    continue
                Pp = 1
                for d, a in zip(range(2, c + 1), prof):
                    Pp *= (gcd(d, p - 1) + 1) ** a
                if not Pp <= Ps:
                    fails += 1; print("FAIL Pp", prof, p)
            n += 1
print("profiles:", n)
art = json.load(open("/Users/jaspersands/Developer/qsearch/research/reductions/rees_full_grade_budget.json"))
for cs in art["cases"][1:]:
    L = cs["source_preparations"]; T = cs["sde_calls"]; M = cs["final_fourier_samples"]
    ok = (T <= L - M and cs["central_character_measurements"] == L + T - M
          and cs["complete_instrument_calls"] == L + T + M <= 2 * L)
    fails += not ok
    print(cs["lower_central_dimensions"][:3], "node identities T<=L-M, chars=L+T-M, I=L+T+M<=2L:", ok)
print("TOTAL FAILURES:", fails)
