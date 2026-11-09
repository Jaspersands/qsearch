# Rees HSP: a coherent-label receiver backend for Heis(F_3) and n4(F_5)

4 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
**Status: AI-checked, pending human review.** Labels: **[proved]** = written argument here;
**[proof-by-computation]** = exhaustive check over ALL inputs of the stated finite set;
**[sampled]** = exact on a stated subset only; **[exact count]** = counted from the emitted
program (macro counts times the per-macro gate counts of `rees_circuit_arith`);
**[exact]** = exact integer / Z[ζ_p] arithmetic; **[argued]** = reasoning, not machine-checked.

Scope: the two instances whose SDE grades all have κ_d = gcd(d, p−1) ∈ {1, 2}:
Heis(F_3) (class 2; grade 2 has κ = 2, g_2 = 1) and n4(F_5) (class 3, p = 5 ≡ 2 mod 3;
grade 3 has κ = 1, g_3 = 1; grade 2 has κ = 2, g_2 = 2). New files only:
`theorems/rees_circuit_coherent.py`, `tests/test_rees_circuit_coherent.py`, this report and
the artifact folder `research/audits/reviews/2026-11-04-rees-circuit-coherent/`.
Read-only imports: `rees_circuit_general` (configs, instances, source circuits, exact Engine,
BCH nodes, symbolic polynomials), `rees_circuit_arith` (macro gate lists), `rees_coherent_sde`
(κ = 1 witness circuit, bit-sliced simulator), `rees_coherent_sde_k2` (κ = 2 witness circuit).

This report is written incrementally; sections are appended as they are finished.

## 1. Design

**What changes against the measured-label generator.** In `rees_circuit_general.
terminal_sample_circuit` every central instrument ends with a measurement of its ancilla z
(the label λ ∈ F_p^{g_d}); the SDE Σ_i s_i^d λ_i = 0 is solved classically and the merge
gate list for that classical s is emitted (slots with s_i = 0 get no gates). In the coherent
backend nothing is measured before the final Fourier readout:

1. *Labels stay coherent.* The instrument (QFT_p on z, a_top −= z, QFT_p^{−1} on z) is the
   same gate list, and its z register is not measured: it becomes label column i of the
   parent's merge block.
2. *Coherent witness.* U_SDE, the permutation circuit of `rees_coherent_sde` (κ_d = 1,
   columns g_d+1) or `rees_coherent_sde_k2` (κ_d = 2, columns (g_d+1)(g_d+2)/2), is applied
   with its input registers mapped onto the M label registers. It writes the canonical witness
   s(λ) into a witness register S (b qubits per column) and returns its own workspace to 0.
3. *Controlled merge.* For each child i = 1..M (all of them; a child with s_i = 0 gets the
   identity, see Lemma 2 below): compute the register G = −δ_{s_i}(σ(q)) coordinatewise,
   G_j = −s_i^{deg j} q_j (powers s^2..s^{d−1} by products, then one product per
   coordinate), run the four-pass BCH right translation x_i ← x_i * G of `merge_ops` with the
   classical coefficient −s^{deg j} q_j replaced by the register G_j (same macro sequence,
   same node set), and uncompute G and the powers. This is "δ_s controlled on the witness
   register", built from the `add_product` / `add_scaled` macros only.
4. *Uncompute the witness.* Apply U_SDE^{−1} (the reversed gate list). The merge reads S
   and the labels but never writes them, so S and the SDE workspace return to 0.
5. The Q register then carries the grade-(d−1) source; at d−1 ≥ 2 its own instrument label
   stays coherent too, and at d−1 = 1 the final QFT_p and measurement are the only
   measurement of the whole terminal sample.

**What is uncomputed and what is garbage.** Uncomputed to |0⟩ (and reused by the next merge
block): the witness registers S, the whole SDE workspace (copies, pivots, flags, roots), the
register G and the powers of s, the BCH workspace W and bracket registers, the arithmetic
ancillas. Left as garbage, never touched again by any later gate: every label register z
(it is entangled with its child, and its child has been translated, so the instrument can
no longer be inverted), every child register x_i after its merge (the "consumed and
discarded" targets of `prop:descent`), and the source's oracle output registers (as in the
measured generator). Garbage is traced out; Section 2 proves that this gives the same
reduced state on every surviving register as the measured version.

