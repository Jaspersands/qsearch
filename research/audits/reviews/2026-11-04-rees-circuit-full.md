# Rees HSP: one gate-level circuit per terminal sample (explicit QFT + coherent labels)

4 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
**Status: AI-checked, pending human review.** COMPLETE (Sections 1-9). Written
incrementally; sections were appended as they were finished.

Labels: **[proved]** = written argument here (or cited proved statement); **[exact]** =
integer / bit-level computation on the emitted gate list, on all stated inputs;
**[sampled]** = exact on a stated subset; **[float]** = double-precision simulation.

Scope: Heis(F_3) and n4(F_5), the two instances of the coherent-label backend. New files
only: `theorems/rees_circuit_full.py`, `tests/test_rees_circuit_full.py`, this report and
the artifact folder `research/audits/reviews/2026-11-04-rees-circuit-full/`. Imported
read-only: `rees_circuit_coherent` (assembled coherent terminal sample `TerminalSample`,
`flatten`, footprints, witness references), `rees_circuit_qft_wire` (pool size,
`CircuitState` sparse simulator), `rees_qft_mod` (the gate list of Lemma `lem:qft-mod`,
`params_for_eta`, `error_bound`), `rees_circuit_general` (configs, instances, exact
`qft_matrix`). No existing file, no `.tex` file and no `research/reductions/*.json` was
edited; `theorems/rees_coherent_sde_k3.py` was not touched.

## 1. Design

**The combined circuit.** Start from the coherent terminal sample of
`rees_circuit_coherent.TerminalSample(cfg)` (an integer-wire program: X/CX/CCX/SWAP gates,
`add_product`/`add_scaled` macros of `rees_circuit_arith`, `qft`/`qft_dg` items on b-wire
registers, table-oracle items, one final `measure` of the root Q). Replace every `qft` item
by the gate list of `rees_qft_mod.qft_mod_ops(p, t, r, tp)` and every `qft_dg` item by its
inverse (reversed list, rotation signs flipped), relabelled:

* register X of the lemma (LSB first) -> the item's b-wire register (LSB first, the
  convention of `BitSim.load` and of the generator's encoding);
* F, Z, K, M, W, a (4b + 2t + 1 qubits) -> the **QFT pool** (below);
* the lemma's 3b + 5 arithmetic ancillas -> the terminal sample's own `arith_ancilla`
  register `ts.anc` (same `Anc` layout Y, P, r, e, c0, f, g, h, index by index).

Every macro is expanded with its `rees_circuit_arith` gate list (as `rees_circuit_coherent.
flatten` does). The emitted list then contains only X, CX, CCX, SWAP, H, R_k^{±1} =
Phase(±2π/2^k) and CR_k^{±1}, plus the oracle calls (excluded, as everywhere) and one
measurement of the root Q at the very end. Nothing is measured before it.

**Ancilla sharing (the design choice of this pass).** The QFT pool is overlaid on the
first 4b + 2t + 1 wires of the coherent terminal sample's `block_workspace_pool` (the wires
that hold the witness S, the SDE workspace and the merge workspace G, powers, W, bracket
registers inside a merge block). That pool has 99 wires at Heis(F_3) and 368 at n4(F_5),
more than the QFT pool at every parameter used here (61 resp. 77 at the targets), so the
explicit transforms add **no qubits** to the coherent circuit. (If 4b + 2t + 1 exceeded
the block pool, the remainder would be fresh wires; option `layout="separate"` puts the
whole QFT pool on fresh wires, for comparison.) The arithmetic ancillas are shared by the
transforms, the source evaluations, the instruments and the merge blocks, as in the two
parent backends.

