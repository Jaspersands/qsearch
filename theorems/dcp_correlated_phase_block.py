"""Retain the whole coarse-syndrome phase block, with actual CX/CCX gates.

No compact fiber indexing, fresh product source, decoder or speedup supplied.
Finite density/Holevo controls are bounded classical simulations only.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from math import log2
from pathlib import Path

import numpy as np

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_disjoint_kernel_pairing import apply_evaluator
from theorems.dcp_nonlinear_fiber_pairing import phase_value

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/dcp_correlated_phase_block.json"
CONTRACT=ROOT/"research/hypotheses/dcp_correlated_phase_block_contract.json"


def syndrome_circuit(labels):
    A=matrix(labels)
    n,m=len(A),len(A[0])
    if n*m > 1000000:
        raise ValueError("UNKNOWN: explicit syndrome gate-export cap")
    gates=[]
    for l,row in enumerate(A):
        lo,hi=m+2*l,m+2*l+1
        for i,a in enumerate(row):
            if a%4==1:
                gates.extend([["CCX",i,lo,hi],["CX",i,lo]])
            elif a%4==2:
                gates.append(["CX",i,hi])
            elif a%4==3:
                gates.extend([["CX",i,lo],["CCX",i,lo,hi]])
    return {"kind":"COMPONENTWISE_MOD4_CONTROLLED_ADD", "input_phase_qubits":m,
            "measured_syndrome_qubits":2*n,"total_qubits":m+2*n,
            "extra_zero_work_qubits":0,"gates":gates,
            "gate_counts":dict(Counter(g[0] for g in gates)),
            "action_on_arbitrary_syndrome":"(x,z)->(x,z+A*x) componentwise modulo4, NOT bitwise XOR",
            "hardware_gate_export_implemented":True,"hardware_transpilation_executed":False,
            "unknown_source_inverse_used":False,"retained_original_phase_qubits":m}


def block_record(labels,phase_bits,measured_syndrome):
    A=matrix(labels)
    integer(phase_bits,"original phase bits",3,4096)
    if any(a >= 1 << phase_bits for row in A for a in row):
        raise ValueError("canonical full source labels required")
    y=tuple(measured_syndrome)
    if len(y)!=len(A):
        raise ValueError("one measured syndrome component per row required")
    for value in y:
        integer(value,"measured mod4 syndrome",0,3)
    return {"kind":"IMPLICIT_CORRELATED_PHASE_BLOCK", "public_full_labels":[list(row) for row in A],
            "original_phase_bits":phase_bits,"coarse_projection_bits":2,
            "measured_syndrome":list(y),"factored_phase_modulus_bits":phase_bits-2,
            "retained_quantum_basis":"original Boolean assignment, restricted to measured fiber",
            "retained_original_quantum_wires":len(A[0]),"compact_quantum_index_supplied":False,
            "fiber_cardinality_known_without_paid_computation":False,
            "fiber_inverse_or_uniform_fiber_state_oracle_supplied":False,
            "fresh_IID_product_phase_source_certified":False,
            "all_measurement_outcomes_retained":True,
            "measured_syndrome_provenance_not_certified_by_record_alone":True,
            "retained_correlations_may_not_be_replaced_by_marginal_qubits":True,
            "descended_phase_coefficients_defined_only_on_measured_fiber":True}


def density(labels,phase_bits,secret,visibility):
    A=matrix(labels)
    n,m=len(A),len(A[0])
    integer(phase_bits,"finite original phase bits",3,16)
    if m>8 or len(secret)!=n:
        raise ValueError("UNKNOWN: finite original density cap or secret dimension mismatch")
    for s in secret:
        integer(s,"finite canonical secret",0,(1 << phase_bits)-1)
    if any(a >= 1 << phase_bits for row in A for a in row):
        raise ValueError("canonical original labels required")
    v=Fraction(visibility)
    if not 0<=v<=1:
        raise ValueError("visibility outside[0,1]")
    q=1 << phase_bits
    phases=np.array([sum(s*a for s,a in zip(secret,phase_value(A,x,q)))%q for x in range(1 << m)])
    amps=np.exp(2j*np.pi*phases/q)/np.sqrt(1 << m)
    attenuation=np.array([[float(v**((x^y).bit_count())) for y in range(1 << m)] for x in range(1 << m)])
    return np.outer(amps,amps.conj())*attenuation


def entropy(rho):
    eigen=np.linalg.eigvalsh(rho)
    if min(eigen)<-1e-10:
        raise ArithmeticError("density lost positivity")
    return -sum(float(x)*log2(float(x)) for x in eigen if x>1e-13)


def finite_control(labels,phase_bits,visibility):
    A=matrix(labels)
    n,m=len(A),len(A[0])
    integer(phase_bits,"finite phase bits",3,16)
    q=1 << phase_bits
    if m>6 or q**n*(1 << (2*m))>300000:
        raise ValueError("UNKNOWN: finite all-secret block-density control cap")
    circuit=syndrome_circuit(A)
    fibers={}
    for x in range(1 << m):
        word=apply_evaluator(x,circuit)
        if word&((1 << m)-1)!=x:
            raise ArithmeticError("syndrome circuit changed source assignment")
        y=tuple((word>>(m+2*l))&3 for l in range(n))
        if y!=phase_value(A,x,4):
            raise ArithmeticError("gate export differs from native syndrome")
        fibers.setdefault(y,[]).append(x)
    full_frequencies=[phase_value(A,x,q) for x in range(1 << m)]
    injective=len(set(full_frequencies))==1 << m
    stats={y:{"average":np.zeros((len(indices),len(indices)),dtype=complex),"mean_entropy":0.0}
           for y,indices in fibers.items()}
    for secret in product(range(q),repeat=n):
        rho=density(A,phase_bits,secret,visibility)
        for y,indices in fibers.items():
            mass=len(indices)/(1 << m)
            block=rho[np.ix_(indices,indices)]/mass
            if abs(np.trace(block)-1)>1e-10:
                raise ArithmeticError("incorrect unconditional Born normalization")
            stats[y]["average"]+=block/q**n
            stats[y]["mean_entropy"]+=entropy(block)/q**n
    chi=0.0
    syndrome_entropy=0.0
    max_uniform_residual=0.0
    for y,indices in fibers.items():
        mass=len(indices)/(1 << m)
        syndrome_entropy-=mass*log2(mass)
        chi+=mass*(entropy(stats[y]["average"])-stats[y]["mean_entropy"])
        max_uniform_residual=max(max_uniform_residual,float(np.max(np.abs(stats[y]["average"]-np.eye(len(indices))/len(indices)))))
    p=float((1-Fraction(visibility))/2)
    h=0.0 if p in (0,1) else -p*log2(p)-(1-p)*log2(1-p)
    lower=max(0.0,m-syndrome_entropy-m*h) if injective else None
    if injective and (max_uniform_residual>1e-10 or chi+1e-10<lower):
        raise ArithmeticError("injective correlated-block information bound falsified")
    return {"full_labels":[list(row) for row in A],"phase_bits":phase_bits,"visibility_exact":str(Fraction(visibility)),
            "exported_circuit":circuit,"all_secret_states_checked":q**n,
            "full_frequency_map_injective":injective,"fiber_sizes":[{"syndrome":list(y),"size":len(indices)} for y,indices in sorted(fibers.items())],
            "syndrome_probabilities_sum":"1","syndrome_entropy_bits":syndrome_entropy,
            "retained_block_Holevo_bits":chi,"scoped_Holevo_lower_bits":lower,
            "injective_uniform_block_average_max_residual":max_uniform_residual if injective else None,
            "efficient_decoder_or_accessible_information_lower_bound":False,
            "sample_block_record":block_record(A,phase_bits,next(iter(fibers)))}


def native_information_frontier(n):
    integer(n,"vector components",2,1 << 24)
    e=(n-1).bit_length()
    return {"components":n,"original_phase_qubits":4*n,"original_phase_bits":n+8,
            "source_original_visibility":"1-1/n","measured_syndrome_bits":2*n,
            "exported_gate_count_upper":8*n*n,"extra_arithmetic_work_qubits":0,
            "live_quantum_wires_before_measurement":6*n,"live_quantum_wires_after_measurement":4*n,
            "full_frequency_noninjectivity_probability_power_of_two_upper_exponent":n*n,
            "entropy_loss_bits_upper":2*(e+3),
            "retained_block_Holevo_bits_lower_IF_injective":max(0,2*n-2*(e+3)),
            "bound_is_pointwise_in_public_labels":False,
            "Holevo_is_accessible_information_or_efficient_decoder":False,
            "compact_fiber_index_or_fiber_inverse_supplied":False,
            "actual_natural_source_noise_certified":False}


def build_report():
    return {"contract_id":"native_correlated_phase_block_gate_and_information_control_v1",
            "status":"PHYSICAL_GATE_EXPORT_INFORMATION_BOUND_REVIEW_PENDING",
            "finite_controls":[finite_control(A,t,v) for A,t,v in (
                (((1,4,0,0),(0,0,1,4)),3,Fraction(1)),
                (((1,4,0,0),(0,0,1,4)),3,Fraction(7,8)),
                (((1,2,5,12),),5,Fraction(7,8)),
                (((1,1,1,1),),3,Fraction(3,4)))],
            "native_information_frontiers":[native_information_frontier(n) for n in (64,256,1024,4096,16384,65536)],
            "hardware_gate_export_implemented":True,"hardware_transpilation_or_execution_performed":False,
            "source_quantum_preparations_executed":0,"accepted_speedup_candidate":False,
            "novelty_claim":False,"external_theorem_review_complete":False,
            "source_noise_and_IID_labels_are_assumed_not_inferred":True,
            "implicit_block_is_fresh_product_source":False,"efficient_block_decoder_supplied":False,
            "prior_local_derivation":"research/DCP_MULTI_OUTPUT_FREQUENCY_BOUND.md#6-correlated-blocks-retain-information"}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write",action="store_true")
    args=parser.parse_args(argv)
    report=build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"finite_controls":4,"hardware_gate_export":True,
                      "efficient_decoder":False,"artifact":str(REPORT)}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
