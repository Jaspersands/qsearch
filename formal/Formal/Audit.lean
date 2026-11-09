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
import Formal.ReesGeneralCover
import Formal.ReesGeneralLaw
import Formal.ReesGeneralLawClassThree
import Formal.ReesGeneralReceiver
import Formal.BCHClassFour
import Formal.BCHClassFourSubgroups
import Formal.ReesGeneralLawClassFour
import Formal.BCHClassFive
import Formal.BCHClassFiveSubgroups
import Formal.ReesGeneralLawClassFive
import Formal.BCHClassSix
import Formal.BCHClassSixSubgroups
import Formal.ReesGeneralLawClassSix
import Formal.BCHClassSeven
import Formal.BCHClassSevenSubgroups
import Formal.ReesGeneralLawClassSeven
import Formal.ReesGeneralMeasuredReceiver
import Formal.ReesSdeGcd
import Formal.ReesSdeWitness
import Formal.ReesSdeTriangular
import Formal.ReesSdeQuadratic
import Formal.ReesSdePolicy
import Formal.ReesSdeSolver
import Formal.ReesMergeReduction
import Formal.ReesS2Local
import Formal.DixmierListerScalars
import Formal.DixmierListerGroup
import Formal.UnitriangularExpLog

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

/-! ## General-class Rees modules (promoted 2026-11-02)

Guards for `ReesGeneralCover`, `ReesGeneralLaw`, `ReesGeneralLawClassThree` and
`ReesGeneralReceiver`, first written in
`research/audits/reviews/2026-11-02-rees-lean/ReesGeneralAudit.lean`.
-/

/-- info: 'QSearch.ReesGeneralCover.evaluation_eq_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_eq_sum

/-- info: 'QSearch.ReesGeneralCover.homogeneousElement' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.homogeneousElement

/-- info: 'QSearch.ReesGeneralCover.evaluation_homogeneousElement' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_homogeneousElement

/-- info: 'QSearch.ReesGeneralCover.evaluation_gradeOne' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_gradeOne

/-- info: 'QSearch.ReesGeneralCover.evaluation_one_surjective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_one_surjective

/-- info: 'QSearch.ReesGeneralCover.lowerCentralSeries_rees_eq_bot_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.lowerCentralSeries_rees_eq_bot_iff

/-- info: 'QSearch.ReesGeneralCover.rees_class_exact' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.rees_class_exact

/-- info: 'QSearch.ReesGeneralCover.nilpotencyLength_rees' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.nilpotencyLength_rees

/-- info: 'QSearch.ReesGeneralCover.top_grade_central' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.top_grade_central

/-- info: 'QSearch.ReesGeneralCover.evaluation_comp_scaling' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_comp_scaling

/-- info: 'QSearch.ReesGeneralCover.evaluation_comp_dilation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_comp_dilation

/-- info: 'QSearch.ReesGeneralCover.evaluation_mem_gamma_of_tail' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_mem_gamma_of_tail

/-- info: 'QSearch.ReesGeneralCover.evaluation_image_tail' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_image_tail

/-- info: 'QSearch.ReesGeneralCover.evaluation_surjective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_surjective

/-- info: 'QSearch.ReesGeneralCover.mem_hiddenCover_iff_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.mem_hiddenCover_iff_coeff

/-- info: 'QSearch.ReesGeneralCover.mem_hiddenCover_iff_graded' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.mem_hiddenCover_iff_graded

/-- info: 'QSearch.ReesGeneralCover.mem_hiddenCover_iff_forall_eval' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.mem_hiddenCover_iff_forall_eval

/-- info: 'QSearch.ReesGeneralCover.hiddenCover_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.hiddenCover_eq

/-- info: 'QSearch.ReesGeneralCover.evaluation_image_hiddenCover' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.evaluation_image_hiddenCover

/-- info: 'QSearch.ReesGeneralCover.gradeOne_mem_hiddenCover_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.gradeOne_mem_hiddenCover_iff

/-- info: 'QSearch.ReesGeneralCover.field_points_isUnit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.field_points_isUnit

/-- info: 'QSearch.ReesGeneralCover.field_hiddenCover_mem_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.field_hiddenCover_mem_iff

/-- info: 'QSearch.ReesGeneralCover.field_hiddenCover_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralCover.field_hiddenCover_eq

/-- info: 'QSearch.ReesGeneralLaw.NilpotentGroupLaw' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.NilpotentGroupLaw

/-- info: 'QSearch.ReesGeneralLaw.AdditiveOnCommuting' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.AdditiveOnCommuting

/-- info: 'QSearch.ReesGeneralLaw.LawGroup' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.LawGroup

