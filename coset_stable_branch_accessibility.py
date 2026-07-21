"""Natural-input accessibility theorem for the solved stable W_n^tensor3 branch.

The stable recoupling workbench conditions three independent involution coset
states on W_n=(n-2,2), then projects the three row-representation registers to
the final diagonal irrep xi_n=(n-3,2,1).  The block encoding and inverse filter
inside that branch are polynomial, but this module prices reaching the branch
from the natural coset-state input.

Writing F for the 25-dimensional scaled multiplicity frame, the exact branch
probability is

    p_branch = d_W^3 d_xi Tr(F) / (n!)^3.

The identity follows either by tracing the three Fourier blocks directly or
by multiplying the three weak-label probabilities by the conditional final
projection probability.  Character ratios have absolute value at most one,
sum_eta g(W,W,eta)g(eta,W,xi)=25, and hence Tr(F)<=200.  Together with
d_W<=n^2/2 and d_xi<=n^3/3,

    p_branch <= (25/3) n^9 / (n!)^3
             <= (25/3) n^9 (e/n)^(3n).

Thus passive postselection and generic amplitude amplification both require
superpolynomial resources.  The fixed stable branch remains useful as a
mechanism and proof control, but it cannot itself support a polynomial natural-
input algorithm unless a new direct preparation route avoids this probability.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import sympy as sp

from coset_stable_shape_family_certificate import (
    FINAL_TAIL,
    SOURCE_TAIL,
    STABLE_TAILS,
)
from coset_stable_three_copy_frame_conditioning import (
    N,
    T,
    _character_ratio_expression,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_BRANCH_ACCESSIBILITY_PATH = Path(
    "research/representation/coset_stable_branch_accessibility.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-BRANCH-ACCESSIBILITY"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

BRANCH_MULTIPLICITIES = {
    (1,): 1,
    (2,): 4,
    (1, 1): 2,
    (3,): 2,
    (2, 1): 8,
    (1, 1, 1): 2,
    (4,): 1,
    (3, 1): 3,
    (2, 2): 2,
}


@dataclass(frozen=True)
class StableBranchAccessibilityRecord:
    n: int
    involution_family: str
    transposition_count: int
    source_dimension: int
    final_dimension: int
    group_order: int
    source_character_ratio: str
    final_character_ratio: str
    exact_scaled_frame_trace: str
    exact_source_label_probability: str
    log2_source_label_probability: float
    exact_conditional_final_projection_probability: str
    exact_branch_probability: str
    log2_branch_probability: float
    log2_expected_passive_samples: float
    log2_generic_amplitude_amplification_iterations: float
    exact_universal_probability_upper_bound: str
    probability_upper_bound_verified: bool
    polynomial_n8_budget_expected_hits: float
    natural_input_polynomial_accessible: bool
    status: str


@dataclass(frozen=True)
class StableBranchAccessibilityReport:
    created_at: str
    probability_theorem: dict[str, object]
    asymptotic_no_go: dict[str, object]
    records: list[StableBranchAccessibilityRecord]
    threshold_crossings: dict[str, dict[str, int | None]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _as_fraction(expression: sp.Expr) -> Fraction:
    rational = sp.cancel(expression)
    numerator, denominator = sp.fraction(rational)
    return Fraction(int(numerator), int(denominator))


def _log2_integer(value: int) -> float:
    if value <= 0:
        raise ValueError("logarithm requires a positive integer")
    bits = value.bit_length()
    shift = max(0, bits - 53)
    return math.log2(value >> shift) + shift


def log2_fraction(value: Fraction) -> float:
    if value <= 0:
        raise ValueError("logarithm requires a positive fraction")
    return _log2_integer(value.numerator) - _log2_integer(value.denominator)


@lru_cache(maxsize=1)
def exact_scaled_frame_trace_expression() -> sp.Expr:
    if tuple(BRANCH_MULTIPLICITIES) != STABLE_TAILS:
        raise ArithmeticError("branch multiplicities do not follow the stable tail order")
    if sum(BRANCH_MULTIPLICITIES.values()) != 25:
        raise ArithmeticError("stable branch multiplicities must sum to 25")
    source_ratio = _character_ratio_expression(SOURCE_TAIL)
    final_ratio = _character_ratio_expression(FINAL_TAIL)
    identity_scalar = 1 + 3 * source_ratio + final_ratio
    return sp.factor(
        sp.cancel(
            25 * identity_scalar
            + 3
            * sum(
                multiplicity * _character_ratio_expression(tail)
                for tail, multiplicity in BRANCH_MULTIPLICITIES.items()
            )
        )
    )


def source_dimension(n: int) -> int:
    return n * (n - 3) // 2


def final_dimension(n: int) -> int:
    return n * (n - 2) * (n - 4) // 3


def _family_specs(n: int) -> tuple[tuple[str, int], ...]:
    return (
        ("partial_matching_t_floor_n_over_4", n // 4),
        ("dense_matching_t_floor_n_over_2", n // 2),
    )


@lru_cache(maxsize=None)
def audit_stable_branch_accessibility(
    n: int,
    transposition_count: int,
    involution_family: str,
) -> StableBranchAccessibilityRecord:
    if n < 8:
        raise ValueError("the stable branch certificate starts at n=8")
    group_order = math.factorial(n)
    d_w = source_dimension(n)
    d_xi = final_dimension(n)
    source_ratio = _as_fraction(
        _character_ratio_expression(SOURCE_TAIL).subs({N: n, T: transposition_count})
    )
    final_ratio = _as_fraction(
        _character_ratio_expression(FINAL_TAIL).subs({N: n, T: transposition_count})
    )
    frame_trace = _as_fraction(
        exact_scaled_frame_trace_expression().subs({N: n, T: transposition_count})
    )
    source_label_probability = Fraction(d_w**2, group_order) * (1 + source_ratio)
    conditional_final_probability = Fraction(d_xi, 1) * frame_trace / (
        Fraction(d_w, 1) * (1 + source_ratio)
    ) ** 3
    branch_probability = Fraction(d_w**3 * d_xi, group_order**3) * frame_trace
    if source_label_probability**3 * conditional_final_probability != branch_probability:
        raise ArithmeticError("weak-label and direct branch probability formulas disagree")
    universal_upper_bound = Fraction(25 * n**9, 3 * group_order**3)
    upper_verified = branch_probability <= universal_upper_bound
    if not upper_verified:
        raise ArithmeticError("universal stable branch probability bound failed")
    log_probability = log2_fraction(branch_probability)
    expected_n8_hits = min(1.0, float(branch_probability * n**8))
    return StableBranchAccessibilityRecord(
        n=n,
        involution_family=involution_family,
        transposition_count=transposition_count,
        source_dimension=d_w,
        final_dimension=d_xi,
        group_order=group_order,
        source_character_ratio=str(source_ratio),
        final_character_ratio=str(final_ratio),
        exact_scaled_frame_trace=str(frame_trace),
        exact_source_label_probability=str(source_label_probability),
        log2_source_label_probability=log2_fraction(source_label_probability),
        exact_conditional_final_projection_probability=str(
            conditional_final_probability
        ),
        exact_branch_probability=str(branch_probability),
        log2_branch_probability=log_probability,
        log2_expected_passive_samples=-log_probability,
        log2_generic_amplitude_amplification_iterations=-log_probability / 2,
        exact_universal_probability_upper_bound=str(universal_upper_bound),
        probability_upper_bound_verified=upper_verified,
        polynomial_n8_budget_expected_hits=expected_n8_hits,
        natural_input_polynomial_accessible=False,
        status="stable-branch-superpolynomially-rare-quarantine-as-mechanism-control",
    )


def _threshold_crossings(
    maximum_n: int = 96,
    exponents: Sequence[int] = (2, 4, 8, 16),
) -> dict[str, dict[str, int | None]]:
    crossings: dict[str, dict[str, int | None]] = {}
    for family_index, family in enumerate(
        ("partial_matching_t_floor_n_over_4", "dense_matching_t_floor_n_over_2")
    ):
        rows: dict[str, int | None] = {}
        for exponent in exponents:
            crossing = None
            for n in range(8, maximum_n + 1):
                transpositions = n // 4 if family_index == 0 else n // 2
                record = audit_stable_branch_accessibility(
                    n, transpositions, family
                )
                if Fraction(record.exact_branch_probability) < Fraction(1, n**exponent):
                    crossing = n
                    break
            rows[f"below_n_to_minus_{exponent}"] = crossing
        crossings[family] = rows
    return crossings


@lru_cache(maxsize=1)
def build_stable_branch_accessibility_report(
    n_values: tuple[int, ...] = (8, 9, 10, 12, 16, 20, 24, 32),
) -> StableBranchAccessibilityReport:
    records = [
        audit_stable_branch_accessibility(n, transpositions, family)
        for n in n_values
        for family, transpositions in _family_specs(n)
    ]
    crossings = _threshold_crossings()
    metrics: dict[str, int | float] = {
        "accessibility_record_count": len(records),
        "exact_branch_probability_identity_count": len(records),
        "universal_probability_upper_bound_verified_count": sum(
            record.probability_upper_bound_verified for record in records
        ),
        "asymptotic_superpolynomial_rarity_theorem_count": 1,
        "natural_input_polynomial_accessible_branch_count": sum(
            record.natural_input_polynomial_accessible for record in records
        ),
        "maximum_n": max(n_values),
        "minimum_log2_branch_probability": min(
            record.log2_branch_probability for record in records
        ),
        "maximum_log2_generic_amplitude_amplification_iterations": max(
            record.log2_generic_amplitude_amplification_iterations
            for record in records
        ),
        "direct_conditioned_state_preparation_count": 0,
        "typical_irrep_transfer_theorem_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableBranchAccessibilityReport(
        created_at=utc_now(),
        probability_theorem={
            "exact_identity": "p[W_n,W_n,W_n,final xi_n]=d_W^3*d_xi*Tr(F)/(n!)^3",
            "weak_label_factorization": (
                "p_W=[d_W^2/n!]*(1+r_W); conditional final probability="
                "d_xi*Tr(F)/[d_W*(1+r_W)]^3"
            ),
            "dimensions": "d_W=n(n-3)/2; d_xi=n(n-2)(n-4)/3",
            "stable_multiplicity_sum": 25,
            "frame_trace": (
                "Tr(F)=25*(1+3*r_W+r_xi)+3*sum_eta g(W,W,eta)g(eta,W,xi)*r_eta"
            ),
            "hidden_element_independence": (
                "The branch probability depends only on the public involution conjugacy class, not the hidden class element."
            ),
        },
        asymptotic_no_go={
            "character_ratio_bound": "abs(r_eta)<=1 for every unitary irreducible representation",
            "frame_trace_bound": "0<Tr(F)<=25*5+3*25=200",
            "dimension_bound": "d_W^3*d_xi<=n^9/24",
            "probability_bound": "p_branch<=(25/3)*n^9/(n!)^3",
            "stirling_bound": "p_branch<=(25/3)*n^9*(e/n)^(3n)",
            "consequence": (
                "For every fixed c, n^c*p_branch tends to zero. Passive postselection costs 1/p and generic "
                "amplitude amplification costs Theta(1/sqrt(p)), both superpolynomial."
            ),
            "scope": (
                "This blocks the fixed low-dimensional stable branch under natural coset-state preparation. It does "
                "not rule out a new direct conditioned-state oracle or transfer to typical high-dimensional labels."
            ),
        },
        records=records,
        threshold_crossings=crossings,
        headline_metrics=metrics,
        claim_gate={
            "stable_branch_internal_filter_polynomial": True,
            "stable_branch_natural_input_access_polynomial": False,
            "stable_branch_viable_algorithmic_route": False,
            "stable_branch_useful_as_mechanism_control": True,
            "direct_conditioned_state_preparation_proved": False,
            "typical_irrep_transfer_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The solved W_n^tensor3/final-xi_n branch has probability exp(-Theta(n log n)) under natural coset-state "
                "preparation. Polynomial operations inside a superpolynomially rare branch do not yield a polynomial algorithm."
            ),
        },
        status="stable-low-dimensional-branch-inaccessible-pivot-to-typical-irreps",
        summary=(
            f"Proved exact natural-input probabilities for {len(records)} stable-branch rows and the universal bound "
            "p<=(25/3)n^9/(n!)^3. The fixed W_n^tensor3 branch is quarantined as a mechanism control; the next route "
            "must transfer its algebra to typical high-dimensional irreps or supply a new direct preparation theorem."
        ),
        falsifiers_triggered=[
            "Polynomial conditioning and inverse filtering inside the stable branch do not make the branch polynomially reachable.",
            "Low-dimensional stable Fourier labels have factorially small natural mass.",
            "Generic amplitude amplification only square-roots the inaccessible postselection cost and remains superpolynomial.",
            "Finite stable-branch spectra cannot be used as direct algorithmic evidence without branch-probability accounting.",
        ],
    )


def write_stable_branch_accessibility_report(
    output_path: Path = COSET_STABLE_BRANCH_ACCESSIBILITY_PATH,
    n_values: tuple[int, ...] = (8, 9, 10, 12, 16, 20, 24, 32),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_branch_accessibility_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-STABLE-W3-BRANCH-NATURAL-INPUT-POSTSELECTION",
                source=str(output_path),
                claim=(
                    "The polynomial stable W_n^tensor3 frame filter is directly usable on natural symmetric-group involution coset states."
                ),
                reason_invalid=(
                    "The exact source/final branch probability is d_W^3*d_xi*Tr(F)/(n!)^3 and is bounded by "
                    "(25/3)n^9/(n!)^3, so postselection and generic amplitude amplification are superpolynomial."
                ),
                lesson=(
                    "Keep the stable branch only as a proof/mechanism control. Transfer the construction to typical "
                    "high-dimensional Plancherel labels or prove a new direct conditioned-state preparation route."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"coset_stable_branch_accessibility": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_branch_accessibility_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
