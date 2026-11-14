import Formal.Schedule1HPlusReview.Probes
import Formal.Schedule1HPlusReview.EllCheck19
import Formal.Schedule1HPlusReview.EllCheck37
import Formal.Schedule1HPlusReview.EllCheck73

/-!
# Hostile review of Schedule 1H⁺ (2026-11-14): axiom audit of the probes

Not imported by `Formal.lean`. Build the modules one at a time (each `decide +kernel` table
file peaks near 2.7 GB), then `lake build Formal.Schedule1HPlusReview.Audit`.
A `sorry` would add `sorryAx` and `native_decide` would add `Lean.ofReduceBool`; either would
fail these `#guard_msgs` checks.
-/

/-- info: 'QSearch.Schedule1HPlus.Review.ann_iff_check' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ann_iff_check

/-- info: 'QSearch.Schedule1HPlus.Review.ann_iff_fullContr' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ann_iff_fullContr

/-- info: 'QSearch.Schedule1HPlus.Review.ell3_13_4' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell3_13_4

/-- info: 'QSearch.Schedule1HPlus.Review.ell3_13_4_pert' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell3_13_4_pert

/-- info: 'QSearch.Schedule1HPlus.Review.ell3_13_4_scaled' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell3_13_4_scaled

/-- info: 'QSearch.Schedule1HPlus.Review.ell3_13_4_solver' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell3_13_4_solver

/-- info: 'QSearch.Schedule1HPlus.Review.ell_136' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell_136

/-- info: 'QSearch.Schedule1HPlus.Review.ell_136_scaled' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell_136_scaled

/-- info: 'QSearch.Schedule1HPlus.Review.ell_19' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell_19

/-- info: 'QSearch.Schedule1HPlus.Review.ell_19_scaled' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell_19_scaled

/-- info: 'QSearch.Schedule1HPlus.Review.ell_37' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell_37

/-- info: 'QSearch.Schedule1HPlus.Review.ell_37_scaled' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell_37_scaled

/-- info: 'QSearch.Schedule1HPlus.Review.ell_73' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell_73

/-- info: 'QSearch.Schedule1HPlus.Review.ell_73_scaled' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.ell_73_scaled

/-- info: 'QSearch.Schedule1HPlus.Review.cl_eq_of_xi_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.cl_eq_of_xi_eq

/-- info: 'QSearch.Schedule1HPlus.Review.xi_of_classMap7' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.xi_of_classMap7

/-- info: 'QSearch.Schedule1HPlus.Review.no_classMap_7_4' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.no_classMap_7_4

/-- info: 'QSearch.Schedule1HPlus.Review.not_isRel_class' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.not_isRel_class

/-- info: 'QSearch.Schedule1HPlus.Review.not_isRel_no_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.not_isRel_no_one

/-- info: 'QSearch.Schedule1HPlus.Review.isNode_reindex' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.isNode_reindex

/-- info: 'QSearch.Schedule1HPlus.Review.hN_trivial' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.hN_trivial

/-- info: 'QSearch.Schedule1HPlus.Review.chainOK17' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.chainOK17

/-- info: 'QSearch.Schedule1HPlus.Review.chainOK17_bad' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.chainOK17_bad

/-- info: 'QSearch.Schedule1HPlus.Review.chain17_solver' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.chain17_solver

/-- info: 'QSearch.Schedule1HPlus.Review.chain17_arity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.Schedule1HPlus.Review.chain17_arity
