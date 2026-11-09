# Rees HSP receiver simulations: monolithic runs at c = 2, 3; exhaustive merges at class four; n5(F_7) and class five

5 November 2026 (session started 4 November, evening). AI-only session (Claude Code, Opus 5.5).
Not human review, not Lean. **Every claim below is a finite computation, AI-checked, pending human review.**
Labels: **[exact]** = complete finite computation in integer, permutation or Z[zeta_p] arithmetic;
**[sampled]** = exact on a stated random subset only; **[argued]** = reasoning, not machine-checked.

Files written (nothing else was edited; main.tex untouched; nothing committed; no network):
- `theorems/rees_circuit_mono.py` (new): monolithic simulation of the assembled coherent terminal sample;
- `theorems/rees_circuit_exhaustive.py` (new): exhaustive merge checks by an exact reduction;
- `tests/test_rees_circuit_mono.py`, `tests/test_rees_circuit_exhaustive.py` (new);
- this report and the folder `research/audits/reviews/2026-11-05-rees-receiver-sims/` (run JSONs, logs,
  `run_commands.sh`, pytest outputs).

Read-only imports: `rees_circuit_coherent.py` (TerminalSample, MergeBlock, flatten), `rees_circuit_general.py`,
`rees_circuit_sparse.py` (SparseEngine), `rees_circuit_arith.py`, `rees_coherent_sde.py`, `rees_end_to_end_sim.py`.
The claim gate `coherent_receiver_implemented` stays false (both new STATUS dicts keep it false; tests check this).
`research/reductions/rees_hsp_reduction.json` was not touched.

## 0. Answers

| Item | Done | Instances and counts |
|---|---|---|
| (c) monolithic, c = 2 | yes | Heis(F_3), all 19 subgroups (12 non-normal); 182 qubits, 115 282 gates, 24 exact QFT_3, 6 oracle calls per terminal sample; 574 terminal samples, 82 of 82 seeded runs recover log H |
| (c) monolithic, c = 3 | 7 of 9 subgroups | n4(F_5), every non-normal one of the 9 (5); 1198 qubits, 2 694 596 gates, 176 exact QFT_5, 36 oracle calls per terminal sample; 56 terminal samples, 7 of 7 runs recover log H. Not run: gamma_2 and <e1+e2,e3> (one factor would hold 4.9e7 rows) |
| (a) exhaustive class four | yes | n5(F_5), all 9 subgroups of the family (5 non-normal), grades 4, 3 and 2 all exhaustive (every label tuple, every witness), source from its gate list on all 5^11 addresses; 18 of 18 seeded runs recover log H |
| (b) n5(F_7), class four | 8 of 9 subgroups | all 5 non-normal; every grade exhaustive; source = exact coset density, its gate list sampled; 16 of 16 seeded runs recover log H. Not run: gamma_2 (7^9 rows) |
| (b) class five | 7 of 8 subgroups | n6(F_7), [e1,e_i] = e_(i+1), i = 2..5, arities (M_5, M_4, M_3, M_2) = (2, 5, 10, 9); 5 non-normal; every grade exhaustive; no seeded runs. Not run: gamma_4 = <e5,e6> |

Tests: 26 new tests pass in 37.6 s; all 21 `tests/test_rees_circuit*.py` files: 278 passed, 25 skipped in 534 s (Section 5).

## 1. (c) Monolithic simulation of the coherent terminal sample

### 1.1 What is simulated

The object is the coherent-label terminal sample of `rees_circuit_coherent.TerminalSample`: the backend that
measures nothing before the final Fourier sampling. Its `items` list (sources, instruments, coherent SDE circuits
U_SDE, witness-controlled BCH merges, U_SDE^-1, Q preparation, final QFT and readout) is flattened, macro by macro,
into the `rees_circuit_arith` X/CX/CCX/SWAP gate lists. Then **every item is executed in program order on one joint
state of all the qubits** (182, resp. 1198):
- every X, CX, CCX and SWAP;
- every exact QFT_p and QFT_p^dagger;
- every table-oracle call U_f|w>|y> = |w>|y xor f(w)>;
- the readout.

