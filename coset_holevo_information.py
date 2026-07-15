"""Exact Holevo-information and copy lower bounds for involution coset states.

For a uniform conjugacy class C of involutions in S_n,

    rho_h = (I + R_h) / |S_n|.

Every rho_h has entropy log2|S_n|-1.  The average state is the central class
sum and has eigenvalue (1+r_lambda)/|S_n| with multiplicity d_lambda^2,
where r_lambda=chi_lambda(C)/d_lambda.  Therefore the exact one-copy Holevo
information is

    chi_1 = 1 - sum_lambda (d_lambda^2/|G|)
                         (1+r_lambda) log2(1+r_lambda).

For k copies carrying the same hidden h, entropy subadditivity gives
chi_k <= k chi_1.  Fano's inequality then yields an exact ensemble-specific
copy lower bound for any requested decoding error.  The hard involution rows
approach one bit per copy, so the resulting Omega(log|C|)=Omega(n log n)
requirement is polynomial and does not replace the recoupling/decoder problem.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from coset_state_distinguishability import involution_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from weak_fourier_signal import character_on_involution, involution_specs_for_n


COSET_HOLEVO_INFORMATION_PATH = Path(
    "research/representation/coset_holevo_information.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-HOLEVO-INFORMATION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HolevoTheoremCertificate:
    theorem_id: str
    individual_state_entropy: str
    average_state_spectrum: str
    exact_one_copy_formula: str
    same_hidden_k_copy_bound: str
    fano_bound: str
    zero_error_copy_bound: str
    exact_formula_proved: bool
    multi_copy_subadditivity_proved: bool
    limitations: list[str]


@dataclass(frozen=True)
class CosetHolevoRecord:
    n: int
    involution_type: str
    transposition_count: int
    fixed_point_count: int
    ensemble_size: int
    log2_ensemble_size: float
    average_state_trace: float
    individual_state_entropy: float
    average_state_entropy: float
    exact_one_copy_holevo_bits: float
    universal_one_bit_upper_bound_satisfied: bool
    zero_error_copy_lower_bound: int
    bounded_error: float
    fano_required_information_bits: float
    bounded_error_copy_lower_bound: int
    coarse_zero_error_one_bit_copy_bound: int
    exact_to_coarse_copy_bound_ratio: float
    asymptotic_hard_family: bool
    efficient_collective_measurement_constructed: bool
    polynomial_outcome_decoder_constructed: bool


@dataclass(frozen=True)
class CosetHolevoReport:
    created_at: str
    theorem: HolevoTheoremCertificate
    records: list[CosetHolevoRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def binary_entropy(probability: float) -> float:
    if probability <= 0.0 or probability >= 1.0:
        return 0.0
    return -probability * math.log2(probability) - (
        1.0 - probability
    ) * math.log2(1.0 - probability)


def fano_required_information(log2_ensemble_size: float, error: float) -> float:
    if not 0.0 <= error < 1.0:
        raise ValueError("error must lie in [0,1)")
    if log2_ensemble_size <= 0.0:
        return 0.0
    # Evaluate log2(M-1) from log2(M) directly.  Forming M overflows for the
    # asymptotic rows where this bound is most useful.
    if log2_ensemble_size > 53.0:
        log2_ensemble_minus_one = log2_ensemble_size
    else:
        inverse_size = 2.0 ** (-log2_ensemble_size)
        log2_ensemble_minus_one = log2_ensemble_size + math.log2(
            max(1.0 - inverse_size, 2.0**-1074)
        )
    return max(
        0.0,
        log2_ensemble_size
        - binary_entropy(error)
        - error * max(0.0, log2_ensemble_minus_one),
    )


def exact_one_copy_holevo(
    n: int, transposition_count: int
) -> tuple[float, float, float]:
    order = math.factorial(n)
    average_entropy = 0.0
    trace = 0.0
    correction = 0.0
    for partition in integer_partitions(n):
        dimension = hook_length_dimension(partition)
        character = character_on_involution(partition, transposition_count)
        ratio = character / dimension
        scalar = 1.0 + ratio
        mass = dimension * dimension / order
        trace += mass * scalar
        if scalar <= 0.0:
            continue
        eigenvalue = scalar / order
        multiplicity = dimension * dimension
        average_entropy -= multiplicity * eigenvalue * math.log2(eigenvalue)
        correction += mass * scalar * math.log2(scalar)
    individual_entropy = math.log2(order) - 1.0
    holevo = 1.0 - correction
    if abs(holevo - (average_entropy - individual_entropy)) > 1e-9:
        raise ArithmeticError("spectral and entropy Holevo formulas disagree")
    return trace, average_entropy, holevo


def build_holevo_theorem() -> HolevoTheoremCertificate:
    return HolevoTheoremCertificate(
        theorem_id="THEOREM-COSET-EXACT-HOLEVO-COPY-LOWER-BOUND",
        individual_state_entropy="S(rho_h)=log2|S_n|-1",
        average_state_spectrum=(
            "eigenvalue (1+chi_lambda(C)/d_lambda)/|S_n| with multiplicity d_lambda^2"
        ),
        exact_one_copy_formula=(
            "chi_1=1-sum_lambda d_lambda^2/|G|*(1+r_lambda)*log2(1+r_lambda)"
        ),
        same_hidden_k_copy_bound=(
            "chi({|C|^-1,rho_h^tensor k}) <= k*chi_1 by entropy subadditivity and additive individual entropies"
        ),
        fano_bound=(
            "k >= [log2|C|-h2(epsilon)-epsilon*log2(|C|-1)]/chi_1"
        ),
        zero_error_copy_bound="k >= log2|C|/chi_1",
        exact_formula_proved=True,
        multi_copy_subadditivity_proved=True,
        limitations=[
            "The bound is information-theoretic and constructs no collective measurement.",
            "A polynomial copy lower bound is not evidence against a polynomial quantum algorithm.",
            "The theorem does not solve internal Kronecker transforms, associators, frame inversion, or decoding.",
            "Numerical rows evaluate an exact character formula but are not an asymptotic expansion of chi_1.",
        ],
    )


def audit_coset_holevo(
    n: int,
    transposition_count: int,
    involution_type: str,
    error: float = 1 / 3,
) -> CosetHolevoRecord:
    ensemble_size = involution_count(n, transposition_count)
    log_ensemble = math.log2(ensemble_size) if ensemble_size > 1 else 0.0
    trace, average_entropy, holevo = exact_one_copy_holevo(
        n, transposition_count
    )
    if holevo <= 0.0 and ensemble_size > 1:
        zero_error = math.inf
        bounded = math.inf
    else:
        zero_error = math.ceil(log_ensemble / holevo) if holevo else 0
        required = fano_required_information(log_ensemble, error)
        bounded = math.ceil(required / holevo) if holevo else 0
    coarse = math.ceil(log_ensemble)
    required = fano_required_information(log_ensemble, error)
    return CosetHolevoRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        fixed_point_count=n - 2 * transposition_count,
        ensemble_size=ensemble_size,
        log2_ensemble_size=log_ensemble,
        average_state_trace=trace,
        individual_state_entropy=math.log2(math.factorial(n)) - 1.0,
        average_state_entropy=average_entropy,
        exact_one_copy_holevo_bits=holevo,
        universal_one_bit_upper_bound_satisfied=holevo <= 1.0 + 1e-10,
        zero_error_copy_lower_bound=int(zero_error),
        bounded_error=error,
        fano_required_information_bits=required,
        bounded_error_copy_lower_bound=int(bounded),
        coarse_zero_error_one_bit_copy_bound=coarse,
        exact_to_coarse_copy_bound_ratio=(zero_error / coarse if coarse else 1.0),
        asymptotic_hard_family=involution_type != "single_transposition_control",
        efficient_collective_measurement_constructed=False,
        polynomial_outcome_decoder_constructed=False,
    )


def build_coset_holevo_report(
    n_values: Sequence[int] = (6, 8, 10, 12, 14, 16, 20),
    error: float = 1 / 3,
) -> CosetHolevoReport:
    records = [
        audit_coset_holevo(n, transpositions, label, error=error)
        for n in n_values
        for label, transpositions in involution_specs_for_n(n)
    ]
    hard = [record for record in records if record.asymptotic_hard_family]
    metrics: dict[str, int | float] = {
        "exact_holevo_formula_count": len(records),
        "multi_copy_subadditivity_theorem_count": 1,
        "fano_copy_lower_bound_count": len(records),
        "hard_family_row_count": len(hard),
        "minimum_hard_family_one_copy_holevo_bits": min(
            (record.exact_one_copy_holevo_bits for record in hard), default=0.0
        ),
        "maximum_hard_family_one_copy_holevo_bits": max(
            (record.exact_one_copy_holevo_bits for record in hard), default=0.0
        ),
        "maximum_hard_family_zero_error_copy_lower_bound": max(
            (record.zero_error_copy_lower_bound for record in hard), default=0
        ),
        "maximum_hard_family_bounded_error_copy_lower_bound": max(
            (record.bounded_error_copy_lower_bound for record in hard), default=0
        ),
        "maximum_exact_to_coarse_copy_bound_ratio": max(
            (record.exact_to_coarse_copy_bound_ratio for record in records),
            default=1.0,
        ),
        "polynomial_collective_measurement_count": 0,
        "polynomial_outcome_decoder_count": 0,
    }
    return CosetHolevoReport(
        created_at=utc_now(),
        theorem=build_holevo_theorem(),
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "exact_one_copy_holevo_information_proved": True,
            "same_hidden_multi_copy_upper_bound_proved": True,
            "omega_log_ensemble_copy_lower_bound_certified": True,
            "copy_lower_bound_is_superpolynomial": False,
            "efficient_collective_measurement_constructed": False,
            "polynomial_outcome_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact Holevo/Fano accounting requires Omega(log|C|) copies, which is Omega(n log n) for the hard "
                "involution ensembles but remains polynomial. The open bottlenecks are coherent recoupling, transition "
                "filtering, and compressed hidden-involution decoding."
            ),
        },
        status="exact-copy-lower-bound-proved-recoupling-decoder-open",
        summary=(
            f"Computed exact one-copy Holevo information and rigorous multi-copy lower bounds for {len(records)} "
            f"involution ensembles. Maximum hard-family zero-error lower bound="
            f"{metrics['maximum_hard_family_zero_error_copy_lower_bound']} copies; no measurement or decoder constructed."
        ),
        falsifiers_triggered=[
            "Any mechanism using fewer than the certified Holevo/Fano copy bound is rejected.",
            "Pairwise Hilbert-Schmidt overlap is not substituted for accessible information.",
            "The polynomial Omega(n log n) lower bound is not promoted as a no-algorithm theorem.",
            "Information sufficiency does not construct internal Kronecker, associator, transition-filter, or decoder circuits.",
        ],
    )


def write_coset_holevo_report(
    output_path: Path = COSET_HOLEVO_INFORMATION_PATH,
    n_values: Sequence[int] = (6, 8, 10, 12, 14, 16, 20),
    error: float = 1 / 3,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_coset_holevo_report(n_values=n_values, error=error))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negatives = (
            (
                "NEG-COSET-UNDERCHARGED-HOLEVO-COPY-BUDGET",
                "A collective hidden-involution decoder may use fewer than the exact Holevo/Fano copy lower bound.",
                "Entropy subadditivity bounds k-copy information by k times the exact one-copy character formula.",
            ),
            (
                "NEG-COSET-POLYNOMIAL-COPY-LOWER-BOUND-AS-NO-ALGORITHM",
                "The Omega(n log n) hard-family copy requirement rules out a polynomial quantum algorithm.",
                "The certified copy count is polynomial; it only rules out under-sampled mechanisms.",
            ),
        )
        for negative_id, claim, reason in negatives:
            upsert_negative_result(
                NegativeResultRecord(
                    id=negative_id,
                    source=str(output_path),
                    claim=claim,
                    reason_invalid=reason,
                    lesson=(
                        "Charge the exact copy lower bound, then focus research on uniform recoupling circuits, "
                        "state-dependent frame action, and a compressed verified decoder."
                    ),
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-COSET-HOLEVO"
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
                artifacts={"coset_holevo_information": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_coset_holevo_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
