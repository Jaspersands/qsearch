from dataclasses import replace
from fractions import Fraction as Q
from itertools import product
import json
import random

import numpy as np
import pytest
from scipy.linalg import block_diag, expm

from theorems import coherent_gibbs_readout as c


P = {
    "I": np.eye(2), "X": np.array([[0, 1], [1, 0]]),
    "Y": np.array([[0, -1j], [1j, 0]]), "Z": np.diag([1, -1]),
}


def pauli(word):
    result = np.ones((1, 1))
    for letter in reversed(word):
        result = np.kron(result, P[letter])
    return result


def dense_hamiltonian(model):
    blocks = []
    for z in range(1 << model.central_bits):
        h = np.zeros((1 << model.n, 1 << model.n))
        for i, f in enumerate(model.columns):
            sign = (-1)**((f & z).bit_count() & 1)
            word = ["I"]*model.n
            word[i] = "X"
            h += float(model.transverse[i])*pauli(word)
            word[i] = "Z"
            h += float(model.longitudinal[i]+model.coupled[i]*sign)*pauli(word)
            h += float(model.central[i]*sign)*np.eye(1 << model.n)
        blocks.append(h)
    return block_diag(*blocks)


def dense(model):
    root = expm(-float(model.beta)*dense_hamiltonian(model)/2)
    size = 1 << model.n
    weights = np.array([np.vdot(root[z*size:(z+1)*size, z*size:(z+1)*size],
                               root[z*size:(z+1)*size, z*size:(z+1)*size]).real
                        for z in range(1 << model.central_bits)])
    return root, weights/weights.sum()


def small():
    return c.BlockModel(1, (1,), (Q(4, 5),), (Q(1, 3),),
                        (Q(1, 2),), (Q(1, 5),), Q(7, 10))


def midpoint(bounds):
    return float(sum(bounds)/2)


def test_all_two_copy_paulis_against_actual_dense_canonical_tfd():
    model = small()
    root, law = dense(model)
    psi = root.reshape(-1)/np.linalg.norm(root)
    for cl, cr, al, ar in product("IXYZ", repeat=4):
        observable = c.PauliReadout(cl, cr, al, ar)
        estimator = c.PairedEstimator(model, observable)
        values = [estimator.evaluate(z) for z in range(2)]
        actual = sum(law[z]*midpoint(values[z]) for z in range(2))
        operator = np.kron(pauli(al+cl), pauli(ar+cr))
        expected = np.vdot(psi, operator@psi)
        assert abs(actual-expected) < 2e-14
        assert all(-1 <= lo <= hi <= 1 and hi-lo < Q(1, 10**25) for lo, hi in values)


@pytest.mark.parametrize("seed", range(4))
def test_dependent_label_multi_block_paulis_and_pair_symmetry(seed):
    model = replace(c.repetition_model(3), beta=Q(3, 4))
    root, law = dense(model)
    rng = random.Random(seed)
    for _ in range(24):
        cl = "".join(rng.choice("IXYZ") for _ in range(2))
        cr = "".join(rng.choice("IXYZ") for _ in range(2))
        al = "".join(rng.choice("IXYZ") for _ in range(3))
        ar = "".join(rng.choice("IXYZ") for _ in range(3))
        observable = c.PauliReadout(cl, cr, al, ar)
        estimator = c.PairedEstimator(model, observable)
        values = [midpoint(estimator.evaluate(z)) for z in range(4)]
        expected = np.trace(root.conj().T@pauli(al+cl)@root@pauli(ar+cr).T)/np.vdot(root, root)
        assert abs(np.dot(law, values)-expected) < 1e-13
        if not estimator.zero:
            assert all(abs(values[z]-values[z ^ estimator.flip]) < 1e-14 for z in range(4))


def test_y_transpose_and_mismatched_central_flip_are_not_ignored():
    model = replace(small(), beta=Q(0))
    assert midpoint(c.PairedEstimator(model, c.PauliReadout("Y", "Y", "I", "I")).evaluate(0)) == -1
    assert midpoint(c.PairedEstimator(model, c.PauliReadout("I", "I", "Y", "Y")).evaluate(0)) == -1
    assert c.PairedEstimator(model, c.PauliReadout("X", "I", "I", "I")).evaluate(0) == (0, 0)


