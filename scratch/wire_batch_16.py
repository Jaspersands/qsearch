import sys

from wire_generic_batch import wire_batch

BATCH_16_MODULES = [
    (
        "self_dual_wreath_shorted_overlap_balance",
        "EXP-CODE-SELF-DUAL-WREATH-SHORTED-OVERLAP-BALANCE",
        "write_shorted_overlap_balance_report",
        "code-wreath-shorted-overlap-balance",
    ),
    (
        "self_dual_wreath_sibling_frame_jacobi_surrogate",
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JACOBI-SURROGATE",
        "write_sibling_frame_jacobi_surrogate_report",
        "code-wreath-sibling-frame-jacobi-surrogate",
    ),
    (
        "self_dual_wreath_sibling_frame_joint_conditioning_surrogate",
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-CONDITIONING-SURROGATE",
        "write_sibling_frame_joint_conditioning_surrogate_report",
        "code-wreath-sibling-frame-joint-conditioning-surrogate",
    ),
    (
        "self_dual_wreath_sibling_frame_joint_freeness",
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-FREENESS",
        "write_sibling_frame_joint_freeness_report",
        "code-wreath-sibling-frame-joint-freeness",
    ),
    (
        "self_dual_wreath_sibling_frame_mp_moments",
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS",
        "write_sibling_frame_mp_moment_report",
        "code-wreath-sibling-frame-mp-moments",
    ),
    (
        "self_dual_wreath_sibling_word_map_normal_form",
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-WORD-MAP-NORMAL-FORM",
        "write_sibling_word_map_normal_form_report",
        "code-wreath-sibling-word-map-normal-form",
    ),
    (
        "self_dual_wreath_signed_steiner_bulk_edge",
        "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-BULK-EDGE",
        "write_signed_steiner_bulk_edge_report",
        "code-wreath-signed-steiner-bulk-edge",
    ),
    (
        "self_dual_wreath_signed_steiner_incidence_boundary",
        "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY",
        "write_signed_steiner_incidence_boundary_report",
        "code-wreath-signed-steiner-incidence-boundary",
    ),
    (
        "self_dual_wreath_signed_steiner_nullity_theorem",
        "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-NULLITY-THEOREM",
        "write_signed_steiner_nullity_theorem_report",
        "code-wreath-signed-steiner-nullity-theorem",
    ),
    (
        "self_dual_wreath_single_anchor_shorting",
        "EXP-CODE-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING",
        "write_single_anchor_shorting_report",
        "code-wreath-single-anchor-shorting",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_16_MODULES)
