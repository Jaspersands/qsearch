# 2026-11-08-rees-sde-fq-nest: output files (index added 9 Nov 2026)

Note: `../2026-11-08-rees-sde-fq-nest.md`. Interpreter `/opt/anaconda3/bin/python -B`. No output
was deleted. Coverage of the case-split outputs is checked by `check_split_cover.py`
(`check_split_cover.out`); `tests/test_rees_sde_fq_cnf5.py` re-runs one UNSAT and one SAT control.

**9 Nov correction.** Every "LRAT VERIFIED" string in the `*_split.out` files was printed by an unsound
lrat-check build (it accepted an empty clause without a conflict, so a bogus one-line proof "verified"
any CNF). Those runs are CaDiCaL UNSAT, not independently proof-checked (checker was unsound, 9 Nov).
`gadget_cnf5.py`, `run_split.sh` and `run_split_k.sh` now use the fixed build
`../2026-11-09-lrat-checker-fix/lrat-check` and refuse to run with a checker that fails its negative
controls. See `../2026-11-09-lrat-and-audit-fixes.md`. The (11,2) and k = 3 cells were then re-verified case by
case (status column below); the (13,2) rerun is queued in `research/MECHANICAL_FOLLOW_UP_PLAN.md`.

## `big_*.out`: unsplit PicoSAT runs (gadget_cnf4.py via run_big.sh)

Eight of the twelve files are **empty (0 bytes)**: those PicoSAT runs were stopped on
2026-11-09 before they printed a result (stated by the pass that ran them; the files carry no
timestamp inside). An empty file is NOT a result, SAT or UNSAT. The run parameters below are read
from the file names with the `run_big.sh` convention `p S k d L` and are inferred, not recorded.

| empty file | run (inferred) | superseded by |
|---|---|---|
| `big_7_nest.out` | p=7, pow:2, k=2, d=2, nest | `cases7.out` (19 Lemma U cases, PicoSAT); there is no `*_split.out` at p = 7, k = 2 |
| `big_7_all.out` | p=7, pow:2, k=2, d=2, all | `cases7_all.out` |
| `big_11_nest.out` | p=11, pow:2, k=2, d=2, nest | `cases11_split.out` (3751 sub-cases, CaDiCaL UNSAT, not independently proof-checked); the cell itself re-verified with the fixed checker, 9 Nov, as the 31 cases of `cases11.txt` without the γ_(1,1) split (`../2026-11-09-lrat-checker-fix/recheck/cases11_cases.out`, `cases11_c10.out`) |
| `big_13_nest.out` | p=13, pow:2, k=2, d=2, nest | `cases13_split.out` (6253 sub-cases, CaDiCaL UNSAT, not independently proof-checked) |
| `big_7_k3deps_nest.out` | p=7, pow:2, k=3, d=2, nest | `k3_7_split.out` (686 sub-cases, CaDiCaL UNSAT, not independently proof-checked); the cell itself re-verified with the fixed checker, 9 Nov, as the 2 cases of `cases7k3.txt` without the γ_(1,1) split (`../2026-11-09-lrat-checker-fix/recheck/k3_7_cases.out`) |
| `big_13_int_nest.out` | p=13, int:3, k=2, d=2, nest (the "(b) q=13" row) | nothing: `int13_split.out` is also empty; the cell is still open |
| `big_5_d3_k2.out`, `big_5_d3_k3_nest.out` | p=5, d=3 (k=2 / k=3) | nothing in this folder (no `*_split.out`) |

Non-empty `big_*.out` (results kept): `big_7_int_nest.out`, `big_7_k3_nest.out` (p=7, S={0,1,6}:
UNSAT, 1.3 s), `big_11_int_nest.out` (p=11, S={0,1,2,9,10}: UNSAT, 581 s, P-equivariant problem
only), `big_13_k3_nest.out` (p=13, S={0,1,5,8,12}: UNSAT, 2807 s, PicoSAT, no proof).

## `*_split.out`: case-split runs (gadget_cnf5.py, CaDiCaL + lrat-check via run_split*.sh)

| file | case file | sub-cases | status |
|---|---|---|---|
| `cases11_split.out` | `cases11.txt` | 31 x 11^2 = 3751 | coverage OK; all UNSAT by CaDiCaL, not independently proof-checked (checker was unsound, 9 Nov); all 31 cases of `cases11.txt`, each solved as one CNF (the case CNF is a clause prefix of each of its sub-case CNFs), re-verified with the fixed checker (`../2026-11-09-lrat-checker-fix/recheck/cases11_cases.out`, `cases11_c10.out`) |
| `cases13_split.out` | `cases13.txt` | 37 x 13^2 = 6253 | coverage OK; all UNSAT by CaDiCaL, not independently proof-checked (checker was unsound, 9 Nov) |
| `k3_7_split.out` | `cases7k3.txt` | 2 x 7^3 = 686 | coverage OK; all UNSAT by CaDiCaL, not independently proof-checked (checker was unsound, 9 Nov); 2 sub-cases re-verified with the fixed checker (`../2026-11-09-lrat-checker-fix/recheck/refC/rerun_k3_7.out`); both cases of `cases7k3.txt`, each solved as one CNF (the case CNF is a clause prefix of each of its sub-case CNFs), re-verified with the fixed checker (`../2026-11-09-lrat-checker-fix/recheck/k3_7_cases.out`) |
| `int13_split.out` | none | 0 | empty; no coverage claimed |

Run `python check_split_cover.py` from this folder to re-check.
