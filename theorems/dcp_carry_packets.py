"""Public parity charts and matched carry-packet Bell readout.

LOCAL DERIVATION / REVIEW PENDING. The operational primitives need unknown
input states, not their preparation/inverse. Secret-dependent state vectors
below are explicitly CALIBRATION ONLY. No native-source matcher is supplied.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
import networkx as nx
from sympy import GF
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_carry_packets.json"
STATUS = "LOCAL_DERIVATION_REVIEW_PENDING"


@dataclass(frozen=True)
class CarryPacket:
    labels: tuple[tuple[int, ...], ...]
    modulus: int
    pivots: tuple[int, ...]
    free: tuple[int, ...]
    parity_rows: tuple[int, ...]
    kernel_rows: tuple[int, ...]
    origin: tuple[int, ...]
    syndrome: int

    @property
    def dimension(self):
        return len(self.labels)

    @property
    def input_qubits(self):
        return len(self.labels[0])

    @property
    def retained_qubits(self):
        return len(self.free)

    @property
    def cnots(self):
        return sum(self.kernel_rows[p].bit_count() for p in self.pivots)

    def assignment(self, z: int) -> tuple[int, ...]:
        if not 0 <= z < 1 << self.retained_qubits:
            raise ValueError("logical assignment out of range")
        return tuple(o ^ ((row & z).bit_count() & 1)
                     for o, row in zip(self.origin, self.kernel_rows))

    def residual(self, z: int) -> tuple[int, ...]:
        assignment = self.assignment(z)
        differences = tuple(sum(a * (b - o) for a, b, o in zip(row, assignment, self.origin))
                            for row in self.labels)
        if any(d & 1 for d in differences):
            raise AssertionError("public parity chart failed divisibility")
        return tuple(d // 2 % (self.modulus // 2) for d in differences)

    def logical_z_mask(self, physical_z_mask: int) -> int:
        if not 0 <= physical_z_mask < 1 << self.input_qubits:
            raise ValueError("physical mask out of range")
        out = 0
        for i, row in enumerate(self.kernel_rows):
            if physical_z_mask >> i & 1:
                out ^= row
        return out

    def cnot_schedule(self) -> tuple[tuple[int, int], ...]:
        return tuple((f, p) for p in self.pivots for j, f in enumerate(self.free)
                     if self.kernel_rows[p] >> j & 1)

    def resource_record(self) -> dict:
        return {"input_phase_qubits": self.input_qubits,
                "measured_syndrome_qubits": len(self.pivots),
                "retained_logical_qubits": self.retained_qubits,
                "cnots": self.cnots,
                "syndrome_probability_denominator_decimal": str(1 << len(self.pivots)),
                "all_syndromes_kept": True, "free_postselection": False,
                "output_is_independent_phase_qubits": False,
                "unknown_preparation_or_inverse_available": False,
                "compact_public_evaluator": True,
                "compact_evaluator_prepares_unknown_phase": False}


def compile_packet(labels, modulus: int, syndrome: int = 0) -> CarryPacket:
    if modulus < 4 or modulus & (modulus - 1):
        raise ValueError("modulus must be a power of two >=4")
    labels = tuple(tuple(int(a) % modulus for a in row) for row in labels)
    if not labels or not labels[0] or any(len(row) != len(labels[0]) for row in labels):
        raise ValueError("nonempty rectangular label matrix required")
    n, m = len(labels), len(labels[0])
    matrix = DomainMatrix.from_list_sympy(n, m, [[a & 1 for a in row] for row in labels]).convert_to(GF(2))
    rref, pivots = matrix.rref()
    if not 0 <= syndrome < 1 << len(pivots):
        raise ValueError("syndrome out of range")
    rref = rref.to_Matrix()
    free = tuple(i for i in range(m) if i not in pivots)
    parity_rows = tuple(sum((int(rref[i, j]) & 1) << j for j in range(m))
                        for i in range(len(pivots)))
    origin = [0] * m
    kernel = [0] * m
    for j, f in enumerate(free):
        kernel[f] = 1 << j
    for i, p in enumerate(pivots):
        origin[p] = syndrome >> i & 1
        kernel[p] = sum((int(rref[i, f]) & 1) << j for j, f in enumerate(free))
    return CarryPacket(labels, modulus, tuple(pivots), free, parity_rows,
                       tuple(kernel), tuple(origin), syndrome)


def expanded_carry_coefficients(packet: CarryPacket) -> dict[int, tuple[int, ...]]:
    """Bounded diagnostic expansion; the scalable representation is the chart."""
    k = packet.retained_qubits
    if k > 10:
        raise ValueError("dense polynomial expansion is calibration-only, k<=10")
    modulus = packet.modulus // 2
    coefficients = {}
    for mask in range(1, 1 << k):
        degree = mask.bit_count()
        sums = [sum((1 - 2 * o) * a
                    for a, o, row in zip(component, packet.origin, packet.kernel_rows)
                    if row & mask == mask) for component in packet.labels]
        if degree == 1:
            assert all(s % 2 == 0 for s in sums)
            values = tuple(s // 2 % modulus for s in sums)
        else:
            multiplier = (-1 if degree % 2 == 0 else 1) * (1 << (degree - 2))
            values = tuple(multiplier * s % modulus for s in sums)
        if any(values):
            coefficients[mask] = values
    return coefficients


def quadratic_data(packet: CarryPacket):
    if packet.modulus != 4:
        raise ValueError("quadratic Bell contract requires modulus four")
    k = packet.retained_qubits
    columns = [sum(((row >> j) & 1) << i for i, row in enumerate(packet.kernel_rows))
               for j in range(k)]
    linear = tuple(tuple(packet.residual(1 << j)[l] for j in range(k))
                   for l in range(packet.dimension))
    quadratic = []
    for component in packet.labels:
        parity = sum((a & 1) << i for i, a in enumerate(component))
        quadratic.append(tuple(tuple(0 if j == h else
                                     ((parity & columns[j] & columns[h]).bit_count() & 1)
                                     for h in range(k)) for j in range(k)))
    return linear, tuple(quadratic)


def matched_bell_equations(left: CarryPacket, right: CarryPacket, xor_outcome: int) -> tuple[int, ...]:
    if left.dimension != right.dimension or left.retained_qubits != right.retained_qubits:
        raise ValueError("packet dimension/width mismatch")
    l1, q1 = quadratic_data(left)
    l2, q2 = quadratic_data(right)
    if q1 != q2:
        raise ValueError("quadratic tensors mismatch; deterministic equations are invalid")
    k = left.retained_qubits
    if not 0 <= xor_outcome < 1 << k:
        raise ValueError("Bell xor outcome out of range")
    return tuple(sum((l1[l][j] ^ l2[l][j] ^
                      (sum(q2[l][j][h] for h in range(k) if xor_outcome >> h & 1) & 1)) << l
                     for l in range(left.dimension)) for j in range(k))


def public_common_radical(left: CarryPacket, right: CarryPacket) -> tuple[int, ...]:
    """All Hadamard parities guaranteed deterministic for EVERY secret."""
    if left.dimension != right.dimension or left.retained_qubits != right.retained_qubits:
        raise ValueError("packet dimension/width mismatch")
    _, q1 = quadratic_data(left)
    _, q2 = quadratic_data(right)
    k = left.retained_qubits
    if k == 0:
        return ()
    rows = [[q1[l][j][h] ^ q2[l][j][h] for h in range(k)]
            for l in range(left.dimension) for j in range(k)]
    matrix = DomainMatrix.from_list_sympy(len(rows), k, rows).convert_to(GF(2))
    rref, pivots = matrix.rref()
    rref = rref.to_Matrix()
    return tuple((1 << f) | sum((int(rref[i, f]) & 1) << p for i, p in enumerate(pivots))
                 for f in range(k) if f not in pivots)


def single_packet_conductor_radical(packet: CarryPacket) -> tuple[int, ...]:
    """Fundamental-matroid components compute C^perp intersect Cond(C,C)."""
    if packet.modulus != 4:
        raise ValueError("conductor readout requires modulus four")
    graph = nx.Graph()
    graph.add_nodes_from(range(packet.input_qubits))
    graph.add_edges_from(packet.cnot_schedule())
    physical_parities = [sum((a & 1) << i for i, a in enumerate(row)) for row in packet.labels]
    directions = []
    for component in nx.connected_components(graph):
        indicator = sum(1 << i for i in component)
        if all((indicator & b).bit_count() % 2 == 0 for b in physical_parities):
            logical = sum((1 << j) for j, f in enumerate(packet.free) if f in component)
            reconstructed = sum(((row & logical).bit_count() & 1) << i
                                for i, row in enumerate(packet.kernel_rows))
            assert reconstructed == indicator
            directions.append(logical)
    return tuple(directions)


def single_packet_source_bound(n: int) -> dict:
    """Exact cut union bound for the native IID m=3n binary-label source."""
    if n < 1:
        raise ValueError("dimension must be positive")
    denominator = 1 << (n * n)
    cut_numerator = 0
    # Every disconnected bipartite graph has a proper cut containing the
    # first left vertex. Charge all such cuts; no independence of cuts.
    for a in range(1, n + 1):
        for b in range(n + 1):
            if a == n and b == n:
                continue
            absent_edges = a * (n - b) + (n - a) * b
            cut_numerator += math.comb(n - 1, a - 1) * math.comb(n, b) * (1 << (n * n - absent_edges))
    raw = Fraction(cut_numerator, denominator) + Fraction(3 * n + 2, 1 << n)
    bound = min(Fraction(1), raw)
    def dyadic(value):
        return {"numerator_hex": hex(value.numerator),
                "denominator_binary_exponent": value.denominator.bit_length() - 1}

    return {"dimension": n, "input_qubits": 3 * n,
            "source": "unconditional independent uniform labels over Z_4^n",
            "public_guaranteed_single_packet_equation_probability_upper_bound":
                dyadic(bound),
            "bipartite_cut_bound": dyadic(Fraction(cut_numerator, denominator)),
            "rank_or_zero_or_even_event_bound": dyadic(Fraction(3 * n + 2, 1 << n)),
            "bound_vacuous": raw >= 1,
            "all_kernel_basis_charts_included": True,
            "all_clifford_or_quantum_measurements_excluded": False}


def exhaustive_conductor_controls() -> int:
    checks = 0
    for n, m in ((1, 3), (2, 4)):
        for flat in itertools.product(range(2), repeat=n * m):
            labels = [flat[l * m:(l + 1) * m] for l in range(n)]
            packet = compile_packet(labels, 4)
            directions = single_packet_conductor_radical(packet)
            parity_rows = [sum(a << i for i, a in enumerate(row)) for row in labels]
            code = {0}
            for row in parity_rows:
                code |= {x ^ row for x in code}
            exact = {x for x in range(1 << m)
                     if all((x & row).bit_count() % 2 == 0 and (x & row) in code for row in parity_rows)}
            generated = {0}
            for h in directions:
                physical = sum(((row & h).bit_count() & 1) << i for i, row in enumerate(packet.kernel_rows))
                generated |= {x ^ physical for x in generated}
            assert exact == generated
            zero = compile_packet([[0] * packet.retained_qubits for _ in range(n)], 4) if packet.retained_qubits else None
            if zero is not None:
                assert len(public_common_radical(packet, zero)) == len(directions)
            checks += 1
    return checks


def partial_bell_equation(left: CarryPacket, right: CarryPacket,
                          xor_outcome: int, parity_direction: int) -> int:
    l1, q1 = quadratic_data(left)
    l2, q2 = quadratic_data(right)
    k = left.retained_qubits
    if left.dimension != right.dimension or k != right.retained_qubits:
        raise ValueError("packet dimension/width mismatch")
    if not 0 <= xor_outcome < 1 << k or not 0 <= parity_direction < 1 << k:
        raise ValueError("Bell logical value out of range")
    hbits = [j for j in range(k) if parity_direction >> j & 1]
    coefficients = []
    for l in range(left.dimension):
        if any(sum((q1[l][j][h] ^ q2[l][j][h]) for h in hbits) & 1 for j in range(k)):
            raise ValueError("direction is outside the public common radical")
        coefficient = sum(l1[l][j] ^ l2[l][j] for j in hbits)
        coefficient += sum(q1[l][j][h] ^ q2[l][j][h]
                           for j, h in itertools.combinations(hbits, 2))
        coefficient += sum(q2[l][j][h] for j in hbits for h in range(k) if xor_outcome >> h & 1)
        coefficients.append(coefficient & 1)
    return sum(c << l for l, c in enumerate(coefficients))


def binary_rank(rows, width):
    if not rows:
        return 0
    matrix = DomainMatrix.from_list_sympy(len(rows), width,
        [[row >> j & 1 for j in range(width)] for row in rows]).convert_to(GF(2))
    return len(matrix.rref()[1])


def greedy_common_isotropic(packet: CarryPacket) -> tuple[int, ...]:
    """Polynomial q=4 baseline, not a better-than-known sieve claim."""
    _, forms = quadratic_data(packet)
    k = packet.retained_qubits
    directions = []
    while k:
        rows = [[sum(form[j][h] for h in range(k) if u >> h & 1) & 1 for j in range(k)]
                for form in forms for u in directions]
        if rows:
            rref, pivots = DomainMatrix.from_list_sympy(len(rows), k, rows).convert_to(GF(2)).rref()
            rref = rref.to_Matrix()
            candidates = [(1 << f) | sum((int(rref[i, f]) & 1) << p for i, p in enumerate(pivots))
                          for f in range(k) if f not in pivots]
        else:
            candidates = [1 << j for j in range(k)]
        candidate = next((v for v in candidates if binary_rank(directions + [v], k) > len(directions)), None)
        if candidate is None:
            break
        directions.append(candidate)
    assert len(directions) >= math.ceil(k / (packet.dimension + 1))
    return tuple(directions)


def isotropic_readout_rows(packet: CarryPacket, directions, background: int = 0) -> tuple[int, ...]:
    _, forms = quadratic_data(packet)
    k = packet.retained_qubits
    if not 0 <= background < 1 << k or any(not 0 < u < 1 << k for u in directions):
        raise ValueError("logical chart value out of range")
    if binary_rank(list(directions), k) != len(directions):
        raise ValueError("independent readout directions required")
    for u, v in itertools.combinations(directions, 2):
        if any(sum(form[j][h] for j in range(k) if u >> j & 1
                   for h in range(k) if v >> h & 1) & 1 for form in forms):
            raise ValueError("directions are not common totally isotropic")
    origin = packet.residual(background)
    return tuple(sum((a ^ b) << l for l, (a, b) in
                     enumerate(zip(packet.residual(background ^ u), origin))) for u in directions)


def isotropic_source_controls() -> dict:
    counts = 0
    strata = []
    for low in ([[1, 1, 1]], [[1, 1, 0, 0]], [[1, 0, 1, 1], [0, 1, 1, 0]]):
        n, m = len(low), len(low[0])
        base = compile_packet(low, 4)
        directions = greedy_common_isotropic(base)
        histogram = Counter()
        for high in itertools.product(range(2), repeat=n * m):
            labels = [[low[l][i] + 2 * high[l * m + i] for i in range(m)] for l in range(n)]
            packet = compile_packet(labels, 4)
            rows = isotropic_readout_rows(packet, directions)
            histogram[rows] += 1
            for background in range(1 << packet.retained_qubits):
                equations = isotropic_readout_rows(packet, directions, background)
                for logical in range(1 << len(directions)):
                    z = background
                    for j, u in enumerate(directions):
                        if logical >> j & 1:
                            z ^= u
                    predicted = tuple(packet.residual(background)[l] ^
                                      (sum(row >> l & 1 for j, row in enumerate(equations)
                                           if logical >> j & 1) & 1) for l in range(n))
                    assert predicted == packet.residual(z)
                    counts += 1
        assert len(histogram) == 1 << (n * len(directions))
        assert len(set(histogram.values())) == 1
        strata.append({"dimension": n, "input_qubits": m,
                       "retained_product_phase_qubits": len(directions),
                       "high_label_tables_exhausted": 1 << (n * m),
                       "joint_output_labels_uniform_and_independent": True,
                       "low_labels_fixed_for_identity_control_not_native_hard_family": True})
    return {"affine_phase_identity_checks": counts, "uniform_high_bit_source_strata": strata}


def native_pair_radical_controls(trials: int = 8) -> list[dict]:
    """Unconditional IID labels; public algebra only, no state simulation."""
    rng = random.Random(260934996)
    rows = []
    for n in (2, 4, 8, 16, 32):
        m = 3 * n
        histogram = Counter()
        for _ in range(trials):
            left = compile_packet([[rng.randrange(4) for _ in range(m)] for _ in range(n)], 4)
            right = compile_packet([[rng.randrange(4) for _ in range(m)] for _ in range(n)], 4)
            if left.retained_qubits != right.retained_qubits:
                histogram["width_mismatch"] += 1
            else:
                histogram[str(len(public_common_radical(left, right)))] += 1
        rows.append({"dimension": n, "input_qubits_per_packet": m,
                     "unconditional_iid_pair_count": trials,
                     "common_radical_dimension_histogram": dict(histogram),
                     "chart_selection": "canonical RREF, no alignment search",
                     "source_conditioning_or_success_postselection": False,
                     "finite_controls_are_asymptotic_evidence": False})
    return rows


def calibration_packet_state(packet: CarryPacket, secret, physical_z_mask: int = 0):
    if packet.retained_qubits > 10 or len(secret) != packet.dimension:
        raise ValueError("bounded calibration state/secret dimension required")
    q = packet.modulus // 2
    zmask = packet.logical_z_mask(physical_z_mask)
    return np.array([np.exp(2j * np.pi * sum(s * f for s, f in zip(secret, packet.residual(z))) / q)
                     * (-1 if (z & zmask).bit_count() & 1 else 1)
                     for z in range(1 << packet.retained_qubits)]) / math.sqrt(1 << packet.retained_qubits)


def calibration_physical_chart(packet: CarryPacket, secret):
    """Apply the actual public CNOT permutation to product phase-state amplitudes."""
    m, k = packet.input_qubits, packet.retained_qubits
    if m > 10:
        raise ValueError("dense physical calibration limited to ten input qubits")
    transformed = np.zeros((1 << len(packet.pivots), 1 << k), dtype=complex)
    for x in range(1 << m):
        phase = sum(s * sum(a for i, a in enumerate(row) if x >> i & 1)
                    for s, row in zip(secret, packet.labels))
        output = x
        for control, target in packet.cnot_schedule():
            if output >> control & 1:
                output ^= 1 << target
        y = sum((output >> p & 1) << i for i, p in enumerate(packet.pivots))
        assert y == sum(((row & x).bit_count() & 1) << i for i, row in enumerate(packet.parity_rows))
        z = sum((output >> f & 1) << j for j, f in enumerate(packet.free))
        transformed[y, z] = np.exp(2j * np.pi * phase / packet.modulus) / math.sqrt(1 << m)
    return transformed


def calibration_bell_probabilities(left_state, right_state):
    size = len(left_state)
    if size != len(right_state) or size > 256 or size & (size - 1):
        raise ValueError("equal bounded power-of-two state dimensions required")
    # CNOT left->right, then Hadamards on left. Rows are measured XOR u,
    # columns are measured Hadamard v. No outcome is postselected away.
    probabilities = np.empty((size, size))
    for u in range(size):
        amplitudes = np.array([left_state[z] * right_state[z ^ u] for z in range(size)])
        step = 1
        while step < size:
            for start in range(0, size, 2 * step):
                a = amplitudes[start:start + step].copy()
                b = amplitudes[start + step:start + 2 * step].copy()
                amplitudes[start:start + step] = (a + b) / math.sqrt(2)
                amplitudes[start + step:start + 2 * step] = (a - b) / math.sqrt(2)
            step *= 2
        probabilities[u] = abs(amplitudes)**2
    return probabilities


def run_controls() -> dict:
    counts = {"physical_chart_branches": 0, "polynomial_identity_points": 0,
              "matched_bell_rows": 0, "fault_shift_rows": 0}
    rng = random.Random(20261004)
    for modulus in (4, 8, 16):
        for n, m in ((1, 4), (2, 5), (3, 6)):
            for trial in range(4):
                labels = [[rng.randrange(modulus) for _ in range(m)] for _ in range(n)]
                base = compile_packet(labels, modulus)
                secret = [rng.randrange(modulus) for _ in range(n)]
                physical = calibration_physical_chart(base, secret)
                for y in range(1 << len(base.pivots)):
                    packet = compile_packet(labels, modulus, y)
                    state = calibration_packet_state(packet, secret)
                    branch = physical[y]
                    probability = float(np.vdot(branch, branch).real)
                    assert abs(probability - 2**-len(base.pivots)) < 1e-12
                    assert abs(abs(np.vdot(state, branch / math.sqrt(probability))) - 1) < 1e-12
                    coefficients = expanded_carry_coefficients(packet)
                    assert all(mask.bit_count() <= modulus.bit_length() - 1 for mask in coefficients)
                    for z in range(1 << packet.retained_qubits):
                        predicted = tuple(sum(value[l] for mask, value in coefficients.items() if z & mask == mask)
                                          % (modulus // 2) for l in range(n))
                        assert predicted == packet.residual(z)
                        counts["polynomial_identity_points"] += 1
                    counts["physical_chart_branches"] += 1
    # Matched forms below are CONDITIONAL algebra controls, not freely chosen
    # input labels in an ordinary DCP algorithm.
    low = [[1, 0, 1, 1, 0], [0, 1, 1, 0, 1]]
    a1 = [[b + 2 * rng.randrange(2) for b in row] for row in low]
    a2 = [[b + 2 * rng.randrange(2) for b in row] for row in low]
    p1, p2 = compile_packet(a1, 4, 1), compile_packet(a2, 4, 2)
    k = p1.retained_qubits
    for secret in itertools.product(range(4), repeat=2):
        for e1, e2 in ((0, 0), (1, 0), (2, 4), (3, 7)):
            probs = calibration_bell_probabilities(calibration_packet_state(p1, secret, e1),
                                                   calibration_packet_state(p2, secret, e2))
            noise = p1.logical_z_mask(e1) ^ p2.logical_z_mask(e2)
            s = sum((v & 1) << i for i, v in enumerate(secret))
            for u in range(1 << k):
                equations = matched_bell_equations(p1, p2, u)
                v = sum(((row & s).bit_count() & 1) << j for j, row in enumerate(equations)) ^ noise
                assert abs(probs[u, v] - 2**-k) < 1e-12
                assert abs(probs[u].sum() - probs[u, v]) < 1e-12
                counts["fault_shift_rows" if noise else "matched_bell_rows"] += 1
    carry = compile_packet([[1, 1, 1]], 4)
    product = compile_packet([[1, 1, 0]], 4)
    state = calibration_packet_state(carry, [1]).reshape(2, 2)
    reduced = state @ state.conj().T
    purity = float(np.trace(reduced @ reduced).real)
    assert abs(purity - 0.5) < 1e-12
    blind = calibration_bell_probabilities(calibration_packet_state(carry, [1]),
                                          calibration_packet_state(product, [1]))
    assert np.max(abs(blind - 1 / 16)) < 1e-12
    cubic = expanded_carry_coefficients(compile_packet([[1, 1, 1, 1]], 8))
    assert cubic[7] == (2,)
    conductor_count = exhaustive_conductor_controls()
    return {"status": STATUS, "controls": counts,
            "countercontrols": {"retained_qubits_not_independent": True,
                                "entangled_packet_single_qubit_purity": purity,
                                "mismatched_quadratic_bell_distribution_uniform": True,
                                "modulus_eight_cubic_carry_retained": True},
            "matched_control_resource_record": p1.resource_record(),
            "native_iid_canonical_chart_pair_controls": native_pair_radical_controls(),
            "exhaustive_code_conductor_controls": conductor_count,
            "isotropic_product_readout_controls": isotropic_source_controls(),
            "single_packet_native_source_bounds": [single_packet_source_bound(n) for n in (8, 16, 32, 64, 128)],
            "source_link": {"literature_id": "ARXIV-2609.34996-v1",
                            "url": "https://arxiv.org/html/2609.34996v1",
                            "checked_sections": ["4.2", "4.3"],
                            "imported_claim_scope": "sample-only prime-power sieve; not a standard-LWE attack",
                            "paper_correctness_independently_verified": False},
            "claim_gate": {"native_iid_quadratic_tensor_matcher": False,
                           "matched_test_batches_are_unconditional_source_samples": False,
                           "full_secret_decoder": False, "higher_level_packet_decoder": False,
                           "known_secret_simulation_is_dequantization": False,
                           "unknown_state_preparation_or_inverse_granted": False,
                           "independent_phase_output_claim": False,
                           "noise_free_bell_interface_derived": True,
                           "q4_greedy_product_extractor_derived": True,
                           "constant_fraction_product_yield_proved": False,
                           "growing_modulus_product_extractor_derived": False,
                           "uniform_output_label_proof_requires_low_label_only_selection": True,
                           "general_fault_model_covered": False,
                           "independent_theorem_review": False, "novelty_claim": False,
                           "speedup_claim_allowed": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "controls": report["controls"],
                      "exhaustive_code_conductor_controls": report["exhaustive_code_conductor_controls"],
                      "isotropic_product_readout_controls": report["isotropic_product_readout_controls"],
                      "native_iid_canonical_chart_pair_controls": report["native_iid_canonical_chart_pair_controls"],
                      "speedup_claim_allowed": False}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
