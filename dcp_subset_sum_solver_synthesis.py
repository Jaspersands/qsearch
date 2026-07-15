"""Typed hypothesis synthesis for Regev-compatible partial subset-sum solvers."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_SOLVER_SYNTHESIS_PATH = Path("research/hypotheses/dcp_subset_sum_solver_synthesis.json")
SUBSET_SUM_BRIDGE_PATH = Path("research/reductions/dcp_subset_sum_bridge.json")
SUBSET_SUM_LATTICE_PATH = Path("research/classical_baselines/dcp_subset_sum_lattice_search.json")
SUBSET_SUM_TWO_ADIC_PATH = Path("research/classical_baselines/dcp_subset_sum_two_adic_search.json")
SUBSET_SUM_RESOURCE_PATH = Path("research/classical_baselines/dcp_subset_sum_resource_frontier.json")
SUBSET_SUM_CARRY_ANF_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_anf.json")
SUBSET_SUM_LOW_BIT_BDD_PATH = Path("research/classical_baselines/dcp_subset_sum_low_bit_bdd.json")
SUBSET_SUM_CONDITIONED_QUOTIENT_PATH = Path("research/classical_baselines/dcp_subset_sum_conditioned_quotient.json")
SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH = Path("research/classical_baselines/dcp_subset_sum_preconditioned_geometry.json")
CARRY_HIGH_PART_NO_GO_PATH = Path("research/classical_baselines/dcp_carry_high_part_no_go.json")
BOOLEAN_COSET_SEPARATION_PATH = Path("research/classical_baselines/dcp_subset_sum_boolean_coset_separation.json")
MARKER_AWARE_LIST_DECODER_PATH = Path("research/classical_baselines/dcp_marker_aware_list_decoder.json")
MARKER_DEVIATION_GEOMETRY_PATH = Path("research/classical_baselines/dcp_marker_deviation_geometry.json")
MARKER_ALL_TARGET_COVERAGE_PATH = Path("research/classical_baselines/dcp_marker_all_target_coverage.json")
SUBSET_SUM_FOURTH_MOMENT_PATH = Path("research/classical_baselines/dcp_subset_sum_fourth_moment_obstruction.json")
SUBSET_SUM_SMITH_MOMENT_PATH = Path("research/classical_baselines/dcp_subset_sum_smith_moment_spectrum.json")
SUBSET_SUM_SMITH_TRANSFER_PATH = Path("research/classical_baselines/dcp_subset_sum_smith_transfer_order_six.json")
SUBSET_SUM_FIXED_ORDER_MOMENT_PATH = Path("research/classical_baselines/dcp_subset_sum_fixed_order_moment_theorem.json")
SUBSET_SUM_CONDITIONED_TAIL_PATH = Path("research/classical_baselines/dcp_subset_sum_conditioned_tail_theorem.json")
SUBSET_SUM_GROWING_ORDER_PATH = Path("research/classical_baselines/dcp_subset_sum_growing_order_theorem.json")
SUBSET_SUM_EMBEDDING_VOLUME_PATH = Path("research/classical_baselines/dcp_subset_sum_embedding_volume_theorem.json")
SUBSET_SUM_SHORT_RELATION_PATH = Path("research/classical_baselines/dcp_subset_sum_short_relation_theorem.json")
SUBSET_SUM_CARRY_RELATION_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_relation_theorem.json")
SUBSET_SUM_MARKER_COSET_PATH = Path("research/reductions/dcp_subset_sum_marker_coset_theorem.json")
SUBSET_SUM_AFFINE_CVP_PATH = Path("research/classical_baselines/dcp_subset_sum_affine_cvp_baseline.json")
SUBSET_SUM_AFFINE_CVP_SCALING_PATH = Path("research/classical_baselines/dcp_subset_sum_affine_cvp_scaling.json")
SUBSET_SUM_AFFINE_BDD_PATH = Path("research/classical_baselines/dcp_subset_sum_affine_bdd_geometry.json")
SUBSET_SUM_CARRY_SLICE_LATTICE_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_slice_lattice.json")
SUBSET_SUM_TARGET_DISTRIBUTION_PATH = Path("research/classical_baselines/dcp_subset_sum_target_distribution.json")
COHERENT_MATCHING_INTERFACE_PATH = Path("research/reductions/dcp_coherent_matching_interface.json")
QUANTUM_RELATION_FIDELITY_PATH = Path("research/reductions/dcp_quantum_relation_fidelity.json")
QUANTUM_WALK_SOURCE_AUDIT_PATH = Path("research/reductions/dcp_quantum_walk_source_audit.json")
SYMMETRIC_RELATION_LIFT_PATH = Path("research/reductions/dcp_symmetric_relation_lift.json")
TWO_ADIC_FIBER_TRANSPORT_PATH = Path("research/phase_workbench/dcp_two_adic_fiber_transport.json")
FIBER_TRANSPORT_GRAPH_PATH = Path("research/phase_workbench/dcp_fiber_transport_graph.json")
SIGNED_PERMUTATION_TRANSPORT_PATH = Path("research/phase_workbench/dcp_signed_permutation_transport.json")
AFFINE_TRANSPORT_PATH = Path("research/phase_workbench/dcp_affine_transport.json")
FIBER_BALANCE_OBSTRUCTION_PATH = Path("research/phase_workbench/dcp_fiber_balance_obstruction.json")
PARTIAL_RELATION_COVERAGE_PATH = Path("research/phase_workbench/dcp_partial_relation_coverage.json")
TARGET_INDEXED_LOCALITY_PATH = Path("research/phase_workbench/dcp_target_indexed_locality.json")
FIBER_ENTANGLEMENT_PATH = Path("research/phase_workbench/dcp_fiber_entanglement.json")
ADAPTIVE_LAYOUT_PATH = Path("research/phase_workbench/dcp_adaptive_layout_audit.json")
RANDOM_SELF_REDUCTION_PATH = Path("research/reductions/dcp_subset_sum_random_self_reduction.json")
ODD_UNIT_ORBIT_GEOMETRY_PATH = Path("research/classical_baselines/dcp_odd_unit_orbit_geometry.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-SOLVER-SYNTHESIS"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class SolverPrimitive:
    primitive_id: str
    role: str
    current_evidence: str
    resource_status: str
    interface_status: str


@dataclass(frozen=True)
class SolverHypothesis:
    hypothesis_id: str
    title: str
    primitive_ids: list[str]
    mechanism: str
    novelty_over_tested_routes: str
    expected_upside: str
    proof_obligations: list[str]
    first_experiments: list[str]
    falsifiers: list[str]
    preflight_status: str
    rejection_reason: str | None
    priority_score: int


@dataclass(frozen=True)
class DCPSubsetSumSolverSynthesisReport:
    created_at: str
    source_contract: dict[str, str]
    primitives: list[SolverPrimitive]
    hypotheses: list[SolverHypothesis]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _metrics(path: Path) -> dict[str, Any]:
    return _read_json(path).get("headline_metrics", {})


def build_solver_primitives() -> list[SolverPrimitive]:
    bridge = _metrics(SUBSET_SUM_BRIDGE_PATH)
    lattice = _metrics(SUBSET_SUM_LATTICE_PATH)
    two_adic = _metrics(SUBSET_SUM_TWO_ADIC_PATH)
    resource = _metrics(SUBSET_SUM_RESOURCE_PATH)
    carry = _metrics(SUBSET_SUM_CARRY_ANF_PATH)
    low_bit_bdd = _metrics(SUBSET_SUM_LOW_BIT_BDD_PATH)
    conditioned_quotient = _metrics(SUBSET_SUM_CONDITIONED_QUOTIENT_PATH)
    preconditioned_geometry = _metrics(SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH)
    carry_high_part = _metrics(CARRY_HIGH_PART_NO_GO_PATH)
    boolean_coset = _metrics(BOOLEAN_COSET_SEPARATION_PATH)
    marker_list = _metrics(MARKER_AWARE_LIST_DECODER_PATH)
    marker_deviations = _metrics(MARKER_DEVIATION_GEOMETRY_PATH)
    marker_all_targets = _metrics(MARKER_ALL_TARGET_COVERAGE_PATH)
    fourth_moment = _metrics(SUBSET_SUM_FOURTH_MOMENT_PATH)
    smith_moments = _metrics(SUBSET_SUM_SMITH_MOMENT_PATH)
    smith_transfer = _metrics(SUBSET_SUM_SMITH_TRANSFER_PATH)
    fixed_order_moments = _metrics(SUBSET_SUM_FIXED_ORDER_MOMENT_PATH)
    conditioned_tail = _metrics(SUBSET_SUM_CONDITIONED_TAIL_PATH)
    growing_order = _metrics(SUBSET_SUM_GROWING_ORDER_PATH)
    embedding_volume = _metrics(SUBSET_SUM_EMBEDDING_VOLUME_PATH)
    short_relations = _metrics(SUBSET_SUM_SHORT_RELATION_PATH)
    carry_relations = _metrics(SUBSET_SUM_CARRY_RELATION_PATH)
    marker_coset = _metrics(SUBSET_SUM_MARKER_COSET_PATH)
    affine_cvp = _metrics(SUBSET_SUM_AFFINE_CVP_PATH)
    affine_cvp_scaling = _metrics(SUBSET_SUM_AFFINE_CVP_SCALING_PATH)
    affine_bdd = _metrics(SUBSET_SUM_AFFINE_BDD_PATH)
    carry_slice_lattice = _metrics(SUBSET_SUM_CARRY_SLICE_LATTICE_PATH)
    target_distribution = _metrics(SUBSET_SUM_TARGET_DISTRIBUTION_PATH)
    coherent_matching = _metrics(COHERENT_MATCHING_INTERFACE_PATH)
    quantum_relation_fidelity = _metrics(QUANTUM_RELATION_FIDELITY_PATH)
    quantum_walk_source = _metrics(QUANTUM_WALK_SOURCE_AUDIT_PATH)
    symmetric_relation_lift = _metrics(SYMMETRIC_RELATION_LIFT_PATH)
    two_adic_fiber_transport = _metrics(TWO_ADIC_FIBER_TRANSPORT_PATH)
    fiber_transport_graph = _metrics(FIBER_TRANSPORT_GRAPH_PATH)
    signed_permutation_transport = _metrics(SIGNED_PERMUTATION_TRANSPORT_PATH)
    affine_transport = _metrics(AFFINE_TRANSPORT_PATH)
    fiber_balance = _metrics(FIBER_BALANCE_OBSTRUCTION_PATH)
    partial_relation = _metrics(PARTIAL_RELATION_COVERAGE_PATH)
    target_indexed_locality = _metrics(TARGET_INDEXED_LOCALITY_PATH)
    fiber_entanglement = _metrics(FIBER_ENTANGLEMENT_PATH)
    adaptive_layout = _metrics(ADAPTIVE_LAYOUT_PATH)
    random_self_reduction = _metrics(RANDOM_SELF_REDUCTION_PATH)
    odd_unit_geometry = _metrics(ODD_UNIT_ORBIT_GEOMETRY_PATH)
    return [
        SolverPrimitive(
            primitive_id="partial-source-contract",
            role="target interface",
            current_evidence=(
                f"source reductions={bridge.get('primary_source_conditional_dcp_reduction_count', 0)}; contract rows="
                f"{bridge.get('source_contract_satisfying_row_count', 0)}"
            ),
            resource_status="requires deterministic poly(n) time and inverse-polynomial legal coverage",
            interface_status="source verified; solver open",
        ),
        SolverPrimitive(
            primitive_id="coherent-matching-interface",
            role="solver-to-DCP composition contract",
            current_evidence=(
                f"seeded bridge certificates="
                f"{coherent_matching.get('proved_seeded_randomized_solver_bridge_count', 0)}/"
                f"{coherent_matching.get('seeded_bridge_certificate_count', 0)}; zero-visibility counterexamples="
                f"{coherent_matching.get('zero_visibility_counterexample_count', 0)}; arbitrary quantum bridges="
                f"{coherent_matching.get('proved_arbitrary_quantum_relation_solver_bridge_count', 0)}"
            ),
            resource_status="shared-seed interface overhead is polynomial; no partial subset-sum solver is constructed",
            interface_status=(
                "explicit target-independent shared-seed randomness proved compatible; arbitrary quantum relation "
                "requires canonicalization or paired-workspace fidelity"
            ),
        ),
        SolverPrimitive(
            primitive_id="quantum-relation-fidelity",
            role="paired endpoint amplitude and witness/history workspace composition gate",
            current_evidence=(
                f"zero/exponential-history mechanisms="
                f"{quantum_relation_fidelity.get('exact_zero_visibility_count', 0)}/"
                f"{quantum_relation_fidelity.get('exponential_history_overlap_count', 0)}; inverse-polynomial overlap proofs="
                f"{quantum_relation_fidelity.get('proved_inverse_polynomial_overlap_count', 0)}; polynomial partial solvers="
                f"{quantum_relation_fidelity.get('proved_polynomial_partial_solver_count', 0)}; full compositions="
                f"{quantum_relation_fidelity.get('proved_full_quantum_relation_composition_count', 0)}"
            ),
            resource_status=(
                "exact uniform-support overlap identity is proved; arbitrary amplitudes require an explicit inner-product "
                "calculation from a concrete circuit"
            ),
            interface_status=(
                "shared-seed control composes but constructs no solver; endpoint-tagged and sparse-history shortcuts are "
                "rejected; canonical cleanup remains proof debt"
            ),
        ),
        SolverPrimitive(
            primitive_id="source-audited-quantum-walk",
            role="concrete exponential quantum-walk mechanism and output-interface audit target",
            current_evidence=(
                f"source claims={quantum_walk_source.get('verified_source_claim_count', 0)}/"
                f"{quantum_walk_source.get('primary_source_claim_count', 0)}; internal history certificates="
                f"{quantum_walk_source.get('internal_history_independence_certificate_count', 0)}; positive "
                f"exponential time/memory={quantum_walk_source.get('positive_exponential_time_count', 0)}/"
                f"{quantum_walk_source.get('positive_exponential_memory_count', 0)}; QRAQM="
                f"{quantum_walk_source.get('qraqm_required_count', 0)}; paired-output/full-composition="
                f"{quantum_walk_source.get('paired_endpoint_output_fidelity_theorem_count', 0)}/"
                f"{quantum_walk_source.get('full_regev_composition_count', 0)}"
            ),
            resource_status=(
                "source-certified time and memory exponent 0.2182 in QRAQM; mechanism baseline only, not polynomial"
            ),
            interface_status=(
                "internal walk history consistency is certified; canonical paired marked-witness output and Regev "
                "composition are not certified"
            ),
        ),
        SolverPrimitive(
            primitive_id="symmetric-quantum-relation-lift",
            role="purified relation-solver to Regev matching interface",
            current_evidence=(
                f"interface certificates={symmetric_relation_lift.get('coherent_relation_interface_certificate_count', 0)}; "
                f"exact pair identities={symmetric_relation_lift.get('exact_symmetric_pair_identity_count', 0)}/"
                f"{symmetric_relation_lift.get('symmetric_pair_identity_count', 0)}; fixed/global loss exponents="
                f"{symmetric_relation_lift.get('fixed_list_weighted_matching_loss_exponent', 0)}/"
                f"{symmetric_relation_lift.get('global_source_weighted_matching_loss_exponent', 0)}; polynomial "
                f"relation solvers={symmetric_relation_lift.get('proved_polynomial_relation_solver_count', 0)}; product "
                f"contamination certificates={symmetric_relation_lift.get('product_contamination_composition_certificate_count', 0)}"
            ),
            resource_status=(
                "two purified solver calls per endpoint pair and polynomial matching-family overhead; solver resources dominate"
            ),
            interface_status=(
                "conditional product-source lift proved without deterministic selection; marginal-only contamination remains out of scope"
            ),
        ),
        SolverPrimitive(
            primitive_id="two-adic-fiber-transport",
            role="reversible low-fiber child transport and target-partial/walk search space",
            current_evidence=(
                f"exact identities={two_adic_fiber_transport.get('exact_identity_certificate_count', 0)}; "
                f"single/swap/block linear-depth rows={two_adic_fiber_transport.get('linear_depth_single_flip_count', 0)}/"
                f"{two_adic_fiber_transport.get('linear_depth_swap_count', 0)}/"
                f"{two_adic_fiber_transport.get('linear_depth_block_transport_count', 0)}; local no-go rows="
                f"{two_adic_fiber_transport.get('local_dictionary_linear_depth_no_go_count', 0)}; open implicit "
                f"architectures={two_adic_fiber_transport.get('open_implicit_transport_architecture_count', 0)}"
            ),
            resource_status=(
                "explicit local dictionaries and all total full-cube transports are closed; target-partial map or polynomial-gap walk unconstructed"
            ),
            interface_status=(
                "exact local child-fiber identities proved; full verified relation output remains open"
            ),
        ),
        SolverPrimitive(
            primitive_id="fiber-transport-graph-walk",
            role="implicit child-fiber transfer through local-move graph spectral structure",
            current_evidence=(
                f"linear rows={fiber_transport_graph.get('linear_depth_row_count', 0)}; fragmented/zero-cross-child="
                f"{fiber_transport_graph.get('fragmented_linear_depth_row_count', 0)}/"
                f"{fiber_transport_graph.get('zero_cross_child_linear_depth_row_count', 0)}; minimum positive finite gap="
                f"{fiber_transport_graph.get('minimum_positive_linear_depth_spectral_gap', 0)}; uniform gap/walk/classical "
                f"separation={fiber_transport_graph.get('uniform_polynomial_spectral_gap_theorem_count', 0)}/"
                f"{fiber_transport_graph.get('proved_polynomial_fiber_transport_walk_count', 0)}/"
                f"{fiber_transport_graph.get('proved_classical_separation_count', 0)}"
            ),
            resource_status=(
                "finite exact graph enumeration and BFS only; linear-depth state preparation and uniform coherent walk costs unproved"
            ),
            interface_status=(
                "source-uniform low residues and cross-child labels audited; verified polynomial relation output open"
            ),
        ),
        SolverPrimitive(
            primitive_id="signed-permutation-transport-no-go",
            role="exact exclusion of total signed-coordinate fiber transports",
            current_evidence=(
                f"classification theorems={signed_permutation_transport.get('exact_classification_theorem_count', 0)}; "
                f"exhaustive tuples/mismatches={signed_permutation_transport.get('exhaustive_label_tuple_count', 0)}/"
                f"{signed_permutation_transport.get('exhaustive_classification_mismatch_count', 0)}; linear-depth "
                f"no-go rows={signed_permutation_transport.get('linear_depth_exponential_no_go_row_count', 0)}/"
                f"{signed_permutation_transport.get('linear_depth_scaling_row_count', 0)}"
            ),
            resource_status=(
                "closed: total coordinate permutations with complements have only the exponentially rare exact-valuation pivot incidence"
            ),
            interface_status=(
                "no solver primitive produced; the broader Fourier theorem closes all total full-cube mechanisms"
            ),
        ),
        SolverPrimitive(
            primitive_id="affine-transport-witness-reduction",
            role="exact affine verifier and direct-witness equivalence",
            current_evidence=(
                f"ANF/witness theorems={affine_transport.get('exact_anf_theorem_count', 0)}/"
                f"{affine_transport.get('zero_image_witness_reduction_count', 0)}; mismatches="
                f"{affine_transport.get('anf_vs_truth_table_mismatch_count', 0)}; affine-only instances="
                f"{affine_transport.get('nonmonomial_affine_only_instance_count', 0)}; polynomial searches="
                f"{affine_transport.get('polynomial_affine_search_count', 0)}"
            ),
            resource_status=(
                "closed as a total transport route; constructing T already constructs b=T(0), and the full-cube theorem forces a pivot"
            ),
            interface_status=(
                "retain the ANF verifier only for explicitly partial target-fiber proposals"
            ),
        ),
        SolverPrimitive(
            primitive_id="total-transport-fourier-no-go",
            role="exact exclusion of every total full-cube next-bit transport",
            current_evidence=(
                f"theorems/mismatches={fiber_balance.get('exact_total_transport_fourier_theorem_count', 0)}/"
                f"{fiber_balance.get('finite_theorem_mismatch_count', 0)}; linear pivot rows="
                f"{fiber_balance.get('linear_depth_pivot_row_count', 0)}/"
                f"{fiber_balance.get('linear_depth_row_count', 0)}; partial-pairing mass range="
                f"{fiber_balance.get('minimum_linear_depth_optimal_partial_pairing_mass', 0)}-"
                f"{fiber_balance.get('maximum_linear_depth_optimal_partial_pairing_mass', 0)}; polynomial target maps="
                f"{fiber_balance.get('proved_polynomial_target_fiber_map_count', 0)}"
            ),
            resource_status=(
                "total route closed exactly; target-dependent partial maps have no polynomial construction"
            ),
            interface_status=(
                "surviving maps must declare target law, partial coverage, success flag, inverse-on-image, and classical relation access"
            ),
        ),
        SolverPrimitive(
            primitive_id="explicit-partial-relation-coverage-no-go",
            role="exclude polynomial dictionaries of fixed signed-difference partial maps",
            current_evidence=(
                f"linear-support/dictionary theorems={partial_relation.get('linear_minimum_support_theorem_count', 0)}/"
                f"{partial_relation.get('polynomial_dictionary_exponential_coverage_theorem_count', 0)}; union-bound "
                f"exponent={partial_relation.get('asymptotic_union_bound_exponent', 0)}; existence/dictionary no-go rows="
                f"{partial_relation.get('asymptotic_inverse_polynomial_existence_no_go_row_count', 0)}/"
                f"{partial_relation.get('asymptotic_inverse_polynomial_dictionary_coverage_no_go_row_count', 0)}; "
                f"implicit target-indexed no-go theorems={partial_relation.get('proved_target_indexed_implicit_map_no_go_count', 0)}"
            ),
            resource_status=(
                "polynomial explicit masks closed by linear minimum support and exponential compatible-domain loss"
            ),
            interface_status=(
                "survivors must be implicitly target-indexed or nontranslation and prove source-law coverage explicitly"
            ),
        ),
        SolverPrimitive(
            primitive_id="target-indexed-locality-no-go",
            role="exclude arbitrary implicit maps confined to a low-radius Hamming ball",
            current_evidence=(
                f"local-map/batch theorems="
                f"{target_indexed_locality.get('arbitrary_target_indexed_local_map_no_go_theorem_count', 0)}/"
                f"{target_indexed_locality.get('polynomial_source_batch_local_map_no_go_theorem_count', 0)}; "
                f"entropy threshold/chosen beta="
                f"{target_indexed_locality.get('entropy_threshold_locality_fraction', 0)}/"
                f"{target_indexed_locality.get('chosen_locality_fraction', 0)}; polynomial classical/quantum solvers="
                f"{target_indexed_locality.get('polynomial_classical_relation_solver_count', 0)}/"
                f"{target_indexed_locality.get('polynomial_quantum_relation_solver_count', 0)}; unrestricted time "
                f"lower bounds={target_indexed_locality.get('unrestricted_linear_support_time_lower_bound_count', 0)}"
            ),
            resource_status=(
                "all beta-local target-indexed maps below the entropy threshold are closed; linear-support search complexity remains open"
            ),
            interface_status=(
                "survivors must output linear-distance partners under the exact source law and expose identical label access to classical baselines"
            ),
        ),
        SolverPrimitive(
            primitive_id="fiber-entanglement-bond-obstruction",
            role="exclude exact low-bond density-one tensor preparation while preserving approximate-route debt",
            current_evidence=(
                f"exact-spectrum/random-rank/density-one no-go theorems="
                f"{fiber_entanglement.get('exact_schmidt_decomposition_theorem_count', 0)}/"
                f"{fiber_entanglement.get('constant_fraction_exponential_rank_theorem_count', 0)}/"
                f"{fiber_entanglement.get('exact_polynomial_bond_density_one_no_go_theorem_count', 0)}; minimum hard "
                f"probability={fiber_entanglement.get('minimum_certified_hard_instance_probability', 0)}; approximate "
                f"bond/layout/general-circuit no-go theorems="
                f"{fiber_entanglement.get('approximate_polynomial_bond_asymptotic_no_go_theorem_count', 0)}/"
                f"{fiber_entanglement.get('polynomial_layout_dictionary_density_one_no_go_theorem_count', 0)}/"
                f"{fiber_entanglement.get('general_quantum_circuit_lower_bound_count', 0)}; polynomial preparations/solvers="
                f"{fiber_entanglement.get('polynomial_fiber_state_preparation_count', 0)}/"
                f"{fiber_entanglement.get('polynomial_relation_solver_count', 0)}"
            ),
            resource_status=(
                "exact and 99-percent-fidelity polynomial-bond density-one routes and fixed polynomial layout dictionaries closed; label-adaptive and partial tensors unclassified"
            ),
            interface_status=(
                "surviving partial-instance tensor proposals must prove source coverage, coherent preparation, verified output, and matched classical contraction"
            ),
        ),
        SolverPrimitive(
            primitive_id="adaptive-layout-valuation-obstruction",
            role="separate impossible valuation compression from open additive label-adaptive layouts",
            current_evidence=(
                f"valuation theorems/no-go rows="
                f"{adaptive_layout.get('adaptive_valuation_compression_no_go_theorem_count', 0)}/"
                f"{adaptive_layout.get('valuation_inverse_polynomial_no_go_row_count', 0)}; exact/evaluated layouts="
                f"{adaptive_layout.get('exact_balanced_optimum_row_count', 0)}/"
                f"{adaptive_layout.get('evaluated_layout_count', 0)}; fitted rank slope="
                f"{adaptive_layout.get('fitted_tail_best_log2_rank_slope_per_n', 0)}; polynomial selector/contractions="
                f"{adaptive_layout.get('polynomial_selector_and_contraction_count', 0)}; general adaptive theorems="
                f"{adaptive_layout.get('general_adaptive_layout_no_go_theorem_count', 0)}"
            ),
            resource_status=(
                "valuation-only adaptive cuts closed; exact-rank adaptive selection costs O(m 2^q) per layout"
            ),
            interface_status=(
                "surviving additive layout needs a polynomial selector, all-n bond/source theorem, coherent contraction, and relation output"
            ),
        ),
        SolverPrimitive(
            primitive_id="source-preserving-random-self-reduction",
            role="randomize canonical subset-sum presentation without changing Regev's source law",
            current_evidence=(
                f"source bijections="
                f"{random_self_reduction.get('source_distribution_bijection_certificate_count', 0)}/"
                f"{random_self_reduction.get('algebra_certificate_count', 0)}; sign isometries="
                f"{random_self_reduction.get('signed_embedding_isometry_certificate_count', 0)}; odd-unit rescues="
                f"{random_self_reduction.get('odd_unit_rescue_count', 0)}; tail odd-unit success="
                f"{random_self_reduction.get('tail_odd_unit_unconditional_success_count', 0)}/"
                f"{random_self_reduction.get('tail_trial_count', 0)}; orbit-geometry slope="
                f"{odd_unit_geometry.get('fitted_log2_unconditional_success_slope_per_n', 'unknown')}; orbit tail="
                f"{odd_unit_geometry.get('tail_verified_witness_count', 0)}/"
                f"{odd_unit_geometry.get('tail_record_count', 0)}"
            ),
            resource_status="polynomial explicit seed budget and LLL calls; no uniform orbit-hitting theorem",
            interface_status=(
                "exact source and witness bijection plus shared-seed compatibility proved; signs are isometric controls, "
                "odd units remain a non-isometric presentation search"
            ),
        ),
        SolverPrimitive(
            primitive_id="modular-lattice-embedding",
            role="global arithmetic geometry",
            current_evidence=(
                f"finite/tail success rows={lattice.get('finite_success_row_count', 0)}/"
                f"{lattice.get('tail_success_row_count', 0)}; coverage proofs="
                f"{lattice.get('proved_uniform_inverse_polynomial_coverage_count', 0)}"
            ),
            resource_status="polynomial LLL baseline; tested geometry loses tail coverage",
            interface_status="deterministic but no coverage/reversible theorem",
        ),
        SolverPrimitive(
            primitive_id="two-adic-lift-representation",
            role="power-of-two local arithmetic",
            current_evidence=(
                f"degree-censored lifts={two_adic.get('degree_censored_lift_count', 0)}; all-affine legal trials="
                f"{two_adic.get('all_lifts_affine_trial_count', 0)}"
            ),
            resource_status="exact current representation costs 2^(n+O(1))",
            interface_status="no compact exact fiber or witness solver",
        ),
        SolverPrimitive(
            primitive_id="logarithmic-low-bit-bdd",
            role="exact polynomial preconditioner and conditional state preparation",
            current_evidence=(
                f"polynomial width/state-preparation certificates="
                f"{low_bit_bdd.get('polynomial_width_certificate_count', 0)}/"
                f"{low_bit_bdd.get('polynomial_state_preparation_certificate_count', 0)}; linear residual certificates="
                f"{low_bit_bdd.get('linear_residual_entropy_certificate_count', 0)}"
            ),
            resource_status="polynomial for b=O(log n); residual high-bit witness space remains exponential",
            interface_status="reversible low-fiber preparation proved; high-bit geometry/decoder open",
        ),
        SolverPrimitive(
            primitive_id="conditioned-high-bit-quotient",
            role="postconditioned average-case geometry",
            current_evidence=(
                f"tail minimum normalized entropy="
                f"{conditioned_quotient.get('minimum_tail_normalized_shannon_entropy', 'unknown')}; maximum target mass="
                f"{conditioned_quotient.get('maximum_tail_exact_target_probability', 'unknown')}; geometry improvements="
                f"{conditioned_quotient.get('proved_high_bit_geometry_improvement_count', 0)}"
            ),
            resource_status="exact finite audit exponential; explicit polynomial quotient lists do not decode",
            interface_status="needs asymptotic quotient law and polynomial implicit decoder",
        ),
        SolverPrimitive(
            primitive_id="conditional-residual-pairwise-moment-theorem",
            role="no-go gate for count-only low-bit preconditioner mechanisms",
            current_evidence=(
                f"first/second-factorial/variance certificates="
                f"{preconditioned_geometry.get('exact_conditional_first_moment_certificate_count', 0)}/"
                f"{preconditioned_geometry.get('exact_conditional_second_factorial_moment_certificate_count', 0)}/"
                f"{preconditioned_geometry.get('exact_conditional_variance_certificate_count', 0)}; density exponent change="
                f"{preconditioned_geometry.get('maximum_absolute_density_exponent_change', 'unknown')}; LLL geometry proofs="
                f"{preconditioned_geometry.get('lll_geometry_improvement_proved_count', 0)}"
            ),
            resource_status="exact theorem; no simulation or exponential table is needed for the moment identities",
            interface_status="kills count/window explanations; higher-order correlation and basis geometry remain open",
        ),
        SolverPrimitive(
            primitive_id="carry-selected-high-part-product-no-go",
            role="no-go gate for low-only carry selection followed by an ordinary high-quotient solver",
            current_evidence=(
                f"conditional product/low-selector/union-bound theorems="
                f"{carry_high_part.get('conditional_product_uniformity_theorem_count', 0)}/"
                f"{carry_high_part.get('low_only_selection_no_bias_theorem_count', 0)}/"
                f"{carry_high_part.get('polynomial_carry_union_bound_theorem_count', 0)}; joint low/high no-go="
                f"{carry_high_part.get('joint_low_high_geometry_no_go_count', 0)}"
            ),
            resource_status="exact distribution theorem; no high-state enumeration is required",
            interface_status=(
                "closes high-only quotient bias and polynomial rescue of exponentially rare events; joint low/high "
                "basis geometry and concrete generic event probabilities remain open"
            ),
        ),
        SolverPrimitive(
            primitive_id="low-fiber-fourth-moment-additive-energy",
            role="localize the first possible fixed-order residual signal",
            current_evidence=(
                f"triplewise/fourth-localization certificates="
                f"{fourth_moment.get('triplewise_independence_certificate_count', 0)}/"
                f"{fourth_moment.get('fourth_order_localization_certificate_count', 0)}; tail energy inflation="
                f"{fourth_moment.get('maximum_tail_additive_energy_inflation', 'unknown')}; relative fourth-excess bound="
                f"{fourth_moment.get('maximum_tail_fourth_excess_relative_upper_bound', 'unknown')}; source-average "
                f"fixed-fourth obstructions={fourth_moment.get('proved_source_fixed_offset_fourth_excess_vanishing_count', 0)}"
            ),
            resource_status=(
                "exact source-average fourth theorem is analytic; individual-fiber Walsh energy remains exponential "
                "without an implicit estimator"
            ),
            interface_status=(
                "orders <=3 and generic source-average order four rejected; only atypical fibers, growing order, or "
                "basis geometry remain"
            ),
        ),
        SolverPrimitive(
            primitive_id="subset-sum-smith-moment-spectrum",
            role="classify the first unresolved high-order 2-adic dependency mechanisms",
            current_evidence=(
                f"complete/sampled rows={smith_moments.get('complete_exact_census_row_count', 0)}/"
                f"{smith_moments.get('sampled_rare_event_blind_row_count', 0)}; fourth cross-checks="
                f"{smith_moments.get('fourth_moment_formula_crosscheck_count', 0)}; fixed-fifth/order>=6/growing obstructions="
                f"{smith_moments.get('proved_asymptotic_fixed_fifth_order_obstruction_count', 0)}/"
                f"{smith_moments.get('proved_asymptotic_order_at_least_six_obstruction_count', 0)}/"
                f"{smith_moments.get('proved_growing_order_obstruction_count', 0)}"
            ),
            resource_status=(
                "complete finite censuses are exact but exponential; sampled spectra are explicitly rare-event blind"
            ),
            interface_status=(
                "fixed fifth source average is closed; remaining classes require uniform counts, implicit observables, "
                "and decoder implications"
            ),
        ),
        SolverPrimitive(
            primitive_id="subset-sum-order-six-smith-transfer",
            role="exact no-go gate for generic fixed-sixth source moments",
            current_evidence=(
                f"reachable/bad states={smith_transfer.get('reachable_lattice_state_count', 0)}/"
                f"{smith_transfer.get('non_generic_terminal_state_count', 0)}; worst growth ratio="
                f"{smith_transfer.get('maximum_bad_growth_ratio', 'unknown')}; fixed-sixth obstructions="
                f"{smith_transfer.get('proved_asymptotic_fixed_sixth_order_obstruction_count', 0)}"
            ),
            resource_status="exact finite-state analytic certificate; no assignment-tuple enumeration scales with n",
            interface_status=(
                "generic fixed sixth is closed; only atypical fibers, order>=7/growing order, or non-moment geometry remain"
            ),
        ),
        SolverPrimitive(
            primitive_id="subset-sum-all-fixed-moment-obstruction",
            role="general no-go gate for generic source statistics of every fixed factorial-moment order",
            current_evidence=(
                f"instantiated/proved certificates={fixed_order_moments.get('certificate_count', 0)}/"
                f"{fixed_order_moments.get('proved_fixed_order_source_obstruction_count', 0)}; general theorem="
                f"{fixed_order_moments.get('general_all_fixed_orders_theorem_count', 0)}; growing-order obstructions="
                f"{fixed_order_moments.get('proved_growing_order_obstruction_count', 0)}"
            ),
            resource_status="analytic k-dependent finite-state theorem; constants are not uniform when k grows with n",
            interface_status=(
                "all fixed source moments closed; only charged growing order, atypical fibers, or non-moment geometry remain"
            ),
        ),
        SolverPrimitive(
            primitive_id="subset-sum-conditioned-fixed-moment-tail",
            role="no-go gate for selecting rare low fibers with fixed-order bad-tuple signal",
            current_evidence=(
                f"proved/total tail certificates={conditioned_tail.get('proved_conditioned_tail_bound_count', 0)}/"
                f"{conditioned_tail.get('certificate_count', 0)}; general theorem="
                f"{conditioned_tail.get('general_fixed_order_conditioned_tail_theorem_count', 0)}; growing/signed/basis proofs="
                f"{conditioned_tail.get('proved_growing_order_conditioned_tail_count', 0)}/"
                f"{conditioned_tail.get('proved_signed_statistic_tail_count', 0)}/"
                f"{conditioned_tail.get('proved_reduced_basis_event_tail_count', 0)}"
            ),
            resource_status="analytic tower-plus-Markov theorem; no finite fiber enumeration is evidence",
            interface_status=(
                "fixed bad-tuple fiber tails closed; growing order, signed observables, and basis events remain"
            ),
        ),
        SolverPrimitive(
            primitive_id="subset-sum-sub-half-log-moment-obstruction",
            role="uniform no-go gate for growing nonnegative moment schedules below half-logarithmic order",
            current_evidence=(
                f"sub-half-log/half-log/signed obstructions="
                f"{growing_order.get('proved_sub_half_log_growing_order_obstruction_count', 0)}/"
                f"{growing_order.get('proved_half_log_boundary_obstruction_count', 0)}/"
                f"{growing_order.get('proved_signed_statistic_obstruction_count', 0)}; finite below-one rows="
                f"{growing_order.get('finite_bound_below_one_row_count', 0)}/{growing_order.get('row_count', 0)}"
            ),
            resource_status="analytic path-count theorem charges q=2^k patterns and non-self transitions",
            interface_status=(
                "sub-half-log nonnegative moments closed; boundary/larger order, signed observables, and basis events remain"
            ),
        ),
        SolverPrimitive(
            primitive_id="subset-sum-embedding-volume-obstruction",
            role="no-go gate for determinant-only standard and logarithmic carry-sliced lattice gaps",
            current_evidence=(
                f"standard/sliced volume theorems="
                f"{embedding_volume.get('exact_standard_covolume_theorem_count', 0)}/"
                f"{embedding_volume.get('exact_carry_sliced_covolume_theorem_count', 0)}; volume obstructions="
                f"{embedding_volume.get('volume_only_asymptotic_separation_ruled_out_count', 0)}; local gaps="
                f"{embedding_volume.get('proved_local_reduced_basis_separation_count', 0)}"
            ),
            resource_status="exact determinant and Cauchy-Binet theorem; Gaussian scale is only a benchmark",
            interface_status=(
                "volume-only gaps closed; explicit local basis events, short-vector counts, and decoders remain"
            ),
        ),
        SolverPrimitive(
            primitive_id="standard-embedding-short-relation-obstruction",
            role="no-go gate for planted shortest-vector uniqueness in the standard modular embedding",
            current_evidence=(
                f"expectation/second-moment/high-probability certificates="
                f"{short_relations.get('positive_expectation_exponent_theorem_count', 0)}/"
                f"{short_relations.get('exact_second_moment_theorem_count', 0)}/"
                f"{short_relations.get('high_probability_exponential_competitor_theorem_count', 0)}; standard/carry "
                f"obstructions={short_relations.get('standard_embedding_shortest_vector_uniqueness_ruled_out_count', 0)}/"
                f"{short_relations.get('carry_sliced_short_relation_obstruction_count', 0)}"
            ),
            resource_status="exact source-distribution second moment; no Gaussian heuristic or finite LLL inference",
            interface_status=(
                "standard uniqueness closed; carry-sliced relation count and marker-aware extraction remain"
            ),
        ),
        SolverPrimitive(
            primitive_id="carry-sliced-relation-source-obstruction",
            role="no-go gate for uniform shortest-vector isolation after logarithmic low-bit slicing",
            current_evidence=(
                f"expectation/joint/inverse-poly/high-probability certificates="
                f"{carry_relations.get('positive_expectation_exponent_theorem_count', 0)}/"
                f"{carry_relations.get('pairwise_joint_probability_bound_theorem_count', 0)}/"
                f"{carry_relations.get('inverse_polynomial_source_coverage_theorem_count', 0)}/"
                f"{carry_relations.get('high_probability_source_coverage_theorem_count', 0)}; isolation obstructions="
                f"{carry_relations.get('carry_sliced_uniform_shortest_vector_isolation_ruled_out_count', 0)}"
            ),
            resource_status="analytic first/second-moment theorem with inverse-polynomial source coverage",
            interface_status=(
                "uniform carry-sliced isolation closed; source-subset separation and marker-aware extraction remain"
            ),
        ),
        SolverPrimitive(
            primitive_id="uniform-legal-boolean-coset-separation",
            role="source-correct separation between abundant kernel relations and compatible Boolean witnesses",
            current_evidence=(
                f"source/exponential-separation theorems="
                f"{boolean_coset.get('uniform_legal_source_theorem_count', 0)}/"
                f"{boolean_coset.get('fixed_beta_exponential_separation_theorem_count', 0)}; exact census failures="
                f"{boolean_coset.get('exact_pair_formula_failure_count', 0)}; tail close-pair no-go rows="
                f"{boolean_coset.get('tail_inverse_polynomial_close_pair_no_go_row_count', 0)}; marker decoders="
                f"{boolean_coset.get('marker_aware_decoder_count', 0)}"
            ),
            resource_status="exact pair counting, Paley-Zygmund source conditioning, and Hamming-ball entropy theorem",
            interface_status=(
                "short relation abundance no longer closes marker-aware decoding; polynomial affine decoder and coverage remain open"
            ),
        ),
        SolverPrimitive(
            primitive_id="marker-coset-affine-cvp-equivalence",
            role="exact interface separating easy marker normalization from hard short affine-coset search",
            current_evidence=(
                f"decomposition/gcd/radius equivalence theorems="
                f"{marker_coset.get('exact_marker_kernel_affine_coset_decomposition_count', 0)}/"
                f"{marker_coset.get('basis_marker_gcd_one_theorem_count', 0)}/"
                f"{marker_coset.get('exact_witness_radius_equivalence_theorem_count', 0)}; short decoders="
                f"{marker_coset.get('polynomial_short_marker_one_decoder_count', 0)}"
            ),
            resource_status="deterministic exact reduction under explicit polynomial-size scale choices",
            interface_status="marker filtering formalized; affine-CVP algorithm and source coverage remain open",
        ),
        SolverPrimitive(
            primitive_id="marker-aware-affine-babai-baseline",
            role="classical nearest-plane attack on standard and carry-sliced marker-one affine cosets",
            current_evidence=(
                f"trials/legal/standard/carry successes={affine_cvp.get('trial_count', 0)}/"
                f"{affine_cvp.get('legal_trial_count', 0)}/{affine_cvp.get('standard_legal_success_count', 0)}/"
                f"{affine_cvp.get('carry_sliced_legal_success_count', 0)}; coverage/scaling theorems="
                f"{affine_cvp.get('proved_uniform_inverse_polynomial_coverage_count', 0)}/"
                f"{affine_cvp.get('proved_affine_cvp_scaling_advantage_count', 0)}"
            ),
            resource_status="deterministic polynomial exact-rational nearest plane after LLL",
            interface_status="verified baseline implemented; source-conditioned BDD coverage theorem absent",
        ),
        SolverPrimitive(
            primitive_id="fixed-depth-marker-aware-cell-list",
            role="polynomial target-dependent list attack over neighboring standard and carry-sliced nearest-plane cells",
            current_evidence=(
                f"list theorem/count failures/max depth="
                f"{marker_list.get('fixed_depth_polynomial_list_theorem_count', 0)}/"
                f"{marker_list.get('candidate_count_theorem_failure_count', 0)}/"
                f"{marker_list.get('maximum_branch_depth', 0)}; depth-zero/max-depth standard="
                f"{marker_list.get('standard_depth_zero_legal_success_count', 0)}/"
                f"{marker_list.get('standard_max_depth_legal_success_count', 0)}, carry="
                f"{marker_list.get('carry_depth_zero_legal_success_count', 0)}/"
                f"{marker_list.get('carry_max_depth_legal_success_count', 0)}; coverage theorems="
                f"{marker_list.get('proved_inverse_polynomial_uniform_legal_coverage_count', 0)}; tail standard/carry/legals="
                f"{marker_list.get('tail_standard_success_count', 0)}/"
                f"{marker_list.get('tail_carry_success_count', 0)}/"
                f"{marker_list.get('tail_legal_trial_count', 0)}"
            ),
            resource_status="O(n^(k+1)) candidate vectors over all carries for each fixed branch depth k",
            interface_status="stronger verified classical baseline; source-conditioned cell-union mass remains unproved",
        ),
        SolverPrimitive(
            primitive_id="exact-marker-witness-deviation-geometry",
            role="witness-complete exact coordinate replay explaining bounded nearest-plane list membership",
            current_evidence=(
                f"complete legal/replay failures/max-n="
                f"{marker_deviations.get('complete_witness_enumeration_trial_count', 0)}/"
                f"{marker_deviations.get('exact_replay_failure_count', 0)}/"
                f"{marker_deviations.get('maximum_n_bits', 0)}; tail depth-two standard/carry="
                f"{marker_deviations.get('tail_standard_depth_two_predicted_success_count', 0)}/"
                f"{marker_deviations.get('tail_carry_depth_two_predicted_success_count', 0)} over "
                f"{marker_deviations.get('tail_complete_legal_trial_count', 0)}; tree escapes="
                f"{marker_deviations.get('tail_standard_one_step_tree_escape_count', 0)}/"
                f"{marker_deviations.get('tail_carry_one_step_tree_escape_count', 0)}; asymptotic laws="
                f"{marker_deviations.get('proved_asymptotic_deviation_growth_count', 0)}"
            ),
            resource_status="exact MITM witness enumeration and rational LLL-coordinate replay; finite diagnostic only",
            interface_status="bounded-list failure explained; source law or different decoder mechanism remains open",
        ),
        SolverPrimitive(
            primitive_id="exact-all-target-marker-list-coverage",
            role="target-noise-free legal-coverage census for fixed-depth standard and carry-sliced branch grammars",
            current_evidence=(
                f"label rows/max-n/depth={marker_all_targets.get('exact_all_target_coverage_census_count', 0)}/"
                f"{marker_all_targets.get('maximum_n_bits', 0)}/"
                f"{marker_all_targets.get('maximum_branch_depth', 0)}; assignments/legal targets="
                f"{marker_all_targets.get('exact_assignment_count', 0)}/"
                f"{marker_all_targets.get('exact_legal_target_count', 0)}; tail standard/carry="
                f"{marker_all_targets.get('tail_mean_standard_max_depth_coverage', 0)}/"
                f"{marker_all_targets.get('tail_mean_carry_max_depth_coverage', 0)}; asymptotic laws="
                f"{marker_all_targets.get('proved_asymptotic_fixed_depth_coverage_bound_count', 0)}"
            ),
            resource_status="full Boolean-cube and target census per finite label row; exponential diagnostic",
            interface_status="target sampling resolved exactly; random-label concentration and scalable decoder remain open",
        ),
        SolverPrimitive(
            primitive_id="source-native-affine-cvp-scaling",
            role="larger-n classical attack with exact meet-in-the-middle legality for failed and successful runs",
            current_evidence=(
                f"trials/max-n/tail standard/carry="
                f"{affine_cvp_scaling.get('exact_mitm_legality_trial_count', 0)}/"
                f"{affine_cvp_scaling.get('maximum_n_bits', 0)}/"
                f"{affine_cvp_scaling.get('tail_standard_success_count', 0)}/"
                f"{affine_cvp_scaling.get('tail_carry_sliced_success_count', 0)}; coverage/asymptotic theorems="
                f"{affine_cvp_scaling.get('proved_inverse_polynomial_legal_coverage_count', 0)}/"
                f"{affine_cvp_scaling.get('proved_asymptotic_affine_cvp_advantage_count', 0)}"
            ),
            resource_status="exact MITM legality plus polynomial affine Babai attack",
            interface_status="source-native scaling implemented; analytic BDD/source-coverage law absent",
        ),
        SolverPrimitive(
            primitive_id="exact-affine-babai-cell-geometry",
            role="witness-complete diagnosis of nearest-plane success via exact reduced-kernel decoding cells",
            current_evidence=(
                f"witness audits/standard/carry/tail cells="
                f"{affine_bdd.get('exact_witness_enumeration_trial_count', 0)}/"
                f"{affine_bdd.get('standard_positive_babai_cell_trial_count', 0)}/"
                f"{affine_bdd.get('carry_sliced_positive_babai_cell_trial_count', 0)}/"
                f"{affine_bdd.get('tail_standard_positive_cell_trial_count', 0)}/"
                f"{affine_bdd.get('tail_carry_sliced_positive_cell_trial_count', 0)}; source theorems="
                f"{affine_bdd.get('proved_source_bdd_coverage_count', 0)}"
            ),
            resource_status="exact MITM witnesses and exact-rational Gram-Schmidt cell tests",
            interface_status="finite mechanism diagnosed; source law for positive margin absent",
        ),
        SolverPrimitive(
            primitive_id="carry-sliced-quotient-lattice",
            role="deterministic polynomial low-carry decomposition plus constrained high-modulus LLL",
            current_evidence=(
                f"paired baseline/sliced successes={carry_slice_lattice.get('baseline_success_count', 0)}/"
                f"{carry_slice_lattice.get('carry_sliced_success_count', 0)}; tail baseline/sliced="
                f"{carry_slice_lattice.get('tail_baseline_success_count', 0)}/"
                f"{carry_slice_lattice.get('tail_carry_sliced_success_count', 0)}"
            ),
            resource_status="polynomial carry count and LLL bit complexity; no uniform coverage theorem",
            interface_status="deterministic witness verification implemented; reversible source composition open",
        ),
        SolverPrimitive(
            primitive_id="source-target-representation-law",
            role="separate independent uniform, uniform legal, and planted target multiplicity",
            current_evidence=(
                f"tail planted/legal TV="
                f"{target_distribution.get('mean_tail_planted_vs_uniform_legal_total_variation', 'unknown')}; "
                f"uniform quadratic-tail probability="
                f"{target_distribution.get('maximum_tail_uniform_target_quadratic_tail_probability', 'unknown')}; "
                f"source subfamilies={target_distribution.get('proved_inverse_polynomial_high_multiplicity_legal_subfamily_count', 0)}"
            ),
            resource_status="full finite target tables exponential; exact first two moments are theorem-certified",
            interface_status="no detectable source subfamily or polynomial representation witness algorithm",
        ),
        SolverPrimitive(
            primitive_id="full-domain-carry-algebra",
            role="symbolic low-bit constraints",
            current_evidence=(
                f"tail bounded-degree={carry.get('tail_bounded_degree_row_count', 0)}/"
                f"{carry.get('tail_carry_row_count', 0)}; maximum degree={carry.get('maximum_observed_anf_degree', 0)}"
            ),
            resource_status="bounded-degree random carry route rejected in tested scaling",
            interface_status="other symbolic representations remain open",
        ),
        SolverPrimitive(
            primitive_id="representation-dissection",
            role="many-representation collision search",
            current_evidence=(
                f"best classical exponent={resource.get('best_recorded_classical_time_exponent', 'unknown')}; deep Wagner "
                f"failures={resource.get('deep_basic_wagner_threshold_failure_count', 0)}/"
                f"{resource.get('deep_wagner_certificate_count', 0)}"
            ),
            resource_status="all recorded routes retain positive exponential exponents",
            interface_status="heuristic/randomized variants need deterministic or coherent composition",
        ),
        SolverPrimitive(
            primitive_id="quantum-fiber-walk",
            role="coherent many-target collision search",
            current_evidence=(
                f"best recorded quantum subset-sum exponent={resource.get('best_recorded_quantum_time_exponent', 'unknown')}"
            ),
            resource_status="known routes exponential; full-rank adaptive walks remain conceptually open",
            interface_status="requires new coherent Regev matching theorem",
        ),
        SolverPrimitive(
            primitive_id="average-case-decoding-reduction",
            role="transfer to coding/lattice algorithms",
            current_evidence="no model-preserving polynomial reduction with an easy target family is registered",
            resource_status="open reduction search",
            interface_status="must preserve random legal distribution, witness, and uniformity",
        ),
    ]


def synthesize_solver_hypotheses() -> list[SolverHypothesis]:
    common_obligations = [
        "Prove poly(n) time, memory, precision, and uniform preprocessing.",
        "Prove inverse-polynomial success conditioned on the primary-source legal-input distribution.",
        "Return a verified binary witness, not only distinguish or estimate a residue.",
        "Provide a deterministic interface, the proved target-independent shared-seed interface, or an algorithm-specific coherent matching theorem.",
        "Give a reversible implementation with no exponential advice, QRAM, or hidden candidate list.",
    ]
    return sorted(
        [
            SolverHypothesis(
                hypothesis_id="HYP-DCP-SS-MARKER-AWARE-AFFINE-DECODER",
                title="Marker-aware affine decoder from source-separated Boolean witness cosets",
                primitive_ids=[
                    "partial-source-contract",
                    "uniform-legal-boolean-coset-separation",
                    "marker-coset-affine-cvp-equivalence",
                    "marker-aware-affine-babai-baseline",
                    "fixed-depth-marker-aware-cell-list",
                    "exact-marker-witness-deviation-geometry",
                    "exact-all-target-marker-list-coverage",
                    "source-native-affine-cvp-scaling",
                    "exact-affine-babai-cell-geometry",
                    "standard-embedding-short-relation-obstruction",
                    "carry-sliced-relation-source-obstruction",
                    "coherent-matching-interface",
                ],
                mechanism=(
                    "Exploit the proved linear Hamming separation of valid Boolean witnesses under the uniform-legal "
                    "source to design a marker-aware affine-coset decoder whose acceptance cell ignores incompatible "
                    "marker-zero relations and returns any verified far-separated witness."
                ),
                novelty_over_tested_routes=(
                    "Abandons planted-SVP uniqueness and volume gaps. It targets the exact unresolved distinction between "
                    "short kernel vectors and Boolean-compatible affine witnesses."
                ),
                expected_upside=(
                    "A polynomial decoder with inverse-polynomial source coverage would directly satisfy the missing "
                    "density-one partial subset-sum interface and improve the DCP frontier."
                ),
                proof_obligations=common_obligations + [
                    "Define a polynomial marker-aware cell or projection computable from public labels and target.",
                    "Prove inverse-polynomial coverage over the independent uniform target conditioned legal, not a planted target.",
                    "Bound the effect of abundant incompatible marker-zero relations on the decoder's reduced basis or walk.",
                    "Use sub-half Hamming separation only to control Boolean compatibility; do not infer far-witness uniqueness.",
                    "Return and verify an explicit binary witness with polynomial time, memory, and precision.",
                ],
                first_experiments=[
                    "Derive a source-average law for the fixed-depth nearest-plane cell union already implemented, stratified by marker-zero relation projections.",
                    "Search held-out marker-weighted basis objectives and require a preregistered inverse-polynomial positive-margin tail.",
                    "Reject any gain that appears only under planted targets, postselected easy instances, or exponential witness enumeration.",
                ],
                falsifiers=[
                    "Every polynomial marker weighting has exponentially small uniform-legal positive-cell probability.",
                    "Short incompatible relations force exponentially poor Gram-Schmidt margins for every legal basis transform.",
                    "The decoder needs witness-dependent basis choices, exponential precision, or exponential candidate lists.",
                    "The apparent effect disappears when targets are sampled uniformly conditioned legal.",
                ],
                preflight_status="proposal-only-proof-debt",
                rejection_reason=None,
                priority_score=104,
            ),
            SolverHypothesis(
                hypothesis_id="REJECT-DCP-SS-BLIND-ODD-UNIT-ORBIT-LLL",
                title="Blind polynomial odd-unit orbit sampling",
                primitive_ids=[
                    "partial-source-contract",
                    "coherent-matching-interface",
                    "source-preserving-random-self-reduction",
                    "modular-lattice-embedding",
                ],
                mechanism=(
                    "Sample polynomially many odd units u modulo 2^n, apply the exact source automorphism "
                    "(A,t)->(uA,ut), and run a deterministic verified LLL extractor until one canonical embedding "
                    "presentation exposes a witness."
                ),
                novelty_over_tested_routes=(
                    "Randomizes a source-equivalent but not sign-isometric modular embedding presentation rather than "
                    "retuning a fixed embedding scale or sampling planted targets."
                ),
                expected_upside="Would be decisive if the easy-unit orbit fraction were inverse polynomial.",
                proof_obligations=common_obligations + [
                    "Prove an inverse-polynomial fraction of odd units produce a decodable reduced basis on uniform inputs.",
                    "Identify an embedding invariant or anti-concentration event that predicts LLL witness extraction.",
                    "Separate odd-unit geometry from sign-only isometric basis-presentation effects.",
                ],
                first_experiments=[
                    "Run held-out odd-unit-only sweeps beyond the observed collapse with confidence bounds against n^-1 and n^-2.",
                    "Record quotient, Gram-Schmidt, and reduced-basis features before decoding to identify a proof candidate.",
                    "Condition only on efficiently computable features and measure their unconditional source prevalence.",
                ],
                falsifiers=[
                    "Odd-unit success becomes zero with upper confidence below every preregistered inverse-polynomial target.",
                    "All rescues are reproduced by sign-only isometric controls or unstable LLL tie breaking.",
                    "The easy-unit predicate has exponentially small source-orbit measure or cannot be recognized efficiently.",
                    "A proof requires target-dependent random coins, advice, or exponentially many unit trials.",
                ],
                preflight_status="rejected-negative-result-match",
                rejection_reason=(
                    "Held-out source-uniform sweeps fit log2 success slope near -0.595 per n, reach 0/256 at n=32, "
                    "and retain no pre-reduction rule beyond n=24. Blind sampling has no surviving easy-orbit mechanism."
                ),
                priority_score=15,
            ),
            SolverHypothesis(
                hypothesis_id="HYP-DCP-SS-ODD-PART-ORBIT-CERTIFICATE",
                title="Analytic odd-part orbit certificate beyond preserved 2-adic signatures",
                primitive_ids=[
                    "partial-source-contract",
                    "coherent-matching-interface",
                    "source-preserving-random-self-reduction",
                    "modular-lattice-embedding",
                ],
                mechanism=(
                    "Derive a new odd-residue equidistribution or anti-concentration invariant over the unit orbit, prove "
                    "that an inverse-polynomial set of units satisfies it, and prove that condition forces LLL to expose a witness."
                ),
                novelty_over_tested_routes=(
                    "Targets the only degrees of freedom odd units can change after exact 2-adic valuation invariants and "
                    "blind finite feature thresholds have been exhausted."
                ),
                expected_upside=(
                    "A proved odd-part easy-orbit condition would revive the exact source-preserving polynomial solver route."
                ),
                proof_obligations=common_obligations + [
                    "Define an odd-part statistic not determined by the preserved valuation signatures.",
                    "Prove inverse-polynomial unit-orbit and unconditional source prevalence.",
                    "Prove the statistic forces a reduced-basis witness rather than merely correlating finitely with success.",
                ],
                first_experiments=[
                    "Derive symbolic residue-order or quotient anti-concentration identities before adding another feature sweep.",
                    "Evaluate a preregistered theorem-motivated statistic on n>=28 held-out units.",
                    "Abandon the route if the statistic cannot produce a uniform LLL implication."
                ],
                falsifiers=[
                    "The statistic reduces to preserved 2-adic signatures.",
                    "Its easy-unit orbit measure is exponentially small.",
                    "It predicts only post-LLL diagnostics or loses held-out enrichment in the scaling tail.",
                    "No deterministic implication from the statistic to witness extraction can be proved."
                ],
                preflight_status="proposal-only-proof-debt",
                rejection_reason=None,
                priority_score=82,
            ),
            SolverHypothesis(
                hypothesis_id="HYP-DCP-SS-TWO-ADIC-LATTICE-PRECONDITIONER",
                title="Symbolic 2-adic preconditioning that changes modular lattice geometry",
                primitive_ids=[
                    "logarithmic-low-bit-bdd",
                    "conditioned-high-bit-quotient",
                    "conditional-residual-pairwise-moment-theorem",
                    "carry-selected-high-part-product-no-go",
                    "low-fiber-fourth-moment-additive-energy",
                    "subset-sum-smith-moment-spectrum",
                    "subset-sum-order-six-smith-transfer",
                    "subset-sum-all-fixed-moment-obstruction",
                    "subset-sum-conditioned-fixed-moment-tail",
                    "subset-sum-sub-half-log-moment-obstruction",
                    "subset-sum-embedding-volume-obstruction",
                    "standard-embedding-short-relation-obstruction",
                    "carry-sliced-relation-source-obstruction",
                    "uniform-legal-boolean-coset-separation",
                    "marker-coset-affine-cvp-equivalence",
                    "marker-aware-affine-babai-baseline",
                    "source-native-affine-cvp-scaling",
                    "exact-affine-babai-cell-geometry",
                    "carry-sliced-quotient-lattice",
                    "two-adic-lift-representation",
                    "two-adic-fiber-transport",
                    "fiber-transport-graph-walk",
                    "signed-permutation-transport-no-go",
                    "affine-transport-witness-reduction",
                    "total-transport-fourier-no-go",
                    "explicit-partial-relation-coverage-no-go",
                    "target-indexed-locality-no-go",
                    "fiber-entanglement-bond-obstruction",
                    "adaptive-layout-valuation-obstruction",
                    "modular-lattice-embedding",
                ],
                mechanism=(
                    "Construct a polynomial-size exact representation of the first O(log n) lift constraints, eliminate "
                    "those carries symbolically, and embed only the quotient/high-bit residual so the planted binary vector "
                    "is separated from random short vectors."
                ),
                novelty_over_tested_routes=(
                    "Must change higher-order or reduced-basis geometry using exact low-bit structure; exact pairwise "
                    "moments now rule out candidate-count and fixed-window explanations."
                ),
                expected_upside="Could turn power-of-two arithmetic into an average-case short-vector gap absent from generic embeddings.",
                proof_obligations=common_obligations + [
                    "Bound compact preconditioner width for random labels through O(log n) lifts.",
                    "Prove quotient labels retain the exact legal-input distribution needed by matching.",
                    "Retain a genuinely joint low/high constraint or prove a concrete generic high event already has inverse-polynomial probability; low-only carry selection gives an exactly generic quotient.",
                    "Define a higher-order residual or reduced-basis statistic not determined by exact pairwise moments.",
                    "At fixed order four, prove an inverse-polynomial atypical-fiber tail and an implicit estimator/decoder despite the vanishing source average; otherwise use growing order or basis geometry explicitly.",
                    "No larger fixed order is admissible as a generic source mechanism; specify k(n) with full resource accounting or prove an atypical conditioned-fiber tail.",
                    "Prove a short-vector separation or decoding theorem after preconditioning.",
                ],
                first_experiments=[
                    "Preregister an atypical-fiber fourth-order statistic, a growing-order correlation, or an explicit LLL basis event, not a generic source-average order-four statistic, count window, or degree<=3 moment.",
                    "Feed compact fibers into alternate embeddings and compare held-out tail recovery, not training constants.",
                    "Search for analytic anti-concentration bounds on competing short vectors.",
                ],
                falsifiers=[
                    "Compact low-bit representation width is superpolynomial.",
                    "Conditioned quotients remain generic for every preregistered geometry statistic.",
                    "Conditioning destroys uniform legal-input coverage or leaves standard LLL geometry unchanged.",
                    "Tail recovery remains exponentially decaying after preregistered scaling.",
                ],
                preflight_status="proposal-only-proof-debt",
                rejection_reason=None,
                priority_score=100,
            ),
            SolverHypothesis(
                hypothesis_id="HYP-DCP-SS-COHERENT-PARTIAL-SOLVER-BRIDGE",
                title="Polynomial purified quantum relation solver under the symmetric matching lift",
                primitive_ids=[
                    "partial-source-contract",
                    "coherent-matching-interface",
                    "quantum-relation-fidelity",
                    "symmetric-quantum-relation-lift",
                    "source-audited-quantum-walk",
                    "two-adic-fiber-transport",
                    "fiber-transport-graph-walk",
                    "signed-permutation-transport-no-go",
                    "affine-transport-witness-reduction",
                    "total-transport-fourier-no-go",
                    "explicit-partial-relation-coverage-no-go",
                    "target-indexed-locality-no-go",
                    "fiber-entanglement-bond-obstruction",
                    "adaptive-layout-valuation-obstruction",
                    "quantum-fiber-walk",
                    "representation-dissection",
                ],
                mechanism=(
                    "Construct a polynomial purified circuit whose measured valid binary-witness output has inverse-polynomial "
                    "mean probability on the exact density-one source; feed it through fixed-order double endpoint "
                    "evaluation and the proved weighted matching transfer."
                ),
                novelty_over_tested_routes=(
                    "Deterministic selection, shared classical coins, and native one-call workspace overlap are no longer "
                    "required. The remaining problem is the substantive one: obtaining polynomial quantum relation success."
                ),
                expected_upside=(
                    "A polynomial relation solver would now transfer to DCP with a conservative seventh-power success loss, "
                    "opening the lattice route without first canonicalizing every witness."
                ),
                proof_obligations=common_obligations + [
                    "State a polynomial-size purified relation circuit with an efficiently verifiable binary witness register.",
                    "Show that valid outputs have linear support beyond the target-indexed locality threshold.",
                    "If tensor preparation is used, leave the fixed polynomial balanced-layout class or prove a valid partial-instance source-coverage theorem.",
                    "Prove inverse-polynomial global mean valid-output probability on Regev's exact random legal-input source.",
                    "Instantiate fixed-order double evaluation and charge the global seventh-power matching loss.",
                    "Retain the product-mixture contamination lower bound and compose approximation errors through all reflection bits.",
                ],
                first_experiments=[
                    "Search source-audited walk/dissection primitives for a polynomial-time valid-output relation subroutine.",
                    "Estimate target-success weight distributions and attack any apparent mean with classical algorithms.",
                    "Mechanize source-distribution, weighted-matching, and product-contamination constants end to end.",
                ],
                falsifiers=[
                    "Every purified relation mechanism has exponentially small mean valid-output probability.",
                    "Amplification, relation verification, or memory remains exponential.",
                    "Known quantum subset-sum walks remain exponential after complete composition.",
                    "Bad-register contamination destroys the paired state faster than the seventh-power signal survives.",
                ],
                preflight_status="proposal-only-proof-debt",
                rejection_reason=None,
                priority_score=94,
            ),
            SolverHypothesis(
                hypothesis_id="HYP-DCP-SS-NONGENERIC-REPRESENTATION-COLLAPSE",
                title="Non-generic representation multiplicity on the legal matching distribution",
                primitive_ids=[
                    "partial-source-contract",
                    "source-target-representation-law",
                    "representation-dissection",
                ],
                mechanism=(
                    "Test whether Regev's legal target distribution, unlike an unconditional random target, has a hidden "
                    "many-representation bias that permits aggressive list filtering with polynomial retained mass."
                ),
                novelty_over_tested_routes="Questions random-list genericity on the exact conditioned legal distribution instead of optimizing a known exponent.",
                expected_upside="A provable representation explosion specific to legal matching inputs could invalidate generic subset-sum exponents.",
                proof_obligations=common_obligations + [
                    "Derive the exact legal target distribution from the primary source.",
                    "Prove representation multiplicity concentration and polynomial filter survival.",
                    "Exclude size-biased planted-target sampling artifacts.",
                ],
                first_experiments=[
                    "Extend exact source-target factorial moments or contiguity bounds beyond the implemented second moment.",
                    "Measure representation-count likelihood ratios under preregistered coefficient alphabets.",
                    "Attempt a second-moment theorem for any persistent legal-distribution bias.",
                ],
                falsifiers=[
                    "Legal conditioning is asymptotically contiguous with generic random targets for all tested statistics.",
                    "Any representation gain is only constant/exponential-exponent improvement, not exponent collapse.",
                    "The effect appears only under size-biased planted witnesses.",
                ],
                preflight_status="proposal-only-proof-debt",
                rejection_reason=None,
                priority_score=94,
            ),
            SolverHypothesis(
                hypothesis_id="HYP-DCP-SS-DECODING-REDUCTION",
                title="Average-case reduction to a polynomially decodable structured code ensemble",
                primitive_ids=["average-case-decoding-reduction", "partial-source-contract"],
                mechanism=(
                    "Encode modular subset-sum witnesses as errors in a structured code whose syndrome distribution "
                    "preserves random legal instances, then use a uniform polynomial decoder on an inverse-polynomial subfamily."
                ),
                novelty_over_tested_routes="Searches a model-preserving algorithmic reduction instead of an analogy to LPN, LWE, or decoding.",
                expected_upside="Could import mature coding-theory decoders and expose an unrecognized easy legal subdistribution.",
                proof_obligations=common_obligations + [
                    "Specify reduction direction, syndrome distribution, rate, weight, and parameter blowup.",
                    "Prove the target decoder's success on the induced distribution without nonuniform code advice.",
                    "Map decoded errors back to verified binary modular witnesses.",
                ],
                first_experiments=[
                    "Generate exact small-n syndrome ensembles for BCH, alternant, quasi-cyclic, and rank-metric targets.",
                    "Measure statistical distance from each decoder's proved easy distribution.",
                    "Reject any family requiring hidden structure not computable from public labels.",
                ],
                falsifiers=[
                    "The induced code is generic random linear decoding at hard parameters.",
                    "Structure needed by the decoder is absent or leaks exponential advice.",
                    "Coverage vanishes after preserving the source distribution and witness map.",
                ],
                preflight_status="proposal-only-proof-debt",
                rejection_reason=None,
                priority_score=90,
            ),
            SolverHypothesis(
                hypothesis_id="REJECT-DCP-SS-LLL-CONSTANT-RETUNE",
                title="Retune centered LLL scales and deltas",
                primitive_ids=["modular-lattice-embedding"],
                mechanism="Sweep more embedding constants without changing short-vector geometry.",
                novelty_over_tested_routes="None.",
                expected_upside="Low.",
                proof_obligations=common_obligations,
                first_experiments=[],
                falsifiers=["Existing tail collapse and absent coverage theorem."],
                preflight_status="rejected-negative-result-match",
                rejection_reason="The tested LLL family already shows finite success with tail collapse; constant retuning adds no asymptotic mechanism.",
                priority_score=0,
            ),
            SolverHypothesis(
                hypothesis_id="REJECT-DCP-SS-BOUNDED-DEGREE-CARRY",
                title="Solve all carries as a bounded-degree ANF system",
                primitive_ids=["full-domain-carry-algebra"],
                mechanism="Assume every high carry has constant algebraic degree.",
                novelty_over_tested_routes="None; contradicted by full-domain audit.",
                expected_upside="Invalid as stated.",
                proof_obligations=common_obligations,
                first_experiments=[],
                falsifiers=["No high-bit bounded-degree rows in the live full-domain tail audit."],
                preflight_status="rejected-negative-result-match",
                rejection_reason="Exact full-domain ANF degree grows with n in the tested random family.",
                priority_score=0,
            ),
            SolverHypothesis(
                hypothesis_id="REJECT-DCP-SS-BASIC-DEEP-WAGNER",
                title="Apply a deeper basic Wagner tree to disjoint binary blocks",
                primitive_ids=["representation-dissection"],
                mechanism="Increase list count without representation expansion.",
                novelty_over_tested_routes="None.",
                expected_upside="Invalid under the audited random-list threshold.",
                proof_obligations=common_obligations,
                first_experiments=[],
                falsifiers=["Every live k>=4 density-one certificate lacks basic leaf-list volume."],
                preflight_status="rejected-negative-result-match",
                rejection_reason="Basic deeper trees require representation expansion; known expanded routes remain exponential.",
                priority_score=0,
            ),
            SolverHypothesis(
                hypothesis_id="REJECT-DCP-SS-KNOWN-QUANTUM-EXPONENT",
                title="Insert the known 0.218-exponent quantum subset-sum algorithm",
                primitive_ids=["quantum-fiber-walk"],
                mechanism="Use an existing exponential quantum subset-sum walk as the matching subroutine.",
                novelty_over_tested_routes="None.",
                expected_upside="Does not meet polynomial DCP complexity.",
                proof_obligations=common_obligations,
                first_experiments=[],
                falsifiers=["Positive exponential time exponent and interface mismatch."],
                preflight_status="rejected-resource-contract",
                rejection_reason="2^(0.218n) remains exponential in n=log2 N and is not a deterministic drop-in solver.",
                priority_score=0,
            ),
        ],
        key=lambda item: (-item.priority_score, item.hypothesis_id),
    )


def run_subset_sum_solver_synthesis() -> DCPSubsetSumSolverSynthesisReport:
    primitives = build_solver_primitives()
    hypotheses = synthesize_solver_hypotheses()
    survivors = [item for item in hypotheses if item.preflight_status == "proposal-only-proof-debt"]
    rejected = [item for item in hypotheses if item.preflight_status.startswith("rejected")]
    metrics: dict[str, int | float] = {
        "primitive_count": len(primitives),
        "hypothesis_count": len(hypotheses),
        "proposal_only_survivor_count": len(survivors),
        "negative_match_rejection_count": len(rejected),
        "accepted_candidate_count": 0,
        "source_contract_satisfying_hypothesis_count": 0,
        "maximum_survivor_priority_score": max(item.priority_score for item in survivors),
    }
    return DCPSubsetSumSolverSynthesisReport(
        created_at=utc_now(),
        source_contract={
            "time": "poly(n)",
            "coverage": "inverse-polynomial conditioned on legal random density-one inputs",
            "output": "verified binary witness",
            "interface": "deterministic consistent solver or separately proved coherent replacement",
            "promotion": "no proposal becomes a CandidateRecord until every obligation is supported by a theorem artifact",
        },
        primitives=primitives,
        hypotheses=hypotheses,
        headline_metrics=metrics,
        claim_gate={
            "negative_results_used_as_rejection_filters": True,
            "source_interface_attached_to_every_survivor": True,
            "proposal_is_algorithmic_evidence": False,
            "candidate_records_accepted": False,
            "speedup_claim_allowed": False,
            "reason": "The grammar identifies high-variance research programs, but none supplies a polynomial coverage or interface theorem.",
        },
        status="typed-solver-hypotheses-generated-all-proof-gated",
        summary=(
            f"Generated {len(hypotheses)} typed partial-solver hypotheses from {len(primitives)} primitives; "
            f"{len(survivors)} survive only as proof-debt proposals, {len(rejected)} match existing negative/resource gates, "
            "and zero enter the candidate registry."
        ),
        falsifiers_triggered=[
            "LLL constant retuning is rejected after tail collapse.",
            "Bounded-degree carry solving is rejected by full-domain ANF growth.",
            "Basic deep Wagner trees are rejected by density-one list-volume accounting.",
            "Known positive quantum subset-sum exponents are rejected as non-polynomial and interface-incompatible.",
            "Surviving hybrids remain proposals until uniform coverage, complexity, witness, and reversibility theorems exist.",
        ],
    )


def write_subset_sum_solver_synthesis(
    path: Path = DCP_SUBSET_SUM_SOLVER_SYNTHESIS_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_subset_sum_solver_synthesis()
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-SOLVER-SYNTHESIS-WEAK-MUTATIONS",
                source=str(path),
                claim="LLL retuning, bounded-degree carries, basic deep Wagner trees, or known quantum exponents are new polynomial partial-solver candidates.",
                reason_invalid="Each route matches a live negative result or retains a positive exponential resource exponent.",
                lesson="Generate hybrids only when they change geometry, distributions, or theorem interfaces and attach uniform proof obligations before candidate promotion.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "negative_match_rejection_count": payload["headline_metrics"]["negative_match_rejection_count"],
                    "proposal_only_survivor_count": payload["headline_metrics"]["proposal_only_survivor_count"],
                    "accepted_candidate_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-SOLVER-SYNTHESIS"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_subset_sum_solver_synthesis": str(path)},
            )
        )
    return payload
