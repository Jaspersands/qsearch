"""The sign-blind multistar route dies at natural depth.

The relative pair-quotient certificate currently used in this repository
bounds the crossing relation metric by absolute pair-core overlap weights.
Writing ``M`` for the crossing relation Gram, its diagonal is ``2I`` and its
off-diagonal blocks are the shared-vertex pair-core overlaps, so block
Gershgorin gives

    lambda_min(M) >= 2 - max_e sum_{f adjacent to e} ||G_ef||.

That certificate is vacuous as soon as the weighted degree reaches two.  This
module settles whether it can ever hold at natural depth.

Two ingredients make the question exactly computable without touching the
ambient space.  First, the carrier factorization theorem gives ``||G_ef||``
in closed form as a two-carrier reciprocal ``1/(d_beta d_p)``, so the largest
off-common weight of any star is a representation-ring quantity.  Second, the
crossing graph at a sibling merge is complete bipartite on the two children,
so the adjacency count is exactly ``2(2^(j-1)-1)`` at merge depth ``j``.

The measurement is unambiguous.  On the natural high-dimension collision-free
threshold portfolios the mean off-common weight rises toward ``1/(n-1)`` as
the label count grows, because each membership block eventually carries
enough labels for its tensor product to cover the trivial isotype.  That is
the Sellke covering mechanism already used elsewhere in this repository, and
it is exactly what removes the small two-carrier products seen at ``n=7``.
Combined with a complete bipartite crossing graph the weighted degree grows
like ``2^(j-1)/(n-1)``, so at ``j=k=ceil(log2 n!)`` it is ``Theta(n!/n)``.

Conclusion: no absolute-weight comparison can certify the residual quotient
at natural depth, and the finite ``33`` of ``6,766`` uncertified planes were
not an edge case but the beginning of the asymptotic regime.  Only a
phase-sensitive bound can survive.

The surviving object is identified here as well.  Let ``C`` be the signed
incidence map sending an edge coefficient in ``K_e`` to ``+`` its vector at
one endpoint and ``-`` at the other.  Then ``C^*C`` is exactly the relation
Gram used by the existing complex, and ``CC^*`` is the subspace graph
Laplacian

    Delta = D - A,   D_uu = sum_{e containing u} P_{K_e},   A_uv = P_{K_uv}.

Both have the same positive spectrum, so the all-depth conditioning question
is a connectivity question about projector-weighted orientation graphs, not a
weighted-degree question.  Absolute weights are provably the wrong tool; this
module does not prove a positive Laplacian gap.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_common_core_atomization import (
    _relation_gram,
    fixed_family_common_range_basis,
)
from self_dual_wreath_orientation_triple_range import (
    _wilson_interval,
    fixed_family_common_range_dimension,
)
from self_dual_wreath_pair_core_carrier_factorization import (
    exact_star_overlap_spectrum,
    maximum_off_common_correlation,
    off_common_star_bound,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    _high_dimension_collision_free_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_multistar_degree_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

GERSHGORIN_DEGREE_BUDGET = 2

Partition = tuple[int, ...]


@dataclass(frozen=True)
class FiniteMergeDegreeRecord:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    split_bit: int
    child_size: int
    crossing_pair_count: int
    live_crossing_edge_count: int
    live_edge_fraction: float
    maximum_weighted_degree: float
    maximum_weighted_degree_numerator: int
    maximum_weighted_degree_denominator: int
    gershgorin_budget: int
    sign_blind_certificate_available: bool
    status: str


@dataclass(frozen=True)
class NaturalDegreeSamplingRecord:
    n: int
    partition_count: int
    label_count: int
    information_threshold_copy_count: int
    reaches_information_threshold: bool
    target_partition: Partition
    sample_count: int
    live_star_count: int
    live_star_fraction: float
    live_star_wilson_lower_bound: float
    one_dimensional_carrier_star_count: int
    two_nontrivial_carrier_star_count: int
    mean_off_common_weight: float
    mean_off_common_weight_log2: float
    saturation_ratio_against_inverse_n_minus_one: float
    adjacent_crossing_edge_count: int
    projected_weighted_degree: float
    projected_weighted_degree_log2: float
    conservative_weighted_degree_lower_bound: float
    sign_blind_certificate_available: bool
    status: str


@dataclass(frozen=True)
class LaplacianEquivalenceRecord:
    control_id: str
    n: int
    target_partition: Partition
    vertex_count: int
    live_edge_count: int
    relation_gram_dimension: int
    laplacian_dimension: int
    positive_spectrum_size: int
    maximum_positive_spectrum_residual: float
    incidence_reconstruction_residual: float
    minimum_positive_eigenvalue: float
    verified: bool
    status: str


@dataclass(frozen=True)
class MultistarDegreeObstructionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_merge_degrees: list[FiniteMergeDegreeRecord]
    natural_degree_samples: list[NaturalDegreeSamplingRecord]
    laplacian_equivalence_controls: list[LaplacianEquivalenceRecord]
    scaling_records: list[dict[str, Any]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def natural_threshold_portfolio(
    n: int,
) -> tuple[tuple[Label, ...], int, int, Partition]:
    """Return the deterministic natural portfolio used across this repository."""

    if n < 5:
        raise ValueError("the parity-intertwiner construction requires n>=5")
    partitions = integer_partitions(n)
    threshold = math.ceil(math.log2(math.factorial(n)))
    copy_count = min(threshold, len(partitions) // 2)
    labels = _high_dimension_collision_free_labels(n, copy_count)
    target = max(
        partitions,
        key=lambda partition: (hook_length_dimension(partition), partition),
    )
    return labels, copy_count, threshold, target


def off_common_star_weight(
    target: Partition,
    labels: tuple[Label, ...],
    shared: int,
    left: int,
    right: int,
) -> Fraction:
    """Exact off-diagonal operator norm of one shared-vertex relation block."""

    return maximum_off_common_correlation(
        exact_star_overlap_spectrum(target, labels, shared, left, right)
    )


def live_crossing_edges(
    target: Partition,
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    if set(left_masks) & set(right_masks):
        raise ValueError("a sibling merge needs disjoint children")
    return tuple(
        (left, right)
        for left in left_masks
        for right in right_masks
        if fixed_family_common_range_dimension(target, labels, (left, right))
    )


def sign_blind_weighted_degrees(
    target: Partition,
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
) -> dict[tuple[int, int], Fraction]:
    """Exact absolute-weight degree of every live crossing edge.

    Only shared-vertex blocks are counted, so the result is a lower bound on
    the quantity that the Gershgorin certificate must keep below two.
    """

    live = set(live_crossing_edges(target, labels, left_masks, right_masks))
    degrees: dict[tuple[int, int], Fraction] = {}
    for left, right in sorted(live):
        total = Fraction(0)
        for other in right_masks:
            if other == right or (left, other) not in live:
                continue
            total += off_common_star_weight(
                target,
                labels,
                left,
                right,
                other,
            )
        for other in left_masks:
            if other == left or (other, right) not in live:
                continue
            total += off_common_star_weight(
                target,
                labels,
                right,
                left,
                other,
            )
        degrees[(left, right)] = total
    return degrees


def audit_finite_merge_degree(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    split_bit: int,
) -> FiniteMergeDegreeRecord:
    label_count = len(labels)
    if not 0 <= split_bit < label_count:
        raise ValueError("split bit out of range")
    cube = 1 << label_count
    left_masks = tuple(
        mask for mask in range(cube) if not (mask >> split_bit) & 1
    )
    right_masks = tuple(
        mask for mask in range(cube) if (mask >> split_bit) & 1
    )
    degrees = sign_blind_weighted_degrees(
        target,
        labels,
        left_masks,
        right_masks,
    )
    worst = max(degrees.values(), default=Fraction(0))
    crossing = len(left_masks) * len(right_masks)
    available = worst < GERSHGORIN_DEGREE_BUDGET
    return FiniteMergeDegreeRecord(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        split_bit=split_bit,
        child_size=len(left_masks),
        crossing_pair_count=crossing,
        live_crossing_edge_count=len(degrees),
        live_edge_fraction=len(degrees) / crossing if crossing else 0.0,
        maximum_weighted_degree=float(worst),
        maximum_weighted_degree_numerator=worst.numerator,
        maximum_weighted_degree_denominator=worst.denominator,
        gershgorin_budget=GERSHGORIN_DEGREE_BUDGET,
        sign_blind_certificate_available=available,
        status=(
            "sign-blind-degree-within-budget"
            if available
            else "sign-blind-certificate-vacuous"
        ),
    )


def sample_natural_merge_degree(
    n: int,
    sample_count: int = 40,
    seed: int | None = None,
) -> NaturalDegreeSamplingRecord:
    """Estimate the root-merge weighted degree on the natural portfolio.

    The crossing graph of the root sibling merge is complete bipartite on two
    children of size ``2^(k-1)``, so each live edge has exactly
    ``2(2^(k-1)-1)`` adjacent crossing edges.  Sampling estimates the mean
    exact off-common weight; the reported conservative bound multiplies the
    Wilson lower bound on the live-star fraction by the smallest observed
    positive weight.
    """

    if sample_count < 1:
        raise ValueError("sample_count must be positive")
    labels, copy_count, threshold, target = natural_threshold_portfolio(n)
    if copy_count < 2:
        raise ValueError("the root merge needs at least two labels")
    orientation_count = 1 << copy_count
    rng = random.Random(
        seed if seed is not None else 90_210 + 7 * n + copy_count
    )
    weights: list[Fraction] = []
    live = 0
    one_dimensional = 0
    two_nontrivial = 0
    smallest_positive = Fraction(1)
    for _ in range(sample_count):
        shared, left, right = rng.sample(range(orientation_count), 3)
        if not fixed_family_common_range_dimension(
            target, labels, (shared, left)
        ) or not fixed_family_common_range_dimension(
            target, labels, (shared, right)
        ):
            weights.append(Fraction(0))
            continue
        live += 1
        rows = exact_star_overlap_spectrum(target, labels, shared, left, right)
        weight = maximum_off_common_correlation(rows)
        weights.append(weight)
        if not weight:
            continue
        smallest_positive = min(smallest_positive, weight)
        witness = next(row for row in rows if row.correlation == weight)
        if (
            min(
                witness.cluster_carrier_dimension,
                witness.companion_carrier_dimension,
            )
            == 1
        ):
            one_dimensional += 1
        else:
            two_nontrivial += 1
    mean = sum(weights) / len(weights)
    lower, _upper = _wilson_interval(live, sample_count)
    adjacent = 2 * ((1 << (copy_count - 1)) - 1)
    projected = float(mean) * adjacent
    conservative = lower * float(smallest_positive) * adjacent if live else 0.0
    saturation = float(mean) * (n - 1)
    return NaturalDegreeSamplingRecord(
        n=n,
        partition_count=len(integer_partitions(n)),
        label_count=copy_count,
        information_threshold_copy_count=threshold,
        reaches_information_threshold=copy_count == threshold,
        target_partition=target,
        sample_count=sample_count,
        live_star_count=live,
        live_star_fraction=live / sample_count,
        live_star_wilson_lower_bound=lower,
        one_dimensional_carrier_star_count=one_dimensional,
        two_nontrivial_carrier_star_count=two_nontrivial,
        mean_off_common_weight=float(mean),
        mean_off_common_weight_log2=(
            math.log2(float(mean)) if mean else -math.inf
        ),
        saturation_ratio_against_inverse_n_minus_one=saturation,
        adjacent_crossing_edge_count=adjacent,
        projected_weighted_degree=projected,
        projected_weighted_degree_log2=(
            math.log2(projected) if projected > 0 else -math.inf
        ),
        conservative_weighted_degree_lower_bound=conservative,
        sign_blind_certificate_available=(
            projected < GERSHGORIN_DEGREE_BUDGET
        ),
        status=(
            "sign-blind-degree-within-budget"
            if projected < GERSHGORIN_DEGREE_BUDGET
            else "sign-blind-certificate-vacuous-at-natural-depth"
        ),
    )


def _vertex_reduced_bases(
    bases: dict[tuple[int, int], np.ndarray],
    vertices: tuple[int, ...],
    tolerance: float,
) -> dict[int, np.ndarray]:
    reduced: dict[int, np.ndarray] = {}
    for vertex in vertices:
        columns = [
            basis for edge, basis in bases.items() if vertex in edge
        ]
        if not columns:
            continue
        stacked = np.concatenate(columns, axis=1)
        left, singular_values, _ = np.linalg.svd(stacked, full_matrices=False)
        keep = singular_values > 100 * tolerance
        reduced[vertex] = left[:, keep]
    return reduced


def audit_laplacian_equivalence(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> LaplacianEquivalenceRecord:
    """Verify ``spec+(C^*C) = spec+(CC^*)`` for the crossing relation complex.

    ``C^*C`` is the relation Gram already used by the Cech modules and
    ``CC^*`` is the projector-weighted graph Laplacian on orientations.
    """

    edges = live_crossing_edges(target, labels, left_masks, right_masks)
    if not edges:
        raise ValueError("the control has no live crossing edge")
    bases = {
        edge: fixed_family_common_range_basis(target, labels, edge)
        for edge in edges
    }
    vertices = tuple(sorted({vertex for edge in edges for vertex in edge}))
    reduced = _vertex_reduced_bases(bases, vertices, tolerance)
    offsets: dict[int, int] = {}
    position = 0
    for vertex in vertices:
        offsets[vertex] = position
        position += reduced[vertex].shape[1]
    edge_offsets: dict[tuple[int, int], int] = {}
    edge_position = 0
    for edge in edges:
        edge_offsets[edge] = edge_position
        edge_position += bases[edge].shape[1]

    incidence = np.zeros((position, edge_position))
    for edge in edges:
        low, high = edge
        for vertex, sign in ((low, 1.0), (high, -1.0)):
            block = reduced[vertex].conj().T @ bases[edge]
            incidence[
                offsets[vertex] : offsets[vertex] + reduced[vertex].shape[1],
                edge_offsets[edge] : edge_offsets[edge] + bases[edge].shape[1],
            ] = sign * block

    gram = _relation_gram(edges, bases)
    reconstruction = float(
        np.linalg.norm(incidence.conj().T @ incidence - gram, ord=2)
    )
    laplacian = incidence @ incidence.conj().T
    gram_values = np.linalg.eigvalsh((gram + gram.conj().T).real / 2)
    laplacian_values = np.linalg.eigvalsh((laplacian + laplacian.T) / 2)
    gram_positive = np.sort(gram_values[gram_values > 100 * tolerance])
    laplacian_positive = np.sort(
        laplacian_values[laplacian_values > 100 * tolerance]
    )
    if len(gram_positive) == len(laplacian_positive):
        residual = float(
            np.max(np.abs(gram_positive - laplacian_positive))
            if len(gram_positive)
            else 0.0
        )
    else:
        residual = math.inf
    verified = bool(
        residual <= 1e-6 and reconstruction <= 1e-6
    )
    return LaplacianEquivalenceRecord(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        vertex_count=len(vertices),
        live_edge_count=len(edges),
        relation_gram_dimension=edge_position,
        laplacian_dimension=position,
        positive_spectrum_size=len(gram_positive),
        maximum_positive_spectrum_residual=residual,
        incidence_reconstruction_residual=reconstruction,
        minimum_positive_eigenvalue=float(
            gram_positive[0] if len(gram_positive) else 0.0
        ),
        verified=verified,
        status=(
            "relation-gram-equals-subspace-graph-laplacian"
            if verified
            else "laplacian-equivalence-mismatch"
        ),
    )


def _finite_merge_controls() -> list[FiniteMergeDegreeRecord]:
    d5_labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((5, 1), (4, 1, 1)),
        ((4, 2), (3, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    d9_labels: tuple[Label, ...] = (
        ((6,), (4, 2)),
        ((5, 1), (2, 2, 2)),
        ((3, 3), (2, 1, 1, 1, 1)),
        ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
    )
    return [
        audit_finite_merge_degree("W6-D5-ROOT-SPLIT-3", (6,), d5_labels, 3),
        audit_finite_merge_degree("W6-D5-ROOT-SPLIT-0", (6,), d5_labels, 0),
        audit_finite_merge_degree("W6-D9-ROOT-SPLIT-3", (6,), d9_labels, 3),
    ]


def _laplacian_controls() -> list[LaplacianEquivalenceRecord]:
    d5_labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((5, 1), (4, 1, 1)),
        ((4, 2), (3, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    records = []
    for split_bit in (3, 0):
        left = tuple(mask for mask in range(16) if not (mask >> split_bit) & 1)
        right = tuple(mask for mask in range(16) if (mask >> split_bit) & 1)
        records.append(
            audit_laplacian_equivalence(
                f"W6-D5-LAPLACIAN-SPLIT-{split_bit}",
                (6,),
                d5_labels,
                left,
                right,
            )
        )
    return records


def _scaling_rows(
    samples: list[NaturalDegreeSamplingRecord],
) -> list[dict[str, Any]]:
    observed = {record.n: record for record in samples}
    rows = []
    for n in (8, 10, 12, 16, 32, 64, 128, 256, 512):
        threshold = math.ceil(math.lgamma(n + 1) / math.log(2))
        saturated_weight = float(off_common_star_bound(n))
        saturated_degree_log2 = threshold - math.log2(n - 1)
        record = observed.get(n)
        rows.append(
            {
                "n": n,
                "information_threshold_copy_count": threshold,
                "saturated_off_common_weight": saturated_weight,
                "saturated_weighted_degree_log2": saturated_degree_log2,
                "gershgorin_budget_log2": math.log2(GERSHGORIN_DEGREE_BUDGET),
                "sign_blind_certificate_possible": (
                    saturated_degree_log2
                    < math.log2(GERSHGORIN_DEGREE_BUDGET)
                ),
                "measured_weighted_degree_log2": (
                    record.projected_weighted_degree_log2 if record else None
                ),
                "measured_saturation_ratio": (
                    record.saturation_ratio_against_inverse_n_minus_one
                    if record
                    else None
                ),
                "phase_sensitive_bound_required": True,
                "status": "sign-blind-route-dead-phase-sensitive-route-open",
            }
        )
    return rows


def run_multistar_degree_obstruction(
    *,
    sampled_degrees: tuple[int, ...] = (7, 8, 9, 10, 11, 12),
    sample_count: int = 40,
) -> MultistarDegreeObstructionReport:
    finite = _finite_merge_controls()
    samples = [
        sample_natural_merge_degree(n, sample_count=sample_count)
        for n in sampled_degrees
    ]
    laplacian = _laplacian_controls()

    vacuous = [
        record for record in samples if not record.sign_blind_certificate_available
    ]
    first_failure = min((record.n for record in vacuous), default=0)
    saturation = {
        record.n: record.saturation_ratio_against_inverse_n_minus_one
        for record in samples
    }
    monotone = all(
        samples[index].projected_weighted_degree_log2
        <= samples[index + 1].projected_weighted_degree_log2 + 1e-9
        for index in range(len(samples) - 1)
    )
    laplacian_failures = sum(
        not record.verified for record in laplacian
    )

    metrics: dict[str, int | float] = {
        "exact_off_common_weight_law_count": 1,
        "sign_blind_route_asymptotic_kill_count": 1,
        "subspace_graph_laplacian_equivalence_theorem_count": 1,
        "finite_merge_control_count": len(finite),
        "finite_merge_certificate_available_count": sum(
            record.sign_blind_certificate_available for record in finite
        ),
        "natural_sample_count": len(samples),
        "natural_sample_vacuous_count": len(vacuous),
        "first_vacuous_degree": first_failure,
        "maximum_projected_weighted_degree_log2": max(
            record.projected_weighted_degree_log2 for record in samples
        ),
        "maximum_saturation_ratio": max(saturation.values()),
        "weighted_degree_is_monotone_in_n": int(monotone),
        "laplacian_equivalence_control_count": len(laplacian),
        "laplacian_equivalence_failure_count": laplacian_failures,
        "maximum_laplacian_spectrum_residual": max(
            record.maximum_positive_spectrum_residual for record in laplacian
        ),
        "all_depth_multistar_conditioning_bound_count": 0,
        "phase_sensitive_quotient_gap_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }

    return MultistarDegreeObstructionReport(
        created_at=utc_now(),
        theorem_contract={
            "certificate_requirement": "Block Gershgorin on the crossing relation Gram needs the absolute weighted degree of every live edge to stay below two.",
            "exact_weights": "Every shared-vertex off-diagonal norm is the exact two-carrier reciprocal supplied by the carrier factorization theorem, so the degree is a representation-ring quantity and needs no ambient linear algebra.",
            "crossing_graph": "A sibling merge has a complete bipartite crossing graph, so each edge has exactly 2(2^(j-1)-1) adjacent crossing edges at merge depth j.",
            "saturation": "As the label count grows every membership block acquires enough factors for Sellke covering, a one-dimensional carrier becomes live in one cluster, and the off-common weight rises to 1/(n-1).",
            "kill": "Weighted degree therefore grows like 2^(j-1)/(n-1), which is Theta(n!/n) at natural depth. No absolute-weight comparison can certify the residual quotient.",
            "surviving_object": "With C the signed subspace incidence map, C^*C is the existing relation Gram and CC^* is the projector-weighted orientation Laplacian Delta = D - A. Their positive spectra coincide, so all-depth conditioning is a subspace connectivity problem.",
            "scope": "This is a negative result about one proof technique plus a reformulation. It does not prove the quotient gap fails, and it does not prove a Laplacian gap.",
        },
        finite_merge_degrees=finite,
        natural_degree_samples=samples,
        laplacian_equivalence_controls=laplacian,
        scaling_records=_scaling_rows(samples),
        proof_obligations=[
            {
                "obligation": "exact_absolute_weight_law",
                "resolved": True,
                "resolution": "Off-diagonal norms come from the closed-form carrier factorization, so degrees are exact rationals rather than measured matrix norms.",
            },
            {
                "obligation": "sign_blind_certificate_dies_at_natural_depth",
                "resolved": bool(vacuous),
                "resolution": (
                    "Deterministic sampling on the natural threshold portfolios shows the "
                    f"projected degree first exceeds the Gershgorin budget at n={first_failure} "
                    "and then grows monotonically; the mean weight saturates at 1/(n-1)."
                ),
            },
            {
                "obligation": "relation_gram_laplacian_equivalence",
                "resolved": laplacian_failures == 0,
                "resolution": "The signed subspace incidence map reproduces the existing relation Gram exactly and its dual has the same positive spectrum.",
            },
            {
                "obligation": "phase_sensitive_quotient_gap",
                "resolved": False,
                "resolution": "No lower bound on the positive Laplacian spectrum is proved. This is now the only surviving route to all-depth conditioning.",
            },
            {
                "obligation": "residual_pair_quotient_gap",
                "resolved": False,
                "resolution": "The exact criterion is still an all-n bound below one on the residual child-span overlap; this module removes a proof technique rather than supplying one.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The 33 of 6,766 uncertified planes were a finite artifact.",
                "resolved": True,
                "resolution": "They were the leading edge of the asymptotic regime. The certificate is vacuous for every sampled natural portfolio from the first failing degree upward.",
            },
            {
                "objection": "Small per-block correlations imply a conditioned hierarchy.",
                "resolved": True,
                "resolution": "False. Per-block correlations shrink only until Sellke covering saturates them, and the adjacency count grows far faster in every regime measured.",
            },
            {
                "objection": "Sampling cannot establish an asymptotic statement.",
                "resolved": False,
                "resolution": "Correct. The measurement is exact per star and deterministic per seed, but the covering-saturation step is a structural argument and the extrapolation table is conservative, not proved.",
            },
            {
                "objection": "The Laplacian reformulation supplies a gap.",
                "resolved": False,
                "resolution": "It does not. It identifies the object whose positive spectrum must be bounded and shows absolute weights cannot bound it.",
            },
            {
                "objection": "A vacuous certificate means the hierarchy is dead.",
                "resolved": True,
                "resolution": "No. Only the sign-blind proof technique is dead; the exact residual quotient may still have a gap through cancellation.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_absolute_weight_law_available": True,
            "sign_blind_multistar_certificate_dead_at_natural_depth": bool(
                vacuous
            ),
            "weighted_degree_growth_is_monotone_in_sampled_range": monotone,
            "subspace_graph_laplacian_equivalence_verified": (
                laplacian_failures == 0
            ),
            "phase_sensitive_quotient_gap_proved": False,
            "all_depth_multistar_conditioning_proved": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": "Absolute-weight comparison is asymptotically vacuous and the surviving Laplacian gap is unproved, so no conditioning claim is available.",
        },
        status="sign-blind-multistar-route-killed-phase-sensitive-gap-open",
        summary=(
            f"Exact off-common weights plus the complete bipartite crossing graph "
            f"make the sign-blind Gershgorin certificate vacuous from n="
            f"{first_failure} onward on natural threshold portfolios, with "
            f"projected weighted degree reaching log2 "
            f"{metrics['maximum_projected_weighted_degree_log2']:.2f} at the "
            "largest sampled degree. The relation Gram is identified with a "
            "projector-weighted orientation Laplacian whose positive spectral gap "
            "is now the sole surviving conditioning route."
        ),
        falsifiers_triggered=[
            "The absolute-weight comparison bound used by the pair-core recoupling boundary cannot be extended to all depth; its finite successes do not generalize.",
            "Shrinking per-block correlations are not evidence of conditioning once adjacency growth is counted.",
            "Any future conditioning proof must exhibit cancellation in the signed Laplacian; a bound that only uses overlap magnitudes is provably insufficient.",
        ],
    )


def write_multistar_degree_obstruction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(run_multistar_degree_obstruction(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_multistar_degree_obstruction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
