"""Physical logical-gate tests: exact function, phase coherence and clean workspace."""
from itertools import product
import json

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from theorems import lattice_cube_source_circuit as C
from theorems.lattice_cube_coset_source import CubeCosetSource


@pytest.fixture(scope="module", params=(1, -1))
def compiled(request):
    return C.compile_cube_evaluator(CubeCosetSource(((request.param,),),3,1,0,2,2,(1 if request.param==1 else 2,)))


@pytest.mark.parametrize("output", (0, 3))
def test_entire_original_domain_and_nonzero_cell_XOR(compiled, output):
    c = compiled
    for t,a in product((0,1),range(2)):
        initial = c.index(t,(a,),(output,))
        state = Statevector.from_int(initial,2**c.circuit.num_qubits).evolve(c.circuit).data
        expected = c.index(t,(a,),tuple(output ^ (x % 2**len(cell)) for x,cell in zip(c.source.cell(t,(a,)),c.cells)))
        assert abs(state[expected]-1) < 1e-11
        state[expected] = 0
        assert np.linalg.norm(state) < 1e-11


def test_arbitrary_complex_superposition_preserves_all_relative_phases_and_cleans_work(compiled):
    c = compiled
    amplitudes = np.array([1,2j,-3,1-4j],dtype=complex)
    amplitudes /= np.linalg.norm(amplitudes)
    original = np.zeros(2**c.circuit.num_qubits,dtype=complex)
    expected = original.copy()
    for (t,a), amp in zip(product((0,1),range(2)), amplitudes):
        original[c.index(t,(a,))] = amp
        expected[c.index(t,(a,),c.source.cell(t,(a,)))] = amp
    state = Statevector(original).evolve(c.circuit).data
    assert np.linalg.norm(state-expected) < 1e-11
    restored = Statevector(state).evolve(c.circuit.inverse()).data
    assert np.linalg.norm(restored-original) < 1e-11


def test_actual_uniform_parent_matches_Born_cell_weights_and_coherent_fibre(compiled):
    c = compiled
    parent = Statevector.from_instruction(c.uniform_parent()).data
    expected = np.zeros_like(parent)
    for t,a in product((0,1),range(2)):
        expected[c.index(t,(a,),c.source.cell(t,(a,)))] = 0.5
    assert np.linalg.norm(parent-expected) < 1e-11
    fibre = next(f for f in c.source.fibres_for_audit().values() if len(f)==2)
    indices = [c.index(t,a,c.source.cell(t,a)) for t,a in fibre]
    conditioned = np.zeros_like(parent)
    conditioned[indices] = parent[indices]
    probability = float(np.linalg.norm(conditioned)**2)
    assert abs(probability-2/c.source.input_population) < 1e-11
    conditioned /= np.sqrt(probability)
    assert abs(conditioned[indices[0]]-conditioned[indices[1]]) < 1e-11
    inverse = Statevector(conditioned).evolve(c.uniform_parent().inverse()).data
    assert abs(abs(inverse[0])**2-probability) < 1e-11
    assert abs(abs(inverse[0])**2-1) > 0.1


def test_compilation_uses_logarithmic_box_size_not_preimage_enumeration(monkeypatch):
    def prohibited(*args,**kwargs):
        raise AssertionError("compiler may not enumerate classical fibres")
    monkeypatch.setattr(CubeCosetSource,"fibres_for_audit",prohibited)
    for bits in (1,2,3,8):
        c = C.compile_cube_evaluator(CubeCosetSource(((1,),),3,1,0,2**bits,2,(1,)))
        assert c.constant_additions == 2*(bits+2)
        record = c.resource_record()
        assert record["input_qubits"] == bits+1
        assert record["shared_arithmetic_workspace_qubits"] == 2*len(c.workspace[0])+1
        assert record["clean_cell_evaluator_logical_circuit_compiled"]
        assert not record["full_position_QFT_phase_source_readout_compiled"]
        assert not record["shortest_vector_or_shift_or_preimages_used"]


def test_compiled_large_control_is_not_claimed_densely_simulated_or_a_speedup():
    report = json.loads(C.REPORT.read_text())
    large = report["compiled_public_source_controls"][-1]
    assert large["compiled_qubits"] > 100
    assert large["constant_additions_including_uncompute"] <= 2*2*(2*8+2)
    assert not large["hardware_noise_or_fault_tolerance_cost_certified"]
    assert not report["accepted_speedup_candidate"]
    assert not report["efficient_noisy_DCP_decoder_supplied"]


def test_typed_source_and_compiler_caps_are_not_impossibility_theorems():
    with pytest.raises(ValueError):
        C.compile_cube_evaluator({"shift":1})
    with pytest.raises(ValueError,match="no source impossibility"):
        C.compile_cube_evaluator(CubeCosetSource(((2**2000,),),3,1,0,2,2,(1,)))
