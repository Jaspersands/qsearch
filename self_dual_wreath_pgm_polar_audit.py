"""Operator-frame and PGM polar-decomposition audit for the wreath HSP.

For k copies, let

    P_s = ((I + R(h_s))/2)^{tensor k}

be the support projector of the normalized hidden-subgroup state, and define

    B_k = (1/n!) sum_s P_s.

The mixed-state PGM has effects

    E_s = (1/n!) B_k^{-1/2} P_s B_k^{-1/2}.

Equivalently, if

    A_k = (1/sqrt(n!)) sum_s |s> tensor P_s,

then A_k^* A_k=B_k and the polar isometry A_k B_k^{-1/2} produces the PGM
label register.  This is an exact operator-valued reduction, unlike the scalar
Hilbert-Schmidt Hecke kernel.

There is a compact LCU contract for B_k: expand each P_s over register subsets
and prepare a uniform superposition over s and the subset mask.  However, at
k=ceil(log2(n!)) the exact first and second moments put broad spectral mass at
frame-eigenvalue scale Theta(1/n!), hence polar singular-value scale
Theta(1/sqrt(n!)).  Generic inverse-square-root/QSVT resolution or even an
optimistic coherent candidate search is factorial.  A useful algorithm must
construct a structured carrier preconditioner/transform that bypasses this
normalization scale.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_pgm_success_theorem import pgm_success_lower_bound


SELF_DUAL_WREATH_PGM_POLAR_PATH = Path(
    "research/representation/self_dual_wreath_pgm_polar_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WreathPgmPolarSpec:
    n_values: tuple[int, ...] = (3, 4, 5, 6, 8, 10, 16, 24, 32, 48, 64)
    verifier_repetitions: int = 3


@dataclass(frozen=True)
class WreathPgmPolarRecord:
    n: int
    hidden_label_count_decimal: str
    log2_hidden_label_count: float
    copy_count: int
    subset_mask_count_decimal: str
    subset_to_label_ratio: float
    register_subset_orbit_count: int
    log2_wreath_group_order: float
    log2_kcopy_hilbert_dimension: float
    projector_rank_fraction: float
    average_frame_trace_per_dimension: float
    average_frame_second_moment_per_dimension: float
    average_frame_effective_rank_fraction: float
    frame_eigenvalue_second_moment_scale: float
    polar_singular_value_second_moment_scale: float
    generic_polar_resolution_log2_charge: float
    information_theoretic_pgm_success_lower_bound: float
    constant_information_theoretic_pgm_success_proved: bool
    candidate_test_completeness: float
    candidate_test_single_round_soundness: float
    candidate_test_repeated_soundness: float
    union_bound_false_candidate_mass: float
    optimistic_grover_log2_candidate_queries: float
    permutation_output_bit_count: int
    average_frame_lcu_contract_explicit: bool
    pgm_polar_isometry_formula_explicit: bool
    coherent_candidate_verifier_reuse_proved: bool
    uniform_polynomial_structured_preconditioner_proved: bool
    polynomial_frame_inverse_proved: bool
    carrier_sensitive_povm_circuit_proved: bool
    polynomial_hidden_permutation_decoder_proved: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathPgmPolarReport:
    created_at: str
    spec: WreathPgmPolarSpec
    operator_frame_contract: dict[str, Any]
    access_and_cost_ledger: dict[str, Any]
    literature_links: list[dict[str, Any]]
    records: list[WreathPgmPolarRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def information_threshold_copy_count(n: int) -> int:
    if n < 2:
        raise ValueError("n must be at least two")
    return math.ceil(math.log2(math.factorial(n)))


def normalized_projector_overlap(copy_count: int, same_hidden: bool) -> float:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    return 1.0 if same_hidden else 2.0 ** (-copy_count)


def normalized_average_frame_moments(
    label_count: int,
    copy_count: int,
) -> dict[str, float]:
    """Return moments after dividing traces by the k-copy Hilbert dimension."""

    if label_count < 2:
        raise ValueError("label_count must be at least two")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    subset_count = 1 << copy_count
    trace_per_dimension = 1.0 / subset_count
    second_per_dimension = (
        subset_count + label_count - 1
    ) / (label_count * subset_count * subset_count)
    effective_rank_fraction = label_count / (
        subset_count + label_count - 1
    )
    eigenvalue_second_moment_scale = (
        subset_count + label_count - 1
    ) / (label_count * subset_count)
    return {
        "trace_per_dimension": trace_per_dimension,
        "second_moment_per_dimension": second_per_dimension,
        "effective_rank_fraction": effective_rank_fraction,
        "eigenvalue_second_moment_scale": eigenvalue_second_moment_scale,
        "polar_singular_value_scale": math.sqrt(
            eigenvalue_second_moment_scale
        ),
    }


def audit_wreath_pgm_polar(
    n: int,
    verifier_repetitions: int = 3,
) -> WreathPgmPolarRecord:
    if verifier_repetitions < 1:
        raise ValueError("verifier_repetitions must be positive")
    labels = math.factorial(n)
    copy_count = information_threshold_copy_count(n)
    subset_count = 1 << copy_count
    moments = normalized_average_frame_moments(labels, copy_count)
    single_soundness = normalized_projector_overlap(copy_count, False)
    repeated_soundness = single_soundness**verifier_repetitions
    union_false_mass = (labels - 1) * repeated_soundness
    log_labels = math.log2(labels)
    log_wreath = math.log2(2 * labels * labels)
    polar_scale = moments["polar_singular_value_scale"]
    return WreathPgmPolarRecord(
        n=n,
        hidden_label_count_decimal=str(labels),
        log2_hidden_label_count=round(log_labels, 12),
        copy_count=copy_count,
        subset_mask_count_decimal=str(subset_count),
        subset_to_label_ratio=round(subset_count / labels, 12),
        register_subset_orbit_count=copy_count + 1,
        log2_wreath_group_order=round(log_wreath, 12),
        log2_kcopy_hilbert_dimension=round(copy_count * log_wreath, 12),
        projector_rank_fraction=2.0 ** (-copy_count),
        average_frame_trace_per_dimension=moments["trace_per_dimension"],
        average_frame_second_moment_per_dimension=moments[
            "second_moment_per_dimension"
        ],
        average_frame_effective_rank_fraction=round(
            moments["effective_rank_fraction"], 12
        ),
        frame_eigenvalue_second_moment_scale=moments[
            "eigenvalue_second_moment_scale"
        ],
        polar_singular_value_second_moment_scale=polar_scale,
        generic_polar_resolution_log2_charge=round(
            -math.log2(polar_scale), 12
        ),
        information_theoretic_pgm_success_lower_bound=(
            pgm_success_lower_bound(labels, copy_count)
        ),
        constant_information_theoretic_pgm_success_proved=True,
        candidate_test_completeness=1.0,
        candidate_test_single_round_soundness=single_soundness,
        candidate_test_repeated_soundness=repeated_soundness,
        union_bound_false_candidate_mass=union_false_mass,
        optimistic_grover_log2_candidate_queries=round(log_labels / 2, 12),
        permutation_output_bit_count=copy_count,
        average_frame_lcu_contract_explicit=True,
        pgm_polar_isometry_formula_explicit=True,
        coherent_candidate_verifier_reuse_proved=False,
        uniform_polynomial_structured_preconditioner_proved=False,
        polynomial_frame_inverse_proved=False,
        carrier_sensitive_povm_circuit_proved=False,
        polynomial_hidden_permutation_decoder_proved=False,
        status="exact-polar-reduction-factorial-normalization-barrier",
    )


def run_self_dual_wreath_pgm_polar_audit(
    spec: WreathPgmPolarSpec = WreathPgmPolarSpec(),
) -> SelfDualWreathPgmPolarReport:
    records = [
        audit_wreath_pgm_polar(
            n,
            verifier_repetitions=spec.verifier_repetitions,
        )
        for n in spec.n_values
    ]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "maximum_n": max((record.n for record in records), default=0),
        "operator_frame_polar_reduction_count": sum(
            record.pgm_polar_isometry_formula_explicit for record in records
        ),
        "average_frame_lcu_contract_count": sum(
            record.average_frame_lcu_contract_explicit for record in records
        ),
        "pairwise_candidate_verifier_formula_count": len(records),
        "maximum_copy_count": max(
            (record.copy_count for record in records),
            default=0,
        ),
        "minimum_effective_rank_fraction": min(
            (
                record.average_frame_effective_rank_fraction
                for record in records
            ),
            default=0.0,
        ),
        "maximum_generic_polar_resolution_log2_charge": max(
            (
                record.generic_polar_resolution_log2_charge
                for record in records
            ),
            default=0.0,
        ),
        "maximum_optimistic_grover_log2_candidate_queries": max(
            (
                record.optimistic_grover_log2_candidate_queries
                for record in records
            ),
            default=0.0,
        ),
        "repeated_verifier_union_bound_below_inverse_label_count": sum(
            record.union_bound_false_candidate_mass
            <= 1.0 / int(record.hidden_label_count_decimal)
            for record in records
        ),
        "coherent_candidate_verifier_reuse_count": 0,
        "uniform_polynomial_structured_preconditioner_count": 0,
        "polynomial_frame_inverse_count": 0,
        "carrier_sensitive_povm_circuit_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "all_register_pgm_optimality_proof_count": 0,
        "information_theoretic_constant_pgm_success_theorem_count": 1,
        "minimum_information_theoretic_pgm_success_lower_bound": min(
            record.information_theoretic_pgm_success_lower_bound
            for record in records
        ),
        "speedup_claim_count": 0,
    }
    return SelfDualWreathPgmPolarReport(
        created_at=utc_now(),
        spec=spec,
        operator_frame_contract={
            "support_projector": (
                "P_s=((I+R(h_s))/2)^{tensor k}, rank(P_s)=|W_n|^k/2^k"
            ),
            "average_frame": "B_k=(1/n!) sum_s P_s",
            "analysis_operator": (
                "A_k=(1/sqrt(n!)) sum_s |s> tensor P_s, so A_k^* A_k=B_k"
            ),
            "pgm_effect": (
                "E_s=(1/n!) B_k^{-1/2} P_s B_k^{-1/2}"
            ),
            "pgm_polar_isometry": "V_k=A_k B_k^{-1/2}",
            "outcome": (
                "Measuring the first register of V_k outputs the candidate "
                "permutation s directly in O(n log n) bits."
            ),
            "lcu_expansion": (
                "B_k=(1/(n! 2^k)) sum_s sum_{A subseteq [k]} "
                "tensor_{i in A} R(h_s)_i"
            ),
            "formal_subset_orbit_compression": (
                "Register permutations group subset masks into k+1 Hamming-weight "
                "orbits, but the carrier orbit sums need not commute."
            ),
        },
        access_and_cost_ledger={
            "available_group_primitives": [
                "reversible preparation of a uniform permutation label",
                "controlled construction of h_s=(s,s^-1;swap)",
                "controlled right multiplication in the wreath group basis",
                "uniform subset-mask preparation",
            ],
            "block_encoding_contract": (
                "PREP over (s,A) and SELECT of the corresponding right actions "
                "gives a normalization-one LCU block encoding of B_k, assuming "
                "the listed reversible group primitives."
            ),
            "missing_gate_proof": (
                "A concrete fault-tolerant gate synthesis and error budget for "
                "all reversible group primitives is not registered."
            ),
            "spectral_charge": (
                "At 2^k approximately n!, Tr(B_k^2)/Tr(B_k) is Theta(1/n!), "
                "so the associated polar singular scale is Theta(1/sqrt(n!))."
            ),
            "generic_qsvt_baseline": (
                "A generic inverse-square-root/polar routine must resolve the "
                "factorial singular scale; no polynomial structured "
                "preconditioner is known."
            ),
            "candidate_verifier": (
                "Testing P_t on the state supported by P_s accepts with "
                "probability 1 for t=s and 2^-k otherwise."
            ),
            "optimistic_search_baseline": (
                "Even granting an illegal reusable coherent verifier for the "
                "unknown mixed input, unstructured amplitude amplification "
                "uses Theta(sqrt(n!)) candidate calls."
            ),
            "query_model_warning": (
                "Ordinary coset-state access does not provide a reusable "
                "coherent candidate-verification oracle or a canonical "
                "purification of the mixed state."
            ),
        },
        literature_links=[
            {
                "paper_id": "moore-russell-explicit-multiregister-2005",
                "title": "Explicit Multiregister Measurements for Hidden Subgroup Problems",
                "url": "https://arxiv.org/abs/quant-ph/0504067",
                "scope": (
                    "An explicit information-theoretic multiregister measurement "
                    "can involve every register subset without yielding an "
                    "efficient implementation."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "bacon-childs-van-dam-semidirect-pgm-2005",
                "title": (
                    "From optimal measurement to efficient quantum algorithms "
                    "for the hidden subgroup problem over semidirect product groups"
                ),
                "url": "https://arxiv.org/abs/quant-ph/0504083",
                "scope": (
                    "For tractable semidirect families, efficient PGM "
                    "implementation is tied to solving a separate average-case "
                    "algebraic problem; measurement optimality alone is not an algorithm."
                ),
                "external_theorem_not_reproved_here": True,
            },
        ],
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "operator_valued_frame_formula_explicit": True,
            "normalization_one_lcu_contract_explicit": True,
            "pgm_polar_reduction_explicit": True,
            "information_theoretic_constant_pgm_success_proved": True,
            "ordinary_coset_access_supplies_coherent_reusable_verifier": False,
            "generic_polar_resolution_is_polynomial": False,
            "uniform_polynomial_structured_preconditioner_proved": False,
            "polynomial_frame_inverse_proved": False,
            "carrier_sensitive_povm_circuit_proved": False,
            "all_register_pgm_optimality_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The mixed-state PGM is reduced exactly to a polar isometry "
                "and the average frame has a compact LCU contract, but its "
                "threshold spectral scale is factorial. No structured "
                "preconditioner, polynomial frame inverse, legal coherent "
                "verifier, or efficient decoder is available. Constant PGM "
                "success is now proved information-theoretically."
            ),
        },
        status="operator-frame-polar-reduced-structured-preconditioner-open",
        summary=(
            f"Derived the exact operator-frame polar reduction on "
            f"{len(records)} scaling rows through n={metrics['maximum_n']}. "
            f"The maximum charged polar resolution is 2^"
            f"{metrics['maximum_generic_polar_resolution_log2_charge']:.3f}, "
            "while structured preconditioners, frame inverses, POVM circuits, "
                "and efficient decoders remain zero, despite the separate "
                "constant-success PGM theorem."
        ),
        falsifiers_triggered=[
            (
                "A compact LCU block encoding of the average frame does not "
                "supply its inverse square root at polynomial cost."
            ),
            (
                "At the information threshold, broad frame spectral mass lies "
                "at factorial eigenvalue scale and factorial-square-root polar scale."
            ),
            (
                "A direct permutation output register removes an n!-entry "
                "outcome table, but not the frame-inversion problem."
            ),
            (
                "Candidate projector tests give equality verification, not a "
                "structured search over S_n."
            ),
            (
                "Ordinary mixed coset-state samples cannot be silently upgraded "
                "to reusable coherent verification or canonical purification access."
            ),
        ],
    )


def write_self_dual_wreath_pgm_polar_audit(
    path: Path = SELF_DUAL_WREATH_PGM_POLAR_PATH,
    spec: WreathPgmPolarSpec = WreathPgmPolarSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_wreath_pgm_polar_audit(spec=spec))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_pgm_polar_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
