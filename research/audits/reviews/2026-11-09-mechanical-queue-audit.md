# Audit of the 9 Nov mechanical queue run (AI only; read-only except this file)

Subject: `2026-11-09-mechanical-queue-run.md` and every plan item it marks DONE in
`research/MECHANICAL_FOLLOW_UP_PLAN.md` (sections "2026-11-08 Rees SDE Open Directions", "2026-11-07 Rees
SDE Worst Case Below a²" and the 2026-11-09 sections). For each item I checked the diff (`git diff`/`git log -p`,
read-only), the acceptance test (rerun where cheap) and every mathematical statement, bound or table value
the run touched, against the named referee and break reports. Paths below are relative to
`research/audits/reviews/` unless absolute. About 17 CPU-minutes, all under `nice -n 19`. Audit scratch files are in
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/audit/`
(temporary). No proof conclusion of the run is overturned. The **"LRAT-verified"** label is the exception: it is
void wherever the proof was not kept (X1).

## Problems, most material first

| # | where | problem | fix |
|---|---|---|---|
| X1 | all CaDiCaL/LRAT runs (pattern SAT, F_q splits, referee C, cnf5 test) | the `lrat-check` build used accepts an empty clause **without a conflict**: any CNF, satisfiable or not, "verifies" with the one-line proof `<m+1> 0 0` | restore the check; add a negative control; rerun or relabel the deleted-proof claims (details below) |
| P1 | Ref 1, `2026-11-08-rees-sde-fq-nest.md` Lemma R | statement and first proof line unchanged; the appended repair says that exact construction can fail | restate Lemma R as the per-slot existence statement |
| P2 | OD 1/3, p3-nest note, break report, plan, run summary | "exact guarantee(n) is 46, 64, 85, 109": guarantee(14) = **108** | 109 → 108 in five places |
| P3 | WC 2, `…-subquad-A-break.md` §11 item 2 | "the 3.3 U⁺ branch at this prime [was] not reached" is false: reached on 4 banks, least `rec_count_U+33` slack 0 | rewrite the sentence (text below) |
| P4 | Ref 1, fq-nest note Lemma Z / §0 item 5 | referee C finding 6, third bullet not applied: "nothing of lower degree from this framework" still labelled [proved, Lemma Z] | label it [argued] |
| P5 | OD 3, p3-nest note §3 table | rows 90/120/150 still say "KOW 2954/5156/7966"; these are the note's sharpened recursion, not KOW (8) (3125/5405/8285) | relabel as in row 60 |
| P6 | WC 2 provenance | `bigp_equiv.py` result not saved; its 22 banks reach none of the case-3.x branches used at the theorem prime | save the compare output; add case-3.3 seed banks |
| P7 | WC 3, `…-subquad-A/run_tests.py` `planted()` | the fix comment "No round has then been realised" is false (87 of 127 direct exits had realised rounds); Ω silently dropped | `Om = st["Ub"] if "Ub" in st else rebuild(Fd, st["rounds"])` |
| P8 | run summary line 54 | "the new `interesting/` files written by `attack_bigp.py` carry p ≈ 2.8e12 banks": no such files exist | delete the sentence |

Nits are listed under each item.

## X1. The lrat-check build is unsound for the final step (material, cross-cutting)

- Binary:
  `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/193e5e8e-8fb0-4a70-a091-69686db23be7/scratchpad/drat-trim/lrat-check`,
  sha256 `9995c9c8e2c641516ed3…`. The copy in session `78b843a7`'s scratchpad has the same hash.
- Who uses it:
  - `pattern_sat.py` (via `LRAT_CHECK`);
  - `run_split.sh` and `run_split_k.sh` (`export LRAT_CHECK=$SCRATCH/drat-trim/lrat-check`);
  - referee C's `free_cnf.py` (hard-coded path);
  - `tests/test_rees_sde_fq_cnf5.py` (as run).
- In `lrat-check.c`, `checkClause`, line 161 is commented out:
  `//    if (res == SUCCESS) return FAILED; // No RAT and no conflict is FAILED`. A lemma whose hints propagate
  without a conflict then falls through to the vacuous-RAT test. That test is sound for a non-empty clause:
  it is a blocked clause. It is unsound for the empty clause.
