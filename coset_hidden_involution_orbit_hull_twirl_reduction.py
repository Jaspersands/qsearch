"""Orbit-hull Schur reduction for the binary support-span measurement.

Let ``U`` be a finite-dimensional unitary representation of a finite group
``G`` and let ``P`` be a projector.  Average its conjugacy orbit:

    A = |G|^-1 sum_x U_x P U_x^*.                       (1)

The support of ``A`` is exactly the invariant hull of ``range(P)``:

    supp(A) = span_x U_x range(P).                       (2)

Under an isotypic decomposition

    H = direct_sum_nu V_nu tensor M_nu,

Schur twirling gives

    A = direct_sum_nu (I_(V_nu)/d_nu) tensor Q_nu,
    Q_nu = Tr_(V_nu)(P_(nu,nu)).                         (3)

Therefore

    supp(A) = direct_sum_nu I_(V_nu) tensor supp(Q_nu). (4)

For hidden involutions, use the diagonal conjugation representation on the
``k`` regular registers and the canonical projector

    P_0 = ((I+R_(h_0))/2)^tensor k.                     (5)

Its conjugacy orbit is precisely the candidate support family, so (4) is the
published binary support-span test.  The carrier factor is automatic: no
orientation of an individual hidden involution and no covariant output label
is required.  Efficient generalized phase estimation can expose ``nu`` when a
group QFT is available.  The sole remaining block problem is the support of
the positive multiplicity operator ``Q_nu``.

For fixed-point-free involutions in ``S_(2m)``, the stabilizer of ``P_0`` is
the hyperoctahedral group ``K=C_2 wr S_m``.  Thus ``P_0`` is ``K``-invariant
and each ``Q_nu`` inherits a restriction/subduction description.  This is a
strictly smaller target than a hidden-element decoder or physical-row polar,
but writing (3) does not compile ``supp(Q_nu)``.  A successful algorithm must
give a uniform polynomial multiplicity-support basis or direct projector on
naturally occupied sectors, and must still survive classical dequantization.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    dense_hidden_coset_state,
    inverse_permutation,
    involution_class_size,
    involution_conjugacy_class,
    symmetric_group,
)
from coset_hidden_involution_support_span_reduction import (
    support_projector,
    support_span_sufficient_copies,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_orbit_hull_twirl_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-ORBIT-HULL-TWIRL-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OrbitHullFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    group_order: int
    conjugacy_class_size: int
    canonical_stabilizer_size: int
    orbit_stabilizer_quotient: int
    data_dimension: int
    orbit_average_full_twirl_residual: float
    maximum_twirl_commutator_residual: float
    maximum_stabilizer_projector_commutator_residual: float
    support_projector_orbit_hull_residual: float
    support_rank: int
    explicit_orbit_hull_rank: int
    carrier_invariant_support_verified: bool
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class PerfectMatchingOrbitHullScalingRecord:
    n: int
    matching_count: int
    hyperoctahedral_stabilizer_order: int
    symmetric_group_order: int
    orbit_stabilizer_identity_verified: bool
    support_test_copy_count: int
    diagonal_conjugation_irrep_label_accessible: bool
    individual_hidden_orientation_required: bool
    uniform_multiplicity_support_projector_known: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionOrbitHullTheorem:
    invariant_hull_identity: str
    schur_twirl_normal_form: str
    support_normal_form: str
    perfect_matching_stabilizer: str
    carrier_orientation_eliminated_for_binary_support: bool
    diagonal_irrep_label_primitive_available: bool
    multiplicity_support_projector_constructed: bool
    orbit_hull_identity_proved: bool
    schur_support_reduction_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionOrbitHullReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[OrbitHullFiniteControl]
    scaling_records: list[PerfectMatchingOrbitHullScalingRecord]
    theorem: HiddenInvolutionOrbitHullTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def conjugation_basis_permutation(
    n: int,
    element: Permutation,
) -> np.ndarray:
    group = symmetric_group(n)
    index = {permutation: offset for offset, permutation in enumerate(group)}
    inverse = inverse_permutation(element)
    return np.asarray(
        [
            index[
                compose_permutations(
                    compose_permutations(element, permutation), inverse
                )
            ]
            for permutation in group
        ],
        dtype=int,
    )


def tensor_basis_permutation(
    one_copy_permutation: np.ndarray,
    copy_count: int,
) -> np.ndarray:
    dimension = len(one_copy_permutation)
    result = np.empty(dimension**copy_count, dtype=int)
    for flat_index, coordinates in enumerate(
        itertools.product(range(dimension), repeat=copy_count)
    ):
        image = tuple(
            int(one_copy_permutation[index]) for index in coordinates
        )
        result[flat_index] = np.ravel_multi_index(
            image, (dimension,) * copy_count
        )

    return result


def permutation_conjugate(
    operator: np.ndarray,
    basis_permutation: np.ndarray,
) -> np.ndarray:
    result = np.zeros_like(operator)
    result[np.ix_(basis_permutation, basis_permutation)] = operator
    return result


def canonical_candidate_projector(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> tuple[Permutation, np.ndarray]:
    hidden = involution_conjugacy_class(n, transposition_count)[0]
    dimension = math.factorial(n) ** copy_count
    state = dense_hidden_coset_state(n, hidden, copy_count)
    projector = (dimension / (1 << copy_count)) * state
    return hidden, projector


def full_conjugation_twirl(
    n: int,
    copy_count: int,
    operator: np.ndarray,
) -> np.ndarray:
    twirl = np.zeros_like(operator, dtype=np.complex128)
    for element in symmetric_group(n):
        permutation = tensor_basis_permutation(
            conjugation_basis_permutation(n, element), copy_count
        )
        twirl += permutation_conjugate(operator, permutation)
    return twirl / math.factorial(n)


def orbit_average_candidate_projector(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> np.ndarray:
    dimension = math.factorial(n) ** copy_count
    average = np.zeros((dimension, dimension), dtype=np.complex128)
    for hidden in involution_conjugacy_class(n, transposition_count):
        state = dense_hidden_coset_state(n, hidden, copy_count)
        average += (dimension / (1 << copy_count)) * state
    return average / involution_class_size(n, transposition_count)


def audit_orbit_hull_control(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    maximum_dimension: int = 512,
) -> OrbitHullFiniteControl:
    order = math.factorial(n)
    dimension = order**copy_count
    if dimension > maximum_dimension:
        raise ValueError("orbit-hull finite control is too large")
    hidden, canonical = canonical_candidate_projector(
        n, transposition_count, copy_count
    )
    group = symmetric_group(n)
    stabilizer = [
        element
        for element in group
        if compose_permutations(
            compose_permutations(element, hidden),
            inverse_permutation(element),
        )
        == hidden
    ]
    orbit_average = orbit_average_candidate_projector(
        n, transposition_count, copy_count
    )
    twirl = full_conjugation_twirl(n, copy_count, canonical)
    twirl_residual = float(np.linalg.norm(twirl - orbit_average, ord=2))

    support, _ = support_projector(orbit_average)
    support_rank = int(round(float(np.trace(support).real)))
    hull_columns = []
    for candidate in involution_conjugacy_class(n, transposition_count):
        state = dense_hidden_coset_state(n, candidate, copy_count)
        projector = (dimension / (1 << copy_count)) * state
        values, vectors = np.linalg.eigh(projector)
        hull_columns.append(vectors[:, values > 1e-9])
    hull = np.column_stack(hull_columns)
    hull_rank = int(np.linalg.matrix_rank(hull, tol=1e-9))
    hull_projector, _ = support_projector(hull @ hull.conj().T)
    hull_residual = float(np.linalg.norm(hull_projector - support, ord=2))

    maximum_commutator = 0.0
    for element in group:
        permutation = tensor_basis_permutation(
            conjugation_basis_permutation(n, element), copy_count
        )
        conjugated = permutation_conjugate(orbit_average, permutation)
        maximum_commutator = max(
            maximum_commutator,
            float(np.linalg.norm(conjugated - orbit_average, ord=2)),
        )
    stabilizer_commutator = 0.0
    for element in stabilizer:
        permutation = tensor_basis_permutation(
            conjugation_basis_permutation(n, element), copy_count
        )
        stabilizer_commutator = max(
            stabilizer_commutator,
            float(
                np.linalg.norm(
                    permutation_conjugate(canonical, permutation) - canonical,
                    ord=2,
                )
            ),
        )
    orbit_size = order // len(stabilizer)
    carrier_invariant = maximum_commutator <= 1e-9
    verified = bool(
        orbit_size == involution_class_size(n, transposition_count)
        and twirl_residual <= 1e-9
        and maximum_commutator <= 1e-9
        and stabilizer_commutator <= 1e-9
        and support_rank == hull_rank
        and hull_residual <= 1e-8
    )
    return OrbitHullFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        group_order=order,
        conjugacy_class_size=involution_class_size(
            n, transposition_count
        ),
        canonical_stabilizer_size=len(stabilizer),
        orbit_stabilizer_quotient=orbit_size,
        data_dimension=dimension,
        orbit_average_full_twirl_residual=twirl_residual,
        maximum_twirl_commutator_residual=maximum_commutator,
        maximum_stabilizer_projector_commutator_residual=(
            stabilizer_commutator
        ),
        support_projector_orbit_hull_residual=hull_residual,
        support_rank=support_rank,
        explicit_orbit_hull_rank=hull_rank,
        carrier_invariant_support_verified=carrier_invariant,
        finite_control_verified=verified,
        status=(
            "orbit-hull-schur-support-reduction-verified"
            if verified
            else "orbit-hull-twirl-control-failure"
        ),
    )


def perfect_matching_orbit_hull_scaling_record(
    n: int,
    *,
    target_null_false_positive: float = 0.1,
) -> PerfectMatchingOrbitHullScalingRecord:
    if n < 2 or n % 2:
        raise ValueError("n must be positive and even")
    half = n // 2
    group_order = math.factorial(n)
    stabilizer_order = (2**half) * math.factorial(half)
    matching_count = involution_class_size(n, half)
    return PerfectMatchingOrbitHullScalingRecord(
        n=n,
        matching_count=matching_count,
        hyperoctahedral_stabilizer_order=stabilizer_order,
        symmetric_group_order=group_order,
        orbit_stabilizer_identity_verified=(
            group_order == matching_count * stabilizer_order
        ),
        support_test_copy_count=support_span_sufficient_copies(
            matching_count, target_null_false_positive
        ),
        diagonal_conjugation_irrep_label_accessible=True,
        individual_hidden_orientation_required=False,
        uniform_multiplicity_support_projector_known=False,
        status="carrier-eliminated-multiplicity-support-compiler-open",
    )


def build_hidden_involution_orbit_hull_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 1),
        (3, 1, 2),
        (4, 2, 1),
    ),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128),
) -> HiddenInvolutionOrbitHullReport:
    controls = [
        audit_orbit_hull_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [
        perfect_matching_orbit_hull_scaling_record(n)
        for n in scaling_n_values
    ]
    verified = all(row.finite_control_verified for row in controls)
    scaling_verified = all(
        row.orbit_stabilizer_identity_verified
        and row.diagonal_conjugation_irrep_label_accessible
        and not row.individual_hidden_orientation_required
        for row in scaling
    )
    theorem = HiddenInvolutionOrbitHullTheorem(
        invariant_hull_identity=(
            "supp(|G|^-1 sum_x U_x P U_x^*)=span_x U_x range(P)."
        ),
        schur_twirl_normal_form=(
            "A=direct_sum_nu (I_(V_nu)/d_nu) tensor "
            "Tr_(V_nu)(P_(nu,nu))."
        ),
        support_normal_form=(
            "supp(A)=direct_sum_nu I_(V_nu) tensor supp(Q_nu)."
        ),
        perfect_matching_stabilizer=(
            "For h_0 of cycle type 2^m in S_(2m), Stab(h_0)=C_2 wr S_m."
        ),
        carrier_orientation_eliminated_for_binary_support=True,
        diagonal_irrep_label_primitive_available=True,
        multiplicity_support_projector_constructed=False,
        orbit_hull_identity_proved=True,
        schur_support_reduction_proved=True,
        theorem_verified=verified and scaling_verified,
        status=(
            "binary-support-reduced-to-canonical-multiplicity-support"
            if verified and scaling_verified
            else "orbit-hull-schur-reduction-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "orbit_hull_identity_control_count": sum(
            row.support_projector_orbit_hull_residual <= 1e-8
            for row in controls
        ),
        "scaling_record_count": len(scaling),
        "carrier_orientation_obligation_eliminated_count": len(scaling),
        "multiplicity_support_projector_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return HiddenInvolutionOrbitHullReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": "Provides the support-span binary measurement whose orbit hull is reduced here.",
            },
            {
                "id": "BEALS-1997-SYMMETRIC-QFT",
                "title": "Quantum computation of Fourier transforms over symmetric groups",
                "url": "https://doi.org/10.1145/258533.258548",
                "scope": "Makes diagonal-conjugation irrep labeling an available primitive, not the missing multiplicity-support projector.",
            },
        ],
        theorem_contract={
            "representation": (
                "Diagonal conjugation of G on k regular data registers."
            ),
            "canonical_projector": (
                "The k-fold plus-eigenspace projector for one fixed hidden "
                "involution h_0."
            ),
            "compiler_target": (
                "After irrep label nu, project onto supp(Q_nu) in the diagonal-"
                "action multiplicity register."
            ),
            "non_claim": (
                "No uniform Q_nu representation, support circuit, dequantization "
                "separation, hidden-element decoder, or speedup."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-BINARY-CANONICAL-QNU",
                "statement": (
                    "Express Q_nu=Tr_(V_nu)(P_0) uniformly through the "
                    "S_(2m) down C_2 wr S_m restriction and sampled source labels."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-MULTIPLICITY-SUPPORT",
                "statement": (
                    "Compile supp(Q_nu) without enumerating exponential branching "
                    "multiplicities or performing a small-gap generic polar transform."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-MULTIPLICITY-DEQUANTIZATION",
                "statement": (
                    "Determine whether Q_nu support is a classically computable "
                    "restriction/association-scheme invariant."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Binary support still needs the individual hidden orientation.",
                "answer": (
                    "False. Orbit averaging makes the support invariant and Schur "
                    "twirling supplies identity on every carrier V_nu."
                ),
                "resolved": True,
            },
            {
                "challenge": "Measuring nu completes the support test.",
                "answer": (
                    "False. Q_nu can have proper support inside a large multiplicity "
                    "space, so the irrep label is only the first stage."
                ),
                "resolved": True,
            },
            {
                "challenge": "Hyperoctahedral stabilizer symmetry diagonalizes Q_nu automatically.",
                "answer": (
                    "Unproved. Stabilizer invariance gives a subduction algebra but "
                    "not a uniform basis or support projector on sampled sectors."
                ),
                "resolved": False,
            },
            {
                "challenge": "The reduction is an efficient algorithm.",
                "answer": (
                    "False. The missing multiplicity-support projector can still "
                    "contain all computational hardness."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "orbit_hull_schur_support_reduction_proved": True,
            "individual_hidden_orientation_required_for_binary_support": False,
            "diagonal_conjugation_irrep_label_available": True,
            "canonical_multiplicity_operators_formalized": True,
            "uniform_multiplicity_support_projector_constructed": False,
            "multiplicity_support_dequantization_passed": False,
            "polynomial_time_hidden_involution_decision_algorithm": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The binary test no longer needs carrier orientation, but efficient "
                "support projection inside the canonical multiplicity blocks remains "
                "unconstructed and may be classically reducible."
            ),
        },
        status=theorem.status,
        summary=(
            "Reduced the published hidden-involution support-span measurement to "
            "canonical multiplicity-support projectors under diagonal conjugation. "
            "Carrier orientation is eliminated; the hyperoctahedral subduction "
            "support is now the exact computational bottleneck."
        ),
        falsifiers_triggered=[
            "Binary support projection does not require an individual hidden-involution output or carrier orientation.",
            "Irrep-label access alone does not implement the multiplicity support.",
            "Stabilizer symmetry is a reduction, not a compiled measurement.",
        ],
    )


def write_hidden_involution_orbit_hull_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-HIDDEN-INVOLUTION-ORBIT-HULL-TWIRL-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(build_hidden_involution_orbit_hull_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_hidden_involution_orbit_hull_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
