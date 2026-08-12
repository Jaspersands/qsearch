import sys

sys.path.insert(0, "scratch")
from wire_generic_batch import wire_batch

BATCH_6_MODULES = [('self_dual_wreath_single_pair_point_signal_no_go', 'EXP-CODE-SELF-DUAL-WREATH-SINGLE-PAIR-POINT-SIGNAL-NO-GO', 'write_single_pair_point_signal_no_go_report', 'self-dual-wreath-single-pair-point-signal-no-go'), ('self_dual_wreath_sparse_polar_access_composition_no_go', 'EXP-CODE-SELF-DUAL-WREATH-SPARSE-POLAR-ACCESS-COMPOSITION-NO-GO', 'write_sparse_polar_access_composition_no_go_report', 'self-dual-wreath-sparse-polar-access-composition-no-go'), ('self_dual_wreath_sparse_support_polar_hybrid', 'EXP-CODE-SELF-DUAL-WREATH-SPARSE-SUPPORT-POLAR-HYBRID', 'write_sparse_support_polar_hybrid_report', 'self-dual-wreath-sparse-support-polar-hybrid'), ('self_dual_wreath_sparse_support_polar_schedule', 'EXP-CODE-SELF-DUAL-WREATH-SPARSE-SUPPORT-POLAR-SCHEDULE', 'write_sparse_support_polar_schedule_report', 'self-dual-wreath-sparse-support-polar-schedule'), ('self_dual_wreath_support_projector_endpoint_gauge_boundary', 'EXP-CODE-SELF-DUAL-WREATH-SUPPORT-PROJECTOR-ENDPOINT-GAUGE-BOUNDARY', 'write_support_projector_endpoint_gauge_boundary_report', 'self-dual-wreath-support-projector-endpoint-gauge-boundary'), ('self_dual_wreath_transpose_edge_admission_no_go', 'EXP-CODE-SELF-DUAL-WREATH-TRANSPOSE-EDGE-ADMISSION-NO-GO', 'write_transpose_edge_admission_no_go_report', 'self-dual-wreath-transpose-edge-admission-no-go'), ('self_dual_wreath_windowed_root_flatness_bridge', 'EXP-CODE-SELF-DUAL-WREATH-WINDOWED-ROOT-FLATNESS-BRIDGE', 'write_windowed_root_flatness_bridge_report', 'self-dual-wreath-windowed-root-flatness-bridge')]

if __name__ == "__main__":
    wire_batch(BATCH_6_MODULES)
