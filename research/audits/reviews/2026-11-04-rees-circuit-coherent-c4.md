# Rees HSP: the coherent-label circuit backend on a class-four instance, n5(F_7)

4 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
**Status: AI-checked, pending human review.** Labels as in the fourth and fifth backends' reports
(`2026-11-04-rees-circuit-coherent.md`, `2026-11-04-rees-circuit-coherent-k3.md`):
**[proved]** = written argument; **[proof-by-computation]** = exhaustive over ALL inputs of the
stated finite set; **[sampled]** = exact on a stated subset only; **[exact count]** = counted from
the emitted program; **[argued]** = reasoning only.

This report was written incrementally; all sections are final.

Scope: one instance, the class-four filiform algebra n5 = ⟨e1..e5 | [e1, e_i] = e_{i+1}, i = 2, 3, 4⟩
over F_7. Graded cover dims (5, 3, 2, 1), |G_4| = 7^11, evaluation points (1, 2, 3, 4), m = 5.
Every SDE grade has p = 7 ∉ E_2(κ_d):

| grade d | κ_d = gcd(d, 6) | label dim g_d | coherent SDE circuit | coherent arity (g+1)(g+2)/2 | CW arity κg+1 |
|---|---|---|---|---|---|
| 4 | 2 | 1 | `CoherentSDEK2(7, 1, 4)` (Lemma coherent-quadratic-sde) | **3** | 3 |
| 3 | **3** | 2 | `CoherentSDEKappa(7, 2, 3)` (Lemma coherent-power-sde) | **6** | 7 |
| 2 | 2 | 3 | `CoherentSDEK2(7, 3, 2)` | **10** | 7 |

New files only: `theorems/rees_circuit_coherent_c4.py`, `tests/test_rees_circuit_coherent_c4.py`,
this report and the folder `research/audits/reviews/2026-11-04-rees-circuit-coherent-c4/`. No
existing file was edited; the fifth backend `rees_circuit_coherent_k3.py` (under review by another
agent) and the fourth backend `rees_circuit_coherent.py` are only imported.

## 1. What was built

**No new circuit code was needed.** The fifth backend's scoped dispatch (`kappa_dispatch`,
`MergeBlockK`, `TerminalSampleK`) is generic in the Config: on `coherent_config_k(filiform5(7))` it
builds the three merge blocks and the whole terminal sample with the circuits in the table above.
The new module adds the instance (`config()`, `instances()` = the nine subgroups of
`rees_circuit_sparse.N5_SUBGROUPS` over F_7, five non-normal; corrected 11-04 from "six", see I180), counts, and checks sized for class
four:

- `sde_check(block, lam)`: U_SDE remapped inside the block, alone, on any label tuples (chunked;
  the fourth backend's `sde_exhaustive` forms all p^{Mg} tuples, which at grade 3 is 7^12).
- `rank_le1_tuples(p, g, M)`: all label tuples spanning a space of dimension ≤ 1
  (1 + (p^g − 1)/(p − 1) · (p^M − 1); 941 185 at grade 3); `random_rank_le1_tuples` for grade 2.
- `block_check_labels`: the fourth backend's whole-block `block_check` (through the fifth
  backend's dispatch wrapper) with one random (x_1..x_M, q) per label tuple.
- `block_mutants`, `assembled_mutants`: mutants that must be rejected (§3.5).
- `source_exact_check`: an exact check of the top source that does not enumerate G_4 (§3.6).
- `SourceFromKernel(SparseEngine)`: the sparse exact engine of `rees_circuit_sparse` (states on
  their support only), with the top source set to the coset state of the identity fibre that
  `source_exact_check` computes, instead of evaluating the source gate list on all 7^11 addresses.
- `state_checks`, `run_seeded`: per-merge exact checks and seeded runs on that engine, with the
  witness of every merge computed by a bit-level run of the coherent SDE gate list (`CircuitWitness`).

**The circuit** is the fourth backend's design (its §1) with the κ = 3 circuit at grade 3: per merge
block at grade d (M = arity), U_SDE writes the canonical witness s(λ) of the M coherent label
registers into S; for each child i the register G = −δ_{s_i}(σ(q)) is computed, the four-pass BCH
right translation x_i ← x_i * G of class d runs with G as a register, G is uncomputed; U_SDE^{−1}
clears S and the SDE workspace. Labels and merged children are garbage that no later gate touches;
the only measurement is the final readout of the root Q. Lemma 1 / Theorem 3 / Corollary 4 of the
fourth report (block action, deferred measurement, ρ_{H_{d−1}} on every Q conditional on
`prop:descent`) do not depend on the class or on κ. [proved there; re-applied here, not re-derived]

## 2. Counts per terminal sample [exact count]

From `TerminalSampleK(config()).counts()` (depth first, no reuse of garbage, one shared pool for the
clean block workspace), artifact `run.json`. Gate set X/CX/CCX/SWAP of `rees_circuit_arith` with
every macro expanded; QFT_7 counted as calls of the exact 3-qubit unitary (not synthesised); the
oracle U_f excluded (calls listed). Measured-generator rows: `rees_circuit_general.terminal_sample_circuit`
under the same counting backend (`C.measured_counts`), all merge slots active; their gate count is the
builder's x/cx/ccx/swap total plus the BCH register swaps it lists separately (7 980 at the coherent
arities, 6 489 at the CW arities), as in the fourth and fifth reports.

