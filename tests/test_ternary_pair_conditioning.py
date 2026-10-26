from fractions import Fraction
from itertools import product
from math import prod

import numpy as np
import pytest

from theorems import ternary_pair_conditioning as conditioning
from theorems.ternary_coloring_bpqm import PHYSICAL
from theorems.ternary_decoded_sampler import index, matrix_data, root_transform


@pytest.mark.parametrize("mus", [(PHYSICAL,)*4,
    ((Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)), PHYSICAL, (0, 1, 0), (Fraction(1, 3),)*3)])
def test_exact_original_spin_weights_and_unique_local_fibers_for_every_offset(mus):
    H = ((1, 1, 0, 0), (0, 0, 1, 1))
    for J in product(range(3), repeat=4):
        plan = conditioning.PairConditioning.build(H, mus, J, ((0, 1), (2, 3)))
        for x in product(range(3), repeat=2):
            full = tuple((j+sum(row[e]*value for row, value in zip(H, x))) % 3 for e, j in enumerate(J))
            short = tuple((j+sum(row[e]*value for row, value in zip(plan.H, x))) % 3 for e, j in enumerate(plan.offsets))
            assert plan.expand(short) == full
            assert plan.compress(full) == short
            original = prod(Fraction(mu[y]) for mu, y in zip(mus, full))
            if plan.spectra is None:
                assert original == 0
            else:
                reduced = prod(mu[y] for mu, y in zip(plan.spectra, short))
                assert original == prod(plan.local_masses)*reduced


@pytest.mark.parametrize("t", range(3))
def test_actual_SUM_expansion_preserves_arbitrary_complex_coherence(t):
    plan = conditioning.PairConditioning.build(((1, 0, 1, 0), (0, 1, 0, 1)), (PHYSICAL,)*4, (t, 1, 0, 2), ((0, 2), (3, 1)))
    rng = np.random.default_rng(817)
    state = rng.normal(size=(2, 3, 9))+1j*rng.normal(size=(2, 3, 9))
    state /= np.linalg.norm(state)
    expanded = plan.expand_state(state)
    reference = np.zeros((2, 3, 81), complex)
    for i, word in enumerate(product(range(3), repeat=2)):
        reference[:, :, index(plan.expand(word))] = state[:, :, i]
    assert np.max(abs(expanded-reference)) < 1e-15
    assert np.linalg.norm(expanded) == pytest.approx(1)
    U = conditioning.pair_gate(t)
    assert np.array_equal(U.conj().T@U, np.eye(9))


def test_overlapping_or_wrong_pairs_and_noncanonical_data_rejected():
    H = ((1, 1, 1, 0), (0, 0, 0, 1))
    for pairs in (((0, 1), (1, 2)), ((0, 3),), ((1, 1),), ((-1, 2),), ((0, True),)):
        with pytest.raises(ValueError):
            conditioning.PairConditioning.build(H, (PHYSICAL,)*4, (0,)*4, pairs)
    with pytest.raises(ValueError):
        conditioning.PairConditioning.build(((True, 1),), (PHYSICAL,)*2, (0, 0), ((0, 1),))
    with pytest.raises(ValueError):
        conditioning.PairConditioning.build(((1, 1),), (PHYSICAL,), (0, 0), ((0, 1),))
    plan = conditioning.PairConditioning.build(((1, 1),), (PHYSICAL,)*2, (0, 1), ((0, 1),))
    with pytest.raises(ValueError):
        plan.compress((1, 1))
    with pytest.raises(ValueError):
        plan.expand((True,))


def test_zero_local_mass_is_a_real_empty_target_not_renormalized():
    plan = conditioning.PairConditioning.build(((1, 1),), ((1, 0, 0), (1, 0, 0)), (0, 1), ((0, 1),))
    assert plan.local_masses == (0,)
    assert plan.spectra is None


@pytest.mark.parametrize("check", ((1, 1, 1), (1, 2, 1), (2, 1, 2)))
def test_heterogeneous_recipe_recovers_prior_homogeneous_actual_gates(check):
    for root in range(3):
        old, _ = root_transform(PHYSICAL, check, root)
        new = conditioning.heterogeneous_root((PHYSICAL,)*3, check, root)
        assert np.max(abs(old-new)) < 1e-14


