"""Exact growing-depth ternary native phase derivatives and visibility gates.

LOCAL DERIVATION / REVIEW PENDING. Public component-function arithmetic is not
an oracle for the unknown phase. No decoder or generic complexity lower bound.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
import json
import math
from pathlib import Path

import numpy as np
from sympy import Matrix

from cyclotomic_fiber_receiver import frequency_matrix
from cyclotomic_rescaling_gate import residue
from dhsp_codomain_instrument import _integer
from ternary_carry_packets import TernaryPacket, compile_packet
from ternary_schur_tensor import NativeCubicTensor, canonical, combine

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_phase_depth.json"


def cyclic_difference(table, direction, modulus):
    _integer(modulus, "positive cyclic modulus")
    if len(table) != 3 or any(type(x) is not int for x in table) or type(direction) is not int or not 0 <= direction < 3:
        raise ValueError("three-entry cyclic table and canonical ternary direction required")
    return tuple((table[(j+direction) % 3]-table[j]) % modulus for j in range(3))


def repeated_identity(order):
    _integer(order, "positive derivative order")
    if order > 512:
        raise ValueError("symbolic derivative ledger capped at512")
    base_order = 1 if order % 2 else 2
    power = (order-base_order)//2
    return {"derivative_order": order, "integer_multiplier": (-3)**power,
            "cyclic_shift_power": power % 3, "remaining_difference_order": base_order,
            "identity": "Delta^3=-3*S*Delta; S^3=I",
            "exact_integer_operator_identity": True}


@dataclass(frozen=True)
class NativePhaseHierarchy:
    packet: TernaryPacket
    local_frequency_tables: tuple
    low_rows: tuple

    @classmethod
    def from_packet(cls, packet):
        if packet.level < 3 or packet.level % 2 == 0 or not packet.retained:
            raise ValueError("nonempty odd-level native kernel packet required")
        q, matrix = frequency_matrix(packet.level)
        tables = tuple(tuple((0, sum(int(matrix[0, j])*y[j] for j in range(2)) % q,
                              sum(int(matrix[1, j])*y[j] for j in range(2)) % q) for y in row)
                       for row in packet.labels)
        rows = tuple(tuple(residue(row[l]) for row in packet.labels) for l in range(packet.secret_dimension))
        r = (packet.level-1)//2
        unit = (-1)**(r+1)
        assert all(table[2] % 3 == 2*table[1] % 3 for row in tables for table in row)
        assert all(tables[i][l][1] % 3 == unit*rows[l][i] % 3 for i in range(packet.consumed) for l in range(packet.secret_dimension))
        return cls(packet, tables, rows)

    @property
    def retained_modulus(self):
        return self.packet.phase_modulus//3

    @property
    def phase_digits(self):
        return (self.packet.level-1)//2

    def physical_direction(self, logical):
        logical = canonical(logical, self.packet.retained)
        base = self.packet.assignment((0,)*self.packet.retained)
        return tuple((a-b) % 3 for a, b in zip(self.packet.assignment(logical), base))

    def derivative(self, base, directions):
        base = canonical(base, self.packet.retained)
        directions = tuple(canonical(v, self.packet.retained) for v in directions)
        if len(directions) > 512:
            raise ValueError("factored derivative order capped at512")
        q, m, n = self.packet.phase_modulus, self.packet.consumed, self.packet.secret_dimension
        physical_base = self.packet.assignment(base)
        zero = self.packet.assignment((0,)*self.packet.retained)
        physical_directions = tuple(self.physical_direction(v) for v in directions)
        values = []
        for l in range(n):
            total = 0
            for i in range(m):
                table = self.local_frequency_tables[i][l]
                if directions:
                    for v in physical_directions:
                        table = cyclic_difference(table, v[i], q)
                    total += table[physical_base[i]]
                else:
                    total += table[physical_base[i]]-table[zero[i]]
            total %= q
            assert total % 3 == 0
            values.append(total//3)
        return tuple(values)

    def top_derivative(self, directions):
        if len(directions) != self.packet.level:
            raise ValueError("exactly L directions required for the native top tensor")
        physical = tuple(self.physical_direction(v) for v in directions)
        coefficient = -3**(self.phase_digits-1)
        return tuple(coefficient*sum(a*math.prod(v[i] for v in physical) for i, a in enumerate(row)) % self.retained_modulus
                     for row in self.low_rows)

    def resources(self, order):
        _integer(order, "derivative order", 0)
        if order > 512:
            raise ValueError("derivative resource ledger capped at512")
        return {"input_native_qutrits": self.packet.consumed, "retained_registers": self.packet.retained,
                "odd_parent_level": self.packet.level, "retained_phase_digits": self.phase_digits,
                "retained_phase_modulus": str(self.retained_modulus),
                "native_additive_degree_upper_bound": self.packet.level,
                "derivative_order": order,
                "local_modular_subtractions": 3*self.packet.consumed*self.packet.secret_dimension*order,
                "local_frequency_entries_stored": 3*self.packet.consumed*self.packet.secret_dimension,
                "derivative_cube_vertices_not_materialized": str(2**order),
                "full_phase_table_not_materialized": str(3**self.packet.retained),
                "unknown_weighted_phase_queries": 0,
                "coherent_unknown_preparation_or_inverse_supplied": False,
                "degree_upper_bound_is_runtime_lower_bound": False}


def degree_visibility(phase_digits, degree):
    _integer(phase_digits, "phase digits")
    _integer(degree, "claimed additive degree", 0)
    if phase_digits > 512 or degree > 512:
        raise ValueError("visibility ledger capped at512 digits and degree512")
    visible = min(phase_digits, (degree+1)//2)
    return {"phase_modulus": str(3**phase_digits), "claimed_additive_degree_upper_bound": degree,
            "maximum_relative_phase_order": str(3**visible),
            "maximum_secret_residue_digits_seen_by_this_whole_flat_phase": visible,
            "secret_alias_step": str(3**visible),
            "all_residual_secret_digits_could_be_retained": visible == phase_digits,
            "minimum_additive_degree_needed_for_full_phase_order": 2*phase_digits-1,
            "conditional_on_degree_bound_proved_for_every_component": True,
            "degree_bound_itself_certified_by_this_ledger": False,
            "retained_junk_coherent_syndromes_other_measurements_excluded": False}


def sharp_degree_control(level):
    packet = compile_packet([[(1, 0)]]*3, level)
    hierarchy = NativePhaseHierarchy.from_packet(packet)
    e1, e2 = (1, 0), (0, 1)
    directions = [e1]*(level-1)+[e2]
    top = hierarchy.derivative((0, 0), directions)
    predicted = hierarchy.top_derivative(directions)
    assert top == predicted == (3**(hierarchy.phase_digits-1),)
    zero = hierarchy.derivative((0, 0), directions+[e1])
    assert zero == (0,)
    return {"native_labels": packet.labels, "level": level, "initial_syndrome": packet.syndrome,
            "logical_base": [0, 0], "logical_derivative_directions": directions,
            "retained_component_derivative": top, "top_weighted_Schur_prediction": predicted,
            "next_derivative_directions": directions+[e1], "next_derivative": zero,
            "exact_additive_degree_of_this_control": level,
            "resources": hierarchy.resources(level+1),
            "deterministic_native_algebra_control_not_IID_source_claim": True}


def cubic_transfer_countercontrol():
    physical_points = tuple(product(range(3), repeat=3))
    labels = [[(x[2], 0)] for x in physical_points]
    physical_columns = tuple(tuple(x[j] for x in physical_points) for j in range(3))
    records = []
    for level in (3, 5):
        packet = compile_packet(labels, level)
        hierarchy = NativePhaseHierarchy.from_packet(packet)
        logical_frame = tuple(tuple(w[i] for i in packet.free) for w in physical_columns)
        directions = [logical_frame[0], logical_frame[0], logical_frame[1], logical_frame[1], logical_frame[2]]
        derivative = hierarchy.derivative((0,)*packet.retained, directions)
        values = [hierarchy.derivative(combine(logical_frame, z, packet.retained), ()) for z in physical_points]
        records.append({"level": level, "retained_modulus": hierarchy.retained_modulus,
                        "physical_frame_columns": physical_columns, "logical_frame_columns": logical_frame,
                        "fifth_derivative": derivative, "restricted_native_residual_table": values,
                        "initial_pivots": packet.pivots, "initial_free_columns": packet.free,
                        "initial_RREF_rows": packet.reduced_rows,
                        "fixed_low_pattern_not_sampled_IID_quantum_source": True})
        if level == 3:
            assert NativeCubicTensor.from_packet(packet).restriction(logical_frame)["classical_quadratic_restriction_admitted"]
            assert derivative == (0,)
        else:
            assert derivative == hierarchy.top_derivative(directions) == (3,)
    return {"native_labels": labels, "physical_point_order": physical_points,
            "low_label_weight_function": "A(x)=x3 on all F3^3 evaluation points",
            "all_kernel_and_cubic_weighted_products_zero": True,
            "weighted_square_square_linear_product_mod3": 2,
            "native_level_controls": records,
            "level3_cubic_admission_transfers_to_level5": False,
            "full_27_input_quantum_instrument_replayed": False,
            "source_cost_or_secret_decoder_supplied": False}


def low_degree_alias_control(phase_digits):
    q = 3**phase_digits
    frequencies = [q//3*j*j % q for j in range(3)]
    low, high = 2, 5
    first, second = (np.array([np.exp(2j*np.pi*(s*f % q)/q)/math.sqrt(3) for f in frequencies]) for s in (low, high))
    assert np.max(abs(first-second)) < 4e-12
    table = tuple(frequencies)
    for _ in range(3):
        table = cyclic_difference(table, 1, q)
    assert table == (0, 0, 0)
    return {"phase_digits": phase_digits, "component_frequency_table": frequencies,
            "secret_pair": [low, high], "secret_alias_step": 3,
            "calibration_phase_amplitudes": [[[float(x.real), float(x.imag)] for x in state] for state in (first, second)],
            "third_derivative_table": table, "pure_output_states_identical": True,
            "whole_phase_constant_degree_only_not_arbitrary_decoder_no_go": True}


def lifted_quadratic_countercontrol():
    q = 9
    table = (0, 1, 4)
    derivatives = [table]
    for _ in range(5):
        derivatives.append(cyclic_difference(derivatives[-1], 1, q))
    assert derivatives[3] == (0, 3, 6) and derivatives[4] == (3, 3, 3) and derivatives[5] == (0, 0, 0)
    _, M = frequency_matrix(4)
    label = (4, 1)
    assert tuple(int(x) % 9 for x in M*Matrix(label)) == table[1:]
    return {"original_even_native_level": 4, "native_ring_label": label,
            "retained_phase_modulus": q, "integer_lift_formula": "j^2 mod9 for ternary j=0,1,2",
            "formal_lifted_polynomial_degree": 2, "actual_additive_phase_degree": 4,
            "all_repeated_cyclic_derivative_tables": derivatives,
            "classical_quadratic_F3_transfer_admitted": False}


def run_controls():
    return {"status": "NATIVE_NONCLASSICAL_PHASE_DEPTH_HIERARCHY_VERIFIED_REVIEW_PENDING",
            "cyclic_operator_identities": [repeated_identity(d) for d in range(1, 21)],
            "sharp_native_odd_level_controls": [sharp_degree_control(L) for L in (3, 5, 7, 9, 13, 19)],
            "cubic_to_fifth_degree_transfer_countercontrol": cubic_transfer_countercontrol(),
            "conditional_degree_visibility_ledgers": [degree_visibility(r, d) for r in (2, 4, 8, 16, 32) for d in (2, 3, 4, 8)],
            "constant_degree_secret_alias_controls": [low_degree_alias_control(r) for r in (2, 4, 8)],
            "formal_quadratic_vs_additive_degree_countercontrol": lifted_quadratic_countercontrol(),
            "claim_gate": {"new_algorithm": False, "candidate_accepted": False,
                "growing_depth_secret_decoder": False, "universal_decoder_lower_bound": False,
                "independent_human_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "growing_native_phase_depth_verified": True, "new_algorithm": False}))


if __name__ == "__main__":
    main()
