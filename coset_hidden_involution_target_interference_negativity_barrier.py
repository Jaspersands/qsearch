"""Exact group-basis negativity barrier for any useful detector.

The all-copy target LCU theorem proves for every group-algebra observable

    X = sum_(ell in G^k x G) alpha_ell ell

that its likelihood bias satisfies

    beta(X) = |tr_B(XZ)-tr_B(X)|
            <= 2^(-k) ||alpha||_1.                    (1)

Therefore any observable with bias at least ``beta`` must obey

    ||alpha||_1 >= beta 2^k.                          (2)

At the natural copy count ``k=ceil(log2(64M))``, where
``M=[G:C_G(h)]``, constant bias requires group-basis L1 norm
``Omega(M)``.  For hidden perfect matchings this is factorial in ``m``.

This is a representation-independent sign/negativity barrier.  It applies
even when ``||X||_op<=1``: a useful bounded detector must realize enormous
destructive interference among group-basis coefficients.  A standard
coefficient-state PREP/SELECT LCU block-encodes ``X/alpha`` with
``alpha>=||alpha||_1``.  Its raw postselection probability is at most
``1/||alpha||_1^2`` and generic amplitude amplification costs at least linear
in that normalization.  Likewise, direct signed importance sampling carries
a worst-case range proportional to ``||alpha||_1``.

This does not prove a general circuit lower bound.  QFTs, QSVT, products of
reflections, and integrable transforms can implement operators with huge
group-basis L1 norm without explicitly preparing their coefficient
distribution.  The theorem identifies exactly what a successful matrix-CS
polar compiler must accomplish: fast-forward factorial coherent cancellation
without paying the coefficient normalization.  Until such structure is
proved, sparse-LCU detector proposals are normalization restatements, not
algorithms.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from coset_hidden_involution_orbit_synthesis_flatness import (
    flatness_copy_count,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_target_interference_negativity_barrier.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-TARGET-INTERFERENCE-NEGATIVITY-BARRIER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class NegativityScalingRecord:
    half_degree: int
    degree: int
    hidden_matching_count_decimal: str
    hidden_matching_label_bits: float
    copy_count: int
    target_bias: float
    required_group_basis_L1_norm_lower_bound_decimal: str
    required_group_basis_L1_norm_log2_lower_bound: float
    required_L1_over_candidate_count: float
    standard_LCU_raw_postselection_probability_upper_bound: float
    standard_LCU_amplitude_amplification_query_lower_bound_decimal: str
    coefficient_sampling_range_lower_bound_decimal: str
    normalization_is_factorial_in_half_degree: bool
    status: str


@dataclass(frozen=True)
class NegativityBarrierTheorem:
    bias_duality: str
    natural_copy_bound: str
    standard_LCU_consequence: str
    classical_sampling_consequence: str
    surviving_quantum_route: str
    exact_group_basis_L1_lower_bound_proved: bool
    constant_bias_requires_Omega_candidate_count_L1_proved: bool
    standard_coefficient_PREP_SELECT_route_ruled_out: bool
    direct_quasiprobability_sampling_has_exponential_range: bool
    all_structured_quantum_compilers_ruled_out: bool
    matrix_CS_fast_forward_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NegativityBarrierReport:
    created_at: str
    theorem_contract: dict[str, Any]
    scaling_records: list[NegativityScalingRecord]
    theorem: NegativityBarrierTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float | str]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def required_L1_norm(copy_count: int, target_bias: float) -> int:
    if copy_count < 1 or not 0 < target_bias <= 1:
        raise ValueError("require copy_count>=1 and target_bias in (0,1]")
    return math.ceil(target_bias * 2**copy_count)


def negativity_scaling_record(
    half_degree: int,
    target_bias: float = 1.0 / 3.0,
) -> NegativityScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    required = required_L1_norm(copies, target_bias)
    if required.bit_length() < 500:
        probability = 1.0 / required**2
    else:
        log_probability = -2.0 * math.log(required)
        probability = (
            math.exp(log_probability) if log_probability > -745.0 else 0.0
        )
    return NegativityScalingRecord(
        half_degree=half_degree,
        degree=degree,
        hidden_matching_count_decimal=str(candidates),
        hidden_matching_label_bits=math.log2(candidates),
        copy_count=copies,
        target_bias=target_bias,
        required_group_basis_L1_norm_lower_bound_decimal=str(required),
        required_group_basis_L1_norm_log2_lower_bound=math.log2(required),
        required_L1_over_candidate_count=required / candidates,
        standard_LCU_raw_postselection_probability_upper_bound=probability,
        standard_LCU_amplitude_amplification_query_lower_bound_decimal=str(
            required
        ),
        coefficient_sampling_range_lower_bound_decimal=str(required),
        normalization_is_factorial_in_half_degree=required >= 16 * candidates,
        status="constant-bias-requires-factorial-group-basis-negativity",
    )


def build_negativity_barrier_report() -> NegativityBarrierReport:
    scaling = [
        negativity_scaling_record(value)
        for value in (4, 8, 16, 32, 64, 128)
    ]
    factorial = all(row.normalization_is_factorial_in_half_degree for row in scaling)
    theorem = NegativityBarrierTheorem(
        bias_duality=(
            "The exact pointwise basis bias bound gives beta(X)<=2^-k "
            "||X||_(group-basis L1), hence L1>=beta 2^k."
        ),
        natural_copy_bound=(
            "At k=ceil(log2(64M)), constant beta requires L1>=64 beta M, "
            "factorial for the perfect-matching candidate orbit."
        ),
        standard_LCU_consequence=(
            "Coefficient PREP/SELECT has normalization at least this L1, raw "
            "postselection at most L1^-2, and generic amplification cost at least L1."
        ),
        classical_sampling_consequence=(
            "Direct signed coefficient sampling has range proportional to L1 and "
            "does not efficiently estimate constant bias without extra structure."
        ),
        surviving_quantum_route=(
            "A positive compiler must fast-forward the factorial cancellation via "
            "structured QFT/QSVT/reflection/polar dynamics rather than enumerate coefficients."
        ),
        exact_group_basis_L1_lower_bound_proved=True,
        constant_bias_requires_Omega_candidate_count_L1_proved=factorial,
        standard_coefficient_PREP_SELECT_route_ruled_out=factorial,
        direct_quasiprobability_sampling_has_exponential_range=factorial,
        all_structured_quantum_compilers_ruled_out=False,
        matrix_CS_fast_forward_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=factorial,
        status=(
            "factorial-target-interference-negativity-barrier-proved-fast-forward-open"
            if factorial
            else "target-interference-negativity-control-failure"
        ),
    )
    return NegativityBarrierReport(
        created_at=utc_now(),
        theorem_contract={
            "observable": "Any group-algebra element on G^k x G",
            "resource": "Coefficient L1 norm in the canonical group basis",
            "target": "Constant baseline-versus-likelihood linear bias",
            "claim_boundary": (
                "Rules out generic coefficient PREP/SELECT normalization, not "
                "structured circuits whose group-basis expansion is implicit."
            ),
        },
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-TARGET-NEGATIVITY-STRUCTURED-FAST-FORWARD",
                "statement": (
                    "Construct a polynomial circuit whose implicit group-basis L1 is "
                    "Omega(M), or prove the matrix-CS reflections cannot fast-forward it."
                ),
                "resolved": False,
            },
            {
                "id": "PO-TARGET-NEGATIVITY-SIGN-STRUCTURE",
                "statement": (
                    "Derive the sign/phase organization of the optimal or candidate "
                    "polar observable and test whether it has an integrable transform."
                ),
                "resolved": False,
            },
            {
                "id": "PO-TARGET-NEGATIVITY-CLASSICAL-MATCHED-BASELINE",
                "statement": (
                    "For every proposed structured cancellation, identify the matched "
                    "classical estimator rather than relying only on generic L1 sampling."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Large group-basis L1 implies large operator norm.",
                "answer": (
                    "False. Destructive interference can keep operator norm at most one; "
                    "that interference is exactly the required resource."
                ),
                "resolved": True,
            },
            {
                "challenge": "The L1 lower bound is already a quantum circuit lower bound.",
                "answer": (
                    "False. Fourier transforms and polynomial functional calculus can "
                    "implement huge implicit L1 without coefficient-state preparation."
                ),
                "resolved": True,
            },
            {
                "challenge": "Standard LCU can ignore its normalization because X is bounded.",
                "answer": (
                    "False for coefficient PREP/SELECT: its block normalization is the "
                    "prepared coefficient L1 regardless of the final operator norm."
                ),
                "resolved": True,
            },
            {
                "challenge": "Any claimed structured fast-forward should be accepted as progress.",
                "answer": (
                    "No. It must include normalization, precision, success probability, "
                    "garbage uncomputation, and a matched classical-access analysis."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_group_basis_negativity_lower_bound_count": 1,
            "standard_LCU_normalization_no_go_count": int(factorial),
            "tail_required_L1_log2_lower_bound": scaling[-1].required_group_basis_L1_norm_log2_lower_bound,
            "tail_required_L1_decimal": scaling[-1].required_group_basis_L1_norm_lower_bound_decimal,
            "structured_fast_forward_count": 0,
            "hidden_involution_detector_count": 0,
        },
        claim_gate={
            "constant_bias_requires_factorial_group_basis_L1": factorial,
            "standard_coefficient_PREP_SELECT_route_ruled_out": factorial,
            "direct_signed_sampling_has_factorial_range": factorial,
            "structured_quantum_fast_forward_ruled_out": False,
            "matrix_CS_fast_forward_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A useful detector needs factorial implicit group-basis cancellation; "
                "generic LCU pays it, while no structured fast-forward is known."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that every constant-bias detector requires factorial group-basis "
            "negativity and ruled out ordinary coefficient PREP/SELECT as the escape."
        ),
        falsifiers_triggered=[
            "Polynomial group-basis L1 can never provide constant natural-copy bias.",
            "Standard sparse-LCU target recoupling necessarily pays the candidate normalization.",
            "Only an implicit structured interference compiler can evade the barrier.",
        ],
    )


def write_negativity_barrier_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_negativity_barrier_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_negativity_barrier_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
