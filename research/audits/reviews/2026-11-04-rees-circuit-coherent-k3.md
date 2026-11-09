# Rees HSP: a fifth (coherent-label) circuit backend with a κ = 3 grade, n4(F_7)

4 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
**Status: AI-checked, pending human review.** Labels as in the fourth backend's report
(`2026-11-04-rees-circuit-coherent.md`): **[proved]** = written argument; **[proof-by-computation]**
= exhaustive over ALL inputs of the stated finite set; **[sampled]** = exact on a stated subset
only; **[exact count]** = counted from the emitted program; **[argued]** = reasoning only.

Scope: one instance, the class-three filiform algebra n4 = ⟨e1..e4 | [e1,e2] = e3, [e1,e3] = e4⟩
over F_7. Its graded cover (`rees_circuit_general.Config`) has dims (4, 2, 1). Grade 3 has
κ_3 = gcd(3, 6) = **3** and label dimension g_3 = 1; grade 2 has κ_2 = 2 and g_2 = 2. This is the
smallest instance that the fourth backend refuses (`coherent_config(filiform4(7))` raises).

New files only: `theorems/rees_circuit_coherent_k3.py`, `tests/test_rees_circuit_coherent_k3.py`,
this report, and the folder `research/audits/reviews/2026-11-04-rees-circuit-coherent-k3/`. No
existing file was edited (`rees_circuit_coherent.py` is being edited by another agent and is only
imported). This report was written incrementally; all sections are final.

## 1. What was built

**Reuse, not a copy.** The merge block, the assembled terminal sample, `block_check`,
`sde_exhaustive`, `prove_controlled_merge`, `block_structure`, `assembled_basis_paths`,
`CircuitWitness`, `run_coherent_witness` and the counting code are the fourth backend's
(`theorems/rees_circuit_coherent.py`, read-only import). That code picks its SDE circuit and its
reference witness through three module-level functions, `sde_circuit`, `sde_reference` and
`coherent_arity`, which raise at κ ≥ 3. The new module adds:

- `sde_circuit_k(p, g, d)`: κ ≤ 2 calls the original function (`CoherentSDE` / `CoherentSDEK2`);
  κ ≥ 3 builds `rees_coherent_sde_kappa.CoherentSDEKappa(p, g, d)` (the triangular solver of
  `lem:coherent-power-sde`, canonical contraction, least κ-th root, default stop test of Lemma 4′).
- `sde_reference_k`: κ ≥ 3 uses `canonical_witness_kappa_batch`, the vectorised reference
  written from the definition in the κ = 3 report (independent of the circuit).
- `coherent_arity_k`: g+1 at κ = 1, (g+1)(g+2)/2 at every κ ≥ 2.
- `kappa_dispatch()`: a context manager that replaces exactly those three names in the fourth
  backend's module namespace and always restores them. It is entered only while a block or a
  terminal sample is being built and while a check that reads the reference runs
  (`block_check`, `block_sampled`, `sde_exhaustive`, `assembled_basis_paths` are wrapped). Tests
  check that the originals are back afterwards, also after an exception, that the fourth backend
  still refuses n4(F_7) on its own, and that at κ ≤ 2 (n4(F_5), both grades) the new block
  emits the identical program.
- `MergeBlockK`, `TerminalSampleK`: the fourth backend's classes built under the dispatch, with
  a guard that the emitted program has only `add_product` / `add_scaled` macros (the only kinds
  the fourth backend's `flatten` and `prog_counts` expand; `CoherentSDEKappa` emits its
  comparators as raw X/CX/CCX).
- `state_checks`: the fourth backend's `n4_state_checks` with bounded memory (at p = 7 one dense
  grade-3 state is 823 543 × 7 int64 = 46 MB, and the original caches one factor per
  (label, s), up to 42 of them). It caches merge outcomes by the multiset of active
  (label, s) pairs, which is all the Engine's merge depends on (a product of factors).
- `all_labels_sampled_rest`, `all_q_fixed_labels`, `all_lambda_q_check`, `chunked_block_check`:
  input generators for the bit-level block checks.

