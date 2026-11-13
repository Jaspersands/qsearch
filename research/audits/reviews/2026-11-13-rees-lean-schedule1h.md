# Lean check of Schedule 1H (and lem:rounds): 2026-11-13

AI-checked (Claude), pending human review. Scope: the finite and combinatorial content
of `docs/papers/rees-hsp/core/main-core.tex`, Section "Schedule~1H: Halving the Degree"
(lines 645-765) and Lemma `lem:rounds` (line 561). Lean 4 v4.35.0 + Mathlib, project
`formal/`.

## Verdict

**PROVED (Lean, no `sorry`, standard axioms only), with the stated conditions.** These
are machine-checked: the definitions of κ-solution and κ-solver; Lemma `lem:stage`;
Lemma `lem:finish` (F0, F1); Lemma `lem:rounds`; the correctness part of Theorem
`thm:halving`(ii) for the paper's arity `A_κ(a)` and tie rule; the inequality of
`thm:halving`(i); Lemma `lem:two-term` given Weil's bound as a hypothesis; the `T_j`
recursion display (line 686); Corollary `cor:hcd`(i) (correctness); and the last claim
of Remark `rem:kappa-two` (that `(1, F0)` is never admissible).

Two imported results enter only as explicit hypotheses:
- the Ivanyos–Santha collision step (Theorem `thm:is-import`), and
- the lower half of Weil's bound for `u^κ + ε v^κ = η` (needed only when `p ≥ 4κ^4`).

**No paper statement was found false.** Every hypothesis the Lean proofs needed is
present in the paper or implied by it. The underspecifications I found are minor (see
"Findings").

Not formalized: running time, Las Vegas behaviour, expected-time bounds and determinism
in (ii); computability of `A_κ(a)` in (i); and `thm:halving`(iii), `cor:hcd`(ii) and
`lem:halved-exponent`.

## Files (all new)

- `formal/Formal/Schedule1H/Objects.lean`: `Pow` (the set P), `IsKSolution`,
  `IsRootSol`, `IsKSolver`, `padRun`, objects (`Obj`, `IsObj`, `IsObj.paperRep`),
  `solOf`, `combine`, `StepSpec`, `step`, `Tset` (the set T(c)), and the finishes
  `finishGen`, `finishF0`, `finishF1`.
- `formal/Formal/Schedule1H/Levels.lean`: `Lev`, `Typ`, `cTyp` (the types c^(j)),
  `runLevel`, `planF0`, `planF1`, `Garity` (the arity G(κ,a)), `ISOut`, `roundsBlock`,
  `rounds_spec`, `calls_eq`.
- `formal/Formal/Schedule1H/Stage.lean`: `stageRun`, `StageOK`, `stage_spec`, the coset
  test over a finite field (`exists_root_of_pow_eq_one`, `pow_eq_one_of_root`,
  `pow_h_eq_one_or_neg_one`, `ff_stageOK`), and `exists_q`.
- `formal/Formal/Schedule1H/Halving.lean`: `Cand`, `Prep`, `arity`, the recursive
  solver `H`, `CandOK`, `H_spec`.
- `formal/Formal/Schedule1H/TwoTerm.lean`: `WeilLower`, `card_pow_eq_le`,
  `card_sol_le`, `two_term_count`, `two_term_mem_T1`.
- `formal/Formal/Schedule1H/Paper.lean`: `tMin` (= t_{p,κ}), `Tsets`, `Admissible`,
  `Apaper` (= A_κ(a)), `paperChoice`, `paperPrep`, `Apaper_le_rounds`,
  `paper_arity_eq`, `halving_correct`, `halving_correct_weil`.
- `formal/Formal/Schedule1H/Extras.lean`: `Tset_unit`, `mem_Tset_extType`,
  `Tset_subset_extType`, `zero_not_mem_T1`, `cor_hcd_i`.
- `formal/Formal/Schedule1H/Audit.lean`: `#guard_msgs` + `#print axioms` for 38
  theorems, and a compiled run of `H` at κ = 2 over `ZMod 7`.
