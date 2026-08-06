"""Black-box query lower bound for factorial-scale spectral trimming.

The information-theoretic trimmed sub-POVM uses a low-pass cutoff
``tau=Theta(1/M)`` for ``M=n!`` hidden labels.  This module shows that no
generic black-box implementation can realize such a filter in polynomially
many projector-oracle queries.

For a search string ``x in {0,1}^M``, define equal-rank projectors on one
qubit by ``P_j(x)=|x_j><x_j|``.  Their average is

    B_x = diag(1-|x|/M, |x|/M).

Moreover ``2P_j-I=(-1)^{x_j} Z``.  A controlled projector reflection is
therefore exactly the usual phase-search oracle, followed by a fixed Pauli.
Any coherent low-pass routine that keeps the ``|1>`` eigenvector when
``|x|=0`` and rejects it when ``|x|=t`` distinguishes zero marked items from
``t=Theta(1)`` marked items.  The BBBV unstructured-search lower bound then
requires ``Omega(sqrt(M/t))`` oracle queries.

At ``M=n!`` this is superpolynomial.  The result applies to generic access to
the indexed projector family (and hence to generic PREPARE/SELECT use of that
family).  It does not rule out a representation transform or another oracle
that exposes additional algebraic structure unavailable in the search
instance.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_spectral_filter_query_lower_bound.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-QUERY-LOWER-BOUND"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SearchProjectorEncodingControl:
    label_count: int
    marked_count: int
    projector_rank: int
    average_frame_eigenvalues: tuple[float, float]
    marked_fraction_eigenvalue: float
    low_pass_cutoff: float
    rejection_threshold: float
    maximum_projector_idempotence_residual: float
    maximum_reflection_phase_oracle_residual: float
    fixed_input_separates_promises: bool
    equal_rank_search_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class QueryLowerBoundScalingRecord:
    n: int
    hidden_label_count_decimal: str
    log2_hidden_label_count: float
    marked_count_promise: int
    low_pass_cutoff_coefficient: int
    rejection_coefficient: int
    quantum_query_lower_bound_order: str
    quantum_query_lower_bound_log2_without_constant: float
    polynomial_query_benchmark_degree: int
    polynomial_query_benchmark_log2: float
    black_box_lower_bound_superpolynomial: bool
    status: str


@dataclass(frozen=True)
class SpectralFilterQueryLowerBoundReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[SearchProjectorEncodingControl]
    scaling_records: list[QueryLowerBoundScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def search_projectors(bits: tuple[int, ...]) -> tuple[np.ndarray, ...]:
    if not bits:
        raise ValueError("at least one search bit is required")
    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("search bits must be zero or one")
    basis = (
        np.asarray([[1.0], [0.0]]),
        np.asarray([[0.0], [1.0]]),
    )
    return tuple(basis[bit] @ basis[bit].T for bit in bits)


def audit_search_projector_encoding(
    label_count: int,
    marked_count: int,
    *,
    cutoff_coefficient: int = 4,
    rejection_coefficient: int = 8,
    tolerance: float = 1e-12,
) -> SearchProjectorEncodingControl:
    if label_count < 2:
        raise ValueError("label_count must be at least two")
    if not 0 < marked_count < label_count:
        raise ValueError("marked_count must lie strictly between zero and M")
    if not 0 <= cutoff_coefficient < rejection_coefficient:
        raise ValueError("cutoff must be below the rejection coefficient")
    if marked_count < rejection_coefficient:
        raise ValueError("marked promise must reach the rejection threshold")

    bits = (1,) * marked_count + (0,) * (label_count - marked_count)
    projectors = search_projectors(bits)
    frame = sum(projectors) / label_count
    expected = np.diag(
        [1 - marked_count / label_count, marked_count / label_count]
    )
    frame_residual = float(np.linalg.norm(frame - expected, ord=2))
    identity = np.eye(2)
    pauli_z = np.diag([1.0, -1.0])
    projector_residual = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors
    )
    reflection_residual = max(
        float(
            np.linalg.norm(
                (2 * projector - identity) - ((-1) ** bit) * pauli_z,
                ord=2,
            )
        )
        for bit, projector in zip(bits, projectors)
    )
    cutoff = cutoff_coefficient / label_count
    rejection = rejection_coefficient / label_count
    marked_eigenvalue = float(frame[1, 1])
    separates = 0 <= cutoff and marked_eigenvalue >= rejection - tolerance
    verified = (
        frame_residual <= tolerance
        and projector_residual <= tolerance
        and reflection_residual <= tolerance
        and separates
        and all(abs(float(np.trace(projector)) - 1) <= tolerance for projector in projectors)
    )
    return SearchProjectorEncodingControl(
        label_count=label_count,
        marked_count=marked_count,
        projector_rank=1,
        average_frame_eigenvalues=(
            float(frame[0, 0]),
            marked_eigenvalue,
        ),
        marked_fraction_eigenvalue=marked_eigenvalue,
        low_pass_cutoff=cutoff,
        rejection_threshold=rejection,
        maximum_projector_idempotence_residual=projector_residual,
        maximum_reflection_phase_oracle_residual=reflection_residual,
        fixed_input_separates_promises=separates,
        equal_rank_search_reduction_verified=verified,
        status=(
            "exact-equal-rank-search-projector-reduction"
            if verified
            else "search-projector-reduction-validation-failure"
        ),
    )


def query_lower_bound_scaling_record(
    n: int,
    *,
    marked_count: int = 8,
    cutoff_coefficient: int = 4,
    polynomial_degree: int = 100,
) -> QueryLowerBoundScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    if marked_count <= cutoff_coefficient:
        raise ValueError("marked promise must exceed the low-pass cutoff")
    if polynomial_degree < 0:
        raise ValueError("polynomial degree must be nonnegative")
    hidden_count = math.factorial(n)
    log_hidden = math.log2(hidden_count)
    lower_log = 0.5 * (log_hidden - math.log2(marked_count))
    benchmark = polynomial_degree * math.log2(n)
    return QueryLowerBoundScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        log2_hidden_label_count=log_hidden,
        marked_count_promise=marked_count,
        low_pass_cutoff_coefficient=cutoff_coefficient,
        rejection_coefficient=marked_count,
        quantum_query_lower_bound_order="Omega(sqrt(n!/t))",
        quantum_query_lower_bound_log2_without_constant=lower_log,
        polynomial_query_benchmark_degree=polynomial_degree,
        polynomial_query_benchmark_log2=benchmark,
        black_box_lower_bound_superpolynomial=lower_log > benchmark,
        status="factorial-scale-black-box-query-lower-bound",
    )


def run_spectral_filter_query_lower_bound() -> SpectralFilterQueryLowerBoundReport:
    controls = [
        audit_search_projector_encoding(label_count, 8)
        for label_count in (16, 32, 64, 128)
    ]
    scaling = [
        query_lower_bound_scaling_record(n)
        for n in (16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512)
    ]
    failures = sum(
        not row.equal_rank_search_reduction_verified for row in controls
    )
    proof_obligations: list[dict[str, bool | str]] = [
        {
            "obligation": "equal_rank_projector_family",
            "resolved": failures == 0,
            "resolution": "Every P_j is an exact rank-one orthogonal projector.",
        },
        {
            "obligation": "projector_query_equals_search_query",
            "resolved": failures == 0,
            "resolution": (
                "The reflection 2P_j-I equals (-1)^x_j Z, so controlled "
                "reflection access and phase-search access differ only by a "
                "known fixed Pauli."
            ),
        },
        {
            "obligation": "low_pass_solves_search_promise",
            "resolved": failures == 0,
            "resolution": (
                "On input |1>, B_x has eigenvalue zero at weight zero and "
                "t/M at promised weight t, crossing a constant-over-M gap."
            ),
        },
        {
            "obligation": "quantum_search_lower_bound",
            "resolved": True,
            "resolution": (
                "The BBBV hybrid lower bound gives Omega(sqrt(M/t)) queries "
                "for bounded-error distinction of weight zero from fixed "
                "positive weight t. This external theorem is linked below."
            ),
        },
    ]
    verified = all(bool(row["resolved"]) for row in proof_obligations)
    return SpectralFilterQueryLowerBoundReport(
        created_at=utc_now(),
        theorem_contract={
            "oracle": (
                "One query applies the indexed controlled reflection "
                "sum_j |j><j| tensor (2P_j-I)."
            ),
            "projector_encoding": "P_j(x)=|x_j><x_j| on a qubit.",
            "average_frame": (
                "B_x=diag(1-|x|/M,|x|/M), with all projectors rank one."
            ),
            "filter_promise": (
                "The implementation retains eigenvectors at lambda<=a/M "
                "and rejects them at lambda>=b/M with fixed b>a."
            ),
            "reduction": (
                "Apply the filter to |1>; zero marks are retained and b "
                "marks are rejected, solving promised unstructured search."
            ),
            "lower_bound": "Omega(sqrt(M/b)) projector-oracle queries.",
            "wreath_substitution": (
                "For M=n! and fixed a,b, the generic query cost is "
                "Omega(sqrt(n!)), which is superpolynomial in n."
            ),
            "scope": (
                "The lower bound is black-box. It does not apply to an oracle "
                "or transform exposing special symmetric-group structure not "
                "present in arbitrary indexed projectors."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=proof_obligations,
        adversarial_audit=[
            {
                "objection": "The reduction cheats by changing projector rank.",
                "resolved": True,
                "resolution": "Every search projector has rank exactly one.",
            },
            {
                "objection": "Projector reflection access is stronger than search access.",
                "resolved": True,
                "resolution": (
                    "For this family they are unitarily identical up to a "
                    "known fixed Z gate, so a filter query transfers one-for-one."
                ),
            },
            {
                "objection": "The theorem rules out all wreath-HSP filters.",
                "resolved": False,
                "resolution": (
                    "No. Wreath projectors have representation-theoretic "
                    "structure absent from the adversarial search family."
                ),
            },
            {
                "objection": "A coarse constant-over-M transition is enough to evade search.",
                "resolved": True,
                "resolution": (
                    "The promise uses two fixed coefficients a<b; constant "
                    "width in units of 1/M still distinguishes zero from b marks."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "bennett-bernstein-brassard-vazirani-1997",
                "title": "Strengths and Weaknesses of Quantum Computing",
                "url": "https://arxiv.org/abs/quant-ph/9701001",
                "use": "Quantum black-box lower bound for unstructured search.",
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics={
            "equal_rank_search_reduction_theorem_count": 1,
            "black_box_spectral_filter_query_lower_bound_theorem_count": 1,
            "finite_search_encoding_control_count": len(controls),
            "finite_search_encoding_failure_count": failures,
            "scaling_record_count": len(scaling),
            "superpolynomial_black_box_lower_bound_row_count": sum(
                row.black_box_lower_bound_superpolynomial for row in scaling
            ),
            "tail_n": scaling[-1].n,
            "tail_quantum_query_lower_bound_log2": (
                scaling[-1].quantum_query_lower_bound_log2_without_constant
            ),
            "representation_structured_filter_count": 0,
            "polynomial_hidden_permutation_decoder_count": 0,
            "general_wreath_circuit_lower_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "equal_rank_search_projector_reduction_proved": verified,
            "generic_indexed_projector_filter_requires_superpolynomial_queries": verified,
            "generic_prepare_select_spectral_trim_is_polynomial": False,
            "representation_structured_filter_ruled_out": False,
            "general_wreath_circuit_lower_bound_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The abstract constant-success measurement cannot be turned "
                "into a polynomial algorithm by treating the projectors as a "
                "generic indexed oracle. A successful implementation must "
                "use additional symmetric-group structure."
            ),
        },
        status=(
            "generic-spectral-trim-query-route-falsified-structured-open"
            if verified
            else "spectral-filter-query-reduction-validation-failure"
        ),
        summary=(
            "Reduced factorial-scale low-pass filtering of equal-rank "
            "projector averages to unstructured search, proving an "
            "Omega(sqrt(n!)) black-box query lower bound."
        ),
        falsifiers_triggered=[
            (
                "A generic PREPARE/SELECT implementation cannot exploit the "
                "existence of the trimmed sub-POVM at polynomial cost."
            ),
            (
                "Equal projector rank does not evade the search reduction."
            ),
            (
                "Future filter proposals must identify the exact additional "
                "representation structure used to beat black-box search."
            ),
        ],
    )


def write_spectral_filter_query_lower_bound_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_spectral_filter_query_lower_bound())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_spectral_filter_query_lower_bound_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
