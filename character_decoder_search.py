"""Non-exhaustive decoder search for multiplicative-character shifts.

The character-shift baseline shows that Legendre/quartic shifts can be isolated
with few samples if all field elements are enumerated.  That is a query/time
gap, not positive quantum evidence.  This module tries a small but explicit set
of non-exhaustive classical decoders and records whether any of them actually
recover the shift.  Exhaustive candidate scoring is allowed only as a baseline
and is labelled as domain-linear in the field size.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from phase_state_workbench import apply_hidden_shift, generate_cyclic_phase_family
from research_registry import upsert_scaling_run, utc_now


CHARACTER_DECODER_SEARCH_PATH = Path("research/classical_baselines/character_decoder_search.json")


@dataclass(frozen=True)
class DecoderAttemptRecord:
    family_id: str
    n_bits: int
    modulus: int
    sample_count: int
    true_shift: int
    decoder_name: str
    access_model: str
    non_exhaustive: bool
    recovered_shift: int | None
    success: bool
    query_count: int
    candidate_operations: int
    degree_operations: int
    polynomial_style: bool
    decoder_class: str
    time_class: str
    status: str
    verdict: str
    notes: str


@dataclass(frozen=True)
class ShiftInvariantProbeRecord:
    family_id: str
    n_bits: int
    modulus: int
    probe_name: str
    tested_shifts: list[int]
    max_signature_variation: float
    status: str
    interpretation: str


@dataclass(frozen=True)
class CharacterDecoderFamilySummary:
    family_id: str
    tested_n_bits: list[int]
    tested_sample_counts: list[int]
    non_exhaustive_success_count: int
    pair_ratio_filter_success_count: int
    algebraic_degree_exponential_success_count: int
    exhaustive_success_count: int
    shift_invariant_probe_count: int
    best_verdict: str
    lesson: str


def _sample_positions(domain_size: int, sample_count: int, seed: int) -> list[int]:
    rng = np.random.default_rng(seed)
    if sample_count <= domain_size:
        return [int(item) for item in rng.choice(domain_size, size=sample_count, replace=False).tolist()]
    return [int(item) for item in rng.integers(0, domain_size, size=sample_count).tolist()]


def _character_instance(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int,
    seed: int,
) -> tuple[Any, np.ndarray, np.ndarray, list[int], np.ndarray, int]:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    if spec.id not in {"legendre_symbol", "quartic_character"}:
        raise ValueError(f"character decoder search only supports multiplicative-character families, got {spec.id}")
    true_shift = int(shift) % spec.domain_size
    shifted = apply_hidden_shift(spec, signal, true_shift)
    positions = _sample_positions(spec.domain_size, sample_count, seed)
    observed = shifted[positions]
    return spec, signal, shifted, positions, observed, true_shift


def phase_frequency_decoder_attempt(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int = 7,
    seed: int = 0,
) -> DecoderAttemptRecord:
    spec, _signal, _shifted, _positions, observed, true_shift = _character_instance(
        family_id, n_bits, sample_count, shift, seed
    )
    labels = sorted((round(float(value.real), 8), round(float(value.imag), 8)) for value in observed)
    label_histogram_size = len(set(labels))
    return DecoderAttemptRecord(
        family_id=spec.id,
        n_bits=spec.n_bits,
        modulus=spec.modulus,
        sample_count=int(sample_count),
        true_shift=true_shift,
        decoder_name="phase_frequency_histogram",
        access_model="random_sample",
        non_exhaustive=True,
        recovered_shift=None,
        success=False,
        query_count=int(sample_count),
        candidate_operations=0,
        degree_operations=0,
        polynomial_style=True,
        decoder_class="shift-invariant-statistic",
        time_class="polynomial-sample-shift-invariant-statistic",
        status="failed-shift-invariant",
        verdict="no-shift-information",
        notes=(
            f"Observed {label_histogram_size} phase label(s), but the label histogram is translation-invariant "
            "and cannot identify the hidden shift."
        ),
    )


def _same_phase(left: complex, right: complex) -> bool:
    return abs(complex(left) - complex(right)) <= 1e-8


def pair_ratio_candidate_filter_attempt(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int = 7,
    seed: int = 0,
    pair_cap: int = 64,
) -> DecoderAttemptRecord:
    """Filter candidate shifts using multiplicative-character ratios between samples.

    For observations y_i = chi(x_i + s), the ratio y_i * conj(y_j) is a
    low-degree-looking relation in the unknown shift, but testing it against a
    public character evaluator still scans candidate shifts.  A success is
    therefore a domain-linear dequantization baseline to beat, not a
    polynomial-time decoder in log p.
    """

    spec, signal, _shifted, positions, observed, true_shift = _character_instance(
        family_id, n_bits, sample_count, shift, seed
    )
    pair_indices = [(left, right) for left in range(len(positions)) for right in range(left + 1, len(positions))]
    pair_indices = pair_indices[: max(0, int(pair_cap))]
    candidates = list(range(spec.domain_size))
    candidate_operations = 0
    first_unique_pair_index: int | None = None

    for pair_index, (left_index, right_index) in enumerate(pair_indices, start=1):
        left_position = positions[left_index]
        right_position = positions[right_index]
        observed_ratio = complex(observed[left_index]) * complex(observed[right_index]).conjugate()
        next_candidates: list[int] = []
        for candidate in candidates:
            candidate_operations += 1
            left_value = complex(signal[(left_position + candidate) % spec.domain_size])
            right_value = complex(signal[(right_position + candidate) % spec.domain_size])
            predicted_ratio = left_value * right_value.conjugate()
            if _same_phase(predicted_ratio, observed_ratio):
                next_candidates.append(candidate)
        candidates = next_candidates
        if len(candidates) <= 1:
            first_unique_pair_index = pair_index
            break

    recovered_shift = candidates[0] if len(candidates) == 1 else None
    success = recovered_shift == true_shift
    status = "success-pair-ratio-candidate-filter" if success else "ambiguous-pair-ratio-candidate-filter"
    return DecoderAttemptRecord(
        family_id=spec.id,
        n_bits=spec.n_bits,
        modulus=spec.modulus,
        sample_count=int(sample_count),
        true_shift=true_shift,
        decoder_name="pair_ratio_candidate_filter",
        access_model="random_sample_plus_public_evaluator",
        non_exhaustive=False,
        recovered_shift=recovered_shift,
        success=bool(success),
        query_count=int(sample_count),
        candidate_operations=int(candidate_operations),
        degree_operations=0,
        polynomial_style=False,
        decoder_class="pair-ratio-candidate-filter",
        time_class="domain-linear-exponential-in-encoded-length",
        status=status,
        verdict=(
            "query-efficient-but-pair-ratio-candidate-filtering"
            if success and sample_count <= max(8, 4 * spec.n_bits)
            else "pair-ratio-candidate-filter-baseline"
            if success
            else "pair-ratio-filter-ambiguous"
        ),
        notes=(
            f"Used {len(pair_indices)} sample-pair ratio constraint(s); first unique pair index={first_unique_pair_index}; "
            f"remaining candidates={len(candidates)}. This exploits algebraic pair ratios but still scans candidate shifts."
        ),
    )


def _poly_trim(poly: Sequence[int], modulus: int) -> list[int]:
    values = [int(item) % modulus for item in poly]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return values or [0]


def _poly_is_zero(poly: Sequence[int], modulus: int) -> bool:
    return len(_poly_trim(poly, modulus)) == 1 and _poly_trim(poly, modulus)[0] == 0


def _poly_monic(poly: Sequence[int], modulus: int) -> list[int]:
    values = _poly_trim(poly, modulus)
    if _poly_is_zero(values, modulus):
        return [0]
    inverse = pow(values[-1], -1, modulus)
    return [(coefficient * inverse) % modulus for coefficient in values]


def _poly_mod(dividend: Sequence[int], divisor: Sequence[int], modulus: int) -> list[int]:
    rem = _poly_trim(dividend, modulus)
    div = _poly_trim(divisor, modulus)
    if _poly_is_zero(div, modulus):
        raise ZeroDivisionError("polynomial division by zero")
    div_inverse = pow(div[-1], -1, modulus)
    while len(rem) >= len(div) and not _poly_is_zero(rem, modulus):
        scale = (rem[-1] * div_inverse) % modulus
        offset = len(rem) - len(div)
        for index, coefficient in enumerate(div):
            rem[offset + index] = (rem[offset + index] - scale * coefficient) % modulus
        rem = _poly_trim(rem, modulus)
    return rem


def _poly_gcd(left: Sequence[int], right: Sequence[int], modulus: int) -> list[int]:
    a = _poly_trim(left, modulus)
    b = _poly_trim(right, modulus)
    while not _poly_is_zero(b, modulus):
        a, b = b, _poly_mod(a, b, modulus)
    return _poly_monic(a, modulus)


def _poly_mul_linear(poly: Sequence[int], constant_term: int, modulus: int) -> list[int]:
    values = _poly_trim(poly, modulus)
    result = [0] * (len(values) + 1)
    for degree, coefficient in enumerate(values):
        result[degree] = (result[degree] + coefficient * constant_term) % modulus
        result[degree + 1] = (result[degree + 1] + coefficient) % modulus
    return _poly_trim(result, modulus)


def _shifted_power_constraint(position: int, degree: int, target: int, modulus: int, include_zero: bool) -> list[int]:
    """Return (S + position)^degree - target, optionally multiplied by S + position.

    Character implementations map zero to the phase 1 for total functions.  A
    phase-1 observation can therefore mean either a genuine character value of
    one or the hidden zero.  Multiplying by S + position keeps the true shift in
    the constraint set without granting an oracle that marks zero separately.
    """

    position = int(position) % modulus
    coefficients = [0] * (int(degree) + 1)
    for power in range(int(degree) + 1):
        coefficients[power] = (math.comb(int(degree), power) * pow(position, int(degree) - power, modulus)) % modulus
    coefficients[0] = (coefficients[0] - int(target)) % modulus
    if include_zero:
        return _poly_mul_linear(coefficients, position, modulus)
    return _poly_trim(coefficients, modulus)


def _quartic_phase_exponent(value: complex) -> int | None:
    if abs(value.real - 1.0) < 1e-8 and abs(value.imag) < 1e-8:
        return 0
    if abs(value.real) < 1e-8 and abs(value.imag - 1.0) < 1e-8:
        return 1
    if abs(value.real + 1.0) < 1e-8 and abs(value.imag) < 1e-8:
        return 2
    if abs(value.real) < 1e-8 and abs(value.imag + 1.0) < 1e-8:
        return 3
    return None


def _character_constraint_for_observation(spec: Any, value: complex) -> tuple[int, int, bool]:
    prime = int(spec.modulus)
    if spec.id == "legendre_symbol":
        degree = (prime - 1) // 2
        if abs(value.real + 1.0) < 1e-8 and abs(value.imag) < 1e-8:
            return degree, prime - 1, False
        if abs(value.real - 1.0) < 1e-8 and abs(value.imag) < 1e-8:
            return degree, 1, True
        raise ValueError(f"unsupported Legendre observation {value!r}")
    if spec.id == "quartic_character":
        exponent = _quartic_phase_exponent(value)
        if exponent is None:
            raise ValueError(f"unsupported quartic observation {value!r}")
        primitive_root = int(spec.parameters["primitive_root"])
        quartic_root = pow(primitive_root, (prime - 1) // 4, prime)
        return (prime - 1) // 4, pow(quartic_root, exponent, prime), exponent == 0
    raise ValueError(f"unsupported character family {spec.id}")


def _linear_root(poly: Sequence[int], modulus: int) -> int | None:
    values = _poly_trim(poly, modulus)
    if len(values) != 2 or values[1] == 0:
        return None
    return int((-values[0] * pow(values[1], -1, modulus)) % modulus)


def cyclotomic_polynomial_gcd_attempt(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int = 7,
    seed: int = 0,
) -> DecoderAttemptRecord:
    spec, _signal, _shifted, positions, observed, true_shift = _character_instance(
        family_id, n_bits, sample_count, shift, seed
    )
    gcd_poly: list[int] | None = None
    max_constraint_degree = 0
    for position, value in zip(positions, observed):
        degree, target, include_zero = _character_constraint_for_observation(spec, complex(value))
        constraint = _shifted_power_constraint(position, degree, target, spec.modulus, include_zero)
        max_constraint_degree = max(max_constraint_degree, len(constraint) - 1)
        gcd_poly = constraint if gcd_poly is None else _poly_gcd(gcd_poly, constraint, spec.modulus)
        if gcd_poly == [1]:
            break

    residual_degree = len(gcd_poly or [0]) - 1
    recovered_shift = _linear_root(gcd_poly or [0], spec.modulus)
    success = recovered_shift == true_shift
    degree_operations = int(max(1, sample_count) * max(1, max_constraint_degree) ** 2)
    status = (
        "success-cyclotomic-gcd-degree-exponential"
        if success
        else "failed-cyclotomic-gcd"
        if residual_degree == 0
        else "ambiguous-cyclotomic-gcd"
    )
    return DecoderAttemptRecord(
        family_id=spec.id,
        n_bits=spec.n_bits,
        modulus=spec.modulus,
        sample_count=int(sample_count),
        true_shift=true_shift,
        decoder_name="cyclotomic_polynomial_gcd",
        access_model="random_sample_plus_public_character_power_constraints",
        non_exhaustive=True,
        recovered_shift=recovered_shift,
        success=bool(success),
        query_count=int(sample_count),
        candidate_operations=0,
        degree_operations=degree_operations,
        polynomial_style=False,
        decoder_class="algebraic-full-degree-gcd",
        time_class="polynomial-in-field-size-exponential-in-encoded-length",
        status=status,
        verdict=(
            "algebraic-degree-exponential-decoding"
            if success
            else "algebraic-gcd-failed"
            if residual_degree == 0
            else "algebraic-gcd-ambiguous"
        ),
        notes=(
            f"Computes a dense cyclotomic polynomial GCD over F_p with residual degree {residual_degree}; "
            "this avoids explicit shift enumeration but still has degree Theta(p), so it is a decoding-time baseline, "
            "not a polynomial-time dequantization in log p."
        ),
    )


def _pairwise_signature(values: np.ndarray) -> tuple[float, ...]:
    size = values.size
    signatures = []
    for delta in range(1, min(size, 16)):
        correlation = np.mean(np.conjugate(values) * np.roll(values, -delta))
        signatures.append(round(float(correlation.real), 10))
        signatures.append(round(float(correlation.imag), 10))
    return tuple(signatures)


def pairwise_difference_invariance_probe(
    family_id: str,
    n_bits: int,
    shift: int = 7,
) -> ShiftInvariantProbeRecord:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    if spec.id not in {"legendre_symbol", "quartic_character"}:
        raise ValueError(f"character decoder search only supports multiplicative-character families, got {spec.id}")
    tested = sorted({0, 1 % spec.domain_size, int(shift) % spec.domain_size, (int(shift) + 3) % spec.domain_size})
    signatures = [_pairwise_signature(apply_hidden_shift(spec, signal, item)) for item in tested]
    reference = np.array(signatures[0], dtype=float)
    max_variation = 0.0
    for signature in signatures[1:]:
        max_variation = max(max_variation, float(np.max(np.abs(reference - np.array(signature, dtype=float)))))
    status = "shift-invariant-obstruction" if max_variation <= 1e-9 else "shift-dependent-pairwise-signal"
    interpretation = (
        "Full-domain pairwise difference correlations are shift-invariant; this class of non-exhaustive statistic cannot decode the shift."
        if status == "shift-invariant-obstruction"
        else "Pairwise correlations vary with shift; inspect for a possible non-exhaustive decoder."
    )
    return ShiftInvariantProbeRecord(
        family_id=spec.id,
        n_bits=spec.n_bits,
        modulus=spec.modulus,
        probe_name="full_domain_pairwise_difference_correlation",
        tested_shifts=tested,
        max_signature_variation=max_variation,
        status=status,
        interpretation=interpretation,
    )


def exhaustive_moment_signature_attempt(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int = 7,
    seed: int = 0,
    max_degree: int = 3,
) -> DecoderAttemptRecord:
    spec, signal, _shifted, positions, observed, true_shift = _character_instance(
        family_id, n_bits, sample_count, shift, seed
    )
    position_array = np.asarray(positions, dtype=np.int64)
    powers = [np.mod(position_array.astype(object) ** degree, spec.modulus).astype(float) for degree in range(max_degree + 1)]
    observed_signature = np.array([np.sum(observed * power) for power in powers], dtype=complex)

    best_shift = 0
    best_score = float("inf")
    for candidate in range(spec.domain_size):
        predicted_values = np.asarray([signal[(position + candidate) % spec.domain_size] for position in positions], dtype=complex)
        candidate_signature = np.array([np.sum(predicted_values * power) for power in powers], dtype=complex)
        score = float(np.linalg.norm(observed_signature - candidate_signature))
        if score < best_score:
            best_score = score
            best_shift = candidate

    success = best_shift == true_shift
    operations = int(spec.domain_size * max(1, sample_count) * (max_degree + 1))
    return DecoderAttemptRecord(
        family_id=spec.id,
        n_bits=spec.n_bits,
        modulus=spec.modulus,
        sample_count=int(sample_count),
        true_shift=true_shift,
        decoder_name="exhaustive_low_moment_signature_scoring",
        access_model="random_sample_plus_public_evaluator",
        non_exhaustive=False,
        recovered_shift=int(best_shift),
        success=bool(success),
        query_count=int(sample_count),
        candidate_operations=operations,
        degree_operations=0,
        polynomial_style=False,
        decoder_class="candidate-enumeration",
        time_class="domain-linear-exponential-in-encoded-length",
        status="success-exhaustive-signature" if success else "failed-exhaustive-signature",
        verdict=(
            "query-efficient-but-exhaustive-decoding"
            if success and sample_count <= max(8, 4 * spec.n_bits)
            else "exhaustive-decoder-baseline"
            if success
            else "exhaustive-moment-signature-failed"
        ),
        notes=(
            f"Scores every candidate shift using moments up to degree {max_degree}; this is a baseline to beat, "
            "not a polynomial-time decoder."
        ),
    )


def decoder_attempts_for_instance(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int = 7,
    seed: int = 0,
) -> list[DecoderAttemptRecord]:
    return [
        phase_frequency_decoder_attempt(family_id, n_bits, sample_count, shift=shift, seed=seed),
        pair_ratio_candidate_filter_attempt(family_id, n_bits, sample_count, shift=shift, seed=seed),
        cyclotomic_polynomial_gcd_attempt(family_id, n_bits, sample_count, shift=shift, seed=seed),
        exhaustive_moment_signature_attempt(family_id, n_bits, sample_count, shift=shift, seed=seed),
    ]


def build_character_decoder_search_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else ["legendre_symbol", "quartic_character"]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    active_samples = list(sample_counts) if sample_counts is not None else [4, 8, 16, 32]

    attempts: list[DecoderAttemptRecord] = []
    probes: list[ShiftInvariantProbeRecord] = []
    for family_id in active_families:
        for n_bits in active_n:
            probes.append(pairwise_difference_invariance_probe(family_id, n_bits, shift=shift))
            for sample_count in active_samples:
                attempts.extend(
                    decoder_attempts_for_instance(
                        family_id,
                        n_bits,
                        sample_count,
                        shift=shift,
                        seed=seed + n_bits * 1009 + sample_count * 17,
                    )
                )

    summaries = build_family_summaries(attempts, probes)
    non_exhaustive_success = sum(1 for item in attempts if item.polynomial_style and item.success)
    pair_ratio_success = sum(1 for item in attempts if item.decoder_class == "pair-ratio-candidate-filter" and item.success)
    algebraic_success = sum(1 for item in attempts if item.decoder_class == "algebraic-full-degree-gcd" and item.success)
    exhaustive_success = sum(1 for item in attempts if item.decoder_class == "candidate-enumeration" and item.success)
    invariant_obstructions = sum(1 for item in probes if item.status == "shift-invariant-obstruction")

    return {
        "id": "CHARACTER-DECODER-SEARCH-LATEST",
        "created_at": utc_now(),
        "kind": "multiplicative-character-decoder-search",
        "families": active_families,
        "n_values": active_n,
        "sample_counts": active_samples,
        "status": "nonexhaustive-dequantization-found" if non_exhaustive_success else "decoder-lower-bound-debt",
        "attempt_count": len(attempts),
        "probe_count": len(probes),
        "summary": (
            f"Ran {len(attempts)} character-shift decoder attempts and {len(probes)} shift-invariance probes; "
            f"{non_exhaustive_success} polynomial-style decoder(s) succeeded, {pair_ratio_success} pair-ratio "
            f"candidate filter(s) succeeded, {algebraic_success} full-degree algebraic decoder(s) succeeded, "
            f"and {exhaustive_success} candidate-enumeration baseline(s) succeeded."
        ),
        "headline_metrics": {
            "non_exhaustive_success_count": non_exhaustive_success,
            "polynomial_style_success_count": non_exhaustive_success,
            "pair_ratio_filter_success_count": pair_ratio_success,
            "algebraic_degree_exponential_success_count": algebraic_success,
            "exhaustive_decoder_success_count": exhaustive_success,
            "shift_invariant_obstruction_count": invariant_obstructions,
            "failed_polynomial_style_count": sum(1 for item in attempts if item.polynomial_style and not item.success),
            "domain_scale_attempt_count": sum(1 for item in attempts if not item.polynomial_style),
            "domain_linear_attempt_count": sum(1 for item in attempts if not item.polynomial_style),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "decoder_attempts": [asdict(item) for item in attempts],
        "invariance_probes": [asdict(item) for item in probes],
    }


def build_family_summaries(
    attempts: Sequence[DecoderAttemptRecord],
    probes: Sequence[ShiftInvariantProbeRecord],
) -> list[CharacterDecoderFamilySummary]:
    family_ids = sorted({item.family_id for item in attempts} | {item.family_id for item in probes})
    summaries: list[CharacterDecoderFamilySummary] = []
    for family_id in family_ids:
        family_attempts = [item for item in attempts if item.family_id == family_id]
        family_probes = [item for item in probes if item.family_id == family_id]
        non_exhaustive_success = sum(1 for item in family_attempts if item.polynomial_style and item.success)
        pair_ratio_success = sum(
            1 for item in family_attempts if item.decoder_class == "pair-ratio-candidate-filter" and item.success
        )
        algebraic_success = sum(1 for item in family_attempts if item.decoder_class == "algebraic-full-degree-gcd" and item.success)
        exhaustive_success = sum(1 for item in family_attempts if item.decoder_class == "candidate-enumeration" and item.success)
        invariant_count = sum(1 for item in family_probes if item.status == "shift-invariant-obstruction")
        if non_exhaustive_success:
            verdict = "reject-character-family-nonexhaustive-decoder"
            lesson = "A polynomial-style decoder recovered the shift; demote this family as dequantized."
        elif algebraic_success:
            verdict = "full-degree-algebraic-decoder-only"
            lesson = (
                "Dense cyclotomic GCD decoding recovers shifts without candidate enumeration, but its degree grows with p; "
                "the remaining question is a decoding-time lower bound, not query evidence."
            )
        elif exhaustive_success:
            verdict = "query-efficient-but-decoding-lower-bound-needed"
            lesson = "Exhaustive candidate scoring succeeds, but no non-exhaustive decoder has been found; prove or refute the decoding gap."
        else:
            verdict = "decoder-search-inconclusive"
            lesson = "Current decoders fail; increase samples and search algebraic/non-exhaustive attacks before treating this as evidence."
        summaries.append(
            CharacterDecoderFamilySummary(
                family_id=family_id,
                tested_n_bits=sorted({item.n_bits for item in family_attempts}),
                tested_sample_counts=sorted({item.sample_count for item in family_attempts}),
                non_exhaustive_success_count=non_exhaustive_success,
                pair_ratio_filter_success_count=pair_ratio_success,
                algebraic_degree_exponential_success_count=algebraic_success,
                exhaustive_success_count=exhaustive_success,
                shift_invariant_probe_count=invariant_count,
                best_verdict=verdict,
                lesson=lesson,
            )
        )
    return summaries


def write_character_decoder_search_report(
    output_path: Path = CHARACTER_DECODER_SEARCH_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_character_decoder_search_report(
        families=families,
        n_values=n_values,
        sample_counts=sample_counts,
        shift=shift,
        seed=seed,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_scaling_run(
            {
                "id": payload["id"],
                "created_at": payload["created_at"],
                "kind": payload["kind"],
                "status": payload["status"],
                "summary": payload["summary"],
                "row_count": payload["attempt_count"],
                "artifacts": {"character_decoder_search": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
    return payload
