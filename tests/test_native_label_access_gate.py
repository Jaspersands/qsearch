from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from native_label_access_gate import (
    ROOT, REPORT, CertificateField, collective_effects, conditional_gram_control,
    information_only_escape, label_access_ledger,
)


@pytest.mark.parametrize("q", [3,9,27,81])
def test_exact_field_retains_full_roots_conjugation_and_canonical_encoding(q):
    K=CertificateField(q)
    assert K.times(K.roots[-1],K.roots[1])==K.one
    for i in range(q):
        assert K.conjugate(K.roots[i])==K.roots[-i % q]
    assert K.encode(K.zero)==[]
    assert K.rational(K.scale(K.one,Fraction(2,3)))==Fraction(2,3)
    with pytest.raises(ArithmeticError):
        K.rational(K.roots[1])


@pytest.mark.parametrize("name", ["bell","coarse_bell","real_entangled","low_controlled_entangled","higher_prefix_entangled","flat_real_product","adaptive_second_basis"])
def test_collective_positive_factors_are_complete_and_not_only_rank_one(name):
    K=CertificateField(9)
    E,factors=collective_effects(K,name,(((1,),(2,)),((2,),(2,))))
    matrices=np.array([[[K.number(x) for x in row] for row in effect] for effect in E])
    assert np.allclose(matrices.sum(axis=0),np.eye(9),atol=2e-13)
    assert min(np.linalg.eigvalsh(matrix).min() for matrix in matrices)>-2e-13
    if name=="coarse_bell":
        assert all(len(terms)==3 for terms in factors)
        assert all(np.linalg.matrix_rank(matrix,tol=1e-10)==3 for matrix in matrices)
    if name not in ("flat_real_product","adaptive_second_basis"):
        # A nonzero Schmidt minor certifies an actual entangled factor.
        v=np.array([K.number(x) for x in factors[0][0][1]]).reshape(3,3)
        assert np.linalg.matrix_rank(v,tol=1e-10)>1


def test_full_high_lift_census_and_alias_blocks_keep_nonprimitive_secrets():
    c=conditional_gram_control(9,1,1,"low_controlled_entangled",((1,),(2,)),((2,),(2,)))
    assert c["high_kernel_secret_count"]==3
    assert c["conditional_high_lift_census_size"]==81
    assert c["full_conditional_Born_Gram_error"]<3e-11
    assert c["ALL_nonzero_high_residue_secrets"]==((1,),(2,),(4,),(5,),(7,),(8,))
    c=conditional_gram_control(9,1,0,"real_entangled",((0,),(0,)),((0,),(0,)))
    assert (3,) in c["ALL_nonzero_high_residue_secrets"]
    assert (6,) in c["ALL_nonzero_high_residue_secrets"]
    assert c["full_conditional_Born_Gram_error"]<3e-11


def test_second_digit_quantum_control_is_not_misclassified_as_first_digit_control():
    K=CertificateField(27)
    a,_=collective_effects(K,"higher_prefix_entangled",(((0,),(0,)),((0,),(0,))))
    b,_=collective_effects(K,"higher_prefix_entangled",(((3,),(0,)),((0,),(0,))))
    assert a!=b
    c=conditional_gram_control(27,1,2,"higher_prefix_entangled",((3,),(0,)),((0,),(0,)))
    assert c["high_kernel_secret_count"]==9
    assert c["high_residue_sign_block_size_upper"]==18
    assert c["full_conditional_Born_Gram_error"]<3e-11
    with pytest.raises(ValueError):
        conditional_gram_control(27,1,1,"higher_prefix_entangled",((3,),(0,)),((0,),(0,)))


def test_real_flat_product_saturates_universal_collective_covariance_constant():
    c=conditional_gram_control(3,1,0,"flat_real_product",((0,),(0,)),((0,),(0,)))
    assert c["maximum_absolute_Gram_row_sum_exact"]=="32/9"
    assert c["universal_nonkernel_operator_bound_exact"]=="32/9"
    assert c["full_nonkernel_centered_Gram_exact_rationals"]==[["16/9","16/9"],["16/9","16/9"]]


@pytest.mark.parametrize("n,r,M,ell", [(1,2,2,0),(8,8,64,1),(64,2,128,1),(32,32,1024,16)])
def test_copy_access_gate_uses_exact_comparison_not_float_underflow(n,r,M,ell):
    c=label_access_ledger(n,r,M,ell)
    v=(Fraction(5,3)**M-1)/3**(n*(r-ell))
    rare=(1-Fraction(1,3)**M)/3**(n*(r-ell))
    expected=rare>=Fraction(1,10) or v>=(Fraction(1,10)-rare)**2
    assert c["necessary_copy_access_gate_passed"]==expected
    assert c["nonzero_residue_covariance_block_size"]["exponent"]==n*ell
    assert not c["higher_label_digits_in_quantum_control_covered"]
    assert not c["all_polynomial_copy_receivers_ruled_out"]
    assert c["unlimited_full_label_FINAL_classical_decoding_covered"]


