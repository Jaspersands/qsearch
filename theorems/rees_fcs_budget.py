"""Exact recomputation of Table tab:fcs-budget of docs/papers/rees-hsp/main.tex.

Every entry is recomputed from the formulas the paper states, in exact integer and rational
arithmetic; log2 values are taken only at the end, for printing. Nothing is imported from the
older report scripts (research/audits/reviews/2026-11-02-rees-schedule3-cost/fcs_budget.py and
../2026-11-02-rees-schedules/combined/combined_budget.py), so this is an independent check.

Columns (class-nine profile g = (19,17,16,14,12,9,6,3,1), eps = 1/3):

  combined Q        Remark rem:combined-schedule, with the query count after Theorem thm:main:
                    Q = c * S * prod_d M_d, S = m + ceil(log_p(3/eps)).
  (iii) Q / trials  Theorem thm:free-coordinate(iii) with the least public arity M_d at every
  / total           grade 2 <= kappa_d < p-1 (rule (R1) of Appendix app:fc-mixed), the combined
                    rule elsewhere, B = ceil(log2(27 N / eps)), and the per-node trial cap
                    ceil(2 B ln2 q_d^{-g_d}) (its value at the worst case r = a_d = g_d).
  uniform-kernel    Theorem thm:free-coordinate(iv) (formerly thm:random-column(i)) nodes (M = 4u_d, 4 kappa^M B trials) mixed into
  Q / trials        the combined rule, with tree restarts as in thm:free-coordinate(iv) with the trees of (ii) (formerly thm:random-column(ii)). The paper
                    states the node formulas but NOT the mixed rule (Remark rem:combined-schedule
                    says the rule does not mix in Schedule 3). The mixed rule used for the printed
                    numbers is the one of combined_budget.py (W+3); it is written out explicitly in
                    `uniform_kernel_mixed` below and flagged as script-defined in the JSON.

Run:  /opt/anaconda3/bin/python -m theorems.rees_fcs_budget [--out PATH]
Writes research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json by default.
This is a finite exact computation. It tests no asymptotic claim and no theorem.
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction as F
from math import gcd
from pathlib import Path

import mpmath

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "research" / "audits" / "reviews" / "2026-11-04-rees-fcs-budget" / "fcs_budget.json"

PROFILE = (19, 17, 16, 14, 12, 9, 6, 3, 1)
EPS = F(1, 3)
PRIMES = (
    ("11", 11),
    ("1031", 1031),
    ("5281", 5281),
    ("2^31-1", 2 ** 31 - 1),
    ("2^61-1", 2 ** 61 - 1),
    ("2^127-1", 2 ** 127 - 1),
)
# Prime tags for the proposed numbers.tex macros (letters only, as make_numbers.py requires).
MACRO_TAGS = {
    "11": "Eleven",
    "1031": "TenThirtyOne",
    "5281": "FiftyTwoEightyOne",
    "2^31-1": "MersThirtyOne",
    "2^61-1": "MersSixtyOne",
    "2^127-1": "MersOneTwentySeven",
}
COLUMNS = ("combined_Q", "uniform_kernel_Q", "uniform_kernel_trials", "iii_Q", "iii_trials", "iii_total")
COLUMN_TAGS = {
    "combined_Q": "CombQ",
    "uniform_kernel_Q": "UkQ",
    "uniform_kernel_trials": "UkTrials",
    "iii_Q": "FcQ",
    "iii_trials": "FcTrials",
    "iii_total": "FcTotal",
}

mpmath.mp.dps = 120
_LN2 = mpmath.log(2)
# Rational bounds lo < ln 2 < hi, tight to about 1e-110.
LN2_LO = F(int(mpmath.floor(_LN2 * mpmath.mpf(10) ** 110)), 10 ** 110)
LN2_HI = LN2_LO + F(1, 10 ** 110)


# ----------------------------------------------------------------------------- exact helpers

def is_probable_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 3.3e24, strong probable-prime test beyond (the six
    table primes are classical primes; this only guards against typos)."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for q in small:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def ceil_log2(x) -> int:
    """Least k >= 0 with 2^k >= x, for a positive rational x."""
    x = F(x)
    k = 0
    while F(2) ** k < x:
        k += 1
    return k


def ceil_log_base(base: int, x) -> int:
    """Least t >= 0 with base^t >= x."""
    x = F(x)
    t = 0
    while F(base) ** t < x:
        t += 1
    return t


def ceil_frac(x: F) -> int:
    return -((-x.numerator) // x.denominator)


def log2_exact(x) -> float:
    """log2 of a positive rational, accurate to float precision for huge numerators."""
    x = F(x)
    return math.log2(x.numerator) - math.log2(x.denominator)


def fmt1(x) -> str:
    """The table's precision: log2 to one decimal, rounded to nearest (as '%.1f')."""
    return f"{log2_exact(x):.1f}"


