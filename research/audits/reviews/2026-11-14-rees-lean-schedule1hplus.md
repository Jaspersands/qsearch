# Lean check of Schedule 1H⁺ (Section `sec:plus`): 2026-11-14

AI-checked (Claude), pending human review. Scope: the algebraic and combinatorial content of
`docs/papers/rees-hsp/core/main-core.tex`, Section `sec:plus` ("Schedule 1H⁺: Refinement
Chains and Multi-Level Contractions", from l. 785). The paper file was read only. Lean 4
v4.35.0 with Mathlib, project `formal/`. The work builds on `formal/Formal/Schedule1H/`
(report `2026-11-13-rees-lean-schedule1h.md` and its review).

## Verdict

**PROVED (Lean; no `sorry`; no new axioms; `decide` only, no `native_decide`).** Correctness
only. Time, Las Vegas behaviour and determinism are not modelled.

These are machine-checked:

- The class map `cl_D` and its properties (paragraph "Classes"), including a concrete
  instance for a primitive root.
- Definitions `def:plus-node` and `def:plus-rc`, and the remarks after `def:plus-node`.
- **Lemma `lem:plus-refine`**.
- **Corollary `cor:plus-chain`**: correctness, the exact arity, and the degree/constant bound.
- **Lemma `lem:plus-stage`** (the two-class stage) and **Lemma `lem:plus-finish`** (the
  finish `F_𝒦`).
- The plans `(𝒩, s, F0)` and `(𝒩, s, F_𝒦)` with a two-class node, run by the Schedule 1H
  level recursion.
- **Lemma `lem:plus-tensor`**, **Definition `def:plus-ell`** and **Lemma `lem:plus-ell-node`**,
  including the constant `(κ-1)^{ℓ(ℓ-1)/2}`.
- **Lemma `lem:plus-sm`(i)**, in counting form. It is CONDITIONAL on an explicit pair-count
  hypothesis, which is where the paper uses Weil's bound.
- Decidable guards: the paper's `TL_6` certificate at `p = 229` and its `TL_3` certificate at
  `p = 7` are checked by `decide`, and a perturbed `TL_6` table is rejected. The `TL_6` guard
  feeds a fully instantiated chain `(Gaussian elimination; TL_6)` over `F_229`, which is a
  6-solver of degree 2. This shows that the chain hypotheses can be satisfied.

**No paper statement was found false.** The findings below are minor underspecifications.

Not formalized:

- `lem:plus-sm`(ii);
- the sizes of the coset unions `A_{ij}` (that is, `E[n_j] = μ_0, μ_1`);
- the step from Weil's bound to the pair count;
- the monotonicity of `Φ`;
- Table `tab:plus-thresholds`;
- Proposition `prop:plus-tables` (the five ℓ-level tables);
- Definition `def:plus-schedule` as one recursive solver `𝓗⁺_κ`, and the minimum over its
  candidates;
- Theorem `thm:plus`(i), (iii), (iv) and the time and Las Vegas part of (ii);
- Lemma `lem:plus-exponent` and the headline exponent 20.

## Files (all new, except one import edit)

`formal/Formal/Schedule1HPlus/` contains 2092 lines in seven files:

- `Classes.lean`: `ClassMap` (the structure for `cl_D`), `xiPow` (`z_m = ξ^m`), `mem_coset`,
  `cl_unique`, `lift`, `mem_lift_iff`, `restrict`, `cl_eq_zero_iff_pow`, and the concrete
  instance `ofGen` (`cl_D = log_g mod D` for a generator `g` of `Kˣ`), `gen_of_orderOf`.
- `Refine.lean`: `IsRel`, `IsNode`, `IsRC`, `depOf`, `normalize`, `gauss`/`gauss_spec`,
  `Uvec`, `sum_Uvec`, `refine`/`refine_spec`, `Step`, `chainIdx`, `chainRun`, `ChainOK`,
  `chain_spec`, `card_chainIdx`, `card_chainIdx_le`, `rootsOf`, `rootSol_of_rel`,
  `rel_of_rootSol`, `rel_of_rootSol'`, `mem_lift_zero_iff`.
- `Stage.lean`: `plusStageRun`, `plusStage_stepSpec`, `plusStage_spec`, `plusFinish`,
  `plusFinish_spec`, `plusPlanF0(_spec)`, `plusPlanFK(_spec)`.
- `Tensor.lean`: `AxisRel`, `axisRel_sum`, `axisRel_map`, `axis_zero_of_nz`, `famT`,
  `TensorOK`, `tIdx`, `card_tIdx`, `card_tIdx_le`, `tensorStep(_spec)`, `tensor(_spec)`,
  `IsEllContraction`, `ellNode(_spec)`, `ellSolver_spec`.
- `SecondMoment.lean`: `cnt`, `sum_cnt`, `sum_cnt_sq`, `sum_cnt_sq_le`, `card_ne_zero_ge`,
  `real_step`, `good_one`, `good_count`, `A0set`, `Aset`, `betaFull`, `rc_of_good`,
  `plus_sm_i`.
- `Guards.lean`: `isRC_zero_iff_check`, `orderOf_g229`, `C229`, `tl6_229`,
  `tl6_229_perturbed`, `chainOK_229`, `tl6_chain_229`, `tl6_arity_229`, `tl6_solver_229`,
  `orderOf_g7`, `C7`, `tl3_7`, `ell1_contraction`.
- `Audit.lean`: `#guard_msgs` + `#print axioms` for 52 declarations.
- `formal/Formal.lean`: seven import lines added after `Formal.Schedule1H.Audit`. This is
  the only edit to an existing file. `formal/README.md` is not edited.

Outputs are in `research/audits/reviews/2026-11-14-rees-lean-schedule1hplus/`:

- `print_axioms.txt`;
- `full_build.log` and `full_build_tail.log`;
- `least_primitive_root_check.py` and its `.out`.

## Modelling choices (read before the table)

1. **Columns** are in an arbitrary finite-dimensional `K`-space `V`, with
   `a = finrank K V`. The paper uses `F_p^a`. The field `K` is arbitrary for the abstract
   lemmas and finite for the class instance, the guards and `lem:plus-sm`.
2. **Classes.** `ClassMap K N` holds `ξ` and a function `cl : (D : ℕ) → K → ZMod D` with
   exactly the four properties the paper uses, for every `D ∣ N` (the paper's `N = N_p`):
   - `cl_D(xy) = cl_D(x) + cl_D(y)`;
   - `cl_D(x) = 0 ⇔ x ∈ P_D`;
   - `cl_{D'}(x) = cl_D(x) mod D'`;
   - `cl_D(ξ) = 1`.

   `mem_coset` and `cl_unique` prove that these properties force `cl_D(x)` to be the unique
   `i` with `x ∈ ξ^i P_D`, which is the paper's definition. So nothing is gained by
   abstracting. `ofGen` builds a real instance from a primitive root, which is the paper's
   choice `ξ = g` for `p < 2·10^6`. No instance is built for a non-primitive coset generator
   (the paper's choice for `p ≥ 2·10^6`).
3. **Exponents in `ℤ_κ`.** `ξ^m` for `m ∈ ℤ_κ` is `ξ^{m.val}` (`xiPow`). This is the
   representative in `{0, …, κ-1}`, as the paper fixes for `z_m`.
4. **Relations and nodes.** `IsRel C D Ω col w` holds when:
   - `∑ w_b λ_b = 0`;
   - every nonzero `w_b` has its class in `Ω`;
   - some `w_b = 1`.

   The designated index is recorded only by its existence, since an algorithm can read it
   off `w`. A node is a function on a fixed finite column index type `ι`, so its arity is
   `|ι|`. The padding "further columns get weight 0" is not modelled (see the Schedule 1H
   `padRun` for the analogous step).
5. **Linear dependences** (the paper's Gaussian elimination) are `depOf`. It is a chosen
   nonzero dependence, which exists when there are more vectors than the dimension
   (`depOf_spec`, via Mathlib's linear independence bound). `normalize` scales by the
   inverse of a nonzero entry. These are `noncomputable`. Correctness does not depend on
   which dependence is chosen.
6. **Block layouts.** As in Schedule 1H, blocks are product index types (`β × ι`, `tIdx`,
   `chainIdx`), so disjointness of supports and of the sets `S_y` holds by construction. The
   ℓ-level tensor records membership in `S_y` as one label per column (`lab : ι → Option`).
7. **Probabilities** in `lem:plus-sm` are counts over all `|K|^{|Δ|-1}` functions
   `β : Δ\{0} → K`, with `β_0 = 0`.
8. **The ℓ-level recursion** starts at `ℓ = 0`: one column, one set `S_()`, weight 1, no
   axes. Its first step is literally the paper's case `ℓ = 1`.

## Statement map (paper ↔ Lean)

| Paper (main-core.tex) | Lean | Status | Notes |
|---|---|---|---|
| "Classes" paragraph (l. 791): `cl_D`, additivity, `P_D ⇔ cl = 0`, compatibility mod `D'`, `lift_D` | `ClassMap`, `cl_one/inv/div/pow`, `cl_xiPow`, `mem_coset`, `cl_unique`, `lift`, `mem_lift_iff`, `ofGen`, `gen_of_orderOf` | PROVED | Instance only for a primitive root. The probability `≥ 8/35` for a random coset generator, and the claim that `q = ξ^{κ/2}` has `q^h = -1`, are not formalized. |
| Def. `def:plus-node` (l. 794) | `IsRel`, `IsNode` | definition | Designated index stored by existence (modelling choice 4). Degree and constant appear in `card_chainIdx_le` and `card_tIdx_le`. |
| Remarks after `def:plus-node` (l. 798): Gaussian elimination is a `ℤ_D`-node; a `D`-solver, scaled, is a `{0}`-node at modulus `D` and a `Dℤ_κ`-node at modulus `κ`; a `{0}`-node with roots is a `κ`-solver | `gauss_spec`, `rel_of_rootSol`, `rel_of_rootSol'` + `mem_lift_zero_iff` (`lift_κ{0} = Dℤ_κ`), `rootSol_of_rel` | PROVED | Roots come from any function `rt` with `rt(x)^κ = x` on `P`. |
| Def. `def:plus-rc` (l. 801) | `IsRC` | definition | `β` is given on all of `ℤ_D`; only its values on `Δ` enter. The conditions `0 ∈ Δ`, `0 ∈ Ω`, `D ≥ 2` are not part of `IsRC`. |
| Translation invariance and exhaustive decision after `def:plus-rc` (l. 805) | none | NOT formalized | `isRC_zero_iff_check` gives a decision procedure for `Ω = {0}` over a finite field. |
| **Lemma `lem:plus-refine`** (l. 808) | `refine`, `refine_spec` | PROVED | Hypotheses: `D' ∣ D ∣ N`; `Δ ⊇ lift_D(Ω')`; a contraction; an `Ω'`-node at modulus `D'`; more than `(|Δ|-1)a` blocks (the paper uses exactly `(r-1)a+1`). The hypothesis `0 ∈ Ω'` is not needed: it follows from the inner designated coefficient. `D ≥ 2` is not needed. The output formula, including the normalization `η_{ν*} = 1` and the final scaling by `(α_0+β_0)^{-1}`, is the paper's. Operation counts are not formalized. |
| **Corollary `cor:plus-chain`** (l. 825): correctness | `chain_spec` (with `ChainOK`) | PROVED | `Δ_t ⊇ lift_{D_t}(Ω_{t-1})` is enough; the paper has equality. The list of steps is stored last-first. |
| `cor:plus-chain`: arity `N_0 ∏((|Δ_t|-1)a+1)` | `card_chainIdx` | PROVED | Exact equality. |
| `cor:plus-chain`: degree `e_0+L`, constant `K_0 ∏(|Δ_t|-1)` | `card_chainIdx_le` | PROVED | Uses `|Δ_t| ≥ 2` and `(r-1)a+1 ≤ (r-1)(a+1)`. |
| `cor:plus-chain`, last sentence (roots give a `κ`-solver) | `rootSol_of_rel` | PROVED | none |
| Example `(GE; (κ, ℤ_κ, {0}))` (after `cor:plus-chain`) | `tl6_chain_229`, `tl6_arity_229`, `tl6_solver_229` | PROVED at `κ = 6`, `p = 229` | Arity `(a+1)(5a+1)`, degree 2. |
| **Lemma `lem:plus-sm`(i)** (l. 836) | `rc_of_good` (the deterministic step), `sum_cnt` (first moment), `sum_cnt_sq` + `sum_cnt_sq_le` (second moment), `card_ne_zero_ge` (Cauchy–Schwarz), `good_one`, `good_count` (union bound), `plus_sm_i` | CONDITIONAL on the pair-count hypothesis `hN`; the algebra is PROVED | `plus_sm_i` gives at least `T(1-Φ)` good `β`, where `Φ = ∑_j(1-1/ρ_j)` and `ρ_j = T/S_j + T∏_iγ_{ij}/(∏_i|A_{ij}|)²`. With the paper's `γ_{ij} = γ|A_{ij}|²/p` and `T = p^{r-1}`, this `ρ_j` is `1/E[n_j] + γ^{r-1}`, exactly as in the paper (checked by hand, not in Lean). Not formalized: (1) `|A_{00}| = h_D`, `|A_{ij}| = ωh_D`, hence `E[n_j] = μ_0, μ_1` and the paper's two-term `Φ`; (2) the derivation of `hN` from Weil's bound through the `D²` pairs `(s, z)` (I checked the arithmetic by hand: `(|A|/h_D)²(p+(D-1)²√p)/D² = γ|A|²/p`); (3) the monotonicity of `Φ`. |
| `lem:plus-sm`(ii) | none | NOT formalized | none |
| Table `tab:plus-thresholds` | none | NOT formalized | none |
| Axis relations, `M_ℓ(a)`, "Multi-level contractions" (l. 876) | `AxisRel`, `tIdx`, `card_tIdx` | definition plus PROVED | `card_tIdx`: `|tIdx κ a ℓ| = ∏_{t<ℓ}((κ-1)^t a + 1)`. |
| **Lemma `lem:plus-tensor`** (l. 879) | `tensorStep_spec`, `tensor_spec`, `axis_zero_of_nz` | PROVED | Disjoint `S_y` by construction; weights in `P`; `b* ∈ S_0` of weight 1; axis relations. `axis_zero_of_nz` is the paper's "induction on the number of zero coordinates". "Deterministically" and the operation counts are not formalized. |
| Def. `def:plus-ell` (l. 890) | `IsEllContraction` | definition | Condition (iii) is quantified over all scalar families with the axis relations, as in the paper. |
| Remark after `def:plus-ell` ((iii) is equivalent to vanishing on the basis `e_m - z_m e_0` of `W^{⊗ℓ}`) | none | NOT formalized | So the five tables cannot be checked by `decide` here. |
| **Lemma `lem:plus-ell-node`** (l. 897) | `ellNode`, `ellNode_spec`, `ellSolver_spec`, `card_tIdx_le` | PROVED | (iii) is applied coordinate-free, through every linear functional on `V` (`Module.forall_dual_apply_eq_zero_iff`). The constant `(κ-1)^{ℓ(ℓ-1)/2}` needs `κ ≥ 2`. Non-vacuity of the definition only at `ℓ = 1`, `Ω = ℤ_κ` (`ell1_contraction`); see the self-check. |
| Prop. `prop:plus-tables` | none | NOT formalized | none |
| **Lemma `lem:plus-stage`** (l. 917) | `plusStageRun`, `plusStage_stepSpec`, `plusStage_spec` | PROVED | `q = ξ^{m.val}`, `ε = -q^{-1}`. The case `I = ∅` cannot occur (the designated index is in `I`), which matches the paper's proof. Block layout, as in `lem:stage`. |
| Paragraph after `lem:plus-stage` (`m = κ/2` gives `lem:stage`; `T_j` recursion; `lem:two-term` holds for every `ε`) | Schedule 1H `two_term_mem_T1` (any `ε ≠ 0`), `cTyp`, `mem_Tset_extType` | PROVED (already in Schedule 1H) | The "depends on the coset `ξ^mP`" claim is not formalized. |
| **Lemma `lem:plus-finish`** (l. 928) | `plusFinish`, `plusFinish_spec` | PROVED | The hypothesis `ξ^{u+k}P ⊆ T(c)` is taken literally (`xiPow (u+k) * y ∈ T(c)` for `y ∈ P`). `fin` must write every nonzero element of `T(c)`. |
| Def. `def:plus-schedule`(f), a plan with `F0` or `F_𝒦` | `plusPlanF0_spec`, `plusPlanFK_spec` | PROVED (correctness of one plan) | Any two-class node and any `Ω`-node finish. The recursive solver `𝓗⁺_κ`, admissibility, the tie rule and `A⁺_κ` are not formalized. |
| `def:plus-schedule`(b)–(d) (chains) | `chain_spec` + `rootSol_of_rel` | PROVED (correctness of each chain, given its contractions) | none |
| `def:plus-schedule`(e) | `ellSolver_spec` | PROVED (given a table) | none |
| Thm. `thm:plus`(ii), correctness of each candidate type | the rows above | PROVED, per candidate | Induction over `κ` and the minimum over candidates are not assembled. |
| Thm. `thm:plus`(i), (iii), (iv); `lem:plus-exponent`; `rem:plus-profile`, `rem:plus-is` | none | NOT formalized | none |

## Guards (Guards.lean; `decide` only)

- `orderOf_g229`, `orderOf_g7`: 6 and 3 are primitive roots of 229 and 7. A Python check
  (`least_primitive_root_check.py`) confirms that they are the *least* primitive roots, as
  the paper prescribes. It also confirms that every entry of `certs_stage1.json` (all 5
  steps) and of `v2/certs_tl6_all.json` (33258 primes) uses the least primitive root.
- `tl6_229`: the entry `"229"` of
  `research/audits/reviews/2026-11-13-rees-headline-below-38/v2/certs_tl6_all.json` is an
  `RC(6; ℤ_6 → {0})` contraction for `ξ = 6`:
  - `α = (1,198,100,141,0,223)`;
  - `β = (0,6,228,31,129,88)`.
- `tl6_229_perturbed`: changing `α_1` by 1 makes it fail (negative control).
- `tl3_7`: entry `"7"` of `certs_stage1.json` (`TL_3`, `ξ = 3`) is a contraction.
- `isRC_zero_iff_check` proves the decidable criterion equivalent to `IsRC`. So the guards
  are statements about `IsRC` itself, and not only about a Boolean mirror of it.

## Axioms and build

All 52 audited declarations depend on `[propext, Classical.choice, Quot.sound]`, except
`ClassMap.mem_lift_iff`, which depends on `[propext, Quot.sound]`. The full output is in
`print_axioms.txt`. `Audit.lean` checks it with `#guard_msgs`, so any `sorry`
(`sorryAx`) or `native_decide` (`Lean.ofReduceBool`) would fail the build. `grep` finds no
`sorry`, `admit`, `axiom` or `native_decide` in `formal/Formal/Schedule1HPlus/`.

The main theorems with this output are:

- `refine_spec`, `chain_spec`, `card_chainIdx`, `card_chainIdx_le`;
- `plusStage_spec`, `plusFinish_spec`, `plusPlanF0_spec`, `plusPlanFK_spec`;
- `tensor_spec`, `ellNode_spec`, `ellSolver_spec`;
- `plus_sm_i`;
- `tl6_229`, `tl6_solver_229`.

Commands, run from `formal/`, one at a time:

- `nice -n 19 ~/.elan/bin/lake build Formal.Schedule1HPlus.<File>` for each file. Each
  ended with `Build completed successfully`.
- `nice -n 19 ~/.elan/bin/lake build Formal`. Tail of the output:

```
✔ [9137/9138] Built Formal (68s)
Build completed successfully (9138 jobs).
```

Peak resident memory (`/usr/bin/time -l`) was about 2.2–2.3 GB per module. The final
`lake build Formal` peaked at **3.60 GB**: under the 4 GB cap, but close to it. Most of that
is loading the whole library into the root module.

The build prints only linter warnings in the new files (31): deprecated `if_pos`/`if_neg`
names, unused section variables, `haveI` style, and one unused variable.

## Findings

None of these is a counterexample.

1. **Representatives of exponents in `ℤ_κ`.**
   - Where: `lem:plus-stage` (`q = ξ^m`), `lem:plus-finish` (`η' = ξ^uη`, `ξ^{u+k}P`), and
     the plan clause `ε = -ξ^{-m}`.
   - The issue: these write `ξ^m` for `m ∈ ℤ_κ`. The paper fixes the representative
     `m ∈ {0,…,κ-1}` only later, for `z_m`, in the paragraph "Multi-level contractions"
     (l. 876).
   - Correctness does not depend on the choice: `cl(ξ^m) = m` for any representative.
   - But the objects that are built do depend on it. The entries of `c^{(j)}` and hence the
     stored `T_j` vectors change by factors in `P`, and so does `ε`. A run must therefore
     use the same representative in the preprocessing and in the run.
   - Lean uses `m.val` throughout. Suggest one sentence in "Classes".
2. **`lem:plus-refine`: `0 ∈ Ω'` and `D ≥ 2` are not needed.** `0 ∈ Ω'` follows from the
   inner node's designated coefficient (`cl(1) = 0`). `Δ ⊇ lift_D(Ω')` already appears in
   the lemma as `⊇`. Corollary `cor:plus-chain` demands `=`, but `⊇` is enough. This is
   harmless.
3. **Paths of the certificate files.** Appendix `app:artifacts` says the certificate tables
   (`certs_stage1.json`, `tierB_witnesses.json`, `v2/certs_tl6_all.json`, `v2/verify_*.py`)
   are "in the draft folder", in the sentence right after naming
   `research/audits/reviews/2026-11-14-rees-schedule1hplus-draft/`.
   - They are not there. They are in `research/audits/reviews/2026-11-13-rees-headline-below-38/`,
     which is the folder of the two drafts `fragment.tex`/`fragment-v2.tex`.
   - The sentence is ambiguous, and a reader will probably look in the wrong folder.
   - Suggest naming the folder explicitly.
4. **`lem:plus-sm`(i): only part of the argument is in Lean.** The second-moment skeleton
   (first moment, pair expansion, Cauchy–Schwarz, union bound) is checked. The coset-size
   facts and the Weil-to-pair-count step are not. By hand I confirmed:
   - `ρ_j = 1/E[n_j] + γ^{r-1}` from the Lean `ρ_j` with `γ_{ij} = γ|A_{ij}|²/p`;
   - `N_{ij}(u) ≤ γ|A_{ij}|²/p` from the stated Weil count;
   - the monotonicity argument.

   I found no error there.
5. **The ℓ-level definition is checked only trivially for non-vacuity.** The remark after
   `def:plus-ell` (basis tensors) is not formalized, so `prop:plus-tables` was not checked in
   Lean. The paper relies on four Python programs there.

## Adversarial self-check

- **Vacuity of the class structure.** `ClassMap` could in principle be unsatisfiable or
  degenerate. It is not:
  - `ofGen` constructs it from any generator of `Kˣ`;
  - `C229` and `C7` are concrete;
  - `cl_unique` and `mem_coset` show that it is the paper's `cl` and nothing weaker.
- **Vacuity of `refine_spec`/`chain_spec`.** Its hypotheses are an `IsRC` contraction and
  an inner node. `tl6_chain_229` discharges every hypothesis of `chain_spec` at a real step,
  using the paper's own certificate and `gauss_spec`. So the chain theorem is not vacuous.
  The negative control shows that the `decide` check can fail.
- **Vacuity of the stage and plan theorems.** `plusPlanFK_spec` assumes a `{0,m}`-node, a
  finisher `fin` and the covering hypothesis `hT`. I built no concrete instance of a full
  `F_𝒦` plan. The `{0,m}`-node hypothesis is satisfiable in principle by the chain
  machinery (`U_m` chains), but I did not instantiate one. Treat the plan theorems as
  correctness given correct sub-objects. This is the same status as `planF1_spec` in
  Schedule 1H.
- **Vacuity of `ellNode_spec`.** The only instance of `IsEllContraction` that I checked is
  the trivial `ℓ = 1`, `Ω = ℤ_κ` (`ell1_contraction`). For `κ ≥ 2`, `ℓ = 1` admits no
  `{0}`-contraction. Whether the paper's level-3/4 tables satisfy the Lean definition is
  UNKNOWN in Lean. If they did not, `ellSolver_spec` would still be true, but it would not
  apply to candidate (e). The tensor lemma itself is unconditional.
- **Statement strength.** `IsRel` requires an entry exactly `1` and classes in `Ω` for every
  nonzero entry, which is what the paper requires. The output of every theorem is a
  relation on the original columns, or a root solution (`IsRootSol`, which was shown
  equivalent to the paper's `κ`-solution in Schedule 1H). No encoding stands between the
  final statement and the paper's notion.
- **Choice hides algorithms.** `depOf`, `normalize` and root extraction use choice. The
  theorems are statements about the constructions given correct subroutines, not about how
  the subroutines are computed or how long they take.
- **`plus_sm_i` is conditional.** Its hypothesis `hN` is where Weil enters. Its constant
  `ρ_j` is written in terms of the actual set sizes, not the paper's `μ_0`/`μ_1`. Do not
  cite it as a proof of `Φ < 1` at the table's thresholds.
- **Finite checks can only falsify.** `tl6_229` and `tl3_7` are certificates, so they are
  proofs of availability at those primes only. No asymptotic claim follows from them.
- **Not checked:** every number of Table `tab:plus-thresholds`, the 53 primes without
  `TL_6`, the exponent 20, and `thm:plus`(i)–(iv) beyond per-candidate correctness.

## Addendum (integrator, 2026-11-14): after the review

The review (`2026-11-14-rees-lean-schedule1hplus-review.md`, verdict SOUND WITH FIXES) changes
three statements above:

- **Tables (Finding 5 above, and the "not covered" list).** The five level-3/4 tables of the
  paper, at (13,4), (13,6), (19,9), (37,9) and (73,9), are now checked in Lean against
  `IsEllContraction` by `decide +kernel`. The checks are in the review modules
  `formal/Formal/Schedule1HPlusReview/EllCheck*.lean`, which `Formal.lean` does not import. Lean does
  not check that each generator is the least primitive root; that rests on the Python check.
- **Plan theorems.** `plusPlanF0_spec` and `plusPlanFK_spec` take nodes on `Fin A`. Chain and
  table nodes use other index types, and the bridge (`isNode_reindex`, `isRel_mono`) is proved
  only in the review module `Probes.lean`.
- **"Any η".** `refine_spec`, `chain_spec` and `tensor_spec` prove correctness for the
  dependence chosen by `depOf`, not for every dependence η as the paper's wording allows.
  This is enough for the algorithm, which makes one choice.

The doc comments in `Schedule1HPlus/Tensor.lean` (a reference to a nonexistent `ann_iff_basis`)
and `Schedule1HPlus/Guards.lean` (which said the tables were unchecked) are corrected. Both
modules rebuild.
