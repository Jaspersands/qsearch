# Wiring the explicit QFT over Z/N (lem:qft-mod) into the Rees circuit generator

Date: 2026-11-04. AI session only; **AI-checked, pending human review**.
Status: COMPLETE (AI session; pending human review).

Scope: the "Gate-level control" paragraph of `docs/papers/rees-hsp/main.tex`
(Section `sec:uniform-compilation`), which says that Lemma `lem:qft-mod`
"is not wired into these circuits". No `.tex` file, no existing theorem
module and no existing test was edited; `research/reductions/rees_hsp_reduction.json`
and every claim gate are untouched. New files only:
`theorems/rees_circuit_qft_wire.py`, `tests/test_rees_circuit_qft_wire.py`,
this report and the folder `research/audits/reviews/2026-11-04-rees-qft-wire/`.

Labels as in the qft-mod report: **proved** (proof given or cited to a
proved statement), **exact computation** (integer / structural computation
on all listed inputs), **float check** (double-precision simulation).

## 1. What was found and what was wired

**How the generator does the transforms (before this pass).** In
`theorems/rees_circuit_general.py`, `Builder.qft(q, role, inverse)` appends
one opaque gate `qft{p}` (or `qft{p}_dg`) whose definition is a single dense
`UnitaryGate` on the b = ceil(log2 p) qubits of the qudit: `qft_matrix(p)`,
the p x p Fourier matrix on the canonical words plus the identity on padding.
`ArithBuilder.qft` in `rees_circuit_arith.py` inherits it unchanged. Every
QFT call site goes through `Builder.qft`: `source_ops` (one `qft_leaf` per
cover coordinate), `instrument_ops` (a QFT and an inverse QFT on each
ancilla z_j), the grade-d `Q` registers in `terminal_sample_circuit`
(`qft_grade{d+1}`), and the final readout (`qft_final`). The exact engines
(`Engine.source`, `instrument_semantics`, `rees_circuit_sparse`) rely on the
transform being this one exact gate: `Engine.source` refuses a source whose
head is not `qft{p}`.

**What was added** (`theorems/rees_circuit_qft_wire.py`, no existing file
edited; same pattern as the arithmetic backend):

* `ExplicitQFTBuilder(ArithBuilder)`: `qft()` emits the gate list of
  `rees_qft_mod.qft_mod_ops(p, t, r, tp, inverse)` (the circuit of Lemma
  `lem:qft-mod`; the inverse is the reversed list with rotation signs
  flipped), relabelled: register X of the lemma -> the macro's qudit
  (LSB first, as in the generator's encoding); F, Z, K, M, W, a (4b + 2t + 1
  qubits) -> a QFT pool register `qftpool*`; the 3b + 5 arithmetic ancillas
  of the lemma -> the ArithBuilder's own `arith` register (same block
  library, same layout `Y, P, r, e, c0, f, g, h`). Gates emitted:
  X, CX, CCX, SWAP, H, Phase(2 pi s/2^k), CPhase(2 pi s/2^k). The macro record
  (kind `qft`/`qft_dg`, qudit, gate slice) and the role counters are the same
  as before, so every generator function runs unchanged.
* pool modes: `pool="shared"` (default: one pool for all calls; every call
  returns it to |0> up to the lemma's error) and `pool="fresh"` (one pool
  per call, for accounting only).
* backend selection: `backend(qft="exact"|"explicit", params=(t, r, tp) or eta=...)`,
  `terminal_sample_circuit(cfg, inst, witness, qft=..., ...)` and
  `build(fn, cfg, ..., qft=...)`. `qft="exact"` (the default) is the
  generator as it was (with `arith=False` literally the original
  generator; with `arith=True` the ArithBuilder arithmetic); the context
  managers restore `G.Builder` and `G.check_macros` on exit.
* `check_macros_qft`: every gate except a measurement lies in exactly one
  macro; each qft slice equals, gate by gate (type, angle, qubits), the
  relabelled reference list and touches only its qudit, its pool and the
  `arith` register; arithmetic macros get the ArithBuilder check (all
  canonical inputs, ancillas returned to 0, operands never targeted).
  **exact computation**; it passes on every circuit generated below.
