"""Bezout exponent-reduced fixed-degree SDE solver and two-stage weighted-to-ordinary phase-erasure cascade.

This standalone module closes the higher-degree and weighted-erasure controller
gaps documented in ``research/NONLINEAR_JET_HSP_RECEIVER.md`` (Sections 6-10),
``research/CLASS_THREE_MONOMIAL_FULL_JET.md`` (Sections 6-7), and
``research/MECHANICAL_FOLLOW_UP_PLAN.md``:

1. **Bezout Exponent-Reduced Fixed-Degree SDE Solver**:
   - Implements the Section 3 exponent reduction of Ivanyos and Santha (2015):
     given degree ``d >= 1`` and odd prime ``p``, set ``g = gcd(d, p - 1)`` and
     ``u = (d // g)^(-1) mod ((p - 1) // g)`` so that ``(y^u)^d == y^g (mod p)``
     for every ``y in F_p``.
   - When ``g == 1``, solves ``sum_i s_i^d v_i = 0`` in ``r + 1`` columns via
     arbitrary-precision ``fmpz_mod_mat`` row compression and ``s_i = c_i^u mod p``.
   - When ``g == 2`` and ``p == 3 (mod 4)``, solves ``sum_i gamma_i^2 v_i = 0``
     in ``(r + 1)^2`` columns via ``square_weights_capped`` and lifts
     ``s_i = gamma_i^u mod p`` so ``s_i^d == gamma_i^2 (mod p)``.
   - When ``g == 3``, uses the two-level curve contraction in
     ``(r+1)(2r+1)`` columns. In the certified large-field regime, arbitrary
     ``g >= 2`` uses symmetric contraction in ``(r+1)((g-1)r+1)`` columns.
     Odd ``g >= 5`` also has a lower-field exterior fallback. Each witness
     is lifted by the same zero-guarded Bezout exponent.
   - Deterministically verifies ``sum_i s_i^d v_i == 0 (mod p)`` against the
     original uncompressed equation columns before returning.
2. **Provenance-Pinned Weighted Erasure & Two-Stage Cascade**:
   - Wraps ``SymbolicScalarPacket`` and ``TaylorJetChart`` / ``FullTaylorJetChart``
     inside ``PinnedWeightedPacket``, rejecting duplicate wrapper instances,
     mismatched ``(instance_id, chart_id, chart, parameter_basis)``, or
     previously consumed packets (including zero-scale inputs).
   - Executes Stage-1 weighted phase erasure from ``d = e`` down to ``1`` using
     ``weighted_leading_columns`` + ``solve_bezout_sde_weights`` +
     ``pullback_phase`` without calling ``evaluate_fixture``.
   - Enforces the mandatory gate ``weighted_degree == 0`` before transitioning
     via negative ``t``-Fourier readout (``fourier_curve_packet``) to Stage-2
     ordinary polynomial phase erasure across degrees ``D, ..., 1`` (or
     ``D - 1, ..., 1``), reaching degree ``0`` at the final root.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
import json
from math import comb, gcd
from pathlib import Path
import random
from typing import Sequence

from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.cubic_diagonal_solver import cubic_arity, cubic_weights
from theorems.graded_hsp_phase_descent import _canonical, _dependence
from theorems.nil3_guarded_cyclic_dispatch import (
    conic_failure_bound,
    independent_columns_exact,
    square_weights_capped,
)
from theorems.nonlinear_jet_erasure import (
    TaylorJetChart,
    fourier_curve_packet,
    pullback_phase,
    verify_weighted_witness,
    weighted_degree,
    weighted_leading_columns,
)
from theorems.prime_character_opi import ring
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket, _add


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "research" / "reductions" / "weighted_two_erasure_cascade.json"
MD_PATH = ROOT / "research" / "WEIGHTED_TWO_ERASURE_CASCADE.md"


def bezout_reduced_exponent(p: int, degree: int) -> tuple[int, int]:
    """Return ``(g, u)`` where ``g = gcd(degree, p - 1)`` and ``(y^u)^degree == y^g (mod p)``."""
    ring(p)
    if type(degree) is not int or degree < 1:
        raise ValueError("positive integer degree required")
    g = gcd(degree, p - 1)
    modulus = (p - 1) // g
    reduced_deg = degree // g
    u = pow(reduced_deg, -1, modulus) if modulus > 1 else 1
    return g, u


def required_bezout_arity(p: int, degree: int, rank: int) -> int:
    """Column count for implemented reduced-degree regimes; not general SDE."""
    if type(rank) is not int or rank < 0:
        raise ValueError("nonnegative equation rank required")
    g, _ = bezout_reduced_exponent(p, degree)
    if rank == 0:
        return 1
    if g == 1:
        return rank + 1
    if g == 2 and p % 4 == 3:
        return (rank + 1) ** 2
    if g == 3:
        return cubic_arity(rank, construction="two_level_curve")
    from theorems.power_sde import field_threshold, power_arity
    if p >= field_threshold(g):
        return power_arity(rank, g)
    if g % 2:
        from theorems.odd_power_sde import odd_power_arity, validate_family
        validate_family(p, g)
        return odd_power_arity(rank, g)
    raise ValueError(
        f"even reduced exponent {g} is below the certified symmetric field regime"
    )


def verify_general_degree_witness(
    p: int,
    columns: Sequence[Sequence[int]],
    weights: Sequence[int],
    degree: int,
) -> None:
    """Deterministically verify ``sum_i weights[i]^degree * columns[i] == 0 (mod p)`` on original columns."""
    ring(p)
    if type(degree) is not int or degree < 1:
        raise ValueError("positive integer degree required")
    if not columns or not columns[0]:
        raise ValueError("nonempty coefficient columns required")
    if len(weights) != len(columns):
        raise ValueError("witness length must match column count")
    _canonical(weights, len(columns), p)
    if not any(weights):
        raise ArithmeticError("all-zero diagonal cancellation witness rejected")
    row_count = len(columns[0])
    for col in columns:
        _canonical(col, row_count, p)
    powered = [pow(int(w), degree, p) for w in weights]
    for row_idx in range(row_count):
        total = sum(columns[col_idx][row_idx] * powered[col_idx] for col_idx in range(len(columns))) % p
        if total != 0:
            raise ArithmeticError(
                f"public degree-{degree} diagonal cancellation failed at equation row {row_idx}"
            )


def solve_bezout_sde_weights(
    p: int,
    columns: Sequence[Sequence[int]],
    degree: int,
    *,
    rng: random.Random | None = None,
    conic_attempt_cap: int = 128,
    nonresidue_attempt_cap: int = 128,
    curve_attempt_cap: int = 256,
    power_sampler_bits: int = 32,
    bounded_randomness_bits: int | None = None,
) -> tuple[list[int], int, int, int]:
    """Solve ``sum_i s_i^degree * columns[i] == 0 (mod p)`` via Bezout exponent reduction.

    Returns ``(weights, compressed_rank, g, u)`` where ``g = gcd(degree, p - 1)``
    and ``(y^u)^degree == y^g (mod p)``.
    For g=3, capped sampling may abort with probability at most
    3^(-nonresidue_attempt_cap)+(8/9)^curve_attempt_cap under independent
    uniform draws. Backend root runtime is not clocked by these caps.
    Odd g>=5 uses the guarded exterior closure; its sampling bound is
    (1-phi(g)/g)^nonresidue_attempt_cap+(1-1/(2g))^curve_attempt_cap.
    When p>=16*g**(2*g+2), symmetric contraction is preferred for g>=4
    (and g=2,p=1 mod4), with sampling bound
    (1-phi(g)/g)^nonresidue_attempt_cap+(g-1)*2**(-power_sampler_bits).
    Explicit bounded_randomness_bits selects the large-field symmetric
    mode with a whole-run failure bound, including root splitting and bit
    rejection. It replaces the individual sampling caps, and fails closed
    outside that regime. The g=1 case is already deterministic.
    """
    ring(p)
    if type(degree) is not int or degree < 1:
        raise ValueError("positive integer degree required")
    if bounded_randomness_bits is not None and (
            type(bounded_randomness_bits) is not int or bounded_randomness_bits < 1):
        raise ValueError("positive integer bounded_randomness_bits required")
    compressed, rank = independent_columns_exact(columns, p)
    g, u = bezout_reduced_exponent(p, degree)
    if rank == 0:
        weights = [1] + [0] * (len(columns) - 1)
        verify_general_degree_witness(p, columns, weights, degree)
        return weights, 0, g, u

    if bounded_randomness_bits is not None and g >= 2:
        from theorems.power_sde import power_arity, validate_family
        validate_family(p, g)
        needed = power_arity(rank, g)
    else:
        needed = required_bezout_arity(p, degree, rank)
    if len(compressed) < needed:
        raise ValueError(
            f"degree-{degree} solver (g={g}) needs {needed} columns at rank {rank} (got {len(compressed)})"
        )
    if g == 1:
        base_rel = [int(x) % p for x in _dependence(p, compressed[: rank + 1])] + [0] * (
            len(compressed) - (rank + 1)
        )
        weights = [pow(c, u, p) if c else 0 for c in base_rel]
    elif bounded_randomness_bits is not None:
        from theorems.power_sde_budget import budgeted_power_weights
        gamma = budgeted_power_weights(p, g, compressed, failure_bits=bounded_randomness_bits,
                                       bit_source=rng).witness.weights
        weights = [pow(int(c), u, p) if c else 0 for c in gamma]
    elif g == 2 and p % 4 == 3:
        # g == 2 and p == 3 mod 4
        gamma = square_weights_capped(
            p,
            compressed,
            rng if rng is not None else random.SystemRandom(),
            conic_attempt_cap=conic_attempt_cap,
        )
        weights = [pow(int(c), u, p) if c else 0 for c in gamma]
    elif g == 3:
        gamma = cubic_weights(p, compressed, rng=rng,
                              nonresidue_attempt_cap=nonresidue_attempt_cap,
                              construction="two_level_curve",
                              curve_attempt_cap=curve_attempt_cap).weights
        weights = [pow(c, u, p) if c else 0 for c in gamma]
    else:
        from theorems.power_sde import field_threshold, power_weights
        if p >= field_threshold(g):
            gamma = power_weights(p, g, compressed, rng=rng,
                                  generator_attempt_cap=nonresidue_attempt_cap,
                                  sampler_bits=power_sampler_bits).weights
        else:
            from theorems.odd_power_sde import odd_power_weights
            gamma = odd_power_weights(p, g, compressed, rng=rng,
                                      generator_attempt_cap=nonresidue_attempt_cap,
                                      scalar_attempt_cap=curve_attempt_cap).weights
        weights = [pow(c, u, p) if c else 0 for c in gamma]
    verify_general_degree_witness(p, columns, weights, degree)
    return weights, rank, g, u


@dataclass
class PinnedWeightedPacket:
    """Provenance-pinned wrapper around a ``SymbolicScalarPacket`` on a ``TaylorJetChart``."""

    instance_id: str
    chart_id: str
    chart: TaylorJetChart
    packet: SymbolicScalarPacket
    consumed: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.instance_id, str) or not self.instance_id.strip():
            raise ValueError("nonempty instance_id string required")
        if not isinstance(self.chart_id, str) or not self.chart_id.strip():
            raise ValueError("nonempty chart_id string required")
        if not isinstance(self.chart, TaylorJetChart):
            raise TypeError("TaylorJetChart (or FullTaylorJetChart) required")
        if not isinstance(self.packet, SymbolicScalarPacket):
            raise TypeError("SymbolicScalarPacket required")
        # Validate against chart and strip any constant/zero terms
        _ = weighted_degree(self.chart, self.packet)
        cleaned = {
            (tuple(alpha), tuple(params)): int(coeff) % self.chart.p
            for (alpha, params), coeff in self.packet.terms.items()
            if int(coeff) % self.chart.p and any(alpha)
        }
        self.packet = SymbolicScalarPacket(
            self.chart.p,
            self.chart.quotient_width,
            self.chart.jet_width,
            self.packet.parameter_basis,
            cleaned,
        )

    @property
    def p(self) -> int:
        return self.chart.p

    @property
    def weighted_degree(self) -> int:
        return weighted_degree(self.chart, self.packet)

    @property
    def ordinary_degree(self) -> int:
        return self.packet.degree

    @property
    def provenance_key(self) -> tuple[object, ...]:
        return (
            self.instance_id,
            self.chart_id,
            type(self.chart),
            self.chart.p,
            self.chart.quotient_width,
            self.chart.noncentral_width,
            self.chart.degree,
            self.packet.parameter_basis,
        )


def _validate_weighted_batch(
    packets: Sequence[PinnedWeightedPacket],
    stage_degree: int,
) -> PinnedWeightedPacket:
    if not packets:
        raise ValueError("nonempty sequence of PinnedWeightedPacket required")
    first = packets[0]
    if not isinstance(first, PinnedWeightedPacket):
        raise TypeError("PinnedWeightedPacket instances required")
    seen_ids: set[int] = set()
    for pkt in packets:
        if not isinstance(pkt, PinnedWeightedPacket):
            raise TypeError("PinnedWeightedPacket instances required")
        if id(pkt) in seen_ids:
            raise ValueError("distinct PinnedWeightedPacket instances required for each physical input")
        seen_ids.add(id(pkt))
        if pkt.consumed:
            raise ValueError("consumed weighted packet cannot be reused")
        if pkt.provenance_key != first.provenance_key:
            raise ValueError("packets must share pinned instance_id, chart_id, chart, and parameter_basis")
        if pkt.weighted_degree > stage_degree:
            raise ValueError(
                f"packet weighted degree {pkt.weighted_degree} exceeds stage degree {stage_degree}"
            )
    return first


def weighted_cancellation_weights(
    packets: Sequence[PinnedWeightedPacket],
    stage_degree: int,
    *,
    rng: random.Random | None = None,
    conic_attempt_cap: int = 128,
    bounded_randomness_bits: int | None = None,
) -> tuple[list[int], int, int, int]:
    """Compute and verify public weighted-degree cancellation scales before outcomes are measured."""
    first = _validate_weighted_batch(packets, stage_degree)
    raw_packets = [pkt.packet for pkt in packets]
    columns, active_keys = weighted_leading_columns(first.chart, raw_packets, stage_degree)
    weights, rank, g, _ = solve_bezout_sde_weights(
        first.p,
        columns,
        stage_degree,
        rng=rng,
        conic_attempt_cap=conic_attempt_cap,
        bounded_randomness_bits=bounded_randomness_bits,
    )
    verify_weighted_witness(first.chart, raw_packets, weights, stage_degree)
    return weights, rank, len(active_keys), g


def weighted_erasure_stage(
    packets: Sequence[PinnedWeightedPacket],
    stage_degree: int,
    outcomes: Sequence[tuple[Sequence[int], Sequence[int]]],
    *,
    rng: random.Random | None = None,
    conic_attempt_cap: int = 128,
    bounded_randomness_bits: int | None = None,
) -> tuple[PinnedWeightedPacket, list[int], int, int]:
    """Execute one verified weighted degree-``stage_degree`` cancellation and triangular pullback."""
    first = _validate_weighted_batch(packets, stage_degree)
    if len(outcomes) != len(packets):
        raise ValueError("matching outcome count required")
    weights, rank, active_eqs, _ = weighted_cancellation_weights(
        packets,
        stage_degree,
        rng=rng,
        conic_attempt_cap=conic_attempt_cap,
        bounded_randomness_bits=bounded_randomness_bits,
    )
    terms: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    for pkt, s, (y, z) in zip(packets, weights, outcomes):
        pkt.consumed = True
        if not s:
            continue
        pulled = pullback_phase(first.chart, pkt.packet, y, z, s)
        _add(terms, pulled.terms, 1, first.p)
    cleaned = {k: v for k, v in terms.items() if v and any(k[0])}
    merged_raw = SymbolicScalarPacket(
        first.p,
        first.chart.quotient_width,
        first.chart.jet_width,
        first.packet.parameter_basis,
        cleaned,
    )
    merged = PinnedWeightedPacket(
        instance_id=first.instance_id,
        chart_id=first.chart_id,
        chart=first.chart,
        packet=merged_raw,
        consumed=False,
    )
    if merged.weighted_degree >= stage_degree:
        raise ArithmeticError("weighted degree did not strictly decrease")
    return merged, weights, rank, active_eqs


def transition_to_fourier_residual(
    erased_root: PinnedWeightedPacket,
    eta: Sequence[int],
) -> SymbolicScalarPacket:
    """Apply negative t-Fourier readout ``eta.F(q)`` ONLY after weighted phase is completely erased.

    Consumes ``erased_root`` and returns a quotient-only ``SymbolicScalarPacket``
    (``jet_width == 0``) of ordinary degree ``<= D - 1`` (for ``TaylorJetChart``)
    or ``<= D`` (for ``FullTaylorJetChart``).
    """
    if not isinstance(erased_root, PinnedWeightedPacket):
        raise TypeError("PinnedWeightedPacket required")
    if erased_root.consumed:
        raise ValueError("consumed weighted root cannot be measured again")
    if erased_root.weighted_degree > 0:
        raise ValueError("weighted phase must be erased to degree 0 before jet Fourier readout")
    erased_root.consumed = True
    residual = fourier_curve_packet(erased_root.chart, erased_root.packet.parameter_basis, eta)
    cleaned = {k: v for k, v in residual.terms.items() if v and any(k[0])}
    return SymbolicScalarPacket(
        erased_root.p,
        erased_root.chart.quotient_width,
        0,
        erased_root.packet.parameter_basis,
        cleaned,
    )


def ordinary_higher_degree_erasure_stage(
    packets: Sequence[SymbolicScalarPacket],
    stage_degree: int,
    outcomes: Sequence[Sequence[int]],
    *,
    rng: random.Random | None = None,
    conic_attempt_cap: int = 128,
    bounded_randomness_bits: int | None = None,
) -> tuple[SymbolicScalarPacket, list[int], int, int]:
    """Erase leading ordinary degree ``stage_degree >= 1`` (including ``stage_degree >= 4``) via Bezout SDE."""
    if not packets:
        raise ValueError("nonempty packet batch required")
    if type(stage_degree) is not int or stage_degree < 1:
        raise ValueError("positive integer stage_degree required")
    first = packets[0]
    p = first.p
    width = first.width
    if len(outcomes) != len(packets):
        raise ValueError("matching outcome count required")
    seen_ids: set[int] = set()
    for pkt in packets:
        if id(pkt) in seen_ids:
            raise ValueError("distinct SymbolicScalarPacket instances required")
        seen_ids.add(id(pkt))
        if (pkt.p, pkt.quotient_width, pkt.jet_width, pkt.parameter_basis) != (
            first.p,
            first.quotient_width,
            first.jet_width,
            first.parameter_basis,
        ):
            raise ValueError("compatible SymbolicScalarPacket batch required")
        if pkt.degree > stage_degree:
            raise ValueError(f"packet ordinary degree {pkt.degree} exceeds stage degree {stage_degree}")

    active_keys = tuple(
        sorted(
            {
                key
                for pkt in packets
                for key, c in pkt.terms.items()
                if c and sum(key[0]) == stage_degree
            }
        )
    )
    columns = (
        [tuple(pkt.terms.get(key, 0) for key in active_keys) for pkt in packets]
        if active_keys
        else [(0,) for _ in packets]
    )
    weights, rank, _, _ = solve_bezout_sde_weights(
        p,
        columns,
        stage_degree,
        rng=rng,
        conic_attempt_cap=conic_attempt_cap,
        bounded_randomness_bits=bounded_randomness_bits,
    )
    for y in outcomes:
        _canonical(y, width, p)

    combined: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    for pkt, scale, y in zip(packets, weights, outcomes):
        if not scale:
            continue
        for (alpha, params), coeff in pkt.terms.items():
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

    merged = SymbolicScalarPacket(
        p=p,
        quotient_width=first.quotient_width,
        jet_width=first.jet_width,
        parameter_basis=first.parameter_basis,
        terms=combined,
    )
    if merged.degree >= stage_degree:
        raise ArithmeticError("ordinary degree did not strictly decrease")
    return merged, weights, rank, len(active_keys)


def build_weighted_two_erasure_cascade_report() -> dict[str, object]:
    """Build the reproducible verification report for Milestone 17."""
    # Choose p = 23 (23 == 2 mod 3, 3 mod 4, 3 mod 5 -> p - 1 = 22 = 2 * 11,
    # so gcd(d, p - 1) in {1, 2} for all degrees d = 1..10!).
    p = 23
    rng = random.Random(20261021)
    chart = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=1, degree=3)
    # chart has indices for k = 1, 2, 3 (jet_width = 6) and weights (1, k_0, ..., k_5).
    param_basis = tuple((0, (k,)) for k in range(1, 6))

    # Construct synthetic degree-e=5 weighted packets with 1 active equation per weighted degree
    # so each stage d = 5, 4, 3, 2, 1 runs cleanly and fast:
    idx_k2 = next(i for i, (_, k, _) in enumerate(chart.indices) if k == 2)
    idx_k3 = next(i for i, (_, k, _) in enumerate(chart.indices) if k == 3)

    def make_weighted_leaf(seed: int, max_w_deg: int = 5) -> PinnedWeightedPacket:
        local_rng = random.Random(seed)
        width = chart.width
        terms: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
        # Pure q-monomials of weight 1..max_w_deg plus jet-coupled terms of weight <= max_w_deg
        for deg in range(1, max_w_deg + 1):
            exp = [0] * width
            exp[0] = deg
            terms[(tuple(exp), (0, 1))] = local_rng.randrange(1, p)
        if max_w_deg >= 5:
            # Weight 5 term: q^2 * t_(k=3)
            exp5 = [0] * width
            exp5[0] = 2
            exp5[1 + idx_k3] = 1
            terms[(tuple(exp5), (0,))] = local_rng.randrange(1, p)
        if max_w_deg >= 4:
            # Weight 4 term: q^2 * t_(k=2)
            exp4 = [0] * width
            exp4[0] = 2
            exp4[1 + idx_k2] = 1
            terms[(tuple(exp4), (1,))] = local_rng.randrange(1, p)
        pkt = SymbolicScalarPacket(p, chart.quotient_width, chart.jet_width, param_basis, terms)
        return PinnedWeightedPacket("cascade-p23", "full-jet-d3", chart, pkt)

    # Run Stage-1 weighted erasure stages d = 5 -> 4 -> 3 -> 2 -> 1 -> 0
    stage1_log: list[dict[str, object]] = []
    # At d=5, active equations <= 2, g = gcd(5, 22) = 1 -> arity <= 3
    batch5 = [make_weighted_leaf(100 + i, max_w_deg=5) for i in range(3)]
    outcomes5 = [
        ([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)])
        for _ in batch5
    ]
    pkt4, w5, r5, eq5 = weighted_erasure_stage(batch5, 5, outcomes5, rng=rng)
    stage1_log.append({"weighted_degree": 5, "gcd_p_minus_1": gcd(5, p - 1), "active_equations": eq5, "rank": r5, "output_weighted_degree": pkt4.weighted_degree})

    # Stage d=4: g = gcd(4, 22) = 2 -> square solver! Prepare fresh weight-4 packets with 2 active equations (rank <= 2, arity 9)
    batch4 = [pkt4] + [make_weighted_leaf(200 + i, max_w_deg=4) for i in range(24)]
    outcomes4 = [
        ([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)])
        for _ in batch4
    ]
    pkt3, w4, r4, eq4 = weighted_erasure_stage(batch4, 4, outcomes4, rng=rng)
    stage1_log.append({"weighted_degree": 4, "gcd_p_minus_1": gcd(4, p - 1), "active_equations": eq4, "rank": r4, "output_weighted_degree": pkt3.weighted_degree})

    # Stage d=3: g = gcd(3, 22) = 1
    batch3 = [make_weighted_leaf(300 + i, max_w_deg=3) for i in range(3)]
    outcomes3 = [
        ([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)])
        for _ in batch3
    ]
    pkt2, w3, r3, eq3 = weighted_erasure_stage(batch3, 3, outcomes3, rng=rng)
    stage1_log.append({"weighted_degree": 3, "gcd_p_minus_1": gcd(3, p - 1), "active_equations": eq3, "rank": r3, "output_weighted_degree": pkt2.weighted_degree})

    # Stage d=2: g = gcd(2, 22) = 2
    batch2 = [make_weighted_leaf(400 + i, max_w_deg=2) for i in range(4)]
    outcomes2 = [
        ([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)])
        for _ in batch2
    ]
    pkt1, w2, r2, eq2 = weighted_erasure_stage(batch2, 2, outcomes2, rng=rng)
    stage1_log.append({"weighted_degree": 2, "gcd_p_minus_1": gcd(2, p - 1), "active_equations": eq2, "rank": r2, "output_weighted_degree": pkt1.weighted_degree})

    # Stage d=1: g = gcd(1, 22) = 1
    batch1 = [make_weighted_leaf(500 + i, max_w_deg=1) for i in range(2)]
    outcomes1 = [
        ([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)])
        for _ in batch1
    ]
    erased_weighted_root, w1, r1, eq1 = weighted_erasure_stage(batch1, 1, outcomes1, rng=rng)
    stage1_log.append({"weighted_degree": 1, "gcd_p_minus_1": gcd(1, p - 1), "active_equations": eq1, "rank": r1, "output_weighted_degree": erased_weighted_root.weighted_degree})

    # Transition via negative t-Fourier readout for several independent roots with k=D=3 active in eta
    stage2_roots: list[SymbolicScalarPacket] = []
    for r_idx in range(4):
        b1 = [make_weighted_leaf(600 + 10 * r_idx + i, max_w_deg=1) for i in range(2)]
        o1 = [([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)]) for _ in b1]
        root_i, _, _, _ = weighted_erasure_stage(b1, 1, o1, rng=rng)
        eta_i = [(r_idx + j + 1) % p for j in range(chart.jet_width)]
        res_i = transition_to_fourier_residual(root_i, eta_i)
        stage2_roots.append(res_i)

    # Stage-2 ordinary erasure starts at degree D = 3 (for FullTaylorJetChart!)
    ord2_pkt, ow3, or3, oeq3 = ordinary_higher_degree_erasure_stage(
        stage2_roots,
        3,
        outcomes=[[rng.randrange(p)] for _ in stage2_roots],
        rng=rng,
    )

    # Also verify 127-bit prime (p = 2^127 - 1) degree-4 and degree-5 Bezout SDE cancellation!
    p127 = (1 << 127) - 1
    cols_d4 = [[(i + 1) * (j + 2) % p127 for j in range(2)] for i in range(9)]
    w_d4, rank_d4, g_d4, u_d4 = solve_bezout_sde_weights(p127, cols_d4, 4, rng=rng)
    cols_d5 = [[(i + 1) * (j + 3) % p127 for j in range(2)] for i in range(3)]
    w_d5, rank_d5, g_d5, u_d5 = solve_bezout_sde_weights(p127, cols_d5, 5, rng=rng)

    return {
        "schema_version": "weighted_two_erasure_cascade_v1",
        "module": "theorems/weighted_two_erasure_cascade.py",
        "scope": {
            "bezout_exponent_reduced_sde_solver": True,
            "higher_degree_d_ge_4_supported": True,
            "provenance_pinned_weighted_packets": True,
            "premature_fourier_readout_rejected": True,
            "two_stage_weighted_to_ordinary_cascade": True,
            "arbitrary_precision_127bit_prime_verified": True,
            "coherent_quantum_circuit_compiler": False,
            "supported_reduced_exponents": [1, 2, 3,
                "g>=4 with p>=16*g**(2*g+2)", "odd g>=5 with p>=4*((g-1)*(g-2))**2"],
            "quadratic_regimes": "p=3 mod4, or p>=1024 via symmetric contraction",
            "cubic_three_coset_collision": True,
            "cubic_two_level_curve_contraction": True,
            "cubic_arity": "(r+1)(2r+1)",
            "large_field_odd_exterior_sde": True,
            "large_field_symmetric_power_sde": True,
            "bounded_randomness_mode_available": True,
            "all_default_randomized_loops_capped": False,
            "general_coset_collision_sde_for_g_gt_3": False,
            "accepted_speedup_candidate": False,
            "novelty_claim": False,
            "speedup_claim_allowed": False,
        },
        "stage1_weighted_erasure_p23": stage1_log,
        "fourier_transition_and_stage2_ordinary_p23": {
            "chart_degree_D": chart.degree,
            "residual_initial_ordinary_degree": max(pkt.degree for pkt in stage2_roots),
            "stage_D_active_equations": oeq3,
            "stage_D_compressed_rank": or3,
            "after_stage_D_ordinary_degree": ord2_pkt.degree,
        },
        "large_prime_127bit_higher_degree_controls": {
            "prime_bits": p127.bit_length(),
            "degree_4": {
                "gcd_p_minus_1": g_d4,
                "compressed_rank": rank_d4,
                "columns_used": len(cols_d4),
                "verified_nonzero_witness": any(w_d4),
            },
            "degree_5": {
                "gcd_p_minus_1": g_d5,
                "compressed_rank": rank_d5,
                "columns_used": len(cols_d5),
                "verified_nonzero_witness": any(w_d5),
            },
            "conic_failure_bound_64": str(conic_failure_bound(p127, 64)),
        },
    }


def render_markdown(report: dict[str, object]) -> str:
    s1 = report["stage1_weighted_erasure_p23"]
    s2 = report["fourier_transition_and_stage2_ordinary_p23"]
    lp = report["large_prime_127bit_higher_degree_controls"]
    rows = "\n".join(
        f"| `{row['weighted_degree']}` | `{row['gcd_p_minus_1']}` | `{row['active_equations']}` | `{row['rank']}` | `{row['output_weighted_degree']}` |"
        for row in s1
    )
    return f"""# Bezout Exponent-Reduced Higher-Degree SDE Solver and Two-Stage Weighted-to-Ordinary Phase-Erasure Cascade

