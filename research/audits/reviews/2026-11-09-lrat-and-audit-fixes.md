# LRAT checker fix and the mechanical-queue audit fixes (9 Nov 2026)

AI only: one Claude Code subagent of the main session; nothing here is human-reviewed. Input:
`2026-11-09-mechanical-queue-audit.md` (X1 and P1-P8). No git actions, except that two read-only commands
(`git check-ignore`, `git status`) were run by mistake; they change nothing. No network; nothing was downloaded. The paper, `docs/` and the
paper-pass prep folder were not touched. Everything ran under `nice -n 19`; CPU used is in §6.

## 0. Summary

- **Checker.** The `lrat-check` build used for every LRAT run of 9 Nov accepted an empty clause without a
  conflict. It is upstream drat-trim master as fetched that morning, not a local edit. A fixed build with
  14 controls is in `2026-11-09-lrat-checker-fix/`. It also closes a second hole that both of the audit's
  patched builds still have: an empty clause with a RAT hint.
- **Re-verified with the fixed checker (certified):**
  - the four p3-nest pattern SAT proofs;
  - the (7,2) unsplit cell;
  - all 64 UNSAT runs of referee C;
  - the k = 3, p = 7 cell and the (11,2) cell, re-done case by case: every case of the cover (2 and 31
    cases) was solved as one CNF, without the γ_(1,1) split, and its proof VERIFIED (§2 note 4).
- **Relabelled "CaDiCaL UNSAT, not independently proof-checked (checker was unsound, 9 Nov)":**
  - the (13,2) cell (6253 sub-cases); its rerun is queued at the top of
    `research/MECHANICAL_FOLLOW_UP_PLAN.md`;
  - the split sub-case runs themselves (3751, 6253 and 686 lines), whose proofs are gone.
  - No claim was strengthened.
- **Audit items P1-P8** are applied. No proof conclusion changed.
  - One new defect turned up while doing P6: a `QS_BIGP`-only `IndexError` in `algt.good_exact`. It is
    fixed, and it could not be reached at the theorem prime.

## 1. The checker

**Defect.**
- Session 193e5e8e fetched `lrat-check.c` from drat-trim master on 9 Nov at 07:02 and built it. The
  file's mtime has not changed since, so it was never edited.
- In that file, line 161 of `checkClause` is commented out:
  `if (res == SUCCESS) return FAILED; // No RAT and no conflict is FAILED`.
- A lemma with no conflict and no RAT hints is then accepted whenever no clause contains its negated
  pivot.
- The empty clause has the pseudo-literal 0 as its pivot, and no clause contains that. So the one-line
  proof `<m+1> 0 0` "verifies" any CNF, including a satisfiable one.

**Second hole.**
- Even with line 161 restored, `2 0 1 -1 0` verifies on the satisfiable CNF `p cnf 1 1 / 1 0`. This is
  an empty clause whose RAT hint is clause 1.
- The RAT branch runs on the pseudo-pivot, and the shortcut `if (mask[clit^1] >= thisMask) return
  SUCCESS; // blocked` then accepts the hint clause.
- The audit's scratch builds `lratfix/lrat-check-fixed` and `lratfix/lrat-check-strict` both verify this
  proof. Each misses 1 of the 14 controls below.

**Fix.** `lrat-check.c` is the upstream copy (`lrat-check.upstream.c`) plus `lrat-check.patch`. The five
changes are marked FIX in the source:
1. Line 161 is restored.
2. The empty clause is accepted only on a RUP conflict. It has no pivot, so RAT hints cannot justify
   it.
3. Hints to never-used clause indices read as DELETED instead of out of bounds.
4. Lemma indices must increase strictly, and the index table grows until the index fits.
5. CNF literals beyond the header's variable count are rejected.

Build and hashes:
- `build.sh` builds the fixed checker and, for comparison only, the upstream copy, then runs the
  controls.
- sha256: source `ae3beb3e…`, binary `13f28c96…`, upstream source `bf07c2ac…`, patch `1aea9f9c…`.
- A run counts as verified only if the checker exits 0 and prints the exact line `c VERIFIED`.

