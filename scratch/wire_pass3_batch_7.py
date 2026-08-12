import sys

sys.path.insert(0, "scratch")
from wire_generic_batch import wire_batch

BATCH_7_MODULES = [('self_dual_wreath_transpose_edge_admission_no_go', 'EXP-CODE-SELF-DUAL-WREATH-TRANSPOSE-EDGE-ADMISSION-NO-GO', 'write_transpose_edge_admission_no_go_report', 'self-dual-wreath-transpose-edge-admission-no-go'), ('self_dual_wreath_windowed_root_flatness_bridge', 'EXP-CODE-SELF-DUAL-WREATH-WINDOWED-ROOT-FLATNESS-BRIDGE', 'write_windowed_root_flatness_bridge_report', 'self-dual-wreath-windowed-root-flatness-bridge')]

if __name__ == "__main__":
    wire_batch(BATCH_7_MODULES)
