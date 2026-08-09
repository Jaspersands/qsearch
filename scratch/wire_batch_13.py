import sys

from wire_generic_batch import wire_batch

BATCH_13_MODULES = [
    (
        "self_dual_wreath_exceptional_block_graph_core_pressure",
        "EXP-CODE-SELF-DUAL-WREATH-EXCEPTIONAL-BLOCK-GRAPH-CORE-PRESSURE",
        "write_exceptional_block_graph_core_pressure_report",
        "code-wreath-exceptional-block-graph-core-pressure",
    ),
    (
        "self_dual_wreath_frame_subword_entropy",
        "EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY",
        "write_frame_subword_entropy_report",
        "code-wreath-frame-subword-entropy",
    ),
    (
        "self_dual_wreath_leaf_marked_green_word_normal_form",
        "EXP-CODE-SELF-DUAL-WREATH-LEAF-MARKED-GREEN-WORD-NORMAL-FORM",
        "write_leaf_marked_green_word_normal_form_report",
        "code-wreath-leaf-marked-green-word-normal-form",
    ),
    (
        "self_dual_wreath_linear_code_support_pressure",
        "EXP-CODE-SELF-DUAL-WREATH-LINEAR-CODE-SUPPORT-PRESSURE",
        "write_linear_code_support_pressure_report",
        "code-wreath-linear-code-support-pressure",
    ),
    (
        "self_dual_wreath_marked_pressure_obstruction_search",
        "EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH",
        "write_marked_pressure_obstruction_search_report",
        "code-wreath-marked-pressure-obstruction-search",
    ),
    (
        "self_dual_wreath_marked_relation_topology",
        "EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY",
        "write_marked_relation_topology_report",
        "code-wreath-marked-relation-topology",
    ),
    (
        "self_dual_wreath_mixed_split_target_genus",
        "EXP-CODE-SELF-DUAL-WREATH-MIXED-SPLIT-TARGET-GENUS",
        "write_mixed_split_target_genus_report",
        "code-wreath-mixed-split-target-genus",
    ),
    (
        "self_dual_wreath_natural_leaf_commutator_trace_profile",
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-TRACE-PROFILE",
        "write_natural_leaf_commutator_trace_profile_report",
        "code-wreath-natural-leaf-commutator-trace-profile",
    ),
    (
        "self_dual_wreath_parity_stopping_core_pressure",
        "EXP-CODE-SELF-DUAL-WREATH-PARITY-STOPPING-CORE-PRESSURE",
        "write_parity_stopping_core_pressure_report",
        "code-wreath-parity-stopping-core-pressure",
    ),
    (
        "self_dual_wreath_periodic_frame_fiber_counterfamily",
        "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-FIBER-COUNTERFAMILY",
        "write_periodic_frame_fiber_counterfamily_report",
        "code-wreath-periodic-frame-fiber-counterfamily",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_13_MODULES)