def boundary_margin(x) -> float:
    """Distance of log2(x) from the nearest one-decimal rounding boundary (k + 0.05)/10 grid."""
    v = log2_exact(x) * 10
    return abs(v - math.floor(v) - 0.5) / 10


def ceil_log2_plus1(d: int) -> int:
    """ceil(log2(d+1)), computed by integer comparison."""
    k = 0
    while 2 ** k < d + 1:
        k += 1
    return k


def B_IS(d: int, a: int) -> int:
    """Ivanyos-Santha arity B_d(a) = [d^{d(d-1)/2} (a+1)^d]^{ceil(log2(d+1))} (after thm:main)."""
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** ceil_log2_plus1(d)


def ln2_ceil(x: F) -> int:
    """ceil(x * ln 2) for a positive rational x; exact because x ln 2 is irrational."""
    lo, hi = ceil_frac(x * LN2_LO), ceil_frac(x * LN2_HI)
    assert lo == hi, "ln 2 bounds too loose"
    return lo


# ----------------------------------------------------------------------------- the schedules

def grade_data(p: int, d: int):
    k = gcd(d, p - 1)
    h = (p - 1) // k
    q = F(h + 1, p)
    return k, h, q


def combined_choice(p: int, d: int, gd: int):
    """Remark rem:combined-schedule: linear if kappa_d = 1; Schedule 2 if kappa_d >= 2 and
    p >= 16 kappa_d^(2 kappa_d + 2); else Schedule 1 at degree kappa_d."""
    k, _, _ = grade_data(p, d)
    if k == 1:
        return "lin", gd + 1
    if p >= 16 * k ** (2 * k + 2):
        return "S2", (gd + 1) * ((k - 1) * gd + 1)
    return "S1", B_IS(k, gd)


def beta(p: int, k: int, M: int, n0: int, a: int) -> F:
    """Bank bound of thm:free-coordinate(i) / eq. (fc-beta):
    4 / (h^(n0-1) q^a) + (p^a - 1) / ((p-1) p^L), L = M - n0."""
    h = (p - 1) // k
    q = F(h + 1, p)
    L = M - n0
    return 4 / (F(h) ** (n0 - 1) * q ** a) + F(p ** a - 1, (p - 1) * p ** L)


def least_fcs_arity(p: int, k: int, gd: int, tau: F):
    """Least integer M with some 1 <= n0 <= M and beta(M, n0; g_d) <= tau (rule (R1))."""
    M = 1
    while True:
        best = None
        for n0 in range(1, M + 1):
            b = beta(p, k, M, n0, gd)
            if b <= tau and (best is None or b < best[1]):
                best = (n0, b)
        if best is not None:
            return M, best[0], best[1]
        M += 1


def explicit_fcs_arity(p: int, k: int, gd: int, tau: F):
    """The explicit choice of thm:free-coordinate(iii) / Lemma lem:fc-choice, in integer form:
    n0 - 1 = least j >= 0 with h^j >= 8 q^{-g_d} / tau; M = n0 + g_d + least i >= 0 with p^i >= 2/tau."""
    h = (p - 1) // k
    q = F(h + 1, p)
    j = 0
    target = 8 / (q ** gd * tau)
    while F(h) ** j < target:
        j += 1
    n0 = 1 + j
    M = n0 + gd + ceil_log_base(p, 2 / tau)
    return M, n0, beta(p, k, M, n0, gd)