- Controls, rerun today:

  | CNF | proof | original build | fixed build |
  |---|---|---|---|
  | `p cnf 1 1 / 1 0` (SAT) | `2 0 0` | c VERIFIED | NOT VERIFIED |
  | `p cnf 1 1 / 1 0` (SAT) | `2 0 1 0` | c VERIFIED | NOT VERIFIED |
  | `p cnf 2 1 / 1 2 0` (SAT) | `2 0 0` | c VERIFIED | NOT VERIFIED |
  | `p cnf 2 2 / 1 0 / 2 0` (SAT) | `3 0 1 2 0` | c VERIFIED | NOT VERIFIED |
  | `p cnf 1 2 / 1 0 / -1 0` (UNSAT) | wrong hint `3 0 1 0` | c VERIFIED | NOT VERIFIED |
  | same UNSAT CNF | correct `3 0 1 2 0` | c VERIFIED | VERIFIED |

  - Two builds count as "fixed" here: `lratfix/lrat-check-fixed` (rejects only an empty clause without a
    conflict) and `lratfix/lrat-check-strict` (line 161 restored, pure LRUP). Both give the results in the last
    column.
  - drat-trim in DRAT mode rejects the bogus proofs too.
  - Intermediate lemmas are still checked. So "c VERIFIED" from this build does **not** certify UNSAT: it only
    shows that the solver's lemmas are valid.
- Effect on DONE items:
  - The pattern SAT k = 4 proofs survive in temp folders, and I re-verified them (OD 2: certified).
  - Everything whose proof was deleted (`gadget_cnf5.py` deletes proofs unless `keep=True`) is a CaDiCaL verdict
    only:
    - the 3751/6253/686 split sub-cases checked by `check_split_cover.py`;
    - the unsplit (7,2) run ("12.3 GB LRAT proof verified", handoff entry "2026-11-09 Rees SDE F_q Extension",
      whose title says "(LRAT-Verified)");
    - the 64 "LRAT VERIFIED" lines in referee C's `*.out` files;
    - `STATE.md` line 15 ("Exact, LRAT-verified").

  The verdicts are very likely right. The certificate claim is not.
- Fix:
  1. Rebuild with line 161 restored. CaDiCaL LRAT has no RAT steps, and the strict build verified all four
     large proofs. Patched sources are in `…/scratchpad/audit/lratfix/`.
  2. Add a negative control to `tests/test_rees_sde_fq_cnf5.py`, and before any batch run: `p cnf 1 1 / 1 0`
     with proof `2 0 0` must give NOT VERIFIED.
  3. Rerun the split runs with the fixed checker (each check takes under 1 s), or use the Kissat + drat-trim path
     already in `gadget_cnf5.py`.
  4. Until then, relabel those claims "CaDiCaL UNSAT; LRAT check void (checker defect, 9 Nov audit)" in the F_q
     note, the handoff entry and STATE.

  I did not check whether upstream drat-trim ships with this line commented out (no network).

## Per item

### Open Directions 1 (`wnest.py` discrepancies): PROBLEM (P2), code OK

- **Code: OK.**
  - `Run.run(qmin_kow=4)` makes WNEST start at q ≥ 4.
  - `kow_round` uses pool q + 1 in the `wnest`/`wnest+` modes, and q + ⌈log₃(q+1)⌉ only in the baseline `kow`
    mode. This matches §2/Theorem A and break §3 items 1-2.
  - `guarantee()` is unchanged, and correctly so: the code was off, not `guarantee()`.
  - The only callers of `qmin_kow` are inside `wnest.py`.
