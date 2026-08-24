"""Sector-resolved no-go theorem for global branch-polar whitening.

The raw/polar matched-filter theorem bounded the correction from global polar
whitening by ``kappa R``.  That global operator-norm estimate left open a
large-concentration escape on low-dimensional Fourier sectors.  The central
raw-concentration theorem identified the exact sector multiplier and makes a
sharper, dimension-cancelling argument possible.

Let ``C_J`` be the branch-polar relative convolution, ``C_K`` the native raw
convolution, and ``Q=polar(C_J)``.  In Fourier sector ``nu`` of dimension
``d_nu``, write their normalized multipliers as ``M_J,nu`` and ``M_K,nu`` and

    E_nu = polar(M_J,nu)-M_J,nu.

For any two equivariant convolutions, the common correct-label block is the
identity Fourier coefficient

    A = |G|^-1 sum_nu d_nu Tr_(V_nu)(M_L,nu^* M_R,nu).    (1)

The exact central raw bridge gives

    M_K,nu^* M_K,nu
      = |G|/d_nu^2 I_(d_nu) tensor Q_nu,
    0 <= Q_nu <= I.                                      (2)

Define the sector whitening-correction amplitude

    A_E,nu = d_nu/|G| Tr_(V_nu)(E_nu^* M_K,nu)

and the sector polar-distance contribution

    r_nu = d_nu ||E_nu||_F^2/(|G|D).

The Hilbert--Schmidt partial-trace inequality and (2) cancel every Fourier
dimension exactly:

    ||A_E,nu||_F^2/D <= r_nu.                             (3)

There are only ``p(n)`` irreps of ``S_n``.  Minkowski followed by Cauchy gives

    P_E = ||sum_nu A_E,nu||_F^2/D
        <= p(n) sum_nu r_nu
        <= p(n) R,                                       (4)

where ``R=||C_J^*C_J-I||_F^2/(|G|D)``; the final inequality follows from
``||polar(M)-M||_F^2<=||M^*M-I||_F^2`` sector by sector.

The unwhitened matched-filter theorem gives

    P_match <= overlap(C_J,C_K).

Therefore the globally whitened correct probability obeys the pointwise
portfolio bound

    P_Q <= (sqrt(overlap)+sqrt(p(n)R))^2.                 (5)

For independent two-Plancherel source pairs at
``k=ceil(3 log_2(n!))+2``, the predecessor theorems prove

    E overlap <= (n+1)2^(-n/4)+gamma^k,
    E R <= (n!-1)(3/4)^k.

Since ``p(n)=exp(O(sqrt(n)))``, equation (5), Cauchy--Schwarz, and the
global-distinct conditioning theorem imply ``E[P_Q | distinct]=o(1)`` and
source-typical ``P_Q=o(1)``.  Thus neither low-sector concentration nor
cross-sector coherent cancellation rescues this specific branch-polar
decoder.

This is not a lower bound for arbitrary circuits or the actual physical PGM.
It rejects only ``polar(C_J)^*`` applied to the native raw coherent ensemble.
A new route must change the physical analysis operator, the state preparation,
or the multiplicity whitening rather than further optimize this polar field.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_branch_character_gpe_dilation_separation import GAMMA
from self_dual_wreath_branch_character_naimark_autocorrelation_fourier_boundary import (
    nonabelian_fourier_multiplier,
)
from self_dual_wreath_branch_character_polar_naimark_completion import (
    Label,
    candidate_relative_convolution,
)
from self_dual_wreath_branch_character_raw_concentration_central_fourier_bridge import (
    central_compressed_isotypic_block,
)
from self_dual_wreath_branch_character_raw_polar_matched_filter_boundary import (
    _canonical_partial_polar,
    raw_candidate_relative_convolution,
)
from self_dual_wreath_joint_character_natural_sector_mass import partition_number
from self_dual_wreath_orientation_fourier_reduction import _w4_collision_free_labels


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_sector_resolved_whitening_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-SECTOR-RESOLVED-"
    "WHITENING-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SectorWhiteningCorrectionControl:
    partition: tuple[int, ...]
    irrep_dimension: int
    raw_multiplier_concentration: float
    central_raw_concentration_upper_bound: float
    central_raw_bound_residual: float
    polar_distance_contribution: float
    correction_amplitude_success: float
    correction_below_polar_distance_contribution: bool
    correction_bound_residual: float
    status: str


@dataclass(frozen=True)
class SectorResolvedWhiteningControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    group_order: int
    partition_count: int
    carrier_dimension: int
    direct_whitened_correct_success: float
    reconstructed_whitened_correct_success: float
    whitened_reconstruction_residual: float
    unwhitened_matched_filter_success: float
    reconstructed_matched_filter_success: float
    matched_reconstruction_residual: float
    normalized_raw_polar_overlap: float
    matched_success_below_overlap: bool
    direct_correction_success: float
    reconstructed_correction_success: float
    correction_reconstruction_residual: float
    direct_polar_distance_residual: float
    polar_distance_residual: float
    polar_distance_parseval_residual: float
    direct_polar_gram_residual: float
    polar_gram_residual: float
    polar_gram_parseval_residual: float
    polar_distance_below_gram_residual: bool
    partition_times_polar_distance_bound: float
    correction_below_partition_times_distance: bool
    partition_times_gram_success_bound: float
    whitened_success_bound_verified: bool
    exact_sector_resolved_whitening_no_go_verified: bool
    sector_controls: list[SectorWhiteningCorrectionControl]
    status: str


@dataclass(frozen=True)
class NaturalWhiteningNoGoScaling:
    n: int
    log2_group_order: float
    copy_count: int
    partition_count_decimal: str
    raw_polar_overlap_upper_bound: float
    log2_expected_polar_gram_residual_upper_bound: float
    log2_partition_weighted_correction_upper_bound: float
    expected_whitened_success_upper_bound: float
    global_distinct_conditioning_probability_tends_to_one: bool
    conditioned_expected_whitened_success_tends_to_zero: bool
    source_typical_whitened_success_tends_to_zero: bool
    status: str


@dataclass(frozen=True)
class SectorResolvedWhiteningNoGoTheorem:
    correct_block_fourier_inversion: str
    central_raw_multiplier: str
    sector_dimension_cancellation: str
    partition_count_sum: str
    pointwise_success_bound: str
    natural_source_consequence: str
    route_decision: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SectorResolvedWhiteningNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SectorResolvedWhiteningNoGoTheorem
    finite_controls: list[SectorResolvedWhiteningControl]
    scaling_records: list[NaturalWhiteningNoGoScaling]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _partial_trace_irrep(
    matrix: np.ndarray,
    irrep_dimension: int,
    carrier_dimension: int,
) -> np.ndarray:
    expected = irrep_dimension * carrier_dimension
    if matrix.shape != (expected, expected):
        raise ValueError("matrix has incompatible irrep/carrier dimensions")
    tensor = matrix.reshape(
        irrep_dimension,
        carrier_dimension,
        irrep_dimension,
        carrier_dimension,
    )
    return sum(
        tensor[index, :, index, :]
        for index in range(irrep_dimension)
    )


def sector_correct_amplitude(
    left_multiplier: np.ndarray,
    right_multiplier: np.ndarray,
    *,
    irrep_dimension: int,
    carrier_dimension: int,
    group_order: int,
) -> np.ndarray:
    """Return one sector's contribution to the common diagonal block."""

    product = left_multiplier.conj().T @ right_multiplier
    return (
        irrep_dimension
        / group_order
        * _partial_trace_irrep(product, irrep_dimension, carrier_dimension)
    )


