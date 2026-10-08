"""Exact one-copy simulation of word-orbit-preserving native readouts.

LOCAL DERIVATION / REVIEW PENDING. Not a bound on arbitrary collective
receivers: mixing simultaneous-rotation word orbits escapes this cut.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

import numpy as np

from cyclotomic_rescaling_gate import multiply, pairing, plus, reduce_element
from cyclic_centre_state_hsp_receiver import integer
from native_noncentral_filter_tradeoff import tensor
from native_state_hsp_bridge import NativeGroup

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/"research/reductions/native_diagonal_orbit_channel.json"
LAMBDAS = ((0,0),(1,0),(1,1))
ROOTS = ((1,0),(0,1),(-1,-1))


def orbit_chart(word):
    if not word or any(type(x) is not int or x not in range(3) for x in word):
        raise ValueError("nonempty canonical ternary word required")
    return tuple((x-word[0]) % 3 for x in word), word[0]


def orbit_word(offset, rotation):
    if not offset or offset[0] != 0 or any(type(x) is not int or x not in range(3) for x in offset):
        raise ValueError("canonical word offset with first coordinate0 required")
    if type(rotation) is not int or rotation not in range(3):
        raise ValueError("canonical ternary rotation required")
    return tuple((x+rotation) % 3 for x in offset)


def effective_label(labels, offset, level):
    if len(labels) != len(offset):
        raise ValueError("one public native row per offset required")
    orbit_word(offset,0)
    G = NativeGroup(level,len(labels[0]))
    labels = tuple(G.vector(a) for a in labels)
    total = tuple((0,0) for _ in range(G.dimension))
    for a,v in zip(labels,offset):
        total = tuple(plus(x,y,level) for x,y in zip(total,G.rotate(a,v)))
    return total


def synthetic_rows(u, offset, auxiliary_rows, level):
    """Classical bijection for the IID source model; no quantum state cloning."""
    if len(auxiliary_rows)+1 != len(offset):
        raise ValueError("M-1 auxiliary public rows required")
    orbit_word(offset,0)
    G=NativeGroup(level,len(u))
    u=G.vector(u)
    rows=(tuple((0,0) for _ in u),)+tuple(G.vector(a) for a in auxiliary_rows)
    residue=effective_label(rows,offset,level)
    first=tuple(plus(x,(-y[0],-y[1]),level) for x,y in zip(u,residue))
    return (first,)+rows[1:]


def information_ledger(level,dimension,copies):
    for x,name in ((level,"native level"),(dimension,"native dimension"),(copies,"original copies")):
        integer(x,name,1)
    return {"native_level":level,"native_dimension":dimension,"original_IID_copies":copies,
            "simulating_original_native_source_copies":1,"public_auxiliary_rows":copies-1,
            "uniform_full_ring_secret_success_upper_bound":{"cap":1,"numerator":3,"denominator":{"base":3,"exponent":level*dimension}},
            "uniform_integer_embedded_secret_success_upper_bound":{"cap":1,"numerator":3,"denominator":{"base":3,"exponent":((level+1)//2)*dimension}},
            "simulation_requires_full_uniform_IID_frequency_prior":True,
            "same_initial_public_frequency_record_distribution_preserved":True,
            "final_readout_must_not_interfere_distinct_word_orbits":True,
            "joint_original_input_trace_distance_error_adds_to_raw_bound":True,
            "arbitrary_seed_mixing_or_independent_per_copy_actions_covered":False,
            "all_native_receivers_ruled_out":False}


def public_group_controls(G):
    values=[G.element((tuple((0,0) for _ in range(G.dimension)),0))]
    for coordinate in range(G.dimension):
        for b in ((1,0),(0,1)):
            v=[(0,0)]*G.dimension
            v[coordinate]=b
            values.extend(G.element((tuple(v),t)) for t in range(3))
    values.extend(G.element((tuple((2,1) for _ in range(G.dimension)),t)) for t in range(3))
    return tuple(dict.fromkeys(values))


def group_protocol(actions,seed,U):
    L=actions.shape[0]
    state=np.einsum("gij,j->gi",actions,seed)/np.sqrt(L)
    histories=[]
    for _ in range(3):
        state=U@state
        reflected=state.copy()
        reflected[[0,L-1]] *= -1
        returned=np.einsum("gji,gj->i",actions.conj(),reflected)/np.sqrt(L)
        state=2*np.einsum("gij,j->gi",actions,returned)/np.sqrt(L)-reflected
        histories.append(state@state.conj().T)
    return histories


def finite_control(level,labels,secret):
    if not 2<=len(labels)<=4 or level not in (2,3,4):
        raise ValueError("bounded original-word controls use M2-4 and levels2-4")
    G=NativeGroup(level,len(labels[0]))
    labels=tuple(G.vector(a) for a in labels)
    secret=G.vector(secret)
    M=len(labels)
    words=tuple(product(range(3),repeat=M))
    indices={w:i for i,w in enumerate(words)}
    offsets=tuple((0,)+v for v in product(range(3),repeat=M-1))
    groups=public_group_controls(G)
    phases=[]
    for w in words:
        phases.append(sum((pairing(s,multiply(a,LAMBDAS[j],level),level) for row,j in zip(labels,w) for s,a in zip(secret,row)),Fraction()) % 1)
    original=np.array([np.exp(2j*np.pi*float(p)) for p in phases])/np.sqrt(3**M)
    W=len(offsets)
    branches=[]
    max_state_error=0.
    for v in offsets:
        u=effective_label(labels,v,level)
        f=tuple((0,0) for _ in range(G.dimension))
        for row,j in zip(labels,v):
            f=tuple(plus(x,multiply(a,LAMBDAS[j],level),level) for x,a in zip(f,row))
        global_phase=sum((pairing(s,a,level) for s,a in zip(secret,f)),Fraction()) % 1
        psi=G.supplied_phase_state(u,secret)
        iw=[indices[orbit_word(v,j)] for j in range(3)]
        max_state_error=max(max_state_error,float(np.linalg.norm(original[iw]-np.exp(2j*np.pi*float(global_phase))*psi/np.sqrt(W))))
        action_phases=[]
        for g in groups:
            b,t=g
            row=[]
            for j in range(3):
                w=orbit_word(v,j)
                p=sum((pairing(a,z,level) for label,out in zip(labels,((x-t)%3 for x in w)) for a,z in zip(label,G.rotate(b,out))),Fraction()) % 1
                expected=sum((pairing(a,z,level) for a,z in zip(u,G.rotate(b,j-t))),Fraction()) % 1
                if p != expected:
                    raise ArithmeticError("synchronized native action changes a word-orbit offset or its effective representation")
                row.append(str(p))
            action_phases.append(row)
        branches.append({"offset":v,"effective_native_frequency":u,"exact_orbit_weight":str(Fraction(1,W)),
                         "exact_secret_dependent_global_phase_mod1_NOT_USED_BY_SIMULATOR":str(global_phase),
                         "exact_original_word_phases_mod1":[str(phases[i]) for i in iw],
                         "exact_effective_qutrit_phases_mod1":[str(sum((pairing(s,multiply(a,LAMBDAS[j],level),level) for s,a in zip(secret,u)),Fraction()) % 1) for j in range(3)],
                         "exact_action_phases_by_public_group_and_rotation":action_phases})
    if max_state_error>2e-11:
        raise ArithmeticError("native batch branches are not exact uniform effective-qutrit orbit states")
    # Nine actual public group controls, not a full-group table or new oracle.
    readout_groups=groups[:9]
    L=len(readout_groups)
    alpha=sum(x+y for row in labels for x,y in row) % 9
    U=np.array([[np.exp(2j*np.pi*(i*j+alpha*j)/9)/3 for j in range(9)] for i in range(9)])
    original_actions=np.array([tensor([G.induced_action(a,g) for a in labels]) for g in readout_groups])
    actual=group_protocol(original_actions,original,U)
    simulated=[np.zeros((L,L),complex) for _ in range(3)]
    for branch in branches:
        u=branch["effective_native_frequency"]
        actions=np.array([G.induced_action(u,g) for g in readout_groups])
        result=group_protocol(actions,G.supplied_phase_state(u,secret),U)
        for t in range(3):
            simulated[t]+=result[t]/W
    density_errors=[float(np.linalg.norm(a-b)) for a,b in zip(actual,simulated)]
    if max(density_errors)>2e-11:
        raise ArithmeticError("group-only output channel is not simulated by the orbit mixture")
    # Explicit escape: a seed Fourier measurement interferes distinct offsets.
    zero_secret_pure=np.ones(3**M)/np.sqrt(3**M)
    full_plus=float(abs(np.vdot(zero_secret_pure,zero_secret_pure))**2)
    pinched_plus=1/W
    return {"native_level":level,"native_dimension":G.dimension,"labels":labels,"native_secret":secret,
            "original_source_copies":M,"complete_original_word_count":len(words),"complete_word_orbit_count":W,
            "all_public_group_controls":groups,"complete_orbit_branches":branches,
            "maximum_original_vs_orbit_branch_state_error":max_state_error,
            "actual_label_dependent_group_protocol":{
                "public_group_control_count":L,"unitary_label_phase_index":alpha,"rounds":3,
                "full_output_group_density_real_imag_by_round":[[[[float(z.real),float(z.imag)] for z in row] for row in rho] for rho in actual],
                "original_vs_one_copy_orbit_mixture_density_errors":density_errors,
                "all_final_seed_registers_discarded":True},
            "seed_mixing_escape":{
                "source_secret_for_escape_control":"all zero",
                "original_batch_all_plus_measurement_probability":full_plus,
                "orbit_pinched_batch_all_plus_measurement_probability":pinched_plus,
                "exact_pinched_probability":str(Fraction(1,W)),
                "this_measurement_interferes_distinct_word_orbits":True},
            "simulation_global_phase_or_secret_is_an_algorithm_input":False,
            "simulation_is_a_classical_dequantization":False,
            "full_depth_receiver_supplied":False}


def run_controls():
    return {"status":"NATIVE_WORD_ORBIT_PRESERVING_CHANNEL_ONE_COPY_SIMULATION_REVIEW_PENDING",
            "complete_source_controls":[
                finite_control(2,(((1,0),),((0,1),),((2,0),)),((1,0),)),
                finite_control(4,(((1,0),),((2,1),),((4,3),)),((5,2),)),
                finite_control(3,(((1,0),(2,1)),((0,1),(4,0)),((2,2),(1,0))),((3,0),(2,1))),
                finite_control(4,(((1,0),),((2,1),),((4,3),),((7,2),)),((5,2),))],
            "growing_information_ledgers":[information_ledger(r,n,n*r) for r,n in ((2,1),(8,8),(32,32),(128,128))],
            "observed_label_dependent_group_operations_covered":True,
            "relative_orbit_preparation_and_inverse_covered":True,
            "preserving_readouts_simulated_with_one_original_native_source_copy":True,
            "simulation_is_valid_for_arbitrary_fixed_frequency_prior":False,
            "arbitrary_seed_mixing_or_independent_per_copy_group_actions_covered":False,
            "all_native_quantum_receivers_ruled_out":False,
            "new_quantum_algorithm_or_speedup_claimed":False,"novelty_claimed":False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write",action="store_true")
    args=p.parse_args()
    out=run_controls()
    if args.write:
        REPORT.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":out["status"],"complete_source_controls":len(out["complete_source_controls"])}))


if __name__=="__main__":
    main()
