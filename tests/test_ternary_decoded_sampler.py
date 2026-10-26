from fractions import Fraction
import hashlib
from itertools import product
import json
from math import sqrt

import numpy as np
import pytest

from theorems import ternary_decoded_sampler as audit
from theorems import ternary_coloring_bpqm as local


@pytest.mark.parametrize("row", ((1, 1, 1), (1, 2, 1), (2, 2, 1)))
@pytest.mark.parametrize("mu", (local.PHYSICAL, (Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)),
                               (Fraction(1, 3),)*3, (1, 0, 0)))
def test_actual_root_gate_matches_independent_CQ_bit_error_and_full_domain_unitarity(row, mu):
    code = audit.matrix_data((row,))
    _, states, words = audit.sources(code, mu)
    for root in range(3):
        T, recipe = audit.root_transform(mu, row, root)
        assert np.allclose(T.conj().T @ T, np.eye(27), atol=1e-12)
        observed = states @ T.T
        actual_error = np.mean([1-sum(abs(amp)**2 for y, amp in zip(product(range(3), repeat=3), psi)
                                    if y[root] == word[root]) for word, psi in zip(words, observed)])
        leaves = [j for j in range(3) if j != root]
        incoming = [tuple(mu) if (-row[j]*row[root]) % 3 == 1 else (mu[0], mu[2], mu[1]) for j in leaves]
        predicted_error = 0.
        for _, probability, conditional in local.check_branches(*incoming):
            combined = local.bit_spectrum(mu, conditional)
            predicted_error += float(probability)*(1-sum(sqrt(float(x)) for x in combined)**2/3)
        assert actual_error == pytest.approx(predicted_error, abs=1e-12)
        assert not recipe["herald_phase_removed_or_measured"]
        assert not recipe["dense_PGM_or_coset_probability_oracle_used"]


@pytest.mark.parametrize("mode", ("bpqm", "product", "none"))
def test_decoder_is_a_total_reversible_gate_program_including_dark_subspaces(mode):
    code = audit.matrix_data(((1, 1, 1),))
    decoder = audit.Decoder(code, local.PHYSICAL, mode=mode, offset=(2, 1))
    rng = np.random.default_rng(773)
    state = rng.normal(size=(2, 9, 27))+1j*rng.normal(size=(2, 9, 27))
    state /= np.linalg.norm(state)
    result = decoder.apply(state)
    assert np.linalg.norm(result) == pytest.approx(1)
    assert np.allclose(decoder.apply(result, inverse=True), state, atol=1e-12)


def test_label_subtraction_is_modular_not_binary_and_never_erases_failures():
    labels = tuple(product(range(3), repeat=2))
    for u, a in enumerate(labels):
        for r, b in enumerate(labels):
            state = np.zeros((9, 9, 1), complex)
            state[u, r, 0] = 1
            actual = audit.subtract_label(state, labels)
            target = audit.index(tuple((x-y) % 3 for x, y in zip(a, b)))
            assert actual[target, r, 0] == 1
            assert np.linalg.norm(actual) == 1


def test_comparison_is_the_direct_UNNORMALIZED_sum_not_a_prepared_conditional_state():
    code = audit.matrix_data(((1, 1, 1),))
    decoder = audit.Decoder(code, local.PHYSICAL)
    _, states, words = audit.sources(code, local.PHYSICAL)
    norms = []
    for J in product(range(3), repeat=3):
        actual, ideal = audit.circuit(code, decoder, J)
        direct = sum(local.OMEGA**(-sum(a*b for a, b in zip(d, J)))*psi
                     for d, psi in zip(words, states))/3
        assert np.allclose(ideal[0, 0], direct, atol=1e-12)
        assert np.linalg.norm(actual) == pytest.approx(1)
        norms.append(float(np.linalg.norm(ideal)**2))
    assert max(norms) == pytest.approx(2.25)
    assert sum(x < 1e-12 for x in norms) == 6
    assert np.mean(norms) == pytest.approx(1)


@pytest.mark.parametrize("mu", (local.PHYSICAL, (Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)), (1, 0, 0)))
def test_source_preparation_uses_actual_public_local_gates_not_a_conditional_amplitude_oracle(mu):
    code = audit.matrix_data(((1, 2, 1),))
    _, states, words = audit.sources(code, mu)
    for J in ((0, 0, 0), (1, 2, 1), (2, 0, 1)):
        prepared = audit.prepare_source(code, mu, J)
        expected = np.zeros_like(prepared)
        for u, (d, psi) in enumerate(zip(words, states)):
            expected[u, 0] = local.OMEGA**(-sum(a*b for a, b in zip(d, J)))*psi/3
        assert np.allclose(prepared, expected, atol=1e-12)
        assert np.linalg.norm(prepared) == pytest.approx(1)


@pytest.mark.parametrize("mode,mu", (("bpqm", local.PHYSICAL), ("none", local.PHYSICAL),
                                    ("product", local.PHYSICAL),
                                    ("bpqm", (Fraction(1, 4), Fraction(3, 8), Fraction(3, 8)))))
