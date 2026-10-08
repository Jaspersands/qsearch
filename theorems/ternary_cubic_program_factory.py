"""Unmatched one-use native cubic-to-quadratic phase program factory.

LOCAL DERIVATION / REVIEW PENDING. Fixed field root only, not a growing-depth
speedup. Distinct source IDs do not prove the physical IID input premise.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import combinations_with_replacement, product
import json
import math
from pathlib import Path

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source, frequency_coordinates
from ternary_correlated_packet_acquisition import PacketAcquisition, integer, word
from ternary_cyclic_extractor import cyclic_output, random_even_source
from ternary_quadratic_program_receiver import (
    QuadraticFamily, isotropic_direction, nullspace, physical_receiver,
)
from ternary_schur_tensor import NativeCubicTensor

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_cubic_program_factory.json"
DERIVATION = ROOT / "research/TERNARY_CUBIC_PROGRAM_FACTORY.md"


def cubic_powers(d):
    integer(d, "program width", 1)
    return tuple(tuple(indices.count(i) for i in range(d))
                 for indices in combinations_with_replacement(range(d), 3)
                 if indices[0] != indices[2])


def evaluate(components, point):
    return tuple(sum(c*math.prod(pow(x, e, 3) for x, e in zip(point, p))
                     for p, c in row.items()) % 3 for row in components)


@dataclass(frozen=True)
class CubicProgram:
    branch: object
    width: int
    complement: tuple

    def __post_init__(self):
        packet = self.branch.packet
        integer(self.width, "program width", 1)
        if packet.level != 3 or self.width > packet.retained:
            raise ValueError("actual level3 packet with sufficient retained width required")
        word(self.complement, packet.retained-self.width)

    @property
    def components(self): return self.branch.packet.secret_dimension

    @property
    def source_ids(self): return self.branch.acquisition.source_ids

    def logical(self, z): return word(z, self.width)+self.complement

    def value(self, z):
        packet = self.branch.packet
        base = packet.residual(self.logical((0,)*self.width))
        return tuple((a-b) % 3 for a, b in zip(packet.residual(self.logical(z)), base))

    def original_value(self, z):
        base = self.branch.original_residual(self.logical((0,)*self.width))
        return tuple((a-b) % 3 for a, b in zip(self.branch.original_residual(self.logical(z)), base))

    def top(self):
        tensor = NativeCubicTensor.from_packet(self.branch.packet)
        out = [dict() for _ in range(self.components)]
        for indices in combinations_with_replacement(range(self.width), 3):
            if indices[0] == indices[2]: continue
            values = tensor.physical_triple(*(tensor.physical_columns[i] for i in indices))
            factor = 2 if len(set(indices)) == 2 else 1
            p = tuple(indices.count(i) for i in range(self.width))
            for l, x in enumerate(values):
                if x: out[l][p] = factor*x % 3
        return tuple(out)

    def polynomial(self):
        out = [dict(row) for row in self.top()]
        basis = [tuple(int(i == j) for i in range(self.width)) for j in range(self.width)]
        first = [self.value(e) for e in basis]
        for i, e in enumerate(basis):
            second = self.value(tuple(2*x for x in e))
            for l in range(self.components):
                for degree, c in ((1, second[l]-first[i][l]), (2, 2*first[i][l]-second[l])):
                    p = tuple(degree*x for x in e)
                    if c % 3: out[l][p] = c % 3
        for i in range(self.width):
            for j in range(i+1, self.width):
                p = tuple(int(k in (i, j)) for k in range(self.width))
                actual, partial = self.value(p), evaluate(out, p)
                for l in range(self.components):
                    c = (actual[l]-partial[l]) % 3
                    if c: out[l][p] = c
        return tuple(out)

    def record(self):
        branch, packet = self.branch, self.branch.packet
        source = branch.acquisition.source
        polynomial = self.polynomial()
        base = branch.lift(self.logical((0,)*self.width))
        e = [tuple(int(i == j) for i in range(self.width)) for j in range(self.width)]
        columns = [tuple((a-b) % 3 for a, b in zip(branch.lift(self.logical(v)), base)) for v in e]
        exponent = branch.resources()["raw_joint_branch_probability_exponent_base_three"]+packet.retained-self.width
        return {"source": branch.acquisition.source_record(), "original_labels": source.labels,
                "original_frequency_pairs": source.frequencies, "original_affine_base": base,
                "original_affine_columns": columns, "inner_pointers": tuple(branch.anchor[i] for i in branch.acquisition.pointers),
                "outer_syndrome": packet.syndrome, "restriction_complement": self.complement,
                "retained_width": self.width,
                "component_polynomials": [[{"powers": p, "coefficient": c} for p, c in sorted(row.items())] for row in polynomial],
                "raw_program_branch_probability": str(Fraction(1, 3**exponent)),
                "all_source_measurement_outcomes_accepted": True,
                "frame_policy": "first-d-free-Gaussian-coordinates-low-only",
                "public_residual_evaluations_for_polynomial": 2*self.width+self.width*(self.width-1)//2,
                "upstream_input_supply_and_hardware_error_proved": False}


def relation(programs):
    programs = tuple(programs)
    if not programs: raise ValueError("nonempty sourced program cohort required")
    d, n = programs[0].width, programs[0].components
    if any((p.width, p.components) != (d, n) for p in programs):
        raise ValueError("same width and secret coordinates required")
    ids = [x for p in programs for x in p.source_ids]
    if len(set(ids)) != len(ids): raise ValueError("disjoint original ancestry required; no source reuse")
    powers = cubic_powers(d)
    tops = [p.top() for p in programs]
    rows = [[top[l].get(e, 0) for top in tops] for l in range(n) for e in powers]
    kernel = nullspace(rows, len(programs))
    if not kernel: raise ValueError("cohort cubic vectors have no nonzero relation")
    c = kernel[0]
    if any(sum(a*b for a, b in zip(row, c)) % 3 for row in rows) or not any(c):
        raise ArithmeticError("invalid cubic cancellation relation")
    return c, {"cubic_feature_dimension": n*len(powers), "cohort_programs_charged": len(programs),
               "guaranteed_cohort_size": n*len(powers)+1, "coefficients": c,
               "selection_reads_high_linear_or_quadratic_coefficients": False,
               "selected_program_indices": tuple(i for i, x in enumerate(c) if x),
               "unselected_programs_claimed_fresh_IID": False,
               "physical_IID_independence_proved_by_ancestry_ids": False}


def factory(programs, outcomes):
    programs = tuple(programs)
    c, certificate = relation(programs)
    selected = certificate["selected_program_indices"]
    if len(outcomes) != len(selected): raise ValueError("one measured word for each consumed program required")
    d, n = programs[0].width, programs[0].components
    outcomes = tuple(word(m, d) for m in outcomes)
    polynomials = [programs[j].polynomial() for j in selected]
    def value(z):
        z = word(z, d)
        out = [0]*n
        for j, m, polynomial in zip(selected, outcomes, polynomials):
            point = tuple((a+c[j]*b) % 3 for a, b in zip(m, z))
            actual, base = evaluate(polynomial, point), evaluate(polynomial, m)
            out = [(x+a-b) % 3 for x, a, b in zip(out, actual, base)]
        return tuple(out)
    first = [value(tuple(int(i == j) for i in range(d))) for j in range(d)]
    M = [[[0]*d for _ in range(d)] for _ in range(n)]
    beta = [[0]*d for _ in range(n)]
    for i in range(d):
        second = value(tuple(2*int(k == i) for k in range(d)))
        for l in range(n):
            M[l][i][i] = (2*first[i][l]-second[l]) % 3
            beta[l][i] = (second[l]-first[i][l]) % 3
        for j in range(i+1, d):
            point = tuple(int(k in (i, j)) for k in range(d))
            actual = value(point)
            for l in range(n): M[l][i][j] = M[l][j][i] = 2*(actual[l]-first[i][l]-first[j][l]) % 3
    family = QuadraticFamily(tuple(tuple(tuple(row) for row in A) for A in M), tuple(tuple(row) for row in beta))
    source_exponent = sum(p.branch.resources()["raw_joint_branch_probability_exponent_base_three"]+p.branch.packet.retained-d for p in programs)
    record = {**certificate, "injection_outcomes": outcomes,
              "injection_gates": [{"gate": "SUM_F3", "control": "data", "target_program": j, "factor": -c[j] % 3} for j in selected],
              "component_matrices": family.matrices, "component_linear": family.linear,
              "all_injection_outcomes_accepted": True, "each_selected_program_consumed_once": True,
              "cloning_conjugate_program_or_unknown_inverse_used": False,
              "original_native_inputs_charged": sum(len(p.source_ids) for p in programs),
              "original_source_measurement_branch_probability": str(Fraction(1, 3**source_exponent)),
              "conditional_one_injection_transcript_probability": str(Fraction(1, 3**(d*len(selected)))),
              "raw_source_and_injection_transcript_probability": str(Fraction(1, 3**(source_exponent+d*len(selected)))),
              "source_label_law": "conditional IID original full pairs, curvature-only windows, low-only frame/relation and matrix-only receiver",
              "source_theorem_review_status": "LOCAL_DERIVATION_REVIEW_PENDING",
              "growing_depth_speedup_proved": False}
    return family, record, value


def injection_tensor(program, coefficient, secret, data):
    """Replay SUM on supplied program amplitudes, then measure its wires."""
    if type(coefficient) is not int or coefficient not in (1, 2): raise ValueError("nonzero domain coefficient required")
    d, D = program.width, 3**program.width
    if d > 3: raise ValueError("complete injection tensor calibration capped at width3")
    secret = word(secret, program.components)
    data = np.asarray(data, dtype=complex)
    if data.ndim == 1: data = data[None, :]
    if data.ndim != 2 or data.shape[1] != D or abs(float(np.sum(abs(data)**2))-1) > 1e-12:
        raise ValueError("normalized data/reference input required")
    ws = tuple(product(range(3), repeat=d)); index = {w: i for i, w in enumerate(ws)}
    phase = [np.exp(2j*math.pi*(sum(a*b for a, b in zip(secret, program.original_value(u))) % 3)/3) for u in ws]
    output = np.zeros((data.shape[0], D, D), complex)
    for zi, z in enumerate(ws):
        for ui, u in enumerate(ws):
            m = tuple((a-coefficient*b) % 3 for a, b in zip(u, z))
            output[:, index[m], zi] += data[:, zi]*phase[ui]/math.sqrt(D)
    return output


def seeded_cohort(n, d, seed):
    integer(n, "secret dimension", 1); integer(d, "width", 1)
    count = n*len(cubic_powers(d))+1; programs = []
    for j in range(count):
        M = (d+n)*(n+1)**2
        acquisition = PacketAcquisition.from_source(random_even_source(n, 4, M, seed+j), d+n,
            tuple(f"cubic-factory-{n}-{d}-{seed}-{j}-{i}" for i in range(M)), M)
        pointers = tuple((seed+j+i) % 3 for i in range(len(acquisition.pointers)))
        branch = acquisition.branch(pointers)
        syndrome = tuple((seed+j+i+1) % 3 for i in range(len(branch.packet.pivots)))
        branch = acquisition.branch(pointers, syndrome)
        complement = tuple((seed+j+i+2) % 3 for i in range(branch.packet.retained-d))
        programs.append(CubicProgram(branch, d, complement))
    return tuple(programs)


def source_chart_census():
    """Pivot-free conditioned original chart; includes nonzero pointer shifts."""
    records = []
    for curvature in range(3):
        for pointer in range(3):
            counts = Counter()
            for a in range(9):
                for c in range(9):
                    if (a+c) % 3 != curvature: continue
                    other = (0, (-curvature) % 3)
                    labels = ((inverse_frequency_coordinates(a, c, 4),), (inverse_frequency_coordinates(*other, 4),))
                    source = native_source(labels, 4)
                    out = cyclic_output(source, (1, 1), (0, pointer))["native_odd_output_labels"][0]
                    A, C = frequency_coordinates(out, 3)
                    ell = A % 3; alpha = (A-ell)//3; delta = ((C-2*A) % 9)//3
                    counts[ell, alpha, delta] += 1
            if len(counts) != 27 or set(counts.values()) != {1}:
                raise ArithmeticError("conditioned original pivot does not yield uniform odd high coordinates")
            records.append({"curvature": curvature, "pointer": pointer,
                            "odd_chart_words": [list(x) for x in sorted(counts)], "multiplicity": 1})
    return {"complete_conditioned_original_frequency_pairs_checked": 243,
            "conditioned_pivot_controls": records,
            "IID_input_premise_certified_by_finite_census": False}


def vary_linear_lift(program, increments, component=0):
    """New calibration source, NOT a physical transformation of unknown states."""
    acquisition = program.branch.acquisition; source = acquisition.source
    increments = word(increments, len(acquisition.supports))
    integer(component, "source component", 0)
    if component >= source.dimension: raise ValueError("component outside source dimension")
    labels = [list(row) for row in source.labels]
    for support, h in zip(acquisition.supports, increments):
        pivot = support[0]; a, c = (row[component] for row in source.frequencies[pivot])
        labels[pivot][component] = inverse_frequency_coordinates((a+3*h) % 9, (c+6*h) % 9, 4)
    new_source = native_source(labels, 4)
    new = PacketAcquisition.from_source(new_source, len(acquisition.supports), acquisition.source_ids, source.inputs)
    if new.supports != acquisition.supports: raise ArithmeticError("linear lift changed low-only support selection")
    pointers = tuple(program.branch.anchor[i] for i in acquisition.pointers)
    branch = new.branch(pointers, program.branch.packet.syndrome)
    return CubicProgram(branch, program.width, program.complement)


def linear_source_census(programs, outcomes):
    coefficients, certificate = relation(programs); j = certificate["selected_program_indices"][0]
    original = programs[j]; K = len(original.branch.acquisition.supports)
    if K > 5: raise ValueError("complete linear source census capped at five odd inputs")
    baseline, _, _ = factory(programs, outcomes); counts = Counter(); records = []
    for increments in product(range(3), repeat=K):
        cohort = list(programs); cohort[j] = vary_linear_lift(original, increments)
        family, r, _ = factory(cohort, outcomes)
        if tuple(r["coefficients"]) != coefficients or family.matrices != baseline.matrices:
            raise ArithmeticError("alpha affected low-only relation or quadratic matrices")
        if family.linear[1:] != baseline.linear[1:]: raise ArithmeticError("changed unvaried secret components")
        counts[family.linear[0]] += 1
        records.append({"original_pivot_linear_lifts": increments, "component_zero_linear": family.linear[0]})
    if len(counts) != 3**original.width or set(counts.values()) != {3**(K-original.width)}:
        raise ArithmeticError("actual original high lifts did not supply uniform beta")
    return {"varied_program_index": j, "varied_component": 0, "odd_inputs": K,
            "width": original.width, "complete_original_pivot_lifts": 3**K,
            "linear_vector_multiplicity": 3**(K-original.width), "quadratic_matrices_unchanged": True,
            "source_lifts": records, "virtual_lifts_are_additional_physical_samples": False,
            "physical_IID_source_premise_certified": False}


def cost_ledger(n):
    integer(n, "secret dimension", 1)
    d = (n+1)**3-n; R = n*(math.comb(d+2, 3)-d); batch = R+1
    originals = batch*(d+n)*(n+1)**2
    return {"dimension": n, "guaranteed_isotropic_width": d, "cubic_features": R,
            "cohort_program_cap": batch, "original_native_input_cap_per_equation": str(originals),
            "original_native_input_cap_for_n_plus_8_equations": str((n+8)*originals),
            "fixed_root_original_input_cap_polynomial": True, "asymptotic_input_cap_degree_in_n": 15,
            "dense_relation_matrix_field_entries": str(R*batch),
            "dense_relation_elimination_field_operation_scale": str(R*R*batch),
            "asymptotic_dense_relation_memory_degree_in_n": 20,
            "asymptotic_dense_relation_elimination_degree_in_n": 30,
            "field_operation_scale_is_tight_gate_count": False,
            "known_fixed_root_sieves_already_polynomial": True,
            "growing_depth_tensor_or_copy_cost_polynomial": False,
            "full_modulus_recovery_or_cryptographic_reduction_supplied": False}


def run_controls():
    controls = []
    for n, d, seed in ((1, 2, 88705), (1, 3, 88707), (2, 3, 88708)):
        programs = seeded_cohort(n, d, seed)
        coefficients, relation_record = relation(programs)
        selected = relation_record["selected_program_indices"]
        outcomes = tuple(tuple((seed+j+i) % 3 for i in range(d)) for j in selected)
        family, record, value = factory(programs, outcomes)
        ws = tuple(product(range(3), repeat=d))
        for p in programs:
            polynomial = p.polynomial()
            if any(p.original_value(z) != evaluate(polynomial, z) for z in ws):
                raise ArithmeticError("source polynomial disagrees with original phases")
        if any(value(z) != family.value(z) for z in ws): raise ArithmeticError("cubic relation did not yield a quadratic program")
        rng = np.random.default_rng(seed); data = rng.normal(size=(2, 3**d))+1j*rng.normal(size=(2, 3**d)); data /= np.linalg.norm(data)
        maximum = 0.; branches = 0
        secret = tuple(range(1, n+1))
        for j in selected:
            output = injection_tensor(programs[j], coefficients[j], secret, data)
            for mi, m in enumerate(ws):
                expected_phase = np.array([np.exp(2j*math.pi*(sum(a*b for a, b in zip(secret, programs[j].original_value(tuple((a+coefficients[j]*b) % 3 for a, b in zip(m, z))))) % 3)/3) for z in ws])
                maximum = max(maximum, float(np.max(abs(output[:, mi]-data*expected_phase/math.sqrt(3**d)))))
                if abs(float(np.sum(abs(output[:, mi])**2))-3**(-d)) > 3e-12: raise ArithmeticError("nonuniform injection branch")
                branches += 1
        record.update({"programs": [p.record() for p in programs], "seed": seed,
                       "calibration_secret": secret,
                       "control_selection": "prespecified-sign-cancellation-calibrations-not-IID-acceptance-estimate",
                       "source_kind": "seeded-native-calibration-not-population-proof",
                       "complete_injection_tensor_branches": branches,
                       "arbitrary_reference_entangled_injection_max_error": maximum,
                       "complete_original_root_words": len(programs)*3**d,
                       "complete_factory_frequency_table": [value(z) for z in ws]})
        try:
            v, policy = isotropic_direction(family)
        except ValueError:
            record["bounded_receiver_admitted"] = False
        else:
            record.update({"bounded_receiver_admitted": True, "isotropic_search": policy,
                           "physical_receiver": physical_receiver(family, secret, v)})
        if d == 2: record["original_linear_source_census"] = linear_source_census(programs, outcomes)
        controls.append(record)
    return {"status": "UNMATCHED_NATIVE_CUBIC_PROGRAM_FACTORY_FIXED_ROOT_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_controls": controls, "source_chart_census": source_chart_census(),
            "cost_ledgers": [cost_ledger(n) for n in (1, 2, 8, 32)],
            "candidate_record_accepted": False, "growing_depth_speedup_proved": False,
            "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True); REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "original_root_words": sum(c["complete_original_root_words"] for c in report["native_controls"])}, indent=2))


if __name__ == "__main__": main()
