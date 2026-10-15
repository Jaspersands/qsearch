"""QFT operator bounds, joint instruments, resource scaling and model gates."""
from copy import copy, deepcopy
from fractions import Fraction
import json
import subprocess

import numpy as np
import pytest
from qiskit.quantum_info import Operator

from theorems import lattice_qft_precision as P
from theorems.lattice_cube_coset_source import CubeCosetSource
from theorems.lattice_cube_source_circuit import cube_resource_estimate, compile_cube_evaluator
from theorems.lattice_cube_dcp_readout import compile_phase_source, simulate_phase_batch, OpaquePhaseBackend


def stored():
    return json.loads(P.REPORT.read_text())


def node_check(payload):
    return subprocess.run(["node","-e",
        "const X=require('./research/certificates/lattice_qft_precision_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);"
        "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));"],
        input=json.dumps(payload),text=True,capture_output=True,cwd=P.ROOT)


@pytest.mark.parametrize("ell,b", ((1,0),(2,0),(3,1),(4,1),(5,2),(6,4),(6,5),(7,5)))
def test_actual_library_cutoff_and_dense_operator_bounds(ell,b):
    plan=P.precision_plan(ell,cutoff=b)
    forward=P.compile_qft(plan)
    inverse=P.compile_qft(plan,inverse=True)
    U=Operator(forward).data
    N=2**ell
    F=np.exp(2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/np.sqrt(N)
    norm=float(np.linalg.norm(U-F,ord=2))
    assert norm<=float(plan.encoded_qft_operator_upper)+1e-12
    assert np.allclose(Operator(inverse).data,U.conj().T,atol=1e-12)
    assert forward.count_ops().get("cp",0)==b*ell-b*(b+1)//2
    if plan.exact:
        assert plan.truncation_operator_upper==0


@pytest.mark.parametrize("ell,b", ((2,0),(4,1),(6,4),(7,5)))
def test_exact_omitted_angle_sums_and_closed_kept_weights(ell,b):
    omitted=sum(Fraction(ell-d,2**d) for d in range(b+1,ell))
    closed=Fraction(ell-b-2,2**b)+Fraction(1,2**(ell-1))
    assert omitted==closed
    kept=sum(Fraction(ell-d,2**d) for d in range(1,b+1))
    assert kept==P.precision_plan(ell,cutoff=b).retained_angle_weight


def test_complete_entangled_instrument_inherits_bound_without_per_label_inference():
    ell,b=7,5
    plan=P.precision_plan(ell,cutoff=b)
    N=2**ell
    F=np.exp(2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/np.sqrt(N)
    U=Operator(P.compile_qft(plan)).data
    rng=np.random.default_rng(99501)
    # Cell ancilla and colour payload are both entangled with position.
    state=rng.normal(size=(2,2,N))+1j*rng.normal(size=(2,2,N))
    state/=np.linalg.norm(state)
    ideal=np.einsum("kv,acv->ack",F,state)
    approximate=np.einsum("kv,acv->ack",U,state)
    distance=0
    for cell in range(2):
        for label in range(N):
            a=np.outer(ideal[cell,:,label],ideal[cell,:,label].conj())
            bmatrix=np.outer(approximate[cell,:,label],approximate[cell,:,label].conj())
            distance+=sum(abs(np.linalg.eigvalsh(a-bmatrix)))/2
    assert distance<=float(plan.encoded_qft_operator_upper)+1e-12
    assert not plan.record()["normalized_rare_branch_accuracy_certified_without_mass_bound"]


@pytest.mark.parametrize("k", (8,32,128))
def test_rare_postselection_can_have_maximal_payload_error(k):
    p=Fraction(1,2**k)
    ideal=np.diag([float(p),0,1-float(p),0])
    other=np.diag([0,float(p),1-float(p),0])
    distance=float(sum(abs(np.linalg.eigvalsh(ideal-other)))/2)
    assert distance==float(p)
    payload0=ideal[:2,:2]/float(p)
    payload1=other[:2,:2]/float(p)
    assert sum(abs(np.linalg.eigvalsh(payload0-payload1)))/2==1
    assert P.conditional_accuracy(p,p)["conditional_trace_upper"]=="1"
    assert P.conditional_accuracy(p)["conditional_trace_upper"] is None


def test_inverse_and_parent_reflection_calls_are_not_free():
    usage=P.QFTUsage(5,2,3)
    assert usage.total_calls==13
    plan=P.precision_plan(64,usage)
    ledger=P.QFTUsageLedger(plan)
    ledger.charge("forward",5)
    ledger.charge("inverse",2)
    ledger.charge("parent_reflection",3)
    assert ledger.record()["charged_total_QFT_or_inverse_calls"]==13
    with pytest.raises(ValueError,match="BUDGET_EXCEEDED"): ledger.charge("forward")
    with pytest.raises(ValueError): ledger.charge("amplification_is_free")
    with pytest.raises(ValueError): copy(ledger)
    with pytest.raises(ValueError): deepcopy(ledger)


def test_rational_auto_selection_and_encoded_pi_failure_are_distinct():
    for ell,T in ((264,128),(65536,10000),(1_000_000,1_000_000)):
        plan=P.precision_plan(ell,P.QFTUsage(T),"1/100")
        assert plan.cutoff==min(ell-1,P.ceil_log2_rational(Fraction(8*ell*T*100)))
        assert plan.usage.total_calls*plan.truncation_operator_upper<=Fraction(1,200)
        assert plan.record()["encoded_QFT_parameter_target_met"]
    huge=P.precision_plan(256,P.QFTUsage(2**80))
    assert huge.record()["ideal_truncation_target_met"]
    assert not huge.record()["encoded_QFT_parameter_target_met"]
    assert huge.record()["complete_experiment_encoded_QFT_trace_upper"]=="1"


def test_external_gate_error_is_conditional_not_hardware_certification():
    plan=P.precision_plan(8,P.QFTUsage(20),external_gate_error="1/1000")
    record=plan.record()
    assert record["complete_experiment_upper_IF_external_gate_bound_holds"] is not None
    assert not record["arithmetic_preparation_and_hardware_errors_covered"]
    assert P.precision_plan(8).record()["complete_experiment_upper_IF_external_gate_bound_holds"] is None


def test_non_normal_angles_fail_closed_and_have_no_encoded_certificate():
    plan=P.precision_plan(2048,cutoff=2047)
    assert plan.record()["complete_experiment_encoded_QFT_trace_upper"] is None
    assert not plan.record()["numeric_normal_angle_encoding_supported"]
    with pytest.raises(ValueError,match="NUMERIC_ANGLE_RANGE"): P.compile_qft(plan)


@pytest.mark.parametrize("bad", (True,0,-1,1.5))
def test_invalid_wire_and_usage_inputs_are_rejected(bad):
    with pytest.raises(ValueError): P.precision_plan(bad)
    if bad!=0:
        with pytest.raises(ValueError): P.QFTUsage(bad)


def test_targets_and_policies_do_not_accept_ambiguous_floats():
    with pytest.raises(ValueError): compile_phase_source({"shift":1})
    with pytest.raises(ValueError): P.precision_plan(8,target=0.01)
    with pytest.raises(ValueError): P.precision_plan(8,cutoff=8)
    with pytest.raises(ValueError): P.QFTUsage(0,0,0)
    with pytest.raises(ValueError): P.CircuitResourcePolicy(max_qubits=True)
    with pytest.raises(ValueError,match="RESOURCE_POLICY"):
        P.compile_qft(P.precision_plan(264),P.CircuitResourcePolicy(max_QFT_instructions=10))


@pytest.mark.parametrize("basis", (((1,),),((-1,),),((7,2),(6,-2))))
def test_closed_signed_arithmetic_resources_match_actual_compilation(basis):
    n=len(basis)
    source=CubeCosetSource(basis,7,1,0,4,4,(1,)*n)
    estimate=cube_resource_estimate(source)
    compiled=compile_cube_evaluator(source)
    record=compiled.resource_record()
    for key in ("compiled_qubits","input_qubits","cell_output_qubits","shared_arithmetic_workspace_qubits",
                "logical_instruction_count","constant_additions_including_uncompute"):
        assert estimate[key]==record[key]
    assert not estimate["estimate_allocates_quantum_gates_or_preimages"]


def test_resource_estimation_is_independent_of_classical_preimages(monkeypatch):
    def forbidden(*args,**kwargs): raise AssertionError("resource estimate enumerated source")
    monkeypatch.setattr(CubeCosetSource,"fibres_for_audit",forbidden)
    source=CubeCosetSource(((1,),),3,1,0,2**512,2,(1,))
    assert cube_resource_estimate(source)["max_signed_adder_bits"]>128
    with pytest.raises(ValueError,match="RESOURCE_POLICY"):
        compile_cube_evaluator(source,policy=P.CircuitResourcePolicy(max_adder_bits=128))


def test_actual_source_compile_passes_old_128_wire_barrier():
    record=stored()["actual_beyond_old_128_wire_compile"]
    assert record["position_qubits"]==264
    assert record["compiled_phase_parent_qubits"]==601
    assert record["logical_QFT_controlled_phase_gates"]==6275
    assert record["QFT_precision_plan"]["encoded_QFT_parameter_target_met"]
    assert stored()["large_control_is_resource_only_classically_easy_not_a_DCP_promise"]


def test_approximate_source_is_budgeted_and_not_mislabeled_exact_DCP():
    source=CubeCosetSource(((1,),),2,1,0,2,2,(1,))
    plan=P.precision_plan(2,P.QFTUsage(4),cutoff=0)
    compiled=compile_phase_source(source,qft_plan=plan)
    batch=simulate_phase_batch(compiled,4,seed=99502,batch_tag="approximate-diagnostic-only")
    assert compiled.qft_usage_ledger.record()["charged_forward_calls"]==4
    assert not batch.metadata["logical_readout_QFT_is_exact_reference"]
    with pytest.raises(ValueError,match="NOT_AN_EXACT_DCP_PROMISE"):
        OpaquePhaseBackend(batch,source.audit())
    with pytest.raises(ValueError,match="BUDGET_EXCEEDED"):
        simulate_phase_batch(compiled,1,seed=99503)


def test_library_mapping_changes_are_caught(monkeypatch):
    original=P.synth_qft_full
    def wrong(*args,**kwargs):
        kwargs["approximation_degree"]=0
        return original(*args,**kwargs)
    monkeypatch.setattr(P,"synth_qft_full",wrong)
    with pytest.raises(ValueError,match="mapping changed"):
        P.compile_qft(P.precision_plan(4,cutoff=1))


def test_independent_JS_checker_accepts_current_math_certificate():
    result=node_check(stored())
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["scaling_profiles"]==4


@pytest.mark.parametrize("kind",("cutoff","inverse-calls","encoded-error","ideal-error","pi-endpoint",
    "target-flag","rare-payload","large-gates","conditional-claim","hardware-claim","hash"))
def test_independent_JS_checker_rejects_precision_or_resource_tampering(kind):
    report=deepcopy(stored())
    p=report["scaling_precision_profiles"][0]
    if kind=="cutoff": p["retained_maximum_separation"]-=1
    elif kind=="inverse-calls": p["query_usage"]["direct_inverse_calls"]+=1
    elif kind=="encoded-error": p["single_use_encoded_CP_parameter_operator_error_upper"]="0"
    elif kind=="ideal-error": p["single_use_ideal_truncation_operator_upper"]="0"
    elif kind=="pi-endpoint": p["pi_rational_upper"]="3"
    elif kind=="target-flag": report["scaling_precision_profiles"][-1]["encoded_QFT_parameter_target_met"]=True
    elif kind=="rare-payload": report["rare_postselection_countercontrols"][0]["normalized_accepted_payload_trace_distance"]="0"
    elif kind=="large-gates": report["actual_beyond_old_128_wire_compile"]["logical_QFT_controlled_phase_gates"]+=1
    elif kind=="conditional-claim": p["normalized_rare_branch_accuracy_certified_without_mass_bound"]=True
    elif kind=="hardware-claim": report["hardware_or_full_source_channel_error_certified"]=True
    else: report["producer_sha256"]="0"*64
    assert node_check(report).returncode!=0
