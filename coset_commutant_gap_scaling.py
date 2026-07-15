"""Uniform gap probe for a fixed Kronecker-multiplicity commutant family.

The family is

    lambda_n = mu_n = (n-2, 2),

and the Hamiltonian is fixed uniformly as the sum of
rho_lambda(tau) tensor rho_mu(c) over oriented 3-cycles c and transpositions
tau whose support is contained in the support of c.  There are exactly
n(n-1)(n-2) unitary LCU terms.

Finite data suggests that the multiplicity-two target (n-3,2,1) has raw gap
2(n-2), hence normalized gap 2/[n(n-1)].  This module verifies that identity
on finite sectors and records it as an explicit conjecture, not a theorem.
Proving the all-n identity would close the spectral-gap part of one coherent
multiplicity-basis route, but not the Racah/transition/decoder obligations.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from coset_jucys_murphy_label_transform import (
    diagonal_jucys_murphy_operators,
    encoded_jucys_murphy_operator,
)
from coset_multiplicity_commutant_search import (
    _encoded_label_targets,
    transposition_three_cycle_intersection_operator,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_COMMUTANT_GAP_SCALING_PATH = Path(
    "research/representation/coset_commutant_gap_scaling.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-COMMUTANT-GAP-SCALING"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class MultiplicityTargetGapRecord:
    target_partition: tuple[int, ...]
    kronecker_multiplicity: int
    tableau_label_count: int
    raw_gap: float
    lcu_normalized_gap: float
    predicted_critical_raw_gap: float | None
    predicted_critical_normalized_gap: float | None
    critical_formula_residual: float | None
    tableau_spectrum_consistency_residual: float


@dataclass(frozen=True)
class CommutantGapScalingRecord:
    n: int
    source_partition: tuple[int, ...]
    source_irrep_dimension: int
    tensor_dimension: int
    lcu_term_count: int
    proved_lcu_term_count_formula: int
    term_count_formula_verified: bool
    nontrivial_multiplicity_target_count: int
    maximum_kronecker_multiplicity: int
    target_gaps: list[MultiplicityTargetGapRecord]
    critical_target: tuple[int, ...]
    critical_target_present: bool
    critical_raw_gap: float
    predicted_critical_raw_gap: float
    critical_normalized_gap: float
    predicted_critical_normalized_gap: float
    critical_gap_formula_residual: float
    all_nontrivial_targets_split: bool
    all_other_target_gaps_at_least_critical: bool
    finite_dense_verification_only: bool
    status: str


@dataclass(frozen=True)
class CommutantGapScalingReport:
    created_at: str
    family_contract: dict[str, object]
    conjecture: dict[str, object]
    records: list[CommutantGapScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_commutant_gap_scaling(n: int) -> CommutantGapScalingRecord:
    if n < 6:
        raise ValueError("the stable multiplicity-two family starts at n=6")
    partition = (n - 2, 2)
    operator, term_count = transposition_three_cycle_intersection_operator(
        partition, partition, support_intersection=2
    )
    base = 2 * n + 1
    yjm_encoded = encoded_jucys_murphy_operator(
        diagonal_jucys_murphy_operators(partition, partition), base, n
    )
    label_values, label_vectors = np.linalg.eigh(yjm_encoded)
    label_indices: dict[int, list[int]] = {}
    for index, value in enumerate(label_values):
        label_indices.setdefault(round(float(value)), []).append(index)
    target_by_label = _encoded_label_targets(n, base)

    spectra_by_target: dict[tuple[int, ...], list[np.ndarray]] = {}
    for label, indices in label_indices.items():
        if len(indices) <= 1:
            continue
        block = label_vectors[:, indices].T @ operator @ label_vectors[:, indices]
        spectra_by_target.setdefault(target_by_label[label], []).append(
            np.linalg.eigvalsh(block)
        )

    normalization = n * (n - 1) * (n - 2)
    critical_target = (n - 3, 2, 1)
    predicted_raw = 2.0 * (n - 2)
    predicted_normalized = 2.0 / (n * (n - 1))
    target_records: list[MultiplicityTargetGapRecord] = []
    for target in sorted(spectra_by_target, reverse=True):
        spectra = spectra_by_target[target]
        reference = spectra[0]
        consistency = max(
            (float(np.linalg.norm(spectrum - reference)) for spectrum in spectra[1:]),
            default=0.0,
        )
        gap = float(min(np.diff(reference), default=math.inf))
        is_critical = target == critical_target
        target_records.append(
            MultiplicityTargetGapRecord(
                target_partition=target,
                kronecker_multiplicity=kronecker_coefficient(partition, partition, target),
                tableau_label_count=len(spectra),
                raw_gap=gap,
                lcu_normalized_gap=gap / normalization,
                predicted_critical_raw_gap=predicted_raw if is_critical else None,
                predicted_critical_normalized_gap=(
                    predicted_normalized if is_critical else None
                ),
                critical_formula_residual=(abs(gap - predicted_raw) if is_critical else None),
                tableau_spectrum_consistency_residual=consistency,
            )
        )
    critical = next(
        (record for record in target_records if record.target_partition == critical_target),
        None,
    )
    critical_gap = critical.raw_gap if critical else 0.0
    multiplicities = [
        kronecker_coefficient(partition, partition, target)
        for target in integer_partitions(n)
    ]
    return CommutantGapScalingRecord(
        n=n,
        source_partition=partition,
        source_irrep_dimension=hook_length_dimension(partition),
        tensor_dimension=hook_length_dimension(partition) ** 2,
        lcu_term_count=term_count,
        proved_lcu_term_count_formula=normalization,
        term_count_formula_verified=term_count == normalization,
        nontrivial_multiplicity_target_count=len(target_records),
        maximum_kronecker_multiplicity=max(multiplicities),
        target_gaps=target_records,
        critical_target=critical_target,
        critical_target_present=critical is not None,
        critical_raw_gap=critical_gap,
        predicted_critical_raw_gap=predicted_raw,
        critical_normalized_gap=critical_gap / normalization,
        predicted_critical_normalized_gap=predicted_normalized,
        critical_gap_formula_residual=abs(critical_gap - predicted_raw),
        all_nontrivial_targets_split=bool(target_records)
        and all(record.raw_gap > 1e-7 for record in target_records),
        all_other_target_gaps_at_least_critical=bool(critical)
        and all(record.raw_gap + 1e-7 >= critical_gap for record in target_records),
        finite_dense_verification_only=True,
        status=(
            "critical-inverse-quadratic-gap-formula-finite-verified"
            if critical is not None and abs(critical_gap - predicted_raw) < 1e-7
            else "uniform-gap-conjecture-counterexample"
        ),
    )


def build_commutant_gap_scaling_report(
    n_values: Sequence[int] = (6, 7, 8, 9, 10),
) -> CommutantGapScalingReport:
    records = [audit_commutant_gap_scaling(n) for n in n_values]
    formula_verified = all(record.critical_gap_formula_residual < 1e-7 for record in records)
    all_split = all(record.all_nontrivial_targets_split for record in records)
    log_n = np.log(np.asarray([record.n for record in records], dtype=float))
    log_gap = np.log(
        np.asarray([record.critical_normalized_gap for record in records], dtype=float)
    )
    slope = float(np.polyfit(log_n, log_gap, 1)[0]) if len(records) > 1 else 0.0
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "minimum_n": min(n_values),
        "maximum_n": max(n_values),
        "term_count_formula_verified_count": sum(
            record.term_count_formula_verified for record in records
        ),
        "critical_gap_formula_finite_verified_count": sum(
            record.critical_gap_formula_residual < 1e-7 for record in records
        ),
        "all_nontrivial_targets_split_count": sum(
            record.all_nontrivial_targets_split for record in records
        ),
        "all_n_critical_gap_theorem_count": 0,
        "minimum_observed_critical_normalized_gap": min(
            record.critical_normalized_gap for record in records
        ),
        "maximum_critical_gap_formula_residual": max(
            record.critical_gap_formula_residual for record in records
        ),
        "empirical_log_log_gap_slope": slope,
        "kcopy_associator_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return CommutantGapScalingReport(
        created_at=utc_now(),
        family_contract={
            "source_partitions": "lambda_n=mu_n=(n-2,2), n>=6",
            "uniform_hamiltonian": (
                "H_n=sum rho_lambda(tau) tensor rho_mu(c), over oriented 3-cycles c and transpositions tau contained in supp(c)"
            ),
            "coefficient_rule": "one for every orbit term, independent of n and the target sector",
            "lcu_term_count_theorem": "6*C(n,3)=n(n-1)(n-2)",
            "access_model": "controlled Young-basis group actions after the polynomial S_n QFT",
        },
        conjecture={
            "id": "CONJ-COSET-COMMUTANT-RAW-GAP-NMINUS3-2-1",
            "statement": (
                "On the multiplicity-two target nu=(n-3,2,1), H_n has eigenvalue gap exactly 2(n-2) for every n>=6."
            ),
            "consequence_if_proved": (
                "The LCU-normalized gap is 2/[n(n-1)], so multiplicity-label phase estimation is polynomial on this family."
            ),
            "proof_status": "finite-verified-all-n-proof-open",
            "required_proof_route": (
                "Evaluate trace and determinant of the 2x2 multiplicity action using the 2-subset permutation module, "
                "partition algebra, or exact character-orbit sums."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "uniform_coefficient_rule": True,
            "lcu_normalization_formula_proved": True,
            "critical_gap_formula_finite_verified": formula_verified,
            "all_n_critical_gap_formula_proved": False,
            "conditional_polynomial_multiplicity_transform": True,
            "unconditional_polynomial_multiplicity_transform": False,
            "kcopy_associator_polynomial_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The same Hamiltonian has the predicted inverse-quadratic normalized gap on every finite row, but "
                "finite interpolation is not an all-n proof and neither associators nor decoding are constructed."
            ),
        },
        status=(
            "uniform-inverse-quadratic-gap-conjecture-survives-finite-scaling"
            if formula_verified and all_split
            else "uniform-commutant-gap-conjecture-falsified"
        ),
        summary=(
            f"Tested one uniform commutant Hamiltonian on lambda=(n-2,2) for n={list(n_values)}; "
            f"the predicted 2/[n(n-1)] normalized critical gap matched {sum(record.critical_gap_formula_residual < 1e-7 for record in records)}/{len(records)} rows."
        ),
        falsifiers_triggered=[
            "Optimizing coefficients independently at each n is rejected as nonuniform advice.",
            "Finite exact-looking gap formulas are retained as conjectures until an all-n representation-theoretic proof exists.",
            "A gapped one-tree multiplicity Hamiltonian does not supply Racah associators or a hidden-involution decoder.",
        ],
    )


def write_commutant_gap_scaling_report(
    output_path: Path = COSET_COMMUTANT_GAP_SCALING_PATH,
    n_values: Sequence[int] = (6, 7, 8, 9, 10),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_commutant_gap_scaling_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-NONUNIFORM-COMMUTANT-COEFFICIENT-SEARCH",
                source=str(output_path),
                claim="Independently optimized finite-n commutant coefficients define a uniform quantum transform.",
                reason_invalid=(
                    "An n- and sector-specific coefficient table is nonuniform advice. The scaling probe therefore "
                    "uses one fixed support-intersection-two orbit Hamiltonian at every n."
                ),
                lesson="Require a closed coefficient rule and normalized-gap theorem before circuit promotion.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-FINITE-GAP-INTERPOLATION-AS-THEOREM",
                source=str(output_path),
                claim="Agreement with 2/[n(n-1)] on finite rows proves the all-n multiplicity gap.",
                reason_invalid=(
                    "Finite numerical spectra do not prove the exact multiplicity action or exclude a later gap collapse."
                ),
                lesson=(
                    "Derive the 2x2 multiplicity trace and determinant symbolically from the 2-subset module or orbit characters."
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
                artifacts={"coset_commutant_gap_scaling": str(output_path)},
            )
        )
    return payload
