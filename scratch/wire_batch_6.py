import sys
from pathlib import Path

sys.path.insert(0, ".")
from scratch.wire_generic_batch import wire_batch

batch_6_info = [
    (
        "self_dual_wreath_component_defect_gap_bridge",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-GAP-BRIDGE",
        "write_component_defect_gap_bridge_report",
        "code-wreath-component-defect-gap-bridge",
    ),
    (
        "self_dual_wreath_component_povm_regular_master_reduction",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION",
        "write_component_povm_regular_master_reduction_report",
        "code-wreath-component-povm-regular-master-reduction",
    ),
    (
        "self_dual_wreath_component_povm_sparse_support_boundary",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY",
        "write_component_povm_sparse_support_boundary_report",
        "code-wreath-component-povm-sparse-support-boundary",
    ),
    (
        "self_dual_wreath_covariant_pgm_factorization",
        "EXP-CODE-SELF-DUAL-WREATH-COVARIANT-PGM-FACTORIZATION",
        "write_covariant_pgm_factorization_report",
        "code-wreath-covariant-pgm-factorization",
    ),
    (
        "self_dual_wreath_coverage_welch_pressure",
        "EXP-CODE-SELF-DUAL-WREATH-COVERAGE-WELCH-PRESSURE",
        "write_coverage_welch_pressure_report",
        "code-wreath-coverage-welch-pressure",
    ),
    (
        "self_dual_wreath_cross_dependency_neutrality",
        "EXP-CODE-SELF-DUAL-WREATH-CROSS-DEPENDENCY-NEUTRALITY",
        "write_cross_dependency_neutrality",
        "code-wreath-cross-dependency-neutrality",
    ),
    (
        "self_dual_wreath_dependency_homology",
        "EXP-CODE-SELF-DUAL-WREATH-DEPENDENCY-HOMOLOGY",
        "write_dependency_homology",
        "code-wreath-dependency-homology",
    ),
    (
        "self_dual_wreath_early_level_overlap_localization",
        "EXP-CODE-SELF-DUAL-WREATH-EARLY-LEVEL-OVERLAP-LOCALIZATION",
        "write_early_level_overlap_localization_report",
        "code-wreath-early-level-overlap-localization",
    ),
    (
        "self_dual_wreath_extended_kronecker_threshold",
        "EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD",
        "write_extended_kronecker_threshold_report",
        "code-wreath-extended-kronecker-threshold",
    ),
    (
        "self_dual_wreath_final_root_leverage_edge",
        "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-LEVERAGE-EDGE",
        "write_final_root_leverage_edge_report",
        "code-wreath-final-root-leverage-edge",
    ),
]

wire_batch(
    batch_6_info,
    last_exp_id="EXP-CODE-SELF-DUAL-WREATH-COMPLETE-S6-VERTEX-CHANNEL-AUDIT",
)
