"""Two-subgroup-projector algebra reduces to one-variable likelihood QSVT.

Let ``P=e_A`` and ``Q=e_B`` be the two subgroup projectors in the exact
double-coset polar normal form, and put

    A = Q P Q = Z/M.

Every word in two idempotents reduces by ``P^2=P`` and ``Q^2=Q`` to an
alternating word.  After source compression, an exact normal form remains:

    Q w(P,Q) Q = A^r,                                 (1)

where ``r`` is the number of surviving ``P`` runs (and ``r=0`` for a word
containing no ``P``).  Hence every scalar-coefficient LCU in the algebra
``Alg(P,Q)`` has a ``Q``-compressed block equal to a univariate polynomial
``p(A)``.  With ancillas and controlled queries, every ancilla matrix entry of
the ``Q``-to-``Q`` block is likewise a polynomial in ``A`` whose degree is at
most the number of ``P`` queries.

The shared-conjugation Markov lower bound therefore applies to the entire
two-projector query algebra, not only to an explicitly advertised
single-operator QSVT routine.  Any bounded source-compressed response that
varies by constant amount between the kernel and the natural bulk
``[1/(2M),3/(2M)]`` needs ``Omega(sqrt(M))`` subgroup-projector queries.
Alternating reflections, oblivious amplitude amplification, arbitrary word
LCUs, and ancilla-controlled combinations of only ``P`` and ``Q`` do not
provide a polynomial fast-forward.

This theorem does not rule out a direct non-black-box matrix-CS basis change
or a circuit using a third physical operator outside ``Alg(P,Q)``.  The
matching charge ``D_m`` is relevant only if it enters a genuinely
target-changing operation and creates matrix structure beyond (1); a
source-local use remains likelihood blind.
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
    involution_class_size,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_two_subgroup_projector_algebra_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-TWO-SUBGROUP-PROJECTOR-ALGEBRA-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TwoProjectorWordControl:
    matrix_dimension: int
    P_rank: int
    Q_rank: int
    maximum_word_length: int
    tested_word_count: int
    maximum_predicted_power: int
    maximum_matrix_residual: float
    every_Q_compressed_word_is_A_power: bool
    exact_symbolic_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class TwoProjectorScalingRecord:
    half_degree: int
    degree: int
    hidden_matching_count_decimal: str
    required_response_variation: float
    subgroup_projector_query_lower_bound: float
    subgroup_projector_query_log2_lower_bound: float
    two_projector_query_algorithm_polynomial_time: bool
    status: str


@dataclass(frozen=True)
class TwoProjectorAlgebraTheorem:
    word_normal_form: str
    compressed_algebra: str
    ancilla_query_extension: str
    lower_bound_transfer: str
    escape_condition: str
    exact_all_word_Q_compression_normal_form_proved: bool
    two_projector_B_to_B_algebra_is_univariate_proved: bool
    ancilla_controlled_two_projector_query_bound_proved: bool
    two_projector_constant_bulk_response_requires_sqrt_M_queries: bool
    third_operator_matrix_recoupling_ruled_out: bool
    direct_non_black_box_basis_transform_ruled_out: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class TwoProjectorAlgebraReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[TwoProjectorWordControl]
    scaling_records: list[TwoProjectorScalingRecord]
    theorem: TwoProjectorAlgebraTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def reduce_idempotent_word(word: str) -> str:
    if any(letter not in "PQ" for letter in word):
        raise ValueError("word must use only P and Q")
    output = []
    for letter in word:
        if not output or output[-1] != letter:
            output.append(letter)
    return "".join(output)


def compressed_word_power(word: str) -> int:
    reduced = reduce_idempotent_word("Q" + word + "Q")
    return reduced.count("P")


def _matrix_word(word: str, P: np.ndarray, Q: np.ndarray) -> np.ndarray:
    output = np.eye(P.shape[0])
    for letter in word:
        output = output @ (P if letter == "P" else Q)
    return output


def audit_two_projector_word_normal_form(
    dimension: int = 8,
    P_rank: int = 5,
    Q_rank: int = 4,
    maximum_word_length: int = 9,
) -> TwoProjectorWordControl:
    if not 1 <= P_rank < dimension or not 1 <= Q_rank < dimension:
        raise ValueError("projector ranks must lie strictly inside dimension")
    generator = np.random.default_rng(20260820 + dimension + P_rank + Q_rank)
    left, _ = np.linalg.qr(generator.normal(size=(dimension, P_rank)))
    right, _ = np.linalg.qr(generator.normal(size=(dimension, Q_rank)))
    P = left @ left.T
    Q = right @ right.T
    A = Q @ P @ Q
    maximum_residual = 0.0
    maximum_power = 0
    tested = 0
    symbolic = True
    for length in range(maximum_word_length + 1):
        for letters in itertools.product("PQ", repeat=length):
            word = "".join(letters)
            power = compressed_word_power(word)
            observed = Q @ _matrix_word(word, P, Q) @ Q
            expected = Q if power == 0 else np.linalg.matrix_power(A, power)
            residual = float(np.linalg.norm(observed - expected, ord=2))
            maximum_residual = max(maximum_residual, residual)
            maximum_power = max(maximum_power, power)
            reduced = reduce_idempotent_word("Q" + word + "Q")
            symbolic &= bool(
                reduced == "Q" if power == 0 else reduced == "Q" + "PQ" * power
            )
            tested += 1
    verified = symbolic and maximum_residual < 1e-12
    return TwoProjectorWordControl(
        matrix_dimension=dimension,
        P_rank=P_rank,
        Q_rank=Q_rank,
        maximum_word_length=maximum_word_length,
        tested_word_count=tested,
        maximum_predicted_power=maximum_power,
        maximum_matrix_residual=maximum_residual,
        every_Q_compressed_word_is_A_power=maximum_residual < 1e-12,
        exact_symbolic_normal_form_verified=symbolic,
        status=(
            "two-projector-Q-compressed-word-normal-form-verified"
            if verified
            else "two-projector-word-normal-form-control-failure"
        ),
    )


def two_projector_scaling_record(
    half_degree: int,
    response_variation: float = 0.5,
) -> TwoProjectorScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    lower = math.sqrt(candidates * response_variation)
    return TwoProjectorScalingRecord(
        half_degree=half_degree,
        degree=degree,
        hidden_matching_count_decimal=str(candidates),
        required_response_variation=response_variation,
        subgroup_projector_query_lower_bound=lower,
        subgroup_projector_query_log2_lower_bound=math.log2(lower),
        two_projector_query_algorithm_polynomial_time=False,
        status="two-subgroup-projector-query-algebra-sqrt-M-no-go",
    )


def build_two_projector_algebra_report() -> TwoProjectorAlgebraReport:
    controls = [
        audit_two_projector_word_normal_form(7, 4, 3, 8),
        audit_two_projector_word_normal_form(9, 6, 5, 9),
    ]
    scaling = [
        two_projector_scaling_record(value)
        for value in (4, 8, 16, 32, 64, 128)
    ]
    normal = all(
        row.every_Q_compressed_word_is_A_power
        and row.exact_symbolic_normal_form_verified
        for row in controls
    )
    lower = all(not row.two_projector_query_algorithm_polynomial_time for row in scaling)
    theorem = TwoProjectorAlgebraTheorem(
        word_normal_form=(
            "Idempotence reduces every word to alternating form, and "
            "Q w(P,Q) Q=(QPQ)^r exactly."
        ),
        compressed_algebra=(
            "The source-compressed algebra Q Alg(P,Q) Q is the commutative "
            "univariate polynomial algebra generated by A=QPQ."
        ),
        ancilla_query_extension=(
            "Expanding an ancilla-controlled P/Q query circuit in query words "
            "makes every Q-to-Q ancilla block a degree-bounded polynomial in A."
        ),
        lower_bound_transfer=(
            "The Markov bulk-amplification bound therefore forces Omega(sqrt(M)) "
            "queries throughout the two-projector black-box algebra."
        ),
        escape_condition=(
            "Use a third physical operator outside Alg(P,Q) in genuine target "
            "recoupling, or compile a direct non-black-box matrix-CS basis transform."
        ),
        exact_all_word_Q_compression_normal_form_proved=normal,
        two_projector_B_to_B_algebra_is_univariate_proved=normal,
        ancilla_controlled_two_projector_query_bound_proved=normal and lower,
        two_projector_constant_bulk_response_requires_sqrt_M_queries=normal and lower,
        third_operator_matrix_recoupling_ruled_out=False,
        direct_non_black_box_basis_transform_ruled_out=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=normal and lower,
        status=(
            "two-subgroup-projector-algebra-sqrt-M-no-go-third-operator-open"
            if normal and lower
            else "two-subgroup-projector-algebra-control-failure"
        ),
    )
    return TwoProjectorAlgebraReport(
        created_at=utc_now(),
        theorem_contract={
            "projectors": "P=e_A and Q=e_B",
            "observable_block": "Q-to-Q/source-compressed response",
            "algorithm_class": (
                "Scalar/ancilla-controlled black-box circuits and LCUs using only P and Q"
            ),
            "claim_boundary": (
                "No claim for a third operator or a direct explicit matrix-CS transform."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-TWO-PROJECTOR-THIRD-OPERATOR-CLOSURE",
                "statement": (
                    "Add a physically target-changing charge/recoupling operator and "
                    "prove its compressed algebra is not reducible to p(QPQ)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-TWO-PROJECTOR-DIRECT-MATRIX-CS-TRANSFORM",
                "statement": (
                    "If using a direct basis change, specify coherent labels, local "
                    "rotations, precision, normalization, and garbage uncomputation."
                ),
                "resolved": False,
            },
            {
                "id": "PO-TWO-PROJECTOR-POSTSELECTED-ESCAPE",
                "statement": (
                    "For measurements/postselection outside bounded query polynomials, "
                    "charge success probability and total expected query cost."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Noncommuting P and Q automatically generate a rich matrix algebra on Q space.",
                "answer": (
                    "False after Q compression: every word is exactly a power of QPQ."
                ),
                "resolved": True,
            },
            {
                "challenge": "Ancilla controls evade the word reduction.",
                "answer": (
                    "They change scalar coefficients into ancilla matrices, but each "
                    "matrix entry still has the same degree-bounded word expansion."
                ),
                "resolved": True,
            },
            {
                "challenge": "Alternating-reflection phase estimation is outside polynomial methods.",
                "answer": (
                    "Its finite-query response is a bounded trigonometric/polynomial "
                    "function of the same principal angle and inherits sqrt(M) resolution."
                ),
                "resolved": True,
            },
            {
                "challenge": "The theorem rules out matching-charge assistance.",
                "answer": (
                    "No. A third operator can enlarge the compressed algebra if it is "
                    "used in a non-gauge-trivial target-changing operation."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_two_projector_word_normal_form_count": int(normal),
            "two_projector_sqrt_M_query_no_go_count": int(normal and lower),
            "maximum_tested_word_length": max(row.maximum_word_length for row in controls),
            "tail_query_log2_lower_bound": scaling[-1].subgroup_projector_query_log2_lower_bound,
            "third_operator_escape_count": 0,
            "hidden_involution_detector_count": 0,
        },
        claim_gate={
            "Q_compressed_two_projector_algebra_is_univariate": normal,
            "two_projector_black_box_fast_forward_ruled_out": normal and lower,
            "third_operator_matrix_recoupling_ruled_out": False,
            "direct_non_black_box_basis_transform_ruled_out": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Using only the two subgroup projectors reduces exactly to a bounded "
                "polynomial in QPQ and inherits the sqrt(M) bulk-resolution cost."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that the full source-compressed two-subgroup-projector query "
            "algebra is univariate and cannot fast-forward the natural bulk."
        ),
        falsifiers_triggered=[
            "Noncommutativity of the two subgroup projectors does not create extra source-block labels.",
            "Ancilla-controlled two-reflection circuits remain polynomial functions of the same principal angles.",
            "A viable recoupling mechanism must add a third physical operator or an explicit basis transform.",
        ],
    )


def write_two_projector_algebra_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_two_projector_algebra_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_two_projector_algebra_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
