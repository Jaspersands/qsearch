import Formal.ReesLeanExt.ReesGeneralLawClassThree
import Formal.ReesLeanExt.ReesGeneralReceiver

/-!
# Axiom audit for the 2026-11-02 general-class Rees extension

Every declaration in the four new modules is checked to depend only on
`propext`, `Classical.choice` and `Quot.sound`. A `sorry` would add `sorryAx`
and fail the `#guard_msgs` check, and with it the build.
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
