"""Trace-moment certificates for wreath projector-sub-POVM success.

For a physical source block with average support-projector frame ``B``, the
maximal covariant projector sub-POVM has conclusive probability

    q = Tr(B^2) / (Tr(B) ||B||).

For every integer ``p>=2``,

    ||B|| <= Tr(B^p)^(1/p),

so

    q >= Tr(B^2)/(Tr(B) Tr(B^p)^(1/p)).

This converts the all-sector sub-POVM question into a high-order character
moment contraction problem.  On the complete naturally occupied W_3 threshold
portfolio the certificate is evaluated exactly through order 16.  At scale,
an order comparable to the log block dimension gives a constant-factor norm
approximation, but no all-sector polynomial contraction at that growing order
or structured maximal-effect Naimark dilation is currently known.
"""

from __future__ import annotations

import json
import math
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
from self_dual_wreath_complete_w3_tuple_audit import (
    run_complete_w3_tuple_audit,
)
from self_dual_wreath_pgm_polar_audit import (
    run_self_dual_wreath_pgm_polar_audit,
)
from self_dual_wreath_natural_unequal_dominance import (
    run_natural_unequal_dominance,
)
from self_dual_wreath_natural_moment_word_map import (
    run_natural_moment_word_map,
)
from self_dual_wreath_word_map_mixing import (
    run_wreath_word_map_mixing,
)
from self_dual_wreath_coupled_word_walk_gap import (
    run_wreath_coupled_word_walk_gap,
)
from self_dual_wreath_all_unequal_conditioned_kernel import (
    run_all_unequal_conditioned_kernel,
)
from self_dual_wreath_global_partition_collision import (
    run_global_partition_collision,
)
from self_dual_wreath_collision_free_frame_probe import (
    run_collision_free_frame_probe,
)
from self_dual_wreath_character_ratio_contract import (
    run_character_ratio_contract,
)
from self_dual_wreath_short_word_profile import (
    run_short_word_profile,
)
from self_dual_wreath_mask_hypergraph_reduction import (
    run_mask_hypergraph_reduction,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    run_subgroup_twirl_reduction,
)
from self_dual_wreath_orientation_fourier_reduction import (
    run_orientation_fourier_reduction,
)
from self_dual_wreath_orientation_fusion_moment import (
    run_orientation_fusion_moment,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_subpovm_moment_certificate.json"
)
W3_TUPLE_PATH = Path(
    "research/representation/self_dual_wreath_complete_w3_tuple_audit.json"
)
WREATH_PGM_PATH = Path(
    "research/representation/self_dual_wreath_pgm_polar_audit.json"
)
NATURAL_UNEQUAL_PATH = Path(
    "research/representation/"
    "self_dual_wreath_natural_unequal_dominance.json"
)
NATURAL_WORD_MAP_PATH = Path(
    "research/representation/"
    "self_dual_wreath_natural_moment_word_map.json"
)
WORD_MAP_MIXING_PATH = Path(
    "research/representation/self_dual_wreath_word_map_mixing.json"
)
COUPLED_WORD_WALK_GAP_PATH = Path(
    "research/representation/"
    "self_dual_wreath_coupled_word_walk_gap.json"
)
ALL_UNEQUAL_CONDITIONED_KERNEL_PATH = Path(
    "research/representation/"
    "self_dual_wreath_all_unequal_conditioned_kernel.json"
)
GLOBAL_PARTITION_COLLISION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_global_partition_collision.json"
)
COLLISION_FREE_FRAME_PROBE_PATH = Path(
    "research/representation/"
    "self_dual_wreath_collision_free_frame_probe.json"
)
CHARACTER_RATIO_CONTRACT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_character_ratio_contract.json"
)
SHORT_WORD_PROFILE_PATH = Path(
    "research/representation/self_dual_wreath_short_word_profile.json"
)
MASK_HYPERGRAPH_REDUCTION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_mask_hypergraph_reduction.json"
)
SUBGROUP_TWIRL_REDUCTION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_subgroup_twirl_reduction.json"
)
ORIENTATION_FOURIER_REDUCTION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_fourier_reduction.json"
)
ORIENTATION_FUSION_MOMENT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_fusion_moment.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-SUBPOVM-MOMENTS"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FiniteMomentCertificateRecord:
    moment_order: int
    naturally_occupied_block_count: int
    natural_mass: float
    exact_natural_average_conclusive_probability: float
    certified_natural_average_conclusive_lower_bound: float
    certificate_fraction_of_exact: float
    minimum_block_certificate_fraction_of_exact: float
    certificate_violation_count: int
    status: str