* simulators: `CircuitState` (the sparse basis-state simulator of
  `rees_qft_mod`, extended by multi-controlled X, a dense few-qubit unitary
  for the exact `qft{p}`, and the table oracle `U_f`), `call_operator_error`
  (operator norm of `V - QFT_p^{+-1} (x) |0>` of ONE emitted slice on the
  canonical subspace, all touched qubits), `compare_prefix` and
  `instrument_block_error` (both backends simulated gate by gate over all
  qubits), and `hybrid_budget` / `coupling_bound` (Section 4).

The explicit backend does NOT feed the exact Z[zeta_p] engines: with an
approximate transform the states are no longer exactly the left-invariant
densities those engines store. Its semantics are checked by simulation and
by the hybrid bound instead (Sections 3-4).

## 2. Exact gate and qubit counts (exact computation, `counts.json`)

One terminal sample, oracle gates excluded, measurements not counted.
"exact+arith" is the generator with the ArithBuilder arithmetic and the
exact `qft{p}` gate (each transform counted as 1 gate); "explicit" replaces
each transform by the lem:qft-mod list. Simulation parameters: t = b + 5,
r = t, tp = 28. Target parameters: Corollary 8 of the qft-mod report,
`params_for_eta(p, eta)` (r capped at t), with eta the largest value on the
grid 0.5 * 2^(-j/8) for which the proved per-run coupling failure of
Section 4 is <= 0.1.

| config | backend | (t, r, tp) | qubits | pool | QFT calls (zero-input / general) | gates per call | QFT gates | arith gates | total |
|---|---|---|---|---|---|---|---|---|---|
| Heis(F_3), c=2 | original | - | 82 | - | 24 | 1 (unitary) | 24 | (value-controlled) | 1236 instr. |
| Heis(F_3) | exact+arith | - | 93 | 0 | 24 (18 / 6) | 1 (unitary) | 24 | 42234 | 42282 |
| Heis(F_3) | explicit, shared | (7, 7, 28) | 116 | 23 | 24 (18 / 6) | 3420 | 82080 | 42234 | 124338 |
| Heis(F_3) | explicit, fresh | (7, 7, 28) | 645 | 552 | 24 | 3420 | 82080 | 42234 | 124338 |
| Heis(F_3) | explicit, shared, target eta = 5.52e-3 | (22, 17, 14) | 146 | 53 | 24 (18 / 6) | 6878 | 165072 | 42234 | 207330 |
| n4(F_5), c=3 | original | - | 744 | - | 148 | 1 (unitary) | 148 | (value-controlled) | 91240 instr. |
| n4(F_5) | exact+arith | - | 758 | 0 | 148 (124 / 24) | 1 (unitary) | 148 | 1028700 | 1029148 |
| n4(F_5) | explicit, shared | (8, 8, 28) | 787 | 29 | 148 (124 / 24) | 5874 | 869352 | 1028700 | 1898352 |
| n4(F_5) | explicit, fresh | (8, 8, 28) | 5050 | 4292 | 148 | 5874 | 869352 | 1028700 | 1898352 |
| n4(F_5) | explicit, shared, target eta = 1.06e-3 | (28, 20, 16) | 827 | 69 | 148 (124 / 24) | 11994 | 1775112 | 1028700 | 2804112 |

(Totals include the 24 resp. 300 SWAP gates of the merge `swap` macros.)
Gate types of the explicit transforms at the target parameters: Heis
X 21264, CX 94200, CCX 35184, SWAP 240, H 2400, Phase 1368, CPhase 10416;
n4 X 222592, CX 1009212, CCX 408184, SWAP 3996, H 18796, Phase 10804,
CPhase 101528; largest rotation index max(r, tp) = 17 resp. 20. The per-call
counts are below the closed form `gate_bound` of the qft-mod report
(Proposition 7): 6878 <= 7318 and 11994 <= 13436; at the simulation
parameters 3420 and 5874 equal the counts of the qft-mod sweep table for
(N, t, r, tp) = (3, 7, 7, 28) and (5, 8, 8, 28). Qubits added by the
shared pool: 4b + 2t + 1 (23, 29, 53, 69); the 3b + 5 arithmetic ancillas are
shared with the ArithBuilder, so the transform adds no further qubits.

Reading. At these tiny primes the explicit transforms dominate the
terminal sample (Heis: 165072 of 207330 gates at the target) and roughly
double the n4 count; this is the expected constant-factor overhead
(about 420 b^2 per call for small L, qft-mod report Section 6) and says
nothing about asymptotics. The counts depend on p only through b and the
bit patterns of the constants, so they extend to large p by counting only;
no large-p terminal sample was counted in this pass.

