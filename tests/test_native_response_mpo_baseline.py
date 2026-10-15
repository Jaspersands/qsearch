"""Operator ordering, exact readout, precision and access-model falsifiers."""
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import random
import subprocess
import numpy as np
import pytest
from theorems import native_response_mpo_baseline as B


def dense_kernel(M,b):
    words=tuple(product(range(3),repeat=M));D=3**M
    kernel=np.empty((D,D),complex)
    for vi,v in enumerate(words):
        for wi,w in enumerate(words):
            turn=sum(v[M-1-k]*w[ell]/3**(ell-k+1)
                for k in range(M) for ell in range(k,min(M,k+b)))
            kernel[vi,wi]=np.exp(2j*np.pi*turn)/np.sqrt(D)
    return kernel


def probabilities(model):
    v=tuple((int(a,0),int(b,0)) for a,b in model.calibration_vector())
    masses=tuple(a*a+b*b for a,b in v)
    return tuple(Fraction(m,sum(masses)) for m in masses)


def ideal(phases,q,b,schedule):
    M=len(phases);D=3**M;F=dense_kernel(M,b)
    eta=np.array([sum(phases[j][x] for j,x in enumerate(w)) for w in product(range(3),repeat=M)])
    phase=np.exp(2j*np.pi*eta/q);state=np.ones(D,complex)/np.sqrt(D)
    for kind,sign in schedule:
        state=(phase**sign)*state if kind=="phase" else (F if sign==1 else F.conj().T)@state
    return np.abs(state)**2


@pytest.mark.parametrize("M,b", ((1,1),(2,1),(2,2),(3,1),(3,2),(3,3)))
@pytest.mark.parametrize("schedule", ((("fourier",1),),(("fourier",-1),),
    (("phase",1),("fourier",1),("phase",-1),("fourier",-1)),B.THREE_CALL,
    (("fourier",-1),("phase",1),("fourier",1),("phase",-1))))
def test_kernel_and_reversal_match_independent_full_matrices(M,b,schedule):
    phases=tuple(((2*j+8)%9,(j+1)%9,(3*j)%9) for j in range(M))
    model=B.PublicPhaseMPOBaseline(phases,9,schedule,b,failure_bits=28,
        policy=replace(B.MPOPolicy(),max_bond=1000))
    p=np.array([float(v) for v in probabilities(model)])
    assert np.abs(ideal(phases,9,b,schedule)-p).sum()/2<=float(Fraction(model.ledger["per_sample_TV_upper_under_IID_bits"]))+1e-13
    assert sum(probabilities(model))==1
    assert model.stats["digit_reversals"]==sum(k=="fourier" for k,_ in schedule)


@pytest.mark.parametrize("M,b", ((2,1),(2,2),(3,2),(3,3)))
@pytest.mark.parametrize("sign",(-1,1))
def test_every_complex_operator_column_matches_independent_kernel(M,b,sign):
    model=B.PublicPhaseMPOBaseline(((0,0,0),)*M,9,(("phase",1),),b,failure_bits=30)
    F=dense_kernel(M,b);F=F if sign==1 else F.conj().T
    for column,word in enumerate(product(range(3),repeat=M)):
        model.state=tuple(tuple(B.GaussianMatrix.scalar(int(x==digit)) for x in range(3)) for digit in word)
        if sign==-1:model._reverse()
        model._apply_fourier_memory(sign==-1)
        if sign==1:model._reverse()
        actual=np.array([complex(int(a,0),int(c,0)) for a,c in model.calibration_vector()])
        actual/=float(2**(model.P*M))*np.sqrt(3**M)
        assert np.linalg.norm(actual-F[:,column])<=float(Fraction(model.ledger["per_operation_operator_error_upper"]))+1e-13


def test_exact_prefix_masses_and_readout_work():
    model=B.PublicPhaseMPOBaseline(((8,1,0),(1,2,6)),9,failure_bits=18)
    p=probabilities(model);samples=model.sample_many(10,random.Random(10).getrandbits,True)
    words=tuple(product(range(3),repeat=2))
    for sample in samples["samples"]:
        for step in sample["trace"]:
            prefix=tuple(step["prefix"]);w=[int(s,0) for s in step["child_weights"]]
            parent=sum(v for word,v in zip(words,p) if word[:len(prefix)]==prefix)
            for d in range(3):
                child=sum(v for word,v in zip(words,p) if word[:len(prefix)+1]==prefix+(d,))
                assert Fraction(w[d],sum(w))==child/parent
    assert model.stats["complex_matrix_products"]==12+18*10
    assert model.stats["underlying_FLINT_integer_matrix_products"]==4*model.stats["complex_matrix_products"]
    assert model.stats["random_bits_consumed"]==20*model.K


def test_growing_product_width_schedule_has_no_dense_solver_table():
    phases=tuple(((8+j)%9,(1+2*j)%9,(-3*j)%9) for j in range(24))
    model=B.PublicPhaseMPOBaseline(phases,9,bandwidth=1)
    result=model.sample_many(1,random.Random(11).getrandbits,True)
    F=dense_kernel(1,1);vectors=[np.ones(3,complex)/np.sqrt(3) for _ in phases]
    for kind,sign in model.schedule:
        if kind=="phase":vectors=[v*np.exp(sign*2j*np.pi*np.array(row)/9) for v,row in zip(vectors,phases)]
        elif sign==1:vectors=list(reversed([F@v for v in vectors]))
        else:vectors=[F.conj().T@v for v in reversed(vectors)]
    for j,step in enumerate(result["samples"][0]["trace"]):
        masses=[int(x,0) for x in step["child_weights"]]
        measured=np.array([float(Fraction(x,sum(masses))) for x in masses])
        reference=np.abs(vectors[j])**2
        assert np.max(np.abs(measured-reference))<=float(Fraction(model.ledger["per_sample_TV_upper_under_IID_bits"]))+1e-12
    assert max(max(p) for p in model.profiles)==1
    assert model.stats["dense_word_table_or_state_allocated_by_sampler"] is False
    with pytest.raises(B.BaselineResourceLimit,match="CALIBRATION_CAP"):model.calibration_vector()
    assert model.stats["maximum_integer_bits_seen"]<=model.ledger["intermediate_integer_bits_upper"]