def _first_diagonal_block(
    matrix: np.ndarray,
    carrier_dimension: int,
) -> np.ndarray:
    return matrix[:carrier_dimension, :carrier_dimension]


def audit_sector_resolved_whitening(
    control_id: str,
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-9,
) -> SectorResolvedWhiteningControl:
    polar_convolution, group, polar_fields = candidate_relative_convolution(labels)
    raw_convolution, raw_group, raw_fields = raw_candidate_relative_convolution(labels)
    if group != raw_group:
        raise ArithmeticError("raw and polar fields enumerate different groups")
    order = len(group)
    n = len(group[0])
    carrier = next(iter(polar_fields.values())).shape[1]
    partitions = tuple(integer_partitions(n))

    whitened_convolution = _canonical_partial_polar(polar_convolution, tolerance)
    direct_whitened_block = _first_diagonal_block(
        whitened_convolution.conj().T @ raw_convolution,
        carrier,
    )
    direct_matched_block = _first_diagonal_block(
        polar_convolution.conj().T @ raw_convolution,
        carrier,
    )
    direct_correction_block = direct_whitened_block - direct_matched_block

    whitened_parts: list[np.ndarray] = []
    matched_parts: list[np.ndarray] = []
    correction_parts: list[np.ndarray] = []
    sectors: list[SectorWhiteningCorrectionControl] = []
    distance_sum = 0.0
    gram_sum = 0.0

    for target in partitions:
        dimension = hook_length_dimension(target)
        polar_multiplier = nonabelian_fourier_multiplier(
            target,
            group,
            polar_fields,
        )
        raw_multiplier = nonabelian_fourier_multiplier(
            target,
            group,
            raw_fields,
        )
        whitened_multiplier = _canonical_partial_polar(
            polar_multiplier,
            tolerance,
        )
        correction_multiplier = whitened_multiplier - polar_multiplier

        whitened_part = sector_correct_amplitude(
            whitened_multiplier,
            raw_multiplier,
            irrep_dimension=dimension,
            carrier_dimension=carrier,
            group_order=order,
        )
        matched_part = sector_correct_amplitude(
            polar_multiplier,
            raw_multiplier,
            irrep_dimension=dimension,
            carrier_dimension=carrier,
            group_order=order,
        )
        correction_part = sector_correct_amplitude(
            correction_multiplier,
            raw_multiplier,
            irrep_dimension=dimension,
            carrier_dimension=carrier,
            group_order=order,
        )
        whitened_parts.append(whitened_part)
        matched_parts.append(matched_part)
        correction_parts.append(correction_part)

        central = central_compressed_isotypic_block(target, labels)
        central_top = float(np.linalg.eigvalsh(central)[-1])
        raw_concentration = float(
            np.linalg.svd(raw_multiplier, compute_uv=False)[0] ** 2
        )
        central_bound = order / dimension**2 * max(0.0, central_top)
        central_residual = max(0.0, raw_concentration - central_bound)
        distance_contribution = float(
            dimension
            * np.linalg.norm(correction_multiplier, ord="fro") ** 2
            / (order * carrier)
        )
        gram = polar_multiplier.conj().T @ polar_multiplier
        gram_contribution = float(
            dimension
            * np.linalg.norm(
                gram - np.eye(gram.shape[0], dtype=complex),
                ord="fro",
            )
            ** 2
            / (order * carrier)
        )
        correction_success = float(
            np.linalg.norm(correction_part, ord="fro") ** 2 / carrier
        )
        bound_residual = max(0.0, correction_success - distance_contribution)
        correction_bound = correction_success <= (
            distance_contribution + 1000 * tolerance
        )
        verified = bool(
            central_residual <= 1000 * tolerance
            and correction_bound
            and distance_contribution <= gram_contribution + 1000 * tolerance
        )
        distance_sum += distance_contribution
        gram_sum += gram_contribution
        sectors.append(
            SectorWhiteningCorrectionControl(
                partition=target,
                irrep_dimension=dimension,
                raw_multiplier_concentration=raw_concentration,
                central_raw_concentration_upper_bound=central_bound,
                central_raw_bound_residual=central_residual,
                polar_distance_contribution=distance_contribution,
                correction_amplitude_success=correction_success,
                correction_below_polar_distance_contribution=correction_bound,
                correction_bound_residual=bound_residual,
                status=(
                    "sector-dimension-cancellation-verified"
                    if verified
                    else "sector-whitening-correction-control-failure"
                ),
            )
        )

    reconstructed_whitened = sum(
        whitened_parts,
        np.zeros((carrier, carrier), dtype=complex),
    )
    reconstructed_matched = sum(
        matched_parts,
        np.zeros((carrier, carrier), dtype=complex),
    )
    reconstructed_correction = sum(
        correction_parts,
        np.zeros((carrier, carrier), dtype=complex),
    )
    whitened_reconstruction_residual = float(
        np.linalg.norm(reconstructed_whitened - direct_whitened_block, ord="fro")
    )
    matched_reconstruction_residual = float(
        np.linalg.norm(reconstructed_matched - direct_matched_block, ord="fro")
    )
    correction_reconstruction_residual = float(
        np.linalg.norm(
            reconstructed_correction - direct_correction_block,
            ord="fro",
        )
    )

    whitened_success = float(
        np.linalg.norm(direct_whitened_block, ord="fro") ** 2 / carrier
    )
    reconstructed_whitened_success = float(
        np.linalg.norm(reconstructed_whitened, ord="fro") ** 2 / carrier
    )
    matched_success = float(
        np.linalg.norm(direct_matched_block, ord="fro") ** 2 / carrier
    )
    reconstructed_matched_success = float(
        np.linalg.norm(reconstructed_matched, ord="fro") ** 2 / carrier
    )
    correction_success = float(
        np.linalg.norm(direct_correction_block, ord="fro") ** 2 / carrier
    )
    reconstructed_correction_success = float(
        np.linalg.norm(reconstructed_correction, ord="fro") ** 2 / carrier
    )
    overlap = float(
        np.trace(polar_convolution.conj().T @ raw_convolution).real
        / (order * carrier)
    )
    matched_below_overlap = matched_success <= overlap + 1000 * tolerance
    distance_below_gram = distance_sum <= gram_sum + 1000 * tolerance
    direct_distance = float(
        np.linalg.norm(
            whitened_convolution - polar_convolution,
            ord="fro",
        )
        ** 2
        / (order * carrier)
    )
    identity = np.eye(order * carrier, dtype=complex)
    direct_gram = float(
        np.linalg.norm(
            polar_convolution.conj().T @ polar_convolution - identity,
            ord="fro",
        )
        ** 2
        / (order * carrier)
    )
    distance_parseval_residual = abs(direct_distance - distance_sum)
    gram_parseval_residual = abs(direct_gram - gram_sum)
    partition_distance_bound = len(partitions) * distance_sum
    correction_below_partition = correction_success <= (
        partition_distance_bound + 1000 * tolerance
    )
    success_bound = (
        math.sqrt(max(0.0, overlap))
        + math.sqrt(max(0.0, len(partitions) * gram_sum))
    ) ** 2
    success_bound_verified = whitened_success <= success_bound + 1000 * tolerance
    verified = bool(
        all(row.status == "sector-dimension-cancellation-verified" for row in sectors)
        and whitened_reconstruction_residual <= 1000 * tolerance
        and matched_reconstruction_residual <= 1000 * tolerance
        and correction_reconstruction_residual <= 1000 * tolerance
        and matched_below_overlap
        and distance_parseval_residual <= 1000 * tolerance
        and gram_parseval_residual <= 1000 * tolerance
        and distance_below_gram
        and correction_below_partition
        and success_bound_verified
    )
    return SectorResolvedWhiteningControl(
        control_id=control_id,
        n=n,
        labels=labels,
        group_order=order,
        partition_count=len(partitions),
        carrier_dimension=carrier,
        direct_whitened_correct_success=whitened_success,
        reconstructed_whitened_correct_success=reconstructed_whitened_success,
        whitened_reconstruction_residual=whitened_reconstruction_residual,
        unwhitened_matched_filter_success=matched_success,
        reconstructed_matched_filter_success=reconstructed_matched_success,
        matched_reconstruction_residual=matched_reconstruction_residual,
        normalized_raw_polar_overlap=overlap,
        matched_success_below_overlap=matched_below_overlap,
        direct_correction_success=correction_success,
        reconstructed_correction_success=reconstructed_correction_success,
        correction_reconstruction_residual=correction_reconstruction_residual,
        direct_polar_distance_residual=direct_distance,
        polar_distance_residual=distance_sum,
        polar_distance_parseval_residual=distance_parseval_residual,
        direct_polar_gram_residual=direct_gram,
        polar_gram_residual=gram_sum,
        polar_gram_parseval_residual=gram_parseval_residual,
        polar_distance_below_gram_residual=distance_below_gram,
        partition_times_polar_distance_bound=partition_distance_bound,
        correction_below_partition_times_distance=correction_below_partition,
        partition_times_gram_success_bound=success_bound,
        whitened_success_bound_verified=success_bound_verified,
        exact_sector_resolved_whitening_no_go_verified=verified,
        sector_controls=sectors,
        status=(
            "exact-sector-resolved-whitening-boundary"
            if verified
            else "sector-resolved-whitening-control-failure"
        ),
    )


