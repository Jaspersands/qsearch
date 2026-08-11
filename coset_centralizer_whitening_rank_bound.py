"""Centralizer-restriction bound for coset multiplicity whitening.

Fix an involution ``h in G`` and let ``K=C_G(h)``.  In a natural source
branch ``lambda=(lambda_1,...,lambda_k)``, put

    U_lambda = tensor_i V_(lambda_i),
    P_lambda = tensor_i (I+rho_(lambda_i)(h))/2,
    W_lambda = range(P_lambda),
    R_lambda = rank(P_lambda).

For an irrep ``nu`` choose an orthonormal basis ``T_a`` of
``Hom_G(V_nu,U_lambda)``.  The covariance-compressed multiplicity matrix is
the Gram matrix

    (D_nu)_(a,b) = Tr(T_a^* P_lambda T_b).

Consequently

    rank(D_nu) = rank[T -> P_lambda T]
               <= dim Hom_K(Res_K V_nu, W_lambda).       (1)

Natural source averaging makes the sum of the right side exact.  Define the
``K``-module

    A = direct_sum_lambda d_lambda V_lambda^(+h).

It is the ``+1`` eigenspace of ``h`` in the regular representation restricted
to ``K``.  Since ``h`` is central in ``K``, its character is ``|G|/2`` at
``e,h`` and zero elsewhere.  Therefore

    E_source[sum_nu rank(D_nu)/R_lambda]
      <= [sum_nu (d_nu+chi_nu(h))]/|K|,                 (2)

independently of ``k``.

For ``G=S_n``, ``sum d_nu`` is the number ``I_n`` of involutions and the
Frobenius--Schur square-root formula gives ``sum chi_nu(h)=Q_h``, the number of
solutions of ``x^2=h``.  If ``h`` is fixed-point-free, ``n=2m`` and

    |K|=2^m m!,
    Q_h=0                         when m is odd,
    Q_h=m!/(m/2)!                when m is even.

The envelope ``(I_n+Q_h)/|K|`` is ``exp(Theta(sqrt(n)))``.  This removes all
copy-count and factorial growth from the ideal source-weighted whitening
bound, but it is still only an upper bound.  A polynomial algorithm requires
an actual-rank theorem, coherent access to the restriction-map image, a
whitening circuit, and a decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_covariant_multiplicity_whitening_escape import (
    natural_whitening_controls,
)
from coset_multiplicity_whitening_copy_window import (
    exact_expected_multiplicity_dimension_ratio,
    symmetric_group_involution_count,
)
from coset_state_distinguishability import involution_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/coset_centralizer_whitening_rank_bound.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-CENTRALIZER-WHITENING-RANK-BOUND"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SquareRootCharacterControl:
    n: int
    transposition_count: int
    centralizer_order: int
    sum_irrep_dimensions: int
    sum_irrep_characters: int
    direct_fixed_point_free_square_root_count: int | None
    frobenius_schur_square_root_identity_verified: bool | None
    centralizer_rank_envelope: float


@dataclass(frozen=True)
class CentralizerRankFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    source_branch_count: int
    observed_average_multiplicity_rank_ratio: float
    regular_tensor_dimension_upper_bound: float
    centralizer_restriction_upper_bound: float
    combined_upper_bound: float
    observed_to_centralizer_envelope_ratio: float
    upper_bound_residual: float
    finite_control_verified: bool


@dataclass(frozen=True)
class FixedPointFreeCentralizerScalingRecord:
    n: int
    transposition_count: int
    centralizer_order_decimal: str
    perfect_matching_count_decimal: str
    involution_count_decimal: str
    square_root_count_decimal: str
    exact_centralizer_rank_envelope: float
    log2_exact_centralizer_rank_envelope: float
    elementary_log2_envelope_lower_bound: float
    cosh_plus_one_log2_envelope_upper_bound: float
    lower_bound_below_exact: bool
    exact_below_upper_bound: bool
    constant_pgm_success_copy_count: int
    regular_tensor_upper_at_pgm_width: float
    centralizer_upper_at_pgm_width: float
    centralizer_improves_copy_dependent_bound: bool
    envelope_is_exp_theta_sqrt_n: bool
    status: str


@dataclass(frozen=True)
class CentralizerWhiteningRankTheorem:
    gram_identity: str
    restriction_map: str
    regular_plus_module: str
    averaged_bound: str
    symmetric_group_numerator: str
    fixed_point_free_square_roots: str
    asymptotic_envelope: str
    scope_limit: str
    multiplicity_rank_as_restriction_map_rank_proved: bool
    copy_independent_natural_upper_bound_proved: bool
    fixed_point_free_exp_sqrt_envelope_proved: bool
    actual_rank_matches_envelope_proved: bool
    polynomial_actual_rank_proved: bool
    coherent_restriction_transform_constructed: bool
    polynomial_hidden_involution_algorithm_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetCentralizerWhiteningRankReport:
    created_at: str
    theorem_contract: dict[str, Any]
    square_root_character_controls: list[SquareRootCharacterControl]
    finite_rank_controls: list[CentralizerRankFiniteControl]
    scaling_records: list[FixedPointFreeCentralizerScalingRecord]
    theorem: CentralizerWhiteningRankTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def involution_centralizer_order(n: int, transposition_count: int) -> int:
    if transposition_count < 1 or 2 * transposition_count > n:
        raise ValueError("invalid involution cycle count")
    return (
        (2**transposition_count)
        * math.factorial(transposition_count)
        * math.factorial(n - 2 * transposition_count)
    )


def fixed_point_free_square_root_count(n: int) -> int:
    if n < 2 or n % 2:
        raise ValueError("fixed-point-free involutions require positive even n")
    transpositions = n // 2
    if transpositions % 2:
        return 0
    return math.factorial(transpositions) // math.factorial(transpositions // 2)


def square_root_character_control(
    n: int,
    transposition_count: int,
) -> SquareRootCharacterControl:
    dimensions = sum(
        hook_length_dimension(partition) for partition in integer_partitions(n)
    )
    characters = sum(
        character_on_involution(partition, transposition_count)
        for partition in integer_partitions(n)
    )
    fixed_point_free = transposition_count == n // 2 and n % 2 == 0
    direct = fixed_point_free_square_root_count(n) if fixed_point_free else None
    verified = characters == direct if direct is not None else None
    centralizer = involution_centralizer_order(n, transposition_count)
    return SquareRootCharacterControl(
        n=n,
        transposition_count=transposition_count,
        centralizer_order=centralizer,
        sum_irrep_dimensions=dimensions,
        sum_irrep_characters=characters,
        direct_fixed_point_free_square_root_count=direct,
        frobenius_schur_square_root_identity_verified=verified,
        centralizer_rank_envelope=(dimensions + characters) / centralizer,
    )


def centralizer_rank_envelope(n: int, transposition_count: int) -> float:
    control = square_root_character_control(n, transposition_count)
    return control.centralizer_rank_envelope


def finite_centralizer_rank_control(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> CentralizerRankFiniteControl:
    _, aggregate = natural_whitening_controls(
        n, transposition_count, copy_count
    )
    observed = aggregate.average_raw_multiplicity_inverse_second_moment
    regular_upper = exact_expected_multiplicity_dimension_ratio(n, copy_count)
    centralizer_upper = centralizer_rank_envelope(n, transposition_count)
    combined = min(regular_upper, centralizer_upper)
    residual = max(0.0, observed - combined)
    return CentralizerRankFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        source_branch_count=aggregate.source_branch_count,
        observed_average_multiplicity_rank_ratio=observed,
        regular_tensor_dimension_upper_bound=regular_upper,
        centralizer_restriction_upper_bound=centralizer_upper,
        combined_upper_bound=combined,
        observed_to_centralizer_envelope_ratio=(
            observed / centralizer_upper if centralizer_upper else 0.0
        ),
        upper_bound_residual=residual,
        finite_control_verified=(
            aggregate.all_finite_controls_passed and residual <= 1e-10
        ),
    )


def _log2_cosh_plus_one(value: float) -> float:
    # cosh(x)+1 = 2 cosh(x/2)^2.
    half = value / 2
    log_cosh_half = (
        half
        - math.log(2.0)
        + math.log1p(math.exp(-2.0 * half))
    ) / math.log(2.0)
    return 1.0 + 2.0 * log_cosh_half


def fixed_point_free_scaling_record(n: int) -> FixedPointFreeCentralizerScalingRecord:
    if n < 8 or n % 4:
        raise ValueError("n must be a multiple of four and at least eight")
    transpositions = n // 2
    order = math.factorial(n)
    centralizer = involution_centralizer_order(n, transpositions)
    matchings = involution_count(n, transpositions)
    involutions = symmetric_group_involution_count(n)
    roots = fixed_point_free_square_root_count(n)
    envelope = (involutions + roots) / centralizer
    log_envelope = math.log2(involutions + roots) - math.log2(centralizer)
    witness_index = math.floor(math.sqrt(n / 2) / 4)
    lower_log = 2 * witness_index - math.log2(n + 1)
    upper_log = _log2_cosh_plus_one(math.sqrt(n))
    pgm_width = math.ceil(math.log2(matchings))
    regular_at_pgm = exact_expected_multiplicity_dimension_ratio(n, pgm_width)
    theta_certificate = bool(
        witness_index >= 1
        and lower_log <= log_envelope + 1e-10
        and log_envelope <= upper_log + 1e-10
    )
    return FixedPointFreeCentralizerScalingRecord(
        n=n,
        transposition_count=transpositions,
        centralizer_order_decimal=str(centralizer),
        perfect_matching_count_decimal=str(matchings),
        involution_count_decimal=str(involutions),
        square_root_count_decimal=str(roots),
        exact_centralizer_rank_envelope=envelope,
        log2_exact_centralizer_rank_envelope=log_envelope,
        elementary_log2_envelope_lower_bound=lower_log,
        cosh_plus_one_log2_envelope_upper_bound=upper_log,
        lower_bound_below_exact=lower_log <= log_envelope + 1e-10,
        exact_below_upper_bound=log_envelope <= upper_log + 1e-10,
        constant_pgm_success_copy_count=pgm_width,
        regular_tensor_upper_at_pgm_width=regular_at_pgm,
        centralizer_upper_at_pgm_width=envelope,
        centralizer_improves_copy_dependent_bound=(
            envelope < regular_at_pgm
        ),
        envelope_is_exp_theta_sqrt_n=theta_certificate,
        status="copy-independent-centralizer-exp-sqrt-envelope",
    )


def build_coset_centralizer_whitening_rank_report(
    *,
    finite_specs: tuple[tuple[int, int], ...] = ((3, 1), (4, 2), (5, 2)),
    finite_copy_counts: tuple[int, ...] = (1, 2, 3),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128, 256, 512),
) -> CosetCentralizerWhiteningRankReport:
    character_controls = [
        square_root_character_control(n, transpositions)
        for n in range(4, 13, 2)
        for transpositions in (n // 2,)
    ]
    finite_controls = [
        finite_centralizer_rank_control(n, transpositions, copy_count)
        for n, transpositions in finite_specs
        for copy_count in finite_copy_counts
    ]
    scaling = [fixed_point_free_scaling_record(n) for n in scaling_n_values]
    verified = bool(
        all(
            row.frobenius_schur_square_root_identity_verified is True
            for row in character_controls
        )
        and all(row.finite_control_verified for row in finite_controls)
        and all(row.lower_bound_below_exact for row in scaling)
        and all(row.exact_below_upper_bound for row in scaling)
    )
    theorem = CentralizerWhiteningRankTheorem(
        gram_identity=(
            "In an orthonormal basis T_a of Hom_G(V_nu,U_lambda), "
            "D_nu[a,b]=Tr(T_a^* P_lambda T_b)."
        ),
        restriction_map=(
            "D_nu is the Gram matrix of T_a -> P_lambda T_a, so its rank is "
            "the image rank of Hom_G(V_nu,U_lambda) into "
            "Hom_K(Res_K V_nu,W_lambda)."
        ),
        regular_plus_module=(
            "A=direct_sum_lambda d_lambda V_lambda^(+h) is [G:K] copies of "
            "Ind_<h>^K(1), with character |G|/2 at e,h and zero elsewhere."
        ),
        averaged_bound=(
            "For every k>=1, E_source sum_nu rank(D_nu)/R <= "
            "|K|^-1 sum_nu(d_nu+chi_nu(h))."
        ),
        symmetric_group_numerator=(
            "For S_n the numerator is I_n+Q_h: Robinson--Schensted gives "
            "sum d_nu=I_n and Frobenius--Schur gives sum chi_nu(h)=Q_h."
        ),
        fixed_point_free_square_roots=(
            "If h has m=n/2 transpositions, every square root consists only "
            "of 4-cycles pairing those transpositions; Q_h=0 for odd m and "
            "m!/(m/2)! for even m."
        ),
        asymptotic_envelope=(
            "For n divisible by four, 4^floor(sqrt(n/2)/4)/(n+1) <= "
            "(I_n+Q_h)/|K| <= cosh(sqrt(n))+1, hence exp(Theta(sqrt(n)))."
        ),
        scope_limit=(
            "The theorem upper-bounds actual rank and does not prove "
            "saturation, polynomial rank, coherent access, whitening, or decoding."
        ),
        multiplicity_rank_as_restriction_map_rank_proved=True,
        copy_independent_natural_upper_bound_proved=True,
        fixed_point_free_exp_sqrt_envelope_proved=True,
        actual_rank_matches_envelope_proved=False,
        polynomial_actual_rank_proved=False,
        coherent_restriction_transform_constructed=False,
        polynomial_hidden_involution_algorithm_proved=False,
        theorem_verified=verified,
        status=(
            "copy-independent-centralizer-rank-envelope-proved"
            if verified
            else "centralizer-rank-bound-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "square_root_character_control_count": len(character_controls),
        "square_root_character_control_failure_count": sum(
            row.frobenius_schur_square_root_identity_verified is not True
            for row in character_controls
        ),
        "finite_rank_control_count": len(finite_controls),
        "finite_rank_control_failure_count": sum(
            not row.finite_control_verified for row in finite_controls
        ),
        "restriction_map_rank_theorem_count": 1,
        "copy_independent_natural_upper_bound_theorem_count": 1,
        "exp_sqrt_envelope_theorem_count": 1,
        "maximum_finite_observed_to_centralizer_envelope_ratio": max(
            row.observed_to_centralizer_envelope_ratio
            for row in finite_controls
        ),
        "maximum_log2_centralizer_rank_envelope": max(
            row.log2_exact_centralizer_rank_envelope for row in scaling
        ),
        "actual_rank_saturation_theorem_count": 0,
        "polynomial_actual_rank_theorem_count": 0,
        "coherent_restriction_transform_count": 0,
        "polynomial_hidden_involution_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetCentralizerWhiteningRankReport(
        created_at=utc_now(),
        theorem_contract={
            "hidden_object": "an involution h in S_n",
            "centralizer": "K=C_(S_n)(h)",
            "source": (
                "Natural hidden-independent weak-Fourier labels on k "
                "same-hidden coset-state registers."
            ),
            "rank_map": (
                "Restriction of diagonal-G intertwiners to the tensor product "
                "of the individual +h eigenspaces."
            ),
            "non_claim": (
                "The exp(Theta(sqrt(n))) expression is an upper envelope, not "
                "a runtime lower bound or evidence of rank saturation."
            ),
        },
        square_root_character_controls=character_controls,
        finite_rank_controls=finite_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-CENTRALIZER-RESTRICTION-RANK",
                "statement": (
                    "Determine the natural rank of Hom_G(V_nu,U)->"
                    "Hom_K(V_nu,W) at PGM copy width, not merely its codomain size."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-CENTRALIZER-TRANSFORM",
                "statement": (
                    "Construct a coherent transform exposing the relevant K-type "
                    "restriction image without dense branching tables."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-MULTIPLICITY-WHITENING-AND-DECODER",
                "statement": (
                    "Whiten the image with source-sensitive precision and decode "
                    "the hidden matching in polynomial time."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The multiplicity rank can still grow as 2^k.",
                "answer": (
                    "Its natural expectation is capped by a centralizer expression "
                    "independent of k; the 2^k bound is not the final envelope."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "The exp(Theta(sqrt(n))) envelope proves a subexponential lower bound."
                ),
                "answer": (
                    "False. It is an upper bound on rank; actual restriction maps "
                    "may have polynomial image rank."
                ),
                "resolved": True,
            },
            {
                "challenge": "A small average rank would itself be an algorithm.",
                "answer": (
                    "False. Basis access, block encoding, precision, and the "
                    "carrier-sensitive outcome decoder remain independent obligations."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "copy_independent_centralizer_rank_upper_bound_proved": True,
            "factorial_or_2_to_k_whitening_envelope_survives": False,
            "actual_rank_saturates_centralizer_envelope": False,
            "actual_rank_is_polynomial": False,
            "coherent_centralizer_restriction_transform_proved": False,
            "polynomial_multiplicity_whitening_proved": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Centralizer restriction caps the ideal natural whitening rank "
                "by exp(Theta(sqrt(n))) for every copy count. Whether the actual "
                "restriction image is polynomial is now the decisive open theorem."
            ),
        },
        status="centralizer-rank-envelope-sharp-image-rank-open",
        summary=(
            "Proved a copy-independent centralizer restriction bound on natural "
            "multiplicity whitening and evaluated its fixed-point-free "
            "exp(Theta(sqrt(n))) envelope. Actual image rank and all circuit "
            "obligations remain open."
        ),
        falsifiers_triggered=[
            (
                "The covariance-compressed multiplicity-rank envelope does not "
                "continue growing as 2^k."
            ),
            (
                "The remaining source-average normalization is subexponential, "
                "not factorial, for fixed-point-free involutions."
            ),
            (
                "An exp(Theta(sqrt(n))) upper envelope cannot be cited as a "
                "superpolynomial lower bound."
            ),
            (
                "The exact next object is the image rank of a G-to-centralizer "
                "restriction map."
            ),
        ],
    )


def write_coset_centralizer_whitening_rank_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-CENTRALIZER-WHITENING-RANK-BOUND"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(build_coset_centralizer_whitening_rank_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG--CENTRALIZER-WHITENING-RANK-BOUND",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-CENTRALIZER-WHITENING-RANK-BOUND."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-CENTRALIZER-WHITENING-RANK-BOUND."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "coset_centralizer_whitening_rank_bound": str(path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    report = write_coset_centralizer_whitening_rank_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
