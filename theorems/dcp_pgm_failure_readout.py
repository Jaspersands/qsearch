"""All-record comparison-readout reduction and projector-processor hybrid gate.

LOCAL DERIVATION / REVIEW PENDING. Not a general collective-measurement no-go.
Physical matrices and optimal finite classifiers are exponential calibration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from dcp_adaptive_product_readout_bound import rational
from dcp_pgm_projected_encoding import _bounded_labels, _data
from dcp_terminal_affine_fibers import _positive_integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/dcp_pgm_failure_readout.json"

GATES = {
    "I":np.eye(2,dtype=complex), "-I":-np.eye(2,dtype=complex),
    "X":np.array([[0,1],[1,0]],dtype=complex),
    "Z":np.diag([1,-1]).astype(complex),
    "H":np.array([[1,1],[1,-1]],dtype=complex)/math.sqrt(2),
    "S":np.diag([1,1j]), "T":np.diag([1,np.exp(1j*math.pi/4)]),
}


def _nonnegative_integer(value,name):
    if type(value) is not int or value<0:
        raise ValueError(f"{name} must be a nonnegative integer")


def _root_dyadic(x):
    if x==0:
        return Fraction(0),None
    if x>=1:
        return Fraction(1),0
    exponent = ((x.denominator//x.numerator).bit_length()-1)//2
    upper = Fraction(1,1 << exponent)
    assert upper*upper>=x
    return upper,exponent


def failure_readout_certificate(n,L,m,output_kicks,implementation_error=Fraction(0)):
    for value,name in ((n,"dimension"),(L,"modulus bits"),(m,"phase qubits")):
        _positive_integer(value,name)
    _nonnegative_integer(output_kicks,"output kicks")
    if type(implementation_error) not in (int,Fraction) or not 0<=implementation_error<=1:
        raise ValueError("exact total composed output trace-error budget in [0,1] required")
    G,H,N = 1 << (n*L),1 << (n*(L-1)),1 << m
    C = Fraction(3,2)**m
    B = min(Fraction(1),(C+(N-C)/H)/G)
    mean_herald = Fraction(N+G-1,N*G)
    gain_squared = 4*output_kicks**2*mean_herald
    baseline_upper,baseline_exponent = _root_dyadic(B)
    gain_upper,gain_exponent = _root_dyadic(gain_squared)
    ideal_upper = min(Fraction(1),baseline_upper+gain_upper)
    upper = min(Fraction(1),ideal_upper+implementation_error)
    squared_common = min(Fraction(1),2*B+8*output_kicks**2*mean_herald)
    return {"status":"SCOPED_ALL_FAILURE_RECORD_NATIVE_GATE_REVIEW_PENDING",
            "dimension":n,"modulus_bits":L,"phase_qubits":m,"density_surplus":m-n*L,
            "maximum_output_projector_kicks":output_kicks,
            "baseline_native_mean_success_squared_bound":rational(B),
            "native_mean_clean_herald":rational(mean_herald),
            "native_mean_trace_distance_gain_squared_bound":rational(gain_squared),
            "baseline_mean_success_dyadic_upper":rational(baseline_upper),
            "trace_gain_dyadic_upper":rational(gain_upper),
            "all_record_native_mean_success_conservative_upper":rational(upper),
            "ideal_all_record_native_mean_success_upper":rational(ideal_upper),
            "assumed_total_composed_output_trace_error_budget":rational(Fraction(implementation_error)),
            "nonzero_error_budget_requires_separate_input_and_gate_composition_proof":True,
            "common_mean_squared_success_bound":rational(squared_common),
            "common_squared_bound_is_for_ideal_operations":True,
            "baseline_dyadic_exponent":baseline_exponent,"gain_dyadic_exponent":gain_exponent,
            "conservative_all_record_success_dyadic_exponent":(upper.denominator//upper.numerator).bit_length()-1,
            "bound_is_vacuous":upper==1,
            "all_signal_computational_outcomes_and_auxiliary_records_retained":True,
            "arbitrary_classical_record_decoder_allowed":True,
            "whole_public_matrix_may_select_processor_and_auxiliary_controls":True,
            "arbitrary_input_projector_kicks_and_auxiliary_only_unitaries_allowed":True,
            "joint_secret_independent_physical_Z_fault_laws_may_depend_on_labels":True,
            "source_mean_not_pointwise_secret_or_matrix":True,
            "arbitrary_terminal_collective_measurements_or_signal_interleavings_covered":False,
            "secret_dependent_fault_laws_or_general_reduction_noise_covered":False,
            "candidate_record_accepted":False,"independent_review":False,"novelty_claim":False,"speedup_claim_allowed":False}


def _unitary_data(A,q):
    n,m = _bounded_labels(A,q)
    secrets,eta,phases = _data(A,q)
    G,N = q**n,2**m
    def walsh(size):
        return np.array([[(-1)**((i&j).bit_count())/math.sqrt(size) for j in range(size)] for i in range(size)])
    U = np.einsum("sz,yx,sx->syzx",walsh(G),walsh(N),phases.conjugate()).reshape(G*N,G*N)
    assert np.max(np.abs(U.conjugate().T@U-np.eye(G*N)))<1e-9
    return secrets,eta,phases,U


def _program(program):
    if not isinstance(program,(list,tuple)) or len(program)>100:
        raise ValueError("bounded list of at most100 projector/auxiliary operations required")
    for op in program:
        if not isinstance(op,dict):
            raise ValueError("operation record required")
        if op.get("kind")=="aux" and set(op)=={"kind","gate"} and type(op["gate"]) is str and op["gate"] in GATES:
            continue
        if op.get("kind") in ("P","Q") and set(op)=={"kind","on","off"} and all(type(op[k]) is str and op[k] in GATES for k in ("on","off")):
            continue
        raise ValueError("only declared input/output projector controls and auxiliary gates are covered")
    return sum(op["kind"]=="Q" for op in program)


def _fault_law(law,m):
    if not isinstance(law,(tuple,list)) or not law:
        raise ValueError("static sparse physical-Z law required, not a secret-dependent evaluator")
    rows = []
    for row in law:
        if not isinstance(row,(tuple,list)) or len(row)!=2:
            raise ValueError("exact weight and binary mask required")
        weight,mask = row
        if type(weight) not in (int,Fraction) or weight<=0 or not isinstance(mask,(list,tuple)) or len(mask)!=m or any(type(b) is not int or b not in (0,1) for b in mask):
            raise ValueError("positive exact weight and canonical physical mask required")
        rows.append((Fraction(weight),tuple(mask)))
    if sum(w for w,_ in rows)!=1:
        raise ValueError("fault law must be normalized without postselection")
    return rows


def bounded_control(A,q,program,law=None):
    n,m = _bounded_labels(A,q)
    kicks = _program(program)
    faults = _fault_law(law if law is not None else [(1,[0]*m)],m)
    secrets,eta,phases,U = _unitary_data(A,q)
    G,N,D = q**n,2**m,len(U)
    columns = U[:,:N]
    good_out = np.arange(G)*N
    clean_h = Fraction(sum(v*v for v in eta),N*N)
    records,base_records,physical = [],[],[]
    for index,s in enumerate(secrets):
        probabilities,base_probabilities = np.zeros((D,2)),np.zeros((D,2))
        for weight,mask in faults:
            signs = np.array([(-1)**sum(((x >> (m-1-i))&1)*mask[i] for i in range(m)) for x in range(N)])
            initial = np.zeros(D,dtype=complex)
            initial[:N] = phases[index]*signs/math.sqrt(N)
            v = U@initial
            herald = float(np.sum(np.abs(v[good_out])**2))
            assert herald<=float(clean_h)+1e-9
            # Audit the complete raw channel against legal random-trial local readout.
            for trial,r in enumerate(secrets):
                for y in range(N):
                    p = 1/G
                    for i in range(m):
                        theta = 2*math.pi*sum(A[j][i]*(s[j]-r[j]) for j in range(n))/q
                        bit = ((y >> (m-1-i))&1)^mask[i]
                        p *= (1+(-1)**bit*math.cos(theta))/2
                    assert abs(p-abs(v[trial*N+y])**2)<1e-9
            state = np.column_stack((v,np.zeros(D,dtype=complex)))
            ideal = state.copy()
            for op in program:
                if op["kind"]=="aux":
                    state = state@GATES[op["gate"]].T
                    ideal = ideal@GATES[op["gate"]].T
                else:
                    if op["kind"]=="P":
                        projected = columns@(columns.conjugate().T@state)
                        ideal_gate = GATES[op["on"]]
                    else:
                        projected = np.zeros_like(state)
                        projected[good_out] = state[good_out]
                        ideal_gate = GATES[op["off"]]
                    state = projected@GATES[op["on"]].T+(state-projected)@GATES[op["off"]].T
                    ideal = ideal@ideal_gate.T
            assert abs(float(np.vdot(state,state).real)-1)<1e-9
            assert abs(float(np.vdot(ideal,ideal).real)-1)<1e-9
            distance = float(np.linalg.norm(state-ideal))
            # Phase-aligned distance avoids catastrophic cancellation near overlap1.
            overlap = np.vdot(ideal,state)
            phase = overlap.conjugate()/abs(overlap) if abs(overlap)>0 else 1
            aligned = float(np.linalg.norm(state*phase-ideal))
            trace = aligned*math.sqrt(max(0,1-aligned*aligned/4))
            tv = float(np.sum(np.abs(np.abs(state)**2-np.abs(ideal)**2))/2)
            bound = 2*kicks*math.sqrt(herald)
            assert distance<=bound+1e-8 and tv<=trace+1e-8 and trace<=distance+1e-8, (distance,trace,tv,bound)
            probabilities += float(weight)*np.abs(state)**2
            base_probabilities += float(weight)*np.abs(ideal)**2
            physical.append({"secret":list(s),"mask":list(mask),"weight":rational(weight),
                             "raw_herald":herald,"state_distance":distance,"pure_trace_distance":trace,
                             "full_record_total_variation":tv,"hybrid_state_distance_bound":bound,
                             "physical_norm":float(np.vdot(state,state).real)})
        assert abs(float(np.sum(probabilities))-1)<1e-9
        records.append(probabilities.flatten())
        base_records.append(base_probabilities.flatten())
    score = float(np.sum(np.max(records,axis=0))/G)
    base_score = float(np.sum(np.max(base_records,axis=0))/G)
    tv_mean = float(np.mean([np.sum(np.abs(a-b))/2 for a,b in zip(records,base_records)]))
    assert abs(score-base_score)<=tv_mean+1e-9
    assert score<=base_score+2*kicks*math.sqrt(float(clean_h))+1e-9
    return {"labels":A,"modulus":q,"program":program,"output_projector_kicks":kicks,
            "fault_law":[{"weight":rational(w),"mask":list(mask)} for w,mask in faults],
            "clean_herald_exact":rational(clean_h),"fiber_counts":eta,
            "optimal_all_record_uniform_secret_success":score,
            "matched_random_trial_product_readout_success":base_score,
            "mean_full_record_total_variation":tv_mean,
            "full_probabilities_by_secret":[[float(v) for v in row] for row in records],
            "reference_probabilities_by_secret":[[float(v) for v in row] for row in base_records],
            "physical_controls":physical,"all_herald_failures_and_auxiliary_outcomes_retained":True,
            "full_channel_matches_legal_local_baseline_before_processing":True,
            "unknown_secret_classically_reconstructed":False,
            "calibration_is_exponential_not_an_efficient_decoder":True,
            "secret_independence_of_external_fault_law_must_be_proved":True}


def reflection_program(rounds):
    _nonnegative_integer(rounds,"rounds")
    return [{"kind":"Q","on":"I","off":"-I"},
            {"kind":"P","on":"I","off":"-I"},{"kind":"aux","gate":"-I"}]*rounds


def run_controls():
    coherent = [{"kind":"aux","gate":"H"},{"kind":"Q","on":"X","off":"S"},
                {"kind":"aux","gate":"T"},{"kind":"P","on":"H","off":"Z"},
                {"kind":"aux","gate":"S"},{"kind":"Q","on":"T","off":"H"},
                {"kind":"P","on":"X","off":"S"},{"kind":"aux","gate":"H"}]
    controls = []
    for A,q in (([[2,1]],4),([[1,3,7]],8),([[1,0],[2,1]],4)):
        m = len(A[0])
        laws = [[(1,[0]*m)],[(Fraction(1,2),[0]*m),(Fraction(1,2),[1]*m)],
                [(Fraction(1,3),[0]*m),(Fraction(2,3),[i%2 for i in range(m)])]]
        for law in laws:
            for program in ([],reflection_program(1),reflection_program(2),reflection_program(3),coherent):
                controls.append(bounded_control(A,q,program,law))
    return {"status":"ALL_RECORD_PROJECTOR_PROCESSOR_SCOPE_FALSIFIER_REVIEW_PENDING",
            "physical_processor_controls":controls,
            "native_growing_ledgers":[failure_readout_certificate(n,4*n+1,n*(4*n+1)+16,(2*n*(4*n+1)+16)**2) for n in (8,16,32)],
            "precision_floor_counterledger":failure_readout_certificate(8,33,280,544**2,Fraction(1,10**6)),
            "scope_counterexamples":{
                "binary_identity_direct_Hadamard_decoder_outside_projector_only_algebra":True,
                "arbitrary_terminal_collective_measurement_could_decode_reference_state":True,
                "secret_dependent_noise_can_itself_encode_secret":True},
            "claim_gate":{"all_failure_records_in_declared_terminal_measurement_class_covered":True,
                          "general_collective_or_QSVT_impossibility":False,"native_reduction_error_transfer_proved":False,
                          "independent_review":False,"candidate_record_accepted":False,"novelty_claim":False,"speedup_claim_allowed":False},
            "dependency_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__),ROOT/"theorems/dcp_pgm_projected_encoding.py",
                                           ROOT/"theorems/dcp_native_product_readout_bound.py",
                                           ROOT/"theorems/dcp_adaptive_product_readout_bound.py",
                                           ROOT/"theorems/dcp_terminal_affine_fibers.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"processor_controls":len(report["physical_processor_controls"]),
                      "pure_physical_controls":sum(len(r["physical_controls"]) for r in report["physical_processor_controls"]),
                      "native_success_upper_exponents":[r["conservative_all_record_success_dyadic_exponent"] for r in report["native_growing_ledgers"]],
                      "claim_gate":report["claim_gate"]},indent=2))


if __name__=="__main__":
    main()
