"""A surviving 6j channel signal requires factorial non-Haar enhancement.

For fixed source and final labels, let a real orthogonal recoupling matrix of
dimension ``M`` be blocked into ``a`` left channels of ranks ``L_i`` and ``b``
right channels of ranks ``R_j``.  If the relative basis is Haar orthogonal,
the standard random-Grassmann second moment gives

    E chi^2(channel_joint || channel_product)
      = 2(a-1)(b-1)/((M-1)(M+2)).                         (1)

The natural physical source/final law supplies a much stronger scale for
``M``.  Let ``alpha,beta,gamma`` be independent Plancherel sources and sample
``lambda`` by its dimension-weighted multiplicity in their tensor product.
Relative to four independent Plancherel labels, this law has density

    Y = |S_n| M/(d_alpha d_beta d_gamma d_lambda).         (2)

Character orthogonality gives ``E[(Y-1)^2]=V4_n``, where

    V4_n = sum_(nonidentity conjugacy classes C) 1/|C|^2. (3)

Under the size-biased physical law, ``Pr[Y<1/2] <= 2 V4_n``.  Each individual
label remains Plancherel.  Atom counting with ``delta=1/n`` therefore gives,
outside physical mass at most ``4/n+2V4_n``,

    M >= n!/(2 n^2 p(n)^2).                               (4)

There are at most ``p(n)`` intermediate channel labels per tree.  Combining
(1) and (4), the orthogonal-Haar chi-square benchmark is at most

    H_n = 8 n^4 p(n)^6/(n!)^2.                            (5)

This vanishes on a factorial scale.  Consequently, if the actual recoupling
chi-square is at most ``A_n H_n`` on the good physical mass for any
``A_n=exp(o(n log n))``, then channel total variation and mutual information
vanish.  Conversely, a nonvanishing measured-label signal requires
``exp(Omega(n log n))`` enhancement over Haar on positive physical mass.

Equation (5) is a conditional reduction, not a claim that symmetric-group
recoupling is Haar.  Arithmetic associators can be highly nonrandom.  The
remaining theorem target is exactly the source-weighted enhancement factor.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_plancherel_kronecker_positivity import centralizer_order
from self_dual_wreath_plancherel_recoupling_rank_pressure_no_go import (
    partition_number,
)
from self_dual_wreath_recoupling_channel_flatness_boundary import (
    audit_complete_s6_channel_information,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_recoupling_haar_gap_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-HAAR-GAP-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FiniteHaarGapControl:
    final_partition: tuple[int, ...]
    total_multiplicity: int
    left_channel_count: int
    right_channel_count: int
    observed_chi_square: float
    orthogonal_haar_expected_chi_square: float
    observed_to_orthogonal_haar_ratio: float
    observed_total_variation: float
    status: str


@dataclass(frozen=True)
class PhysicalHaarGapScalingRecord:
    n: int
    partition_count: int
    four_label_variance: float
    good_physical_mass_lower_bound: float
    multiplicity_lower_bound_log2: float
    orthogonal_haar_chi_square_upper_log2: float
    inverse_haar_chi_square_lower_log2: float
    status: str


@dataclass(frozen=True)
class RecouplingHaarGapReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FiniteHaarGapControl]
    scaling_records: list[PhysicalHaarGapScalingRecord]
    asymptotic_proof: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def four_label_variance(n: int) -> float:
    if n < 2:
        raise ValueError("n must be at least two")
    order = math.factorial(n)
    identity = (1,) * n
    return sum(
        (centralizer_order(cycle_type) / order) ** 2
        for cycle_type in integer_partitions(n)
        if cycle_type != identity
    )


def orthogonal_haar_expected_chi_square(
    total_multiplicity: int,
    left_channel_count: int,
    right_channel_count: int,
) -> float:
    if total_multiplicity < 1:
        raise ValueError("total multiplicity must be positive")
    if not 1 <= left_channel_count <= total_multiplicity:
        raise ValueError("invalid left channel count")
    if not 1 <= right_channel_count <= total_multiplicity:
        raise ValueError("invalid right channel count")
    if total_multiplicity == 1:
        return 0.0
    return (
        2.0
        * (left_channel_count - 1)
        * (right_channel_count - 1)
        / ((total_multiplicity - 1) * (total_multiplicity + 2))
    )


def complex_haar_expected_chi_square(
    total_multiplicity: int,
    left_channel_count: int,
    right_channel_count: int,
) -> float:
    if total_multiplicity < 1:
        raise ValueError("total multiplicity must be positive")
    if not 1 <= left_channel_count <= total_multiplicity:
        raise ValueError("invalid left channel count")
    if not 1 <= right_channel_count <= total_multiplicity:
        raise ValueError("invalid right channel count")
    if total_multiplicity == 1:
        return 0.0
    return (
        (left_channel_count - 1)
        * (right_channel_count - 1)
        / (total_multiplicity * total_multiplicity - 1)
    )


def audit_complete_s6_haar_gap() -> list[FiniteHaarGapControl]:
    rows = audit_complete_s6_channel_information()
    controls = []
    for row in rows:
        channels = row.channel_count
        haar = orthogonal_haar_expected_chi_square(
            row.total_multiplicity,
            channels,
            channels,
        )
        ratio = row.chi_square_from_channel_independence / haar if haar else 0.0
        controls.append(
            FiniteHaarGapControl(
                final_partition=row.final_partition,
                total_multiplicity=row.total_multiplicity,
                left_channel_count=channels,
                right_channel_count=channels,
                observed_chi_square=row.chi_square_from_channel_independence,
                orthogonal_haar_expected_chi_square=haar,
                observed_to_orthogonal_haar_ratio=ratio,
                observed_total_variation=row.total_variation_from_channel_independence,
                status=(
                    "finite-observed-chi-below-orthogonal-haar-mean"
                    if row.chi_square_from_channel_independence <= haar + 1e-10
                    else "finite-observed-chi-above-orthogonal-haar-mean"
                ),
            )
        )
    return controls


def physical_haar_gap_scaling_record(n: int) -> PhysicalHaarGapScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    count = partition_number(n)
    variance = four_label_variance(n)
    good_mass = max(0.0, 1.0 - 4.0 / n - 2.0 * variance)
    log2_order = math.lgamma(n + 1) / math.log(2)
    multiplicity_log2 = (
        log2_order - 1.0 - 2.0 * math.log2(n) - 2.0 * math.log2(count)
    )
    haar_log2 = (
        3.0
        + 4.0 * math.log2(n)
        + 6.0 * math.log2(count)
        - 2.0 * log2_order
    )
    return PhysicalHaarGapScalingRecord(
        n=n,
        partition_count=count,
        four_label_variance=variance,
        good_physical_mass_lower_bound=good_mass,
        multiplicity_lower_bound_log2=multiplicity_log2,
        orthogonal_haar_chi_square_upper_log2=haar_log2,
        inverse_haar_chi_square_lower_log2=-haar_log2,
        status=(
            "factorial-haar-channel-flatness-benchmark"
            if multiplicity_log2 > 0 and haar_log2 < 0
            else "finite-n-haar-gap-not-yet-separated"
        ),
    )


def run_recoupling_haar_gap_reduction() -> RecouplingHaarGapReductionReport:
    controls = audit_complete_s6_haar_gap()
    rows = [
        physical_haar_gap_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 30, 40, 50)
    ]
    finite_below = sum(
        row.observed_chi_square
        <= row.orthogonal_haar_expected_chi_square + 1e-10
        for row in controls
    )
    tail = rows[-1]
    return RecouplingHaarGapReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "orthogonal_haar_second_moment": (
                "For block ranks L_i,R_j summing to M, Haar orthogonal mixing "
                "gives E chi^2=2(a-1)(b-1)/((M-1)(M+2))."
            ),
            "physical_source_final_density": (
                "Relative to four independent Plancherel labels, the physical "
                "source/final law has density Y=n! M/(d_alpha d_beta d_gamma d_lambda)."
            ),
            "four_label_variance": (
                "E[(Y-1)^2]=V4_n=sum_(C!=1)1/|C|^2."
            ),
            "multiplicity_lower_bound": (
                "Outside physical mass 4/n+2V4_n, M>=n!/(2n^2p(n)^2)."
            ),
            "haar_gap": (
                "With at most p(n) channels per tree, Haar E chi^2 is at most "
                "8n^4p(n)^6/(n!)^2."
            ),
            "conditional_consequence": (
                "Any exp(o(n log n)) enhancement over Haar still forces measured "
                "channel TV and mutual information to vanish."
            ),
            "scope": (
                "No Haar universality or enhancement bound for natural symmetric-group "
                "recoupling is proved."
            ),
        },
        finite_controls=controls,
        scaling_records=rows,
        asymptotic_proof={
            "physical_bad_mass_upper": "4/n+2V4_n=o(1)",
            "physical_multiplicity_lower": "n!/(2n^2p(n)^2)",
            "channel_count_upper_each_tree": "p(n)",
            "orthogonal_haar_chi_upper": "8n^4p(n)^6/(n!)^2",
            "haar_chi_log_scale": "-2n log n+O(n)",
            "subfactorial_enhancement_definition": "log A_n=o(n log n)",
            "subfactorial_enhancement_implies_channel_independence": True,
            "nonvanishing_signal_requires_factorial_enhancement": True,
        },
        proof_obligations=[
            {
                "obligation": "bound_natural_recoupling_haar_enhancement",
                "resolved": False,
                "resolution": (
                    "Prove chi^2_actual/chi^2_Haar=exp(o(n log n)) on positive "
                    "physical mass, or construct a factorially enhanced outlier family."
                ),
            },
            {
                "obligation": "source_weighted_channel_mutual_information",
                "resolved": False,
                "resolution": (
                    "The conditional reduction decides it once the enhancement factor is controlled."
                ),
            },
            {
                "obligation": "coherent_phase_observable_after_label_flatness",
                "resolved": False,
                "resolution": (
                    "Vanishing measured-label information would leave phase-sensitive "
                    "multiplicity observables as the only recoupling route."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Typical final multiplicity may be small despite large Specht dimensions.",
                "resolved": True,
                "resolution": (
                    "The exact four-label normalized multiplicity variance and physical "
                    "size bias give the factorial lower bound outside o(1) mass."
                ),
            },
            {
                "objection": "There may be factorially many channel labels.",
                "resolved": True,
                "resolution": (
                    "Intermediate labels are partitions of n, so each tree has at most p(n)=exp(O(sqrt n)) channels."
                ),
            },
            {
                "objection": "Finite S6 nonflatness contradicts the Haar-gap reduction.",
                "resolved": True,
                "resolution": (
                    "No: every complete S6 observed chi-square is below the corresponding "
                    "orthogonal-Haar mean, and no asymptotic universality is inferred."
                ),
            },
            {
                "objection": "Associators are generic random orthogonal matrices.",
                "resolved": False,
                "resolution": (
                    "Unproved and likely false pointwise; only a source-weighted fourth-moment bound is required."
                ),
            },
        ],
        headline_metrics={
            "orthogonal_haar_channel_chi_identity_count": 1,
            "physical_final_multiplicity_lower_bound_theorem_count": 1,
            "conditional_subfactorial_enhancement_reduction_count": 1,
            "complete_s6_control_count": len(controls),
            "complete_s6_observed_below_haar_mean_count": finite_below,
            "tail_n": tail.n,
            "tail_good_physical_mass_lower_bound": tail.good_physical_mass_lower_bound,
            "tail_multiplicity_lower_bound_log2": tail.multiplicity_lower_bound_log2,
            "tail_haar_chi_square_upper_log2": (
                tail.orthogonal_haar_chi_square_upper_log2
            ),
            "natural_enhancement_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_final_multiplicity_factorial_lower_bound_proved": True,
            "haar_channel_chi_factorially_small_proved": True,
            "subfactorial_enhancement_would_force_label_independence_proved": True,
            "natural_recoupling_subfactorial_enhancement_proved": False,
            "factorially_enhanced_outlier_family_constructed": False,
            "source_weighted_channel_mutual_information_vanishes_proved": False,
            "coherent_phase_route_dequantized": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The required non-Haar enhancement scale is now factorially sharp, "
                "but the actual symmetric-group 6j fourth moment remains open."
            ),
        },
        status="factorial-haar-gap-proved-natural-enhancement-open",
        summary=(
            "Proved that any surviving measured 6j channel signal requires "
            "factorial enhancement over orthogonal-Haar mixing on positive physical mass."
        ),
        falsifiers_triggered=[
            "Typical physical final multiplicity is not a low-rank escape.",
            "Subexponential channel count cannot offset factorial Haar mixing.",
            "A useful measured-label signal must exhibit factorially non-Haar arithmetic structure.",
        ],
    )


def write_recoupling_haar_gap_reduction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_recoupling_haar_gap_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> int:
    payload = write_recoupling_haar_gap_reduction_report()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
