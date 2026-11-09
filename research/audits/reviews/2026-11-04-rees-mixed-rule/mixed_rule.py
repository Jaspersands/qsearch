"""Independent recomputation of the uniform-kernel column of tab:fcs-budget (Rees HSP paper)
from the rule stated as prop:mixed-schedule in ../2026-11-04-rees-mixed-rule.md.

Written from the statement only. Imports nothing from combined_budget.py, fcs_budget.py or
theorems/rees_fcs_budget.py. All arithmetic is exact (int / Fraction); log2 values are rounded
to one decimal by exact integer comparison (round(10 log2 x) = k iff 2^(2k-1) <= x^20 < 2^(2k+1)).

Run (from the repo root):
  nice -n 10 /opt/anaconda3/bin/python research/audits/reviews/2026-11-04-rees-mixed-rule/mixed_rule.py
Writes mixed_rule.json next to this file.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as Fr
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TABLE_JSON = ROOT / "research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json"

PROFILE = (19, 17, 16, 14, 12, 9, 6, 3, 1)   # g_1 = m, g_2, ..., g_9
EPS = Fr(1, 3)
PRIMES = [("11", 11), ("1031", 1031), ("5281", 5281), ("2^31-1", 2**31 - 1),
          ("2^61-1", 2**61 - 1), ("2^127-1", 2**127 - 1)]


# ------------------------------------------------------------------ small exact helpers

def least_pow2_exp(x) -> int:
    """least integer e >= 0 with 2^e >= x (x a positive int or Fraction)."""
    x = Fr(x)
    e = 0
    while Fr(2**e) < x:
        e += 1
    return e


def round_log2_1dp(x: int) -> str:
    """log2 of a positive integer x, rounded to one decimal, decided exactly."""
    assert x >= 1
    k = (x.bit_length() - 1) * 10           # starting guess
    x20 = x**20
    while not (x20 < 2**(2 * k + 1)):
        k += 1
    while not (2**max(2 * k - 1, 0) <= x20) and k > 0:
        k -= 1
    assert 2**(2 * k - 1) <= x20 < 2**(2 * k + 1)
    return f"{k // 10}.{k % 10}"


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for q in small:
        if n % q == 0:
            return n == q
    dd, s = n - 1, 0
    while dd % 2 == 0:
        dd //= 2
        s += 1
    for a in small:          # deterministic for n < 3.3e24; probabilistic-strong beyond
        x = pow(a, dd, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


# ------------------------------------------------------------------ the node types

def ivanyos_santha_arity(k: int, a: int) -> int:
    """B_k(a) = (k^{k(k-1)/2} (a+1)^k)^{ceil(log2(k+1))}  (thm:is-import)."""
    e = least_pow2_exp(k + 1)
    return (k**(k * (k - 1) // 2) * (a + 1)**k)**e


def worst_case_choice(p: int, d: int, g: int):
    """rem:combined-schedule (no label law)."""
    k = gcd(d, p - 1)
    if k == 1:
        return ("lin", g + 1)
    if p >= 16 * k**(2 * k + 2):
        return ("S2", (g + 1) * ((k - 1) * g + 1))
    return ("S1", ivanyos_santha_arity(k, g))


def bank_bound(p: int, d: int, g: int, M: int, printed: bool = False) -> Fr:
    """Public bound on the bank event of a uniform-kernel node at a = g (worst case; monotone in a):
    4/mu + Pr[rank < a], mu = ((h+1)^M - 1)/(h p^a).  Pr[rank<a] <= (p^a-1)/((p-1)p^M)  (lem:s3-moment(d));
    printed=True uses 2 p^{a-M} as printed in thm:random-column(i)."""
    k = gcd(d, p - 1)
    h = (p - 1) // k
    t1 = Fr(4 * h * p**g, (h + 1)**M - 1)
    t2 = Fr(2 * p**g, p**M) if printed else Fr(p**g - 1, (p - 1) * p**M)
    return t1 + t2


# ------------------------------------------------------------------ the mixed rule (prop:mixed-schedule, rule (U1)-(U4))

def mixed_rule(p: int, profile=PROFILE, eps: Fr = EPS, printed: bool = False, max_bumps: int = 200):
    c, m = len(profile), profile[0]
    g = {d: profile[d - 1] for d in range(1, c + 1)}
    # (U1) per-grade node type
    typ, M, u = {}, {}, {}
    for d in range(2, c + 1):
        k = gcd(d, p - 1)
        t0, M0 = worst_case_choice(p, d, g[d])
        ud = max(2, k, g[d] + 1)
        if p >= 16 * ud * ud and 4 * ud < M0:
            typ[d], M[d], u[d] = "S3", 4 * ud, ud
        else:
            typ[d], M[d] = t0, M0
    if "S3" not in typ.values():
        return None
    # (U2) weighted bank budget, raising the worst uniform-kernel grade by one column
    bumps = 0
    while True:
        n, acc = {}, 1
        for d in range(2, c + 1):
            n[d] = acc
            acc *= M[d]
        P = acc
        wb = {d: n[d] * bank_bound(p, d, g[d], M[d], printed) for d in typ if typ[d] == "S3"}
        bank = sum(wb.values(), Fr(0))
        if bumps == 0:
            n3_0 = sum(n[d] for d in typ if typ[d] == "S3")
            n2_0 = sum(n[d] for d in typ if typ[d] == "S2")
            B0 = max(1, least_pow2_exp(64 * max(1, 3 * n3_0 + n2_0)))
            unweighted_abort = bank + (3 * n3_0 + n2_0) * Fr(1, 2**B0)
            M_initial = dict(M)
        if bank <= Fr(1, 64):
            break
        bumps += 1
        if bumps > max_bumps:
            return dict(nonterminating=True, p=p)
        worst = max(sorted(wb), key=lambda dd: wb[dd])
        M[worst] += 1
    # (U3) caps
    n3 = sum(n[d] for d in typ if typ[d] == "S3")
    n2 = sum(n[d] for d in typ if typ[d] == "S2")
    B = least_pow2_exp(64 * max(1, 3 * n3 + n2))
    B = max(B, 1)
    tree_abort = bank + (3 * n3 + n2) * Fr(1, 2**B)
    # (U4) restarts
    mp = m + least_pow2_exp(3 / eps)
    trees = 4 * mp
    Q = c * trees * P
    trials = {d: 4 * gcd(d, p - 1)**M[d] * B for d in typ if typ[d] == "S3"}
    # hypothesis checks of prop:mixed-schedule
    hyp = []
    for d in typ:
        k = gcd(d, p - 1)
        if typ[d] == "S3":
            hyp.append(u[d] >= max(2, k, g[d] + 1) and p >= 16 * u[d]**2 and M[d] >= 4 * u[d] and k < p - 1)
        elif typ[d] == "S2":
            hyp.append(k >= 2 and p >= 16 * k**(2 * k + 2) and M[d] >= (g[d] + 1) * ((k - 1) * g[d] + 1))
        elif typ[d] == "S1":
            hyp.append(M[d] >= ivanyos_santha_arity(k, g[d]))
        else:
            hyp.append(k == 1 and M[d] >= g[d] + 1)
    rank_fail = Fr(p**m - 1, (p - 1) * p**mp)
    few = binom(4 * mp, 3 * mp) * tree_abort**(3 * mp)
    n_instr = trees * (P + sum(n[d] * (M[d] + 1) for d in n)) + mp
    return dict(
        p=p, types={d: typ[d] for d in sorted(typ)}, M={d: M[d] for d in sorted(M)},
        u={d: u[d] for d in sorted(u)}, n=n, P=P, bumps=bumps, bank=bank, n_S3=n3, n_S2=n2, B=B,
        tree_abort=tree_abort, no_bump_tree_abort=unweighted_abort, M_initial=M_initial, mprime=mp, trees=trees, Q=Q, trials=trials,
        max_trials=max(trials.values()), hypotheses_ok=all(hyp),
        rank_fail=rank_fail, few_successes=few, n_instr=n_instr,
        error_ok=(tree_abort <= Fr(1, 16) and rank_fail <= eps / 3 and few <= eps / 3),
    )


def binom(n: int, k: int) -> int:
    r = 1
    for i in range(k):
        r = r * (n - i) // (i + 1)
    return r


def f_up_log2(x: Fr) -> float:
    """an upper float for log2 of a positive Fraction, for display only."""
    from math import log2
    return log2(x.numerator) - log2(x.denominator)


# ------------------------------------------------------------------ scans

def scan(profile, pmax: int, pmin: int | None = None):
    """Every prime p (c < p <= pmax) at which the rule uses a uniform-kernel node: bumps, termination,
    and whether the hypotheses and the error budget hold."""
    c = len(profile)
    out = dict(profile=list(profile), pmax=pmax, primes_with_S3=0, first_S3=None, bump_primes=[],
               nonterminating=[], hyp_fail=[], err_fail=[], max_tree_abort_log2=None,
               no_bump_fail_count=0, first_no_bump_fail=None)
    worst = None
    p = max(c + 1, pmin or 0)
    while p <= pmax:
        if is_prime(p):
            r = mixed_rule(p, profile)
            if r is not None:
                if r.get("nonterminating"):
                    out["nonterminating"].append(p)
                else:
                    out["primes_with_S3"] += 1
                    out["first_S3"] = out["first_S3"] or p
                    if r["bumps"]:
                        out["bump_primes"].append([p, r["bumps"]])
                    if r["no_bump_tree_abort"] > Fr(1, 16):
                        out["no_bump_fail_count"] += 1
                        if out["first_no_bump_fail"] is None:
                            out["first_no_bump_fail"] = dict(
                                p=p, no_bump_tree_abort_log2=round(f_up_log2(r["no_bump_tree_abort"]), 3),
                                M_initial={str(d): v for d, v in r["M_initial"].items()},
                                M_final={str(d): v for d, v in r["M"].items()}, types={str(d): t for d, t in r["types"].items()},
                                bumps=r["bumps"], final_tree_abort_log2=round(f_up_log2(r["tree_abort"]), 3))
                    if not r["hypotheses_ok"]:
                        out["hyp_fail"].append(p)
                    if not r["error_ok"]:
                        out["err_fail"].append(p)
                    ta = f_up_log2(r["tree_abort"])
                    worst = ta if worst is None else max(worst, ta)
        p += 1
    out["max_tree_abort_log2"] = worst
    out["bump_primes"] = out["bump_primes"][:40] + ([["...", len(out["bump_primes"])]] if len(out["bump_primes"]) > 40 else [])
    return out


# ------------------------------------------------------------------ main

def main() -> int:
    table = json.loads(TABLE_JSON.read_text())
    rows_json = {str(r["p"]): r for r in table["rows"]}
    rows, mismatches = [], []
    for label, p in PRIMES:
        assert is_prime(p)
        r = mixed_rule(p)
        rp = mixed_rule(p, printed=True)
        jr = rows_json[str(p)]
        if r is None:
            mine = dict(Q="--", trials="--")
            ok = jr["table"]["uniform_kernel_Q"] is None and jr["table"]["uniform_kernel_trials"] is None
            printed_same = rp is None
            exact_same = ok
            rec = dict(label=label, p=p, uses_uniform_kernel=False, table=mine, json_table=jr["table"],
                       agree=ok, printed_bank_term_same=printed_same)
        else:
            mine = dict(Q=round_log2_1dp(r["Q"]), trials=round_log2_1dp(r["max_trials"]))
            ok = (mine["Q"] == jr["table"]["uniform_kernel_Q"] and mine["trials"] == jr["table"]["uniform_kernel_trials"])
            exact_same = (str(r["Q"]) == jr["exact"]["uniform_kernel_Q"]
                          and str(r["max_trials"]) == jr["exact"]["uniform_kernel_trials"])
            ju = jr["uniform_kernel"]
            sched_same = ({str(d): [r["types"][d], str(r["M"][d])] for d in r["types"]} == ju["arities"]
                          and r["B"] == ju["B"] and r["trees"] == ju["trees"] and r["bumps"] == ju["column_bumps"])
            printed_same = (round_log2_1dp(rp["Q"]) == mine["Q"] and round_log2_1dp(rp["max_trials"]) == mine["trials"])
            rec = dict(label=label, p=p, uses_uniform_kernel=True, table=mine, json_table={k: jr["table"][k] for k in ("uniform_kernel_Q", "uniform_kernel_trials")},
                       agree=ok, exact_integers_agree=exact_same, schedule_B_trees_bumps_agree=sched_same,
                       printed_bank_term_same=printed_same,
                       types={str(d): t for d, t in r["types"].items()}, M={str(d): v for d, v in r["M"].items()},
                       u={str(d): v for d, v in r["u"].items()},
                       n_S3=str(r["n_S3"]), n_S2=str(r["n_S2"]), B=r["B"], bumps=r["bumps"],
                       bank_log2_up=round(f_up_log2(r["bank"]), 4) if r["bank"] else None,
                       tree_abort_log2_up=round(f_up_log2(r["tree_abort"]), 4),
                       tree_abort_le_1_32=r["tree_abort"] <= Fr(1, 32),
                       trials_log2={str(d): round(f_up_log2(Fr(v)), 4) for d, v in r["trials"].items()},
                       Q_exact=str(r["Q"]), max_trials_exact=str(r["max_trials"]),
                       hypotheses_ok=r["hypotheses_ok"], error_ok=r["error_ok"],
                       few_successes_log2=round(f_up_log2(r["few_successes"]), 2),
                       rank_fail_log2=round(f_up_log2(r["rank_fail"]), 2),
                       n_instr_log2=round(f_up_log2(Fr(r["n_instr"])), 2))
            if not (exact_same and sched_same):
                ok = False
        if not ok:
            mismatches.append(label)
        rows.append(rec)
    scans = []
    if "--scan" in sys.argv:
        pmax = int(sys.argv[sys.argv.index("--scan") + 1])
        scans = [scan(PROFILE, pmax), scan((6, 4, 2), min(pmax, 20_000)), scan((8, 5, 3, 1), min(pmax, 20_000)),
                 scan((10, 7, 5, 3, 1), min(pmax, 20_000)), scan((4, 3), min(pmax, 5_000))]
    out = dict(artifact="mixed_rule.json", generator="research/audits/reviews/2026-11-04-rees-mixed-rule/mixed_rule.py",
               status="exact computation; AI-checked, pending human review",
               profile=list(PROFILE), eps=str(EPS), rows=rows, mismatches=mismatches, scans=scans)
    (HERE / "mixed_rule.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(f"{'p':>8s} {'ukQ':>6s} {'trials':>7s}  json      agree exact sched printed  bumps B   tree_abort")
    for r in rows:
        print(f"{r['label']:>8s} {r['table']['Q']:>6s} {r['table']['trials']:>7s}  "
              f"{str(r['json_table']):s} {r['agree']} {r.get('exact_integers_agree')} {r.get('schedule_B_trees_bumps_agree')} "
              f"{r['printed_bank_term_same']} {r.get('bumps')} {r.get('B')} {r.get('tree_abort_log2_up')}")
        if r["uses_uniform_kernel"]:
            print("          types", r["types"], "M", r["M"])
    for s in scans:
        print("scan", {k: v for k, v in s.items()})
    print("mismatches:", mismatches)
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
