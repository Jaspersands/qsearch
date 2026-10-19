"""Self-dual wreath product subcommands, moved out of qsearch.py by tools/split_cli/migrate.py.

Each ``add_*`` function registers one subcommand and each ``command_*`` function runs one.
A command imports what it needs from ``qsearch`` when it runs, so loading this module stays
cheap and ``monkeypatch.setattr(qsearch, name, ...)`` still reaches the command.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path



def command_sdw_branch_character_cyclic_polar_compiler(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_branch_character_cyclic_polar_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_branch_character_cyclic_polar_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_branch_character_cyclic_polar_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_cyclic_polar_compiler complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_cyclic_quadrant_overlap(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_cyclic_quadrant_overlap_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_cyclic_quadrant_overlap_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_cyclic_quadrant_overlap_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_cyclic_quadrant_overlap complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_equivariant_multiplier_normal_form(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_equivariant_multiplier_normal_form_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_equivariant_multiplier_normal_form_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_equivariant_multiplier_normal_form_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_equivariant_multiplier_normal_form complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_gpe_dilation_separation(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_gpe_dilation_separation_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_gpe_dilation_separation_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_gpe_dilation_separation_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_gpe_dilation_separation complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_label_coherent_power_map_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_label_coherent_power_map_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_label_coherent_power_map_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_label_coherent_power_map_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_label_coherent_power_map_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_naimark_autocorrelation_fourier_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_naimark_autocorrelation_fourier_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_naimark_autocorrelation_fourier_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_naimark_autocorrelation_fourier_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_naimark_autocorrelation_fourier_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_natural_frobenius_word_map(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_frobenius_word_map_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_natural_frobenius_word_map_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_natural_frobenius_word_map_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_natural_frobenius_word_map complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_polar_naimark_completion(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_branch_character_polar_naimark_completion_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_branch_character_polar_naimark_completion_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_branch_character_polar_naimark_completion_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_polar_naimark_completion complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_power_map_fourier_access_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_power_map_fourier_access_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_power_map_fourier_access_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_power_map_fourier_access_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_power_map_fourier_access_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_raw_concentration_central_fourier_bridge(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_central_raw_concentration_bridge_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_central_raw_concentration_bridge_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_central_raw_concentration_bridge_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_raw_concentration_central_fourier_bridge complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_raw_polar_matched_filter_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_raw_polar_matched_filter_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_raw_polar_matched_filter_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_raw_polar_matched_filter_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_raw_polar_matched_filter_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_sector_resolved_whitening_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sector_resolved_whitening_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_sector_resolved_whitening_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_sector_resolved_whitening_no_go_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_sector_resolved_whitening_no_go complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_branch_character_whole_sum_path_erasure_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_whole_sum_path_erasure_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_whole_sum_path_erasure_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_whole_sum_path_erasure_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_branch_character_whole_sum_path_erasure_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_joint_character_analysis_map_normalization(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_joint_analysis_map_normalization_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_joint_analysis_map_normalization_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_joint_analysis_map_normalization_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_joint_character_analysis_map_normalization complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_joint_character_natural_sector_mass(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_joint_character_natural_sector_mass_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_joint_character_natural_sector_mass_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_joint_character_natural_sector_mass_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_joint_character_natural_sector_mass complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_joint_character_purification_access_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_joint_purification_access_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_joint_purification_access_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_joint_purification_access_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_joint_character_purification_access_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_orientation_kernel_character_tensor_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_character_tensor_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_character_tensor_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_character_tensor_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_orientation_kernel_character_tensor_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_orientation_kernel_hash_normalization_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hash_normalization_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_hash_normalization_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_hash_normalization_no_go_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_orientation_kernel_hash_normalization_no_go complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_schur_branch_merger_polar_equivalence(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_schur_branch_merger_polar_equivalence_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_schur_branch_merger_polar_equivalence_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_schur_branch_merger_polar_equivalence_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_schur_branch_merger_polar_equivalence complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_schur_dilated_multiplicity_access(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_schur_dilated_multiplicity_access_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_schur_dilated_multiplicity_access_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_schur_dilated_multiplicity_access_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_schur_dilated_multiplicity_access complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_split_sector_branch_regularity(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_split_sector_branch_regularity_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_split_sector_branch_regularity_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_split_sector_branch_regularity_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_split_sector_branch_regularity complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_trace_biased_coefficient_rank_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_trace_biased_coefficient_rank_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_trace_biased_coefficient_rank_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_trace_biased_coefficient_rank_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_trace_biased_coefficient_rank_no_go complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_schur_companion_transform_scope_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_schur_companion_transform_scope_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_schur_companion_transform_scope_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_schur_companion_transform_scope_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_schur_companion_transform_scope_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_addressed_cross_map_pair_polar_gram_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_addressed_cross_map_pair_polar_gram_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_addressed_cross_map_pair_polar_gram_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_addressed_cross_map_pair_polar_gram_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_addressed_cross_map_linear_assembly_normalization_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_linear_assembly_normalization_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_linear_assembly_normalization_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_linear_assembly_normalization_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_addressed_cross_map_linear_assembly_normalization_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_natural_q_scale_spectral_window_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_q_scale_spectral_window_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_natural_q_scale_spectral_window_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_natural_q_scale_spectral_window_no_go_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_natural_q_scale_spectral_window_no_go complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_final_root_metric_access_width_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_metric_access_width_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_final_root_metric_access_width_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_final_root_metric_access_width_no_go_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_final_root_metric_access_width_no_go complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_final_root_scalar_mixer_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_scalar_mixer_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_final_root_scalar_mixer_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_final_root_scalar_mixer_no_go_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_final_root_scalar_mixer_no_go complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_final_root_byproduct_covariance_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_byproduct_covariance_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_final_root_byproduct_covariance_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_final_root_byproduct_covariance_no_go_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_final_root_byproduct_covariance_no_go complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_final_root_physical_preparation_extension_scope_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_physical_preparation_extension_scope_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_final_root_physical_preparation_extension_scope_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_final_root_physical_preparation_extension_scope_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_final_root_physical_preparation_extension_scope_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_final_root_program_contraction_normalization_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_program_contraction_normalization_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_final_root_program_contraction_normalization_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_final_root_program_contraction_normalization_no_go_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_final_root_program_contraction_normalization_no_go complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_final_root_purification_naimark_program_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_purification_naimark_program_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_final_root_purification_naimark_program_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_final_root_purification_naimark_program_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_final_root_purification_naimark_program_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_sdw_final_root_state_preparation_oracle_query_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_state_preparation_oracle_query_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_final_root_state_preparation_oracle_query_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_final_root_state_preparation_oracle_query_boundary_report()
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("self_dual_wreath_final_root_state_preparation_oracle_query_boundary complete")
    print(f"Speedup claim allowed: {payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_final_root_addressed_weyl_assembly_boundary(subparsers) -> None:
    addressed_weyl = subparsers.add_parser(
        "self-dual-wreath-final-root-addressed-weyl-assembly-boundary",
        help="Run the final-root addressed Weyl assembly and global-whitening boundary theorem.",
    )
    addressed_weyl.add_argument("--no-registry", action="store_true")
    addressed_weyl.set_defaults(
        func=command_sdw_final_root_addressed_weyl_assembly_boundary
    )


def command_sdw_final_root_addressed_weyl_assembly_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_addressed_weyl_assembly_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_final_root_addressed_weyl_assembly_boundary_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_final_root_addressed_weyl_assembly_boundary complete")
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_recursive_polar_normalization_conservation_boundary(subparsers) -> None:
    recursive_normalization = subparsers.add_parser(
        "self-dual-wreath-recursive-polar-normalization-conservation-boundary",
        help="Run the recursive polar normalization-conservation and trim-compatibility boundary theorem.",
    )
    recursive_normalization.add_argument("--no-registry", action="store_true")
    recursive_normalization.set_defaults(
        func=command_sdw_recursive_polar_normalization_conservation_boundary
    )


def command_sdw_recursive_polar_normalization_conservation_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_recursive_polar_normalization_conservation_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_recursive_polar_normalization_conservation_boundary_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_recursive_polar_normalization_conservation_boundary complete")
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_affine_gpe_nodelocal_naimark_access_boundary(subparsers) -> None:
    affine_gpe_naimark = subparsers.add_parser(
        "self-dual-wreath-affine-gpe-nodelocal-naimark-access-boundary",
        help="Run the affine/GPE scalar-SELECT versus matrix-Naimark local-router boundary theorem.",
    )
    affine_gpe_naimark.add_argument("--no-registry", action="store_true")
    affine_gpe_naimark.set_defaults(
        func=command_sdw_affine_gpe_nodelocal_naimark_access_boundary
    )


def command_sdw_affine_gpe_nodelocal_naimark_access_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_gpe_nodelocal_naimark_access_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_gpe_nodelocal_naimark_access_boundary_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_affine_gpe_nodelocal_naimark_access_boundary complete")
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_positive_naimark_access_equivalence_boundary(subparsers) -> None:
    positive_naimark = subparsers.add_parser(
        "self-dual-wreath-positive-naimark-access-equivalence-boundary",
        help="Run the positive component/endpoint Naimark access-equivalence and scalar-width boundary theorem.",
    )
    positive_naimark.add_argument("--no-registry", action="store_true")
    positive_naimark.set_defaults(
        func=command_sdw_positive_naimark_access_equivalence_boundary
    )


def command_sdw_positive_naimark_access_equivalence_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_positive_naimark_access_equivalence_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_positive_naimark_access_equivalence_boundary_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_positive_naimark_access_equivalence_boundary complete")
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_hierarchical_endpoint_schur_algebra_boundary(subparsers) -> None:
    endpoint_schur = subparsers.add_parser(
        "self-dual-wreath-hierarchical-endpoint-schur-algebra-boundary",
        help="Run the operator-valued Schur-short conditional endpoint compiler and full-algebra boundary theorem.",
    )
    endpoint_schur.add_argument("--no-registry", action="store_true")
    endpoint_schur.set_defaults(
        func=command_sdw_hierarchical_endpoint_schur_algebra_boundary
    )


def command_sdw_hierarchical_endpoint_schur_algebra_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hierarchical_endpoint_schur_algebra_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_hierarchical_endpoint_schur_algebra_boundary_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_hierarchical_endpoint_schur_algebra_boundary complete")
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_affine_flag_aggregate_schur_query_boundary(subparsers) -> None:
    affine_aggregate_schur = subparsers.add_parser(
        "self-dual-wreath-affine-flag-aggregate-schur-query-boundary",
        help="Run the affine-flag label, nested Schur-short, and addressed aggregate-query boundary theorem.",
    )
    affine_aggregate_schur.add_argument("--no-registry", action="store_true")
    affine_aggregate_schur.set_defaults(
        func=command_sdw_affine_flag_aggregate_schur_query_boundary
    )


def command_sdw_affine_flag_aggregate_schur_query_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_flag_aggregate_schur_query_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_flag_aggregate_schur_query_boundary_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_affine_flag_aggregate_schur_query_boundary complete")
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_affine_node_frame_response_boundary(subparsers) -> None:
    affine_node_response = subparsers.add_parser(
        "self-dual-wreath-affine-node-frame-response-boundary",
        help="Run the exact affine-node representation frame and separate-QSVT natural response boundary theorem.",
    )
    affine_node_response.add_argument("--no-registry", action="store_true")
    affine_node_response.set_defaults(
        func=command_sdw_affine_node_frame_response_boundary
    )


def command_sdw_affine_node_frame_response_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_node_frame_response_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_node_frame_response_boundary_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_affine_node_frame_response_boundary complete")
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_cayley_endpoint_gauge_compiler(subparsers) -> None:
    cayley_endpoint = subparsers.add_parser(
        "self-dual-wreath-cayley-endpoint-gauge-compiler",
        help="Run the scale-free Hermitian Cayley endpoint, recursive child-gauge, and root-anchor boundary theorem.",
    )
    cayley_endpoint.add_argument("--no-registry", action="store_true")
    cayley_endpoint.set_defaults(
        func=command_sdw_cayley_endpoint_gauge_compiler
    )


def command_sdw_cayley_endpoint_gauge_compiler(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_cayley_endpoint_gauge_compiler_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_cayley_endpoint_gauge_compiler_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_cayley_endpoint_gauge_compiler complete")
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_affine_star_cayley_compiler(subparsers) -> None:
    affine_star_cayley = subparsers.add_parser(
        "self-dual-wreath-affine-star-cayley-compiler",
        help="Run the normalization-one label-resolved affine-star Cayley compiler and spectrum-degree boundary.",
    )
    affine_star_cayley.add_argument("--no-registry", action="store_true")
    affine_star_cayley.set_defaults(
        func=command_sdw_affine_star_cayley_compiler
    )


def command_sdw_affine_star_cayley_compiler(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_star_cayley_compiler_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_star_cayley_compiler_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_affine_star_cayley_compiler complete")
    print(
        "Covered physical W6 channels: "
        f"{payload.get('headline_metrics', {}).get('physical_w6_compiler_covered_channel_count', 0)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_pair_carrier_label_contextuality(subparsers) -> None:
    pair_carrier_labels = subparsers.add_parser(
        "self-dual-wreath-pair-carrier-label-contextuality",
        help="Run the coherent local pair-carrier label compiler and overlapping-label contextuality boundary.",
    )
    pair_carrier_labels.add_argument("--no-registry", action="store_true")
    pair_carrier_labels.set_defaults(
        func=command_sdw_pair_carrier_label_contextuality
    )


def command_sdw_pair_carrier_label_contextuality(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_carrier_label_contextuality_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pair_carrier_label_contextuality_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_pair_carrier_label_contextuality complete")
    print(
        "Overlapping label commutator: "
        f"{payload.get('headline_metrics', {}).get('overlapping_s3_projector_commutator_norm', 0.0)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_occupied_carrier_octahedral_boundary(subparsers) -> None:
    occupied_octahedral = subparsers.add_parser(
        "self-dual-wreath-occupied-carrier-octahedral-boundary",
        help="Run the all-n occupied octahedral channel and repeated-source natural-mass boundary theorem.",
    )
    occupied_octahedral.add_argument("--no-registry", action="store_true")
    occupied_octahedral.set_defaults(
        func=command_sdw_occupied_carrier_octahedral_boundary
    )


def command_sdw_occupied_carrier_octahedral_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_occupied_carrier_octahedral_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_occupied_carrier_octahedral_boundary_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_occupied_carrier_octahedral_boundary complete")
    print(
        "Occupied support commutator: "
        f"{payload.get('headline_metrics', {}).get('occupied_support_projector_commutator_norm', 0.0)}"
    )
    print(
        "Unit-correlation minimum eigenvalue: "
        f"{payload.get('headline_metrics', {}).get('unit_correlation_minimum_eigenvalue', 0.0)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_plancherel_carrier_contextuality(subparsers) -> None:
    plancherel_carrier_contextuality = subparsers.add_parser(
        "self-dual-wreath-plancherel-carrier-contextuality",
        help="Run the exact natural overlapping-carrier contextuality reduction and weighted commuting-moment probe.",
    )
    plancherel_carrier_contextuality.add_argument(
        "--samples", type=int, default=20_000
    )
    plancherel_carrier_contextuality.add_argument(
        "--no-registry", action="store_true"
    )
    plancherel_carrier_contextuality.set_defaults(
        func=command_sdw_plancherel_carrier_contextuality
    )


def command_sdw_plancherel_carrier_contextuality(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_plancherel_carrier_contextuality_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_plancherel_carrier_contextuality_report(
        write_registry=not args.no_registry,
        sample_count=args.samples,
    )
    validation = validate_registry()
    print("self_dual_wreath_plancherel_carrier_contextuality complete")
    print(
        "Tail weighted commuting probability: "
        f"{payload.get('headline_metrics', {}).get('tail_estimated_weighted_commuting_probability', 0.0)}"
    )
    print(
        "Tail contextuality confidence lower bound: "
        f"{payload.get('headline_metrics', {}).get('tail_contextuality_confidence_lower', 0.0)}"
    )
    print(
        "Asymptotic contextuality proved: "
        f"{payload.get('claim_gate', {}).get('weighted_commuting_probability_asymptotically_vanishes_proved', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_plancherel_carrier_nonidentity_tail(subparsers) -> None:
    plancherel_carrier_tail = subparsers.add_parser(
        "self-dual-wreath-plancherel-carrier-nonidentity-tail",
        help="Run the exact centralizer cycle index and isolate the high-support character-squared commuting tail.",
    )
    plancherel_carrier_tail.add_argument(
        "--max-exact-degree", type=int, default=20, choices=range(3, 25)
    )
    plancherel_carrier_tail.add_argument("--no-registry", action="store_true")
    plancherel_carrier_tail.set_defaults(
        func=command_sdw_plancherel_carrier_nonidentity_tail
    )


def command_sdw_plancherel_carrier_nonidentity_tail(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_plancherel_carrier_nonidentity_tail_report,
    )
    initialize_seed_registry(overwrite=False)
    default_degrees = (3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20)
    exact_degrees = tuple(
        degree for degree in default_degrees if degree <= args.max_exact_degree
    )
    if args.max_exact_degree not in exact_degrees:
        exact_degrees += (args.max_exact_degree,)
    payload = write_plancherel_carrier_nonidentity_tail_report(
        write_registry=not args.no_registry,
        exact_degrees=tuple(sorted(set(exact_degrees))),
    )
    validation = validate_registry()
    print("self_dual_wreath_plancherel_carrier_nonidentity_tail complete")
    print(
        "Largest exact degree: "
        f"{payload.get('headline_metrics', {}).get('largest_exact_weighted_commuting_degree', 0)}"
    )
    print(
        "Exact conditional nonidentity commuting probability: "
        f"{payload.get('headline_metrics', {}).get('tail_exact_nonidentity_conditional_commuting_probability', 0.0)}"
    )
    print(
        "High-support tail theorem proved: "
        f"{payload.get('claim_gate', {}).get('mesoscopic_macroscopic_commuting_tail_vanishes_proved', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_plancherel_carrier_near_derangement_reduction(subparsers) -> None:
    near_derangement_reduction = subparsers.add_parser(
        "self-dual-wreath-plancherel-carrier-near-derangement-reduction",
        help="Reduce the exact Plancherel carrier tail to logarithmic-fixed-point near-derangement class pairs.",
    )
    near_derangement_reduction.add_argument(
        "--max-exact-degree", type=int, default=20, choices=range(10, 25, 2)
    )
    near_derangement_reduction.add_argument("--no-registry", action="store_true")
    near_derangement_reduction.set_defaults(
        func=command_sdw_plancherel_carrier_near_derangement_reduction
    )


def command_sdw_plancherel_carrier_near_derangement_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_plancherel_carrier_near_derangement_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    default_degrees = (10, 12, 14, 16, 18, 20)
    exact_degrees = tuple(
        degree for degree in default_degrees if degree <= args.max_exact_degree
    )
    if args.max_exact_degree not in exact_degrees:
        exact_degrees += (args.max_exact_degree,)
    payload = write_plancherel_carrier_near_derangement_reduction_report(
        write_registry=not args.no_registry,
        exact_degrees=tuple(sorted(set(exact_degrees))),
    )
    validation = validate_registry()
    print("self_dual_wreath_plancherel_carrier_near_derangement_reduction complete")
    print(
        "Largest exact near-derangement degree: "
        f"{payload.get('headline_metrics', {}).get('largest_exact_near_derangement_degree', 0)}"
    )
    print(
        "Tail log-corner contribution: "
        f"{payload.get('headline_metrics', {}).get('tail_exact_log_corner_commuting_contribution', 0.0)}"
    )
    print(
        "Logarithmic-fixed-point tail theorem proved: "
        f"{payload.get('claim_gate', {}).get('logarithmic_fixed_point_commuting_tail_vanishes_proved', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_plancherel_carrier_asymptotic_closure(subparsers) -> None:
    carrier_asymptotic_closure = subparsers.add_parser(
        "self-dual-wreath-plancherel-carrier-asymptotic-closure",
        help="Close the logarithmic-fixed-point kernel and prove the natural Plancherel carrier contextuality limit.",
    )
    carrier_asymptotic_closure.add_argument("--no-registry", action="store_true")
    carrier_asymptotic_closure.set_defaults(
        func=command_sdw_plancherel_carrier_asymptotic_closure
    )


def command_sdw_plancherel_carrier_asymptotic_closure(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_plancherel_carrier_asymptotic_closure_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_plancherel_carrier_asymptotic_closure_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("self_dual_wreath_plancherel_carrier_asymptotic_closure complete")
    print(
        "Weighted commuting probability vanishes proved: "
        f"{payload.get('claim_gate', {}).get('weighted_commuting_probability_asymptotically_vanishes_proved', False)}"
    )
    print(
        "Natural carrier contextuality limit two proved: "
        f"{payload.get('claim_gate', {}).get('natural_aggregate_carrier_contextuality_limit_two_proved', False)}"
    )
    print(
        "Structured Racah resolver compiled: "
        f"{payload.get('claim_gate', {}).get('structured_multistar_racah_resolver_compiled', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_plancherel_carrier_racah_access_boundary(subparsers) -> None:
    carrier_racah_access = subparsers.add_parser(
        "self-dual-wreath-plancherel-carrier-racah-access-boundary",
        help="Resolve the minimum active Racah block, compile the carrier disturbance test, and audit conjugation-invariant decoder failure.",
    )
    carrier_racah_access.add_argument("--no-registry", action="store_true")
    carrier_racah_access.set_defaults(
        func=command_sdw_plancherel_carrier_racah_access_boundary
    )


def command_sdw_plancherel_carrier_racah_access_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_plancherel_carrier_racah_access_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_plancherel_carrier_racah_access_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("self_dual_wreath_plancherel_carrier_racah_access_boundary complete")
    print(
        "Minimum multiplicity Racah block identified: "
        f"{payload.get('claim_gate', {}).get('minimum_multiplicity_racah_block_identified', False)}"
    )
    print(
        "Carrier disturbance accessible by pair GPE: "
        f"{payload.get('claim_gate', {}).get('carrier_contextuality_operationally_accessible_by_pair_gpe', False)}"
    )
    print(
        "Active Racah physical mass tends to one: "
        f"{payload.get('claim_gate', {}).get('active_racah_physical_mass_tends_to_one', False)}"
    )
    print(
        "Carrier-only hidden-involution decoder: "
        f"{payload.get('claim_gate', {}).get('carrier_only_protocol_can_identify_hidden_involution', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_carrier_noncentral_readout_boundary(subparsers) -> None:
    carrier_noncentral_readout = subparsers.add_parser(
        "self-dual-wreath-carrier-noncentral-readout-boundary",
        help="Audit the minimum covariant noncentral row readout after carrier measurements against product and PGM baselines.",
    )
    carrier_noncentral_readout.add_argument("--no-registry", action="store_true")
    carrier_noncentral_readout.set_defaults(
        func=command_sdw_carrier_noncentral_readout_boundary
    )


def command_sdw_carrier_noncentral_readout_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_carrier_noncentral_readout_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_carrier_noncentral_readout_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("self_dual_wreath_carrier_noncentral_readout_boundary complete")
    print(
        "Carrier transcript zero information: "
        f"{payload.get('claim_gate', {}).get('carrier_transcript_zero_hidden_information_proved', False)}"
    )
    print(
        "Minimum covariant noncentral readout compiled: "
        f"{payload.get('claim_gate', {}).get('minimum_covariant_noncentral_readout_compiled', False)}"
    )
    print(
        "Physical hidden-conditioned row signal: "
        f"{payload.get('claim_gate', {}).get('physical_hidden_conditioned_row_signal_exhibited', False)}"
    )
    print(
        "Robust product-baseline advantage: "
        f"{payload.get('claim_gate', {}).get('finite_carrier_gain_robust_to_product_baselines', False)}"
    )
    print(
        "Scalable hidden-involution decoder: "
        f"{payload.get('claim_gate', {}).get('scalable_hidden_involution_decoder_compiled', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_carrier_conditioned_pgm_boundary(subparsers) -> None:
    carrier_conditioned_pgm = subparsers.add_parser(
        "self-dual-wreath-carrier-conditioned-pgm-boundary",
        help="Factor the natural PGM over one pair-carrier flag and audit information retention, conditioning, and residual multiplicity whitening.",
    )
    carrier_conditioned_pgm.add_argument("--no-registry", action="store_true")
    carrier_conditioned_pgm.set_defaults(
        func=command_sdw_carrier_conditioned_pgm_boundary
    )


def command_sdw_carrier_conditioned_pgm_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_carrier_conditioned_pgm_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_carrier_conditioned_pgm_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("self_dual_wreath_carrier_conditioned_pgm_boundary complete")
    print(
        "Hidden-independent carrier branch law: "
        f"{payload.get('claim_gate', {}).get('carrier_branch_probability_hidden_independent', False)}"
    )
    print(
        "Finite collective gain retained: "
        f"{payload.get('claim_gate', {}).get('finite_collective_information_gain_retained', False)}"
    )
    print(
        "Average support conditioning improved: "
        f"{payload.get('claim_gate', {}).get('carrier_conditioning_improves_average_support_conditioning', False)}"
    )
    print(
        "Multiplicity whitening eliminated: "
        f"{payload.get('claim_gate', {}).get('carrier_conditioning_eliminates_multiplicity_whitening', False)}"
    )
    print(
        "Polynomial branch PGM: "
        f"{payload.get('claim_gate', {}).get('polynomial_carrier_branch_pgm_compiled', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_carrier_holevo_budget_theorem(subparsers) -> None:
    carrier_holevo_budget = subparsers.add_parser(
        "self-dual-wreath-carrier-holevo-budget-theorem",
        help="Prove the all-n log-outcome Holevo loss budget for shallow adaptive carrier hierarchies.",
    )
    carrier_holevo_budget.add_argument("--no-registry", action="store_true")
    carrier_holevo_budget.set_defaults(
        func=command_sdw_carrier_holevo_budget_theorem
    )


def command_sdw_carrier_holevo_budget_theorem(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_carrier_holevo_budget_theorem_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_carrier_holevo_budget_theorem_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("self_dual_wreath_carrier_holevo_budget_theorem complete")
    print(
        "Adaptive carrier Holevo budget proved: "
        f"{payload.get('claim_gate', {}).get('adaptive_carrier_holevo_budget_proved', False)}"
    )
    print(
        "Shallow hierarchy preserves extensive Holevo information: "
        f"{payload.get('claim_gate', {}).get('shallow_carrier_hierarchy_preserves_extensive_holevo', False)}"
    )
    print(
        "Accessible information retained: "
        f"{payload.get('claim_gate', {}).get('carrier_hierarchy_accessible_information_retained', False)}"
    )
    print(
        "Full linear-depth carrier tree certified: "
        f"{payload.get('claim_gate', {}).get('full_linear_depth_carrier_tree_certified', False)}"
    )
    print(
        "Hidden-involution decoder: "
        f"{payload.get('claim_gate', {}).get('hidden_involution_decoder_compiled', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_carrier_branch_pgm_success_certificate(subparsers) -> None:
    carrier_branch_pgm_certificate = subparsers.add_parser(
        "self-dual-wreath-carrier-branch-pgm-success-certificate",
        help="Certify carrier-branch PGM success from self-purity inflation and distinct-hypothesis collision burden.",
    )
    carrier_branch_pgm_certificate.add_argument(
        "--no-registry",
        action="store_true",
    )
    carrier_branch_pgm_certificate.set_defaults(
        func=command_sdw_carrier_branch_pgm_success_certificate
    )


def command_sdw_carrier_branch_pgm_success_certificate(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_carrier_branch_pgm_success_certificate_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_carrier_branch_pgm_success_certificate_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("self_dual_wreath_carrier_branch_pgm_success_certificate complete")
    print(
        "Carrier branch PGM success certificate: "
        f"{payload.get('claim_gate', {}).get('carrier_branch_pgm_success_certificate_proved', False)}"
    )
    print(
        "Finite accessible collective success certified: "
        f"{payload.get('claim_gate', {}).get('finite_accessible_collective_success_certified', False)}"
    )
    print(
        "Aggregate Jensen certificate: "
        f"{payload.get('claim_gate', {}).get('aggregate_jensen_success_certificate_proved', False)}"
    )
    print(
        "Operational pinching anti-locking: "
        f"{payload.get('claim_gate', {}).get('all_n_operational_pinching_anti_locking_proved', False)}"
    )
    print(
        "Natural outcome angle first moment bounded: "
        f"{payload.get('claim_gate', {}).get('all_n_natural_outcome_angle_first_moment_proved', False)}"
    )
    print(
        "Disjoint-pair collision transfer bounded: "
        f"{payload.get('claim_gate', {}).get('disjoint_pair_collision_biased_angle_moment_bounded', False)}"
    )
    print(
        "Overlapping adaptive collision control: "
        f"{payload.get('claim_gate', {}).get('overlapping_adaptive_collision_control_proved', False)}"
    )
    print(
        "Coherent branch PGM: "
        f"{payload.get('claim_gate', {}).get('coherent_carrier_branch_pgm_compiled', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_disjoint_pair_branch_pgm_compiler_boundary(subparsers) -> None:
    disjoint_pair_branch_pgm_compiler = subparsers.add_parser(
        "self-dual-wreath-disjoint-pair-branch-pgm-compiler-boundary",
        help="Falsify naive pair-local factorization of disjoint carrier-branch PGMs and isolate the shared-label covariance polar.",
    )
    disjoint_pair_branch_pgm_compiler.add_argument(
        "--no-registry",
        action="store_true",
    )
    disjoint_pair_branch_pgm_compiler.set_defaults(
        func=command_sdw_disjoint_pair_branch_pgm_compiler_boundary
    )


def command_sdw_disjoint_pair_branch_pgm_compiler_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_disjoint_pair_branch_pgm_compiler_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_disjoint_pair_branch_pgm_compiler_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("self_dual_wreath_disjoint_pair_branch_pgm_compiler_boundary complete")
    print(
        "Shared-hidden-label covariance identity: "
        f"{payload.get('claim_gate', {}).get('shared_hidden_label_covariance_identity_proved', False)}"
    )
    print(
        "Naive pair-local branch PGM falsified: "
        f"{payload.get('claim_gate', {}).get('naive_pair_local_branch_pgm_compiler_falsified', False)}"
    )
    print(
        "Covariance-aware branch PGM: "
        f"{payload.get('claim_gate', {}).get('covariance_aware_branch_pgm_compiled', False)}"
    )
    print(
        "Hidden-involution decoder: "
        f"{payload.get('claim_gate', {}).get('hidden_involution_decoder_compiled', False)}"
    )
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_disjoint_pair_covariance_polar_reduction(subparsers) -> None:
    disjoint_pair_covariance_polar = subparsers.add_parser(
        "self-dual-wreath-disjoint-pair-covariance-polar-reduction",
        help="Reduce the two-pair carrier PGM to a dimensionless shared-label covariance polar and audit its access normalization.",
    )
    disjoint_pair_covariance_polar.add_argument(
        "--no-registry",
        action="store_true",
    )
    disjoint_pair_covariance_polar.set_defaults(
        func=command_sdw_disjoint_pair_covariance_polar_reduction
    )


def command_sdw_disjoint_pair_covariance_polar_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_disjoint_pair_covariance_polar_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_disjoint_pair_covariance_polar_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    gate = payload.get("claim_gate", {})
    print("self_dual_wreath_disjoint_pair_covariance_polar_reduction complete")
    print(
        "Dimensionless covariance frame reduction: "
        f"{gate.get('dimensionless_covariance_frame_reduction_proved', False)}"
    )
    print(
        "Natural bounded-normalization schema: "
        f"{gate.get('constant_mass_bounded_covariance_lcu_schema_proved', False)}"
    )
    print(
        "Uniform public block encoding compiled: "
        f"{gate.get('uniform_public_covariance_block_encoding_compiled', False)}"
    )
    print(
        "Inverse-square-root spectral gap: "
        f"{gate.get('inverse_square_root_spectral_gap_proved', False)}"
    )
    print(f"Speedup claim allowed: {gate.get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_dimensionless_pgm_truncation_bridge(subparsers) -> None:
    dimensionless_pgm_truncation = subparsers.add_parser(
        "self-dual-wreath-dimensionless-pgm-truncation-bridge",
        help="Remove the minimum-positive-eigenvalue requirement by truncating the rank-scaled carrier PGM metric at a success-adaptive cutoff.",
    )
    dimensionless_pgm_truncation.add_argument(
        "--no-registry",
        action="store_true",
    )
    dimensionless_pgm_truncation.set_defaults(
        func=command_sdw_dimensionless_pgm_truncation_bridge
    )


def command_sdw_dimensionless_pgm_truncation_bridge(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_dimensionless_pgm_truncation_bridge_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_dimensionless_pgm_truncation_bridge_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    gate = payload.get("claim_gate", {})
    print("self_dual_wreath_dimensionless_pgm_truncation_bridge complete")
    print(
        "Mixed-state truncated PGM retention: "
        f"{gate.get('mixed_state_truncated_pgm_success_retention_proved', False)}"
    )
    print(
        "Minimum positive spectral edge required: "
        f"{gate.get('minimum_positive_spectral_edge_required', True)}"
    )
    print(
        "Full threshold metric block encoding: "
        f"{gate.get('full_threshold_metric_block_encoding_compiled', False)}"
    )
    print(
        "PGM output isometry: "
        f"{gate.get('pgm_output_isometry_compiled', False)}"
    )
    print(f"Speedup claim allowed: {gate.get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_local_block_metric_normalization_no_go(subparsers) -> None:
    local_block_metric_no_go = subparsers.add_parser(
        "self-dual-wreath-local-block-metric-normalization-no-go",
        help="Prove the exact natural pair-carrier marginal and rule out local singleton/pair LCU composition at threshold width.",
    )
    local_block_metric_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    local_block_metric_no_go.set_defaults(
        func=command_sdw_local_block_metric_normalization_no_go
    )


def command_sdw_local_block_metric_normalization_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_local_block_metric_normalization_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_local_block_metric_normalization_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    gate = payload.get("claim_gate", {})
    print("self_dual_wreath_local_block_metric_normalization_no_go complete")
    print(
        "Pair-carrier natural marginal: "
        f"{gate.get('pair_carrier_exact_natural_marginal_proved', False)}"
    )
    print(
        "Local threshold metric composition falsified: "
        f"{gate.get('local_singleton_pair_product_metric_access_falsified', False)}"
    )
    print(
        "Global shared-label metric access compiled: "
        f"{gate.get('global_shared_label_metric_access_compiled', False)}"
    )
    print(f"Speedup claim allowed: {gate.get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_scale_free_endpoint_graph_transfer_boundary(subparsers) -> None:
    scale_free_graph = subparsers.add_parser(
        "self-dual-wreath-scale-free-endpoint-graph-transfer-boundary",
        help="Run the response/short complementarity and scale-free relative graph-transfer boundary theorem.",
    )
    scale_free_graph.add_argument("--no-registry", action="store_true")
    scale_free_graph.set_defaults(
        func=command_sdw_scale_free_endpoint_graph_transfer_boundary
    )


def command_sdw_scale_free_endpoint_graph_transfer_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_scale_free_endpoint_graph_transfer_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_scale_free_endpoint_graph_transfer_boundary_report(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    print("self_dual_wreath_scale_free_endpoint_graph_transfer_boundary complete")
    print(
        "Speedup claim allowed: "
        f"{payload.get('claim_gate', {}).get('speedup_claim_allowed', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_self_dual_wreath_adaptive_syndrome_trim_transfer(subparsers) -> None:
    parser_self_dual_wreath_adaptive_syndrome_trim_transfer = subparsers.add_parser(
        "self-dual-wreath-adaptive-syndrome-trim-transfer",
        help="Run Self Dual Wreath Adaptive Syndrome Trim Transfer.",
    )
    parser_self_dual_wreath_adaptive_syndrome_trim_transfer.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_adaptive_syndrome_trim_transfer.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_adaptive_syndrome_trim_transfer.set_defaults(func=command_self_dual_wreath_adaptive_syndrome_trim_transfer)


def command_self_dual_wreath_adaptive_syndrome_trim_transfer(args: argparse.Namespace) -> int:
    from qsearch import write_adaptive_syndrome_trim_transfer_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_adaptive_syndrome_trim_transfer_report(output_path=output_path)
        else:
            payload = write_adaptive_syndrome_trim_transfer_report()
    except TypeError:
        payload = write_adaptive_syndrome_trim_transfer_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_base_orbit_reduction(subparsers) -> None:
    parser_self_dual_wreath_alternating_base_orbit_reduction = subparsers.add_parser(
        "self-dual-wreath-alternating-base-orbit-reduction",
        help="Run Self Dual Wreath Alternating Base Orbit Reduction.",
    )
    parser_self_dual_wreath_alternating_base_orbit_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_base_orbit_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_base_orbit_reduction.set_defaults(func=command_self_dual_wreath_alternating_base_orbit_reduction)


def command_self_dual_wreath_alternating_base_orbit_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_base_orbit_reduction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_base_orbit_reduction_report(output_path=output_path)
        else:
            payload = write_alternating_base_orbit_reduction_report()
    except TypeError:
        payload = write_alternating_base_orbit_reduction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_block_operator_anova(subparsers) -> None:
    parser_self_dual_wreath_alternating_block_operator_anova = subparsers.add_parser(
        "self-dual-wreath-alternating-block-operator-anova",
        help="Run Self Dual Wreath Alternating Block Operator Anova.",
    )
    parser_self_dual_wreath_alternating_block_operator_anova.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_block_operator_anova.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_block_operator_anova.set_defaults(func=command_self_dual_wreath_alternating_block_operator_anova)


def command_self_dual_wreath_alternating_block_operator_anova(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_block_operator_anova_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_block_operator_anova_report(output_path=output_path)
        else:
            payload = write_alternating_block_operator_anova_report()
    except TypeError:
        payload = write_alternating_block_operator_anova_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_cycle_type_block_dependence(subparsers) -> None:
    parser_self_dual_wreath_alternating_cycle_type_block_dependence = subparsers.add_parser(
        "self-dual-wreath-alternating-cycle-type-block-dependence",
        help="Run Self Dual Wreath Alternating Cycle Type Block Dependence.",
    )
    parser_self_dual_wreath_alternating_cycle_type_block_dependence.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_cycle_type_block_dependence.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_cycle_type_block_dependence.set_defaults(func=command_self_dual_wreath_alternating_cycle_type_block_dependence)


def command_self_dual_wreath_alternating_cycle_type_block_dependence(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_cycle_type_block_dependence_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_cycle_type_block_dependence_report(output_path=output_path)
        else:
            payload = write_alternating_cycle_type_block_dependence_report()
    except TypeError:
        payload = write_alternating_cycle_type_block_dependence_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_entropy_transfer_reduction(subparsers) -> None:
    parser_self_dual_wreath_alternating_entropy_transfer_reduction = subparsers.add_parser(
        "self-dual-wreath-alternating-entropy-transfer-reduction",
        help="Run Self Dual Wreath Alternating Entropy Transfer Reduction.",
    )
    parser_self_dual_wreath_alternating_entropy_transfer_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_entropy_transfer_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_entropy_transfer_reduction.set_defaults(func=command_self_dual_wreath_alternating_entropy_transfer_reduction)


def command_self_dual_wreath_alternating_entropy_transfer_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_entropy_transfer_reduction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_entropy_transfer_reduction_report(output_path=output_path)
        else:
            payload = write_alternating_entropy_transfer_reduction_report()
    except TypeError:
        payload = write_alternating_entropy_transfer_reduction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_even_collision_core_reduction(subparsers) -> None:
    parser_self_dual_wreath_alternating_even_collision_core_reduction = subparsers.add_parser(
        "self-dual-wreath-alternating-even-collision-core-reduction",
        help="Run Self Dual Wreath Alternating Even Collision Core Reduction.",
    )
    parser_self_dual_wreath_alternating_even_collision_core_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_even_collision_core_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_even_collision_core_reduction.set_defaults(func=command_self_dual_wreath_alternating_even_collision_core_reduction)


def command_self_dual_wreath_alternating_even_collision_core_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_even_collision_core_reduction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_even_collision_core_reduction_report(output_path=output_path)
        else:
            payload = write_alternating_even_collision_core_reduction_report()
    except TypeError:
        payload = write_alternating_even_collision_core_reduction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_even_collision_entropy_bridge(subparsers) -> None:
    parser_self_dual_wreath_alternating_even_collision_entropy_bridge = subparsers.add_parser(
        "self-dual-wreath-alternating-even-collision-entropy-bridge",
        help="Run Self Dual Wreath Alternating Even Collision Entropy Bridge.",
    )
    parser_self_dual_wreath_alternating_even_collision_entropy_bridge.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_even_collision_entropy_bridge.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_even_collision_entropy_bridge.set_defaults(func=command_self_dual_wreath_alternating_even_collision_entropy_bridge)


def command_self_dual_wreath_alternating_even_collision_entropy_bridge(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_even_collision_entropy_bridge_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_even_collision_entropy_bridge_report(output_path=output_path)
        else:
            payload = write_alternating_even_collision_entropy_bridge_report()
    except TypeError:
        payload = write_alternating_even_collision_entropy_bridge_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_even_collision_support_pressure(subparsers) -> None:
    parser_self_dual_wreath_alternating_even_collision_support_pressure = subparsers.add_parser(
        "self-dual-wreath-alternating-even-collision-support-pressure",
        help="Run Self Dual Wreath Alternating Even Collision Support Pressure.",
    )
    parser_self_dual_wreath_alternating_even_collision_support_pressure.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_even_collision_support_pressure.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_even_collision_support_pressure.set_defaults(func=command_self_dual_wreath_alternating_even_collision_support_pressure)


def command_self_dual_wreath_alternating_even_collision_support_pressure(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_even_collision_support_pressure_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_even_collision_support_pressure_report(output_path=output_path)
        else:
            payload = write_alternating_even_collision_support_pressure_report()
    except TypeError:
        payload = write_alternating_even_collision_support_pressure_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_parity_coset_channel(subparsers) -> None:
    parser_self_dual_wreath_alternating_parity_coset_channel = subparsers.add_parser(
        "self-dual-wreath-alternating-parity-coset-channel",
        help="Run Self Dual Wreath Alternating Parity Coset Channel.",
    )
    parser_self_dual_wreath_alternating_parity_coset_channel.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_parity_coset_channel.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_parity_coset_channel.set_defaults(func=command_self_dual_wreath_alternating_parity_coset_channel)


def command_self_dual_wreath_alternating_parity_coset_channel(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_parity_coset_channel_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_parity_coset_channel_report(output_path=output_path)
        else:
            payload = write_alternating_parity_coset_channel_report()
    except TypeError:
        payload = write_alternating_parity_coset_channel_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_product_character_zeta(subparsers) -> None:
    parser_self_dual_wreath_alternating_product_character_zeta = subparsers.add_parser(
        "self-dual-wreath-alternating-product-character-zeta",
        help="Run Self Dual Wreath Alternating Product Character Zeta.",
    )
    parser_self_dual_wreath_alternating_product_character_zeta.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_product_character_zeta.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_product_character_zeta.set_defaults(func=command_self_dual_wreath_alternating_product_character_zeta)


def command_self_dual_wreath_alternating_product_character_zeta(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_product_character_zeta_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_product_character_zeta_report(output_path=output_path)
        else:
            payload = write_alternating_product_character_zeta_report()
    except TypeError:
        payload = write_alternating_product_character_zeta_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_sixway_synergy_reduction(subparsers) -> None:
    parser_self_dual_wreath_alternating_sixway_synergy_reduction = subparsers.add_parser(
        "self-dual-wreath-alternating-sixway-synergy-reduction",
        help="Run Self Dual Wreath Alternating Sixway Synergy Reduction.",
    )
    parser_self_dual_wreath_alternating_sixway_synergy_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_sixway_synergy_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_sixway_synergy_reduction.set_defaults(func=command_self_dual_wreath_alternating_sixway_synergy_reduction)


def command_self_dual_wreath_alternating_sixway_synergy_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_sixway_synergy_reduction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_sixway_synergy_reduction_report(output_path=output_path)
        else:
            payload = write_alternating_sixway_synergy_reduction_report()
    except TypeError:
        payload = write_alternating_sixway_synergy_reduction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_alternating_trimmed_sixway_renyi_transfer(subparsers) -> None:
    parser_self_dual_wreath_alternating_trimmed_sixway_renyi_transfer = subparsers.add_parser(
        "self-dual-wreath-alternating-trimmed-sixway-renyi-transfer",
        help="Run Self Dual Wreath Alternating Trimmed Sixway Renyi Transfer.",
    )
    parser_self_dual_wreath_alternating_trimmed_sixway_renyi_transfer.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_alternating_trimmed_sixway_renyi_transfer.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_alternating_trimmed_sixway_renyi_transfer.set_defaults(func=command_self_dual_wreath_alternating_trimmed_sixway_renyi_transfer)


def command_self_dual_wreath_alternating_trimmed_sixway_renyi_transfer(args: argparse.Namespace) -> int:
    from qsearch import write_alternating_trimmed_sixway_renyi_transfer_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_alternating_trimmed_sixway_renyi_transfer_report(output_path=output_path)
        else:
            payload = write_alternating_trimmed_sixway_renyi_transfer_report()
    except TypeError:
        payload = write_alternating_trimmed_sixway_renyi_transfer_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_central_fiber_racah_information_reduction(subparsers) -> None:
    parser_self_dual_wreath_central_fiber_racah_information_reduction = subparsers.add_parser(
        "self-dual-wreath-central-fiber-racah-information-reduction",
        help="Run Self Dual Wreath Central Fiber Racah Information Reduction.",
    )
    parser_self_dual_wreath_central_fiber_racah_information_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_central_fiber_racah_information_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_central_fiber_racah_information_reduction.set_defaults(func=command_self_dual_wreath_central_fiber_racah_information_reduction)


def command_self_dual_wreath_central_fiber_racah_information_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_central_fiber_racah_information_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_central_fiber_racah_information_report(output_path=output_path)
        else:
            payload = write_central_fiber_racah_information_report()
    except TypeError:
        payload = write_central_fiber_racah_information_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_character_triangle_barrier(subparsers) -> None:
    parser_self_dual_wreath_character_triangle_barrier = subparsers.add_parser(
        "self-dual-wreath-character-triangle-barrier",
        help="Run Self Dual Wreath Character Triangle Barrier.",
    )
    parser_self_dual_wreath_character_triangle_barrier.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_character_triangle_barrier.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_character_triangle_barrier.set_defaults(func=command_self_dual_wreath_character_triangle_barrier)


def command_self_dual_wreath_character_triangle_barrier(args: argparse.Namespace) -> int:
    from qsearch import write_character_triangle_barrier_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_character_triangle_barrier_report(output_path=output_path)
        else:
            payload = write_character_triangle_barrier_report()
    except TypeError:
        payload = write_character_triangle_barrier_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_coherent_branching_transport_boundary(subparsers) -> None:
    parser_self_dual_wreath_coherent_branching_transport_boundary = subparsers.add_parser(
        "self-dual-wreath-coherent-branching-transport-boundary",
        help="Run Self Dual Wreath Coherent Branching Transport Boundary.",
    )
    parser_self_dual_wreath_coherent_branching_transport_boundary.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_coherent_branching_transport_boundary.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_coherent_branching_transport_boundary.set_defaults(func=command_self_dual_wreath_coherent_branching_transport_boundary)


def command_self_dual_wreath_coherent_branching_transport_boundary(args: argparse.Namespace) -> int:
    from qsearch import write_coherent_branching_transport_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_coherent_branching_transport_report(output_path=output_path)
        else:
            payload = write_coherent_branching_transport_report()
    except TypeError:
        payload = write_coherent_branching_transport_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_compressed_orientation_racah_cumulant_probe(subparsers) -> None:
    parser_self_dual_wreath_compressed_orientation_racah_cumulant_probe = subparsers.add_parser(
        "self-dual-wreath-compressed-orientation-racah-cumulant-probe",
        help="Run Self Dual Wreath Compressed Orientation Racah Cumulant Probe.",
    )
    parser_self_dual_wreath_compressed_orientation_racah_cumulant_probe.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_compressed_orientation_racah_cumulant_probe.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_compressed_orientation_racah_cumulant_probe.set_defaults(func=command_self_dual_wreath_compressed_orientation_racah_cumulant_probe)


def command_self_dual_wreath_compressed_orientation_racah_cumulant_probe(args: argparse.Namespace) -> int:
    from qsearch import write_compressed_orientation_racah_cumulant_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_compressed_orientation_racah_cumulant_report(output_path=output_path)
        else:
            payload = write_compressed_orientation_racah_cumulant_report()
    except TypeError:
        payload = write_compressed_orientation_racah_cumulant_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_compressed_racah_block_probe(subparsers) -> None:
    parser_self_dual_wreath_compressed_racah_block_probe = subparsers.add_parser(
        "self-dual-wreath-compressed-racah-block-probe",
        help="Run Self Dual Wreath Compressed Racah Block Probe.",
    )
    parser_self_dual_wreath_compressed_racah_block_probe.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_compressed_racah_block_probe.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_compressed_racah_block_probe.set_defaults(func=command_self_dual_wreath_compressed_racah_block_probe)


def command_self_dual_wreath_compressed_racah_block_probe(args: argparse.Namespace) -> int:
    from qsearch import write_compressed_racah_probe_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_compressed_racah_probe_report(output_path=output_path)
        else:
            payload = write_compressed_racah_probe_report()
    except TypeError:
        payload = write_compressed_racah_probe_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_compressed_racah_coupling_probe(subparsers) -> None:
    parser_self_dual_wreath_compressed_racah_coupling_probe = subparsers.add_parser(
        "self-dual-wreath-compressed-racah-coupling-probe",
        help="Run Self Dual Wreath Compressed Racah Coupling Probe.",
    )
    parser_self_dual_wreath_compressed_racah_coupling_probe.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_compressed_racah_coupling_probe.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_compressed_racah_coupling_probe.set_defaults(func=command_self_dual_wreath_compressed_racah_coupling_probe)


def command_self_dual_wreath_compressed_racah_coupling_probe(args: argparse.Namespace) -> int:
    from qsearch import write_complete_compressed_racah_coupling_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_complete_compressed_racah_coupling_report(output_path=output_path)
        else:
            payload = write_complete_compressed_racah_coupling_report()
    except TypeError:
        payload = write_complete_compressed_racah_coupling_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_dense_automaton_fiber_dyadic_boundary(subparsers) -> None:
    parser_self_dual_wreath_dense_automaton_fiber_dyadic_boundary = subparsers.add_parser(
        "self-dual-wreath-dense-automaton-fiber-dyadic-boundary",
        help="Run Self Dual Wreath Dense Automaton Fiber Dyadic Boundary.",
    )
    parser_self_dual_wreath_dense_automaton_fiber_dyadic_boundary.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_dense_automaton_fiber_dyadic_boundary.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_dense_automaton_fiber_dyadic_boundary.set_defaults(func=command_self_dual_wreath_dense_automaton_fiber_dyadic_boundary)


def command_self_dual_wreath_dense_automaton_fiber_dyadic_boundary(args: argparse.Namespace) -> int:
    from qsearch import write_dense_automaton_fiber_dyadic_boundary_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_dense_automaton_fiber_dyadic_boundary_report(output_path=output_path)
        else:
            payload = write_dense_automaton_fiber_dyadic_boundary_report()
    except TypeError:
        payload = write_dense_automaton_fiber_dyadic_boundary_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_disjoint_grid_recoupling_falsifier(subparsers) -> None:
    parser_self_dual_wreath_disjoint_grid_recoupling_falsifier = subparsers.add_parser(
        "self-dual-wreath-disjoint-grid-recoupling-falsifier",
        help="Run Self Dual Wreath Disjoint Grid Recoupling Falsifier.",
    )
    parser_self_dual_wreath_disjoint_grid_recoupling_falsifier.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_disjoint_grid_recoupling_falsifier.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_disjoint_grid_recoupling_falsifier.set_defaults(func=command_self_dual_wreath_disjoint_grid_recoupling_falsifier)


def command_self_dual_wreath_disjoint_grid_recoupling_falsifier(args: argparse.Namespace) -> int:
    from qsearch import write_disjoint_grid_recoupling_falsifier_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_disjoint_grid_recoupling_falsifier_report(output_path=output_path)
        else:
            payload = write_disjoint_grid_recoupling_falsifier_report()
    except TypeError:
        payload = write_disjoint_grid_recoupling_falsifier_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_dyadic_modular_fiber_torsion_no_go(subparsers) -> None:
    parser_self_dual_wreath_dyadic_modular_fiber_torsion_no_go = subparsers.add_parser(
        "self-dual-wreath-dyadic-modular-fiber-torsion-no-go",
        help="Run Self Dual Wreath Dyadic Modular Fiber Torsion No Go.",
    )
    parser_self_dual_wreath_dyadic_modular_fiber_torsion_no_go.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_dyadic_modular_fiber_torsion_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_dyadic_modular_fiber_torsion_no_go.set_defaults(func=command_self_dual_wreath_dyadic_modular_fiber_torsion_no_go)


def command_self_dual_wreath_dyadic_modular_fiber_torsion_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_dyadic_modular_fiber_torsion_no_go_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_dyadic_modular_fiber_torsion_no_go_report(output_path=output_path)
        else:
            payload = write_dyadic_modular_fiber_torsion_no_go_report()
    except TypeError:
        payload = write_dyadic_modular_fiber_torsion_no_go_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_fractional_haar_enhancement_reduction(subparsers) -> None:
    parser_self_dual_wreath_fractional_haar_enhancement_reduction = subparsers.add_parser(
        "self-dual-wreath-fractional-haar-enhancement-reduction",
        help="Run Self Dual Wreath Fractional Haar Enhancement Reduction.",
    )
    parser_self_dual_wreath_fractional_haar_enhancement_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_fractional_haar_enhancement_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_fractional_haar_enhancement_reduction.set_defaults(func=command_self_dual_wreath_fractional_haar_enhancement_reduction)


def command_self_dual_wreath_fractional_haar_enhancement_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_fractional_haar_enhancement_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_fractional_haar_enhancement_report(output_path=output_path)
        else:
            payload = write_fractional_haar_enhancement_report()
    except TypeError:
        payload = write_fractional_haar_enhancement_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_free_probability_projector_resolution_boundary(subparsers) -> None:
    parser_self_dual_wreath_free_probability_projector_resolution_boundary = subparsers.add_parser(
        "self-dual-wreath-free-probability-projector-resolution-boundary",
        help="Run Self Dual Wreath Free Probability Projector Resolution Boundary.",
    )
    parser_self_dual_wreath_free_probability_projector_resolution_boundary.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_free_probability_projector_resolution_boundary.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_free_probability_projector_resolution_boundary.set_defaults(func=command_self_dual_wreath_free_probability_projector_resolution_boundary)


def command_self_dual_wreath_free_probability_projector_resolution_boundary(args: argparse.Namespace) -> int:
    from qsearch import write_free_probability_projector_resolution_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_free_probability_projector_resolution_report(output_path=output_path)
        else:
            payload = write_free_probability_projector_resolution_report()
    except TypeError:
        payload = write_free_probability_projector_resolution_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_grid_quantum_marginal_boundary(subparsers) -> None:
    parser_self_dual_wreath_grid_quantum_marginal_boundary = subparsers.add_parser(
        "self-dual-wreath-grid-quantum-marginal-boundary",
        help="Run Self Dual Wreath Grid Quantum Marginal Boundary.",
    )
    parser_self_dual_wreath_grid_quantum_marginal_boundary.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_grid_quantum_marginal_boundary.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_grid_quantum_marginal_boundary.set_defaults(func=command_self_dual_wreath_grid_quantum_marginal_boundary)


def command_self_dual_wreath_grid_quantum_marginal_boundary(args: argparse.Namespace) -> int:
    from qsearch import write_grid_quantum_marginal_boundary_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_grid_quantum_marginal_boundary_report(output_path=output_path)
        else:
            payload = write_grid_quantum_marginal_boundary_report()
    except TypeError:
        payload = write_grid_quantum_marginal_boundary_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_orientation_fixed_support_control_variate(subparsers) -> None:
    parser_self_dual_wreath_orientation_fixed_support_control_variate = subparsers.add_parser(
        "self-dual-wreath-orientation-fixed-support-control-variate",
        help="Run Self Dual Wreath Orientation Fixed Support Control Variate.",
    )
    parser_self_dual_wreath_orientation_fixed_support_control_variate.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_orientation_fixed_support_control_variate.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_orientation_fixed_support_control_variate.set_defaults(func=command_self_dual_wreath_orientation_fixed_support_control_variate)


def command_self_dual_wreath_orientation_fixed_support_control_variate(args: argparse.Namespace) -> int:
    from qsearch import write_orientation_fixed_support_control_variate_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_orientation_fixed_support_control_variate_report(output_path=output_path)
        else:
            payload = write_orientation_fixed_support_control_variate_report()
    except TypeError:
        payload = write_orientation_fixed_support_control_variate_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_orientation_identity_tail_control_variate(subparsers) -> None:
    parser_self_dual_wreath_orientation_identity_tail_control_variate = subparsers.add_parser(
        "self-dual-wreath-orientation-identity-tail-control-variate",
        help="Run Self Dual Wreath Orientation Identity Tail Control Variate.",
    )
    parser_self_dual_wreath_orientation_identity_tail_control_variate.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_orientation_identity_tail_control_variate.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_orientation_identity_tail_control_variate.set_defaults(func=command_self_dual_wreath_orientation_identity_tail_control_variate)


def command_self_dual_wreath_orientation_identity_tail_control_variate(args: argparse.Namespace) -> int:
    from qsearch import write_orientation_identity_tail_control_variate_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_orientation_identity_tail_control_variate_report(output_path=output_path)
        else:
            payload = write_orientation_identity_tail_control_variate_report()
    except TypeError:
        payload = write_orientation_identity_tail_control_variate_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_orientation_word_map_classical_baseline(subparsers) -> None:
    parser_self_dual_wreath_orientation_word_map_classical_baseline = subparsers.add_parser(
        "self-dual-wreath-orientation-word-map-classical-baseline",
        help="Run Self Dual Wreath Orientation Word Map Classical Baseline.",
    )
    parser_self_dual_wreath_orientation_word_map_classical_baseline.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_orientation_word_map_classical_baseline.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_orientation_word_map_classical_baseline.set_defaults(func=command_self_dual_wreath_orientation_word_map_classical_baseline)


def command_self_dual_wreath_orientation_word_map_classical_baseline(args: argparse.Namespace) -> int:
    from qsearch import write_orientation_word_map_classical_baseline_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_orientation_word_map_classical_baseline_report(output_path=output_path)
        else:
            payload = write_orientation_word_map_classical_baseline_report()
    except TypeError:
        payload = write_orientation_word_map_classical_baseline_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_projector_orbit_variance(subparsers) -> None:
    parser_self_dual_wreath_parity_projector_orbit_variance = subparsers.add_parser(
        "self-dual-wreath-parity-projector-orbit-variance",
        help="Run Self Dual Wreath Parity Projector Orbit Variance.",
    )
    parser_self_dual_wreath_parity_projector_orbit_variance.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_projector_orbit_variance.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_projector_orbit_variance.set_defaults(func=command_self_dual_wreath_parity_projector_orbit_variance)


def command_self_dual_wreath_parity_projector_orbit_variance(args: argparse.Namespace) -> int:
    from qsearch import write_parity_projector_orbit_variance_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_projector_orbit_variance_report(output_path=output_path)
        else:
            payload = write_parity_projector_orbit_variance_report()
    except TypeError:
        payload = write_parity_projector_orbit_variance_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_projector_tetrahedral_reduction(subparsers) -> None:
    parser_self_dual_wreath_parity_projector_tetrahedral_reduction = subparsers.add_parser(
        "self-dual-wreath-parity-projector-tetrahedral-reduction",
        help="Run Self Dual Wreath Parity Projector Tetrahedral Reduction.",
    )
    parser_self_dual_wreath_parity_projector_tetrahedral_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_projector_tetrahedral_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_projector_tetrahedral_reduction.set_defaults(func=command_self_dual_wreath_parity_projector_tetrahedral_reduction)


def command_self_dual_wreath_parity_projector_tetrahedral_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_parity_projector_tetrahedral_reduction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_projector_tetrahedral_reduction_report(output_path=output_path)
        else:
            payload = write_parity_projector_tetrahedral_reduction_report()
    except TypeError:
        payload = write_parity_projector_tetrahedral_reduction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_racah_conditional_cumulant(subparsers) -> None:
    parser_self_dual_wreath_parity_racah_conditional_cumulant = subparsers.add_parser(
        "self-dual-wreath-parity-racah-conditional-cumulant",
        help="Run Self Dual Wreath Parity Racah Conditional Cumulant.",
    )
    parser_self_dual_wreath_parity_racah_conditional_cumulant.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_racah_conditional_cumulant.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_racah_conditional_cumulant.set_defaults(func=command_self_dual_wreath_parity_racah_conditional_cumulant)


def command_self_dual_wreath_parity_racah_conditional_cumulant(args: argparse.Namespace) -> int:
    from qsearch import write_parity_racah_conditional_cumulant_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_racah_conditional_cumulant_report(output_path=output_path)
        else:
            payload = write_parity_racah_conditional_cumulant_report()
    except TypeError:
        payload = write_parity_racah_conditional_cumulant_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_racah_information_projection(subparsers) -> None:
    parser_self_dual_wreath_parity_racah_information_projection = subparsers.add_parser(
        "self-dual-wreath-parity-racah-information-projection",
        help="Run Self Dual Wreath Parity Racah Information Projection.",
    )
    parser_self_dual_wreath_parity_racah_information_projection.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_racah_information_projection.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_racah_information_projection.set_defaults(func=command_self_dual_wreath_parity_racah_information_projection)


def command_self_dual_wreath_parity_racah_information_projection(args: argparse.Namespace) -> int:
    from qsearch import write_parity_racah_information_projection_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_racah_information_projection_report(output_path=output_path)
        else:
            payload = write_parity_racah_information_projection_report()
    except TypeError:
        payload = write_parity_racah_information_projection_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_racah_rank_residual_decomposition(subparsers) -> None:
    parser_self_dual_wreath_parity_racah_rank_residual_decomposition = subparsers.add_parser(
        "self-dual-wreath-parity-racah-rank-residual-decomposition",
        help="Run Self Dual Wreath Parity Racah Rank Residual Decomposition.",
    )
    parser_self_dual_wreath_parity_racah_rank_residual_decomposition.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_racah_rank_residual_decomposition.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_racah_rank_residual_decomposition.set_defaults(func=command_self_dual_wreath_parity_racah_rank_residual_decomposition)


def command_self_dual_wreath_parity_racah_rank_residual_decomposition(args: argparse.Namespace) -> int:
    from qsearch import write_parity_racah_rank_residual_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_racah_rank_residual_report(output_path=output_path)
        else:
            payload = write_parity_racah_rank_residual_report()
    except TypeError:
        payload = write_parity_racah_rank_residual_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_racah_toric_obstruction(subparsers) -> None:
    parser_self_dual_wreath_parity_racah_toric_obstruction = subparsers.add_parser(
        "self-dual-wreath-parity-racah-toric-obstruction",
        help="Run Self Dual Wreath Parity Racah Toric Obstruction.",
    )
    parser_self_dual_wreath_parity_racah_toric_obstruction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_racah_toric_obstruction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_racah_toric_obstruction.set_defaults(func=command_self_dual_wreath_parity_racah_toric_obstruction)


def command_self_dual_wreath_parity_racah_toric_obstruction(args: argparse.Namespace) -> int:
    from qsearch import write_parity_racah_toric_obstruction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_racah_toric_obstruction_report(output_path=output_path)
        else:
            payload = write_parity_racah_toric_obstruction_report()
    except TypeError:
        payload = write_parity_racah_toric_obstruction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_rank_profile_entropy_transfer(subparsers) -> None:
    parser_self_dual_wreath_parity_rank_profile_entropy_transfer = subparsers.add_parser(
        "self-dual-wreath-parity-rank-profile-entropy-transfer",
        help="Run Self Dual Wreath Parity Rank Profile Entropy Transfer.",
    )
    parser_self_dual_wreath_parity_rank_profile_entropy_transfer.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_rank_profile_entropy_transfer.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_rank_profile_entropy_transfer.set_defaults(func=command_self_dual_wreath_parity_rank_profile_entropy_transfer)


def command_self_dual_wreath_parity_rank_profile_entropy_transfer(args: argparse.Namespace) -> int:
    from qsearch import write_parity_rank_profile_entropy_transfer_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_rank_profile_entropy_transfer_report(output_path=output_path)
        else:
            payload = write_parity_rank_profile_entropy_transfer_report()
    except TypeError:
        payload = write_parity_rank_profile_entropy_transfer_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_rank_profile_physical_transfer_boundary(subparsers) -> None:
    parser_self_dual_wreath_parity_rank_profile_physical_transfer_boundary = subparsers.add_parser(
        "self-dual-wreath-parity-rank-profile-physical-transfer-boundary",
        help="Run Self Dual Wreath Parity Rank Profile Physical Transfer Boundary.",
    )
    parser_self_dual_wreath_parity_rank_profile_physical_transfer_boundary.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_rank_profile_physical_transfer_boundary.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_rank_profile_physical_transfer_boundary.set_defaults(func=command_self_dual_wreath_parity_rank_profile_physical_transfer_boundary)


def command_self_dual_wreath_parity_rank_profile_physical_transfer_boundary(args: argparse.Namespace) -> int:
    from qsearch import write_parity_rank_profile_physical_transfer_boundary_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_rank_profile_physical_transfer_boundary_report(output_path=output_path)
        else:
            payload = write_parity_rank_profile_physical_transfer_boundary_report()
    except TypeError:
        payload = write_parity_rank_profile_physical_transfer_boundary_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_rank_profile_plancherel_mixing(subparsers) -> None:
    parser_self_dual_wreath_parity_rank_profile_plancherel_mixing = subparsers.add_parser(
        "self-dual-wreath-parity-rank-profile-plancherel-mixing",
        help="Run Self Dual Wreath Parity Rank Profile Plancherel Mixing.",
    )
    parser_self_dual_wreath_parity_rank_profile_plancherel_mixing.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_rank_profile_plancherel_mixing.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_rank_profile_plancherel_mixing.set_defaults(func=command_self_dual_wreath_parity_rank_profile_plancherel_mixing)


def command_self_dual_wreath_parity_rank_profile_plancherel_mixing(args: argparse.Namespace) -> int:
    from qsearch import write_parity_rank_profile_plancherel_mixing_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_rank_profile_plancherel_mixing_report(output_path=output_path)
        else:
            payload = write_parity_rank_profile_plancherel_mixing_report()
    except TypeError:
        payload = write_parity_rank_profile_plancherel_mixing_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer(subparsers) -> None:
    parser_self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer = subparsers.add_parser(
        "self-dual-wreath-parity-rank-profile-trimmed-likelihood-transfer",
        help="Run Self Dual Wreath Parity Rank Profile Trimmed Likelihood Transfer.",
    )
    parser_self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer.set_defaults(func=command_self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer)


def command_self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer(args: argparse.Namespace) -> int:
    from qsearch import write_parity_rank_profile_trimmed_likelihood_transfer_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_parity_rank_profile_trimmed_likelihood_transfer_report(output_path=output_path)
        else:
            payload = write_parity_rank_profile_trimmed_likelihood_transfer_report()
    except TypeError:
        payload = write_parity_rank_profile_trimmed_likelihood_transfer_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_physical_orientation_racah_sampling(subparsers) -> None:
    parser_self_dual_wreath_physical_orientation_racah_sampling = subparsers.add_parser(
        "self-dual-wreath-physical-orientation-racah-sampling",
        help="Run Self Dual Wreath Physical Orientation Racah Sampling.",
    )
    parser_self_dual_wreath_physical_orientation_racah_sampling.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_physical_orientation_racah_sampling.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_physical_orientation_racah_sampling.set_defaults(func=command_self_dual_wreath_physical_orientation_racah_sampling)


def command_self_dual_wreath_physical_orientation_racah_sampling(args: argparse.Namespace) -> int:
    from qsearch import write_physical_orientation_racah_sampling_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_physical_orientation_racah_sampling_report(output_path=output_path)
        else:
            payload = write_physical_orientation_racah_sampling_report()
    except TypeError:
        payload = write_physical_orientation_racah_sampling_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_physical_outer_racah_sampling(subparsers) -> None:
    parser_self_dual_wreath_physical_outer_racah_sampling = subparsers.add_parser(
        "self-dual-wreath-physical-outer-racah-sampling",
        help="Run Self Dual Wreath Physical Outer Racah Sampling.",
    )
    parser_self_dual_wreath_physical_outer_racah_sampling.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_physical_outer_racah_sampling.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_physical_outer_racah_sampling.set_defaults(func=command_self_dual_wreath_physical_outer_racah_sampling)


def command_self_dual_wreath_physical_outer_racah_sampling(args: argparse.Namespace) -> int:
    from qsearch import write_physical_outer_racah_sampling_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_physical_outer_racah_sampling_report(output_path=output_path)
        else:
            payload = write_physical_outer_racah_sampling_report()
    except TypeError:
        payload = write_physical_outer_racah_sampling_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_physical_recoupling_rank_pressure_no_go(subparsers) -> None:
    parser_self_dual_wreath_physical_recoupling_rank_pressure_no_go = subparsers.add_parser(
        "self-dual-wreath-physical-recoupling-rank-pressure-no-go",
        help="Run Self Dual Wreath Physical Recoupling Rank Pressure No Go.",
    )
    parser_self_dual_wreath_physical_recoupling_rank_pressure_no_go.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_physical_recoupling_rank_pressure_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_physical_recoupling_rank_pressure_no_go.set_defaults(func=command_self_dual_wreath_physical_recoupling_rank_pressure_no_go)


def command_self_dual_wreath_physical_recoupling_rank_pressure_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_physical_recoupling_rank_pressure_no_go_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_physical_recoupling_rank_pressure_no_go_report(output_path=output_path)
        else:
            payload = write_physical_recoupling_rank_pressure_no_go_report()
    except TypeError:
        payload = write_physical_recoupling_rank_pressure_no_go_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_physical_recoupling_tetrahedral_synergy(subparsers) -> None:
    parser_self_dual_wreath_physical_recoupling_tetrahedral_synergy = subparsers.add_parser(
        "self-dual-wreath-physical-recoupling-tetrahedral-synergy",
        help="Run Self Dual Wreath Physical Recoupling Tetrahedral Synergy.",
    )
    parser_self_dual_wreath_physical_recoupling_tetrahedral_synergy.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_physical_recoupling_tetrahedral_synergy.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_physical_recoupling_tetrahedral_synergy.set_defaults(func=command_self_dual_wreath_physical_recoupling_tetrahedral_synergy)


def command_self_dual_wreath_physical_recoupling_tetrahedral_synergy(args: argparse.Namespace) -> int:
    from qsearch import write_physical_recoupling_tetrahedral_synergy_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_physical_recoupling_tetrahedral_synergy_report(output_path=output_path)
        else:
            payload = write_physical_recoupling_tetrahedral_synergy_report()
    except TypeError:
        payload = write_physical_recoupling_tetrahedral_synergy_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_plancherel_character_racah_fourier_reduction(subparsers) -> None:
    parser_self_dual_wreath_plancherel_character_racah_fourier_reduction = subparsers.add_parser(
        "self-dual-wreath-plancherel-character-racah-fourier-reduction",
        help="Run Self Dual Wreath Plancherel Character Racah Fourier Reduction.",
    )
    parser_self_dual_wreath_plancherel_character_racah_fourier_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_plancherel_character_racah_fourier_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_plancherel_character_racah_fourier_reduction.set_defaults(func=command_self_dual_wreath_plancherel_character_racah_fourier_reduction)


def command_self_dual_wreath_plancherel_character_racah_fourier_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_plancherel_character_racah_fourier_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_plancherel_character_racah_fourier_report(output_path=output_path)
        else:
            payload = write_plancherel_character_racah_fourier_report()
    except TypeError:
        payload = write_plancherel_character_racah_fourier_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_plancherel_down_up_racah_tail_reduction(subparsers) -> None:
    parser_self_dual_wreath_plancherel_down_up_racah_tail_reduction = subparsers.add_parser(
        "self-dual-wreath-plancherel-down-up-racah-tail-reduction",
        help="Run Self Dual Wreath Plancherel Down Up Racah Tail Reduction.",
    )
    parser_self_dual_wreath_plancherel_down_up_racah_tail_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_plancherel_down_up_racah_tail_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_plancherel_down_up_racah_tail_reduction.set_defaults(func=command_self_dual_wreath_plancherel_down_up_racah_tail_reduction)


def command_self_dual_wreath_plancherel_down_up_racah_tail_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_plancherel_down_up_racah_tail_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_plancherel_down_up_racah_tail_report(output_path=output_path)
        else:
            payload = write_plancherel_down_up_racah_tail_report()
    except TypeError:
        payload = write_plancherel_down_up_racah_tail_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_plancherel_marginal_compatibility_no_go(subparsers) -> None:
    parser_self_dual_wreath_plancherel_marginal_compatibility_no_go = subparsers.add_parser(
        "self-dual-wreath-plancherel-marginal-compatibility-no-go",
        help="Run Self Dual Wreath Plancherel Marginal Compatibility No Go.",
    )
    parser_self_dual_wreath_plancherel_marginal_compatibility_no_go.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_plancherel_marginal_compatibility_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_plancherel_marginal_compatibility_no_go.set_defaults(func=command_self_dual_wreath_plancherel_marginal_compatibility_no_go)


def command_self_dual_wreath_plancherel_marginal_compatibility_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_plancherel_marginal_compatibility_no_go_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_plancherel_marginal_compatibility_no_go_report(output_path=output_path)
        else:
            payload = write_plancherel_marginal_compatibility_no_go_report()
    except TypeError:
        payload = write_plancherel_marginal_compatibility_no_go_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_plancherel_recoupling_rank_pressure_no_go(subparsers) -> None:
    parser_self_dual_wreath_plancherel_recoupling_rank_pressure_no_go = subparsers.add_parser(
        "self-dual-wreath-plancherel-recoupling-rank-pressure-no-go",
        help="Run Self Dual Wreath Plancherel Recoupling Rank Pressure No Go.",
    )
    parser_self_dual_wreath_plancherel_recoupling_rank_pressure_no_go.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_plancherel_recoupling_rank_pressure_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_plancherel_recoupling_rank_pressure_no_go.set_defaults(func=command_self_dual_wreath_plancherel_recoupling_rank_pressure_no_go)


def command_self_dual_wreath_plancherel_recoupling_rank_pressure_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_plancherel_recoupling_rank_pressure_no_go_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_plancherel_recoupling_rank_pressure_no_go_report(output_path=output_path)
        else:
            payload = write_plancherel_recoupling_rank_pressure_no_go_report()
    except TypeError:
        payload = write_plancherel_recoupling_rank_pressure_no_go_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_projected_parity_coset_kernel(subparsers) -> None:
    parser_self_dual_wreath_projected_parity_coset_kernel = subparsers.add_parser(
        "self-dual-wreath-projected-parity-coset-kernel",
        help="Run Self Dual Wreath Projected Parity Coset Kernel.",
    )
    parser_self_dual_wreath_projected_parity_coset_kernel.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_projected_parity_coset_kernel.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_projected_parity_coset_kernel.set_defaults(func=command_self_dual_wreath_projected_parity_coset_kernel)


def command_self_dual_wreath_projected_parity_coset_kernel(args: argparse.Namespace) -> int:
    from qsearch import write_projected_parity_coset_kernel_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_projected_parity_coset_kernel_report(output_path=output_path)
        else:
            payload = write_projected_parity_coset_kernel_report()
    except TypeError:
        payload = write_projected_parity_coset_kernel_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_projected_tetrahedral_word_map(subparsers) -> None:
    parser_self_dual_wreath_projected_tetrahedral_word_map = subparsers.add_parser(
        "self-dual-wreath-projected-tetrahedral-word-map",
        help="Run Self Dual Wreath Projected Tetrahedral Word Map.",
    )
    parser_self_dual_wreath_projected_tetrahedral_word_map.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_projected_tetrahedral_word_map.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_projected_tetrahedral_word_map.set_defaults(func=command_self_dual_wreath_projected_tetrahedral_word_map)


def command_self_dual_wreath_projected_tetrahedral_word_map(args: argparse.Namespace) -> int:
    from qsearch import write_projected_tetrahedral_word_map_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_projected_tetrahedral_word_map_report(output_path=output_path)
        else:
            payload = write_projected_tetrahedral_word_map_report()
    except TypeError:
        payload = write_projected_tetrahedral_word_map_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_racah_entropic_delocalization_certificate(subparsers) -> None:
    parser_self_dual_wreath_racah_entropic_delocalization_certificate = subparsers.add_parser(
        "self-dual-wreath-racah-entropic-delocalization-certificate",
        help="Run Self Dual Wreath Racah Entropic Delocalization Certificate.",
    )
    parser_self_dual_wreath_racah_entropic_delocalization_certificate.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_racah_entropic_delocalization_certificate.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_racah_entropic_delocalization_certificate.set_defaults(func=command_self_dual_wreath_racah_entropic_delocalization_certificate)


def command_self_dual_wreath_racah_entropic_delocalization_certificate(args: argparse.Namespace) -> int:
    from qsearch import write_racah_entropic_delocalization_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_racah_entropic_delocalization_report(output_path=output_path)
        else:
            payload = write_racah_entropic_delocalization_report()
    except TypeError:
        payload = write_racah_entropic_delocalization_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_racah_fractional_moment_certificate(subparsers) -> None:
    parser_self_dual_wreath_racah_fractional_moment_certificate = subparsers.add_parser(
        "self-dual-wreath-racah-fractional-moment-certificate",
        help="Run Self Dual Wreath Racah Fractional Moment Certificate.",
    )
    parser_self_dual_wreath_racah_fractional_moment_certificate.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_racah_fractional_moment_certificate.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_racah_fractional_moment_certificate.set_defaults(func=command_self_dual_wreath_racah_fractional_moment_certificate)


def command_self_dual_wreath_racah_fractional_moment_certificate(args: argparse.Namespace) -> int:
    from qsearch import write_racah_fractional_moment_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_racah_fractional_moment_report(output_path=output_path)
        else:
            payload = write_racah_fractional_moment_report()
    except TypeError:
        payload = write_racah_fractional_moment_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_recoupling_channel_flatness_boundary(subparsers) -> None:
    parser_self_dual_wreath_recoupling_channel_flatness_boundary = subparsers.add_parser(
        "self-dual-wreath-recoupling-channel-flatness-boundary",
        help="Run Self Dual Wreath Recoupling Channel Flatness Boundary.",
    )
    parser_self_dual_wreath_recoupling_channel_flatness_boundary.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_recoupling_channel_flatness_boundary.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_recoupling_channel_flatness_boundary.set_defaults(func=command_self_dual_wreath_recoupling_channel_flatness_boundary)


def command_self_dual_wreath_recoupling_channel_flatness_boundary(args: argparse.Namespace) -> int:
    from qsearch import write_recoupling_channel_flatness_boundary_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_recoupling_channel_flatness_boundary_report(output_path=output_path)
        else:
            payload = write_recoupling_channel_flatness_boundary_report()
    except TypeError:
        payload = write_recoupling_channel_flatness_boundary_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_recoupling_collision_channel_reduction(subparsers) -> None:
    parser_self_dual_wreath_recoupling_collision_channel_reduction = subparsers.add_parser(
        "self-dual-wreath-recoupling-collision-channel-reduction",
        help="Run Self Dual Wreath Recoupling Collision Channel Reduction.",
    )
    parser_self_dual_wreath_recoupling_collision_channel_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_recoupling_collision_channel_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_recoupling_collision_channel_reduction.set_defaults(func=command_self_dual_wreath_recoupling_collision_channel_reduction)


def command_self_dual_wreath_recoupling_collision_channel_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_recoupling_collision_channel_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_recoupling_collision_channel_report(output_path=output_path)
        else:
            payload = write_recoupling_collision_channel_report()
    except TypeError:
        payload = write_recoupling_collision_channel_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_recoupling_dimension_certificate(subparsers) -> None:
    parser_self_dual_wreath_recoupling_dimension_certificate = subparsers.add_parser(
        "self-dual-wreath-recoupling-dimension-certificate",
        help="Run Self Dual Wreath Recoupling Dimension Certificate.",
    )
    parser_self_dual_wreath_recoupling_dimension_certificate.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_recoupling_dimension_certificate.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_recoupling_dimension_certificate.set_defaults(func=command_self_dual_wreath_recoupling_dimension_certificate)


def command_self_dual_wreath_recoupling_dimension_certificate(args: argparse.Namespace) -> int:
    from qsearch import write_recoupling_dimension_certificate_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_recoupling_dimension_certificate_report(output_path=output_path)
        else:
            payload = write_recoupling_dimension_certificate_report()
    except TypeError:
        payload = write_recoupling_dimension_certificate_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_recoupling_haar_gap_reduction(subparsers) -> None:
    parser_self_dual_wreath_recoupling_haar_gap_reduction = subparsers.add_parser(
        "self-dual-wreath-recoupling-haar-gap-reduction",
        help="Run Self Dual Wreath Recoupling Haar Gap Reduction.",
    )
    parser_self_dual_wreath_recoupling_haar_gap_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_recoupling_haar_gap_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_recoupling_haar_gap_reduction.set_defaults(func=command_self_dual_wreath_recoupling_haar_gap_reduction)


def command_self_dual_wreath_recoupling_haar_gap_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_recoupling_haar_gap_reduction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_recoupling_haar_gap_reduction_report(output_path=output_path)
        else:
            payload = write_recoupling_haar_gap_reduction_report()
    except TypeError:
        payload = write_recoupling_haar_gap_reduction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_recoupling_mutual_information_reduction(subparsers) -> None:
    parser_self_dual_wreath_recoupling_mutual_information_reduction = subparsers.add_parser(
        "self-dual-wreath-recoupling-mutual-information-reduction",
        help="Run Self Dual Wreath Recoupling Mutual Information Reduction.",
    )
    parser_self_dual_wreath_recoupling_mutual_information_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_recoupling_mutual_information_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_recoupling_mutual_information_reduction.set_defaults(func=command_self_dual_wreath_recoupling_mutual_information_reduction)


def command_self_dual_wreath_recoupling_mutual_information_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_recoupling_mutual_information_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_recoupling_mutual_information_report(output_path=output_path)
        else:
            payload = write_recoupling_mutual_information_report()
    except TypeError:
        payload = write_recoupling_mutual_information_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_separating_surface_target_mixing(subparsers) -> None:
    parser_self_dual_wreath_separating_surface_target_mixing = subparsers.add_parser(
        "self-dual-wreath-separating-surface-target-mixing",
        help="Run Self Dual Wreath Separating Surface Target Mixing.",
    )
    parser_self_dual_wreath_separating_surface_target_mixing.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_separating_surface_target_mixing.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_separating_surface_target_mixing.set_defaults(func=command_self_dual_wreath_separating_surface_target_mixing)


def command_self_dual_wreath_separating_surface_target_mixing(args: argparse.Namespace) -> int:
    from qsearch import write_separating_surface_target_mixing_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_separating_surface_target_mixing_report(output_path=output_path)
        else:
            payload = write_separating_surface_target_mixing_report()
    except TypeError:
        payload = write_separating_surface_target_mixing_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_sign_orbit_kl_chain_reduction(subparsers) -> None:
    parser_self_dual_wreath_sign_orbit_kl_chain_reduction = subparsers.add_parser(
        "self-dual-wreath-sign-orbit-kl-chain-reduction",
        help="Run Self Dual Wreath Sign Orbit Kl Chain Reduction.",
    )
    parser_self_dual_wreath_sign_orbit_kl_chain_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_sign_orbit_kl_chain_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_sign_orbit_kl_chain_reduction.set_defaults(func=command_self_dual_wreath_sign_orbit_kl_chain_reduction)


def command_self_dual_wreath_sign_orbit_kl_chain_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_sign_orbit_kl_chain_reduction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_sign_orbit_kl_chain_reduction_report(output_path=output_path)
        else:
            payload = write_sign_orbit_kl_chain_reduction_report()
    except TypeError:
        payload = write_sign_orbit_kl_chain_reduction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_sign_orbit_syndrome_reduction(subparsers) -> None:
    parser_self_dual_wreath_sign_orbit_syndrome_reduction = subparsers.add_parser(
        "self-dual-wreath-sign-orbit-syndrome-reduction",
        help="Run Self Dual Wreath Sign Orbit Syndrome Reduction.",
    )
    parser_self_dual_wreath_sign_orbit_syndrome_reduction.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_sign_orbit_syndrome_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_sign_orbit_syndrome_reduction.set_defaults(func=command_self_dual_wreath_sign_orbit_syndrome_reduction)


def command_self_dual_wreath_sign_orbit_syndrome_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_sign_orbit_syndrome_reduction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_sign_orbit_syndrome_reduction_report(output_path=output_path)
        else:
            payload = write_sign_orbit_syndrome_reduction_report()
    except TypeError:
        payload = write_sign_orbit_syndrome_reduction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_sign_syndrome_unconditional_decoupling(subparsers) -> None:
    parser_self_dual_wreath_sign_syndrome_unconditional_decoupling = subparsers.add_parser(
        "self-dual-wreath-sign-syndrome-unconditional-decoupling",
        help="Run Self Dual Wreath Sign Syndrome Unconditional Decoupling.",
    )
    parser_self_dual_wreath_sign_syndrome_unconditional_decoupling.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_sign_syndrome_unconditional_decoupling.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_sign_syndrome_unconditional_decoupling.set_defaults(func=command_self_dual_wreath_sign_syndrome_unconditional_decoupling)


def command_self_dual_wreath_sign_syndrome_unconditional_decoupling(args: argparse.Namespace) -> int:
    from qsearch import write_sign_syndrome_unconditional_decoupling_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_sign_syndrome_unconditional_decoupling_report(output_path=output_path)
        else:
            payload = write_sign_syndrome_unconditional_decoupling_report()
    except TypeError:
        payload = write_sign_syndrome_unconditional_decoupling_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_source_conditioned_channel_decoupling(subparsers) -> None:
    parser_self_dual_wreath_source_conditioned_channel_decoupling = subparsers.add_parser(
        "self-dual-wreath-source-conditioned-channel-decoupling",
        help="Run Self Dual Wreath Source Conditioned Channel Decoupling.",
    )
    parser_self_dual_wreath_source_conditioned_channel_decoupling.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_source_conditioned_channel_decoupling.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_source_conditioned_channel_decoupling.set_defaults(func=command_self_dual_wreath_source_conditioned_channel_decoupling)


def command_self_dual_wreath_source_conditioned_channel_decoupling(args: argparse.Namespace) -> int:
    from qsearch import write_source_conditioned_channel_decoupling_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_source_conditioned_channel_decoupling_report(output_path=output_path)
        else:
            payload = write_source_conditioned_channel_decoupling_report()
    except TypeError:
        payload = write_source_conditioned_channel_decoupling_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_tetrahedral_chi_square_tail_no_go(subparsers) -> None:
    parser_self_dual_wreath_tetrahedral_chi_square_tail_no_go = subparsers.add_parser(
        "self-dual-wreath-tetrahedral-chi-square-tail-no-go",
        help="Run Self Dual Wreath Tetrahedral Chi Square Tail No Go.",
    )
    parser_self_dual_wreath_tetrahedral_chi_square_tail_no_go.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_tetrahedral_chi_square_tail_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_tetrahedral_chi_square_tail_no_go.set_defaults(func=command_self_dual_wreath_tetrahedral_chi_square_tail_no_go)


def command_self_dual_wreath_tetrahedral_chi_square_tail_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_tetrahedral_chi_square_tail_no_go_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_tetrahedral_chi_square_tail_no_go_report(output_path=output_path)
        else:
            payload = write_tetrahedral_chi_square_tail_no_go_report()
    except TypeError:
        payload = write_tetrahedral_chi_square_tail_no_go_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_tetrahedral_collision_growth_scale(subparsers) -> None:
    parser_self_dual_wreath_tetrahedral_collision_growth_scale = subparsers.add_parser(
        "self-dual-wreath-tetrahedral-collision-growth-scale",
        help="Run Self Dual Wreath Tetrahedral Collision Growth Scale.",
    )
    parser_self_dual_wreath_tetrahedral_collision_growth_scale.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_tetrahedral_collision_growth_scale.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_tetrahedral_collision_growth_scale.set_defaults(func=command_self_dual_wreath_tetrahedral_collision_growth_scale)


def command_self_dual_wreath_tetrahedral_collision_growth_scale(args: argparse.Namespace) -> int:
    from qsearch import write_tetrahedral_collision_growth_scale_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_tetrahedral_collision_growth_scale_report(output_path=output_path)
        else:
            payload = write_tetrahedral_collision_growth_scale_report()
    except TypeError:
        payload = write_tetrahedral_collision_growth_scale_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_tetrahedral_dimension_trim(subparsers) -> None:
    parser_self_dual_wreath_tetrahedral_dimension_trim = subparsers.add_parser(
        "self-dual-wreath-tetrahedral-dimension-trim",
        help="Run Self Dual Wreath Tetrahedral Dimension Trim.",
    )
    parser_self_dual_wreath_tetrahedral_dimension_trim.add_argument("--output", help="Optional report output path")
    parser_self_dual_wreath_tetrahedral_dimension_trim.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_self_dual_wreath_tetrahedral_dimension_trim.set_defaults(func=command_self_dual_wreath_tetrahedral_dimension_trim)


def command_self_dual_wreath_tetrahedral_dimension_trim(args: argparse.Namespace) -> int:
    from qsearch import write_tetrahedral_dimension_trim_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_tetrahedral_dimension_trim_report(output_path=output_path)
        else:
            payload = write_tetrahedral_dimension_trim_report()
    except TypeError:
        payload = write_tetrahedral_dimension_trim_report()
    print(payload.get("summary", "Done"))
    return 0


def add_self_dual_wreath_component_dependency_ridge_physical_curl(subparsers) -> None:
    self_dual_wreath_component_dependency_ridge_physical_curl = subparsers.add_parser(
        "self-dual-wreath-component-dependency-ridge-physical-curl",
        help="Exp Code Self Dual Wreath Component Dependency Ridge Physical Curl",
    )
    self_dual_wreath_component_dependency_ridge_physical_curl.set_defaults(func=command_self_dual_wreath_component_dependency_ridge_physical_curl)


def command_self_dual_wreath_component_dependency_ridge_physical_curl(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_dependency_ridge_physical_curl_report
    report = write_component_dependency_ridge_physical_curl_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_dependency_ridge_physical_hamming(subparsers) -> None:
    self_dual_wreath_component_dependency_ridge_physical_hamming = subparsers.add_parser(
        "self-dual-wreath-component-dependency-ridge-physical-hamming",
        help="Exp Code Self Dual Wreath Component Dependency Ridge Physical Hamming",
    )
    self_dual_wreath_component_dependency_ridge_physical_hamming.set_defaults(func=command_self_dual_wreath_component_dependency_ridge_physical_hamming)


def command_self_dual_wreath_component_dependency_ridge_physical_hamming(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_dependency_ridge_physical_hamming_report
    report = write_component_dependency_ridge_physical_hamming_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_dependency_ridge_physical_spectrum(subparsers) -> None:
    self_dual_wreath_component_dependency_ridge_physical_spectrum = subparsers.add_parser(
        "self-dual-wreath-component-dependency-ridge-physical-spectrum",
        help="Exp Code Self Dual Wreath Component Dependency Ridge Physical Spectrum",
    )
    self_dual_wreath_component_dependency_ridge_physical_spectrum.set_defaults(func=command_self_dual_wreath_component_dependency_ridge_physical_spectrum)


def command_self_dual_wreath_component_dependency_ridge_physical_spectrum(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_dependency_ridge_physical_spectrum_report
    report = write_component_dependency_ridge_physical_spectrum_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_dependency_ridge_single_frame_tail(subparsers) -> None:
    self_dual_wreath_component_dependency_ridge_single_frame_tail = subparsers.add_parser(
        "self-dual-wreath-component-dependency-ridge-single-frame-tail",
        help="Exp Code Self Dual Wreath Component Dependency Ridge Single Frame Tail",
    )
    self_dual_wreath_component_dependency_ridge_single_frame_tail.set_defaults(func=command_self_dual_wreath_component_dependency_ridge_single_frame_tail)


def command_self_dual_wreath_component_dependency_ridge_single_frame_tail(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_dependency_ridge_single_frame_tail_report
    report = write_component_dependency_ridge_single_frame_tail_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_diagonal_leakage_bridge(subparsers) -> None:
    self_dual_wreath_component_diagonal_leakage_bridge = subparsers.add_parser(
        "self-dual-wreath-component-diagonal-leakage-bridge",
        help="Exp Code Self Dual Wreath Component Diagonal Leakage Bridge",
    )
    self_dual_wreath_component_diagonal_leakage_bridge.set_defaults(func=command_self_dual_wreath_component_diagonal_leakage_bridge)


def command_self_dual_wreath_component_diagonal_leakage_bridge(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_diagonal_leakage_bridge_report
    report = write_component_diagonal_leakage_bridge_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_leaf_fourier_commutator_duality(subparsers) -> None:
    self_dual_wreath_component_leaf_fourier_commutator_duality = subparsers.add_parser(
        "self-dual-wreath-component-leaf-fourier-commutator-duality",
        help="Exp Code Self Dual Wreath Component Leaf Fourier Commutator Duality",
    )
    self_dual_wreath_component_leaf_fourier_commutator_duality.set_defaults(func=command_self_dual_wreath_component_leaf_fourier_commutator_duality)


def command_self_dual_wreath_component_leaf_fourier_commutator_duality(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_leaf_fourier_commutator_duality_report
    report = write_component_leaf_fourier_commutator_duality_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_leaf_fourier_leverage(subparsers) -> None:
    self_dual_wreath_component_leaf_fourier_leverage = subparsers.add_parser(
        "self-dual-wreath-component-leaf-fourier-leverage",
        help="Exp Code Self Dual Wreath Component Leaf Fourier Leverage",
    )
    self_dual_wreath_component_leaf_fourier_leverage.set_defaults(func=command_self_dual_wreath_component_leaf_fourier_leverage)


def command_self_dual_wreath_component_leaf_fourier_leverage(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_leaf_fourier_leverage_report
    report = write_component_leaf_fourier_leverage_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_leaf_fourier_strata(subparsers) -> None:
    self_dual_wreath_component_leaf_fourier_strata = subparsers.add_parser(
        "self-dual-wreath-component-leaf-fourier-strata",
        help="Exp Code Self Dual Wreath Component Leaf Fourier Strata",
    )
    self_dual_wreath_component_leaf_fourier_strata.set_defaults(func=command_self_dual_wreath_component_leaf_fourier_strata)


def command_self_dual_wreath_component_leaf_fourier_strata(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_leaf_fourier_strata_report
    report = write_component_leaf_fourier_strata_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_m4_operational_boundary(subparsers) -> None:
    self_dual_wreath_component_m4_operational_boundary = subparsers.add_parser(
        "self-dual-wreath-component-m4-operational-boundary",
        help="Exp Code Self Dual Wreath Component M4 Operational Boundary",
    )
    self_dual_wreath_component_m4_operational_boundary.set_defaults(func=command_self_dual_wreath_component_m4_operational_boundary)


def command_self_dual_wreath_component_m4_operational_boundary(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_m4_operational_boundary_report
    report = write_component_m4_operational_boundary_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_polar_traffic_curl(subparsers) -> None:
    self_dual_wreath_component_polar_traffic_curl = subparsers.add_parser(
        "self-dual-wreath-component-polar-traffic-curl",
        help="Exp Code Self Dual Wreath Component Polar Traffic Curl",
    )
    self_dual_wreath_component_polar_traffic_curl.set_defaults(func=command_self_dual_wreath_component_polar_traffic_curl)


def command_self_dual_wreath_component_polar_traffic_curl(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_polar_traffic_curl_report
    report = write_component_polar_traffic_curl_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_single_leaf_diagonal_reduction(subparsers) -> None:
    self_dual_wreath_component_single_leaf_diagonal_reduction = subparsers.add_parser(
        "self-dual-wreath-component-single-leaf-diagonal-reduction",
        help="Exp Code Self Dual Wreath Component Single Leaf Diagonal Reduction",
    )
    self_dual_wreath_component_single_leaf_diagonal_reduction.set_defaults(func=command_self_dual_wreath_component_single_leaf_diagonal_reduction)


def command_self_dual_wreath_component_single_leaf_diagonal_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_single_leaf_diagonal_reduction_report
    report = write_component_single_leaf_diagonal_reduction_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_size_biased_effect_law(subparsers) -> None:
    self_dual_wreath_component_size_biased_effect_law = subparsers.add_parser(
        "self-dual-wreath-component-size-biased-effect-law",
        help="Exp Code Self Dual Wreath Component Size Biased Effect Law",
    )
    self_dual_wreath_component_size_biased_effect_law.set_defaults(func=command_self_dual_wreath_component_size_biased_effect_law)


def command_self_dual_wreath_component_size_biased_effect_law(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_component_size_biased_effect_law_report
    report = write_component_size_biased_effect_law_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_point_parent_coherence_witness(subparsers) -> None:
    self_dual_wreath_point_parent_coherence_witness = subparsers.add_parser(
        "self-dual-wreath-point-parent-coherence-witness",
        help="Exp Code Self Dual Wreath Point Parent Coherence Witness",
    )
    self_dual_wreath_point_parent_coherence_witness.set_defaults(func=command_self_dual_wreath_point_parent_coherence_witness)


def command_self_dual_wreath_point_parent_coherence_witness(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_point_parent_coherence_witness_report
    report = write_point_parent_coherence_witness_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_point_pgm_coarse_graining(subparsers) -> None:
    self_dual_wreath_point_pgm_coarse_graining = subparsers.add_parser(
        "self-dual-wreath-point-pgm-coarse-graining",
        help="Exp Code Self Dual Wreath Point Pgm Coarse Graining",
    )
    self_dual_wreath_point_pgm_coarse_graining.set_defaults(func=command_self_dual_wreath_point_pgm_coarse_graining)


def command_self_dual_wreath_point_pgm_coarse_graining(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_point_pgm_coarse_graining_report
    report = write_point_pgm_coarse_graining_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_point_stabilizer_collision_free_kernel(subparsers) -> None:
    self_dual_wreath_point_stabilizer_collision_free_kernel = subparsers.add_parser(
        "self-dual-wreath-point-stabilizer-collision-free-kernel",
        help="Exp Code Self Dual Wreath Point Stabilizer Collision Free Kernel",
    )
    self_dual_wreath_point_stabilizer_collision_free_kernel.set_defaults(func=command_self_dual_wreath_point_stabilizer_collision_free_kernel)


def command_self_dual_wreath_point_stabilizer_collision_free_kernel(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_collision_free_point_kernel_report
    report = write_collision_free_point_kernel_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_point_stabilizer_quotient(subparsers) -> None:
    self_dual_wreath_point_stabilizer_quotient = subparsers.add_parser(
        "self-dual-wreath-point-stabilizer-quotient",
        help="Exp Code Self Dual Wreath Point Stabilizer Quotient",
    )
    self_dual_wreath_point_stabilizer_quotient.set_defaults(func=command_self_dual_wreath_point_stabilizer_quotient)


def command_self_dual_wreath_point_stabilizer_quotient(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_point_stabilizer_quotient_report
    report = write_point_stabilizer_quotient_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_point_standard_energy(subparsers) -> None:
    self_dual_wreath_point_standard_energy = subparsers.add_parser(
        "self-dual-wreath-point-standard-energy",
        help="Exp Code Self Dual Wreath Point Standard Energy",
    )
    self_dual_wreath_point_standard_energy.set_defaults(func=command_self_dual_wreath_point_standard_energy)


def command_self_dual_wreath_point_standard_energy(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_point_standard_energy_report
    report = write_point_standard_energy_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_point_young_star_naimark(subparsers) -> None:
    self_dual_wreath_point_young_star_naimark = subparsers.add_parser(
        "self-dual-wreath-point-young-star-naimark",
        help="Exp Code Self Dual Wreath Point Young Star Naimark",
    )
    self_dual_wreath_point_young_star_naimark.set_defaults(func=command_self_dual_wreath_point_young_star_naimark)


def command_self_dual_wreath_point_young_star_naimark(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_young_star_naimark_report
    report = write_young_star_naimark_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_recursive_kernel_isometry(subparsers) -> None:
    self_dual_wreath_recursive_kernel_isometry = subparsers.add_parser(
        "self-dual-wreath-recursive-kernel-isometry",
        help="Exp Code Self Dual Wreath Recursive Kernel Isometry",
    )
    self_dual_wreath_recursive_kernel_isometry.set_defaults(func=command_self_dual_wreath_recursive_kernel_isometry)


def command_self_dual_wreath_recursive_kernel_isometry(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_recursive_kernel_isometry_report
    report = write_recursive_kernel_isometry_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_reversible_automaton_fiber_collapse(subparsers) -> None:
    self_dual_wreath_reversible_automaton_fiber_collapse = subparsers.add_parser(
        "self-dual-wreath-reversible-automaton-fiber-collapse",
        help="Exp Code Self Dual Wreath Reversible Automaton Fiber Collapse",
    )
    self_dual_wreath_reversible_automaton_fiber_collapse.set_defaults(func=command_self_dual_wreath_reversible_automaton_fiber_collapse)


def command_self_dual_wreath_reversible_automaton_fiber_collapse(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_reversible_automaton_fiber_report
    report = write_reversible_automaton_fiber_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_shared_pair_recoupling_decoupling(subparsers) -> None:
    self_dual_wreath_shared_pair_recoupling_decoupling = subparsers.add_parser(
        "self-dual-wreath-shared-pair-recoupling-decoupling",
        help="Exp Code Self Dual Wreath Shared Pair Recoupling Decoupling",
    )
    self_dual_wreath_shared_pair_recoupling_decoupling.set_defaults(func=command_self_dual_wreath_shared_pair_recoupling_decoupling)


def command_self_dual_wreath_shared_pair_recoupling_decoupling(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_shared_pair_recoupling_decoupling_report
    report = write_shared_pair_recoupling_decoupling_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_sibling_frame_all_fixed_joint(subparsers) -> None:
    self_dual_wreath_sibling_frame_all_fixed_joint = subparsers.add_parser(
        "self-dual-wreath-sibling-frame-all-fixed-joint",
        help="Exp Code Self Dual Wreath Sibling Frame All Fixed Joint",
    )
    self_dual_wreath_sibling_frame_all_fixed_joint.set_defaults(func=command_self_dual_wreath_sibling_frame_all_fixed_joint)


def command_self_dual_wreath_sibling_frame_all_fixed_joint(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_sibling_frame_all_fixed_joint_report
    report = write_sibling_frame_all_fixed_joint_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_sibling_frame_all_fixed_mp(subparsers) -> None:
    self_dual_wreath_sibling_frame_all_fixed_mp = subparsers.add_parser(
        "self-dual-wreath-sibling-frame-all-fixed-mp",
        help="Exp Code Self Dual Wreath Sibling Frame All Fixed Mp",
    )
    self_dual_wreath_sibling_frame_all_fixed_mp.set_defaults(func=command_self_dual_wreath_sibling_frame_all_fixed_mp)


def command_self_dual_wreath_sibling_frame_all_fixed_mp(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_sibling_frame_all_fixed_mp_report
    report = write_sibling_frame_all_fixed_mp_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_sign_twist_collective_activation(subparsers) -> None:
    self_dual_wreath_sign_twist_collective_activation = subparsers.add_parser(
        "self-dual-wreath-sign-twist-collective-activation",
        help="Exp Code Self Dual Wreath Sign Twist Collective Activation",
    )
    self_dual_wreath_sign_twist_collective_activation.set_defaults(func=command_self_dual_wreath_sign_twist_collective_activation)


def command_self_dual_wreath_sign_twist_collective_activation(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_sign_twist_collective_activation_report
    report = write_sign_twist_collective_activation_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_self_dual_wreath_component_direct_naimark_polar_equivalence(subparsers) -> None:
    parser_self_dual_wreath_component_direct_naimark_polar_equivalence = subparsers.add_parser(
        "self-dual-wreath-component-direct-naimark-polar-equivalence",
        help="Direct component Naimark dilation is a restricted orientation polar.",
    )
    parser_self_dual_wreath_component_direct_naimark_polar_equivalence.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_component_direct_naimark_polar_equivalence.set_defaults(func=command_self_dual_wreath_component_direct_naimark_polar_equivalence)


def command_self_dual_wreath_component_direct_naimark_polar_equivalence(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_direct_naimark_polar_equivalence_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_component_direct_naimark_polar_equivalence_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_component_direct_naimark_polar_equivalence_report()
    validation = validate_registry()
    print("self_dual_wreath_component_direct_naimark_polar_equivalence complete")
    print("Artifact: research/representation/self_dual_wreath_component_direct_naimark_polar_equivalence.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_component_polar_physical_pgm_closure(subparsers) -> None:
    parser_self_dual_wreath_component_polar_physical_pgm_closure = subparsers.add_parser(
        "self-dual-wreath-component-polar-physical-pgm-closure",
        help="The complete orientation polar closes the physical PGM and decoder gate.",
    )
    parser_self_dual_wreath_component_polar_physical_pgm_closure.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_component_polar_physical_pgm_closure.set_defaults(func=command_self_dual_wreath_component_polar_physical_pgm_closure)


def command_self_dual_wreath_component_polar_physical_pgm_closure(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_polar_physical_pgm_closure_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_component_polar_physical_pgm_closure_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_component_polar_physical_pgm_closure_report()
    validation = validate_registry()
    print("self_dual_wreath_component_polar_physical_pgm_closure complete")
    print("Artifact: research/representation/self_dual_wreath_component_polar_physical_pgm_closure.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_connected_clifford_normal_form(subparsers) -> None:
    parser_self_dual_wreath_connected_clifford_normal_form = subparsers.add_parser(
        "self-dual-wreath-connected-clifford-normal-form",
        help="Clifford theory exposes, but does not solve, the connected CS polar.",
    )
    parser_self_dual_wreath_connected_clifford_normal_form.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_connected_clifford_normal_form.set_defaults(func=command_self_dual_wreath_connected_clifford_normal_form)


def command_self_dual_wreath_connected_clifford_normal_form(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_connected_clifford_normal_form_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_connected_clifford_normal_form_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_connected_clifford_normal_form_report()
    validation = validate_registry()
    print("self_dual_wreath_connected_clifford_normal_form complete")
    print("Artifact: research/representation/self_dual_wreath_connected_clifford_normal_form.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_connected_quotient_heisenberg_reduction(subparsers) -> None:
    parser_self_dual_wreath_connected_quotient_heisenberg_reduction = subparsers.add_parser(
        "self-dual-wreath-connected-quotient-heisenberg-reduction",
        help="The connected orientation group has an easy class-two parity quotient.",
    )
    parser_self_dual_wreath_connected_quotient_heisenberg_reduction.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_connected_quotient_heisenberg_reduction.set_defaults(func=command_self_dual_wreath_connected_quotient_heisenberg_reduction)


def command_self_dual_wreath_connected_quotient_heisenberg_reduction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_connected_quotient_heisenberg_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_connected_quotient_heisenberg_reduction_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_connected_quotient_heisenberg_reduction_report()
    validation = validate_registry()
    print("self_dual_wreath_connected_quotient_heisenberg_reduction complete")
    print("Artifact: research/representation/self_dual_wreath_connected_quotient_heisenberg_reduction.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_gpe_fusion_tree_cs_boundary(subparsers) -> None:
    parser_self_dual_wreath_gpe_fusion_tree_cs_boundary = subparsers.add_parser(
        "self-dual-wreath-gpe-fusion-tree-cs-boundary",
        help="Recursive GPE compiles recoupling unitaries, not their CS subblock polar.",
    )
    parser_self_dual_wreath_gpe_fusion_tree_cs_boundary.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_gpe_fusion_tree_cs_boundary.set_defaults(func=command_self_dual_wreath_gpe_fusion_tree_cs_boundary)


def command_self_dual_wreath_gpe_fusion_tree_cs_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_gpe_fusion_tree_cs_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_gpe_fusion_tree_cs_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_gpe_fusion_tree_cs_boundary_report()
    validation = validate_registry()
    print("self_dual_wreath_gpe_fusion_tree_cs_boundary complete")
    print("Artifact: research/representation/self_dual_wreath_gpe_fusion_tree_cs_boundary.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_latent_master_polar_tradeoff(subparsers) -> None:
    parser_self_dual_wreath_latent_master_polar_tradeoff = subparsers.add_parser(
        "self-dual-wreath-latent-master-polar-tradeoff",
        help="A latent master fiber moves, but does not remove, polar normalization cost.",
    )
    parser_self_dual_wreath_latent_master_polar_tradeoff.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_latent_master_polar_tradeoff.set_defaults(func=command_self_dual_wreath_latent_master_polar_tradeoff)


def command_self_dual_wreath_latent_master_polar_tradeoff(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_latent_master_polar_tradeoff_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_latent_master_polar_tradeoff_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_latent_master_polar_tradeoff_report()
    validation = validate_registry()
    print("self_dual_wreath_latent_master_polar_tradeoff complete")
    print("Artifact: research/representation/self_dual_wreath_latent_master_polar_tradeoff.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_mrs_identification_escape_theorem(subparsers) -> None:
    parser_self_dual_wreath_mrs_identification_escape_theorem = subparsers.add_parser(
        "self-dual-wreath-mrs-identification-escape-theorem",
        help="Identification success separates the target PGM from every MRS sieve.",
    )
    parser_self_dual_wreath_mrs_identification_escape_theorem.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_mrs_identification_escape_theorem.set_defaults(func=command_self_dual_wreath_mrs_identification_escape_theorem)


def command_self_dual_wreath_mrs_identification_escape_theorem(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_mrs_identification_escape_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_mrs_identification_escape_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_mrs_identification_escape_report()
    validation = validate_registry()
    print("self_dual_wreath_mrs_identification_escape_theorem complete")
    print("Artifact: research/representation/self_dual_wreath_mrs_identification_escape_theorem.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_orientation_fixed_space_recoupling(subparsers) -> None:
    parser_self_dual_wreath_orientation_fixed_space_recoupling = subparsers.add_parser(
        "self-dual-wreath-orientation-fixed-space-recoupling",
        help="Exact fixed-space recoupling target inside the homogeneous orientation polar.",
    )
    parser_self_dual_wreath_orientation_fixed_space_recoupling.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_orientation_fixed_space_recoupling.set_defaults(func=command_self_dual_wreath_orientation_fixed_space_recoupling)


def command_self_dual_wreath_orientation_fixed_space_recoupling(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_fixed_space_recoupling_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_fixed_space_recoupling_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_fixed_space_recoupling_report()
    validation = validate_registry()
    print("self_dual_wreath_orientation_fixed_space_recoupling complete")
    print("Artifact: research/representation/self_dual_wreath_orientation_fixed_space_recoupling.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_orientation_homogeneous_space_polar(subparsers) -> None:
    parser_self_dual_wreath_orientation_homogeneous_space_polar = subparsers.add_parser(
        "self-dual-wreath-orientation-homogeneous-space-polar",
        help="Homogeneous-space flattening of the complete orientation polar.",
    )
    parser_self_dual_wreath_orientation_homogeneous_space_polar.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_orientation_homogeneous_space_polar.set_defaults(func=command_self_dual_wreath_orientation_homogeneous_space_polar)


def command_self_dual_wreath_orientation_homogeneous_space_polar(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_homogeneous_space_polar_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_orientation_homogeneous_space_polar_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_orientation_homogeneous_space_polar_report()
    validation = validate_registry()
    print("self_dual_wreath_orientation_homogeneous_space_polar complete")
    print("Artifact: research/representation/self_dual_wreath_orientation_homogeneous_space_polar.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_orientation_syndrome_component_reduction(subparsers) -> None:
    parser_self_dual_wreath_orientation_syndrome_component_reduction = subparsers.add_parser(
        "self-dual-wreath-orientation-syndrome-component-reduction",
        help="Parity-component reduction of the homogeneous orientation incidence.",
    )
    parser_self_dual_wreath_orientation_syndrome_component_reduction.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_orientation_syndrome_component_reduction.set_defaults(func=command_self_dual_wreath_orientation_syndrome_component_reduction)


def command_self_dual_wreath_orientation_syndrome_component_reduction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_syndrome_component_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_syndrome_component_reduction_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_syndrome_component_reduction_report()
    validation = validate_registry()
    print("self_dual_wreath_orientation_syndrome_component_reduction complete")
    print("Artifact: research/representation/self_dual_wreath_orientation_syndrome_component_reduction.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_pair_relation_common_support_no_go(subparsers) -> None:
    parser_self_dual_wreath_pair_relation_common_support_no_go = subparsers.add_parser(
        "self-dual-wreath-pair-relation-common-support-no-go",
        help="Every exact two-vertex relation is confined to literal common support.",
    )
    parser_self_dual_wreath_pair_relation_common_support_no_go.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_pair_relation_common_support_no_go.set_defaults(func=command_self_dual_wreath_pair_relation_common_support_no_go)


def command_self_dual_wreath_pair_relation_common_support_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_relation_common_support_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_pair_relation_common_support_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_pair_relation_common_support_no_go_report()
    validation = validate_registry()
    print("self_dual_wreath_pair_relation_common_support_no_go complete")
    print("Artifact: research/representation/self_dual_wreath_pair_relation_common_support_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_pair_sheaf_metric_incompatibility(subparsers) -> None:
    parser_self_dual_wreath_pair_sheaf_metric_incompatibility = subparsers.add_parser(
        "self-dual-wreath-pair-sheaf-metric-incompatibility",
        help="Noncommon pair-polars cannot be glued into the global frame polar.",
    )
    parser_self_dual_wreath_pair_sheaf_metric_incompatibility.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_pair_sheaf_metric_incompatibility.set_defaults(func=command_self_dual_wreath_pair_sheaf_metric_incompatibility)


def command_self_dual_wreath_pair_sheaf_metric_incompatibility(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_sheaf_metric_incompatibility_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_pair_sheaf_metric_incompatibility_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_pair_sheaf_metric_incompatibility_report()
    validation = validate_registry()
    print("self_dual_wreath_pair_sheaf_metric_incompatibility complete")
    print("Artifact: research/representation/self_dual_wreath_pair_sheaf_metric_incompatibility.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_point_centered_residual_no_go(subparsers) -> None:
    parser_self_dual_wreath_point_centered_residual_no_go = subparsers.add_parser(
        "self-dual-wreath-point-centered-residual-no-go",
        help="Centered residual no-go for carrier-traced point decoding.",
    )
    parser_self_dual_wreath_point_centered_residual_no_go.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_point_centered_residual_no_go.set_defaults(func=command_self_dual_wreath_point_centered_residual_no_go)


def command_self_dual_wreath_point_centered_residual_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_point_centered_residual_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_point_centered_residual_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_point_centered_residual_report()
    validation = validate_registry()
    print("self_dual_wreath_point_centered_residual_no_go complete")
    print("Artifact: research/representation/self_dual_wreath_point_centered_residual_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_point_child_star_relative_collision(subparsers) -> None:
    parser_self_dual_wreath_point_child_star_relative_collision = subparsers.add_parser(
        "self-dual-wreath-point-child-star-relative-collision",
        help="Positive Young-star decomposition of the point PGM relative collision.",
    )
    parser_self_dual_wreath_point_child_star_relative_collision.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_point_child_star_relative_collision.set_defaults(func=command_self_dual_wreath_point_child_star_relative_collision)


def command_self_dual_wreath_point_child_star_relative_collision(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_point_child_star_relative_collision_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_point_child_star_relative_collision_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_point_child_star_relative_collision_report()
    validation = validate_registry()
    print("self_dual_wreath_point_child_star_relative_collision complete")
    print("Artifact: research/representation/self_dual_wreath_point_child_star_relative_collision.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_point_copy_threshold(subparsers) -> None:
    parser_self_dual_wreath_point_copy_threshold = subparsers.add_parser(
        "self-dual-wreath-point-copy-threshold",
        help="Sharp copy threshold for the annealed point-quotient signal.",
    )
    parser_self_dual_wreath_point_copy_threshold.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_point_copy_threshold.set_defaults(func=command_self_dual_wreath_point_copy_threshold)


def command_self_dual_wreath_point_copy_threshold(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_point_copy_threshold_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_point_copy_threshold_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_point_copy_threshold_report()
    validation = validate_registry()
    print("self_dual_wreath_point_copy_threshold complete")
    print("Artifact: research/representation/self_dual_wreath_point_copy_threshold.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_point_critical_energy_separation(subparsers) -> None:
    parser_self_dual_wreath_point_critical_energy_separation = subparsers.add_parser(
        "self-dual-wreath-point-critical-energy-separation",
        help="Critical point energy does not determine operational distinguishability.",
    )
    parser_self_dual_wreath_point_critical_energy_separation.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_point_critical_energy_separation.set_defaults(func=command_self_dual_wreath_point_critical_energy_separation)


def command_self_dual_wreath_point_critical_energy_separation(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_critical_energy_separation_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_critical_energy_separation_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_critical_energy_separation_report()
    validation = validate_registry()
    print("self_dual_wreath_point_critical_energy_separation complete")
    print("Artifact: research/representation/self_dual_wreath_point_critical_energy_separation.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_point_critical_identity_atom(subparsers) -> None:
    parser_self_dual_wreath_point_critical_identity_atom = subparsers.add_parser(
        "self-dual-wreath-point-critical-identity-atom",
        help="The critical ambient point-energy spike is a factorially rare atom.",
    )
    parser_self_dual_wreath_point_critical_identity_atom.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_point_critical_identity_atom.set_defaults(func=command_self_dual_wreath_point_critical_identity_atom)


def command_self_dual_wreath_point_critical_identity_atom(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_critical_identity_atom_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_critical_identity_atom_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_critical_identity_atom_report()
    validation = validate_registry()
    print("self_dual_wreath_point_critical_identity_atom complete")
    print("Artifact: research/representation/self_dual_wreath_point_critical_identity_atom.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_regular_master_walsh_flatness_no_go(subparsers) -> None:
    parser_self_dual_wreath_regular_master_walsh_flatness_no_go = subparsers.add_parser(
        "self-dual-wreath-regular-master-walsh-flatness-no-go",
        help="Regular-source Walsh output is flat, killing fixed sparse-mode truncation.",
    )
    parser_self_dual_wreath_regular_master_walsh_flatness_no_go.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_regular_master_walsh_flatness_no_go.set_defaults(func=command_self_dual_wreath_regular_master_walsh_flatness_no_go)


def command_self_dual_wreath_regular_master_walsh_flatness_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_regular_master_walsh_flatness_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_regular_master_walsh_flatness_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_regular_master_walsh_flatness_report()
    validation = validate_registry()
    print("self_dual_wreath_regular_master_walsh_flatness_no_go complete")
    print("Artifact: research/representation/self_dual_wreath_regular_master_walsh_flatness_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_source_adaptive_walsh_collision_reduction(subparsers) -> None:
    parser_self_dual_wreath_source_adaptive_walsh_collision_reduction = subparsers.add_parser(
        "self-dual-wreath-source-adaptive-walsh-collision-reduction",
        help="Reduce source-adaptive Walsh routing to an autocorrelation collision bound.",
    )
    parser_self_dual_wreath_source_adaptive_walsh_collision_reduction.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_source_adaptive_walsh_collision_reduction.set_defaults(func=command_self_dual_wreath_source_adaptive_walsh_collision_reduction)


def command_self_dual_wreath_source_adaptive_walsh_collision_reduction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_source_adaptive_walsh_collision_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_source_adaptive_walsh_collision_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_source_adaptive_walsh_collision_report()
    validation = validate_registry()
    print("self_dual_wreath_source_adaptive_walsh_collision_reduction complete")
    print("Artifact: research/representation/self_dual_wreath_source_adaptive_walsh_collision_reduction.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_source_block_branch_covariance_boundary(subparsers) -> None:
    parser_self_dual_wreath_source_block_branch_covariance_boundary = subparsers.add_parser(
        "self-dual-wreath-source-block-branch-covariance-boundary",
        help="Branch covariance moves the source block; it is not a sibling compiler.",
    )
    parser_self_dual_wreath_source_block_branch_covariance_boundary.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_source_block_branch_covariance_boundary.set_defaults(func=command_self_dual_wreath_source_block_branch_covariance_boundary)


def command_self_dual_wreath_source_block_branch_covariance_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_source_block_branch_covariance_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_source_block_branch_covariance_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_source_block_branch_covariance_boundary_report()
    validation = validate_registry()
    print("self_dual_wreath_source_block_branch_covariance_boundary complete")
    print("Artifact: research/representation/self_dual_wreath_source_block_branch_covariance_boundary.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_source_order_gauge_canonicalization(subparsers) -> None:
    parser_self_dual_wreath_source_order_gauge_canonicalization = subparsers.add_parser(
        "self-dual-wreath-source-order-gauge-canonicalization",
        help="Coherent source-pair sorting removes order gauge, not orientation structure.",
    )
    parser_self_dual_wreath_source_order_gauge_canonicalization.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_source_order_gauge_canonicalization.set_defaults(func=command_self_dual_wreath_source_order_gauge_canonicalization)


def command_self_dual_wreath_source_order_gauge_canonicalization(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_source_order_gauge_canonicalization_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_source_order_gauge_canonicalization_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_source_order_gauge_canonicalization_report()
    validation = validate_registry()
    print("self_dual_wreath_source_order_gauge_canonicalization complete")
    print("Artifact: research/representation/self_dual_wreath_source_order_gauge_canonicalization.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_trace_biased_adaptive_walsh_no_go(subparsers) -> None:
    parser_self_dual_wreath_trace_biased_adaptive_walsh_no_go = subparsers.add_parser(
        "self-dual-wreath-trace-biased-adaptive-walsh-no-go",
        help="Reject source-adaptive sparse Walsh routing under the physical block law.",
    )
    parser_self_dual_wreath_trace_biased_adaptive_walsh_no_go.add_argument("--no-registry", action="store_true")
    parser_self_dual_wreath_trace_biased_adaptive_walsh_no_go.set_defaults(func=command_self_dual_wreath_trace_biased_adaptive_walsh_no_go)


def command_self_dual_wreath_trace_biased_adaptive_walsh_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_trace_biased_adaptive_walsh_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_trace_biased_adaptive_walsh_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_trace_biased_adaptive_walsh_report()
    validation = validate_registry()
    print("self_dual_wreath_trace_biased_adaptive_walsh_no_go complete")
    print("Artifact: research/representation/self_dual_wreath_trace_biased_adaptive_walsh_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_plancherel_mass_extinction_barrier(subparsers) -> None:
    self_dual_wreath_plancherel_mass_extinction_barrier = subparsers.add_parser(
        "self-dual-wreath-plancherel-mass-extinction-barrier",
        help="Run wreath product sign-orbit Plancherel mass extinction barrier, Euler self-conjugacy, and Racah CMI collapse audit.",
    )
    self_dual_wreath_plancherel_mass_extinction_barrier.add_argument("--no-registry", action="store_true")
    self_dual_wreath_plancherel_mass_extinction_barrier.set_defaults(func=command_self_dual_wreath_plancherel_mass_extinction_barrier)


def command_self_dual_wreath_plancherel_mass_extinction_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.self_dual_wreath_plancherel_mass_extinction_barrier import REPORT, write_report
    write_report(write_registry=not getattr(args, "no_registry", False))
    validation = validate_registry()
    print("self_dual_wreath_plancherel_mass_extinction_barrier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_self_dual_wreath_naimark_compressed_permutation_barrier(subparsers) -> None:
    self_dual_wreath_naimark_compressed_permutation_barrier = subparsers.add_parser(
        "self-dual-wreath-naimark-compressed-permutation-barrier",
        help="Run uniform harmonic Naimark dilation, Young branching reciprocity, and compressed permutation multiplicity barrier audit.",
    )
    self_dual_wreath_naimark_compressed_permutation_barrier.add_argument("--no-registry", action="store_true")
    self_dual_wreath_naimark_compressed_permutation_barrier.set_defaults(func=command_self_dual_wreath_naimark_compressed_permutation_barrier)


def command_self_dual_wreath_naimark_compressed_permutation_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    import json
    from theorems.self_dual_wreath_naimark_compressed_permutation_barrier import REPORT, build_report, register_negative_result
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    if not getattr(args, "no_registry", False):
        register_negative_result()
    validation = validate_registry()
    print("self_dual_wreath_naimark_compressed_permutation_barrier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1