No module is simulated on its own, and nothing is composed through the tensor and Schur-product structure of
prop:descent. The labels and witnesses are computed by the gates themselves (U_SDE acts on the label wires in the
joint state), and so are the merges and the reduced states.

**Representation [exact].** The state is a product of factors. Each wire is either:
- a classical constant shared by all branches (e.g. clean workspace), or
- a column of exactly one factor. A factor is a sparse superposition sum_r a_r |bits_r>, with a_r in Z[zeta_p]
  (an integer coefficient vector) and the bits stored bit-sliced.

The factors are updated as follows:
- a gate across two factors forms their tensor product;
- a wire constant over its factor is split off;
- a rational common divisor of a factor's amplitudes is divided out (probabilities are ratios);
- QFT_p groups the rows that agree off the register (exact `np.unique` keys) and sums zeta^(+-xy) a_r.

Overflow is guarded (|coefficient| < 2^52, never hit).

**Deferred measurement [argued, standard; schedule checked].** A register may be measured in the computational
basis once every later item uses its wires only as controls of CX/CCX gates: never as a target, and never inside a
QFT, an oracle output or a measurement. Such a measurement commutes with every later gate (each later gate is block
diagonal in that register's basis), so the joint law of all later outcomes is unchanged. `measurement_schedule`
computes the points from the flattened gate list and re-verifies the condition. There are three levels:
- **level 0:** nothing is measured before the readout. The computed readout law is the exact output law of the
  whole circuit.
- **level 1:** only registers no later item touches at all are measured: oracle outputs after their call, and
  children and their labels after the parent's merge.
- **level 2:** level 1, plus each instrument label right after its QFT_p^dagger. In both instances the label
  wires are afterwards used only as CX controls inside U_SDE and U_SDE^-1 (120 resp. 864 such uses; checked).

At levels 1 and 2 the measurements are **sampled** with their Born weights (floats computed from the exact
amplitudes). One run is therefore one quantum trajectory, and its readout sample has exactly the circuit's output
law. The trajectory's final conditional readout law is computed **exactly** in Z[zeta_p] and compared with the
uniform law on h^perp. Every one of the 1198 (resp. 182) wires is accounted for: the arithmetic ancillas, the
evaluation workspace w and the block-workspace pool end as the constant 0 in every trajectory.

Cost per terminal sample, estimated before the runs and then measured:

| | qubits | gates | QFT | oracle | largest factor (estimate -> actual) | time per sample |
|---|---|---|---|---|---|---|
| Heis(F_3), level 2 | 182 | 115 282 | 24 | 6 | <= 27·81 rows -> 2 187 | 0.05-0.5 s |
| Heis(F_3), level 1 | 182 | 115 282 | 24 | 6 | -> 531 441 | <= 1.8 s |
| Heis(F_3), level 0 | 182 | 115 282 | 24 | 6 | 729^3 = 3.9e8 for small S -> run only where <= 8e6 | 0.4-0.5 s |
| n4(F_5), level 2 | 1198 | 2 694 596 | 176 | 36 | 5^6·5·\|S\| (Q uniform on G_2 times one child) -> 7.8e4 .. 9.8e6 | 2.2 s (\|S\| = 1, 5) .. 88 s (\|S\| = 625) |

The binding cost is the top merge. The register Q is uniform on G_2 (5^6 = 15 625 rows) and must be multiplied
with one child, a coset of S = exp(h~) of |S| rows. For gamma_2 (|S| = 3125) and <e1+e2,e3> (|S| = 15 625) that
product has 4.9e7 rows x 93 wires (about 2.5 GB of state plus a transient of the same size). It was not attempted.

### 1.2 Results

**Heis(F_3), c = 2** (`mono_heis_f3.json`, `mono_heis_f3_level0.json`). Coherent arity M_2 = 3, points (1, 2),
19 subgroups (12 non-normal), 7 terminal samples per seeded run.

| level | subgroups | runs (seeds) | terminal samples | recovered | every conditional law exactly uniform on h^perp | workspace clean | peak rows | wall time |
|---|---|---|---|---|---|---|---|---|
| 2 | 19 | 38 (2 seeds) | 266 | 38/38 | yes | yes | 2 187 | 17 s |
| 1 | 19 | 38 (2 seeds) | 266 | 38/38 | yes | yes | 531 441 | 38 s |
| 0 | 6 of 19 | 6 | 42 | 6/6 | yes: the **exact output law** of the whole circuit | yes | 19 683 | 3 s |

Level 0 ran for the six normal subgroups containing Z (|S| >= 9). For them the oracle outputs take few values, and
the whole 182-qubit circuit fits with nothing measured before the readout. Its exact output law is uniform on
h^perp. For the other 13 subgroups a level-0 factor would hold 3^18 = 3.9e8 rows (101-107 wires); they were skipped.

**n4(F_5), c = 3** (`mono_n4_f5.json`). Coherent arities (M_3, M_2) = (2, 6), points (1, 2, 3), level 2, seed
20261105, 8 terminal samples per run.

| H | normal | \|S\| | recovered | 8/8 conditional laws exactly uniform on h^perp | workspace clean | peak rows | s (8 samples) |
|---|---|---|---|---|---|---|---|
| <e2> | no | 5 | yes | yes | yes | 78 125 | 18 |
| <e1> | no | 5 | yes | yes | yes | 78 125 | 20 |
| <e1+e3> | no | 5 | yes | yes | yes | 78 125 | 19 |
| <e2,e4> | no | 625 | yes | yes | yes | 9 765 625 | 704 |
| <e2,e3> | no | 125 | yes | yes | yes | 1 953 125 | 155 |
| Z(G) | yes | 125 | yes | yes | yes | 1 953 125 | 135 |
| trivial | yes | 1 | yes | yes | yes | 78 125 | 18 |
| <e1+e2,e3> | yes | 15 625 | not run (factor 4.9e7 rows x 93 wires) | | | | |
| gamma_2 = <e3,e4> | yes | 3 125 | not run (same) | | | | |

Whole run: 1081 s wall, peak RSS 2.2 GB. Per terminal sample the counts are those of the coherent report:
36 oracle outputs, 24 labels and 18 children are measured (level 2). Program compilation takes 1.0 s.

**Negative controls (tests).**
- A merge block without the Bennett uncompute (`skip_bennett`) leaves garbage, and readouts outside h^perp appear.
- Measuring the root Q right after its preparation (a register later used as a target) breaks exact uniformity on
  h^perp, and the schedule verifier would reject it.
- The `g_sign` mutation is **not** visible in the readout law on Heis trajectories. Plausibly this is the
  relabelling q -> q^-1 of the uniformly prepared Q, under which h^perp is invariant [argued, not checked]. The
  coherent backend's block checks catch it.
- The factor simulator equals a dense statevector, up to a global scalar, on 6 random 9-qubit X/CX/CCX/SWAP/H
  circuits and on a mod-3 arithmetic program with exact QFT_3 (17 qubits).

### 1.3 What 1 does not show

- No level-0 (fully coherent) run at c = 3, or for the 13 Heis subgroups with small S.
- Levels 1 and 2 give exactly simulated **sampled** trajectories, not the law averaged over all trajectories.
  Exactness holds per trajectory.
- The two n4 subgroups with the largest S were not run.
- The transforms are the exact QFT_p unitaries, not the circuit of lem:qft-mod (the explicit-transform circuit of
  `rees_circuit_full.py` is not what is simulated here).
- The early-measurement equivalence is the standard deferred-measurement argument. It is checked on the gate list,
  not proved in Lean.

## 2. (a) Exhaustive merges at class four, n5(F_5)

**Reduction.** In the sparse module-by-module mode, the merges at grade d (arity M) cover
(p^M - 1)|K_d^perp|^(M-1) pairs of (label tuple, witness). For n5(F_5) at grade 2 that is up to 2.98e17 pairs, so
direct exhaustion is impossible. `rees_circuit_exhaustive.py` covers all of them with three exact checks plus a
five-line argument:
- **(E1) [exact]** The label law is uniform on K_d^perp.
- **(E2) [exact, every label]** Every conditioned branch phi_lam has the support of phi_0 and equals
  zeta^(e_lam) phi_0 row by row, with e_lam = sum_j c_j W_j linear in lam = sum_j c_j b_j over a basis b of
  K_d^perp. Also, phi_0 is constant on its support.
- **(E3) [exact, every value set]** Take every nonempty set T of nonzero scalars with |T| <= M. The zero-label
  merge with witness values T (each once, and once with a value repeated up to arity M) equals rho_(H_(d-1)). On
  its support, the vectors t^(-d) W(delta_t g) (t in T) coincide.
- **(R) [argued]** For labels lam_i = sum_j c_ij b_j and a witness s with value set T,
  F = prod phi_lam_i o delta_si = F_0 · zeta^(sum_ij c_ij W_j(delta_si g)). By (E3), W_j(delta_si g) =
  s_i^d tau_j(g) on supp F_0, so the exponent is sum_j tau_j sum_i s_i^d c_ij = 0 by the witness equation. Hence
  every pair's merge output is the zero-label output, which by (E3) is rho_(H_(d-1)).

**Cross-checks.**
- 60 direct merges per grade on random witness pairs agree.
- 6 non-witness controls per grade are rejected.
- On Heis(F_3) (all 19 subgroups), direct exhaustion of all 234 pairs gives the same verdict (test).
- With the wrong power t^(-(d-1)), the phase test fails on a real subgroup (test).
- The covered-pair counts at grades 4 and 3 for H = 1 and <e2> equal the direct exhaustive counts of
  2026-11-03-rees-circuit-3 (1 952 500 and 77 500).

**Run** (`exhaustive_n5_f5.json`; 3284 s wall, peak RSS 1.7 GB). Points 1..4, CW arities (M_4, M_3, M_2) =
(5, 3, 7).
- For every subgroup the source was evaluated from its gate list on all 5^11 = 48 828 125 addresses. It equals the
  coset density of exp(h~), with clean workspace and fibres that are left cosets.
- The merge gate lists are proved equal to the BCH right translation (prove_merge, d = 2, 3, 4, s = 1..4; 12 of
  12).
- Each grade input below the top is the exact rho_(H_d), which (E1)-(E3) show is every merge output.

| H | normal | source s | grade 4 pairs | grade 3 pairs | grade 2 pairs | all exhaustive | readout uniform on h^perp | seeded runs |
|---|---|---|---|---|---|---|---|---|
| trivial | yes | 80 | 1 952 500 | 77 500 | 2.98e17 | yes | yes | 2/2 |
| <e1> | no | 142 | 1 952 500 | 77 500 | 2.98e17 | yes | yes | 2/2 |
| <e2> | no | 148 | 1 952 500 | 77 500 | 2.98e17 | yes | yes | 2/2 |
| <e3> | no | 195 | 1 952 500 | 77 500 | 1.91e13 | yes | yes | 2/2 |
| Z(G) = <e5> | yes | 348 | 3 124 | 3 100 | 1.91e13 | yes | yes | 2/2 |
| <e2,e5> | no | 355 | 3 124 | 3 100 | 1.91e13 | yes | yes | 2/2 |
| <e1+e2+e5> | no | 118 | 1 952 500 | 77 500 | 2.98e17 | yes | yes | 2/2 |
| gamma_3 = <e4,e5> | yes | 466 | 3 124 | 124 | 1.22e9 | yes | yes | 2/2 |
| gamma_2 = <e3,e4,e5> | yes | 611 | 3 124 | 124 | 78 124 | yes | yes | 2/2 |

The grade checks take 0.1-1 s, except gamma_3 and gamma_2 at grade 4 (14 s and 460 s, input supports 5^7 and 5^9).
Each seeded run uses 9 terminal samples, 945 top sources from the gate-list source, 3780 oracle queries and
classical SDE solves.

**What (a) does not cover.**
- "Every subgroup" means the nine subgroups of the family N5_SUBGROUPS, not all subalgebras of n5(F_5).
- The merges are the Schur-product channel fed by the proved merge gate lists (as before), not a gate-level
  simulation at class four.
- (R) is an argument, not a machine check.

## 3. (b) n5(F_7) at class four, and a class-five instance

A gate-list source on all 7^11 = 2.0e9 addresses (n5(F_7)) or 7^16 (n6(F_7)) was out of reach: about 16 GB for the
key array alone. So the top state is the **exact coset density of exp(h~)** computed by linear algebra.

The source gate list is checked **[sampled]**: run bit-level on 2^14 random addresses x, on x·s for random s in
exp(h~) and on x·u for random u not in exp(h~). The key must be constant on the S-translates and separate the
others, the address must come back, and the workspace must be clean. This passed for every run subgroup.

Everything else is as in Section 2:
- instrument exponents from the instrument gate lists (exact);
- merge gate lists proved by prove_merge;
- exhaustive merges by (E1)-(E3) and (R).

**n5(F_7), class four** (`exhaustive_n5_f7.json`; 1568 s, peak RSS 2.3 GB). CW arities (M_4, M_3, M_2) =
(3, 7, 7); prove_merge d = 2, 3, 4, s = 1..6: 18 of 18 proved.

| H | normal | grade 4 pairs | grade 3 pairs | grade 2 pairs | exhaustive | seeded runs |
|---|---|---|---|---|---|---|
| trivial | yes | 16 758 | 1.14e16 | 1.34e21 | yes | 2/2 |
| <e1> | no | 16 758 | 1.14e16 | 1.34e21 | yes | 2/2 |
| <e2> | no | 16 758 | 1.14e16 | 1.34e21 | yes | 2/2 |
| <e3> | no | 16 758 | 1.14e16 | 1.14e16 | yes | 2/2 |
| Z(G) = <e5> | yes | 342 | 9.7e10 | 1.14e16 | yes | 2/2 |
| <e2,e5> | no | 342 | 9.7e10 | 1.14e16 | yes | 2/2 |
| <e1+e2+e5> | no | 16 758 | 1.14e16 | 1.34e21 | yes | 2/2 |
| gamma_3 = <e4,e5> | yes | 342 | 823 542 | 9.7e10 | yes | 2/2 |
| gamma_2 = <e3,e4,e5> | yes | not run: \|exp h~\| = 7^9 = 4.0e7 rows; grade-4 conditioning would need ~2.8e8 keys | | | | |

Each seeded run uses 9 terminal samples, 1323 top sources and 5292 oracle queries; brute-force SDE at grade 4, IS or
brute force elsewhere. The generated circuits have 16 302 qubits per terminal sample (original arithmetic; counted
in 2026-11-03-rees-circuit-2) and were not simulated at the gate level.

**n6(F_7), class five** (`exhaustive_n6_f7.json`; 613 s, peak RSS 3.4 GB). The algebra is [e1,e_i] = e_(i+1),
i = 2..5, with cover dims (6, 4, 3, 2, 1), |G_5| = 7^16, points 1..5 and CW arities (M_5, M_4, M_3, M_2) =
(2, 5, 10, 9). prove_merge d = 2..5, s = 1..6: 24 of 24 proved. At d = 5 the reference polynomial is the checked
right-nested BCH form, not the independently written NilGroup formula used for d <= 4.

| H | normal | grade 5 | grade 4 | grade 3 | grade 2 | exhaustive |
|---|---|---|---|---|---|---|
| trivial | yes | 336 | 9.7e10 | 1.86e31 | 4.46e34 | yes |
| <e1> | no | 336 | 9.7e10 | 1.86e31 | 4.46e34 | yes |
| <e2> | no | 336 | 9.7e10 | 1.86e31 | 4.46e34 | yes |
| <e3> | no | 336 | 9.7e10 | 1.86e31 | 7.7e27 | yes |
| Z(G) = <e6> | yes | 48 | 4.0e7 | 4.6e23 | 7.7e27 | yes |
| <e2,e6> | no | 48 | 4.0e7 | 4.6e23 | 7.7e27 | yes |
| <e1+e2+e6> | no | 336 | 9.7e10 | 1.86e31 | 4.46e34 | yes |
| gamma_4 = <e5,e6> | yes | not run: \|exp h~\| = 7^9 rows | | | | |

Readout is uniform on h^perp in every run row. **No seeded runs at class five.** The classical SDE solve at
grade 3 (M = 10, 7^10 brute force) exceeds the existing solver's brute-force cap unless the IS column count is
met. This was not attempted.

**Resource note.** A first n6 attempt enumerated all 7^10 witness vectors in the direct cross-check. Its memory
footprint reached about 61 GB (compressed, swapped) before I killed it (my own process only). The fix samples
witness pairs by solving for the last label. The stale `/usr/bin/time` lines of that killed run sit in the middle of
`exhaustive_n6_f7.out`. The valid run's own lines are at the end: 613 s real, max RSS 3.4 GB, macOS peak footprint
13.6 GB.

**What (b) covers and does not cover.**
- *Covered:* instrument and merge gate lists at p = 7, class four and class five; exhaustive merge coverage at every
  grade; recovery from the exact source (class four).
- *Not covered:*
  - the source gate list on all addresses (sampled only);
  - any gate-level or monolithic simulation at p = 7 or class five;
  - gamma_2 (n5(F_7)) and gamma_4 (n6(F_7));
  - seeded runs at class five;
  - any coherent-label (kappa >= 3) circuit at class five.

## 4. Times (loaded machine, load average ~45-75 on 10 cores, at most two of my processes at once, nice 10)

| run | wall | peak RSS |
|---|---|---|
| mono Heis levels 1, 2 (2 seeds) | 55 s | 0.4 GB |
| mono Heis level 0 | 3 s | small |
| mono n4(F_5) level 2 | 1081 s | 2.2 GB |
| exhaustive n5(F_5), gate-list sources | 3284 s | 1.7 GB |
| exhaustive n5(F_7) | 1568 s | 2.3 GB |
| exhaustive n6(F_7) | 613 s | 3.4 GB |

## 5. Tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_mono.py tests/test_rees_circuit_exhaustive.py --durations=5
```
Output (`pytest_new.out`): `26 passed in 37.56s` (slowest: schedule verification 12.8 s, Heis recovery levels 1-2
7.0 s, n4 trajectories 4.3 s).

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit*.py --durations=8
```
Output (`pytest_circuit_all.out`): `278 passed, 25 skipped, 12 warnings in 533.67s (0:08:53)`. This covers all
existing circuit tests (general, sparse, arith, coherent, coherent_k3, coherent_c4, full, qft_wire, rees_circuit)
plus the two new files. The skips are the existing REES_SLOW tests. This run predates the last edit to
`rees_circuit_exhaustive.py` (the witness-sampling fix and its n5(F_7) test). The new-file run above includes that
edit.

## 6. Claim gates that must stay false

None was touched:
- `coherent_receiver_implemented`: these are finite simulated instances with the exact QFT, and no generator for
  the receiver of prop:coherent-receiver exists;
- `general_sde_implemented`, `formal_compiler_checked`, `independent_review`, `novelty_established`,
  `speedup_claim_allowed`.

## 7. Proposed paper text (finite computation, AI-checked, pending human review)

**(i) Coherent-label backends paragraph.** After the sentence "Over $\mathbb{F}_3$ the whole circuit is simulated
exactly, module by module, for all $19$ subgroups, and its merge block on all $3^{18}$ basis inputs." insert:

> The assembled terminal sample is also simulated as one state of all its qubits (\file{theorems/rees_circuit_mono.py}, report \file{research/audits/reviews/2026-11-05-rees-receiver-sims.md}; finite computation, AI-checked, pending human review): every gate, every exact transform and every oracle call acts in program order on one exact sparse state over $\mathbb{Z}[\zeta_p]$, kept as a product of factors, and no module is simulated separately. A register is measured early only once every later gate uses it as a control at most, which leaves the output law unchanged; these measurements are sampled, so each run is one trajectory whose final readout law is computed exactly. Over $\mathbb{F}_3$ ($182$ qubits, $115282$ gates, $24$ transforms, $6$ oracle calls), for all $19$ subgroups, the readout law of every one of $574$ simulated terminal samples is exactly uniform on $\hh^\perp$ and all $82$ seeded runs recover $\hh$; for the six normal subgroups containing the centre nothing is measured before the readout, so this is the exact output law of the whole circuit. Over $\mathbb{F}_5$ ($1198$ qubits, $2694596$ gates, $176$ transforms, $36$ oracle calls) the same holds for all $56$ terminal samples of seven of the nine subgroups, the five nonnormal ones included, and all seven seeded runs recover $\hh$; the other two, $\gamma_2(\mathcal{L})$ and $\langle e_1+e_2,e_3\rangle$, need a factor of $4.9\cdot10^7$ basis states and were not run.

**(ii) Instances paragraph.** Replace "The checked merges are all label tuples with all their witnesses at grades
four and three for two subgroups, the trivial one and $\langle e_2\rangle$, and sampled tuples and witnesses
otherwise; at grade two they are sampled for every subgroup. One seeded run per subgroup from oracle access recovers
$\hh$. The class-four circuits over $\mathbb{F}_7$ ($16302$ qubits per terminal sample with the original arithmetic,
$16316$ with the binary arithmetic and its $3b+5=14$ ancillas) are generated and counted." by:

> For all nine subgroups every label tuple with every witness is covered at grades four, three and two, that is $(p^{M_d}-1)|K_d^\perp|^{M_d-1}$ pairs at grade $d$, up to $3.0\cdot10^{17}$ at grade two (\file{theorems/rees_circuit_exhaustive.py}, report \file{research/audits/reviews/2026-11-05-rees-receiver-sims.md}; finite computation, AI-checked, pending human review): it is checked exactly that every conditioned branch is $\zeta^{e_\lambda}\phi_0$ with $\phi_0$ the zero-label branch and $e_\lambda$ linear in $\lambda$, and that for every set $T$ of nonzero witness values the zero-label merge is $\rho_{H_{d-1}}$ and the twists $t^{-d}e(\delta_t g)$, $t\in T$, agree on its support; the witness equation then cancels the phase of every pair, and direct merges on samples agree. Two seeded runs per subgroup from oracle access recover $\hh$. The class-four circuits over $\mathbb{F}_7$ ($16302$ qubits per terminal sample with the original arithmetic, $16316$ with the binary arithmetic and its $3b+5=14$ ancillas) are generated and counted, and are simulated in the sparse mode at the arities $(M_4,M_3,M_2)=(3,7,7)$ from the coset density of $\exp(\hlift)$, computed by linear algebra (the source gate list is checked on sampled addresses only): for eight of the nine subgroups, the five nonnormal ones included, every grade is covered in the same way and two seeded runs each recover $\hh$; $\gamma_2(\mathcal{L})$ ($7^9$ states) was not run. The same coverage holds at class five, for $[e_1,e_i]=e_{i+1}$ ($i=2,\dots,5$) over $\mathbb{F}_7$ with arities $(M_5,M_4,M_3,M_2)=(2,5,10,9)$, for seven of eight subgroups, five of them nonnormal, without seeded runs.

**(iii) Scope paragraph.** After "Every exact simulation uses the exact Fourier transform;" insert:

> the monolithic simulation of \file{theorems/rees_circuit_mono.py} samples the trajectories of the early measurements and covers the coherent-label circuits over $\mathbb{F}_3$ and $\mathbb{F}_5$ only;

**Also to update (not paper text).** REES_FULL_CONTINUATION.md item 7, "Still missing: exhaustive class-four
merges, n5(F_7) or class five, and a monolithic (not module-by-module) simulation". All three now exist with the
limits above. What remains:
- level-0 coverage and the two largest subgroups at c = 3;
- gate-list sources and gate-level simulation at p = 7 and class five;
- seeded runs at class five.
