import Formal.Schedule1HPlus.Guards
import Formal.Schedule1HPlus.SecondMoment

/-!
# Schedule 1H⁺: axiom audit

Each theorem below is checked to depend only on `propext`, `Classical.choice` and
`Quot.sound` (or fewer); a `sorry` would add `sorryAx`, and `native_decide` would add
`Lean.ofReduceBool`, and either would fail the `#guard_msgs` check. The `decide` guards
(`tl6_229`, `tl6_229_perturbed`, `tl3_7`, `orderOf_g229`, `orderOf_g7`) are among them.
-/

/-- info: 'QSearch.Schedule1HPlus.ClassMap.mem_coset' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.ClassMap.mem_coset

/-- info: 'QSearch.Schedule1HPlus.ClassMap.cl_unique' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.ClassMap.cl_unique

/-- info: 'QSearch.Schedule1HPlus.ClassMap.mem_lift_iff' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.ClassMap.mem_lift_iff

/-- info: 'QSearch.Schedule1HPlus.ClassMap.cl_eq_zero_iff_pow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.ClassMap.cl_eq_zero_iff_pow

/-- info: 'QSearch.Schedule1HPlus.ClassMap.gen_of_orderOf' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.ClassMap.gen_of_orderOf

/-- info: 'QSearch.Schedule1HPlus.ClassMap.ofGen' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.ClassMap.ofGen

/-- info: 'QSearch.Schedule1HPlus.depOf_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.depOf_spec

/-- info: 'QSearch.Schedule1HPlus.normalize_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.normalize_spec

/-- info: 'QSearch.Schedule1HPlus.gauss_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.gauss_spec

/-- info: 'QSearch.Schedule1HPlus.sum_Uvec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.sum_Uvec

/-- info: 'QSearch.Schedule1HPlus.refine_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.refine_spec

/-- info: 'QSearch.Schedule1HPlus.chain_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.chain_spec

/-- info: 'QSearch.Schedule1HPlus.card_chainIdx' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.card_chainIdx

/-- info: 'QSearch.Schedule1HPlus.card_chainIdx_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.card_chainIdx_le

/-- info: 'QSearch.Schedule1HPlus.rootSol_of_rel' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.rootSol_of_rel

/-- info: 'QSearch.Schedule1HPlus.rel_of_rootSol' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.rel_of_rootSol

/-- info: 'QSearch.Schedule1HPlus.rel_of_rootSol'' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.rel_of_rootSol'

/-- info: 'QSearch.Schedule1HPlus.mem_lift_zero_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.mem_lift_zero_iff

/-- info: 'QSearch.Schedule1HPlus.plusStage_stepSpec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.plusStage_stepSpec

/-- info: 'QSearch.Schedule1HPlus.plusStage_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.plusStage_spec

/-- info: 'QSearch.Schedule1HPlus.plusFinish_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.plusFinish_spec

/-- info: 'QSearch.Schedule1HPlus.plusPlanF0_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.plusPlanF0_spec

/-- info: 'QSearch.Schedule1HPlus.plusPlanFK_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.plusPlanFK_spec

/-- info: 'QSearch.Schedule1HPlus.axisRel_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.axisRel_sum

/-- info: 'QSearch.Schedule1HPlus.axisRel_map' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.axisRel_map

/-- info: 'QSearch.Schedule1HPlus.axis_zero_of_nz' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.axis_zero_of_nz

/-- info: 'QSearch.Schedule1HPlus.card_tIdx' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.card_tIdx

/-- info: 'QSearch.Schedule1HPlus.card_tIdx_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.card_tIdx_le

/-- info: 'QSearch.Schedule1HPlus.tensorStep_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.tensorStep_spec

/-- info: 'QSearch.Schedule1HPlus.tensor_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.tensor_spec

/-- info: 'QSearch.Schedule1HPlus.ellNode_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.ellNode_spec

/-- info: 'QSearch.Schedule1HPlus.ellSolver_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.ellSolver_spec

/-- info: 'QSearch.Schedule1HPlus.sum_cnt' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.sum_cnt

/-- info: 'QSearch.Schedule1HPlus.sum_cnt_sq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.sum_cnt_sq

/-- info: 'QSearch.Schedule1HPlus.sum_cnt_sq_le' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.sum_cnt_sq_le

/-- info: 'QSearch.Schedule1HPlus.card_ne_zero_ge' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.card_ne_zero_ge

/-- info: 'QSearch.Schedule1HPlus.real_step' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.real_step

/-- info: 'QSearch.Schedule1HPlus.good_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.good_one

/-- info: 'QSearch.Schedule1HPlus.good_count' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.good_count

/-- info: 'QSearch.Schedule1HPlus.rc_of_good' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.rc_of_good

/-- info: 'QSearch.Schedule1HPlus.plus_sm_i' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.plus_sm_i

/-- info: 'QSearch.Schedule1HPlus.isRC_zero_iff_check' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.isRC_zero_iff_check

/-- info: 'QSearch.Schedule1HPlus.orderOf_g229' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.orderOf_g229

/-- info: 'QSearch.Schedule1HPlus.tl6_229' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.tl6_229

/-- info: 'QSearch.Schedule1HPlus.tl6_229_perturbed' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.tl6_229_perturbed

/-- info: 'QSearch.Schedule1HPlus.chainOK_229' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.chainOK_229

/-- info: 'QSearch.Schedule1HPlus.tl6_chain_229' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.tl6_chain_229

/-- info: 'QSearch.Schedule1HPlus.tl6_arity_229' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.tl6_arity_229

/-- info: 'QSearch.Schedule1HPlus.tl6_solver_229' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.tl6_solver_229

/-- info: 'QSearch.Schedule1HPlus.orderOf_g7' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.orderOf_g7

/-- info: 'QSearch.Schedule1HPlus.tl3_7' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.tl3_7

/-- info: 'QSearch.Schedule1HPlus.ell1_contraction' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.ell1_contraction
