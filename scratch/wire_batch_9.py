import sys

from wire_generic_batch import wire_batch

BATCH_9_MODULES = [
    (
        "self_dual_wreath_internal_closure_graded_rescue",
        "EXP-CODE-SELF-DUAL-WREATH-INTERNAL-CLOSURE-GRADED-RESCUE",
        "write_internal_closure_graded_rescue_report",
        "code-wreath-internal-closure-graded-rescue",
    ),
    (
        "self_dual_wreath_interplane_gauge_homology",
        "EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY",
        "write_interplane_gauge_homology_report",
        "code-wreath-interplane-gauge-homology",
    ),
    (
        "self_dual_wreath_invariant_projector_circuit",
        "EXP-CODE-SELF-DUAL-WREATH-INVARIANT-PROJECTOR-CIRCUIT",
        "write_invariant_projector_circuit_report",
        "code-wreath-invariant-projector-circuit",
    ),
    (
        "self_dual_wreath_isotypic_dephasing_no_go",
        "EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO",
        "write_isotypic_dephasing_no_go_report",
        "code-wreath-isotypic-dephasing-no-go",
    ),
    (
        "self_dual_wreath_leaf_whitening_commutator_no_go",
        "EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO",
        "write_leaf_whitening_commutator_no_go_report",
        "code-wreath-leaf-whitening-commutator-no-go",
    ),
    (
        "self_dual_wreath_level_three_flag_audit",
        "EXP-CODE-SELF-DUAL-WREATH-LEVEL-THREE-FLAG-AUDIT",
        "write_level_three_flag_audit_report",
        "code-wreath-level-three-flag-audit",
    ),
    (
        "self_dual_wreath_local_pair_transversality",
        "EXP-CODE-SELF-DUAL-WREATH-LOCAL-PAIR-TRANSVERSALITY",
        "write_local_pair_transversality_report",
        "code-wreath-local-pair-transversality",
    ),
    (
        "self_dual_wreath_matrix_cayley_boundary",
        "EXP-CODE-SELF-DUAL-WREATH-MATRIX-CAYLEY-BOUNDARY",
        "write_matrix_cayley_boundary",
        "code-wreath-matrix-cayley-boundary",
    ),
    (
        "self_dual_wreath_matrix_povm_recursive_compiler",
        "EXP-CODE-SELF-DUAL-WREATH-MATRIX-POVM-RECURSIVE-COMPILER",
        "write_matrix_povm_recursive_compiler_report",
        "code-wreath-matrix-povm-recursive-compiler",
    ),
    (
        "self_dual_wreath_mixed_covariant_decoder",
        "EXP-CODE-SELF-DUAL-WREATH-MIXED-COVARIANT-DECODER",
        "write_mixed_covariant_decoder_report",
        "code-wreath-mixed-covariant-decoder",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_9_MODULES)
