# Hostile review of the Lean check of Schedule 1H and lem:rounds (2026-11-13)

AI-checked (Claude, hostile reviewer), pending human review. I reviewed
`formal/Formal/Schedule1H/*.lean` (8 files, 2112 lines) against
`docs/papers/rees-hsp/core/main-core.tex`: `thm:is-import` (l.533), `lem:rounds`
(l.560-578), and Section "Schedule~1H: Halving the Degree" (l.645-765). I also checked the
author's report `research/audits/reviews/2026-11-13-rees-lean-schedule1h.md`.

## Verdict

**No VACUOUS and no MISMATCH verdict.** Every main theorem says what the paper says, for
correctness only. Every hypothesis can be satisfied. I built a concrete instance in Lean
in which all hypotheses of the main theorem hold (`instance13`).

The imported Ivanyos–Santha hypothesis turns out to be **provable** in Lean
(`isOut_nonempty`, by Chevalley–Warning). So the Lean result does not actually depend on
the import. It is **conditional only on Weil's bound** (`WeilLower`), which is a true
published statement.

One consequence affects how the result may be described. The Lean check gives **no
evidence about the paper's use of `thm:is-import`**. The paper's dependence on that
theorem is algorithmic (deterministic polynomial time), and the Lean files do not model
time.

The author's open Finding 4 (does `A_κ(a)` depend on the choice of `q`?) is now
**PROVED** in Lean (`Apaper_indep`).

Status of the new probes: **PROVED (Lean, no `sorry`)**. Each depends only on
`[propext, Classical.choice, Quot.sound]`, checked by `#guard_msgs` in
`formal/Formal/Schedule1HReview/Audit.lean`. `cTyp_mul` depends on fewer axioms
(`[propext, Quot.sound]`). Command and result, run from `formal/`:

```
nice -n 19 ~/.elan/bin/lake build Formal.Schedule1HReview.Audit
Build completed successfully (2453 jobs).
```

Peak resident memory was 1.84 GB, under the 4 GB cap. Before the probes I also rebuilt
`Formal.Schedule1H.Audit`, which succeeded. `grep` finds no
`sorry`/`admit`/`native_decide`/`axiom` in either folder.

The new files are only in `formal/Formal/Schedule1HReview/` and are **not** imported by
`formal/Formal.lean`:

- `Probes.lean`
- `KappaTwo7.lean`
- `QIndep.lean`
- `Audit.lean`

The supporting outputs are in `research/audits/reviews/2026-11-13-rees-lean-schedule1h-review/`.

## 1. The imported hypotheses: every hypothesis of every main theorem

| Theorem | Hypotheses | Satisfiable? |
|---|---|---|
| `rounds_spec` (Levels.lean:343) | `0<κ`; `hIS : ∀ v, ∃ o : ISOut κ v, isRun v = o.rs`; `z ≠ 0`, `∑ z^κ = 0`; `G^L ≤ M` | Yes over every finite field. `isOut_nonempty` gives an `ISOut` for every `v`, so `isRun := (choice).rs` meets `hIS`. `z` exists by `zeroSums_nonempty`. |
| `stage_spec`, `stageRun_stepSpec` (Stage.lean:53,122) | `StageOK κ D q cls rt` (`κ=2D`, `D>0`, `q≠0`, roots correct on both cosets); `hD` (the `D`-solver output is a root solution) | Yes. `ff_stageOK` together with `exists_q`. `hD` comes from any `D`-solver, for example `H_spec` or my `cwRun_solver`. |
| `finishF0_spec`, `finishF1_spec` (Objects.lean:420,443) | an object; `ρ ≠ 0` with `∑ρ^κ c = 0`, or `fin` correct on `K^×`; `η ≠ 0` in the kernel | Yes, by construction (for example the zero sum in `zeroSum_lift`, and `T1_full7`). |
| `H_spec` (Halving.lean:110) | `0<κ`; `CandOK` at every divisor `κ' ≥ 2` of `κ` and every `a` | Yes. `paperPrep`/`paperChoice` meet it (that is the proof of `halving_correct`). |
| `halving_correct` (Paper.lean:219) | `0<κ`, `κ ∣ |K|−1`; `hq` (`qf κ'^h = −1` at every even `κ' ∣ κ`); `hIS` (`Nonempty (ISOut κ' v)` at every `κ' ∣ κ`, `κ' ≥ 2`, every `a`, `v`); `hT1` (`T_1 ⊇ K^×` at every even `κ' ∣ κ` with `|K| ≥ 4κ'^4`) | Yes. `hIS` is a theorem (`isOut_nonempty`). `hq` holds by `exists_q` in odd characteristic, and is vacuous in characteristic 2. `hT1` follows from `WeilLower` (`two_term_mem_T1`), and is vacuous below `4κ'^4`. **Lean instance:** `instance13` (`K = ZMod 13`, `κ = 4`, `qf 2 = 2`, `qf 4 = −1`). |
| `halving_correct_weil` (Paper.lean:277) | `ringChar K ≠ 2`, `0<κ`, `κ ∣ |K|−1`, `hIS`, `hW` (`WeilLower K κ'` at every even `κ' ∣ κ` with `|K| ≥ 4κ'^4`) | `hIS` is discharged in `halving_correct_weil_noIS`. Only `WeilLower` remains (see below). |
| `cor_hcd_i` (Extras.lean:143) | `StageOK κ D (−1) cls rt`; any `D`-solver; a zero sum | Yes when `h` is odd, by `ff_stageOK` with `q = −1` and `neg_one_pow_odd`. This is exactly the paper's case. |
| `two_term_count`, `two_term_mem_T1` (TwoTerm.lean:119,154) | `0<κ`, `WeilLower K κ`, `ε,η ≠ 0`, `4κ^4 ≤ |K|` | Yes if Weil holds. |
| `zero_not_mem_T1` (Extras.lean:99) | `ringChar K ≠ 2`, `κh = |K|−1`, `q^h = −1` | Yes. Used in `not_adm10`. |