def free_coordinate_iii(p: int, profile=PROFILE, eps: F = EPS, explicit: bool = False):
    """Theorem thm:free-coordinate(iii) with rule (R1)-(R4) of Appendix app:fc-mixed."""
    c, m = len(profile), profile[0]
    g = {d: profile[d - 1] for d in range(1, c + 1)}
    t = ceil_log_base(p, 3 / eps)
    S = m + t
    grades, n, acc = {}, {}, 1
    for d in range(2, c + 1):
        n[d] = acc
        k, h, q = grade_data(p, d)
        comb = combined_choice(p, d, g[d])
        if 2 <= k < p - 1:
            tau = eps / (9 * (c - 1) * S * n[d])
            M, n0, b = (explicit_fcs_arity if explicit else least_fcs_arity)(p, k, g[d], tau)
            assert b <= tau
            grades[d] = dict(cls="F", schedule="FCS", kappa=k, M=M, n0=n0, bank=b, tau=tau,
                             combined=comb)
        elif k == 1:
            grades[d] = dict(cls="1", schedule="lin", kappa=k, M=g[d] + 1, combined=comb)
        else:  # kappa_d = p - 1 >= 2: Schedule 1 at degree d
            assert k == p - 1 == d
            grades[d] = dict(cls="0", schedule="S1", kappa=k, M=B_IS(d, g[d]), combined=comb)
        acc *= grades[d]["M"]
    P = acc
    N = S * sum(n[d] for d in grades if grades[d]["cls"] == "F")
    B = ceil_log2(27 * F(N) / eps) if N else 0
    caps = {}
    for d, gr in grades.items():
        if gr["cls"] == "F":
            q = grade_data(p, d)[2]
            caps[d] = ln2_ceil(2 * B / q ** g[d])  # ceil(2 B ln2 q^{-g_d})
    total = S * sum(n[d] * caps[d] for d in caps)
    Q = c * S * P
    # Error budget of the proof of (iii): rank eps/3, bank eps/9, capped steps eps/9, approx eps/3.
    rank = F(p ** m - 1, (p - 1) * p ** S)
    bank = S * sum(n[d] * grades[d]["bank"] for d in caps)
    capped = 3 * N * F(1, 2 ** B) if N else F(0)
    budget_ok = rank <= eps / 3 and bank <= eps / 9 and capped <= eps / 9 and \
        rank + bank + capped + eps / 3 <= eps
    return dict(c=c, m=m, t=t, S=S, n=n, grades=grades, P=P, Q=Q, N=N, B=B, caps=caps,
                max_cap=max(caps.values()) if caps else 0,
                argmax_cap=max(caps, key=caps.get) if caps else None,
                total=total, rank=rank, bank=bank, capped=capped, budget_ok=budget_ok)


def combined_rule(p: int, profile=PROFILE, eps: F = EPS):
    c, m = len(profile), profile[0]
    S = m + ceil_log_base(p, 3 / eps)
    sch = {d: combined_choice(p, d, profile[d - 1]) for d in range(2, c + 1)}
    P = 1
    for d in sch:
        P *= sch[d][1]
    return dict(S=S, sch=sch, P=P, Q=c * S * P)


def rc_bank(p: int, k: int, gd: int, M: int, literal_main: bool) -> F:
    """thm:free-coordinate(iv) (formerly thm:random-column(i)) bank event at a = g_d: 4/mu + Pr[rank < a], mu = ((h+1)^M - 1)/(h p^a).
    literal_main=False uses Lemma lem:s3-moment(d)'s (p^a - 1) p^{-M}/(p-1); True uses main.tex's 2p^{a-M}."""
    h = (p - 1) // k
    four_over_mu = F(4 * h * p ** gd, (h + 1) ** M - 1)
    second = F(2 * p ** gd, p ** M) if literal_main else F(p ** gd - 1, (p - 1) * p ** M)
    return four_over_mu + second


