import sys

from wire_generic_batch import wire_batch

BATCH_14_MODULES = [
    (
        "self_dual_wreath_high_codimension_face_word_frontier",
        "EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER",
        "write_high_codimension_face_word_frontier_report",
        "code-wreath-high-codimension-face-word-frontier",
    ),
    (
        "self_dual_wreath_periodic_frame_rank_collapse",
        "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-RANK-COLLAPSE",
        "write_periodic_frame_rank_collapse_report",
        "code-wreath-periodic-frame-rank-collapse",
    ),
    (
        "self_dual_wreath_petz_pgm_obstruction",
        "EXP-CODE-SELF-DUAL-WREATH-PETZ-PGM-OBSTRUCTION",
        "write_petz_pgm_obstruction_report",
        "code-wreath-petz-pgm-obstruction",
    ),
    (
        "self_dual_wreath_pgm_quantum_sampling_reduction",
        "EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION",
        "write_pgm_quantum_sampling_reduction_report",
        "code-wreath-pgm-quantum-sampling-reduction",
    ),
    (
        "self_dual_wreath_pgm_spectral_window",
        "EXP-CODE-SELF-DUAL-WREATH-PGM-SPECTRAL-WINDOW",
        "write_pgm_spectral_window_report",
        "code-wreath-pgm-spectral-window",
    ),
    (
        "self_dual_wreath_pgm_success_theorem",
        "EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM",
        "write_pgm_success_theorem_report",
        "code-wreath-pgm-success-theorem",
    ),
    (
        "self_dual_wreath_pgm_truncation_robustness",
        "EXP-CODE-SELF-DUAL-WREATH-PGM-TRUNCATION-ROBUSTNESS",
        "write_pgm_truncation_robustness_report",
        "code-wreath-pgm-truncation-robustness",
    ),
    (
        "self_dual_wreath_physical_orientation_interference",
        "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-INTERFERENCE",
        "write_physical_orientation_interference_report",
        "code-wreath-physical-orientation-interference",
    ),
    (
        "self_dual_wreath_physical_pgm_intertwiner",
        "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-PGM-INTERTWINER",
        "write_physical_pgm_intertwiner_report",
        "code-wreath-physical-pgm-intertwiner",
    ),
    (
        "self_dual_wreath_plancherel_kronecker_positivity",
        "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-KRONECKER-POSITIVITY",
        "write_plancherel_kronecker_positivity_report",
        "code-wreath-plancherel-kronecker-positivity",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_14_MODULES)
