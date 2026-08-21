"""Plancherel 6j spectra approach the quantum-marginal compatibility set.

For a partition ``rho`` of ``n``, let

    s(rho) = (rho_1/n, rho_2/n, ...)

be its normalized row spectrum.  The Logan--Shepp--Vershik--Kerov limit-shape
theorem implies that a Plancherel-random Young diagram converges in normalized
area to one deterministic shape.  For left-justified diagrams,

    ||s(rho)-s(sigma)||_1
      = |Young(rho) symmetric_difference Young(sigma)| / n.          (1)

Thus any fixed number of labels with Plancherel marginals have spectra that
are all ``o(1)`` apart in ``L1``, without requiring independence.

This has an exact quantum-marginal consequence.  For every probability vector
``r``, the classical diagonal tripartite state

    omega_ABC = sum_i r_i |iii><iii|                             (2)

has spectrum ``r`` on each of ``A,B,C,AB,BC,ABC`` (with zero padding).
Therefore the six spectra of a physical symmetric-group 6j block lie at
``o(1)`` distance from the compatible marginal set with probability tending
to one.  The physical trace-mass law is used only to supply exact Plancherel
marginals for all six edge labels.

This closes the constant-incompatibility-gap route to typical exponential
recoupling suppression.  It does not prove that the recoupling coefficient is
large: a shrinking distance ``D_n`` can still have ``n D_n^2 -> infinity``,
the published theorem has fixed local dimension, and coherent generalized
3nj networks involve a growing number of correlated labels.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_marginal_compatibility_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-MARGINAL-COMPATIBILITY-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
VKLS_SOURCE_URL = (
    "https://www.mathnet.ru/eng/dan40430"
)
RECOUPLING_SOURCE_URL = "https://arxiv.org/abs/1210.0463"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PlancherelSpectrumDistanceRecord:
    n: int
    partition_count: int
    expected_two_sample_l1_distance: float
    expected_two_sample_l1_distance_log2: float
    status: str


@dataclass(frozen=True)
class PlancherelMarginalCompatibilityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_distance_records: list[PlancherelSpectrumDistanceRecord]
    asymptotic_proof: dict[str, str | bool]
    literature_links: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def normalized_row_spectrum(partition: Partition) -> tuple[float, ...]:
    n = sum(partition)
    if n < 1:
        raise ValueError("partition must be nonempty")
    return tuple(part / n for part in partition)


def row_spectrum_l1(left: Partition, right: Partition) -> float:
    if sum(left) != sum(right):
        raise ValueError("partitions must have the same degree")
    n = sum(left)
    width = max(len(left), len(right))
    return sum(
        abs(
            (left[index] if index < len(left) else 0)
            - (right[index] if index < len(right) else 0)
        )
        for index in range(width)
    ) / n


def expected_plancherel_pair_l1(n: int) -> float:
    """Compute the exact-law expectation using row-coordinate marginals."""

    if n < 1:
        raise ValueError("n must be positive")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    weighted = tuple(
        (partition, hook_length_dimension(partition) ** 2 / order)
        for partition in partitions
    )
    expectation = 0.0
    for index in range(n):
        coordinate_law: dict[int, float] = defaultdict(float)
        for partition, probability in weighted:
            value = partition[index] if index < len(partition) else 0
            coordinate_law[value] += probability

        prefix_probability = 0.0
        prefix_first_moment = 0.0
        coordinate_expectation = 0.0
        for value, probability in sorted(coordinate_law.items()):
            coordinate_expectation += 2.0 * probability * (
                value * prefix_probability - prefix_first_moment
            )
            prefix_probability += probability
            prefix_first_moment += value * probability
        expectation += coordinate_expectation / n
    return expectation


def spectrum_distance_record(n: int) -> PlancherelSpectrumDistanceRecord:
    value = expected_plancherel_pair_l1(n)
    return PlancherelSpectrumDistanceRecord(
        n=n,
        partition_count=len(integer_partitions(n)),
        expected_two_sample_l1_distance=value,
        expected_two_sample_l1_distance_log2=math.log2(value),
        status="finite-plancherel-spectrum-concentration-control",
    )


def run_plancherel_marginal_compatibility_no_go(
) -> PlancherelMarginalCompatibilityReport:
    rows = [spectrum_distance_record(n) for n in (4, 6, 8, 12, 16, 20, 24, 30)]
    decreasing = all(
        current.expected_two_sample_l1_distance
        < previous.expected_two_sample_l1_distance
        for previous, current in zip(rows, rows[1:])
    )
    tail = rows[-1]
    return PlancherelMarginalCompatibilityReport(
        created_at=utc_now(),
        theorem_contract={
            "row_area_identity": (
                "||rho/n-sigma/n||_1 equals normalized area of the symmetric "
                "difference of their left-justified Young diagrams."
            ),
            "plancherel_limit_shape": (
                "VKLS normalized-area convergence implies that any fixed number "
                "of labels with Plancherel marginals are mutually o(1) in L1."
            ),
            "diagonal_compatibility_witness": (
                "omega_ABC=sum_i r_i |iii><iii| has spectrum r on "
                "A,B,C,AB,BC,ABC."
            ),
            "physical_transfer": (
                "The physical 6j trace-mass law gives exact Plancherel marginals "
                "for alpha,beta,gamma,mu,nu,lambda; dependence is harmless for a "
                "fixed six-label union bound."
            ),
            "conclusion": (
                "The L1 distance D_n from a physical six-spectrum tuple to the "
                "tripartite quantum-marginal compatibility set tends to zero in probability."
            ),
            "scope": (
                "No rate for D_n, recoupling norm lower bound, growing-row converse, "
                "or growing-size generalized 3nj compatibility theorem is claimed."
            ),
        },
        finite_distance_records=rows,
        asymptotic_proof={
            "external_limit_shape_input": (
                "Plancherel Young diagrams converge in normalized area to the VKLS shape."
            ),
            "l1_equals_normalized_symmetric_difference_area": True,
            "fixed_six_label_union_requires_independence": False,
            "diagonal_tripartite_state_is_compatible": True,
            "physical_six_spectrum_distance_to_compatibility_tends_to_zero": True,
            "constant_positive_incompatibility_gap_on_positive_mass": False,
        },
        literature_links=[
            {
                "paper_id": "vershik-kerov-1977-limit-shape",
                "title": (
                    "Asymptotics of the Plancherel measure of the symmetric group "
                    "and the limiting form of Young tableaux"
                ),
                "url": VKLS_SOURCE_URL,
                "use": "Plancherel normalized Young-diagram limit shape.",
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "christandl-sahinoglu-walter-2016",
                "title": "Recoupling coefficients and quantum entropies",
                "url": RECOUPLING_SOURCE_URL,
                "use": (
                    "Tripartite marginal interpretation and L1 incompatibility "
                    "distance in the recoupling suppression theorem."
                ),
                "external_theorem_not_reproved_here": True,
            },
        ],
        proof_obligations=[
            {
                "obligation": "classify_natural_six_spectrum_marginal_distance",
                "resolved": True,
                "resolution": (
                    "It converges to zero under physical trace mass by VKLS and "
                    "the diagonal-state compatibility witness."
                ),
            },
            {
                "obligation": "derive_marginal_distance_rate",
                "resolved": False,
                "resolution": (
                    "A rate is needed to decide whether n D_n^2 can still diverge."
                ),
            },
            {
                "obligation": "dimension_growing_compatible_recoupling_lower_bound",
                "resolved": False,
                "resolution": (
                    "The published polynomial lower branch assumes bounded local dimensions."
                ),
            },
            {
                "obligation": "growing_generalized_3nj_marginal_geometry",
                "resolved": False,
                "resolution": (
                    "A growing network has more than a fixed six labels and may not "
                    "inherit the same union-bound conclusion."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Six correlated labels cannot share a limit-shape conclusion.",
                "resolved": True,
                "resolution": (
                    "Each marginal is Plancherel and there are only six events, so "
                    "a union bound needs no independence."
                ),
            },
            {
                "objection": "Six nearly equal spectra need not be quantum-marginal compatible.",
                "resolved": True,
                "resolution": (
                    "They are near the explicit compatible diagonal tuple "
                    "(r,r,r,r,r,r)."
                ),
            },
            {
                "objection": "D_n=o(1) rules out every exponential or stretched-exponential suppression.",
                "resolved": False,
                "resolution": (
                    "False. A shrinking D_n can still satisfy n D_n^2 -> infinity."
                ),
            },
            {
                "objection": "Near compatibility proves a large physical recoupling norm.",
                "resolved": False,
                "resolution": (
                    "The converse is fixed-dimensional and no dimension-uniform "
                    "lower bound is available."
                ),
            },
        ],
        headline_metrics={
            "plancherel_marginal_compatibility_no_go_theorem_count": 1,
            "finite_distance_record_count": len(rows),
            "finite_expected_distance_strictly_decreasing": int(decreasing),
            "tail_n": tail.n,
            "tail_expected_two_sample_l1_distance": (
                tail.expected_two_sample_l1_distance
            ),
            "marginal_distance_rate_theorem_count": 0,
            "dimension_growing_recoupling_lower_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_six_spectra_approach_compatibility_proved": True,
            "constant_incompatibility_gap_on_positive_physical_mass_possible": False,
            "marginal_distance_rate_proved": False,
            "typical_recoupling_norm_lower_bound_proved": False,
            "typical_recoupling_contraction_proved": False,
            "coherent_generalized_3nj_contraction_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Typical physical spectra are asymptotically near compatible, but "
                "neither the shrinking-gap rate nor the true growing-row norm is controlled."
            ),
        },
        status="constant-marginal-incompatibility-route-closed-shrinking-gap-open",
        summary=(
            "Proved that physical Plancherel 6j spectra approach the tripartite "
            "quantum-marginal compatibility set, closing constant-gap suppression."
        ),
        falsifiers_triggered=[
            "Typical physical Plancherel spectra cannot remain a constant L1 distance outside compatibility.",
            "Near compatibility is not a growing-row lower bound on recoupling coefficients.",
            "A shrinking incompatibility gap may still create weaker suppression and requires a rate theorem.",
        ],
    )


def write_plancherel_marginal_compatibility_no_go_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_plancherel_marginal_compatibility_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> int:
    payload = write_plancherel_marginal_compatibility_no_go_report()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
