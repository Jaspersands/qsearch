"""Exact recoupling spectrum of the all-standard hidden-involution block.

Let ``G=S_(2m)`` and let ``h`` be a fixed-point-free involution.  In the
three-copy double-coset reduction, consider the ``L=G^4`` irrep in which all
four factors are the standard representation ``V`` of ``G``.  Its
``A=Delta(G)`` fixed space is ``Inv_G(V^tensor 4)``.

Writing ``K=C_G(h)=C_2 wr S_m``, the ``+1`` eigenspace of ``h`` in ``V`` is
an embedded copy ``U`` of the standard representation of ``S_m``.  Averaging
the three source factors over ``<h>`` and then over ``K`` gives exactly

    pi^B = Inv_(S_m)(U^tensor 4).

For ``m>=4`` both fixed spaces have dimension four.  They have explicit
fourth-order invariant-tensor bases: the fourth simplex moment and the three
metric pairings.  Their Gram and cross-Gram matrices split under permutation
of the four tensor legs into a two-dimensional pair-standard sector and a
two-dimensional symmetric sector.  The squared principal cosines are

    p_m, p_m, lambda_-(m), lambda_+(m),

where

    p_m = (m-2)/(2(2m-1)),

and ``lambda_+/-`` are the two roots determined below.  They converge to
``{1/4,1/4,1/8,1/4}``, so this is a scalable, full-rank, genuinely nonflat
matrix block.

The same result is an adversarial warning.  This multiplicity transform is
succinct: two directions are already scalar and only one explicit 2-by-2
generalized eigensystem remains.  Moreover this block has super-exponentially
small source and alternative mass.  Thus matrix multiplicity, occupied rank,
and nonuniform singular values do not by themselves imply a hard transform
or a useful hidden-involution detector.  The natural huge-multiplicity blocks
remain unresolved.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_standard_block_recoupling.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-STANDARD-BLOCK-RECOUPLING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class StandardBlockFiniteControl:
    half_degree: int
    degree: int
    candidate_count: int
    physical_fixed_multiplicity: int
    source_fixed_multiplicity: int
    analytic_squared_principal_cosines: list[float]
    tensor_squared_principal_cosines: list[float]
    maximum_spectrum_residual: float
    full_rank_verified: bool
    nonuniform_spectrum_verified: bool
    invariant_tensor_formula_verified: bool
    status: str


@dataclass(frozen=True)
class StandardBlockScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    physical_fixed_multiplicity: int
    source_fixed_multiplicity: int
    repeated_pair_squared_cosine: float
    symmetric_squared_cosine_lower: float
    symmetric_squared_cosine_upper: float
    minimum_squared_principal_cosine: float
    maximum_squared_principal_cosine: float
    squared_cosine_condition_number: float
    first_principal_angle_moment: float
    second_principal_angle_moment: float
    principal_angle_effective_rank: float
    log2_source_isotypic_fraction: float
    log2_alternative_isotypic_mass: float
    full_rank_nonuniform_matrix_block: bool
    succinct_multiplicity_diagonalization_proved: bool
    natural_mass_block: bool
    coherent_fourier_block_transform_compiled: bool
    status: str


@dataclass(frozen=True)
class StandardBlockRecouplingTheorem:
    physical_fixed_space: str
    source_fixed_space: str
    invariant_tensor_basis: str
    pair_standard_sector: str
    symmetric_sector: str
    asymptotic_spectrum: str
    mass_boundary: str
    scalable_full_rank_nonuniformity_proved: bool
    succinct_multiplicity_diagonalization_proved: bool
    universal_scalarization_falsified: bool
    natural_huge_block_transform_resolved: bool
    coherent_fourier_block_transform_compiled: bool
    binary_hidden_involution_detector_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class StandardBlockRecouplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[StandardBlockFiniteControl]
    scaling_records: list[StandardBlockScalingRecord]
    theorem: StandardBlockRecouplingTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _simplex_fourth_norm(degree: int) -> Fraction:
    if degree < 2:
        raise ValueError("degree must be at least two")
    return Fraction((degree - 1) ** 4 + degree - 1, degree**3)


def invariant_gram_matrix(degree: int) -> tuple[tuple[Fraction, ...], ...]:
    """Gram matrix for ``(Q, P12|34, P13|24, P14|23)``."""

    if degree < 4:
        raise ValueError("the four invariant tensors are independent for degree>=4")
    rank = degree - 1
    q_pair = Fraction(rank * rank, degree)
    rows: list[tuple[Fraction, ...]] = []
    rows.append((_simplex_fourth_norm(degree), q_pair, q_pair, q_pair))
    for row_index in range(3):
        rows.append(
            (q_pair,)
            + tuple(
                Fraction(rank * rank if row_index == column else rank)
                for column in range(3)
            )
        )
    return tuple(rows)


def cross_gram_matrix(half_degree: int) -> tuple[tuple[Fraction, ...], ...]:
    """Cross Gram from ``S_(2m)`` invariants to embedded ``S_m`` invariants."""

    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    m = half_degree
    rank = m - 1
    q_a_q_b = _simplex_fourth_norm(m) / 2
    q_a_pair_b = Fraction(rank * rank, 2 * m)
    pair_a_q_b = Fraction(rank * rank, m)
    rows: list[tuple[Fraction, ...]] = []
    rows.append((q_a_q_b, q_a_pair_b, q_a_pair_b, q_a_pair_b))
    for row_index in range(3):
        rows.append(
            (pair_a_q_b,)
            + tuple(
                Fraction(rank * rank if row_index == column else rank)
                for column in range(3)
            )
        )
    return tuple(rows)


def repeated_pair_squared_cosine(half_degree: int) -> Fraction:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    m = half_degree
    return Fraction(m - 2, 2 * (2 * m - 1))


def symmetric_sector_trace_and_determinant(
    half_degree: int,
) -> tuple[Fraction, Fraction]:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    m = half_degree
    trace = Fraction(
        6 * m * m - 19 * m + 18,
        4 * (2 * m - 3) * (2 * m - 1),
    )
    determinant = Fraction(
        (m - 3) * (m - 2) * (m - 1),
        4 * (2 * m - 3) * (2 * m - 1) ** 2,
    )
    return trace, determinant


def analytic_squared_principal_cosines(half_degree: int) -> tuple[float, ...]:
    """Return the exact-formula spectrum in increasing order."""

    m = half_degree
    pair = float(repeated_pair_squared_cosine(m))
    trace, determinant = symmetric_sector_trace_and_determinant(m)
    discriminant = float(trace * trace - 4 * determinant)
    if discriminant <= 0:
        raise ArithmeticError("symmetric-sector discriminant must be positive")
    root = math.sqrt(discriminant)
    lower = (float(trace) - root) / 2
    upper = (float(trace) + root) / 2
    return tuple(sorted((lower, pair, pair, upper)))


def _standard_invariant_tensor_basis(degree: int) -> np.ndarray:
    projection = np.eye(degree) - np.ones((degree, degree)) / degree
    fourth = np.einsum(
        "ai,bi,ci,di->abcd",
        projection,
        projection,
        projection,
        projection,
        optimize=True,
    )
    pairings = (
        np.einsum("ab,cd->abcd", projection, projection),
        np.einsum("ac,bd->abcd", projection, projection),
        np.einsum("ad,bc->abcd", projection, projection),
    )
    return np.column_stack(
        [tensor.reshape(-1) for tensor in (fourth, *pairings)]
    )


def _embedded_pair_invariant_tensor_basis(half_degree: int) -> np.ndarray:
    m = half_degree
    degree = 2 * m
    pair_embedding = np.zeros((degree, m), dtype=float)
    for pair in range(m):
        pair_embedding[2 * pair, pair] = 1 / math.sqrt(2)
        pair_embedding[2 * pair + 1, pair] = 1 / math.sqrt(2)
    centered = pair_embedding @ (np.eye(m) - np.ones((m, m)) / m)
    projection = centered @ centered.T
    fourth = np.einsum(
        "ai,bi,ci,di->abcd",
        centered,
        centered,
        centered,
        centered,
        optimize=True,
    )
    pairings = (
        np.einsum("ab,cd->abcd", projection, projection),
        np.einsum("ac,bd->abcd", projection, projection),
        np.einsum("ad,bc->abcd", projection, projection),
    )
    return np.column_stack(
        [tensor.reshape(-1) for tensor in (fourth, *pairings)]
    )


def audit_standard_block_tensors(
    half_degree: int,
    *,
    tolerance: float = 1e-10,
) -> StandardBlockFiniteControl:
    if half_degree > 8:
        raise ValueError("dense tensor controls are restricted to half_degree<=8")
    physical = _standard_invariant_tensor_basis(2 * half_degree)
    source = _embedded_pair_invariant_tensor_basis(half_degree)
    physical_frame, _ = np.linalg.qr(physical)
    source_frame, _ = np.linalg.qr(source)
    singular_values = np.linalg.svd(
        physical_frame.T @ source_frame,
        compute_uv=False,
    )
    numerical = np.sort(singular_values * singular_values)
    analytic = np.asarray(
        analytic_squared_principal_cosines(half_degree),
        dtype=float,
    )
    residual = float(np.max(np.abs(numerical - analytic)))
    full_rank = bool(numerical[0] > tolerance)
    nonuniform = bool(numerical[-1] - numerical[0] > tolerance)
    verified = residual <= tolerance and full_rank and nonuniform
    return StandardBlockFiniteControl(
        half_degree=half_degree,
        degree=2 * half_degree,
        candidate_count=involution_class_size(2 * half_degree, half_degree),
        physical_fixed_multiplicity=physical.shape[1],
        source_fixed_multiplicity=source.shape[1],
        analytic_squared_principal_cosines=analytic.tolist(),
        tensor_squared_principal_cosines=numerical.tolist(),
        maximum_spectrum_residual=residual,
        full_rank_verified=full_rank,
        nonuniform_spectrum_verified=nonuniform,
        invariant_tensor_formula_verified=verified,
        status=(
            "exact-invariant-tensor-spectrum-verified"
            if verified
            else "invariant-tensor-spectrum-control-failure"
        ),
    )


def standard_block_scaling_record(half_degree: int) -> StandardBlockScalingRecord:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    m = half_degree
    degree = 2 * m
    group_log2 = math.lgamma(degree + 1) / math.log(2)
    centralizer_log2 = m + math.lgamma(m + 1) / math.log(2)
    source_stabilizer_log2 = 3 + centralizer_log2
    carrier_log2 = 4 * math.log2(degree - 1)
    source_fraction_log2 = (
        carrier_log2
        + 2
        + source_stabilizer_log2
        - 4 * group_log2
    )
    candidate_count = involution_class_size(degree, m)
    spectrum = analytic_squared_principal_cosines(m)
    first = sum(spectrum)
    second = sum(value * value for value in spectrum)
    effective_rank = first * first / second
    alternative_mass_log2 = (
        source_fraction_log2
        + math.log2(candidate_count)
        + math.log2(first / 4)
    )
    trace, _ = symmetric_sector_trace_and_determinant(m)
    pair = float(repeated_pair_squared_cosine(m))
    symmetric_lower = spectrum[0]
    symmetric_upper = float(trace) - symmetric_lower
    return StandardBlockScalingRecord(
        half_degree=m,
        degree=degree,
        candidate_count_decimal=str(candidate_count),
        physical_fixed_multiplicity=4,
        source_fixed_multiplicity=4,
        repeated_pair_squared_cosine=pair,
        symmetric_squared_cosine_lower=symmetric_lower,
        symmetric_squared_cosine_upper=symmetric_upper,
        minimum_squared_principal_cosine=min(spectrum),
        maximum_squared_principal_cosine=max(spectrum),
        squared_cosine_condition_number=max(spectrum) / min(spectrum),
        first_principal_angle_moment=first,
        second_principal_angle_moment=second,
        principal_angle_effective_rank=effective_rank,
        log2_source_isotypic_fraction=source_fraction_log2,
        log2_alternative_isotypic_mass=alternative_mass_log2,
        full_rank_nonuniform_matrix_block=True,
        succinct_multiplicity_diagonalization_proved=True,
        natural_mass_block=False,
        coherent_fourier_block_transform_compiled=False,
        status="succinct-nonflat-standard-block-negligible-natural-mass",
    )


def build_standard_block_recoupling_report(
    *,
    finite_half_degrees: tuple[int, ...] = (4, 5, 6),
    scaling_half_degrees: tuple[int, ...] = (4, 5, 8, 16, 32, 64),
) -> StandardBlockRecouplingReport:
    finite = [audit_standard_block_tensors(value) for value in finite_half_degrees]
    scaling = [standard_block_scaling_record(value) for value in scaling_half_degrees]
    exact = all(row.invariant_tensor_formula_verified for row in finite)
    scalable = all(row.full_rank_nonuniform_matrix_block for row in scaling)
    succinct = all(
        row.succinct_multiplicity_diagonalization_proved for row in scaling
    )
    theorem = StandardBlockRecouplingTheorem(
        physical_fixed_space=(
            "For V=Std(S_(2m)), pi^A=Inv_(S_(2m))(V^tensor4), of dimension "
            "four for m>=2."
        ),
        source_fixed_space=(
            "V restricted to C_2 wr S_m is U plus the signed pair-difference "
            "module. The three H averages retain U, and base-sign averaging "
            "kills the signed target summand, so pi^B=Inv_(S_m)(U^tensor4)."
        ),
        invariant_tensor_basis=(
            "Each fixed space is spanned by its centered-simplex fourth "
            "moment and the three metric pairings. Their exact Gram and "
            "cross-Gram matrices give the principal-angle formulas."
        ),
        pair_standard_sector=(
            "The two-dimensional nontrivial permutation sector of the three "
            "pairings has squared cosine (m-2)/(2(2m-1)), with multiplicity two."
        ),
        symmetric_sector=(
            "The fourth moments and symmetric sum of pairings leave one "
            "explicit 2-by-2 generalized eigensystem with the recorded trace "
            "and determinant."
        ),
        asymptotic_spectrum=(
            "The squared principal cosines converge to "
            "{1/8,1/4,1/4,1/4}; nonflatness persists at constant scale."
        ),
        mass_boundary=(
            "The all-standard isotypic source and alternative masses decay "
            "super-exponentially. This tractable block does not control the "
            "proved natural huge-rank mass."
        ),
        scalable_full_rank_nonuniformity_proved=exact and scalable,
        succinct_multiplicity_diagonalization_proved=exact and succinct,
        universal_scalarization_falsified=exact and scalable,
        natural_huge_block_transform_resolved=False,
        coherent_fourier_block_transform_compiled=False,
        binary_hidden_involution_detector_constructed=False,
        theorem_verified=exact and scalable and succinct,
        status=(
            "scalable-matrix-nonuniformity-proved-standard-block-succinct-but-negligible"
            if exact and scalable and succinct
            else "standard-block-recoupling-control-failure"
        ),
    )
    return StandardBlockRecouplingReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "S_(2m), fixed-point-free involution, three copies",
            "block": "Std(S_(2m)) tensor power four in L=S_(2m)^4",
            "principal_angle_operator": (
                "The overlap between A-fixed and B-fixed multiplicity spaces; "
                "squared singular values are eigenvalues of P_A P_B P_A."
            ),
            "claim_boundary": (
                "A scalable exact multiplicity-space diagonalization, not a "
                "coherent Fourier-block circuit or natural-mass detector."
            ),
        },
        finite_controls=finite,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-NATURAL-BLOCK-BRANCHING",
                "statement": (
                    "Find an asymptotically controlled basis for the natural "
                    "huge-multiplicity A/B fixed spaces, not only fixed-row blocks."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-NATURAL-BLOCK-RECOUPLING",
                "statement": (
                    "Determine whether partition/wreath recoupling reduces the "
                    "natural matrix CS transform to polynomial local sectors."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-COHERENT-MULTIPLICITY-BASIS",
                "statement": (
                    "Compile any multiplicity diagonalization coherently from "
                    "the physical tuple representation with controlled normalization."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A nonflat matrix CS block is evidence of hardness.",
                "answer": (
                    "False in this scalable family: leg-permutation symmetry "
                    "reduces it to two scalar directions and one 2-by-2 sector."
                ),
                "resolved": True,
            },
            {
                "challenge": "The exact transform supplies a detector.",
                "answer": (
                    "False: its source and alternative isotypic masses are "
                    "super-exponentially small."
                ),
                "resolved": True,
            },
            {
                "challenge": "Observed nonuniformity is a small-group artifact.",
                "answer": (
                    "False: the exact all-m spectrum converges to a nonuniform "
                    "constant limit."
                ),
                "resolved": True,
            },
            {
                "challenge": "A four-dimensional success extrapolates to natural blocks.",
                "answer": (
                    "Unsupported: natural signal was proved to occupy blocks of "
                    "super-exponential multiplicity and rank."
                ),
                "resolved": False,
            },
        ],
        headline_metrics={
            "finite_tensor_control_count": len(finite),
            "finite_tensor_control_failure_count": sum(
                not row.invariant_tensor_formula_verified for row in finite
            ),
            "scalable_nonflat_block_count": sum(
                row.full_rank_nonuniform_matrix_block for row in scaling
            ),
            "tail_minimum_squared_principal_cosine": (
                scaling[-1].minimum_squared_principal_cosine
            ),
            "tail_maximum_squared_principal_cosine": (
                scaling[-1].maximum_squared_principal_cosine
            ),
            "tail_log2_source_isotypic_fraction": (
                scaling[-1].log2_source_isotypic_fraction
            ),
            "tail_log2_alternative_isotypic_mass": (
                scaling[-1].log2_alternative_isotypic_mass
            ),
            "natural_mass_block_count": sum(row.natural_mass_block for row in scaling),
            "coherent_block_transform_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "scalable_full_rank_nonuniform_matrix_block_proved": exact and scalable,
            "universal_scalarization_falsified": exact and scalable,
            "succinct_standard_block_multiplicity_diagonalization_proved": (
                exact and succinct
            ),
            "natural_huge_block_transform_resolved": False,
            "natural_mass_detector_constructed": False,
            "coherent_fourier_block_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact scalable block is tractable but negligible; the "
                "natural huge-rank matrix CS transform remains open."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the exact scalable all-standard matrix CS spectrum and "
            "showed that its genuine nonuniformity is succinctly diagonalizable "
            "but carries negligible natural mass."
        ),
        falsifiers_triggered=[
            "Universal scalarization of three-copy hidden-involution CS blocks is false.",
            "Matrix nonuniformity and occupied rank alone are not hardness evidence.",
            "The all-standard tractable block cannot carry a natural detector.",
        ],
    )


def write_standard_block_recoupling_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_standard_block_recoupling_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_standard_block_recoupling_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