## 3. What was simulated (float checks)

### 3.1 Per call, from the emitted slices (`per_call.json`)

For each (p, t, r, tp) below, the grade-c instrument circuit was generated
with the explicit backend, `check_macros_qft` passed, and each of its two
transform slices (one `qft`, one `qft_dg`) was simulated gate by gate on
every canonical input |x>|0> over every qubit it touches (qudit, pool,
arith ancillas; sparse simulator, amplitudes < 1e-13 dropped and accounted
for, `sigma_upper` = sigma_max + sqrt(p) * dropped-norm). sigma_max is the
operator norm of `V - QFT_p^{+-1} (x) |0>` on the canonical subspace; "col 0"
is the error on input |0>; B and prep are the proved bound and its exact
prep term (qft-mod Theorem 6, Lemma 1).

| p | (t, r, tp) | kind | sigma_max | col 0 | prep (proved) | B (proved) | max support |
|---|---|---|---|---|---|---|---|
| 3 | (7, 7, 28) | qft | 0.11475 | 1.194e-08 | 1.194e-08 | 0.2215 | 21729 |
| 3 | (7, 7, 28) | qft_dg | 0.11475 | 0.09304 | | 0.2215 | 3072 |
| 3 | (9, 9, 28) | qft | 0.05697 | 1.194e-08 | 1.194e-08 | 0.1089 | 86688 |
| 3 | (9, 9, 28) | qft_dg | 0.05697 | 0.04643 | | 0.1089 | 12288 |
| 3 | (11, 11, 28) | qft | 0.02844 | 1.194e-08 | 1.194e-08 | 0.05421 | 345061 |
| 3 | (11, 11, 28) | qft_dg | 0.02844 | 0.02321 | | 0.05421 | 49152 |
| 3 | (11, 11, 8) = eta 0.25 | qft | 0.02959 | 4.624e-03 | 4.624e-03 | 0.06701 | 348160 |
| 3 | (11, 11, 8) | qft_dg | 0.02959 | 0.02431 | | 0.06701 | 49152 |
| 5 | (8, 8, 28) | qft | 0.11792 | 4.057e-09 | 4.057e-09 | 0.2015 | 169344 |
| 5 | (8, 8, 28) | qft_dg | 0.11792 | 0.08734 | | 0.2015 | 20480 |
| 5 | (10, 10, 28) | qft | 0.05896 | 4.057e-09 | 4.057e-09 | 0.09930 | 674869 |
| 5 | (10, 10, 28) | qft_dg | 0.05896 | 0.04376 | | 0.09930 | 81920 |
| 5 | (12, 11, 8) = eta 0.25 | qft | 0.03109 | 5.309e-03 | 5.309e-03 | 0.07168 | 2711552 |
| 5 | (12, 11, 8) | qft_dg | 0.03109 | 0.02377 | | 0.07168 | 327680 |

Every emitted slice is within its proved bound (sigma_max ~ B/2), and the
sigma_max values agree with the standalone qft-mod runs at the same
parameters (0.1148, 0.0296, 0.1179, 0.0311 there), as they must: the slice
is the same gate list relabelled. The column error at |0> equals the
proved prep term to within 1e-14 (absolute) in every case. That is the fact used
below for zero-input calls, and it is **proved**, not only observed: on
input |0> the phase step is the identity (x y = 0), the eigenvalue of the
shift on |chi_0> is 1, so the phase-estimation register is mapped exactly to
|0> by the approximate inverse QFT for every r (each H acts on |+> before
any controlled phase can act, and the controlled phases are diagonal with
target already |0>), and k~(0) = 0; so in Theorem 6's telescoping only the
prep term is nonzero, ||(V - U)|0>|0>|| = eps_prep = 2|sin((pi/2 - 3 alpha~)/2)|.
(For V^dag on |0> no such statement is used; no zero-input inverse call
occurs in the generated circuits.)

### 3.2 Composite modules, both backends, gate by gate over all qubits

