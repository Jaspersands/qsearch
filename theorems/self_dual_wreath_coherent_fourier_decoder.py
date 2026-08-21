"""Coherent cross-sector Fourier decoder criterion.

For a finite group ``G`` with irreps ``rho_nu`` of dimensions ``d_nu``, the
nonabelian Fourier image of a group element is

    |F_g> = direct_sum_nu sqrt(d_nu/|G|) vec(rho_nu(g)).

These states are orthonormal.  An inverse group Fourier transform maps
``|F_g>`` to ``|g>`` exactly.

Consider instead a coherent covariant state

    |psi_g> = direct_sum_nu sqrt(p_nu)
              (rho_nu(g) tensor I)|phi_nu>,

where the Schmidt coefficients of ``|phi_nu>`` between the row irrep and an
aligned multiplicity/column register are ``sqrt(lambda_nu,i)``.  Define

    f_nu = d_nu^-1/2 sum_i sqrt(lambda_nu,i),   0 <= f_nu <= 1.

After the inverse group QFT, the exact correct-label probability is

    P_Fourier = [sum_nu d_nu sqrt(p_nu/|G|) f_nu]^2.          (1)

Thus perfect decoding requires two transparent resources:

1. Plancherel sector amplitudes ``p_nu=d_nu^2/|G|``;
2. a maximally entangled, coherently aligned dual row register in every sector.

For ``G=S_n``, Beals' efficient symmetric-group QFT makes the final inverse
transform polynomial.  The hard research problem is no longer an abstract
``n!``-outcome decoder: it is a structured coherent carrier-normalization
problem.  The orientation filter must preserve cross-``nu`` coherence, expose
the column partner, flatten each sector's Schmidt spectrum, and reweight sector
amplitudes toward Plancherel without a factorial postselection cost.

The module verifies (1) against exact Young-representation Fourier matrices.
It does not claim that the physical wreath coset-state carrier already has the
required Schmidt spectra or that the normalization is efficient.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_coherent_fourier_decoder.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COHERENT-FOURIER-DECODER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
BEALS_PAPER_URL = "https://doi.org/10.1145/258533.258548"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class CoherentFourierDecoderControl:
    control_id: str
    n: int
    group_order: int
    irrep_count: int
    fourier_dimension: int
    maximum_fourier_unitarity_residual: float
    sector_weights: tuple[float, ...]
    sector_entanglement_fidelities: tuple[float, ...]
    predicted_correct_label_probability: float
    minimum_observed_correct_label_probability: float
    maximum_observed_correct_label_probability: float
    maximum_success_formula_residual: float
    exact_permutation_independence_verified: bool
    exact_decoder_formula_verified: bool
    status: str


@dataclass(frozen=True)
class CoherentFourierDecoderScalingRecord:
    n: int
    group_order_decimal: str
    log2_group_order: float
    irrep_count: int
    maximum_irrep_dimension_decimal: str
    coherent_irrep_label_qubit_upper_bound: int
    row_register_qubit_upper_bound: int
    column_register_qubit_upper_bound: int
    total_fourier_register_qubit_upper_bound: int
    plancherel_weight_identity_verified: bool
    efficient_symmetric_group_qft_available: bool
    physical_sector_weight_match_proved: bool
    coherent_dual_row_extraction_proved: bool
    sector_schmidt_flattening_proved: bool
    polynomial_sector_reweighting_proved: bool
    end_to_end_fourier_decoder_proved: bool
    status: str


@dataclass(frozen=True)
class CoherentFourierDecoderReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CoherentFourierDecoderControl]
    scaling_records: list[CoherentFourierDecoderScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def symmetric_group_fourier_matrix(
    n: int,
) -> tuple[np.ndarray, tuple[Permutation, ...], tuple[Partition, ...]]:
    """Return rows ``<g|F^-1`` in the Young matrix-coefficient basis."""

    if n < 1:
        raise ValueError("n must be positive")
    partitions = integer_partitions(n)
    tables = {
        partition: _source_representation_rows(partition)
        for partition in partitions
    }
    permutations = tuple(next(iter(tables.values())))
    order = math.factorial(n)
    matrix = np.zeros((order, order))
    column = 0
    for partition in partitions:
        dimension = hook_length_dimension(partition)
        scale = math.sqrt(dimension / order)
        width = dimension * dimension
        for row_index, permutation in enumerate(permutations):
            matrix[row_index, column : column + width] = (
                scale * tables[partition][permutation].reshape(-1)
            )
        column += width
    if column != order:
        raise ArithmeticError("sum of squared irrep dimensions is not |S_n|")
    return matrix, permutations, partitions


def entanglement_fidelity_from_schmidt(
    coefficients: tuple[float, ...],
    dimension: int,
) -> float:
    if dimension < 1:
        raise ValueError("dimension must be positive")
    if len(coefficients) > dimension:
        raise ValueError("too many Schmidt coefficients")
    if any(value < 0 for value in coefficients):
        raise ValueError("Schmidt probabilities must be nonnegative")
    if abs(sum(coefficients) - 1) > 1e-10:
        raise ValueError("Schmidt probabilities must sum to one")
    return sum(math.sqrt(value) for value in coefficients) / math.sqrt(
        dimension
    )


def coherent_fourier_success(
    dimensions: tuple[int, ...],
    sector_weights: tuple[float, ...],
    entanglement_fidelities: tuple[float, ...],
) -> float:
    if not (
        len(dimensions)
        == len(sector_weights)
        == len(entanglement_fidelities)
    ):
        raise ValueError("one weight and fidelity are required per irrep")
    if abs(sum(sector_weights) - 1) > 1e-10:
        raise ValueError("sector weights must sum to one")
    if any(weight < 0 for weight in sector_weights):
        raise ValueError("sector weights must be nonnegative")
    if any(not 0 <= value <= 1 + 1e-12 for value in entanglement_fidelities):
        raise ValueError("entanglement fidelities must lie in [0,1]")
    order = sum(dimension * dimension for dimension in dimensions)
    amplitude = sum(
        dimension * math.sqrt(weight / order) * fidelity
        for dimension, weight, fidelity in zip(
            dimensions,
            sector_weights,
            entanglement_fidelities,
        )
    )
    return amplitude * amplitude


def _schmidt_profiles(
    dimensions: tuple[int, ...],
    mode: str,
) -> tuple[tuple[float, ...], ...]:
    if mode == "maximally-entangled":
        return tuple(
            tuple(1 / dimension for _ in range(dimension))
            for dimension in dimensions
        )
    if mode == "rank-one":
        return tuple((1.0,) for _ in dimensions)
    if mode == "mixed-profile":
        profiles = []
        for dimension in dimensions:
            raw = np.arange(dimension, 0, -1, dtype=float)
            raw /= raw.sum()
            profiles.append(tuple(float(value) for value in raw))
        return tuple(profiles)
    raise ValueError("unknown Schmidt profile mode")


def audit_coherent_fourier_decoder(
    n: int,
    *,
    control_id: str,
    weight_mode: str,
    schmidt_mode: str,
    tolerance: float = 1e-10,
) -> CoherentFourierDecoderControl:
    fourier, permutations, partitions = symmetric_group_fourier_matrix(n)
    dimensions = tuple(hook_length_dimension(item) for item in partitions)
    order = math.factorial(n)
    plancherel = tuple(dimension * dimension / order for dimension in dimensions)
    if weight_mode == "plancherel":
        weights = plancherel
    elif weight_mode == "uniform-irrep":
        weights = tuple(1 / len(dimensions) for _ in dimensions)
    elif weight_mode == "dimension":
        total = sum(dimensions)
        weights = tuple(dimension / total for dimension in dimensions)
    else:
        raise ValueError("unknown sector weight mode")
    profiles = _schmidt_profiles(dimensions, schmidt_mode)
    fidelities = tuple(
        entanglement_fidelity_from_schmidt(profile, dimension)
        for profile, dimension in zip(profiles, dimensions)
    )
    predicted = coherent_fourier_success(dimensions, weights, fidelities)
    unitarity = float(
        np.linalg.norm(fourier @ fourier.T - np.eye(order), ord=2)
    )

    observed = []
    column_offsets = []
    offset = 0
    for dimension in dimensions:
        column_offsets.append(offset)
        offset += dimension * dimension
    tables = {
        partition: _source_representation_rows(partition)
        for partition in partitions
    }
    for permutation_index, permutation in enumerate(permutations):
        state = np.zeros(order)
        for partition, dimension, weight, profile, offset in zip(
            partitions,
            dimensions,
            weights,
            profiles,
            column_offsets,
        ):
            coefficient = math.sqrt(weight)
            padded_profile = (*profile, *((0.0,) * (dimension - len(profile))))
            root = np.sqrt(np.asarray(padded_profile))
            sector = tables[partition][permutation] @ np.diag(root)
            state[offset : offset + dimension * dimension] = (
                coefficient * sector.reshape(-1)
            )
        computational = fourier @ state
        observed.append(float(abs(computational[permutation_index]) ** 2))
    formula_residual = max(abs(value - predicted) for value in observed)
    independent = max(observed) - min(observed) <= 100 * tolerance
    verified = (
        unitarity <= 100 * tolerance
        and formula_residual <= 100 * tolerance
        and independent
    )
    return CoherentFourierDecoderControl(
        control_id=control_id,
        n=n,
        group_order=order,
        irrep_count=len(partitions),
        fourier_dimension=len(fourier),
        maximum_fourier_unitarity_residual=unitarity,
        sector_weights=weights,
        sector_entanglement_fidelities=fidelities,
        predicted_correct_label_probability=predicted,
        minimum_observed_correct_label_probability=min(observed),
        maximum_observed_correct_label_probability=max(observed),
        maximum_success_formula_residual=formula_residual,
        exact_permutation_independence_verified=independent,
        exact_decoder_formula_verified=verified,
        status=(
            "exact-coherent-fourier-decoder-control"
            if verified
            else "coherent-fourier-decoder-validation-failure"
        ),
    )


def coherent_fourier_scaling_record(
    n: int,
) -> CoherentFourierDecoderScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = integer_partitions(n)
    dimensions = tuple(hook_length_dimension(item) for item in partitions)
    order = math.factorial(n)
    maximum = max(dimensions)
    label_qubits = math.ceil(math.log2(len(partitions)))
    row_qubits = math.ceil(math.log2(maximum))
    return CoherentFourierDecoderScalingRecord(
        n=n,
        group_order_decimal=str(order),
        log2_group_order=math.log2(order),
        irrep_count=len(partitions),
        maximum_irrep_dimension_decimal=str(maximum),
        coherent_irrep_label_qubit_upper_bound=label_qubits,
        row_register_qubit_upper_bound=row_qubits,
        column_register_qubit_upper_bound=row_qubits,
        total_fourier_register_qubit_upper_bound=(
            label_qubits + 2 * row_qubits
        ),
        plancherel_weight_identity_verified=(
            sum(dimension * dimension for dimension in dimensions) == order
        ),
        efficient_symmetric_group_qft_available=True,
        physical_sector_weight_match_proved=False,
        coherent_dual_row_extraction_proved=False,
        sector_schmidt_flattening_proved=False,
        polynomial_sector_reweighting_proved=False,
        end_to_end_fourier_decoder_proved=False,
        status="ideal-fourier-decoder-target-physical-carrier-normalization-open",
    )


def run_coherent_fourier_decoder() -> CoherentFourierDecoderReport:
    controls = [
        audit_coherent_fourier_decoder(
            3,
            control_id="S3-IDEAL",
            weight_mode="plancherel",
            schmidt_mode="maximally-entangled",
        ),
        audit_coherent_fourier_decoder(
            3,
            control_id="S3-WEIGHT-MISMATCH",
            weight_mode="uniform-irrep",
            schmidt_mode="maximally-entangled",
        ),
        audit_coherent_fourier_decoder(
            4,
            control_id="S4-SCHMIDT-MISMATCH",
            weight_mode="plancherel",
            schmidt_mode="mixed-profile",
        ),
        audit_coherent_fourier_decoder(
            4,
            control_id="S4-RANK-ONE",
            weight_mode="dimension",
            schmidt_mode="rank-one",
        ),
    ]
    scaling = [
        coherent_fourier_scaling_record(n)
        for n in (3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 28, 32)
    ]
    failures = sum(not row.exact_decoder_formula_verified for row in controls)
    ideal = controls[0]
    verified = (
        failures == 0
        and abs(ideal.predicted_correct_label_probability - 1) <= 1e-10
        and all(row.plancherel_weight_identity_verified for row in scaling)
    )
    proof_obligations: list[dict[str, bool | str]] = [
        {
            "obligation": "matrix_coefficient_fourier_orthogonality",
            "resolved": verified,
            "resolution": (
                "Schur orthogonality makes the states direct_sum sqrt(d/|G|) "
                "vec(rho_nu(g)) an orthonormal basis indexed by g."
            ),
        },
        {
            "obligation": "coherent_decoder_success_formula",
            "resolved": verified,
            "resolution": (
                "Direct contraction with the matrix-coefficient Fourier row gives "
                "[sum_nu d_nu sqrt(p_nu/|G|) f_nu]^2."
            ),
        },
        {
            "obligation": "efficient_inverse_symmetric_group_qft",
            "resolved": True,
            "resolution": (
                "Beals supplies a polynomial quantum Fourier transform over S_n; "
                "the external theorem is linked below."
            ),
        },
        {
            "obligation": "physical_filtered_sector_weight_match",
            "resolved": False,
            "resolution": (
                "No typical-source theorem shows that the filtered physical "
                "carrier has Plancherel coherent amplitudes after acceptance."
            ),
        },
        {
            "obligation": "coherent_dual_row_extraction_and_schmidt_flattening",
            "resolved": False,
            "resolution": (
                "No polynomial isometry extracts an aligned column partner and "
                "flattens the sector Schmidt spectrum without factorial cost."
            ),
        },
    ]
    return CoherentFourierDecoderReport(
        created_at=utc_now(),
        theorem_contract={
            "ideal_fourier_state": (
                "|F_g>=direct_sum_nu sqrt(d_nu/|G|) vec(rho_nu(g))."
            ),
            "candidate_state": (
                "|psi_g>=direct_sum_nu sqrt(p_nu)(rho_nu(g) tensor I)|phi_nu>."
            ),
            "sector_quality": (
                "f_nu=d_nu^-1/2 sum_i sqrt(lambda_nu,i), where lambda are "
                "row-column Schmidt probabilities."
            ),
            "exact_success": (
                "P=[sum_nu d_nu sqrt(p_nu/|G|) f_nu]^2."
            ),
            "perfect_case": (
                "p_nu=d_nu^2/|G| and f_nu=1 for all nu imply exact output g."
            ),
            "physical_decoder_schema": (
                "Coherently align multiplicity as the dual row register, flatten "
                "Schmidt spectra, reweight sectors to Plancherel, then apply the "
                "inverse S_n QFT."
            ),
            "critical_boundary": (
                "The inverse QFT is polynomial; coherent carrier normalization "
                "and reweighting are the unresolved algorithmic core."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=proof_obligations,
        adversarial_audit=[
            {
                "objection": "An efficient inverse S_n QFT alone is a decoder.",
                "resolved": False,
                "resolution": (
                    "Only for ideal matrix-coefficient amplitudes. The physical "
                    "carrier's sector weights and Schmidt spectra are unproved."
                ),
            },
            {
                "objection": "Correct sector weights compensate for poor entanglement.",
                "resolved": True,
                "resolution": (
                    "Equation (1) contains both factors. Rank-one sector carriers "
                    "lose a factor 1/sqrt(d_nu) in amplitude."
                ),
            },
            {
                "objection": "Measuring nu and preparing the same weights later is equivalent.",
                "resolved": False,
                "resolution": (
                    "It destroys the cross-sector phases carrying the common group "
                    "element and is ruled out by the isotypic-dephasing no-go."
                ),
            },
            {
                "objection": "The n! outcomes force an n!-size classical table.",
                "resolved": True,
                "resolution": (
                    "A permutation uses O(n log n) bits and inverse group Fourier "
                    "synthesis produces it algorithmically; carrier normalization, "
                    "not outcome enumeration, is the core obstruction."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "beals-1997-symmetric-group-qft",
                "title": "Quantum computation of Fourier transforms over symmetric groups",
                "url": BEALS_PAPER_URL,
                "use": "Polynomial implementation of the final S_n inverse QFT.",
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics={
            "matrix_coefficient_fourier_basis_theorem_count": 1,
            "coherent_fourier_success_formula_theorem_count": 1,
            "perfect_plancherel_maximal_entanglement_decoder_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "ideal_control_success_probability": (
                ideal.predicted_correct_label_probability
            ),
            "minimum_mismatch_control_success_probability": min(
                row.predicted_correct_label_probability for row in controls[1:]
            ),
            "scaling_record_count": len(scaling),
            "efficient_inverse_symmetric_group_qft_count": len(scaling),
            "physical_sector_weight_match_theorem_count": 0,
            "coherent_dual_row_extraction_count": 0,
            "sector_schmidt_flattening_count": 0,
            "polynomial_sector_reweighting_count": 0,
            "end_to_end_fourier_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "coherent_fourier_decoder_criterion_proved": verified,
            "ideal_matrix_coefficient_state_decodes_exactly": verified,
            "efficient_inverse_symmetric_group_qft_available": True,
            "physical_filtered_sector_weights_match_plancherel": False,
            "coherent_dual_row_extraction_proved": False,
            "sector_schmidt_flattening_proved": False,
            "polynomial_sector_reweighting_proved": False,
            "end_to_end_hidden_permutation_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact coherent Fourier target and success formula are now "
                "known, and the final inverse S_n QFT is efficient. The physical "
                "carrier has not been transformed to the required Plancherel, "
                "maximally entangled matrix-coefficient form."
            ),
        },
        status=(
            "coherent-fourier-decoder-target-proved-carrier-normalization-open"
            if verified
            else "coherent-fourier-decoder-validation-failure"
        ),
        summary=(
            "Derived and validated the exact cross-sector Fourier decoding "
            "criterion, reducing hidden-permutation output to coherent sector "
            "reweighting and row-multiplicity entanglement normalization before "
            "an efficient inverse S_n QFT."
        ),
        falsifiers_triggered=[
            (
                "Independent sector decoding is unnecessary in the ideal case "
                "and impossible at constant success after dephasing; coherent "
                "matrix-coefficient synthesis is the correct target."
            ),
            (
                "An n!-outcome table is not intrinsically required: inverse S_n "
                "Fourier synthesis outputs the permutation in O(n log n) bits."
            ),
            (
                "Plancherel sector weights alone are insufficient; row-column "
                "Schmidt flatness enters multiplicatively in the exact amplitude."
            ),
            (
                "No speedup follows until physical carrier extraction, flattening, "
                "reweighting, and classical separation are proved."
            ),
        ],
    )


def write_coherent_fourier_decoder_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COHERENT-FOURIER-DECODER"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_coherent_fourier_decoder())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_coherent_fourier_decoder_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
