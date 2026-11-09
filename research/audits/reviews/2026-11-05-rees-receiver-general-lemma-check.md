# Check of the Rees receiver general lemma (left invariance, per-tuple deferred measurement)

5 November 2026. AI-only adversarial check (Claude Code, Opus 5.5), written by the integrator of
I229. Not human review. Subject: `2026-11-05-rees-receiver-general-lemma.md` (Lemma 1, Corollaries
A_c and B_d, Lemma 2, Theorem 2, Corollary 3, Proposition 4, Section 8). Code read:
`theorems/rees_circuit_coherent.py` (`MergeBlock`, `TerminalSample`, `remap`, `flatten`,
`sde_exhaustive`, `prove_controlled_merge`, `block_structure`), `theorems/rees_circuit_mono.py`
(`compile_program`, `_registers`, `measurement_schedule`), `theorems/rees_circuit_mono_c3.py`
(`setup`, `lemma_hypotheses_check`), `theorems/rees_coherent_sde_k2.py` (`check_circuit`,
`exhaustive_check_chunked`), `theorems/rees_circuit_arith.py` (`Anc`, `add_*_ops`). No git, no
network, `make_numbers.py` not run, no claim gate touched (`coherent_receiver_implemented` stays
false). AI-checked, pending human review.

Scripts and outputs: folder `2026-11-05-rees-receiver-general-lemma-check/` (all run with
`nice -n 19 /opt/anaconda3/bin/python -B`, each < 20 s, < 1 GB).

## Verdict

No Error and no Gap. The weakest link is not in the proofs but in the provenance of (D2a): the
5^12 run predates a later edit of `rees_circuit_arith.py`; see item 5 and the residuals.

