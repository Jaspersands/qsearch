"""Exact high-part distribution no-go for carry-sliced subset sum.

Write each uniform label modulo ``2^n`` uniquely as

    a_i = l_i + 2^b h_i,

where ``l_i`` is uniform modulo ``2^b`` and ``h_i`` is independently uniform
modulo ``Q=2^(n-b)``.  After fixing every low label, the target low residue,
and any reachable integer carry ``k``, the high equation is

    sum_i h_i x_i = h_t - k (mod Q).

Translation by ``k`` preserves the uniform target law.  Consequently, a carry
chosen only from low data and target-independent coins cannot bias any
high-only coefficient or target statistic: the quotient instance is exactly a
fresh uniform modular subset-sum instance.  Even if all polynomially many
carries are inspected using high data, a union bound shows that an event with
probability ``p`` on a generic high instance occurs with probability at most
``m p``.

This closes low-only carry selection followed by a standard high-only lattice
attack as a source of new geometry.  It does not close joint low/high lattice
bases, carry-dependent witness-set geometry, or an event already having
inverse-polynomial generic probability.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_CARRY_HIGH_PART_NO_GO_PATH = Path(
    "research/classical_baselines/dcp_carry_high_part_no_go.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-CARRY-HIGH-PART-NOGO"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class CarryHighPartTheoremCertificate:
    decomposition_bijection_proved: bool
    low_high_product_uniformity_proved: bool
    conditional_high_uniformity_proved: bool
    carry_target_translation_bijection_proved: bool
    low_only_carry_selection_no_bias_proved: bool
    polynomial_carry_union_bound_proved: bool
    exponentially_rare_generic_event_remains_exponential: bool
    joint_low_high_geometry_ruled_out: bool
    statement: str
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class CarryHighPartScalingRow:
    n_bits: int
    register_offset: int
    register_count: int
    log_multiplier: int
    constrained_low_bits: int
    quotient_bits: int
    reachable_carry_upper_bound: int
    carry_family_polynomial: bool
    assumed_generic_event_exponent: float
    generic_event_log2_probability: float
    carry_sweep_log2_union_bound: float
    union_bound_exponent_per_n: float
    finite_union_bound_below_one: bool
    asymptotically_exponential_after_sweep: bool


@dataclass(frozen=True)
class CarryHighPartNoGoReport:
    created_at: str
    theorem_contract: dict[str, str]
    theorem_certificate: CarryHighPartTheoremCertificate
    rows: list[CarryHighPartScalingRow]
    exact_controls: list[dict[str, int | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def split_power_of_two_label(value: int, n_bits: int, low_bits: int) -> tuple[int, int]:
    if not 1 <= low_bits < n_bits:
        raise ValueError("low_bits must lie strictly between zero and n_bits")
    modulus = 1 << n_bits
    if not 0 <= value < modulus:
        raise ValueError("value must be a canonical residue modulo 2^n")
    low_modulus = 1 << low_bits
    return value & (low_modulus - 1), value >> low_bits


def compose_power_of_two_label(low: int, high: int, n_bits: int, low_bits: int) -> int:
    if not 1 <= low_bits < n_bits:
        raise ValueError("low_bits must lie strictly between zero and n_bits")
    low_modulus = 1 << low_bits
    high_modulus = 1 << (n_bits - low_bits)
    if not 0 <= low < low_modulus or not 0 <= high < high_modulus:
        raise ValueError("low or high component lies outside its canonical range")
    return low + low_modulus * high


def carry_slice_assignments(
    low_labels: Sequence[int],
    target_low: int,
    low_modulus: int,
    carry: int,
) -> list[tuple[int, ...]]:
    if low_modulus < 2 or low_modulus & (low_modulus - 1):
        raise ValueError("low_modulus must be a power of two")
    if not 0 <= target_low < low_modulus or carry < 0:
        raise ValueError("invalid target residue or carry")
    target_sum = target_low + carry * low_modulus
    return [
        bits
        for bits in itertools.product((0, 1), repeat=len(low_labels))
        if sum(int(label) * bit for label, bit in zip(low_labels, bits)) == target_sum
    ]


def transformed_high_target(target_high: int, carry: int, quotient_modulus: int) -> int:
    if quotient_modulus < 1:
        raise ValueError("quotient_modulus must be positive")
    if not 0 <= target_high < quotient_modulus:
        raise ValueError("target_high must be a canonical quotient residue")
    return (target_high - carry) % quotient_modulus


def high_equation_matches_full_equation(
    labels: Sequence[int],
    target: int,
    assignment: Sequence[int],
    n_bits: int,
    low_bits: int,
) -> bool:
    if len(labels) != len(assignment):
        raise ValueError("labels and assignment lengths differ")
    low_modulus = 1 << low_bits
    quotient_modulus = 1 << (n_bits - low_bits)
    lows, highs = zip(*(split_power_of_two_label(int(label), n_bits, low_bits) for label in labels))
    target_low, target_high = split_power_of_two_label(int(target), n_bits, low_bits)
    low_sum = sum(low * int(bit) for low, bit in zip(lows, assignment))
    delta = low_sum - target_low
    full_valid = sum(int(label) * int(bit) for label, bit in zip(labels, assignment)) % (1 << n_bits) == target
    if delta < 0 or delta % low_modulus:
        return not full_valid
    carry = delta // low_modulus
    high_valid = (
        sum(high * int(bit) for high, bit in zip(highs, assignment))
        - transformed_high_target(target_high, carry, quotient_modulus)
    ) % quotient_modulus == 0
    return full_valid == high_valid


def exact_target_translation_census(
    quotient_modulus: int,
    carry: int,
) -> dict[str, int | bool]:
    if quotient_modulus < 1:
        raise ValueError("quotient_modulus must be positive")
    counts = [0] * quotient_modulus
    for target_high in range(quotient_modulus):
        counts[transformed_high_target(target_high, carry, quotient_modulus)] += 1
    return {
        "quotient_modulus": quotient_modulus,
        "carry": carry,
        "input_target_count": quotient_modulus,
        "output_target_count": sum(counts),
        "minimum_output_multiplicity": min(counts),
        "maximum_output_multiplicity": max(counts),
        "translation_is_bijection": min(counts) == max(counts) == 1,
    }


def carry_union_bound(
    generic_event_probability: float,
    carry_count: int,
) -> float:
    if not 0.0 <= generic_event_probability <= 1.0:
        raise ValueError("generic_event_probability must lie in [0,1]")
    if carry_count < 0:
        raise ValueError("carry_count must be nonnegative")
    return min(1.0, carry_count * generic_event_probability)


def theorem_certificate() -> CarryHighPartTheoremCertificate:
    return CarryHighPartTheoremCertificate(
        decomposition_bijection_proved=True,
        low_high_product_uniformity_proved=True,
        conditional_high_uniformity_proved=True,
        carry_target_translation_bijection_proved=True,
        low_only_carry_selection_no_bias_proved=True,
        polynomial_carry_union_bound_proved=True,
        exponentially_rare_generic_event_remains_exponential=True,
        joint_low_high_geometry_ruled_out=False,
        statement=(
            "Conditioned on arbitrary low labels and target residue, every fixed low-data-selected carry produces an "
            "exactly uniform high-label/high-target subset-sum instance modulo 2^(n-b). For any event E_k on the "
            "translated high instance, Pr[exists reachable k:E_k] <= m max_k Pr[E_k]."
        ),
        proof=(
            "The map a -> (a mod 2^b, floor(a/2^b)) is a bijection from Z_(2^n) to "
            "Z_(2^b) x Z_(2^(n-b)), so uniform labels factor into independent low and high parts. Conditioning on "
            "low data leaves all high parts uniform. For a low assignment with integer carry k, division of the full "
            "equation by 2^b gives sum h_i x_i=h_t-k modulo Q. Translation h_t->h_t-k is a permutation of Z_Q. "
            "Low-only carry selection therefore cannot bias the high instance, and the union bound needs no "
            "independence across the at most m reachable carries."
        ),
        limitations=[
            "A joint lattice basis retaining exact low coordinates is outside the high-only theorem.",
            "The low carry slice restricts the accepted witness set even though the public high instance is uniform.",
            "The theorem does not prove that a generic high-part LLL or BKZ event is exponentially rare.",
            "An inverse-polynomial generic event remains compatible with inverse-polynomial source coverage.",
            "Carry selection using high data is covered only by the event-family union bound, not by a no-adaptivity theorem.",
            "No computational lower bound or subset-sum solver is proved.",
        ],
    )


def scaling_row(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
    generic_event_exponent: float,
) -> CarryHighPartScalingRow:
    if n_bits < 4 or log_multiplier < 1 or generic_event_exponent <= 0:
        raise ValueError("invalid scaling parameters")
    register_count = n_bits + register_offset
    low_bits = min(n_bits - 1, max(1, math.ceil(log_multiplier * math.log2(n_bits))))
    quotient_bits = n_bits - low_bits
    generic_log_probability = -generic_event_exponent * quotient_bits
    union_log_bound = min(0.0, math.log2(max(1, register_count)) + generic_log_probability)
    return CarryHighPartScalingRow(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        log_multiplier=log_multiplier,
        constrained_low_bits=low_bits,
        quotient_bits=quotient_bits,
        reachable_carry_upper_bound=register_count,
        carry_family_polynomial=True,
        assumed_generic_event_exponent=generic_event_exponent,
        generic_event_log2_probability=generic_log_probability,
        carry_sweep_log2_union_bound=union_log_bound,
        union_bound_exponent_per_n=union_log_bound / n_bits,
        finite_union_bound_below_one=union_log_bound < 0,
        asymptotically_exponential_after_sweep=True,
    )


def run_carry_high_part_no_go(
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1, 2),
    generic_event_exponent: float = 0.05,
) -> CarryHighPartNoGoReport:
    rows = [
        scaling_row(n_bits, offset, multiplier, generic_event_exponent)
        for n_bits in n_values
        for offset in register_offsets
        for multiplier in log_multipliers
    ]
    controls = [
        exact_target_translation_census(quotient_modulus, carry)
        for quotient_modulus in (2, 4, 8, 16)
        for carry in range(min(5, quotient_modulus + 1))
    ]
    certificate = theorem_certificate()
    metrics: dict[str, int | float] = {
        "scaling_row_count": len(rows),
        "exact_translation_control_count": len(controls),
        "exact_translation_control_failure_count": sum(
            not bool(control["translation_is_bijection"]) for control in controls
        ),
        "conditional_product_uniformity_theorem_count": 1,
        "low_only_selection_no_bias_theorem_count": 1,
        "polynomial_carry_union_bound_theorem_count": 1,
        "exponential_event_preservation_row_count": sum(
            row.asymptotically_exponential_after_sweep for row in rows
        ),
        "finite_union_bound_below_one_row_count": sum(row.finite_union_bound_below_one for row in rows),
        "joint_low_high_geometry_no_go_count": 0,
        "generic_high_event_exponential_probability_theorem_count": 0,
        "polynomial_witness_solver_count": 0,
        "source_contract_satisfying_row_count": 0,
    }
    return CarryHighPartNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "source": "independent uniform labels and target modulo 2^n",
            "conditioning": "arbitrary exposed low labels/target residue and a reachable carry selected from low data",
            "closed_class": "discard low constraints after carry selection and run an ordinary high-only quotient method",
            "multiple_testing": "all reachable carries may be inspected, but their union probability is at most m times the generic event probability",
            "open_class": "joint low/high bases, carry-restricted witness geometry, and generic inverse-polynomial high events",
        },
        theorem_certificate=certificate,
        rows=rows,
        exact_controls=controls,
        headline_metrics=metrics,
        claim_gate={
            "conditional_high_instance_is_exactly_uniform": True,
            "low_only_carry_selection_creates_high_geometry": False,
            "polynomial_carry_sweep_rescues_exponentially_rare_event": False,
            "generic_high_event_proved_exponentially_rare": False,
            "joint_low_high_lattice_geometry_closed": False,
            "polynomial_witness_solver_constructed": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Low-only carry selection leaves the high quotient exactly generic, and a polynomial carry sweep "
                "cannot amplify an exponentially rare generic event to inverse-polynomial mass. The theorem neither "
                "establishes rarity for a concrete LLL event nor closes a genuinely joint low/high basis."
            ),
        },
        status="low-only-carry-high-quotient-exactly-generic-joint-geometry-open",
        summary=(
            f"Proved exact conditional high-part uniformity and a polynomial carry-family union bound; verified "
            f"{len(controls)} target-translation controls and instantiated {len(rows)} scaling rows. No joint-basis "
            "no-go or polynomial witness solver is claimed."
        ),
        falsifiers_triggered=[
            "Choosing a reachable carry from low bits does not create a special high-label or high-target distribution.",
            "Subtracting the carry from the high target is an exact permutation, not a source of algebraic bias.",
            "Trying every polynomially many carry cannot turn an exponentially rare generic high-only event into inverse-polynomial coverage.",
            "A finite high-only LLL improvement must be compared to the same generic quotient distribution and cannot be credited to low-bit selection.",
            "The result must not be cited against joint low/high constraints or without proving the concrete generic event probability.",
        ],
    )


def write_carry_high_part_no_go(
    path: Path = DCP_CARRY_HIGH_PART_NO_GO_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1, 2),
    generic_event_exponent: float = 0.05,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_carry_high_part_no_go(
            n_values=n_values,
            register_offsets=register_offsets,
            log_multipliers=log_multipliers,
            generic_event_exponent=generic_event_exponent,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-LOW-ONLY-CARRY-SELECTION-HIGH-GEOMETRY",
                source=str(path),
                claim=(
                    "Selecting a reachable low carry and discarding the low constraints creates a specially "
                    "distributed high quotient on which a standard lattice solver gains structural advantage."
                ),
                reason_invalid=(
                    "Conditioned on all low data, the high labels remain independent uniform and target translation "
                    "by the carry is a bijection. Every fixed low-selected quotient is exactly a generic random instance."
                ),
                lesson=(
                    "Require a genuinely joint low/high basis or a carry-restricted witness-set theorem. If sweeping "
                    "carries for a high-only event, prove its generic probability and charge the polynomial union bound."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-CARRY-HIGH-PART-NOGO"
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
                artifacts={"dcp_carry_high_part_no_go": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_carry_high_part_no_go()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
