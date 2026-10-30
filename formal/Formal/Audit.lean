import Formal.CycleIndicator
import Formal.CoeffList
import Formal.CrossCheck
import Formal.PermTrace
import Formal.StdRepExterior
import Formal.FieldThreshold
import Formal.BalancedSigned
import Formal.ReesHomogenization
import Formal.ReesPrimePowerInterpolation
import Formal.ReesLieConstruction
import Formal.ReesLieInterpolation
import Formal.BCHClassThree
import Formal.BCHClassThreeSubgroups
import Formal.ReesGroupClassThree
import Formal.ReesCentralQuotient
import Formal.ReesCentralQuotientBCH
import Formal.ReesClassThreeReceiver
import Formal.CentralCharacterDescent
import Formal.CentralQuotientReceiver
import Formal.CentralSpectralProjector
import Formal.CentralDescentRecords
import Formal.CentralDescentPolicy
import Formal.ReesMeasuredReceiver

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

/-- info: 'QSearch.BalancedSigned.rational_separation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BalancedSigned.rational_separation

/-- info: 'QSearch.BalancedSigned.box_injective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BalancedSigned.box_injective

/-- info: 'QSearch.BalancedSigned.positive_readout_separation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BalancedSigned.positive_readout_separation

/-- info: 'QSearch.BalancedSigned.negative_readout_separation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BalancedSigned.negative_readout_separation

/-- info: 'QSearch.BalancedSigned.integer_label_encoding' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BalancedSigned.integer_label_encoding

/-- info: 'QSearch.BalancedSigned.integer_label_separation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BalancedSigned.integer_label_separation

/-- info: 'QSearch.BalancedSigned.budget_guard_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BalancedSigned.budget_guard_iff

/-- info: 'QSearch.BalancedSigned.readout_guard_counterexample' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BalancedSigned.readout_guard_counterexample

/-- info: 'QSearch.BalancedSigned.counterexample_points_valid' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BalancedSigned.counterexample_points_valid

/-! Rees interfaces and the actual nontransverse normalized descent source. -/

/-- info: 'QSearch.ReesHomogenization.applyRows_mul' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.applyRows_mul

/-- info: 'QSearch.ReesHomogenization.applyRows_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.applyRows_one

/-- info: 'QSearch.ReesHomogenization.evaluationMatrix_apply' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.evaluationMatrix_apply

/-- info: 'QSearch.ReesHomogenization.evaluation_det_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.evaluation_det_ne_zero

/-- info: 'QSearch.ReesHomogenization.rows_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.rows_mem

/-- info: 'QSearch.ReesHomogenization.coefficientwise_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.coefficientwise_iff

/-- info: 'QSearch.ReesHomogenization.tuple_hides' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.tuple_hides

/-- info: 'QSearch.ReesHomogenization.coefficient_translate' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.coefficient_translate

/-- info: 'QSearch.ReesHomogenization.coefficient_allowed' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.coefficient_allowed

/-- info: 'QSearch.CentralCharacterDescent.coefficient_allowed' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.coefficient_allowed

/-- info: 'QSearch.CentralCharacterDescent.twisted_trace_allowed' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.twisted_trace_allowed

/-- info: 'QSearch.CentralCharacterDescent.label_probability_allowed' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.label_probability_allowed

/-- info: 'QSearch.CentralCharacterDescent.label_probability_allowed_ne_zero' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.label_probability_allowed_ne_zero

/-- info: 'QSearch.CentralCharacterDescent.normalized_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_source

/-- info: 'QSearch.CentralCharacterDescent.normalized_correlation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_correlation

/-- info: 'QSearch.CentralCharacterDescent.normalized_correlation_at' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_correlation_at

/-- info: 'QSearch.CentralCharacterDescent.normalized_correlation_off' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_correlation_off

/-- info: 'QSearch.CentralCharacterDescent.normalized_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_trace

/-- info: 'QSearch.CentralCharacterDescent.mem_saturation_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.mem_saturation_iff

/-- info: 'QSearch.CentralCharacterDescent.normalized_descent_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_descent_output

/-- info: 'QSearch.ReesHomogenization.coefficientwise_iff_of_isUnit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.coefficientwise_iff_of_isUnit