**n5(F_7)** (p = 7, b = 3, (M_4, M_3, M_2) = (3, 6, 10), sources N = (N_1, N_2, N_3, N_4) = (1, 10, 60, 180)):

| component | gates | CCX | macros (product / scaled) | QFT_7 calls |
|---|---|---|---|---|
| sources: E_s compute + uncompute (180 sources, 4 points) | 7 809 120 | 1 948 320 | 0 / 15 840 | 1 980 |
| instruments (180 + 60 + 10), a_top −= z | 163 680 | 41 580 | 0 / 330 | 660 |
| Q preparation (60 grade-3, 10 grade-2, 1 grade-1) | 0 | 0 | — | 685 |
| coherent SDE grade 4 (κ = 2, g = 1, M = 3), 60 blocks | 21 294 480 | 5 097 360 | 13 440 / 1 320 | 0 |
| coherent SDE grade 3 (**κ = 3**, g = 2, M = 6), 10 blocks | 8 054 520 | 1 928 680 | 4 920 / 920 | 0 |
| coherent SDE grade 2 (κ = 2, g = 3, M = 10), 1 block | 2 043 940 | 488 572 | 1 304 / 72 | 0 |
| witness control grade 4 (180 children) | 6 661 440 | 1 581 120 | 4 320 / 0 | 0 |
| witness control grade 3 (60 children) | 1 666 080 | 395 280 | 1 080 / 0 | 0 |
| witness control grade 2 (10 children) | 154 400 | 36 600 | 100 / 0 | 0 |
| BCH merge grade 4 (180 children) | 28 354 140 | 6 809 400 | 14 400 / 12 600 | 0 |
| BCH merge grade 3 (60 children) | 6 763 920 | 1 625 400 | 3 360 / 3 240 | 0 |
| BCH merge grade 2 (10 children) | 526 820 | 126 900 | 240 / 320 | 0 |
| final Fourier readout | 0 | 0 | — | 5 |
| **total (coherent)** | **83 492 540** | **20 079 212** | 43 164 / 34 642 | **3 330** |
| measured generator, coherent arities (3, 6, 10) | 43 645 640 | 10 579 560 | 18 000 / 32 330 | 3 330 |
| measured generator, CW arities (3, 7, 7) | 35 580 671 | 8 624 658 | 14 672 / 26 362 | 2 705 |

Qubits: **20 566** coherent (top addresses 5 940, oracle outputs 10 800, labels 540 / 360 / 90 at
grades 4 / 3 / 2, Q registers 1 800 / 240 / 15 at grades 3 / 2 / 1, evaluation w 15, arithmetic
ancillas 14, block workspace pool 752 = the grade-2 block's workspace: S 30 + SDE workspace 722;
the grade-4 and grade-3 blocks need 146 and 362 of it), against **19 979** measured at the coherent
arities (+1 005 classical bits) and **16 316** at the CW arities. The paper's 16 302 is the CW-arity
generator with the original arithmetic; the poly(log p) backend adds its 3b+5 = 14 ancillas
(16 316 = 16 302 + 14; `test_measured_generator_counts`). Oracle calls: **720** (588 at the CW arities).