Method (`compare_prefix`, `instrument_block_error`). The same generator call
is made twice, once with the exact backend (ArithBuilder + exact `qft{p}`)
and once with the explicit backend (shared pool). Both gate lists are run
by the sparse simulator from |0...0> over ALL qubits of the circuit
(93 resp. 116 qubits for the Heis terminal-sample prefixes, 758 resp. 779
for n4), and the full output vectors are compared, qubits identified by
register name and index (pool qubits are |0> in the exact run). Amplitudes
below 1e-10 (1e-12 for the instrument blocks) are dropped after an H; the
true distance is within `prune_err` of the reported one (triangle
inequality over the dropped parts). The hybrid budget in the last column is
the proved bound of Section 4 for exactly the calls in the prefix.

| module | params | inputs / instances | qubits (exact / explicit) | gates (exact / explicit) | max distance | prune_err | proved hybrid budget |
|---|---|---|---|---|---|---|---|
| Heis first top source (4 `qft_leaf`, 2 evaluations, 2 oracle calls, uncompute) | (7, 7, 28) | all 19 subgroups | 93 / 116 | 3054 / 16730 | 1.6e-14 | 5.1e-08 | 4.8e-08 (4 zero-input calls) |
| Heis first quantum segment (that source + complete central instrument, up to the first measurement) | (7, 7, 28) | all 19 subgroups | 93 / 116 | 4326 / 24840 | 0.09304 (13 subgroups), 1.19e-08 (6 subgroups containing the centre) | 6.7e-08 | 0.2215 (5 zero-input + 1 general) |
| Heis instrument block (z: QFT, a_top -= z, QFT^dag) | (7, 7, 28) | all 3 canonical a_top | 21 / 44 | - / 7094 | 0.09304 | 1.4e-09 | 0.2215 |
| n4 instrument block, grade 3 | (8, 8, 28) | all 5 canonical a_top | 38 / 67 | - / 12224 | 0.08734 | 1.1e-08 | 0.2015 |
| n4 instrument block, grade 3 | (5, 5, 28) | all 5 | 38 / 61 | - / 10488 | 0.2526 | 2.8e-09 | 0.6404 |
| n4 first top source (7 `qft_leaf`, 3 evaluations, 3 oracle calls) | (4, 4, 28) | 3 subgroups (<e2>, <e1>, <e1+e3>) | 758 / 779 | 16652 / 49699 | 1.9e-14 | 3.6e-08 | 2.8e-08 (7 zero-input calls) |

Label law of the first measurement (Heis first segment, register z0): the
exact backend gives the uniform law on the three canonical words for the
13 subgroups not containing the centre and the point mass at 0 for the 6
containing it; the explicit backend is within total variation 2.18e-3
resp. 2.1e-14 of it (bounded, as it must be, by the state distance plus
prune_err). In every row the measured distance is below the proved budget,
by a factor 2.2-2.5 on the rows with a general call. The source rows show
directly that the zero-input calls contribute only the prep error: the
computed distance is at round-off level and the dropped mass bounds the
rest by 5e-8, consistent with 4 x 1.19e-8 resp. 7 x 4.06e-9 proved.

What was NOT simulated, and why. (i) No complete terminal sample was
simulated with the explicit backend. Each general call leaves a
phase-estimation tail of norm ~0.1 spread over ~10^4-10^5 basis states of
the pool (column "max support" of Section 3.1), and with a shared pool the
next general call acts on every branch, so the support multiplies: the Heis
first segment already has 591948 basis states (one general call); the next
top source would multiply that by 81 and its general call again by
~10^4. With a fresh pool per call the support multiplies the same way. (ii)
The n4 grade-2 instrument (two top coordinates, so two general calls in
sequence on the shared pool) did not finish in 300 s even at t = 3 and was
dropped. (iii) The merges, the grade-d `Q` transforms and the final readout
were not simulated with the explicit backend; the merges contain no
transform, and the `Q` transforms are zero-input calls (covered by the
proved prep term), while the final readout calls are general calls covered
by B. (iv) The exact Z[zeta_p] engines were not run on explicit circuits
(they do not apply). End to end, the explicit backend is therefore covered
by the proved composition of Section 4, not by a monolithic simulation.

## 4. End to end: composition bound and recoveries