/-- info: 'QSearch.ReesHomogenization.tuple_hides_of_isUnit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.tuple_hides_of_isUnit

/-- info: 'QSearch.ReesPrimePowerInterpolation.small_nat_unit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesPrimePowerInterpolation.small_nat_unit

/-- info: 'QSearch.ReesPrimePowerInterpolation.points_unit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesPrimePowerInterpolation.points_unit

/-- info: 'QSearch.ReesPrimePowerInterpolation.difference_unit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesPrimePowerInterpolation.difference_unit

/-- info: 'QSearch.ReesPrimePowerInterpolation.evaluation_det_unit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesPrimePowerInterpolation.evaluation_det_unit

/-- info: 'QSearch.ReesPrimePowerInterpolation.coefficientwise_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesPrimePowerInterpolation.coefficientwise_iff

/-- info: 'QSearch.ReesPrimePowerInterpolation.tuple_hides' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesPrimePowerInterpolation.tuple_hides

/-- info: 'QSearch.ReesPrimePowerInterpolation.bad_points_distinct_units' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesPrimePowerInterpolation.bad_points_distinct_units

/-- info: 'QSearch.ReesPrimePowerInterpolation.bad_points_nonzero_nonunit_determinant' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesPrimePowerInterpolation.bad_points_nonzero_nonunit_determinant

/-- info: 'QSearch.ReesPrimePowerInterpolation.bad_points_lose_coefficients' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesPrimePowerInterpolation.bad_points_lose_coefficients

/-- info: 'QSearch.ReesLieConstruction.gamma_bracket_le' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.gamma_bracket_le

/-- info: 'QSearch.ReesLieConstruction.rees' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.rees

/-- info: 'QSearch.ReesLieConstruction.mem_rees_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.mem_rees_iff

/-- info: 'QSearch.ReesLieConstruction.nilpotent_cutoff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.nilpotent_cutoff

/-- info: 'QSearch.ReesLieConstruction.currentEval' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.currentEval

/-- info: 'QSearch.ReesLieConstruction.evaluation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.evaluation

/-- info: 'QSearch.ReesLieConstruction.evaluation_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.evaluation_formula

/-- info: 'QSearch.ReesLieConstruction.grade_one_retention' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.grade_one_retention

/-- info: 'QSearch.ReesLieConstruction.currentScale' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.currentScale

/-- info: 'QSearch.ReesLieConstruction.scaling_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.scaling_coeff

/-- info: 'QSearch.ReesLieConstruction.dilation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.dilation

/-- info: 'QSearch.ReesLieConstruction.rees_class_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.rees_class_bound

/-- info: 'QSearch.ReesLieInterpolation.evaluation_finite' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.evaluation_finite

/-- info: 'QSearch.ReesLieInterpolation.evaluation_rows' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.evaluation_rows

/-- info: 'QSearch.ReesLieInterpolation.hiddenCover' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.hiddenCover

/-- info: 'QSearch.ReesLieInterpolation.mem_hiddenCover_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.mem_hiddenCover_iff

/-- info: 'QSearch.ReesLieInterpolation.scaling_preserves_hiddenCover' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.scaling_preserves_hiddenCover

/-- info: 'QSearch.ReesLieInterpolation.dilation_mem_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.dilation_mem_iff

/-- info: 'QSearch.ReesLieInterpolation.prime_power_hiddenCover_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.prime_power_hiddenCover_iff

/-! Actual class-three group laws and concrete Rees group transport. -/

/-- info: 'QSearch.BCHClassThree.classThree_of_lowerCentralSeries' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.classThree_of_lowerCentralSeries

/-- info: 'QSearch.BCHClassThree.bch_assoc_of_classThree' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.bch_assoc_of_classThree

/-- info: 'QSearch.BCHClassThree.bch_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.bch_assoc

/-- info: 'QSearch.BCHClassThree.instGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.instGroup

/-- info: 'QSearch.BCHClassThree.val_mul_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.val_mul_formula

/-- info: 'QSearch.BCHClassThree.lieHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.lieHom

/-- info: 'QSearch.BCHClassThree.lieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.lieEquiv

/-- info: 'QSearch.BCHClassThree.val_zpow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.val_zpow

/-- info: 'QSearch.ReesGroupClassThree.canonical_det' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.canonical_det