Reading the table.
- The non-SDE, non-control part (sources, instruments, BCH merges) is 43 617 680 gates, 27 960 below
  the measured 43 645 640 at equal arity, and the difference is exactly the CCX difference
  (10 579 560 − 10 551 600): as at n4(F_5) and n4(F_7), the coherent merge multiplies by −T and takes
  s^{deg} from the register G, while the measured merge multiplies by the classical constant
  −T·s^{deg}, and the controlled constant loads of `add_product` depend on the constant's bits.
- The coherent overhead is the SDE circuits plus the witness control: +39 874 860 gates
  (+9 527 612 CCX), so the coherent sample is ×1.91 the measured gate count at equal arity, with
  +587 qubits. Grade 4 carries most of it (60 blocks: U_SDE + U_SDE^{−1} = 354 908 gates each,
  and 180 children at 37 008 gates each for the powers s², s³, s⁴ and G = −δ_s(σ(q))), then the κ = 3 grade
  (10 blocks of 805 452).
- Against the CW arities the arity change (M_3: 7 → 6, M_2: 7 → 10) costs, before the coherent
  overhead, +8 064 969 gates, +625 QFT calls, +132 oracle calls and +3 663 qubits per terminal
  sample (180 instead of 147 top sources): unlike n4(F_7), the κ = 2 arity at g_2 = 3 (10 against 7)
  outweighs the κ = 3 saving at g_3 = 2 (6 against 7). The paper's counts (`rem:triangular-scope`)
  stay at the CW arity and are not changed here.
