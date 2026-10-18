"""Independent channel/amplitude controls; finite numerics, not asymptotic proofs."""
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random

import numpy as np
import pytest
from qiskit import transpile
from qiskit.quantum_info import Operator, Statevector

from theorems.coherent_local_gibbs import (
    CalibrationLimit, CodeProblem, REPORT, coset_mass_table, decoder_program,
    decoder_word_errors, finite_readout, linear_shadow, parity_pgm,
    readout_circuit, run_controls, sample_global_reference, sample_linear_shadow,
    source_circuit,
)
from theorems.bpqm_gibbs_frontier import exact_gibbs
from theorems.xor_factor_reference import ExactXorReference


@pytest.mark.parametrize("degree", [2, 3, 4])
def test_actual_parity_pgm_covariance_on_the_full_hilbert_space(degree):
    circuit = parity_pgm(degree, "13/20")
    assert set(circuit.count_ops()) <= {"u", "cx"}
    U = Operator(circuit).data
    indices = np.arange(1 << degree)
    assert np.max(abs(U.conj().T@U-np.eye(1 << degree))) < 2e-13
    for codeword in range(1 << degree):
        if codeword.bit_count() % 2 == 0:
            quotient_word = codeword & ((1 << (degree-1))-1)
            assert np.max(abs(U[:, indices ^ codeword]-U[indices ^ quotient_word, :])) < 2e-13


@pytest.mark.parametrize("mode", ["linear", "local_pgm", "global_pgm_reference"])
def test_full_decoder_covariance_includes_its_record_register(mode):
    problem = CodeProblem(4, (7, 12))
    A = Operator(decoder_program(problem, "13/20", mode=mode)[0]).data
    indices = np.arange(A.shape[0])
    for word in range(1 << len(problem.structure[0])):
        encoded = problem.encode(word)
        assert np.max(abs(A[:, indices ^ encoded]-A[indices ^ encoded ^ (word << problem.length), :])) < 3e-12


@pytest.mark.parametrize("problem", [CodeProblem(3, (7,)), CodeProblem(4, (7, 12)),
                                      CodeProblem(3, (3, 3, 0)), CodeProblem(2, (1, 2))])
def test_linear_entire_joint_output_has_an_exact_classical_shadow(problem):
    for signs in range(1 << problem.length):
        circuit, _ = readout_circuit(problem, "13/20", signs, mode="linear")
        state = Statevector.from_instruction(circuit)
        actual = state.probabilities(qargs=list(range(problem.length)))
        expected = linear_shadow(problem, "13/20", signs)
        assert sum(expected) == 1
        assert np.max(abs(actual-np.array(list(map(float, expected))))) < 3e-13


@pytest.mark.parametrize("mode", ["linear", "local_pgm", "global_pgm_reference"])
def test_all_signs_and_dependent_checks_keep_legal_support_without_projection(mode):
    problem = CodeProblem(3, (3, 3, 0))
    for signs in range(8):
        result = finite_readout(problem, "13/20", signs, mode=mode)
        assert result["support_leakage_probability_included_not_discarded"] < 2e-12
        assert sum(result["spin_probabilities"]) == pytest.approx(1, abs=3e-12)
        assert result["postselection_used_for_primary_readout"] is False
        assert result["work_register_reset_assumed"] is False
        if mode == "global_pgm_reference":
            assert result["unconditional_TV_including_abort"] < 3e-12


@pytest.mark.parametrize("mode", ["local_pgm", "global_pgm_reference"])
def test_word_error_is_not_a_necessary_sampling_failure(mode):
    problem = CodeProblem(3, (7,))
    errors = decoder_word_errors(problem, "13/20", mode=mode)
    assert errors["average_word_error"] > .10
    for signs in range(8):
        result = finite_readout(problem, "13/20", signs, mode=mode)
        assert result["unconditional_TV_including_abort"] < 4e-12
        assert result["data_purity"] == pytest.approx(1, abs=5e-12)
        assert result["source_and_work_zero_probability"] < .90
        assert result["minimum_trials_per_postselected_output"] > 1.1


