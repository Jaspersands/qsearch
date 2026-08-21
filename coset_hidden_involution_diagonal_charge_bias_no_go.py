"""Exact bias bound for the simplest all-copy target-coupled charges.

The proper-marginal no-go forces a useful group-algebra statistic to couple
all ``k`` source coordinates to the target.  The most direct such element is

    a_t = (t,...,t;t) in A <= L=G^k x G.

Compress it to the source space as ``X_t=e_B a_t e_B`` and let
``Z=M e_B e_A e_B`` be the squared source-synthesis likelihood, where
``M=[G:K]`` and ``K=C_G(h)``.  Exact ``B A B`` factorization gives

    tr_B(X_t)   = 1[t in K],
    tr_B(X_t Z) = 1                    if t in K,
                  2^(-k)              if t not in K.

For ``t not in K``, each source equation
``eps_i t eps'_i=t`` has only the trivial solution; for ``t in K`` it has two.
Thus a Hermitian diagonal convolution

    X_alpha=e_B (sum_t alpha_t a_t) e_B,
    alpha_(t^-1)=conj(alpha_t),

has alternative-minus-baseline bias

    2^(-k) sum_(t not in K) alpha_t,

whose magnitude is at most ``2^(-k)||alpha||_1``.  At the natural flatness
copy count ``k=ceil(log2(64M))``, every unit-normalized diagonal LCU has bias
at most ``1/(64M)``.  Constant linear bias requires exponential LCU
normalization and simply recreates the orbit-label normalization barrier.

This does not rule out powers of ``e_B y e_B``, interleaved B/A walks,
nonlinear spectral tests, or more general all-copy recoupling operators.  It
rules out the obvious normalized diagonal class-sum charge as a detector.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from coset_hidden_involution_orbit_synthesis_flatness import (
    flatness_copy_count,
)
from coset_hidden_involution_source_local_likelihood_no_go import (
    _BAB_counts,
    _product_inverse,
    _subgroups,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_diagonal_charge_bias_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-DIAGONAL-CHARGE-BIAS-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class DiagonalElementBiasControl:
    degree: int
    transposition_count: int
    copy_count: int
    group_order: int
    centralizer_order: int
    conjugacy_class_size: int
    centralizer_element_count: int
    noncentralizer_element_count: int
    expected_inside_centralizer_weighted_trace: str
    expected_outside_centralizer_weighted_trace: str
    maximum_baseline_formula_residual: float
    maximum_likelihood_formula_residual: float
    exact_elementwise_bias_formula_verified: bool
    status: str


@dataclass(frozen=True)
class DiagonalChargeScalingRecord:
    half_degree: int
    degree: int
    conjugacy_class_size_decimal: str
    copy_count: int
    unit_LCU_bias_upper_bound: float
    unit_LCU_bias_log2_upper_bound: float
    inverse_candidate_bound: float
    bound_at_most_inverse_64_candidates: bool
    constant_bias_LCU_norm_lower_bound_decimal: str
    normalized_diagonal_LCU_has_constant_bias: bool
    status: str


@dataclass(frozen=True)
class DiagonalChargeBiasNoGoTheorem:
    diagonal_element: str
    compressed_observable: str
    baseline_trace: str
    likelihood_weighted_trace: str
    signed_LCU_bias: str
    natural_copy_consequence: str
    scope_limit: str
    exact_all_finite_groups_elementwise_formula_proved: bool
    unit_LCU_bias_upper_bound_proved: bool
    natural_copy_bias_inverse_candidate_bound_proved: bool
    normalized_diagonal_class_charge_detector_ruled_out: bool
    interleaved_recoupling_walk_ruled_out: bool
    nonlinear_spectral_decoder_constructed: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DiagonalChargeBiasNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[DiagonalElementBiasControl]
    scaling_records: list[DiagonalChargeScalingRecord]
    theorem: DiagonalChargeBiasNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_diagonal_element_bias(
    degree: int,
    transposition_count: int,
    copy_count: int,
) -> DiagonalElementBiasControl:
    group, centralizer, diagonal, source_stabilizer, _ = _subgroups(
        degree,
        transposition_count,
        copy_count,
    )
    counts = _BAB_counts(diagonal, source_stabilizer)
    source_stabilizer_set = set(source_stabilizer)
    B_order = len(source_stabilizer)
    M = len(group) // len(centralizer)
    expected_outside = Fraction(1, 2**copy_count)
    maximum_baseline_residual = Fraction(0, 1)
    maximum_likelihood_residual = Fraction(0, 1)
    for target in group:
        element = (target,) * (copy_count + 1)
        inverse_element = _product_inverse(element)
        baseline = Fraction(
            int(inverse_element in source_stabilizer_set),
            1,
        )
        likelihood = Fraction(
            M * B_order * counts.get(inverse_element, 0),
            B_order**2 * len(diagonal),
        )
        expected_baseline = Fraction(int(target in centralizer), 1)
        expected_likelihood = (
            Fraction(1, 1)
            if target in centralizer
            else expected_outside
        )
        maximum_baseline_residual = max(
            maximum_baseline_residual,
            abs(baseline - expected_baseline),
        )
        maximum_likelihood_residual = max(
            maximum_likelihood_residual,
            abs(likelihood - expected_likelihood),
        )
    verified = bool(
        maximum_baseline_residual == 0
        and maximum_likelihood_residual == 0
    )
    return DiagonalElementBiasControl(
        degree=degree,
        transposition_count=transposition_count,
        copy_count=copy_count,
        group_order=len(group),
        centralizer_order=len(centralizer),
        conjugacy_class_size=M,
        centralizer_element_count=len(centralizer),
        noncentralizer_element_count=len(group) - len(centralizer),
        expected_inside_centralizer_weighted_trace="1",
        expected_outside_centralizer_weighted_trace=str(expected_outside),
        maximum_baseline_formula_residual=float(maximum_baseline_residual),
        maximum_likelihood_formula_residual=float(maximum_likelihood_residual),
        exact_elementwise_bias_formula_verified=verified,
        status=(
            "exact-diagonal-element-bias-formula-verified"
            if verified
            else "diagonal-element-bias-control-failure"
        ),
    )


def diagonal_charge_scaling_record(
    half_degree: int,
) -> DiagonalChargeScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    bias = 2.0 ** (-copies)
    inverse_candidate_bound = 1.0 / (64.0 * candidates)
    verified = bias <= inverse_candidate_bound * (1.0 + 1e-15)
    return DiagonalChargeScalingRecord(
        half_degree=half_degree,
        degree=degree,
        conjugacy_class_size_decimal=str(candidates),
        copy_count=copies,
        unit_LCU_bias_upper_bound=bias,
        unit_LCU_bias_log2_upper_bound=-float(copies),
        inverse_candidate_bound=inverse_candidate_bound,
        bound_at_most_inverse_64_candidates=verified,
        constant_bias_LCU_norm_lower_bound_decimal=str(2**copies),
        normalized_diagonal_LCU_has_constant_bias=False,
        status=(
            "diagonal-LCU-bias-below-inverse-candidate-scale"
            if verified
            else "diagonal-LCU-scaling-control-failure"
        ),
    )


def build_diagonal_charge_bias_no_go_report() -> DiagonalChargeBiasNoGoReport:
    controls = [
        audit_diagonal_element_bias(3, 1, 2),
        audit_diagonal_element_bias(4, 2, 2),
        audit_diagonal_element_bias(3, 1, 3),
    ]
    scaling = [
        diagonal_charge_scaling_record(half_degree)
        for half_degree in (4, 8, 16, 32, 64)
    ]
    verified = bool(
        all(control.exact_elementwise_bias_formula_verified for control in controls)
        and all(row.bound_at_most_inverse_64_candidates for row in scaling)
    )
    theorem = DiagonalChargeBiasNoGoTheorem(
        diagonal_element="a_t=(t,...,t;t) in the diagonal subgroup A",
        compressed_observable="X_t=e_B a_t e_B on the B-fixed source space",
        baseline_trace="tr_B(X_t)=1[t in K]",
        likelihood_weighted_trace=(
            "tr_B(X_t Z)=1 for t in K and 2^(-k) for t outside K"
        ),
        signed_LCU_bias=(
            "tr_B(X_alpha Z)-tr_B(X_alpha)="
            "2^(-k) sum_(t outside K) alpha_t"
        ),
        natural_copy_consequence=(
            "At k=ceil(log2(64M)), every ||alpha||_1<=1 diagonal LCU "
            "has bias at most 1/(64M)."
        ),
        scope_limit=(
            "Does not cover powers/interleavings of e_B y e_B, nonlinear "
            "spectral tests, or non-diagonal all-copy recoupling operators."
        ),
        exact_all_finite_groups_elementwise_formula_proved=True,
        unit_LCU_bias_upper_bound_proved=True,
        natural_copy_bias_inverse_candidate_bound_proved=True,
        normalized_diagonal_class_charge_detector_ruled_out=True,
        interleaved_recoupling_walk_ruled_out=False,
        nonlinear_spectral_decoder_constructed=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "normalized-diagonal-all-copy-charge-bias-no-go-proved"
            if verified
            else "diagonal-charge-bias-no-go-control-failure"
        ),
    )
    return DiagonalChargeBiasNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": "finite-group hidden-involution double-coset polar",
            "observable": (
                "Hermitian B-compressions of diagonal A-group LCUs with "
                "coefficient l1 normalization"
            ),
            "natural_copy_count": "k=ceil(log2(64[G:C_G(h)]))",
            "claim_boundary": (
                "Exact linear-bias no-go only; interleaved and nonlinear "
                "all-copy recoupling mechanisms remain open."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-INTERLEAVED-DIAGONAL-WALK",
                "statement": (
                    "Determine whether powers or polynomial filters of e_B y e_B "
                    "amplify likelihood bias with polynomial degree and normalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-NONDIAGONAL-ALL-COPY-CHARGE",
                "statement": (
                    "Search for B-compatible all-copy charges outside the diagonal "
                    "A convolution span with inverse-polynomial normalized bias."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-RECOUPLING-FAST-FORWARD",
                "statement": (
                    "Find a fast-forwardable recoupling walk whose spectral filter "
                    "approximates the source polar without M-scale normalization."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "An all-copy diagonal element already escapes the proper-marginal no-go.",
                "answer": (
                    "Yes, but its unit-normalized linear likelihood bias is exactly "
                    "2^(-k), inverse in the candidate count at natural k."
                ),
                "resolved": True,
            },
            {
                "challenge": "A conjugacy-class sum contains many diagonal elements.",
                "answer": (
                    "After the coefficient l1 normalization required by a direct "
                    "LCU block encoding, the same 2^(-k) upper bound remains."
                ),
                "resolved": True,
            },
            {
                "challenge": "The theorem proves every diagonal recoupling walk useless.",
                "answer": (
                    "False. Interleaved powers e_B y e_B y e_B contain new double-"
                    "coset paths and are explicitly outside the linear theorem."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "DOUBLE-COSET-POLAR-REDUCTION",
                "role": "Provides A, B, and the likelihood operator Z.",
            },
            {
                "id": "ORBIT-SYNTHESIS-FLATNESS",
                "role": "Provides the natural copy count k=ceil(log2(64M)).",
            },
        ],
        headline_metrics={
            "exact_elementwise_control_count": len(controls),
            "maximum_elementwise_formula_residual": max(
                max(
                    control.maximum_baseline_formula_residual,
                    control.maximum_likelihood_formula_residual,
                )
                for control in controls
            ),
            "natural_scaling_row_count": len(scaling),
            "minimum_unit_LCU_bias_log2_upper_bound": min(
                row.unit_LCU_bias_log2_upper_bound for row in scaling
            ),
        },
        claim_gate={
            "exact_diagonal_element_bias_formula_proved": True,
            "unit_normalized_diagonal_LCU_inverse_candidate_bias_proved": True,
            "normalized_diagonal_class_charge_detector_possible": False,
            "interleaved_recoupling_walk_ruled_out": False,
            "nonlinear_spectral_decoder_constructed": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The first all-copy diagonal escape has only 2^-k normalized "
                "linear bias; stronger interleaved/nonlinear structure is unresolved."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that every unit-normalized all-copy diagonal LCU has only "
            "inverse-candidate likelihood bias at the natural copy count."
        ),
        falsifiers_triggered=[
            "A normalized diagonal conjugacy-class charge does not evade orbit-label normalization.",
            "All-copy support alone is insufficient for a useful likelihood statistic.",
            "The next viable search space is interleaved or nonlinear recoupling walks.",
        ],
    )


def write_diagonal_charge_bias_no_go_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_diagonal_charge_bias_no_go_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_diagonal_charge_bias_no_go_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
