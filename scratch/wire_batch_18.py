import sys

from wire_generic_batch import wire_batch

BATCH_18_MODULES = [
    (
        "self_dual_wreath_transport_carrier_mass",
        "EXP-CODE-SELF-DUAL-WREATH-TRANSPORT-CARRIER-MASS",
        "write_transport_carrier_mass_report",
        "code-wreath-transport-carrier-mass",
    ),
    (
        "self_dual_wreath_two_color_return_walk",
        "EXP-CODE-SELF-DUAL-WREATH-TWO-COLOR-RETURN-WALK",
        "write_two_color_return_walk_report",
        "code-wreath-two-color-return-walk",
    ),
    (
        "self_dual_wreath_two_partition_ribbon_surface",
        "EXP-CODE-SELF-DUAL-WREATH-TWO-PARTITION-RIBBON-SURFACE",
        "write_two_partition_ribbon_surface_report",
        "code-wreath-two-partition-ribbon-surface",
    ),
    (
        "self_dual_wreath_uniform_orientation_rank_concentration",
        "EXP-CODE-SELF-DUAL-WREATH-UNIFORM-ORIENTATION-RANK-CONCENTRATION",
        "write_uniform_orientation_rank_concentration_report",
        "code-wreath-uniform-orientation-rank-concentration",
    ),
    (
        "self_dual_wreath_vertex_channel_groupoid",
        "EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID",
        "write_vertex_channel_groupoid_report",
        "code-wreath-vertex-channel-groupoid",
    ),
    (
        "self_dual_wreath_vertex_kernel_graded_reduction",
        "EXP-CODE-SELF-DUAL-WREATH-VERTEX-KERNEL-GRADED-REDUCTION",
        "write_vertex_kernel_graded_reduction_report",
        "code-wreath-vertex-kernel-graded-reduction",
    ),
    (
        "self_dual_wreath_vertex_trivialization_criterion",
        "EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION",
        "write_vertex_trivialization_criterion_report",
        "code-wreath-vertex-trivialization-criterion",
    ),
    (
        "self_dual_wreath_weighted_overlap_exclusion",
        "EXP-CODE-SELF-DUAL-WREATH-WEIGHTED-OVERLAP-EXCLUSION",
        "write_weighted_overlap_exclusion",
        "code-wreath-weighted-overlap-exclusion",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_18_MODULES)
