# Rees HSP receiver, round 2: exact output law at c = 2, checkpoints, Lean check of (R), class-five seeded runs

5 November 2026 (overnight). AI-only session (Claude Code, Opus 5.5). Not human review.
Follows `2026-11-05-rees-receiver-sims.md` and its check `2026-11-05-rees-receiver-sims-check.md`
(REES_FULL_CONTINUATION.md item 7, "Still lacking").

Labels used below:
- **[finite computation]**: a complete computation on the stated finite instances, exact in integer, permutation
  or Z[zeta_p] arithmetic;
- **[sampled]**: exact on a stated random subset only;
- **[Lean-checked]**: a Lean 4 theorem (Lean v4.35, Mathlib), `lake build --wfail`, standard axioms only;
- **[argued]**: reasoning, not machine-checked.

Everything is AI-checked, pending human review.

Files written (nothing else was edited; no .tex, registry JSON, claim gate, AGENT_HANDOFF.md or STATE.md was
touched; nothing committed; no network):
- `theorems/rees_circuit_mono.py`: new section "round 2". It holds HubState, `exact_level0_law` with checkpoints
  K0-K5, `plain_level0_law`, `exact_report`, `negative_controls`, `trajectory_controls` and checkpoint KS. One new
  keyword, `source_check=False`, in `run_terminal_sample`; the default behaviour is unchanged. Module docstring
  updated.
- `theorems/rees_circuit_exhaustive.py`: `power_class_sde`, `solve_sde_pc`, `run_algorithm_sparse_pc`,
  `seeded_report`; the docstring of (R) is updated.
- `formal/Formal/ReesMergeReduction.lean`: a new Lean module. `Formal.lean` does not import it yet (that root
  file was left alone).
- `tests/test_rees_circuit_round2.py` (new).
- This report and the folder `2026-11-05-rees-receiver-round2/` (run JSONs, logs, `run_commands.sh`). The runs of
  Sections 1-2 were redone after the independent check (Section 10); the earlier outputs are kept as
  `*_v3_beforeReview.*`. The catch counts did not change.

The claim gate `coherent_receiver_implemented` stays false: it is false in both STATUS dicts, and a test checks
this.

## 0. Answers

| # | Item | Result | Label |
|---|---|---|---|
| 1 | Exact output law of the whole circuit, Heis(F_3) | **Done for all 19 subgroups.** It is computed with nothing measured before the readout (level 0), so it is the circuit's output law, not one sampled trajectory. It is exactly uniform on h^perp for all 19. It covers all 13 small-S subgroups that had no level-0 run. For the 6 large-S subgroups it agrees with the direct level-0 computation. | finite computation |
| 2 | Intermediate-state certification | **Done at c = 2.** Checkpoints K0-K5 compare the monolithic state with module-level reference states computed from h. Of 92 genuine mutant runs (100 minus 8 runs of two MergeBlock flags that do not change the assembled program), 72 are caught, deterministically, and the other 20 leave the final joint state bit-for-bit unchanged (equivalent mutants); 24 of the caught ones have an exactly uniform output law, so no readout test could see them. One changed oracle entry at H = Z is caught on every run (K1), and also in every sampled terminal sample by the per-source checkpoint KS (Heis and n4(F_5)): 60/60 and 4/4 terminal samples, no false alarm (the readout test: 0/60 at H = Z). | finite computation |
| 3 | Machine check of step (R) | **Lean-checked.** The pointwise identity "merged product = zero-label product" is proved for every label tuple and every witness, from the hypotheses that the exact checks (E2) and (E3) establish. One link remains code reading: the merge output is a function of that product. | Lean-checked; link argued |
| 4 | Seeded runs at class five, n6(F_7) | **14 of 14 recover log H** (7 of 8 subgroups, 2 seeds; gamma_4 not run). The top state is the exact coset density, as in round 1. They use a complete power-class search: at grade 3 it has 3^10 = 59 049 points instead of 7^10, and it matches the brute-force witness set exactly on tests. | finite computation, seeded |
| 5 | Two largest n4(F_5) subgroups | **Not attempted.** The machine was loaded (load average 60-140), and a memory-reduced factor format would need new amplitude storage. | none |

## 1. The exact output law of the whole terminal sample at c = 2

### 1.1 Method

The object is the same as in round 1: the assembled coherent terminal sample of
`rees_circuit_coherent.TerminalSample` for Heis(F_3) (182 qubits, 115 282 X/CX/CCX/SWAP gates, 24 exact
QFT_3, 6 oracle calls). The flattened gate list is the same, from `compile_program`, and every gate is executed in
program order.

Steps 0-77 run on the round-1 `FactorState` with nothing measured. These are the three sources, their oracle calls,
the three instruments and the preparation of Q. The state is then a product of three child factors (address,
oracle outputs, label; at most 729 rows each) and the uniform Q.

At step 77 the state is rewritten **exactly** as an orthogonal sum over the basis values h of the hub wires: the
three instrument labels and the root Q (`HubState.split`):

    |Psi> = sum_h |c(h)> (x) prod_f |psi_f(h)>,

The pieces of this sum are:
- c(h) gives a basis value for every wire not held in a factor: the hub wires, and every wire whose value is a
  function of h, such as the witness register S and the clean workspace;
- each factor stores its rows for all h at once.

This is a change of representation. It is not a measurement and not an approximation. All later gates (steps
78-324: U_SDE, the witness-controlled BCH merges, U_SDE^-1) are applied to it exactly:
- a gate on hub-classical wires acts on c(h);
- a gate with a local control and a hub-classical target first moves that target into the factor;
- factors that one gate needs together are joined, for each h, by a tensor product;
- a factor wire that is constant within every h returns to c(h).