### `ISOut` against `thm:is-import`

`ISOut` (Levels.lean:275) is field for field the paper's output: disjoint `I ≠ ∅` and
`J`, nonzero `γ` on `I ∪ J`, and `∑_I γ^κ v = ∑_J γ^κ v`, at arity
`Garity κ a = κ^{κ(κ−1)/2}(a+1)^κ = G(κ,a)` (eq:Bd). It is **not stronger** than
`thm:is-import`.

Two things are weaker than the paper's statement:

- Lean asks only for **existence** of an output (`Nonempty`), with no determinism or time
  bound.
- Lean allows any field.

**It is required at every divisor `κ' ≥ 2` of `κ`**, and not only on the chain
`κ/2^i`; `hq` and `hT1` are likewise required at every even divisor. This is harmless:

- `thm:is-import` holds at every `d ∣ p−1`, and so at every divisor of `κ`;
- the existence form is in any case a theorem.

**`isOut_nonempty` (Probes.lean).** Over any finite field and for every `κ ≥ 1`,
`κa < G(κ,a)` (`garity_gt`). So Chevalley–Warning (`ReesSdeWitness.exists_witness`) gives
a nonzero `s` with `∑ s^κ v = 0`, and `I = supp s`, `J = ∅`, `γ = s` is an `ISOut`.
Hence:

- `halving_correct_noIS`: `halving_correct` with no `hIS`;
- `halving_correct_weil_noIS`: the Weil version with no `hIS`; only `WeilLower` remains.

The author's report says "PROVED, given the imported step" and calls `hIS` "the imported
theorem, which cannot be proved here". Both should be corrected. In its existence form,
the step **is** provable, and the dependence on Ivanyos–Santha that Lean leaves out is
entirely algorithmic.

### `WeilLower` (TwoTerm.lean:43)

`WeilLower K κ` states: for all `ε, η ≠ 0`,
`|K| − (κ−1)²√|K| ≤ #{(u,v) : u^κ + εv^κ = η}`.

This is the lower half of the bound the paper cites at l.~697, for exactly the curve the
paper uses. It is true for every finite field and every `κ ≥ 1`, by the following
argument (PROVED given cited theorems):

- Put `d = gcd(κ, |K|−1)`. The maps `x ↦ x^κ` and `x ↦ x^d` have the same fibre sizes,
  so `N` is the same at `κ` and at `d`.
- The two-variable Weil/Jacobi-sum bound `|N − q| ≤ (d−1)²√q`, which is the case `n = 2`
  of Lidl–Niederreiter Ch. 6 on diagonal equations, gives the claim, since
  `(d−1)² ≤ (κ−1)²`.

The Lidl–Niederreiter theorem number is still the paper's `% NEEDS HUMAN VERIFICATION`
item (l.597); I did not check it against the book.

Finite falsification check, `weil_lower_check.py` (output in `weil_lower_check.out`):
- Range: all primes `3 ≤ p < 30000`, every `κ ≤ 9`, and one representative per pair of
  cosets of `(ε, η)` (which suffices, since `N` depends only on these cosets).
