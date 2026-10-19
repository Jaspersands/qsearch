"""Native higher-call subcommands, moved out of qsearch.py by tools/split_cli/migrate.py.

Each ``add_*`` function registers one subcommand and each ``command_*`` function runs one.
A command imports what it needs from ``qsearch`` when it runs, so loading this module stays
cheap and ``monkeypatch.setattr(qsearch, name, ...)`` still reaches the command.
"""

from __future__ import annotations

import argparse
import json



def add_native_higher_call_signed_path_valuation_audit(subparsers) -> None:
    native_higher_call_signed_path_valuation_audit = subparsers.add_parser(
        "native-higher-call-signed-path-valuation-audit",
        help="Audit higher-call signed response path Z_3-coset invariants, sign-schedule invariance, and the universal 1/3 non-unit valuation law.",
    )
    native_higher_call_signed_path_valuation_audit.add_argument("--no-write", action="store_true")
    native_higher_call_signed_path_valuation_audit.set_defaults(func=command_native_higher_call_signed_path_valuation_audit)


def command_native_higher_call_signed_path_valuation_audit(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_signed_path_valuation_audit import (
        build_native_higher_call_signed_path_valuation_audit_report,
        write_native_higher_call_signed_path_valuation_audit_report,
    )

    payload = (
        build_native_higher_call_signed_path_valuation_audit_report()
        if args.no_write
        else write_native_higher_call_signed_path_valuation_audit_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_prime_power_survival_closed_form(subparsers) -> None:
    native_higher_call_prime_power_survival_closed_form = subparsers.add_parser(
        "native-higher-call-prime-power-survival-closed-form",
        help="Audit Eisenstein root-of-unity isomorphism, squared-trinomial zero-difference law, and prime-power Fourier survival spectra.",
    )
    native_higher_call_prime_power_survival_closed_form.add_argument("--no-write", action="store_true")
    native_higher_call_prime_power_survival_closed_form.set_defaults(func=command_native_higher_call_prime_power_survival_closed_form)


def command_native_higher_call_prime_power_survival_closed_form(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_prime_power_survival_closed_form import (
        build_native_higher_call_prime_power_survival_closed_form_report,
        write_native_higher_call_prime_power_survival_closed_form_report,
    )

    payload = (
        build_native_higher_call_prime_power_survival_closed_form_report()
        if args.no_write
        else write_native_higher_call_prime_power_survival_closed_form_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_weighted_fourier_pinching_audit(subparsers) -> None:
    native_higher_call_weighted_fourier_pinching_audit = subparsers.add_parser(
        "native-higher-call-weighted-fourier-pinching-audit",
        help="Audit general k-call weighted Fourier pinching varieties, 1/D diagonal floor conservation, and zero-mean off-diagonal interference.",
    )
    native_higher_call_weighted_fourier_pinching_audit.add_argument("--no-write", action="store_true")
    native_higher_call_weighted_fourier_pinching_audit.set_defaults(func=command_native_higher_call_weighted_fourier_pinching_audit)


def command_native_higher_call_weighted_fourier_pinching_audit(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_weighted_fourier_pinching_audit import (
        build_native_higher_call_weighted_fourier_pinching_audit,
        write_native_higher_call_weighted_fourier_pinching_audit,
    )

    payload = (
        build_native_higher_call_weighted_fourier_pinching_audit()
        if args.no_write
        else write_native_higher_call_weighted_fourier_pinching_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_prime_power_divisibility_hierarchy_audit(subparsers) -> None:
    native_higher_call_prime_power_divisibility_hierarchy_audit = subparsers.add_parser(
        "native-higher-call-prime-power-divisibility-hierarchy-audit",
        help="Audit p-adic subgroup pinching filtration, telescoping valuation shells, and zero-sum shell increments for prime-power LWE.",
    )
    native_higher_call_prime_power_divisibility_hierarchy_audit.add_argument("--no-write", action="store_true")
    native_higher_call_prime_power_divisibility_hierarchy_audit.set_defaults(func=command_native_higher_call_prime_power_divisibility_hierarchy_audit)


def command_native_higher_call_prime_power_divisibility_hierarchy_audit(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_prime_power_divisibility_hierarchy_audit import (
        build_native_higher_call_prime_power_divisibility_hierarchy_audit,
        write_native_higher_call_prime_power_divisibility_hierarchy_audit,
    )

    payload = (
        build_native_higher_call_prime_power_divisibility_hierarchy_audit()
        if args.no_write
        else write_native_higher_call_prime_power_divisibility_hierarchy_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_kronecker_moment_rank_bridge(subparsers) -> None:
    native_higher_call_kronecker_moment_rank_bridge = subparsers.add_parser(
        "native-higher-call-kronecker-moment-rank-bridge",
        help="Audit native higher-call Kronecker moment-rank bridges, non-scalar commutant bounds, and rank-deficiency witnesses.",
    )
    native_higher_call_kronecker_moment_rank_bridge.add_argument("--no-write", action="store_true")
    native_higher_call_kronecker_moment_rank_bridge.set_defaults(func=command_native_higher_call_kronecker_moment_rank_bridge)


def command_native_higher_call_kronecker_moment_rank_bridge(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_kronecker_moment_rank_bridge import (
        build_native_higher_call_kronecker_moment_rank_bridge,
        write_native_higher_call_kronecker_moment_rank_bridge,
    )

    payload = (
        build_native_higher_call_kronecker_moment_rank_bridge()
        if args.no_write
        else write_native_higher_call_kronecker_moment_rank_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_commutant_trace_orthogonality_audit(subparsers) -> None:
    native_higher_call_commutant_trace_orthogonality_audit = subparsers.add_parser(
        "native-higher-call-commutant-trace-orthogonality-audit",
        help="Audit operator harmonic zero-trace conservation, purity-deficit Parseval identity, and universal unitary readout bounds.",
    )
    native_higher_call_commutant_trace_orthogonality_audit.add_argument("--no-write", action="store_true")
    native_higher_call_commutant_trace_orthogonality_audit.set_defaults(func=command_native_higher_call_commutant_trace_orthogonality_audit)


def command_native_higher_call_commutant_trace_orthogonality_audit(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_commutant_trace_orthogonality_audit import (
        build_native_higher_call_commutant_trace_orthogonality_audit,
        write_native_higher_call_commutant_trace_orthogonality_audit,
    )

    payload = (
        build_native_higher_call_commutant_trace_orthogonality_audit()
        if args.no_write
        else write_native_higher_call_commutant_trace_orthogonality_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_two_copy_swap_purity_bridge(subparsers) -> None:
    native_higher_call_two_copy_swap_purity_bridge = subparsers.add_parser(
        "native-higher-call-two-copy-swap-purity-bridge",
        help="Audit two-copy SWAP purity excess vs classical coincidence excess, 1-call variety purity law, and CNOT autocorrelation.",
    )
    native_higher_call_two_copy_swap_purity_bridge.add_argument("--no-write", action="store_true")
    native_higher_call_two_copy_swap_purity_bridge.set_defaults(func=command_native_higher_call_two_copy_swap_purity_bridge)


def command_native_higher_call_two_copy_swap_purity_bridge(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_two_copy_swap_purity_bridge import (
        build_native_higher_call_two_copy_swap_purity_bridge,
        write_native_higher_call_two_copy_swap_purity_bridge,
    )

    payload = (
        build_native_higher_call_two_copy_swap_purity_bridge()
        if args.no_write
        else write_native_higher_call_two_copy_swap_purity_bridge()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_error_table_gauge_invariance_audit(subparsers) -> None:
    native_higher_call_error_table_gauge_invariance_audit = subparsers.add_parser(
        "native-higher-call-error-table-gauge-invariance-audit",
        help="Audit affine-secret error-gauge covariance, injective-frequency purity pinning, and universal word-multiplicity pinching.",
    )
    native_higher_call_error_table_gauge_invariance_audit.add_argument("--no-write", action="store_true")
    native_higher_call_error_table_gauge_invariance_audit.set_defaults(func=command_native_higher_call_error_table_gauge_invariance_audit)


def command_native_higher_call_error_table_gauge_invariance_audit(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_error_table_gauge_invariance_audit import (
        build_native_higher_call_error_table_gauge_invariance_audit,
        write_native_higher_call_error_table_gauge_invariance_audit,
    )

    payload = (
        build_native_higher_call_error_table_gauge_invariance_audit()
        if args.no_write
        else write_native_higher_call_error_table_gauge_invariance_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_time_reversal_schedule_duality_audit(subparsers) -> None:
    native_higher_call_time_reversal_schedule_duality_audit = subparsers.add_parser(
        "native-higher-call-time-reversal-schedule-duality-audit",
        help="Audit global sign-conjugation invariance, Klein four-group schedule reduction, and symmetric-transpose time-reversal duality.",
    )
    native_higher_call_time_reversal_schedule_duality_audit.add_argument("--no-write", action="store_true")
    native_higher_call_time_reversal_schedule_duality_audit.set_defaults(func=command_native_higher_call_time_reversal_schedule_duality_audit)


def command_native_higher_call_time_reversal_schedule_duality_audit(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_time_reversal_schedule_duality_audit import (
        build_native_higher_call_time_reversal_schedule_duality_audit,
        write_native_higher_call_time_reversal_schedule_duality_audit,
    )

    payload = (
        build_native_higher_call_time_reversal_schedule_duality_audit()
        if args.no_write
        else write_native_higher_call_time_reversal_schedule_duality_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_word_permutation_covariance_audit(subparsers) -> None:
    native_higher_call_word_permutation_covariance_audit = subparsers.add_parser(
        "native-higher-call-word-permutation-covariance-audit",
        help="Audit word-permutation involutive dilation covariance, m^2 != 1 bilinear symmetry breaking at k >= 2, and alternating intertwining rescue.",
    )
    native_higher_call_word_permutation_covariance_audit.add_argument("--no-write", action="store_true")
    native_higher_call_word_permutation_covariance_audit.set_defaults(func=command_native_higher_call_word_permutation_covariance_audit)


def command_native_higher_call_word_permutation_covariance_audit(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_word_permutation_covariance_audit import (
        build_native_higher_call_word_permutation_covariance_audit,
        write_native_higher_call_word_permutation_covariance_audit,
    )

    payload = (
        build_native_higher_call_word_permutation_covariance_audit()
        if args.no_write
        else write_native_higher_call_word_permutation_covariance_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_higher_call_secret_subspace_restriction_audit(subparsers) -> None:
    native_higher_call_secret_subspace_restriction_audit = subparsers.add_parser(
        "native-higher-call-secret-subspace-restriction-audit",
        help="Audit secret-subspace projected variety pinching, coset harmonic folding, and Fourier-space Law of Total Variance.",
    )
    native_higher_call_secret_subspace_restriction_audit.add_argument("--no-write", action="store_true")
    native_higher_call_secret_subspace_restriction_audit.set_defaults(func=command_native_higher_call_secret_subspace_restriction_audit)


def command_native_higher_call_secret_subspace_restriction_audit(args: argparse.Namespace) -> int:
    from theorems.native_higher_call_secret_subspace_restriction_audit import (
        build_native_higher_call_secret_subspace_restriction_audit,
        write_native_higher_call_secret_subspace_restriction_audit,
    )

    payload = (
        build_native_higher_call_secret_subspace_restriction_audit()
        if args.no_write
        else write_native_higher_call_secret_subspace_restriction_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_native_recovery_capacity(subparsers) -> None:
    native_recovery_capacity = subparsers.add_parser(
        "native-recovery-capacity",
        help="Run full-recovery capacity gates for native copies and fixed-bank phase queries.",
    )
    native_recovery_capacity.add_argument("--no-registry", action="store_true")
    native_recovery_capacity.set_defaults(func=command_native_recovery_capacity)


def command_native_recovery_capacity(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_recovery_capacity import REPORT, build_report
    from ternary_measured_lattice_decoder import exact_json
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print("native_recovery_capacity complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_gaussian_bank_robustness(subparsers) -> None:
    native_gaussian_bank_robustness = subparsers.add_parser(
        "native-gaussian-bank-robustness",
        help="Run Gaussian-tail refinement of the fixed-bank coherent phase error ledger.",
    )
    native_gaussian_bank_robustness.add_argument("--no-registry", action="store_true")
    native_gaussian_bank_robustness.set_defaults(func=command_native_gaussian_bank_robustness)


def command_native_gaussian_bank_robustness(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_gaussian_bank_robustness import REPORT, build_report
    from ternary_measured_lattice_decoder import exact_json
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print("native_gaussian_bank_robustness complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_history_erasure_dequantization(subparsers) -> None:
    native_history_erasure_dequantization = subparsers.add_parser(
        "native-history-erasure-dequantization",
        help="Replay scoped history countercontrols and quarantine the unsupported universal no-go.",
    )
    native_history_erasure_dequantization.add_argument("--no-registry", action="store_true")
    native_history_erasure_dequantization.set_defaults(func=command_native_history_erasure_dequantization)


def command_native_history_erasure_dequantization(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_history_erasure_dequantization import REPORT, write_report
    write_report(write_registry=not getattr(args, "no_registry", False))
    validation = validate_registry()
    print("native_history_erasure_dequantization complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_basis_lottery(subparsers) -> None:
    native_basis_lottery = subparsers.add_parser(
        "native-basis-lottery",
        help="Audit disjoint clean-basis classical multiple completion and monotone Gaussian source event.",
    )
    native_basis_lottery.add_argument("--no-write", action="store_true")
    native_basis_lottery.set_defaults(func=command_native_basis_lottery)


def command_native_basis_lottery(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_basis_lottery import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_recursive_quotient_audit(subparsers) -> None:
    native_recursive_quotient_audit = subparsers.add_parser(
        "native-recursive-quotient-audit",
        help="Audit exact same-original recursive quotient composition, canonical nodes, and producer coverage debt.",
    )
    native_recursive_quotient_audit.add_argument("--no-write", action="store_true")
    native_recursive_quotient_audit.set_defaults(func=command_native_recursive_quotient_audit)


def command_native_recursive_quotient_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_recursive_quotient_audit import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_source_refresh(subparsers) -> None:
    native_source_refresh = subparsers.add_parser(
        "native-source-refresh",
        help="Audit conditional sign-mix Gaussian source refresh, odd prime-power chi-square identity, and common energy event.",
    )
    native_source_refresh.add_argument("--no-write", action="store_true")
    native_source_refresh.set_defaults(func=command_native_source_refresh)


def command_native_source_refresh(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_source_refresh import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_prefix_ambiguity_pruning(subparsers) -> None:
    native_prefix_ambiguity_pruning = subparsers.add_parser(
        "native-prefix-ambiguity-pruning",
        help="Audit modulo-scale original-prefix pruning, canonical DAG width collapse, and wrap-around horizons.",
    )
    native_prefix_ambiguity_pruning.add_argument("--no-write", action="store_true")
    native_prefix_ambiguity_pruning.set_defaults(func=command_native_prefix_ambiguity_pruning)


def command_native_prefix_ambiguity_pruning(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_prefix_ambiguity_pruning import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_syndrome_dilation(subparsers) -> None:
    native_syndrome_dilation = subparsers.add_parser(
        "native-syndrome-dilation",
        help="Audit constructive constant-gap syndrome dilation and noncommuting word effects.",
    )
    native_syndrome_dilation.add_argument("--no-write", action="store_true")
    native_syndrome_dilation.set_defaults(func=command_native_syndrome_dilation)


def command_native_syndrome_dilation(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_syndrome_dilation import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_word_collision_symmetry(subparsers) -> None:
    native_word_collision_symmetry = subparsers.add_parser(
        "native-word-collision-symmetry",
        help="Audit two-word collision/swap symmetry observable and rare branch costs.",
    )
    native_word_collision_symmetry.add_argument("--no-write", action="store_true")
    native_word_collision_symmetry.set_defaults(func=command_native_word_collision_symmetry)


def command_native_word_collision_symmetry(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_word_collision_symmetry import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_word_spectral_filter_audit(subparsers) -> None:
    native_word_spectral_filter_audit = subparsers.add_parser(
        "native-word-spectral-filter-audit",
        help="Audit bounded raw-frame spectral filters, exact controls, and degree price.",
    )
    native_word_spectral_filter_audit.add_argument("--no-write", action="store_true")
    native_word_spectral_filter_audit.set_defaults(func=command_native_word_spectral_filter_audit)


def command_native_word_spectral_filter_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_word_spectral_filter_audit import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_refresh_crossover_scope_audit(subparsers) -> None:
    native_refresh_crossover_scope_audit = subparsers.add_parser(
        "native-refresh-crossover-scope-audit",
        help="Audit composability, classical dominance, and dimension debt of refresh crossover.",
    )
    native_refresh_crossover_scope_audit.add_argument("--no-write", action="store_true")
    native_refresh_crossover_scope_audit.set_defaults(func=command_native_refresh_crossover_scope_audit)


def command_native_refresh_crossover_scope_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_refresh_crossover_scope_audit import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_refresh_lottery_crossover(subparsers) -> None:
    native_refresh_lottery_crossover = subparsers.add_parser(
        "native-refresh-lottery-crossover",
        help="Audit parameter-free refresh-to-clean-basis crossover inequality and composed canonical DAG pipeline.",
    )
    native_refresh_lottery_crossover.add_argument("--no-write", action="store_true")
    native_refresh_lottery_crossover.set_defaults(func=command_native_refresh_lottery_crossover)


def command_native_refresh_lottery_crossover(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_refresh_lottery_crossover import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_gaussian_dither_sampler(subparsers) -> None:
    native_gaussian_dither_sampler = subparsers.add_parser(
        "native-gaussian-dither-sampler",
        help="Audit certified rounded-Gaussian dither and sign/mask batch sampler with adaptive-threshold union.",
    )
    native_gaussian_dither_sampler.add_argument("--no-write", action="store_true")
    native_gaussian_dither_sampler.set_defaults(func=command_native_gaussian_dither_sampler)


def command_native_gaussian_dither_sampler(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_gaussian_dither_sampler import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_interleaved_syndrome_work_audit(subparsers) -> None:
    native_interleaved_syndrome_work_audit = subparsers.add_parser(
        "native-interleaved-syndrome-work-audit",
        help="Audit multi-round interleaved syndrome-work circuits, Parseval ground-band conservation, and 2-call 3-adic stratification.",
    )
    native_interleaved_syndrome_work_audit.add_argument("--no-write", action="store_true")
    native_interleaved_syndrome_work_audit.set_defaults(func=command_native_interleaved_syndrome_work_audit)


def command_native_interleaved_syndrome_work_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_interleaved_syndrome_work_audit import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_banded_qft_transfer_matrix_audit(subparsers) -> None:
    native_banded_qft_transfer_matrix_audit = subparsers.add_parser(
        "native-banded-qft-transfer-matrix-audit",
        help="Audit banded cyclic QFT two-call transfer-matrix O(M 3^b) contraction and bandwidth scaling.",
    )
    native_banded_qft_transfer_matrix_audit.add_argument("--no-write", action="store_true")
    native_banded_qft_transfer_matrix_audit.set_defaults(func=command_native_banded_qft_transfer_matrix_audit)


def command_native_banded_qft_transfer_matrix_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_banded_qft_transfer_matrix_audit import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_response_fourier_factorization_audit(subparsers) -> None:
    native_response_fourier_factorization_audit = subparsers.add_parser(
        "native-response-fourier-factorization-audit",
        help="Audit tensor qutrit F3 factorization, 1-call cyclic autoregressive chain rule, and signed 2-call difference pinching.",
    )
    native_response_fourier_factorization_audit.add_argument("--no-write", action="store_true")
    native_response_fourier_factorization_audit.set_defaults(func=command_native_response_fourier_factorization_audit)


def command_native_response_fourier_factorization_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_response_fourier_factorization_audit import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_banded_qft_baseline(subparsers) -> None:
    banded_qft_baseline = subparsers.add_parser(
        "native-banded-qft-baseline",
        help="Run certified dense-free classical sampling for two-call banded Fourier schedules.",
    )
    banded_qft_baseline.add_argument("--no-write", action="store_true")
    banded_qft_baseline.set_defaults(func=command_native_banded_qft_baseline)


def command_native_banded_qft_baseline(args: argparse.Namespace) -> int:
    from theorems.native_banded_qft_baseline import REPORT, build_report
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print("Dense-free public-phase sampling. No secret solver or general quantum lower bound.")
    return 0


def add_native_response_mpo_baseline(subparsers) -> None:
    response_mpo=subparsers.add_parser("native-response-mpo-baseline",
        help="Run paid exact-integer MPS sampling of fixed public phase/Fourier schedules.")
    response_mpo.add_argument("--no-write",action="store_true")
    response_mpo.set_defaults(func=command_native_response_mpo_baseline)


def command_native_response_mpo_baseline(args: argparse.Namespace) -> int:
    from theorems.native_response_mpo_baseline import REPORT, build_report, exact_json
    report=build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True,exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report),indent=2)+"\n")
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print("Fixed public Fourier calls only. No growing-depth or unknown-copy no-go.")
    return 0


def add_native_mp12_prime_power_search_to_decision_audit(subparsers) -> None:
    native_mp12_prime_power_search_to_decision_audit = subparsers.add_parser(
        "native-mp12-prime-power-search-to-decision-audit",
        help="Audit Micciancio-Peikert prime-power Hensel subgroup probes, certified dither widening, and disjoint sample expansion.",
    )
    native_mp12_prime_power_search_to_decision_audit.add_argument("--no-write", action="store_true")
    native_mp12_prime_power_search_to_decision_audit.set_defaults(func=command_native_mp12_prime_power_search_to_decision_audit)


def command_native_mp12_prime_power_search_to_decision_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.native_mp12_prime_power_search_to_decision_audit import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_native_response_path_valuation(subparsers) -> None:
    response_path_valuation = subparsers.add_parser(
        "native-response-path-valuation",
        help="Evaluate exact higher-call collision ideals and weighted two-call Fourier readout.",
    )
    response_path_valuation.add_argument("--no-write", action="store_true")
    response_path_valuation.set_defaults(func=command_native_response_path_valuation)


def command_native_response_path_valuation(args: argparse.Namespace) -> int:
    from theorems.native_response_path_valuation import REPORT, build_report, exact_json
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print("No speedup or general lower bound admitted.")
    return 0
