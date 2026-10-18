"""Counterfactual exact-sign diagnostic, NOT a QSVT or dense-decoder implementation.

Even granting perfect spectral sharpening does not fix the chosen cyclic
receiver. Dense matrices here are capped finite falsification references.
"""
from fractions import Fraction
from functools import lru_cache

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

from theorems.bpqm_gibbs_frontier import exact_gibbs
from theorems.coherent_bpqm_split import split_root
from theorems.coherent_local_gibbs import CodeProblem, source_circuit


PROBLEM = CodeProblem(4, (7, 13))


@lru_cache(maxsize=1)
def diagnostics():
    c = Fraction(13, 20)
    gamma = (1-np.sqrt(1-float(c)**2))/2
    states = np.array([[np.sqrt(gamma**((x ^ PROBLEM.encode(word)).bit_count())*
                               (1-gamma)**(4-(x ^ PROBLEM.encode(word)).bit_count()))
                        for x in range(16)] for word in range(4)]).T
    orbit, _ = np.linalg.qr(states)
    P = orbit@orbit.T
    rows, signs = [], []
    for i, root in enumerate(PROBLEM.structure[1]):
        U = Operator(split_root(PROBLEM, c, root, depth=1)[0]).data
        root_z = 1-2*((np.arange(U.shape[0]) >> root) & 1)
        # Compress the ACTUAL public root reflection to initial-zero split work.
        O = (U.conj().T@(root_z[:, None]*U))[:16, :16]
        eigenvalues, eigenvectors = np.linalg.eigh(O)
        sharp = (eigenvectors*np.sign(eigenvalues))@eigenvectors.conj().T
        word_signs = 1-2*((np.arange(4) >> i) & 1)
        delta = (states*word_signs)@states.T/2
        rows.append({"root": root, "gap": float(min(abs(eigenvalues))),
                     "raw_orbit_leakage": float(np.linalg.norm((np.eye(16)-P)@O@orbit)),
                     "sharp_orbit_leakage": float(np.linalg.norm((np.eye(16)-P)@sharp@orbit)),
                     "raw_to_sharp_change": float(np.linalg.norm(O-sharp)),
                     "raw_bit_error": float(.5-np.trace(O@delta).real/4),
                     "sharp_bit_error": float(.5-np.trace(sharp@delta).real/4),
                     "optimal_bit_error": float(.5-sum(abs(np.linalg.eigvalsh(delta)))/4)})
        signs.append(sharp)
    return rows, signs


def test_a_benign_gap_does_not_make_sign_sharpening_preserve_the_native_orbit():
    rows, _ = diagnostics()
    two = next(r for r in rows if r["root"] == 2)
    assert two["gap"] > .78
    assert two["raw_orbit_leakage"] > .20
    assert two["sharp_orbit_leakage"] > two["raw_orbit_leakage"]+.005
    assert two["sharp_bit_error"] < two["raw_bit_error"]
    assert two["sharp_bit_error"] > two["optimal_bit_error"]+.003


def test_an_already_sharp_root_still_has_the_wrong_native_eigenvectors():
    rows, _ = diagnostics()
    three = next(r for r in rows if r["root"] == 3)
    assert three["gap"] > 1-1e-12
    assert three["raw_to_sharp_change"] < 2e-12
    assert three["sharp_orbit_leakage"] > .69
    assert three["sharp_bit_error"] > three["optimal_bit_error"]+.04


def test_even_counterfactual_free_exact_sign_reflections_do_not_fix_whole_gibbs_readout():
    _, signs = diagnostics()
    A = np.eye(64, dtype=complex)
    for i, sharp in enumerate(signs):
        zero, one = (np.eye(16)+sharp)/2, (np.eye(16)-sharp)/2
        flip_record = np.eye(4)[np.arange(4) ^ (1 << i)]
        A = (np.kron(np.eye(4), zero)+np.kron(flip_record, one))@A
    assert np.linalg.norm(A.conj().T@A-np.eye(64)) < 2e-12
    xor = QuantumCircuit(8)
    xor.cx(6, 4)
    xor.cx(7, 5)
    values = []
    for source_signs in range(16):
        state = Statevector.from_instruction(source_circuit(PROBLEM, "13/20", source_signs))
        # Dense reference granted ONLY to falsify this best-case mutation.
        state = state.evolve(Operator(A), qargs=[0, 1, 2, 3, 6, 7]).evolve(xor)
        state = state.evolve(Operator(A.conj().T), qargs=[0, 1, 2, 3, 6, 7])
        finish = QuantumCircuit(8)
        for j in range(4):
            if (source_signs >> j) & 1:
                finish.z(j)
        finish.h(range(4))
        data = state.evolve(finish).probabilities([0, 1, 2, 3])
        spin = data[[0, 7, 13, 10]]
        target = np.array(list(map(float, exact_gibbs(PROBLEM.ising(source_signs), "13/20"))))
        values.append(float((sum(abs(spin-target))+max(0, 1-sum(spin)))/2))
    assert .089 < np.mean(values) < .091
    assert max(values) > .157
