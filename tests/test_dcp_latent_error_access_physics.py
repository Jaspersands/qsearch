"""Exact access-model countercontrols, including positive exceptions. Preserve."""
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys

import pytest
from sympy import I,Matrix,Rational,diag,exp,eye,kronecker_product,simplify,sqrt,symbols,zeros

from theorems.dcp_latent_error_access_audit import (
    CONTRACT,CONTRACT_ID,PAIRS,REPORT,build_report,coincidence_access_receipt,
    conditional_classical_controls,root,unequal_state_span,
)

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_latent_error_access_audit_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_report()


def product_rows(phases):
    return Matrix([[1,phases[f],phases[e],phases[e]*phases[f]] for e,f in PAIRS])/2


def decode_matrix(rows,q):
    z=I if q==4 else -Rational(1,2)+I*sqrt(3)/2
    return Matrix([[Rational(a)+Rational(b)*z for a,b in row] for row in rows])


def test_symbolic_determinant_for_any_three_distinct_phase_points():
    z0,z1,z2=symbols("z0 z1 z2")
    V=product_rows((z0,z1,z2))
    assert simplify(16*V.det()+(z0-z1)**2*(z0-z2)*(z1-z2))==0


@pytest.mark.parametrize("q,expected",[(3,Rational(81,256)),(4,Rational(1,8))])
def test_exact_unequal_input_basis_and_Gram_not_a_float_rank_threshold(q,expected):
    C=unequal_state_span(q)
    phases=(1,root(q),root(q).conjugate())
    V=product_rows(phases)
    G=(V*V.conjugate().T).applyfunc(simplify)
    assert (decode_matrix(C["normalized_product_vectors_in_quadratic_field"],q)-V).applyfunc(simplify)==zeros(4)
    assert (decode_matrix(C["unequal_input_Gram_matrix_in_quadratic_field"],q)-G).applyfunc(simplify)==zeros(4)
    assert simplify(G.det())==expected==Rational(C["Gram_determinant_exact_rational"])
    assert all(simplify(sum(v*value.conjugate() for v,value in zip(V.row(i),V.row(i))))==1 for i in range(4))
    assert simplify(V.det())!=0
    assert C["general_quantum_purification_impossible"] is False


def test_unknown_signal_phase_rotations_cannot_remove_the_unequal_span():
    a,b=symbols("a b",real=True)
    U=diag(1,exp(I*b),exp(I*a),exp(I*(a+b)))
    V=product_rows((1,I,-I))
    original=V*V.conjugate().T
    rotated=V*U
    assert (rotated*rotated.conjugate().T-original).applyfunc(simplify)==zeros(4)


def test_positive_effect_premise_is_essential_not_merely_four_zero_expectations():
    V=product_rows((1,I,-I))
    nonpositive=diag(1,1,-1,-1)
    assert all(simplify((V.row(i)*nonpositive*V.row(i).conjugate().T)[0])==0 for i in range(4))
    assert nonpositive!=zeros(4)
    assert -1 in nonpositive.eigenvals()
    # For a PSD effect, zero expectation instead implies E^(1/2)|v>=0;
    # invertibility of the spanning vector matrix then forces E^(1/2)=0.
    assert V.det()!=0


def test_a_real_false_positive_comparison_measurement_is_NOT_excluded():
    SWAP=Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    symmetric=(eye(4)+SWAP)/2
    assert symmetric*symmetric==symmetric
    for z in (1,I,-I):
        v=Matrix([1,z,z,z*z])/2
        assert simplify((v.conjugate().T*symmetric*v)[0])==1
    unequal=Matrix([1,I,1,I])/2
    assert simplify((unequal.conjugate().T*symmetric*unequal)[0])==Rational(3,4)


def test_orthogonal_error_register_is_a_stronger_source_that_does_allow_comparison():
    label_effect=diag(1,0,0,0,1,0,0,0,1)
    effect=kronecker_product(eye(4),label_effect)
    phases=(1,I,-I)
    for e in range(3):
        for f in range(3):
            phase=Matrix([1,phases[f],phases[e],phases[e]*phases[f]])/2
            flag=zeros(9,1)
            flag[3*e+f]=1
            v=kronecker_product(phase,flag)
            assert simplify((v.conjugate().T*effect*v)[0])==int(e==f)
    receipt=coincidence_access_receipt("orthogonal-error-register-supplied")
    assert receipt["extra_source_access_proved"] is False
    assert receipt["accepted_speedup_candidate"] is False


def test_tensor_extension_uses_non_all_equal_inputs_not_a_general_purification_claim(report):
    V=product_rows((1,I,-I))
    G=V*V.conjugate().T
    W=Matrix([[1,1],[1,I]])/sqrt(2)
    H=W*W.conjugate().T
    assert simplify(H.det())==Rational(1,2)
    for k in (2,3,4):
        gram=G
        for _ in range(k-2):
            gram=kronecker_product(gram,H)
        expected=Rational(1,2)**((3+2*(k-2))*(1 << (k-2)))
        assert simplify(gram.det())==expected
    assert report["scope"]["all_noise_mitigation_or_quantum_algorithms_excluded"] is False
    assert report["scope"]["ensemble_equivalent_false_positive_channels_excluded"] is False


