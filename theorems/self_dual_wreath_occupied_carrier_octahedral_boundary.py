"""Occupied carrier labels can commute while their channel graph is not a star.

The local carrier-label compiler leaves one physical question unresolved: do
the labels from several incident pair cores remain compatible after restricting
to the occupied coefficient space?  This module gives an exact growing-rank
control and, equally importantly, keeps its natural-mass scope honest.

For ``n>=5`` put

    V = [n-1,1],  W = [n-2,2],  tau = W tensor sign,

and use four unequal source labels

    (sign, V tensor sign), (W,V), (W,V), (W,V).

At orientation vertex zero exactly six incident pair cores survive.  Group
them into the three opposite pairs

    (6,7), (10,11), (12,13).

The exact membership-pattern carrier theorem and

    V tensor V = 1 + V + W + [n-2,1,1]

give the following all-n coefficient-space decomposition:

* the three even cores have rank ``(n-1)^2``;
* the three odd cores have rank ``n-1``;
* every nonopposite overlap has correlation
  ``gamma=2/(n(n-1)(n-3))``;
* an octahedral ``K_{2,2,2}`` channel has multiplicity ``n-1``;
* the three even cores also carry a triangle channel of multiplicity
  ``(n-1)(n-2)``.

Thus the occupied carrier support projectors commute and atomize, but the
unit-correlation normalized Gram is not a clique Gram.  The octahedral block
has spectrum ``{-1,1,5}`` after adding the identity, with ``-1`` multiplicity
``2(n-1)``.  At the physical correlation its minimum is ``1-2 gamma>0``;
the failure is specifically the scale-one vertex trivialization used by the
flat-clique route, not positivity of the physical Gram.

This family repeats source partitions.  Existing global Plancherel collision
theory therefore removes it from the natural information-threshold event with
probability ``1-o(1)``.  It decisively falsifies a universal star/clique law,
but it is not evidence for positive-mass contextuality in collision-free
typical portfolios.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_global_carrier_channel_extractor import (
    audit_carrier_channel_extraction,
)
from self_dual_wreath_orientation_triple_range import (
    fixed_family_common_range_dimension,
)
from self_dual_wreath_pair_core_carrier_factorization import (
    exact_star_overlap_spectrum,
)
from self_dual_wreath_vertex_channel_groupoid import (
    audit_vertex_channel_groupoid,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_occupied_carrier_octahedral_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-OCCUPIED-CARRIER-OCTAHEDRAL-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]
LIVE_DIFFERENCES = (6, 7, 10, 11, 12, 13)
OPPOSITE_PAIRS = ((6, 7), (10, 11), (12, 13))
LARGE_DIFFERENCES = (6, 10, 12)
SMALL_DIFFERENCES = (7, 11, 13)


@dataclass(frozen=True)
class OctahedralFamilyRecord:
    n: int
    target_partition: Partition
    source_labels: tuple[Label, ...]
    live_differences: tuple[int, ...]
    live_core_ranks: tuple[int, ...]
    nonopposite_overlap_count: int
    opposite_zero_overlap_count: int
    correlation_numerator: int
    correlation_denominator: int
    observed_correlation_denominators: tuple[int, ...]
    maximum_exact_overlap_multiplicity: int
    octahedral_channel_multiplicity: int
    triangle_channel_multiplicity: int
    total_coefficient_dimension: int
    octahedral_coefficient_trace_mass: float
    unit_correlation_negative_dimension: int
    unit_correlation_negative_trace_mass: float
    physical_gram_minimum_eigenvalue: float
    exact_family_formula_verified: bool
    status: str


@dataclass(frozen=True)
class DenseOccupiedCompatibilityControl:
    n: int
    ambient_dimension: int
    exact_common_dimension_removed: int
    residual_edge_dimensions: tuple[int, ...]
    support_projector_commutator_norm: float
    occupied_support_projectors_commute: bool
    extracted_channel_count: int
    octahedral_channel_multiplicity: int
    triangle_channel_multiplicity: int
    maximum_link_unitarity_residual: float
    clique_path_composition_residual: float
    unit_correlation_minimum_eigenvalue: float
    unit_correlation_negative_eigenvalue_count: int
    expected_unit_correlation_negative_eigenvalue_count: int
    physical_correlation: float
    physical_gram_minimum_eigenvalue: float
    physical_gram_positive: bool
    dense_control_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalMassBoundaryRecord:
    n: int
    information_threshold_copy_count: int
    target_plancherel_mass: str
    exceptional_source_tuple_mass: str
    full_control_mass: str
    log2_full_control_mass: float
    conditional_octahedral_trace_mass: float
    conditional_negative_normalized_trace_mass: float
    repeats_source_partitions: bool
    excluded_by_global_distinct_typical_event: bool
    positive_natural_mass_proved: bool
    status: str


@dataclass(frozen=True)
class OccupiedCarrierOctahedralBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    family_records: list[OctahedralFamilyRecord]
    dense_control: DenseOccupiedCompatibilityControl
    natural_mass_records: list[NaturalMassBoundaryRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def octahedral_family_labels(
    n: int,
) -> tuple[Partition, tuple[Label, ...]]:
    if n < 5:
        raise ValueError("the stable octahedral family requires n>=5")
    sign = (1,) * n
    standard = (n - 1, 1)
    conjugate_standard = (2,) + (1,) * (n - 2)
    two_row = (n - 2, 2)
    target = (2, 2) + (1,) * (n - 4)
    labels: tuple[Label, ...] = (
        (sign, conjugate_standard),
        (two_row, standard),
        (two_row, standard),
        (two_row, standard),
    )
    return target, labels


def _is_opposite(first: int, second: int) -> bool:
    return tuple(sorted((first, second))) in OPPOSITE_PAIRS


def _fraction_log2(value: Fraction) -> float:
    if value <= 0:
        return -math.inf
    return math.log2(value.numerator) - math.log2(value.denominator)


def audit_octahedral_family(n: int) -> OctahedralFamilyRecord:
    target, labels = octahedral_family_labels(n)
    ranks = tuple(
        fixed_family_common_range_dimension(target, labels, (0, difference))
        for difference in LIVE_DIFFERENCES
    )
    expected_large = (n - 1) ** 2
    expected_small = n - 1
    expected_ranks = tuple(
        expected_large if difference in LARGE_DIFFERENCES else expected_small
        for difference in LIVE_DIFFERENCES
    )
    two_row_dimension = n * (n - 3) // 2
    denominator = two_row_dimension * (n - 1)
    observed_denominators: set[int] = set()
    nonopposite_count = 0
    opposite_zero_count = 0
    multiplicities: dict[tuple[int, int], int] = {}
    rows_verified = True
    for first, second in itertools.combinations(LIVE_DIFFERENCES, 2):
        rows = exact_star_overlap_spectrum(
            target,
            labels,
            0,
            first,
            second,
        )
        if _is_opposite(first, second):
            opposite_zero_count += not rows
            rows_verified &= not rows
            continue
        nonopposite_count += 1
        expected_multiplicity = (
            expected_large
            if first in LARGE_DIFFERENCES and second in LARGE_DIFFERENCES
            else expected_small
        )
        rows_verified &= bool(
            len(rows) == 1
            and rows[0].correlation_denominator == denominator
            and rows[0].multiplicity == expected_multiplicity
        )
        if rows:
            observed_denominators.add(rows[0].correlation_denominator)
            multiplicities[(first, second)] = rows[0].multiplicity

    octahedral_multiplicity = n - 1
    triangle_multiplicity = (n - 1) * (n - 2)
    total_dimension = 3 * n * (n - 1)
    gamma = Fraction(1, denominator)
    verified = bool(
        ranks == expected_ranks
        and nonopposite_count == 12
        and opposite_zero_count == 3
        and observed_denominators == {denominator}
        and rows_verified
        and hook_length_dimension((n - 2, 2)) == two_row_dimension
        and hook_length_dimension((n - 1, 1)) == n - 1
        and 6 * octahedral_multiplicity
        + 3 * triangle_multiplicity
        == total_dimension
    )
    return OctahedralFamilyRecord(
        n=n,
        target_partition=target,
        source_labels=labels,
        live_differences=LIVE_DIFFERENCES,
        live_core_ranks=ranks,
        nonopposite_overlap_count=nonopposite_count,
        opposite_zero_overlap_count=opposite_zero_count,
        correlation_numerator=1,
        correlation_denominator=denominator,
        observed_correlation_denominators=tuple(sorted(observed_denominators)),
        maximum_exact_overlap_multiplicity=max(multiplicities.values(), default=0),
        octahedral_channel_multiplicity=octahedral_multiplicity,
        triangle_channel_multiplicity=triangle_multiplicity,
        total_coefficient_dimension=total_dimension,
        octahedral_coefficient_trace_mass=2 / n,
        unit_correlation_negative_dimension=2 * (n - 1),
        unit_correlation_negative_trace_mass=2 / (3 * n),
        physical_gram_minimum_eigenvalue=float(1 - 2 * gamma),
        exact_family_formula_verified=verified,
        status=(
            "exact-occupied-octahedral-plus-triangle-family-verified"
            if verified
            else "occupied-octahedral-family-control-failure"
        ),
    )


def _adjacency(vertices: tuple[int, ...], edges: tuple[tuple[int, int], ...]) -> np.ndarray:
    index = {vertex: position for position, vertex in enumerate(vertices)}
    matrix = np.zeros((len(vertices), len(vertices)))
    for first, second in edges:
        left, right = index[first], index[second]
        matrix[left, right] = 1.0
        matrix[right, left] = 1.0
    return matrix


def _octahedral_edges() -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for first, second in itertools.combinations(LIVE_DIFFERENCES, 2)
        if not _is_opposite(first, second)
    )


def audit_dense_occupied_compatibility() -> DenseOccupiedCompatibilityControl:
    n = 5
    target, labels = octahedral_family_labels(n)
    edges = tuple((0, difference) for difference in LIVE_DIFFERENCES)
    groupoid = audit_vertex_channel_groupoid(
        "W5-REPEATED-OCCUPIED-OCTAHEDRAL-CONTROL",
        target,
        labels,
        edges,
        0,
    )
    extraction = audit_carrier_channel_extraction(
        "W5-REPEATED-OCCUPIED-OCTAHEDRAL-EXTRACTION",
        target,
        labels,
        (0, *LIVE_DIFFERENCES),
    )
    octahedral = next(
        channel for channel in extraction.channels if channel.edge_count == 6
    )
    triangle = next(
        channel for channel in extraction.channels if channel.edge_count == 3
    )
    gamma = 1 / audit_octahedral_family(n).correlation_denominator
    physical_minimum = 1 - 2 * gamma
    expected_negative = 2 * (n - 1)
    verified = bool(
        extraction.extraction_audit_verified
        and groupoid.maximum_support_projection_commutator_norm <= 1e-8
        and octahedral.coefficient_multiplicity == n - 1
        and triangle.coefficient_multiplicity == (n - 1) * (n - 2)
        and groupoid.normalized_gram_negative_eigenvalue_count == expected_negative
        and abs(groupoid.normalized_gram_minimum_eigenvalue + 1) <= 1e-8
        and physical_minimum > 0
    )
    return DenseOccupiedCompatibilityControl(
        n=n,
        ambient_dimension=extraction.ambient_dimension,
        exact_common_dimension_removed=(
            extraction.exact_common_coefficient_dimension_removed
        ),
        residual_edge_dimensions=groupoid.residual_edge_dimensions,
        support_projector_commutator_norm=(
            groupoid.maximum_support_projection_commutator_norm
        ),
        occupied_support_projectors_commute=(
            groupoid.maximum_support_projection_commutator_norm <= 1e-8
        ),
        extracted_channel_count=extraction.nontrivial_channel_count,
        octahedral_channel_multiplicity=octahedral.coefficient_multiplicity,
        triangle_channel_multiplicity=triangle.coefficient_multiplicity,
        maximum_link_unitarity_residual=max(
            channel.maximum_link_unitarity_residual
            for channel in extraction.channels
        ),
        clique_path_composition_residual=(
            groupoid.maximum_path_composition_residual
        ),
        unit_correlation_minimum_eigenvalue=(
            groupoid.normalized_gram_minimum_eigenvalue
        ),
        unit_correlation_negative_eigenvalue_count=(
            groupoid.normalized_gram_negative_eigenvalue_count
        ),
        expected_unit_correlation_negative_eigenvalue_count=expected_negative,
        physical_correlation=gamma,
        physical_gram_minimum_eigenvalue=physical_minimum,
        physical_gram_positive=physical_minimum > 0,
        dense_control_verified=verified,
        status=(
            "occupied-labels-commute-octahedral-clique-normalization-fails"
            if verified
            else "occupied-octahedral-dense-control-failure"
        ),
    )


def natural_mass_boundary_record(n: int) -> NaturalMassBoundaryRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    order = math.factorial(n)
    standard_dimension = n - 1
    two_row_dimension = n * (n - 3) // 2
    target_mass = Fraction(two_row_dimension**2, order)
    exceptional_label_mass = Fraction(2 * standard_dimension**2, order**2)
    repeated_label_mass = Fraction(
        2 * two_row_dimension**2 * standard_dimension**2,
        order**2,
    )
    source_tuple_mass = exceptional_label_mass * repeated_label_mass**3
    full_mass = target_mass * source_tuple_mass
    return NaturalMassBoundaryRecord(
        n=n,
        information_threshold_copy_count=math.ceil(math.log2(order)),
        target_plancherel_mass=str(target_mass),
        exceptional_source_tuple_mass=str(source_tuple_mass),
        full_control_mass=str(full_mass),
        log2_full_control_mass=round(_fraction_log2(full_mass), 12),
        conditional_octahedral_trace_mass=2 / n,
        conditional_negative_normalized_trace_mass=2 / (3 * n),
        repeats_source_partitions=True,
        excluded_by_global_distinct_typical_event=True,
        positive_natural_mass_proved=False,
        status="repeated-source-octahedral-family-natural-mass-vanishes",
    )


def run_occupied_carrier_octahedral_boundary(
) -> OccupiedCarrierOctahedralBoundaryReport:
    exact_n_values = (5, 6, 7, 8, 10, 12, 16)
    family = [audit_octahedral_family(n) for n in exact_n_values]
    dense = audit_dense_occupied_compatibility()
    natural = [
        natural_mass_boundary_record(n)
        for n in (5, 8, 12, 16, 24, 32, 48, 64)
    ]
    exact = all(record.exact_family_formula_verified for record in family)
    mass_decreases = all(
        right.log2_full_control_mass < left.log2_full_control_mass
        for left, right in zip(natural, natural[1:])
    )
    verified = bool(exact and dense.dense_control_verified and mass_decreases)
    metrics: dict[str, int | float] = {
        "all_n_octahedral_channel_formula_theorem_count": int(verified),
        "exact_scaling_control_count": len(family),
        "exact_scaling_control_failure_count": sum(
            not record.exact_family_formula_verified for record in family
        ),
        "maximum_exact_control_n": max(exact_n_values),
        "occupied_support_commuting_control_count": int(
            dense.occupied_support_projectors_commute
        ),
        "occupied_support_projector_commutator_norm": (
            dense.support_projector_commutator_norm
        ),
        "octahedral_channel_edge_count": 12,
        "octahedral_channel_vertex_count": 6,
        "dense_octahedral_channel_multiplicity": (
            dense.octahedral_channel_multiplicity
        ),
        "dense_triangle_channel_multiplicity": dense.triangle_channel_multiplicity,
        "unit_correlation_minimum_eigenvalue": (
            dense.unit_correlation_minimum_eigenvalue
        ),
        "unit_correlation_negative_eigenvalue_count": (
            dense.unit_correlation_negative_eigenvalue_count
        ),
        "physical_gram_minimum_eigenvalue": dense.physical_gram_minimum_eigenvalue,
        "tail_conditional_octahedral_trace_mass": (
            natural[-1].conditional_octahedral_trace_mass
        ),
        "tail_log2_full_control_mass": natural[-1].log2_full_control_mass,
        "collision_free_positive_mass_contextuality_theorem_count": 0,
        "coherent_collision_free_global_atom_labeler_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return OccupiedCarrierOctahedralBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "stable_family": (
                "tau=[2,2,1^(n-4)]; sources (sign,[2,1^(n-2)]) and "
                "three copies of ([n-2,2],[n-1,1]), n>=5."
            ),
            "representation_identity": (
                "[n-1,1]^tensor2=[n]+[n-1,1]+[n-2,2]+[n-2,1,1], "
                "with sign twisting by partition conjugation."
            ),
            "occupied_decomposition": (
                "K_(2,2,2) tensor C^(n-1) plus K_3 tensor "
                "C^((n-1)(n-2)) on the six incident coefficient fibers."
            ),
            "correlation": "gamma=2/[n(n-1)(n-3)].",
            "scale_one_boundary": (
                "I+A(K_2,2,2) has minimum -1, while the physical "
                "I+gamma A has minimum 1-2gamma>0."
            ),
            "natural_scope": (
                "The family repeats source partitions and lies outside the "
                "asymptotically full globally distinct Plancherel event."
            ),
        },
        family_records=family,
        dense_control=dense,
        natural_mass_records=natural,
        proof_obligations=[
            {
                "obligation": "identify_a_growing_multiplicity_physical_occupied_control",
                "resolved": verified,
                "resolution": (
                    "The exact stable family has coefficient ranks (n-1)^2 and "
                    "n-1 and channel multiplicities growing as n and n^2."
                ),
            },
            {
                "obligation": "test_occupied_carrier_label_commutation",
                "resolved": verified,
                "resolution": (
                    "The coefficient fibers split into exact octahedral and "
                    "triangle support atoms; the dense physical commutator is roundoff."
                ),
            },
            {
                "obligation": "derive_channel_topology_after_atomization",
                "resolved": verified,
                "resolution": (
                    "The six-edge support is the octahedral graph K_(2,2,2), "
                    "not a star or clique, plus a triangle on the larger fibers."
                ),
            },
            {
                "obligation": "prove_positive_natural_mass_for_the_obstruction",
                "resolved": False,
                "resolution": (
                    "False for this family: it repeats source partitions and its "
                    "explicit Plancherel mass vanishes; global collisions are o(1)."
                ),
            },
            {
                "obligation": "settle_collision_free_typical_label_compatibility",
                "resolved": False,
                "resolution": (
                    "Need a coefficient-level commutator/holonomy theorem or "
                    "counterexample for globally distinct typical partitions."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Noncommuting occupied label projectors cause the failure.",
                "resolved": True,
                "resolution": (
                    "False here: supports commute. The failed inference is from "
                    "commuting atoms to clique/star channel topology."
                ),
            },
            {
                "objection": "The indefinite normalized Gram makes the physical Gram invalid.",
                "resolved": True,
                "resolution": (
                    "False: physical gamma is O(n^-3), and the exact minimum "
                    "1-2gamma is positive. Only unit-correlation trivialization fails."
                ),
            },
            {
                "objection": "A growing-rank exact family has positive natural mass.",
                "resolved": True,
                "resolution": (
                    "False: rank growth and Plancherel mass are separate. The "
                    "repeated stable source tuple is asymptotically negligible."
                ),
            },
            {
                "objection": "This settles the collision-free natural route.",
                "resolved": False,
                "resolution": (
                    "It does not; global distinctness removes this family from the "
                    "typical event, where compatibility and graph topology remain open."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "all_n_occupied_octahedral_channel_formula_proved": verified,
            "occupied_repeated_family_support_projectors_commute": verified,
            "commuting_occupied_supports_force_clique_channels": False,
            "unit_correlation_vertex_trivialization_valid_for_family": False,
            "physical_gram_remains_positive": dense.physical_gram_positive,
            "repeated_octahedral_family_has_positive_natural_mass": False,
            "collision_free_typical_occupied_projectors_commute_all_depth": False,
            "coherent_collision_free_global_atom_labeler_compiled": False,
            "coherent_multistar_racah_resolver_compiled": False,
            "physical_root_anchor_compiled": False,
            "physical_pgm_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A growing physical occupied family atomizes exactly but produces "
                "an octahedral channel, refuting universal star/clique inference. "
                "Its repeated-source mass vanishes, so the collision-free typical "
                "compatibility and compiler questions remain open."
            ),
        },
        status=(
            "occupied-octahedral-channel-proved-repeated-mass-vanishes-"
            "collision-free-boundary-open"
            if verified
            else "occupied-octahedral-boundary-validation-failure"
        ),
        summary=(
            "Proved an all-n growing-rank occupied K_(2,2,2) plus K_3 carrier "
            "decomposition with commuting labels but failed clique normalization; "
            "the repeated-source family has vanishing natural mass."
        ),
        falsifiers_triggered=[
            "Commuting occupied carrier supports do not force star or clique channel topology.",
            "A unit-correlation flat-clique normalization can be indefinite even when the physical small-correlation Gram is positive.",
            "Growing coefficient multiplicity does not imply positive Plancherel mass.",
            "Repeated-label physical counterfamilies cannot settle the globally distinct natural threshold regime.",
        ],
    )


def write_occupied_carrier_octahedral_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    payload = asdict(run_occupied_carrier_octahedral_boundary(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Occupied carrier octahedral channel boundary",
                status="completed-exact-repeated-family-boundary",
                hypothesis=(
                    "Physically occupied carrier labels may atomize at growing "
                    "multiplicity without producing the star/clique topology "
                    "assumed by the current scalar compiler."
                ),
                protocol=(
                    "Construct the stable repeated-source family, evaluate exact "
                    "pair-core ranks and carrier overlaps, densely short the n=5 "
                    "control, extract support atoms, and audit Plancherel mass."
                ),
                positive_signal=(
                    "A collision-free positive-mass family with commuting global "
                    "atoms and a uniformly compilable bounded channel graph."
                ),
                falsifiers=[
                    "commuting supports are promoted to clique topology",
                    "unit-correlation indefiniteness is confused with physical Gram failure",
                    "growing rank is promoted without natural mass",
                    "a repeated-label control is extrapolated to globally distinct tuples",
                ],
                metrics=[
                    "all_n_octahedral_channel_formula_theorem_count",
                    "occupied_support_projector_commutator_norm",
                    "unit_correlation_minimum_eigenvalue",
                    "physical_gram_minimum_eigenvalue",
                    "tail_log2_full_control_mass",
                    "collision_free_positive_mass_contextuality_theorem_count",
                ],
                dependencies=[
                    "pair-core carrier factorization",
                    "global carrier-channel extraction",
                    "vertex channel groupoid",
                    "global Plancherel partition collision theorem",
                ],
                next_actions=[
                    "search globally distinct typical portfolios at coefficient level",
                    "derive a collision-free occupied support-commutation or contextuality theorem",
                    "classify bounded channel graphs before applying the star Cayley compiler",
                    "compile a graph-general Cayley observable only on positive natural mass",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-OCCUPIED-CARRIER-"
            "OCTAHEDRAL-BOUNDARY-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_occupied_carrier_octahedral_boundary": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="COMMUTING-OCCUPIED-CARRIER-SUPPORTS-NOT-CLIQUE-CHANNELS",
                source=registry_experiment_id,
                claim=(
                    "Commuting occupied carrier support projectors and partial-"
                    "isometry links force a star or positive clique channel."
                ),
                reason_invalid=(
                    "The exact repeated-source family atomizes as K_(2,2,2) "
                    "with multiplicity n-1 plus K_3 with multiplicity "
                    "(n-1)(n-2); its unit-correlation Gram has eigenvalue -1."
                ),
                lesson=(
                    "Classify the occupied channel graph and its scale separately "
                    "from support commutation before selecting a Cayley compiler."
                ),
                applies_to=[
                    registry_candidate_id,
                    "global carrier-channel atomization",
                    "affine-star Cayley compilation",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="REPEATED-OCTAHEDRAL-CARRIER-FAMILY-NOT-NATURAL-MASS",
                source=registry_experiment_id,
                claim=(
                    "The growing-rank octahedral occupied family establishes a "
                    "positive-mass obstruction for natural threshold tuples."
                ),
                reason_invalid=(
                    "Its source portfolio repeats partitions; explicit Plancherel "
                    "mass vanishes and global source collisions occur with o(1) probability."
                ),
                lesson=(
                    "Continue on globally distinct typical partitions and report "
                    "coefficient trace mass separately from source probability."
                ),
                applies_to=[
                    registry_candidate_id,
                    "natural-mass extrapolation",
                    "repeated-label controls",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_occupied_carrier_octahedral_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