def test_full_original_offset_population_obeys_the_reduction_identity(mode, mu):
    record = audit.audit_case(((1, 1, 1),), mu, mode=mode)
    assert record["Parseval_identity_residual_numeric"] < 1e-12
    assert record["mean_full_state_distance_squared_numeric"] == pytest.approx(2*record["mean_word_error_numeric"])
    assert len(record["all_original_offset_rows"]) == 27
    assert not record["scalable_whole_LDPC_receiver_compiled"]
    assert not record["speedup_claim_allowed"]
    for row in record["all_original_offset_rows"]:
        assert row["actual_total_probability_numeric"] == pytest.approx(1)
        assert not row["postselection_or_retries_used"]
        if row["target_empty"]:
            assert row["invalid_output_ABSTAIN_probability_numeric"] == pytest.approx(1)
            assert row["unconditional_TV_with_ABSTAIN_numeric"] < 1e-12


def test_NO_decoder_is_exactly_the_same_input_classical_product_proposal():
    record = audit.audit_case(((1, 1, 1),), mode="none")
    assert max(r["same_input_classical_shadow_TV_from_actual_numeric"] for r in record["all_original_offset_rows"]) < 1e-12
    assert record["mean_valid_native_output_probability_numeric"] == pytest.approx(1/9)
    assert record["empty_original_offset_fraction_exact"] == "2/9"
    # Do not omit the STRONGER elementary original-spin rejection proposal.
    assert record["uniform_spin_rejection_mean_acceptance_exact"] == "8/27"
    assert record["product_then_affine_solve_mean_acceptance_exact"] == "1/9"


def test_constant_decoder_error_is_not_necessary_for_good_sampling():
    code = audit.matrix_data(((1, 1, 1),))
    good = audit.Decoder(code, local.PHYSICAL)
    shifted = audit.Decoder(code, local.PHYSICAL, offset=(1, 0))
    assert np.mean(audit.word_errors(code, shifted)) > np.mean(audit.word_errors(code, good))+.4
    for J in product(range(3), repeat=3):
        first, _ = audit.circuit(code, good, J)
        second, _ = audit.circuit(code, shifted, J)
        assert np.allclose((abs(first)**2).sum(axis=(0, 1)), (abs(second)**2).sum(axis=(0, 1)), atol=1e-12)


def test_wrong_adjoint_passes_norm_but_fails_the_mathematical_identity():
    record = audit.audit_case(((1, 1, 1),), wrong_adjoint=True)
    assert all(abs(row["actual_total_probability_numeric"]-1) < 1e-12 for row in record["all_original_offset_rows"])
    assert record["Parseval_identity_residual_numeric"] > .5


def test_dependent_zero_rows_and_uniform_gauge_lift_do_not_change_the_native_problem():
    record = audit.audit_case(((1, 2, 1), (2, 1, 2), (0, 0, 0)))
    assert record["original_row_rank"] == 1 and record["gauge_dimension"] == 2
    assert record["dependent_and_zero_rows_retained"]
    code = audit.matrix_data(((1, 2, 1), (2, 1, 2), (0, 0, 0)))
    decoder = audit.Decoder(code, local.PHYSICAL)
    state, _ = audit.circuit(code, decoder, (0, 0, 0))
    actual, target, partition = audit.native_distribution(code, local.PHYSICAL, (0, 0, 0), (abs(state)**2).sum(axis=(0, 1)))
    assert partition > 0 and len(target) == 28
    nonzero = target[target > 0]
    assert np.allclose(nonzero, np.ones(len(nonzero))/len(nonzero))
    assert sum(actual) == pytest.approx(1)


@pytest.mark.parametrize("rows", (((1, 1, 1),), ((1, 2, 1), (2, 1, 2), (0, 0, 0)), ((1, 1, 0),)))
def test_polynomial_Gaussian_postprocessor_matches_an_independent_complete_fiber_census(rows):
    code = audit.matrix_data(rows)
    for target in product(range(3), repeat=3):
        exact = {x for x in product(range(3), repeat=len(rows))
                 if all(sum(row[e]*value for row, value in zip(rows, x)) % 3 == t for e, t in enumerate(target))}
        actual = [audit.affine_lift(rows, target, coins)
                  for coins in product(range(3), repeat=code["gauge_dimension"])]
        if exact:
            assert set(actual) == exact and len(actual) == len(exact)
        else:
            assert all(x is None for x in actual)


def test_gaussian_postprocessing_does_not_inherit_the_exponential_quantum_reference_cap():
    rows = tuple(tuple(int(j == i) if j < 32 else (int(i == (j-32) % 32)+int(i == (j-31) % 32)) % 3
                       for j in range(64)) for i in range(32))
    x = tuple(i % 3 for i in range(32))
    target = tuple(sum(row[e]*value for row, value in zip(rows, x)) % 3 for e in range(64))
    assert audit.affine_lift(rows, target, ()) == x


@pytest.mark.parametrize("call", (
    lambda: audit.matrix_data(((1, 1, 1, 1),)),
    lambda: audit.matrix_data(((1, True, 0),)),
    lambda: audit.Decoder(audit.matrix_data(((1, 1, 0),)), local.PHYSICAL, mode="bpqm"),
    lambda: audit.root_transform(local.PHYSICAL, (1, 0, 1), 0),
))
def test_unimplemented_or_invalid_domains_cannot_be_promoted(call):
    with pytest.raises(ValueError):
        call()


def test_live_report_is_source_bound_and_does_not_claim_the_natural_large_sampler():
    report = json.loads(audit.REPORT.read_text())
    for path, digest in report["source_sha256"].items():
        assert digest == hashlib.sha256((audit.ROOT/path).read_bytes()).hexdigest()
    assert not report["natural_3_6_LDPC_sampler_executed"]
    assert not report["local_reduction_proof_independently_reviewed"]
    assert len(report["cases"]) == 7
