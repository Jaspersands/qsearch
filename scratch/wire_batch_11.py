import sys

from wire_generic_batch import wire_batch

BATCH_11_MODULES = [
    (
        "self_dual_wreath_orientation_retention_theorem",
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RETENTION-THEOREM",
        "write_orientation_retention_theorem_report",
        "code-wreath-orientation-retention-theorem",
    ),
    (
        "self_dual_wreath_orientation_subspace_filter",
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SUBSPACE-FILTER",
        "write_orientation_subspace_filter_report",
        "code-wreath-orientation-subspace-filter",
    ),
    (
        "self_dual_wreath_pair_common_covering_transition",
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-COMMON-COVERING-TRANSITION",
        "write_pair_common_covering_transition_report",
        "code-wreath-pair-common-covering-transition",
    ),
    (
        "self_dual_wreath_pair_core_rank_concentration",
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RANK-CONCENTRATION",
        "write_pair_core_rank_concentration_report",
        "code-wreath-pair-core-rank-concentration",
    ),
    (
        "self_dual_wreath_pair_polar_sampler",
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-SAMPLER",
        "write_pair_polar_sampler_report",
        "code-wreath-pair-polar-sampler",
    ),
    (
        "self_dual_wreath_pair_polar_transport_network",
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK",
        "write_pair_polar_transport_network_report",
        "code-wreath-pair-polar-transport-network",
    ),
    (
        "self_dual_wreath_pair_transport_degree_obstruction",
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION",
        "write_pair_transport_degree_obstruction_report",
        "code-wreath-pair-transport-degree-obstruction",
    ),
    (
        "self_dual_wreath_pair_transport_native_mass_boundary",
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY",
        "write_pair_transport_native_mass_boundary_report",
        "code-wreath-pair-transport-native-mass-boundary",
    ),
    (
        "self_dual_wreath_partial_support_child_embedding",
        "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-CHILD-EMBEDDING",
        "write_partial_support_child_embedding_report",
        "code-wreath-partial-support-child-embedding",
    ),
    (
        "self_dual_wreath_partial_support_source_mass_boundary",
        "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-SOURCE-MASS-BOUNDARY",
        "write_partial_support_source_mass_boundary_report",
        "code-wreath-partial-support-source-mass-boundary",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_11_MODULES)