def test_overlapping_local_checks_are_not_the_global_pgm():
    problem = CodeProblem(5, (7, 28))
    cases = [finite_readout(problem, "13/20", signs) for signs in range(32)]
    assert np.mean([r["unconditional_TV_including_abort"] for r in cases]) > .15
    assert max(r["unconditional_TV_including_abort"] for r in cases) > .33
    for signs in (0, 13):
        global_result = finite_readout(problem, "13/20", signs, mode="global_pgm_reference")
        assert global_result["unconditional_TV_including_abort"] < 2e-11
        assert global_result["data_purity"] == pytest.approx(1, abs=4e-11)
        assert global_result["resource_ledger"]["global_reference_is_exponential_not_a_scalable_decoder"] is True


@pytest.mark.parametrize("mode", ["local_pgm", "global_pgm_reference"])
def test_zero_noise_does_not_make_either_phase_or_adjoint_optional(mode):
    problem = CodeProblem(3, (7,))
    correct = finite_readout(problem, 0, 1, mode=mode)
    wrong_phase = finite_readout(problem, 0, 1, mode=mode, omit_data_sign_phase=True)
    wrong_adjoint = finite_readout(problem, 0, 1, mode=mode, skip_adjoint=True)
    assert correct["unconditional_TV_including_abort"] < 3e-12
    assert correct["source_and_work_zero_probability"] == pytest.approx(1, abs=3e-12)
    assert wrong_phase["support_leakage_probability_included_not_discarded"] > .99
    assert wrong_adjoint["unconditional_TV_including_abort"] > .4


@pytest.mark.parametrize("mode", ["linear", "local_pgm", "global_pgm_reference"])
def test_source_readout_and_inverse_gate_costs_are_all_charged(mode):
    problem = CodeProblem(3, (7,))
    circuit, ledger = readout_circuit(problem, "13/20", 5, mode=mode)
    compiled = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    assert set(compiled.count_ops()) <= {"u", "cx"}
    assert int(compiled.count_ops().get("u", 0)) == ledger["total_executed_one_qubit_gates"]
    assert int(compiled.count_ops().get("cx", 0)) == ledger["total_executed_CNOTs"]
    assert ledger["qubits_with_source_label_and_work"] == circuit.num_qubits
    assert ledger["universal_gate_synthesis_error_certified"] is False
    assert ledger["global_mass_table_entries_materialized"] == (8 if mode == "global_pgm_reference" else 0)


def test_actual_source_amplitudes_include_all_codeword_phases():
    problem = CodeProblem(3, (7,))
    c = Fraction(13, 20)
    gamma = (1-np.sqrt(1-float(c)**2))/2
    expected = np.zeros(128, dtype=complex)
    for word in range(4):
        encoded = problem.encode(word)
        for data in range(8):
            weight = (encoded ^ data).bit_count()
            expected[data | (word << 3)] = (-1)**((encoded & 5).bit_count())*np.sqrt(gamma**weight*(1-gamma)**(3-weight))/2
    assert np.max(abs(Statevector.from_instruction(source_circuit(problem, c, 5)).data-expected)) < 3e-14


def conditional_classical_law(problem, c, signs):
    # Independent raw Fourier words conditioned on the desired syndrome.
    basis, _ = problem.structure
    weighted = {}
    for y in range(1 << problem.length):
        if all(((g & (y ^ signs)).bit_count() % 2) == 0 for g in basis):
            weighted[y ^ signs] = ((1+c)/2)**(problem.length-y.bit_count())*((1-c)/2)**y.bit_count()
    total = sum(weighted.values())
    return {key: value/total for key, value in weighted.items()}