def natural_whitening_no_go_scaling(n: int) -> NaturalWhiteningNoGoScaling:
    if n < 4:
        raise ValueError("n must be at least four")
    log_order = math.log2(math.factorial(n))
    copies = math.ceil(3.0 * log_order) + 2
    count = partition_number(n)

    low_order_log = math.log2(n + 1) - n / 4.0
    gamma_log = copies * math.log2(GAMMA)
    low_order = 2.0**low_order_log if low_order_log > -1074 else 0.0
    gamma_term = 2.0**gamma_log if gamma_log > -1074 else 0.0
    overlap = min(1.0, low_order + gamma_term)

    inverse_order = 2.0**(-log_order) if log_order < 1074 else 0.0
    log_order_minus_one = log_order + math.log2(1.0 - inverse_order)
    gram_log = log_order_minus_one + copies * math.log2(3.0 / 4.0)
    weighted_log = math.log2(count) + gram_log
    weighted = 2.0**weighted_log if weighted_log > -1074 else 0.0
    upper = (math.sqrt(overlap) + math.sqrt(weighted)) ** 2
    tends_to_zero = weighted_log < 0
    return NaturalWhiteningNoGoScaling(
        n=n,
        log2_group_order=log_order,
        copy_count=copies,
        partition_count_decimal=str(count),
        raw_polar_overlap_upper_bound=overlap,
        log2_expected_polar_gram_residual_upper_bound=gram_log,
        log2_partition_weighted_correction_upper_bound=weighted_log,
        expected_whitened_success_upper_bound=upper,
        global_distinct_conditioning_probability_tends_to_one=True,
        conditioned_expected_whitened_success_tends_to_zero=tends_to_zero,
        source_typical_whitened_success_tends_to_zero=tends_to_zero,
        status=(
            "natural-branch-polar-whitened-success-vanishes"
            if tends_to_zero
            else "asymptotic-whitening-no-go-not-yet-visible"
        ),
    )