def test_coherent_signal_is_not_a_diagonal_gibbs_observable():
    model = replace(small(), longitudinal=(Q(0),), central=(Q(0),))
    value = midpoint(c.PairedEstimator(model, c.PauliReadout("X", "X", "I", "I")).evaluate(0))
    a, h, beta = map(float, (model.transverse[0], model.coupled[0], model.beta))
    expected = (a*a+h*h/np.cosh(beta*np.sqrt(a*a+h*h)))/(a*a+h*h)
    assert abs(value-expected) < 2e-14
    assert value > 0.9
    # The corresponding diagonal classical mixture has no central X coherence.
    diagonal_mixture_value = 0
    assert value != diagonal_mixture_value


def test_local_interval_factors_match_exponential_and_norm():
    model = replace(small(), transverse=(Q(0),), longitudinal=(Q(1, 2),))
    factors, weights = c.local_factors(model)
    for j, sign in enumerate((1, -1)):
        h = float(model.transverse[0])*P["X"] + float(model.longitudinal[0]+sign*model.coupled[0])*P["Z"]
        h += float(sign*model.central[0])*P["I"]
        expected = expm(-float(model.beta)*h/2)
        actual = np.array([[complex(factors[0][j][r, s]) for s in range(2)] for r in range(2)])
        np.testing.assert_allclose(actual, expected, atol=2e-15)
        assert abs(float(weights[0][j])-np.vdot(expected, expected)) < 2e-15


def pin_law(sampler):
    model = sampler.model
    law = [Q(0)]*((1 << model.central_bits)+1)
    for selection in product((0, 1), repeat=model.n):
        probability = Q(1)
        equations = []
        for i, selected in enumerate(selection):
            p = Q(abs(sampler.signed_pins[i]), 1 << sampler.coin_bits)
            probability *= p if selected else 1-p
            if selected:
                equations.append((model.columns[i], int(sampler.signed_pins[i] < 0)))
        system = c.affine_system(equations, model.central_bits)
        if system["rank"] != len(equations):
            law[-1] += probability
        else:
            solutions = [z for z in range(1 << model.central_bits)
                         if all(((z & f).bit_count() & 1) == sign for f, sign in equations)]
            for z in solutions:
                law[z] += probability/len(solutions)
    return law


@pytest.mark.parametrize("beta", [Q(0), Q(1, 8), Q(1), Q(7)])
@pytest.mark.parametrize("columns", [(1, 2, 3), (1, 1, 0)])
def test_actual_quantized_pin_law_and_abstention_are_charged(beta, columns):
    model = replace(c.repetition_model(3), columns=columns, beta=beta)
    sampler = c.PinSampler(model, coin_bits=8)
    law = pin_law(sampler)
    _, target = dense(model)
    assert sum(law) == 1
    tv = (sum(abs(float(p)-q) for p, q in zip(law[:-1], target))+float(law[-1]))/2
    assert tv <= float(sampler.tv_upper)+2e-15
    assert sampler.kernel_word_count == len(c.kernel_words(model))


def test_dependent_pins_abstain_instead_of_postselecting():
    class ZeroCoins:
        def getrandbits(self, bits):
            return 0

    sampler = c.PinSampler(c.repetition_model(3))
    assert sampler.draw(ZeroCoins()) is None
    assert all(p != 0 for p in sampler.signed_pins)


def test_kernel_enumeration_independently_matches_exhaustive_binary_relations():
    model = replace(c.repetition_model(5), columns=(1, 3, 2, 7, 4))
    expected = set()
    for word in range(1, 1 << model.n):
        image = 0
        for i, column in enumerate(model.columns):
            if (word >> i) & 1:
                image ^= column
        if image == 0:
            expected.add(word)
    assert set(c.kernel_words(model)) == expected
    assert c.kernel_words(c.repetition_model(128)) == ((1 << 128)-1,)
    with pytest.raises(ValueError, match="budget"):
        c.kernel_words(model, max_nullity=0)