On the gate list, the hub wires are used after step 77 only as controls until the final QFT
(`hub_condition`: true). So the three children never join: `hub_joins = 0` for every subgroup. The state then
needs 729 x (3 x at most 243) rows instead of one factor of 27·243^3 = 3.9e8 rows.

The readout law is computed exactly from the Gram matrices of the factors, in Z[zeta_3]:

    P(y) = sum over (h, h') with c(h) = c(h') off Q of  zeta^(y·(q_h - q_h')) · prod_f <psi_f(h')|psi_f(h)>.

**Relation to the early-measurement trajectories [argued, standard].** The round-1 levels 1 and 2 measure, early:
- oracle outputs and children, which are never touched again;
- labels, which are used only as controls afterwards.

The level-0 law computed here is the trace over all of these registers. It is therefore the average over all
early-measurement branches of those circuits, with the label branches summed explicitly: each label tuple is one
group of hubs, and K5 checks every group separately. So the trajectory average is computed exactly. The step from
"measure an untouched register" to "trace it out" is the standard identity, and the schedule verifier checks its
condition.

### 1.2 Validation of the method

- **HubState against a dense state vector [finite computation, tests].** Random 8-qubit circuits: Hadamards and
  permutation gates, a split over 3 random wires, then 40 permutation gates on the hub representation, with hub
  wires also used as targets. 8 seeds; the represented state equals the dense one.
- **Gram matrices against dense inner products** on a random p = 3 program with 3 hubs: equal up to one positive
  scale.
- **Two independent exact computations agree [finite computation].** For the six subgroups containing Z, a
  plain level-0 `FactorState` run (no split, one product of factors) gives a law proportional to the hub law
  (`plain_level0_law_equal: true`, 6 of 6). The same agreement holds on two mutants whose law is **not** uniform
  (one QFT of the preparation of Q removed, at H = Z and at H = <(1,0,0), Z>) and on one with a uniform law (one
  CCX dropped in U_SDE, H = Z) (test `test_hub_law_matches_plain_law_on_a_mutant`).

### 1.3 Results (`exact_heis_f3_level0.json`; rerun after the review: 172 s wall on the loaded machine, peak RSS 0.51 GB)

| H | normal | \|S\| | hubs | label tuples | peak rows | exact law uniform on h^perp | all checkpoints | plain level-0 agrees | s |
|---|---|---|---|---|---|---|---|---|---|
| trivial | yes | 1 | 729 | 27 | 177 147 | yes (27 x 10460353203) | yes | (does not fit) | 12 |
| 12 non-normal <v> (v = (1,a,b), (0,1,b)) | no | 3 | 729 | 27 | 177 147 | yes (9 equal masses) | yes | (does not fit) | 8-14 each |
| Z = <(0,0,1)> | yes | 9 | 27 | 1 | 2 187 | yes | yes | yes | 0.3 |
| <(1,0,0),Z>, <(1,1,0),Z>, <(1,2,0),Z>, <(0,1,0),Z> | yes | 27 | 27 | 1 | 2 187 | yes | yes | yes | 0.3 each |
| G | yes | 81 | 27 | 1 | 2 187 | yes (point mass at 0) | yes | yes | 0.3 |

All 19 laws are rational and supported exactly on h^perp, with equal masses. Two seeded recoveries per subgroup,
sampled from the exact law, recover log H (38 of 38). The 13 subgroups with small S had no level-0 run before;
round 1 needed 3.9e8-row factors for them.

## 2. Intermediate-state certification

### 2.1 Checkpoints of `exact_level0_law` (deterministic, every hub)

The reference states are computed from h by module-level formulas, never from the oracle or the gate lists:

| | where | compared with |
|---|---|---|
| K0 | after every source and every instrument | arithmetic ancillas, evaluation workspace and block pool are constant 0 |
| K1 | after each source (both oracle calls) | the reduced density of the address is proportional to the coset density of S = exp(h~) in G_2: [x^-1 x' in S] (left cosets from `stage_indices`) |
| K2 | after each instrument | the reduced density of (address, label) is proportional to the instrument formula applied to that density. The formula is psi(x', lam; k) = sum_z zeta^(-lam·z) [coset(x'z) = k], with x' = x z^-1 and z central |
| K3 | at every component boundary of the merge block | no workspace wire is entangled (all are functions of the labels and q). After child i's (ctrl_i, bch_i, ctrl_i^-1), child i is already its reference translation (as K4), for each of the 3 children (before the review only children 0 and 1 were checked here: finding 1) |
| K4 | after the merge block, for every hub (labels, q) | each child equals its pre-merge state right-translated by -delta_(s_i)(sigma(q)). Here s is the independent reference witness `sde_reference` of the label values at the split, and it is checked to be nonzero with sum_i s_i^2 lam_i = 0 for every hub. The translation is computed with the group law `GroupLaw.mul` and `_witness_bound_g`. Labels and Q are unchanged; S and all workspace are 0. K4 is **relative**: it compares with the state at the split, not with a state computed from h. A corruption already present at the split passes K4 and is left to K1/K2 (sources, instruments) and K5 |
| K5 | before the final QFT | for every label tuple separately, and in total, the reduced state of Q is proportional to rho_(H_1) (`rho_target`). The label law is uniform on (K^perp)^3. The readout law is exactly uniform on h^perp |

All checkpoints hold for all 19 subgroups (Section 1.3), with no false alarm.

### 2.2 Negative controls (`negative_controls_exact.json`) [finite computation]

The mutants run on four subgroups: trivial, <(1,0,0)> (non-normal), Z and <(1,0,0),Z>. Each mutant is one of:
- one changed oracle entry, f(x0) := f(e) for the first x0 not in H;
- one dropped CX or CCX, the first or the middle one of its kind, in the first step of each component;
- one of the four MergeBlock mutations.

Every run is deterministic: a mutant is caught or not. A mutant that no check catches is then compared with the
unmutated run. If its final joint state is bit-for-bit identical (`state_signature`), it is an **equivalent
mutant** on that instance: no test of the circuit's action can see it.

Columns: H = 1 (trivial), <(1,0,0)>, Z = <(0,0,1)>, <(1,0,0),Z>. "caught: Kn" lists the failed checkpoints;
"workspace" is the end-of-run clean-workspace check; "(law uniform)" means the exact output law of the mutant is
still exactly uniform on h^perp, so no readout test, sampled or averaged, can see it. "[then over budget at step n]":
the mutant's state outgrows the 8e6-row budget after the failing checkpoint, so the law is not computed (detection
does not depend on it). Baseline (unmutated): all checks pass on all four subgroups.

