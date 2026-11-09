# 2026-11-08-rees-sde-fq-nest: output files (index added 9 Nov 2026)

Note: `../2026-11-08-rees-sde-fq-nest.md`. Interpreter `/opt/anaconda3/bin/python -B`. No output
was deleted. Coverage of the case-split outputs is checked by `check_split_cover.py`
(`check_split_cover.out`); `tests/test_rees_sde_fq_cnf5.py` re-runs one UNSAT and one SAT control.

## `big_*.out`: unsplit PicoSAT runs (gadget_cnf4.py via run_big.sh)

Eight of the twelve files are **empty (0 bytes)**: those PicoSAT runs were stopped on
2026-11-09 before they printed a result (stated by the pass that ran them; the files carry no
timestamp inside). An empty file is NOT a result, SAT or UNSAT. The run parameters below are read
from the file names with the `run_big.sh` convention `p S k d L` and are inferred, not recorded.

| empty file | run (inferred) | superseded by |
|---|---|---|
| `big_7_nest.out` | p=7, pow:2, k=2, d=2, nest | `cases7.out` (19 Lemma U cases, PicoSAT); there is no `*_split.out` at p = 7, k = 2 |
| `big_7_all.out` | p=7, pow:2, k=2, d=2, all | `cases7_all.out` |
| `big_11_nest.out` | p=11, pow:2, k=2, d=2, nest | `cases11_split.out` (3751 sub-cases, LRAT-verified) |
| `big_13_nest.out` | p=13, pow:2, k=2, d=2, nest | `cases13_split.out` (6253 sub-cases, LRAT-verified) |
| `big_7_k3deps_nest.out` | p=7, pow:2, k=3, d=2, nest | `k3_7_split.out` (686 sub-cases, LRAT-verified) |
| `big_13_int_nest.out` | p=13, int:3, k=2, d=2, nest (the "(b) q=13" row) | nothing: `int13_split.out` is also empty; the cell is still open |
| `big_5_d3_k2.out`, `big_5_d3_k3_nest.out` | p=5, d=3 (k=2 / k=3) | nothing in this folder (no `*_split.out`) |

Non-empty `big_*.out` (results kept): `big_7_int_nest.out`, `big_7_k3_nest.out` (p=7, S={0,1,6}:
UNSAT, 1.3 s), `big_11_int_nest.out` (p=11, S={0,1,2,9,10}: UNSAT, 581 s, P-equivariant problem
only), `big_13_k3_nest.out` (p=13, S={0,1,5,8,12}: UNSAT, 2807 s, PicoSAT, no proof).

## `*_split.out`: case-split runs (gadget_cnf5.py, CaDiCaL + lrat-check via run_split*.sh)

| file | case file | sub-cases | status |
|---|---|---|---|
| `cases11_split.out` | `cases11.txt` | 31 x 11^2 = 3751 | all UNSAT, LRAT VERIFIED (checker OK) |
| `cases13_split.out` | `cases13.txt` | 37 x 13^2 = 6253 | all UNSAT, LRAT VERIFIED (checker OK) |
| `k3_7_split.out` | `cases7k3.txt` | 2 x 7^3 = 686 | all UNSAT, LRAT VERIFIED (checker OK) |
| `int13_split.out` | none | 0 | empty; no coverage claimed |

Run `python check_split_cover.py` from this folder to re-check.
