"""Shape-resolved label probe for the exact stable Racah sector family.

The stable final sector of W_n^tensor3, with W_n=(n-2,2) and
xi_n=(n-3,2,1), routes through exactly nine padded intermediate shapes.
Seven of those shapes have nontrivial second-stage Kronecker multiplicity.
This module tests one uniform bounded-support Hamiltonian on every such block:

    H_eta,n = sum rho_eta(tau) tensor rho_W(c),

where tau is a transposition, c is an oriented three-cycle, and their
supports intersect in two points.  A separating Young--Jucys--Murphy
functional extracts one xi_n tableau block without materializing the full
Hamiltonian.  The same equivariant multiplicity action occurs on every
xi_n tableau block.

Finite spectral splitting is only a theorem target.  It is not an exact
all-n characteristic polynomial, a normalized gap proof, a coherent LCU
implementation, a complete associator, or a hidden-involution decoder.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy.sparse.linalg import eigsh

from coset_sparse_stable_gap_probe import (
    _apply_orbit_hamiltonian,
    _sparse_encoded_yjm,
    separating_yjm_weights,
)
from coset_stable_shape_family_certificate import (
    FINAL_TAIL,
    STABLE_TAILS,
    padded_partition,
)
from representation_obstruction import hook_length_dimension
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_STABLE_SHAPE_LABEL_PATH = Path(
    "research/representation/coset_stable_shape_label_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SHAPE-LABEL-PROBE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class StableShapeLabelRecord:
    n: int
    intermediate_tail: tuple[int, ...]
    source_partition: tuple[int, ...]
    intermediate_partition: tuple[int, ...]
    final_partition: tuple[int, ...]
    first_stage_multiplicity: int
    second_stage_multiplicity: int
    branch_dimension: int
    intermediate_irrep_dimension: int
    source_irrep_dimension: int
    extracted_tensor_dimension: int
    target_yjm_label: int
    minimum_yjm_label_separation: int
    sparse_yjm_nonzero_count: int
    target_eigenspace_residual: float
    target_eigenspace_relative_residual: float
    target_basis_orthogonality_residual: float
    orbit_generator_id: str
    orbit_term_count: int
    orbit_term_count_formula: int
    eigenvalues: tuple[float, ...]
    integer_characteristic_polynomial_candidate: tuple[int, ...]
    integer_polynomial_reconstruction_residual: float
    integer_polynomial_relative_reconstruction_residual: float
    exact_integer_polynomial_candidate: bool
    raw_minimum_gap: float
    lcu_normalized_minimum_gap: float
    nontrivial_multiplicity_fully_split: bool
    coherent_normalized_gap_already_proved: bool
    finite_numerical_probe_only: bool
    status: str


@dataclass(frozen=True)
class StableShapeLabelReport:
    created_at: str
    mathematical_contract: dict[str, object]
    records: list[StableShapeLabelRecord]
    shape_summaries: list[dict[str, object]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def audit_stable_shape_label(
    n: int, intermediate_tail: tuple[int, ...]
) -> StableShapeLabelRecord:
    if n < 8:
        raise ValueError("the exact nine-shape endpoint starts at n=8")
    if intermediate_tail not in STABLE_TAILS:
        raise ValueError("intermediate tail is outside the proved nine-shape family")

    source = padded_partition(n, (2,))
    intermediate = padded_partition(n, intermediate_tail)
    final = padded_partition(n, FINAL_TAIL)
    first_multiplicity = kronecker_coefficient(source, source, intermediate)
    second_multiplicity = kronecker_coefficient(intermediate, source, final)
    if first_multiplicity <= 0 or second_multiplicity <= 0:
        raise ArithmeticError("proved stable shape has a zero finite-n multiplicity")

    weights, target_label, separation, _ = separating_yjm_weights(n, final)
    encoded_yjm = _sparse_encoded_yjm(intermediate, source, weights)
    eigenvalues, basis = eigsh(
        encoded_yjm,
        k=second_multiplicity,
        sigma=float(target_label) + 0.125,
        which="LM",
        tol=1e-12,
        maxiter=30_000,
    )
    eigenspace_residual = float(
        np.linalg.norm(encoded_yjm @ basis - basis @ np.diag(eigenvalues))
    )
    relative_residual = eigenspace_residual / max(1.0, abs(target_label))
    label_error = float(np.max(np.abs(eigenvalues - target_label)))
    if label_error > max(1e-4, separation * 1e-8):
        raise ArithmeticError("sparse eigensolver did not recover the target YJM block")

    hamiltonian_basis, term_count = _apply_orbit_hamiltonian(
        intermediate, source, basis, support_intersection=2
    )
    block = basis.T @ hamiltonian_basis
    hermitian_block = (block + block.T) / 2
    spectrum = np.linalg.eigvalsh(hermitian_block)
    polynomial = np.poly(spectrum)
    rounded_polynomial = np.rint(polynomial)
    polynomial_residual = float(np.max(np.abs(polynomial - rounded_polynomial)))
    relative_polynomial_residual = polynomial_residual / max(
        1.0, float(np.max(np.abs(rounded_polynomial)))
    )
    integer_candidate = (
        polynomial_residual < 1e-4 or relative_polynomial_residual < 1e-10
    )
    nontrivial = second_multiplicity > 1
    raw_gap = float(min(np.diff(spectrum))) if nontrivial else 0.0
    fully_split = not nontrivial or raw_gap > 1e-8
    already_proved = intermediate_tail == FINAL_TAIL
    return StableShapeLabelRecord(
        n=n,
        intermediate_tail=intermediate_tail,
        source_partition=source,
        intermediate_partition=intermediate,
        final_partition=final,
        first_stage_multiplicity=first_multiplicity,
        second_stage_multiplicity=second_multiplicity,
        branch_dimension=first_multiplicity * second_multiplicity,
        intermediate_irrep_dimension=hook_length_dimension(intermediate),
        source_irrep_dimension=hook_length_dimension(source),
        extracted_tensor_dimension=encoded_yjm.shape[0],
        target_yjm_label=target_label,
        minimum_yjm_label_separation=separation,
        sparse_yjm_nonzero_count=encoded_yjm.nnz,
        target_eigenspace_residual=eigenspace_residual,
        target_eigenspace_relative_residual=relative_residual,
        target_basis_orthogonality_residual=float(
            np.linalg.norm(basis.T @ basis - np.eye(second_multiplicity))
        ),
        orbit_generator_id="ORB-TC-INTERSECTION-2",
        orbit_term_count=term_count,
        orbit_term_count_formula=n * (n - 1) * (n - 2),
        eigenvalues=tuple(float(value) for value in spectrum),
        integer_characteristic_polynomial_candidate=tuple(
            int(value) for value in rounded_polynomial
        ),
        integer_polynomial_reconstruction_residual=polynomial_residual,
        integer_polynomial_relative_reconstruction_residual=(
            relative_polynomial_residual
        ),
        exact_integer_polynomial_candidate=integer_candidate,
        raw_minimum_gap=raw_gap,
        lcu_normalized_minimum_gap=(raw_gap / term_count if nontrivial else 0.0),
        nontrivial_multiplicity_fully_split=fully_split,
        coherent_normalized_gap_already_proved=already_proved,
        finite_numerical_probe_only=True,
        status=(
            "coherent-normalized-gap-already-proved"
            if already_proved
            else (
                "finite-uniform-orbit-label-target-found"
                if fully_split and integer_candidate
                else "finite-shape-label-probe-inconclusive"
            )
        ),
    )


def build_stable_shape_label_report(
    n_values: Sequence[int] = (8, 9, 10),
) -> StableShapeLabelReport:
    audited_n = tuple(sorted(set(int(value) for value in n_values)))
    if not audited_n or min(audited_n) < 8:
        raise ValueError("n_values must contain sizes at least 8")
    records = [
        audit_stable_shape_label(n, tail)
        for n in audited_n
        for tail in STABLE_TAILS
    ]
    nontrivial = [record for record in records if record.second_stage_multiplicity > 1]
    unresolved = [
        record
        for record in nontrivial
        if not record.coherent_normalized_gap_already_proved
    ]
    shape_summaries: list[dict[str, object]] = []
    for tail in STABLE_TAILS:
        rows = [record for record in records if record.intermediate_tail == tail]
        nontrivial_rows = [row for row in rows if row.second_stage_multiplicity > 1]
        shape_summaries.append(
            {
                "intermediate_tail": list(tail),
                "second_stage_multiplicity": rows[0].second_stage_multiplicity,
                "all_audited_sizes_split": all(
                    row.nontrivial_multiplicity_fully_split for row in rows
                ),
                "minimum_observed_raw_gap": min(
                    (row.raw_minimum_gap for row in nontrivial_rows), default=0.0
                ),
                "minimum_observed_lcu_normalized_gap": min(
                    (
                        row.lcu_normalized_minimum_gap
                        for row in nontrivial_rows
                    ),
                    default=0.0,
                ),
                "integer_polynomial_candidate_at_every_size": all(
                    row.exact_integer_polynomial_candidate for row in rows
                ),
                "coherent_normalized_gap_proved": all(
                    row.coherent_normalized_gap_already_proved for row in rows
                ),
                "proof_target": (
                    "already closed by exact stable-shape certificate"
                    if tail == FINAL_TAIL
                    else (
                        "derive exact characteristic polynomial and normalized root separation"
                        if rows[0].second_stage_multiplicity > 1
                        else "multiplicity one; no internal label split required"
                    )
                ),
            }
        )

    metrics: dict[str, int | float] = {
        "scaling_point_count": len(audited_n),
        "minimum_n": min(audited_n),
        "maximum_n": max(audited_n),
        "stable_shape_count": len(STABLE_TAILS),
        "nontrivial_second_stage_shape_count": sum(
            summary["second_stage_multiplicity"] > 1
            for summary in shape_summaries
        ),
        "finite_nontrivial_block_count": len(nontrivial),
        "finite_fully_split_nontrivial_block_count": sum(
            record.nontrivial_multiplicity_fully_split for record in nontrivial
        ),
        "unproved_shape_finite_target_count": sum(
            all(
                row.nontrivial_multiplicity_fully_split
                and row.exact_integer_polynomial_candidate
                for row in unresolved
                if row.intermediate_tail == tail
            )
            for tail in STABLE_TAILS
            if tail != FINAL_TAIL
            and any(
                row.intermediate_tail == tail for row in unresolved
            )
        ),
        "minimum_observed_unproved_shape_raw_gap": min(
            record.raw_minimum_gap for record in unresolved
        ),
        "minimum_observed_unproved_shape_lcu_normalized_gap": min(
            record.lcu_normalized_minimum_gap for record in unresolved
        ),
        "maximum_target_eigenspace_relative_residual": max(
            record.target_eigenspace_relative_residual for record in records
        ),
        "maximum_integer_polynomial_relative_reconstruction_residual": max(
            record.integer_polynomial_relative_reconstruction_residual
            for record in records
        ),
        "uniform_orbit_generator_count": 1,
        "new_exact_all_n_characteristic_polynomial_count": 0,
        "new_normalized_gap_theorem_count": 0,
        "new_coherent_shape_label_count": 0,
        "uniform_polynomial_racah_circuit_count": 0,
    }
    all_split = (
        metrics["finite_fully_split_nontrivial_block_count"]
        == metrics["finite_nontrivial_block_count"]
    )
    all_integer = all(
        record.exact_integer_polynomial_candidate for record in records
    )
    expected_unproved_targets = 6
    target_count = metrics["unproved_shape_finite_target_count"]
    return StableShapeLabelReport(
        created_at=utc_now(),
        mathematical_contract={
            "source_family": "W_n=(n-2,2)",
            "final_family": "xi_n=(n-3,2,1)",
            "intermediate_family": "the exact nine padded shapes from the character-polynomial certificate",
            "operator": (
                "sum rho_eta(tau) tensor rho_W(c) over transpositions tau and oriented three-cycles c "
                "with support intersection two"
            ),
            "operator_term_count": "n(n-1)(n-2)",
            "target_extraction": (
                "one separating YJM tableau label; diagonal equivariance makes the multiplicity spectrum "
                "independent of the chosen final-irrep tableau"
            ),
            "proof_boundary": (
                "floating finite spectra and integer polynomial reconstruction are conjecture targets only"
            ),
        },
        records=records,
        shape_summaries=shape_summaries,
        headline_metrics=metrics,
        claim_gate={
            "uniform_operator_splits_every_audited_nontrivial_shape": all_split,
            "integer_characteristic_polynomial_candidates_at_every_audited_block": all_integer,
            "all_six_unproved_shape_targets_found": target_count
            == expected_unproved_targets,
            "all_n_characteristic_polynomials_proved": False,
            "all_n_normalized_gaps_proved": False,
            "coherent_lcu_implementations_proved": False,
            "complete_racah_associator_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "One uniform orbit Hamiltonian supplies finite theorem targets for the six missing labels, but "
                "those targets still lack exact all-n spectra, normalized gaps, coherent implementation, and a decoder."
            ),
        },
        status=(
            "uniform-finite-label-targets-found-six-all-n-proofs-open"
            if all_split and all_integer and target_count == expected_unproved_targets
            else "stable-shape-label-probe-found-counterexample"
        ),
        summary=(
            f"The same support-intersection-two orbit Hamiltonian split all {len(nontrivial)} audited nontrivial "
            f"blocks across n={min(audited_n)}..{max(audited_n)}, yielding finite integer-polynomial targets for "
            f"all {target_count} previously unproved shape families; no new all-n or coherent label theorem follows."
        ),
        falsifiers_triggered=[
            "Finite splitting at three sizes does not imply an all-n simple spectrum.",
            "Near-integer floating characteristic coefficients are not exact identities.",
            "An observed raw or LCU-normalized gap is not a uniform asymptotic lower bound.",
            "A formal orbit sum is not a compiled coherent SELECT/PREPARE circuit.",
            "Complete intermediate labels would still not constitute a hidden-involution decoder or a classical separation.",
        ],
    )


def write_stable_shape_label_report(
    output_path: Path = COSET_STABLE_SHAPE_LABEL_PATH,
    n_values: Sequence[int] = (8, 9, 10),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_shape_label_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-FINITE-NINE-SHAPE-SPECTRA-AS-COMPLETE-RACAH-LABELS",
                source=str(output_path),
                claim=(
                    "Finite simple spectra from one orbit Hamiltonian close all nine stable Racah shape labels."
                ),
                reason_invalid=(
                    "Six shape families still lack exact all-n characteristic polynomials, normalized root "
                    "separation, and coherent LCU compilation; all labels also lack a complete transition circuit."
                ),
                lesson=(
                    "Use the shape-resolved integer polynomials as exact trace-moment targets, then prove each "
                    "bounded-degree family before attempting coherent phase estimation."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"coset_stable_shape_label_probe": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_shape_label_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
