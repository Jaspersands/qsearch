import sys

from wire_generic_batch import wire_batch

BATCH_10_MODULES = [
    (
        "self_dual_wreath_common_span_component_universality_no_go",
        "EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO",
        "write_common_span_component_universality_no_go_report",
        "code-wreath-common-span-component-universality-no-go",
    ),
    (
        "self_dual_wreath_mrs_coherence_escape_criterion",
        "EXP-CODE-SELF-DUAL-WREATH-MRS-COHERENCE-ESCAPE-CRITERION",
        "write_mrs_coherence_escape_criterion_report",
        "code-wreath-mrs-coherence-escape-criterion",
    ),
    (
        "self_dual_wreath_mrs_transcript_povm_separation",
        "EXP-CODE-SELF-DUAL-WREATH-MRS-TRANSCRIPT-POVM-SEPARATION",
        "write_mrs_transcript_povm_separation_report",
        "code-wreath-mrs-transcript-povm-separation",
    ),
    (
        "self_dual_wreath_multiscale_polar_schedule",
        "EXP-CODE-SELF-DUAL-WREATH-MULTISCALE-POLAR-SCHEDULE",
        "write_multiscale_polar_schedule_report",
        "code-wreath-multiscale-polar-schedule",
    ),
    (
        "self_dual_wreath_native_frame_access_boundary",
        "EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY",
        "write_native_frame_access_boundary_report",
        "code-wreath-native-frame-access-boundary",
    ),
    (
        "self_dual_wreath_natural_leaf_commutator_mass",
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS",
        "write_natural_leaf_commutator_mass_report",
        "code-wreath-natural-leaf-commutator-mass",
    ),
    (
        "self_dual_wreath_natural_pair_carrier_law",
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-PAIR-CARRIER-LAW",
        "write_natural_pair_carrier_law_report",
        "code-wreath-natural-pair-carrier-law",
    ),
    (
        "self_dual_wreath_operator_steiner_bulk_reduction",
        "EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION",
        "write_operator_steiner_bulk_reduction_report",
        "code-wreath-operator-steiner-bulk-reduction",
    ),
    (
        "self_dual_wreath_orientation_filter_physical_access",
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FILTER-PHYSICAL-ACCESS",
        "write_orientation_filter_physical_access_report",
        "code-wreath-orientation-filter-physical-access",
    ),
    (
        "self_dual_wreath_orientation_rank_budget",
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET",
        "write_orientation_rank_budget_report",
        "code-wreath-orientation-rank-budget",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_10_MODULES)
