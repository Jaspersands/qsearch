"""Walsh duality for the complete component commutator fourth moment.

Let ``{H_x : x in F_2^m}`` be a Hermitian leaf POVM, ``q=2^m``, and

    A_S = sum_x chi_S(x) H_x.

Walsh orthogonality applied separately to the two outcome indices gives the
deterministic identity

    M4(H)
      = sum_(x,y) [Tr(H_x^2 H_y^2)-Tr(H_x H_y H_x H_y)]
      = q^-2 sum_(S,T)
          [Tr(A_S^2 A_T^2)-Tr(A_S A_T A_S A_T)].         (1)

Every summand on the right is

    G(S,T)=1/2 ||[A_S,A_T]||_F^2 >= 0.                   (2)

Thus ``M4/r`` is exactly the mean normalized commutator gap for two uniform
Walsh masks.  There is no diagonal/crossing cancellation left to control.

For a coordinate-compression POVM ``H_x=W^*D_xW``, let ``P=WW^*`` and
``Z_S=sum_x chi_S(x)D_x``.  Then

    A_S = W^* Z_S W,
    [PZ_SP,PZ_TP]
      = P Z_T(I-P)Z_S P - P Z_S(I-P)Z_T P.               (3)

The ambient block-sign involutions commute.  Their compressed commutator is
exactly a phase-sensitive curl through the complement of the dependency
projection.  This identifies a representation-specific object not visible to
unsigned block-overlap or Gershgorin bounds.

Under the natural source-pair permutation symmetry, the annealed gap for
``(S,T)`` depends only on the four cell counts

    c_ab = |{j : (1_S(j),1_T(j))=(a,b)}|.

Consequently the ``q^2=4^m`` pair average has exactly
``binom(m+3,3)=O(m^3)`` strata with multinomial weights.  Equivalently, the
stratum law is the four-cell occupancy law of two independent uniform masks.
A positive lower bound on a constant-probability set of typical strata would
prove natural M4 directly.

This is an exact reduction, not such a lower bound.  The dependency projection
can commute with every ``Z_S`` (orthogonal PVM control), and finite repeated
labels do not establish a typical Plancherel parity-curl gap.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_leaf_fourier_leverage import (
    _coarse_pvm,
    _uniform_povm,
    _validate_povm,
    walsh_fourier_coefficients,
)
from self_dual_wreath_component_leaf_fourier_strata import (
    _haar_block_povm,
    _natural_effects,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_leaf_fourier_commutator_duality.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-COMMUTATOR-DUALITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FourierCommutatorStratum:
    cell_counts_00_01_10_11: tuple[int, int, int, int]
    representative_masks: tuple[int, int]
    pair_multiplicity: int
    enumerated_pair_count: int
    orbit_averaged_normalized_gap: float
    weighted_normalized_gap: float
    exact_multinomial_count_verified: bool
    status: str


@dataclass(frozen=True)
class FourierCommutatorDualityControl:
    control_id: str
    profile_kind: str
    cube_dimension: int
    leaf_count: int
    fiber_dimension: int
    leaf_pair_count: int
    fourier_pair_count: int
    observed_pair_stratum_count: int
    predicted_pair_stratum_count: int
    direct_normalized_component_M4: float
    fourier_dual_normalized_component_M4: float
    strata_reconstructed_normalized_component_M4: float
    maximum_negative_fourier_pair_gap: float
    maximum_pair_gap_to_half_commutator_residual: float
    fourier_duality_residual: float
    stratum_reconstruction_residual: float
    maximum_stratum_multinomial_residual: int
    exact_fourier_commutator_duality_verified: bool
    positive_component_M4_in_control: bool
    status: str


@dataclass(frozen=True)
class FourierCommutatorScalingRecord:
    cube_dimension: int
    leaf_pair_count_log2: int
    exact_pair_stratum_count: int
    log2_pair_stratum_count: float
    pair_stratum_polynomial_degree: int
    typical_cell_lower_count: int
    typical_cell_upper_count: int
    typical_four_cell_mass_lower_bound: float
    constant_typical_stratum_gap_would_prove_constant_M4: bool
    natural_typical_parity_gap_proved: bool
    status: str


@dataclass(frozen=True)
class FourierCommutatorDualityTheorem:
    deterministic_duality: str
    positive_pair_gap: str
    coordinate_compression: str
    parity_leakage_curl: str
    annealed_stratum_count: str
    typical_stratum_implication: str
    arbitrary_hermitian_povm: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentLeafFourierCommutatorDualityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FourierCommutatorDualityTheorem
    finite_controls: list[FourierCommutatorDualityControl]
    scaling_records: list[FourierCommutatorScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _pair_gap(left: np.ndarray, right: np.ndarray) -> float:
    return float(
        np.trace(
            left @ left @ right @ right
            - left @ right @ left @ right
        ).real
    )


def _half_commutator_square(left: np.ndarray, right: np.ndarray) -> float:
    commutator = left @ right - right @ left
    return float(np.linalg.norm(commutator, ord="fro") ** 2 / 2.0)


def _pair_cell_counts(
    left: int,
    right: int,
    cube_dimension: int,
) -> tuple[int, int, int, int]:
    counts = [0] * 4
    for coordinate in range(cube_dimension):
        pattern = (
            ((left >> coordinate) & 1) << 1
            | ((right >> coordinate) & 1)
        )
        counts[pattern] += 1
    return counts[0], counts[1], counts[2], counts[3]


def _pair_representative(
    counts: tuple[int, int, int, int],
) -> tuple[int, int]:
    if len(counts) != 4 or any(count < 0 for count in counts):
        raise ValueError("four nonnegative pair-cell counts are required")
    left = 0
    right = 0
    coordinate = 0
    for pattern, count in enumerate(counts):
        for _ in range(count):
            left |= ((pattern >> 1) & 1) << coordinate
            right |= (pattern & 1) << coordinate
            coordinate += 1
    return left, right


def _pair_multinomial(counts: tuple[int, int, int, int]) -> int:
    output = math.factorial(sum(counts))
    for count in counts:
        output //= math.factorial(count)
    return output


def audit_fourier_commutator_duality(
    control_id: str,
    profile_kind: str,
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> FourierCommutatorDualityControl:
    m, r, _, _ = _validate_povm(effects, tolerance=tolerance)
    q = 1 << m
    coefficients = walsh_fourier_coefficients(effects, tolerance=tolerance)
    direct = 0.0
    for left in effects:
        for right in effects:
            direct += _pair_gap(left, right)
    groups: dict[tuple[int, int, int, int], list[float | int]] = {}
    fourier_sum = 0.0
    maximum_negative = 0.0
    maximum_commutator_residual = 0.0
    for left_mask, left in enumerate(coefficients):
        for right_mask, right in enumerate(coefficients):
            gap = _pair_gap(left, right)
            half_square = _half_commutator_square(left, right)
            maximum_negative = max(maximum_negative, max(0.0, -gap))
            maximum_commutator_residual = max(
                maximum_commutator_residual,
                abs(gap - half_square),
            )
            fourier_sum += gap
            key = _pair_cell_counts(left_mask, right_mask, m)
            if key not in groups:
                groups[key] = [0, 0.0]
            groups[key][0] += 1
            groups[key][1] += gap / r
    rows = []
    strata_sum = 0.0
    maximum_count_residual = 0
    for counts, values in sorted(groups.items()):
        enumerated = int(values[0])
        normalized_sum = float(values[1])
        multiplicity = _pair_multinomial(counts)
        average = normalized_sum / enumerated
        weighted = multiplicity * average
        strata_sum += weighted
        residual = abs(enumerated - multiplicity)
        maximum_count_residual = max(maximum_count_residual, residual)
        rows.append(
            FourierCommutatorStratum(
                cell_counts_00_01_10_11=counts,
                representative_masks=_pair_representative(counts),
                pair_multiplicity=multiplicity,
                enumerated_pair_count=enumerated,
                orbit_averaged_normalized_gap=average,
                weighted_normalized_gap=weighted,
                exact_multinomial_count_verified=residual == 0,
                status=(
                    "exact-fourier-commutator-pair-stratum"
                    if residual == 0
                    else "fourier-commutator-stratum-count-failure"
                ),
            )
        )
    direct_normalized = direct / r
    fourier_normalized = fourier_sum / (q**2 * r)
    strata_normalized = strata_sum / q**2
    predicted = math.comb(m + 3, 3)
    duality_residual = abs(direct_normalized - fourier_normalized)
    strata_residual = abs(strata_normalized - fourier_normalized)
    exact = bool(
        len(groups) == predicted
        and maximum_count_residual == 0
        and max(
            maximum_negative,
            maximum_commutator_residual,
            duality_residual,
            strata_residual,
        )
        <= 5000 * tolerance
    )
    return FourierCommutatorDualityControl(
        control_id=control_id,
        profile_kind=profile_kind,
        cube_dimension=m,
        leaf_count=q,
        fiber_dimension=r,
        leaf_pair_count=q**2,
        fourier_pair_count=q**2,
        observed_pair_stratum_count=len(groups),
        predicted_pair_stratum_count=predicted,
        direct_normalized_component_M4=direct_normalized,
        fourier_dual_normalized_component_M4=fourier_normalized,
        strata_reconstructed_normalized_component_M4=strata_normalized,
        maximum_negative_fourier_pair_gap=maximum_negative,
        maximum_pair_gap_to_half_commutator_residual=(
            maximum_commutator_residual
        ),
        fourier_duality_residual=duality_residual,
        stratum_reconstruction_residual=strata_residual,
        maximum_stratum_multinomial_residual=maximum_count_residual,
        exact_fourier_commutator_duality_verified=exact,
        positive_component_M4_in_control=direct_normalized > 5000 * tolerance,
        status=(
            "positive-component-M4-fourier-commutator-duality-verified"
            if exact and direct_normalized > 5000 * tolerance
            else "zero-component-M4-fourier-commutator-boundary-verified"
            if exact
            else "fourier-commutator-duality-control-failure"
        ),
    )


def _typical_four_cell_mass_lower_bound(
    cube_dimension: int,
) -> tuple[int, int, float]:
    radius = math.ceil(math.sqrt(cube_dimension * math.log(max(cube_dimension, 2))))
    lower = max(0, cube_dimension // 4 - radius)
    upper = min(cube_dimension, math.ceil(cube_dimension / 4) + radius)
    # Each occupancy is marginally Bin(m,1/4). Hoeffding plus a union over
    # the four cells gives a sufficient simultaneous typical-mass bound.
    failure = 8.0 * math.exp(-2.0 * radius**2 / cube_dimension)
    return lower, upper, max(0.0, 1.0 - failure)


def fourier_commutator_scaling_record(
    cube_dimension: int,
) -> FourierCommutatorScalingRecord:
    if cube_dimension < 1:
        raise ValueError("cube dimension must be positive")
    lower, upper, mass = _typical_four_cell_mass_lower_bound(cube_dimension)
    strata = math.comb(cube_dimension + 3, 3)
    return FourierCommutatorScalingRecord(
        cube_dimension=cube_dimension,
        leaf_pair_count_log2=2 * cube_dimension,
        exact_pair_stratum_count=strata,
        log2_pair_stratum_count=math.log2(strata),
        pair_stratum_polynomial_degree=3,
        typical_cell_lower_count=lower,
        typical_cell_upper_count=upper,
        typical_four_cell_mass_lower_bound=mass,
        constant_typical_stratum_gap_would_prove_constant_M4=True,
        natural_typical_parity_gap_proved=False,
        status="fourier-pair-average-reduced-to-cubic-many-occupancy-strata",
    )


def fourier_commutator_duality_theorem() -> FourierCommutatorDualityTheorem:
    return FourierCommutatorDualityTheorem(
        deterministic_duality=(
            "M4(H)=q^-2 sum_(S,T)[Tr(A_S^2A_T^2)-Tr(A_SA_TA_SA_T)]"
        ),
        positive_pair_gap=(
            "each Fourier pair gap equals ||[A_S,A_T]||_F^2/2 and is nonnegative"
        ),
        coordinate_compression=(
            "A_S=W*Z_SW for block-sign involution Z_S=sum_x chi_S(x)D_x"
        ),
        parity_leakage_curl=(
            "[PZ_SP,PZ_TP]=PZ_T(I-P)Z_SP-PZ_S(I-P)Z_TP"
        ),
        annealed_stratum_count=(
            "coordinate exchangeability reduces q^2 pairs to binom(m+3,3) four-cell strata"
        ),
        typical_stratum_implication=(
            "a kappa lower bound on normalized gap over stratum mass rho gives M4/r>=rho*kappa"
        ),
        arbitrary_hermitian_povm=True,
        theorem_verified=True,
        status="component-M4-is-average-compressed-parity-commutator-gap",
    )


def run_component_leaf_fourier_commutator_duality(
    *,
    tolerance: float = 1e-9,
) -> ComponentLeafFourierCommutatorDualityReport:
    standard = (2, 1)
    controls = [
        audit_fourier_commutator_duality(
            "UNIFORM-Q8-R3",
            "uniform-scalar-povm",
            _uniform_povm(3, 3),
            tolerance=tolerance,
        ),
        audit_fourier_commutator_duality(
            "COARSE-Q8-TWO-BIT-PVM",
            "commuting-coarse-pvm",
            _coarse_pvm(3, 2),
            tolerance=tolerance,
        ),
        audit_fourier_commutator_duality(
            "HAAR-Q8-B2-R5",
            "noncommutative-haar-block-povm",
            _haar_block_povm(3, 2, 5, seed=5591),
            tolerance=tolerance,
        ),
        audit_fourier_commutator_duality(
            "S3-REPEATED-STANDARD-TRIVIAL-TARGET",
            "finite-wreath-canonical-component-povm",
            _natural_effects((3,), ((standard, standard),) * 3, tolerance=tolerance),
            tolerance=tolerance,
        ),
    ]
    scaling = [
        fourier_commutator_scaling_record(m)
        for m in (4, 8, 16, 32, 64, 128, 256)
    ]
    theorem = fourier_commutator_duality_theorem()
    failures = sum(
        not row.exact_fourier_commutator_duality_verified for row in controls
    )
    positive_controls = sum(row.positive_component_M4_in_control for row in controls)
    tail = scaling[-1]
    return ComponentLeafFourierCommutatorDualityReport(
        created_at=utc_now(),
        theorem_contract={
            "deterministic_duality": theorem.deterministic_duality,
            "positive_pair_gap": theorem.positive_pair_gap,
            "coordinate_compression": theorem.coordinate_compression,
            "parity_leakage_curl": theorem.parity_leakage_curl,
            "annealed_strata": theorem.annealed_stratum_count,
            "typical_implication": theorem.typical_stratum_implication,
            "natural_scope": (
                "Independent Plancherel sources and global-distinct/rank-event "
                "conditioning are coordinate-exchangeable. Physical 1/D "
                "weights may be inserted before the stratum expectation."
            ),
            "scope": (
                "The duality proves no natural typical parity-commutator gap."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "replace_signed_diagonal_crossing_subtraction_by_positive_fourier_pair_average",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Two applications of Walsh orthogonality give equation (1), "
                    "whose summands are half commutator squares."
                ),
            },
            {
                "obligation": "remove_exponential_fourier_pair_enumeration",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Coordinate exchangeability leaves binom(m+3,3) four-cell "
                    "occupancy strata with exact multinomial weights."
                ),
            },
            {
                "obligation": "prove_positive_natural_typical_parity_curl_gap",
                "resolved": False,
                "resolution": (
                    "For four-cell counts m/4+O(sqrt(m log m)), lower-bound "
                    "E[1_E ||[W*Z_SW,W*Z_TW]||_F^2/(2D)] on positive mass."
                ),
            },
            {
                "obligation": "identify_exact_commuting_recoupling_if_typical_gap_vanishes",
                "resolved": False,
                "resolution": (
                    "A vanishing result must exhibit why the natural dependency "
                    "projection asymptotically commutes with typical parity "
                    "involutions; ambient commutativity alone is insufficient."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The dual observables commute because all Z_S commute.",
                "resolved": True,
                "resolution": (
                    "False after compression. Equation (3) shows noncommutativity "
                    "is exactly complement leakage through P."
                ),
            },
            {
                "objection": "Fourier duality merely moves a signed cancellation.",
                "resolved": True,
                "resolution": (
                    "No. Every pair gap is a nonnegative commutator square."
                ),
            },
            {
                "objection": "One exceptional Fourier pair proves positive M4.",
                "resolved": True,
                "resolution": (
                    "A single pair has q^-2 weight. The proof needs positive "
                    "gap on inverse-polynomial or constant pair mass."
                ),
            },
            {
                "objection": "Generic projection geometry proves the natural gap.",
                "resolved": True,
                "resolution": (
                    "It does not. Natural P is a support difference of structured "
                    "Racah Gram operators, and may have arithmetic commuting sectors."
                ),
            },
        ],
        headline_metrics={
            "component_fourier_commutator_duality_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "positive_fourier_pair_gap_identity_count": int(theorem.theorem_verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "finite_positive_component_M4_control_count": positive_controls,
            "maximum_control_fourier_duality_residual": max(
                row.fourier_duality_residual for row in controls
            ),
            "tail_cube_dimension": tail.cube_dimension,
            "tail_fourier_pair_count_log2": tail.leaf_pair_count_log2,
            "tail_exact_pair_stratum_count": tail.exact_pair_stratum_count,
            "tail_typical_four_cell_mass_lower_bound": (
                tail.typical_four_cell_mass_lower_bound
            ),
            "natural_typical_parity_gap_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "component_M4_is_uniform_fourier_pair_gap_average": (
                theorem.theorem_verified and failures == 0
            ),
            "fourier_pair_gaps_are_termwise_nonnegative": True,
            "annealed_fourier_pairs_reduce_to_cubic_many_strata": True,
            "natural_typical_compressed_parity_gap_positive": False,
            "natural_component_M4_positive": False,
            "component_compiler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The signed diagonal/crossing burden is replaced by one positive "
                "typical compressed-parity gap, but that natural gap is unproved."
            ),
        },
        status=(
            "component-M4-reduced-to-typical-compressed-parity-commutator-gap"
            if failures == 0
            else "fourier-commutator-duality-control-failure"
        ),
        summary=(
            "Proved that component M4 is the uniform average of nonnegative "
            "Walsh-coefficient commutator gaps and reduced its natural pair law "
            "to cubic-many four-cell occupancy strata."
        ),
        falsifiers_triggered=[
            "Ambient parity involutions commute, but their dependency-projection compressions need not.",
            "A single exceptional Fourier pair has exponentially small averaging weight.",
            "Commuting PVM controls have zero parity-curl gap despite full Fourier support.",
            "No natural typical parity gap, M4, component compiler, algorithm, or speedup is proved.",
        ],
    )


def write_component_leaf_fourier_commutator_duality_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-COMMUTATOR-DUALITY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_leaf_fourier_commutator_duality" in globals():
        report = run_component_leaf_fourier_commutator_duality(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-COMMUTATOR-DUALITY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-COMMUTATOR-DUALITY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-COMMUTATOR-DUALITY.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_component_leaf_fourier_commutator_duality": str(path)
                },
            )
        )
    return payload
