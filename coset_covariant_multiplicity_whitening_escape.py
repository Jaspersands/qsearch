"""Covariance-compressed escape from direct coset-frame inversion.

For a rank-``R`` projector ``P`` and its orbit under a finite-group
representation

    U = direct_sum_nu V_nu tensor M_nu,

Schur averaging gives

    B = E_g U_g P U_g^* = direct_sum_nu I_(d_nu)/d_nu tensor D_nu,
    D_nu = Tr_(V_nu)(Pi_nu P Pi_nu).

The direct source-weighted frame-inverse moment is

    rank(B)/R = sum_nu d_nu rank(D_nu)/R.

The covariance-compressed PGM factorization instead contains
``P(I tensor D_nu^(-1/2))``.  Under the actual average-state source law, its
raw multiplicity inverse-square moment is exactly

    sum_nu rank(D_nu)/R.

Carrier dimensions therefore cancel before multiplicity whitening.  With the
physical cost floor one, the clipped moment is

    sum_(nu,j) max(delta_(nu,j),1)/R
      <= 1 + sum_nu rank(D_nu)/R,

where ``delta_(nu,j)`` are the positive eigenvalues of ``D_nu``.  This is a
genuine escape from the standalone direct-frame obstruction: extensive
Holevo information can reside in carrier orbit dimensions without forcing a
large ideal multiplicity-whitening moment.

The identities are algebraic, not a circuit.  They do not construct a
coherent internal Kronecker transform, block-encode ``D_nu`` with the needed
normalization, implement its source-adapted inverse, or decode the hidden
involution.  Those are now the precise constructive obligations.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations_with_replacement
from pathlib import Path
from typing import Any

import numpy as np

from coset_natural_multicopy_pgm_benchmark import (
    _multiset_multiplicity,
    _source_data,
    _tensor_states,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/"
    "coset_covariant_multiplicity_whitening_escape.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-COVARIANT-MULTIPLICITY-WHITENING-ESCAPE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class MultiplicityWhiteningSector:
    target_partition: Partition
    carrier_dimension: int
    physical_isotypic_rank: int
    multiplicity_support_rank: int
    minimum_positive_multiplicity_eigenvalue: float
    maximum_multiplicity_eigenvalue: float
    raw_inverse_square_moment_contribution: float
    clipped_inverse_square_moment_contribution: float


@dataclass(frozen=True)
class MultiplicityWhiteningControl:
    control_id: str
    n: int
    transposition_count: int
    copy_count: int
    source_partitions: tuple[Partition, ...]
    natural_source_probability: float
    hidden_hypothesis_count: int
    physical_dimension: int
    input_projector_rank: int
    direct_frame_support_rank: int
    total_multiplicity_support_rank: int
    direct_frame_inverse_second_moment: float
    raw_multiplicity_inverse_second_moment: float
    clipped_multiplicity_inverse_second_moment: float
    direct_to_raw_carrier_cancellation_factor: float
    direct_rank_decomposition_residual: float
    raw_moment_identity_residual: float
    clipped_moment_upper_bound_residual: float
    input_projector_residual: float
    generator_commutator_residual: float
    central_projector_completeness_residual: float
    central_projector_idempotence_residual: float
    rank_divisibility_failure_count: int
    normalized_frame_spectral_upper_residual: float
    sectors: list[MultiplicityWhiteningSector]
    theorem_control_passed: bool
    status: str


@dataclass(frozen=True)
class NaturalWhiteningAggregate:
    n: int
    transposition_count: int
    copy_count: int
    source_branch_count: int
    total_natural_source_probability: float
    average_direct_frame_inverse_second_moment: float
    average_raw_multiplicity_inverse_second_moment: float
    average_clipped_multiplicity_inverse_second_moment: float
    average_carrier_cancellation_factor: float
    maximum_branch_raw_multiplicity_inverse_second_moment: float
    maximum_branch_clipped_multiplicity_inverse_second_moment: float
    all_finite_controls_passed: bool
    status: str


@dataclass(frozen=True)
class CovariantMultiplicityWhiteningTheorem:
    schur_average: str
    direct_moment: str
    compressed_factor: str
    raw_compressed_moment: str
    clipped_cost_bound: str
    information_separation: str
    constructive_criterion: str
    scope_limit: str
    carrier_dimension_cancellation_proved: bool
    raw_multiplicity_moment_identity_proved: bool
    clipped_moment_bound_proved: bool
    natural_finite_escape_controls_passed: bool
    all_n_polynomial_multiplicity_moment_proved: bool
    coherent_multiplicity_transform_constructed: bool
    controlled_multiplicity_whitening_circuit_constructed: bool
    polynomial_hidden_involution_decoder_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetCovariantMultiplicityWhiteningReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[MultiplicityWhiteningControl]
    natural_source_aggregates: list[NaturalWhiteningAggregate]
    theorem: CovariantMultiplicityWhiteningTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    result = matrices[0]
    for matrix in matrices[1:]:
        result = np.kron(result, matrix)

    return result


def _adjacent_transpositions(n: int) -> tuple[Permutation, ...]:
    output = []
    for index in range(n - 1):
        permutation = list(range(n))
        permutation[index], permutation[index + 1] = (
            permutation[index + 1],
            permutation[index],
        )
        output.append(tuple(permutation))
    return tuple(output)


def audit_multiplicity_whitening_branch(
    n: int,
    transposition_count: int,
    source_partitions: tuple[Partition, ...],
    states: tuple[np.ndarray, ...],
    *,
    natural_source_probability: float = 1.0,
    tolerance: float = 1e-9,
) -> MultiplicityWhiteningControl:
    """Resolve isotypic support ranks without choosing a multiplicity basis."""

    if not source_partitions or not states:
        raise ValueError("source partitions and hidden states are required")
    if any(sum(partition) != n for partition in source_partitions):
        raise ValueError("source partitions must have size n")
    dimension = states[0].shape[0]
    if any(state.shape != (dimension, dimension) for state in states):
        raise ValueError("state dimensions differ")

    source_eigenvalues = np.linalg.eigvalsh(
        (states[0] + states[0].conj().T) / 2
    )
    input_rank = int(np.count_nonzero(source_eigenvalues > tolerance))
    if input_rank <= 0:
        raise ValueError("source state has empty support")
    projector = input_rank * states[0]
    projector_residual = float(
        np.linalg.norm(projector @ projector - projector, ord=2)
    )
    frame = input_rank * sum(states) / len(states)
    frame = (frame + frame.conj().T) / 2
    frame_eigenvalues = np.linalg.eigvalsh(frame)
    direct_rank = int(np.count_nonzero(frame_eigenvalues > tolerance))
    frame_upper_residual = max(
        0.0,
        float(np.max(frame_eigenvalues, initial=0.0)) - 1.0,
    )

    representation_tables = tuple(
        _source_representation_rows(partition)
        for partition in source_partitions
    )
    permutations = tuple(representation_tables[0])
    diagonal_action = {
        permutation: _kron_all(
            tuple(table[permutation] for table in representation_tables)
        )
        for permutation in permutations
    }
    generator_residual = max(
        float(
            np.linalg.norm(
                diagonal_action[generator] @ frame
                - frame @ diagonal_action[generator],
                ord=2,
            )
        )
        for generator in _adjacent_transpositions(n)
    )

    central_sum = np.zeros((dimension, dimension), dtype=np.complex128)
    central_idempotence = 0.0
    sectors: list[MultiplicityWhiteningSector] = []
    decomposed_rank = 0
    multiplicity_rank = 0
    raw_numeric = 0.0
    clipped_numeric = 0.0
    divisibility_failures = 0
    for target in integer_partitions(n):
        target_dimension = hook_length_dimension(target)
        target_table = _source_representation_rows(target)
        central = sum(
            np.conjugate(np.trace(target_table[permutation]))
            * diagonal_action[permutation]
            for permutation in permutations
        ) * (target_dimension / math.factorial(n))
        central = (central + central.conj().T) / 2
        central_sum += central
        central_idempotence = max(
            central_idempotence,
            float(np.linalg.norm(central @ central - central, ord=2)),
        )
        block = central @ frame @ central
        block = (block + block.conj().T) / 2
        eigenvalues = np.linalg.eigvalsh(block)
        positive = eigenvalues[eigenvalues > tolerance]
        block_rank = len(positive)
        if not block_rank:
            continue
        decomposed_rank += block_rank
        if block_rank % target_dimension:
            divisibility_failures += 1
            block_multiplicity_rank = block_rank / target_dimension
        else:
            block_multiplicity_rank = block_rank // target_dimension
        multiplicity_rank += int(round(block_multiplicity_rank))

        # Every D_nu eigenvalue delta appears d_nu times in the frame as
        # delta/d_nu.  Summing over the physical repetitions avoids choosing
        # a Clebsch/multiplicity basis.
        raw_contribution = float(
            np.sum(
                (positive / input_rank)
                * (1.0 / (target_dimension * positive))
            )
        )
        clipped_contribution = float(
            np.sum(
                (positive / input_rank)
                * np.maximum(
                    1.0,
                    1.0 / (target_dimension * positive),
                )
            )
        )
        raw_numeric += raw_contribution
        clipped_numeric += clipped_contribution
        multiplicity_eigenvalues = target_dimension * positive
        sectors.append(
            MultiplicityWhiteningSector(
                target_partition=target,
                carrier_dimension=target_dimension,
                physical_isotypic_rank=block_rank,
                multiplicity_support_rank=int(round(block_multiplicity_rank)),
                minimum_positive_multiplicity_eigenvalue=float(
                    np.min(multiplicity_eigenvalues)
                ),
                maximum_multiplicity_eigenvalue=float(
                    np.max(multiplicity_eigenvalues)
                ),
                raw_inverse_square_moment_contribution=raw_contribution,
                clipped_inverse_square_moment_contribution=(
                    clipped_contribution
                ),
            )
        )

    direct_moment = direct_rank / input_rank
    raw_formula = multiplicity_rank / input_rank
    clipped_upper = 1.0 + raw_formula
    direct_rank_residual = abs(decomposed_rank - direct_rank)
    raw_residual = abs(raw_numeric - raw_formula)
    clipped_residual = max(0.0, clipped_numeric - clipped_upper)
    completeness_residual = float(
        np.linalg.norm(central_sum - np.eye(dimension), ord=2)
    )
    cancellation = direct_moment / raw_formula if raw_formula else math.inf
    passed = bool(
        projector_residual <= 1e-8
        and generator_residual <= 1e-8
        and completeness_residual <= 1e-8
        and central_idempotence <= 1e-8
        and not divisibility_failures
        and direct_rank_residual <= 1e-8
        and raw_residual <= 1e-8
        and clipped_residual <= 1e-8
        and frame_upper_residual <= 1e-8
    )
    source_name = "-".join(".".join(map(str, p)) for p in source_partitions)
    return MultiplicityWhiteningControl(
        control_id=f"S{n}-k{len(source_partitions)}-{source_name}",
        n=n,
        transposition_count=transposition_count,
        copy_count=len(source_partitions),
        source_partitions=source_partitions,
        natural_source_probability=natural_source_probability,
        hidden_hypothesis_count=len(states),
        physical_dimension=dimension,
        input_projector_rank=input_rank,
        direct_frame_support_rank=direct_rank,
        total_multiplicity_support_rank=multiplicity_rank,
        direct_frame_inverse_second_moment=direct_moment,
        raw_multiplicity_inverse_second_moment=raw_formula,
        clipped_multiplicity_inverse_second_moment=clipped_numeric,
        direct_to_raw_carrier_cancellation_factor=cancellation,
        direct_rank_decomposition_residual=direct_rank_residual,
        raw_moment_identity_residual=raw_residual,
        clipped_moment_upper_bound_residual=clipped_residual,
        input_projector_residual=projector_residual,
        generator_commutator_residual=generator_residual,
        central_projector_completeness_residual=completeness_residual,
        central_projector_idempotence_residual=central_idempotence,
        rank_divisibility_failure_count=divisibility_failures,
        normalized_frame_spectral_upper_residual=frame_upper_residual,
        sectors=sectors,
        theorem_control_passed=passed,
        status=(
            "covariant-carrier-cancellation-verified"
            if passed
            else "covariant-whitening-control-failure"
        ),
    )


def natural_whitening_controls(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> tuple[list[MultiplicityWhiteningControl], NaturalWhiteningAggregate]:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    partitions, probabilities, state_families = _source_data(
        n, transposition_count
    )
    controls: list[MultiplicityWhiteningControl] = []
    for indices in combinations_with_replacement(
        range(len(partitions)), copy_count
    ):
        source_probability = float(_multiset_multiplicity(indices))
        for index in indices:
            source_probability *= probabilities[index]
        source_partitions = tuple(partitions[index] for index in indices)
        states = _tensor_states(
            tuple(state_families[index] for index in indices)
        )
        controls.append(
            audit_multiplicity_whitening_branch(
                n,
                transposition_count,
                source_partitions,
                states,
                natural_source_probability=source_probability,
            )
        )

    source_mass = sum(row.natural_source_probability for row in controls)
    average_direct = sum(
        row.natural_source_probability
        * row.direct_frame_inverse_second_moment
        for row in controls
    )
    average_raw = sum(
        row.natural_source_probability
        * row.raw_multiplicity_inverse_second_moment
        for row in controls
    )
    average_clipped = sum(
        row.natural_source_probability
        * row.clipped_multiplicity_inverse_second_moment
        for row in controls
    )
    passed = bool(
        abs(source_mass - 1.0) <= 1e-10
        and all(row.theorem_control_passed for row in controls)
    )
    aggregate = NaturalWhiteningAggregate(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        source_branch_count=len(controls),
        total_natural_source_probability=source_mass,
        average_direct_frame_inverse_second_moment=average_direct,
        average_raw_multiplicity_inverse_second_moment=average_raw,
        average_clipped_multiplicity_inverse_second_moment=average_clipped,
        average_carrier_cancellation_factor=(
            average_direct / average_raw if average_raw else math.inf
        ),
        maximum_branch_raw_multiplicity_inverse_second_moment=max(
            row.raw_multiplicity_inverse_second_moment for row in controls
        ),
        maximum_branch_clipped_multiplicity_inverse_second_moment=max(
            row.clipped_multiplicity_inverse_second_moment for row in controls
        ),
        all_finite_controls_passed=passed,
        status=(
            "natural-covariant-whitening-controls-pass"
            if passed
            else "natural-covariant-whitening-control-failure"
        ),
    )
    return controls, aggregate


def build_coset_covariant_multiplicity_whitening_report(
    *,
    finite_n: int = 5,
    finite_transposition_count: int = 2,
    finite_copy_counts: tuple[int, ...] = (1, 2, 3),
) -> CosetCovariantMultiplicityWhiteningReport:
    controls: list[MultiplicityWhiteningControl] = []
    aggregates: list[NaturalWhiteningAggregate] = []
    for copy_count in finite_copy_counts:
        branch_controls, aggregate = natural_whitening_controls(
            finite_n,
            finite_transposition_count,
            copy_count,
        )
        controls.extend(branch_controls)
        aggregates.append(aggregate)
    verified = bool(
        all(row.theorem_control_passed for row in controls)
        and all(row.all_finite_controls_passed for row in aggregates)
    )
    finite_escape = bool(
        verified
        and all(
            row.average_raw_multiplicity_inverse_second_moment
            < row.average_direct_frame_inverse_second_moment + 1e-10
            for row in aggregates
        )
    )
    theorem = CovariantMultiplicityWhiteningTheorem(
        schur_average=(
            "B=E_g U_g P U_g^*=direct_sum_nu I_(d_nu)/d_nu tensor D_nu, "
            "D_nu=Tr_(V_nu)(Pi_nu P Pi_nu)."
        ),
        direct_moment=(
            "Tr((B/R)B^+)=sum_nu d_nu rank(D_nu)/R."
        ),
        compressed_factor=(
            "The Fourier-compressed covariant PGM factor is "
            "P(I tensor D_nu^(-1/2)); group, projector-rank, and carrier "
            "normalizations cancel algebraically."
        ),
        raw_compressed_moment=(
            "Under the average-state source spectrum, the ideal multiplicity "
            "inverse-square moment is sum_nu rank(D_nu)/R exactly."
        ),
        clipped_cost_bound=(
            "After flooring per-eigenvalue cost at one, the moment is "
            "sum_(nu,j) max(delta_(nu,j),1)/R <= "
            "1+sum_nu rank(D_nu)/R."
        ),
        information_separation=(
            "Holevo information lower-bounds the carrier-weighted direct "
            "moment but does not force the carrier-cancelled multiplicity "
            "moment to be large."
        ),
        constructive_criterion=(
            "A viable route must prove sum_nu rank(D_nu)/R=poly(n) under the "
            "natural k=Theta(n log n) source, implement the coherent internal "
            "Kronecker decomposition, and realize source-adapted D_nu whitening."
        ),
        scope_limit=(
            "Finite small moments are not an all-n rank theorem, a block "
            "encoding, an inverse circuit, or a hidden-involution decoder."
        ),
        carrier_dimension_cancellation_proved=True,
        raw_multiplicity_moment_identity_proved=True,
        clipped_moment_bound_proved=True,
        natural_finite_escape_controls_passed=finite_escape,
        all_n_polynomial_multiplicity_moment_proved=False,
        coherent_multiplicity_transform_constructed=False,
        controlled_multiplicity_whitening_circuit_constructed=False,
        polynomial_hidden_involution_decoder_constructed=False,
        theorem_verified=verified,
        status=(
            "covariant-multiplicity-whitening-escape-criterion-proved"
            if verified
            else "covariant-multiplicity-whitening-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_branch_control_count": len(controls),
        "natural_source_aggregate_count": len(aggregates),
        "finite_control_failure_count": sum(
            not row.theorem_control_passed for row in controls
        ),
        "carrier_dimension_cancellation_theorem_count": 1,
        "raw_multiplicity_moment_identity_count": 1,
        "clipped_multiplicity_moment_bound_count": 1,
        "maximum_direct_rank_decomposition_residual": max(
            row.direct_rank_decomposition_residual for row in controls
        ),
        "maximum_raw_moment_identity_residual": max(
            row.raw_moment_identity_residual for row in controls
        ),
        "maximum_clipped_moment_bound_residual": max(
            row.clipped_moment_upper_bound_residual for row in controls
        ),
        "maximum_central_projector_residual": max(
            max(
                row.central_projector_completeness_residual,
                row.central_projector_idempotence_residual,
            )
            for row in controls
        ),
        "maximum_finite_average_direct_inverse_second_moment": max(
            row.average_direct_frame_inverse_second_moment
            for row in aggregates
        ),
        "maximum_finite_average_raw_multiplicity_second_moment": max(
            row.average_raw_multiplicity_inverse_second_moment
            for row in aggregates
        ),
        "maximum_finite_average_clipped_multiplicity_second_moment": max(
            row.average_clipped_multiplicity_inverse_second_moment
            for row in aggregates
        ),
        "all_n_polynomial_multiplicity_moment_theorem_count": 0,
        "coherent_internal_kronecker_transform_count": 0,
        "controlled_multiplicity_whitening_circuit_count": 0,
        "polynomial_hidden_involution_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetCovariantMultiplicityWhiteningReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "One natural source branch of k same-hidden conditioned "
                "involution carrier states, each a normalized projector."
            ),
            "representation": (
                "Diagonal conjugation action decomposed into carrier irreps "
                "and internal Kronecker multiplicities."
            ),
            "finite_method": (
                "Central isotypic projectors recover d_nu rank(D_nu) and the "
                "D_nu spectrum without selecting a multiplicity basis."
            ),
            "positive_boundary": (
                "Covariance cancels carrier dimensions from ideal source-"
                "weighted whitening; the remaining object is multiplicity-only."
            ),
            "non_claim": (
                "The finite spectrum calculation supplies no coherent basis "
                "transform or oracle for D_nu."
            ),
        },
        finite_controls=controls,
        natural_source_aggregates=aggregates,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-MULTIPLICITY-RANK-SCALING",
                "statement": (
                    "Bound the natural-source distribution of "
                    "sum_nu rank(D_nu)/R at k=Theta(n log n)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-COHERENT-KRONECKER-TRANSFORM",
                "statement": (
                    "Implement the diagonal S_n decomposition with a coherent "
                    "multiplicity basis in polynomial time."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-SOURCE-ADAPTED-D-WHITENING",
                "statement": (
                    "Block-encode and whiten D_nu with the algebraic carrier "
                    "normalization cancellation preserved by the circuit."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-COMPRESSED-OUTCOME-DECODER",
                "statement": (
                    "Convert the covariant PGM output into a verified hidden "
                    "involution without enumerating its conjugacy class."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": (
                    "The direct source-weighted inversion obstruction also "
                    "forces the compressed covariant inverse to be large."
                ),
                "answer": (
                    "False: Schur orthogonality removes d_nu. The two exact "
                    "moments differ by carrier-dimension weights."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "A small finite multiplicity moment proves a polynomial PGM."
                ),
                "answer": (
                    "False: the all-n moment, coherent Kronecker basis, D_nu "
                    "access, precision, and decoder are all unresolved."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "Central-projector calculations already implement the "
                    "multiplicity transform."
                ),
                "answer": (
                    "False: dense finite projectors reveal invariant spectra "
                    "but provide no uniform circuit or multiplicity coordinates."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "covariant_carrier_dimension_cancellation_proved": True,
            "finite_natural_multiplicity_moment_escape_observed": finite_escape,
            "all_n_polynomial_multiplicity_moment_proved": False,
            "coherent_internal_kronecker_transform_proved": False,
            "controlled_multiplicity_whitening_circuit_proved": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Covariance invalidates the direct-frame moment as a lower "
                "bound on fused PGM whitening and isolates a smaller, promising "
                "multiplicity-only target. No scalable access theorem or decoder exists."
            ),
        },
        status=(
            "covariant-carrier-cost-cancelled-multiplicity-whitening-open"
        ),
        summary=(
            f"Verified carrier-dimension cancellation on {len(controls)} "
            f"natural S_{finite_n} branches through {max(finite_copy_counts)} "
            "copies. The finite multiplicity moments remain small, but all-n "
            "rank scaling, coherent access, whitening, and decoding remain open."
        ),
        falsifiers_triggered=[
            (
                "The direct rank(F)/R inverse moment cannot be reused as a "
                "lower bound on the covariance-compressed PGM factorization."
            ),
            (
                "Carrier irrep dimensions cancel exactly before ideal "
                "multiplicity whitening."
            ),
            (
                "Finite small multiplicity moments do not establish an "
                "asymptotic circuit or algorithm."
            ),
            (
                "The research target is now source-adapted multiplicity "
                "whitening plus coherent Kronecker access and decoding."
            ),
        ],
    )


def write_coset_covariant_multiplicity_whitening_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-COVARIANT-MULTIPLICITY-WHITENING-ESCAPE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(
        build_coset_covariant_multiplicity_whitening_report(**kwargs)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_coset_covariant_multiplicity_whitening_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
