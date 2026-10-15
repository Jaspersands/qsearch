"""Actual public lattice parent -> measured cell/label -> opaque phase register.

Exact bounded Born-law reference and numerical logical-circuit diagnostics are
separate. No hidden shift or preimage advice enters compilation or sampling.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import uuid

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator

if __package__:
    from .lattice_cube_coset_source import CubeCosetSource, ROOT, encode_position
    from .lattice_cube_source_circuit import compile_cube_evaluator
    from .lattice_qft_precision import QFTPrecisionPlan, QFTUsageLedger, CircuitResourcePolicy, compile_qft
else:
    from lattice_cube_coset_source import CubeCosetSource, ROOT, encode_position
    from lattice_cube_source_circuit import compile_cube_evaluator
    from lattice_qft_precision import QFTPrecisionPlan, QFTUsageLedger, CircuitResourcePolicy, compile_qft

REPORT = ROOT / "research/phase_workbench/lattice_cube_dcp_readout.json"
DERIVATION = ROOT / "research/LATTICE_CUBE_DCP_READOUT.md"
CONTRACT = ROOT / "research/hypotheses/lattice_cube_dcp_readout_contract.json"
NUMERICAL_TOLERANCE = 1e-7


def source_fingerprint(public_source):
    return hashlib.sha256(json.dumps(public_source, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def dyadic_polynomial(coefficients, root):
    if type(root) is not int or root < 2 or root > 32 or root & (root - 1):
        raise ValueError("bounded dyadic root required")
    if len(coefficients) != root:
        raise ValueError("complete cyclotomic coefficients required")
    c = [Fraction(x) for x in coefficients]
    for i in range(root // 2, root):
        c[i - root // 2] -= c[i]
    c = c[:root // 2]
    while c and not c[-1]:
        c.pop()
    return tuple(str(x) for x in reversed(c))


def polynomial_value(coefficients, root):
    return sum(float(Fraction(c)) * np.exp(2j*np.pi*i/root)
               for i, c in enumerate(reversed(coefficients)))


@dataclass
class CompiledPhaseSource:
    evaluator: object
    padding: QuantumRegister
    position_wires: tuple
    coherent_parent: QuantumCircuit
    qft_plan: QFTPrecisionPlan | None = None
    qft_usage_ledger: QFTUsageLedger | None = None
    qft_gate: object = None

    @property
    def source(self):
        return self.evaluator.source

    def readout_circuit(self, diagnostic_snapshots=False):
        c = self.evaluator
        cell_bits = sum(len(r) for r in c.cells)
        classical = ClassicalRegister(cell_bits + len(self.position_wires), "source_readout")
        qc = QuantumCircuit(*c.circuit.qregs, self.padding, classical)
        qc.compose(c.uniform_parent(), inplace=True)
        cursor = 0
        for register in c.cells:
            qc.measure(register, classical[cursor:cursor+len(register)])
            cursor += len(register)
        qc.append(self.qft_gate, list(self.position_wires))
        qc.measure(list(self.position_wires), classical[cell_bits:])
        if diagnostic_snapshots:
            # Aer only stores classical-register bits used by feed-forward.
            # A whole-register condition prevents deferred/averaged snapshots.
            # Snapshot between two known Z frames; the final qubit is restored.
            with qc.if_test((classical, 0)):
                qc.z(c.input_register[0])
            qc.save_density_matrix([c.input_register[0]], label="phase_qubit", pershot=True, conditional=True)
            with qc.if_test((classical, 0)):
                qc.z(c.input_register[0])
        return qc

    def decode_memory(self, word):
        total = sum(len(r) for r in self.evaluator.cells) + len(self.position_wires)
        if type(word) is not int or not 0 <= word < 2 ** total:
            raise ValueError("canonical measured memory word required")
        cursor, cells = 0, []
        for register in self.evaluator.cells:
            bits = len(register)
            x = (word >> cursor) % (2 ** bits)
            cells.append(x - 2 ** bits if x >= 2 ** (bits - 1) else x)
            cursor += bits
        return tuple(cells), word >> cursor

    def resource_record(self):
        c = self.evaluator
        ell = len(self.position_wires)
        record = {"clean_evaluator": c.resource_record(), "phase_modulus": self.source.phase_modulus,
                "compiled_phase_parent_qubits": self.coherent_parent.num_qubits,
                "position_qubits": ell, "zero_padding_qubits": len(self.padding),
                "original_position_wires_reused_in_place": True,
                "copied_original_position_garbage_retained": False,
                "logical_QFT_H_gates": ell, "logical_QFT_controlled_phase_gates": ell*(ell-1)//2 if self.qft_plan is None else self.qft_plan.controlled_phases,
                "logical_QFT_swap_gates": ell//2,
                "public_cell_and_label_measured_colour_qubit_retained": True,
                "hidden_shift_or_preimages_enter_compiler": False,
                "hardware_or_fault_tolerant_QFT_precision_certified": False}
        if self.qft_plan is not None:
            record["QFT_precision_plan"] = self.qft_plan.record()
            record["QFT_usage_ledger"] = self.qft_usage_ledger.record()
        return record


def compile_phase_source(source, qft_plan=None, policy=None):
    if not isinstance(source,CubeCosetSource):
        raise ValueError("typed public cube source required")
    policy = CircuitResourcePolicy() if policy is None else policy
    if not isinstance(policy,CircuitResourcePolicy):
        raise ValueError("explicit typed circuit resource policy required")
    b = source.box.bit_length()-1
    ell = source.dimension*(b+1)
    if qft_plan is not None and (not isinstance(qft_plan,QFTPrecisionPlan) or qft_plan.wires != ell):
        raise ValueError("QFT precision plan must match actual position wires")
    if qft_plan is None and ell-1 > 1022:
        raise ValueError("UNKNOWN_NUMERIC_ANGLE_RANGE; supply an explicit approximate precision plan")
    qft_instructions = ell+ell//2+(ell*(ell-1)//2 if qft_plan is None else qft_plan.controlled_phases)
    policy.check(qubits=ell, QFT_instructions=qft_instructions)
    c = compile_cube_evaluator(source,policy=policy)
    policy.check(qubits=c.circuit.num_qubits+source.dimension)
    padding = QuantumRegister(source.dimension, "position_padding")
    b = source.box.bit_length() - 1
    wires = tuple(bit for j in range(source.dimension)
                  for bit in (*c.input_register[1+j*b:1+(j+1)*b], padding[j]))
    parent = QuantumCircuit(*c.circuit.qregs, padding)
    parent.compose(c.uniform_parent(), inplace=True)
    gate = QFTGate(ell) if qft_plan is None else compile_qft(qft_plan,policy=policy).to_gate()
    parent.append(gate,list(wires))
    ledger = QFTUsageLedger(qft_plan) if qft_plan is not None else None
    return CompiledPhaseSource(c,padding,wires,parent,qft_plan,ledger,gate)


def exact_born_reference(source, cap=16384):
    D, N = source.input_population, source.phase_modulus
    if N > 32 or D * N > cap:
        raise ValueError("UNKNOWN_EXACT_READOUT_CAP; no source-failure conclusion")
    fibres = source.fibres_for_audit()
    rows = []
    label_trace = [[Fraction(0)] * N for _ in range(N)]
    for cell, fibre in sorted(fibres.items()):
        positions = [[encode_position(a, source.box) for t, a in fibre if t == colour] for colour in (0, 1)]
        for k in range(N):
            matrix = []
            trace = [Fraction(0)] * N
            for t in (0, 1):
                row = []
                for u in (0, 1):
                    coefficients = [Fraction(0)] * N
                    for x in positions[t]:
                        for y in positions[u]:
                            coefficients[(k * (x - y)) % N] += Fraction(1, D * N)
                    row.append(dyadic_polynomial(coefficients, N))
                    if t == u:
                        trace = [a + b for a, b in zip(trace, coefficients)]
                matrix.append(tuple(row))
            label_trace[k] = [a + b for a, b in zip(label_trace[k], trace)]
            rows.append({"cell": cell, "label": k, "unnormalized_colour_density": tuple(matrix),
                         "joint_Born_probability": dyadic_polynomial(trace, N)})
    probabilities = tuple(dyadic_polynomial(c, N) for c in label_trace)
    uniform = all(p == (str(Fraction(1, N)),) for p in probabilities)
    return {"modulus": N, "input_population": D, "all_cell_label_outcomes": tuple(rows),
            "all_label_Born_probabilities": probabilities,
            "label_distribution_uniform": uniform,
            "full_domain_source_shape_audit": source.audit(),
            "preimages_are_private_reference_data_not_emitter_advice": True}


def _valid_density(raw):
    rho = np.asarray(raw, dtype=complex)
    if rho.shape != (2, 2) or not np.all(np.isfinite(rho)) or not np.allclose(rho, rho.conj().T, atol=NUMERICAL_TOLERANCE, rtol=0):
        raise ValueError("UNKNOWN_DENSITY_NUMERICS")
    trace = float(np.trace(rho).real)
    if abs(trace - 1) > NUMERICAL_TOLERANCE or np.linalg.eigvalsh(rho).min() < -NUMERICAL_TOLERANCE:
        raise ValueError("UNKNOWN_DENSITY_NUMERICS")
    return (rho + rho.conj().T) / (2 * trace)


@dataclass(frozen=True)
class PhaseReceipt:
    id: str
    modulus: int
    label: int
    measured_cells: tuple
    ancestors: tuple
    merge_depth: int = 0

    def public_view(self):
        return {"id": self.id, "modulus": self.modulus, "label": self.label,
                "measured_cells": self.measured_cells, "original_source_receipts": self.ancestors,
                "merge_depth": self.merge_depth}


@dataclass
class SimulatedPhaseBatch:
    receipts: tuple
    _densities: dict
    metadata: dict
    _claimed: bool = False

    def __copy__(self):
        raise ValueError("quantum source batches cannot be copied; reprepare and charge the source")

    def __deepcopy__(self, memo):
        return self.__copy__()

    def public_receipts(self):
        return tuple(r.public_view() for r in self.receipts)


def simulate_phase_batch(compiled, shots=32, seed=0, batch_tag=None, force_conditioned_snapshots=True):
    if type(shots) is not int or not 1 <= shots <= 128:
        raise ValueError("bounded complete positive shot count required")
    if compiled.coherent_parent.num_qubits > 48:
        raise ValueError("UNKNOWN_SIMULATOR_CAP; large circuit is not disproved")
    if compiled.qft_usage_ledger is not None:
        compiled.qft_usage_ledger.charge("forward",shots)
    if not force_conditioned_snapshots:
        qc = compiled.readout_circuit()
        qc.save_density_matrix([compiled.evaluator.input_register[0]], label="phase_qubit", pershot=True, conditional=True)
    else:
        qc = compiled.readout_circuit(diagnostic_snapshots=True)
    backend = AerSimulator(method="matrix_product_state", matrix_product_state_truncation_threshold=0.0,
                           max_parallel_threads=1, shot_branching_enable=False)
    circuit = transpile(qc, backend, optimization_level=0, seed_transpiler=seed)
    result = backend.run(circuit, shots=shots, memory=True, seed_simulator=seed).result()
    if not result.success:
        raise RuntimeError("quantum source diagnostic failed")
    metadata = result.results[0].metadata
    memory = [int(s.replace(" ", ""), 2) for s in result.get_memory()]
    counts = Counter(memory)
    snapshots = {int(key, 16): deque(values) for key, values in result.data()["phase_qubit"].items()}
    if metadata.get("measure_sampling") or set(snapshots) != set(counts) or any(len(snapshots[k]) != count for k, count in counts.items()):
        raise ValueError("UNCONDITIONED_OR_INCOMPLETE_SNAPSHOT_REJECTED")
    tag = batch_tag or uuid.uuid4().hex
    receipts, densities = [], {}
    Z = np.diag([1, -1])
    for i, word in enumerate(memory):
        cell, k = compiled.decode_memory(word)
        rho = np.asarray(snapshots[word].popleft().data, dtype=complex)
        # The recorded diagnostic snapshot is between two public Z frames.
        if word == 0:
            rho = Z @ rho @ Z
        receipt = PhaseReceipt(f"{tag}:{i}", compiled.source.phase_modulus, k, (cell,), (f"{tag}:{i}",))
        receipts.append(receipt)
        densities[receipt.id] = _valid_density(rho)
    return SimulatedPhaseBatch(tuple(receipts), densities,
        {"actual_compiled_source_preparations_charged": shots, "original_receipts_emitted": shots,
         "source_function_evaluations_charged": shots, "simulation_method": "Aer matrix_product_state",
         "source_shots_independent_given_public_parameters": True,
         "MPS_truncation_threshold": 0.0, "conditioned_snapshot_key_and_count_checks_passed": True,
         "floating_point_density_tolerance": NUMERICAL_TOLERANCE,
         "numerical_error_is_a_formally_certified_channel_bound": False,
         "public_Z_frame_snapshot_then_correction_used": True,
         "public_source_function_fingerprint": source_fingerprint(compiled.source.public_access()),
         "logical_readout_QFT_is_exact_reference": compiled.qft_plan is None or compiled.qft_plan.exact,
         "hidden_shift_or_preimages_supplied_to_sampler": False,
         "receipt_ids_are_a_security_sandbox": False})


class OpaquePhaseBackend:
    """Destructive simulated quantum operations; density matrices remain audit-private."""
    def __init__(self, batch, shape_audit, seed=0):
        if not shape_audit["valid_two_point_source_on_full_domain"]:
            raise ValueError("MULTIPOINT_SOURCE_IS_NOT_DCP")
        if batch._claimed:
            raise ValueError("source batch already claimed; no backend reset or unpaid reuse")
        if batch.metadata.get("source_shots_independent_given_public_parameters") is not True:
            raise ValueError("explicit conditional-product source model required")
        if batch.metadata.get("logical_readout_QFT_is_exact_reference") is not True:
            raise ValueError("APPROXIMATE_SOURCE_NOT_AN_EXACT_DCP_PROMISE; joint-channel receiver contract required")
        if batch.metadata.get("public_source_function_fingerprint") != source_fingerprint(shape_audit["public_source"]):
            raise ValueError("shape audit is not for the emitted public source")
        if batch.metadata["actual_compiled_source_preparations_charged"] != len(batch.receipts):
            raise ValueError("every original source preparation must be charged")
        if any(r.modulus != shape_audit["public_source"]["phase_modulus"] for r in batch.receipts):
            raise ValueError("emitted modulus differs from audited source")
        if any(r.ancestors != (r.id,) or r.merge_depth != 0 for r in batch.receipts):
            raise ValueError("original emitter receipts cannot impersonate merged or cloned registers")
        self._states = {k: v.copy() for k, v in batch._densities.items()}
        self._receipts = {r.id: r for r in batch.receipts}
        if len(self._receipts) != len(batch.receipts):
            raise ValueError("distinct actual source receipts required")
        batch._claimed = True
        self._active = set(self._receipts)
        self._rng = np.random.default_rng(seed)
        self._serial = 0
        self.source_preparations_charged = batch.metadata["actual_compiled_source_preparations_charged"]

    def __copy__(self):
        raise ValueError("live quantum backend cannot be copied or reset")

    def __deepcopy__(self, memo):
        return self.__copy__()

    def public_view(self, receipt_id):
        if receipt_id not in self._active:
            raise ValueError("register has been consumed or never emitted")
        return self._receipts[receipt_id].public_view()

    def merge(self, left, right):
        if left == right or left not in self._active or right not in self._active:
            raise ValueError("two distinct live registers required; no copying or retry")
        a, b = self._receipts[left], self._receipts[right]
        if a.modulus != b.modulus or set(a.ancestors) & set(b.ancestors):
            raise ValueError("same modulus and disjoint original ancestry required")
        joint = np.kron(self._states[left], self._states[right])
        permutation = (0, 1, 3, 2)
        joint = joint[np.ix_(permutation, permutation)]
        blocks = [joint[np.ix_((j, 2+j), (j, 2+j))] for j in (0, 1)]
        p0 = float(np.trace(blocks[0]).real)
        if not -NUMERICAL_TOLERANCE <= p0 <= 1+NUMERICAL_TOLERANCE:
            raise ValueError("UNKNOWN_BRANCH_NUMERICS")
        branch = 0 if self._rng.random() < min(1, max(0, p0)) else 1
        probability = float(np.trace(blocks[branch]).real)
        self._active.difference_update((left, right))
        if probability < NUMERICAL_TOLERANCE:
            return {"branch": branch, "status": "UNKNOWN_RARE_BRANCH_NUMERICS", "output": None}
        self._serial += 1
        child = PhaseReceipt(f"merge:{self._serial}:{left}", a.modulus,
                             (a.label + (b.label if branch == 0 else -b.label)) % a.modulus,
                             a.measured_cells + b.measured_cells, a.ancestors + b.ancestors,
                             max(a.merge_depth, b.merge_depth)+1)
        self._states[child.id] = _valid_density(blocks[branch]/probability)
        self._receipts[child.id] = child
        self._active.add(child.id)
        return {"branch": branch, "status": "PHYSICAL_BRANCH_SAMPLED", "output": child.public_view()}

    def measure(self, receipt_id, axis="X"):
        matrices = {"X": np.array([[0,1],[1,0]]), "Y": np.array([[0,-1j],[1j,0]]), "Z": np.diag([1,-1])}
        if axis not in matrices or receipt_id not in self._active:
            raise ValueError("live register and X/Y/Z measurement required")
        probability = (1 + float(np.trace(self._states[receipt_id] @ matrices[axis]).real))/2
        if not -NUMERICAL_TOLERANCE <= probability <= 1+NUMERICAL_TOLERANCE:
            raise ValueError("UNKNOWN_MEASUREMENT_NUMERICS")
        bit = int(self._rng.random() >= min(1, max(0, probability)))
        self._active.remove(receipt_id)
        return {"id": receipt_id, "label": self._receipts[receipt_id].label, "axis": axis, "outcome": bit,
                "original_source_receipts": self._receipts[receipt_id].ancestors}


def _serialize_density(rho):
    return tuple(tuple((float(z.real), float(z.imag)) for z in row) for row in rho)


def audit_simulation(compiled, reference, batch):
    table = {(tuple(r["cell"]), r["label"]): r for r in reference["all_cell_label_outcomes"]}
    errors = []
    for receipt in batch.receipts:
        row = table[receipt.measured_cells[0], receipt.label]
        p = polynomial_value(row["joint_Born_probability"], reference["modulus"]).real
        if p <= NUMERICAL_TOLERANCE:
            raise ValueError("observed an exactly zero or unresolved rare reference branch")
        expected = np.array([[polynomial_value(c, reference["modulus"]) for c in r]
                             for r in row["unnormalized_colour_density"]]) / p
        errors.append(float(np.max(np.abs(expected - batch._densities[receipt.id]))))
    error = max(errors, default=0)
    if error > NUMERICAL_TOLERANCE:
        raise ValueError("NUMERICAL_COMPILED_SOURCE_DISAGREES_WITH_EXACT_REFERENCE")
    shape = reference["full_domain_source_shape_audit"]
    logN = compiled.source.phase_modulus.bit_length()-1
    bad = Fraction(shape["bad_register_rate"]) if shape["bad_register_rate"] is not None else None
    return {"simulation_metadata": batch.metadata, "private_audit_max_conditional_density_error": error,
            "exact_reference_agrees_for_every_emitted_register": True,
            "numerical_f1_bad_register_budget": str(Fraction(1,logN)),
            "finite_f1_bad_register_budget_met": bad is not None and bad <= Fraction(1,logN),
            "full_Regev_growing_family_reduction_certified": False,
            "public_receipts": batch.public_receipts(),
            "PRIVATE_AUDIT_ONLY_emitted_density_matrices": {k:_serialize_density(v) for k,v in batch._densities.items()}}


def build_report():
    sources = (CubeCosetSource(((1,),),3,1,0,2,2,(1,)),
               CubeCosetSource(((-1,),),3,1,0,2,2,(2,)),
               CubeCosetSource(((8,2),(7,2)),7,1,0,2,2,(1,1)),
               CubeCosetSource(((1,),),17,1,0,16,8,(1,)),
               CubeCosetSource(((1,),),3,1,0,4,8,(1,)))
    controls = []
    for i, source in enumerate(sources):
        compiled = compile_phase_source(source)
        reference = exact_born_reference(source)
        batch = simulate_phase_batch(compiled, shots=24, seed=99300+i, batch_tag=f"lattice-phase-control-{i}")
        controls.append({"compiled_resources": compiled.resource_record(), "exact_Born_reference": reference,
                         "compiled_source_sampling_audit": audit_simulation(compiled, reference, batch)})
    large = compile_phase_source(CubeCosetSource(((10000,1000),(9999,1000)),389,1,0,256,128,(1,1)))
    return {"status": "PUBLIC_LATTICE_TO_DCP_PHASE_CIRCUIT_AND_OPAQUE_NOISY_REGISTERS_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "dependency_sha256": {f:hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest()
                                  for f in ("lattice_cube_coset_source.py", "lattice_cube_source_circuit.py", "lattice_qft_precision.py")},
            "actual_lattice_source_controls": tuple(controls),
            "large_compiled_not_simulated_phase_source": large.resource_record(),
            "source_preparations_in_finite_calibration": 120,
            "accepted_speedup_candidate": False, "efficient_noisy_DCP_decoder_supplied": False,
            "new_active_negative_result_created": False, "novelty_claim": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status":report["status"],"actual_compiled_source_controls":len(report["actual_lattice_source_controls"]),
                      "charged_source_preparations":report["source_preparations_in_finite_calibration"],
                      "large_compiled_qubits":report["large_compiled_not_simulated_phase_source"]["compiled_phase_parent_qubits"],
                      "accepted_speedup_candidate":False},indent=2))


if __name__ == "__main__":
    main()