/-- info: 'QSearch.ReesGroupClassThree.canonical_det_unit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.canonical_det_unit

/-- info: 'QSearch.ReesGroupClassThree.subgroupOfLie' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.subgroupOfLie

/-- info: 'QSearch.ReesGroupClassThree.evaluationHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.evaluationHom

/-- info: 'QSearch.ReesGroupClassThree.evaluation_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.evaluation_identity

/-- info: 'QSearch.ReesGroupClassThree.mem_hiddenSubgroup_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.mem_hiddenSubgroup_iff

/-- info: 'QSearch.ReesGroupClassThree.tuple_hides' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.tuple_hides

/-- info: 'QSearch.ReesGroupClassThree.tuple_hides_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.tuple_hides_subgroup

/-- info: 'QSearch.ReesGroupClassThree.dilationEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.dilationEquiv

/-- info: 'QSearch.ReesGroupClassThree.dilation_hidden_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.dilation_hidden_iff

/-- info: 'QSearch.BCHClassThreeSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.val_comm

/-- info: 'QSearch.BCHClassThreeSubgroups.val_nested_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.val_nested_comm

/-- info: 'QSearch.BCHClassThreeSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassThreeSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.val_addWord

/-- info: 'QSearch.BCHClassThreeSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassThreeSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassThreeSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassThreeSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassThreeSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.toSubgroup_toLieSubalgebra

/-- info: 'QSearch.ReesGroupClassThree.arbitrary_subgroup_roundtrip' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.arbitrary_subgroup_roundtrip

/-- info: 'QSearch.ReesGroupClassThree.lifted_mem_coefficients' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.lifted_mem_coefficients

/-- info: 'QSearch.ReesGroupClassThree.tuple_hides_arbitrary_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.tuple_hides_arbitrary_subgroup

/-- info: 'QSearch.ReesGroupClassThree.dilation_arbitrary_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.dilation_arbitrary_subgroup

/-- info: 'QSearch.CentralQuotientReceiver.disallowed_character_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.disallowed_character_sum

/-- info: 'QSearch.CentralQuotientReceiver.disallowed_coefficient' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.disallowed_coefficient

/-- info: 'QSearch.CentralQuotientReceiver.disallowed_projected_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.disallowed_projected_source

/-- info: 'QSearch.CentralQuotientReceiver.nonzero_branch_iff_allowed' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.nonzero_branch_iff_allowed

/-- info: 'QSearch.CentralQuotientReceiver.quotient_membership' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.quotient_membership

/-- info: 'QSearch.CentralQuotientReceiver.dilation_preserves_saturation' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.dilation_preserves_saturation

/-- info: 'QSearch.CentralQuotientReceiver.cancelled_normalized_correlation' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.cancelled_normalized_correlation

/-- info: 'QSearch.CentralQuotientReceiver.quotient_coset_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.quotient_coset_output

/-- info: 'QSearch.CentralQuotientReceiver.active_sde' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.active_sde

/-- info: 'QSearch.CentralQuotientReceiver.active_nonempty' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.active_nonempty

/-- info: 'QSearch.CentralQuotientReceiver.sde_character_cancellation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.sde_character_cancellation

/-- info: 'QSearch.CentralQuotientReceiver.scalar_quotient_coset_output' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.scalar_quotient_coset_output

/-- info: 'QSearch.ReesCentralQuotient.bracket_vanishes' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.bracket_vanishes

/-- info: 'QSearch.ReesCentralQuotient.tail' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.tail

/-- info: 'QSearch.ReesCentralQuotient.trunc_class_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.trunc_class_bound

/-- info: 'QSearch.ReesCentralQuotient.projection' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.projection

/-- info: 'QSearch.ReesCentralQuotient.top_kernel_central' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.top_kernel_central

/-- info: 'QSearch.ReesCentralQuotient.finiteCoefficients_injective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.finiteCoefficients_injective

/-- info: 'QSearch.ReesCentralQuotient.top_kernel_dilation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.top_kernel_dilation

/-- info: 'QSearch.ReesCentralQuotient.fullEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.fullEquiv

/-- info: 'QSearch.ReesCentralQuotient.terminalEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.terminalEquiv

/-- info: 'QSearch.ReesCentralQuotient.top_kernel_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.top_kernel_iff