- Result: **0 violations**.
- Smallest margin in the regime the paper uses (even `κ`, `p ≥ 4κ^4`): 7.19, at `κ=2`,
  `p=67`.

This can only falsify, and it did not.

## 2. Statement against paper, per main theorem

| Paper | Lean | Verdict | Notes |
|---|---|---|---|
| κ-solution (l.650) | `IsKSolution`, `isKSolution_iff` | **FAITHFUL** | `w ≠ 0` is required. `IsRootSol` requires `r ≠ 0` (`zero_not_rootSol`). The equivalence is proved for κ ≥ 1. |
| κ-solver of arity N(a) (l.650) | `IsKSolver` (Objects.lean:105) | **FAITHFUL WITH CAVEATS** | It is stronger than the paper: every `n ≥ N(a)`. It is not trivial: there is no solver of arity 0 or 1 (`not_solver_arity_zero`, `not_solver_arity_one`). **Caveat:** it is a pure correctness predicate. A noncomputable "solver" of arity `κa+1` exists (`cwRun_solver`), far below `A_κ(a) ≥ (a+1)^2`. So the paper's arity claims mean something only together with polynomial time, which Lean does not model. The Lean content is that the specific procedure `H` is correct, given any oracles that meet their specifications. |
| `lem:rounds` | `rounds_spec` | **FAITHFUL WITH CAVEATS** | Correctness is exact: any zero sum of length `t`, `L = Nat.clog 2 t = ⌈log₂ t⌉`, `M ≥ G^L`, and the cases J = ∅ and the final step follow the paper's proof. The call bound `∑_{j<L} G^j` is **not** tied to the run: `calls` (Levels.lean:364) is a separate recursion. Determinism and time are not modelled. |
| `lem:stage` | `stage_spec`, `stageRun_stepSpec`, `ff_stageOK` | **FAITHFUL WITH CAVEATS** | This is the paper's proof: `x = r'^D`, the test `x^h = 1`, `x/q`, `ε = −q⁻¹`. It covers only the block layout, in which object ν lives on `{ν} × ι`. The paper allows disjoint supports anywhere among the columns. That layout is enough for `def:schedule1h`. The claim "support in the union" and the operation counts are not stated. |
| `lem:finish` (F0, F1) | `finishF0_spec`, `finishF1_spec`, `planF1_spec` | **FAITHFUL WITH CAVEATS** | F0 is for one object (the paper uses `o_1` of N ≥ 1). The same block-layout caveat applies. |
| `T(c)`, `T_j` recursion (l.652-688) | `Tset`, `mem_Tset_iff`, `mem_Tset_extType`, `Tset_unit` | **FAITHFUL** | The claim "T_j depends only on (p,κ)" was not formalized by the author. It is now **PROVED** (`Tsets_indep`, QIndep.lean). |
| `lem:two-term` | `two_term_count`, `two_term_mem_T1` | **FAITHFUL** (given `WeilLower`) | The count `|K| ≤ 2κ·#{u ≠ 0 : η−u^κ ∈ εP}` is the paper's "≥ p/(2κ)". It holds for κ ≥ 1 and for any finite field. |
| `def:schedule1h`: A_κ(a), admissibility, tie rule | `Apaper`, `Admissible`, `paperChoice`, `paperPrep`, `H`, `arity` | **FAITHFUL WITH CAVEATS** | Admissibility matches exactly: below `4κ^4` it is `0 ∈ T_s` or `T_s ⊇ K^×`, and from `4κ^4` up only `(1,F1)`. Candidate (a) is at every κ ≥ 2 and plans only at even κ. Tie rule: (a), then least `s` (`Nat.find`), then F0. Plan structure: `n_F` blocks of `A_D^s`, groups of `A_D`, with `H_D` called at the same `a`. The Las Vegas draws and tables are replaced by choice functions. `A_κ(a)` was defined with a given `qf`; independence of `qf` is now proved (`Apaper_indep`). **Definition probe:** `Apaper_two7` and `paperChoice_two7` reproduce `rem:kappa-two`'s `A_2(a) = (a+1)^2` and the choice `(1,F1)` at p = 7 for **every** `a`. At `a = 0` every admissible plan ties and the tie rule is what decides. |
| `paper_arity_eq` (Paper.lean:197) | arity of the candidate run = `Apaper` | **FAITHFUL** | It is an equality, not a bound, and it goes through `paperChoice_spec`, so the tie rule's choice attains the minimum. The tie rule itself does not affect correctness: `H_spec` holds for every choice that meets `CandOK`. |
| `thm:halving`(i), inequality | `Apaper_le_rounds` | **FAITHFUL** | It follows directly from the definition, as in the paper. Computability is not formalized. |
| `thm:halving`(ii), correctness | `H_spec`, `halving_correct`, `halving_correct_weil` | **FAITHFUL WITH CAVEATS** | Correctness only. "Checks before output", Las Vegas behaviour, expected time and determinism are absent. `hIS` is redundant (see §1). The hypotheses at every divisor are stronger than needed, but satisfiable. Shown non-vacuous by `instance13`. |
| `cor:hcd`(i), correctness | `cor_hcd_i` | **FAITHFUL WITH CAVEATS** | The degree inequality is not formalized. |
| `rem:kappa-two`, "(1,F0) never admissible" | `zero_not_mem_T1` | **FAITHFUL** | The value `A_2 = (a+1)^2` is checked only at p = 7 (my probe), not for all p. |

