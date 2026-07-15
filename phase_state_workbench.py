"""Hidden-shift and DHSP phase-state workbench.

This module supplies the first executable research workbench behind the
hidden-shift candidates.  It works with explicit scalable cyclic phase
families, audits their Fourier/derivative structure, runs classical
dequantization baselines, and simulates a Kuperberg-style phase-label sieve for
the dihedral hidden subgroup problem.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


PHASE_WORKBENCH_DIR = Path("research/phase_workbench")
HIDDEN_SHIFT_AUDIT_PATH = PHASE_WORKBENCH_DIR / "hidden_shift_audit.json"


@dataclass(frozen=True)
class PhaseFamilySpec:
    id: str
    group: str
    n_bits: int
    domain_size: int
    modulus: int
    parameters: dict[str, int | str]
    description: str


@dataclass(frozen=True)
class FourierProfile:
    domain_size: int
    entropy_bits: float
    support_99_percent: int
    top_mass: float
    flatness_ratio: float


@dataclass(frozen=True)
class DerivativeProfile:
    sampled_shifts: int
    best_support_99_percent: int
    median_support_99_percent: float
    best_top_mass: float
    interpretation: str


@dataclass(frozen=True)
class ShiftAttackResult:
    name: str
    recovered_shift: int | None
    success: bool
    confidence: float
    cost_model: str
    notes: str
    legal_query_models: list[str]
    sample_count: int | None = None


@dataclass(frozen=True)
class QueryModelAssessment:
    model: str
    legal_attacks: list[str]
    successful_attacks: list[str]
    survives_current_baselines: bool
    notes: str


@dataclass(frozen=True)
class QueryLowerBoundProbe:
    model: str
    baseline: str
    legal: bool
    required_queries_for_constant_signal: int | None
    observed_query_budget: int | None
    verdict: str
    notes: str


@dataclass(frozen=True)
class HiddenShiftAuditRecord:
    family: PhaseFamilySpec
    true_shift: int
    fourier_profile: FourierProfile
    derivative_profile: DerivativeProfile
    autocorrelation_alias_ratio: float
    classical_attacks: list[ShiftAttackResult]
    query_model_assessments: list[QueryModelAssessment]
    query_lower_bound_probes: list[QueryLowerBoundProbe]
    survives_restricted_query_models: list[str]
    dequantization_risk: str
    positive_signal: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class SieveRoundRecord:
    round_index: int
    bucket_bits: int
    input_states: int
    output_states: int
    zero_labels: int
    best_two_adic_valuation: int
    median_two_adic_valuation: float


@dataclass(frozen=True)
class PhaseSieveResult:
    n_bits: int
    modulus: int
    initial_states: int
    final_states: int
    memory_peak: int
    best_two_adic_valuation: int
    reached_target: bool
    target_two_adic_valuation: int
    sample_exponent_log2: float
    memory_exponent_log2: float
    merge_depth: int
    strategy: str
    schedule: list[int]
    rounds: list[SieveRoundRecord]


@dataclass(frozen=True)
class PhaseStateRecord:
    id: str
    modulus: int
    label: int
    two_adic_valuation: int
    phase_expression: str
    source: str
    merge_depth: int
    merge_history: list[str]


@dataclass(frozen=True)
class PhaseStateTrace:
    n_bits: int
    modulus: int
    strategy: str
    input_model: str
    merge_rule: str
    initial_state_count: int
    final_state_count: int
    memory_peak: int
    target_two_adic_valuation: int
    best_two_adic_valuation: int
    reached_target: bool
    success_probability_proxy: float
    sample_exponent_log2: float
    memory_exponent_log2: float
    merge_depth: int
    schedule: list[int]
    rounds: list[SieveRoundRecord]
    survivor_states_sample: list[PhaseStateRecord]
    interpretation: str


@dataclass(frozen=True)
class SieveSearchResult:
    n_bits: int
    sample_count: int
    baseline: PhaseSieveResult
    candidates: list[PhaseSieveResult]
    best_strategy: str
    best_target_success: bool
    best_two_adic_valuation: int
    best_memory_exponent_log2: float
    generic_sample_exponent_log2: float


@dataclass(frozen=True)
class ScalingFamilyRecord:
    family_id: str
    n_bits: list[int]
    high_dequantization_risk: list[bool]
    full_table_success: list[bool]
    random_sample_success: list[bool]
    derivative_best_support: list[int]
    structured_signal: list[bool]


@dataclass(frozen=True)
class HiddenShiftWorkbenchResult:
    created_at: str
    family_audits: list[HiddenShiftAuditRecord]
    sieve_baseline: PhaseSieveResult
    sieve_search: SieveSearchResult
    phase_state_trace: PhaseStateTrace
    scaling_history: list[ScalingFamilyRecord]
    summary: str
    falsifiers_triggered: list[str]


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value in {2, 3}:
        return True
    if value % 2 == 0:
        return False
    limit = int(math.sqrt(value)) + 1
    for factor in range(3, limit, 2):
        if value % factor == 0:
            return False
    return True


def next_prime_at_least(value: int) -> int:
    candidate = max(2, int(value))
    while not _is_prime(candidate):
        candidate += 1
    return candidate


def _legendre_symbol(x: int, prime: int) -> int:
    if x % prime == 0:
        return 1
    value = pow(x, (prime - 1) // 2, prime)
    return -1 if value == prime - 1 else int(value)


def _prime_factors(value: int) -> list[int]:
    n = value
    factors = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 1
    if n > 1:
        factors.append(n)
    return factors


def _primitive_root(prime: int) -> int:
    factors = _prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for {prime}")


def _next_prime_with_congruence(start: int, modulus: int, residue: int) -> int:
    candidate = max(2, int(start))
    while not (_is_prime(candidate) and candidate % modulus == residue):
        candidate += 1
    return candidate


def _hash_bit(value: int, seed: int = 0) -> int:
    x = (int(value) + 0x9E3779B97F4A7C15 + (seed << 1)) & ((1 << 64) - 1)
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9 & ((1 << 64) - 1)
    x = (x ^ (x >> 27)) * 0x94D049BB133111EB & ((1 << 64) - 1)
    x ^= x >> 31
    return int(x & 1)


def _f2_quadratic_bit(x: int, n_bits: int) -> int:
    value = 0
    for bit in range(0, n_bits - 1, 2):
        value ^= ((x >> bit) & 1) & ((x >> (bit + 1)) & 1)
    if n_bits % 2:
        value ^= (x >> (n_bits - 1)) & 1
    return value


def _mm_majority_bent_bit(x: int, n_bits: int) -> int:
    left_bits = n_bits // 2
    right_bits = n_bits - left_bits
    left = x & ((1 << left_bits) - 1)
    right = x >> left_bits
    dot = 0
    for bit in range(min(left_bits, right_bits)):
        dot ^= ((left >> bit) & 1) & ((right >> bit) & 1)
    majority = 1 if right.bit_count() >= ((right_bits + 1) // 2) else 0
    return dot ^ majority


def _f2_signal_from_bits(bits: Sequence[int]) -> np.ndarray:
    return np.array([1.0 if (int(bit) & 1) == 0 else -1.0 for bit in bits], dtype=complex)


def _fp2_prime_for_bits(n_bits: int) -> int:
    return next_prime_at_least(int(math.ceil(math.sqrt(1 << n_bits))))


def _fp2_coords(index: int, prime: int) -> tuple[int, int]:
    return int(index) // prime, int(index) % prime


def _fp2_index(x_coord: int, y_coord: int, prime: int) -> int:
    return (int(x_coord) % prime) * prime + (int(y_coord) % prime)


def _mod_inverse(value: int, modulus: int) -> int | None:
    value = int(value) % modulus
    if value == 0:
        return None
    try:
        return pow(value, -1, modulus)
    except ValueError:
        return None


def canonical_family_id(family_id: str) -> str:
    normalized = family_id.strip().lower().replace("-", "_")
    aliases = {
        "quadratic": "quadratic_chirp",
        "quadratic_chirp": "quadratic_chirp",
        "cubic": "cubic_chirp",
        "cubic_chirp": "cubic_chirp",
        "noisy_cubic": "noisy_cubic_chirp",
        "noisy_cubic_chirp": "noisy_cubic_chirp",
        "legendre": "legendre_symbol",
        "legendre_symbol": "legendre_symbol",
        "quartic": "quartic_character",
        "quartic_character": "quartic_character",
        "kloosterman": "kloosterman_trace",
        "kloosterman_trace": "kloosterman_trace",
        "finite_field_trace": "kloosterman_trace",
        "bent": "bent_quadratic_f2",
        "bent_quadratic": "bent_quadratic_f2",
        "bent_quadratic_f2": "bent_quadratic_f2",
        "masked": "masked_quadratic_f2",
        "masked_quadratic": "masked_quadratic_f2",
        "masked_quadratic_f2": "masked_quadratic_f2",
        "mm_majority": "mm_majority_bent_f2",
        "mm_majority_bent": "mm_majority_bent_f2",
        "mm_majority_bent_f2": "mm_majority_bent_f2",
        "maiorana_mcfarland_majority": "mm_majority_bent_f2",
        "fp2_quadratic": "fp2_quadratic_form",
        "fp2_quadratic_form": "fp2_quadratic_form",
        "finite_field_vector_quadratic": "fp2_quadratic_form",
    }
    if normalized not in aliases:
        raise ValueError(f"unknown phase family: {family_id}")
    return aliases[normalized]


def generate_cyclic_phase_family(family_id: str, n_bits: int) -> tuple[PhaseFamilySpec, np.ndarray]:
    """Generate an explicit scalable cyclic phase family."""

    if n_bits < 3:
        raise ValueError("n_bits must be at least 3 for meaningful cyclic phase audits")

    canonical = canonical_family_id(family_id)

    if canonical in {"bent_quadratic_f2", "masked_quadratic_f2", "mm_majority_bent_f2"}:
        domain_size = 1 << n_bits
        bits = []
        for x_value in range(domain_size):
            bit = _mm_majority_bent_bit(x_value, n_bits) if canonical == "mm_majority_bent_f2" else _f2_quadratic_bit(x_value, n_bits)
            if canonical == "masked_quadratic_f2":
                bit ^= _hash_bit(x_value, seed=17)
            bits.append(bit)
        signal = _f2_signal_from_bits(bits)
        descriptions = {
            "bent_quadratic_f2": "Boolean quadratic form over F_2^n with pairwise terms; even n is bent, odd n is a quadratic control.",
            "masked_quadratic_f2": "Quadratic F_2 phase masked by a deterministic high-entropy sign pattern; probes full-table versus sample-limited access.",
            "mm_majority_bent_f2": (
                "Maiorana-McFarland-style split Boolean phase x dot y plus majority(y); "
                "a structured high-degree/sparse-ANF stress test rather than a random table."
            ),
        }
        spec = PhaseFamilySpec(
            id=canonical,
            group="F2^n",
            n_bits=n_bits,
            domain_size=domain_size,
            modulus=domain_size,
            parameters={"mask_seed": 17 if canonical == "masked_quadratic_f2" else "none"},
            description=descriptions[canonical],
        )
        return spec, signal

    if canonical == "fp2_quadratic_form":
        prime = _fp2_prime_for_bits(n_bits)
        domain_size = prime * prime
        coefficient_y2 = 5
        signal = np.empty(domain_size, dtype=complex)
        for index in range(domain_size):
            x_coord, y_coord = _fp2_coords(index, prime)
            phase = (x_coord * x_coord + x_coord * y_coord + coefficient_y2 * y_coord * y_coord) % prime
            signal[index] = np.exp(2j * np.pi * phase / prime)
        spec = PhaseFamilySpec(
            id=canonical,
            group="F_p^2",
            n_bits=n_bits,
            domain_size=domain_size,
            modulus=prime,
            parameters={"prime": prime, "quadratic_y2_coefficient": coefficient_y2},
            description=(
                "Noncyclic vector-space hidden-shift family over F_p^2 with quadratic phase "
                "x^2 + xy + 5y^2; included to test finite-field algebraic dequantization."
            ),
        )
        return spec, signal

    modulus = next_prime_at_least(1 << n_bits)
    if canonical == "quartic_character":
        modulus = _next_prime_with_congruence(1 << n_bits, 4, 1)
    x = np.arange(modulus, dtype=int)

    if canonical == "quadratic_chirp":
        a = 1
        phases = (a * x * x) % modulus
        description = "Prime-modulus quadratic chirp exp(2 pi i x^2 / p); useful flat-spectrum control family."
        parameters: dict[str, int | str] = {"a": a}
    elif canonical == "cubic_chirp":
        a = 1
        phases = (a * x * x * x) % modulus
        description = "Prime-modulus cubic chirp exp(2 pi i x^3 / p); derivative is quadratic rather than linear."
        parameters = {"a": a}
    elif canonical == "noisy_cubic_chirp":
        a = 1
        phases = (a * x * x * x) % modulus
        mask = np.array([_hash_bit(int(item), seed=31) for item in x], dtype=int)
        phases = (phases + mask * (modulus // 3)) % modulus
        description = "Cubic chirp with deterministic sparse phase masking; probes whether structure survives query-limited classical attacks."
        parameters = {"a": a, "mask_seed": 31}
    elif canonical == "legendre_symbol":
        values = np.array([_legendre_symbol(int(item), modulus) for item in x], dtype=float)
        signal = values.astype(complex)
        spec = PhaseFamilySpec(
            id=canonical,
            group="Z_p",
            n_bits=n_bits,
            domain_size=modulus,
            modulus=modulus,
            parameters={"prime": modulus},
            description="Legendre-symbol phase over prime field; a multiplicative-character hidden-shift family.",
        )
        return spec, signal
    elif canonical == "quartic_character":
        root = _primitive_root(modulus)
        log_table = {1: 0}
        value = 1
        for exponent in range(1, modulus - 1):
            value = (value * root) % modulus
            log_table[value] = exponent
        signal = np.ones(modulus, dtype=complex)
        for item in range(1, modulus):
            signal[item] = 1j ** (log_table[item] % 4)
        spec = PhaseFamilySpec(
            id=canonical,
            group="Z_p",
            n_bits=n_bits,
            domain_size=modulus,
            modulus=modulus,
            parameters={"prime": modulus, "primitive_root": root},
            description="Quartic multiplicative character over F_p for p = 1 mod 4; a finite-field character hidden-shift probe.",
        )
        return spec, signal
    elif canonical == "kloosterman_trace":
        phases = np.zeros(modulus, dtype=int)
        for item in range(1, modulus):
            phases[item] = (item + pow(int(item), modulus - 2, modulus)) % modulus
        description = (
            "Finite-field Kloosterman-style trace phase exp(2 pi i (x + x^{-1}) / p), with x=0 fixed; "
            "a natural algebraic-geometry trace-function hidden-shift stress test without hash masking."
        )
        parameters = {"prime": modulus, "trace_function": "x_plus_inverse_x"}
    else:
        raise AssertionError(f"unhandled family: {canonical}")

    signal = np.exp(2j * np.pi * phases / modulus)
    spec = PhaseFamilySpec(
        id=canonical,
        group="Z_p",
        n_bits=n_bits,
        domain_size=modulus,
        modulus=modulus,
        parameters={**parameters, "prime": modulus},
        description=description,
    )
    return spec, signal


def apply_cyclic_hidden_shift(signal: Sequence[complex], shift: int) -> np.ndarray:
    values = np.asarray(signal, dtype=complex)
    if values.size < 2:
        raise ValueError("need at least two signal values")
    return np.roll(values, -int(shift) % values.size)


def shifted_index(spec: PhaseFamilySpec, x: int, shift: int) -> int:
    if spec.group == "F2^n":
        return int(x) ^ (int(shift) % spec.domain_size)
    if spec.group == "F_p^2":
        prime = int(spec.modulus)
        x0, x1 = _fp2_coords(int(x), prime)
        s0, s1 = _fp2_coords(int(shift) % spec.domain_size, prime)
        return _fp2_index(x0 + s0, x1 + s1, prime)
    return (int(x) + int(shift)) % spec.domain_size


def apply_hidden_shift(spec: PhaseFamilySpec, signal: Sequence[complex], shift: int) -> np.ndarray:
    values = np.asarray(signal, dtype=complex)
    if spec.group == "F2^n":
        return np.array([values[x ^ (int(shift) % spec.domain_size)] for x in range(spec.domain_size)], dtype=complex)
    if spec.group == "F_p^2":
        return np.array([values[shifted_index(spec, x, shift)] for x in range(spec.domain_size)], dtype=complex)
    return apply_cyclic_hidden_shift(values, shift)


def walsh_hadamard_complex(signal: Sequence[complex]) -> np.ndarray:
    values = np.asarray(signal, dtype=complex).copy()
    size = values.size
    if size == 0 or size & (size - 1):
        raise ValueError("Walsh-Hadamard input length must be a non-zero power of two")
    step = 1
    while step < size:
        for start in range(0, size, step * 2):
            left = values[start : start + step].copy()
            right = values[start + step : start + 2 * step].copy()
            values[start : start + step] = left + right
            values[start + step : start + 2 * step] = left - right
        step *= 2
    return values


def fourier_profile(signal: Sequence[complex]) -> FourierProfile:
    values = np.asarray(signal, dtype=complex)
    size = values.size
    if size < 2:
        raise ValueError("need at least two signal values")
    spectrum = np.fft.fft(values) / math.sqrt(size)
    power = np.abs(spectrum) ** 2
    total = float(power.sum())
    if total <= 0:
        raise ValueError("signal has zero Fourier power")
    probabilities = power / total
    nonzero = probabilities[probabilities > 1e-15]
    entropy = float(-np.sum(nonzero * np.log2(nonzero)))
    ordered = np.sort(probabilities)[::-1]
    support_99 = int(np.searchsorted(np.cumsum(ordered), 0.99) + 1)
    flatness = float(nonzero.min() / nonzero.max()) if nonzero.size else 0.0
    return FourierProfile(size, entropy, support_99, float(ordered[0]), flatness)


def group_fourier_profile(spec: PhaseFamilySpec, signal: Sequence[complex]) -> FourierProfile:
    values = np.asarray(signal, dtype=complex)
    if spec.group != "F2^n":
        if spec.group == "F_p^2":
            prime = int(spec.modulus)
            grid = values.reshape((prime, prime))
            spectrum_grid = np.fft.fft2(grid) / math.sqrt(values.size)
            power = np.abs(spectrum_grid.reshape(values.size)) ** 2
            total = float(power.sum())
            if total <= 0:
                raise ValueError("signal has zero Fourier power")
            probabilities = power / total
            nonzero = probabilities[probabilities > 1e-15]
            entropy = float(-np.sum(nonzero * np.log2(nonzero)))
            ordered = np.sort(probabilities)[::-1]
            support_99 = int(np.searchsorted(np.cumsum(ordered), 0.99) + 1)
            flatness = float(nonzero.min() / nonzero.max()) if nonzero.size else 0.0
            return FourierProfile(values.size, entropy, support_99, float(ordered[0]), flatness)
        return fourier_profile(values)
    size = values.size
    spectrum = walsh_hadamard_complex(values) / math.sqrt(size)
    power = np.abs(spectrum) ** 2
    total = float(power.sum())
    if total <= 0:
        raise ValueError("signal has zero Fourier power")
    probabilities = power / total
    nonzero = probabilities[probabilities > 1e-15]
    entropy = float(-np.sum(nonzero * np.log2(nonzero)))
    ordered = np.sort(probabilities)[::-1]
    support_99 = int(np.searchsorted(np.cumsum(ordered), 0.99) + 1)
    flatness = float(nonzero.min() / nonzero.max()) if nonzero.size else 0.0
    return FourierProfile(size, entropy, support_99, float(ordered[0]), flatness)


def cyclic_autocorrelation_alias_ratio(signal: Sequence[complex]) -> float:
    values = np.asarray(signal, dtype=complex)
    size = values.size
    correlations = np.empty(size, dtype=float)
    for shift in range(size):
        correlations[shift] = abs(np.vdot(values, np.roll(values, -shift)))
    peak0 = float(correlations[0])
    if peak0 == 0:
        return 0.0
    return float(np.max(correlations[1:]) / peak0)


def group_autocorrelation_alias_ratio(spec: PhaseFamilySpec, signal: Sequence[complex]) -> float:
    if spec.group not in {"F2^n", "F_p^2"}:
        return cyclic_autocorrelation_alias_ratio(signal)
    values = np.asarray(signal, dtype=complex)
    correlations = np.empty(spec.domain_size, dtype=float)
    for shift in range(spec.domain_size):
        if spec.group == "F2^n":
            correlations[shift] = abs(sum(np.conjugate(values[x]) * values[x ^ shift] for x in range(spec.domain_size)))
        else:
            correlations[shift] = abs(
                sum(np.conjugate(values[x]) * values[shifted_index(spec, x, shift)] for x in range(spec.domain_size))
            )
    peak0 = float(correlations[0])
    if peak0 == 0:
        return 0.0
    return float(np.max(correlations[1:]) / peak0)


def derivative_profile(signal: Sequence[complex], shifts: Iterable[int] | None = None) -> DerivativeProfile:
    values = np.asarray(signal, dtype=complex)
    size = values.size
    if shifts is None:
        base_shifts = [1, 2, 3, 5, 8, 13, 21]
        shifts = [shift for shift in base_shifts if shift < size]
    sampled = [int(shift) % size for shift in shifts if int(shift) % size != 0]
    if not sampled:
        raise ValueError("need at least one nonzero derivative shift")

    supports = []
    top_masses = []
    for shift in sampled:
        derivative = np.conjugate(values) * np.roll(values, -shift)
        profile = fourier_profile(derivative)
        supports.append(profile.support_99_percent)
        top_masses.append(profile.top_mass)

    best_support = int(min(supports))
    median_support = float(np.median(supports))
    best_top_mass = float(max(top_masses))
    if best_support <= 2:
        interpretation = "very sparse derivative spectrum; likely classically learnable algebraic structure"
    elif best_support <= max(8, int(math.sqrt(size))):
        interpretation = "structured derivative spectrum; possible phase-sieve handle but needs dequantization checks"
    else:
        interpretation = "broad derivative spectrum; weak evidence for higher-order Fourier leverage"
    return DerivativeProfile(len(sampled), best_support, median_support, best_top_mass, interpretation)


def derivative_profile_for_family(
    spec: PhaseFamilySpec, signal: Sequence[complex], shifts: Iterable[int] | None = None
) -> DerivativeProfile:
    if spec.group not in {"F2^n", "F_p^2"}:
        return derivative_profile(signal, shifts=shifts)
    values = np.asarray(signal, dtype=complex)
    if shifts is None and spec.group == "F2^n":
        shifts = [1 << bit for bit in range(min(spec.n_bits, 8))]
    elif shifts is None:
        prime = int(spec.modulus)
        shifts = [1, prime, prime + 1, 2 * prime + 1, prime + 2]
    sampled = [int(shift) for shift in shifts if 0 < int(shift) < spec.domain_size]
    supports = []
    top_masses = []
    for shift in sampled:
        if spec.group == "F2^n":
            derivative = np.array([np.conjugate(values[x]) * values[x ^ shift] for x in range(spec.domain_size)], dtype=complex)
        else:
            derivative = np.array(
                [np.conjugate(values[x]) * values[shifted_index(spec, x, shift)] for x in range(spec.domain_size)],
                dtype=complex,
            )
        profile = group_fourier_profile(spec, derivative)
        supports.append(profile.support_99_percent)
        top_masses.append(profile.top_mass)
    best_support = int(min(supports))
    median_support = float(np.median(supports))
    best_top_mass = float(max(top_masses))
    if best_support <= 2:
        interpretation = "very sparse derivative spectrum; likely classically learnable algebraic structure"
    elif best_support <= max(8, spec.n_bits):
        interpretation = "structured derivative spectrum; possible higher-order Fourier handle"
    else:
        interpretation = "broad derivative spectrum; weak evidence for low-degree learning"
    return DerivativeProfile(len(sampled), best_support, median_support, best_top_mass, interpretation)


def correlation_shift_attack(base: Sequence[complex], shifted: Sequence[complex], true_shift: int) -> ShiftAttackResult:
    f = np.asarray(base, dtype=complex)
    g = np.asarray(shifted, dtype=complex)
    if f.size != g.size:
        raise ValueError("signals must have the same domain size")
    correlations = np.empty(f.size, dtype=float)
    for guess in range(f.size):
        correlations[guess] = abs(np.vdot(np.roll(f, -guess), g))
    best = int(np.argmax(correlations))
    ordered = np.sort(correlations)
    runner_up = float(ordered[-2]) if f.size > 1 else 0.0
    confidence = float((correlations[best] - runner_up) / max(correlations[best], 1e-12))
    return ShiftAttackResult(
        name="full_table_cyclic_correlation",
        recovered_shift=best,
        success=best == int(true_shift) % f.size,
        confidence=confidence,
        cost_model="O(N^2) direct comparisons, or O(N log N) with FFT correlation under full-table access",
        notes="If the full truth table or concise classical evaluator is available, this is a dequantization risk.",
        legal_query_models=["full_table"],
    )


def fourier_phase_shift_attack(base: Sequence[complex], shifted: Sequence[complex], true_shift: int) -> ShiftAttackResult:
    f = np.asarray(base, dtype=complex)
    g = np.asarray(shifted, dtype=complex)
    size = f.size
    spectrum_f = np.fft.fft(f)
    spectrum_g = np.fft.fft(g)
    weights = np.abs(spectrum_f) ** 2
    usable = weights > (weights.max() * 1e-9)
    ratios = np.zeros(size, dtype=complex)
    ratios[usable] = spectrum_g[usable] / spectrum_f[usable]
    ratios[usable] /= np.maximum(np.abs(ratios[usable]), 1e-12)
    frequencies = np.arange(size)

    scores = np.empty(size, dtype=float)
    for guess in range(size):
        predicted = np.exp(-2j * np.pi * frequencies * guess / size)
        scores[guess] = float(np.real(np.sum(weights[usable] * ratios[usable] * predicted[usable])))
    best = int(np.argmax(scores))
    ordered = np.sort(scores)
    runner_up = float(ordered[-2]) if size > 1 else 0.0
    confidence = float((scores[best] - runner_up) / max(abs(scores[best]), 1e-12))
    return ShiftAttackResult(
        name="full_table_fourier_phase_regression",
        recovered_shift=best,
        success=best == int(true_shift) % size,
        confidence=confidence,
        cost_model="O(N log N + NK) with full-table FFT and K scored frequencies",
        notes="Recovers cyclic shifts from Fourier phase ratios when full-table access is allowed.",
        legal_query_models=["full_table"],
    )


def full_table_group_correlation_attack(
    spec: PhaseFamilySpec, base: Sequence[complex], shifted: Sequence[complex], true_shift: int
) -> ShiftAttackResult:
    if spec.group not in {"F2^n", "F_p^2"}:
        return correlation_shift_attack(base, shifted, true_shift)
    f = np.asarray(base, dtype=complex)
    g = np.asarray(shifted, dtype=complex)
    correlations = np.empty(spec.domain_size, dtype=float)
    for guess in range(spec.domain_size):
        if spec.group == "F2^n":
            correlations[guess] = abs(sum(np.conjugate(f[x ^ guess]) * g[x] for x in range(spec.domain_size)))
        else:
            correlations[guess] = abs(
                sum(np.conjugate(f[shifted_index(spec, x, guess)]) * g[x] for x in range(spec.domain_size))
            )
    best = int(np.argmax(correlations))
    ordered = np.sort(correlations)
    runner_up = float(ordered[-2]) if spec.domain_size > 1 else 0.0
    confidence = float((correlations[best] - runner_up) / max(correlations[best], 1e-12))
    return ShiftAttackResult(
        name="full_table_group_correlation",
        recovered_shift=best,
        success=best == int(true_shift) % spec.domain_size,
        confidence=confidence,
        cost_model="O(N^2) direct group-correlation comparisons under full-table access",
        notes="Full truth-table correlation recovers shifts for any nondegenerate explicit finite function.",
        legal_query_models=["full_table"],
    )


def sparse_fourier_recovery_attack(
    spec: PhaseFamilySpec,
    base: Sequence[complex],
    shifted: Sequence[complex],
    true_shift: int,
    top_k: int | None = None,
) -> ShiftAttackResult:
    f = np.asarray(base, dtype=complex)
    g = np.asarray(shifted, dtype=complex)
    size = spec.domain_size
    if spec.group == "F2^n":
        spectrum_f = walsh_hadamard_complex(f)
        spectrum_g = walsh_hadamard_complex(g)
    elif spec.group == "F_p^2":
        prime = int(spec.modulus)
        spectrum_f = np.fft.fft2(f.reshape((prime, prime))).reshape(size)
        spectrum_g = np.fft.fft2(g.reshape((prime, prime))).reshape(size)
    else:
        spectrum_f = np.fft.fft(f)
        spectrum_g = np.fft.fft(g)
    weights = np.abs(spectrum_f) ** 2
    top_k = top_k or max(4, min(size, 2 * spec.n_bits))
    usable = np.argsort(weights)[::-1][:top_k]
    ratios = np.zeros(size, dtype=complex)
    nonzero = np.abs(spectrum_f[usable]) > 1e-12
    active = usable[nonzero]
    if active.size == 0:
        return ShiftAttackResult(
            name="sparse_fourier_recovery",
            recovered_shift=None,
            success=False,
            confidence=0.0,
            cost_model="No usable Fourier support found.",
            notes="Sparse Fourier recovery could not form phase ratios.",
            legal_query_models=["full_table"],
        )
    ratios[active] = spectrum_g[active] / spectrum_f[active]
    ratios[active] /= np.maximum(np.abs(ratios[active]), 1e-12)
    scores = np.empty(size, dtype=float)
    if spec.group == "F2^n":
        for guess in range(size):
            total = 0.0
            for frequency in active:
                parity = (int(frequency) & guess).bit_count() & 1
                predicted = -1.0 if parity else 1.0
                total += float(weights[frequency] * np.real(ratios[frequency] * predicted))
            scores[guess] = total
    elif spec.group == "F_p^2":
        prime = int(spec.modulus)
        active_pairs = [_fp2_coords(int(frequency), prime) for frequency in active]
        for guess in range(size):
            sx, sy = _fp2_coords(guess, prime)
            total = 0.0
            for frequency, (fx, fy) in zip(active, active_pairs):
                predicted = np.exp(-2j * np.pi * ((fx * sx + fy * sy) % prime) / prime)
                total += float(weights[frequency] * np.real(ratios[frequency] * predicted))
            scores[guess] = total
    else:
        frequencies = np.arange(size)
        for guess in range(size):
            predicted = np.exp(-2j * np.pi * frequencies[active] * guess / size)
            scores[guess] = float(np.real(np.sum(weights[active] * ratios[active] * predicted)))
    best = int(np.argmax(scores))
    ordered = np.sort(scores)
    runner_up = float(ordered[-2]) if size > 1 else 0.0
    confidence = float((scores[best] - runner_up) / max(abs(scores[best]), 1e-12))
    return ShiftAttackResult(
        name="sparse_fourier_recovery",
        recovered_shift=best,
        success=best == int(true_shift) % size,
        confidence=confidence,
        cost_model=f"O(N log N) transform plus top_k={int(top_k)} phase-ratio scoring",
        notes="Tests whether a small Fourier support already classically reveals the shift.",
        legal_query_models=["full_table"],
    )


def sample_limited_correlation_attack(
    spec: PhaseFamilySpec,
    base: Sequence[complex],
    shifted: Sequence[complex],
    true_shift: int,
    sample_count: int,
    seed: int,
) -> ShiftAttackResult:
    f = np.asarray(base, dtype=complex)
    g = np.asarray(shifted, dtype=complex)
    rng = np.random.default_rng(seed)
    count = min(sample_count, spec.domain_size)
    base_xs = rng.choice(spec.domain_size, size=count, replace=False)
    shifted_xs = rng.choice(spec.domain_size, size=count, replace=False)
    base_samples = {int(x): f[int(x)] for x in base_xs}
    shifted_samples = {int(x): g[int(x)] for x in shifted_xs}
    scores = np.empty(spec.domain_size, dtype=float)
    for guess in range(spec.domain_size):
        total = 0.0 + 0.0j
        overlap = 0
        for x, g_value in shifted_samples.items():
            base_index = shifted_index(spec, x, guess)
            if base_index in base_samples:
                total += np.conjugate(base_samples[base_index]) * g_value
                overlap += 1
        scores[guess] = abs(total) / max(overlap, 1)
    best = int(np.argmax(scores))
    ordered = np.sort(scores)
    runner_up = float(ordered[-2]) if spec.domain_size > 1 else 0.0
    confidence = float((scores[best] - runner_up) / max(scores[best], 1e-12))
    return ShiftAttackResult(
        name="sample_limited_correlation",
        recovered_shift=best,
        success=best == int(true_shift) % spec.domain_size,
        confidence=confidence,
        cost_model=f"O(sample_count * |G|) sparse-overlap scoring with sample_count={count} random f-samples and g-samples",
        notes="Models a random-sample adversary that cannot query arbitrary shifted locations.",
        legal_query_models=["random_sample"],
        sample_count=int(count),
    )


def chosen_query_exhaustive_correlation_attack(
    spec: PhaseFamilySpec,
    base: Sequence[complex],
    shifted: Sequence[complex],
    true_shift: int,
    query_count: int,
    seed: int,
) -> ShiftAttackResult:
    """Score every shift using a small chosen-query panel.

    This is intentionally not a breakthrough classical attack: it still scans
    all shifts.  Its purpose is to prevent us from mistaking random-sample
    survival for evaluator-model survival when arbitrary point queries are
    allowed.
    """

    f = np.asarray(base, dtype=complex)
    g = np.asarray(shifted, dtype=complex)
    rng = np.random.default_rng(seed + 8191)
    count = min(max(1, int(query_count)), spec.domain_size)
    xs = rng.choice(spec.domain_size, size=count, replace=False)
    scores = np.empty(spec.domain_size, dtype=float)
    for guess in range(spec.domain_size):
        total = 0.0 + 0.0j
        for x in xs:
            total += np.conjugate(f[shifted_index(spec, int(x), guess)]) * g[int(x)]
        scores[guess] = abs(total) / count
    best = int(np.argmax(scores))
    ordered = np.sort(scores)
    runner_up = float(ordered[-2]) if spec.domain_size > 1 else 0.0
    confidence = float((scores[best] - runner_up) / max(scores[best], 1e-12))
    return ShiftAttackResult(
        name="chosen_query_exhaustive_correlation",
        recovered_shift=best,
        success=best == int(true_shift) % spec.domain_size,
        confidence=confidence,
        cost_model=(
            f"O(|G| * q) chosen evaluator queries with q={count}; exponential in n unless the shift space "
            "has additional exploitable structure"
        ),
        notes=(
            "Arbitrary evaluator access plus an exhaustive shift scan recovers many families; this is a model-separation "
            "baseline, not a polynomial-time dequantization."
        ),
        legal_query_models=["explicit_evaluator"],
        sample_count=int(count * spec.domain_size),
    )


def _invert_f2_quadratic_derivative_frequency(frequency: int, n_bits: int) -> int:
    shift = 0
    for bit in range(0, n_bits - 1, 2):
        if (frequency >> bit) & 1:
            shift |= 1 << (bit + 1)
        if (frequency >> (bit + 1)) & 1:
            shift |= 1 << bit
    if n_bits % 2 and ((frequency >> (n_bits - 1)) & 1):
        shift |= 1 << (n_bits - 1)
    return shift


def f2_quadratic_algebraic_reconstruction_attack(
    spec: PhaseFamilySpec, base: Sequence[complex], shifted: Sequence[complex], true_shift: int
) -> ShiftAttackResult:
    if spec.group != "F2^n" or "quadratic" not in spec.id or "masked" in spec.id:
        return ShiftAttackResult(
            name="f2_quadratic_algebraic_reconstruction",
            recovered_shift=None,
            success=False,
            confidence=0.0,
            cost_model="Not applicable outside unmasked F_2 quadratic forms.",
            notes="Attack skipped because the family is not an unmasked F_2 quadratic form.",
            legal_query_models=["explicit_evaluator"],
        )
    f = np.asarray(base, dtype=complex)
    g = np.asarray(shifted, dtype=complex)
    derivative = np.conjugate(f) * g
    spectrum = walsh_hadamard_complex(derivative)
    power = np.abs(spectrum) ** 2
    frequency = int(np.argmax(power))
    recovered = _invert_f2_quadratic_derivative_frequency(frequency, spec.n_bits)
    top_mass = float(power[frequency] / max(float(power.sum()), 1e-12))
    return ShiftAttackResult(
        name="f2_quadratic_algebraic_reconstruction",
        recovered_shift=recovered,
        success=recovered == int(true_shift) % spec.domain_size,
        confidence=top_mass,
        cost_model="O(n) chosen-query derivative learning for canonical F_2 quadratic forms",
        notes="Low-degree algebraic structure maps the hidden shift to a linear derivative frequency.",
        legal_query_models=["explicit_evaluator", "full_table"],
        sample_count=2 * spec.n_bits + 2,
    )


def fp2_quadratic_algebraic_reconstruction_attack(
    spec: PhaseFamilySpec, base: Sequence[complex], shifted: Sequence[complex], true_shift: int
) -> ShiftAttackResult:
    if spec.group != "F_p^2" or spec.id != "fp2_quadratic_form":
        return ShiftAttackResult(
            name="fp2_quadratic_algebraic_reconstruction",
            recovered_shift=None,
            success=False,
            confidence=0.0,
            cost_model="Not applicable outside the audited F_p^2 quadratic form family.",
            notes="Attack skipped because the family is not the explicit F_p^2 quadratic test family.",
            legal_query_models=["explicit_evaluator"],
        )

    prime = int(spec.modulus)
    coefficient_y2 = int(spec.parameters.get("quadratic_y2_coefficient", 5))
    determinant = (4 * coefficient_y2 - 1) % prime
    inverse_determinant = _mod_inverse(determinant, prime)
    if inverse_determinant is None:
        return ShiftAttackResult(
            name="fp2_quadratic_algebraic_reconstruction",
            recovered_shift=None,
            success=False,
            confidence=0.0,
            cost_model="Quadratic derivative matrix is singular for this prime.",
            notes="Attack skipped because the generated quadratic form is degenerate over the chosen field.",
            legal_query_models=["explicit_evaluator", "full_table"],
        )

    f = np.asarray(base, dtype=complex)
    g = np.asarray(shifted, dtype=complex)
    derivative = np.conjugate(f) * g
    spectrum = np.fft.fft2(derivative.reshape((prime, prime)))
    power = np.abs(spectrum) ** 2
    flat_frequency = int(np.argmax(power.reshape(spec.domain_size)))
    coeff_x, coeff_y = _fp2_coords(flat_frequency, prime)
    recovered_x = ((2 * coefficient_y2 * coeff_x - coeff_y) * inverse_determinant) % prime
    recovered_y = ((-coeff_x + 2 * coeff_y) * inverse_determinant) % prime
    recovered = _fp2_index(recovered_x, recovered_y, prime)
    top_mass = float(power.reshape(spec.domain_size)[flat_frequency] / max(float(power.sum()), 1e-12))
    return ShiftAttackResult(
        name="fp2_quadratic_algebraic_reconstruction",
        recovered_shift=recovered,
        success=recovered == int(true_shift) % spec.domain_size,
        confidence=top_mass,
        cost_model=(
            "O(poly(n)) chosen-query derivative learning for explicit low-degree F_p^2 quadratic forms; "
            "implemented with a full transform as a finite-instance certificate"
        ),
        notes="The derivative of a quadratic form is a linear character whose frequency solves a 2x2 system for the shift.",
        legal_query_models=["explicit_evaluator", "full_table"],
        sample_count=4 * spec.n_bits + 8,
    )


def classical_shift_attacks(
    spec: PhaseFamilySpec,
    base: Sequence[complex],
    shifted: Sequence[complex],
    true_shift: int,
    sample_count: int,
    seed: int,
) -> list[ShiftAttackResult]:
    attacks = [
        full_table_group_correlation_attack(spec, base, shifted, true_shift),
        sparse_fourier_recovery_attack(spec, base, shifted, true_shift),
        sample_limited_correlation_attack(spec, base, shifted, true_shift, sample_count=sample_count, seed=seed),
        chosen_query_exhaustive_correlation_attack(
            spec,
            base,
            shifted,
            true_shift,
            query_count=sample_count,
            seed=seed,
        ),
        f2_quadratic_algebraic_reconstruction_attack(spec, base, shifted, true_shift),
        fp2_quadratic_algebraic_reconstruction_attack(spec, base, shifted, true_shift),
    ]
    if spec.group == "Z_p":
        attacks.insert(1, fourier_phase_shift_attack(base, shifted, true_shift))
    return attacks


QUERY_MODELS = ["full_table", "random_sample", "explicit_evaluator", "coherent_oracle"]


def build_query_model_assessments(attacks: list[ShiftAttackResult]) -> list[QueryModelAssessment]:
    assessments: list[QueryModelAssessment] = []
    for model in QUERY_MODELS:
        legal = [attack.name for attack in attacks if model in attack.legal_query_models]
        successful = [attack.name for attack in attacks if model in attack.legal_query_models and attack.success]
        if model == "coherent_oracle":
            notes = "No purely classical attack is legal in the coherent-oracle model without a stated measurement/sample reduction."
        elif successful:
            notes = f"{len(successful)} implemented classical attack(s) recover the shift under this model."
        elif legal:
            notes = "No implemented legal attack recovered the shift under this model; this is only a provisional survival signal."
        else:
            notes = "No implemented classical baseline currently covers this access model."
        assessments.append(QueryModelAssessment(model, legal, successful, not successful, notes))
    return assessments


def _constant_signal_overlap_sample_bound(domain_size: int) -> int:
    """Samples needed before two random sample sets have constant expected overlap."""

    return int(math.ceil(math.sqrt(max(1, domain_size))))


def _poly_query_threshold(n_bits: int) -> int:
    return max(64, int(n_bits**4))


def build_query_lower_bound_probes(
    spec: PhaseFamilySpec,
    attacks: list[ShiftAttackResult],
    sample_budget: int,
) -> list[QueryLowerBoundProbe]:
    full_table_success = any(
        attack.success and "full_table" in attack.legal_query_models for attack in attacks
    )
    random_success = any(
        attack.success and "random_sample" in attack.legal_query_models for attack in attacks
    )
    low_complexity_explicit_successes = [
        attack
        for attack in attacks
        if attack.success
        and "explicit_evaluator" in attack.legal_query_models
        and attack.name != "chosen_query_exhaustive_correlation"
        and (attack.sample_count is None or attack.sample_count <= _poly_query_threshold(spec.n_bits))
    ]
    exhaustive = next((attack for attack in attacks if attack.name == "chosen_query_exhaustive_correlation"), None)
    overlap_bound = _constant_signal_overlap_sample_bound(spec.domain_size)

    if random_success:
        random_verdict = "dequantized-random-sample"
        random_notes = "A legal random-sample baseline recovered the shift; this family cannot support the sampled-access claim."
    elif sample_budget < overlap_bound:
        random_verdict = "undersampled-gap-not-evidence"
        random_notes = (
            "Random-sample correlation sees too little overlap for a constant signal; survival here is a lower-bound proof debt."
        )
    else:
        random_verdict = "survives-implemented-random-baselines"
        random_notes = "The sampled budget reaches the collision scale but current random-sample baselines still fail."

    if low_complexity_explicit_successes:
        explicit_verdict = "low-complexity-evaluator-dequantization"
        explicit_required = min(attack.sample_count or _poly_query_threshold(spec.n_bits) for attack in low_complexity_explicit_successes)
        explicit_notes = "A polynomial-sized evaluator attack recovered the shift."
    elif exhaustive and exhaustive.success:
        explicit_verdict = "exhaustive-evaluator-recovery-only"
        explicit_required = exhaustive.sample_count
        explicit_notes = (
            "Arbitrary point queries plus exhaustive scoring recover the shift, but the query count still scales with |G|."
        )
    else:
        explicit_verdict = "unresolved-evaluator-model"
        explicit_required = None
        explicit_notes = "No implemented evaluator-model attack recovered the shift; add chosen-query learning and reconstruction tests."

    return [
        QueryLowerBoundProbe(
            model="full_table",
            baseline="truth-table correlation / Fourier phase regression",
            legal=True,
            required_queries_for_constant_signal=spec.domain_size,
            observed_query_budget=spec.domain_size,
            verdict="dequantized-full-table" if full_table_success else "unexpected-full-table-survival",
            notes=(
                "Full-table access is sufficient to recover nondegenerate hidden shifts and should not be counted as quantum evidence."
                if full_table_success
                else "Full-table baselines failed; inspect aliases or degeneracy before treating this as positive."
            ),
        ),
        QueryLowerBoundProbe(
            model="random_sample",
            baseline="sample-overlap correlation lower-bound probe",
            legal=True,
            required_queries_for_constant_signal=overlap_bound,
            observed_query_budget=int(sample_budget),
            verdict=random_verdict,
            notes=random_notes,
        ),
        QueryLowerBoundProbe(
            model="explicit_evaluator",
            baseline="chosen-query reconstruction / exhaustive evaluator scoring",
            legal=True,
            required_queries_for_constant_signal=explicit_required,
            observed_query_budget=exhaustive.sample_count if exhaustive else None,
            verdict=explicit_verdict,
            notes=explicit_notes,
        ),
        QueryLowerBoundProbe(
            model="coherent_oracle",
            baseline="no classical point-query baseline is legal without measurement reduction",
            legal=False,
            required_queries_for_constant_signal=None,
            observed_query_budget=None,
            verdict="requires-formal-classical-lower-bound",
            notes="Coherent-oracle survival is a hypothesis about the input model, not evidence for a speedup by itself.",
        ),
    ]


def audit_hidden_shift_family(
    family_id: str,
    n_bits: int,
    shift: int,
    sample_count: int | None = None,
    seed: int = 0,
) -> HiddenShiftAuditRecord:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits)
    true_shift = int(shift) % spec.domain_size
    shifted = apply_hidden_shift(spec, signal, true_shift)
    f_profile = group_fourier_profile(spec, signal)
    d_profile = derivative_profile_for_family(spec, signal)
    alias_ratio = group_autocorrelation_alias_ratio(spec, signal)
    sample_budget = sample_count if sample_count is not None else max(8, 3 * n_bits)
    attacks = classical_shift_attacks(spec, signal, shifted, true_shift, sample_count=sample_budget, seed=seed)
    assessments = build_query_model_assessments(attacks)
    lower_bound_probes = build_query_lower_bound_probes(spec, attacks, sample_budget)
    survives_restricted = [
        assessment.model
        for assessment in assessments
        if assessment.survives_current_baselines and assessment.model in {"random_sample", "coherent_oracle"}
    ]

    falsifiers: list[str] = []
    if any(attack.success and "full_table" in attack.legal_query_models for attack in attacks):
        falsifiers.append("Full-table classical shift recovery succeeds; claimed advantage must rely on a stricter oracle/query model.")
    low_complexity_explicit_success = any(
        attack.success
        and "explicit_evaluator" in attack.legal_query_models
        and attack.name != "chosen_query_exhaustive_correlation"
        and (attack.sample_count is None or attack.sample_count <= _poly_query_threshold(spec.n_bits))
        for attack in attacks
    )
    if low_complexity_explicit_success:
        falsifiers.append("Explicit-evaluator classical attack recovers the shift; low-degree or concise structure is dequantized.")
    if any(attack.name == "chosen_query_exhaustive_correlation" and attack.success for attack in attacks):
        falsifiers.append("Chosen-query exhaustive correlation recovers the shift; any claim must beat O(|G|) evaluator scoring.")
    if d_profile.best_support_99_percent <= 2:
        falsifiers.append("Derivative spectrum is extremely sparse; the family may be classically learnable.")
    if alias_ratio > 0.35:
        falsifiers.append("Autocorrelation aliases are large enough to threaten hidden-shift distinguishability.")

    if survives_restricted and any(attack.success and "full_table" in attack.legal_query_models for attack in attacks):
        positive = "query-model separation probe: full-table dequantized but restricted sampled model survives implemented baselines"
    elif f_profile.flatness_ratio > 0.75 and d_profile.best_support_99_percent <= max(8, n_bits):
        positive = "flat Fourier profile with structured derivatives"
    elif d_profile.best_support_99_percent <= max(8, n_bits):
        positive = "structured derivative spectrum but Fourier profile needs scrutiny"
    else:
        positive = "weak phase-family signal"

    if low_complexity_explicit_success:
        risk = "critical: explicit-evaluator algebraic reconstruction dequantizes this family"
    elif any(attack.success and "full_table" in attack.legal_query_models for attack in attacks) and d_profile.best_support_99_percent <= 2:
        risk = "high: full-table attacks and sparse derivatives create a likely dequantization of this family"
    elif any(attack.success and "full_table" in attack.legal_query_models for attack in attacks):
        risk = "medium: full-table attacks work; oracle/query separation must be justified"
    else:
        risk = "low in tested baselines, but more classical attacks are required"

    return HiddenShiftAuditRecord(
        family=spec,
        true_shift=true_shift,
        fourier_profile=f_profile,
        derivative_profile=d_profile,
        autocorrelation_alias_ratio=alias_ratio,
        classical_attacks=attacks,
        query_model_assessments=assessments,
        query_lower_bound_probes=lower_bound_probes,
        survives_restricted_query_models=survives_restricted,
        dequantization_risk=risk,
        positive_signal=positive,
        falsifiers_triggered=falsifiers,
    )


def two_adic_valuation(label: int, n_bits: int) -> int:
    label = int(label) % (1 << n_bits)
    if label == 0:
        return n_bits
    valuation = 0
    while label % 2 == 0:
        valuation += 1
        label //= 2
    return valuation


def default_sieve_schedule(n_bits: int) -> list[int]:
    limit = max(2, min(n_bits - 1, int(math.ceil(2.0 * math.sqrt(n_bits)))))
    return list(range(1, limit + 1))


def generate_phase_state_records(n_bits: int, sample_count: int, seed: int = 0) -> list[PhaseStateRecord]:
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    if sample_count < 1:
        raise ValueError("sample_count must be positive")
    modulus = 1 << n_bits
    rng = np.random.default_rng(seed)
    labels = rng.integers(1, modulus, size=sample_count, dtype=np.int64)
    records = []
    for index, label in enumerate(labels.tolist()):
        label_int = int(label)
        records.append(
            PhaseStateRecord(
                id=f"psi0-{index}",
                modulus=modulus,
                label=label_int,
                two_adic_valuation=two_adic_valuation(label_int, n_bits),
                phase_expression=f"omega_{modulus}^({label_int} * s)",
                source="dihedral Fourier sampling phase state (|0> + omega_N^(k*s)|1>) / sqrt(2)",
                merge_depth=0,
                merge_history=[f"sample k={label_int}"],
            )
        )
    return records


def run_phase_state_collimation_trace(
    n_bits: int,
    sample_count: int,
    schedule: Sequence[int] | None = None,
    seed: int = 0,
    target_two_adic_valuation: int | None = None,
    strategy: str = "generic_low_bit_pairing",
    survivor_sample_limit: int = 12,
) -> PhaseStateTrace:
    """Track an explicit DHSP phase-state sieve trace.

    The trace is a research artifact, not a claim of a new algorithm.  It makes
    the current Kuperberg/Regev-style baseline auditable: every retained state
    has a label, valuation, and merge history explaining how low bits were
    cancelled.
    """

    if n_bits < 4:
        raise ValueError("n_bits must be at least 4 for phase-state collimation")
    if sample_count < 2:
        raise ValueError("sample_count must be at least 2")

    modulus = 1 << n_bits
    active_schedule = list(schedule) if schedule is not None else default_sieve_schedule(n_bits)
    target = target_two_adic_valuation if target_two_adic_valuation is not None else max(1, n_bits - 2)
    states = generate_phase_state_records(n_bits=n_bits, sample_count=sample_count, seed=seed)
    memory_peak = len(states)
    rounds: list[SieveRoundRecord] = []

    for round_index, bucket_bits in enumerate(active_schedule, start=1):
        if len(states) < 2:
            break
        bucket_modulus = 1 << int(bucket_bits)
        buckets: dict[int, list[PhaseStateRecord]] = {}
        for state in states:
            buckets.setdefault(state.label % bucket_modulus, []).append(state)

        next_states: list[PhaseStateRecord] = []
        zero_labels = 0
        merge_index = 0
        for bucket_key, bucket_states in sorted(buckets.items()):
            for left_index in range(0, len(bucket_states) - 1, 2):
                left = bucket_states[left_index]
                right = bucket_states[left_index + 1]
                combined = (left.label - right.label) % modulus
                if combined == 0:
                    zero_labels += 1
                    continue
                history = [
                    f"round {round_index}: matched labels congruent mod 2^{int(bucket_bits)} in bucket {bucket_key}",
                    f"{left.id} label {left.label} - {right.id} label {right.label} = {combined} mod {modulus}",
                ]
                if len(left.merge_history) <= 2:
                    history.extend(left.merge_history)
                if len(right.merge_history) <= 2:
                    history.extend(right.merge_history)
                next_states.append(
                    PhaseStateRecord(
                        id=f"psi{round_index}-{merge_index}",
                        modulus=modulus,
                        label=int(combined),
                        two_adic_valuation=two_adic_valuation(int(combined), n_bits),
                        phase_expression=f"omega_{modulus}^({int(combined)} * s)",
                        source="low-bit collimation merge of two DHSP phase states",
                        merge_depth=max(left.merge_depth, right.merge_depth) + 1,
                        merge_history=history[:8],
                    )
                )
                merge_index += 1

        valuations = [state.two_adic_valuation for state in next_states]
        best = max(valuations) if valuations else 0
        median = float(np.median(valuations)) if valuations else 0.0
        rounds.append(
            SieveRoundRecord(
                round_index=round_index,
                bucket_bits=int(bucket_bits),
                input_states=sum(len(bucket) for bucket in buckets.values()),
                output_states=len(next_states),
                zero_labels=zero_labels,
                best_two_adic_valuation=best,
                median_two_adic_valuation=median,
            )
        )
        states = next_states
        memory_peak = max(memory_peak, len(states))

    best_final = max((round_record.best_two_adic_valuation for round_record in rounds), default=0)
    reached = best_final >= target
    survivor_sample = sorted(states, key=lambda state: (-state.two_adic_valuation, state.label))[:survivor_sample_limit]
    success_proxy = min(1.0, 2.0 ** (best_final - target)) if target else 1.0
    if reached:
        interpretation = "Baseline collimation reaches the target valuation; compare sample exponent against known DHSP sieves."
    elif states:
        interpretation = "Trace leaves phase states but does not reach the target valuation; stronger merge rules or more samples are needed."
    else:
        interpretation = "All phase states were consumed before reaching the target valuation; the merge schedule is too aggressive."

    return PhaseStateTrace(
        n_bits=n_bits,
        modulus=modulus,
        strategy=strategy,
        input_model="coherent_oracle_to_phase_states",
        merge_rule="pair states whose labels agree modulo 2^b, then subtract labels to cancel low bits",
        initial_state_count=sample_count,
        final_state_count=len(states),
        memory_peak=memory_peak,
        target_two_adic_valuation=int(target),
        best_two_adic_valuation=best_final,
        reached_target=reached,
        success_probability_proxy=float(success_proxy),
        sample_exponent_log2=float(math.log2(sample_count)),
        memory_exponent_log2=float(math.log2(max(memory_peak, 1))),
        merge_depth=len(rounds),
        schedule=active_schedule,
        rounds=rounds,
        survivor_states_sample=survivor_sample,
        interpretation=interpretation,
    )


def run_kuperberg_sieve_baseline(
    n_bits: int,
    sample_count: int,
    schedule: Sequence[int] | None = None,
    seed: int = 0,
    target_two_adic_valuation: int | None = None,
    strategy: str = "generic_low_bit_pairing",
) -> PhaseSieveResult:
    """Simulate a bucketed DHSP phase-label sieve over Z_{2^n}.

    This is not a new algorithm. It is a baseline for tracking whether future
    family-specific merge rules beat generic low-bit cancellation.
    """

    if n_bits < 4:
        raise ValueError("n_bits must be at least 4 for sieve simulation")
    if sample_count < 2:
        raise ValueError("sample_count must be at least 2")

    modulus = 1 << n_bits
    rng = np.random.default_rng(seed)
    labels = rng.integers(1, modulus, size=sample_count, dtype=np.int64)
    active_schedule = list(schedule) if schedule is not None else default_sieve_schedule(n_bits)
    target = target_two_adic_valuation if target_two_adic_valuation is not None else max(1, n_bits - 2)
    memory_peak = int(labels.size)
    rounds: list[SieveRoundRecord] = []

    for index, bucket_bits in enumerate(active_schedule, start=1):
        if labels.size < 2:
            break
        bucket_modulus = 1 << int(bucket_bits)
        buckets: dict[int, list[int]] = {}
        for label in labels.tolist():
            buckets.setdefault(int(label) % bucket_modulus, []).append(int(label))

        new_labels: list[int] = []
        zero_labels = 0
        for bucket in buckets.values():
            for left_index in range(0, len(bucket) - 1, 2):
                combined = (bucket[left_index] - bucket[left_index + 1]) % modulus
                if combined == 0:
                    zero_labels += 1
                else:
                    new_labels.append(combined)

        labels = np.array(new_labels, dtype=np.int64)
        memory_peak = max(memory_peak, int(labels.size))
        valuations = [two_adic_valuation(int(label), n_bits) for label in labels.tolist()]
        best = max(valuations) if valuations else 0
        median = float(np.median(valuations)) if valuations else 0.0
        rounds.append(
            SieveRoundRecord(
                round_index=index,
                bucket_bits=int(bucket_bits),
                input_states=sum(len(bucket) for bucket in buckets.values()),
                output_states=int(labels.size),
                zero_labels=zero_labels,
                best_two_adic_valuation=best,
                median_two_adic_valuation=median,
            )
        )

    best_final = max((round_record.best_two_adic_valuation for round_record in rounds), default=0)
    return PhaseSieveResult(
        n_bits=n_bits,
        modulus=modulus,
        initial_states=sample_count,
        final_states=int(labels.size),
        memory_peak=memory_peak,
        best_two_adic_valuation=best_final,
        reached_target=best_final >= target,
        target_two_adic_valuation=int(target),
        sample_exponent_log2=float(math.log2(sample_count)),
        memory_exponent_log2=float(math.log2(max(memory_peak, 1))),
        merge_depth=len(rounds),
        strategy=strategy,
        schedule=active_schedule,
        rounds=rounds,
    )


def sieve_schedule_candidates(n_bits: int) -> dict[str, list[int]]:
    default = default_sieve_schedule(n_bits)
    return {
        "generic_low_bit_pairing": default,
        "regev_collimation_proxy": [max(1, int(math.ceil(math.sqrt(n_bits)))) for _ in default],
        "aggressive_doubling": list(range(1, n_bits, 2)),
        "family_specific_sparse_derivative": sorted(set([1, 2, 3, max(2, n_bits // 2), max(3, n_bits - 2)])),
    }


def run_sieve_strategy_search(
    n_bits: int,
    sample_count: int,
    seed: int = 0,
    target_two_adic_valuation: int | None = None,
) -> SieveSearchResult:
    schedules = sieve_schedule_candidates(n_bits)
    candidates = [
        run_kuperberg_sieve_baseline(
            n_bits=n_bits,
            sample_count=sample_count,
            schedule=schedule,
            seed=seed + index,
            target_two_adic_valuation=target_two_adic_valuation,
            strategy=name,
        )
        for index, (name, schedule) in enumerate(schedules.items())
    ]
    baseline = next(item for item in candidates if item.strategy == "generic_low_bit_pairing")
    best = max(
        candidates,
        key=lambda item: (
            item.reached_target,
            item.best_two_adic_valuation,
            -item.memory_exponent_log2,
            -item.merge_depth,
        ),
    )
    return SieveSearchResult(
        n_bits=n_bits,
        sample_count=sample_count,
        baseline=baseline,
        candidates=candidates,
        best_strategy=best.strategy,
        best_target_success=best.reached_target,
        best_two_adic_valuation=best.best_two_adic_valuation,
        best_memory_exponent_log2=best.memory_exponent_log2,
        generic_sample_exponent_log2=baseline.sample_exponent_log2,
    )


def build_scaling_history(audits: list[HiddenShiftAuditRecord]) -> list[ScalingFamilyRecord]:
    by_family: dict[str, list[HiddenShiftAuditRecord]] = {}
    for audit in audits:
        by_family.setdefault(audit.family.id, []).append(audit)
    records = []
    for family_id, family_audits in sorted(by_family.items()):
        ordered = sorted(family_audits, key=lambda item: item.family.n_bits)
        records.append(
            ScalingFamilyRecord(
                family_id=family_id,
                n_bits=[audit.family.n_bits for audit in ordered],
                high_dequantization_risk=[
                    audit.dequantization_risk.startswith(("critical", "high")) for audit in ordered
                ],
                full_table_success=[
                    any(
                        attack.success and "full_table" in attack.legal_query_models
                        for attack in audit.classical_attacks
                    )
                    for audit in ordered
                ],
                random_sample_success=[
                    any(
                        attack.success and "random_sample" in attack.legal_query_models
                        for attack in audit.classical_attacks
                    )
                    for audit in ordered
                ],
                derivative_best_support=[audit.derivative_profile.best_support_99_percent for audit in ordered],
                structured_signal=["structured" in audit.positive_signal or "flat" in audit.positive_signal for audit in ordered],
            )
        )
    return records


def run_hidden_shift_workbench(
    families: Sequence[str] | None = None,
    min_bits: int = 5,
    max_bits: int = 8,
    shift: int = 7,
    sieve_samples: int = 2048,
    seed: int = 0,
    sample_count: int | None = None,
) -> HiddenShiftWorkbenchResult:
    if min_bits > max_bits:
        raise ValueError("min_bits must be <= max_bits")
    family_ids = (
        list(families)
        if families is not None
        else [
            "quadratic_chirp",
            "cubic_chirp",
            "legendre_symbol",
            "quartic_character",
            "kloosterman_trace",
            "fp2_quadratic_form",
            "mm_majority_bent_f2",
            "bent_quadratic_f2",
            "masked_quadratic_f2",
            "noisy_cubic_chirp",
        ]
    )
    audits: list[HiddenShiftAuditRecord] = []
    for n_bits in range(min_bits, max_bits + 1):
        for family_id in family_ids:
            audits.append(audit_hidden_shift_family(family_id, n_bits, shift, sample_count=sample_count, seed=seed + n_bits))

    sieve_search = run_sieve_strategy_search(max(4, max_bits), sample_count=sieve_samples, seed=seed)
    sieve = sieve_search.baseline
    best_schedule = sieve_schedule_candidates(max(4, max_bits))[sieve_search.best_strategy]
    phase_trace = run_phase_state_collimation_trace(
        n_bits=max(4, max_bits),
        sample_count=sieve_samples,
        schedule=best_schedule,
        seed=seed,
        target_two_adic_valuation=sieve_search.baseline.target_two_adic_valuation,
        strategy=sieve_search.best_strategy,
    )
    scaling = build_scaling_history(audits)
    falsifiers = sorted({item for audit in audits for item in audit.falsifiers_triggered})
    high_risk_count = sum(1 for audit in audits if audit.dequantization_risk.startswith(("critical", "high")))
    structured_count = sum(1 for audit in audits if "structured" in audit.positive_signal or "flat" in audit.positive_signal)
    restricted_survivors = sum(1 for audit in audits if audit.survives_restricted_query_models)
    summary = (
        f"Audited {len(audits)} explicit hidden-shift instances across {len(family_ids)} phase families. "
        f"{structured_count} instances show Fourier/derivative structure; {high_risk_count} are critical/high dequantization risk; "
        f"{restricted_survivors} survive at least one restricted query model. "
        f"Best DHSP sieve strategy {sieve_search.best_strategy} reaches v2={sieve_search.best_two_adic_valuation} "
        f"from {sieve_search.sample_count} phase labels; explicit phase-state trace reaches "
        f"v2={phase_trace.best_two_adic_valuation} with {phase_trace.final_state_count} survivor states."
    )
    return HiddenShiftWorkbenchResult(utc_now(), audits, sieve, sieve_search, phase_trace, scaling, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def write_hidden_shift_negative_results(result: HiddenShiftWorkbenchResult) -> int:
    by_family: dict[str, list[HiddenShiftAuditRecord]] = {}
    for audit in result.family_audits:
        if audit.dequantization_risk.startswith(("critical", "high")):
            by_family.setdefault(audit.family.id, []).append(audit)

    written = 0
    for family_id, audits in by_family.items():
        latest = sorted(audits, key=lambda item: item.family.n_bits)[-1]
        successful_attacks = sorted(
            {
                attack.name
                for audit in audits
                for attack in audit.classical_attacks
                if attack.success and ("full_table" in attack.legal_query_models or "explicit_evaluator" in attack.legal_query_models)
            }
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=f"HS-DEQUANTIZED-{family_id.upper()}",
                source="phase_state_workbench.py",
                claim=f"{family_id} provides hidden-shift quantum advantage without additional restrictions.",
                reason_invalid=(
                    "Implemented full-table or explicit-evaluator classical attacks recover the shift; "
                    f"successful attacks: {', '.join(successful_attacks)}"
                ),
                lesson="Do not treat algebraic/Fourier structure as quantum advantage until it survives query-model-specific classical baselines.",
                applies_to=["DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "family_id": family_id,
                    "max_n_bits": latest.family.n_bits,
                    "dequantization_risk": latest.dequantization_risk,
                    "successful_attacks": successful_attacks,
                    "survives_restricted_query_models": latest.survives_restricted_query_models,
                },
            )
        )
        written += 1
    return written


def write_hidden_shift_workbench(
    output_path: Path = HIDDEN_SHIFT_AUDIT_PATH,
    families: Sequence[str] | None = None,
    min_bits: int = 5,
    max_bits: int = 8,
    shift: int = 7,
    sieve_samples: int = 2048,
    seed: int = 0,
    sample_count: int | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-DHS-GOWERS-SPECTRUM",
    registry_candidate_id: str = "DHS-GOWERS-SIEVE",
    registry_result_id: str = "RESULT-HIDDEN-SHIFT-WORKBENCH-LATEST",
) -> dict[str, Any]:
    result = run_hidden_shift_workbench(
        families=families,
        min_bits=min_bits,
        max_bits=max_bits,
        shift=shift,
        sieve_samples=sieve_samples,
        seed=seed,
        sample_count=sample_count,
    )
    payload = _json_ready(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_hidden_shift_negative_results(result)
        metrics = {
            "family_audit_count": len(result.family_audits),
            "high_dequantization_risk_count": sum(
                1 for audit in result.family_audits if audit.dequantization_risk.startswith(("critical", "high"))
            ),
            "restricted_query_survivor_count": sum(1 for audit in result.family_audits if audit.survives_restricted_query_models),
            "structured_signal_count": sum(
                1 for audit in result.family_audits if "structured" in audit.positive_signal or "flat" in audit.positive_signal
            ),
            "sieve_best_two_adic_valuation": result.sieve_baseline.best_two_adic_valuation,
            "sieve_target_two_adic_valuation": result.sieve_baseline.target_two_adic_valuation,
            "sieve_reached_target": result.sieve_baseline.reached_target,
            "sieve_best_strategy": result.sieve_search.best_strategy,
            "sieve_search_best_two_adic_valuation": result.sieve_search.best_two_adic_valuation,
            "sieve_search_best_memory_exponent_log2": result.sieve_search.best_memory_exponent_log2,
            "sieve_strategy_count": len(result.sieve_search.candidates),
            "sieve_initial_states": result.sieve_baseline.initial_states,
            "sieve_final_states": result.sieve_baseline.final_states,
            "phase_state_trace_best_two_adic_valuation": result.phase_state_trace.best_two_adic_valuation,
            "phase_state_trace_reached_target": result.phase_state_trace.reached_target,
            "phase_state_trace_success_probability_proxy": result.phase_state_trace.success_probability_proxy,
            "phase_state_trace_final_states": result.phase_state_trace.final_state_count,
            "phase_state_trace_survivor_sample_count": len(result.phase_state_trace.survivor_states_sample),
            "query_lower_bound_probe_count": sum(len(audit.query_lower_bound_probes) for audit in result.family_audits),
            "scaling_family_count": len(result.scaling_history),
            "negative_results_written": negative_results_written,
        }
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=result.created_at,
                status="needs-theory" if result.falsifiers_triggered else "promising",
                summary=result.summary,
                metrics=metrics,
                falsifiers_triggered=result.falsifiers_triggered,
                artifacts={"hidden_shift_audit": str(output_path)},
            )
        )
    return payload