Soundness [argued, from reading the code; not formally verified]:
- With fixes 1 and 2, a lemma is accepted in only two ways: by a RUP conflict from its positive hints,
  or, for a non-empty lemma, by a RAT check over every live clause that contains the negated pivot.
- The empty clause is accepted only by a RUP conflict.
- Assignments that a candidate's RAT check overwrites can only make later checks stricter, never more
  permissive.
- CaDiCaL 3.0.1 LRAT proofs contain no RAT hints, so only the RUP path is used here.

**Controls** (`controls.sh`, output `controls.out`; "upstream" is the verbatim upstream build):

| control | fixed build | upstream |
|---|---|---|
| sat_1 + `2 0 0` (audit X1) | REJECTED | VERIFIED |
| sat_1 + `2 0 1 0` (empty clause, satisfied hint) | REJECTED | VERIFIED |
| sat_1 + `2 0 1 -1 0` (empty clause with a RAT hint) | REJECTED | VERIFIED |
| sat_1 + `2 0 99999 0` (hint to an unused index) | REJECTED | VERIFIED |
| sat_1 + pure-literal lemma, then the empty clause | REJECTED | VERIFIED |
| sat_1 + `1 0 0` (lemma reuses index 1) | REJECTED | VERIFIED |
| sat_or + `2 0 0` | REJECTED | VERIFIED |
| sat_2units + `3 0 0` | REJECTED | VERIFIED |
| sat_2units + `3 0 1 2 0` (hints satisfied, no conflict) | REJECTED | VERIFIED |
| unsat_1 + wrong hint `3 0 1 0` | REJECTED | VERIFIED |
| php54_sat (satisfiable, same clause ids) + CaDiCaL proof of php54 | REJECTED | REJECTED |
| php54 + CaDiCaL proof without its empty-clause line | REJECTED | REJECTED |
| unsat_1 + correct proof `3 0 1 2 0` | VERIFIED | VERIFIED |
| php54 (pigeonhole 5 into 4) + CaDiCaL 3.0.1 LRAT proof | VERIFIED | VERIFIED |

The upstream build verifies 10 of the 12 negative controls. The fixed build matches all 14 expectations.

**Callers.**
- `gadget_cnf5.py`, `pattern_sat.py` and referee C's `free_cnf.py` now:
  - default to the fixed build;
  - call `require_sound_lrat_check()` before use, which raises `RuntimeError` unless the checker rejects
    `2 0 0` and `2 0 1 -1 0` on `p cnf 1 1 / 1 0` and verifies `3 0 1 2 0` on `p cnf 1 2 / 1 0 / -1 0`;
  - accept UNSAT only with exit 0 as well as `c VERIFIED`.
- `run_split.sh` and `run_split_k.sh` run `controls.sh` as a preflight and refuse to start if it fails.
- `tests/test_rees_sde_fq_cnf5.py` prefers the fixed build and adds
  `test_lrat_check_rejects_bogus_empty_clause_proofs`. Result: 3 passed with the fixed build. With the
  upstream build 2 fail, as intended, because `gadget_cnf5.py` refuses that build.

## 2. Every LRAT claim: certified or relabelled

The claims come from `grep -i lrat` over `research/*.md`, `research/audits/reviews/2026-11-0[7-9]*.md`,
the handoff and STATE, plus the folder README.

