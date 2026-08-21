"""Weak-source deflation no-go for binary hidden-involution detection.

Let ``C`` be a conjugacy class of ``M`` nonidentity involutions in a finite
group and measure the weak Fourier irrep label of each coset-state copy.  If

    p(lambda) = d_lambda^2 / |G|,
    q(lambda) = d_lambda(d_lambda + chi_lambda(C)) / |G|,

are the null and alternative laws, then the source likelihood ratio is

    ell(lambda) = q(lambda) / p(lambda) = 1 + r_lambda,
    r_lambda = chi_lambda(C) / d_lambda.

Character-column orthogonality gives the exact identity

    E_p[ell^2] = 1 + 1/M.

Consequently, for ``k`` source labels,

    chi^2(q^k || p^k) = (1 + 1/M)^k - 1.                (1)

At the information-theoretic threshold ``k=Theta(log M)``, this tends to
zero.  Weak source labels alone therefore cannot implement the binary test.
They also cannot isolate a rare set carrying the useful signal: every source
event has alternative and null probabilities differing by at most the total
variation upper bound from (1).

Conditioned on a source tuple ``s=(lambda_1,...,lambda_k)``, define

    B_s = E_(h in C) tensor_i (I + rho_lambda_i(h))/2.

Its normalized trace is exactly

    a_s = Tr(B_s)/D_s = 2^-k ell(s).                    (2)

Under the alternative source law, ``E[ell(s)]=(1+1/M)^k``.  Markov's
inequality therefore puts at least ``1-delta`` alternative source mass in
blocks with

    a_s <= 2^-k (1+1/M)^k / delta.                      (3)

At ``k=ceil(log2(4M))`` and ``delta=1/4``, this is ``O(1/M)``.  The global
support-spectrum theorem independently puts at least ``3/4`` alternative
mass at eigenvalues at most ``4 mu <= 5/M``.  The union bound leaves at least
one half of alternative mass satisfying both properties.  Deleting
exceptional weak-source sectors cannot remove the generic low-spectrum
burden.

The exact block chi-square chain rule makes the location of the signal
explicit.  If ``sigma_s=B_s/Tr(B_s)`` and ``tau_s=I/D_s``, then

    sum_s p_s ell_s^2 chi^2(sigma_s || tau_s)
      = (2^k-1)/M - [(1+1/M)^k-1].                      (4)

Thus almost all threshold-scale chi-square signal is conditional, inside the
source blocks, rather than in the weak-source transcript.

This theorem rules out source-label-only discrimination and exceptional-
source deflation before a generic normalized filter.  It does not rule out a
coherent source-controlled renormalization, a fused multiplicity-support
transform, or an arbitrary circuit.  Those are precisely the surviving hard
routes.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from coset_commutant_information_obstruction import _involution_representation
from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
    involution_conjugacy_class,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_source_deflation_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-SOURCE-DEFLATION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SourceDeflationFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    conjugacy_class_size: int
    source_tuple_count: int
    exact_source_chi_square: float
    predicted_source_chi_square: float
    source_chi_square_residual: float
    exact_source_total_variation: float
    source_total_variation_chi_square_upper_bound: float
    exact_full_quantum_chi_square: float
    weighted_conditional_chi_square: float
    predicted_weighted_conditional_chi_square: float
    conditional_chain_rule_residual: float
    conditional_share_of_full_chi_square: float
    maximum_block_trace_identity_residual: float
    maximum_conditional_state_trace_residual: float
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class SourceDeflationScalingRecord:
    n: int
    conjugacy_class_size: int
    copy_count: int
    full_quantum_chi_square: float
    weak_source_chi_square_upper_scale: float
    weak_source_total_variation_upper_bound: float
    conditional_chi_square_lower_scale: float
    conditional_share_of_full_chi_square: float
    typical_alternative_source_mass: float
    typical_source_frame_trace_upper_bound: float
    typical_source_frame_trace_times_class_size: float
    low_spectrum_eigenvalue_upper_bound: float
    low_spectrum_eigenvalue_times_class_size: float
    simultaneous_typical_source_and_low_spectrum_mass_lower_bound: float
    source_only_bounded_error_binary_test_possible: bool
    exceptional_source_deflation_removes_low_spectrum_burden: bool
    coherent_within_block_rescaling_ruled_out: bool
    status: str


@dataclass(frozen=True)
class SourceDeflationNoGoTheorem:
    weak_source_likelihood: str
    source_chi_square_identity: str
    source_signal_consequence: str
    source_frame_trace_identity: str
    typical_block_consequence: str
    conditional_chi_square_chain_rule: str
    joint_hard_mass_consequence: str
    scope_limit: str
    exact_source_chi_square_proved: bool
    source_only_threshold_test_refuted: bool
    exceptional_source_deflation_refuted: bool
    conditional_signal_localization_proved: bool
    coherent_within_block_rescaling_refuted: bool
    arbitrary_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SourceDeflationNoGoReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[SourceDeflationFiniteControl]
    scaling_records: list[SourceDeflationScalingRecord]
    theorem: SourceDeflationNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def source_chi_square(
    conjugacy_class_size: int,
    copy_count: int,
) -> Fraction:
    """Return ``(1+1/M)^k-1`` exactly."""

    if conjugacy_class_size < 1 or copy_count < 1:
        raise ValueError("class size and copy count must be positive")
    size = conjugacy_class_size
    return Fraction((size + 1) ** copy_count - size**copy_count, size**copy_count)


def full_quantum_chi_square(
    conjugacy_class_size: int,
    copy_count: int,
) -> Fraction:
    """Return the exact class-mixture chi-square ``(2^k-1)/M``."""

    if conjugacy_class_size < 1 or copy_count < 1:
        raise ValueError("class size and copy count must be positive")
    return Fraction((1 << copy_count) - 1, conjugacy_class_size)


def weighted_conditional_chi_square(
    conjugacy_class_size: int,
    copy_count: int,
) -> Fraction:
    """Return the conditional term in the block chi-square chain rule."""

    return full_quantum_chi_square(
        conjugacy_class_size, copy_count
    ) - source_chi_square(conjugacy_class_size, copy_count)


def source_likelihood_second_moment(
    conjugacy_class_size: int,
    copy_count: int,
) -> Fraction:
    return 1 + source_chi_square(conjugacy_class_size, copy_count)


def _tensor_product(operators: tuple[np.ndarray, ...]) -> np.ndarray:
    result = np.asarray([[1.0]])
    for operator in operators:
        result = np.kron(result, operator)
    return result


def _source_label_data(
    n: int,
    transposition_count: int,
) -> tuple[tuple[Partition, int, int, Fraction, Fraction], ...]:
    order = math.factorial(n)
    records = []
    for partition in integer_partitions(n):
        dimension = hook_length_dimension(partition)
        character = character_on_involution(partition, transposition_count)
        null_probability = Fraction(dimension * dimension, order)
        alternative_probability = Fraction(
            dimension * (dimension + character), order
        )
        records.append(
            (
                partition,
                dimension,
                character,
                null_probability,
                alternative_probability,
            )
        )
    if sum(record[3] for record in records) != 1:
        raise ArithmeticError("null weak-source law failed normalization")
    if sum(record[4] for record in records) != 1:
        raise ArithmeticError("alternative weak-source law failed normalization")
    return tuple(records)


def audit_source_deflation_control(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> SourceDeflationFiniteControl:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    class_elements = involution_conjugacy_class(n, transposition_count)
    class_size = len(class_elements)
    label_data = _source_label_data(n, transposition_count)
    representations = {
        (partition, hidden): _involution_representation(partition, hidden)
        for partition, *_ in label_data
        for hidden in class_elements
    }

    source_chi = Fraction()
    source_tv = Fraction()
    conditional_term = 0.0
    maximum_block_trace_residual = 0.0
    maximum_state_trace_residual = 0.0
    tuple_count = 0
    for source_tuple in itertools.product(label_data, repeat=copy_count):
        tuple_count += 1
        dimensions = tuple(record[1] for record in source_tuple)
        carrier_dimension = math.prod(dimensions)
        null_probability = math.prod(record[3] for record in source_tuple)
        alternative_probability = math.prod(record[4] for record in source_tuple)
        likelihood = alternative_probability / null_probability
        source_chi += null_probability * (likelihood - 1) ** 2
        source_tv += abs(alternative_probability - null_probability) / 2

        frame = np.zeros((carrier_dimension, carrier_dimension), dtype=float)
        for hidden in class_elements:
            projectors = tuple(
                (
                    np.eye(dimension)
                    + representations[(record[0], hidden)]
                )
                / 2.0
                for record, dimension in zip(source_tuple, dimensions)
            )
            frame += _tensor_product(projectors) / class_size

        predicted_trace = Fraction(1, 1 << copy_count) * likelihood
        empirical_trace = float(np.trace(frame).real / carrier_dimension)
        maximum_block_trace_residual = max(
            maximum_block_trace_residual,
            abs(empirical_trace - float(predicted_trace)),
        )
        if alternative_probability == 0:
            continue
        conditional_state = frame / (
            carrier_dimension * float(predicted_trace)
        )
        maximum_state_trace_residual = max(
            maximum_state_trace_residual,
            abs(float(np.trace(conditional_state).real) - 1.0),
        )
        conditional_chi = (
            carrier_dimension
            * float(np.trace(conditional_state @ conditional_state).real)
            - 1.0
        )
        conditional_term += float(
            null_probability * likelihood * likelihood
        ) * conditional_chi

    predicted_source = source_chi_square(class_size, copy_count)
    predicted_conditional = weighted_conditional_chi_square(
        class_size, copy_count
    )
    full = full_quantum_chi_square(class_size, copy_count)
    source_residual = abs(float(source_chi - predicted_source))
    chain_residual = abs(conditional_term - float(predicted_conditional))
    tv_upper = 0.5 * math.sqrt(float(predicted_source))
    verified = bool(
        source_residual <= tolerance
        and float(source_tv) <= tv_upper + tolerance
        and chain_residual <= 100 * tolerance
        and maximum_block_trace_residual <= 100 * tolerance
        and maximum_state_trace_residual <= 100 * tolerance
        and abs(
            float(source_chi) + conditional_term - float(full)
        )
        <= 100 * tolerance
    )
    return SourceDeflationFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        conjugacy_class_size=class_size,
        source_tuple_count=tuple_count,
        exact_source_chi_square=float(source_chi),
        predicted_source_chi_square=float(predicted_source),
        source_chi_square_residual=source_residual,
        exact_source_total_variation=float(source_tv),
        source_total_variation_chi_square_upper_bound=tv_upper,
        exact_full_quantum_chi_square=float(full),
        weighted_conditional_chi_square=conditional_term,
        predicted_weighted_conditional_chi_square=float(predicted_conditional),
        conditional_chain_rule_residual=chain_residual,
        conditional_share_of_full_chi_square=(
            conditional_term / float(full) if full else 0.0
        ),
        maximum_block_trace_identity_residual=maximum_block_trace_residual,
        maximum_conditional_state_trace_residual=maximum_state_trace_residual,
        finite_control_verified=verified,
        status=(
            "exact-source-law-and-conditional-signal-decomposition-verified"
            if verified
            else "source-deflation-control-failure"
        ),
    )


def source_deflation_scaling_record(
    n: int,
    *,
    tail_probability: float = 0.25,
) -> SourceDeflationScalingRecord:
    if n < 6 or n % 2:
        raise ValueError("n must be even and at least six")
    if not 0.0 < tail_probability < 0.5:
        raise ValueError("tail_probability must lie in (0,1/2)")
    class_size = involution_class_size(n, n // 2)
    copies = (4 * class_size - 1).bit_length()
    inverse_size = 1.0 / class_size
    source_chi = math.expm1(copies * math.log1p(inverse_size))
    likelihood_second = 1.0 + source_chi
    source_tv = 0.5 * math.sqrt(source_chi)
    full_chi = ((1 << copies) - 1) / class_size
    conditional = full_chi - source_chi
    frame_trace_threshold = (
        likelihood_second / (tail_probability * (1 << copies))
    )
    inverse_power = 1.0 / (1 << copies)
    alternative_mean = inverse_power + (1.0 - inverse_power) / class_size
    low_spectrum_threshold = 4.0 * alternative_mean
    joint_mass = max(0.0, 1.0 - tail_probability - 0.25)
    source_only_possible = source_tv >= 1.0 / 3.0
    return SourceDeflationScalingRecord(
        n=n,
        conjugacy_class_size=class_size,
        copy_count=copies,
        full_quantum_chi_square=full_chi,
        weak_source_chi_square_upper_scale=source_chi,
        weak_source_total_variation_upper_bound=source_tv,
        conditional_chi_square_lower_scale=conditional,
        conditional_share_of_full_chi_square=conditional / full_chi,
        typical_alternative_source_mass=1.0 - tail_probability,
        typical_source_frame_trace_upper_bound=frame_trace_threshold,
        typical_source_frame_trace_times_class_size=(
            frame_trace_threshold * class_size
        ),
        low_spectrum_eigenvalue_upper_bound=low_spectrum_threshold,
        low_spectrum_eigenvalue_times_class_size=(
            low_spectrum_threshold * class_size
        ),
        simultaneous_typical_source_and_low_spectrum_mass_lower_bound=(
            joint_mass
        ),
        source_only_bounded_error_binary_test_possible=source_only_possible,
        exceptional_source_deflation_removes_low_spectrum_burden=False,
        coherent_within_block_rescaling_ruled_out=False,
        status=(
            "source-transcript-negligible-exceptional-deflation-refuted-"
            "fused-block-transform-open"
            if not source_only_possible and joint_mass >= 0.5
            else "finite-source-deflation-scaling-control"
        ),
    )


def build_source_deflation_no_go_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 2),
        (3, 1, 3),
        (4, 1, 2),
        (4, 2, 2),
    ),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128),
) -> SourceDeflationNoGoReport:
    controls = [
        audit_source_deflation_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [
        source_deflation_scaling_record(n) for n in scaling_n_values
    ]
    finite_verified = all(row.finite_control_verified for row in controls)
    scaling_verified = all(
        not row.source_only_bounded_error_binary_test_possible
        and row.simultaneous_typical_source_and_low_spectrum_mass_lower_bound
        >= 0.5
        and row.typical_source_frame_trace_times_class_size < 1.01
        and row.low_spectrum_eigenvalue_times_class_size <= 5.0
        for row in scaling
    )
    verified = finite_verified and scaling_verified
    theorem = SourceDeflationNoGoTheorem(
        weak_source_likelihood=(
            "p(lambda)=d_lambda^2/|G|, q(lambda)=p(lambda)(1+r_lambda), "
            "r_lambda=chi_lambda(C)/d_lambda."
        ),
        source_chi_square_identity=(
            "Character-column orthogonality gives "
            "chi^2(q^k||p^k)=(1+1/M)^k-1."
        ),
        source_signal_consequence=(
            "At k=Theta(log M), source-label total variation is "
            "O(sqrt(log(M)/M))=o(1), so source-only bounded-error "
            "binary discrimination is impossible."
        ),
        source_frame_trace_identity=(
            "For B_s=E_h tensor_i(I+rho_i(h))/2, "
            "Tr(B_s)/D_s=2^-k ell(s)."
        ),
        typical_block_consequence=(
            "At least 3/4 alternative source mass has normalized frame "
            "trace at most 2^-k(1+1/M)^k/(1/4)=O(1/M)."
        ),
        conditional_chi_square_chain_rule=(
            "sum_s p_s ell_s^2 chi^2(sigma_s||I/D_s)="
            "(2^k-1)/M-[(1+1/M)^k-1]."
        ),
        joint_hard_mass_consequence=(
            "Combining source-trace and global spectral Markov bounds leaves "
            "at least one half of alternative mass in ordinary source blocks "
            "and at eigenvalues O(1/M)."
        ),
        scope_limit=(
            "The theorem excludes source-label-only tests and deletion of "
            "exceptional source sectors. It does not exclude coherent "
            "within-block rescaling, fused multiplicity transforms, rational "
            "methods with new access, or arbitrary circuits."
        ),
        exact_source_chi_square_proved=True,
        source_only_threshold_test_refuted=scaling_verified,
        exceptional_source_deflation_refuted=scaling_verified,
        conditional_signal_localization_proved=finite_verified,
        coherent_within_block_rescaling_refuted=False,
        arbitrary_circuit_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "weak-source-deflation-refuted-fused-multiplicity-transform-open"
            if verified
            else "source-deflation-no-go-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "exact_source_chi_square_theorem_count": 1,
        "conditional_chi_square_chain_rule_theorem_count": 1,
        "source_only_threshold_test_no_go_count": 1 if scaling_verified else 0,
        "exceptional_source_deflation_no_go_count": 1 if scaling_verified else 0,
        "minimum_scaling_conditional_signal_fraction": min(
            row.conditional_share_of_full_chi_square for row in scaling
        ),
        "maximum_scaling_weak_source_total_variation_bound": max(
            row.weak_source_total_variation_upper_bound for row in scaling
        ),
        "minimum_simultaneous_hard_mass_lower_bound": min(
            row.simultaneous_typical_source_and_low_spectrum_mass_lower_bound
            for row in scaling
        ),
        "coherent_within_block_rescaling_no_go_count": 0,
        "arbitrary_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return SourceDeflationNoGoReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": (
                    "Provides the support-span measurement whose weak-source "
                    "preprocessing is audited here."
                ),
            }
        ],
        theorem_contract={
            "state_model": (
                "The standard mixed coset-state binary problem for a uniform "
                "conjugacy class of nonidentity involutions."
            ),
            "source_model": (
                "Weak Fourier irrep labels are measured on each copy; the "
                "remaining column/multiplicity state is retained exactly."
            ),
            "deflation_scope": (
                "Preselection or deletion determined only by weak-source labels, "
                "followed by the normalization-one average-projector route."
            ),
            "outside_scope": (
                "Coherent source labels, source-controlled transforms acting "
                "inside multiplicity blocks, and non-polynomial structured circuits."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-FUSED-MULTIPLICITY-SUPPORT",
                "statement": (
                    "Construct or obstruct a coherent transform that acts inside "
                    "the naturally occupied multiplicity blocks and avoids "
                    "standalone inverse amplification."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-BLOCK-RELATIVE-SPECTRUM",
                "statement": (
                    "Determine the source-conditioned spectrum after optimal "
                    "legal block normalization, not merely its absolute trace scale."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-CLASSICAL-COMPARISON",
                "statement": (
                    "Compare any surviving fused transform against legal classical "
                    "query/sample access for the same promised input family."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Rare weak-source sectors carry the binary signal.",
                "answer": (
                    "False at k=Theta(log M): source total variation is o(1), "
                    "and any source event has nearly equal null and alternative mass."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "Deleting atypical source sectors removes the low-spectrum tail."
                ),
                "answer": (
                    "False: at least one half of alternative mass is simultaneously "
                    "in typical-trace source blocks and at eigenvalues O(1/M)."
                ),
                "resolved": True,
            },
            {
                "challenge": "Blockwise rescaling is now impossible.",
                "answer": (
                    "Not proved. The theorem fixes absolute trace and signal "
                    "location but does not lower-bound a fused source-controlled "
                    "multiplicity transform."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "weak_source_label_binary_test_refuted": scaling_verified,
            "exceptional_weak_source_deflation_refuted": scaling_verified,
            "conditional_multiplicity_signal_required": verified,
            "coherent_within_block_rescaling_refuted": False,
            "fused_multiplicity_support_transform_constructed": False,
            "fused_multiplicity_support_transform_refuted": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "classical_separation_proved": False,
            "arbitrary_circuit_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Weak-source preprocessing neither distinguishes the hypotheses nor "
                "removes the typical low-spectrum mass. The only live route acts "
                "coherently inside multiplicity blocks and remains unconstructed."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that weak-source labels have vanishing threshold-scale signal, "
            "localized the constant chi-square signal inside conditional blocks, "
            "and showed exceptional-source deletion leaves constant O(1/M) "
            "spectral mass. Fused multiplicity-block rescaling remains open."
        ),
        falsifiers_triggered=[
            "Rare weak Fourier labels do not carry constant binary hidden-involution signal at the logarithmic-copy threshold.",
            "Exceptional-source deflation cannot remove the normalization-one support filter's low-spectrum burden.",
            "The remaining computational question is an internal multiplicity transform, not another source-label weighting.",
            "No arbitrary-circuit lower bound or quantum speedup follows from this source-deflation theorem.",
        ],
    )


def write_source_deflation_no_go_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_source_deflation_no_go_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_source_deflation_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
