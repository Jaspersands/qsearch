"""Q-Search research-lab CLI.

Commands:
  python qsearch.py audit
  python qsearch.py literature
  python qsearch.py hypothesize
  python qsearch.py hidden-shift
  python qsearch.py dcp-samples
  python qsearch.py dcp-decode
  python qsearch.py dcp-recurrence
  python qsearch.py dcp-schedules
  python qsearch.py dcp-uniform-schedules
  python qsearch.py dcp-bad-registers
  python qsearch.py dcp-contamination
  python qsearch.py dcp-witness-search
  python qsearch.py dcp-clifford-witnesses
  python qsearch.py dcp-clifford-contamination
  python qsearch.py dcp-hadamard-scaling
  python qsearch.py dcp-random-decoder
  python qsearch.py dcp-decoder-frontier
  python qsearch.py dcp-multiscale-aliasing
  python qsearch.py dcp-fourier-bridge
  python qsearch.py dcp-sparse-fourier-audit
  python qsearch.py dcp-iid-hash-audit
  python qsearch.py dcp-biased-linear-audit
  python qsearch.py dcp-multirecord-audit
  python qsearch.py dcp-ustatistic-audit
  python qsearch.py dcp-factorized-contraction
  python qsearch.py dcp-low-rank-contraction
  python qsearch.py dcp-subset-sum-measurement
  python qsearch.py dcp-hashed-fiber-measurement
  python qsearch.py dcp-reference-projection
  python qsearch.py dcp-covariant-pgm
  python qsearch.py dcp-contaminated-pgm
  python qsearch.py dcp-subset-sum-bridge
  python qsearch.py dcp-subset-sum-lattice
  python qsearch.py dcp-subset-sum-two-adic
  python qsearch.py dcp-subset-sum-resource-frontier
  python qsearch.py dcp-subset-sum-carry-anf
  python qsearch.py dcp-subset-sum-synthesize
  python qsearch.py dcp-subset-sum-low-bit-bdd
  python qsearch.py dcp-subset-sum-conditioned-quotient
  python qsearch.py dcp-subset-sum-carry-slice-lattice
  python qsearch.py dcp-carry-high-part
  python qsearch.py dcp-boolean-coset-separation
  python qsearch.py dcp-marker-list-decoder
  python qsearch.py dcp-marker-deviations
  python qsearch.py dcp-marker-all-targets
  python qsearch.py dcp-subset-sum-target-distribution
  python qsearch.py dcp-coherent-matching
  python qsearch.py dcp-quantum-relation-fidelity
  python qsearch.py dcp-quantum-walk-source-audit
  python qsearch.py dcp-symmetric-relation-lift
  python qsearch.py dcp-fiber-transport
  python qsearch.py dcp-fiber-graph
  python qsearch.py dcp-signed-permutation-transport
  python qsearch.py dcp-affine-transport
  python qsearch.py dcp-fiber-balance
  python qsearch.py dcp-partial-relations
  python qsearch.py dcp-target-locality
  python qsearch.py dcp-fiber-entanglement
  python qsearch.py dcp-adaptive-layouts
  python qsearch.py dcp-subset-sum-randomize
  python qsearch.py dcp-odd-unit-geometry
  python qsearch.py dcp-likelihood-search
  python qsearch.py coset-state
  python qsearch.py collective-observables
  python qsearch.py code-family-search
  python qsearch.py tensor-observables
  python qsearch.py gm-switching
  python qsearch.py cfi-scaling
  python qsearch.py cfi-base-search
  python qsearch.py cfi-parity-solver
  python qsearch.py cfi-structural-decoder
  python qsearch.py cfi-irregular-decoder
  python qsearch.py cfi-bipartite-decoder
  python qsearch.py cfi-code-reduction
  python qsearch.py code-hull-projector
  python qsearch.py individualized-wl
  python qsearch.py individualized-tensors
  python qsearch.py coset-triage
  python qsearch.py representation-obstructions
  python qsearch.py weak-fourier
  python qsearch.py coset-distinguishability
  python qsearch.py coset-pgm
  python qsearch.py coset-holevo
  python qsearch.py coset-covariant-frame
  python qsearch.py coset-two-copy-frame
  python qsearch.py coset-two-copy-transitions
  python qsearch.py coset-three-copy-recoupling
  python qsearch.py coset-commutant-gap-scaling
  python qsearch.py coset-commutant-gap-proof
  python qsearch.py coset-racah-control
  python qsearch.py coset-racah-complete-control
  python qsearch.py coset-racah-hierarchical-control
  python qsearch.py coset-racah-gap-scaling
  python qsearch.py coset-racah-sparse-gap
  python qsearch.py coset-racah-trace-conjecture
  python qsearch.py coset-racah-trace-proof
  python qsearch.py coset-racah-second-moment-proof
  python qsearch.py coset-recoupling-capabilities
  python qsearch.py coset-recoupling-synthesize
  python qsearch.py code-equivalence
  python qsearch.py code-invariants
  python qsearch.py code-info-sets
  python qsearch.py code-canonicalize
  python qsearch.py code-profile-search
  python qsearch.py code-tuple-profiles
  python qsearch.py code-low-weight
  python qsearch.py code-qc-search
  python qsearch.py code-qc-canonicalize
  python qsearch.py code-qc-info-resolve
  python qsearch.py code-cyclic-search
  python qsearch.py code-bch-search
  python qsearch.py code-goppa-search
  python qsearch.py code-goppa-scaling
  python qsearch.py code-goppa-syzygies
  python qsearch.py code-goppa-projectors
  python qsearch.py code-tanner-search
  python qsearch.py code-rm-search
  python qsearch.py code-rank-metric-search
  python qsearch.py code-incidence-resolve
  python qsearch.py code-ag-search
  python qsearch.py code-pg-search
  python qsearch.py code-schur-filtration
  python qsearch.py code-closure-attack
  python qsearch.py code-triage
  python qsearch.py dequantize
  python qsearch.py baselines
  python qsearch.py query-lower-bounds
  python qsearch.py learnability
  python qsearch.py fourier-learnability
  python qsearch.py character-shift
  python qsearch.py character-decoders
  python qsearch.py character-query-info
  python qsearch.py character-complexity
  python qsearch.py phase-naturalness
  python qsearch.py trace-functions
  python qsearch.py family-triage
  python qsearch.py run EXPERIMENT_ID
  python qsearch.py run-next
  python qsearch.py trends
  python qsearch.py proofs
  python qsearch.py reductions
  python qsearch.py reduction-contracts
  python qsearch.py proof-queue
  python qsearch.py sweep
  python qsearch.py conjectures
  python qsearch.py mutate
  python qsearch.py quarantine-invalid
  python qsearch.py blockers
  python qsearch.py frontiers
  python qsearch.py query-models
  python qsearch.py dcp-subset-sum-preconditioned-geometry
  python qsearch.py dcp-subset-sum-fourth-moment
  python qsearch.py dcp-subset-sum-smith-moments
  python qsearch.py dcp-subset-sum-smith-transfer
  python qsearch.py dcp-subset-sum-fixed-moments
  python qsearch.py dcp-subset-sum-conditioned-tail
  python qsearch.py dcp-subset-sum-growing-moments
  python qsearch.py dcp-subset-sum-embedding-volume
  python qsearch.py dcp-subset-sum-short-relations
  python qsearch.py dcp-subset-sum-carry-relations
  python qsearch.py dcp-subset-sum-marker-coset
  python qsearch.py dcp-subset-sum-affine-cvp
  python qsearch.py dcp-subset-sum-affine-scaling
  python qsearch.py dcp-subset-sum-affine-bdd
  python qsearch.py ingest-papers PATH
  python qsearch.py propose
  python qsearch.py validate
  python qsearch.py list
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from blocker_taxonomy import write_blocker_taxonomy
from affine_geometry_code_search import AffineGeometrySearchSpec, write_affine_geometry_code_search
from bch_code_search import BCHSearchSpec, write_bch_code_search
from candidate_quarantine import quarantine_exact_access_invalid_mutations
from character_decoder_search import write_character_decoder_search_report
from character_query_information import write_character_query_information_report
from character_shift_complexity import write_character_shift_complexity_report
from character_shift_baselines import write_character_shift_report
from cfi_bipartite_structural_decoder import write_bipartite_cfi_structural_decoder_report
from cfi_code_reduction import write_cfi_graph_code_reduction
from cfi_parity_solver import write_cfi_parity_solver_report
from cfi_scaling_probe import write_cfi_scaling_probe
from cfi_base_family_search import write_cfi_base_family_search
from cfi_irregular_structural_decoder import write_irregular_cfi_structural_decoder_report
from cfi_structural_decoder import write_cfi_structural_decoder_report
from code_canonicalization_baseline import write_code_canonicalization_baseline
from code_closure_attack import write_code_closure_attack_report
from code_family_search import write_code_family_search
from code_frontier_triage import write_code_frontier_triage
from code_hull_projector_reduction import write_hull_projector_reduction
from code_incidence_resolver import write_code_incidence_resolver
from code_low_weight_structure import write_code_low_weight_structure
from code_profile_collision_search import write_profile_collision_search
from code_schur_filtration import write_code_schur_filtration_report
from code_tuple_profile_baseline import write_code_tuple_profile_baseline
from cyclic_code_search import CyclicCodeSearchSpec, write_cyclic_code_search
from dcp_recurrence_analysis import write_dcp_recurrence_report
from dcp_bad_register_audit import write_dcp_bad_register_report
from dcp_contamination_witness import write_contamination_witness_report
from dcp_collective_witness_search import write_collective_witness_search
from dcp_clifford_witness_search import write_clifford_witness_search
from dcp_clifford_contamination import write_clifford_contamination_report
from dcp_hadamard_scaling import write_hadamard_scaling_report
from dcp_random_design_decoder import write_random_design_decoder_report
from dcp_decoder_frontier import write_decoder_frontier
from dcp_multiscale_aliasing_audit import write_multiscale_aliasing_report
from dcp_hidden_number_bridge import write_hidden_number_bridge_report
from dcp_sparse_fourier_transfer_audit import write_sparse_fourier_transfer_report
from dcp_iid_hash_estimator_audit import write_iid_hash_estimator_report
from dcp_biased_linear_margin_audit import write_biased_linear_margin_report
from dcp_multirecord_estimator_hierarchy import write_multirecord_hierarchy_report
from dcp_ustatistic_variance_audit import write_ustatistic_variance_report
from dcp_factorized_contraction_audit import write_factorized_contraction_report
from dcp_low_rank_contraction_search import write_low_rank_contraction_search
from dcp_subset_sum_measurement_audit import write_subset_sum_measurement_audit
from dcp_hashed_fiber_measurement_audit import write_hashed_fiber_measurement_audit
from dcp_reference_projection_audit import write_reference_projection_audit
from dcp_covariant_pgm_audit import write_covariant_pgm_audit
from dcp_contaminated_pgm_audit import write_contaminated_pgm_audit
from dcp_subset_sum_bridge import write_subset_sum_bridge_audit
from dcp_subset_sum_lattice_search import write_subset_sum_lattice_search
from dcp_subset_sum_two_adic_search import write_subset_sum_two_adic_search
from dcp_subset_sum_resource_frontier import write_subset_sum_resource_frontier
from dcp_subset_sum_carry_anf import write_subset_sum_carry_anf_audit
from dcp_subset_sum_solver_synthesis import write_subset_sum_solver_synthesis
from dcp_subset_sum_low_bit_bdd import write_subset_sum_low_bit_bdd_audit
from dcp_subset_sum_conditioned_quotient import write_conditioned_quotient_audit
from dcp_subset_sum_preconditioned_geometry import write_preconditioned_geometry_audit
from dcp_subset_sum_fourth_moment_obstruction import write_fourth_moment_obstruction
from dcp_subset_sum_smith_moment_spectrum import write_smith_moment_spectrum
from dcp_subset_sum_smith_transfer import write_smith_transfer_order_six
from dcp_subset_sum_fixed_order_moment_theorem import write_fixed_order_moment_theorem
from dcp_subset_sum_conditioned_tail_theorem import write_conditioned_tail_theorem
from dcp_subset_sum_growing_order_theorem import write_growing_order_theorem
from dcp_subset_sum_embedding_volume_theorem import write_embedding_volume_theorem
from dcp_subset_sum_short_relation_theorem import write_short_relation_theorem
from dcp_subset_sum_carry_relation_theorem import write_carry_relation_theorem
from dcp_subset_sum_marker_coset_theorem import write_marker_coset_theorem
from dcp_subset_sum_affine_cvp_baseline import write_affine_cvp_baseline
from dcp_subset_sum_affine_cvp_scaling import write_affine_cvp_scaling
from dcp_subset_sum_affine_bdd_geometry import write_affine_bdd_geometry
from dcp_subset_sum_carry_slice_lattice import write_carry_slice_lattice_search
from dcp_carry_high_part_no_go import write_carry_high_part_no_go
from dcp_subset_sum_boolean_coset_separation import write_boolean_coset_separation
from dcp_marker_aware_list_decoder import (
    load_and_register_marker_aware_list_decoder,
    write_marker_aware_list_decoder,
)
from dcp_marker_deviation_geometry import write_marker_deviation_geometry
from dcp_marker_all_target_coverage import write_marker_all_target_coverage
from dcp_subset_sum_target_distribution import write_target_distribution_audit
from dcp_coherent_matching_interface import write_coherent_matching_interface_audit
from dcp_quantum_relation_fidelity import write_quantum_relation_fidelity_audit
from dcp_quantum_walk_source_audit import write_quantum_walk_source_audit
from dcp_symmetric_relation_lift import write_symmetric_relation_lift_audit
from dcp_two_adic_fiber_transport import write_two_adic_fiber_transport_audit
from dcp_fiber_transport_graph import write_fiber_transport_graph_audit
from dcp_signed_permutation_transport import write_signed_permutation_transport_audit
from dcp_affine_transport import write_affine_transport_audit
from dcp_fiber_balance_obstruction import write_fiber_balance_obstruction_audit
from dcp_partial_relation_coverage import write_partial_relation_coverage_audit
from dcp_target_indexed_locality import write_target_indexed_locality_audit
from dcp_fiber_entanglement import write_fiber_entanglement_audit
from dcp_adaptive_layout_audit import write_adaptive_layout_audit
from dcp_subset_sum_random_self_reduction import write_random_self_reduction_audit
from dcp_odd_unit_orbit_geometry import write_odd_unit_orbit_geometry_audit
from dcp_likelihood_branch_bound import write_likelihood_branch_bound_report
from dcp_recursive_decoder import write_recursive_decoder_report
from dcp_schedule_search import write_dcp_schedule_search_report
from dcp_uniform_schedule_family import write_dcp_uniform_schedule_report
from dcp_sample_workbench import write_dcp_sample_workbench
from goppa_code_search import GoppaSearchSpec, write_goppa_code_search
from goppa_scaling_frontier import write_goppa_scaling_frontier
from goppa_syzygy_frontier import write_goppa_syzygy_frontier
from goppa_hull_projector_frontier import write_goppa_hull_projector_frontier
from qc_information_set_resolver import write_qc_information_set_resolver
from rank_metric_code_search import RankMetricSearchSpec, write_rank_metric_code_search
from reed_muller_code_search import ReedMullerSearchSpec, write_reed_muller_code_search
from tanner_code_search import TannerSearchSpec, write_tanner_code_search
from collective_observable_search import write_collective_observable_search
from coset_frontier_triage import write_coset_frontier_triage
from coset_state_distinguishability import write_coset_distinguishability_report
from coset_state_workbench import write_coset_workbench
from coset_pgm_capacity import write_coset_pgm_capacity_report
from coset_holevo_information import write_coset_holevo_report
from coset_covariant_frame import write_covariant_frame_report
from coset_two_copy_frame import write_two_copy_frame_report
from coset_two_copy_transition_audit import write_two_copy_transition_report
from coset_three_copy_recoupling_obstruction import write_three_copy_recoupling_report
from coset_jucys_murphy_label_transform import write_jucys_murphy_label_transform_report
from coset_multiplicity_commutant_search import write_multiplicity_commutant_report
from coset_commutant_gap_scaling import write_commutant_gap_scaling_report
from coset_commutant_gap_certificate import write_commutant_gap_certificate
from coset_restricted_racah_control import write_restricted_racah_control_report
from coset_complete_racah_control import write_complete_racah_control_report
from coset_hierarchical_racah_control import write_hierarchical_racah_control_report
from coset_hierarchical_gap_scaling import write_hierarchical_gap_scaling_report
from coset_sparse_stable_gap_probe import write_sparse_stable_gap_report
from coset_stable_trace_conjecture import write_stable_trace_conjecture_report
from coset_stable_trace_certificate import write_stable_trace_certificate
from coset_stable_second_moment_certificate import (
    write_stable_second_moment_certificate,
)
from coset_recoupling_capability_ledger import write_recoupling_capability_report
from coset_recoupling_mechanism_synthesis import write_recoupling_mechanism_synthesis_report
from classical_baseline_suite import write_hidden_shift_baselines
from character_moment_obstruction import write_character_moment_obstruction_report
from code_equivalence_workbench import write_code_equivalence_workbench
from code_information_set_baseline import write_code_information_set_baseline
from code_structural_invariants import write_code_structural_invariants
from conjecture_tracker import write_conjecture_report
from dequantization_checks import write_dequantization_report
from experiment_runner import (
    run_experiment,
    run_next_experiment,
    run_supported_experiments,
    select_next_experiment,
    supported_experiment_ids,
    write_experiment_trends,
)
from fourier_compressibility_baselines import write_fourier_compressibility_report
from graphlet_tensor_observables import write_graphlet_tensor_observables
from godsil_mckay_search import write_godsil_mckay_search
from character_shift_lower_bound import write_character_shift_lower_bound_report
from hidden_shift_query_lower_bounds import write_hidden_shift_query_lower_bounds
from individualized_tensor_observables import write_individualized_tensor_observables
from individualized_wl_baseline import write_individualized_wl_baseline
from literature_radar import write_literature_index
from literature_pipeline import hypothesize_from_literature, write_literature_records
from learnability_baselines import write_learnability_report
from mutation_engine import write_mutation_report
from paper_ingestion import write_paper_ingestion, write_paper_ingestion_with_arxiv
from phase_family_naturalness import write_phase_family_naturalness_report
from phase_family_triage import write_phase_family_triage
from phase_state_workbench import write_hidden_shift_workbench
from problem_ontology import write_problem_ontology
from projective_geometry_code_search import ProjectiveGeometrySearchSpec, write_projective_geometry_code_search
from proof_tracker import write_proof_status_report
from proof_work_queue import write_proof_work_queue
from query_model_ledger import write_query_model_ledger
from quasi_cyclic_canonicalization import write_qc_canonicalization_report
from quasi_cyclic_code_search import write_quasi_cyclic_code_search
from representation_obstruction import write_representation_obstruction_report
from reduction_contract_audit import CONTRACT_AUDIT_PATH, write_reduction_contract_audit
from reduction_gate import write_reduction_ledger
from reduction_theorem_catalog import write_theorem_catalog
from research_engine import build_agenda, write_outputs
from research_frontier_map import write_frontier_map
from research_lab import write_research_audit
from trace_function_search import write_trace_function_search_report
from weak_fourier_signal import write_weak_fourier_signal_report
from research_registry import (
    CANDIDATES_PATH,
    EXPERIMENTS_PATH,
    NEGATIVE_RESULTS_PATH,
    REJECTED_CANDIDATES_PATH,
    CandidateRecord,
    import_legacy_negative_results,
    initialize_seed_registry,
    load_candidates,
    load_conjectures,
    load_dequantization_checks,
    load_experiment_results,
    load_experiments,
    load_mutation_proposals,
    load_negative_results,
    load_proof_status,
    load_rejected_candidates,
    load_reduction_ledger,
    load_scaling_runs,
    registry_summary,
    upsert_candidate,
    validate_registry,
)
from scaling_runner import parse_int_csv, write_hidden_shift_sweep


def command_audit(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    output_dir = args.output_dir
    agenda = build_agenda(root)
    write_outputs(agenda, output_dir)
    write_research_audit(agenda, root, output_dir)
    write_literature_index(output_dir / "literature_index.json", refresh_arxiv=args.refresh_arxiv)
    write_problem_ontology(output_dir / "problem_ontology.json")
    initialize_seed_registry(overwrite=args.overwrite_registry)
    imported = import_legacy_negative_results(root)
    validation = validate_registry()

    print("Q-Search audit complete")
    print(f"Agenda: {output_dir / 'agenda.json'}")
    print(f"Registry candidates: {CANDIDATES_PATH}")
    print(f"Registry experiments: {EXPERIMENTS_PATH}")
    print(f"Negative results: {NEGATIVE_RESULTS_PATH}")
    print(f"Imported legacy negative results: {imported}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_propose(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    if args.file:
        payload = json.loads(args.file.read_text())
        candidate = CandidateRecord(**payload)
        upsert_candidate(candidate)
        print(f"Accepted candidate: {candidate.id}")
    else:
        print("Seed proof-gated candidates are registered.")
    print(registry_summary())
    return 0


def command_literature(args: argparse.Namespace) -> int:
    write_literature_index(args.output_dir / "literature_index.json", refresh_arxiv=args.refresh_arxiv)
    records = write_literature_records(
        args.output_dir / "literature_records.json",
        refresh_arxiv=args.refresh_arxiv,
        max_arxiv_results=args.max_arxiv_results,
    )
    print(f"Structured literature records: {len(records)}")
    print(f"Literature records: {args.output_dir / 'literature_records.json'}")
    if args.verbose:
        for record in records:
            print(f"- {record['id']} | {record['mechanism']}")
    return 0


def command_hypothesize(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    write_literature_records(
        Path("research/literature_records.json"),
        refresh_arxiv=args.refresh_arxiv,
        max_arxiv_results=args.max_arxiv_results,
    )
    result = hypothesize_from_literature(refresh_arxiv=args.refresh_arxiv, max_arxiv_results=args.max_arxiv_results)
    validation = validate_registry()
    print("Literature hypothesis generation complete")
    print(f"Accepted candidates: {', '.join(result.accepted) if result.accepted else 'none'}")
    print(f"Rejected candidates: {', '.join(result.rejected) if result.rejected else 'none'}")
    print(f"Generated experiments: {', '.join(result.experiments) if result.experiments else 'none'}")
    print(f"Candidate registry: {CANDIDATES_PATH}")
    print(f"Rejected registry: {REJECTED_CANDIDATES_PATH}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_hidden_shift(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_hidden_shift_workbench(
        families=families,
        min_bits=args.min_bits,
        max_bits=args.max_bits,
        shift=args.shift,
        sieve_samples=args.sieve_samples,
        seed=args.seed,
        sample_count=args.sample_count,
        write_registry=not args.no_registry,
    )
    dcp_payload = write_dcp_sample_workbench(
        sample_count=args.sieve_samples,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    decoder_payload = write_recursive_decoder_report(
        n_values=(max(4, args.max_bits),),
        trials_per_size=3,
        samples_per_stage=args.sieve_samples,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Hidden-shift/DHSP workbench complete")
    print("Artifact: research/phase_workbench/hidden_shift_audit.json")
    print(f"Family audits: {len(payload['family_audits'])}")
    print(f"Summary: {payload['summary']}")
    print(
        "Legacy idealized phase-label trace: "
        f"v2={payload['sieve_baseline']['best_two_adic_valuation']}/"
        f"{payload['sieve_baseline']['target_two_adic_valuation']} "
        f"from {payload['sieve_baseline']['initial_states']} labels"
    )
    print(
        "DCP state-sample baseline: "
        f"trials={dcp_payload['headline_metrics']['trial_count']} "
        f"evaluator_queries={dcp_payload['headline_metrics']['evaluator_query_count']} "
        f"postselection_gap={dcp_payload['headline_metrics']['postselection_optimism_gap']} "
        f"full_decodes={dcp_payload['headline_metrics']['full_hidden_reflection_decode_count']}"
    )
    print("DCP artifact: research/phase_workbench/dcp_sample_native_sieve.json")
    print(
        "Recursive DCP decoder: "
        f"full_recoveries={decoder_payload['headline_metrics']['empirical_full_recovery_count']}/"
        f"{decoder_payload['headline_metrics']['recursive_trial_count']} "
        f"proved_failure_bounds={decoder_payload['headline_metrics']['proved_full_failure_bound_count']}"
    )
    print("Decoder artifact: research/phase_workbench/dcp_recursive_decoder.json")
    print(
        "Phase-state trace: "
        f"strategy={payload['phase_state_trace']['strategy']} "
        f"v2={payload['phase_state_trace']['best_two_adic_valuation']}/"
        f"{payload['phase_state_trace']['target_two_adic_valuation']} "
        f"survivors={payload['phase_state_trace']['final_state_count']}"
    )
    print(f"Falsifiers triggered: {len(payload['falsifiers_triggered'])}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_dcp_samples(args: argparse.Namespace) -> int:
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


def command_dcp_decode(args: argparse.Namespace) -> int:
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


def command_dcp_recurrence(args: argparse.Namespace) -> int:
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


def command_dcp_schedules(args: argparse.Namespace) -> int:
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


def command_dcp_uniform_schedules(args: argparse.Namespace) -> int:
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


def command_dcp_bad_registers(args: argparse.Namespace) -> int:
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


def command_dcp_contamination(args: argparse.Namespace) -> int:
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


def command_dcp_witness_search(args: argparse.Namespace) -> int:
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


def command_dcp_clifford_witnesses(args: argparse.Namespace) -> int:
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


def command_dcp_clifford_contamination(args: argparse.Namespace) -> int:
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


def command_dcp_hadamard_scaling(args: argparse.Namespace) -> int:
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


def command_dcp_random_decoder(args: argparse.Namespace) -> int:
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


def command_dcp_decoder_frontier(args: argparse.Namespace) -> int:
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


def command_dcp_multiscale_aliasing(args: argparse.Namespace) -> int:
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


def command_dcp_fourier_bridge(args: argparse.Namespace) -> int:
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


def command_dcp_sparse_fourier_audit(args: argparse.Namespace) -> int:
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


def command_dcp_iid_hash_audit(args: argparse.Namespace) -> int:
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


def command_dcp_biased_linear_audit(args: argparse.Namespace) -> int:
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


def command_dcp_multirecord_audit(args: argparse.Namespace) -> int:
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


def command_dcp_ustatistic_audit(args: argparse.Namespace) -> int:
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


def command_dcp_factorized_contraction(args: argparse.Namespace) -> int:
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


def command_dcp_low_rank_contraction(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_measurement(args: argparse.Namespace) -> int:
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


def command_dcp_hashed_fiber_measurement(args: argparse.Namespace) -> int:
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


def command_dcp_reference_projection(args: argparse.Namespace) -> int:
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


def command_dcp_covariant_pgm(args: argparse.Namespace) -> int:
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


def command_dcp_contaminated_pgm(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_bridge(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_lattice(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_two_adic(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_resource_frontier(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_carry_anf(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_synthesize(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_low_bit_bdd(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_conditioned_quotient(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_preconditioned_geometry(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_fourth_moment(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_smith_moments(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_smith_transfer(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_fixed_moments(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_conditioned_tail(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_growing_moments(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_embedding_volume(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_short_relations(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_carry_relations(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_marker_coset(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_affine_cvp(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_affine_scaling(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_affine_bdd(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_carry_slice_lattice(args: argparse.Namespace) -> int:
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


def command_dcp_carry_high_part(args: argparse.Namespace) -> int:
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


def command_dcp_boolean_coset_separation(args: argparse.Namespace) -> int:
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


def command_dcp_marker_list_decoder(args: argparse.Namespace) -> int:
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


def command_dcp_marker_deviations(args: argparse.Namespace) -> int:
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


def command_dcp_marker_all_targets(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_target_distribution(args: argparse.Namespace) -> int:
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


def command_dcp_coherent_matching(args: argparse.Namespace) -> int:
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
        "Arbitrary quantum relation bridges: "
        f"{metrics['proved_arbitrary_quantum_relation_solver_bridge_count']}"
    )
    print(f"Partial subset-sum solvers: {metrics['proved_polynomial_partial_subset_sum_solver_count']}")
    print(f"Speedup claim allowed: {payload['claim_gate']['speedup_claim_allowed']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_dcp_quantum_relation_fidelity(args: argparse.Namespace) -> int:
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


def command_dcp_quantum_walk_source_audit(args: argparse.Namespace) -> int:
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


def command_dcp_symmetric_relation_lift(args: argparse.Namespace) -> int:
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


def command_dcp_fiber_transport(args: argparse.Namespace) -> int:
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


def command_dcp_fiber_graph(args: argparse.Namespace) -> int:
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


def command_dcp_signed_permutation_transport(args: argparse.Namespace) -> int:
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


def command_dcp_affine_transport(args: argparse.Namespace) -> int:
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


def command_dcp_fiber_balance(args: argparse.Namespace) -> int:
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


def command_dcp_partial_relations(args: argparse.Namespace) -> int:
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


def command_dcp_target_locality(args: argparse.Namespace) -> int:
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


def command_dcp_fiber_entanglement(args: argparse.Namespace) -> int:
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


def command_dcp_adaptive_layouts(args: argparse.Namespace) -> int:
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


def command_dcp_subset_sum_randomize(args: argparse.Namespace) -> int:
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


def command_dcp_odd_unit_geometry(args: argparse.Namespace) -> int:
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


def command_dcp_likelihood_search(args: argparse.Namespace) -> int:
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


def command_coset_state(args: argparse.Namespace) -> int:
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


def command_collective_observables(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_collective_observable_search(
        pair_ids=pair_ids,
        tuple_cap=args.tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Collective-observable search complete")
    print("Artifact: research/coset_workbench/collective_observable_search.json")
    print(f"Pairs: {payload['headline_metrics']['pair_count']}")
    print(f"Observables: {payload['headline_metrics']['observable_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for audit in payload["pair_audits"]:
            print(f"- {audit['pair']['id']} | {audit['boundary_status']}")
            for record in audit["observable_records"]:
                print(
                    f"  {record['observable_name']} | {record['status']} | "
                    f"registers={record['register_count']} shadow={record['classical_shadow']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_code_family_search(args: argparse.Namespace) -> int:
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


def command_tensor_observables(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_graphlet_tensor_observables(
        pair_ids=pair_ids,
        tuple_cap=args.tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Graphlet tensor observable audit complete")
    print("Artifact: research/coset_workbench/graphlet_tensor_observables.json")
    print(f"Pairs: {payload['headline_metrics']['pair_count']}")
    print(f"Observables: {payload['headline_metrics']['observable_count']}")
    print(f"Classical-shadow collapses: {payload['headline_metrics']['classical_shadow_collapse_count']}")
    print(f"Boundary pairs: {payload['headline_metrics']['boundary_pair_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for audit in payload["pair_audits"]:
            print(f"- {audit['pair']['id']} | {audit['status']}")
            for record in audit["records"]:
                print(
                    f"  {record['observable_name']} | {record['status']} | "
                    f"bond={record['bond_dimension']} shadow={record['classical_shadow']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_gm_switching(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    payload = write_godsil_mckay_search(write_registry=not args.no_registry)
    validation = validate_registry()
    print("Godsil-McKay switching search complete")
    print("Artifact: research/coset_workbench/godsil_mckay_switching_search.json")
    print(f"Families: {payload['headline_metrics']['family_count']}")
    print(f"Rows: {payload['headline_metrics']['row_count']}")
    print(f"Non-isomorphic cospectral rows: {payload['headline_metrics']['nonisomorphic_cospectral_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_row_count']}")
    print(f"Survivor rows: {payload['headline_metrics']['survivor_row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for family in payload["family_records"]:
            print(f"- {family['spec']['id']} | {family['status']} | checked={family['subsets_checked']}")
            for record in family["records"]:
                distinguishing = [item["name"] for item in record["baselines"] if item["distinguishes"]]
                print(f"  {record['id']} | {record['status']} | distinguishes={','.join(distinguishing) or 'none'}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_cfi_scaling(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    base_sizes = parse_int_csv(args.base_sizes)
    payload = write_cfi_scaling_probe(
        base_sizes=base_sizes,
        wl2_pair_cap=args.wl2_pair_cap,
        wl_tuple_cap=args.wl_tuple_cap,
        graphlet_tuple_cap=args.graphlet_tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("CFI scaling probe complete")
    print("Artifact: research/coset_workbench/cfi_scaling_probe.json")
    print(f"Base sizes: {payload['base_sizes']}")
    print(f"Boundary rows: {payload['headline_metrics']['boundary_record_count']}")
    print(f"3-WL skips: {payload['headline_metrics']['wl3_skipped_count']}")
    print(f"Graphlet skips: {payload['headline_metrics']['graphlet4_skipped_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- K{record['base_size']} n={record['vertex_count']} | {record['status']} | "
                f"wl3={'eval' if record['wl3_evaluated'] else 'skip'} "
                f"graphlet4={'eval' if record['graphlet4_evaluated'] else 'skip'}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_cfi_base_search(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.base_ids.split(",") if item.strip()]
    payload = write_cfi_base_family_search(
        base_ids=base_ids,
        max_individualization=args.max_individualization,
        tuple_cap=args.tuple_cap,
        exact_vertex_cap=args.exact_vertex_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("CFI base-family search complete")
    print("Artifact: research/coset_workbench/cfi_base_family_search.json")
    print(f"Bases: {payload['headline_metrics']['base_count']}")
    print(f"Individualized-WL dequantized: {payload['headline_metrics']['individualized_wl_dequantized_count']}")
    print(f"Proof-debt survivors: {payload['headline_metrics']['proof_debt_survivor_count']}")
    print(f"Finite survivors: {payload['headline_metrics']['finite_survivor_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base']['id']} cfi_n={record['cfi_vertex_count']} | {record['status']} | "
                f"first_indiv={record['first_individualized_separator']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_cfi_parity_solver(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    base_sizes = parse_int_csv(args.base_sizes)
    payload = write_cfi_parity_solver_report(
        base_sizes=base_sizes,
        shuffle=not args.no_shuffle,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("CFI parity solver complete")
    print("Artifact: research/coset_workbench/cfi_parity_solver.json")
    print(f"Base sizes: {payload['base_sizes']}")
    print(f"Decoded rows: {payload['headline_metrics']['decoded_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_count']}")
    print(f"Ambiguous controls: {payload['headline_metrics']['ambiguous_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- K{record['base_size']} n={record['vertex_count']} | {record['status']} | "
                f"untwisted={record['untwisted_decode']['global_twist_parity']} "
                f"twisted={record['twisted_decode']['global_twist_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_cfi_structural_decoder(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.base_ids.split(",") if item.strip()]
    payload = write_cfi_structural_decoder_report(
        base_ids=base_ids,
        shuffle=not args.no_shuffle,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("CFI structural decoder complete")
    print("Artifact: research/coset_workbench/cfi_structural_decoder.json")
    print(f"Bases: {payload['base_ids']}")
    print(f"Decoded rows: {payload['headline_metrics']['decoded_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_count']}")
    print(f"Ambiguous rows: {payload['headline_metrics']['ambiguous_count']}")
    print(f"Failed rows: {payload['headline_metrics']['failed_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base_id']} n={record['cfi_vertex_count']} | {record['status']} | "
                f"untwisted={record['untwisted_decode']['global_twist_parity']} "
                f"twisted={record['twisted_decode']['global_twist_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_cfi_irregular_decoder(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.base_ids.split(",") if item.strip()]
    payload = write_irregular_cfi_structural_decoder_report(
        base_ids=base_ids,
        shuffle=not args.no_shuffle,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Irregular CFI structural decoder complete")
    print("Artifact: research/coset_workbench/cfi_irregular_structural_decoder.json")
    print(f"Bases: {payload['base_ids']}")
    print(f"Decoded rows: {payload['headline_metrics']['decoded_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_count']}")
    print(f"Proof debt rows: {payload['headline_metrics']['proof_debt_count']}")
    print(f"Degree-separated rows: {payload['headline_metrics']['degree_separated_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base']['id']} n={record['cfi_vertex_count']} | {record['status']} | "
                f"untwisted={record['untwisted_decode']['global_twist_parity']} "
                f"twisted={record['twisted_decode']['global_twist_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_cfi_bipartite_decoder(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.base_ids.split(",") if item.strip()]
    payload = write_bipartite_cfi_structural_decoder_report(
        base_ids=base_ids,
        shuffle=not args.no_shuffle,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Bipartite CFI structural decoder complete")
    print("Artifact: research/coset_workbench/cfi_bipartite_structural_decoder.json")
    print(f"Bases: {payload['base_ids']}")
    print(f"Decoded rows: {payload['headline_metrics']['decoded_count']}")
    print(f"Dequantized rows: {payload['headline_metrics']['dequantized_count']}")
    print(f"Proof debt rows: {payload['headline_metrics']['proof_debt_count']}")
    print(f"Non-degree-separated rows: {payload['headline_metrics']['non_degree_separated_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base']['id']} n={record['cfi_vertex_count']} | {record['status']} | "
                f"untwisted={record['untwisted_decode']['global_twist_parity']} "
                f"twisted={record['twisted_decode']['global_twist_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_individualized_wl(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_individualized_wl_baseline(
        pair_ids=pair_ids,
        max_individualization=args.max_individualization,
        tuple_cap=args.tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Individualized-WL baseline complete")
    print("Artifact: research/coset_workbench/individualized_wl_baseline.json")
    print(f"Pairs: {payload['headline_metrics']['pair_count']}")
    print(f"Dequantized pairs: {payload['headline_metrics']['dequantized_pair_count']}")
    print(f"Survivor pairs: {payload['headline_metrics']['survivor_pair_count']}")
    print(f"Proof-debt pairs: {payload['headline_metrics']['proof_debt_pair_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for audit in payload["pair_audits"]:
            print(f"- {audit['pair']['id']} | {audit['status']}")
            for record in audit["records"]:
                print(
                    f"  t={record['individualization_size']} | {record['status']} | "
                    f"count={record['tuple_count']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_individualized_tensors(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    pair_ids = [item.strip() for item in args.pairs.split(",") if item.strip()]
    payload = write_individualized_tensor_observables(
        pair_ids=pair_ids,
        max_root_size=args.max_root_size,
        tuple_cap=args.tuple_cap,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Individualized rooted tensor baseline complete")
    print("Artifact: research/coset_workbench/individualized_tensor_observables.json")
    print(f"Pairs: {payload['headline_metrics']['pair_count']}")
    print(f"Dequantized pairs: {payload['headline_metrics']['dequantized_pair_count']}")
    print(f"Survivor pairs: {payload['headline_metrics']['survivor_pair_count']}")
    print(f"Proof-debt pairs: {payload['headline_metrics']['proof_debt_pair_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for audit in payload["pair_audits"]:
            print(f"- {audit['pair']['id']} | {audit['status']}")
            for record in audit["records"]:
                print(
                    f"  roots={record['root_size']} | {record['status']} | "
                    f"extensions={record['extension_tuple_count']}"
                )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_coset_triage(args: argparse.Namespace) -> int:
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


def command_representation_obstructions(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    n_values = parse_int_csv(args.n_values)
    payload = write_representation_obstruction_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Representation obstruction report complete")
    print("Artifact: research/representation/symmetric_group_obstructions.json")
    print(f"n values: {payload['n_values']}")
    print(f"No-go pressure rows: {payload['headline_metrics']['no_go_pressure_count']}")
    print(f"Min low-dimensional mass: {payload['headline_metrics']['min_low_dimension_mass']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- S_{record['n']} partitions={record['partition_count']} | {record['status']} | "
                f"low-dim-mass={record['low_dimension_mass']:.4g} balanced={record['balanced_shape_mass']:.4g}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_weak_fourier(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    n_values = parse_int_csv(args.n_values)
    payload = write_weak_fourier_signal_report(
        n_values=n_values,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Weak Fourier signal audit complete")
    print("Artifact: research/representation/weak_fourier_involution_signal.json")
    print(f"Records: {payload['headline_metrics']['record_count']}")
    print(f"Nearly Plancherel: {payload['headline_metrics']['near_plancherel_count']}")
    print(f"Small signal: {payload['headline_metrics']['small_signal_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- S_{record['n']} {record['involution_type']} r={record['transposition_count']} | "
                f"{record['status']} | tv={record['total_variation_from_plancherel']:.4g} "
                f"low-frac={record['low_dimension_signal_fraction']:.4g}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_coset_distinguishability(args: argparse.Namespace) -> int:
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


def command_coset_pgm(args: argparse.Namespace) -> int:
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


def command_coset_holevo(args: argparse.Namespace) -> int:
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


def command_coset_covariant_frame(args: argparse.Namespace) -> int:
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


def command_coset_two_copy_frame(args: argparse.Namespace) -> int:
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


def command_coset_two_copy_transitions(args: argparse.Namespace) -> int:
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


def command_coset_three_copy_recoupling(args: argparse.Namespace) -> int:
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


def command_coset_recoupling_capabilities(args: argparse.Namespace) -> int:
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


def command_coset_jm_labels(args: argparse.Namespace) -> int:
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


def command_coset_multiplicity_commutant(args: argparse.Namespace) -> int:
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


def command_coset_commutant_gap_scaling(args: argparse.Namespace) -> int:
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


def command_coset_commutant_gap_proof(args: argparse.Namespace) -> int:
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


def command_coset_racah_control(args: argparse.Namespace) -> int:
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


def command_coset_racah_complete_control(args: argparse.Namespace) -> int:
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


def command_coset_racah_hierarchical_control(args: argparse.Namespace) -> int:
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


def command_coset_racah_gap_scaling(args: argparse.Namespace) -> int:
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


def command_coset_racah_sparse_gap(args: argparse.Namespace) -> int:
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


def command_coset_racah_trace_conjecture(args: argparse.Namespace) -> int:
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


def command_coset_racah_trace_proof(args: argparse.Namespace) -> int:
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


def command_coset_racah_second_moment_proof(args: argparse.Namespace) -> int:
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


def command_coset_recoupling_synthesize(args: argparse.Namespace) -> int:
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


def command_code_equivalence(args: argparse.Namespace) -> int:
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


def command_cfi_code_reduction(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    base_ids = [item.strip() for item in args.bases.split(",") if item.strip()]
    payload = write_cfi_graph_code_reduction(
        base_ids=base_ids or None,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Faithful CFI graph-to-code reduction audit complete")
    print("Artifact: research/code_equivalence/cfi_code_reduction.json")
    print(f"Theorem directions certified: {metrics['theorem_direction_count']}")
    print(f"Graph recoveries verified: {metrics['recovery_verified_count']}")
    print(f"Equivalent controls verified: {metrics['equivalent_control_verified_count']}")
    print(f"Promised-family dequantizations: {metrics['promised_decoder_dequantized_count']}")
    print(f"Transferred GI proof debt: {metrics['transferred_gi_proof_debt_count']}")
    print(f"Positive quantum evidence: {metrics['positive_quantum_evidence_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['base_id']} | [{record['code_dimension']},{record['code_length']}] | "
                f"{record['status']} | decoder={record['promised_decoder_recovers_parity']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_code_hull_projector(args: argparse.Namespace) -> int:
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


def command_code_invariants(args: argparse.Namespace) -> int:
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


def command_code_info_sets(args: argparse.Namespace) -> int:
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


def command_code_canonicalize(args: argparse.Namespace) -> int:
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


def command_code_profile_search(args: argparse.Namespace) -> int:
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


def command_code_tuple_profiles(args: argparse.Namespace) -> int:
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


def command_code_low_weight(args: argparse.Namespace) -> int:
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


def command_code_qc_search(args: argparse.Namespace) -> int:
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


def command_code_qc_canonicalize(args: argparse.Namespace) -> int:
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


def command_code_qc_info_resolve(args: argparse.Namespace) -> int:
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


def command_code_cyclic_search(args: argparse.Namespace) -> int:
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


def command_code_bch_search(args: argparse.Namespace) -> int:
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


def command_code_goppa_search(args: argparse.Namespace) -> int:
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


def command_code_goppa_scaling(args: argparse.Namespace) -> int:
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


def command_code_goppa_syzygies(args: argparse.Namespace) -> int:
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


def command_code_goppa_projectors(args: argparse.Namespace) -> int:
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


def command_code_tanner_search(args: argparse.Namespace) -> int:
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


def command_code_reed_muller_search(args: argparse.Namespace) -> int:
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


def command_code_rank_metric_search(args: argparse.Namespace) -> int:
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


def command_code_incidence_resolve(args: argparse.Namespace) -> int:
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


def command_code_affine_geometry_search(args: argparse.Namespace) -> int:
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


def command_code_projective_geometry_search(args: argparse.Namespace) -> int:
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


def command_code_schur_filtration(args: argparse.Namespace) -> int:
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


def command_code_closure_attack(args: argparse.Namespace) -> int:
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


def command_code_triage(args: argparse.Namespace) -> int:
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


def command_dequantize(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    report = write_dequantization_report()
    validation = validate_registry()
    print("Dequantization report complete")
    print("Report: research/dequantization_report.json")
    print("Attack matrix: research/dequantization_attack_matrix.json")
    print("Registry: research/registry/dequantization_checks.json")
    print(f"Findings: {report['finding_count']}")
    print(f"Blocking findings: {report['blocking_finding_count']}")
    matrix_summary = report.get("attack_legality_matrix", {}).get("summary", {})
    if matrix_summary:
        print(
            "Attack matrix: "
            f"{matrix_summary.get('attack_row_count', 0)} attack rows, "
            f"{matrix_summary.get('query_model_row_count', 0)} query-model rows, "
            f"{matrix_summary.get('random_sample_undersampled_gap_count', 0)} undersampled sampled-access gaps"
        )
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for finding in report["findings"]:
            print(f"- {finding['severity']} | {finding['target_id']} | {finding['evidence']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_baselines(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_hidden_shift_baselines(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Classical baseline sweep complete")
    print("Artifact: research/classical_baselines/hidden_shift_baselines.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"random={summary['random_sample_recovery_count']} "
                f"evaluator={summary['low_complexity_evaluator_recovery_count']} "
                f"collision_survival={summary['collision_scale_survival_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_query_lower_bounds(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_hidden_shift_query_lower_bounds(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        trials=args.trials,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Hidden-shift query lower-bound probe complete")
    print("Artifact: research/classical_baselines/hidden_shift_query_lower_bounds.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"poly-fingerprints={summary['poly_sample_unique_count']} "
                f"chosen-poly={summary.get('chosen_query_poly_unique_count', 0)} "
                f"agreement-ceilings={summary.get('agreement_query_ceiling_count', 0)} "
                f"overlap-collisions={summary['overlap_scale_collision_count']} "
                f"undersampled={summary['undersampled_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_learnability(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_learnability_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        samples=args.samples,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Learnability baseline report complete")
    print("Artifact: research/classical_baselines/learnability_baselines.json")
    print(f"Records: {payload['record_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"dequantized={summary['dequantized_low_degree_count']} "
                f"unresolved={summary['high_degree_or_unresolved_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_fourier_learnability(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_fourier_compressibility_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Fourier compressibility baseline report complete")
    print("Artifact: research/classical_baselines/fourier_compressibility_baselines.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"evaluator={summary['explicit_evaluator_sparse_recovery_count']} "
                f"sample={summary['random_sample_sparse_recovery_count']} "
                f"derivative={summary['derivative_sparse_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_character_shift(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_shift_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character shift baseline report complete")
    print("Artifact: research/classical_baselines/character_shift_baselines.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"poly-sample={summary['unique_by_poly_samples_count']} "
                f"exhaustive={summary['exhaustive_time_only_count']} "
                f"insufficient={summary['insufficient_sample_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_character_decoders(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_decoder_search_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character decoder search complete")
    print("Artifact: research/classical_baselines/character_decoder_search.json")
    print(f"Attempts: {payload['attempt_count']}")
    print(f"Probes: {payload['probe_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_verdict']} | "
                f"poly-style={summary['non_exhaustive_success_count']} "
                f"pair-ratio={summary.get('pair_ratio_filter_success_count', 0)} "
                f"algebraic-degree={summary.get('algebraic_degree_exponential_success_count', 0)} "
                f"exhaustive={summary['exhaustive_success_count']} "
                f"invariant={summary['shift_invariant_probe_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_character_lower_bound(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_shift_lower_bound_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        trials=args.trials,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character lower-bound ledger complete")
    print("Artifact: research/classical_baselines/character_shift_lower_bound.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"sample={summary['sample_fingerprint_count']} "
                f"chosen={summary['chosen_query_fingerprint_count']} "
                f"pair-ratio={summary.get('pair_ratio_filter_success_count', 0)} "
                f"max-pair-exp={summary.get('max_pair_ratio_operation_exponent_per_bit', 0.0):.2f} "
                f"gcd={summary['full_degree_gcd_success_count']} "
                f"max-gcd-exp={summary['max_gcd_operation_exponent_per_bit']:.2f}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_character_moments(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_moment_obstruction_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character moment obstruction complete")
    print("Artifact: research/classical_baselines/character_moment_obstruction.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"min-first-nonzero={summary['minimum_first_nonzero_degree']} "
                f"blocked={summary['all_rows_block_low_degree_moments']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_character_query_info(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_query_information_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        failure_probability=args.failure_probability,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Multiplicative-character query information ceiling complete")
    print("Artifact: research/classical_baselines/character_query_information.json")
    print(f"Rows: {payload['row_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"max-union-bound-q={summary['max_union_bound_queries']} "
                f"max-q/logp={summary['max_query_ceiling_over_log2_prime']:.2f} "
                f"killed={summary['query_lower_bound_killed_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_character_complexity(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_character_shift_complexity_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        shift=args.shift,
        max_prefix_factor=args.max_prefix_factor,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    metrics = payload["headline_metrics"]
    print("Multiplicative-character complexity/preprocessing audit complete")
    print("Artifact: research/classical_baselines/character_shift_complexity.json")
    print(f"Rows: {metrics['preprocessing_row_count']}")
    print(f"Fixed-prefix online decodes: {metrics['fixed_prefix_decode_success_count']}")
    print(f"Uniform polylog decoders: {metrics['uniform_polylog_classical_decoder_count']}")
    print(f"Natural reductions: {metrics['natural_problem_reduction_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for row in payload["preprocessing_records"]:
            print(
                f"- {row['family_id']} n={row['n_bits']} p={row['prime']} | {row['status']} | "
                f"prefix={row['first_globally_unique_prefix']} | prefix/n={row['prefix_over_n_bits']} | "
                f"preprocess={row['preprocessing_operations']} | online={row['online_lookup_operations']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_family_triage(args: argparse.Namespace) -> int:
    payload = write_phase_family_triage(write_registry=not args.no_registry)
    validation = validate_registry()
    print("Phase-family triage complete")
    print("Artifact: research/phase_workbench/phase_family_triage.json")
    print(f"Families: {payload['family_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in payload["records"]:
            print(
                f"- {record['family_id']} | {record['status']} | "
                f"blocker={record['primary_blocker']} | action={record['next_action']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_phase_naturalness(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_phase_family_naturalness_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Phase-family naturalness audit complete")
    print("Artifact: research/phase_workbench/phase_family_naturalness.json")
    print(f"Records: {payload['record_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"artificial={summary['artificial_record_count']} natural={summary['natural_record_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_trace_functions(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_trace_function_search_report(
        families=families,
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Trace-function hidden-shift search complete")
    print("Artifact: research/phase_workbench/trace_function_search.json")
    print(f"Records: {payload['record_count']}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for summary in payload["family_summaries"]:
            print(
                f"- {summary['family_id']} | {summary['best_status']} | "
                f"algebraic={summary.get('algebraic_decoder_count', 0)} "
                f"sample={summary['sample_dequantized_count']} sparse={summary['sparse_spectrum_count']} "
                f"low_degree={summary['low_degree_count']} unresolved={summary['unresolved_count']}"
            )
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_run(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    if args.list_supported:
        print("Supported experiment IDs")
        print("========================")
        for experiment_id in supported_experiment_ids():
            print(experiment_id)
        return 0
    if args.all_supported:
        results = run_supported_experiments()
    else:
        if not args.experiment_id:
            raise SystemExit("run requires EXPERIMENT_ID unless --all-supported is set")
        results = [run_experiment(args.experiment_id)]
    validation = validate_registry()
    print("Experiment runner complete")
    for result in results:
        print(f"{result.experiment_id} -> {result.result_id} [{result.status}]")
        if args.verbose:
            print(f"  {result.summary}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_run_next(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    if args.dry_run:
        selection = select_next_experiment()
        print("Next experiment selection")
        print("=========================")
        print(f"Experiment: {selection.experiment_id}")
        print(f"Score: {selection.score}")
        print(f"Supported: {selection.supported}")
        print(f"Reason: {selection.reason}")
        return 0
    selection, result = run_next_experiment()
    validation = validate_registry()
    print("Next experiment run complete")
    print(f"Selected: {selection.experiment_id} (score={selection.score})")
    print(f"Reason: {selection.reason}")
    print(f"Result: {result.result_id} [{result.status}]")
    print("Run history: research/experiment_run_history.json")
    print("Trends: research/experiment_trends.json")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_trends(args: argparse.Namespace) -> int:
    report = write_experiment_trends()
    print("Experiment trends complete")
    print("Artifact: research/experiment_trends.json")
    print(f"History records: {report['history_count']}")
    print(f"Trend records: {report['trend_count']}")
    if args.verbose:
        for trend in report["trends"]:
            print(
                f"- {trend['experiment_id']} runs={trend['run_count']} "
                f"latest={trend['latest_status']} blockers={trend['blocking_run_count']}"
            )
    return 0


def command_proofs(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    report = write_proof_status_report()
    validation = validate_registry()
    print("Proof status report complete")
    print("Report: research/proof_status_report.json")
    print("Proof debt: research/proof_debt_report.json")
    print("Registry: research/registry/proof_status.json")
    print(f"Proof statuses: {report['proof_status_count']}")
    print(f"Blocking statuses: {report['blocking_status_count']}")
    print(f"Needs evidence: {report['needs_evidence_count']}")
    print(
        "Proof debt: "
        f"{report.get('proof_debt_count', 0)} debts, "
        f"{report.get('lemma_count', 0)} lemmas, "
        f"{report.get('reduction_edge_count', 0)} reduction edges, "
        f"{report.get('counterexample_search_count', 0)} counterexample searches"
    )
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for record in report["records"]:
            if record["status"] != "text-present":
                print(f"- {record['candidate_id']} {record['obligation_id']} {record['status']}: {record['evidence']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_reductions(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    report = write_reduction_ledger()
    contract_audit = write_reduction_contract_audit()
    validation = validate_registry()
    print("Certificate-gated reduction ledger complete")
    print("Artifact: research/reductions/reduction_ledger.json")
    print("Registry: research/registry/reductions.json")
    print(f"Edges: {report['edge_count']} ({report['accepted_edge_count']} accepted, {report['blocked_edge_count']} blocked)")
    print(f"Routes: {report['route_count']} ({report['complete_route_count']} complete, {report['blocked_route_count']} blocked)")
    print(f"Blocked candidates: {report['blocked_candidate_count']}")
    print(
        f"Exact interface audits: {contract_audit['route_audit_count']} "
        f"({contract_audit['blocked_interface_count']} blocked)"
    )
    print(f"Status: {report['status']}")
    print(f"Summary: {report['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for route in report["routes"]:
            print(
                f"- {route['candidate_id']} | {route['id']} | {route['status']} | "
                f"blocking={len(route['blocking_edge_ids'])}"
            )
        for edge in report["edges"]:
            if edge["accepted"]:
                continue
            certificate = edge["certificate"]
            print(f"  {certificate['id']} | issues={len(edge['issues'])}")
            for issue in edge["issues"][: args.max_verbose_issues]:
                print(f"    {issue['field']}: {issue['message']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_reduction_contracts(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    catalog = write_theorem_catalog()
    report = write_reduction_contract_audit()
    print("Exact reduction theorem-contract audit complete")
    print("Catalog: research/reductions/theorem_contracts.json")
    print("Audit: research/reductions/interface_audit.json")
    print(f"Theorem contracts: {catalog['contract_count']}")
    print(f"Route interfaces: {report['route_audit_count']}")
    print(f"Blocked interfaces: {report['blocked_interface_count']}")
    print(f"Access mismatches: {report['access_mismatch_count']}")
    print(f"Family-coverage mismatches: {report['family_coverage_mismatch_count']}")
    print(f"Status: {report['status']}")
    print(f"Summary: {report['summary']}")
    if args.verbose:
        for audit in report["audits"]:
            failed = [check for check in audit["checks"] if not check["passed"]]
            print(
                f"- {audit['candidate_id']} | {audit['route_id']} | {audit['status']} | "
                f"failed={len(failed)} debt={audit['proof_debt_score']}"
            )
            for check in failed[: args.max_verbose_checks]:
                print(f"  {check['axis']}: {check['burden']}")
    return 0


def command_proof_queue(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    write_proof_status_report()
    report = write_proof_work_queue(max_items=args.max_items)
    print("Proof work queue complete")
    print("Artifact: research/proof_work_queue.json")
    print(f"Items: {report['work_item_count']}")
    print(f"Action clusters: {report['action_cluster_count']}")
    print(f"Ready to run: {report['ready_to_run_count']}")
    print(f"Theory/mixed: {report['theory_or_mixed_count']}")
    print(f"Status: {report['status']}")
    top = report.get("top_action_cluster") or report.get("top_work_item")
    if top:
        top_id = top.get("id", "cluster")
        print(f"Top: {top_id} | {top['work_type']} | score={top['priority_score']}")
        print(f"Command: {top['recommended_command']}")
    if args.verbose:
        for cluster in report["action_clusters"]:
            print(
                f"* cluster {cluster['work_type']} | score={cluster['priority_score']} | "
                f"candidates={cluster['affected_candidate_count']}"
            )
            print(f"  command: {cluster['recommended_command']}")
        for item in report["items"]:
            print(f"- {item['id']} | {item['work_type']} | score={item['priority_score']} | {item['status']}")
            print(f"  action: {item['recommended_action']}")
            print(f"  command: {item['recommended_command']}")
    return 0


def command_sweep(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    families = [item.strip() for item in args.families.split(",") if item.strip()]
    payload = write_hidden_shift_sweep(
        n_values=parse_int_csv(args.n_values),
        sample_counts=parse_int_csv(args.sample_counts),
        families=families,
        shift=args.shift,
        seed=args.seed,
        write_registry=not args.no_registry,
    )
    validation = validate_registry()
    print("Scaling sweep complete")
    print("Artifact: research/scaling/hidden_shift_sweep.json")
    print(f"Rows: {len(payload['rows'])}")
    print(f"Status: {payload['status']}")
    print(f"Summary: {payload['summary']}")
    print(f"Registry valid: {validation['valid']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_conjectures(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    report = write_conjecture_report()
    validation = validate_registry()
    print("Conjecture report complete")
    print("Report: research/conjecture_report.json")
    print("Registry: research/registry/conjectures.json")
    print(f"Conjectures: {report['conjecture_count']}")
    print(f"Blocked: {report['blocked_count']}")
    print(f"Needs evidence: {report['needs_evidence_count']}")
    print(f"Active: {report['active_count']}")
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for conjecture in report["conjectures"]:
            print(f"- {conjecture['id']} | {conjecture['status']} | blockers={len(conjecture['blocking_evidence'])}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_mutate(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    report = write_mutation_report()
    validation = validate_registry()
    print("Mutation report complete")
    print("Report: research/mutation_report.json")
    print("Registry: research/registry/mutation_proposals.json")
    print(f"Proposals: {report['proposal_count']}")
    print(f"Reduction-interface repairs: {report.get('interface_repair_proposal_count', 0)}")
    print(f"Proposal-only (not proof-gate eligible): {report.get('proposal_only_count', 0)}")
    print(
        "Proof-gate preflights: "
        f"{report.get('accepted_preflight_count', 0)} accepted, "
        f"{report.get('rejected_preflight_count', 0)} rejected, "
        f"{report.get('not_generated_preflight_count', 0)} proposal-only"
    )
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for proposal in report["proposals"]:
            print(f"- {proposal['id']} | {proposal['mutation_type']} | {proposal['rationale']}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_quarantine_invalid(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    report = quarantine_exact_access_invalid_mutations()
    write_reduction_ledger()
    write_reduction_contract_audit()
    validation = validate_registry()
    print("Exact-interface quarantine complete")
    print("Report: research/quarantine_report.json")
    print(f"Quarantined candidates: {report['quarantined_candidate_count']}")
    print(f"Removed experiments: {report['removed_experiment_count']}")
    print(f"Status: {report['status']}")
    print(f"Registry valid: {validation['valid']}")
    if args.verbose:
        for candidate_id in report["quarantined_candidate_ids"]:
            print(f"- {candidate_id}")
    if validation["issues"]:
        print(json.dumps(validation["issues"], indent=2))
        return 1
    return 0


def command_blockers(args: argparse.Namespace) -> int:
    report = write_blocker_taxonomy()
    print("Blocker taxonomy complete")
    print("Artifact: research/blocker_taxonomy.json")
    print(f"Evidence rows: {report['evidence_count']}")
    print(f"Blocker classes: {report['blocker_class_count']}")
    print(f"Top blocker: {report['top_blocker_class']}")
    print(f"Top actionable blocker: {report['top_actionable_blocker_class']}")
    print(f"Status: {report['status']}")
    if args.verbose:
        for item in report["classes"]:
            print(
                f"- {item['blocker_class']} score={item['priority_score']} "
                f"evidence={item['evidence_count']} action={item['required_action']}"
            )
    return 0


def command_frontiers(args: argparse.Namespace) -> int:
    report = write_frontier_map()
    print("Research frontier map complete")
    print("Artifact: research/frontier_map.json")
    print(f"Frontiers: {report['frontier_count']}")
    print(f"Top frontier: {report['top_frontier']}")
    print(f"Status: {report['status']}")
    if args.verbose:
        for frontier in report["frontiers"]:
            print(
                f"- {frontier['frontier_id']} score={frontier['priority_score']} "
                f"status={frontier['status']} next={frontier['next_experiment']}"
            )
    return 0


def command_query_models(args: argparse.Namespace) -> int:
    report = write_query_model_ledger()
    print("Query-model ledger complete")
    print("Artifact: research/query_model_ledger.json")
    print(f"Candidates: {report['candidate_count']}")
    print(f"Blocking records: {report['blocking_record_count']}")
    print(f"Status: {report['status']}")
    if args.verbose:
        for record in report["records"]:
            print(
                f"- {record['candidate_id']} | {record['candidate_kind']} | {record['status']} | "
                f"attacks={len(record['attacks_that_must_be_excluded'])} obligations={len(record['lower_bound_obligations'])}"
            )
    return 0


def command_ingest_papers(args: argparse.Namespace) -> int:
    records = (
        write_paper_ingestion_with_arxiv(args.paths, args.arxiv_id)
        if args.arxiv_id
        else write_paper_ingestion(args.paths)
    )
    print("Paper ingestion complete")
    print("Artifact: research/paper_ingestion.json")
    print("No-go index: research/literature_no_go_index.json")
    print(f"Records: {len(records)}")
    if args.verbose:
        for record in records:
            print(f"- {record['id']} | {record['mechanism']} | {record['problem_family']}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    validation = validate_registry()
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["valid"] else 1


def command_list(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    if args.kind in {"all", "candidates"}:
        print("Candidates")
        print("==========")
        for candidate in load_candidates():
            print(f"{candidate['id']} | {candidate['status']} | {candidate['title']}")
            if args.verbose:
                print(f"  mechanism: {candidate['quantum_mechanism']}")
                print(f"  literature: {', '.join(candidate['literature_ids'])}")
    if args.kind in {"all", "experiments"}:
        print("\nExperiments")
        print("===========")
        for experiment in load_experiments():
            print(f"{experiment['id']} | {experiment['candidate_id']} | {experiment['status']} | {experiment['title']}")
            if args.verbose:
                print(f"  falsifiers: {'; '.join(experiment['falsifiers'])}")
    if args.kind in {"all", "results"}:
        print("\nExperiment Results")
        print("==================")
        for result in load_experiment_results()[: args.limit]:
            print(f"{result['id']} | {result['experiment_id']} | {result['status']} | {result['summary']}")
            if args.verbose:
                print(f"  metrics: {json.dumps(result.get('metrics', {}), sort_keys=True)}")
                print(f"  falsifiers: {'; '.join(result.get('falsifiers_triggered', []))}")
    if args.kind in {"all", "dequantization"}:
        print("\nDequantization Checks")
        print("=====================")
        for finding in load_dequantization_checks()[: args.limit]:
            print(f"{finding['id']} | {finding['severity']} | {finding['target_id']} | {finding['claim_under_test']}")
            if args.verbose:
                print(f"  evidence: {finding['evidence']}")
                print(f"  action: {finding['required_action']}")
    if args.kind in {"all", "proofs"}:
        print("\nProof Status")
        print("============")
        for record in load_proof_status()[: args.limit]:
            print(f"{record['candidate_id']} | {record['obligation_id']} | {record['status']}")
            if args.verbose:
                print(f"  evidence: {record['evidence']}")
                print(f"  next: {record['next_action']}")
    if args.kind in {"all", "reductions"}:
        print("\nReduction Routes")
        print("================")
        ledger = load_reduction_ledger()
        for route in ledger.get("routes", [])[: args.limit]:
            print(f"{route['id']} | {route['candidate_id']} | {route['status']}")
            if args.verbose:
                print(f"  source: {route['natural_source_problem']}")
                print(f"  target: {route['candidate_target']}")
                print(f"  blocking edges: {', '.join(route['blocking_edge_ids'])}")
    if args.kind in {"all", "reduction-contracts"}:
        print("\nReduction Contract Interfaces")
        print("=============================")
        contract_audit = json.loads(CONTRACT_AUDIT_PATH.read_text()) if CONTRACT_AUDIT_PATH.exists() else {}
        for audit in contract_audit.get("audits", [])[: args.limit]:
            print(f"{audit['route_id']} | {audit['candidate_id']} | {audit['status']}")
            if args.verbose:
                failed = [check for check in audit.get("checks", []) if not check.get("passed")]
                print(f"  theorem: {audit.get('theorem_contract_id', '')}")
                print(f"  failed axes: {', '.join(check['axis'] for check in failed)}")
    if args.kind in {"all", "scaling"}:
        print("\nScaling Runs")
        print("============")
        for run in load_scaling_runs()[: args.limit]:
            print(f"{run['id']} | {run['status']} | {run['summary']}")
            if args.verbose:
                print(f"  metrics: {json.dumps(run.get('headline_metrics', {}), sort_keys=True)}")
    if args.kind in {"all", "conjectures"}:
        print("\nConjectures")
        print("===========")
        for conjecture in load_conjectures()[: args.limit]:
            print(f"{conjecture['id']} | {conjecture['status']} | {conjecture['statement']}")
            if args.verbose:
                print(f"  reductions: {'; '.join(conjecture.get('reduction_links', []))}")
                print(f"  blockers: {len(conjecture.get('blocking_evidence', []))}")
    if args.kind in {"all", "mutations"}:
        print("\nMutation Proposals")
        print("==================")
        for proposal in load_mutation_proposals()[: args.limit]:
            print(f"{proposal['id']} | {proposal['mutation_type']} | {proposal['status']}")
            if args.verbose:
                print(f"  rationale: {proposal['rationale']}")
                print(f"  required: {'; '.join(proposal.get('required_modules', []))}")
    if args.kind in {"all", "negative"}:
        print("\nNegative Results")
        print("================")
        for item in load_negative_results()[: args.limit]:
            print(f"{item['id']} | {item['claim']}")
            if args.verbose:
                print(f"  invalid: {item['reason_invalid']}")
                print(f"  lesson: {item['lesson']}")
    if args.kind in {"all", "rejected"}:
        print("\nRejected Candidates")
        print("===================")
        for item in load_rejected_candidates()[: args.limit]:
            print(f"{item['id']} | {item['title']} | issues={len(item.get('issues', []))}")
            if args.verbose:
                for issue in item.get("issues", []):
                    print(f"  {issue['obligation_id']}:{issue['field']}: {issue['message']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Regenerate research artifacts and validate the registry.")
    audit.add_argument("--output-dir", type=Path, default=Path("research"))
    audit.add_argument("--refresh-arxiv", action="store_true")
    audit.add_argument("--overwrite-registry", action="store_true")
    audit.set_defaults(func=command_audit)

    literature = subparsers.add_parser("literature", help="Extract structured mechanism records from seed and optional arXiv literature.")
    literature.add_argument("--output-dir", type=Path, default=Path("research"))
    literature.add_argument("--refresh-arxiv", action="store_true")
    literature.add_argument("--max-arxiv-results", type=int, default=20)
    literature.add_argument("--verbose", action="store_true")
    literature.set_defaults(func=command_literature)

    hypothesize = subparsers.add_parser("hypothesize", help="Generate proof-gated hypotheses from literature and ontology records.")
    hypothesize.add_argument("--refresh-arxiv", action="store_true")
    hypothesize.add_argument("--max-arxiv-results", type=int, default=20)
    hypothesize.set_defaults(func=command_hypothesize)

    hidden_shift = subparsers.add_parser("hidden-shift", help="Run hidden-shift/DHSP phase-family audits and sieve baselines.")
    hidden_shift.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,kloosterman_trace,legendre_symbol,quartic_character,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2,noisy_cubic_chirp",
    )
    hidden_shift.add_argument("--min-bits", type=int, default=5)
    hidden_shift.add_argument("--max-bits", type=int, default=8)
    hidden_shift.add_argument("--shift", type=int, default=7)
    hidden_shift.add_argument("--sieve-samples", type=int, default=2048)
    hidden_shift.add_argument("--sample-count", type=int)
    hidden_shift.add_argument("--seed", type=int, default=0)
    hidden_shift.add_argument("--no-registry", action="store_true")
    hidden_shift.set_defaults(func=command_hidden_shift)

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

    dcp_bad = subparsers.add_parser(
        "dcp-bad-registers",
        help="Audit arbitrary bad-register contamination under the exact Regev f=1 DCP promise.",
    )
    dcp_bad.add_argument("--n-values", default="12,16,20,24")
    dcp_bad.add_argument("--trials-per-row", type=int, default=32)
    dcp_bad.add_argument("--seed", type=int, default=0)
    dcp_bad.add_argument("--no-registry", action="store_true")
    dcp_bad.set_defaults(func=command_dcp_bad_registers)

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

    dcp_clifford = subparsers.add_parser(
        "dcp-clifford-witnesses",
        help="Search global public-label Clifford measurements with efficient Hamming-weight decoders.",
    )
    dcp_clifford.add_argument("--n-values", default="8,10,12,14,16")
    dcp_clifford.add_argument("--trials-per-row", type=int, default=4)
    dcp_clifford.add_argument("--seed", type=int, default=0)
    dcp_clifford.add_argument("--no-registry", action="store_true")
    dcp_clifford.set_defaults(func=command_dcp_clifford_witnesses)

    dcp_clifford_contamination = subparsers.add_parser(
        "dcp-clifford-contamination",
        help="Minimize global Clifford Hamming signal over every one-bad coordinate and basis value.",
    )
    dcp_clifford_contamination.add_argument("--n-values", default="6,8,10,12")
    dcp_clifford_contamination.add_argument("--trials-per-row", type=int, default=3)
    dcp_clifford_contamination.add_argument("--seed", type=int, default=0)
    dcp_clifford_contamination.add_argument("--no-registry", action="store_true")
    dcp_clifford_contamination.set_defaults(func=command_dcp_clifford_contamination)

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

    dcp_frontier = subparsers.add_parser(
        "dcp-decoder-frontier",
        help="Compare legal DCP decoders against named sample/time/memory and robustness frontiers.",
    )
    dcp_frontier.add_argument("--no-registry", action="store_true")
    dcp_frontier.set_defaults(func=command_dcp_decoder_frontier)

    dcp_aliasing = subparsers.add_parser(
        "dcp-multiscale-aliasing",
        help="Certify random-label sample barriers for raw and pairwise high-valuation aliases.",
    )
    dcp_aliasing.add_argument("--n-values", default="32,64,128,256,512,1024")
    dcp_aliasing.add_argument("--effective-bit-multipliers", default="1,2")
    dcp_aliasing.add_argument("--polynomial-sample-power", type=int, default=3)
    dcp_aliasing.add_argument("--no-registry", action="store_true")
    dcp_aliasing.set_defaults(func=command_dcp_multiscale_aliasing)

    dcp_fourier_bridge = subparsers.add_parser(
        "dcp-fourier-bridge",
        help="Formalize DCP random-label Fourier/HNP bridges, access mismatches, and sample-vs-time bounds.",
    )
    dcp_fourier_bridge.add_argument("--n-values", default="32,64,128,256,512,1024")
    dcp_fourier_bridge.add_argument("--target-failure-probability", type=float, default=1.0 / 3.0)
    dcp_fourier_bridge.add_argument("--no-registry", action="store_true")
    dcp_fourier_bridge.set_defaults(func=command_dcp_fourier_bridge)

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

    dcp_factorized = subparsers.add_parser(
        "dcp-factorized-contraction",
        help="Audit polynomial elementary-symmetric contraction of rank-one DCP product kernels.",
    )
    dcp_factorized.add_argument("--n-values", default="32,64,128,256,512")
    dcp_factorized.add_argument("--degrees", default="2,3,4,8,16,32")
    dcp_factorized.add_argument("--sample-budget-power", type=int, default=3)
    dcp_factorized.add_argument("--no-registry", action="store_true")
    dcp_factorized.set_defaults(func=command_dcp_factorized_contraction)

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

    dcp_subset_sum_resource = subparsers.add_parser(
        "dcp-subset-sum-resource-frontier",
        help="Audit source-linked meet-in-middle, dissection, Wagner, representation, and quantum resource exponents.",
    )
    dcp_subset_sum_resource.add_argument("--n-values", default="64,128,256,512")
    dcp_subset_sum_resource.add_argument("--register-offsets", default="0,4,8")
    dcp_subset_sum_resource.add_argument("--list-counts", default="2,4,8,16")
    dcp_subset_sum_resource.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_resource.set_defaults(func=command_dcp_subset_sum_resource_frontier)

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

    dcp_subset_sum_synthesize = subparsers.add_parser(
        "dcp-subset-sum-synthesize",
        help="Generate typed high-variance partial-solver hypotheses and reject negative-result matches.",
    )
    dcp_subset_sum_synthesize.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_synthesize.set_defaults(func=command_dcp_subset_sum_synthesize)

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

    dcp_subset_sum_smith_transfer = subparsers.add_parser(
        "dcp-subset-sum-smith-transfer",
        help="Prove the fixed-sixth source moment obstruction by exhaustive HNF transfer.",
    )
    dcp_subset_sum_smith_transfer.add_argument("--n-values", default="6,8,10,12,16,20")
    dcp_subset_sum_smith_transfer.add_argument("--register-offsets", default="0,2")
    dcp_subset_sum_smith_transfer.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_smith_transfer.set_defaults(func=command_dcp_subset_sum_smith_transfer)

    dcp_subset_sum_fixed_moments = subparsers.add_parser(
        "dcp-subset-sum-fixed-moments",
        help="Prove source-average contraction for every fixed subset-sum factorial-moment order.",
    )
    dcp_subset_sum_fixed_moments.add_argument(
        "--moment-orders", default=",".join(str(value) for value in range(2, 13))
    )
    dcp_subset_sum_fixed_moments.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_fixed_moments.set_defaults(func=command_dcp_subset_sum_fixed_moments)

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

    dcp_subset_sum_short_relations = subparsers.add_parser(
        "dcp-subset-sum-short-relations",
        help="Prove exponentially many short marker-zero competitors in the standard embedding.",
    )
    dcp_subset_sum_short_relations.add_argument("--n-values", default="32,64,128,256,512")
    dcp_subset_sum_short_relations.add_argument("--register-offset", type=int, default=2)
    dcp_subset_sum_short_relations.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_short_relations.set_defaults(func=command_dcp_subset_sum_short_relations)

    dcp_subset_sum_carry_relations = subparsers.add_parser(
        "dcp-subset-sum-carry-relations",
        help="Prove inverse-polynomial source coverage of short carry-sliced competitors.",
    )
    dcp_subset_sum_carry_relations.add_argument("--n-values", default="32,64,128,256,512")
    dcp_subset_sum_carry_relations.add_argument("--register-offset", type=int, default=2)
    dcp_subset_sum_carry_relations.add_argument("--log-multiplier", type=int, default=1)
    dcp_subset_sum_carry_relations.add_argument("--no-registry", action="store_true")
    dcp_subset_sum_carry_relations.set_defaults(func=command_dcp_subset_sum_carry_relations)

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

    dcp_coherent_matching = subparsers.add_parser(
        "dcp-coherent-matching",
        help="Prove shared-seed randomized matching compatibility and audit quantum workspace coherence.",
    )
    dcp_coherent_matching.add_argument("--n-values", default="16,32,64,128")
    dcp_coherent_matching.add_argument("--coverage-exponents", default="1,2,3")
    dcp_coherent_matching.add_argument("--register-offset", type=int, default=4)
    dcp_coherent_matching.add_argument("--no-registry", action="store_true")
    dcp_coherent_matching.set_defaults(func=command_dcp_coherent_matching)

    dcp_quantum_relation_fidelity = subparsers.add_parser(
        "dcp-quantum-relation-fidelity",
        help="Audit paired witness/history fidelity for concrete quantum relation solver interfaces.",
    )
    dcp_quantum_relation_fidelity.add_argument("--no-registry", action="store_true")
    dcp_quantum_relation_fidelity.set_defaults(func=command_dcp_quantum_relation_fidelity)

    dcp_quantum_walk_source_audit = subparsers.add_parser(
        "dcp-quantum-walk-source-audit",
        help="Audit the 0.2182 subset-sum quantum walk directly against cached primary-source LaTeX.",
    )
    dcp_quantum_walk_source_audit.add_argument("--no-registry", action="store_true")
    dcp_quantum_walk_source_audit.set_defaults(func=command_dcp_quantum_walk_source_audit)

    dcp_symmetric_relation_lift = subparsers.add_parser(
        "dcp-symmetric-relation-lift",
        help="Prove the symmetric double-evaluation interface for purified quantum relation solvers.",
    )
    dcp_symmetric_relation_lift.add_argument("--no-registry", action="store_true")
    dcp_symmetric_relation_lift.set_defaults(func=command_dcp_symmetric_relation_lift)

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

    dcp_affine_transport = subparsers.add_parser(
        "dcp-affine-transport",
        help="Audit exact GF(2)-affine transport congruences and witness extraction.",
    )
    dcp_affine_transport.add_argument("--n-values", default="32,64,128,256")
    dcp_affine_transport.add_argument("--register-offset", type=int, default=4)
    dcp_affine_transport.add_argument("--no-registry", action="store_true")
    dcp_affine_transport.set_defaults(func=command_dcp_affine_transport)

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

    coset_state = subparsers.add_parser("coset-state", help="Run coset-state/nonabelian HSP graph-pair audits.")
    coset_state.add_argument("--pairs", default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cycle-vs-chorded-cycle")
    coset_state.add_argument("--no-registry", action="store_true")
    coset_state.set_defaults(func=command_coset_state)

    collective_observables = subparsers.add_parser(
        "collective-observables",
        help="Run adversarial collective-observable search on coset/nonabelian graph-pair frontiers.",
    )
    collective_observables.add_argument("--pairs", default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cycle-vs-chorded-cycle")
    collective_observables.add_argument("--tuple-cap", type=int, default=120_000)
    collective_observables.add_argument("--no-registry", action="store_true")
    collective_observables.add_argument("--verbose", action="store_true")
    collective_observables.set_defaults(func=command_collective_observables)

    code_family_search = subparsers.add_parser(
        "code-family-search",
        help="Generate weak-invariant code-equivalence collisions and attack them with stronger classical invariants.",
    )
    code_family_search.add_argument("--no-registry", action="store_true")
    code_family_search.add_argument("--verbose", action="store_true")
    code_family_search.set_defaults(func=command_code_family_search)

    tensor_observables = subparsers.add_parser(
        "tensor-observables",
        help="Audit graphlet/homomorphism tensor observables against classical small-pattern-count shadows.",
    )
    tensor_observables.add_argument("--pairs", default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cfi-k6-parity-twist,cycle-vs-chorded-cycle")
    tensor_observables.add_argument("--tuple-cap", type=int, default=1_000_000)
    tensor_observables.add_argument("--no-registry", action="store_true")
    tensor_observables.add_argument("--verbose", action="store_true")
    tensor_observables.set_defaults(func=command_tensor_observables)

    gm_switching = subparsers.add_parser(
        "gm-switching",
        aliases=["godsil-mckay"],
        help="Search Godsil-McKay switched cospectral graph rows and attack them with classical baselines.",
    )
    gm_switching.add_argument("--no-registry", action="store_true")
    gm_switching.add_argument("--verbose", action="store_true")
    gm_switching.set_defaults(func=command_gm_switching)

    cfi_scaling = subparsers.add_parser(
        "cfi-scaling",
        help="Probe CFI parity scaling boundaries for coset-state collective-measurement experiments.",
    )
    cfi_scaling.add_argument("--base-sizes", default="4,5,6,7")
    cfi_scaling.add_argument("--wl2-pair-cap", type=int, default=10_000)
    cfi_scaling.add_argument("--wl-tuple-cap", type=int, default=100_000)
    cfi_scaling.add_argument("--graphlet-tuple-cap", type=int, default=1_000_000)
    cfi_scaling.add_argument("--no-registry", action="store_true")
    cfi_scaling.add_argument("--verbose", action="store_true")
    cfi_scaling.set_defaults(func=command_cfi_scaling)

    cfi_base_search = subparsers.add_parser(
        "cfi-base-search",
        help="Search non-complete CFI base families and attack them with individualized-WL baselines.",
    )
    cfi_base_search.add_argument("--base-ids", default="complete-k5,triangular-prism,cube-q3,mobius-ladder-8,petersen,heawood-like-14")
    cfi_base_search.add_argument("--max-individualization", type=int, default=3)
    cfi_base_search.add_argument("--tuple-cap", type=int, default=40_000)
    cfi_base_search.add_argument("--exact-vertex-cap", type=int, default=50)
    cfi_base_search.add_argument("--no-registry", action="store_true")
    cfi_base_search.add_argument("--verbose", action="store_true")
    cfi_base_search.set_defaults(func=command_cfi_base_search)

    cfi_parity_solver = subparsers.add_parser(
        "cfi-parity-solver",
        help="Run the promised complete-CFI gadget parity decoder as a structural dequantization baseline.",
    )
    cfi_parity_solver.add_argument("--base-sizes", default="4,5,6,7,8")
    cfi_parity_solver.add_argument("--seed", type=int, default=2718)
    cfi_parity_solver.add_argument("--no-shuffle", action="store_true")
    cfi_parity_solver.add_argument("--no-registry", action="store_true")
    cfi_parity_solver.add_argument("--verbose", action="store_true")
    cfi_parity_solver.set_defaults(func=command_cfi_parity_solver)

    cfi_structural_decoder = subparsers.add_parser(
        "cfi-structural-decoder",
        help="Run the promised regular-CFI gadget parity decoder across non-complete base families.",
    )
    cfi_structural_decoder.add_argument("--base-ids", default="complete-k5,triangular-prism,cube-q3,mobius-ladder-8,petersen,heawood-like-14")
    cfi_structural_decoder.add_argument("--seed", type=int, default=9041)
    cfi_structural_decoder.add_argument("--no-shuffle", action="store_true")
    cfi_structural_decoder.add_argument("--no-registry", action="store_true")
    cfi_structural_decoder.add_argument("--verbose", action="store_true")
    cfi_structural_decoder.set_defaults(func=command_cfi_structural_decoder)

    cfi_irregular_decoder = subparsers.add_parser(
        "cfi-irregular-decoder",
        help="Run the degree-separated irregular-CFI structural parity decoder.",
    )
    cfi_irregular_decoder.add_argument("--base-ids", default="complete-bipartite-3-5,complete-bipartite-4-5,complete-tripartite-2-3-4")
    cfi_irregular_decoder.add_argument("--seed", type=int, default=13001)
    cfi_irregular_decoder.add_argument("--no-shuffle", action="store_true")
    cfi_irregular_decoder.add_argument("--no-registry", action="store_true")
    cfi_irregular_decoder.add_argument("--verbose", action="store_true")
    cfi_irregular_decoder.set_defaults(func=command_cfi_irregular_decoder)

    cfi_bipartite_decoder = subparsers.add_parser(
        "cfi-bipartite-decoder",
        help="Run the bipartition-based CFI structural decoder, including non-degree-separated stress rows.",
    )
    cfi_bipartite_decoder.add_argument("--base-ids", default="complete-k4,mobius-ladder-8,complete-bipartite-3-5,prism-degree4-hub")
    cfi_bipartite_decoder.add_argument("--seed", type=int, default=17011)
    cfi_bipartite_decoder.add_argument("--no-shuffle", action="store_true")
    cfi_bipartite_decoder.add_argument("--no-registry", action="store_true")
    cfi_bipartite_decoder.add_argument("--verbose", action="store_true")
    cfi_bipartite_decoder.set_defaults(func=command_cfi_bipartite_decoder)

    individualized_wl = subparsers.add_parser(
        "individualized-wl",
        help="Run individualization-refinement WL baselines for graph/coset rows.",
    )
    individualized_wl.add_argument("--pairs", default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cycle-vs-chorded-cycle")
    individualized_wl.add_argument("--max-individualization", type=int, default=3)
    individualized_wl.add_argument("--tuple-cap", type=int, default=40_000)
    individualized_wl.add_argument("--no-registry", action="store_true")
    individualized_wl.add_argument("--verbose", action="store_true")
    individualized_wl.set_defaults(func=command_individualized_wl)

    individualized_tensors = subparsers.add_parser(
        "individualized-tensors",
        help="Run individualized rooted tensor/graphlet baselines for graph/coset rows.",
    )
    individualized_tensors.add_argument(
        "--pairs",
        default="shrikhande-vs-rook,cfi-k4-parity-twist,cfi-k5-parity-twist,cfi-k6-parity-twist,cycle-vs-chorded-cycle",
    )
    individualized_tensors.add_argument("--max-root-size", type=int, default=2)
    individualized_tensors.add_argument("--tuple-cap", type=int, default=3_000_000)
    individualized_tensors.add_argument("--no-registry", action="store_true")
    individualized_tensors.add_argument("--verbose", action="store_true")
    individualized_tensors.set_defaults(func=command_individualized_tensors)

    coset_triage = subparsers.add_parser(
        "coset-triage",
        help="Aggregate coset frontier rows across WL, tensor, individualization, and CFI structural baselines.",
    )
    coset_triage.add_argument("--no-registry", action="store_true")
    coset_triage.add_argument("--verbose", action="store_true")
    coset_triage.set_defaults(func=command_coset_triage)

    representation_obstructions = subparsers.add_parser(
        "representation-obstructions",
        help="Audit symmetric-group irrep growth and strong-Fourier no-go pressure.",
    )
    representation_obstructions.add_argument("--n-values", default="4,5,6,8,10,12,14,16")
    representation_obstructions.add_argument("--no-registry", action="store_true")
    representation_obstructions.add_argument("--verbose", action="store_true")
    representation_obstructions.set_defaults(func=command_representation_obstructions)

    weak_fourier = subparsers.add_parser(
        "weak-fourier",
        help="Audit weak Fourier irrep-label signal for symmetric-group involution hidden subgroups.",
    )
    weak_fourier.add_argument("--n-values", default="6,8,10,12,14,16")
    weak_fourier.add_argument("--no-registry", action="store_true")
    weak_fourier.add_argument("--verbose", action="store_true")
    weak_fourier.set_defaults(func=command_weak_fourier)

    coset_distinguishability = subparsers.add_parser(
        "coset-distinguishability",
        help="Audit multi-copy distinguishability obligations for symmetric-group involution coset states.",
    )
    coset_distinguishability.add_argument("--n-values", default="6,8,10,12,14,16")
    coset_distinguishability.add_argument("--no-registry", action="store_true")
    coset_distinguishability.add_argument("--verbose", action="store_true")
    coset_distinguishability.set_defaults(func=command_coset_distinguishability)

    coset_pgm = subparsers.add_parser(
        "coset-pgm",
        help="Audit PGM copy/capacity obligations for symmetric-group involution coset states.",
    )
    coset_pgm.add_argument("--n-values", default="6,8,10,12,14,16")
    coset_pgm.add_argument("--epsilon", type=float, default=0.1)
    coset_pgm.add_argument("--no-registry", action="store_true")
    coset_pgm.add_argument("--verbose", action="store_true")
    coset_pgm.set_defaults(func=command_coset_pgm)

    coset_holevo = subparsers.add_parser(
        "coset-holevo",
        help="Compute exact one-copy Holevo information and rigorous multi-copy decoding lower bounds.",
    )
    coset_holevo.add_argument("--n-values", default="6,8,10,12,14,16,20")
    coset_holevo.add_argument("--error", type=float, default=1 / 3)
    coset_holevo.add_argument("--no-registry", action="store_true")
    coset_holevo.add_argument("--verbose", action="store_true")
    coset_holevo.set_defaults(func=command_coset_holevo)

    coset_covariant_frame = subparsers.add_parser(
        "coset-covariant-frame",
        help="Diagonalize one-copy involution class frames and isolate multi-copy decoder debt.",
    )
    coset_covariant_frame.add_argument("--n-values", default="6,8,10,12,14,16")
    coset_covariant_frame.add_argument("--no-registry", action="store_true")
    coset_covariant_frame.set_defaults(func=command_coset_covariant_frame)

    coset_two_copy_frame = subparsers.add_parser(
        "coset-two-copy-frame",
        help="Diagonalize the two-copy average frame and expose the missing Kronecker transition algebra.",
    )
    coset_two_copy_frame.add_argument("--n-values", default="4,5,6,7,8")
    coset_two_copy_frame.add_argument("--no-registry", action="store_true")
    coset_two_copy_frame.set_defaults(func=command_coset_two_copy_frame)

    coset_two_copy_transitions = subparsers.add_parser(
        "coset-two-copy-transitions",
        help="Measure finite cross-sector transition weights and reject factorial explicit tables.",
    )
    coset_two_copy_transitions.add_argument("--n-values", default="3,4")
    coset_two_copy_transitions.add_argument("--no-registry", action="store_true")
    coset_two_copy_transitions.set_defaults(func=command_coset_two_copy_transitions)

    coset_three_copy_recoupling = subparsers.add_parser(
        "coset-three-copy-recoupling",
        help="Prove the overlapping pair-class-sum obstruction and isolate associator proof debt.",
    )
    coset_three_copy_recoupling.add_argument("--n-values", default="3,4,5,6,7")
    coset_three_copy_recoupling.add_argument("--no-registry", action="store_true")
    coset_three_copy_recoupling.set_defaults(func=command_coset_three_copy_recoupling)

    coset_recoupling_capabilities = subparsers.add_parser(
        "coset-recoupling-capabilities",
        help="Separate solved QFT/projection primitives from open internal recoupling and decoding.",
    )
    coset_recoupling_capabilities.add_argument("--n-values", default="4,5,6,7,8,9,10")
    coset_recoupling_capabilities.add_argument("--no-registry", action="store_true")
    coset_recoupling_capabilities.set_defaults(func=command_coset_recoupling_capabilities)

    coset_jm_labels = subparsers.add_parser(
        "coset-jm-labels",
        help="Verify the polynomial diagonal YJM label transform and isolate unresolved Kronecker multiplicity space.",
    )
    coset_jm_labels.add_argument("--n-values", default="4,5,6")
    coset_jm_labels.add_argument("--no-registry", action="store_true")
    coset_jm_labels.set_defaults(func=command_coset_jm_labels)

    coset_multiplicity_commutant = subparsers.add_parser(
        "coset-multiplicity-commutant",
        help="Search bounded-support diagonal-action commutants inside Kronecker multiplicity registers.",
    )
    coset_multiplicity_commutant.add_argument("--n-values", default="5,6")
    coset_multiplicity_commutant.add_argument("--coefficient-bound", type=int, default=2)
    coset_multiplicity_commutant.add_argument("--no-registry", action="store_true")
    coset_multiplicity_commutant.set_defaults(func=command_coset_multiplicity_commutant)

    coset_commutant_gap_scaling = subparsers.add_parser(
        "coset-commutant-gap-scaling",
        help="Verify finite scaling of one uniform multiplicity-commutant gap family.",
    )
    coset_commutant_gap_scaling.add_argument("--n-values", default="6,7,8,9,10")
    coset_commutant_gap_scaling.add_argument("--no-registry", action="store_true")
    coset_commutant_gap_scaling.set_defaults(func=command_coset_commutant_gap_scaling)

    coset_commutant_gap_proof = subparsers.add_parser(
        "coset-commutant-gap-proof",
        help="Build the exact all-n Specht-polytabloid gap certificate.",
    )
    coset_commutant_gap_proof.add_argument("--no-registry", action="store_true")
    coset_commutant_gap_proof.set_defaults(func=command_coset_commutant_gap_proof)

    coset_racah_control = subparsers.add_parser(
        "coset-racah-control",
        help="Resolve finite parity-channel Racah subblocks and measure leakage into other intermediates.",
    )
    coset_racah_control.add_argument("--n", type=int, default=6)
    coset_racah_control.add_argument("--no-registry", action="store_true")
    coset_racah_control.set_defaults(func=command_coset_racah_control)

    coset_racah_complete_control = subparsers.add_parser(
        "coset-racah-complete-control",
        help="Assemble complete finite Racah matrices where second-stage coupling is multiplicity-free.",
    )
    coset_racah_complete_control.add_argument("--n", type=int, default=6)
    coset_racah_complete_control.add_argument("--no-registry", action="store_true")
    coset_racah_complete_control.set_defaults(
        func=command_coset_racah_complete_control
    )

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

    coset_racah_gap_scaling = subparsers.add_parser(
        "coset-racah-gap-scaling",
        help="Scale second-stage multiplicity gaps on the stable (n-2,2) three-copy target family.",
    )
    coset_racah_gap_scaling.add_argument("--n-values", default="6,7,8")
    coset_racah_gap_scaling.add_argument("--no-registry", action="store_true")
    coset_racah_gap_scaling.set_defaults(func=command_coset_racah_gap_scaling)

    coset_racah_sparse_gap = subparsers.add_parser(
        "coset-racah-sparse-gap",
        help="Extract the stable multiplicity-four Racah block sparsely and reconstruct integer quartics.",
    )
    coset_racah_sparse_gap.add_argument("--n-values", default="7,8,9,10")
    coset_racah_sparse_gap.add_argument("--no-registry", action="store_true")
    coset_racah_sparse_gap.set_defaults(func=command_coset_racah_sparse_gap)

    coset_racah_trace_conjecture = subparsers.add_parser(
        "coset-racah-trace-conjecture",
        help="Generate and hold out-test an exact trace formula target from sparse Racah quartics.",
    )
    coset_racah_trace_conjecture.add_argument("--training-count", type=int, default=4)
    coset_racah_trace_conjecture.add_argument("--no-registry", action="store_true")
    coset_racah_trace_conjecture.set_defaults(
        func=command_coset_racah_trace_conjecture
    )

    coset_racah_trace_proof = subparsers.add_parser(
        "coset-racah-trace-proof",
        help="Prove the stable Racah trace by exact falling-cycle equality patterns.",
    )
    coset_racah_trace_proof.add_argument("--no-registry", action="store_true")
    coset_racah_trace_proof.set_defaults(func=command_coset_racah_trace_proof)

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

    coset_recoupling_synthesize = subparsers.add_parser(
        "coset-recoupling-synthesize",
        help="Synthesize typed recoupling mechanisms and reject undefined or known-invalid architectures.",
    )
    coset_recoupling_synthesize.add_argument("--no-registry", action="store_true")
    coset_recoupling_synthesize.set_defaults(func=command_coset_recoupling_synthesize)

    cfi_code_reduction = subparsers.add_parser(
        "cfi-code-reduction",
        help="Certify the faithful CFI graph-to-code reduction and run legal graph-side dequantization attacks.",
    )
    cfi_code_reduction.add_argument(
        "--bases",
        default="complete-k5,triangular-prism,cube-q3,mobius-ladder-8,petersen,heawood-like-14",
    )
    cfi_code_reduction.add_argument("--seed", type=int, default=14_071)
    cfi_code_reduction.add_argument("--no-registry", action="store_true")
    cfi_code_reduction.add_argument("--verbose", action="store_true")
    cfi_code_reduction.set_defaults(func=command_cfi_code_reduction)

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

    code_equivalence = subparsers.add_parser("code-equivalence", help="Run binary linear-code equivalence audits and classical baselines.")
    code_equivalence.add_argument("--pairs", default="hamming-7-4-permuted,hamming-7-4-column-twist,random-8-4-weak-invariant-collision")
    code_equivalence.add_argument("--no-registry", action="store_true")
    code_equivalence.set_defaults(func=command_code_equivalence)

    code_invariants = subparsers.add_parser(
        "code-invariants",
        help="Run support-splitting, dual/hull, puncturing, and shortening code-equivalence invariant baselines.",
    )
    code_invariants.add_argument("--no-code-family-search", action="store_true")
    code_invariants.add_argument("--no-registry", action="store_true")
    code_invariants.add_argument("--verbose", action="store_true")
    code_invariants.set_defaults(func=command_code_invariants)

    code_info_sets = subparsers.add_parser(
        "code-info-sets",
        help="Run information-set canonicalization baselines for code-equivalence rows.",
    )
    code_info_sets.add_argument("--max-ordered-information-sets", type=int, default=250_000)
    code_info_sets.add_argument("--no-code-family-search", action="store_true")
    code_info_sets.add_argument("--no-registry", action="store_true")
    code_info_sets.add_argument("--verbose", action="store_true")
    code_info_sets.set_defaults(func=command_code_info_sets)

    code_canonicalize = subparsers.add_parser(
        "code-canonicalize",
        help="Run profile-pruned canonicalization baselines for code-equivalence rows.",
    )
    code_canonicalize.add_argument("--max-assignments", type=int, default=2_000_000)
    code_canonicalize.add_argument("--no-code-family-search", action="store_true")
    code_canonicalize.add_argument("--no-registry", action="store_true")
    code_canonicalize.add_argument("--verbose", action="store_true")
    code_canonicalize.set_defaults(func=command_code_canonicalize)

    code_profile_search = subparsers.add_parser(
        "code-profile-search",
        help="Search for code pairs colliding on coordinate-refinement profiles, then canonicalize them.",
    )
    code_profile_search.add_argument("--max-assignments", type=int, default=2_000_000)
    code_profile_search.add_argument("--no-registry", action="store_true")
    code_profile_search.add_argument("--verbose", action="store_true")
    code_profile_search.set_defaults(func=command_code_profile_search)

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

    code_qc_search = subparsers.add_parser(
        "code-qc-search",
        help="Search structured quasi-cyclic code families for tuple-profile collisions, then canonicalize them.",
    )
    code_qc_search.add_argument("--tuple-size", type=int, default=2)
    code_qc_search.add_argument("--tuple-cap", type=int, default=50_000)
    code_qc_search.add_argument("--no-registry", action="store_true")
    code_qc_search.add_argument("--verbose", action="store_true")
    code_qc_search.set_defaults(func=command_code_qc_search)

    code_qc_canonicalize = subparsers.add_parser(
        "code-qc-canonicalize",
        help="Canonicalize quasi-cyclic tuple-profile collision rows under block permutations and cyclic shifts.",
    )
    code_qc_canonicalize.add_argument("--max-group-size", type=int, default=250_000)
    code_qc_canonicalize.add_argument("--no-registry", action="store_true")
    code_qc_canonicalize.add_argument("--verbose", action="store_true")
    code_qc_canonicalize.set_defaults(func=command_code_qc_canonicalize)

    code_qc_info_resolve = subparsers.add_parser(
        "code-qc-info-resolve",
        help="Resolve quasi-cyclic proof-debt rows with exact information-set canonicalization.",
    )
    code_qc_info_resolve.add_argument("--max-ordered-information-sets", type=int, default=2_000_000)
    code_qc_info_resolve.add_argument("--audit-all-rows", action="store_true")
    code_qc_info_resolve.add_argument("--no-registry", action="store_true")
    code_qc_info_resolve.add_argument("--verbose", action="store_true")
    code_qc_info_resolve.set_defaults(func=command_code_qc_info_resolve)

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

    code_goppa_scaling = subparsers.add_parser(
        "code-goppa-scaling",
        help="Audit scalable punctured Goppa/alternant families with exact dual and Schur invariants.",
    )
    code_goppa_scaling.add_argument("--no-registry", action="store_true")
    code_goppa_scaling.add_argument("--verbose", action="store_true")
    code_goppa_scaling.set_defaults(func=command_code_goppa_scaling)

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

    code_goppa_projectors = subparsers.add_parser(
        "code-goppa-projectors",
        help="Apply the exact trivial-hull projector-to-GI reduction to scalable Goppa frontier pairs.",
    )
    code_goppa_projectors.add_argument("--max-search-seconds", type=float, default=10.0)
    code_goppa_projectors.add_argument("--no-registry", action="store_true")
    code_goppa_projectors.add_argument("--verbose", action="store_true")
    code_goppa_projectors.set_defaults(func=command_code_goppa_projectors)

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

    code_incidence_resolver = subparsers.add_parser(
        "code-incidence-resolve",
        help="Exactly resolve tractable rank-metric/QC proof-debt rows using full codeword-coordinate incidence graphs.",
    )
    code_incidence_resolver.add_argument("--max-codewords", type=int, default=4_096)
    code_incidence_resolver.add_argument("--max-search-seconds", type=float, default=20.0)
    code_incidence_resolver.add_argument("--no-registry", action="store_true")
    code_incidence_resolver.add_argument("--verbose", action="store_true")
    code_incidence_resolver.set_defaults(func=command_code_incidence_resolve)

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

    code_triage = subparsers.add_parser(
        "code-triage",
        help="Aggregate code-equivalence rows across structural, tuple, canonicalization, and QC baselines.",
    )
    code_triage.add_argument("--no-registry", action="store_true")
    code_triage.add_argument("--verbose", action="store_true")
    code_triage.set_defaults(func=command_code_triage)

    dequantize = subparsers.add_parser("dequantize", help="Scan candidates/results for classical dequantization risks.")
    dequantize.add_argument("--verbose", action="store_true")
    dequantize.set_defaults(func=command_dequantize)

    baselines = subparsers.add_parser("baselines", help="Run classical baseline sweeps across hidden-shift query/sample budgets.")
    baselines.add_argument("--families", default="bent_quadratic_f2,masked_quadratic_f2,quartic_character,kloosterman_trace,noisy_cubic_chirp,fp2_quadratic_form,mm_majority_bent_f2")
    baselines.add_argument("--n-values", default="5,6,7,8")
    baselines.add_argument("--sample-counts", default="4,8,16,32,64,128")
    baselines.add_argument("--shift", type=int, default=7)
    baselines.add_argument("--seed", type=int, default=0)
    baselines.add_argument("--no-registry", action="store_true")
    baselines.add_argument("--verbose", action="store_true")
    baselines.set_defaults(func=command_baselines)

    query_lower_bounds = subparsers.add_parser(
        "query-lower-bounds",
        aliases=["hidden-shift-lower-bounds"],
        help="Probe hidden-shift query/time lower-bound gaps with exhaustive candidate fingerprints.",
    )
    query_lower_bounds.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,kloosterman_trace,legendre_symbol,quartic_character,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2,noisy_cubic_chirp",
    )
    query_lower_bounds.add_argument("--n-values", default="5,6,7,8")
    query_lower_bounds.add_argument("--sample-counts", default="2,4,8,16,32,64")
    query_lower_bounds.add_argument("--shift", type=int, default=7)
    query_lower_bounds.add_argument("--seed", type=int, default=0)
    query_lower_bounds.add_argument("--trials", type=int, default=5)
    query_lower_bounds.add_argument("--no-registry", action="store_true")
    query_lower_bounds.add_argument("--verbose", action="store_true")
    query_lower_bounds.set_defaults(func=command_query_lower_bounds)

    learnability = subparsers.add_parser("learnability", help="Run low-degree and sparse-structure learnability baselines.")
    learnability.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,noisy_cubic_chirp,kloosterman_trace,quartic_character,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2",
    )
    learnability.add_argument("--n-values", default="5,6,7,8")
    learnability.add_argument("--samples", type=int, default=128)
    learnability.add_argument("--seed", type=int, default=0)
    learnability.add_argument("--no-registry", action="store_true")
    learnability.add_argument("--verbose", action="store_true")
    learnability.set_defaults(func=command_learnability)

    fourier_learnability = subparsers.add_parser(
        "fourier-learnability",
        aliases=["compressibility"],
        help="Run sparse Fourier and derivative-spectrum compressibility baselines.",
    )
    fourier_learnability.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,noisy_cubic_chirp,kloosterman_trace,quartic_character,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2",
    )
    fourier_learnability.add_argument("--n-values", default="5,6,7,8")
    fourier_learnability.add_argument("--sample-counts", default="4,8,16,32,64,128")
    fourier_learnability.add_argument("--no-registry", action="store_true")
    fourier_learnability.add_argument("--verbose", action="store_true")
    fourier_learnability.set_defaults(func=command_fourier_learnability)

    character_shift = subparsers.add_parser(
        "character-shift",
        help="Run multiplicative-character hidden-shift sample/elimination baselines.",
    )
    character_shift.add_argument("--families", default="legendre_symbol,quartic_character")
    character_shift.add_argument("--n-values", default="5,6,7,8")
    character_shift.add_argument("--sample-counts", default="2,4,8,16,32")
    character_shift.add_argument("--shift", type=int, default=7)
    character_shift.add_argument("--seed", type=int, default=0)
    character_shift.add_argument("--no-registry", action="store_true")
    character_shift.add_argument("--verbose", action="store_true")
    character_shift.set_defaults(func=command_character_shift)

    character_decoders = subparsers.add_parser(
        "character-decoders",
        help="Search non-exhaustive decoders for multiplicative-character hidden shifts.",
    )
    character_decoders.add_argument("--families", default="legendre_symbol,quartic_character")
    character_decoders.add_argument("--n-values", default="5,6,7,8")
    character_decoders.add_argument("--sample-counts", default="4,8,16,32")
    character_decoders.add_argument("--shift", type=int, default=7)
    character_decoders.add_argument("--seed", type=int, default=0)
    character_decoders.add_argument("--no-registry", action="store_true")
    character_decoders.add_argument("--verbose", action="store_true")
    character_decoders.set_defaults(func=command_character_decoders)

    character_lower_bound = subparsers.add_parser(
        "character-lower-bound",
        aliases=["character-decoding-lower-bound"],
        help="Build the multiplicative-character sample/decode lower-bound ledger.",
    )
    character_lower_bound.add_argument("--families", default="legendre_symbol,quartic_character")
    character_lower_bound.add_argument("--n-values", default="5,6,7,8")
    character_lower_bound.add_argument("--sample-counts", default="4,8,16,32")
    character_lower_bound.add_argument("--shift", type=int, default=7)
    character_lower_bound.add_argument("--seed", type=int, default=0)
    character_lower_bound.add_argument("--trials", type=int, default=5)
    character_lower_bound.add_argument("--no-registry", action="store_true")
    character_lower_bound.add_argument("--verbose", action="store_true")
    character_lower_bound.set_defaults(func=command_character_lower_bound)

    character_query_info = subparsers.add_parser(
        "character-query-info",
        aliases=["character-query-information"],
        help="Audit information-theoretic query ceilings for multiplicative-character shifts.",
    )
    character_query_info.add_argument("--families", default="legendre_symbol,quartic_character")
    character_query_info.add_argument("--n-values", default="5,6,7,8")
    character_query_info.add_argument("--failure-probability", type=float, default=0.01)
    character_query_info.add_argument("--no-registry", action="store_true")
    character_query_info.add_argument("--verbose", action="store_true")
    character_query_info.set_defaults(func=command_character_query_info)

    character_moments = subparsers.add_parser(
        "character-moments",
        aliases=["character-moment-obstruction"],
        help="Check exact low-degree moment obstructions for multiplicative-character shifts.",
    )
    character_moments.add_argument("--families", default="legendre_symbol,quartic_character")
    character_moments.add_argument("--n-values", default="5,6,7,8")
    character_moments.add_argument("--no-registry", action="store_true")
    character_moments.add_argument("--verbose", action="store_true")
    character_moments.set_defaults(func=command_character_moments)

    character_complexity = subparsers.add_parser(
        "character-complexity",
        help="Audit shifted-character classical upper bounds, preprocessing, advice, and reduction debt.",
    )
    character_complexity.add_argument("--families", default="legendre_symbol,quartic_character")
    character_complexity.add_argument("--n-values", default="5,6,7,8,9,10")
    character_complexity.add_argument("--shift", type=int, default=7)
    character_complexity.add_argument("--max-prefix-factor", type=int, default=8)
    character_complexity.add_argument("--no-registry", action="store_true")
    character_complexity.add_argument("--verbose", action="store_true")
    character_complexity.set_defaults(func=command_character_complexity)

    phase_naturalness = subparsers.add_parser(
        "phase-naturalness",
        help="Audit hidden-shift phase families for artificial masks and unsupported descriptions.",
    )
    phase_naturalness.add_argument(
        "--families",
        default="quadratic_chirp,cubic_chirp,noisy_cubic_chirp,kloosterman_trace,quartic_character,legendre_symbol,fp2_quadratic_form,mm_majority_bent_f2,bent_quadratic_f2,masked_quadratic_f2",
    )
    phase_naturalness.add_argument("--n-values", default="5,6,7,8")
    phase_naturalness.add_argument("--no-registry", action="store_true")
    phase_naturalness.add_argument("--verbose", action="store_true")
    phase_naturalness.set_defaults(func=command_phase_naturalness)

    trace_functions = subparsers.add_parser(
        "trace-functions",
        help="Search natural finite-field rational trace-function hidden-shift families.",
    )
    trace_functions.add_argument(
        "--families",
        default="trace_kloosterman_x_plus_inv,trace_quadratic_plus_inv,trace_cubic_plus_inv,trace_two_pole,trace_cubic_two_pole",
    )
    trace_functions.add_argument("--n-values", default="5,6,7,8")
    trace_functions.add_argument("--sample-counts", default="8,16,32,64")
    trace_functions.add_argument("--shift", type=int, default=7)
    trace_functions.add_argument("--seed", type=int, default=0)
    trace_functions.add_argument("--no-registry", action="store_true")
    trace_functions.add_argument("--verbose", action="store_true")
    trace_functions.set_defaults(func=command_trace_functions)

    family_triage = subparsers.add_parser("family-triage", help="Triage hidden-shift phase families across baseline artifacts.")
    family_triage.add_argument("--no-registry", action="store_true")
    family_triage.add_argument("--verbose", action="store_true")
    family_triage.set_defaults(func=command_family_triage)

    run = subparsers.add_parser("run", help="Run a registry experiment by id.")
    run.add_argument("experiment_id", nargs="?")
    run.add_argument("--all-supported", action="store_true")
    run.add_argument("--list-supported", action="store_true")
    run.add_argument("--verbose", action="store_true")
    run.set_defaults(func=command_run)

    run_next = subparsers.add_parser("run-next", help="Select and run the next highest-priority registry experiment.")
    run_next.add_argument("--dry-run", action="store_true")
    run_next.set_defaults(func=command_run_next)

    trends = subparsers.add_parser("trends", help="Build append-only experiment trend summaries.")
    trends.add_argument("--verbose", action="store_true")
    trends.set_defaults(func=command_trends)

    proofs = subparsers.add_parser("proofs", help="Build per-candidate proof-obligation status records.")
    proofs.add_argument("--verbose", action="store_true")
    proofs.set_defaults(func=command_proofs)

    reductions = subparsers.add_parser(
        "reductions",
        help="Build typed reduction edges and reject routes with unproved model, complexity, or family coverage.",
    )
    reductions.add_argument("--max-verbose-issues", type=int, default=4)
    reductions.add_argument("--verbose", action="store_true")
    reductions.set_defaults(func=command_reductions)

    reduction_contracts = subparsers.add_parser(
        "reduction-contracts",
        help="Audit candidate interfaces against exact primary-source reduction theorem contracts.",
    )
    reduction_contracts.add_argument("--max-verbose-checks", type=int, default=5)
    reduction_contracts.add_argument("--verbose", action="store_true")
    reduction_contracts.set_defaults(func=command_reduction_contracts)

    proof_queue = subparsers.add_parser("proof-queue", help="Build a prioritized proof-debt work queue with commands and kill criteria.")
    proof_queue.add_argument("--max-items", type=int, default=30)
    proof_queue.add_argument("--verbose", action="store_true")
    proof_queue.set_defaults(func=command_proof_queue)

    sweep = subparsers.add_parser("sweep", help="Run parameter sweeps for executable workbenches.")
    sweep.add_argument("--kind", choices=["hidden-shift"], default="hidden-shift")
    sweep.add_argument("--n-values", default="5,6,7,8")
    sweep.add_argument("--sample-counts", default="256,512,1024,2048")
    sweep.add_argument("--families", default="bent_quadratic_f2,masked_quadratic_f2,quartic_character,kloosterman_trace,noisy_cubic_chirp")
    sweep.add_argument("--shift", type=int, default=7)
    sweep.add_argument("--seed", type=int, default=0)
    sweep.add_argument("--no-registry", action="store_true")
    sweep.set_defaults(func=command_sweep)

    conjectures = subparsers.add_parser("conjectures", help="Build candidate conjecture, assumption, reduction, and blocker records.")
    conjectures.add_argument("--verbose", action="store_true")
    conjectures.set_defaults(func=command_conjectures)

    mutate = subparsers.add_parser("mutate", help="Generate blocker-driven mutation proposals without accepting them as candidates.")
    mutate.add_argument("--verbose", action="store_true")
    mutate.set_defaults(func=command_mutate)

    quarantine_invalid = subparsers.add_parser(
        "quarantine-invalid",
        help="Move mutation candidates with failed exact access contracts out of the accepted registry.",
    )
    quarantine_invalid.add_argument("--verbose", action="store_true")
    quarantine_invalid.set_defaults(func=command_quarantine_invalid)

    blockers = subparsers.add_parser("blockers", help="Cluster dequantization, proof-debt, and negative-result blockers.")
    blockers.add_argument("--verbose", action="store_true")
    blockers.set_defaults(func=command_blockers)

    frontiers = subparsers.add_parser("frontiers", help="Rank research frontiers from current blockers and artifacts.")
    frontiers.add_argument("--verbose", action="store_true")
    frontiers.set_defaults(func=command_frontiers)

    query_models = subparsers.add_parser("query-models", help="Build candidate-level query-model and lower-bound obligation records.")
    query_models.add_argument("--verbose", action="store_true")
    query_models.set_defaults(func=command_query_models)

    ingest_papers = subparsers.add_parser("ingest-papers", help="Extract mechanism records from local .tex/.txt/.md/.pdf papers.")
    ingest_papers.add_argument("paths", nargs="*", type=Path)
    ingest_papers.add_argument("--arxiv-id", action="append", default=[])
    ingest_papers.add_argument("--verbose", action="store_true")
    ingest_papers.set_defaults(func=command_ingest_papers)

    propose = subparsers.add_parser("propose", help="Register proof-gated seed candidates or a candidate JSON file.")
    propose.add_argument("--file", type=Path)
    propose.set_defaults(func=command_propose)

    validate = subparsers.add_parser("validate", help="Validate candidates and experiments against proof obligations.")
    validate.set_defaults(func=command_validate)

    list_cmd = subparsers.add_parser("list", help="List registry records.")
    list_cmd.add_argument(
        "--kind",
        choices=[
            "all",
            "candidates",
            "experiments",
            "results",
            "dequantization",
            "proofs",
            "reductions",
            "reduction-contracts",
            "scaling",
            "conjectures",
            "mutations",
            "negative",
            "rejected",
        ],
        default="all",
    )
    list_cmd.add_argument("--limit", type=int, default=20)
    list_cmd.add_argument("--verbose", action="store_true")
    list_cmd.set_defaults(func=command_list)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