**The circuit.** Per merge block at grade d (M = arity): U_SDE writes the canonical witness s(λ)
of the M coherent label registers into S; for each child i the register G = −δ_{s_i}(σ(q)) is
computed, the four-pass BCH right translation x_i ← x_i * G runs with G as a register, G is
uncomputed; U_SDE^{−1} clears S and the SDE workspace. Labels and merged children are garbage
that no later gate touches; the only measurement is the final readout of the root Q. This is the
fourth backend's design (its §1) with the κ = 3 solver at grade 3.

**Arities.** M_3 = (1+1)(1+2)/2 = **3** (the generator's Chevalley–Warning arity κa+1 is 4) and
M_2 = (2+1)(2+2)/2 = **6** (CW arity 5). So a terminal sample has N_3 = 18 top sources, N_2 = 6,
N_1 = 1, and 54 oracle calls, against 20 sources and 60 oracle calls at the CW arities: at this
instance the triangular arity at κ = 3 lowers the grade-3 arity by more than the κ = 2 arity
raises the grade-2 one. The paper's counts (`rem:triangular-scope`) stay at the CW arity and are
not changed here.

**Witness constants at grade 3** (from `kappa_constants(7, 3)`): coset generator g = 2,
h = 2, ω = 4, contraction α = (1, 0, 5), β = (0, 2, 6), Bezout exponent u = 1, one
Adleman–Manders–Miller root at q = 3 with S_3 = 1. U_SDE alone is 135 024 gates on 169 wires
(the κ = 3 report's (7, 1) row).

**Equivalence with the measured version.** Unchanged from the fourth backend's report §2: Lemma 1
(block action) needs only that U_SDE maps |λ⟩|0⟩|0⟩ to |λ⟩|s(λ)⟩|0⟩ on canonical λ with a
footprint off the labels, children and Q, which §3 checks for the κ = 3 circuit inside the
block; Lemma 2 (zero witness entries), Theorem 3 (deferred measurement: tracing out the labels
gives the measured circuit with the same witness rule, averaged over records) and Corollary 4
(ρ_{H_{d−1}} on every Q, conditional on `prop:descent`) do not depend on κ. [proved there;
re-applied here, not re-derived]

## 2. Counts per terminal sample [exact count]

From `TerminalSampleK(cfg).counts()` (depth first, no reuse of garbage, one shared pool for the
clean block workspace). Gate set X/CX/CCX/SWAP of `rees_circuit_arith` with every macro
expanded; QFT_7 counted as calls of the exact 3-qubit unitary (not synthesised); the oracle
U_f excluded (calls listed). Measured-generator rows: `rees_circuit_general.terminal_sample_circuit`
under the same counting backend, all merge slots active; their gate count is the builder's
x/cx/ccx/swap total plus the BCH register swaps it lists separately (486 at the coherent arity,
510 at the CW arity), so that the rows are comparable (the fourth backend's report did the same:
1 234 440 + 360 = 1 234 800 at n4(F_5)).

**n4(F_7)** (p = 7, b = 3, M_3 = 3, M_2 = 6, sources N = (1, 6, 18)):

| component | gates | CCX | macros (product / scaled) | QFT_7 calls |
|---|---|---|---|---|
| sources: E_s compute + uncompute (18 sources) | 372 708 | 92 988 | 0 / 756 | 126 |
| instruments (18 at grade 3, 6 at grade 2), a_top −= z | 14 880 | 3 780 | 0 / 30 | 60 |
| Q preparation (6 grade-2, 1 grade-1) | 0 | 0 | — | 40 |
| coherent SDE grade 3 (**κ = 3**, g = 1, M = 3), 6 blocks | 1 620 288 | 388 560 | 960 / 276 | 0 |
| coherent SDE grade 2 (κ = 2, g = 2, M = 6), 1 block | 938 476 | 224 500 | 596 / 44 | 0 |
| witness control grade 3 (18 children) | 388 656 | 92 232 | 252 / 0 | 0 |
| witness control grade 2 (6 children) | 74 112 | 17 568 | 48 / 0 | 0 |
| BCH merge grade 3 (18 children) | 1 205 082 | 289 872 | 576 / 648 | 0 |
| BCH merge grade 2 (6 children) | 218 604 | 52 704 | 96 / 144 | 0 |
| final Fourier readout | 0 | 0 | — | 4 |
| **total (coherent)** | **4 832 806** | **1 162 204** | 2 528 / 1 898 | **230** |
| measured generator, coherent arities (M_3, M_2) = (3, 6) | 1 812 858 | 440 928 | 672 / 1 578 | 230 |
| measured generator, CW arities (4, 5) | 1 951 830 | 474 780 | 720 / 1 710 | 238 |

Qubits: **1 629** coherent (top addresses 378, oracle outputs 648, grade-3 labels 54, grade-2 Q
108, grade-2 labels 36, root Q 12, evaluation w 12, arithmetic ancillas 14, block workspace pool
367 = the grade-2 block's S 18 + SDE workspace 349; the grade-3 block needs 146 of them), against
**1 322** measured at the coherent arities (+102 classical bits) and 1 418 at the CW arities.
Oracle calls: **54** (60 at the CW arities).

Reading the table.
- The non-SDE, non-control part (sources, instruments, BCH merges) has the measured generator's
  macro sequence at equal arity (672 / 1 578 macros, `test_terminal_sample_counts_and_structure`
  checks totals per component). Its gate count is 1 811 274, 1 584 below the measured
  1 812 858, and the difference is exactly the CCX difference (440 928 − 439 344): as at
  n4(F_5), the coherent merge multiplies by −T and takes s^{deg} from the register G, while the
  measured merge multiplies by the classical constant −T·s^{deg}, and the controlled constant
  loads of `add_product` depend on the bits of the constant.
- The coherent overhead is the SDE circuits plus the witness control: +3 021 532 gates
  (+722 860 CCX), i.e. the coherent sample is ×2.67 the measured gate count at equal arity, with
  +307 qubits. The κ = 3 grade carries most of it: 6 grade-3 blocks of U_SDE + U_SDE^{−1}
  (270 048 gates each) and 18 controlled powers s, s² (21 592 gates per child).
- Against the CW arities the arity change alone saves 138 972 gates, 8 QFT calls, 96 qubits and
  6 oracle calls per terminal sample (fewer top sources), before the coherent overhead.
- Per block (all wires): grade 3 is 535 671 gates on 250 wires (U + U^{−1} 270 048, control
  64 776, BCH 200 847); grade 2 is 1 231 192 gates on 537 wires (938 476 / 74 112 / 218 604).
  The block gate count equals the length of the flattened list (`test_gate_counts_equal_emitted_list`).
- QFT_7 is not synthesised; with an explicit `lem:qft-mod` backend each of the 230 calls would
  add its own per-call cost (not computed here for p = 7).

## 3. Checks and results

Everything below is exact (bit-level permutations, Z[ζ_7] amplitudes, rational probabilities).
Artifacts in `research/audits/reviews/2026-11-04-rees-circuit-coherent-k3/`: `run.json` / `run.log`
(default CLI with `--per-label 1024`), `state_wide.json` / `.log` (wider state checks, §3.4),
`all_lambda_q.json` / `.log` (§3.2, all (λ, q)).

### 3.1 Compositional proof pieces (all pass)

| check | grade 3 (κ = 3, M = 3) | grade 2 (κ = 2, M = 6) | label |
|---|---|---|---|
| U_SDE inside the block (`sde_exhaustive`): S = canonical witness, s ≠ 0, Σ s_i^d λ_i = 0, labels restored, workspace 0 | **all 7^3 = 343 label triples** (135 024 gates) | — (the κ = 2 report samples (7, 2, 2): 8 192 structured inputs) | proof-by-computation / cited |
| controlled merge C_i K_i C_i^{−1} by symbolic replay over F_7[s, q, x] against `sym_bch_reference` (`prove_controlled_merge`): x ↦ x * (−δ_s(σ(q))), G, powers, W, bracket registers 0, s and q unchanged, labels/S/Q never written | proved (82 macros) | proved (48 macros) | proved, given the macro gate lists (proof-by-computation for p ≤ 13, I146) |
| footprints (`block_structure`): U_SDE never writes labels, Q or children; child merge i writes only x_i and merge workspace, reads only x_i, S_i, Q and workspace; merge workspace inside the SDE workspace | yes / yes / 0 wires outside | yes / yes / 0 wires outside | exact |

### 3.2 Merge blocks on all their wires (bit level; a permutation, so basis states suffice)

`block_check` loads labels, children and q (every other wire 0), runs the whole block gate list
(U_SDE, the M controlled merges, U_SDE^{−1}) and asserts: labels and q unchanged; every child
equals x_i * (−δ_{s_i}(σ(q))) with s from the independent reference and * from `GroupLaw.mul`;
the witness register S and every other wire 0; outputs canonical. This is the statement "each
merge gate list equals the BCH right translation with clean scratch".

| block | gates | wires | inputs | result | label |
|---|---|---|---|---|---|
| grade 3 | 535 671 | 250 | **all (λ, q): 343 label triples × all 7^6 q = 40 353 607**, one random child triple per input (`all_lambda_q.json`, 421 s) | pass | proof-by-computation over (λ, q); sampled children |
| grade 3 | 535 671 | 250 | **all 343 label triples × 1 024 random (x_1, x_2, x_3, q) each** = 351 232 | pass | sampled (x, q) |
| grade 3 | 535 671 | 250 | two label triples ((3,5,1), (0,2,4)) × **all 7^6 = 117 649 q**, random children = 235 298 | pass | sampled (λ, x) |
| grade 3 | 535 671 | 250 | 4 096 structured (rank-deficient) | pass | sampled |
| grade 2 | 1 231 192 | 537 | 4 096 structured (rank-deficient label 6-tuples) | pass | sampled |

Mutants detected by `block_check` (tests): the κ = 3 witness circuit with β = (0, 2, 5), with
α = (1, 0, 4), or without the least-root normalisation (`omega_min`); and the block mutants of the
fourth backend at grade 3 (sign of G, no uncompute of G, no U_SDE^{−1}, no first Bennett pass).

### 3.3 The assembled terminal-sample program (wiring)

`assembled_basis_paths` on `TerminalSampleK` (all 18 sources, 24 instruments, 7 merge blocks
with their global wires and the shared pool), 512 random basis paths: each QFT_7 on a fresh
register replaced by a random canonical value, qft_dg, the oracle and the readout skipped; an
independent classical recursion predicts every register (address a ↦ (a z^{−1}) * g(s_i, q),
labels kept, root Q unchanged, w / ancillas / pool / oracle outputs 0). **Pass.** Structure of the
same program: garbage (labels, merged children) never touched after its block, a single
measurement, at the end, of the root Q. This checks wiring, not amplitudes.

### 3.4 Merge outputs equal ρ_{H_{d−1}} (exact Z[ζ_7] states, witnesses from the circuit)

A monolithic or module-by-module amplitude simulation of the whole coherent terminal sample is
out of reach (1 629 qubits; one dense grade-3 state already has 823 543 × 7 integer
coefficients). As at n4(F_5) (fourth report §4.4), `state_checks` uses the measured generator's
exact Engine (dense Z[ζ_7] states; the instrument kernels come from the instrument gate list,
the source from the source gate list) at the coherent arities (3, 6), and takes the witness of
every merge from a **bit-level run of the coherent SDE gate list remapped into the block**
(`CircuitWitness`; κ = 3 circuit at grade 3, κ = 2 circuit at grade 2). By Theorem 3 of the
fourth report the coherent block's reduced output is the π-mixture of the measured outputs with
the same witness rule, so every checked label tuple whose merged output equals ρ_{H_{d−1}} is a
check of the coherent block on that tuple. Each witness is also checked directly (s ≠ 0 and
Σ s_i^d λ_i = 0). The Engine's merge depends only on the multiset of active (label, s) pairs, so
outcomes are cached by it; "distinct merges" counts the Engine calls.

All 9 subgroups of `n4_instances(7)` (5 non-normal; the same list as at n4(F_5)), `run.json`
(grade-2 sample 64) and `state_wide.json` (grade-2 all or 512):

| subgroup | grade-3 label support | grade 3 (M = 3) | grade-2 label support | grade 2 (M = 6) |
|---|---|---|---|---|
| ⟨e2⟩, ⟨e1⟩, ⟨e1+e3⟩ (non-normal), trivial | 7 | **all 7^3 = 343** triples (24 distinct merges) | 49 | 512 sampled of 49^6 = 1.4·10^10 (393–418 distinct merges) |
| ⟨e2,e3⟩ (non-normal) | 7 | **all 343** | 7 | **all 7^6 = 117 649** 6-tuples (54 distinct merges) |
| ⟨e2,e4⟩ (non-normal), Z(G) | 1 | all (1) | 7 | **all 117 649** (54 distinct merges) |
| ⟨e1+e2,e3⟩, γ_2 = ⟨e3,e4⟩ | 1 | all (1) | 1 | all (1) |

Results: every witness valid, every merged output equals ρ_{H_{d−1}} exactly, and the readout
law is uniform on h^⊥, for **9/9** subgroups in both files. Labels: grade 3 and the grade-2 rows
marked "all" are proof-by-computation over all positive-probability label tuples (given the
Engine and `prop:descent`'s semantics of the merge as verified in the generator's reports); the
49-support grade-2 rows are sampled (zero tuple, a constant tuple, then uniform random tuples).
The coherent BCH gate list itself is not used by the Engine; the Engine applies the right
translation that §3.1–3.2 check the gate list against.

### 3.5 Seeded runs from oracle access (`run_coherent_witness`)

Labels sampled from the exact instrument laws, the witness of EVERY merge from the coherent SDE
gate lists, m+4 = 8 terminal samples per run (144 top sources, 432 oracle queries, 48 grade-3
and 8 grade-2 coherent witnesses), nullspace of the readout samples. By deferred measurement this
is the law of the coherent receiver's readout. Six subgroups × seeds 20261103, 20261104:

| subgroup | normal? | recovered log H |
|---|---|---|
| ⟨e2⟩ | no | 2/2 |
| ⟨e1⟩ | no | 2/2 |
| ⟨e1+e3⟩ | no | 2/2 |
| ⟨e2,e4⟩ | no | 2/2 |
| Z(G) | yes | 2/2 |
| trivial | yes | 2/2 |

**12/12** recovered (18–50 s per run).

## 4. What is NOT shown

1. **No amplitude simulation of the whole circuit.** Neither a statevector nor a module-by-module
   exact composition (as the fourth report §4.3 did at Heis(F_3)) of the n4(F_7) terminal
   sample. The amplitude-level evidence is per merge through the Engine (§3.4) plus Theorem 3
   of the fourth report; the assembled program is checked for wiring only (§3.3).
2. **Sampled parts.** The grade-3 block's child registers (all 343 · 7^6 (λ, q) are covered,
   but with one random child triple each, §3.2; there are 7^21 child triples per (λ, q)), the grade-2 block (4 096 structured joint
   inputs), the κ = 2 SDE circuit at (7, 2, 2) (8 192 structured inputs in the κ = 2 report, not
   exhaustive: 7^12 label tuples), and grade-2 label 6-tuples for the four subgroups with label
   support 49 (512 of 1.4·10^10 each).
3. **Reliance on cited results.** The macro gate lists of `rees_circuit_arith` (proof-by-
   computation for p ≤ 13, I146), the κ = 3 circuit's correctness beyond the inputs checked
   here (κ = 3 report), `prop:descent` (Corollary 4), and the fourth report's Lemma 1/Theorem 3.
4. **One instance.** The module is generic in code (any Config with p ∉ E_2(κ_d) at every
   κ_d ≥ 3 grade), but only n4(F_7) is built, counted and checked.
5. **Not covered:** QFT_7 synthesis (230 exact-unitary calls counted, not expanded), the oracle
   cost, noise, depth, layout, padding words in label registers, any asymptotic claim. No
   optimisation (e.g. skipping U_SDE^{−1}, sharing it across blocks).
6. **Mechanism caveat.** The κ = 3 circuit enters the fourth backend's code by a scoped override
   of three module-level functions (§1), not by an interface of that module. If the other
   agent renames them, `kappa_dispatch` raises (it checks they exist) rather than silently
   using the κ ≤ 2 path; `test_k12_delegation_matches_fourth_backend` and the gate-count test
   would also catch drift.
7. **No independent review.** Unlike the fourth and κ = 3 reports, no separate agent reviewed
   this module.

## 5. Claim gates

`research/reductions/rees_hsp_reduction.json` is not edited; `coherent_receiver_implemented` stays
**false** (three finite instances in total across the two backends, not a receiver for general
(G, H)). `STATUS` of the new module: `coherent_receiver_implemented: False`,
`general_instances: False`, `qft_synthesised: False`, `whole_circuit_amplitude_simulation: False`,
`independent_review: False`, `speedup_claim_allowed: False`; only
`coherent_label_backend_kappa3_instance: True`, scoped to n4(F_7). No claim of quantum advantage,
of an asymptotic receiver cost or of a native application follows.

## 6. Proposed sentence for main.tex (not applied; main.tex untouched)

Append to the "Gate-level control" paragraph, after the fourth-backend sentences proposed in
`2026-11-04-rees-circuit-coherent.md` §7:

```latex
A fifth backend, \file{theorems/rees_circuit_coherent_k3.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-coherent-k3.md}; finite computation, AI-checked, pending human review), does the same on the class-three filiform algebra over $\mathbb{F}_7$, whose grade three has $\kappa_3=3$, with the circuit of Lemma~\ref{lem:coherent-power-sde} at grade three and that of Lemma~\ref{lem:coherent-quadratic-sde} at grade two (merge arities $3$ and $6$ instead of $4$ and $5$): one terminal sample uses $1629$ qubits and $4832806$ gates excluding the oracle and $230$ exact transforms, the grade-three merge block equals the right translation by $-\delta_s(\sigma(q))$ with clean workspace on all $7^3\cdot7^6$ pairs of label triple and $q$ (sampled targets) and the grade-two block on samples, and with witnesses computed by the circuit every merged output equals $\rho_{H_{d-1}}$ (all label tuples at grade three, all or sampled at grade two) and seeded runs recover $\log H$ for six hidden subgroups, four of them non-normal.
```

(One sentence. "Sampled targets": one random child triple per (λ, q), §3.2; the exact-state
statement is the Engine check of §3.4, not a simulation of the whole circuit.)

## 7. Files and commands

- `theorems/rees_circuit_coherent_k3.py` (new): `kappa_dispatch`, `sde_circuit_k`,
  `sde_reference_k`, `coherent_arity_k`, `coherent_config_k`, `job_config`, `MergeBlockK`,
  `TerminalSampleK`, wrapped checks (`block_check`, `block_sampled`, `block_exhaustive`,
  `sde_exhaustive`, `assembled_basis_paths`), `all_labels_sampled_rest`, `all_q_fixed_labels`,
  `all_lambda_q_check`, `chunked_block_check`, `state_checks`, `counts_report`, CLI `main`.
- `tests/test_rees_circuit_coherent_k3.py` (new): 20 tests (19 default, about 30 s; 1 more
  with REES_SLOW=1, about 55 s: full-support state check on ⟨e2⟩ with all 343 triples and a
  seeded recovery).
- `research/audits/reviews/2026-11-04-rees-circuit-coherent-k3/`: `run.json`, `run.log`,
  `state_wide.json`, `state_wide.log`, `all_lambda_q.json`, `all_lambda_q.log`.
- This report. No existing file edited; nothing committed or pushed.

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_coherent_k3.py
D=research/audits/reviews/2026-11-04-rees-circuit-coherent-k3
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -u -B -m theorems.rees_circuit_coherent_k3 --per-label 1024 --out $D/run.json   # ~12 min loaded
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -u -B -m theorems.rees_circuit_coherent_k3 --parts state --max-all 117649 --grade2-tuples 512 --state-instances 0,1,2,3,6,7,8 --out $D/state_wide.json   # ~6 min
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -u -B -m theorems.rees_circuit_coherent_k3 --parts none --all-lambda-q --out $D/all_lambda_q.json   # ~8 min
```

Test runs in this session: new file 19 passed, 1 skipped (default) and the slow test passed with
REES_SLOW=1; `tests/test_rees_circuit_coherent.py` 16 passed; `tests/test_rees_coherent_sde_k3.py`
87 passed, 27 skipped.

## 8. Next hard question

Is there a coherent backend for a grade with p ∈ E_2(κ_d), where no universal two-level
contraction exists (smallest: grade 4 of the class-four filiform algebra over F_5, κ_4 = 4)? The
triangular solver does not apply there; Chevalley–Warning or Schedules 1/3 would need coherent
versions. A cheaper next step on this instance: an independent AI review of this module, then a
module-by-module amplitude composition of one grade-3 merge (three sources, three unmeasured
instruments, the block) in the factorised form of the fourth report §4.3, comparing the reduced
state on the grade-2 Q with ρ_{H_2}; acceptance: equality on the four grade-3-support-7
subgroups. Memory is the obstacle (|G_3| = 823 543 per child register).
