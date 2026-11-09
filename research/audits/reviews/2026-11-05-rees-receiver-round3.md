# Rees HSP receiver, round 3: exact level-0 law at c = 3 by two coset symmetries, deterministic merge checkpoints at c = 3, gate-level sources and merges at p = 7

5 November 2026 (overnight). AI-only session (Claude Code, Opus 5.5). Not human review.
Follows `2026-11-05-rees-receiver-round2.md` and its check `2026-11-05-rees-receiver-round2-check.md`
(REES_FULL_CONTINUATION.md item 7, "Still lacking").

Labels used below:
- **[finite computation]**: a complete computation on the stated finite instances, exact in integer, permutation
  or Z[zeta_p] arithmetic;
- **[sampled]**: exact on a stated random subset only;
- **[proved]**: a written proof (Section 2), not machine-checked; its hypotheses are checked by finite computation
  on the instances.

Everything is AI-checked, pending human review.

Files written (no .tex, registry JSON, claim gate, AGENT_HANDOFF.md, STATE.md, formal/Formal.lean or Audit.lean was
touched; nothing committed; no network):
- `theorems/rees_circuit_mono_c3.py` (new): program anatomy, `lemma_hypotheses_check`, `subtree_relabeling_check`,
  `PackedHub`, Phase A (`phase_a`), Phase B (`phase_b`), the overflow-free Gram product (`total_gram_exact`), the
  c = 2 validation (`heis_reduction_check`), the c = 3 negative controls (`negative_controls_c3`) and a CLI
  (`python -m theorems.rees_circuit_mono_c3 --mode ...`).
- `theorems/rees_circuit_mono.py`: one new keyword `condition_sources=None` of `exact_level0_law` and the helper
  `condition_on_coset`. With the default the behaviour is unchanged. When conditioning, K2 is skipped (its
  reference is the unconditioned source) and K5 per label tuple is grouped by the label wires (Section 3.4).
- `tests/test_rees_circuit_round3.py` (new).
- This report and the folder `2026-11-05-rees-receiver-round3/` (run JSONs, logs, `run_commands.sh`).

The claim gate `coherent_receiver_implemented` stays false (STATUS of both modules; a test checks it).

## 0. Answers

| # | Item | Result | Label |
|---|---|---|---|
| 1 | c = 3 exact law, n4(F_5), level 0, and deterministic merge checkpoints at c = 3 | **Exact whole-circuit law for 2 of the 9 subgroups. For the other 7, an exact law conditional on 13 grade-2 label tuples each. Checkpoints on all 9.** Both come through two exact reductions. Lemma A: conditioning each source's oracle outputs on the key of one coset leaves the output law unchanged. Lemma B: once the reduced state of a grade-2 Q is rho_(H_2), it may be replaced by one coset state. Both are proved (Section 2), and their hypotheses are checked on the program. With them every gate acts in program order on one exact Z[zeta_5] state, kept as an orthogonal sum over hubs (at most 390 625 hubs at grade 3, 625 at the root), with nothing measured before the readout. **The exact output law of the whole terminal sample** is computed for gamma_2 and <e1+e2,e3>, the two subgroups with deterministic grade-2 labels: it is uniform on h^perp. For the other seven, the law conditioned on the grade-2 labels is exactly uniform for every label tuple run: 13 distinct tuples per subgroup (the zero tuple and 12 random ones), out of 5^6 or 25^6. Checkpoints KS, K0-K5 hold on every hub. The grade-3 merges are checked on all 6 subtrees for 5 subgroups, and on node 0 (the other 5 are identical up to relabeling, checked) for 4. | proved + finite computation; conditional laws sampled over label tuples |
| 1b | Reductions validated | At c = 2, the conditioned law equals the unreduced round-2 law for all 19 Heis(F_3) subgroups (37 comparisons). At c = 3, a random coset instead of the identity gives the identical exact rho_(Q_2) (3 subgroups) and the identical law (gamma_2; <e2>, Z(G) conditional). | finite computation |
| 1c | Negative controls at c = 3 | Phase A: 15 mutants. 7 are caught by checkpoints, 5 stop at a structural guard, 3 are equivalent, 0 are missed. Phase B, zero and one random grade-2 label tuple: 12 mutants each. 5 are caught, 1 stops at a guard, 6 are equivalent, 0 are missed. On the zero tuple every caught mutant that reaches the readout has an exactly uniform law: only the checkpoints see it. On the random tuple one caught mutant also makes the law non-uniform. | finite computation |
| 2 | Explicit QFT (lem:qft-mod) inside the monolithic simulation | **Not done.** The explicit transforms have phases 2 pi/2^k, which are not in Z[zeta_p]. A float simulation fails on support growth of about 10^4 per general call (qft-wire report). Section 7. | none |
| 3 | Gate level at p = 7 | **Sources:** every source gate list of n4(F_7) is run on all 7^7 addresses with KS, for all 9 subgroups (all 18 sources of each terminal sample, on all 6 nodes, 162 sources in all). One changed oracle entry is caught on all 9. **Gate-level simulation:** H = Z(G) (the smallest that fits). Phase A runs the kappa_3 = 3 coherent grade-3 merge on 117 649 hubs, with all checkpoints. Phase B, conditional on grade-2 labels: zero + 2 random tuples, all checkpoints, conditional law exactly uniform on h^perp (343 points). | finite computation |
| 4 | The two largest n4(F_5) subgroups | **Done:** gamma_2 (9.8e7 child rows) and <e1+e2,e3> (4.9e8 child rows, in 3 hub ranges). Memory is reduced by bit-packed rows, chunking over hubs and the coset reductions. Peak RSS 2.9 GB. Exact laws are uniform on h^perp. | finite computation |
| 5 | kappa >= 3 coherent-label circuits at class five | **Not attempted** (time). | none |

## 1. Method: the exact level-0 law at c = 3

### 1.1 Object

The assembled coherent terminal sample of `rees_circuit_coherent.TerminalSample` for the class-three filiform
algebra over F_5 (cover dimensions (4,2,1), merge arities M_3 = 2, M_2 = 6): 1198 qubits, 2 694 596
X/CX/CCX/SWAP gates, 176 exact QFT_5 and 36 oracle calls, flattened by `rees_circuit_mono.compile_program` into
3181 steps. The tree has six grade-2 nodes; each has two top sources (three oracle calls each, then a grade-3
instrument), the preparation of its Q_2 and a grade-3 merge block. The root has the six grade-2 instruments,
the preparation of Q_1, the grade-2 merge block and the final QFT. Nothing is measured before the readout.