/-- info: 'QSearch.ReesGeneralLaw.lawHom' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.lawHom

/-- info: 'QSearch.ReesGeneralLaw.lawHom_surjective' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.lawHom_surjective

/-- info: 'QSearch.ReesGeneralLaw.lawEquiv' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.lawEquiv

/-- info: 'QSearch.ReesGeneralLaw.subgroupOfLie' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.subgroupOfLie

/-- info: 'QSearch.ReesGeneralLaw.comap_subgroupOfLie' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.comap_subgroupOfLie

/-- info: 'QSearch.ReesGeneralLaw.SubgroupsAreSubalgebras' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.SubgroupsAreSubalgebras

/-- info: 'QSearch.ReesGeneralLaw.mul_eq_add_of_lie_eq_zero' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.mul_eq_add_of_lie_eq_zero

/-- info: 'QSearch.ReesGeneralLaw.ReesGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.ReesGroup

/-- info: 'QSearch.ReesGeneralLaw.BaseGroup' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.BaseGroup

/-- info: 'QSearch.ReesGeneralLaw.evaluationHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.evaluationHom

/-- info: 'QSearch.ReesGeneralLaw.dilationHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.dilationHom

/-- info: 'QSearch.ReesGeneralLaw.evaluationHom_surjective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.evaluationHom_surjective

/-- info: 'QSearch.ReesGeneralLaw.evaluationHom_comp_dilation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.evaluationHom_comp_dilation

/-- info: 'QSearch.ReesGeneralLaw.hiddenSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.hiddenSubgroup

/-- info: 'QSearch.ReesGeneralLaw.hiddenSubgroup_eq_iInf' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.hiddenSubgroup_eq_iInf

/-- info: 'QSearch.ReesGeneralLaw.mem_hiddenSubgroup_iff_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.mem_hiddenSubgroup_iff_coeff

/-- info: 'QSearch.ReesGeneralLaw.hiddenSubgroup_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.hiddenSubgroup_eq

/-- info: 'QSearch.ReesGeneralLaw.tuple_hides' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.tuple_hides

/-- info: 'QSearch.ReesGeneralLaw.tuple_hides_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.tuple_hides_coeff

/-- info: 'QSearch.ReesGeneralLaw.tuple_hides_arbitrary_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.tuple_hides_arbitrary_subgroup

/-- info: 'QSearch.ReesGeneralLaw.dilation_hiddenSubgroup_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.dilation_hiddenSubgroup_iff

/-- info: 'QSearch.ReesGeneralLaw.evaluationHom_image_hiddenSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.evaluationHom_image_hiddenSubgroup

/-- info: 'QSearch.ReesGeneralLaw.trunc_class_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.trunc_class_le

/-- info: 'QSearch.ReesGeneralLaw.TruncGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.TruncGroup

/-- info: 'QSearch.ReesGeneralLaw.groupMk' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.groupMk

/-- info: 'QSearch.ReesGeneralLaw.groupMk_surjective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.groupMk_surjective

/-- info: 'QSearch.ReesGeneralLaw.groupMk_ker' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.groupMk_ker

/-- info: 'QSearch.ReesGeneralLaw.projectHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.projectHom

/-- info: 'QSearch.ReesGeneralLaw.projectHom_surjective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.projectHom_surjective

/-- info: 'QSearch.ReesGeneralLaw.projectHom_groupMk' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.projectHom_groupMk

/-- info: 'QSearch.ReesGeneralLaw.projectHom_kernel_central' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.projectHom_kernel_central

/-- info: 'QSearch.ReesGeneralLaw.projectHom_kernel_additive' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.projectHom_kernel_additive

/-- info: 'QSearch.ReesGeneralLaw.terminalGroupEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.terminalGroupEquiv

/-- info: 'QSearch.ReesGeneralLaw.terminalMap' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.terminalMap

/-- info: 'QSearch.ReesGeneralLaw.terminal_hidden_image' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.terminal_hidden_image

/-- info: 'QSearch.ReesGeneralLaw.groupDilation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.groupDilation

/-- info: 'QSearch.ReesGeneralLawClassThree.bchLaw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassThree.bchLaw

/-- info: 'QSearch.ReesGeneralLawClassThree.bchLaw_additive' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassThree.bchLaw_additive

/-- info: 'QSearch.ReesGeneralLawClassThree.toBCH' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassThree.toBCH

/-- info: 'QSearch.ReesGeneralLawClassThree.bchLaw_subgroups' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassThree.bchLaw_subgroups

/-- info: 'QSearch.ReesGeneralLawClassThree.classThree_tuple_hides_arbitrary_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassThree.classThree_tuple_hides_arbitrary_subgroup

