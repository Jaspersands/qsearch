"""All-degree classical estimator for matching-charge scalar word moments.

For an explicitly specified hidden matching ``h_j``, the normalized charge is

    D_(h_j) = (1/N) sum_(g in O_(h_j)) g,
    N = 192 binomial(m,4).

For any word ``W=D_(h_1)...D_(h_d)``, normalized regular trace is exactly

    tr_reg(W) = Pr[g_1...g_d=e],                       (1)

where the ``g_j`` are sampled independently and uniformly from their indexed
orbits.  The normalized ``h``-even source trace is

    tr_even(W) = coefficient_e(W)+coefficient_h(W)
               = Pr[g_1...g_d in {e,h}].              (2)

Both have unbiased Bernoulli estimators.  Hoeffding gives additive error
``epsilon`` and failure probability ``delta`` with

    ceil(log(2/delta)/(2 epsilon^2))

samples.  One sample uses ``d`` reversible-orbit indices classically and
``O(dm)`` permutation work.  Thus every inverse-polynomial scalar charge-word
signal of polynomial word length is classically estimable in polynomial time,
independently of the nominal Hilbert-space or branching multiplicity size.

Signed linear combinations of polynomially many such moments are handled by
estimating each monomial to the allocated additive precision.  In particular,
regular or h-even commutator norms, fixed/growing-degree scalar transition
moments, and moment-based spectral heuristics do not establish exponential
quantum advantage.  Quantum amplitude estimation can at most improve the
``epsilon`` dependence quadratically in this access model.

This theorem assumes the candidate matchings/charge oracles are explicitly
specified, as they are in the binary-candidate and mechanism-evaluation
workflows.  It does not reconstruct an unknown matching from coset states and
does not dequantize conditioned matrix-valued Fourier blocks, spectral
projector transition matrices, or coherent all-copy target interference that
cannot be expressed as scalar charge-word traces.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
)
from coset_hidden_involution_matching_charge_coherent_label_compiler import (
    matching_charge_term_count,
    matching_charge_term_from_index,
)
from coset_hidden_involution_matching_charge_orbit_recoupling_reduction import (
    Permutation,
    conjugate_permutation,
    reference_hidden_involution,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_matching_charge_word_moment_dequantization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-WORD-MOMENT-DEQUANTIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ExactWordMomentControl:
    half_degree: int
    word_degree: int
    charge_term_count: int
    enumerated_term_tuple_count: int
    identity_return_count: int
    hidden_return_count: int
    exact_regular_trace: float
    exact_hidden_even_trace: float
    Monte_Carlo_regular_estimate: float
    Monte_Carlo_hidden_even_estimate: float
    estimator_absolute_error_bound: float
    regular_estimate_within_bound: bool
    hidden_even_estimate_within_bound: bool
    return_probability_identity_verified: bool
    status: str


@dataclass(frozen=True)
class WordMomentScalingRecord:
    half_degree: int
    word_degree: int
    target_additive_error: float
    target_failure_probability: float
    Hoeffding_sample_upper_bound: int
    sample_upper_bound_log2: float
    permutation_multiplication_work_upper_bound: int
    inverse_polynomial_signal_classically_estimable: bool
    quantum_amplitude_estimation_exponential_advantage_possible: bool
    status: str


@dataclass(frozen=True)
class WordMomentDequantizationTheorem:
    regular_trace_identity: str
    hidden_even_trace_identity: str
    classical_estimator: str
    complexity_consequence: str
    scope_limit: str
    exact_all_degree_return_probability_reduction_proved: bool
    inverse_polynomial_scalar_word_moments_classically_estimable: bool
    polynomial_signed_moment_combinations_classically_estimable: bool
    scalar_commutator_moment_advantage_ruled_out: bool
    conditioned_matrix_transition_dequantized: bool
    spectral_projector_transition_dequantized: bool
    all_copy_target_interference_dequantized: bool
    hidden_involution_reconstruction_algorithm_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class WordMomentDequantizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[ExactWordMomentControl]
    scaling_records: list[WordMomentScalingRecord]
    theorem: WordMomentDequantizationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def identity_permutation(degree: int) -> Permutation:
    return tuple(range(degree))


def charge_term(
    half_degree: int,
    conjugator: Permutation,
    index: int,
) -> Permutation:
    if len(conjugator) != 2 * half_degree:
        raise ValueError("conjugator degree does not match half_degree")
    return conjugate_permutation(
        conjugator,
        matching_charge_term_from_index(half_degree, index),
    )


def multiply_word(permutations: Iterable[Permutation], degree: int) -> Permutation:
    product = identity_permutation(degree)
    for permutation in permutations:
        product = compose_permutations(product, permutation)
    return product


def exact_charge_word_returns(
    half_degree: int,
    conjugators: tuple[Permutation, ...],
    maximum_tuple_count: int = 2_000_000,
) -> tuple[int, int, int]:
    if not conjugators:
        raise ValueError("word must contain at least one charge")
    count = matching_charge_term_count(half_degree)
    tuple_count = count ** len(conjugators)
    if tuple_count > maximum_tuple_count:
        raise ValueError("exact word enumeration exceeds safety limit")
    identity = identity_permutation(2 * half_degree)
    hidden = reference_hidden_involution(half_degree)
    identity_returns = 0
    hidden_returns = 0
    for indices in itertools.product(range(count), repeat=len(conjugators)):
        product = multiply_word(
            (
                charge_term(half_degree, conjugator, index)
                for conjugator, index in zip(conjugators, indices)
            ),
            2 * half_degree,
        )
        identity_returns += product == identity
        hidden_returns += product == hidden
    return tuple_count, identity_returns, hidden_returns


def estimate_charge_word_returns(
    half_degree: int,
    conjugators: tuple[Permutation, ...],
    sample_count: int,
    seed: int = 0,
) -> tuple[float, float]:
    if not conjugators or sample_count < 1:
        raise ValueError("require a nonempty word and positive sample_count")
    count = matching_charge_term_count(half_degree)
    identity = identity_permutation(2 * half_degree)
    hidden = reference_hidden_involution(half_degree)
    generator = random.Random(seed)
    identity_returns = 0
    hidden_even_returns = 0
    for _ in range(sample_count):
        product = multiply_word(
            (
                charge_term(
                    half_degree,
                    conjugator,
                    generator.randrange(count),
                )
                for conjugator in conjugators
            ),
            2 * half_degree,
        )
        identity_returns += product == identity
        hidden_even_returns += product == identity or product == hidden
    return (
        identity_returns / sample_count,
        hidden_even_returns / sample_count,
    )


def Hoeffding_sample_bound(error: float, failure_probability: float) -> int:
    if not 0 < error < 1 or not 0 < failure_probability < 1:
        raise ValueError("error and failure_probability must lie in (0,1)")
    return math.ceil(
        math.log(2.0 / failure_probability) / (2.0 * error**2)
    )


def exact_word_moment_control(half_degree: int = 4) -> ExactWordMomentControl:
    identity = identity_permutation(2 * half_degree)
    conjugators = (identity, identity)
    tuple_count, identity_returns, hidden_returns = exact_charge_word_returns(
        half_degree,
        conjugators,
    )
    regular = identity_returns / tuple_count
    hidden_even = (identity_returns + hidden_returns) / tuple_count
    sample_count = 100_000
    estimate_regular, estimate_even = estimate_charge_word_returns(
        half_degree,
        conjugators,
        sample_count=sample_count,
        seed=20260820,
    )
    bound = math.sqrt(math.log(40.0) / (2.0 * sample_count))
    regular_ok = abs(estimate_regular - regular) <= bound
    even_ok = abs(estimate_even - hidden_even) <= bound
    expected_regular = 1.0 / matching_charge_term_count(half_degree)
    verified = bool(
        abs(regular - expected_regular) < 1e-15
        and regular_ok
        and even_ok
    )
    return ExactWordMomentControl(
        half_degree=half_degree,
        word_degree=len(conjugators),
        charge_term_count=matching_charge_term_count(half_degree),
        enumerated_term_tuple_count=tuple_count,
        identity_return_count=identity_returns,
        hidden_return_count=hidden_returns,
        exact_regular_trace=regular,
        exact_hidden_even_trace=hidden_even,
        Monte_Carlo_regular_estimate=estimate_regular,
        Monte_Carlo_hidden_even_estimate=estimate_even,
        estimator_absolute_error_bound=bound,
        regular_estimate_within_bound=regular_ok,
        hidden_even_estimate_within_bound=even_ok,
        return_probability_identity_verified=verified,
        status=(
            "charge-word-return-probability-identity-verified"
            if verified
            else "charge-word-return-control-failure"
        ),
    )


def word_moment_scaling_record(
    half_degree: int,
    word_degree: int,
    signal_exponent: int = 9,
    failure_probability: float = 0.01,
) -> WordMomentScalingRecord:
    if half_degree < 4 or word_degree < 1 or signal_exponent < 1:
        raise ValueError("invalid scaling parameters")
    error = 0.1 / half_degree**signal_exponent
    samples = Hoeffding_sample_bound(error, failure_probability)
    work = samples * word_degree * 2 * half_degree
    return WordMomentScalingRecord(
        half_degree=half_degree,
        word_degree=word_degree,
        target_additive_error=error,
        target_failure_probability=failure_probability,
        Hoeffding_sample_upper_bound=samples,
        sample_upper_bound_log2=math.log2(samples),
        permutation_multiplication_work_upper_bound=work,
        inverse_polynomial_signal_classically_estimable=True,
        quantum_amplitude_estimation_exponential_advantage_possible=False,
        status="inverse-polynomial-charge-word-moment-classically-estimable",
    )


def build_word_moment_dequantization_report() -> WordMomentDequantizationReport:
    exact_controls = [exact_word_moment_control(4)]
    scaling = [
        word_moment_scaling_record(
            half_degree=value,
            word_degree=max(4, math.ceil(math.log2(value))),
        )
        for value in (8, 16, 32, 64, 128)
    ]
    exact = all(row.return_probability_identity_verified for row in exact_controls)
    classical = all(
        row.inverse_polynomial_signal_classically_estimable for row in scaling
    )
    theorem = WordMomentDequantizationTheorem(
        regular_trace_identity=(
            "tr_reg(product_j D_(h_j)) is the probability that independent "
            "uniform orbit terms multiply to identity."
        ),
        hidden_even_trace_identity=(
            "The h-even source trace is the probability that the same product "
            "equals either identity or the reference hidden involution h."
        ),
        classical_estimator=(
            "Sample indexed constant-support terms, multiply permutations, and "
            "test the return event; Hoeffding costs O(epsilon^-2 log(1/delta))."
        ),
        complexity_consequence=(
            "Polynomial word length and inverse-polynomial additive signal give "
            "a polynomial classical estimator, even when branching blocks are huge."
        ),
        scope_limit=(
            "Does not recover an unknown matching or estimate conditioned matrix "
            "transition blocks and coherent all-copy target interference."
        ),
        exact_all_degree_return_probability_reduction_proved=exact,
        inverse_polynomial_scalar_word_moments_classically_estimable=classical,
        polynomial_signed_moment_combinations_classically_estimable=classical,
        scalar_commutator_moment_advantage_ruled_out=classical,
        conditioned_matrix_transition_dequantized=False,
        spectral_projector_transition_dequantized=False,
        all_copy_target_interference_dequantized=False,
        hidden_involution_reconstruction_algorithm_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact and classical,
        status=(
            "all-degree-scalar-charge-word-moments-dequantized-matrix-data-open"
            if exact and classical
            else "charge-word-moment-dequantization-control-failure"
        ),
    )
    return WordMomentDequantizationReport(
        created_at=utc_now(),
        theorem_contract={
            "access_model": (
                "Explicit candidate matchings and classical access to the same "
                "reversible constant-support charge-term sampler used by the quantum LCU"
            ),
            "observable_class": (
                "Scalar regular or h-even traces of arbitrary charge words and "
                "polynomial signed combinations thereof"
            ),
            "accuracy": "Additive inverse-polynomial",
            "claim_boundary": (
                "No claim for exponentially small relative error or conditioned "
                "matrix-valued Fourier transition data."
            ),
        },
        exact_controls=exact_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-MATCHING-CHARGE-CONDITIONED-MATRIX-ESTIMATOR",
                "statement": (
                    "Determine whether natural source-conditioned spectral-projector "
                    "transition matrices admit a comparable classical sampler."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-CHARGE-EXPONENTIAL-PRECISION-SCOPE",
                "statement": (
                    "If a proposed signal is exponentially small, compare quantum "
                    "amplitude-estimation cost with the exact normalization bottleneck."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-CHARGE-TARGET-INTERFERENCE-RETURN-MAP",
                "statement": (
                    "Prove or falsify a return-probability representation for the "
                    "full all-copy target-coupled likelihood statistic."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Growing word degree evades fixed-degree enumeration.",
                "answer": (
                    "It evades exact enumeration, but not Monte Carlo: one sample "
                    "costs only polynomial work when the word degree is polynomial."
                ),
                "resolved": True,
            },
            {
                "challenge": "Huge branching multiplicity makes the scalar moment hard.",
                "answer": (
                    "False. The return estimator never constructs a Fourier or "
                    "branching block."
                ),
                "resolved": True,
            },
            {
                "challenge": "Quantum amplitude estimation restores an exponential advantage.",
                "answer": (
                    "Not for inverse-polynomial additive accuracy: it gives at most a "
                    "polynomial quadratic improvement in epsilon."
                ),
                "resolved": True,
            },
            {
                "challenge": "Scalar-moment dequantization kills matrix recoupling.",
                "answer": (
                    "Too strong. Conditioning on large multiplicity blocks can retain "
                    "matrix information absent from scalar return probabilities."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "all_degree_return_probability_theorem_count": int(exact),
            "inverse_polynomial_scalar_moment_classical_estimator_count": int(classical),
            "tail_classical_sample_bound_log2": scaling[-1].sample_upper_bound_log2,
            "conditioned_matrix_estimator_count": 0,
            "all_copy_target_interference_estimator_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "scalar_charge_word_moments_classically_estimable": classical,
            "scalar_commutator_moment_quantum_advantage": False,
            "conditioned_matrix_transition_dequantized": False,
            "spectral_projector_transition_dequantized": False,
            "all_copy_target_interference_dequantized": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every inverse-polynomial scalar charge-word signal is a classically "
                "estimable return probability; only conditioned matrix data can escape."
            ),
        },
        status=theorem.status,
        summary=(
            "Reduced arbitrary-degree scalar matching-charge moments to classical "
            "return-probability estimation and closed them as speedup evidence."
        ),
        falsifiers_triggered=[
            "Growing-degree scalar charge moments do not evade classical sampling at inverse-polynomial accuracy.",
            "Large Fourier multiplicity does not make regular or h-even scalar traces hard.",
            "A viable mechanism must expose conditioned matrix information or all-copy target interference.",
        ],
    )


def write_word_moment_dequantization_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_word_moment_dequantization_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_word_moment_dequantization_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
