"""Dihedral coset problem (DCP) subcommands, moved out of qsearch.py by tools/split_cli/migrate.py.

Each ``add_*`` function registers one subcommand and each ``command_*`` function runs one.
A command imports what it needs from ``qsearch`` when it runs, so loading this module stays
cheap and ``monkeypatch.setattr(qsearch, name, ...)`` still reaches the command.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path



def add_dcp_samples(subparsers) -> None:
    dcp_samples = subparsers.add_parser(
        "dcp-samples",
        help="Run the theorem-contract-faithful DCP coset/phase-state sample and merge audit.",
    )
    dcp_samples.add_argument("--n-values", default="8,10,12")
    dcp_samples.add_argument("--sample-count", type=int, default=4096)
    dcp_samples.add_argument("--seed", type=int, default=0)
    dcp_samples.add_argument("--no-registry", action="store_true")
    dcp_samples.add_argument("--verbose", action="store_true")
    dcp_samples.set_defaults(func=command_dcp_samples)


def command_dcp_samples(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_dcp_sample_workbench
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_dcp_sample_workbench(
        n_values=n_values,
        sample_count=args.sample_count,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP state-sample workbench complete")
    print("Artifact: research/phase_workbench/dcp_sample_native_sieve.json")
    print(f"Trials: {metrics['trial_count']}")
    print(f"Charged coset states: {metrics['total_input_coset_states']}")
    print(f"Evaluator queries: {metrics['evaluator_query_count']}")
    print(f"Postselection optimism gap: {metrics['postselection_optimism_gap']}")
    print(f"Parity endpoints: {metrics['parity_endpoint_trial_count']}")
    print(f"Full hidden-reflection decodes: {metrics['full_hidden_reflection_decode_count']}")
    print(f"Status: {payload['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for trial in payload["trials"]:
            print(
                f"- {trial['id']} | v2={trial['best_two_adic_valuation']}/{trial['n_bits'] - 1} "
                f"targets={trial['harvested_target_state_count']} depth={trial['merge_depth']} "
                f"full_decode={trial['decoder']['full_hidden_reflection_recovered']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_decode(subparsers) -> None:
    dcp_decode = subparsers.add_parser(
        "dcp-decode",
        help="Run fresh-batch recursive DCP reflection decoding without promoting empirical success.",
    )
    dcp_decode.add_argument("--n-values", default="8,10,12")
    dcp_decode.add_argument("--trials-per-size", type=int, default=3)
    dcp_decode.add_argument("--samples-per-stage", type=int, default=4096)
    dcp_decode.add_argument("--seed", type=int, default=0)
    dcp_decode.add_argument("--no-registry", action="store_true")
    dcp_decode.add_argument("--verbose", action="store_true")
    dcp_decode.set_defaults(func=command_dcp_decode)


def command_dcp_decode(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_recursive_decoder_report
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_recursive_decoder_report(
        n_values=n_values,
        trials_per_size=args.trials_per_size,
        samples_per_stage=args.samples_per_stage,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Recursive DCP decoder audit complete")
    print("Artifact: research/phase_workbench/dcp_recursive_decoder.json")
    print(
        f"Empirical full recoveries: {metrics['empirical_full_recovery_count']}/"
        f"{metrics['recursive_trial_count']}"
    )
    print(f"Charged coset states: {metrics['total_coset_state_samples']}")
    print(f"Evaluator queries: {metrics['evaluator_query_count']}")
    print(f"Phase-identity failures: {metrics['phase_correction_failure_count']}")
    print(f"Proved full failure bounds: {metrics['proved_full_failure_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for trial in payload["trials"]:
            print(
                f"- {trial['id']} | recovered={trial['recovered_hidden_reflection']} "
                f"truth={trial['true_hidden_reflection']} stages={len(trial['stages'])} "
                f"states={trial['total_coset_state_samples']} success={trial['full_recovery_success']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_recurrence(subparsers) -> None:
    dcp_recurrence = subparsers.add_parser(
        "dcp-recurrence",
        help="Audit exact DCP pair kernels and finite endpoint-yield scaling without asymptotic promotion.",
    )
    dcp_recurrence.add_argument("--n-values", default="8,12,16,20,24")
    dcp_recurrence.add_argument("--budget-multipliers", default="1.5,2.0,2.5,3.0")
    dcp_recurrence.add_argument("--trials-per-point", type=int, default=12)
    dcp_recurrence.add_argument("--seed", type=int, default=0)
    dcp_recurrence.add_argument("--no-registry", action="store_true")
    dcp_recurrence.add_argument("--verbose", action="store_true")
    dcp_recurrence.set_defaults(func=command_dcp_recurrence)


def command_dcp_recurrence(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_dcp_recurrence_report
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    multipliers = [float(value.strip()) for value in args.budget_multipliers.split(",") if value.strip()]
    payload = write_dcp_recurrence_report(
        n_values=n_values,
        budget_multipliers=multipliers,
        trials_per_point=args.trials_per_point,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP recurrence scaling audit complete")
    print("Artifact: research/phase_workbench/dcp_recurrence_analysis.json")
    print(f"Pair-kernel failures: {metrics['pair_kernel_failure_count']}")
    print(f"Scaling rows: {metrics['scaling_row_count']}")
    print(f"Trials: {metrics['total_trial_count']}")
    print(f"Charged coset states: {metrics['total_charged_coset_states']}")
    print(f"Raw-input target labels: {metrics['direct_target_input_count']}")
    print(f"Sieve-generated targets: {metrics['sieve_generated_target_count']}")
    print(f"Target-capable pairs: {metrics['target_capable_pair_count']}")
    print(f"Trials with no target opportunity: {metrics['no_target_opportunity_trial_count']}")
    print(f"Proved uniform endpoint bounds: {metrics['proved_uniform_endpoint_lower_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for fit in payload["scaling_fits"]:
            print(
                f"- {fit['rule']} | thresholds={fit['successful_n_count']} "
                f"sqrt_slope={fit['sqrt_n_slope']} linear_slope={fit['linear_n_slope']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_schedules(subparsers) -> None:
    dcp_schedules = subparsers.add_parser(
        "dcp-schedules",
        help="Search DCP bucket schedules with disjoint training and holdout seeds.",
    )
    dcp_schedules.add_argument("--n-values", default="20,24,28,32")
    dcp_schedules.add_argument("--budget-multiplier", type=float, default=2.0)
    dcp_schedules.add_argument("--population-size", type=int, default=10)
    dcp_schedules.add_argument("--generations", type=int, default=6)
    dcp_schedules.add_argument("--train-trials", type=int, default=8)
    dcp_schedules.add_argument("--holdout-trials", type=int, default=24)
    dcp_schedules.add_argument("--confirmation-trials", type=int, default=128)
    dcp_schedules.add_argument("--seed", type=int, default=0)
    dcp_schedules.add_argument("--no-registry", action="store_true")
    dcp_schedules.add_argument("--verbose", action="store_true")
    dcp_schedules.set_defaults(func=command_dcp_schedules)


def command_dcp_schedules(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_dcp_schedule_search_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_dcp_schedule_search_report(
        n_values=n_values,
        budget_multiplier=args.budget_multiplier,
        population_size=args.population_size,
        generations=args.generations,
        train_trials=args.train_trials,
        holdout_trials=args.holdout_trials,
        confirmation_trials=args.confirmation_trials,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP held-out schedule search complete")
    print("Artifact: research/phase_workbench/dcp_schedule_search.json")
    print(f"Unique schedules: {metrics['unique_schedule_count']}")
    print(f"Optimizer trials: {metrics['optimizer_trial_count']}")
    print(f"Holdout trials: {metrics['holdout_trial_count']}")
    print(f"Held-out seed improvements: {metrics['heldout_seed_improvement_count']}")
    print(f"Confirmed improvements: {metrics['statistically_confirmed_improvement_count']}")
    print(f"Max held-out success improvement: {metrics['max_holdout_success_improvement']}")
    print(f"Max selection optimism gap: {metrics['max_selection_optimism_gap']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- n={record['n_bits']} {record['rule']} selected={record['selected_schedule']} "
                f"holdout={record['holdout_evaluation']['generated_endpoint_success_rate']:.3f} "
                f"default={record['default_holdout_evaluation']['generated_endpoint_success_rate']:.3f} "
                f"improvement={record['holdout_success_improvement']:.3f} "
                f"confirm_p={record['confirmation_adjusted_p_value']:.4g}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_uniform_schedules(subparsers) -> None:
    dcp_uniform = subparsers.add_parser(
        "dcp-uniform-schedules",
        help="Fit one sqrt(log N) block-schedule constant and test it on unseen modulus sizes.",
    )
    dcp_uniform.add_argument("--train-n-values", default="20,24,28")
    dcp_uniform.add_argument("--unseen-n-values", default="32,36,40")
    dcp_uniform.add_argument("--train-trials", type=int, default=12)
    dcp_uniform.add_argument("--unseen-trials", type=int, default=64)
    dcp_uniform.add_argument("--seed", type=int, default=0)
    dcp_uniform.add_argument("--no-registry", action="store_true")
    dcp_uniform.add_argument("--verbose", action="store_true")
    dcp_uniform.set_defaults(func=command_dcp_uniform_schedules)


def command_dcp_uniform_schedules(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_dcp_uniform_schedule_report,
    )
    initialize_seed_registry(overwrite=False)
    train_n = [int(value.strip()) for value in args.train_n_values.split(",") if value.strip()]
    unseen_n = [int(value.strip()) for value in args.unseen_n_values.split(",") if value.strip()]
    payload = write_dcp_uniform_schedule_report(
        train_n_values=train_n,
        unseen_n_values=unseen_n,
        train_trials=args.train_trials,
        unseen_trials=args.unseen_trials,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Uniform DCP schedule-family audit complete")
    print("Artifact: research/phase_workbench/dcp_uniform_schedule_family.json")
    print(f"Training trials: {metrics['training_trial_count']}")
    print(f"Unseen-size trials: {metrics['unseen_trial_count']}")
    print(f"Positive finite-size rules: {metrics['positive_mean_unseen_improvement_count']}")
    print(f"Asymptotic class changes: {metrics['asymptotic_class_change_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['rule']} c={record['selected_block_scale']} "
                f"mean_unseen_improvement={record['mean_unseen_success_improvement']:.3f} "
                f"class_changed={record['asymptotic_class_changed']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_bad_registers(subparsers) -> None:
    dcp_bad = subparsers.add_parser(
        "dcp-bad-registers",
        help="Audit arbitrary bad-register contamination under the exact Regev f=1 DCP promise.",
    )
    dcp_bad.add_argument("--n-values", default="12,16,20,24")
    dcp_bad.add_argument("--trials-per-row", type=int, default=32)
    dcp_bad.add_argument("--seed", type=int, default=0)
    dcp_bad.add_argument("--no-registry", action="store_true")
    dcp_bad.set_defaults(func=command_dcp_bad_registers)


def command_dcp_bad_registers(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_dcp_bad_register_report
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_dcp_bad_register_report(
        n_values=n_values,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP bad-register robustness audit complete")
    print("Artifact: research/phase_workbench/dcp_bad_register_audit.json")
    print(f"Trials: {metrics['total_trial_count']}")
    print(f"Corrupted theorem-promise rows: {metrics['theorem_corrupted_endpoint_row_count']}")
    print(f"Worst false parity-bit probability: {metrics['maximum_theorem_false_bit_probability']}")
    print(f"Minimum all-bits-valid estimate: {metrics['minimum_theorem_all_bits_valid_probability']}")
    print(f"Robustness proofs: {metrics['proved_bad_register_robustness_count']}")
    print(
        "First generic-depth robustness failure: "
        f"n_bits={metrics['first_generic_depth_robustness_failure_n_bits']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_contamination(subparsers) -> None:
    dcp_contamination = subparsers.add_parser(
        "dcp-contamination",
        help="Compute exact state-only bad-register ensemble and subset-sum witness boundaries.",
    )
    dcp_contamination.add_argument("--n-values", default="8,10,12,14,16")
    dcp_contamination.add_argument("--register-fractions", default="0.25,0.5,1.0")
    dcp_contamination.add_argument("--trials-per-row", type=int, default=8)
    dcp_contamination.add_argument("--seed", type=int, default=0)
    dcp_contamination.add_argument("--no-registry", action="store_true")
    dcp_contamination.set_defaults(func=command_dcp_contamination)


def command_dcp_contamination(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_contamination_witness_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_fractions = [float(value.strip()) for value in args.register_fractions.split(",") if value.strip()]
    payload = write_contamination_witness_report(
        n_values=n_values,
        register_fractions=register_fractions,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP state-only contamination-witness audit complete")
    print("Artifact: research/phase_workbench/dcp_contamination_witness.json")
    print(f"Exact label batches: {metrics['trial_count']}")
    print(f"Exactly indistinguishable batches: {metrics['collision_free_exact_indistinguishability_count']}")
    print(f"Collective-signal batches: {metrics['information_signal_instance_count']}")
    print(f"Polynomial-time witnesses: {metrics['polynomial_time_witness_count']}")
    print(f"Robust decoders proved: {metrics['proved_robust_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_witness_search(subparsers) -> None:
    dcp_witness = subparsers.add_parser(
        "dcp-witness-search",
        help="Search state-native collective observables and certify bounded-locality signed-relation no-go bounds.",
    )
    dcp_witness.add_argument("--n-values", default="12,16,20,24")
    dcp_witness.add_argument("--label-multiplier", type=int, default=1)
    dcp_witness.add_argument("--maximum-weight", type=int, default=4)
    dcp_witness.add_argument("--trials-per-row", type=int, default=12)
    dcp_witness.add_argument("--seed", type=int, default=0)
    dcp_witness.add_argument("--no-registry", action="store_true")
    dcp_witness.set_defaults(func=command_dcp_witness_search)


def command_dcp_witness_search(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_collective_witness_search
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_collective_witness_search(
        n_values=n_values,
        label_multiplier=args.label_multiplier,
        maximum_weight=args.maximum_weight,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP collective-witness language search complete")
    print("Artifact: research/phase_workbench/dcp_collective_witness_search.json")
    print(f"Finite trials: {metrics['finite_trial_count']}")
    print(f"Trials with signed relations: {metrics['finite_relation_trial_count']}")
    print(f"Log-locality no-go certificates: {metrics['logarithmic_locality_negligible_count']}")
    print(f"Polynomial-time robust witnesses: {metrics['polynomial_time_robust_witness_count']}")
    print(f"Full decoders proved: {metrics['proved_full_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_clifford_witnesses(subparsers) -> None:
    dcp_clifford = subparsers.add_parser(
        "dcp-clifford-witnesses",
        help="Search global public-label Clifford measurements with efficient Hamming-weight decoders.",
    )
    dcp_clifford.add_argument("--n-values", default="8,10,12,14,16")
    dcp_clifford.add_argument("--trials-per-row", type=int, default=4)
    dcp_clifford.add_argument("--seed", type=int, default=0)
    dcp_clifford.add_argument("--no-registry", action="store_true")
    dcp_clifford.set_defaults(func=command_dcp_clifford_witnesses)


def command_dcp_clifford_witnesses(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_clifford_witness_search
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_clifford_witness_search(
        n_values=n_values,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP global Clifford-witness search complete")
    print("Artifact: research/phase_workbench/dcp_clifford_witness_search.json")
    print(f"Instances: {metrics['instance_count']}")
    print(f"Circuit evaluations: {metrics['schema_evaluation_count']}")
    print(f"Finite inverse-polynomial Hamming signals: {metrics['inverse_polynomial_hamming_signal_count']}")
    print(f"Proved signal families: {metrics['proved_inverse_polynomial_signal_family_count']}")
    print(f"Adversarial thresholds: {metrics['proved_adversarial_threshold_count']}")
    print(f"Full decoders proved: {metrics['proved_full_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_clifford_contamination(subparsers) -> None:
    dcp_clifford_contamination = subparsers.add_parser(
        "dcp-clifford-contamination",
        help="Minimize global Clifford Hamming signal over every one-bad coordinate and basis value.",
    )
    dcp_clifford_contamination.add_argument("--n-values", default="6,8,10,12")
    dcp_clifford_contamination.add_argument("--trials-per-row", type=int, default=3)
    dcp_clifford_contamination.add_argument("--seed", type=int, default=0)
    dcp_clifford_contamination.add_argument("--no-registry", action="store_true")
    dcp_clifford_contamination.set_defaults(func=command_dcp_clifford_contamination)


def command_dcp_clifford_contamination(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_clifford_contamination_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_clifford_contamination_report(
        n_values=n_values,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP adversarial one-bad Clifford audit complete")
    print("Artifact: research/phase_workbench/dcp_clifford_contamination.json")
    print(f"Adversarial cases: {metrics['adversarial_one_bad_case_count']}")
    print(f"Finite inverse-polynomial survivors: {metrics['inverse_polynomial_one_bad_signal_count']}")
    print(f"Zero worst-case signals: {metrics['zero_worst_case_signal_count']}")
    print(f"Uniform signal families proved: {metrics['proved_uniform_one_bad_signal_family_count']}")
    print(f"Full f=1 thresholds proved: {metrics['proved_full_f1_threshold_count']}")
    print(f"Full decoders proved: {metrics['proved_full_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_hadamard_scaling(subparsers) -> None:
    dcp_hadamard = subparsers.add_parser(
        "dcp-hadamard-scaling",
        help="Sweep Hadamard witness register ratios across the analytic signed-relation threshold.",
    )
    dcp_hadamard.add_argument("--n-values", default="6,8,10,12")
    dcp_hadamard.add_argument("--register-ratios", default="0.5,1.0,1.5,2.0")
    dcp_hadamard.add_argument("--trials-per-row", type=int, default=3)
    dcp_hadamard.add_argument("--seed", type=int, default=0)
    dcp_hadamard.add_argument("--no-registry", action="store_true")
    dcp_hadamard.set_defaults(func=command_dcp_hadamard_scaling)


def command_dcp_hadamard_scaling(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_hadamard_scaling_report
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_ratios = [float(value.strip()) for value in args.register_ratios.split(",") if value.strip()]
    payload = write_hadamard_scaling_report(
        n_values=n_values,
        register_ratios=register_ratios,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP Hadamard register-ratio scaling audit complete")
    print("Artifact: research/phase_workbench/dcp_hadamard_scaling.json")
    print(f"Rows: {metrics['scaling_row_count']}")
    print(f"Analytic subcritical threshold: {metrics['analytic_subcritical_ratio_threshold']}")
    print(f"Subcritical rows: {metrics['analytically_subcritical_row_count']}")
    print(f"Supercritical finite-signal rows: {metrics['supercritical_inverse_polynomial_signal_row_count']}")
    print(f"Worst-reflection signal families proved: {metrics['proved_worst_case_reflection_signal_family_count']}")
    print(f"Robust decoders proved: {metrics['proved_f1_robust_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_random_decoder(subparsers) -> None:
    dcp_random_decoder = subparsers.add_parser(
        "dcp-random-decoder",
        help="Decode random-label local X/Y measurements with a full FFT and charge exponential resources.",
    )
    dcp_random_decoder.add_argument("--n-values", default="8,10,12,14,16")
    dcp_random_decoder.add_argument("--sample-multipliers", default="2,4,8,16")
    dcp_random_decoder.add_argument("--trials-per-row", type=int, default=24)
    dcp_random_decoder.add_argument("--seed", type=int, default=0)
    dcp_random_decoder.add_argument("--no-registry", action="store_true")
    dcp_random_decoder.set_defaults(func=command_dcp_random_decoder)


def command_dcp_random_decoder(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_random_design_decoder_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    sample_multipliers = [float(value.strip()) for value in args.sample_multipliers.split(",") if value.strip()]
    payload = write_random_design_decoder_report(
        n_values=n_values,
        sample_multipliers=sample_multipliers,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP random-design local-quadrature decoder baseline complete")
    print("Artifact: research/classical_baselines/dcp_random_design_decoder.json")
    print(f"Trials: {metrics['trial_count']}")
    print(f"FFT recoveries: {metrics['fft_success_count']}")
    print(f"High-success FFT rows: {metrics['high_success_fft_row_count']}")
    print(f"Polynomial random-candidate recoveries: {metrics['polynomial_random_candidate_success_count']}")
    print(f"Polynomial-time decoders proved: {metrics['proved_polynomial_time_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_decoder_frontier(subparsers) -> None:
    dcp_frontier = subparsers.add_parser(
        "dcp-decoder-frontier",
        help="Compare legal DCP decoders against named sample/time/memory and robustness frontiers.",
    )
    dcp_frontier.add_argument("--no-registry", action="store_true")
    dcp_frontier.set_defaults(func=command_dcp_decoder_frontier)


def command_dcp_decoder_frontier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_decoder_frontier
    initialize_seed_registry(overwrite=False)
    payload = write_decoder_frontier(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP named decoder resource frontier complete")
    print("Artifact: research/phase_workbench/dcp_decoder_frontier.json")
    print(f"Methods: {metrics['row_count']}")
    print(f"Legal methods: {metrics['legal_row_count']}")
    print(f"Illegal access methods: {metrics['illegal_access_row_count']}")
    print(f"Exponential-time methods: {metrics['exponential_time_row_count']}")
    print(f"Polynomial exact-f=1 decoders: {metrics['proved_polynomial_exact_f1_decoder_count']}")
    print(f"Complete lattice compositions: {metrics['complete_lattice_composition_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_multiscale_aliasing(subparsers) -> None:
    dcp_aliasing = subparsers.add_parser(
        "dcp-multiscale-aliasing",
        help="Certify random-label sample barriers for raw and pairwise high-valuation aliases.",
    )
    dcp_aliasing.add_argument("--n-values", default="32,64,128,256,512,1024")
    dcp_aliasing.add_argument("--effective-bit-multipliers", default="1,2")
    dcp_aliasing.add_argument("--polynomial-sample-power", type=int, default=3)
    dcp_aliasing.add_argument("--no-registry", action="store_true")
    dcp_aliasing.set_defaults(func=command_dcp_multiscale_aliasing)


def command_dcp_multiscale_aliasing(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_multiscale_aliasing_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    multipliers = [float(value.strip()) for value in args.effective_bit_multipliers.split(",") if value.strip()]
    payload = write_multiscale_aliasing_report(
        n_values=n_values,
        effective_bit_multipliers=multipliers,
        polynomial_sample_power=args.polynomial_sample_power,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP random-label multiscale aliasing audit complete")
    print("Artifact: research/classical_baselines/dcp_multiscale_aliasing_audit.json")
    print(f"Certificates: {metrics['certificate_count']}")
    print(f"Tail raw-label no-go rows: {metrics['tail_raw_polynomial_access_ruled_out_count']}")
    print(f"Tail pair-difference no-go rows: {metrics['tail_pair_polynomial_access_ruled_out_count']}")
    print(f"General decoder lower bounds: {metrics['proved_general_random_label_decoder_lower_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_fourier_bridge(subparsers) -> None:
    dcp_fourier_bridge = subparsers.add_parser(
        "dcp-fourier-bridge",
        help="Formalize DCP random-label Fourier/HNP bridges, access mismatches, and sample-vs-time bounds.",
    )
    dcp_fourier_bridge.add_argument("--n-values", default="32,64,128,256,512,1024")
    dcp_fourier_bridge.add_argument("--target-failure-probability", type=float, default=1.0 / 3.0)
    dcp_fourier_bridge.add_argument("--no-registry", action="store_true")
    dcp_fourier_bridge.set_defaults(func=command_dcp_fourier_bridge)


def command_dcp_fourier_bridge(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hidden_number_bridge_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_hidden_number_bridge_report(
        n_values=n_values,
        target_failure_probability=args.target_failure_probability,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP random-Fourier/hidden-number bridge audit complete")
    print("Artifact: research/reductions/dcp_hidden_number_bridge.json")
    print(f"Bridge edges: {metrics['bridge_edge_count']}")
    print(f"Polynomial-sample certificates: {metrics['polynomial_sample_certificate_count']}")
    print(f"Exact f=1 sample-robustness proofs: {metrics['proved_exact_f1_sample_robustness_count']}")
    print(f"Access-invalid transfers: {metrics['access_invalid_transfer_count']}")
    print(f"Polynomial-time decoders proved: {metrics['proved_polynomial_time_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_sparse_fourier_audit(subparsers) -> None:
    dcp_sparse_fourier = subparsers.add_parser(
        "dcp-sparse-fourier-audit",
        help="Audit sparse-FFT query schedules and constant-arity attempts to synthesize them from iid DCP labels.",
    )
    dcp_sparse_fourier.add_argument("--n-values", default="64,128,256,512,1024")
    dcp_sparse_fourier.add_argument("--arities", default="2,3,4")
    dcp_sparse_fourier.add_argument("--sample-budget-power", type=int, default=3)
    dcp_sparse_fourier.add_argument("--offset-count-power", type=int, default=2)
    dcp_sparse_fourier.add_argument("--no-registry", action="store_true")
    dcp_sparse_fourier.set_defaults(func=command_dcp_sparse_fourier_audit)


def command_dcp_sparse_fourier_audit(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sparse_fourier_transfer_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    arities = [int(value.strip()) for value in args.arities.split(",") if value.strip()]
    payload = write_sparse_fourier_transfer_report(
        n_values=n_values,
        arities=arities,
        sample_budget_power=args.sample_budget_power,
        prescribed_offset_count_power=args.offset_count_power,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP sparse-Fourier transfer audit complete")
    print("Artifact: research/classical_baselines/dcp_sparse_fourier_transfer_audit.json")
    print(f"Mechanisms: {metrics['mechanism_count']}")
    print(f"Direct access-invalid transfers: {metrics['direct_access_invalid_count']}")
    print(
        "Tail constant-arity closures ruled out: "
        f"{metrics['tail_inverse_polynomial_coverage_ruled_out_count']}/{metrics['tail_certificate_count']}"
    )
    print(f"Polylog iid decoders proved: {metrics['proved_polylog_random_example_decoder_count']}")
    print(f"General random-example lower bounds proved: {metrics['proved_general_random_example_lower_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_iid_hash_audit(subparsers) -> None:
    dcp_iid_hash = subparsers.add_parser(
        "dcp-iid-hash-audit",
        help="Prove Parseval sample/enumeration tradeoffs for exact linear iid DCP hash-bin estimators.",
    )
    dcp_iid_hash.add_argument("--n-values", default="32,64,128,256,512,1024")
    dcp_iid_hash.add_argument("--finite-check-n-values", default="6,8,10")
    dcp_iid_hash.add_argument("--target-mse", type=float, default=1.0 / 9.0)
    dcp_iid_hash.add_argument("--sample-budget-power", type=int, default=3)
    dcp_iid_hash.add_argument("--no-registry", action="store_true")
    dcp_iid_hash.set_defaults(func=command_dcp_iid_hash_audit)


def command_dcp_iid_hash_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_iid_hash_estimator_report
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    finite_values = [int(value.strip()) for value in args.finite_check_n_values.split(",") if value.strip()]
    payload = write_iid_hash_estimator_report(
        n_values=n_values,
        target_mse=args.target_mse,
        sample_budget_power=args.sample_budget_power,
        finite_check_n_values=finite_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP iid linear hash-estimator audit complete")
    print("Artifact: research/classical_baselines/dcp_iid_hash_estimator_audit.json")
    print(f"Certificates: {metrics['certificate_count']}")
    print(f"Finite Parseval failures: {metrics['finite_parseval_failure_count']}")
    print(
        "Polynomial-bucket rows with super-budget samples: "
        f"{metrics['polynomial_bucket_rows_with_exponential_sample_lower_bound']}/"
        f"{metrics['polynomial_bucket_count_row_count']}"
    )
    print(f"Joint polynomial linear rows: {metrics['joint_polynomial_resource_row_count']}")
    print(f"Nonlinear decoder lower bounds: {metrics['proved_nonlinear_decoder_lower_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_biased_linear_audit(subparsers) -> None:
    dcp_biased_linear = subparsers.add_parser(
        "dcp-biased-linear-audit",
        help="Prove Parseval tradeoffs for biased, uniformly margin-separated linear iid DCP scores.",
    )
    dcp_biased_linear.add_argument("--n-values", default="32,64,128,256,512,1024")
    dcp_biased_linear.add_argument("--finite-check-n-values", default="6,8,10")
    dcp_biased_linear.add_argument("--decision-margin", type=float, default=1.0 / 8.0)
    dcp_biased_linear.add_argument("--sample-budget-power", type=int, default=3)
    dcp_biased_linear.add_argument("--no-registry", action="store_true")
    dcp_biased_linear.set_defaults(func=command_dcp_biased_linear_audit)


def command_dcp_biased_linear_audit(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_biased_linear_margin_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    finite_values = [int(value.strip()) for value in args.finite_check_n_values.split(",") if value.strip()]
    payload = write_biased_linear_margin_report(
        n_values=n_values,
        decision_margin=args.decision_margin,
        sample_budget_power=args.sample_budget_power,
        finite_check_n_values=finite_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP biased linear margin audit complete")
    print("Artifact: research/classical_baselines/dcp_biased_linear_margin_audit.json")
    print(f"Certificates: {metrics['certificate_count']}")
    print(f"Finite optimality failures: {metrics['finite_check_failure_count']}")
    print(
        "Polynomial-bucket rows with super-budget samples: "
        f"{metrics['polynomial_bucket_rows_with_super_budget_samples']}/"
        f"{metrics['polynomial_bucket_count_row_count']}"
    )
    print(f"Joint polynomial linear rows: {metrics['joint_polynomial_resource_row_count']}")
    print(f"Arbitrary linear-classifier lower bounds: {metrics['proved_arbitrary_linear_classifier_lower_bound_count']}")
    print(f"Nonlinear decoder lower bounds: {metrics['proved_nonlinear_decoder_lower_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_multirecord_audit(subparsers) -> None:
    dcp_multirecord = subparsers.add_parser(
        "dcp-multirecord-audit",
        help="Audit degree-indexed multilinear iid DCP sketches and preserve overlapping/collective open classes.",
    )
    dcp_multirecord.add_argument("--n-values", default="32,64,128,256,512")
    dcp_multirecord.add_argument("--degrees", default="1,2,3,4,6,8")
    dcp_multirecord.add_argument("--decision-margin", type=float, default=1.0 / 8.0)
    dcp_multirecord.add_argument("--sample-budget-power", type=int, default=3)
    dcp_multirecord.add_argument("--finite-n-bits", type=int, default=4)
    dcp_multirecord.add_argument("--finite-degrees", default="1,2,3")
    dcp_multirecord.add_argument("--no-registry", action="store_true")
    dcp_multirecord.set_defaults(func=command_dcp_multirecord_audit)


def command_dcp_multirecord_audit(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_multirecord_hierarchy_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    degrees = [int(value.strip()) for value in args.degrees.split(",") if value.strip()]
    finite_degrees = [int(value.strip()) for value in args.finite_degrees.split(",") if value.strip()]
    payload = write_multirecord_hierarchy_report(
        n_values=n_values,
        degrees=degrees,
        decision_margin=args.decision_margin,
        sample_budget_power=args.sample_budget_power,
        finite_n_bits=args.finite_n_bits,
        finite_degrees=finite_degrees,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP multirecord estimator hierarchy complete")
    print("Artifact: research/classical_baselines/dcp_multirecord_estimator_hierarchy.json")
    print(f"Certificates: {metrics['certificate_count']}")
    print(f"Degrees: {metrics['degree_count']}")
    print(f"Finite aggregate-label failures: {metrics['finite_check_failure_count']}")
    print(f"Joint polynomial disjoint-block rows: {metrics['joint_polynomial_resource_row_count']}")
    print(f"Higher-degree rows cheaper than degree one: {metrics['higher_degree_rows_cheaper_than_degree_one_count']}")
    print(f"Overlapping U-statistic lower bounds: {metrics['proved_overlapping_ustatistic_lower_bound_count']}")
    print(f"Collective-measurement lower bounds: {metrics['proved_collective_measurement_lower_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_ustatistic_audit(subparsers) -> None:
    dcp_ustatistic = subparsers.add_parser(
        "dcp-ustatistic-audit",
        help="Apply Hoeffding variance bounds to overlapping DCP product-kernel U-statistics.",
    )
    dcp_ustatistic.add_argument("--n-values", default="32,64,128,256,512")
    dcp_ustatistic.add_argument("--degrees", default="2,3,4,6,8,16,32")
    dcp_ustatistic.add_argument("--sample-budget-power", type=int, default=3)
    dcp_ustatistic.add_argument("--tuple-budget-power", type=int, default=6)
    dcp_ustatistic.add_argument("--no-registry", action="store_true")
    dcp_ustatistic.set_defaults(func=command_dcp_ustatistic_audit)


def command_dcp_ustatistic_audit(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_ustatistic_variance_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    degrees = [int(value.strip()) for value in args.degrees.split(",") if value.strip()]
    payload = write_ustatistic_variance_report(
        n_values=n_values,
        degrees=degrees,
        sample_budget_power=args.sample_budget_power,
        tuple_budget_power=args.tuple_budget_power,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP overlapping U-statistic variance audit complete")
    print("Artifact: research/classical_baselines/dcp_ustatistic_variance_audit.json")
    print(f"Certificates: {metrics['certificate_count']}")
    print(f"Degrees: {metrics['degree_count']}")
    print(f"Hoeffding coefficient failures: {metrics['coefficient_check_failure_count']}")
    print(f"Polynomial-record/exponential-tuple rows: {metrics['polynomial_record_but_exponential_tuple_row_count']}")
    print(f"Joint polynomial explicit rows: {metrics['joint_polynomial_explicit_resource_row_count']}")
    print(f"Implicit-contraction lower bounds: {metrics['proved_implicit_contraction_lower_bound_count']}")
    print(f"Collective-measurement lower bounds: {metrics['proved_collective_measurement_lower_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_factorized_contraction(subparsers) -> None:
    dcp_factorized = subparsers.add_parser(
        "dcp-factorized-contraction",
        help="Audit polynomial elementary-symmetric contraction of rank-one DCP product kernels.",
    )
    dcp_factorized.add_argument("--n-values", default="32,64,128,256,512")
    dcp_factorized.add_argument("--degrees", default="2,3,4,8,16,32")
    dcp_factorized.add_argument("--sample-budget-power", type=int, default=3)
    dcp_factorized.add_argument("--no-registry", action="store_true")
    dcp_factorized.set_defaults(func=command_dcp_factorized_contraction)


def command_dcp_factorized_contraction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_factorized_contraction_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    degrees = [int(value.strip()) for value in args.degrees.split(",") if value.strip()]
    payload = write_factorized_contraction_report(
        n_values=n_values,
        degrees=degrees,
        sample_budget_power=args.sample_budget_power,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP rank-one factorized contraction audit complete")
    print("Artifact: research/classical_baselines/dcp_factorized_contraction_audit.json")
    print(f"Certificates: {metrics['certificate_count']}")
    print(f"Degrees: {metrics['degree_count']}")
    print(f"Finite variance failures: {metrics['finite_variance_check_failure_count']}")
    print(f"Joint polynomial rank-one rows: {metrics['joint_polynomial_resource_row_count']}")
    print(f"Polynomial-rank contraction lower bounds: {metrics['proved_polynomial_rank_contraction_lower_bound_count']}")
    print(f"Tensor-train contraction lower bounds: {metrics['proved_tensor_train_contraction_lower_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_low_rank_contraction(subparsers) -> None:
    dcp_low_rank = subparsers.add_parser(
        "dcp-low-rank-contraction",
        help="Search polynomial-rank Fejer/Fourier contractions with exact all-order Hoeffding variance.",
    )
    dcp_low_rank.add_argument("--n-values", default="6,8,10")
    dcp_low_rank.add_argument("--degrees", default="2,4,8")
    dcp_low_rank.add_argument("--rank-multiplier", type=int, default=2)
    dcp_low_rank.add_argument(
        "--dictionaries",
        default="cosine-low-frequency,fejer-multiscale,hybrid-fejer-cosine",
    )
    dcp_low_rank.add_argument("--no-registry", action="store_true")
    dcp_low_rank.set_defaults(func=command_dcp_low_rank_contraction)


def command_dcp_low_rank_contraction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_low_rank_contraction_search,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    degrees = [int(value.strip()) for value in args.degrees.split(",") if value.strip()]
    dictionary_ids = [value.strip() for value in args.dictionaries.split(",") if value.strip()]
    payload = write_low_rank_contraction_search(
        n_values=n_values,
        degrees=degrees,
        rank_multiplier=args.rank_multiplier,
        dictionary_ids=dictionary_ids,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP polynomial-rank contraction search complete")
    print("Artifact: research/classical_baselines/dcp_low_rank_contraction_search.json")
    print(f"Rows: {metrics['row_count']}")
    print(f"Uniform separators: {metrics['uniform_separation_row_count']}")
    print(f"Superpolynomial-sample rows: {metrics['superpolynomial_sample_row_count']}")
    print(f"Superpolynomial-precision rows: {metrics['superpolynomial_precision_row_count']}")
    print(f"Finite joint-polynomial survivors: {metrics['joint_polynomial_finite_survivor_count']}")
    print(f"Proved uniform low-rank families: {metrics['proved_uniform_low_rank_family_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_measurement(subparsers) -> None:
    dcp_subset_sum = subparsers.add_parser(
        "dcp-subset-sum-measurement",
        help="Audit collective subset-sum/QFT circuits and exact residue tensor-network bond dimensions.",
    )
    dcp_subset_sum.add_argument("--n-values", default="8,10,12,14,16")
    dcp_subset_sum.add_argument("--register-ratio", type=float, default=1.0)
    dcp_subset_sum.add_argument("--trials-per-size", type=int, default=4)
    dcp_subset_sum.add_argument("--seed", type=int, default=0)
    dcp_subset_sum.add_argument("--no-registry", action="store_true")
    dcp_subset_sum.set_defaults(func=command_dcp_subset_sum_measurement)


def command_dcp_subset_sum_measurement(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_subset_sum_measurement_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_subset_sum_measurement_audit(
        n_values=n_values,
        register_ratio=args.register_ratio,
        trials_per_size=args.trials_per_size,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP collective subset-sum measurement audit complete")
    print("Artifact: research/phase_workbench/dcp_subset_sum_measurement_audit.json")
    print(f"Finite instances: {metrics['finite_instance_count']}")
    print(f"QFT uniformity failures: {metrics['qft_uniformity_failure_count']}")
    print(f"Compute/QFT signal instances: {metrics['compute_qft_signal_instance_count']}")
    print(f"High-probability exponential-bond certificates: {metrics['high_probability_exponential_bond_certificate_count']}")
    print(f"Polynomial collective measurements: {metrics['proved_polynomial_collective_measurement_count']}")
    print(f"Exact f=1 robust decoders: {metrics['proved_exact_f1_robust_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_hashed_fiber_measurement(subparsers) -> None:
    dcp_hashed_fiber = subparsers.add_parser(
        "dcp-hashed-fiber-measurement",
        help="Audit polynomial residue hashing plus Hadamard fiber erasure and amplitude amplification.",
    )
    dcp_hashed_fiber.add_argument("--n-values", default="8,10,12,14")
    dcp_hashed_fiber.add_argument("--register-ratios", default="0.5,1.0")
    dcp_hashed_fiber.add_argument("--hash-families", default="low-bits-modulo,affine-high-bits")
    dcp_hashed_fiber.add_argument("--trials-per-row", type=int, default=2)
    dcp_hashed_fiber.add_argument("--seed", type=int, default=0)
    dcp_hashed_fiber.add_argument("--no-registry", action="store_true")
    dcp_hashed_fiber.set_defaults(func=command_dcp_hashed_fiber_measurement)


def command_dcp_hashed_fiber_measurement(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hashed_fiber_measurement_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_ratios = [float(value.strip()) for value in args.register_ratios.split(",") if value.strip()]
    hash_families = [value.strip() for value in args.hash_families.split(",") if value.strip()]
    payload = write_hashed_fiber_measurement_audit(
        n_values=n_values,
        register_ratios=register_ratios,
        hash_families=hash_families,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP hashed fiber measurement audit complete")
    print("Artifact: research/phase_workbench/dcp_hashed_fiber_measurement_audit.json")
    print(f"Finite instances: {metrics['finite_instance_count']}")
    print(f"Mean-identity failures: {metrics['mean_identity_failure_count']}")
    print(f"Polynomial uniform-postselection instances: {metrics['polynomial_uniform_postselection_instance_count']}")
    print(f"High-probability worst-d no-go certificates: {metrics['high_probability_polynomial_uniform_success_ruled_out_count']}")
    print(f"Polynomial fiber symmetrizations: {metrics['proved_polynomial_fiber_symmetrization_count']}")
    print(f"Exact f=1 robust decoders: {metrics['proved_exact_f1_robust_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_reference_projection(subparsers) -> None:
    dcp_reference_projection = subparsers.add_parser(
        "dcp-reference-projection",
        help="Prove hidden-average no-go bounds for arbitrary public low-trace DCP reference projections.",
    )
    dcp_reference_projection.add_argument("--n-values", default="6,8,10,12")
    dcp_reference_projection.add_argument("--register-ratios", default="0.5,1.0")
    dcp_reference_projection.add_argument("--hash-families", default="low-bits-modulo,affine-high-bits")
    dcp_reference_projection.add_argument("--trials-per-row", type=int, default=2)
    dcp_reference_projection.add_argument("--seed", type=int, default=0)
    dcp_reference_projection.add_argument("--no-registry", action="store_true")
    dcp_reference_projection.set_defaults(func=command_dcp_reference_projection)


def command_dcp_reference_projection(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_reference_projection_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_ratios = [float(value.strip()) for value in args.register_ratios.split(",") if value.strip()]
    hash_families = [value.strip() for value in args.hash_families.split(",") if value.strip()]
    payload = write_reference_projection_audit(
        n_values=n_values,
        register_ratios=register_ratios,
        hash_families=hash_families,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP public reference-projection audit complete")
    print("Artifact: research/phase_workbench/dcp_reference_projection_audit.json")
    print(f"Finite instances: {metrics['finite_instance_count']}")
    print(f"Rank-one bound violations: {metrics['random_reference_bound_violation_count']}")
    print(f"Rank-one tightness failures: {metrics['tight_rank_one_bound_failure_count']}")
    print(f"Polynomial-trace no-go proofs: {metrics['proved_low_trace_effect_no_go_count']}")
    print(f"Full-rank collective no-go proofs: {metrics['proved_full_rank_collective_measurement_no_go_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_covariant_pgm(subparsers) -> None:
    dcp_covariant_pgm = subparsers.add_parser(
        "dcp-covariant-pgm",
        help="Audit exact clean DCP PGM success and the missing normalized-fiber implementation.",
    )
    dcp_covariant_pgm.add_argument("--n-values", default="8,10,12,14,16,18")
    dcp_covariant_pgm.add_argument("--register-offsets", default="-4,-2,0,2")
    dcp_covariant_pgm.add_argument("--trials-per-row", type=int, default=4)
    dcp_covariant_pgm.add_argument("--seed", type=int, default=0)
    dcp_covariant_pgm.add_argument("--no-registry", action="store_true")
    dcp_covariant_pgm.set_defaults(func=command_dcp_covariant_pgm)


def command_dcp_covariant_pgm(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_covariant_pgm_audit
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    payload = write_covariant_pgm_audit(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP covariant PGM audit complete")
    print("Artifact: research/phase_workbench/dcp_covariant_pgm_audit.json")
    print(f"Finite ensembles: {metrics['finite_instance_count']}")
    print(f"Mean clean PGM success at m=n: {metrics['mean_n_register_pgm_success']:.6g}")
    print(f"Clean information theorems: {metrics['proved_clean_information_theorem_count']}")
    print(f"Polynomial PGM circuits: {metrics['proved_polynomial_pgm_circuit_count']}")
    print(f"Exact f=1 robust PGMs: {metrics['proved_exact_f1_robust_pgm_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_pgm_gram(subparsers) -> None:
    dcp_pgm_gram = subparsers.add_parser(
        "dcp-pgm-gram",
        help="Construct the exact DCP Gram block encoding and audit its normalization cost.",
    )
    dcp_pgm_gram.add_argument("--control-n-values", default="3,4")
    dcp_pgm_gram.add_argument("--control-trials", type=int, default=2)
    dcp_pgm_gram.add_argument(
        "--scaling-n-values",
        default="64,128,256,512,1024",
    )
    dcp_pgm_gram.add_argument("--register-offsets", default="0,2")
    dcp_pgm_gram.add_argument("--seed", type=int, default=0)
    dcp_pgm_gram.add_argument(
        "--output",
        default="research/phase_workbench/dcp_pgm_gram_block_encoding.json",
    )
    dcp_pgm_gram.add_argument("--no-registry", action="store_true")
    dcp_pgm_gram.set_defaults(func=command_dcp_pgm_gram)


def command_dcp_pgm_gram(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_gram_block_encoding_report,
    )
    initialize_seed_registry(overwrite=False)
    control_n_values = tuple(
        int(value.strip())
        for value in args.control_n_values.split(",")
        if value.strip()
    )
    scaling_n_values = tuple(
        int(value.strip())
        for value in args.scaling_n_values.split(",")
        if value.strip()
    )
    register_offsets = tuple(
        int(value.strip())
        for value in args.register_offsets.split(",")
        if value.strip()
    )
    payload = write_gram_block_encoding_report(
        output_path=Path(args.output),
        write_registry=not args.no_registry,
        control_n_values=control_n_values,
        control_trials=args.control_trials,
        scaling_n_values=scaling_n_values,
        register_offsets=register_offsets,
        seed=args.seed,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP PGM Gram block-encoding audit complete")
    print(f"Artifact: {args.output}")
    print(
        "Exact projected Gram controls: "
        f"{metrics['finite_control_count'] - metrics['finite_control_failure_count']}/"
        f"{metrics['finite_control_count']}"
    )
    print(
        "Block-encoding normalization log2 slope: "
        f"{metrics['gram_block_encoding_normalization_log2_slope']}"
    )
    print(
        "Tail generic amplification log2 queries: "
        f"{metrics['minimum_tail_generic_amplification_log2_queries']:.6g}"
    )
    print(
        "Structured polynomial preconditioners: "
        f"{metrics['uniform_polynomial_structured_preconditioner_count']}"
    )
    print(
        f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_pgm_qsvt(subparsers) -> None:
    dcp_pgm_qsvt = subparsers.add_parser(
        "dcp-pgm-qsvt",
        help="Prove Markov-degree obstructions for generic QSVT rescaling of direct DCP Gram encodings.",
    )
    dcp_pgm_qsvt.add_argument(
        "--exact-n-values",
        default="2,3,4,5,6,7,8,9,10,11,12,13,14",
    )
    dcp_pgm_qsvt.add_argument(
        "--random-n-values",
        default="8,10,12,14,16,18",
    )
    dcp_pgm_qsvt.add_argument("--random-trials", type=int, default=4)
    dcp_pgm_qsvt.add_argument(
        "--scaling-n-values",
        default="64,128,256,512,1024",
    )
    dcp_pgm_qsvt.add_argument(
        "--approximation-error",
        type=float,
        default=1 / 32,
    )
    dcp_pgm_qsvt.add_argument("--seed", type=int, default=0)
    dcp_pgm_qsvt.add_argument(
        "--output",
        default="research/phase_workbench/dcp_pgm_qsvt_degree_obstruction.json",
    )
    dcp_pgm_qsvt.add_argument("--no-registry", action="store_true")
    dcp_pgm_qsvt.set_defaults(func=command_dcp_pgm_qsvt)


def command_dcp_pgm_qsvt(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_qsvt_degree_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    exact_n_values = tuple(
        int(value.strip())
        for value in args.exact_n_values.split(",")
        if value.strip()
    )
    random_n_values = tuple(
        int(value.strip())
        for value in args.random_n_values.split(",")
        if value.strip()
    )
    scaling_n_values = tuple(
        int(value.strip())
        for value in args.scaling_n_values.split(",")
        if value.strip()
    )
    payload = write_qsvt_degree_obstruction_report(
        output_path=Path(args.output),
        write_registry=not args.no_registry,
        exact_n_values=exact_n_values,
        random_n_values=random_n_values,
        random_trials=args.random_trials,
        scaling_n_values=scaling_n_values,
        approximation_error=args.approximation_error,
        seed=args.seed,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP PGM QSVT degree obstruction complete")
    print(f"Artifact: {args.output}")
    print(
        "Exact lifted sources/failures: "
        f"{metrics['exact_lifted_source_count']}/"
        f"{metrics['exact_lifted_source_failure_count']}"
    )
    print(
        "Random singleton-doubleton controls: "
        f"{metrics['random_source_singleton_doubleton_count']}/"
        f"{metrics['random_source_control_count']}"
    )
    print(
        "Tail count/amplitude degree lower bounds log2: "
        f"{metrics['tail_count_encoding_degree_lower_bound_log2']:.6g}/"
        f"{metrics['tail_amplitude_encoding_degree_lower_bound_log2']:.6g}"
    )
    print(
        "Average-source prevalence theorems: "
        f"{metrics['average_case_random_source_prevalence_theorem_count']}"
    )
    print(
        f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_quenched_occupancy(subparsers) -> None:
    dcp_quenched_occupancy = subparsers.add_parser(
        "dcp-quenched-occupancy",
        help="Prove the quenched Poisson fiber law for random density-one modular subset sum.",
    )
    dcp_quenched_occupancy.add_argument(
        "--exact-n-values", default="2,3,4"
    )
    dcp_quenched_occupancy.add_argument(
        "--scaling-n-values", default="8,10,12,14,16,18"
    )
    dcp_quenched_occupancy.add_argument(
        "--trials-per-size", type=int, default=8
    )
    dcp_quenched_occupancy.add_argument("--seed", type=int, default=0)
    dcp_quenched_occupancy.add_argument(
        "--output",
        default=(
            "research/classical_baselines/"
            "dcp_subset_sum_quenched_occupancy_theorem.json"
        ),
    )
    dcp_quenched_occupancy.add_argument(
        "--no-registry", action="store_true"
    )
    dcp_quenched_occupancy.set_defaults(
        func=command_dcp_quenched_occupancy
    )


def command_dcp_quenched_occupancy(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_quenched_occupancy_report
    initialize_seed_registry(overwrite=False)
    exact_n_values = tuple(
        int(value.strip())
        for value in args.exact_n_values.split(",")
        if value.strip()
    )
    scaling_n_values = tuple(
        int(value.strip())
        for value in args.scaling_n_values.split(",")
        if value.strip()
    )
    payload = write_quenched_occupancy_report(
        output_path=Path(args.output),
        write_registry=not args.no_registry,
        exact_n_values=exact_n_values,
        scaling_n_values=scaling_n_values,
        trials_per_size=args.trials_per_size,
        seed=args.seed,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP quenched occupancy theorem complete")
    print(f"Artifact: {args.output}")
    print(
        "Mixed-moment certificates/failures: "
        f"{metrics['mixed_moment_certificate_count']}/"
        f"{metrics['two_target_transfer_failure_count']}"
    )
    print(
        "Exact source ensembles/failures: "
        f"{metrics['exact_source_ensemble_control_count']}/"
        f"{metrics['exact_source_ensemble_control_failure_count']}"
    )
    print(
        "Tail singleton/doubleton fractions: "
        f"{metrics['tail_mean_singleton_fraction']:.6g}/"
        f"{metrics['tail_mean_doubleton_fraction']:.6g}"
    )
    print(
        "Quenched Poisson theorems: "
        f"{metrics['quenched_poisson_occupancy_theorem_count']}"
    )
    print(
        f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_fiber_erasure_boundary(subparsers) -> None:
    dcp_fiber_erasure_boundary = subparsers.add_parser(
        "dcp-fiber-erasure-boundary",
        help="Separate black-box index erasure from structured DCP fiber-preparation and global-channel interfaces.",
    )
    dcp_fiber_erasure_boundary.add_argument(
        "--n-values", default="64,128,256,512,1024"
    )
    dcp_fiber_erasure_boundary.add_argument(
        "--output",
        default=(
            "research/reductions/"
            "dcp_coherent_fiber_erasure_boundary.json"
        ),
    )
    dcp_fiber_erasure_boundary.add_argument(
        "--no-registry", action="store_true"
    )
    dcp_fiber_erasure_boundary.set_defaults(
        func=command_dcp_fiber_erasure_boundary
    )


def command_dcp_fiber_erasure_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_coherent_fiber_erasure_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(
        int(value.strip())
        for value in args.n_values.split(",")
        if value.strip()
    )
    payload = write_coherent_fiber_erasure_boundary_report(
        output_path=Path(args.output),
        write_registry=not args.no_registry,
        n_values=n_values,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP coherent fiber-erasure boundary complete")
    print(f"Artifact: {args.output}")
    print(
        "Access models/reduction certificates: "
        f"{metrics['access_model_count']}/"
        f"{metrics['reduction_certificate_count']}"
    )
    print(
        "Black-box lower-bound transfers to subset sum: "
        f"{metrics['valid_black_box_lower_bound_transfer_to_structured_subset_sum_count']}"
    )
    print(
        "Support-decision/fixed-variable witness reductions: "
        f"{metrics['proved_target_addressable_support_decision_reduction_count']}/"
        f"{metrics['proved_fixed_variable_witness_self_reduction_count']}"
    )
    print(
        "Polynomial global collective PGM channels: "
        f"{metrics['polynomial_global_collective_pgm_channel_count']}"
    )
    print(
        f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_erasure_inversion(subparsers) -> None:
    dcp_erasure_inversion = subparsers.add_parser(
        "dcp-erasure-inversion",
        help="Reduce coherent erasure-plus-QFT implementations to average subset-sum witness preparation.",
    )
    dcp_erasure_inversion.add_argument(
        "--n-values", default="8,10,12,14,16,18"
    )
    dcp_erasure_inversion.add_argument(
        "--trials-per-size", type=int, default=4
    )
    dcp_erasure_inversion.add_argument("--seed", type=int, default=0)
    dcp_erasure_inversion.add_argument(
        "--output",
        default=(
            "research/reductions/"
            "dcp_global_erasure_inversion_reduction.json"
        ),
    )
    dcp_erasure_inversion.add_argument(
        "--no-registry", action="store_true"
    )
    dcp_erasure_inversion.set_defaults(
        func=command_dcp_erasure_inversion
    )


def command_dcp_erasure_inversion(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_global_erasure_inversion_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = tuple(
        int(value.strip())
        for value in args.n_values.split(",")
        if value.strip()
    )
    payload = write_global_erasure_inversion_report(
        output_path=Path(args.output),
        write_registry=not args.no_registry,
        n_values=n_values,
        trials_per_size=args.trials_per_size,
        seed=args.seed,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP global erasure inversion reduction complete")
    print(f"Artifact: {args.output}")
    print(
        "Target-law controls/failures: "
        f"{metrics['target_law_transfer_control_count']}/"
        f"{metrics['target_law_transfer_failure_count']}"
    )
    print(
        "Coherent erasure-to-witness reductions: "
        f"{metrics['proved_coherent_erasure_to_witness_reduction_count']}"
    )
    print(
        "Arbitrary PGM-to-witness reductions: "
        f"{metrics['proved_arbitrary_pgm_to_witness_reduction_count']}"
    )
    print(
        "Poisson asymptotic domination constant: "
        f"{metrics['poisson_asymptotic_domination_constant']:.6g}"
    )
    print(
        f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_erasure_coherence(subparsers) -> None:
    dcp_erasure_coherence = subparsers.add_parser(
        "dcp-erasure-coherence",
        help="Reduce target-dependent-garbage erasure-plus-QFT success to average witness preparation.",
    )
    dcp_erasure_coherence.add_argument(
        "--output",
        default=(
            "research/reductions/"
            "dcp_approximate_erasure_coherence_reduction.json"
        ),
    )
    dcp_erasure_coherence.add_argument(
        "--no-registry", action="store_true"
    )
    dcp_erasure_coherence.set_defaults(
        func=command_dcp_erasure_coherence
    )


def command_dcp_erasure_coherence(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_approximate_erasure_coherence_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_approximate_erasure_coherence_report(
        output_path=Path(args.output),
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP target-dependent erasure coherence reduction complete")
    print(f"Artifact: {args.output}")
    print(
        "Finite controls/failures: "
        f"{metrics['finite_control_count']}/"
        f"{metrics['finite_control_failure_count']}"
    )
    print(
        "Erasure-to-witness reductions: "
        f"{metrics['inverse_polynomial_erasure_to_witness_reduction_count']}"
    )
    print(
        "Approximate-isometry/arbitrary-PGM reductions: "
        f"{metrics['proved_approximate_isometry_perturbation_bound_count']}/"
        f"{metrics['proved_arbitrary_full_rank_pgm_reduction_count']}"
    )
    print(
        f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_erasure_perturbation(subparsers) -> None:
    dcp_erasure_perturbation = subparsers.add_parser(
        "dcp-erasure-perturbation",
        help="Prove operator-norm robustness of the erasure-plus-QFT witness reduction.",
    )
    dcp_erasure_perturbation.add_argument(
        "--output",
        default=(
            "research/reductions/"
            "dcp_erasure_perturbation_reduction.json"
        ),
    )
    dcp_erasure_perturbation.add_argument(
        "--no-registry", action="store_true"
    )
    dcp_erasure_perturbation.set_defaults(
        func=command_dcp_erasure_perturbation
    )


def command_dcp_erasure_perturbation(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_erasure_perturbation_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_erasure_perturbation_report(
        output_path=Path(args.output),
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP erasure perturbation reduction complete")
    print(f"Artifact: {args.output}")
    print(
        "Scaling/polynomial-precision rows: "
        f"{metrics['scaling_row_count']}/"
        f"{metrics['polynomial_precision_sufficient_row_count']}"
    )
    print(
        "Operator/average-only/arbitrary-PGM reductions: "
        f"{metrics['operator_norm_perturbation_theorem_count']}/"
        f"{metrics['proved_average_only_channel_perturbation_count']}/"
        f"{metrics['proved_arbitrary_full_rank_pgm_reduction_count']}"
    )
    print(
        f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}"
    )
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_contaminated_pgm(subparsers) -> None:
    dcp_contaminated_pgm = subparsers.add_parser(
        "dcp-contaminated-pgm",
        help="Prove exact f=1 information robustness of the clean global PGM and preserve its circuit blocker.",
    )
    dcp_contaminated_pgm.add_argument("--n-values", default="6,8,10,12,14,16")
    dcp_contaminated_pgm.add_argument("--register-offsets", default="-2,0,2")
    dcp_contaminated_pgm.add_argument("--bad-patterns", default="all-zero,all-one,alternating,seeded-random")
    dcp_contaminated_pgm.add_argument("--trials-per-row", type=int, default=2)
    dcp_contaminated_pgm.add_argument("--seed", type=int, default=0)
    dcp_contaminated_pgm.add_argument("--no-registry", action="store_true")
    dcp_contaminated_pgm.set_defaults(func=command_dcp_contaminated_pgm)


def command_dcp_contaminated_pgm(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_contaminated_pgm_audit
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    bad_patterns = [value.strip() for value in args.bad_patterns.split(",") if value.strip()]
    payload = write_contaminated_pgm_audit(
        n_values=n_values,
        register_offsets=register_offsets,
        bad_patterns=bad_patterns,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP contaminated PGM audit complete")
    print("Artifact: research/phase_workbench/dcp_contaminated_pgm_audit.json")
    print(f"Finite instances: {metrics['finite_instance_count']}")
    print(f"All-good lower-bound violations: {metrics['lower_bound_violation_count']}")
    print(f"Minimum m=n all-good probability: {metrics['minimum_n_register_all_good_probability']:.6g}")
    print(f"Exact f=1 information robustness proofs: {metrics['proved_exact_f1_information_robustness_count']}")
    print(f"Polynomial robust PGM circuits: {metrics['proved_exact_f1_robust_pgm_circuit_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_bridge(subparsers) -> None:
    dcp_subset_sum_bridge = subparsers.add_parser(
        "dcp-subset-sum-bridge",
        help="Audit Regev's partial average-case modular subset-sum route to an f=1 DCP decoder.",
    )
    dcp_subset_sum_bridge.add_argument("--n-values", default="8,10,12,14,16,18,20")
    dcp_subset_sum_bridge.add_argument("--register-offset", type=int, default=4)
    dcp_subset_sum_bridge.add_argument("--trials-per-size", type=int, default=3)
    dcp_subset_sum_bridge.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_bridge.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_bridge.set_defaults(func=command_dcp_subset_sum_bridge)


def command_dcp_subset_sum_bridge(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_subset_sum_bridge_audit
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_subset_sum_bridge_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        trials_per_size=args.trials_per_size,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP average-case subset-sum bridge audit complete")
    print("Artifact: research/reductions/dcp_subset_sum_bridge.json")
    print(f"Finite baselines: {metrics['finite_baseline_count']}")
    print(f"Source-contract satisfying rows: {metrics['source_contract_satisfying_row_count']}")
    print(f"Explicit-enumeration no-go certificates: {metrics['polynomial_enumeration_ruled_out_count']}")
    print(f"Primary-source conditional reductions: {metrics['primary_source_conditional_dcp_reduction_count']}")
    print(f"Polynomial partial subset-sum solvers: {metrics['proved_polynomial_partial_average_subset_sum_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_lattice(subparsers) -> None:
    dcp_subset_sum_lattice = subparsers.add_parser(
        "dcp-subset-sum-lattice",
        help="Search deterministic polynomial LLL embeddings for Regev's partial density-one subset-sum contract.",
    )
    dcp_subset_sum_lattice.add_argument("--n-values", default="16,20,24,28,32,40,48")
    dcp_subset_sum_lattice.add_argument("--register-offsets", default="2,4,8")
    dcp_subset_sum_lattice.add_argument("--embedding-scales", default="1,4,16")
    dcp_subset_sum_lattice.add_argument("--lll-deltas", default="0.75,0.99")
    dcp_subset_sum_lattice.add_argument("--combination-arities", default="1,2")
    dcp_subset_sum_lattice.add_argument("--trials-per-row", type=int, default=8)
    dcp_subset_sum_lattice.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_lattice.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_lattice.set_defaults(func=command_dcp_subset_sum_lattice)


def command_dcp_subset_sum_lattice(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_subset_sum_lattice_search
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    embedding_scales = [int(value.strip()) for value in args.embedding_scales.split(",") if value.strip()]
    lll_deltas = [float(value.strip()) for value in args.lll_deltas.split(",") if value.strip()]
    combination_arities = [int(value.strip()) for value in args.combination_arities.split(",") if value.strip()]
    payload = write_subset_sum_lattice_search(
        n_values=n_values,
        register_offsets=register_offsets,
        embedding_scales=embedding_scales,
        lll_deltas=lll_deltas,
        combination_arities=combination_arities,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum lattice search complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_lattice_search.json")
    print(f"Rows/trials: {metrics['row_count']}/{metrics['trial_count']}")
    print(f"Finite success rows: {metrics['finite_success_row_count']}")
    print(f"Tail success rows: {metrics['tail_success_row_count']}/{metrics['tail_row_count']}")
    print(f"Uniform inverse-polynomial coverage proofs: {metrics['proved_uniform_inverse_polynomial_coverage_count']}")
    print(f"Source-contract satisfying rows: {metrics['source_contract_satisfying_row_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_two_adic(subparsers) -> None:
    dcp_subset_sum_two_adic = subparsers.add_parser(
        "dcp-subset-sum-two-adic",
        help="Audit exact 2-adic carry/lift structure without promoting exponential enumeration as a solver.",
    )
    dcp_subset_sum_two_adic.add_argument("--n-values", default="8,10,12")
    dcp_subset_sum_two_adic.add_argument("--register-offsets", default="2,4")
    dcp_subset_sum_two_adic.add_argument("--trials-per-row", type=int, default=2)
    dcp_subset_sum_two_adic.add_argument("--degree-cap", type=int, default=3)
    dcp_subset_sum_two_adic.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_two_adic.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_two_adic.set_defaults(func=command_dcp_subset_sum_two_adic)


def command_dcp_subset_sum_two_adic(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_subset_sum_two_adic_search,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    payload = write_subset_sum_two_adic_search(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=args.trials_per_row,
        degree_cap=args.degree_cap,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum 2-adic lifting search complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_two_adic_search.json")
    print(f"Trials/lift rows: {metrics['trial_count']}/{metrics['lift_row_count']}")
    print(f"Degree-censored lift rows: {metrics['degree_censored_lift_count']}")
    print(f"All-affine legal trials: {metrics['all_lifts_affine_trial_count']}")
    print(f"Mean final affine-hull overcoverage log2: {metrics['mean_final_affine_hull_overcoverage_log2']:.6g}")
    print(f"Uniform polynomial solvers: {metrics['proved_uniform_polynomial_two_adic_solver_count']}")
    print(f"Source-contract satisfying rows: {metrics['source_contract_satisfying_row_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_resource_frontier(subparsers) -> None:
    dcp_subset_sum_resource = subparsers.add_parser(
        "dcp-subset-sum-resource-frontier",
        help="Audit source-linked meet-in-middle, dissection, Wagner, representation, and quantum resource exponents.",
    )
    dcp_subset_sum_resource.add_argument("--n-values", default="64,128,256,512")
    dcp_subset_sum_resource.add_argument("--register-offsets", default="0,4,8")
    dcp_subset_sum_resource.add_argument("--list-counts", default="2,4,8,16")
    dcp_subset_sum_resource.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_resource.set_defaults(func=command_dcp_subset_sum_resource_frontier)


def command_dcp_subset_sum_resource_frontier(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_subset_sum_resource_frontier,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    list_counts = [int(value.strip()) for value in args.list_counts.split(",") if value.strip()]
    payload = write_subset_sum_resource_frontier(
        n_values=n_values,
        register_offsets=register_offsets,
        list_counts=list_counts,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum resource frontier complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_resource_frontier.json")
    print(f"Known algorithms: {metrics['known_algorithm_count']}")
    print(f"Best classical time exponent: {metrics['best_recorded_classical_time_exponent']}")
    print(f"Best quantum time exponent: {metrics['best_recorded_quantum_time_exponent']}")
    print(
        "Deep basic Wagner threshold failures: "
        f"{metrics['deep_basic_wagner_threshold_failure_count']}/{metrics['deep_wagner_certificate_count']}"
    )
    print(f"Known Regev-contract solvers: {metrics['known_regev_contract_satisfying_algorithm_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_carry_anf(subparsers) -> None:
    dcp_subset_sum_carry_anf = subparsers.add_parser(
        "dcp-subset-sum-carry-anf",
        help="Compute exact full-domain carry-bit ANFs and reject restricted-fiber interpolation artifacts.",
    )
    dcp_subset_sum_carry_anf.add_argument("--n-values", default="6,8,10,12")
    dcp_subset_sum_carry_anf.add_argument("--register-offsets", default="2,4")
    dcp_subset_sum_carry_anf.add_argument("--trials-per-row", type=int, default=2)
    dcp_subset_sum_carry_anf.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_carry_anf.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_carry_anf.set_defaults(func=command_dcp_subset_sum_carry_anf)


def command_dcp_subset_sum_carry_anf(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_subset_sum_carry_anf_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    payload = write_subset_sum_carry_anf_audit(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum full-domain carry ANF audit complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_carry_anf.json")
    print(f"Trials/carry rows: {metrics['trial_count']}/{metrics['carry_row_count']}")
    print(
        f"Tail bounded-degree rows: {metrics['tail_bounded_degree_row_count']}/"
        f"{metrics['tail_carry_row_count']}"
    )
    print(f"Maximum observed ANF degree: {metrics['maximum_observed_anf_degree']}")
    print(f"Final-bit degree slope per n: {metrics['fitted_final_bit_degree_slope_per_n']:.6g}")
    print(f"Polynomial algebraic solvers: {metrics['proved_polynomial_algebraic_witness_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_synthesize(subparsers) -> None:
    dcp_subset_sum_synthesize = subparsers.add_parser(
        "dcp-subset-sum-synthesize",
        help="Generate typed high-variance partial-solver hypotheses and reject negative-result matches.",
    )
    dcp_subset_sum_synthesize.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_synthesize.set_defaults(func=command_dcp_subset_sum_synthesize)


def command_dcp_subset_sum_synthesize(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_subset_sum_solver_synthesis,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_subset_sum_solver_synthesis(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum solver hypothesis synthesis complete")
    print("Artifact: research/hypotheses/dcp_subset_sum_solver_synthesis.json")
    print(f"Primitives/hypotheses: {metrics['primitive_count']}/{metrics['hypothesis_count']}")
    print(f"Proposal-only survivors: {metrics['proposal_only_survivor_count']}")
    print(f"Negative/resource rejections: {metrics['negative_match_rejection_count']}")
    print(f"Accepted candidates: {metrics['accepted_candidate_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_low_bit_bdd(subparsers) -> None:
    dcp_subset_sum_low_bit_bdd = subparsers.add_parser(
        "dcp-subset-sum-low-bit-bdd",
        help="Prove polynomial O(log n)-bit subset-sum BDD/state preparation and measure residual entropy.",
    )
    dcp_subset_sum_low_bit_bdd.add_argument("--n-values", default="16,32,64,128")
    dcp_subset_sum_low_bit_bdd.add_argument("--register-offsets", default="2,4")
    dcp_subset_sum_low_bit_bdd.add_argument("--log-multipliers", default="1,2")
    dcp_subset_sum_low_bit_bdd.add_argument("--trials-per-row", type=int, default=2)
    dcp_subset_sum_low_bit_bdd.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_low_bit_bdd.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_low_bit_bdd.set_defaults(func=command_dcp_subset_sum_low_bit_bdd)


def command_dcp_subset_sum_low_bit_bdd(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_subset_sum_low_bit_bdd_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    log_multipliers = [int(value.strip()) for value in args.log_multipliers.split(",") if value.strip()]
    payload = write_subset_sum_low_bit_bdd_audit(
        n_values=n_values,
        register_offsets=register_offsets,
        log_multipliers=log_multipliers,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum low-bit BDD audit complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_low_bit_bdd.json")
    print(f"Rows/theorem certificates: {metrics['row_count']}/{metrics['theorem_certificate_count']}")
    print(f"Polynomial width certificates: {metrics['polynomial_width_certificate_count']}")
    print(f"Polynomial state-preparation certificates: {metrics['polynomial_state_preparation_certificate_count']}")
    print(f"Linear residual-entropy certificates: {metrics['linear_residual_entropy_certificate_count']}")
    print(f"Polynomial witness solvers: {metrics['proved_polynomial_witness_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_conditioned_quotient(subparsers) -> None:
    dcp_subset_sum_conditioned_quotient = subparsers.add_parser(
        "dcp-subset-sum-conditioned-quotient",
        help="Audit high-bit quotient multiplicities after polynomial low-bit conditioning.",
    )
    dcp_subset_sum_conditioned_quotient.add_argument("--n-values", default="10,12,14,16,18")
    dcp_subset_sum_conditioned_quotient.add_argument("--register-offsets", default="2,4")
    dcp_subset_sum_conditioned_quotient.add_argument("--log-multipliers", default="1")
    dcp_subset_sum_conditioned_quotient.add_argument("--trials-per-row", type=int, default=2)
    dcp_subset_sum_conditioned_quotient.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_conditioned_quotient.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_conditioned_quotient.set_defaults(func=command_dcp_subset_sum_conditioned_quotient)


def command_dcp_subset_sum_conditioned_quotient(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_conditioned_quotient_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    log_multipliers = [int(value.strip()) for value in args.log_multipliers.split(",") if value.strip()]
    payload = write_conditioned_quotient_audit(
        n_values=n_values,
        register_offsets=register_offsets,
        log_multipliers=log_multipliers,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP conditioned high-bit quotient audit complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_conditioned_quotient.json")
    print(f"Rows/tail rows: {metrics['row_count']}/{metrics['tail_row_count']}")
    print(f"Tail minimum normalized entropy: {metrics['minimum_tail_normalized_shannon_entropy']:.6g}")
    print(f"Tail maximum target mass: {metrics['maximum_tail_exact_target_probability']:.6g}")
    print(f"High-bit geometry improvements: {metrics['proved_high_bit_geometry_improvement_count']}")
    print(f"Polynomial high-bit decoders: {metrics['proved_polynomial_high_bit_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_preconditioned_geometry(subparsers) -> None:
    dcp_subset_sum_preconditioned_geometry = subparsers.add_parser(
        "dcp-subset-sum-preconditioned-geometry",
        help="Prove exact residual moments after logarithmic low-bit conditioning and audit count-only geometry claims.",
    )
    dcp_subset_sum_preconditioned_geometry.add_argument("--n-values", default="10,12,14,16,18")
    dcp_subset_sum_preconditioned_geometry.add_argument("--register-offsets", default="2,4")
    dcp_subset_sum_preconditioned_geometry.add_argument("--log-multipliers", default="1")
    dcp_subset_sum_preconditioned_geometry.add_argument("--residual-window-radii", default="0,1,4")
    dcp_subset_sum_preconditioned_geometry.add_argument("--trials-per-row", type=int, default=4)
    dcp_subset_sum_preconditioned_geometry.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_preconditioned_geometry.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_preconditioned_geometry.set_defaults(func=command_dcp_subset_sum_preconditioned_geometry)


def command_dcp_subset_sum_preconditioned_geometry(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_preconditioned_geometry_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    log_multipliers = [int(value.strip()) for value in args.log_multipliers.split(",") if value.strip()]
    residual_window_radii = [
        int(value.strip()) for value in args.residual_window_radii.split(",") if value.strip()
    ]
    payload = write_preconditioned_geometry_audit(
        n_values=n_values,
        register_offsets=register_offsets,
        log_multipliers=log_multipliers,
        residual_window_radii=residual_window_radii,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP low-bit preconditioned residual-geometry audit complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_preconditioned_geometry.json")
    print(f"Rows/theorem certificates: {metrics['row_count']}/{metrics['theorem_certificate_count']}")
    print(f"Maximum density exponent change: {metrics['maximum_absolute_density_exponent_change']:.6g}")
    print(
        "Conditional first/second-factorial/variance certificates: "
        f"{metrics['exact_conditional_first_moment_certificate_count']}/"
        f"{metrics['exact_conditional_second_factorial_moment_certificate_count']}/"
        f"{metrics['exact_conditional_variance_certificate_count']}"
    )
    print(f"LLL geometry improvements proved: {metrics['lll_geometry_improvement_proved_count']}")
    print(f"Polynomial witness solvers: {metrics['polynomial_witness_solver_proved_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_fourth_moment(subparsers) -> None:
    dcp_subset_sum_fourth_moment = subparsers.add_parser(
        "dcp-subset-sum-fourth-moment",
        help="Localize low-bit-conditioned fourth-order residual signal to exact affine additive energy.",
    )
    dcp_subset_sum_fourth_moment.add_argument("--n-values", default="8,10,12,14")
    dcp_subset_sum_fourth_moment.add_argument("--register-offsets", default="2,4")
    dcp_subset_sum_fourth_moment.add_argument("--log-multipliers", default="1")
    dcp_subset_sum_fourth_moment.add_argument("--trials-per-row", type=int, default=2)
    dcp_subset_sum_fourth_moment.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_fourth_moment.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_fourth_moment.set_defaults(func=command_dcp_subset_sum_fourth_moment)


def command_dcp_subset_sum_fourth_moment(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_fourth_moment_obstruction
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    log_multipliers = [int(value.strip()) for value in args.log_multipliers.split(",") if value.strip()]
    payload = write_fourth_moment_obstruction(
        n_values=n_values,
        register_offsets=register_offsets,
        log_multipliers=log_multipliers,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP low-fiber fourth-moment obstruction audit complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_fourth_moment_obstruction.json")
    print(f"Rows/theorem certificates: {metrics['row_count']}/{metrics['theorem_certificate_count']}")
    print(f"Triplewise certificates: {metrics['triplewise_independence_certificate_count']}")
    print(f"Fourth-order localization certificates: {metrics['fourth_order_localization_certificate_count']}")
    print(f"Source fourth-moment certificates: {metrics['source_fourth_moment_certificate_count']}")
    print(f"Tail maximum energy inflation: {metrics['maximum_tail_additive_energy_inflation']:.6g}")
    print(
        "Tail maximum relative fourth-excess upper bound: "
        f"{metrics['maximum_tail_fourth_excess_relative_upper_bound']:.6g}"
    )
    print(
        "Source-average fixed-offset fourth-order obstructions: "
        f"{metrics['proved_asymptotic_fixed_fourth_order_obstruction_count']}"
    )
    print(f"Polynomial witness solvers: {metrics['polynomial_witness_solver_proved_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_smith_moments(subparsers) -> None:
    dcp_subset_sum_smith_moments = subparsers.add_parser(
        "dcp-subset-sum-smith-moments",
        help="Census integer Smith types controlling density-one subset-sum factorial moments.",
    )
    dcp_subset_sum_smith_moments.add_argument("--n-values", default="3,4,6,8")
    dcp_subset_sum_smith_moments.add_argument("--register-offsets", default="0,2")
    dcp_subset_sum_smith_moments.add_argument("--moment-orders", default="2,3,4,5,6")
    dcp_subset_sum_smith_moments.add_argument("--exact-combination-cap", type=int, default=20_000)
    dcp_subset_sum_smith_moments.add_argument("--sample-count", type=int, default=2_000)
    dcp_subset_sum_smith_moments.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_smith_moments.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_smith_moments.set_defaults(func=command_dcp_subset_sum_smith_moments)


def command_dcp_subset_sum_smith_moments(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_smith_moment_spectrum
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [
        int(value.strip()) for value in args.register_offsets.split(",") if value.strip()
    ]
    moment_orders = [
        int(value.strip()) for value in args.moment_orders.split(",") if value.strip()
    ]
    payload = write_smith_moment_spectrum(
        n_values=n_values,
        register_offsets=register_offsets,
        moment_orders=moment_orders,
        exact_combination_cap=args.exact_combination_cap,
        sample_count=args.sample_count,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum Smith moment spectrum complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_smith_moment_spectrum.json")
    print(f"Rows: {metrics['row_count']}")
    print(f"Complete exact censuses: {metrics['complete_exact_census_row_count']}")
    print(f"Rare-event-blind sampled rows: {metrics['sampled_rare_event_blind_row_count']}")
    print(f"Exact fourth-moment cross-checks: {metrics['fourth_moment_formula_crosscheck_count']}")
    print(f"Exact fifth-moment cross-checks: {metrics['fifth_moment_formula_crosscheck_count']}")
    print(f"Fixed-fifth asymptotic obstructions: {metrics['proved_asymptotic_fixed_fifth_order_obstruction_count']}")
    print(f"Order>=6 asymptotic obstructions: {metrics['proved_asymptotic_order_at_least_six_obstruction_count']}")
    print(f"Growing-order obstructions: {metrics['proved_growing_order_obstruction_count']}")
    print(f"Polynomial witness decoders: {metrics['polynomial_witness_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_smith_transfer(subparsers) -> None:
    dcp_subset_sum_smith_transfer = subparsers.add_parser(
        "dcp-subset-sum-smith-transfer",
        help="Prove the fixed-sixth source moment obstruction by exhaustive HNF transfer.",
    )
    dcp_subset_sum_smith_transfer.add_argument("--n-values", default="6,8,10,12,16,20")
    dcp_subset_sum_smith_transfer.add_argument("--register-offsets", default="0,2")
    dcp_subset_sum_smith_transfer.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_smith_transfer.set_defaults(func=command_dcp_subset_sum_smith_transfer)


def command_dcp_subset_sum_smith_transfer(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_smith_transfer_order_six
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [
        int(value.strip()) for value in args.register_offsets.split(",") if value.strip()
    ]
    payload = write_smith_transfer_order_six(
        n_values=n_values,
        register_offsets=register_offsets,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum order-six Smith transfer theorem complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_smith_transfer_order_six.json")
    print(f"Reachable HNF states: {metrics['reachable_lattice_state_count']}")
    print(f"Non-generic terminal states: {metrics['non_generic_terminal_state_count']}")
    print(f"Tuple normalization certificates: {metrics['tuple_count_normalization_certificate_count']}")
    print(f"Worst bad-state growth ratio: {metrics['maximum_bad_growth_ratio']:.6g}")
    print(f"Fixed-sixth asymptotic obstructions: {metrics['proved_asymptotic_fixed_sixth_order_obstruction_count']}")
    print(f"Order>=7 asymptotic obstructions: {metrics['proved_asymptotic_order_at_least_seven_obstruction_count']}")
    print(f"Growing-order obstructions: {metrics['proved_growing_order_obstruction_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_fixed_moments(subparsers) -> None:
    dcp_subset_sum_fixed_moments = subparsers.add_parser(
        "dcp-subset-sum-fixed-moments",
        help="Prove source-average contraction for every fixed subset-sum factorial-moment order.",
    )
    dcp_subset_sum_fixed_moments.add_argument(
        "--moment-orders", default=",".join(str(value) for value in range(2, 13))
    )
    dcp_subset_sum_fixed_moments.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_fixed_moments.set_defaults(func=command_dcp_subset_sum_fixed_moments)


def command_dcp_subset_sum_fixed_moments(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_fixed_order_moment_theorem,
    )
    initialize_seed_registry(overwrite=False)
    moment_orders = [
        int(value.strip()) for value in args.moment_orders.split(",") if value.strip()
    ]
    payload = write_fixed_order_moment_theorem(
        moment_orders=moment_orders,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP all-fixed-order source moment theorem complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_fixed_order_moment_theorem.json")
    print(f"Instantiated certificates: {metrics['certificate_count']}")
    print(f"Largest instantiated order: {metrics['largest_instantiated_fixed_order']}")
    print(f"General all-fixed-orders theorems: {metrics['general_all_fixed_orders_theorem_count']}")
    print(f"Growing-order obstructions: {metrics['proved_growing_order_obstruction_count']}")
    print(f"Atypical-fiber obstructions: {metrics['proved_atypical_conditioned_fiber_obstruction_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_conditioned_tail(subparsers) -> None:
    dcp_subset_sum_conditioned_tail = subparsers.add_parser(
        "dcp-subset-sum-conditioned-tail",
        help="Transfer fixed-order source moment decay to low-fiber inverse-polynomial tail bounds.",
    )
    dcp_subset_sum_conditioned_tail.add_argument(
        "--moment-orders", default=",".join(str(value) for value in range(2, 13))
    )
    dcp_subset_sum_conditioned_tail.add_argument("--threshold-degrees", default="1,2,4")
    dcp_subset_sum_conditioned_tail.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_conditioned_tail.set_defaults(func=command_dcp_subset_sum_conditioned_tail)


def command_dcp_subset_sum_conditioned_tail(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_conditioned_tail_theorem
    initialize_seed_registry(overwrite=False)
    moment_orders = [
        int(value.strip()) for value in args.moment_orders.split(",") if value.strip()
    ]
    threshold_degrees = [
        int(value.strip()) for value in args.threshold_degrees.split(",") if value.strip()
    ]
    payload = write_conditioned_tail_theorem(
        moment_orders=moment_orders,
        threshold_degrees=threshold_degrees,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP conditioned fixed-moment tail theorem complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_conditioned_tail_theorem.json")
    print(f"Tail certificates: {metrics['certificate_count']}")
    print(f"General conditioned-tail theorems: {metrics['general_fixed_order_conditioned_tail_theorem_count']}")
    print(f"Growing-order tail obstructions: {metrics['proved_growing_order_conditioned_tail_count']}")
    print(f"Signed-statistic tail obstructions: {metrics['proved_signed_statistic_tail_count']}")
    print(f"Reduced-basis tail obstructions: {metrics['proved_reduced_basis_event_tail_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_growing_moments(subparsers) -> None:
    dcp_subset_sum_growing_moments = subparsers.add_parser(
        "dcp-subset-sum-growing-moments",
        help="Prove source obstruction for moment schedules below half-logarithmic order.",
    )
    dcp_subset_sum_growing_moments.add_argument(
        "--n-values", default="256,1024,4096,65536,1048576"
    )
    dcp_subset_sum_growing_moments.add_argument("--epsilons", default="0.2")
    dcp_subset_sum_growing_moments.add_argument("--register-offset", type=int, default=2)
    dcp_subset_sum_growing_moments.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_growing_moments.set_defaults(func=command_dcp_subset_sum_growing_moments)


def command_dcp_subset_sum_growing_moments(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_growing_order_theorem
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    epsilons = [float(value.strip()) for value in args.epsilons.split(",") if value.strip()]
    payload = write_growing_order_theorem(
        n_values=n_values,
        epsilons=epsilons,
        register_offset=args.register_offset,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP growing-order source moment theorem complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_growing_order_theorem.json")
    print(f"Scaling rows: {metrics['row_count']}")
    print(f"Finite bounds below one: {metrics['finite_bound_below_one_row_count']}")
    print(f"Sub-half-log obstructions: {metrics['proved_sub_half_log_growing_order_obstruction_count']}")
    print(f"Half-log boundary obstructions: {metrics['proved_half_log_boundary_obstruction_count']}")
    print(f"Signed-statistic obstructions: {metrics['proved_signed_statistic_obstruction_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_growing_chain(subparsers) -> None:
    dcp_subset_sum_growing_chain = subparsers.add_parser(
        "dcp-subset-sum-growing-chain",
        help=(
            "Prove a polynomial lattice-chain bound and obstruct "
            "near-logarithmic nonnegative subset-sum moments."
        ),
    )
    dcp_subset_sum_growing_chain.add_argument(
        "--n-values",
        default=(
            "65536,16777216,4294967296,"
            "281474976710656,18446744073709551616"
        ),
    )
    dcp_subset_sum_growing_chain.add_argument("--epsilons", default="0.25")
    dcp_subset_sum_growing_chain.add_argument(
        "--near-log-deficits", default="5.0"
    )
    dcp_subset_sum_growing_chain.add_argument(
        "--exact-control-orders", default="2,3,4,5"
    )
    dcp_subset_sum_growing_chain.add_argument(
        "--register-offset", type=int, default=2
    )
    dcp_subset_sum_growing_chain.add_argument(
        "--no-registry", action="store_true"
    )
    dcp_subset_sum_growing_chain.set_defaults(
        func=command_dcp_subset_sum_growing_chain
    )


def command_dcp_subset_sum_growing_chain(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_growing_order_chain_theorem,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [
        int(value.strip()) for value in args.n_values.split(",") if value.strip()
    ]
    epsilons = [
        float(value.strip())
        for value in args.epsilons.split(",")
        if value.strip()
    ]
    deficits = [
        float(value.strip())
        for value in args.near_log_deficits.split(",")
        if value.strip()
    ]
    controls = [
        int(value.strip())
        for value in args.exact_control_orders.split(",")
        if value.strip()
    ]
    payload = write_growing_order_chain_theorem(
        n_values=n_values,
        fixed_fraction_epsilons=epsilons,
        near_log_deficit_multipliers=deficits,
        register_offset=args.register_offset,
        exact_control_orders=controls,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP near-log growing-order lattice-chain theorem complete")
    print(
        "Artifact: "
        "research/classical_baselines/dcp_subset_sum_growing_order_chain_theorem.json"
    )
    print(
        "Exact controls/failures/max path: "
        f"{metrics['exact_control_count']}/"
        f"{metrics['exact_chain_bound_failure_count']}/"
        f"{metrics['maximum_exact_longest_nonself_path']}"
    )
    print(
        "Polynomial/fixed-fraction/near-log theorem counts: "
        f"{metrics['polynomial_chain_length_theorem_count']}/"
        f"{metrics['proved_fixed_fraction_log_obstruction_count']}/"
        f"{metrics['proved_near_log_deficit_obstruction_count']}"
    )
    print(f"Scaling rows: {metrics['row_count']}")
    print(f"Finite bounds below one: {metrics['finite_bound_below_one_row_count']}")
    print(
        "Final near-log/signed obstructions: "
        f"{metrics['proved_final_near_log_window_obstruction_count']}/"
        f"{metrics['proved_signed_statistic_obstruction_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_signed_l2(subparsers) -> None:
    dcp_subset_sum_signed_l2 = subparsers.add_parser(
        "dcp-subset-sum-signed-l2",
        help=(
            "Prove the conditional L2 identity and sparse-support obstruction "
            "for signed exact-hit observables chosen from exposed low bits."
        ),
    )
    dcp_subset_sum_signed_l2.add_argument(
        "--n-values",
        default="32,64,128,256,512",
    )
    dcp_subset_sum_signed_l2.add_argument(
        "--support-powers",
        default="1,2,4,8",
    )
    dcp_subset_sum_signed_l2.add_argument(
        "--log-multiplier",
        type=int,
        default=1,
    )
    dcp_subset_sum_signed_l2.add_argument(
        "--no-registry",
        action="store_true",
    )
    dcp_subset_sum_signed_l2.set_defaults(
        func=command_dcp_subset_sum_signed_l2
    )


def command_dcp_subset_sum_signed_l2(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_signed_l2_obstruction
    initialize_seed_registry(overwrite=False)
    n_values = [
        int(value.strip())
        for value in args.n_values.split(",")
        if value.strip()
    ]
    support_powers = [
        int(value.strip())
        for value in args.support_powers.split(",")
        if value.strip()
    ]
    payload = write_signed_l2_obstruction(
        n_values=n_values,
        support_powers=support_powers,
        log_multiplier=args.log_multiplier,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP conditional signed-L2 obstruction complete")
    print(
        "Artifact: research/classical_baselines/"
        "dcp_subset_sum_signed_l2_obstruction.json"
    )
    print(
        "Exact controls/pairs/failures: "
        f"{metrics['exact_control_count']}/"
        f"{metrics['exact_assignment_pair_count']}/"
        f"{metrics['exact_control_failure_count']}"
    )
    print(
        "Unit-minor/pair-independence/variance theorems: "
        f"{metrics['unit_minor_theorem_count']}/"
        f"{metrics['conditional_pairwise_independence_theorem_count']}/"
        f"{metrics['conditional_signed_variance_identity_theorem_count']}"
    )
    print(
        "Polynomial-support negligible-deviation theorems: "
        f"{metrics['polynomial_support_negligible_deviation_theorem_count']}"
    )
    print(
        "High-label-adaptive/dense/nonlinear obstructions: "
        f"{metrics['proved_high_label_adaptive_signed_obstruction_count']}/"
        f"{metrics['proved_dense_implicit_signed_obstruction_count']}/"
        f"{metrics['proved_nonlinear_signed_obstruction_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_sparse_characters(subparsers) -> None:
    dcp_subset_sum_sparse_characters = subparsers.add_parser(
        "dcp-subset-sum-sparse-characters",
        help=(
            "Obstruct every polynomially sparse subset-sum character "
            "truncation, including full-label adaptive frequency selection."
        ),
    )
    dcp_subset_sum_sparse_characters.add_argument(
        "--n-values",
        default="512,1024,4096,16384,65536",
    )
    dcp_subset_sum_sparse_characters.add_argument(
        "--register-offset",
        type=int,
        default=2,
    )
    dcp_subset_sum_sparse_characters.add_argument(
        "--amplitude-gap-power",
        type=int,
        default=12,
    )
    dcp_subset_sum_sparse_characters.add_argument(
        "--selected-frequency-power",
        type=int,
        default=4,
    )
    dcp_subset_sum_sparse_characters.add_argument(
        "--no-registry",
        action="store_true",
    )
    dcp_subset_sum_sparse_characters.set_defaults(
        func=command_dcp_subset_sum_sparse_characters
    )


def command_dcp_subset_sum_sparse_characters(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sparse_character_obstruction,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [
        int(value.strip())
        for value in args.n_values.split(",")
        if value.strip()
    ]
    payload = write_sparse_character_obstruction(
        n_values=n_values,
        register_offset=args.register_offset,
        amplitude_gap_power=args.amplitude_gap_power,
        selected_frequency_power=args.selected_frequency_power,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP adaptive sparse-character obstruction complete")
    print(
        "Artifact: research/classical_baselines/"
        "dcp_subset_sum_sparse_character_obstruction.json"
    )
    print(
        "Exact targets/failures/root-moment identities: "
        f"{metrics['exact_fourier_target_count']}/"
        f"{metrics['exact_control_failure_count']}/"
        f"{metrics['exact_root_moment_identity_count']}"
    )
    print(
        "Low/high/adaptive theorem counts: "
        f"{metrics['low_order_annihilation_theorem_count']}/"
        f"{metrics['high_order_simultaneous_moment_theorem_count']}/"
        f"{metrics['adaptive_sparse_selection_theorem_count']}"
    )
    print(
        "Finite conclusive source rows: "
        f"{metrics['finite_source_failure_bound_below_one_row_count']}/"
        f"{metrics['scaling_row_count']}"
    )
    print(
        "Dense/general lower-bound closures: "
        f"{metrics['proved_dense_implicit_character_obstruction_count']}/"
        f"{metrics['proved_general_computational_lower_bound_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_qtt(subparsers) -> None:
    dcp_subset_sum_qtt = subparsers.add_parser(
        "dcp-subset-sum-qtt",
        help=(
            "Search quantized tensor-train compression of the exact density-one "
            "subset-sum count vector under additive-half accuracy."
        ),
    )
    dcp_subset_sum_qtt.add_argument(
        "--n-values",
        default="8,10,12,14,16,18",
    )
    dcp_subset_sum_qtt.add_argument(
        "--register-offset",
        type=int,
        default=2,
    )
    dcp_subset_sum_qtt.add_argument(
        "--trials-per-size",
        type=int,
        default=2,
    )
    dcp_subset_sum_qtt.add_argument(
        "--random-order-count",
        type=int,
        default=3,
    )
    dcp_subset_sum_qtt.add_argument(
        "--registered-bond-power",
        type=int,
        default=1,
    )
    dcp_subset_sum_qtt.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_qtt.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_qtt.set_defaults(func=command_dcp_subset_sum_qtt)


def command_dcp_subset_sum_qtt(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_qtt_contraction_search
    initialize_seed_registry(overwrite=False)
    n_values = [
        int(value.strip())
        for value in args.n_values.split(",")
        if value.strip()
    ]
    payload = write_qtt_contraction_search(
        n_values=n_values,
        register_offset=args.register_offset,
        trials_per_size=args.trials_per_size,
        random_order_count=args.random_order_count,
        registered_bond_power=args.registered_bond_power,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum QTT dense-contraction search complete")
    print(
        "Artifact: research/classical_baselines/"
        "dcp_subset_sum_qtt_contraction_search.json"
    )
    print(
        "Instances/unfoldings/max n: "
        f"{metrics['instance_count']}/"
        f"{metrics['unfolding_row_count']}/"
        f"{metrics['maximum_n_bits']}"
    )
    print(
        "Tail registered-cap survivors/best source/control ranks: "
        f"{metrics['tail_source_registered_cap_survivor_count']}/"
        f"{metrics['tail_best_source_required_rank']}/"
        f"{metrics['tail_best_permuted_required_rank']}"
    )
    print(
        "Fitted log2 required-rank slope: "
        f"{metrics['fitted_log2_required_rank_slope_per_n']:.6g}"
    )
    print(
        "Tail raw/source-excess-over-zero/control coverage: "
        f"{metrics['tail_best_source_qtt_legal_coverage']:.6g}/"
        f"{metrics['tail_mean_source_qtt_coverage_excess_over_zero_frequency_constant']:.6g}/"
        f"{metrics['tail_mean_source_qtt_coverage_excess_over_permuted']:.6g}"
    )
    print(
        "Tail inverse-polynomial nontrivial excess instances: "
        f"{metrics['tail_inverse_polynomial_nontrivial_coverage_excess_instance_count']}"
    )
    print(
        "Asymptotic bond theorems/dense contractions/witness decoders: "
        f"{metrics['proved_asymptotic_qtt_bond_lower_bound_count']}/"
        f"{metrics['proved_polynomial_dense_character_contraction_count']}/"
        f"{metrics['polynomial_witness_decoder_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_embedding_volume(subparsers) -> None:
    dcp_subset_sum_embedding_volume = subparsers.add_parser(
        "dcp-subset-sum-embedding-volume",
        help="Prove exact standard and carry-sliced covolumes and audit volume-only gaps.",
    )
    dcp_subset_sum_embedding_volume.add_argument("--n-values", default="16,32,64,128,256")
    dcp_subset_sum_embedding_volume.add_argument("--register-offset", type=int, default=2)
    dcp_subset_sum_embedding_volume.add_argument("--log-multiplier", type=int, default=1)
    dcp_subset_sum_embedding_volume.add_argument("--embedding-scale", type=int, default=4)
    dcp_subset_sum_embedding_volume.add_argument("--low-constraint-scale", type=int, default=4)
    dcp_subset_sum_embedding_volume.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_embedding_volume.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_embedding_volume.set_defaults(func=command_dcp_subset_sum_embedding_volume)


def command_dcp_subset_sum_embedding_volume(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_embedding_volume_theorem
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_embedding_volume_theorem(
        n_values=n_values,
        register_offset=args.register_offset,
        log_multiplier=args.log_multiplier,
        embedding_scale=args.embedding_scale,
        low_constraint_scale=args.low_constraint_scale,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum embedding volume theorem complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_embedding_volume_theorem.json")
    print(f"Exact standard/sliced covolume theorems: {metrics['exact_standard_covolume_theorem_count']}/{metrics['exact_carry_sliced_covolume_theorem_count']}")
    print(f"Volume-only separation obstructions: {metrics['volume_only_asymptotic_separation_ruled_out_count']}")
    print(f"Limiting planted/Gaussian ratio: {metrics['limiting_witness_to_gaussian_scale_ratio']:.6g}")
    print(f"Local reduced-basis gaps: {metrics['proved_local_reduced_basis_separation_count']}")
    print(f"Polynomial witness decoders: {metrics['polynomial_witness_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_short_relations(subparsers) -> None:
    dcp_subset_sum_short_relations = subparsers.add_parser(
        "dcp-subset-sum-short-relations",
        help="Prove exponentially many short marker-zero competitors in the standard embedding.",
    )
    dcp_subset_sum_short_relations.add_argument("--n-values", default="32,64,128,256,512")
    dcp_subset_sum_short_relations.add_argument("--register-offset", type=int, default=2)
    dcp_subset_sum_short_relations.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_short_relations.set_defaults(func=command_dcp_subset_sum_short_relations)


def command_dcp_subset_sum_short_relations(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_short_relation_theorem
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_short_relation_theorem(
        n_values=n_values,
        register_offset=args.register_offset,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP standard-embedding short signed-relation theorem complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_short_relation_theorem.json")
    print(f"Expectation exponent: {metrics['asymptotic_log2_expectation_rate']:.6g}")
    print(f"Exact second-moment theorems: {metrics['exact_second_moment_theorem_count']}")
    print(f"High-probability competitor theorems: {metrics['high_probability_exponential_competitor_theorem_count']}")
    print(f"Standard uniqueness obstructions: {metrics['standard_embedding_shortest_vector_uniqueness_ruled_out_count']}")
    print(f"Carry-sliced relation obstructions: {metrics['carry_sliced_short_relation_obstruction_count']}")
    print(f"Polynomial witness decoders: {metrics['polynomial_witness_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_carry_relations(subparsers) -> None:
    dcp_subset_sum_carry_relations = subparsers.add_parser(
        "dcp-subset-sum-carry-relations",
        help="Prove inverse-polynomial source coverage of short carry-sliced competitors.",
    )
    dcp_subset_sum_carry_relations.add_argument("--n-values", default="32,64,128,256,512")
    dcp_subset_sum_carry_relations.add_argument("--register-offset", type=int, default=2)
    dcp_subset_sum_carry_relations.add_argument("--log-multiplier", type=int, default=1)
    dcp_subset_sum_carry_relations.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_carry_relations.set_defaults(func=command_dcp_subset_sum_carry_relations)


def command_dcp_subset_sum_carry_relations(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_carry_relation_theorem
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_carry_relation_theorem(
        n_values=n_values,
        register_offset=args.register_offset,
        log_multiplier=args.log_multiplier,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP carry-sliced balanced signed-relation theorem complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_carry_relation_theorem.json")
    print(f"Expectation exponent: {metrics['asymptotic_log2_expectation_rate']:.6g}")
    print(f"Inverse-polynomial coverage theorems: {metrics['inverse_polynomial_source_coverage_theorem_count']}")
    print(f"High-probability coverage theorems: {metrics['high_probability_source_coverage_theorem_count']}")
    print(f"Uniform isolation obstructions: {metrics['carry_sliced_uniform_shortest_vector_isolation_ruled_out_count']}")
    print(f"Tail log2 mean lower bound: {metrics['tail_log2_first_moment_lower_bound']:.6g}")
    print(f"Tail source-coverage lower bound: {metrics['tail_source_coverage_lower_bound']:.6g}")
    print(f"Marker-aware decoders: {metrics['polynomial_marker_aware_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_marker_coset(subparsers) -> None:
    dcp_subset_sum_marker_coset = subparsers.add_parser(
        "dcp-subset-sum-marker-coset",
        help="Prove marker-one bounded-distance search is exactly subset-sum witness search.",
    )
    dcp_subset_sum_marker_coset.add_argument("--n-values", default="16,32,64,128,256")
    dcp_subset_sum_marker_coset.add_argument("--register-offset", type=int, default=2)
    dcp_subset_sum_marker_coset.add_argument("--embedding-scale", type=int)
    dcp_subset_sum_marker_coset.add_argument("--low-constraint-scale", type=int)
    dcp_subset_sum_marker_coset.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_marker_coset.set_defaults(func=command_dcp_subset_sum_marker_coset)


def command_dcp_subset_sum_marker_coset(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_marker_coset_theorem
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_marker_coset_theorem(
        n_values=n_values,
        register_offset=args.register_offset,
        embedding_scale=args.embedding_scale,
        low_constraint_scale=args.low_constraint_scale,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum marker-coset equivalence theorem complete")
    print("Artifact: research/reductions/dcp_subset_sum_marker_coset_theorem.json")
    print(f"Kernel/coset decompositions: {metrics['exact_marker_kernel_affine_coset_decomposition_count']}")
    print(f"Witness-radius equivalences: {metrics['exact_witness_radius_equivalence_theorem_count']}")
    print(f"Marker gcd-one theorems: {metrics['basis_marker_gcd_one_theorem_count']}")
    print(f"Unbounded marker-one constructions: {metrics['polynomial_unbounded_marker_one_vector_theorem_count']}")
    print(f"Short marker-one decoders: {metrics['polynomial_short_marker_one_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_affine_cvp(subparsers) -> None:
    dcp_subset_sum_affine_cvp = subparsers.add_parser(
        "dcp-subset-sum-affine-cvp",
        help="Run exact marker-aware nearest-plane baselines in standard and carry-sliced cosets.",
    )
    dcp_subset_sum_affine_cvp.add_argument("--n-values", default="8,10,12,14")
    dcp_subset_sum_affine_cvp.add_argument("--register-offsets", default="2")
    dcp_subset_sum_affine_cvp.add_argument("--log-multiplier", type=int, default=1)
    dcp_subset_sum_affine_cvp.add_argument("--trials-per-row", type=int, default=3)
    dcp_subset_sum_affine_cvp.add_argument("--embedding-scale", type=int, default=4)
    dcp_subset_sum_affine_cvp.add_argument("--low-constraint-scale", type=int, default=4)
    dcp_subset_sum_affine_cvp.add_argument("--lll-delta", type=float, default=0.75)
    dcp_subset_sum_affine_cvp.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_affine_cvp.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_affine_cvp.set_defaults(func=command_dcp_subset_sum_affine_cvp)


def command_dcp_subset_sum_affine_cvp(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_affine_cvp_baseline
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [
        int(value.strip()) for value in args.register_offsets.split(",") if value.strip()
    ]
    payload = write_affine_cvp_baseline(
        n_values=n_values,
        register_offsets=register_offsets,
        log_multiplier=args.log_multiplier,
        trials_per_row=args.trials_per_row,
        embedding_scale=args.embedding_scale,
        low_constraint_scale=args.low_constraint_scale,
        lll_delta=args.lll_delta,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP marker-aware affine-CVP baseline complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_affine_cvp_baseline.json")
    print(f"Trials/legal: {metrics['trial_count']}/{metrics['legal_trial_count']}")
    print(f"Standard/carry legal successes: {metrics['standard_legal_success_count']}/{metrics['carry_sliced_legal_success_count']}")
    print(f"Tail standard/carry successes: {metrics['tail_standard_success_count']}/{metrics['tail_carry_sliced_success_count']}")
    print(f"Invalid witnesses: {metrics['invalid_witness_count']}")
    print(f"Marker-coset enforced trials: {metrics['marker_coset_enforced_trial_count']}")
    print(f"Coverage theorems: {metrics['proved_uniform_inverse_polynomial_coverage_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_affine_scaling(subparsers) -> None:
    dcp_subset_sum_affine_scaling = subparsers.add_parser(
        "dcp-subset-sum-affine-scaling",
        help="Scale exact-legality marker-aware affine nearest-plane attacks to larger n.",
    )
    dcp_subset_sum_affine_scaling.add_argument("--n-values", default="16,20,24,28,32")
    dcp_subset_sum_affine_scaling.add_argument("--register-offsets", default="2")
    dcp_subset_sum_affine_scaling.add_argument("--trials-per-row", type=int, default=2)
    dcp_subset_sum_affine_scaling.add_argument("--log-multiplier", type=int, default=1)
    dcp_subset_sum_affine_scaling.add_argument("--embedding-scale", type=int, default=4)
    dcp_subset_sum_affine_scaling.add_argument("--low-constraint-scale", type=int, default=4)
    dcp_subset_sum_affine_scaling.add_argument("--lll-delta", type=float, default=0.75)
    dcp_subset_sum_affine_scaling.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_affine_scaling.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_affine_scaling.set_defaults(func=command_dcp_subset_sum_affine_scaling)


def command_dcp_subset_sum_affine_scaling(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_affine_cvp_scaling
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [
        int(value.strip()) for value in args.register_offsets.split(",") if value.strip()
    ]
    payload = write_affine_cvp_scaling(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=args.trials_per_row,
        log_multiplier=args.log_multiplier,
        embedding_scale=args.embedding_scale,
        low_constraint_scale=args.low_constraint_scale,
        lll_delta=args.lll_delta,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP source-native affine-CVP scaling audit complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_affine_cvp_scaling.json")
    print(f"Trials/exact legality: {metrics['trial_count']}/{metrics['exact_mitm_legality_trial_count']}")
    print(f"Standard/carry legal successes: {metrics['standard_legal_success_count']}/{metrics['carry_sliced_legal_success_count']}")
    print(f"Tail standard/carry successes: {metrics['tail_standard_success_count']}/{metrics['tail_carry_sliced_success_count']}")
    print(f"Tail distance ratios: {metrics['tail_mean_standard_distance_ratio']:.6g}/{metrics['tail_mean_carry_sliced_distance_ratio']:.6g}")
    print(f"Maximum n: {metrics['maximum_n_bits']}")
    print(f"Coverage theorems: {metrics['proved_inverse_polynomial_legal_coverage_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_affine_bdd(subparsers) -> None:
    dcp_subset_sum_affine_bdd = subparsers.add_parser(
        "dcp-subset-sum-affine-bdd",
        help="Audit exact witness-specific Babai cells and global BDD conditions.",
    )
    dcp_subset_sum_affine_bdd.add_argument("--n-values", default="12,16,20,24,28,32")
    dcp_subset_sum_affine_bdd.add_argument("--register-offsets", default="2")
    dcp_subset_sum_affine_bdd.add_argument("--trials-per-row", type=int, default=2)
    dcp_subset_sum_affine_bdd.add_argument("--log-multiplier", type=int, default=1)
    dcp_subset_sum_affine_bdd.add_argument("--embedding-scale", type=int, default=4)
    dcp_subset_sum_affine_bdd.add_argument("--low-constraint-scale", type=int, default=4)
    dcp_subset_sum_affine_bdd.add_argument("--lll-delta", type=float, default=0.75)
    dcp_subset_sum_affine_bdd.add_argument("--witness-cap", type=int, default=256)
    dcp_subset_sum_affine_bdd.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_affine_bdd.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_affine_bdd.set_defaults(func=command_dcp_subset_sum_affine_bdd)


def command_dcp_subset_sum_affine_bdd(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_affine_bdd_geometry
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [
        int(value.strip()) for value in args.register_offsets.split(",") if value.strip()
    ]
    payload = write_affine_bdd_geometry(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=args.trials_per_row,
        log_multiplier=args.log_multiplier,
        embedding_scale=args.embedding_scale,
        low_constraint_scale=args.low_constraint_scale,
        lll_delta=args.lll_delta,
        witness_cap=args.witness_cap,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP exact affine Babai-cell geometry audit complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_affine_bdd_geometry.json")
    print(f"Trials/exact witness enumerations: {metrics['trial_count']}/{metrics['exact_witness_enumeration_trial_count']}")
    print(f"Standard/carry positive-cell trials: {metrics['standard_positive_babai_cell_trial_count']}/{metrics['carry_sliced_positive_babai_cell_trial_count']}")
    print(f"Tail standard/carry positive cells: {metrics['tail_standard_positive_cell_trial_count']}/{metrics['tail_carry_sliced_positive_cell_trial_count']}")
    print(f"Global BDD standard/carry trials: {metrics['standard_global_bdd_condition_trial_count']}/{metrics['carry_sliced_global_bdd_condition_trial_count']}")
    print(f"Prediction inconsistencies: {metrics['cell_prediction_inconsistency_count']}")
    print(f"Source BDD theorems: {metrics['proved_source_bdd_coverage_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_carry_slice_lattice(subparsers) -> None:
    dcp_subset_sum_carry_slice_lattice = subparsers.add_parser(
        "dcp-subset-sum-carry-slice-lattice",
        help="Compare unsliced LLL with all polynomially enumerable exact low-carry slices.",
    )
    dcp_subset_sum_carry_slice_lattice.add_argument("--n-values", default="10,12,14,16")
    dcp_subset_sum_carry_slice_lattice.add_argument("--register-offsets", default="2,4")
    dcp_subset_sum_carry_slice_lattice.add_argument("--log-multipliers", default="1")
    dcp_subset_sum_carry_slice_lattice.add_argument("--embedding-scales", default="4")
    dcp_subset_sum_carry_slice_lattice.add_argument("--low-constraint-scales", default="4")
    dcp_subset_sum_carry_slice_lattice.add_argument("--lll-deltas", default="0.75,0.99")
    dcp_subset_sum_carry_slice_lattice.add_argument("--combination-arities", default="1")
    dcp_subset_sum_carry_slice_lattice.add_argument("--trials-per-row", type=int, default=2)
    dcp_subset_sum_carry_slice_lattice.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_carry_slice_lattice.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_carry_slice_lattice.set_defaults(func=command_dcp_subset_sum_carry_slice_lattice)


def command_dcp_subset_sum_carry_slice_lattice(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_carry_slice_lattice_search,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    log_multipliers = [int(value.strip()) for value in args.log_multipliers.split(",") if value.strip()]
    embedding_scales = [int(value.strip()) for value in args.embedding_scales.split(",") if value.strip()]
    low_constraint_scales = [
        int(value.strip()) for value in args.low_constraint_scales.split(",") if value.strip()
    ]
    lll_deltas = [float(value.strip()) for value in args.lll_deltas.split(",") if value.strip()]
    combination_arities = [
        int(value.strip()) for value in args.combination_arities.split(",") if value.strip()
    ]
    payload = write_carry_slice_lattice_search(
        n_values=n_values,
        register_offsets=register_offsets,
        log_multipliers=log_multipliers,
        embedding_scales=embedding_scales,
        low_constraint_scales=low_constraint_scales,
        lll_deltas=lll_deltas,
        combination_arities=combination_arities,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP carry-sliced LLL audit complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_carry_slice_lattice.json")
    print(f"Rows/trials: {metrics['row_count']}/{metrics['trial_count']}")
    print(
        f"Baseline/carry-sliced successes: {metrics['baseline_success_count']}/"
        f"{metrics['carry_sliced_success_count']}"
    )
    print(
        f"Tail baseline/carry-sliced successes: {metrics['tail_baseline_success_count']}/"
        f"{metrics['tail_carry_sliced_success_count']}"
    )
    print(f"Carry-sliced-only successes: {metrics['carry_sliced_only_success_count']}")
    print(f"Uniform coverage proofs: {metrics['proved_uniform_inverse_polynomial_coverage_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_carry_high_part(subparsers) -> None:
    dcp_carry_high_part = subparsers.add_parser(
        "dcp-carry-high-part",
        help="Prove low-only carry selection leaves the high quotient exactly generic and charge carry sweeps.",
    )
    dcp_carry_high_part.add_argument("--n-values", default="32,64,128,256,512,1024")
    dcp_carry_high_part.add_argument("--register-offsets", default="2,4")
    dcp_carry_high_part.add_argument("--log-multipliers", default="1,2")
    dcp_carry_high_part.add_argument("--generic-event-exponent", type=float, default=0.05)
    dcp_carry_high_part.add_argument("--no-registry", action="store_true")
    dcp_carry_high_part.set_defaults(func=command_dcp_carry_high_part)


def command_dcp_carry_high_part(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_carry_high_part_no_go
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    log_multipliers = [int(value.strip()) for value in args.log_multipliers.split(",") if value.strip()]
    payload = write_carry_high_part_no_go(
        n_values=n_values,
        register_offsets=register_offsets,
        log_multipliers=log_multipliers,
        generic_event_exponent=args.generic_event_exponent,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP carry high-part distribution no-go complete")
    print("Artifact: research/classical_baselines/dcp_carry_high_part_no_go.json")
    print(f"Scaling rows: {metrics['scaling_row_count']}")
    print(f"Exact translation controls: {metrics['exact_translation_control_count']}")
    print(f"Translation control failures: {metrics['exact_translation_control_failure_count']}")
    print(f"Conditional product-uniformity theorems: {metrics['conditional_product_uniformity_theorem_count']}")
    print(f"Polynomial carry union-bound theorems: {metrics['polynomial_carry_union_bound_theorem_count']}")
    print(f"Joint low/high no-go theorems: {metrics['joint_low_high_geometry_no_go_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_carry_affine_degree_invariance(subparsers) -> None:
    dcp_carry_affine = subparsers.add_parser(
        "dcp-carry-affine-degree-invariance",
        help="Prove dense GL(m,2) preprocessing preserves linear ANF degree for 2-adic carries.",
    )
    dcp_carry_affine.add_argument("--modulus-bits", default="128,256,512,1024")
    dcp_carry_affine.add_argument("--no-registry", action="store_true")
    dcp_carry_affine.set_defaults(func=command_dcp_carry_affine_degree_invariance)


def command_dcp_carry_affine_degree_invariance(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_carry_affine_degree_report,
    )
    initialize_seed_registry(overwrite=False)
    modulus_bits = [int(v.strip()) for v in args.modulus_bits.split(",") if v.strip()]
    payload = write_carry_affine_degree_report(
        scaling_modulus_bits=modulus_bits,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP carry affine-degree invariance complete")
    print("Artifact: research/classical_baselines/dcp_carry_affine_degree_invariance.json")
    print(f"Scaling records: {metrics['scaling_record_count']}")
    print(f"Coefficient controls: {metrics['coefficient_control_count']}")
    print(f"Affine controls: {metrics['affine_control_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_boolean_coset_separation(subparsers) -> None:
    dcp_boolean_coset = subparsers.add_parser(
        "dcp-boolean-coset-separation",
        help="Prove uniform-legal Boolean witnesses are exponentially separated below half Hamming distance.",
    )
    dcp_boolean_coset.add_argument("--n-values", default="32,64,128,256,512,1024")
    dcp_boolean_coset.add_argument("--register-offsets", default="0,2,4")
    dcp_boolean_coset.add_argument("--radius-fractions", default="0.125,0.25")
    dcp_boolean_coset.add_argument("--finite-n-values", default="8,10,12")
    dcp_boolean_coset.add_argument("--finite-register-offset", type=int, default=2)
    dcp_boolean_coset.add_argument("--finite-trials", type=int, default=2)
    dcp_boolean_coset.add_argument("--seed", type=int, default=0)
    dcp_boolean_coset.add_argument("--no-registry", action="store_true")
    dcp_boolean_coset.set_defaults(func=command_dcp_boolean_coset_separation)


def command_dcp_boolean_coset_separation(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_boolean_coset_separation
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    radius_fractions = [float(value.strip()) for value in args.radius_fractions.split(",") if value.strip()]
    finite_n_values = [int(value.strip()) for value in args.finite_n_values.split(",") if value.strip()]
    payload = write_boolean_coset_separation(
        n_values=n_values,
        register_offsets=register_offsets,
        radius_fractions=radius_fractions,
        finite_n_values=finite_n_values,
        finite_register_offset=args.finite_register_offset,
        finite_trials=args.finite_trials,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP Boolean witness-coset separation theorem complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_boolean_coset_separation.json")
    print(f"Scaling/finite rows: {metrics['scaling_row_count']}/{metrics['finite_row_count']}")
    print(f"Exact source censuses: {metrics['exact_pair_census_count']}")
    print(f"Exact formula failures: {metrics['exact_pair_formula_failure_count']}")
    print(f"Uniform-legal source theorems: {metrics['uniform_legal_source_theorem_count']}")
    print(f"Tail inverse-polynomial close-pair no-go rows: {metrics['tail_inverse_polynomial_close_pair_no_go_row_count']}")
    print(f"Maximum tail exponent per n: {metrics['maximum_tail_exponent_per_n']:.6g}")
    print(f"Marker-aware decoders: {metrics['marker_aware_decoder_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_marker_list_decoder(subparsers) -> None:
    dcp_marker_list = subparsers.add_parser(
        "dcp-marker-list-decoder",
        help="Test polynomial fixed-depth nearest-plane lists in standard and carry-sliced marker cosets.",
    )
    dcp_marker_list.add_argument("--n-values", default="10,12,14,16")
    dcp_marker_list.add_argument("--register-offsets", default="2")
    dcp_marker_list.add_argument("--trials-per-row", type=int, default=2)
    dcp_marker_list.add_argument("--maximum-deviations", type=int, default=2)
    dcp_marker_list.add_argument("--log-multiplier", type=int, default=1)
    dcp_marker_list.add_argument("--embedding-scale", type=int, default=4)
    dcp_marker_list.add_argument("--low-constraint-scale", type=int, default=4)
    dcp_marker_list.add_argument("--lll-delta", type=float, default=0.75)
    dcp_marker_list.add_argument("--seed", type=int, default=0)
    dcp_marker_list.add_argument("--no-registry", action="store_true")
    dcp_marker_list.add_argument(
        "--register-existing",
        action="store_true",
        help="Register the current expensive sweep artifact without recomputing it.",
    )
    dcp_marker_list.set_defaults(func=command_dcp_marker_list_decoder)


def command_dcp_marker_list_decoder(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        load_and_register_marker_aware_list_decoder,
        validate_registry,
        write_marker_aware_list_decoder,
    )
    initialize_seed_registry(overwrite=False)
    if args.register_existing:
        payload = load_and_register_marker_aware_list_decoder()
    else:
        n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
        register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
        payload = write_marker_aware_list_decoder(
            n_values=n_values,
            register_offsets=register_offsets,
            trials_per_row=args.trials_per_row,
            maximum_deviations=args.maximum_deviations,
            log_multiplier=args.log_multiplier,
            embedding_scale=args.embedding_scale,
            low_constraint_scale=args.low_constraint_scale,
            lll_delta=args.lll_delta,
            seed=args.seed,
            write_registry=not args.no_registry,
        )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP marker-aware fixed-depth list decoder complete")
    print("Artifact: research/classical_baselines/dcp_marker_aware_list_decoder.json")
    print(f"Trials/rows: {metrics['trial_count']}/{metrics['row_count']}")
    print(f"Maximum n/depth: {metrics['maximum_n_bits']}/{metrics['maximum_branch_depth']}")
    print(f"Legal trials: {metrics['legal_trial_count']}")
    print(
        "Depth-zero/max-depth standard successes: "
        f"{metrics['standard_depth_zero_legal_success_count']}/"
        f"{metrics['standard_max_depth_legal_success_count']}"
    )
    print(
        "Depth-zero/max-depth carry successes: "
        f"{metrics['carry_depth_zero_legal_success_count']}/"
        f"{metrics['carry_max_depth_legal_success_count']}"
    )
    print(
        "Strict standard/carry list improvements: "
        f"{metrics['strict_standard_list_improvement_count']}/"
        f"{metrics['strict_carry_list_improvement_count']}"
    )
    print(f"Candidate-count theorem failures: {metrics['candidate_count_theorem_failure_count']}")
    print(f"Invalid returned witnesses: {metrics['invalid_witness_count']}")
    print(f"Coverage theorem count: {metrics['proved_inverse_polynomial_uniform_legal_coverage_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_marker_deviations(subparsers) -> None:
    dcp_marker_deviations = subparsers.add_parser(
        "dcp-marker-deviations",
        help="Replay every exact witness path to measure nearest-plane rounding deviation depth and offset.",
    )
    dcp_marker_deviations.add_argument("--n-values", default="20,24,28,32,36")
    dcp_marker_deviations.add_argument("--register-offsets", default="2")
    dcp_marker_deviations.add_argument("--trials-per-row", type=int, default=4)
    dcp_marker_deviations.add_argument("--log-multiplier", type=int, default=1)
    dcp_marker_deviations.add_argument("--embedding-scale", type=int, default=4)
    dcp_marker_deviations.add_argument("--low-constraint-scale", type=int, default=4)
    dcp_marker_deviations.add_argument("--lll-delta", type=float, default=0.75)
    dcp_marker_deviations.add_argument("--witness-cap", type=int, default=256)
    dcp_marker_deviations.add_argument("--seed", type=int, default=0)
    dcp_marker_deviations.add_argument("--no-registry", action="store_true")
    dcp_marker_deviations.set_defaults(func=command_dcp_marker_deviations)


def command_dcp_marker_deviations(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_marker_deviation_geometry
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    payload = write_marker_deviation_geometry(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=args.trials_per_row,
        log_multiplier=args.log_multiplier,
        embedding_scale=args.embedding_scale,
        low_constraint_scale=args.low_constraint_scale,
        lll_delta=args.lll_delta,
        witness_cap=args.witness_cap,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP exact marker-witness deviation geometry complete")
    print("Artifact: research/classical_baselines/dcp_marker_deviation_geometry.json")
    print(f"Trials/complete legal: {metrics['trial_count']}/{metrics['complete_witness_enumeration_trial_count']}")
    print(f"Maximum n: {metrics['maximum_n_bits']}")
    print(f"Exact replay failures: {metrics['exact_replay_failure_count']}")
    print(
        "Tail depth-two standard/carry predictions: "
        f"{metrics['tail_standard_depth_two_predicted_success_count']}/"
        f"{metrics['tail_carry_depth_two_predicted_success_count']} over "
        f"{metrics['tail_complete_legal_trial_count']} complete legal trials"
    )
    print(
        "Tail standard/carry one-step tree escapes: "
        f"{metrics['tail_standard_one_step_tree_escape_count']}/"
        f"{metrics['tail_carry_one_step_tree_escape_count']}"
    )
    print(f"Asymptotic deviation-growth theorems: {metrics['proved_asymptotic_deviation_growth_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_marker_all_targets(subparsers) -> None:
    dcp_marker_all_targets = subparsers.add_parser(
        "dcp-marker-all-targets",
        help="Enumerate the full Boolean cube and compute exact fixed-depth coverage over every legal target.",
    )
    dcp_marker_all_targets.add_argument("--n-values", default="14,16,18,20")
    dcp_marker_all_targets.add_argument("--register-offsets", default="2")
    dcp_marker_all_targets.add_argument("--trials-per-row", type=int, default=3)
    dcp_marker_all_targets.add_argument("--maximum-branch-depth", type=int, default=2)
    dcp_marker_all_targets.add_argument("--log-multiplier", type=int, default=1)
    dcp_marker_all_targets.add_argument("--embedding-scale", type=int, default=4)
    dcp_marker_all_targets.add_argument("--low-constraint-scale", type=int, default=4)
    dcp_marker_all_targets.add_argument("--lll-delta", type=float, default=0.75)
    dcp_marker_all_targets.add_argument("--seed", type=int, default=0)
    dcp_marker_all_targets.add_argument("--no-registry", action="store_true")
    dcp_marker_all_targets.set_defaults(func=command_dcp_marker_all_targets)


def command_dcp_marker_all_targets(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_marker_all_target_coverage,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    payload = write_marker_all_target_coverage(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=args.trials_per_row,
        maximum_branch_depth=args.maximum_branch_depth,
        log_multiplier=args.log_multiplier,
        embedding_scale=args.embedding_scale,
        low_constraint_scale=args.low_constraint_scale,
        lll_delta=args.lll_delta,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP exact all-target marker-list coverage census complete")
    print("Artifact: research/classical_baselines/dcp_marker_all_target_coverage.json")
    print(f"Label rows/max n/depth: {metrics['trial_count']}/{metrics['maximum_n_bits']}/{metrics['maximum_branch_depth']}")
    print(f"Assignments/legal targets: {metrics['exact_assignment_count']}/{metrics['exact_legal_target_count']}")
    print(f"Kernel/full-cube failures: {metrics['target_independent_kernel_failure_count']}/{metrics['full_boolean_cube_failure_count']}")
    print(
        "Tail mean standard/carry coverage: "
        f"{metrics['tail_mean_standard_max_depth_coverage']:.6g}/"
        f"{metrics['tail_mean_carry_max_depth_coverage']:.6g}"
    )
    print(
        "Tail mean standard/carry no-one-step fractions: "
        f"{metrics['tail_mean_standard_no_one_step_target_fraction']:.6g}/"
        f"{metrics['tail_mean_carry_no_one_step_target_fraction']:.6g}"
    )
    print(f"Asymptotic coverage bounds: {metrics['proved_asymptotic_fixed_depth_coverage_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_marker_vulnerable_coordinates(subparsers) -> None:
    dcp_marker_vulnerable = subparsers.add_parser(
        "dcp-marker-vulnerable-coordinates",
        help=(
            "Test polynomial lists that branch on public risk-ranked "
            "O(log n) nearest-plane coordinates."
        ),
    )
    dcp_marker_vulnerable.add_argument(
        "--n-values", default="14,18,22,26,30,36,42,48,56"
    )
    dcp_marker_vulnerable.add_argument("--register-offsets", default="2")
    dcp_marker_vulnerable.add_argument("--trials-per-row", type=int, default=3)
    dcp_marker_vulnerable.add_argument(
        "--selector-multiplier", type=int, default=2
    )
    dcp_marker_vulnerable.add_argument("--maximum-offset", type=int, default=1)
    dcp_marker_vulnerable.add_argument(
        "--assignment-samples", type=int, default=8192
    )
    dcp_marker_vulnerable.add_argument("--fixed-depth", type=int, default=2)
    dcp_marker_vulnerable.add_argument(
        "--exact-target-max-n", type=int, default=18
    )
    dcp_marker_vulnerable.add_argument(
        "--exact-trials-per-row", type=int, default=1
    )
    dcp_marker_vulnerable.add_argument("--log-multiplier", type=int, default=1)
    dcp_marker_vulnerable.add_argument("--embedding-scale", type=int, default=4)
    dcp_marker_vulnerable.add_argument(
        "--low-constraint-scale", type=int, default=4
    )
    dcp_marker_vulnerable.add_argument("--lll-delta", type=float, default=0.75)
    dcp_marker_vulnerable.add_argument("--seed", type=int, default=0)
    dcp_marker_vulnerable.add_argument("--no-registry", action="store_true")
    dcp_marker_vulnerable.add_argument(
        "--register-existing",
        action="store_true",
        help="Register the current expensive sweep artifact without recomputing it.",
    )
    dcp_marker_vulnerable.set_defaults(
        func=command_dcp_marker_vulnerable_coordinates
    )


def command_dcp_marker_vulnerable_coordinates(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        load_and_register_marker_vulnerable_coordinate_decoder,
        validate_registry,
        write_marker_vulnerable_coordinate_decoder,
    )
    initialize_seed_registry(overwrite=False)
    if args.register_existing:
        payload = load_and_register_marker_vulnerable_coordinate_decoder()
    else:
        n_values = [
            int(value.strip())
            for value in args.n_values.split(",")
            if value.strip()
        ]
        register_offsets = [
            int(value.strip())
            for value in args.register_offsets.split(",")
            if value.strip()
        ]
        payload = write_marker_vulnerable_coordinate_decoder(
            n_values=n_values,
            register_offsets=register_offsets,
            trials_per_row=args.trials_per_row,
            selector_multiplier=args.selector_multiplier,
            maximum_offset=args.maximum_offset,
            assignment_sample_count=args.assignment_samples,
            fixed_depth=args.fixed_depth,
            exact_target_max_n=args.exact_target_max_n,
            exact_trials_per_row=args.exact_trials_per_row,
            log_multiplier=args.log_multiplier,
            embedding_scale=args.embedding_scale,
            low_constraint_scale=args.low_constraint_scale,
            lll_delta=args.lll_delta,
            seed=args.seed,
            write_registry=not args.no_registry,
        )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP vulnerable-coordinate marker decoder audit complete")
    print(
        "Artifact: "
        "research/classical_baselines/dcp_marker_vulnerable_coordinate_decoder.json"
    )
    print(
        f"Trials/rows/max n: {metrics['trial_count']}/"
        f"{metrics['row_count']}/{metrics['maximum_n_bits']}"
    )
    print(
        "Exact cubes/assignments/legal targets: "
        f"{metrics['exact_full_cube_trial_count']}/"
        f"{metrics['exact_assignment_count']}/"
        f"{metrics['exact_legal_target_count']}"
    )
    print(
        "Tail sampled assignment coverage standard/carry: "
        f"{metrics['tail_standard_sampled_assignment_coverage']:.6g}/"
        f"{metrics['tail_carry_sampled_assignment_coverage']:.6g}"
    )
    print(
        "Coverage slopes standard/carry: "
        f"{metrics['standard_log2_coverage_slope_per_n']:.6g}/"
        f"{metrics['carry_log2_coverage_slope_per_n']:.6g}"
    )
    print(
        "List/transfer theorem failures: "
        f"{metrics['polynomial_selected_coordinate_list_theorem_count']}/"
        f"{metrics['transfer_sandwich_failure_count']}"
    )
    print(
        "Inverse-polynomial uniform-legal coverage theorems: "
        f"{metrics['proved_inverse_polynomial_uniform_legal_coverage_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_marker_chart_union(subparsers) -> None:
    dcp_marker_chart_union = subparsers.add_parser(
        "dcp-marker-chart-union",
        help=(
            "Learn a polynomial union of target-independent logarithmic "
            "nearest-plane coordinate charts."
        ),
    )
    dcp_marker_chart_union.add_argument(
        "--n-values", default="14,24,30,36,42,48,56,64"
    )
    dcp_marker_chart_union.add_argument("--register-offsets", default="2")
    dcp_marker_chart_union.add_argument("--trials-per-row", type=int, default=2)
    dcp_marker_chart_union.add_argument(
        "--selector-multiplier", type=int, default=2
    )
    dcp_marker_chart_union.add_argument(
        "--chart-budget-power", type=int, default=2
    )
    dcp_marker_chart_union.add_argument("--maximum-offset", type=int, default=1)
    dcp_marker_chart_union.add_argument(
        "--training-samples", type=int, default=0
    )
    dcp_marker_chart_union.add_argument(
        "--heldout-samples", type=int, default=0
    )
    dcp_marker_chart_union.add_argument(
        "--training-samples-per-n-squared", type=int, default=16
    )
    dcp_marker_chart_union.add_argument(
        "--heldout-samples-per-n-squared", type=int, default=8
    )
    dcp_marker_chart_union.add_argument(
        "--exact-target-max-n", type=int, default=14
    )
    dcp_marker_chart_union.add_argument(
        "--exact-trials-per-row", type=int, default=1
    )
    dcp_marker_chart_union.add_argument("--log-multiplier", type=int, default=1)
    dcp_marker_chart_union.add_argument("--embedding-scale", type=int, default=4)
    dcp_marker_chart_union.add_argument(
        "--low-constraint-scale", type=int, default=4
    )
    dcp_marker_chart_union.add_argument("--lll-delta", type=float, default=0.75)
    dcp_marker_chart_union.add_argument("--seed", type=int, default=0)
    dcp_marker_chart_union.add_argument("--no-registry", action="store_true")
    dcp_marker_chart_union.set_defaults(func=command_dcp_marker_chart_union)


def command_dcp_marker_chart_union(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_marker_chart_union_decoder,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [
        int(value.strip()) for value in args.n_values.split(",") if value.strip()
    ]
    register_offsets = [
        int(value.strip())
        for value in args.register_offsets.split(",")
        if value.strip()
    ]
    payload = write_marker_chart_union_decoder(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=args.trials_per_row,
        selector_multiplier=args.selector_multiplier,
        chart_budget_power=args.chart_budget_power,
        maximum_offset=args.maximum_offset,
        training_sample_count=args.training_samples,
        heldout_sample_count=args.heldout_samples,
        training_samples_per_n_squared=args.training_samples_per_n_squared,
        heldout_samples_per_n_squared=args.heldout_samples_per_n_squared,
        exact_target_max_n=args.exact_target_max_n,
        exact_trials_per_row=args.exact_trials_per_row,
        log_multiplier=args.log_multiplier,
        embedding_scale=args.embedding_scale,
        low_constraint_scale=args.low_constraint_scale,
        lll_delta=args.lll_delta,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP learned marker chart-union decoder audit complete")
    print(
        "Artifact: "
        "research/classical_baselines/dcp_marker_chart_union_decoder.json"
    )
    print(
        f"Trials/rows/max n: {metrics['trial_count']}/"
        f"{metrics['row_count']}/{metrics['maximum_n_bits']}"
    )
    print(
        "Train/held-out samples: "
        f"{metrics['training_sample_count']}/{metrics['heldout_sample_count']}"
    )
    print(
        "Maximum charts/candidate upper bound: "
        f"{metrics['maximum_chart_count']}/"
        f"{metrics['maximum_candidate_count_upper_bound']}"
    )
    print(
        "Tail carry held-out/max-row coverage: "
        f"{metrics['tail_carry_heldout_coverage']:.6g}/"
        f"{metrics['tail_maximum_carry_heldout_coverage']:.6g}"
    )
    print(
        "Held-out slopes standard/carry: "
        f"{metrics['standard_log2_heldout_coverage_slope_per_n']:.6g}/"
        f"{metrics['carry_log2_heldout_coverage_slope_per_n']:.6g}"
    )
    print(
        "Polynomial/target/train-test/transfer failures: "
        f"{metrics['polynomial_chart_union_theorem_count']}/"
        f"{metrics['target_independent_selector_failure_count']}/"
        f"{metrics['disjoint_train_test_failure_count']}/"
        f"{metrics['transfer_sandwich_failure_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_marker_target_beam(subparsers) -> None:
    dcp_marker_target_beam = subparsers.add_parser(
        "dcp-marker-target-beam",
        help=(
            "Run a source-native target-adaptive polynomial K-best "
            "nearest-plane baseline."
        ),
    )
    dcp_marker_target_beam.add_argument(
        "--n-values", default="12,16,20,24,32,40,48"
    )
    dcp_marker_target_beam.add_argument("--register-offsets", default="2")
    dcp_marker_target_beam.add_argument("--trials-per-row", type=int, default=2)
    dcp_marker_target_beam.add_argument(
        "--standard-width-powers", default="1,2"
    )
    dcp_marker_target_beam.add_argument(
        "--carry-width-powers", default="1,2"
    )
    dcp_marker_target_beam.add_argument("--maximum-offset", type=int, default=1)
    dcp_marker_target_beam.add_argument(
        "--exact-legality-max-n", type=int, default=20
    )
    dcp_marker_target_beam.add_argument("--log-multiplier", type=int, default=1)
    dcp_marker_target_beam.add_argument("--embedding-scale", type=int, default=4)
    dcp_marker_target_beam.add_argument(
        "--low-constraint-scale", type=int, default=4
    )
    dcp_marker_target_beam.add_argument("--lll-delta", type=float, default=0.75)
    dcp_marker_target_beam.add_argument("--seed", type=int, default=0)
    dcp_marker_target_beam.add_argument("--no-registry", action="store_true")
    dcp_marker_target_beam.add_argument(
        "--register-existing",
        action="store_true",
        help="Register the current expensive sweep artifact without recomputing it.",
    )
    dcp_marker_target_beam.set_defaults(
        func=command_dcp_marker_target_beam
    )


def command_dcp_marker_target_beam(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        load_and_register_target_adaptive_beam_audit,
        validate_registry,
        write_target_adaptive_beam_audit,
    )
    initialize_seed_registry(overwrite=False)
    if args.register_existing:
        payload = load_and_register_target_adaptive_beam_audit()
    else:
        n_values = [
            int(value.strip())
            for value in args.n_values.split(",")
            if value.strip()
        ]
        register_offsets = [
            int(value.strip())
            for value in args.register_offsets.split(",")
            if value.strip()
        ]
        standard_powers = [
            int(value.strip())
            for value in args.standard_width_powers.split(",")
            if value.strip()
        ]
        carry_powers = [
            int(value.strip())
            for value in args.carry_width_powers.split(",")
            if value.strip()
        ]
        payload = write_target_adaptive_beam_audit(
            n_values=n_values,
            register_offsets=register_offsets,
            trials_per_row=args.trials_per_row,
            standard_width_powers=standard_powers,
            carry_width_powers=carry_powers,
            maximum_offset=args.maximum_offset,
            exact_legality_max_n=args.exact_legality_max_n,
            log_multiplier=args.log_multiplier,
            embedding_scale=args.embedding_scale,
            low_constraint_scale=args.low_constraint_scale,
            lll_delta=args.lll_delta,
            seed=args.seed,
            write_registry=not args.no_registry,
        )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP target-adaptive marker beam audit complete")
    print(
        "Artifact: research/classical_baselines/"
        "dcp_marker_target_adaptive_beam.json"
    )
    print(
        f"Trials/rows/max n: {metrics['trial_count']}/"
        f"{metrics['row_count']}/{metrics['maximum_n_bits']}"
    )
    print(
        "Maximum standard/carry width powers: "
        f"{metrics['maximum_standard_width_power']}/"
        f"{metrics['maximum_carry_width_power']}"
    )
    print(
        "Tail max-power source success standard/carry: "
        f"{metrics['tail_standard_max_power_source_success_rate']:.6g}/"
        f"{metrics['tail_carry_max_power_source_success_rate']:.6g}"
    )
    print(
        "Exact-rounding/state-bound/invalid-output failures: "
        f"{metrics['exact_rounding_failure_count']}/"
        f"{metrics['state_bound_failure_count']}/"
        f"{metrics['invalid_marker_candidate_count']}"
    )
    print(
        "Inverse-polynomial uniform-source theorems: "
        f"{metrics['proved_inverse_polynomial_uniform_source_success_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_target_distribution(subparsers) -> None:
    dcp_subset_sum_target_distribution = subparsers.add_parser(
        "dcp-subset-sum-target-distribution",
        help="Separate uniform source, uniform legal, and planted subset-sum target multiplicity laws.",
    )
    dcp_subset_sum_target_distribution.add_argument("--n-values", default="10,12,14,16,18")
    dcp_subset_sum_target_distribution.add_argument("--register-offsets", default="0,2,4")
    dcp_subset_sum_target_distribution.add_argument("--trials-per-row", type=int, default=2)
    dcp_subset_sum_target_distribution.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_target_distribution.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_target_distribution.set_defaults(func=command_dcp_subset_sum_target_distribution)


def command_dcp_subset_sum_target_distribution(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_target_distribution_audit
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [int(value.strip()) for value in args.register_offsets.split(",") if value.strip()]
    payload = write_target_distribution_audit(
        n_values=n_values,
        register_offsets=register_offsets,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum target-distribution audit complete")
    print("Artifact: research/classical_baselines/dcp_subset_sum_target_distribution.json")
    print(f"Rows/moment certificates: {metrics['row_count']}/{metrics['moment_certificate_count']}")
    print(
        "Mean tail planted-vs-uniform-legal TV: "
        f"{metrics['mean_tail_planted_vs_uniform_legal_total_variation']:.6g}"
    )
    print(
        "Maximum tail planted multiplicity mean ratio: "
        f"{metrics['maximum_tail_planted_to_uniform_legal_mean_ratio']:.6g}"
    )
    print(
        "Maximum tail uniform-target quadratic-tail probability: "
        f"{metrics['maximum_tail_uniform_target_quadratic_tail_probability']:.6g}"
    )
    print(f"Polynomial representation solvers: {metrics['proved_polynomial_representation_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_coherent_matching(subparsers) -> None:
    dcp_coherent_matching = subparsers.add_parser(
        "dcp-coherent-matching",
        help="Audit conditional clean pairing readouts, source coverage, workspace and noise; no efficient finder supplied.",
    )
    dcp_coherent_matching.add_argument("--n-values", default="16,32,64,128")
    dcp_coherent_matching.add_argument("--coverage-exponents", default="1,2,3")
    dcp_coherent_matching.add_argument("--register-offset", type=int, default=4)
    dcp_coherent_matching.add_argument("--no-registry", action="store_true")
    dcp_coherent_matching.set_defaults(func=command_dcp_coherent_matching)


def command_dcp_coherent_matching(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_coherent_matching_interface_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    coverage_exponents = [
        int(value.strip()) for value in args.coverage_exponents.split(",") if value.strip()
    ]
    payload = write_coherent_matching_interface_audit(
        n_values=n_values,
        legal_coverage_exponents=coverage_exponents,
        register_offset=args.register_offset,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP coherent matching-interface audit complete")
    print("Artifact: research/reductions/dcp_coherent_matching_interface.json")
    print(f"Primary-source deterministic use sites: {metrics['primary_source_deterministic_use_site_count']}")
    print(
        f"Seeded randomized bridge certificates: "
        f"{metrics['proved_seeded_randomized_solver_bridge_count']}/"
        f"{metrics['seeded_bridge_certificate_count']}"
    )
    print(f"Zero-visibility counterexamples: {metrics['zero_visibility_counterexample_count']}")
    print(
        "Arbitrary quantum relation bridges in this single-evaluation audit only: "
        f"{metrics['proved_arbitrary_quantum_relation_solver_bridge_count']}"
    )
    print(f"Physical pairing/permutation controls: {metrics['physical_pairing_control_count']}/{metrics['physical_permutation_control_count']}")
    print(f"Physical failures: {metrics['physical_pairing_failure_count']}")
    print(f"Exact noise-envelope rows: {metrics['noise_mass_envelope_count']}")
    print(f"Correlated-fault controls: {metrics['correlated_noise_control_count']}")
    print(f"Efficient high-coverage pairing finders: {metrics['efficient_pairing_finder_count']}")
    print(f"Explicit exponential-time pairing finders: {metrics['explicit_exponential_pairing_finder_count']}")
    print(f"Balanced MITM source/program controls: {metrics['balanced_mitm_source_control_count']}/{metrics['balanced_mitm_program_control_count']}")
    print("Balanced MITM: fixed sorting network; exponential time and coherent storage, no QRAM assumed.")
    print(f"List-free coherent edge readouts: {metrics['list_free_edge_sampler_count']}; physical controls: {metrics['coherent_edge_physical_control_count']}")
    print("Shared geometric Grover time: polynomial workspace, no unique partner or vertex isolation; still exponential time.")
    print(f"Partial subset-sum solvers: {metrics['proved_polynomial_partial_subset_sum_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"] or metrics["physical_pairing_failure_count"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_quantum_relation_fidelity(subparsers) -> None:
    dcp_quantum_relation_fidelity = subparsers.add_parser(
        "dcp-quantum-relation-fidelity",
        help="Audit paired witness/history fidelity for concrete quantum relation solver interfaces.",
    )
    dcp_quantum_relation_fidelity.add_argument("--no-registry", action="store_true")
    dcp_quantum_relation_fidelity.set_defaults(func=command_dcp_quantum_relation_fidelity)


def command_dcp_quantum_relation_fidelity(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_quantum_relation_fidelity_audit,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_quantum_relation_fidelity_audit(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP quantum relation paired-workspace fidelity audit complete")
    print("Artifact: research/reductions/dcp_quantum_relation_fidelity.json")
    print(f"Mechanisms: {metrics['mechanism_count']}")
    print(f"Exact zero-visibility mechanisms: {metrics['exact_zero_visibility_count']}")
    print(f"Exponential history-overlap mechanisms: {metrics['exponential_history_overlap_count']}")
    print(f"Inverse-polynomial overlap proofs: {metrics['proved_inverse_polynomial_overlap_count']}")
    print(f"Polynomial partial solvers: {metrics['proved_polynomial_partial_solver_count']}")
    print(f"Full quantum relation compositions: {metrics['proved_full_quantum_relation_composition_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_quantum_walk_source_audit(subparsers) -> None:
    dcp_quantum_walk_source_audit = subparsers.add_parser(
        "dcp-quantum-walk-source-audit",
        help="Audit the 0.2182 subset-sum quantum walk directly against cached primary-source LaTeX.",
    )
    dcp_quantum_walk_source_audit.add_argument("--no-registry", action="store_true")
    dcp_quantum_walk_source_audit.set_defaults(func=command_dcp_quantum_walk_source_audit)


def command_dcp_quantum_walk_source_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_quantum_walk_source_audit
    initialize_seed_registry(overwrite=False)
    payload = write_quantum_walk_source_audit(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP 0.2182 quantum-walk primary-source audit complete")
    print("Artifact: research/reductions/dcp_quantum_walk_source_audit.json")
    print(
        f"Verified source claims: {metrics['verified_source_claim_count']}/"
        f"{metrics['primary_source_claim_count']}"
    )
    print(
        "Internal history-independence certificates: "
        f"{metrics['internal_history_independence_certificate_count']}"
    )
    print(f"Positive exponential time rows: {metrics['positive_exponential_time_count']}")
    print(f"QRAQM-required rows: {metrics['qraqm_required_count']}")
    print(
        "Paired-endpoint output fidelity theorems: "
        f"{metrics['paired_endpoint_output_fidelity_theorem_count']}"
    )
    print(f"Full Regev compositions: {metrics['full_regev_composition_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_symmetric_relation_lift(subparsers) -> None:
    dcp_symmetric_relation_lift = subparsers.add_parser(
        "dcp-symmetric-relation-lift",
        help="Prove the symmetric double-evaluation interface for purified quantum relation solvers.",
    )
    dcp_symmetric_relation_lift.add_argument("--no-registry", action="store_true")
    dcp_symmetric_relation_lift.set_defaults(func=command_dcp_symmetric_relation_lift)


def command_dcp_symmetric_relation_lift(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_symmetric_relation_lift_audit,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_symmetric_relation_lift_audit(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP symmetric quantum-relation matching lift complete")
    print("Artifact: research/reductions/dcp_symmetric_relation_lift.json")
    print(
        f"Verified Regev source sites: {metrics['verified_primary_source_site_count']}/"
        f"{metrics['primary_source_site_count']}"
    )
    print(f"Exact symmetric pair identities: {metrics['exact_symmetric_pair_identity_count']}")
    print(
        "Coherent relation interface certificates: "
        f"{metrics['coherent_relation_interface_certificate_count']}"
    )
    print(
        "Weighted matching loss exponents (fixed-list/global-source): "
        f"{metrics['fixed_list_weighted_matching_loss_exponent']}/"
        f"{metrics['global_source_weighted_matching_loss_exponent']}"
    )
    print(f"Polynomial relation solvers: {metrics['proved_polynomial_relation_solver_count']}")
    print(
        "Product-contamination composition certificates: "
        f"{metrics['product_contamination_composition_certificate_count']}"
    )
    print(f"End-to-end DCP speedups: {metrics['proved_end_to_end_dcp_speedup_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_fiber_transport(subparsers) -> None:
    dcp_fiber_transport = subparsers.add_parser(
        "dcp-fiber-transport",
        help="Audit exact 2-adic child-fiber transports and explicit local-dictionary limits.",
    )
    dcp_fiber_transport.add_argument("--n-values", default="32,64,128,256")
    dcp_fiber_transport.add_argument("--register-offset", type=int, default=4)
    dcp_fiber_transport.add_argument("--trials-per-size", type=int, default=3)
    dcp_fiber_transport.add_argument("--seed", type=int, default=0)
    dcp_fiber_transport.add_argument("--no-registry", action="store_true")
    dcp_fiber_transport.set_defaults(func=command_dcp_fiber_transport)


def command_dcp_fiber_transport(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_two_adic_fiber_transport_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_two_adic_fiber_transport_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        trials_per_size=args.trials_per_size,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP 2-adic fiber-transport audit complete")
    print("Artifact: research/phase_workbench/dcp_two_adic_fiber_transport.json")
    print(f"Exact transport identities: {metrics['exact_identity_certificate_count']}")
    print(
        "Maximum single/swap/block depths: "
        f"{metrics['maximum_observed_single_flip_depth']}/"
        f"{metrics['maximum_observed_swap_depth']}/"
        f"{metrics['maximum_observed_block_transport_depth']}"
    )
    print(
        "Local-dictionary linear-depth no-go rows: "
        f"{metrics['local_dictionary_linear_depth_no_go_count']}"
    )
    print(
        "Open implicit transport architectures: "
        f"{metrics['open_implicit_transport_architecture_count']}"
    )
    print(f"Polynomial relation solvers: {metrics['proved_polynomial_relation_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_fiber_graph(subparsers) -> None:
    dcp_fiber_graph = subparsers.add_parser(
        "dcp-fiber-graph",
        help="Build exact low-fiber transport graphs and audit components, gaps, and classical traversal.",
    )
    dcp_fiber_graph.add_argument("--n-values", default="8,10,12,14")
    dcp_fiber_graph.add_argument("--register-offset", type=int, default=2)
    dcp_fiber_graph.add_argument("--trials-per-depth", type=int, default=2)
    dcp_fiber_graph.add_argument("--block-size", type=int, default=3)
    dcp_fiber_graph.add_argument("--seed", type=int, default=0)
    dcp_fiber_graph.add_argument("--no-registry", action="store_true")
    dcp_fiber_graph.set_defaults(func=command_dcp_fiber_graph)


def command_dcp_fiber_graph(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_fiber_transport_graph_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_fiber_transport_graph_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        trials_per_depth=args.trials_per_depth,
        seed=args.seed,
        block_size=args.block_size,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP exact fiber-transport graph audit complete")
    print("Artifact: research/phase_workbench/dcp_fiber_transport_graph.json")
    print(f"Exact graph rows: {metrics['row_count']}")
    print(f"Linear-depth rows: {metrics['linear_depth_row_count']}")
    print(f"Fragmented linear-depth rows: {metrics['fragmented_linear_depth_row_count']}")
    print(
        "Zero cross-child linear-depth rows: "
        f"{metrics['zero_cross_child_linear_depth_row_count']}"
    )
    print(
        "Minimum positive finite linear-depth gap: "
        f"{metrics['minimum_positive_linear_depth_spectral_gap']:.6g}"
    )
    print(f"Polynomial walk theorems: {metrics['proved_polynomial_fiber_transport_walk_count']}")
    print(f"Classical separations: {metrics['proved_classical_separation_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_signed_permutation_transport(subparsers) -> None:
    dcp_signed_permutation_transport = subparsers.add_parser(
        "dcp-signed-permutation-transport",
        help="Classify total signed-coordinate next-bit transports and their linear-depth incidence.",
    )
    dcp_signed_permutation_transport.add_argument("--n-values", default="32,64,128,256")
    dcp_signed_permutation_transport.add_argument("--register-offset", type=int, default=4)
    dcp_signed_permutation_transport.add_argument("--no-registry", action="store_true")
    dcp_signed_permutation_transport.set_defaults(
        func=command_dcp_signed_permutation_transport
    )


def command_dcp_signed_permutation_transport(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_signed_permutation_transport_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_signed_permutation_transport_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP signed-permutation transport classification complete")
    print("Artifact: research/phase_workbench/dcp_signed_permutation_transport.json")
    print(f"Exact classification theorems: {metrics['exact_classification_theorem_count']}")
    print(f"Exhaustive label tuples: {metrics['exhaustive_label_tuple_count']}")
    print(f"Classification mismatches: {metrics['exhaustive_classification_mismatch_count']}")
    print(
        "Linear-depth exponential no-go rows: "
        f"{metrics['linear_depth_exponential_no_go_row_count']}/"
        f"{metrics['linear_depth_scaling_row_count']}"
    )
    print(
        "Maximum linear-depth transport probability bound: "
        f"{metrics['maximum_linear_depth_transport_probability_bound']:.6g}"
    )
    print(f"Polynomial relation solvers: {metrics['proved_polynomial_relation_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_affine_transport(subparsers) -> None:
    dcp_affine_transport = subparsers.add_parser(
        "dcp-affine-transport",
        help="Audit exact GF(2)-affine transport congruences and witness extraction.",
    )
    dcp_affine_transport.add_argument("--n-values", default="32,64,128,256")
    dcp_affine_transport.add_argument("--register-offset", type=int, default=4)
    dcp_affine_transport.add_argument("--no-registry", action="store_true")
    dcp_affine_transport.set_defaults(func=command_dcp_affine_transport)


def command_dcp_affine_transport(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_affine_transport_audit
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_affine_transport_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP GF(2)-affine transport audit complete")
    print("Artifact: research/phase_workbench/dcp_affine_transport.json")
    print(f"Exact ANF theorems: {metrics['exact_anf_theorem_count']}")
    print(f"ANF/truth-table mismatches: {metrics['anf_vs_truth_table_mismatch_count']}")
    print(f"Zero-image witness reductions: {metrics['zero_image_witness_reduction_count']}")
    print(f"Affine-only small instances: {metrics['nonmonomial_affine_only_instance_count']}")
    print(f"Polynomial affine searches: {metrics['polynomial_affine_search_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_fiber_balance(subparsers) -> None:
    dcp_fiber_balance = subparsers.add_parser(
        "dcp-fiber-balance",
        help="Prove the total-transport Fourier obstruction and audit target-fiber partial pairability.",
    )
    dcp_fiber_balance.add_argument("--n-values", default="8,10,12,14,16")
    dcp_fiber_balance.add_argument("--register-offset", type=int, default=2)
    dcp_fiber_balance.add_argument("--trials-per-depth", type=int, default=2)
    dcp_fiber_balance.add_argument("--seed", type=int, default=0)
    dcp_fiber_balance.add_argument("--no-registry", action="store_true")
    dcp_fiber_balance.set_defaults(func=command_dcp_fiber_balance)


def command_dcp_fiber_balance(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_fiber_balance_obstruction_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_fiber_balance_obstruction_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        trials_per_depth=args.trials_per_depth,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP fiber-balance Fourier obstruction audit complete")
    print("Artifact: research/phase_workbench/dcp_fiber_balance_obstruction.json")
    print(
        "Exact total-transport Fourier theorems: "
        f"{metrics['exact_total_transport_fourier_theorem_count']}"
    )
    print(f"Finite theorem mismatches: {metrics['finite_theorem_mismatch_count']}")
    print(
        "Linear-depth pivot rows: "
        f"{metrics['linear_depth_pivot_row_count']}/{metrics['linear_depth_row_count']}"
    )
    print(
        "Linear-depth optimal partial-pairing mass range: "
        f"{metrics['minimum_linear_depth_optimal_partial_pairing_mass']:.6g}-"
        f"{metrics['maximum_linear_depth_optimal_partial_pairing_mass']:.6g}"
    )
    print(f"Polynomial target-fiber maps: {metrics['proved_polynomial_target_fiber_map_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_partial_relations(subparsers) -> None:
    dcp_partial_relations = subparsers.add_parser(
        "dcp-partial-relations",
        help="Prove source-coverage limits for polynomial signed-difference partial-map dictionaries.",
    )
    dcp_partial_relations.add_argument("--n-values", default="64,128,256,512,1024")
    dcp_partial_relations.add_argument("--register-offset", type=int, default=4)
    dcp_partial_relations.add_argument("--finite-n-values", default="6,8,10")
    dcp_partial_relations.add_argument("--finite-register-offset", type=int, default=2)
    dcp_partial_relations.add_argument("--finite-trials", type=int, default=2)
    dcp_partial_relations.add_argument("--seed", type=int, default=0)
    dcp_partial_relations.add_argument("--no-registry", action="store_true")
    dcp_partial_relations.set_defaults(func=command_dcp_partial_relations)


def command_dcp_partial_relations(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_partial_relation_coverage_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    finite_n_values = [
        int(value.strip()) for value in args.finite_n_values.split(",") if value.strip()
    ]
    payload = write_partial_relation_coverage_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        finite_n_values=finite_n_values,
        finite_register_offset=args.finite_register_offset,
        finite_trials=args.finite_trials,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP explicit partial-relation coverage audit complete")
    print("Artifact: research/phase_workbench/dcp_partial_relation_coverage.json")
    print(f"Asymptotic union-bound exponent: {metrics['asymptotic_union_bound_exponent']:.6g}")
    print(
        "Linear minimum-support theorems: "
        f"{metrics['linear_minimum_support_theorem_count']}"
    )
    print(
        "Polynomial dictionary coverage theorems: "
        f"{metrics['polynomial_dictionary_exponential_coverage_theorem_count']}"
    )
    print(
        "Implicit target-indexed map no-go theorems: "
        f"{metrics['proved_target_indexed_implicit_map_no_go_count']}"
    )
    print(f"Polynomial relation solvers: {metrics['proved_polynomial_relation_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_target_locality(subparsers) -> None:
    dcp_target_locality = subparsers.add_parser(
        "dcp-target-locality",
        help="Prove locality limits for arbitrary target-indexed child-fiber partner maps.",
    )
    dcp_target_locality.add_argument("--n-values", default="128,256,512,1024,2048")
    dcp_target_locality.add_argument("--register-offset", type=int, default=4)
    dcp_target_locality.add_argument("--finite-n-values", default="12,16,20,24")
    dcp_target_locality.add_argument("--finite-trials", type=int, default=3)
    dcp_target_locality.add_argument("--seed", type=int, default=0)
    dcp_target_locality.add_argument("--depth-fraction", type=float, default=0.5)
    dcp_target_locality.add_argument("--locality-fraction", type=float, default=0.09)
    dcp_target_locality.add_argument("--no-registry", action="store_true")
    dcp_target_locality.add_argument("--verbose", action="store_true")
    dcp_target_locality.set_defaults(func=command_dcp_target_locality)


def command_dcp_target_locality(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_target_indexed_locality_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    finite_n_values = [
        int(value.strip()) for value in args.finite_n_values.split(",") if value.strip()
    ]
    payload = write_target_indexed_locality_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        finite_n_values=finite_n_values,
        finite_trials=args.finite_trials,
        seed=args.seed,
        depth_fraction=args.depth_fraction,
        locality_fraction=args.locality_fraction,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP target-indexed locality obstruction complete")
    print("Artifact: research/phase_workbench/dcp_target_indexed_locality.json")
    print(
        "Locality exponent / entropy threshold: "
        f"{metrics['asymptotic_locality_union_bound_exponent']:.6g} / "
        f"{metrics['entropy_threshold_locality_fraction']:.6g}"
    )
    print(
        "Target-indexed local / polynomial-batch no-go theorems: "
        f"{metrics['arbitrary_target_indexed_local_map_no_go_theorem_count']}/"
        f"{metrics['polynomial_source_batch_local_map_no_go_theorem_count']}"
    )
    print(
        "Polynomial classical / quantum relation solvers: "
        f"{metrics['polynomial_classical_relation_solver_count']}/"
        f"{metrics['polynomial_quantum_relation_solver_count']}"
    )
    print(
        "Unrestricted linear-support time lower bounds: "
        f"{metrics['unrestricted_linear_support_time_lower_bound_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['quantum_speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for row in payload["scaling_rows"]:
            print(
                f"- n={row['n_bits']} k={row['depth']} support<={row['maximum_local_support']} "
                f"log2 single/batch bounds={row['log2_single_source_union_bound']:.3f}/"
                f"{row['log2_polynomial_batch_union_bound']:.3f}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_fiber_entanglement(subparsers) -> None:
    dcp_fiber_entanglement = subparsers.add_parser(
        "dcp-fiber-entanglement",
        help="Derive exact subset-sum fiber Schmidt spectra and tensor-network bond obstructions.",
    )
    dcp_fiber_entanglement.add_argument("--n-values", default="32,64,128,256,512")
    dcp_fiber_entanglement.add_argument("--finite-n-values", default="12,16,20,24,28")
    dcp_fiber_entanglement.add_argument("--register-offset", type=int, default=4)
    dcp_fiber_entanglement.add_argument("--finite-trials", type=int, default=2)
    dcp_fiber_entanglement.add_argument("--seed", type=int, default=0)
    dcp_fiber_entanglement.add_argument("--depth-fraction", type=float, default=0.5)
    dcp_fiber_entanglement.add_argument("--no-registry", action="store_true")
    dcp_fiber_entanglement.add_argument("--verbose", action="store_true")
    dcp_fiber_entanglement.set_defaults(func=command_dcp_fiber_entanglement)


def command_dcp_fiber_entanglement(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_fiber_entanglement_audit
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    finite_n_values = [
        int(value.strip()) for value in args.finite_n_values.split(",") if value.strip()
    ]
    payload = write_fiber_entanglement_audit(
        n_values=n_values,
        finite_n_values=finite_n_values,
        register_offset=args.register_offset,
        finite_trials=args.finite_trials,
        seed=args.seed,
        depth_fraction=args.depth_fraction,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum fiber entanglement audit complete")
    print("Artifact: research/phase_workbench/dcp_fiber_entanglement.json")
    print(
        "Exact spectrum / random exponential-rank theorems: "
        f"{metrics['exact_schmidt_decomposition_theorem_count']}/"
        f"{metrics['constant_fraction_exponential_rank_theorem_count']}"
    )
    print(
        "Minimum certified hard-instance probability: "
        f"{metrics['minimum_certified_hard_instance_probability']:.6g}"
    )
    print(
        "Approximate-bond / general-circuit no-go theorems: "
        f"{metrics['approximate_polynomial_bond_asymptotic_no_go_theorem_count']}/"
        f"{metrics['general_quantum_circuit_lower_bound_count']}"
    )
    print(f"Polynomial fiber-state preparations: {metrics['polynomial_fiber_state_preparation_count']}")
    print(f"Polynomial relation solvers: {metrics['polynomial_relation_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for row in payload["finite_rows"]:
            print(
                f"- n={row['n_bits']} q={row['modulus_bits']} rank=2^{row['log2_exact_schmidt_rank']:.3f} "
                f"S/q={row['normalized_entanglement_entropy']:.3f} "
                f"rank99={row['rank_for_99_percent_fidelity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_adaptive_layouts(subparsers) -> None:
    dcp_adaptive_layouts = subparsers.add_parser(
        "dcp-adaptive-layouts",
        help="Audit label-adaptive balanced tensor layouts and valuation compression.",
    )
    dcp_adaptive_layouts.add_argument("--n-values", default="8,10,12,16,20,24,28")
    dcp_adaptive_layouts.add_argument("--register-offset", type=int, default=4)
    dcp_adaptive_layouts.add_argument("--trials-per-size", type=int, default=1)
    dcp_adaptive_layouts.add_argument("--proposal-budget", type=int, default=24)
    dcp_adaptive_layouts.add_argument("--exhaustive-max-registers", type=int, default=16)
    dcp_adaptive_layouts.add_argument("--seed", type=int, default=0)
    dcp_adaptive_layouts.add_argument("--no-registry", action="store_true")
    dcp_adaptive_layouts.add_argument("--verbose", action="store_true")
    dcp_adaptive_layouts.set_defaults(func=command_dcp_adaptive_layouts)


def command_dcp_adaptive_layouts(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_adaptive_layout_audit
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_adaptive_layout_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        trials_per_size=args.trials_per_size,
        proposal_budget=args.proposal_budget,
        exhaustive_max_registers=args.exhaustive_max_registers,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP label-adaptive fiber layout audit complete")
    print("Artifact: research/phase_workbench/dcp_adaptive_layout_audit.json")
    print(
        "Adaptive valuation no-go theorems: "
        f"{metrics['adaptive_valuation_compression_no_go_theorem_count']}"
    )
    print(f"Exact balanced optimum rows: {metrics['exact_balanced_optimum_row_count']}")
    print(f"Evaluated layouts: {metrics['evaluated_layout_count']}")
    print(f"Maximum finite improvement bits: {metrics['maximum_adaptive_improvement_bits']:.6g}")
    print(
        "Tail best log-rank slope per n: "
        f"{metrics['fitted_tail_best_log2_rank_slope_per_n']:.6g}"
    )
    print(
        "Polynomial selector/contractions and relation solvers: "
        f"{metrics['polynomial_selector_and_contraction_count']}/"
        f"{metrics['polynomial_relation_solver_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for row in payload["finite_rows"]:
            best = row["exact_optimal_layout"] or row["best_adaptive_layout"]
            print(
                f"- n={row['n_bits']} q={row['modulus_bits']} layouts={row['evaluated_layout_count']} "
                f"natural/best log2 rank99={row['natural_layout']['log2_rank_for_99_percent_schmidt_mass']:.3f}/"
                f"{best['log2_rank_for_99_percent_schmidt_mass']:.3f} exhaustive={row['exhaustive_balanced_search']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_subset_sum_randomize(subparsers) -> None:
    dcp_subset_sum_randomize = subparsers.add_parser(
        "dcp-subset-sum-randomize",
        help="Audit signed and odd-unit source-preserving random self-reductions for density-one subset sum.",
    )
    dcp_subset_sum_randomize.add_argument("--n-values", default="20,24,28,32")
    dcp_subset_sum_randomize.add_argument("--register-offsets", default="4")
    dcp_subset_sum_randomize.add_argument("--attempt-multiplier", type=int, default=1)
    dcp_subset_sum_randomize.add_argument("--trials-per-row", type=int, default=4)
    dcp_subset_sum_randomize.add_argument("--seed", type=int, default=0)
    dcp_subset_sum_randomize.add_argument("--embedding-scale", type=int, default=4)
    dcp_subset_sum_randomize.add_argument("--lll-delta", type=float, default=0.75)
    dcp_subset_sum_randomize.add_argument("--combination-arity", type=int, choices=[1, 2], default=1)
    dcp_subset_sum_randomize.add_argument("--exact-legality-max-bits", type=int, default=20)
    dcp_subset_sum_randomize.add_argument(
        "--classes", default="sign-only,odd-unit,signed-odd-unit"
    )
    dcp_subset_sum_randomize.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_randomize.set_defaults(func=command_dcp_subset_sum_randomize)


def command_dcp_subset_sum_randomize(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_random_self_reduction_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    register_offsets = [
        int(value.strip()) for value in args.register_offsets.split(",") if value.strip()
    ]
    payload = write_random_self_reduction_audit(
        n_values=n_values,
        register_offsets=register_offsets,
        attempt_multiplier=args.attempt_multiplier,
        trials_per_row=args.trials_per_row,
        seed=args.seed,
        embedding_scale=args.embedding_scale,
        lll_delta=args.lll_delta,
        combination_arity=args.combination_arity,
        exact_legality_max_bits=args.exact_legality_max_bits,
        enabled_classes=[
            value.strip() for value in args.classes.split(",") if value.strip()
        ],
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP subset-sum random self-reduction audit complete")
    print("Artifact: research/reductions/dcp_subset_sum_random_self_reduction.json")
    print(
        "Source-bijection certificates: "
        f"{metrics['source_distribution_bijection_certificate_count']}/"
        f"{metrics['algebra_certificate_count']}"
    )
    print(f"Signed embedding isometries: {metrics['signed_embedding_isometry_certificate_count']}")
    print(
        "Legal direct/sign/unit/signed-unit successes: "
        f"{metrics['direct_legal_success_count']}/{metrics['sign_only_legal_success_count']}/"
        f"{metrics['odd_unit_legal_success_count']}/{metrics['signed_odd_unit_legal_success_count']}"
    )
    print(
        "Odd-unit/signed-unit rescues: "
        f"{metrics['odd_unit_rescue_count']}/{metrics['signed_odd_unit_rescue_count']}"
    )
    print(
        "Tail unconditional direct/sign/unit/signed-unit successes: "
        f"{metrics['tail_direct_unconditional_success_count']}/"
        f"{metrics['tail_sign_only_unconditional_success_count']}/"
        f"{metrics['tail_odd_unit_unconditional_success_count']}/"
        f"{metrics['tail_signed_odd_unit_unconditional_success_count']} of "
        f"{metrics['tail_trial_count']}"
    )
    print(
        "Uniform inverse-polynomial coverage proofs: "
        f"{metrics['proved_uniform_inverse_polynomial_legal_coverage_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_odd_unit_geometry(subparsers) -> None:
    dcp_odd_unit_geometry = subparsers.add_parser(
        "dcp-odd-unit-geometry",
        help="Learn held-out geometric predictors over exact odd-unit subset-sum orbits.",
    )
    dcp_odd_unit_geometry.add_argument("--n-values", default="20,24,28,32")
    dcp_odd_unit_geometry.add_argument("--register-offset", type=int, default=4)
    dcp_odd_unit_geometry.add_argument("--base-instances-per-size", type=int, default=4)
    dcp_odd_unit_geometry.add_argument("--units-multiplier", type=int, default=2)
    dcp_odd_unit_geometry.add_argument("--seed", type=int, default=0)
    dcp_odd_unit_geometry.add_argument("--embedding-scale", type=int, default=4)
    dcp_odd_unit_geometry.add_argument("--lll-delta", type=float, default=0.75)
    dcp_odd_unit_geometry.add_argument("--combination-arity", type=int, choices=[1, 2], default=1)
    dcp_odd_unit_geometry.add_argument("--no-registry", action="store_true")
    dcp_odd_unit_geometry.set_defaults(func=command_dcp_odd_unit_geometry)


def command_dcp_odd_unit_geometry(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_odd_unit_orbit_geometry_audit,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_odd_unit_orbit_geometry_audit(
        n_values=n_values,
        register_offset=args.register_offset,
        base_instances_per_size=args.base_instances_per_size,
        units_multiplier=args.units_multiplier,
        seed=args.seed,
        embedding_scale=args.embedding_scale,
        lll_delta=args.lll_delta,
        combination_arity=args.combination_arity,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP odd-unit orbit geometry audit complete")
    print("Artifact: research/classical_baselines/dcp_odd_unit_orbit_geometry.json")
    print(
        "Full 2-adic invariant certificates: "
        f"{metrics['full_two_adic_invariant_certificate_count']}/"
        f"{metrics['invariant_certificate_count']}"
    )
    print(f"Odd-unit presentations: {metrics['geometry_record_count']}")
    print(f"Verified witnesses: {metrics['verified_witness_count']}")
    print(
        "Tail verified witnesses: "
        f"{metrics['tail_verified_witness_count']}/{metrics['tail_record_count']}"
    )
    print(
        "Held-out positive pre-reduction rules: "
        f"{metrics['heldout_positive_pre_reduction_rule_count']}"
    )
    print(
        "Easy-orbit measure proofs: "
        f"{metrics['proved_inverse_polynomial_easy_orbit_measure_count']}"
    )
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_likelihood_search(subparsers) -> None:
    dcp_likelihood = subparsers.add_parser(
        "dcp-likelihood-search",
        help="Run exact nonlinear interval branch-and-bound on random-label DCP likelihoods and fit candidate scaling.",
    )
    dcp_likelihood.add_argument("--n-values", default="8,10,12,14,16")
    dcp_likelihood.add_argument("--sample-multiplier", type=float, default=12.0)
    dcp_likelihood.add_argument("--trials-per-size", type=int, default=4)
    dcp_likelihood.add_argument("--seed", type=int, default=0)
    dcp_likelihood.add_argument("--no-registry", action="store_true")
    dcp_likelihood.set_defaults(func=command_dcp_likelihood_search)


def command_dcp_likelihood_search(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_likelihood_branch_bound_report,
    )
    initialize_seed_registry(overwrite=False)
    n_values = [int(value.strip()) for value in args.n_values.split(",") if value.strip()]
    payload = write_likelihood_branch_bound_report(
        n_values=n_values,
        sample_multiplier=args.sample_multiplier,
        trials_per_size=args.trials_per_size,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("DCP exact likelihood branch-and-bound baseline complete")
    print("Artifact: research/classical_baselines/dcp_likelihood_branch_bound.json")
    print(f"Trials: {metrics['trial_count']}")
    print(f"Exact recoveries: {metrics['exact_decode_success_count']}")
    print(f"Mean candidate-score fraction: {metrics['mean_score_evaluation_fraction']}")
    print(f"Fitted log2 evaluation slope: {metrics['fitted_log2_evaluation_slope_per_n']}")
    print(f"Polynomial branch-bound proofs: {metrics['proved_polynomial_branch_bound_count']}")
    print(f"General nonlinear lower bounds: {metrics['proved_nonlinear_decoder_lower_bound_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_dcp_adaptive_layout_uniform_entanglement_no_go(subparsers) -> None:
    dcp_adaptive_layout_uniform_entanglement_no_go = subparsers.add_parser(
        "dcp-adaptive-layout-uniform-entanglement-no-go",
        help="Exp Dhs Dcp Adaptive Layout Uniform Entanglement No Go",
    )
    dcp_adaptive_layout_uniform_entanglement_no_go.set_defaults(func=command_dcp_adaptive_layout_uniform_entanglement_no_go)


def command_dcp_adaptive_layout_uniform_entanglement_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_dcp_adaptive_layout_uniform_entanglement_report
    report = write_dcp_adaptive_layout_uniform_entanglement_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_label_digest_audit(subparsers) -> None:
    dcp_label_digest_audit = subparsers.add_parser(
        "dcp-label-digest-audit",
        help="Check physical DCP label loss, joint-slice bounds and analytic scaling",
    )
    dcp_label_digest_audit.set_defaults(func=command_dcp_label_digest_audit)


def command_dcp_label_digest_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_digest_audit_report
    initialize_seed_registry(overwrite=False)
    report = write_digest_audit_report()
    print(report["summary"])
    print(json.dumps(report["headline_metrics"], indent=2))
    valid = validate_registry()["valid"]
    print(f"Registry valid: {valid}")
    return 0 if valid and report["claim_gate"]["finite_controls_passed"] is True else 1


def add_dcp_arbitrary_measurement_witness_reduction(subparsers) -> None:
    dcp_arbitrary_measurement_witness_reduction = subparsers.add_parser(
        "dcp-arbitrary-measurement-witness-reduction",
        help="Exp Dhs Dcp Arbitrary Measurement Witness Reduction",
    )
    dcp_arbitrary_measurement_witness_reduction.set_defaults(func=command_dcp_arbitrary_measurement_witness_reduction)


def command_dcp_arbitrary_measurement_witness_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_arbitrary_measurement_witness_reduction_report
    report = write_arbitrary_measurement_witness_reduction_report()
    print(report["summary"])
    print(f"Status: {report.get('status')}")
    print(json.dumps(report["headline_metrics"], indent=2))
    valid = validate_registry()["valid"]
    print(f"Registry valid: {valid}")
    return 0 if valid and report["claim_gate"]["unamplified_label_average_success_transfer_derived"] is True else 1


def add_dcp_canonical_pgm_erasure_equivalence(subparsers) -> None:
    dcp_canonical_pgm_erasure_equivalence = subparsers.add_parser(
        "dcp-canonical-pgm-erasure-equivalence",
        help="Exp Dhs Dcp Canonical Pgm Erasure Equivalence",
    )
    dcp_canonical_pgm_erasure_equivalence.set_defaults(func=command_dcp_canonical_pgm_erasure_equivalence)


def command_dcp_canonical_pgm_erasure_equivalence(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_canonical_pgm_erasure_equivalence
    report = write_canonical_pgm_erasure_equivalence()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_covariant_rank_one_measurement_reduction(subparsers) -> None:
    dcp_covariant_rank_one_measurement_reduction = subparsers.add_parser(
        "dcp-covariant-rank-one-measurement-reduction",
        help="Exp Dhs Dcp Covariant Rank One Measurement Reduction",
    )
    dcp_covariant_rank_one_measurement_reduction.set_defaults(func=command_dcp_covariant_rank_one_measurement_reduction)


def command_dcp_covariant_rank_one_measurement_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_covariant_rank_one_measurement_reduction_report
    report = write_covariant_rank_one_measurement_reduction_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_four_block_ksum_noncollapse(subparsers) -> None:
    dcp_four_block_ksum_noncollapse = subparsers.add_parser(
        "dcp-four-block-ksum-noncollapse",
        help="Exp Dhs Dcp Four Block Ksum Noncollapse",
    )
    dcp_four_block_ksum_noncollapse.set_defaults(func=command_dcp_four_block_ksum_noncollapse)


def command_dcp_four_block_ksum_noncollapse(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_four_block_ksum_noncollapse
    report = write_four_block_ksum_noncollapse()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_linear_depth_fiber_walk_no_go(subparsers) -> None:
    dcp_linear_depth_fiber_walk_no_go = subparsers.add_parser(
        "dcp-linear-depth-fiber-walk-no-go",
        help="Exp Dhs Dcp Linear Depth Fiber Walk No Go",
    )
    dcp_linear_depth_fiber_walk_no_go.set_defaults(func=command_dcp_linear_depth_fiber_walk_no_go)


def command_dcp_linear_depth_fiber_walk_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_linear_depth_fiber_walk_no_go
    report = write_linear_depth_fiber_walk_no_go()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_low_bit_candidate_list_no_go(subparsers) -> None:
    dcp_low_bit_candidate_list_no_go = subparsers.add_parser(
        "dcp-low-bit-candidate-list-no-go",
        help="Exp Dhs Dcp Low Bit Candidate List No Go",
    )
    dcp_low_bit_candidate_list_no_go.set_defaults(func=command_dcp_low_bit_candidate_list_no_go)


def command_dcp_low_bit_candidate_list_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_low_bit_candidate_list_no_go_report
    report = write_low_bit_candidate_list_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_multiplicity_oracle_query_lower_bound(subparsers) -> None:
    dcp_multiplicity_oracle_query_lower_bound = subparsers.add_parser(
        "dcp-multiplicity-oracle-query-lower-bound",
        help="Exp Dhs Dcp Multiplicity Oracle Query Lower Bound",
    )
    dcp_multiplicity_oracle_query_lower_bound.set_defaults(func=command_dcp_multiplicity_oracle_query_lower_bound)


def command_dcp_multiplicity_oracle_query_lower_bound(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_multiplicity_oracle_query_lower_bound
    report = write_multiplicity_oracle_query_lower_bound()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_per_target_stratum_obstruction(subparsers) -> None:
    dcp_per_target_stratum_obstruction = subparsers.add_parser(
        "dcp-per-target-stratum-obstruction",
        help="Exp Dhs Dcp Per Target Stratum Obstruction",
    )
    dcp_per_target_stratum_obstruction.set_defaults(func=command_dcp_per_target_stratum_obstruction)


def command_dcp_per_target_stratum_obstruction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_per_target_stratum_obstruction
    report = write_per_target_stratum_obstruction()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_pgm_bootstrap_perturbation_reduction(subparsers) -> None:
    dcp_pgm_bootstrap_perturbation_reduction = subparsers.add_parser(
        "dcp-pgm-bootstrap-perturbation-reduction",
        help="Exp Dhs Dcp Pgm Bootstrap Perturbation Reduction",
    )
    dcp_pgm_bootstrap_perturbation_reduction.set_defaults(func=command_dcp_pgm_bootstrap_perturbation_reduction)


def command_dcp_pgm_bootstrap_perturbation_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_pgm_bootstrap_perturbation_reduction
    report = write_pgm_bootstrap_perturbation_reduction()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_pgm_garbage_bootstrap_reduction(subparsers) -> None:
    dcp_pgm_garbage_bootstrap_reduction = subparsers.add_parser(
        "dcp-pgm-garbage-bootstrap-reduction",
        help="Exp Dhs Dcp Pgm Garbage Bootstrap Reduction",
    )
    dcp_pgm_garbage_bootstrap_reduction.set_defaults(func=command_dcp_pgm_garbage_bootstrap_reduction)


def command_dcp_pgm_garbage_bootstrap_reduction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_pgm_garbage_bootstrap_reduction
    report = write_pgm_garbage_bootstrap_reduction()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_polynomial_feature_contraction_no_go(subparsers) -> None:
    dcp_polynomial_feature_contraction_no_go = subparsers.add_parser(
        "dcp-polynomial-feature-contraction-no-go",
        help="Exp Dhs Dcp Polynomial Feature Contraction No Go",
    )
    dcp_polynomial_feature_contraction_no_go.set_defaults(func=command_dcp_polynomial_feature_contraction_no_go)


def command_dcp_polynomial_feature_contraction_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_polynomial_feature_contraction_no_go
    report = write_polynomial_feature_contraction_no_go()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_source_weighted_inversion_tradeoff(subparsers) -> None:
    dcp_source_weighted_inversion_tradeoff = subparsers.add_parser(
        "dcp-source-weighted-inversion-tradeoff",
        help="Exp Dhs Dcp Source Weighted Inversion Tradeoff",
    )
    dcp_source_weighted_inversion_tradeoff.set_defaults(func=command_dcp_source_weighted_inversion_tradeoff)


def command_dcp_source_weighted_inversion_tradeoff(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_dcp_source_weighted_inversion_tradeoff
    report = write_dcp_source_weighted_inversion_tradeoff()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_subset_sum_cube_section_gap_theorem(subparsers) -> None:
    dcp_subset_sum_cube_section_gap_theorem = subparsers.add_parser(
        "dcp-subset-sum-cube-section-gap-theorem",
        help="Exp Dhs Dcp Subset Sum Cube Section Gap Theorem",
    )
    dcp_subset_sum_cube_section_gap_theorem.set_defaults(func=command_dcp_subset_sum_cube_section_gap_theorem)


def command_dcp_subset_sum_cube_section_gap_theorem(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_cube_section_gap_theorem
    report = write_cube_section_gap_theorem()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_subset_sum_sparse_character_obstruction(subparsers) -> None:
    dcp_subset_sum_sparse_character_obstruction = subparsers.add_parser(
        "dcp-subset-sum-sparse-character-obstruction",
        help="Exp Dhs Dcp Subset Sum Adaptive Sparse Character Obstruction",
    )
    dcp_subset_sum_sparse_character_obstruction.set_defaults(func=command_dcp_subset_sum_sparse_character_obstruction)


def command_dcp_subset_sum_sparse_character_obstruction(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_sparse_character_obstruction
    report = write_sparse_character_obstruction()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_uniform_legal_multiplicity_no_go(subparsers) -> None:
    dcp_uniform_legal_multiplicity_no_go = subparsers.add_parser(
        "dcp-uniform-legal-multiplicity-no-go",
        help="Exp Dhs Dcp Uniform Legal Multiplicity No Go",
    )
    dcp_uniform_legal_multiplicity_no_go.set_defaults(func=command_dcp_uniform_legal_multiplicity_no_go)


def command_dcp_uniform_legal_multiplicity_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_uniform_legal_multiplicity_no_go_report
    report = write_uniform_legal_multiplicity_no_go_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_varying_hms_fiber_normal_form(subparsers) -> None:
    dcp_varying_hms_fiber_normal_form = subparsers.add_parser(
        "dcp-varying-hms-fiber-normal-form",
        help="Exp Dhs Dcp Varying Hms Fiber Normal Form",
    )
    dcp_varying_hms_fiber_normal_form.set_defaults(func=command_dcp_varying_hms_fiber_normal_form)


def command_dcp_varying_hms_fiber_normal_form(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_dcp_varying_hms_fiber_normal_form
    report = write_dcp_varying_hms_fiber_normal_form()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_cnot_linear_split_entanglement_no_go(subparsers) -> None:
    dcp_cnot_linear_split_entanglement_no_go = subparsers.add_parser(
        "dcp-cnot-linear-split-entanglement-no-go",
        help="Exp Dhs Dcp Cnot Linear Split Entanglement No Go",
    )
    dcp_cnot_linear_split_entanglement_no_go.set_defaults(func=command_dcp_cnot_linear_split_entanglement_no_go)


def command_dcp_cnot_linear_split_entanglement_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_cnot_linear_split_entanglement_report
    report = write_cnot_linear_split_entanglement_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_linear_reparameterization_affine_flat_no_go(subparsers) -> None:
    dcp_linear_reparameterization_affine_flat_no_go = subparsers.add_parser(
        "dcp-linear-reparameterization-affine-flat-no-go",
        help="Exp Dhs Dcp Linear Reparameterization Affine Flat No Go",
    )
    dcp_linear_reparameterization_affine_flat_no_go.set_defaults(func=command_dcp_linear_reparameterization_affine_flat_no_go)


def command_dcp_linear_reparameterization_affine_flat_no_go(args: argparse.Namespace) -> int:
    from qsearch import validate_registry, write_linear_reparameterization_affine_flat_report
    report = write_linear_reparameterization_affine_flat_report()
    print(f"Analysis complete: {args.command}")
    print(f"Status: {report.get('status')}")
    print(f"Registry valid: {validate_registry()['valid']}")
    return 0


def add_dcp_noisy_fourier_likelihood_decoder_audit(subparsers) -> None:
    dcp_noisy_fourier_likelihood_decoder_audit = subparsers.add_parser(
        "dcp-noisy-fourier-likelihood-decoder-audit",
        help="Audit CNOT tree-merge visibility multiplication and {X, Y} quadrature Fourier/log-likelihood decoding on OpaquePhaseBackend.",
    )
    dcp_noisy_fourier_likelihood_decoder_audit.add_argument("--no-write", action="store_true")
    dcp_noisy_fourier_likelihood_decoder_audit.set_defaults(func=command_dcp_noisy_fourier_likelihood_decoder_audit)


def command_dcp_noisy_fourier_likelihood_decoder_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_noisy_fourier_likelihood_decoder_audit import (
        build_dcp_noisy_fourier_likelihood_decoder_audit_report,
        write_dcp_noisy_fourier_likelihood_decoder_audit_report,
    )

    payload = (
        build_dcp_noisy_fourier_likelihood_decoder_audit_report()
        if args.no_write
        else write_dcp_noisy_fourier_likelihood_decoder_audit_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_adaptive_quadrature_tree_sieve_audit(subparsers) -> None:
    dcp_adaptive_quadrature_tree_sieve_audit = subparsers.add_parser(
        "dcp-adaptive-quadrature-tree-sieve-audit",
        help="Audit bitwise dyadic quadrature demodulation, equal-valuation CNOT pairing dichotomy, and sieve-depth visibility thresholds.",
    )
    dcp_adaptive_quadrature_tree_sieve_audit.add_argument("--no-write", action="store_true")
    dcp_adaptive_quadrature_tree_sieve_audit.set_defaults(func=command_dcp_adaptive_quadrature_tree_sieve_audit)


def command_dcp_adaptive_quadrature_tree_sieve_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_adaptive_quadrature_tree_sieve_audit import (
        build_dcp_adaptive_quadrature_tree_sieve_audit_report,
        write_dcp_adaptive_quadrature_tree_sieve_audit_report,
    )

    payload = (
        build_dcp_adaptive_quadrature_tree_sieve_audit_report()
        if args.no_write
        else write_dcp_adaptive_quadrature_tree_sieve_audit_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_truncated_qft_tree_merge_joint_channel_audit(subparsers) -> None:
    dcp_truncated_qft_tree_merge_joint_channel_audit = subparsers.add_parser(
        "dcp-truncated-qft-tree-merge-joint-channel-audit",
        help="Audit truncated-QFT CNOT tree-merge additive phase-defect propagation, branch-symmetry sine cancellation, and depth-d visibility factorization.",
    )
    dcp_truncated_qft_tree_merge_joint_channel_audit.add_argument("--no-write", action="store_true")
    dcp_truncated_qft_tree_merge_joint_channel_audit.set_defaults(func=command_dcp_truncated_qft_tree_merge_joint_channel_audit)


def command_dcp_truncated_qft_tree_merge_joint_channel_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_truncated_qft_tree_merge_joint_channel_audit import (
        build_dcp_truncated_qft_tree_merge_joint_channel_audit_report,
        write_dcp_truncated_qft_tree_merge_joint_channel_audit_report,
    )

    payload = (
        build_dcp_truncated_qft_tree_merge_joint_channel_audit_report()
        if args.no_write
        else write_dcp_truncated_qft_tree_merge_joint_channel_audit_report()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_noisy_tree_merge_error_propagation_audit(subparsers) -> None:
    dcp_noisy_tree_merge_error_propagation_audit = subparsers.add_parser(
        "dcp-noisy-tree-merge-error-propagation-audit",
        help="Audit DCP noisy tree-merge 2^L-fold phase-error convolution, double-exponential visibility decay, and classical-vs-tree SNR crossover.",
    )
    dcp_noisy_tree_merge_error_propagation_audit.add_argument("--no-write", action="store_true")
    dcp_noisy_tree_merge_error_propagation_audit.set_defaults(func=command_dcp_noisy_tree_merge_error_propagation_audit)


def command_dcp_noisy_tree_merge_error_propagation_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_noisy_tree_merge_error_propagation_audit import (
        build_dcp_noisy_tree_merge_error_propagation_audit,
        write_dcp_noisy_tree_merge_error_propagation_audit,
    )

    payload = (
        build_dcp_noisy_tree_merge_error_propagation_audit()
        if args.no_write
        else write_dcp_noisy_tree_merge_error_propagation_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_pgm_fidelity_window_threshold_audit(subparsers) -> None:
    dcp_pgm_fidelity_window_threshold_audit = subparsers.add_parser(
        "dcp-pgm-fidelity-window-threshold-audit",
        help="Audit DCP K-copy covariant PGM Bhattacharyya convolution formula, flat-window optimality, and contiguous support copy lower bounds.",
    )
    dcp_pgm_fidelity_window_threshold_audit.add_argument("--no-write", action="store_true")
    dcp_pgm_fidelity_window_threshold_audit.set_defaults(func=command_dcp_pgm_fidelity_window_threshold_audit)


def command_dcp_pgm_fidelity_window_threshold_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_pgm_fidelity_window_threshold_audit import (
        build_dcp_pgm_fidelity_window_threshold_audit,
        write_dcp_pgm_fidelity_window_threshold_audit,
    )

    payload = (
        build_dcp_pgm_fidelity_window_threshold_audit()
        if args.no_write
        else write_dcp_pgm_fidelity_window_threshold_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_interleaved_tree_merge_syndrome_pruning_audit(subparsers) -> None:
    dcp_interleaved_tree_merge_syndrome_pruning_audit = subparsers.add_parser(
        "dcp-interleaved-tree-merge-syndrome-pruning-audit",
        help="Audit DCP interleaved tree-merge coincidence pruning, telescoping 2^L-moment survival law, p*=2/3 crossover, and SNR deficit.",
    )
    dcp_interleaved_tree_merge_syndrome_pruning_audit.add_argument("--no-write", action="store_true")
    dcp_interleaved_tree_merge_syndrome_pruning_audit.set_defaults(func=command_dcp_interleaved_tree_merge_syndrome_pruning_audit)


def command_dcp_interleaved_tree_merge_syndrome_pruning_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_interleaved_tree_merge_syndrome_pruning_audit import (
        build_dcp_interleaved_tree_merge_syndrome_pruning_audit,
        write_dcp_interleaved_tree_merge_syndrome_pruning_audit,
    )

    payload = (
        build_dcp_interleaved_tree_merge_syndrome_pruning_audit()
        if args.no_write
        else write_dcp_interleaved_tree_merge_syndrome_pruning_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_multi_harmonic_weighted_fisher_decoder_audit(subparsers) -> None:
    dcp_multi_harmonic_weighted_fisher_decoder_audit = subparsers.add_parser(
        "dcp-multi-harmonic-weighted-fisher-decoder-audit",
        help="Audit DCP multi-harmonic Parseval mean-square visibility law, zero-lag inversion identity, and matched-filter optimality.",
    )
    dcp_multi_harmonic_weighted_fisher_decoder_audit.add_argument("--no-write", action="store_true")
    dcp_multi_harmonic_weighted_fisher_decoder_audit.set_defaults(func=command_dcp_multi_harmonic_weighted_fisher_decoder_audit)


def command_dcp_multi_harmonic_weighted_fisher_decoder_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_multi_harmonic_weighted_fisher_decoder_audit import (
        build_dcp_multi_harmonic_weighted_fisher_decoder_audit,
        write_dcp_multi_harmonic_weighted_fisher_decoder_audit,
    )

    payload = (
        build_dcp_multi_harmonic_weighted_fisher_decoder_audit()
        if args.no_write
        else write_dcp_multi_harmonic_weighted_fisher_decoder_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_quadrature_conjugate_pair_holevo_audit(subparsers) -> None:
    dcp_quadrature_conjugate_pair_holevo_audit = subparsers.add_parser(
        "dcp-quadrature-conjugate-pair-holevo-audit",
        help="Audit DCP equatorial Bloch-disk Holevo capacity, randomized X/Y Fisher isotropization bounds, and singlet phase-independence.",
    )
    dcp_quadrature_conjugate_pair_holevo_audit.add_argument("--no-write", action="store_true")
    dcp_quadrature_conjugate_pair_holevo_audit.set_defaults(func=command_dcp_quadrature_conjugate_pair_holevo_audit)


def command_dcp_quadrature_conjugate_pair_holevo_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_quadrature_conjugate_pair_holevo_audit import (
        build_dcp_quadrature_conjugate_pair_holevo_audit,
        write_dcp_quadrature_conjugate_pair_holevo_audit,
    )

    payload = (
        build_dcp_quadrature_conjugate_pair_holevo_audit()
        if args.no_write
        else write_dcp_quadrature_conjugate_pair_holevo_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_two_copy_cnot_difference_alignment_audit(subparsers) -> None:
    dcp_two_copy_cnot_difference_alignment_audit = subparsers.add_parser(
        "dcp-two-copy-cnot-difference-alignment-audit",
        help="Audit DCP two-copy CNOT sum/difference branch bifurcation, diagonal/anti-diagonal phase annihilation, and off-diagonal visibility yield.",
    )
    dcp_two_copy_cnot_difference_alignment_audit.add_argument("--no-write", action="store_true")
    dcp_two_copy_cnot_difference_alignment_audit.set_defaults(func=command_dcp_two_copy_cnot_difference_alignment_audit)


def command_dcp_two_copy_cnot_difference_alignment_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_two_copy_cnot_difference_alignment_audit import (
        build_dcp_two_copy_cnot_difference_alignment_audit,
        write_dcp_two_copy_cnot_difference_alignment_audit,
    )

    payload = (
        build_dcp_two_copy_cnot_difference_alignment_audit()
        if args.no_write
        else write_dcp_two_copy_cnot_difference_alignment_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_subset_sum_modular_collision_entropy_audit(subparsers) -> None:
    dcp_subset_sum_modular_collision_entropy_audit = subparsers.add_parser(
        "dcp-subset-sum-modular-collision-entropy-audit",
        help="Audit DCP modular subset-sum cosine-product collision purity, universal Boolean-difference surjectivity, and ensemble collision law.",
    )
    dcp_subset_sum_modular_collision_entropy_audit.add_argument("--no-write", action="store_true")
    dcp_subset_sum_modular_collision_entropy_audit.set_defaults(func=command_dcp_subset_sum_modular_collision_entropy_audit)


def command_dcp_subset_sum_modular_collision_entropy_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_subset_sum_modular_collision_entropy_audit import (
        build_dcp_subset_sum_modular_collision_entropy_audit,
        write_dcp_subset_sum_modular_collision_entropy_audit,
    )

    payload = (
        build_dcp_subset_sum_modular_collision_entropy_audit()
        if args.no_write
        else write_dcp_subset_sum_modular_collision_entropy_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_cyclic_subgroup_quotient_aliasing_audit(subparsers) -> None:
    dcp_cyclic_subgroup_quotient_aliasing_audit = subparsers.add_parser(
        "dcp-cyclic-subgroup-quotient-aliasing-audit",
        help="Audit DCP g-fold secret-coset aliasing, Euler-Ramanujan divisor-stratum visibility sum, and folded-kernel Parseval purity.",
    )
    dcp_cyclic_subgroup_quotient_aliasing_audit.add_argument("--no-write", action="store_true")
    dcp_cyclic_subgroup_quotient_aliasing_audit.set_defaults(func=command_dcp_cyclic_subgroup_quotient_aliasing_audit)


def command_dcp_cyclic_subgroup_quotient_aliasing_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_cyclic_subgroup_quotient_aliasing_audit import (
        build_dcp_cyclic_subgroup_quotient_aliasing_audit,
        write_dcp_cyclic_subgroup_quotient_aliasing_audit,
    )

    payload = (
        build_dcp_cyclic_subgroup_quotient_aliasing_audit()
        if args.no_write
        else write_dcp_cyclic_subgroup_quotient_aliasing_audit()
    )
    print(json.dumps(payload, indent=2))
    return 0


def add_dcp_clean_linear_witness_carry_obstruction(subparsers) -> None:
    dcp_clean_linear_witness_carry_obstruction = subparsers.add_parser(
        "dcp-clean-linear-witness-carry-obstruction",
        help="Check scoped linear witness identities and conditioned-label parity; no general decay bound.",
    )
    dcp_clean_linear_witness_carry_obstruction.add_argument("--no-write", action="store_true")
    dcp_clean_linear_witness_carry_obstruction.set_defaults(func=command_dcp_clean_linear_witness_carry_obstruction)


def command_dcp_clean_linear_witness_carry_obstruction(args: argparse.Namespace) -> int:
    from theorems.dcp_clean_linear_witness_carry_obstruction import (
        build_dcp_clean_linear_witness_carry_obstruction_report,
        write_dcp_clean_linear_witness_carry_obstruction_report,
    )

    payload = (
        build_dcp_clean_linear_witness_carry_obstruction_report()
        if getattr(args, "no_write", False)
        else write_dcp_clean_linear_witness_carry_obstruction_report()
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], indent=2))
    return 0


def add_dcp_babai_lattice_rounding_witness_obstruction(subparsers) -> None:
    dcp_babai_lattice_rounding_witness_obstruction = subparsers.add_parser(
        "dcp-babai-lattice-rounding-witness-obstruction",
        help="Check exact coordinate-rounding coverage and no-overflow countercontrols, not a general no-go.",
    )
    dcp_babai_lattice_rounding_witness_obstruction.add_argument("--no-write", action="store_true")
    dcp_babai_lattice_rounding_witness_obstruction.set_defaults(func=command_dcp_babai_lattice_rounding_witness_obstruction)


def command_dcp_babai_lattice_rounding_witness_obstruction(args: argparse.Namespace) -> int:
    from theorems.dcp_babai_lattice_rounding_witness_obstruction import (
        build_dcp_babai_lattice_rounding_witness_obstruction_report,
        write_dcp_babai_lattice_rounding_witness_obstruction_report,
    )

    payload = (
        build_dcp_babai_lattice_rounding_witness_obstruction_report()
        if getattr(args, "no_write", False)
        else write_dcp_babai_lattice_rounding_witness_obstruction_report()
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], indent=2))
    return 0


def add_dcp_product_sine_source_coordinate_marginal_obstruction(subparsers) -> None:
    dcp_product_sine_source_coordinate_marginal_obstruction = subparsers.add_parser(
        "dcp-product-sine-source-coordinate-marginal-obstruction",
        help="Run the product-group sine-window coordinate-marginal obstruction audit.",
    )
    dcp_product_sine_source_coordinate_marginal_obstruction.add_argument("--no-write", action="store_true")
    dcp_product_sine_source_coordinate_marginal_obstruction.set_defaults(func=command_dcp_product_sine_source_coordinate_marginal_obstruction)


def command_dcp_product_sine_source_coordinate_marginal_obstruction(args: argparse.Namespace) -> int:
    from theorems.dcp_product_sine_source_coordinate_marginal_obstruction import (
        build_dcp_product_sine_source_coordinate_marginal_obstruction_report,
        write_dcp_product_sine_source_coordinate_marginal_obstruction_report,
    )

    payload = (
        build_dcp_product_sine_source_coordinate_marginal_obstruction_report()
        if getattr(args, "no_write", False)
        else write_dcp_product_sine_source_coordinate_marginal_obstruction_report()
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], indent=2))
    return 0


def add_dcp_poly_pool_cnot_collimation_branching_obstruction(subparsers) -> None:
    dcp_poly_pool_cnot_collimation_branching_obstruction = subparsers.add_parser(
        "dcp-poly-pool-cnot-collimation-branching-obstruction",
        help="Run the clean DCP polynomial-pool CNOT collimation branching obstruction audit.",
    )
    dcp_poly_pool_cnot_collimation_branching_obstruction.add_argument("--no-write", action="store_true")
    dcp_poly_pool_cnot_collimation_branching_obstruction.set_defaults(func=command_dcp_poly_pool_cnot_collimation_branching_obstruction)


def command_dcp_poly_pool_cnot_collimation_branching_obstruction(args: argparse.Namespace) -> int:
    from theorems.dcp_poly_pool_cnot_collimation_branching_obstruction import (
        build_dcp_poly_pool_cnot_collimation_branching_obstruction_report,
        write_dcp_poly_pool_cnot_collimation_branching_obstruction_report,
    )

    payload = (
        build_dcp_poly_pool_cnot_collimation_branching_obstruction_report()
        if getattr(args, "no_write", False)
        else write_dcp_poly_pool_cnot_collimation_branching_obstruction_report()
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], indent=2))
    return 0


def add_dcp_sine_window_public_basis_lll_dominance_bridge(subparsers) -> None:
    dcp_sine_window_public_basis_lll_dominance_bridge = subparsers.add_parser(
        "dcp-sine-window-public-basis-lll-dominance-bridge",
        help="Run the sine-window clean-budget source vs classical LLL dominance bridge audit.",
    )
    dcp_sine_window_public_basis_lll_dominance_bridge.add_argument("--no-write", action="store_true")
    dcp_sine_window_public_basis_lll_dominance_bridge.set_defaults(func=command_dcp_sine_window_public_basis_lll_dominance_bridge)


def command_dcp_sine_window_public_basis_lll_dominance_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_sine_window_public_basis_lll_dominance_bridge import (
        build_dcp_sine_window_public_basis_lll_dominance_bridge_report,
        write_dcp_sine_window_public_basis_lll_dominance_bridge_report,
    )

    payload = (
        build_dcp_sine_window_public_basis_lll_dominance_bridge_report()
        if getattr(args, "no_write", False)
        else write_dcp_sine_window_public_basis_lll_dominance_bridge_report()
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], indent=2))
    return 0


def add_dcp_iqp_bounded_degree_carry_orthogonality_obstruction(subparsers) -> None:
    dcp_iqp_bounded_degree_carry_orthogonality_obstruction = subparsers.add_parser(
        "dcp-iqp-bounded-degree-carry-orthogonality-obstruction",
        help="Run the clean/noisy DCP IQP bounded-degree carry-orthogonality obstruction audit.",
    )
    dcp_iqp_bounded_degree_carry_orthogonality_obstruction.add_argument("--no-write", action="store_true")
    dcp_iqp_bounded_degree_carry_orthogonality_obstruction.set_defaults(func=command_dcp_iqp_bounded_degree_carry_orthogonality_obstruction)


def command_dcp_iqp_bounded_degree_carry_orthogonality_obstruction(args: argparse.Namespace) -> int:
    from theorems.dcp_iqp_bounded_degree_carry_orthogonality_obstruction import (
        build_dcp_iqp_bounded_degree_carry_orthogonality_obstruction_report,
        write_dcp_iqp_bounded_degree_carry_orthogonality_obstruction_report,
    )

    payload = (
        build_dcp_iqp_bounded_degree_carry_orthogonality_obstruction_report()
        if getattr(args, "no_write", False)
        else write_dcp_iqp_bounded_degree_carry_orthogonality_obstruction_report()
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], indent=2))
    return 0


def add_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction(subparsers) -> None:
    dcp_disjoint_tree_wire_capacity_tradeoff_obstruction = subparsers.add_parser(
        "dcp-disjoint-tree-wire-capacity-tradeoff-obstruction",
        help="Run the disjoint-block coherent 2^a-tree wire-capacity tradeoff obstruction audit.",
    )
    dcp_disjoint_tree_wire_capacity_tradeoff_obstruction.add_argument("--no-write", action="store_true")
    dcp_disjoint_tree_wire_capacity_tradeoff_obstruction.set_defaults(func=command_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction)


def command_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction(args: argparse.Namespace) -> int:
    from theorems.dcp_disjoint_tree_wire_capacity_tradeoff_obstruction import (
        build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report,
        write_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report,
    )

    payload = (
        build_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report()
        if getattr(args, "no_write", False)
        else write_dcp_disjoint_tree_wire_capacity_tradeoff_obstruction_report()
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], indent=2))
    return 0


def add_dcp_prefix_peeling_error_propagation_union_bridge(subparsers) -> None:
    dcp_prefix_peeling_error_propagation_union_bridge = subparsers.add_parser(
        "dcp-prefix-peeling-error-propagation-union-bridge",
        help="Run the clean DCP dyadic prefix-peeling error propagation and depolarization audit.",
    )
    dcp_prefix_peeling_error_propagation_union_bridge.add_argument("--no-write", action="store_true")
    dcp_prefix_peeling_error_propagation_union_bridge.set_defaults(func=command_dcp_prefix_peeling_error_propagation_union_bridge)


def command_dcp_prefix_peeling_error_propagation_union_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_prefix_peeling_error_propagation_union_bridge import (
        build_dcp_prefix_peeling_error_propagation_union_bridge_report,
        write_dcp_prefix_peeling_error_propagation_union_bridge_report,
    )

    payload = (
        build_dcp_prefix_peeling_error_propagation_union_bridge_report()
        if getattr(args, "no_write", False)
        else write_dcp_prefix_peeling_error_propagation_union_bridge_report()
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], indent=2))
    return 0


def add_dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge(subparsers) -> None:
    dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge = subparsers.add_parser(
        "dcp-grand-synthesis-50-subsystem-taxonomy-and-frontier-bridge",
        help="Run the DCP grand synthesis 50-subsystem taxonomy and unified 6-law frontier bridge certificate.",
    )
    dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge.set_defaults(func=command_dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge)


def command_dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge import (
        generate_dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_certificate,
    )
    cert = generate_dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_certificate()
    print(json.dumps(cert, indent=2, sort_keys=True))
    return 0


def add_dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge(subparsers) -> None:
    dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge = subparsers.add_parser(
        "dcp-non-stationary-markov-drift-secret-tracking-kalman-bridge",
        help="Run the DCP non-stationary drifting secret tracking via cross-packet CNOT velocity locking bridge certificate.",
    )
    dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge.set_defaults(func=command_dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge)


def command_dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge import (
        generate_dcp_non_stationary_markov_drift_secret_tracking_kalman_certificate,
    )
    cert = generate_dcp_non_stationary_markov_drift_secret_tracking_kalman_certificate()
    print(json.dumps(cert, indent=2, sort_keys=True))
    return 0


def add_dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge(subparsers) -> None:
    dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge = subparsers.add_parser(
        "dcp-quantum-z-error-detection-stabilizer-iceberg-code-bridge",
        help="Run the DCP quantum Z-error-detection [[2m+2, 2m, 2]] Iceberg stabilizer code bridge certificate.",
    )
    dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge.set_defaults(func=command_dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge)


def command_dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge import (
        generate_dcp_quantum_z_error_detection_stabilizer_iceberg_code_certificate,
    )
    cert = generate_dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge() if False else generate_dcp_quantum_z_error_detection_stabilizer_iceberg_code_certificate()
    print(json.dumps(cert, indent=2, sort_keys=True))
    return 0


def add_dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge(subparsers) -> None:
    dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge = subparsers.add_parser(
        "dcp-short-integer-solution-sis-dual-homomorphic-trapdoor-bridge",
        help="Run the DCP Short Integer Solution (SIS) dual gadget trapdoor binary witness compilation bridge certificate.",
    )
    dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge.set_defaults(func=command_dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge)


def command_dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge import (
        generate_dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_certificate,
    )
    cert = generate_dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_certificate()
    print(json.dumps(cert, indent=2, sort_keys=True))
    return 0


def add_dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge(subparsers) -> None:
    dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge = subparsers.add_parser(
        "dcp-haar-random-vs-dihedral-2-design-frame-potential-bridge",
        help="Run the DCP Haar-random vs dihedral 2-design frame potential and additive energy bridge certificate.",
    )
    dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge.set_defaults(func=command_dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge)


def command_dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge import (
        generate_dcp_haar_random_vs_dihedral_2_design_frame_potential_certificate,
    )
    cert = generate_dcp_haar_random_vs_dihedral_2_design_frame_potential_certificate()
    print(json.dumps(cert, indent=2, sort_keys=True))
    return 0


def add_dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge(subparsers) -> None:
    dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge = subparsers.add_parser(
        "dcp-kitaev-phase-estimation-hadamard-test-bit-by-bit-bridge",
        help="Run the DCP Kitaev bit-by-bit phase estimation vs coherent feedforward bridge certificate.",
    )
    dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge.set_defaults(func=command_dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge)


def command_dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge import (
        generate_dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_certificate,
    )
    cert = generate_dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_certificate()
    print(json.dumps(cert, indent=2, sort_keys=True))
    return 0


def add_dcp_multi_antenna_mimo_spatial_diversity_combining_bridge(subparsers) -> None:
    dcp_multi_antenna_mimo_spatial_diversity_combining_bridge = subparsers.add_parser(
        "dcp-multi-antenna-mimo-spatial-diversity-combining-bridge",
        help="Run the DCP multi-antenna MIMO spatial diversity combining bridge certificate.",
    )
    dcp_multi_antenna_mimo_spatial_diversity_combining_bridge.set_defaults(func=command_dcp_multi_antenna_mimo_spatial_diversity_combining_bridge)


def command_dcp_multi_antenna_mimo_spatial_diversity_combining_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_multi_antenna_mimo_spatial_diversity_combining_bridge import (
        generate_dcp_multi_antenna_mimo_spatial_diversity_combining_certificate,
    )
    cert = generate_dcp_multi_antenna_mimo_spatial_diversity_combining_certificate()
    print(json.dumps(cert, indent=2, sort_keys=True))
    return 0


def add_dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge(subparsers) -> None:
    dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge = subparsers.add_parser(
        "dcp-walsh-hadamard-gold-bent-nonlinear-carry-spectrum-bridge",
        help="Run the DCP Walsh-Hadamard Gold bent nonlinear carry spectrum bridge certificate.",
    )
    dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge.set_defaults(func=command_dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge)


def command_dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge(args: argparse.Namespace) -> int:
    from theorems.dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge import (
        generate_dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_certificate,
    )
    cert = generate_dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_certificate()
    print(json.dumps(cert, indent=2, sort_keys=True))
    return 0


def add_dcp_babai_deviation_depth_barrier(subparsers) -> None:
    dcp_babai_deviation_depth_barrier = subparsers.add_parser(
        "dcp-babai-deviation-depth-barrier",
        help="Run DCP density-one subset sum Babai deviation depth scaling and exponential list coverage collapse audit.",
    )
    dcp_babai_deviation_depth_barrier.add_argument("--no-registry", action="store_true")
    dcp_babai_deviation_depth_barrier.set_defaults(func=command_dcp_babai_deviation_depth_barrier)


def command_dcp_babai_deviation_depth_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.dcp_babai_deviation_depth_barrier import REPORT_PATH, write_report
    write_report(write_registry=not args.no_registry)
    validation = validate_registry()
    print("dcp_babai_deviation_depth_barrier complete")
    print(f"Artifact: {REPORT_PATH}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_dcp_two_adic_carry_fragmentation_barrier(subparsers) -> None:
    dcp_two_adic_carry_fragmentation_barrier = subparsers.add_parser(
        "dcp-two-adic-carry-fragmentation-barrier",
        help="Run 2-adic carry transfer recurrence, critical relation weight, and dictionary walk fragmentation barrier audit.",
    )
    dcp_two_adic_carry_fragmentation_barrier.add_argument("--no-registry", action="store_true")
    dcp_two_adic_carry_fragmentation_barrier.set_defaults(func=command_dcp_two_adic_carry_fragmentation_barrier)


def command_dcp_two_adic_carry_fragmentation_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.dcp_two_adic_carry_fragmentation_barrier import REPORT, write_report
    write_report(write_registry=not getattr(args, "no_registry", False))
    validation = validate_registry()
    print("dcp_two_adic_carry_fragmentation_barrier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_dcp_general_povm_secret_variance_collapse(subparsers) -> None:
    dcp_general_povm_secret_variance_collapse = subparsers.add_parser(
        "dcp-general-povm-secret-variance-collapse",
        help="Run general quantum POVM secret variance collapse, shallow-depth zero-information, and Fano reconstruction failure audit.",
    )
    dcp_general_povm_secret_variance_collapse.add_argument("--no-registry", action="store_true")
    dcp_general_povm_secret_variance_collapse.set_defaults(func=command_dcp_general_povm_secret_variance_collapse)


def command_dcp_general_povm_secret_variance_collapse(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.dcp_general_povm_secret_variance_collapse import REPORT, write_report
    write_report(write_registry=not getattr(args, "no_registry", False))
    validation = validate_registry()
    print("dcp_general_povm_secret_variance_collapse complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_dcp_subset_sum_euclidean_volume_inflation_barrier(subparsers) -> None:
    dcp_subset_sum_euclidean_volume_inflation_barrier = subparsers.add_parser(
        "dcp-subset-sum-euclidean-volume-inflation-barrier",
        help="Run density-one subset-sum Euclidean volume inflation and BDD multiplicity barrier audit.",
    )
    dcp_subset_sum_euclidean_volume_inflation_barrier.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_euclidean_volume_inflation_barrier.set_defaults(func=command_dcp_subset_sum_euclidean_volume_inflation_barrier)


def command_dcp_subset_sum_euclidean_volume_inflation_barrier(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    import json
    from theorems.dcp_subset_sum_euclidean_volume_inflation_barrier import REPORT, build_report, register_negative_result
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    if not getattr(args, "no_registry", False):
        register_negative_result()
    validation = validate_registry()
    print("dcp_subset_sum_euclidean_volume_inflation_barrier complete")
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_dcp_bad_register_audit(subparsers) -> None:
    dcp_bad_audit = subparsers.add_parser(
        "dcp-bad-register-audit",
        help="Physical CNOT merge audit under the real lattice-to-DCP bad-register promise.",
    )
    dcp_bad_audit.add_argument("--no-write", action="store_true")
    dcp_bad_audit.set_defaults(func=command_dcp_bad_register_audit)


def add_dcp_physical_bad_register_lineage(subparsers) -> None:
    dcp_lineage = subparsers.add_parser(
        "dcp-physical-bad-register-lineage",
        help="Audit physical CNOT bad-register lineage and visibility degradation.",
    )
    dcp_lineage.add_argument("--no-write", action="store_true")
    dcp_lineage.set_defaults(func=command_dcp_bad_register_audit)


def command_dcp_bad_register_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.dcp_physical_bad_register_lineage import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_dcp_collective_majority_purification_audit(subparsers) -> None:
    dcp_collective_majority_purification_audit = subparsers.add_parser(
        "dcp-collective-majority-purification-audit",
        help="Audit DCP shifted-box intersection producer, equal-label heralding dichotomy, and collective majority Helstrom optimality.",
    )
    dcp_collective_majority_purification_audit.add_argument("--no-write", action="store_true")
    dcp_collective_majority_purification_audit.set_defaults(func=command_dcp_collective_majority_purification_audit)


def command_dcp_collective_majority_purification_audit(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry
    initialize_seed_registry(overwrite=False)
    from theorems.dcp_collective_majority_purification_audit import REPORT, build_report, exact_json
    report = build_report()
    if not getattr(args, "no_write", False):
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    validation = validate_registry()
    print(report["status"])
    print(f"Artifact: {REPORT}")
    print(f"Registry valid: {validation['valid']}")
    return 0 if validation["valid"] else 1


def add_dcp_latent_error_access(subparsers) -> None:
    latent_access = subparsers.add_parser("dcp-latent-error-access",
        help="Reject hidden-error equality oracles on bare phase qubits; no general purification no-go.")
    latent_access.add_argument("--no-write", action="store_true")
    latent_access.set_defaults(func=command_dcp_latent_error_access)


def command_dcp_latent_error_access(args: argparse.Namespace) -> int:
    from theorems.dcp_latent_error_access_audit import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_complex_axis_readout(subparsers) -> None:
    complex_axes = subparsers.add_parser("dcp-complex-axis-readout",
        help="Export public X/Y/T-grid block readout; audit exact native all-secret Gram and charged inference limits.")
    complex_axes.add_argument("--no-write", action="store_true")
    complex_axes.set_defaults(func=command_dcp_complex_axis_readout)


def command_dcp_complex_axis_readout(args: argparse.Namespace) -> int:
    from theorems.dcp_complex_axis_readout import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_correlated_block_observables(subparsers) -> None:
    block_observables = subparsers.add_parser("dcp-correlated-block-observables",
        help="Calibrate full syndrome/X outcome likelihoods, low-degree blindness and a charged product-measurement twirl baseline.")
    block_observables.add_argument("--no-write", action="store_true")
    block_observables.set_defaults(func=command_dcp_correlated_block_observables)


def command_dcp_correlated_block_observables(args: argparse.Namespace) -> int:
    from theorems.dcp_correlated_block_observables import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_pairing_composition_barrier(subparsers) -> None:
    pairing_composition = subparsers.add_parser("dcp-pairing-composition-barrier",
        help="Bound two fresh one-pair compression levels under explicit independent-noise/source premises; no general DHSP no-go.")
    pairing_composition.add_argument("--no-write", action="store_true")
    pairing_composition.set_defaults(func=command_dcp_pairing_composition_barrier)


def command_dcp_pairing_composition_barrier(args: argparse.Namespace) -> int:
    from theorems.dcp_pairing_composition_barrier import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_correlated_phase_block(subparsers) -> None:
    correlated_block = subparsers.add_parser("dcp-correlated-phase-block",
        help="Export a polynomial CX/CCX syndrome measurement retaining the correlated original phase block, not a fiber inverse.")
    correlated_block.add_argument("--no-write", action="store_true")
    correlated_block.set_defaults(func=command_dcp_correlated_phase_block)


def command_dcp_correlated_phase_block(args: argparse.Namespace) -> int:
    from theorems.dcp_correlated_phase_block import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_native_tree_variance_cap(subparsers) -> None:
    variance_cap = subparsers.add_parser("dcp-native-tree-variance-cap",
        help="Audit exact native partial-list variances and smaller centered overflow caps, without silent proof transfer.")
    variance_cap.add_argument("--no-write", action="store_true")
    variance_cap.set_defaults(func=command_dcp_native_tree_variance_cap)


def command_dcp_native_tree_variance_cap(args: argparse.Namespace) -> int:
    from theorems.dcp_native_tree_variance_cap import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_oblivious_tree_merge(subparsers) -> None:
    oblivious_merge = subparsers.add_parser("dcp-oblivious-tree-merge",
        help="Test reversible bounded-output native joins with linear-sized sorting schedules, no free RAM.")
    oblivious_merge.add_argument("--no-write", action="store_true")
    oblivious_merge.set_defaults(func=command_dcp_oblivious_tree_merge)


def command_dcp_oblivious_tree_merge(args: argparse.Namespace) -> int:
    from theorems.dcp_oblivious_tree_merge import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_native_tree_receiver(subparsers) -> None:
    tree_receiver = subparsers.add_parser("dcp-native-tree-receiver",
        help="Run a clean bounded-list native tree program with whole-attempt overflow rejection and charged histories.")
    tree_receiver.add_argument("--no-write", action="store_true")
    tree_receiver.set_defaults(func=command_dcp_native_tree_receiver)


def command_dcp_native_tree_receiver(args: argparse.Namespace) -> int:
    from theorems.dcp_native_tree_receiver import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_native_tree_moment_audit(subparsers) -> None:
    tree_moment = subparsers.add_parser("dcp-native-tree-moment-audit",
        help="Audit native filtered-tree moments and overflow bounds; this is not an implemented quantum receiver.")
    tree_moment.add_argument("--no-write", action="store_true")
    tree_moment.set_defaults(func=command_dcp_native_tree_moment_audit)


def command_dcp_native_tree_moment_audit(args: argparse.Namespace) -> int:
    from theorems.dcp_native_tree_moment_audit import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_vector_short_mask_join(subparsers) -> None:
    vector_join = subparsers.add_parser("dcp-vector-short-mask-join",
        help="Run vector short-mask pairing with charged exponential sorting and coherent workspace; no new speedup.")
    vector_join.add_argument("--no-write", action="store_true")
    vector_join.set_defaults(func=command_dcp_vector_short_mask_join)


def command_dcp_vector_short_mask_join(args: argparse.Namespace) -> int:
    from theorems.dcp_vector_short_mask_join import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_noise_matched_source(subparsers) -> None:
    matched_source = subparsers.add_parser("dcp-noise-matched-source",
        help="Check conditional noisy source closure using visibility-matched zero-label replacement and paid supply.")
    matched_source.add_argument("--no-write", action="store_true")
    matched_source.set_defaults(func=command_dcp_noise_matched_source)


def command_dcp_noise_matched_source(args: argparse.Namespace) -> int:
    from theorems.dcp_noise_matched_source import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_disjoint_kernel_pairing(subparsers) -> None:
    disjoint_pairing = subparsers.add_parser("dcp-disjoint-kernel-pairing",
        help="Compile a polynomial coarse-only nonlinear pairing baseline with paid quadratic supply and exponential recursion.")
    disjoint_pairing.add_argument("--no-write", action="store_true")
    disjoint_pairing.set_defaults(func=command_dcp_disjoint_kernel_pairing)


def command_dcp_disjoint_kernel_pairing(args: argparse.Namespace) -> int:
    from theorems.dcp_disjoint_kernel_pairing import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_affine_fiber_rigidity(subparsers) -> None:
    affine_rigidity = subparsers.add_parser("dcp-affine-fiber-rigidity",
        help="Test global affine mod4 fibre rigidity; partial and adaptive programs remain outside the obstruction.")
    affine_rigidity.add_argument("--no-write", action="store_true")
    affine_rigidity.set_defaults(func=command_dcp_affine_fiber_rigidity)


def command_dcp_affine_fiber_rigidity(args: argparse.Namespace) -> int:
    from theorems.dcp_affine_fiber_rigidity import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_nonlinear_fiber_pairing(subparsers) -> None:
    nonlinear_pairing = subparsers.add_parser("dcp-nonlinear-fiber-pairing",
        help="Certify nonlinear phase descent, native fibre parity/coverage and charged pairing/noise frontiers.")
    nonlinear_pairing.add_argument("--no-write", action="store_true")
    nonlinear_pairing.set_defaults(func=command_dcp_nonlinear_fiber_pairing)


def command_dcp_nonlinear_fiber_pairing(args: argparse.Namespace) -> int:
    from theorems.dcp_nonlinear_fiber_pairing import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_affine_packet_noise(subparsers) -> None:
    affine_noise = subparsers.add_parser("dcp-affine-packet-noise",
        help="Audit original-register product-noise coherence and noise-aware affine feedback.")
    affine_noise.add_argument("--no-write", action="store_true")
    affine_noise.set_defaults(func=command_dcp_affine_packet_noise)


def command_dcp_affine_packet_noise(args: argparse.Namespace) -> int:
    from theorems.dcp_affine_packet_noise import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_adaptive_affine_packet_receiver(subparsers) -> None:
    affine_receiver = subparsers.add_parser("dcp-adaptive-affine-packet-receiver",
        help="Benchmark paid outcome-adaptive affine measurements on native carry packets.")
    affine_receiver.add_argument("--no-write", action="store_true")
    affine_receiver.set_defaults(func=command_dcp_adaptive_affine_packet_receiver)


def command_dcp_adaptive_affine_packet_receiver(args: argparse.Namespace) -> int:
    from theorems.dcp_adaptive_affine_packet_receiver import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_adaptive_direction_rank_gate(subparsers) -> None:
    adaptive_rank = subparsers.add_parser("dcp-adaptive-direction-rank-gate",
        help="Certify full-label pre-complement single-output descent and native random cut-rank bounds.")
    adaptive_rank.add_argument("--no-write", action="store_true")
    adaptive_rank.set_defaults(func=command_dcp_adaptive_direction_rank_gate)


def command_dcp_adaptive_direction_rank_gate(args: argparse.Namespace) -> int:
    from theorems.dcp_adaptive_direction_rank_gate import main
    return main(["--no-write"] if args.no_write else [])


def add_dcp_carry_congruence_source(subparsers) -> None:
    carry_source = subparsers.add_parser("dcp-carry-congruence-source",
        help="Certify higher-modulus conditional carry-source acceptance and full affine output laws.")
    carry_source.add_argument("--no-write", action="store_true")
    carry_source.set_defaults(func=command_dcp_carry_congruence_source)


def command_dcp_carry_congruence_source(args: argparse.Namespace) -> int:
    from theorems.dcp_carry_congruence_source import REPORT, build_report, exact_json
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(report["status"])
    print(f"Conditional source controls: {len(report['native_source_controls'])}")
    print(f"Artifact: {REPORT}")
    print("Integer source-law certificate only; no compiled quantum extractor or decoder.")
    return 0


def add_dcp_paid_tree_receiver(subparsers) -> None:
    paid_tree = subparsers.add_parser("dcp-paid-tree-receiver",
        help="Run paid physical CNOT feedback with a bounded exact single-parity policy benchmark.")
    paid_tree.add_argument("--no-write", action="store_true")
    paid_tree.set_defaults(func=command_dcp_paid_tree_receiver)


def command_dcp_paid_tree_receiver(args: argparse.Namespace) -> int:
    from theorems.dcp_paid_tree_receiver import REPORT, build_report, exact_json
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(report["status"])
    print(f"Actual source preparations: {report['actual_source_preparations_charged']}")
    print(f"Artifact: {REPORT}")
    print("Bounded exponential single-parity benchmark, not an efficient DCP solver.")
    return 0