/-- info: 'QSearch.ReesGeneralReceiver.centralEmbedding' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.centralEmbedding

/-- info: 'QSearch.ReesGeneralReceiver.centralEmbedding_injective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.centralEmbedding_injective

/-- info: 'QSearch.ReesGeneralReceiver.projectHom_kernel_eq_range' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.projectHom_kernel_eq_range

/-- info: 'QSearch.ReesGeneralReceiver.centralEmbedding_central' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.centralEmbedding_central

/-- info: 'QSearch.ReesGeneralReceiver.groupDilation_centralEmbedding' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.groupDilation_centralEmbedding

/-- info: 'QSearch.ReesGeneralReceiver.groupDilation_groupMk' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.groupDilation_groupMk

/-- info: 'QSearch.ReesGeneralReceiver.stageHidden' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.stageHidden

/-- info: 'QSearch.ReesGeneralReceiver.stageHidden_projection' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.stageHidden_projection

/-- info: 'QSearch.ReesGeneralReceiver.dilation_stageHidden_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.dilation_stageHidden_iff

/-- info: 'QSearch.ReesGeneralReceiver.canonicalSection' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.canonicalSection

/-- info: 'QSearch.ReesGeneralReceiver.canonicalSection_right_inverse' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.canonicalSection_right_inverse

/-- info: 'QSearch.ReesGeneralReceiver.step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.step_output

/-- info: 'QSearch.ReesGeneralReceiver.step_output_canonical' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.step_output_canonical

/-- info: 'QSearch.ReesGeneralReceiver.terminal_membership' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.terminal_membership

/-- info: 'QSearch.ReesGeneralReceiver.terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralReceiver.terminal_source

/-- info: 'QSearch.ReesGeneralLaw.instGroup' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLaw.instGroup

/-! ## Class-four BCH group (2026-11-02) -/

/-- info: 'QSearch.BCHClassFour.ClassFour' depends on axioms: [propext] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.ClassFour

/-- info: 'QSearch.BCHClassFour.jacobi3' depends on axioms: [propext] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.jacobi3

/-- info: 'QSearch.BCHClassFour.jacobi4a' depends on axioms: [propext] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.jacobi4a

/-- info: 'QSearch.BCHClassFour.jacobi4b' depends on axioms: [propext] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.jacobi4b

/-- info: 'QSearch.BCHClassFour.jacobi4b'' depends on axioms: [propext] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.jacobi4b'

/-- info: 'QSearch.BCHClassFour.jacobi4c' depends on axioms: [propext] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.jacobi4c

/-- info: 'QSearch.BCHClassFour.classFour_of_lowerCentralSeries' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.classFour_of_lowerCentralSeries

/-- info: 'QSearch.BCHClassFour.bch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch

/-- info: 'QSearch.BCHClassFour.bch_zero_left' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_zero_left

/-- info: 'QSearch.BCHClassFour.bch_zero_right' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_zero_right

/-- info: 'QSearch.BCHClassFour.bch_neg_left' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_neg_left

/-- info: 'QSearch.BCHClassFour.bch_neg_right' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_neg_right

/-- info: 'QSearch.BCHClassFour.bch_of_lie_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_of_lie_eq_zero

/-- info: 'QSearch.BCHClassFour.map_bch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.map_bch

/-- info: 'QSearch.BCHClassFour.bch_smul_same' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_smul_same

/-- info: 'QSearch.BCHClassFour.four_ne_zero'' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.four_ne_zero'

/-- info: 'QSearch.BCHClassFour.six_ne_zero'' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.six_ne_zero'

/-- info: 'QSearch.BCHClassFour.twelve_ne_zero'' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.twelve_ne_zero'

/-- info: 'QSearch.BCHClassFour.twentyfour_ne_zero'' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.twentyfour_ne_zero'

/-- info: 'QSearch.BCHClassFour.bch_assoc_of_classFour' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_assoc_of_classFour

/-- info: 'QSearch.BCHClassFour.bch_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_assoc

/-- info: 'QSearch.BCHClassFour.BCH' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.BCH

/-- info: 'QSearch.BCHClassFour.BCH.ext' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.BCH.ext

/-- info: 'QSearch.BCHClassFour.equiv' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.equiv

/-- info: 'QSearch.BCHClassFour.instGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.instGroup

/-- info: 'QSearch.BCHClassFour.val_mul' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.val_mul

/-- info: 'QSearch.BCHClassFour.val_mul_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.val_mul_formula

/-- info: 'QSearch.BCHClassFour.val_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.val_one

