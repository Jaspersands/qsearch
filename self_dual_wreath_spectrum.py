"""Exact one-copy spectrum for rigid code-equivalence bridge involutions.

The rowspace reduction for rigid length-n codes is a hidden subgroup problem
over

    W_n = (S_n x S_n) semidirect Z_2,

where the nontrivial Z_2 element swaps the two factors.  Hidden permutations
`s in S_n` correspond to bridge involutions

    h_s = (s, s^-1; swap).

These n! elements form one conjugacy class.  Irreducible representations of
`W_n` are:

* one induced representation for each unordered unequal pair (lambda, mu),
  of dimension 2 d_lambda d_mu and bridge character zero;
* two +/- extensions for each equal pair (lambda, lambda), of dimension
  d_lambda^2 and bridge character +/- d_lambda.

This gives the exact class-average frame, weak-Fourier label law, one-copy PGM
success, and one-copy Holevo information.  It also shows precisely what remains:
the k=Theta(log n!) diagonal-action multiplicity algebra, a carrier-sensitive
covariant POVM, and a polynomial hidden-permutation decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_holevo_information import fano_required_information
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


SELF_DUAL_WREATH_SPECTRUM_PATH = Path(
    "research/representation/self_dual_wreath_spectrum.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WreathSpectrumSpec:
    exact_n_values: tuple[int, ...] = (2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 28, 32)
    tail_n_values: tuple[int, ...] = (48, 64)
    bounded_error: float = 1 / 3


@dataclass(frozen=True)
class WreathIrrepClass:
    kind: str
    label_count: str
    dimension_formula: str
    bridge_character_formula: str
    bridge_character_ratio_formula: str
    frame_scalar_formula: str


@dataclass(frozen=True)
class WreathSpectrumRecord:
    n: int
    partition_count: int | None
    wreath_irrep_count: int | None
    log2_group_order: float
    log2_bridge_ensemble_size: float
    exact_representation_sum_of_squares_verified: bool | None
    equal_pair_plancherel_mass: float | None
    frame_support_plancherel_mass: float | None
    exact_one_copy_pgm_success_probability: float | None
    pgm_advantage_over_uniform_guess: float | None
    exact_one_copy_holevo_bits: float | None
    one_copy_holevo_lower_bound: float | None
    one_copy_holevo_upper_bound: float
    coarse_zero_error_copy_lower_bound: int
    exact_bounded_error_copy_lower_bound: int | None
    weak_fourier_label_mutual_information_bits: int
    one_copy_wreath_fourier_schema_explicit: bool
    growing_copy_diagonal_action_transform_proved: bool
    carrier_sensitive_covariant_povm_proved: bool
    polynomial_hidden_permutation_decoder_proved: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathSpectrumReport:
    created_at: str
    spec: WreathSpectrumSpec
    group_model: dict[str, Any]
    irrep_classes: list[WreathIrrepClass]
    records: list[WreathSpectrumRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def wreath_group_order(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    order = math.factorial(n)
    return 2 * order * order


def bridge_class_size(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return math.factorial(n)


def bridge_centralizer_size(n: int) -> int:
    return wreath_group_order(n) // bridge_class_size(n)


def wreath_irrep_dimensions(n: int) -> list[int]:
    dimensions = [
        hook_length_dimension(partition)
        for partition in integer_partitions(n)
    ]
    irreps = []
    for left, left_dimension in enumerate(dimensions):
        irreps.extend((left_dimension * left_dimension,) * 2)
        for right_dimension in dimensions[left + 1 :]:
            irreps.append(2 * left_dimension * right_dimension)
    return irreps


def _diagonal_frame_statistics(
    n: int,
) -> tuple[int, int, float, float, float]:
    order = math.factorial(n)
    dimensions = [
        hook_length_dimension(partition)
        for partition in integer_partitions(n)
    ]
    partition_count = len(dimensions)
    irrep_count = partition_count * (partition_count - 1) // 2 + 2 * partition_count
    sum_dimension_squares = sum(
        dimension * dimension for dimension in dimensions
    )
    representation_sum = 2 * sum_dimension_squares * sum_dimension_squares
    if representation_sum != wreath_group_order(n):
        raise ArithmeticError("wreath irreducible dimensions fail regular-representation sum")

    collision_mass = sum(
        ((dimension * dimension) / order) ** 2
        for dimension in dimensions
    )
    correction = 0.0
    for dimension in dimensions:
        mass = (dimension**4) / wreath_group_order(n)
        inverse_dimension = 1.0 / dimension
        plus = 1.0 + inverse_dimension
        minus = 1.0 - inverse_dimension
        correction += mass * plus * math.log2(plus)
        if minus > 0:
            correction += mass * minus * math.log2(minus)
    holevo = 1.0 - correction
    support_mass = 1.0 - 1.0 / (order * order)
    pgm_success = 2.0 * support_mass / order
    return partition_count, irrep_count, collision_mass, holevo, pgm_success


def audit_wreath_spectrum(
    n: int,
    bounded_error: float = 1 / 3,
    exact: bool = True,
) -> WreathSpectrumRecord:
    ensemble = bridge_class_size(n)
    log_ensemble = math.log2(ensemble)
    if exact:
        (
            partition_count,
            irrep_count,
            collision_mass,
            holevo,
            pgm_success,
        ) = _diagonal_frame_statistics(n)
        holevo_lower = max(0.0, 1.0 - collision_mass)
        required = fano_required_information(log_ensemble, bounded_error)
        bounded_copy_lower = (
            math.ceil(required / holevo) if holevo > 0 else None
        )
        support_mass = 1.0 - 1.0 / (ensemble * ensemble)
        pgm_advantage = pgm_success * ensemble
        verified: bool | None = True
    else:
        partition_count = None
        irrep_count = None
        collision_mass = None
        holevo = None
        pgm_success = None
        holevo_lower = None
        bounded_copy_lower = None
        support_mass = None
        pgm_advantage = None
        verified = None
    return WreathSpectrumRecord(
        n=n,
        partition_count=partition_count,
        wreath_irrep_count=irrep_count,
        log2_group_order=round(math.log2(wreath_group_order(n)), 9),
        log2_bridge_ensemble_size=round(log_ensemble, 9),
        exact_representation_sum_of_squares_verified=verified,
        equal_pair_plancherel_mass=(
            round(collision_mass, 12) if collision_mass is not None else None
        ),
        frame_support_plancherel_mass=(
            round(support_mass, 12) if support_mass is not None else None
        ),
        exact_one_copy_pgm_success_probability=(
            pgm_success if pgm_success is not None else None
        ),
        pgm_advantage_over_uniform_guess=(
            round(pgm_advantage, 12)
            if pgm_advantage is not None
            else None
        ),
        exact_one_copy_holevo_bits=(
            round(holevo, 12) if holevo is not None else None
        ),
        one_copy_holevo_lower_bound=(
            round(holevo_lower, 12) if holevo_lower is not None else None
        ),
        one_copy_holevo_upper_bound=1.0,
        coarse_zero_error_copy_lower_bound=math.ceil(log_ensemble),
        exact_bounded_error_copy_lower_bound=bounded_copy_lower,
        weak_fourier_label_mutual_information_bits=0,
        one_copy_wreath_fourier_schema_explicit=True,
        growing_copy_diagonal_action_transform_proved=False,
        carrier_sensitive_covariant_povm_proved=False,
        polynomial_hidden_permutation_decoder_proved=False,
        status=(
            "exact-one-copy-wreath-spectrum-growing-copy-decoder-open"
            if exact
            else "coarse-tail-copy-bound-growing-copy-decoder-open"
        ),
    )


def run_self_dual_wreath_spectrum(
    spec: WreathSpectrumSpec = WreathSpectrumSpec(),
) -> SelfDualWreathSpectrumReport:
    exact_records = [
        audit_wreath_spectrum(
            n,
            bounded_error=spec.bounded_error,
            exact=True,
        )
        for n in spec.exact_n_values
    ]
    tail_records = [
        audit_wreath_spectrum(
            n,
            bounded_error=spec.bounded_error,
            exact=False,
        )
        for n in spec.tail_n_values
        if n not in spec.exact_n_values
    ]
    records = exact_records + tail_records
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "exact_record_count": len(exact_records),
        "maximum_n": max((record.n for record in records), default=0),
        "exact_irrep_dimension_sum_verification_count": sum(
            record.exact_representation_sum_of_squares_verified is True
            for record in records
        ),
        "weak_fourier_zero_information_record_count": sum(
            record.weak_fourier_label_mutual_information_bits == 0
            for record in records
        ),
        "maximum_exact_pgm_advantage_over_guess": max(
            (
                record.pgm_advantage_over_uniform_guess
                for record in exact_records
                if record.pgm_advantage_over_uniform_guess is not None
            ),
            default=0.0,
        ),
        "minimum_exact_one_copy_holevo_bits": min(
            (
                record.exact_one_copy_holevo_bits
                for record in exact_records
                if record.exact_one_copy_holevo_bits is not None
            ),
            default=0.0,
        ),
        "maximum_coarse_zero_error_copy_lower_bound": max(
            (
                record.coarse_zero_error_copy_lower_bound
                for record in records
            ),
            default=0,
        ),
        "one_copy_wreath_fourier_schema_count": len(records),
        "growing_copy_diagonal_action_transform_count": 0,
        "carrier_sensitive_covariant_povm_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return SelfDualWreathSpectrumReport(
        created_at=utc_now(),
        spec=spec,
        group_model={
            "group": "W_n=(S_n x S_n) semidirect Z_2",
            "multiplication": (
                "(a,b,0)(c,d,e)=(ac,bd,e); "
                "(a,b,1)(c,d,e)=(ad,bc,1+e)"
            ),
            "bridge": "h_s=(s,s^-1,1)",
            "bridge_square": "h_s^2=e",
            "conjugation": "(a,b,0) h_s (a,b,0)^-1 = h_(a s b^-1)",
            "class_size": "n!",
            "centralizer_size": "2 n!",
            "hsp_state": "rho_s=(I+R_(h_s))/|W_n|",
        },
        irrep_classes=[
            WreathIrrepClass(
                kind="unequal-pair-induced",
                label_count="p(n)(p(n)-1)/2",
                dimension_formula="2 d_lambda d_mu",
                bridge_character_formula="0",
                bridge_character_ratio_formula="0",
                frame_scalar_formula="1",
            ),
            WreathIrrepClass(
                kind="equal-pair-plus-minus",
                label_count="2 p(n)",
                dimension_formula="d_lambda^2",
                bridge_character_formula="+/- d_lambda",
                bridge_character_ratio_formula="+/- 1/d_lambda",
                frame_scalar_formula="1 +/- 1/d_lambda",
            ),
        ],
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "correct_code_equivalence_wreath_group_modeled": True,
            "one_copy_frame_and_pgm_spectrally_explicit": True,
            "weak_fourier_labels_identify_hidden_permutation": False,
            "one_copy_pgm_is_hidden_permutation_algorithm": False,
            "growing_copy_diagonal_action_transform_proved": False,
            "carrier_sensitive_covariant_povm_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The correct wreath-product one-copy spectrum is explicit, but "
                "one-copy success is only a factor below two over guessing and "
                "the growing-copy covariant decoder is still missing."
            ),
        },
        status="correct-wreath-spectrum-solved-growing-copy-covariant-decoder-open",
        summary=(
            f"Certified the exact W_n bridge spectrum through n={max(spec.exact_n_values)} "
            f"and coarse copy bounds through n={metrics['maximum_n']}; growing-copy "
            "diagonal-action transforms, carrier-sensitive POVMs, and decoders remain zero."
        ),
        falsifiers_triggered=[
            "The rigid code-equivalence HSP is modeled over W_n, not silently replaced by an S_n involution ensemble.",
            "Weak Fourier irrep labels have exactly zero information about the individual bridge h_s.",
            "One-copy PGM success is less than twice uniform guessing.",
            "One-copy wreath Fourier diagonalization does not construct the growing-copy covariant measurement.",
            "Information-theoretic polynomial copy bounds do not supply a decoder.",
        ],
    )


def write_self_dual_wreath_spectrum(
    path: Path = SELF_DUAL_WREATH_SPECTRUM_PATH,
    spec: WreathSpectrumSpec = WreathSpectrumSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_wreath_spectrum(spec=spec))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-SELF-DUAL-WREATH-ONE-COPY-ALGORITHM",
                source=str(path),
                claim=(
                    "The explicit one-copy wreath-product Fourier spectrum "
                    "already yields a hidden-permutation algorithm."
                ),
                reason_invalid=(
                    "Weak labels contain zero hidden-permutation information and "
                    "one-copy PGM success is below twice uniform guessing."
                ),
                lesson=(
                    "Use the exact wreath spectrum as the base representation "
                    "schema, then solve the growing-copy carrier-sensitive "
                    "covariant measurement and decoder."
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
                artifacts={"self_dual_wreath_spectrum": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_spectrum()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