| mutant | 1 | <(1,0,0)> | Z | <(1,0,0),Z> |
|---|---|---|---|---|
| oracle entry 1 | caught: K1,K2,K5 (law not uniform) | caught: K1,K2,K5 (law not uniform) |  |  |
| oracle entry 3 |  |  | caught: K1,K2,K5 (law not uniform) | caught: K1,K2,K5 (law not uniform) |
| drop gate source_evaluation cx first | caught: K0,workspace (law uniform) | caught: K0,workspace (law uniform) | caught: K0,workspace (law uniform) | caught: K0,workspace (law uniform) |
| drop gate source_evaluation cx middle | not caught; final state identical | not caught; final state identical | not caught; final state identical | not caught; final state identical |
| drop gate source_evaluation ccx first | not caught; final state identical | not caught; final state identical | not caught; final state identical | not caught; final state identical |
| drop gate source_evaluation ccx middle | caught: K0,K1,K2 [then over budget at step 56] | caught: K0,K1,K2 [then over budget at step 56] | caught: K0,K1,K2 [then over budget at step 73] | caught: K0,K1,K2 [then over budget at step 73] |
| drop gate instrument cx first | caught: K2,K3 [then over budget at step 194] | caught: K2,K3 [then over budget at step 194] | caught: K2,K3 [then over budget at step 225] | caught: K2,K3 [then over budget at step 225] |
| drop gate instrument cx middle | caught: K0,K1,K2 [then over budget at step 56] | caught: K0,K1,K2 [then over budget at step 56] | caught: K0,K1,K2 [then over budget at step 73] | caught: K0,K1,K2 [then over budget at step 73] |
| drop gate instrument ccx first | caught: K0,K1,K2 [then over budget at step 56] | caught: K0,K1,K2 [then over budget at step 56] | caught: K0,K1,K2 [then over budget at step 73] | caught: K0,K1,K2 [then over budget at step 73] |
| drop gate instrument ccx middle | caught: K0,K1,K2 [then over budget at step 56] | caught: K0,K1,K2 [then over budget at step 56] | caught: K0,K1,K2 [then over budget at step 57] | caught: K0,K1,K2 [then over budget at step 57] |
| drop gate sde_grade2 cx first | caught: K3,K4,workspace (law uniform) | caught: K3,K4,K5,workspace (law not uniform) | not caught; final state identical | not caught; final state identical |
| drop gate sde_grade2 cx middle | caught: K3,K4,K5,workspace (law not uniform) | caught: K3,K4,K5,workspace (law not uniform) | caught: K3,K4,K5,workspace (law uniform) | caught: K3,K4,K5,workspace (law not uniform) |
| drop gate sde_grade2 ccx first | caught: K3,K4,K5,workspace (law not uniform) | caught: K3,K4,K5,workspace (law not uniform) | caught: K3,K4,K5,workspace (law uniform) | caught: K3,K4,K5,workspace (law uniform) |
| drop gate sde_grade2 ccx middle | caught: K3,K4,K5,workspace (law not uniform) | caught: K3,K4,K5,workspace (law not uniform) | not caught; final state identical | not caught; final state identical |
| drop gate witness_control_grade2 cx first | caught: K3,K4,workspace (law uniform) | caught: K3,K4,workspace (law uniform) | caught: K3,K4,workspace (law uniform) | caught: workspace (law uniform) |
| drop gate witness_control_grade2 cx middle | caught: K3,K4,K5,workspace (law uniform) | caught: K3,K4,K5,workspace (law not uniform) | caught: K3,K4,K5,workspace (law uniform) | caught: K5,workspace (law not uniform) |
| drop gate witness_control_grade2 ccx first | not caught; final state identical | not caught; final state identical | not caught; final state identical | not caught; final state identical |
| drop gate witness_control_grade2 ccx middle | caught: K3,K4,K5,workspace (law uniform) | caught: K3,K4,K5,workspace (law not uniform) | caught: K3,K4,K5,workspace (law uniform) | caught: K3,K4,K5,workspace (law not uniform) |
| drop gate bch_merge_grade2 cx first | caught: K3,K4,workspace (law uniform) | caught: K3,K4,workspace (law uniform) | caught: workspace (law uniform) | caught: workspace (law uniform) |
| drop gate bch_merge_grade2 cx middle | caught: K3 [then over budget at step 189] | caught: K3 [then over budget at step 189] | caught: K3 [then over budget at step 220] | caught: K3 [then over budget at step 220] |
| drop gate bch_merge_grade2 ccx first | not caught; final state identical | not caught; final state identical | not caught; final state identical | not caught; final state identical |
| drop gate bch_merge_grade2 ccx middle | caught: K3 [then over budget at step 189] | caught: K3 [then over budget at step 189] | caught: K3 [then over budget at step 220] | caught: K3 [then over budget at step 220] |
| MergeBlock g_sign | caught: K3,K4 (law uniform) | caught: K3,K4 (law uniform) | caught: K3,K4 (law uniform) | caught: K3,K4 (law uniform) |
| MergeBlock skip_bennett | caught: K3 [then over budget at step 187] | caught: K3 [then over budget at step 187] | caught: K3 [then over budget at step 216] | caught: K3 [then over budget at step 216] |
| MergeBlock skip_ctrl_inv | not caught; final state identical | not caught; final state identical | not caught; final state identical | not caught; final state identical |
| MergeBlock skip_sde_inv | not caught; final state identical | not caught; final state identical | not caught; final state identical | not caught; final state identical |

