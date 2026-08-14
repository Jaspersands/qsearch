"""Matrix-valued Hecke transfer for hidden-involution source synthesis.

The induced-source reduction identifies the branch source as
``Ind_K^G R``, where ``R=ran(P_0)``.  This module writes the remaining
multiplicity synthesis operator explicitly.

For ``T in Hom_K(V_nu,R)``, define the normalized induction transfer

    F_nu(T) = |G:K|^(-1/2) sum_(xK) U_x T rho_nu(x)^*.  (1)

It lies in ``Hom_G(V_nu,H)``.  Its Gram form is exactly

    <F_nu(T),F_nu(T')>
      = |K|^-1 sum_(g in G)
          Tr[T^* P_0 U_g P_0 T' rho_nu(g)^*].           (2)

Equation (2) is a matrix-valued Hecke transfer on
``Hom_K(V_nu,R)``.  It is not the scalar Hecke algebra of the label space
``G/K`` unless ``R`` is the trivial one-dimensional stabilizer module.

On the regular ``S_3`` chart, the scalar permutation module on three branches
has commutant dimension two.  For ``k`` source copies, however,

    dim End_G(Ind_K^G R^tensor k) = (3*9^k+1)/2,         (3)

and the standard sector alone has source multiplicity ``3^k``.  Exact finite
controls verify (1)-(2) and the synthesis ranks from the induced-source
theorem.  Thus a scalar perfect-matching spherical transform can organize
branch labels but cannot diagonalize the source-specific physical transfer.

This reduction identifies the operator that a serious algorithm must compile.
It does not construct a basis for its large multiplicity spaces, a structured
inverse/support transform, the physical-to-source lift, or a speedup.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    involution_conjugacy_class,
    right_regular_matrix,
    symmetric_group,
)
from coset_hidden_involution_induced_source_bundle_reduction import (
    s3_induced_source_multiplicities,
    s3_synthesis_multiplicity_ranks,
)
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_matrix_hecke_transfer_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MATRIX-HECKE-TRANSFER-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class MatrixHeckeSectorControl:
    copy_count: int
    irrep_name: str
    irrep_partition: Partition
    carrier_dimension: int
    source_multiplicity: int
    physical_multiplicity: int
    observed_transfer_rank: int
    predicted_transfer_rank: int
    maximum_transfer_equivariance_residual: float
    direct_vs_matrix_hecke_gram_residual: float
    minimum_positive_transfer_gram_eigenvalue: float
    maximum_transfer_gram_eigenvalue: float
    exact_matrix_hecke_transfer_verified: bool
    status: str


@dataclass(frozen=True)
class MatrixHeckeFiniteControl:
    copy_count: int
    scalar_branch_hecke_dimension: int
    vector_bundle_commutant_dimension: int
    maximum_source_multiplicity: int
    matrix_valued_extension_noncommutative: bool
    sectors: list[MatrixHeckeSectorControl]
    maximum_gram_formula_residual: float
    maximum_equivariance_residual: float
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class MatrixHeckeScalingRecord:
    copy_count: int
    scalar_branch_hecke_dimension: int
    vector_bundle_commutant_dimension_decimal: str
    vector_to_scalar_dimension_ratio: float
    standard_source_multiplicity_decimal: str
    standard_transfer_kernel_multiplicity: int
    scalar_spherical_transform_sufficient: bool
    matrix_hecke_basis_compiled: bool
    structured_transfer_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class MatrixHeckeTransferTheorem:
    normalized_transfer: str
    gram_formula: str
    double_coset_structure: str
    scalar_hecke_boundary: str
    s3_commutant_growth: str
    computational_target: str
    scope_limit: str
    exact_transfer_formula_proved: bool
    matrix_valued_hecke_reduction_proved: bool
    scalar_spherical_transform_sufficient: bool
    uniform_matrix_hecke_basis_compiled: bool
    structured_multiplicity_polar_compiled: bool
    physical_to_source_lift_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class MatrixHeckeTransferReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[MatrixHeckeFiniteControl]
    scaling_records: list[MatrixHeckeScalingRecord]
    theorem: MatrixHeckeTransferTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


IRREPS: tuple[tuple[str, Partition, int], ...] = (
    ("trivial", (3,), 1),
    ("sign", (1, 1, 1), 1),
    ("standard", (2, 1), 2),
)


def _conjugate(
    element: Permutation,
    value: Permutation,
) -> Permutation:
    return compose_permutations(
        compose_permutations(element, value), inverse_permutation(element)
    )


def _conjugation_matrix(
    group: tuple[Permutation, ...],
    element: Permutation,
) -> np.ndarray:
    index = {value: offset for offset, value in enumerate(group)}
    matrix = np.zeros((len(group), len(group)), dtype=complex)
    for column, value in enumerate(group):
        matrix[index[_conjugate(element, value)], column] = 1.0
    return matrix


def _tensor_power(operator: np.ndarray, copy_count: int) -> np.ndarray:
    output = operator
    for _ in range(copy_count - 1):
        output = np.kron(output, operator)
    return output


def _right_coset_representatives(
    group: tuple[Permutation, ...],
    subgroup: tuple[Permutation, ...],
) -> tuple[Permutation, ...]:
    unused = set(group)
    representatives = []
    while unused:
        representative = min(unused)
        representatives.append(representative)
        unused.difference_update(
            compose_permutations(representative, element)
            for element in subgroup
        )
    return tuple(representatives)


def _intertwiner_basis(
    domain_actions: dict[Permutation, np.ndarray],
    codomain_actions: dict[Permutation, np.ndarray],
    elements: tuple[Permutation, ...],
    *,
    tolerance: float,
) -> tuple[np.ndarray, ...]:
    domain_dimension = next(iter(domain_actions.values())).shape[0]
    codomain_dimension = next(iter(codomain_actions.values())).shape[0]
    reynolds = sum(
        np.kron(
            np.conjugate(domain_actions[element]),
            codomain_actions[element],
        )
        for element in elements
    ) / len(elements)
    reynolds = (reynolds + reynolds.conj().T) / 2.0
    values, vectors = np.linalg.eigh(reynolds)
    return tuple(
        vectors[:, index].reshape(
            (codomain_dimension, domain_dimension), order="F"
        )
        for index, value in enumerate(values)
        if value > 1.0 - 100 * tolerance
    )


def _physical_multiplicities(copy_count: int) -> tuple[int, int, int]:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    trivial = (
        6**copy_count + 3 * 2**copy_count + 2 * 3**copy_count
    ) // 6
    sign = (
        6**copy_count - 3 * 2**copy_count + 2 * 3**copy_count
    ) // 6
    standard = (6**copy_count - 3**copy_count) // 3
    return trivial, sign, standard


def audit_matrix_hecke_transfer(
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> MatrixHeckeFiniteControl:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    group = symmetric_group(3)
    base = involution_conjugacy_class(3, 1)[0]
    subgroup = tuple(
        element for element in group if _conjugate(element, base) == base
    )
    coset_representatives = _right_coset_representatives(group, subgroup)
    one_copy_projector = (
        np.eye(len(group)) + right_regular_matrix(3, base)
    ) / 2.0
    values, vectors = np.linalg.eigh(one_copy_projector)
    fiber_embedding = _tensor_power(
        vectors[:, values > 0.5], copy_count
    )
    physical_actions = {
        element: _tensor_power(
            _conjugation_matrix(group, element), copy_count
        )
        for element in group
    }
    fiber_actions = {
        element: (
            fiber_embedding.conj().T
            @ physical_actions[element]
            @ fiber_embedding
        )
        for element in subgroup
    }
    predicted_source = s3_induced_source_multiplicities(copy_count)
    predicted_ranks = s3_synthesis_multiplicity_ranks(copy_count)
    predicted_physical = _physical_multiplicities(copy_count)

    sectors: list[MatrixHeckeSectorControl] = []
    for sector_index, (name, partition, carrier_dimension) in enumerate(IRREPS):
        representation = _source_representation_rows(partition)
        source_basis = _intertwiner_basis(
            {element: representation[element] for element in subgroup},
            fiber_actions,
            subgroup,
            tolerance=tolerance,
        )
        physical_basis = _intertwiner_basis(
            representation,
            physical_actions,
            group,
            tolerance=tolerance,
        )
        transfers = tuple(
            sum(
                physical_actions[representative]
                @ fiber_embedding
                @ intertwiner
                @ representation[representative].conj().T
                for representative in coset_representatives
            )
            / math.sqrt(len(coset_representatives))
            for intertwiner in source_basis
        )
        transfer_matrix = np.asarray(
            [
                [
                    np.trace(output.conj().T @ transfer)
                    for transfer in transfers
                ]
                for output in physical_basis
            ],
            dtype=complex,
        )
        direct_gram = transfer_matrix.conj().T @ transfer_matrix
        hecke_gram = np.zeros_like(direct_gram)
        for left, left_intertwiner in enumerate(source_basis):
            for right, right_intertwiner in enumerate(source_basis):
                hecke_gram[left, right] = sum(
                    np.trace(
                        left_intertwiner.conj().T
                        @ (
                            fiber_embedding.conj().T
                            @ physical_actions[element]
                            @ fiber_embedding
                        )
                        @ right_intertwiner
                        @ representation[element].conj().T
                    )
                    for element in group
                ) / len(subgroup)
        gram_residual = float(np.linalg.norm(direct_gram - hecke_gram, ord=2))
        equivariance = max(
            (
                float(
                    np.linalg.norm(
                        physical_actions[element] @ transfer
                        - transfer @ representation[element],
                        ord=2,
                    )
                )
                for element in group
                for transfer in transfers
            ),
            default=0.0,
        )
        gram_values = np.linalg.eigvalsh(
            (direct_gram + direct_gram.conj().T) / 2.0
        )
        positive = gram_values[gram_values > tolerance]
        observed_rank = int(len(positive))
        verified = bool(
            len(source_basis) == predicted_source[sector_index]
            and len(physical_basis) == predicted_physical[sector_index]
            and observed_rank == predicted_ranks[sector_index]
            and gram_residual <= 100 * tolerance
            and equivariance <= 100 * tolerance
        )
        sectors.append(
            MatrixHeckeSectorControl(
                copy_count=copy_count,
                irrep_name=name,
                irrep_partition=partition,
                carrier_dimension=carrier_dimension,
                source_multiplicity=len(source_basis),
                physical_multiplicity=len(physical_basis),
                observed_transfer_rank=observed_rank,
                predicted_transfer_rank=predicted_ranks[sector_index],
                maximum_transfer_equivariance_residual=equivariance,
                direct_vs_matrix_hecke_gram_residual=gram_residual,
                minimum_positive_transfer_gram_eigenvalue=float(
                    np.min(positive)
                ),
                maximum_transfer_gram_eigenvalue=float(np.max(positive)),
                exact_matrix_hecke_transfer_verified=verified,
                status=(
                    "exact-matrix-hecke-transfer-sector-verified"
                    if verified
                    else "matrix-hecke-transfer-sector-failure"
                ),
            )
        )

    vector_dimension = (3 * 9**copy_count + 1) // 2
    verified = bool(
        all(row.exact_matrix_hecke_transfer_verified for row in sectors)
        and vector_dimension
        == sum(value**2 for value in predicted_source)
        and vector_dimension > 2
    )
    return MatrixHeckeFiniteControl(
        copy_count=copy_count,
        scalar_branch_hecke_dimension=2,
        vector_bundle_commutant_dimension=vector_dimension,
        maximum_source_multiplicity=max(predicted_source),
        matrix_valued_extension_noncommutative=True,
        sectors=sectors,
        maximum_gram_formula_residual=max(
            row.direct_vs_matrix_hecke_gram_residual for row in sectors
        ),
        maximum_equivariance_residual=max(
            row.maximum_transfer_equivariance_residual for row in sectors
        ),
        finite_control_verified=verified,
        status=(
            "matrix-valued-hecke-transfer-reduction-verified"
            if verified
            else "matrix-hecke-transfer-control-failure"
        ),
    )


def matrix_hecke_scaling_record(
    copy_count: int,
) -> MatrixHeckeScalingRecord:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    vector_dimension = (3 * 9**copy_count + 1) // 2
    standard = 3**copy_count
    return MatrixHeckeScalingRecord(
        copy_count=copy_count,
        scalar_branch_hecke_dimension=2,
        vector_bundle_commutant_dimension_decimal=str(vector_dimension),
        vector_to_scalar_dimension_ratio=vector_dimension / 2.0,
        standard_source_multiplicity_decimal=str(standard),
        standard_transfer_kernel_multiplicity=copy_count + 1,
        scalar_spherical_transform_sufficient=False,
        matrix_hecke_basis_compiled=False,
        structured_transfer_polar_compiled=False,
        status="matrix-hecke-operator-formalized-transform-open",
    )


def build_matrix_hecke_transfer_report(
    *,
    finite_copy_counts: tuple[int, ...] = (1, 2),
    scaling_copy_counts: tuple[int, ...] = (1, 2, 8, 32, 128),
) -> MatrixHeckeTransferReport:
    controls = [audit_matrix_hecke_transfer(k) for k in finite_copy_counts]
    scaling = [matrix_hecke_scaling_record(k) for k in scaling_copy_counts]
    verified = all(row.finite_control_verified for row in controls)
    theorem = MatrixHeckeTransferTheorem(
        normalized_transfer=(
            "F_nu(T)=|G:K|^-1/2 sum_(xK) U_x T rho_nu(x)^*."
        ),
        gram_formula=(
            "<F(T),F(T')>=|K|^-1 sum_g Tr[T^* P_0 U_g P_0 T' "
            "rho_nu(g)^*]."
        ),
        double_coset_structure=(
            "K-equivariance groups the operator-valued coefficients by K double "
            "cosets, producing End_G(Ind_K^G R), a matrix-valued Hecke algebra."
        ),
        scalar_hecke_boundary=(
            "The commutative scalar Hecke algebra of G/K applies only to the "
            "trivial stabilizer fiber and cannot determine physical row orientation."
        ),
        s3_commutant_growth=(
            "On k regular S_3 chart copies, the vector-bundle commutant dimension "
            "is (3*9^k+1)/2 versus scalar branch dimension two."
        ),
        computational_target=(
            "Compile the support/polar of this positive matrix-valued transfer "
            "in a uniform Hom_K multiplicity basis."
        ),
        scope_limit=(
            "No such basis, structured inverse, physical source lift, decoder, "
            "classical separation, or algorithm is constructed."
        ),
        exact_transfer_formula_proved=True,
        matrix_valued_hecke_reduction_proved=True,
        scalar_spherical_transform_sufficient=False,
        uniform_matrix_hecke_basis_compiled=False,
        structured_multiplicity_polar_compiled=False,
        physical_to_source_lift_compiled=False,
        theorem_verified=verified,
        status=(
            "matrix-hecke-transfer-formalized-structured-polar-open"
            if verified
            else "matrix-hecke-transfer-control-failure"
        ),
    )
    return MatrixHeckeTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "representation": (
                "A finite G representation H, K-invariant projector P_0, and "
                "fiber R=ran(P_0)."
            ),
            "operator": (
                "The normalized induced synthesis transfer on each "
                "Hom_K(V_nu,R) multiplicity space."
            ),
            "normalization": (
                "The explicit |G:K|^-1/2 branch normalization; changing it "
                "rescales the Gram but not its support."
            ),
            "outside_scope": (
                "A scalar outcome Hecke transform, abstract arbitrary row "
                "orientation, and any unproved full-class compiler."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-MATRIX-HECKE-BASIS",
                "statement": (
                    "Construct a polynomial coherent basis for the natural "
                    "Hom_K(V_nu,R^tensor k) matrix-Hecke modules."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-MATRIX-HECKE-POLAR",
                "statement": (
                    "Exploit source-specific coefficient structure to compile "
                    "support/polar without generic small-scale QSVT."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-MATRIX-HECKE-DEQUANTIZATION",
                "statement": (
                    "Determine whether the same matrix-valued transfer admits a "
                    "polynomial classical representation or sampling algorithm."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The perfect-matching Gelfand transform diagonalizes the source Gram.",
                "answer": (
                    "False in general: the nontrivial fiber R produces a large "
                    "matrix-valued commutant even when scalar G/K is Gelfand."
                ),
                "resolved": True,
            },
            {
                "challenge": "The transfer formula itself supplies an efficient inverse.",
                "answer": (
                    "False. It gives an exact positive operator and access model, "
                    "not a condition bound or structured polar circuit."
                ),
                "resolved": True,
            },
            {
                "challenge": "Large commutant dimension proves hardness.",
                "answer": (
                    "False. A succinct recoupling transform may exist; dimension "
                    "alone is not a circuit lower bound."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_transfer_formula_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.finite_control_verified for row in controls
            ),
            "matrix_valued_hecke_reduction_theorem_count": 1,
            "scalar_spherical_transform_sufficient_count": 0,
            "uniform_matrix_hecke_basis_compiler_count": 0,
            "structured_transfer_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "matrix_valued_hecke_transfer_formula_proved": verified,
            "scalar_matching_association_scheme_sufficient": False,
            "source_specific_physical_multiplicity_operator_isolated": verified,
            "uniform_matrix_hecke_basis_compiled": False,
            "structured_multiplicity_polar_compiled": False,
            "physical_to_source_lift_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact source transfer is matrix-valued on large stabilizer "
                "multiplicity spaces. Its structured basis, polar, and physical "
                "access remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the exact matrix-valued Hecke Gram for induced orbit "
            "synthesis, verified it against direct transfers, and proved that "
            "the scalar matching spherical transform omits the source-specific "
            "multiplicity operator that must actually be compiled."
        ),
        falsifiers_triggered=[
            "Scalar Gelfand-pair spectra do not diagonalize a nontrivial source fiber.",
            "The normalized transfer formula does not remove its own small-scale polar cost.",
            "Large matrix-Hecke dimension is a representation target, not a hardness proof.",
        ],
    )


def write_matrix_hecke_transfer_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_matrix_hecke_transfer_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_matrix_hecke_transfer_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
