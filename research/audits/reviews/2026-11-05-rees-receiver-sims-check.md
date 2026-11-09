# Adversarial check: Rees receiver simulations of 2026-11-05

5 November 2026. AI-only session (Claude Code, Opus 5.5), independent checker and integrator.
Not human review, not Lean. **Everything below is a finite computation or an argument, AI-checked,
pending human review.**

Object: `2026-11-05-rees-receiver-sims.md` and its folder, `theorems/rees_circuit_mono.py`,
`theorems/rees_circuit_exhaustive.py`, `tests/test_rees_circuit_mono.py`,
`tests/test_rees_circuit_exhaustive.py`. Scratch scripts and outputs of this check:
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/`
(`scripts/neg_mono.py`, `scripts/neg_mono2.py`, `scripts/exh_check.py`, `runs/*.out`, `runs/*.json`).
Their results are copied in Sections 3 and 4.

## 0. Verdict

**No Error.** No Gap in the five-line argument (R): it is sound as stated (Section 2). Seven
Imprecisions, all fixed in the paper text (Section 5). The claim gate `coherent_receiver_implemented`
stays false (`research/reductions/rees_hsp_reduction.json` line 35; not touched).

## 1. Code read (claims c, a, b)

**The whole gate list runs on one state [checked by reading].**
- `TerminalSample(cfg)` is built once per job from `cfg` alone. It does not depend on the instance.
- `compile_program` turns every item into a step: perm (flattened X/CX/CCX/SWAP), qft, qft_dg, oracle
  or measure. Any other kind raises `ValueError`, so no item is skipped.
- `run_terminal_sample` executes the steps in order on one `FactorState`. Merging factors is an exact
  tensor product. Splitting off a constant wire is exact. Rows stay distinct basis states, because
  permutation gates and the oracle are bijections, QFT outputs are keyed by (other wires, y) and
  `_select` takes a subset.

**Amplitudes are exact.**
- Z[zeta_p] is stored as p integer coefficients, made canonical by subtracting the last one. The
  remaining p-1 coordinates are coordinates in the basis 1, ..., zeta^(p-2), so a zero test is exact.
- Dividing out the gcd only rescales a factor. The overflow guard is 2^52.
- Floats are used only for the Born weights that choose a trajectory. Every row kept has a nonzero
  amplitude, so any outcome chosen has positive probability.

**"Uniform on h^perp" is checked exactly.**
- The trajectory's readout law is computed as sums of a·conj(a) in Z[zeta_p], with the other wires of
  the factor marginalised. The other factors contribute a common scalar.
- Two tests: the support must equal h^perp (from `inst.log_h`, with m = dim g: 3 resp. 4), and every
  mass must be equal as an element of Z[zeta_p]. A zero first mass can only produce a false failure,
  never a false pass.

**The recoveries are genuine.**
- The circuit reads the instance only through `oracle_table`, f(x) = min index of xH: one oracle call
  per (source, point).
- `log_h` is used only to grade the result (h^perp, and comparing the null space of the samples with
  h). The readout sample is drawn from the exact conditional law.
- Exception, at p = 7 (claim b): the top state is `truth_state`, computed from `log_h` by
  `stage_indices`, not from oracle queries. So the F_7 "recoveries" test the descent from the
  correct source, not recovery from oracle access (Imprecision I1).

**Deferred measurement is valid.**
- A step's non-control set `nc` is defined as:
  - the target of X/CX/CCX, and both wires of a SWAP;
  - the register of a QFT;
  - the output register y of the oracle (w is a control: U_f is block diagonal in w);
  - all readout wires.
- A label is scheduled after its last non-control use (level 2); every other register after its
  last use of any kind (levels 1 and 2). The verifier rechecks that no later step has a scheduled
  wire in `nc`, and at level 1 that no later step touches it at all.
- A computational-basis measurement of R commutes with every later gate that is block diagonal in
  R's basis. Measuring R at the end and ignoring the result leaves the readout marginal unchanged.
  So the joint law of the later outcomes, and in particular the readout law, is unchanged.
- The argument is standard and the schedule is machine-verified. Both test levels report
  `schedule_verified: true`, and so does my run.

**Exhaustive mode [checked by reading].**
- `branch_structure` checks (E1) and (E2) exactly, including the scales (`_row_exponents` compares
  scale·V up to a cyclic shift).
- `subset_checks` enumerates every T ⊆ F_p^* with |T| <= min(M, p-1). It forms
  Sigma_T = {g : delta_t g ∈ supp phi_0 for all t ∈ T} and compares t^(-d) W(delta_t g) across t.
- `SparseEngine.merge` computes F(g) = prod over active i of phi_i(delta_(s_i) g) on exactly that
  support, then descends.

## 2. The five-line argument (R): written out and verified

Fix a grade d, its arity M and its input state rho_(H_d), with branches phi_lam for lam ∈ K^perp
(the support of the label law, by E1). Let b_1..b_k be the rref basis of K^perp. A pair consists of
labels lam_1..lam_M ∈ K^perp and a witness s ∈ F_p^M \ {0} with sum_i s_i^d lam_i = 0. Let
A = {i : s_i ≠ 0} and T = {s_i : i ∈ A}.

1. By (E2), every phi_lam has support Sigma_0 = supp phi_0. phi_0 is constant there, and the code
   also checks that phi_0(e) = 1 (`conditioned` asserts the value at the identity), so phi_0 = 1 on
   Sigma_0. Moreover phi_lam = zeta^(sum_j c_j W_j) phi_0 with lam = sum_j c_j b_j. Writing
   lam_i = sum_j c_ij b_j gives F(g) = prod over i ∈ A of phi_(lam_i)(delta_(s_i) g).
2. F(g) ≠ 0 iff delta_(s_i) g ∈ Sigma_0 for all i ∈ A, that is, iff g ∈ Sigma_T. This depends only on
   T. On Sigma_T, F(g) = zeta^(sum over i ∈ A, sum over j of c_ij W_j(delta_(s_i) g)), and the
   zero-label product F_0 = 1 on Sigma_T, whatever the multiplicities.
3. By (E3), W(delta_t g) = t^d tau(g) on Sigma_T for every t ∈ T, with tau(g) independent of t.
4. So the exponent is sum_j tau_j(g) · sum over i ∈ A of s_i^d c_ij. Since 0^d = 0, the inner sum is
   the b_j coefficient of sum_i s_i^d lam_i = 0, and b is a basis, so it is 0 mod p for every j.
   Hence F = F_0 = 1 on Sigma_T.
5. The merge output (descent and normalisation) is a function of F alone, so it equals the output of
   the zero-label merge with value set T. (E3) checks that output to be rho_(H_(d-1)) for every T.

**Verdict: sound.** It covers every pair of label tuple (any tuple in (K^perp)^M) and nonzero witness,
not only those the solver would return. The count (p^M - 1)|K^perp|^(M-1) is exact because K^perp is
a span (`allowed_labels` returns `span_elements`). For each s ≠ 0 the witness equation is a
surjective linear map, so it has |K^perp|^(M-1) solutions.

Two small corrections to the wording of the report (Imprecision I6):
- Multiplicities change nothing at all, not "only the scale", because phi_0 = 1 on its support.
- The repeated-value variants in (E3) are redundant, which does no harm.

What (R) does not cover. It works in the Schur-product channel of prop:descent: M independent copies
of rho_(H_d), each through the complete central instrument read off its gate list, merged by gate
lists that prove_merge has shown equal to the BCH translation. It says nothing about a gate-level
simulation at class four or five, and it is not machine-checked.

## 3. Re-runs

| run | result |
|---|---|
| new tests (`pytest ... test_rees_circuit_mono.py test_rees_circuit_exhaustive.py`) | **26 passed in 48.8 s** |
| mono Heis(F_3), levels 2 and 1, **seed 4242** (report used 20261105/6), all 19 subgroups | 38/38 runs recovered; 266 trajectories, all exactly uniform on h^perp, workspace clean; schedules verified; 51 s, 0.36 GB |
| mono Heis(F_3) level 0, H = Z, seed 99 | exact output law uniform on h^perp |
| exhaustive n5(F_5) H = <e1> non-normal, **source from its gate list on all 5^11 addresses**, cross-check seed 777 | source: coset state, 9 765 625 equal fibres, left cosets, address restored, workspace clean, equals rho of exp(h~) (139 s). Grades 4, 3, 2: E1, E2, E3 all true. Pairs 1 952 500 / 77 500 / 2.98e17. 60/60 direct merges and 6/6 non-witness controls per grade. Seeded run 777: recovered, 3780 queries. 143 s total, 1.0 GB RSS |
| JSON tallies of the report folder | Heis: 574 samples, 82/82 runs, all uniform and clean; n4(F_5): 7 runs, 56 samples, 2 skipped; n5(F_5): 9/9 passed, 18/18 recovered, prove_merge 12/12; n5(F_7): 8 passed, 16/16 recovered, sampled source checks passed; n6(F_7): 7 passed, prove_merge 24/24 |

## 4. Negative controls (new, this check)

In the table, "bad" means a trajectory whose conditional law is not exactly uniform on h^perp or
whose workspace is dirty. Heis(F_3), level 2.

| corruption | H = <(1,0,0)> non-normal | H = Z = <(0,0,1)> |
|---|---|---|
| none (baseline, seed 99) | 0/10 bad | 0/10 bad; level 0 exact law uniform |
| one oracle entry: f(x0) := f(e), x0 the first index outside H | **8/20 bad** | 0/20, then 1/60 bad (level 0: over budget) |
| same, H = <(1,0,0),(0,0,1)> | | **39/60 bad** |
| drop one CX in bch_merge grade 2 | **10/10** | **10/10**; level 0 fails |
| drop one CCX in bch_merge grade 2 | **10/10** | 3/10 |
| drop one CCX in witness_control grade 2 | **10/10** | **10/10** |
| drop one CCX in sde grade 2 (U only) | 2/10 | 0/10 |
| drop one CCX / CX in the instrument | 5/10 / 6/10 | 3/10 / 1/10 |
| drop one CCX / CX in source_evaluation | **10/10** / **10/10** | 6/10 / **10/10**; level 0 fails |
| replace CX(2, t) by X(t) (bch, witness_control) | 0/10 | 0/10: wire 2 is an arithmetic ancilla that is 1 at that point, so this is not a real mutation |

Exhaustive mode, n5(F_5) and Heis:

| corruption | result |
|---|---|
| one non-identity row of the grade-4 input (H = <e2>) times zeta | fails: phi_0 not constant, zero-label merge ≠ rho, direct merges fail |
| one row of the grade-4 input dropped | fails |
| one instrument exponent entry changed (grade 4) | the merge raises "does not descend" |
| one oracle entry changed, Heis(F_3) source from its gate list | coset_state false (unequal fibres, not cosets) |

Every corruption that is a genuine change is detected somewhere. But the monolithic **readout-law**
test alone is weak for some of them:
- one oracle entry at H = Z (1/60);
- an SDE gate whose control is 0 on the reachable states at H = Z (0/10);
- the report's own `g_sign` example.

So the monolithic runs certify the output law of the correct circuit on the sampled trajectories.
They do not by themselves certify the intermediate states; those rest on the module and coherent
backend checks (Imprecision I3).

## 5. Findings and how the paper text handles them

| # | kind | finding | fix in main.tex |
|---|---|---|---|
| I1 | Imprecision | F_7 and class-five top states are computed from h (`truth_state`), not from oracle queries, so the F_7 "recoveries" test the descent only | Instances: "computed from $\hh$ by linear algebra rather than from oracle queries ... two seeded runs each from that density" |
| I2 | Imprecision | "readout law of every one of 574 samples": at levels 1 and 2 (532 of the 574) it is the conditional law of one sampled trajectory | "conditional readout law of each of 574 simulated terminal samples"; "there it is the exact output law" for level 0 |
| I3 | Imprecision | the readout-law test misses some corruptions (Section 4) | "Only the readout law is tested: some corrupted circuits ... pass on most trajectories, so the intermediate states rest on the module checks above." |
| I4 | Imprecision | the proposed text uses "t^{-d}e(delta_t g)" with e undefined, and no basis | written with $W$, the basis $(b_j)$ of $K_d^\perp$ and $e_\lambda=\sum_jc_jW_j$ |
| I5 | Imprecision | proposed (ii) presents the extension to all pairs as checked | "The extension to all pairs is argued, not machine-checked"; repeated in Scope |
| I6 | Imprecision | (R) wording: multiplicities change nothing (phi_0 = 1), not "only the scale" | report only; no paper impact |
| I7 | Imprecision | the merges are the Schur-product channel, not gate level; at d = 5 prove_merge checks against the right-nested BCH form, not the independent NilGroup formula | "These merges are the Schur-product channel fed by the checked merge gate lists, not a gate-level simulation"; "the grade-five merge gate lists are checked against the right-nested BCH form only" |

Also added:
- "No complete coherent receiver is implemented (see Scope)" in the coherent-label paragraph;
- "finite computation, AI-checked, pending human review" in all three insertions.

## 6. Integration done

- `docs/papers/rees-hsp/main.tex`: three exact-string edits, each with count asserted 1 and the file
  re-read before it. The backup is in the scratchpad at `backup/main.tex.before`.
  - Coherent-label backends: an insertion after the "... all $3^{18}$ basis inputs." sentence.
  - Instances: the three sentences from "The checked merges are ..." to "... are generated and
    counted." are replaced.
  - Scope: an insertion after "Every exact simulation uses the exact Fourier transform;".
  - No \mathsf, \mathrel, \begingroup or \aa.
- Build in `$TMPDIR/rees-build-sims-check`: latexmk exit 0, 160 pages, 0 Overfull, no undefined
  references or citations, no "Float too large". `tests/tools/test_rees_paper_numbers.py`: 2 passed.
  `make_numbers.py` not run.
- `research/REES_FULL_CONTINUATION.md` item 7: what is still lacking.
- Integration log: row I208, directly after I207.
- Not done: no git, no network, `docs/outreach/` untouched, no claim gate touched.

## 7. Claim gates (must stay false)

These stay false:
- `coherent_receiver_implemented`;
- `general_sde_implemented`, `formal_compiler_checked`, `independent_review`, `novelty_established`,
  `speedup_claim_allowed`.

## 8. Next hard question

Machine-check (R): a Lean lemma, or an exhaustive check over F_p-linear label tuples, that phase
linearity plus the subset phase condition imply equality of merges.

Then a level-0 (trajectory-averaged) run at c = 3, which needs a factor of about 10^8 rows, or a
smarter factorisation.

Next command:
`nice -n 10 /opt/anaconda3/bin/python -m theorems.rees_circuit_mono --jobs heis_f3 --levels 0 --max-rows 40000000`
on a quiet machine, capped at about 8 GB. Expected artifact: level-0 rows for more of the 13 small-S
Heis subgroups. Acceptance test: the exact output law is uniform on h^perp.
