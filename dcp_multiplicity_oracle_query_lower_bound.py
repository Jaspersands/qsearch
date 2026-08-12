"""Black-box query lower bound for DCP fiber-multiplicity discrimination.

Generic collision-walk and multiplicity-filter proposals often assume only a
reversible equality oracle for the public subset-sum map ``f`` and a target
``s``.  Even with one known preimage, distinguishing a singleton fiber from a
doubleton fiber is unstructured search.

Take a search string ``x in {0,1}^M`` with promise ``|x| in {0,t}``.  Define a
function on ``M+1`` inputs whose equality flag for the target is always one at
input zero and equals ``x_j`` at input ``j>=1``.  The target fiber therefore
has size one when ``|x|=0`` and size ``1+t`` when ``|x|=t``.  One equality-
oracle query is exactly one search-oracle query, apart from the known input-zero
branch.  Any bounded-error multiplicity discriminator, constant-gap
target-addressable filter, or generic collision routine solves promised search.

The BBBV hybrid lower bound gives

    Q = Omega(sqrt(M/t)).

For a Boolean subset-sum domain of size ``D=2^m`` and fixed ``t``, this is
``2^(Omega(m))`` queries (``Omega(2^(m/2))`` for singleton versus doubleton).

This is a black-box theorem.  Real DCP labels give an arithmetic description of
``f(x)=<a,x> mod 2^n`` that is absent from the adversarial search oracle.  The
result closes generic equality-oracle collision walks and source-independent
multiplicity filters, not source-aware algebraic preconditioners or other
collective measurements.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/reductions/dcp_multiplicity_oracle_query_lower_bound.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-MULTIPLICITY-ORACLE-QUERY-LOWER-BOUND"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class MultiplicitySearchEncodingControl:
    search_domain_size: int
    extra_marked_count: int
    fiber_domain_size: int
    zero_case_fiber_multiplicity: int
    marked_case_fiber_multiplicity: int
    maximum_oracle_action_residual: float
    known_preimage_preserved: bool
    one_query_search_to_equality_reduction: bool
    multiplicity_promise_separates_search_cases: bool
    reduction_verified: bool
    status: str


@dataclass(frozen=True)
class MultiplicityQueryScalingRecord:
    assignment_bits: int
    assignment_domain_log2: int
    extra_marked_count_promise: int
    query_lower_bound_order: str
    query_lower_bound_log2_without_constant: float
    polynomial_query_benchmark_power: int
    polynomial_query_benchmark_log2: float
    black_box_query_lower_bound_superpolynomial: bool
    status: str


@dataclass(frozen=True)
class MultiplicityOracleQueryTheorem:
    oracle_model: str
    search_embedding: str
    multiplicity_promise: str
    query_transfer: str
    bbbv_consequence: str
    dcp_consequence: str
    scope_limit: str
    singleton_doubleton_black_box_lower_bound_proved: bool
    generic_equality_oracle_collision_walk_polynomial: bool
    arithmetic_subset_sum_structure_ruled_out: bool
    general_collective_measurement_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DCPMultiplicityOracleQueryLowerBoundReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[MultiplicitySearchEncodingControl]
    scaling_records: list[MultiplicityQueryScalingRecord]
    theorem: MultiplicityOracleQueryTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def equality_flags(search_bits: Sequence[int]) -> tuple[int, ...]:
    if not search_bits or any(bit not in (0, 1) for bit in search_bits):
        raise ValueError("search_bits must be a nonempty binary sequence")
    return (1, *(int(bit) for bit in search_bits))


def bit_flip_oracle(flags: Sequence[int]) -> np.ndarray:
    if not flags or any(bit not in (0, 1) for bit in flags):
        raise ValueError("flags must be a nonempty binary sequence")
    domain_size = len(flags)
    oracle = np.zeros((2 * domain_size, 2 * domain_size), dtype=float)
    for index, flag in enumerate(flags):
        for target_bit in (0, 1):
            source = 2 * index + target_bit
            destination = 2 * index + (target_bit ^ int(flag))
            oracle[destination, source] = 1.0
    return oracle


def audit_multiplicity_search_encoding(
    search_domain_size: int,
    extra_marked_count: int,
    *,
    tolerance: float = 1e-12,
) -> MultiplicitySearchEncodingControl:
    if search_domain_size < 2:
        raise ValueError("search domain must have at least two positions")
    if not 0 < extra_marked_count <= search_domain_size:
        raise ValueError("invalid marked-count promise")
    zero_bits = (0,) * search_domain_size
    marked_bits = (1,) * extra_marked_count + (0,) * (
        search_domain_size - extra_marked_count
    )
    zero_flags = equality_flags(zero_bits)
    marked_flags = equality_flags(marked_bits)
    zero_oracle = bit_flip_oracle(zero_flags)
    marked_oracle = bit_flip_oracle(marked_flags)
    identity_residual = max(
        float(
            np.linalg.norm(
                oracle.T @ oracle - np.eye(oracle.shape[0]),
                ord=2,
            )
        )
        for oracle in (zero_oracle, marked_oracle)
    )
    known_preserved = zero_flags[0] == marked_flags[0] == 1
    one_query = all(
        zero_flags[index + 1] == 0
        and marked_flags[index + 1] == marked_bits[index]
        for index in range(search_domain_size)
    )
    separates = (
        sum(zero_flags) == 1
        and sum(marked_flags) == 1 + extra_marked_count
    )
    verified = (
        identity_residual <= tolerance
        and known_preserved
        and one_query
        and separates
    )
    return MultiplicitySearchEncodingControl(
        search_domain_size=search_domain_size,
        extra_marked_count=extra_marked_count,
        fiber_domain_size=search_domain_size + 1,
        zero_case_fiber_multiplicity=sum(zero_flags),
        marked_case_fiber_multiplicity=sum(marked_flags),
        maximum_oracle_action_residual=identity_residual,
        known_preimage_preserved=known_preserved,
        one_query_search_to_equality_reduction=one_query,
        multiplicity_promise_separates_search_cases=separates,
        reduction_verified=verified,
        status=(
            "known-preimage-search-embedded-in-fiber-multiplicity"
            if verified
            else "multiplicity-search-encoding-failure"
        ),
    )


def multiplicity_query_scaling_record(
    assignment_bits: int,
    *,
    extra_marked_count: int = 1,
    polynomial_query_benchmark_power: int = 8,
) -> MultiplicityQueryScalingRecord:
    if assignment_bits < 2:
        raise ValueError("assignment_bits must be at least two")
    if extra_marked_count < 1:
        raise ValueError("extra_marked_count must be positive")
    if polynomial_query_benchmark_power < 0:
        raise ValueError("benchmark power must be nonnegative")
    # Use M=2^m-1 search positions and one known target preimage.
    log_search_size = assignment_bits + math.log2(
        1.0 - math.exp2(-assignment_bits)
    )
    lower_log = 0.5 * (
        log_search_size - math.log2(extra_marked_count)
    )
    benchmark = polynomial_query_benchmark_power * math.log2(assignment_bits)
    return MultiplicityQueryScalingRecord(
        assignment_bits=assignment_bits,
        assignment_domain_log2=assignment_bits,
        extra_marked_count_promise=extra_marked_count,
        query_lower_bound_order="Omega(sqrt((2^m-1)/t))",
        query_lower_bound_log2_without_constant=lower_log,
        polynomial_query_benchmark_power=polynomial_query_benchmark_power,
        polynomial_query_benchmark_log2=benchmark,
        black_box_query_lower_bound_superpolynomial=lower_log > benchmark,
        status="exponential-black-box-fiber-multiplicity-query-lower-bound",
    )


def multiplicity_oracle_query_theorem() -> MultiplicityOracleQueryTheorem:
    return MultiplicityOracleQueryTheorem(
        oracle_model=(
            "reversible target-equality access O_f:|x,b> maps to "
            "|x,b xor [f(x)=s]>"
        ),
        search_embedding=(
            "input zero is a known preimage and the other equality flags are "
            "the promised unstructured search bits"
        ),
        multiplicity_promise="c_s=1 versus c_s=1+t",
        query_transfer=(
            "one target-equality query and one search query are identical on "
            "the unknown positions; the known position is fixed"
        ),
        bbbv_consequence=(
            "bounded-error distinction requires Omega(sqrt(M/t)) queries"
        ),
        dcp_consequence=(
            "at M=2^m-1 and fixed t, a generic equality-oracle multiplicity "
            "filter or collision walk needs 2^Omega(m) queries"
        ),
        scope_limit=(
            "The adversarial oracle has no modular-subset-sum arithmetic. The "
            "bound does not apply once a circuit proves and exploits additional "
            "structure of the public labels."
        ),
        singleton_doubleton_black_box_lower_bound_proved=True,
        generic_equality_oracle_collision_walk_polynomial=False,
        arithmetic_subset_sum_structure_ruled_out=False,
        general_collective_measurement_lower_bound_proved=False,
        theorem_verified=True,
        status="generic-fiber-multiplicity-query-route-reduced-to-search",
    )


def run_multiplicity_oracle_query_lower_bound(
) -> DCPMultiplicityOracleQueryLowerBoundReport:
    controls = [
        audit_multiplicity_search_encoding(domain, marked)
        for domain in (8, 16, 32, 64)
        for marked in (1, 2, 4)
        if marked <= domain
    ]
    scaling = [
        multiplicity_query_scaling_record(bits, extra_marked_count=marked)
        for bits in (32, 64, 128, 256, 512, 1024)
        for marked in (1, 4)
    ]
    theorem = multiplicity_oracle_query_theorem()
    failures = sum(not row.reduction_verified for row in controls)
    verified = failures == 0 and theorem.theorem_verified
    metrics: dict[str, int | float] = {
        "known_preimage_search_reduction_theorem_count": int(verified),
        "singleton_doubleton_query_lower_bound_theorem_count": int(verified),
        "finite_search_encoding_control_count": len(controls),
        "finite_search_encoding_failure_count": failures,
        "scaling_record_count": len(scaling),
        "superpolynomial_query_lower_bound_row_count": sum(
            row.black_box_query_lower_bound_superpolynomial for row in scaling
        ),
        "tail_assignment_bits": scaling[-1].assignment_bits,
        "tail_singleton_doubleton_query_lower_bound_log2": (
            multiplicity_query_scaling_record(1024).query_lower_bound_log2_without_constant
        ),
        "arithmetic_source_aware_multiplicity_filter_count": 0,
        "polynomial_generic_collision_walk_count": 0,
        "general_dcp_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DCPMultiplicityOracleQueryLowerBoundReport(
        created_at=utc_now(),
        theorem_contract={
            "oracle": theorem.oracle_model,
            "promise": theorem.multiplicity_promise,
            "reduction": theorem.search_embedding,
            "query_lower_bound": theorem.bbbv_consequence,
            "dcp_substitution": theorem.dcp_consequence,
            "scope": theorem.scope_limit,
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "retain_one_known_preimage_in_both_promises",
                "resolved": verified,
                "resolution": (
                    "Domain point zero is always a target preimage, so the "
                    "promise is singleton versus singleton plus hidden marks."
                ),
            },
            {
                "obligation": "simulate_target_equality_query_with_one_search_query",
                "resolved": verified,
                "resolution": (
                    "Every unknown equality flag is exactly one search bit; "
                    "the point-zero flag is a known fixed NOT."
                ),
            },
            {
                "obligation": "invoke_bounded_error_quantum_search_lower_bound",
                "resolved": True,
                "resolution": (
                    "The BBBV hybrid bound is Omega(sqrt(M/t)) for zero versus "
                    "t marked positions."
                ),
            },
            {
                "obligation": "transfer_black_box_bound_to_explicit_modular_subset_sum",
                "resolved": False,
                "resolution": (
                    "Explicit labels expose arithmetic structure absent from the "
                    "search oracle; exploiting that structure is the remaining route."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Knowing one witness might make collision detection easy.",
                "survives": True,
                "response": (
                    "After removing the known position, deciding whether another "
                    "preimage exists is exactly OR on M unknown bits."
                ),
            },
            {
                "challenge": "A coherent filter is weaker than outputting the hidden preimage.",
                "survives": True,
                "response": (
                    "Only bounded-error distinction is needed; a constant-gap "
                    "filter followed by a flag measurement already solves OR."
                ),
            },
            {
                "challenge": "The lower bound proves DCP multiplicity hard.",
                "survives": False,
                "response": (
                    "No. It proves only the generic oracle boundary. Modular "
                    "linearity and two-adic carries may support a non-black-box algorithm."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "BBBV-1997",
                "title": "Strengths and Weaknesses of Quantum Computing",
                "url": "https://arxiv.org/abs/quant-ph/9701001",
                "use": "quantum black-box lower bound for unstructured search",
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "generic_equality_oracle_multiplicity_filter_polynomial": False,
            "generic_collision_walk_route_open": False,
            "source_aware_arithmetic_collision_route_open": True,
            "explicit_subset_sum_query_lower_bound_proved": False,
            "general_dcp_measurement_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Singleton-versus-doubleton discrimination with only equality "
                "access contains unstructured search and needs exponential "
                "queries. A surviving proposal must name the arithmetic label "
                "structure it exploits."
            ),
        },
        status=(
            "generic-multiplicity-oracle-route-falsified-arithmetic-open"
            if verified
            else "multiplicity-query-reduction-control-failure"
        ),
        summary=(
            "Reduced generic singleton/doubleton fiber discrimination to "
            "unstructured search with one known preimage, proving an "
            "Omega(2^(m/2)) equality-oracle query lower bound."
        ),
        falsifiers_triggered=[
            "A known witness does not make generic second-preimage detection polynomial.",
            "A target-addressable constant-gap multiplicity filter already solves promised OR and inherits its query lower bound.",
            "Generic equality-oracle collision walks cannot implement the multiplicity-stratum measurement in polynomial queries.",
            "The theorem does not charge arithmetic operations on explicit modular subset-sum labels.",
        ],
    )


def write_multiplicity_oracle_query_lower_bound(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-MULTIPLICITY-ORACLE-QUERY-LOWER-BOUND"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_multiplicity_oracle_query_lower_bound())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    output = write_multiplicity_oracle_query_lower_bound()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))
