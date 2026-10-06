import math
from fractions import Fraction

import pytest

from dcp_adaptive_product_readout_bound import (
    _fiber_control, bounded_control, coefficient_weight, general_policy,
    parity_policy, refine_equatorial, run_controls, source_certificate,
)


def read(row):
    return Fraction(int(row["numerator_hex"],16),int(row["denominator_hex"],16))


@pytest.mark.parametrize("outcomes",[
    [(0.5,0.6,0,0.2),(0.5,-0.6,0,-0.2)],
    [(1/3,math.cos(2*math.pi*k/3),math.sin(2*math.pi*k/3),0) for k in range(3)],
    [(0.25,x/math.sqrt(3),y/math.sqrt(3),z/math.sqrt(3))
     for x,y,z in ((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))],
    [(0.25,1,0,0),(0.75,-1/3,0,0)],
    [(1,0,0,0)],
])
def test_equatorial_refinement_preserves_each_coarse_phase_probability(outcomes):
    rows,mapping = refine_equatorial(outcomes)
    assert all(abs(r[1]**2+r[2]**2-1)<1e-10 and r[3]==0 for r in rows)
    for theta in (0,0.2,1.7,4.3):
        for index,e in enumerate(outcomes):
            actual = sum(r[0]*(1+r[1]*math.cos(theta)+r[2]*math.sin(theta))
                         for r,k in zip(rows,mapping) if k==index)
            assert actual==pytest.approx(e[0]*(1+e[1]*math.cos(theta)+e[2]*math.sin(theta)))


def test_feedback_keeps_earlier_odd_terms_but_cancels_latest_linear_terms():
    row = bounded_control([[2,1]],4,parity_policy)
    coefficients = {tuple(r["delta"]):complex(r["real"],r["imaginary"]) for r in row["refined_fourier_coefficients"]}
    assert abs(coefficients[(1,2)])>0.1
    for delta,v in coefficients.items():
        nonzero = [a for a in delta if a]
        if nonzero and abs(nonzero[-1])==1:
            assert abs(v)<1e-9
    assert row["evaluations"][0]["optimal_classical_record_success"]==pytest.approx(1)
    assert read(row["fixed_matrix_refined_collision_envelope"])==4
    assert not row["efficient_decoder_claim"]


def test_coarse_history_is_retained_and_refinement_cannot_reduce_success_or_collision():
    row = bounded_control([[1,3,7]],8,general_policy)
    coarse,refined = row["evaluations"]
    assert refined["tree_leaves"]>coarse["tree_leaves"]
    assert coarse["weighted_collision"]<=refined["weighted_collision"]+1e-9
    assert coarse["optimal_classical_record_success"]<=refined["optimal_classical_record_success"]+1e-9
    assert {tuple(r["coarse_history"]) for r in refined["leaf_reference_probabilities_and_effects"]}=={
        tuple(r["coarse_history"]) for r in coarse["leaf_reference_probabilities_and_effects"]}


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_complete_censuses_verify_feedback_envelope_and_collective_moments(report):
    rows = report["complete_source_envelopes"]
    assert [r["complete_label_matrices"] for r in rows]==[16,512,256]
    assert [read(r["exact_mean_collision_envelope"]) for r in rows]==[Fraction(27,8),Fraction(175,32),Fraction(11,4)]
    for row in rows:
        mu = Fraction(2**row["m"],row["q"]**row["n"])
        second = mu**2+mu*(1-Fraction(1,row["q"]**row["n"]))
        assert read(row["exact_mean_uniform_target_fiber_second_moment"])==second
        assert row["actual_source_mean_collective_PGM_success"]>=float(mu**2/second)-1e-9


def test_exact_entropy_width_comparison_and_sample_surplus_limit(report):
    rows = report["growing_ledgers"]
    for row in rows:
        delta = row["density_surplus"]
        assert row["collective_lower_exceeds_adaptive_upper"]==(delta==0)
        assert row["bound_is_vacuous"]==(delta>=2)
        if delta==0:
            assert read(row["collective_PGM_source_mean_success_lower_bound"])>Fraction(1,2)
            assert read(row["unclamped_source_mean_success_squared_envelope"])<Fraction(1,4)
        assert not row["label_adaptive_ordering_revisiting_or_quantum_memory_covered"]
        assert not row["collective_PGM_efficient_implementation_supplied"]
        assert not row["speedup_claim_allowed"]
    assert not any(report["claim_gate"].values())


def test_order_two_source_exception_is_vacuous_not_an_asymptotic_separation():
    row = source_certificate(8,1,8)
    assert row["bound_is_vacuous"]
    assert not row["collective_lower_exceeds_adaptive_upper"]


def test_zero_and_injective_fibers_have_correct_PGM_controls():
    assert _fiber_control([[0,0]],4)==(Fraction(1),Fraction(4),0.25)
    first,second,pgm = _fiber_control([[2,1]],4)
    assert first==second==1 and pgm==pytest.approx(1)


@pytest.mark.parametrize("args",[(0,2,2),(1,0,2),(1,2,0),(True,2,2),(1,2,2.0)])
def test_invalid_source_parameters_rejected(args):
    with pytest.raises(ValueError):
        source_certificate(*args)


@pytest.mark.parametrize("A,q",[([],4),([[]],4),([[1],[1,2]],4),([[True]],4),([[4]],4),([[1]],3),([[1]],True),([[1]],4.0)])
def test_malformed_native_controls_rejected(A,q):
    with pytest.raises(ValueError):
        bounded_control(A,q,general_policy)


def test_invalid_fourier_frequencies_and_incomplete_POVMs_rejected():
    for delta in ((3,),(True,),(0.0,)):
        with pytest.raises(ValueError):
            coefficient_weight(delta)
    with pytest.raises(ValueError):
        bounded_control([[1]],4,lambda A,h:[(0.5,1,0,0)])