Totals: 100 runs (25 mutants x 4 subgroups).
- The flags `skip_ctrl_inv` and `skip_sde_inv` of `MergeBlock` change only `MergeBlock.prog`, which
  `TerminalSample` does not use (it assembles U, ctrl_i, bch_i, ctrl_i^-1, U^-1 itself): the assembled program is
  identical to the unmutated one (checked), so these 8 runs are not mutations. Of the other **92 runs, 72 are
  caught and 20 are equivalent mutants** (final joint state identical to the unmutated one: the dropped gate's
  controls are 0 on every reachable state). **No run changes the final state without being caught.**
- **24 caught runs have an exactly uniform output law**: the readout law alone, even averaged over all
  trajectories, cannot see them. Among them: `g_sign` on all four subgroups (caught by K3/K4: the children are
  translated by +delta_s(sigma(q)), and Q's reduced state at grade one is unchanged, as round 1 conjectured);
  the first CX of `source_evaluation` (dirty evaluation workspace, K0); several witness-control, BCH and U_SDE
  drops at H = Z and <(1,0,0),Z> (K3/K4, workspace).
- One changed oracle entry: caught on every subgroup (K1, K2, K5). At H = Z, where round 1's readout test caught it
  in 1 of 60 trajectories, the exact output law is in fact **not** uniform, and K1 fails deterministically.
- The rerun after the review (K3 on all three children, the K4 witness check) gives exactly the same failed-check
  lists for all 100 runs as `negative_controls_exact_v3_beforeReview.json`.
- Earlier versions of this run (kept in the folder) had no K0/K3: 12 runs then ended over budget before any check
  failed (`negative_controls_exact_v2_beforeK3.json`); with K3 all 12 are caught.

### 2.3 Sampled trajectories with checkpoint KS (`trajectory_controls_*.json`) [sampled trajectories, exact per trajectory]

KS is the source check of K1, done per trajectory in the level-2 mode. The oracle-output measurements are delayed
to the source's last oracle call (`delay_oracle_measurements`). This is still a valid schedule: no later step
touches an oracle output, and the number of measured registers is unchanged. Before anything is measured, the
source's joint state must be sum_x |x>|key(x)>:
- every workspace wire (arithmetic ancillas, evaluation workspace, block pool) is the constant 0 (added after the
  review, finding 4: without it a dropped CX in a source evaluation passed KS);
- every address appears exactly once, with equal amplitudes;
- no other wire is entangled;
- the fibres of the key are exactly the left cosets of exp(h~).

KS runs at every top-grade source of every terminal sample, which makes it deterministic per terminal sample.

| instance | oracle | terminal samples | caught by KS | caught by the readout-law test | s |
|---|---|---|---|---|---|
| Heis(F_3), <(1,0,0)> | unmutated | 60 | 0 | 0 | 6.3 |
| Heis(F_3), <(1,0,0)> | one entry changed (x0 = 1) | 60 | **60** | 21 | 6.2 |
| Heis(F_3), Z | unmutated | 60 | 0 | 0 | 5.5 |
| Heis(F_3), Z | one entry changed (x0 = 3) | 60 | **60** | 0 | 5.4 |
| Heis(F_3), <(1,0,0),Z> | unmutated | 60 | 0 | 0 | 6.2 |
| Heis(F_3), <(1,0,0),Z> | one entry changed (x0 = 3) | 60 | **60** | 39 | 6.2 |
| n4(F_5), <e2> (non-normal) | unmutated | 4 | 0 | 0 | 21.1 |
| n4(F_5), <e2> | one entry changed (x0 = 1) | 4 | **4** | 1 | 20.8 |
| n4(F_5), Z(G) | unmutated | 4 | 0 | 0 | 87.3 |
| n4(F_5), Z(G) | one entry changed (x0 = 5) | 4 | **4** | 0 | 84.9 |

[sampled trajectories; KS itself is an exact check of each source, 3 per terminal sample over F_3, 12 over F_5.
Rerun after the review, with the workspace condition: the same counts.]
So the corruption that the readout test caught in 1/60 trajectories at H = Z (round 1) and 0/60 here is caught in
every terminal sample, with no false alarm in 188 unmutated terminal samples (3 x 60 + 2 x 4). At c = 3 only the sources get a
deterministic checkpoint; the merges at c = 3 are still certified by the readout law and the module checks.

## 3. Step (R): Lean check

`formal/Formal/ReesMergeReduction.lean` (namespace `QSearch.ReesMergeReduction`; imports only
`Mathlib.Data.ZMod.Basic`, the two BigOperators files, `LinearIndependent.Defs` and `Module.BigOperators`):

- `witness_coords`: if sum_i s_i^d • lam_i = 0 with lam_i = sum_j c_ij b_j and b linearly independent, then
  sum_i s_i^d c_ij = 0 for every j.
- `exponent_cancels`: under (E3) at a point and the coordinate witness equation, the total twist exponent
  sum over {i : s_i != 0} of sum_j c_ij W_j(delta_(s_i) g) is 0. The inactive indices drop out because
  0^d = 0 for d >= 1.
- `merge_product_eq`, `merge_product_eq_of_labels` (**step (R)**). The hypotheses are:
  - (E2) phi c g = zeta^(sum_j c_j W_j(g)).val · phi 0 g for all coordinate vectors c and all g;
  - phi 0 = 0 off supp0;
  - (E3) on Sigma_T = {g : delta_(s_i) g in supp0 for all active i}, W(delta_(s_i) g) = s_i^d tau(g);
  - zeta^p = 1.

  The conclusion holds for **every** label tuple c : Fin M -> Fin k -> ZMod p and **every** witness s:
  prod over {i : s_i != 0} of phi (c i) (delta (s i) g) = prod over {i : s_i != 0} of phi 0 (delta (s i) g),
  for all g. Off Sigma_T both sides are 0. On Sigma_T the phases multiply to zeta^(0.val) = 1
  (`prod_pow_val`, `pow_val_add`).
- `zero_product_indicator`: if phi 0 is a constant kappa on its support, the zero-label product is
  kappa^#A · 1_(Sigma_T). It therefore depends on the witness only through its value set T and the count #A.

`lake build --wfail Formal.ReesMergeReduction`: success (`lean_build.out`). `#print axioms` for all five
theorems gives `[propext, Classical.choice, Quot.sound]` (`lean_axioms.out`).

**How the hypotheses are met (code, `rees_circuit_exhaustive.py`) [finite computation + code reading].**

The Lean phi c is the conditioned branch (scale included) of the label lam = sum_j c_j b_j, with b the rref
basis of K^perp. (E2) is `branch_structure`:
- every lam of the span `allowed_labels` has the support of phi_0;
- `_row_exponents` checks scale·V = zeta^e · scale_0·V_0 row by row;
- e is checked equal to W·c mod p.

(E3) is `subset_checks`. For every value set T with |T| <= min(M, p-1), it computes Sigma_T and checks that
t^(-d) W(delta_t g) is the same for all t in T. tau(g) is that common value. "phi_0 constant on its support" is
checked as well.

**What is not in Lean [argued, code reading].** `SparseEngine.merge` computes exactly the product over the active
children, F(g) = prod phi_i(delta_(s_i) g) with scales, and its output (descent to G_(d-1) and normalisation) is
a function of F. Given the Lean identity, every (label tuple, witness) pair therefore gives the zero-label output.
`zero_product_indicator` shows that this output depends on T only, and (E3) checks it to be rho_(H_(d-1)) for
every T.

So the extension from (E1)-(E3) to all (p^M - 1)|K^perp|^(M-1) pairs is now Lean-checked except for this
reading of `merge`. As before, it is the Schur-product channel fed by the proved merge gate lists; it is not a
gate-level simulation at class four or five.

## 4. Seeded recovery runs at class five (`seeded_n6_f7.json`)

**Solver [finite computation, tests].** `power_class_sde(labels, d, p)`:
- It enumerates u in P^M, with P = {x^d : x in F_p} the d-th powers and 0, keeps the nonzero u with
  sum u_i lam_i = 0, and lifts each u_i to an s_i with s_i^d = u_i.
- The search is complete, so it finds a witness whenever one exists.
- It draws the witness with weight prod_i #{s_i : s_i^d = u_i}. That is the uniform law on all witnesses, the law
  of `brute_force_sde`.
- n6(F_7) grade 3 (d = 3, M = 10, cubes {0, ±1}): 3^10 = 59 049 points instead of 7^10 = 2.8e8. Grade 2: 4^9.
  Grade 4: 4^5.
- At grade 5 (kappa = 1, M = 2) the existing IS solver applies and is used.
- Checks: in `test_power_class_solver_complete`, 60 random cases (p in {3, 5, 7}, d in {2, 3, 4, 5}): the witness
  count equals `all_witnesses` exactly, and the drawn s lies in that set. In an interactive check that left no
  artifact, 60 000 draws on one instance hit 18 628 of its 19 494 witnesses (the uniform law predicts about
  18 596). The independent reviewer (Section 10) reproduced completeness on 200 fresh cases and found
  chi2/dof = 1.11 for uniformity on a 54-witness instance.
- `run_algorithm_sparse_pc` re-checks the witness equation at every merge.

**Runs.** The top state is the exact coset density of exp(h~), computed from h, not from oracle queries (as for
F_7 in round 1, Imprecision I1 there). These runs therefore test the descent from the correct source, with
sampled labels, classical witnesses and the Schur-product merges of the proved gate lists. Each run uses 10
terminal samples, 9000 top sources and 45 000 (counted) oracle queries.

n6(F_7), [e1,e_i] = e_(i+1) (i = 2..5), arities (M_5, M_4, M_3, M_2) = (2, 5, 10, 9), seeds 1 and 2.

| H | normal | recovered (seed 1, 2) | witnesses per run: IS d5 / power-class d4 / d3 / d2 | s per run |
|---|---|---|---|---|
| trivial | yes | yes, yes | 4500 / 900 / 90 / 10 | 39, 22 |
| <e1> | no | yes, yes | 4500 / 900 / 90 / 10 | 29, 28 |
| <e2> | no | yes, yes | 4500 / 900 / 90 / 10 | 27, 29 |
| <e3> | no | yes, yes | 4500 / 900 / 90 / 10 | 36, 44 |
| Z(G) = <e6> | yes | yes, yes | 4500 / 899 (+1 IS) / 90 / 10; 4500 / 900 / 90 / 10 | 102, 112 |
| <e2,e6> | no | yes, yes | 4500 / 899 (+1 IS) / 90 / 10; 4500 / 900 / 90 / 10 | 534, 581 |
| <e1+e2+e6> | no | yes, yes | 4500 / 900 / 90 / 10 | 21, 25 |
| gamma_4 = <e5,e6> | yes | not run: \|exp(h~)\| = 7^9 = 4.0e7 rows (budget 2e6). The skip record was missing from the JSON (the file was written only after a run, finding 9); it was added afterwards with a note, and `seeded_report` now writes the file after a skip and at the end | | |

14 of 14 seeded runs recover log H (5 non-normal subgroups). Whole run 1701 s wall.
**Resource breach, disclosed:** the peak RSS of this run was 6.0 GiB (`seeded_n6_f7.out`, `/usr/bin/time`),
above the 5 GB cap I was given. It came from the two <e2,e6> runs; I was not sampling RSS
during them. The machine stayed up; at most two of my processes ran at any time. A rerun
should cap <e2,e6> (e.g. `max_support` 3e5) or run it alone.

## 5. Not done

- **Item 5** (gamma_2 and <e1+e2,e3> of n4(F_5) in the monolithic mode). Not attempted. A 4.9e7-row factor with
  int64 Z[zeta_5] amplitudes needs about 2.5 GB plus a transient of the same size. On this loaded machine that
  would break the 5 GB cap. A memory-reduced format (int16 amplitudes, or a hub split over Q at the top merge,
  which alone does not shrink the row count) was not implemented.
- **The exact output law at c = 3** (n4(F_5)). The Q register of grade 2 is a QFT target of its own instrument,
  so a fixed hub does not apply. That needs re-merging hub branches, which was not implemented. The c = 3 runs
  remain sampled trajectories, now with KS.
- **The explicit QFT of lem:qft-mod** inside the monolithic simulation; gate-list sources on all addresses and any
  gate-level simulation at p = 7 or class five; gamma_2 of n5(F_7) and gamma_4 of n6(F_7) (7^9-row coset
  densities); coherent-label (kappa >= 3) circuits at class five; a coherent receiver for general (G, H).

## 6. Tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_mono.py tests/test_rees_circuit_exhaustive.py tests/test_rees_circuit_round2.py --durations=8
```
Output (`pytest_round2.out`, rerun after the review fixes): `46 passed, 1 skipped in 84.16s` (the 26 round-1 tests still pass). The skipped
test is the class-five seeded run, behind REES_SLOW; with `REES_SLOW=1 ... -k class_five`: `1 passed in 54.66s`
(`pytest_round2_slow.out`).

The new tests (`tests/test_rees_circuit_round2.py`, 21):
- HubState against a dense state vector (8 random circuits);
- Gram matrices against dense inner products;
- the exact law against the plain level-0 law, on H = Z and on three mutants (two with a non-uniform law);
- the exact law at a small-S non-normal subgroup (729 hubs, 27 label tuples);
- one oracle entry at H = Z caught by K1;
- `g_sign` caught by K4 with a uniform law;
- checkpoint KS: no false alarm, the oracle mutant caught in every terminal sample;
- the power-class solver against `all_witnesses`;
- a seeded n5(F_5) run with the new solver;
- the Lean source has the theorems and no `sorry` or `axiom`;
- (after the review) K3 covers all three children and the K4 witness check holds; KS catches a dropped CX in a
  source evaluation (dirty workspace) in every terminal sample;
- STATUS gates false.

The other `tests/test_rees_circuit*.py` files were not rerun. They do not import the edited functions, except
`run_terminal_sample`, whose default path is unchanged.

## 7. Claim gates (must stay false)

None was touched. They stay false:
- `coherent_receiver_implemented`: these are finite instances with exact QFT_p, and no generator of the receiver of
  prop:coherent-receiver exists;
- `general_sde_implemented`, `formal_compiler_checked`, `independent_review`, `novelty_established`,
  `speedup_claim_allowed`.

The Lean module proves one algebraic lemma. It does not check the compiler or the circuits.

## 8. Proposed text for the "Gate-level control" section of main.tex

**Status: AI-checked, pending human review.** The text below is exact. Old sentences are quoted from the current
main.tex. The text avoids \mathsf, \mathrel, \begingroup and \aa.

All five edits are in the "Gate-level control" section (paragraphs "Coherent-label backends", "Instances",
"Scope"). Each old sentence occurs exactly once in main.tex (checked).

**(i) Coherent-label backends paragraph.** Replace

> ; for the six normal subgroups containing the centre nothing is measured before the readout, so there it is the exact output law of the whole circuit.

by

> . The exact output law of the whole circuit, with nothing measured before the readout, is computed for all $19$ subgroups (report \file{research/audits/reviews/2026-11-05-rees-receiver-round2.md}; finite computation, AI-checked, pending human review). After the preparation of $Q$ the labels and $Q$ are used only as controls, so the joint state is written exactly as an orthogonal sum over their at most $729$ basis values, in which the three children stay separate tensor factors instead of one factor of $3.9\cdot10^8$ basis states, and the readout law follows exactly from the Gram matrices of the factors; it is exactly uniform on $\hh^\perp$ for all $19$ subgroups, and for the six normal subgroups containing the centre it agrees with the computation from one product of factors.

**(ii) Coherent-label backends paragraph.** Replace

> Only the readout law is tested: some corrupted circuits (one oracle entry changed, one gate dropped) pass on most trajectories, so the intermediate states rest on the module checks above.

by

> The exact computation also compares the joint state with reference states computed from $\hh$ rather than from the oracle: after each source the reduced state of its address is the coset density of $\exp(\hlift)$, and after each instrument that of address and label is the instrument applied to it; the workspace is clean after each module and unentangled between the merge components; after the merge block each child, for every value of the labels and of $q$, is its earlier state right-translated by $-\delta_s(\sigma(q))$ with the reference witness $s$; and the reduced state of $Q$ is proportional to $\rho_{H_1}$ for every label tuple. All of these hold for all $19$ subgroups. Of $92$ runs ($23$ mutations, one oracle entry changed, one gate dropped in a module, or a modified merge block, each on four subgroups), $72$ fail one of these checks, deterministically, and the other $20$ leave the final state unchanged; $24$ of the $72$, among them the merge with the opposite sign of the translation, have an exactly uniform output law, which the readout law therefore cannot detect. In the sampled-trajectory mode, a pure-state form of the source check, with a clean workspace, on every source catches one changed oracle entry in every terminal sample, $60$ each on three subgroups over $\mathbb{F}_3$ and $4$ each on two over $\mathbb{F}_5$, where the readout test caught it in at most one of $60$ trajectories at $H=Z(G)$ over $\mathbb{F}_3$; at $c=3$ the merges are still checked only through the readout law and the module checks above.

**(iii) Instances paragraph.** Replace

> The extension to all pairs is argued, not machine-checked: by the witness equation $\sum_is_i^d\lambda_i=0$ the phases of every merged product cancel, so every pair gives the zero-label output.

by

> The extension to all pairs rests on an identity: from these two checks and the witness equation $\sum_is_i^d\lambda_i=0$, every merged product equals the zero-label product pointwise, for every label tuple and every witness. This identity is proved in Lean, in the standalone module \file{formal/Formal/ReesMergeReduction.lean}, which is not among the audited modules of Table~\ref{tab:lean-modules} (Lean-checked, AI-written, pending human review). That the merge output depends only on this product is read off the code, not machine-checked.

**(iv) Instances paragraph.** Replace

> for seven of eight subgroups, five of them nonnormal, without seeded runs; there the grade-five merge gate lists are checked against the right-nested BCH form only.

by

> for seven of eight subgroups, five of them nonnormal, and two seeded runs each from the coset density of $\exp(\hlift)$ recover $\hh$ ($14$ of $14$). At grade three ($M_3=10$) the witness is found by a complete search over the cubes $\{0,\pm1\}$ of $\mathbb{F}_7$, which has $3^{10}$ points instead of $7^{10}$. There the grade-five merge gate lists are checked against the right-nested BCH form only.

**(v) Scope paragraph.** Replace

> the monolithic simulation of \file{theorems/rees_circuit_mono.py} samples the trajectories of its early measurements and covers the coherent-label circuits over $\mathbb{F}_3$ and $\mathbb{F}_5$ only, and the extension of the merge checks of \file{theorems/rees_circuit_exhaustive.py} to all pairs is argued, not machine-checked (finite computation, AI-checked, pending human review);

by

> the monolithic simulation of \file{theorems/rees_circuit_mono.py} gives the exact output law over $\mathbb{F}_3$ and samples the trajectories of its early measurements over $\mathbb{F}_5$, and it covers the coherent-label circuits over $\mathbb{F}_3$ and $\mathbb{F}_5$ only. For the extension of the merge checks of \file{theorems/rees_circuit_exhaustive.py} to all pairs, the product identity is Lean-checked and its link to the merge code is read off the code (finite computation, AI-checked, pending human review);

Notes for the integrator:
- `\hh`, `\hlift` and `\file` are existing macros of the paper.
- No `\mathsf`, `\mathrel`, `\begingroup` or `\aa`.
- Edit (i) quotes the old text from the semicolon on ("... recover $\hh$; for the six ..."), so after the edit
  the sentence ends "recover $\hh$." and the new text starts a new sentence. The old string with its leading
  "; " occurs exactly once (checked).
- Edit (iii): the Lean module is standalone. `formal/Formal.lean` does not import it, `Audit.lean` has no guards for
  it, and it is not in Table `tab:lean-modules`, so the paper's guard counts do not cover it. To make it an audited
  module, add the import, five `#print axioms` guards, a table row, and update the counts (not done here: both root
  files carry uncommitted edits from other work).