/-- info: 'QSearch.BCHClassFour.val_inv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.val_inv

/-- info: 'QSearch.BCHClassFour.val_pow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.val_pow

/-- info: 'QSearch.BCHClassFour.val_zpow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.val_zpow

/-- info: 'QSearch.BCHClassFour.lieHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.lieHom

/-- info: 'QSearch.BCHClassFour.lieHom_apply' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.lieHom_apply

/-- info: 'QSearch.BCHClassFour.lieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.lieEquiv

/-- info: 'QSearch.BCHClassFour.lieEquiv_apply' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.lieEquiv_apply

/-- info: 'QSearch.BCHClassFour.lieHom_id' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.lieHom_id

/-- info: 'QSearch.BCHClassFour.lieHom_comp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.lieHom_comp

/-- info: 'QSearch.BCHClassFour.lieEquiv_symm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.lieEquiv_symm

/-! ## Class-four subgroups are Lie subalgebras (2026-11-02) -/

/-- info: 'QSearch.BCHClassFourSubgroups.quad_central' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.quad_central

/-- info: 'QSearch.BCHClassFourSubgroups.commPoly' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.commPoly

/-- info: 'QSearch.BCHClassFourSubgroups.bch_conjugate' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.bch_conjugate

/-- info: 'QSearch.BCHClassFourSubgroups.bch_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.bch_comm

/-- info: 'QSearch.BCHClassFourSubgroups.commPoly_left' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.commPoly_left

/-- info: 'QSearch.BCHClassFourSubgroups.commPoly_right' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.commPoly_right

/-- info: 'QSearch.BCHClassFourSubgroups.commPoly_deg_three' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.commPoly_deg_three

/-- info: 'QSearch.BCHClassFourSubgroups.commPoly_deg_four' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.commPoly_deg_four

/-- info: 'QSearch.BCHClassFourSubgroups.commPoly_left_left' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.commPoly_left_left

/-- info: 'QSearch.BCHClassFourSubgroups.commPoly_right_left' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.commPoly_right_left

/-- info: 'QSearch.BCHClassFourSubgroups.commPoly_right_right' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.commPoly_right_right

/-- info: 'QSearch.BCHClassFourSubgroups.bch_cancel_bracket' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.bch_cancel_bracket

/-- info: 'QSearch.BCHClassFourSubgroups.bch_cancel_cubic' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.bch_cancel_cubic

/-- info: 'QSearch.BCHClassFourSubgroups.comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.comm

/-- info: 'QSearch.BCHClassFourSubgroups.comm_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.comm_mem

/-- info: 'QSearch.BCHClassFourSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_comm

/-- info: 'QSearch.BCHClassFourSubgroups.val_comm_left' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_comm_left

/-- info: 'QSearch.BCHClassFourSubgroups.val_comm_right' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_comm_right

/-- info: 'QSearch.BCHClassFourSubgroups.val_comm_left_left' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_comm_left_left

/-- info: 'QSearch.BCHClassFourSubgroups.val_comm_right_left' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_comm_right_left

/-- info: 'QSearch.BCHClassFourSubgroups.val_comm_right_right' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_comm_right_right

/-- info: 'QSearch.BCHClassFourSubgroups.neZeroTwo' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.neZeroTwo

/-- info: 'QSearch.BCHClassFourSubgroups.neZeroThree' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.neZeroThree

/-- info: 'QSearch.BCHClassFourSubgroups.powerScalar' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.powerScalar

/-- info: 'QSearch.BCHClassFourSubgroups.val_powerScalar' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_powerScalar

/-- info: 'QSearch.BCHClassFourSubgroups.powerScalar_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.powerScalar_mem

/-- info: 'QSearch.BCHClassFourSubgroups.bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.bracketWord

/-- info: 'QSearch.BCHClassFourSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassFourSubgroups.bracketWord_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.bracketWord_mem

/-- info: 'QSearch.BCHClassFourSubgroups.addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.addWord

/-- info: 'QSearch.BCHClassFourSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_addWord

/-- info: 'QSearch.BCHClassFourSubgroups.addWord_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.addWord_mem

/-- info: 'QSearch.BCHClassFourSubgroups.mk_smul_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.mk_smul_mem

/-- info: 'QSearch.BCHClassFourSubgroups.mk_lie_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.mk_lie_mem

/-- info: 'QSearch.BCHClassFourSubgroups.mk_add_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.mk_add_mem

/-- info: 'QSearch.BCHClassFourSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassFourSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassFourSubgroups.val_mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassFourSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassFourSubgroups.mem_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.mem_toSubgroup

/-- info: 'QSearch.BCHClassFourSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassFourSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.toSubgroup_toLieSubalgebra