`anatomy` partitions the 3181 steps into, for each node j, a Phase-A range (sources, grade-3 instruments, Q_2
preparation, grade-3 merge; steps 0-349 for node 0), the grade-2 instrument (steps 350-355 for node 0), and the
root steps (Q_1 preparation up to step 2139, merge up to 3175, final QFT from 3176). It checks the footprint of
every step: a Phase-A step of node j touches only node j's wires and the shared workspace, an instrument step
only Q_2j, z_2j and the workspace, a root step only Q_1, the Q_2's, the z_2's and the workspace, and the root comes
after all subtrees. `subtree_relabeling_check` checks that the Phase-A and instrument step lists of nodes 1-5 equal
those of node 0 gate for gate under one wire bijection that fixes the workspace (all True). `lemma_hypotheses_check`
reads hypotheses (2)-(4) of the two lemmas of Section 2 off the program (all True; Section 3.1).

### 1.2 Why the direct level-0 computation does not fit

Round 2's hub representation (an orthogonal sum over the values of the labels and Q) gives the c = 2 law with at
most 729 hubs. At c = 3 the same split at grade 3 has |K_3^perp|^2 · |G_2| = 25 · 15 625 = 390 625 hubs for
<e2>, and without conditioning each child carries the whole address superposition of a source, 5^7 = 78 125 rows
per hub, about 390 625 · 2 · 78 125 = 6 · 10^10 rows in all; the
root split has |K_2^perp|^6 · |G_1| hubs, up to 25^6 · 625 = 1.5 · 10^11. Neither fits. Two exact reductions
(Section 2, proved) and a packed hub representation make it fit.

### 1.3 Phase A (one grade-2 node, gate level, exact)

1. The two sources are run on the whole address superposition (78 125 rows each), with their three oracle calls
   and the uncomputation of the evaluation workspace. Checkpoint **KS** (round 2) runs on each source: the state is
   sum_x |x>|key(x)> with clean workspace, every address once with equal amplitude, no other wire entangled, and
   the fibres of the key are exactly the left cosets of exp(h~).
2. The oracle outputs of each source are then **conditioned on the key of one coset** (default: the identity
   coset; `condition_on_coset`). By Lemma A this leaves the output law unchanged. Checkpoint **K1c**: the
   conditioned address support is exactly that left coset.
3. The grade-3 instrument runs at gate level. Checkpoint **K2**: the joint state of (address, label) equals the
   reference formula psi(x', lam) = sum_z zeta^(-lam·z) [x' z in coset], computed from h, up to one scalar.
4. Q_2 is prepared (uniform on G_2, checked). The state is rewritten exactly as an orthogonal sum over the hub
   values (both grade-3 labels and Q_2) in `PackedHub`: hub-classical wires are uint8 arrays over the hubs; each
   child is bit-packed rows (hub, address bits) with fixed Z[zeta_5] amplitudes, since only permutation gates act
   from here on. Hubs never interact (hub wires are only controls), so the hubs are processed in chunks of at most
   3 · 10^6 child rows. A gate that would join two children raises an error. This never happened in an unmutated run.
5. The grade-3 merge block (U_SDE, the witness-controlled BCH merges, U_SDE^-1) runs gate by gate. Checkpoints:
   **K3** at every merge component boundary (workspace unentangled; after child i's own merge, child i already
   equals its reference translation); **K4** after the block, for every hub: every row of every child equals its
   pre-merge row right-translated by -delta_(s_i)(sigma(q)), with s the independent reference witness
   `C.sde_reference` of the label values (nonzero, sum_i s_i^3 lam_i = 0 checked); labels and Q_2 unchanged;
   witness and workspace 0.
6. Checkpoint **K5_2**: for every grade-3 label tuple, the reduced state of Q_2 is exactly proportional to
   rho_(H_2) = sum_k |C'_k><C'_k| over the left cosets C'_k of H_2 in G_2. It is computed from the K4-verified rows:
   child i at hub (lam, q) is R_(t_i(q)) phi_(i,lam_i), so <c_i(q')|c_i(q)> = A_i(t_i(q) t_i(q')^-1) with the
   autocorrelation A_i(u) = <phi_i|R_u|phi_i>, and rho[q,q'] = prod_i A_i(...). The grade-3 label law is checked
   uniform on (K_3^perp)^2. **Direct cross-check** (trivial and Z(G), node 0, `A_direct_gram_trivial_ZG_node0.json`; the first two label
   tuples): the rows of rho
   for q = 0 and 47 random q (all q' each) recomputed directly from the stored output rows of the children by
   summing over equal basis keys, without the descriptor, are identical.

### 1.4 Phase B (the root, gate level, exact)

By Lemma B, once K5_2 holds, each Q_2 may be replaced by the uniform state of one left coset gH_2 (default g = e).
The six grade-2 instruments (checkpoint K2 against the reference formula, and the grade-2 label law of each child
checked uniform on K_2^perp), the preparation of Q_1 and the grade-2 merge block then run gate by gate on
round 2's `HubState` over (grade-2 labels, Q_1), with checkpoints K3, K4 (every hub; reference witness
`C.sde_reference` with sum_i s_i^2 lam_i = 0) and K5 (the reduced state of Q_1 proportional to rho_(H_1), for every
grade-2 label tuple separately and in total). The final exact QFT_p on Q_1 (the last steps, acting on Q_1 only) is not run gate by gate. It is applied
analytically: the readout law is computed exactly from the Gram matrices, P(y) = sum_d zeta^(y·d) W(d), with W(d)
the sum of the Gram entries over hub pairs with q_h - q_h' = d. This is the law of the same exact transform.

- When K_2^perp = 0 (gamma_2 = <e3,e4> and <e1+e2,e3>) the grade-2 labels are deterministic, and the Phase-B law is
  **the exact output law of the whole terminal sample**.
- Otherwise there are |K_2^perp|^6 = 5^6 or 25^6 grade-2 label tuples. Phase B is then run **conditionally on a
  stated label tuple** (an exact projector on the six label registers after the instruments): the exact
  conditional readout law given those labels. The zero tuple and two random tuples are run per subgroup. The
  grade-2 label law itself is computed exactly (uniform on (K_2^perp)^6: each child's law is uniform on K_2^perp
  and the children are independent before the root merge).

## 2. The two reductions [proved; hypotheses checked on the instances by finite computation]

Notation. For a group register X with values in a group Γ (canonical words only) and g ∈ Γ,
L_g |x> = |g x> (left translation) and R_t |x> = |x t> (right translation). Exponential coordinates,
the BCH product of `GroupLaw.mul`; inverse x^-1 = -x.

**Lemma A (source coset symmetry).** Fix one top source of the terminal sample, with address register A
(values in G_c), oracle-output register Y, and let |Ψ> be the joint state right after the source's last
oracle call and the uncomputation of its evaluation workspace. Suppose

1. (KS) |Ψ> = |G_c|^(-1/2) Σ_x |x>_A |κ(x)>_Y ⊗ |Φ>, where |Φ> is the state of all other wires, the
   workspace is 0, and κ is constant exactly on the left cosets x S, S = exp(h~), with distinct values on
   distinct cosets;
2. no later gate touches Y;
3. every later gate either does not touch A, or belongs to one of two segments whose action on inputs with
   canonical A and clean workspace is, as a map of basis states, a translation of A that commutes with every
   L_g: the instrument of this source (|x>|z> -> |x z^-1>|z> with z in the central top coordinates) and the
   controlled merge of this child in its parent's merge block (|x>|s>|q> -> |x · t(s, q)>|s>|q>, with
   t(s, q) = -δ_s(σ(q))), each leaving the workspace clean;
