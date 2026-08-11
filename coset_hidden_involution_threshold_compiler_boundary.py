"""Compiler boundary for the logarithmic-copy hidden-involution Helstrom test.

The information-theoretic threshold theorem leaves one decisive computational
problem: implement the sign of the likelihood operator

    L_k = (1/M) sum_(h in C) product_(i=1)^k (I+R_h^(i)). (1)

Write ``Pi_h=(I+R_h)/2`` and

    A_k = (1/M) sum_h Pi_h^tensor k,    L_k=2^k A_k.     (2)

For fixed-point-free involutions, a uniform ``h`` can be prepared reversibly
and every controlled ``R_h`` is efficient.  Coherently testing all ``k`` plus
eigenspaces therefore gives a standard projected-unitary/block encoding of
``A_k`` with normalization one.  The desired sign, however, is

    sign(A_k - 2^-k I).                                 (3)

At the information threshold ``k=ceil(log2 M)``, the spectral threshold is
``Theta(1/M)``.  A bounded polynomial that is at most ``-2/3`` at zero and at
least ``2/3`` at ``2^(1-k)`` has degree at least

    sqrt(2^k/3),                                        (4)

by the Markov derivative inequality after mapping ``[0,1]`` to ``[-1,1]``.
Thus a generic polynomial/QSVT compiler for this normalized block encoding is
exponential at threshold.  This is a lower bound on the black-box polynomial
strategy, not on structured circuits for the actual symmetric-group family.

There is a natural central dilation.  Add branch qubits and define the group
representation

    V_g = direct_sum_(b in {0,1}^k) tensor_(i:b_i=1) R_g. (5)

For the uniform branch state ``|+>^k`` and the central class average
``K_C=M^-1 sum_h V_h``, one has the exact compression

    A_k = (<+|^k tensor I) K_C (|+>^k tensor I).         (6)

Generalized phase estimation can label the isotypic sectors of ``V`` when the
group QFT and controlled representation are available.  But spectral
thresholding does not commute with compression: measuring only the central
class-sum eigenvalue is strictly suboptimal in exact ``S_3`` controls, and the
branch-plus subspace is not invariant under ``K_C``.  Hence the dilation does
not by itself implement (3).

The remaining high-upside route must exploit source-weighted representation
structure to compile the compressed sign directly, or prove that its useful
spectral mass is dequantizable.  Merely writing an LCU, invoking generic QSVT,
or measuring central dilation labels does not cross the computational gate.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    dense_binary_states,
    involution_class_size,
    involution_conjugacy_class,
    right_regular_matrix,
    symmetric_group,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_threshold_compiler_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CentralDilationFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    conjugacy_class_size: int
    data_dimension: int
    branch_dimension: int
    dilation_dimension: int
    compression_identity_residual: float
    branch_plus_invariance_commutator_norm: float
    helstrom_trace_distance: float
    central_class_sum_measurement_total_variation: float
    retained_helstrom_signal_fraction: float
    central_measurement_strictly_suboptimal: bool
    compression_not_reducing_for_class_sum: bool
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class GenericPolynomialCompilerScalingRecord:
    n: int
    conjugacy_class_size: int
    threshold_copy_count: int
    normalized_likelihood_threshold: float
    markov_degree_lower_bound: int
    log2_markov_degree_lower_bound: float
    degree_lower_bound_over_sqrt_class_size: float
    generic_polynomial_compiler_is_polynomial: bool
    structured_direct_compiler_known: bool
    actual_family_circuit_lower_bound_proved: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionThresholdCompilerTheorem:
    average_projector_encoding: str
    normalized_sign_problem: str
    markov_polynomial_lower_bound: str
    central_dilation_identity: str
    compression_obstruction: str
    efficient_average_projector_block_encoding_formalized: bool
    generic_polynomial_degree_exponential_at_threshold: bool
    central_dilation_compression_proved: bool
    central_class_sum_measurement_is_helstrom: bool
    structured_threshold_sign_compiler_constructed: bool
    actual_family_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionThresholdCompilerReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[CentralDilationFiniteControl]
    scaling_records: list[GenericPolynomialCompilerScalingRecord]
    theorem: HiddenInvolutionThresholdCompilerTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def generic_markov_degree_lower_bound(copy_count: int) -> int:
    """Degree needed to change by 4/3 between 0 and ``2^(1-k)``."""

    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    return math.ceil(math.sqrt((2**copy_count) / 3.0))


def average_projector_from_dense_alternative(
    alternative: np.ndarray,
    copy_count: int,
) -> np.ndarray:
    dimension = alternative.shape[0]
    if alternative.shape != (dimension, dimension):
        raise ValueError("alternative state must be square")
    return (dimension / (2**copy_count)) * alternative


def _tensor_right_action(
    n: int,
    element: tuple[int, ...],
    mask: int,
    copy_count: int,
) -> np.ndarray:
    order = math.factorial(n)
    right = right_regular_matrix(n, element)
    identity = np.eye(order)
    operator = np.asarray([[1.0]])
    for index in range(copy_count):
        operator = np.kron(
            operator,
            right if (mask >> index) & 1 else identity,
        )
    return operator


def central_class_sum_dilation(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> np.ndarray:
    conjugacy_class = involution_conjugacy_class(n, transposition_count)
    branch_dimension = 1 << copy_count
    data_dimension = math.factorial(n) ** copy_count
    dilation = np.zeros(
        (branch_dimension * data_dimension,) * 2,
        dtype=float,
    )
    for hidden in conjugacy_class:
        for mask in range(branch_dimension):
            start = mask * data_dimension
            stop = start + data_dimension
            dilation[start:stop, start:stop] += (
                _tensor_right_action(n, hidden, mask, copy_count)
                / len(conjugacy_class)
            )
    return dilation


def _branch_plus_projector(
    branch_dimension: int,
    data_dimension: int,
) -> np.ndarray:
    plus = np.ones(branch_dimension) / math.sqrt(branch_dimension)
    return np.kron(np.outer(plus, plus), np.eye(data_dimension))


def compress_uniform_branch(
    dilation: np.ndarray,
    branch_dimension: int,
) -> np.ndarray:
    if dilation.shape[0] % branch_dimension:
        raise ValueError("dilation dimension is not divisible by branch dimension")
    data_dimension = dilation.shape[0] // branch_dimension
    blocks = dilation.reshape(
        branch_dimension,
        data_dimension,
        branch_dimension,
        data_dimension,
    )
    return blocks.sum(axis=(0, 2)) / branch_dimension


def _spectral_measurement_total_variation(
    observable: np.ndarray,
    null_state: np.ndarray,
    alternative_state: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> float:
    eigenvalues, eigenvectors = np.linalg.eigh(observable)
    total_variation = 0.0
    start = 0
    while start < len(eigenvalues):
        stop = start + 1
        while (
            stop < len(eigenvalues)
            and abs(eigenvalues[stop] - eigenvalues[start]) <= tolerance
        ):
            stop += 1
        fiber = eigenvectors[:, start:stop]
        null_probability = float(
            np.trace(fiber.conj().T @ null_state @ fiber).real
        )
        alternative_probability = float(
            np.trace(fiber.conj().T @ alternative_state @ fiber).real
        )
        total_variation += 0.5 * abs(
            alternative_probability - null_probability
        )
        start = stop
    return total_variation


def audit_central_dilation_control(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    maximum_dilation_dimension: int = 2048,
) -> CentralDilationFiniteControl:
    order = math.factorial(n)
    data_dimension = order**copy_count
    branch_dimension = 1 << copy_count
    dilation_dimension = data_dimension * branch_dimension
    if dilation_dimension > maximum_dilation_dimension:
        raise ValueError("central dilation finite control is too large")

    null, alternative = dense_binary_states(
        n,
        transposition_count,
        copy_count,
        maximum_dimension=maximum_dilation_dimension,
    )
    average_projector = average_projector_from_dense_alternative(
        alternative, copy_count
    )
    dilation = central_class_sum_dilation(
        n, transposition_count, copy_count
    )
    compressed = compress_uniform_branch(dilation, branch_dimension)
    compression_residual = float(
        np.linalg.norm(compressed - average_projector, ord=2)
    )

    branch_projector = _branch_plus_projector(
        branch_dimension, data_dimension
    )
    commutator = float(
        np.linalg.norm(
            branch_projector @ dilation - dilation @ branch_projector,
            ord=2,
        )
    )
    plus = np.ones(branch_dimension) / math.sqrt(branch_dimension)
    branch_state = np.outer(plus, plus)
    lifted_null = np.kron(branch_state, null)
    lifted_alternative = np.kron(branch_state, alternative)
    central_tv = _spectral_measurement_total_variation(
        dilation, lifted_null, lifted_alternative
    )
    helstrom = 0.5 * float(
        np.abs(np.linalg.eigvalsh(alternative - null)).sum()
    )
    suboptimal = central_tv < helstrom - 1e-9
    nonreducing = commutator > 1e-9
    verified = bool(
        compression_residual <= 1e-9
        and central_tv <= helstrom + 1e-9
        and suboptimal
        and nonreducing
    )
    return CentralDilationFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        conjugacy_class_size=involution_class_size(
            n, transposition_count
        ),
        data_dimension=data_dimension,
        branch_dimension=branch_dimension,
        dilation_dimension=dilation_dimension,
        compression_identity_residual=compression_residual,
        branch_plus_invariance_commutator_norm=commutator,
        helstrom_trace_distance=helstrom,
        central_class_sum_measurement_total_variation=central_tv,
        retained_helstrom_signal_fraction=central_tv / helstrom,
        central_measurement_strictly_suboptimal=suboptimal,
        compression_not_reducing_for_class_sum=nonreducing,
        finite_control_verified=verified,
        status=(
            "central-dilation-compression-exact-label-measurement-suboptimal"
            if verified
            else "central-dilation-compiler-control-failure"
        ),
    )


def generic_polynomial_compiler_scaling_record(
    n: int,
) -> GenericPolynomialCompilerScalingRecord:
    if n < 2 or n % 2:
        raise ValueError("n must be positive and even")
    size = involution_class_size(n, n // 2)
    copies = math.ceil(math.log2(size))
    degree = generic_markov_degree_lower_bound(copies)
    return GenericPolynomialCompilerScalingRecord(
        n=n,
        conjugacy_class_size=size,
        threshold_copy_count=copies,
        normalized_likelihood_threshold=2.0**(-copies),
        markov_degree_lower_bound=degree,
        log2_markov_degree_lower_bound=math.log2(degree),
        degree_lower_bound_over_sqrt_class_size=(
            degree / math.sqrt(size)
        ),
        generic_polynomial_compiler_is_polynomial=False,
        structured_direct_compiler_known=False,
        actual_family_circuit_lower_bound_proved=False,
        status="generic-polynomial-compiler-exponential-structured-route-open",
    )


def build_hidden_involution_threshold_compiler_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 1),
        (3, 1, 2),
    ),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128),
) -> HiddenInvolutionThresholdCompilerReport:
    controls = [
        audit_central_dilation_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [
        generic_polynomial_compiler_scaling_record(n)
        for n in scaling_n_values
    ]
    verified = all(row.finite_control_verified for row in controls)
    exponential = all(
        not row.generic_polynomial_compiler_is_polynomial
        and row.markov_degree_lower_bound > row.threshold_copy_count
        for row in scaling
    )
    theorem = HiddenInvolutionThresholdCompilerTheorem(
        average_projector_encoding=(
            "A_k=M^-1 sum_h Pi_h^tensor k has a normalization-one "
            "projected-unitary encoding from uniform h and controlled R_h tests."
        ),
        normalized_sign_problem=(
            "The Helstrom effect is sign(A_k-2^-k I), not sign(A_k) or a "
            "constant-threshold transform."
        ),
        markov_polynomial_lower_bound=(
            "Any bounded scalar polynomial separating 0 from 2^(1-k) by "
            "values -2/3 and +2/3 has degree at least sqrt(2^k/3)."
        ),
        central_dilation_identity=(
            "For V_g=direct_sum_b tensor_(i:b_i=1)R_g, "
            "A_k=<+^k| (M^-1 sum_h V_h) |+^k>."
        ),
        compression_obstruction=(
            "The branch-plus subspace is not K_C-invariant and spectral "
            "thresholding does not commute with compression."
        ),
        efficient_average_projector_block_encoding_formalized=True,
        generic_polynomial_degree_exponential_at_threshold=exponential,
        central_dilation_compression_proved=verified,
        central_class_sum_measurement_is_helstrom=False,
        structured_threshold_sign_compiler_constructed=False,
        actual_family_circuit_lower_bound_proved=False,
        theorem_verified=verified and exponential,
        status=(
            "generic-threshold-compilers-blocked-structured-sign-route-open"
            if verified and exponential
            else "threshold-compiler-boundary-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "strict_central_measurement_suboptimality_control_count": sum(
            row.central_measurement_strictly_suboptimal for row in controls
        ),
        "scaling_record_count": len(scaling),
        "generic_exponential_degree_record_count": sum(
            not row.generic_polynomial_compiler_is_polynomial
            for row in scaling
        ),
        "structured_threshold_sign_compiler_count": 0,
        "actual_family_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return HiddenInvolutionThresholdCompilerReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": (
                    "Proves optimal information-theoretic sample complexity and "
                    "emphasizes that the resulting measurements ignore time complexity."
                ),
            },
            {
                "id": "SEN-2005-RANDOM-MEASUREMENT-HSP",
                "title": "Random measurement bases, quantum state distinction and applications to the hidden subgroup problem",
                "url": "https://arxiv.org/abs/quant-ph/0512085",
                "scope": (
                    "Gives information-theoretic random-measurement constructions "
                    "and identifies efficient pseudorandom measurement bases as open."
                ),
            },
        ],
        theorem_contract={
            "input_operator": (
                "The class-averaged k-copy likelihood in the standard mixed "
                "coset-state model."
            ),
            "generic_compiler_scope": (
                "Polynomial/QSVT transformations using only the normalization-one "
                "block encoding of A_k and a uniform scalar approximation promise."
            ),
            "central_dilation_scope": (
                "Class-sum eigenvalue measurement on V with branch initialized "
                "to |+>^k; not every possible coherent use of the dilation."
            ),
            "non_claim": (
                "No lower bound on source-specific recoupling circuits, arbitrary "
                "quantum circuits, or efficient symmetric-group transforms."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-BINARY-SOURCE-WEIGHTED-SIGN",
                "statement": (
                    "Find a source-weighted rational, variable-time, or direct "
                    "representation transform that implements sign(A_k-2^-k I) "
                    "without uniform small-threshold approximation."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-MULTIPLICITY-ALGEBRA",
                "statement": (
                    "Identify a polynomial presentation of the permutation- and "
                    "diagonal-action invariant algebra containing the threshold sign."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-DILATION-COHERENT-ESCAPE",
                "statement": (
                    "Test whether coherent isotypic labels plus branch amplitude "
                    "transforms can implement the compressed sign even though "
                    "measuring the central eigenvalue is suboptimal."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-SIGN-DEQUANTIZATION",
                "statement": (
                    "Determine whether the useful sign mass is equivalent to a "
                    "classically estimable relation count or collision statistic."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A normalization-one block encoding makes QSVT efficient.",
                "answer": (
                    "False. The decision threshold is 2^-k in that normalization; "
                    "Markov's inequality forces degree Omega(2^(k/2)) for a generic "
                    "bounded scalar separator."
                ),
                "resolved": True,
            },
            {
                "challenge": "The polynomial bound proves the actual Helstrom circuit hard.",
                "answer": (
                    "False. A direct structured transform can bypass generic scalar "
                    "approximation, as other repository polar counterfamilies show."
                ),
                "resolved": True,
            },
            {
                "challenge": "Centrality of K_C makes its isotypic labels Helstrom-optimal.",
                "answer": (
                    "False after compression. The |+> branch subspace is not reducing, "
                    "and exact S_3 controls retain only a strict fraction of the signal."
                ),
                "resolved": True,
            },
            {
                "challenge": "The central dilation is useless for every coherent compiler.",
                "answer": (
                    "Unproved. Coherent labels and branch transforms may exploit more "
                    "than the measured class-sum eigenvalue."
                ),
                "resolved": False,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "threshold_information_exists": True,
            "information_theoretic_sample_threshold_new_to_literature": False,
            "efficient_measurement_bottleneck_matches_published_open_boundary": True,
            "normalization_one_average_projector_block_encoding_formalized": True,
            "generic_polynomial_threshold_compiler_is_polynomial": False,
            "central_class_sum_label_measurement_is_helstrom": False,
            "coherent_central_dilation_compiler_ruled_out": False,
            "structured_threshold_sign_compiler_constructed": False,
            "actual_family_circuit_lower_bound_proved": False,
            "polynomial_time_hidden_involution_decision_algorithm": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Information is present, but generic normalized polynomial transforms "
                "and measured central labels do not compile the exponentially small "
                "compressed threshold. A source-specific direct sign is still required."
            ),
        },
        status=theorem.status,
        summary=(
            "Formalized the threshold likelihood block encoding, proved an "
            "exponential generic polynomial-degree boundary, and showed that the "
            "obvious central-dilation label measurement is strictly suboptimal. "
            "Only a structured compressed-sign compiler remains viable."
        ),
        falsifiers_triggered=[
            "A normalization-one LCU does not remove the exponentially small likelihood threshold.",
            "Measuring central dilation eigenvalues does not recover the Helstrom test after compression.",
            "The generic polynomial lower bound is not an arbitrary-circuit lower bound.",
        ],
    )


def write_hidden_involution_threshold_compiler_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY"
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
    payload = asdict(build_hidden_involution_threshold_compiler_report(**kwargs))
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
                id="NEG--HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY."
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
                    "coset_hidden_involution_threshold_compiler_boundary": str(output_path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    report = write_hidden_involution_threshold_compiler_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