- **Acceptance: OK.**
  - `tables.py` rerun (52 s): output identical to `tables.out` minus its last line.
  - `crosscheck_wnest_fixed.py` rerun: byte-identical. Its 24 "divergences" all have equal `m_used`: 22 are
    an extra logged KOW tuple and 2 are a different valid witness (n = 6 and n = 21, kind 1).
  - The guarantee values match the break report (30, 46, 64, 85, 133, 191 at n = 6, 8, 10, 12, 16, 20).
- **P2.**
  - `wnest.guarantee(8, 10, 12, 14) = 46, 64, 85, 108`. `bound` gives 62.7, 84.2, 108.7, 135.4, which is
    "63, 84, 109, 135" as cited.
  - The wrong "…, 109" appears in five places:
    - `2026-11-08-rees-sde-p3-nest.md` lines 18 and 238;
    - `2026-11-08-rees-sde-p3-nest-break.md` line 135 (where it originated, commit 79d66f19);
    - `MECHANICAL_FOLLOW_UP_PLAN.md` line 99;
    - the run summary line 46.
  - No conclusion changes, since 95 < 108.
  - Fix: 109 → 108 in all five.
- Nits:
  - `tables.out`'s last line ("n in [35,3000) … (line carried over from the 8 Nov run …)") is hand-carried
    and not printed by `tables.py`. Its content is right: the referee's `recursion_ref.out` gives 35 ≤ n < 3000.
    Either make `tables.py` print it or move it to a side note.
  - Break report line 137 says "items 1-3 above are fixed in `wnest.py`". Item 3 was a note fix.
  - Break report line 56, "variant `code` mirrors `wnest.py`", is stale. Variant `proof` now matches.

### Open Directions 2 (k = 4 SAT; (6,2), (7,1)): OK

- `pattern_sat.py` `cadical_solve` and the `solver='cadical'` path are correct. The variable count `cnt[0]` is
  right. The encoding itself is unchanged.
- I regenerated all four CNFs from `pattern_sat.py`. They are byte-identical (sha256) to the leftover `p.cnf`:

  | case | sha256 prefix | variables | clauses |
  |---|---|---|---|
  | 80 patterns | `03b91198…` | 17223 | 501529 |
  | 54 patterns | `a0b76288…` | 12231 | 362767 |
  | 36 patterns | `680550e6…` | 8775 | 266701 |
  | k = 3, 12 patterns | `e99460dd…` | 2925 | 32422 |

- Each proof **re-verified with both fixed builds** (4.7 s, 3.7 s, 45.9 s, 109.8 s). So, despite X1, these UNSAT
  verdicts are now certified.
- The (6,2) and (7,1) figures match `lemma_exhaustive2.out` lines 29-31 and 67 (529 984 + 2 186 bases, total
  1 893 220, 0 failures), which predate the run.
- Note §4/§5 values match `pattern_sat_k4.out`.
- Nit: `cadical_solve` never removes its `mkdtemp` folder. About 8.9 GB is left in
  `/var/folders/y_/k55rjs0x7nb045dsgq61qw000000gn/T/tmp{msctpm82,hphqjqlf3,z7ov42ta,tybp1e89}`. These are
  now the only copies of the four certificates, so either keep them deliberately (record the paths and hashes) or
  delete them. Add cleanup or a `keep` flag.

### Open Directions 3 (p3-nest text per referee): PROBLEM (P5), the rest OK

- **OK:**
  - the dual distance ≥ 2 gloss and the Lemma M parenthetical: variance 4N*/9 is tight; 2N*/9 would need dual
    distance ≥ 3;
  - Remark (b) marked UNPROVED (line 196);
  - the §0 item 1 KOW comparison: n = 64 gives 1433 vs 1536 (sharpened) vs 1651 (KOW (8)); KOW (8) holds for
    9 ≤ n < 3000, integer pieces for 15 ≤ n; the closed form beats KOW's closed form for n > 80 and (8) for
    n > 105. All of these agree with `…-referee/recursion_ref.out`.
