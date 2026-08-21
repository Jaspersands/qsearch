"""Exact no-go for low-bit-only polynomial witness lists in DCP subset sum.

Split a density-one modular subset-sum instance modulo ``2^n`` at bit ``b``:

    a_i = l_i + 2^b h_i,       t = l_t + 2^b h_t,

where, conditioned on all low parts, the ``h_i`` and ``h_t`` remain
independent uniform residues modulo ``Q=2^(n-b)``.  A low-bit algorithm may
use ``(l_1,...,l_m,l_t)`` and target-independent random coins to output an
explicit list ``L`` of binary assignments.  For each selected assignment
``x``, its full high equation is

    sum_i h_i x_i = h_t - carry_x  (mod Q).

Because ``h_t`` is still uniform and unseen by the selector, this equation
holds with probability exactly ``1/Q`` whenever the low equation is valid.
The union bound is therefore an exact source-law theorem:

    Pr[some listed x is a full witness] <= E|L| / Q.       (1)

For ``m=n+r``, write ``lambda=2^r``.  The exact first and second fiber
moments give the Paley--Zygmund legal-input lower bound

    Pr[target is legal] >= lambda/[1+lambda(1-2^-m)].      (2)

Combining (1)-(2), conditional legal success is at most

    [1+lambda(1-2^-m)] E|L| / (lambda Q).                 (3)

Thus ``b=O(log n)`` and polynomial list size leave success
``2^(-n+O(log n))``.  Exact low-bit BDDs, carry tables, vulnerable-coordinate
lists, and low-only marker filters do not become a Regev-compatible solver by
enumerating polynomially many witnesses.

The theorem deliberately does not cover a joint low/high lattice basis, an
implicit high-dimensional quantum state processed coherently with the high
labels, or a selector whose decisions genuinely use the high parts.  Those
are the remaining admissible mechanisms.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from research_registry import utc_now


REPORT_PATH = Path(
    "research/classical_baselines/dcp_low_bit_candidate_list_no_go.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-LOW-BIT-CANDIDATE-LIST-NO-GO"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class LowBitListScalingRecord:
    n_bits: int
    register_offset: int
    register_count: int
    low_bit_log_multiplier: int
    low_bits: int
    quotient_bits: int
    polynomial_list_exponent: int
    list_size_upper_bound: int
    mean_fiber_multiplicity: int
    legal_probability_lower_bound: float
    unconditional_success_upper_bound: float
    conditional_legal_success_upper_bound: float
    log2_conditional_legal_success_upper_bound: float
    exponentially_small_success: bool
    status: str


@dataclass(frozen=True)
class ExactLowBitListControl:
    n_bits: int
    low_bits: int
    register_count: int
    low_labels: tuple[int, ...]
    target_low: int
    selected_assignment_count: int
    valid_low_assignment_count: int
    quotient_modulus: int
    enumerated_high_instance_count: int
    successful_high_instance_count: int
    exact_success_probability: float
    union_bound: float
    bound_residual: float
    exact_low_bit_list_bound_verified: bool
    status: str


@dataclass(frozen=True)
class LowBitCandidateListNoGoTheorem:
    conditional_product_law: str
    per_candidate_probability: str
    list_success_bound: str
    legal_probability_bound: str
    conditional_legal_bound: str
    asymptotic_consequence: str
    scope_limit: str
    arbitrary_low_selector: bool
    arbitrary_target_independent_random_coins: bool
    arbitrary_polynomial_list: bool
    low_bit_only_polynomial_list_solver_eliminated: bool
    joint_low_high_geometry_eliminated: bool
    coherent_implicit_decoder_eliminated: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class LowBitCandidateListNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[ExactLowBitListControl]
    scaling_records: list[LowBitListScalingRecord]
    theorem: LowBitCandidateListNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def legal_probability_lower_bound(n_bits: int, register_offset: int) -> float:
    if n_bits < 1 or register_offset < 0:
        raise ValueError("invalid subset-sum dimensions")
    register_count = n_bits + register_offset
    mean = 1 << register_offset
    return mean / (1.0 + mean * (1.0 - 2.0 ** (-register_count)))


def conditional_legal_list_success_upper_bound(
    n_bits: int,
    register_offset: int,
    low_bits: int,
    expected_list_size: float,
) -> float:
    if not 1 <= low_bits < n_bits:
        raise ValueError("low_bits must lie strictly between zero and n_bits")
    if expected_list_size < 0:
        raise ValueError("expected list size must be nonnegative")
    quotient = 1 << (n_bits - low_bits)
    legal_lower = legal_probability_lower_bound(n_bits, register_offset)
    return min(1.0, expected_list_size / (quotient * legal_lower))


def low_bit_list_scaling_record(
    n_bits: int,
    register_offset: int,
    low_bit_log_multiplier: int,
    polynomial_list_exponent: int,
) -> LowBitListScalingRecord:
    if n_bits < 4 or register_offset < 0:
        raise ValueError("invalid scaling dimensions")
    if low_bit_log_multiplier < 1 or polynomial_list_exponent < 0:
        raise ValueError("invalid polynomial exponents")
    low_bits = min(
        n_bits - 1,
        math.ceil(low_bit_log_multiplier * math.log2(n_bits)),
    )
    quotient_bits = n_bits - low_bits
    list_size = n_bits**polynomial_list_exponent
    quotient = 1 << quotient_bits
    legal_lower = legal_probability_lower_bound(n_bits, register_offset)
    unconditional = min(1.0, list_size / quotient)
    conditional = min(1.0, unconditional / legal_lower)
    log2_conditional = math.log2(conditional) if conditional > 0 else -math.inf
    return LowBitListScalingRecord(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=n_bits + register_offset,
        low_bit_log_multiplier=low_bit_log_multiplier,
        low_bits=low_bits,
        quotient_bits=quotient_bits,
        polynomial_list_exponent=polynomial_list_exponent,
        list_size_upper_bound=list_size,
        mean_fiber_multiplicity=1 << register_offset,
        legal_probability_lower_bound=legal_lower,
        unconditional_success_upper_bound=unconditional,
        conditional_legal_success_upper_bound=conditional,
        log2_conditional_legal_success_upper_bound=log2_conditional,
        exponentially_small_success=(
            quotient_bits - polynomial_list_exponent * math.log2(n_bits)
            >= n_bits / 2
        ),
        status="low-bit-polynomial-list-success-exponentially-small",
    )


def _low_valid_assignments(
    low_labels: Sequence[int],
    target_low: int,
    low_modulus: int,
) -> list[tuple[int, ...]]:
    return [
        bits
        for bits in itertools.product((0, 1), repeat=len(low_labels))
        if (sum(label * bit for label, bit in zip(low_labels, bits)) - target_low)
        % low_modulus
        == 0
    ]


def audit_exact_low_bit_list_bound(
    n_bits: int,
    low_bits: int,
    low_labels: tuple[int, ...],
    target_low: int,
    selected_assignment_count: int,
) -> ExactLowBitListControl:
    if not 1 <= low_bits < n_bits:
        raise ValueError("invalid low-bit split")
    low_modulus = 1 << low_bits
    quotient = 1 << (n_bits - low_bits)
    if not low_labels or any(not 0 <= label < low_modulus for label in low_labels):
        raise ValueError("low labels must be canonical and nonempty")
    if not 0 <= target_low < low_modulus or selected_assignment_count < 0:
        raise ValueError("invalid target or list size")
    valid = _low_valid_assignments(low_labels, target_low, low_modulus)
    selected = valid[:selected_assignment_count]
    total = quotient ** (len(low_labels) + 1)
    successes = 0
    for values in itertools.product(range(quotient), repeat=len(low_labels) + 1):
        high_labels = values[:-1]
        target_high = values[-1]
        solved = False
        for assignment in selected:
            carry = (
                sum(label * bit for label, bit in zip(low_labels, assignment))
                - target_low
            ) // low_modulus
            if (
                sum(label * bit for label, bit in zip(high_labels, assignment))
                - target_high
                + carry
            ) % quotient == 0:
                solved = True
                break
        successes += int(solved)
    probability = successes / total
    union = min(1.0, len(selected) / quotient)
    residual = max(0.0, probability - union)
    verified = residual <= 1e-12
    return ExactLowBitListControl(
        n_bits=n_bits,
        low_bits=low_bits,
        register_count=len(low_labels),
        low_labels=low_labels,
        target_low=target_low,
        selected_assignment_count=len(selected),
        valid_low_assignment_count=len(valid),
        quotient_modulus=quotient,
        enumerated_high_instance_count=total,
        successful_high_instance_count=successes,
        exact_success_probability=probability,
        union_bound=union,
        bound_residual=residual,
        exact_low_bit_list_bound_verified=verified,
        status=(
            "exact-low-bit-list-union-bound-verified"
            if verified
            else "exact-low-bit-list-control-failure"
        ),
    )


def low_bit_candidate_list_no_go_theorem() -> LowBitCandidateListNoGoTheorem:
    return LowBitCandidateListNoGoTheorem(
        conditional_product_law=(
            "conditioned on all low labels and target low bits, all high labels and "
            "the target high part remain independent uniform modulo 2^(n-b)"
        ),
        per_candidate_probability=(
            "every low-selected assignment satisfying the low equation solves the full equation with probability 2^-(n-b)"
        ),
        list_success_bound="Pr[listed full witness]<=E|L|/2^(n-b)",
        legal_probability_bound=(
            "Paley-Zygmund gives Pr[legal]>=lambda/[1+lambda(1-2^-m)], lambda=2^(m-n)"
        ),
        conditional_legal_bound=(
            "Pr[listed witness | legal]<=[1+lambda(1-2^-m)]E|L|/[lambda 2^(n-b)]"
        ),
        asymptotic_consequence=(
            "b=O(log n) and |L|=poly(n) imply conditional success 2^(-n+O(log n))"
        ),
        scope_limit=(
            "Joint low/high geometry, high-dependent selection, and coherent implicit "
            "processing of the complete low fiber are not covered."
        ),
        arbitrary_low_selector=True,
        arbitrary_target_independent_random_coins=True,
        arbitrary_polynomial_list=True,
        low_bit_only_polynomial_list_solver_eliminated=True,
        joint_low_high_geometry_eliminated=False,
        coherent_implicit_decoder_eliminated=False,
        theorem_verified=True,
        status="low-bit-only-explicit-polynomial-list-route-eliminated",
    )


def run_low_bit_candidate_list_no_go() -> LowBitCandidateListNoGoReport:
    controls = [
        audit_exact_low_bit_list_bound(4, 2, (0, 1, 2), 1, 1),
        audit_exact_low_bit_list_bound(4, 2, (1, 1, 3), 2, 2),
        audit_exact_low_bit_list_bound(5, 3, (1, 2, 4), 3, 3),
    ]
    scaling = [
        low_bit_list_scaling_record(n_bits, offset, multiplier, list_exponent)
        for n_bits, offset, multiplier, list_exponent in (
            (64, 0, 1, 2),
            (128, 2, 2, 3),
            (256, 4, 2, 4),
            (512, 4, 3, 5),
            (1024, 4, 3, 6),
        )
    ]
    theorem = low_bit_candidate_list_no_go_theorem()
    failures = sum(not row.exact_low_bit_list_bound_verified for row in controls)
    exact = bool(failures == 0 and theorem.theorem_verified)
    return LowBitCandidateListNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "conditional_product_law": theorem.conditional_product_law,
            "list_bound": theorem.list_success_bound,
            "legal_bound": theorem.legal_probability_bound,
            "conditional_consequence": theorem.conditional_legal_bound,
            "scope": theorem.scope_limit,
        },
        exact_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "decide_whether_polynomial_low_bit_state_representation_yields_polynomial_witness_list",
                "resolved": exact,
                "resolution": (
                    "Each low-selected witness pays one independent high-target equation, "
                    "so a polynomial list retains exponentially small success."
                ),
            },
            {
                "obligation": "preserve_the_uniform_legal_target_contract",
                "resolved": exact,
                "resolution": (
                    "The exact second-moment legal lower bound is constant for every fixed "
                    "register offset, so legal conditioning cannot remove the exponent."
                ),
            },
            {
                "obligation": "construct_joint_low_high_or_coherent_implicit_decoder",
                "resolved": False,
                "resolution": (
                    "A viable preconditioner must use high labels jointly or process the "
                    "complete low-fiber superposition without explicit enumeration."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The selector can use arbitrary nonlinear low-bit processing.",
                "resolved": True,
                "resolution": (
                    "Equation (1) conditions on the selector's entire low transcript; only "
                    "independence of the unseen high target is used."
                ),
            },
            {
                "objection": "Conditioning on legal targets could make every listed row succeed.",
                "resolved": True,
                "resolution": (
                    "Conditional success is bounded by the unconditional union bound divided "
                    "by a constant Paley-Zygmund lower bound for legality."
                ),
            },
            {
                "objection": "Randomized low-bit candidate generation evades the theorem.",
                "resolved": True,
                "resolution": (
                    "Condition on target-independent coins and average; expected list size replaces deterministic size."
                ),
            },
            {
                "objection": "The theorem rules out the proposed joint lattice preconditioner.",
                "resolved": True,
                "resolution": (
                    "False. A basis using high coefficients or coherent processing of an implicit "
                    "fiber lies outside the low-only explicit-list model."
                ),
            },
        ],
        headline_metrics={
            "low_bit_candidate_list_no_go_theorem_count": int(exact),
            "exact_control_count": len(controls),
            "exact_control_failure_count": failures,
            "scaling_record_count": len(scaling),
            "largest_scaling_n_bits": scaling[-1].n_bits,
            "largest_scale_log2_conditional_success_upper_bound": (
                scaling[-1].log2_conditional_legal_success_upper_bound
            ),
            "joint_low_high_decoder_count": 0,
            "coherent_implicit_decoder_count": 0,
            "polynomial_partial_subset_sum_solver_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "low_bit_only_polynomial_explicit_list_survives": False,
            "joint_low_high_preconditioner_survives": True,
            "coherent_implicit_low_fiber_decoder_survives": True,
            "polynomial_partial_subset_sum_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Polynomial low-bit compression leaves an unseen linear-size high target; "
                "every explicit candidate pays the full quotient probability."
            ),
        },
        status=(
            "low-bit-explicit-list-shortcut-falsified-joint-geometry-open"
            if exact
            else "low-bit-list-control-failure"
        ),
        summary=(
            "Proved an exact exponential upper bound for every polynomial witness list "
            "selected from logarithmically many low bits, including legal conditioning."
        ),
        falsifiers_triggered=[
            "Polynomial-size low-bit BDDs do not yield a polynomial full-witness list decoder.",
            "Low-only marker, carry, or vulnerable-coordinate candidate lists retain exponentially small legal success.",
            "A viable 2-adic route must use joint low/high geometry or coherent implicit processing rather than explicit candidates.",
        ],
    )


def write_low_bit_candidate_list_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-LOW-BIT-CANDIDATE-LIST-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_low_bit_candidate_list_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    payload = write_low_bit_candidate_list_no_go_report()
    print(json.dumps(payload["headline_metrics"], indent=2, sort_keys=True))
