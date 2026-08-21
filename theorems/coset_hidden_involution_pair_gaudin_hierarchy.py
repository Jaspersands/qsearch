"""A commuting pair-Gaudin hierarchy for hyperoctahedral recoupling.

For pair labels ``i<j``, let ``c_ij`` be the sum of the eight 3-cycles on
the four endpoints of the two distinguished pairs.  These local interactions
satisfy the infinitesimal braid relations

    [c_ij,c_kl] = 0                              for disjoint pair sets,
    [c_ij,c_ik+c_jk] = 0                         for distinct i,j,k.

Consequently the relative charges

    J_r = sum_(i<r) c_(i,r),       r=2,...,m,

commute exactly at every rank.  Each ``J_r`` is Hermitian and has only
``8(r-1)`` permutation terms.  The cumulative sum is the unnormalized local
orbit charge from the natural-mass commutator theorem:

    sum_(r=2)^m J_r = sum_(g in C_m) g.

Thus this is not an arbitrary commuting family.  Its normalized aggregate
has inverse-polynomial copy-space variance and spectral diameter on growing-
defect hidden-involution source mass.

The hierarchy is a plausible factorization coordinate system for the huge
vertical edges in the ``K_(m-1) <= K_m`` / ``S_(2m-1) <= S_(2m)`` commuting
square.  It is not yet that factorization.  Individual ``J_r`` do not commute
with the final ``K_m`` action; only their cumulative orbit sum does.  Finite
joint spectra are highly nontrivial but retain degeneracies.  A useful
compiler must derive the connection from this intermediate Gaudin basis to a
``K_m``-adapted vertical-edge basis, with polynomial gaps and source-aware
normalization.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    _K_generators,
    exact_branching_commutant_dimension,
)
from coset_hidden_involution_commutant_support_growth_boundary import (
    _average_matrices_for_sets,
)
from coset_hidden_involution_plancherel_local_commutant_certificate import (
    C_orbit,
    _embed_pair_template,
    canonical_C_orbit,
    normalized_commutator_squared_norm,
)
from representation_obstruction import integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_pair_gaudin_hierarchy.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-PAIR-GAUDIN-HIERARCHY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
GroupAlgebraElement = dict[Permutation, int]


@dataclass(frozen=True)
class InfinitesimalBraidControl:
    disjoint_commutator_nonzero_count: int
    triangle_relation_nonzero_count: int
    pair_interaction_term_count: int
    disjoint_support_relation_verified: bool
    triangle_relation_verified: bool
    all_rank_local_relations_proved: bool
    status: str


@dataclass(frozen=True)
class ChargeHierarchyControl:
    half_degree: int
    charge_count: int
    minimum_charge_term_count: int
    maximum_charge_term_count: int
    pairwise_charge_commutator_failure_count: int
    cumulative_term_count: int
    expected_cumulative_orbit_term_count: int
    cumulative_equals_global_orbit_sum: bool
    charges_commute_pairwise: bool
    individual_charges_commuting_with_final_K_count: int
    cumulative_charge_commutes_with_final_K: bool
    status: str


@dataclass(frozen=True)
class JointSpectrumFiniteControl:
    half_degree: int
    repeated_partition_count: int
    minimum_symmetric_irrep_dimension: int
    maximum_symmetric_irrep_dimension: int
    minimum_distinct_joint_eigenvalue_count: int
    maximum_distinct_joint_eigenvalue_count: int
    minimum_distinct_joint_eigenvalue_fraction: float
    maximum_joint_eigenspace_multiplicity: int
    simple_joint_spectrum_partition_count: int
    maximum_pairwise_matrix_commutator_residual: float
    minimum_observed_distinct_encoded_gap: float
    finite_numerical_control_only: bool
    status: str


@dataclass(frozen=True)
class PairGaudinHierarchyTheorem:
    local_interaction: str
    infinitesimal_braid_relations: str
    commuting_charges: str
    cumulative_natural_charge: str
    compiler_opportunity: str
    final_K_boundary: str
    exact_all_rank_commuting_hierarchy_proved: bool
    polynomial_term_count_per_charge_proved: bool
    cumulative_charge_has_natural_copy_variance_proved: bool
    joint_spectrum_simple_on_all_finite_controls: bool
    charges_preserve_final_K_labels: bool
    vertical_multiplicity_edges_factored: bool
    connection_to_K_adapted_basis_compiled: bool
    source_aware_subduction_transform_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairGaudinHierarchyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    local_control: InfinitesimalBraidControl
    hierarchy_controls: list[ChargeHierarchyControl]
    spectrum_controls: list[JointSpectrumFiniteControl]
    theorem: PairGaudinHierarchyTheorem
    natural_variance_bridge: dict[str, Any]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _element(permutations: Iterable[Permutation]) -> GroupAlgebraElement:
    output: defaultdict[Permutation, int] = defaultdict(int)
    for permutation in permutations:
        output[permutation] += 1
    return dict(output)


def _add_elements(*elements: GroupAlgebraElement) -> GroupAlgebraElement:
    output: defaultdict[Permutation, int] = defaultdict(int)
    for element in elements:
        for permutation, coefficient in element.items():
            output[permutation] += coefficient
    return {
        permutation: coefficient
        for permutation, coefficient in output.items()
        if coefficient
    }


def _commutator(
    left: GroupAlgebraElement,
    right: GroupAlgebraElement,
) -> GroupAlgebraElement:
    output: defaultdict[Permutation, int] = defaultdict(int)
    for left_permutation, left_coefficient in left.items():
        for right_permutation, right_coefficient in right.items():
            coefficient = left_coefficient * right_coefficient
            output[
                compose_permutations(left_permutation, right_permutation)
            ] += coefficient
            output[
                compose_permutations(right_permutation, left_permutation)
            ] -= coefficient
    return {
        permutation: coefficient
        for permutation, coefficient in output.items()
        if coefficient
    }


@lru_cache(maxsize=None)
def pair_interaction(
    half_degree: int,
    left_pair: int,
    right_pair: int,
) -> tuple[Permutation, ...]:
    if not 0 <= left_pair < right_pair < half_degree:
        raise ValueError("pair labels must satisfy 0<=left<right<m")
    return tuple(
        _embed_pair_template(
            template,
            (left_pair, right_pair),
            half_degree,
        )
        for template in canonical_C_orbit()
    )


@lru_cache(maxsize=None)
def relative_charge_terms(
    rank: int,
    ambient_half_degree: int,
) -> tuple[Permutation, ...]:
    if not 2 <= rank <= ambient_half_degree:
        raise ValueError("rank must lie in [2,ambient_half_degree]")
    return tuple(
        permutation
        for earlier in range(rank - 1)
        for permutation in pair_interaction(
            ambient_half_degree,
            earlier,
            rank - 1,
        )
    )


@lru_cache(maxsize=1)
def audit_infinitesimal_braid_relations() -> InfinitesimalBraidControl:
    c01 = _element(pair_interaction(4, 0, 1))
    c02 = _element(pair_interaction(4, 0, 2))
    c12 = _element(pair_interaction(4, 1, 2))
    c23 = _element(pair_interaction(4, 2, 3))
    disjoint = _commutator(c01, c23)
    triangle = _commutator(c01, _add_elements(c02, c12))
    verified = not disjoint and not triangle
    return InfinitesimalBraidControl(
        disjoint_commutator_nonzero_count=len(disjoint),
        triangle_relation_nonzero_count=len(triangle),
        pair_interaction_term_count=len(canonical_C_orbit()),
        disjoint_support_relation_verified=not disjoint,
        triangle_relation_verified=not triangle,
        all_rank_local_relations_proved=verified,
        status=(
            "pair-interactions-satisfy-infinitesimal-braid-relations"
            if verified
            else "pair-gaudin-local-relation-failure"
        ),
    )


def _commutes_with_permutation_generators(
    element: GroupAlgebraElement,
    generators: tuple[Permutation, ...],
) -> bool:
    return all(
        not _commutator(element, {generator: 1})
        for generator in generators
    )


@lru_cache(maxsize=None)
def audit_charge_hierarchy(half_degree: int) -> ChargeHierarchyControl:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    charges = [
        _element(relative_charge_terms(rank, half_degree))
        for rank in range(2, half_degree + 1)
    ]
    failures = sum(
        bool(_commutator(charges[left], charges[right]))
        for left in range(len(charges))
        for right in range(left + 1, len(charges))
    )
    cumulative = _add_elements(*charges)
    global_orbit = _element(C_orbit(half_degree))
    generators = _K_generators(half_degree)
    compatible_count = sum(
        _commutes_with_permutation_generators(charge, generators)
        for charge in charges
    )
    cumulative_compatible = _commutes_with_permutation_generators(
        cumulative,
        generators,
    )
    exact = (
        failures == 0
        and cumulative == global_orbit
        and cumulative_compatible
    )
    term_counts = [sum(abs(value) for value in charge.values()) for charge in charges]
    return ChargeHierarchyControl(
        half_degree=half_degree,
        charge_count=len(charges),
        minimum_charge_term_count=min(term_counts),
        maximum_charge_term_count=max(term_counts),
        pairwise_charge_commutator_failure_count=failures,
        cumulative_term_count=sum(abs(value) for value in cumulative.values()),
        expected_cumulative_orbit_term_count=len(C_orbit(half_degree)),
        cumulative_equals_global_orbit_sum=cumulative == global_orbit,
        charges_commute_pairwise=failures == 0,
        individual_charges_commuting_with_final_K_count=compatible_count,
        cumulative_charge_commutes_with_final_K=cumulative_compatible,
        status=(
            "commuting-succinct-hierarchy-final-K-incompatible"
            if exact and compatible_count < len(charges)
            else "pair-gaudin-hierarchy-control-failure"
        ),
    )


def _eigenvalue_cluster_sizes(
    eigenvalues: np.ndarray,
    *,
    tolerance: float = 1e-8,
) -> tuple[list[int], float]:
    ordered = np.sort(eigenvalues)
    if not len(ordered):
        return [], 0.0
    sizes = [1]
    distinct_gaps: list[float] = []
    for left, right in zip(ordered, ordered[1:]):
        gap = float(abs(right - left))
        if gap <= tolerance:
            sizes[-1] += 1
        else:
            sizes.append(1)
            distinct_gaps.append(gap)
    return sizes, min(distinct_gaps, default=0.0)


@lru_cache(maxsize=None)
def audit_joint_spectra(half_degree: int) -> JointSpectrumFiniteControl:
    if half_degree not in (4, 5):
        raise ValueError("dense joint-spectrum controls are limited to m=4,5")
    charge_sets = [
        relative_charge_terms(rank, half_degree)
        for rank in range(2, half_degree + 1)
    ]
    irrational_weights = tuple(
        math.sqrt(prime) for prime in (2, 3, 5, 7, 11)[: len(charge_sets)]
    )
    dimensions: list[int] = []
    distinct_counts: list[int] = []
    distinct_fractions: list[float] = []
    maximum_multiplicity = 0
    simple_count = 0
    commutator_residual = 0.0
    minimum_gap = math.inf
    repeated_count = 0
    for partition in integer_partitions(2 * half_degree):
        _, _, _, repeated = exact_branching_commutant_dimension(
            partition,
            half_degree,
        )
        if not repeated:
            continue
        repeated_count += 1
        matrices = _average_matrices_for_sets(partition, charge_sets)
        dimension = matrices[0].shape[0]
        encoded = sum(
            (
                weight * matrix
                for weight, matrix in zip(irrational_weights, matrices)
            ),
            np.zeros_like(matrices[0]),
        )
        sizes, gap = _eigenvalue_cluster_sizes(np.linalg.eigvalsh(encoded))
        distinct = len(sizes)
        dimensions.append(dimension)
        distinct_counts.append(distinct)
        distinct_fractions.append(distinct / dimension)
        maximum_multiplicity = max(maximum_multiplicity, max(sizes))
        simple_count += int(all(size == 1 for size in sizes))
        if gap:
            minimum_gap = min(minimum_gap, gap)
        for left in range(len(matrices)):
            for right in range(left + 1, len(matrices)):
                commutator_residual = max(
                    commutator_residual,
                    float(
                        np.linalg.norm(
                            matrices[left] @ matrices[right]
                            - matrices[right] @ matrices[left]
                        )
                    ),
                )
    return JointSpectrumFiniteControl(
        half_degree=half_degree,
        repeated_partition_count=repeated_count,
        minimum_symmetric_irrep_dimension=min(dimensions),
        maximum_symmetric_irrep_dimension=max(dimensions),
        minimum_distinct_joint_eigenvalue_count=min(distinct_counts),
        maximum_distinct_joint_eigenvalue_count=max(distinct_counts),
        minimum_distinct_joint_eigenvalue_fraction=min(distinct_fractions),
        maximum_joint_eigenspace_multiplicity=maximum_multiplicity,
        simple_joint_spectrum_partition_count=simple_count,
        maximum_pairwise_matrix_commutator_residual=commutator_residual,
        minimum_observed_distinct_encoded_gap=(
            minimum_gap if math.isfinite(minimum_gap) else 0.0
        ),
        finite_numerical_control_only=True,
        status=(
            "nontrivial-degenerate-joint-gaudin-spectrum"
            if commutator_residual < 1e-9 and simple_count == 0
            else "pair-gaudin-joint-spectrum-control-failure"
        ),
    )


@lru_cache(maxsize=1)
def build_pair_gaudin_hierarchy_report() -> PairGaudinHierarchyReport:
    local = audit_infinitesimal_braid_relations()
    hierarchy = [audit_charge_hierarchy(value) for value in (3, 4, 5, 6, 8)]
    spectra = [audit_joint_spectra(value) for value in (4, 5)]
    hierarchy_exact = local.all_rank_local_relations_proved and all(
        row.charges_commute_pairwise
        and row.cumulative_equals_global_orbit_sum
        and row.cumulative_charge_commutes_with_final_K
        for row in hierarchy
    )
    all_incompatible = all(
        row.individual_charges_commuting_with_final_K_count == 0
        for row in hierarchy
    )
    finite_degenerate = all(
        row.simple_joint_spectrum_partition_count == 0 for row in spectra
    )
    theorem_verified = hierarchy_exact and all_incompatible and finite_degenerate
    theorem = PairGaudinHierarchyTheorem(
        local_interaction=(
            "c_ij is the eight-term sum of all 3-cycles on the endpoints of pair labels i,j."
        ),
        infinitesimal_braid_relations=(
            "Disjoint interactions commute and [c_ij,c_ik+c_jk]=0 on every triple."
        ),
        commuting_charges=(
            "J_r=sum_(i<r)c_ir commute pairwise, with exactly 8(r-1) permutation terms."
        ),
        cumulative_natural_charge=(
            "sum_r J_r is the support-three K_m-orbit sum whose normalized action has natural copy-space variance."
        ),
        compiler_opportunity=(
            "Use the joint Gaudin spectrum as an intermediate path basis for factorizing vertical commuting-square edges."
        ),
        final_K_boundary=(
            "Individual J_r break final pair-permutation symmetry and do not preserve K_m irrep labels; only their cumulative sum is K_m-invariant."
        ),
        exact_all_rank_commuting_hierarchy_proved=hierarchy_exact,
        polynomial_term_count_per_charge_proved=hierarchy_exact,
        cumulative_charge_has_natural_copy_variance_proved=hierarchy_exact,
        joint_spectrum_simple_on_all_finite_controls=False,
        charges_preserve_final_K_labels=False,
        vertical_multiplicity_edges_factored=False,
        connection_to_K_adapted_basis_compiled=False,
        source_aware_subduction_transform_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=theorem_verified,
        status=(
            "pair-gaudin-hierarchy-proved-K-adapted-connection-open"
            if theorem_verified
            else "pair-gaudin-hierarchy-control-failure"
        ),
    )
    delta_64 = normalized_commutator_squared_norm(64)
    return PairGaudinHierarchyReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "S_(2m) with m distinguished pairs",
            "range": "every integer m>=2",
            "charge_family": "J_r=sum_(i<r)c_ir, r=2,...,m",
            "claim_boundary": (
                "Exact commuting intermediate hierarchy; not a final K_m-adapted multiplicity basis."
            ),
        },
        local_control=local,
        hierarchy_controls=hierarchy,
        spectrum_controls=spectra,
        theorem=theorem,
        natural_variance_bridge={
            "normalized_cumulative_charge": "C_m/|C_m|",
            "source_variance_threshold_formula": "delta_m/8",
            "source_spectral_diameter_formula": "sqrt(delta_m/2)",
            "delta_formula": "(m-3)/[8 m^3 (m-2) (m-1)^3]",
            "m64_variance_threshold": delta_64 / 8,
            "m64_spectral_diameter_lower_bound": math.sqrt(delta_64 / 2),
            "proved_by": (
                "The parity-resolved local-commutator certificate plus ||[C,D]||_F^2<=4 min_a||C-aI||_F^2."
            ),
        },
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-GAUDIN-K-CONNECTION",
                "statement": (
                    "Derive a uniformly computable connection from joint J_r eigenspaces to K_m-adapted vertical-edge labels."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-GAUDIN-JOINT-GAPS",
                "statement": (
                    "Prove inverse-polynomial conditional gaps or bounded branching for the joint hierarchy on natural source mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-GAUDIN-DEGENERACY-COMPLETION",
                "statement": (
                    "Find additional commuting local charges that split the observed joint degeneracies without destroying efficient preparation."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Finite pairwise commutation is accidental.",
                "answer": (
                    "The two local infinitesimal braid identities imply [J_r,J_s]=0 algebraically at every rank."
                ),
                "resolved": True,
            },
            {
                "challenge": "The hierarchy may be unrelated to the natural commutant signal.",
                "answer": (
                    "Its exact cumulative sum is the natural-mass support-three charge with proved source variance."
                ),
                "resolved": True,
            },
            {
                "challenge": "Commuting polynomial charges already solve subduction.",
                "answer": (
                    "False: finite joint spectra retain degeneracy and individual charges fail to commute with final K_m."
                ),
                "resolved": True,
            },
            {
                "challenge": "Final K incompatibility makes the hierarchy useless.",
                "answer": (
                    "Not proved.  It makes the hierarchy an intermediate connection basis rather than a terminal label basis; the connection remains the decisive test."
                ),
                "resolved": False,
            },
        ],
        literature_links=[
            {
                "id": "arXiv:1001.2345",
                "role": (
                    "Odd Jucys-Murphy elements and hyperoctahedral Hecke algebra context; the present pair interactions are a distinct conjugation-commutant construction."
                ),
            },
            {
                "id": "arXiv:0710.4971",
                "role": "Gaudin limits, commuting algebras, and Gelfand-Tsetlin basis mechanisms."
            },
            {
                "id": "arXiv:0904.4854",
                "role": "Partial Jucys-Murphy locality and stable group-algebra filtrations."
            },
        ],
        headline_metrics={
            "all_rank_commuting_gaudin_hierarchy_count": int(hierarchy_exact),
            "polynomial_lcu_charge_family_count": int(hierarchy_exact),
            "natural_variance_cumulative_charge_count": int(hierarchy_exact),
            "finite_joint_spectrum_control_count": len(spectra),
            "finite_simple_joint_spectrum_count": sum(
                row.simple_joint_spectrum_partition_count for row in spectra
            ),
            "final_K_compatible_relative_charge_count": max(
                row.individual_charges_commuting_with_final_K_count
                for row in hierarchy
            ),
            "vertical_edge_factorization_count": 0,
            "K_adapted_connection_compiler_count": 0,
            "hidden_involution_detector_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_commuting_hierarchy_proved": hierarchy_exact,
            "each_charge_has_linear_term_count": hierarchy_exact,
            "cumulative_charge_has_natural_copy_variance": hierarchy_exact,
            "joint_hierarchy_resolves_all_finite_degeneracy": False,
            "relative_charges_preserve_final_K_labels": False,
            "K_adapted_connection_compiled": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A succinct commuting intermediate basis now exists, but its degenerate joint spectrum and incompatibility with final K labels leave the vertical-edge connection open."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved an all-rank linear-size pair-Gaudin charge hierarchy whose cumulative observable reaches natural copy-space variance; the K-adapted connection remains open."
        ),
        falsifiers_triggered=[
            "The support-three natural charge is not an isolated Hamiltonian; it is the aggregate of a full commuting hierarchy.",
            "The hierarchy is not already a final hyperoctahedral subduction basis.",
            "Finite joint spectra retain degeneracies, so extra charges or connection data are required."
        ],
    )


def write_pair_gaudin_hierarchy_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_pair_gaudin_hierarchy_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_pair_gaudin_hierarchy_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