- Per block (all wires): grade 4 is 938 501 gates on 298 wires (U + U^{−1} 354 908, control 111 024,
  BCH 472 569); grade 3 is 1 648 452 gates on 616 wires (805 452 / 166 608 / 676 392; U_SDE alone is
  402 726 gates, the κ = 3 report's (7, 2) circuit); grade 2 is 2 725 160 gates on 1 111 wires
  (2 043 940 / 154 400 / 526 820). The block gate count equals the length of the flattened list
  (`test_gate_counts_equal_emitted_list`), and every component total is N_{d−1} times the block's
  segment (`test_terminal_sample_counts_and_structure`).
- QFT_7 is not synthesised; with an explicit `lem:qft-mod` backend each of the 3 330 calls would add
  its own cost (not computed here).

## 3. Checks and results

Everything below is exact (bit-level permutations, Z[ζ_7] amplitudes, rational probabilities).
Artifacts in `research/audits/reviews/2026-11-04-rees-circuit-coherent-c4/`: `run.json` / `run.log`
(§2, §3.1–3.5: counts, macros, proofs, SDE, blocks, mutants; 136 s), `rref_paths.json` / `.log`
(§3.2 row spaces, §3.4 wiring), `state_runs.json` / `.log` (§3.6–3.8).

### 3.1 Compositional proof pieces (all pass)

| check | grade 4 (κ = 2, M = 3) | grade 3 (κ = 3, M = 6) | grade 2 (κ = 2, M = 10) | label |
|---|---|---|---|---|
| every macro gate list the blocks use (add_product ×1, 2, 6; add_scaled ×1, 2, 3, 4, 6): `exhaustive_macro_check(7)`, all 6 coefficients of both kinds, all 2^{kb} words (64 / 512), declared F_7 map on canonical inputs, padding fixed, bijective, ancillas clean, operands never targeted | yes | yes | yes | proof-by-computation |
| controlled merge C_i K_i C_i^{−1} by symbolic replay over F_7[s, q, x] against `sym_bch_reference` (class-d BCH polynomial): x ↦ x * (−δ_s(σ(q))), G, powers, W and bracket registers 0, s and q unchanged, labels / S / Q never written | proved (174 macros) | proved (128 macros) | proved (66 macros) | proved, given the macro gate lists (row above) |
| footprints (`block_structure`): U_SDE never writes labels, Q or children; child merge i writes only x_i and merge workspace, reads only x_i, S_i, Q and workspace; merge workspace inside the SDE workspace | yes / yes / 0 wires outside | yes / yes / 0 | yes / yes / 0 | exact |

### 3.2 U_SDE inside the block (`sde_check`: S = canonical witness of the independent reference, s ≠ 0, Σ s_i^d λ_i = 0, labels restored, every other wire 0)

| grade | circuit (gates) | inputs | result | label |
|---|---|---|---|---|
| 4 | `CoherentSDEK2(7, 1, 4)` (177 454) | **all 7^3 = 343 label triples** | pass | proof-by-computation |
| 3 | `CoherentSDEKappa(7, 2, 3)` (402 726) | **all 941 185 rank ≤ 1 label 6-tuples** | pass | proof-by-computation on that set |
| 3 | same | **one representative per row space (all 6 884 860 row spaces of dimension ≤ 2 of F_7^6)**, inside the block | **pass** (46 s) | proof-by-computation on the representatives |
| 3 | same | 4 194 304 uniform random + 16 384 structured | pass | sampled |
| 2 | `CoherentSDEK2(7, 3, 2)` (1 021 970) | 1 048 576 uniform random + 16 384 structured + 16 384 random rank-1 | pass | sampled |

The grade-3 rows cover the definition on every input via Lemma 5 of the κ = 3 report (the canonical
witness depends only on the row space of the g × M label matrix), but the circuit is checked only
on the representatives, the rank ≤ 1 set and the samples; it is not proved row-space invariant, so
the 7^12 ≈ 1.4·10^10 grade-3 inputs are not all covered. The κ = 3 report ran the same representatives
on the standalone circuit; here they are run on the circuit remapped into the merge block.

### 3.3 Merge blocks on all their wires (`block_check`, bit level; a permutation, so basis states suffice)

`block_check` loads labels, children and q (every other wire 0), runs the whole block gate list
(U_SDE, the M controlled merges, U_SDE^{−1}) and asserts: labels and q unchanged; every child equals
x_i * (−δ_{s_i}(σ(q))) with s from the independent reference and * from `GroupLaw.mul` (class-d BCH);
the witness register S and every other wire 0; outputs canonical. This is the statement "each merge
gate list equals the BCH right translation with clean scratch", on the inputs listed.

| block | gates | wires | inputs | result | label |
|---|---|---|---|---|---|
| grade 4 | 938 501 | 298 | **all 343 label triples × 4 096 random (x_1, x_2, x_3, q)** = 1 404 928 | pass | all λ; sampled (x, q) |
| grade 3 | 1 648 452 | 616 | **all 941 185 rank ≤ 1 label 6-tuples**, one random (x, q) each | pass | all rank ≤ 1 λ; sampled (x, q) |
| grade 3 | 1 648 452 | 616 | **one representative per row space (6 884 860)**, one random (x, q) each | **pass** (221 s) | representatives; sampled (x, q) |
| grade 3 | 1 648 452 | 616 | 262 144 uniform random + 4 096 structured | pass | sampled |
| grade 2 | 2 725 160 | 1 111 | 65 536 uniform random + 4 096 structured (rank-deficient) | pass | sampled |

All (λ, q) at grade 4 (343 · 7^10 ≈ 9.7·10^10 inputs) was not run: about 20 days at this
simulator's measured rate (~55 000 inputs/s on this block).

### 3.4 The assembled terminal-sample program (wiring)

`assembled_basis_paths` (fourth backend, through the fifth backend's dispatch) on
`TerminalSampleK(config())`: all 180 sources, 250 instruments, 71 merge blocks with their global
wires and the shared pool, 83 492 540 gates, 512 random basis paths (`rref_paths.json`, 62 s). Each
QFT_7 on a fresh register is replaced by a random canonical value; qft_dg, the oracle and the readout
are skipped; an independent classical recursion predicts every register (address a ↦ (a z^{−1}) *
g(s_i, q) with s the canonical witness of the sibling labels, labels kept, root Q unchanged, w /
ancillas / pool / oracle outputs 0). **Pass.** Structure of the same program (`ts.structure()`):
garbage (labels, merged children) is never touched after its block; there is a single
measurement, at the end, of the root Q. This checks wiring, not amplitudes.

**3.4a Mutants of the assembled program.** The same check with one instrument macro removed, and
with the last grade-4 G-uncompute macro removed: both **rejected** (64 paths each).

### 3.5 Mutants (all rejected; `block_mutants`, `assembled_mutants`, tests)

| mutant | detected by |
|---|---|
| grade-4 block: sign of G flipped (`g_sign`) | block_check |
| grade-4 block: G not uncomputed (`skip_ctrl_inv`) | block_check (workspace) |
| grade-4 block: no U_SDE^{−1} (`skip_sde_inv`) | block_check (S, workspace) |
| grade-4 block: first Bennett pass missing (`skip_bennett`) | block_check |
| grade-3 κ = 3 circuit with β = (0, 2, 5) (true (0, 2, 6)) | sde_check and block_check |
| grade-3 κ = 3 circuit with α = (1, 0, 4) (true (1, 0, 5)) | sde_check and block_check |
| grade-3 κ = 3 circuit without the least-root normalisation (`omega_min`) | sde_check and block_check |
| grade-4 block with the wrong-degree witness (the κ = 2 circuit for d = 2, i.e. Σ s_i² λ_i = 0) | block_check on all 343 triples |
| assembled sample with one instrument macro removed | assembled_basis_paths (§3.4a) |
| assembled sample with one grade-4 G-uncompute macro removed | assembled_basis_paths (§3.4a) |

### 3.6 The top source without enumerating G_4 (`source_exact_check`; all 9 subgroups pass)

The fourth and fifth backends evaluate the source gate list on every address of G_c. At |G_4| = 7^11
≈ 2·10^9 that is not feasible here (the sparse engine's key array alone would be 16 GB). Instead:

1. **Evaluation program [proof-by-computation over all a, given the macro lists of §3.1].** The
   first top source's items (QFT_7 on 11 address registers, 4 × (compute E_s, oracle, uncompute))
   are replayed with linear forms over the 11 address coordinates: at the k-th oracle call the
   register w holds exactly a E_{s_k} (s_k = 1, 2, 3, 4) as a linear map of a, the oracle item reads
   w (in the generator's order) and writes the k-th output register of that source, and w is 0 after
   the last uncompute. Every source is emitted by the same code with its own registers; only the
   first is replayed (the wiring of all 180 is in §3.4).
2. **Identity fibre [exact linear algebra].** f has the left cosets of H as fibres (oracle table =
   least index of xH); E_s is linear in exponential coordinates; so a and b have the same joint key
   (f(a E_s))_s iff a^{−1} b lies in S = {a : a E_s n = 0 for all s and all n ∈ h^⊥}, given (3).
   S is computed by a nullspace over F_7 and equals exp(h~) = `stage_indices(cfg, log h, 4)` for all
   nine subgroups (dimensions 0, 1, 1, 2, 4, 5, 1, 7, 9).
3. **Homomorphism [sampled].** E_s(x * y) = E_s(x) * E_s(y) (class-4 BCH on G_4 and on G) on 4 096
   random pairs per point. This is the cover lemma of the paper; it is only sampled here.

Given 1–3, the reduced state of a source address register is 1_S/|G_4| on S (fibres are the left
cosets of S), and `SourceFromKernel` starts the exact engine from that state. [argued from 1–3; the
source is NOT evaluated from its gate list on all addresses]

### 3.7 Merge outputs equal ρ_{H_{d−1}} (exact Z[ζ_7] states on their support, witnesses from the circuit)

Engine: `rees_circuit_sparse.SparseEngine` (states stored on their support; its instrument kernels
are read off the generator's instrument gate list, which equals the coherent backend's `add_scaled`
macro on canonical inputs, `equals_old_on_canonical` in §3.1), with the source of §3.6. The witness
of every merge is the output of a **bit-level run of the coherent SDE gate list remapped into the
block** (`CircuitWitness`: CoherentSDEK2 at grades 4 and 2, CoherentSDEKappa at grade 3), and each
witness is also checked directly (s ≠ 0, Σ s_i^d λ_i = 0). By Theorem 3 of the fourth report the
coherent block's reduced output is the mixture of the measured outputs with the same witness rule,
so every checked label tuple whose merged output equals ρ_{H_{d−1}} is a check of the coherent block
on that tuple. The next grade starts from ρ_{H_{d−1}}. Merges are cached by the multiset of active
(label, s) pairs ("distinct merges" counts engine calls).

`state_wide.json` (all-tuple threshold 117 649, else 1 024 sampled tuples: the zero tuple, a constant
tuple, uniform random ones), 8 of the 9 subgroups, 53 s:

| subgroup | normal? | |S| | grade 4 (M = 3): labels, tuples | grade 3 (M = 6): labels, tuples | grade 2 (M = 10): labels, tuples |
|---|---|---|---|---|---|
| trivial | yes | 1 | 7, **all 343** | 49, 1 024 sampled | 343, 1 024 sampled |
| ⟨e1⟩ | no | 7 | 7, **all 343** | 49, 1 024 sampled | 343, 1 024 sampled |
| ⟨e2⟩ | no | 7 | 7, **all 343** | 49, 1 024 sampled | 343, 1 024 sampled |
| ⟨e3⟩ | no | 49 | 7, **all 343** | 49, 1 024 sampled | 49, 1 024 sampled |
| Z(G) = ⟨e5⟩ | yes | 2 401 | 1, all (1) | 7, **all 7^6 = 117 649** (24 distinct merges) | 49, 1 024 sampled |
| ⟨e2, e5⟩ | no | 16 807 | 1, all (1) | 7, **all 117 649** (24 distinct merges) | 49, 1 024 sampled |
| ⟨e1+e2+e5⟩ | no | 7 | 7, **all 343** | 49, 1 024 sampled | 343, 1 024 sampled |
| γ_3 = ⟨e4, e5⟩ | yes | 823 543 | 1, all (1) | 1, all (1) | 7, 1 024 sampled of 7^10 |

Results: every label law uniform on its support (which is K_d^⊥), every witness valid, every merged
output equal to ρ_{H_{d−1}} exactly, and the readout law uniform on h^⊥, for **8/8** subgroups (also
in `state_runs.json` with 64 sampled tuples). Rows marked "all" are proof-by-computation over all
positive-probability label tuples of that merge (given the engine and `prop:descent`'s semantics of
the merge, as verified in the generator's reports); the others are sampled.

**Not run: γ_2 = ⟨e3, e4, e5⟩** (|S| = 7^9 = 40 353 607; after the grade-4 instrument the conditioned
state has 7^10 rows of 7 integers, about 16 GB). Its source check (§3.6) passes.

### 3.8 Seeded runs from oracle access (`run_seeded`)

Labels sampled from the exact label laws, the witness of EVERY merge from the coherent SDE gate lists,
m+4 = 9 terminal samples per run (1 620 top sources, 6 480 oracle queries, 540 grade-4, 90 grade-3 and
9 grade-2 coherent witnesses), breadth first (same law as depth first: all sources are independent),
nullspace of the readout samples. By deferred measurement this is the law of the coherent receiver's
readout, with the source of §3.6. Eight subgroups × seeds 20261103, 20261104 (`state_runs.json`):
trivial, ⟨e1⟩, ⟨e2⟩, ⟨e3⟩, Z(G), ⟨e2, e5⟩, ⟨e1+e2+e5⟩, γ_3: **16/16** recovered log H (0.4–46 s per run;
five of the eight subgroups are non-normal).

## 4. What is NOT shown

1. **No amplitude simulation of the whole circuit** (20 566 qubits), and no module-by-module amplitude
   composition of a terminal sample as at Heis(F_3). Amplitude-level evidence is per merge through the
   sparse engine (§3.7) plus Theorem 3 of the fourth report; the assembled program is checked for
   wiring only (§3.4).
2. **The source is not evaluated from its gate list on all 7^11 addresses.** It is checked by the
   symbolic replay of the evaluation program, a linear-algebra identity-fibre computation and a
   sampled homomorphism check (§3.6); the state checks and runs start from the resulting coset state.
3. **Sampled parts.** The (x, q) registers of every block (no block is run on all its basis inputs:
   grade 4 alone has 343 · 7^43 joint inputs); grade-3 label tuples outside the rank ≤ 1 set and the
   row-space representatives (the circuit is not proved row-space invariant); grade-2 label 10-tuples
   (sampled only, at the SDE and the block level, out of 7^30); sampled label tuples in §3.7 at grade 3
   (support 49) and grade 2; the homomorphism of §3.6.
4. **One subgroup not state-checked:** γ_2 (memory, §3.7); one seeded run per seed for 8 of 9 subgroups.
5. **Reliance on cited results.** `prop:descent` (Corollary 4 of the fourth report), the fourth
   report's Lemma 1 / Theorem 3, the κ = 3 report's Lemma 5 (only to say what the representatives
   cover), the sparse engine's equivalence with the dense one (checked in its own report at smaller
   instances), the cover lemma (sampled here).
6. **Not covered:** QFT_7 synthesis (3 330 exact-unitary calls counted, not expanded), the oracle cost,
   noise, depth, layout, padding words in label registers, any optimisation (e.g. sharing U_SDE^{−1}),
   any asymptotic claim, other instances. Grades with p ∈ E_2(κ_d) (e.g. this algebra over F_5,
   κ_4 = 4) have no coherent circuit here.
7. **Mechanism caveat.** The circuit enters through the fifth backend's scoped override of three
   module-level functions of the fourth backend; `block_mutants` itself patches the fifth backend's
   `sde_circuit_k` for one mutant and restores it in a `finally` block (tests check the fourth
   backend's functions are restored). If the fifth backend changes under its current review, the
   count and wiring tests here would catch drift.
8. **No independent review** of this module.

## 5. Claim gates

`research/reductions/rees_hsp_reduction.json` is not edited; `coherent_receiver_implemented` stays
**false** (four finite instances across the three coherent backends, not a receiver for general (G, H)).
`STATUS` of the new module: `coherent_receiver_implemented`, `general_instances`, `qft_synthesised`,
`whole_circuit_amplitude_simulation`, `source_from_gate_list_on_all_addresses`, `independent_review`,
`speedup_claim_allowed` all **False**; only `coherent_label_backend_class_four_instance: True`, scoped
to n5(F_7). No claim of quantum advantage, of an asymptotic receiver cost or of a native application follows.

## 6. Proposed sentence for main.tex (not applied; main.tex untouched)

To replace "The class-four circuits over $\mathbb{F}_7$ ($16302$ qubits per terminal sample) are
generated and counted but not simulated." in the "Gate-level control" paragraph:

```latex
The class-four circuits over $\mathbb{F}_7$ ($16302$ qubits per terminal sample) are generated and counted; a coherent-label version, \file{theorems/rees_circuit_coherent_c4.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-coherent-c4.md}; finite computation, AI-checked, pending human review), uses the circuits of Lemmas~\ref{lem:coherent-quadratic-sde} and~\ref{lem:coherent-power-sde} at grades four, three and two ($\kappa_d = 2, 3, 2$; merge arities $3$, $6$ and $10$ instead of $3$, $7$ and $7$), so that one terminal sample uses $20566$ qubits and $83492540$ gates excluding the oracle and $3330$ exact transforms; its merge blocks equal the right translation by $-\delta_s(\sigma(q))$ with clean workspace on all label triples at grade four and all rank-at-most-one label tuples and one tuple per row space at grade three (sampled targets and $q$), and on samples at grade two, and with the source state computed from the evaluation program by linear algebra rather than simulated, witnesses computed by the circuit give merged outputs equal to $\rho_{H_{d-1}}$ for eight of the nine hidden subgroups (all label tuples at grade four, all or sampled at grades three and two) and seeded runs recover $\log H$ for these eight; the whole circuit is checked on classical basis paths only.
```

(One sentence, long like its neighbours. "Sampled targets and q": one random (x, q) per label tuple, §3.3.)

## 7. Files and commands

- `theorems/rees_circuit_coherent_c4.py` (new): `config`, `instances`, `blocks`, `counts_report`,
  `macro_checks`, `rank_le1_tuples`, `random_rank_le1_tuples`, `rref_label_chunks`, `sde_check`,
  `sde_check_rref`, `block_check_labels`, `block_check_rref`, `block_mutants`, `assembled_mutants`,
  `source_exact_check`, `SourceFromKernel`, `state_checks`, `run_seeded`, CLI `main`.
- `tests/test_rees_circuit_coherent_c4.py` (new): 26 tests (23 default, about 30 s; 3 more with
  REES_SLOW=1: source check of γ_3 and γ_2, a Z(G) state check plus a seeded ⟨e2⟩ run, and the
  wiring of a whole terminal sample with its two mutants).
- `research/audits/reviews/2026-11-04-rees-circuit-coherent-c4/`: `run.json` / `.log`, `rref_paths.json` / `.log`,
  `state_runs.json` / `.log`, `state_wide.json` / `.log`.
- This report. No existing file edited; nothing committed or pushed.

```bash
D=research/audits/reviews/2026-11-04-rees-circuit-coherent-c4
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -u -B -m theorems.rees_circuit_coherent_c4 --parts counts,macros,proofs,sde,blocks,mutants --out $D/run.json   # ~2.5 min
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -u -B -m theorems.rees_circuit_coherent_c4 --parts rref,paths --paths 512 --out $D/rref_paths.json   # ~8.5 min
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -u -B -m theorems.rees_circuit_coherent_c4 --parts state,runs --state-instances 0,1,2,3,4,5,6,7 --run-instances 0,1,2,3,4,5,6,7 --tuples 64 --out $D/state_runs.json   # ~2 min
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -u -B -m theorems.rees_circuit_coherent_c4 --parts state --state-instances 0,1,2,3,4,5,6,7 --tuples 1024 --max-all 117649 --out $D/state_wide.json   # ~1 min
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_coherent_c4.py
```

Test runs in this session: new file 23 passed, 3 skipped (default, 31 s); the 3 slow tests passed with
REES_SLOW=1 (304 s); `tests/test_rees_circuit_coherent_k3.py` rerun: 22 passed, 1 skipped (50 s).

## 8. Next hard question

Is there a coherent backend for a grade with p ∈ E_2(κ_d)? The smallest is this same algebra over F_5
(κ_4 = 4, p = 5 ∈ E_2(4)), where no universal two-level contraction exists and the triangular solver
does not apply; Chevalley–Warning or Schedules 1/3 would need coherent versions. Cheaper next steps on
this instance: an independent AI review of this module; the γ_2 state check with a support-aware
instrument (condition only the labels of positive probability, without materialising 7^10 rows);
acceptance: equality with ρ_{H_3} at grade four and the uniform readout on h^⊥.

## Post-review fixes (11-04)

Code only (`theorems/rees_circuit_coherent_c4.py`, `tests/test_rees_circuit_coherent_c4.py`); this report text, the
JSON and the paper are unchanged.

- G1: `source_exact_check` now also requires exactly one source `qft` per address register, in register order, all
  before the first evaluation macro and with no other `qft`/`qft_dg` before the instrument
  (`source_transforms_one_qft_per_address`); that the oracle output registers are distinct and disjoint from the
  address and `w` registers (`oracle_outputs_distinct_fresh`); and that each address register's form is its unit
  vector after the last uncompute (`address_register_restored`). Mutants M1 (one source transform deleted) and M2
  (`a_0 += a_5` after the last uncompute) now give `passed = False` (tests
  `test_source_check_rejects_source_mutants`).
- `run_seeded` returns `recovered: False, source_check_failed: True` without running when the source check fails
  (`test_run_seeded_refuses_failed_source`).
- Basis paths: new `basis_paths_checked` wraps `K.assembled_basis_paths` and reports a structural crash
  (KeyError etc.) as `passed: False` with a `crashed` field; used by `assembled_mutants` and the CLI. The slow test
  checks M1 and M2 through it.
- Tests for the four grade-2 block mutants (`g_sign`, `skip_ctrl_inv`, `skip_sde_inv`, `skip_bennett`) added
  (`test_grade2_block_mutations_detected`).
- Not changed: I1-I7 wording/field renames (I3 exact homomorphism check, I4 mutant label, I6 `oracle_queries`
  rename, I7 `label_law_uniform` support comparison) and the report and LaTeX text. `assembled_basis_paths` in the
  shared module still raises on M1; only the c4 wrapper turns it into a failure.
