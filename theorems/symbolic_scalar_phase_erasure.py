"""Sparse symbolic-scalar phase-erasure adapter and certified class-descent controller.

This standalone module connects the public symbolic scalar packets produced by
``ut5_scalar_phase_compiler.compile_scalar_packet`` and
``class_four_scalar_phase_compiler.compile_variable_scalar_packet`` to public
cubic/quadratic/linear phase erasure without materializing dense
``1 + h + h*(h+1)//2`` lifted parameter tables or evaluating hidden potentials,
and implements the public certified lower-central-series class-descent
controller from Section 4 of ``research/BOUNDED_CLASS_METABELIAN_HSP.md``.

Scope boundaries:
- Classical public algebra and finite reference controls only; not a coherent
  quantum gate compiler, general-prime SDE solver, or full HSP execution.
- Packet provenance (``instance_id``, ``chart_id``, ``parameter_basis``) is
  explicitly pinned across merges, and consumed packets (including zero-scale
  inputs) are permanently retired.
- All novelty, speedup, and accepted-candidate flags remain ``False``.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from math import ceil, comb, log
from pathlib import Path
import random
from typing import Callable, Sequence

from flint import fmpz_mod_ctx, fmpz_mod_mat

from theorems.graded_hsp_phase_descent import _canonical, _dependence
from theorems.nil3_guarded_cyclic_dispatch import (
    conic_failure_bound,
    independent_columns_exact,
    square_weights_capped,
)
from theorems.prime_character_opi import ring
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "research" / "reductions" / "symbolic_scalar_phase_erasure.json"
MD_PATH = ROOT / "research" / "SYMBOLIC_SCALAR_PHASE_ERASURE.md"


def _canonical_vec(vec: Sequence[int], dim: int, p: int) -> None:
    _canonical(vec, dim, p)


def _dependence_exact(p: int, vectors: Sequence[Sequence[int]]) -> list[int]:
    return [int(x) % p for x in _dependence(p, vectors)]


def _fmpz_rref(rows: Sequence[Sequence[int]], p: int) -> tuple[list[list[int]], int]:
    """Exact row-reduced echelon form over GF(p) for arbitrary-precision primes."""
    if not rows or not rows[0]:
        return [], 0
    ctx = fmpz_mod_ctx(p)
    mat = fmpz_mod_mat([[int(x) % p for x in row] for row in rows], ctx)
    reduced, rank = mat.rref()
    rank = int(rank)
    out = [
        [int(reduced[i, j]) for j in range(reduced.ncols())]
        for i in range(rank)
    ]
    return out, rank


def _fmpz_row_space_basis(vectors: Sequence[Sequence[int]], dim: int, p: int) -> list[tuple[int, ...]]:
    """Retain independent vectors in insertion order over GF(p)."""
    basis: list[tuple[int, ...]] = []
    for vec in vectors:
        _canonical_vec(vec, dim, p)
        if not any(vec):
            continue
        candidate = [list(b) for b in basis] + [list(vec)]
        _, rank = _fmpz_rref(candidate, p)
        if rank > len(basis):
            basis.append(tuple(int(x) % p for x in vec))
    return basis


def _fmpz_nullspace_basis(rows: Sequence[Sequence[int]], width: int, p: int) -> list[tuple[int, ...]]:
    """Exact right nullspace basis of ``rows`` in F_p^width using fmpz_mod_mat."""
    ring(p)
    if width < 1:
        raise ValueError("positive vector width required")
    if not rows:
        return [tuple(int(i == j) for j in range(width)) for i in range(width)]
    for row in rows:
        _canonical_vec(row, width, p)
    reduced, rank = _fmpz_rref(rows, p)
    pivots: list[int] = []
    for r in range(rank):
        pivot = next(c for c in range(width) if reduced[r][c] != 0)
        pivots.append(pivot)
    pivot_set = set(pivots)
    free_cols = [c for c in range(width) if c not in pivot_set]
    basis: list[tuple[int, ...]] = []
    for free in free_cols:
        vec = [0] * width
        vec[free] = 1
        for r, pivot in enumerate(pivots):
            vec[pivot] = (-reduced[r][free]) % p
        basis.append(tuple(vec))
    return basis


def _fmpz_solve_coordinates(
    basis: Sequence[Sequence[int]],
    target: Sequence[int],
    p: int,
) -> tuple[int, ...] | None:
    """Solve sum_i c_i * basis[i] = target over GF(p), or return None if not in span."""
    if not basis:
        return () if not any(int(x) % p for x in target) else None
    dim = len(target)
    _canonical_vec(target, dim, p)
    k = len(basis)
    augmented = [
        [int(basis[col][row]) % p for col in range(k)] + [int(target[row]) % p]
        for row in range(dim)
    ]
    reduced, rank = _fmpz_rref(augmented, p)
    for r in range(rank):
        if all(reduced[r][c] == 0 for c in range(k)) and reduced[r][k] != 0:
            return None
    coords = [0] * k
    for r in range(rank):
        pivot = next((c for c in range(k) if reduced[r][c] != 0), None)
        if pivot is not None:
            coords[pivot] = int(reduced[r][k]) % p
    return tuple(coords)


@dataclass
class PinnedSymbolicPacket:
    """Provenance-pinned wrapper around a public ``SymbolicScalarPacket``.

    Packets in an erasure tree must share the exact same ``instance_id``,
    ``chart_id``, ``p``, ``quotient_width``, ``jet_width``, and ordered
    ``parameter_basis``. Once a packet participates in a shear merge (even
    with scale zero), ``consumed`` is set to ``True`` and any further use is
    rejected.
    """

    instance_id: str
    chart_id: str
    packet: SymbolicScalarPacket
    consumed: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.instance_id, str) or not self.instance_id.strip():
            raise ValueError("nonempty instance_id string required")
        if not isinstance(self.chart_id, str) or not self.chart_id.strip():
            raise ValueError("nonempty chart_id string required")
        if not isinstance(self.packet, SymbolicScalarPacket):
            raise TypeError("SymbolicScalarPacket instance required")
        ring(self.packet.p)
        if self.packet.quotient_width < 1 or self.packet.jet_width < 0:
            raise ValueError("positive quotient width and nonnegative jet width required")
        if not self.packet.parameter_basis:
            raise ValueError("nonempty symbolic parameter basis required")
        h = len(self.packet.parameter_basis)
        cleaned: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
        for (alpha, params), coeff in self.packet.terms.items():
            if len(alpha) != self.packet.width or any(type(a) is not int or a < 0 for a in alpha):
                raise ValueError("canonical monomial exponent tuple required")
            if sum(alpha) > 3:
                raise ValueError("SymbolicScalarPacket degree exceeds cubic bound")
            if (
                len(params) > 2
                or tuple(sorted(params)) != tuple(params)
                or any(type(idx) is not int or not 0 <= idx < h for idx in params)
            ):
                raise ValueError("canonical lifted parameter indices of degree <= 2 required")
            if type(coeff) is not int:
                raise ValueError("integer field coefficient required")
            val = coeff % self.packet.p
            if val and any(alpha):
                cleaned[(tuple(alpha), tuple(params))] = val
        self.packet = SymbolicScalarPacket(
            self.packet.p,
            self.packet.quotient_width,
            self.packet.jet_width,
            self.packet.parameter_basis,
            cleaned,
        )

    @property
    def p(self) -> int:
        return self.packet.p

    @property
    def width(self) -> int:
        return self.packet.width

    @property
    def degree(self) -> int:
        return self.packet.degree

    @property
    def provenance_key(self) -> tuple[str, str, int, int, int, tuple[tuple[int, tuple[int, ...]], ...]]:
        return (
            self.instance_id,
            self.chart_id,
            self.packet.p,
            self.packet.quotient_width,
            self.packet.jet_width,
            self.packet.parameter_basis,
        )


def pin_symbolic_packet(
    packet: SymbolicScalarPacket,
    *,
    instance_id: str,
    chart_id: str,
) -> PinnedSymbolicPacket:
    """Bind a public ``SymbolicScalarPacket`` to an explicit instance and chart."""
    return PinnedSymbolicPacket(instance_id=instance_id, chart_id=chart_id, packet=packet)


def _validate_compatible_batch(
    packets: Sequence[PinnedSymbolicPacket],
    max_degree: int,
) -> PinnedSymbolicPacket:
    if not packets:
        raise ValueError("nonempty sequence of PinnedSymbolicPacket required")
    first = packets[0]
    if not isinstance(first, PinnedSymbolicPacket):
        raise TypeError("PinnedSymbolicPacket instances required")
    seen_ids: set[int] = set()
    for pkt in packets:
        if not isinstance(pkt, PinnedSymbolicPacket):
            raise TypeError("PinnedSymbolicPacket instances required")
        if id(pkt) in seen_ids:
            raise ValueError("distinct packet wrapper instances required for each physical input")
        seen_ids.add(id(pkt))
        if pkt.consumed:
            raise ValueError("consumed packet cannot be reused in another merge")
        if pkt.provenance_key != first.provenance_key:
            raise ValueError("packets must share pinned instance_id, chart_id, dimensions, and parameter_basis")
        if pkt.degree > max_degree:
            raise ValueError(f"packet degree {pkt.degree} exceeds stage degree {max_degree}")
    return first


def sparse_leading_columns(
    packets: Sequence[PinnedSymbolicPacket],
    degree: int,
) -> tuple[list[tuple[int, ...]], tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]]:
    """Extract homogeneous degree-``degree`` coefficient columns over active lifted keys."""
    if degree not in (1, 2, 3):
        raise ValueError("implemented degrees are 1, 2, 3")
    _validate_compatible_batch(packets, degree)
    active_keys = tuple(
        sorted(
            {
                key
                for pkt in packets
                for key in pkt.packet.terms
                if sum(key[0]) == degree
            }
        )
    )
    if not active_keys:
        return [(0,) for _ in packets], ()
    columns = [
        tuple(pkt.packet.terms.get(key, 0) for key in active_keys)
        for pkt in packets
    ]
    return columns, active_keys


def verify_diagonal_witness(
    p: int,
    columns: Sequence[Sequence[int]],
    weights: Sequence[int],
    degree: int,
) -> None:
    """Deterministically verify a proposed diagonal cancellation witness on original columns."""
    ring(p)
    if degree not in (1, 2, 3):
        raise ValueError("implemented degrees are 1, 2, 3")
    if not columns or not columns[0]:
        raise ValueError("nonempty coefficient columns required")
    if len(weights) != len(columns):
        raise ValueError("witness length must match number of columns")
    _canonical_vec(weights, len(columns), p)
    if not any(weights):
        raise ArithmeticError("all-zero diagonal cancellation witness rejected")
    row_count = len(columns[0])
    for col in columns:
        _canonical_vec(col, row_count, p)
    powered = [pow(int(w), degree, p) for w in weights]
    for row_idx in range(row_count):
        total = sum(columns[col_idx][row_idx] * powered[col_idx] for col_idx in range(len(columns))) % p
        if total != 0:
            raise ArithmeticError(f"public leading-degree cancellation failed at equation row {row_idx}")


def sparse_cancellation_weights(
    packets: Sequence[PinnedSymbolicPacket],
    degree: int,
    *,
    rng: random.Random | None = None,
    conic_cap: int = 64,
) -> tuple[list[int], int, int]:
    """Compute and verify public leading-degree cancellation scales for sparse packets."""
    if degree not in (1, 2, 3):
        raise ValueError("implemented degrees are 1, 2, 3")
    first = _validate_compatible_batch(packets, degree)
    p = first.p
    columns, active_keys = sparse_leading_columns(packets, degree)
    compressed, rank = independent_columns_exact(columns, p)
    if rank == 0:
        weights = [1] + [0] * (len(packets) - 1)
    elif degree == 2:
        weights = square_weights_capped(
            p,
            compressed,
            rng or random.Random(0),
            conic_attempt_cap=conic_cap,
        )
    else:
        if len(compressed) < rank + 1:
            raise ValueError(f"degree-{degree} controller needs {rank + 1} columns at rank {rank}")
        coefficients = _dependence_exact(p, compressed[: rank + 1]) + [0] * (len(compressed) - (rank + 1))
        if degree == 3:
            if p % 3 != 2:
                raise ValueError("cubic controller currently requires p=2 mod 3")
            cube_root_exp = pow(3, -1, p - 1)
            coefficients = [pow(c, cube_root_exp, p) for c in coefficients]
        weights = coefficients
    verify_diagonal_witness(p, columns, weights, degree)
    return weights, rank, len(active_keys)


def sparse_translate_combine(
    packets: Sequence[PinnedSymbolicPacket],
    weights: Sequence[int],
    outcomes: Sequence[Sequence[int]],
) -> PinnedSymbolicPacket:
    """Update the sparse symbolic scalar phase after public coordinate-shear measurement."""
    if not packets:
        raise ValueError("nonempty packet sequence required")
    max_deg = max((pkt.degree for pkt in packets), default=0)
    first = _validate_compatible_batch(packets, max(1, max_deg))
    p = first.p
    width = first.width
    if len(packets) != len(weights) or len(packets) != len(outcomes):
        raise ValueError("matching packets, weights, and outcomes required")
    _canonical_vec(weights, len(packets), p)
    if not any(weights):
        raise ValueError("at least one nonzero weight required")
    for y in outcomes:
        _canonical_vec(y, width, p)

    combined: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    for pkt, scale, y in zip(packets, weights, outcomes):
        pkt.consumed = True
        if not scale:
            continue
        for (alpha, params), coeff in pkt.packet.terms.items():
            for beta in product(*(range(a + 1) for a in alpha)):
                if not any(beta):
                    continue
                term_scalar = coeff * pow(scale, sum(beta), p) % p
                for a, b, yj in zip(alpha, beta, y):
                    term_scalar = term_scalar * comb(a, b) * pow(yj, a - b, p) % p
                if term_scalar:
                    key = (tuple(beta), params)
                    new_val = (combined.get(key, 0) + term_scalar) % p
                    if new_val:
                        combined[key] = new_val
                    else:
                        combined.pop(key, None)

    merged_packet = SymbolicScalarPacket(
        p=p,
        quotient_width=first.packet.quotient_width,
        jet_width=first.packet.jet_width,
        parameter_basis=first.packet.parameter_basis,
        terms=combined,
    )
    return PinnedSymbolicPacket(
        instance_id=first.instance_id,
        chart_id=first.chart_id,
        packet=merged_packet,
        consumed=False,
    )


def sparse_degree_erasure_stage(
    packets: Sequence[PinnedSymbolicPacket],
    degree: int,
    outcomes: Sequence[Sequence[int]],
    *,
    rng: random.Random | None = None,
    conic_cap: int = 64,
) -> tuple[PinnedSymbolicPacket, list[int], int, int]:
    """Execute one verified degree-``degree`` cancellation and shear update on sparse packets."""
    weights, rank, active_equations = sparse_cancellation_weights(
        packets,
        degree,
        rng=rng,
        conic_cap=conic_cap,
    )
    merged = sparse_translate_combine(packets, weights, outcomes)
    if merged.degree >= degree:
        raise ArithmeticError("leading degree survived verified sparse cancellation")
    return merged, weights, rank, active_equations


@dataclass(frozen=True)
class PublicLieAlgebra:
    """Public Lazard Lie algebra over GF(p) with arbitrary-precision linear algebra."""

    p: int
    dimension: int
    bracket_fn: Callable[[Sequence[int], Sequence[int]], Sequence[int]]

    def __post_init__(self) -> None:
        ring(self.p)
        if self.dimension < 1:
            raise ValueError("positive ambient Lie dimension required")

    def bracket(self, left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        _canonical_vec(left, self.dimension, self.p)
        _canonical_vec(right, self.dimension, self.p)
        out = self.bracket_fn(left, right)
        _canonical_vec(out, self.dimension, self.p)
        return tuple(int(x) % self.p for x in out)

    def span(self, vectors: Sequence[Sequence[int]]) -> list[tuple[int, ...]]:
        return _fmpz_row_space_basis(vectors, self.dimension, self.p)

    def lower_central_series(self, subspace_basis: Sequence[Sequence[int]]) -> list[list[tuple[int, ...]]]:
        """Compute [gamma_1(S), gamma_2(S), ..., 0] for a Lie subalgebra basis S."""
        base = self.span(subspace_basis)
        series = [base]
        current = base
        for _ in range(len(base) + 1):
            if not current:
                return series
            next_term = self.span([self.bracket(a, b) for a in base for b in current])
            series.append(next_term)
            if not next_term:
                return series
            current = next_term
        raise ValueError("supplied Lie subalgebra is not nilpotent")

    def nilpotency_class(self, subspace_basis: Sequence[Sequence[int]]) -> int:
        """Return the nilpotency class r of S (0 for trivial, 1 for nonzero abelian)."""
        series = self.lower_central_series(subspace_basis)
        return max(0, len(series) - 1)

    def derived_chart(
        self,
        ambient_basis: Sequence[Sequence[int]],
    ) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
        """Return (normal_basis N=[S,S], section_basis V) and verify [N, N] = 0."""
        ambient = self.span(ambient_basis)
        normal = self.span([self.bracket(a, b) for a in ambient for b in ambient])
        for a, b in product(normal, repeat=2):
            if any(self.bracket(a, b)):
                raise ValueError("scalar phase source requires abelian derived ideal")
        adapted = self.span(list(normal) + list(ambient))
        if len(adapted) != len(ambient):
            raise ValueError("ambient basis is not closed under brackets")
        return normal, adapted[len(normal) :]


@dataclass(frozen=True)
class ClassDescentStepResult:
    """Result of one public class-descent evaluation on observed quotient frequencies."""

    level: int
    chart_id: str
    next_chart_id: str
    old_basis: tuple[tuple[int, ...], ...]
    derived_basis: tuple[tuple[int, ...], ...]
    section_basis: tuple[tuple[int, ...], ...]
    image_basis: tuple[tuple[int, ...], ...]
    preimage_basis: tuple[tuple[int, ...], ...]
    old_profile: tuple[int, ...]
    new_profile: tuple[int, ...]
    old_class: int
    new_class: int
    strict_class_drop: bool
    fourier_samples_consumed: int


def certified_class_descent_step(
    algebra: PublicLieAlgebra,
    ambient_basis: Sequence[Sequence[int]],
    fourier_rows: Sequence[Sequence[int]],
    *,
    level: int = 0,
    instance_id: str = "default-instance",
) -> ClassDescentStepResult:
    """Public arithmetic predicate from Section 4 of BOUNDED_CLASS_METABELIAN_HSP.md."""
    ambient = algebra.span(ambient_basis)
    normal, section = algebra.derived_chart(ambient)
    quotient_dim = len(section)
    for row in fourier_rows:
        _canonical_vec(row, quotient_dim, algebra.p)
    image_basis = _fmpz_nullspace_basis(fourier_rows, quotient_dim, algebra.p)
    lifts: list[tuple[int, ...]] = []
    for coeff_vec in image_basis:
        lifted = [
            sum(coeff_vec[j] * section[j][coord] for j in range(quotient_dim)) % algebra.p
            for coord in range(algebra.dimension)
        ]
        lifts.append(tuple(lifted))
    preimage = algebra.span(list(normal) + lifts)
    old_series = algebra.lower_central_series(ambient)
    new_series = algebra.lower_central_series(preimage)
    old_profile = tuple(len(term) for term in old_series)
    new_profile = tuple(len(term) for term in new_series)
    old_class = max(0, len(old_profile) - 1)
    new_class = max(0, len(new_profile) - 1)
    chart_id = f"{instance_id}:level-{level}:dim-{len(ambient)}:class-{old_class}"
    next_chart_id = f"{instance_id}:level-{level + 1}:dim-{len(preimage)}:class-{new_class}"
    return ClassDescentStepResult(
        level=level,
        chart_id=chart_id,
        next_chart_id=next_chart_id,
        old_basis=tuple(ambient),
        derived_basis=tuple(normal),
        section_basis=tuple(section),
        image_basis=tuple(image_basis),
        preimage_basis=tuple(preimage),
        old_profile=old_profile,
        new_profile=new_profile,
        old_class=old_class,
        new_class=new_class,
        strict_class_drop=new_class < old_class,
        fourier_samples_consumed=len(fourier_rows),
    )


def rank_batch_size(width: int, p: int, delta: Fraction = Fraction(1, 16)) -> int:
    """Fixed rank batch size ``width + ceil(log_p(1/delta))`` from Section 3 & 4."""
    ring(p)
    if width < 0:
        raise ValueError("nonnegative width required")
    if delta <= 0 or delta >= 1:
        raise ValueError("error budget delta must lie in (0, 1)")
    extra = max(1, int(ceil(log(float(1 / delta)) / log(float(p)))))
    return width + extra


@dataclass(frozen=True)
class CertifiedClassDescentReport:
    """Complete execution trace of the public certified class-descent controller."""

    status: str
    abort_reason: str | None
    instance_id: str
    initial_class: int
    terminal_class: int
    dimension_trajectory: tuple[int, ...]
    class_trajectory: tuple[int, ...]
    chart_trajectory: tuple[str, ...]
    steps: tuple[ClassDescentStepResult, ...]
    initial_normal_intersection: tuple[tuple[int, ...], ...]
    terminal_transverse_generators: tuple[tuple[int, ...], ...]
    recovered_generators: tuple[tuple[int, ...], ...]
    fourier_samples_by_level: tuple[int, ...]
    terminal_abelian_samples: int
    oracle_membership_queries: int
    ideal_model_certificate_only: bool = True
    unconditional_noisy_certificate: bool = False
    accepted_speedup_candidate: bool = False
    novelty_claim: bool = False
    speedup_claim_allowed: bool = False


def certified_class_descent_controller(
    algebra: PublicLieAlgebra,
    initial_ambient_basis: Sequence[Sequence[int]],
    *,
    quotient_fourier_sampler: Callable[[int, str, Sequence[tuple[int, ...]], Sequence[tuple[int, ...]]], Sequence[int]],
    terminal_abelian_sampler: Callable[[str, Sequence[tuple[int, ...]]], Sequence[int]],
    original_oracle_label: Callable[[tuple[int, ...]], object],
    initial_normal_intersection: Sequence[Sequence[int]] = (),
    instance_id: str = "metabelian-class-descent",
    level_sample_cap: int | None = None,
    terminal_sample_cap: int | None = None,
) -> CertifiedClassDescentReport:
    """Execute the Section 4 certified class-descent control flow."""
    current_basis = algebra.span(initial_ambient_basis)
    initial_class = algebra.nilpotency_class(current_basis)
    zero_vec = (0,) * algebra.dimension
    oracle_queries = 1
    identity_label = original_oracle_label(zero_vec)

    k_basis = algebra.span(initial_normal_intersection)
    for k_vec in k_basis:
        oracle_queries += 1
        if original_oracle_label(k_vec) != identity_label:
            return CertifiedClassDescentReport(
                status="ABORT",
                abort_reason="INITIAL_INTERSECTION_MEMBERSHIP_FAILURE",
                instance_id=instance_id,
                initial_class=initial_class,
                terminal_class=initial_class,
                dimension_trajectory=(len(current_basis),),
                class_trajectory=(initial_class,),
                chart_trajectory=(f"{instance_id}:level-0:dim-{len(current_basis)}:class-{initial_class}",),
                steps=(),
                initial_normal_intersection=tuple(k_basis),
                terminal_transverse_generators=(),
                recovered_generators=(),
                fourier_samples_by_level=(),
                terminal_abelian_samples=0,
                oracle_membership_queries=oracle_queries,
            )

    steps: list[ClassDescentStepResult] = []
    dim_trajectory = [len(current_basis)]
    class_trajectory = [initial_class]
    chart_trajectory = [f"{instance_id}:level-0:dim-{len(current_basis)}:class-{initial_class}"]
    samples_by_level: list[int] = []

    max_levels = max(0, initial_class - 1)
    for level in range(max_levels):
        current_class = algebra.nilpotency_class(current_basis)
        if current_class <= 1:
            break
        normal, section = algebra.derived_chart(current_basis)
        cap = level_sample_cap if level_sample_cap is not None else rank_batch_size(len(section), algebra.p)
        if cap < 1:
            raise ValueError("positive level_sample_cap required")
        chart_id = chart_trajectory[-1]
        rows: list[tuple[int, ...]] = []
        accepted_step: ClassDescentStepResult | None = None
        for _ in range(cap):
            sample = quotient_fourier_sampler(level, chart_id, normal, section)
            _canonical_vec(sample, len(section), algebra.p)
            rows.append(tuple(int(x) % algebra.p for x in sample))
            step = certified_class_descent_step(
                algebra,
                current_basis,
                rows,
                level=level,
                instance_id=instance_id,
            )
            if step.strict_class_drop:
                accepted_step = step
                break
        if accepted_step is None:
            samples_by_level.append(len(rows))
            return CertifiedClassDescentReport(
                status="ABORT",
                abort_reason="DESCENT_CLASS_DROP_FAILURE",
                instance_id=instance_id,
                initial_class=initial_class,
                terminal_class=current_class,
                dimension_trajectory=tuple(dim_trajectory),
                class_trajectory=tuple(class_trajectory),
                chart_trajectory=tuple(chart_trajectory),
                steps=tuple(steps),
                initial_normal_intersection=tuple(k_basis),
                terminal_transverse_generators=(),
                recovered_generators=(),
                fourier_samples_by_level=tuple(samples_by_level),
                terminal_abelian_samples=0,
                oracle_membership_queries=oracle_queries,
            )
        steps.append(accepted_step)
        samples_by_level.append(accepted_step.fourier_samples_consumed)
        current_basis = list(accepted_step.preimage_basis)
        dim_trajectory.append(len(current_basis))
        class_trajectory.append(accepted_step.new_class)
        chart_trajectory.append(accepted_step.next_chart_id)

    terminal_class = algebra.nilpotency_class(current_basis)
    if terminal_class > 1:
        return CertifiedClassDescentReport(
            status="ABORT",
            abort_reason="NONABELIAN_TERMINAL_AMBIENT",
            instance_id=instance_id,
            initial_class=initial_class,
            terminal_class=terminal_class,
            dimension_trajectory=tuple(dim_trajectory),
            class_trajectory=tuple(class_trajectory),
            chart_trajectory=tuple(chart_trajectory),
            steps=tuple(steps),
            initial_normal_intersection=tuple(k_basis),
            terminal_transverse_generators=(),
            recovered_generators=(),
            fourier_samples_by_level=tuple(samples_by_level),
            terminal_abelian_samples=0,
            oracle_membership_queries=oracle_queries,
        )

    terminal_chart = chart_trajectory[-1]
    abelian_dim = len(current_basis)
    if abelian_dim == 0:
        terminal_samples = 0
        transverse_generators: list[tuple[int, ...]] = []
    else:
        t_cap = terminal_sample_cap if terminal_sample_cap is not None else rank_batch_size(abelian_dim, algebra.p)
        if t_cap < 1:
            raise ValueError("positive terminal_sample_cap required")
        t_rows: list[tuple[int, ...]] = []
        for _ in range(t_cap):
            row = terminal_abelian_sampler(terminal_chart, current_basis)
            _canonical_vec(row, abelian_dim, algebra.p)
            t_rows.append(tuple(int(x) % algebra.p for x in row))
        terminal_samples = len(t_rows)
        null_coords = _fmpz_nullspace_basis(t_rows, abelian_dim, algebra.p)
        transverse_generators = [
            tuple(
                sum(coords[j] * current_basis[j][c] for j in range(abelian_dim)) % algebra.p
                for c in range(algebra.dimension)
            )
            for coords in null_coords
        ]

    for gen in transverse_generators:
        oracle_queries += 1
        if original_oracle_label(gen) != identity_label:
            return CertifiedClassDescentReport(
                status="ABORT",
                abort_reason="TERMINAL_ORACLE_MEMBERSHIP_FAILURE",
                instance_id=instance_id,
                initial_class=initial_class,
                terminal_class=terminal_class,
                dimension_trajectory=tuple(dim_trajectory),
                class_trajectory=tuple(class_trajectory),
                chart_trajectory=tuple(chart_trajectory),
                steps=tuple(steps),
                initial_normal_intersection=tuple(k_basis),
                terminal_transverse_generators=tuple(transverse_generators),
                recovered_generators=(),
                fourier_samples_by_level=tuple(samples_by_level),
                terminal_abelian_samples=terminal_samples,
                oracle_membership_queries=oracle_queries,
            )

    recovered = algebra.span(list(k_basis) + transverse_generators)
    return CertifiedClassDescentReport(
        status="SUCCESS",
        abort_reason=None,
        instance_id=instance_id,
        initial_class=initial_class,
        terminal_class=terminal_class,
        dimension_trajectory=tuple(dim_trajectory),
        class_trajectory=tuple(class_trajectory),
        chart_trajectory=tuple(chart_trajectory),
        steps=tuple(steps),
        initial_normal_intersection=tuple(k_basis),
        terminal_transverse_generators=tuple(transverse_generators),
        recovered_generators=tuple(recovered),
        fourier_samples_by_level=tuple(samples_by_level),
        terminal_abelian_samples=terminal_samples,
        oracle_membership_queries=oracle_queries,
    )


def build_symbolic_scalar_phase_erasure_report() -> dict[str, object]:
    """Generate the reproducible audit report for Milestone 15."""
    from tests.test_class_four_matrix_source import forms3, symbolic_transcript
    from tests.test_metabelian_phase_extension import ClassFourFixture, _matrix_coordinates
    from tests.test_ut5_matrix_phase_alignment import batch as ut5_batch
    from theorems.class_four_scalar_phase_compiler import compile_variable_scalar_packet
    from theorems.ut5_matrix_phase_alignment import align_public_jets
    from theorems.ut5_scalar_phase_compiler import compile_scalar_packet

    # 1. Variable-radical sparse cubic cancellation at p=11
    p = 11
    forms = forms3(p) + [[[0] * 3 for _ in range(3)]]
    rng = random.Random(20261021)

    def make_variable_packet(seed_offset: int) -> PinnedSymbolicPacket:
        _, labels, scales, outcomes, alignment, alpha, spectator = symbolic_transcript(p, seed_offset % 3)
        pkt = compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes, alpha, spectator)
        return pin_symbolic_packet(pkt, instance_id="var-rad-p11", chart_id="root-chart")

    var_packets = [make_variable_packet(i) for i in range(4)]
    var_Stage3, var_w3, var_rank3, var_eq3 = sparse_degree_erasure_stage(
        var_packets,
        3,
        outcomes=[[rng.randrange(p) for _ in range(var_packets[0].width)] for _ in var_packets],
        rng=rng,
    )

    # 2. Complete 3 -> 2 -> 1 -> 0 sparse symbolic erasure stages on synthetic lifted SymbolicScalarPackets
    p_tree, q_width, j_width = 11, 2, 1
    width = q_width + j_width
    param_basis = ((0, (1, 0)), (0, (2, 0)), (1, (1, 1)), (2, (3, 0)))

    def random_symbolic_packet(seed: int, max_deg: int = 3) -> PinnedSymbolicPacket:
        local_rng = random.Random(seed)
        terms: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
        active_exponents = [
            alpha
            for alpha in [
                (3, 0, 0),
                (2, 1, 0),
                (1, 1, 1),
                (2, 0, 0),
                (1, 1, 0),
                (1, 0, 1),
                (0, 1, 1),
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
            ]
            if sum(alpha) <= max_deg
        ]
        active_params = [(0,), (1,), (0, 1), (1, 2), (2, 3)]
        for alpha in active_exponents:
            for pair in active_params[:2]:
                val = local_rng.randrange(1, p_tree)
                terms[(alpha, pair)] = val
        return pin_symbolic_packet(
            SymbolicScalarPacket(p_tree, q_width, j_width, param_basis, terms),
            instance_id="tree-p11",
            chart_id="level-0",
        )

    stage_arities = [7, 169, 7]
    cubic_leaves = [random_symbolic_packet(100 + i, max_deg=3) for i in range(stage_arities[0])]
    quad_pkt, w3, r3, eq3 = sparse_degree_erasure_stage(
        cubic_leaves,
        3,
        outcomes=[[rng.randrange(p_tree) for _ in range(width)] for _ in cubic_leaves],
        rng=rng,
    )
    quad_packets = [quad_pkt] + [
        random_symbolic_packet(1000 + i, max_deg=2) for i in range(stage_arities[1] - 1)
    ]
    lin_pkt, w2, r2, eq2 = sparse_degree_erasure_stage(
        quad_packets,
        2,
        outcomes=[[rng.randrange(p_tree) for _ in range(width)] for _ in quad_packets],
        rng=rng,
    )
    lin_packets = [lin_pkt] + [
        random_symbolic_packet(5000 + i, max_deg=1) for i in range(stage_arities[2] - 1)
    ]
    erased_pkt, w1, r1, eq1 = sparse_degree_erasure_stage(
        lin_packets,
        1,
        outcomes=[[rng.randrange(p_tree) for _ in range(width)] for _ in lin_packets],
        rng=rng,
    )

    # 3. UT5 sparse packet density reduction ratio
    ut5_p, ut5_r, ut5_m = 7, 1, 4
    u_labels, u_scales, u_outcomes = ut5_batch(ut5_p, ut5_r, ut5_m, 17)
    u_align = align_public_jets(ut5_p, u_labels, u_scales, u_outcomes)
    u_R, u_D = u_align.maps.carrier_width, u_align.maps.jet_width
    u_pkt = compile_scalar_packet(
        u_align,
        u_labels,
        u_scales,
        u_outcomes,
        [[1, 2, 3] for _ in u_labels],
        [0] * (u_R - u_D),
    )
    u_pinned = pin_symbolic_packet(u_pkt, instance_id="ut5-p7", chart_id="ut5-root")
    _, u_active_cubic = sparse_leading_columns([u_pinned], 3)
    dense_cubic_equations = u_pkt.lifted_parameter_count * comb(u_pkt.width + 3 - 1, 3)

    # 4. Certified Class Descent 4 -> 3 -> 2 -> 1 on ClassFourFixture
    group = ClassFourFixture()
    basis_matrices = [group.x, group.y] + group.normal
    dim = len(basis_matrices)

    def coords_in_fixture(mat) -> tuple[int, ...]:
        res = _matrix_coordinates(mat % group.p, basis_matrices, group.p)
        assert res is not None
        return tuple(int(x) % group.p for x in res)

    def mat_from_coords(vec: Sequence[int]):
        return sum((int(c) * m for c, m in zip(vec, basis_matrices)), group.x * 0) % group.p

    def lie_bracket_fn(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        a = mat_from_coords(left)
        b = mat_from_coords(right)
        return coords_in_fixture(group.bracket(a, b))

    algebra = PublicLieAlgebra(p=group.p, dimension=dim, bracket_fn=lie_bracket_fn)
    std_basis = [tuple(int(i == j) for j in range(dim)) for i in range(dim)]
    hidden_vec = coords_in_fixture(group.hidden)
    quotient_calls: dict[int, int] = {}

    def exact_quotient_sampler(
        level: int,
        chart_id: str,
        normal: Sequence[tuple[int, ...]],
        section: Sequence[tuple[int, ...]],
    ) -> tuple[int, ...]:
        adapted = list(normal) + list(section)
        h_coords = _fmpz_solve_coordinates(adapted, hidden_vec, group.p)
        assert h_coords is not None
        h_image = h_coords[len(normal) :]
        perp_basis = _fmpz_nullspace_basis([h_image], len(section), group.p)
        if not perp_basis:
            return (0,) * len(section)
        idx = quotient_calls.get(level, 0)
        quotient_calls[level] = idx + 1
        return perp_basis[idx % len(perp_basis)]

    terminal_calls = 0

    def exact_terminal_sampler(
        chart_id: str,
        ambient: Sequence[tuple[int, ...]],
    ) -> tuple[int, ...]:
        nonlocal terminal_calls
        h_coords = _fmpz_solve_coordinates(ambient, hidden_vec, group.p)
        assert h_coords is not None
        perp_basis = _fmpz_nullspace_basis([h_coords], len(ambient), group.p)
        if not perp_basis:
            return (0,) * len(ambient)
        idx = terminal_calls
        terminal_calls += 1
        return perp_basis[idx % len(perp_basis)]

    def original_label_fn(vec: tuple[int, ...]) -> tuple[int, ...]:
        mat = mat_from_coords(vec)
        return min(
            tuple(int(x) for x in (group.exp(mat) @ group.exp(t * group.hidden) % group.p).ravel())
            for t in range(group.p)
        )

    descent_report = certified_class_descent_controller(
        algebra,
        std_basis,
        quotient_fourier_sampler=exact_quotient_sampler,
        terminal_abelian_sampler=exact_terminal_sampler,
        original_oracle_label=original_label_fn,
        instance_id="class4-free-metabelian-p7",
    )

    return {
        "schema_version": "symbolic_scalar_phase_erasure_v1",
        "module": "theorems/symbolic_scalar_phase_erasure.py",
        "scope": {
            "sparse_symbolic_packet_adapter": True,
            "pinned_instance_chart_parameter_basis": True,
            "consumed_packet_reuse_rejected": True,
            "arbitrary_precision_row_compression": True,
            "capped_conic_square_solver": True,
            "certified_class_descent_controller": True,
            "coherent_quantum_circuit_compiler": False,
            "oracle_to_erased_fourier_executed": False,
            "diagnostic_samplers_use_hidden_fixture": True,
            "general_prime_sde_backend": False,
            "accepted_speedup_candidate": False,
            "novelty_claim": False,
            "speedup_claim_allowed": False,
        },
        "sparse_erasure_controls": {
            "ut5_r1_m4_p7": {
                "width": u_pkt.width,
                "base_parameter_count": len(u_pkt.parameter_basis),
                "lifted_parameter_count": u_pkt.lifted_parameter_count,
                "dense_cubic_equation_count": dense_cubic_equations,
                "active_sparse_cubic_equation_count": len(u_active_cubic),
                "sparsity_compression_factor": round(dense_cubic_equations / len(u_active_cubic), 2),
            },
            "variable_radical_p11_cubic_cancellation": {
                "initial_degree": 3,
                "merged_degree": var_Stage3.degree,
                "active_cubic_equations": var_eq3,
                "compressed_rank": var_rank3,
                "weights": var_w3,
            },
            "three_stage_symbolic_tree_p11": {
                "stages": [
                    {"degree": 3, "active_equations": eq3, "compressed_rank": r3, "output_degree": quad_pkt.degree},
                    {"degree": 2, "active_equations": eq2, "compressed_rank": r2, "output_degree": lin_pkt.degree},
                    {"degree": 1, "active_equations": eq1, "compressed_rank": r1, "output_degree": erased_pkt.degree},
                ],
                "stage_arities": stage_arities,
                "total_cubic_leaves": stage_arities[0] * stage_arities[1] * stage_arities[2],
                "reference_descriptors_only": True,
                "erased_root_term_count": len(erased_pkt.packet.terms),
                "erased_root_degree": erased_pkt.degree,
                "conic_failure_bound_64": str(conic_failure_bound(p_tree, 64)),
            },
        },
        "certified_class_descent": {
            "status": descent_report.status,
            "instance_id": descent_report.instance_id,
            "initial_class": descent_report.initial_class,
            "terminal_class": descent_report.terminal_class,
            "dimension_trajectory": list(descent_report.dimension_trajectory),
            "class_trajectory": list(descent_report.class_trajectory),
            "chart_trajectory": list(descent_report.chart_trajectory),
            "fourier_samples_by_level": list(descent_report.fourier_samples_by_level),
            "terminal_abelian_samples": descent_report.terminal_abelian_samples,
            "oracle_membership_queries": descent_report.oracle_membership_queries,
            "recovered_generators": [list(g) for g in descent_report.recovered_generators],
            "ideal_model_certificate_only": descent_report.ideal_model_certificate_only,
            "unconditional_noisy_certificate": descent_report.unconditional_noisy_certificate,
        },
    }


def render_markdown(report: dict[str, object]) -> str:
    ut5 = report["sparse_erasure_controls"]["ut5_r1_m4_p7"]
    tree = report["sparse_erasure_controls"]["three_stage_symbolic_tree_p11"]
    descent = report["certified_class_descent"]
    return f"""# Sparse Symbolic-Scalar Phase-Erasure Adapter and Certified Class-Descent Controller