**Arity.** The κ = 2 solver needs M = (a+1)(a+2)/2 columns (a = g_2). Heis(F_3): a = 1,
M_2 = 3, equal to the generator's Chevalley–Warning arity κa+1 = 3, so nothing changes.
n4(F_5): a = 2, **M_2 = 6 instead of 5**; M_3 = g_3+1 = 2 is unchanged (κ_3 = 1). Hence
N_3 = M_3·M_2 = 12 top sources per terminal sample instead of 10, i.e. 36 oracle calls
instead of 30. This is the owner decision flagged in the κ = 2 report (§0, §5): the
paper's counts (`rem:triangular-scope`) stay at the CW arity and are not changed here.

**One wire layout, one simulator.** Everything is emitted as integer-wire programs in the
format of `rees_coherent_sde` (gate tuples X/CX/CCX/SWAP plus `add_product` / `add_scaled`
macro items, expanded by `rees_circuit_arith`), so a merge block is one permutation gate
list that the bit-sliced simulator runs on all its wires.

## 2. Equivalence with the measured version (deferred measurement)

Notation for one merge block at grade d with arity M: child registers X_1..X_M (G_d
coordinates), label registers Z_1..Z_M (F_p^{g_d}), Q (G_{d−1}), witness S, workspace Wk
(SDE workspace, G, powers, W, bracket registers, arithmetic ancillas), and Γ = every other
register (oracle outputs, earlier garbage, other subtrees). R_g x = x * g on G_d (the BCH
product), g(s, q) = −δ_s(σ(q)), and V_λ = Σ_q |q⟩⟨q|_Q ⊗ ⊗_i R_{g(s_i(λ), q)} on (Q, X),
where s(λ) is the canonical witness of the coherent SDE circuit.

**Lemma 1 (block action) [proved, from the cited results and the checks below; plus
proof-by-computation at Heis(F_3)].** On every canonical basis input with S = Wk = 0, the
block gate list B maps |λ⟩_Z |ξ⟩_X |q⟩_Q |0⟩_{S,Wk} to |λ⟩_Z (V_λ|ξ⟩|q⟩)_{X,Q} |0⟩_{S,Wk}.

*Proof.* B = U_SDE · Π_i (C_i · K_i · C_i^{−1}) · U_SDE^{−1} read left to right (C_i: compute G
and the powers from S_i and Q; K_i: the BCH translation of X_i by the register G).
(a) U_SDE maps |λ⟩|0⟩_S|0⟩ ↦ |λ⟩|s(λ)⟩|0⟩ on every canonical λ: Theorem 5 of the κ = 2 report
and Lemma 2 / Section 4 of the κ = 1 report (conditional there on the arithmetic macros above
p = 13, which is not needed here: p ∈ {3, 5}); re-checked inside the block on all 27 (Heis) and
25 (n4 grade 3) label tuples (`sde_exhaustive`), and at n4 grade 2 the κ = 2 report's run on
all 5^12 label tuples applies (the same gate list, wires relabelled). (b) For every s, q, x,
C_i K_i C_i^{−1} maps (s, q, x, 0) ↦ (s, q, x * g(s, q), 0): `prove_controlled_merge` replays
the macro program over F_p[s, q, x] and compares x with the classical BCH polynomial
`sym_bch_reference` (written independently of the node derivation), G, powers, W and bracket
registers with 0, s and q with themselves. Equality of formal polynomials implies equality
on all canonical inputs, given that each macro gate list realises its declared map on canonical
inputs (proof-by-computation for p ≤ 13 in the I146 report, which covers p = 3, 5). Proved for
Heis grade 2 (30 macros), n4 grade 2 (48) and n4 grade 3 (82). (c) Footprints
(`block_structure`): U_SDE writes only S and SDE workspace; C_i K_i C_i^{−1} writes only X_i and
merge workspace and reads only X_i, S_i, Q and merge workspace; children are disjoint. The
merge workspace lives on SDE workspace wires, which are 0 after U_SDE (Bennett-clean) and
are returned to 0 by (b). (d) Hence after the merges the (Z, S, SDE-workspace) wires are still
|λ⟩|s(λ)⟩|0⟩ and U_SDE^{−1} returns them to |λ⟩|0⟩|0⟩, untouched by the X, Q content. ∎

**Lemma 2 (zero witness entries) [proved; covered by (b)].** g(0, q) = 1 because every cover
coordinate has grade ≥ 1, so δ_0 kills it; hence R_{g(0,q)} = id. The coherent block runs all M
children, and a child with s_i = 0 is mapped by the identity, which is what the measured
generator does by emitting no gates for it. (The symbolic proof is over a free variable s, so
s = 0 is included.)

