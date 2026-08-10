import sys

from wire_generic_batch import wire_batch

BATCH_15_MODULES = [
    (
        "self_dual_wreath_polar_factor_transfer",
        "EXP-CODE-SELF-DUAL-WREATH-POLAR-FACTOR-TRANSFER",
        "write_polar_factor_transfer_report",
        "code-wreath-polar-factor-transfer",
    ),
    (
        "self_dual_wreath_postfilter_frame_compression",
        "EXP-CODE-SELF-DUAL-WREATH-POSTFILTER-FRAME-COMPRESSION",
        "write_postfilter_frame_compression_report",
        "code-wreath-postfilter-frame-compression",
    ),
    (
        "self_dual_wreath_random_steiner_gauge_edge",
        "EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE",
        "write_random_steiner_gauge_edge_report",
        "code-wreath-random-steiner-gauge-edge",
    ),
    (
        "self_dual_wreath_reciprocal_carrier_accumulation_no_go",
        "EXP-CODE-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO",
        "write_reciprocal_carrier_accumulation_no_go_report",
        "code-wreath-reciprocal-carrier-accumulation-no-go",
    ),
    (
        "self_dual_wreath_regular_master_central_support",
        "EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-CENTRAL-SUPPORT",
        "write_regular_master_central_support_report",
        "code-wreath-regular-master-central-support",
    ),
    (
        "self_dual_wreath_relation_cokernel_transfer",
        "EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER",
        "write_relation_cokernel_transfer_report",
        "code-wreath-relation-cokernel-transfer",
    ),
    (
        "self_dual_wreath_relative_effect_intersection",
        "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION",
        "write_relative_effect_intersection_report",
        "code-wreath-relative-effect-intersection",
    ),
    (
        "self_dual_wreath_relative_surface_factorization",
        "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION",
        "write_relative_surface_factorization_report",
        "code-wreath-relative-surface-factorization",
    ),
    (
        "self_dual_wreath_residual_frobenius_typicality",
        "EXP-CODE-SELF-DUAL-WREATH-RESIDUAL-FROBENIUS-TYPICALITY",
        "write_residual_frobenius_typicality_report",
        "code-wreath-residual-frobenius-typicality",
    ),
    (
        "self_dual_wreath_sector_weight_concentration",
        "EXP-CODE-SELF-DUAL-WREATH-SECTOR-WEIGHT-CONCENTRATION",
        "write_sector_weight_concentration_report",
        "code-wreath-sector-weight-concentration",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_15_MODULES)
