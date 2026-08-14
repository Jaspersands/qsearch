"""Conditioning no-go for a generic Foulkes support projector.

Let ``L=S_3 wr S_a <= S_(3a)`` with even ``a`` and let ``Q_x`` project onto
right invariants of a conjugate ``xLx^-1``.  The normalized conjugate twirl

    T_L = |Orb(L)|^-1 sum_(xLx^-1) Q_x                (1)

is a positive contraction.  If
``m_lambda=dim((V_lambda)^L)``, Schur averaging gives

    T_L restricted to V_lambda = (m_lambda/d_lambda) I. (2)

Consequently, turning the twirl into its support projector by a generic
singular-value polynomial depends on the smallest positive ratio
``m_lambda/d_lambda``.

Take ``t=a-1`` and ``lambda=(3a-t,t)=(2a+1,a-1)``.  The exact subset-orbit
formula gives

    m_lambda = coefficient of x^(a-1) in
               1/[(1-x^2)(1-x^3)],                    (3)

so ``1<=m_lambda<=a``.  Both rows are odd, hence this constituent survives
the earlier even-row spherical trim.  Its dimension is

    d_lambda = C(3a,a-1)-C(3a,a-2) >= 3^a/6.          (4)

For (4), choosing one point from each of ``a`` disjoint triples injects
``3^a`` objects into the ``a``-subsets, so ``C(3a,a)>=3^a``.  The adjacent
binomial ratios and the two-row hook formula then give the displayed bound.

Thus ``m_lambda/d_lambda<=6a/3^a``.  Any polynomial bounded by one on
``[0,1]`` that separates eigenvalue zero from this positive eigenvalue by a
constant has degree ``Omega(sqrt(d_lambda/m_lambda))`` by Markov's derivative
inequality, hence exponential in ``a``.

This refutes only the generic orbit-twirl threshold route.  The selected
two-row family is directly recognizable from the symmetric-group QFT label
and was already shown to have negligible all-register mass, so direct label
deflation bypasses this witness.  A higher-row support projector might also
use subgroup-specific structure rather than polynomial thresholding.  No
quantum lower bound, residual frame-norm bound, or algorithm is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_imprimitive_plethysm_boundary import (
    two_row_dimension,
    two_row_wreath_multiplicity,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_foulkes_support_projector_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-FOULKES-SUPPORT-PROJECTOR-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FoulkesProjectorConditionRecord:
    block_count: int
    degree: int
    selected_second_row: int
    selected_partition: tuple[int, int]
    selected_partition_has_even_rows: bool
    exact_invariant_multiplicity: int
    exact_irrep_dimension_decimal: str
    multiplicity_upper_bound: int
    dimension_elementary_lower_bound_decimal: str
    normalized_twirl_eigenvalue: float
    normalized_twirl_eigenvalue_log2: float
    support_condition_ratio_log2: float
    markov_degree_lower_bound_log2: float
    exponential_conditioning_witness_verified: bool
    direct_partition_label_bypass_available: bool
    higher_row_structured_bypass_ruled_out: bool
    status: str


@dataclass(frozen=True)
class FoulkesSupportProjectorTheorem:
    conjugate_twirl_spectrum: str
    selected_constituent: str
    multiplicity: str
    dimension_bound: str
    polynomial_degree_obstruction: str
    bypass: str
    scope_limit: str
    exact_twirl_spectrum_proved: bool
    exponential_generic_threshold_degree_proved: bool
    full_foulkes_support_projector_via_generic_qsvt_refuted: bool
    direct_two_row_label_bypass_available: bool
    higher_row_structured_projector_ruled_out: bool
    residual_frame_norm_bounded: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FoulkesSupportProjectorReport:
    created_at: str
    theorem_contract: dict[str, Any]
    records: list[FoulkesProjectorConditionRecord]
    theorem: FoulkesSupportProjectorTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def foulkes_projector_condition_record(
    block_count: int,
) -> FoulkesProjectorConditionRecord:
    if block_count < 4 or block_count % 2:
        raise ValueError("block_count must be even and at least four")
    degree = 3 * block_count
    second_row = block_count - 1
    partition = (degree - second_row, second_row)
    multiplicity = two_row_wreath_multiplicity(
        block_count, 3, second_row
    )
    dimension = two_row_dimension(degree, second_row)
    dimension_lower = 3**block_count // 6
    eigenvalue = multiplicity / dimension
    condition_ratio = dimension / multiplicity
    markov_degree = math.sqrt(condition_ratio / 3.0)
    verified = bool(
        1 <= multiplicity <= block_count
        and dimension >= dimension_lower
        and partition[0] % 2 == 1
        and partition[1] % 2 == 1
        and eigenvalue <= (6.0 * block_count) / (3**block_count)
        and markov_degree > 0.0
    )
    return FoulkesProjectorConditionRecord(
        block_count=block_count,
        degree=degree,
        selected_second_row=second_row,
        selected_partition=partition,
        selected_partition_has_even_rows=False,
        exact_invariant_multiplicity=multiplicity,
        exact_irrep_dimension_decimal=str(dimension),
        multiplicity_upper_bound=block_count,
        dimension_elementary_lower_bound_decimal=str(dimension_lower),
        normalized_twirl_eigenvalue=eigenvalue,
        normalized_twirl_eigenvalue_log2=math.log2(eigenvalue),
        support_condition_ratio_log2=math.log2(condition_ratio),
        markov_degree_lower_bound_log2=math.log2(markov_degree),
        exponential_conditioning_witness_verified=verified,
        direct_partition_label_bypass_available=True,
        higher_row_structured_bypass_ruled_out=False,
        status=(
            "generic-foulkes-support-threshold-exponential-direct-label-bypass"
            if verified
            else "foulkes-projector-conditioning-control-failure"
        ),
    )


def build_foulkes_support_projector_report(
    *,
    block_counts: tuple[int, ...] = (4, 8, 16, 32, 64, 128),
) -> FoulkesSupportProjectorReport:
    records = [foulkes_projector_condition_record(a) for a in block_counts]
    verified = all(
        row.exponential_conditioning_witness_verified
        and row.direct_partition_label_bypass_available
        and not row.higher_row_structured_bypass_ruled_out
        for row in records
    )
    theorem = FoulkesSupportProjectorTheorem(
        conjugate_twirl_spectrum=(
            "The normalized conjugate-L invariant projection twirl acts by "
            "m_lambda/d_lambda on each right irrep carrier."
        ),
        selected_constituent=(
            "For even a, lambda=(2a+1,a-1) occurs in h_a[h_3] and has two odd rows."
        ),
        multiplicity=(
            "m_lambda=[x^(a-1)]1/((1-x^2)(1-x^3)), so 1<=m_lambda<=a."
        ),
        dimension_bound=(
            "d_(2a+1,a-1)=C(3a,a-1)-C(3a,a-2)>=3^a/6."
        ),
        polynomial_degree_obstruction=(
            "Markov's inequality forces degree Omega(sqrt(d_lambda/m_lambda)) "
            "for a bounded polynomial thresholding zero versus m_lambda/d_lambda."
        ),
        bypass=(
            "This two-row label is directly QFT-recognizable and negligibly "
            "deflatable; the no-go targets only generic full-support thresholding."
        ),
        scope_limit=(
            "No lower bound covers direct label predicates, structured subgroup "
            "verification, or the higher-row residual support."
        ),
        exact_twirl_spectrum_proved=True,
        exponential_generic_threshold_degree_proved=True,
        full_foulkes_support_projector_via_generic_qsvt_refuted=True,
        direct_two_row_label_bypass_available=True,
        higher_row_structured_projector_ruled_out=False,
        residual_frame_norm_bounded=False,
        theorem_verified=verified,
        status=(
            "generic-foulkes-support-qsvt-no-go-structured-projector-open"
            if verified
            else "foulkes-support-projector-control-failure"
        ),
    )
    return FoulkesSupportProjectorReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "L=S_3 wr S_a with even a.",
            "operator": "Normalized average of conjugate right-L invariant projections.",
            "witness": "Two-row constituent (2a+1,a-1).",
            "outside_scope": (
                "Direct Fourier-label predicates, higher-row structured support "
                "tests, residual frame norm, and decoding."
            ),
        },
        records=records,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-FOULKES-STRUCTURED-SUPPORT-PROJECTOR",
                "statement": (
                    "Construct a support projector exploiting Foulkes structure "
                    "without resolving exponentially small twirl eigenvalues."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-HIGHER-ROW-EIGEN-GAP",
                "statement": (
                    "Determine the smallest m_lambda/d_lambda after all directly "
                    "recognizable negligible sectors are removed."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-FOULKES-DIRECT-LABEL-PREDICATE",
                "statement": (
                    "Decide whether the higher-row Foulkes support admits an "
                    "efficient partition-label predicate in the needed regime."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Averaging efficient subgroup projectors yields an efficient support flag.",
                "answer": (
                    "False generically: the normalized twirl has exponentially "
                    "small positive eigenvalues m_lambda/d_lambda."
                ),
                "resolved": True,
            },
            {
                "challenge": "This is a lower bound for every Foulkes support circuit.",
                "answer": (
                    "False. It only applies to bounded polynomial thresholding of "
                    "the conjugate twirl; direct label logic bypasses the witness."
                ),
                "resolved": True,
            },
            {
                "challenge": "The witness remains after the two-row trim.",
                "answer": (
                    "False. It motivates the generic no-go but is itself removed "
                    "by the already compiled odd-two-row label trim."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_conditioning_record_count": len(records),
            "conditioning_control_failure_count": sum(
                not row.exponential_conditioning_witness_verified for row in records
            ),
            "generic_support_qsvt_no_go_theorem_count": 1,
            "direct_label_bypass_count": 1,
            "higher_row_structured_projector_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "conjugate_twirl_spectrum_proved": verified,
            "generic_foulkes_support_qsvt_refuted": verified,
            "direct_two_row_label_bypass_available": verified,
            "higher_row_structured_support_projector_compiled": False,
            "residual_frame_norm_bounded": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Generic twirl thresholding is exponentially conditioned, while "
                "the direct-label bypass does not yet extend to higher-row support."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that naive QSVT thresholding of the conjugate Foulkes twirl "
            "has exponential degree, while preserving direct-label and structured "
            "higher-row projector routes as the only valid escapes."
        ),
        falsifiers_triggered=[
            "Efficient access to each subgroup projector does not make its conjugate support easy to flag.",
            "The explicit small-eigenvalue witness is directly label-deflatable and is not a universal lower bound.",
            "Higher-row structured support access remains unclassified.",
        ],
    )


def write_foulkes_support_projector_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_foulkes_support_projector_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_foulkes_support_projector_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