**Theorem 3 (same reduced state) [proved].** Let ρ be any state of (Z, X, Γ) at the start of a
merge block (labels not measured), with Q prepared as |u⟩ = |G_{d−1}|^{−1/2} Σ_q |q⟩ and
S = Wk = 0. Let D be the measured version: measure Z in the computational basis (outcome λ
with probability π(λ) = tr ⟨λ|ρ|λ⟩, post-state ρ_λ), apply the classical-witness merge for
s(λ) (the gate list V_λ on (Q, X)), keep the record λ. Then

  tr_Z [ B (ρ ⊗ |u⟩⟨u| ⊗ |0⟩⟨0|) B^† ] = Σ_λ π(λ) V_λ (|u⟩⟨u| ⊗ ρ_λ) V_λ^† ⊗ |0⟩⟨0|,

i.e. the coherent block, with the label registers traced out, equals the measured block with
its classical record discarded, on ALL other registers (Q, the consumed children X, Γ), not
only on Q. Every later gate of the terminal sample acts on registers other than the Z of this
block (checked on the assembled program: `garbage_never_touched_again`), so for any later
channel E, tr_Z((E ⊗ id_Z)(σ)) = E(tr_Z σ); by induction over the blocks in depth-first order,
the final state of the coherent terminal sample, traced over all label registers, equals the
measured terminal sample's final state averaged over all classical records, **provided the
measured version uses the same witness rule λ ↦ s(λ)**. The only measurement of the coherent
circuit is the final readout of the root Q, so the readout laws are equal.

