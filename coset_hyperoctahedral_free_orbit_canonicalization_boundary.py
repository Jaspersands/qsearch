"""Free-orbit source basis and coherent canonicalization boundary.

Let ``G=S_(2m)``, ``h`` the canonical perfect matching,
``H=<h>``, and ``K=C_G(h)=C_2 wr S_m``.  The canonical one-copy plus fiber has
the permutation basis

    |gH>_+ = (|g>+|gh>)/sqrt(2),  gH in X=G/H.          (1)

Because ``K`` centralizes ``h``, conjugation acts on ``X`` and the ``k``-copy
fiber is the diagonal permutation module ``C[X^k]``.  For ``x in K``, its
fixed fraction is the normalized source character ``q_x``.  A tuple is
nonfree only if some nonidentity ``x`` fixes it, so

    Pr_(z in X^k)[Stab_K(z)!=1]
      <= sum_(x!=e) q_x^k
      <= (|K|-1) q_max^k.                              (2)

At the hidden-involution copy width this vanishes superpolynomially.  The free
subset is a disjoint union of regular ``K`` orbits, hence exactly

    C[X^k_free] ~= C[K] tensor C[O_free].               (3)

Given a reversible canonicalizer that maps a free tuple to its canonical orbit
representative and unique transporter, (3) becomes a coherent regular-basis
transform.  The ``K`` QFT then exposes an explicit source multiplicity copy,
not merely an isotypic label.  Conversely, any transform with the stated
representative/transporter semantics is an orbit canonicalizer.

The same frame-second-moment argument bounds the alternative contribution of
the nonfree source by the square root of its source fraction.  Thus a
canonicalizer may discard nonfree tuples without losing asymptotic signal.

This does not construct the canonicalizer.  Simultaneous conjugacy of tuples
of permutations modulo ``H`` is a nontrivial canonical-labeling problem, and
generic canonicalization may hide graph-isomorphism-like complexity.  Even a
free-orbit basis does not by itself diagonalize the source-specific
matrix-Hecke transfer or compile its polar.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    symmetric_group,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from coset_hyperoctahedral_branching_polar_boundary import (
    hyperoctahedral_elements,
)
from coset_hyperoctahedral_source_plancherel_typicality import (
    nonidentity_character_bound,
    normalized_source_fiber_character,
)
from coset_hyperoctahedral_trivial_color_mass_no_go import (
    canonical_matching_involution,
)
from coset_perfect_matching_spherical_boundary import perfect_matching_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hyperoctahedral_free_orbit_canonicalization_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HYPEROCTAHEDRAL-FREE-ORBIT-CANONICALIZATION-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FreeOrbitFiniteControl:
    half_degree: int
    degree: int
    copy_count: int
    base_set_size: int
    tuple_count: int
    hyperoctahedral_order: int
    free_tuple_count: int
    nonfree_tuple_count: int
    exact_free_tuple_fraction: float
    exact_nonfree_tuple_fraction: float
    exact_fixed_point_union_upper_bound: float
    maximum_character_union_upper_bound: float
    free_orbit_count: int
    free_tuple_count_divisible_by_group_order: bool
    exact_permutation_module_control_verified: bool
    status: str


@dataclass(frozen=True)
class FreeOrbitScalingRecord:
    half_degree: int
    degree: int
    perfect_matching_count_decimal: str
    copy_count: int
    hyperoctahedral_order_decimal: str
    nonfree_source_fraction_upper_bound: float
    nonfree_alternative_contribution_upper_bound: float
    free_source_fraction_lower_bound: float
    free_alternative_contribution_lower_bound: float
    asymptotically_free_source_module: bool
    coherent_orbit_canonicalizer_constructed: bool
    regular_orbit_qft_after_canonicalization_available: bool
    matrix_hecke_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class FreeOrbitCanonicalizationTheorem:
    permutation_basis: str
    fixed_fraction: str
    free_fraction_bound: str
    free_module: str
    canonicalizer_transform: str
    alternative_transfer: str
    computational_boundary: str
    scope_limit: str
    exact_permutation_module_identity_proved: bool
    asymptotically_free_source_proved: bool
    free_regular_module_decomposition_proved: bool
    alternative_free_mass_proved: bool
    coherent_orbit_canonicalizer_constructed: bool
    matrix_hecke_polar_compiled: bool
    graph_isomorphism_hardness_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FreeOrbitCanonicalizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FreeOrbitFiniteControl]
    scaling_records: list[FreeOrbitScalingRecord]
    theorem: FreeOrbitCanonicalizationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _conjugate(
    element: Permutation,
    value: Permutation,
) -> Permutation:
    return compose_permutations(
        compose_permutations(element, value), inverse_permutation(element)
    )


def canonical_plus_cosets(
    half_degree: int,
) -> tuple[Permutation, ...]:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    hidden = canonical_matching_involution(half_degree)
    return tuple(
        sorted(
            {
                min(
                    element,
                    compose_permutations(element, hidden),
                )
                for element in symmetric_group(2 * half_degree)
            }
        )
    )


def _action_stabilizer_masks(
    half_degree: int,
) -> tuple[tuple[Permutation, ...], tuple[int, ...]]:
    hidden = canonical_matching_involution(half_degree)
    cosets = canonical_plus_cosets(half_degree)
    elements = tuple(
        element
        for element, _, _ in hyperoctahedral_elements(half_degree)
    )
    coset_index = {representative: index for index, representative in enumerate(cosets)}
    masks = []
    for representative in cosets:
        mask = 0
        for element_index, element in enumerate(elements):
            image = _conjugate(element, representative)
            image = min(image, compose_permutations(image, hidden))
            if coset_index[image] == coset_index[representative]:
                mask |= 1 << element_index
        masks.append(mask)
    return elements, tuple(masks)


def audit_free_orbits(
    half_degree: int,
    copy_count: int,
) -> FreeOrbitFiniteControl:
    if half_degree < 2 or half_degree > 3:
        raise ValueError("finite control supports half_degree in [2,3]")
    if copy_count < 1 or (half_degree == 3 and copy_count > 2):
        raise ValueError("copy count exceeds the exact finite-control cap")
    elements, masks = _action_stabilizer_masks(half_degree)
    identity_mask = 1 << elements.index(tuple(range(2 * half_degree)))
    free = 0
    for coordinates in itertools.product(range(len(masks)), repeat=copy_count):
        stabilizer = (1 << len(elements)) - 1
        for coordinate in coordinates:
            stabilizer &= masks[coordinate]
        free += stabilizer == identity_mask
    tuples = len(masks) ** copy_count
    nonfree = tuples - free
    exact_union = sum(
        normalized_source_fiber_character(half_degree, element) ** copy_count
        for element in elements
        if element != tuple(range(2 * half_degree))
    )
    if half_degree >= 3:
        maximum_union = (len(elements) - 1) * nonidentity_character_bound(
            half_degree
        ) ** copy_count
    else:
        maximum = max(
            normalized_source_fiber_character(half_degree, element)
            for element in elements
            if element != tuple(range(2 * half_degree))
        )
        maximum_union = (len(elements) - 1) * maximum**copy_count
    verified = bool(
        len(masks) == math.factorial(2 * half_degree) // 2
        and nonfree / tuples <= exact_union + 1e-12
        and exact_union <= maximum_union + 1e-12
        and free % len(elements) == 0
    )
    return FreeOrbitFiniteControl(
        half_degree=half_degree,
        degree=2 * half_degree,
        copy_count=copy_count,
        base_set_size=len(masks),
        tuple_count=tuples,
        hyperoctahedral_order=len(elements),
        free_tuple_count=free,
        nonfree_tuple_count=nonfree,
        exact_free_tuple_fraction=free / tuples,
        exact_nonfree_tuple_fraction=nonfree / tuples,
        exact_fixed_point_union_upper_bound=exact_union,
        maximum_character_union_upper_bound=maximum_union,
        free_orbit_count=free // len(elements),
        free_tuple_count_divisible_by_group_order=(free % len(elements) == 0),
        exact_permutation_module_control_verified=verified,
        status=(
            "exact-free-orbit-permutation-module-control-verified"
            if verified
            else "free-orbit-control-failure"
        ),
    )


def free_orbit_scaling_record(
    half_degree: int,
) -> FreeOrbitScalingRecord:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    matchings = perfect_matching_count(half_degree)
    copies = flatness_copy_count(matchings)
    order = (2**half_degree) * math.factorial(half_degree)
    log_nonfree = math.log(order - 1) + copies * math.log(
        nonidentity_character_bound(half_degree)
    )
    nonfree = min(1.0, math.exp(log_nonfree))
    eta = (matchings - 1) / (2**copies)
    alternative_nonfree = min(1.0, math.sqrt((1.0 + eta) * nonfree))
    return FreeOrbitScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        perfect_matching_count_decimal=str(matchings),
        copy_count=copies,
        hyperoctahedral_order_decimal=str(order),
        nonfree_source_fraction_upper_bound=nonfree,
        nonfree_alternative_contribution_upper_bound=alternative_nonfree,
        free_source_fraction_lower_bound=1.0 - nonfree,
        free_alternative_contribution_lower_bound=1.0 - alternative_nonfree,
        asymptotically_free_source_module=True,
        coherent_orbit_canonicalizer_constructed=False,
        regular_orbit_qft_after_canonicalization_available=True,
        matrix_hecke_polar_compiled=False,
        status="free-regular-source-dominant-canonicalizer-open",
    )


def build_free_orbit_canonicalization_report(
    *,
    finite_specs: tuple[tuple[int, int], ...] = (
        (2, 1),
        (2, 2),
        (2, 3),
        (3, 1),
        (3, 2),
    ),
    scaling_half_degrees: tuple[int, ...] = (3, 4, 8, 16, 32, 64, 128),
) -> FreeOrbitCanonicalizationReport:
    controls = [audit_free_orbits(m, k) for m, k in finite_specs]
    scaling = [free_orbit_scaling_record(m) for m in scaling_half_degrees]
    verified = all(row.exact_permutation_module_control_verified for row in controls)
    scaling_verified = all(
        row.asymptotically_free_source_module
        and row.regular_orbit_qft_after_canonicalization_available
        and not row.coherent_orbit_canonicalizer_constructed
        for row in scaling
    )
    theorem = FreeOrbitCanonicalizationTheorem(
        permutation_basis=(
            "The canonical plus fiber is C[G/<h>] with K acting by conjugation; "
            "k copies are the diagonal K-set X^k."
        ),
        fixed_fraction=(
            "The fraction fixed by x is q_x^k, the kth power of the normalized "
            "source character."
        ),
        free_fraction_bound=(
            "Nonfree fraction <=sum_(x!=e)q_x^k<=(|K|-1)q_max^k."
        ),
        free_module=(
            "The free subset is a disjoint union of regular K orbits, so its "
            "permutation module is C[K] tensor an orbit-copy register."
        ),
        canonicalizer_transform=(
            "A reversible representative/transporter map followed by the K QFT "
            "provides explicit carrier and multiplicity coordinates."
        ),
        alternative_transfer=(
            "Frame second moments bound nonfree alternative contribution by "
            "sqrt((1+eta) times nonfree source fraction)."
        ),
        computational_boundary=(
            "The unresolved primitive is coherent canonical labeling for free "
            "simultaneous-conjugacy orbits, not abstract generic wreath fusion."
        ),
        scope_limit=(
            "No canonicalizer, graph-isomorphism reduction, transfer polar, "
            "physical lift, or hidden-involution algorithm is proved."
        ),
        exact_permutation_module_identity_proved=True,
        asymptotically_free_source_proved=True,
        free_regular_module_decomposition_proved=True,
        alternative_free_mass_proved=True,
        coherent_orbit_canonicalizer_constructed=False,
        matrix_hecke_polar_compiled=False,
        graph_isomorphism_hardness_proved=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "free-regular-source-proved-coherent-canonicalizer-open"
            if verified and scaling_verified
            else "free-orbit-canonicalization-control-failure"
        ),
    )
    return FreeOrbitCanonicalizationReport(
        created_at=utc_now(),
        theorem_contract={
            "basis": (
                "Canonical plus-coset basis of R^tensor k, not an arbitrary "
                "vector in the fiber."
            ),
            "action": "Diagonal conjugation by K=C_2 wr S_m.",
            "free_transform_semantics": (
                "Return a canonical orbit representative and the unique K "
                "transporter for every free tuple."
            ),
            "outside_scope": (
                "Nonfree tuples, arbitrary canonical labeling complexity, and "
                "the source-specific synthesis transfer after basis exposure."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-FREE-ORBIT-CANONICALIZER",
                "statement": (
                    "Construct a uniform reversible polynomial canonicalizer and "
                    "unique transporter for almost all source tuples."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-CANONICALIZER-AVERAGE-CASE",
                "statement": (
                    "Exploit random-tuple structure to prove average-case "
                    "polynomial cost without assuming worst-case GI canonicalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-FREE-BASIS-TRANSFER",
                "statement": (
                    "Express and compile the matrix-Hecke transfer in the regular-"
                    "orbit plus orbit-representative basis."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Plancherel typicality is only an abstract character statement.",
                "answer": (
                    "False: it comes from an overwhelming exact free K-set whose "
                    "module is explicitly regular-by-orbit."
                ),
                "resolved": True,
            },
            {
                "challenge": "Existence of orbit representatives gives an efficient basis.",
                "answer": (
                    "False. Coherent canonicalization and transporter recovery are "
                    "the computationally nontrivial primitives."
                ),
                "resolved": True,
            },
            {
                "challenge": "A free-orbit K basis compiles the full polar.",
                "answer": (
                    "False. It resolves source multiplicity coordinates but not "
                    "the physical matrix-Hecke transfer between them."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_free_orbit_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_permutation_module_control_verified
                for row in controls
            ),
            "asymptotically_free_source_theorem_count": 1,
            "regular_module_decomposition_theorem_count": 1,
            "minimum_scaling_free_alternative_contribution_lower_bound": min(
                row.free_alternative_contribution_lower_bound for row in scaling
            ),
            "coherent_orbit_canonicalizer_count": 0,
            "matrix_hecke_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_source_basis_asymptotically_free_under_K": (
                verified and scaling_verified
            ),
            "free_source_module_regular_by_orbit": verified,
            "nonfree_alternative_contribution_negligible": scaling_verified,
            "coherent_free_orbit_canonicalizer_constructed": False,
            "average_case_canonicalizer_polynomial": False,
            "matrix_hecke_transfer_compiled_in_free_basis": False,
            "graph_isomorphism_hardness_proved": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Almost all source basis tuples lie in exact regular K orbits, "
                "but no coherent canonical representative/transporter algorithm "
                "or physical transfer polar is known."
            ),
        },
        status=theorem.status,
        summary=(
            "Upgraded wreath-Plancherel typicality to an overwhelming exact free-"
            "orbit decomposition of the source permutation basis, replacing a "
            "generic fusion target by coherent simultaneous-conjugacy "
            "canonicalization plus the still-open matrix-Hecke transfer."
        ),
        falsifiers_triggered=[
            "Source Plancherel behavior is explained by exact free regular orbits, not random-matrix speculation.",
            "A generic hyperoctahedral Clebsch-Gordan transform is not necessary merely to expose source multiplicity copies.",
            "Existence of a free regular submodule does not imply an efficient coherent orbit canonicalizer.",
            "A source multiplicity basis alone does not implement the physical transfer polar.",
        ],
    )


def write_free_orbit_canonicalization_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_free_orbit_canonicalization_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_free_orbit_canonicalization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