/-! ## General-law hypotheses discharged at class four (2026-11-02) -/

/-- info: 'QSearch.ReesGeneralLawClassFour.bchLaw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.bchLaw

/-- info: 'QSearch.ReesGeneralLawClassFour.bchLaw_additive' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.bchLaw_additive

/-- info: 'QSearch.ReesGeneralLawClassFour.toBCH' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.toBCH

/-- info: 'QSearch.ReesGeneralLawClassFour.bchLaw_subgroups' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.bchLaw_subgroups

/-- info: 'QSearch.ReesGeneralLawClassFour.classFour_tuple_hides_arbitrary_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.classFour_tuple_hides_arbitrary_subgroup

/-- info: 'QSearch.ReesGeneralLawClassFour.canonicalPoints' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.canonicalPoints

/-- info: 'QSearch.ReesGeneralLawClassFour.canonicalPoints_isUnit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.canonicalPoints_isUnit

/-- info: 'QSearch.ReesGeneralLawClassFour.classFour_tuple_hides_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.classFour_tuple_hides_coeff

/-- info: 'QSearch.ReesGeneralLawClassFour.classFour_step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.classFour_step_output

/-- info: 'QSearch.ReesGeneralLawClassFour.classFour_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.classFour_terminal_source

/-! ## General-class measured receiver composed over all stages (2026-11-02) -/

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.convertStep' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.convertStep

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.measuredPacket' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.measuredPacket

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.measured_packet_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.measured_packet_eq

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.measured_step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.measured_step_output

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.averaged_step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.averaged_step_output

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.convert_step_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.convert_step_source

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.descend' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.descend

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.descend_top' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.descend_top

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.descend_step' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.descend_step

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.descend_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.descend_source

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.measured_terminal_source

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.classFour_measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.classFour_measured_terminal_source

/-! ## Rees SDE solvers: Chevalley–Warning witness, triangular solver, gcd reduction (2026-11-03) -/

/-- info: 'QSearch.ReesSdeGcd.pow_bezout_exponent' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeGcd.pow_bezout_exponent

/-- info: 'QSearch.ReesSdeGcd.range_pow_units_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeGcd.range_pow_units_eq

/-- info: 'QSearch.ReesSdeGcd.bezout_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeGcd.bezout_witness

/-- info: 'QSearch.ReesSdeWitness.coordPoly_totalDegree_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeWitness.coordPoly_totalDegree_le

/-- info: 'QSearch.ReesSdeWitness.eval_coordPoly' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeWitness.eval_coordPoly

/-- info: 'QSearch.ReesSdeWitness.exists_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeWitness.exists_witness

/-- info: 'QSearch.ReesSdeWitness.exists_witness_zmod' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeWitness.exists_witness_zmod

/-- info: 'QSearch.ReesSdeWitness.exists_witness_gcd' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeWitness.exists_witness_gcd

/-- info: 'QSearch.ReesSdeWitness.exists_witness_linear' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeWitness.exists_witness_linear

/-- info: 'QSearch.ReesSdeTriangular.realized_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.realized_zero

/-- info: 'QSearch.ReesSdeTriangular.realized_mono' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.realized_mono

/-- info: 'QSearch.ReesSdeTriangular.add_mem_of_disjoint' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.add_mem_of_disjoint

/-- info: 'QSearch.ReesSdeTriangular.realized_add' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.realized_add

/-- info: 'QSearch.ReesSdeTriangular.roundWeight_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.roundWeight_mem

/-- info: 'QSearch.ReesSdeTriangular.roundWeight_support' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.roundWeight_support

/-- info: 'QSearch.ReesSdeTriangular.roundWeight_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.roundWeight_sum

/-- info: 'QSearch.ReesSdeTriangular.exists_dependence' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.exists_dependence

/-- info: 'QSearch.ReesSdeTriangular.realized_extend' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.realized_extend

/-- info: 'QSearch.ReesSdeTriangular.stop_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.stop_witness

/-- info: 'QSearch.ReesSdeTriangular.witness_aux' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.witness_aux

/-- info: 'QSearch.ReesSdeTriangular.triangular_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.triangular_witness

/-- info: 'QSearch.ReesSdeTriangular.two_mul_triangle' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.two_mul_triangle

/-- info: 'QSearch.ReesSdeTriangular.triangular_sde_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.triangular_sde_witness

/-- info: 'QSearch.ReesSdeTriangular.coset_product' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.coset_product

/-- info: 'QSearch.ReesSdeTriangular.exists_coset_index' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.exists_coset_index

/-- info: 'QSearch.ReesSdeTriangular.exists_generator' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.exists_generator