2026-10-21. **Standalone public classical controller and finite reference verification; not a coherent quantum circuit compiler, general-prime SDE backend, novelty claim, or accepted speedup candidate.**

## 1. Summary and Mechanical Gaps Closed

This note documents `theorems/symbolic_scalar_phase_erasure.py` and `tests/test_symbolic_scalar_phase_erasure.py`, closing two bounded mechanical gaps identified in `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Sparse `SymbolicScalarPacket` Adapter to Public Scalar Phase Erasure**:
   - Connects both `ut5_scalar_phase_compiler.compile_scalar_packet` and `class_four_scalar_phase_compiler.compile_variable_scalar_packet` (`SymbolicScalarPacket`) to cubic, quadratic, and linear phase erasure (`sparse_leading_columns`, `verify_diagonal_witness`, `sparse_cancellation_weights`, `sparse_translate_combine`, `sparse_degree_erasure_stage`) without materializing dense `1 + h + h(h+1)/2` lifted parameter tables or calling `evaluate_fixture`.
   - Checks declared provenance (`PinnedSymbolicPacket(instance_id, chart_id, packet, consumed)`), rejecting mismatched instances, charts, parameter bases, repeated wrapper objects within a merge and previously consumed wrappers. These checks cannot establish that the declared physical sources are fresh, independent or from the claimed oracle/chart; that remains a protocol obligation.
   - Uses arbitrary-precision `fmpz_mod_mat` row compression (`independent_columns_exact`) and capped conic square solving (`square_weights_capped`), supporting 127-bit primes ($p = 2^{{127}} - 1$) without machine-word overflow and verifying every diagonal witness against the original uncompressed equation columns.
2. **Standalone Certified Class-Descent Controller**:
   - Implements `PublicLieAlgebra`, `certified_class_descent_step`, and `certified_class_descent_controller` following Section 4 of `research/BOUNDED_CLASS_METABELIAN_HSP.md`.
   - Computes public derived charts $N = [S, S]$ (rejecting nonabelian derived ideals) and exact lower central series via `fmpz_mod_mat` over $\\mathbb{{F}}_p$, accepting a subgroup restriction $\\hat{{T}} = N + \\hat{{U}}$ **if and only if** $\\text{{class}}(\\hat{{T}}) < \\text{{class}}(S)$ (permitting valid strict support overestimates $\\hat{{U}} \\supsetneq U$ while rejecting dimension-only reductions that leave the nilpotency class unchanged).
   - Rotates `chart_id` at every accepted descent level so no phase packets carry across levels, and finishes in the terminal abelian ambient with a fixed abelian Fourier batch, original-oracle membership verification $f(g) = f(1)$ on every basis generator of $\\hat{{R}}$, and inclusion of the verified initial normal intersection $K$.

## 2. Sparse Symbolic Erasure Verification

| Metric | Value |
| :--- | :--- |
| UT5 $(p=7, r=1, m=4)$ packet width $m + D$ | `{ut5["width"]}` |
| Base parameter count $h$ | `{ut5["base_parameter_count"]}` |
| Lifted parameter count $1 + h + h(h+1)/2$ | `{ut5["lifted_parameter_count"]}` |
| Dense cubic equation count $P \\cdot \\binom{{width+2}}{{3}}$ | `{ut5["dense_cubic_equation_count"]}` |
| Active sparse cubic equations | `{ut5["active_sparse_cubic_equation_count"]}` |
| Sparse equation compression ratio | `{ut5["sparsity_compression_factor"]}x` |
| Full $3 \\to 2 \\to 1 \\to 0$ tree leaves ($p=11$) | `{tree["total_cubic_leaves"]}` |
| Erased root degree / remaining nonconstant terms | `{tree["erased_root_degree"]}` / `{tree["erased_root_term_count"]}` |

## 3. Certified Class-Descent Verification (`class4-free-metabelian-p7`)

| Attribute | Value |
| :--- | :--- |
| Status | `{descent["status"]}` |
| Dimension trajectory | `{descent["dimension_trajectory"]}` |
| Nilpotency class trajectory | `{descent["class_trajectory"]}` |
| Chart trajectory | `{descent["chart_trajectory"]}` |
| Quotient Fourier samples per level | `{descent["fourier_samples_by_level"]}` |
| Terminal abelian Fourier samples | `{descent["terminal_abelian_samples"]}` |
| Original-oracle membership queries | `{descent["oracle_membership_queries"]}` |
| Recovered hidden generator basis | `{descent["recovered_generators"]}` |
| Ideal-model certificate only | `{descent["ideal_model_certificate_only"]}` |
| Unconditional noisy certificate | `{descent["unconditional_noisy_certificate"]}` |

## 4. Explicit Scope Boundaries

- `evaluate_fixture` is never called by `sparse_leading_columns`, `sparse_cancellation_weights`, `sparse_translate_combine`, or `certified_class_descent_controller`.
- The report's class-descent samplers use hidden fixture data to supply ideal Fourier rows. The erasure tree processes public polynomial descriptors, not quantum states. Neither is an end-to-end oracle-to-Fourier execution.
- Terminal membership verification certifies completeness only in the exact-source ideal model where $\\hat{{R}} \\supseteq H$; approximate-source underestimates that lose $H$ while still dropping class can return a proper subgroup of $H$. Accordingly, `unconditional_noisy_certificate` is `False`.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown artifacts.")
    args = parser.parse_args()
    report = build_symbolic_scalar_phase_erasure_report()
    if args.write:
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        MD_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"status": report["certified_class_descent"]["status"], "module": report["module"]}, indent=2))


if __name__ == "__main__":
    main()
