"""Structural tests for quantum-algorithm research leads.

These tests are intentionally not "did a 3-qubit circuit work?" checks.  They
look for scalable structure that known major quantum algorithms exploit:
Fourier concentration, hidden periodicity, hidden-shift distinguishability,
coset-state information, and spectral gaps for walk-based approaches.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Iterable, Sequence

import numpy as np


@dataclass(frozen=True)
class FourierMetrics:
    """Summary of a Boolean function's Walsh-Fourier spectrum."""

    n_bits: int
    entropy_bits: float
    top_coefficient_mass: float
    support_99_percent: int
    effective_support: float
    flatness_ratio: float


@dataclass(frozen=True)
class PeriodicityMetrics:
    """Collision/autocorrelation evidence for a hidden period."""

    domain_size: int
    best_nonzero_shift: int | None
    best_nonzero_collision_rate: float
    perfect_periods: list[int]
    collision_rates: dict[int, float]


@dataclass(frozen=True)
class HiddenShiftMetrics:
    """Signals relevant to abelian hidden-shift algorithms."""

    domain_size: int
    fourier_entropy_bits: float
    fourier_flatness_ratio: float
    autocorrelation_peak_ratio: float
    shift_signal_quality: str


@dataclass(frozen=True)
class CosetFingerprintMetrics:
    """Information content of small hidden-structure instances.

    The fingerprint vector is the equality relation R_h(x, y)=1[f_h(x)=f_h(y)].
    If different hidden objects produce nearly identical relation fingerprints,
    then the instance family is unlikely to yield useful single-register
    information and needs stronger collective measurements or a different handle.
    """

    instance_count: int
    domain_size: int
    relation_rank: int
    average_pairwise_overlap: float
    max_pairwise_overlap: float
    distinguishability: str


@dataclass(frozen=True)
class WalkSpectralMetrics:
    """Basic spectral data for candidate quantum-walk search spaces."""

    vertex_count: int
    regular: bool
    degree_min: float
    degree_max: float
    spectral_gap: float
    marked_overlap: float | None


@dataclass(frozen=True)
class GowersMetrics:
    """Higher-order uniformity signal for Boolean phase functions on F_2^n."""

    n_bits: int
    order: int
    norm: float
    norm_power: float
    interpretation: str


@dataclass(frozen=True)
class DerivativeSpectrumMetrics:
    """Fourier sparsity after taking Boolean finite derivatives."""

    n_bits: int
    sampled_derivatives: int
    best_support_99_percent: int
    median_support_99_percent: float
    best_top_coefficient_mass: float
    candidate_for_higher_order_fourier: bool


def as_jsonable(obj):
    """Return a JSON-friendly representation of a dataclass result."""

    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    return obj


def truth_table_from_boolean(fn: Callable[[int], int], n_bits: int) -> np.ndarray:
    """Return +/-1 truth table for a Boolean function on {0,1}^n."""

    size = 1 << n_bits
    values = np.empty(size, dtype=float)
    for x in range(size):
        bit = int(fn(x)) & 1
        values[x] = 1.0 if bit == 0 else -1.0
    return values


def walsh_hadamard_transform(signal: Sequence[float]) -> np.ndarray:
    """Fast Walsh-Hadamard transform for a vector of power-of-two length."""

    values = np.asarray(signal, dtype=float).copy()
    n = values.shape[0]
    if n == 0 or n & (n - 1):
        raise ValueError("Walsh-Hadamard input length must be a power of two")

    step = 1
    while step < n:
        for start in range(0, n, step * 2):
            left = values[start : start + step].copy()
            right = values[start + step : start + 2 * step].copy()
            values[start : start + step] = left + right
            values[start + step : start + 2 * step] = left - right
        step *= 2
    return values


def fourier_metrics(signal: Sequence[float]) -> FourierMetrics:
    """Measure Fourier concentration for a Boolean phase signal."""

    values = np.asarray(signal, dtype=float)
    size = values.shape[0]
    if size == 0 or size & (size - 1):
        raise ValueError("signal length must be a non-zero power of two")

    coeffs = walsh_hadamard_transform(values) / np.sqrt(size)
    power = np.square(np.abs(coeffs))
    total = float(power.sum())
    if total <= 0:
        raise ValueError("signal has zero Fourier power")

    probabilities = power / total
    nonzero = probabilities[probabilities > 1e-15]
    entropy = float(-np.sum(nonzero * np.log2(nonzero)))
    ordered = np.sort(probabilities)[::-1]
    support_99 = int(np.searchsorted(np.cumsum(ordered), 0.99) + 1)
    effective_support = float(2.0**entropy)
    flatness_ratio = float(nonzero.min() / nonzero.max()) if len(nonzero) else 0.0

    return FourierMetrics(
        n_bits=int(np.log2(size)),
        entropy_bits=entropy,
        top_coefficient_mass=float(ordered[0]),
        support_99_percent=support_99,
        effective_support=effective_support,
        flatness_ratio=flatness_ratio,
    )