/-- info: 'QSearch.ReesCentralQuotient.dilation_topEmbedding' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.dilation_topEmbedding

/-- info: 'QSearch.ReesCentralQuotientBCH.trunc_classThree' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.trunc_classThree

/-- info: 'QSearch.ReesCentralQuotientBCH.finiteTruncGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.finiteTruncGroup

/-- info: 'QSearch.ReesCentralQuotientBCH.stepQuotientEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.stepQuotientEquiv

/-- info: 'QSearch.ReesCentralQuotientBCH.fullGroupEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.fullGroupEquiv

/-- info: 'QSearch.ReesCentralQuotientBCH.centralEmbedding' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.centralEmbedding

/-- info: 'QSearch.ReesCentralQuotientBCH.centralEmbedding_injective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.centralEmbedding_injective

/-- info: 'QSearch.ReesCentralQuotientBCH.pi32_kernel_eq_range' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.pi32_kernel_eq_range

/-- info: 'QSearch.ReesCentralQuotientBCH.pi21_kernel_eq_range' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.pi21_kernel_eq_range

/-- info: 'QSearch.ReesCentralQuotientBCH.projectHom_kernel_central' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.projectHom_kernel_central

/--
info: 'QSearch.ReesCentralQuotientBCH.groupDilation_centralEmbedding' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
-/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.groupDilation_centralEmbedding

/-- info: 'QSearch.ReesCentralQuotientBCH.dilation_hiddenImage_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.dilation_hiddenImage_iff

/-- info: 'QSearch.ReesCentralQuotientBCH.terminalGroupEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.terminalGroupEquiv

/-- info: 'QSearch.ReesCentralQuotientBCH.terminal_arbitrary_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.terminal_arbitrary_subgroup

/-- info: 'QSearch.ReesClassThreeReceiver.sectionLie32_right_inverse' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.sectionLie32_right_inverse

/-- info: 'QSearch.ReesClassThreeReceiver.section32_right_inverse' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.section32_right_inverse

/-- info: 'QSearch.ReesClassThreeReceiver.section21_right_inverse' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.section21_right_inverse

/-- info: 'QSearch.ReesClassThreeReceiver.stageHidden_projection' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.stageHidden_projection

/-- info: 'QSearch.ReesClassThreeReceiver.step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.step_output

/-- info: 'QSearch.ReesClassThreeReceiver.degree_three_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.degree_three_output

/-- info: 'QSearch.ReesClassThreeReceiver.degree_two_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.degree_two_output

/-- info: 'QSearch.ReesClassThreeReceiver.terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.terminal_source

/-- info: 'QSearch.CentralSpectralProjector.ancillaKraus_eq_projector' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralSpectralProjector.ancillaKraus_eq_projector

/-- info: 'QSearch.CentralSpectralProjector.projector_self_adjoint' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralSpectralProjector.projector_self_adjoint

/-- info: 'QSearch.CentralSpectralProjector.projector_idempotent' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralSpectralProjector.projector_idempotent

/-- info: 'QSearch.CentralSpectralProjector.projector_orthogonal' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralSpectralProjector.projector_orthogonal

/-- info: 'QSearch.CentralSpectralProjector.projector_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralSpectralProjector.projector_sum

/-- info: 'QSearch.CentralSpectralProjector.projector_kraus_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralSpectralProjector.projector_kraus_complete

/-- info: 'QSearch.CentralSpectralProjector.ancilla_kraus_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralSpectralProjector.ancilla_kraus_complete

/-- info: 'QSearch.CentralSpectralProjector.two_sided_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralSpectralProjector.two_sided_source

/-- info: 'QSearch.CentralSpectralProjector.ancilla_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralSpectralProjector.ancilla_source

/-- info: 'QSearch.CentralDescentRecords.tensor_two_sided' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.tensor_two_sided

/-- info: 'QSearch.CentralDescentRecords.zero_mass_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.zero_mass_source

/-- info: 'QSearch.CentralDescentRecords.projected_mass_normalized' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.projected_mass_normalized

/-- info: 'QSearch.CentralDescentRecords.padded_relative' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.padded_relative

/-- info: 'QSearch.CentralDescentRecords.normalized_padded_correlation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.normalized_padded_correlation