def test_independent_parity_reference_matches_dense_and_large_interval():
    for n in (3, 4):
        model = c.repetition_model(n)
        root, _ = dense(model)
        a = pauli("I"*n+"X"*(n-1))
        expected = np.trace(root@a@root@a.T)/np.vdot(root, root)
        assert abs(midpoint(c.repetition_reference(model))-expected) < 1e-13
    model = c.repetition_model(128)
    lo, hi = c.repetition_reference(model)
    assert 0 < lo < hi < 1
    assert hi-lo < Q(1, 10**40)
    assert c.PinSampler(model).tv_upper < Q(1, 10**17)


def test_estimator_remains_bounded_when_unsymmetrized_ratio_is_large():
    model = replace(small(), central=(Q(60),), beta=Q(1))
    est = c.PairedEstimator(model, c.PauliReadout("X", "X", "I", "I"))
    for z in (0, 1):
        lo, hi = est.evaluate(z)
        assert -1 <= lo <= hi <= 1
    w = [float(value) for value in est.weights[0]]
    assert max(w)/min(w) > 1e40
    assert float(est.contractions[0][0][1].real)/min(w) > 1e20


def test_confidence_ledger_charges_sampler_bias_and_finite_arithmetic():
    model = c.repetition_model(3)
    obs = c.PauliReadout("XX", "XX", "III", "III")
    result = c.estimate(model, obs, 64, 19)
    assert Q(result["systematic_observable_bias_upper"]) == 2*Q(result["sampler_tv_upper"])
    assert Q(result["mean_lower"]) <= Q(result["mean_upper"])
    lo, hi = c.repetition_reference(model)
    assert Q(result["confidence_lower"]) < lo < hi < Q(result["confidence_upper"])
    assert result["prng_is_not_a_certified_fair_coin_source"]
    assert not result["partition_function_oracle_used"]


def test_interacting_block_extension_is_not_implicitly_accepted():
    with pytest.raises(TypeError):
        c.BlockModel(**{**small().__dict__, "quantum_couplings": (Q(1),)})
    model = c.repetition_model(3)
    # Add a ZZ interaction between two local spins and compare the actual TFD.
    h = dense_hamiltonian(model)+2*pauli("ZZIII")
    interacting = expm(-float(model.beta)*h/2)
    operator = pauli("IIIXX")
    actual = np.trace(interacting@operator@interacting@operator.T)/np.vdot(interacting, interacting)
    assert abs(actual-midpoint(c.repetition_reference(model))) > 1e-6


@pytest.mark.parametrize("change", [
    {"beta": -1}, {"beta": 0.1}, {"central_bits": True}, {"columns": (2,)},
    {"transverse": [1]}, {"longitudinal": (float("nan"),)},
])
def test_fail_closed_model_validation(change):
    with pytest.raises(ValueError):
        replace(small(), **change)


def test_invalid_observable_precision_and_sampling_inputs():
    with pytest.raises(ValueError):
        c.PairedEstimator(small(), c.PauliReadout("A", "X", "I", "I"))
    with pytest.raises(ValueError):
        c.local_factors(small(), 32)
    with pytest.raises(ValueError):
        c.PinSampler(small(), coin_bits=7)
    with pytest.raises(ValueError):
        c.estimate(small(), c.PauliReadout("X", "X", "I", "I"), 0, 1)
    with pytest.raises(ValueError):
        c.PairedEstimator(small(), c.PauliReadout("X", "X", "I", "I")).evaluate(2)


def test_saved_artifact_scope_and_reference():
    if not c.REPORT.exists():
        pytest.skip("live report not yet generated")
    report = json.loads(c.REPORT.read_text())
    assert report["model"]["calibration_not_hardness_evidence"] is True
    assert report["model"]["tfd_qubits"] == 510
    assert report["native"]["samples"] == 4096
    lo, hi = c.repetition_reference(c.repetition_model(128))
    saved = report["independent_even_parity_reference"]
    assert Q(saved["lower"]) == lo and Q(saved["upper"]) == hi
    assert Q(report["native"]["confidence_lower"]) <= lo <= hi <= Q(report["native"]["confidence_upper"])
    assert report["native"]["kernel_words_enumerated"] == 1
