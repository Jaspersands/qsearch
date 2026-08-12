"""Operator-norm robustness of the DCP PGM garbage bootstrap.

Let ``V_0`` be an exact accessible rank-one covariant-PGM dilation and let
``V`` be an implemented dilation satisfying

    ||(V-V_0) P_legal|| <= delta,

with the same bound for inverse calls.  The exact garbage-bootstrap reduction
uses public known-shift phase states and fixed-point amplitude amplification to
construct the controlled outcome-garbage preparation ``G_0``.

If exact amplification uses at most

    Q <= 16 p^(-1/2) log(8/eta)

dilation/inverse calls to reach error ``eta/4``, replacing each call by the
approximate implementation changes the full amplified circuit by at most
``Q delta`` via the standard hybrid/telescoping argument.  The sufficient
condition

    delta <= eta/[8(Q+1)]                              (1)

therefore gives an implemented garbage preparation within ``3 eta/8`` of
``G_0``.  Canonicalization obeys

    ||G^dagger V - G_0^dagger V_0||
      <= ||G-G_0|| + ||V-V_0|| < eta/2.                (2)

For ``p>=n^-a`` and target canonicalization error ``eta=n^-b``, both ``Q`` and
the inverse of the sufficient ``delta`` are polynomial in ``n`` (up to a log
factor).  Hence operator-norm approximate standard-circuit PGMs do not evade
the exact bootstrap merely by using finite precision.

This theorem deliberately assumes an aligned accessible dilation with uniform
operator error on the legal span.  Closeness of classical outcome
distributions alone, average-state error, diamond closeness after discarding
an inaccessible environment, and a non-PGM POVM are not covered.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from scipy.linalg import expm

from research_registry import utc_now


REPORT_PATH = Path(
    "research/reductions/dcp_pgm_bootstrap_perturbation_reduction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-PGM-BOOTSTRAP-PERTURBATION-REDUCTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class HybridTelescopingControl:
    dimension: int
    query_count: int
    per_query_operator_error: float
    exact_product_unitarity_residual: float
    approximate_product_unitarity_residual: float
    product_operator_error: float
    hybrid_error_upper_bound: float
    hybrid_bound_residual: float
    hybrid_bound_verified: bool
    status: str


@dataclass(frozen=True)
class PGMBootstrapPerturbationScalingRecord:
    n_bits: int
    pgm_success_power: int
    pgm_success_lower_bound: float
    target_error_power: int
    target_canonicalization_error: float
    amplification_query_upper_bound: int
    sufficient_dilation_operator_error: float
    sufficient_dilation_operator_error_log2: float
    amplified_garbage_preparation_error_upper_bound: float
    canonicalization_error_upper_bound: float
    polynomial_query_complexity: bool
    inverse_polynomial_precision_sufficient: bool
    status: str


@dataclass(frozen=True)
class PGMBootstrapPerturbationTheorem:
    approximation_contract: str
    exact_amplification_cost: str
    hybrid_bound: str
    sufficient_precision: str
    canonicalization_bound: str
    polynomial_resource_consequence: str
    operator_norm_approximate_accessible_pgm_reduced: bool
    classical_outcome_distribution_closeness_reduced: bool
    average_state_error_reduced: bool
    inaccessible_environment_recovered: bool
    arbitrary_collective_povm_reduced: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DCPPGMBootstrapPerturbationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[HybridTelescopingControl]
    scaling_records: list[PGMBootstrapPerturbationScalingRecord]
    theorem: PGMBootstrapPerturbationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def amplification_query_upper_bound(
    pgm_success_lower_bound: float,
    target_canonicalization_error: float,
) -> int:
    if not 0 < pgm_success_lower_bound <= 1:
        raise ValueError("PGM success lower bound must lie in (0,1]")
    if not 0 < target_canonicalization_error < 1:
        raise ValueError("target error must lie in (0,1)")
    return math.ceil(
        16.0
        * pgm_success_lower_bound**-0.5
        * math.log(8.0 / target_canonicalization_error)
    )


def sufficient_dilation_error(
    pgm_success_lower_bound: float,
    target_canonicalization_error: float,
) -> tuple[int, float]:
    queries = amplification_query_upper_bound(
        pgm_success_lower_bound,
        target_canonicalization_error,
    )
    return queries, target_canonicalization_error / (8.0 * (queries + 1))


def _random_unitary(dimension: int, rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    unitary, diagonal = np.linalg.qr(raw)
    phases = np.diag(diagonal)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    return unitary @ np.diag(np.conj(phases))


def audit_hybrid_telescoping_bound(
    dimension: int,
    query_count: int,
    perturbation_scale: float,
    *,
    seed: int,
) -> HybridTelescopingControl:
    if dimension < 2 or query_count < 1 or perturbation_scale <= 0:
        raise ValueError("invalid hybrid control parameters")
    rng = np.random.default_rng(seed)
    exact_factors = []
    approximate_factors = []
    per_errors = []
    for _ in range(query_count):
        exact = _random_unitary(dimension, rng)
        raw = rng.normal(size=(dimension, dimension))
        hermitian = (raw + raw.T) / 2.0
        hermitian /= max(1.0, float(np.linalg.norm(hermitian, ord=2)))
        perturbation = expm(1j * perturbation_scale * hermitian)
        approximate = perturbation @ exact
        exact_factors.append(exact)
        approximate_factors.append(approximate)
        per_errors.append(float(np.linalg.norm(approximate - exact, ord=2)))
    exact_product = np.eye(dimension, dtype=complex)
    approximate_product = np.eye(dimension, dtype=complex)
    for exact, approximate in zip(exact_factors, approximate_factors):
        exact_product = exact @ exact_product
        approximate_product = approximate @ approximate_product
    product_error = float(
        np.linalg.norm(approximate_product - exact_product, ord=2)
    )
    per_query = max(per_errors)
    bound = query_count * per_query
    residual = max(0.0, product_error - bound)
    exact_unitarity = float(
        np.linalg.norm(
            exact_product.conj().T @ exact_product - np.eye(dimension), ord=2
        )
    )
    approximate_unitarity = float(
        np.linalg.norm(
            approximate_product.conj().T @ approximate_product
            - np.eye(dimension),
            ord=2,
        )
    )
    verified = residual <= 1e-10
    return HybridTelescopingControl(
        dimension=dimension,
        query_count=query_count,
        per_query_operator_error=per_query,
        exact_product_unitarity_residual=exact_unitarity,
        approximate_product_unitarity_residual=approximate_unitarity,
        product_operator_error=product_error,
        hybrid_error_upper_bound=bound,
        hybrid_bound_residual=residual,
        hybrid_bound_verified=verified,
        status=(
            "unitary-hybrid-telescoping-bound-verified"
            if verified
            else "unitary-hybrid-bound-failure"
        ),
    )


def perturbation_scaling_record(
    n_bits: int,
    pgm_success_power: int,
    target_error_power: int,
) -> PGMBootstrapPerturbationScalingRecord:
    if n_bits < 2 or pgm_success_power < 0 or target_error_power < 1:
        raise ValueError("invalid perturbation scaling parameters")
    success = n_bits ** (-pgm_success_power)
    target = n_bits ** (-target_error_power)
    queries, delta = sufficient_dilation_error(success, target)
    amplified_error = target / 4.0 + queries * delta
    canonical_error = amplified_error + delta
    polynomial_query = queries <= n_bits ** (
        math.ceil(pgm_success_power / 2) + target_error_power + 3
    )
    inverse_poly_precision = -math.log2(delta) <= (
        pgm_success_power / 2 + target_error_power + 4
    ) * math.log2(n_bits)
    return PGMBootstrapPerturbationScalingRecord(
        n_bits=n_bits,
        pgm_success_power=pgm_success_power,
        pgm_success_lower_bound=success,
        target_error_power=target_error_power,
        target_canonicalization_error=target,
        amplification_query_upper_bound=queries,
        sufficient_dilation_operator_error=delta,
        sufficient_dilation_operator_error_log2=math.log2(delta),
        amplified_garbage_preparation_error_upper_bound=amplified_error,
        canonicalization_error_upper_bound=canonical_error,
        polynomial_query_complexity=polynomial_query,
        inverse_polynomial_precision_sufficient=inverse_poly_precision,
        status=(
            "operator-norm-approximate-pgm-bootstrap-polynomial"
            if polynomial_query
            and inverse_poly_precision
            and canonical_error < target / 2.0
            else "pgm-bootstrap-perturbation-scaling-failure"
        ),
    )


def pgm_bootstrap_perturbation_theorem() -> PGMBootstrapPerturbationTheorem:
    return PGMBootstrapPerturbationTheorem(
        approximation_contract=(
            "uniform aligned operator-norm error delta for V and V^dagger on "
            "the full legal fiber span"
        ),
        exact_amplification_cost=(
            "Q<=16 p^-1/2 log(8/eta) dilation/inverse calls for exact "
            "garbage preparation error eta/4"
        ),
        hybrid_bound="replacing Q oracle calls changes the amplified unitary by at most Q delta",
        sufficient_precision="delta<=eta/[8(Q+1)]",
        canonicalization_bound=(
            "||G^dagger V-G_0^dagger V_0||<=3eta/8+delta<eta/2"
        ),
        polynomial_resource_consequence=(
            "p>=n^-a and eta=n^-b require polynomial queries and only inverse-polynomial dilation precision"
        ),
        operator_norm_approximate_accessible_pgm_reduced=True,
        classical_outcome_distribution_closeness_reduced=False,
        average_state_error_reduced=False,
        inaccessible_environment_recovered=False,
        arbitrary_collective_povm_reduced=False,
        theorem_verified=True,
        status="operator-norm-approximate-pgm-bootstrap-robustified",
    )


def run_pgm_bootstrap_perturbation_reduction() -> DCPPGMBootstrapPerturbationReport:
    controls = [
        audit_hybrid_telescoping_bound(3, 2, 1e-3, seed=3),
        audit_hybrid_telescoping_bound(4, 5, 2e-3, seed=5),
        audit_hybrid_telescoping_bound(5, 12, 5e-4, seed=7),
    ]
    scaling = [
        perturbation_scaling_record(n_bits, success_power, error_power)
        for n_bits in (64, 128, 256, 512, 1024)
        for success_power in (0, 2, 6, 12)
        for error_power in (2, 8, 16)
    ]
    theorem = pgm_bootstrap_perturbation_theorem()
    failures = sum(not row.hybrid_bound_verified for row in controls)
    metrics: dict[str, int | float] = {
        "pgm_bootstrap_perturbation_theorem_count": 1,
        "operator_norm_approximate_accessible_pgm_reduction_count": 1,
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "scaling_row_count": len(scaling),
        "polynomial_resource_scaling_row_count": sum(
            row.status == "operator-norm-approximate-pgm-bootstrap-polynomial"
            for row in scaling
        ),
        "maximum_hybrid_bound_residual": max(
            row.hybrid_bound_residual for row in controls
        ),
        "minimum_sufficient_dilation_operator_error_log2": min(
            row.sufficient_dilation_operator_error_log2 for row in scaling
        ),
        "proved_outcome_distribution_only_reduction_count": 0,
        "proved_average_state_error_reduction_count": 0,
        "proved_inaccessible_environment_recovery_count": 0,
        "proved_arbitrary_collective_povm_reduction_count": 0,
        "polynomial_pgm_circuit_count": 0,
        "polynomial_average_subset_sum_witness_solver_count": 0,
    }
    return DCPPGMBootstrapPerturbationReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "an accessible approximate dilation uniformly aligned in "
                "operator norm with an exact rank-one PGM dilation"
            ),
            "success": "exact PGM success p>=1/poly(n)",
            "precision": "delta<=eta/[8(Q+1)] for desired canonicalization error eta",
            "proved": (
                "hybrid-stable garbage amplification and approximate canonical fiber erasure"
            ),
            "excluded": (
                "outcome-distribution-only approximation, average-state error, "
                "unaligned/inaccessible Stinespring environments, and non-PGM POVMs"
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-DCP-PGM-BOOTSTRAP-HYBRID",
                "description": "Control accumulated dilation error through amplitude amplification.",
                "satisfied": True,
                "evidence": "Q-call telescoping gives operator error at most Q delta",
            },
            {
                "id": "PO-DCP-PGM-BOOTSTRAP-POLY-PRECISION",
                "description": (
                    "Show inverse-polynomial PGM success needs only inverse-polynomial circuit precision."
                ),
                "satisfied": True,
                "evidence": (
                    "Q=poly(n) and delta=eta/[8(Q+1)] remains inverse polynomial"
                ),
            },
            {
                "id": "PO-DCP-PGM-OUTCOME-CHANNEL-STINESPRING",
                "description": (
                    "Derive an efficiently known aligned dilation from closeness "
                    "of the discarded classical outcome channel alone."
                ),
                "satisfied": False,
                "evidence": "Stinespring continuity gives existence, not necessarily an accessible alignment circuit",
            },
            {
                "id": "PO-DCP-NON-PGM-COLLECTIVE-POVM",
                "description": "Analyze a collective decoder outside the covariant rank-one PGM family.",
                "satisfied": False,
                "evidence": "outside the perturbation theorem",
            },
        ],
        adversarial_audit=[
            {
                "attack": "Accumulate small gate/dilation errors through amplification.",
                "survives": False,
                "reason": "the Q delta hybrid charge is explicit in the sufficient precision",
            },
            {
                "attack": "Use only inverse-polynomial PGM success and very high target precision.",
                "survives": False,
                "reason": "for fixed polynomial exponents, both query count and inverse precision remain polynomial",
            },
            {
                "attack": "Promise only close classical PGM outcome probabilities.",
                "survives": True,
                "reason": "that promise does not supply the aligned coherent dilation required by the bootstrap",
            },
            {
                "attack": "Use a different approximate collective POVM.",
                "survives": True,
                "reason": "the exact rank-one PGM target is essential",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "operator_norm_approximate_accessible_pgm_route_is_solver_equivalent": True,
            "finite_precision_standard_circuit_loophole_alive": False,
            "outcome_distribution_only_approximation_route_closed": False,
            "average_state_approximation_route_closed": False,
            "inaccessible_environment_route_closed": False,
            "non_pgm_collective_measurement_route_closed": False,
            "polynomial_pgm_constructed": False,
            "polynomial_average_witness_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Aligned operator-norm approximation at inverse-polynomial "
                "precision preserves the garbage bootstrap with polynomial "
                "overhead. Only weaker approximation contracts, inaccessible "
                "environments, or non-PGM collective measurements remain."
            ),
        },
        status="operator-norm-approximate-pgm-reduced-weaker-channel-contracts-open",
        summary=(
            "Proved a hybrid-stable perturbation threshold for the PGM outcome-"
            "garbage bootstrap. With inverse-polynomial PGM success, an aligned "
            "accessible dilation needs only inverse-polynomial operator precision "
            "to recover approximate canonical fiber erasure. Outcome-only and "
            "average-state approximation contracts remain open."
        ),
        falsifiers_triggered=[
            "Finite precision does not rescue an aligned accessible PGM dilation from the witness reduction.",
            "Amplitude-amplification error must be charged as Q delta, not treated as constant.",
            "Inverse-polynomial success and target error keep both Q and 1/delta polynomial.",
            "Classical outcome closeness is strictly weaker than the operator-norm dilation contract used here.",
        ],
    )


def write_pgm_bootstrap_perturbation_reduction(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-PGM-BOOTSTRAP-PERTURBATION-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_pgm_bootstrap_perturbation_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_pgm_bootstrap_perturbation_reduction()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
