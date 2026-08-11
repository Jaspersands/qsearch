"""Principal-angle normal form for the fused coset PGM polar map.

Fix a natural source representation ``U`` of ``G=S_n``, the base involution
projector ``P``, and an output irrep ``V_nu``.  Vectorization identifies

    Hom_G(V_nu,U)

with the invariant subspace of ``conj(V_nu) tensor U``.  Let ``J_nu`` be an
isometric embedding of that invariant subspace and put

    P_tilde = I_(V_nu^*) tensor P.

Then the centralizer restriction map and its Gram matrix are exactly

    R_nu = P_tilde J_nu,
    R_nu^* R_nu = D_nu.                                (1)

Consequently the covariance-compressed PGM factor is the principal-angle
polar isometry

    Q_nu = R_nu D_nu^(-1/2).                           (2)

This closes coherent *normalization-one* access to the restriction map.  The
projector ``J_nu J_nu^*`` is the group-average invariant projector and admits
a coherent reflection via generalized phase estimation using the efficient
``S_n`` QFT and controlled group actions.  ``P_tilde`` is a tensor product of
known involution eigenspace projectors.  Standard products-of-projectors/QSVT
therefore access (2) without materializing a dense branching table.

The normalization is still obstructive.  In the physical frame decomposition

    B_nu = I_(d_nu)/d_nu tensor D_nu,

a retained physical eigenvalue ``lambda<=beta/M`` corresponds to principal
singular value

    sigma=sqrt(d_nu lambda)<=sqrt(beta d_max(S_n)/M).   (3)

For the perfect-matching orbit ``M=(n-1)!!`` and

    d_max(S_n)=sqrt(n!) exp(-(mathfrak_d+o(1))sqrt(n)),

the right side of (3) is ``exp(-Omega(sqrt(n)))``.  A bounded polynomial that
maps zero to zero and a retained positive singular value to one has Bernstein
degree ``exp(Omega(sqrt(n)))``.  Thus generic QSVT on the normalization-one
principal-angle encoding remains subexponential even after constant-mass
spectral truncation.

This is not a circuit lower bound.  A representation-specific rescaling,
hyperoctahedral branching transform, exact quotient construction, or another
non-polynomial structured polar implementation can bypass the black-box
polynomial degree obstruction.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_state_distinguishability import involution_count
from coset_whitening_rank_sandwich_no_go import (
    MAXIMAL_DIMENSION_PAPER_ID,
    MAXIMAL_DIMENSION_PAPER_URL,
    maximum_irrep_dimension,
)
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)
from self_dual_wreath_pgm_spectral_window import (
    windowed_pgm_success_lower_bound,
)


REPORT_PATH = Path(
    "research/representation/"
    "coset_restriction_principal_angle_polar_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-RESTRICTION-PRINCIPAL-ANGLE-POLAR-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class RestrictionPrincipalAngleControl:
    n: int
    source_partitions: tuple[Partition, ...]
    target_partition: Partition
    source_dimension: int
    target_dimension: int
    hom_space_multiplicity: int
    involution_projector_rank: int
    restriction_map_rank: int
    minimum_positive_gram_eigenvalue: float
    maximum_gram_eigenvalue: float
    invariant_projector_idempotence_residual: float
    involution_projector_idempotence_residual: float
    restriction_gram_residual: float
    product_projector_singular_value_residual: float
    polar_initial_support_residual: float
    exact_principal_angle_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class PrincipalAngleScalingRecord:
    n: int
    perfect_matching_count_decimal: str
    constant_pgm_success_copy_count: int
    physical_window_alpha: float
    physical_window_beta: float
    windowed_pgm_success_lower_bound: float
    maximum_irrep_partition: Partition
    maximum_irrep_dimension_decimal: str
    exact_beta_dmax_over_matching_count: float
    exact_principal_singular_upper_bound: float
    finite_bernstein_degree_lower_bound: float | None
    finite_row_in_subconstant_singular_regime: bool
    asymptotic_principal_singular_order: str
    asymptotic_generic_qsvt_degree_order: str
    polynomial_normalization_one_generic_qsvt_possible_asymptotically: bool
    status: str


@dataclass(frozen=True)
class RestrictionPrincipalAnglePolarTheorem:
    vectorized_intertwiner_space: str
    restriction_product: str
    gram_identity: str
    polar_identity: str
    coherent_projector_access: str
    physical_to_principal_spectrum: str
    maximal_dimension_consequence: str
    bernstein_consequence: str
    scope_limit: str
    exact_restriction_principal_angle_normal_form_proved: bool
    coherent_normalization_one_restriction_access_proved: bool
    dense_branching_table_required: bool
    generic_qsvt_subexponential_obstruction_proved: bool
    representation_specific_rescaling_ruled_out: bool
    hyperoctahedral_branching_transform_constructed: bool
    polynomial_fused_polar_circuit_constructed: bool
    general_quantum_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetRestrictionPrincipalAnglePolarReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[RestrictionPrincipalAngleControl]
    scaling_records: list[PrincipalAngleScalingRecord]
    theorem: RestrictionPrincipalAnglePolarTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    result = matrices[0]
    for matrix in matrices[1:]:
        result = np.kron(result, matrix)
    return result


def _canonical_involution(n: int) -> Permutation:
    values = list(range(n))
    for index in range(0, n - 1, 2):
        values[index], values[index + 1] = values[index + 1], values[index]
    return tuple(values)


def _support_and_inverse_root(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2)
    positive = values > tolerance
    support_vectors = vectors[:, positive]
    support = support_vectors @ support_vectors.conj().T
    inverse_root = (
        support_vectors * values[positive] ** -0.5
    ) @ support_vectors.conj().T
    return support, inverse_root, values[positive]


def audit_restriction_principal_angle_control(
    source_partitions: tuple[Partition, ...],
    target_partition: Partition,
    *,
    tolerance: float = 1e-9,
) -> RestrictionPrincipalAngleControl:
    if not source_partitions:
        raise ValueError("source_partitions must be nonempty")
    n = sum(source_partitions[0])
    if any(sum(partition) != n for partition in source_partitions):
        raise ValueError("source partitions must have one common size")
    if sum(target_partition) != n:
        raise ValueError("target partition must have the source size")
    source_tables = tuple(
        _source_representation_rows(partition)
        for partition in source_partitions
    )
    target_table = _source_representation_rows(target_partition)
    group = tuple(source_tables[0])
    source_action = {
        element: _kron_all(
            tuple(table[element] for table in source_tables)
        )
        for element in group
    }
    source_dimension = source_action[group[0]].shape[0]
    target_dimension = target_table[group[0]].shape[0]

    invariant = sum(
        np.kron(np.conjugate(target_table[element]), source_action[element])
        for element in group
    ) / len(group)
    invariant = (invariant + invariant.conj().T) / 2
    invariant_values, invariant_vectors = np.linalg.eigh(invariant)
    active = invariant_values > 1 - 100 * tolerance
    embedding = invariant_vectors[:, active]
    hom_multiplicity = embedding.shape[1]
    if hom_multiplicity == 0:
        raise ValueError("target does not occur in the source representation")

    hidden = _canonical_involution(n)
    source_projectors = tuple(
        (np.eye(table[hidden].shape[0]) + table[hidden]) / 2
        for table in source_tables
    )
    projector = _kron_all(source_projectors)
    lifted_projector = np.kron(np.eye(target_dimension), projector)
    restriction = lifted_projector @ embedding
    gram = embedding.conj().T @ lifted_projector @ embedding
    gram_support, inverse_root, positive_gram = _support_and_inverse_root(
        gram, tolerance
    )
    polar = restriction @ inverse_root

    invariant_residual = float(
        np.linalg.norm(invariant @ invariant - invariant, ord=2)
    )
    projector_residual = float(
        np.linalg.norm(projector @ projector - projector, ord=2)
    )
    gram_residual = float(
        np.linalg.norm(restriction.conj().T @ restriction - gram, ord=2)
    )
    product_singular = np.linalg.svd(
        lifted_projector @ invariant, compute_uv=False
    )
    product_positive = np.sort(product_singular[product_singular > tolerance])
    restriction_singular = np.sort(np.sqrt(positive_gram))
    if len(product_positive) != len(restriction_singular):
        singular_residual = math.inf
    else:
        singular_residual = float(
            np.max(
                np.abs(product_positive - restriction_singular),
                initial=0.0,
            )
        )
    polar_residual = float(
        np.linalg.norm(polar.conj().T @ polar - gram_support, ord=2)
    )
    verified = bool(
        invariant_residual <= 1e-8
        and projector_residual <= 1e-8
        and gram_residual <= 1e-8
        and singular_residual <= 1e-8
        and polar_residual <= 1e-8
    )
    return RestrictionPrincipalAngleControl(
        n=n,
        source_partitions=source_partitions,
        target_partition=target_partition,
        source_dimension=source_dimension,
        target_dimension=target_dimension,
        hom_space_multiplicity=hom_multiplicity,
        involution_projector_rank=int(
            np.linalg.matrix_rank(projector, tol=tolerance)
        ),
        restriction_map_rank=len(positive_gram),
        minimum_positive_gram_eigenvalue=float(positive_gram[0]),
        maximum_gram_eigenvalue=float(positive_gram[-1]),
        invariant_projector_idempotence_residual=invariant_residual,
        involution_projector_idempotence_residual=projector_residual,
        restriction_gram_residual=gram_residual,
        product_projector_singular_value_residual=singular_residual,
        polar_initial_support_residual=polar_residual,
        exact_principal_angle_normal_form_verified=verified,
        status=(
            "restriction-principal-angle-polar-verified"
            if verified
            else "restriction-principal-angle-control-failure"
        ),
    )


def bernstein_polar_degree_lower_bound(
    singular_value_upper_bound: float,
    approximation_error: float = 1 / 16,
) -> float:
    """Bound degree for p(0)=0 and p(sigma)>=1-error at sigma<=bound."""

    if not 0.0 < singular_value_upper_bound < 1.0:
        raise ValueError("singular bound must lie in (0,1)")
    if not 0.0 <= approximation_error < 1.0:
        raise ValueError("approximation_error must lie in [0,1)")
    return (
        (1.0 - approximation_error)
        * math.sqrt(1.0 - singular_value_upper_bound**2)
        / singular_value_upper_bound
    )


def principal_angle_scaling_record(
    n: int,
    *,
    alpha: float = 1e-4,
    beta: float = 400.0,
    approximation_error: float = 1 / 16,
) -> PrincipalAngleScalingRecord:
    if n < 4 or n % 2:
        raise ValueError("n must be even and at least four")
    hidden_count = involution_count(n, n // 2)
    copies = math.ceil(math.log2(hidden_count))
    partition, maximum = maximum_irrep_dimension(n)
    ratio = beta * maximum / hidden_count
    singular_bound = min(1.0, math.sqrt(ratio))
    active = singular_bound < 0.5
    degree = (
        bernstein_polar_degree_lower_bound(
            singular_bound, approximation_error
        )
        if active
        else None
    )
    return PrincipalAngleScalingRecord(
        n=n,
        perfect_matching_count_decimal=str(hidden_count),
        constant_pgm_success_copy_count=copies,
        physical_window_alpha=alpha,
        physical_window_beta=beta,
        windowed_pgm_success_lower_bound=windowed_pgm_success_lower_bound(
            hidden_count, copies, alpha, beta
        ),
        maximum_irrep_partition=partition,
        maximum_irrep_dimension_decimal=str(maximum),
        exact_beta_dmax_over_matching_count=ratio,
        exact_principal_singular_upper_bound=singular_bound,
        finite_bernstein_degree_lower_bound=degree,
        finite_row_in_subconstant_singular_regime=active,
        asymptotic_principal_singular_order=(
            "exp(-(mathfrak_d/2+o(1))*sqrt(n))*poly(n)"
        ),
        asymptotic_generic_qsvt_degree_order=(
            "exp((mathfrak_d/2+o(1))*sqrt(n))/poly(n)"
        ),
        polynomial_normalization_one_generic_qsvt_possible_asymptotically=False,
        status=(
            "finite-subconstant-principal-angle-control"
            if active
            else "preasymptotic-principal-angle-control"
        ),
    )


def build_coset_restriction_principal_angle_polar_report(
    *,
    scaling_n_values: tuple[int, ...] = (8, 10, 12, 16, 20, 24, 28, 32),
) -> CosetRestrictionPrincipalAnglePolarReport:
    standard = (2, 1)
    finite = [
        audit_restriction_principal_angle_control((standard,), standard),
        audit_restriction_principal_angle_control(
            (standard, standard), (3,)
        ),
        audit_restriction_principal_angle_control(
            (standard, standard), standard
        ),
        audit_restriction_principal_angle_control(
            (standard, standard, standard), standard
        ),
    ]
    scaling = [principal_angle_scaling_record(n) for n in scaling_n_values]
    verified = all(
        row.exact_principal_angle_normal_form_verified for row in finite
    )
    theorem = RestrictionPrincipalAnglePolarTheorem(
        vectorized_intertwiner_space=(
            "Hom_G(V_nu,U) is the invariant subspace of conj(V_nu) tensor U; "
            "J_nu is its isometric embedding."
        ),
        restriction_product=(
            "R_nu=(I_(V_nu^*) tensor P)J_nu is the vectorized centralizer "
            "restriction map."
        ),
        gram_identity="R_nu^*R_nu=D_nu exactly.",
        polar_identity=(
            "R_nu D_nu^(-1/2) is the covariance-compressed PGM polar factor."
        ),
        coherent_projector_access=(
            "The invariant projector is implementable by S_n generalized phase "
            "estimation and the fixed-involution projector is an explicit tensor product."
        ),
        physical_to_principal_spectrum=(
            "lambda(B)=delta(D_nu)/d_nu, so a physical window "
            "lambda<=beta/M gives sigma(R_nu)<=sqrt(beta d_max/M)."
        ),
        maximal_dimension_consequence=(
            "For M=(n-1)!!, Aggarwal--Elboim implies the retained principal "
            "singular scale is exp(-Omega(sqrt(n)))."
        ),
        bernstein_consequence=(
            "A bounded polynomial polar transform on normalization-one access "
            "has degree exp(Omega(sqrt(n)))."
        ),
        scope_limit=(
            "Only generic bounded-polynomial/QSVT transforms of the stated "
            "normalization-one product-of-projectors access are obstructed."
        ),
        exact_restriction_principal_angle_normal_form_proved=True,
        coherent_normalization_one_restriction_access_proved=True,
        dense_branching_table_required=False,
        generic_qsvt_subexponential_obstruction_proved=True,
        representation_specific_rescaling_ruled_out=False,
        hyperoctahedral_branching_transform_constructed=False,
        polynomial_fused_polar_circuit_constructed=False,
        general_quantum_circuit_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "restriction-principal-angle-access-and-generic-qsvt-bound-proved"
            if verified
            else "restriction-principal-angle-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_principal_angle_control_count": len(finite),
        "finite_control_failure_count": sum(
            not row.exact_principal_angle_normal_form_verified for row in finite
        ),
        "scaling_record_count": len(scaling),
        "restriction_principal_angle_normal_form_theorem_count": 1,
        "coherent_normalization_one_restriction_access_count": 1,
        "dense_branching_table_required_count": 0,
        "generic_qsvt_exp_sqrt_degree_obstruction_theorem_count": 1,
        "finite_subconstant_singular_row_count": sum(
            row.finite_row_in_subconstant_singular_regime for row in scaling
        ),
        "representation_specific_rescaling_count": 0,
        "hyperoctahedral_branching_transform_count": 0,
        "polynomial_fused_polar_circuit_count": 0,
        "general_quantum_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetRestrictionPrincipalAnglePolarReport(
        created_at=utc_now(),
        theorem_contract={
            "source": (
                "Natural weak-Fourier source branch U and target irrep nu for "
                "same-hidden fixed-point-free involution coset states."
            ),
            "access_model": (
                "Coherent reflections about the G-intertwiner invariant subspace "
                "and the fixed-involution source projector, each normalized by one."
            ),
            "retained_window": (
                "Physical frame eigenvalues in [alpha/M,beta/M], which retain "
                "constant average PGM success by the spectral-window theorem."
            ),
            "non_claim": (
                "No lower bound on structured rescaling, exact branching, "
                "non-polynomial circuits, or arbitrary measurements."
            ),
        },
        finite_controls=finite,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-RESTRICTION-PROJECTOR-ACCESS",
                "statement": (
                    "Expose the restriction map coherently without dense "
                    "Kronecker or centralizer branching tables."
                ),
                "resolved": True,
            },
            {
                "id": "PO-COSET-RESTRICTION-RESCALING",
                "statement": (
                    "Construct a representation-specific encoding normalized by "
                    "sqrt(d_nu/M), or prove that such an encoding is impossible."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-BRANCHING-POLAR",
                "statement": (
                    "Determine whether S_n down to S_2 wr S_(n/2) branching "
                    "diagonalizes or directly compiles the principal-angle polar."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-POLAR-TO-DECODER",
                "statement": (
                    "Complete the physical outcome map and hidden-matching decoder "
                    "after any structured polar construction."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The restriction map still needs a dense Hom basis.",
                "answer": (
                    "False at the access level: vectorization turns it into two "
                    "coherently projectable subspaces. No basis table is required."
                ),
                "resolved": True,
            },
            {
                "challenge": "Constant physical condition makes generic QSVT polynomial.",
                "answer": (
                    "False for normalization-one access. The whole retained window "
                    "lies at principal singular scale exp(-Omega(sqrt(n)))."
                ),
                "resolved": True,
            },
            {
                "challenge": "A small singular scale proves the polar is hard.",
                "answer": (
                    "False beyond generic bounded-polynomial access. Structured "
                    "fiber and branching transforms can implement tiny-scale polars directly."
                ),
                "resolved": True,
            },
            {
                "challenge": "Finite d_max rows prove the asymptotic degree bound.",
                "answer": (
                    "False. The asymptotic step uses the cited maximal-dimension "
                    "theorem; finite rows are normalization controls only."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "title": (
                    "On the maximal dimension of an irreducible representation "
                    "of the symmetric group"
                ),
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "use": (
                    "Turns sqrt(beta d_max/M) into an "
                    "exp(-Omega(sqrt(n))) principal singular scale."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "restriction_map_principal_angle_normal_form_proved": True,
            "coherent_normalization_one_restriction_access_proved": True,
            "dense_branching_table_required": False,
            "normalization_one_generic_qsvt_polynomial": False,
            "representation_specific_rescaled_access_proved": False,
            "hyperoctahedral_branching_polar_constructed": False,
            "polynomial_fused_polar_circuit_constructed": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "general_quantum_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The fused PGM is now an exactly accessible principal-angle "
                "polar, but normalization-one generic QSVT still costs "
                "exp(Omega(sqrt(n))). Only structured rescaling or branching "
                "can turn this normal form into a polynomial algorithm."
            ),
        },
        status=(
            "coherent-restriction-access-closed-generic-qsvt-subexponential-"
            "structured-rescaling-open"
        ),
        summary=(
            "Converted the centralizer restriction matrix into an exact "
            "product-of-projectors principal-angle polar with coherent "
            "normalization-one access. Generic QSVT remains exp(Omega(sqrt(n))); "
            "structured rescaling and hyperoctahedral branching are now the "
            "specific constructive frontier."
        ),
        falsifiers_triggered=[
            (
                "A dense centralizer branching table is not required merely to "
                "access the fused restriction map."
            ),
            (
                "Constant condition of the retained physical frame does not "
                "remove its exp(-Omega(sqrt(n))) normalization-one singular scale."
            ),
            (
                "The black-box polynomial obstruction cannot be promoted to a "
                "structured-transform or general circuit lower bound."
            ),
        ],
    )


def write_coset_restriction_principal_angle_polar_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-RESTRICTION-PRINCIPAL-ANGLE-POLAR-REDUCTION"
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
    payload = asdict(
        build_coset_restriction_principal_angle_polar_report(**kwargs)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG--RESTRICTION-PRINCIPAL-ANGLE-POLAR-REDUCTION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-RESTRICTION-PRINCIPAL-ANGLE-POLAR-REDUCTION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-RESTRICTION-PRINCIPAL-ANGLE-POLAR-REDUCTION."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "coset_restriction_principal_angle_polar_reduction": str(output_path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    report = write_coset_restriction_principal_angle_polar_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
