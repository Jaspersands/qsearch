"""Fourier boundary for candidate-relative branch-character convolution.

Let ``J_h:H->K`` be the tensor branch-character Naimark isometry for a
known relative element ``h`` and define

    C[g,s] = |G|^(-1/2) J_(s^-1 g).                       (1)

The operator-valued autocorrelations

    A_x = |G|^-1 sum_h J_h^* J_(xh)                      (2)

are the group-basis blocks of ``C^*C``.  This module gives the exact dual
criterion which the preceding Naimark-completion result left implicit.  For
each irrep ``nu`` of ``G``, set

    Jhat_nu = |G|^(-1/2) sum_h rho_nu(h^-1) tensor J_h.  (3)

The group Fourier transform block-diagonalizes (1): ``C`` is unitarily
equivalent to ``direct_sum_nu I_(d_nu) tensor Jhat_nu``.  Consequently,
uniform conditioning is equivalent to simultaneous lower and upper bounds
on every ``Jhat_nu^* Jhat_nu``.  Matrix-valued Parseval also gives

    ||C^*C-I||_F^2/(|G| dim H)
      = sum_x ||A_x-delta_(x,e)I||_F^2/dim H
      = [sum_nu d_nu ||Jhat_nu^*Jhat_nu-I||_F^2]
        /(|G| dim H).                                    (4)

Small individual autocorrelations do not imply a uniform Fourier gap.  For
the additive group ``Z_p``, where ``p=3 mod 4`` is prime, take the scalar
unit-modulus field

    j(0)=1,  j(x)=Legendre(x) for x!=0.

Every nonzero autocorrelation is exactly ``-1/p``, but the convolution
singular values are ``1/sqrt(p)`` once and ``sqrt(1+1/p)`` otherwise.  Its
condition number is ``sqrt(p+1)`` and its Gram operator-norm error tends to
one.  Thus even the apparently optimal pointwise scale ``1/|G|`` is
insufficient without signed global/Fourier control.

The same counterexample also prevents an overcorrection.  Its normalized
Frobenius error is only ``(p-1)/p^2`` and the bad Fourier sector has normalized
rank ``1/p``.  More generally, if the left side of (4) is ``R``, at most
``R/epsilon^2`` of the maximally mixed input mass can have Gram eigenvalue
outside ``[1-epsilon,1+epsilon]``.  A state-weighted decoder may therefore
discard rare bad sectors even when uniform conditioning fails.  It still
needs a physical input-mass theorem and normalization-one structured access;
neither follows from this Fourier reduction.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_branch_character_polar_naimark_completion import (
    Label,
    Permutation,
    _inverse_permutation,
    candidate_relative_convolution,
)
from self_dual_wreath_character_moments import compose_permutations
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_naimark_autocorrelation_fourier_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-NAIMARK-"
    "AUTOCORRELATION-FOURIER-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FourierSectorControl:
    partition: tuple[int, ...]
    irrep_dimension: int
    multiplier_input_dimension: int
    multiplier_output_dimension: int
    minimum_gram_eigenvalue: float
    maximum_gram_eigenvalue: float
    condition_number: float
    normalized_sector_frobenius_residual: float
    regular_input_mass: float
    uniformly_inverse_polynomial_sector_gap_observed: bool
    status: str


@dataclass(frozen=True)
class BranchFourierControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    group_order: int
    carrier_dimension: int
    character_output_dimension: int
    sector_controls: list[FourierSectorControl]
    convolution_minimum_singular_value: float
    convolution_maximum_singular_value: float
    convolution_condition_number: float
    direct_to_fourier_singular_spectrum_residual: float
    autocorrelation_to_global_parseval_residual: float
    fourier_to_global_parseval_residual: float
    normalized_gram_frobenius_residual: float
    gram_operator_norm_residual: float
    trim_epsilon: float
    bad_spectral_mass_fraction: float
    frobenius_markov_bad_mass_upper_bound: float
    exact_nonabelian_fourier_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class LegendreAutocorrelationCountercontrol:
    prime: int
    group_order: int
    maximum_nonidentity_autocorrelation_magnitude: float
    expected_nonidentity_autocorrelation: float
    minimum_convolution_singular_value: float
    maximum_convolution_singular_value: float
    convolution_condition_number: float
    expected_condition_number: float
    gram_operator_norm_residual: float
    expected_gram_operator_norm_residual: float
    normalized_gram_frobenius_residual: float
    expected_normalized_gram_frobenius_residual: float
    half_window_bad_spectral_mass_fraction: float
    pointwise_order_inverse_autocorrelation_sufficient_for_uniform_gap: bool
    vanishing_frobenius_error_allows_state_weighted_trimming: bool
    exact_legendre_counterexample_verified: bool
    status: str


@dataclass(frozen=True)
class AutocorrelationFourierTheorem:
    block_diagonalization: str
    uniform_conditioning_criterion: str
    matrix_parseval_identity: str
    legendre_uniform_counterexample: str
    state_weighted_tail_bound: str
    access_boundary: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NaimarkAutocorrelationFourierReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: AutocorrelationFourierTheorem
    branch_controls: list[BranchFourierControl]
    legendre_countercontrols: list[LegendreAutocorrelationCountercontrol]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def operator_autocorrelation(
    group: tuple[Permutation, ...],
    fields: dict[Permutation, np.ndarray],
    shift: Permutation,
) -> np.ndarray:
    """Return ``A_shift`` from equation (2)."""

    input_dimension = next(iter(fields.values())).shape[1]
    return sum(
        (
            fields[value].conj().T
            @ fields[compose_permutations(shift, value)]
            for value in group
        ),
        np.zeros((input_dimension, input_dimension), dtype=complex),
    ) / len(group)


def nonabelian_fourier_multiplier(
    partition: tuple[int, ...],
    group: tuple[Permutation, ...],
    fields: dict[Permutation, np.ndarray],
) -> np.ndarray:
    """Return the normalized multiplier in equation (3)."""

    rows = _source_representation_rows(partition)
    return sum(
        (
            np.kron(rows[_inverse_permutation(value)], fields[value])
            for value in group
        ),
        np.zeros(
            (
                next(iter(rows.values())).shape[0]
                * next(iter(fields.values())).shape[0],
                next(iter(rows.values())).shape[0]
                * next(iter(fields.values())).shape[1],
            ),
            dtype=complex,
        ),
    ) / math.sqrt(len(group))


def _condition_number(
    singular_values: np.ndarray,
    tolerance: float,
) -> float:
    if not len(singular_values) or singular_values[-1] <= tolerance:
        return math.inf
    return float(singular_values[0] / singular_values[-1])


def audit_branch_fourier_boundary(
    control_id: str,
    labels: tuple[Label, ...],
    *,
    trim_epsilon: float = 0.75,
    tolerance: float = 1e-9,
) -> BranchFourierControl:
    if not 0.0 < trim_epsilon < 1.0:
        raise ValueError("trim epsilon must lie strictly between zero and one")
    convolution, group, fields = candidate_relative_convolution(labels)
    input_dimension = next(iter(fields.values())).shape[1]
    identity_group = tuple(range(len(group[0])))
    identity = np.eye(input_dimension, dtype=complex)

    direct_singular_values = np.sort(
        np.linalg.svd(convolution, compute_uv=False)
    )
    predicted_singular_values: list[float] = []
    sectors: list[FourierSectorControl] = []
    weighted_fourier_error = 0.0
    bad_eigenvalue_count = 0
    for partition in integer_partitions(len(group[0])):
        multiplier = nonabelian_fourier_multiplier(partition, group, fields)
        irrep_dimension = _source_representation_rows(partition)[
            identity_group
        ].shape[0]
        singular_values = np.linalg.svd(multiplier, compute_uv=False)
        predicted_singular_values.extend(
            value
            for value in singular_values
            for _ in range(irrep_dimension)
        )
        gram = multiplier.conj().T @ multiplier
        gram_values = np.linalg.eigvalsh(
            (gram + gram.conj().T) / 2.0
        ).real
        residual = float(
            np.linalg.norm(
                gram - np.eye(gram.shape[0], dtype=complex),
                ord="fro",
            )
            ** 2
        )
        weighted_fourier_error += irrep_dimension * residual
        bad_eigenvalue_count += irrep_dimension * int(
            np.count_nonzero(np.abs(gram_values - 1.0) > trim_epsilon)
        )
        condition = _condition_number(singular_values, tolerance)
        sectors.append(
            FourierSectorControl(
                partition=partition,
                irrep_dimension=irrep_dimension,
                multiplier_input_dimension=multiplier.shape[1],
                multiplier_output_dimension=multiplier.shape[0],
                minimum_gram_eigenvalue=float(gram_values[0]),
                maximum_gram_eigenvalue=float(gram_values[-1]),
                condition_number=condition,
                normalized_sector_frobenius_residual=(
                    residual / (irrep_dimension * input_dimension)
                ),
                regular_input_mass=(irrep_dimension**2 / len(group)),
                uniformly_inverse_polynomial_sector_gap_observed=bool(
                    gram_values[0] > tolerance
                ),
                status=(
                    "finite-fourier-sector-nonsingular"
                    if gram_values[0] > tolerance
                    else "finite-fourier-sector-singular"
                ),
            )
        )

    predicted = np.sort(np.asarray(predicted_singular_values))
    spectrum_residual = float(
        np.max(np.abs(predicted - direct_singular_values))
    )
    gram = convolution.conj().T @ convolution
    gram_residual = gram - np.eye(gram.shape[0], dtype=complex)
    normalized_frobenius = float(
        np.linalg.norm(gram_residual, ord="fro") ** 2
        / gram.shape[0]
    )
    operator_residual = float(np.linalg.norm(gram_residual, ord=2))

    autocorrelation_error = 0.0
    for shift in group:
        autocorrelation = operator_autocorrelation(group, fields, shift)
        target = identity if shift == identity_group else np.zeros_like(identity)
        autocorrelation_error += float(
            np.linalg.norm(autocorrelation - target, ord="fro") ** 2
            / input_dimension
        )
    fourier_error = weighted_fourier_error / (
        len(group) * input_dimension
    )
    bad_mass = bad_eigenvalue_count / gram.shape[0]
    markov_bound = min(1.0, normalized_frobenius / trim_epsilon**2)
    direct_condition = _condition_number(
        direct_singular_values[::-1], tolerance
    )
    verified = bool(
        spectrum_residual <= 5000 * tolerance
        and abs(autocorrelation_error - normalized_frobenius)
        <= 5000 * tolerance
        and abs(fourier_error - normalized_frobenius)
        <= 5000 * tolerance
        and bad_mass <= markov_bound + 5000 * tolerance
    )
    return BranchFourierControl(
        control_id=control_id,
        n=len(group[0]),
        labels=labels,
        group_order=len(group),
        carrier_dimension=input_dimension,
        character_output_dimension=next(iter(fields.values())).shape[0],
        sector_controls=sectors,
        convolution_minimum_singular_value=float(direct_singular_values[0]),
        convolution_maximum_singular_value=float(direct_singular_values[-1]),
        convolution_condition_number=direct_condition,
        direct_to_fourier_singular_spectrum_residual=spectrum_residual,
        autocorrelation_to_global_parseval_residual=abs(
            autocorrelation_error - normalized_frobenius
        ),
        fourier_to_global_parseval_residual=abs(
            fourier_error - normalized_frobenius
        ),
        normalized_gram_frobenius_residual=normalized_frobenius,
        gram_operator_norm_residual=operator_residual,
        trim_epsilon=trim_epsilon,
        bad_spectral_mass_fraction=bad_mass,
        frobenius_markov_bad_mass_upper_bound=markov_bound,
        exact_nonabelian_fourier_boundary_verified=verified,
        status=(
            "exact-nonabelian-fourier-autocorrelation-boundary"
            if verified
            else "nonabelian-fourier-boundary-control-failure"
        ),
    )


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def _legendre_symbol(value: int, prime: int) -> int:
    residue = value % prime
    if residue == 0:
        return 0
    power = pow(residue, (prime - 1) // 2, prime)
    return -1 if power == prime - 1 else 1


def legendre_phase_field(prime: int) -> np.ndarray:
    if not _is_prime(prime) or prime % 4 != 3:
        raise ValueError("prime must be congruent to three modulo four")
    return np.asarray(
        [1 if value == 0 else _legendre_symbol(value, prime) for value in range(prime)],
        dtype=complex,
    )


def audit_legendre_autocorrelation_counterexample(
    prime: int,
    *,
    tolerance: float = 1e-9,
) -> LegendreAutocorrelationCountercontrol:
    field = legendre_phase_field(prime)
    correlations = np.asarray(
        [
            sum(
                field[value].conjugate() * field[(value + shift) % prime]
                for value in range(prime)
            )
            / prime
            for shift in range(prime)
        ]
    )
    convolution = np.asarray(
        [
            [field[(output - source) % prime] / math.sqrt(prime) for source in range(prime)]
            for output in range(prime)
        ],
        dtype=complex,
    )
    singular_values = np.linalg.svd(convolution, compute_uv=False)
    gram = convolution.conj().T @ convolution
    gram_values = np.linalg.eigvalsh((gram + gram.conj().T) / 2.0).real
    condition = float(singular_values[0] / singular_values[-1])
    operator_residual = float(
        np.linalg.norm(gram - np.eye(prime, dtype=complex), ord=2)
    )
    normalized_frobenius = float(
        np.linalg.norm(gram - np.eye(prime, dtype=complex), ord="fro") ** 2
        / prime
    )
    bad_mass = float(np.count_nonzero(np.abs(gram_values - 1.0) > 0.5) / prime)
    expected_minimum = 1.0 / math.sqrt(prime)
    expected_maximum = math.sqrt(1.0 + 1.0 / prime)
    expected_condition = math.sqrt(prime + 1.0)
    expected_operator = 1.0 - 1.0 / prime
    expected_frobenius = (prime - 1.0) / prime**2
    correlation_residual = float(
        max(abs(correlations[shift] + 1.0 / prime) for shift in range(1, prime))
    )
    verified = bool(
        np.max(np.abs(np.abs(field) - 1.0)) <= tolerance
        and abs(correlations[0] - 1.0) <= tolerance
        and correlation_residual <= 100 * tolerance
        and abs(singular_values[-1] - expected_minimum) <= 1000 * tolerance
        and abs(singular_values[0] - expected_maximum) <= 1000 * tolerance
        and abs(condition - expected_condition) <= 1000 * tolerance
        and abs(operator_residual - expected_operator) <= 1000 * tolerance
        and abs(normalized_frobenius - expected_frobenius) <= 1000 * tolerance
        and abs(bad_mass - 1.0 / prime) <= tolerance
    )
    return LegendreAutocorrelationCountercontrol(
        prime=prime,
        group_order=prime,
        maximum_nonidentity_autocorrelation_magnitude=float(
            np.max(np.abs(correlations[1:]))
        ),
        expected_nonidentity_autocorrelation=-1.0 / prime,
        minimum_convolution_singular_value=float(singular_values[-1]),
        maximum_convolution_singular_value=float(singular_values[0]),
        convolution_condition_number=condition,
        expected_condition_number=expected_condition,
        gram_operator_norm_residual=operator_residual,
        expected_gram_operator_norm_residual=expected_operator,
        normalized_gram_frobenius_residual=normalized_frobenius,
        expected_normalized_gram_frobenius_residual=expected_frobenius,
        half_window_bad_spectral_mass_fraction=bad_mass,
        pointwise_order_inverse_autocorrelation_sufficient_for_uniform_gap=False,
        vanishing_frobenius_error_allows_state_weighted_trimming=True,
        exact_legendre_counterexample_verified=verified,
        status=(
            "order-inverse-autocorrelation-uniform-gap-counterexample"
            if verified
            else "legendre-autocorrelation-control-failure"
        ),
    )


def run_naimark_autocorrelation_fourier_boundary(
) -> NaimarkAutocorrelationFourierReport:
    branch_controls = [
        audit_branch_fourier_boundary(
            "S3-SINGLE-PAIR-FOURIER-BOUNDARY",
            (((3,), (2, 1)),),
        ),
        audit_branch_fourier_boundary(
            "S3-THRESHOLD-FOURIER-BOUNDARY",
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
    ]
    legendre = [
        audit_legendre_autocorrelation_counterexample(prime)
        for prime in (3, 7, 11, 19, 43, 67, 103, 163)
    ]
    verified = bool(
        all(row.exact_nonabelian_fourier_boundary_verified for row in branch_controls)
        and all(row.exact_legendre_counterexample_verified for row in legendre)
    )
    theorem = AutocorrelationFourierTheorem(
        block_diagonalization=(
            "C is unitarily equivalent to direct_sum_nu I_(d_nu) tensor "
            "[|G|^-1/2 sum_h rho_nu(h^-1) tensor J_h]."
        ),
        uniform_conditioning_criterion=(
            "C has singular spectrum equal to the union of each Fourier-multiplier "
            "spectrum repeated d_nu times; a uniform gap requires every sector."
        ),
        matrix_parseval_identity=(
            "The normalized Gram Frobenius residual equals both the sum of squared "
            "operator-autocorrelation errors and the dimension-weighted Fourier-block residual."
        ),
        legendre_uniform_counterexample=(
            "For p=3 mod 4, the completed Legendre phase has A_x=-1/p for x!=0 "
            "but convolution condition sqrt(p+1)."
        ),
        state_weighted_tail_bound=(
            "If normalized Gram Frobenius error is R, maximally mixed mass outside "
            "the epsilon Gram window is at most R/epsilon^2."
        ),
        access_boundary=(
            "Fourier concentration or conditioning does not compile the dense "
            "multiplier at normalization one from pointwise J_h access."
        ),
        scope=(
            "The theorem refines the required spectral target. It neither proves nor "
            "refutes a state-weighted natural S_n gap, physical input domination, a "
            "structured Fourier multiplier circuit, a decoder, or a speedup."
        ),
        theorem_verified=verified,
        status=(
            "autocorrelation-reduced-to-fourier-extremes-and-state-weighted-tail"
            if verified
            else "autocorrelation-fourier-boundary-control-failure"
        ),
    )
    tail = legendre[-1]
    threshold = branch_controls[-1]
    return NaimarkAutocorrelationFourierReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        branch_controls=branch_controls,
        legendre_countercontrols=legendre,
        proof_obligations=[
            {
                "obligation": "replace_pointwise_autocorrelation_target_by_fourier_extreme_or_tail_control",
                "resolved": verified,
                "resolution": "Equations (3)-(4) give the exact uniform and state-weighted criteria.",
            },
            {
                "obligation": "prove_natural_branch_field_state_weighted_fourier_tail",
                "resolved": False,
                "resolution": "Bound the source-conditioned normalized Gram Frobenius residual and identify the physical Fourier-sector mass law.",
            },
            {
                "obligation": "prove_or_refute_uniform_natural_branch_fourier_gap",
                "resolved": False,
                "resolution": "The Legendre family shows that order-inverse pointwise autocorrelation alone cannot prove this.",
            },
            {
                "obligation": "compile_dense_branch_fourier_multipliers_at_normalization_one",
                "resolved": False,
                "resolution": "Need a representation-specific QFT/Clebsch-Gordan/Racah transform, not generic pointwise PREPARE/SELECT.",
            },
            {
                "obligation": "compose_with_physical_pgm_and_classical_falsifiers",
                "resolved": False,
                "resolution": "No physical decoder or complexity separation is supplied here.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Autocorrelation O(1/|G|) should make the Gram close to identity.",
                "resolved": True,
                "resolution": "False without signed global control: the Legendre off-diagonal blocks add coherently in the trivial Fourier sector.",
            },
            {
                "objection": "The divergent condition number kills every state-weighted decoder.",
                "resolved": True,
                "resolution": "Also false: the bad Legendre sector has only 1/p regular input mass and the Frobenius tail bound permits trimming.",
            },
            {
                "objection": "A small normalized Frobenius residual proves a uniform inverse.",
                "resolved": True,
                "resolution": "False; it proves only a spectral-mass tail bound, not a minimum singular value."
            },
            {
                "objection": "Fourier block diagonalization supplies an efficient circuit.",
                "resolved": True,
                "resolution": "No. The dense matrix-valued multipliers still require normalization-one structured access."
            },
        ],
        headline_metrics={
            "exact_nonabelian_fourier_boundary_theorem_count": int(verified),
            "finite_branch_fourier_control_count": len(branch_controls),
            "finite_control_failure_count": sum(
                not row.exact_nonabelian_fourier_boundary_verified
                for row in branch_controls
            )
            + sum(
                not row.exact_legendre_counterexample_verified for row in legendre
            ),
            "legendre_uniform_gap_counterexample_count": len(legendre),
            "tail_prime": tail.prime,
            "tail_maximum_nonidentity_autocorrelation": (
                tail.maximum_nonidentity_autocorrelation_magnitude
            ),
            "tail_convolution_condition_number": tail.convolution_condition_number,
            "tail_bad_spectral_mass_fraction": (
                tail.half_window_bad_spectral_mass_fraction
            ),
            "threshold_branch_condition_number": (
                threshold.convolution_condition_number
            ),
            "threshold_branch_normalized_frobenius_residual": (
                threshold.normalized_gram_frobenius_residual
            ),
            "all_n_natural_state_weighted_fourier_tail_theorem_count": 0,
            "normalization_one_fourier_multiplier_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "nonabelian_fourier_block_criterion_proved": verified,
            "matrix_autocorrelation_parseval_proved": verified,
            "order_inverse_pointwise_autocorrelation_suffices_for_uniform_gap": False,
            "vanishing_frobenius_error_suffices_for_uniform_gap": False,
            "frobenius_error_controls_maximally_mixed_bad_mass": verified,
            "natural_branch_state_weighted_fourier_tail_proved": False,
            "physical_input_maximally_mixed_or_dominated_proved": False,
            "uniform_natural_branch_fourier_gap_proved": False,
            "normalization_one_dense_fourier_multiplier_compiled": False,
            "physical_pgm_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Reduced candidate-relative Naimark convolution exactly to nonabelian "
            "Fourier multipliers. A Legendre family refutes order-inverse pointwise "
            "autocorrelation as a uniform-gap criterion, while its vanishing bad "
            "sector mass redirects the viable target to a physical state-weighted "
            "Fourier-tail theorem plus structured normalization-one access."
        ),
        falsifiers_triggered=[
            "O(1/|G|) pointwise operator autocorrelation is not by itself a uniform conditioning theorem.",
            "Vanishing normalized Gram Frobenius error is not a minimum-singular-value theorem.",
            "A divergent uniform condition number does not by itself refute state-weighted trimming.",
            "Fourier diagonalization is a mathematical reduction, not a dense multiplier compiler.",
        ],
    )


def write_naimark_autocorrelation_fourier_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_naimark_autocorrelation_fourier_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_naimark_autocorrelation_fourier_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