- `formal/Formal.lean`: eight import lines added (the only edit to an existing file).
  `formal/README.md` was not updated, as the brief allowed no other edits; the
  integrator may add a line.

Supporting outputs are in `research/audits/reviews/2026-11-13-rees-lean-schedule1h/`:
build logs, `print_axioms.txt`, `run_outputs.txt`, and timing and memory files.

## Modelling choices (read before the table)

1. **Field.** Every result is over an arbitrary field `K`, or an arbitrary finite field
   for the coset test, `tMin`, two-term and the paper layer. This is more general than
   `𝔽_p` with `p` an odd prime: odd characteristic is assumed only where it is used
   (`exists_q`, `zero_not_mem_T1`).
2. **κ-solution as a root vector.** `isKSolution_iff` proves that the paper's pair
   `(w, r)` is the same as `r ≠ 0` with `∑ r_b^κ λ_b = 0`, where `w = r^κ` (for κ ≥ 1).
   All algorithms return `r`.
3. **κ-solver.** `IsKSolver κ N run` means that for all `a`, all `n ≥ N(a)` and all
   columns in `K^a`, `run a n col` is a root solution. This is the paper's definition
   including "further columns get weight 0"; `padRun` pads with zeros.
4. **Objects.** An object is encoded as a labelling `part : ι → Option τ` with roots,
   where representation `R_k = {i | part i = some k}`. Disjointness of the
   representations of one object is therefore built in. Objects with pairwise disjoint
   supports are placed on a product column type `β × ι`, so that disjointness is also
   built in. `IsObj.paperRep` derives the paper's form: nonempty, pairwise disjoint index
   sets, weights in `P` with roots, and value `c_k v`.
5. **Algorithms.** These are ordinary Lean `def`s. `H` runs (`Audit.lean`). Its oracles
   come from a preprocessing record `Prep`: the imported collision algorithm, the root
   function, the coset test, `q`, and the F0/F1 tables. In the paper layer
   (`paperPrep`), the roots and tables are non-computable choice functions whose
   existence follows from admissibility. The paper instead uses tables when
   `p < 4κ^4`, and Las Vegas root finding plus uniform draws of `u` when `p ≥ 4κ^4`.
   Any implementation that meets the stated specification gives the same correctness.
6. **The imported step** is `ISOut κ v`: disjoint `I ≠ ∅` and `J`, γ nonzero on
   `I ∪ J`, and `∑_I γ^κ v = ∑_J γ^κ v`. This is the paper's statement of
   `thm:is-import`. `ISOut.stepSpec` converts it into the generic step specification.

## Statement-by-statement correspondence