**Proposition (hybrid composition; proved, given qft-mod Theorem 6 and the
arithmetic block correctness already assumed there).** Fix a generated
terminal-sample circuit with K transform calls, and defer its mid-circuit
measurements (copy each measured qubit into a fresh register by CNOT and
measure at the end; this does not change the joint outcome law). Let
U_k be the call with the exact transform (pool untouched) and V_k the
emitted lem:qft-mod slice, and let psi_k be the state just before call k in
the circuit whose calls 1..k-1 are exact. Then
||psi_explicit - psi_exact (x) |0>_pool|| <= sum_k ||(V_k - U_k (x) I) psi_k||.
Proof: telescope over H_j = (calls > j explicit)(calls <= j exact); the
gates between calls are unitaries, identical in both circuits, and act
trivially on the pool. In psi_k the pool is |0> (it is touched only by
calls, all exact so far, and the arithmetic macros return the shared
`arith` register to 0 on every input) and the called qudit is supported
on canonical words (every exact-backend state is), so qft-mod Theorem 6
gives ||(V_k - U_k (x) I) psi_k|| <= B, for every entanglement with the
rest (the bound is an operator-norm bound on C_N (x) |0>, tensored with the
identity). If the qudit is untouched before call k, psi_k = |0>_qudit (x)
rest and the term is the prep error exactly (Section 3.1). The joint law
of all measurement outcomes of one terminal sample is then within total
variation distance delta <= that sum of the exact one. A seeded run of
`run_algorithm` uses n = m + 4 terminal samples and classical feed-forward
between them; coupling each sample's outcome with the exact one gives
P(explicit run != exact run) <= n delta. The call structure (and so delta)
does not depend on the witnesses or the measured labels.
**Zero-input classification is an exact computation on the gate list**
(`qft_call_inputs`: no earlier gate touches the qudit).

Budgets per terminal sample (`recoveries.json`):

| config | calls (zero / general) | params | proved delta | float delta (sigma_upper / col 0) | n | proved P(run differs) |
|---|---|---|---|---|---|---|
| Heis(F_3) | 18 / 6 (3 `qft_dg` instrument, 3 `qft_final`) | (7, 7, 28) | 1.329 | 0.6885 | 7 | vacuous (1) |
| Heis(F_3) | 18 / 6 | target (22, 17, 14), eta = 5.52e-3 | 0.01135 | not simulated | 7 | 0.0795 |
| n4(F_5) | 124 / 24 (20 `qft_dg` instrument, 4 `qft_final`) | (8, 8, 28) | 4.835 | 2.830 | 8 | vacuous (1) |
| n4(F_5) | 124 / 24 | target (28, 20, 16), eta = 1.06e-3 | 0.01104 | not simulated | 8 | 0.0883 |

Recoveries. The exact backend (ArithBuilder + exact `qft{p}`, sparse engine
`run_algorithm_sparse`) recovers log(H) in all 38 seeded runs on Heis(F_3)
(19 subgroups x seeds 20261103, 20261104) and all 9 on n4(F_5) (9 subgroups,
seed 20261103). With the explicit backend at the target parameters, each of
these runs is reproduced, outcome for outcome, except with probability at
most 0.0795 (Heis) resp. 0.0883 (n4), by the proposition; so each such
explicit run recovers log(H) with probability >= 0.92 resp. >= 0.91.
At the simulation parameters the proved and the float budgets both exceed
1/n, so no recovery statement follows there. No run of the algorithm was
executed on the explicit circuits themselves (Section 3.2 says why).
The target values B used here are the proved formula `error_bound`
evaluated at (22, 17, 14) and (28, 20, 16); those two parameter sets were
not simulated (one call would need ~10^7-10^9 basis states).

## 5. Limits

1. Not a monolithic simulation: end to end, only the proved composition
   of Section 4 covers the explicit circuits; the simulated pieces are the
   single calls, one complete quantum segment of Heis(F_3) (19 subgroups),
   the first n4(F_5) top source (3 subgroups) and the grade-c instrument
   blocks. The n4(F_5) grade-2 instrument was not simulated.
2. The composition uses B = qft-mod Theorem 6, which rests on the
   ripple-carry adder and multiplier being correct for all widths
   (exhaustive there only for widths <= 6 and the listed N); p = 3, 5 are
   inside the exhaustively checked range.
3. Gate set Gamma_kappa (Phase(2 pi/2^k) and controlled versions with
   k <= max(r, tp)), not a fixed finite set; no Clifford+T synthesis.
4. Shared pool: the pool is reused dirty (up to the lemma's error); this is
   what the bound charges. `pool="fresh"` exists only for accounting.
5. Counts are exact for these two configurations only; nothing asymptotic
   is claimed, and at these primes the transform's constant (~420 b^2 per
   call) dominates.
