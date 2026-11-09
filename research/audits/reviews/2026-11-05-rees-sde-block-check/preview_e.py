"""Computed preview only (no table or headline number is changed): what a 'random-label two-level'
option built on Theorem C (block-steered solver, Corollary C for i.i.d. labels) would do to the
combined column of tab:fcs-budget (class-nine profile g = (19,17,16,14,12,9,6,3,1), eps = 1/3,
S = 20), reading the per-grade data from research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json.

At grade d with 2 <= kappa_d < p-1 a Theorem C node uses E = max(3, kappa_d) (variant A) or the
E in [max(3,kappa_d), 8] with kappa_d^E <= 2^20 minimising M_E(g_d) (variant B), and is admitted only if
  (G1) p is not in E_cg(E, kappa): E_cg(3,2) = {} ; E_cg(3,3) = 22 primes <= 241 ; otherwise p >= p_W(E, kappa);
  (G2) per-pass failure L*C(E,2)/G_lb(p) <= 1/2, G_lb = Weil lower bound of Lemma W;
  (G3) node abort from the bank, (M_E(g_d) + L*C(E,2))/(p-1) + 1/((p-1)p^(M-g_d)), at most
       tau_d = eps/(9(c-1) S n_d) with n_d = prod_{d'<d} M_d' (the error split of thm:free-coordinate(iii)).
It replaces the combined-rule arity only when M_E(g_d) is smaller.  Also printed: the triangular
preview of rem:triangular-scope (S2 arity -> (g+1)(g+2)/2) for comparison.
"""
import json
import math
from math import comb, gcd

ROOT = "/Users/jaspersands/Developer/qsearch"
d = json.load(open(ROOT + "/research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json"))
c = d["class"]
g = dict(zip(range(2, c + 1), d["profile"][1:]))
EPS = 1 / 3
ECG33 = {7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127, 139, 151, 157, 163, 181, 193, 211, 241}


def arity(a, E):
    M, q = 1, a
    while q > 0:
        M += q + 1
        q -= min(E - 1, q)
    return M


def p_weil(k, E):
    # least p with p - e > (k^e - 1)(e - 1) sqrt(p) for all 2 <= e <= E (bisection on the monotone tail)
    def ok(p):
        return all(p - e > (k ** e - 1) * (e - 1) * math.sqrt(p) for e in range(2, E + 1))
    lo, hi = 2, 2
    while not ok(hi):
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def g_lb(k, E, p):
    return min((p - e - (k ** e - 1) * (e - 1) * math.sqrt(p)) / k ** e for e in range(2, E + 1))


def not_exc(k, E, p):
    if (k, E) == (2, 3):
        return True
    if (k, E) == (3, 3):
        return p not in ECG33
    return p >= p_weil(k, E)


def evaluate(p, base, variant):
    """base: dict d -> (kind, M) of the combined rule.  Returns (log2 Q, per-grade choices, bank sum)."""
    S = 20
    Ms, kinds, bank = {}, {}, 0.0
    n = 1
    for dd in range(2, c + 1):
        kind, M = base[dd]
        k = gcd(dd, p - 1)
        best = (M, kind, 0.0)
        if 2 <= k < p - 1:
            Es = [max(3, k)] if variant == "A" else [E for E in range(max(3, k), 9) if k ** E <= 2 ** 20]
            for E in Es:
                ME = arity(g[dd], E)
                L = math.ceil(g[dd] / (E - 1))
                pairs = L * comb(E, 2)
                if not not_exc(k, E, p):
                    continue
                gl = g_lb(k, E, p)
                if gl <= 0 or pairs / gl > 0.5:
                    continue
                f = (ME + pairs) / (p - 1) + 1 / ((p - 1) * p ** (ME - g[dd]))
                tau = EPS / (9 * (c - 1) * S * n)
                if f > tau:
                    continue
                if ME < best[0]:
                    best = (ME, f"TC(E={E})", S * n * f)
        Ms[dd], kinds[dd] = best[0], best[1]
        bank += best[2]
        n *= best[0]
    Q = c * S
    for dd in Ms:
        Q *= Ms[dd]
    return math.log2(Q), kinds, Ms, bank


if __name__ == "__main__":
    print("p_W(E,kappa):", {(k, E): p_weil(k, E) for (k, E) in [(2, 3), (3, 3), (2, 4), (4, 4), (5, 5), (6, 6), (7, 7), (9, 9)]})
    for row in d["rows"]:
        lab = row["label"]
        p = int(eval(lab.replace("^", "**"))) if "^" in lab else int(lab)
        base = {int(k): (v[0], int(v[1])) for k, v in row["combined"]["arities"].items()}
        Q0 = c * 20
        Qt = c * 20
        for dd, (kind, M) in base.items():
            Q0 *= M
            Qt *= (g[dd] + 1) * (g[dd] + 2) // 2 if kind == "S2" else M
        assert abs(math.log2(Q0) - float(row["table"]["combined_Q"])) < 0.06, (lab, math.log2(Q0))
        print(f"p={lab}: kappa_d={[gcd(dd, p - 1) for dd in range(2, c + 1)]} table combined log2Q={row['table']['combined_Q']}"
              f" (recomputed {math.log2(Q0):.1f}); triangular preview {math.log2(Qt):.1f}")
        for var in ("A", "B"):
            lq, kinds, Ms, bank = evaluate(p, base, var)
            print(f"    variant {var}: log2Q={lq:.1f}  kinds={[kinds[dd] for dd in sorted(kinds)]}"
                  f"  M={[Ms[dd] if Ms[dd] < 10 ** 6 else f'{Ms[dd]:.2e}' for dd in sorted(Ms)]}  bank-abort sum={bank:.2e}")