/-- info: 'QSearch.ReesSdeTriangular.triangular_sde_of_contraction' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.triangular_sde_of_contraction

/-- info: 'QSearch.ReesSdeTriangular.triangular_sde_zmod' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.triangular_sde_zmod

/-- info: 'QSearch.ReesSdeTriangular.contraction_three' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.contraction_three

/-- info: 'QSearch.ReesSdeTriangular.generator_three' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.generator_three

/-- info: 'QSearch.ReesSdeTriangular.triangular_sde_three' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeTriangular.triangular_sde_three

/-! ## Class-five BCH group (2026-11-04) -/

/-- info: 'QSearch.BCHClassFive.classFive_of_lowerCentralSeries' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.classFive_of_lowerCentralSeries

/-- info: 'QSearch.BCHClassFive.bch_assoc_of_classFive' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.bch_assoc_of_classFive

/-- info: 'QSearch.BCHClassFive.bch_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.bch_assoc

/-- info: 'QSearch.BCHClassFive.instGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.instGroup

/-- info: 'QSearch.BCHClassFive.val_mul_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.val_mul_formula

/-- info: 'QSearch.BCHClassFive.lieHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.lieHom

/-- info: 'QSearch.BCHClassFive.lieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.lieEquiv

/-- info: 'QSearch.BCHClassFive.val_zpow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.val_zpow

/-- info: 'QSearch.BCHClassFiveSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.val_comm

/-- info: 'QSearch.BCHClassFiveSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassFiveSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.val_addWord

/-- info: 'QSearch.BCHClassFiveSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassFiveSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassFiveSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassFiveSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassFiveSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.toSubgroup_toLieSubalgebra

/-- info: 'QSearch.ReesGeneralLawClassFive.bchLaw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.bchLaw

/-- info: 'QSearch.ReesGeneralLawClassFive.bchLaw_subgroups' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.bchLaw_subgroups

/-- info: 'QSearch.ReesGeneralLawClassFive.classFive_tuple_hides_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.classFive_tuple_hides_coeff

/-- info: 'QSearch.ReesGeneralLawClassFive.classFive_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.classFive_terminal_source

/-- info: 'QSearch.ReesGeneralLawClassFive.classFive_measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.classFive_measured_terminal_source

/-! ## Class-six BCH group (2026-11-05) -/

/-- info: 'QSearch.BCHClassSix.classSix_of_lowerCentralSeries' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSix.classSix_of_lowerCentralSeries

/-- info: 'QSearch.BCHClassSix.bch_assoc_of_classSix' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSix.bch_assoc_of_classSix

/-- info: 'QSearch.BCHClassSix.bch_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSix.bch_assoc

/-- info: 'QSearch.BCHClassSix.instGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSix.instGroup

/-- info: 'QSearch.BCHClassSix.val_mul_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSix.val_mul_formula

/-- info: 'QSearch.BCHClassSix.lieHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSix.lieHom

/-- info: 'QSearch.BCHClassSix.lieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSix.lieEquiv

/-- info: 'QSearch.BCHClassSix.val_zpow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSix.val_zpow

/-- info: 'QSearch.BCHClassSixSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.val_comm

/-- info: 'QSearch.BCHClassSixSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassSixSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.val_addWord

/-- info: 'QSearch.BCHClassSixSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassSixSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassSixSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassSixSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassSixSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.toSubgroup_toLieSubalgebra

/-- info: 'QSearch.ReesGeneralLawClassSix.bchLaw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSix.bchLaw

/-- info: 'QSearch.ReesGeneralLawClassSix.bchLaw_subgroups' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSix.bchLaw_subgroups

/-- info: 'QSearch.ReesGeneralLawClassSix.classSix_tuple_hides_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSix.classSix_tuple_hides_coeff

/-- info: 'QSearch.ReesGeneralLawClassSix.classSix_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSix.classSix_terminal_source

/-- info: 'QSearch.ReesGeneralLawClassSix.classSix_measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSix.classSix_measured_terminal_source

/-! ## Class-seven BCH group (2026-11-05) -/

/-- info: 'QSearch.BCHClassSeven.classSeven_of_lowerCentralSeries' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.classSeven_of_lowerCentralSeries

/-- info: 'QSearch.BCHClassSeven.bch_assoc_of_classSeven' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.bch_assoc_of_classSeven

/-- info: 'QSearch.BCHClassSeven.bch_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.bch_assoc

/-- info: 'QSearch.BCHClassSeven.instGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.instGroup

/-- info: 'QSearch.BCHClassSeven.val_mul_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.val_mul_formula

