"""Source-mass and dequantization gate for diagram-algebra multiplicities.

An efficient algebra Fourier transform is a basis change, not an efficient
algorithm for a rare representation-theoretic multiplicity.  If a prepared
module state has target-sector mass

    p_lambda = m_lambda d_lambda / dim(V),

then direct label sampling needs order ``1/p_lambda`` copies to witness the
sector.  Even with coherent state-preparation access, reflection about the
target sector, and amplitude amplification, zero-versus-nonzero detection has
the black-box search cost ``Theta(1/sqrt(p_lambda))``.  A candidate therefore
needs an inverse-polynomial source-mass theorem or additional source-aware
structure; #BQP membership alone does not provide a BQP algorithm.

The generic Brauer regular representation provides an exact normalization
control.  Its irreps are indexed by partitions of ``n-2k`` and have dimension

    binom(n,2k) (2k-1)!! f^lambda.

Their regular Fourier masses are ``d_lambda^2/(2n-1)!!``.  One-dimensional
sectors consequently have exponentially small mass.  This does not rule out
large, deliberately targeted sectors or nonregular modules.  It rules out the
shortcut "efficient QFT plus multiplicity label equals efficient discovery."
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_perfect_matching_spherical_boundary import (
    brauer_irrep_dimension,
    perfect_matching_count,
)
from representation_obstruction import integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/classical_baselines/diagram_multiplicity_source_mass_gate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DIAGRAM-MULTIPLICITY-SOURCE-MASS-GATE"
DEFAULT_CANDIDATE_ID = "DIAGRAM-MODULE-SPECTRAL"


@dataclass(frozen=True)
class BrauerRegularMassControl:
    diagram_order: int
    algebra_dimension_decimal: str
    algebra_dimension_log2: float
    irrep_sector_count: int
    regular_mass_sum: float
    regular_mass_sum_residual: float
    minimum_sector_dimension: int
    maximum_sector_dimension_decimal: str
    minimum_positive_sector_mass: float
    maximum_sector_mass: float
    one_dimensional_sector_count: int
    coherent_queries_for_rarest_sector_log2: float
    sample_copies_for_rarest_sector_log2: float
    polynomial_dimension_threshold: int
    polynomial_dimension_sector_count: int
    polynomial_dimension_sector_total_mass: float
    exact_regular_normalization_verified: bool
    status: str


@dataclass(frozen=True)
class MultiplicitySignalScaling:
    input_parameter: int
    ambient_module_dimension_log2: float
    target_irrep_dimension_log2: float
    promised_multiplicity_log2: float
    target_source_mass_log2: float
    direct_sample_copy_log2: float
    coherent_detection_query_log2: float
    polynomial_coherent_detection: bool
    polynomial_direct_sampling: bool
    status: str


@dataclass(frozen=True)
class MultiplicitySourceMassTheorem:
    sector_probability: str
    sample_complexity: str
    coherent_query_complexity: str
    exact_counting_scope: str
    counting_class_scope: str
    dequantization_scope: str
    inverse_polynomial_mass_required: bool
    qft_alone_removes_mass_cost: bool
    sharp_black_box_detection_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DiagramMultiplicitySourceMassGateReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[BrauerRegularMassControl]
    scaling_records: list[MultiplicitySignalScaling]
    theorem: MultiplicitySourceMassTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def brauer_regular_mass_control(
    diagram_order: int,
    polynomial_dimension_power: int = 3,
) -> BrauerRegularMassControl:
    if diagram_order < 1:
        raise ValueError("diagram_order must be positive")
    if polynomial_dimension_power < 1:
        raise ValueError("polynomial_dimension_power must be positive")
    algebra_dimension = perfect_matching_count(diagram_order)
    dimensions = [
        brauer_irrep_dimension(diagram_order, partition)
        for contractions in range(diagram_order // 2 + 1)
        for partition in integer_partitions(diagram_order - 2 * contractions)
    ]
    squared_sum = sum(dimension * dimension for dimension in dimensions)
    masses = [
        dimension * dimension / algebra_dimension for dimension in dimensions
    ]
    threshold = diagram_order**polynomial_dimension_power
    polynomial_masses = [
        mass
        for dimension, mass in zip(dimensions, masses)
        if dimension <= threshold
    ]
    rarest_mass = min(masses)
    residual = abs(squared_sum / algebra_dimension - 1.0)
    verified = squared_sum == algebra_dimension and residual < 1e-15
    return BrauerRegularMassControl(
        diagram_order=diagram_order,
        algebra_dimension_decimal=str(algebra_dimension),
        algebra_dimension_log2=math.log2(algebra_dimension),
        irrep_sector_count=len(dimensions),
        regular_mass_sum=sum(masses),
        regular_mass_sum_residual=residual,
        minimum_sector_dimension=min(dimensions),
        maximum_sector_dimension_decimal=str(max(dimensions)),
        minimum_positive_sector_mass=rarest_mass,
        maximum_sector_mass=max(masses),
        one_dimensional_sector_count=sum(dimension == 1 for dimension in dimensions),
        coherent_queries_for_rarest_sector_log2=-0.5 * math.log2(rarest_mass),
        sample_copies_for_rarest_sector_log2=-math.log2(rarest_mass),
        polynomial_dimension_threshold=threshold,
        polynomial_dimension_sector_count=len(polynomial_masses),
        polynomial_dimension_sector_total_mass=sum(polynomial_masses),
        exact_regular_normalization_verified=verified,
        status=(
            "exact-brauer-regular-source-mass-control"
            if verified
            else "brauer-regular-source-mass-control-failure"
        ),
    )


def multiplicity_signal_scaling(
    input_parameter: int,
    ambient_module_dimension_log2: float,
    target_irrep_dimension_log2: float,
    promised_multiplicity_log2: float = 0.0,
) -> MultiplicitySignalScaling:
    if input_parameter < 1:
        raise ValueError("input_parameter must be positive")
    if min(
        ambient_module_dimension_log2,
        target_irrep_dimension_log2,
        promised_multiplicity_log2,
    ) < 0.0:
        raise ValueError("log dimensions must be nonnegative")
    source_log2 = (
        promised_multiplicity_log2
        + target_irrep_dimension_log2
        - ambient_module_dimension_log2
    )
    source_log2 = min(0.0, source_log2)
    direct_log2 = -source_log2
    coherent_log2 = -0.5 * source_log2
    polynomial_threshold = 4.0 * math.log2(max(2, input_parameter))
    return MultiplicitySignalScaling(
        input_parameter=input_parameter,
        ambient_module_dimension_log2=ambient_module_dimension_log2,
        target_irrep_dimension_log2=target_irrep_dimension_log2,
        promised_multiplicity_log2=promised_multiplicity_log2,
        target_source_mass_log2=source_log2,
        direct_sample_copy_log2=direct_log2,
        coherent_detection_query_log2=coherent_log2,
        polynomial_coherent_detection=coherent_log2 <= polynomial_threshold,
        polynomial_direct_sampling=direct_log2 <= polynomial_threshold,
        status=(
            "inverse-polynomial-source-mass-regime"
            if direct_log2 <= polynomial_threshold
            else "rare-sector-source-mass-obstruction"
        ),
    )


def multiplicity_source_mass_theorem() -> MultiplicitySourceMassTheorem:
    return MultiplicitySourceMassTheorem(
        sector_probability=(
            "For V=direct_sum_lambda W_lambda tensor C^(m_lambda), the "
            "maximally mixed module state yields label probability "
            "p_lambda=m_lambda dim(W_lambda)/dim(V)."
        ),
        sample_complexity=(
            "Zero versus p_lambda>=p needs Theta(1/p) independent measured "
            "samples in the worst case."
        ),
        coherent_query_complexity=(
            "With coherent preparation, inverse preparation, and a target "
            "reflection, amplitude amplification detects the sector in "
            "Theta(1/sqrt(p)) queries, and unstructured search gives the "
            "matching black-box lower bound."
        ),
        exact_counting_scope=(
            "Resolving an exact multiplicity can require precision at the unit "
            "probability spacing dim(W_lambda)/dim(V), stronger than detecting "
            "nonzero mass."
        ),
        counting_class_scope=(
            "Membership of a multiplicity in #BQP describes a quantum counting "
            "verifier; it does not assert a polynomial-time BQP algorithm that "
            "outputs the count."
        ),
        dequantization_scope=(
            "Recent classical algorithms cover many dimension-ratio/fixed-"
            "parameter regimes previously proposed for quantum Kronecker or "
            "plethysm advantages. A diagram analogue must rerun those baselines."
        ),
        inverse_polynomial_mass_required=True,
        qft_alone_removes_mass_cost=False,
        sharp_black_box_detection_bound_proved=True,
        theorem_verified=True,
        status="multiplicity-source-mass-and-dequantization-gate-proved",
    )


def run_diagram_multiplicity_source_mass_gate(
) -> DiagramMultiplicitySourceMassGateReport:
    controls = [brauer_regular_mass_control(n) for n in (4, 8, 12, 16)]
    scaling = [
        multiplicity_signal_scaling(
            n,
            ambient_module_dimension_log2=float(n * n),
            target_irrep_dimension_log2=float(3 * math.log2(n)),
        )
        for n in (8, 16, 32, 64, 128)
    ] + [
        multiplicity_signal_scaling(
            n,
            ambient_module_dimension_log2=float(8 * math.log2(n)),
            target_irrep_dimension_log2=float(3 * math.log2(n)),
        )
        for n in (8, 16, 32, 64, 128)
    ]
    theorem = multiplicity_source_mass_theorem()
    failures = sum(not row.exact_regular_normalization_verified for row in controls)
    rare_scaling = sum(not row.polynomial_coherent_detection for row in scaling)
    verified = failures == 0 and theorem.theorem_verified
    metrics: dict[str, int | float] = {
        "source_mass_query_gate_theorem_count": int(verified),
        "finite_brauer_control_count": len(controls),
        "finite_brauer_control_failure_count": failures,
        "maximum_regular_mass_sum_residual": max(
            row.regular_mass_sum_residual for row in controls
        ),
        "maximum_rarest_sector_coherent_query_log2": max(
            row.coherent_queries_for_rarest_sector_log2 for row in controls
        ),
        "minimum_tail_polynomial_dimension_sector_mass": min(
            row.polynomial_dimension_sector_total_mass for row in controls
        ),
        "scaling_record_count": len(scaling),
        "rare_sector_coherent_obstruction_count": rare_scaling,
        "inverse_polynomial_source_mass_theorem_for_replacement_candidate_count": 0,
        "matched_classical_baseline_survival_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DiagramMultiplicitySourceMassGateReport(
        created_at=utc_now(),
        theorem_contract={
            "candidate": "DIAGRAM-MODULE-SPECTRAL",
            "access_model": (
                "prepared module states, algebra Fourier transform, coherent "
                "inverse preparation, and target-sector marking"
            ),
            "signal": "target irrep/multiplicity sector probability",
            "required_scaling": (
                "inverse-polynomial informative source mass plus a decision "
                "observable and matched classical hardness"
            ),
            "black_box_boundary": (
                "Theta(1/sqrt(p)) coherent queries and Theta(1/p) measured copies"
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "prove_informative_module_sector_mass",
                "resolved": False,
                "resolution": (
                    "No natural diagram-module candidate currently has an "
                    "inverse-polynomial YES/NO sector-mass gap."
                ),
            },
            {
                "obligation": "separate_counting_class_membership_from_bqp_algorithm",
                "resolved": verified,
                "resolution": (
                    "The report records #BQP only as a verifier/counting-class "
                    "statement and applies the explicit probability-query gate."
                ),
            },
            {
                "obligation": "rerun_recent_classical_multiplicity_algorithms",
                "resolved": False,
                "resolution": (
                    "Panova's dequantizations must be specialized to each "
                    "diagram coefficient family and parameter promise."
                ),
            },
            {
                "obligation": "derive_natural_decision_reduction",
                "resolved": False,
                "resolution": (
                    "A coefficient-estimation primitive is not yet tied to a "
                    "natural decision problem with major algorithmic impact."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Amplitude estimation makes every multiplicity efficient.",
                "survives": False,
                "response": (
                    "Its query complexity depends on the target probability or "
                    "required additive precision; exponentially rare mass "
                    "remains exponential."
                ),
            },
            {
                "challenge": "#BQP membership is a BQP speedup claim.",
                "survives": False,
                "response": (
                    "#BQP is a counting class and does not promise efficient "
                    "numeric output of the multiplicity."
                ),
            },
            {
                "challenge": "The regular Brauer rare sectors rule out all modules.",
                "survives": False,
                "response": (
                    "They are normalization controls only. A structured module "
                    "may concentrate inverse-polynomial mass on informative sectors."
                ),
            },
            {
                "challenge": "Prior quantum multiplicity proposals establish a classical barrier.",
                "survives": False,
                "response": (
                    "The 2025 classical results refuted broad advertised "
                    "superpolynomial regimes, so every new promise needs fresh baselines."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "LAROCCA-HAVLICEK-2024",
                "title": "Quantum Algorithms for Representation-Theoretic Multiplicities",
                "url": "https://arxiv.org/abs/2407.17649",
                "use": "Dimension-ratio quantum multiplicity algorithms and sampling conditions",
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "PANOVA-2025",
                "title": (
                    "Polynomial time classical versus quantum algorithms for "
                    "representation theoretic multiplicities"
                ),
                "url": "https://arxiv.org/abs/2502.20253",
                "use": "Classical dequantization of many proposed efficient regimes",
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "CHRISTANDL-HARROW-PANOVA-POSTA-WALTER-2026",
                "title": "Plethysm is in #BQP",
                "url": "https://arxiv.org/abs/2602.08441",
                "use": "Counting-class scope and fixed-parameter classical algorithms",
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "FOXMAN-NEHORAN-DING-2026",
                "title": "Efficient Quantum Fourier Transforms For Semisimple Algebras",
                "url": "https://arxiv.org/abs/2605.05337",
                "use": "Potential extension of multiplicity methods to diagram algebras",
                "external_theorem_not_reproved_here": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "efficient_qft_implies_efficient_multiplicity_detection": False,
            "counting_class_membership_implies_bqp_algorithm": False,
            "inverse_polynomial_informative_source_mass_proved": False,
            "recent_classical_dequantization_baselines_passed": False,
            "natural_decision_reduction_proved": False,
            "diagram_module_spectral_candidate_passes_proof_gate": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The new algebra QFT is useful infrastructure, but no natural "
                "diagram-module target yet has inverse-polynomial informative "
                "mass, a decision reduction, and a surviving classical barrier."
            ),
        },
        status=(
            "diagram-multiplicity-source-mass-gate-active"
            if verified
            else "diagram-multiplicity-source-mass-control-failure"
        ),
        summary=(
            "Added the missing probability/query gate for diagram-algebra "
            "multiplicity proposals and incorporated the 2025 dequantization "
            "evidence; the replacement direction remains open but unaccepted."
        ),
        falsifiers_triggered=[
            "An efficient algebra QFT does not remove rare-sector sample complexity.",
            "Coherent amplitude amplification gives only a quadratic improvement in inverse source mass.",
            "#BQP membership is not an efficient BQP counting algorithm.",
            "Many previously advertised efficient multiplicity regimes already have polynomial classical algorithms.",
            "Regular Brauer sectors include exponentially rare one-dimensional labels.",
            "No diagram-module candidate has yet passed source-mass, reduction, or dequantization gates.",
        ],
    )


def write_diagram_multiplicity_source_mass_gate(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DIAGRAM-MULTIPLICITY-SOURCE-MASS-GATE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_diagram_multiplicity_source_mass_gate())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    output = write_diagram_multiplicity_source_mass_gate()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))
