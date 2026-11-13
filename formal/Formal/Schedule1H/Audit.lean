import Formal.Schedule1H.Paper
import Formal.Schedule1H.Extras

/-!
# Schedule 1H: axiom audit and a run

Each theorem below is checked to depend only on `propext`, `Classical.choice` and
`Quot.sound`; a `sorry` would add `sorryAx` and fail the `#guard_msgs` check.

The run at the end executes the compiled solver `H` at `κ = 2` over `ZMod 7` (one
halving stage, finish F1, over Gaussian elimination: arity `(a+1)^2 = 9` at `a = 2`).
It is a test of the compiled code, not a proof.
-/

/-- info: 'QSearch.Schedule1H.isKSolution_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.isKSolution_iff

/-- info: 'QSearch.Schedule1H.IsObj.paperRep' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.IsObj.paperRep

/-- info: 'QSearch.Schedule1H.padRun_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.padRun_spec

/-- info: 'QSearch.Schedule1H.solOf_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.solOf_spec

/-- info: 'QSearch.Schedule1H.combine_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.combine_spec

/-- info: 'QSearch.Schedule1H.step_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.step_spec

/-- info: 'QSearch.Schedule1H.mem_Tset_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.mem_Tset_iff

/-- info: 'QSearch.Schedule1H.finishGen_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.finishGen_spec

/-- info: 'QSearch.Schedule1H.finishF0_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.finishF0_spec

/-- info: 'QSearch.Schedule1H.finishF1_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.finishF1_spec

/-- info: 'QSearch.Schedule1H.runLevel_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.runLevel_spec

/-- info: 'QSearch.Schedule1H.planF0_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.planF0_spec

/-- info: 'QSearch.Schedule1H.planF1_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.planF1_spec

/-- info: 'QSearch.Schedule1H.ISOut.stepSpec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.ISOut.stepSpec

/-- info: 'QSearch.Schedule1H.zeroSum_lift' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.zeroSum_lift

/-- info: 'QSearch.Schedule1H.rounds_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.rounds_spec

/-- info: 'QSearch.Schedule1H.calls_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.calls_eq

/-- info: 'QSearch.Schedule1H.stageRun_stepSpec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.stageRun_stepSpec

/-- info: 'QSearch.Schedule1H.stage_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.stage_spec

/-- info: 'QSearch.Schedule1H.exists_root_of_pow_eq_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.exists_root_of_pow_eq_one

/-- info: 'QSearch.Schedule1H.pow_h_eq_one_or_neg_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.pow_h_eq_one_or_neg_one

/-- info: 'QSearch.Schedule1H.ff_stageOK' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.ff_stageOK

/-- info: 'QSearch.Schedule1H.exists_q' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.exists_q

/-- info: 'QSearch.Schedule1H.H_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.H_spec

/-- info: 'QSearch.Schedule1H.card_sol_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.card_sol_le

/-- info: 'QSearch.Schedule1H.two_term_count' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.two_term_count

/-- info: 'QSearch.Schedule1H.two_term_mem_T1' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.two_term_mem_T1

/-- info: 'QSearch.Schedule1H.zeroSums_nonempty' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.zeroSums_nonempty

/-- info: 'QSearch.Schedule1H.Apaper_le_rounds' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.Apaper_le_rounds

/-- info: 'QSearch.Schedule1H.paperChoice_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.paperChoice_spec

/-- info: 'QSearch.Schedule1H.paper_arity_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.paper_arity_eq

/-- info: 'QSearch.Schedule1H.halving_correct' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.halving_correct

/-- info: 'QSearch.Schedule1H.halving_correct_weil' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.halving_correct_weil

/-- info: 'QSearch.Schedule1H.Tset_unit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.Tset_unit

/-- info: 'QSearch.Schedule1H.mem_Tset_extType' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.mem_Tset_extType

/-- info: 'QSearch.Schedule1H.zero_not_mem_T1' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.zero_not_mem_T1

/-- info: 'QSearch.Schedule1H.Tset_subset_extType' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.Tset_subset_extType

/-- info: 'QSearch.Schedule1H.cor_hcd_i' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1H.cor_hcd_i

namespace QSearch.Schedule1H.Run

open QSearch.Schedule1H

local instance : Fact (Nat.Prime 7) := ⟨by norm_num⟩

/-- All elements of `ZMod 7`. -/
def elems7 : List (ZMod 7) := (List.finRange 7).map fun i => (i : ZMod 7)

/-- A square root by search (`0` if none). -/
def sqrt7 (x : ZMod 7) : ZMod 7 := (elems7.find? fun r => r ^ 2 == x).getD 0

/-- `q = 3` has `q^3 = -1` in `ZMod 7` (`h = 3`), so `ε = -q⁻¹ = 2`. -/
def q7 : ZMod 7 := 3

/-- F1 table at `s = 1`: some `(u, v) ≠ 0` with `u^2 + ε v^2 = x`, by search. -/
def fin7 (x : ZMod 7) : Typ 1 → ZMod 7 :=
  let ε : ZMod 7 := -q7⁻¹
  let pairs := elems7.flatMap fun u => elems7.map fun v => (u, v)
  match pairs.find? (fun uv => (uv.1 != 0 || uv.2 != 0) && uv.1 ^ 2 + ε * uv.2 ^ 2 == x) with
  | some uv => Sum.elim (fun _ => uv.1) (fun _ => uv.2)
  | none => fun _ => 0

/-- Preprocessing at `κ = 2` (the fields for candidate (a) are unused here). -/
def prep7 (κ : ℕ) : Prep (ZMod 7) κ where
  t := 0
  z := fun i => i.elim0
  isRun _ _ := (0, 0)
  q := q7
  cls := powTest 3
  rt := sqrt7
  f0 _ := 0
  f1 s x := if h : s = 1 then h ▸ fin7 x else 0

/-- Always the plan `(1, F1)`. -/
def ch7 : ℕ → ℕ → Cand := fun _ _ => .plan 1 true

/-- Nine columns in `(ZMod 7)^2`. -/
def cols7 : Fin 9 → Fin 2 → ZMod 7 :=
  ![![1, 0], ![0, 1], ![1, 1], ![2, 3], ![4, 1], ![3, 5], ![6, 6], ![5, 2], ![1, 4]]

/-- info: 9 -/
#guard_msgs in #eval arity prep7 ch7 2 2

/-- info: [0, 0] -/
#guard_msgs in
#eval let r := H prep7 ch7 2 2 9 cols7; (List.finRange 2).map (∑ i, r i ^ 2 • cols7 i)

/-- info: true -/
#guard_msgs in
#eval let r := H prep7 ch7 2 2 9 cols7; (List.finRange 9).any fun i => r i != 0

end QSearch.Schedule1H.Run