4. the readout projectors Π_y act on wires other than A and Y.

Then for every y, P(y) = P(y | Y = κ(x_0)) for every address x_0: conditioning the oracle outputs on the key
of any one coset leaves the output law unchanged.

*Proof.* Write the cosets as g_k S and |C_k> = |G_c|^(-1/2) Σ_(x ∈ g_k S) |x> = L_(g_k) |C_0>. By (1),
|Ψ> = Σ_k |C_k>|κ_k> ⊗ |Φ> with orthonormal |κ_k>. Let W be the rest of the circuit. By (2), W does not act on
Y, so P(y) = Σ_k ||Π_y W (|C_k> ⊗ |Φ>)||^2. By (3), W L_g = L_g W on the states reached from |C_k> ⊗ |Φ>
(every segment maps canonical-A, clean-workspace inputs to canonical-A, clean-workspace outputs by a
translation that commutes with L_g, since g(x z^-1) = (g x) z^-1 and g(x t) = (g x) t; the other gates do not
touch A). By (4), Π_y commutes with L_g. Hence
||Π_y W L_(g_k)(|C_0>|Φ>)|| = ||L_(g_k) Π_y W (|C_0>|Φ>)|| = ||Π_y W (|C_0>|Φ>)||, all terms are equal,
P(y) = #cosets · ||Π_y W(|C_0>|Φ>)||^2 and P(Y = κ_0) = 1/#cosets. Replacing C_0 by any C_k gives the same. ∎

The lemma applies to the sources one at a time (the other sources are part of |Φ>; a conditioned source
is still a tensor factor of |Φ>), so all 2·6 = 12 sources of the class-three terminal sample (3·6 = 18 over
F_7) may be conditioned, and the output law is unchanged.

**Lemma B (grade-2 coset symmetry).** Fix a grade-2 node j. At the end of its grade-3 merge block
(U_SDE^-1 done), let ρ_j be the reduced state of Q_2j, all other wires of the subtree (addresses, oracle
outputs, grade-3 labels) traced out. Suppose

1. (K5_2) ρ_j = c Σ_k |C'_k><C'_k| for a scalar c > 0, where C'_k runs over the left cosets of H_2 in G_2 and
   |C'_k> is the uniform superposition over C'_k; the workspace is 0;
2. the traced wires of the subtree are never touched again;
3. every later gate touching Q_2j belongs to the grade-2 instrument of j (a central translation of the top
   coordinates of Q_2j) or to the controlled merge of child j in the root merge block (a right translation
   x -> x · t(s, q)), each as in Lemma A (3);
4. the readout projectors and, for a conditional law, the projector onto stated grade-2 label values act on
   wires other than Q_2j.

Then the joint law of (readout, grade-2 labels) is unchanged when the subtree's state is replaced by the
pure state |C'_k> on Q_2j, for any one k.

*Proof.* Before the root merge the six subtrees act on disjoint wires apart from the clean workspace, so the
global state is a product, and by (2) the law depends on subtree j only through ρ_j. By (1),
ρ_j = c Σ_k L_(g_k) |C'_0><C'_0| L_(g_k)^†. W commutes with L_g on Q_2j by (3) and the projectors commute with
it by (4), so Tr(Π W L_g σ L_g^† W^†) = Tr(Π W σ W^†) for every σ, and each term gives the same law. ∎

**Where the hypotheses come from.**
- Lemma A (1) is checkpoint KS, run on every source on all |G_c| addresses (78 125 over F_5, 823 543 over
  F_7), exact.
