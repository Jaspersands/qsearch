"""Physical nonlinear filter vs exact classical block sampling and falsifiers."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random
import subprocess

import numpy as np
import pytest

from ternary_decoder_filter import (
    audit_filter,decoder_erasure,apply_local_readout,linear_erasure_reference,_index,
)
from ternary_syndrome_correction import (
    SyndromeQuadratic,conditional_block,sample_classical,complete_classical_reference,
    physical_comparison,canonical_kernel_rows,fixed_cross_correction,run_controls,
    twirled_conditional_block,random_full_syndrome_success_bound,
)

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT/"research/certificates/ternary_decoder_filter_crosscheck.js"


def fraction(record):
    return Fraction(record["numerator"],record["denominator"])


@pytest.fixture(scope="module")
def report():
    return run_controls()


def program():
    return SyndromeQuadratic(((1,1,1),),((1,2,0),(1,0,2)),((0,1,0),))


def test_nonlinearity_can_raise_finite_success_but_not_beat_its_classical_sampler(report):
    control = report["controls"][2]
    assert fraction(control["exact_classical_signed_success"]) == Fraction(7,12)
    assert fraction(control["linear_free_sign_baseline_success"]) == Fraction(1,2)
    assert fraction(control["finite_gain_over_linear_baseline"]) == Fraction(1,12)
    assert not control["quantum_advantage_from_this_gain"]
    # The calibration itself is easy: this public signed word is deterministic.
    assert report["easy_control_has_deterministic_classical_signed_witness"] == (1,1,1)


def test_all_27_policies_include_failures_no_optimization_cost_hidden(report):
    policies = report["all_27_quadratic_policies_on_one_easy_control"]
    assert len(policies) == len({tuple(row["public_coefficients"]) for row in policies}) == 27
    assert max(fraction(row["success"]) for row in policies) == Fraction(7,12)
    assert min(fraction(row["success"]) for row in policies) == Fraction(1,4)
    assert not report["quadratic_policy_optimization_is_free_or_scalable"]


def test_complete_IID_source_includes_zero_rank_and_losing_instances(report):
    census = report["complete_one_row_IID_source_census"]
    cases = census["all_source_cases"]
    assert len(cases) == census["all_IID_label_matrices"] == 27
    assert len({tuple(c["labels"][0]) for c in cases}) == 27
    assert sum(c["rank_zero_classical_fallback"] for c in cases) == 1
    assert fraction(census["mean_success"]) == sum((fraction(c["unconditional_success"]) for c in cases),Fraction())/27
    assert not census["favorable_source_selection"]
    assert not census["large_rank_success_proved"]
    assert all(c["actual_quantum_comparison_error"] < 1e-12 for c in cases)


@pytest.mark.parametrize("R", [None,((1,),(1,),(2,))])
@pytest.mark.parametrize("C", [(0,0,0),(1,0,0),(0,1,0),(1,2,1)])
def test_actual_full_word_and_residual_Fourier_joint_law(C,R):
    P = SyndromeQuadratic(((1,1,1),),((1,2,0),(1,0,2)),(C,),R)
    m,n = 3,1
    values = tuple(product(range(3),repeat=m))
    secrets = tuple(product(range(3),repeat=n))
    table = [P.decode(b) for b in values]
    source = np.zeros((3**m,3**n),complex)
    for si,s in enumerate(secrets):
        for e in product((1,2),repeat=m):
            b = tuple((a*s[0]+x) % 3 for a,x in zip(P.labels[0],e))
            source[_index(b),si] = (-1)**sum(x == 2 for x in e)/np.sqrt(3**n*2**m)
    output = apply_local_readout(decoder_erasure(source,table),m)
    F = np.array([[np.exp(2j*np.pi*x*y/3)/np.sqrt(3) for y in range(3)] for x in range(3)])
    actual = abs(output@F.T)**2
    predicted = np.zeros_like(actual)
    for e in product((1,2),repeat=m):
        block = conditional_block(P,e)
        z = _index(block["computed_residual_Fourier_label"])
        for row in block["outcomes"]:
            predicted[_index(row["word"]),z] += row["integer_weight"]/block["weight_denominator"]/2**m
    np.testing.assert_allclose(actual,predicted,atol=1e-13)
    assert abs(actual.sum()-1) < 1e-13


@pytest.mark.parametrize("e", list(product((1,2),repeat=3)))
def test_integer_block_weights_are_normalized_and_anchor_independent(e):
    P = program()
    block = conditional_block(P,e)
    law = {row["word"]: Fraction(row["integer_weight"],block["weight_denominator"]) for row in block["outcomes"]}
    assert all(type(row["integer_weight"]) is int and row["integer_weight"] >= 0 for row in block["outcomes"])
    assert sum(law.values()) == 1
    for shift in product(range(3),repeat=2):
        other = tuple((x+sum(c*h[j] for c,h in zip(shift,P.kernel_rows))) % 3 for j,x in enumerate(e))
        if not all(other):
            continue
        other_block = conditional_block(P,other)
        other_law = {row["word"]: Fraction(row["integer_weight"],other_block["weight_denominator"]) for row in other_block["outcomes"]}
        assert law == other_law


def test_quadratic_program_is_covariant_without_seeing_the_secret():
    P = program()
    for b in product(range(3),repeat=3):
        for s in range(3):
            shifted = tuple((x+s*a) % 3 for x,a in zip(b,P.labels[0]))
            assert P.decode(shifted) == tuple((v+s) % 3 for v in P.decode(b))


def test_zero_rank_block_reproduces_the_previous_linear_baseline():
    A = ((1,0,1,2),(0,1,2,2))
    P = SyndromeQuadratic(A,(),((),()))
    assert complete_classical_reference(P) == {
        word: Fraction(count,2**4) for word,count in linear_erasure_reference(A)["all_output_counts"].items()}


def test_exact_sampler_includes_failed_outputs_not_success_conditioning():
    P = SyndromeQuadratic(((1,1,1),),((1,2,0),),((1,),))
    class Coins:
        def __init__(self,values): self.values = iter(values)
        def randrange(self,upper):
            value = next(self.values)
            assert 0 <= value < upper
            return value
    law = {}
    for e in product((1,2),repeat=3):
        block = conditional_block(P,e)
        total = block["weight_denominator"]
        for draw in range(total):
            row = sample_classical(P,rng=Coins([x-1 for x in e]+[draw]))
            word = row["word"]
            law[word] = law.get(word,Fraction())+Fraction(1,8*total)
            assert not row["postselection_on_valid_signed_witness"]
    assert law == {x:p for x,p in complete_classical_reference(P).items() if p}
    assert any(not all(word) and p for word,p in law.items())


def test_large_explicit_classical_sampler_never_calls_a_quantum_or_exhaustive_reference(monkeypatch):
    import ternary_syndrome_correction as module
    n,m = 32,96
    A = tuple(tuple(int(i == j) if j < n else (i*j+i+j) % 3 for j in range(m)) for i in range(n))
    H = canonical_kernel_rows(A)[:2]
    P = SyndromeQuadratic(A,H,((0,1,0),)*n)
    def forbidden(*args,**kwargs): raise AssertionError("unpaid quantum state or exhaustive reference")
    original = module.product
    def bounded(*args,**kwargs):
        assert kwargs.get("repeat",0) <= 2
        return original(*args,**kwargs)
    monkeypatch.setattr(module,"audit_filter",forbidden)
    monkeypatch.setattr(module,"complete_classical_reference",forbidden)
    monkeypatch.setattr(module,"product",bounded)
    result = sample_classical(P,rng=random.Random(720813))
    assert all(sum(x*y for x,y in zip(row,result["word"])) % 3 == 0 for row in A)
    assert result["source_sign_bits_charged"] == m
    assert result["block_size_charged"] == 9


@pytest.mark.parametrize("H,C", [
    (((1,0,0),),((1,),)), (((1,2,0),(2,1,0)),((1,0,0),)),
    (((1,2),),((1,),)), (((True,2,0),),((1,),)),
    (((1,2,0),),((True,),)), (((1,2,0),),((1,2),)),
])
def test_invalid_or_noncovariant_programs_fail_closed(H,C):
    with pytest.raises(ValueError): SyndromeQuadratic(((1,1,1),),H,C)


def test_typed_source_binding_and_resource_caps_fail_closed():
    P = program()
    with pytest.raises(ValueError): conditional_block(P,(1,1,1),cap=3)
    with pytest.raises(ValueError): conditional_block(P,(1,0,2))
    with pytest.raises(ValueError): sample_classical(object())
    with pytest.raises(ValueError): complete_classical_reference(P,sign_cap=4)
    with pytest.raises(ValueError): audit_filter(((1,1,2),),decoder_mode="quadratic-syndrome",syndrome_correction=P)
    with pytest.raises(ValueError): audit_filter(P.labels,syndrome_correction=P)


def test_public_program_is_rebuilt_not_an_untrusted_decoder_callback():
    P = program()
    class Pretend:
        labels,kernel_rows,coefficients,right_inverse = P.labels,P.kernel_rows,P.coefficients,P.right_inverse
        def decode(self,b): raise AssertionError("unavailable decoder oracle invoked")
    actual = audit_filter(P.labels,decoder_mode="quadratic-syndrome",syndrome_correction=Pretend())
    expected = audit_filter(P.labels,decoder_mode="quadratic-syndrome",syndrome_correction=P)
    assert actual["actual_quantum_word_probabilities"] == expected["actual_quantum_word_probabilities"]


def test_repository_package_import_path_has_the_same_validated_instrument():
    from theorems.ternary_syndrome_correction import SyndromeQuadratic as PackageProgram
    P = PackageProgram(((1,1,1),),((1,2,0),(1,0,2)),((0,1,0),))
    result = audit_filter(P.labels,decoder_mode="quadratic-syndrome",syndrome_correction=P)
    assert abs(result["executed_valid_signed_zero_sum_probability"]-7/12) < 1e-12


def test_random_quadratic_twirl_matches_ALL_coefficients_and_actual_quantum_states():
    A = ((1,1,1),)
    H = ((1,2,0),(1,0,2))
    exact_average = {}
    physical_average = np.zeros(27)
    for C in product(range(3),repeat=3):
        P = SyndromeQuadratic(A,H,(C,))
        for word,p in complete_classical_reference(P).items():
            exact_average[word] = exact_average.get(word,Fraction())+p/27
        control = audit_filter(A,decoder_mode="quadratic-syndrome",syndrome_correction=P)
        physical_average += np.array(control["actual_quantum_word_probabilities"])/27
    P = SyndromeQuadratic(A,H,((0,0,0),))
    twirl = complete_classical_reference(P,average_random_quadratic=True)
    assert exact_average == twirl
    np.testing.assert_allclose(physical_average,[float(twirl.get(word,0)) for word in product(range(3),repeat=3)],atol=1e-13)
    assert sum((p for word,p in twirl.items() if all(word)),Fraction()) == Fraction(7,18)


def test_quadratic_tensor_pinching_is_exactly_plus_or_minus_in_any_dimension():
    for r in (1,2,3):
        vectors = list(product(range(3),repeat=r))
        for x in vectors:
            for y in vectors:
                same = all((x[i]*x[j]-y[i]*y[j]) % 3 == 0 for i in range(r) for j in range(i,r))
                assert same == (y == x or y == tuple(-a % 3 for a in x))


def test_twirl_point_mass_bound_does_not_apply_to_the_unchanged_zero_frequency():
    P = program()
    for e in product((1,2),repeat=3):
        block = twirled_conditional_block(P,e)
        masses = [Fraction(row["integer_weight"],block["weight_denominator"]) for row in block["outcomes"]]
        assert sum(masses) == 1
        if block["nonzero_residual_frequency"]:
            assert max(masses) <= Fraction(2,block["block_size"])
        else:
            # This branch is retained separately in the large-source proof.
            assert sum(p for row,p in zip(block["outcomes"],masses) if all(row["word"])) == 1


@pytest.mark.parametrize("A", [((1,1,1),),((1,0,1,2),(0,1,2,2)),((1,0),(0,1))])
def test_fixed_matrix_random_full_syndrome_bound_includes_zero_frequency_mass(A):
    H = canonical_kernel_rows(A)
    r = len(H)
    P = SyndromeQuadratic(A,H,((0,)*(r*(r+1)//2),)*len(A))
    distribution = complete_classical_reference(P,average_random_quadratic=True)
    success = sum((p for word,p in distribution.items() if all(word)),Fraction())
    V = sum(all(sum(a*x for a,x in zip(row,word)) % 3 == 0 for row in A)
            for word in product((1,2),repeat=len(A[0])))
    assert success <= Fraction(V,2**len(A[0]))+Fraction(2*V,3**r)


@pytest.mark.parametrize("n,m", [(1,3),(2,3)])
def test_exact_IID_source_moment_and_rank_loss_used_in_large_bound(n,m):
    total_V,rank_failures = 0,0
    for flat in product(range(3),repeat=n*m):
        A = tuple(flat[i*m:(i+1)*m] for i in range(n))
        row_span = {tuple(sum(c*a[j] for c,a in zip(coeff,A)) % 3 for j in range(m))
                    for coeff in product(range(3),repeat=n)}
        rank_failures += len(row_span) < 3**n
        total_V += sum(all(sum(a*x for a,x in zip(row,word)) % 3 == 0 for row in A)
                       for word in product((1,2),repeat=m))
    assert Fraction(total_V,3**(n*m)) == Fraction(2**m,3**n)
    record = random_full_syndrome_success_bound(n,m)
    assert Fraction(rank_failures,3**(n*m)) <= fraction(record["rank_failure_upper"])


def test_dense_random_quadratic_candidate_fails_even_with_polynomial_restarts(report):
    record = random_full_syndrome_success_bound(64,128,64**2)
    assert fraction(record["unconditional_IID_source_success_upper_including_arbitrary_rank_failure_fallback"]) <= Fraction(1,2**61)
    assert not record["arbitrary_optimized_or_structured_Q_covered"]
    assert not record["large_quantum_circuit_executed"]
    assert not report["all_growing_rank_quadratic_filters_dequantized"]
    assert len(report["random_full_syndrome_quadratic_source_bounds"]) == 16
    for row in report["random_full_syndrome_quadratic_source_bounds"]:
        assert fraction(row["unconditional_IID_source_success_upper_including_arbitrary_rank_failure_fallback"]) <= Fraction(1,2**row["unconditional_success_at_most_two_to_minus"])


@pytest.mark.parametrize("args", [(True,3),(0,3),(3,2),(1,3,0),(1,3,True)])
def test_random_program_bound_cannot_hide_bad_dimensions_or_free_attempts(args):
    with pytest.raises(ValueError): random_full_syndrome_success_bound(*args)


def test_independent_quantum_replay_rejects_green_but_false_claims(report,tmp_path):
    output = tmp_path/"syndrome.json"
    output.write_text(json.dumps(report))
    good = subprocess.run(["node",str(CHECKER),"--syndrome-correction",str(output)],check=True,text=True,capture_output=True)
    assert json.loads(good.stdout)["checkedMatrices"] == 4
    for forgery in ("output", "program", "speedup"):
        bad = deepcopy(report)
        control = bad["controls"][2]
        if forgery == "output":
            control["exact_classical_output_distribution"][0]["probability"] = {"numerator":1,"denominator":1}
        elif forgery == "program":
            control["actual_quantum_control"]["quadratic_syndrome_program"]["upper_triangle_quadratic_coefficients"] = ((0,0,0),)
        else:
            bad["accepted_speedup_candidate"] = True
        output.write_text(json.dumps(bad))
        result = subprocess.run(["node",str(CHECKER),"--syndrome-correction",str(output)],text=True,capture_output=True)
        assert result.returncode != 0
