"""A near-maximal-dimension trim removes all misleading information tails.

Let ``P_n`` be the physical six-label Racah law and ``Q_n`` the product of six
Plancherel laws on ``Irrep(S_n)``.  Every coordinate marginal of both laws is
exactly Plancherel.  If ``p(n)`` is the partition number and

    E_D = {at least one of the six irrep dimensions is at most D},

then atom counting gives, under either law,

    P_n(E_D), Q_n(E_D) <= delta_D := 6 p(n) D^2 / n!.     (1)

The total-variation contribution of this event is at most ``delta_D``.  More
importantly, its positive KL contribution is also controlled.  Every label
tuple has ``Q_n(x)>=|S_n|^-6`` and ``P_n(x)<=1``, so its likelihood ratio is
at most ``|S_n|^6``.  Therefore

    sum_(x in E_D) P_n(x) [log2(P_n(x)/Q_n(x))]_+
      <= 6 delta_D log2(n!).                              (2)

Choose the canonical threshold

    D_n = floor(sqrt(n!) / (p(n) log2(n!))).              (3)

Then ``delta_D<=6/[p(n) log2(n!)^2]`` and the right side of (2) is at most
``36/[p(n) log2(n!)]``, both tending to zero.  Thus no polynomial-dimensional,
subexponential-dimensional, or indeed any sector below this near-maximal
threshold can carry nonvanishing TV or KL information.  The trivial/sign
parity spike is a special case.

This theorem does not show that the retained high-dimensional bulk is flat.
It changes the research target: estimate dimension-trimmed TV/KL or
source/final-conditioned mutual information on the event that all six Specht
dimensions exceed (3).  Any surviving signal there cannot be dismissed as a
low-dimensional likelihood tail and becomes a legitimate structured-
recoupling target, subject to classical baselines and coherent-access costs.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_tetrahedral_dimension_trim.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TETRAHEDRAL-DIMENSION-TRIM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TetrahedralDimensionTrimRecord:
    n: int
    partition_count: int
    group_order_log2: float
    canonical_dimension_threshold_decimal: str
    canonical_dimension_threshold_log2: float
    canonical_relative_dimension_threshold_log2: float
    one_coordinate_low_dimension_mass_upper_bound: float
    six_coordinate_removed_mass_upper_bound: float
    removed_total_variation_contribution_upper_bound: float
    removed_positive_kl_contribution_upper_bound_bits: float
    retained_physical_mass_lower_bound: float
    retained_product_mass_lower_bound: float
    low_dimension_tail_tv_vanishing_certified: bool
    low_dimension_tail_positive_kl_vanishing_certified: bool
    status: str


@dataclass(frozen=True)
class TetrahedralDimensionTrimReport:
    created_at: str
    theorem_contract: dict[str, Any]
    scaling_records: list[TetrahedralDimensionTrimRecord]
    asymptotic_proof: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def canonical_dimension_threshold(n: int) -> int:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    partitions = len(integer_partitions(n))
    log2_order = math.lgamma(n + 1) / math.log(2)
    return max(1, math.isqrt(order) // max(1, math.ceil(partitions * log2_order)))


def tetrahedral_dimension_trim_record(n: int) -> TetrahedralDimensionTrimRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    partition_count = len(integer_partitions(n))
    log2_order = math.lgamma(n + 1) / math.log(2)
    threshold = canonical_dimension_threshold(n)
    one_coordinate = min(1.0, partition_count * threshold**2 / order)
    removed = min(1.0, 6.0 * one_coordinate)
    positive_kl = 6.0 * removed * log2_order
    asymptotic_tv = 6.0 / (partition_count * log2_order**2)
    asymptotic_kl = 36.0 / (partition_count * log2_order)
    return TetrahedralDimensionTrimRecord(
        n=n,
        partition_count=partition_count,
        group_order_log2=log2_order,
        canonical_dimension_threshold_decimal=str(threshold),
        canonical_dimension_threshold_log2=math.log2(threshold),
        canonical_relative_dimension_threshold_log2=(
            math.log2(threshold) - 0.5 * log2_order
        ),
        one_coordinate_low_dimension_mass_upper_bound=one_coordinate,
        six_coordinate_removed_mass_upper_bound=removed,
        removed_total_variation_contribution_upper_bound=removed,
        removed_positive_kl_contribution_upper_bound_bits=positive_kl,
        retained_physical_mass_lower_bound=max(0.0, 1.0 - removed),
        retained_product_mass_lower_bound=max(0.0, 1.0 - removed),
        low_dimension_tail_tv_vanishing_certified=(
            removed <= asymptotic_tv * (1 + 1e-12)
        ),
        low_dimension_tail_positive_kl_vanishing_certified=(
            positive_kl <= asymptotic_kl * (1 + 1e-12)
        ),
        status="near-maximal-dimension-tail-tv-kl-bound-certified",
    )


def run_tetrahedral_dimension_trim() -> TetrahedralDimensionTrimReport:
    rows = [
        tetrahedral_dimension_trim_record(n)
        for n in (10, 12, 16, 20, 24, 30, 40, 50)
    ]
    verified = all(
        row.low_dimension_tail_tv_vanishing_certified
        and row.low_dimension_tail_positive_kl_vanishing_certified
        for row in rows
    )
    tail = rows[-1]
    return TetrahedralDimensionTrimReport(
        created_at=utc_now(),
        theorem_contract={
            "shared_marginals": (
                "Every physical and product coordinate marginal is exactly Plancherel."
            ),
            "low_dimension_atom_count": (
                "For one coordinate, Pr[d_lambda<=D]<=p(n)D^2/n!."
            ),
            "six_coordinate_union": (
                "The event that any of six dimensions is at most D has physical "
                "and product mass at most delta_D=6p(n)D^2/n!."
            ),
            "tail_total_variation": (
                "The total-variation contribution on the removed event is at most delta_D."
            ),
            "tail_positive_kl": (
                "Its positive KL contribution is at most 6 delta_D log2(n!)."
            ),
            "canonical_threshold": (
                "D_n=floor(sqrt(n!)/(p(n)log2(n!)))."
            ),
            "canonical_consequence": (
                "Removed TV<=6/[p(n)log2(n!)^2] and removed positive "
                "KL<=36/[p(n)log2(n!)], both o(1)."
            ),
            "scope": (
                "No TV/KL estimate is proved on the retained high-dimensional bulk."
            ),
        },
        scaling_records=rows,
        asymptotic_proof={
            "plancherel_atom": "q_lambda=d_lambda^2/n!",
            "number_of_irreps": "p(n)",
            "physical_marginals_equal_plancherel": True,
            "minimum_product_atom": "Q(x)>=1/(n!)^6",
            "maximum_likelihood_ratio": "P(x)/Q(x)<=(n!)^6",
            "removed_tv_bound": "6p(n)D_n^2/n!<=6/[p(n)log2(n!)^2]",
            "removed_positive_kl_bound": "<=36/[p(n)log2(n!)]",
            "removed_mass_tends_to_zero": True,
            "removed_positive_kl_tends_to_zero": True,
        },
        proof_obligations=[
            {
                "obligation": "remove_low_dimension_chi_square_tails_without_losing_tv_or_kl",
                "resolved": True,
                "resolution": (
                    "Exact Plancherel marginals, atom counting, and the finite-space "
                    "likelihood ceiling give vanishing TV and positive-KL tail bounds."
                ),
            },
            {
                "obligation": "bound_retained_high_dimension_tetrahedral_tv",
                "resolved": False,
                "resolution": (
                    "Requires a typical-shape character/word-map estimate or a "
                    "positive-mass counterfamily after the canonical trim."
                ),
            },
            {
                "obligation": "bound_retained_source_final_conditioned_mutual_information",
                "resolved": False,
                "resolution": (
                    "The trim prevents rare-label false positives but does not "
                    "control conditional Racah channel structure."
                ),
            },
            {
                "obligation": "test_classical_access_to_any_retained_signal",
                "resolved": False,
                "resolution": (
                    "Any retained signal must be compared with character-table, "
                    "Kronecker-support, and random-permutation word-map baselines."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The threshold removes most Plancherel mass because it is near sqrt(n!).",
                "resolved": True,
                "resolution": (
                    "Irrespective of the dimension distribution, atom counting "
                    "bounds removed mass by 6/[p(n)log2(n!)^2]=o(1)."
                ),
            },
            {
                "objection": "Tiny mass may still carry constant KL through huge likelihood.",
                "resolved": True,
                "resolution": (
                    "The universal likelihood ceiling (n!)^6 makes its positive "
                    "KL contribution at most 36/[p(n)log2(n!)]."
                ),
            },
            {
                "objection": "Vanishing removed mass proves the retained law is product.",
                "resolved": False,
                "resolution": (
                    "It only makes retained-bulk TV/KL the faithful decision problem."
                ),
            },
            {
                "objection": "This trim provides an efficient coherent projector.",
                "resolved": False,
                "resolution": (
                    "The theorem is information-theoretic; coherent dimension "
                    "comparison and downstream recoupling compilation are separate."
                ),
            },
        ],
        headline_metrics={
            "dimension_trim_tail_theorem_count": 1,
            "tail_total_variation_bound_theorem_count": 1,
            "tail_positive_kl_bound_theorem_count": 1,
            "scaling_record_count": len(rows),
            "maximum_scaling_n": tail.n,
            "n50_dimension_threshold_log2": tail.canonical_dimension_threshold_log2,
            "n50_removed_mass_upper_bound": tail.six_coordinate_removed_mass_upper_bound,
            "n50_removed_positive_kl_upper_bound_bits": (
                tail.removed_positive_kl_contribution_upper_bound_bits
            ),
            "retained_bulk_tv_kl_theorem_count": 0,
            "positive_mass_measured_signal_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "near_maximal_dimension_trim_has_vanishing_physical_mass_cost_proved": verified,
            "removed_tail_total_variation_contribution_vanishes_proved": verified,
            "removed_tail_positive_kl_contribution_vanishes_proved": verified,
            "trivial_sign_parity_tail_removed": verified,
            "retained_high_dimension_total_variation_vanishes_proved": False,
            "retained_high_dimension_total_variation_survives_proved": False,
            "retained_high_dimension_conditional_information_survives_proved": False,
            "efficient_coherent_trim_compiled": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All low-dimensional likelihood tails are information-negligible, "
                "but the near-maximal-dimensional tetrahedral bulk is unresolved."
            ),
        },
        status=(
            "low-dimension-information-tails-removed-retained-bulk-open"
            if verified
            else "tetrahedral-dimension-trim-control-failure"
        ),
        summary=(
            "Proved that a near-maximal-dimension trim removes vanishing physical "
            "mass and vanishing TV/KL contribution, making the retained bulk the "
            "only valid measured-recoupling search space."
        ),
        falsifiers_triggered=[
            "Factorially large likelihood cannot rescue sectors below the canonical dimension threshold in TV or KL.",
            "The trivial/sign parity witness is excluded at vanishing information cost.",
            "Any claimed measured-label signal must now be demonstrated on the retained near-maximal-dimensional bulk.",
        ],
    )


def write_tetrahedral_dimension_trim_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_tetrahedral_dimension_trim())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_tetrahedral_dimension_trim_report()
    print(json.dumps(report, indent=2))