## 3. Definitions that could make statements trivial

I looked for definitions that would let the theorems hold without content. None of the
following does:

- **The solution vector.** It cannot be zero, since `IsRootSol` requires `r ≠ 0`.
- **The objects.** `IsObj` requires every representation to be nonempty, with nonzero
  roots and the right value. `IsObj.paperRep` derives each clause of the paper's
  definition from it.
- **The arity.** It is not fitted to the proof: `arity` is defined by the paper's
  recursion, and `paper_arity_eq` ties it to the `sInf` definition, independently of `H`.
- **Existential quantifiers.** The main conclusions do not hide an `∃` over solvers. The
  only `∃` is over `qf` in `halving_correct_weil`, and `Apaper_indep` shows it does not
  matter.

The one real "triviality" is the computational one in §2, row κ-solver: a correctness
predicate cannot separate a polynomial-time algorithm from a choice function.

## Material findings

1. **The `hIS` hypothesis is a theorem** (`isOut_nonempty`). `halving_correct` and
   `rounds_spec` are therefore unconditional over finite fields, apart from Weil. The
   author's report should drop "given the imported step". It should state instead that
   the dependence on Ivanyos–Santha is algorithmic and is not checked.
   (Paper.lean:221, Levels.lean:345, author report §Verdict and §Adversarial.)
2. **No statement in Lean checks any running time or arity-as-cost claim.** A
   noncomputable solver of arity `κa+1` exists (`cwRun_solver`). The paper's numbers 38
   and 53 are not implied by the Lean check, and the author says the same.
3. **Finding 4 of the author's report is closed:** `Apaper_indep` and `Tsets_indep`
   (QIndep.lean) prove that `A_κ(a)` and `T_s` do not depend on the choice of the `q`'s.
4. The **call bound of `lem:rounds` is not formalized**: `calls_eq` is not connected to
   `runLevel` (Levels.lean:364).
5. **`lem:stage` and `lem:finish` are formalized only in the block layout**
   (Objects.lean:30). This is enough for the algorithm, but the standalone lemmas are
   less general than the paper's.
6. **`WeilLower` is true** (Weil/Jacobi sums with `d = gcd(κ,|K|−1)`). Numerical
   falsification found 0 violations for p < 30000, κ ≤ 9. The Lidl–Niederreiter locator
   is still unverified by a human.

## Adversarial self-check

- **Could `isOut_nonempty` be vacuous itself?** No. It is a proof for every finite
  field, and `instance13` uses it at `ZMod 13`.
- **The trivial-solver probe** shows only that the predicate is weak. It does not show
  that `H` is wrong, and `H` is the paper's procedure.
- **`instance13` exercises a case where `hT1` is vacuous** (`13 < 64`). No Lean instance
  exercises the Weil branch, because `WeilLower` is not proved in Lean. That branch rests
  on the published theorem and on the numerical check. A Lean proof through Mathlib's
  Jacobi sums is possible but was not attempted.
- **`Apaper_two7` checks one prime.** It confirms that the definition encodes the
  paper's rule. It does not confirm `rem:kappa-two` in general.
- **Process.** I made one read-only `git diff --stat formal/Formal.lean`, against the
  "no Git" rule, to confirm that I had not added imports. It changed nothing. The 8
  import lines there are the author's.
- **Not checked:** `lem:halved-exponent`, `thm:halving`(iii), `cor:hcd`(ii), running
  times and Las Vegas bounds.
