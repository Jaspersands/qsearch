"""Nonabelian coset and hidden-subgroup subcommands, moved out of qsearch.py by tools/split_cli/migrate.py.

Each ``add_*`` function registers one subcommand and each ``command_*`` function runs one.
A command imports what it needs from ``qsearch`` when it runs, so loading this module stays
cheap and ``monkeypatch.setattr(qsearch, name, ...)`` still reaches the command.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path



def add_coset_state(subparsers) -> None:
    coset_state = subparsers.add_parser("coset-state", help="Run coset-state/nonabelian HSP graph-pair audits.")
    coset_state.add_argument("--pairs", default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cycle-vs-chorded-cycle")
    coset_state.add_argument("--no-registry", action="store_true")
    coset_state.set_defaults(func=command_coset_state)


def command_coset_state(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_coset_workbench
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_coset_workbench(pair_ids=pair_ids, write_registry=not args.no_registry)
    validation = validate_registry()
    print("Coset-state/nonabelian HSP workbench complete")
    print("Artifact: research/coset_workbench/nonabelian_hsp_audit.json")
    print(f"Pair audits: {len(payload['pair_audits'])}")
    print(f"Summary: {payload['summary']}")
    print(f"Falsifiers triggered: {len(payload['falsifiers_triggered'])}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_triage(subparsers) -> None:
    coset_triage = subparsers.add_parser(
        "coset-triage",
        help="Aggregate coset frontier rows across WL, tensor, individualization, and CFI structural baselines.",
    )
    coset_triage.add_argument("--no-registry", action="store_true")
    coset_triage.add_argument("--verbose", action="store_true")
    coset_triage.set_defaults(func=command_coset_triage)


def command_coset_triage(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_coset_frontier_triage
    initialize_seed_registry(overwrite=False)
    payload = write_coset_frontier_triage(write_registry=not args.no_registry)
    validation = validate_registry()
    print("Coset frontier triage complete")
    print("Artifact: research/coset_workbench/coset_frontier_triage.json")
    print(f"Rows: {payload['headline_metrics']['record_count']}")
    print(f"Rejected rows: {payload['headline_metrics']['rejected_pair_count']}")
    print(f"Proof-debt rows: {payload['headline_metrics']['proof_debt_pair_count']}")
    print(f"Survivor rows: {payload['headline_metrics']['survivor_pair_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(f"- {record['pair_id']} | {record['final_status']} | evidence={len(record['evidence'])}")
            for item in record["evidence"][:6]:
                print(f"  {item['source']} | {item['status']} | {item['verdict']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_distinguishability(subparsers) -> None:
    coset_distinguishability = subparsers.add_parser(
        "coset-distinguishability",
        help="Audit multi-copy distinguishability obligations for symmetric-group involution coset states.",
    )
    coset_distinguishability.add_argument("--n-values", default="6,8,10,12,14,16")
    coset_distinguishability.add_argument("--no-registry", action="store_true")
    coset_distinguishability.add_argument("--verbose", action="store_true")
    coset_distinguishability.set_defaults(func=command_coset_distinguishability)


def command_coset_distinguishability(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_coset_distinguishability_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = parse_int_csv(args.n_values)
    payload = write_coset_distinguishability_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Coset-state distinguishability audit complete")
    print("Artifact: research/representation/coset_state_distinguishability.json")
    print(f"Records: {payload['headline_metrics']['record_count']}")
    print(f"Copy-debt rows: {payload['headline_metrics']['copy_debt_count']}")
    print(f"Max Holevo copy lower bound: {payload['headline_metrics']['max_holevo_copy_lower_bound']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- S_{record['n']} {record['involution_type']} M≈2^{record['log2_ensemble_size']:.2f} | "
                f"{record['status']} | holevo>={record['holevo_copy_lower_bound']} "
                f"overlap2<={record['copies_for_pairwise_overlap_below_inverse_square']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_pgm(subparsers) -> None:
    coset_pgm = subparsers.add_parser(
        "coset-pgm",
        help="Audit PGM copy/capacity obligations for symmetric-group involution coset states.",
    )
    coset_pgm.add_argument("--n-values", default="6,8,10,12,14,16")
    coset_pgm.add_argument("--epsilon", type=float, default=0.1)
    coset_pgm.add_argument("--no-registry", action="store_true")
    coset_pgm.add_argument("--verbose", action="store_true")
    coset_pgm.set_defaults(func=command_coset_pgm)


def command_coset_pgm(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_coset_pgm_capacity_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = parse_int_csv(args.n_values)
    payload = write_coset_pgm_capacity_report(
        n_values=n_values,
        epsilon=args.epsilon,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Coset PGM capacity audit complete")
    print("Artifact: research/representation/coset_pgm_capacity.json")
    print(f"Records: {payload['headline_metrics']['record_count']}")
    print(f"Measurement proof debt: {payload['headline_metrics']['measurement_proof_debt_count']}")
    print(f"Max threshold copies: {payload['headline_metrics']['max_cross_mass_threshold_copies']}")
    print(f"Max register bits at threshold: {payload['headline_metrics']['max_register_bits_at_threshold']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- S_{record['n']} {record['involution_type']} M≈2^{record['log2_ensemble_size']:.2f} | "
                f"{record['status']} | cross<=1 copies={record['copies_for_overlap_cross_mass_below_one']} "
                f"explicit-PGM-log2={record['explicit_pgm_matrix_log2_entries']:.2f}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_holevo(subparsers) -> None:
    coset_holevo = subparsers.add_parser(
        "coset-holevo",
        help="Compute exact one-copy Holevo information and rigorous multi-copy decoding lower bounds.",
    )
    coset_holevo.add_argument("--n-values", default="6,8,10,12,14,16,20")
    coset_holevo.add_argument("--error", type=float, default=1 / 3)
    coset_holevo.add_argument("--no-registry", action="store_true")
    coset_holevo.add_argument("--verbose", action="store_true")
    coset_holevo.set_defaults(func=command_coset_holevo)


def command_coset_holevo(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_coset_holevo_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = parse_int_csv(args.n_values)
    payload = write_coset_holevo_report(
        n_values=n_values,
        error=args.error,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Coset exact Holevo-information audit complete")
    print("Artifact: research/representation/coset_holevo_information.json")
    print(f"Exact Holevo rows: {metrics['exact_holevo_formula_count']}")
    print(
        "Hard-family one-copy Holevo range: "
        f"{metrics['minimum_hard_family_one_copy_holevo_bits']:.6g}-"
        f"{metrics['maximum_hard_family_one_copy_holevo_bits']:.6g} bits"
    )
    print(
        "Maximum hard-family zero/bounded-error copy lower bounds: "
        f"{metrics['maximum_hard_family_zero_error_copy_lower_bound']}/"
        f"{metrics['maximum_hard_family_bounded_error_copy_lower_bound']}"
    )
    print(f"Collective measurements: {metrics['polynomial_collective_measurement_count']}")
    print(f"Outcome decoders: {metrics['polynomial_outcome_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- S_{record['n']} {record['involution_type']} chi={record['exact_one_copy_holevo_bits']:.6g} "
                f"zero/bounded copies={record['zero_error_copy_lower_bound']}/"
                f"{record['bounded_error_copy_lower_bound']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_covariant_frame(subparsers) -> None:
    coset_covariant_frame = subparsers.add_parser(
        "coset-covariant-frame",
        help="Diagonalize one-copy involution class frames and isolate multi-copy decoder debt.",
    )
    coset_covariant_frame.add_argument("--n-values", default="6,8,10,12,14,16")
    coset_covariant_frame.add_argument("--no-registry", action="store_true")
    coset_covariant_frame.set_defaults(func=command_coset_covariant_frame)


def command_coset_covariant_frame(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_covariant_frame_report
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_covariant_frame_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Symmetric-group covariant coset frame theorem complete")
    print("Artifact: research/representation/coset_covariant_frame.json")
    print(f"Frame spectra/single-copy PGM formulas: {metrics['exact_central_frame_spectrum_count']}/{metrics['exact_single_copy_pgm_formula_count']}")
    print(f"Maximum frontier one-copy PGM advantage: {metrics['maximum_frontier_one_copy_pgm_advantage']:.6g}")
    print(f"Multi-copy proof-debt rows: {metrics['multi_copy_diagonal_action_proof_debt_count']}")
    print(f"Efficient multi-copy circuits: {metrics['efficient_multi_copy_diagonal_action_circuit_count']}")
    print(f"Polynomial outcome decoders: {metrics['polynomial_outcome_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_two_copy_frame(subparsers) -> None:
    coset_two_copy_frame = subparsers.add_parser(
        "coset-two-copy-frame",
        help="Diagonalize the two-copy average frame and expose the missing Kronecker transition algebra.",
    )
    coset_two_copy_frame.add_argument("--n-values", default="4,5,6,7,8")
    coset_two_copy_frame.add_argument("--no-registry", action="store_true")
    coset_two_copy_frame.set_defaults(func=command_coset_two_copy_frame)


def command_coset_two_copy_frame(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_two_copy_frame_report
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_two_copy_frame_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    control = payload["noncommutation_control"]
    print("Symmetric-group two-copy frame obstruction complete")
    print("Artifact: research/representation/coset_two_copy_frame.json")
    print(f"Exact frame spectra: {metrics['exact_two_copy_recoupling_spectrum_count']}")
    print(f"Rigorous PGM spectral bounds: {metrics['spectral_pgm_bound_count']}")
    print(f"Exact PGM formulas from spectrum: {metrics['exact_two_copy_pgm_formula_count']}")
    print(f"S_3 frame/state commutator norm: {control['commutator_frobenius_norm']:.6g}")
    print(f"S_3 rank-formula gap: {control['absolute_formula_gap']:.6g}")
    print(f"Rank formula falsified: {control['rank_formula_falsified']}")
    print(f"Transition/transform proof-debt rows: {metrics['coherent_kronecker_transform_proof_debt_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_same_hidden_target_law(subparsers) -> None:
    coset_same_hidden_target_law = subparsers.add_parser(
        "coset-same-hidden-target-law",
        help=(
            "Derive the exact coupled-irrep target law for two states "
            "carrying the same hidden involution."
        ),
    )
    coset_same_hidden_target_law.add_argument(
        "--n-values",
        default="5,6,8,9,10",
    )
    coset_same_hidden_target_law.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_same_hidden_target_law.set_defaults(
        func=command_coset_same_hidden_target_law
    )


def command_coset_same_hidden_target_law(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_same_hidden_target_law_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(
        int(value.strip())
        for value in args.n_values.split(",")
        if value.strip()
    )
    payload = write_same_hidden_target_law_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Same-hidden-involution target law complete")
    print(
        "Artifact: research/representation/"
        "coset_same_hidden_target_law.json"
    )
    print(
        "Exact normalized controls: "
        f"{metrics['exact_normalization_verified_record_count']}/"
        f"{metrics['same_hidden_target_law_record_count']}"
    )
    print(
        "Maximum expected TV from dimension coupling: "
        f"{metrics['maximum_expected_conditional_tv_from_dimension_coupling']:.6g}"
    )
    print(
        "Maximum exact-collision target mass: "
        f"{metrics['maximum_scalar_collision_target_joint_mass']:.6g}"
    )
    print(
        "Coherent target measurements: "
        f"{metrics['coherent_kronecker_target_measurement_theorem_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_commutant_information_no_go(subparsers) -> None:
    coset_commutant_information = subparsers.add_parser(
        "coset-commutant-information-no-go",
        help=(
            "Prove that diagonal-action commutant outcomes carry zero "
            "information about the individual hidden involution."
        ),
    )
    coset_commutant_information.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_commutant_information.set_defaults(
        func=command_coset_commutant_information_obstruction
    )


def command_coset_commutant_information_obstruction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_commutant_information_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_commutant_information_obstruction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Commutant-only information obstruction complete")
    print(
        "Artifact: research/representation/"
        "coset_commutant_information_obstruction.json"
    )
    print(
        "All-k zero-information theorems: "
        f"{metrics['general_all_k_commutant_zero_information_theorem_count']}"
    )
    print(
        "Finite invariant controls: "
        f"{metrics['finite_commutant_distribution_invariance_verified_count']}/"
        f"{metrics['finite_control_count']}"
    )
    print(
        "Maximum commutant outcome TV: "
        f"{metrics['maximum_finite_commutant_outcome_total_variation']:.6g}"
    )
    print(
        "Carrier-sensitive escape witnesses: "
        f"{metrics['finite_noncommutant_escape_witness_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_carrier_information(subparsers) -> None:
    coset_carrier_information = subparsers.add_parser(
        "coset-carrier-information",
        help=(
            "Search carrier-sensitive YJM-plus-separator measurements by "
            "hidden-involution information and compare strong Fourier."
        ),
    )
    coset_carrier_information.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_carrier_information.set_defaults(
        func=command_coset_carrier_information_audit
    )


def command_coset_carrier_information_audit(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_carrier_information_audit_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_carrier_information_audit_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Carrier-sensitive information audit complete")
    print(
        "Artifact: research/representation/"
        "coset_carrier_information_audit.json"
    )
    print(
        "Searched separator rules: "
        f"{metrics['coefficient_vector_count']}"
    )
    print(
        "Controls dominated by product strong Fourier: "
        f"{metrics['product_strong_fourier_dominates_all_searched_rules_count']}/"
        f"{metrics['finite_control_count']}"
    )
    print(
        "Maximum searched joint information: "
        f"{metrics['maximum_best_joint_mutual_information_bits']:.6g} bits"
    )
    print(
        "Maximum product-basis information: "
        f"{metrics['maximum_product_young_basis_mutual_information_bits']:.6g} bits"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_natural_multicopy_pgm(subparsers) -> None:
    coset_natural_multicopy_pgm = subparsers.add_parser(
        "coset-natural-multicopy-pgm",
        help=(
            "Benchmark exact natural-source global carrier PGMs against "
            "product PGMs and separate strong Fourier measurements."
        ),
    )
    coset_natural_multicopy_pgm.add_argument("--n", type=int, default=5)
    coset_natural_multicopy_pgm.add_argument(
        "--transposition-count",
        type=int,
        default=2,
    )
    coset_natural_multicopy_pgm.add_argument(
        "--copy-counts",
        default="1,2,3",
    )
    coset_natural_multicopy_pgm.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_natural_multicopy_pgm.set_defaults(
        func=command_coset_natural_multicopy_pgm
    )


def command_coset_natural_multicopy_pgm(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_multicopy_pgm_report,
    )
    initialize_seed_registry(overwrite=False)
    copy_counts = tuple(
        int(value.strip())
        for value in args.copy_counts.split(",")
        if value.strip()
    )
    payload = write_natural_multicopy_pgm_report(
        n=args.n,
        transposition_count=args.transposition_count,
        copy_counts=copy_counts,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Natural-input multi-copy carrier PGM benchmark complete")
    print(
        "Artifact: research/representation/"
        "coset_natural_multicopy_pgm_benchmark.json"
    )
    print(
        "Finite collective information-gain rows: "
        f"{metrics['finite_collective_information_gain_row_count']}"
    )
    print(
        "Maximum gain over product PGM: "
        f"{metrics['maximum_global_information_gain_over_product_pgm_bits']:.6g} bits"
    )
    print(
        "Maximum gain over separate Young basis: "
        f"{metrics['maximum_global_information_gain_over_separate_young_bits']:.6g} bits"
    )
    print(
        "Scalable PGM circuits/decoders: "
        f"{metrics['uniform_polynomial_global_pgm_circuit_count']}/"
        f"{metrics['polynomial_hidden_involution_decoder_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_pgm_gain_localization(subparsers) -> None:
    coset_pgm_gain_localization = subparsers.add_parser(
        "coset-pgm-gain-localization",
        help=(
            "Localize natural collective-PGM gain across source branches and "
            "audit average-frame condition and inverse-root spectra."
        ),
    )
    coset_pgm_gain_localization.add_argument("--n", type=int, default=5)
    coset_pgm_gain_localization.add_argument(
        "--transposition-count",
        type=int,
        default=2,
    )
    coset_pgm_gain_localization.add_argument(
        "--copy-count",
        type=int,
        default=3,
    )
    coset_pgm_gain_localization.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_pgm_gain_localization.set_defaults(
        func=command_coset_pgm_gain_localization
    )


def command_coset_pgm_gain_localization(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pgm_gain_localization_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pgm_gain_localization_report(
        n=args.n,
        transposition_count=args.transposition_count,
        copy_count=args.copy_count,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Natural PGM gain localization complete")
    print(
        "Artifact: research/representation/"
        "coset_pgm_gain_localization.json"
    )
    print(
        "Positive branches/source mass: "
        f"{metrics['positive_information_gain_branch_count']}/"
        f"{metrics['positive_gain_natural_source_probability']:.6g}"
    )
    print(
        "80% gain branch count/source mass: "
        f"{metrics['gain_80_percent_branch_count']}/"
        f"{metrics['gain_80_percent_natural_source_probability']:.6g}"
    )
    print(
        "Maximum frame condition/interpolation degree: "
        f"{metrics['maximum_frame_condition_number']:.6g}/"
        f"{metrics['maximum_exact_inverse_root_interpolation_degree_upper_bound']}"
    )
    print(
        "Uniform harmonic frame encodings: "
        f"{metrics['uniform_harmonic_average_frame_block_encoding_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_pgm_average_frame(subparsers) -> None:
    coset_pgm_average_frame = subparsers.add_parser(
        "coset-pgm-average-frame",
        help=(
            "Prove the all-k average-frame subset identity and audit direct "
            "projected-LCU normalization at growing entanglement width."
        ),
    )
    coset_pgm_average_frame.add_argument("--n", type=int, default=5)
    coset_pgm_average_frame.add_argument(
        "--transposition-count",
        type=int,
        default=2,
    )
    coset_pgm_average_frame.add_argument(
        "--copy-count",
        type=int,
        default=3,
    )
    coset_pgm_average_frame.add_argument(
        "--scaling-n-values",
        default="8,16,32,64",
    )
    coset_pgm_average_frame.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_pgm_average_frame.set_defaults(
        func=command_coset_pgm_average_frame
    )


def command_coset_pgm_average_frame(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_average_frame_block_encoding_report,
    )
    initialize_seed_registry(overwrite=False)
    scaling_n_values = tuple(
        int(value.strip())
        for value in args.scaling_n_values.split(",")
        if value.strip()
    )
    payload = write_average_frame_block_encoding_report(
        n=args.n,
        transposition_count=args.transposition_count,
        copy_count=args.copy_count,
        scaling_n_values=scaling_n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Coset PGM average-frame block-encoding audit complete")
    print(
        "Artifact: research/representation/"
        "coset_pgm_average_frame_block_encoding.json"
    )
    print(
        "Subset/LCU finite failures: "
        f"{metrics['finite_subset_expansion_failure_count']}/"
        f"{metrics['finite_projected_lcu_failure_count']}"
    )
    print(
        "Conditional superpolynomial amplification rows: "
        f"{metrics['conditional_superpolynomial_generic_amplification_row_count']}/"
        f"{metrics['scaling_record_count']}"
    )
    print(
        "Tail generic sqrt-amplification log2 bound: "
        f"{metrics['tail_log2_generic_sqrt_amplification_lower_bound']:.6g}"
    )
    print(
        "Structured amplifiers/decoders: "
        f"{metrics['polynomial_structured_spectral_amplification_count']}/"
        f"{metrics['polynomial_hidden_involution_decoder_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_character_ratios(subparsers) -> None:
    coset_character_ratios = subparsers.add_parser(
        "coset-character-ratios",
        help=(
            "Prove natural weak-Fourier character-ratio concentration across "
            "growing-width involution source tuples."
        ),
    )
    coset_character_ratios.add_argument(
        "--finite-n-values",
        default="6,8,10,12,14,16",
    )
    coset_character_ratios.add_argument(
        "--scaling-n-values",
        default="8,16,32,64,128",
    )
    coset_character_ratios.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_character_ratios.set_defaults(
        func=command_coset_character_ratios
    )


def command_coset_character_ratios(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_character_ratio_concentration_report,
    )
    initialize_seed_registry(overwrite=False)
    finite_n_values = tuple(
        int(value.strip())
        for value in args.finite_n_values.split(",")
        if value.strip()
    )
    scaling_n_values = tuple(
        int(value.strip())
        for value in args.scaling_n_values.split(",")
        if value.strip()
    )
    payload = write_natural_character_ratio_concentration_report(
        finite_n_values=finite_n_values,
        scaling_n_values=scaling_n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Natural-source character-ratio concentration complete")
    print(
        "Artifact: research/representation/"
        "coset_natural_character_ratio_concentration.json"
    )
    print(
        "Moment/source-mass failures: "
        f"{metrics['finite_column_orthogonality_failure_count']}/"
        f"{metrics['finite_natural_source_mass_failure_count']}"
    )
    print(
        "Inverse-polynomial tuple-envelope rows: "
        f"{metrics['inverse_polynomial_tuple_envelope_row_count']}/"
        f"{metrics['scaling_record_count']}"
    )
    print(
        "Tail tuple failure log2 upper bound: "
        f"{metrics['tail_tuple_failure_log2_upper_bound']:.6g}"
    )
    print(
        "PGM circuits/decoders: "
        f"{metrics['pgm_measurement_circuit_count']}/"
        f"{metrics['polynomial_hidden_involution_decoder_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_projector_subpovm(subparsers) -> None:
    coset_projector_subpovm = subparsers.add_parser(
        "coset-projector-subpovm",
        help=(
            "Audit a whitening-free covariant projector sub-POVM whose "
            "conclusive rate depends on frame condition, not absolute scale."
        ),
    )
    coset_projector_subpovm.add_argument("--n", type=int, default=5)
    coset_projector_subpovm.add_argument(
        "--transposition-count",
        type=int,
        default=2,
    )
    coset_projector_subpovm.add_argument(
        "--copy-counts",
        default="1,2,3",
    )
    coset_projector_subpovm.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_projector_subpovm.set_defaults(
        func=command_coset_projector_subpovm
    )


def command_coset_projector_subpovm(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_covariant_projector_subpovm_report,
    )
    initialize_seed_registry(overwrite=False)
    copy_counts = tuple(
        int(value.strip())
        for value in args.copy_counts.split(",")
        if value.strip()
    )
    payload = write_covariant_projector_subpovm_report(
        n=args.n,
        transposition_count=args.transposition_count,
        copy_counts=copy_counts,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Whitening-free covariant projector sub-POVM audit complete")
    print(
        "Artifact: research/representation/"
        "coset_covariant_projector_subpovm.json"
    )
    print(
        "Tail information/conclusive probability: "
        f"{metrics['tail_subpovm_mutual_information_bits']:.6g}/"
        f"{metrics['tail_subpovm_conclusive_probability']:.6g}"
    )
    print(
        "Tail gain over product PGM: "
        f"{metrics['tail_subpovm_information_gain_over_product_pgm_bits']:.6g} bits"
    )
    print(
        "Uniform circuits/compressed outcomes/decoders: "
        f"{metrics['uniform_covariant_natural_subpovm_circuit_count']}/"
        f"{metrics['compressed_hidden_label_outcome_count']}/"
        f"{metrics['polynomial_hidden_involution_decoder_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_hidden_involution_binary_identification_self_reduction(subparsers) -> None:
    parser_coset_hidden_involution_binary_identification_self_reduction = subparsers.add_parser(
        "coset-hidden-involution-binary-identification-self-reduction",
        help="Run Coset Hidden Involution Binary Identification Self Reduction.",
    )
    parser_coset_hidden_involution_binary_identification_self_reduction.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_binary_identification_self_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_binary_identification_self_reduction.set_defaults(func=command_coset_hidden_involution_binary_identification_self_reduction)


def command_coset_hidden_involution_binary_identification_self_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_binary_identification_self_reduction_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_binary_identification_self_reduction_report(output_path=output_path)
        else:
            payload = write_binary_identification_self_reduction_report()
    except TypeError:
        payload = write_binary_identification_self_reduction_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_branch_erasure_normalization_no_go(subparsers) -> None:
    parser_coset_hidden_involution_branch_erasure_normalization_no_go = subparsers.add_parser(
        "coset-hidden-involution-branch-erasure-normalization-no-go",
        help="Run Coset Hidden Involution Branch Erasure Normalization No Go.",
    )
    parser_coset_hidden_involution_branch_erasure_normalization_no_go.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_branch_erasure_normalization_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_branch_erasure_normalization_no_go.set_defaults(func=command_coset_hidden_involution_branch_erasure_normalization_no_go)


def command_coset_hidden_involution_branch_erasure_normalization_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_branch_erasure_normalization_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_branch_erasure_normalization_report(output_path=output_path)
        else:
            payload = write_branch_erasure_normalization_report()
    except TypeError:
        payload = write_branch_erasure_normalization_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_bulk_conditioning_normalization_no_go(subparsers) -> None:
    parser_coset_hidden_involution_bulk_conditioning_normalization_no_go = subparsers.add_parser(
        "coset-hidden-involution-bulk-conditioning-normalization-no-go",
        help="Run Coset Hidden Involution Bulk Conditioning Normalization No Go.",
    )
    parser_coset_hidden_involution_bulk_conditioning_normalization_no_go.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_bulk_conditioning_normalization_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_bulk_conditioning_normalization_no_go.set_defaults(func=command_coset_hidden_involution_bulk_conditioning_normalization_no_go)


def command_coset_hidden_involution_bulk_conditioning_normalization_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_bulk_conditioning_normalization_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_bulk_conditioning_normalization_report(output_path=output_path)
        else:
            payload = write_bulk_conditioning_normalization_report()
    except TypeError:
        payload = write_bulk_conditioning_normalization_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_common_factor_trim(subparsers) -> None:
    parser_coset_hidden_involution_common_factor_trim = subparsers.add_parser(
        "coset-hidden-involution-common-factor-trim",
        help="Run Coset Hidden Involution Common Factor Trim.",
    )
    parser_coset_hidden_involution_common_factor_trim.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_common_factor_trim.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_common_factor_trim.set_defaults(func=command_coset_hidden_involution_common_factor_trim)


def command_coset_hidden_involution_common_factor_trim(args: argparse.Namespace) -> int:
    from qsearch import write_common_factor_trim_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_common_factor_trim_report(output_path=output_path)
        else:
            payload = write_common_factor_trim_report()
    except TypeError:
        payload = write_common_factor_trim_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_common_outlier_deflation(subparsers) -> None:
    parser_coset_hidden_involution_common_outlier_deflation = subparsers.add_parser(
        "coset-hidden-involution-common-outlier-deflation",
        help="Run Coset Hidden Involution Common Outlier Deflation.",
    )
    parser_coset_hidden_involution_common_outlier_deflation.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_common_outlier_deflation.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_common_outlier_deflation.set_defaults(func=command_coset_hidden_involution_common_outlier_deflation)


def command_coset_hidden_involution_common_outlier_deflation(args: argparse.Namespace) -> int:
    from qsearch import write_common_outlier_deflation_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_common_outlier_deflation_report(output_path=output_path)
        else:
            payload = write_common_outlier_deflation_report()
    except TypeError:
        payload = write_common_outlier_deflation_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_foulkes_support_mass_probe(subparsers) -> None:
    parser_coset_hidden_involution_foulkes_support_mass_probe = subparsers.add_parser(
        "coset-hidden-involution-foulkes-support-mass-probe",
        help="Run Coset Hidden Involution Foulkes Support Mass Probe.",
    )
    parser_coset_hidden_involution_foulkes_support_mass_probe.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_foulkes_support_mass_probe.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_foulkes_support_mass_probe.set_defaults(func=command_coset_hidden_involution_foulkes_support_mass_probe)


def command_coset_hidden_involution_foulkes_support_mass_probe(args: argparse.Namespace) -> int:
    from qsearch import write_foulkes_support_mass_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_foulkes_support_mass_report(output_path=output_path)
        else:
            payload = write_foulkes_support_mass_report()
    except TypeError:
        payload = write_foulkes_support_mass_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_foulkes_support_projector_no_go(subparsers) -> None:
    parser_coset_hidden_involution_foulkes_support_projector_no_go = subparsers.add_parser(
        "coset-hidden-involution-foulkes-support-projector-no-go",
        help="Run Coset Hidden Involution Foulkes Support Projector No Go.",
    )
    parser_coset_hidden_involution_foulkes_support_projector_no_go.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_foulkes_support_projector_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_foulkes_support_projector_no_go.set_defaults(func=command_coset_hidden_involution_foulkes_support_projector_no_go)


def command_coset_hidden_involution_foulkes_support_projector_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_foulkes_support_projector_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_foulkes_support_projector_report(output_path=output_path)
        else:
            payload = write_foulkes_support_projector_report()
    except TypeError:
        payload = write_foulkes_support_projector_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_fourier_coefficient_normalization_no_go(subparsers) -> None:
    parser_coset_hidden_involution_fourier_coefficient_normalization_no_go = subparsers.add_parser(
        "coset-hidden-involution-fourier-coefficient-normalization-no-go",
        help="Run Coset Hidden Involution Fourier Coefficient Normalization No Go.",
    )
    parser_coset_hidden_involution_fourier_coefficient_normalization_no_go.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_fourier_coefficient_normalization_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_fourier_coefficient_normalization_no_go.set_defaults(func=command_coset_hidden_involution_fourier_coefficient_normalization_no_go)


def command_coset_hidden_involution_fourier_coefficient_normalization_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_fourier_coefficient_normalization_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_fourier_coefficient_normalization_report(output_path=output_path)
        else:
            payload = write_fourier_coefficient_normalization_report()
    except TypeError:
        payload = write_fourier_coefficient_normalization_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_imprimitive_plethysm_boundary(subparsers) -> None:
    parser_coset_hidden_involution_imprimitive_plethysm_boundary = subparsers.add_parser(
        "coset-hidden-involution-imprimitive-plethysm-boundary",
        help="Run Coset Hidden Involution Imprimitive Plethysm Boundary.",
    )
    parser_coset_hidden_involution_imprimitive_plethysm_boundary.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_imprimitive_plethysm_boundary.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_imprimitive_plethysm_boundary.set_defaults(func=command_coset_hidden_involution_imprimitive_plethysm_boundary)


def command_coset_hidden_involution_imprimitive_plethysm_boundary(args: argparse.Namespace) -> int:
    from qsearch import write_imprimitive_plethysm_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_imprimitive_plethysm_report(output_path=output_path)
        else:
            payload = write_imprimitive_plethysm_report()
    except TypeError:
        payload = write_imprimitive_plethysm_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_incidence_walk_boundary(subparsers) -> None:
    parser_coset_hidden_involution_incidence_walk_boundary = subparsers.add_parser(
        "coset-hidden-involution-incidence-walk-boundary",
        help="Run Coset Hidden Involution Incidence Walk Boundary.",
    )
    parser_coset_hidden_involution_incidence_walk_boundary.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_incidence_walk_boundary.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_incidence_walk_boundary.set_defaults(func=command_coset_hidden_involution_incidence_walk_boundary)


def command_coset_hidden_involution_incidence_walk_boundary(args: argparse.Namespace) -> int:
    from qsearch import write_incidence_walk_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_incidence_walk_report(output_path=output_path)
        else:
            payload = write_incidence_walk_report()
    except TypeError:
        payload = write_incidence_walk_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_induced_source_bundle_reduction(subparsers) -> None:
    parser_coset_hidden_involution_induced_source_bundle_reduction = subparsers.add_parser(
        "coset-hidden-involution-induced-source-bundle-reduction",
        help="Run Coset Hidden Involution Induced Source Bundle Reduction.",
    )
    parser_coset_hidden_involution_induced_source_bundle_reduction.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_induced_source_bundle_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_induced_source_bundle_reduction.set_defaults(func=command_coset_hidden_involution_induced_source_bundle_reduction)


def command_coset_hidden_involution_induced_source_bundle_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_induced_source_bundle_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_induced_source_bundle_report(output_path=output_path)
        else:
            payload = write_induced_source_bundle_report()
    except TypeError:
        payload = write_induced_source_bundle_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_isotypic_support_no_go(subparsers) -> None:
    parser_coset_hidden_involution_isotypic_support_no_go = subparsers.add_parser(
        "coset-hidden-involution-isotypic-support-no-go",
        help="Run Coset Hidden Involution Isotypic Support No Go.",
    )
    parser_coset_hidden_involution_isotypic_support_no_go.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_isotypic_support_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_isotypic_support_no_go.set_defaults(func=command_coset_hidden_involution_isotypic_support_no_go)


def command_coset_hidden_involution_isotypic_support_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_isotypic_support_no_go_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_isotypic_support_no_go_report(output_path=output_path)
        else:
            payload = write_isotypic_support_no_go_report()
    except TypeError:
        payload = write_isotypic_support_no_go_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_matrix_hecke_transfer_reduction(subparsers) -> None:
    parser_coset_hidden_involution_matrix_hecke_transfer_reduction = subparsers.add_parser(
        "coset-hidden-involution-matrix-hecke-transfer-reduction",
        help="Run Coset Hidden Involution Matrix Hecke Transfer Reduction.",
    )
    parser_coset_hidden_involution_matrix_hecke_transfer_reduction.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_matrix_hecke_transfer_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_matrix_hecke_transfer_reduction.set_defaults(func=command_coset_hidden_involution_matrix_hecke_transfer_reduction)


def command_coset_hidden_involution_matrix_hecke_transfer_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_matrix_hecke_transfer_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_matrix_hecke_transfer_report(output_path=output_path)
        else:
            payload = write_matrix_hecke_transfer_report()
    except TypeError:
        payload = write_matrix_hecke_transfer_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_multiplicity_hard_mass(subparsers) -> None:
    parser_coset_hidden_involution_multiplicity_hard_mass = subparsers.add_parser(
        "coset-hidden-involution-multiplicity-hard-mass",
        help="Run Coset Hidden Involution Multiplicity Hard Mass.",
    )
    parser_coset_hidden_involution_multiplicity_hard_mass.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_multiplicity_hard_mass.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_multiplicity_hard_mass.set_defaults(func=command_coset_hidden_involution_multiplicity_hard_mass)


def command_coset_hidden_involution_multiplicity_hard_mass(args: argparse.Namespace) -> int:
    from qsearch import write_multiplicity_hard_mass_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_multiplicity_hard_mass_report(output_path=output_path)
        else:
            payload = write_multiplicity_hard_mass_report()
    except TypeError:
        payload = write_multiplicity_hard_mass_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_orbit_synthesis_flatness(subparsers) -> None:
    parser_coset_hidden_involution_orbit_synthesis_flatness = subparsers.add_parser(
        "coset-hidden-involution-orbit-synthesis-flatness",
        help="Run Coset Hidden Involution Orbit Synthesis Flatness.",
    )
    parser_coset_hidden_involution_orbit_synthesis_flatness.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_orbit_synthesis_flatness.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_orbit_synthesis_flatness.set_defaults(func=command_coset_hidden_involution_orbit_synthesis_flatness)


def command_coset_hidden_involution_orbit_synthesis_flatness(args: argparse.Namespace) -> int:
    from qsearch import write_orbit_synthesis_flatness_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_orbit_synthesis_flatness_report(output_path=output_path)
        else:
            payload = write_orbit_synthesis_flatness_report()
    except TypeError:
        payload = write_orbit_synthesis_flatness_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_pair_polar_holonomy_no_go(subparsers) -> None:
    parser_coset_hidden_involution_pair_polar_holonomy_no_go = subparsers.add_parser(
        "coset-hidden-involution-pair-polar-holonomy-no-go",
        help="Run Coset Hidden Involution Pair Polar Holonomy No Go.",
    )
    parser_coset_hidden_involution_pair_polar_holonomy_no_go.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_pair_polar_holonomy_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_pair_polar_holonomy_no_go.set_defaults(func=command_coset_hidden_involution_pair_polar_holonomy_no_go)


def command_coset_hidden_involution_pair_polar_holonomy_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_pair_polar_holonomy_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_pair_polar_holonomy_report(output_path=output_path)
        else:
            payload = write_pair_polar_holonomy_report()
    except TypeError:
        payload = write_pair_polar_holonomy_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_pair_polar_phase_compiler(subparsers) -> None:
    parser_coset_hidden_involution_pair_polar_phase_compiler = subparsers.add_parser(
        "coset-hidden-involution-pair-polar-phase-compiler",
        help="Run Coset Hidden Involution Pair Polar Phase Compiler.",
    )
    parser_coset_hidden_involution_pair_polar_phase_compiler.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_pair_polar_phase_compiler.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_pair_polar_phase_compiler.set_defaults(func=command_coset_hidden_involution_pair_polar_phase_compiler)


def command_coset_hidden_involution_pair_polar_phase_compiler(args: argparse.Namespace) -> int:
    from qsearch import write_pair_polar_phase_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_pair_polar_phase_report(output_path=output_path)
        else:
            payload = write_pair_polar_phase_report()
    except TypeError:
        payload = write_pair_polar_phase_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_regular_orbit_row_reduction(subparsers) -> None:
    parser_coset_hidden_involution_regular_orbit_row_reduction = subparsers.add_parser(
        "coset-hidden-involution-regular-orbit-row-reduction",
        help="Run Coset Hidden Involution Regular Orbit Row Reduction.",
    )
    parser_coset_hidden_involution_regular_orbit_row_reduction.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_regular_orbit_row_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_regular_orbit_row_reduction.set_defaults(func=command_coset_hidden_involution_regular_orbit_row_reduction)


def command_coset_hidden_involution_regular_orbit_row_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_regular_orbit_row_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_regular_orbit_row_report(output_path=output_path)
        else:
            payload = write_regular_orbit_row_report()
    except TypeError:
        payload = write_regular_orbit_row_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_rigid_gi_bridge(subparsers) -> None:
    parser_coset_hidden_involution_rigid_gi_bridge = subparsers.add_parser(
        "coset-hidden-involution-rigid-gi-bridge",
        help="Run Coset Hidden Involution Rigid Gi Bridge.",
    )
    parser_coset_hidden_involution_rigid_gi_bridge.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_rigid_gi_bridge.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_rigid_gi_bridge.set_defaults(func=command_coset_hidden_involution_rigid_gi_bridge)


def command_coset_hidden_involution_rigid_gi_bridge(args: argparse.Namespace) -> int:
    from qsearch import write_rigid_gi_hidden_involution_bridge_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_rigid_gi_hidden_involution_bridge_report(output_path=output_path)
        else:
            payload = write_rigid_gi_hidden_involution_bridge_report()
    except TypeError:
        payload = write_rigid_gi_hidden_involution_bridge_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_s3_chart_gram_compiler(subparsers) -> None:
    parser_coset_hidden_involution_s3_chart_gram_compiler = subparsers.add_parser(
        "coset-hidden-involution-s3-chart-gram-compiler",
        help="Run Coset Hidden Involution S3 Chart Gram Compiler.",
    )
    parser_coset_hidden_involution_s3_chart_gram_compiler.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_s3_chart_gram_compiler.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_s3_chart_gram_compiler.set_defaults(func=command_coset_hidden_involution_s3_chart_gram_compiler)


def command_coset_hidden_involution_s3_chart_gram_compiler(args: argparse.Namespace) -> int:
    from qsearch import write_s3_chart_gram_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_s3_chart_gram_report(output_path=output_path)
        else:
            payload = write_s3_chart_gram_report()
    except TypeError:
        payload = write_s3_chart_gram_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_source_deflation_no_go(subparsers) -> None:
    parser_coset_hidden_involution_source_deflation_no_go = subparsers.add_parser(
        "coset-hidden-involution-source-deflation-no-go",
        help="Run Coset Hidden Involution Source Deflation No Go.",
    )
    parser_coset_hidden_involution_source_deflation_no_go.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_source_deflation_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_source_deflation_no_go.set_defaults(func=command_coset_hidden_involution_source_deflation_no_go)


def command_coset_hidden_involution_source_deflation_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_source_deflation_no_go_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_source_deflation_no_go_report(output_path=output_path)
        else:
            payload = write_source_deflation_no_go_report()
    except TypeError:
        payload = write_source_deflation_no_go_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_spherical_outlier_deflation(subparsers) -> None:
    parser_coset_hidden_involution_spherical_outlier_deflation = subparsers.add_parser(
        "coset-hidden-involution-spherical-outlier-deflation",
        help="Run Coset Hidden Involution Spherical Outlier Deflation.",
    )
    parser_coset_hidden_involution_spherical_outlier_deflation.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_spherical_outlier_deflation.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_spherical_outlier_deflation.set_defaults(func=command_coset_hidden_involution_spherical_outlier_deflation)


def command_coset_hidden_involution_spherical_outlier_deflation(args: argparse.Namespace) -> int:
    from qsearch import write_spherical_outlier_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_spherical_outlier_report(output_path=output_path)
        else:
            payload = write_spherical_outlier_report()
    except TypeError:
        payload = write_spherical_outlier_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_subgroup_outlier_hierarchy(subparsers) -> None:
    parser_coset_hidden_involution_subgroup_outlier_hierarchy = subparsers.add_parser(
        "coset-hidden-involution-subgroup-outlier-hierarchy",
        help="Run Coset Hidden Involution Subgroup Outlier Hierarchy.",
    )
    parser_coset_hidden_involution_subgroup_outlier_hierarchy.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_subgroup_outlier_hierarchy.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_subgroup_outlier_hierarchy.set_defaults(func=command_coset_hidden_involution_subgroup_outlier_hierarchy)


def command_coset_hidden_involution_subgroup_outlier_hierarchy(args: argparse.Namespace) -> int:
    from qsearch import write_subgroup_outlier_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_subgroup_outlier_report(output_path=output_path)
        else:
            payload = write_subgroup_outlier_report()
    except TypeError:
        payload = write_subgroup_outlier_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hidden_involution_subgroup_support_dichotomy(subparsers) -> None:
    parser_coset_hidden_involution_subgroup_support_dichotomy = subparsers.add_parser(
        "coset-hidden-involution-subgroup-support-dichotomy",
        help="Run Coset Hidden Involution Subgroup Support Dichotomy.",
    )
    parser_coset_hidden_involution_subgroup_support_dichotomy.add_argument("--output", help="Optional report output path")
    parser_coset_hidden_involution_subgroup_support_dichotomy.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hidden_involution_subgroup_support_dichotomy.set_defaults(func=command_coset_hidden_involution_subgroup_support_dichotomy)


def command_coset_hidden_involution_subgroup_support_dichotomy(args: argparse.Namespace) -> int:
    from qsearch import write_subgroup_support_dichotomy_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_subgroup_support_dichotomy_report(output_path=output_path)
        else:
            payload = write_subgroup_support_dichotomy_report()
    except TypeError:
        payload = write_subgroup_support_dichotomy_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hyperoctahedral_cg_kronecker_reduction(subparsers) -> None:
    parser_coset_hyperoctahedral_cg_kronecker_reduction = subparsers.add_parser(
        "coset-hyperoctahedral-cg-kronecker-reduction",
        help="Run Coset Hyperoctahedral Cg Kronecker Reduction.",
    )
    parser_coset_hyperoctahedral_cg_kronecker_reduction.add_argument("--output", help="Optional report output path")
    parser_coset_hyperoctahedral_cg_kronecker_reduction.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hyperoctahedral_cg_kronecker_reduction.set_defaults(func=command_coset_hyperoctahedral_cg_kronecker_reduction)


def command_coset_hyperoctahedral_cg_kronecker_reduction(args: argparse.Namespace) -> int:
    from qsearch import write_hyperoctahedral_cg_kronecker_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_hyperoctahedral_cg_kronecker_report(output_path=output_path)
        else:
            payload = write_hyperoctahedral_cg_kronecker_report()
    except TypeError:
        payload = write_hyperoctahedral_cg_kronecker_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hyperoctahedral_color_weight_concentration(subparsers) -> None:
    parser_coset_hyperoctahedral_color_weight_concentration = subparsers.add_parser(
        "coset-hyperoctahedral-color-weight-concentration",
        help="Run Coset Hyperoctahedral Color Weight Concentration.",
    )
    parser_coset_hyperoctahedral_color_weight_concentration.add_argument("--output", help="Optional report output path")
    parser_coset_hyperoctahedral_color_weight_concentration.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hyperoctahedral_color_weight_concentration.set_defaults(func=command_coset_hyperoctahedral_color_weight_concentration)


def command_coset_hyperoctahedral_color_weight_concentration(args: argparse.Namespace) -> int:
    from qsearch import write_color_weight_concentration_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_color_weight_concentration_report(output_path=output_path)
        else:
            payload = write_color_weight_concentration_report()
    except TypeError:
        payload = write_color_weight_concentration_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hyperoctahedral_free_orbit_canonicalization_boundary(subparsers) -> None:
    parser_coset_hyperoctahedral_free_orbit_canonicalization_boundary = subparsers.add_parser(
        "coset-hyperoctahedral-free-orbit-canonicalization-boundary",
        help="Run Coset Hyperoctahedral Free Orbit Canonicalization Boundary.",
    )
    parser_coset_hyperoctahedral_free_orbit_canonicalization_boundary.add_argument("--output", help="Optional report output path")
    parser_coset_hyperoctahedral_free_orbit_canonicalization_boundary.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hyperoctahedral_free_orbit_canonicalization_boundary.set_defaults(func=command_coset_hyperoctahedral_free_orbit_canonicalization_boundary)


def command_coset_hyperoctahedral_free_orbit_canonicalization_boundary(args: argparse.Namespace) -> int:
    from qsearch import write_free_orbit_canonicalization_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_free_orbit_canonicalization_report(output_path=output_path)
        else:
            payload = write_free_orbit_canonicalization_report()
    except TypeError:
        payload = write_free_orbit_canonicalization_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hyperoctahedral_source_plancherel_typicality(subparsers) -> None:
    parser_coset_hyperoctahedral_source_plancherel_typicality = subparsers.add_parser(
        "coset-hyperoctahedral-source-plancherel-typicality",
        help="Run Coset Hyperoctahedral Source Plancherel Typicality.",
    )
    parser_coset_hyperoctahedral_source_plancherel_typicality.add_argument("--output", help="Optional report output path")
    parser_coset_hyperoctahedral_source_plancherel_typicality.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hyperoctahedral_source_plancherel_typicality.set_defaults(func=command_coset_hyperoctahedral_source_plancherel_typicality)


def command_coset_hyperoctahedral_source_plancherel_typicality(args: argparse.Namespace) -> int:
    from qsearch import write_source_plancherel_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_source_plancherel_report(output_path=output_path)
        else:
            payload = write_source_plancherel_report()
    except TypeError:
        payload = write_source_plancherel_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hyperoctahedral_trimmed_orbit_canonicalizer(subparsers) -> None:
    parser_coset_hyperoctahedral_trimmed_orbit_canonicalizer = subparsers.add_parser(
        "coset-hyperoctahedral-trimmed-orbit-canonicalizer",
        help="Run Coset Hyperoctahedral Trimmed Orbit Canonicalizer.",
    )
    parser_coset_hyperoctahedral_trimmed_orbit_canonicalizer.add_argument("--output", help="Optional report output path")
    parser_coset_hyperoctahedral_trimmed_orbit_canonicalizer.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hyperoctahedral_trimmed_orbit_canonicalizer.set_defaults(func=command_coset_hyperoctahedral_trimmed_orbit_canonicalizer)


def command_coset_hyperoctahedral_trimmed_orbit_canonicalizer(args: argparse.Namespace) -> int:
    from qsearch import write_trimmed_canonicalizer_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_trimmed_canonicalizer_report(output_path=output_path)
        else:
            payload = write_trimmed_canonicalizer_report()
    except TypeError:
        payload = write_trimmed_canonicalizer_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_hyperoctahedral_trivial_color_mass_no_go(subparsers) -> None:
    parser_coset_hyperoctahedral_trivial_color_mass_no_go = subparsers.add_parser(
        "coset-hyperoctahedral-trivial-color-mass-no-go",
        help="Run Coset Hyperoctahedral Trivial Color Mass No Go.",
    )
    parser_coset_hyperoctahedral_trivial_color_mass_no_go.add_argument("--output", help="Optional report output path")
    parser_coset_hyperoctahedral_trivial_color_mass_no_go.add_argument("--no-write", action="store_true", help="Skip writing report to disk")
    parser_coset_hyperoctahedral_trivial_color_mass_no_go.set_defaults(func=command_coset_hyperoctahedral_trivial_color_mass_no_go)


def command_coset_hyperoctahedral_trivial_color_mass_no_go(args: argparse.Namespace) -> int:
    from qsearch import write_trivial_color_mass_report
    output_path = Path(args.output) if args.output else None
    try:
        if output_path:
            payload = write_trivial_color_mass_report(output_path=output_path)
        else:
            payload = write_trivial_color_mass_report()
    except TypeError:
        payload = write_trivial_color_mass_report()
    print(payload.get("summary", "Done"))
    return 0


def add_coset_arbitrary_covariant_measurement_reduction(subparsers) -> None:
    coset_arbitrary_covariant_measurement_reduction = subparsers.add_parser(
        "coset-arbitrary-covariant-measurement-reduction",
        help="Exp Coset Arbitrary Covariant Measurement Reduction",
    )
    coset_arbitrary_covariant_measurement_reduction.set_defaults(func=command_coset_arbitrary_covariant_measurement_reduction)


def command_coset_arbitrary_covariant_measurement_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_arbitrary_covariant_measurement_reduction
    report = write_arbitrary_covariant_measurement_reduction()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_centralizer_whitening_rank_bound(subparsers) -> None:
    coset_centralizer_whitening_rank_bound = subparsers.add_parser(
        "coset-centralizer-whitening-rank-bound",
        help="Exp Coset Centralizer Whitening Rank Bound",
    )
    coset_centralizer_whitening_rank_bound.set_defaults(func=command_coset_centralizer_whitening_rank_bound)


def command_coset_centralizer_whitening_rank_bound(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_centralizer_whitening_rank_report
    report = write_coset_centralizer_whitening_rank_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_covariant_measurement_multiplicity_width_no_go(subparsers) -> None:
    coset_covariant_measurement_multiplicity_width_no_go = subparsers.add_parser(
        "coset-covariant-measurement-multiplicity-width-no-go",
        help="Exp Coset Covariant Measurement Multiplicity Width No Go",
    )
    coset_covariant_measurement_multiplicity_width_no_go.set_defaults(func=command_coset_covariant_measurement_multiplicity_width_no_go)


def command_coset_covariant_measurement_multiplicity_width_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        validate_registry,
        write_coset_covariant_measurement_multiplicity_width_report,
    )
    report = write_coset_covariant_measurement_multiplicity_width_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_covariant_multiplicity_whitening_escape(subparsers) -> None:
    coset_covariant_multiplicity_whitening_escape = subparsers.add_parser(
        "coset-covariant-multiplicity-whitening-escape",
        help="Exp Coset Covariant Multiplicity Whitening Escape",
    )
    coset_covariant_multiplicity_whitening_escape.set_defaults(func=command_coset_covariant_multiplicity_whitening_escape)


def command_coset_covariant_multiplicity_whitening_escape(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_covariant_multiplicity_whitening_report
    report = write_coset_covariant_multiplicity_whitening_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_gelfand_row_orientation_no_go(subparsers) -> None:
    coset_gelfand_row_orientation_no_go = subparsers.add_parser(
        "coset-gelfand-row-orientation-no-go",
        help="Exp Coset Gelfand Row Orientation No Go",
    )
    coset_gelfand_row_orientation_no_go.set_defaults(func=command_coset_gelfand_row_orientation_no_go)


def command_coset_gelfand_row_orientation_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_gelfand_row_orientation_no_go
    report = write_gelfand_row_orientation_no_go()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_hidden_involution_binary_decision_reduction(subparsers) -> None:
    coset_hidden_involution_binary_decision_reduction = subparsers.add_parser(
        "coset-hidden-involution-binary-decision-reduction",
        help="Exp Coset Hidden Involution Binary Decision Reduction",
    )
    coset_hidden_involution_binary_decision_reduction.set_defaults(func=command_coset_hidden_involution_binary_decision_reduction)


def command_coset_hidden_involution_binary_decision_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_hidden_involution_binary_decision_report
    report = write_hidden_involution_binary_decision_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_hidden_involution_fourth_moment_threshold(subparsers) -> None:
    coset_hidden_involution_fourth_moment_threshold = subparsers.add_parser(
        "coset-hidden-involution-fourth-moment-threshold",
        help="Exp Coset Hidden Involution Fourth Moment Threshold",
    )
    coset_hidden_involution_fourth_moment_threshold.set_defaults(func=command_coset_hidden_involution_fourth_moment_threshold)


def command_coset_hidden_involution_fourth_moment_threshold(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_hidden_involution_fourth_moment_report
    report = write_hidden_involution_fourth_moment_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_hidden_involution_multiplicity_support_obstruction(subparsers) -> None:
    coset_hidden_involution_multiplicity_support_obstruction = subparsers.add_parser(
        "coset-hidden-involution-multiplicity-support-obstruction",
        help="Exp Coset Hidden Involution Multiplicity Support Obstruction",
    )
    coset_hidden_involution_multiplicity_support_obstruction.set_defaults(func=command_coset_hidden_involution_multiplicity_support_obstruction)


def command_coset_hidden_involution_multiplicity_support_obstruction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_multiplicity_support_obstruction_report
    report = write_multiplicity_support_obstruction_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_hidden_involution_orbit_hull_twirl_reduction(subparsers) -> None:
    coset_hidden_involution_orbit_hull_twirl_reduction = subparsers.add_parser(
        "coset-hidden-involution-orbit-hull-twirl-reduction",
        help="Exp Coset Hidden Involution Orbit Hull Twirl Reduction",
    )
    coset_hidden_involution_orbit_hull_twirl_reduction.set_defaults(func=command_coset_hidden_involution_orbit_hull_twirl_reduction)


def command_coset_hidden_involution_orbit_hull_twirl_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_hidden_involution_orbit_hull_report
    report = write_hidden_involution_orbit_hull_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_hidden_involution_query_separation_boundary(subparsers) -> None:
    coset_hidden_involution_query_separation_boundary = subparsers.add_parser(
        "coset-hidden-involution-query-separation-boundary",
        help="Exp Coset Hidden Involution Query Separation Boundary",
    )
    coset_hidden_involution_query_separation_boundary.set_defaults(func=command_coset_hidden_involution_query_separation_boundary)


def command_coset_hidden_involution_query_separation_boundary(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_hidden_involution_query_separation_report
    report = write_hidden_involution_query_separation_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_hidden_involution_support_span_reduction(subparsers) -> None:
    coset_hidden_involution_support_span_reduction = subparsers.add_parser(
        "coset-hidden-involution-support-span-reduction",
        help="Exp Coset Hidden Involution Support Span Reduction",
    )
    coset_hidden_involution_support_span_reduction.set_defaults(func=command_coset_hidden_involution_support_span_reduction)


def command_coset_hidden_involution_support_span_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_hidden_involution_support_span_report
    report = write_hidden_involution_support_span_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_hidden_involution_threshold_compiler_boundary(subparsers) -> None:
    coset_hidden_involution_threshold_compiler_boundary = subparsers.add_parser(
        "coset-hidden-involution-threshold-compiler-boundary",
        help="Exp Coset Hidden Involution Threshold Compiler Boundary",
    )
    coset_hidden_involution_threshold_compiler_boundary.set_defaults(func=command_coset_hidden_involution_threshold_compiler_boundary)


def command_coset_hidden_involution_threshold_compiler_boundary(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_hidden_involution_threshold_compiler_report
    report = write_hidden_involution_threshold_compiler_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_hyperoctahedral_branching_polar_boundary(subparsers) -> None:
    coset_hyperoctahedral_branching_polar_boundary = subparsers.add_parser(
        "coset-hyperoctahedral-branching-polar-boundary",
        help="Exp Coset Hyperoctahedral Branching Polar Boundary",
    )
    coset_hyperoctahedral_branching_polar_boundary.set_defaults(func=command_coset_hyperoctahedral_branching_polar_boundary)


def command_coset_hyperoctahedral_branching_polar_boundary(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_hyperoctahedral_branching_polar_report
    report = write_coset_hyperoctahedral_branching_polar_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_kronecker_marginal_conservation(subparsers) -> None:
    coset_kronecker_marginal_conservation = subparsers.add_parser(
        "coset-kronecker-marginal-conservation",
        help="Exp Coset Kronecker Marginal Conservation",
    )
    coset_kronecker_marginal_conservation.set_defaults(func=command_coset_kronecker_marginal_conservation)


def command_coset_kronecker_marginal_conservation(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_kronecker_marginal_conservation_report
    report = write_kronecker_marginal_conservation_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_measurement_copy_width_whitening_tradeoff(subparsers) -> None:
    coset_measurement_copy_width_whitening_tradeoff = subparsers.add_parser(
        "coset-measurement-copy-width-whitening-tradeoff",
        help="Exp Coset Measurement Copy Width Whitening Tradeoff",
    )
    coset_measurement_copy_width_whitening_tradeoff.set_defaults(func=command_coset_measurement_copy_width_whitening_tradeoff)


def command_coset_measurement_copy_width_whitening_tradeoff(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_measurement_copy_width_whitening_report
    report = write_coset_measurement_copy_width_whitening_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_multiplicity_whitening_copy_window(subparsers) -> None:
    coset_multiplicity_whitening_copy_window = subparsers.add_parser(
        "coset-multiplicity-whitening-copy-window",
        help="Exp Coset Multiplicity Whitening Copy Window",
    )
    coset_multiplicity_whitening_copy_window.set_defaults(func=command_coset_multiplicity_whitening_copy_window)


def command_coset_multiplicity_whitening_copy_window(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_multiplicity_whitening_copy_window_report
    report = write_coset_multiplicity_whitening_copy_window_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_perfect_matching_spherical_boundary(subparsers) -> None:
    coset_perfect_matching_spherical_boundary = subparsers.add_parser(
        "coset-perfect-matching-spherical-boundary",
        help="Exp Coset Perfect Matching Spherical Boundary",
    )
    coset_perfect_matching_spherical_boundary.set_defaults(func=command_coset_perfect_matching_spherical_boundary)


def command_coset_perfect_matching_spherical_boundary(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_perfect_matching_spherical_boundary
    report = write_perfect_matching_spherical_boundary()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_prefix_polar_holonomy_reduction(subparsers) -> None:
    coset_prefix_polar_holonomy_reduction = subparsers.add_parser(
        "coset-prefix-polar-holonomy-reduction",
        help="Exp Coset Prefix Polar Holonomy Reduction",
    )
    coset_prefix_polar_holonomy_reduction.set_defaults(func=command_coset_prefix_polar_holonomy_reduction)


def command_coset_prefix_polar_holonomy_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_prefix_polar_holonomy_report
    report = write_coset_prefix_polar_holonomy_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_prefix_relative_gap_inference_no_go(subparsers) -> None:
    coset_prefix_relative_gap_inference_no_go = subparsers.add_parser(
        "coset-prefix-relative-gap-inference-no-go",
        help="Exp Coset Prefix Relative Gap Inference No Go",
    )
    coset_prefix_relative_gap_inference_no_go.set_defaults(func=command_coset_prefix_relative_gap_inference_no_go)


def command_coset_prefix_relative_gap_inference_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_prefix_relative_gap_inference_report
    report = write_coset_prefix_relative_gap_inference_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_restriction_principal_angle_polar_reduction(subparsers) -> None:
    coset_restriction_principal_angle_polar_reduction = subparsers.add_parser(
        "coset-restriction-principal-angle-polar-reduction",
        help="Exp Coset Restriction Principal Angle Polar Reduction",
    )
    coset_restriction_principal_angle_polar_reduction.set_defaults(func=command_coset_restriction_principal_angle_polar_reduction)


def command_coset_restriction_principal_angle_polar_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_restriction_principal_angle_polar_report
    report = write_coset_restriction_principal_angle_polar_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_sector_coherence_degree_no_go(subparsers) -> None:
    coset_sector_coherence_degree_no_go = subparsers.add_parser(
        "coset-sector-coherence-degree-no-go",
        help="Exp Coset Sector Coherence Degree No Go",
    )
    coset_sector_coherence_degree_no_go.set_defaults(func=command_coset_sector_coherence_degree_no_go)


def command_coset_sector_coherence_degree_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_sector_coherence_degree_no_go_report
    report = write_sector_coherence_degree_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_source_weighted_frame_inversion_tradeoff(subparsers) -> None:
    coset_source_weighted_frame_inversion_tradeoff = subparsers.add_parser(
        "coset-source-weighted-frame-inversion-tradeoff",
        help="Exp Coset Source Weighted Frame Inversion Tradeoff",
    )
    coset_source_weighted_frame_inversion_tradeoff.set_defaults(func=command_coset_source_weighted_frame_inversion_tradeoff)


def command_coset_source_weighted_frame_inversion_tradeoff(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_source_weighted_frame_inversion_report
    report = write_coset_source_weighted_frame_inversion_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_whitening_rank_sandwich_no_go(subparsers) -> None:
    coset_whitening_rank_sandwich_no_go = subparsers.add_parser(
        "coset-whitening-rank-sandwich-no-go",
        help="Exp Coset Whitening Rank Sandwich No Go",
    )
    coset_whitening_rank_sandwich_no_go.set_defaults(func=command_coset_whitening_rank_sandwich_no_go)


def command_coset_whitening_rank_sandwich_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_coset_whitening_rank_sandwich_report
    report = write_coset_whitening_rank_sandwich_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_hidden_involution_support_filter_no_go(subparsers) -> None:
    coset_hidden_involution_support_filter_no_go = subparsers.add_parser(
        "coset-hidden-involution-support-filter-no-go",
        help="Exp Coset Hidden Involution Support Filter No Go",
    )
    coset_hidden_involution_support_filter_no_go.set_defaults(func=command_coset_hidden_involution_support_filter_no_go)


def command_coset_hidden_involution_support_filter_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_support_filter_no_go_report
    report = write_support_filter_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_coset_strong_fourier_information(subparsers) -> None:
    coset_strong_fourier_information = subparsers.add_parser(
        "coset-strong-fourier-information",
        help=(
            "Measure naturally weighted one- and two-copy Young-basis strong "
            "Fourier information across complete involution classes."
        ),
    )
    coset_strong_fourier_information.add_argument(
        "--n-values",
        default="3,4,5,6,7,8",
    )
    coset_strong_fourier_information.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_strong_fourier_information.set_defaults(
        func=command_coset_strong_fourier_information
    )


def command_coset_strong_fourier_information(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_strong_fourier_information_scaling_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(
        int(value.strip())
        for value in args.n_values.split(",")
        if value.strip()
    )
    payload = write_strong_fourier_information_scaling_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Natural strong Fourier information scaling complete")
    print(
        "Artifact: research/representation/"
        "coset_strong_fourier_information_scaling.json"
    )
    print(
        "Weak-label zero-information controls: "
        f"{metrics['weak_label_zero_information_verified_count']}/"
        f"{metrics['record_count']}"
    )
    print(
        "Largest-n one-copy carrier information: "
        f"{metrics['largest_n_one_copy_carrier_mutual_information_bits']:.6g} bits"
    )
    print(
        "Largest-n two-copy carrier information: "
        f"{metrics['largest_n_two_copy_carrier_mutual_information_bits']:.6g} bits"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_entanglement_width(subparsers) -> None:
    coset_entanglement_width = subparsers.add_parser(
        "coset-entanglement-width",
        help=(
            "Apply primary multiregister lower bounds and quarantine "
            "bounded-copy coset mechanisms."
        ),
    )
    coset_entanglement_width.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_entanglement_width.set_defaults(
        func=command_coset_entanglement_width_gate
    )


def command_coset_entanglement_width_gate(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_entanglement_width_gate_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_entanglement_width_gate_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Coset-state entanglement-width gate complete")
    print(
        "Artifact: research/representation/"
        "coset_entanglement_width_gate.json"
    )
    print(
        "Primary no-go theorems: "
        f"{metrics['primary_literature_theorem_count']}"
    )
    print(
        "Bounded-register mechanisms quarantined: "
        f"{metrics['bounded_register_mechanism_count']}"
    )
    print(
        "Maximum current joint register width: "
        f"{metrics['maximum_current_joint_register_count']}"
    )
    print(
        "Growing-width architectures: "
        f"{metrics['growing_entanglement_width_architecture_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_growing_width_architecture(subparsers) -> None:
    coset_growing_width = subparsers.add_parser(
        "coset-growing-width-architecture",
        help=(
            "Type-check growing-copy measurement DAGs against width, "
            "carrier, covariance, information, and decoder obligations."
        ),
    )
    coset_growing_width.add_argument(
        "--no-registry",
        action="store_true",
    )
    coset_growing_width.set_defaults(
        func=command_coset_growing_width_architecture
    )


def command_coset_growing_width_architecture(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_growing_width_architecture_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_growing_width_architecture_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Growing-width coset architecture compiler complete")
    print(
        "Artifact: research/representation/"
        "coset_growing_width_architecture.json"
    )
    print(
        "Structurally compliant architectures: "
        f"{metrics['structurally_compliant_architecture_count']}/"
        f"{metrics['architecture_count']}"
    )
    print(
        "Proof-complete architectures: "
        f"{metrics['proof_complete_architecture_count']}"
    )
    print(
        "Blocking proof issues: "
        f"{metrics['blocking_proof_issue_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_two_copy_transitions(subparsers) -> None:
    coset_two_copy_transitions = subparsers.add_parser(
        "coset-two-copy-transitions",
        help="Measure finite cross-sector transition weights and reject factorial explicit tables.",
    )
    coset_two_copy_transitions.add_argument("--n-values", default="3,4")
    coset_two_copy_transitions.add_argument("--no-registry", action="store_true")
    coset_two_copy_transitions.set_defaults(func=command_coset_two_copy_transitions)


def command_coset_two_copy_transitions(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_two_copy_transition_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_two_copy_transition_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Two-copy transition-algebra audit complete")
    print("Artifact: research/representation/coset_two_copy_transition_audit.json")
    print(f"Verified spectra: {metrics['spectrum_verified_count']}/{metrics['record_count']}")
    print(f"Noncommuting classes: {metrics['noncommuting_frame_count']}")
    print(f"Commuting controls: {metrics['commuting_class_control_count']}")
    print(f"Rank-formula falsifications: {metrics['rank_formula_falsified_count']}")
    print(f"Maximum off-diagonal PGM fraction: {metrics['maximum_off_diagonal_pgm_contribution_fraction']:.6g}")
    print(f"Largest dense transition representation: {metrics['maximum_dense_matrix_entry_count']} entries")
    print(f"Polynomial transition tables: {metrics['polynomial_transition_table_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_three_copy_recoupling(subparsers) -> None:
    coset_three_copy_recoupling = subparsers.add_parser(
        "coset-three-copy-recoupling",
        help="Prove the overlapping pair-class-sum obstruction and isolate associator proof debt.",
    )
    coset_three_copy_recoupling.add_argument("--n-values", default="3,4,5,6,7")
    coset_three_copy_recoupling.add_argument("--no-registry", action="store_true")
    coset_three_copy_recoupling.set_defaults(func=command_coset_three_copy_recoupling)


def command_coset_three_copy_recoupling(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_three_copy_recoupling_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_three_copy_recoupling_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Three-copy overlapping-recoupling obstruction complete")
    print("Artifact: research/representation/coset_three_copy_recoupling_obstruction.json")
    print(f"All-n transposition theorem rows: {metrics['single_transposition_all_n_theorem_row_count']}")
    print(f"Noncommuting overlapping-pair rows: {metrics['noncommuting_overlapping_pair_count']}")
    print(f"Commuting controls: {metrics['commuting_class_control_count']}")
    print(f"Uniform coherent associators: {metrics['uniform_coherent_associator_count']}")
    print(f"Polynomial multiplicity decoders: {metrics['polynomial_multiplicity_space_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_recoupling_capabilities(subparsers) -> None:
    coset_recoupling_capabilities = subparsers.add_parser(
        "coset-recoupling-capabilities",
        help="Separate solved QFT/projection primitives from open internal recoupling and decoding.",
    )
    coset_recoupling_capabilities.add_argument("--n-values", default="4,5,6,7,8,9,10")
    coset_recoupling_capabilities.add_argument("--no-registry", action="store_true")
    coset_recoupling_capabilities.set_defaults(func=command_coset_recoupling_capabilities)


def command_coset_recoupling_capabilities(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_recoupling_capability_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_recoupling_capability_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Symmetric-group recoupling capability ledger complete")
    print("Artifact: research/representation/coset_recoupling_capability_ledger.json")
    print(f"Proved polynomial primitives: {metrics['proved_polynomial_primitive_count']}/{metrics['capability_count']}")
    print(f"Internal Kronecker transform proofs: {metrics['internal_kronecker_transform_poly_proof_count']}")
    print(f"Growing-k associator proofs: {metrics['kcopy_associator_poly_proof_count']}")
    print(f"Hidden-involution decoders: {metrics['hidden_involution_decoder_count']}")
    print(f"Restricted classical matches: {metrics['restricted_multiplicity_classical_match_count']}")
    print(f"Maximum finite Kronecker multiplicity: {metrics['maximum_kronecker_multiplicity']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_jm_labels(subparsers) -> None:
    coset_jm_labels = subparsers.add_parser(
        "coset-jm-labels",
        help="Verify the polynomial diagonal YJM label transform and isolate unresolved Kronecker multiplicity space.",
    )
    coset_jm_labels.add_argument("--n-values", default="4,5,6")
    coset_jm_labels.add_argument("--no-registry", action="store_true")
    coset_jm_labels.set_defaults(func=command_coset_jm_labels)


def command_coset_jm_labels(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_jucys_murphy_label_transform_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_jucys_murphy_label_transform_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Diagonal Young--Jucys--Murphy label-transform audit complete")
    print("Artifact: research/representation/coset_jucys_murphy_label_transform.json")
    print(
        "Verified finite label spectra: "
        f"{metrics['finite_label_spectrum_verified_count']}/{metrics['record_count']}"
    )
    print(f"Nontrivial multiplicity witnesses: {metrics['nontrivial_multiplicity_witness_count']}")
    print(f"Polynomial diagonal-label contracts: {metrics['diagonal_jm_label_poly_contract_count']}")
    print(f"Coherent multiplicity bases: {metrics['coherent_multiplicity_basis_count']}")
    print(f"Hidden-involution decoders: {metrics['hidden_involution_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_multiplicity_commutant(subparsers) -> None:
    coset_multiplicity_commutant = subparsers.add_parser(
        "coset-multiplicity-commutant",
        help="Search bounded-support diagonal-action commutants inside Kronecker multiplicity registers.",
    )
    coset_multiplicity_commutant.add_argument("--n-values", default="5,6,7")
    coset_multiplicity_commutant.add_argument("--coefficient-bound", type=int, default=2)
    coset_multiplicity_commutant.add_argument("--no-registry", action="store_true")
    coset_multiplicity_commutant.set_defaults(func=command_coset_multiplicity_commutant)


def command_coset_multiplicity_commutant(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_multiplicity_commutant_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_multiplicity_commutant_report(
        n_values=n_values,
        coefficient_bound=args.coefficient_bound,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Kronecker multiplicity commutant search complete")
    print("Artifact: research/representation/coset_multiplicity_commutant_search.json")
    print(
        "Finite all-block splits: "
        f"{metrics['finite_all_block_split_count']}/{metrics['record_count']}"
    )
    print(f"Maximum audited multiplicity: {metrics['maximum_kronecker_multiplicity']}")
    print(f"Minimum observed normalized gap: {metrics['minimum_observed_lcu_normalized_gap']:.6g}")
    print(f"Inverse-polynomial gap theorems: {metrics['inverse_polynomial_gap_theorem_count']}")
    print(f"Polynomial multiplicity transforms: {metrics['coherent_polynomial_multiplicity_transform_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_commutant_gap_scaling(subparsers) -> None:
    coset_commutant_gap_scaling = subparsers.add_parser(
        "coset-commutant-gap-scaling",
        help="Verify finite scaling of one uniform multiplicity-commutant gap family.",
    )
    coset_commutant_gap_scaling.add_argument("--n-values", default="6,7,8,9,10")
    coset_commutant_gap_scaling.add_argument("--no-registry", action="store_true")
    coset_commutant_gap_scaling.set_defaults(func=command_coset_commutant_gap_scaling)


def command_coset_commutant_gap_scaling(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_commutant_gap_scaling_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_commutant_gap_scaling_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Uniform Kronecker-commutant gap scaling audit complete")
    print("Artifact: research/representation/coset_commutant_gap_scaling.json")
    print(
        "Finite critical-gap matches: "
        f"{metrics['critical_gap_formula_finite_verified_count']}/{metrics['record_count']}"
    )
    print(f"All-n critical-gap theorems: {metrics['all_n_critical_gap_theorem_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_commutant_gap_proof(subparsers) -> None:
    coset_commutant_gap_proof = subparsers.add_parser(
        "coset-commutant-gap-proof",
        help="Build the exact all-n Specht-polytabloid gap certificate.",
    )
    coset_commutant_gap_proof.add_argument("--no-registry", action="store_true")
    coset_commutant_gap_proof.set_defaults(func=command_coset_commutant_gap_proof)


def command_coset_commutant_gap_proof(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_commutant_gap_certificate
    initialize_seed_registry(overwrite=False)
    payload = write_commutant_gap_certificate(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    gap = payload["exact_gap_certificate"]
    print("Exact Kronecker-commutant gap certificate complete")
    print("Artifact: research/representation/coset_commutant_gap_certificate.json")
    print(f"All-n restricted gap theorems: {metrics['all_n_critical_gap_theorem_count']}")
    print(f"Raw gap: {gap['raw_gap']}")
    print(f"LCU-normalized gap: {gap['lcu_normalized_gap']}")
    print(f"General-sector gap theorems: {metrics['general_sector_gap_theorem_count']}")
    print(f"Racah associators: {metrics['kcopy_associator_count']}")
    print(f"Hidden-involution decoders: {metrics['hidden_involution_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_control(subparsers) -> None:
    coset_racah_control = subparsers.add_parser(
        "coset-racah-control",
        help="Resolve finite parity-channel Racah subblocks and measure leakage into other intermediates.",
    )
    coset_racah_control.add_argument("--n", type=int, default=6)
    coset_racah_control.add_argument("--no-registry", action="store_true")
    coset_racah_control.set_defaults(func=command_coset_racah_control)


def command_coset_racah_control(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_restricted_racah_control_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_restricted_racah_control_report(
        n=args.n,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Restricted three-copy Racah control complete")
    print("Artifact: research/representation/coset_restricted_racah_control.json")
    print(f"Tableau-consistent subblocks: {metrics['tableau_consistent_subblock_count']}/{metrics['record_count']}")
    print(f"Channels with leakage: {metrics['channel_leakage_detected_count']}")
    print(f"Full Racah associators: {metrics['full_racah_associator_count']}")
    print(f"Uniform polynomial Racah circuits: {metrics['uniform_polynomial_racah_circuit_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_complete_control(subparsers) -> None:
    coset_racah_complete_control = subparsers.add_parser(
        "coset-racah-complete-control",
        help="Assemble complete finite Racah matrices where second-stage coupling is multiplicity-free.",
    )
    coset_racah_complete_control.add_argument("--n", type=int, default=6)
    coset_racah_complete_control.add_argument("--no-registry", action="store_true")
    coset_racah_complete_control.set_defaults(
        func=command_coset_racah_complete_control
    )


def command_coset_racah_complete_control(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_complete_racah_control_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_complete_racah_control_report(
        n=args.n,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Complete finite three-copy Racah control complete")
    print("Artifact: research/representation/coset_complete_racah_control.json")
    print(
        "Complete finite matrices: "
        f"{metrics['complete_finite_racah_matrix_count']}/"
        f"{metrics['final_target_count']} final sectors"
    )
    print(
        "Nontrivial finite matrices: "
        f"{metrics['nontrivial_complete_finite_racah_matrix_count']}"
    )
    print(
        "Unresolved second-stage multiplicity sectors: "
        f"{metrics['unresolved_second_stage_multiplicity_sector_count']}"
    )
    print(
        "Uniform polynomial Racah circuits: "
        f"{metrics['uniform_polynomial_racah_circuit_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_hierarchical_control(subparsers) -> None:
    coset_racah_hierarchical_control = subparsers.add_parser(
        "coset-racah-hierarchical-control",
        help="Resolve every finite S_6 Racah sector with a two-level bounded-support commutant hierarchy.",
    )
    coset_racah_hierarchical_control.add_argument("--n", type=int, default=6)
    coset_racah_hierarchical_control.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_hierarchical_control.set_defaults(
        func=command_coset_racah_hierarchical_control
    )


def command_coset_racah_hierarchical_control(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hierarchical_racah_control_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_hierarchical_racah_control_report(
        n=args.n,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Hierarchical finite three-copy Racah control complete")
    print("Artifact: research/representation/coset_hierarchical_racah_control.json")
    print(
        "Complete hierarchical matrices: "
        f"{metrics['complete_hierarchical_finite_racah_matrix_count']}/"
        f"{metrics['final_target_count']} final sectors"
    )
    print(
        "Second-stage multiplicity resolved sectors: "
        f"{metrics['second_stage_multiplicity_resolved_sector_count']}"
    )
    print(
        "Minimum observed second-stage normalized gap: "
        f"{metrics['minimum_observed_second_stage_normalized_gap']:.6g}"
    )
    print(f"Stable-n joint-gap theorems: {metrics['stable_n_joint_gap_theorem_count']}")
    print(
        "Uniform polynomial Racah circuits: "
        f"{metrics['uniform_polynomial_racah_circuit_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_gap_scaling(subparsers) -> None:
    coset_racah_gap_scaling = subparsers.add_parser(
        "coset-racah-gap-scaling",
        help="Scale second-stage multiplicity gaps on the stable (n-2,2) three-copy target family.",
    )
    coset_racah_gap_scaling.add_argument("--n-values", default="6,7,8")
    coset_racah_gap_scaling.add_argument("--no-registry", action="store_true")
    coset_racah_gap_scaling.set_defaults(func=command_coset_racah_gap_scaling)


def command_coset_racah_gap_scaling(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_hierarchical_gap_scaling_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = parse_int_csv(args.n_values)
    payload = write_hierarchical_gap_scaling_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Hierarchical Racah gap scaling audit complete")
    print("Artifact: research/representation/coset_hierarchical_gap_scaling.json")
    print(
        "Finite all-block split rows: "
        f"{metrics['finite_all_blocks_split_count']}/{metrics['record_count']}"
    )
    print(f"Maximum second-stage multiplicity: {metrics['maximum_second_stage_multiplicity']}")
    print(f"Minimum normalized gap: {metrics['minimum_observed_normalized_gap']:.6g}")
    print(
        "Empirical log-log gap slope: "
        f"{metrics['empirical_log_log_normalized_gap_slope']:.6g}"
    )
    print(
        "All-n second-stage gap theorems: "
        f"{metrics['all_n_second_stage_gap_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_sparse_gap(subparsers) -> None:
    coset_racah_sparse_gap = subparsers.add_parser(
        "coset-racah-sparse-gap",
        help="Extract the stable multiplicity-four Racah block sparsely and reconstruct integer quartics.",
    )
    coset_racah_sparse_gap.add_argument("--n-values", default="7,8,9,10")
    coset_racah_sparse_gap.add_argument("--no-registry", action="store_true")
    coset_racah_sparse_gap.set_defaults(func=command_coset_racah_sparse_gap)


def command_coset_racah_sparse_gap(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_sparse_stable_gap_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = parse_int_csv(args.n_values)
    payload = write_sparse_stable_gap_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Sparse stable Racah gap probe complete")
    print("Artifact: research/representation/coset_sparse_stable_gap_probe.json")
    print(f"Finite split rows: {metrics['finite_split_count']}/{metrics['record_count']}")
    print(
        "Integer characteristic polynomials: "
        f"{metrics['integer_characteristic_polynomial_candidate_count']}/"
        f"{metrics['record_count']}"
    )
    print(f"Maximum sparse tensor dimension: {metrics['maximum_sparse_tensor_dimension']}")
    print(f"Minimum normalized gap: {metrics['minimum_observed_normalized_gap']:.6g}")
    print(
        "All-n characteristic-polynomial theorems: "
        f"{metrics['all_n_characteristic_polynomial_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_trace_conjecture(subparsers) -> None:
    coset_racah_trace_conjecture = subparsers.add_parser(
        "coset-racah-trace-conjecture",
        help="Generate and hold out-test an exact trace formula target from sparse Racah quartics.",
    )
    coset_racah_trace_conjecture.add_argument("--training-count", type=int, default=4)
    coset_racah_trace_conjecture.add_argument("--no-registry", action="store_true")
    coset_racah_trace_conjecture.set_defaults(
        func=command_coset_racah_trace_conjecture
    )


def command_coset_racah_trace_conjecture(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_trace_conjecture_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_trace_conjecture_report(
        training_count=args.training_count,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah trace conjecture audit complete")
    print("Artifact: research/representation/coset_stable_trace_conjecture.json")
    print(f"Candidate trace formula: {payload['candidate_trace_formula_expanded']}")
    print(
        "Holdout matches: "
        f"{metrics['holdout_match_count']}/{metrics['holdout_row_count']}"
    )
    print(
        "Exact marked-cycle trace theorems: "
        f"{metrics['exact_marked_cycle_trace_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_trace_proof(subparsers) -> None:
    coset_racah_trace_proof = subparsers.add_parser(
        "coset-racah-trace-proof",
        help="Prove the stable Racah trace by exact falling-cycle equality patterns.",
    )
    coset_racah_trace_proof.add_argument("--no-registry", action="store_true")
    coset_racah_trace_proof.set_defaults(func=command_coset_racah_trace_proof)


def command_coset_racah_trace_proof(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_stable_trace_certificate
    initialize_seed_registry(overwrite=False)
    payload = write_stable_trace_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah trace certificate complete")
    print("Artifact: research/representation/coset_stable_trace_certificate.json")
    print(
        "Exact stable trace theorems: "
        f"{metrics['exact_marked_cycle_trace_theorem_count']}"
    )
    print(f"Trace formula: {payload['stable_symbolic_certificate']['trace']}")
    print(
        "Equality patterns: "
        f"{metrics['canonical_equality_pattern_count']} across "
        f"{metrics['falling_monomial_product_count']} monomial products"
    )
    print(f"Full quartic theorems: {metrics['all_n_quartic_theorem_count']}")
    print(
        "Root-separation theorems: "
        f"{metrics['all_n_root_separation_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_second_moment_proof(subparsers) -> None:
    coset_racah_second_moment_proof = subparsers.add_parser(
        "coset-racah-second-moment-proof",
        help="Prove Tr(H^2) and the second stable quartic coefficient by relative orbit classes.",
    )
    coset_racah_second_moment_proof.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_second_moment_proof.set_defaults(
        func=command_coset_racah_second_moment_proof
    )


def command_coset_racah_second_moment_proof(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_second_moment_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_second_moment_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah second-moment certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_second_moment_certificate.json"
    )
    print(
        "Exact second-moment theorems: "
        f"{metrics['exact_second_power_trace_theorem_count']}"
    )
    print(f"Tr(H^2): {payload['theorem']['second_power_trace']}")
    print(
        "Proved quartic coefficients: "
        f"{metrics['proved_quartic_coefficient_count']}/"
        f"{metrics['required_quartic_coefficient_count']}"
    )
    print(f"Relative orbit classes: {metrics['relative_orbit_class_count']}")
    print(
        "Root-separation theorems: "
        f"{metrics['all_n_root_separation_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_third_moment_proof(subparsers) -> None:
    coset_racah_third_moment_proof = subparsers.add_parser(
        "coset-racah-third-moment-proof",
        help="Prove Tr(H^3) and the third stable quartic coefficient by two-relative-term orbit classes.",
    )
    coset_racah_third_moment_proof.add_argument("--workers", type=int, default=None)
    coset_racah_third_moment_proof.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_third_moment_proof.set_defaults(
        func=command_coset_racah_third_moment_proof
    )


def command_coset_racah_third_moment_proof(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_third_moment_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_third_moment_certificate(
        workers=args.workers,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah third-moment certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_third_moment_certificate.json"
    )
    print(
        "Exact third-moment theorems: "
        f"{metrics['exact_third_power_trace_theorem_count']}"
    )
    print(f"Tr(H^3): {payload['theorem']['third_power_trace']}")
    print(
        "Proved quartic coefficients: "
        f"{metrics['proved_quartic_coefficient_count']}/"
        f"{metrics['required_quartic_coefficient_count']}"
    )
    print(f"Relative orbit classes: {metrics['relative_orbit_class_count']}")
    print(
        "Root-separation theorems: "
        f"{metrics['all_n_root_separation_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_fourth_moment_proof(subparsers) -> None:
    coset_racah_fourth_moment_proof = subparsers.add_parser(
        "coset-racah-fourth-moment-proof",
        help="Complete the stable Racah quartic with a resumable exact Tr(H^4) certificate.",
    )
    coset_racah_fourth_moment_proof.add_argument("--workers", type=int, default=None)
    coset_racah_fourth_moment_proof.add_argument("--no-resume", action="store_true")
    coset_racah_fourth_moment_proof.add_argument("--no-registry", action="store_true")
    coset_racah_fourth_moment_proof.set_defaults(
        func=command_coset_racah_fourth_moment_proof
    )


def command_coset_racah_fourth_moment_proof(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_fourth_moment_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_fourth_moment_certificate(
        workers=args.workers,
        resume=not args.no_resume,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah fourth-moment certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_fourth_moment_certificate.json"
    )
    print(f"Tr(H^4): {payload['theorem']['fourth_power_trace']}")
    print(f"Determinant: {payload['theorem']['determinant']}")
    print(
        "Proved quartic coefficients: "
        f"{metrics['proved_quartic_coefficient_count']}/"
        f"{metrics['required_quartic_coefficient_count']}"
    )
    print(f"Relative orbit classes: {metrics['relative_orbit_class_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_root_separation_proof(subparsers) -> None:
    coset_racah_root_separation_proof = subparsers.add_parser(
        "coset-racah-root-separation-proof",
        help="Prove an inverse-polynomial LCU-normalized gap from the exact stable quartic discriminant.",
    )
    coset_racah_root_separation_proof.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_root_separation_proof.set_defaults(
        func=command_coset_racah_root_separation_proof
    )


def command_coset_racah_root_separation_proof(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_root_separation_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_root_separation_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah root-separation certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_root_separation_certificate.json"
    )
    print(
        "Normalized gap lower bound: "
        f"{payload['theorem']['lcu_normalized_gap_lower_bound']}"
    )
    print(
        "Stable root-separation theorems: "
        f"{metrics['stable_channel_root_separation_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_coherent_label_proof(subparsers) -> None:
    coset_racah_coherent_label_proof = subparsers.add_parser(
        "coset-racah-coherent-label-proof",
        help="Certify a uniform coherent eigenlabel transform in one stable multiplicity-four channel.",
    )
    coset_racah_coherent_label_proof.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_coherent_label_proof.set_defaults(
        func=command_coset_racah_coherent_label_proof
    )


def command_coset_racah_coherent_label_proof(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_coherent_label_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_coherent_label_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Scoped stable Racah coherent-label certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_coherent_label_certificate.json"
    )
    print(
        "Stable coherent-label theorems: "
        f"{metrics['uniform_polynomial_stable_multiplicity_label_transform_count']}"
    )
    print(
        "Unrestricted Kronecker/associator/decoder theorems: "
        f"{metrics['unrestricted_internal_kronecker_transform_count']}/"
        f"{metrics['overlapping_racah_associator_count']}/"
        f"{metrics['hidden_involution_decoder_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_transition(subparsers) -> None:
    coset_racah_stable_transition = subparsers.add_parser(
        "coset-racah-stable-transition",
        help="Measure gauge-invariant leakage between left/right stable 2x4 Racah branches.",
    )
    coset_racah_stable_transition.add_argument(
        "--n-values", default="7,8"
    )
    coset_racah_stable_transition.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_transition.set_defaults(
        func=command_coset_racah_stable_transition
    )


def command_coset_racah_stable_transition(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_subspace_transition_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(
        int(value.strip()) for value in args.n_values.split(",") if value.strip()
    )
    payload = write_stable_subspace_transition_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah subspace-transition probe complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_subspace_transition_probe.json"
    )
    print(f"Scaling points: {metrics['stable_scaling_point_count']}")
    print(
        "Minimum leakage: "
        f"{metrics['minimum_maximally_mixed_leakage']:.6f}"
    )
    print(f"Closed stable associators: {metrics['closed_stable_associator_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_complementary_sectors(subparsers) -> None:
    coset_racah_complementary_sectors = subparsers.add_parser(
        "coset-racah-complementary-sectors",
        help="Resolve stable-branch leakage across every character-allowed intermediate sector.",
    )
    coset_racah_complementary_sectors.add_argument(
        "--n-values", default="7,8"
    )
    coset_racah_complementary_sectors.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_complementary_sectors.set_defaults(
        func=command_coset_racah_complementary_sectors
    )


def command_coset_racah_complementary_sectors(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_complementary_sector_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(
        int(value.strip()) for value in args.n_values.split(",") if value.strip()
    )
    payload = write_complementary_sector_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah complementary-sector resolution complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_complementary_sector_probe.json"
    )
    print(f"Scaling points: {metrics['scaling_point_count']}")
    print(
        "Minimum nonzero complementary sectors: "
        f"{metrics['minimum_nonzero_complementary_sector_count']}"
    )
    print(
        "Largest one-sector leakage share: "
        f"{metrics['maximum_single_complementary_leakage_share']:.6f}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_shape_proof(subparsers) -> None:
    coset_racah_stable_shape_proof = subparsers.add_parser(
        "coset-racah-stable-shape-proof",
        help="Prove the exact nine-shape intermediate family by character polynomials.",
    )
    coset_racah_stable_shape_proof.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_shape_proof.set_defaults(
        func=command_coset_racah_stable_shape_proof
    )


def command_coset_racah_stable_shape_proof(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_shape_family_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_shape_family_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah shape-family certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_shape_family_certificate.json"
    )
    print(
        "Stable shape theorems: "
        f"{metrics['exact_stable_shape_family_theorem_count']}"
    )
    print(f"Intermediate shapes: {metrics['stable_intermediate_shape_count']}")
    print(
        "Open nontrivial second-stage label shapes: "
        f"{metrics['unresolved_coherent_second_stage_shape_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_shape_labels(subparsers) -> None:
    coset_racah_stable_shape_labels = subparsers.add_parser(
        "coset-racah-stable-shape-labels",
        help="Probe one uniform bounded-support label Hamiltonian on all nine stable shapes.",
    )
    coset_racah_stable_shape_labels.add_argument(
        "--n-values", default="8,9,10"
    )
    coset_racah_stable_shape_labels.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_shape_labels.set_defaults(
        func=command_coset_racah_stable_shape_labels
    )


def command_coset_racah_stable_shape_labels(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_stable_shape_label_report
    initialize_seed_registry(overwrite=False)
    n_values = tuple(
        int(value.strip()) for value in args.n_values.split(",") if value.strip()
    )
    payload = write_stable_shape_label_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah shape-label spectral probe complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_shape_label_probe.json"
    )
    print(f"Audited nontrivial blocks: {metrics['finite_nontrivial_block_count']}")
    print(
        "Fully split finite blocks: "
        f"{metrics['finite_fully_split_nontrivial_block_count']}"
    )
    print(
        "Unproved shape theorem targets: "
        f"{metrics['unproved_shape_finite_target_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_shape_traces(subparsers) -> None:
    coset_racah_stable_shape_traces = subparsers.add_parser(
        "coset-racah-stable-shape-traces",
        help="Prove exact first characteristic coefficients for all nine stable shapes.",
    )
    coset_racah_stable_shape_traces.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_shape_traces.set_defaults(
        func=command_coset_racah_stable_shape_traces
    )


def command_coset_racah_stable_shape_traces(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_shape_trace_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_shape_trace_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah shape-trace certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_shape_trace_certificate.json"
    )
    print(
        "Exact all-n shape traces: "
        f"{metrics['exact_all_n_shape_trace_theorem_count']}/9"
    )
    print(
        "New exact open-shape traces: "
        f"{metrics['new_exact_open_shape_trace_theorem_count']}/6"
    )
    print(
        "Remaining characteristic-coefficient families: "
        f"{metrics['remaining_open_shape_characteristic_coefficient_family_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_shape_second_moments(subparsers) -> None:
    coset_racah_stable_shape_second_moments = subparsers.add_parser(
        "coset-racah-stable-shape-second-moments",
        help="Prove exact second moments and all five open quadratic shape polynomials.",
    )
    coset_racah_stable_shape_second_moments.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_shape_second_moments.set_defaults(
        func=command_coset_racah_stable_shape_second_moments
    )


def command_coset_racah_stable_shape_second_moments(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_shape_second_moment_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_shape_second_moment_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah shape second-moment certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_shape_second_moment_certificate.json"
    )
    print(
        "Exact all-n shape second moments: "
        f"{metrics['exact_all_n_shape_second_moment_theorem_count']}/9"
    )
    print(
        "New complete quadratic shape polynomials: "
        f"{metrics['new_exact_complete_quadratic_shape_polynomial_count']}/5"
    )
    print(
        "Remaining characteristic-coefficient families: "
        f"{metrics['remaining_open_shape_characteristic_coefficient_family_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_shape_cubic_determinant(subparsers) -> None:
    coset_racah_stable_shape_cubic_determinant = subparsers.add_parser(
        "coset-racah-stable-shape-cubic-determinant",
        help="Prove the final multiplicity-three determinant and complete all nine stable-shape spectra.",
    )
    coset_racah_stable_shape_cubic_determinant.add_argument(
        "--workers", type=int, default=None
    )
    coset_racah_stable_shape_cubic_determinant.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_shape_cubic_determinant.set_defaults(
        func=command_coset_racah_stable_shape_cubic_determinant
    )


def command_coset_racah_stable_shape_cubic_determinant(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_shape_cubic_determinant_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_shape_cubic_determinant_certificate(
        workers=args.workers,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah cubic-shape determinant certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_shape_cubic_determinant_certificate.json"
    )
    print(
        "Exact cubic determinant theorems: "
        f"{metrics['exact_cubic_shape_determinant_theorem_count']}"
    )
    print(
        "Exact stable-shape polynomials: "
        f"{metrics['exact_complete_stable_shape_polynomial_count']}/9"
    )
    print(
        "Remaining characteristic-coefficient families: "
        f"{metrics['remaining_open_shape_characteristic_coefficient_family_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_shape_quadratic_gaps(subparsers) -> None:
    coset_racah_stable_shape_quadratic_gaps = subparsers.add_parser(
        "coset-racah-stable-shape-quadratic-gaps",
        help="Prove normalized root gaps for all five complementary quadratic stable shapes.",
    )
    coset_racah_stable_shape_quadratic_gaps.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_shape_quadratic_gaps.set_defaults(
        func=command_coset_racah_stable_shape_quadratic_gaps
    )


def command_coset_racah_stable_shape_quadratic_gaps(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_shape_quadratic_gap_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_shape_quadratic_gap_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah quadratic-shape gap certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_shape_quadratic_gap_certificate.json"
    )
    print(
        "New normalized gap theorems: "
        f"{metrics['new_normalized_gap_theorem_count']}/5"
    )
    print(
        "Remaining stable-shape gap families: "
        f"{metrics['remaining_open_stable_shape_gap_family_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_shape_cubic_gap(subparsers) -> None:
    coset_racah_stable_shape_cubic_gap = subparsers.add_parser(
        "coset-racah-stable-shape-cubic-gap",
        help="Prove the final cubic normalized gap and close all stable-shape spectral gaps.",
    )
    coset_racah_stable_shape_cubic_gap.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_shape_cubic_gap.set_defaults(
        func=command_coset_racah_stable_shape_cubic_gap
    )


def command_coset_racah_stable_shape_cubic_gap(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_shape_cubic_gap_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_shape_cubic_gap_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact stable Racah cubic-shape gap certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_shape_cubic_gap_certificate.json"
    )
    print(
        "Complementary normalized gap families: "
        f"{metrics['complementary_shape_normalized_gap_theorem_count']}/6"
    )
    print(
        "All nontrivial stable-shape gap families: "
        f"{metrics['all_nontrivial_stable_shape_normalized_gap_theorem_count']}/7"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_shape_coherent_labels(subparsers) -> None:
    coset_racah_stable_shape_coherent_labels = subparsers.add_parser(
        "coset-racah-stable-shape-coherent-labels",
        help="Prove shape-local coherent eigenlabels on all seven nontrivial stable shapes.",
    )
    coset_racah_stable_shape_coherent_labels.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_shape_coherent_labels.set_defaults(
        func=command_coset_racah_stable_shape_coherent_labels
    )


def command_coset_racah_stable_shape_coherent_labels(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_shape_coherent_label_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_shape_coherent_label_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah all-shape coherent-label certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_shape_coherent_label_certificate.json"
    )
    print(
        "All nontrivial coherent shape labels: "
        f"{metrics['all_nontrivial_stable_shape_coherent_label_count']}/7"
    )
    print(
        "Coupling-tree transition circuits: "
        f"{metrics['coupling_tree_transition_circuit_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_first_stage_labels(subparsers) -> None:
    coset_racah_stable_first_stage_labels = subparsers.add_parser(
        "coset-racah-stable-first-stage-labels",
        help="Prove coherent labels for both nontrivial first-stage stable multiplicity blocks.",
    )
    coset_racah_stable_first_stage_labels.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_first_stage_labels.set_defaults(
        func=command_coset_racah_stable_first_stage_labels
    )


def command_coset_racah_stable_first_stage_labels(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_first_stage_label_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_first_stage_label_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah first-stage multiplicity-label certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_first_stage_label_certificate.json"
    )
    print(
        "Nontrivial first-stage gaps: "
        f"{metrics['all_nontrivial_first_stage_gap_theorem_count']}/2"
    )
    print(
        "Stable shapes with first-stage multiplicity resolved: "
        f"{metrics['all_stable_first_stage_multiplicity_resolved_shape_count']}/9"
    )
    print(
        "Coupling-tree transition circuits: "
        f"{metrics['coupling_tree_transition_circuit_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_shape_router(subparsers) -> None:
    coset_racah_stable_shape_router = subparsers.add_parser(
        "coset-racah-stable-shape-router",
        help="Prove a collision-free coherent intermediate-shape router on the stable branch.",
    )
    coset_racah_stable_shape_router.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_shape_router.set_defaults(
        func=command_coset_racah_stable_shape_router
    )


def command_coset_racah_stable_shape_router(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_shape_router_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_shape_router_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah intermediate-shape router certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_shape_router_certificate.json"
    )
    print(
        "Stable-range signature collisions: "
        f"{metrics['stable_range_shape_pair_collision_count']}/"
        f"{metrics['shape_pair_collision_audit_count']} pairs"
    )
    print(
        "Coherent encoded shape routers: "
        f"{metrics['coherent_intermediate_shape_router_count']}"
    )
    print(
        "Compressed Clebsch isometries: "
        f"{metrics['compressed_clebsch_isometry_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_encoded_tree(subparsers) -> None:
    coset_racah_stable_encoded_tree = subparsers.add_parser(
        "coset-racah-stable-encoded-tree",
        help="Compose complete encoded left/right stable coupling-tree labels and their transition isometry.",
    )
    coset_racah_stable_encoded_tree.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_encoded_tree.set_defaults(
        func=command_coset_racah_stable_encoded_tree
    )


def command_coset_racah_stable_encoded_tree(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_encoded_tree_certificate,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_encoded_tree_certificate(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah encoded coupling-tree certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_encoded_tree_certificate.json"
    )
    print(
        "Complete joint labels: "
        f"{metrics['joint_multiplicity_label_count']}/"
        f"{metrics['final_multiplicity_dimension']}"
    )
    print(
        "Encoded coupling-tree transition isometries: "
        f"{metrics['encoded_coupling_tree_transition_isometry_count']}"
    )
    print(
        "State-dependent transition filters: "
        f"{metrics['transition_filter_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_three_copy_frame(subparsers) -> None:
    coset_racah_stable_three_copy_frame = subparsers.add_parser(
        "coset-racah-stable-three-copy-frame",
        help="Block-encode the exact stable three-copy frame and audit finite support conditioning.",
    )
    coset_racah_stable_three_copy_frame.add_argument("--n", type=int, default=8)
    coset_racah_stable_three_copy_frame.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_three_copy_frame.set_defaults(
        func=command_coset_racah_stable_three_copy_frame
    )


def command_coset_racah_stable_three_copy_frame(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_three_copy_frame_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_three_copy_frame_report(
        n=args.n,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah three-copy frame certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_three_copy_frame.json"
    )
    print(
        "Polynomial frame block encodings: "
        f"{metrics['polynomial_three_copy_frame_block_encoding_count']}"
    )
    print(
        "Finite full-support frames: "
        f"{metrics['finite_full_support_frame_count']}/"
        f"{metrics['finite_frame_record_count']}"
    )
    print(
        "Maximum frontier finite condition number: "
        f"{metrics['maximum_frontier_finite_condition_number']:.6f}"
    )
    print(
        "All-n conditioning theorems: "
        f"{metrics['all_n_inverse_polynomial_minimum_eigenvalue_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_three_copy_frame_conditioning(subparsers) -> None:
    coset_racah_stable_three_copy_frame_conditioning = subparsers.add_parser(
        "coset-racah-stable-three-copy-frame-conditioning",
        help="Prove all-n stable-frame coercivity and the polynomial inverse-square-root filter contract.",
    )
    coset_racah_stable_three_copy_frame_conditioning.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_three_copy_frame_conditioning.set_defaults(
        func=command_coset_racah_stable_three_copy_frame_conditioning
    )


def command_coset_racah_stable_three_copy_frame_conditioning(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_stable_three_copy_frame_conditioning_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_stable_three_copy_frame_conditioning_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah three-copy frame all-n conditioning certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_three_copy_frame_conditioning.json"
    )
    print(
        "Exact residue/shape coercivity certificates: "
        f"{metrics['verified_coercivity_residue_certificate_count']}/"
        f"{metrics['coercivity_residue_certificate_count']}"
    )
    print(
        "Global eigenvalue lower bound: "
        f"{metrics['global_minimum_eigenvalue_lower_bound_constant']}/"
        f"n^{metrics['global_minimum_eigenvalue_lower_bound_exponent']}"
    )
    print(
        "Polynomial inverse-square-root filters: "
        f"{metrics['polynomial_inverse_square_root_filter_count']}"
    )
    print(f"Hidden-involution decoders: {metrics['hidden_involution_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_stable_branch_access(subparsers) -> None:
    coset_racah_stable_branch_access = subparsers.add_parser(
        "coset-racah-stable-branch-access",
        help="Prove or falsify natural-input access to the solved stable W-cubed branch.",
    )
    coset_racah_stable_branch_access.add_argument(
        "--n-values", default="8,9,10,12,16,20,24,32"
    )
    coset_racah_stable_branch_access.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_stable_branch_access.set_defaults(
        func=command_coset_racah_stable_branch_access
    )


def command_coset_racah_stable_branch_access(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_stable_branch_accessibility_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(parse_int_csv(args.n_values))
    payload = write_stable_branch_accessibility_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Stable Racah branch natural-input accessibility audit complete")
    print(
        "Artifact: research/representation/"
        "coset_stable_branch_accessibility.json"
    )
    print(
        "Exact branch probability identities: "
        f"{metrics['exact_branch_probability_identity_count']}"
    )
    print(
        "Asymptotic superpolynomial rarity theorems: "
        f"{metrics['asymptotic_superpolynomial_rarity_theorem_count']}"
    )
    print(
        "Natural-input polynomially accessible stable branches: "
        f"{metrics['natural_input_polynomial_accessible_branch_count']}"
    )
    print(
        "Largest audited log2 amplitude-amplification cost: "
        f"{metrics['maximum_log2_generic_amplitude_amplification_iterations']:.3f}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_irrep_transfer(subparsers) -> None:
    coset_racah_typical_irrep_transfer = subparsers.add_parser(
        "coset-racah-typical-irrep-transfer",
        help="Prove the fixed-tail access no-go and audit transfer to naturally sampled typical partitions.",
    )
    coset_racah_typical_irrep_transfer.add_argument(
        "--n-values", default="8,10,12,14,16,18,20"
    )
    coset_racah_typical_irrep_transfer.add_argument(
        "--tail-limit", type=int, default=4
    )
    coset_racah_typical_irrep_transfer.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_irrep_transfer.set_defaults(
        func=command_coset_racah_typical_irrep_transfer
    )


def command_coset_racah_typical_irrep_transfer(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_typical_irrep_transfer_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(parse_int_csv(args.n_values))
    payload = write_typical_irrep_transfer_report(
        n_values=n_values,
        bounded_tail_limit=args.tail_limit,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep recoupling transfer audit complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_irrep_transfer_audit.json"
    )
    print(
        "Fixed bounded-tail natural-access no-go theorems: "
        f"{metrics['bounded_tail_natural_access_no_go_theorem_count']}"
    )
    print(
        "Largest exact typical-sector multiplicity: "
        f"{metrics['maximum_kronecker_multiplicity']}"
    )
    print(
        "Minimum audited bounded-tail coupling mass: "
        f"{metrics['minimum_bounded_tail_coupling_mass']:.3e}"
    )
    print(
        "Uniform typical-label commutant-gap theorems: "
        f"{metrics['uniform_typical_label_commutant_gap_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_commutant_moments(subparsers) -> None:
    coset_racah_typical_commutant_moments = subparsers.add_parser(
        "coset-racah-typical-commutant-moments",
        help="Audit bounded-support commutant non-scalarity on typical irreps using exact character moments.",
    )
    coset_racah_typical_commutant_moments.add_argument(
        "--n-values", default="7,8"
    )
    coset_racah_typical_commutant_moments.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_commutant_moments.set_defaults(
        func=command_coset_racah_typical_commutant_moments
    )


def command_coset_racah_typical_commutant_moments(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_typical_commutant_moment_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(parse_int_csv(args.n_values))
    payload = write_typical_commutant_moment_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep commutant moment audit complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_commutant_moment_audit.json"
    )
    print(
        "Finite non-scalar multiplicity blocks: "
        f"{metrics['finite_non_scalar_covered_count']}/"
        f"{metrics['nontrivial_multiplicity_block_count']}"
    )
    print(f"Finite uncovered blocks: {metrics['finite_uncovered_count']}")
    print(
        "Uniform inverse-polynomial gap theorems: "
        f"{metrics['uniform_typical_commutant_gap_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_class_contraction(subparsers) -> None:
    coset_racah_typical_class_contraction = subparsers.add_parser(
        "coset-racah-typical-class-contraction",
        help="Scale exact typical-irrep commutant moments by marked conjugacy-class contraction.",
    )
    coset_racah_typical_class_contraction.add_argument(
        "--n-values", default="6,7,8,9,10"
    )
    coset_racah_typical_class_contraction.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_class_contraction.set_defaults(
        func=command_coset_racah_typical_class_contraction
    )


def command_coset_racah_typical_class_contraction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_class_contraction_scaling_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(parse_int_csv(args.n_values))
    payload = write_class_contraction_scaling_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep class-contraction scaling audit complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_class_contraction_scaling.json"
    )
    print(f"Maximum exact n: {metrics['maximum_n']}")
    print(
        "Exact scalar multiplicity blocks: "
        f"{metrics['total_exact_scalar_block_count']}"
    )
    print(
        "Single-generator uniformity falsifications: "
        f"{metrics['single_primary_generator_uniformity_falsification_count']}"
    )
    print(
        "Uniform portfolio joint-gap theorems: "
        f"{metrics['uniform_portfolio_joint_gap_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_portfolio_collision(subparsers) -> None:
    coset_racah_typical_portfolio_collision = subparsers.add_parser(
        "coset-racah-typical-portfolio-collision",
        help="Prove the exact n=8 repeated-root collision in the support-three commutant portfolio.",
    )
    coset_racah_typical_portfolio_collision.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_portfolio_collision.set_defaults(
        func=command_coset_racah_typical_portfolio_collision
    )


def command_coset_racah_typical_portfolio_collision(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_portfolio_collision_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_portfolio_collision_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep portfolio collision certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_portfolio_collision_certificate.json"
    )
    print(
        "Repeated-root collision targets: "
        f"{metrics['repeated_zero_eigenvalue_target_count']}"
    )
    print(
        "Finite coefficient rules falsified at n=8: "
        f"{metrics['finite_common_coefficient_rules_falsified_at_n8']}"
    )
    print(
        "Minimum required portfolio generators: "
        f"{metrics['minimum_required_portfolio_generator_count_on_certified_targets']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_third_generator(subparsers) -> None:
    coset_racah_typical_third_generator = subparsers.add_parser(
        "coset-racah-typical-third-generator",
        help="Prove the exact TC-intersection-one repair of the n=8 commutant collisions.",
    )
    coset_racah_typical_third_generator.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_third_generator.set_defaults(
        func=command_coset_racah_typical_third_generator
    )


def command_coset_racah_typical_third_generator(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_independent_third_generator_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_independent_third_generator_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep independent third-generator certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_independent_third_generator_certificate.json"
    )
    print(
        "Exact n=8 collision targets repaired: "
        f"{metrics['certified_n8_collision_target_repair_count']}"
    )
    print(
        "Exact n=8 low-multiplicity targets certified: "
        f"{metrics['certified_n8_low_multiplicity_simple_spectrum_target_count']}/"
        f"{metrics['n8_nontrivial_multiplicity_target_count']}"
    )
    print(
        "All-n simple-spectrum theorems: "
        f"{metrics['all_n_simple_spectrum_theorem_count']}"
    )
    print(
        "Inverse-polynomial gap theorems: "
        f"{metrics['inverse_polynomial_gap_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_high_multiplicity(subparsers) -> None:
    coset_racah_typical_high_multiplicity = subparsers.add_parser(
        "coset-racah-typical-high-multiplicity",
        help="Run the exact quotient transfer through all n=8 multiplicity targets.",
    )
    coset_racah_typical_high_multiplicity.add_argument(
        "--recompute", action="store_true"
    )
    coset_racah_typical_high_multiplicity.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_high_multiplicity.set_defaults(
        func=command_coset_racah_typical_high_multiplicity
    )


def command_coset_racah_typical_high_multiplicity(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_high_multiplicity_transfer_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_high_multiplicity_transfer_report(
        recompute=args.recompute,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep higher-multiplicity transfer audit complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_high_multiplicity_transfer.json"
    )
    print(
        "Exact n=8 targets certified: "
        f"{metrics['certified_n8_simple_spectrum_target_count']}/"
        f"{metrics['n8_nontrivial_multiplicity_target_count']}"
    )
    print(
        "Maximum certified multiplicity: "
        f"{metrics['maximum_certified_kronecker_multiplicity']}"
    )
    print(f"Transfer recomputed: {bool(metrics['exact_transfer_recomputed_count'])}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_separator_gaps(subparsers) -> None:
    coset_racah_typical_separator_gaps = subparsers.add_parser(
        "coset-racah-typical-separator-gaps",
        help="Audit finite normalized gaps for the fixed TT1+TC1 separator.",
    )
    coset_racah_typical_separator_gaps.add_argument(
        "--n-values", default="5,6,7,8"
    )
    coset_racah_typical_separator_gaps.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_separator_gaps.set_defaults(
        func=command_coset_racah_typical_separator_gaps
    )


def command_coset_racah_typical_separator_gaps(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_fixed_separator_gap_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(
        int(value.strip()) for value in args.n_values.split(",") if value.strip()
    )
    payload = write_fixed_separator_gap_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep fixed-separator gap audit complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_fixed_separator_gap_scaling.json"
    )
    print(
        "Finite all-block split sizes: "
        f"{metrics['finite_all_block_simple_spectrum_size_count']}/"
        f"{metrics['finite_size_count']}"
    )
    print(
        "Certified n=8 normalized minimum gap lower bound: "
        f"{metrics['n8_certified_minimum_lcu_normalized_gap_lower_bound']:.12g}"
    )
    print(
        "Inverse-polynomial gap theorems: "
        f"{metrics['inverse_polynomial_normalized_gap_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_n9_probe(subparsers) -> None:
    coset_racah_typical_n9_probe = subparsers.add_parser(
        "coset-racah-typical-n9-probe",
        help="Run the exact n=9 probe on every target of multiplicity at most ten.",
    )
    coset_racah_typical_n9_probe.add_argument(
        "--recompute", action="store_true"
    )
    coset_racah_typical_n9_probe.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_n9_probe.set_defaults(
        func=command_coset_racah_typical_n9_probe
    )


def command_coset_racah_typical_n9_probe(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_n9_low_multiplicity_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_n9_low_multiplicity_report(
        recompute=args.recompute,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep n=9 low-multiplicity probe complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_n9_low_multiplicity_probe.json"
    )
    print(
        "Exact n=9 targets certified: "
        f"{metrics['low_multiplicity_simple_spectrum_target_count']}/"
        f"{metrics['n9_nontrivial_multiplicity_target_count']}"
    )
    print(
        "Unaudited higher-multiplicity targets: "
        f"{metrics['n9_unaudited_higher_multiplicity_target_count']}"
    )
    print(f"Transfer recomputed: {bool(metrics['exact_transfer_recomputed_count'])}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_n9_full(subparsers) -> None:
    coset_racah_typical_n9_full = subparsers.add_parser(
        "coset-racah-typical-n9-full",
        help="Validate the exact all-target n=9 TT1+TC1 separator certificate.",
    )
    coset_racah_typical_n9_full.add_argument(
        "--recompute", action="store_true"
    )
    coset_racah_typical_n9_full.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_n9_full.set_defaults(
        func=command_coset_racah_typical_n9_full
    )


def command_coset_racah_typical_n9_full(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_n9_full_transfer_report
    initialize_seed_registry(overwrite=False)
    payload = write_n9_full_transfer_report(
        recompute=args.recompute,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep full n=9 transfer certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_n9_full_transfer.json"
    )
    print(
        "Exact n=9 targets certified: "
        f"{metrics['certified_n9_simple_spectrum_target_count']}/"
        f"{metrics['n9_nontrivial_multiplicity_target_count']}"
    )
    print(
        "Certified n=9 normalized minimum gap lower bound: "
        f"{metrics['certified_n9_minimum_lcu_normalized_gap_lower_bound']:.12g}"
    )
    print(f"Transfer recomputed: {bool(metrics['exact_transfer_recomputed_count'])}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_n10_feasibility(subparsers) -> None:
    coset_racah_typical_n10_feasibility = subparsers.add_parser(
        "coset-racah-typical-n10-feasibility",
        help="Validate the first n=10 targets and exact contraction scaling boundary.",
    )
    coset_racah_typical_n10_feasibility.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_n10_feasibility.set_defaults(
        func=command_coset_racah_typical_n10_feasibility
    )


def command_coset_racah_typical_n10_feasibility(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_n10_feasibility_report
    initialize_seed_registry(overwrite=False)
    payload = write_n10_feasibility_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep n=10 feasibility boundary complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_n10_feasibility.json"
    )
    print(
        "Exact n=10 targets certified: "
        f"{metrics['certified_n10_simple_spectrum_target_count']}/"
        f"{metrics['n10_nontrivial_multiplicity_target_count']}"
    )
    print(
        "Degree-five naive character table bytes: "
        f"{metrics['degree5_naive_temporary_character_table_bytes']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_support_growth(subparsers) -> None:
    coset_racah_typical_support_growth = subparsers.add_parser(
        "coset-racah-typical-support-growth",
        help="Certify the full-support barrier for direct marked-class transfer contraction.",
    )
    coset_racah_typical_support_growth.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_support_growth.set_defaults(
        func=command_coset_racah_typical_support_growth
    )


def command_coset_racah_typical_support_growth(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_transfer_support_growth_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_transfer_support_growth_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep transfer support-growth audit complete")
    print(
        "Artifact: research/representation/"
        "coset_transfer_support_growth.json"
    )
    print(
        "n=9 degree-28 full-support weight: "
        f"{metrics['n9_degree28_full_support_weight_fraction']:.6f}"
    )
    print(
        "n=10 degree-five support 9 or 10 weight: "
        f"{metrics['n10_degree5_support9_or_10_weight_fraction']:.6f}"
    )
    print(
        "Scalable full-support contractions: "
        f"{metrics['scalable_full_support_character_contraction_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_invariant_contraction(subparsers) -> None:
    coset_racah_typical_invariant_contraction = subparsers.add_parser(
        "coset-racah-typical-invariant-contraction",
        help="Contract n=10 typical blocks through sparse diagonal-S_n invariants.",
    )
    coset_racah_typical_invariant_contraction.add_argument(
        "--recompute", action="store_true"
    )
    coset_racah_typical_invariant_contraction.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_invariant_contraction.set_defaults(
        func=command_coset_racah_typical_invariant_contraction
    )


def command_coset_racah_typical_invariant_contraction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_invariant_contraction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_invariant_contraction_report(
        recompute=args.recompute,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep sparse invariant contraction complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_invariant_contraction.json"
    )
    print(
        "Exact-control trace residual: "
        f"{metrics['maximum_exact_control_trace_residual']:.3g}"
    )
    print(
        "Multiplicity-six numerical minimum gap: "
        f"{metrics['n10_multiplicity6_minimum_numerical_raw_gap']:.12g}"
    )
    print(
        "Explicit S_10 character bytes avoided: "
        f"{metrics['explicit_s10_character_table_bytes_avoided']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_yjm_projector(subparsers) -> None:
    coset_racah_typical_yjm_projector = subparsers.add_parser(
        "coset-racah-typical-yjm-projector",
        help="Certify exact YJM projector traces and audit pair-algebra scaling.",
    )
    coset_racah_typical_yjm_projector.add_argument(
        "--recompute", action="store_true"
    )
    coset_racah_typical_yjm_projector.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_yjm_projector.set_defaults(
        func=command_coset_racah_typical_yjm_projector
    )


def command_coset_racah_typical_yjm_projector(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_yjm_projector_certificate_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_yjm_projector_certificate_report(
        recompute=args.recompute,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep exact YJM projector certificate complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_yjm_projector_certificate.json"
    )
    print(f"Exact projector power traces: {metrics['exact_power_trace_count']}")
    print(
        "n=6 degree-two pair-state saturation: "
        f"{metrics['n6_degree2_pair_state_saturation_fraction']:.6f}"
    )
    print(
        "Young-tower exact evaluators: "
        f"{metrics['young_tower_compressed_exact_trace_evaluator_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_modular_yjm(subparsers) -> None:
    coset_racah_typical_modular_yjm = subparsers.add_parser(
        "coset-racah-typical-modular-yjm",
        help="Run exact finite-field YJM controls and the n=10 CRT cost gate.",
    )
    coset_racah_typical_modular_yjm.add_argument(
        "--recompute", action="store_true"
    )
    coset_racah_typical_modular_yjm.add_argument(
        "--compute-n10", action="store_true"
    )
    coset_racah_typical_modular_yjm.add_argument(
        "--workers", type=int, default=6
    )
    coset_racah_typical_modular_yjm.add_argument(
        "--target", default="5,5"
    )
    coset_racah_typical_modular_yjm.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_modular_yjm.set_defaults(
        func=command_coset_racah_typical_modular_yjm
    )


def command_coset_racah_typical_modular_yjm(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_modular_yjm_contraction_report,
        write_n10_target_prime_certificate,
    )
    initialize_seed_registry(overwrite=False)
    if args.compute_n10:
        target = tuple(int(value) for value in args.target.split(","))
        write_n10_target_prime_certificate(
            target,
            workers=args.workers,
        )
    payload = write_modular_yjm_contraction_report(
        recompute=args.recompute,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep exact modular YJM contraction complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_modular_yjm_contraction.json"
    )
    print(
        "Exact modular control traces: "
        f"{metrics['exact_modular_power_trace_count']}"
    )
    print(
        "n=10 pair/tensor reduction: "
        f"{metrics['n10_pair_group_to_tensor_dimension_reduction_factor']:.0f}x"
    )
    print(
        "n=10 modular residues: "
        f"{metrics['n10_modular_prime_residue_count']}"
    )
    print(
        "n=10 exact square-free targets: "
        f"{metrics['n10_exact_square_free_target_count']}/"
        f"{metrics['n10_nontrivial_multiplicity_target_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_modular_gaps(subparsers) -> None:
    coset_racah_typical_modular_gaps = subparsers.add_parser(
        "coset-racah-typical-modular-gaps",
        help="Prove denominator-based gap bounds and audit phase-estimation precision.",
    )
    coset_racah_typical_modular_gaps.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_modular_gaps.set_defaults(
        func=command_coset_racah_typical_modular_gaps
    )


def command_coset_racah_typical_modular_gaps(
    args: argparse.Namespace,
) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_modular_gap_bound_report
    initialize_seed_registry(overwrite=False)
    payload = write_modular_gap_bound_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep exact denominator gap audit complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_modular_gap_bounds.json"
    )
    print(
        "Certified target bounds: "
        f"{metrics['square_free_target_bound_count']}"
    )
    print(
        "Strongest normalized log10 lower bound: "
        f"{metrics['strongest_lcu_normalized_gap_lower_bound_log10']:.1f}"
    )
    print(
        "Inverse-polynomial gap theorems: "
        f"{metrics['inverse_polynomial_normalized_gap_theorem_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_n10_gap_trend(subparsers) -> None:
    coset_racah_typical_n10_gap_trend = subparsers.add_parser(
        "coset-racah-typical-n10-gap-trend",
        help="Compare numerical real gaps on exactly square-free n=10 blocks.",
    )
    coset_racah_typical_n10_gap_trend.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_n10_gap_trend.set_defaults(
        func=command_coset_racah_typical_n10_gap_trend
    )


def command_coset_racah_typical_n10_gap_trend(
    args: argparse.Namespace,
) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_n10_gap_trend_report
    initialize_seed_registry(overwrite=False)
    payload = write_n10_gap_trend_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep n=10 numerical gap trend complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_n10_gap_trend.json"
    )
    print(
        "Multiplicity-6 to multiplicity-8 gap drop: "
        f"{metrics['multiplicity6_to_multiplicity8_gap_drop_factor']:.2f}x"
    )
    print(
        "Machine-verified roundoff bounds: "
        f"{metrics['machine_verified_roundoff_bound_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_source_coverage(subparsers) -> None:
    coset_racah_typical_source_coverage = subparsers.add_parser(
        "coset-racah-typical-source-coverage",
        help=(
            "Audit natural Fourier source mass and exact target coupling "
            "coverage of the fixed-source typical separator ladder."
        ),
    )
    coset_racah_typical_source_coverage.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_source_coverage.set_defaults(
        func=command_coset_racah_typical_source_coverage
    )


def command_coset_racah_typical_source_coverage(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_typical_source_coverage_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_typical_source_coverage_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep natural source/target coverage audit complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_source_coverage.json"
    )
    print(
        "n=10 certified target coupling mass: "
        f"{metrics['n10_certified_target_coupling_mass']:.3%}"
    )
    print(
        "Polynomial pre-certified source catalog no-go theorems: "
        f"{metrics['polynomial_precertified_source_catalog_no_go_theorem_count']}"
    )
    print(
        "Uniform arbitrary-source separators: "
        f"{metrics['uniform_arbitrary_source_partition_separator_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_uniform_sources(subparsers) -> None:
    coset_racah_typical_uniform_sources = subparsers.add_parser(
        "coset-racah-typical-uniform-sources",
        help=(
            "Probe the fixed typical separator on every ordered source pair "
            "and certify unequal-source scalar collisions."
        ),
    )
    coset_racah_typical_uniform_sources.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_uniform_sources.set_defaults(
        func=command_coset_racah_typical_uniform_sources
    )


def command_coset_racah_typical_uniform_sources(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_uniform_source_probe_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_uniform_source_probe_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep all-source fixed-separator probe complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_uniform_source_probe.json"
    )
    print(
        "Exact scalar collisions: "
        f"{metrics['exact_scalar_collision_count']}"
    )
    print(
        "Numerical repeated-root blocks: "
        f"{metrics['numerical_repeated_eigenvalue_block_count']}"
    )
    print(
        "Maximum natural source-pair mass with exact scalar collision: "
        f"{metrics['maximum_natural_source_pair_mass_with_exact_scalar_collision']:.3%}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_parity_separator(subparsers) -> None:
    coset_racah_typical_parity_separator = subparsers.add_parser(
        "coset-racah-typical-parity-separator",
        help=(
            "Search parity-complete TT/TC/CT coefficients across every "
            "small-n ordered source pair."
        ),
    )
    coset_racah_typical_parity_separator.add_argument(
        "--recompute-n7", action="store_true"
    )
    coset_racah_typical_parity_separator.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_parity_separator.set_defaults(
        func=command_coset_racah_typical_parity_separator
    )


def command_coset_racah_typical_parity_separator(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_parity_complete_separator_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_parity_complete_separator_report(
        recompute_n7=args.recompute_n7,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typical-irrep parity-complete separator search complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_parity_complete_separator.json"
    )
    print(
        "Finite collision-free candidates: "
        f"{metrics['collision_free_finite_candidate_count']}/"
        f"{metrics['coefficient_vector_count']}"
    )
    print(
        "Best minimum numerical raw gap: "
        f"{metrics['best_candidate_minimum_numerical_raw_gap']:.12g}"
    )
    print(
        "Former scalar blocks exactly repaired: "
        f"{metrics['former_scalar_block_exact_repair_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_racah_typical_parity_holdout(subparsers) -> None:
    coset_racah_typical_parity_holdout = subparsers.add_parser(
        "coset-racah-typical-parity-holdout",
        help=(
            "Run exact class-compressed all-source holdouts for the frozen "
            "parity-complete separator."
        ),
    )
    coset_racah_typical_parity_holdout.add_argument(
        "--n-values", default="5,6,7,8"
    )
    coset_racah_typical_parity_holdout.add_argument(
        "--no-registry", action="store_true"
    )
    coset_racah_typical_parity_holdout.set_defaults(
        func=command_coset_racah_typical_parity_holdout
    )


def command_coset_racah_typical_parity_holdout(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_parity_class_contraction_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(
        int(value.strip())
        for value in args.n_values.split(",")
        if value.strip()
    )
    payload = write_parity_class_contraction_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact parity-complete class-contraction holdout complete")
    print(
        "Artifact: research/representation/"
        "coset_typical_parity_class_contraction.json"
    )
    print(
        "Exact scalar obstructions: "
        f"{metrics['exact_scalar_obstruction_count']}/"
        f"{metrics['all_source_exact_block_count']}"
    )
    print(
        "Multiplicity-two simple spectra: "
        f"{metrics['exact_multiplicity_two_simple_spectrum_count']}/"
        f"{metrics['multiplicity_two_block_count']}"
    )
    print(
        f"Speedup claim allowed: "
        f"{payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_recoupling_synthesize(subparsers) -> None:
    coset_recoupling_synthesize = subparsers.add_parser(
        "coset-recoupling-synthesize",
        help="Synthesize typed recoupling mechanisms and reject undefined or known-invalid architectures.",
    )
    coset_recoupling_synthesize.add_argument("--no-registry", action="store_true")
    coset_recoupling_synthesize.set_defaults(func=command_coset_recoupling_synthesize)


def command_coset_recoupling_synthesize(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_recoupling_mechanism_synthesis_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_recoupling_mechanism_synthesis_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Typed recoupling mechanism synthesis complete")
    print("Artifact: research/representation/coset_recoupling_mechanism_synthesis.json")
    print(f"Mechanisms: {metrics['mechanism_count']}")
    print(f"Known no-go rejections: {metrics['known_no_go_rejected_count']}")
    print(f"Proposal-only architectures: {metrics['proposal_only_count']}")
    print(f"Proof-gate eligible architectures: {metrics['proof_gate_eligible_count']}")
    print(f"Automatically promoted candidates: {metrics['automatically_promoted_candidate_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_coset_hidden_involution_all_copy_target_lcu_no_go(subparsers) -> None:
    parser_coset_hidden_involution_all_copy_target_lcu_no_go = subparsers.add_parser(
        "coset-hidden-involution-all-copy-target-lcu-no-go",
        help="All-copy target-coupled normalized-LCU no-go.",
    )
    parser_coset_hidden_involution_all_copy_target_lcu_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_all_copy_target_lcu_no_go.set_defaults(func=command_coset_hidden_involution_all_copy_target_lcu_no_go)


def command_coset_hidden_involution_all_copy_target_lcu_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_all_copy_target_LCU_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_all_copy_target_LCU_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_all_copy_target_LCU_no_go_report()
    validation = validate_registry()
    print("coset_hidden_involution_all_copy_target_lcu_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_all_copy_target_lcu_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_bounded_support_commutant_generation(subparsers) -> None:
    parser_coset_hidden_involution_bounded_support_commutant_generation = subparsers.add_parser(
        "coset-hidden-involution-bounded-support-commutant-generation",
        help="Bounded-support generators for hyperoctahedral branching commutants.",
    )
    parser_coset_hidden_involution_bounded_support_commutant_generation.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_bounded_support_commutant_generation.set_defaults(func=command_coset_hidden_involution_bounded_support_commutant_generation)


def command_coset_hidden_involution_bounded_support_commutant_generation(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_bounded_support_commutant_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_bounded_support_commutant_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_bounded_support_commutant_report()
    validation = validate_registry()
    print("coset_hidden_involution_bounded_support_commutant_generation complete")
    print("Artifact: research/representation/coset_hidden_involution_bounded_support_commutant_generation.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_colour_resolved_paired_tower_boundary(subparsers) -> None:
    parser_coset_hidden_involution_colour_resolved_paired_tower_boundary = subparsers.add_parser(
        "coset-hidden-involution-colour-resolved-paired-tower-boundary",
        help="Colour-resolved paired-tower boundary for hyperoctahedral subduction.",
    )
    parser_coset_hidden_involution_colour_resolved_paired_tower_boundary.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_colour_resolved_paired_tower_boundary.set_defaults(func=command_coset_hidden_involution_colour_resolved_paired_tower_boundary)


def command_coset_hidden_involution_colour_resolved_paired_tower_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_colour_resolved_paired_tower_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_colour_resolved_paired_tower_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_colour_resolved_paired_tower_report()
    validation = validate_registry()
    print("coset_hidden_involution_colour_resolved_paired_tower_boundary complete")
    print("Artifact: research/representation/coset_hidden_involution_colour_resolved_paired_tower_boundary.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_commutant_support_growth_boundary(subparsers) -> None:
    parser_coset_hidden_involution_commutant_support_growth_boundary = subparsers.add_parser(
        "coset-hidden-involution-commutant-support-growth-boundary",
        help="First support-growth boundary for hyperoctahedral commutant generators.",
    )
    parser_coset_hidden_involution_commutant_support_growth_boundary.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_commutant_support_growth_boundary.set_defaults(func=command_coset_hidden_involution_commutant_support_growth_boundary)


def command_coset_hidden_involution_commutant_support_growth_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_commutant_support_growth_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_commutant_support_growth_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_commutant_support_growth_report()
    validation = validate_registry()
    print("coset_hidden_involution_commutant_support_growth_boundary complete")
    print("Artifact: research/representation/coset_hidden_involution_commutant_support_growth_boundary.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_commuting_square_recoupling_boundary(subparsers) -> None:
    parser_coset_hidden_involution_commuting_square_recoupling_boundary = subparsers.add_parser(
        "coset-hidden-involution-commuting-square-recoupling-boundary",
        help="Commuting-square architecture and its vertical-multiplicity boundary.",
    )
    parser_coset_hidden_involution_commuting_square_recoupling_boundary.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_commuting_square_recoupling_boundary.set_defaults(func=command_coset_hidden_involution_commuting_square_recoupling_boundary)


def command_coset_hidden_involution_commuting_square_recoupling_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_commuting_square_recoupling_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_commuting_square_recoupling_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_commuting_square_recoupling_report()
    validation = validate_registry()
    print("coset_hidden_involution_commuting_square_recoupling_boundary complete")
    print("Artifact: research/representation/coset_hidden_involution_commuting_square_recoupling_boundary.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_cross_transposition_hecke_degree_five_no_go(subparsers) -> None:
    parser_coset_hidden_involution_cross_transposition_hecke_degree_five_no_go = subparsers.add_parser(
        "coset-hidden-involution-cross-transposition-hecke-degree-five-no-go",
        help="Exact degree-five no-go for the canonical cross-transposition Hecke walk.",
    )
    parser_coset_hidden_involution_cross_transposition_hecke_degree_five_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_cross_transposition_hecke_degree_five_no_go.set_defaults(func=command_coset_hidden_involution_cross_transposition_hecke_degree_five_no_go)


def command_coset_hidden_involution_cross_transposition_hecke_degree_five_no_go(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_degree_five_report
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_degree_five_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_degree_five_report()
    validation = validate_registry()
    print("coset_hidden_involution_cross_transposition_hecke_degree_five_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_cross_transposition_hecke_degree_five_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_cross_transposition_hecke_moment_no_go(subparsers) -> None:
    parser_coset_hidden_involution_cross_transposition_hecke_moment_no_go = subparsers.add_parser(
        "coset-hidden-involution-cross-transposition-hecke-moment-no-go",
        help="Degree-four moment no-go for the cross-transposition recoupling walk.",
    )
    parser_coset_hidden_involution_cross_transposition_hecke_moment_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_cross_transposition_hecke_moment_no_go.set_defaults(func=command_coset_hidden_involution_cross_transposition_hecke_moment_no_go)


def command_coset_hidden_involution_cross_transposition_hecke_moment_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_cross_transposition_Hecke_moment_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_cross_transposition_Hecke_moment_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_cross_transposition_Hecke_moment_report()
    validation = validate_registry()
    print("coset_hidden_involution_cross_transposition_hecke_moment_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_cross_transposition_hecke_moment_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_diagonal_charge_bias_no_go(subparsers) -> None:
    parser_coset_hidden_involution_diagonal_charge_bias_no_go = subparsers.add_parser(
        "coset-hidden-involution-diagonal-charge-bias-no-go",
        help="Exact bias bound for the simplest all-copy target-coupled charges.",
    )
    parser_coset_hidden_involution_diagonal_charge_bias_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_diagonal_charge_bias_no_go.set_defaults(func=command_coset_hidden_involution_diagonal_charge_bias_no_go)


def command_coset_hidden_involution_diagonal_charge_bias_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_diagonal_charge_bias_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_diagonal_charge_bias_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_diagonal_charge_bias_no_go_report()
    validation = validate_registry()
    print("coset_hidden_involution_diagonal_charge_bias_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_diagonal_charge_bias_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_double_coset_polar_reduction(subparsers) -> None:
    parser_coset_hidden_involution_double_coset_polar_reduction = subparsers.add_parser(
        "coset-hidden-involution-double-coset-polar-reduction",
        help="Double-coset normal form for the hidden-involution row polar.",
    )
    parser_coset_hidden_involution_double_coset_polar_reduction.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_double_coset_polar_reduction.set_defaults(func=command_coset_hidden_involution_double_coset_polar_reduction)


def command_coset_hidden_involution_double_coset_polar_reduction(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_double_coset_polar_report
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_double_coset_polar_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_double_coset_polar_report()
    validation = validate_registry()
    print("coset_hidden_involution_double_coset_polar_reduction complete")
    print("Artifact: research/representation/coset_hidden_involution_double_coset_polar_reduction.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_hyperoctahedral_branching_mass(subparsers) -> None:
    parser_coset_hidden_involution_hyperoctahedral_branching_mass = subparsers.add_parser(
        "coset-hidden-involution-hyperoctahedral-branching-mass",
        help="Natural mass in large hyperoctahedral branching multiplicities.",
    )
    parser_coset_hidden_involution_hyperoctahedral_branching_mass.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_hyperoctahedral_branching_mass.set_defaults(func=command_coset_hidden_involution_hyperoctahedral_branching_mass)


def command_coset_hidden_involution_hyperoctahedral_branching_mass(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hyperoctahedral_branching_mass_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_hyperoctahedral_branching_mass_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_hyperoctahedral_branching_mass_report()
    validation = validate_registry()
    print("coset_hidden_involution_hyperoctahedral_branching_mass complete")
    print("Artifact: research/representation/coset_hidden_involution_hyperoctahedral_branching_mass.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_joint_primitive_ambient_lift_obstruction(subparsers) -> None:
    parser_coset_hidden_involution_joint_primitive_ambient_lift_obstruction = subparsers.add_parser(
        "coset-hidden-involution-joint-primitive-ambient-lift-obstruction",
        help="Schur-block obstruction to lifting the paired-tower label projector.",
    )
    parser_coset_hidden_involution_joint_primitive_ambient_lift_obstruction.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_joint_primitive_ambient_lift_obstruction.set_defaults(func=command_coset_hidden_involution_joint_primitive_ambient_lift_obstruction)


def command_coset_hidden_involution_joint_primitive_ambient_lift_obstruction(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_ambient_lift_report
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_ambient_lift_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_ambient_lift_report()
    validation = validate_registry()
    print("coset_hidden_involution_joint_primitive_ambient_lift_obstruction complete")
    print("Artifact: research/representation/coset_hidden_involution_joint_primitive_ambient_lift_obstruction.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_joint_primitive_representation_cone_obstruction(subparsers) -> None:
    parser_coset_hidden_involution_joint_primitive_representation_cone_obstruction = subparsers.add_parser(
        "coset-hidden-involution-joint-primitive-representation-cone-obstruction",
        help="Representation-cone obstruction for paired-tower primitive labels.",
    )
    parser_coset_hidden_involution_joint_primitive_representation_cone_obstruction.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_joint_primitive_representation_cone_obstruction.set_defaults(func=command_coset_hidden_involution_joint_primitive_representation_cone_obstruction)


def command_coset_hidden_involution_joint_primitive_representation_cone_obstruction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_representation_cone_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_representation_cone_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_representation_cone_report()
    validation = validate_registry()
    print("coset_hidden_involution_joint_primitive_representation_cone_obstruction complete")
    print("Artifact: research/representation/coset_hidden_involution_joint_primitive_representation_cone_obstruction.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_matching_charge_coherent_label_compiler(subparsers) -> None:
    parser_coset_hidden_involution_matching_charge_coherent_label_compiler = subparsers.add_parser(
        "coset-hidden-involution-matching-charge-coherent-label-compiler",
        help="Coherent sparse-LCU compiler for the natural matching-charge label.",
    )
    parser_coset_hidden_involution_matching_charge_coherent_label_compiler.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_matching_charge_coherent_label_compiler.set_defaults(func=command_coset_hidden_involution_matching_charge_coherent_label_compiler)


def command_coset_hidden_involution_matching_charge_coherent_label_compiler(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_coherent_label_compiler_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_coherent_label_compiler_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_coherent_label_compiler_report()
    validation = validate_registry()
    print("coset_hidden_involution_matching_charge_coherent_label_compiler complete")
    print("Artifact: research/representation/coset_hidden_involution_matching_charge_coherent_label_compiler.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_matching_charge_conditional_diameter(subparsers) -> None:
    parser_coset_hidden_involution_matching_charge_conditional_diameter = subparsers.add_parser(
        "coset-hidden-involution-matching-charge-conditional-diameter",
        help="Natural conditional spectral diameter for the matching charge ``D_m``.",
    )
    parser_coset_hidden_involution_matching_charge_conditional_diameter.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_matching_charge_conditional_diameter.set_defaults(func=command_coset_hidden_involution_matching_charge_conditional_diameter)


def command_coset_hidden_involution_matching_charge_conditional_diameter(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_conditional_diameter_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_conditional_diameter_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_conditional_diameter_report()
    validation = validate_registry()
    print("coset_hidden_involution_matching_charge_conditional_diameter complete")
    print("Artifact: research/representation/coset_hidden_involution_matching_charge_conditional_diameter.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_matching_charge_cs_correlation(subparsers) -> None:
    parser_coset_hidden_involution_matching_charge_cs_correlation = subparsers.add_parser(
        "coset-hidden-involution-matching-charge-cs-correlation",
        help="Finite matrix-CS correlation test for the natural matching charge.",
    )
    parser_coset_hidden_involution_matching_charge_cs_correlation.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_matching_charge_cs_correlation.set_defaults(func=command_coset_hidden_involution_matching_charge_cs_correlation)


def command_coset_hidden_involution_matching_charge_cs_correlation(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_matching_charge_CS_correlation_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_matching_charge_CS_correlation_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_matching_charge_CS_correlation_report()
    validation = validate_registry()
    print("coset_hidden_involution_matching_charge_cs_correlation complete")
    print("Artifact: research/representation/coset_hidden_involution_matching_charge_cs_correlation.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_matching_charge_natural_independence(subparsers) -> None:
    parser_coset_hidden_involution_matching_charge_natural_independence = subparsers.add_parser(
        "coset-hidden-involution-matching-charge-natural-independence",
        help="Natural-mass independence certificate for the matching charge ``D_m``.",
    )
    parser_coset_hidden_involution_matching_charge_natural_independence.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_matching_charge_natural_independence.set_defaults(func=command_coset_hidden_involution_matching_charge_natural_independence)


def command_coset_hidden_involution_matching_charge_natural_independence(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_matching_charge_natural_independence_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_matching_charge_natural_independence_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_matching_charge_natural_independence_report()
    validation = validate_registry()
    print("coset_hidden_involution_matching_charge_natural_independence complete")
    print("Artifact: research/representation/coset_hidden_involution_matching_charge_natural_independence.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_matching_charge_orbit_recoupling_reduction(subparsers) -> None:
    parser_coset_hidden_involution_matching_charge_orbit_recoupling_reduction = subparsers.add_parser(
        "coset-hidden-involution-matching-charge-orbit-recoupling-reduction",
        help="Faithful matching-charge orbit and target-recoupling reduction.",
    )
    parser_coset_hidden_involution_matching_charge_orbit_recoupling_reduction.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_matching_charge_orbit_recoupling_reduction.set_defaults(func=command_coset_hidden_involution_matching_charge_orbit_recoupling_reduction)


def command_coset_hidden_involution_matching_charge_orbit_recoupling_reduction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_charge_orbit_recoupling_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_charge_orbit_recoupling_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_charge_orbit_recoupling_report()
    validation = validate_registry()
    print("coset_hidden_involution_matching_charge_orbit_recoupling_reduction complete")
    print("Artifact: research/representation/coset_hidden_involution_matching_charge_orbit_recoupling_reduction.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_matching_charge_pairwise_kernel_dequantization(subparsers) -> None:
    parser_coset_hidden_involution_matching_charge_pairwise_kernel_dequantization = subparsers.add_parser(
        "coset-hidden-involution-matching-charge-pairwise-kernel-dequantization",
        help="Classical dequantization of the matching-charge pairwise kernel.",
    )
    parser_coset_hidden_involution_matching_charge_pairwise_kernel_dequantization.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_matching_charge_pairwise_kernel_dequantization.set_defaults(func=command_coset_hidden_involution_matching_charge_pairwise_kernel_dequantization)


def command_coset_hidden_involution_matching_charge_pairwise_kernel_dequantization(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pairwise_kernel_dequantization_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_pairwise_kernel_dequantization_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_pairwise_kernel_dequantization_report()
    validation = validate_registry()
    print("coset_hidden_involution_matching_charge_pairwise_kernel_dequantization complete")
    print("Artifact: research/representation/coset_hidden_involution_matching_charge_pairwise_kernel_dequantization.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_matching_charge_target_gauge_trivialization(subparsers) -> None:
    parser_coset_hidden_involution_matching_charge_target_gauge_trivialization = subparsers.add_parser(
        "coset-hidden-involution-matching-charge-target-gauge-trivialization",
        help="Gauge trivialization of naive target-controlled matching charges.",
    )
    parser_coset_hidden_involution_matching_charge_target_gauge_trivialization.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_matching_charge_target_gauge_trivialization.set_defaults(func=command_coset_hidden_involution_matching_charge_target_gauge_trivialization)


def command_coset_hidden_involution_matching_charge_target_gauge_trivialization(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_target_gauge_trivialization_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_target_gauge_trivialization_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_target_gauge_trivialization_report()
    validation = validate_registry()
    print("coset_hidden_involution_matching_charge_target_gauge_trivialization complete")
    print("Artifact: research/representation/coset_hidden_involution_matching_charge_target_gauge_trivialization.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_matching_charge_word_moment_dequantization(subparsers) -> None:
    parser_coset_hidden_involution_matching_charge_word_moment_dequantization = subparsers.add_parser(
        "coset-hidden-involution-matching-charge-word-moment-dequantization",
        help="All-degree classical estimator for matching-charge scalar word moments.",
    )
    parser_coset_hidden_involution_matching_charge_word_moment_dequantization.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_matching_charge_word_moment_dequantization.set_defaults(func=command_coset_hidden_involution_matching_charge_word_moment_dequantization)


def command_coset_hidden_involution_matching_charge_word_moment_dequantization(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_word_moment_dequantization_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_word_moment_dequantization_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_word_moment_dequantization_report()
    validation = validate_registry()
    print("coset_hidden_involution_matching_charge_word_moment_dequantization complete")
    print("Artifact: research/representation/coset_hidden_involution_matching_charge_word_moment_dequantization.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_mixed_hecke_word_lcu_no_go(subparsers) -> None:
    parser_coset_hidden_involution_mixed_hecke_word_lcu_no_go = subparsers.add_parser(
        "coset-hidden-involution-mixed-hecke-word-lcu-no-go",
        help="Mixed-word LCU no-go for diagonal all-copy hidden-involution charges.",
    )
    parser_coset_hidden_involution_mixed_hecke_word_lcu_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_mixed_hecke_word_lcu_no_go.set_defaults(func=command_coset_hidden_involution_mixed_hecke_word_lcu_no_go)


def command_coset_hidden_involution_mixed_hecke_word_lcu_no_go(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_mixed_word_LCU_report
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_mixed_word_LCU_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_mixed_word_LCU_report()
    validation = validate_registry()
    print("coset_hidden_involution_mixed_hecke_word_lcu_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_mixed_hecke_word_lcu_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_natural_matrix_multiplicity(subparsers) -> None:
    parser_coset_hidden_involution_natural_matrix_multiplicity = subparsers.add_parser(
        "coset-hidden-involution-natural-matrix-multiplicity",
        help="Natural-mass theorem for matrix-valued double-coset multiplicities.",
    )
    parser_coset_hidden_involution_natural_matrix_multiplicity.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_natural_matrix_multiplicity.set_defaults(func=command_coset_hidden_involution_natural_matrix_multiplicity)


def command_coset_hidden_involution_natural_matrix_multiplicity(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_matrix_multiplicity_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_natural_matrix_multiplicity_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_natural_matrix_multiplicity_report()
    validation = validate_registry()
    print("coset_hidden_involution_natural_matrix_multiplicity complete")
    print("Artifact: research/representation/coset_hidden_involution_natural_matrix_multiplicity.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_natural_recoupling_boundary(subparsers) -> None:
    parser_coset_hidden_involution_natural_recoupling_boundary = subparsers.add_parser(
        "coset-hidden-involution-natural-recoupling-boundary",
        help="Natural Kronecker-to-hyperoctahedral recoupling boundary.",
    )
    parser_coset_hidden_involution_natural_recoupling_boundary.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_natural_recoupling_boundary.set_defaults(func=command_coset_hidden_involution_natural_recoupling_boundary)


def command_coset_hidden_involution_natural_recoupling_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_recoupling_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_natural_recoupling_boundary_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_natural_recoupling_boundary_report()
    validation = validate_registry()
    print("coset_hidden_involution_natural_recoupling_boundary complete")
    print("Artifact: research/representation/coset_hidden_involution_natural_recoupling_boundary.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_normalized_likelihood_charge_commutator_no_go(subparsers) -> None:
    parser_coset_hidden_involution_normalized_likelihood_charge_commutator_no_go = subparsers.add_parser(
        "coset-hidden-involution-normalized-likelihood-charge-commutator-no-go",
        help="Natural-mass no-go for charge noncommutativity with normalized likelihood.",
    )
    parser_coset_hidden_involution_normalized_likelihood_charge_commutator_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_normalized_likelihood_charge_commutator_no_go.set_defaults(func=command_coset_hidden_involution_normalized_likelihood_charge_commutator_no_go)


def command_coset_hidden_involution_normalized_likelihood_charge_commutator_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_normalized_likelihood_charge_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_normalized_likelihood_charge_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_normalized_likelihood_charge_no_go_report()
    validation = validate_registry()
    print("coset_hidden_involution_normalized_likelihood_charge_commutator_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_normalized_likelihood_charge_commutator_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_occupied_matrix_rank(subparsers) -> None:
    parser_coset_hidden_involution_occupied_matrix_rank = subparsers.add_parser(
        "coset-hidden-involution-occupied-matrix-rank",
        help="Natural occupied-rank theorem for hidden-involution matrix CS blocks.",
    )
    parser_coset_hidden_involution_occupied_matrix_rank.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_occupied_matrix_rank.set_defaults(func=command_coset_hidden_involution_occupied_matrix_rank)


def command_coset_hidden_involution_occupied_matrix_rank(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_occupied_matrix_rank_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_occupied_matrix_rank_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_occupied_matrix_rank_report()
    validation = validate_registry()
    print("coset_hidden_involution_occupied_matrix_rank complete")
    print("Artifact: research/representation/coset_hidden_involution_occupied_matrix_rank.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_pair_gaudin_hierarchy(subparsers) -> None:
    parser_coset_hidden_involution_pair_gaudin_hierarchy = subparsers.add_parser(
        "coset-hidden-involution-pair-gaudin-hierarchy",
        help="A commuting pair-Gaudin hierarchy for hyperoctahedral recoupling.",
    )
    parser_coset_hidden_involution_pair_gaudin_hierarchy.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_pair_gaudin_hierarchy.set_defaults(func=command_coset_hidden_involution_pair_gaudin_hierarchy)


def command_coset_hidden_involution_pair_gaudin_hierarchy(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_gaudin_hierarchy_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_pair_gaudin_hierarchy_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_pair_gaudin_hierarchy_report()
    validation = validate_registry()
    print("coset_hidden_involution_pair_gaudin_hierarchy complete")
    print("Artifact: research/representation/coset_hidden_involution_pair_gaudin_hierarchy.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_pair_matching_charge_hierarchy(subparsers) -> None:
    parser_coset_hidden_involution_pair_matching_charge_hierarchy = subparsers.add_parser(
        "coset-hidden-involution-pair-matching-charge-hierarchy",
        help="A K-adapted commuting charge pair from pair-Gaudin interactions.",
    )
    parser_coset_hidden_involution_pair_matching_charge_hierarchy.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_pair_matching_charge_hierarchy.set_defaults(func=command_coset_hidden_involution_pair_matching_charge_hierarchy)


def command_coset_hidden_involution_pair_matching_charge_hierarchy(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_matching_charge_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_pair_matching_charge_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_pair_matching_charge_report()
    validation = validate_registry()
    print("coset_hidden_involution_pair_matching_charge_hierarchy complete")
    print("Artifact: research/representation/coset_hidden_involution_pair_matching_charge_hierarchy.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_paired_tower_joint_primitive_projector(subparsers) -> None:
    parser_coset_hidden_involution_paired_tower_joint_primitive_projector = subparsers.add_parser(
        "coset-hidden-involution-paired-tower-joint-primitive-projector",
        help="Polynomial-query projector for paired-tower joint primitive labels.",
    )
    parser_coset_hidden_involution_paired_tower_joint_primitive_projector.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_paired_tower_joint_primitive_projector.set_defaults(func=command_coset_hidden_involution_paired_tower_joint_primitive_projector)


def command_coset_hidden_involution_paired_tower_joint_primitive_projector(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_joint_primitive_projector_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_joint_primitive_projector_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_joint_primitive_projector_report()
    validation = validate_registry()
    print("coset_hidden_involution_paired_tower_joint_primitive_projector complete")
    print("Artifact: research/representation/coset_hidden_involution_paired_tower_joint_primitive_projector.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_paired_tower_missing_label_boundary(subparsers) -> None:
    parser_coset_hidden_involution_paired_tower_missing_label_boundary = subparsers.add_parser(
        "coset-hidden-involution-paired-tower-missing-label-boundary",
        help="Paired Young-tower boundary for hyperoctahedral missing labels.",
    )
    parser_coset_hidden_involution_paired_tower_missing_label_boundary.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_paired_tower_missing_label_boundary.set_defaults(func=command_coset_hidden_involution_paired_tower_missing_label_boundary)


def command_coset_hidden_involution_paired_tower_missing_label_boundary(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_paired_tower_missing_label_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_paired_tower_missing_label_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_paired_tower_missing_label_report()
    validation = validate_registry()
    print("coset_hidden_involution_paired_tower_missing_label_boundary complete")
    print("Artifact: research/representation/coset_hidden_involution_paired_tower_missing_label_boundary.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_physical_target_convolution_normal_form(subparsers) -> None:
    parser_coset_hidden_involution_physical_target_convolution_normal_form = subparsers.add_parser(
        "coset-hidden-involution-physical-target-convolution-normal-form",
        help="Physical quotient normal form for genuine target-changing convolution.",
    )
    parser_coset_hidden_involution_physical_target_convolution_normal_form.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_physical_target_convolution_normal_form.set_defaults(func=command_coset_hidden_involution_physical_target_convolution_normal_form)


def command_coset_hidden_involution_physical_target_convolution_normal_form(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_physical_target_convolution_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_physical_target_convolution_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_physical_target_convolution_report()
    validation = validate_registry()
    print("coset_hidden_involution_physical_target_convolution_normal_form complete")
    print("Artifact: research/representation/coset_hidden_involution_physical_target_convolution_normal_form.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_plancherel_local_commutant_certificate(subparsers) -> None:
    parser_coset_hidden_involution_plancherel_local_commutant_certificate = subparsers.add_parser(
        "coset-hidden-involution-plancherel-local-commutant-certificate",
        help="Natural-mass certificate for a local hyperoctahedral commutator.",
    )
    parser_coset_hidden_involution_plancherel_local_commutant_certificate.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_plancherel_local_commutant_certificate.set_defaults(func=command_coset_hidden_involution_plancherel_local_commutant_certificate)


def command_coset_hidden_involution_plancherel_local_commutant_certificate(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_plancherel_local_commutant_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_plancherel_local_commutant_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_plancherel_local_commutant_report()
    validation = validate_registry()
    print("coset_hidden_involution_plancherel_local_commutant_certificate complete")
    print("Artifact: research/representation/coset_hidden_involution_plancherel_local_commutant_certificate.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_rank_tracking_commutant_witness(subparsers) -> None:
    parser_coset_hidden_involution_rank_tracking_commutant_witness = subparsers.add_parser(
        "coset-hidden-involution-rank-tracking-commutant-witness",
        help="Rank-tracking support witness for hyperoctahedral commutant generation.",
    )
    parser_coset_hidden_involution_rank_tracking_commutant_witness.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_rank_tracking_commutant_witness.set_defaults(func=command_coset_hidden_involution_rank_tracking_commutant_witness)


def command_coset_hidden_involution_rank_tracking_commutant_witness(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_rank_tracking_commutant_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_rank_tracking_commutant_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_rank_tracking_commutant_report()
    validation = validate_registry()
    print("coset_hidden_involution_rank_tracking_commutant_witness complete")
    print("Artifact: research/representation/coset_hidden_involution_rank_tracking_commutant_witness.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_multiplicity_twirl_projection(subparsers) -> None:
    parser_coset_hidden_involution_multiplicity_twirl_projection = subparsers.add_parser(
        "coset-hidden-involution-multiplicity-twirl-projection",
        help="Project bounded-support hyperoctahedral orbit representatives directly into repeated multiplicity blocks and audit support growth.",
    )
    parser_coset_hidden_involution_multiplicity_twirl_projection.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_multiplicity_twirl_projection.set_defaults(func=command_coset_hidden_involution_multiplicity_twirl_projection)


def command_coset_hidden_involution_multiplicity_twirl_projection(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_multiplicity_twirl_projection_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_multiplicity_twirl_projection_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    gate = payload.get("claim_gate", {})
    print("coset_hidden_involution_multiplicity_twirl_projection complete")
    print(
        "Compressed orbit projection verified: "
        f"{gate.get('compressed_orbit_representative_method_verified', False)}"
    )
    print(
        "Strict rank-tracking growth falsified: "
        f"{gate.get('strict_rank_tracking_support_growth_falsified', False)}"
    )
    print(
        "Uniform support-six theorem: "
        f"{gate.get('universal_support_six_generation_proved', False)}"
    )
    print(f"Speedup claim allowed: {gate.get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_multiplicity_fiber_trace(subparsers) -> None:
    parser_coset_hidden_involution_multiplicity_fiber_trace = subparsers.add_parser(
        "coset-hidden-involution-multiplicity-fiber-trace",
        help="Contract exact hyperoctahedral copy matrices through one signed YJM multiplicity fiber without forming a full isotypic basis.",
    )
    parser_coset_hidden_involution_multiplicity_fiber_trace.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_multiplicity_fiber_trace.set_defaults(func=command_coset_hidden_involution_multiplicity_fiber_trace)


def command_coset_hidden_involution_multiplicity_fiber_trace(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_multiplicity_fiber_trace_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_multiplicity_fiber_trace_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    gate = payload.get("claim_gate", {})
    print("coset_hidden_involution_multiplicity_fiber_trace complete")
    print(
        "Exact copy-fiber trace verified: "
        f"{gate.get('exact_copy_fiber_trace_verified', False)}"
    )
    print(
        "Polynomial typical compression proved: "
        f"{gate.get('polynomial_typical_ambient_compression_proved', False)}"
    )
    print(
        "Coherent multiplicity transform: "
        f"{gate.get('coherent_multiplicity_transform_compiled', False)}"
    )
    print(f"Speedup claim allowed: {gate.get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_high_mass_support_scan(subparsers) -> None:
    parser_coset_hidden_involution_high_mass_support_scan = subparsers.add_parser(
        "coset-hidden-involution-high-mass-support-scan",
        help="Test bounded-support copy-algebra generation on the highest-mass untested repeated S_14 branch.",
    )
    parser_coset_hidden_involution_high_mass_support_scan.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_high_mass_support_scan.set_defaults(func=command_coset_hidden_involution_high_mass_support_scan)


def command_coset_hidden_involution_high_mass_support_scan(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_high_mass_support_scan_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_high_mass_support_scan_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    gate = payload.get("claim_gate", {})
    print("coset_hidden_involution_high_mass_support_scan complete")
    print(
        "Target natural mass: "
        f"{metrics.get('target_natural_mass_probability', 0.0):.12f}"
    )
    print(
        "Support-three algebra dimension: "
        f"{metrics.get('support_three_generated_algebra_dimension', 0)}"
    )
    print(
        "Support-four full copy algebra: "
        f"{gate.get('support_four_full_copy_algebra_numerically_certified', False)}"
    )
    print(
        "Direct commutant nullity: "
        f"{metrics.get('support_four_direct_commutant_nullity', 0)}"
    )
    print(f"Speedup claim allowed: {gate.get('speedup_claim_allowed', False)}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_source_weighted_support_portfolio(subparsers) -> None:
    portfolio = subparsers.add_parser("coset-hidden-involution-source-weighted-support-portfolio",
                                      help="Scan exact source-ranked multiplicity blocks with numerical commutant diagnostics.")
    portfolio.add_argument("--target-count", type=int, default=5)
    portfolio.add_argument("--no-registry", action="store_true")
    portfolio.set_defaults(func=command_coset_hidden_involution_source_weighted_support_portfolio)


def command_coset_hidden_involution_source_weighted_support_portfolio(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_source_weighted_support_portfolio_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_source_weighted_support_portfolio_report(
        write_registry=not args.no_registry, target_count=args.target_count,
    )
    print(payload["summary"])
    print(json.dumps(payload["headline_metrics"], indent=2))
    return 0 if validate_registry()["valid"] else 1


def add_coset_hidden_involution_spectral_label_budget(subparsers) -> None:
    label_budget = subparsers.add_parser("coset-hidden-involution-spectral-label-budget",
                                         help="Audit the exact source-mass capacity of normalized spectral labels.")
    label_budget.add_argument("--no-registry", action="store_true")
    label_budget.set_defaults(func=command_coset_hidden_involution_spectral_label_budget)


def command_coset_hidden_involution_spectral_label_budget(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_spectral_label_budget_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_spectral_label_budget_report(write_registry=not args.no_registry)
    print(payload["summary"])
    print(json.dumps(payload["headline_metrics"], indent=2))
    return 0 if validate_registry()["valid"] else 1


def add_coset_hidden_involution_signed_tensor_access(subparsers) -> None:
    signed_access = subparsers.add_parser("coset-hidden-involution-signed-tensor-access",
                                          help="Audit signed-tensor diagram degrees against natural K-type source mass.")
    signed_access.add_argument("--no-registry", action="store_true")
    signed_access.set_defaults(func=command_coset_hidden_involution_signed_tensor_access)


def command_coset_hidden_involution_signed_tensor_access(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_signed_tensor_access_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_signed_tensor_access_report(write_registry=not args.no_registry)
    print(payload["summary"])
    print(json.dumps(payload["headline_metrics"], indent=2))
    return 0 if validate_registry()["valid"] else 1


def add_coset_hidden_involution_encoded_restriction(subparsers) -> None:
    encoded_access = subparsers.add_parser("coset-hidden-involution-encoded-restriction",
                                           help="Verify normalized subgroup carrier extraction with an implicit copy code.")
    encoded_access.add_argument("--no-registry", action="store_true")
    encoded_access.set_defaults(func=command_coset_hidden_involution_encoded_restriction)


def command_coset_hidden_involution_encoded_restriction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_encoded_restriction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_encoded_restriction_report(write_registry=not args.no_registry)
    print(payload["summary"])
    print(json.dumps(payload["headline_metrics"], indent=2))
    return 0 if validate_registry()["valid"] else 1


def add_coset_hidden_involution_reference_twirl_information(subparsers) -> None:
    reference_information = subparsers.add_parser("coset-hidden-involution-reference-twirl-information",
        help="Audit binary information lost by independent reference-carrier discard.")
    reference_information.add_argument("--no-registry", action="store_true")
    reference_information.set_defaults(func=command_coset_hidden_involution_reference_twirl_information)


def command_coset_hidden_involution_reference_twirl_information(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_reference_twirl_information_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_reference_twirl_information_report(write_registry=not args.no_registry)
    print(payload["summary"])
    print(json.dumps(payload["headline_metrics"], indent=2))
    return 0 if validate_registry()["valid"] else 1


def add_coset_overlap_transfer(subparsers) -> None:
    overlap_transfer = subparsers.add_parser(
        "coset-overlap-transfer", help="Evaluate exact long-path echo transfer and scoped all-copy decay certificates."
    )
    overlap_transfer.add_argument("--no-registry", action="store_true")
    overlap_transfer.add_argument("--replay", action="store_true", help="Read-only exact replay of saved S6 decay witnesses.")
    overlap_transfer.set_defaults(func=command_coset_overlap_transfer)


def command_coset_overlap_transfer(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, replay_transfer_report, write_transfer_report
    if args.replay:
        result = replay_transfer_report()
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1
    if not args.no_registry:
        initialize_seed_registry(overwrite=False)
    payload = write_transfer_report(write_registry=not args.no_registry)
    print(payload["summary"])
    print(json.dumps(payload["headline_metrics"], indent=2))
    return 0 if payload["claim_gate"]["exact_transfer_controls_verified"] else 1


def add_coset_overlap_echo(subparsers) -> None:
    overlap_echo = subparsers.add_parser(
        "coset-overlap-echo", help="Evaluate costed coherent nonmissing-sector echoes and actual X-readout laws."
    )
    overlap_echo.add_argument("--no-registry", action="store_true")
    overlap_echo.set_defaults(func=command_coset_overlap_echo)


def command_coset_overlap_echo(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, write_overlap_echo_report
    if not args.no_registry:
        initialize_seed_registry(overwrite=False)
    payload = write_overlap_echo_report(write_registry=not args.no_registry)
    print(payload["summary"])
    print(json.dumps(payload["headline_metrics"], indent=2))
    return 0 if payload["claim_gate"]["finite_controls_verified"] else 1


def add_coset_missing_harmonic(subparsers) -> None:
    missing_harmonic = subparsers.add_parser(
        "coset-missing-harmonic", help="Audit the retained-data missing-sign detector and its amplification cost."
    )
    missing_harmonic.add_argument("--no-registry", action="store_true")
    missing_harmonic.set_defaults(func=command_coset_missing_harmonic_detector)


def command_coset_missing_harmonic_detector(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, write_missing_harmonic_report
    if not args.no_registry:
        initialize_seed_registry(overwrite=False)
    payload = write_missing_harmonic_report(write_registry=not args.no_registry)
    print(payload["summary"])
    print(payload["source_adaptive_research_update"])
    print(json.dumps(payload["headline_metrics"], indent=2))
    return 0 if payload["claim_gate"]["finite_physical_controls_verified"] else 1


def add_coset_binary_carrier_instruments(subparsers) -> None:
    binary_instruments = subparsers.add_parser("coset-binary-carrier-instruments",
        help="Audit noncentral selectors, radial masks, and scoped tail/vacuum-coherence information bounds.")
    binary_instruments.add_argument("--no-registry", action="store_true")
    binary_instruments.set_defaults(func=command_coset_binary_carrier_instruments)


def command_coset_binary_carrier_instruments(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_binary_carrier_instrument_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_binary_carrier_instrument_report(write_registry=not args.no_registry)
    print(payload["summary"])
    print(payload["mask_tail_research_update"])
    print(payload["selector_mask_symmetry_research_update"])
    print(payload["vacuum_coherence_research_update"])
    print(payload["low_occupation_research_update"])
    print(payload["occupation_band_research_update"])
    print(payload["selector_schur_research_update"])
    print(payload["selector_coefficient_mass_research_update"])
    print(json.dumps(payload["headline_metrics"], indent=2))
    return 0 if validate_registry()["valid"] and payload["claim_gate"]["finite_complete_channel_evaluation_verified"] else 1


def add_coset_hidden_involution_natural_support_six_mass_audit(subparsers) -> None:
    parser_coset_hidden_involution_natural_support_six_mass_audit = subparsers.add_parser(
        "coset-hidden-involution-natural-support-six-mass-audit",
        help="Measure exact natural-source coverage of finite support-six multiplicity controls and rank untested high-mass blocks.",
    )
    parser_coset_hidden_involution_natural_support_six_mass_audit.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_natural_support_six_mass_audit.set_defaults(func=command_coset_hidden_involution_natural_support_six_mass_audit)


def command_coset_hidden_involution_natural_support_six_mass_audit(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_support_six_mass_audit,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_natural_support_six_mass_audit(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload.get("headline_metrics", {})
    print("coset_hidden_involution_natural_support_six_mass_audit complete")
    print(
        "Repeated natural mass: "
        f"{metrics.get('repeated_natural_mass_probability', 0.0):.12f}"
    )
    print(
        "Audited support-six natural mass: "
        f"{metrics.get('audited_rank_natural_mass_probability', 0.0):.12g}"
    )
    print(
        "Uniform support-six theorem: "
        f"{payload.get('claim_gate', {}).get('uniform_support_six_generation_proved', False)}"
    )
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_shared_conjugation_qsvt_lower_bound(subparsers) -> None:
    parser_coset_hidden_involution_shared_conjugation_qsvt_lower_bound = subparsers.add_parser(
        "coset-hidden-involution-shared-conjugation-qsvt-lower-bound",
        help="QSVT lower bound for the shared-conjugation likelihood average.",
    )
    parser_coset_hidden_involution_shared_conjugation_qsvt_lower_bound.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_shared_conjugation_qsvt_lower_bound.set_defaults(func=command_coset_hidden_involution_shared_conjugation_qsvt_lower_bound)


def command_coset_hidden_involution_shared_conjugation_qsvt_lower_bound(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_shared_conjugation_QSVT_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_shared_conjugation_QSVT_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_shared_conjugation_QSVT_report()
    validation = validate_registry()
    print("coset_hidden_involution_shared_conjugation_qsvt_lower_bound complete")
    print("Artifact: research/representation/coset_hidden_involution_shared_conjugation_QSVT_lower_bound.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_single_hecke_all_degree_moment_no_go(subparsers) -> None:
    parser_coset_hidden_involution_single_hecke_all_degree_moment_no_go = subparsers.add_parser(
        "coset-hidden-involution-single-hecke-all-degree-moment-no-go",
        help="All-degree moment no-go for a single nontrivial binary Hecke walk.",
    )
    parser_coset_hidden_involution_single_hecke_all_degree_moment_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_single_hecke_all_degree_moment_no_go.set_defaults(func=command_coset_hidden_involution_single_hecke_all_degree_moment_no_go)


def command_coset_hidden_involution_single_hecke_all_degree_moment_no_go(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_all_degree_moment_report
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_all_degree_moment_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_all_degree_moment_report()
    validation = validate_registry()
    print("coset_hidden_involution_single_hecke_all_degree_moment_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_single_hecke_all_degree_moment_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_single_hecke_bounded_spectral_no_go(subparsers) -> None:
    parser_coset_hidden_involution_single_hecke_bounded_spectral_no_go = subparsers.add_parser(
        "coset-hidden-involution-single-hecke-bounded-spectral-no-go",
        help="Bounded-polynomial spectral no-go for one hidden-involution Hecke walk.",
    )
    parser_coset_hidden_involution_single_hecke_bounded_spectral_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_single_hecke_bounded_spectral_no_go.set_defaults(func=command_coset_hidden_involution_single_hecke_bounded_spectral_no_go)


def command_coset_hidden_involution_single_hecke_bounded_spectral_no_go(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_bounded_spectral_report
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_bounded_spectral_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_bounded_spectral_report()
    validation = validate_registry()
    print("coset_hidden_involution_single_hecke_bounded_spectral_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_single_hecke_bounded_spectral_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_source_local_likelihood_no_go(subparsers) -> None:
    parser_coset_hidden_involution_source_local_likelihood_no_go = subparsers.add_parser(
        "coset-hidden-involution-source-local-likelihood-no-go",
        help="Exact no-go theorem for source-local hidden-involution charges.",
    )
    parser_coset_hidden_involution_source_local_likelihood_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_source_local_likelihood_no_go.set_defaults(func=command_coset_hidden_involution_source_local_likelihood_no_go)


def command_coset_hidden_involution_source_local_likelihood_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_source_local_likelihood_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_source_local_likelihood_no_go_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_source_local_likelihood_no_go_report()
    validation = validate_registry()
    print("coset_hidden_involution_source_local_likelihood_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_source_local_likelihood_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_stable_support_six_certificate(subparsers) -> None:
    parser_coset_hidden_involution_stable_support_six_certificate = subparsers.add_parser(
        "coset-hidden-involution-stable-support-six-certificate",
        help="All-rank low-support certificate for one hyperoctahedral copy space.",
    )
    parser_coset_hidden_involution_stable_support_six_certificate.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_stable_support_six_certificate.set_defaults(func=command_coset_hidden_involution_stable_support_six_certificate)


def command_coset_hidden_involution_stable_support_six_certificate(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_stable_support_six_report
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_stable_support_six_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_stable_support_six_report()
    validation = validate_registry()
    print("coset_hidden_involution_stable_support_six_certificate complete")
    print("Artifact: research/representation/coset_hidden_involution_stable_support_six_certificate.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_standard_block_recoupling(subparsers) -> None:
    parser_coset_hidden_involution_standard_block_recoupling = subparsers.add_parser(
        "coset-hidden-involution-standard-block-recoupling",
        help="Exact recoupling spectrum of the all-standard hidden-involution block.",
    )
    parser_coset_hidden_involution_standard_block_recoupling.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_standard_block_recoupling.set_defaults(func=command_coset_hidden_involution_standard_block_recoupling)


def command_coset_hidden_involution_standard_block_recoupling(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_standard_block_recoupling_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_standard_block_recoupling_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_standard_block_recoupling_report()
    validation = validate_registry()
    print("coset_hidden_involution_standard_block_recoupling complete")
    print("Artifact: research/representation/coset_hidden_involution_standard_block_recoupling.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_target_interference_negativity_barrier(subparsers) -> None:
    parser_coset_hidden_involution_target_interference_negativity_barrier = subparsers.add_parser(
        "coset-hidden-involution-target-interference-negativity-barrier",
        help="Exact group-basis negativity barrier for any useful detector.",
    )
    parser_coset_hidden_involution_target_interference_negativity_barrier.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_target_interference_negativity_barrier.set_defaults(func=command_coset_hidden_involution_target_interference_negativity_barrier)


def command_coset_hidden_involution_target_interference_negativity_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_negativity_barrier_report
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_negativity_barrier_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_negativity_barrier_report()
    validation = validate_registry()
    print("coset_hidden_involution_target_interference_negativity_barrier complete")
    print("Artifact: research/representation/coset_hidden_involution_target_interference_negativity_barrier.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_trimmed_row_block_encoding_no_go(subparsers) -> None:
    parser_coset_hidden_involution_trimmed_row_block_encoding_no_go = subparsers.add_parser(
        "coset-hidden-involution-trimmed-row-block-encoding-no-go",
        help="Normalization no-go for coherent access to the trimmed orbit-row kernel.",
    )
    parser_coset_hidden_involution_trimmed_row_block_encoding_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_trimmed_row_block_encoding_no_go.set_defaults(func=command_coset_hidden_involution_trimmed_row_block_encoding_no_go)


def command_coset_hidden_involution_trimmed_row_block_encoding_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_trimmed_row_block_encoding_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_trimmed_row_block_encoding_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_trimmed_row_block_encoding_report()
    validation = validate_registry()
    print("coset_hidden_involution_trimmed_row_block_encoding_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_trimmed_row_block_encoding_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_trimmed_row_kernel_succinctness(subparsers) -> None:
    parser_coset_hidden_involution_trimmed_row_kernel_succinctness = subparsers.add_parser(
        "coset-hidden-involution-trimmed-row-kernel-succinctness",
        help="Pairwise succinctness and the true trimmed row-polar boundary.",
    )
    parser_coset_hidden_involution_trimmed_row_kernel_succinctness.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_trimmed_row_kernel_succinctness.set_defaults(func=command_coset_hidden_involution_trimmed_row_kernel_succinctness)


def command_coset_hidden_involution_trimmed_row_kernel_succinctness(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_trimmed_row_kernel_report
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_trimmed_row_kernel_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_trimmed_row_kernel_report()
    validation = validate_registry()
    print("coset_hidden_involution_trimmed_row_kernel_succinctness complete")
    print("Artifact: research/representation/coset_hidden_involution_trimmed_row_kernel_succinctness.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_hidden_involution_two_subgroup_projector_algebra_no_go(subparsers) -> None:
    parser_coset_hidden_involution_two_subgroup_projector_algebra_no_go = subparsers.add_parser(
        "coset-hidden-involution-two-subgroup-projector-algebra-no-go",
        help="Two-subgroup-projector algebra reduces to one-variable likelihood QSVT.",
    )
    parser_coset_hidden_involution_two_subgroup_projector_algebra_no_go.add_argument("--no-registry", action="store_true")
    parser_coset_hidden_involution_two_subgroup_projector_algebra_no_go.set_defaults(func=command_coset_hidden_involution_two_subgroup_projector_algebra_no_go)


def command_coset_hidden_involution_two_subgroup_projector_algebra_no_go(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_two_projector_algebra_report,
    )
    initialize_seed_registry(overwrite=False)
    try:
        payload = write_two_projector_algebra_report(write_registry=not args.no_registry)
    except TypeError:
        payload = write_two_projector_algebra_report()
    validation = validate_registry()
    print("coset_hidden_involution_two_subgroup_projector_algebra_no_go complete")
    print("Artifact: research/representation/coset_hidden_involution_two_subgroup_projector_algebra_no_go.json")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_coset_multiplicity_carrier_trilemma(subparsers) -> None:
    coset_multiplicity_carrier_trilemma = subparsers.add_parser(
        "coset-multiplicity-carrier-trilemma",
        help="Check scoped coset identities and structured pair access; quarantine the unsupported general trilemma.",
    )
    coset_multiplicity_carrier_trilemma.add_argument("--no-registry", action="store_true")
    coset_multiplicity_carrier_trilemma.set_defaults(func=command_coset_multiplicity_carrier_trilemma)


def command_coset_multiplicity_carrier_trilemma(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.coset_multiplicity_carrier_trilemma import REPORT, write_report
    write_report(write_registry=not getattr(args, "no_registry", False))
    validation = validate_registry()
    print("Coset scope checks complete; broad trilemma retracted, no general circuit lower bound.")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1