| Paper (main-core.tex) | Lean | Status | Difference from paper |
|---|---|---|---|
| κ-solution (l.650) | `IsKSolution`, `isKSolution_iff`, `IsRootSol.isKSolution` | PROVED | Equivalent to the root form (needs κ ≥ 1). |
| κ-solver of arity N(a), with extra columns at weight 0 (l.650) | `IsKSolver`, `padRun_spec` | definition | The arity is a function `ℕ → ℕ`; the solver must work for every `n ≥ N(a)`. |
| Gaussian elimination is a 1-solver of arity a+1 (l.650) | `H_spec`, case κ ≤ 1 (uses `ReesSdeSolver.kernelVec_spec`) | PROVED | none |
| Lemma `lem:rounds` is a κ-solver of arity G^L (l.650) | `rounds_spec` | PROVED, given the imported step | See the `lem:rounds` row. |
| Representation, object, support, a column as an object of type (1) (l.652) | `Obj`, `IsObj`, `IsObj.paperRep`, `colObj_spec` | definition plus PROVED | Encoding as in modelling choice 4. The type `c` may contain any entries; the paper requires nonzero entries, and all `cTyp` entries are nonzero. |
| `T(c)` (l.652-654) | `Tset`, `mem_Tset_iff` | definition plus PROVED | `mem_Tset_iff` gives the root form `∃ ρ ≠ 0, ∑ ρ_k^κ c_k = x`. Stability under multiplication by `P` is not formalized (not needed). |
| `P_D = P ∪ qP`; `x^h = ±1` on `P_D`; `x ∈ P ⇔ x^h = 1`; existence of `q` (l.658) | `pow_h_eq_one_or_neg_one`, `exists_root_of_pow_eq_one`, `pow_eq_one_of_root`, `exists_q`, `neg_one_pow_odd` | PROVED | Over any finite field. `exists_q` assumes `ringChar K ≠ 2`. |
| **Lemma `lem:stage`** (l.660-669) | `stageRun`, `stageRun_stepSpec`, `stage_spec`; instance `ff_stageOK` | PROVED | The `D`-solver call is any `Dsol` whose output is a D-solution on the `v_ν`. The test and roots are abstract (`StageOK`); `ff_stageOK` shows that the paper's `x^h = 1` test and any root function satisfy it. The claim "supported in the union of the supports" holds structurally (block column type), but is not stated as a separate lemma for `solOf` and `combine`. Operation counts are not formalized. |
| **Lemma `lem:finish`(i) F0** (l.671-683) | `finishF0`, `finishF0_spec`, `finishF0_support` | PROVED | Stated for a single object (the paper uses `o_1` of N ≥ 1 objects). |
| **Lemma `lem:finish`(ii) F1** | `finishF1`, `finishF1_spec`, `finishF1_support`, `finishGen_spec` | PROVED | Holds for any nonzero `η` with `∑ η_ν v_ν = 0`. The plan uses `kernelVec` with `N = a + 1` (`planF1_spec`). |
| `c^(j)`, `T_j`, and the recursion `T_0 = P`, `T_j = T_{j-1} ∪ εT_{j-1} ∪ {α+εβ}` (l.684-687) | `cTyp`, `Tset_unit`, `mem_Tset_extType`, `Tset_subset_extType` | PROVED | The entries of `c^(j)` are indexed by `Typ j` (2^j elements), not listed in order; `T(c)` does not depend on the order. Not formalized: "T_j depends only on (p, κ)", stabilization by j ≤ κ+1, and the O(jκp) table cost. |
| **Lemma `lem:two-term`** (l.690-697) | `two_term_count`, `two_term_mem_T1`, `card_sol_le`, `card_pow_eq_le` | PROVED, given `WeilLower` | Weil is a hypothesis, and only its lower half `N ≥ p − (κ−1)²√p` is used. The conclusion is the count `|K| ≤ 2κ·#{u ≠ 0 : η − u^κ ∈ εP}`; the probability `> 1/(2κ)` is not restated. Holds for κ ≥ 1 (the paper states κ ≥ 2) and for any finite field. |
| **Definition `def:schedule1h`** (l.699-710): candidates, admissibility, `A_κ(a)`, tie rule, block and level structure, preprocessing | `Cand`, `nF`, `Prep`, `arity`, `H`; `Admissible`, `Apaper`, `paperChoice`, `paperPrep`, `tMin`, `zeroSums_nonempty` | definitions | `A_κ(a)` is `sInf` over a nonempty set (so a minimum is attained). Tie rule: (a) first, then least `s`, then F0, as in the paper. The Las Vegas draws of `u` for `p ≥ 4κ^4` are replaced by a choice-function table (existence from `two_term_mem_T1`). The degree `e^H_κ` is not defined. |
| **Theorem `thm:halving`(ii), correctness** (l.716, proof l.722) | `H_spec` (any choice and preprocessing); `halving_correct` (paper's arity and choice); `halving_correct_weil` | PROVED, given the imported step, `q`, and T_1 ⊇ K^× or Weil | `hIS` and `hq` are required at every `κ' ∣ κ` (respectively every even one), not only on the chain κ/2^i. This is stronger than needed, but satisfiable (`exists_q`; the paper's `thm:is-import` holds at every divisor). Not formalized: "checks before output" (the output is proved correct), Las Vegas behaviour, expected time, determinism. |
| `thm:halving`(i), inequality `A_κ(a) ≤ G(κ,a)^{⌈log₂ t⌉}` | `Apaper_le_rounds` | PROVED | Polynomial-time computability of `A_κ(a)` is not formalized. |
| `thm:halving`(iii) | none | NOT formalized | none |
| Corollary `cor:hcd`(i) (l.729-736), correctness | `cor_hcd_i` | PROVED | With `q = −1` (so ε = 1), for any D-solver of any arity N. The degree bound `e^H_κ ≤ ⌈log₂ t⌉ e^H_D` is not formalized. `cor:hcd`(ii) is not formalized. |
| Remark `rem:kappa-two`, "(1, F0) is never admissible" (l.744-745) | `zero_not_mem_T1` | PROVED | Odd characteristic, `κh = |K|−1`, `q^h = −1`. The other claims of the remark (the values of `A_2` and `T_1` at κ = 2) are not formalized. |
| **Lemma `lem:rounds`** (l.561-578) | `roundsBlock`, `rounds_spec`, `zeroSum_lift`, `runLevel_spec`, `calls`, `calls_eq` | PROVED, given the imported step | Holds for κ ≥ 1; the paper's κ ≥ 2 and κ ∣ p−1 are only needed for the imported step to exist. `L = Nat.clog 2 t`, and 2^L ≥ t is used. The call count is proved only as the recursion `calls(ℓ+1) = G·calls(ℓ)+1 = ∑_{j<ℓ} G^j`; it is not tied to an instrumented run. Time is not formalized. |

## Axioms and build

All 38 audited theorems depend only on `[propext, Classical.choice, Quot.sound]`; see
`print_axioms.txt`. These are checked by `#guard_msgs` in `Formal/Schedule1H/Audit.lean`,
so a `sorry` would fail the build. `grep` finds no `sorry`, `axiom`, `admit` or
`native_decide` in `formal/Formal/Schedule1H/`.

Main theorems: `H_spec`, `halving_correct`, `halving_correct_weil`, `stage_spec`,
`stageRun_stepSpec`, `finishF0_spec`, `finishF1_spec`, `rounds_spec`,
`two_term_count`, `two_term_mem_T1`, `paper_arity_eq`, `Apaper_le_rounds`,
`mem_Tset_extType`, `zero_not_mem_T1`, `cor_hcd_i`, `ff_stageOK`, `isKSolution_iff`.

Build commands, each run from `formal/` with `nice -n 19 ~/.elan/bin/lake build <target>`:

- `Formal.Schedule1H.<File>` for each `File` in Objects, Levels, Stage, Halving,
  TwoTerm, Paper, Extras, Audit. Each ended with `Build completed successfully`.
- The whole library, `Formal`. Output tail:

```
✔ [9130/9131] Built Formal (145s)
Build completed successfully (9131 jobs).
```

Peak resident memory (macOS `/usr/bin/time -l`): 2.45 GB for elaborating
`Paper.lean`, 2.09 GB for the full `lake build Formal`. Both are under the 4 GB cap.
Builds were run one at a time.

The build prints only linter warnings in the new files: deprecated `dif_pos`/`if_pos`
names, unused section variables, and unused binder names.

Run (`Audit.lean`, checked by `#guard_msgs`; extra outputs in `run_outputs.txt`). This
is `H` at κ = 2 over `ZMod 7`, using the plan (1, F1) over Gaussian elimination, with
q = 3 (so q³ = −1 and ε = 2):
- arity 9 at a = 2;
- on nine sample columns in `(ZMod 7)²` it returns `r = (6,6,0,0,0,0,6,0,0)` with
  `∑ r_i² λ_i = 0`.

This tests the compiled code; it is not a proof.

## Findings

None of these is a counterexample. All are minor.

1. **Lemma `lem:two-term` uses only half of Weil, and κ ≥ 1 suffices.** The proof uses
   only `N ≥ p − (κ−1)²√p` and works for any finite field and any κ ≥ 1. The arithmetic
   chain is confirmed exactly (`two_term_count`): `(κ−1)²√p ≤ p/2 − (2κ−1)√p`,
   `(2κ−1)√p ≥ 2κ`, at most 2κ pairs with `uv = 0`, and at most κ values of `v` per `u`.
   The Weil locator itself is still unchecked (the paper's `% NEEDS HUMAN VERIFICATION`
   at l.597).
2. **The candidate (a) zero sum is formalized at any length.** Lemma `lem:rounds` does
   not need t ≥ 2: any nonzero zero sum of length t with `2^L ≥ t` works. The paper's
   remark "t ≥ 2 and L ≥ 1" is true but not needed.
3. **Underspecified: the order of the entries of `c^(j)`.** The paper writes
   `c^(j) = (c^(j−1), εc^(j−1))` as an ordered tuple, and "the first representation
   R_1" in `lem:stage` depends on that order. Correctness needs only some fixed
   representation index. The Lean code uses `k0 j = inl^j ()`, which is the paper's
   first entry. Nothing breaks.
4. **Underspecified: the choice of q in `T_j`.** Admissibility and `A_κ(a)` are defined
   through `T_s`, which in Lean depends on the chosen `q` (`qf κ`). The paper asserts
   that `T_j` depends only on `(p, κ)` (l.688); this was not formalized. So `Apaper qf`
   is proved correct for every admissible `qf`, but its independence of `qf` is
   UNKNOWN in Lean (asserted with a one-line argument in the paper).
5. **Remark `rem:kappa-two`'s inadmissibility claim** (used in `lem:halved-exponent`(i)
   for "every candidate at κ ≥ 2 has degree at least 2") is confirmed in Lean for any
   odd-characteristic finite field (`zero_not_mem_T1`).