def periodicity_metrics(labels: Sequence[object]) -> PeriodicityMetrics:
    """Find shifts that preserve a labeled finite function."""

    values = list(labels)
    size = len(values)
    if size < 2:
        raise ValueError("need at least two labels")

    rates: dict[int, float] = {}
    perfect: list[int] = []
    for shift in range(1, size):
        collisions = sum(1 for x in range(size) if values[x] == values[(x + shift) % size])
        rate = collisions / size
        rates[shift] = rate
        if rate == 1.0:
            perfect.append(shift)

    best_shift = max(rates, key=rates.get) if rates else None
    best_rate = rates[best_shift] if best_shift is not None else 0.0
    return PeriodicityMetrics(size, best_shift, best_rate, perfect, rates)


def hidden_shift_metrics(base_signal: Sequence[float]) -> HiddenShiftMetrics:
    """Score whether a cyclic hidden-shift family has a useful Fourier handle."""

    values = np.asarray(base_signal, dtype=float)
    size = values.shape[0]
    if size < 2:
        raise ValueError("need at least two signal values")

    spectrum = np.fft.fft(values) / np.sqrt(size)
    power = np.square(np.abs(spectrum))
    nonzero = power[power > 1e-15]
    probabilities = power / float(power.sum())
    p_nonzero = probabilities[probabilities > 1e-15]
    entropy = float(-np.sum(p_nonzero * np.log2(p_nonzero)))
    flatness = float(nonzero.min() / nonzero.max()) if len(nonzero) else 0.0

    autocorr = np.fft.ifft(np.square(np.abs(np.fft.fft(values)))).real
    peak0 = abs(float(autocorr[0]))
    next_peak = max(abs(float(x)) for x in autocorr[1:]) if size > 1 else 0.0
    peak_ratio = next_peak / peak0 if peak0 else 0.0

    if flatness > 0.8 and peak_ratio < 0.35:
        quality = "strong: flat spectrum and low autocorrelation aliases"
    elif flatness > 0.3 and peak_ratio < 0.65:
        quality = "mixed: some shift signal, but aliases may dominate"
    else:
        quality = "weak: likely classical correlation or noisy Fourier signal"

    return HiddenShiftMetrics(size, entropy, flatness, peak_ratio, quality)


def gowers_uniformity_metrics(signal: Sequence[float], order: int) -> GowersMetrics:
    """Compute exact U^k norm for small Boolean phase functions over F_2^n.

    For a phase function f:{0,1}^n -> {-1,+1}, U^k detects degree < k
    polynomial structure. Hidden-shift algorithms for quadratics and functions
    with large Gowers norms make this a useful early structural test.
    """

    values = np.asarray(signal, dtype=float)
    size = values.shape[0]
    if size == 0 or size & (size - 1):
        raise ValueError("signal length must be a non-zero power of two")
    if order < 1:
        raise ValueError("order must be positive")

    n_bits = int(np.log2(size))
    total = 0.0
    count = 0
    corners = list(range(1 << order))
    for x in range(size):
        for hs in np.ndindex(*(size for _ in range(order))):
            product = 1.0
            for corner in corners:
                point = x
                for bit in range(order):
                    if corner & (1 << bit):
                        point ^= hs[bit]
                product *= values[point]
            total += product
            count += 1

    norm_power = total / count
    norm = float(abs(norm_power) ** (1.0 / (1 << order)))
    if norm > 0.98:
        interpretation = "very high: consistent with degree < order polynomial phase"
    elif norm > 0.7:
        interpretation = "high: possible exploitable higher-order structure"
    elif norm > 0.35:
        interpretation = "mixed: structure exists but may be noisy or classical"
    else:
        interpretation = "low: likely pseudorandom for this order"

    return GowersMetrics(n_bits, order, norm, float(norm_power), interpretation)


def derivative_signal(signal: Sequence[float], shift: int) -> np.ndarray:
    """Return multiplicative derivative D_h f(x)=f(x)f(x+h) over F_2^n."""

    values = np.asarray(signal, dtype=float)
    size = values.shape[0]
    if size == 0 or size & (size - 1):
        raise ValueError("signal length must be a non-zero power of two")
    if shift < 0 or shift >= size:
        raise ValueError("shift out of range")
    return np.array([values[x] * values[x ^ shift] for x in range(size)], dtype=float)