@pytest.mark.parametrize("mus", ((PHYSICAL, (1, 0, 0), PHYSICAL),
    ((Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)), PHYSICAL, (0, 0, 1))))
def test_heterogeneous_dark_completions_are_unitary_and_decoder_inverse_is_total(mus):
    code = matrix_data(((1, 2, 1),))
    decoder = conditioning.ResidualDecoder(code, mus)
    for _, T in decoder.transforms:
        assert np.max(abs(T.conj().T@T-np.eye(27))) < 2e-14
    rng = np.random.default_rng(1817)
    state = rng.normal(size=(4, 9, 27))+1j*rng.normal(size=(4, 9, 27))
    state /= np.linalg.norm(state)
    roundtrip = decoder.apply(decoder.apply(state), inverse=True)
    assert np.max(abs(roundtrip-state)) < 2e-14
    assert decoder.mu is None


@pytest.mark.parametrize("mode", ("bpqm", "product", "none"))
@pytest.mark.parametrize("t", range(3))
def test_full_sampler_conditional_identity_native_output_and_classical_comparator(mode, t):
    result = conditioning.audit(t, mode=mode)
    assert result["conditional_Parseval_residual"] < 1e-12
    assert result["conditional_average_TV"] <= result["conditional_TV_bound"]+1e-12
    assert result["matched_classical_mean_acceptance"] == pytest.approx(1/9)
    assert len(result["cases"]) == 27
    assert not result["rare_event_postselection_used"]
    for case in result["cases"]:
        assert case["source_preparation_residual"] < 1e-14
        assert case["actual_norm_squared"] == pytest.approx(1)
        assert sum(case["actual_native_output_including_ABSTAIN"]) == pytest.approx(1)
        if case["target_empty"]:
            assert case["actual_native_output_including_ABSTAIN"][-1] == pytest.approx(1)
            assert case["classical_conditional_TV_when_nonempty"] is None
        else:
            assert case["classical_conditional_TV_when_nonempty"] < 1e-12
        if mode == "none":
            assert np.max(abs(np.array(case["actual_native_output_including_ABSTAIN"])-case["classical_native_output_including_ABSTAIN"])) < 1e-12


def test_wrong_adjoint_and_residual_adaptivity_are_independently_detected():
    wrong = conditioning.audit(0, wrong_adjoint=True)
    assert wrong["conditional_Parseval_residual"] > .1
    assert all(abs(c["actual_norm_squared"]-1) < 1e-12 for c in wrong["cases"])
    adaptive = conditioning.adaptive_countercontrol()
    assert adaptive["average_Parseval_identity_failure"] > .08


def test_pair_source_rotations_equal_exact_conditional_product_without_rejection():
    for t in range(3):
        plan = conditioning.PairConditioning.build(((1, 1, 1, 1),), (PHYSICAL,)*4, (t, 0, 0, 0), ((0, 1),))
        code = matrix_data(plan.H)
        _, _, phi, _, _ = conditioning.source_arrays(code, plan.spectra)
        actual = plan.expand_state(phi)
        expected = []
        for word in product(range(3), repeat=4):
            mass = prod(mu[y] for mu, y in zip(plan.original_spectra, word))
            expected.append(float(mass/plan.local_masses[0]) if (word[0]-word[1]) % 3 == t else 0.)
        assert np.max(abs(abs(actual)**2-expected)) < 1e-15


def test_native_inventory_preserves_saved_sources_and_does_not_claim_a_decoder():
    inventory = conditioning.native_inventory()
    assert [len(c["disjoint_duplicate_pairs"]) for c in inventory] == [1, 0]
    assert [c["residual_decoding_dimension"] for c in inventory] == [15, 32]
    assert all(not c["generic_residual_decoder_supplied"] for c in inventory)
    assert all(not c["quantum_receiver_executed_on_native_input"] for c in inventory)