def uniform_kernel_mixed(p: int, profile=PROFILE, eps: F = EPS, literal_main: bool = False):
    """Script-defined mixed rule (combined_budget.py, W+3); the paper does not state it.

    Per grade: the combined-rule choice, replaced by a uniform-kernel Schedule-3 node of arity
    4 u_d, u_d = max(2, kappa_d, g_d + 1), when p >= 16 u_d^2 and 4 u_d is strictly smaller.
    Then, while the node-weighted bank sum per tree sum_d n_d beta_d exceeds 1/64, add one column
    at the grade with the largest weighted term (public data only). Cap B = ceil(log2(64 max(1,
    3 n_S3 + n_S2))) per tree; trials per node 4 kappa^M B (thm:free-coordinate(iv) (formerly thm:random-column(i))); 4m' trees with
    m' = m + ceil(log2(3/eps)) (thm:free-coordinate(iv) with the trees of (ii) (formerly thm:random-column(ii))); Q = c * 4m' * P."""
    c, m = len(profile), profile[0]
    g = {d: profile[d - 1] for d in range(1, c + 1)}
    sch = {}
    for d in range(2, c + 1):
        k = gcd(d, p - 1)
        name, M = combined_choice(p, d, g[d])
        u = max(2, k, g[d] + 1)
        if p >= 16 * u * u and 4 * u < M:
            name, M = "S3", 4 * u
        sch[d] = [name, M]
    if not any(s == "S3" for s, _ in sch.values()):
        return None
    bumps = 0
    while True:
        n, acc = {}, 1
        for d in range(2, c + 1):
            n[d] = acc
            acc *= sch[d][1]
        P = acc
        weighted = {d: n[d] * rc_bank(p, gcd(d, p - 1), g[d], sch[d][1], literal_main)
                    for d in sch if sch[d][0] == "S3"}
        if sum(weighted.values(), F(0)) <= F(1, 64):
            break
        worst = max(weighted, key=weighted.get)
        sch[worst][1] += 1
        bumps += 1
    n_s3 = sum(n[d] for d in sch if sch[d][0] == "S3")
    n_s2 = sum(n[d] for d in sch if sch[d][0] == "S2")
    B = ceil_log2(64 * max(1, 3 * n_s3 + n_s2))
    trials = {d: 4 * gcd(d, p - 1) ** sch[d][1] * B for d in sch if sch[d][0] == "S3"}
    mprime = m + ceil_log2(3 / eps)
    trees = 4 * mprime
    tree_abort = (3 * n_s3 + n_s2) * F(1, 2 ** B) + sum(weighted.values(), F(0))
    return dict(sch={d: tuple(v) for d, v in sch.items()}, n=n, P=P, B=B, trials=trials,
                max_trials=max(trials.values()), trees=trees, Q=c * trees * P, bumps=bumps,
                tree_abort=tree_abort, tree_abort_ok=tree_abort <= F(1, 16))


# ----------------------------------------------------------------------------- assembly

def _s(x) -> str:
    """Exact value as a string: integers as decimal, rationals as 'a/b'."""
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def _bound(x) -> dict:
    """A small positive rational bound, stored by its log2 rounded up (and exactly if short)."""
    x = F(x)
    out = {"log2_up": math.ceil(log2_exact(x) * 1000) / 1000 if x > 0 else None}
    if x.denominator < 10 ** 80 and x.numerator < 10 ** 80:
        out["exact"] = _s(x)
    return out


