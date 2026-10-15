"""Clean public cube evaluator compiled with Qiskit's CDKM modular adder."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

import qiskit
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.synthesis.arithmetic.adders import adder_ripple_c04

if __package__:
    from .lattice_cube_coset_source import CubeCosetSource, ROOT
    from .lattice_qft_precision import CircuitResourcePolicy
else:
    from lattice_cube_coset_source import CubeCosetSource, ROOT
    from lattice_qft_precision import CircuitResourcePolicy

REPORT = ROOT / "research/reductions/lattice_cube_source_circuit.json"
DERIVATION = ROOT / "research/LATTICE_CUBE_SOURCE_CIRCUIT.md"
CONTRACT = ROOT / "research/hypotheses/lattice_cube_source_circuit_contract.json"


@dataclass
class CompiledCubeEvaluator:
    source: CubeCosetSource
    circuit: QuantumCircuit
    input_register: QuantumRegister
    cells: tuple
    workspace: tuple
    constant_additions: int

    def uniform_parent(self):
        parent = QuantumCircuit(*self.circuit.qregs)
        parent.h(self.input_register)
        parent.compose(self.circuit, inplace=True)
        return parent

    def index(self, t, a, cell_values=None):
        """Basis index for finite tests, with ZERO arithmetic workspace."""
        self.source.lattice_point(t, a)
        value = t
        b = self.source.box.bit_length() - 1
        for j, x in enumerate(a):
            value |= x << (1 + j * b)
        if cell_values is not None:
            if len(cell_values) != len(self.cells):
                raise ValueError("full cell output required")
            for cell, x in zip(self.cells, cell_values):
                x %= 2 ** len(cell)
                for h, qubit in enumerate(cell):
                    value |= ((x >> h) & 1) << self.circuit.find_bit(qubit).index
        return value

    def resource_record(self):
        return {"public_source": self.source.public_access(),
                "width_certificate": self.source.clean_arithmetic_plan(),
                "compiled_qubits": self.circuit.num_qubits,
                "input_qubits": len(self.input_register),
                "cell_output_qubits": sum(len(r) for r in self.cells),
                "shared_arithmetic_workspace_qubits": sum(len(r) for r in self.workspace),
                "constant_additions_including_uncompute": self.constant_additions,
                "logical_instruction_count": len(self.circuit.data),
                "library_adder": "Qiskit adder_ripple_c04(kind=fixed), CDKM",
                "qiskit_version": qiskit.__version__,
                "clean_cell_evaluator_logical_circuit_compiled": True,
                "uniform_parent_logical_circuit_compiled": True,
                "full_position_QFT_phase_source_readout_compiled": False,
                "hardware_noise_or_fault_tolerance_cost_certified": False,
                "shortest_vector_or_shift_or_preimages_used": False}


def cube_resource_estimate(source):
    """Closed exact instruction/qubit counts; no gates or preimages allocated."""
    if not isinstance(source, CubeCosetSource):
        raise ValueError("public cube source required")
    plan = source.clean_arithmetic_plan()
    b = source.box.bit_length() - 1
    widths = plan["coordinate_width_certificates"]
    w = max(c["signed_point_workspace_bits"] for c in widths)
    adds = popcount_sum = 0
    for i in range(source.dimension):
        for j,row in enumerate(source.basis):
            coefficient = (source.prime if j == source.coordinate else 1)*row[i]
            if coefficient:
                adds += b
                popcount_sum += b*coefficient.bit_count() if coefficient > 0 else b*w-b*(b-1)//2-b*((-coefficient)-1).bit_count()
        colour = source.residue_guess*source.basis[source.coordinate][i]
        if colour:
            adds += 1
            popcount_sum += colour.bit_count() if colour > 0 else w-((-colour)-1).bit_count()
        adds += 1
        popcount_sum += w-(source.offsets[i]-1).bit_count()
    outputs = sum(c["signed_cell_output_bits"] for c in widths)
    return {"input_qubits":1+source.dimension*b,"cell_output_qubits":outputs,
            "shared_arithmetic_workspace_qubits":2*w+1,
            "compiled_qubits":1+source.dimension*b+outputs+2*w+1,
            "max_signed_adder_bits":w,"constant_additions_including_uncompute":2*adds,
            "logical_instruction_count":4*popcount_sum+2*adds+outputs,
            "estimate_allocates_quantum_gates_or_preimages":False}


def compile_cube_evaluator(source, policy=None):
    policy = CircuitResourcePolicy() if policy is None else policy
    if not isinstance(policy,CircuitResourcePolicy):
        raise ValueError("explicit typed circuit resource policy required")
    estimate = cube_resource_estimate(source)
    policy.check(qubits=estimate["compiled_qubits"], adder_bits=estimate["max_signed_adder_bits"],
                 constant_additions=estimate["constant_additions_including_uncompute"])
    plan = source.clean_arithmetic_plan()
    b = source.box.bit_length()-1
    widths = plan["coordinate_width_certificates"]
    w = estimate["max_signed_adder_bits"]
    inputs = QuantumRegister(1 + source.dimension * b, "input")
    cells = tuple(QuantumRegister(c["signed_cell_output_bits"], f"cell_{i}") for i, c in enumerate(widths))
    constant, accumulator, carry = QuantumRegister(w, "constant"), QuantumRegister(w, "point"), QuantumRegister(1, "carry")
    registers = (inputs, *cells, constant, accumulator, carry)
    output = QuantumCircuit(*registers)
    adder = adder_ripple_c04(w, kind="fixed").to_gate()
    controlled = adder.control(1)
    additions = 0

    def add_constant(circuit, value, control=None):
        nonlocal additions
        value %= 2 ** w
        if not value:
            return
        ones = [constant[h] for h in range(w) if (value >> h) & 1]
        for bit in ones:
            circuit.x(bit)
        wires = [*constant, *accumulator, *carry]
        circuit.append(adder if control is None else controlled, wires if control is None else [control, *wires])
        for bit in ones:
            circuit.x(bit)
        additions += 1

    for i, cert in enumerate(widths):
        compute = QuantumCircuit(*registers)
        for j, row in enumerate(source.basis):
            multiplier = source.prime if j == source.coordinate else 1
            for h in range(b):
                add_constant(compute, multiplier * row[i] * 2 ** h, inputs[1 + j * b + h])
        add_constant(compute, source.residue_guess * source.basis[source.coordinate][i], inputs[0])
        add_constant(compute, -source.offsets[i])
        output.compose(compute, inplace=True)
        low = cert["low_remainder_bits_to_uncompute"]
        for h, qubit in enumerate(cells[i]):
            output.cx(accumulator[low + h], qubit)
        output.compose(compute.inverse(), inplace=True)
    if len(output.data) != estimate["logical_instruction_count"] or 2*additions != estimate["constant_additions_including_uncompute"]:
        raise ValueError("compiled arithmetic disagrees with closed resource estimate")
    return CompiledCubeEvaluator(source, output, inputs, cells, (constant, accumulator, carry), 2 * additions)


def build_report():
    sources = (CubeCosetSource(((1,),), 3, 1, 0, 2, 2, (1,)),
               CubeCosetSource(((-1,),), 3, 1, 0, 2, 2, (2,)),
               CubeCosetSource(((10000,1000),(9999,1000)),389,1,0,256,128,(1,1)))
    return {"status": "CLEAN_PUBLIC_CUBE_ARITHMETIC_COMPILED_RECEIVER_MISSING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "source_producer_sha256": hashlib.sha256((ROOT / "theorems/lattice_cube_coset_source.py").read_bytes()).hexdigest(),
            "precision_policy_producer_sha256": hashlib.sha256((ROOT / "theorems/lattice_qft_precision.py").read_bytes()).hexdigest(),
            "compiled_public_source_controls": tuple(compile_cube_evaluator(s).resource_record() for s in sources),
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "efficient_noisy_DCP_decoder_supplied": False, "novelty_claim": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status":report["status"],"compiled_qubits":[r["compiled_qubits"] for r in report["compiled_public_source_controls"]],"accepted_speedup_candidate":False},indent=2))


if __name__ == "__main__":
    main()
