from fractions import Fraction
from itertools import product
import random

import numpy as np
import pytest

from ternary_incidence_decoder import IncidenceDecoder, IncidenceSample
from ternary_likelihood_gate import (
    centered_characters, dense_gram_control, exact_centered_gram,
    likelihood_ratio, likelihood_spectrum, observation_gate, run_controls, sq_gate,
)


@pytest.mark.parametrize("n,q", [(1, 3), (1, 9), (2, 3), (1, 27)])
def test_every_born_record_has_exact_orthogonal_centered_likelihood(n, q):
    record = dense_gram_control(n, q)
    assert record["complete_public_label_basis_outcome_records"] == 9*q**(2*n)
    assert record["maximum_orthogonality_error"] < 1e-12
    assert np.allclose(record["centered_Gram_matrix"], 2/3*np.eye(q**n), atol=1e-12)


@pytest.mark.parametrize("q", [3, 9, 3**16])
def test_character_compiler_distinguishes_all_secrets_including_zero_and_negations(q):
    secrets = [(0, 0), (1, 2), (q-1, q-2), (3 % q, 0), (q//3, 0)]
    for s, t in product(secrets, repeat=2):
        assert len(set(centered_characters(s, q))) == 6
        assert exact_centered_gram(s, t, q) == (Fraction(2, 3) if s == t else 0)


def test_sparse_spectrum_is_the_actual_positive_born_likelihood_not_a_field_shadow():
    rng = random.Random(63010)
    for q in (3, 9, 81):
        for _ in range(40):
            a, c, secret = [tuple(rng.randrange(q) for _ in range(2)) for _ in range(3)]
            b, o = rng.randrange(3), rng.randrange(3)
            terms = likelihood_spectrum(a, c, q, b, o)
            value = sum(float(scale)*np.exp(2j*np.pi*(sum(x*s for x, s in zip(frequency, secret))/q+phase/3))
                        for frequency, phase, scale in terms)
            assert abs(value.imag) < 1e-12
            assert abs(value.real-likelihood_ratio(a, c, secret, q, b, o)) < 1e-12


def test_sq_ledger_charges_tolerance_arity_and_does_not_claim_classical_hardness():
    for k in (1, 2, 4, 64):
        gate = sq_gate(8, 2, 100, Fraction(1, 32), k)
        d = Fraction(5, 3)**k-1
        affected = d//Fraction(1, 32)**2
        assert Fraction(gate["centered_likelihood_norm_squared"]) == d
        assert Fraction(gate["uniform_secret_identification_success_upper"]) == min(Fraction(1), Fraction(100*affected+1, 3**16))
        assert not gate["raw_samples_or_growing_arity_joint_inference_ruled_out"]
        assert not gate["general_classical_hardness_proved"]
    assert Fraction(sq_gate(8, 2, 100, Fraction(1, 32), 64)["uniform_secret_identification_success_upper"]) == 1


def test_raw_field_samples_decode_the_same_SQ_hard_distribution():
    report = run_controls()
    easy = report["raw_sample_field_decoder_counterexample"]
    decoder = IncidenceDecoder(easy["dimension"])
    for s in easy["public_measurement_records"]:
        decoder.add(IncidenceSample(tuple(s["alpha"]), tuple(s["beta"]), s["basis"], s["outcome"]))
    assert decoder.result()["status"] == "FIELD_SECRET_CERTIFIED"
    assert decoder.result()["secret"] == easy["result"]["secret"]
    assert not report["claim_gate"]["general_classical_hardness"]


def test_unlimited_likelihood_processing_density_converse_and_surplus_scope():
    for n, r in ((1, 1), (8, 1), (32, 4)):
        near = observation_gate(n, r, n*r)
        assert Fraction(near["uniform_secret_success_squared_upper"]) == Fraction(5, 9)**(n*r)
        surplus = observation_gate(n, r, 4*n*r)
        assert Fraction(surplus["uniform_secret_success_squared_upper"]) == 1
        assert not surplus["efficient_decoding_above_threshold_proved"]
        assert not near["arbitrary_or_collective_quantum_measurements_covered"]


@pytest.mark.parametrize("args", [(0, 1, 1, Fraction(1, 10)), (1, True, 1, Fraction(1, 10)),
                                  (1, 1, -1, Fraction(1, 10)), (1, 1, 1, .1), (1, 1, 1, Fraction(0))])
def test_invalid_statistical_query_ledgers_are_rejected(args):
    with pytest.raises(ValueError):
        sq_gate(*args)


def test_validation_does_not_coerce_secrets_or_expand_unbounded_dense_source():
    for s in ((True,), (3,), (), (1.0,)):
        with pytest.raises(ValueError):
            centered_characters(s, 3)
    with pytest.raises(ValueError):
        dense_gram_control(8, 3)
    with pytest.raises(ValueError):
        likelihood_spectrum((1,), (2,), 3, 0, True)


def test_complete_two_record_gram_and_optimal_classical_decoder_obey_density_bound():
    secrets = [(0,), (1,), (2,)]
    ratios = np.array([[likelihood_ratio((a,), (c,), s, 3, b, o) for s in secrets]
                       for a, c, b, o in product(range(3), repeat=4)])
    for k in (1, 2):
        joint = ratios if k == 1 else (ratios[:, None, :]*ratios[None, :, :]).reshape(-1, 3)
        centered = joint-1
        assert np.allclose(centered.T@centered/len(centered), (float(Fraction(5, 3)**k)-1)*np.eye(3), atol=1e-12)
        optimum = float(np.mean(np.max(joint, axis=1)))/3
        certificate = observation_gate(1, 1, k)
        assert optimum**2 <= float(Fraction(certificate["uniform_secret_success_squared_upper"]))+1e-12


def test_Bessel_screen_for_independent_bounded_real_queries_on_full_record_domain():
    secrets = [(0,), (1,), (2,)]
    g = np.array([[likelihood_ratio((a,), (c,), s, 3, b, o)-1 for s in secrets]
                  for a, c, b, o in product(range(3), repeat=4)])
    rng = np.random.default_rng(63190)
    queries = [np.sign(g[:, j]) for j in range(3)]+[rng.uniform(-1, 1, size=len(g)) for _ in range(30)]
    for h in queries:
        delta = h@g/len(g)
        assert sum(delta**2) <= (2/3)*float(np.mean(h**2))+1e-12