6. The explicit backend uses the ArithBuilder arithmetic only (not the
   original value-controlled increments).
7. Unchanged: classical SDE solve between segments, Chevalley-Warning
   arities, no coherent receiver, oracle cost T_f not counted.

## 6. Claim gates and flags

All claim gates stay False and were not touched
(`coherent_receiver_implemented`, `general_sde_implemented`,
`formal_compiler_checked`, `independent_review`, `novelty_established`,
`speedup_claim_allowed`; asserted in `test_status_gates_stay_false`).
`research/reductions/rees_hsp_reduction.json` was not edited. New module
flags in `WIRE_STATUS`: `explicit_qft_backend_available` = True (optional;
`default_backend_unchanged` = True), `fixed_finite_gate_set` = False,
`monolithic_explicit_simulation` = False. The flags of the existing
modules are unchanged (`ARITH_STATUS["qft_poly_log_p_implemented"]` and
`rees_qft_mod.STATUS["rees_generator_uses_this_qft"]` stay False, since
those modules were not edited; the test asserts this).

## 7. Targets from the lemma statement alone (`lemma_level.json`)

The targets of Sections 2 and 4 evaluate the error terms of qft-mod
Theorem 6 exactly. A reader of the paper has only the statement of
`lem:qft-mod` (each call <= eta) plus the prep bound
3 pi 2^-tau <= eta/(b+3) for zero-input calls (qft-mod Lemma 1 at the
Corollary-8 tau). Using only these, delta <= eta (n_zero/(b+3) + n_general),
and eta = 0.1 / (n (n_zero/(b+3) + n_general)) gives:

| config | eta | (t, r, tau) | delta (lemma level) | n | P(run differs) <= | qubits | transform gates | total gates (excl. oracle) | per call |
|---|---|---|---|---|---|---|---|---|---|
| Heis(F_3) | 1.488e-3 | (26, 19, 15) | 0.01411 | 7 | 0.0987 | 154 | 188952 | 231210 | 7873 |
| n4(F_5) | 2.799e-4 | (32, 22, 18) | 0.01117 | 8 | 0.0894 | 835 | 1968844 | 2997844 | 13303 |

(The exact-formula budgets at these parameters are 0.00456 and 0.00556.)
These are the numbers used in the proposed text below.

## 8. Proposed replacement text for "Gate-level control" (AI-checked, pending human review)

Current text (main.tex, paragraph `Gate-level control`, re-read
2026-11-04; the line number moves as the integrator edits):

> In both backends $\mathrm{QFT}_{\Fp}$ is one exact $b$-qubit unitary, so
> the circuits as a whole remain a small-$p$ synthesis and do not realise
> the $\poly(\log p)$ transform of~(iii). Lemma~\ref{lem:qft-mod}
> constructs that transform separately (...), and it is not wired into
> these circuits.

