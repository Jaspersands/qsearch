"""One-use isotropic-line receiver for supplied quadratic phase programs.

LOCAL DERIVATION / REVIEW PENDING. Teleportation is known. This compiles an
exact secret equation without identical program copies or an unknown inverse.
Native calibration sources are engineered, not a proved IID program factory.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random

from flint import nmod_mat
import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_correlated_packet_acquisition import PacketAcquisition, integer, word
from ternary_cyclic_extractor import zero_sum_support
from ternary_schur_tensor import NativeCubicTensor

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_quadratic_program_receiver.json"
DERIVATION = ROOT / "research/TERNARY_QUADRATIC_PROGRAM_RECEIVER.md"


def rank(columns, height):
    return int(nmod_mat([[column[i] for column in columns] for i in range(height)],3).rank()) if columns else 0


def combination(columns, digits, height):
    return tuple(sum(column[i]*digit for column,digit in zip(columns,digits)) % 3 for i in range(height))


def nullspace(rows, width):
    if not rows:
        return tuple(tuple(int(i==j) for i in range(width)) for j in range(width))
    R,r = nmod_mat(rows,3).rref()
    reduced = tuple(tuple(int(R[i,j]) for j in range(width)) for i in range(r))
    pivots = tuple(next(i for i,a in enumerate(row) if a) for row in reduced)
    out=[]
    for f in range(width):
        if f in pivots: continue
        v=[0]*width;v[f]=1
        for p,row in zip(pivots,reduced): v[p]=-row[f] % 3
        out.append(tuple(v))
    return tuple(out)


def linear_chart(frame, height):
    frame=tuple(word(column,height) for column in frame)
    if not frame or rank(frame,height)!=len(frame):
        raise ValueError("independent nonempty logical frame required")
    columns=list(frame)
    for j in range(height):
        e=tuple(int(i==j) for i in range(height))
        if rank(columns+[e],height)>len(columns): columns.append(e)
    A=[[columns[j][i] for j in range(height)] for i in range(height)]
    gates=[]
    for j in range(height):
        p=next(i for i in range(j,height) if A[i][j])
        if p!=j:
            A[p],A[j]=A[j],A[p];gates.append({"gate":"SWAP_F3","first":p,"second":j})
        if A[j][j]==2:
            A[j]=[2*a % 3 for a in A[j]];gates.append({"gate":"SCALE_F3","wire":j,"factor":2})
        for i in range(height):
            if i!=j and A[i][j]:
                c=-A[i][j] % 3;A[i]=[(a+c*b) % 3 for a,b in zip(A[i],A[j])]
                gates.append({"gate":"SUM_F3","control":j,"target":i,"factor":c})
    return tuple(columns),tuple(gates)


def apply_chart(gates, original):
    out=list(word(original,len(original)))
    for gate in gates:
        if gate["gate"]=="SWAP_F3":
            i,j=gate["first"],gate["second"];out[i],out[j]=out[j],out[i]
        elif gate["gate"]=="SCALE_F3": out[gate["wire"]]=2*out[gate["wire"]] % 3
        else: out[gate["target"]]=(out[gate["target"]]+gate["factor"]*out[gate["control"]]) % 3
    return tuple(out)


@dataclass(frozen=True)
class QuadraticFamily:
    matrices: tuple
    linear: tuple

    def __post_init__(self):
        if not self.matrices or len(self.matrices)!=len(self.linear) or not self.linear[0]:
            raise ValueError("nonempty component quadratic family required")
        d=len(self.linear[0])
        for M,b in zip(self.matrices,self.linear):
            word(b,d)
            if len(M)!=d: raise ValueError("square component matrices required")
            for row in M: word(row,d)
            if any(M[i][j]!=M[j][i] for i in range(d) for j in range(d)):
                raise ValueError("symmetric canonical quadratic matrices required")

    @property
    def width(self): return len(self.linear[0])

    @property
    def components(self): return len(self.linear)

    def quadratic(self,z):
        z=word(z,self.width)
        return tuple(sum(z[i]*M[i][j]*z[j] for i in range(self.width) for j in range(self.width)) % 3 for M in self.matrices)

    def value(self,z):
        z=word(z,self.width)
        return tuple((q+sum(a*b for a,b in zip(row,z))) % 3 for q,row in zip(self.quadratic(z),self.linear))

    def gradients(self,v):
        v=word(v,self.width)
        return tuple(tuple(2*sum(M[i][j]*v[j] for j in range(self.width)) % 3 for i in range(self.width)) for M in self.matrices)

    def receiver(self,v):
        v=word(v,self.width)
        if not any(v) or any(self.quadratic(v)):
            raise ValueError("nonzero common isotropic direction required")
        gradients=self.gradients(v)
        r=int(nmod_mat(gradients,3).rank())
        return {"direction":v,"gradient_rows":gradients,"gradient_rank":r,
                "label_offset":tuple(sum(a*b for a,b in zip(row,v)) % 3 for row in self.linear),
                "uniform_full_secret_label_law_certified":r==self.components,
                "one_supplied_program_consumed_per_equation":True,
                "all_Bell_outcomes_accepted":True,"identical_program_copies_or_unknown_inverse_used":False}


def isotropic_direction(family):
    """Guaranteed polynomial construction at wide dimension; bounded fallback only."""
    n,d=family.components,family.width;k=(n+1)**2;threshold=(n+1)*k-n
    if d<threshold:
        if d>6: raise ValueError("below guaranteed width; exhaustive calibration limited to six coordinates")
        candidates=[v for v in product(range(3),repeat=d) if any(v) and not any(family.quadratic(v))]
        if not candidates: raise ValueError("no common isotropic direction in this bounded calibration")
        v=max(candidates,key=lambda v:int(nmod_mat(family.gradients(v),3).rank()))
        return v,{"method":"bounded-complete-isotropic-calibration","scalable_search_claimed":False,
                  "directions_audited":3**d,"guaranteed_width":threshold,
                  "direction_selection_reads_linear_coefficients":False}
    basis=[]
    for _ in range(k):
        constraints=[tuple(sum(M[i][j]*e[j] for j in range(d)) % 3 for i in range(d))
                     for e in basis for M in family.matrices]
        v=next(v for v in nullspace(constraints,d) if rank(basis+[v],d)>len(basis))
        basis.append(v)
    certificate=zero_sum_support([family.quadratic(v) for v in basis])
    v=combination([basis[i] for i in certificate["support"]],(1,)*len(certificate["support"]),d)
    if not any(v) or any(family.quadratic(v)): raise ArithmeticError("guaranteed isotropic construction failed")
    return v,{"method":"common-orthogonal-basis-and-known-diagonal-SDE","scalable_search_claimed":True,
              "guaranteed_width":threshold,"orthogonal_basis_size":k,"support_certificate":certificate,
              "full_gradient_rank_guaranteed":False,"direction_selection_reads_linear_coefficients":False}


def native_quadratic_program(branch,frame,complement):
    packet=branch.packet
    if packet.level!=3:
        raise ValueError("native field-root level3 packet required; higher-depth extension not supplied")
    admission=NativeCubicTensor.from_packet(packet).restriction(frame)
    if not admission["classical_quadratic_restriction_admitted"]:
        raise ValueError("actual mixed cubic restriction must vanish in every component")
    columns,gates=linear_chart(frame,packet.retained);d=len(frame)
    complement=word(complement,packet.retained-d)
    base=combination(columns[d:],complement,packet.retained)
    def value(z):
        logical=tuple((a+b) % 3 for a,b in zip(base,combination(columns[:d],z,packet.retained)))
        return tuple((a-b) % 3 for a,b in zip(branch.original_residual(logical),branch.original_residual(base)))
    e=[tuple(int(i==j) for i in range(d)) for j in range(d)]
    first=[value(v) for v in e];second=[value(tuple(2*x % 3 for x in v)) for v in e]
    matrices=[[[0]*d for _ in range(d)] for _ in range(packet.secret_dimension)]
    linear=[[0]*d for _ in range(packet.secret_dimension)]
    for i in range(d):
        for l in range(packet.secret_dimension):
            matrices[l][i][i]=(2*first[i][l]-second[i][l]) % 3
            linear[l][i]=(second[i][l]-first[i][l]) % 3
        for j in range(i+1,d):
            point=tuple((a+b) % 3 for a,b in zip(e[i],e[j]));values=value(point)
            for l in range(packet.secret_dimension):
                matrices[l][i][j]=matrices[l][j][i]=2*(values[l]-first[i][l]-first[j][l]) % 3
    family=QuadraticFamily(tuple(tuple(tuple(row) for row in M) for M in matrices),tuple(tuple(row) for row in linear))
    exponent=branch.resources()["raw_joint_branch_probability_exponent_base_three"]+packet.retained-d
    record={"original_source":branch.acquisition.source_record(),"original_labels":branch.acquisition.source.labels,
            "odd_native_labels":packet.labels,"inner_pointers":tuple(branch.anchor[i] for i in branch.acquisition.pointers),
            "outer_syndrome":packet.syndrome,"logical_frame":frame,"complete_chart_columns":columns,
            "chart_gates":gates,"restriction_complement":complement,"restriction_base":base,
            "mixed_cubic_admission":admission,"component_matrices":family.matrices,"component_linear":family.linear,
            "all_restriction_outcomes_accepted":True,"raw_program_branch_probability":str(Fraction(1,3**exponent)),
            "identical_program_factory_supplied":False,"IID_original_source_program_factory_proved":False,
            "one_unknown_program_copy_supplied":True,"higher_parent_secret_digits_recovered":False}
    if d<=6:
        table=[value(z) for z in product(range(3),repeat=d)]
        if table!=[family.value(z) for z in product(range(3),repeat=d)]:
            raise ArithmeticError("native restriction is not the advertised quadratic family")
        record["complete_native_program_frequency_table"]=table
    return family,record


def engineered_native_program(n,seed):
    """Actual native instrument calibration; engineered low labels, not an IID factory."""
    integer(n,"calibration secret dimension",1)
    if n>2: raise ValueError("prespecified native calibration limited to one/two secret coordinates")
    grid=tuple(product(range(3),repeat=3));K=len(grid);W=(n+1)**2;rng=random.Random(seed)
    labels=[]
    for x in grid:
        a=tuple(x[l]+3*rng.randrange(3) for l in range(n))
        c=tuple(2*x[l] % 3+3*rng.randrange(3) for l in range(n))
        labels.append(tuple(inverse_frequency_coordinates(u,v,4) for u,v in zip(a,c)))
        labels.extend(tuple((rng.randrange(9),rng.randrange(9)) for _ in range(n)) for _ in range(W-1))
    source=native_source(labels,4)
    acquisition=PacketAcquisition.from_source(source,K,tuple(f"native-program-{n}-{seed}-{i}" for i in range(K*W)),K*W)
    branch=acquisition.branch((0,)*len(acquisition.pointers))
    physical=tuple(tuple(x[j] for x in grid) for j in range(3))
    frame=tuple(tuple(v[i] for i in branch.packet.free) for v in physical)
    family,record=native_quadratic_program(branch,frame,(0,)*(branch.packet.retained-3))
    v,search=isotropic_direction(family)
    record.update({"engineered_low_source_seed":seed,"source_is_IID_population_control":False,
                   "receiver":family.receiver(v),"isotropic_search":search,
                   "whole_original_or_parent_packet_word_cube_enumerated":False})
    return family,record


def teleport_tensor(family,secret,data):
    """Basis copy, actual SUM permutation and FFT implement the full Bell instrument."""
    d,D=family.width,3**family.width
    if d>3: raise ValueError("complete tensor replay limited to three program coordinates")
    secret=word(secret,family.components);data=np.asarray(data,dtype=complex)
    if data.ndim==1:data=data[None,:]
    if data.ndim!=2 or data.shape[1]!=D or abs(float(np.sum(abs(data)**2))-1)>1e-12:
        raise ValueError("normalized data/reference amplitudes required")
    ws=tuple(product(range(3),repeat=d));index={w:i for i,w in enumerate(ws)}
    phases=np.array([np.exp(2j*math.pi*(sum(a*b for a,b in zip(secret,family.value(z))) % 3)/3) for z in ws])
    # The supplied flat program is basis-copied into a known zero register.
    state=np.zeros((data.shape[0],D,D,D),complex)
    for x,z in enumerate(ws):
        for t,w in enumerate(ws):
            a=index[tuple((u-v) % 3 for u,v in zip(w,z))]
            state[:,x,a,t]=data[:,x]*phases[t]/math.sqrt(D)
    state=state.reshape((data.shape[0],)+(3,)*d+(D,D))
    state=np.fft.fftn(state,axes=tuple(range(1,d+1)))/math.sqrt(D)
    return state.reshape(data.shape[0],D,D,D),phases


def physical_receiver(family,secret,v):
    contract=family.receiver(v);d,D=family.width,3**family.width
    if d>3:raise ValueError("complete receiver replay limited to three program coordinates")
    ws=tuple(product(range(3),repeat=d));index={w:i for i,w in enumerate(ws)}
    line=[tuple(j*x % 3 for x in v) for j in range(3)]
    data=np.zeros(D,complex)
    for point in line:data[index[point]]=1/math.sqrt(3)
    actual,phases=teleport_tensor(family,secret,data);records=[];maximum=0.;total=0.;labels=Counter()
    # Also certify arbitrary data entangled with a reference, not only the line.
    rng=np.random.default_rng(88690+family.components)
    arbitrary=rng.normal(size=(2,D))+1j*rng.normal(size=(2,D));arbitrary/=np.linalg.norm(arbitrary)
    replay,phase2=teleport_tensor(family,secret,arbitrary)
    for bi,b in enumerate(ws):
        for ai,a in enumerate(ws):
            branch=actual[0,bi,ai];probability=float(np.sum(abs(branch)**2));total+=probability
            if abs(probability-1/D**2)>3e-12:raise ArithmeticError("Bell outcome is not uniformly charged")
            for ti,t in enumerate(ws):
                x=tuple((u-v) % 3 for u,v in zip(t,a));xi=index[x]
                expected=arbitrary[:,xi]*phase2[ti]*np.exp(-2j*math.pi*(sum(u*v for u,v in zip(b,x)) % 3)/3)/D
                maximum=max(maximum,float(np.max(abs(replay[:,bi,ai,ti]-expected))))
            label=tuple((offset+sum(row[i]*a[i] for i in range(d))) % 3 for row,offset in zip(contract["gradient_rows"],contract["label_offset"]))
            correction=sum(x*y for x,y in zip(b,v)) % 3
            clean=np.array([branch[index[tuple((x+j*y) % 3 for x,y in zip(a,v))]]*np.exp(2j*math.pi*j*correction/3) for j in range(3)])*D
            probabilities=abs(np.fft.fft(clean)/math.sqrt(3))**2
            answer=sum(s*l for s,l in zip(secret,label)) % 3
            if abs(float(probabilities[answer])-1)>3e-12:raise ArithmeticError("isotropic query did not yield its exact secret equation")
            labels[label]+=1
            records.append({"Bell_shift":a,"Bell_phase":b,"public_equation_label":label,
                            "answer":answer,"raw_Bell_probability":str(Fraction(1,D**2)),
                            "known_phase_correction":correction,"all_Fourier_probabilities":list(map(float,probabilities))})
    if maximum>3e-12 or abs(total-1)>3e-12:raise ArithmeticError("complete Choi/Bell instrument failed")
    if contract["uniform_full_secret_label_law_certified"] and len(labels)!=3**family.components:
        raise ArithmeticError("full gradient rank did not cover every field label")
    return {"calibration_secret":secret,"receiver":contract,"all_Bell_branches":records,
            "total_raw_Bell_probability":total,"arbitrary_entangled_data_maximum_amplitude_error":maximum,
            "reference_dimension":2,"public_label_histogram":[{"label":key,"count":value} for key,value in sorted(labels.items())],
            "one_program_consumed_per_actual_use":True,"virtual_calibration_branches_are_source_copies":False,
            "unknown_gate_inverse_or_Clifford_byproduct_correction_used":False}


def equation_sample_ledger(n,kappa):
    integer(n,"field secret dimension",1);integer(kappa,"extra exact field equations",0)
    m=n+kappa
    return {"dimension":n,"extra_equations":kappa,"independent_supplied_programs_required":m,
            "field_equation_rank_failure_upper":str(Fraction(3**n-1,2*3**m)),
            "conditional_on_each_program_full_gradient_rank_and_fresh_Bell_randomness":True,
            "availability_of_these_programs_proved":False,"original_full_modulus_secret_recovery_proved":False}


def linear_offset_census():
    M=((0,0),(0,0));counts=Counter();direction=None
    for digits in product(range(3),repeat=4):
        family=QuadraticFamily((M,M),(digits[:2],digits[2:]))
        v,policy=isotropic_direction(family)
        if direction is not None and v!=direction:raise ArithmeticError("isotropic policy reads random linear offsets")
        direction=v;counts[family.receiver(v)["label_offset"]]+=1
    if len(counts)!=9 or set(counts.values())!={9}:raise ArithmeticError("uniform independent linear offsets failed the label law")
    return {"components":2,"width":2,"gradient_rank":0,"complete_independent_linear_offsets":81,
            "direction":direction,"direction_selection_reads_linear_coefficients":False,
            "public_label_histogram":[{"label":key,"count":value} for key,value in sorted(counts.items())],
            "uniform_labels_require_full_gradient_rank_for_fixed_program":True,
            "uniform_labels_from_fresh_uniform_offsets_need_full_gradient_rank":False,
            "fresh_uniform_independent_linear_offsets_are_a_source_premise":True,
            "unconditional_native_factory_proved_by_this_census":False}


def run_controls():
    controls=[]
    for n,seed in ((1,88601),(2,88602)):
        family,record=engineered_native_program(n,seed)
        if not record["receiver"]["uniform_full_secret_label_law_certified"]:
            raise ArithmeticError("pinned native control needs a full-rank isotropic query")
        record["physical_receiver"]=physical_receiver(family,tuple(range(1,n+1)),record["receiver"]["direction"])
        record["original_source_program_and_one_Bell_branch_probability"]=str(Fraction(record["raw_program_branch_probability"])*Fraction(1,3**(2*family.width)))
        controls.append(record)
    return {"status":"ONE_USE_QUADRATIC_PROGRAM_SECRET_EQUATION_RECEIVER_NATIVE_FACTORY_OPEN_REVIEW_PENDING",
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),"native_calibration_controls":controls,
            "conditional_sample_ledgers":[equation_sample_ledger(n,8) for n in (1,2,8,32,128)],
            "fresh_linear_offset_law_census":linear_offset_census(),
            "candidate_record_accepted":False,"unconditional_IID_native_program_factory_supplied":False,
            "growing_depth_or_full_secret_quantum_speedup_proved":False,
            "research_decision":"Quadratic program decoding no longer requires identical states. Construct a useful charged IID source transition producing such programs, or extend the isotropic query to growing-depth phases.",
            "routine_wiring_owner":"Gemini or Antigravity"}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args()
    report=run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"report":str(REPORT) if args.write else None,
                      "Bell_branches":sum(len(c["physical_receiver"]["all_Bell_branches"]) for c in report["native_calibration_controls"])},indent=2))


if __name__=="__main__":main()
