# Check of the Rees receiver round 2 (exact law at c = 2, checkpoints, Lean (R), class-five seeded runs)

5 November 2026 (overnight). Independent adversarial check and integration, AI-only (Claude Code, Opus 5.5).
Not human review. Object: `2026-11-05-rees-receiver-round2.md` and its folder; round-2 sections of
`theorems/rees_circuit_mono.py` and `theorems/rees_circuit_exhaustive.py`; `tests/test_rees_circuit_round2.py`;
`formal/Formal/ReesMergeReduction.lean`. Scratch files (scripts, logs, JSON) are in the session scratchpad
`chk/` folder, outside the repository; the results that matter are quoted below.

**Verdict: no Error, no Gap. Three Imprecisions, all fixed in the integrated text.** The paper's
"Gate-level control" section now carries the report's §8 replacements (amended as listed in §6). The gate
`coherent_receiver_implemented` stays false; no claim gate, registry JSON, `Formal.lean`, `Audit.lean`,
`numbers.tex` or `docs/outreach/` was touched. Nothing committed.

## 1. Claim 1: exact output law of the whole Heis(F_3) circuit (finite computation)

Read `HubState` (`split`, `gate`, `_join`, `split_constants`, `gram`, `total_gram`) and `exact_level0_law`.

- **Exact over all branches.** Nothing is measured: steps 0-77 run on the round-1 `FactorState` with no
  `measure`; `HubState.split` only re-indexes the product of factors by the joint values of the hub wires
  (labels and Q). For a product state the hub index is the product of per-factor value digits, and each
  factor keeps exactly its rows with that value, so the split is a change of representation. Every later
  gate is a permutation applied per row: a hub-only gate XORs the hub arrays; a mixed gate localizes a hub
  target and reads hub controls as `hub[w][f.h]`; factors meeting in one gate are joined per hub. The
  law sums over **all pairs (h, h')** with equal classical values off Q (`Gt[~same] = 0`), with the
  factor Gram matrices for the local wires and the phase `zeta^(y·(q_h - q_h'))` of the final QFT_p on Q,
  so the cross terms between branches are kept. Orthogonal branches (different labels, or different
  witness/workspace values) are exactly the ones masked. This is the full output law; by deferred
  measurement (labels used only as controls, oracle outputs and children untouched later) it equals the
  average of the round-1 trajectory laws. Exactness does not depend on `hub_condition`; that condition
  only keeps the children in separate factors.
- JSON (`exact_heis_f3_level0.json`): 19/19 `exact_law_uniform_on_h_perp`, `hub_wires_only_controls`
  true and `hub_joins = 0` for all 19, all checkpoints pass, 6/6 `plain_level0_law_equal`, K3 has 3 entries
  per subgroup (review finding 1 fixed), 38/38 seeded recoveries.
- The uniformity test is real: support equal to h^perp, all masses rational and equal.

## 2. Claim 2: checkpoints and mutants (finite computation)

**References independent of the circuit under test.**
- K1/K2: `child_reference_rdm` builds the coset density from `G.stage_indices(cfg, log_h, 2)` (the span
  of `graded_hidden(cover, log_h)` on the cover) and the instrument formula. Neither the oracle table
  (built in `Hidden.__post_init__` from `law.closure(generators)`) nor any gate list is used.
- K4: the witness is `C.sde_reference` (`canonical_witness_batch`, a separate Gauss-Jordan; the circuit
  never calls it) and the translation is `_witness_bound_g` (a three-line formula `-s^deg q`, used only in
  checkers, never to build gates) composed with `GroupLaw.mul`. K4 is relative to the state at the split,
  as the report says.
- K5: `rho_target` from `stage_indices` at grade 1.
- Shared dependency, stated here for precision: all references and the oracle use the same `GroupLaw`
  class. They are independent of the gate lists and of the oracle table, not of the group-law library.

**Accounting** (`negative_controls_exact.json`): 100 rows; 72 detected, each with a non-empty list of
failed checks (none is caught by the law alone); 28 undetected, all `final_state_identical_to_unmutated`;
24 detected with a uniform law. The 8 `skip_ctrl_inv`/`skip_sde_inv` rows: I recompiled both mutated
`TerminalSample`s and the compiled step lists are identical to the unmutated one (`g_sign` differs, as it
should). So 92 genuine runs, 72 caught, 20 equivalent.

**The 20 equivalent mutants, verified by a different criterion** (my script `equiv_check.py`): run the
**unmutated** circuit up to the dropped gate and test whether all its controls can be 1 together on any
reachable row (per hub, per factor). Result on all four subgroups:

| dropped gate (step, wires, control roles) | controls can fire? H = 1 / <(1,0,0)> / Z / <(1,0,0),Z> |
|---|---|
| source_evaluation cx middle (4, [0,11], ctrl = arith ancilla) | no / no / no / no |
| source_evaluation ccx first (4, [7,11,2], ctrl 7 = arith ancilla) | no / no / no / no |
| witness_control ccx first (155, [7,23,2]) | no / no / no / no |
| bch_merge ccx first (158, [7,37,2]) | no / no / no / no |
| sde_grade2 cx first (78, [134,24], ctrl = label wire) | yes / yes / **no** / **no** |
| sde_grade2 ccx middle (78, [31,33,35]) | yes / yes / **no** / **no** |
| control of the check: sde_grade2 cx middle (caught on all four) | yes / yes / yes / yes |

The "no" cells are exactly the 20 equivalent runs and the "yes" cells exactly the caught ones. So each
equivalent mutant drops a gate that is the identity on the reachable state: 16 are dead gates of the
arithmetic (a control on an ancilla that is 0 there), and 4 have a label-bit control that is 0 on the
restricted label support K^perp of the two subgroups containing Z. These are equivalent on that instance
only (the same gate is caught at H = 1), which the report says ("on that instance").

**Own negative controls** (none in the author's or the first reviewer's set), through `exact_level0_law`:

| control | result |
|---|---|
| oracle of <(1,0,0)>, reference h of <(0,1,0)> (same order, both non-normal) | caught: K1, K2, K5; support != h^perp |
| oracle of <(1,0,0),Z>, reference h of <(0,1,0),Z> | caught: K1, K2, K5; support != h^perp |
| drop middle CCX of the **last** U_SDE^-1 step (324), H = <(1,0,0)> | caught: workspace |
| same, H = Z | all checks pass; final state **identical** to the unmutated one (equivalent) |
| drop last CCX of step 324, H = Z and H = <(1,0,0)> | caught: workspace (law uniform) |

The mismatch controls show that the checkpoints depend on h and not on quantities derived from the
oracle or the circuit. No mutant changed the final state without being caught.

**KS** (`source_coset_check`, `delay_oracle_measurements`): read; the workspace condition (review finding
4) is in place. The trajectory JSONs were not rerun (not needed for the claims checked here; the tests
below cover KS on the dropped-CX mutant and the false-alarm case).

## 3. Claim 3: step (R) in Lean (Lean-checked)

- `cd formal && nice -n 10 lake env lean <copy of the module with #print axioms appended>`: exit 0, no
  warning, about 16 s. `#print axioms` for `merge_product_eq_of_labels`, `merge_product_eq`,
  `exponent_cancels`, `witness_coords`, `zero_product_indicator`: `[propext, Classical.choice, Quot.sound]`
  each. The source contains no `sorry` and no `axiom`.
- **Statement read** (`#check` output): for any commutative ring R, zeta with zeta^p = 1, branches
  `phi : (Fin k -> ZMod p) -> G -> R`, exponents `W : G -> Fin k -> ZMod p`, hypotheses (E2)
  `phi c g = zeta^(sum_j c_j W g j).val * phi 0 g` for all c, g; `phi 0 = 0` off `supp0`; a linearly
  independent basis b; any `s : Fin M -> ZMod p` and coordinates `c : Fin M -> Fin k -> ZMod p` with
  `sum_i s_i^d • sum_j c_ij • b_j = 0`; and (E3) for that s (on {g : delta(s_i) g in supp0 for all
  active i}, `W(delta(s_i) g) = s_i^d * tau g`), the products over {i : s_i != 0} of `phi (c i)` and of
  `phi 0` at `delta (s i) g` are equal for every g. That is what the report states. delta is an arbitrary
  map, so no group structure is assumed (the lemma is purely algebraic, which makes it stronger).
- The hypotheses match the code: (E2) is `branch_structure` (support, `_row_exponents`, e = W·c);
  (E3) is `subset_checks`, run for every value set T with |T| <= min(M, p-1), i.e. every possible value
  set of a witness, with tau_T(g) = t^(-d) W(delta_t g). The hypotheses are satisfiable (phi = 0), so the
  theorem is not vacuous.
- **The link** "merge output is a function of the product": `SparseEngine.merge`
  (`rees_circuit_sparse.py` l. 301-339) forms F(g) = prod over active i of phi_i(delta_(s_i) g) with scales,
  removes gcds into the scale, then descends and normalizes; the output is a function of (F, scale). Read and
  agreed; it stays code reading, as claimed.
- The module is standalone: `Formal.lean` does not import it, `Audit.lean` has no guard for it
  (grep: no match), and it is not in `tab:lean-modules`. The paper now says so.

## 4. Claim 4: n6(F_7) class five (finite computation, seeded)

**Why 3^10 points are complete for a problem over F_7^10.** The equation sum_i s_i^d lambda_i = 0 depends
on s only through u_i = s_i^d, and is linear in u. The map s -> u sends F_p^M onto P^M, P = {x^d : x in
F_p}, with s = 0 iff u = 0 (s_i^d = 0 iff s_i = 0). So the witnesses are exactly the lifts of the nonzero
u in P^M with sum u_i lambda_i = 0; enumerating P^M and lifting each coordinate is complete. |P| = 1 +
(p-1)/gcd(d, p-1): for p = 7, d = 3, gcd = 3 and P = {0, 1, 6} = {0, ±1}, so 3^10 = 59 049 points; d = 2
and d = 4 give |P| = 4 (4^9, 4^5); d = 5 gives |P| = 7 (no gain; the IS solver is used there). The weight
prod_i #{s_i : s_i^d = u_i} (1 for u_i = 0, gcd(d, p-1) otherwise) counts the lifts, so drawing u with it
and then a uniform lift is uniform on all witnesses; the code (`power_class_sde`) does exactly this
(`searchsorted(cumsum(w), r, side="right")` with r uniform in [0, total)). The search is complete, not
efficient: it is |P|^M.

**Checks.** Own spot check: 30 random cases over F_7 (d in {2,3,4}, M <= 6, labels with zero entries),
witness count equal to `all_witnesses` and the drawn s in that set: 30/30. Reran two seeded runs (not the
batch): `<e1>` seed 1 and `<e1+e2+e6>` seed 2: both recovered, solver counts 4500 / 900 / 90 / 10 and
45 000 queries, identical to `seeded_n6_f7.json`; 138 s wall, peak RSS 1.16 GB. The top state is the
exact coset density computed from h, as the report and the paper say.

## 5. Tests

`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10 python -B -m pytest -q -p
no:cacheprovider tests/test_rees_circuit_mono.py tests/test_rees_circuit_exhaustive.py
tests/test_rees_circuit_round2.py`: **46 passed, 1 skipped in 93.84 s** (peak RSS 0.70 GB; the skip is
the REES_SLOW class-five test). `tests/tools/test_rees_paper_numbers.py`: 2 passed.

## 6. Findings

| # | severity | finding | fix |
|---|---|---|---|
| 1 | Imprecision | Edit (i) inserts the exact-law sentences before "Over F_5 the same holds for all 56 terminal samples", so "the same" would read as the exact law over F_5, which is only sampled | one extra exact-string edit: "Over $\mathbb{F}_5$ the conditional readout law is exactly uniform on $\hh^\perp$ for all $56$ terminal samples ..." |
| 2 | Imprecision | Edit (iii) says "from these two checks", but the preceding sentence lists three ((E1) phi_0 constant, (E2), (E3)); and it did not say that `Formal.lean` does not import the module | "from these checks"; the module is called standalone, not imported by `Formal.lean`, not in Table `tab:lean-modules`, not covered by the guard counts of Section `sec:formalization`; status "Lean-checked, standard axioms only; AI-written and AI-checked, pending human review" |
| 3 | Imprecision | Edit (iv): after the new grade-three sentence, "There the grade-five merge gate lists ..." reads as "at grade three"; no report cited for the seeded runs | "At class five the grade-five merge gate lists ..."; report and status added; gamma_4 (7^9 states) named as not run, as for class four |
| - | note | Edit (ii): "the other 20 leave the final state unchanged" | made precise from §2: "in the other 20 the dropped gate never acts on the reachable state, which is left unchanged" |
| - | note | references share the `GroupLaw` class with the oracle generator | stated in §2; not an issue for the claim (independent of gate lists and oracle table) |

## 7. Integration

- `docs/papers/rees-hsp/main.tex` (backup in the scratchpad before editing): the five §8 replacements
  (amended per §6) plus the one disambiguation edit, each an exact-string replacement with count asserted
  1, the file re-read before each edit. No `\mathsf`, `\mathrel`, `\begingroup`, `\aa`. The statuses are
  "finite computation" for (i), (ii), (iv), "Lean-checked" for (iii) and both for (v), each with
  "AI-checked, pending human review". The existing sentence "No complete coherent receiver is implemented
  (see Scope)" follows edit (ii) unchanged, and Scope still says that no generator of the receiver of
  `prop:coherent-receiver` is implemented.
- Build in a scratch copy (`$TMPDIR/rees-build-r2check`, all `*.tex` and `references.bib`):
  `latexmk -g -pdf`: exit 0, 0 Overfull, no LaTeX warning, no undefined reference or citation, no
  "Float too large". `make_numbers.py` not run.
- `research/REES_FULL_CONTINUATION.md` item 7: round 2 recorded as done; "Still lacking" rewritten.
- Integration log: row I212.

## 8. Claim gates

Untouched and false: `coherent_receiver_implemented`, `general_sde_implemented`, `formal_compiler_checked`,
`independent_review`, `novelty_established`, `speedup_claim_allowed`.

## 9. Next hard question

As in the report: the exact output law at c = 3 (n4(F_5)), which needs a hub split over a register while it
is control-only and a coherent re-merge before it is next a QFT target. Separately, making
`ReesMergeReduction` an audited module (import, five guards, table row, counts) needs the owner of
`Formal.lean`/`Audit.lean`, which carry other uncommitted edits.