| claim | verdict |
|---|---|
| Lemma 1 | accept with rewording: the subspace V must also fix the control registers a segment reads to canonical values (or be any span of basis states invariant under L_g that contains the run); with "other wires arbitrary", (b) is not implied by (D2b), which says nothing for non-canonical S or Q |
| Corollary A_c | accept (it is round 3's Lemma A, already integrated in I225) |
| Corollary B_d | accept with rewording: the stated-label projectors must act outside the traced subtree T, and the support hypothesis of Lemma 1 for each coset term follows from that of the sum (each term is PSD), which the proof should say instead of "by (CLEAN)" alone |
| Lemma 2 | accept |
| Theorem 2 | accept; (D1) re-read from the raw gate payloads (I1 below) |
| Corollary 3 | accept with rewording: exact transforms only; conditional on `lem:central` and `prop:descent`, which are themselves AI-checked, pending human review (the report's Section 7 item 4 calls them "human-written"; this check cannot confirm that and the paper text does not repeat it) |
| Proposition 4 | accept; count confirmed; the link from the exhaustively checked gate list to the assembled program is now checked gate by gate (I2, I3), not only read off `remap` |
| Section 8 (a), (b), (c) | accept with rewording (Section 4) |

## 1. Lemma 1 re-derived

Left and right regular actions of a group commute: L_g R_t |x> = |g x t> = R_t L_g |x>. That is the
whole content. A segment W of type (b) acts on a basis state |x, r> of V as |x u(r), r'(r)>. With
L_g|x, r> = |g x, r> and g x canonical whenever x is, W L_g |x, r> = |g x u(r), r'(r)> =
L_g W |x, r>. Linearity extends this to every state supported in V, and the induction over the
items, followed by L_g^dagger Pi_y L_g = Pi_y for a POVM off X, gives the lemma. Gates of type (a)
commute with L_g as operators.

**What "right translation by values on other wires" requires.** u may depend only on r, the
wires other than X, and r' must not depend on x. Both fail for a gate that reads X as a control
and writes elsewhere. In every application the controls of u are not translated:

- X = a top-source address A or a grade-d node register after its block. Its later history is its
  instrument (u = z^-1 read from the label register, central, so x z^-1 is x minus z in the top
  coordinates) and its own merge segment in the parent's block (u = t(s_i, q) = -delta_(s_i)(sigma(q)),
  with q the **parent** register and s_i the witness register).
- So sigma(q) depends on the parent's register, which is never the register being translated.
  Lemma 1 cannot be applied to the parent register Q during its own block, where the children's
  translations depend on q. The corollaries are stated only after that block (tau after U^-1), and
  `lemma_hypotheses_check` confirms the footprint: after tau, Q is touched only by its instrument
  and its merge as a child.

**Domain.** (D2b) gives the form of the merge segment for canonical (s_i, q, x_i) only, so V must
include "S_i and Q canonical". The proof needs only that V is invariant under L_g (it is: L_g
permutes canonical X and fixes every other wire) and contains the run, which (CLEAN) gives. Hence
the rewording.

**Stress toy** (`lemma1_toy.py`, Gamma = S_3, a 4-level register R, a random entangled mixed state
on X (x) R, two random unitaries on R and two controlled right translations x -> x u(r), readout on
R): the law is invariant under all six L_g (max deviation 5.6e-17). Each violated hypothesis
breaks it: a left-translation segment (deviation 0.12), a segment writing R from X (0.13), a
readout on X (0.14). The report's right-coset toy (`right_cosets_equal_reduced_Q: false`) is
reproduced.

## 2. Corollaries

A_c: re-derived in the round-3 check; unchanged. B_d: rho (x) eta = kappa sum_k L_(g_k) (C'_0 (x) eta)
L_(g_k)^dagger. Each term of a PSD sum supported in V is supported in V, and the run is linear.
So the support hypothesis holds for the C'_0 term, though the report does not say so. Projectors on
labels of the node's own subtree would act on T, which the proof traces out. So B_d covers only
label registers outside the subtree, and that is how it is used.

## 3. Theorem 2, Corollary 3, Proposition 4

**(D1) in the code** (`independent_check.py`, I1). It does not use the `nc` field of
`compile_program`. For each of the 24 label registers, after its `qft_dg`, every later flattened
gate is checked for X/CX/CCX targets (the last qubit), every SWAP, qft, qft_dg, oracle (read and
write registers) and measurement. No label wire occurs in any of them. The only components that read
labels afterwards (as controls) are `sde_grade2` and `sde_grade3`, that is U and U^-1. The macros
emit only x, cx, ccx and swap (`rees_circuit_arith.Ops`), so "last qubit = target" is exact. Lemma 2
then applies item by item, with no restriction to a subspace: U uses labels as controls at the gate
level, not only on clean inputs.

**Theorem 2.** Lemma 2 moves each label measurement to just after its transform. On a branch with
classical lambda, the block is a permutation that is the right translation on every canonical basis
state with clean S and workspace, so it is that permutation on every superposition of them. The
induction over items then matches Mea. Correct. Note that Theorem 2 alone does not need validity of
the witness. Validity enters only in Corollary 3 through `prop:descent`.

**Corollary 3.** Re-derived against the paper. The gate-level instrument is QFT_p on Lambda from
|0>, then x -> x - z, then QFT_p^dagger. Its Kraus operator for outcome lambda is
|Z|^-1 sum_z omega^(-lambda.z) R_z = Pi_lambda of `lem:central` exactly (paper's R_z|x> = |x z^-1>,
chi_lambda(-z) = omega^(-lambda.z)). The merge x -> x * (-delta_s(sigma(q))) is the paper's
R_(delta_s(sigma(q))). Children of one node are independent given all deeper labels, by induction:
each conditional state is rho_(H_(d+1)), whatever the deeper labels. So `prop:descent` applies
branch by branch. Correct, for exact transforms only (labels canonical).

**Proposition 4.** The proof is correct. It needs the SDE workspace to be clean between U and U^-1
so that the merge workspace may live on it. That is (D2a) and the merge's own cleanliness (D2b).
Facts checked:

1. **5^12 count.** `2026-11-04-rees-coherent-sde-k2/exhaustive_p5_a2.json` (cited in the kappa = 2
   report, table row p = 5, a = 2, d = 2, and command line 392). It records inputs 244 140 625 = 5^12,
   M = 6, gates 351 466, qubits 418. All six flags are true: output_equals_canonical,
   inputs_restored, workspace_clean, witness_nonzero, equation_holds, canonical_padding_free. The run
   took 1781.3 s, and the log ends at 244140625 of 244140625, ok. `exhaustive_check_chunked` runs
   `circ.flatten()`, the real X/CX/CCX/SWAP gate list with macros expanded, through `BitSim`. So
   (D2a) at grade 2 is a gate-level computation and does not rest on the macros' declared maps.
2. **Link to the assembled program** (I3). The first half of the root block's `sde_grade2` gates in
   the compiled n4(F_5) terminal sample equals the gate list of `CoherentSDEK2(5, 2, 2)`, gate by
   gate (351 466 each), under one injective wire map psi. psi sends L[c][r] to the label register of
   root child c, row r, and S[c] to the block's S[c]. It sends every other wire of the circuit into
   the arithmetic ancilla and the block-workspace pool. The second half is exactly the reversed
   list. The report's argument ("remap under a wire bijection") was correct, but only read off the
   code; flatten commuting with remap depends on `Anc` being positional, which it is.
3. **Blocks equal the objects that were proved** (I2). For all 7 blocks (root, 984 344 gates; six
   grade-3 blocks, 243 198 each), the assembled gates equal `flatten(blk.prog, p, blk.anc)` under
   one injective wire map phi. phi sends lam, x and Q to the right tree registers and every other
   block wire into ancilla + pool. So `prove_controlled_merge`, `block_structure`, `sde_exhaustive`
   and the renaming check, which all run on the `MergeBlock` object, apply to the assembled program.
4. **Children i > 0.** Child i's segment equals child 0's under S_0 -> S_i, x_0 -> x_i at item level
   (report script, rerun). The map is not a bijection on all wires (S_i -> S_i is kept), but child
   0's segment touches neither S_i nor x_i: `block_structure` checks reads within x_0 ∪ work ∪ S_0 ∪
   Q. So the renaming is a bijection on the segment's support, and the translation property
   transfers.
5. **Drift** (`k2_drift_check.py`). `rees_circuit_arith.py` was modified at 2026-11-04 22:15, after
   the 5^12 run (13:57). The edit recorded for that evening (`2026-11-04-rees-k30-exact-exponents.md`)
   is to `instrument_semantics_arith`, not to `add_*_ops`. The current gate list has the same length,
   351 466, and passes all six flags on 2^20 inputs from index 0, on 2^20 from index 123 456 789, and
   on 16 384 structured inputs (10.7 s). A full re-run of the current gate list (about 233 chunks of
   2^20, roughly 20 to 30 CPU minutes at nice 19) was not done under this pass's 2-minute limit.

**Sanity script** (`general_lemma_check.py`, the report's Appendix A verbatim). Rerun: 2.0 s,
3181 steps. Every flag matches Section 6 of the report: D1 24/24, oracle outputs 36/36, schedule
and lemma checks true, D2c 1 block with 6 children and 6 blocks with 2, block_structure,
prove_controlled_merge, renaming at both grades, and sde_exhaustive at grade 3 (25 inputs, 36 472
gates).

**Attempted breaks.** (i) U modifying labels in place and restoring them: excluded at the gate
level by I1. (ii) U reading children or Q: excluded, since the image of psi and phi on SDE wires
lies in labels + S + ancilla + pool. (iii) A witness that depends on deeper labels or on another
node: U reads only its own children's labels (I2 map). (iv) Non-canonical labels: impossible with
exact transforms. With the explicit transforms of `lem:qft-mod` they are not excluded, and the
report says so (Section 7 item 5). (v) Translating the control register: see Section 1; not an
application of the lemma. No break found.

## 4. Integrated text (`docs/papers/rees-hsp/main.tex`, paragraphs Coherent-label backends and Scope)

Changes from the report's Section 8:

- (b) The file citation moved here, with the check, because (b) comes before (a) in the paragraph.
  Added "on the states reached" (the Lemma 1 domain rewording) and "hand proofs, not
  machine-checked".
- (a) Added "With exact transforms". Added that the conditional law is uniform for every
  positive-probability tuple. "provided the grade-two block" became "provided every merge block",
  since the grade-three blocks are needed too. Grade three is now cited (all 25 label pairs,
  Lemma `lem:coherent-linear-sde`, whose artifact checks (5, 1, 3) exhaustively). Added the checked
  bijection between the exhausted gate lists and the assembled program. The status parenthesis
  moved to (b); (a) says "by a proof plus label-complete finite checks in the report and check
  just cited".
- (c) As proposed, with "output law, and conditional law on every other label tuple".
- New, after "It covers no other coherent-label circuit.": the proof is conditional for the fifth
  backend and for the class-four circuit over F_7 (witness circuit sampled at grade two, and at
  grades three and two in class four; class-four footprints not read off), and no generator of
  coherent receivers for general (G, H) exists.

Each old string occurred exactly once. No new macro, and no `\mathsf`, `\mathrel`, `\begingroup`,
`\aa` or `\ni`. `core/main-core.tex` has no receiver-simulation sentence (grep for label tuple,
symmetry lemma, deferred measurement, coherent-label, rees_circuit_mono) and is not edited.

Build (scratch copy `build_rxg`): exit 0, **178 pages** (baseline 177), 0 Overfull, no undefined
references or citations, no "Float too large". `tests/tools/test_rees_paper_numbers.py`: 2 passed.

**OD3 companion diff.** `patch --dry-run` of `companion/od3-main.diff` applies cleanly to the
pre-edit main.tex. Against the edited copy, hunk 17 (the Scope line, old line 857) fails, and 22 of
23 hunks apply. OD3 changes one phrase on that physical line, "with the query count, arities and
error of Theorem~\ref{thm:main}" to "...of Corollary~\ref{cor:main-is}". This edit changes other
sentences on the same line. The conflict is textual only and is resolved by applying that one
replacement by hand. The Coherent-label backends line (853) is in no OD3 hunk.

## 5. Residuals (gate stays false)

- Full re-run of the current `CoherentSDEK2(5, 2, 2)` gate list on all 5^12 inputs. Command:
  `nice -n 19 /opt/anaconda3/bin/python -B -m theorems.rees_coherent_sde_k2 --chunked 5,2,2 --out <new json>`.
  Acceptance: the six flags all true and K_hist [105390625, 94350000, 44400000].
- n4(F_7) grade 2 (7^12) and class four over F_7: (D2a) sampled only, so the paper states those
  backends as conditional.
- Lemma 1, Lemma 2, Theorem 2, Corollary 3 and Proposition 4 are hand proofs by AI sessions, not
  machine-checked, and so are `lem:central` and `prop:descent` as far as this check knows.

## Addendum (2026-11-05, parent): full 5^12 re-run on the current gate list

The weakest link above (the 5^12 run predated an edit of `rees_circuit_arith.py`) is closed.
Command: `nice -n 19 /opt/anaconda3/bin/python -B -m theorems.rees_coherent_sde_k2 --chunked 5,2,2 --out research/audits/reviews/2026-11-05-rees-receiver-general-lemma-check/exhaustive_p5_a2_rerun_20261105.json`.
Result: 244140625 = 5^12 inputs, 351466 gates, 418 qubits; output_equals_canonical, inputs_restored,
workspace_clean, witness_nonzero, equation_holds, canonical_padding_free all true; 1216.7 s.
The κ = 2 circuit is also now proved correct on every canonical input for every odd p
(`2026-11-05-rees-kappa2-circuit-proof.md`, checked in `-kappa2-circuit-proof-check.md`), so this run is a control.