- **P5.**
  - §3 table (lines 222-225): row 60 now says "sharpened KOW-type recursion 1359", but rows 90/120/150 still say
    "KOW 2954 / 5156 / 7966".
  - These are `wnest.kow_recursion(90/120/150)`. KOW's own recursion (8) gives 3125 / 5405 / 8285, and 1465 at
    n = 60.
  - The comparison stays true either way (conservative), but the label contradicts the corrected §0.
  - Fix: "sharpened 2954" etc., optionally adding the (8) values. The `tables.out` column header "KOW recursion"
    should also read "sharpened KOW-type recursion" (`tables.py` print).
- Nit: line 56 ("n ≥ 9 for KOW's recursion (8)") and line 295 ("all n ≥ 9") state an unbounded range. The
  referee computed 9 ≤ n < 3000, which line 33 says correctly. Write "9 ≤ n < 3000 [exact]", or add the
  asymptotic argument for larger n.

### Worst Case 1 (U⁺ climb, J ∈ {4, 5}): OK

- `out/climb_uplus_J45.json` and `out/climb_uplus_J5.json` show:
  - 8 591 + 15 609 evaluations;
  - `any_negative_slack: false` and `fails: 0` in both;
  - least `rec_count_U+33` slack 0, with 3 538 banks reaching the branch at J = 4 and 364 at J = 5.
- The "19 saved seed banks": `interesting/` has 24 case-3.3-U⁺ banks with κ = 2 and J ∈ {4, 5}; the `par_kw`
  filter in `load_seeds` reduces them further, consistent with 19.
- Not rerun (cost).

### Worst Case 2 (J = 4, κ = 3 at p = 2 789 427 520 807): control OK; PROBLEMS P3, P6, P8

- `out/bigp_J4k3_1.out` line 134: 131 banks, 0 assertion or check failures, 3 480 back-substitution passes with
  0 failures, 1 `twist` generator failure.
- The prime is in the theorem range: p ≥ 8·3²⁰·10², and p ≡ 1 mod 3.
- Leaves and witnesses are checked by `checker.py`, which uses pure Python ints and shares no code with `la.py`.
  So validity at this prime is checked independently of the new big-int path.
- `la.py` is unchanged by default (`I64 = np.int64` unless `QS_BIGP=1`).
- **P3.** `…-subquad-A-break.md` line 301 is contradicted by `BRANCHES` (line 135):
  - `case33_Uplus: 4` (top-stall design r = 35; `design_top` r = 12, 16, 24);
  - `case30_Uplus: 1`;
  - least `rec_count_U+33` slack 0 (json `summary`).

  What was not reached: `case33_top`, `top_stall_rec`, `case31_W` and `direct_top`. Fix: "The case-3.3 U⁺
  recursion was reached on 4 banks (least slack 0) and case 3.0 U⁺ on 1. The top phase, the top-stall recursion,
  case 3.1 W and ranks above 49 were not reached, so the T_m and top-round asserts were not exercised at this
  prime."
- **P6.**
  - The "identical traces on 22 banks" claim had no saved artifact. I reran `bigp_equiv.py dump` in both builds
    plus `compare`: 22 runs, **0 differences** (scratch `equiv_int64.json`, `equiv_bigp.json`). So the claim
    holds.
  - The 22 banks reach only call, stall, reach_V, case32_leafB, case1_closure, case2_Y and direct_fwd, none of the
    case-3.x branches used at the theorem prime.
  - Fix: save the compare output in `out/`, and add the `interesting/` case-3.3 seed banks (all p < 2³¹) to the
    equivalence set.
- **P8.** No `interesting/` file is newer than 7 Nov 22:43. `harness.py` saves only while fewer than 25 files share
  a branch key. Fix: delete the sentence (run summary line 54).

### Worst Case 3 (KeyError `Ub`; new asserts): asserts OK; PROBLEM P7