def derivative_spectrum_metrics(
    signal: Sequence[float], shifts: Sequence[int] | None = None
) -> DerivativeSpectrumMetrics:
    """Measure whether derivatives reveal sparse Fourier spectra."""

    values = np.asarray(signal, dtype=float)
    size = values.shape[0]
    if size == 0 or size & (size - 1):
        raise ValueError("signal length must be a non-zero power of two")
    n_bits = int(np.log2(size))

    if shifts is None:
        shifts = list(range(1, size))
    shifts = [int(shift) for shift in shifts if 0 < int(shift) < size]
    if not shifts:
        raise ValueError("need at least one nonzero derivative shift")

    supports = []
    top_masses = []
    for shift in shifts:
        metrics = fourier_metrics(derivative_signal(values, shift))
        supports.append(metrics.support_99_percent)
        top_masses.append(metrics.top_coefficient_mass)

    best_support = int(min(supports))
    median_support = float(np.median(supports))
    best_top_mass = float(max(top_masses))
    candidate = best_support <= max(2, n_bits) and best_top_mass > 0.5

    return DerivativeSpectrumMetrics(
        n_bits=n_bits,
        sampled_derivatives=len(shifts),
        best_support_99_percent=best_support,
        median_support_99_percent=median_support,
        best_top_coefficient_mass=best_top_mass,
        candidate_for_higher_order_fourier=bool(candidate),
    )


def coset_fingerprint_metrics(label_tables: Iterable[Sequence[object]]) -> CosetFingerprintMetrics:
    """Compare hidden-structure instances through their equality relations."""

    tables = [list(table) for table in label_tables]
    if not tables:
        raise ValueError("need at least one label table")
    size = len(tables[0])
    if any(len(table) != size for table in tables):
        raise ValueError("all label tables must share one domain size")

    vectors = []
    for table in tables:
        rel = np.zeros(size * size, dtype=float)
        for x in range(size):
            for y in range(size):
                rel[x * size + y] = 1.0 if table[x] == table[y] else 0.0
        norm = np.linalg.norm(rel)
        vectors.append(rel / norm if norm else rel)

    matrix = np.vstack(vectors)
    gram = matrix @ matrix.T
    off_diag = gram[np.triu_indices(len(tables), k=1)]
    avg_overlap = float(off_diag.mean()) if off_diag.size else 1.0
    max_overlap = float(off_diag.max()) if off_diag.size else 1.0
    rank = int(np.linalg.matrix_rank(matrix, tol=1e-9))

    if max_overlap < 0.25 and rank == len(tables):
        distinguishability = "strong single-register relation signal"
    elif max_overlap < 0.75:
        distinguishability = "partial signal; test collective measurements"
    else:
        distinguishability = "weak signal; likely needs a new observable"

    return CosetFingerprintMetrics(
        instance_count=len(tables),
        domain_size=size,
        relation_rank=rank,
        average_pairwise_overlap=avg_overlap,
        max_pairwise_overlap=max_overlap,
        distinguishability=distinguishability,
    )


def walk_spectral_metrics(
    adjacency: Sequence[Sequence[float]], marked: Sequence[int] | None = None
) -> WalkSpectralMetrics:
    """Compute normalized-walk spectral gap and marked-state overlap."""

    adj = np.asarray(adjacency, dtype=float)
    if adj.ndim != 2 or adj.shape[0] != adj.shape[1]:
        raise ValueError("adjacency must be a square matrix")
    if not np.allclose(adj, adj.T):
        raise ValueError("adjacency must be symmetric")

    degrees = adj.sum(axis=1)
    if np.any(degrees <= 0):
        raise ValueError("all vertices must have positive degree")

    inv_sqrt = np.diag(1.0 / np.sqrt(degrees))
    normalized = inv_sqrt @ adj @ inv_sqrt
    eigenvalues = np.sort(np.linalg.eigvalsh(normalized))[::-1]
    spectral_gap = float(1.0 - eigenvalues[1]) if len(eigenvalues) > 1 else 0.0

    overlap = None
    if marked is not None:
        marked_set = set(int(v) for v in marked)
        if any(v < 0 or v >= adj.shape[0] for v in marked_set):
            raise ValueError("marked vertex index out of range")
        overlap = len(marked_set) / adj.shape[0]

    return WalkSpectralMetrics(
        vertex_count=adj.shape[0],
        regular=bool(np.allclose(degrees, degrees[0])),
        degree_min=float(degrees.min()),
        degree_max=float(degrees.max()),
        spectral_gap=spectral_gap,
        marked_overlap=overlap,
    )
