"""Gate-level covariant local-PGM decoder and unconditional soft Gibbs readout.

Known local measurement mechanism; finite numerical physics controls, not full
BPQM, a new quantum algorithm, or a speedup certificate. No ideal decoder gate.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import cached_property, lru_cache
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import qiskit
from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import RYGate
from qiskit.quantum_info import Statevector

from theorems.bpqm_gibbs_frontier import XorIsing, affine_system, integer, rational, exact_gibbs
from theorems.linear_erasure_prange_duality import null_basis
from theorems.parity_block_usd_prange import uniform_affine_solution

REPORT = ROOT/"research/phase_workbench/coherent_local_gibbs.json"


class CalibrationLimit(RuntimeError):
    pass


@dataclass(frozen=True)
class CodeProblem:
    length: int
    checks: tuple[int, ...]

    def __post_init__(self):
        integer(self.length, "code length", 1, 512)
        if (type(self.checks) is not tuple or not self.checks
                or any(type(h) is not int or not 0 <= h < 1 << self.length for h in self.checks)):
            raise ValueError("explicit canonical binary check masks required")

    @cached_property
    def structure(self):
        system = affine_system(tuple((h, 0) for h in self.checks), self.length)
        basis = null_basis(self.checks, self.length)
        free = tuple(system["free"])
        if (len(basis) != len(free) or any((g & h).bit_count() % 2 for g in basis for h in self.checks)
                or any(((g >> f) & 1) != int(i == j) for i, g in enumerate(basis) for j, f in enumerate(free))):
            raise ArithmeticError("code basis/information-coordinate invariant failed")
        return basis, free

    def encode(self, information):
        basis, _ = self.structure
        integer(information, "information word", 0, (1 << len(basis))-1)
        result = 0
        for i, g in enumerate(basis):
            if (information >> i) & 1:
                result ^= g
        return result

    def ising(self, signs):
        integer(signs, "clause sign mask", 0, (1 << self.length)-1)
        return XorIsing(len(self.checks), tuple((sum(((h >> j) & 1) << i for i, h in enumerate(self.checks)),
                                                (signs >> j) & 1) for j in range(self.length)))


def _channel(c):
    c = rational(c)
    if not 0 <= c < 1:
        raise ValueError("finite nonnegative inverse temperature required")
    value = float(c)
    if not 0 <= value < 1 or (value == 0 and c != 0):
        raise CalibrationLimit("UNKNOWN: binary64 channel calibration loses the exact overlap")
    gamma = value*value/(2*(1+math.sqrt(1-value*value)))
    if c and not gamma:
        raise CalibrationLimit("UNKNOWN: binary64 flip amplitude underflow")
    return c, gamma


@lru_cache(maxsize=128)
def _parity_pgm(degree, c):
    """Public parity quotient/compression/Fourier gates, not a dense unitary."""
    integer(degree, "bounded parity-check degree", 2, 8)
    c, _ = _channel(c)
    p0, p1 = (1+float(c))/2, (1-float(c))/2
    circuit = QuantumCircuit(degree)
    circuit.h(range(degree))
    pivot = degree-1
    for j in range(pivot):
        circuit.cx(pivot, j)
    for word in range(1 << pivot):
        weight = word.bit_count()
        a = p0**(degree-weight)*p1**weight
        b = p0**weight*p1**(degree-weight)
        angle = -2*math.atan2(math.sqrt(b), math.sqrt(a))
        circuit.append(RYGate(angle).control(pivot, ctrl_state=word), [*range(pivot), pivot])
    circuit.h(range(pivot))
    # The executed program consists of standard one-qubit Euler gates and CNOTs.
    # This is not a finite universal-gate synthesis or a numerical certificate.
    return transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)


def parity_pgm(degree, c):
    return _parity_pgm(degree, rational(c)).copy()


@lru_cache(maxsize=64)
def _coset_mass_table(problem, c):
    """Explicit exponential reference, NOT an efficient coset-weight oracle.

    Coordinates are u=G^T y at the free positions and v=y at the other
    positions. All entries are exact products/sums before gate-angle rounding.
    """
    c = rational(c)
    if not 0 <= c < 1:
        raise ValueError("finite nonnegative temperature required")
    if problem.length > 8:
        raise CalibrationLimit("UNKNOWN: exponential global-PGM reference cap")
    basis, free = problem.structure
    pivots = tuple(j for j in range(problem.length) if j not in free)
    k = len(basis)
    masses = [Fraction(0)]*(1 << problem.length)
    for y in range(1 << problem.length):
        u = sum(((g & y).bit_count() % 2) << i for i, g in enumerate(basis))
        v = sum(((y >> p) & 1) << i for i, p in enumerate(pivots))
        masses[u | (v << k)] = ((1+c)/2)**(problem.length-y.bit_count())*((1-c)/2)**y.bit_count()
    if sum(masses) != 1 or min(masses) <= 0:
        raise ArithmeticError("strict positive normalized Fourier table required")
    return tuple(masses)


def coset_mass_table(problem, c):
    # Validate before cache lookup: bool and exact zero otherwise alias keys.
    return _coset_mass_table(problem, rational(c))


@lru_cache(maxsize=64)
def _global_pgm(problem, c):
    """Explicit public Fourier-coset compression using controlled Ry gates.

    This materializes 2^M masses and is deliberately only a finite reference.
    Its very same conditional probabilities provide a classical Gibbs sampler.
    """
    masses = coset_mass_table(problem, c)
    basis, free = problem.structure
    m, k = problem.length, len(basis)
    pivots = tuple(j for j in range(m) if j not in free)
    circuit = QuantumCircuit(m)
    circuit.h(range(m))
    for i, g in enumerate(basis):
        for p in pivots:
            if (g >> p) & 1:
                circuit.cx(p, free[i])
    # Undo a positive conditional state-preparation tree, suffix first.
    for i in reversed(range(len(pivots))):
        controls = [*free, *pivots[:i]]
        for prefix in range(1 << len(controls)):
            denominator = sum(masses[prefix | (suffix << len(controls))]
                              for suffix in range(1 << (m-len(controls))))
            numerator = sum(masses[prefix | (1 << len(controls)) | (suffix << (len(controls)+1))]
                            for suffix in range(1 << (m-len(controls)-1)))
            probability = numerator/denominator
            angle = -2*math.atan2(math.sqrt(float(probability)), math.sqrt(float(1-probability)))
            gate = RYGate(angle)
            if controls:
                gate = gate.control(len(controls), ctrl_state=prefix)
            circuit.append(gate, [*controls, pivots[i]])
    circuit.h(free)
    return transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)


def decoder_program(problem, c, *, mode="local_pgm", reverse=False, tree_depth=None):
    """Polynomial at bounded check degree; records all information coordinates."""
    c, _ = _channel(c)
    if mode not in ("local_pgm", "linear", "global_pgm_reference", "tree_bpqm", "split_tree_bpqm"):
        raise ValueError("explicit public decoder mode required")
    if mode not in ("tree_bpqm", "split_tree_bpqm") and tree_depth is not None:
        raise ValueError("tree depth only applies to the tree decoder")
    if type(reverse) is not bool:
        raise ValueError("record order flag must be Boolean")
    basis, free = problem.structure
    m, k = problem.length, len(basis)
    circuit = QuantumCircuit(m+k)
    sequence = list(enumerate(free))
    if reverse:
        sequence.reverse()
    one_qubit = cnots = 0
    tree_roots = []
    split_fields = {"additional_split_qubits": 0}
    if mode == "split_tree_bpqm":
        from theorems.coherent_bpqm_split import split_decoder
        circuit, split_fields = split_decoder(problem, c, depth=1 if tree_depth is None else tree_depth, reverse=reverse)
        tree_roots = split_fields.pop("tree_root_programs")
        one_qubit = int(circuit.count_ops().get("u", 0))
        cnots = int(circuit.count_ops().get("cx", 0))
        sequence = []
    if mode == "global_pgm_reference":
        local = _global_pgm(problem, c)
        circuit.compose(local, qubits=range(m), inplace=True)
        for i, coordinate in enumerate(free):
            circuit.cx(coordinate, m+i)
        circuit.compose(local.inverse(), qubits=range(m), inplace=True)
        one_qubit = 2*int(local.count_ops().get("u", 0))
        cnots = 2*int(local.count_ops().get("cx", 0))+k
        sequence = []
    for i, coordinate in sequence:
        if mode == "tree_bpqm":
            from theorems.coherent_bpqm_tree import root_program
            local, root_ledger = root_program(problem, c, coordinate, depth=tree_depth)
            tree_roots.append(root_ledger)
            circuit.compose(local, qubits=range(m), inplace=True)
            circuit.cx(coordinate, m+i)
            circuit.compose(local.inverse(), qubits=range(m), inplace=True)
            counts = local.count_ops()
            one_qubit += 2*int(counts.get("u", 0))
            cnots += 2*int(counts.get("cx", 0))+1
            continue
        rows = [h for h in problem.checks if (h >> coordinate) & 1]
        if mode == "linear" or not rows:
            circuit.cx(coordinate, m+i)
            cnots += 1
            continue
        row = min(rows, key=lambda h: (h.bit_count(), h))
        support = [j for j in range(m) if (row >> j) & 1]
        if len(support) > 8:
            raise CalibrationLimit("UNKNOWN: local controlled-rotation table cap, not a decoder no-go")
        pivot = max(j for j in support if j != coordinate)
        order = [coordinate, *[j for j in support if j not in (coordinate, pivot)], pivot]
        local = _parity_pgm(len(order), c)
        circuit.append(local.to_gate(), order)
        circuit.cx(coordinate, m+i)
        circuit.append(local.inverse().to_gate(), order)
        counts = local.count_ops()
        one_qubit += 2*int(counts.get("u", 0))
        cnots += 2*int(counts.get("cx", 0))+1
    return circuit, {"mode": mode, "record_order_reversed": reverse, "information_bits": k,
                     "data_qubits": m, "decoder_A_one_qubit_Euler_gates": one_qubit,
                     "decoder_A_CNOTs": cnots,
                     "erasure_conversion_one_qubit_Euler_gates": 2*one_qubit,
                     "erasure_conversion_CNOTs": 2*cnots+k,
                     "coherent_workspace_record_qubits": k,
                     "qubits_with_source_label_and_work": m+2*k+split_fields["additional_split_qubits"],
                     "counts_are_constructive_unsimplified_not_optimized": True,
                     "global_mass_table_entries_materialized": (1 << m) if mode == "global_pgm_reference" else 0,
                     "global_reference_is_exponential_not_a_scalable_decoder": mode == "global_pgm_reference",
                     "tree_root_programs": tree_roots,
                     "universal_gate_synthesis_error_certified": False,
                     "full_BPQM_or_reliable_asymptotic_decoder_claimed": False, **split_fields}


def source_circuit(problem, c, signs):
    """Prepare actual coherent bit-flip code states with orthogonal labels."""
    _, gamma = _channel(c)
    basis, _ = problem.structure
    m, k = problem.length, len(basis)
    integer(signs, "source signs", 0, (1 << m)-1)
    circuit = QuantumCircuit(m+2*k)
    for j in range(m):
        circuit.ry(2*math.asin(math.sqrt(gamma)), j)
    for i, g in enumerate(basis):
        circuit.h(m+i)
        if (g & signs).bit_count() % 2:
            circuit.z(m+i)
        for j in range(m):
            if (g >> j) & 1:
                circuit.cx(m+i, j)
    return circuit


def readout_circuit(problem, c, signs, *, mode="local_pgm", reverse=False,
                    omit_data_sign_phase=False, skip_adjoint=False, tree_depth=None):
    """A -> XOR estimate into source label -> A^dagger, then the correct phase/QFT.

    Original and work labels are NEVER reset, projected out or silently ignored
    mid-program. The two fault switches exist for falsification controls only.
    """
    circuit = source_circuit(problem, c, signs)
    decoder, ledger = decoder_program(problem, c, mode=mode, reverse=reverse, tree_depth=tree_depth)
    m, k = problem.length, len(problem.structure[0])
    extra = ledger["additional_split_qubits"]
    if extra:
        circuit.add_register(QuantumRegister(extra, "split_work"))
    mapping = [*range(m), *range(m+k, m+2*k), *range(m+2*k, m+2*k+extra)]
    circuit.append(decoder.to_gate(), mapping)
    for i in range(k):
        circuit.cx(m+k+i, m+i)
    if not skip_adjoint:
        circuit.append(decoder.inverse().to_gate(), mapping)
    if not omit_data_sign_phase:
        for j in range(m):
            if (signs >> j) & 1:
                circuit.z(j)
    circuit.h(range(m))
    source_oneq = m+k+sum((g & signs).bit_count() % 2 for g in problem.structure[0])
    source_cnots = sum(g.bit_count() for g in problem.structure[0])
    repeats = 1 if skip_adjoint else 2
    ledger.update({"source_one_qubit_gates": source_oneq, "source_CNOTs": source_cnots,
                   "final_data_sign_Z_gates": 0 if omit_data_sign_phase else signs.bit_count(),
                   "final_data_H_gates": m,
                   "total_executed_one_qubit_gates": source_oneq+repeats*ledger["decoder_A_one_qubit_Euler_gates"]+m+(0 if omit_data_sign_phase else signs.bit_count()),
                   "total_executed_CNOTs": source_cnots+repeats*ledger["decoder_A_CNOTs"]+k,
                   "fault_skip_adjoint": skip_adjoint,
                   "fault_omit_data_sign_phase": omit_data_sign_phase})
    return circuit, ledger


def _calibration_cap(problem):
    m, k = problem.length, len(problem.structure[0])
    if m+2*k > 20 or m > 8 or len(problem.checks) > 8:
        raise CalibrationLimit("UNKNOWN: finite statevector/sign-enumeration cap; no hardness conclusion")


def decoder_word_errors(problem, c, *, mode="local_pgm", reverse=False, tree_depth=None):
    _calibration_cap(problem)
    _, gamma = _channel(c)
    m, k = problem.length, len(problem.structure[0])
    decoder, ledger = decoder_program(problem, c, mode=mode, reverse=reverse, tree_depth=tree_depth)
    extra = ledger["additional_split_qubits"]
    if ledger["qubits_with_source_label_and_work"] > 20:
        raise CalibrationLimit("UNKNOWN: retained-workspace calibration cap")
    probabilities = []
    for word in range(1 << k):
        circuit = QuantumCircuit(decoder.num_qubits)
        encoded = problem.encode(word)
        for j in range(m):
            circuit.ry(2*math.asin(math.sqrt(gamma)), j)
            if (encoded >> j) & 1:
                circuit.x(j)
        circuit.compose(decoder, inplace=True)
        result = np.abs(Statevector.from_instruction(circuit).data.reshape(1 << extra, 1 << k, 1 << m))**2
        probabilities.append(float(result[:, word, :].sum()))
    return {"success_by_actual_codeword": probabilities,
            "average_word_error": 1-float(np.mean(probabilities)),
            "maximum_word_error": 1-min(probabilities),
            "numerical_calibration_not_formal_gate_error_bound": True}


def _spin_readout(problem, data_probabilities):
    size = 1 << len(problem.checks)
    fibers = {}
    for x in range(size):
        image = 0
        for i, row in enumerate(problem.checks):
            if (x >> i) & 1:
                image ^= row
        fibers.setdefault(image, []).append(x)
    result = np.zeros(size)
    abort = 0.
    for image, mass in enumerate(data_probabilities):
        if image in fibers:
            for x in fibers[image]:
                result[x] += float(mass)/len(fibers[image])
        else:
            abort += float(mass)
    return result, abort


def finite_readout(problem, c, signs, *, mode="local_pgm", reverse=False,
                   omit_data_sign_phase=False, skip_adjoint=False, tree_depth=None):
    _calibration_cap(problem)
    circuit, ledger = readout_circuit(problem, c, signs, mode=mode, reverse=reverse,
                                      omit_data_sign_phase=omit_data_sign_phase, skip_adjoint=skip_adjoint,
                                      tree_depth=tree_depth)
    m, k = problem.length, len(problem.structure[0])
    extra = ledger["additional_split_qubits"]
    if circuit.num_qubits > 20:
        raise CalibrationLimit("UNKNOWN: retained-workspace calibration cap")
    state = Statevector.from_instruction(circuit).data
    environment_data = state.reshape(1 << (2*k+extra), 1 << m)
    reduced_data = environment_data.T@environment_data.conj()
    joint = np.abs(state.reshape(1 << extra, 1 << k, 1 << k, 1 << m))**2
    if abs(float(joint.sum())-1) > 2e-11:
        raise ArithmeticError("gate-level readout state lost normalization")
    data = joint.sum(axis=(0, 1, 2))
    spin, abort = _spin_readout(problem, data)
    target = np.array(list(map(float, exact_gibbs(problem.ising(signs), c))))
    cleared = joint[0, 0, 0, :]
    cleared_probability = float(cleared.sum())
    conditional, conditional_abort = _spin_readout(problem, cleared/cleared_probability) if cleared_probability > 1e-14 else (None, None)
    return {"sign_mask_hex": hex(signs), "spin_probabilities": list(map(float, spin)),
            "data_purity": float(np.trace(reduced_data@reduced_data).real),
            "unconditional_TV_including_abort": float((np.abs(spin-target).sum()+abort)/2),
            "support_leakage_probability_included_not_discarded": abort,
            "source_label_zero_probability": float(joint[:, :, 0, :].sum()),
            "split_workspace_zero_probability": float(joint[0, :, :, :].sum()),
            "source_and_work_zero_probability": cleared_probability,
            "postselected_TV": None if conditional is None else float((np.abs(conditional-target).sum()+conditional_abort)/2),
            "minimum_trials_per_postselected_output": None if cleared_probability <= 1e-14 else 1/cleared_probability,
            "postselection_used_for_primary_readout": False, "work_register_reset_assumed": False,
            "numerical_statevector_control_not_certified_hardware": True, "resource_ledger": ledger}


def linear_shadow(problem, c, signs):
    """Exact finite law of a scalable independent-bit classical sampler."""
    c = rational(c)
    integer(signs, "clause sign mask", 0, (1 << problem.length)-1)
    if not 0 <= c < 1:
        raise ValueError("finite nonnegative temperature required")
    if problem.length > 16:
        raise CalibrationLimit("UNKNOWN: finite shadow enumeration cap, not sampling complexity")
    basis, free = problem.structure
    law = [Fraction(0)]*(1 << problem.length)
    for b in range(1 << problem.length):
        probability = math.prod((1+c if (((b ^ signs) >> j) & 1) == 0 else 1-c)/2
                                for j in range(problem.length))
        image = b
        for g, coordinate in zip(basis, free):
            if (g & b).bit_count() % 2:
                image ^= 1 << coordinate
        law[image] += probability
    return law


def sample_linear_shadow(problem, c, signs, rng):
    c = rational(c)
    integer(signs, "clause sign mask", 0, (1 << problem.length)-1)
    if not 0 <= c < 1:
        raise ValueError("finite nonnegative temperature required")
    basis, free = problem.structure
    b = 0
    for j in range(problem.length):
        p1 = (1-c if ((signs >> j) & 1) == 0 else 1+c)/2
        if rng.randrange(p1.denominator) < p1.numerator:
            b |= 1 << j
    image = b
    for g, coordinate in zip(basis, free):
        if (g & b).bit_count() % 2:
            image ^= 1 << coordinate
    equations = tuple((sum(((h >> j) & 1) << i for i, h in enumerate(problem.checks)),
                       (image >> j) & 1) for j in range(problem.length))
    system = affine_system(equations, len(problem.checks))
    return uniform_affine_solution(system, len(problem.checks), rng)


def sample_global_reference(problem, c, signs, rng):
    """Exact classical output using the SAME exponential conditional table."""
    integer(signs, "clause sign mask", 0, (1 << problem.length)-1)
    masses = coset_mass_table(problem, rational(c))
    basis, free = problem.structure
    pivots = tuple(j for j in range(problem.length) if j not in free)
    k = len(basis)
    prefix = sum(((g & signs).bit_count() % 2) << i for i, g in enumerate(basis))
    for i in range(len(pivots)):
        denominator = sum(masses[prefix | (suffix << (k+i))]
                          for suffix in range(1 << (problem.length-k-i)))
        numerator = sum(masses[prefix | (1 << (k+i)) | (suffix << (k+i+1))]
                        for suffix in range(1 << (problem.length-k-i-1)))
        p = numerator/denominator
        if rng.randrange(p.denominator) < p.numerator:
            prefix |= 1 << (k+i)
    image = 0
    for i, p in enumerate(pivots):
        if (prefix >> (k+i)) & 1:
            image ^= 1 << p
    for i, g in enumerate(basis):
        bit = ((prefix >> i) & 1) ^ ((g & image).bit_count() % 2)
        image |= bit << free[i]
    image ^= signs
    equations = tuple((sum(((h >> j) & 1) << i for i, h in enumerate(problem.checks)),
                       (image >> j) & 1) for j in range(problem.length))
    return uniform_affine_solution(affine_system(equations, len(problem.checks)), len(problem.checks), rng)


def run_controls():
    problems = (CodeProblem(3, (7,)), CodeProblem(5, (7, 28)))
    results = []
    for problem in problems:
        for c in ("1/5", "13/20"):
            for mode in ("linear", "local_pgm", "global_pgm_reference"):
                cases = [finite_readout(problem, c, signs, mode=mode) for signs in range(1 << problem.length)]
                results.append({"length": problem.length, "checks": list(problem.checks), "overlap_c_exact": c,
                    "mode": mode, "word_recovery": decoder_word_errors(problem, c, mode=mode),
                    "all_sign_cases": cases, "all_signs_enumerated_no_favorable_selection": True,
                    "mean_unconditional_TV": float(np.mean([r["unconditional_TV_including_abort"] for r in cases])),
                    "maximum_unconditional_TV": max(r["unconditional_TV_including_abort"] for r in cases)})
    dependencies = ("bpqm_gibbs_frontier.py", "linear_erasure_prange_duality.py", "parity_block_usd_prange.py")
    return {"schema_version": "1.1", "subsystem": "coherent_local_gibbs",
            "mechanism": "known bounded-check PGM with coherent record/XOR/adjoint soft readout",
            "results": results, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest() for name in dependencies},
            "qiskit_version": qiskit.__version__, "numpy_version": np.__version__,
            "numerical_controls_are_not_hardware_error_certificates": True,
            "full_BPQM_decoder_implemented": False, "accepted_speedup_candidate": False,
            "new_quantum_algorithm_claimed": False, "classical_hardness_proved": False,
            "classical_baseline": "exact independent-bit linear shadow; same-table conditional Gibbs sampler; existing integer factor sampler",
            "known_PGM_coset_mechanism_source": "https://arxiv.org/html/2605.03972v1#S6",
            "Holevo_decoding_is_not_a_universal_sampling_gate_source": "https://arxiv.org/html/2609.40345v1"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{k: r[k] for k in ("length", "overlap_c_exact", "mode", "mean_unconditional_TV", "maximum_unconditional_TV")}
                      for r in result["results"]], indent=2))


if __name__ == "__main__":
    main()