*Proof.* By Lemma 1, B (· ⊗ |0⟩_{S,Wk}) = Σ_λ |λ⟩⟨λ|_Z ⊗ V_λ ⊗ 1_Γ (· ⊗ |0⟩). Write
ρ = Σ_{λ,λ'} |λ⟩⟨λ'| ⊗ ρ_{λλ'}. The output is Σ_{λ,λ'} |λ⟩⟨λ'| ⊗ V_λ(|u⟩⟨u| ⊗ ρ_{λλ'})V_{λ'}^† ⊗
|0⟩⟨0|, and tr_Z keeps the λ = λ' terms, ρ_{λλ} = π(λ)ρ_λ. The commutation of tr_Z with E is
the definition of the partial trace for E acting on the complement. ∎ (This is the
deferred-measurement principle, with the principle of implicit measurement for the garbage:
leaving Z, X unmeasured at the end is the same as measuring and discarding them.)

**Corollary 4 [proved, conditional on `prop:descent`].** `prop:descent` gives, for every
positive-probability label tuple and every valid witness, the merged output ρ_{H_{d−1}} on Q.
Hence the coherent terminal sample leaves ρ_{H_{d−1}} on every intermediate Q, ρ_{H_1} on the
root, and its readout law is the generator's (uniform on h^⊥) for any witness rule the
measured generator uses (IS or brute force). Moreover Q is independent of the label
registers (the conditional state given λ does not depend on λ); the Heis(F_3) simulation
checks this branch by branch.

What is *not* uncomputed and why. The labels Z cannot be uncomputed: inverting the
instrument would need the child register in its pre-merge state, but the child has been
translated by g(s(λ), q), which depends on Q. The children X are the consumed targets of
`prop:descent` and carry no information the readout needs. Both are garbage; Theorem 3 says
that exactly reproduces the measured version. Zero-probability label tuples have zero
amplitude, so the witness the circuit computes on them is irrelevant.

## 3. Counts per terminal sample [exact count]

From `TerminalSample(cfg).counts()` (the assembled program of one terminal sample, depth
first, no reuse of garbage, one shared pool for the clean block workspace). Gate set
X/CX/CCX/SWAP of `rees_circuit_arith` (every macro expanded with its own gate counts); QFT_p
is counted as calls of the exact b-qubit unitary (as in the generator's default backend); the
oracle U_f is excluded (calls listed). The measured-generator rows are
`rees_circuit_general.terminal_sample_circuit` under the same arithmetic backend
(`CountingArithBuilder`), with all merge slots active (witness all ones; a witness with zero
entries removes those slots' merge gates).

**Heis(F_3)** (p = 3, b = 2, M_2 = 3, N_2 = 3 sources):

| component | gates | CCX | macros (product / scaled) | QFT_3 calls |
|---|---|---|---|---|
| sources: E_s compute + uncompute | 12 192 | 2 880 | 0 / 48 | 12 |
| instruments (unmeasured), a_top −= z | 762 | 180 | 0 / 3 | 6 |
| Q preparation | 0 | 0 | — | 3 |
| coherent SDE U + U^{−1} (κ = 2, a = 1, M = 3) | 60 208 | 13 932 | 76 / 22 | 0 |
| witness control (G = −δ_s σ(q), compute + uncompute, 3 children) | 12 816 | 2 952 | 18 / 0 | 0 |
| BCH merge, 3 children | 29 304 | 6 816 | 24 / 48 | 0 |
| final Fourier readout | 0 | 0 | — | 3 |
| **total (coherent)** | **115 282** | **26 760** | 118 / 121 | **24** |
| measured generator (same backend) | 42 258 | 9 876 | 24 / 99 | 24 |

Qubits: **182** coherent (addresses 24, oracle outputs 30, labels 6, root Q 6, evaluation w 6,
arithmetic ancillas 11, block workspace pool 99 = witness S 6 + SDE workspace 93, with the merge
workspace G, W, bracket inside the SDE workspace) against **93** measured (+ 12 classical bits).
Oracle calls 6 in both.

**n4(F_5)** (p = 5, b = 3, M_3 = 2, **M_2 = 6**, N_3 = 12, N_2 = 6 sources):

| component | gates | CCX | macros (product / scaled) | QFT_5 calls |
|---|---|---|---|---|
| sources: E_s compute + uncompute (12 sources) | 239 640 | 61 224 | 0 / 504 | 84 |
| instruments (12 at grade 3, 6 at grade 2) | 11 424 | 2 928 | 0 / 24 | 48 |
| Q preparation (6 grade-2, 1 grade-1) | 0 | 0 | — | 40 |
| coherent SDE grade 3 (κ = 1, g = 1, M = 2), 6 blocks | 437 664 | 108 648 | 288 / 24 | 0 |
| coherent SDE grade 2 (κ = 2, a = 2, M = 6), 1 block | 702 932 | 174 668 | 460 / 44 | 0 |
| witness control grade 3 (12 children) | 248 544 | 61 488 | 168 / 0 | 0 |
| witness control grade 2 (6 children) | 71 040 | 17 568 | 48 / 0 | 0 |
| BCH merge grade 3 (12 children) | 772 980 | 192 792 | 384 / 432 | 0 |
| BCH merge grade 2 (6 children) | 210 372 | 52 536 | 96 / 144 | 0 |
| final Fourier readout | 0 | 0 | — | 4 |
| **total (coherent)** | **2 694 596** | **671 852** | 1 444 / 1 172 | **176** |
| measured generator, M_2 = 6 | 1 234 800 | 309 864 | 480 / 1 104 | 176 |
| measured generator, CW arity M_2 = 5 | 1 029 000 | 258 220 | — | 148 |

Qubits: **1 198** coherent (addresses 252, oracle outputs 360, grade-3 labels 36, grade-2 Q 108,
grade-2 labels 36, root Q 12, w 12, arithmetic ancillas 14, block workspace pool 368 =
the grade-2 block's S 18 + SDE workspace 350; the grade-3 block needs 65 of them) against
**890** measured at M_2 = 6 (+ 84 classical bits) and 758 at M_2 = 5. Oracle calls: 36 (30 at
the CW arity).

Reading the tables.
- The non-SDE, non-control part (sources, instruments, BCH merges) has exactly the measured
  generator's macro sequence (Heis 24 / 99, n4 480 / 1 104 macros; `test_counts_and_structure`).
  At Heis the gate counts are equal too (42 258); at n4 the coherent part is 384 gates smaller
  (1 234 416 against 1 234 800, all 384 of them CCX), because the measured merge multiplies by
  the classical constant −T·s^{deg} while the coherent one multiplies by −T and takes s^{deg}
  from the register G: the controlled constant loads of `add_product` depend on the bits of the
  constant.
- The coherent overhead per terminal sample is the SDE circuits plus the witness control:
  Heis +73 024 gates (+16 884 CCX), n4 +1 460 180 gates (+362 372 CCX; net +1 459 796 after the
  384 above), i.e. ×2.7 and ×2.2 the
  measured gate count at equal arity, and +89 / +308 qubits (the block workspace pool minus the
  measured version's W and bracket registers). The arity change at n4 costs, separately,
  +205 800 gates, +28 QFT calls, +132 qubits and +6 oracle calls against the CW arity.
- QFT_p is not synthesised here. With the explicit `lem:qft-mod` backend at the parameters of
  the QFT-wire report (Heis (t, r, t') = (7, 7, 28): 3 420 gates per call; n4 (8, 8, 28): 5 874)
  the QFT calls would add about 82 080 (Heis) and 1 033 824 (n4) gates and a shared QFT pool of
  4b+2t+1 = 23 / 29 qubits [cited from 2026-11-04-rees-qft-wire.md, not recomputed here].
- Per block (all wires): Heis grade 2 is 102 328 gates on 146 wires; n4 grade 3 is 243 198 gates
  on 145 wires; n4 grade 2 is 984 344 gates on 538 wires. The block gate count equals the length
  of the flattened gate list (`test_gate_counts_equal_emitted_lists`).

## 4. Simulations: what was and was not simulated

No monolithic statevector of a whole terminal sample was simulated: the Heis(F_3) coherent
circuit has 182 qubits and its state (before the readout) has up to ~10^10 nonzero basis
amplitudes; n4(F_5) has 1 198 qubits. Everything below is exact (bit-level permutations,
Z[ζ_p] amplitudes, rational probabilities). Artifacts: `run.json` / `run.log` (default CLI,
about 3 minutes) and `heis_block_exhaustive.json` / `.log` (13 minutes) in
`research/audits/reviews/2026-11-04-rees-circuit-coherent/`.

**4.1 Merge blocks on all their wires (basis-state simulation; a permutation, so basis
states suffice).** `block_check` loads labels, children and q, all other wires 0, runs the
whole block gate list (U_SDE, all controlled merges, U_SDE^{−1}) and asserts: labels and q
unchanged; every child equals x_i * (−δ_{s_i}(σ(q))) with s the canonical witness from the
independent reference (`canonical_witness_batch` / `canonical_witness_k2_batch`) and * from
`GroupLaw.mul`; the witness register S and every other wire 0; outputs canonical.

| block | gates | wires | inputs | label |
|---|---|---|---|---|
| Heis grade 2 (M = 3) | 102 328 | 146 | **all 3^18 = 387 420 489** joint (λ, x_1, x_2, x_3, q) | proof-by-computation |
| Heis grade 2 | 102 328 | 146 | 65 536 structured | sampled |
| n4 grade 3 (M = 2) | 243 198 | 145 | all 25 label pairs × all 15 625 q, one random child pair each (390 625) | sampled (x) |
| n4 grade 3 | 243 198 | 145 | 4 096 structured | sampled |
| n4 grade 2 (M = 6) | 984 344 | 538 | 4 096 structured (rank-deficient label tuples) | sampled |

All pass. Compositional proof pieces (all pass): U_SDE inside the block on all label tuples
at Heis (27) and n4 grade 3 (25) (`sde_exhaustive`); the controlled merge proved on all
canonical (s, q, x) by symbolic replay for the three blocks (`prove_controlled_merge`); the
footprints of `block_structure`. Mutations detected by `block_check`: flipping the sign of G,
dropping the uncompute of G, dropping U_SDE^{−1}, dropping the first Bennett pass.

**4.2 The assembled terminal-sample program (wiring).** `assembled_basis_paths` runs the
assembled program of one terminal sample (all sources, instruments, blocks with their real
global wires and the shared pool) bit-level on random basis paths: each QFT_p on a fresh
register is replaced by a random canonical basis value, qft_dg, the oracle and the readout
are skipped. An independent classical recursion predicts every register (a source address a
ends at (a·z^{−1}) * g(s_i, q), z central; the labels keep their values; the root Q is
unchanged; w, ancillas, pool and oracle registers end 0). Heis 16 384 paths, n4 1 024 paths
(`run.json`): all pass; a sign mutant of the witness control fails. This checks the wiring
of the assembled program, not its amplitudes; Section 4.3 does the amplitudes at Heis. The
structure checks of the same program: garbage (labels, merged children) is never touched
after its block, and the only measurement is the readout of the root Q, at the end.

**4.3 Heis(F_3): exact simulation of the whole coherent terminal sample, all 19
subgroups.** `heis_end_to_end` composes, exactly, every module of the circuit from its own
gate list: the three sources (the generator's source gate list under the poly(log p)
backend, run bit-level on all 81 addresses: address unchanged, evaluation workspace and
ancillas clean, label key per address), the three unmeasured instruments (QFT_3 is the exact
matrix of `qft_matrix`, checked by `_qft_ok`; a_top −= z run bit-level on all (x, z)), Q
prepared by QFT_3, the merge block (bit-level tables π^{(i)}_{λ,q} for every label tuple λ,
every q and every child value, from the block gate list; valid per child because 4.1 checked
all joint inputs), and the final QFT_3 on Q. The state is held in the exact factorised form

  Σ_λ |λ⟩_Z ⊗ |G_1|^{−1/2} Σ_q |q⟩ ⊗ ⊗_i R^{(i)}_{λ,q} φ^{λ_i},  φ^λ(x', y) = Σ_z ζ^{−λz}[y = key(x'z)],

which is exact because the children are disjoint registers until the block and the block is
block-diagonal in λ with S and the workspace returned to 0 (4.1). Then
ρ_Q[q, r] = |G_1|^{−1} Σ_λ Π_i ⟨R_r φ^{λ_i} | R_q φ^{λ_i}⟩ (scale |G_2|^{−M} p^{−2gM}), in Z[ζ_3]
with a rational scale, and P(k) = |G_1|^{−1} Σ_{q,r} ζ^{k·(q−r)} ρ_Q[q, r].

| check (all 19 subgroups, 12 non-normal) | result |
|---|---|
| reduced state on Q equals ρ_{H_1} = [q^{−1}r ∈ H_1]/27 exactly | 19/19 |
| every positive-probability label tuple: the conditional Q state ∝ ρ_{H_1} (labels uncorrelated with Q) | 19/19 (27 tuples for the 13 subgroups not containing the centre, 1 for the 6 containing it) |
| measured generator (exact Engine, labels measured, classical feed-forward of the same canonical s, mixture over all label tuples) equals ρ_{H_1} | 19/19 |
| readout law equals the generator's (uniform on h^⊥), total probability 1 | 19/19 |
| nullspace of the readout support = log H | 19/19 |
| seeded runs (m+4 = 7 samples from the exact readout law, two seeds) recover log H | 38/38 |

Non-vacuity: replacing child 1's tables by child 2's (wrong witness) breaks the reduced state
on 18 of 19 subgroups (the test asks for ≥ 10); leaving two children untranslated breaks it
on 13 of 19. A sign flip of G is invisible at this level (ρ_{H_1}[q, r] depends only on
whether r − q lies in the subgroup H_1, which is closed under negation); 4.1 detects it. The
independent review (§10) added more mutants: witness (1,1,1), permuted label tuples and left
instead of right translation fail on 12 of 19, an identity block on 18 of 19, and another
valid witness passes, as Corollary 4 predicts.

**4.4 n4(F_5): per merge, exact states, coherent witnesses.** The full circuit is out of
reach; `n4_state_checks` uses the measured generator's exact Engine (dense Z[ζ_5] states,
instrument kernels from the instrument gate list) with arity M_2 = 6, and takes the witness
of every merge from a bit-level run of the coherent SDE gate list remapped into the block
(`CircuitWitness`). By Theorem 3 the coherent reduced output of a merge is the π-mixture of
these outputs, so each checked output equal to ρ_{H_{d−1}} is a check of the coherent block
on that label tuple. For the 9 subgroups (5 non-normal):

| subgroups | grade 3 (M = 2) | grade 2 (M = 6) |
|---|---|---|
| ⟨e2⟩, ⟨e1⟩, ⟨e1+e3⟩, trivial (label support 5 / 25) | all 25 label pairs | 256 sampled 6-tuples of 25^6 = 2.4·10^8 |
| ⟨e2,e4⟩, ⟨e2,e3⟩, Z(G) (support 1 / 5) | all | **all 5^6 = 15 625** 6-tuples |
| ⟨e1+e2,e3⟩, γ_2 (support 1 / 1) | all | all (1) |

Every witness is valid (nonzero, Σ s_i^d λ_i = 0), every merged output equals ρ_{H_{d−1}}
exactly, and the readout is uniform on h^⊥: 9/9. Seeded runs with the coherent witness rule
(labels sampled from the exact laws, every witness from the circuit, 8 terminal samples, 288
oracle queries each): 18/18 recover log H. The coherent BCH gate list itself is not used
here; the Engine applies the right translation it was proved to equal (4.1, symbolic proof).

**Not simulated.** A monolithic statevector of either circuit; the n4(F_5) assembled circuit
at the amplitude level (only its wiring, 4.2, and its blocks, 4.1); n4 grade-2 label tuples
outside the samples for the four subgroups with label support 25; the n4 grade-2 block on
more than 4 096 joint inputs (the U_SDE part is exhaustive on all 5^12 label tuples in the
κ = 2 report); the explicit QFT backend; noise.

## 5. Limits

1. **κ_d ≥ 3 grades stay classical.** `coherent_arity` and `MergeBlock` refuse them
   (`coherent_config(filiform4(7))` raises: κ_3 = gcd(3, 6) = 3). So n4(F_7), n5(F_5) (κ_4 = 4)
   and every instance with a grade d and an odd prime q ≤ c dividing both d and p − 1 (or
   4 | gcd(d, p − 1)) keep a classical solve between quantum segments. The κ = 2 report §9
   lists what a κ = 3 circuit would need.
2. **Two instances only.** The backend is generic in the code (any Config whose grades all
   have κ_d ≤ 2: `coherent_config`), but only Heis(F_3) and n4(F_5) are built, counted and
   checked. The κ_d ≤ 2 condition for all grades is gcd(p − 1, lcm(2..c)) = 2 (κ = 2 report §5).
3. **Arity.** At κ = 2 the arity is (g_2+1)(g_2+2)/2, larger than the generator's 2g_2+1 when
   g_2 ≥ 2 (n4(F_5): 6 against 5; +6 oracle calls, +205 800 gates, +132 qubits per terminal
   sample even before the coherent overhead). The paper's arities and budgets are unchanged.
4. **Cost.** The coherent version is 2.2–2.7 times the measured gate count at equal arity,
   with +89 / +308 qubits, dominated by U_SDE and U_SDE^{−1} (the SDE circuit is applied twice
   per merge). No optimisation was attempted (e.g. sharing U_SDE^{−1} with the next block,
   batching the Fermat inversions, or keeping the witness and skipping U_SDE^{−1} entirely,
   which would leave S as more garbage).
5. **Exactness scope.** Exhaustive: the Heis block (all 3^18 joint inputs), the SDE circuits
   on all label tuples (Heis, n4 grade 3 here; n4 grade 2 in the κ = 2 report), the controlled
   merges symbolically. Sampled: the n4 blocks on joint inputs, n4 grade-2 label tuples for
   four subgroups. The macro gate lists are proof-by-computation for p ≤ 13 (I146), which
   covers p = 3, 5. Canonical inputs only; padding words are not claimed (they never occur).
6. **Not covered.** QFT_p synthesis (counted as exact unitaries; §3 cites the explicit
   backend's per-call cost), the oracle cost T_f, noise, depth, layout, any asymptotic claim.
   Theorem 3 is the textbook deferred-measurement argument applied to this circuit: it gives
   no capability the measured algorithm lacks.

## 6. Claim gates

`research/reductions/rees_hsp_reduction.json` is not edited; `coherent_receiver_implemented`
stays **false** (two finite instances, κ ≤ 2 only, not a receiver for general (G, H)).
`STATUS` of the new module: `coherent_receiver_implemented: False`,
`kappa_ge3_grades_coherent: False`, `general_instances: False`, `qft_synthesised: False`,
`independent_review: False`, `speedup_claim_allowed: False`; only
`coherent_label_backend_kappa_le2_instances: True`, scoped to Heis(F_3) and n4(F_5). No claim
of quantum advantage, of an asymptotic receiver cost or of a native application follows.

## 7. Proposed paper text (not applied; main.tex untouched)

In the "Gate-level control" paragraph of Section `sec:uniform-compilation`, replace
"(Lemmas~\ref{lem:coherent-linear-sde} and~\ref{lem:coherent-quadratic-sde}; none of the three
backends uses them)" by "(Lemmas~\ref{lem:coherent-linear-sde} and~\ref{lem:coherent-quadratic-sde};
only the fourth backend below uses them)", and insert after the sentence ending "…every gate is
$X$, CNOT, Toffoli, SWAP, $H$, $R_k^{\pm1}$ or $\mathrm{C}R_k^{\pm1}$ with $k\le\max(r,\tau)$;
each emitted transform is checked gate by gate against the gate list of the lemma." (or at the
end of the paragraph):

```latex
A fourth backend, \file{theorems/rees_circuit_coherent.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-coherent.md}; finite computation, AI-checked, pending human review), measures nothing before the final Fourier sampling on the Heisenberg group over $\mathbb{F}_3$ and the class-three filiform algebra over $\mathbb{F}_5$, where every grade has $\kappa_d\le2$: the instrument labels stay in registers, the circuits of Lemmas~\ref{lem:coherent-linear-sde} and~\ref{lem:coherent-quadratic-sde} write the witness into a register, the right translation by $-\delta_s(\sigma(q))$ is computed from that register and the witness is then uncomputed, while the labels and the consumed targets stay as garbage that no later gate touches, so by deferred measurement the reduced state is that of the measured circuit with the same witness rule, hence $\rho_{H_{d-1}}$ by Proposition~\ref{prop:descent}. With merge arity $(g_2+1)(g_2+2)/2$ at grade two ($3$, resp.\ $6$ instead of $5$), one terminal sample uses $182$ qubits and $115282$ gates, resp.\ $1198$ qubits and $2694596$ gates, excluding the oracle and the $24$, resp.\ $176$, exact transforms; over $\mathbb{F}_3$ the whole circuit is simulated exactly for all $19$ subgroups and its merge block on all $3^{18}$ basis inputs, and over $\mathbb{F}_5$ each merge is checked through the exact simulation with witnesses computed by the circuit (all label pairs at grade three, all or sampled label tuples at grade two).
```

(Two sentences. "Simulated exactly" means the module-by-module exact composition of §4.3, not
a monolithic statevector; if the paper wants that distinction in the sentence, write "simulated
exactly, module by module," instead.)

## 8. Files and commands

- `theorems/rees_circuit_coherent.py` (new): `MergeBlock(cfg, d)` (block program, `flatten`,
  `segment_counts`, `qubits`), `TerminalSample(cfg)` (assembled program, `counts`,
  `structure`), `block_check` / `block_exhaustive` / `block_sampled`, `sde_exhaustive`,
  `prove_controlled_merge`, `block_structure`, `assembled_basis_paths`, `heis_end_to_end`,
  `heis_compare`, `heis_measured_reference`, `n4_state_checks`, `run_coherent_witness`,
  `measured_counts`, `counts_report`, CLI `main`.
- `tests/test_rees_circuit_coherent.py` (new): 16 tests, about 30–40 s on the loaded machine.
- `research/audits/reviews/2026-11-04-rees-circuit-coherent/run.json`, `run.log`,
  `heis_block_exhaustive.json`, `heis_block_exhaustive.log` (artifacts).
- This report. No existing file edited; nothing committed or pushed.

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_coherent.py
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m theorems.rees_circuit_coherent --out research/audits/reviews/2026-11-04-rees-circuit-coherent/run.json        # ~3 min
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m theorems.rees_circuit_coherent --parts none --heis-exhaustive --out research/audits/reviews/2026-11-04-rees-circuit-coherent/heis_block_exhaustive.json   # ~13 min
```

## 9. Next hard question

The coherent receiver is still classical at every κ_d ≥ 3 grade. The smallest instance that
needs it is n4(F_7) (grade 3, κ = 3, g_3 = 1). Build the κ = 3 witness circuit (triangular
solver with a precomputed contraction, E_2(3) = ∅; oblivious Adleman–Manders–Miller cube
roots with a fixed non-cube; the second elimination per round, since Lemma 4 of the κ = 2
report fails), wire it into `MergeBlock` unchanged, and rerun §4.1–4.4 at n4(F_7).
Acceptance: block_check on all (λ, q) with sampled children, n4_state_checks 9/9 and seeded
recoveries with the circuit's witnesses. (During this session a parallel session added
`theorems/rees_coherent_sde_kappa.py`, `tests/test_rees_coherent_sde_k3.py` and a
`2026-11-04-rees-coherent-sde-k3` report; they were not read or used here. If that circuit has
the interface of `CoherentSDE` (input registers L, output S, clean workspace), `sde_circuit`
is the one function to extend.) A cheaper side question: drop U_SDE^{−1} (keep S as
garbage) and measure what the readout law and the qubit/gate counts become (Theorem 3 still
applies, with S added to the traced registers).

## 10. Independent review (AI subagent, unanchored)

A separate AI agent was given the code, the tests and the task, but not this report's
conclusions. It found no correctness bug and confirmed independently: `_bch_prog` is
`merge_ops` with the classical coefficient −s^{deg j} q_j replaced by the register G_j (macro
sequences, coefficients and node order identical for every s, at all three blocks); the
references used by `block_check` and `prove_controlled_merge` are independent of the node
pruning; the merge workspace takes only SDE-workspace wires, which it re-checked to be 0 after
U_SDE on 3 000 rank-biased n4 grade-2 label tuples; the factorisation, conjugation
conventions, scale and readout phase of `heis_end_to_end` (its tables equal tables built
from `GroupLaw.mul` with the canonical witness); the counts (flattening every item gives the
counted totals, 115 282 and 2 694 596; qubits recount to 182 and 1 198). It added a
basis-path simulation of the assembled program, which became `assembled_basis_paths` (§4.2),
and the mutants quoted in §4.3. Fixed after the review: two constant structure flags were
replaced by real checks (`measured_register_is_root_Q` now compares the measured registers
with the root; the child footprint now allows reads of S_i only), the oracle item's wire order
now matches the generator's, the CLI help said 3^24 instead of 3^18, and the module docstring
now says that `heis_end_to_end` composes the module gate lists (it does not run the
assembled program; §4.2 does that for the wiring). This is not human review.