2026-10-28 update. **Public classical controller and exact reference controls;
not a coherent quantum compiler, all-prime SDE backend, novelty claim, or
accepted speedup candidate.**

Reduced degree3 uses [two-level cubic contraction](CUBIC_TWO_LEVEL_CONTRACTION.md).
For any reduced g>=2, [symmetric contraction](POWER_SDE_SYMMETRIC_CONTRACTION.md)
provides `(r+1)*((g-1)*r+1)` columns when `p>=16*g**(2*g+2)`.
It is selected for g>=4 and g=2,p=1 mod4; existing cubic and p=3 mod4
quadratic backends retain their broader regimes. Odd g>=5 also has the
[exterior fallback](ODD_POWER_EXTERIOR_SDE.md) when
`p>=4*((g-1)*(g-2))**2`. Other nonzero-rank regimes fail closed.
Sampling bounds require uniform draws; FLINT root runtime is not clocked.
Explicit `bounded_randomness_bits` opts into a whole-run large-field budget
including root splitting and bit rejection; other nontrivial regimes reject
that option. See [the budget proof](POWER_SDE_RANDOMNESS_BUDGET.md).

## 1. Summary and Mechanical Gaps Closed

This note documents `theorems/weighted_two_erasure_cascade.py` and `tests/test_weighted_two_erasure_cascade.py`, closing the higher-degree and two-stage weighted-to-ordinary phase-erasure controller gaps identified in `research/NONLINEAR_JET_HSP_RECEIVER.md` (Sections 6–10), `research/CLASS_THREE_MONOMIAL_FULL_JET.md` (Sections 6–7), and `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Bezout Exponent-Reduced Fixed-Degree SDE Solver (`bezout_reduced_exponent`, `solve_bezout_sde_weights`, `verify_general_degree_witness`)**:
   - Implements the Section 3 exponent reduction of [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016): for any degree $d \\ge 1$ and odd prime $p$, sets $g = \\gcd(d, p - 1)$ and $u = (d / g)^{{-1}} \\bmod ((p - 1) / g)$ so $(y^u)^d \\equiv y^g \\pmod p$ for all $y \\in \\mathbb{{F}}_p$.
   - Solves $\\sum_i s_i^d v_i \\equiv 0 \\pmod p$ in $r + 1$ columns when $g = 1$ and in $(r + 1)^2$ columns via `square_weights_capped` when $g = 2$ and $p \\equiv 3 \\pmod 4$, deterministically verifying the witness on the original uncompressed columns (`verify_general_degree_witness`).
   - Supports higher original degrees only when their reduced exponent and field regime are covered. New controls include genuine reduced degrees4 and5, Bezout lifts, and weighted unknown-phase erasure. The large-prime controls in this report below still reduce to g=1 or2; the separate power-SDE reports exercise the new regimes.
2. **Provenance-Pinned Weighted Erasure & Two-Stage Cascade (`PinnedWeightedPacket`, `weighted_erasure_stage`, `transition_to_fourier_residual`, `ordinary_higher_degree_erasure_stage`)**:
   - Enforces distinct wrapper instances, pinned `(instance_id, chart_id, chart, parameter_basis)`, and single-use consumption across all weighted merges.
   - Enforces `weighted_degree == 0` before allowing negative $t$-Fourier readout (`transition_to_fourier_residual`), and executes Stage-2 ordinary degree erasure from $D$ down to $0$.

## 2. Stage-1 Weighted Erasure Cascade ($p = 23$, `FullTaylorJetChart` $D = 3$)

| Stage Weighted Degree $d$ | $g = \\gcd(d, p-1)$ | Active Equations | Compressed Rank $r$ | Output Weighted Degree |
| :--- | :--- | :--- | :--- | :--- |
{rows}

## 3. Negative $t$-Fourier Transition, Stage-2 Ordinary Erasure & 127-Bit Prime Controls

| Verification Control | Result |
| :--- | :--- |
| Full-jet residual initial ordinary degree ($D = {s2["chart_degree_D"]}$) | `{s2["residual_initial_ordinary_degree"]}` |
| Stage-$D$ ordinary erasure active equations / rank | `{s2["stage_D_active_equations"]}` / `{s2["stage_D_compressed_rank"]}` |
| Ordinary degree after Stage-$D$ erasure | `{s2["after_stage_D_ordinary_degree"]}` |
| 127-bit prime ($p = 2^{{127}} - 1$) degree-4 SDE ($g={lp["degree_4"]["gcd_p_minus_1"]}$) | Verified (`rank = {lp["degree_4"]["compressed_rank"]}`, `{lp["degree_4"]["columns_used"]}` cols) |
| 127-bit prime ($p = 2^{{127}} - 1$) degree-5 SDE ($g={lp["degree_5"]["gcd_p_minus_1"]}$) | Verified (`rank = {lp["degree_5"]["compressed_rank"]}`, `{lp["degree_5"]["columns_used"]}` cols) |

## 4. Explicit Scope Boundaries

- `evaluate_fixture` is never called by any solver or cascade function.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown artifacts.")
    args = parser.parse_args()
    report = build_weighted_two_erasure_cascade_report()
    if args.write:
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        MD_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"module": report["module"], "schema_version": report["schema_version"]}, indent=2))


if __name__ == "__main__":
    main()
