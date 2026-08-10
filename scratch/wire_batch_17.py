import sys

from wire_generic_batch import wire_batch

BATCH_17_MODULES = [
    (
        "self_dual_wreath_sparse_invariant_dependency",
        "EXP-CODE-SELF-DUAL-WREATH-SPARSE-INVARIANT-DEPENDENCY",
        "write_sparse_invariant_dependency",
        "code-wreath-sparse-invariant-dependency",
    ),
    (
        "self_dual_wreath_star_channel_mass_typicality",
        "EXP-CODE-SELF-DUAL-WREATH-STAR-CHANNEL-MASS-TYPICALITY",
        "write_star_channel_mass_typicality_report",
        "code-wreath-star-channel-mass-typicality",
    ),
    (
        "self_dual_wreath_subgroup_pair_angle_no_go",
        "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PAIR-ANGLE-NO-GO",
        "write_subgroup_pair_angle_no_go_report",
        "code-wreath-subgroup-pair-angle-no-go",
    ),
    (
        "self_dual_wreath_subgroup_projection_walk",
        "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PROJECTION-WALK",
        "write_subgroup_projection_walk_report",
        "code-wreath-subgroup-projection-walk",
    ),
    (
        "self_dual_wreath_support_affine_rank_entropy",
        "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-AFFINE-RANK-ENTROPY",
        "write_support_affine_rank_entropy_report",
        "code-wreath-support-affine-rank-entropy",
    ),
    (
        "self_dual_wreath_support_difference_peeling_no_go",
        "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO",
        "write_support_difference_peeling_no_go_report",
        "code-wreath-support-difference-peeling-no-go",
    ),
    (
        "self_dual_wreath_target_survival_surface_seed",
        "EXP-CODE-SELF-DUAL-WREATH-TARGET-SURVIVAL-SURFACE-SEED",
        "write_target_survival_surface_seed_report",
        "code-wreath-target-survival-surface-seed",
    ),
    (
        "self_dual_wreath_trace_polynomial_edge_burden",
        "EXP-CODE-SELF-DUAL-WREATH-TRACE-POLYNOMIAL-EDGE-BURDEN",
        "write_trace_polynomial_edge_burden_report",
        "code-wreath-trace-polynomial-edge-burden",
    ),
    (
        "self_dual_wreath_trace_weighted_pgm_bridge",
        "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-PGM-BRIDGE",
        "write_trace_weighted_pgm_bridge_report",
        "code-wreath-trace-weighted-pgm-bridge",
    ),
    (
        "self_dual_wreath_trace_weighted_polar_truncation",
        "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-POLAR-TRUNCATION",
        "write_trace_weighted_polar_truncation_report",
        "code-wreath-trace-weighted-polar-truncation",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_17_MODULES)
