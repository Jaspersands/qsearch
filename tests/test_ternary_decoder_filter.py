import itertools
from fractions import Fraction

import numpy as np
import pytest

from ternary_decoder_filter import (
    apply_local_readout, audit_filter, controlled_not_preparation, decoder_erasure,
    run_controls, signed_word_to_subset, trine_to_not_unitary,
    signed_word_to_target_witness, target_to_signed_labels,
)


def test_exact_local_unitary_maps_all_three_trines_with_correct_signed_phases():
    omega = np.exp(2j*np.pi/3)
    U = trine_to_not_unitary()
    assert np.max(abs(U.conj().T@U-np.eye(3))) < 1e-12
    for a in range(3):
        tau = np.asarray((0,omega**a,omega**(-a)))/np.sqrt(2)
        V = controlled_not_preparation(a)
        assert np.max(abs(V.conj().T@V-np.eye(3))) < 1e-12
        assert np.max(abs(U@tau-V[:,0])) < 1e-12


def test_erasure_is_a_unitary_permutation_on_arbitrary_input_not_just_planted_states():
    rng = np.random.default_rng(719)
    state = rng.normal(size=(27,9))+1j*rng.normal(size=(27,9))
    decoded = tuple(tuple(int(v) for v in row) for row in rng.integers(0,3,size=(27,2)))
    output = decoder_erasure(state,decoded)
    assert np.array_equal(decoder_erasure(output,decoded,inverse=True),state)
    assert abs(np.linalg.norm(output)-np.linalg.norm(state)) < 1e-12


def test_local_readout_matches_independent_full_tensor_product():
    rng = np.random.default_rng(7191)
    state = rng.normal(size=(27,3))+1j*rng.normal(size=(27,3))
    U = trine_to_not_unitary().conj().T
    explicit = np.kron(np.kron(U,U),U)@state
    assert np.max(abs(apply_local_readout(state,3)-explicit)) < 1e-12


def test_shear_is_IID_bijection_and_all_output_words_are_nonempty_valid_subsets():
    images = set()
    for a in itertools.product(range(3),repeat=3):
        H = a[:-1]+((a[-1]+sum(a[:-1])) % 3,)
        images.add(H)
        for c in itertools.product((1,2),repeat=3):
            if sum(x*y for x,y in zip(a,c)) % 3:
                continue
            returned,word = signed_word_to_subset((a,),c)
            assert returned == (H,) and word[-1] == 1
            assert sum(x*y for x,y in zip(H,word)) % 3 == 0
            assert all(v in (0,1) for v in word)
    assert len(images) == 27


def test_missing_solution_and_decoder_failures_are_not_silently_conditioned_away():
    row = audit_filter(((1,),))
    assert not row["verified_signed_witnesses"]
    assert row["executed_valid_signed_zero_sum_probability"] < 1e-12
    assert abs(row["unheralded_state_norm_squared"]-1) < 1e-12
    assert not row["failure_branches_discarded_or_renormalized"]
    assert row["decoder_basis_table_status_counts"]["MULTIPLE_BINARY_ERROR_SECRETS"] == 3


def test_complete_native_source_not_favorable_labels_satisfies_error_accounting():
    report = run_controls()
    source = report["complete_native_one_dimensional_source"]
    rows = source["all_source_instances_including_failures"]
    assert len(rows) == source["complete_IID_label_matrices"] == 81
    assert len({tuple(row["labels"][0]) for row in rows}) == 81
    assert source["no_signed_solution_source_instances"] == 8
    for row in rows:
        bound = row["pointwise_failure_probability_upper_bound"]
        bound = Fraction(bound["numerator"],bound["denominator"])
        assert 1-row["executed_valid_signed_zero_sum_probability"] <= float(bound)+1e-10
        assert abs(row["unheralded_state_norm_squared"]-1) < 1e-12
    vector = report["fixed_two_dimensional_source"]
    assert vector["dimension"] == 2 and vector["degree"] == 3
    assert vector["executed_valid_signed_zero_sum_probability"] > 0
    assert vector["exhaustive_classical_reference_finds_a_witness"]
    assert not vector["exhaustive_classical_reference_is_scalable_baseline"]
    assert not report["claim_gate"]["scalable_quantum_circuit_compiled"]
    assert not report["claim_gate"]["new_classical_quantum_separation_established"]


def test_global_bias_is_a_harmless_residual_translation_not_a_physical_failure():
    good = audit_filter(((1,1,1,1),))
    bad = audit_filter(((1,1,1,1),),decoder_offset=(1,))
    def error(row):
        value = row["exact_decoder_error_probability"]
        return Fraction(value["numerator"],value["denominator"])
    assert error(bad) > error(good)
    assert abs(bad["executed_valid_signed_zero_sum_probability"]-
               good["executed_valid_signed_zero_sum_probability"]) < 1e-12
    assert not bad["candidate_record_accepted"]
    assert not bad["speedup_claim_allowed"]


def test_no_decoder_control_exactly_matches_random_signed_guess_not_quantum_success():
    A = ((1,2,0,1),(2,0,1,1))
    row = audit_filter(A,3,decoder_mode="constant-zero")
    random = row["random_signed_guess_zero_sum_probability"]
    assert abs(row["executed_valid_signed_zero_sum_probability"]-
               float(Fraction(random["numerator"],random["denominator"]))) < 1e-12


@pytest.mark.parametrize("A", [(), ((3,),), ((True,),), ((1,),(1,),(1,)), ((1,)*7,), ((1,2),(1,))])
def test_invalid_or_unbudgeted_statevector_sources_rejected(A):
    with pytest.raises(ValueError):
        audit_filter(A)


def test_invalid_signed_word_rejected():
    with pytest.raises(ValueError):
        signed_word_to_subset(((1,1),),(0,1))
    with pytest.raises(ValueError):
        signed_word_to_subset(((1,),),(1,))


def test_specialized_target_wrapper_is_a_full_IID_bijection_without_marker_loss():
    images = set()
    successes = 0
    for a in itertools.product(range(3),repeat=3):
        for t in range(3):
            B = target_to_signed_labels((a,),(t,))
            images.add(B[0])
            for c in itertools.product((1,2),repeat=4):
                if sum(x*y for x,y in zip(B[0],c)) % 3:
                    continue
                word = signed_word_to_target_witness((a,),(t,),c)
                assert all(v in (0,1) for v in word)
                assert sum(x*y for x,y in zip(a,word)) % 3 == t
                successes += 1
    assert len(images) == 81 and successes > 0


def test_vector_target_witness_preserves_full_target_and_rejects_bad_inputs():
    A = ((1,2,0),(0,1,2))
    for t in itertools.product(range(3),repeat=2):
        B = target_to_signed_labels(A,t)
        for c in itertools.product((1,2),repeat=4):
            if any(sum(x*y for x,y in zip(row,c)) % 3 for row in B):
                continue
            word = signed_word_to_target_witness(A,t,c)
            assert all(sum(x*y for x,y in zip(row,word)) % 3 == target for row,target in zip(A,t))
    with pytest.raises(ValueError):
        target_to_signed_labels(A,(0,))
    with pytest.raises(ValueError):
        target_to_signed_labels(A,(0,True))