- REES_FULL_CONTINUATION.md item 7, "Still lacking", needs updating (not done here):
  - the trajectory-averaged law is done at c = 2;
  - checkpoints are done at c = 2, and KS (the per-source checkpoint) at c = 3;
  - (R) is Lean-checked, with its link to the code argued;
  - seeded runs at class five are done;
  - level-0 runs are done for all 13 small-S Heis subgroups.

## 9. Next hard question

The exact output law at c = 3 (n4(F_5)), which needs a hub split that can be undone. The grade-2 Q registers are
used only as controls inside the top merge, but they are QFT targets of their own instrument. The method would
split over a register while it is control-only, and re-merge the branches (a coherent sum over the hub index)
before it is next a target.

Next command (after implementing that): `nice -n 10 /opt/anaconda3/bin/python -c "import theorems.rees_circuit_mono as M; M.exact_report_c3(...)"`.
Expected artifact: `exact_n4_f5_level0.json`.
Acceptance test: the exact law is uniform on h^perp, with K1-K5 for the seven subgroups that fit, and the law is
cross-checked against the round-1 trajectory average on one subgroup.

## 10. Independent adversarial check (fresh general-purpose subagent, AI-only)

The reviewer was briefed with the code, the outputs and this report, but not with the author's conclusions. It
was read-only, and its scratch files are outside the repository.