def test_more_label_control_or_more_charged_copies_can_escape_the_gate():
    assert not label_access_ledger(128,2,256,1)["necessary_copy_access_gate_passed"]
    assert label_access_ledger(128,2,768,1)["necessary_copy_access_gate_passed"]
    assert not label_access_ledger(32,32,1024,16)["necessary_copy_access_gate_passed"]
    assert label_access_ledger(32,32,1024,20)["necessary_copy_access_gate_passed"]
    assert label_access_ledger(128,128,16384,64)["approximate_advantage_upper_NOT_authoritative"]>0
    json.dumps(label_access_ledger(128,128,16384,64),allow_nan=False)


def test_zero_copy_gate_and_full_label_scope_are_not_confused():
    assert label_access_ledger(3,5,0,4)["approximate_advantage_upper_NOT_authoritative"]==0
    assert not label_access_ledger(3,5,0,4)["necessary_copy_access_gate_passed"]
    assert label_access_ledger(3,5,0,4,0)["necessary_copy_access_gate_passed"]
    with pytest.raises(ValueError,match="outside"):
        label_access_ledger(3,5,15,5)


def test_float_underflow_never_rewrites_the_positive_exact_bound():
    c=label_access_ledger(256,256,65536,128)
    assert c["approximate_advantage_upper_NOT_authoritative"]==0
    assert c["least_trit_advantage_upper"]["nonkernel_squared"]["numerator"]=={
        "positive_base":5,"negative_base":3,"exponent":65536}
    assert c["numerical_underflow_is_NOT_an_exact_zero_bound"]
    assert not c["necessary_copy_access_gate_passed"]


@pytest.mark.parametrize("args", [(True,2,2,0),(1,2,-1,0),(1,2,2,True),(1,2,2,0,.1),(1,2,2,0,"1")])
def test_invalid_scope_and_inexact_requested_advantage_rejected(args):
    with pytest.raises(ValueError):
        label_access_ledger(*args)


@pytest.mark.parametrize("r", [4,5,6])
def test_full_label_PGM_reference_is_an_information_escape_not_a_compiler(r):
    c=information_only_escape(r,70321)
    counts=dict(c["fiber_counts"])
    assert sum(counts.values())==3**r
    q=3**r
    # Independent direct Fourier output law includes EVERY secret difference.
    y=np.array(sorted(counts))
    weights=np.sqrt([counts[z] for z in y])
    probability=np.array([abs(np.sum(weights*np.exp(2j*np.pi*d*y/q)))**2/(q*3**r) for d in range(q)])
    assert np.isclose(sum(probability),1,atol=3e-13)
    assert np.isclose(probability[np.arange(q)%3==0].sum(),c["dense_FULL_label_PGM_least_trit_success_information_only"],atol=3e-13)
    assert not c["efficient_PGM_compiler_or_fiber_oracle_supplied"]
    assert c["conditional_cohort_is_NOT_a_population_bound_violation"]


def test_live_collective_controls_keep_source_scope_and_all_debt_flags():
    c=json.loads(REPORT.read_text())
    assert len(c["exact_collective_POVM_controls"])==9
    for control in c["exact_collective_POVM_controls"]:
        Q=control["modulus"]//3**control["quantum_low_label_digits"]
        secrets=control["ALL_nonzero_high_residue_secrets"]
        gram=control["full_nonkernel_centered_Gram_exact_rationals"]
        for i,s in enumerate(secrets):
            for j,t in enumerate(secrets):
                if not (all((x-y)%Q==0 for x,y in zip(s,t)) or all((x+y)%Q==0 for x,y in zip(s,t))):
                    assert Fraction(gram[i][j])==0
        assert control["kernel_secret_removal_is_charged_in_gate_NOT_postselection"]
    assert not c["new_speedup_claimed"]
    assert not c["full_label_quantum_measurements_or_all_polynomial_copies_ruled_out"]


def test_independent_exact_factor_and_character_kernel_replay():
    result=subprocess.run(["node",str(ROOT/"research/certificates/native_label_access_gate_crosscheck.js")],capture_output=True,text=True,check=True)
    c=json.loads(result.stdout)
    assert c["effectCount"]==82
    assert c["gramEntries"]==7568
    assert c["entangledFactors"]==63
    assert c["higherRankEffects"]==3


@pytest.mark.parametrize("tamper", ["scope","negative_factor","gram","kernel","copy_gate"])
def test_independent_checker_rejects_false_mathematical_artifacts(tmp_path,tamper):
    c=json.loads(REPORT.read_text())
    if tamper=="scope":
        c["full_label_quantum_measurements_or_all_polynomial_copies_ruled_out"]=True
    elif tamper=="negative_factor":
        c["exact_collective_POVM_controls"][0]["positive_effect_factors"][0][0]["positive_weight"]="-1/3"
    elif tamper=="gram":
        c["exact_collective_POVM_controls"][0]["full_nonkernel_centered_Gram_exact_rationals"][0][0]="19"
    elif tamper=="kernel":
        c["exact_collective_POVM_controls"][0]["kernel_secret_removal_is_charged_in_gate_NOT_postselection"]=False
    else:
        c["scaling_ledgers"][0]["necessary_copy_access_gate_passed"]=not c["scaling_ledgers"][0]["necessary_copy_access_gate_passed"]
    path=tmp_path/"tampered.json"
    path.write_text(json.dumps(c))
    result=subprocess.run(["node",str(ROOT/"research/certificates/native_label_access_gate_crosscheck.js"),str(path)],capture_output=True,text=True)
    assert result.returncode!=0
