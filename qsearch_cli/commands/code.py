"""Code equivalence subcommands, moved out of qsearch.py by tools/split_cli/migrate.py.

Each ``add_*`` function registers one subcommand and each ``command_*`` function runs one.
A command imports what it needs from ``qsearch`` when it runs, so loading this module stays
cheap and ``monkeypatch.setattr(qsearch, name, ...)`` still reaches the command.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter



def add_code_family_search(subparsers) -> None:
    code_family_search = subparsers.add_parser(
        "code-family-search",
        help="Generate weak-invariant code-equivalence collisions and attack them with stronger classical invariants.",
    )
    code_family_search.add_argument("--no-registry", action="store_true")
    code_family_search.add_argument("--verbose", action="store_true")
    code_family_search.set_defaults(func=command_code_family_search)


def command_code_family_search(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_code_family_search
    initialize_seed_registry(overwrite=False)
    payload = write_code_family_search(write_registry=not args.no_registry)
    validation = validate_registry()
    print("Code-family hard search complete")
    print("Artifact: research/code_equivalence/code_family_search.json")
    print(f"Searches: {payload['headline_metrics']['search_count']}")
    print(f"Collisions: {payload['headline_metrics']['collision_found_count']}")
    print(f"Strong-invariant rejections: {payload['headline_metrics']['strong_invariant_rejection_count']}")
    print(f"Survivors: {payload['headline_metrics']['hard_family_candidate_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | trials={record['trials_run']} "
                f"strong={','.join(record['strong_distinguishing_invariants']) or 'none'}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_search(subparsers) -> None:
    code_self_dual_search = subparsers.add_parser(
        "code-self-dual-search",
        help="Search growing-hull self-dual code families and attack collisions with scalable and exact controls.",
    )
    code_self_dual_search.add_argument("--no-registry", action="store_true")
    code_self_dual_search.add_argument("--verbose", action="store_true")
    code_self_dual_search.set_defaults(func=command_code_self_dual_search)


def command_code_self_dual_search(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_self_dual_code_boundary
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_code_boundary(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual code boundary search complete")
    print("Artifact: research/code_equivalence/self_dual_code_boundary_search.json")
    print(f"Families: {metrics['family_count']}")
    print(f"Maximum dimension/length: {metrics['maximum_dimension']}/{metrics['maximum_length']}")
    print(f"Growing-hull families: {metrics['growing_hull_family_count']}")
    print(f"Scalable collision pairs: {metrics['scalable_collision_pair_count']}")
    print(f"Exact non-equivalent finite boundaries: {metrics['exact_nonequivalent_boundary_count']}")
    print(
        "Incidence cap/timeout debt: "
        f"{metrics['incidence_cap_count']}/{metrics['incidence_timeout_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["family_records"]:
            statuses = Counter(audit["status"] for audit in record["collision_audits"])
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"signature_classes={record['scalable_signature_class_count']} | {dict(statuses)}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_local_obstruction(subparsers) -> None:
    code_self_dual_local = subparsers.add_parser(
        "code-self-dual-local-obstruction",
        help="Certify why bounded puncture/shorten rank-hull profiles collapse below self-dual code distance.",
    )
    code_self_dual_local.add_argument("--no-registry", action="store_true")
    code_self_dual_local.add_argument("--verbose", action="store_true")
    code_self_dual_local.set_defaults(func=command_code_self_dual_local_obstruction)


def command_code_self_dual_local_obstruction(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_local_obstruction,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_local_obstruction(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual local-profile obstruction complete")
    print("Artifact: research/code_equivalence/self_dual_local_profile_obstruction.json")
    print(f"Instances: {metrics['instance_count']}")
    print(f"Full order-collapse instances: {metrics['full_order_collapse_instance_count']}")
    print(f"Full order-collapse families: {metrics['full_order_collapse_family_count']}")
    print(f"Theorem-covered subsets: {metrics['theorem_covered_subset_count']}")
    print(f"Control failures: {metrics['theorem_control_failure_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["family_records"]:
            print(
                f"- {record['family_id']} | {record['status']} | "
                f"common_order={record['maximum_certified_common_collapse_order']} "
                f"full_order_instances={record['full_order_collapse_instance_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_global_orbit(subparsers) -> None:
    code_self_dual_global = subparsers.add_parser(
        "code-self-dual-global-orbit",
        help="Audit global information-set orbits and Construction-A lattice invariants for self-dual codes.",
    )
    code_self_dual_global.add_argument("--no-registry", action="store_true")
    code_self_dual_global.add_argument("--verbose", action="store_true")
    code_self_dual_global.set_defaults(func=command_code_self_dual_global_orbit)


def command_code_self_dual_global_orbit(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_global_orbit_audit,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_global_orbit_audit(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual global orbit and Construction-A audit complete")
    print("Artifact: research/code_equivalence/self_dual_global_orbit_audit.json")
    print(f"Instances: {metrics['instance_count']}")
    print(
        "Largest estimated information-set count: "
        f"2^{metrics['maximum_estimated_log2_information_set_count']:.2f}"
    )
    print(f"Sampled exact equivalence witnesses: {metrics['sampled_equivalence_witness_count']}")
    print(f"Sampled misses retained as debt: {metrics['no_intersection_proof_debt_count']}")
    print(
        "Construction-A single-class families: "
        f"{metrics['construction_a_single_invariant_class_family_count']}"
    )
    print(f"Frame-preserving reverse reductions: {metrics['frame_preserving_reverse_reduction_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["family_records"]:
            print(
                f"- {record['family_id']} | {record['status']} | "
                f"log2_info_sets={record['maximum_estimated_log2_information_sets']} "
                f"lattice_classes={record['construction_a_invariant_class_count']} "
                f"witnesses/misses={record['sampled_equivalence_witness_count']}/"
                f"{record['no_intersection_proof_debt_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_hsp(subparsers) -> None:
    code_self_dual_hsp = subparsers.add_parser(
        "code-self-dual-hsp",
        help="Audit the exact wreath-product HSP reduction and published no-go applicability for self-dual codes.",
    )
    code_self_dual_hsp.add_argument("--no-registry", action="store_true")
    code_self_dual_hsp.add_argument("--verbose", action="store_true")
    code_self_dual_hsp.set_defaults(func=command_code_self_dual_hsp)


def command_code_self_dual_hsp(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_hsp_applicability,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_hsp_applicability(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual code-equivalence HSP applicability audit complete")
    print("Artifact: research/representation/self_dual_code_hsp_applicability.json")
    print(f"Families: {metrics['family_count']}")
    print(f"Published dimension-gate failures: {metrics['dimension_condition_fail_family_count']}")
    print(f"Certified single-coset no-go families: {metrics['single_coset_no_go_certified_family_count']}")
    print(f"Largest dimension-condition log2 gap: {metrics['maximum_dimension_condition_log2_gap']}")
    print(f"Largest wreath-HSP group log2 size: {metrics['maximum_log2_wreath_hsp_group_size']}")
    print(f"Explicit measurements: {metrics['explicit_single_coset_measurement_count'] + metrics['explicit_multicoset_measurement_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["family_records"]:
            print(
                f"- {record['family_id']} | {record['status']} | "
                f"condition_gap={record['dimension_condition_log2_gap']} "
                f"group_qubits={record['minimum_group_register_qubits']} "
                f"obvious_transposition_instances={record['obvious_transposition_instance_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_rowspace_hsp(subparsers) -> None:
    code_self_dual_rowspace_hsp = subparsers.add_parser(
        "code-self-dual-rowspace-hsp",
        help="Eliminate the GL row-scrambler gauge and certify the exact S_n rowspace hidden-shift reduction.",
    )
    code_self_dual_rowspace_hsp.add_argument("--no-registry", action="store_true")
    code_self_dual_rowspace_hsp.add_argument("--verbose", action="store_true")
    code_self_dual_rowspace_hsp.set_defaults(func=command_code_self_dual_rowspace_hsp)


def command_code_self_dual_rowspace_hsp(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_rowspace_hsp_reduction,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_rowspace_hsp_reduction(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual rowspace-canonical HSP reduction complete")
    print("Artifact: research/representation/self_dual_rowspace_hsp_reduction.json")
    print(f"Families with GL factor eliminated: {metrics['gl_factor_eliminated_family_count']}")
    print(f"Maximum eliminated log2 group size: {metrics['maximum_eliminated_group_log2_size']}")
    print(f"Hidden-shift control failures: {metrics['hidden_shift_control_failure_count']}")
    print(f"Obvious nonrigid instances: {metrics['obvious_nonrigid_instance_count']}")
    print(f"Rigidity-certified instances: {metrics['rigidity_certified_instance_count']}")
    print(f"GI-type no-go-certified instances: {metrics['gi_type_order_two_no_go_certified_instance_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["family_records"]:
            print(
                f"- {record['family_id']} | {record['status']} | "
                f"GL-eliminated={record['eliminated_group_log2_size']} "
                f"rowspace_group={record['rowspace_wreath_log2_size']} "
                f"nonrigid={record['obvious_nonrigid_instance_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_automorphisms(subparsers) -> None:
    code_self_dual_automorphisms = subparsers.add_parser(
        "code-self-dual-automorphisms",
        help="Certify self-dual tail rigidity or explicit automorphisms from exact bounded-weight supports.",
    )
    code_self_dual_automorphisms.add_argument("--no-registry", action="store_true")
    code_self_dual_automorphisms.add_argument("--verbose", action="store_true")
    code_self_dual_automorphisms.set_defaults(
        func=command_code_self_dual_automorphisms
    )


def command_code_self_dual_automorphisms(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_automorphism_workbench,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_automorphism_workbench(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual automorphism workbench complete")
    print("Artifact: research/code_equivalence/self_dual_automorphism_workbench.json")
    print(f"Tail instances: {metrics['instance_count']}")
    print(f"Rigidity-certified instances: {metrics['rigidity_certified_instance_count']}")
    print(f"Explicit automorphism instances: {metrics['explicit_automorphism_instance_count']}")
    print(f"Unresolved instances: {metrics['unresolved_instance_count']}")
    print(
        "GI-type single-register no-go instances: "
        f"{metrics['gi_type_single_register_no_go_certified_instance_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["family_records"]:
            print(
                f"- {record['family_id']} | {record['status']} | "
                f"rigid={record['rigidity_certified_instance_count']} "
                f"nonrigid={record['explicit_automorphism_instance_count']} "
                f"unresolved={record['unresolved_instance_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_high_order(subparsers) -> None:
    code_self_dual_high_order = subparsers.add_parser(
        "code-self-dual-high-order",
        help="Resolve sparse weight-eight self-dual automorphism debt with packed exact weight-ten supports.",
    )
    code_self_dual_high_order.add_argument("--no-registry", action="store_true")
    code_self_dual_high_order.add_argument("--verbose", action="store_true")
    code_self_dual_high_order.set_defaults(func=command_code_self_dual_high_order)


def command_code_self_dual_high_order(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_high_order_automorphism_resolver,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_high_order_automorphism_resolver(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    strata = payload["combined_tail_strata"]
    print("Self-dual high-order automorphism resolver complete")
    print(
        "Artifact: "
        "research/code_equivalence/self_dual_high_order_automorphism_resolver.json"
    )
    print(f"Target instances: {metrics['target_instance_count']}")
    print(
        "Resolved rigidity instances: "
        f"{metrics['resolved_rigidity_instance_count']}"
    )
    print(
        "Remaining unresolved instances: "
        f"{metrics['remaining_unresolved_instance_count']}"
    )
    print(
        "Combined rigid/nonrigid/unresolved: "
        f"{strata['rigidity_certified_instance_count']}/"
        f"{strata['explicit_nonrigid_instance_count']}/"
        f"{strata['unresolved_instance_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["family_records"]:
            print(
                f"- {record['family_id']} | {record['status']} | "
                f"resolved={record['resolved_rigidity_instance_count']} "
                f"remaining={record['remaining_unresolved_instance_count']} "
                f"weight={record['maximum_required_support_weight']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_sparsity(subparsers) -> None:
    code_self_dual_sparsity = subparsers.add_parser(
        "code-self-dual-sparsity",
        help="Prove why explicit fixed-order support rigidity certificates fail on growing random self-dual codes.",
    )
    code_self_dual_sparsity.add_argument("--no-registry", action="store_true")
    code_self_dual_sparsity.add_argument("--verbose", action="store_true")
    code_self_dual_sparsity.set_defaults(func=command_code_self_dual_sparsity)


def command_code_self_dual_sparsity(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_fixed_order_sparsity_obstruction,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_fixed_order_sparsity_obstruction(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual fixed-order sparsity obstruction complete")
    print(
        "Artifact: "
        "research/code_equivalence/self_dual_fixed_order_sparsity_obstruction.json"
    )
    print(f"Scaling lengths: {metrics['scaling_length_count']}")
    print(
        "Weight-ten expected-below-one rows: "
        f"{metrics['weight_10_expected_below_one_length_count']}"
    )
    print(
        "Entropy-half relative-weight threshold: "
        f"{metrics['entropy_half_relative_weight_threshold']}"
    )
    print(
        "Asymptotic fixed-order rigidity certificates: "
        f"{metrics['asymptotic_fixed_order_rigidity_certificate_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["observed_comparisons"]:
            print(
                f"- {record['family_id']} weight<={record['maximum_weight']} | "
                f"observed={record['mean_observed_support_count']} "
                f"expected={record['ensemble_expected_support_count']} "
                f"ratio={record['observed_to_expected_ratio']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath(subparsers) -> None:
    code_self_dual_wreath = subparsers.add_parser(
        "code-self-dual-wreath",
        help="Derive the exact one-copy representation spectrum for the rigid code-equivalence wreath HSP.",
    )
    code_self_dual_wreath.add_argument("--no-registry", action="store_true")
    code_self_dual_wreath.add_argument("--verbose", action="store_true")
    code_self_dual_wreath.set_defaults(func=command_code_self_dual_wreath)


def command_code_self_dual_wreath(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_self_dual_wreath_spectrum
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_spectrum(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath-product spectrum complete")
    print("Artifact: research/representation/self_dual_wreath_spectrum.json")
    print(f"Exact spectrum rows: {metrics['exact_record_count']}")
    print(f"Maximum n: {metrics['maximum_n']}")
    print(
        "Weak-Fourier zero-information rows: "
        f"{metrics['weak_fourier_zero_information_record_count']}"
    )
    print(
        "Maximum coarse zero-error copy lower bound: "
        f"{metrics['maximum_coarse_zero_error_copy_lower_bound']}"
    )
    print(
        "Growing-copy transforms/POVMs/decoders: "
        f"{metrics['growing_copy_diagonal_action_transform_count']}/"
        f"{metrics['carrier_sensitive_covariant_povm_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- n={record['n']} | {record['status']} | "
                f"log2|hidden|={record['log2_bridge_ensemble_size']} "
                f"holevo={record['exact_one_copy_holevo_bits']} "
                f"copies>={record['coarse_zero_error_copy_lower_bound']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_hecke(subparsers) -> None:
    code_self_dual_wreath_hecke = subparsers.add_parser(
        "code-self-dual-wreath-hecke",
        help="Audit the centralizer Hecke algebra without confusing it with the actual hidden-subgroup PGM.",
    )
    code_self_dual_wreath_hecke.add_argument("--no-registry", action="store_true")
    code_self_dual_wreath_hecke.add_argument("--verbose", action="store_true")
    code_self_dual_wreath_hecke.set_defaults(
        func=command_code_self_dual_wreath_hecke
    )


def command_code_self_dual_wreath_hecke(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_hecke_audit,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_hecke_audit(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath Hecke/Gelfand audit complete")
    print("Artifact: research/representation/self_dual_wreath_hecke_audit.json")
    print(
        "Centralizer Gelfand proofs: "
        f"{metrics['centralizer_gelfand_pair_proof_count']}/"
        f"{metrics['record_count']}"
    )
    print(
        "Actual hidden-subgroup non-Gelfand rows: "
        f"{metrics['actual_hidden_subgroup_non_gelfand_count']}"
    )
    print(
        "Pairwise scalar-kernel collapses: "
        f"{metrics['pairwise_hs_kernel_collapse_count']}/"
        f"{metrics['record_count']}"
    )
    print(
        "Maximum copy threshold/subset orbits: "
        f"{metrics['maximum_information_threshold_copy_count']}/"
        f"{metrics['maximum_register_subset_orbit_count']}"
    )
    print(
        "Operator reductions/POVMs/decoders: "
        f"{metrics['operator_valued_kcopy_frame_reduction_count']}/"
        f"{metrics['carrier_sensitive_covariant_povm_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- n={record['n']} | {record['status']} | "
                f"p(n)={record['partition_count']} "
                f"H-multiplicity>={record['actual_hidden_subgroup_multiplicity_lower_bound']} "
                f"copies={record['information_threshold_copy_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_pgm(subparsers) -> None:
    code_self_dual_wreath_pgm = subparsers.add_parser(
        "code-self-dual-wreath-pgm",
        help="Reduce the k-copy mixed-state PGM to a polar isometry and audit its factorial normalization barrier.",
    )
    code_self_dual_wreath_pgm.add_argument("--no-registry", action="store_true")
    code_self_dual_wreath_pgm.add_argument("--verbose", action="store_true")
    code_self_dual_wreath_pgm.set_defaults(
        func=command_code_self_dual_wreath_pgm
    )


def command_code_self_dual_wreath_pgm(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_pgm_polar_audit,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_pgm_polar_audit(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath PGM polar audit complete")
    print(
        "Artifact: "
        "research/representation/self_dual_wreath_pgm_polar_audit.json"
    )
    print(
        "Operator polar reductions/LCU contracts: "
        f"{metrics['operator_frame_polar_reduction_count']}/"
        f"{metrics['average_frame_lcu_contract_count']}"
    )
    print(f"Maximum copy count: {metrics['maximum_copy_count']}")
    print(
        "Maximum generic polar/Grover log2 charges: "
        f"{metrics['maximum_generic_polar_resolution_log2_charge']}/"
        f"{metrics['maximum_optimistic_grover_log2_candidate_queries']}"
    )
    print(
        "Preconditioners/frame inverses/POVM circuits/decoders: "
        f"{metrics['uniform_polynomial_structured_preconditioner_count']}/"
        f"{metrics['polynomial_frame_inverse_count']}/"
        f"{metrics['carrier_sensitive_povm_circuit_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- n={record['n']} | copies={record['copy_count']} "
                f"effective-rank={record['average_frame_effective_rank_fraction']} "
                f"polar-charge={record['generic_polar_resolution_log2_charge']} "
                f"grover-charge={record['optimistic_grover_log2_candidate_queries']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_carrier(subparsers) -> None:
    code_self_dual_wreath_carrier = subparsers.add_parser(
        "code-self-dual-wreath-carrier",
        help="Compute exact subset-orbit carrier commutators and truncated noncommutative algebra growth.",
    )
    code_self_dual_wreath_carrier.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_carrier.add_argument("--verbose", action="store_true")
    code_self_dual_wreath_carrier.set_defaults(
        func=command_code_self_dual_wreath_carrier
    )


def command_code_self_dual_wreath_carrier(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_subset_carrier_algebra,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_subset_carrier_algebra(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath subset-carrier algebra audit complete")
    print(
        "Artifact: "
        "research/representation/self_dual_wreath_subset_carrier_algebra.json"
    )
    print(
        "Commuting controls/symmetrized noncommuting rows: "
        f"{metrics['commuting_control_count']}/"
        f"{metrics['symmetrized_orbit_noncommutation_count']}"
    )
    print(
        "First noncommuting copy count: "
        f"{metrics['first_symmetrized_noncommuting_copy_count']}"
    )
    print(
        "Maximum truncated depth/rank/support: "
        f"{metrics['maximum_truncated_word_depth']}/"
        f"{metrics['maximum_truncated_algebra_rank_lower_bound']}/"
        f"{metrics['maximum_truncated_word_support_size']}"
    )
    print(
        "Carrier transforms/preconditioners/frame inverses/decoders: "
        f"{metrics['uniform_noncommutative_carrier_block_transform_count']}/"
        f"{metrics['polynomial_structured_frame_preconditioner_count']}/"
        f"{metrics['polynomial_frame_inverse_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["commutator_records"]:
            print(
                f"- {record['id']} | commutes={record['commutes']} "
                f"support={record['commutator_support_size']} "
                f"norm2={record['commutator_l2_squared_exact']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_orbits(subparsers) -> None:
    code_self_dual_wreath_orbits = subparsers.add_parser(
        "code-self-dual-wreath-orbits",
        help="Prove factorial hidden-label carrier-orbit growth at word depth three and cut explicit orbit tables.",
    )
    code_self_dual_wreath_orbits.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_orbits.add_argument("--verbose", action="store_true")
    code_self_dual_wreath_orbits.set_defaults(
        func=command_code_self_dual_wreath_orbits
    )


def command_code_self_dual_wreath_orbits(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_carrier_orbit_growth,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_carrier_orbit_growth(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath carrier-orbit growth audit complete")
    print(
        "Artifact: "
        "research/representation/self_dual_wreath_carrier_orbit_growth.json"
    )
    print(
        "Exact/total scaling rows: "
        f"{metrics['exact_record_count']}/{metrics['record_count']}"
    )
    print(
        "Factorial hidden-label orbit lower bounds: "
        f"{metrics['factorial_hidden_label_orbit_lower_bound_count']}"
    )
    print(
        "Maximum carrier/subset-profile log2 counts: "
        f"{metrics['maximum_log2_full_wreath_orbit_lower_bound']}/"
        f"{metrics['maximum_log2_subset_profile_upper_bound']}"
    )
    print(
        "Harmonic transforms/preconditioners/frame inverses/decoders: "
        f"{metrics['compressed_harmonic_block_transform_count']}/"
        f"{metrics['polynomial_structured_frame_preconditioner_count']}/"
        f"{metrics['polynomial_frame_inverse_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- n={record['n']} depth={record['word_depth']} | "
                f"log2-orbits>={record['log2_full_wreath_orbit_lower_bound']} "
                f"log2-subsets<={record['log2_subset_intersection_profile_upper_bound']} "
                f"factorial={record['factorial_lower_bound']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_harmonics(subparsers) -> None:
    code_self_dual_wreath_harmonics = subparsers.add_parser(
        "code-self-dual-wreath-harmonics",
        help="Derive exact simultaneous-conjugacy harmonic blocks and audit factorial Kronecker multiplicities.",
    )
    code_self_dual_wreath_harmonics.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_harmonics.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_harmonics.set_defaults(
        func=command_code_self_dual_wreath_harmonics
    )


def command_code_self_dual_wreath_harmonics(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_harmonic_carrier_schema,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_harmonic_carrier_schema(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath harmonic carrier schema audit complete")
    print(
        "Artifact: "
        "research/representation/self_dual_wreath_harmonic_carrier_schema.json"
    )
    print(
        "Harmonic/Burnside identity verifications: "
        f"{metrics['harmonic_burnside_identity_verification_count']}/"
        f"{metrics['exact_scaling_record_count']}"
    )
    print(
        "Exact blocks/non-multiplicity-free blocks: "
        f"{metrics['exact_block_record_count']}/"
        f"{metrics['non_multiplicity_free_block_count']}"
    )
    print(
        "Maximum certified block/multiplicity log2 lower bounds: "
        f"{metrics['maximum_log2_certified_block_coordinate_lower_bound']}/"
        f"{metrics['maximum_log2_certified_multiplicity_lower_bound']}"
    )
    print(
        "Internal transforms/sparse products/preconditioners/decoders: "
        f"{metrics['internal_kronecker_basis_transform_count']}/"
        f"{metrics['sparse_carrier_product_rule_count']}/"
        f"{metrics['polynomial_structured_frame_preconditioner_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["scaling_records"]:
            print(
                f"- n={record['n']} exact={record['exact']} | "
                f"p(n)={record['partition_count']} "
                f"log2-block>="
                f"{record['log2_certified_maximum_block_coordinate_lower_bound']} "
                f"identity={record['harmonic_burnside_identity_verified']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_commutant(subparsers) -> None:
    code_self_dual_wreath_commutant = subparsers.add_parser(
        "code-self-dual-wreath-commutant",
        help="Transfer the proved equal-source Kronecker gap and audit its factorially small carrier coverage.",
    )
    code_self_dual_wreath_commutant.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_commutant.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_commutant.set_defaults(
        func=command_code_self_dual_wreath_commutant
    )


def command_code_self_dual_wreath_commutant(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_commutant_transfer_audit,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_commutant_transfer_audit(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath commutant transfer audit complete")
    print(
        "Artifact: "
        "research/representation/self_dual_wreath_commutant_transfer_audit.json"
    )
    print(
        "Restricted all-n gap theorems/coordinates: "
        f"{metrics['restricted_all_n_inverse_polynomial_gap_theorem_count']}/"
        f"{metrics['restricted_invariant_matrix_coordinate_count']}"
    )
    print(
        "Maximum exact nontrivial sectors/unresolved states: "
        f"{metrics['maximum_exact_nontrivial_multiplicity_sector_count']}/"
        f"{metrics['maximum_exact_unresolved_internal_multiplicity_state_count']}"
    )
    print(
        "Maximum -log2 restricted coordinate coverage: "
        f"{metrics['maximum_negative_log2_restricted_coordinate_coverage_upper_bound']}"
    )
    print(
        "General gaps/cross-source rules/frame sectors/decoders: "
        f"{metrics['general_equal_source_gap_theorem_count']}/"
        f"{metrics['cross_source_carrier_mixing_rule_count']}/"
        f"{metrics['carrier_frame_invariant_subspace_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- n={record['n']} exact={record['exact']} | "
                f"gap={record['normalized_gap']} "
                f"-log2-coverage="
                f"{record['negative_log2_restricted_coordinate_coverage_upper_bound']} "
                f"unresolved="
                f"{record['unresolved_internal_multiplicity_state_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_frame_blocks(subparsers) -> None:
    code_self_dual_wreath_frame_blocks = subparsers.add_parser(
        "code-self-dual-wreath-frame-blocks",
        help="Construct actual equal-pair wreath Fourier frame blocks and audit finite spectra and conditioning.",
    )
    code_self_dual_wreath_frame_blocks.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_frame_blocks.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_frame_blocks.set_defaults(
        func=command_code_self_dual_wreath_frame_blocks
    )


def command_code_self_dual_wreath_frame_blocks(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_physical_frame_blocks,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_physical_frame_blocks(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath physical frame-block probe complete")
    print(
        "Artifact: "
        "research/representation/self_dual_wreath_physical_frame_blocks.json"
    )
    print(
        "Blocks/information-threshold blocks: "
        f"{metrics['record_count']}/"
        f"{metrics['information_threshold_block_count']}"
    )
    print(
        "Maximum dimension/distinct eigenvalues/condition number: "
        f"{metrics['maximum_block_dimension']}/"
        f"{metrics['maximum_distinct_eigenvalue_count']}/"
        f"{metrics['maximum_support_condition_number']}"
    )
    print(
        "Unequal blocks/all-n recurrences/preconditioners/decoders: "
        f"{metrics['unequal_pair_physical_block_count']}/"
        f"{metrics['uniform_all_n_spectral_recurrence_count']}/"
        f"{metrics['polynomial_structured_frame_preconditioner_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- n={record['n']} lambda={record['partition']} "
                f"k={record['copy_count']} minus={record['minus_sign_count']} | "
                f"rank={record['support_rank']}/{record['block_dimension']} "
                f"min={record['minimum_positive_eigenvalue']} "
                f"kappa={record['support_condition_number']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_unequal_blocks(subparsers) -> None:
    code_self_dual_wreath_unequal_blocks = subparsers.add_parser(
        "code-self-dual-wreath-unequal-blocks",
        help="Construct unequal-pair induced wreath blocks and expose collective spectra hidden at one copy.",
    )
    code_self_dual_wreath_unequal_blocks.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_unequal_blocks.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_unequal_blocks.set_defaults(
        func=command_code_self_dual_wreath_unequal_blocks
    )


def command_code_self_dual_wreath_unequal_blocks(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_unequal_frame_blocks,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_unequal_frame_blocks(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath unequal-pair frame-block probe complete")
    print(
        "Artifact: "
        "research/representation/self_dual_wreath_unequal_frame_blocks.json"
    )
    print(
        "Blocks/collective spectra/information-threshold blocks: "
        f"{metrics['record_count']}/"
        f"{metrics['collective_nontrivial_spectrum_count']}/"
        f"{metrics['information_threshold_unequal_block_count']}"
    )
    print(
        "Maximum dimension/distinct eigenvalues/condition number: "
        f"{metrics['maximum_block_dimension']}/"
        f"{metrics['maximum_distinct_eigenvalue_count']}/"
        f"{metrics['maximum_support_condition_number']}"
    )
    print(
        "Mixed tuples/all-n recurrences/preconditioners/decoders: "
        f"{metrics['mixed_physical_irrep_tuple_block_count']}/"
        f"{metrics['uniform_all_n_spectral_recurrence_count']}/"
        f"{metrics['polynomial_structured_frame_preconditioner_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- n={record['n']} lambda={record['left_partition']} "
                f"mu={record['right_partition']} k={record['copy_count']} | "
                f"rank={record['support_rank']}/{record['block_dimension']} "
                f"distinct={record['distinct_eigenvalue_count']} "
                f"kappa={record['support_condition_number']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_w3_tuples(subparsers) -> None:
    code_self_dual_wreath_w3_tuples = subparsers.add_parser(
        "code-self-dual-wreath-w3-tuples",
        help="Diagonalize every physical W_3 irrep tuple at the exact three-copy information threshold.",
    )
    code_self_dual_wreath_w3_tuples.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_w3_tuples.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_w3_tuples.set_defaults(
        func=command_code_self_dual_wreath_w3_tuples
    )


def command_code_self_dual_wreath_w3_tuples(
    args: argparse.Namespace,
) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_complete_w3_tuple_audit
    initialize_seed_registry(overwrite=False)
    payload = write_complete_w3_tuple_audit(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Complete W_3 physical tuple audit complete")
    print(
        "Artifact: "
        "research/representation/self_dual_wreath_complete_w3_tuple_audit.json"
    )
    print(
        "Irreps/tuples/naturally occupied tuples: "
        f"{metrics['physical_irrep_count']}/"
        f"{metrics['unordered_threshold_tuple_count']}/"
        f"{metrics['naturally_occupied_threshold_tuple_count']}"
    )
    print(
        "Natural mass/kernel mass/well-conditioned mass: "
        f"{metrics['natural_tuple_mass_sum']}/"
        f"{metrics['natural_mass_in_kernel_blocks']}/"
        f"{metrics['natural_mass_with_condition_number_at_most_four']}"
    )
    print(
        "Minimum positive eigenvalue/maximum condition number: "
        f"{metrics['minimum_naturally_occupied_positive_eigenvalue']}/"
        f"{metrics['maximum_naturally_occupied_support_condition_number']}"
    )
    print(
        "All-n recurrences/coherent inverses/harmonic transforms/decoders: "
        f"{metrics['uniform_all_n_character_moment_recurrence_count']}/"
        f"{metrics['coherent_blockwise_frame_inverse_count']}/"
        f"{metrics['hidden_label_harmonic_transform_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        worst = sorted(
            (
                record
                for record in payload["tuple_records"]
                if record["naturally_occupied"]
            ),
            key=lambda record: (
                record["support_condition_number"] or 0,
                record["aggregate_natural_probability"],
            ),
            reverse=True,
        )[:10]
        for record in worst:
            print(
                f"- labels={record['label_ids']} "
                f"mass={record['aggregate_natural_probability']} "
                f"rank={record['support_rank']}/{record['block_dimension']} "
                f"kappa={record['support_condition_number']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_moments(subparsers) -> None:
    code_self_dual_wreath_moments = subparsers.add_parser(
        "code-self-dual-wreath-moments",
        help="Derive exact mixed-block character moments and the all-n second-moment class recurrence.",
    )
    code_self_dual_wreath_moments.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_moments.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_moments.set_defaults(
        func=command_code_self_dual_wreath_moments
    )


def command_code_self_dual_wreath_moments(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_character_moments,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_character_moments(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath character-moment audit complete")
    print(
        "Artifact: "
        "research/representation/self_dual_wreath_character_moments.json"
    )
    print(
        "Validated W_3 moments/failures: "
        f"{metrics['w3_validated_tuple_moment_count']}/"
        f"{metrics['w3_failed_tuple_moment_count']}"
    )
    print(
        "Second-moment rows/max n/class terms: "
        f"{metrics['second_moment_scaling_record_count']}/"
        f"{metrics['maximum_second_moment_n']}/"
        f"{metrics['maximum_partition_class_term_count']}"
    )
    print(
        "Third-moment barriers/polynomial contractions/all-moment recurrences: "
        f"{metrics['third_moment_factorial_orbit_barrier_count']}/"
        f"{metrics['polynomial_third_moment_contraction_count']}/"
        f"{metrics['all_moment_spectral_recurrence_count']}"
    )
    print(
        "Support projectors/pseudoinverses/decoders: "
        f"{metrics['coherent_support_projector_count']}/"
        f"{metrics['coherent_blockwise_frame_pseudoinverse_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["w3_validation_records"]:
            print(
                f"- moment={record['moment_power']} "
                f"tuples={record['tuple_count']} "
                f"residual={record['maximum_absolute_residual']}"
            )
        for record in payload["scaling_records"]:
            print(
                f"- n={record['n']} portfolio={record['portfolio_id']} "
                f"k={record['copy_count']} "
                f"log2-effective-rank="
                f"{record['log2_effective_rank_fraction']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_third_moment(subparsers) -> None:
    code_self_dual_wreath_third_moment = subparsers.add_parser(
        "code-self-dual-wreath-third-moment",
        help="Contract the repeated trivial-standard unequal-sector third moment by a cycle-index rook recurrence.",
    )
    code_self_dual_wreath_third_moment.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_third_moment.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_third_moment.set_defaults(
        func=command_code_self_dual_wreath_third_moment
    )


def command_code_self_dual_wreath_third_moment(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_third_moment_contraction,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_third_moment_contraction(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath third-moment contraction complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_third_moment_contraction.json"
    )
    print(
        "Distribution/moment validations failed: "
        f"{metrics['failed_distribution_validation_count']}/"
        f"{metrics['failed_moment_validation_count']}"
    )
    print(
        "Scaling max n/k/states: "
        f"{metrics['maximum_scaling_n']}/"
        f"{metrics['maximum_scaling_copy_count']}/"
        f"{metrics['maximum_bivariate_state_count']}"
    )
    print(
        "Polynomial special/all-sector contractions: "
        f"{metrics['exact_polynomial_third_moment_contraction_count']}/"
        f"{metrics['all_physical_irrep_sector_contraction_count']}"
    )
    print(
        "Support gaps/pseudoinverses/decoders: "
        f"{metrics['support_gap_theorem_count']}/"
        f"{metrics['coherent_blockwise_frame_pseudoinverse_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["scaling_records"]:
            print(
                f"- n={record['n']} k={record['copy_count']} "
                f"support={record['distribution_support_size']} "
                f"states={record['bivariate_state_count']} "
                f"log2-normalized-m3="
                f"{record['log2_normalized_third_moment']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_all_unequal(subparsers) -> None:
    code_self_dual_wreath_all_unequal = subparsers.add_parser(
        "code-self-dual-wreath-all-unequal",
        help="Contract arbitrary unequal-only third moments by symmetric-group class algebra.",
    )
    code_self_dual_wreath_all_unequal.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_all_unequal.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_all_unequal.set_defaults(
        func=command_code_self_dual_wreath_all_unequal
    )


def command_code_self_dual_wreath_all_unequal(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_all_unequal_third_moment,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_all_unequal_third_moment(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath all-unequal third-moment audit complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_all_unequal_third_moment.json"
    )
    print(
        "Kernel/moment validation failures: "
        f"{metrics['failed_class_kernel_validation_count']}/"
        f"{metrics['failed_unequal_moment_validation_count']}"
    )
    print(
        "Max n/partitions/class triples/kernel terms: "
        f"{metrics['maximum_class_contraction_n']}/"
        f"{metrics['maximum_partition_count']}/"
        f"{metrics['maximum_class_triple_count']}/"
        f"{metrics['maximum_character_kernel_term_bound']}"
    )
    print(
        "Unequal/equal/all-sector contractions: "
        f"{metrics['arbitrary_mixed_unequal_tuple_contraction_count']}/"
        f"{metrics['equal_pair_commutator_contraction_count']}/"
        f"{metrics['all_physical_irrep_sector_contraction_count']}"
    )
    print(
        "Commutator counterexamples/min n: "
        f"{metrics['commutator_class_counterexample_count']}/"
        f"{metrics['minimum_commutator_counterexample_n']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        witness = payload["commutator_counterexample"]
        print(
            "- equal class triple "
            f"{witness['left_cycle_type']}/"
            f"{witness['right_cycle_type']}/"
            f"{witness['relative_cycle_type']} has commutators "
            f"{witness['first_commutator_cycle_type']} and "
            f"{witness['second_commutator_cycle_type']}"
        )
        for record in payload["scaling_records"]:
            print(
                f"- n={record['n']} k={record['copy_count']} "
                f"p(n)={record['partition_count']} "
                f"nonzero-triples={record['nonzero_class_triple_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_commutators(subparsers) -> None:
    code_self_dual_wreath_commutators = subparsers.add_parser(
        "code-self-dual-wreath-commutators",
        help="Contract pure commutator products and audit the mixed four-class recoupling kernel.",
    )
    code_self_dual_wreath_commutators.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_commutators.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_commutators.set_defaults(
        func=command_code_self_dual_wreath_commutators
    )


def command_code_self_dual_wreath_commutators(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_equal_commutator_audit,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_equal_commutator_audit(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath equal-commutator audit complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_equal_commutator_audit.json"
    )
    print(
        "Pure validations/failures/max n: "
        f"{metrics['pure_commutator_validation_count']}/"
        f"{metrics['failed_pure_commutator_validation_count']}/"
        f"{metrics['maximum_pure_commutator_scaling_n']}"
    )
    print(
        "Refined kernels/max n/pairs/quadruples: "
        f"{metrics['finite_refined_kernel_count']}/"
        f"{metrics['maximum_refined_kernel_n']}/"
        f"{metrics['maximum_refined_kernel_explicit_pair_count']}/"
        f"{metrics['maximum_refined_class_quadruple_support_count']}"
    )
    print(
        "Pure/mixed/polynomial-kernel contractions: "
        f"{metrics['exact_pure_commutator_frobenius_contraction_count']}/"
        f"{metrics['mixed_class_commutator_contraction_count']}/"
        f"{metrics['polynomial_refined_kernel_construction_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["refined_kernel_records"]:
            print(
                f"- n={record['n']} pairs={record['explicit_pair_count']} "
                f"triples={record['class_triple_support_count']} "
                f"quadruples={record['class_quadruple_support_count']} "
                f"split={record['split_class_triple_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_stable_rank(subparsers) -> None:
    code_self_dual_wreath_stable_rank = subparsers.add_parser(
        "code-self-dual-wreath-stable-rank",
        help="Measure stable-partition four-class feature rank and Plancherel mass coverage.",
    )
    code_self_dual_wreath_stable_rank.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_stable_rank.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_stable_rank.set_defaults(
        func=command_code_self_dual_wreath_stable_rank
    )


def command_code_self_dual_wreath_stable_rank(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_stable_commutator_rank,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_stable_commutator_rank(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath stable-partition rank audit complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_stable_commutator_rank.json"
    )
    print(
        "Rank controls/max n/rank/support: "
        f"{metrics['finite_rank_record_count']}/"
        f"{metrics['maximum_rank_control_n']}/"
        f"{metrics['maximum_stable_feature_algebra_rank']}/"
        f"{metrics['maximum_refined_kernel_support_count']}"
    )
    print(
        "Mass records/max n/min one-copy log2 mass: "
        f"{metrics['mass_scaling_record_count']}/"
        f"{metrics['maximum_mass_scaling_n']}/"
        f"{metrics['minimum_log2_one_copy_physical_stable_mass']}"
    )
    print(
        "Vanishing theorem/typical coverage/typical contraction: "
        f"{metrics['fixed_tail_vanishing_mass_theorem_count']}/"
        f"{metrics['typical_sector_coverage_count']}/"
        f"{metrics['polynomial_typical_four_class_contraction_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["rank_records"]:
            print(
                f"- n={record['n']} descriptors="
                f"{record['physical_descriptor_count']} "
                f"ranks={record['modular_rank_by_degree']} "
                f"support={record['refined_kernel_support_count']}"
            )
        for record in payload["mass_records"]:
            if record["tail_budget"] == 2:
                print(
                    f"- n={record['n']} b=2 "
                    f"log2-physical-mass="
                    f"{record['log2_one_copy_physical_label_mass']} "
                    f"log2-all-k="
                    f"{record['log2_all_threshold_labels_stable_mass']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_typical_portfolio(subparsers) -> None:
    code_self_dual_wreath_typical_portfolio = subparsers.add_parser(
        "code-self-dual-wreath-typical-portfolio",
        help="Measure constant-mass Plancherel catalogs and finite typical four-class feature rank.",
    )
    code_self_dual_wreath_typical_portfolio.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_typical_portfolio.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_typical_portfolio.set_defaults(
        func=command_code_self_dual_wreath_typical_portfolio
    )


def command_code_self_dual_wreath_typical_portfolio(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_typical_partition_portfolio,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_typical_partition_portfolio(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath typical-partition portfolio audit complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_typical_partition_portfolio.json"
    )
    print(
        "Catalog records/max n/partitions: "
        f"{metrics['catalog_record_count']}/"
        f"{metrics['maximum_catalog_n']}/"
        f"{metrics['maximum_partition_count']}"
    )
    print(
        "90% catalog/max-atom lower bound: "
        f"{metrics['maximum_ninety_percent_catalog_count']}/"
        f"{metrics['maximum_ninety_percent_atom_lower_bound']}"
    )
    print(
        "Typical rank controls/max rank/support: "
        f"{metrics['finite_typical_rank_record_count']}/"
        f"{metrics['maximum_typical_feature_algebra_rank']}/"
        f"{metrics['maximum_typical_refined_kernel_support_count']}"
    )
    print(
        "Catalog no-go/uniform rules/typical contractions: "
        f"{metrics['constant_mass_polynomial_catalog_no_go_theorem_count']}/"
        f"{metrics['uniform_partition_description_recoupling_rule_count']}/"
        f"{metrics['polynomial_typical_four_class_contraction_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["catalog_records"]:
            if record["target_source_mass"] == "9/10":
                print(
                    f"- n={record['n']} p(n)={record['partition_count']} "
                    f"catalog={record['catalog_partition_count']} "
                    f"physical-mass="
                    f"{record['exact_physical_pair_label_mass']}"
                )
        for record in payload["rank_records"]:
            print(
                f"- rank n={record['n']} selected="
                f"{record['selected_partition_count']} "
                f"ranks={record['modular_rank_by_degree']} "
                f"support={record['refined_kernel_support_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_self_dual_wreath_recoupling_transfer(subparsers) -> None:
    code_self_dual_wreath_recoupling_transfer = subparsers.add_parser(
        "code-self-dual-wreath-recoupling-transfer",
        help="Map known symmetric-group recoupling capabilities onto the physical four-class decoder contract.",
    )
    code_self_dual_wreath_recoupling_transfer.add_argument(
        "--no-registry", action="store_true"
    )
    code_self_dual_wreath_recoupling_transfer.add_argument(
        "--verbose", action="store_true"
    )
    code_self_dual_wreath_recoupling_transfer.set_defaults(
        func=command_code_self_dual_wreath_recoupling_transfer
    )


def command_code_self_dual_wreath_recoupling_transfer(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_self_dual_wreath_typical_recoupling_transfer,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_self_dual_wreath_typical_recoupling_transfer(
        write_registry=not args.no_registry
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Self-dual wreath typical recoupling transfer audit complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_typical_recoupling_transfer.json"
    )
    print(
        "Transfers/valid partial/missing blockers: "
        f"{metrics['capability_transfer_record_count']}/"
        f"{metrics['valid_partial_primitive_transfer_count']}/"
        f"{metrics['decoder_blocking_missing_primitive_count']}"
    )
    print(
        "Internal transforms/associators/four-class contractions: "
        f"{metrics['internal_kronecker_transform_count']}/"
        f"{metrics['kcopy_associator_count']}/"
        f"{metrics['mixed_four_class_contraction_count']}"
    )
    print(
        "Fixed collisions/max natural mass/end-to-end algorithms: "
        f"{metrics['fixed_separator_exact_collision_count']}/"
        f"{metrics['maximum_exact_collision_natural_source_pair_mass']}/"
        f"{metrics['new_end_to_end_quantum_algorithm_count']}"
    )
    print(
        "Parity-complete n=8 exact scalar obstructions: "
        f"{metrics['parity_complete_n8_exact_scalar_obstruction_count']}"
    )
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["capability_records"]:
            print(
                f"- {record['id']} count={record['source_count']} "
                f"status={record['transfer_status']} "
                f"blocks={record['blocks_decoder']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_wreath_projector_subpovm(subparsers) -> None:
    code_wreath_projector_subpovm = subparsers.add_parser(
        "code-wreath-projector-subpovm",
        help=(
            "Transfer the whitening-free projector sub-POVM theorem to the "
            "physical code-equivalence wreath HSP and audit condition debt."
        ),
    )
    code_wreath_projector_subpovm.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_projector_subpovm.set_defaults(
        func=command_code_wreath_projector_subpovm
    )


def command_code_wreath_projector_subpovm(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_wreath_projector_subpovm_transfer_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_wreath_projector_subpovm_transfer_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Physical wreath projector sub-POVM transfer complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_projector_subpovm_transfer.json"
    )
    print(
        "Transfer theorem/tail moment-only log2 bound: "
        f"{metrics['wreath_projector_subpovm_transfer_theorem_count']}/"
        f"{metrics['tail_moment_only_conclusive_log2_lower_bound']:.6g}"
    )
    print(
        "Direct dilation tail conclusive log2/structured maximal dilations: "
        f"{metrics['tail_direct_uniform_projector_conclusive_log2_probability']:.6g}/"
        f"{metrics['structured_maximal_effect_dilation_count']}"
    )
    print(
        "Selected threshold blocks/inverse-condition floor: "
        f"{metrics['selected_information_threshold_block_count']}/"
        f"{metrics['minimum_selected_inverse_condition_conclusive_floor']:.6g}"
    )
    print(
        "All-sector conditions/circuits/outcomes/decoders: "
        f"{metrics['natural_all_sector_polynomial_condition_theorem_count']}/"
        f"{metrics['uniform_wreath_covariant_subpovm_circuit_count']}/"
        f"{metrics['compressed_permutation_outcome_transform_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
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


def add_code_wreath_subpovm_moments(subparsers) -> None:
    code_wreath_subpovm_moments = subparsers.add_parser(
        "code-wreath-subpovm-moments",
        help=(
            "Convert physical wreath frame moments into rigorous projector-"
            "sub-POVM conclusive-probability certificates."
        ),
    )
    code_wreath_subpovm_moments.add_argument(
        "--moment-orders",
        default="2,3,4,8,16",
    )
    code_wreath_subpovm_moments.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_subpovm_moments.set_defaults(
        func=command_code_wreath_subpovm_moments
    )


def command_code_wreath_subpovm_moments(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_wreath_subpovm_moment_certificate_report,
    )
    initialize_seed_registry(overwrite=False)
    moment_orders = tuple(
        int(value.strip())
        for value in args.moment_orders.split(",")
        if value.strip()
    )
    payload = write_wreath_subpovm_moment_certificate_report(
        moment_orders=moment_orders,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Wreath sub-POVM moment certificate complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_subpovm_moment_certificate.json"
    )
    print(
        "Exact/order-4/order-16 natural conclusive: "
        f"{metrics['exact_w3_natural_average_conclusive_probability']:.6g}/"
        f"{metrics['order_four_certified_natural_average_conclusive_lower_bound']:.6g}/"
        f"{metrics['order_sixteen_certified_natural_average_conclusive_lower_bound']:.6g}"
    )
    print(
        "Tail factor-two moment order: "
        f"{metrics['tail_factor_two_moment_order_upper_bound']}"
    )
    print(
        "Equal-sector bypass/growing all-unequal contractions/"
        "all-order word reduction/growing word contraction/concentration/"
        "maximal dilations/decoders: "
        f"{metrics['natural_source_equal_sector_bypass_theorem_count']}/"
        f"{metrics['growing_order_all_unequal_contraction_count']}/"
        f"{metrics['all_order_natural_word_map_reduction_count']}/"
        f"{metrics['growing_order_word_map_contraction_count']}/"
        f"{metrics['natural_tuple_moment_concentration_theorem_count']}/"
        f"{metrics['structured_maximal_effect_dilation_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
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


def add_code_wreath_natural_unequal(subparsers) -> None:
    code_wreath_natural_unequal = subparsers.add_parser(
        "code-wreath-natural-unequal",
        help=(
            "Prove that natural information-threshold wreath tuples are "
            "asymptotically all unequal Plancherel-pair sectors."
        ),
    )
    code_wreath_natural_unequal.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_natural_unequal.set_defaults(
        func=command_code_wreath_natural_unequal
    )


def command_code_wreath_natural_unequal(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_unequal_dominance_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_natural_unequal_dominance_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Natural all-unequal wreath-sector reduction complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_natural_unequal_dominance.json"
    )
    print(
        "Exact controls/max n/source-law failures: "
        f"{metrics['exact_collision_control_count']}/"
        f"{metrics['maximum_exact_control_n']}/"
        f"{metrics['failed_source_law_identity_count']}"
    )
    print(
        "Tail equal/any-equal/all-unequal probabilities: "
        f"{metrics['tail_equal_label_probability']:.6g}/"
        f"{metrics['tail_any_equal_label_probability']:.6g}/"
        f"{metrics['tail_all_unequal_tuple_probability']:.6g}"
    )
    print(
        "Natural bypass/growing unequal contraction/decoder: "
        f"{metrics['equal_commutator_natural_critical_path_bypass_count']}/"
        f"{metrics['growing_order_all_unequal_contraction_count']}/"
        f"{metrics['polynomial_hidden_permutation_decoder_count']}"
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


def add_code_wreath_moment_word_map(subparsers) -> None:
    code_wreath_moment_word_map = subparsers.add_parser(
        "code-wreath-moment-word-map",
        help=(
            "Reduce all-order natural wreath-frame moments to identity and "
            "bridge-class subset word-map counts."
        ),
    )
    code_wreath_moment_word_map.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_moment_word_map.set_defaults(
        func=command_code_wreath_moment_word_map
    )


def command_code_wreath_moment_word_map(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_moment_word_map_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_natural_moment_word_map_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Natural wreath moment word-map reduction complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_natural_moment_word_map.json"
    )
    print(
        "Character/W3 validation failures: "
        f"{metrics['failed_character_sequence_count']}/"
        f"{metrics['failed_w3_spectrum_validation_count']}"
    )
    print(
        "All-order reductions/irrep sums removed: "
        f"{metrics['all_order_source_averaged_word_map_reduction_count']}/"
        f"{metrics['physical_irrep_sum_eliminated_count']}"
    )
    print(
        "Tail order/log2 explicit sequences/growing contractions/"
        "concentration: "
        f"{metrics['tail_required_moment_order']}/"
        f"{metrics['tail_log2_explicit_bridge_sequence_count']:.6g}/"
        f"{metrics['growing_order_word_map_contraction_count']}/"
        f"{metrics['natural_tuple_moment_concentration_theorem_count']}"
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


def add_code_wreath_word_map_mixing(subparsers) -> None:
    code_wreath_word_map_mixing = subparsers.add_parser(
        "code-wreath-word-map-mixing",
        help=(
            "Prove lazy bridge-walk mean mixing and quantify the unresolved "
            "shared-generator kth-moment concentration gap."
        ),
    )
    code_wreath_word_map_mixing.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_word_map_mixing.set_defaults(
        func=command_code_wreath_word_map_mixing
    )


def command_code_wreath_word_map_mixing(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_wreath_word_map_mixing_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_wreath_word_map_mixing_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Natural wreath word-map lazy-walk mixing complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_word_map_mixing.json"
    )
    print(
        "Lazy-walk controls/failures/mean-mixing theorems: "
        f"{metrics['lazy_walk_validation_count']}/"
        f"{metrics['failed_lazy_walk_validation_count']}/"
        f"{metrics['single_walk_mean_mixing_theorem_count']}"
    )
    print(
        "Tail log2 error ratio/kth-moment interval width: "
        f"{metrics['tail_log2_error_to_stationary_ratio_upper_bound']:.6g}/"
        f"{metrics['tail_log2_unresolved_kth_moment_interval_width']:.6g}"
    )
    print(
        "Coupled contractions/concentration/conclusive theorems: "
        f"{metrics['coupled_k_walk_contraction_count']}/"
        f"{metrics['word_map_concentration_theorem_count']}/"
        f"{metrics['natural_average_inverse_polynomial_conclusive_theorem_count']}"
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


def add_code_wreath_coupled_word_gap(subparsers) -> None:
    code_wreath_coupled_word_gap = subparsers.add_parser(
        "code-wreath-coupled-word-gap",
        help=(
            "Prove a constant shared-generator coupled-walk gap and expose "
            "the remaining all-unequal conditioned-moment obstruction."
        ),
    )
    code_wreath_coupled_word_gap.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_coupled_word_gap.set_defaults(
        func=command_code_wreath_coupled_word_gap
    )


def command_code_wreath_coupled_word_gap(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_wreath_coupled_word_walk_gap_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_wreath_coupled_word_walk_gap_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Coupled wreath word-walk gap audit complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_coupled_word_walk_gap.json"
    )
    print(
        "Subgroup/moment validation failures: "
        f"{metrics['bridge_subgroup_validation_failure_count']}/"
        f"{metrics['exact_coupled_moment_validation_failure_count']}"
    )
    print(
        "Coupled gap/transient-to-stationary log2 ratio: "
        f"{metrics['tail_coupled_spectral_gap_lower_bound']:.6g}/"
        f"{metrics['tail_log2_transient_to_stationary_ratio_upper_bound']:.6g}"
    )
    print(
        "Moment-root/second-moment scale/gap in bits: "
        f"{metrics['tail_log2_normalized_moment_root_upper_bound']:.6g}/"
        f"{metrics['tail_log2_second_moment_eigenvalue_scale']:.6g}/"
        f"{metrics['tail_log2_root_to_second_moment_scale_gap']:.6g}"
    )
    print(
        "Coupled contractions/conditioned kernels/conclusive theorems: "
        f"{metrics['coupled_k_walk_contraction_count']}/"
        f"{metrics['typical_all_unequal_conditioned_kernel_count']}/"
        f"{metrics['natural_average_inverse_polynomial_conclusive_theorem_count']}"
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


def add_code_wreath_conditioned_kernel(subparsers) -> None:
    code_wreath_conditioned_kernel = subparsers.add_parser(
        "code-wreath-conditioned-kernel",
        help=(
            "Derive the all-unequal conditioned character kernel and quantify "
            "the remaining simultaneous k-coordinate contraction gap."
        ),
    )
    code_wreath_conditioned_kernel.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_conditioned_kernel.set_defaults(
        func=command_code_wreath_conditioned_kernel
    )


def command_code_wreath_conditioned_kernel(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_all_unequal_conditioned_kernel_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_all_unequal_conditioned_kernel_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("All-unequal conditioned wreath kernel audit complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_all_unequal_conditioned_kernel.json"
    )
    print(
        "Kernel/word/annealed validation failures: "
        f"{metrics['conditioned_kernel_validation_failure_count']}/"
        f"{metrics['conditioned_word_validation_failure_count']}/"
        f"{metrics['conditioned_annealed_half_power_failure_count']}"
    )
    print(
        "Conditioned kernel/word reduction/half-norm bounds: "
        f"{metrics['typical_all_unequal_conditioned_kernel_count']}/"
        f"{metrics['all_order_conditioned_word_map_reduction_count']}/"
        f"{metrics['all_unequal_frame_half_norm_bound_count']}"
    )
    print(
        "Tail moment root/second-scale gap/simultaneous contractions: "
        f"{metrics['tail_log2_conditioned_normalized_moment_root_upper_bound']:.6g}/"
        f"{metrics['tail_log2_root_to_second_moment_scale_gap']:.6g}/"
        f"{metrics['simultaneous_k_coordinate_contraction_count']}"
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


def add_code_wreath_global_collision(subparsers) -> None:
    code_wreath_global_collision = subparsers.add_parser(
        "code-wreath-global-collision",
        help=(
            "Prove asymptotic global distinctness of all source Plancherel "
            "partitions and isolate the collision-free tuple frontier."
        ),
    )
    code_wreath_global_collision.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_global_collision.set_defaults(
        func=command_code_wreath_global_collision
    )


def command_code_wreath_global_collision(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_global_partition_collision_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_global_partition_collision_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Global Plancherel collision audit complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_global_partition_collision.json"
    )
    print(
        "Controls/global-source/union-bound/asymptotic theorems: "
        f"{metrics['global_collision_control_count']}/"
        f"{metrics['global_source_draw_as_iid_plancherel_theorem_count']}/"
        f"{metrics['global_collision_union_bound_theorem_count']}/"
        f"{metrics['asymptotic_global_all_distinct_dominance_theorem_count']}"
    )
    print(
        "Counterexamples/excluded/collision-free norm/contraction: "
        f"{metrics['repeated_source_half_norm_counterexample_count']}/"
        f"{metrics['repeated_source_counterexample_exclusion_count']}/"
        f"{metrics['collision_free_tuple_norm_theorem_count']}/"
        f"{metrics['collision_free_growing_moment_contraction_count']}"
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


def add_code_wreath_collision_free_frame(subparsers) -> None:
    code_wreath_collision_free_frame = subparsers.add_parser(
        "code-wreath-collision-free-frame",
        help=(
            "Probe mixed collision-free wreath frame norms and test the "
            "poly(n)2^-k contraction target."
        ),
    )
    code_wreath_collision_free_frame.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_collision_free_frame.set_defaults(
        func=command_code_wreath_collision_free_frame
    )


def command_code_wreath_collision_free_frame(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_collision_free_frame_probe_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_collision_free_frame_probe_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Collision-free mixed wreath frame probe complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_collision_free_frame_probe.json"
    )
    print(
        "Probes/W4 complete/W5 three-copy/max dimension: "
        f"{metrics['collision_free_probe_count']}/"
        f"{metrics['complete_w4_collision_free_pairing_count']}/"
        f"{metrics['w5_collision_free_three_copy_probe_count']}/"
        f"{metrics['maximum_probe_block_dimension']}"
    )
    print(
        "W5 exact-target violations/factor-two successes/max ratio: "
        f"{metrics['w5_exact_two_to_one_minus_k_violation_count']}/"
        f"{metrics['w5_factor_two_target_bound_success_count']}/"
        f"{metrics['maximum_w5_top_to_target_ratio']:.6g}"
    )
    print(
        "Polynomial-factor norm/growing contractions: "
        f"{metrics['collision_free_polynomial_factor_norm_theorem_count']}/"
        f"{metrics['collision_free_growing_moment_contraction_count']}"
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


def add_code_wreath_character_ratios(subparsers) -> None:
    code_wreath_character_ratios = subparsers.add_parser(
        "code-wreath-character-ratios",
        help=(
            "Formalize the character-ratio and short-word proof contract for "
            "collision-free poly(n)2^-k frame contraction."
        ),
    )
    code_wreath_character_ratios.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_character_ratios.set_defaults(
        func=command_code_wreath_character_ratios
    )


def command_code_wreath_character_ratios(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_character_ratio_contract_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_character_ratio_contract_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Collision-free character-ratio contract complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_character_ratio_contract.json"
    )
    print(
        "Factorization controls/failures/literature bounds: "
        f"{metrics['character_factorization_validation_count']}/"
        f"{metrics['character_factorization_failure_count']}/"
        f"{metrics['literature_linked_character_bound_count']}"
    )
    print(
        "Typical-shape/short-word/norm/contraction theorems: "
        f"{metrics['simultaneous_typical_shape_tail_theorem_count']}/"
        f"{metrics['joint_short_word_anticoncentration_theorem_count']}/"
        f"{metrics['collision_free_polynomial_factor_norm_theorem_count']}/"
        f"{metrics['collision_free_growing_moment_contraction_count']}"
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


def add_code_wreath_short_words(subparsers) -> None:
    code_wreath_short_words = subparsers.add_parser(
        "code-wreath-short-words",
        help=(
            "Compute exact fixed-mask bridge-word marginals, short-length "
            "tails, and target-order mask-collision bounds."
        ),
    )
    code_wreath_short_words.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_short_words.set_defaults(
        func=command_code_wreath_short_words
    )


def command_code_wreath_short_words(
    args: argparse.Namespace,
) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_short_word_profile_report
    initialize_seed_registry(overwrite=False)
    payload = write_short_word_profile_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Bridge subset short-word profile complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_short_word_profile.json"
    )
    print(
        "Uniformity controls/failures/Stirling formulas: "
        f"{metrics['fixed_mask_uniformity_validation_count']}/"
        f"{metrics['fixed_mask_uniformity_failure_count']}/"
        f"{metrics['unsigned_stirling_short_length_formula_count']}"
    )
    print(
        "Tail half-n short log2 probability/mask collision log2 bound: "
        f"{metrics['tail_half_n_log2_short_probability']:.6g}/"
        f"{metrics['tail_log2_pairwise_mask_collision_union_bound']:.6g}"
    )
    print(
        "Non-diagonal correlation/joint tail/norm theorems: "
        f"{metrics['non_diagonal_shared_generator_correlation_theorem_count']}/"
        f"{metrics['joint_short_word_anticoncentration_theorem_count']}/"
        f"{metrics['collision_free_polynomial_factor_norm_theorem_count']}"
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


def add_code_wreath_mask_hypergraph(subparsers) -> None:
    code_wreath_mask_hypergraph = subparsers.add_parser(
        "code-wreath-mask-hypergraph",
        help=(
            "Reduce nonzero joint unequal-character products to dense "
            "mask-incidence two-cores and audit exact triangle residuals."
        ),
    )
    code_wreath_mask_hypergraph.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_mask_hypergraph.set_defaults(
        func=command_code_wreath_mask_hypergraph
    )


def command_code_wreath_mask_hypergraph(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_mask_hypergraph_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_mask_hypergraph_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Mask-incidence hypergraph reduction complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_mask_hypergraph_reduction.json"
    )
    print(
        "Private-column controls/failures/two-core reductions: "
        f"{metrics['private_column_validation_count']}/"
        f"{metrics['private_column_validation_failure_count']}/"
        f"{metrics['mask_hypergraph_two_core_reduction_count']}"
    )
    print(
        "W5 triangles/nonzero/max correlation: "
        f"{metrics['w5_collision_free_triangle_record_count']}/"
        f"{metrics['w5_nonzero_collision_free_triangle_count']}/"
        f"{metrics['maximum_w5_collision_free_triangle_correlation']:.6g}"
    )
    print(
        "Two-core/joint-tail/norm theorems: "
        f"{metrics['joint_two_core_anticoncentration_theorem_count']}/"
        f"{metrics['joint_short_word_anticoncentration_theorem_count']}/"
        f"{metrics['collision_free_polynomial_factor_norm_theorem_count']}"
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


def add_code_wreath_subgroup_twirl(subparsers) -> None:
    code_wreath_subgroup_twirl = subparsers.add_parser(
        "code-wreath-subgroup-twirl",
        help=(
            "Resum dense mask correlations as a subgroup twirl and reduce "
            "the collision-free norm theorem to isotypic partial traces."
        ),
    )
    code_wreath_subgroup_twirl.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_subgroup_twirl.set_defaults(
        func=command_code_wreath_subgroup_twirl
    )


def command_code_wreath_subgroup_twirl(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_subgroup_twirl_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_subgroup_twirl_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Subgroup-twirl isotypic reduction complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_subgroup_twirl_reduction.json"
    )
    print(
        "W4 validations/failures/max residual: "
        f"{metrics['complete_w4_collision_free_twirl_validation_count']}/"
        f"{metrics['finite_twirl_validation_failure_count']}/"
        f"{metrics['maximum_finite_twirl_validation_residual']:.6g}"
    )
    print(
        "Conjugacy/twirl/isotypic reduction theorems: "
        f"{metrics['bridge_subgroup_conjugacy_identity_theorem_count']}/"
        f"{metrics['subgroup_twirl_identity_theorem_count']}/"
        f"{metrics['isotypic_partial_trace_reduction_theorem_count']}"
    )
    print(
        "Tail n/k/max multiplicity log2/partial-trace theorem: "
        f"{metrics['tail_n']}/"
        f"{metrics['tail_copy_count']}/"
        f"{metrics['tail_maximum_restriction_multiplicity_log2']:.6g}/"
        f"{metrics['uniform_partial_trace_delocalization_theorem_count']}"
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


def add_code_wreath_orientation_fourier(subparsers) -> None:
    code_wreath_orientation_fourier = subparsers.add_parser(
        "code-wreath-orientation-fourier",
        help=(
            "Reduce the collision-free orbit Gram Fourier blocks to "
            "orientation-projector averages and audit support saturation."
        ),
    )
    code_wreath_orientation_fourier.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_fourier.set_defaults(
        func=command_code_wreath_orientation_fourier
    )


def command_code_wreath_orientation_fourier(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_fourier_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_fourier_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Orientation-projector Fourier reduction complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_orientation_fourier_reduction.json"
    )
    print(
        "W4 validations/failures/orbit-spectrum residual: "
        f"{metrics['complete_w4_orientation_fourier_validation_count']}/"
        f"{metrics['finite_orientation_fourier_validation_failure_count']}/"
        f"{metrics['maximum_orbit_gram_spectral_residual']:.6g}"
    )
    print(
        "Overlap/orbit/projector theorems: "
        f"{metrics['compressed_overlap_formula_theorem_count']}/"
        f"{metrics['operator_valued_orbit_gram_fourier_theorem_count']}/"
        f"{metrics['orientation_invariant_projector_decomposition_theorem_count']}"
    )
    print(
        "Tail n/k/log2 active/min fraction/full-support step: "
        f"{metrics['tail_n']}/"
        f"{metrics['tail_copy_count']}/"
        f"{metrics['tail_log2_maximum_active_orientation_count']:.6g}/"
        f"{metrics['tail_minimum_active_orientation_fraction']:.6g}/"
        f"{metrics['tail_first_full_support_saturation_step']}"
    )
    print(
        "Uniform projector-sum norm theorem: "
        f"{metrics['uniform_projector_sum_norm_theorem_count']}"
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


def add_code_wreath_orientation_moments(subparsers) -> None:
    code_wreath_orientation_moments = subparsers.add_parser(
        "code-wreath-orientation-moments",
        help=(
            "Compute exact pairwise orientation-projector overlaps and "
            "class-algebra second moments through the copy threshold."
        ),
    )
    code_wreath_orientation_moments.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_moments.set_defaults(
        func=command_code_wreath_orientation_moments
    )


def command_code_wreath_orientation_moments(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_fusion_moment_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_fusion_moment_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Orientation fusion-frame moment reduction complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_orientation_fusion_moment.json"
    )
    print(
        "W4 tuples/pair validations/failures/max residual: "
        f"{metrics['complete_w4_fusion_tuple_validation_count']}/"
        f"{metrics['pair_overlap_formula_validation_count']}/"
        f"{metrics['finite_pair_overlap_validation_failure_count']}/"
        f"{metrics['maximum_pair_overlap_formula_residual']:.6g}"
    )
    print(
        "Pair/class-second-moment theorems/common-range pairs: "
        f"{metrics['pairwise_character_convolution_theorem_count']}/"
        f"{metrics['orientation_average_class_algebra_second_moment_theorem_count']}/"
        f"{metrics['w4_common_range_pair_count']}"
    )
    print(
        "Tail n/k/collision-to-target/effective-rank log2: "
        f"{metrics['tail_n']}/"
        f"{metrics['tail_copy_count']}/"
        f"{metrics['tail_collision_lower_bound_to_target_ratio']:.6g}/"
        f"{metrics['tail_maximum_log2_effective_rank']:.6g}"
    )
    print(
        "Higher-moment/projector-sum norm theorems: "
        f"{metrics['higher_orientation_moment_norm_theorem_count']}/"
        f"{metrics['uniform_projector_sum_norm_theorem_count']}"
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


def add_code_wreath_pair_core_carrier_factorization(subparsers) -> None:
    code_wreath_pair_core_carrier_factorization = subparsers.add_parser(
        "code-wreath-pair-core-carrier-factorization",
        help=(
            "Derive and validate the exact two-carrier reciprocal spectrum "
            "of shared-vertex pair-core overlaps."
        ),
    )
    code_wreath_pair_core_carrier_factorization.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_core_carrier_factorization.set_defaults(
        func=command_code_wreath_pair_core_carrier_factorization
    )


def command_code_wreath_pair_core_carrier_factorization(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_core_carrier_factorization_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pair_core_carrier_factorization_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Pair-core carrier factorization complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_pair_core_carrier_factorization.json"
    )
    print(
        "Selected/screened star controls and failures: "
        f"{metrics['selected_star_control_count']}/"
        f"{metrics['screened_star_control_count']}/"
        f"{metrics['selected_star_failure_count']}/"
        f"{metrics['screened_star_failure_count']}"
    )
    print(
        "Max spectrum residual / off-common violations: "
        f"{metrics['maximum_spectrum_residual']:.6g}/"
        f"{metrics['screened_off_common_violation_count']}"
    )
    print(
        "Disjoint waist controls/violations/tight: "
        f"{metrics['disjoint_waist_control_count']}/"
        f"{metrics['disjoint_waist_violation_count']}/"
        f"{metrics['disjoint_waist_tight_count']}"
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


def add_code_wreath_multistar_degree(subparsers) -> None:
    code_wreath_multistar_degree = subparsers.add_parser(
        "code-wreath-multistar-degree",
        help=(
            "Measure the exact sign-blind weighted degree of the crossing "
            "pair-core graph on natural threshold portfolios."
        ),
    )
    code_wreath_multistar_degree.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_multistar_degree.set_defaults(
        func=command_code_wreath_multistar_degree
    )


def command_code_wreath_multistar_degree(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_multistar_degree_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_multistar_degree_obstruction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Multistar degree obstruction complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_multistar_degree_obstruction.json"
    )
    print(
        "Natural samples/vacuous/first vacuous degree: "
        f"{metrics['natural_sample_count']}/"
        f"{metrics['natural_sample_vacuous_count']}/"
        f"{metrics['first_vacuous_degree']}"
    )
    print(
        "Max projected weighted degree log2 / saturation ratio: "
        f"{metrics['maximum_projected_weighted_degree_log2']:.6g}/"
        f"{metrics['maximum_saturation_ratio']:.6g}"
    )
    print(
        "Laplacian controls/failures/max residual: "
        f"{metrics['laplacian_equivalence_control_count']}/"
        f"{metrics['laplacian_equivalence_failure_count']}/"
        f"{metrics['maximum_laplacian_spectrum_residual']:.6g}"
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


def add_code_wreath_pair_quotient_overlap(subparsers) -> None:
    code_wreath_pair_quotient_overlap = subparsers.add_parser(
        "code-wreath-pair-quotient-overlap",
        help=(
            "Audit the exact residual principal-angle gap after quotienting "
            "all crossing pair cores."
        ),
    )
    code_wreath_pair_quotient_overlap.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_quotient_overlap.set_defaults(
        func=command_code_wreath_pair_quotient_overlap
    )


def command_code_wreath_pair_quotient_overlap(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_quotient_overlap_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pair_quotient_overlap_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Pair-core quotient overlap complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_pair_quotient_overlap.json"
    )
    print(
        "S6 min gap / S6 phase certificates / S6 merges: "
        f"{metrics['s6_minimum_exact_pair_quotient_gap']:.6g}/"
        f"{metrics['s6_phase_only_certificate_count']}/"
        f"{metrics['s6_affine_merge_audit_count']}"
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


def add_code_wreath_recursive_pair_generation(subparsers) -> None:
    code_wreath_recursive_pair_generation = subparsers.add_parser(
        "code-wreath-recursive-pair-generation",
        help=(
            "Verify the exact recursive H0 short-exact sequence and exhaust "
            "all S5 affine boundary nodes."
        ),
    )
    code_wreath_recursive_pair_generation.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_recursive_pair_generation.set_defaults(
        func=command_code_wreath_recursive_pair_generation
    )


def command_code_wreath_recursive_pair_generation(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_recursive_pair_generation_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_recursive_pair_generation_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Recursive pair generation complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_recursive_pair_generation.json"
    )
    print(
        "S5 affine nodes / emergent H0 nodes / S5 portfolios: "
        f"{metrics['s5_affine_node_audit_count']}/"
        f"{metrics['s5_emergent_h0_node_count']}/"
        f"{metrics['s5_globally_distinct_portfolio_count']}"
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


def add_code_wreath_augmented_common_core_cech(subparsers) -> None:
    code_wreath_augmented_common_core_cech = subparsers.add_parser(
        "code-wreath-augmented-common-core-cech",
        help=(
            "Audit the augmented common-core Cech complex with leaf "
            "synthesis."
        ),
    )
    code_wreath_augmented_common_core_cech.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_augmented_common_core_cech.set_defaults(
        func=command_code_wreath_augmented_common_core_cech
    )


def command_code_wreath_augmented_common_core_cech(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_augmented_common_core_cech_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_augmented_common_core_cech_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Augmented common-core Cech complex complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_augmented_common_core_cech.json"
    )
    print(
        "W3 distinct/repeated H0 dim / W5 H0 dim / Cube min Hodge eval: "
        f"{metrics['w3_distinct_emergent_h0_dimension']}/"
        f"{metrics['w3_repeated_emergent_h0_dimension']}/"
        f"{metrics['w5_emergent_h0_dimension']}/"
        f"{metrics['depth_three_cube_minimum_positive_hodge_eigenvalue']:.6g}"
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


def add_code_wreath_common_core_cech(subparsers) -> None:
    code_wreath_common_core_cech = subparsers.add_parser(
        "code-wreath-common-core-cech",
        help=(
            "Verify exact pair-cycle resolution on the relative "
            "common-core Cech complex."
        ),
    )
    code_wreath_common_core_cech.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_common_core_cech.set_defaults(
        func=command_code_wreath_common_core_cech
    )


def command_code_wreath_common_core_cech(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_common_core_cech_laplacian_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_common_core_cech_laplacian_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Common-core Cech complex Laplacian complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_common_core_cech_laplacian.json"
    )
    print(
        "Min positive eval / max condition number / emergent H1 dim: "
        f"{metrics['minimum_positive_pair_laplacian_eigenvalue']:.6g}/"
        f"{metrics['maximum_pair_laplacian_condition_number']:.6g}/"
        f"{metrics['finite_emergent_pair_cycle_homology_dimension']}"
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


def add_code_wreath_pair_core_recoupling(subparsers) -> None:
    code_wreath_pair_core_recoupling = subparsers.add_parser(
        "code-wreath-pair-core-recoupling",
        help=(
            "Analyze local scalar recouplings and screen S6 pair-core "
            "correlations."
        ),
    )
    code_wreath_pair_core_recoupling.add_argument(
        "--limit",
        type=int,
        default=180,
        help="Maximum S6 controls to screen.",
    )
    code_wreath_pair_core_recoupling.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_core_recoupling.set_defaults(
        func=command_code_wreath_pair_core_recoupling
    )


def command_code_wreath_pair_core_recoupling(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_core_recoupling_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pair_core_recoupling_boundary_report(
        screen_control_limit=args.limit,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Pair-core recoupling boundary analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_pair_core_recoupling_boundary.json"
    )
    print(
        "Screened stars / controls / min endpoint gap / unexpected correlations: "
        f"{metrics['screened_pair_core_star_count']}/"
        f"{metrics['screened_control_count']}/"
        f"{metrics['selected_minimum_certified_endpoint_gap']:.6g}/"
        f"{metrics['screened_unexpected_correlation_count']}"
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


def add_code_wreath_common_core_atomization(subparsers) -> None:
    code_wreath_common_core_atomization = subparsers.add_parser(
        "code-wreath-common-core-atomization",
        help=(
            "Construct exact parity intertwiners and verify the relative "
            "Cech atom formula."
        ),
    )
    code_wreath_common_core_atomization.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_common_core_atomization.set_defaults(
        func=command_code_wreath_common_core_atomization
    )


def command_code_wreath_common_core_atomization(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_common_core_atomization_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_common_core_atomization_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Common-core atomization complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_common_core_atomization.json"
    )
    print(
        "Controls / crossing atoms / max commutator norm: "
        f"{metrics['finite_control_count']}/"
        f"{metrics['finite_crossing_atom_count']}/"
        f"{metrics['maximum_pair_core_projector_commutator_norm']:.6g}"
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


def add_code_wreath_orientation_laplacian_gap(subparsers) -> None:
    code_wreath_orientation_laplacian_gap = subparsers.add_parser(
        "code-wreath-orientation-laplacian-gap",
        help=(
            "Analyze orientation Laplacian spectrum and test width-independent "
            "floor."
        ),
    )
    code_wreath_orientation_laplacian_gap.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_laplacian_gap.set_defaults(
        func=command_code_wreath_orientation_laplacian_gap
    )


def command_code_wreath_orientation_laplacian_gap(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_laplacian_gap_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_laplacian_gap_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Orientation Laplacian gap analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_orientation_laplacian_gap.json"
    )
    print(
        "Full-graph controls / min positive eval / floor violations: "
        f"{metrics['screened_full_graph_control_count']}/"
        f"{metrics['minimum_observed_positive_eigenvalue']:.6g}/"
        f"{metrics['screened_floor_violation_count']}"
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


def add_code_wreath_orientation_common_ranges(subparsers) -> None:
    code_wreath_orientation_common_ranges = subparsers.add_parser(
        "code-wreath-orientation-common-ranges",
        help="Analyze trivial/sign common-range multiplicities.",
    )
    code_wreath_orientation_common_ranges.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_common_ranges.set_defaults(
        func=command_code_wreath_orientation_common_ranges
    )


def command_code_wreath_orientation_common_ranges(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_common_range_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_common_range_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Orientation common-range analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_orientation_common_range.json"
    )
    print(
        "Validation count / failures / scaling records: "
        f"{metrics['common_range_formula_validation_count']}/"
        f"{metrics['finite_common_range_validation_failure_count']}/"
        f"{metrics['scaling_record_count']}"
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


def add_code_wreath_orientation_family_ranges(subparsers) -> None:
    code_wreath_orientation_family_ranges = subparsers.add_parser(
        "code-wreath-orientation-family-ranges",
        help="Analyze fixed-family triple-range multi-way incidence.",
    )
    code_wreath_orientation_family_ranges.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_family_ranges.set_defaults(
        func=command_code_wreath_orientation_family_ranges
    )


def command_code_wreath_orientation_family_ranges(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_triple_range_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_triple_range_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Orientation triple-range analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_orientation_triple_range.json"
    )
    print(
        "Formula validations / failures / sampling records: "
        f"{metrics['finite_formula_validation_count']}/"
        f"{metrics['finite_formula_validation_failure_count']}/"
        f"{metrics['sampling_record_count']}"
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


def add_code_wreath_orientation_pair_angles(subparsers) -> None:
    code_wreath_orientation_pair_angles = subparsers.add_parser(
        "code-wreath-orientation-pair-angles",
        help="Analyze orientation pair principal-angle spectrum.",
    )
    code_wreath_orientation_pair_angles.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_pair_angles.set_defaults(
        func=command_code_wreath_orientation_pair_angles
    )


def command_code_wreath_orientation_pair_angles(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_pair_angle_spectrum_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_pair_angle_spectrum_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Orientation pair principal-angle analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_orientation_pair_angle_spectrum.json"
    )
    print(
        "W4 validations / failures / W5 controls: "
        f"{metrics['complete_w4_pair_angle_validation_count']}/"
        f"{metrics['finite_pair_angle_validation_failure_count']}/"
        f"{metrics['w5_pair_angle_control_count']}"
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


def add_code_wreath_orientation_block_core(subparsers) -> None:
    code_wreath_orientation_block_core = subparsers.add_parser(
        "code-wreath-orientation-block-core",
        help="Analyze orientation block common-core witness structures.",
    )
    code_wreath_orientation_block_core.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_block_core.set_defaults(
        func=command_code_wreath_orientation_block_core
    )


def command_code_wreath_orientation_block_core(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_block_common_core_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_block_common_core_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Orientation block common-core analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_orientation_block_common_core.json"
    )
    print(
        "Witnesses / scaling records / max block rate: "
        f"{metrics['exact_finite_block_common_core_witness_count']}/"
        f"{metrics['scaling_record_count']}/"
        f"{metrics['maximum_observed_block_rate']:.6g}"
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


def add_code_wreath_plancherel_block_obstruction(subparsers) -> None:
    code_wreath_plancherel_block_obstruction = subparsers.add_parser(
        "code-wreath-plancherel-block-obstruction",
        help="Evaluate Sellke covering and Plancherel block norm obstruction.",
    )
    code_wreath_plancherel_block_obstruction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_plancherel_block_obstruction.set_defaults(
        func=command_code_wreath_plancherel_block_obstruction
    )


def command_code_wreath_plancherel_block_obstruction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_plancherel_block_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_plancherel_block_obstruction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Plancherel block norm obstruction analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_plancherel_block_obstruction.json"
    )
    print(
        "Target controls / failures / Sellke theorem count: "
        f"{metrics['residual_target_control_count']}/"
        f"{metrics['residual_target_control_failure_count']}/"
        f"{metrics['sellke_covering_literature_theorem_count']}"
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


def add_code_wreath_spectral_trim(subparsers) -> None:
    code_wreath_spectral_trim = subparsers.add_parser(
        "code-wreath-spectral-trim",
        help="Analyze spectral-trimmed sub-POVM hidden label recovery.",
    )
    code_wreath_spectral_trim.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_spectral_trim.set_defaults(
        func=command_code_wreath_spectral_trim
    )


def command_code_wreath_spectral_trim(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_spectral_trimmed_subpovm_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_spectral_trimmed_subpovm_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Spectral-trimmed sub-POVM analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_spectral_trimmed_subpovm.json"
    )
    print(
        "Trimmed sub-POVM controls / failures / min success bound: "
        f"{metrics['finite_trimmed_subpovm_control_count']}/"
        f"{metrics['finite_trimmed_subpovm_validation_failure_count']}/"
        f"{metrics['minimum_finite_correct_label_success_probability']:.6g}"
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


def add_code_wreath_spectral_filter_degree(subparsers) -> None:
    code_wreath_spectral_filter_degree = subparsers.add_parser(
        "code-wreath-spectral-filter-degree",
        help="Analyze low-pass filter polynomial degree obstructions.",
    )
    code_wreath_spectral_filter_degree.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_spectral_filter_degree.set_defaults(
        func=command_code_wreath_spectral_filter_degree
    )


def command_code_wreath_spectral_filter_degree(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_spectral_filter_degree_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_spectral_filter_degree_obstruction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Spectral filter degree obstruction analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_spectral_filter_degree_obstruction.json"
    )
    print(
        "Scaling records / eval superpoly rows / singular superpoly rows: "
        f"{metrics['scaling_record_count']}/"
        f"{metrics['eigenvalue_encoding_superpolynomial_row_count']}/"
        f"{metrics['singular_value_encoding_superpolynomial_row_count']}"
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


def add_code_wreath_plancherel_block_mass(subparsers) -> None:
    code_wreath_plancherel_block_mass = subparsers.add_parser(
        "code-wreath-plancherel-block-mass",
        help="Analyze Plancherel tensor stationarity and expected block mass.",
    )
    code_wreath_plancherel_block_mass.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_plancherel_block_mass.set_defaults(
        func=command_code_wreath_plancherel_block_mass
    )


def command_code_wreath_plancherel_block_mass(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_plancherel_block_mass_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_plancherel_block_mass_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Plancherel block mass analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_plancherel_block_mass.json"
    )
    print(
        "Stationarity controls / failures / scaling records: "
        f"{metrics['exact_stationarity_control_count']}/"
        f"{metrics['exact_stationarity_failure_count']}/"
        f"{metrics['scaling_record_count']}"
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


def add_code_wreath_orientation_covariant_quotient(subparsers) -> None:
    code_wreath_orientation_covariant_quotient = subparsers.add_parser(
        "code-wreath-orientation-covariant-quotient",
        help="Analyze orientation-covariant quotient scalar-commutant obstructions.",
    )
    code_wreath_orientation_covariant_quotient.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_covariant_quotient.set_defaults(
        func=command_code_wreath_orientation_covariant_quotient
    )


def command_code_wreath_orientation_covariant_quotient(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_covariant_quotient_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_covariant_quotient_obstruction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Orientation covariant quotient obstruction analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_orientation_covariant_quotient_obstruction.json"
    )
    print(
        "Orbit closure controls / failures / max closure fraction: "
        f"{metrics['finite_orbit_closure_control_count']}/"
        f"{metrics['finite_orbit_closure_validation_failure_count']}/"
        f"{metrics['maximum_finite_orbit_closure_fraction']:.6g}"
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


def add_code_wreath_branch_controlled_invariant_filter(subparsers) -> None:
    code_wreath_branch_controlled_invariant_filter = subparsers.add_parser(
        "code-wreath-branch-controlled-invariant-filter",
        help="Analyze branch-controlled physical invariant filter performance.",
    )
    code_wreath_branch_controlled_invariant_filter.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_branch_controlled_invariant_filter.set_defaults(
        func=command_code_wreath_branch_controlled_invariant_filter
    )


def command_code_wreath_branch_controlled_invariant_filter(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_branch_controlled_invariant_filter_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_branch_controlled_invariant_filter_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Branch-controlled invariant filter analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_branch_controlled_invariant_filter.json"
    )
    print(
        "Physical filter controls / failures / min trace retention: "
        f"{metrics['finite_physical_filter_control_count']}/"
        f"{metrics['finite_physical_filter_validation_failure_count']}/"
        f"{metrics['minimum_finite_filtered_trace_retention']:.6g}"
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


def add_code_wreath_block_core_quotient(subparsers) -> None:
    code_wreath_block_core_quotient = subparsers.add_parser(
        "code-wreath-block-core-quotient",
        help="Analyze block common-core algebraic quotient annihilation.",
    )
    code_wreath_block_core_quotient.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_block_core_quotient.set_defaults(
        func=command_code_wreath_block_core_quotient
    )


def command_code_wreath_block_core_quotient(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_block_common_core_quotient_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_block_common_core_quotient_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Block common-core quotient analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_block_common_core_quotient.json"
    )
    print(
        "Quotient controls / failures / scaling records: "
        f"{metrics['finite_quotient_control_count']}/"
        f"{metrics['finite_quotient_validation_failure_count']}/"
        f"{metrics['scaling_record_count']}"
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


def add_code_wreath_paired_block_filter_bypass(subparsers) -> None:
    code_wreath_paired_block_filter_bypass = subparsers.add_parser(
        "code-wreath-paired-block-filter-bypass",
        help="Analyze paired-block self-dual irrep filter bypass.",
    )
    code_wreath_paired_block_filter_bypass.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_paired_block_filter_bypass.set_defaults(
        func=command_code_wreath_paired_block_filter_bypass
    )


def command_code_wreath_paired_block_filter_bypass(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_paired_block_filter_bypass_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_paired_block_filter_bypass_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Paired-block filter bypass analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_paired_block_filter_bypass.json"
    )
    print(
        "Paired-block witnesses / scaling records / target violations: "
        f"{metrics['exact_filtered_paired_block_witness_count']}/"
        f"{metrics['scaling_record_count']}/"
        f"{metrics['finite_target_violation_count']}"
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


def add_code_wreath_local_isotypic_filter_no_go(subparsers) -> None:
    code_wreath_local_isotypic_filter_no_go = subparsers.add_parser(
        "code-wreath-local-isotypic-filter-no-go",
        help="Analyze Plancherel-incidence no-go for block-local isotypic filters.",
    )
    code_wreath_local_isotypic_filter_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_local_isotypic_filter_no_go.set_defaults(
        func=command_code_wreath_local_isotypic_filter_no_go
    )


def command_code_wreath_local_isotypic_filter_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_local_isotypic_filter_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_local_isotypic_filter_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Local isotypic filter no-go analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_local_isotypic_filter_no_go.json"
    )
    print(
        "Incidence controls / failures / scaling records: "
        f"{metrics['finite_incidence_control_count']}/"
        f"{metrics['finite_incidence_validation_failure_count']}/"
        f"{metrics['scaling_record_count']}"
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


def add_code_wreath_cluster_locality_no_go(subparsers) -> None:
    code_wreath_cluster_locality_no_go = subparsers.add_parser(
        "code-wreath-cluster-locality-no-go",
        help="Analyze cluster-locality lower bounds for disjoint product filters.",
    )
    code_wreath_cluster_locality_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_cluster_locality_no_go.set_defaults(
        func=command_code_wreath_cluster_locality_no_go
    )


def command_code_wreath_cluster_locality_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_cluster_locality_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_cluster_locality_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Cluster locality no-go analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_cluster_locality_no_go.json"
    )
    print(
        "Locality thresholds / falsifications / scaling records: "
        f"{metrics['finite_locality_threshold_count']}/"
        f"{metrics['finite_degree_d_falsification_count']}/"
        f"{metrics['finite_scaling_record_count']}"
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


def add_code_wreath_spectral_filter_query_bound(subparsers) -> None:
    code_wreath_spectral_filter_query_bound = subparsers.add_parser(
        "code-wreath-spectral-filter-query-bound",
        help="Analyze search reduction query lower bounds for low-pass filters.",
    )
    code_wreath_spectral_filter_query_bound.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_spectral_filter_query_bound.set_defaults(
        func=command_code_wreath_spectral_filter_query_bound
    )


def command_code_wreath_spectral_filter_query_bound(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_spectral_filter_query_lower_bound_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_spectral_filter_query_lower_bound_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Spectral filter query lower bound analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_spectral_filter_query_lower_bound.json"
    )
    print(
        "Search encoding controls / failures / superpoly rows: "
        f"{metrics['finite_search_encoding_control_count']}/"
        f"{metrics['finite_search_encoding_failure_count']}/"
        f"{metrics['superpolynomial_black_box_lower_bound_row_count']}"
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


def add_code_wreath_affine_core_flag(subparsers) -> None:
    code_wreath_affine_core_flag = subparsers.add_parser(
        "code-wreath-affine-core-flag",
        help="Analyze affine core flag balance and linear routing.",
    )
    code_wreath_affine_core_flag.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_affine_core_flag.set_defaults(
        func=command_code_wreath_affine_core_flag
    )


def command_code_wreath_affine_core_flag(
    args: argparse.Namespace,
) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_affine_core_flag_report
    initialize_seed_registry(overwrite=False)
    payload = write_affine_core_flag_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Affine core flag analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_affine_core_flag_theorem.json"
    )
    print(
        "Incidence controls / matrix controls / matrix failures / block records: "
        f"{metrics['incidence_control_count']}/"
        f"{metrics['matrix_control_count']}/"
        f"{metrics['matrix_validation_failure_count']}/"
        f"{metrics['block_affine_core_record_count']}"
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


def add_code_wreath_affine_node_common_outlier(subparsers) -> None:
    code_wreath_affine_node_common_outlier = subparsers.add_parser(
        "code-wreath-affine-node-common-outlier",
        help="Analyze affine node generated subgroups and common outlier rarity.",
    )
    code_wreath_affine_node_common_outlier.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_affine_node_common_outlier.set_defaults(
        func=command_code_wreath_affine_node_common_outlier
    )


def command_code_wreath_affine_node_common_outlier(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_node_common_outlier_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_node_common_outlier_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Affine node common outlier analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_affine_node_common_outlier.json"
    )
    print(
        "Subgroup controls / failures / physical controls / failures: "
        f"{metrics['subgroup_control_count']}/"
        f"{metrics['subgroup_control_failure_count']}/"
        f"{metrics['physical_control_count']}/"
        f"{metrics['physical_control_failure_count']}"
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


def add_code_wreath_affine_plane_scalar_holonomy(subparsers) -> None:
    code_wreath_affine_plane_scalar_holonomy = subparsers.add_parser(
        "code-wreath-affine-plane-scalar-holonomy",
        help="Analyze scalar affine-plane J3 holonomy positivity.",
    )
    code_wreath_affine_plane_scalar_holonomy.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_affine_plane_scalar_holonomy.set_defaults(
        func=command_code_wreath_affine_plane_scalar_holonomy
    )


def command_code_wreath_affine_plane_scalar_holonomy(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_plane_scalar_holonomy_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_plane_scalar_holonomy_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Affine plane scalar holonomy analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_affine_plane_scalar_holonomy.json"
    )
    print(
        "Scalar plane controls / failures / canonical controls: "
        f"{metrics['scalar_affine_plane_channel_control_count']}/"
        f"{metrics['finite_control_failure_count']}/"
        f"{metrics['canonical_pairing_control_count']}"
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


def add_code_wreath_affine_plane_support_pressure_no_go(subparsers) -> None:
    code_wreath_affine_plane_support_pressure_no_go = subparsers.add_parser(
        "code-wreath-affine-plane-support-pressure-no-go",
        help="Analyze affine plane support demand versus capacity pressure.",
    )
    code_wreath_affine_plane_support_pressure_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_affine_plane_support_pressure_no_go.set_defaults(
        func=command_code_wreath_affine_plane_support_pressure_no_go
    )


def command_code_wreath_affine_plane_support_pressure_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_plane_support_pressure_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_plane_support_pressure_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Affine plane support pressure no-go analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_affine_plane_support_pressure_no_go.json"
    )
    print(
        "Plane controls / failures / pressure capacity failures: "
        f"{metrics['exact_rich_plane_count_control_count']}/"
        f"{metrics['finite_plane_count_control_failure_count']}/"
        f"{metrics['finite_pressure_capacity_failure_count']}"
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


def add_code_wreath_affine_recoupling_bundle(subparsers) -> None:
    code_wreath_affine_recoupling_bundle = subparsers.add_parser(
        "code-wreath-affine-recoupling-bundle",
        help="Analyze affine recoupling flat transport bundle structures.",
    )
    code_wreath_affine_recoupling_bundle.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_affine_recoupling_bundle.set_defaults(
        func=command_code_wreath_affine_recoupling_bundle
    )


def command_code_wreath_affine_recoupling_bundle(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_recoupling_bundle_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_recoupling_bundle_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Affine recoupling bundle analysis complete")
    print(
        "Artifact: research/representation/"
        "self_dual_wreath_affine_recoupling_bundle.json"
    )
    print(
        "Finite controls / failures / scaling records: "
        f"{metrics['finite_control_count']}/"
        f"{metrics['finite_flat_transport_validation_failure_count']}/"
        f"{len(payload['scaling_records'])}"
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


def add_code_wreath_affine_relation_weighted_bulk(subparsers) -> None:
    code_wreath_affine_relation_weighted_bulk = subparsers.add_parser(
        "code-wreath-affine-relation-weighted-bulk",
        help="Analyze code wreath affine relation weighted bulk theorem performance.",
    )
    code_wreath_affine_relation_weighted_bulk.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_affine_relation_weighted_bulk.set_defaults(
        func=command_code_wreath_affine_relation_weighted_bulk
    )


def command_code_wreath_affine_relation_weighted_bulk(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_relation_weighted_bulk_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_relation_weighted_bulk_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Affine Relation Weighted Bulk analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_affine_relation_weighted_bulk.json"
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


def add_code_wreath_affine_star_channel_gap(subparsers) -> None:
    code_wreath_affine_star_channel_gap = subparsers.add_parser(
        "code-wreath-affine-star-channel-gap",
        help="Analyze code wreath affine star channel gap theorem performance.",
    )
    code_wreath_affine_star_channel_gap.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_affine_star_channel_gap.set_defaults(
        func=command_code_wreath_affine_star_channel_gap
    )


def command_code_wreath_affine_star_channel_gap(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_affine_star_channel_gap_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_affine_star_channel_gap_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Affine Star Channel Gap analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_affine_star_channel_gap.json"
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


def add_code_wreath_augmented_h0_dimension_obstruction(subparsers) -> None:
    code_wreath_augmented_h0_dimension_obstruction = subparsers.add_parser(
        "code-wreath-augmented-h0-dimension-obstruction",
        help="Analyze code wreath augmented h0 dimension obstruction theorem performance.",
    )
    code_wreath_augmented_h0_dimension_obstruction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_augmented_h0_dimension_obstruction.set_defaults(
        func=command_code_wreath_augmented_h0_dimension_obstruction
    )


def command_code_wreath_augmented_h0_dimension_obstruction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_augmented_h0_dimension_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_augmented_h0_dimension_obstruction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Augmented H0 Dimension Obstruction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_augmented_h0_dimension_obstruction.json"
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


def add_code_wreath_canonical_coefficient_affine(subparsers) -> None:
    code_wreath_canonical_coefficient_affine = subparsers.add_parser(
        "code-wreath-canonical-coefficient-affine",
        help="Analyze code wreath canonical coefficient affine theorem performance.",
    )
    code_wreath_canonical_coefficient_affine.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_canonical_coefficient_affine.set_defaults(
        func=command_code_wreath_canonical_coefficient_affine
    )


def command_code_wreath_canonical_coefficient_affine(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_canonical_coefficient_affine_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_canonical_coefficient_affine_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Canonical Coefficient Affine analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_canonical_coefficient_affine.json"
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


def add_code_wreath_cayley_fiber_reduction(subparsers) -> None:
    code_wreath_cayley_fiber_reduction = subparsers.add_parser(
        "code-wreath-cayley-fiber-reduction",
        help="Analyze code wreath cayley fiber reduction theorem performance.",
    )
    code_wreath_cayley_fiber_reduction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_cayley_fiber_reduction.set_defaults(
        func=command_code_wreath_cayley_fiber_reduction
    )


def command_code_wreath_cayley_fiber_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_cayley_fiber_reduction
    initialize_seed_registry(overwrite=False)
    payload = write_cayley_fiber_reduction(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Cayley Fiber Reduction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_cayley_fiber_reduction.json"
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


def add_code_wreath_central_support_rank_bridge(subparsers) -> None:
    code_wreath_central_support_rank_bridge = subparsers.add_parser(
        "code-wreath-central-support-rank-bridge",
        help="Analyze code wreath central support rank bridge theorem performance.",
    )
    code_wreath_central_support_rank_bridge.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_central_support_rank_bridge.set_defaults(
        func=command_code_wreath_central_support_rank_bridge
    )


def command_code_wreath_central_support_rank_bridge(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_central_support_rank_bridge_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_central_support_rank_bridge_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Central Support Rank Bridge analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_central_support_rank_bridge.json"
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


def add_code_wreath_coherent_fourier_decoder(subparsers) -> None:
    code_wreath_coherent_fourier_decoder = subparsers.add_parser(
        "code-wreath-coherent-fourier-decoder",
        help="Analyze code wreath coherent fourier decoder theorem performance.",
    )
    code_wreath_coherent_fourier_decoder.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_coherent_fourier_decoder.set_defaults(
        func=command_code_wreath_coherent_fourier_decoder
    )


def command_code_wreath_coherent_fourier_decoder(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_coherent_fourier_decoder_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_coherent_fourier_decoder_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Coherent Fourier Decoder analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_coherent_fourier_decoder.json"
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


def add_code_wreath_collision_free_event_transfer(subparsers) -> None:
    code_wreath_collision_free_event_transfer = subparsers.add_parser(
        "code-wreath-collision-free-event-transfer",
        help="Analyze code wreath collision free event transfer theorem performance.",
    )
    code_wreath_collision_free_event_transfer.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_collision_free_event_transfer.set_defaults(
        func=command_code_wreath_collision_free_event_transfer
    )


def command_code_wreath_collision_free_event_transfer(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_collision_free_event_transfer_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_collision_free_event_transfer_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Collision Free Event Transfer analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_collision_free_event_transfer.json"
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


def add_code_wreath_common_core_polar_bypass(subparsers) -> None:
    code_wreath_common_core_polar_bypass = subparsers.add_parser(
        "code-wreath-common-core-polar-bypass",
        help="Analyze code wreath common core polar bypass theorem performance.",
    )
    code_wreath_common_core_polar_bypass.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_common_core_polar_bypass.set_defaults(
        func=command_code_wreath_common_core_polar_bypass
    )


def command_code_wreath_common_core_polar_bypass(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_common_core_polar_bypass_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_common_core_polar_bypass_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Common Core Polar Bypass analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_common_core_polar_bypass.json"
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


def add_code_wreath_complete_s6_vertex_channel_audit(subparsers) -> None:
    code_wreath_complete_s6_vertex_channel_audit = subparsers.add_parser(
        "code-wreath-complete-s6-vertex-channel-audit",
        help="Analyze code wreath complete s6 vertex channel audit theorem performance.",
    )
    code_wreath_complete_s6_vertex_channel_audit.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_complete_s6_vertex_channel_audit.set_defaults(
        func=command_code_wreath_complete_s6_vertex_channel_audit
    )


def command_code_wreath_complete_s6_vertex_channel_audit(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_complete_s6_vertex_channel_audit_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_complete_s6_vertex_channel_audit_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Complete S6 Vertex Channel Audit analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_complete_s6_vertex_channel_audit.json"
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


def add_code_wreath_component_defect_gap_bridge(subparsers) -> None:
    code_wreath_component_defect_gap_bridge = subparsers.add_parser(
        "code-wreath-component-defect-gap-bridge",
        help="Analyze code wreath component defect gap bridge theorem performance.",
    )
    code_wreath_component_defect_gap_bridge.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_defect_gap_bridge.set_defaults(
        func=command_code_wreath_component_defect_gap_bridge
    )


def command_code_wreath_component_defect_gap_bridge(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_defect_gap_bridge_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_defect_gap_bridge_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Defect Gap Bridge analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_defect_gap_bridge.json"
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


def add_code_wreath_component_povm_regular_master_reduction(subparsers) -> None:
    code_wreath_component_povm_regular_master_reduction = subparsers.add_parser(
        "code-wreath-component-povm-regular-master-reduction",
        help="Analyze code wreath component povm regular master reduction theorem performance.",
    )
    code_wreath_component_povm_regular_master_reduction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_povm_regular_master_reduction.set_defaults(
        func=command_code_wreath_component_povm_regular_master_reduction
    )


def command_code_wreath_component_povm_regular_master_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_povm_regular_master_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_povm_regular_master_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Povm Regular Master Reduction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_povm_regular_master_reduction.json"
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


def add_code_wreath_component_povm_sparse_support_boundary(subparsers) -> None:
    code_wreath_component_povm_sparse_support_boundary = subparsers.add_parser(
        "code-wreath-component-povm-sparse-support-boundary",
        help="Analyze code wreath component povm sparse support boundary theorem performance.",
    )
    code_wreath_component_povm_sparse_support_boundary.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_povm_sparse_support_boundary.set_defaults(
        func=command_code_wreath_component_povm_sparse_support_boundary
    )


def command_code_wreath_component_povm_sparse_support_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_povm_sparse_support_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_povm_sparse_support_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Povm Sparse Support Boundary analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_povm_sparse_support_boundary.json"
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


def add_code_wreath_covariant_pgm_factorization(subparsers) -> None:
    code_wreath_covariant_pgm_factorization = subparsers.add_parser(
        "code-wreath-covariant-pgm-factorization",
        help="Analyze code wreath covariant pgm factorization theorem performance.",
    )
    code_wreath_covariant_pgm_factorization.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_covariant_pgm_factorization.set_defaults(
        func=command_code_wreath_covariant_pgm_factorization
    )


def command_code_wreath_covariant_pgm_factorization(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_covariant_pgm_factorization_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_covariant_pgm_factorization_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Covariant Pgm Factorization analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_covariant_pgm_factorization.json"
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


def add_code_wreath_coverage_welch_pressure(subparsers) -> None:
    code_wreath_coverage_welch_pressure = subparsers.add_parser(
        "code-wreath-coverage-welch-pressure",
        help="Analyze code wreath coverage welch pressure theorem performance.",
    )
    code_wreath_coverage_welch_pressure.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_coverage_welch_pressure.set_defaults(
        func=command_code_wreath_coverage_welch_pressure
    )


def command_code_wreath_coverage_welch_pressure(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_coverage_welch_pressure_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_coverage_welch_pressure_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Coverage Welch Pressure analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_coverage_welch_pressure.json"
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


def add_code_wreath_cross_dependency_neutrality(subparsers) -> None:
    code_wreath_cross_dependency_neutrality = subparsers.add_parser(
        "code-wreath-cross-dependency-neutrality",
        help="Analyze code wreath cross dependency neutrality theorem performance.",
    )
    code_wreath_cross_dependency_neutrality.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_cross_dependency_neutrality.set_defaults(
        func=command_code_wreath_cross_dependency_neutrality
    )


def command_code_wreath_cross_dependency_neutrality(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_cross_dependency_neutrality,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_cross_dependency_neutrality(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Cross Dependency Neutrality analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_cross_dependency_neutrality.json"
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


def add_code_wreath_dependency_homology(subparsers) -> None:
    code_wreath_dependency_homology = subparsers.add_parser(
        "code-wreath-dependency-homology",
        help="Analyze code wreath dependency homology theorem performance.",
    )
    code_wreath_dependency_homology.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_dependency_homology.set_defaults(
        func=command_code_wreath_dependency_homology
    )


def command_code_wreath_dependency_homology(
    args: argparse.Namespace,
) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_dependency_homology
    initialize_seed_registry(overwrite=False)
    payload = write_dependency_homology(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Dependency Homology analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_dependency_homology.json"
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


def add_code_wreath_early_level_overlap_localization(subparsers) -> None:
    code_wreath_early_level_overlap_localization = subparsers.add_parser(
        "code-wreath-early-level-overlap-localization",
        help="Analyze code wreath early level overlap localization theorem performance.",
    )
    code_wreath_early_level_overlap_localization.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_early_level_overlap_localization.set_defaults(
        func=command_code_wreath_early_level_overlap_localization
    )


def command_code_wreath_early_level_overlap_localization(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_early_level_overlap_localization_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_early_level_overlap_localization_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Early Level Overlap Localization analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_early_level_overlap_localization.json"
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


def add_code_wreath_extended_kronecker_threshold(subparsers) -> None:
    code_wreath_extended_kronecker_threshold = subparsers.add_parser(
        "code-wreath-extended-kronecker-threshold",
        help="Analyze code wreath extended kronecker threshold theorem performance.",
    )
    code_wreath_extended_kronecker_threshold.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_extended_kronecker_threshold.set_defaults(
        func=command_code_wreath_extended_kronecker_threshold
    )


def command_code_wreath_extended_kronecker_threshold(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_extended_kronecker_threshold_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_extended_kronecker_threshold_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Extended Kronecker Threshold analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_extended_kronecker_threshold.json"
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


def add_code_wreath_final_root_leverage_edge(subparsers) -> None:
    code_wreath_final_root_leverage_edge = subparsers.add_parser(
        "code-wreath-final-root-leverage-edge",
        help="Analyze code wreath final root leverage edge theorem performance.",
    )
    code_wreath_final_root_leverage_edge.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_final_root_leverage_edge.set_defaults(
        func=command_code_wreath_final_root_leverage_edge
    )


def command_code_wreath_final_root_leverage_edge(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_leverage_edge_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_final_root_leverage_edge_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Final Root Leverage Edge analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_final_root_leverage_edge.json"
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


def add_code_wreath_component_defect_rank_mass(subparsers) -> None:
    code_wreath_component_defect_rank_mass = subparsers.add_parser(
        "code-wreath-component-defect-rank-mass",
        help="Analyze code wreath component defect rank mass theorem performance.",
    )
    code_wreath_component_defect_rank_mass.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_defect_rank_mass.set_defaults(
        func=command_code_wreath_component_defect_rank_mass
    )


def command_code_wreath_component_defect_rank_mass(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_defect_rank_mass_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_defect_rank_mass_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Defect Rank Mass analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_defect_rank_mass.json"
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


def add_code_wreath_component_effect_algebra_boundary(subparsers) -> None:
    code_wreath_component_effect_algebra_boundary = subparsers.add_parser(
        "code-wreath-component-effect-algebra-boundary",
        help="Analyze code wreath component effect algebra boundary theorem performance.",
    )
    code_wreath_component_effect_algebra_boundary.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_effect_algebra_boundary.set_defaults(
        func=command_code_wreath_component_effect_algebra_boundary
    )


def command_code_wreath_component_effect_algebra_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_effect_algebra_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_effect_algebra_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Effect Algebra Boundary analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_effect_algebra_boundary.json"
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


def add_code_wreath_component_povm_spectral_trim(subparsers) -> None:
    code_wreath_component_povm_spectral_trim = subparsers.add_parser(
        "code-wreath-component-povm-spectral-trim",
        help="Analyze code wreath component povm spectral trim theorem performance.",
    )
    code_wreath_component_povm_spectral_trim.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_povm_spectral_trim.set_defaults(
        func=command_code_wreath_component_povm_spectral_trim
    )


def command_code_wreath_component_povm_spectral_trim(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_povm_spectral_trim_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_povm_spectral_trim_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Povm Spectral Trim analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_povm_spectral_trim.json"
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


def add_code_wreath_final_root_natural_common_span(subparsers) -> None:
    code_wreath_final_root_natural_common_span = subparsers.add_parser(
        "code-wreath-final-root-natural-common-span",
        help="Analyze code wreath final root natural common span theorem performance.",
    )
    code_wreath_final_root_natural_common_span.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_final_root_natural_common_span.set_defaults(
        func=command_code_wreath_final_root_natural_common_span
    )


def command_code_wreath_final_root_natural_common_span(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_final_root_natural_common_span_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_final_root_natural_common_span_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Final Root Natural Common Span analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_final_root_natural_common_span.json"
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


def add_code_wreath_fixed_family_common_rank_dilution(subparsers) -> None:
    code_wreath_fixed_family_common_rank_dilution = subparsers.add_parser(
        "code-wreath-fixed-family-common-rank-dilution",
        help="Analyze code wreath fixed family common rank dilution theorem performance.",
    )
    code_wreath_fixed_family_common_rank_dilution.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_fixed_family_common_rank_dilution.set_defaults(
        func=command_code_wreath_fixed_family_common_rank_dilution
    )


def command_code_wreath_fixed_family_common_rank_dilution(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_fixed_family_common_rank_dilution_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_fixed_family_common_rank_dilution_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Fixed Family Common Rank Dilution analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_fixed_family_common_rank_dilution.json"
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


def add_code_wreath_global_carrier_channel_extractor(subparsers) -> None:
    code_wreath_global_carrier_channel_extractor = subparsers.add_parser(
        "code-wreath-global-carrier-channel-extractor",
        help="Analyze code wreath global carrier channel extractor theorem performance.",
    )
    code_wreath_global_carrier_channel_extractor.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_global_carrier_channel_extractor.set_defaults(
        func=command_code_wreath_global_carrier_channel_extractor
    )


def command_code_wreath_global_carrier_channel_extractor(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_global_carrier_channel_extractor_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_global_carrier_channel_extractor_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Global Carrier Channel Extractor analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_global_carrier_channel_extractor.json"
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


def add_code_wreath_global_collision_free_mass(subparsers) -> None:
    code_wreath_global_collision_free_mass = subparsers.add_parser(
        "code-wreath-global-collision-free-mass",
        help="Analyze code wreath global collision free mass theorem performance.",
    )
    code_wreath_global_collision_free_mass.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_global_collision_free_mass.set_defaults(
        func=command_code_wreath_global_collision_free_mass
    )


def command_code_wreath_global_collision_free_mass(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_global_collision_free_mass_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_global_collision_free_mass_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Global Collision Free Mass analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_global_collision_free_mass.json"
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


def add_code_wreath_global_distinct_joint_kernel(subparsers) -> None:
    code_wreath_global_distinct_joint_kernel = subparsers.add_parser(
        "code-wreath-global-distinct-joint-kernel",
        help="Analyze code wreath global distinct joint kernel theorem performance.",
    )
    code_wreath_global_distinct_joint_kernel.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_global_distinct_joint_kernel.set_defaults(
        func=command_code_wreath_global_distinct_joint_kernel
    )


def command_code_wreath_global_distinct_joint_kernel(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_global_distinct_joint_kernel_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_global_distinct_joint_kernel_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Global Distinct Joint Kernel analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_global_distinct_joint_kernel.json"
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


def add_code_wreath_global_partition_collision(subparsers) -> None:
    code_wreath_global_partition_collision = subparsers.add_parser(
        "code-wreath-global-partition-collision",
        help="Analyze code wreath global partition collision theorem performance.",
    )
    code_wreath_global_partition_collision.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_global_partition_collision.set_defaults(
        func=command_code_wreath_global_partition_collision
    )


def command_code_wreath_global_partition_collision(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_global_partition_collision_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_global_partition_collision_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Global Partition Collision analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_global_partition_collision.json"
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


def add_code_wreath_gpe_holonomy_resolver_reduction(subparsers) -> None:
    code_wreath_gpe_holonomy_resolver_reduction = subparsers.add_parser(
        "code-wreath-gpe-holonomy-resolver-reduction",
        help="Analyze code wreath gpe holonomy resolver reduction theorem performance.",
    )
    code_wreath_gpe_holonomy_resolver_reduction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_gpe_holonomy_resolver_reduction.set_defaults(
        func=command_code_wreath_gpe_holonomy_resolver_reduction
    )


def command_code_wreath_gpe_holonomy_resolver_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_gpe_holonomy_resolver_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_gpe_holonomy_resolver_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Gpe Holonomy Resolver Reduction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_gpe_holonomy_resolver_reduction.json"
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


def add_code_wreath_gpe_pair_polar_transport(subparsers) -> None:
    code_wreath_gpe_pair_polar_transport = subparsers.add_parser(
        "code-wreath-gpe-pair-polar-transport",
        help="Analyze code wreath gpe pair polar transport theorem performance.",
    )
    code_wreath_gpe_pair_polar_transport.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_gpe_pair_polar_transport.set_defaults(
        func=command_code_wreath_gpe_pair_polar_transport
    )


def command_code_wreath_gpe_pair_polar_transport(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_gpe_pair_polar_transport_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_gpe_pair_polar_transport_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Gpe Pair Polar Transport analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_gpe_pair_polar_transport.json"
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


def add_code_wreath_gpe_recursive_node_compiler(subparsers) -> None:
    code_wreath_gpe_recursive_node_compiler = subparsers.add_parser(
        "code-wreath-gpe-recursive-node-compiler",
        help="Analyze code wreath gpe recursive node compiler theorem performance.",
    )
    code_wreath_gpe_recursive_node_compiler.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_gpe_recursive_node_compiler.set_defaults(
        func=command_code_wreath_gpe_recursive_node_compiler
    )


def command_code_wreath_gpe_recursive_node_compiler(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_gpe_recursive_node_compiler_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_gpe_recursive_node_compiler_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Gpe Recursive Node Compiler analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_gpe_recursive_node_compiler.json"
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


def add_code_wreath_graded_channel_graph_reduction(subparsers) -> None:
    code_wreath_graded_channel_graph_reduction = subparsers.add_parser(
        "code-wreath-graded-channel-graph-reduction",
        help="Analyze code wreath graded channel graph reduction theorem performance.",
    )
    code_wreath_graded_channel_graph_reduction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_graded_channel_graph_reduction.set_defaults(
        func=command_code_wreath_graded_channel_graph_reduction
    )


def command_code_wreath_graded_channel_graph_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_graded_channel_graph_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_graded_channel_graph_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Graded Channel Graph Reduction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_graded_channel_graph_reduction.json"
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


def add_code_wreath_graded_flat_transport_no_go(subparsers) -> None:
    code_wreath_graded_flat_transport_no_go = subparsers.add_parser(
        "code-wreath-graded-flat-transport-no-go",
        help="Analyze code wreath graded flat transport no go theorem performance.",
    )
    code_wreath_graded_flat_transport_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_graded_flat_transport_no_go.set_defaults(
        func=command_code_wreath_graded_flat_transport_no_go
    )


def command_code_wreath_graded_flat_transport_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_graded_flat_transport_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_graded_flat_transport_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Graded Flat Transport No Go analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_graded_flat_transport_no_go.json"
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


def add_code_wreath_graded_frobenius_trim(subparsers) -> None:
    code_wreath_graded_frobenius_trim = subparsers.add_parser(
        "code-wreath-graded-frobenius-trim",
        help="Analyze code wreath graded frobenius trim theorem performance.",
    )
    code_wreath_graded_frobenius_trim.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_graded_frobenius_trim.set_defaults(
        func=command_code_wreath_graded_frobenius_trim
    )


def command_code_wreath_graded_frobenius_trim(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_graded_frobenius_trim_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_graded_frobenius_trim_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Graded Frobenius Trim analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_graded_frobenius_trim.json"
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


def add_code_wreath_hamming_stratum_rank_transition(subparsers) -> None:
    code_wreath_hamming_stratum_rank_transition = subparsers.add_parser(
        "code-wreath-hamming-stratum-rank-transition",
        help="Analyze code wreath hamming stratum rank transition theorem performance.",
    )
    code_wreath_hamming_stratum_rank_transition.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_hamming_stratum_rank_transition.set_defaults(
        func=command_code_wreath_hamming_stratum_rank_transition
    )


def command_code_wreath_hamming_stratum_rank_transition(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hamming_stratum_rank_transition_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_hamming_stratum_rank_transition_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Hamming Stratum Rank Transition analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_hamming_stratum_rank_transition.json"
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


def add_code_wreath_hierarchical_cokernel_resolution(subparsers) -> None:
    code_wreath_hierarchical_cokernel_resolution = subparsers.add_parser(
        "code-wreath-hierarchical-cokernel-resolution",
        help="Analyze code wreath hierarchical cokernel resolution theorem performance.",
    )
    code_wreath_hierarchical_cokernel_resolution.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_hierarchical_cokernel_resolution.set_defaults(
        func=command_code_wreath_hierarchical_cokernel_resolution
    )


def command_code_wreath_hierarchical_cokernel_resolution(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hierarchical_cokernel_resolution_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_hierarchical_cokernel_resolution_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Hierarchical Cokernel Resolution analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_hierarchical_cokernel_resolution.json"
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


def add_code_wreath_hierarchical_polar_tree(subparsers) -> None:
    code_wreath_hierarchical_polar_tree = subparsers.add_parser(
        "code-wreath-hierarchical-polar-tree",
        help="Analyze code wreath hierarchical polar tree theorem performance.",
    )
    code_wreath_hierarchical_polar_tree.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_hierarchical_polar_tree.set_defaults(
        func=command_code_wreath_hierarchical_polar_tree
    )


def command_code_wreath_hierarchical_polar_tree(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hierarchical_polar_tree_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_hierarchical_polar_tree_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Hierarchical Polar Tree analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_hierarchical_polar_tree.json"
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


def add_code_wreath_hierarchy_low_carrier_trim(subparsers) -> None:
    code_wreath_hierarchy_low_carrier_trim = subparsers.add_parser(
        "code-wreath-hierarchy-low-carrier-trim",
        help="Analyze code wreath hierarchy low carrier trim theorem performance.",
    )
    code_wreath_hierarchy_low_carrier_trim.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_hierarchy_low_carrier_trim.set_defaults(
        func=command_code_wreath_hierarchy_low_carrier_trim
    )


def command_code_wreath_hierarchy_low_carrier_trim(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hierarchy_low_carrier_trim_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_hierarchy_low_carrier_trim_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Hierarchy Low Carrier Trim analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_hierarchy_low_carrier_trim.json"
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


def add_code_wreath_hierarchy_pair_common_rank_budget(subparsers) -> None:
    code_wreath_hierarchy_pair_common_rank_budget = subparsers.add_parser(
        "code-wreath-hierarchy-pair-common-rank-budget",
        help="Analyze code wreath hierarchy pair common rank budget theorem performance.",
    )
    code_wreath_hierarchy_pair_common_rank_budget.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_hierarchy_pair_common_rank_budget.set_defaults(
        func=command_code_wreath_hierarchy_pair_common_rank_budget
    )


def command_code_wreath_hierarchy_pair_common_rank_budget(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_hierarchy_pair_common_rank_budget_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_hierarchy_pair_common_rank_budget_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Hierarchy Pair Common Rank Budget analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_hierarchy_pair_common_rank_budget.json"
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


def add_code_wreath_internal_closure_graded_rescue(subparsers) -> None:
    code_wreath_internal_closure_graded_rescue = subparsers.add_parser(
        "code-wreath-internal-closure-graded-rescue",
        help="Analyze code wreath internal closure graded rescue theorem performance.",
    )
    code_wreath_internal_closure_graded_rescue.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_internal_closure_graded_rescue.set_defaults(
        func=command_code_wreath_internal_closure_graded_rescue
    )


def command_code_wreath_internal_closure_graded_rescue(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_internal_closure_graded_rescue_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_internal_closure_graded_rescue_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Internal Closure Graded Rescue analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_internal_closure_graded_rescue.json"
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


def add_code_wreath_interplane_gauge_homology(subparsers) -> None:
    code_wreath_interplane_gauge_homology = subparsers.add_parser(
        "code-wreath-interplane-gauge-homology",
        help="Analyze code wreath interplane gauge homology theorem performance.",
    )
    code_wreath_interplane_gauge_homology.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_interplane_gauge_homology.set_defaults(
        func=command_code_wreath_interplane_gauge_homology
    )


def command_code_wreath_interplane_gauge_homology(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_interplane_gauge_homology_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_interplane_gauge_homology_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Interplane Gauge Homology analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_interplane_gauge_homology.json"
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


def add_code_wreath_invariant_projector_circuit(subparsers) -> None:
    code_wreath_invariant_projector_circuit = subparsers.add_parser(
        "code-wreath-invariant-projector-circuit",
        help="Analyze code wreath invariant projector circuit theorem performance.",
    )
    code_wreath_invariant_projector_circuit.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_invariant_projector_circuit.set_defaults(
        func=command_code_wreath_invariant_projector_circuit
    )


def command_code_wreath_invariant_projector_circuit(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_invariant_projector_circuit_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_invariant_projector_circuit_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Invariant Projector Circuit analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_invariant_projector_circuit.json"
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


def add_code_wreath_isotypic_dephasing_no_go(subparsers) -> None:
    code_wreath_isotypic_dephasing_no_go = subparsers.add_parser(
        "code-wreath-isotypic-dephasing-no-go",
        help="Analyze code wreath isotypic dephasing no go theorem performance.",
    )
    code_wreath_isotypic_dephasing_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_isotypic_dephasing_no_go.set_defaults(
        func=command_code_wreath_isotypic_dephasing_no_go
    )


def command_code_wreath_isotypic_dephasing_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_isotypic_dephasing_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_isotypic_dephasing_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Isotypic Dephasing No Go analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_isotypic_dephasing_no_go.json"
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


def add_code_wreath_leaf_whitening_commutator_no_go(subparsers) -> None:
    code_wreath_leaf_whitening_commutator_no_go = subparsers.add_parser(
        "code-wreath-leaf-whitening-commutator-no-go",
        help="Analyze code wreath leaf whitening commutator no go theorem performance.",
    )
    code_wreath_leaf_whitening_commutator_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_leaf_whitening_commutator_no_go.set_defaults(
        func=command_code_wreath_leaf_whitening_commutator_no_go
    )


def command_code_wreath_leaf_whitening_commutator_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_leaf_whitening_commutator_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_leaf_whitening_commutator_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Leaf Whitening Commutator No Go analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_leaf_whitening_commutator_no_go.json"
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


def add_code_wreath_level_three_flag_audit(subparsers) -> None:
    code_wreath_level_three_flag_audit = subparsers.add_parser(
        "code-wreath-level-three-flag-audit",
        help="Analyze code wreath level three flag audit theorem performance.",
    )
    code_wreath_level_three_flag_audit.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_level_three_flag_audit.set_defaults(
        func=command_code_wreath_level_three_flag_audit
    )


def command_code_wreath_level_three_flag_audit(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_level_three_flag_audit_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_level_three_flag_audit_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Level Three Flag Audit analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_level_three_flag_audit.json"
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


def add_code_wreath_local_pair_transversality(subparsers) -> None:
    code_wreath_local_pair_transversality = subparsers.add_parser(
        "code-wreath-local-pair-transversality",
        help="Analyze code wreath local pair transversality theorem performance.",
    )
    code_wreath_local_pair_transversality.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_local_pair_transversality.set_defaults(
        func=command_code_wreath_local_pair_transversality
    )


def command_code_wreath_local_pair_transversality(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_local_pair_transversality_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_local_pair_transversality_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Local Pair Transversality analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_local_pair_transversality.json"
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


def add_code_wreath_matrix_cayley_boundary(subparsers) -> None:
    code_wreath_matrix_cayley_boundary = subparsers.add_parser(
        "code-wreath-matrix-cayley-boundary",
        help="Analyze code wreath matrix cayley boundary theorem performance.",
    )
    code_wreath_matrix_cayley_boundary.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_matrix_cayley_boundary.set_defaults(
        func=command_code_wreath_matrix_cayley_boundary
    )


def command_code_wreath_matrix_cayley_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_matrix_cayley_boundary
    initialize_seed_registry(overwrite=False)
    payload = write_matrix_cayley_boundary(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Matrix Cayley Boundary analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_matrix_cayley_boundary.json"
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


def add_code_wreath_matrix_povm_recursive_compiler(subparsers) -> None:
    code_wreath_matrix_povm_recursive_compiler = subparsers.add_parser(
        "code-wreath-matrix-povm-recursive-compiler",
        help="Analyze code wreath matrix povm recursive compiler theorem performance.",
    )
    code_wreath_matrix_povm_recursive_compiler.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_matrix_povm_recursive_compiler.set_defaults(
        func=command_code_wreath_matrix_povm_recursive_compiler
    )


def command_code_wreath_matrix_povm_recursive_compiler(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_matrix_povm_recursive_compiler_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_matrix_povm_recursive_compiler_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Matrix Povm Recursive Compiler analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_matrix_povm_recursive_compiler.json"
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


def add_code_wreath_mixed_covariant_decoder(subparsers) -> None:
    code_wreath_mixed_covariant_decoder = subparsers.add_parser(
        "code-wreath-mixed-covariant-decoder",
        help="Analyze code wreath mixed covariant decoder theorem performance.",
    )
    code_wreath_mixed_covariant_decoder.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_mixed_covariant_decoder.set_defaults(
        func=command_code_wreath_mixed_covariant_decoder
    )


def command_code_wreath_mixed_covariant_decoder(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_mixed_covariant_decoder_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_mixed_covariant_decoder_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Mixed Covariant Decoder analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_mixed_covariant_decoder.json"
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


def add_code_wreath_common_span_component_universality_no_go(subparsers) -> None:
    code_wreath_common_span_component_universality_no_go = subparsers.add_parser(
        "code-wreath-common-span-component-universality-no-go",
        help="Analyze code wreath common span component universality no go theorem performance.",
    )
    code_wreath_common_span_component_universality_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_common_span_component_universality_no_go.set_defaults(
        func=command_code_wreath_common_span_component_universality_no_go
    )


def command_code_wreath_common_span_component_universality_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_common_span_component_universality_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_common_span_component_universality_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Common Span Component Universality No Go analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_common_span_component_universality_no_go.json"
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


def add_code_wreath_mrs_coherence_escape_criterion(subparsers) -> None:
    code_wreath_mrs_coherence_escape_criterion = subparsers.add_parser(
        "code-wreath-mrs-coherence-escape-criterion",
        help="Analyze code wreath mrs coherence escape criterion theorem performance.",
    )
    code_wreath_mrs_coherence_escape_criterion.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_mrs_coherence_escape_criterion.set_defaults(
        func=command_code_wreath_mrs_coherence_escape_criterion
    )


def command_code_wreath_mrs_coherence_escape_criterion(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_mrs_coherence_escape_criterion_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_mrs_coherence_escape_criterion_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Mrs Coherence Escape Criterion analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_mrs_coherence_escape_criterion.json"
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


def add_code_wreath_mrs_transcript_povm_separation(subparsers) -> None:
    code_wreath_mrs_transcript_povm_separation = subparsers.add_parser(
        "code-wreath-mrs-transcript-povm-separation",
        help="Analyze code wreath mrs transcript povm separation theorem performance.",
    )
    code_wreath_mrs_transcript_povm_separation.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_mrs_transcript_povm_separation.set_defaults(
        func=command_code_wreath_mrs_transcript_povm_separation
    )


def command_code_wreath_mrs_transcript_povm_separation(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_mrs_transcript_povm_separation_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_mrs_transcript_povm_separation_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Mrs Transcript Povm Separation analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_mrs_transcript_povm_separation.json"
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


def add_code_wreath_multiscale_polar_schedule(subparsers) -> None:
    code_wreath_multiscale_polar_schedule = subparsers.add_parser(
        "code-wreath-multiscale-polar-schedule",
        help="Analyze code wreath multiscale polar schedule theorem performance.",
    )
    code_wreath_multiscale_polar_schedule.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_multiscale_polar_schedule.set_defaults(
        func=command_code_wreath_multiscale_polar_schedule
    )


def command_code_wreath_multiscale_polar_schedule(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_multiscale_polar_schedule_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_multiscale_polar_schedule_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Multiscale Polar Schedule analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_multiscale_polar_schedule.json"
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


def add_code_wreath_native_frame_access_boundary(subparsers) -> None:
    code_wreath_native_frame_access_boundary = subparsers.add_parser(
        "code-wreath-native-frame-access-boundary",
        help="Analyze code wreath native frame access boundary theorem performance.",
    )
    code_wreath_native_frame_access_boundary.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_native_frame_access_boundary.set_defaults(
        func=command_code_wreath_native_frame_access_boundary
    )


def command_code_wreath_native_frame_access_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_native_frame_access_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_native_frame_access_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Native Frame Access Boundary analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_native_frame_access_boundary.json"
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


def add_code_wreath_natural_leaf_commutator_mass(subparsers) -> None:
    code_wreath_natural_leaf_commutator_mass = subparsers.add_parser(
        "code-wreath-natural-leaf-commutator-mass",
        help="Analyze code wreath natural leaf commutator mass theorem performance.",
    )
    code_wreath_natural_leaf_commutator_mass.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_natural_leaf_commutator_mass.set_defaults(
        func=command_code_wreath_natural_leaf_commutator_mass
    )


def command_code_wreath_natural_leaf_commutator_mass(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_leaf_commutator_mass_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_natural_leaf_commutator_mass_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Natural Leaf Commutator Mass analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_natural_leaf_commutator_mass.json"
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


def add_code_wreath_natural_pair_carrier_law(subparsers) -> None:
    code_wreath_natural_pair_carrier_law = subparsers.add_parser(
        "code-wreath-natural-pair-carrier-law",
        help="Analyze code wreath natural pair carrier law theorem performance.",
    )
    code_wreath_natural_pair_carrier_law.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_natural_pair_carrier_law.set_defaults(
        func=command_code_wreath_natural_pair_carrier_law
    )


def command_code_wreath_natural_pair_carrier_law(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_pair_carrier_law_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_natural_pair_carrier_law_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Natural Pair Carrier Law analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_natural_pair_carrier_law.json"
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


def add_code_wreath_operator_steiner_bulk_reduction(subparsers) -> None:
    code_wreath_operator_steiner_bulk_reduction = subparsers.add_parser(
        "code-wreath-operator-steiner-bulk-reduction",
        help="Analyze code wreath operator steiner bulk reduction theorem performance.",
    )
    code_wreath_operator_steiner_bulk_reduction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_operator_steiner_bulk_reduction.set_defaults(
        func=command_code_wreath_operator_steiner_bulk_reduction
    )


def command_code_wreath_operator_steiner_bulk_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_operator_steiner_bulk_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_operator_steiner_bulk_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Operator Steiner Bulk Reduction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_operator_steiner_bulk_reduction.json"
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


def add_code_wreath_orientation_filter_physical_access(subparsers) -> None:
    code_wreath_orientation_filter_physical_access = subparsers.add_parser(
        "code-wreath-orientation-filter-physical-access",
        help="Analyze code wreath orientation filter physical access theorem performance.",
    )
    code_wreath_orientation_filter_physical_access.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_filter_physical_access.set_defaults(
        func=command_code_wreath_orientation_filter_physical_access
    )


def command_code_wreath_orientation_filter_physical_access(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_filter_physical_access_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_filter_physical_access_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Orientation Filter Physical Access analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_orientation_filter_physical_access.json"
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


def add_code_wreath_orientation_rank_budget(subparsers) -> None:
    code_wreath_orientation_rank_budget = subparsers.add_parser(
        "code-wreath-orientation-rank-budget",
        help="Analyze code wreath orientation rank budget theorem performance.",
    )
    code_wreath_orientation_rank_budget.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_rank_budget.set_defaults(
        func=command_code_wreath_orientation_rank_budget
    )


def command_code_wreath_orientation_rank_budget(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_rank_budget_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_rank_budget_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Orientation Rank Budget analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_orientation_rank_budget.json"
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


def add_code_wreath_orientation_retention_theorem(subparsers) -> None:
    code_wreath_orientation_retention_theorem = subparsers.add_parser(
        "code-wreath-orientation-retention-theorem",
        help="Analyze code wreath orientation retention theorem theorem performance.",
    )
    code_wreath_orientation_retention_theorem.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_retention_theorem.set_defaults(
        func=command_code_wreath_orientation_retention_theorem
    )


def command_code_wreath_orientation_retention_theorem(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_retention_theorem_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_retention_theorem_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Orientation Retention Theorem analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_orientation_retention_theorem.json"
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


def add_code_wreath_orientation_subspace_filter(subparsers) -> None:
    code_wreath_orientation_subspace_filter = subparsers.add_parser(
        "code-wreath-orientation-subspace-filter",
        help="Analyze code wreath orientation subspace filter theorem performance.",
    )
    code_wreath_orientation_subspace_filter.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_orientation_subspace_filter.set_defaults(
        func=command_code_wreath_orientation_subspace_filter
    )


def command_code_wreath_orientation_subspace_filter(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_orientation_subspace_filter_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_orientation_subspace_filter_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Orientation Subspace Filter analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_orientation_subspace_filter.json"
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


def add_code_wreath_pair_common_covering_transition(subparsers) -> None:
    code_wreath_pair_common_covering_transition = subparsers.add_parser(
        "code-wreath-pair-common-covering-transition",
        help="Analyze code wreath pair common covering transition theorem performance.",
    )
    code_wreath_pair_common_covering_transition.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_common_covering_transition.set_defaults(
        func=command_code_wreath_pair_common_covering_transition
    )


def command_code_wreath_pair_common_covering_transition(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_common_covering_transition_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pair_common_covering_transition_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pair Common Covering Transition analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pair_common_covering_transition.json"
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


def add_code_wreath_pair_core_rank_concentration(subparsers) -> None:
    code_wreath_pair_core_rank_concentration = subparsers.add_parser(
        "code-wreath-pair-core-rank-concentration",
        help="Analyze code wreath pair core rank concentration theorem performance.",
    )
    code_wreath_pair_core_rank_concentration.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_core_rank_concentration.set_defaults(
        func=command_code_wreath_pair_core_rank_concentration
    )


def command_code_wreath_pair_core_rank_concentration(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_core_rank_concentration_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pair_core_rank_concentration_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pair Core Rank Concentration analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pair_core_rank_concentration.json"
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


def add_code_wreath_pair_polar_sampler(subparsers) -> None:
    code_wreath_pair_polar_sampler = subparsers.add_parser(
        "code-wreath-pair-polar-sampler",
        help="Analyze code wreath pair polar sampler theorem performance.",
    )
    code_wreath_pair_polar_sampler.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_polar_sampler.set_defaults(
        func=command_code_wreath_pair_polar_sampler
    )


def command_code_wreath_pair_polar_sampler(
    args: argparse.Namespace,
) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_pair_polar_sampler_report
    initialize_seed_registry(overwrite=False)
    payload = write_pair_polar_sampler_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pair Polar Sampler analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pair_polar_sampler.json"
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


def add_code_wreath_pair_polar_transport_network(subparsers) -> None:
    code_wreath_pair_polar_transport_network = subparsers.add_parser(
        "code-wreath-pair-polar-transport-network",
        help="Analyze code wreath pair polar transport network theorem performance.",
    )
    code_wreath_pair_polar_transport_network.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_polar_transport_network.set_defaults(
        func=command_code_wreath_pair_polar_transport_network
    )


def command_code_wreath_pair_polar_transport_network(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_polar_transport_network_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pair_polar_transport_network_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pair Polar Transport Network analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pair_polar_transport_network.json"
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


def add_code_wreath_pair_transport_degree_obstruction(subparsers) -> None:
    code_wreath_pair_transport_degree_obstruction = subparsers.add_parser(
        "code-wreath-pair-transport-degree-obstruction",
        help="Analyze code wreath pair transport degree obstruction theorem performance.",
    )
    code_wreath_pair_transport_degree_obstruction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_transport_degree_obstruction.set_defaults(
        func=command_code_wreath_pair_transport_degree_obstruction
    )


def command_code_wreath_pair_transport_degree_obstruction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_transport_degree_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pair_transport_degree_obstruction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pair Transport Degree Obstruction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pair_transport_degree_obstruction.json"
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


def add_code_wreath_pair_transport_native_mass_boundary(subparsers) -> None:
    code_wreath_pair_transport_native_mass_boundary = subparsers.add_parser(
        "code-wreath-pair-transport-native-mass-boundary",
        help="Analyze code wreath pair transport native mass boundary theorem performance.",
    )
    code_wreath_pair_transport_native_mass_boundary.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pair_transport_native_mass_boundary.set_defaults(
        func=command_code_wreath_pair_transport_native_mass_boundary
    )


def command_code_wreath_pair_transport_native_mass_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pair_transport_native_mass_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pair_transport_native_mass_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pair Transport Native Mass Boundary analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pair_transport_native_mass_boundary.json"
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


def add_code_wreath_partial_support_child_embedding(subparsers) -> None:
    code_wreath_partial_support_child_embedding = subparsers.add_parser(
        "code-wreath-partial-support-child-embedding",
        help="Analyze code wreath partial support child embedding theorem performance.",
    )
    code_wreath_partial_support_child_embedding.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_partial_support_child_embedding.set_defaults(
        func=command_code_wreath_partial_support_child_embedding
    )


def command_code_wreath_partial_support_child_embedding(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_partial_support_child_embedding_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_partial_support_child_embedding_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Partial Support Child Embedding analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_partial_support_child_embedding.json"
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


def add_code_wreath_partial_support_source_mass_boundary(subparsers) -> None:
    code_wreath_partial_support_source_mass_boundary = subparsers.add_parser(
        "code-wreath-partial-support-source-mass-boundary",
        help="Analyze code wreath partial support source mass boundary theorem performance.",
    )
    code_wreath_partial_support_source_mass_boundary.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_partial_support_source_mass_boundary.set_defaults(
        func=command_code_wreath_partial_support_source_mass_boundary
    )


def command_code_wreath_partial_support_source_mass_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_partial_support_source_mass_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_partial_support_source_mass_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Partial Support Source Mass Boundary analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_partial_support_source_mass_boundary.json"
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


def add_code_wreath_boolean_graph_stopping_core_pressure(subparsers) -> None:
    code_wreath_boolean_graph_stopping_core_pressure = subparsers.add_parser(
        "code-wreath-boolean-graph-stopping-core-pressure",
        help="Analyze code wreath boolean graph stopping core pressure theorem performance.",
    )
    code_wreath_boolean_graph_stopping_core_pressure.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_boolean_graph_stopping_core_pressure.set_defaults(
        func=command_code_wreath_boolean_graph_stopping_core_pressure
    )


def command_code_wreath_boolean_graph_stopping_core_pressure(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_boolean_graph_stopping_core_pressure_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_boolean_graph_stopping_core_pressure_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Boolean Graph Stopping Core Pressure analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_boolean_graph_stopping_core_pressure.json"
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


def add_code_wreath_component_aggregate_frame_indeterminacy(subparsers) -> None:
    code_wreath_component_aggregate_frame_indeterminacy = subparsers.add_parser(
        "code-wreath-component-aggregate-frame-indeterminacy",
        help="Analyze code wreath component aggregate frame indeterminacy theorem performance.",
    )
    code_wreath_component_aggregate_frame_indeterminacy.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_aggregate_frame_indeterminacy.set_defaults(
        func=command_code_wreath_component_aggregate_frame_indeterminacy
    )


def command_code_wreath_component_aggregate_frame_indeterminacy(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_aggregate_frame_indeterminacy_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_aggregate_frame_indeterminacy_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Aggregate Frame Indeterminacy analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_aggregate_frame_indeterminacy.json"
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


def add_code_wreath_component_commutator_collision_free_transfer(subparsers) -> None:
    code_wreath_component_commutator_collision_free_transfer = subparsers.add_parser(
        "code-wreath-component-commutator-collision-free-transfer",
        help="Analyze code wreath component commutator collision free transfer theorem performance.",
    )
    code_wreath_component_commutator_collision_free_transfer.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_commutator_collision_free_transfer.set_defaults(
        func=command_code_wreath_component_commutator_collision_free_transfer
    )


def command_code_wreath_component_commutator_collision_free_transfer(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_commutator_collision_free_transfer_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_commutator_collision_free_transfer_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Commutator Collision Free Transfer analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_commutator_collision_free_transfer.json"
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


def add_code_wreath_component_commutator_haar_benchmark(subparsers) -> None:
    code_wreath_component_commutator_haar_benchmark = subparsers.add_parser(
        "code-wreath-component-commutator-haar-benchmark",
        help="Analyze code wreath component commutator haar benchmark theorem performance.",
    )
    code_wreath_component_commutator_haar_benchmark.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_commutator_haar_benchmark.set_defaults(
        func=command_code_wreath_component_commutator_haar_benchmark
    )


def command_code_wreath_component_commutator_haar_benchmark(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_commutator_haar_benchmark_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_commutator_haar_benchmark_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Commutator Haar Benchmark analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_commutator_haar_benchmark.json"
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


def add_code_wreath_component_commutator_trace_mass_bridge(subparsers) -> None:
    code_wreath_component_commutator_trace_mass_bridge = subparsers.add_parser(
        "code-wreath-component-commutator-trace-mass-bridge",
        help="Analyze code wreath component commutator trace mass bridge theorem performance.",
    )
    code_wreath_component_commutator_trace_mass_bridge.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_commutator_trace_mass_bridge.set_defaults(
        func=command_code_wreath_component_commutator_trace_mass_bridge
    )


def command_code_wreath_component_commutator_trace_mass_bridge(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_commutator_trace_mass_bridge_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_commutator_trace_mass_bridge_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Commutator Trace Mass Bridge analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_commutator_trace_mass_bridge.json"
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


def add_code_wreath_component_green_ridge_stability(subparsers) -> None:
    code_wreath_component_green_ridge_stability = subparsers.add_parser(
        "code-wreath-component-green-ridge-stability",
        help="Analyze code wreath component green ridge stability theorem performance.",
    )
    code_wreath_component_green_ridge_stability.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_green_ridge_stability.set_defaults(
        func=command_code_wreath_component_green_ridge_stability
    )


def command_code_wreath_component_green_ridge_stability(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_green_ridge_stability_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_green_ridge_stability_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Green Ridge Stability analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_green_ridge_stability.json"
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


def add_code_wreath_component_hamming_orbit_reduction(subparsers) -> None:
    code_wreath_component_hamming_orbit_reduction = subparsers.add_parser(
        "code-wreath-component-hamming-orbit-reduction",
        help="Analyze code wreath component hamming orbit reduction theorem performance.",
    )
    code_wreath_component_hamming_orbit_reduction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_hamming_orbit_reduction.set_defaults(
        func=command_code_wreath_component_hamming_orbit_reduction
    )


def command_code_wreath_component_hamming_orbit_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_hamming_orbit_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_hamming_orbit_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Hamming Orbit Reduction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_hamming_orbit_reduction.json"
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


def add_code_wreath_component_leaf_resolved_green_normal_form(subparsers) -> None:
    code_wreath_component_leaf_resolved_green_normal_form = subparsers.add_parser(
        "code-wreath-component-leaf-resolved-green-normal-form",
        help="Analyze code wreath component leaf resolved green normal form theorem performance.",
    )
    code_wreath_component_leaf_resolved_green_normal_form.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_component_leaf_resolved_green_normal_form.set_defaults(
        func=command_code_wreath_component_leaf_resolved_green_normal_form
    )


def command_code_wreath_component_leaf_resolved_green_normal_form(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_component_leaf_resolved_green_normal_form_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_component_leaf_resolved_green_normal_form_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Component Leaf Resolved Green Normal Form analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_component_leaf_resolved_green_normal_form.json"
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


def add_code_wreath_contiguous_all_a_support_pressure(subparsers) -> None:
    code_wreath_contiguous_all_a_support_pressure = subparsers.add_parser(
        "code-wreath-contiguous-all-a-support-pressure",
        help="Analyze code wreath contiguous all a support pressure theorem performance.",
    )
    code_wreath_contiguous_all_a_support_pressure.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_contiguous_all_a_support_pressure.set_defaults(
        func=command_code_wreath_contiguous_all_a_support_pressure
    )


def command_code_wreath_contiguous_all_a_support_pressure(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_contiguous_all_a_support_pressure_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_contiguous_all_a_support_pressure_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Contiguous All A Support Pressure analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_contiguous_all_a_support_pressure.json"
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


def add_code_wreath_contiguous_frame_target_factorization(subparsers) -> None:
    code_wreath_contiguous_frame_target_factorization = subparsers.add_parser(
        "code-wreath-contiguous-frame-target-factorization",
        help="Analyze code wreath contiguous frame target factorization theorem performance.",
    )
    code_wreath_contiguous_frame_target_factorization.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_contiguous_frame_target_factorization.set_defaults(
        func=command_code_wreath_contiguous_frame_target_factorization
    )


def command_code_wreath_contiguous_frame_target_factorization(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_contiguous_frame_target_factorization_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_contiguous_frame_target_factorization_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Contiguous Frame Target Factorization analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_contiguous_frame_target_factorization.json"
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


def add_code_wreath_exceptional_block_graph_core_pressure(subparsers) -> None:
    code_wreath_exceptional_block_graph_core_pressure = subparsers.add_parser(
        "code-wreath-exceptional-block-graph-core-pressure",
        help="Analyze code wreath exceptional block graph core pressure theorem performance.",
    )
    code_wreath_exceptional_block_graph_core_pressure.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_exceptional_block_graph_core_pressure.set_defaults(
        func=command_code_wreath_exceptional_block_graph_core_pressure
    )


def command_code_wreath_exceptional_block_graph_core_pressure(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_exceptional_block_graph_core_pressure_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_exceptional_block_graph_core_pressure_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Exceptional Block Graph Core Pressure analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_exceptional_block_graph_core_pressure.json"
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


def add_code_wreath_frame_subword_entropy(subparsers) -> None:
    code_wreath_frame_subword_entropy = subparsers.add_parser(
        "code-wreath-frame-subword-entropy",
        help="Analyze code wreath frame subword entropy theorem performance.",
    )
    code_wreath_frame_subword_entropy.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_frame_subword_entropy.set_defaults(
        func=command_code_wreath_frame_subword_entropy
    )


def command_code_wreath_frame_subword_entropy(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_frame_subword_entropy_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_frame_subword_entropy_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Frame Subword Entropy analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_frame_subword_entropy.json"
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


def add_code_wreath_leaf_marked_green_word_normal_form(subparsers) -> None:
    code_wreath_leaf_marked_green_word_normal_form = subparsers.add_parser(
        "code-wreath-leaf-marked-green-word-normal-form",
        help="Analyze code wreath leaf marked green word normal form theorem performance.",
    )
    code_wreath_leaf_marked_green_word_normal_form.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_leaf_marked_green_word_normal_form.set_defaults(
        func=command_code_wreath_leaf_marked_green_word_normal_form
    )


def command_code_wreath_leaf_marked_green_word_normal_form(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_leaf_marked_green_word_normal_form_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_leaf_marked_green_word_normal_form_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Leaf Marked Green Word Normal Form analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_leaf_marked_green_word_normal_form.json"
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


def add_code_wreath_linear_code_support_pressure(subparsers) -> None:
    code_wreath_linear_code_support_pressure = subparsers.add_parser(
        "code-wreath-linear-code-support-pressure",
        help="Analyze code wreath linear code support pressure theorem performance.",
    )
    code_wreath_linear_code_support_pressure.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_linear_code_support_pressure.set_defaults(
        func=command_code_wreath_linear_code_support_pressure
    )


def command_code_wreath_linear_code_support_pressure(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_linear_code_support_pressure_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_linear_code_support_pressure_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Linear Code Support Pressure analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_linear_code_support_pressure.json"
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


def add_code_wreath_marked_pressure_obstruction_search(subparsers) -> None:
    code_wreath_marked_pressure_obstruction_search = subparsers.add_parser(
        "code-wreath-marked-pressure-obstruction-search",
        help="Analyze code wreath marked pressure obstruction search theorem performance.",
    )
    code_wreath_marked_pressure_obstruction_search.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_marked_pressure_obstruction_search.set_defaults(
        func=command_code_wreath_marked_pressure_obstruction_search
    )


def command_code_wreath_marked_pressure_obstruction_search(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_marked_pressure_obstruction_search_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_marked_pressure_obstruction_search_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Marked Pressure Obstruction Search analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_marked_pressure_obstruction_search.json"
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


def add_code_wreath_marked_relation_topology(subparsers) -> None:
    code_wreath_marked_relation_topology = subparsers.add_parser(
        "code-wreath-marked-relation-topology",
        help="Analyze code wreath marked relation topology theorem performance.",
    )
    code_wreath_marked_relation_topology.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_marked_relation_topology.set_defaults(
        func=command_code_wreath_marked_relation_topology
    )


def command_code_wreath_marked_relation_topology(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_marked_relation_topology_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_marked_relation_topology_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Marked Relation Topology analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_marked_relation_topology.json"
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


def add_code_wreath_mixed_split_target_genus(subparsers) -> None:
    code_wreath_mixed_split_target_genus = subparsers.add_parser(
        "code-wreath-mixed-split-target-genus",
        help="Analyze code wreath mixed split target genus theorem performance.",
    )
    code_wreath_mixed_split_target_genus.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_mixed_split_target_genus.set_defaults(
        func=command_code_wreath_mixed_split_target_genus
    )


def command_code_wreath_mixed_split_target_genus(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_mixed_split_target_genus_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_mixed_split_target_genus_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Mixed Split Target Genus analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_mixed_split_target_genus.json"
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


def add_code_wreath_natural_leaf_commutator_trace_profile(subparsers) -> None:
    code_wreath_natural_leaf_commutator_trace_profile = subparsers.add_parser(
        "code-wreath-natural-leaf-commutator-trace-profile",
        help="Analyze code wreath natural leaf commutator trace profile theorem performance.",
    )
    code_wreath_natural_leaf_commutator_trace_profile.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_natural_leaf_commutator_trace_profile.set_defaults(
        func=command_code_wreath_natural_leaf_commutator_trace_profile
    )


def command_code_wreath_natural_leaf_commutator_trace_profile(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_natural_leaf_commutator_trace_profile_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_natural_leaf_commutator_trace_profile_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Natural Leaf Commutator Trace Profile analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_natural_leaf_commutator_trace_profile.json"
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


def add_code_wreath_parity_stopping_core_pressure(subparsers) -> None:
    code_wreath_parity_stopping_core_pressure = subparsers.add_parser(
        "code-wreath-parity-stopping-core-pressure",
        help="Analyze code wreath parity stopping core pressure theorem performance.",
    )
    code_wreath_parity_stopping_core_pressure.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_parity_stopping_core_pressure.set_defaults(
        func=command_code_wreath_parity_stopping_core_pressure
    )


def command_code_wreath_parity_stopping_core_pressure(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_parity_stopping_core_pressure_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_parity_stopping_core_pressure_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Parity Stopping Core Pressure analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_parity_stopping_core_pressure.json"
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


def add_code_wreath_periodic_frame_fiber_counterfamily(subparsers) -> None:
    code_wreath_periodic_frame_fiber_counterfamily = subparsers.add_parser(
        "code-wreath-periodic-frame-fiber-counterfamily",
        help="Analyze code wreath periodic frame fiber counterfamily theorem performance.",
    )
    code_wreath_periodic_frame_fiber_counterfamily.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_periodic_frame_fiber_counterfamily.set_defaults(
        func=command_code_wreath_periodic_frame_fiber_counterfamily
    )


def command_code_wreath_periodic_frame_fiber_counterfamily(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_periodic_frame_fiber_counterfamily_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_periodic_frame_fiber_counterfamily_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Periodic Frame Fiber Counterfamily analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_periodic_frame_fiber_counterfamily.json"
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


def add_code_wreath_high_codimension_face_word_frontier(subparsers) -> None:
    code_wreath_high_codimension_face_word_frontier = subparsers.add_parser(
        "code-wreath-high-codimension-face-word-frontier",
        help="Analyze code wreath high codimension face word frontier theorem performance.",
    )
    code_wreath_high_codimension_face_word_frontier.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_high_codimension_face_word_frontier.set_defaults(
        func=command_code_wreath_high_codimension_face_word_frontier
    )


def command_code_wreath_high_codimension_face_word_frontier(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_high_codimension_face_word_frontier_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_high_codimension_face_word_frontier_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath High Codimension Face Word Frontier analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_high_codimension_face_word_frontier.json"
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


def add_code_wreath_periodic_frame_rank_collapse(subparsers) -> None:
    code_wreath_periodic_frame_rank_collapse = subparsers.add_parser(
        "code-wreath-periodic-frame-rank-collapse",
        help="Analyze code wreath periodic frame rank collapse theorem performance.",
    )
    code_wreath_periodic_frame_rank_collapse.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_periodic_frame_rank_collapse.set_defaults(
        func=command_code_wreath_periodic_frame_rank_collapse
    )


def command_code_wreath_periodic_frame_rank_collapse(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_periodic_frame_rank_collapse_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_periodic_frame_rank_collapse_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Periodic Frame Rank Collapse analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_periodic_frame_rank_collapse.json"
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


def add_code_wreath_petz_pgm_obstruction(subparsers) -> None:
    code_wreath_petz_pgm_obstruction = subparsers.add_parser(
        "code-wreath-petz-pgm-obstruction",
        help="Analyze code wreath petz pgm obstruction theorem performance.",
    )
    code_wreath_petz_pgm_obstruction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_petz_pgm_obstruction.set_defaults(
        func=command_code_wreath_petz_pgm_obstruction
    )


def command_code_wreath_petz_pgm_obstruction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_petz_pgm_obstruction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_petz_pgm_obstruction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Petz Pgm Obstruction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_petz_pgm_obstruction.json"
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


def add_code_wreath_pgm_quantum_sampling_reduction(subparsers) -> None:
    code_wreath_pgm_quantum_sampling_reduction = subparsers.add_parser(
        "code-wreath-pgm-quantum-sampling-reduction",
        help="Analyze code wreath pgm quantum sampling reduction theorem performance.",
    )
    code_wreath_pgm_quantum_sampling_reduction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pgm_quantum_sampling_reduction.set_defaults(
        func=command_code_wreath_pgm_quantum_sampling_reduction
    )


def command_code_wreath_pgm_quantum_sampling_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pgm_quantum_sampling_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pgm_quantum_sampling_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pgm Quantum Sampling Reduction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pgm_quantum_sampling_reduction.json"
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


def add_code_wreath_pgm_spectral_window(subparsers) -> None:
    code_wreath_pgm_spectral_window = subparsers.add_parser(
        "code-wreath-pgm-spectral-window",
        help="Analyze code wreath pgm spectral window theorem performance.",
    )
    code_wreath_pgm_spectral_window.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pgm_spectral_window.set_defaults(
        func=command_code_wreath_pgm_spectral_window
    )


def command_code_wreath_pgm_spectral_window(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pgm_spectral_window_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pgm_spectral_window_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pgm Spectral Window analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pgm_spectral_window.json"
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


def add_code_wreath_pgm_success_theorem(subparsers) -> None:
    code_wreath_pgm_success_theorem = subparsers.add_parser(
        "code-wreath-pgm-success-theorem",
        help="Analyze code wreath pgm success theorem theorem performance.",
    )
    code_wreath_pgm_success_theorem.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pgm_success_theorem.set_defaults(
        func=command_code_wreath_pgm_success_theorem
    )


def command_code_wreath_pgm_success_theorem(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pgm_success_theorem_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pgm_success_theorem_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pgm Success Theorem analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pgm_success_theorem.json"
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


def add_code_wreath_pgm_truncation_robustness(subparsers) -> None:
    code_wreath_pgm_truncation_robustness = subparsers.add_parser(
        "code-wreath-pgm-truncation-robustness",
        help="Analyze code wreath pgm truncation robustness theorem performance.",
    )
    code_wreath_pgm_truncation_robustness.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_pgm_truncation_robustness.set_defaults(
        func=command_code_wreath_pgm_truncation_robustness
    )


def command_code_wreath_pgm_truncation_robustness(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_pgm_truncation_robustness_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_pgm_truncation_robustness_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Pgm Truncation Robustness analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_pgm_truncation_robustness.json"
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


def add_code_wreath_physical_orientation_interference(subparsers) -> None:
    code_wreath_physical_orientation_interference = subparsers.add_parser(
        "code-wreath-physical-orientation-interference",
        help="Analyze code wreath physical orientation interference theorem performance.",
    )
    code_wreath_physical_orientation_interference.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_physical_orientation_interference.set_defaults(
        func=command_code_wreath_physical_orientation_interference
    )


def command_code_wreath_physical_orientation_interference(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_physical_orientation_interference_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_physical_orientation_interference_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Physical Orientation Interference analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_physical_orientation_interference.json"
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


def add_code_wreath_physical_pgm_intertwiner(subparsers) -> None:
    code_wreath_physical_pgm_intertwiner = subparsers.add_parser(
        "code-wreath-physical-pgm-intertwiner",
        help="Analyze code wreath physical pgm intertwiner theorem performance.",
    )
    code_wreath_physical_pgm_intertwiner.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_physical_pgm_intertwiner.set_defaults(
        func=command_code_wreath_physical_pgm_intertwiner
    )


def command_code_wreath_physical_pgm_intertwiner(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_physical_pgm_intertwiner_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_physical_pgm_intertwiner_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Physical Pgm Intertwiner analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_physical_pgm_intertwiner.json"
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


def add_code_wreath_plancherel_kronecker_positivity(subparsers) -> None:
    code_wreath_plancherel_kronecker_positivity = subparsers.add_parser(
        "code-wreath-plancherel-kronecker-positivity",
        help="Analyze code wreath plancherel kronecker positivity theorem performance.",
    )
    code_wreath_plancherel_kronecker_positivity.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_plancherel_kronecker_positivity.set_defaults(
        func=command_code_wreath_plancherel_kronecker_positivity
    )


def command_code_wreath_plancherel_kronecker_positivity(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_plancherel_kronecker_positivity_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_plancherel_kronecker_positivity_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Plancherel Kronecker Positivity analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_plancherel_kronecker_positivity.json"
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


def add_code_wreath_polar_factor_transfer(subparsers) -> None:
    code_wreath_polar_factor_transfer = subparsers.add_parser(
        "code-wreath-polar-factor-transfer",
        help="Analyze code wreath polar factor transfer theorem performance.",
    )
    code_wreath_polar_factor_transfer.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_polar_factor_transfer.set_defaults(
        func=command_code_wreath_polar_factor_transfer
    )


def command_code_wreath_polar_factor_transfer(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_polar_factor_transfer_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_polar_factor_transfer_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Polar Factor Transfer analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_polar_factor_transfer.json"
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


def add_code_wreath_postfilter_frame_compression(subparsers) -> None:
    code_wreath_postfilter_frame_compression = subparsers.add_parser(
        "code-wreath-postfilter-frame-compression",
        help="Analyze code wreath postfilter frame compression theorem performance.",
    )
    code_wreath_postfilter_frame_compression.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_postfilter_frame_compression.set_defaults(
        func=command_code_wreath_postfilter_frame_compression
    )


def command_code_wreath_postfilter_frame_compression(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_postfilter_frame_compression_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_postfilter_frame_compression_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Postfilter Frame Compression analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_postfilter_frame_compression.json"
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


def add_code_wreath_random_steiner_gauge_edge(subparsers) -> None:
    code_wreath_random_steiner_gauge_edge = subparsers.add_parser(
        "code-wreath-random-steiner-gauge-edge",
        help="Analyze code wreath random steiner gauge edge theorem performance.",
    )
    code_wreath_random_steiner_gauge_edge.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_random_steiner_gauge_edge.set_defaults(
        func=command_code_wreath_random_steiner_gauge_edge
    )


def command_code_wreath_random_steiner_gauge_edge(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_random_steiner_gauge_edge_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_random_steiner_gauge_edge_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Random Steiner Gauge Edge analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_random_steiner_gauge_edge.json"
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


def add_code_wreath_reciprocal_carrier_accumulation_no_go(subparsers) -> None:
    code_wreath_reciprocal_carrier_accumulation_no_go = subparsers.add_parser(
        "code-wreath-reciprocal-carrier-accumulation-no-go",
        help="Analyze code wreath reciprocal carrier accumulation no go theorem performance.",
    )
    code_wreath_reciprocal_carrier_accumulation_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_reciprocal_carrier_accumulation_no_go.set_defaults(
        func=command_code_wreath_reciprocal_carrier_accumulation_no_go
    )


def command_code_wreath_reciprocal_carrier_accumulation_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_reciprocal_carrier_accumulation_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_reciprocal_carrier_accumulation_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Reciprocal Carrier Accumulation No Go analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_reciprocal_carrier_accumulation_no_go.json"
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


def add_code_wreath_regular_master_central_support(subparsers) -> None:
    code_wreath_regular_master_central_support = subparsers.add_parser(
        "code-wreath-regular-master-central-support",
        help="Analyze code wreath regular master central support theorem performance.",
    )
    code_wreath_regular_master_central_support.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_regular_master_central_support.set_defaults(
        func=command_code_wreath_regular_master_central_support
    )


def command_code_wreath_regular_master_central_support(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_regular_master_central_support_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_regular_master_central_support_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Regular Master Central Support analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_regular_master_central_support.json"
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


def add_code_wreath_relation_cokernel_transfer(subparsers) -> None:
    code_wreath_relation_cokernel_transfer = subparsers.add_parser(
        "code-wreath-relation-cokernel-transfer",
        help="Analyze code wreath relation cokernel transfer theorem performance.",
    )
    code_wreath_relation_cokernel_transfer.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_relation_cokernel_transfer.set_defaults(
        func=command_code_wreath_relation_cokernel_transfer
    )


def command_code_wreath_relation_cokernel_transfer(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_relation_cokernel_transfer_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_relation_cokernel_transfer_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Relation Cokernel Transfer analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_relation_cokernel_transfer.json"
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


def add_code_wreath_relative_effect_intersection(subparsers) -> None:
    code_wreath_relative_effect_intersection = subparsers.add_parser(
        "code-wreath-relative-effect-intersection",
        help="Analyze code wreath relative effect intersection theorem performance.",
    )
    code_wreath_relative_effect_intersection.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_relative_effect_intersection.set_defaults(
        func=command_code_wreath_relative_effect_intersection
    )


def command_code_wreath_relative_effect_intersection(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_relative_effect_intersection_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_relative_effect_intersection_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Relative Effect Intersection analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_relative_effect_intersection.json"
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


def add_code_wreath_relative_surface_factorization(subparsers) -> None:
    code_wreath_relative_surface_factorization = subparsers.add_parser(
        "code-wreath-relative-surface-factorization",
        help="Analyze code wreath relative surface factorization theorem performance.",
    )
    code_wreath_relative_surface_factorization.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_relative_surface_factorization.set_defaults(
        func=command_code_wreath_relative_surface_factorization
    )


def command_code_wreath_relative_surface_factorization(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_relative_surface_factorization_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_relative_surface_factorization_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Relative Surface Factorization analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_relative_surface_factorization.json"
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


def add_code_wreath_residual_frobenius_typicality(subparsers) -> None:
    code_wreath_residual_frobenius_typicality = subparsers.add_parser(
        "code-wreath-residual-frobenius-typicality",
        help="Analyze code wreath residual frobenius typicality theorem performance.",
    )
    code_wreath_residual_frobenius_typicality.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_residual_frobenius_typicality.set_defaults(
        func=command_code_wreath_residual_frobenius_typicality
    )


def command_code_wreath_residual_frobenius_typicality(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_residual_frobenius_typicality_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_residual_frobenius_typicality_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Residual Frobenius Typicality analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_residual_frobenius_typicality.json"
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


def add_code_wreath_sector_weight_concentration(subparsers) -> None:
    code_wreath_sector_weight_concentration = subparsers.add_parser(
        "code-wreath-sector-weight-concentration",
        help="Analyze code wreath sector weight concentration theorem performance.",
    )
    code_wreath_sector_weight_concentration.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_sector_weight_concentration.set_defaults(
        func=command_code_wreath_sector_weight_concentration
    )


def command_code_wreath_sector_weight_concentration(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sector_weight_concentration_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_sector_weight_concentration_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Sector Weight Concentration analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_sector_weight_concentration.json"
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


def add_code_wreath_shorted_overlap_balance(subparsers) -> None:
    code_wreath_shorted_overlap_balance = subparsers.add_parser(
        "code-wreath-shorted-overlap-balance",
        help="Analyze code wreath shorted overlap balance theorem performance.",
    )
    code_wreath_shorted_overlap_balance.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_shorted_overlap_balance.set_defaults(
        func=command_code_wreath_shorted_overlap_balance
    )


def command_code_wreath_shorted_overlap_balance(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_shorted_overlap_balance_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_shorted_overlap_balance_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Shorted Overlap Balance analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_shorted_overlap_balance.json"
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


def add_code_wreath_sibling_frame_jacobi_surrogate(subparsers) -> None:
    code_wreath_sibling_frame_jacobi_surrogate = subparsers.add_parser(
        "code-wreath-sibling-frame-jacobi-surrogate",
        help="Analyze code wreath sibling frame jacobi surrogate theorem performance.",
    )
    code_wreath_sibling_frame_jacobi_surrogate.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_sibling_frame_jacobi_surrogate.set_defaults(
        func=command_code_wreath_sibling_frame_jacobi_surrogate
    )


def command_code_wreath_sibling_frame_jacobi_surrogate(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sibling_frame_jacobi_surrogate_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_sibling_frame_jacobi_surrogate_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Sibling Frame Jacobi Surrogate analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_sibling_frame_jacobi_surrogate.json"
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


def add_code_wreath_sibling_frame_joint_conditioning_surrogate(subparsers) -> None:
    code_wreath_sibling_frame_joint_conditioning_surrogate = subparsers.add_parser(
        "code-wreath-sibling-frame-joint-conditioning-surrogate",
        help="Analyze code wreath sibling frame joint conditioning surrogate theorem performance.",
    )
    code_wreath_sibling_frame_joint_conditioning_surrogate.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_sibling_frame_joint_conditioning_surrogate.set_defaults(
        func=command_code_wreath_sibling_frame_joint_conditioning_surrogate
    )


def command_code_wreath_sibling_frame_joint_conditioning_surrogate(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sibling_frame_joint_conditioning_surrogate_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_sibling_frame_joint_conditioning_surrogate_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Sibling Frame Joint Conditioning Surrogate analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_sibling_frame_joint_conditioning_surrogate.json"
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


def add_code_wreath_sibling_frame_joint_freeness(subparsers) -> None:
    code_wreath_sibling_frame_joint_freeness = subparsers.add_parser(
        "code-wreath-sibling-frame-joint-freeness",
        help="Analyze code wreath sibling frame joint freeness theorem performance.",
    )
    code_wreath_sibling_frame_joint_freeness.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_sibling_frame_joint_freeness.set_defaults(
        func=command_code_wreath_sibling_frame_joint_freeness
    )


def command_code_wreath_sibling_frame_joint_freeness(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sibling_frame_joint_freeness_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_sibling_frame_joint_freeness_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Sibling Frame Joint Freeness analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_sibling_frame_joint_freeness.json"
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


def add_code_wreath_sibling_frame_mp_moments(subparsers) -> None:
    code_wreath_sibling_frame_mp_moments = subparsers.add_parser(
        "code-wreath-sibling-frame-mp-moments",
        help="Analyze code wreath sibling frame mp moments theorem performance.",
    )
    code_wreath_sibling_frame_mp_moments.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_sibling_frame_mp_moments.set_defaults(
        func=command_code_wreath_sibling_frame_mp_moments
    )


def command_code_wreath_sibling_frame_mp_moments(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sibling_frame_mp_moment_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_sibling_frame_mp_moment_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Sibling Frame Mp Moments analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_sibling_frame_mp_moments.json"
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


def add_code_wreath_sibling_word_map_normal_form(subparsers) -> None:
    code_wreath_sibling_word_map_normal_form = subparsers.add_parser(
        "code-wreath-sibling-word-map-normal-form",
        help="Analyze code wreath sibling word map normal form theorem performance.",
    )
    code_wreath_sibling_word_map_normal_form.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_sibling_word_map_normal_form.set_defaults(
        func=command_code_wreath_sibling_word_map_normal_form
    )


def command_code_wreath_sibling_word_map_normal_form(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sibling_word_map_normal_form_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_sibling_word_map_normal_form_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Sibling Word Map Normal Form analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_sibling_word_map_normal_form.json"
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


def add_code_wreath_signed_steiner_bulk_edge(subparsers) -> None:
    code_wreath_signed_steiner_bulk_edge = subparsers.add_parser(
        "code-wreath-signed-steiner-bulk-edge",
        help="Analyze code wreath signed steiner bulk edge theorem performance.",
    )
    code_wreath_signed_steiner_bulk_edge.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_signed_steiner_bulk_edge.set_defaults(
        func=command_code_wreath_signed_steiner_bulk_edge
    )


def command_code_wreath_signed_steiner_bulk_edge(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_signed_steiner_bulk_edge_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_signed_steiner_bulk_edge_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Signed Steiner Bulk Edge analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_signed_steiner_bulk_edge.json"
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


def add_code_wreath_signed_steiner_incidence_boundary(subparsers) -> None:
    code_wreath_signed_steiner_incidence_boundary = subparsers.add_parser(
        "code-wreath-signed-steiner-incidence-boundary",
        help="Analyze code wreath signed steiner incidence boundary theorem performance.",
    )
    code_wreath_signed_steiner_incidence_boundary.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_signed_steiner_incidence_boundary.set_defaults(
        func=command_code_wreath_signed_steiner_incidence_boundary
    )


def command_code_wreath_signed_steiner_incidence_boundary(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_signed_steiner_incidence_boundary_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_signed_steiner_incidence_boundary_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Signed Steiner Incidence Boundary analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_signed_steiner_incidence_boundary.json"
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


def add_code_wreath_signed_steiner_nullity_theorem(subparsers) -> None:
    code_wreath_signed_steiner_nullity_theorem = subparsers.add_parser(
        "code-wreath-signed-steiner-nullity-theorem",
        help="Analyze code wreath signed steiner nullity theorem theorem performance.",
    )
    code_wreath_signed_steiner_nullity_theorem.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_signed_steiner_nullity_theorem.set_defaults(
        func=command_code_wreath_signed_steiner_nullity_theorem
    )


def command_code_wreath_signed_steiner_nullity_theorem(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_signed_steiner_nullity_theorem_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_signed_steiner_nullity_theorem_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Signed Steiner Nullity Theorem analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_signed_steiner_nullity_theorem.json"
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


def add_code_wreath_single_anchor_shorting(subparsers) -> None:
    code_wreath_single_anchor_shorting = subparsers.add_parser(
        "code-wreath-single-anchor-shorting",
        help="Analyze code wreath single anchor shorting theorem performance.",
    )
    code_wreath_single_anchor_shorting.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_single_anchor_shorting.set_defaults(
        func=command_code_wreath_single_anchor_shorting
    )


def command_code_wreath_single_anchor_shorting(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_single_anchor_shorting_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_single_anchor_shorting_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Single Anchor Shorting analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_single_anchor_shorting.json"
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


def add_code_wreath_sparse_invariant_dependency(subparsers) -> None:
    code_wreath_sparse_invariant_dependency = subparsers.add_parser(
        "code-wreath-sparse-invariant-dependency",
        help="Analyze code wreath sparse invariant dependency theorem performance.",
    )
    code_wreath_sparse_invariant_dependency.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_sparse_invariant_dependency.set_defaults(
        func=command_code_wreath_sparse_invariant_dependency
    )


def command_code_wreath_sparse_invariant_dependency(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_sparse_invariant_dependency,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_sparse_invariant_dependency(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Sparse Invariant Dependency analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_sparse_invariant_dependency.json"
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


def add_code_wreath_star_channel_mass_typicality(subparsers) -> None:
    code_wreath_star_channel_mass_typicality = subparsers.add_parser(
        "code-wreath-star-channel-mass-typicality",
        help="Analyze code wreath star channel mass typicality theorem performance.",
    )
    code_wreath_star_channel_mass_typicality.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_star_channel_mass_typicality.set_defaults(
        func=command_code_wreath_star_channel_mass_typicality
    )


def command_code_wreath_star_channel_mass_typicality(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_star_channel_mass_typicality_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_star_channel_mass_typicality_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Star Channel Mass Typicality analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_star_channel_mass_typicality.json"
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


def add_code_wreath_subgroup_pair_angle_no_go(subparsers) -> None:
    code_wreath_subgroup_pair_angle_no_go = subparsers.add_parser(
        "code-wreath-subgroup-pair-angle-no-go",
        help="Analyze code wreath subgroup pair angle no go theorem performance.",
    )
    code_wreath_subgroup_pair_angle_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_subgroup_pair_angle_no_go.set_defaults(
        func=command_code_wreath_subgroup_pair_angle_no_go
    )


def command_code_wreath_subgroup_pair_angle_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_subgroup_pair_angle_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_subgroup_pair_angle_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Subgroup Pair Angle No Go analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_subgroup_pair_angle_no_go.json"
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


def add_code_wreath_subgroup_projection_walk(subparsers) -> None:
    code_wreath_subgroup_projection_walk = subparsers.add_parser(
        "code-wreath-subgroup-projection-walk",
        help="Analyze code wreath subgroup projection walk theorem performance.",
    )
    code_wreath_subgroup_projection_walk.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_subgroup_projection_walk.set_defaults(
        func=command_code_wreath_subgroup_projection_walk
    )


def command_code_wreath_subgroup_projection_walk(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_subgroup_projection_walk_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_subgroup_projection_walk_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Subgroup Projection Walk analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_subgroup_projection_walk.json"
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


def add_code_wreath_support_affine_rank_entropy(subparsers) -> None:
    code_wreath_support_affine_rank_entropy = subparsers.add_parser(
        "code-wreath-support-affine-rank-entropy",
        help="Analyze code wreath support affine rank entropy theorem performance.",
    )
    code_wreath_support_affine_rank_entropy.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_support_affine_rank_entropy.set_defaults(
        func=command_code_wreath_support_affine_rank_entropy
    )


def command_code_wreath_support_affine_rank_entropy(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_support_affine_rank_entropy_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_support_affine_rank_entropy_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Support Affine Rank Entropy analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_support_affine_rank_entropy.json"
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


def add_code_wreath_support_difference_peeling_no_go(subparsers) -> None:
    code_wreath_support_difference_peeling_no_go = subparsers.add_parser(
        "code-wreath-support-difference-peeling-no-go",
        help="Analyze code wreath support difference peeling no go theorem performance.",
    )
    code_wreath_support_difference_peeling_no_go.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_support_difference_peeling_no_go.set_defaults(
        func=command_code_wreath_support_difference_peeling_no_go
    )


def command_code_wreath_support_difference_peeling_no_go(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_support_difference_peeling_no_go_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_support_difference_peeling_no_go_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Support Difference Peeling No Go analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_support_difference_peeling_no_go.json"
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


def add_code_wreath_target_survival_surface_seed(subparsers) -> None:
    code_wreath_target_survival_surface_seed = subparsers.add_parser(
        "code-wreath-target-survival-surface-seed",
        help="Analyze code wreath target survival surface seed theorem performance.",
    )
    code_wreath_target_survival_surface_seed.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_target_survival_surface_seed.set_defaults(
        func=command_code_wreath_target_survival_surface_seed
    )


def command_code_wreath_target_survival_surface_seed(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_target_survival_surface_seed_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_target_survival_surface_seed_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Target Survival Surface Seed analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_target_survival_surface_seed.json"
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


def add_code_wreath_trace_polynomial_edge_burden(subparsers) -> None:
    code_wreath_trace_polynomial_edge_burden = subparsers.add_parser(
        "code-wreath-trace-polynomial-edge-burden",
        help="Analyze code wreath trace polynomial edge burden theorem performance.",
    )
    code_wreath_trace_polynomial_edge_burden.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_trace_polynomial_edge_burden.set_defaults(
        func=command_code_wreath_trace_polynomial_edge_burden
    )


def command_code_wreath_trace_polynomial_edge_burden(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_trace_polynomial_edge_burden_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_trace_polynomial_edge_burden_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Trace Polynomial Edge Burden analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_trace_polynomial_edge_burden.json"
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


def add_code_wreath_trace_weighted_pgm_bridge(subparsers) -> None:
    code_wreath_trace_weighted_pgm_bridge = subparsers.add_parser(
        "code-wreath-trace-weighted-pgm-bridge",
        help="Analyze code wreath trace weighted pgm bridge theorem performance.",
    )
    code_wreath_trace_weighted_pgm_bridge.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_trace_weighted_pgm_bridge.set_defaults(
        func=command_code_wreath_trace_weighted_pgm_bridge
    )


def command_code_wreath_trace_weighted_pgm_bridge(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_trace_weighted_pgm_bridge_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_trace_weighted_pgm_bridge_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Trace Weighted Pgm Bridge analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_trace_weighted_pgm_bridge.json"
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


def add_code_wreath_trace_weighted_polar_truncation(subparsers) -> None:
    code_wreath_trace_weighted_polar_truncation = subparsers.add_parser(
        "code-wreath-trace-weighted-polar-truncation",
        help="Analyze code wreath trace weighted polar truncation theorem performance.",
    )
    code_wreath_trace_weighted_polar_truncation.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_trace_weighted_polar_truncation.set_defaults(
        func=command_code_wreath_trace_weighted_polar_truncation
    )


def command_code_wreath_trace_weighted_polar_truncation(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_trace_weighted_polar_truncation_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_trace_weighted_polar_truncation_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Trace Weighted Polar Truncation analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_trace_weighted_polar_truncation.json"
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


def add_code_wreath_transport_carrier_mass(subparsers) -> None:
    code_wreath_transport_carrier_mass = subparsers.add_parser(
        "code-wreath-transport-carrier-mass",
        help="Analyze code wreath transport carrier mass theorem performance.",
    )
    code_wreath_transport_carrier_mass.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_transport_carrier_mass.set_defaults(
        func=command_code_wreath_transport_carrier_mass
    )


def command_code_wreath_transport_carrier_mass(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_transport_carrier_mass_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_transport_carrier_mass_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Transport Carrier Mass analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_transport_carrier_mass.json"
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


def add_code_wreath_two_color_return_walk(subparsers) -> None:
    code_wreath_two_color_return_walk = subparsers.add_parser(
        "code-wreath-two-color-return-walk",
        help="Analyze code wreath two color return walk theorem performance.",
    )
    code_wreath_two_color_return_walk.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_two_color_return_walk.set_defaults(
        func=command_code_wreath_two_color_return_walk
    )


def command_code_wreath_two_color_return_walk(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_two_color_return_walk_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_two_color_return_walk_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Two Color Return Walk analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_two_color_return_walk.json"
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


def add_code_wreath_two_partition_ribbon_surface(subparsers) -> None:
    code_wreath_two_partition_ribbon_surface = subparsers.add_parser(
        "code-wreath-two-partition-ribbon-surface",
        help="Analyze code wreath two partition ribbon surface theorem performance.",
    )
    code_wreath_two_partition_ribbon_surface.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_two_partition_ribbon_surface.set_defaults(
        func=command_code_wreath_two_partition_ribbon_surface
    )


def command_code_wreath_two_partition_ribbon_surface(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_two_partition_ribbon_surface_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_two_partition_ribbon_surface_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Two Partition Ribbon Surface analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_two_partition_ribbon_surface.json"
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


def add_code_wreath_uniform_orientation_rank_concentration(subparsers) -> None:
    code_wreath_uniform_orientation_rank_concentration = subparsers.add_parser(
        "code-wreath-uniform-orientation-rank-concentration",
        help="Analyze code wreath uniform orientation rank concentration theorem performance.",
    )
    code_wreath_uniform_orientation_rank_concentration.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_uniform_orientation_rank_concentration.set_defaults(
        func=command_code_wreath_uniform_orientation_rank_concentration
    )


def command_code_wreath_uniform_orientation_rank_concentration(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_uniform_orientation_rank_concentration_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_uniform_orientation_rank_concentration_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Uniform Orientation Rank Concentration analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_uniform_orientation_rank_concentration.json"
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


def add_code_wreath_vertex_channel_groupoid(subparsers) -> None:
    code_wreath_vertex_channel_groupoid = subparsers.add_parser(
        "code-wreath-vertex-channel-groupoid",
        help="Analyze code wreath vertex channel groupoid theorem performance.",
    )
    code_wreath_vertex_channel_groupoid.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_vertex_channel_groupoid.set_defaults(
        func=command_code_wreath_vertex_channel_groupoid
    )


def command_code_wreath_vertex_channel_groupoid(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_vertex_channel_groupoid_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_vertex_channel_groupoid_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Vertex Channel Groupoid analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_vertex_channel_groupoid.json"
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


def add_code_wreath_vertex_kernel_graded_reduction(subparsers) -> None:
    code_wreath_vertex_kernel_graded_reduction = subparsers.add_parser(
        "code-wreath-vertex-kernel-graded-reduction",
        help="Analyze code wreath vertex kernel graded reduction theorem performance.",
    )
    code_wreath_vertex_kernel_graded_reduction.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_vertex_kernel_graded_reduction.set_defaults(
        func=command_code_wreath_vertex_kernel_graded_reduction
    )


def command_code_wreath_vertex_kernel_graded_reduction(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_vertex_kernel_graded_reduction_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_vertex_kernel_graded_reduction_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Vertex Kernel Graded Reduction analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_vertex_kernel_graded_reduction.json"
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


def add_code_wreath_vertex_trivialization_criterion(subparsers) -> None:
    code_wreath_vertex_trivialization_criterion = subparsers.add_parser(
        "code-wreath-vertex-trivialization-criterion",
        help="Analyze code wreath vertex trivialization criterion theorem performance.",
    )
    code_wreath_vertex_trivialization_criterion.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_vertex_trivialization_criterion.set_defaults(
        func=command_code_wreath_vertex_trivialization_criterion
    )


def command_code_wreath_vertex_trivialization_criterion(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_vertex_trivialization_criterion_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_vertex_trivialization_criterion_report(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Vertex Trivialization Criterion analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_vertex_trivialization_criterion.json"
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


def add_code_wreath_weighted_overlap_exclusion(subparsers) -> None:
    code_wreath_weighted_overlap_exclusion = subparsers.add_parser(
        "code-wreath-weighted-overlap-exclusion",
        help="Analyze code wreath weighted overlap exclusion theorem performance.",
    )
    code_wreath_weighted_overlap_exclusion.add_argument(
        "--no-registry",
        action="store_true",
    )
    code_wreath_weighted_overlap_exclusion.set_defaults(
        func=command_code_wreath_weighted_overlap_exclusion
    )


def command_code_wreath_weighted_overlap_exclusion(
    args: argparse.Namespace,
) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_weighted_overlap_exclusion,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_weighted_overlap_exclusion(
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Wreath Weighted Overlap Exclusion analysis complete")
    print(
        "Artifact: research/representation/self_dual_wreath_weighted_overlap_exclusion.json"
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


def add_code_equivalence(subparsers) -> None:
    code_equivalence = subparsers.add_parser("code-equivalence", help="Run binary linear-code equivalence audits and classical baselines.")
    code_equivalence.add_argument("--pairs", default="hamming-7-4-permuted,hamming-7-4-column-twist,random-8-4-weak-invariant-collision")
    code_equivalence.add_argument("--no-registry", action="store_true")
    code_equivalence.set_defaults(func=command_code_equivalence)


def command_code_equivalence(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_code_equivalence_workbench,
    )
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_code_equivalence_workbench(pair_ids=pair_ids, write_registry=not args.no_registry)
    validation = validate_registry()
    print("Code-equivalence workbench complete")
    print("Artifact: research/code_equivalence/code_equivalence_audit.json")
    print(f"Pair audits: {len(payload['pair_audits'])}")
    print(f"Summary: {payload['summary']}")
    print(f"Falsifiers triggered: {len(payload['falsifiers_triggered'])}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_hull_projector(subparsers) -> None:
    code_hull_projector = subparsers.add_parser(
        "code-hull-projector",
        help="Stratify random codes by hull dimension and run the exact trivial-hull projector-to-GI reduction.",
    )
    code_hull_projector.add_argument("--lengths", default="24,32,48,64,96")
    code_hull_projector.add_argument("--rate", type=float, default=0.5)
    code_hull_projector.add_argument("--trials", type=int, default=2)
    code_hull_projector.add_argument("--hull-samples", type=int, default=64)
    code_hull_projector.add_argument("--seed", type=int, default=22_071)
    code_hull_projector.add_argument("--max-search-seconds", type=float, default=10.0)
    code_hull_projector.add_argument("--no-registry", action="store_true")
    code_hull_projector.add_argument("--verbose", action="store_true")
    code_hull_projector.set_defaults(func=command_code_hull_projector)


def command_code_hull_projector(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_hull_projector_reduction
    initialize_seed_registry(overwrite=False)
    lengths = [int(item.strip()) for item in args.lengths.split(",") if item.strip()]
    payload = write_hull_projector_reduction(
        lengths=lengths,
        rate=args.rate,
        trials=args.trials,
        hull_samples=args.hull_samples,
        seed=args.seed,
        max_search_seconds=args.max_search_seconds,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Hull-projector code-equivalence reduction complete")
    print("Artifact: research/code_equivalence/code_hull_projector_reduction.json")
    print(f"Unconditional hull samples: {metrics['hull_sample_count']}")
    print(f"Trivial-hull fraction: {metrics['trivial_hull_fraction']:.4f}")
    print(f"Hull dimension <=2 fraction: {metrics['hull_at_most_two_fraction']:.4f}")
    print(f"Projector/GI finite resolutions: {metrics['projector_finite_resolved_count']}")
    print(f"Graph-match timeouts: {metrics['projector_timeout_count']}")
    print(f"Polynomial GI solvers proved: {metrics['proved_polynomial_gi_solver_count']}")
    print(f"Positive quantum evidence: {metrics['positive_quantum_evidence_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["hull_distribution_records"]:
            print(
                f"- n={record['length']} k={record['dimension']} hulls={record['hull_histogram']} "
                f"trivial={record['trivial_hull_fraction']:.3f} <=2={record['hull_at_most_two_fraction']:.3f}"
            )
        for record in payload["planted_records"]:
            print(
                f"- {record['id']} | {record['status']} | "
                f"eq={record['equivalent_match']['search_seconds']:.6f}s "
                f"null={record['null_match']['search_seconds']:.6f}s"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_invariants(subparsers) -> None:
    code_invariants = subparsers.add_parser(
        "code-invariants",
        help="Run support-splitting, dual/hull, puncturing, and shortening code-equivalence invariant baselines.",
    )
    code_invariants.add_argument("--no-code-family-search", action="store_true")
    code_invariants.add_argument("--no-registry", action="store_true")
    code_invariants.add_argument("--verbose", action="store_true")
    code_invariants.set_defaults(func=command_code_invariants)


def command_code_invariants(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_code_structural_invariants,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_code_structural_invariants(
        include_code_family_search=not args.no_code_family_search,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Code structural invariant baseline complete")
    print("Artifact: research/code_equivalence/code_structural_invariants.json")
    print(f"Records: {payload['headline_metrics']['record_count']}")
    print(f"Structural rejections: {payload['headline_metrics']['structural_rejection_count']}")
    print(f"Support-splitting rejections: {payload['headline_metrics']['support_splitting_rejection_count']}")
    print(f"Dual-enumerator rejections: {payload['headline_metrics']['dual_rejection_count']}")
    print(f"Puncture/shorten rejections: {payload['headline_metrics']['puncture_shorten_rejection_count']}")
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(f"- {record['id']} | {record['status']} | {record['distinguishing_invariants']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_info_sets(subparsers) -> None:
    code_info_sets = subparsers.add_parser(
        "code-info-sets",
        help="Run information-set canonicalization baselines for code-equivalence rows.",
    )
    code_info_sets.add_argument("--max-ordered-information-sets", type=int, default=250_000)
    code_info_sets.add_argument("--no-code-family-search", action="store_true")
    code_info_sets.add_argument("--no-registry", action="store_true")
    code_info_sets.add_argument("--verbose", action="store_true")
    code_info_sets.set_defaults(func=command_code_info_sets)


def command_code_info_sets(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_code_information_set_baseline,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_code_information_set_baseline(
        max_ordered_information_sets=args.max_ordered_information_sets,
        include_code_family_search=not args.no_code_family_search,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Code information-set canonicalization complete")
    print("Artifact: research/code_equivalence/code_information_set_baseline.json")
    print(f"Records: {payload['headline_metrics']['record_count']}")
    print(f"Information-set rejections: {payload['headline_metrics']['information_set_rejection_count']}")
    print(f"Equivalent controls: {payload['headline_metrics']['equivalent_control_count']}")
    print(f"Survivor proof debt: {payload['headline_metrics']['survivor_proof_debt_count']}")
    print(f"Cap proof debt: {payload['headline_metrics']['cap_proof_debt_count']}")
    print(f"Max ordered information sets: {payload['headline_metrics']['max_ordered_information_sets_evaluated']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['id']} | {record['status']} | equal={record['canonical_equal']} "
                f"left_sets={record['left_form']['ordered_information_set_count']} "
                f"right_sets={record['right_form']['ordered_information_set_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_canonicalize(subparsers) -> None:
    code_canonicalize = subparsers.add_parser(
        "code-canonicalize",
        help="Run profile-pruned canonicalization baselines for code-equivalence rows.",
    )
    code_canonicalize.add_argument("--max-assignments", type=int, default=2_000_000)
    code_canonicalize.add_argument("--no-code-family-search", action="store_true")
    code_canonicalize.add_argument("--no-registry", action="store_true")
    code_canonicalize.add_argument("--verbose", action="store_true")
    code_canonicalize.set_defaults(func=command_code_canonicalize)


def command_code_canonicalize(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_code_canonicalization_baseline,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_code_canonicalization_baseline(
        max_assignments=args.max_assignments,
        include_code_family_search=not args.no_code_family_search,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Code canonicalization baseline complete")
    print("Artifact: research/code_equivalence/code_canonicalization_baseline.json")
    print(f"Records: {payload['headline_metrics']['record_count']}")
    print(f"Profile rejections: {payload['headline_metrics']['profile_rejection_count']}")
    print(f"Canonical-form rejections: {payload['headline_metrics']['canonical_form_rejection_count']}")
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['id']} | {record['status']} | "
                f"weak={record['weak_invariants_match']} "
                f"assignments={max(record['left_canonical']['estimated_assignments'], record['right_canonical']['estimated_assignments'])}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_profile_search(subparsers) -> None:
    code_profile_search = subparsers.add_parser(
        "code-profile-search",
        help="Search for code pairs colliding on coordinate-refinement profiles, then canonicalize them.",
    )
    code_profile_search.add_argument("--max-assignments", type=int, default=2_000_000)
    code_profile_search.add_argument("--no-registry", action="store_true")
    code_profile_search.add_argument("--verbose", action="store_true")
    code_profile_search.set_defaults(func=command_code_profile_search)


def command_code_profile_search(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_profile_collision_search
    initialize_seed_registry(overwrite=False)
    payload = write_profile_collision_search(
        max_assignments=args.max_assignments,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Code profile-collision search complete")
    print("Artifact: research/code_equivalence/code_profile_collision_search.json")
    print(f"Searches: {payload['headline_metrics']['search_count']}")
    print(f"Profile collisions: {payload['headline_metrics']['profile_collision_count']}")
    print(f"Equivalent controls: {payload['headline_metrics']['equivalent_collision_count']}")
    print(f"Canonicalization rejections: {payload['headline_metrics']['rejected_collision_count']}")
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"trials={record['trials_run']} collisions={record['profile_collision_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_tuple_profiles(subparsers) -> None:
    code_tuple_profiles = subparsers.add_parser(
        "code-tuple-profiles",
        help="Run higher-order coordinate tuple-profile baselines and tuple-profile collision search for code equivalence.",
    )
    code_tuple_profiles.add_argument("--max-tuple-size", type=int, default=3)
    code_tuple_profiles.add_argument("--tuple-cap", type=int, default=50_000)
    code_tuple_profiles.add_argument("--no-code-family-search", action="store_true")
    code_tuple_profiles.add_argument("--no-registry", action="store_true")
    code_tuple_profiles.add_argument("--verbose", action="store_true")
    code_tuple_profiles.set_defaults(func=command_code_tuple_profiles)


def command_code_tuple_profiles(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_code_tuple_profile_baseline,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_code_tuple_profile_baseline(
        max_tuple_size=args.max_tuple_size,
        tuple_cap=args.tuple_cap,
        include_code_family_search=not args.no_code_family_search,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Code tuple-profile baseline complete")
    print("Artifact: research/code_equivalence/code_tuple_profile_baseline.json")
    print(f"Pairs: {payload['headline_metrics']['pair_count']}")
    print(f"Tuple-profile rejections: {payload['headline_metrics']['tuple_profile_rejection_count']}")
    print(f"Tuple-profile survivors: {payload['headline_metrics']['tuple_profile_survivor_count']}")
    print(f"Tuple-profile proof debt: {payload['headline_metrics']['tuple_profile_proof_debt_count']}")
    print(f"Tuple collisions: {payload['headline_metrics']['tuple_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['id']} | {record['status']} | "
                f"first_tuple={record['first_distinguishing_tuple_size']}"
            )
        for record in payload["collision_records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"collisions={record['tuple_collision_count']} trials={record['trials_run']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_low_weight(subparsers) -> None:
    code_low_weight = subparsers.add_parser(
        "code-low-weight",
        help="Run low-weight support hypergraph/matroid baselines for code-equivalence rows.",
    )
    code_low_weight.add_argument("--max-weight", type=int, default=6)
    code_low_weight.add_argument("--weight-radius", type=int, default=2)
    code_low_weight.add_argument("--max-codewords", type=int, default=32768)
    code_low_weight.add_argument("--wl-iterations", type=int, default=4)
    code_low_weight.add_argument("--max-incidence-nodes", type=int, default=220)
    code_low_weight.add_argument("--no-code-family-search", action="store_true")
    code_low_weight.add_argument("--no-algebraic-searches", action="store_true")
    code_low_weight.add_argument("--no-registry", action="store_true")
    code_low_weight.add_argument("--verbose", action="store_true")
    code_low_weight.set_defaults(func=command_code_low_weight)


def command_code_low_weight(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_code_low_weight_structure
    initialize_seed_registry(overwrite=False)
    payload = write_code_low_weight_structure(
        max_weight=args.max_weight,
        weight_radius=args.weight_radius,
        max_codewords=args.max_codewords,
        wl_iterations=args.wl_iterations,
        max_incidence_nodes=args.max_incidence_nodes,
        include_code_family_search=not args.no_code_family_search,
        include_algebraic_searches=not args.no_algebraic_searches,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Code low-weight matroid baseline complete")
    print("Artifact: research/code_equivalence/code_low_weight_structure.json")
    print(f"Records: {payload['headline_metrics']['record_count']}")
    print(f"Low-weight rejections: {payload['headline_metrics']['low_weight_rejection_count']}")
    print(f"Equivalent controls: {payload['headline_metrics']['equivalent_control_count']}")
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_count']}")
    print(f"Survivor proof debt: {payload['headline_metrics']['survivor_proof_debt_count']}")
    print(f"Cap proof debt: {payload['headline_metrics']['cap_proof_debt_count']}")
    print(f"Incidence-isomorphism matches: {payload['headline_metrics']['incidence_isomorphism_match_count']}")
    print(f"Incidence-isomorphism rejections: {payload['headline_metrics']['incidence_isomorphism_rejection_count']}")
    print(f"Incidence-isomorphism caps: {payload['headline_metrics']['incidence_isomorphism_cap_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['row_id']} / {record['id']} | {record['status']} | "
                f"distinguish={record['distinguishing_signatures']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_qc_search(subparsers) -> None:
    code_qc_search = subparsers.add_parser(
        "code-qc-search",
        help="Search structured quasi-cyclic code families for tuple-profile collisions, then canonicalize them.",
    )
    code_qc_search.add_argument("--tuple-size", type=int, default=2)
    code_qc_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_qc_search.add_argument("--no-registry", action="store_true")
    code_qc_search.add_argument("--verbose", action="store_true")
    code_qc_search.set_defaults(func=command_code_qc_search)


def command_code_qc_search(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_quasi_cyclic_code_search
    initialize_seed_registry(overwrite=False)
    payload = write_quasi_cyclic_code_search(
        tuple_size=args.tuple_size,
        tuple_cap=args.tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Quasi-cyclic code search complete")
    print("Artifact: research/code_equivalence/quasi_cyclic_code_search.json")
    print(f"Searches: {payload['headline_metrics']['search_count']}")
    print(f"Tuple collisions: {payload['headline_metrics']['tuple_collision_count']}")
    print(f"Equivalent collisions: {payload['headline_metrics']['equivalent_collision_count']}")
    print(f"Tuple-profile rejections: {payload['headline_metrics']['tuple_profile_rejection_count']}")
    print(f"Canonicalization rejections: {payload['headline_metrics']['canonicalization_rejection_count']}")
    print(f"Total rejected collisions: {payload['headline_metrics']['rejected_collision_count']}")
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"collisions={record['tuple_collision_count']} trials={record['trials_run']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_qc_canonicalize(subparsers) -> None:
    code_qc_canonicalize = subparsers.add_parser(
        "code-qc-canonicalize",
        help="Canonicalize quasi-cyclic tuple-profile collision rows under block permutations and cyclic shifts.",
    )
    code_qc_canonicalize.add_argument("--max-group-size", type=int, default=250_000)
    code_qc_canonicalize.add_argument("--no-registry", action="store_true")
    code_qc_canonicalize.add_argument("--verbose", action="store_true")
    code_qc_canonicalize.set_defaults(func=command_code_qc_canonicalize)


def command_code_qc_canonicalize(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_qc_canonicalization_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_qc_canonicalization_report(
        max_group_size=args.max_group_size,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Quasi-cyclic automorphism canonicalization complete")
    print("Artifact: research/code_equivalence/quasi_cyclic_canonicalization.json")
    print(f"Rows: {payload['headline_metrics']['record_count']}")
    print(f"Evaluated rows: {payload['headline_metrics']['evaluated_count']}")
    print(f"Equivalent controls: {payload['headline_metrics']['equivalent_control_count']}")
    print(f"QC no-equivalence proof debt: {payload['headline_metrics']['qc_no_equivalence_proof_debt_count']}")
    print(f"Cap proof debt: {payload['headline_metrics']['canonicalization_cap_proof_debt_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['id']} | {record['status']} | "
                f"group={record['left_canonical']['group_size']} unrestricted={record['unrestricted_estimated_assignments']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_qc_info_resolve(subparsers) -> None:
    code_qc_info_resolve = subparsers.add_parser(
        "code-qc-info-resolve",
        help="Resolve quasi-cyclic proof-debt rows with exact information-set canonicalization.",
    )
    code_qc_info_resolve.add_argument("--max-ordered-information-sets", type=int, default=2_000_000)
    code_qc_info_resolve.add_argument("--audit-all-rows", action="store_true")
    code_qc_info_resolve.add_argument("--no-registry", action="store_true")
    code_qc_info_resolve.add_argument("--verbose", action="store_true")
    code_qc_info_resolve.set_defaults(func=command_code_qc_info_resolve)


def command_code_qc_info_resolve(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_qc_information_set_resolver,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_qc_information_set_resolver(
        max_ordered_information_sets=args.max_ordered_information_sets,
        stop_after_family_control=not args.audit_all_rows,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("QC information-set proof-debt resolver complete")
    print("Artifact: research/code_equivalence/qc_information_set_resolver.json")
    print(f"Rows: {payload['headline_metrics']['record_count']}")
    print(f"Evaluated rows: {payload['headline_metrics']['evaluated_count']}")
    print(f"Equivalent controls: {payload['headline_metrics']['equivalent_control_count']}")
    print(f"Information-set rejections: {payload['headline_metrics']['information_set_rejection_count']}")
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['id']} | {record['status']} | "
                f"source={record['source_search_id']} estimated={record['estimated_ordered_information_sets']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_cyclic_search(subparsers) -> None:
    code_cyclic_search = subparsers.add_parser(
        "code-cyclic-search",
        help="Search binary cyclic code families for tuple-profile collisions and dihedral/canonicalization controls.",
    )
    code_cyclic_search.add_argument("--lengths", default="7,15,21")
    code_cyclic_search.add_argument("--min-dimension", type=int, default=2)
    code_cyclic_search.add_argument("--max-dimension", type=int, default=10)
    code_cyclic_search.add_argument("--tuple-size", type=int, default=2)
    code_cyclic_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_cyclic_search.add_argument("--canonical-max-assignments", type=int, default=200_000)
    code_cyclic_search.add_argument("--max-collisions", type=int, default=8)
    code_cyclic_search.add_argument("--max-verbose-audits", type=int, default=4)
    code_cyclic_search.add_argument("--no-registry", action="store_true")
    code_cyclic_search.add_argument("--verbose", action="store_true")
    code_cyclic_search.set_defaults(func=command_code_cyclic_search)


def command_code_cyclic_search(args: argparse.Namespace) -> int:
    from qsearch import (
        CyclicCodeSearchSpec,
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_cyclic_code_search,
    )
    initialize_seed_registry(overwrite=False)
    lengths = parse_int_csv(args.lengths)
    specs = [
        CyclicCodeSearchSpec(
            id=f"cyclic-n{length}",
            length=length,
            min_dimension=args.min_dimension,
            max_dimension=args.max_dimension,
            tuple_size=args.tuple_size,
            max_collisions=args.max_collisions,
        )
        for length in lengths
    ]
    payload = write_cyclic_code_search(
        specs=specs,
        tuple_cap=args.tuple_cap,
        canonical_max_assignments=args.canonical_max_assignments,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Cyclic code algebraic search complete")
    print("Artifact: research/code_equivalence/cyclic_code_search.json")
    print(f"Searches: {payload['headline_metrics']['search_count']}")
    print(f"Codes enumerated: {payload['headline_metrics']['code_count']}")
    print(f"Tuple collisions: {payload['headline_metrics']['tuple_collision_count']}")
    print(f"Dihedral controls: {payload['headline_metrics']['dihedral_equivalent_count']}")
    print(f"Multiplier-affine controls: {payload['headline_metrics'].get('multiplier_equivalent_count', 0)}")
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"codes={record['code_count']} collisions={record['tuple_collision_count']} "
                f"dihedral={record['dihedral_equivalent_count']} multiplier={record.get('multiplier_equivalent_count', 0)}"
            )
            for audit in record["collision_audits"][: args.max_verbose_audits]:
                print(
                    f"  {audit['generator_poly_a']} vs {audit['generator_poly_b']} | "
                    f"{audit['status']} | tuple={audit['tuple_profile_status']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_bch_search(subparsers) -> None:
    code_bch_search = subparsers.add_parser(
        "code-bch-search",
        help="Search primitive BCH code families with cyclotomic/decimation controls.",
    )
    code_bch_search.add_argument("--specs", default="4,3,9,1|2|3|5|7;5,3,11,1|2|3|5|7|11")
    code_bch_search.add_argument("--tuple-size", type=int, default=2)
    code_bch_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_bch_search.add_argument("--canonical-max-assignments", type=int, default=200_000)
    code_bch_search.add_argument("--max-collisions", type=int, default=10)
    code_bch_search.add_argument("--max-verbose-audits", type=int, default=4)
    code_bch_search.add_argument("--no-registry", action="store_true")
    code_bch_search.add_argument("--verbose", action="store_true")
    code_bch_search.set_defaults(func=command_code_bch_search)


def command_code_bch_search(args: argparse.Namespace) -> int:
    from qsearch import (
        BCHSearchSpec,
        initialize_seed_registry,
        validate_registry,
        write_bch_code_search,
    )
    initialize_seed_registry(overwrite=False)
    specs = []
    for raw_spec in args.specs.split(";"):
        if not raw_spec.strip():
            continue
        parts = [item.strip() for item in raw_spec.split(",")]
        if len(parts) not in {3, 4}:
            raise ValueError("each BCH spec must be extension_degree,min_distance,max_distance[,start|start|...]")
        extension_degree = int(parts[0])
        min_distance = int(parts[1])
        max_distance = int(parts[2])
        starts = tuple(int(item) for item in parts[3].split("|")) if len(parts) == 4 and parts[3] else (1, 2, 3, 5, 7)
        specs.append(
            BCHSearchSpec(
                id=f"bch-m{extension_degree}-d{min_distance}-{max_distance}",
                extension_degree=extension_degree,
                min_designed_distance=min_distance,
                max_designed_distance=max_distance,
                starts=starts,
                tuple_size=args.tuple_size,
                max_collisions=args.max_collisions,
            )
        )
    payload = write_bch_code_search(
        specs=specs or None,
        tuple_cap=args.tuple_cap,
        canonical_max_assignments=args.canonical_max_assignments,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("BCH code algebraic search complete")
    print("Artifact: research/code_equivalence/bch_code_search.json")
    print(f"Searches: {metrics['search_count']}")
    print(f"Codes generated: {metrics['generated_code_count']}")
    print(f"Duplicate defining-set controls: {metrics['duplicate_code_count']}")
    print(f"Tuple/algebraic-profile collisions: {metrics['tuple_collision_count']}")
    print(f"Decimation controls: {metrics['multiplier_equivalent_count']}")
    print(f"Dual higher-tuple rejections: {metrics.get('dual_higher_tuple_rejection_count', 0)}")
    print(f"Classical rejections: {metrics['structural_rejection_count'] + metrics['tuple_profile_rejection_count'] + metrics['low_weight_rejection_count'] + metrics.get('dual_rejection_count', 0) + metrics['canonicalization_rejection_count']}")
    print(f"Proof debt: {metrics['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"codes={record['generated_code_count']} duplicates={record['duplicate_code_count']} "
                f"collisions={record['tuple_collision_count']} decimation={record['multiplier_equivalent_count']} "
                f"proof_debt={record['proof_debt_collision_count']}"
            )
            for audit in record["collision_audits"][: args.max_verbose_audits]:
                print(
                    f"  {audit['code_a']['id']} vs {audit['code_b']['id']} | "
                    f"{audit['status']} | multiplier={audit['multiplier']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_goppa_search(subparsers) -> None:
    code_goppa_search = subparsers.add_parser(
        "code-goppa-search",
        help="Search binary Goppa/alternant code families with semilinear automorphism controls.",
    )
    code_goppa_search.add_argument("--field-degrees", default="3,4")
    code_goppa_search.add_argument("--goppa-degree", type=int, default=2)
    code_goppa_search.add_argument("--max-polynomials", type=int, default=96)
    code_goppa_search.add_argument("--tuple-size", type=int, default=2)
    code_goppa_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_goppa_search.add_argument("--canonical-max-assignments", type=int, default=200_000)
    code_goppa_search.add_argument("--max-collisions", type=int, default=4)
    code_goppa_search.add_argument("--min-dimension", type=int, default=2)
    code_goppa_search.add_argument("--max-dimension", type=int, default=12)
    code_goppa_search.add_argument("--seed", type=int, default=0)
    code_goppa_search.add_argument("--max-verbose-audits", type=int, default=4)
    code_goppa_search.add_argument("--no-registry", action="store_true")
    code_goppa_search.add_argument("--verbose", action="store_true")
    code_goppa_search.set_defaults(func=command_code_goppa_search)


def command_code_goppa_search(args: argparse.Namespace) -> int:
    from qsearch import (
        GoppaSearchSpec,
        initialize_seed_registry,
        parse_int_csv,
        validate_registry,
        write_goppa_code_search,
    )
    initialize_seed_registry(overwrite=False)
    specs = [
        GoppaSearchSpec(
            id=f"goppa-m{field_degree}-t{args.goppa_degree}",
            field_degree=field_degree,
            goppa_degree=args.goppa_degree,
            max_polynomials=args.max_polynomials,
            tuple_size=args.tuple_size,
            max_collisions=args.max_collisions,
            min_dimension=args.min_dimension,
            max_dimension=args.max_dimension,
            seed=args.seed + field_degree * 100 + args.goppa_degree,
        )
        for field_degree in parse_int_csv(args.field_degrees)
    ]
    payload = write_goppa_code_search(
        specs=specs,
        tuple_cap=args.tuple_cap,
        canonical_max_assignments=args.canonical_max_assignments,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Goppa/alternant code algebraic search complete")
    print("Artifact: research/code_equivalence/goppa_code_search.json")
    print(f"Searches: {payload['headline_metrics']['search_count']}")
    print(f"Codes enumerated: {payload['headline_metrics']['code_count']}")
    print(f"Tuple collisions: {payload['headline_metrics']['tuple_collision_count']}")
    print(f"Semilinear controls: {payload['headline_metrics']['semilinear_control_count']}")
    print(f"Classical rejections: {payload['headline_metrics']['structural_rejection_count'] + payload['headline_metrics']['tuple_profile_rejection_count'] + payload['headline_metrics']['canonicalization_rejection_count']}")
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"codes={record['code_count']} collisions={record['tuple_collision_count']} "
                f"semilinear={record['semilinear_control_count']}"
            )
            for audit in record["collision_audits"][: args.max_verbose_audits]:
                print(
                    f"  {audit['generator_poly_a']} vs {audit['generator_poly_b']} | "
                    f"{audit['status']} | semilinear={audit['semilinear_witness']['equivalent']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_goppa_scaling(subparsers) -> None:
    code_goppa_scaling = subparsers.add_parser(
        "code-goppa-scaling",
        help="Audit scalable punctured Goppa/alternant families with exact dual and Schur invariants.",
    )
    code_goppa_scaling.add_argument("--no-registry", action="store_true")
    code_goppa_scaling.add_argument("--verbose", action="store_true")
    code_goppa_scaling.set_defaults(func=command_code_goppa_scaling)


def command_code_goppa_scaling(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_goppa_scaling_frontier
    initialize_seed_registry(overwrite=False)
    payload = write_goppa_scaling_frontier(write_registry=not args.no_registry)
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Scalable punctured Goppa/alternant frontier complete")
    print("Artifact: research/code_equivalence/goppa_scaling_frontier.json")
    print(f"Families: {metrics['family_count']}")
    print(f"Instances: {metrics['instance_count']}")
    print(f"Maximum length: {metrics['maximum_length']}")
    print(f"Exact dual signatures: {metrics['exact_dual_signature_count']}")
    print(f"Exact invariant rejections: {metrics['exact_invariant_rejection_count']}")
    print(f"Proof-debt pairs: {metrics['proof_debt_pair_count']}")
    print(f"Baseline-cap pairs: {metrics['baseline_cap_pair_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"instances={len(record['instances'])} exact={record['exact_dual_signature_count']} "
                f"rejections={record['exact_invariant_rejection_count']} "
                f"proof_debt={record['proof_debt_pair_count']} caps={record['baseline_cap_pair_count']}"
            )
            for audit in record["collision_audits"]:
                print(f"  {audit['left_id']} vs {audit['right_id']} | {audit['status']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_goppa_syzygies(subparsers) -> None:
    code_goppa_syzygies = subparsers.add_parser(
        "code-goppa-syzygies",
        help="Compute exact dual-code Betti and complete shortening-profile invariants on scalable Goppa rows.",
    )
    code_goppa_syzygies.add_argument(
        "--coordinate-limit",
        type=int,
        default=None,
        help="Cap shortening coordinates for diagnostics; capped profiles cannot reject a pair.",
    )
    code_goppa_syzygies.add_argument("--skip-permutation-controls", action="store_true")
    code_goppa_syzygies.add_argument("--audit-resolved-pairs", action="store_true")
    code_goppa_syzygies.add_argument("--no-registry", action="store_true")
    code_goppa_syzygies.add_argument("--verbose", action="store_true")
    code_goppa_syzygies.set_defaults(func=command_code_goppa_syzygies)


def command_code_goppa_syzygies(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_goppa_syzygy_frontier
    initialize_seed_registry(overwrite=False)
    payload = write_goppa_syzygy_frontier(
        coordinate_limit=args.coordinate_limit,
        recompute_permutation_controls=not args.skip_permutation_controls,
        audit_resolved_pairs=args.audit_resolved_pairs,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact scalable Goppa dual-syzygy frontier complete")
    print("Artifact: research/code_equivalence/goppa_syzygy_frontier.json")
    print(f"Exact whole-code signatures: {metrics['exact_whole_syzygy_signature_count']}")
    print(f"Complete shortening profiles: {metrics['complete_shortening_profile_count']}")
    print(f"Evaluated shortenings: {metrics['evaluated_shortening_count']}")
    print(f"Exact syzygy rejections: {metrics['exact_syzygy_rejection_count']}")
    print(f"Exact syzygy collisions: {metrics['exact_syzygy_collision_count']}")
    print(f"Shortening-cap pairs: {metrics['shortening_cap_pair_count']}")
    print(f"Prior classical rejections retained: {metrics['prior_classical_rejection_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['family_id']} | {record['status']} | "
                f"rejections={record['exact_syzygy_rejection_count']} "
                f"collisions={record['exact_syzygy_collision_count']} caps={record['shortening_cap_pair_count']}"
            )
            for audit in record["pair_audits"]:
                print(f"  {audit['left_id']} vs {audit['right_id']} | {audit['status']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_goppa_projectors(subparsers) -> None:
    code_goppa_projectors = subparsers.add_parser(
        "code-goppa-projectors",
        help="Apply the exact trivial-hull projector-to-GI reduction to scalable Goppa frontier pairs.",
    )
    code_goppa_projectors.add_argument("--max-search-seconds", type=float, default=10.0)
    code_goppa_projectors.add_argument("--no-registry", action="store_true")
    code_goppa_projectors.add_argument("--verbose", action="store_true")
    code_goppa_projectors.set_defaults(func=command_code_goppa_projectors)


def command_code_goppa_projectors(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_goppa_hull_projector_frontier,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_goppa_hull_projector_frontier(
        max_search_seconds=args.max_search_seconds,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Scalable Goppa hull-projector frontier complete")
    print("Artifact: research/code_equivalence/goppa_hull_projector_frontier.json")
    print(f"Trivial-hull certificates: {metrics['trivial_hull_certificate_count']}")
    print(f"Frontier pairs: {metrics['frontier_pair_count']}")
    print(f"Polynomial projector rejections: {metrics['polynomial_projector_rejection_count']}")
    print(f"Exact graph rejections: {metrics['exact_graph_rejection_count']}")
    print(f"Equivalent/automorphic rows: {metrics['equivalent_or_automorphic_count']}")
    print(f"Projector proof debt: {metrics['projector_proof_debt_count']}")
    print(f"Control failures: {metrics['control_failure_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(f"- {record['family_id']} | {record['status']} | frontier={record['frontier_pair_count']}")
            for audit in record["pair_audits"]:
                print(f"  {audit['left_id']} vs {audit['right_id']} | {audit['status']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_tanner_search(subparsers) -> None:
    code_tanner_search = subparsers.add_parser(
        "code-tanner-search",
        help="Search regular Tanner/LDPC code families with Tanner-graph and code-canonicalization controls.",
    )
    code_tanner_search.add_argument("--specs", default="10,5,2,4;12,6,2,4;12,9,3,4")
    code_tanner_search.add_argument("--max-trials", type=int, default=120)
    code_tanner_search.add_argument("--max-collisions", type=int, default=4)
    code_tanner_search.add_argument("--tuple-size", type=int, default=2)
    code_tanner_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_tanner_search.add_argument("--max-ordered-information-sets", type=int, default=500_000)
    code_tanner_search.add_argument("--canonical-max-assignments", type=int, default=200_000)
    code_tanner_search.add_argument("--min-dimension", type=int, default=2)
    code_tanner_search.add_argument("--max-dimension", type=int, default=12)
    code_tanner_search.add_argument("--seed", type=int, default=0)
    code_tanner_search.add_argument("--max-verbose-audits", type=int, default=4)
    code_tanner_search.add_argument("--no-registry", action="store_true")
    code_tanner_search.add_argument("--verbose", action="store_true")
    code_tanner_search.set_defaults(func=command_code_tanner_search)


def command_code_tanner_search(args: argparse.Namespace) -> int:
    from qsearch import (
        TannerSearchSpec,
        initialize_seed_registry,
        validate_registry,
        write_tanner_code_search,
    )
    initialize_seed_registry(overwrite=False)
    specs = []
    for raw_spec in args.specs.split(";"):
        if not raw_spec.strip():
            continue
        parts = [int(item.strip()) for item in raw_spec.split(",")]
        if len(parts) != 4:
            raise ValueError("each Tanner spec must be variables,checks,variable_degree,check_degree")
        variable_count, check_count, variable_degree, check_degree = parts
        specs.append(
            TannerSearchSpec(
                id=f"tanner-{variable_count}-{check_count}-dv{variable_degree}-dc{check_degree}",
                variable_count=variable_count,
                check_count=check_count,
                variable_degree=variable_degree,
                check_degree=check_degree,
                max_trials=args.max_trials,
                max_collisions=args.max_collisions,
                seed=args.seed + variable_count * 100 + check_count * 10 + variable_degree,
                tuple_size=args.tuple_size,
                min_dimension=args.min_dimension,
                max_dimension=args.max_dimension,
            )
        )
    payload = write_tanner_code_search(
        specs=specs or None,
        tuple_cap=args.tuple_cap,
        max_ordered_information_sets=args.max_ordered_information_sets,
        canonical_max_assignments=args.canonical_max_assignments,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Tanner/LDPC code-family search complete")
    print("Artifact: research/code_equivalence/tanner_code_search.json")
    print(f"Searches: {payload['headline_metrics']['search_count']}")
    print(f"Codes enumerated: {payload['headline_metrics']['code_count']}")
    print(f"Tuple collisions: {payload['headline_metrics']['tuple_collision_count']}")
    print(f"Equivalent controls: {payload['headline_metrics']['equivalent_control_count']}")
    print(f"Classical rejections: {payload['headline_metrics']['structural_rejection_count'] + payload['headline_metrics']['tuple_profile_rejection_count'] + payload['headline_metrics']['information_set_rejection_count'] + payload['headline_metrics']['canonicalization_rejection_count']}")
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"codes={record['code_count']} collisions={record['tuple_collision_count']} "
                f"controls={record['equivalent_control_count']}"
            )
            for audit in record["collision_audits"][: args.max_verbose_audits]:
                print(
                    f"  {audit['id']} | {audit['status']} | "
                    f"tanner_iso={audit['tanner_graph']['isomorphic']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_rm_search(subparsers) -> None:
    code_reed_muller_search = subparsers.add_parser(
        "code-rm-search",
        help="Search punctured Reed-Muller code families with affine-support automorphism controls.",
    )
    code_reed_muller_search.add_argument("--specs", default="1,4,12;2,4,12;2,4,14")
    code_reed_muller_search.add_argument("--max-trials", type=int, default=120)
    code_reed_muller_search.add_argument("--max-collisions", type=int, default=4)
    code_reed_muller_search.add_argument("--tuple-size", type=int, default=2)
    code_reed_muller_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_reed_muller_search.add_argument("--affine-map-cap", type=int, default=1_000_000)
    code_reed_muller_search.add_argument("--canonical-max-assignments", type=int, default=200_000)
    code_reed_muller_search.add_argument("--seed", type=int, default=0)
    code_reed_muller_search.add_argument("--max-verbose-audits", type=int, default=4)
    code_reed_muller_search.add_argument("--no-registry", action="store_true")
    code_reed_muller_search.add_argument("--verbose", action="store_true")
    code_reed_muller_search.set_defaults(func=command_code_reed_muller_search)


def command_code_reed_muller_search(args: argparse.Namespace) -> int:
    from qsearch import (
        ReedMullerSearchSpec,
        initialize_seed_registry,
        validate_registry,
        write_reed_muller_code_search,
    )
    initialize_seed_registry(overwrite=False)
    specs = []
    for raw_spec in args.specs.split(";"):
        if not raw_spec.strip():
            continue
        parts = [int(item.strip()) for item in raw_spec.split(",")]
        if len(parts) != 3:
            raise ValueError("each Reed-Muller spec must be order,variables,puncture_size")
        order, variables, puncture_size = parts
        specs.append(
            ReedMullerSearchSpec(
                id=f"rm-r{order}-m{variables}-k{puncture_size}",
                order=order,
                variables=variables,
                puncture_size=puncture_size,
                max_trials=args.max_trials,
                max_collisions=args.max_collisions,
                tuple_size=args.tuple_size,
                seed=args.seed + order * 1000 + variables * 100 + puncture_size,
            )
        )
    payload = write_reed_muller_code_search(
        specs=specs or None,
        affine_map_cap=args.affine_map_cap,
        tuple_cap=args.tuple_cap,
        canonical_max_assignments=args.canonical_max_assignments,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Reed-Muller punctured-code search complete")
    print("Artifact: research/code_equivalence/reed_muller_code_search.json")
    print(f"Searches: {payload['headline_metrics']['search_count']}")
    print(f"Codes sampled: {payload['headline_metrics']['code_count']}")
    print(f"Tuple collisions: {payload['headline_metrics']['tuple_collision_count']}")
    print(f"Affine controls: {payload['headline_metrics']['affine_control_count']}")
    print(
        "Classical rejections: "
        f"{payload['headline_metrics']['structural_rejection_count'] + payload['headline_metrics']['tuple_profile_rejection_count'] + payload['headline_metrics']['low_weight_rejection_count'] + payload['headline_metrics']['canonicalization_rejection_count']}"
    )
    print(f"Proof debt: {payload['headline_metrics']['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"codes={record['code_count']} collisions={record['tuple_collision_count']} "
                f"affine={record['affine_control_count']} proof_debt={record['proof_debt_collision_count']}"
            )
            for audit in record["collision_audits"][: args.max_verbose_audits]:
                print(
                    f"  {audit['id']} | {audit['status']} | affine={audit['affine_support']['equivalent']} "
                    f"tuple={audit['tuple_profile_status']} low_weight={audit['low_weight_status']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_rank_metric_search(subparsers) -> None:
    code_rank_metric_search = subparsers.add_parser(
        "code-rank-metric-search",
        help="Search binary-expanded Gabidulin/rank-metric code families with symbol-block controls.",
    )
    code_rank_metric_search.add_argument("--specs", default="4,3,2;5,3,2")
    code_rank_metric_search.add_argument("--max-trials", type=int, default=90)
    code_rank_metric_search.add_argument("--max-collisions", type=int, default=4)
    code_rank_metric_search.add_argument("--tuple-size", type=int, default=2)
    code_rank_metric_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_rank_metric_search.add_argument("--canonical-max-assignments", type=int, default=200_000)
    code_rank_metric_search.add_argument("--seed", type=int, default=0)
    code_rank_metric_search.add_argument("--max-verbose-audits", type=int, default=4)
    code_rank_metric_search.add_argument("--no-registry", action="store_true")
    code_rank_metric_search.add_argument("--verbose", action="store_true")
    code_rank_metric_search.set_defaults(func=command_code_rank_metric_search)


def command_code_rank_metric_search(args: argparse.Namespace) -> int:
    from qsearch import (
        RankMetricSearchSpec,
        initialize_seed_registry,
        validate_registry,
        write_rank_metric_code_search,
    )
    initialize_seed_registry(overwrite=False)
    specs = []
    for raw_spec in args.specs.split(";"):
        if not raw_spec.strip():
            continue
        parts = [int(item.strip()) for item in raw_spec.split(",")]
        if len(parts) != 3:
            raise ValueError("each rank-metric spec must be field_degree,rank_length,gabidulin_dimension")
        field_degree, rank_length, gabidulin_dimension = parts
        specs.append(
            RankMetricSearchSpec(
                id=f"gabidulin-m{field_degree}-n{rank_length}-k{gabidulin_dimension}",
                field_degree=field_degree,
                rank_length=rank_length,
                gabidulin_dimension=gabidulin_dimension,
                max_trials=args.max_trials,
                max_collisions=args.max_collisions,
                tuple_size=args.tuple_size,
                seed=args.seed + field_degree * 1000 + rank_length * 100 + gabidulin_dimension,
            )
        )
    payload = write_rank_metric_code_search(
        specs=specs or None,
        tuple_cap=args.tuple_cap,
        canonical_max_assignments=args.canonical_max_assignments,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Binary-expanded rank-metric/Gabidulin code search complete")
    print("Artifact: research/code_equivalence/rank_metric_code_search.json")
    print(f"Searches: {metrics['search_count']}")
    print(f"Descriptors sampled: {metrics['descriptor_count']}")
    print(f"Tuple/control rows: {metrics['tuple_collision_count']}")
    print(f"Block-permutation controls: {metrics['block_permutation_control_count']}")
    print(f"Equivalent controls: {metrics['equivalent_control_count']}")
    print(f"Classical rejections: {metrics['structural_rejection_count'] + metrics['tuple_profile_rejection_count'] + metrics['low_weight_rejection_count'] + metrics['canonicalization_rejection_count']}")
    print(f"Proof debt: {metrics['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"descriptors={record['descriptor_count']} rows={record['tuple_collision_count']} "
                f"block-controls={record['block_permutation_control_count']} proof_debt={record['proof_debt_collision_count']}"
            )
            for audit in (record["control_audits"] + record["collision_audits"])[: args.max_verbose_audits]:
                print(
                    f"  {audit['id']} | {audit.get('collision_source', 'unknown')} | {audit['status']} | "
                    f"block={audit['block_permutation']['equivalent']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_incidence_resolve(subparsers) -> None:
    code_incidence_resolver = subparsers.add_parser(
        "code-incidence-resolve",
        help="Exactly resolve tractable rank-metric/QC proof-debt rows using full codeword-coordinate incidence graphs.",
    )
    code_incidence_resolver.add_argument("--max-codewords", type=int, default=4_096)
    code_incidence_resolver.add_argument("--max-search-seconds", type=float, default=20.0)
    code_incidence_resolver.add_argument("--no-registry", action="store_true")
    code_incidence_resolver.add_argument("--verbose", action="store_true")
    code_incidence_resolver.set_defaults(func=command_code_incidence_resolve)


def command_code_incidence_resolve(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_code_incidence_resolver
    initialize_seed_registry(overwrite=False)
    payload = write_code_incidence_resolver(
        max_codewords=args.max_codewords,
        max_search_seconds=args.max_search_seconds,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Exact code-incidence isomorphism resolver complete")
    print("Artifact: research/code_equivalence/code_incidence_resolver.json")
    print(f"Proof-debt inputs: {metrics['input_count']}")
    print(f"Family buckets: {metrics['family_count']}")
    print(f"Verified equivalent controls: {metrics['equivalent_control_count']}")
    print(f"Exact finite-instance rejections: {metrics['exact_rejection_count']}")
    print(f"Unresolved proof debt: {metrics['proof_debt_count']}")
    print(f"Timeouts: {metrics['timeout_count']}")
    print(f"Expansion-cap rows: {metrics['expansion_cap_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            witness = record["witness"]
            print(
                f"- {record['source']}:{record['id']} | {record['status']} | "
                f"[n={witness['length_a']}, k={witness['dimension_a']}] "
                f"equivalent={witness['equivalent']} verified={witness['verification_passed']} "
                f"seconds={witness['search_seconds']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_ag_search(subparsers) -> None:
    code_affine_geometry_search = subparsers.add_parser(
        "code-ag-search",
        help="Search affine-geometry incidence-code families with AGL(2,q) support controls.",
    )
    code_affine_geometry_search.add_argument("--specs", default="2,3;3,6")
    code_affine_geometry_search.add_argument("--max-trials", type=int, default=70)
    code_affine_geometry_search.add_argument("--max-collisions", type=int, default=4)
    code_affine_geometry_search.add_argument("--tuple-size", type=int, default=2)
    code_affine_geometry_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_affine_geometry_search.add_argument("--affine-map-cap", type=int, default=250_000)
    code_affine_geometry_search.add_argument("--canonical-max-assignments", type=int, default=200_000)
    code_affine_geometry_search.add_argument("--seed", type=int, default=0)
    code_affine_geometry_search.add_argument("--max-verbose-audits", type=int, default=4)
    code_affine_geometry_search.add_argument("--no-registry", action="store_true")
    code_affine_geometry_search.add_argument("--verbose", action="store_true")
    code_affine_geometry_search.set_defaults(func=command_code_affine_geometry_search)


def command_code_affine_geometry_search(args: argparse.Namespace) -> int:
    from qsearch import (
        AffineGeometrySearchSpec,
        initialize_seed_registry,
        validate_registry,
        write_affine_geometry_code_search,
    )
    initialize_seed_registry(overwrite=False)
    specs = []
    for raw_spec in args.specs.split(";"):
        if not raw_spec.strip():
            continue
        parts = [int(item.strip()) for item in raw_spec.split(",")]
        if len(parts) != 2:
            raise ValueError("each affine-geometry spec must be field_order,puncture_size")
        field_order, puncture_size = parts
        specs.append(
            AffineGeometrySearchSpec(
                id=f"ag2-f{field_order}-k{puncture_size}",
                field_order=field_order,
                puncture_size=puncture_size,
                max_trials=args.max_trials,
                max_collisions=args.max_collisions,
                tuple_size=args.tuple_size,
                seed=args.seed + field_order * 100 + puncture_size,
            )
        )
    payload = write_affine_geometry_code_search(
        specs=specs or None,
        affine_map_cap=args.affine_map_cap,
        tuple_cap=args.tuple_cap,
        canonical_max_assignments=args.canonical_max_assignments,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Affine-geometry incidence-code search complete")
    print("Artifact: research/code_equivalence/affine_geometry_code_search.json")
    print(f"Searches: {metrics['search_count']}")
    print(f"Codes sampled: {metrics['code_count']}")
    print(f"Tuple/control collisions: {metrics['tuple_collision_count']}")
    print(f"Support affine-profile candidates: {metrics.get('support_affine_profile_collision_count', 0)}")
    print(f"Affine-linear controls: {metrics['affine_control_count']}")
    print(f"Classical rejections: {metrics['structural_rejection_count'] + metrics['tuple_profile_rejection_count'] + metrics['low_weight_rejection_count'] + metrics['canonicalization_rejection_count']}")
    print(f"Proof debt: {metrics['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"codes={record['code_count']} controls={record['affine_control_count']} "
                f"affine-profile={record.get('support_affine_profile_collision_count', 0)} "
                f"proof_debt={record['proof_debt_collision_count']}"
            )
            for audit in (record["control_audits"] + record["collision_audits"])[: args.max_verbose_audits]:
                print(
                    f"  {audit['id']} | {audit.get('collision_source', 'unknown')} | "
                    f"{audit['status']} | maps={audit['affine_support']['maps_checked']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_pg_search(subparsers) -> None:
    code_projective_geometry_search = subparsers.add_parser(
        "code-pg-search",
        help="Search projective-geometry incidence-code families with projective-linear controls.",
    )
    code_projective_geometry_search.add_argument("--specs", default="2,6;3,10")
    code_projective_geometry_search.add_argument("--max-trials", type=int, default=70)
    code_projective_geometry_search.add_argument("--max-collisions", type=int, default=4)
    code_projective_geometry_search.add_argument("--tuple-size", type=int, default=2)
    code_projective_geometry_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_projective_geometry_search.add_argument("--projective-map-cap", type=int, default=250_000)
    code_projective_geometry_search.add_argument("--canonical-max-assignments", type=int, default=200_000)
    code_projective_geometry_search.add_argument("--seed", type=int, default=0)
    code_projective_geometry_search.add_argument("--max-verbose-audits", type=int, default=4)
    code_projective_geometry_search.add_argument("--no-registry", action="store_true")
    code_projective_geometry_search.add_argument("--verbose", action="store_true")
    code_projective_geometry_search.set_defaults(func=command_code_projective_geometry_search)


def command_code_projective_geometry_search(args: argparse.Namespace) -> int:
    from qsearch import (
        ProjectiveGeometrySearchSpec,
        initialize_seed_registry,
        validate_registry,
        write_projective_geometry_code_search,
    )
    initialize_seed_registry(overwrite=False)
    specs = []
    for raw_spec in args.specs.split(";"):
        if not raw_spec.strip():
            continue
        parts = [int(item.strip()) for item in raw_spec.split(",")]
        if len(parts) != 2:
            raise ValueError("each projective-geometry spec must be field_order,puncture_size")
        field_order, puncture_size = parts
        specs.append(
            ProjectiveGeometrySearchSpec(
                id=f"pg2-f{field_order}-k{puncture_size}",
                field_order=field_order,
                puncture_size=puncture_size,
                max_trials=args.max_trials,
                max_collisions=args.max_collisions,
                tuple_size=args.tuple_size,
                seed=args.seed + field_order * 100 + puncture_size,
            )
        )
    payload = write_projective_geometry_code_search(
        specs=specs or None,
        projective_map_cap=args.projective_map_cap,
        tuple_cap=args.tuple_cap,
        canonical_max_assignments=args.canonical_max_assignments,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Projective-geometry incidence-code search complete")
    print("Artifact: research/code_equivalence/projective_geometry_code_search.json")
    print(f"Searches: {metrics['search_count']}")
    print(f"Codes sampled: {metrics['code_count']}")
    print(f"Tuple/control collisions: {metrics['tuple_collision_count']}")
    print(f"Support-line-profile candidates: {metrics.get('support_line_profile_collision_count', 0)}")
    print(f"Projective-linear controls: {metrics['projective_control_count']}")
    print(f"Classical rejections: {metrics['structural_rejection_count'] + metrics['tuple_profile_rejection_count'] + metrics['low_weight_rejection_count'] + metrics['canonicalization_rejection_count']}")
    print(f"Proof debt: {metrics['proof_debt_collision_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['spec']['id']} | {record['status']} | "
                f"codes={record['code_count']} controls={record['projective_control_count']} "
                f"line-profile={record.get('support_line_profile_collision_count', 0)} "
                f"proof_debt={record['proof_debt_collision_count']}"
            )
            for audit in (record["control_audits"] + record["collision_audits"])[: args.max_verbose_audits]:
                print(
                    f"  {audit['id']} | {audit.get('collision_source', 'unknown')} | "
                    f"{audit['status']} | maps={audit['projective_support']['maps_checked']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_schur_filtration(subparsers) -> None:
    code_schur_filtration = subparsers.add_parser(
        "code-schur-filtration",
        aliases=["code-schur"],
        help="Apply primal/dual Schur powers and puncture/shortening filtrations to code-equivalence rows.",
    )
    code_schur_filtration.add_argument("--max-power", type=int, default=3)
    code_schur_filtration.add_argument("--max-pairs", type=int, default=160)
    code_schur_filtration.add_argument("--no-registry", action="store_true")
    code_schur_filtration.add_argument("--verbose", action="store_true")
    code_schur_filtration.set_defaults(func=command_code_schur_filtration)


def command_code_schur_filtration(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_code_schur_filtration_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_code_schur_filtration_report(
        max_power=args.max_power,
        max_pairs=args.max_pairs,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code Schur-product filtration complete")
    print("Artifact: research/code_equivalence/code_schur_filtration.json")
    print(f"Pairs: {metrics['input_pair_count']}")
    print(f"Schur rejections: {metrics['schur_rejection_count']}")
    print(f"Equivalent controls: {metrics['equivalent_control_count']}")
    print(f"Proof debt: {metrics['schur_proof_debt_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["family_records"]:
            print(
                f"- {record['triage_row_id']} | {record['status']} | "
                f"rejected={record['rejection_count']} controls={record['equivalent_control_count']} "
                f"proof_debt={record['proof_debt_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_closure_attack(subparsers) -> None:
    code_closure_attack = subparsers.add_parser(
        "code-closure-attack",
        aliases=["code-closure"],
        help="Apply prime-field conductors and local t-closures to code-equivalence rows.",
    )
    code_closure_attack.add_argument("--t", type=int, default=2)
    code_closure_attack.add_argument("--max-pairs", type=int, default=160)
    code_closure_attack.add_argument("--no-registry", action="store_true")
    code_closure_attack.add_argument("--verbose", action="store_true")
    code_closure_attack.set_defaults(func=command_code_closure_attack)


def command_code_closure_attack(args: argparse.Namespace) -> int:
    from qsearch import (
        initialize_seed_registry,
        validate_registry,
        write_code_closure_attack_report,
    )
    initialize_seed_registry(overwrite=False)
    payload = write_code_closure_attack_report(
        t=args.t,
        max_pairs=args.max_pairs,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Code conductor/t-closure attack complete")
    print("Artifact: research/code_equivalence/code_closure_attack.json")
    print(f"Pairs: {metrics['input_pair_count']}")
    print(f"Closure rejections: {metrics['closure_rejection_count']}")
    print(f"Equivalent controls: {metrics['equivalent_control_count']}")
    print(f"Proof debt: {metrics['closure_proof_debt_count']}")
    print(f"Ambient recovery calibrations: {metrics['ambient_recovery_calibration_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["family_records"]:
            print(
                f"- {record['triage_row_id']} | {record['status']} | "
                f"rejected={record['rejection_count']} controls={record['equivalent_control_count']} "
                f"proof_debt={record['proof_debt_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def add_code_triage(subparsers) -> None:
    code_triage = subparsers.add_parser(
        "code-triage",
        help="Aggregate code-equivalence rows across structural, tuple, canonicalization, and QC baselines.",
    )
    code_triage.add_argument("--no-registry", action="store_true")
    code_triage.add_argument("--verbose", action="store_true")
    code_triage.set_defaults(func=command_code_triage)


def command_code_triage(args: argparse.Namespace) -> int:
    from qsearch import initialize_seed_registry, validate_registry, write_code_frontier_triage
    initialize_seed_registry(overwrite=False)
    payload = write_code_frontier_triage(write_registry=not args.no_registry)
    validation = validate_registry()
    print("Code frontier triage complete")
    print("Artifact: research/code_equivalence/code_frontier_triage.json")
    print(f"Rows: {payload['headline_metrics']['record_count']}")
    print(f"Rejected rows: {payload['headline_metrics']['rejected_row_count']}")
    print(f"Proof-debt rows: {payload['headline_metrics']['proof_debt_row_count']}")
    print(f"Control/no-hard rows: {payload['headline_metrics']['control_or_no_hard_row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(f"- {record['row_id']} | {record['final_status']} | evidence={len(record['evidence'])}")
            for item in record["evidence"][:6]:
                print(f"  {item['source']} | {item['status']} | {item['verdict']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0
