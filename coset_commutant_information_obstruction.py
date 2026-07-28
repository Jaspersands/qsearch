"""Zero-information theorem for commutant-only coset-state measurements.

Fix a conjugacy class ``C`` in a finite group and an ensemble satisfying

    sigma_{x h x^-1} = U_x sigma_h U_x^dagger.

If every POVM effect ``E_y`` commutes with every ``U_x``, then

    Tr(E_y sigma_{x h x^-1}) = Tr(E_y sigma_h).

Thus a commutant-only outcome is independent of the individual hidden element
``h`` under the uniform conjugacy-class prior and has exactly zero mutual
information with it.  For conditioned symmetric-group coset states,
``U_x`` is the diagonal action on all Fourier column registers.

This theorem applies to target-irrep projectors, intermediate coupling-shape
projectors, multiplicity-space commutant observables, and Racah intertwiners
when the final POVM effects remain in the diagonal-action commutant.  Such
operations may still be useful preprocessing.  They become informative only
when followed by carrier-sensitive/covariant effects that do not commute
outcome-by-outcome with the diagonal action.  In particular, fixed tableau
effects from diagonal YJM operators are outside this no-go's premise.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from coset_jucys_murphy_label_transform import transposition_matrix
from coset_multiplicity_commutant_search import (
    bounded_support_orbit_generators,
)
from coset_three_copy_recoupling_obstruction import involutions
from representation_obstruction import hook_length_dimension
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/coset_commutant_information_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-COMMUTANT-INFORMATION-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CommutantFiniteControlRecord:
    n: int
    transposition_count: int
    left_source_partition: tuple[int, ...]
    right_source_partition: tuple[int, ...]
    hidden_involution_count: int
    conditioned_tensor_dimension: int
    commutant_generator_count: int
    maximum_diagonal_action_commutator_residual: float
    maximum_state_trace_residual: float
    maximum_commutant_outcome_total_variation: float
    maximum_commutant_expectation_range: float
    maximum_noncommutant_basis_effect_probability_range: float
    commutant_distribution_invariance_verified: bool
    noncommutant_escape_witness_verified: bool
    status: str


@dataclass(frozen=True)
class CommutantInformationObstructionReport:
    created_at: str
    theorem_contract: dict[str, object]
    architecture_boundary: dict[str, list[str]]
    finite_controls: list[CommutantFiniteControlRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def commutant_only_mutual_information_bits() -> int:
    """Return the exact theorem value for a uniform conjugacy-class prior."""

    return 0


def _involution_representation(
    partition: tuple[int, ...],
    permutation: tuple[int, ...],
) -> np.ndarray:
    dimension = hook_length_dimension(partition)
    result = np.eye(dimension)
    seen: set[int] = set()
    for left, right in enumerate(permutation):
        if left in seen or right == left:
            continue
        if permutation[right] != left:
            raise ValueError("expected an involution permutation")
        first, second = sorted((left + 1, right + 1))
        result = result @ transposition_matrix(
            partition,
            first,
            second,
        )
        seen.update((left, right))
    return result


def _conditioned_source_state(
    partition: tuple[int, ...],
    permutation: tuple[int, ...],
    transposition_count: int,
) -> np.ndarray:
    dimension = hook_length_dimension(partition)
    character = character_on_involution(partition, transposition_count)
    denominator = dimension + character
    if denominator <= 0:
        raise ValueError("source label is inaccessible for this involution class")
    representation = _involution_representation(partition, permutation)
    return (np.eye(dimension) + representation) / denominator


def _spectral_distribution(
    operator: np.ndarray,
    state: np.ndarray,
    tolerance: float = 1e-9,
) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    probabilities: list[float] = []
    start = 0
    while start < len(eigenvalues):
        stop = start + 1
        while (
            stop < len(eigenvalues)
            and abs(eigenvalues[stop] - eigenvalues[start]) <= tolerance
        ):
            stop += 1
        fiber = eigenvectors[:, start:stop]
        projector = fiber @ fiber.T
        probabilities.append(float(np.trace(projector @ state).real))
        start = stop
    return np.asarray(probabilities)


def audit_commutant_finite_control(
    n: int = 5,
    transposition_count: int = 2,
    left_source: tuple[int, ...] = (3, 2),
    right_source: tuple[int, ...] = (3, 1, 1),
) -> CommutantFiniteControlRecord:
    hidden = involutions(n, transposition_count)
    names, operators, generator_records = bounded_support_orbit_generators(
        left_source,
        right_source,
    )
    states = [
        np.kron(
            _conditioned_source_state(
                left_source,
                permutation,
                transposition_count,
            ),
            _conditioned_source_state(
                right_source,
                permutation,
                transposition_count,
            ),
        )
        for permutation in hidden
    ]
    trace_residual = max(
        (abs(float(np.trace(state).real) - 1.0) for state in states),
        default=0.0,
    )
    maximum_tv = 0.0
    maximum_expectation_range = 0.0
    for operator in operators:
        distributions = [
            _spectral_distribution(operator, state)
            for state in states
        ]
        reference = distributions[0]
        maximum_tv = max(
            maximum_tv,
            max(
                (
                    0.5 * float(np.abs(distribution - reference).sum())
                    for distribution in distributions
                ),
                default=0.0,
            ),
        )
        expectations = [
            float(np.trace(operator @ state).real)
            for state in states
        ]
        maximum_expectation_range = max(
            maximum_expectation_range,
            max(expectations) - min(expectations),
        )
    diagonals = np.asarray([np.diag(state).real for state in states])
    noncommutant_range = float(
        np.max(np.max(diagonals, axis=0) - np.min(diagonals, axis=0))
    )
    commutator_residual = max(
        (
            record.diagonal_action_commutator_residual
            for record in generator_records
        ),
        default=0.0,
    )
    invariant = (
        maximum_tv <= 1e-10
        and maximum_expectation_range <= 1e-10
        and commutator_residual <= 1e-10
    )
    escape = noncommutant_range > 1e-8
    return CommutantFiniteControlRecord(
        n=n,
        transposition_count=transposition_count,
        left_source_partition=left_source,
        right_source_partition=right_source,
        hidden_involution_count=len(hidden),
        conditioned_tensor_dimension=states[0].shape[0],
        commutant_generator_count=len(names),
        maximum_diagonal_action_commutator_residual=commutator_residual,
        maximum_state_trace_residual=trace_residual,
        maximum_commutant_outcome_total_variation=maximum_tv,
        maximum_commutant_expectation_range=maximum_expectation_range,
        maximum_noncommutant_basis_effect_probability_range=(
            noncommutant_range
        ),
        commutant_distribution_invariance_verified=invariant,
        noncommutant_escape_witness_verified=escape,
        status=(
            "commutant-zero-information-verified-carrier-sensitive-escape-open"
            if invariant and escape
            else "finite-commutant-control-failed"
        ),
    )


def build_commutant_information_obstruction_report(
) -> CommutantInformationObstructionReport:
    controls = [audit_commutant_finite_control()]
    invariance_count = sum(
        record.commutant_distribution_invariance_verified
        for record in controls
    )
    escape_count = sum(
        record.noncommutant_escape_witness_verified
        for record in controls
    )
    metrics: dict[str, int | float] = {
        "general_all_k_commutant_zero_information_theorem_count": 1,
        "exact_commutant_only_mutual_information_bits": (
            commutant_only_mutual_information_bits()
        ),
        "finite_control_count": len(controls),
        "finite_commutant_distribution_invariance_verified_count": (
            invariance_count
        ),
        "finite_noncommutant_escape_witness_count": escape_count,
        "maximum_finite_commutant_outcome_total_variation": max(
            (
                record.maximum_commutant_outcome_total_variation
                for record in controls
            ),
            default=0.0,
        ),
        "maximum_finite_commutant_expectation_range": max(
            (
                record.maximum_commutant_expectation_range
                for record in controls
            ),
            default=0.0,
        ),
        "maximum_noncommutant_basis_effect_probability_range": max(
            (
                record.maximum_noncommutant_basis_effect_probability_range
                for record in controls
            ),
            default=0.0,
        ),
        "commutant_only_hidden_involution_decoder_count": 0,
        "carrier_sensitive_covariant_decoder_count": 0,
    }
    return CommutantInformationObstructionReport(
        created_at=utc_now(),
        theorem_contract={
            "ensemble_covariance": (
                "sigma_(x h x^-1)=U_x sigma_h U_x^dagger"
            ),
            "commutant_effect": (
                "[E_y,U_x]=0 for every outcome y and group element x"
            ),
            "probability_identity": (
                "Tr(E_y sigma_(x h x^-1))=Tr(E_y sigma_h)"
            ),
            "information_consequence": (
                "For a uniform conjugacy-class prior, Y is independent of H "
                "and I(H;Y)=0 exactly."
            ),
            "copy_scope": (
                "All k and all conditioned source-label tuples; U_x is the "
                "diagonal action on the k Fourier column registers."
            ),
            "does_not_assume": (
                "Any complexity conjecture, finite-size trend, or classical "
                "simulation algorithm."
            ),
        },
        architecture_boundary={
            "information_free_when_measured_alone": [
                "coupled target irrep labels",
                "intermediate coupling-tree shape labels",
                "Kronecker multiplicity commutant observables",
                "Racah/associator labels with commutant POVM effects",
                "class-sum frame eigenvalues",
            ],
            "not_ruled_out": [
                "carrier/tableau-sensitive POVM effects",
                "covariant outcomes transformed with the hidden conjugacy class",
                "commutant preprocessing followed by noncommutant measurement",
                "pretty-good or other covariant measurements with compressed outcomes",
            ],
            "required_architecture_change": [
                "preserve carrier registers rather than output only invariant labels",
                "specify the symmetry-breaking/covariant final POVM",
                "prove mutual information about the individual h",
                "supply a polynomial decoder and classical comparison",
            ],
        },
        finite_controls=controls,
        headline_metrics=metrics,
        claim_gate={
            "commutant_only_outcomes_can_identify_hidden_involution": False,
            "commutant_only_zero_information_proved": True,
            "current_multiplicity_separator_is_decoder": False,
            "carrier_sensitive_escape_exists_finitely": escape_count > 0,
            "carrier_sensitive_covariant_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The current commutant and Racah labels are invariant over the "
                "hidden conjugacy class. They can organize a measurement but "
                "cannot be its information-bearing final outcomes."
            ),
        },
        status=(
            "commutant-only-decoder-route-falsified-carrier-sensitive-covariant-route-required"
        ),
        summary=(
            "Proved for all copy counts that diagonal-action commutant POVM "
            "outcomes have exactly zero information about the individual "
            "hidden involution, and verified the boundary on a nontrivial "
            "S_5 multiplicity control."
        ),
        falsifiers_triggered=[
            (
                "A simple-spectrum multiplicity separator is not an "
                "information-bearing hidden-involution measurement."
            ),
            (
                "Changing coupling trees and reading only invariant Racah "
                "labels cannot break conjugacy covariance."
            ),
            (
                "Exact target and multiplicity branch probabilities do not "
                "imply a decoder when every effect lies in the commutant."
            ),
            (
                "Carrier-sensitive effects can vary across conjugates, so the "
                "theorem redirects rather than rules out collective algorithms."
            ),
        ],
    )


def write_commutant_information_obstruction_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(build_commutant_information_obstruction_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-COMMUTANT-ONLY-HIDDEN-INVOLUTION-DECODER",
                source=str(output_path),
                claim=(
                    "Target, multiplicity, or Racah labels from "
                    "diagonal-action commutant effects can identify the "
                    "individual hidden involution."
                ),
                reason_invalid=(
                    "Every such outcome probability is constant over the "
                    "hidden conjugacy class, so its mutual information is zero."
                ),
                lesson=(
                    "Retain commutant transforms only as preprocessing and "
                    "require a carrier-sensitive covariant final POVM."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-SUCCESS",
                    "PO-NO-GO",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-COSET"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=dict(payload["headline_metrics"]),
                falsifiers_triggered=list(payload["falsifiers_triggered"]),
                artifacts={
                    "coset_commutant_information_obstruction": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_commutant_information_obstruction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
