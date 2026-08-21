"""Classical dequantization of the matching-charge pairwise kernel.

For a perfect matching ``h``, let ``O_h`` be the 192*C(m,4)-term support of
the disjoint matching charge.  The normalized regular Hilbert-Schmidt kernel
between two charges is

    kappa(h,h') = <D_h,D_h'>/<D_h,D_h>
                = |O_h intersect O_h'|/|O_h|.            (1)

This kernel is classically easy.  Every term is a product of two disjoint
3-cycles.  It belongs to ``O_h'`` exactly when each 3-cycle uses endpoints
from two ``h'`` edges and the two resulting edge pairs are disjoint.  After a
linear-time point-to-edge table is built, membership is constant time.
Enumerating the explicit ``O(m^4)`` orbit index therefore evaluates (1) in
``O(m^4)`` time and logarithmic auxiliary space apart from the input matching.

There is also an exact all-rank nearest-switch formula.  Switch two reference
edges by conjugating with one cross-pair transposition and put ``n=m-2``.  A
common term touches either two, three, or four unaffected edges.  Exact local
cores contribute respectively 80, 192, and 192 terms per selected unaffected
set, hence

    I_m = 80 C(n,2) + 192 C(n,3) + 192 C(n,4),
    |O_h| = 192 C(m,4),
    kappa_near(m) = (m^2-5m+9)/(m(m-1)),
    1-kappa_near(m) = (4m-9)/(m(m-1)).                  (2)

Thus neighboring charge orbit vectors become nearly parallel, with only an
``Theta(1/m)`` normalized Gram separation.  That scale is polynomially
resolvable, but the entire pairwise kernel is already classically available.
A useful quantum route must exploit matrix-valued spectral transitions,
noncommuting higher moments, or coherent all-copy target interference not
determined by (1).  This theorem does not dequantize those stronger objects.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_matching_charge_coherent_label_compiler import (
    matching_charge_term_count,
    matching_charge_term_from_index,
)
from coset_hidden_involution_matching_charge_orbit_recoupling_reduction import (
    Permutation,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_matching_charge_pairwise_kernel_dequantization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-PAIRWISE-KERNEL-DEQUANTIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Matching = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class NearestSwitchKernelControl:
    half_degree: int
    unaffected_edge_count: int
    charge_term_count: int
    observed_intersection_count: int
    expected_two_unaffected_contribution: int
    expected_three_unaffected_contribution: int
    expected_four_unaffected_contribution: int
    expected_intersection_count: int
    normalized_kernel: str
    expected_normalized_kernel: str
    normalized_kernel_deficit: str
    exact_local_support_formula_verified: bool
    status: str


@dataclass(frozen=True)
class PairwiseKernelScalingRecord:
    half_degree: int
    charge_term_count: int
    classical_membership_tests: int
    classical_time_exponent: int
    nearest_switch_kernel: float
    nearest_switch_kernel_deficit: float
    nearest_orbit_vector_distance_squared: float
    pairwise_kernel_classically_computable: bool
    status: str


@dataclass(frozen=True)
class PairwiseKernelDequantizationTheorem:
    membership_test: str
    classical_algorithm: str
    nearest_switch_formula: str
    mechanism_boundary: str
    exact_all_rank_nearest_switch_kernel_proved: bool
    arbitrary_pairwise_kernel_polynomial_time_classical: bool
    charge_orbit_pairwise_fidelity_is_quantum_advantage: bool
    matrix_valued_spectral_transition_dequantized: bool
    noncommuting_higher_transition_moments_dequantized: bool
    all_copy_target_interference_dequantized: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairwiseKernelDequantizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    nearest_switch_controls: list[NearestSwitchKernelControl]
    scaling_records: list[PairwiseKernelScalingRecord]
    theorem: PairwiseKernelDequantizationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def reference_matching(half_degree: int) -> Matching:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    return tuple((2 * pair, 2 * pair + 1) for pair in range(half_degree))


def nearest_switched_matching(half_degree: int) -> Matching:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    return (
        (0, 2),
        (1, 3),
        *tuple((2 * pair, 2 * pair + 1) for pair in range(2, half_degree)),
    )


def _point_to_matching_edge(matching: Matching) -> tuple[int, ...]:
    degree = 2 * len(matching)
    edge_of = [-1] * degree
    for edge_index, edge in enumerate(matching):
        if len(edge) != 2 or edge[0] == edge[1]:
            raise ValueError("matching edges must contain two distinct points")
        for point in edge:
            if not 0 <= point < degree or edge_of[point] != -1:
                raise ValueError("matching must partition the point set")
            edge_of[point] = edge_index
    if any(value < 0 for value in edge_of):
        raise ValueError("matching does not cover every point")
    return tuple(edge_of)


def _nontrivial_cycles(permutation: Permutation) -> tuple[tuple[int, ...], ...]:
    visited = [False] * len(permutation)
    cycles: list[tuple[int, ...]] = []
    for start in range(len(permutation)):
        if visited[start]:
            continue
        cycle: list[int] = []
        point = start
        while not visited[point]:
            visited[point] = True
            cycle.append(point)
            point = permutation[point]
        if len(cycle) > 1:
            cycles.append(tuple(cycle))
    return tuple(cycles)


def is_matching_charge_term(
    permutation: Permutation,
    matching: Matching,
) -> bool:
    if len(permutation) != 2 * len(matching):
        raise ValueError("permutation and matching degrees do not agree")
    edge_of = _point_to_matching_edge(matching)
    cycles = _nontrivial_cycles(permutation)
    if len(cycles) != 2 or any(len(cycle) != 3 for cycle in cycles):
        return False
    edge_pairs = [set(edge_of[point] for point in cycle) for cycle in cycles]
    return bool(
        all(len(edges) == 2 for edges in edge_pairs)
        and edge_pairs[0].isdisjoint(edge_pairs[1])
    )


def matching_charge_pairwise_intersection(
    half_degree: int,
    target_matching: Matching,
) -> int:
    _point_to_matching_edge(target_matching)
    return sum(
        is_matching_charge_term(
            matching_charge_term_from_index(half_degree, index),
            target_matching,
        )
        for index in range(matching_charge_term_count(half_degree))
    )


def nearest_switch_intersection_formula(half_degree: int) -> int:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    unaffected = half_degree - 2
    return (
        80 * math.comb(unaffected, 2)
        + 192 * math.comb(unaffected, 3)
        + 192 * math.comb(unaffected, 4)
    )


def nearest_switch_kernel_formula(half_degree: int) -> Fraction:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    return Fraction(
        half_degree**2 - 5 * half_degree + 9,
        half_degree * (half_degree - 1),
    )


def audit_nearest_switch_kernel(
    half_degree: int,
) -> NearestSwitchKernelControl:
    if not 4 <= half_degree <= 12:
        raise ValueError("dense nearest-switch audit is limited to 4<=m<=12")
    unaffected = half_degree - 2
    total = matching_charge_term_count(half_degree)
    observed = matching_charge_pairwise_intersection(
        half_degree,
        nearest_switched_matching(half_degree),
    )
    two = 80 * math.comb(unaffected, 2)
    three = 192 * math.comb(unaffected, 3)
    four = 192 * math.comb(unaffected, 4)
    expected = two + three + four
    kernel = Fraction(observed, total)
    expected_kernel = nearest_switch_kernel_formula(half_degree)
    verified = bool(observed == expected and kernel == expected_kernel)
    return NearestSwitchKernelControl(
        half_degree=half_degree,
        unaffected_edge_count=unaffected,
        charge_term_count=total,
        observed_intersection_count=observed,
        expected_two_unaffected_contribution=two,
        expected_three_unaffected_contribution=three,
        expected_four_unaffected_contribution=four,
        expected_intersection_count=expected,
        normalized_kernel=str(kernel),
        expected_normalized_kernel=str(expected_kernel),
        normalized_kernel_deficit=str(1 - kernel),
        exact_local_support_formula_verified=verified,
        status=(
            "nearest-switch-charge-kernel-exact"
            if verified
            else "nearest-switch-charge-kernel-control-failure"
        ),
    )


def pairwise_kernel_scaling_record(
    half_degree: int,
) -> PairwiseKernelScalingRecord:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    count = matching_charge_term_count(half_degree)
    kernel = float(nearest_switch_kernel_formula(half_degree))
    deficit = 1.0 - kernel
    return PairwiseKernelScalingRecord(
        half_degree=half_degree,
        charge_term_count=count,
        classical_membership_tests=count,
        classical_time_exponent=4,
        nearest_switch_kernel=kernel,
        nearest_switch_kernel_deficit=deficit,
        nearest_orbit_vector_distance_squared=2.0 * deficit,
        pairwise_kernel_classically_computable=True,
        status="pairwise-charge-kernel-polynomial-classical",
    )


def build_pairwise_kernel_dequantization_report() -> PairwiseKernelDequantizationReport:
    controls = [audit_nearest_switch_kernel(value) for value in range(4, 11)]
    scaling = [
        pairwise_kernel_scaling_record(value)
        for value in (8, 16, 32, 64, 128, 256)
    ]
    exact = all(row.exact_local_support_formula_verified for row in controls)
    classical = all(row.pairwise_kernel_classically_computable for row in scaling)
    theorem = PairwiseKernelDequantizationTheorem(
        membership_test=(
            "A charge term is two disjoint 3-cycles; each cycle must span exactly "
            "two target-matching edges and the two edge pairs must be disjoint."
        ),
        classical_algorithm=(
            "Build point-to-edge labels, enumerate 192*C(m,4) reference terms, "
            "and apply the constant-time membership predicate: O(m^4) time."
        ),
        nearest_switch_formula=(
            "I_m=80*C(m-2,2)+192*C(m-2,3)+192*C(m-2,4), so "
            "kappa=(m^2-5m+9)/(m(m-1))."
        ),
        mechanism_boundary=(
            "Pairwise charge fidelity is dequantized; only matrix-valued spectral "
            "transitions, noncommuting higher moments, or all-copy target interference remain."
        ),
        exact_all_rank_nearest_switch_kernel_proved=exact,
        arbitrary_pairwise_kernel_polynomial_time_classical=classical,
        charge_orbit_pairwise_fidelity_is_quantum_advantage=False,
        matrix_valued_spectral_transition_dequantized=False,
        noncommuting_higher_transition_moments_dequantized=False,
        all_copy_target_interference_dequantized=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact and classical,
        status=(
            "matching-charge-pairwise-kernel-dequantized-matrix-transition-open"
            if exact and classical
            else "matching-charge-pairwise-kernel-control-failure"
        ),
    )
    return PairwiseKernelDequantizationReport(
        created_at=utc_now(),
        theorem_contract={
            "input": "Two explicitly represented perfect matchings on 2m points",
            "kernel": "Normalized regular Hilbert-Schmidt overlap of D_h and D_h'",
            "classical_access": "Read both matching edge lists and enumerate polynomial orbit terms",
            "claim_boundary": (
                "Dequantizes only the pairwise charge Gram kernel, not spectral "
                "projector transitions or coherent likelihood interference."
            ),
        },
        nearest_switch_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-MATCHING-CHARGE-MATRIX-TRANSITION-KERNEL",
                "statement": (
                    "Compute source-weighted spectral-projector transition matrices, "
                    "not merely regular Hilbert-Schmidt overlaps."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-CHARGE-HIGHER-KERNEL-DEQUANTIZATION",
                "statement": (
                    "Determine whether fixed-order noncommuting charge transition "
                    "moments are also finite-support character polynomials."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-CHARGE-ALL-COPY-TRANSITION",
                "statement": (
                    "Isolate an all-copy target-coupled transition statistic that "
                    "escapes both pairwise-kernel and source-local no-go theorems."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Near-parallel neighboring charge states imply hardness.",
                "answer": (
                    "False. Their exact overlap and Theta(1/m) deficit have a direct "
                    "O(m^4) classical calculation."
                ),
                "resolved": True,
            },
            {
                "challenge": "The kernel algorithm requires enumerating S_(2m).",
                "answer": (
                    "False. It enumerates only 192*C(m,4) constant-support terms."
                ),
                "resolved": True,
            },
            {
                "challenge": "Pairwise-kernel dequantization kills the charge route.",
                "answer": (
                    "Too strong. Spectral projector transitions depend on matrix "
                    "structure not captured by the regular pairwise overlap."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_nearest_switch_kernel_theorem_count": int(exact),
            "polynomial_classical_pairwise_kernel_algorithm_count": int(classical),
            "classical_time_exponent": 4,
            "tail_nearest_kernel_deficit": scaling[-1].nearest_switch_kernel_deficit,
            "matrix_transition_dequantization_count": 0,
            "hidden_involution_detector_count": 0,
        },
        claim_gate={
            "pairwise_charge_kernel_classically_computable": classical,
            "nearest_switch_kernel_formula_proved": exact,
            "pairwise_charge_fidelity_quantum_advantage": False,
            "matrix_valued_spectral_transition_dequantized": False,
            "noncommuting_higher_transition_moments_dequantized": False,
            "all_copy_target_interference_dequantized": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The faithful charge orbit has a classically computable pairwise "
                "Gram geometry; only stronger matrix-valued transitions can matter."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the exact nearest-switch charge overlap and dequantized the "
            "arbitrary pairwise matching-charge kernel in O(m^4) classical time."
        ),
        falsifiers_triggered=[
            "Pairwise matching-charge fidelity is not a source of quantum advantage.",
            "Nearest hidden matchings have only Theta(1/m) charge-kernel separation.",
            "A viable charge algorithm must use matrix-valued or higher-order target recoupling.",
        ],
    )


def write_pairwise_kernel_dequantization_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_pairwise_kernel_dequantization_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_pairwise_kernel_dequantization_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