/-- info: 'QSearch.CentralDescentRecords.normalized_padded_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.normalized_padded_output

/-- info: 'QSearch.CentralDescentRecords.all_record_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.all_record_output

/-- info: 'QSearch.ReesMeasuredReceiver.linear_instrument_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.linear_instrument_complete

/-- info: 'QSearch.ReesMeasuredReceiver.measured_branch_eq_projected' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_branch_eq_projected

/-- info: 'QSearch.ReesMeasuredReceiver.linear_projector_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.linear_projector_sum

/-- info: 'QSearch.ReesMeasuredReceiver.measured_branch_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_branch_sum

/-- info: 'QSearch.ReesMeasuredReceiver.measured_mass_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_mass_sum

/-- info: 'QSearch.ReesMeasuredReceiver.branch_mass_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.branch_mass_sum

/-- info: 'QSearch.ReesMeasuredReceiver.packet_mass_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.packet_mass_sum

/-- info: 'QSearch.ReesMeasuredReceiver.measured_packet_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_packet_eq

/-- info: 'QSearch.ReesMeasuredReceiver.measured_step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_step_output

/-- info: 'QSearch.ReesMeasuredReceiver.averaged_step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.averaged_step_output

/-- info: 'QSearch.ReesMeasuredReceiver.degree_three_measured' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.degree_three_measured

/-- info: 'QSearch.ReesMeasuredReceiver.degree_two_measured' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.degree_two_measured

/-- info: 'QSearch.ReesMeasuredReceiver.convert_step_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.convert_step_source

/-- info: 'QSearch.ReesMeasuredReceiver.two_stage_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.two_stage_source

/-- info: 'QSearch.ReesMeasuredReceiver.measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_terminal_source

/-- info: 'QSearch.CentralDescentPolicy.padded_relative' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.padded_relative

/-- info: 'QSearch.CentralDescentPolicy.packet_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.packet_trace

/-- info: 'QSearch.CentralDescentPolicy.normalized_padded_correlation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.normalized_padded_correlation

/-- info: 'QSearch.CentralDescentPolicy.normalized_padded_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.normalized_padded_output

/-- info: 'QSearch.CentralDescentPolicy.all_record_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.all_record_output

/-- info: 'QSearch.CentralDescentPolicy.discarded_output_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.discarded_output_eq

/-- info: 'QSearch.CentralDescentPolicy.selected_mass_partition' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.selected_mass_partition

/-- info: 'QSearch.CentralDescentPolicy.accepted_output_factorization' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.accepted_output_factorization

/-- info: 'QSearch.CentralDescentPolicy.accepted_output_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.accepted_output_trace

/-- info: 'QSearch.CentralDescentPolicy.abort_output_factorization' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.abort_output_factorization

/-- info: 'QSearch.CentralDescentPolicy.accepted_abort_mass_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.accepted_abort_mass_conservation

/-- info: 'QSearch.CentralDescentPolicy.accepted_abort_trace_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.accepted_abort_trace_conservation

/-- info: 'QSearch.CentralDescentPolicy.randomized_record_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.randomized_record_sum

/-- info: 'QSearch.CentralDescentPolicy.randomized_mass_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.randomized_mass_conservation

/-- info: 'QSearch.CentralDescentPolicy.randomized_mass_conservation_of_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.randomized_mass_conservation_of_complete

/-- info: 'QSearch.CentralDescentPolicy.randomized_output_trace_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.randomized_output_trace_conservation

/-- info: 'QSearch.CentralDescentPolicy.measured_bank_eq_packet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_bank_eq_packet

/-- info: 'QSearch.CentralDescentPolicy.projected_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.projected_sum

/-- info: 'QSearch.CentralDescentPolicy.packet_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.packet_sum

/-- info: 'QSearch.CentralDescentPolicy.independent_source_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.independent_source_trace

/-- info: 'QSearch.CentralDescentPolicy.measured_bank_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_bank_sum

/-- info: 'QSearch.CentralDescentPolicy.measured_bank_mass_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_bank_mass_sum

/-- info: 'QSearch.CentralDescentPolicy.measured_accepted_output_factorization' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_accepted_output_factorization

/-- info: 'QSearch.CentralDescentPolicy.measured_randomized_output_trace_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_randomized_output_trace_conservation