def test_CNOT_target_Z_outcome_is_independent_of_equal_or_unequal_hidden_errors(report):
    rows=report["physical_CNOT_Z_controls"]
    assert len(rows)==9
    assert {Fraction(B["Born_probability"]) for C in rows for B in C["branches"]}=={Fraction(1,2)}
    assert any(C["errors_equal"] for C in rows) and any(not C["errors_equal"] for C in rows)
    gate=Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    for C in rows:
        e,f=C["input_error_exponents"]
        source=Matrix([1,I**f,I**e,I**(e+f)])/2
        output=gate*source
        for B in C["branches"]:
            r=B["measured_target_Z"]
            v=Matrix([output[r],output[r+2]])
            mass=simplify((v.conjugate().T*v)[0])
            density=(v*v.conjugate().T/mass).applyfunc(simplify)
            assert mass==Rational(1,2)
            assert decode_matrix(B["root_density_quadratic_field"],4)==density
            assert B["root_error_exponent_mod4"]==(e+(1 if r==0 else -1)*f)%4


def test_latent_classical_retained_error_is_not_the_CNOT_sum_error():
    C=conditional_classical_controls()["q4_p_half"]
    assert Fraction(C["formal_latent_equality_probability"])==Fraction(3,8)
    assert Fraction(C["formal_retained_error_visibility"])==Fraction(2,3)
    assert Fraction(C["CNOT_sum_branch_visibility_given_magic_equality"])==Fraction(1,3)
    assert C["latent_error_equality_measurement_available"] is False


def test_exact_zero_boundary_refutes_strict_SNR_dominance_at_every_depth():
    p=Fraction(2,3)
    K=(1-p,p/2,p/2)
    lam=1-Fraction(3,2)*p
    assert K==(Fraction(1,3),)*3 and lam==0
    for depth in range(1,9):
        power=1 << depth
        survival=sum(x**power for x in K)
        posterior=tuple(x**power/survival for x in K)
        post_lam=posterior[0]-(posterior[1]+posterior[2])/2
        assert post_lam==0 and survival*post_lam**2==power*lam**2==0
    C=conditional_classical_controls()["q3_p_two_thirds"]
    assert C["strict_leaf_dominance"] is False


def test_access_gate_does_not_promote_private_error_arrays_or_overextend_the_support_promise():
    denied=coincidence_access_receipt("phase-qubits-only")
    assert denied["latent_error_equality_available"] is False
    assert denied["full_product_error_support_assumed"] is True
    for count in (1,2):
        unknown=coincidence_access_receipt("phase-qubits-only",count)
        assert unknown["latent_error_equality_available"] is None
    correlated=coincidence_access_receipt("phase-qubits-only",full_product_error_support=False)
    assert correlated["latent_error_equality_available"] is None
    assert correlated["status"]=="UNKNOWN_OUTSIDE_FULL_PRODUCT_ERROR_SUPPORT"
    with pytest.raises(ValueError):
        coincidence_access_receipt("private-simulator-error-array")
    with pytest.raises(ValueError):
        coincidence_access_receipt("phase-qubits-only",True)
    with pytest.raises(ValueError):
        coincidence_access_receipt("phase-qubits-only",full_product_error_support=1)


def js_check(R,tmp_path):
    target=tmp_path/"certificate.json"
    target.write_text(json.dumps(R))
    return subprocess.run(["node",str(CHECKER),str(target)],capture_output=True,text=True)


def test_live_provenance_and_independent_exact_cyclotomic_replay(report,tmp_path):
    assert json.loads(REPORT.read_text())==report
    assert json.loads(CONTRACT.read_text())["contract_id"]==CONTRACT_ID
    result=js_check(report,tmp_path)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["exact_Gram_determinants"]==["81/256","1/8"]


@pytest.mark.parametrize("mutation",["vector","gram","determinant","oracle","branch","doubled","strict","tensor","scope","support"])
def test_checker_rejects_false_physical_access_and_kernel_claims(report,tmp_path,mutation):
    R=deepcopy(report)
    if mutation=="vector":
        R["unequal_input_span_controls"][0]["normalized_product_vectors_in_quadratic_field"][0][0]=["1","0"]
    elif mutation=="gram":
        R["unequal_input_span_controls"][1]["unequal_input_Gram_matrix_in_quadratic_field"][0][0]=["0","0"]
    elif mutation=="determinant":
        R["unequal_input_span_controls"][0]["Gram_determinant_exact_rational"]="0"
    elif mutation=="oracle":
        R["access_receipts"][0]["latent_error_equality_available"]=True
    elif mutation=="branch":
        R["physical_CNOT_Z_controls"][0]["branches"][0]["Born_probability"]="1"
    elif mutation=="doubled":
        R["conditional_classical_vs_physical_controls"]["q4_p_half"]["CNOT_sum_branch_visibility_given_magic_equality"]="2/3"
    elif mutation=="strict":
        R["conditional_classical_vs_physical_controls"]["q3_p_two_thirds"]["strict_leaf_dominance"]=True
    elif mutation=="tensor":
        R["tensor_extension_q4"][2]["Gram_determinant_one_over_two_exponent"]-=1
    elif mutation=="support":
        R["scope"]["four_unequal_product_inputs_allowed_by_source_promise"]=False
    else:
        R["scope"]["all_noise_mitigation_or_quantum_algorithms_excluded"]=True
    assert js_check(R,tmp_path).returncode!=0


def test_read_only_CLI_is_a_scoped_access_audit_not_a_general_purification_no_go():
    before=REPORT.read_bytes()
    result=subprocess.run([sys.executable,"qsearch.py","dcp-latent-error-access","--no-write"],
                          cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["general_purification_no_go"] is False
    assert REPORT.read_bytes()==before
