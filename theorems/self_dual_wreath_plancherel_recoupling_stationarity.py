"""Plancherel stationarity of dimension-weighted Kronecker recoupling.

For irreps ``lambda,mu`` of a finite group, sample an output irrep ``nu`` from

    K_(lambda,mu)(nu)
      = g(lambda,mu,nu) d_nu/(d_lambda d_mu),             (1)

the dimension-weighted decomposition of ``V_lambda tensor V_mu``.  If ``mu``
is Plancherel distributed, then for every fixed ``lambda``

    sum_mu (d_mu^2/|G|) K_(lambda,mu)(nu)
      = d_nu^2/|G|.                                      (2)

The proof is the regular-representation identity

    V_lambda tensor Reg(G) = d_lambda Reg(G),

or equivalently
``sum_mu d_mu g(lambda,mu,nu)=d_lambda d_nu``.  Therefore a
dimension-weighted recoupling output is exactly Plancherel and independent of
the other input whenever one input is fresh Plancherel noise.

Consequences for the wreath point-decoder search:

* every disjoint binary recoupling tree fed by independent Plancherel leaves
  has a Plancherel root;
* roots of disjoint trees are independent;
* one-box/transpose-edge admission between such roots remains bounded by
  polynomial Young degree times the maximal Plancherel atom, hence
  ``exp(-Theta(sqrt(n)))``;
* iterating independent recoupling cannot focus mass onto the rare sign-twist
  witness channels.

This theorem concerns the classical irrep-label law obtained by measuring the
dimension-weighted decomposition.  It does not dequantize coherent Racah
amplitudes, shared-source coupling trees, multiplicity registers, or hidden-
label-dependent transition filters.  Those correlations are now the only
viable recoupling escape within this mechanism.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import kronecker_coefficient


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_plancherel_recoupling_stationarity.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-RECOUPLING-STATIONARITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
MAXIMAL_DIMENSION_PAPER_ID = "aggarwal-elboim-maximal-dimension-2026"
MAXIMAL_DIMENSION_PAPER_URL = "https://arxiv.org/abs/2605.25995"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PlancherelRecouplingControl:
    n: int
    partition_count: int
    group_order: int
    fixed_input_count: int
    transition_row_normalization_residual: str
    maximum_stationarity_residual: str
    maximum_regular_multiplicity_identity_residual: int
    maximum_output_dependence_on_fixed_input_residual: str
    maximum_two_step_stationarity_residual: str
    exact_plancherel_stationarity_verified: bool
    status: str


@dataclass(frozen=True)
class RecouplingStationarityScalingRecord:
    n: int
    maximum_plancherel_atom_asymptotic: str
    disjoint_tree_root_law: str
    disjoint_tree_root_independence: bool
    local_young_degree_upper: float
    disjoint_root_young_edge_probability_upper_asymptotic: str
    independent_recoupling_focuses_rare_channels: bool
    shared_source_coherence_ruled_out: bool
    coherent_racah_transform_dequantized: bool
    status: str


@dataclass(frozen=True)
class PlancherelRecouplingTheorem:
    transition: str
    regular_identity: str
    stationarity: str
    disjoint_tree_consequence: str
    admission_consequence: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PlancherelRecouplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PlancherelRecouplingTheorem
    finite_controls: list[PlancherelRecouplingControl]
    scaling_records: list[RecouplingStationarityScalingRecord]
    literature_links: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def plancherel_weights(n: int) -> dict[Partition, Fraction]:
    if n < 1:
        raise ValueError("n must be positive")
    order = math.factorial(n)
    return {
        partition: Fraction(hook_length_dimension(partition) ** 2, order)
        for partition in integer_partitions(n)
    }


def dimension_weighted_kronecker_transition(
    left: Partition,
    right: Partition,
) -> dict[Partition, Fraction]:
    if sum(left) != sum(right):
        raise ValueError("partitions must have equal size")
    denominator = hook_length_dimension(left) * hook_length_dimension(right)
    return {
        target: Fraction(
            kronecker_coefficient(left, right, target)
            * hook_length_dimension(target),
            denominator,
        )
        for target in integer_partitions(sum(left))
    }


def recouple_against_plancherel(
    fixed: Partition,
) -> dict[Partition, Fraction]:
    weights = plancherel_weights(sum(fixed))
    output = {partition: Fraction() for partition in weights}
    for random_input, weight in weights.items():
        transition = dimension_weighted_kronecker_transition(fixed, random_input)
        for target, probability in transition.items():
            output[target] += weight * probability
    return output


def _push_distribution_against_plancherel(
    distribution: dict[Partition, Fraction],
) -> dict[Partition, Fraction]:
    n = sum(next(iter(distribution)))
    weights = plancherel_weights(n)
    output = {partition: Fraction() for partition in weights}
    for fixed, fixed_weight in distribution.items():
        conditional = recouple_against_plancherel(fixed)
        for target, probability in conditional.items():
            output[target] += fixed_weight * probability
    return output


def audit_plancherel_recoupling_stationarity(
    n: int,
) -> PlancherelRecouplingControl:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = tuple(integer_partitions(n))
    weights = plancherel_weights(n)
    row_residual = Fraction()
    stationarity_residual = Fraction()
    regular_residual = 0
    dependence_residual = Fraction()
    reference_output: dict[Partition, Fraction] | None = None
    for fixed in partitions:
        fixed_dimension = hook_length_dimension(fixed)
        for random_input in partitions:
            row = dimension_weighted_kronecker_transition(fixed, random_input)
            row_residual = max(row_residual, abs(sum(row.values()) - 1))
        output = recouple_against_plancherel(fixed)
        stationarity_residual = max(
            stationarity_residual,
            *(abs(output[target] - weights[target]) for target in partitions),
        )
        if reference_output is None:
            reference_output = output
        dependence_residual = max(
            dependence_residual,
            *(
                abs(output[target] - reference_output[target])
                for target in partitions
            ),
        )
        for target in partitions:
            regular_sum = sum(
                hook_length_dimension(random_input)
                * kronecker_coefficient(fixed, random_input, target)
                for random_input in partitions
            )
            regular_residual = max(
                regular_residual,
                abs(
                    regular_sum
                    - fixed_dimension * hook_length_dimension(target)
                ),
            )
    skew = {
        partition: Fraction(index + 1, len(partitions) * (len(partitions) + 1) // 2)
        for index, partition in enumerate(partitions)
    }
    if sum(skew.values()) != 1:
        raise ArithmeticError("test distribution must normalize")
    two_step = _push_distribution_against_plancherel(skew)
    two_step_residual = max(
        abs(two_step[target] - weights[target]) for target in partitions
    )
    verified = bool(
        row_residual == 0
        and stationarity_residual == 0
        and regular_residual == 0
        and dependence_residual == 0
        and two_step_residual == 0
    )
    return PlancherelRecouplingControl(
        n=n,
        partition_count=len(partitions),
        group_order=math.factorial(n),
        fixed_input_count=len(partitions),
        transition_row_normalization_residual=str(row_residual),
        maximum_stationarity_residual=str(stationarity_residual),
        maximum_regular_multiplicity_identity_residual=regular_residual,
        maximum_output_dependence_on_fixed_input_residual=str(dependence_residual),
        maximum_two_step_stationarity_residual=str(two_step_residual),
        exact_plancherel_stationarity_verified=verified,
        status=(
            "exact-plancherel-absorbing-recoupling-law"
            if verified
            else "plancherel-recoupling-validation-failure"
        ),
    )


def recoupling_stationarity_scaling_record(
    n: int,
) -> RecouplingStationarityScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    return RecouplingStationarityScalingRecord(
        n=n,
        maximum_plancherel_atom_asymptotic="exp(-Theta(sqrt(n)))",
        disjoint_tree_root_law="exact Plancherel",
        disjoint_tree_root_independence=True,
        local_young_degree_upper=(math.sqrt(2 * n) + 1) ** 2,
        disjoint_root_young_edge_probability_upper_asymptotic=(
            "poly(n) exp(-Theta(sqrt(n)))"
        ),
        independent_recoupling_focuses_rare_channels=False,
        shared_source_coherence_ruled_out=False,
        coherent_racah_transform_dequantized=False,
        status="disjoint-recoupling-stationary-shared-source-correlations-open",
    )


def run_plancherel_recoupling_stationarity() -> PlancherelRecouplingReport:
    controls = [
        audit_plancherel_recoupling_stationarity(n) for n in range(2, 11)
    ]
    scaling = [
        recoupling_stationarity_scaling_record(n)
        for n in (32, 64, 128, 256, 512, 1024)
    ]
    failures = sum(not row.exact_plancherel_stationarity_verified for row in controls)
    verified = failures == 0
    theorem = PlancherelRecouplingTheorem(
        transition=(
            "K_(lambda,mu)(nu)=g(lambda,mu,nu)d_nu/(d_lambda d_mu)."
        ),
        regular_identity=(
            "sum_mu d_mu g(lambda,mu,nu)=d_lambda d_nu from "
            "V_lambda tensor Reg=d_lambda Reg."
        ),
        stationarity=(
            "For every fixed lambda, averaging K_(lambda,mu) over Plancherel mu "
            "returns Plancherel nu, independent of lambda."
        ),
        disjoint_tree_consequence=(
            "Every disjoint dimension-weighted Kronecker tree with independent "
            "Plancherel leaves has independent Plancherel roots."
        ),
        admission_consequence=(
            "Independent recoupling cannot focus exact conjugate or one-box edge "
            "events beyond their stretched-exponential Plancherel mass."
        ),
        scope=(
            "Measured irrep-label stationarity does not dequantize shared-source "
            "coherence, Racah amplitudes, multiplicities, or transition filters."
        ),
        theorem_verified=verified,
        status=(
            "plancherel-recoupling-stationarity-proved-shared-correlation-open"
            if verified
            else "plancherel-recoupling-validation-failure"
        ),
    )
    return PlancherelRecouplingReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "supports": "The maximal Plancherel atom is exp(-Theta(sqrt(n))).",
                "external_theorem_not_reproved_here": True,
            }
        ],
        proof_obligations=[
            {
                "obligation": "derive_natural_dimension_weighted_recoupling_law",
                "resolved": verified,
                "resolution": (
                    "Plancherel is an exact absorbing/stationary law under Kronecker "
                    "recoupling with one fresh Plancherel input."
                ),
            },
            {
                "obligation": "test_independent_recoupling_as_rare_channel_focuser",
                "resolved": verified,
                "resolution": (
                    "Rejected: disjoint trees retain independent Plancherel roots."
                ),
            },
            {
                "obligation": "characterize_shared_source_recoupling_correlations",
                "resolved": False,
                "resolution": (
                    "Useful activation must reuse labels or preserve coherent "
                    "multiplicity/Racah correlations absent from the classical tree law."
                ),
            },
            {
                "obligation": "compile_label_adaptive_shared_source_transform",
                "resolved": False,
                "resolution": (
                    "No polynomial circuit or information-bearing filter is known."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Repeated random Kronecker recoupling concentrates onto useful intermediate shapes.",
                "resolved": True,
                "resolution": (
                    "False for dimension-weighted measured labels: one fresh "
                    "Plancherel input resets the output exactly to Plancherel."
                ),
            },
            {
                "objection": "Stationarity proves a classical simulation of the coherent decoder.",
                "resolved": True,
                "resolution": (
                    "False. It discards multiplicity phases and correlations between "
                    "overlapping coupling trees."
                ),
            },
            {
                "objection": "The sign-twist collective witness contradicts stationarity.",
                "resolved": True,
                "resolution": (
                    "No. Its useful channels share source labels and are deterministically "
                    "correlated across complementary orientations."
                ),
            },
        ],
        headline_metrics={
            "plancherel_recoupling_stationarity_theorem_count": 1,
            "regular_multiplicity_identity_theorem_count": 1,
            "disjoint_tree_root_law_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "independent_recoupling_rare_channel_focuser_count": 0,
            "shared_source_correlation_theorem_count": 0,
            "natural_collective_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "dimension_weighted_recoupling_preserves_plancherel": verified,
            "disjoint_recoupling_tree_roots_independent_plancherel": verified,
            "independent_recoupling_focuses_rare_channels": False,
            "shared_source_recoupling_dequantized": False,
            "coherent_racah_transform_dequantized": False,
            "typical_collective_energy_bound_proved": False,
            "polynomial_point_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Only shared-source coherent recoupling can evade the stationary "
                "classical label law, and its magnitude/access remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved exact Plancherel stationarity under dimension-weighted Kronecker "
            "recoupling. Independent/disjoint trees cannot focus rare useful channels; "
            "the surviving target is shared-source coherent recoupling."
        ),
        falsifiers_triggered=[
            (
                "Random independent Kronecker trees do not change the natural irrep "
                "label law at any depth."
            ),
            (
                "A useful collective mechanism must exploit overlap between coupling "
                "trees, shared source labels, or multiplicity coherence."
            ),
            (
                "Classical label stationarity must not be reported as a dequantization "
                "of coherent Racah processing."
            ),
        ],
    )


def write_plancherel_recoupling_stationarity_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-RECOUPLING-STATIONARITY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_plancherel_recoupling_stationarity" in globals():
        report = run_plancherel_recoupling_stationarity(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-PLANCHEREL-RECOUPLING-STATIONARITY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-RECOUPLING-STATIONARITY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-RECOUPLING-STATIONARITY.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
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
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_plancherel_recoupling_stationarity": str(path)
                },
            )
        )
    return payload
