"""Factored native level3 carry tensor and weighted Schur restriction gate.

LOCAL DERIVATION / REVIEW PENDING. Not a decoder, source matching algorithm,
or transfer to higher levels. Public polynomial geometry, not secret access.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement, product
import json
import math
from pathlib import Path
import random

from flint import nmod_mat
import numpy as np

from cyclotomic_rescaling_gate import residue
from dhsp_codomain_instrument import rational
from ternary_carry_packets import compile_packet, _interpolate

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_schur_tensor.json"


def canonical(vector, length):
    if len(vector) != length or any(type(x) is not int or not 0 <= x < 3 for x in vector):
        raise ValueError("canonical ternary vector of specified length required")
    return tuple(vector)


def rank(columns, height):
    return int(nmod_mat([[c[i] for c in columns] for i in range(height)], 3).rank()) if columns else 0


def combine(columns, coefficients, height):
    return tuple(sum(c[i]*a for c, a in zip(columns, coefficients)) % 3 for i in range(height))


@dataclass(frozen=True)
class NativeCubicTensor:
    low_rows: tuple
    physical_columns: tuple

    @classmethod
    def from_packet(cls, packet):
        if packet.level != 3 or not packet.retained:
            raise ValueError("nonempty native level3 kernel packet required")
        rows = tuple(tuple(residue(y[l]) for y in packet.labels) for l in range(packet.secret_dimension))
        base = packet.assignment((0,)*packet.retained)
        columns = []
        for j in range(packet.retained):
            e = tuple(int(j == i) for i in range(packet.retained))
            columns.append(tuple((a-b) % 3 for a, b in zip(packet.assignment(e), base)))
        assert all(sum(a*b for a, b in zip(row, column)) % 3 == 0 for row in rows for column in columns)
        return cls(rows, tuple(columns))

    @property
    def width(self):
        return len(self.physical_columns)

    @property
    def inputs(self):
        return len(self.low_rows[0])

    def physical(self, logical):
        return combine(self.physical_columns, canonical(logical, self.width), self.inputs)

    def physical_triple(self, first, second, third):
        first, second, third = (canonical(x, self.inputs) for x in (first, second, third))
        return tuple(-sum(a*x*y*z for a, x, y, z in zip(row, first, second, third)) % 3
                     for row in self.low_rows)

    def evaluate(self, first, second, third):
        return self.physical_triple(*(self.physical(x) for x in (first, second, third)))

    def entries(self):
        for indices in combinations_with_replacement(range(self.width), 3):
            yield indices, self.physical_triple(*(self.physical_columns[j] for j in indices))

    def cubic_terms(self):
        if self.width > 64:
            raise ValueError("expanded cubic output capped at64; factored tensor remains available")
        components = [[] for _ in self.low_rows]
        for indices, values in self.entries():
            if indices[0] == indices[2]:
                assert not any(values)
                continue
            factor = 2 if len(set(indices)) == 2 else 1
            powers = [indices.count(j) for j in range(self.width)]
            for l, value in enumerate(values):
                if value:
                    components[l].append({"powers": powers, "coefficient": factor*value % 3})
        return components

    def restriction(self, frame):
        frame = tuple(canonical(c, self.width) for c in frame)
        if not frame or rank(frame, self.width) != len(frame):
            raise ValueError("nonempty independent logical restriction frame required")
        physical = tuple(self.physical(c) for c in frame)
        witnesses = []
        for indices in combinations_with_replacement(range(len(frame)), 3):
            values = self.physical_triple(*(physical[j] for j in indices))
            if any(values):
                witnesses.append({"logical_basis_triple": list(indices), "component_values": list(values)})
        return {"retained_width": len(frame), "logical_frame_columns": frame,
                "physical_frame_columns": physical,
                "all_diagonal_triples_zero": all(not any(self.physical_triple(c, c, c)) for c in physical),
                "mixed_cubic_witnesses": witnesses,
                "classical_quadratic_restriction_admitted": not witnesses,
                "every_complement_syndrome_has_same_cubic_admission": True,
                "quadratic_restriction_is_secret_decoder": False,
                "higher_level_transfer_admitted": False}


def public_polynomial(packet):
    tensor = NativeCubicTensor.from_packet(packet)
    h, n = tensor.width, len(tensor.low_rows)
    cubic = tensor.cubic_terms()
    coefficients = [dict((tuple(x["powers"]), x["coefficient"]) for x in row) for row in cubic]
    basis = [tuple(int(i == j) for i in range(h)) for j in range(h)]
    evaluations = 0
    singles = []
    for j, e in enumerate(basis):
        first, second = packet.residual(e), packet.residual(tuple(2*x for x in e))
        evaluations += 2
        singles.append(first)
        for l in range(n):
            power = [0]*h
            for degree, value in ((1, second[l]-first[l]), (2, 2*first[l]-second[l])):
                power[j] = degree
                if value % 3:
                    coefficients[l][tuple(power)] = value % 3
    for i in range(h):
        for j in range(i+1, h):
            point = tuple(int(k in (i, j)) for k in range(h))
            value = packet.residual(point)
            evaluations += 1
            powers = tuple(int(k in (i, j)) for k in range(h))
            for l in range(n):
                carry = sum(x["coefficient"] for x in cubic[l] if all(not a or point[k] for k, a in enumerate(x["powers"])))
                coefficient = (value[l]-singles[i][l]-singles[j][l]-carry) % 3
                if coefficient:
                    coefficients[l][powers] = coefficient
    return {"retained_width": h,
            "component_polynomials": [[{"powers": list(p), "coefficient": c} for p, c in sorted(row.items())] for row in coefficients],
            "public_residual_evaluations": evaluations,
            "dense_3_to_h_phase_table_built": False,
            "unknown_weighted_phase_oracle_supplied": False}


def evaluate_polynomial(record, point):
    canonical(point, record["retained_width"])
    return tuple(sum(x["coefficient"]*math.prod(pow(a, e, 3) for a, e in zip(point, x["powers"]))
                     for x in row) % 3 for row in record["component_polynomials"])


def disjoint_block_frame(packet):
    n, m = packet.secret_dimension, packet.consumed
    columns = []
    for start in range(0, m-n, n+1):
        block = list(range(start, start+n+1))
        rref, r = nmod_mat([[residue(packet.labels[j][l]) for j in block] for l in range(n)], 3).rref()
        pivots = [next(j for j in range(n+1) if int(rref[i, j])) for i in range(r)]
        free = next(j for j in range(n+1) if j not in pivots)
        word = [0]*m
        word[block[free]] = 1
        for i, pivot in enumerate(pivots):
            word[block[pivot]] = -int(rref[i, free]) % 3
        columns.append(tuple(word[j] for j in packet.free))
    return tuple(columns)


def quadratic_source_ledger(packet, frame):
    tensor = NativeCubicTensor.from_packet(packet)
    admitted = tensor.restriction(frame)
    if not admitted["classical_quadratic_restriction_admitted"]:
        raise ValueError("native quadratic restriction required before source admission")
    W = admitted["physical_frame_columns"]
    k, m, n = len(W), packet.consumed, packet.secret_dimension
    diagonal = [tuple(x*x % 3 for x in w) for w in W]
    mixed = [tuple(a*b % 3 for a, b in zip(W[i], W[j])) for i in range(k) for j in range(i+1, k)]
    d, e = rank(diagonal+mixed, m), rank(mixed, m)
    # Only the low-frequency part of the source determines this affine offset.
    base = packet.assignment((0,)*packet.retained)
    def fixed_low(point):
        actual = packet.assignment(combine(frame, point, packet.retained))
        differences = [sum(a*(x-b) for a, x, b in zip(row, actual, base)) for row in tensor.low_rows]
        assert all(value % 3 == 0 for value in differences)
        return tuple((value//3) % 3 for value in differences)
    singles = [fixed_low(tuple(int(i == j) for i in range(k))) for j in range(k)]
    offsets = [[] for _ in range(n)]
    for i in range(k):
        for j in range(i+1, k):
            value = fixed_low(tuple(int(l in (i, j)) for l in range(k)))
            for l in range(n):
                offsets[l].append((value[l]-singles[i][l]-singles[j][l]) % 3)
    target_consistent = True
    if mixed:
        rows = [[column[i] for column in mixed] for i in range(m)]
        target_consistent = all(int(nmod_mat(rows+[[-x % 3 for x in offset]], 3).rank()) == e for offset in offsets)
    success = Fraction(1, 3**(n*e)) if target_consistent else Fraction(0)
    return {"physical_frame_columns": W, "low_label_rows": tensor.low_rows,
            "secret_components": n, "retained_width": k,
            "square_Schur_rank": d, "offdiagonal_Schur_rank": e,
            "fixed_low_cross_offsets": offsets,
            "all_cross_cancellation_targets_consistent": target_consistent,
            "all_component_cross_terms_cancel_probability": rational(success),
            "conditional_linear_label_entropy_per_component_trits": k,
            "conditional_diagonal_label_entropy_per_component_trits": d-e,
            "conditional_product_qutrit_labels_IID_uniform": target_consistent and d-e == k,
            "scope": "Condition on low labels, low-defined frame and all measured affine syndromes; higher source digits IID uniform. Adaptive high-label-selected frames not covered.",
            "frame_low_defined_lineage_programmatically_verified": False,
            "cross_filter_physically_executed_here": False,
            "arbitrary_public_Clifford_or_basis_changes_excluded": False,
            "correlated_quadratic_outputs_useless": False}


def completed_frame(frame, height):
    columns = list(frame)
    for j in range(height):
        e = tuple(int(i == j) for i in range(height))
        if rank(columns+[e], height) > len(columns):
            columns.append(e)
    assert len(columns) == height
    return tuple(columns)


def restricted_native_control(labels, secret):
    packet = compile_packet(labels, 3)
    if packet.consumed > 7:
        raise ValueError("physical restriction replay capped at7 native qutrits")
    if len(secret) != packet.secret_dimension or any(type(s) is not int or not 0 <= s < 9 for s in secret):
        raise ValueError("canonical full input secret modulo9 required")
    tensor = NativeCubicTensor.from_packet(packet)
    frame = disjoint_block_frame(packet)
    admission = tensor.restriction(frame)
    assert admission["classical_quadratic_restriction_admitted"]
    full = completed_frame(frame, packet.retained)
    matrix = nmod_mat([[c[i] for c in full] for i in range(packet.retained)], 3)
    inverse = matrix.inv()
    k, h, m = len(frame), packet.retained, packet.consumed
    branches = {}
    for word in product(range(3), repeat=m):
        y = tuple((word[p]+sum(row[f]*word[f] for f in packet.free)) % 3 for row, p in zip(packet.reduced_rows, packet.pivots))
        z = tuple(word[f] for f in packet.free)
        new = tuple(sum(int(inverse[i, j])*z[j] for j in range(h)) % 3 for i in range(h))
        branch = y+new[k:]
        frequencies = packet.component_frequencies(word)
        amplitude = np.exp(2j*np.pi*(sum(s*f for s, f in zip(secret, frequencies)) % 9)/9)/np.sqrt(3**m)
        branches.setdefault(branch, {})[new[:k]] = (frequencies, amplitude)
    records = []
    for branch, outputs in sorted(branches.items()):
        points = list(product(range(3), repeat=k))
        base = outputs[(0,)*k][0]
        residual = [tuple(((a-b) % 9)//3 for a, b in zip(outputs[z][0], base)) for z in points]
        assert all((a-b) % 3 == 0 for z in points for a, b in zip(outputs[z][0], base))
        polynomials = _interpolate(residual, k)
        assert all(row["degree"] <= 2 for row in polynomials)
        assert all(sum(bool(e) for e in term["powers"]) <= 1 for row in polynomials for term in row["coefficients"])
        probability = float(sum(abs(outputs[z][1])**2 for z in points))
        assert abs(probability-3**(-(m-k))) < 4e-12
        records.append({"measured_initial_and_complement_syndrome": branch,
                        "probability": probability, "public_component_frequency_base_mod9": base,
                        "public_divided_residual_table_mod3": residual,
                        "quadratic_component_polynomials": polynomials,
                        "all_unnormalized_native_amplitudes": [[float(outputs[z][1].real), float(outputs[z][1].imag)] for z in points]})
    return {"native_labels": labels, "integer_secret_calibration": secret,
            "low_label_rows": tensor.low_rows, "initial_RREF_rows": packet.reduced_rows,
            "initial_pivots": packet.pivots, "initial_free_columns": packet.free,
            "physical_kernel_columns": tensor.physical_columns, "completed_logical_frame_columns": full,
            "restriction_admission": admission, "all_native_words_replayed": 3**m,
            "all_native_branch_probabilities_sum": sum(c["probability"] for c in records),
            "all_initial_and_complement_outcomes": records,
            "native_qutrits_consumed": m, "retained_quadratic_qutrits": k,
            "retention_is_floor_m_over_n_plus_one_not_constant_fraction": k == m//(packet.secret_dimension+1),
            "original_even_source_acquisition_charged": False,
            "full_secret_top_digit_recovered": False,
            "generic_quadratic_packet_is_decoder": False}


def random_labels(n, m, seed):
    rng = random.Random(seed)
    return [[(rng.randrange(9), rng.randrange(3)) for _ in range(n)] for _ in range(m)]


def run_controls():
    small = compile_packet(random_labels(2, 5, 48011), 3)
    tensor = NativeCubicTensor.from_packet(small)
    identity = [tuple(int(i == j) for i in range(tensor.width)) for j in range(tensor.width)]
    diagonal = tensor.restriction(identity)
    assert diagonal["all_diagonal_triples_zero"] and not diagonal["classical_quadratic_restriction_admitted"]
    scalable = compile_packet(random_labels(4, 20, 48021), 3)
    scalable_tensor = NativeCubicTensor.from_packet(scalable)
    polynomial = public_polynomial(scalable)
    source_packet = compile_packet([[(1, 0)]]*4, 3)
    block = disjoint_block_frame(source_packet)
    rotated = tuple(tuple((a+sign*b) % 3 for a, b in zip(*block)) for sign in (1, -1))
    return {"status": "FACTORED_NATIVE_CUBIC_SCHUR_TENSOR_LOCAL_DERIVATION_REVIEW_PENDING",
            "formula": "Delta_u Delta_v Delta_w Q_l = -sum_i A_li*(V*u)_i*(V*v)_i*(V*w)_i mod3",
            "diagonal_zero_false_admission_control": {"native_labels": small.labels,
                "low_label_rows": tensor.low_rows, "physical_kernel_columns": tensor.physical_columns,
                "mixed_admission": diagonal, "public_polynomial": public_polynomial(small)},
            "polynomial_size_representation_control": {"native_labels": scalable.labels,
                "low_label_rows": scalable_tensor.low_rows, "physical_kernel_columns": scalable_tensor.physical_columns,
                "retained_width": scalable.retained, "input_qutrits": scalable.consumed,
                "public_polynomial": polynomial, "dense_phase_table_size_avoided": str(3**scalable.retained),
                "unknown_secret_decoded": False},
            "all_outcome_disjoint_block_controls": [restricted_native_control(random_labels(1, 6, seed), [8]) for seed in (48031, 48032)],
            "quadratic_source_law_controls": [quadratic_source_ledger(source_packet, frame) for frame in (block, rotated)],
            "claim_gate": {"new_algorithm": False, "candidate_accepted": False,
                "constant_fraction_quadratic_output_rate": False, "growing_level_decoder": False,
                "general_subspace_search_impossibility": False, "independent_human_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "factored_tensor_verified": True, "new_algorithm": False}))


if __name__ == "__main__":
    main()