@pytest.mark.parametrize("problem", [CodeProblem(3, (7,)), CodeProblem(4, (7, 12)), CodeProblem(3, (3, 3, 0))])
def test_same_table_classical_conditional_distribution_equals_the_entire_gibbs_law(problem):
    c = Fraction(13, 20)
    for signs in range(1 << problem.length):
        law = conditional_classical_law(problem, c, signs)
        target = exact_gibbs(problem.ising(signs), c)
        reference = ExactXorReference(problem.ising(signs), c)
        fibers = Counter()
        for spin in range(1 << len(problem.checks)):
            image = 0
            for i, h in enumerate(problem.checks):
                if (spin >> i) & 1:
                    image ^= h
            fibers[image] += 1
        for spin, expected in enumerate(target):
            image = 0
            for i, h in enumerate(problem.checks):
                if (spin >> i) & 1:
                    image ^= h
            assert law[image]/fibers[image] == expected == reference.probability(spin)


@pytest.mark.parametrize("sampler", [sample_linear_shadow, sample_global_reference])
def test_public_classical_samplers_execute_and_do_not_need_a_secret(sampler):
    problem = CodeProblem(4, (7, 12))
    rng = random.Random(20261016)
    counts = Counter(sampler(problem, "13/20", 5, rng) for _ in range(4000))
    if sampler == sample_global_reference:
        expected = exact_gibbs(problem.ising(5), "13/20")
        assert max(abs(counts[x]/4000-float(p)) for x, p in enumerate(expected)) < .04
    else:
        # Both checks independent, so each legal Fourier word has one spin preimage.
        raw = linear_shadow(problem, "13/20", 5)
        for x in range(4):
            image = (7 if x & 1 else 0) ^ (12 if x & 2 else 0)
            assert abs(counts[x]/4000-float(raw[image])) < .04


@pytest.mark.parametrize("bad", [True, -1, 8, 1.0, "1"])
def test_classical_shadows_reject_noncanonical_sign_masks(bad):
    problem = CodeProblem(3, (7,))
    for sampler in (sample_linear_shadow, sample_global_reference):
        with pytest.raises(ValueError):
            sampler(problem, "1/2", bad, random.Random(1))
    with pytest.raises(ValueError):
        linear_shadow(problem, "1/2", bad)


def test_caps_and_precision_failures_are_unknown_not_hardness():
    coset_mass_table(CodeProblem(3, (7,)), 0)
    with pytest.raises(ValueError):
        coset_mass_table(CodeProblem(3, (7,)), False)
    with pytest.raises(CalibrationLimit, match="UNKNOWN"):
        finite_readout(CodeProblem(9, (511,)), "1/2", 0)
    with pytest.raises(CalibrationLimit, match="UNKNOWN"):
        coset_mass_table(CodeProblem(9, (511,)), Fraction(1, 2))
    for c in (Fraction(1, 10**300), Fraction(10**100-1, 10**100)):
        with pytest.raises(CalibrationLimit, match="UNKNOWN"):
            source_circuit(CodeProblem(3, (7,)), c, 0)
    for c in (True, 1., -1, 1):
        with pytest.raises(ValueError):
            source_circuit(CodeProblem(3, (7,)), c, 0)


def test_live_artifact_replays_with_all_dependency_and_scope_flags():
    live = run_controls()
    stored = json.loads(REPORT.read_text())
    assert live == stored
    assert live["source_sha256"] == hashlib.sha256(Path("theorems/coherent_local_gibbs.py").read_bytes()).hexdigest()
    assert len(live["dependency_sha256"]) == 3
    assert live["full_BPQM_decoder_implemented"] is False
    assert live["accepted_speedup_candidate"] is False
    assert live["new_quantum_algorithm_claimed"] is False
    assert live["classical_hardness_proved"] is False
    assert len(live["results"]) == 12
    assert all(row["all_signs_enumerated_no_favorable_selection"] for row in live["results"])
