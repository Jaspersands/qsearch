import Formal.CycleIndicator
import Formal.CoeffList
import Formal.CrossCheck
import Formal.PermTrace
import Formal.StdRepExterior
import Formal.FieldThreshold

/-!
# Axiom audit

Each headline theorem is checked to depend only on Lean's three standard axioms
(`propext`, `Classical.choice`, `Quot.sound`). If any proof used `sorry`, the
axiom list would contain `sorryAx`, the `#guard_msgs` check would fail, and so
would `lake build`.
-/

/-- info: 'QSearch.permDet_eq_mul_stdDet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.permDet_eq_mul_stdDet

/-- info: 'QSearch.one_add_X_dvd_permDet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.one_add_X_dvd_permDet

/-- info: 'QSearch.stdDet_unique' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.stdDet_unique

/-- info: 'QSearch.stdDet_eval_neg_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.stdDet_eval_neg_one

/-- info: 'QSearch.cycle_indicator' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.cycle_indicator

/-- info: 'QSearch.cycle_indicator_of_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.cycle_indicator_of_eq

/-- info: 'QSearch.stdDet_coeff_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.stdDet_coeff_zero

/-- info: 'QSearch.perm_cycle_indicator' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.perm_cycle_indicator

/-- info: 'QSearch.ofCoeffList_extCharsList' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ofCoeffList_extCharsList

/-- info: 'QSearch.stdDet_coeff_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.stdDet_coeff_eq

/-- info: 'QSearch.altSum_extCharsList' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.altSum_extCharsList

/-- info: 'QSearch.CrossCheck.extCharsList_eq_python' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CrossCheck.extCharsList_eq_python

/-- info: 'QSearch.CrossCheck.python_cycle_indicator' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CrossCheck.python_cycle_indicator

/-- info: 'QSearch.CrossCheck.stdDet_eq_python' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CrossCheck.stdDet_eq_python

/-- info: 'QSearch.CrossCheck.stdDet_coeff_eq_python' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CrossCheck.stdDet_coeff_eq_python

/-- info: 'QSearch.stdDet_coeff_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.stdDet_coeff_one

/-- info: 'QSearch.count_one_partition' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.count_one_partition

/-- info: 'QSearch.trace_stdRep' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.trace_stdRep

/-- info: 'QSearch.quotient_coeff_one_eq_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.quotient_coeff_one_eq_trace

/-- info: 'QSearch.sum_map_stdRep_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.sum_map_stdRep_eq_zero

/-- info: 'QSearch.exterior_std_no_invariants' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.exterior_std_no_invariants

/-- info: 'QSearch.extStdRep_invariants_eq_bot' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.extStdRep_invariants_eq_bot

/-- info: 'QSearch.ceilSqrt_eq_ceil_sqrt' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ceilSqrt_eq_ceil_sqrt

/-- info: 'QSearch.A_mul_sqrt_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.A_mul_sqrt_le

/-- info: 'QSearch.four_A_mul_ceilSqrt_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.four_A_mul_ceilSqrt_le

/-- info: 'QSearch.traceBound_ge_inv_two_n' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.traceBound_ge_inv_two_n

/-- info: 'QSearch.exterior_threshold_suffices' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.exterior_threshold_suffices

/-- info: 'QSearch.sum_choose_Ico' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.sum_choose_Ico

/-- info: 'QSearch.irreducible_rate_ge_traceBound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.irreducible_rate_ge_traceBound
