import sys

from wire_generic_batch import wire_batch

BATCH_8_MODULES = [
    (
        "self_dual_wreath_gpe_pair_polar_transport",
        "EXP-CODE-SELF-DUAL-WREATH-GPE-PAIR-POLAR-TRANSPORT",
        "write_gpe_pair_polar_transport_report",
        "code-wreath-gpe-pair-polar-transport",
    ),
    (
        "self_dual_wreath_gpe_recursive_node_compiler",
        "EXP-CODE-SELF-DUAL-WREATH-GPE-RECURSIVE-NODE-COMPILER",
        "write_gpe_recursive_node_compiler_report",
        "code-wreath-gpe-recursive-node-compiler",
    ),
    (
        "self_dual_wreath_graded_channel_graph_reduction",
        "EXP-CODE-SELF-DUAL-WREATH-GRADED-CHANNEL-GRAPH-REDUCTION",
        "write_graded_channel_graph_reduction_report",
        "code-wreath-graded-channel-graph-reduction",
    ),
    (
        "self_dual_wreath_graded_flat_transport_no_go",
        "EXP-CODE-SELF-DUAL-WREATH-GRADED-FLAT-TRANSPORT-NO-GO",
        "write_graded_flat_transport_no_go_report",
        "code-wreath-graded-flat-transport-no-go",
    ),
    (
        "self_dual_wreath_graded_frobenius_trim",
        "EXP-CODE-SELF-DUAL-WREATH-GRADED-FROBENIUS-TRIM",
        "write_graded_frobenius_trim_report",
        "code-wreath-graded-frobenius-trim",
    ),
    (
        "self_dual_wreath_hamming_stratum_rank_transition",
        "EXP-CODE-SELF-DUAL-WREATH-HAMMING-STRATUM-RANK-TRANSITION",
        "write_hamming_stratum_rank_transition_report",
        "code-wreath-hamming-stratum-rank-transition",
    ),
    (
        "self_dual_wreath_hierarchical_cokernel_resolution",
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION",
        "write_hierarchical_cokernel_resolution_report",
        "code-wreath-hierarchical-cokernel-resolution",
    ),
    (
        "self_dual_wreath_hierarchical_polar_tree",
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE",
        "write_hierarchical_polar_tree_report",
        "code-wreath-hierarchical-polar-tree",
    ),
    (
        "self_dual_wreath_hierarchy_low_carrier_trim",
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-LOW-CARRIER-TRIM",
        "write_hierarchy_low_carrier_trim_report",
        "code-wreath-hierarchy-low-carrier-trim",
    ),
    (
        "self_dual_wreath_hierarchy_pair_common_rank_budget",
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-PAIR-COMMON-RANK-BUDGET",
        "write_hierarchy_pair_common_rank_budget_report",
        "code-wreath-hierarchy-pair-common-rank-budget",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_8_MODULES)