**Why the overlay is sound [proved].** Order the K transform calls of one terminal sample.
Let U_k be call k with the exact transform (acting on its qudit only) and V_k the emitted
lem:qft-mod slice, and let psi_k be the state just before call k in the circuit in which
calls 1..k-1 are exact (with the exact Fourier transform everywhere this is the coherent
backend's circuit). Every gate other than a transform is the same unitary in both
circuits, and the only measurement is at the end, so the telescoping identity
H_K - H_0 = sum_k (H_k - H_{k-1}) (H_j: calls <= j exact, the rest explicit) gives

  || psi_explicit - psi_exact || <= sum_k || (V_k - U_k) psi_k ||,

the rest of the circuit after call k being unitary whatever it does on a dirty pool. Each
term is bounded by Lemma `lem:qft-mod` (an operator-norm bound on the canonical subspace
tensored with |0> on the pool and the arithmetic ancillas, entanglement with the rest
allowed) **provided** that in psi_k (i) the 4b + 2t + 1 pool wires and the 3b + 5 arithmetic
ancillas are |0>, (ii) the called register is supported on canonical words, and (iii) the
called register is disjoint from the pool and the ancillas. In the exact-transform circuit
the pool wires are touched only inside merge blocks, every merge block returns them to 0 on
every canonical basis input (Lemma 1 of the coherent report: proved, plus block_check),
every arithmetic macro returns the ancillas to 0 on every canonical input (I146), no
transform call lies inside a merge block, and an exact transform never touches the pool;
so by linearity (i) holds at every call, whatever superposition the other registers are in.
(ii) holds because every register of the exact coherent circuit is canonical (block outputs
canonical; QFT_p maps canonical words to canonical words). (iii) is a disjointness check
of wire roles. Hence the overlay changes nothing in the hybrid bound of the qft-wire report:
in the explicit circuit the block workspace may begin a merge block with the residue a
transform left in the pool, and that residue is exactly what the bound charges. No separate
"pool is clean before each block" statement is needed (or true) in the explicit circuit.

The checks of (i)-(iii) on the emitted circuit are in Section 3: a static wire-role and
footprint check, and a bit-level basis-path run of the whole assembled program asserting
that the pool and the ancillas are 0 immediately before every one of the 24 resp. 176 calls.
Three layout mutants (pool overlaid on live label registers; on the oracle outputs; on the
called register itself) are rejected.

**Error budget per terminal sample [proved, given lem:qft-mod as now stated in main.tex].**
With the measurement at the end and nothing in between, the total variation distance
between the readout laws of the explicit and the exact-transform circuit is at most
delta = sum_k ||(V_k - U_k) psi_k||. Following the paper's current wording, a **forward**
transform whose input is |0> is charged its preparation error 3 pi 2^-tau <= eta/(b+3); every
other transform (every inverse transform, and every forward transform on a non-|0> input)
is charged eta. "Input |0>" is an exact computation on the emitted list: no earlier gate
touches the called register. In these circuits every transform with input |0> is forward
(source addresses, instrument labels and Q registers are fresh when first transformed);
every inverse transform (instrument label, after `a_top -= z`) and the final readout are
general. A seeded run uses n = m + 4 independent terminal samples (7 at Heis(F_3), 8 at
n4(F_5)) and no classical feed-forward inside a sample (the witness is coherent), so
coupling each sample with the exact-transform one gives P(run differs) <= n delta.

## 2. Exact gate and qubit counts per terminal sample [exact]

From `counts_report` (artifact `counts.json`): the whole emitted list of one terminal sample
is streamed and every gate counted by component and type; oracle calls excluded, the one
final measurement not counted. The emitted total equals, as it must, the coherent
backend's count plus (number of transforms) x (gates per transform)
(`formula_equals_emitted` = true for both instances and both parameter sets).

**Choice of eta.** Lemma level, as main.tex now words it: per terminal sample
delta_lemma = n_general eta + n_zero 3 pi 2^-tau, where n_zero counts forward transforms on
input |0> (an exact computation on the emitted list) and (t, r, tau) = `params_for_eta(p,
eta)` (r capped at t), for which every call is within eta (qft-mod Corollary 8) and
3 pi 2^-tau <= eta/(b+3). eta is the largest two-significant-digit value with
n delta_lemma < 0.1 (`target_params`). The exact-formula bound (qft-mod Theorem 6
evaluated: B per general call, the exact prep term per zero-input forward call) is shown
too; it is about a third to a half of the lemma-level one.

| | Heis(F_3) | n4(F_5) |
|---|---|---|
| transforms per sample: forward on \|0> / general (inverse + final readout) | 18 / 6 (3 `qft_dg` + 3 final) | 148 / 28 (24 `qft_dg` + 4 final) |
| terminal samples per run n | 7 | 8 |
| eta | 1.5e-3 | 2.5e-4 |
| (t, r, tau) | (26, 19, 15) | (32, 22, 18) |
| delta per sample, lemma level / exact formula | 0.01418 / 0.00456 | 0.01232 / 0.00657 |
| **P(run differs from the exact-transform coherent run)**, lemma level / exact formula | **0.0992** / 0.0319 | **0.0986** / 0.0526 |
| QFT pool 4b+2t+1 (overlaid on the block-workspace pool of 99 / 368 wires) | 61 | 77 |
| **qubits** (overlay) | **182** (= coherent backend) | **1198** (= coherent backend) |
| qubits with the pool on fresh wires (`layout="separate"`) | 243 | 1275 |
| gates per transform (forward = inverse); closed-form bound `gate_bound` | 7873; 8405 | 13303; 14948 |
| gates in the transforms (K x per call) | 188952 | 2341328 |
| gates outside the transforms (the coherent backend's count) | 115282 | 2694596 |
| **total gates per terminal sample, oracle excluded** | **304234** | **5035924** |
| oracle calls (excluded) | 6 | 36 |
| largest rotation index max(r, tau) | 19 | 22 |

Totals by gate type. Heis(F_3): X 44888, CX 173578, CCX 66552, SWAP 736, H 2784,
R_k^{±1} 1392, CR_k^{±1} 14304. n4(F_5): X 733700, CX 2880524, CCX 1205132, SWAP 22440,
H 25168, R_k^{±1} 13376, CR_k^{±1} 155584. (Per transform: Heis H 116, R 58, CR 596, X 982,
CX 4453, CCX 1658, SWAP 10; n4 H 143, R 76, CR 884, X 1632, CX 7511, CCX 3030, SWAP 27.)

**By component** (gates; transforms in brackets as calls x 7873 resp. 13303):

| component | Heis(F_3) | n4(F_5) |
|---|---|---|
| source transforms (forward, input \|0>) | 94476 (12) | 1117452 (84) |
| source evaluations (compute + uncompute) | 12192 | 239640 |
| instrument transforms (forward on \|0>, and inverse) | 47238 (3 + 3) | 638544 (24 + 24) |
| instrument a_top -= z | 762 | 11424 |
| Q preparation transforms (forward, input \|0>) | 23619 (3) | 532120 (40) |
| coherent SDE U + U^-1 | 60208 (grade 2) | 437664 (grade 3, 6 blocks) + 702932 (grade 2) |
| witness control G = -delta_s(sigma(q)) | 12816 | 248544 (grade 3) + 71040 (grade 2) |
| BCH merges | 29304 | 772980 (grade 3) + 210372 (grade 2) |
| final readout transforms (general) | 23619 (3) | 53212 (4) |
| **total** | **304234** | **5035924** |

Qubits by role (overlay layout; the QFT pool is not a separate role, its wires are the
first 61 resp. 77 block-workspace-pool wires): Heis addresses 24, oracle outputs 30,
labels 6, root Q 6, evaluation w 6, arithmetic ancillas 11, block-workspace pool 99;
n4 addresses 252, oracle outputs 360, labels 36 + 36, grade-2 Q 108, root Q 12, w 12,
arithmetic ancillas 14, block-workspace pool 368. Of the 182 resp. 1198 qubits, 152 resp.
838 are touched by a counted gate; the rest are oracle outputs, touched only by U_f.

At the simulation parameters used in Section 3 ((7, 7, 28) resp. (8, 8, 28); 3420 resp.
5874 gates per transform) the totals are 197362 resp. 3728420 gates on the same 182 resp.
1198 qubits; the proved budgets there are vacuous (P = 1), as in the qft-wire report.

Reading. The combined circuit costs the coherent backend plus the explicit transforms;
neither component interferes with the other's count. At these tiny primes the transforms
are 62% (Heis) resp. 46% (n4) of the gates. Against the qft-wire backend with measured
labels at the lemma-level targets (154 qubits / 231210 gates resp. 835 / 2997844), the
coherent labels cost +28 resp. +363 qubits and x1.3 resp. x1.7 gates; the n4 arity change
(M_2 = 6 instead of 5) is part of that. Nothing asymptotic is claimed.

## 3. Checks

### 3.1 Exact checks on the emitted circuit (`checks.json`, target parameters)

All on the complete emitted gate list of one terminal sample (Heis(F_3) 304234 gates,
n4(F_5) 5035924), streamed, at (26, 19, 15) resp. (32, 22, 18).

| check | Heis(F_3) | n4(F_5) |
|---|---|---|
| **gate set** (`gate_set_check`): every gate in {X, CX, CCX, SWAP, H, R_k^{±1}, CR_k^{±1}}, right arity, distinct wires inside the circuit, R/CR with integer 1 <= k <= max(r, tau) and sign ±1 | pass (304234 gates; k <= 19) | pass (5035924 gates; k <= 22) |
| exactly one measurement, the last item, on the root Q; oracle items excluded and counted | pass (6 oracle calls) | pass (36) |
| **slices** (`slice_check`): each transform slice equals, gate by gate (name, wires, k, sign), the list `qft_mod_ops(p, t, r, tau)` (resp. its inverse) rebuilt inside the check and relabelled from the `Layout` fields (X -> called register taken from the coherent item, F, Z, K, M, W, a -> pool, arithmetic ancillas -> `arith_ancilla`); footprint inside register + pool + ancillas, pairwise disjoint | 24 slices, 188952 gates compared, pass | 176 slices, 2341328 gates, pass |
| **wires, static** (`wire_check`): pool, ancillas and every called register disjoint; pool wires all of role `block_workspace_pool`; outside merge blocks no item touches a pool wire; no transform, oracle call or measurement inside a merge block; blocks = merge nodes; zero-input classification from the emitted stream = item level; every zero-input call forward | pass (1 block) | pass (7 blocks) |
| **basis paths** (`basis_paths`, whole assembled program, bit level): pool and ancillas 0 on every path immediately before **every** transform call; zero-input registers 0; every child, label and root Q equal to the independent classical recursion of the coherent report (address a -> (a z^-1) * (-delta_{s_i}(sigma(q))) with s the canonical witness of the sibling labels); w, ancillas and block pool 0 at the end | 16384 paths, 24 calls, pass | 1024 paths, 176 calls, pass |

The basis-path model is the classical skeleton of the exact-transform circuit, as in the
coherent report except for the oracle: a forward transform on a fresh register is replaced
by a random canonical load, the other transforms are skipped, an oracle call XORs a random
value into its output register (so the oracle outputs are live, as f(w) makes them; the
coherent report skipped the oracle, which would hide a pool placed on oracle outputs), and
every other item is run bit by bit. It checks premise (i) of Section 1 on the
same permutation program the exact-transform circuit runs between transforms, and the
wiring; it does not exercise the transform slices (they are not permutations); the slices
are covered by `slice_check` and the float checks below.

`slice_check` is a consistency and mutation check: its reference is the same
deterministic `qft_mod_ops` and the relabelling it rebuilds coincides with the emitter's
(the layout is sequential), so what it verifies is that every slice is that list on the
right wires with nothing added, and the footprint and disjointness. The correctness of the
list itself (LSB-first X included) is the qft-mod report's, and it is re-checked in float
on the emitted slices in Section 3.2.

Mutants (all rejected, at both instances): `layout="mutant_labels"` (pool overlaid on the
label registers, which are live after their instrument) fails `wire_check` and the
basis-path premise; `layout="mutant_oracle"` (pool on the oracle output registers) fails
both; `layout="mutant_qudit"` (pool containing the first address register)
fails both; a rotation index changed by one in the first slice fails `slice_check`
(`equal_to_lemma`); one gate of the first slice moved onto the evaluation register fails
the footprint test. `layout="separate"` (pool on 61 fresh wires, 243 qubits) passes the
same checks (test only, Heis).

### 3.2 Floating-point simulations (what was simulated)

Simulator: `rees_circuit_qft_wire.CircuitState` (sparse basis-key simulator; H merges equal
keys, amplitudes below `tol` dropped after an H and their norm accumulated in `prune_err`,
so the true distance is within `prune_err` of the reported one). Each run is over **every
wire the segment touches** (called registers, QFT pool on its overlay wires, arithmetic
ancillas, block workspace, oracle outputs), once with the emitted explicit slices and once
with the exact transform (`qft_matrix` as a b-qubit unitary), from the same initial
state; the full output vectors are compared. Budgets are the proved exact-formula hybrid
bounds of Section 1 for exactly the calls in the segment. All at smaller t than the
targets (the targets need ~10^7-10^9 basis states per general call).

**(a) Single transforms, as emitted in the full circuit** (`per_call.json`). One slice of
each (component, kind) is cut out of the emitted list and run on every canonical input
|x>|0> over its own wires (register + pool + ancillas, 36 resp. 46 wires); sigma_max is
the operator norm of V - QFT_p^{±1} (x) |0> on the canonical subspace.

| p | (t, r, tau) | slices (5 components) | sigma_max | sigma_upper / B | column error at \|0>: forward / inverse | prep (proved) |
|---|---|---|---|---|---|---|
| 3 | (7, 7, 28) | source, instr. fwd, Q prep, final; instr. inverse | 0.11475 (all 5) | 0.518 | 1.194e-8 / 0.0930 | 1.194e-8 |
| 3 | (9, 9, 28) | same | 0.05697 | 0.523 | 1.194e-8 / 0.0464 | 1.194e-8 |
| 3 | (7, 7, 8) | same | 0.11505 | 0.491 | 4.624e-3 / 0.0934 | 4.624e-3 |
| 5 | (8, 8, 28) | same | 0.11792 | 0.585 | 4.057e-9 / 0.0873 | 4.057e-9 |
| 5 | (8, 8, 8) | same | 0.11834 | 0.534 | 5.309e-3 / 0.0878 | 5.309e-3 |

Every slice is within its proved bound; the forward column error at |0> equals the prep term
to within 4e-15 in every row (the zero-input refinement), while the **inverse** transform on
|0> has error 0.044-0.093, far above prep: charging inverse calls the cheap rate would be
wrong, and the budget does not. The values agree with the standalone qft-mod and qft-wire
runs (0.1148, 0.0570, 0.1179), as they must for the same list on other wires.

**(b) First top source with its unmeasured instrument** (`source_segment.json`).
Heis(F_3), (7, 7, 28), all 19 subgroups: items 0-24 of the terminal sample (4 address
transforms, 2 evaluations + oracle calls + uncomputations, label transform, a_top -= z,
inverse label transform; 5 zero-input forward calls + 1 general), 60 wires, 24840 explicit
gates; the label register is not measured. Distance 0.09304 for the 13 subgroups not
containing the centre and 1.19e-8 for the 6 containing it (prune_err <= 6.7e-8), against
the proved budget 0.2215 (ratio 0.42); the exact run puts no probability on a nonzero pool
or ancilla wire. These are the qft-wire report's numbers for the same gates on its own
layout (it measured the label afterwards), as expected. n4(F_5), (4, 4, 28), subgroups
<e2>, <e1>, <e1+e3>: the source and the instrument up to (not including) the inverse label
transform (7 + 1 zero-input forward calls, 3 oracle calls), 101 wires, 58225 explicit
gates: distance 2.2e-14, prune_err 4.2e-8, budget 3.2e-8 (all residue is pruned mass). The
inverse transform was left out at n4: it multiplies a support of 5^7 addresses x 5 labels
by its ~10^3-10^4-state pool tail.

**(c) Q preparation + one merge block** (`merge_segment.json`; "single merges"). The
forward transforms on the fresh Q register (zero input) followed by the whole merge block
(U_SDE, the M controlled merges, U_SDE^-1), with the QFT pool **overlaid on the block's own
workspace** (the case the overlay argument is about), from a uniform superposition of K
random canonical basis assignments of all children and labels:

| block | (t, r, tau) | wires | explicit gates | K inputs | support (exact) | distance | prune_err | budget | exact run: mass on pool/ancillas |
|---|---|---|---|---|---|---|---|---|---|
| Heis grade 2 (3 Q transforms) | (7, 7, 28) | 146 | 112588 | 64 | 1728 | 1.2e-14 | 5.0e-8 | 3.6e-8 | 0 |
| n4 grade 3, first block (6 Q transforms) | (8, 8, 28) | 145 | 278442 | 2 | 31250 | 2.3e-14 | 3.4e-8 | 2.4e-8 | 0 |
| n4 grade 2, root block (4 Q transforms) | (8, 8, 28) | 538 | 1007840 | 2 | 1250 | 1.4e-14 | 2.3e-8 | 1.6e-8 | 0 |
| mutant: pool on live labels, Heis, first Q transform only | (7, 7, 28) | 60 | 3420 | 64 | - | **1.45** | 1.3e-8 | 1.2e-8 | - |
| mutant, n4 grade 3 | (8, 8, 28) | 88 | 5874 | 2 | - | **1.41** | 1.9e-10 | 4.1e-9 | - |
| mutant, n4 root | (8, 8, 28) | 178 | 5874 | 2 | - | **0.80** | 5.7e-9 | 4.1e-9 | - |

With the correct overlay the block runs on whatever residue the Q transforms left in its
workspace and the explicit output stays within the (prep-only) budget; the exact run's
output has zero probability on a nonzero pool or ancilla wire after the block (the float
form of premise (i)). With the pool placed on live label registers a single transform is
already off by 0.8-1.45, 10^8 times its budget: the lemma's premise fails and the bound
with it. (This check is weak in one direction: with zero-input calls only, every residue is
below tol and is pruned, so these rows show consistency at round-off plus the pruned mass,
not a resolved error; an attempt at tau = 8 to make the residue visible needed tol = 1e-6
and gave distance 0.0042 against a pruned mass 0.016, too coarse to report as a check.)

**Not simulated.** A monolithic state of a whole terminal sample, explicit or exact (Heis
182 qubits; the exact coherent state alone has ~10^10 basis states); any segment with two
general calls in sequence (pool tails multiply: ~10^4 states per call at these t); the
final readout and the instrument inverse transforms inside a larger segment (only as single
slices, (a)); n4 sources with their inverse label transform; anything at the target
parameters (26, 19, 15), (32, 22, 18) (their slices are checked structurally and counted;
their error is the proved bound); noise. End to end the combined circuit is covered by the
proved composition of Section 1 plus the exact checks of 3.1, not by a simulation.

## 4. End-to-end statement and recoveries

**Proposition [proved, given lem:qft-mod, the coherent report's Lemma 1 / Theorem 3, and the
checks of Section 3.1].** For Heis(F_3) at (t, r, tau) = (26, 19, 15) and n4(F_5) at
(32, 22, 18), the emitted circuit of one terminal sample (every gate in {X, CX, CCX, SWAP, H,
R_k^{±1}, CR_k^{±1}}, k <= 19 resp. 22, oracle calls aside, one measurement at the end) has
readout law within total variation 0.01418 resp. 0.01232 (lemma level) of the readout law of
the coherent backend with exact transforms; hence a seeded run with 7 resp. 8 terminal
samples agrees outcome for outcome with the exact-transform coherent run except with
probability <= 0.0992 resp. 0.0986 (exact formula: 0.0319 resp. 0.0526).

Recoveries are cited, not rerun: the coherent report recovers log(H) in 38/38 seeded runs on
Heis(F_3) (19 subgroups x 2 seeds, readout law from the exact module-by-module simulation)
and 18/18 on n4(F_5) (9 subgroups x 2 seeds, exact Engine with circuit-computed witnesses,
equal in law by its Theorem 3). By the proposition each such run is reproduced by the
combined circuit with probability >= 0.90, so it recovers log(H) with probability >= 0.90.
No run was executed on the combined circuits themselves.

## 5. Limits

1. Not a monolithic simulation (Section 3.2, "Not simulated"); the end-to-end statement is
   the proved hybrid composition plus exact structural and basis-path checks.
2. Two instances only (every grade kappa_d <= 2); kappa_d >= 3 grades have no coherent solver
   here, and `rees_coherent_sde_k3.py` was not used or touched.
3. The hybrid bound rests on lem:qft-mod (qft-mod Theorem 6, Corollary 8) and its
   arithmetic blocks (exhaustive for p <= 13), and on the coherent report's Lemma 1 for the
   blocks returning their workspace to 0 (exhaustive at Heis, sampled at n4, plus the
   symbolic proof of the controlled merges); Section 3.1 checks the wiring premises on the
   emitted list and on basis paths (16384 resp. 1024), not on all basis inputs.
4. Gate set Gamma_kappa: R_k with k up to 19 / 22 are primitives; no Clifford+T synthesis.
5. The n4 arity is the coherent one, M_2 = 6 (CW arity 5); paper arities unchanged.
6. No optimisation: the pool overlay is the only sharing added; U_SDE^-1 is kept, the label
   registers and consumed children are garbage, no wire reuse across merge subtrees.
7. Oracle cost T_f not counted; noise, depth, layout not considered; nothing asymptotic.

## 6. Claim gates and flags

`research/reductions/rees_hsp_reduction.json` is not edited (no `research/reductions/*.json`
is); `coherent_receiver_implemented` stays **false** there and in every module status
(asserted in `test_status_and_claim_gates_stay_false`, together with
`rees_qft_mod.STATUS["rees_generator_uses_this_qft"]` = False, unchanged since that module
was not edited). New module `STATUS`: `full_gate_level_terminal_sample` = True and
`no_mid_circuit_measurement` = True, scoped to Heis(F_3) and n4(F_5);
`monolithic_simulation`, `fixed_finite_gate_set`, `coherent_receiver_implemented`,
`general_instances`, `kappa_ge3_grades_coherent`, `independent_review`,
`speedup_claim_allowed` all False. No claim of advantage, asymptotic cost or native
application follows.

## 7. Proposed sentences for main.tex, "Gate-level control" (not applied)

Insert after the sentence of the fourth backend ending "...(all label pairs at grade three,
all or sampled label tuples at grade two)." and before "By a hybrid argument over the
transforms":

```latex
Combining the third and fourth backends, \file{theorems/rees_circuit_full.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-full.md}; finite computation, AI-checked, pending human review) emits one circuit per terminal sample over $\mathbb{F}_3$ and $\mathbb{F}_5$ in which every gate except the oracle is $X$, CNOT, Toffoli, SWAP, $H$, $R_k^{\pm1}$ or $\mathrm{C}R_k^{\pm1}$ and nothing is measured before the final Fourier sampling; the ancillas of the transforms are placed on the workspace of the coherent merge blocks, which is $|0\rangle$ at every transform in the circuit with exact transforms, so the bound below applies unchanged and no qubit is added. With $\eta = 1.5\cdot10^{-3}$, resp.\ $2.5\cdot10^{-4}$ ($24$ transforms, $6$ of them on inputs other than $|0\rangle$, resp.\ $176$ and $28$), one terminal sample uses $182$ qubits and $304234$ gates, resp.\ $1198$ qubits and $5035924$ gates, and a run with $7$, resp.\ $8$, terminal samples agrees with the coherent run with exact transforms except with probability below $0.1$; this circuit is checked gate by gate and on classical basis paths, and simulated in floating point only in pieces (single transforms, the first source, single merges) at smaller $t$.
```

(Two sentences. Every number is in Sections 2-4. The sentence relies on the paragraph's
existing hybrid-bound sentence, which follows it, for the meaning of the charge per
transform; if the integrator prefers the new sentence after that sentence, replace "the
bound below" by "the bound above".)

## 8. Tests, artifacts, commands

* `tests/test_rees_circuit_full.py`: 11 tests (status/claim gates; targets and budgets;
  Heis and n4 counts and gate set over the whole emitted list; slices and wires at both
  instances; basis paths (1024 / 128 paths); mutants rejected (three layouts, rotation,
  footprint); separate layout; per-call float; Heis source segment float; Heis merge
  segment float with the label mutant). Default run about 18-25 s.
* Artifacts in `research/audits/reviews/2026-11-04-rees-circuit-full/`: `counts.json`/`.log`
  (12 s), `checks.json`/`.log` (29 s), `per_call.json`/`.log` (~20 s),
  `source_segment.json`, `merge_segment.json`, `float_segments.log` (331 s).

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_full.py
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m theorems.rees_circuit_full --out research/audits/reviews/2026-11-04-rees-circuit-full --parts counts,checks,per_call,source,merge
```

## 9. Independent review (AI subagent, unanchored)

A separate AI agent was given the module, the tests and a list of questions, not this
report's conclusions. It found no correctness bug: the lemma-to-circuit relabelling, the
overlay (it flattened every permutation item and found no gate outside a merge block on a
pool wire, at both instances), the zero-input classification (no inverse charged the cheap
rate; float: inverse on |0> has error 0.093-0.35, forward equals prep also for r < t), the
gate-set and count coverage, the float helpers (oracle wire order, sign convention, the two
backends really differ) and the eta choice (it swept `params_for_eta` over 8 primes up to
65537 and eta in [1e-8, 0.99]: B <= B_simple <= eta and prep <= 3 pi 2^-tau throughout).
It found one test-strength gap, fixed here: the basis-path model skipped the oracle, so a
pool placed on the oracle outputs passed `basis_paths` (only `wire_check` caught it); the
oracle now XORs random values into its outputs, `mutant_oracle` was added and is rejected
by both checks. It also asked that `slice_check` be described as a consistency and
mutation check rather than an independent derivation (done in Section 3.1 and the
docstring). Nits not changed: `wire_check` rejects an overlay on the evaluation register w
(over-strict, harmless); oracle wires are not range-checked by `gate_set_check`; the exact
float run keeps exact-zero amplitudes. This is not human review.

Next step for the paper owner: decide whether to add the combined-backend sentences of
Section 7; human review of the overlay argument of Section 1.