@dataclass(frozen=True)
class GrowingMomentRequirementRecord:
    n: int
    copy_count: int
    log2_hilbert_dimension_upper_bound: float
    moment_order_for_factor_two_norm_approximation: int
    moment_order_polynomial_in_input_n: bool
    all_sector_moment_contraction_proved: bool
    structured_maximal_effect_dilation_proved: bool
    status: str


@dataclass(frozen=True)
class WreathSubPOVMMomentCertificateReport:
    created_at: str
    theorem_contract: dict[str, object]
    finite_certificates: list[FiniteMomentCertificateRecord]
    scaling_requirements: list[GrowingMomentRequirementRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def moment_conclusive_lower_bound(
    eigenvalues: tuple[float, ...],
    moment_order: int,
) -> tuple[float, float]:
    if moment_order < 2:
        raise ValueError("moment_order must be at least two")
    positive = tuple(value for value in eigenvalues if value > 1e-12)
    if not positive:
        return 0.0, 0.0
    trace = sum(positive)
    second = sum(value * value for value in positive)
    exact = second / (trace * max(positive))
    moment = sum(value**moment_order for value in positive)
    lower = second / (trace * moment ** (1 / moment_order))
    return exact, lower


def build_wreath_subpovm_moment_certificate_report(
    moment_orders: tuple[int, ...] = (2, 3, 4, 8, 16),
    w3_tuple_path: Path = W3_TUPLE_PATH,
    wreath_pgm_path: Path = WREATH_PGM_PATH,
    natural_unequal_path: Path = NATURAL_UNEQUAL_PATH,
    natural_word_map_path: Path = NATURAL_WORD_MAP_PATH,
    word_map_mixing_path: Path = WORD_MAP_MIXING_PATH,
    coupled_word_walk_gap_path: Path = COUPLED_WORD_WALK_GAP_PATH,
    all_unequal_conditioned_kernel_path: Path = (
        ALL_UNEQUAL_CONDITIONED_KERNEL_PATH
    ),
    global_partition_collision_path: Path = (
        GLOBAL_PARTITION_COLLISION_PATH
    ),
    collision_free_frame_probe_path: Path = (
        COLLISION_FREE_FRAME_PROBE_PATH
    ),
    character_ratio_contract_path: Path = CHARACTER_RATIO_CONTRACT_PATH,
    short_word_profile_path: Path = SHORT_WORD_PROFILE_PATH,
    mask_hypergraph_reduction_path: Path = (
        MASK_HYPERGRAPH_REDUCTION_PATH
    ),
    subgroup_twirl_reduction_path: Path = (
        SUBGROUP_TWIRL_REDUCTION_PATH
    ),
    orientation_fourier_reduction_path: Path = (
        ORIENTATION_FOURIER_REDUCTION_PATH
    ),
    orientation_fusion_moment_path: Path = ORIENTATION_FUSION_MOMENT_PATH,
) -> WreathSubPOVMMomentCertificateReport:
    w3 = _read_json(w3_tuple_path, {})
    if not w3:
        w3 = asdict(run_complete_w3_tuple_audit())
    occupied = [
        record
        for record in w3.get("tuple_records", [])
        if float(record.get("aggregate_natural_probability", 0)) > 0
    ]
    certificates: list[FiniteMomentCertificateRecord] = []
    for order in moment_orders:
        exact_average = 0.0
        lower_average = 0.0
        minimum_fraction = 1.0
        violations = 0
        natural_mass = 0.0
        for record in occupied:
            eigenvalues: list[float] = []
            for cluster in record.get("eigenvalue_multiplicities", []):
                eigenvalues.extend(
                    [float(cluster["eigenvalue"])]
                    * int(cluster["multiplicity"])
                )
            exact, lower = moment_conclusive_lower_bound(
                tuple(eigenvalues),
                order,
            )
            weight = float(record["aggregate_natural_probability"])
            natural_mass += weight
            exact_average += weight * exact
            lower_average += weight * lower
            if lower > exact + 1e-10:
                violations += 1
            if exact > 0:
                minimum_fraction = min(minimum_fraction, lower / exact)
        certificates.append(
            FiniteMomentCertificateRecord(
                moment_order=order,
                naturally_occupied_block_count=len(occupied),
                natural_mass=natural_mass,
                exact_natural_average_conclusive_probability=exact_average,
                certified_natural_average_conclusive_lower_bound=lower_average,
                certificate_fraction_of_exact=(
                    lower_average / exact_average
                    if exact_average > 0
                    else 0.0
                ),
                minimum_block_certificate_fraction_of_exact=minimum_fraction,
                certificate_violation_count=violations,
                status="exact-finite-subpovm-moment-certificate",
            )
        )
    wreath = _read_json(wreath_pgm_path, {})
    if not wreath:
        wreath = asdict(run_self_dual_wreath_pgm_polar_audit())
    natural_unequal = _read_json(natural_unequal_path, {})
    if not natural_unequal:
        natural_unequal = asdict(run_natural_unequal_dominance())
    natural_metrics = natural_unequal.get("headline_metrics", {})
    natural_word_map = _read_json(natural_word_map_path, {})
    if not natural_word_map:
        natural_word_map = asdict(run_natural_moment_word_map())
    word_map_metrics = natural_word_map.get("headline_metrics", {})
    word_map_mixing = _read_json(word_map_mixing_path, {})
    if not word_map_mixing:
        word_map_mixing = asdict(run_wreath_word_map_mixing())
    mixing_metrics = word_map_mixing.get("headline_metrics", {})
    coupled_word_walk_gap = _read_json(coupled_word_walk_gap_path, {})
    if not coupled_word_walk_gap:
        coupled_word_walk_gap = asdict(run_wreath_coupled_word_walk_gap())
    coupled_metrics = coupled_word_walk_gap.get("headline_metrics", {})
    all_unequal_conditioned_kernel = _read_json(
        all_unequal_conditioned_kernel_path,
        {},
    )
    if not all_unequal_conditioned_kernel:
        all_unequal_conditioned_kernel = asdict(
            run_all_unequal_conditioned_kernel()
        )
    conditioned_metrics = all_unequal_conditioned_kernel.get(
        "headline_metrics", {}
    )
    global_partition_collision = _read_json(
        global_partition_collision_path,
        {},
    )
    if not global_partition_collision:
        global_partition_collision = asdict(
            run_global_partition_collision()
        )
    global_collision_metrics = global_partition_collision.get(
        "headline_metrics", {}
    )
    collision_free_frame_probe = _read_json(
        collision_free_frame_probe_path,
        {},
    )
    if not collision_free_frame_probe:
        collision_free_frame_probe = asdict(
            run_collision_free_frame_probe()
        )
    collision_free_probe_metrics = collision_free_frame_probe.get(
        "headline_metrics", {}
    )
    character_ratio_contract = _read_json(
        character_ratio_contract_path,
        {},
    )
    if not character_ratio_contract:
        character_ratio_contract = asdict(
            run_character_ratio_contract()
        )
    character_ratio_metrics = character_ratio_contract.get(
        "headline_metrics", {}
    )
    short_word_profile = _read_json(short_word_profile_path, {})
    if not short_word_profile:
        short_word_profile = asdict(run_short_word_profile())
    short_word_metrics = short_word_profile.get("headline_metrics", {})
    mask_hypergraph_reduction = _read_json(
        mask_hypergraph_reduction_path,
        {},
    )
    if not mask_hypergraph_reduction:
        mask_hypergraph_reduction = asdict(
            run_mask_hypergraph_reduction()
        )
    mask_hypergraph_metrics = mask_hypergraph_reduction.get(
        "headline_metrics", {}
    )
    subgroup_twirl_reduction = _read_json(
        subgroup_twirl_reduction_path,
        {},
    )
    if not subgroup_twirl_reduction:
        subgroup_twirl_reduction = asdict(
            run_subgroup_twirl_reduction()
        )
    subgroup_twirl_metrics = subgroup_twirl_reduction.get(
        "headline_metrics", {}
    )
    orientation_fourier_reduction = _read_json(
        orientation_fourier_reduction_path,
        {},
    )
    if not orientation_fourier_reduction:
        orientation_fourier_reduction = asdict(
            run_orientation_fourier_reduction()
        )
    orientation_fourier_metrics = orientation_fourier_reduction.get(
        "headline_metrics", {}
    )
    orientation_fusion_moment = _read_json(
        orientation_fusion_moment_path,
        {},
    )
    if not orientation_fusion_moment:
        orientation_fusion_moment = asdict(
            run_orientation_fusion_moment()
        )
    orientation_fusion_metrics = orientation_fusion_moment.get(
        "headline_metrics", {}
    )
    scaling = [
        GrowingMomentRequirementRecord(
            n=int(record["n"]),
            copy_count=int(record["copy_count"]),
            log2_hilbert_dimension_upper_bound=float(
                record["log2_kcopy_hilbert_dimension"]
            ),
            moment_order_for_factor_two_norm_approximation=math.ceil(
                float(record["log2_kcopy_hilbert_dimension"])
            ),
            moment_order_polynomial_in_input_n=True,
            all_sector_moment_contraction_proved=False,
            structured_maximal_effect_dilation_proved=False,
            status="polynomial-order-moment-target-contraction-open",
        )
        for record in wreath.get("records", [])
    ]
    order_four = next(
        record for record in certificates if record.moment_order == 4
    )
    tail = scaling[-1] if scaling else None
    metrics: dict[str, int | float] = {
        "moment_to_conclusive_lower_bound_theorem_count": 1,
        "finite_certificate_count": len(certificates),
        "naturally_occupied_w3_block_count": len(occupied),
        "finite_certificate_violation_count": sum(
            record.certificate_violation_count for record in certificates
        ),
        "exact_w3_natural_average_conclusive_probability": (
            order_four.exact_natural_average_conclusive_probability
        ),
        "order_four_certified_natural_average_conclusive_lower_bound": (
            order_four.certified_natural_average_conclusive_lower_bound
        ),
        "order_sixteen_certified_natural_average_conclusive_lower_bound": next(
            record.certified_natural_average_conclusive_lower_bound
            for record in certificates
            if record.moment_order == 16
        ),
        "scaling_requirement_count": len(scaling),
        "tail_n": tail.n if tail else 0,
        "tail_factor_two_moment_order_upper_bound": (
            tail.moment_order_for_factor_two_norm_approximation
            if tail
            else 0
        ),
        "polynomial_order_requirement_row_count": sum(
            record.moment_order_polynomial_in_input_n for record in scaling
        ),
        "all_sector_growing_order_moment_contraction_count": 0,
        "natural_source_equal_sector_bypass_theorem_count": int(
            natural_metrics.get(
                "equal_commutator_natural_critical_path_bypass_count",
                0,
            )
            or 0
        ),
        "natural_source_all_unequal_threshold_dominance_theorem_count": int(
            natural_metrics.get(
                "threshold_tuple_all_unequal_dominance_theorem_count",
                0,
            )
            or 0
        ),
        "growing_order_all_unequal_contraction_count": int(
            natural_metrics.get(
                "growing_order_all_unequal_contraction_count",
                0,
            )
            or 0
        ),
        "all_order_natural_word_map_reduction_count": int(
            word_map_metrics.get(
                "all_order_source_averaged_word_map_reduction_count",
                0,
            )
            or 0
        ),
        "growing_order_word_map_contraction_count": int(
            word_map_metrics.get(
                "growing_order_word_map_contraction_count",
                0,
            )
            or 0
        ),
        "natural_tuple_moment_concentration_theorem_count": int(
            mixing_metrics.get(
                "word_map_concentration_theorem_count",
                0,
            )
            or 0
        ),
        "single_walk_mean_mixing_theorem_count": int(
            mixing_metrics.get(
                "single_walk_mean_mixing_theorem_count",
                0,
            )
            or 0
        ),
        "coupled_k_walk_contraction_count": int(
            coupled_metrics.get(
                "coupled_k_walk_contraction_count",
                0,
            )
            or 0
        ),
        "constant_coupled_spectral_gap_theorem_count": int(
            coupled_metrics.get(
                "constant_coupled_spectral_gap_theorem_count",
                0,
            )
            or 0
        ),
        "tail_log2_root_to_second_moment_scale_gap": float(
            coupled_metrics.get(
                "tail_log2_root_to_second_moment_scale_gap",
                0,
            )
            or 0
        ),
        "typical_all_unequal_conditioned_kernel_count": int(
            conditioned_metrics.get(
                "typical_all_unequal_conditioned_kernel_count",
                0,
            )
            or 0
        ),
        "all_unequal_frame_half_norm_bound_count": int(
            conditioned_metrics.get(
                "all_unequal_frame_half_norm_bound_count",
                0,
            )
            or 0
        ),
        "simultaneous_k_coordinate_contraction_count": int(
            conditioned_metrics.get(
                "simultaneous_k_coordinate_contraction_count",
                0,
            )
            or 0
        ),
        "asymptotic_global_all_distinct_dominance_theorem_count": int(
            global_collision_metrics.get(
                "asymptotic_global_all_distinct_dominance_theorem_count",
                0,
            )
            or 0
        ),
        "collision_free_growing_moment_contraction_count": int(
            collision_free_probe_metrics.get(
                "collision_free_growing_moment_contraction_count",
                0,
            )
            or 0
        ),
        "finite_collision_free_constant_factor_signal_count": int(
            collision_free_probe_metrics.get(
                "finite_collision_free_constant_factor_signal_count",
                0,
            )
            or 0
        ),
        "collision_free_polynomial_factor_norm_theorem_count": int(
            character_ratio_metrics.get(
                "collision_free_polynomial_factor_norm_theorem_count",
                0,
            )
            or 0
        ),
        "joint_short_word_anticoncentration_theorem_count": int(
            short_word_metrics.get(
                "joint_short_word_anticoncentration_theorem_count",
                0,
            )
            or 0
        ),
        "fixed_even_mask_uniform_marginal_theorem_count": int(
            short_word_metrics.get(
                "fixed_even_mask_uniform_marginal_theorem_count",
                0,
            )
            or 0
        ),
        "non_diagonal_shared_generator_correlation_theorem_count": int(
            short_word_metrics.get(
                "non_diagonal_shared_generator_correlation_theorem_count",
                0,
            )
            or 0
        ),
        "mask_hypergraph_two_core_reduction_count": int(
            mask_hypergraph_metrics.get(
                "mask_hypergraph_two_core_reduction_count",
                0,
            )
            or 0
        ),
        "joint_two_core_anticoncentration_theorem_count": int(
            mask_hypergraph_metrics.get(
                "joint_two_core_anticoncentration_theorem_count",
                0,
            )
            or 0
        ),
        "subgroup_twirl_identity_theorem_count": int(
            subgroup_twirl_metrics.get(
                "subgroup_twirl_identity_theorem_count",
                0,
            )
            or 0
        ),
        "isotypic_partial_trace_reduction_theorem_count": int(
            subgroup_twirl_metrics.get(
                "isotypic_partial_trace_reduction_theorem_count",
                0,
            )
            or 0
        ),
        "uniform_partial_trace_delocalization_theorem_count": int(
            subgroup_twirl_metrics.get(
                "uniform_partial_trace_delocalization_theorem_count",
                0,
            )
            or 0
        ),
        "operator_valued_orbit_gram_fourier_theorem_count": int(
            orientation_fourier_metrics.get(
                "operator_valued_orbit_gram_fourier_theorem_count",
                0,
            )
            or 0
        ),
        "orientation_invariant_projector_decomposition_theorem_count": int(
            orientation_fourier_metrics.get(
                "orientation_invariant_projector_decomposition_theorem_count",
                0,
            )
            or 0
        ),
        "full_orientation_support_saturation_record_count": int(
            orientation_fourier_metrics.get(
                "full_orientation_support_saturation_record_count",
                0,
            )
            or 0
        ),
        "uniform_projector_sum_norm_theorem_count": int(
            orientation_fourier_metrics.get(
                "uniform_projector_sum_norm_theorem_count",
                0,
            )
            or 0
        ),
        "pairwise_character_convolution_theorem_count": int(
            orientation_fusion_metrics.get(
                "pairwise_character_convolution_theorem_count",
                0,
            )
            or 0
        ),
        "orientation_average_class_algebra_second_moment_theorem_count": int(
            orientation_fusion_metrics.get(
                "orientation_average_class_algebra_second_moment_theorem_count",
                0,
            )
            or 0
        ),
        "higher_orientation_moment_norm_theorem_count": int(
            orientation_fusion_metrics.get(
                "higher_orientation_moment_norm_theorem_count",
                0,
            )
            or 0
        ),
        "tail_log2_unresolved_kth_moment_interval_width": float(
            mixing_metrics.get(
                "tail_log2_unresolved_kth_moment_interval_width",
                0,
            )
            or 0
        ),
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
        "structured_maximal_effect_dilation_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return WreathSubPOVMMomentCertificateReport(
        created_at=utc_now(),
        theorem_contract={
            "exact_conclusive": (
                "q(B)=Tr(B^2)/(Tr(B)||B||) for a normalized-projector source "
                "block."
            ),
            "moment_certificate": (
                "q(B)>=Tr(B^2)/(Tr(B)Tr(B^p)^(1/p)) for integer p>=2."
            ),
            "factor_approximation": (
                "For support rank R, Tr(B^p)^(1/p)<=R^(1/p)||B||. "
                "Thus p>=log2(R) makes the certificate at least half exact."
            ),
            "scaling_scope": (
                "The full k-copy Hilbert dimension is an upper bound on R, so "
                "the recorded factor-two moment order is polynomial in n. "
                "Natural tuples are all unequal with probability 1-o(1), but "
                "computing the required growing moment on arbitrary "
                "all-unequal tuples is not yet polynomial."
            ),
            "source_average_reduction": (
                "At every order, natural normalized moments reduce exactly "
                "to identity and bridge-class subset word counts. A growing-"
                "order contraction and per-tuple concentration theorem remain "
                "open."
            ),
            "lazy_walk_boundary": (
                "The one-label word statistic mixes to 2/(n!)^2 with "
                "nonstationary eigenvalues at most 3/4. Projection domination "
                "gives the shared-generator kth walk the same constant gap, "
                "but rare equal one-dimensional sectors contaminate its "
                "unconditional high moment. The next theorem must condition "
                "the character kernel on all-unequal labels. That kernel is "
                "now exact and gives B<=I/2, but simultaneous contraction in "
                "all k active coordinates remains open. Global source "
                "collisions also vanish, so the remaining target can be "
                "restricted to globally distinct source partitions. Finite "
                "mixed-frame probes stay within a small constant factor of "
                "2^{1-k}. Unequal characters reduce to ordinary S_n ratios, "
                "and fixed-mask word marginals are uniform, but non-diagonal "
                "joint terms only reduce to dense incidence two-cores. Their "
                "anti-concentration and an all-n polynomial-factor bound are "
                "open."
            ),
            "implementation_boundary": (
                "A success certificate does not synthesize the maximal-effect "
                "Naimark dilation or decode its permutation outcome."
            ),
        },
        finite_certificates=certificates,
        scaling_requirements=scaling,
        headline_metrics=metrics,
        claim_gate={
            "moment_certificate_theorem_proved": True,
            "finite_natural_w3_conclusive_signal_certified": True,
            "required_moment_order_polynomial_in_n": True,
            "natural_equal_sector_asymptotically_bypassed": bool(
                metrics[
                    "natural_source_equal_sector_bypass_theorem_count"
                ]
            ),
            "all_sector_growing_order_contraction_proved": False,
            "growing_order_all_unequal_contraction_proved": False,
            "all_order_natural_word_map_reduction_proved": bool(
                metrics["all_order_natural_word_map_reduction_count"]
            ),
            "growing_order_word_map_contraction_proved": False,
            "natural_tuple_moment_concentration_proved": False,
            "single_walk_mean_mixing_proved": bool(
                metrics["single_walk_mean_mixing_theorem_count"]
            ),
            "coupled_k_walk_contraction_proved": bool(
                metrics["coupled_k_walk_contraction_count"]
            ),
            "typical_all_unequal_conditioned_kernel_derived": bool(
                metrics["typical_all_unequal_conditioned_kernel_count"]
            ),
            "all_unequal_frame_half_norm_bound_proved": bool(
                metrics["all_unequal_frame_half_norm_bound_count"]
            ),
            "simultaneous_k_coordinate_contraction_proved": bool(
                metrics["simultaneous_k_coordinate_contraction_count"]
            ),
            "asymptotic_global_source_distinctness_proved": bool(
                metrics[
                    "asymptotic_global_all_distinct_dominance_theorem_count"
                ]
            ),
            "collision_free_growing_moment_contraction_proved": bool(
                metrics["collision_free_growing_moment_contraction_count"]
            ),
            "collision_free_polynomial_factor_norm_bound_proved": bool(
                metrics[
                    "collision_free_polynomial_factor_norm_theorem_count"
                ]
            ),
            "joint_short_word_anticoncentration_proved": bool(
                metrics[
                    "joint_short_word_anticoncentration_theorem_count"
                ]
            ),
            "mask_hypergraph_two_core_reduction_proved": bool(
                metrics["mask_hypergraph_two_core_reduction_count"]
            ),
            "joint_two_core_anticoncentration_proved": bool(
                metrics[
                    "joint_two_core_anticoncentration_theorem_count"
                ]
            ),
            "subgroup_twirl_identity_proved": bool(
                metrics["subgroup_twirl_identity_theorem_count"]
            ),
            "isotypic_partial_trace_reduction_proved": bool(
                metrics[
                    "isotypic_partial_trace_reduction_theorem_count"
                ]
            ),
            "uniform_partial_trace_delocalization_proved": bool(
                metrics[
                    "uniform_partial_trace_delocalization_theorem_count"
                ]
            ),
            "operator_valued_orbit_gram_fourier_reduction_proved": bool(
                metrics[
                    "operator_valued_orbit_gram_fourier_theorem_count"
                ]
            ),
            "orientation_projector_decomposition_proved": bool(
                metrics[
                    "orientation_invariant_projector_decomposition_theorem_count"
                ]
            ),
            "orientation_support_saturation_observed": bool(
                metrics[
                    "full_orientation_support_saturation_record_count"
                ]
            ),
            "uniform_projector_sum_norm_bound_proved": bool(
                metrics["uniform_projector_sum_norm_theorem_count"]
            ),
            "pairwise_character_convolution_proved": bool(
                metrics["pairwise_character_convolution_theorem_count"]
            ),
            "orientation_average_second_moment_proved": bool(
                metrics[
                    "orientation_average_class_algebra_second_moment_theorem_count"
                ]
            ),
            "higher_orientation_moment_norm_bound_proved": bool(
                metrics["higher_orientation_moment_norm_theorem_count"]
            ),
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "structured_maximal_effect_dilation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "High-order moments can certify the desired conclusive rate "
                "without diagonalizing the frame. The unconditional coupled "
                "walk now has a constant gap and the conditioned all-unequal "
                "kernel is exact and global source collisions vanish, but no "
                "all-n collision-free polynomial-factor norm theorem, "
                "simultaneous contraction, or maximal-effect circuit exists."
            ),
        },
        status=(
            "subpovm-moment-certificate-natural-unequal-"
            "growing-contraction-open"
        ),
        summary=(
            "Converted wreath frame moments into rigorous projector-sub-POVM "
            f"success certificates on {len(occupied)} naturally occupied W_3 "
            "blocks. Order four certifies "
            f"{order_four.certified_natural_average_conclusive_lower_bound:.6g} "
            "average conclusive probability. Natural equal sectors vanish "
            "asymptotically; growing-order contraction on arbitrary "
            "all-unequal tuples remains open."
        ),
        falsifiers_triggered=[
            (
                "First and second moments alone need not tightly estimate the "
                "frame operator norm."
            ),
            (
                "Finite fourth and sixteenth moments certify substantial "
                "natural W_3 conclusive probability without a condition-number "
                "fit."
            ),
            (
                "Natural all-unequal dominance removes mixed equal-sector "
                "recoupling from the asymptotic critical path."
            ),
            (
                "Character orthogonality removes the physical-irrep sum at "
                "all orders but leaves an exponential subset word-map count "
                "and a source-tuple concentration gap."
            ),
            (
                "Projection domination closes the shared-generator spectral-"
                "gap question but its unconditional moment is contaminated "
                "by rare equal one-dimensional sectors."
            ),
            (
                "Polynomial moment order does not imply polynomial contraction "
                "on arbitrary all-unequal physical source tuples."
            ),
            (
                "A trace-moment success proof is not a Naimark dilation, "
                "permutation decoder, or classical separation."
            ),
        ],
    )


def write_wreath_subpovm_moment_certificate_report(
    output_path: Path = REPORT_PATH,
    *,
    moment_orders: tuple[int, ...] = (2, 3, 4, 8, 16),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(
        build_wreath_subpovm_moment_certificate_report(
            moment_orders=moment_orders
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_wreath_subpovm_moment_certificate_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
