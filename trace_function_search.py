"""Natural finite-field trace-function hidden-shift search.

The fixed phase-family list is now mostly dead: low-degree, sparse Fourier,
sampled, or artificial-mask baselines explain it.  This module searches a small
natural algebraic space instead: rational trace functions over prime fields.
Every generated family is immediately attacked by low-degree finite differences,
sparse spectra, and sampled candidate-elimination baselines.  Survivors are not
promoted; they become lower-bound obligations.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

import numpy as np

from phase_state_workbench import next_prime_at_least
from research_registry import NegativeResultRecord, upsert_negative_result, upsert_scaling_run, utc_now


TRACE_FUNCTION_SEARCH_PATH = Path("research/phase_workbench/trace_function_search.json")


@dataclass(frozen=True)
class TraceFunctionSpec:
    id: str
    expression: str
    n_bits: int
    prime: int
    domain_size: int
    pole_count: int
    description: str


@dataclass(frozen=True)
class TraceFunctionAuditRecord:
    family_id: str
    expression: str
    n_bits: int
    prime: int
    domain_size: int
    pole_count: int
    low_degree_acceptance_degree4: float
    fourier_support_99: int
    fourier_top_mass: float
    derivative_best_support_99: int
    derivative_best_top_mass: float
    sample_count: int
    sample_candidate_count: int
    sample_unique_recovery: bool
    exhaustive_candidate_operations: int
    algebraic_decoder_success: bool
    algebraic_decoder_recovered_shift: int | None
    algebraic_decoder_residual_degree: int
    algebraic_decoder_operations: int
    status: str
    primary_blocker: str
    use_as_positive_evidence: bool
    next_action: str


@dataclass(frozen=True)
class TraceFunctionFamilySummary:
    family_id: str
    expression: str
    tested_n_bits: list[int]
    algebraic_decoder_count: int
    low_degree_count: int
    sparse_spectrum_count: int
    sample_dequantized_count: int
    unresolved_count: int
    best_status: str
    lesson: str


def _inv(value: int, prime: int) -> int | None:
    value %= prime
    if value == 0:
        return None
    return pow(value, prime - 2, prime)


def _term_inv_shift(x: int, prime: int, shift: int = 0, coefficient: int = 1) -> tuple[int, bool]:
    inv = _inv(x + shift, prime)
    if inv is None:
        return 0, True
    return (coefficient * inv) % prime, False


def _trace_expression_builders() -> dict[str, tuple[str, Callable[[int, int], tuple[int, bool]], str]]:
    def kloosterman(x: int, p: int) -> tuple[int, bool]:
        inv, pole = _term_inv_shift(x, p)
        return (x + inv) % p, pole

    def cubic_inverse(x: int, p: int) -> tuple[int, bool]:
        inv, pole = _term_inv_shift(x, p)
        return (pow(x, 3, p) + inv) % p, pole

    def quadratic_inverse(x: int, p: int) -> tuple[int, bool]:
        inv, pole = _term_inv_shift(x, p)
        return (pow(x, 2, p) + inv) % p, pole

    def two_pole(x: int, p: int) -> tuple[int, bool]:
        inv0, pole0 = _term_inv_shift(x, p)
        inv1, pole1 = _term_inv_shift(x, p, shift=1, coefficient=2)
        return (x + inv0 + inv1) % p, pole0 or pole1

    def cubic_two_pole(x: int, p: int) -> tuple[int, bool]:
        inv0, pole0 = _term_inv_shift(x, p)
        inv1, pole1 = _term_inv_shift(x, p, shift=1)
        return (pow(x, 3, p) + inv0 + inv1) % p, pole0 or pole1

    return {
        "trace_kloosterman_x_plus_inv": (
            "x + x^{-1}",
            kloosterman,
            "Kloosterman-style rank-2 trace function.",
        ),
        "trace_quadratic_plus_inv": (
            "x^2 + x^{-1}",
            quadratic_inverse,
            "Quadratic plus reciprocal trace function; tests whether adding one pole defeats low-degree baselines.",
        ),
        "trace_cubic_plus_inv": (
            "x^3 + x^{-1}",
            cubic_inverse,
            "Cubic plus reciprocal trace function; natural rational-phase stress test.",
        ),
        "trace_two_pole": (
            "x + x^{-1} + 2(x+1)^{-1}",
            two_pole,
            "Two-pole rational trace function with a small algebraic description.",
        ),
        "trace_cubic_two_pole": (
            "x^3 + x^{-1} + (x+1)^{-1}",
            cubic_two_pole,
            "Cubic two-pole rational trace function; harder natural family candidate.",
        ),
    }


def generate_trace_function_signal(family_id: str, n_bits: int) -> tuple[TraceFunctionSpec, np.ndarray, np.ndarray]:
    builders = _trace_expression_builders()
    if family_id not in builders:
        raise ValueError(f"unknown trace function family: {family_id}")
    expression, builder, description = builders[family_id]
    prime = next_prime_at_least(1 << n_bits)
    phases = np.zeros(prime, dtype=int)
    pole_count = 0
    for x in range(prime):
        value, pole = builder(x, prime)
        phases[x] = value % prime
        pole_count += int(pole)
    signal = np.exp(2j * np.pi * phases / prime)
    spec = TraceFunctionSpec(
        id=family_id,
        expression=expression,
        n_bits=n_bits,
        prime=prime,
        domain_size=prime,
        pole_count=pole_count,
        description=description,
    )
    return spec, phases, signal


def _finite_difference_acceptance(phases: np.ndarray, prime: int, degree: int = 4, samples: int = 128, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    order = degree + 1
    coefficients = [(-1) ** (order - index) * math.comb(order, index) for index in range(order + 1)]
    accepted = 0
    for _ in range(samples):
        x = int(rng.integers(0, prime))
        h = int(rng.integers(1, prime))
        total = 0
        for index, coefficient in enumerate(coefficients):
            total += coefficient * int(phases[(x + index * h) % prime])
        accepted += int(total % prime == 0)
    return accepted / max(1, samples)


def _spectrum_profile(signal: np.ndarray) -> tuple[int, float]:
    spectrum = np.fft.fft(signal) / math.sqrt(signal.size)
    power = np.abs(spectrum) ** 2
    probabilities = power / max(float(power.sum()), 1e-15)
    ordered = np.sort(probabilities)[::-1]
    support_99 = int(np.searchsorted(np.cumsum(ordered), 0.99) + 1)
    return support_99, float(ordered[0])


def _derivative_profile(signal: np.ndarray) -> tuple[int, float]:
    supports = []
    top_masses = []
    for shift in [1, 2, 3, 5, 8, 13, 21]:
        if shift >= signal.size:
            continue
        derivative = np.conjugate(signal) * np.roll(signal, -shift)
        support, top = _spectrum_profile(derivative)
        supports.append(support)
        top_masses.append(top)
    return int(min(supports)), float(max(top_masses))


def _sample_candidate_count(signal: np.ndarray, true_shift: int, sample_count: int, seed: int) -> tuple[int, bool]:
    rng = np.random.default_rng(seed)
    domain_size = signal.size
    positions = rng.choice(domain_size, size=min(sample_count, domain_size), replace=False)
    shifted = np.roll(signal, -true_shift % domain_size)
    observed = shifted[positions]
    candidates = 0
    for candidate in range(domain_size):
        predicted = signal[(positions + candidate) % domain_size]
        if np.allclose(predicted, observed, atol=1e-8):
            candidates += 1
    return candidates, candidates == 1


def _poly_trim(poly: Sequence[int], prime: int) -> list[int]:
    values = [int(item) % prime for item in poly]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return values or [0]


def _poly_is_zero(poly: Sequence[int], prime: int) -> bool:
    values = _poly_trim(poly, prime)
    return len(values) == 1 and values[0] == 0


def _poly_monic(poly: Sequence[int], prime: int) -> list[int]:
    values = _poly_trim(poly, prime)
    if _poly_is_zero(values, prime):
        return [0]
    inverse = pow(values[-1], -1, prime)
    return [(coefficient * inverse) % prime for coefficient in values]


def _poly_mul(left: Sequence[int], right: Sequence[int], prime: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_degree, left_coefficient in enumerate(left):
        for right_degree, right_coefficient in enumerate(right):
            result[left_degree + right_degree] = (
                result[left_degree + right_degree] + int(left_coefficient) * int(right_coefficient)
            ) % prime
    return _poly_trim(result, prime)


def _poly_mul_linear(poly: Sequence[int], constant_term: int, prime: int) -> list[int]:
    return _poly_mul(poly, [int(constant_term) % prime, 1], prime)


def _poly_mod(dividend: Sequence[int], divisor: Sequence[int], prime: int) -> list[int]:
    rem = _poly_trim(dividend, prime)
    div = _poly_trim(divisor, prime)
    if _poly_is_zero(div, prime):
        raise ZeroDivisionError("polynomial division by zero")
    inverse = pow(div[-1], -1, prime)
    while len(rem) >= len(div) and not _poly_is_zero(rem, prime):
        scale = (rem[-1] * inverse) % prime
        offset = len(rem) - len(div)
        for index, coefficient in enumerate(div):
            rem[offset + index] = (rem[offset + index] - scale * coefficient) % prime
        rem = _poly_trim(rem, prime)
    return rem


def _poly_gcd(left: Sequence[int], right: Sequence[int], prime: int) -> list[int]:
    a = _poly_trim(left, prime)
    b = _poly_trim(right, prime)
    while not _poly_is_zero(b, prime):
        a, b = b, _poly_mod(a, b, prime)
    return _poly_monic(a, prime)


def _poly_substitute_shift(poly_z: Sequence[int], position: int, prime: int) -> list[int]:
    """Substitute z = S + position in a univariate polynomial."""

    position = int(position) % prime
    result = [0]
    for z_power, coefficient in enumerate(poly_z):
        if coefficient % prime == 0:
            continue
        term = [0] * (z_power + 1)
        for s_power in range(z_power + 1):
            term[s_power] = (
                int(coefficient)
                * math.comb(z_power, s_power)
                * pow(position, z_power - s_power, prime)
            ) % prime
        if len(term) > len(result):
            result.extend([0] * (len(term) - len(result)))
        for index, value in enumerate(term):
            result[index] = (result[index] + value) % prime
    return _poly_trim(result, prime)


def _linear_root(poly: Sequence[int], prime: int) -> int | None:
    values = _poly_trim(poly, prime)
    if len(values) != 2 or values[1] == 0:
        return None
    return int((-values[0] * pow(values[1], -1, prime)) % prime)


def _trace_constraint_polynomial_z(family_id: str, observed_phase: int, prime: int) -> list[int]:
    a = int(observed_phase) % prime
    if family_id == "trace_kloosterman_x_plus_inv":
        poly = [1, -a, 1]
        if a == 0:
            poly = _poly_mul_linear(poly, 0, prime)
        return _poly_trim(poly, prime)
    if family_id == "trace_quadratic_plus_inv":
        poly = [1, -a, 0, 1]
        if a == 0:
            poly = _poly_mul_linear(poly, 0, prime)
        return _poly_trim(poly, prime)
    if family_id == "trace_cubic_plus_inv":
        poly = [1, -a, 0, 0, 1]
        if a == 0:
            poly = _poly_mul_linear(poly, 0, prime)
        return _poly_trim(poly, prime)
    if family_id == "trace_two_pole":
        poly = [1, 3 - a, 1 - a, 1]
        if a == 2 % prime:
            poly = _poly_mul_linear(poly, 0, prime)
        if a == (-2) % prime:
            poly = _poly_mul_linear(poly, 1, prime)
        return _poly_trim(poly, prime)
    if family_id == "trace_cubic_two_pole":
        poly = [1, 2 - a, -a, 0, 1, 1]
        if a == 1 % prime:
            poly = _poly_mul_linear(poly, 0, prime)
        if a == (-2) % prime:
            poly = _poly_mul_linear(poly, 1, prime)
        return _poly_trim(poly, prime)
    raise ValueError(f"unknown trace function family: {family_id}")


def algebraic_rational_shift_decoder(
    family_id: str,
    phases: np.ndarray,
    true_shift: int,
    sample_count: int,
    seed: int,
) -> tuple[bool, int | None, int, int]:
    prime = int(phases.size)
    rng = np.random.default_rng(seed)
    positions = rng.choice(prime, size=min(int(sample_count), prime), replace=False)
    gcd_poly: list[int] | None = None
    max_degree = 0
    for position in positions:
        observed_phase = int(phases[(int(position) + int(true_shift)) % prime])
        constraint_z = _trace_constraint_polynomial_z(family_id, observed_phase, prime)
        constraint_shift = _poly_substitute_shift(constraint_z, int(position), prime)
        max_degree = max(max_degree, len(constraint_shift) - 1)
        gcd_poly = constraint_shift if gcd_poly is None else _poly_gcd(gcd_poly, constraint_shift, prime)
        if len(gcd_poly) <= 2:
            break
    residual_degree = len(gcd_poly or [0]) - 1
    recovered = _linear_root(gcd_poly or [0], prime)
    operations = int(max(1, sample_count) * max(1, max_degree) ** 2)
    return recovered == int(true_shift) % prime, recovered, residual_degree, operations


def audit_trace_function_family(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int = 7,
    seed: int = 0,
) -> TraceFunctionAuditRecord:
    spec, phases, signal = generate_trace_function_signal(family_id, n_bits)
    low_degree_acceptance = _finite_difference_acceptance(phases, spec.prime, degree=4, seed=seed + n_bits)
    fourier_support, fourier_top = _spectrum_profile(signal)
    derivative_support, derivative_top = _derivative_profile(signal)
    true_shift = shift % spec.domain_size
    candidate_count, sample_unique = _sample_candidate_count(signal, true_shift, sample_count, seed=seed + 17)
    algebraic_success, algebraic_recovered, algebraic_degree, algebraic_operations = algebraic_rational_shift_decoder(
        family_id=family_id,
        phases=phases,
        true_shift=true_shift,
        sample_count=sample_count,
        seed=seed + 37,
    )
    poly_sparse_threshold = max(8, spec.n_bits**2)
    operations = int(spec.domain_size * sample_count)

    if algebraic_success:
        status = "rejected-algebraic-rational-decoder"
        blocker = "constant-degree-rational-shift-decoder"
        next_action = "Discard this rational trace family; constant-degree equations recover the shift from samples."
    elif low_degree_acceptance >= 0.999:
        status = "rejected-low-degree-trace"
        blocker = "low-degree-classical-reconstruction"
        next_action = "Discard as a low-degree trace control."
    elif fourier_support <= poly_sparse_threshold or derivative_support <= poly_sparse_threshold:
        status = "rejected-sparse-spectrum-trace"
        blocker = "sparse-fourier-classical-reconstruction"
        next_action = "Discard unless sparse Fourier access is formally illegal."
    elif sample_unique:
        status = "rejected-sample-elimination"
        blocker = "sample-limited-classical-reconstruction"
        next_action = "Discard under sampled access or prove candidate-elimination time is the relevant barrier."
    else:
        status = "unresolved-natural-trace-family"
        blocker = "missing-lower-bound"
        next_action = "Increase n, add algebraic decoders, and attach lower-bound obligations before promotion."

    return TraceFunctionAuditRecord(
        family_id=spec.id,
        expression=spec.expression,
        n_bits=spec.n_bits,
        prime=spec.prime,
        domain_size=spec.domain_size,
        pole_count=spec.pole_count,
        low_degree_acceptance_degree4=low_degree_acceptance,
        fourier_support_99=fourier_support,
        fourier_top_mass=fourier_top,
        derivative_best_support_99=derivative_support,
        derivative_best_top_mass=derivative_top,
        sample_count=int(sample_count),
        sample_candidate_count=int(candidate_count),
        sample_unique_recovery=bool(sample_unique),
        exhaustive_candidate_operations=operations,
        algebraic_decoder_success=bool(algebraic_success),
        algebraic_decoder_recovered_shift=algebraic_recovered,
        algebraic_decoder_residual_degree=int(algebraic_degree),
        algebraic_decoder_operations=int(algebraic_operations),
        status=status,
        primary_blocker=blocker,
        use_as_positive_evidence=False,
        next_action=next_action,
    )


def build_trace_function_search_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else sorted(_trace_expression_builders())
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    active_samples = list(sample_counts) if sample_counts is not None else [8, 16, 32, 64]
    records = [
        audit_trace_function_family(
            family_id=family_id,
            n_bits=n_bits,
            sample_count=sample_count,
            shift=shift,
            seed=seed + n_bits * 1009 + sample_count * 17,
        )
        for family_id in active_families
        for n_bits in active_n
        for sample_count in active_samples
    ]
    summaries = build_family_summaries(records)
    unresolved_count = sum(1 for record in records if record.status == "unresolved-natural-trace-family")
    return {
        "id": "TRACE-FUNCTION-SEARCH-LATEST",
        "created_at": utc_now(),
        "kind": "finite-field-trace-function-search",
        "families": active_families,
        "n_values": active_n,
        "sample_counts": active_samples,
        "status": "trace-families-need-lower-bound-review" if unresolved_count else "all-trace-families-rejected",
        "record_count": len(records),
        "summary": (
            f"Audited {len(records)} rational finite-field trace-function hidden-shift rows across "
            f"{len(active_families)} families; {unresolved_count} rows survive current implemented baselines but remain lower-bound debt."
        ),
        "headline_metrics": {
            "algebraic_decoder_rejected_count": sum(1 for record in records if record.status == "rejected-algebraic-rational-decoder"),
            "low_degree_rejected_count": sum(1 for record in records if record.status == "rejected-low-degree-trace"),
            "sparse_spectrum_rejected_count": sum(1 for record in records if record.status == "rejected-sparse-spectrum-trace"),
            "sample_elimination_rejected_count": sum(1 for record in records if record.status == "rejected-sample-elimination"),
            "unresolved_count": unresolved_count,
            "positive_evidence_count": sum(1 for record in records if record.use_as_positive_evidence),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "records": [asdict(record) for record in records],
    }


def build_family_summaries(records: Sequence[TraceFunctionAuditRecord]) -> list[TraceFunctionFamilySummary]:
    by_family: dict[str, list[TraceFunctionAuditRecord]] = {}
    for record in records:
        by_family.setdefault(record.family_id, []).append(record)
    summaries: list[TraceFunctionFamilySummary] = []
    for family_id, items in sorted(by_family.items()):
        algebraic = sum(1 for item in items if item.status == "rejected-algebraic-rational-decoder")
        low_degree = sum(1 for item in items if item.status == "rejected-low-degree-trace")
        sparse = sum(1 for item in items if item.status == "rejected-sparse-spectrum-trace")
        sample = sum(1 for item in items if item.status == "rejected-sample-elimination")
        unresolved = sum(1 for item in items if item.status == "unresolved-natural-trace-family")
        if algebraic:
            status = "reject-algebraic-rational-decoder"
            lesson = "Constant-degree rational equations recover the hidden shift; this natural trace family is classically learnable."
        elif sample:
            status = "reject-sampled-trace-family"
            lesson = "Sampled candidate elimination recovers shifts on tested rows; do not use as positive evidence."
        elif sparse:
            status = "reject-sparse-spectrum-trace-family"
            lesson = "Sparse spectrum or derivative spectrum creates a classical reconstruction route."
        elif low_degree:
            status = "reject-low-degree-trace-family"
            lesson = "Finite-difference tests identify low-degree trace structure."
        else:
            status = "unresolved-natural-trace-family"
            lesson = "Natural trace family survived implemented baselines but needs larger scaling and lower-bound work."
        summaries.append(
            TraceFunctionFamilySummary(
                family_id=family_id,
                expression=items[0].expression,
                tested_n_bits=sorted({item.n_bits for item in items}),
                algebraic_decoder_count=algebraic,
                low_degree_count=low_degree,
                sparse_spectrum_count=sparse,
                sample_dequantized_count=sample,
                unresolved_count=unresolved,
                best_status=status,
                lesson=lesson,
            )
        )
    return summaries


def write_trace_function_search_report(
    output_path: Path = TRACE_FUNCTION_SEARCH_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_trace_function_search_report(
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
                "row_count": payload["record_count"],
                "artifacts": {"trace_function_search": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
        write_negative_results_from_trace_search(payload)
    return payload


def write_negative_results_from_trace_search(payload: dict[str, Any]) -> int:
    written = 0
    for summary in payload.get("family_summaries", []):
        if not str(summary.get("best_status", "")).startswith("reject"):
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"TRACE-FUNCTION-REJECT-{summary['family_id'].upper()}",
                source="trace_function_search.py",
                claim=f"{summary['family_id']} is a viable natural trace-function hidden-shift family.",
                reason_invalid=summary["lesson"],
                lesson="Natural algebraic description is not enough; every trace family must survive sample, spectral, and low-degree baselines.",
                applies_to=["DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "family_id": summary["family_id"],
                    "expression": summary["expression"],
                    "tested_n_bits": summary["tested_n_bits"],
                    "best_status": summary["best_status"],
                },
            )
        )
        written += 1
    return written