def test_large_integer_encoding_roundtrips_without_global_decimal_limit_changes():
    import sys
    previous=sys.get_int_max_str_digits()
    for value in (0,1,-1,2**20000,-2**20000):assert int(B.encode_integer(value),0)==value
    assert sys.get_int_max_str_digits()==previous


@pytest.mark.parametrize("field,reason", (("max_bond","BOND"),("max_tensor_entries","TENSOR"),
    ("max_environment_entries","ENVIRONMENT"),("max_phase_entries","PHASE"),("max_enclosure_bits","PRECISION")))
def test_caps_are_UNKNOWN_not_failed_classical_attacks(field,reason):
    with pytest.raises(B.BaselineResourceLimit,match="UNKNOWN_.*"+reason):
        B.PublicPhaseMPOBaseline(((8,1,0),(2,3,4)),9,policy=replace(B.MPOPolicy(),**{field:1}))


def test_batch_preflight_precedes_random_bits_and_environments():
    model=B.PublicPhaseMPOBaseline(((8,1,0),(2,3,4)),9,
        policy=replace(B.MPOPolicy(),max_readout_complex_matrix_products=1))
    def denied(K):raise AssertionError("random draw before cap preflight")
    with pytest.raises(B.BaselineResourceLimit,match="READOUT_WORK_CAP"):model.sample_many(1,denied)
    assert model.environment is None and model.stats["random_bits_consumed"]==0


@pytest.mark.parametrize("M,Q,f", ((1,1,1),(8,3,8),(64,3,20),(1024,3,10),(256,8,12)))
def test_all_Fourier_calls_and_full_cyclic_accuracy_are_paid(M,Q,f):
    L=B.schedule_ledger(M,1,tuple(("fourier",(-1)**j) for j in range(Q)),f,True)
    assert L["Fourier_calls_Q"]==Q
    assert Fraction(L["per_sample_TV_upper_under_IID_bits"])<=Fraction(1,2**f)
    assert L["MPS_bond_upper"]==3**(Q*(L["selected_bandwidth_b"]-1))
    assert L["polynomial_Q_or_exponential_accuracy_is_not_covered"] is True


def test_full_cyclic_target_executes_when_small_and_fails_caps_without_hardness():
    model=B.PublicPhaseMPOBaseline(((8,1,0),(2,3,4)),9,full_cyclic=True,failure_bits=8)
    assert model.b==2
    assert model.sample_many(1,random.Random(4).getrandbits)["status"].startswith("COMPLETED")
    assert B.PublicPhaseMPOBaseline(((8,1,0),),9,full_cyclic=True).b==1
    with pytest.raises(B.BaselineResourceLimit,match="BOND_CAP"):
        B.PublicPhaseMPOBaseline(((8,1,0),)*64,9,full_cyclic=True)
    with pytest.raises(ValueError,match="boolean"):
        B.PublicPhaseMPOBaseline(((8,1,0),),9,bandwidth=1,full_cyclic="false")


@pytest.mark.parametrize("turn",(True,0.1,"1/9"))
def test_certified_root_primitive_refuses_ambiguous_float_or_string_angles(turn):
    with pytest.raises(ValueError,match="exact integer or Fraction"):
        B.certified_dyadic_root(turn,32,256)


@pytest.mark.parametrize("schedule", ((),(("oracle",1),),(("phase",0),),(("phase",True),),(("fourier",1,0),)))
def test_schema_rejects_free_oracles_and_invalid_operations(schedule):
    with pytest.raises(ValueError):B.PublicPhaseMPOBaseline(((8,1,0),),9,schedule)


def node_check(payload):
    return subprocess.run(["node","-e",
        "const X=require('./research/certificates/native_response_mpo_baseline_crosscheck.js');let s='';"
        "process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));"],
        input=json.dumps(payload),text=True,capture_output=True,cwd=B.ROOT)


def test_independent_dense_integer_kernel_and_trace_replay():
    result=node_check(json.loads(B.REPORT.read_text()))
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["verified"] is True


@pytest.mark.parametrize("kind", ("root","vector","mass","bond","calls","work","truth","hash"))
def test_independent_checker_rejects_false_evidence(kind):
    p=json.loads(B.REPORT.read_text());C=p["controls"][0];M=C["model"]
    if kind=="root":M["phase_grid"][0]["integer_value"][0]="999999999999999999999999999999999999999"
    elif kind=="vector":
        v=C["small_calibration_integer_statevector"][0];v[0]=str(int(v[0],0)+1)
    elif kind=="mass":
        v=C["sampling"]["samples"][0]["trace"][0]["child_weights"];v[0]=str(int(v[0],0)+1)
    elif kind=="bond":M["bond_profiles"][1][1]+=1
    elif kind=="calls":M["accuracy_and_width_ledger"]["Fourier_calls_Q"]+=1
    elif kind=="work":M["observed_work"]["complex_matrix_products"]-=1
    elif kind=="truth":M["observed_work"]["private_secret_or_errors_used"]=True
    else:p["producer_sha256"]="0"*64
    assert node_check(p).returncode!=0