/-- info: 'QSearch.BCHClassSeven.lieHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.lieHom

/-- info: 'QSearch.BCHClassSeven.lieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.lieEquiv

/-- info: 'QSearch.BCHClassSeven.val_zpow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.val_zpow

/-- info: 'QSearch.BCHClassSevenSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.val_comm

/-- info: 'QSearch.BCHClassSevenSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassSevenSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.val_addWord

/-- info: 'QSearch.BCHClassSevenSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassSevenSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassSevenSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassSevenSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassSevenSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.toSubgroup_toLieSubalgebra

/-- info: 'QSearch.ReesGeneralLawClassSeven.bchLaw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSeven.bchLaw

/-- info: 'QSearch.ReesGeneralLawClassSeven.bchLaw_subgroups' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSeven.bchLaw_subgroups

/-- info: 'QSearch.ReesGeneralLawClassSeven.classSeven_tuple_hides_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSeven.classSeven_tuple_hides_coeff

/-- info: 'QSearch.ReesGeneralLawClassSeven.classSeven_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSeven.classSeven_terminal_source

/-- info: 'QSearch.ReesGeneralLawClassSeven.classSeven_measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassSeven.classSeven_measured_terminal_source

/-! ## Rees SDE at kappa = 2 and Chevalley-Warning receiver policies (2026-11-05) -/

/-- info: 'QSearch.ReesSdeQuadratic.nonsquare_mul_nonsquare' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.nonsquare_mul_nonsquare

/-- info: 'QSearch.ReesSdeQuadratic.exists_consecutive_nonsquare' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.exists_consecutive_nonsquare

/-- info: 'QSearch.ReesSdeQuadratic.exists_quadratic_contraction' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.exists_quadratic_contraction

/-- info: 'QSearch.ReesSdeQuadratic.contraction_two' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.contraction_two

/-- info: 'QSearch.ReesSdeQuadratic.triangular_sde_quadratic' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.triangular_sde_quadratic

/-- info: 'QSearch.ReesSdeQuadratic.triangular_sde_gcd_two' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.triangular_sde_gcd_two

/-- info: 'QSearch.ReesSdePolicy.exists_witness_module' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.exists_witness_module

/-- info: 'QSearch.ReesSdePolicy.exists_witness_module_gcd' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.exists_witness_module_gcd

/-- info: 'QSearch.ReesSdePolicy.cwPolicy_active' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.cwPolicy_active

/-- info: 'QSearch.ReesSdePolicy.cwPolicy_sde' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.cwPolicy_sde

/-- info: 'QSearch.ReesSdePolicy.measured_terminal_source_cw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.measured_terminal_source_cw

/-- info: 'QSearch.ReesSdePolicy.classSix_measured_terminal_source_cw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.classSix_measured_terminal_source_cw

/-- info: 'QSearch.ReesSdeSolver.kernelVec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.kernelVec

/-- info: 'QSearch.ReesSdeSolver.solveVec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.solveVec

/-- info: 'QSearch.ReesSdeSolver.triSolve' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.triSolve

/-- info: 'QSearch.ReesSdeSolver.quadSolveZMod' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveZMod

/-- info: 'QSearch.ReesSdeSolver.linSolve' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.linSolve

/-- info: 'QSearch.ReesSdeSolver.cwSearch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch

/-- info: 'QSearch.ReesSdeSolver.kernelVec_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.kernelVec_spec

/-- info: 'QSearch.ReesSdeSolver.solveVec_some' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.solveVec_some

/-- info: 'QSearch.ReesSdeSolver.solveVec_none' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.solveVec_none

/-- info: 'QSearch.ReesSdeSolver.triRound_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.triRound_spec

/-- info: 'QSearch.ReesSdeSolver.triSolve_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.triSolve_spec

/-- info: 'QSearch.ReesSdeSolver.contraction_of_index' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.contraction_of_index

/-- info: 'QSearch.ReesSdeSolver.pow_bezoutExp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.pow_bezoutExp

/-- info: 'QSearch.ReesSdeSolver.linSolve_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.linSolve_spec

/-- info: 'QSearch.ReesSdeSolver.linSolve_zmod_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.linSolve_zmod_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolve_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolve_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolveExp_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveExp_spec

/-- info: 'QSearch.ReesSdeSolver.findMu_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.findMu_spec

/-- info: 'QSearch.ReesSdeSolver.findMu_contraction' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.findMu_contraction

/-- info: 'QSearch.ReesSdeSolver.quadSolveZMod_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveZMod_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolveZModExp_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveZModExp_spec

/-- info: 'QSearch.ReesSdeSolver.cwSearch_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch_spec