**Verdict: "sound with fixes". No blocking finding.** It confirmed the following:
- the hub decomposition and the Gram-matrix law: `hub_condition` and `hub_joins = 0`, and the sign convention
  against the three final QFTs;
- the code really tests "uniform on h^perp" (support equal to h^perp, rational, equal masses; all 19 in the
  JSON);
- the K1 reference comes from `graded_hidden(log_h)`, independent of the oracle table (`law.closure(generators)`);
- the K4 witness comes from a separate Gauss-Jordan, and `_witness_bound_g` does not follow the `g_sign` mutant;
- the mutation accounting matches the JSON: 0 undecided, 0 exceptions, and the 8 no-op flags really are no-ops;
- KS: delaying a measurement past its last touch is valid (0 schedule violations), and there is no false alarm on
  a valid relabelled oracle;
- the power-class solver is complete and uniform: 200 fresh cases agree with `all_witnesses`, chi2/dof = 1.11;
  3^10 is right;
- the Lean module elaborates with no warning and standard axioms, and its hypotheses match `branch_structure` and
  `subset_checks`. They are consistent (phi = 0 satisfies them), so the theorem is not vacuous;
- the five old sentences each occur once in main.tex, and the new text has none of the forbidden macros.

**Its own negative controls** (none of them in the author's set), through `exact_level0_law`:

| control | result |
|---|---|
| swap of two oracle entries across cosets | caught (K1, K2, K5) |
| fresh value at one entry | caught |
| valid relabellings (one entry, a whole coset) | no false alarm |
| dropped middle CX or CCX in the third child's BCH | caught (K3, K4, K5, workspace), or state-identical |
| extra X on a Q wire mid-merge | caught; law uniform |
| extra label-controlled CX onto a child at the start of U_SDE^-1 | caught by K4 only; law uniform |
| sign flip of one row of a child, mid-merge or at the first merge step | caught (K4, K5) |
| the same flip injected at the split itself | K4 passes, K5 and the law catch it (finding 7) |
| one reported equivalent mutant | independently confirmed to have its control 0 on all rows |
| KS: dropped first CX of the second child's source evaluation | **passed KS** in 5/5 trajectories, caught only by the end-of-run workspace flag (finding 4) |

No mutant changed the final state without being caught.

**Findings and what was done**:

| # | severity | finding | fix |
|---|---|---|---|
| 1 | should-fix | `wc_ends = [...][1::2]` skipped the third child in K3 (ctrl_i^-1 and ctrl_(i+1) share a component name) | `[1:]`, with an assert that there are as many boundaries as children; K3 now has 3 entries (test). Rerun: all 19 pass; the negative-control failed-check lists are unchanged |
| 2 | should-fix | false-alarm count 128 | corrected to 188 |
| 3 | should-fix | edit (iii) cites a Lean module that is outside the audited set (`Formal.lean`, `Audit.lean`, `tab:lean-modules`) | edit (iii) now calls it a standalone module, not among the audited ones; the integration steps are listed in the notes. Not integrated: both root files carry others' uncommitted edits |
| 4 | minor | KS had no workspace condition | `source_coset_check` now requires every workspace wire to be constant 0; new test (the dropped CX is caught in every terminal sample); trajectory runs redone, same counts, no false alarm |
| 5, 6 | minor | wording of edits (i) and (ii) | (i): quotes from the semicolon on, "at most 729"; (ii): "92 runs (23 mutations ... each on four subgroups)", "deterministically", sample counts and "a pure-state form of the source check, with a clean workspace" |
| 7 | minor | K4 is relative to the split | stated in the K4 row; K4 now also checks that the reference witness is nonzero and solves sum s_i^2 lam_i = 0 (holds for all 19) |
| 8 | minor | timing/RSS numbers and the "200 cases / 60 000 draws" claims | numbers from the rerun JSON; the solver checks now cite the 60-case test, mark the 60 000-draw check as artifact-free, and cite the reviewer's 200-case reproduction |
| 9 | minor | the gamma_4 skip was missing from the seeded JSON | `seeded_report` writes after a skip and at the end; the record is added to `seeded_n6_f7.json` with a note (no rerun of the 1700 s batch) |
| 10 | minor | overflow checked after the int64 multiply | bounded before multiplying |
| 11 | minor | dead variable `nz` | removed |

After the fixes:
- tests: `46 passed, 1 skipped in 84.16s` (`pytest_round2.out`);
- exact report: 19/19 uniform, all checkpoints pass, 6/6 plain agreement, 38/38 recoveries, 172 s, 0.51 GB;
- negative controls: 72 caught, 20 equivalent, 0 missed (577 s, 1.6 GB);
- trajectory controls: unchanged.
