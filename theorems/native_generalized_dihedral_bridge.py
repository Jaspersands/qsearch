"""Costed native-qutrit to generalized-dihedral phase-state reduction.

Known-baseline interface, not a new hidden-shift algorithm or a noisy sieve.
True secrets occur only in forward controls, never projection/merge gates.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random

from flint import fmpq
import numpy as np

from cyclotomic_rescaling_gate import ideal_chart, pairing, reduce_element
from cyclic_centre_state_hsp_receiver import density
from native_state_hsp_bridge import NativeGroup, ring_words
from native_uniform_descent_receiver import OriginalSource, SourceExhausted, forward_fixture, resource_contract
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_GENERALIZED_DIHEDRAL_BRIDGE.md"
REPORT = ROOT/"research/reductions/native_generalized_dihedral_bridge.json"
KU_SOURCE = "https://arxiv.org/abs/quant-ph/0302112"


@dataclass(frozen=True)
class AdditiveChart:
    level: int
    dimension: int = 1

    def __post_init__(self):
        NativeGroup(self.level, self.dimension)

    @property
    def orders(self):
        q = 3**(self.level//2)
        return ((3*q, q) if self.level % 2 else (q, q))*self.dimension

    @property
    def dual_matrix(self):
        Q = 3**((self.level+1)//2)
        u, v = (int(Q*b) for b in ideal_chart(self.level)[1])
        if self.level % 2:
            if (v-u) % 3:
                raise ArithmeticError("ramified dual cross coefficient must be divisible by3")
            T = ((u, v-u), ((v-u)//3, -v))
        else:
            T = ((u, v), (v, -u-v))
        if T[0][0]*T[1][1]-T[0][1]*T[1][0] != -1:
            raise ArithmeticError("perfect native pairing requires a unimodular chart")
        return T

    def coordinates(self, value):
        value = NativeGroup(self.level, self.dimension).vector(value)
        out = []
        for i, (a, b) in enumerate(value):
            out.extend(((a+b) % self.orders[2*i], b) if self.level % 2 else (a, b))
        return tuple(out)

    def canonical(self, coordinates):
        if len(coordinates) != len(self.orders) or any(type(v) is not int or not 0 <= v < m for v, m in zip(coordinates, self.orders)):
            raise ValueError("canonical mixed cyclic coordinates required")
        return tuple(coordinates)

    def value(self, coordinates):
        coordinates = self.canonical(coordinates)
        return tuple(reduce_element((coordinates[2*i]-coordinates[2*i+1], coordinates[2*i+1])
                                    if self.level % 2 else coordinates[2*i:2*i+2], self.level)
                     for i in range(self.dimension))

    def dual(self, label):
        x, T = self.coordinates(label), self.dual_matrix
        return tuple((T[j][0]*x[2*i]+T[j][1]*x[2*i+1]) % self.orders[2*i+j]
                     for i in range(self.dimension) for j in range(2))

    def label(self, dual):
        dual, T = self.canonical(dual), self.dual_matrix
        inverse = ((-T[1][1], T[0][1]), (T[1][0], -T[0][0]))
        x = tuple((inverse[j][0]*dual[2*i]+inverse[j][1]*dual[2*i+1]) % self.orders[2*i+j]
                  for i in range(self.dimension) for j in range(2))
        return self.value(x)

    def character(self, dual, secret_coordinates):
        dual, secret_coordinates = self.canonical(dual), self.canonical(secret_coordinates)
        return sum((Fraction(a*s, m) for a, s, m in zip(dual, secret_coordinates, self.orders)), Fraction()) % 1

    def record(self):
        return {"native_level": self.level, "ring_dimension": self.dimension, "cyclic_orders": self.orders,
                "additive_coordinates": "(a+b,b) in basis(1,pi)" if self.level % 2 else "(a,b) in basis(1,zeta)",
                "dual_matrix_per_coordinate": self.dual_matrix, "dual_matrix_determinant": -1,
                "group_order_log3_exact": self.level*self.dimension,
                "basis_chart_is_a_field_shadow": False}


@dataclass(frozen=True)
class BinaryPhaseSample:
    dual_label: tuple[int, ...]
    cyclic_orders: tuple[int, ...]
    state: np.ndarray
    original_indices: tuple[int, ...]

    def __post_init__(self):
        orders, label, ids = tuple(self.cyclic_orders), tuple(self.dual_label), tuple(self.original_indices)
        if (not orders or len(label) != len(orders) or any(type(m) is not int or m < 1 for m in orders) or
                any(type(k) is not int or not 0 <= k < m for k, m in zip(label, orders))):
            raise ValueError("canonical public dual label in a declared finite abelian group required")
        if not ids or len(set(ids)) != len(ids) or any(type(i) is not int or i < 0 for i in ids):
            raise ValueError("paid distinct original physical ancestry required")
        rho = density(self.state)
        if rho.shape != (2, 2) or np.max(abs(np.diag(rho)-.5)) > 1e-12:
            raise ValueError("normalized binary phase density with uniform diagonal required")
        rho = rho.copy()
        rho.setflags(write=False)
        object.__setattr__(self, "dual_label", label)
        object.__setattr__(self, "cyclic_orders", orders)
        object.__setattr__(self, "original_indices", tuple(sorted(ids)))
        object.__setattr__(self, "state", rho)


def project_native_density(label, rho, level, original_indices):
    rho = density(rho)
    if rho.shape != (3, 3) or np.max(abs(np.diag(rho)-1/3)) > 1e-12:
        raise ValueError("supplied uniform-diagonal native qutrit required by this source contract")
    chart = AdditiveChart(level, len(label))
    probability = float(np.trace(rho[:2, :2]).real)
    sample = BinaryPhaseSample(chart.dual(label), chart.orders, rho[:2, :2]/probability, original_indices)
    return sample, {"success_probability": probability, "ideal_success_probability_exact": "2/3",
                    "projector": "|0><0|+|1><1|", "rejected_outcome": "|2><2|",
                    "public_native_label": label, "public_dual_label": sample.dual_label,
                    "normalized_retained_density": [[[float(z.real), float(z.imag)] for z in row] for row in sample.state],
                    "original_indices": sample.original_indices, "state_prepared_from_secret": False,
                    "success_filters_higher_label_digits": False}


def extraction_budget(required_outputs, failure_bits=16):
    integer(required_outputs, "positive binary output count", 1)
    integer(failure_bits, "positive source failure bits", 1)
    C = 3*(required_outputs+failure_bits)
    exact = 2**(required_outputs-1)*fmpq(2, 3)**C
    return {"required_binary_outputs": required_outputs, "original_copy_cap": C, "failure_bits": failure_bits,
            "ideal_IID_extraction_failure_upper_exact": str(exact),
            "simpler_failure_upper": str(fmpq(1, 2**(failure_bits+1))),
            "acceptance_is_label_and_secret_independent": True,
            "finite_source_or_preparation_promises_established_here": False}


def extract_binary_source(source, required_outputs, rng, failure_bits=16):
    budget = extraction_budget(required_outputs, failure_bits)
    if source.cap < budget["original_copy_cap"]:
        raise ValueError("declare and pay the complete original cap before accepting the promised failure bound")
    if source.count:
        raise ValueError("fresh original source with its own paid extraction budget required")
    outputs, records = [], []
    exhausted = None
    while len(outputs) < required_outputs and source.count < budget["original_copy_cap"]:
        try:
            packet = source.take()
        except SourceExhausted as error:
            exhausted = str(error)
            break
        sample, record = project_native_density(packet.sample.label, np.outer(packet.sample.state, packet.sample.state.conj()), source.level, packet.original_indices)
        accepted = bool(rng.random() < record["success_probability"])
        record["accepted"] = accepted
        records.append(record)
        if accepted:
            outputs.append(sample)
    return tuple(outputs), {"status": "FINITE_GENERALIZED_DIHEDRAL_PHASE_BATCH_READY" if len(outputs) == required_outputs else "NO_COMPLETE_BATCH_FROM_PAID_FINITE_SOURCE",
                            "budget": budget, "original_inputs_supplied": source.count, "source_exhaustion": exhausted,
                            "projection_records": records, "outputs_accepted": len(outputs),
                            "rejected_original_indices": [i for r in records if not r["accepted"] for i in r["original_indices"]],
                            "original_source_records": source.input_records if source.retain_trace else None,
                            "receiver_takes_hidden_secret": False, "hidden_shift_solved": False,
                            "quantum_hardware_executed": False, "new_quantum_speedup_established": False}


def binary_merge(left, right, outcome):
    if left.cyclic_orders != right.cyclic_orders or type(outcome) is not int or outcome not in (0, 1):
        raise ValueError("matching finite abelian group and actual measured bit required")
    if set(left.original_indices).intersection(right.original_indices):
        raise ValueError("physical phase samples cannot reuse an original ancestor")
    sign = 1 if outcome == 0 else -1
    label = tuple((a+sign*b) % m for a, b, m in zip(left.dual_label, right.dual_label, left.cyclic_orders))
    order = (outcome, 1-outcome)
    rho = left.state*right.state[np.ix_(order, order)]
    probability = float(np.trace(rho).real)
    child = BinaryPhaseSample(label, left.cyclic_orders, rho/probability, left.original_indices+right.original_indices)
    return child, {"measured_complement_bit": outcome, "label_sign": sign, "input_dual_labels": (left.dual_label, right.dual_label),
                   "output_dual_label": label, "original_indices": child.original_indices,
                   "input_original_lineages": (left.original_indices, right.original_indices),
                   "branch_probability": probability, "ideal_branch_probability_exact": "1/2",
                   "quantum_recipe": "CNOT(control=left,target=right), measure right, retain left",
                   "normalized_retained_density": [[[float(z.real), float(z.imag)] for z in row] for row in child.state],
                   "unknown_secret_used": False, "unknown_state_inverse_used": False,
                   "either_sign_can_be_chosen_deterministically": False}


def finite_control(dimension, level, seed, required=16):
    G, chart = NativeGroup(level, dimension), AdditiveChart(level, dimension)
    rng, h = random.Random(seed), ideal_chart(level)[0]
    truth = tuple((rng.randrange(h[0]), rng.randrange(h[2])) for _ in range(dimension))
    budget = extraction_budget(required)
    original = OriginalSource(forward_fixture(level, truth, seed+1), level, dimension, budget["original_copy_cap"], retain_trace=True)
    samples, result = extract_binary_source(original, required, np.random.default_rng(seed+2))
    if len(samples) != required:
        raise ArithmeticError("committed extraction control failed its paid cap")
    secret_coordinates = chart.coordinates(truth)
    merges = []
    for left, right in zip(samples[::2], samples[1::2]):
        branches = []
        for outcome in (0, 1):
            child, record = binary_merge(left, right, outcome)
            theta = chart.character(child.dual_label, secret_coordinates)
            phi = np.array([1, np.exp(2j*np.pi*float(theta))])/np.sqrt(2)
            if np.max(abs(child.state-np.outer(phi, phi.conj()))) > 1e-12:
                raise ArithmeticError("binary branch does not retain the actual native secret character")
            branches.append(record)
        merges.append({"branches_are_alternative_counterfactual_replays_not_two_physical_outputs": True,
                       "both_actual_instrument_branches": branches})
    return {"dimension": dimension, "level": level, "truth_fixture_only": G.vector(truth),
            "secret_additive_coordinates_fixture_only": secret_coordinates, "additive_chart": chart.record(),
            "extraction": result, "binary_merge_controls": merges}


def baseline_contract(dimension, level):
    NativeGroup(level, dimension)
    return {"dimension": dimension, "level": level, "entropy_log3_exact": dimension*level,
            "native_measured_descent_original_copy_upper": resource_contract(dimension, level)["original_copy_upper"],
            "known_ideal_generalized_dihedral_time_query_form": "2^{O(sqrt(n*L*log2(3)))}",
            "citation": KU_SOURCE, "source_location": "Theorem7.1 and the explicitly supplied labelled phase qubits in Section7",
            "constants_or_finite_runtime_estimated": False, "complete_Kuperberg_sieve_implemented": False,
            "known_bound_is_a_new_quantum_algorithm": False, "noise_robustness_inherited_from_ideal_theorem": False,
            "classical_original_data_separation_established": False,
            "conditional_integer_secret_entropy_log3_exact": dimension*((level+1)//2),
            "conditional_integer_embedding_active_phase_axes": tuple(range(0, 2*dimension, 2)),
            "integer_embedding_verified_from_data": False,
            "conditional_integer_secret_known_baseline_form": "2^{O(sqrt(n*ceil(L/2)*log2(3)))}",
            "fixed_level_polynomial_native_receiver_also_available": True}


def build_report():
    controls = [finite_control(n, L, 14000+100*n+L) for n, L in ((1, 2), (1, 3), (2, 3), (4, 4))]
    censuses = []
    for L in (1, 2, 3, 4):
        chart = AdditiveChart(L)
        labels = ring_words(L)
        dual = [chart.dual((a,)) for a in labels]
        if len(set(dual)) != len(labels) or any(chart.label(k) != (a,) for a, k in zip(labels, dual)):
            raise ArithmeticError("uniform native labels did not map bijectively to the dual group")
        censuses.append({"level": L, "native_ring_labels": labels, "dual_labels": dual, "chart": chart.record()})
    return {"status": "NATIVE_TO_GENERALIZED_DIHEDRAL_PHASE_BRIDGE_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
                                  for name in ("cyclotomic_rescaling_gate.py", "native_state_hsp_bridge.py",
                                               "native_uniform_descent_receiver.py", "cyclic_centre_state_hsp_receiver.py")},
            "additive_dual_label_censuses": censuses, "finite_original_source_controls": controls,
            "scalable_chart_controls": [AdditiveChart(L, 4).record() for L in (1, 2, 3, 4, 16, 64, 128, 256)],
            "known_baseline_contracts": [baseline_contract(n, L) for n in (8, 32, 128) for L in (2, 4, 2*n)],
            "known_ideal_solver_is_implemented_here": False, "efficient_growing_depth_receiver_supplied": False,
            "noisy_receiver_supplied": False, "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "uniform_dual_censuses": 4,
                      "finite_source_controls": 4, "original_copy_counts": [c["extraction"]["original_inputs_supplied"] for c in report["finite_original_source_controls"]],
                      "complete_known_solver_implemented": False, "new_quantum_speedup_established": False}, indent=2))


if __name__ == "__main__":
    main()
