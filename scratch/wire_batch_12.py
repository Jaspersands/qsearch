import sys

from wire_generic_batch import wire_batch

BATCH_12_MODULES = [
    (
        "self_dual_wreath_boolean_graph_stopping_core_pressure",
        "EXP-CODE-SELF-DUAL-WREATH-BOOLEAN-GRAPH-STOPPING-CORE-PRESSURE",
        "write_boolean_graph_stopping_core_pressure_report",
        "code-wreath-boolean-graph-stopping-core-pressure",
    ),
    (
        "self_dual_wreath_component_aggregate_frame_indeterminacy",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-AGGREGATE-FRAME-INDETERMINACY",
        "write_component_aggregate_frame_indeterminacy_report",
        "code-wreath-component-aggregate-frame-indeterminacy",
    ),
    (
        "self_dual_wreath_component_commutator_collision_free_transfer",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-COLLISION-FREE-TRANSFER",
        "write_component_commutator_collision_free_transfer_report",
        "code-wreath-component-commutator-collision-free-transfer",
    ),
    (
        "self_dual_wreath_component_commutator_haar_benchmark",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-HAAR-BENCHMARK",
        "write_component_commutator_haar_benchmark_report",
        "code-wreath-component-commutator-haar-benchmark",
    ),
    (
        "self_dual_wreath_component_commutator_trace_mass_bridge",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE",
        "write_component_commutator_trace_mass_bridge_report",
        "code-wreath-component-commutator-trace-mass-bridge",
    ),
    (
        "self_dual_wreath_component_green_ridge_stability",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-GREEN-RIDGE-STABILITY",
        "write_component_green_ridge_stability_report",
        "code-wreath-component-green-ridge-stability",
    ),
    (
        "self_dual_wreath_component_hamming_orbit_reduction",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-HAMMING-ORBIT-REDUCTION",
        "write_component_hamming_orbit_reduction_report",
        "code-wreath-component-hamming-orbit-reduction",
    ),
    (
        "self_dual_wreath_component_leaf_resolved_green_normal_form",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM",
        "write_component_leaf_resolved_green_normal_form_report",
        "code-wreath-component-leaf-resolved-green-normal-form",
    ),
    (
        "self_dual_wreath_contiguous_all_a_support_pressure",
        "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-ALL-A-SUPPORT-PRESSURE",
        "write_contiguous_all_a_support_pressure_report",
        "code-wreath-contiguous-all-a-support-pressure",
    ),
    (
        "self_dual_wreath_contiguous_frame_target_factorization",
        "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-FRAME-TARGET-FACTORIZATION",
        "write_contiguous_frame_target_factorization_report",
        "code-wreath-contiguous-frame-target-factorization",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_12_MODULES)