Proposed replacement for those two sentences (uses only existing labels
`lem:qft-mod` and the paper's `\file` macro; numbers from Sections 2-4, 7):

```latex
In these two backends $\mathrm{QFT}_{\Fp}$ is one exact $b$-qubit unitary, a small-$p$ synthesis. A third, optional backend, \file{theorems/rees_circuit_qft_wire.py} (report \file{research/audits/reviews/2026-11-04-rees-qft-wire.md}; finite computation, AI-checked, pending human review), uses the binary arithmetic above and replaces every transform and every inverse transform by the circuit of Lemma~\ref{lem:qft-mod} on that qudit, a pool of $4b+2t+1$ ancillas shared by all transforms and the $3b+5$ arithmetic ancillas, so that every gate is $X$, CNOT, Toffoli, SWAP, $H$, $R_k^{\pm1}$ or $\mathrm{C}R_k^{\pm1}$ with $k\le\max(r,\tau)$; each emitted transform is checked gate by gate against the gate list of the lemma. By a hybrid argument over the transforms, with the measurements deferred, the state of one terminal sample then differs from that of the circuit with exact transforms by at most the sum, over the transforms, of $\eta$ for a transform whose input is not $|0\rangle$ and of the preparation error $3\pi 2^{-\tau} \le \eta/(b+3)$ of the proof of Lemma~\ref{lem:qft-mod} for one whose input is $|0\rangle$ (on input $|0\rangle$ the phase and phase-estimation steps of that proof are exact). On the Heisenberg group over $\mathbb{F}_3$ ($24$ transforms per terminal sample, $6$ of them on inputs other than $|0\rangle$) with $\eta = 1.5\cdot10^{-3}$, and on the class-three filiform algebra over $\mathbb{F}_5$ below ($148$ transforms, $24$ of them on inputs other than $|0\rangle$) with $\eta = 2.8\cdot10^{-4}$, a seeded run with $7$ resp.\ $8$ terminal samples therefore agrees with the run with exact transforms, outcome for outcome, except with probability below $0.1$. One terminal sample then uses $154$ qubits and $231210$ gates, $188952$ of them in the transforms, resp.\ $835$ qubits and $2997844$ gates, $1968844$ of them in the transforms, excluding the oracle. These circuits are not simulated as a whole. Single transforms, the first quantum segment over $\mathbb{F}_3$ for all $19$ subgroups, the first top source over $\mathbb{F}_5$ and the top-grade instruments are simulated gate by gate in floating point over all their qubits at smaller $t$, and differ from the circuits with exact transforms by at most $0.6$ times the proved bounds.
```

And, in the last sentence of the same paragraph, replace
"These are fixed finite instances with an exact Fourier transform and a
classical solve between quantum segments." by:

```latex
These are fixed finite instances, simulated exactly only with the exact Fourier transform (the explicit transform is covered by the bound above), with a classical solve between quantum segments.
```

Checks on the proposed text. "At most 0.6 times the proved bounds": the
largest simulated ratio sigma_upper/B over the single calls is 0.594 (p = 5,
t = 10); the others are 0.518, 0.523, 0.525, 0.442 (p = 3) and 0.585, 0.434
(p = 5); the composites give 0.42, 0.43, 0.39; zero-input rows are at
round-off against bounds of ~1e-8. "Below 0.1" is 0.0987 resp. 0.0894
(Section 7). The prep bound $3\pi 2^{-\tau}$ is the first term of the
current proof of `lem:qft-mod` in main.tex; the parenthetical fact that the
phase and phase-estimation steps are exact on input |0> is NOT yet in that
proof (it is argued in Section 3.1 here) and should either be added to the
proof as one sentence or the zero-input refinement dropped, in which case
every transform costs eta and the targets become eta = 0.1/(n K) with
K = 24 resp. 148 (Heis 5.95e-4, n4 8.45e-5; counts not computed here).

The sentence "Lemma~\ref{lem:qft-mod} ... is not wired into these circuits"
should be deleted, and the earlier clause "so the circuits as a whole
remain a small-$p$ synthesis and do not realise the $\poly(\log p)$
transform of~(iii)" is replaced by the new sentences. No `.tex` file was
edited in this pass.

## 9. Tests and artifacts

* `tests/test_rees_circuit_qft_wire.py`: 11 tests, 11 passed in 31.5 s
  (default backend equals the original generator gate for gate and is
  restored after the context; explicit terminal sample structure, counts,
  zero-input classification and gate set; count-only = full emission;
  fresh pool; a corrupted rotation in a qft slice is rejected; per-call
  error <= B and col 0 = prep; the simulator reproduces the exact source
  permutation; instrument block and both Heis prefixes within the hybrid
  budget; budgets monotone in eta; n4 counts).
* Related existing suites, run together with the new file:
  `tests/test_rees_qft_mod.py`, `test_rees_circuit_arith.py`,
  `test_rees_circuit_general.py`, `test_rees_circuit_sparse.py`,
  `test_rees_circuit.py`: 239 passed, 33 skipped (the REES_SLOW tests),
  0 failed, in 158 s. No existing file was modified.
* Folder `research/audits/reviews/2026-11-04-rees-qft-wire/`: `run_all.py`
  (jobs counts, per_call, heis_composite, n4_composite, recoveries; each
  writes `JOB.json` and `JOB.log`), `lemma_level.py` / `lemma_level.json`
  (Section 7). Run times: counts 6.5 s, per_call 63 s, heis_composite 166 s,
  n4_composite 147 s, recoveries 4.7 s.

Next step for the paper owner: decide whether to add the one-sentence
zero-input fact to the proof of `lem:qft-mod` (Section 8) and then paste
the proposed text; human review of Section 4's composition argument.