- **Asserts: OK and faithful to the note.**
  - Case 2, under `P.strict`: r ≥ q + b; b + (C−1)r + D_J(q) − q ≥ F(b) for C ≥ 2; b + |pool| ≥ F(b).
  - Unconditional: m ≤ J − 2 before `top_phase`; |S| ≤ m + 1 ≤ J − 1 in it. These are valid in stress mode too.
    For m ≥ J − 1 and C ≥ 0, F(r) − F(r−m) ≥ r + 1 > r − 1 ≥ |X′|, so the U⁺ recursion is taken and the top
    phase is never entered.
- **Acceptance (partial rerun):**
  - `run_tests.py heavy 1`: TOTAL identical to `heavy_1.out` (8 banks, `rec:Y` 8).
  - `run_tests.py topbank 1`: TOTAL identical to `topbank_1.out` (36 banks, `top-rounds` 6, `rec:Y` 6).
  - The other nine groups were not rerun by me.
- **P7.** `run_tests.py` lines 78-81 say forward_fast's early "direct" exit happens before any round is realised.
  - In fact `forward_fast` returns "direct" from inside its loop after earlier rounds were appended
    (`subquad.py` line 138). Only "ok" and "stall" set `Ub`.
  - My probe called `planted()` 352 times on mixed shapes (`planted_probe.py`/`.out`): 0 errors, 127 direct exits,
    **87 with realised rounds**. There `Om = []` drops the intended Ω component of the later columns.
  - The banks stay valid inputs (no effect on ALG-T checks), but the family silently changes.
  - Fix: `Om = st["Ub"] if "Ub" in st else rebuild(Fd, st["rounds"])` (`rebuild` is importable from `subquad`),
    and correct the comment.

### 2026-11-09 SDE F_q Referees 1 (fq-nest text): PROBLEMS P1, P4; the rest OK

- **OK:**
  - N(q) ≤ 5q/4 + √(2q) + 7 via N₀ = ⌈5q/4 + √(2q) + 6⌉: I re-derived it.
  - Theorem C: κ = 3 needs p ≡ 1 mod 3; running time poly(a, log p); gain a²/(2p) − O(a log a), positive only
    for a ≫ p log a.
  - Lemma Z garble fixed: allowed nonzero values {−2, −1, 1}; nested and full sets give ≥ p − 1 ≥ 4 values.
    The mathematics is correct.
  - The chain3/chain4 relabel, plus comment-only lines in `adversarial_p5.py`.
- **P1: Lemma R** (lines 115-127).
  - The statement still reads "so is (Φ, γ′) with γ′_{λα} := λγ_α for λ ∈ P and α in a fixed set of
    representatives", and the first proof sentence still argues per α.
  - The appended "wording repair" (referee B finding 3) says this very formula "can make that direction
    degenerate".
  - The lemma therefore asserts what its own proof refutes. Referee B's "Lemma R stands" refers to the reduction
    with per-slot representatives.
  - Fix: restate as "If (Φ, γ) is feasible and weakly nondegenerate, there is a feasible, weakly nondegenerate
    (Φ′, γ′) with γ′_{λβ} = λγ′_β (λ ∈ P) for coset representatives β chosen per (direction, coset) slot, Φ′
    re-normalised at unit directions". Drop or relabel the old one-line proof.
  - The CNF verdicts are unaffected, since the CNF keeps one free γ-slot per coset.
- **P4: Lemma Z label.**
  - §0 item 5 (lines 75-76) still reads "Nothing of lower degree from this framework [proved, Lemma Z]".
  - The closing sentence of (c) ("so the framework gives no polynomial of degree below q − 1 here") sits
    unlabelled after a [proved] lemma.
  - Referee C finding 6, third bullet, says it is [argued], and the plan item named finding 6.
  - Fix: "[argued; Lemma Z proves the four-hyperplane confinement and the infeasibility of nested and full label
    sets]" in §0 item 5, and "[argued]" on the sentence in (c).

