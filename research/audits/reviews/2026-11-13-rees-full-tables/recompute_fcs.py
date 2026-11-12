"""Recompute Table tab:fcs-budget (docs/papers/rees-hsp/main.tex) at the Schedule-1 depth
L_d = ceil(log2 t_{p,kappa_d}) of eq:Bd (Lemma lem:rounds), keeping the published-depth values.

Method: reuse theorems/rees_fcs_budget.py UNCHANGED. Its combined rule calls the module-level
function `combined_choice`, whose Schedule-1 branch uses the full depth ceil(log2(kappa+1)).
We first build every row with the module as it is (published depth) and assert that it
reproduces the printed table; then we replace `combined_choice` by the same rule with the
Schedule-1 arity B_d(g_d) = G(kappa_d, g_d)^{L_d} of eq:Bd, taken from
theorems.rees_hsp_reduction.zero_sum_sde_arity, and rebuild. Nothing in theorems/ is edited.

Also recomputed: the worst-case combined counts of the caption (944.9, 555.4, 61.5), the
triangular-variant count of main.tex l. 884 (555.4 -> 542.0 at 2^61-1), and, per row, the
Schedule-1 grades, their (kappa, t, L), whether the preprocessing of lem:zero-sum-length(iv)
is Las Vegas there, the block-steered grades and the Schedule-2 grades kept.

Run (repo root):
  nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-full-tables/recompute_fcs.py
Writes recompute_fcs.json next to this file. Exact integer arithmetic; log2 only for printing.
Finite computation; AI-checked, pending human review.
"""
from __future__ import annotations

import json
import sys
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))

import theorems.rees_fcs_budget as fb  # noqa: E402
from theorems.rees_hsp_reduction import zero_sum_length, zero_sum_sde_arity  # noqa: E402

PRINTED = {  # main.tex tab:fcs-budget as of 2026-11-12 (published depth)
    "11": ("202.1", None, None, "42.3", "28.3", "47.0", "103.5"),
    "1031": ("167.3", None, None, "36.6", "33.4", "50.8", "93.0"),
    "5281": ("852.3", "50.3", "128.2", "39.1", "33.8", "52.2", "119.9"),
    "2^31-1": ("940.3", "50.9", "121.6", "35.9", "31.0", "49.8", "127.1"),
    "2^61-1": ("533.4", "52.9", "128.3", "34.1", "33.5", "51.0", "150.8"),
    "2^127-1": ("41.4", "49.9", "115.2", "34.0", "31.0", "49.5", "142.0"),
}
PRINTED_WORST = {"2^31-1": "944.9", "2^61-1": "555.4", "2^127-1": "61.5"}
PRINTED_TRIANGULAR_2_61 = "542.0"

ORIGINAL_CHOICE = fb.combined_choice


def zero_sum_choice(p: int, d: int, gd: int):
    """rem:combined-schedule with M_d = B_d(g_d) of eq:Bd at the Schedule-1 grades."""
    k, _, _ = fb.grade_data(p, d)
    if k == 1:
        return "lin", gd + 1
    if p >= 16 * k ** (2 * k + 2):
        return "S2", (gd + 1) * ((k - 1) * gd + 1)
    return "S1", zero_sum_sde_arity(p, d, gd)


def triangular_worst(p: int, choice) -> int:
    """Worst-case combined rule with the Schedule-2 arity replaced by (g+1)(g+2)/2
    (prop:triangular-sde under the same guard), as in main.tex l. 884."""
    c, m = len(fb.PROFILE), fb.PROFILE[0]
    S = m + fb.ceil_log_base(p, 3 / fb.EPS)
    acc = 1
    for d in range(2, c + 1):
        gd = fb.PROFILE[d - 1]
        name, M = choice(p, d, gd)
        if name == "S2":
            M = (gd + 1) * (gd + 2) // 2
        acc *= M
    return c * S * acc


def s1_grades(p: int):
    out = []
    for d in range(2, len(fb.PROFILE) + 1):
        name, _ = zero_sum_choice(p, d, fb.PROFILE[d - 1])
        if name != "S1":
            continue
        k = gcd(d, p - 1)
        t = zero_sum_length(p, k)
        L = (t - 1).bit_length()
        full = (k + 1 - 1).bit_length()  # ceil(log2(k+1))
        h = (p - 1) // k
        las_vegas = (k % 2 == 0) and p >= 4 * k ** 4
        out.append(dict(d=d, kappa=k, t=t, L=L, full_depth=full, h_even=(h % 2 == 0),
                        preprocessing="Las Vegas" if las_vegas else "deterministic"))
    return out


def build_rows():
    return [fb.row(label, p) for label, p in fb.PRIMES]