def run_sector_resolved_whitening_no_go() -> SectorResolvedWhiteningNoGoReport:
    controls = [
        audit_sector_resolved_whitening(
            "S3-SINGLE-PAIR-SECTOR-WHITENING",
            (((3,), (2, 1)),),
        ),
        audit_sector_resolved_whitening(
            "S3-THRESHOLD-SECTOR-WHITENING",
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
        audit_sector_resolved_whitening(
            "S4-COLLISION-FREE-SECTOR-WHITENING",
            _w4_collision_free_labels()[0],
        ),
    ]
    scaling = [natural_whitening_no_go_scaling(n) for n in (32, 64, 128, 256, 512)]
    verified = bool(
        all(row.exact_sector_resolved_whitening_no_go_verified for row in controls)
        and scaling[-1].conditioned_expected_whitened_success_tends_to_zero
        and scaling[-1].expected_whitened_success_upper_bound < 0.01
    )
    theorem = SectorResolvedWhiteningNoGoTheorem(
        correct_block_fourier_inversion=(
            "A=|G|^-1 sum_nu d_nu Tr_(V_nu)(M_L,nu^*M_R,nu) for the "
            "common diagonal block of equivariant convolutions."
        ),
        central_raw_multiplier=(
            "M_K,nu^*M_K,nu=|G|/d_nu^2 I tensor Q_nu with 0<=Q_nu<=I."
        ),
        sector_dimension_cancellation=(
            "For A_E,nu=d_nu/|G| Tr_(V_nu)(E_nu^*M_K,nu), "
            "||A_E,nu||_F^2/D<=d_nu||E_nu||_F^2/(|G|D)=r_nu."
        ),
        partition_count_sum=(
            "Minkowski and Cauchy over the p(n) irreps give P_E<=p(n)R."
        ),
        pointwise_success_bound=(
            "P_polar<=[sqrt(raw/polar overlap)+sqrt(p(n)R)]^2."
        ),
        natural_source_consequence=(
            "At k=ceil(3log2(n!))+2, annealed and globally-distinct conditioned "
            "success vanish; Markov gives source-typical failure."
        ),
        route_decision=(
            "Low-sector concentration and coherent cross-sector cancellation do not "
            "rescue polar(C_J)^* on the native raw ensemble."
        ),
        scope=(
            "This terminates the branch-polar whitening decoder, not arbitrary "
            "circuits, alternate state preparations, or the physical multiplicity PGM."
        ),
        theorem_verified=verified,
        status=(
            "natural-branch-polar-global-whitening-asymptotically-rejected"
            if verified
            else "sector-resolved-whitening-no-go-control-failure"
        ),
    )
    tail = scaling[-1]
    return SectorResolvedWhiteningNoGoReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "resolve_low_sector_coherent_alignment_escape",
                "resolved": verified,
                "resolution": (
                    "Sector Fourier inversion and the exact d_nu^-2 raw multiplier "
                    "bound reduce every correction amplitude to its polar-distance mass."
                ),
            },
            {
                "obligation": "remove_global_raw_concentration_from_whitening_bound",
                "resolved": verified,
                "resolution": (
                    "The new bound pays only the number p(n) of Fourier sectors, not "
                    "max_nu ||M_K,nu||^2."
                ),
            },
            {
                "obligation": "decide_branch_polar_global_whitening_route",
                "resolved": verified,
                "resolution": (
                    "Its natural correct probability vanishes at the proved copy scale."
                ),
            },
            {
                "obligation": "analyze_actual_joint_character_multiplicity_PGM",
                "resolved": False,
                "resolution": (
                    "The physical PGM uses D_nu^-1/2 after discarding the carrier and "
                    "is not identified with polar(C_J)^*."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A tiny low-dimensional mass can coherently cancel a large high-sector matched amplitude.",
                "resolved": True,
                "resolution": (
                    "The proof bounds the whitening correction before sectors interfere. "
                    "Each sector costs r_nu, and coherent summation costs only p(n)."
                ),
            },
            {
                "objection": "The global raw norm may be factorial, invalidating the correction bound.",
                "resolved": True,
                "resolution": (
                    "The exact |G|/d_nu^2 factor cancels the Fourier inversion and "
                    "partial-trace dimensions sector by sector. No global kappa appears."
                ),
            },
            {
                "objection": "Frobenius near-isometry alone gives an operator-norm decoder theorem.",
                "resolved": True,
                "resolution": (
                    "Not in general. The conclusion additionally uses equivariant Fourier "
                    "inversion and the exact central raw multiplier bound."
                ),
            },
            {
                "objection": "Failure of this purified branch-polar decoder rejects the physical PGM.",
                "resolved": False,
                "resolution": (
                    "No. The physical multiplicity inverse is a different analysis map."
                ),
            },
        ],
        headline_metrics={
            "sector_correct_block_inversion_theorem_count": int(verified),
            "sector_dimension_cancellation_theorem_count": int(verified),
            "global_branch_polar_whitening_no_go_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_sector_resolved_whitening_no_go_verified
                for row in controls
            ),
            "tail_n": tail.n,
            "tail_log2_partition_weighted_correction_upper_bound": (
                tail.log2_partition_weighted_correction_upper_bound
            ),
            "tail_expected_whitened_success_upper_bound": (
                tail.expected_whitened_success_upper_bound
            ),
            "actual_physical_pgm_no_go_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "sector_correct_block_fourier_formula_proved": verified,
            "low_sector_coherent_alignment_escape_closed": verified,
            "global_raw_concentration_escape_closed": verified,
            "natural_branch_polar_whitened_decoder_success_vanishes": verified,
            "branch_polar_whitened_decoder_rejected": verified,
            "actual_physical_pgm_rejected": False,
            "alternate_multiplicity_whitening_rejected": False,
            "arbitrary_circuit_lower_bound_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Resolved the last concentration escape for the branch-polar decoder. "
            "Fourier-sector dimension cancellation replaces the global kappa R bound "
            "by p(n)R, proving natural global-whitening success vanishes. The actual "
            "joint-character multiplicity PGM remains the next distinct route."
        ),
        falsifiers_triggered=[
            "Factorial raw operator concentration cannot rescue this decoder after sector-resolved Fourier inversion.",
            "The vanishing-mass low-dimensional tail cannot create a constant whitening correction through coherent sector summation.",
            "Further optimization of polar(C_J)^* is deprioritized; progress requires a different physical analysis map.",
        ],
    )


def write_sector_resolved_whitening_no_go_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_sector_resolved_whitening_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_sector_resolved_whitening_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