/-- info: 'QSearch.ReesSdeSolver.cwSearch_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch_witness

/-- info: 'QSearch.ReesSdeSolver.cwSearch_zmod_gcd' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch_zmod_gcd

/-- info: 'QSearch.ReesMergeReduction.witness_coords' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMergeReduction.witness_coords

/-- info: 'QSearch.ReesMergeReduction.exponent_cancels' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMergeReduction.exponent_cancels

/-- info: 'QSearch.ReesMergeReduction.merge_product_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMergeReduction.merge_product_eq

/-- info: 'QSearch.ReesMergeReduction.merge_product_eq_of_labels' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMergeReduction.merge_product_eq_of_labels

/-- info: 'QSearch.ReesMergeReduction.zero_product_indicator' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMergeReduction.zero_product_indicator

/-- info: 'QSearch.ReesS2Local.hasContraction_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.hasContraction_iff

/-- info: 'QSearch.ReesS2Local.two_rows_diff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.two_rows_diff

/-- info: 'QSearch.ReesS2Local.beta_injective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.beta_injective

/-- info: 'QSearch.ReesS2Local.alpha_injective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.alpha_injective

/-- info: 'QSearch.ReesS2Local.exists_A_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.exists_A_witness

/-- info: 'QSearch.ReesS2Local.mem_E2_of_A_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.mem_E2_of_A_eq_zero

/-- info: 'QSearch.ReesS2Local.hasContraction_transfer' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.hasContraction_transfer

/-- info: 'QSearch.ReesS2Local.mem_E2_iff_exists' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.mem_E2_iff_exists

/-- info: 'QSearch.ReesS2Local.card_pairs_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.card_pairs_le

/-- info: 'QSearch.ReesS2Local.mem_E2_of_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.mem_E2_of_le

/-- info: 'QSearch.ReesS2Local.mem_E2_of_dvd' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.mem_E2_of_dvd

/-- info: 'QSearch.ReesS2Local.thirteen_mem_E2_four' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.thirteen_mem_E2_four

/-- info: 'QSearch.ReesS2Local.twentynine_mem_E2_four' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.twentynine_mem_E2_four

/-- info: 'QSearch.ReesS2Local.seven_not_mem_E2_three' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesS2Local.seven_not_mem_E2_three

/-! ## Dixmier–Lister central scalars and the unitriangular exp/log condition (2026-11-09) -/

/-- info: 'QSearch.DixmierLister.table' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.table

/-- info: 'QSearch.DixmierLister.table_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.table_zero

/-- info: 'QSearch.DixmierLister.mem_center_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.mem_center_iff

/-- info: 'QSearch.DixmierLister.signEquiv_center' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.signEquiv_center

/-- info: 'QSearch.DixmierLister.core_alg' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.core_alg

/-- info: 'QSearch.DixmierLister.scalar_core' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.scalar_core

/-- info: 'QSearch.DixmierLister.exists_aut_center_smul_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.exists_aut_center_smul_iff

/-- info: 'QSearch.DixmierLister.lcs_three_eq_bot' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.lcs_three_eq_bot

/-- info: 'QSearch.DixmierLister.toLieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.toLieEquiv

/-- info: 'QSearch.DixmierLister.mem_center_iff_val' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.mem_center_iff_val

/-- info: 'QSearch.DixmierLister.group_center_pow_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.group_center_pow_iff

/-- info: 'QSearch.DixmierLister.group_center_zpow_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.DixmierLister.group_center_zpow_iff

/-- info: 'QSearch.UnitriangularExpLog.natCast_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.natCast_ne_zero

/-- info: 'QSearch.UnitriangularExpLog.factorial_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.factorial_ne_zero

/-- info: 'QSearch.UnitriangularExpLog.exp_log_congr' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.exp_log_congr

/-- info: 'QSearch.UnitriangularExpLog.log_exp_congr' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.log_exp_congr

/-- info: 'QSearch.UnitriangularExpLog.texp_tlog' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.texp_tlog

/-- info: 'QSearch.UnitriangularExpLog.tlog_texp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.tlog_texp

/-- info: 'QSearch.UnitriangularExpLog.expEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.expEquiv

/-- info: 'QSearch.UnitriangularExpLog.pow_eq_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.pow_eq_one

/-- info: 'QSearch.UnitriangularExpLog.matrix_group_condition' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.matrix_group_condition

/-- info: 'QSearch.UnitriangularExpLog.strictUpper_prod_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.strictUpper_prod_eq_zero

/-- info: 'QSearch.UnitriangularExpLog.unitriangular_condition' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.UnitriangularExpLog.unitriangular_condition