| claim | status now | evidence |
|---|---|---|
| p3-nest pattern SAT, d = 3: k = 4 all 80 / 54 / 36 patterns, k = 3 12 patterns | **re-verified with the fixed checker, 9 Nov** | `recheck/pattern_proofs.{py,out}` (note 1) |
| (7,2) nested, unsplit (CaDiCaL 1436 s, 12.3 GB proof) | **re-verified with the fixed checker, 9 Nov** | `recheck/unsplit_7_2.{sh,out}`, `unsplit_7_2.original.txt` (note 2) |
| referee C: 38 + 19 + 1 + 3 + 3 = 64 UNSAT runs (p = 7 κ = 2 nested/all, without R, κ = 3, interval k = 1 at q = 11, 13 and p = 7, three gadget_cnf5 reruns) | **re-verified with the fixed checker, 9 Nov** | `recheck/refC_rerun.sh`, `recheck/refC/`, `recheck/refC_compare.{py,out}` (note 3) |
| k = 3 at p = 7 (κ = 2, nested set): 686 sub-cases | **re-verified with the fixed checker, 9 Nov**, as the 2 cases of `cases7k3.txt` without the γ_(1,1) split; the 686 sub-case runs stay CaDiCaL-only | `recheck/k3_7_cases.{sh,out}` (note 4) |
| (11,2): 3751 sub-cases | **re-verified with the fixed checker, 9 Nov**, as the 31 Lemma U cases without the γ_(1,1) split; the 3751 sub-case runs stay CaDiCaL-only | `recheck/case_cert.py`, `recheck/cases11_cases.out`, `recheck/cases11_c10.{txt,out}` (note 4) |
| (13,2): 6253 sub-cases | CaDiCaL UNSAT, not independently proof-checked (checker was unsound, 9 Nov) | queued: case by case (unmeasured, roughly 17-45 core-h scaled from p = 11) or the split (about 58 core-h) |
| `check_split_cover.out`, referee C's `split_coverage.out` | coverage exact; the "LRAT VERIFIED" strings they count are void | annotated in the README, the script docstring and the reports |

Notes:
1. **Pattern SAT proofs.**
   - The four proofs survive only in another session's temp folders.
   - Each leftover `p.cnf` matches by sha256 one of the four CNFs regenerated from `pattern_sat.py`.
   - All four proofs (0.2-6.3 GB) were VERIFIED with exit 0, in 5-106 s each.
2. **(7,2) unsplit.**
   - The CNF was regenerated with `recheck/dump_gadget_cnf.py`: sha256 `9990c084…`, 1134 vars, 106100
     clauses. The original run recorded the same counts but no hash.
   - CaDiCaL said UNSAT in 859 s user CPU. Its proof has exactly the original's size, 12,293,854,888 bytes
     (original result line in `unsplit_7_2.original.txt`).
   - The fixed checker reported `c VERIFIED`, exit 0, in 224 s. Proof sha256 `1e88afef…`; the proof was
     then deleted.
3. **Referee C's runs.**
   - These are referee C's own commands, with the fixed checker.
   - Output lines are identical apart from timings: verdicts, var and clause counts, fix strings, and for
     the gadget_cnf5 runs `cnf_sha256` and `proof_bytes`.
   - All 64 UNSAT runs are VERIFIED. The one SAT run (p = 5 interval) is unchanged.