### 2026-11-09 SDE F_q Referees 2 (`tests/test_rees_sde_p5_simple.py`): OK

- Passes.
- It execs referee B's `attack_ref.py` up to `t0 = time.time()` (the eight families) and runs n ∈ {3, 4, 6, 9, 12}
  at m = `guarantee_simple(n)`.
- It asserts each witness is nonzero, has entries in {0, 1, 4} (= {0, ±1} mod 5) and sums to zero.
- Nit: the item says "n ≤ 12" and the test samples five values. All of 3..12 would still run in seconds.

### 2026-11-09 SDE F_q Extension 1 (`check_split_cover.py`): OK as specified; X1 applies

- Rerun: OK 3751/3751, 6253/6253, 686/686; `int13_split.out` reported as EMPTY.
- My edited copies (a deleted line, a SAT line) make it FAIL.
- It does not check that all lines of a split file share one (p, S, k, d, L). I checked by hand that they do. Add
  that check.
- The "LRAT VERIFIED" lines it counts come from the defective build (X1). The coverage is exact, but each
  sub-case is a solver verdict until rerun.

### Extension 2 (`tests/test_rees_sde_fq_cnf5.py`): OK as specified; X1 applies

- 2 passed with the original build and with the fixed build; skips without `LRAT_CHECK`.
- It would also pass with a checker that accepts anything. Add the negative control from X1.

### Extension 3 (folder `README.md`): OK

- 8 of 12 `big_*.out` are empty, as stated.
- Nits:
  - The parameters are inferred from file names (`run_big.sh` fixes no naming scheme).
  - The unsplit (7,2) CaDiCaL run (1436 s) has no output file in the folder.
  - Referee C's `free_cnf.py` runs are not listed as further evidence.

### Exponent p^e 1 (`tests/test_rees_exponent_pe_blackbox.py`): OK

Passes: ok == subs and calls_max ≤ cap for 81_3, 243_24 and 625_8. With the two tests above: 6 passed in 12.5 s.

### Square Gap 1 (`e2dfs_k89.out`): OK

Rerun identical.

### Square Gap 2: BLOCKED is justified; nits

- There are 85 primes p ≡ 1 mod 5 in [191, 2628], not "~130" (run summary line 78; plan BLOCKED note).
- `types/orbit_k5_641.out` is 0 bytes, so it records nothing of the cited 7 200 s.

### Square Gap 3: no action, OK. Black-Box Corollary: not audited (DONE before this run)

## Reruns done for this audit

| what | result |
|---|---|
| regenerate the four pattern CNFs; sha256 against the leftover `p.cnf` | 4/4 identical |
| four leftover LRAT proofs, fixed and strict `lrat-check` builds | 4/4 VERIFIED with both |
| checker negative controls (original, fixed, strict builds) | original accepts all four bogus proofs; fixed and strict reject them |
| `tables.py` | identical to `tables.out` minus the annotated last line |
| `crosscheck_wnest_fixed.py` | byte-identical |
| `run_tests.py heavy 1`, `topbank 1` | TOTAL lines identical |
| `bigp_equiv.py` dump ×2 + compare | 22 runs, 0 differences |
| `planted()` probe | 352 calls, 0 errors; 127 direct exits, 87 with realised rounds |
| `pytest` on the three new test files | 6 passed (12.5 s); cnf5 also passes with the fixed checker |
| `check_split_cover.py` (+ negative controls) | OK ×3, EMPTY ×1; controls FAIL |
| `e2dfs.py 8 336`, `9 504` | identical to `e2dfs_k89.out` |

## Not checked

- Not rerun:
  - `climb_uplus.py` and `attack_bigp.py` (717 s);
  - nine of the eleven `run_tests.py` groups;
  - `wnest.py`'s main run (`wnest.out`).
- Not audited:
  - the Black-Box Corollary items;
  - the new "2026-11-09 Rees Square Gap Follow-Up" plan section (another session).
- Not determined: whether upstream drat-trim ships with line 161 commented out.
