import sys

from wire_generic_batch import wire_batch

BATCH_7_MODULES = [
    (
        "self_dual_wreath_component_defect_rank_mass",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS",
        "write_component_defect_rank_mass_report",
        "code-wreath-component-defect-rank-mass",
    ),
    (
        "self_dual_wreath_component_effect_algebra_boundary",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY",
        "write_component_effect_algebra_boundary_report",
        "code-wreath-component-effect-algebra-boundary",
    ),
    (
        "self_dual_wreath_component_povm_spectral_trim",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM",
        "write_component_povm_spectral_trim_report",
        "code-wreath-component-povm-spectral-trim",
    ),
    (
        "self_dual_wreath_final_root_natural_common_span",
        "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN",
        "write_final_root_natural_common_span_report",
        "code-wreath-final-root-natural-common-span",
    ),
    (
        "self_dual_wreath_fixed_family_common_rank_dilution",
        "EXP-CODE-SELF-DUAL-WREATH-FIXED-FAMILY-COMMON-RANK-DILUTION",
        "write_fixed_family_common_rank_dilution_report",
        "code-wreath-fixed-family-common-rank-dilution",
    ),
    (
        "self_dual_wreath_global_carrier_channel_extractor",
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-CARRIER-CHANNEL-EXTRACTOR",
        "write_global_carrier_channel_extractor_report",
        "code-wreath-global-carrier-channel-extractor",
    ),
    (
        "self_dual_wreath_global_collision_free_mass",
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-COLLISION-FREE-MASS",
        "write_global_collision_free_mass_report",
        "code-wreath-global-collision-free-mass",
    ),
    (
        "self_dual_wreath_global_distinct_joint_kernel",
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-DISTINCT-JOINT-KERNEL",
        "write_global_distinct_joint_kernel_report",
        "code-wreath-global-distinct-joint-kernel",
    ),
    (
        "self_dual_wreath_global_partition_collision",
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION",
        "write_global_partition_collision_report",
        "code-wreath-global-partition-collision",
    ),
    (
        "self_dual_wreath_gpe_holonomy_resolver_reduction",
        "EXP-CODE-SELF-DUAL-WREATH-GPE-HOLONOMY-RESOLVER-REDUCTION",
        "write_gpe_holonomy_resolver_reduction_report",
        "code-wreath-gpe-holonomy-resolver-reduction",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_7_MODULES)