def row(label: str, p: int) -> dict:
    assert is_probable_prime(p) and p > len(PROFILE)
    comb = combined_rule(p)
    fc = free_coordinate_iii(p)
    fcx = free_coordinate_iii(p, explicit=True)
    uk = uniform_kernel_mixed(p)
    uk_lit = uniform_kernel_mixed(p, literal_main=True)
    exact = {
        "combined_Q": comb["Q"],
        "uniform_kernel_Q": uk["Q"] if uk else None,
        "uniform_kernel_trials": uk["max_trials"] if uk else None,
        "iii_Q": fc["Q"],
        "iii_trials": fc["max_cap"],
        "iii_total": fc["total"],
    }
    table = {k: (fmt1(v) if v is not None else None) for k, v in exact.items()}
    margins = {k: (round(boundary_margin(v), 4) if v is not None else None) for k, v in exact.items()}
    grades = {}
    for d, gr in fc["grades"].items():
        e = dict(cls=gr["cls"], schedule=gr["schedule"], kappa=gr["kappa"], M=_s(gr["M"]),
                 combined_schedule=gr["combined"][0], combined_M=_s(gr["combined"][1]))
        if gr["cls"] == "F":
            q = grade_data(p, d)[2]
            e.update(n0=gr["n0"], tau=_bound(gr["tau"]), bank_bound=_bound(gr["bank"]),
                     trial_cap=_s(fc["caps"][d]), log2_trial_cap=round(log2_exact(fc["caps"][d]), 4),
                     log2_q_inv_g=round(log2_exact(1 / q ** PROFILE[d - 1]), 4),
                     explicit_M=_s(fcx["grades"][d]["M"]), explicit_n0=fcx["grades"][d]["n0"],
                     fcs_not_above_combined=gr["M"] <= gr["combined"][1])
        grades[str(d)] = e
    out = {
        "label": label,
        "p": str(p),
        "table": table,
        "exact": {k: (_s(v) if v is not None else None) for k, v in exact.items()},
        "rounding_margin": margins,
        "combined": {"S": comb["S"], "arities": {str(d): [s, _s(M)] for d, (s, M) in comb["sch"].items()}},
        "iii": {
            "S": fc["S"], "t": fc["t"], "N_sampler_nodes": _s(fc["N"]), "B": fc["B"],
            "argmax_cap_grade": fc["argmax_cap"], "Gamma0_empty": all(g["cls"] != "0" for g in fc["grades"].values()),
            "schedule2_used": any(g["schedule"] == "S2" for g in fc["grades"].values()),
            "grades": grades,
            "error_budget": {"rank": _bound(fc["rank"]), "bank": _bound(fc["bank"]), "capped_steps": _bound(fc["capped"]),
                             "approximation": _s(EPS / 3), "within_eps": fc["budget_ok"]},
            "explicit_choice": {"Q": _s(fcx["Q"]), "log2_Q": round(log2_exact(fcx["Q"]), 4),
                                "log2_Q_increase": round(log2_exact(fcx["Q"]) - log2_exact(fc["Q"]), 4),
                                "B": fcx["B"], "max_trial_cap_log2": round(log2_exact(fcx["max_cap"]), 4),
                                "within_eps": fcx["budget_ok"]},
        },
        "uniform_kernel": None if uk is None else {
            "rule": "script-defined (combined_budget.py W+3); not stated in main.tex",
            "arities": {str(d): [s, _s(M)] for d, (s, M) in uk["sch"].items()},
            "column_bumps": uk["bumps"], "B": uk["B"], "trees": uk["trees"],
            "tree_abort_bound": _bound(uk["tree_abort"]), "tree_abort_le_1_16": uk["tree_abort_ok"],
            "trials_per_grade_log2": {str(d): round(log2_exact(v), 4) for d, v in uk["trials"].items()},
            "main_tex_literal_rank_term": {
                "note": "bank term 2p^{a-M} as printed in thm:random-column(i) instead of lem:s3-moment(d)",
                "Q_1dp": fmt1(uk_lit["Q"]), "trials_1dp": fmt1(uk_lit["max_trials"]),
                "same_as_table": fmt1(uk_lit["Q"]) == table["uniform_kernel_Q"]
                and fmt1(uk_lit["max_trials"]) == table["uniform_kernel_trials"],
            },
        },
    }
    return out


def macro_map(rows: list[dict], source: str) -> list[dict]:
    """Proposed numbers_map.json entries (not applied by this script)."""
    entries = []
    for i, r in enumerate(rows):
        for col in COLUMNS:
            if r["table"][col] is None:
                continue
            entries.append({"macro": f"Fcs{MACRO_TAGS[r['label']]}{COLUMN_TAGS[col]}", "source": source,
                            "path": f"rows.{i}.table.{col}", "format": "{}"})
    return entries


def build() -> dict:
    rows = [row(label, p) for label, p in PRIMES]
    source = "research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json"
    return {
        "artifact": "tab:fcs-budget (docs/papers/rees-hsp/main.tex)",
        "generator": "theorems/rees_fcs_budget.py",
        "status": "exact computation from the formulas stated in main.tex; AI-checked, pending human review",
        "profile": list(PROFILE),
        "class": len(PROFILE),
        "m": PROFILE[0],
        "eps": _s(EPS),
        "formulas": {
            "combined_Q": "rem:combined-schedule arities; Q = c S prod_d M_d, S = m + ceil(log_p(3/eps)) (after thm:main)",
            "iii": "thm:free-coordinate(iii), rule (R1)-(R4) of app:fc-mixed, least public M_d with beta(M_d,n0;g_d) <= tau_d,"
                   " tau_d = eps/(9(c-1) S n_d); B = ceil(log2(27N/eps)); trial cap ceil(2 B ln2 q^{-g_d})",
            "uniform_kernel": "thm:random-column(i) nodes in a script-defined mixed rule (see uniform_kernel.rule)",
            "rounding": "log2 to one decimal, rounded to nearest, as printed",
        },
        "rows": rows,
        "proposed_numbers_map_entries": macro_map(rows, source),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args(argv)
    data = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    for r in data["rows"]:
        t = r["table"]
        print(f"{r['label']:>8s} & {t['combined_Q']} & {t['uniform_kernel_Q'] or '--'} & "
              f"{t['uniform_kernel_trials'] or '--'} & {t['iii_Q']} & {t['iii_trials']} & {t['iii_total']}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