- Lemma A (2)-(4), Lemma B (2)-(4), footprints: `lemma_hypotheses_check` reads them off the flattened program
  (`relabeling.json`, all True). For each of the 12 sources: the last oracle call precedes the source end, no
  later step touches its oracle outputs, and every later step that touches its address belongs to its own
  instrument (one contiguous run, inside the instrument steps on its own label register, touching no other
  child's address; tightened after the review) or to the merge components `witness_control_grade3`/`bch_merge_grade3`, which
  form one interval of merge steps touching no other child's address. For each of the 6 grade-2 nodes: no step
  after its grade-3 merge block touches the subtree's addresses, oracle outputs or grade-3 labels, and every later
  step touching Q_2 is in its own grade-2 instrument (inside that node's instrument range) or in one interval of the root's merge components touching no
  other Q_2. The final QFT acts on Q_1 only and is last. Negative controls (test): a CX from an oracle-output
  wire, inserted in a root step, makes the check fail; so does a CX on node 0's Q_2 inserted into node 1's
  grade-2 instrument (an allowed component name, but not its own instrument). `anatomy` checks the footprints of all 3181 steps.
- Lemma A (3), Lemma B (3), merge part: `C.prove_controlled_merge` (symbolic replay of ctrl_i, bch_i,
  ctrl_i^-1 over F_p[s, q, x] against the classical BCH polynomial, for all canonical (s, q, x)) and
  `C.block_structure` (U_SDE never writes labels, Q or children; child i's merge writes only x_i and merge
  workspace), both rerun for the grade-3 and grade-2 blocks here; the macro gate lists are the
  `rees_circuit_arith` ones, checked on all basis inputs for p <= 13 in that report. The instrument part: the
  `add_scaled` macro on canonical inputs (same report) and the grading (the top coordinates of G_d are
  central).
- Lemma B (1) is checkpoint K5_2, exact, for every grade-3 label tuple.
- Lemma A and B (4): the readout is the root Q_1; label conditioning acts on z2 only.

**Checks of the reductions themselves (gate level, exact).** (a) At c = 2 the round-2 hub computation needs no
reduction. With every source conditioned on the identity coset and on a random coset, the exact level-0 law
of Heis(F_3) equals the unreduced one for all 19 subgroups (Section 3.4). (b) At c = 3, Phase A with the sources
conditioned on a random non-identity coset gives the identical reduced state of Q_2 (equal signatures of the
exact sparse matrix, Section 3.2), and Phase B with each Q_2 replaced by a random coset gH_2 gives the identical
law (equal law signatures, Section 3.3). (c) Negative control of the comparison: with a changed oracle entry, the
conditioned c = 2 law differs from the unreduced law of the same oracle (test).

## 3. Results over F_5 [finite computation; reductions proved]

The full per-run tables (every node, every label tuple, all checkpoint columns, signatures, seconds, RSS) are in
`2026-11-05-rees-receiver-round3/tables.md`, generated from the run JSONs.

### 3.1 Program structure (`relabeling.json`, `merge_proofs_f5.json`)

- `anatomy`: ok. `subtree_relabeling_check`: nodes 1-5 equal node 0 up to a wire bijection fixing the workspace
  (5 of 5). `lemma_hypotheses_check`: ok for all 12 sources and 6 grade-2 nodes; after the source end only
  `instrument` and `bch_merge_grade3` steps touch a source address, and after the grade-3 block only `instrument`
  and `bch_merge_grade2` steps touch Q_2.
- `prove_controlled_merge` (symbolic replay over F_5[s, q, x], 82 macros at grade 3, 48 at grade 2): proved at both
  grades; `block_structure`: U_SDE never writes labels, Q or children, each child merge has a local footprint.

### 3.2 Phase A: grade-2 subtrees (`A_*.json`)

| H | normal | nodes run | hubs per node | grade-3 label tuples | child rows per node | KS, K1c, K2 | K3, K4 (every hub) | K5_2 (every label tuple) | s per node |
|---|---|---|---|---|---|---|---|---|---|
| trivial | yes | all 6 | 390 625 | 25 | 3 906 250 | pass | pass | pass (25 of 25) | 69-81 |
| Z(G) | yes | all 6 | 15 625 | 1 | 3 906 250 | pass | pass | pass | 17-19 |
| <e2> | no | all 6 | 390 625 | 25 | 19 531 250 | pass | pass | pass (25 of 25) | 116-137 |
| <e1> | no | all 6 | 390 625 | 25 | 19 531 250 | pass | pass | pass (25 of 25) | 107-151 |
| <e1+e3> | no | all 6 | 390 625 | 25 | 19 531 250 | pass | pass | pass (25 of 25) | 103-124 |
| <e2,e4> | no | node 0 | 15 625 | 1 | 19 531 250 | pass | pass | pass | 89 |
| <e2,e3> | no | node 0 | 390 625 | 25 | 488 281 250 | pass | pass | pass (25 of 25) | 1842 |
| gamma_2 = <e3,e4> | yes | node 0 | 15 625 | 1 | 97 656 250 | pass | pass | pass | 455 |
| <e1+e2,e3> | yes | node 0, 3 hub ranges | 15 625 | 1 | 488 281 250 | pass (3 of 3 ranges) | pass (3 of 3 ranges) | pass (3 of 3 ranges) | 1087 + 701 + 673 |

- Every Phase-A run has `all_checkpoints_pass: true`, and no gate joined two children (PackedHub would have raised),
  Q_2 uniform on G_2, the grade-3 label law uniform on (K_3^perp)^2, and the reference witness solves
  sum_i s_i^3 lam_i = 0 on every label tuple. Peak RSS of any Phase-A run 2.9 GB (ru_maxrss of the <e1+e2,e3> hub-range runs; the guard's 3 s samples peaked at 2.6 GB) (guard limit 5 GB).
- **Hub ranges** (<e1+e2,e3>). The 15 625 hubs of node 0 are split into three runs (hubs 0-5208, 5209-10416,
  10417-15624; 55 chunks each), each a separate process. Hubs never interact, so K3 and K4 checked on each range
  together cover every hub. K5_2 is computed in each run from the K4 descriptor over all q (it uses only the
  pre-merge child states and the reference translations, both computed in full in each run). So it does not
  depend on the hub range, and the identical `rho_Q2_signature` in the three runs holds by construction. It is
  not corroboration. K5_2 applies to the node because K4 holds on all three ranges and the ranges partition the
  hubs. `combine_hub_ranges` checks this (`closure_hub_ranges_combined.json`: partition, every range passes,
  identical signature). Each partial-range JSON carries `K5_2_conditional_on_K4_on_other_hub_ranges: true`
  (the flag was added after the runs; the runs predate it).
- The six nodes of each subgroup run on all 6 nodes give the identical exact reduced state of Q_2 (`rho_Q2_signature`)
  and the identical output rows (`final_state_signature`), as the relabeling predicts.
- **Direct cross-check of K5_2** (trivial, Z(G), node 0; `A_direct_gram_trivial_ZG_node0.json`; rows of rho for q = 0 and 47 random q, first two label tuples):
  identical to the descriptor computation. Negative control (slow test): one doubled child amplitude, or one changed
  descriptor entry, makes the cross-check fail.
- **Coset-symmetry check of Lemma A at c = 3** (`A_symmetry_random_coset.json`): with every source conditioned on a
  random coset outside exp(h~) (<e2>: x0 = 52407; Z(G): 62915; trivial: 1770) instead of the identity coset, the
  exact reduced state of Q_2 is identical (equal `rho_Q2_signature`), while the output rows differ (different
  `final_state_signature`).

### 3.3 Phase B: the root and the readout law (`B_*.json`)

| H | grade-2 labels | runs | hubs | peak child rows | all checkpoints | readout law | s |
|---|---|---|---|---|---|---|---|
| gamma_2 = <e3,e4> | deterministic (K_2^perp = 0) | Q_2 = H_2; and six random cosets gH_2 | 625 | 390 625 | pass | **exact law of the whole circuit: uniform on h^perp (25 points, 1/25 each)**; equal signature with random cosets | 174, 124 |
| <e1+e2,e3> | deterministic | Q_2 = H_2 | 625 | 1 953 125 | pass | **exact law of the whole circuit: uniform on h^perp (5 points, 1/5 each)** | 626 |
| trivial | 25^6 tuples | zero + 12 random (13 distinct tuples) | 625 | 15 625 | pass | conditional law uniform on h^perp (625 points) for every tuple run | 14-20 |
| Z(G) | 5^6 tuples | zero + 12 random (13 distinct); zero with six random cosets | 625 | 15 625 | pass | conditional law uniform on h^perp (125); equal signature with random cosets | 22-32 |
| <e2> | 25^6 | zero + 12 random (13 distinct); zero with six random cosets | 625 | 78 125 | pass | conditional law uniform on h^perp (125); equal signature with random cosets | 24-39 |
| <e1> | 25^6 | zero + 12 random (13 distinct) | 625 | 78 125 | pass | conditional law uniform on h^perp (125) | 25-33 |
| <e1+e3> | 25^6 | zero + 12 random (13 distinct) | 625 | 78 125 | pass | conditional law uniform on h^perp (125) | 22-27 |
| <e2,e4> | 5^6 | zero + 12 random (13 distinct) | 625 | 390 625 | pass | conditional law uniform on h^perp (25) | 50-63 |
| <e2,e3> | 5^6 | zero + 12 random (13 distinct) | 625 | 390 625 | pass | conditional law uniform on h^perp (25) | 52-65 |

Checkpoints of every Phase-B run: K0; K2 of all six grade-2 instruments against the reference formula; each
child's grade-2 label law uniform on K_2^perp; K3 at every merge component boundary; K4 for every hub (every
child equals its right translation by -delta_(s_i)(sigma(q)), with the reference witness, sum_i s_i^2 lam_i = 0);
labels and Q_1 unchanged, workspace and witness 0; K5 (reduced state of Q_1 proportional to rho_(H_1)) for every
label tuple and in total. No gate joins two children. `hub_joins` in the Phase-B JSONs is not zero: it is 1-6 in
the runs with K_2^perp != 0. It counts the 66 Phase-B runs for <e2>, <e1>, <e1+e3>, <e2,e4> and <e2,e3>, and the
merges of two factors of the sparse state in them. The independent review (Section 11) logged the joins in two
<e2> runs: each merges a factor of one Q_2 with a workspace factor, never two children. A join of two different
children would make K4 fail (`hub_joint_rows` returns None), and K4 passes in every run.

**What is and is not the exact law of the whole circuit.** For gamma_2 and <e1+e2,e3> the Phase-B law is the exact
output law of the whole terminal sample, by Lemmas A and B and the checks of Section 2. For the other seven it is
the exact law conditional on the stated grade-2 label tuple; the whole-circuit law is the average of the
conditional laws over the |K_2^perp|^6 equally likely tuples (each child's label law is checked uniform, and the
children are independent before the root merge), and only the tuples listed were run. Within each subgroup all
13 conditional laws have the identical `law_signature`.

### 3.4 Validation of Lemma A at c = 2 against the unreduced law (`heis_f3_reduction_check.json`)

For all 19 subgroups of Heis(F_3), the round-2 exact level-0 law (nothing measured, no reduction) is compared with
the same computation with every source's oracle outputs conditioned on one coset: the identity coset, and a random
coset outside exp(h~) (one coset only for H = G). All 37 conditioned laws equal the unreduced law exactly
(proportional in Z[zeta_3]). Every conditioned run also passes its own checkpoints. K2 is skipped there, and K5 per label tuple is grouped by the label wires (see the list of files written). Negative control (test `test_a_changed_oracle_entry_changes_the_conditioned_c2_law`):
one changed oracle entry breaks Lemma A (1): the key fibres are no longer the left cosets. The conditioned law of
the mutated oracle then differs from the unreduced law of the same mutated oracle, so the comparison has power. A
direct check on H = <(0,0,1)> and <(1,0,0)> found this. It also found a caveat. For <(0,0,1)>, the mutated
oracle's law conditioned on the identity coset equals the unmutated law, because conditioning projects most of the
change away. An earlier version of this test compared with the unmutated law and failed in the final run. It was
fixed to compare with the unreduced mutated law (Section 6).

## 4. Gate level at p = 7: n4(F_7), the fifth backend [finite computation]

Object: `rees_circuit_coherent_k3.TerminalSampleK` for n4(F_7) (kappa_3 = 3; merge arities M_3 = 3, M_2 = 6;
1629 qubits, flattened into 5703 steps), run inside `kappa_dispatch()` so that the reference witness is the
kappa >= 3 one. The same anatomy, relabeling and lemma-hypotheses checks pass (`f7_relabeling.json`), and
`prove_controlled_merge` proves the grade-3 and grade-2 controlled merges symbolically (`merge_proofs_f7.json`).

**Sources on all addresses (item 3, first half).** Every source is run from its gate list on all 7^7 = 823 543
addresses with its three oracle calls, and checkpoint KS holds (sum_x |x>|key(x)>, clean workspace, every
address once with equal amplitude, key fibres exactly the left cosets of exp(h~)); then K1c and the instrument
check K2 on the conditioned coset. Coverage: all 6 grade-2 nodes of all 9 subgroups, that is all 18 sources of each terminal sample, 162 sources
in all (`f7_sources_all_subgroups_all_nodes.json`, `f7_sources_part2.json`, `f7_sources_part3.json`). Every KS,
K0, K1c and K2 holds (162, 324, 162 and 162 checks), at 3-70 s per node. One node run took 558 s; it was done
before the fast left-coset enumeration replaced the reference one, which gives equal output (test). The first
run was stopped by hand after 19 node runs for that reason, and the rest were run in two later parts. Negative control: one changed oracle entry is caught by KS on node 0 of all 9
subgroups (`f7_sources_oracle_mutant.json`, 9 of 9; K1c and K2 also fail for 7 of them).

**Gate-level simulation (item 3, second half): H = Z(G), the smallest instance that fits.**
- Phase A, node 0 (`f7_A_ZG_node0.json`): 117 649 hubs (Q_2 in G_2, one grade-3 label triple), three children,
  121 060 821 child rows in 41 chunks, 419 s, 2.1 GB. All checkpoints pass: KS, K0, K1c, K2 (3 sources);
  K3 at 369 component boundaries and after each of the 3 child merges in every chunk; K4 on every hub (the
  coherent power-SDE grade-3 block U_SDE, the witness-controlled merges, U_SDE^-1, with the kappa_3 = 3 reference
  witness, sum_i s_i^3 lam_i = 0); K5_2 (reduced state of Q_2 exactly proportional to rho_(H_2), |H_2| = 49).
- Phase B (`f7_B_ZG_conditional.json`): conditional on the zero grade-2 label tuple and two random ones (out of 7^6; K_2^perp = F_7 per child). Each run has 2401 hubs over (grade-2 labels, Q_1), peak 117 649 child rows, and 558-604 s. All checkpoints pass for each: K0, K2 of the six grade-2 instruments, the grade-2 label laws, K3, K4 with sum_i s_i^2 lam_i = 0, and K5 per tuple and in total. **The conditional readout law is exactly uniform on h^perp (343 points, 1/343 each)**, and the three law signatures are identical. Peak RSS 2.6 GB.

Not run at p = 7: Phase A for the other eight subgroups. With |K_3^perp| = 7 the grade-3 split has 7^3 · 7^6 =
4.0 · 10^7 hubs (five subgroups); for gamma_2, <e2,e4> and <e1+e2,e3> (one label triple) the children have
7^5, 7^4 and 7^6 rows per hub, that is 5.9 · 10^9, 8.5 · 10^8 and 4.2 · 10^10 rows, beyond the time cap here.

## 5. Negative controls [finite computation, deterministic]

Each new check has a negative control. Mutants are run deterministically through the same code as the unmutated
run. A mutant that no check flags is compared with the unmutated run by the signature of its final state
(Phase A: the output rows of the children; Phase B: `state_signature` of the HubState); equal is called an
**equivalent mutant**: the final-state signature is identical to the unmutated run. For Phase A this signature
covers only the children's output rows, so the claim is that the dropped gate leaves those rows unchanged; that it
never acts on any reachable state is not checked. "Guard" means the run stopped before
any checkpoint at a structural guard that a correct run never reaches: PackedHub refuses a gate acting jointly on
two children (the workspace is then entangled with a child mid-merge), the row budget is exceeded, or the
conditioning finds an address more than once.

### 5.1 Phase A, H = <e2> (non-normal), node 0 (`negative_controls_c3_phaseA_part0.json`, `..._part1.json`)

Baseline: all checkpoints pass (159 s, 89 s).

| mutant | result |
|---|---|
| one oracle entry changed (x0 = 1) | caught: KS, K1c, K2, K5_2 |
| drop source_evaluation cx middle | guard: row budget exceeded at the source |
| drop source_evaluation ccx middle | equivalent (final state identical) |
| drop instrument cx middle | guard: conditioning finds the address twice |
| drop sde_grade3 cx first / cx middle / ccx middle | caught: K3, K4 (translation), K4 (workspace) |
| drop witness_control_grade3 cx first / cx middle | caught: K3, K4, K4 (workspace) |
| drop witness_control_grade3 ccx middle | guard: gate joins two children |
| drop bch_merge_grade3 cx first | guard: gate joins two children |
| drop bch_merge_grade3 cx middle / ccx middle | equivalent |
| MergeBlock g_sign (both grades) | caught: K3, K4 (children translated by +delta instead of -delta) |
| MergeBlock skip_bennett (both grades) | guard: gate joins two children |

15 mutants: 7 caught by checkpoints, 5 stopped by a guard, 3 equivalent, **0 missed**.

### 5.2 Phase B, H = <e2>, zero grade-2 label tuple (`negative_controls_c3_phaseB.json`)

Baseline: all checkpoints pass, law uniform (26 s).

| mutant | result |
|---|---|
| drop instrument cx middle | guard: row budget exceeded |
| drop sde_grade2 cx middle | caught: K3, K4, workspace (law still uniform) |
| drop witness_control_grade2 cx first | caught: K3, K4, workspace (law still uniform) |
| drop bch_merge_grade2 cx first | caught: workspace (law still uniform) |
| drop sde_grade2 cx first / ccx middle; witness_control_grade2 cx middle / ccx middle; bch_merge_grade2 cx middle / ccx middle | equivalent (6) |
| MergeBlock g_sign | caught: K3, K4 (law still uniform) |
| MergeBlock skip_bennett | caught: K3 |

12 mutants: 5 caught, 1 guard, 6 equivalent, 0 missed. **Every caught mutant whose run reached the readout (4 of
5) has an exactly uniform readout law**: the readout cannot see it, the checkpoints do.

### 5.3 Phase B, H = <e2>, a random nonzero grade-2 label tuple (`negative_controls_c3_phaseB_random_tuple.json`)

Label tuple ((4,1),(3,0),(2,2),(1,1),(1,2),(0,1)). Baseline: all checkpoints pass, law uniform (25 s). Same 12
mutants: 5 caught (witness_control_grade2 cx first, witness_control_grade2 ccx middle, bch_merge_grade2 cx first,
g_sign, skip_bennett), 1 guard (instrument cx middle, row budget), 6 equivalent, 0 missed. With this tuple, the
witness_control_grade2 cx-first mutant also makes K5 fail and **makes the readout law non-uniform**, so the
readout sees it too. Which mutants are equivalent depends on the reachable states. sde_grade2 cx middle is caught
on the zero tuple and equivalent on this one; witness_control_grade2 ccx middle is the reverse. Five mutants
(sde_grade2 cx first and ccx middle, witness_control_grade2 cx middle, bch_merge_grade2 cx middle and ccx middle)
leave the final state identical on both tuples: they act trivially on every state reached in these runs.

### 5.4 Controls of the other new checks

- KS at p = 7: one changed oracle entry, node 0 of each of the 9 subgroups (`f7_sources_oracle_mutant.json`):
  caught by KS on 9 of 9; K1c and K2 also fail for 7 of them (all but gamma_2 and <e1+e2,e3>).
- `lemma_hypotheses_check`: a CX from an oracle-output wire into the workspace, inserted in a root step, makes it
  fail (test).
- `subtree_relabeling_check`: one dropped CX in node 1's grade-3 BCH merge makes it fail (test).
- `PackedHub`: equals a dense state vector on 6 random circuits; refuses a gate joining two children (tests).
- Coset conditioning at c = 2: with one changed oracle entry, the conditioned law differs from the unreduced law of the same oracle (test).
- `instrument_reference`: a wrong coset gives a different reference: a non-central address gives other keys, and a central one gives the same keys with amplitudes that are not proportional (test).
- Direct Gram cross-check of K5_2: a doubled amplitude or a changed descriptor entry is detected (slow test).
- `law_signature`: scale-free, and separates two different laws (test).

## 6. Tests

`tests/test_rees_circuit_round3.py` (new). The default run checks:
- the status gate (`coherent_receiver_implemented` is False in both modules);
- `anatomy`, `subtree_relabeling_check` (with its negative control) and `lemma_hypotheses_check` (with two
  negative controls: an oracle-output wire touched at the root, and a Q_2 touched in another node's instrument);
- `combine_hub_ranges`: accepts a partition with equal signatures; rejects a gap, a differing signature, a failing
  range;
- `PackedHub` against a dense state vector on 6 random circuits, and its refusal of a joining gate;
- the c = 2 coset conditioning: law unchanged on 3 subgroups, and a changed oracle entry changes it;
- KS and conditioning at c = 3, KS catching a changed oracle entry, `instrument_reference` rejecting a wrong coset;
- Phase B on <e2> with the zero label tuple (all checkpoints, uniform conditional law);
- `cyc_mul_rows_exact` against int64 and past the int64 range, `law_signature`, and the fast `left_coset_ids`
  against the reference on 4 cases.

Behind `REES_SLOW=1` are Phase A trivial with the direct Gram cross-check and its two negative controls, the
g_sign mutant at Phase A, and the gamma_2 exact law.

Final run (the brief's command, `nice -n 10`, one process):

```
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/test_rees_circuit_mono.py tests/test_rees_circuit_exhaustive.py tests/test_rees_circuit_round2.py \
  tests/test_rees_circuit_round3.py
```

Result after the review fixes: **69 passed, 4 skipped in 105 s** (`pytest_final.txt` in the folder). Before the review it was 68 passed, 4 skipped. The 4 skips are the `REES_SLOW` tests: 3 in round 3 and 1 in round 2. The 3 round-3 slow tests were then run separately with `REES_SLOW=1`: 3 passed (193 s before the review fixes, 218 s after; `pytest_slow_round3.txt` is the later run).

The first final run (before the fixes below) had **2 failures**, both in negative controls of the new tests:
- `test_a_changed_oracle_entry_changes_the_conditioned_c2_law` compared the conditioned law of the mutated oracle with the *unmutated* law. For H = <(0,0,1)> those are equal, because conditioning on the identity coset projects most of the change away. The test now compares with the unreduced law of the same mutated oracle, which is the comparison that `heis_reduction_check` makes. They differ, so the control has power (checked on <(0,0,1)> and <(1,0,0)>).
- `test_instrument_reference_rejects_a_wrong_coset` compared address 0 with address index 1, which is central. A central address gives the same keys with other phases, so the key-only comparison could not see it. The test now uses a non-central address (other keys), plus a central one (same keys, amplitudes not proportional over Z[zeta_5]).

Neither failure touches a run result. Both were defects in the controls, not in the checks they control.

## 7. Not done, and why

- **Item 2, explicit QFT inside the monolithic simulation: not done.** The transforms of Lemma qft-mod use
  Phase(2 pi s/2^k) gates, so their outputs are not in Z[zeta_p]: an exact law of the explicit-transform circuit
  cannot be computed in this representation, and "the same exact output law" cannot hold exactly (only within a
  total-variation bound). A floating-point monolithic simulation is out of reach for the reason recorded in
  `2026-11-04-rees-qft-wire.md` Section 3.2(i): each general call leaves a phase-estimation tail of norm ~0.1 spread
  over 10^4-10^5 pool states, and with a shared pool every later general call acts on every branch, so the support
  multiplies by ~10^4 per general call (Heis(F_3) has 6 general calls). The coset reductions of Section 2 shrink
  the address registers but not these tails. The explicit transform therefore stays covered only by the proved
  hybrid bound of that report; nothing new is claimed for it here.
- **The exact law of the whole terminal sample for the seven n4(F_5) subgroups with K_2^perp != 0.** The root has
  5^6 or 25^6 grade-2 label tuples; only the zero tuple and 12 random tuples were run per subgroup (exact
  conditional laws). The unconditional law is the average over all tuples. The 13 tuples run are a sample, not a
  proof of uniformity for the rest.
- **Item 5, coherent-label circuits with kappa >= 3 at class five: not attempted** (time).
- Lemma A (3) needs the grade-3 instrument to act as the central translation x -> x z^-1 on *every* address, not
  only on the conditioned coset. K2 checks it on the conditioned coset only. On the other addresses it rests on the
  check of the `add_scaled` macro on all canonical inputs in the `rees_circuit_arith` report, and on the grading.
  `lemma_hypotheses_check` checks only that the steps touching the address are this source's own instrument steps.
- Lemma A (3) and Lemma B (3) rest on the symbolic merge proof for child 0 of each block (`prove_controlled_merge`)
  together with `block_structure` and the relabeling of children inside a block as assembled by `TerminalSample`;
  that the assembled ctrl_i, bch_i, ctrl_i^-1 of child i > 0 are the relabelled child-0 lists is read off the code,
  and is checked on the reachable states by K3/K4 (every hub), not on all inputs.

## 8. Claim gates

No claim gate changes. `coherent_receiver_implemented`, `general_instances`, `qft_synthesised` and
`speedup_claim_allowed` stay False in `STATUS` of `rees_circuit_mono.py` and `rees_circuit_mono_c3.py`, and in
every run JSON. The results are finite computations on fixed instances (n4(F_5), n4(F_7) Z(G), Heis(F_3)), plus two
lemmas proved here by hand. They say nothing asymptotic. The explicit QFT is not in them (item 2).

## 9. Proposed text for "Gate-level control" (AI-checked, pending human review)

Each old sentence is quoted exactly as it stands in `docs/papers/rees-hsp/main.tex` (paragraph "Coherent-label
backends", line 851, and paragraph "Scope", line 855). The replacements avoid \mathsf, \mathrel, \begingroup and \aa. Line numbers are those of main.tex at 06:45 on 5 November 2026; main.tex is being edited by others, so locate each sentence by its text (each occurs exactly once, checked at that time).

**(a) Line 851, replace**

> Over $\mathbb{F}_5$ the conditional readout law is exactly uniform on $\hh^\perp$ for all $56$ terminal samples of seven of the nine subgroups, the five nonnormal ones included, and all seven seeded runs recover $\hh$; the other two, $\gamma_2(\mathcal{L})$ and $\langle e_1+e_2,e_3\rangle$, need a factor of $4.9\cdot10^7$ basis states and were not run.

**by**

> Over $\mathbb{F}_5$ the conditional readout law is exactly uniform on $\hh^\perp$ for all $56$ terminal samples of seven of the nine subgroups, the five nonnormal ones included, and all seven seeded runs recover $\hh$. With nothing measured before the readout, two symmetries make the computation fit (report \file{research/audits/reviews/2026-11-05-rees-receiver-round3.md}; proved, and finite computation, AI-checked, pending human review). After its oracle calls, the address of a top source is touched only by its instrument, a central translation, and by its merge, a right translation, and its oracle outputs are never touched again; both commute with left translation, so conditioning the oracle outputs on the key of one coset of $\exp(\hlift)$ leaves the output law unchanged. Likewise, once the reduced state of each $Q$ of grade two is $\rho_{H_2}$, that $Q$ may be replaced by the uniform state of one coset of $H_2$. Every gate of one subtree of grade two and of the root then acts on one exact state over $\mathbb{Z}[\zeta_5]$, written as an orthogonal sum over the values of the labels and $Q$, at most $390625$ terms at grade three. The other five subtrees equal the first up to a bijection of wires, which is checked; for five of the subgroups they were also simulated. For $\gamma_2(\mathcal{L})$ and $\langle e_1+e_2,e_3\rangle$, whose grade-two labels are deterministic, this gives the exact output law of the whole circuit, and it is uniform on $\hh^\perp$. For the other seven subgroups the readout law conditioned on stated grade-two labels is exactly uniform on $\hh^\perp$ for each of the $13$ label tuples tried, out of $5^6$ or $25^6$.

**(b) Line 851, replace**

> In the sampled-trajectory mode, a pure-state form of the source check, with a clean workspace, on every source catches one changed oracle entry in every terminal sample, $60$ each on three subgroups over $\mathbb{F}_3$ and $4$ each on two over $\mathbb{F}_5$, where the readout test caught it in at most one of $60$ trajectories at $H=Z(G)$ over $\mathbb{F}_3$; at $c=3$ the merges are still checked only through the readout law and the module checks above.

**by**

> In the sampled-trajectory mode, a pure-state form of the source check, with a clean workspace, on every source catches one changed oracle entry in every terminal sample, $60$ each on three subgroups over $\mathbb{F}_3$ and $4$ each on two over $\mathbb{F}_5$, where the readout test caught it in at most one of $60$ trajectories at $H=Z(G)$ over $\mathbb{F}_3$. At $c=3$ over $\mathbb{F}_5$ the same comparisons now run on the exact state of the computation above, for every hub: the source state, the instruments, the workspace at every merge component, every child after each merge block against its right translation by $-\delta_s(\sigma(q))$ with the reference witness, the reduced state of each $Q$ of grade two against $\rho_{H_2}$ for every label pair, and that of the root $Q$ against $\rho_{H_1}$; they hold for all nine subgroups, the grade-three merges on one of the six identical subtrees for four of them and on all six for the other five, and the checks at the root on every label tuple run. Of $39$ deterministic mutant runs at $c=3$ on $\langle e_2\rangle$, which change one oracle entry, drop one gate in a module or modify the merge block ($15$ in a subtree of grade two, and $12$ at the root for each of two label tuples), $17$ fail one of these checks, $7$ stop at a structural guard of the simulation, and in the other $15$ the dropped gate never acts on the reachable state. On the zero label tuple the four failing root mutants that reach the readout, among them the merge with the opposite sign of the translation, have an exactly uniform output law.

**(c) Line 855, replace**

> Every exact simulation uses the exact Fourier transform; the monolithic simulation of \file{theorems/rees_circuit_mono.py} gives the exact output law over $\mathbb{F}_3$ and samples the trajectories of its early measurements over $\mathbb{F}_5$, and it covers the coherent-label circuits over $\mathbb{F}_3$ and $\mathbb{F}_5$ only.

**by**

> Every exact simulation uses the exact Fourier transform; the monolithic simulation of \file{theorems/rees_circuit_mono.py} gives the exact output law over $\mathbb{F}_3$, and over $\mathbb{F}_5$ for the two subgroups with deterministic grade-two labels and conditionally on stated grade-two labels for the other seven, through the two symmetries above; over $\mathbb{F}_7$ it covers the top sources of the fifth backend, run from their gate lists on all $7^7$ addresses for all nine subgroups, and for $H=Z(G)$ the merges at both grades, with the readout law exactly uniform on $\hh^\perp$ conditionally on three stated grade-two label tuples.

## 10. Next hard question

**Is the conditional Phase-B law independent of the grade-2 label tuple by a proved symmetry?** If it is, the
exact law of the whole circuit would follow for the seven subgroups with K_2^perp != 0, from one representative
per orbit. One candidate is the action of translations of K_2^perp on each child's label, together with F_p^*
scaling of the witness. Running every tuple by brute force would take 5^6 · 30 s (about 5 days) for Z(G) alone.

- Next step: state the symmetry and prove it as Lemma C, in the style of Section 2. Check its hypotheses with
  `lemma_hypotheses_check` and add a `--tuples orbit-reps` mode to `rees_circuit_mono_c3.run_cli`.
- Expected artifact: `B_orbit_representatives.json`, with one run per orbit for each of the seven subgroups.
- Acceptance test: every representative has all checkpoints and an exactly uniform law. A negative control (a
  non-symmetric label perturbation, e.g. the g_sign mutant) breaks the claimed equality of the per-tuple
  signatures within an orbit.
- Second question: Phase A at p = 7 for the eight other subgroups. This needs about 4 · 10^7 hubs, or up to
  4 · 10^10 child rows. It needs either a further symmetry on the grade-3 labels or a compiled kernel.

## 11. Independent review (fresh general-purpose subagent) and fixes

A fresh subagent checked the report, the code and the JSONs adversarially. It was given the files, `research/STATE.md`
and the interpreter, and none of the conclusions. It ran its own scripts (scratch only; no repo edits).

**Verdict (quoted in substance):** nothing blocking. The two proofs are correct. W L_g = L_g W holds because the
instrument is x -> x z^-1 with z central, U_SDE acts only on labels and the witness, and the merge x -> x·t(s, q)
has t independent of x. Applying Lemma A first and then Lemma B to the conditioned circuit is valid, and checking
K5_2 for every grade-3 label tuple is stronger than Lemma B needs. K5_2 is not vacuous: it needs exactly
nQ·|H_2| unique pairs, all inside left cosets, with one positive rational value. Every number spot-checked
matches the JSONs: hubs, rows, timings, 13 distinct tuples with one law signature per subgroup, the 162/324/162/162
source checks at p = 7, the 37/37 Heis comparisons, and the mutant totals. The Section 9 old sentences each occur
once in main.tex, and the new text uses only defined macros. "The claims are supported as labelled, once the
wording is fixed."

**The reviewer's own negative controls** (n4(F_5), node 0):
- On <e2>, with g = 49993, a coset not used in the report (gS != Sg), the conditioned address state was replaced
  by the left coset gS and then by the right coset Sg.
  - gS gives the baseline `rho_Q2`, and K5_2 passes 25/25. K1c and K2 fail, as they must, since their references
    are built for S.
  - Sg changes `rho_Q2`, and K5_2 fails.
  - On Z(G), where S is normal, both give the baseline.
  - So the left-coset symmetry is not automatic, and K5_2 catches a wrong address state.
- Hub range [0, 100) on Z(G) passes with the same `rho_Q2_signature` (see finding 3).
- The direct Gram check on Z(G) is true.
- Phase-B join logging on <e2>, on the zero tuple and one random tuple: 1 and 3 joins, all inside one child. The
  law signature equals the report's.

**Findings and what was done:**

| # | Finding | Severity | Fix |
|---|---|---|---|
| 1 | "No hub join" in Section 3.3 is false: `hub_joins` is 1-6 in 66 Phase-B runs. Each logged join merges factors within one Q_2 (with workspace), never two children. | should-fix | Wording fixed in Sections 1.3 and 3.3, with what `hub_joins` counts. No result is affected (a join of two children makes K4 fail). |
| 2 | The direct Gram cross-check had no artifact (only a slow test for trivial). | should-fix | Run and saved: `A_direct_gram_trivial_ZG_node0.json` (trivial [True, True], Z(G) [True]). |
| 3 | The hub-range K5_2 evidence is circular: K5_2 does not depend on the range, so equal signatures hold by construction. | should-fix | Section 3.2 now says so. `phase_a` writes `K5_2_conditional_on_K4_on_other_hub_ranges`. New `combine_hub_ranges` (partition, every range passes, identical signature) is tested, and its output is `closure_hub_ranges_combined.json` (all true). |
| 4 | Overstated wording: the Section 0 headline "Done for all 9"; Section 1.4 "final QFT gate by gate" (it is applied analytically from the Gram matrices); proposed (a) "Every gate then acts" (for 4 subgroups, 5 subtrees are covered by relabeling); proposed (b) "hold for all nine" (root checks only on the tuples run). | should-fix | All four reworded. |
| 5 | `lemma_hypotheses_check` accepted any "instrument*" component touching the address. The instrument acting on addresses outside the conditioned coset rests on another report. | should-fix | The check now requires the source's own instrument steps (inside the instrument steps on its own label register, touching no other child's address) and, for Q_2, the node's own grade-2 instrument range. New negative control: node 0's Q_2 touched inside node 1's instrument. `relabeling.json` and `f7_relabeling.json` were rerun (ok). The caveat is added to Section 7. |
| 6 | Minor: an empty checkpoint list reported `all([]) = True`; `phase_b` had no non-empty guard and no `checkpoint_counts`; "equivalent" overclaimed; a typo "2.6 GB.."; "conditional readout law" is used in two senses. | minor | Empty list is now None (check not reached). `phase_b` requires every checkpoint True and records `checkpoint_counts`. The definition of an equivalent mutant is restated in Section 5. Typo fixed. The new proposed text says "conditioned on stated grade-two labels". |

After the fixes the final command gives 69 passed, 4 skipped, and the 3 round-3 slow tests pass again
(3 passed in 218 s, `pytest_slow_round3.txt`). The run JSONs from before fix 6 still carry the old `True` for checkpoint lists that were never
reached. That affects only mutant rows, where the run fails anyway, and every pass flag quoted in this report
comes from a run with all lists non-empty: `all_checkpoints_pass` required non-empty lists from the start in
Phase A. In Phase B the stricter rule (every checkpoint True) passes on the re-run Phase-B tests (<e2> zero tuple; gamma_2 in the slow set).
