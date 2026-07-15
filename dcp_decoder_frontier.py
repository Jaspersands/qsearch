"""Named resource frontier for state-native DCP decoding approaches."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import ExperimentResultRecord, upsert_experiment_result, utc_now


DCP_DECODER_FRONTIER_PATH = Path("research/phase_workbench/dcp_decoder_frontier.json")
RANDOM_DESIGN_PATH = Path("research/classical_baselines/dcp_random_design_decoder.json")
CLIFFORD_PATH = Path("research/phase_workbench/dcp_clifford_witness_search.json")
BAD_REGISTER_PATH = Path("research/phase_workbench/dcp_bad_register_audit.json")
HIDDEN_NUMBER_BRIDGE_PATH = Path("research/reductions/dcp_hidden_number_bridge.json")
SPARSE_FOURIER_AUDIT_PATH = Path("research/classical_baselines/dcp_sparse_fourier_transfer_audit.json")
IID_HASH_ESTIMATOR_PATH = Path("research/classical_baselines/dcp_iid_hash_estimator_audit.json")
BIASED_LINEAR_MARGIN_PATH = Path("research/classical_baselines/dcp_biased_linear_margin_audit.json")
MULTIRECORD_HIERARCHY_PATH = Path("research/classical_baselines/dcp_multirecord_estimator_hierarchy.json")
USTATISTIC_VARIANCE_PATH = Path("research/classical_baselines/dcp_ustatistic_variance_audit.json")
FACTORIZED_CONTRACTION_PATH = Path("research/classical_baselines/dcp_factorized_contraction_audit.json")
LOW_RANK_CONTRACTION_PATH = Path("research/classical_baselines/dcp_low_rank_contraction_search.json")
SUBSET_SUM_MEASUREMENT_PATH = Path("research/phase_workbench/dcp_subset_sum_measurement_audit.json")
FIBER_ENTANGLEMENT_PATH = Path("research/phase_workbench/dcp_fiber_entanglement.json")
ADAPTIVE_LAYOUT_PATH = Path("research/phase_workbench/dcp_adaptive_layout_audit.json")
HASHED_FIBER_MEASUREMENT_PATH = Path("research/phase_workbench/dcp_hashed_fiber_measurement_audit.json")
REFERENCE_PROJECTION_PATH = Path("research/phase_workbench/dcp_reference_projection_audit.json")
COVARIANT_PGM_PATH = Path("research/phase_workbench/dcp_covariant_pgm_audit.json")
CONTAMINATED_PGM_PATH = Path("research/phase_workbench/dcp_contaminated_pgm_audit.json")
SUBSET_SUM_BRIDGE_PATH = Path("research/reductions/dcp_subset_sum_bridge.json")
SUBSET_SUM_LATTICE_PATH = Path("research/classical_baselines/dcp_subset_sum_lattice_search.json")
SUBSET_SUM_TWO_ADIC_PATH = Path("research/classical_baselines/dcp_subset_sum_two_adic_search.json")
SUBSET_SUM_RESOURCE_FRONTIER_PATH = Path("research/classical_baselines/dcp_subset_sum_resource_frontier.json")
SUBSET_SUM_CARRY_ANF_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_anf.json")
SUBSET_SUM_LOW_BIT_BDD_PATH = Path("research/classical_baselines/dcp_subset_sum_low_bit_bdd.json")
SUBSET_SUM_CONDITIONED_QUOTIENT_PATH = Path("research/classical_baselines/dcp_subset_sum_conditioned_quotient.json")
SUBSET_SUM_CARRY_SLICE_LATTICE_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_slice_lattice.json")
SUBSET_SUM_TARGET_DISTRIBUTION_PATH = Path("research/classical_baselines/dcp_subset_sum_target_distribution.json")
COHERENT_MATCHING_INTERFACE_PATH = Path("research/reductions/dcp_coherent_matching_interface.json")
RANDOM_SELF_REDUCTION_PATH = Path("research/reductions/dcp_subset_sum_random_self_reduction.json")
ODD_UNIT_ORBIT_GEOMETRY_PATH = Path("research/classical_baselines/dcp_odd_unit_orbit_geometry.json")
LIKELIHOOD_BRANCH_BOUND_PATH = Path("research/classical_baselines/dcp_likelihood_branch_bound.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-DECODER-FRONTIER"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class DecoderFrontierRow:
    method_id: str
    access_model: str
    access_legal_for_regev_dcp: bool
    state_sample_class: str
    time_class: str
    memory_class: str
    decoder_status: str
    exact_f1_robustness: str
    lattice_composition_status: str
    dominated_by: list[str]
    blocking_reason: str
    source_ids: list[str]


@dataclass(frozen=True)
class DCPDecoderFrontierReport:
    created_at: str
    parameter: str
    rows: list[DecoderFrontierRow]
    headline_metrics: dict[str, int]
    target_contract: dict[str, str]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def build_decoder_frontier() -> DCPDecoderFrontierReport:
    random_design = _read_json(RANDOM_DESIGN_PATH)
    clifford = _read_json(CLIFFORD_PATH)
    bad_register = _read_json(BAD_REGISTER_PATH)
    bridge = _read_json(HIDDEN_NUMBER_BRIDGE_PATH)
    sparse_fourier = _read_json(SPARSE_FOURIER_AUDIT_PATH)
    iid_hash = _read_json(IID_HASH_ESTIMATOR_PATH)
    biased_linear = _read_json(BIASED_LINEAR_MARGIN_PATH)
    multirecord = _read_json(MULTIRECORD_HIERARCHY_PATH)
    ustatistic = _read_json(USTATISTIC_VARIANCE_PATH)
    factorized = _read_json(FACTORIZED_CONTRACTION_PATH)
    low_rank = _read_json(LOW_RANK_CONTRACTION_PATH)
    subset_sum_measurement = _read_json(SUBSET_SUM_MEASUREMENT_PATH)
    fiber_entanglement = _read_json(FIBER_ENTANGLEMENT_PATH)
    adaptive_layout = _read_json(ADAPTIVE_LAYOUT_PATH)
    hashed_fiber_measurement = _read_json(HASHED_FIBER_MEASUREMENT_PATH)
    reference_projection = _read_json(REFERENCE_PROJECTION_PATH)
    covariant_pgm = _read_json(COVARIANT_PGM_PATH)
    contaminated_pgm = _read_json(CONTAMINATED_PGM_PATH)
    subset_sum_bridge = _read_json(SUBSET_SUM_BRIDGE_PATH)
    subset_sum_lattice = _read_json(SUBSET_SUM_LATTICE_PATH)
    subset_sum_two_adic = _read_json(SUBSET_SUM_TWO_ADIC_PATH)
    subset_sum_resource = _read_json(SUBSET_SUM_RESOURCE_FRONTIER_PATH)
    subset_sum_carry = _read_json(SUBSET_SUM_CARRY_ANF_PATH)
    subset_sum_low_bit = _read_json(SUBSET_SUM_LOW_BIT_BDD_PATH)
    subset_sum_conditioned_quotient = _read_json(SUBSET_SUM_CONDITIONED_QUOTIENT_PATH)
    subset_sum_carry_slice_lattice = _read_json(SUBSET_SUM_CARRY_SLICE_LATTICE_PATH)
    subset_sum_target_distribution = _read_json(SUBSET_SUM_TARGET_DISTRIBUTION_PATH)
    coherent_matching = _read_json(COHERENT_MATCHING_INTERFACE_PATH)
    random_self_reduction = _read_json(RANDOM_SELF_REDUCTION_PATH)
    odd_unit_geometry = _read_json(ODD_UNIT_ORBIT_GEOMETRY_PATH)
    likelihood = _read_json(LIKELIHOOD_BRANCH_BOUND_PATH)
    random_metrics = random_design.get("headline_metrics", {})
    clifford_metrics = clifford.get("headline_metrics", {})
    bad_metrics = bad_register.get("headline_metrics", {})
    bridge_metrics = bridge.get("headline_metrics", {})
    sparse_metrics = sparse_fourier.get("headline_metrics", {})
    iid_hash_metrics = iid_hash.get("headline_metrics", {})
    biased_linear_metrics = biased_linear.get("headline_metrics", {})
    multirecord_metrics = multirecord.get("headline_metrics", {})
    ustatistic_metrics = ustatistic.get("headline_metrics", {})
    factorized_metrics = factorized.get("headline_metrics", {})
    low_rank_metrics = low_rank.get("headline_metrics", {})
    subset_sum_metrics = subset_sum_measurement.get("headline_metrics", {})
    fiber_entanglement_metrics = fiber_entanglement.get("headline_metrics", {})
    adaptive_layout_metrics = adaptive_layout.get("headline_metrics", {})
    hashed_fiber_metrics = hashed_fiber_measurement.get("headline_metrics", {})
    reference_projection_metrics = reference_projection.get("headline_metrics", {})
    covariant_pgm_metrics = covariant_pgm.get("headline_metrics", {})
    contaminated_pgm_metrics = contaminated_pgm.get("headline_metrics", {})
    subset_sum_bridge_metrics = subset_sum_bridge.get("headline_metrics", {})
    subset_sum_lattice_metrics = subset_sum_lattice.get("headline_metrics", {})
    subset_sum_two_adic_metrics = subset_sum_two_adic.get("headline_metrics", {})
    subset_sum_resource_metrics = subset_sum_resource.get("headline_metrics", {})
    subset_sum_carry_metrics = subset_sum_carry.get("headline_metrics", {})
    subset_sum_low_bit_metrics = subset_sum_low_bit.get("headline_metrics", {})
    subset_sum_conditioned_quotient_metrics = subset_sum_conditioned_quotient.get("headline_metrics", {})
    subset_sum_carry_slice_metrics = subset_sum_carry_slice_lattice.get("headline_metrics", {})
    subset_sum_target_distribution_metrics = subset_sum_target_distribution.get("headline_metrics", {})
    coherent_matching_metrics = coherent_matching.get("headline_metrics", {})
    random_self_reduction_metrics = random_self_reduction.get("headline_metrics", {})
    odd_unit_geometry_metrics = odd_unit_geometry.get("headline_metrics", {})
    likelihood_metrics = likelihood.get("headline_metrics", {})
    rows = [
        DecoderFrontierRow(
            method_id="local-quadrature-full-fft",
            access_model="random public DCP labels; independent X/Y measurements; classical length-N FFT",
            access_legal_for_regev_dcp=True,
            state_sample_class="poly(n) observed empirically",
            time_class="Theta(N log N)=2^(Theta(n))",
            memory_class="Theta(N)=2^(Theta(n))",
            decoder_status=f"finite FFT recoveries={random_metrics.get('fft_success_count', 'unknown')}",
            exact_f1_robustness=(
                "sample-level exhaustive-correlation theorem proved="
                f"{bridge_metrics.get('proved_exact_f1_sample_robustness_count', 'unknown')}; decoder remains exponential"
            ),
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason="Exponential time and memory in n=log2(N).",
            source_ids=["dcp_random_design_decoder.py"],
        ),
        DecoderFrontierRow(
            method_id="grover-likelihood-search",
            access_model="coherent search over N candidate reflections using a score oracle built from measured records",
            access_legal_for_regev_dcp=False,
            state_sample_class="poly(n) classical measurement records",
            time_class="Omega(sqrt(N)) score evaluations=2^(Theta(n))",
            memory_class="poly(n) only with nontrivial coherent record access",
            decoder_status="conceptual baseline only",
            exact_f1_robustness="not established",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason="Still exponential in n and assumes a coherent likelihood oracle not supplied by DCP.",
            source_ids=["Grover maximum-finding baseline", "dcp_random_design_decoder.py"],
        ),
        DecoderFrontierRow(
            method_id="kuperberg-generic-sieve",
            access_model="independent random-label DCP phase states",
            access_legal_for_regev_dcp=True,
            state_sample_class="2^O(sqrt(n))",
            time_class="2^O(sqrt(n))",
            memory_class="2^O(sqrt(n))",
            decoder_status="known generic subexponential DHSP baseline",
            exact_f1_robustness=(
                "not established in this repository; exact audit robustness proofs="
                f"{bad_metrics.get('proved_bad_register_robustness_count', 'unknown')}"
            ),
            lattice_composition_status="blocked on exact f=1 implementation contract",
            dominated_by=[],
            blocking_reason="Subexponential rather than polynomial and current implementation lacks exact bad-register proof.",
            source_ids=["kuperberg-dhsp-2003", "dcp_sample_workbench.py", "dcp_bad_register_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="regev-polynomial-space-sieve",
            access_model="independent random-label DCP phase states with polynomial-space collimation",
            access_legal_for_regev_dcp=True,
            state_sample_class="2^O(sqrt(n log n))",
            time_class="2^O(sqrt(n log n))",
            memory_class="poly(n) quantum space",
            decoder_status="known polynomial-space generic baseline",
            exact_f1_robustness="not established by current executable workbench",
            lattice_composition_status="source reduction known; executable decoder contract blocked",
            dominated_by=[],
            blocking_reason="Subexponential time and no current end-to-end f=1 decoder certificate.",
            source_ids=["regev-lattice-dhsp-2003", "dcp_bad_register_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="chosen-label-phase-estimation",
            access_model="chosen/repeated Fourier labels and adaptive quadrature tomography",
            access_legal_for_regev_dcp=False,
            state_sample_class="poly(n) under the stronger oracle",
            time_class="poly(n) under the stronger oracle",
            memory_class="poly(n)",
            decoder_status="illegal oracle comparator",
            exact_f1_robustness="irrelevant under access mismatch",
            lattice_composition_status="invalid interface",
            dominated_by=[],
            blocking_reason="Regev DCP supplies random labels; chosen and repeated labels cannot be requested.",
            source_ids=["query_model_ledger.py", "dcp_random_design_decoder.py"],
        ),
        DecoderFrontierRow(
            method_id="global-clifford-hamming-decoder",
            access_model="random public labels; public CZ-plus-Hadamard circuit; Hamming-weight decision",
            access_legal_for_regev_dcp=True,
            state_sample_class="finite poly(n) batches plus inverse-bias repetition",
            time_class="poly(n) per circuit and decision; repetition unresolved",
            memory_class="poly(n) circuit execution",
            decoder_status=(
                "finite log2 Hamming-TV slope="
                f"{clifford_metrics.get('finite_log2_hamming_tv_slope_per_n', 'unknown')}"
            ),
            exact_f1_robustness="one-bad finite audit only",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve"],
            blocking_reason="Efficient statistic decays in finite scaling and does not recover the reflection.",
            source_ids=["dcp_clifford_witness_search.py", "dcp_clifford_contamination.py"],
        ),
        DecoderFrontierRow(
            method_id="structured-query-sparse-fft",
            access_model="HashToBins or significant-Fourier measurements at selected shifted, filtered, and correlated locations",
            access_legal_for_regev_dcp=False,
            state_sample_class="poly(n) only under structured query access",
            time_class="poly(n) only under structured query access",
            memory_class="poly(n) only under structured query access",
            decoder_status=(
                "direct transfer proofs="
                f"{sparse_metrics.get('proved_sparse_fft_transfer_count', 'unknown')}; access-invalid methods="
                f"{sparse_metrics.get('direct_access_invalid_count', 'unknown')}"
            ),
            exact_f1_robustness="irrelevant until random-label access is preserved",
            lattice_composition_status="invalid interface",
            dominated_by=[],
            blocking_reason="The joint query schedule is not iid and cannot be requested from DCP.",
            source_ids=["arxiv:1604.00845", "arxiv:1607.01842", "dcp_sparse_fourier_transfer_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="iid-exact-linear-hash-buckets",
            access_model="iid random-label local measurements; one-pass exact unbiased linear bucket statistics",
            access_legal_for_regev_dcp=True,
            state_sample_class="2^Theta(n) for B=poly(n) coarse buckets",
            time_class="2^(Theta(n)) sample processing or exponentially many fine buckets",
            memory_class="poly(n) per bucket but no joint-polynomial sample/enumeration row",
            decoder_status=(
                "restricted Parseval no-go proofs="
                f"{iid_hash_metrics.get('proved_exact_linear_estimator_no_go_count', 'unknown')}; joint-poly rows="
                f"{iid_hash_metrics.get('joint_polynomial_resource_row_count', 'unknown')}"
            ),
            exact_f1_robustness="observation channel included; no decoder",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason="Parseval forces exponential samples for coarse buckets or exponentially many fine buckets.",
            source_ids=["dcp_iid_hash_estimator_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="iid-biased-linear-margin-buckets",
            access_model="iid random-label local measurements; one biased linear score with a uniform decision margin",
            access_legal_for_regev_dcp=True,
            state_sample_class="2^Theta(n) for B=poly(n) coarse buckets under the uniform MSE contract",
            time_class="2^(Theta(n)) sample processing or exponentially many fine bucket scores",
            memory_class="poly(n) per score but no joint-polynomial sample/enumeration row",
            decoder_status=(
                "restricted margin no-go proofs="
                f"{biased_linear_metrics.get('proved_uniform_margin_linear_no_go_count', 'unknown')}; joint-poly rows="
                f"{biased_linear_metrics.get('joint_polynomial_resource_row_count', 'unknown')}"
            ),
            exact_f1_robustness="observation channel included; no decoder",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason=(
                "Bias and smoothing do not remove the Parseval sample/enumeration tradeoff for a uniformly "
                "margin-separated one-score empirical mean."
            ),
            source_ids=["dcp_biased_linear_margin_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="iid-disjoint-multirecord-product-kernels",
            access_model="iid random-label local measurements grouped into disjoint fixed-degree signed-product blocks",
            access_legal_for_regev_dcp=True,
            state_sample_class="2^Theta(n) for coarse polynomial bucket counts under the uniform margin/MSE contract",
            time_class="2^Theta(n) sample processing; degree r worsens the certified block second moment by 4^r",
            memory_class="poly(n) per kernel; no joint-polynomial sample/enumeration row",
            decoder_status=(
                "restricted disjoint-block no-go proofs="
                f"{multirecord_metrics.get('proved_disjoint_block_multilinear_no_go_count', 'unknown')}; overlapping "
                f"U-statistic lower bounds={multirecord_metrics.get('proved_overlapping_ustatistic_lower_bound_count', 'unknown')}"
            ),
            exact_f1_robustness="observation channel included; no decoder",
            lattice_composition_status="blocked",
            dominated_by=["iid-biased-linear-margin-buckets", "kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason=(
                "Signed aggregate labels remain uniform, conditional Jensen retains response energy, and product outcomes "
                "add a 4^r second moment. Overlapping U-statistics are outside this row."
            ),
            source_ids=["dcp_multirecord_estimator_hierarchy.py"],
        ),
        DecoderFrontierRow(
            method_id="iid-explicit-overlapping-product-ustatistics",
            access_model="iid random-label records; one symmetric signed-product kernel averaged over all r-subsets",
            access_legal_for_regev_dcp=True,
            state_sample_class="2^Omega(n/r) records at fixed degree; records can be polynomial at growing degree",
            time_class="2^Omega(n) explicit tuple terms for coarse polynomial bucket counts",
            memory_class="potentially polynomial streaming memory, but explicit arithmetic remains exponential",
            decoder_status=(
                "restricted Hoeffding variance proofs="
                f"{ustatistic_metrics.get('proved_overlapping_ustatistic_variance_bound_count', 'unknown')}; joint-poly "
                f"explicit rows={ustatistic_metrics.get('joint_polynomial_explicit_resource_row_count', 'unknown')}"
            ),
            exact_f1_robustness="observation channel included; no decoder",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason=(
                "Hoeffding decomposition forces exponentially many records at fixed degree or explicitly evaluated "
                "tuples at growing degree. Polynomial implicit contractions remain outside this row."
            ),
            source_ids=["dcp_ustatistic_variance_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="iid-rank-one-elementary-symmetric-contraction",
            access_model="iid random-label records; scalar rank-one product kernel contracted in O(mr)",
            access_legal_for_regev_dcp=True,
            state_sample_class="Omega(r^2 N/B) for B equal buckets under the uniform margin/MSE contract",
            time_class="O(mr) contraction but exponential because the required m is exponential for B=poly(n)",
            memory_class="O(r) contraction state plus input records",
            decoder_status=(
                "restricted rank-one no-go proofs="
                f"{factorized_metrics.get('proved_rank_one_implicit_contraction_no_go_count', 'unknown')}; joint-poly "
                f"rows={factorized_metrics.get('joint_polynomial_resource_row_count', 'unknown')}"
            ),
            exact_f1_robustness="observation channel included; no decoder",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason=(
                "Elementary-symmetric contraction removes tuple enumeration but the first Hoeffding projection forces "
                "exponential records. Polynomial-rank and low-bond kernels remain outside this row."
            ),
            source_ids=["dcp_factorized_contraction_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="iid-tested-polynomial-rank-contractions",
            access_model="iid random labels; polynomial-rank cosine/Fejer/hybrid product-kernel sums",
            access_legal_for_regev_dcp=True,
            state_sample_class="superpolynomial in every finite uniformly separating row under exact covariance",
            time_class="O(BRrm), superpolynomial because fitted m is superpolynomial",
            memory_class="polynomial rank and contraction state; analysis grid is not used at runtime",
            decoder_status=(
                f"uniform finite separators={low_rank_metrics.get('uniform_separation_row_count', 'unknown')}; "
                f"finite joint-poly survivors={low_rank_metrics.get('joint_polynomial_finite_survivor_count', 'unknown')}; "
                f"proved uniform families={low_rank_metrics.get('proved_uniform_low_rank_family_count', 'unknown')}"
            ),
            exact_f1_robustness="not reached; no polynomial clean-channel decoder",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason=(
                "Exact all-order cross-component covariance makes every tested uniform separator sample-superpolynomial. "
                "Only a genuinely new cancellation/tensor mechanism can reopen this class."
            ),
            source_ids=["dcp_low_rank_contraction_search.py"],
        ),
        DecoderFrontierRow(
            method_id="collective-compute-subset-sum-qft",
            access_model="collective phase qubits; reversible public-label subset sum and ancilla QFT",
            access_legal_for_regev_dcp=True,
            state_sample_class="poly(n)",
            time_class="polynomial circuit",
            memory_class="m input qubits plus n-qubit sum register",
            decoder_status=(
                f"exact QFT signal instances={subset_sum_metrics.get('compute_qft_signal_instance_count', 'unknown')}; "
                f"uniformity failures={subset_sum_metrics.get('qft_uniformity_failure_count', 'unknown')}"
            ),
            exact_f1_robustness="irrelevant because the clean architecture has zero signal",
            lattice_composition_status="blocked",
            dominated_by=["no-information"],
            blocking_reason="Orthogonal which-subset garbage makes the sum-register QFT output exactly uniform.",
            source_ids=["dcp_subset_sum_measurement_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="collective-exact-residue-mps",
            access_model="collective phase qubits; sequential exact residue-tracking tensor network",
            access_legal_for_regev_dcp=True,
            state_sample_class="poly(n)",
            time_class="exponential exact bond contraction with high probability",
            memory_class="2^Omega(n) exact residue bond dimension on random labels",
            decoder_status=(
                "high-probability exponential-bond certificates="
                f"{subset_sum_metrics.get('high_probability_exponential_bond_certificate_count', 'unknown')}"
            ),
            exact_f1_robustness="not reached",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason="A linear prefix has exponentially many distinct subset sums, forcing exact residue states.",
            source_ids=["dcp_subset_sum_measurement_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="collective-approximate-fiber-tensor-layout-dictionary",
            access_model=(
                "collective phase qubits; 99-percent-fidelity subset-sum fiber-state tensor over a fixed polynomial "
                "dictionary of balanced coordinate layouts"
            ),
            access_legal_for_regev_dcp=True,
            state_sample_class="poly(n) input registers assumed",
            time_class="2^(Omega(n))/poly(n) certified bond on density-one random fibers",
            memory_class="2^(Omega(n))/poly(n) approximate Schmidt rank on the certified balanced cut",
            decoder_status=(
                "approximate/layout no-go theorems="
                f"{fiber_entanglement_metrics.get('approximate_polynomial_bond_asymptotic_no_go_theorem_count', 'unknown')}/"
                f"{fiber_entanglement_metrics.get('polynomial_layout_dictionary_density_one_no_go_theorem_count', 'unknown')}; "
                f"adaptive valuation/general-layout theorems="
                f"{adaptive_layout_metrics.get('adaptive_valuation_compression_no_go_theorem_count', 'unknown')}/"
                f"{adaptive_layout_metrics.get('general_adaptive_layout_no_go_theorem_count', 'unknown')}"
            ),
            exact_f1_robustness="not reached",
            lattice_composition_status="blocked",
            dominated_by=["fiber-schmidt-purity-obstruction"],
            blocking_reason=(
                "Second-moment purity and full-fiber concentration force exponential 99-percent-fidelity bond "
                "simultaneously across every layout in a fixed polynomial dictionary. Fully label-adaptive layouts "
                "cannot gain a growing 2-adic subgroup by valuation sorting; genuinely additive adaptive layouts and "
                "partial-instance relation tensors remain open and must prove polynomial selection and source coverage."
            ),
            source_ids=["dcp_fiber_entanglement.py"],
        ),
        DecoderFrontierRow(
            method_id="collective-hashed-hadamard-fiber-erasure",
            access_model="collective phase qubits; public subset-sum hash followed by uniform input postselection",
            access_legal_for_regev_dcp=True,
            state_sample_class="exponential repetitions in the worst hidden reflection with high probability",
            time_class="polynomial conditional circuit plus exponential postselection/amplification overhead",
            memory_class="polynomial hash and input registers",
            decoder_status=(
                "worst-d no-go certificates="
                f"{hashed_fiber_metrics.get('high_probability_polynomial_uniform_success_ruled_out_count', 'unknown')}; "
                f"fiber symmetrizations={hashed_fiber_metrics.get('proved_polynomial_fiber_symmetrization_count', 'unknown')}"
            ),
            exact_f1_robustness="not reached; clean-state postselection is already exponential",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason=(
                "Hidden-average success is the exact subset-sum collision probability, independent of hash dimension; "
                "some hidden d therefore has exponentially small success."
            ),
            source_ids=["dcp_hashed_fiber_measurement_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="collective-public-low-trace-reference-projection",
            access_model="collective phase qubits; arbitrary public label-dependent effect E independent of hidden d",
            access_legal_for_regev_dcp=True,
            state_sample_class="exponential for every polynomial-trace postselection effect on random m=Theta(n) labels",
            time_class="preparation may be polynomial or unbounded; the information/success bound applies regardless",
            memory_class="polynomial-rank effects covered; full-rank many-outcome measurements excluded",
            decoder_status=(
                "low-trace no-go proofs="
                f"{reference_projection_metrics.get('proved_low_trace_effect_no_go_count', 'unknown')}; full-rank no-go "
                f"proofs={reference_projection_metrics.get('proved_full_rank_collective_measurement_no_go_count', 'unknown')}"
            ),
            exact_f1_robustness="not reached; clean-state low-trace success is already exponential",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason=(
                "The exact hidden-average bound Tr(E)c_max/2^m blocks rank-one, polynomial-rank, and every public "
                "polynomial-trace reference effect. Full-rank many-outcome/adaptive measurements remain open."
            ),
            source_ids=["dcp_reference_projection_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="collective-clean-covariant-pgm",
            access_model="clean collective public-label DCP ensemble; full-rank N-outcome covariant measurement",
            access_legal_for_regev_dcp=True,
            state_sample_class="Theta(n) clean states give constant finite information success",
            time_class="unknown; explicit PGM matrix/multiplicity table costs 2^Theta(n)",
            memory_class="unknown; explicit representation has N outcomes and N multiplicities",
            decoder_status=(
                f"mean clean m=n success={covariant_pgm_metrics.get('mean_n_register_pgm_success', 'unknown')}; "
                f"polynomial circuits={covariant_pgm_metrics.get('proved_polynomial_pgm_circuit_count', 'unknown')}"
            ),
            exact_f1_robustness=(
                "information robustness proofs="
                f"{contaminated_pgm_metrics.get('proved_exact_f1_information_robustness_count', 'unknown')}; robust "
                f"circuits={contaminated_pgm_metrics.get('proved_exact_f1_robust_pgm_circuit_count', 'unknown')}"
            ),
            lattice_composition_status="blocked",
            dominated_by=["information-positive-but-computationally-unresolved"],
            blocking_reason=(
                "The exact PGM resolves clean information complexity, but implementing |F_s>->|s> requires an unknown "
                "normalized-fiber isometry, block encoding, or collision walk without N-sized advice."
            ),
            source_ids=["dcp_covariant_pgm_audit.py"],
        ),
        DecoderFrontierRow(
            method_id="regev-partial-average-subset-sum-route",
            access_model="random public DCP labels; deterministic partial modular subset-sum solver at r=n+O(1)",
            access_legal_for_regev_dcp=True,
            state_sample_class="poly(n) conditional on inverse-polynomial legal-input solver coverage",
            time_class="poly(n) conditional theorem; every implemented exact control remains exponential",
            memory_class="poly(n) required; meet-in-the-middle tables are exponential",
            decoder_status=(
                "primary-source bridges="
                f"{subset_sum_bridge_metrics.get('primary_source_conditional_dcp_reduction_count', 'unknown')}; polynomial "
                f"partial solvers={subset_sum_bridge_metrics.get('proved_polynomial_partial_average_subset_sum_solver_count', 'unknown')}"
            ),
            exact_f1_robustness="built into the primary-source conditional DCP matching theorem",
            lattice_composition_status="conditional edge to the verified Regev lattice contract",
            dominated_by=[],
            blocking_reason=(
                "A partial deterministic solver is sufficient and weaker than full PGM implementation, but no structural "
                "poly(n) solver with inverse-polynomial legal-input coverage exists in the project."
            ),
            source_ids=["regev-lattice-dhsp-2003", "dcp_subset_sum_bridge.py"],
        ),
        DecoderFrontierRow(
            method_id="shared-seed-randomized-partial-solver-interface",
            access_model=(
                "uniform random density-one subset-sum inputs; explicit target-independent coins shared coherently "
                "across matched endpoints"
            ),
            access_legal_for_regev_dcp=True,
            state_sample_class="poly(n) conditional on inverse-polynomial average legal coverage",
            time_class="polynomial composition overhead conditional on a polynomial fixed-seed solver",
            memory_class="polynomial shared seed and reversible workspace required",
            decoder_status=(
                f"proved seeded bridge certificates="
                f"{coherent_matching_metrics.get('proved_seeded_randomized_solver_bridge_count', 'unknown')}/"
                f"{coherent_matching_metrics.get('seeded_bridge_certificate_count', 'unknown')}; actual solvers="
                f"{coherent_matching_metrics.get('proved_polynomial_partial_subset_sum_solver_count', 'unknown')}"
            ),
            exact_f1_robustness="inherits the source all-good analysis under the certified shared-seed interface",
            lattice_composition_status="conditional interface proved; solver construction and coverage remain open",
            dominated_by=[],
            blocking_reason=(
                "The interface obstruction is resolved for explicit target-independent shared coins, but no polynomial "
                "partial subset-sum solver with inverse-polynomial source coverage has been constructed."
            ),
            source_ids=["dcp_coherent_matching_interface.py", "regev-lattice-dhsp-2003"],
        ),
        DecoderFrontierRow(
            method_id="general-quantum-relation-partial-solver-interface",
            access_model="target-dependent coherent witness relation with retained amplitude and garbage workspaces",
            access_legal_for_regev_dcp=True,
            state_sample_class="unknown; algorithm-specific",
            time_class="open; no generic composition theorem",
            memory_class="open; paired witness workspaces may be asymptotically orthogonal",
            decoder_status=(
                "proved arbitrary quantum bridges="
                f"{coherent_matching_metrics.get('proved_arbitrary_quantum_relation_solver_bridge_count', 'unknown')}; "
                "zero-visibility counterexamples="
                f"{coherent_matching_metrics.get('zero_visibility_counterexample_count', 'unknown')}"
            ),
            exact_f1_robustness="not reached until paired-endpoint coherence is proved",
            lattice_composition_status="blocked on canonicalization, amplitude balance, workspace overlap, and erasure",
            dominated_by=[],
            blocking_reason=(
                "A generic quantum relation solver can leave orthogonal which-path workspaces and erase the DCP phase. "
                "A concrete algorithm needs a seeded decomposition or inverse-polynomial paired-workspace fidelity theorem."
            ),
            source_ids=["dcp_coherent_matching_interface.py"],
        ),
        DecoderFrontierRow(
            method_id="odd-unit-randomized-lll-partial-subset-sum",
            access_model=(
                "independent uniform density-one labels and target; target-independent explicit odd-unit seeds shared coherently"
            ),
            access_legal_for_regev_dcp=True,
            state_sample_class="not a state routine; verified classical partial-solver candidate",
            time_class="poly(n) LLL calls under a polynomial odd-unit seed budget",
            memory_class="poly(n) integer basis and explicit O(n)-bit seed",
            decoder_status=(
                f"source bijections="
                f"{random_self_reduction_metrics.get('source_distribution_bijection_certificate_count', 'unknown')}; "
                f"odd-unit rescues={random_self_reduction_metrics.get('odd_unit_rescue_count', 'unknown')}; tail "
                f"unconditional success={random_self_reduction_metrics.get('tail_odd_unit_unconditional_success_count', 'unknown')}/"
                f"{random_self_reduction_metrics.get('tail_trial_count', 'unknown')}; orbit slope="
                f"{odd_unit_geometry_metrics.get('fitted_log2_unconditional_success_slope_per_n', 'unknown')}; orbit tail="
                f"{odd_unit_geometry_metrics.get('tail_verified_witness_count', 'unknown')}/"
                f"{odd_unit_geometry_metrics.get('tail_record_count', 'unknown')}"
            ),
            exact_f1_robustness="inherits the proved shared-seed matching interface if source coverage is established",
            lattice_composition_status="exact source map proved; orbit-hitting and average-case LLL coverage open",
            dominated_by=[],
            blocking_reason=(
                "Odd units are a legitimate non-sign-isometric presentation class, but success fits exponential decay, "
                "reaches zero in the scaling tail, and no pre-reduction rule survives there. Blind orbit sampling is cut "
                "unless a new odd-part invariant yields an easy-orbit measure and LLL theorem."
            ),
            source_ids=[
                "dcp_subset_sum_random_self_reduction.py",
                "dcp_odd_unit_orbit_geometry.py",
                "dcp_coherent_matching_interface.py",
            ],
        ),
        DecoderFrontierRow(
            method_id="deterministic-modular-lll-partial-subset-sum",
            access_model="uniform random density-one modular subset-sum inputs from Regev's matching interface",
            access_legal_for_regev_dcp=True,
            state_sample_class="not a state routine; candidate classical preprocessing subroutine",
            time_class="polynomial exact integer LLL and fixed-arity basis scan",
            memory_class="polynomial dimension and O(n)-bit entries",
            decoder_status=(
                f"finite success rows={subset_sum_lattice_metrics.get('finite_success_row_count', 'unknown')}; tail success "
                f"rows={subset_sum_lattice_metrics.get('tail_success_row_count', 'unknown')}/"
                f"{subset_sum_lattice_metrics.get('tail_row_count', 'unknown')}; coverage proofs="
                f"{subset_sum_lattice_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 'unknown')}"
            ),
            exact_f1_robustness="would inherit source theorem only after the partial-solver coverage contract is proved",
            lattice_composition_status="blocked on coverage and reversible uniform implementation",
            dominated_by=["regev-partial-average-subset-sum-route-target"],
            blocking_reason=(
                "Small-n centered-embedding recovery collapses in the tail; no uniform inverse-polynomial legal-input "
                "coverage or reversible implementation theorem exists."
            ),
            source_ids=["dcp_subset_sum_lattice_search.py"],
        ),
        DecoderFrontierRow(
            method_id="two-adic-carry-lifting-partial-subset-sum",
            access_model="uniform random density-one subset-sum inputs over Z_(2^n)",
            access_legal_for_regev_dcp=True,
            state_sample_class="not a state routine; structural candidate for Regev's partial solver",
            time_class="current audit Theta(2^(n+offset)); no polynomial witness algorithm",
            memory_class="exact fiber enumeration is exponential; compact symbolic representation remains open",
            decoder_status=(
                f"degree-censored lifts={subset_sum_two_adic_metrics.get('degree_censored_lift_count', 'unknown')}; "
                f"all-affine legal trials={subset_sum_two_adic_metrics.get('all_lifts_affine_trial_count', 'unknown')}; "
                f"uniform polynomial solvers={subset_sum_two_adic_metrics.get('proved_uniform_polynomial_two_adic_solver_count', 'unknown')}"
            ),
            exact_f1_robustness="would inherit the source theorem only after satisfying the partial-solver contract",
            lattice_composition_status="blocked on symbolic compactness, polynomial solving, coverage, and reversibility",
            dominated_by=["regev-partial-average-subset-sum-route-target"],
            blocking_reason=(
                "The exact carry audit uses exponential enumeration; finite bounded-degree fits may be interpolation, "
                "affine hulls overcover exact fibers, and no polynomial witness-finding theorem exists."
            ),
            source_ids=["dcp_subset_sum_two_adic_search.py"],
        ),
        DecoderFrontierRow(
            method_id="known-subset-sum-resource-frontier",
            access_model="random density-one modular subset sum; algorithm-specific exact, heuristic, randomized, or quantum access",
            access_legal_for_regev_dcp=True,
            state_sample_class="not a DCP state routine; comparison frontier for the partial matching subroutine",
            time_class=(
                "best recorded classical/quantum exponents="
                f"{subset_sum_resource_metrics.get('best_recorded_classical_time_exponent', 'unknown')}/"
                f"{subset_sum_resource_metrics.get('best_recorded_quantum_time_exponent', 'unknown')}"
            ),
            memory_class="algorithm-dependent exponential memory or quantum-accessible memory; no polynomial complete route",
            decoder_status=(
                f"known algorithms={subset_sum_resource_metrics.get('known_algorithm_count', 'unknown')}; Regev-contract "
                f"solvers={subset_sum_resource_metrics.get('known_regev_contract_satisfying_algorithm_count', 'unknown')}"
            ),
            exact_f1_robustness="only source-interface compatible after polynomial deterministic or coherent composition",
            lattice_composition_status="blocked because every recorded route retains a positive time exponent",
            dominated_by=["regev-partial-average-subset-sum-route-target"],
            blocking_reason=(
                "Known exponent improvements remain exponential in n=log2 N; heuristic/randomized/quantum routes also "
                "need an interface theorem before entering Regev's deterministic matching reduction."
            ),
            source_ids=["dcp_subset_sum_resource_frontier.py"],
        ),
        DecoderFrontierRow(
            method_id="bounded-degree-two-adic-carry-reconstruction",
            access_model="public random density-one labels and target over Z_(2^n)",
            access_legal_for_regev_dcp=True,
            state_sample_class="not a state routine; proposed algebraic partial subset-sum subroutine",
            time_class="current exact ANF audit costs 2^(n+O(1)); no polynomial symbolic solver",
            memory_class="full truth tables exponential; no uniform sparse representation proved",
            decoder_status=(
                f"tail bounded-degree rows={subset_sum_carry_metrics.get('tail_bounded_degree_row_count', 'unknown')}/"
                f"{subset_sum_carry_metrics.get('tail_carry_row_count', 'unknown')}; max degree="
                f"{subset_sum_carry_metrics.get('maximum_observed_anf_degree', 'unknown')}"
            ),
            exact_f1_robustness="would inherit source theorem only after satisfying the partial-solver contract",
            lattice_composition_status="blocked on bounded representation, witness solving, legal coverage, and reversibility",
            dominated_by=["regev-partial-average-subset-sum-route-target"],
            blocking_reason=(
                "Exact full-domain high-bit carry ANFs are not bounded degree in the tested random family; the audit is "
                "exponential and no polynomial algebraic witness solver exists."
            ),
            source_ids=["dcp_subset_sum_carry_anf.py"],
        ),
        DecoderFrontierRow(
            method_id="logarithmic-low-bit-bdd-preconditioner",
            access_model="public random density-one labels; exact congruence modulo 2^ceil(c log n)",
            access_legal_for_regev_dcp=True,
            state_sample_class="polynomial reversible preparation of the low-bit-valid assignment fiber",
            time_class="O(n 2^b poly(n))=poly(n) for fixed b/log n multiplier",
            memory_class="O(2^b poly(n))=poly(n); completion counts have O(n) bits",
            decoder_status=(
                f"width/state certificates={subset_sum_low_bit_metrics.get('polynomial_width_certificate_count', 'unknown')}/"
                f"{subset_sum_low_bit_metrics.get('polynomial_state_preparation_certificate_count', 'unknown')}; witness "
                f"solvers={subset_sum_low_bit_metrics.get('proved_polynomial_witness_solver_count', 'unknown')}"
            ),
            exact_f1_robustness="preprocessing primitive only; would compose after a high-bit partial solver exists",
            lattice_composition_status="positive low-bit primitive; blocked on conditioned high-bit geometry and legal coverage",
            dominated_by=[],
            blocking_reason=(
                "The exact polynomial low-bit representation is proved, but O(log n)-bit conditioning leaves linear "
                "residual witness entropy and no polynomial high-bit decoder."
            ),
            source_ids=["dcp_subset_sum_low_bit_bdd.py"],
        ),
        DecoderFrontierRow(
            method_id="conditioned-high-bit-quotient-implicit-decoder",
            access_model="public random density-one labels conditioned by the exact O(log n)-bit BDD",
            access_legal_for_regev_dcp=True,
            state_sample_class="not yet a state routine; exact finite quotient multiplicities are an exponential audit",
            time_class="open target poly(n); explicit multiplicity table costs 2^Theta(n)",
            memory_class="open target poly(n); current full quotient table costs 2^Theta(n)",
            decoder_status=(
                f"tail minimum normalized entropy="
                f"{subset_sum_conditioned_quotient_metrics.get('minimum_tail_normalized_shannon_entropy', 'unknown')}; "
                f"polynomial high-bit decoders="
                f"{subset_sum_conditioned_quotient_metrics.get('proved_polynomial_high_bit_decoder_count', 'unknown')}"
            ),
            exact_f1_robustness="would inherit the source theorem only after legal coverage and reversible composition",
            lattice_composition_status="open; must prove changed quotient geometry rather than explicit-list concentration",
            dominated_by=[],
            blocking_reason=(
                "Exact finite conditioned quotients remain broad and no polynomial implicit decoder or asymptotic geometry "
                "theorem exists; this rejects the explicit-list shortcut, not all quotient-lattice mechanisms."
            ),
            source_ids=["dcp_subset_sum_conditioned_quotient.py"],
        ),
        DecoderFrontierRow(
            method_id="carry-sliced-quotient-lattice",
            access_model="public random density-one labels; all exact O(log n)-bit carry slices",
            access_legal_for_regev_dcp=True,
            state_sample_class="not a state routine; deterministic classical partial-solver candidate",
            time_class="poly(n) LLL calls with O(n)-bit entries for fixed extraction arity",
            memory_class="poly(n)",
            decoder_status=(
                f"paired baseline/sliced={subset_sum_carry_slice_metrics.get('baseline_success_count', 'unknown')}/"
                f"{subset_sum_carry_slice_metrics.get('carry_sliced_success_count', 'unknown')}; tail="
                f"{subset_sum_carry_slice_metrics.get('tail_baseline_success_count', 'unknown')}/"
                f"{subset_sum_carry_slice_metrics.get('tail_carry_sliced_success_count', 'unknown')}"
            ),
            exact_f1_robustness="would inherit source robustness only after the partial-solver coverage theorem",
            lattice_composition_status="deterministic finite solver implemented; uniform legal coverage and reversibility open",
            dominated_by=["deterministic-modular-lll-partial-subset-sum"],
            blocking_reason=(
                "Carry slicing adds a real polynomial exact constraint but does not improve paired tail recovery in the "
                "live sweep and has no average-case short-vector separation or inverse-polynomial coverage theorem."
            ),
            source_ids=["dcp_subset_sum_carry_slice_lattice.py"],
        ),
        DecoderFrontierRow(
            method_id="source-target-high-representation-partial-solver",
            access_model="independent uniform density-one labels and target; no planted witness",
            access_legal_for_regev_dcp=True,
            state_sample_class="not a state routine; proposed classical partial subset-sum solver",
            time_class="open target poly(n); current full target-table audit is 2^Theta(n)",
            memory_class="open target poly(n); current multiplicity table is 2^Theta(n)",
            decoder_status=(
                f"planted/legal TV="
                f"{subset_sum_target_distribution_metrics.get('mean_tail_planted_vs_uniform_legal_total_variation', 'unknown')}; "
                f"detectable source subfamilies="
                f"{subset_sum_target_distribution_metrics.get('proved_inverse_polynomial_high_multiplicity_legal_subfamily_count', 'unknown')}"
            ),
            exact_f1_robustness="would inherit source theorem only after a valid partial-solver contract",
            lattice_composition_status="blocked on source coverage, efficient detection, witness recovery, and reversibility",
            dominated_by=[],
            blocking_reason=(
                "Planted targets are measurably size-biased; no independent-uniform source subfamily is proved both "
                "inverse-polynomially common and efficiently detectable, and no polynomial representation solver exists."
            ),
            source_ids=["dcp_subset_sum_target_distribution.py"],
        ),
        DecoderFrontierRow(
            method_id="exact-likelihood-interval-branch-bound",
            access_model="iid random-label local measurements with f=1-rate basis-state contamination",
            access_legal_for_regev_dcp=True,
            state_sample_class="poly(n)",
            time_class="2^(Theta(n)) candidate score evaluations in observed exact scaling",
            memory_class="sublinear queue possible, but exponential score work remains",
            decoder_status=(
                "exact recoveries="
                f"{likelihood_metrics.get('exact_decode_success_count', 'unknown')}; fitted slope="
                f"{likelihood_metrics.get('fitted_log2_evaluation_slope_per_n', 'unknown')}"
            ),
            exact_f1_robustness="finite exact search uses the allowed contamination channel; no efficient theorem",
            lattice_composition_status="blocked",
            dominated_by=["kuperberg-generic-sieve", "regev-polynomial-space-sieve"],
            blocking_reason="Rigorous separable interval bounds evaluate an exponential candidate set.",
            source_ids=["dcp_likelihood_branch_bound.py"],
        ),
        DecoderFrontierRow(
            method_id="target-polynomial-dcp-decoder",
            access_model="exact f=1 random-label DCP state contract",
            access_legal_for_regev_dcp=True,
            state_sample_class="poly(n)",
            time_class="poly(n)",
            memory_class="poly(n)",
            decoder_status="open target",
            exact_f1_robustness="required",
            lattice_composition_status="required with primary-source parameter map",
            dominated_by=[],
            blocking_reason="No construction or proof currently exists.",
            source_ids=["THM-REGEV-USVP-TO-DCP-2003"],
        ),
    ]
    metrics = {
        "row_count": len(rows),
        "legal_row_count": sum(row.access_legal_for_regev_dcp for row in rows),
        "illegal_access_row_count": sum(not row.access_legal_for_regev_dcp for row in rows),
        "exponential_time_row_count": sum("2^(Theta(n))" in row.time_class for row in rows),
        "generic_subexponential_baseline_count": 2,
        "proved_polynomial_exact_f1_decoder_count": 0,
        "complete_lattice_composition_count": 0,
        "proved_restricted_decoder_no_go_count": int(
            bool(iid_hash_metrics.get("proved_exact_linear_estimator_no_go_count", 0))
        ),
    }
    return DCPDecoderFrontierReport(
        created_at=utc_now(),
        parameter="n=ceil(log2 N)",
        rows=rows,
        headline_metrics=metrics,
        target_contract={
            "input": "poly(n) independent registers, each good with probability >=1-1/n and otherwise arbitrary basis state",
            "success": "inverse-polynomial in n",
            "resources": "poly(n) time, state samples, and memory",
            "output": "complete hidden reflection d, not one parity bit or a detector statistic",
        },
        claim_gate={
            "named_generic_baselines_present": True,
            "access_legality_explicit": True,
            "sample_time_memory_separated": True,
            "proved_polynomial_exact_f1_decoder": False,
            "complete_lattice_composition": False,
            "speedup_claim_allowed": False,
            "reason": "Every implemented legal route is exponential, subexponential, signal-only, restricted-no-go, or missing exact f=1 robustness.",
        },
        status="polynomial-dcp-decoder-open",
        summary=(
            f"Compared {len(rows)} DCP decoder/resource classes. FFT, exact likelihood search, and exact or uniformly "
            "margin-separated linear iid hash "
            "and disjoint multirecord routes are dominated or restricted-no-go; structured sparse FFT and chosen-label methods are access-invalid; "
            "no polynomial exact-f=1 decoder exists."
        ),
        falsifiers_triggered=[
            "Polynomial state samples do not imply polynomial decoding time.",
            "Grover over candidate reflections remains exponential and loses to generic DCP sieves.",
            "Chosen-label phase estimation does not preserve the theorem input interface.",
            "Finite Clifford signal does not provide a full robust decoder.",
            "Structured-query sparse FFT does not preserve iid DCP access.",
            "Exact linear iid hash bins satisfy an exponential Parseval tradeoff.",
            "Biased uniformly margin-separated one-score buckets retain the Parseval/MSE tradeoff.",
            "Disjoint fixed-degree product kernels retain the aggregate-label Jensen/Parseval tradeoff and add a 4^r penalty.",
            "Explicit overlapping product U-statistics require exponential records or tuple terms by Hoeffding decomposition.",
            "Rank-one elementary-symmetric contraction removes tuple enumeration but still needs exponential records.",
            "Tested polynomial-rank Fejer/Fourier contractions separate finitely but fail exact sample scaling.",
            "Computing and QFTing a subset-sum ancilla is exactly uninformative while which-subset garbage remains.",
            "Straightforward exact residue tensor networks have exponential bond dimension with high probability.",
            "Fixed polynomial dictionaries of balanced 99-percent-fidelity fiber-state tensor layouts retain exponential bond with high probability.",
            "Balanced label-adaptive valuation sorting cannot obtain a growing power-of-two subgroup compression; exact-rank adaptive scoring is exponential.",
            "Uniform hashed-fiber erasure has exponentially small worst-d postselection success.",
            "Changing to any public polynomial-trace reference effect cannot overcome the maximum-fiber bound.",
            "Constant exact covariant-PGM success is information-theoretic evidence, not an efficient circuit.",
            "Global linear-block PGM information survives exact f=1 product contamination, so signal-only robustness is no longer the open target.",
            "Regev's partial average-case subset-sum route is source-verified, but polynomial explicit candidate enumeration has inadequate coverage.",
            "Tested deterministic modular LLL embeddings show transient finite recovery but no tail coverage theorem.",
            "Exact 2-adic carry fits are structural diagnostics, not polynomial witness solvers.",
            "Every source-linked known subset-sum frontier retains a positive exponential time exponent.",
            "Full-domain random carry ANFs reject bounded-degree algebraic reconstruction in the tested scaling range.",
            "Polynomial logarithmic-low-bit BDD/state preparation leaves the high-bit witness problem open.",
            "Exact conditioned high-bit quotients reject polynomial explicit-list concentration and still lack an implicit decoder theorem.",
            "Carry-sliced constrained LLL fails to improve the live paired tail and has no legal-coverage theorem.",
            "Planted target representation gains do not transfer to the independent uniform source law without coverage and detectability proofs.",
            "Explicit target-independent shared-seed randomness is interface-compatible but supplies no subset-sum solver.",
            "Arbitrary quantum relation solvers can erase phase information through orthogonal paired witness workspaces.",
            "Signed self-reductions are embedding isometries; odd-unit LLL randomization remains coverage-blocked after tail collapse.",
            "Separable likelihood interval bounds evaluate all N candidates in the live scaling sweep.",
        ],
    )


def write_decoder_frontier(
    path: Path = DCP_DECODER_FRONTIER_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = build_decoder_frontier()
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-DECODER-FRONTIER"
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
                artifacts={"dcp_decoder_frontier": str(path)},
            )
        )
    return payload