## Adversarial self-check

- **Vacuity.** `halving_correct` assumes `hIS`, the imported theorem, which cannot be
  proved here. If `thm:is-import` failed for some input, the Lean theorem would hold
  only vacuously at degrees where candidate (a) is chosen. The plan path (stage, F1,
  Gaussian elimination) does not use `hIS` when the chosen candidates never include (a):
  `H_spec` only asks `CandOK` for the chosen candidates. `WeilLower` is a true theorem
  (Weil), but it is not proved here. The κ = 2 run confirms that the plan path computes
  real solutions. It does not show that `CandOK` is satisfiable in general; that follows
  from `halving_correct`'s own proof (`paperPrep` meets it under the stated hypotheses).
- **Statement strength.** `IsKSolver` demands a correct output on every input of every
  length `n ≥ N(a)`, which is at least the paper's demand. The paper's "κ-solution"
  is reached through `isKSolution_iff`, which is proved in both directions.
- **Choice functions hide algorithmic content.** `paperPrep` uses `Classical.choose`
  for the zero sum, the roots, the tables, and the imported step's output.
  `halving_correct` is therefore a correctness statement about the algorithm given
  correct subroutines, not about how they are computed. The paper's tables and Las
  Vegas procedures are not checked. This matches the brief: time and probability are
  out of scope.
- **Encoding risk.** If `IsObj` were weaker than the paper's object, the lemmas could
  still prove a weaker thing. However, `IsObj.paperRep` derives every clause of the
  paper's definition from `IsObj`. The final output is a plain root solution of the
  original columns, so no encoding sits between the theorem and the paper's κ-solution.
- **The arity identity.** `paper_arity_eq` proves that the arity of the candidate `H`
  actually runs equals `Apaper`. The arity is not just bounded by it.
- **What a finite check could not do.** No theorem here was promoted from the run.
- **Not checked:** the `lem:halved-exponent` exact computations, the numbers 38 and 53,
  and the expected-time recursion `T_κ(a)` in the proof of (ii).
