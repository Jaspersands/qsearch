from collections import Counter
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from native_echo_shifted_probe_gate import (
    ROOT, REPORT, cross_probe_moment, exact_gram_control, full_A_inverse_calibration_countercontrol,
    quartet_classes, weak_trit_ledger,
)
from ternary_covariant_noise import phase


@pytest.mark.parametrize("q,n,left,right,settings", [
    (9,1,(2,),(7,),(0,0)), (9,1,(2,),(2,),(4,7)),
    (3,2,(1,0),(2,1),(1,2)), (9,1,(0,),(3,),(5,1)),
])
def test_complete_original_iid_source_and_output_gram(q,n,left,right,settings):
    vectors = tuple(product(range(q),repeat=n))
    good = [s for s in vectors if s not in {tuple(-x%q for x in left),tuple(-x%q for x in right)}]
    records = []
    for first,second,outcome in product(vectors,vectors,range(3)):
        def response(s,shift):
            a = sum((x+d)*y for x,d,y in zip(s,shift,first))-settings[0]
            b = sum((x+d)*y for x,d,y in zip(s,shift,second))-settings[1]
            return (1+phase(a,q)*phase(-outcome,3)+phase(b,q)*phase(-2*outcome,3))/3
        difference = tuple(x-y for x,y in zip(left,right))
        C = (1+phase(sum(x*y for x,y in zip(difference,first)),q)+phase(sum(x*y for x,y in zip(difference,second)),q))/3
        records.append([3*response(s,left)*response(s,right).conjugate()-C for s in good])
    Z = np.array(records)
    gram = Z.T@Z.conj()/len(records)
    variance = 2/3
    assert np.allclose(gram,variance*np.eye(len(good)),atol=2e-13)
    control = exact_gram_control(q,left,right,1)
    assert np.allclose(gram,[[float(Fraction(v)) for v in row] for row in control["full_centered_probe_Gram_exact_rationals"]])


def test_all_character_quartets_are_classified_with_unit_exception_elimination():
    classes = quartet_classes()
    assert len(classes)==81
    counts = Counter(c["class"] for c in classes)
    assert sorted(counts.values())==[6,9,12,54]
    for c in classes:
        if "exceptional_first_secret_coefficients" in c:
            assert {c["exceptional_first_secret_coefficients"],c["exceptional_second_secret_coefficients"]}=={(-1,0),(0,-1)}


@pytest.mark.parametrize("q,left,right,m", [(9,(2,),(7,),3),(9,(2,),(2,),3),(27,(5,),(18,),2),(3,(1,0),(2,1),2)])
def test_tensor_gram_has_only_claimed_nonexceptional_diagonal(q,left,right,m):
    c = exact_gram_control(q,left,right,m)
    v = Fraction(5,3)**m-1 if left==right else 1-Fraction(1,3)**m
    assert all(Fraction(value)==(v if i==j else 0) for i,row in enumerate(c["full_centered_probe_Gram_exact_rationals"]) for j,value in enumerate(row))
    assert cross_probe_moment(q,left,right,left,left)>=0


@pytest.mark.parametrize("n,r,M,w,L", [(1,2,4,1,1),(2,3,8,2,4),(8,8,66,3,4),(4,3,8,2,7)])
def test_directed_rational_envelope_dominates_analytic_bound(n,r,M,w,L):
    ledger = weak_trit_ledger(n,r,M,w,L)
    W = 3**w
    exact = (W*(W-1)+L*W)/3**(n*r)+np.sqrt(L*W*W*((5/3)**(M-w)-1)/(2*3**(n*r)))
    envelope = (W*(W-1)+L*W)/3**(n*r)+L*W*(5/3)**((max(M-n*r,0)+1)//2)*(3/4)**(n*r)
    assert envelope>=exact
    assert not ledger["coupling_values_depending_on_full_A_labels_OUTSIDE_fixed_menu_covered"]
    assert not ledger["multiple_interleaved_echo_rounds_ruled_out"]
    assert ledger["classical_unknown_secret_postprocessing_unlimited_in_bound"]


@pytest.mark.parametrize("args", [(1,2,2,2),(True,2,4,1),(1,2,4,0),(1,2,600,513)])
def test_invalid_regimes_rejected(args):
    with pytest.raises(ValueError):
        weak_trit_ledger(*args)


def test_independent_rational_checker_replays_every_entry():
    result = subprocess.run(["node",str(ROOT/"research/certificates/native_echo_shifted_probe_gate_crosscheck.js")],capture_output=True,text=True,check=True)
    assert json.loads(result.stdout)["gramEntries"]==836


@pytest.mark.parametrize("q", [9,27,81])
def test_full_A_inverse_calibration_actually_breaks_centered_orthogonality(q):
    control = full_A_inverse_calibration_countercontrol(q)
    assert control["exact_nonzero_centered_Gram_entry"]=="4/27"
    rows = []
    for a,c,z in product(range(q),range(q),range(3)):
        d = pow(a,-1,q) if a%3 else 0
        A = lambda s: (1+phase(s*a,q)*phase(-z,3)+phase(s*c,q)*phase(-2*z,3))/3
        C = (1+phase(-d*a,q)+phase(-d*c,q))/3
        rows.append([3*A(s)*A(s+d).conjugate()-C for s in (q//3,2*q//3)])
        assert all(s not in (0,(-d)%q) for s in (q//3,2*q//3))
    Z = np.array(rows)
    gram = Z.T@Z.conj()/len(rows)
    assert np.isclose(gram[0,1],4/27,atol=2e-13)
    unit = np.repeat(np.arange(q)%3!=0,3*q)
    assert np.isclose((Z[unit,0]*Z[unit,1].conj()).mean(),-1/9,atol=2e-13)
    assert np.isclose((Z[~unit,0]*Z[~unit,1].conj()).mean(),2/3,atol=2e-13)
    assert control["conditional_unit_A_Gram_entry"]=="-1/9"
    assert control["conditional_nonunit_A_zero_fallback_Gram_entry"]=="2/3"
    assert not control["source_labels_rejected"]
    assert not control["positive_receiver_or_decoder_follows"]


@pytest.mark.parametrize("tamper", ["scope","gram","ledger","quartet"])
def test_independent_checker_rejects_false_theorem_artifacts(tmp_path,tamper):
    report = json.loads(REPORT.read_text())
    if tamper=="scope":
        report["full_A_frequency_inverse_calibration_is_covered"] = True
    elif tamper=="gram":
        report["exact_centered_Gram_controls"][0]["full_centered_probe_Gram_exact_rationals"][0][1] = "1"
    elif tamper=="ledger":
        report["growing_weak_trit_ledgers"][0]["least_trit_mean_advantage_upper_bound"]["centered_probe_term"]["coefficient_squared"] = 0
    else:
        report["complete_single_copy_character_quartets"][0]["class"] = "incorrect"
    path = tmp_path/"tampered.json"
    path.write_text(json.dumps(report))
    result = subprocess.run(["node",str(ROOT/"research/certificates/native_echo_shifted_probe_gate_crosscheck.js"),str(path)],capture_output=True,text=True)
    assert result.returncode!=0
