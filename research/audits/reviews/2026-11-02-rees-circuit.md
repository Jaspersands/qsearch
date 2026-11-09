# Rees HSP: gate-level circuit on Heis(F_3), simulated in Qiskit (campaign 2, item 11)

2 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
Labels: **[exact]** = complete finite computation with integer/permutation arithmetic;
**[float]** = complex floating point (Aer statevector or `qiskit.quantum_info.Operator`),
tolerance 1e-9; **[argued]** = reasoning, not machine-checked.

Files written (and nothing else): `theorems/rees_circuit.py`, `tests/test_rees_circuit.py`,
this report. `theorems/rees_end_to_end_sim.py` is imported read-only (cover, oracle tables,
dense reference backend, brute-force SDE solver). The full-run JSON is outside the repo,
since only these three paths are in my row; rerun it with the second command below.

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit.py
```
```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m theorems.rees_circuit --out rees_circuit_report.json
```

The tests (36) passed in 57-107 s; the full report took 82 s, on a machine at load average
about 40 shared with the other sessions. `git status --short` changed only by my files; the
other new paths belong to sibling sessions. No claim gate, registry or shared state file was
touched.

**Result in one line.** For all 19 subgroups of Heis(F_3), 12 of them non-normal, the
compiled circuit gives exactly the paper's intermediate states. That holds on every
positive-probability label triple and every valid witness, 3198 branch/witness cases in all,
and 57/57 seeded runs recover log H. Primitive counts per terminal sample equal the
compilation note's formulas: 6 oracle calls, 12 BCH passes, 24 QFT_3, 3 controlled right
actions. There are 12 bracket evaluations against the paper's unoptimized bound of 48. One
terminal sample is 82 qubits (45 with reuse) and 5528 CNOTs, excluding the oracle.

## 1. Instance and encoding

- L = Heis(F_3), [x, y] = z, class c = 2, evaluation points s = 1, 2. The cover from
  `rees_end_to_end_sim.make_cover` is A = tL + t^2[L, L], dims (g_1, g_2) = (3, 1), so
  G_2 = (A, *) has order 81 with coordinates (a1, a2, a3 | a4 = t^2 z), and
  G_1 = F_3^3 is abelian. BCH on G_2 is u * v = u + v + 2[u, v] with [u, v]_4 = u1 v2 - u2 v1.
- Merge arity M_2 = kappa_2 g_2 + 1 = 3 (Chevalley-Warning), as in the item-10 simulator.
  Schedule 1's B_2(1) = 64 is **not** used (M = 2 fails: lambda = (1, 1) has no nonzero
  solution of s1^2 + s2^2 = 0 over F_3).
- All 19 Lie subalgebras h of Heis(F_3) are tested (1 trivial, 13 lines, 4 planes through z,
  the whole algebra); 12 of them (the lines other than <z>) are non-normal.
- **Encoding choice.** Qiskit 2.3 circuits are qubit-only (no qudit wires), so each F_3
  coordinate is a qubit pair, v = b0 + 2 b1, with 11 as padding. This is also how a real
  compile would encode F_p. A qudit-aware simulator would not add evidence: what is under
  test is the binary gate list. Arithmetic uses only X, CX, MCX (up to 3 controls) and SWAP,
  so it is an exact permutation of basis states. QFT_3 is one exact two-qubit unitary
  F_3 + [1] (padding fixed); it transpiles to 3 CX + 8 u. Labels are 5-bit binary
  registers written by XOR, matching the input contract U_f|g, y> = |g, y xor f(g)>. The
  oracle is a table-built gate (MCX on the 6 input qubits per set label bit). Its gates
  are T_f, so they are not counted.

## 2. The circuit (`theorems/rees_circuit.py`)

Per terminal sample (one descent tree), in order:

1. **Source**, three times (`source_circuit`, 24 qubits). QFT_3 on the 4 address qutrits.
   For s = 1, 2: compute E_s(a) = (s a1, s a2, s a3 + s^2 a4) into a 3-qutrit workspace,
   make the coherent oracle call U_f(workspace, label_s), then uncompute E_s. The labels are
   discarded.
2. **Complete central instrument**, three times (`instrument_circuit`). QFT_3 on an
   ancilla qutrit, controlled central subtraction a4 -= z (R_z|x> = |x z^-1>, the paper's
   convention), inverse QFT_3, measure lambda.
3. **Classical SDE.** Solve s1^2 l1 + s2^2 l2 + s3^2 l3 = 0 (brute force, from item 10).
   The merge is then emitted for that classical witness. This is classical feed-forward:
   the quantum circuit after the measurement depends on the record.
4. **Merge** (`merge_ops`, 24 qubits per target). QFT_3 on the 3-qutrit Q register. Then,
   on each target with s_i != 0, the controlled right translation
   x -> x * g, g = -delta_s(sigma(q)) = (-s q1, -s q2, -s q3, 0), with the four-pass
   schedule of thm:uniform-compilation(ii):
   - pass 1: b += [x, g]_4 into a 1-qutrit bracket workspace (compute);
     then copy W += x + g + 2b into a fresh 4-qutrit scratch W;
   - pass 2: b -= [x, g]_4 (uncompute). Now W = x * g, out of place, with no garbage;
   - swap x and W, so x = x * g and W = old x = x_new * g^-1;
   - pass 3: b += [x_new, -g]_4, then W -= x_new - g + 2b, which erases W;
   - pass 4: uncompute b.
   sigma (zero top coordinate) and delta_s are public linear maps folded into the
   controls; slots with s_i = 0 get no gates and the target is discarded.
5. **Readout** (`fourier_circuit("qft_final")`). QFT_3 on each Q qutrit, then measure.
   The F_3-nullspace of the samples is returned as log H.

`terminal_sample_circuit` assembles all of this into one `QuantumCircuit`: 82 qubits,
no register reuse, oracle calls as opaque `U_f` gates, 12 measurements.

## 3. How it is simulated, and why this is exact

The assembled 82-qubit circuit (45 qubits with register reuse) is far beyond statevector or
density-matrix simulation. Each module is simulated exactly from its own gate list, and
the modules are composed by two identities. Both identities are checked on the gate list,
not assumed.

- **Source:** the circuit is 4 QFT_3 on |0> followed only by permutation gates (the
  E_s passes and the table oracle; any other gate raises), so its output is
  (1/9) sum_a |pi(a, 0)>, with pi evaluated bit by bit on all 81 addresses. This gives
  the reduced address density and P(workspace = 0) exactly. [exact] An Aer statevector
  run of the same 24-qubit circuit agrees to 1.4e-17 on three subgroups. [float]
- **Instrument and readout:** the exact `Operator` of the circuit (10 and 6 qubits), with
  the ancilla projected onto each lambda. [float]
- **Merge:** the gate list has only X/CX/MCX/SWAP (any other gate raises), so it is a
  permutation of basis states. It is evaluated bit by bit on **all** 27 x 81 canonical
  inputs (q, x) with zero scratch. [exact] An Aer statevector run of Q preparation plus
  merge on a random target state matches it to 1e-8, with clean scratch (tests, both s).
  [float]
- **Composition 1:** the three sources sit on disjoint registers, so their joint state is
  a tensor product, and the instrument acts on each one separately. [argued; registers
  disjoint by construction]
- **Composition 2:** no merge gate targets a Q qubit (checked: `q_never_targeted`). So
  each merge is sum_q |q><q| (x) U_q, and its channel on Q is the Schur multiplier
  T_i[q, r] = tr(U_q rho_i U_r^dagger). With uniform Q, the output is
  |Q|^-1 prod_i T_i (entrywise), which is the formula in the proof of prop:descent.
  [exact identity; the structural premise is checked]

## 4. Checks and results (all 19 subgroups)

| Check | Result | Label |
|---|---|---|
| Merge gates = BCH x * (-delta_s(sigma(q))) on all 2187 canonical inputs, s = 1, 2 | yes | exact |
| Merge scratch W and b return to 0 on all canonical inputs; Q unchanged; output canonical | yes | exact |
| Aer statevector merge = bit-level merge (random targets, s = 1, 2) | max diff 5e-17, scratch P(0) = 1 | float |
| Source address density = rho of exp(h~) (dense reference backend), every H | 19/19 | exact gate evaluation; float comparison |
| Aer statevector source = bit-level source (H = 1, a line, H = G) | max diff 1.4e-17 | float |
| Source E_s workspace returns to \|0> with probability 1, every H | 19/19 | float |
| Padding weight after source and after instrument | < 1e-14 | float |
| Label law uniform on K_2^perp; each conditioned state = reference Pi rho Pi / p | 19/19 | float |
| For EVERY positive-probability label triple and EVERY valid witness, merge output = rho_(H_1) | 3198 cases, all equal | float |
| Readout law uniform on h^perp; nullspace of its support = log H | all cases | float |
| Seeded runs from oracle access (7 samples, 3 seeds per H) recover log H | 57/57 | float |

Here H_1 = exp(t h) on G_1 = F_3^3. This is all of h, including the non-normal lines,
not just its image modulo [L, L].

## 5. Resource counts

Primitive counts for one terminal sample (witness with all s_i nonzero), from the
circuit's own counters, against the table in
`research/REES_UNIFORM_INSTRUMENT_COMPILATION.md` ("Primitive Counts") at c = 2, M_2 = 3,
r_2 = 1, D_1 = 3, D_2 = 4, n = dim L = 3, m = 1 sample:

| Primitive | Circuit | Note formula | Value |
|---|---|---|---|
| Coherent oracle calls | 6 | c L | 6 |
| E_s compute / uncompute passes | 6 / 6 | c L | 6 |
| Leaf QFT_3 | 12 | D_c L | 12 |
| Grade-2 QFT_3 (instrument 2 per target, plus Q preparation) | 9 | v_2(2 M_2 r_2 + D_1) | 9 |
| Final QFT_3 | 3 | n per sample | 3 |
| Central coordinate subtractions | 3 | v_2 M_2 r_2 | 3 |
| Controlled right actions | 3 | v_2 M_2 = L + T - m | 3 |
| BCH passes | 12 | 4 v_2 M_2 | 12 |
| Bracket evaluations | 12 | 4 v_2 M_2 B(2), B(2) = 4 | 48 (upper bound) |

Every count is equal except the brackets. The paper's B(d) = (d-1)d(d+1)(d+2)/6 is the
unoptimized ODE schedule, and class-two BCH needs one bracket per pass, so 12 <= 48 is
consistent with thm:uniform-compilation(i). A full run with 7 terminal samples multiplies
each count by 7 (42 oracle calls).

Gate-level counts (oracle excluded; transpiled to {cx, u} at optimization level 1):

| Module | Qubits | Logical gates | cx | u | depth |
|---|---|---|---|---|---|
| Source (no oracle) | 24 | 4 QFT_3, 64 CX, 64 Toffoli | 440 | 574 | 379 |
| Instrument | 10 | 2 QFT_3, 4 CX, 4 Toffoli | 32 | 51 | 57 |
| Merge, s = 1 | 24 | 8 SWAP, 128 CX, 64 Toffoli, 64 C3X | 1362 | 1572 | 1663 |
| Merge, s = 2 | 24 | same | 1370 | 1567 | 1662 |
| Q preparation / readout | 6 | 3 QFT_3 | 9 | 24 | 7 |
| **One terminal sample, assembled** | **82** | 24 QFT_3, 24 SWAP, 588 CX, 396 Toffoli, 192 C3X, 12 measure | **5528** | **6647** | **5103** |

Width: 82 qubits without reuse. With reuse it is 45: three addresses, Q, W, b and one
5-bit label register, with the E_s workspace in W, the instrument ancilla in b, and
labels measured and reset. At most 4 group registers are live (3 targets + Q), which is
the bound 2 + (M_2 - 1) of thm:uniform-compilation(iv).

## 6. Negative controls (the checks can fail)

All from `negative_controls()` in the full report, over all 19 subgroups:

| Broken variant | What the checks report |
|---|---|
| One evaluation point (s = 1 only) | Source wrong for exactly the 13 subgroups with z not in h, which is prop:single-evaluation (wrong iff [G, G] not <= H) |
| E_s workspace not uncomputed | Workspace never returns to 0 (19/19). The address state is wrong for 18/19; for H = 1 the source is already I/81, so only the workspace check sees it |
| Bennett uncompute (pass 2) dropped from the merge | `scratch_clean_all_inputs` = False |
| Nonzero NON-witness scales | Wrong merge output in 468 cases for each of the 12 lines that meet the centre trivially. 0 cases for H = 1 (output is I/27 whatever the scales) and for H containing z (every label is 0, so no non-witness exists) |

**Qiskit/Aer traps found on the way** (recorded for other sessions):
(1) In Qiskit 2.x the default `transpile` (optimization level 2) elides SWAP gates by
relabelling qubits. A statevector read with the original layout is then silently wrong.
It showed up as P(scratch = 0) = 0.013. Every simulation transpile here uses
`optimization_level=0`, and the gate-count transpile (level 1) asserts a trivial final
layout. (2) Aer's `save_density_matrix` on a subsystem of a 24-qubit state took about 65 s,
against about 9 s for `save_statevector` plus a numpy partial trace. (3) Aer's
`initialize` on 8 qubits of a 24-qubit circuit did not finish in 10 minutes;
`set_statevector` took 20 s.

## 7. What this establishes and what it does not

Establishes, for this one instance [float/exact as labelled above]: an explicit binary gate
list implements every quantum step of the Rees algorithm. These are the two coherent
evaluation-point oracle calls with uncomputed workspaces, the complete central
instrument, the witness-driven controlled right action compiled as the four-pass Bennett
BCH schedule, and abelian Fourier sampling. Simulated exactly, it reproduces the paper's
intermediate states and recovers log H for every subgroup of Heis(F_3), including the 12
non-normal ones. Its primitive counts match the compilation note's formulas exactly, and
its bracket count is within the paper's bound.

Does **not** establish:
- anything asymptotic: the size is polynomial only by the written argument of
  thm:uniform-compilation, and one instance at p = 3 cannot test that;
- Schedule 1 or any of the three schedules (the arity is the Chevalley-Warning 3, the
  solver is brute force, and the solve is classical feed-forward between quantum segments);
- QFT approximation (QFT_3 is an exact unitary; Kitaev/Cleve-Watrous synthesis and the
  eta budget of thm:uniform-compilation(iii) are not exercised), noise, or the oracle cost T_f;
- a monolithic simulation of the 82-qubit circuit: the modules are composed by the two
  identities of Section 3;
- the identity-on-padding convention of the compilation note: the arithmetic preserves
  the canonical subspace and is correct on it (checked), but it permutes padding words
  arbitrarily. The note's restricted-domain hybrid says this is enough, but it is a
  deviation from the note's stated P_u;
- a coherent receiver in the sense of the claim gate: no scalable generator, no proof
  that the circuit family is correct for all (G, H), no hardware run.

## 8. Exact statement that now holds

For L = Heis(F_3), evaluation points 1, 2, merge arity 3, and every one of the 19 subgroups
H of G = (L, *): the Qiskit gate lists in `theorems/rees_circuit.py`, simulated exactly as in
Section 3 (float tolerance 1e-9), produce lifted sources equal to rho of exp(h~) with clean
evaluation workspaces. They produce central labels uniform on K_2^perp. For every
positive-probability label triple and every nonzero witness of s1^2 l1 + s2^2 l2 + s3^2 l3 = 0,
the merge output equals rho_(exp(t h)). The readout is uniform on h^perp, so its
annihilator is log H. The compiled controlled right translation equals
x -> x * (-delta_s(sigma(q))) on every canonical input, with scratch returned to zero. The
primitive counts per terminal sample are 6 oracle calls, 12 BCH passes, 12 brackets and
24 QFT_3, against the note's 6, 12, <= 48 and 24.

Still missing: a scalable circuit generator for general (L, c, p), with tests at c >= 3;
an implemented Schedule 1 arity and solver inside the circuit flow; finite-gate QFT
synthesis at larger p; identity-on-padding arithmetic, if the note's convention is
kept; and human review.

Claim gates that must stay false: `coherent_receiver_implemented`,
`general_sde_implemented`, `formal_compiler_checked`, `independent_review`,
`novelty_established`, `speedup_claim_allowed`. None was touched.

## 9. Proposed paper text

Target: `main.tex`, Section~\ref{sec:uniform-compilation}, a new paragraph right after the
proof of Theorem~\ref{thm:uniform-compilation} (before `\subsection{Reproducible Resource
Profiles}`). Status: exact finite computation; AI-checked, pending human review.

```latex
\paragraph{Gate-level control.} The artifact \file{theorems/rees_circuit.py} (report \file{research/audits/reviews/2026-11-02-rees-circuit.md}) compiles the whole procedure on the smallest instance, the Heisenberg group over $\mathbb{F}_3$ with evaluation points $1,2$ and merge arity $3$, into an explicit Qiskit circuit. Each $\mathbb{F}_3$ coordinate is a qubit pair, arithmetic uses only $X$, CNOT, Toffoli and three-control Toffoli gates, and $\mathrm{QFT}_{\mathbb{F}_3}$ is one exact two-qubit unitary. The circuit makes the two coherent oracle calls per source with uncomputed evaluation workspaces, applies the complete central instrument, and implements the controlled right translation $x \mapsto x \ast (-\delta_s(\sigma(q)))$ with the four BCH passes of~(ii), followed by abelian Fourier sampling. One terminal sample uses $82$ qubits without register reuse ($45$ with reuse) and $6$ oracle calls, $12$ BCH passes, $12$ bracket evaluations (the bound in~(i) gives $48$) and $24$ Fourier transforms; it transpiles to $5528$ CNOTs, excluding the oracle. The modules are simulated exactly and composed through the tensor and Schur-product structure of Proposition~\ref{prop:descent}. For all $19$ subgroups, $12$ of them nonnormal, every source equals the coset density of $\exp(\hlift)$ with clean workspace, every label law is uniform on $K_2^\perp$, and for every label triple and every valid witness the merge output is exactly $\rho_{\exp(t\hh)}$, so the readout recovers $\hh$. This is one fixed instance with an exact Fourier transform and a brute-force classical solve between quantum segments; it is not a coherent receiver for general $(G,H)$, and it tests no asymptotic cost.
```

The macros `\file`, `\hlift` and `\hh` are already used in `main.tex`. If the
integrator uses the counts, they should be regenerated from `resource_report()`, not
retyped.
