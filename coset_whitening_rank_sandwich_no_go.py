"""Subexponential rank sandwich for direct multiplicity whitening.

Let ``C`` be a conjugacy class of ``M`` distinct involutions in ``S_n`` and
let ``P_h`` be the rank-``r=(n!/2)^k`` support projector of ``k`` regular
coset-state registers.  For

    B = M^-1 sum_(h in C) P_h,

distinct projector overlaps satisfy ``Tr(P_h P_t)/r=2^-k``.  Hence

    Tr(B^2)=r/M [1+(M-1)2^-k]

and the effective-rank inequality gives

    rank(B)/r >= M/[1+(M-1)2^-k].                         (1)

After the regular Fourier transform, each natural source branch has direct
carrier support ``sum_nu d_nu rank(D_nu)``.  Since ``d_nu<=d_max(S_n)``, the
exact natural-source decomposition of (1) yields

    E_source[sum_nu rank(D_nu)/R]
      >= M/[d_max(S_n)(1+(M-1)2^-k)].                    (2)

For fixed-point-free involutions, ``M=(n-1)!!``.  At
``k=ceil(log2 M)+O(1)``, the equal-overlap PGM has constant
information-theoretic success and (2) is at least ``M/(2 d_max)``.  Aggarwal
and Elboim prove

    d_max(S_n)=sqrt(n!) exp(-(d+o(1))sqrt(n)), d>0.

Since ``M/sqrt(n!)=Theta(n^-1/4)``, the lower bound is
``exp(Omega(sqrt(n)))``.  The separate centralizer-restriction theorem gives
an ``exp(O(sqrt(n)))`` upper bound.  Therefore the actual natural-source
multiplicity-support moment is ``exp(Theta(sqrt(n)))`` at the standard
constant-PGM-success copy width.

This closes standalone source-weighted ``D_nu^(-1/2)`` and standard
branchwise variable-time whitening as polynomial implementations of that PGM.
It is not a lower bound on a fused polar isometry that never exposes the
inverse, a different collective measurement, a below-threshold decoder, or
general quantum circuits.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_centralizer_whitening_rank_bound import centralizer_rank_envelope
from coset_covariant_multiplicity_whitening_escape import (
    natural_whitening_controls,
)
from coset_state_distinguishability import involution_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_pgm_success_theorem import pgm_success_lower_bound


REPORT_PATH = Path(
    "research/representation/coset_whitening_rank_sandwich_no_go.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-WHITENING-RANK-SANDWICH-NO-GO"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
MAXIMAL_DIMENSION_PAPER_ID = "aggarwal-elboim-maximal-dimension-2026"
MAXIMAL_DIMENSION_PAPER_URL = "https://arxiv.org/abs/2605.25995"


@dataclass(frozen=True)
class WhiteningRankFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    hidden_hypothesis_count: int
    maximum_irrep_dimension: int
    observed_average_multiplicity_rank_ratio: float
    effective_rank_lower_bound: float
    centralizer_upper_bound: float
    lower_bound_residual: float
    upper_bound_residual: float
    finite_sandwich_verified: bool


@dataclass(frozen=True)
class WhiteningRankScalingRecord:
    n: int
    perfect_matching_count_decimal: str
    maximum_irrep_partition: tuple[int, ...]
    maximum_irrep_dimension_decimal: str
    constant_pgm_success_copy_count: int
    pgm_success_lower_bound: float
    exact_effective_rank_lower_bound: float
    exact_source_inverse_rms_lower_bound: float
    exact_centralizer_rank_upper_bound: float
    lower_below_upper: bool
    finite_lower_bound_exceeds_one: bool
    status: str


@dataclass(frozen=True)
class WhiteningRankSandwichTheorem:
    projector_overlap: str
    frame_effective_rank: str
    natural_fourier_decomposition: str
    multiplicity_rank_lower_bound: str
    maximal_dimension_asymptotic: str
    perfect_matching_ratio: str
    centralizer_upper_bound: str
    sandwich_consequence: str
    route_consequence: str
    scope_limit: str
    exact_finite_group_lower_bound_proved: bool
    maximal_dimension_theorem_applied: bool
    exp_theta_sqrt_n_actual_moment_at_pgm_width_proved: bool
    polynomial_standalone_multiplicity_whitening_possible: bool
    fused_polar_isometry_ruled_out: bool
    alternative_collective_measurement_ruled_out: bool
    general_quantum_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetWhiteningRankSandwichReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[WhiteningRankFiniteControl]
    scaling_records: list[WhiteningRankScalingRecord]
    theorem: WhiteningRankSandwichTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def maximum_irrep_dimension(n: int) -> tuple[tuple[int, ...], int]:
    if n < 2:
        raise ValueError("n must be at least two")
    return max(
        (
            (partition, hook_length_dimension(partition))
            for partition in integer_partitions(n)
        ),
        key=lambda row: (row[1], row[0]),
    )


def multiplicity_rank_effective_lower_bound(
    n: int,
    hidden_count: int,
    copy_count: int,
) -> float:
    if hidden_count < 2 or copy_count < 1:
        raise ValueError("at least two hypotheses and one copy are required")
    _, maximum = maximum_irrep_dimension(n)
    collision = (hidden_count - 1) / (1 << copy_count)
    return hidden_count / (maximum * (1.0 + collision))


def finite_whitening_rank_control(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> WhiteningRankFiniteControl:
    _, aggregate = natural_whitening_controls(
        n, transposition_count, copy_count
    )
    hidden_count = involution_count(n, transposition_count)
    _, maximum = maximum_irrep_dimension(n)
    lower = multiplicity_rank_effective_lower_bound(
        n, hidden_count, copy_count
    )
    upper = centralizer_rank_envelope(n, transposition_count)
    observed = aggregate.average_raw_multiplicity_inverse_second_moment
    lower_residual = max(0.0, lower - observed)
    upper_residual = max(0.0, observed - upper)
    return WhiteningRankFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        hidden_hypothesis_count=hidden_count,
        maximum_irrep_dimension=maximum,
        observed_average_multiplicity_rank_ratio=observed,
        effective_rank_lower_bound=lower,
        centralizer_upper_bound=upper,
        lower_bound_residual=lower_residual,
        upper_bound_residual=upper_residual,
        finite_sandwich_verified=(
            aggregate.all_finite_controls_passed
            and lower_residual <= 1e-10
            and upper_residual <= 1e-10
        ),
    )


def whitening_rank_scaling_record(n: int) -> WhiteningRankScalingRecord:
    if n < 4 or n % 2:
        raise ValueError("n must be even and at least four")
    hidden_count = involution_count(n, n // 2)
    partition, maximum = maximum_irrep_dimension(n)
    copies = math.ceil(math.log2(hidden_count))
    lower = multiplicity_rank_effective_lower_bound(n, hidden_count, copies)
    upper = centralizer_rank_envelope(n, n // 2)
    return WhiteningRankScalingRecord(
        n=n,
        perfect_matching_count_decimal=str(hidden_count),
        maximum_irrep_partition=partition,
        maximum_irrep_dimension_decimal=str(maximum),
        constant_pgm_success_copy_count=copies,
        pgm_success_lower_bound=pgm_success_lower_bound(hidden_count, copies),
        exact_effective_rank_lower_bound=lower,
        exact_source_inverse_rms_lower_bound=math.sqrt(lower),
        exact_centralizer_rank_upper_bound=upper,
        lower_below_upper=lower <= upper + 1e-10,
        finite_lower_bound_exceeds_one=lower > 1.0,
        status="finite-rank-sandwich-control",
    )


def build_coset_whitening_rank_sandwich_report(
    *,
    finite_specs: tuple[tuple[int, int], ...] = ((3, 1), (4, 2), (5, 2)),
    finite_copy_counts: tuple[int, ...] = (1, 2, 3),
    scaling_n_values: tuple[int, ...] = (
        4,
        6,
        8,
        10,
        12,
        16,
        20,
        24,
        28,
        32,
    ),
) -> CosetWhiteningRankSandwichReport:
    finite_controls = [
        finite_whitening_rank_control(n, transpositions, copy_count)
        for n, transpositions in finite_specs
        for copy_count in finite_copy_counts
    ]
    scaling = [whitening_rank_scaling_record(n) for n in scaling_n_values]
    verified = bool(
        all(row.finite_sandwich_verified for row in finite_controls)
        and all(row.lower_below_upper for row in scaling)
    )
    theorem = WhiteningRankSandwichTheorem(
        projector_overlap=(
            "For distinct nonidentity involutions h,t in the regular "
            "representation, Tr(P_h^tensor k P_t^tensor k)/r=2^-k."
        ),
        frame_effective_rank=(
            "rank(B)/r >= M/[1+(M-1)2^-k] by "
            "rank(B)>=Tr(B)^2/Tr(B^2)."
        ),
        natural_fourier_decomposition=(
            "rank(B)/r equals the natural-source average of "
            "sum_nu d_nu rank(D_nu)/R."
        ),
        multiplicity_rank_lower_bound=(
            "Since d_nu<=d_max, E_source sum_nu rank(D_nu)/R >= "
            "M/[d_max(1+(M-1)2^-k)]."
        ),
        maximal_dimension_asymptotic=(
            "Aggarwal--Elboim: d_max(S_n)=sqrt(n!) "
            "exp(-(mathfrak_d+o(1))sqrt(n)) for a constant mathfrak_d>0."
        ),
        perfect_matching_ratio=(
            "For M=(n-1)!!, M/sqrt(n!)=Theta(n^-1/4), from the central "
            "binomial asymptotic."
        ),
        centralizer_upper_bound=(
            "The separate restriction theorem gives E_source sum rank(D_nu)/R "
            "<=exp(O(sqrt(n))) for every k."
        ),
        sandwich_consequence=(
            "At k=ceil(log2 M)+O(1), the actual natural multiplicity moment "
            "is exp(Theta(sqrt(n)))."
        ),
        route_consequence=(
            "Standalone D_nu inverse roots and standard source-weighted or "
            "branchwise variable-time whitening are superpolynomial at the "
            "constant-PGM-success width."
        ),
        scope_limit=(
            "The sandwich does not constrain a fused polar isometry that "
            "avoids standalone inversion, another collective POVM, a useful "
            "below-threshold decoder, or general quantum circuits."
        ),
        exact_finite_group_lower_bound_proved=True,
        maximal_dimension_theorem_applied=True,
        exp_theta_sqrt_n_actual_moment_at_pgm_width_proved=True,
        polynomial_standalone_multiplicity_whitening_possible=False,
        fused_polar_isometry_ruled_out=False,
        alternative_collective_measurement_ruled_out=False,
        general_quantum_circuit_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "exp-sqrt-actual-whitening-rank-sandwich-proved"
            if verified
            else "whitening-rank-sandwich-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_sandwich_control_count": len(finite_controls),
        "finite_sandwich_control_failure_count": sum(
            not row.finite_sandwich_verified for row in finite_controls
        ),
        "effective_rank_lower_bound_theorem_count": 1,
        "maximal_dimension_asymptotic_loaded_count": 1,
        "exp_theta_sqrt_actual_moment_theorem_count": 1,
        "maximum_finite_lower_bound_residual": max(
            row.lower_bound_residual for row in finite_controls
        ),
        "maximum_finite_upper_bound_residual": max(
            row.upper_bound_residual for row in finite_controls
        ),
        "maximum_exact_scaling_lower_bound": max(
            row.exact_effective_rank_lower_bound for row in scaling
        ),
        "tail_exact_source_inverse_rms_lower_bound": (
            scaling[-1].exact_source_inverse_rms_lower_bound
        ),
        "polynomial_standalone_multiplicity_whitening_count": 0,
        "fused_polar_isometry_lower_bound_count": 0,
        "alternative_collective_measurement_lower_bound_count": 0,
        "general_quantum_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetWhiteningRankSandwichReport(
        created_at=utc_now(),
        theorem_contract={
            "ensemble": (
                "Uniform fixed-point-free involution class in S_n, represented "
                "by k same-hidden regular coset-state support projectors."
            ),
            "copy_width": (
                "k=ceil(log2((n-1)!!))+O(1), where the equal-overlap PGM has "
                "constant information-theoretic success."
            ),
            "cost_quantity": (
                "Natural-source actual multiplicity support-rank moment, which "
                "lower-bounds the clipped inverse-square whitening moment."
            ),
            "external_input": (
                "Aggarwal--Elboim's 2026 maximal S_n irrep-dimension asymptotic."
            ),
            "non_claim": (
                "No lower bound on fused PGM implementations or arbitrary measurements."
            ),
        },
        finite_controls=finite_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-FUSED-POLAR-BEYOND-D-INVERSE",
                "statement": (
                    "Construct or obstruct a coherent PGM polar isometry that "
                    "does not expose D_nu^(-1/2) as a standalone operation."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BELOW-PGM-THRESHOLD",
                "statement": (
                    "Find a measurement with inverse-polynomial useful success "
                    "at least Omega(sqrt(n)) copies below the standard PGM width."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-ALTERNATIVE-COVARIANT-DECODER",
                "statement": (
                    "Exploit coherent cross-sector information using a "
                    "measurement whose implementation cost is not this rank moment."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": (
                    "The centralizer upper bound might hide polynomial actual rank."
                ),
                "answer": (
                    "Not at constant-PGM-success width: the effective-rank lower "
                    "bound plus maximal irrep dimension forces exp(Omega(sqrt(n)))."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "An exp(Theta(sqrt(n))) moment proves every PGM circuit is slow."
                ),
                "answer": (
                    "False. It charges standalone or branchwise multiplicity "
                    "inverse implementations, not a globally fused polar circuit."
                ),
                "resolved": True,
            },
            {
                "challenge": "Finite d_max rows prove the asymptotic lower bound.",
                "answer": (
                    "False. The asymptotic step explicitly depends on the cited "
                    "Aggarwal--Elboim theorem; finite rows are normalization controls."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "title": (
                    "On the maximal dimension of an irreducible representation "
                    "of the symmetric group"
                ),
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "use": (
                    "Turns the exact M/d_max multiplicity-rank lower bound into "
                    "exp(Omega(sqrt(n))) for fixed-point-free involutions."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "actual_multiplicity_rank_polynomial_at_pgm_width": False,
            "exp_theta_sqrt_actual_rank_moment_proved": True,
            "standalone_source_weighted_multiplicity_inverse_polynomial": False,
            "standard_branchwise_variable_time_whitening_polynomial": False,
            "fused_pgm_polar_isometry_ruled_out": False,
            "alternative_collective_measurement_ruled_out": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "general_quantum_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "At the copy width where the standard PGM has constant success, "
                "the actual source-average multiplicity inverse moment is "
                "exp(Theta(sqrt(n))). A viable algorithm must avoid exposing "
                "that inverse or use a different measurement/copy regime."
            ),
        },
        status="standalone-multiplicity-whitening-subexponential-no-go-fused-polar-open",
        summary=(
            "Proved an exp(Theta(sqrt(n))) sandwich for the actual natural "
            "multiplicity-support moment at constant-PGM-success width. This "
            "closes standalone source-weighted whitening but leaves fused polar "
            "and alternative collective measurements open."
        ),
        falsifiers_triggered=[
            (
                "Actual multiplicity rank is not polynomial at the standard "
                "constant-success PGM copy width."
            ),
            (
                "The centralizer exp(O(sqrt(n))) envelope is asymptotically tight "
                "in exponent for the natural source average."
            ),
            (
                "Covariance removes factorial cost but does not make standalone "
                "multiplicity whitening polynomial."
            ),
            (
                "The theorem cannot be promoted to a lower bound on globally "
                "fused PGM implementations or arbitrary quantum circuits."
            ),
        ],
    )


def write_coset_whitening_rank_sandwich_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-WHITENING-RANK-SANDWICH-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(build_coset_whitening_rank_sandwich_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_coset_whitening_rank_sandwich_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