4. **Case by case: k = 3 at p = 7, and (11,2).**
   - Every case of the case file (`cases7k3.txt`, 2 cases; `cases11.txt`, the 31 Lemma U cases) was
     written as one CNF by `recheck/dump_gadget_cnf.py` (gadget_cnf5's encoding with `--fix CASE`), solved
     by CaDiCaL with gadget_cnf5's flags, and its proof checked by the fixed lrat-check, hashed and deleted.
     Drivers: `recheck/k3_7_cases.sh` and `recheck/case_cert.py`.
   - Tie-in, per case: one recorded sub-case `CASE;1,1,0:…` of the split file was regenerated. Its sha256
     equals the recorded `cnf_sha256`, and it is the case CNF plus trailing unit clauses, with the same
     variable count. So the case CNF is the recorded encoding with the γ_(1,1) units removed, and its UNSAT
     shows the whole case infeasible without the γ_(1,1) split. The case covers are the ones the split
     relied on (Lemma U, `cases_cover.out`; for k = 3 the two-case first-slot cover).
   - k = 3: both cases UNSAT and VERIFIED (case 1: CaDiCaL 1165 s CPU, 22.4 GB proof, check 298 s;
     case 2: 142 s, 2.6 GB, 34 s).
   - (11,2): 31/31 cases UNSAT and VERIFIED: 30 in `cases11_cases.out`, and the case
     `1,0,1:2,0;0,1,1:9,0` in `cases11_c10.out`. That case had the largest split cost (1617 s). I stopped
     its first attempt in the driver by hand after 36 s (the driver line reads `UNKNOWN(rc=-15)`), expecting
     the 1200 s wall cap to cut it off at this machine load, and reran it alone with a 5400 s cap. It
     needed only 606 s CPU (745 s wall; 8.9 GB proof, check 132 s), so the stop was
     not needed; it cost 40 s of CPU. Per case: CaDiCaL 1-650 s CPU, proofs up to 10.4 GB.
   - Cost: the (11,2) split had taken 15,396 s of solver CPU (sum of its recorded times). Case by case took
     3301 s of CaDiCaL and 742 s of checking, 4231 s with dumps and overheads.

Labels changed in:
- `2026-11-08-rees-sde-fq-nest.md`: §0 item 2, the §2 methods paragraph (correction note) and table
  rows, the §4 obstruction paragraph, §8;
- that folder's `README.md` and the `check_split_cover.py` docstring;
- `2026-11-08-rees-sde-p3-nest.md`, lines 261 and 298 (certified);
- `2026-11-09-mechanical-queue-run.md`;
- `2026-11-09-rees-sde-fq-nest-referee-C.md` (bracketed 9 Nov notes; the referee's text is kept);
- `MECHANICAL_FOLLOW_UP_PLAN.md`;
- the two F_q handoff entries, including the Extension title;
- `STATE.md`, lines 15-19 and the SDE row near line 1235.

## 3. Audit items P1-P8

| item | change | check |
|---|---|---|
| P1 Lemma R | `2026-11-08-rees-sde-fq-nest.md` Lemma R restated in referee B's per-slot existence form, with the re-basing proof. Slots are {λα : λ ∈ cP}. If a feasible, weakly nondegenerate solution exists, so does a P-equivariant, normalised one (γ′_{e_j} = 0) built from one member per slot. The earlier statement, which built γ′ from the original γ at fixed representatives, is noted as false in general | statement and proof only; the CNF and every conclusion are unchanged |
| P2 guarantee(14) | "46, 64, 85, 109" → "46, 64, 85, 108" in the plan, run summary, p3-nest (×2) and p3-nest-break | `wnest.guarantee(6..20)` = 30, 46, 64, 85, 108, 133, 191; `bound(n)` = 63, 84, 109, 135 left as is |
| P3 subquad-A-break §11 item 2 | the sentence now says the 3.3 U⁺ recursion was reached on 4 banks (least slack 0) and 3.0 U⁺ on 1; top phase, top-stall recursion, 3.1 W and ranks above 49 not reached | BRANCHES line of `out/bigp_J4k3_1.out` |
| P4 Lemma Z | fq-nest §0 item 5 label "[argued; Lemma Z proves the four-hyperplane confinement and the infeasibility of nested and full label sets]"; (c) "no polynomial of degree below q − 1 here [argued]" | labels only |
| P5 p3-nest §3 table | rows n = 60, 90, 120, 150 now give "sharpened KOW-type recursion" 1359, 2954, 5156, 7966 and KOW's own recursion (8) 1465, 3125, 5405, 8285; `tables.py` header and labels renamed, and it now prints the "WNEST guarantee ≥ sharpened recursion" scan itself | `tables.py` rerun: same numbers, new `tables.out` |
| P6 bigp_equiv | `bigp_equiv.py` also replays the 57 `interesting/*case33_Uplus*` banks (p < 2³¹, saved par_kw, seed from the file name); outputs saved as `out/bigp_equiv_{int64,bigp}.json`, `out/bigp_equiv_compare.out`; break §11 item 2 updated | 79 runs, 0 differences; the new banks reach 3.3 U⁺ (57), 3.0 U⁺ (25), 3.1 W (1), 3.3 closure (6), no top phase; the first 22 runs equal the audit's scratch dump |
| P6, new defect | the QS_BIGP dump crashed in `algt.good_exact` (`t[y]` with an object-dtype index). Fixed: int64 `arange` and `int(bt)`. `good_exact` runs only when the class table exists (p ≤ 3·10⁶), so the theorem-prime run (p ≈ 2.8·10¹²) could not reach it | the int64 dump is byte-identical before and after the fix |
| P7 planted() | `Om = st["Ub"] if "Ub" in st else rebuild(Fd, st["rounds"])`, `rebuild` imported from `subquad`, comment corrected; break §11 item 3 updated | groups planted, stress, thmprime and climb (all four call `planted()`) rerun: output identical to the stored `*_1.out`. `planted_probe.{py,out}`: 352 calls, 0 errors, 108 direct exits, 68 with realised rounds, rebuilt Ω of rank 1-5, never None (counts differ from the audit's 127/87 because the fixed generator draws more random numbers) |
| P8 run summary | the sentence about new p ≈ 2.8e12 `interesting/` files was deleted, with a bracketed note | no such files exist (audit) |

Also, from the audit's Extension 1 nit: `check_split_cover.py` now requires one shared
(p, S, k, d, L) header per file. Its output on the three split files is unchanged, and an edited
copy with one changed S fails.

## 4. Left open / queued

- Queued in `MECHANICAL_FOLLOW_UP_PLAN.md`, "2026-11-09 LRAT Checker Fix: Queued Split Reruns":
  - (13,2), case by case first (`recheck/case_cert.py 13 …`; unmeasured, roughly 17-45 core-h scaled
    from p = 11, more than this pass's 4 core-hour cap), with the split rerun (about 58 core-h, 970 GB
    of proofs in total) as the fallback;
  - a note that other sessions' upstream-built checkers have the same defect.
- Items 1-2 there, (11,2) and k = 3, are marked DONE case by case. Their split reruns are no longer
  needed for the claims.
- The handoff's next command (p = 5, k = 3, "CaDiCaL + lrat-check") now names the fixed build.
- `STATE.md`'s "As of" header was not moved. Three handoff entries are now newer than it: two from other
  work today, and this one. The integrator owns that header.
- I did not inspect cloud sessions. Any LRAT result produced elsewhere with an upstream-built
  lrat-check is a CaDiCaL verdict until re-checked.

## 5. Files

New, in `2026-11-09-lrat-checker-fix/`:
- `lrat-check.c`, `lrat-check.upstream.c`, `lrat-check.patch`;
- `build.sh`, `controls.sh`, `controls/`, `controls.out`, `.gitignore`;
- `recheck/`: `dump_gadget_cnf.py`, `pattern_proofs.{py,out,time}`, `unsplit_7_2.{sh,out}`,
  `unsplit_7_2.original.txt`, `refC_rerun.sh`, `refC/`, `refC_compare.{py,out}`, `k3_7_cases.{sh,out}`,
  `case_cert.py`, `cases11_cases.{out,time}`, `cases11_c10.{txt,out,time}`.

Other new files:
- `2026-11-07-rees-sde-subquad-A/planted_probe.{py,out}`;
- `2026-11-07-rees-sde-subquad-A-break/out/bigp_equiv_{int64,bigp}.json` and `bigp_equiv_compare.out`.

Edited code:
- `2026-11-08-rees-sde-fq-nest/{gadget_cnf5.py, run_split.sh, run_split_k.sh, check_split_cover.py}`;
- `2026-11-08-rees-sde-p3-nest/{pattern_sat.py, tables.py, tables.out}`;
- `2026-11-09-rees-sde-fq-nest-referee-C/free_cnf.py`;
- `2026-11-07-rees-sde-subquad-A/run_tests.py`;
- `2026-11-07-rees-sde-subquad-A-break/{bigp_equiv.py, algt.py}`;
- `tests/test_rees_sde_fq_cnf5.py`.

Edited text: the files listed at the end of §2, plus the `2026-11-07-rees-sde-subquad-A-break.md` §11
items 2-3 and the run summary's P8 note.

## 6. CPU

Everything ran under `nice -n 19` on a machine at load 75-120 (10 cores), so wall times are long.

| work | CPU |
|---|---|
| controls, builds, the P5-P7 reruns, the cnf5 tests (partly untimed, estimated) | about 550 s |
| pattern proofs (`pattern_proofs.time`) | 146 s |
| referee C reruns (`refC/run.time`) | 162 s |
| (7,2) unsplit (CaDiCaL 891 s user + sys, check 189 s, `unsplit_7_2.out`) | 1080 s |
| k = 3 cases (CaDiCaL 1306 s, checks 332 s, plus CNF dumps and hashing) | about 1790 s |
| (11,2) driver, 31 cases with the stopped one (`cases11_cases.time`) | 3484 s |
| (11,2) case `1,0,1:2,0;0,1,1:9,0` alone (`cases11_c10.time`) | 747 s |
| total | about 8000 s = 2.2 core-h (cap about 4) |
