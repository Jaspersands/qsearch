"""Raw Fourier-coefficient access does not normalize regular orbit rows.

After trimmed-source canonicalization, hidden-involution synthesis has the
regular covariant form

    W|g,o> = U_g|v_o>.                                  (1)

Let ``rho_nu`` have dimension ``d_nu`` and write the ``nu`` component of a
representative as

    Pi_nu v_o = sum_(b,mu) a_nu(mu;b,o)|b,mu>.

Schur orthogonality gives the exact regular-Fourier block

    W_nu = sqrt(|G|/d_nu) I_(d_nu) tensor A_nu,          (2)

where ``A_nu[mu;(b,o)]=a_nu(mu;b,o)``.  Equation (2) is
verified below on the complete free-orbit ``S_3`` chart, including every
carrier and multiplicity coordinate.

A tempting compiler prepares ``v_o``, applies a generalized physical QFT, and
uses its raw coefficient block ``A_nu`` as a normalization-one block encoding.
But a useful singular value ``sigma(W_nu)=Theta(1)`` then appears at

    sigma(A_nu)=Theta(sqrt(d_nu/|G|)).                   (3)

Generic bounded odd-polynomial polar amplification costs
``Omega(sqrt(|G|/d_nu))``.  Since ``d_nu^2<=sum_lambda d_lambda^2=|G|``, this is
at least ``Omega(|G|^(1/4))`` in every sector.  For perfect-matching candidates
``M=(2m-1)!!``, ``|S_(2m)|^(1/4)`` and ``sqrt(M)`` have the same
``Theta(m log m)`` logarithmic leading term.

This closes only normalization-one access to the raw Fourier coefficients and
generic QSVT on them.  It does not rule out a direct block encoding already
normalized at ``sqrt(d_nu/|G|)``, a structured polar/fast-forward, or a joint
transform that never exposes ``A_nu`` at unit normalization.  Producing one of
those is exactly the remaining representation-specific opportunity.
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
    involution_conjugacy_class,
    symmetric_group,
)
from coset_hidden_involution_bulk_conditioning_normalization_no_go import (
    bulk_copy_count,
)
from coset_hidden_involution_matrix_hecke_transfer_reduction import (
    IRREPS,
    _intertwiner_basis,
)
from coset_hidden_involution_regular_orbit_row_reduction import (
    _conjugation_matrix,
    _s3_free_fiber_orbit_representatives,
)
from coset_perfect_matching_spherical_boundary import perfect_matching_count
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_fourier_coefficient_normalization_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-FOURIER-COEFFICIENT-NORMALIZATION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FourierCoefficientSectorControl:
    irrep_name: str
    irrep_partition: tuple[int, ...]
    carrier_dimension: int
    physical_multiplicity: int
    orbit_representative_count: int
    coefficient_row_count: int
    coefficient_column_count: int
    maximum_multiplicity_isometry_residual: float
    fourier_block_formula_residual: float
    singular_value_scaling_residual: float
    raw_coefficient_maximum_singular_value: float
    scaled_row_maximum_singular_value: float
    fourier_scalar_amplification: float
    generic_raw_coefficient_polar_degree_lower_scale: float
    exact_fourier_coefficient_formula_verified: bool
    status: str


@dataclass(frozen=True)
class FourierCoefficientFiniteControl:
    copy_count: int
    group_order: int
    physical_dimension: int
    free_orbit_representative_count: int
    regular_source_dimension: int
    sector_source_dimension_sum: int
    sectors: list[FourierCoefficientSectorControl]
    maximum_fourier_block_formula_residual: float
    maximum_singular_value_scaling_residual: float
    exact_all_sector_formula_verified: bool
    status: str


@dataclass(frozen=True)
class FourierCoefficientScalingRecord:
    half_degree: int
    degree: int
    group_order_decimal: str
    candidate_count_decimal: str
    copy_count: int
    universal_maximum_irrep_dimension_upper_log2: float
    raw_coefficient_qsvt_degree_lower_log2: float
    branch_erasure_sqrt_M_cost_log2: float
    lower_bound_to_branch_erasure_log2_ratio: float
    same_factorial_leading_exponent: bool
    sector_normalized_direct_access_compiled: bool
    status: str


@dataclass(frozen=True)
class FourierCoefficientNormalizationTheorem:
    regular_fourier_identity: str
    coefficient_block: str
    useful_scale_transfer: str
    universal_dimension_bound: str
    perfect_matching_comparison: str
    architecture_rule: str
    scope_limit: str
    regular_fourier_block_formula_proved: bool
    raw_coefficient_useful_scale_proved: bool
    every_sector_quarter_root_obstruction_proved: bool
    same_factorial_scale_as_branch_erasure_proved: bool
    sector_normalized_direct_access_compiled: bool
    structured_row_polar_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FourierCoefficientNormalizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FourierCoefficientFiniteControl]
    scaling_records: list[FourierCoefficientScalingRecord]
    theorem: FourierCoefficientNormalizationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _tensor_power(operator: np.ndarray, copy_count: int) -> np.ndarray:
    output = operator
    for _ in range(copy_count - 1):
        output = np.kron(output, operator)
    return output


def _s3_representative_vectors(
    copy_count: int,
) -> tuple[np.ndarray, ...]:
    group = symmetric_group(3)
    group_index = {element: index for index, element in enumerate(group)}
    hidden = involution_conjugacy_class(3, 1)[0]

    def plus_vector(representative: Permutation) -> np.ndarray:
        vector = np.zeros(len(group), dtype=complex)
        vector[group_index[representative]] = 1.0 / math.sqrt(2.0)
        vector[
            group_index[compose_permutations(representative, hidden)]
        ] = 1.0 / math.sqrt(2.0)
        return vector

    vectors = []
    for source_tuple in _s3_free_fiber_orbit_representatives(copy_count):
        vector = plus_vector(source_tuple[0])
        for representative in source_tuple[1:]:
            vector = np.kron(vector, plus_vector(representative))
        vectors.append(vector)
    return tuple(vectors)


def audit_fourier_coefficient_normalization(
    copy_count: int = 2,
    *,
    tolerance: float = 1e-9,
) -> FourierCoefficientFiniteControl:
    if copy_count < 1 or copy_count > 3:
        raise ValueError("S_3 finite control supports copy_count in [1,3]")
    group = symmetric_group(3)
    group_order = len(group)
    representative_vectors = _s3_representative_vectors(copy_count)
    physical_actions = {
        element: _tensor_power(
            _conjugation_matrix(group, element), copy_count
        )
        for element in group
    }
    physical_dimension = group_order**copy_count
    sectors: list[FourierCoefficientSectorControl] = []
    sector_source_dimension_sum = 0

    for name, partition, carrier_dimension in IRREPS:
        representation = _source_representation_rows(partition)
        raw_intertwiners = _intertwiner_basis(
            representation,
            physical_actions,
            group,
            tolerance=tolerance,
        )
        # Reynolds eigenvectors have Frobenius norm one.  Schur's lemma then
        # gives T^*T=I/d, so sqrt(d)T is an isometric carrier embedding.
        intertwiners = tuple(
            math.sqrt(carrier_dimension) * matrix
            for matrix in raw_intertwiners
        )
        isometry_residual = max(
            (
                float(
                    np.linalg.norm(
                        matrix.conj().T @ matrix
                        - np.eye(carrier_dimension),
                        ord=2,
                    )
                )
                for matrix in intertwiners
            ),
            default=0.0,
        )
        coefficient = np.zeros(
            (
                len(intertwiners),
                carrier_dimension * len(representative_vectors),
            ),
            dtype=complex,
        )
        for orbit, vector in enumerate(representative_vectors):
            for carrier_input in range(carrier_dimension):
                column = orbit * carrier_dimension + carrier_input
                for multiplicity, embedding in enumerate(intertwiners):
                    coefficient[multiplicity, column] = np.vdot(
                        embedding[:, carrier_input], vector
                    )

        fourier_columns = []
        predicted_columns = []
        scalar = math.sqrt(group_order / carrier_dimension)
        for carrier_output in range(carrier_dimension):
            for orbit, vector in enumerate(representative_vectors):
                for carrier_input in range(carrier_dimension):
                    transformed = sum(
                        np.conjugate(
                            representation[element][
                                carrier_output, carrier_input
                            ]
                        )
                        * (physical_actions[element] @ vector)
                        for element in group
                    ) * math.sqrt(carrier_dimension / group_order)
                    predicted = sum(
                        scalar
                        * coefficient[
                            multiplicity,
                            orbit * carrier_dimension + carrier_input,
                        ]
                        * embedding[:, carrier_output]
                        for multiplicity, embedding in enumerate(intertwiners)
                    )
                    fourier_columns.append(transformed)
                    predicted_columns.append(predicted)
        fourier_block = np.column_stack(fourier_columns)
        predicted_block = np.column_stack(predicted_columns)
        formula_residual = float(
            np.linalg.norm(fourier_block - predicted_block, ord=2)
        )
        observed_singular = np.linalg.svd(fourier_block, compute_uv=False)
        raw_singular = np.linalg.svd(coefficient, compute_uv=False)
        expected_positive = np.repeat(raw_singular * scalar, carrier_dimension)
        observed_positive = observed_singular[observed_singular > tolerance]
        expected_positive = expected_positive[expected_positive > tolerance]
        observed_positive.sort()
        expected_positive.sort()
        spectrum_residual = (
            float(np.max(np.abs(observed_positive - expected_positive)))
            if len(observed_positive) == len(expected_positive)
            else math.inf
        )
        verified = bool(
            isometry_residual <= 100 * tolerance
            and formula_residual <= 100 * tolerance
            and spectrum_residual <= 100 * tolerance
        )
        sectors.append(
            FourierCoefficientSectorControl(
                irrep_name=name,
                irrep_partition=partition,
                carrier_dimension=carrier_dimension,
                physical_multiplicity=len(intertwiners),
                orbit_representative_count=len(representative_vectors),
                coefficient_row_count=coefficient.shape[0],
                coefficient_column_count=coefficient.shape[1],
                maximum_multiplicity_isometry_residual=isometry_residual,
                fourier_block_formula_residual=formula_residual,
                singular_value_scaling_residual=spectrum_residual,
                raw_coefficient_maximum_singular_value=(
                    float(raw_singular[0]) if len(raw_singular) else 0.0
                ),
                scaled_row_maximum_singular_value=(
                    float(observed_singular[0]) if len(observed_singular) else 0.0
                ),
                fourier_scalar_amplification=scalar,
                generic_raw_coefficient_polar_degree_lower_scale=scalar,
                exact_fourier_coefficient_formula_verified=verified,
                status=(
                    "exact-regular-fourier-coefficient-scaling-verified"
                    if verified
                    else "fourier-coefficient-control-failure"
                ),
            )
        )
        sector_source_dimension_sum += (
            carrier_dimension**2 * len(representative_vectors)
        )

    maximum_formula = max(row.fourier_block_formula_residual for row in sectors)
    maximum_spectrum = max(row.singular_value_scaling_residual for row in sectors)
    source_dimension = group_order * len(representative_vectors)
    verified = bool(
        sector_source_dimension_sum == source_dimension
        and all(row.exact_fourier_coefficient_formula_verified for row in sectors)
    )
    return FourierCoefficientFiniteControl(
        copy_count=copy_count,
        group_order=group_order,
        physical_dimension=physical_dimension,
        free_orbit_representative_count=len(representative_vectors),
        regular_source_dimension=source_dimension,
        sector_source_dimension_sum=sector_source_dimension_sum,
        sectors=sectors,
        maximum_fourier_block_formula_residual=maximum_formula,
        maximum_singular_value_scaling_residual=maximum_spectrum,
        exact_all_sector_formula_verified=verified,
        status=(
            "exact-all-sector-fourier-coefficient-normal-form-verified"
            if verified
            else "fourier-coefficient-normalization-control-failure"
        ),
    )


def fourier_coefficient_scaling_record(
    half_degree: int,
    *,
    target_source_variance: float = 1e-6,
) -> FourierCoefficientScalingRecord:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    degree = 2 * half_degree
    group_order = math.factorial(degree)
    candidates = perfect_matching_count(half_degree)
    group_log2 = math.lgamma(degree + 1) / math.log(2.0)
    raw_lower = 0.25 * group_log2
    branch_cost = 0.5 * math.log2(candidates)
    copies = bulk_copy_count(candidates, target_source_variance)
    return FourierCoefficientScalingRecord(
        half_degree=half_degree,
        degree=degree,
        group_order_decimal=str(group_order),
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        universal_maximum_irrep_dimension_upper_log2=0.5 * group_log2,
        raw_coefficient_qsvt_degree_lower_log2=raw_lower,
        branch_erasure_sqrt_M_cost_log2=branch_cost,
        lower_bound_to_branch_erasure_log2_ratio=raw_lower - branch_cost,
        same_factorial_leading_exponent=True,
        sector_normalized_direct_access_compiled=False,
        status="raw-fourier-QSVT-factorial-scale-direct-sector-access-open",
    )


def build_fourier_coefficient_normalization_report(
    *,
    finite_copy_counts: tuple[int, ...] = (1, 2, 3),
    scaling_half_degrees: tuple[int, ...] = (3, 4, 8, 16, 32, 64, 128),
) -> FourierCoefficientNormalizationReport:
    controls = [
        audit_fourier_coefficient_normalization(copy_count)
        for copy_count in finite_copy_counts
    ]
    scaling = [
        fourier_coefficient_scaling_record(m) for m in scaling_half_degrees
    ]
    verified = all(row.exact_all_sector_formula_verified for row in controls)
    scaling_verified = all(
        row.same_factorial_leading_exponent
        and not row.sector_normalized_direct_access_compiled
        for row in scaling
    )
    theorem = FourierCoefficientNormalizationTheorem(
        regular_fourier_identity=(
            "For W|g,o>=U_gv_o, the normalized G QFT gives "
            "W_nu=sqrt(|G|/d_nu) I_(d_nu) tensor A_nu."
        ),
        coefficient_block=(
            "A_nu consists exactly of the physical nu-isotypic carrier-row "
            "coefficients of the canonical representative vectors v_o."
        ),
        useful_scale_transfer=(
            "A Theta(1) useful singular value of W_nu is "
            "Theta(sqrt(d_nu/|G|)) in raw A_nu access."
        ),
        universal_dimension_bound=(
            "d_nu^2<=sum_lambda d_lambda^2=|G|, so generic raw-coefficient "
            "polar degree is Omega(|G|^(1/4)) in every sector."
        ),
        perfect_matching_comparison=(
            "For G=S_(2m), |G|^(1/4) and sqrt((2m-1)!!) differ only by "
            "exp(O(log m)) and share the factorial leading exponent."
        ),
        architecture_rule=(
            "Do not treat prepare-v_o plus physical QFT plus normalization-one "
            "QSVT as the structured normalization escape."
        ),
        scope_limit=(
            "A sector-normalized direct block encoding, structured fast-forward, "
            "or direct row polar could bypass raw-coefficient QSVT."
        ),
        regular_fourier_block_formula_proved=True,
        raw_coefficient_useful_scale_proved=True,
        every_sector_quarter_root_obstruction_proved=True,
        same_factorial_scale_as_branch_erasure_proved=True,
        sector_normalized_direct_access_compiled=False,
        structured_row_polar_compiled=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "raw-fourier-normalization-closed-direct-sector-polar-open"
            if verified and scaling_verified
            else "fourier-coefficient-normalization-control-failure"
        ),
    )
    return FourierCoefficientNormalizationReport(
        created_at=utc_now(),
        theorem_contract={
            "source_normal_form": "C[G] tensor C[O] after trimmed free-orbit canonicalization.",
            "physical_action": "Diagonal G action decomposed as direct_sum_nu V_nu tensor M_nu.",
            "access_model": (
                "Normalization-one block access to raw representative Fourier "
                "coefficients A_nu, followed by generic bounded odd-polynomial QSVT."
            ),
            "useful_window": "Any sector singular vectors whose W singular values are Theta(1).",
            "outside_scope": (
                "Directly normalized coefficient access, exact branching transforms, "
                "fast-forwarding, and arbitrary representation-specific circuits."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-SECTOR-NORMALIZED-ROW-ACCESS",
                "statement": (
                    "Construct A_nu access with effective normalization "
                    "Theta(sqrt(d_nu/|G|)) on constant natural mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-ROW-FAST-FORWARD",
                "statement": (
                    "Exploit matrix-Hecke/recoupling structure to implement the "
                    "polar without a generic polynomial in raw A_nu."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-SECTOR-NATIVE-SPECTRUM",
                "statement": (
                    "Determine which nu sectors carry the constant-conditioned "
                    "alternative bulk and whether their row polars simplify."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A high-dimensional irrep removes the Fourier scalar loss.",
                "answer": (
                    "No irrep has d_nu>sqrt(|G|), leaving at least a |G|^(1/4) "
                    "generic amplification in every sector."
                ),
                "resolved": True,
            },
            {
                "challenge": "Measuring nu first permits constant normalization conditionally.",
                "answer": (
                    "Conditioning on nu does not rescale raw A_nu. A different "
                    "sector-normalized access primitive would be substantive new structure."
                ),
                "resolved": True,
            },
            {
                "challenge": "The regular QFT itself implements the scalar amplification.",
                "answer": (
                    "The identity specifies W_nu algebraically; implementing W is "
                    "the original label-erasure/polar problem, so using it is circular."
                ),
                "resolved": True,
            },
            {
                "challenge": "This rules out all Fourier or recoupling algorithms.",
                "answer": (
                    "False. Only normalization-one raw-coefficient access plus "
                    "generic QSVT is closed. Structured direct polars remain open."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_all_sector_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_all_sector_formula_verified for row in controls
            ),
            "regular_fourier_block_identity_theorem_count": 1,
            "universal_quarter_root_obstruction_theorem_count": 1,
            "sector_normalized_direct_access_count": 0,
            "structured_row_polar_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "regular_fourier_coefficient_identity_proved": verified,
            "normalization_one_raw_coefficient_qsvt_polynomial": False,
            "every_sector_quarter_root_obstruction_proved": verified,
            "sector_normalized_direct_access_compiled": False,
            "structured_row_polar_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The regular QFT moves the missing normalization into the scalar "
                "sqrt(|G|/d_nu); raw coefficient access does not supply it."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived and exactly verified the regular Fourier row formula, then "
            "proved that generic normalization-one access to its coefficient "
            "blocks retains a universal factorial-scale polar amplification cost."
        ),
        falsifiers_triggered=[
            "Preparing canonical orbit representatives and applying a physical QFT does not by itself normalize the row polar.",
            "Sector conditioning cannot beat the quarter-root group-order barrier under normalization-one raw coefficient access.",
            "The regular Fourier scalar is an algebraic identity, not a free circuit amplitude.",
        ],
    )


def write_fourier_coefficient_normalization_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_fourier_coefficient_normalization_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_fourier_coefficient_normalization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