def main() -> int:
    # ---- published depth: reproduce the printed table
    fb.combined_choice = ORIGINAL_CHOICE
    old_rows = build_rows()
    old_tri = {label: fb.fmt1(triangular_worst(p, ORIGINAL_CHOICE)) for label, p in fb.PRIMES}
    problems = []
    for r in old_rows:
        t = r["table"]
        got = tuple(t[c] for c in fb.COLUMNS)
        if got != PRINTED[r["label"]]:
            problems.append(("published row mismatch", r["label"], got, PRINTED[r["label"]]))
        if r["label"] in PRINTED_WORST and t["combined_worst_case_Q"] != PRINTED_WORST[r["label"]]:
            problems.append(("published worst-case mismatch", r["label"], t["combined_worst_case_Q"]))
    if old_tri["2^61-1"] != PRINTED_TRIANGULAR_2_61:
        problems.append(("published triangular mismatch", old_tri["2^61-1"]))

    # ---- zero-sum depth
    fb.combined_choice = zero_sum_choice
    new_rows = build_rows()
    new_tri = {label: fb.fmt1(triangular_worst(p, zero_sum_choice)) for label, p in fb.PRIMES}
    fb.combined_choice = ORIGINAL_CHOICE

    summary = []
    for (label, p), o, n in zip(fb.PRIMES, old_rows, new_rows):
        assert n["iii"]["Gamma0_empty"], "a Gamma_0 grade would use the full-depth B_IS"
        s2_kept = [d for d, (s, _) in n["combined"]["arities"].items() if s == "S2"]
        s1_kept = [d for d, (s, _) in n["combined"]["arities"].items() if s == "S1"]
        s1_kept_wc = [d for d, (s, _) in n["combined_worst_case"]["arities"].items() if s == "S1"]
        changed = {c: (o["table"][c], n["table"][c]) for c in list(fb.COLUMNS) + ["combined_worst_case_Q"]
                   if o["table"][c] != n["table"][c]}
        uk_same = (o["uniform_kernel"] == n["uniform_kernel"])
        summary.append(dict(
            label=label, p=str(p),
            published=o["table"], zero_sum=n["table"], changed=changed,
            uniform_kernel_record_identical=uk_same,
            combined_arities_published=o["combined"]["arities"],
            combined_arities_zero_sum=n["combined"]["arities"],
            bs_grades_published=o["combined"]["bs_grades"], bs_grades_zero_sum=n["combined"]["bs_grades"],
            s2_grades_kept_zero_sum=s2_kept, s1_grades_kept_zero_sum_bs=s1_kept,
            s1_grades_worst_case_zero_sum=s1_kept_wc,
            s1_grade_depths=s1_grades(p),
            triangular_worst_published=old_tri[label], triangular_worst_zero_sum=new_tri[label],
            exact_combined_Q_zero_sum=n["exact"]["combined_Q"],
            exact_combined_worst_case_Q_zero_sum=n["exact"]["combined_worst_case_Q"],
            rounding_margin_zero_sum=n["rounding_margin"],
        ))
    out = dict(
        artifact="tab:fcs-budget at the zero-sum depth (docs/papers/rees-hsp/main.tex)",
        generator="research/audits/reviews/2026-11-13-rees-full-tables/recompute_fcs.py",
        method="theorems/rees_fcs_budget.py unchanged; combined_choice replaced by eq:Bd arity",
        status="exact finite computation; AI-checked, pending human review",
        published_reproduced=not problems, problems=problems, rows=summary)
    (HERE / "recompute_fcs.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    hdr = ("p", "comb", "uk", "ukTr", "iiiQ", "iiiTr", "iiiTot", "wd", "worst", "tri")
    print("published reproduced:", not problems, problems)
    print(" ".join(f"{h:>8s}" for h in hdr))
    for s in summary:
        for tag, t, tri in (("old", s["published"], s["triangular_worst_published"]),
                            ("new", s["zero_sum"], s["triangular_worst_zero_sum"])):
            vals = [t[c] or "--" for c in fb.COLUMNS] + [t["combined_worst_case_Q"], tri]
            print(f"{s['label']:>8s} " + " ".join(f"{v:>8s}" for v in vals) + f"  {tag}")
        print("          changed:", s["changed"], "| uk identical:", s["uniform_kernel_record_identical"])
        print("          BS grades old/new:", s["bs_grades_published"], s["bs_grades_zero_sum"],
              "| S2 kept:", s["s2_grades_kept_zero_sum"], "| S1 kept (BS rule):", s["s1_grades_kept_zero_sum_bs"],
              "| S1 (worst case):", s["s1_grades_worst_case_zero_sum"])
        print("          S1 depths:", s["s1_grade_depths"])
        print("          new combined arities:", s["combined_arities_zero_sum"])
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
