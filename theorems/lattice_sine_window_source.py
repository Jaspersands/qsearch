"""Public sine-localized lattice source, exact finite instrument and physical registers.

Compilers and samplers receive no short vector. Private templates are audits,
not trial selectors. No efficient noisy receiver or hard source is supplied.
"""
from __future__ import annotations

import argparse
from collections import Counter,deque
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import gcd,isqrt,prod
from pathlib import Path
import uuid

from flint import fmpz_mat,fmpq_mat
import numpy as np
from qiskit import QuantumCircuit,QuantumRegister,ClassicalRegister,transpile
from qiskit.circuit.library import QFTGate
from qiskit.synthesis.arithmetic.adders import adder_ripple_c04
from qiskit_aer import AerSimulator

if __package__:
    from .lattice_sine_packet import compile_packet,packet_plan,DyadicField,exact_affinity
    from .lattice_qft_precision import CircuitResourcePolicy,QFTPrecisionPlan,QFTUsage,QFTUsageLedger,compile_qft,integer,precision_plan
    from .lattice_cube_coset_source import encode_position,decode_difference
    from .lattice_cube_dcp_readout import (PhaseReceipt,SimulatedPhaseBatch,OpaquePhaseBackend,
        _valid_density,_serialize_density,NUMERICAL_TOLERANCE)
    from .planted_qary_usvp_source import prime_certificate,public_LLL_attack,PublicQaryLattice
else:
    from lattice_sine_packet import compile_packet,packet_plan,DyadicField,exact_affinity
    from lattice_qft_precision import CircuitResourcePolicy,QFTPrecisionPlan,QFTUsage,QFTUsageLedger,compile_qft,integer,precision_plan
    from lattice_cube_coset_source import encode_position,decode_difference
    from lattice_cube_dcp_readout import (PhaseReceipt,SimulatedPhaseBatch,OpaquePhaseBackend,
        _valid_density,_serialize_density,NUMERICAL_TOLERANCE)
    from planted_qary_usvp_source import prime_certificate,public_LLL_attack,PublicQaryLattice
from ternary_measured_lattice_decoder import exact_json

ROOT=Path(__file__).resolve().parents[1]
DERIVATION=ROOT/"research/LATTICE_SINE_WINDOW_SOURCE.md"
CONTRACT=ROOT/"research/hypotheses/lattice_sine_window_source_contract.json"
REPORT=ROOT/"research/phase_workbench/lattice_sine_window_source.json"


def signed(x,name):
    if type(x) is not int:raise ValueError("exact "+name+" required")
    return x


def fingerprint(record):
    return hashlib.sha256(json.dumps(exact_json(record),sort_keys=True,separators=(",",":")).encode()).hexdigest()


@dataclass(frozen=True)
class SineWindowSource:
    basis: tuple
    prime: int
    residue: int
    coordinate: int
    box: int
    packet_side: int

    def __post_init__(self):
        B=tuple(tuple(row) for row in self.basis);n=len(B)
        if not n or any(len(row)!=n for row in B):raise ValueError("square nonempty public basis required")
        for row in B:
            for x in row:signed(x,"basis entry")
        if not fmpz_mat(B).det():raise ValueError("full rank public integer lattice required")
        integer(self.prime,"odd splitting prime",3);prime_certificate(self.prime)
        integer(self.residue,"nonzero public residue",1);integer(self.coordinate,"public coordinate")
        if self.residue>=self.prime or self.coordinate>=n:raise ValueError("coordinate/residue out of range")
        for value in (self.box,self.packet_side):
            integer(value,"dyadic side",2)
            if value&(value-1):raise ValueError("power-of-two sides required")
        object.__setattr__(self,"basis",B)

    @property
    def dimension(self):return len(self.basis)
    @property
    def input_population(self):return 2*self.box**self.dimension
    @property
    def phase_modulus(self):return (2*self.box)**self.dimension
    @property
    def packet_bits(self):return self.packet_side.bit_length()-1

    def point(self,b,a):
        integer(b,"colour bit");a=tuple(a)
        if b>1 or len(a)!=self.dimension or any(type(x) is not int or not 0<=x<self.box for x in a):
            raise ValueError("canonical colour and parent position required")
        c=list(a);c[self.coordinate]=self.prime*c[self.coordinate]+b*self.residue
        return tuple(sum(t*row[j] for t,row in zip(c,self.basis)) for j in range(self.dimension))

    def public_access(self):
        return {"source_type":"PUBLIC_SINE_WINDOW_LATTICE_INSTRUMENT","basis_rows":self.basis,
            "prime":self.prime,"split_prime_certificate":prime_certificate(self.prime).record(),
            "residue":self.residue,"coordinate":self.coordinate,"box":self.box,
            "packet_side":self.packet_side,"input_population":self.input_population,
            "phase_modulus":self.phase_modulus,"hidden_short_vector_or_shift_given":False,
            "receiver_gets_localization_register":False,"uniform_secret_prior_inferred":False}

    def arithmetic_plan(self):
        maxima=[self.box-1]*self.dimension
        maxima[self.coordinate]=self.prime*(self.box-1)+self.residue
        bounds=tuple(sum(abs(row[j])*t for t,row in zip(maxima,self.basis)) for j in range(self.dimension))
        W=max((t+self.packet_side-1).bit_length()+1 for t in bounds)
        return {"point_absolute_bounds":bounds,"localization_absolute_bounds":tuple(t+self.packet_side-1 for t in bounds),
            "shared_signed_word_bits":W,"localization_coordinates_share_word_width":True,
            "all_signed_localization_values_in_range":all(t+self.packet_side-1<2**(W-1) for t in bounds),
            "copied_point_or_original_noise_garbage_retained":False}


def ceil_sqrt_fraction(x):
    x=Fraction(x)
    r=isqrt(x.numerator//x.denominator)
    return r+int(r*r*x.denominator<x.numerator)


def promise_budget(source,norm_squared_lower,norm_squared_upper,unique_gap):
    """Conditional public PROMISE ledger; never certifies its assumptions from B."""
    for x,name in ((norm_squared_lower,"lower norm square"),(norm_squared_upper,"upper norm square"),(unique_gap,"unique gap")):
        integer(x,name,1)
    if norm_squared_lower>norm_squared_upper:raise ValueError("ordered public norm interval required")
    inverse=fmpq_mat(source.basis).inv();bounds=[]
    for j in range(source.dimension):
        squared=sum((Fraction(int(inverse[i,j].numerator),int(inverse[i,j].denominator))**2
                     for i in range(source.dimension)),Fraction(0))
        bounds.append(ceil_sqrt_fraction(norm_squared_upper*squared))
    shifts=list(bounds);shifts[source.coordinate]=(bounds[source.coordinate]+source.residue)//source.prime
    packet_loss=Fraction(242*norm_squared_upper,49*source.packet_side**2)
    boundary=Fraction(sum(shifts),source.box)
    return {"norm_squared_lower":norm_squared_lower,"norm_squared_upper":norm_squared_upper,"promised_unique_gap":unique_gap,
        "nonparallel_aliases_excluded_IF_promises_hold":unique_gap**2*norm_squared_lower>=source.dimension*source.packet_side**2,
        "parallel_cross_colour_aliases_excluded_IF_promises_hold":(source.prime-1)**2*norm_squared_lower>source.dimension*source.packet_side**2,
        "public_basis_coefficient_bounds":tuple(bounds),"public_parent_shift_bounds":tuple(shifts),
        "packet_visibility_loss_upper":str(min(Fraction(1),packet_loss)),
        "box_boundary_loss_upper":str(min(Fraction(1),boundary)),
        "bad_rate_upper_IF_correct_trial_and_promises_hold":str(min(Fraction(1),packet_loss+boundary)),
        "short_vector_norm_gap_and_correct_trial_are_unverified_assumptions":True,
        "outer_length_coordinate_residue_trials_are_not_free":True,
        "efficient_robust_receiver_supplied":False}


def resource_estimate(source):
    if not isinstance(source,SineWindowSource):raise ValueError("typed public sine source required")
    plan=source.arithmetic_plan();W=plan["shared_signed_word_bits"];n=source.dimension;m=source.box.bit_length()-1
    additions=flips=0
    for i in range(n):
        values=[((source.prime if j==source.coordinate else 1)*row[i])*(1<<h) for j,row in enumerate(source.basis) for h in range(m)]
        values.append(source.residue*source.basis[source.coordinate][i])
        for value in values:
            value%=1<<W
            if value:additions+=1;flips+=value.bit_count()
    packet=packet_plan(source.packet_bits);ell=n*(m+1)
    return {"arithmetic_width_plan":plan,"input_qubits":1+n*m,"localization_output_qubits":n*W,
        "shared_point_arithmetic_work_qubits":2*W+1,"shared_packet_work_qubits":source.packet_bits,
        "zero_padding_qubits":n,"position_QFT_qubits":ell,
        "total_source_qubits":1+n*m+n*W+2*W+1+source.packet_bits+n,
        "constant_additions_including_uncompute":2*additions,"point_to_localization_additions":n,
        "arithmetic_logical_instructions":4*flips+2*additions+n,
        "packet_unitary_applications":n,"packet_plan":packet,
        "coherent_source_instructions_before_QFT":1+n*m+2*n+4*flips+2*additions,
        "no_preimages_or_private_shift_needed":True}


@dataclass
class CompiledSinePosition:
    source: SineWindowSource
    evaluator: QuantumCircuit
    input_register: QuantumRegister
    outputs: tuple
    arithmetic_work: tuple
    packet_work: QuantumRegister
    padding: QuantumRegister
    position_wires: tuple
    coherent_parent: QuantumCircuit
    resources: dict


@dataclass
class CompiledSineSource(CompiledSinePosition):
    qft_plan: object
    qft_ledger: object

    def readout_circuit(self,diagnostic=True):
        bits=ClassicalRegister(len(self.position_wires),"label")
        qc=QuantumCircuit(*self.coherent_parent.qregs,bits);qc.compose(self.coherent_parent,inplace=True)
        qc.measure(list(self.position_wires),bits)
        if diagnostic:
            with qc.if_test((bits,0)):qc.z(self.input_register[0])
            qc.save_density_matrix([self.input_register[0]],label="colour",conditional=True,pershot=True)
            with qc.if_test((bits,0)):qc.z(self.input_register[0])
        return qc

    def resource_record(self):
        packet=self.resources["packet_plan"];err=Fraction(packet["encoded_rotation_operator_error_upper"])
        plan=precision_plan(len(self.position_wires),cutoff=len(self.position_wires)-1) if self.qft_plan is None else self.qft_plan
        return {"public_source":self.source.public_access(),"closed_resources":self.resources,
            "compiled_qubits":self.coherent_parent.num_qubits,"compiled_parent_instructions":len(self.coherent_parent.data),
            "encoded_packet_parameter_operator_upper_per_parent":str(min(Fraction(2),self.source.dimension*err)),
            "QFT_precision_plan":None if self.qft_plan is None else self.qft_plan.record(),
            "QFT_angle_accounting_plan":plan.record(),
            "packet_and_retained_QFT_parameter_operator_upper_per_parent":str(min(Fraction(2),self.source.dimension*err+plan.encoded_angle_upper)),
            "packet_and_QFT_operator_upper_relative_to_ideal_full_QFT":str(min(Fraction(2),self.source.dimension*err+plan.encoded_qft_operator_upper)),
            "original_position_wires_reused_in_place":True,"localization_register_is_traced_not_replaced_by_a_preimage":True,
            "arithmetic_and_packet_workspace_return_zero":True,"mixed_colour_inverse_available":False,
            "full_parent_inverse_requires_localization_and_label_registers":True,
            "normalized_conditional_colour_error_not_inferred_without_label_mass":True,
            "hardware_arithmetic_synthesis_or_roundoff_certified":False}


def compile_position_parent(source,policy=None):
    """Public position/localization parent BEFORE choosing a Fourier group."""
    policy=CircuitResourcePolicy() if policy is None else policy
    if not isinstance(policy,CircuitResourcePolicy):raise ValueError("typed circuit policy required")
    E=resource_estimate(source);W=E["arithmetic_width_plan"]["shared_signed_word_bits"];ell=E["position_QFT_qubits"]
    policy.check(qubits=E["total_source_qubits"],adder_bits=W,constant_additions=E["constant_additions_including_uncompute"]+source.dimension)
    packet=compile_packet(source.packet_bits,policy)
    inputs=QuantumRegister(E["input_qubits"],"input")
    outputs=tuple(QuantumRegister(W,f"y_{i}") for i in range(source.dimension))
    constant,point,carry=QuantumRegister(W,"constant"),QuantumRegister(W,"point"),QuantumRegister(1,"carry")
    evaluator=QuantumCircuit(inputs,*outputs,constant,point,carry)
    adder=adder_ripple_c04(W,kind="fixed").to_gate();controlled=adder.control(1);m=source.box.bit_length()-1
    for i in range(source.dimension):
        compute=QuantumCircuit(*evaluator.qregs)
        values=[((source.prime if j==source.coordinate else 1)*row[i]*(1<<h),inputs[1+j*m+h])
                for j,row in enumerate(source.basis) for h in range(m)]
        values.append((source.residue*source.basis[source.coordinate][i],inputs[0]))
        for value,control in values:
            value%=1<<W
            if not value:continue
            ones=[constant[j] for j in range(W) if (value>>j)&1]
            for q in ones:compute.x(q)
            compute.append(controlled,[control,*constant,*point,*carry])
            for q in ones:compute.x(q)
        evaluator.compose(compute,inplace=True)
        evaluator.append(adder,[*point,*outputs[i],*carry])
        evaluator.compose(compute.inverse(),inplace=True)
    if len(evaluator.data)!=E["arithmetic_logical_instructions"]:raise ArithmeticError("arithmetic count mismatch")
    packet_work=QuantumRegister(source.packet_bits,"packet_work");padding=QuantumRegister(source.dimension,"position_padding")
    parent=QuantumCircuit(*evaluator.qregs,packet_work,padding);parent.h(inputs)
    for register in outputs:
        parent.append(packet.circuit.to_gate(),[*register[:source.packet_bits],*packet_work])
    parent.compose(evaluator,inplace=True)
    wires=tuple(q for j in range(source.dimension) for q in (*inputs[1+j*m:1+(j+1)*m],padding[j]))
    if parent.num_qubits!=E["total_source_qubits"]:raise ArithmeticError("source qubit count mismatch")
    if len(parent.data)!=E["coherent_source_instructions_before_QFT"]:raise ArithmeticError("position parent instruction count mismatch")
    return CompiledSinePosition(source,evaluator,inputs,outputs,(constant,point,carry),packet_work,padding,wires,parent,E)


def compile_source(source,qft_plan=None,policy=None):
    """Cyclic-group source; product-group readout is a separate instrument."""
    policy=CircuitResourcePolicy() if policy is None else policy
    ell=resource_estimate(source)["position_QFT_qubits"]
    if qft_plan is not None and (not isinstance(qft_plan,QFTPrecisionPlan) or qft_plan.wires!=ell):
        raise ValueError("QFT plan must match complete cyclic position register")
    if qft_plan is None and ell-1>1022:raise ValueError("UNKNOWN_NUMERIC_QFT_RANGE; provide a budgeted approximation")
    position=compile_position_parent(source,policy)
    parent=position.coherent_parent
    qft=QFTGate(ell) if qft_plan is None else compile_qft(qft_plan,policy).to_gate()
    parent.append(qft,list(position.position_wires))
    policy.check(qubits=parent.num_qubits,QFT_instructions=ell+ell//2+(ell*(ell-1)//2 if qft_plan is None else qft_plan.controlled_phases))
    E=position.resources
    if len(parent.data)!=E["coherent_source_instructions_before_QFT"]+1:raise ArithmeticError("parent instruction count mismatch")
    return CompiledSineSource(**vars(position),qft_plan=qft_plan,
                             qft_ledger=None if qft_plan is None else QFTUsageLedger(qft_plan))


def exact_reference(source,work_cap=2000000,qft_cutoff=None):
    """Complete bounded Born instrument, including non-character cutoff QFTs."""
    integer(work_cap,"positive reference work cap",1)
    D,N=source.input_population,source.phase_modulus;root=max(2*source.packet_side,N)
    ell=N.bit_length()-1
    cutoff=ell-1 if qft_cutoff is None else integer(qft_cutoff,"QFT cutoff")
    if cutoff>=ell:raise ValueError("cutoff below position width required")
    if root>128 or D*D*N*source.dimension>work_cap:raise ValueError("UNKNOWN_COMPLETE_SINE_REFERENCE_CAP")
    F=DyadicField(root);parents=tuple((b,a) for b in (0,1) for a in product(range(source.box),repeat=source.dimension))
    points=tuple(source.point(b,a) for b,a in parents);cache={};gram=[]
    for x in points:
        row=[]
        for y in points:
            value=F.scalar(Fraction(1,D))
            for t in (a-b for a,b in zip(x,y)):
                if t not in cache:cache[t]=exact_affinity(source.packet_side,t,F)
                value=F.multiply(value,cache[t])
                if not any(value):break
            row.append(value)
        gram.append(row)
    outcomes=[];sum_prob=F.zero()
    def phase_power(k,x):
        return (root//N)*sum(((k>>m)&1)*((x>>j)&1)*(1<<(m+j))
            for m in range(ell) for j in range(ell) if ell-1-cutoff<=m+j<=ell-1)
    for k in range(N):
        matrix=[[F.zero(),F.zero()],[F.zero(),F.zero()]]
        for i,(b,a) in enumerate(parents):
            for j,(c,z) in enumerate(parents):
                if any(gram[i][j]):
                    power=phase_power(k,encode_position(a,source.box))-phase_power(k,encode_position(z,source.box))
                    term=F.scale(F.multiply(gram[i][j],F.monomial(power)),Fraction(1,N))
                    matrix[b][c]=F.add(matrix[b][c],term)
        p=F.add(matrix[0][0],matrix[1][1]);sum_prob=F.add(sum_prob,p)
        outcomes.append({"label":k,"joint_label_probability":F.encode(p),
            "unnormalized_colour_density":tuple(tuple(F.encode(x) for x in row) for row in matrix)})
    if sum_prob!=F.scalar(1):raise ArithmeticError("complete instrument failed normalization")
    return {"public_source":source.public_access(),"reference_root":root,"complete_parent_count":D,
        "QFT_cutoff":cutoff,"QFT_is_exact":cutoff==ell-1,
        "parents":parents,"public_points":points,"complete_public_Gram":tuple(tuple(F.encode(x) for x in row) for row in gram),
        "all_label_outcomes":tuple(outcomes),"label_distribution_uniform":all(r["joint_label_probability"]==(str(Fraction(1,N)),) for r in outcomes),
        "dense_reference_is_not_a_polynomial_preimage_or_receiver_oracle":True}


def _decode(poly,F):
    coefficients=tuple(Fraction(x) for x in reversed(poly))
    return coefficients+(Fraction(0),)*(F.degree-len(coefficients))


def audit_template(source,reference,private_vector):
    """Private forward check AFTER source construction; never admission/solver advice."""
    if reference["QFT_is_exact"] is not True:
        return {"status":"APPROXIMATE_QFT_NOT_AN_EXACT_DCP_TEMPLATE","finite_marginal_template_matches":False,
            "correct_trial_flag_given_to_receiver":False,"full_growing_reduction_certified":False}
    vector=tuple(private_vector)
    if len(vector)!=source.dimension or any(type(x) is not int for x in vector) or gcd(*vector)!=1:
        raise ValueError("primitive private audit vector required")
    d=fmpq_mat([vector])*fmpq_mat(source.basis).inv();coords=[]
    for x in d.tolist()[0]:
        if x.denominator!=1:raise ValueError("private audit vector not in lattice")
        coords.append(int(x))
    if coords[source.coordinate]%source.prime!=source.residue:
        return {"status":"WRONG_TRIAL_NOT_A_PROMISED_SOURCE","finite_marginal_template_matches":False,
            "correct_trial_flag_given_to_receiver":False,"full_growing_reduction_certified":False}
    h=tuple((x-source.residue)//source.prime if i==source.coordinate else x for i,x in enumerate(coords))
    F=DyadicField(reference["reference_root"]);N=source.phase_modulus;v=F.scalar(1)
    for x in vector:v=F.multiply(v,exact_affinity(source.packet_side,x,F))
    overlap=prod(Fraction(max(0,source.box-abs(x)),source.box) for x in h);v=F.scale(v,overlap)
    matches=True
    for outcome in reference["all_label_outcomes"]:
        k=outcome["label"];phase=F.monomial(-(F.root//N)*k*encode_position(h,source.box))
        off=F.scale(F.multiply(v,phase),Fraction(1,2*N))
        expected=((F.scalar(Fraction(1,2*N)),off),(F.conjugate(off),F.scalar(Fraction(1,2*N))))
        matches &= outcome["unnormalized_colour_density"]==tuple(tuple(F.encode(x) for x in row) for row in expected)
    return {"status":"FINITE_PRIVATE_TEMPLATE_MATCH" if matches else "ALIASES_OR_MODEL_MISMATCH",
        "PRIVATE_AUDIT_ONLY_vector":vector,"PRIVATE_AUDIT_ONLY_basis_coefficients":tuple(coords),
        "PRIVATE_AUDIT_ONLY_parent_shift":h,"PRIVATE_AUDIT_ONLY_cyclic_shift":encode_position(h,source.box)%N,
        "exact_marginal_visibility":F.encode(v),"box_overlap":str(overlap),
        "finite_marginal_template_matches":bool(matches),"correct_trial_flag_given_to_receiver":False,
        "conservative_private_bad_rate_upper":str(min(Fraction(1),Fraction(242*sum(x*x for x in vector),49*source.packet_side**2)+Fraction(sum(abs(x) for x in h),source.box))),
        "full_growing_reduction_certified":False}


@dataclass
class SinePhaseBatch(SimulatedPhaseBatch):
    source_public: object=None


def simulate_batch(compiled,shots=8,seed=0,batch_tag=None):
    if not isinstance(compiled,CompiledSineSource):
        raise ValueError("cyclic sine compiler required; product-group output is a different source")
    integer(shots,"positive shots",1)
    if shots>64 or compiled.coherent_parent.num_qubits>48:raise ValueError("UNKNOWN_SINE_SIMULATOR_CAP")
    if compiled.qft_ledger is not None:compiled.qft_ledger.charge("forward",shots)
    qc=compiled.readout_circuit()
    backend=AerSimulator(method="matrix_product_state",matrix_product_state_truncation_threshold=0.0,
        max_parallel_threads=1,shot_branching_enable=False)
    qc=transpile(qc,backend,optimization_level=0,seed_transpiler=seed)
    result=backend.run(qc,shots=shots,memory=True,seed_simulator=seed).result()
    if not result.success:raise RuntimeError("sine source simulation failed")
    metadata=result.results[0].metadata;memory=[int(x.replace(" ",""),2) for x in result.get_memory()]
    counts=Counter(memory);snapshots={int(k,16):deque(v) for k,v in result.data()["colour"].items()}
    if metadata.get("measure_sampling") or set(snapshots)!=set(counts) or any(len(snapshots[k])!=v for k,v in counts.items()):
        raise ValueError("UNCONDITIONED_OR_INCOMPLETE_SINE_SNAPSHOTS")
    tag=batch_tag or uuid.uuid4().hex;receipts=[];densities={};Z=np.diag([1,-1])
    for i,k in enumerate(memory):
        rho=np.asarray(snapshots[k].popleft().data,complex)
        if k==0:rho=Z@rho@Z
        r=PhaseReceipt(f"{tag}:{i}",compiled.source.phase_modulus,k,(),(f"{tag}:{i}",))
        receipts.append(r);densities[r.id]=_valid_density(rho)
    public=compiled.source.public_access()
    return SinePhaseBatch(tuple(receipts),densities,{"actual_compiled_source_preparations_charged":shots,
        "QFT_cutoff":len(compiled.position_wires)-1 if compiled.qft_plan is None else compiled.qft_plan.cutoff,
        "logical_readout_QFT_is_exact_reference":compiled.qft_plan is None or compiled.qft_plan.exact,
        "QFT_usage_ledger":None if compiled.qft_ledger is None else compiled.qft_ledger.record(),
        "packet_unitaries_charged":shots*compiled.source.dimension,"W_calls_charged":3*shots*compiled.source.dimension,
        "source_shots_independent_given_public_parameters":True,"public_source_fingerprint":fingerprint(public),
        "localization_register_was_unmeasured_and_traced":True,"source_DCP_promise_is_not_inferred_from_samples":True,
        "numerical_error_is_a_formally_certified_channel_bound":False,"MPS_truncation_threshold":0.0,
        "conditioned_snapshot_keys_and_multiplicities_checked":True},source_public=public)


class SinePhysicalBackend(OpaquePhaseBackend):
    """Physical destructive operations, with NO DCP-promise/trial selector."""
    def __init__(self,batch,seed=0):
        if not isinstance(batch,SinePhaseBatch) or batch._claimed:raise ValueError("fresh sine batch required; no reset/copy")
        meta=batch.metadata
        if meta.get("source_shots_independent_given_public_parameters") is not True:raise ValueError("explicit source product law required")
        if meta.get("public_source_fingerprint")!=fingerprint(batch.source_public):raise ValueError("source binding mismatch")
        if meta.get("actual_compiled_source_preparations_charged")!=len(batch.receipts):raise ValueError("all preparations must be paid")
        if any(r.modulus!=batch.source_public["phase_modulus"] or r.ancestors!=(r.id,) or r.merge_depth for r in batch.receipts):
            raise ValueError("bound original receipts required")
        if any(type(r.label) is not int or not 0<=r.label<r.modulus or r.measured_cells for r in batch.receipts):
            raise ValueError("canonical labels only; localization must not be disclosed")
        if set(batch._densities)!={r.id for r in batch.receipts} or len({r.id for r in batch.receipts})!=len(batch.receipts):
            raise ValueError("one physical density per distinct receipt required")
        self._states={k:_valid_density(v) for k,v in batch._densities.items()}
        self._receipts={r.id:r for r in batch.receipts};self._active=set(self._receipts)
        self._rng=np.random.default_rng(seed);self._serial=0;batch._claimed=True
        self.source_preparations_charged=meta["actual_compiled_source_preparations_charged"]


def audit_batch(source,reference,batch):
    expected=fingerprint(source.public_access())
    if fingerprint(reference["public_source"])!=expected or batch.metadata.get("public_source_fingerprint")!=expected:
        raise ValueError("public source/reference/batch binding mismatch")
    if reference["QFT_cutoff"]!=batch.metadata.get("QFT_cutoff"):
        raise ValueError("matching QFT instrument reference required")
    F=DyadicField(reference["reference_root"]);errors=[]
    for receipt in batch.receipts:
        row=reference["all_label_outcomes"][receipt.label]
        mass=F.value(_decode(row["joint_label_probability"],F)).real
        if mass<=NUMERICAL_TOLERANCE:raise ValueError("UNKNOWN_RARE_SINE_REFERENCE_BRANCH")
        rho=np.array([[F.value(_decode(x,F)) for x in r] for r in row["unnormalized_colour_density"]])/mass
        errors.append(float(np.max(np.abs(rho-batch._densities[receipt.id]))))
    if max(errors,default=0)>NUMERICAL_TOLERANCE:raise ValueError("COMPILED_SINE_SOURCE_DISAGREES_WITH_REFERENCE")
    return {"all_emitted_conditional_densities_agree":True,"private_max_numerical_error":max(errors,default=0),
        "metadata":batch.metadata,"public_receipts":batch.public_receipts(),
        "PRIVATE_AUDIT_ONLY_density_matrices":{k:_serialize_density(v) for k,v in batch._densities.items()},
        "speedup_or_hardware_channel_certificate":False}


def build_report():
    sources=(SineWindowSource(((1,),),7,1,0,2,4),SineWindowSource(((-1,),),7,1,0,2,4),
        SineWindowSource(((17,0),(16,1)),7,1,0,2,4),SineWindowSource(((1,),),3,1,0,2,4))
    vectors=((1,),(-1,),(1,-1),(1,));controls=[]
    for i,(source,vector) in enumerate(zip(sources,vectors)):
        compiled=compile_source(source);reference=exact_reference(source)
        batch=simulate_batch(compiled,8,101100+i,f"sine-control-{i}")
        controls.append({"compiled_resources":compiled.resource_record(),"exact_reference":reference,
            "private_template_audit":audit_template(source,reference,vector),"actual_sampling_audit":audit_batch(source,reference,batch)})
    large=compile_source(SineWindowSource(((10000,1000),(9999,1000)),389,1,0,256,128))
    approximate=compile_source(sources[2],precision_plan(4,QFTUsage(direct_forward_calls=2),cutoff=0))
    approx_reference=exact_reference(sources[2],qft_cutoff=0)
    approx_batch=simulate_batch(approximate,2,101104,"sine-cutoff-control")
    deps=("lattice_sine_packet.py","lattice_qft_precision.py","lattice_cube_dcp_readout.py","lattice_cube_coset_source.py",
        "planted_qary_usvp_source.py","ternary_measured_lattice_decoder.py")
    return {"status":"PUBLIC_COHERENT_SINE_WINDOW_SOURCE_AND_UNKNOWN_PHASE_REGISTERS_REVIEW_PENDING",
        "producer_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256":hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256":{x:hashlib.sha256((ROOT/"theorems"/x).read_bytes()).hexdigest() for x in deps},
        "actual_source_controls":tuple(controls),"large_compiled_not_simulated":large.resource_record(),
        "public_conditional_promise_budget":promise_budget(large.source,1,1,512),
        "approximate_instrument_control":{"compiled_resources":approximate.resource_record(),
            "exact_reference":approx_reference,"actual_sampling_audit":audit_batch(sources[2],approx_reference,approx_batch),
            "private_template_audit":audit_template(sources[2],approx_reference,vectors[2])},
        "charged_source_preparations":34,"accepted_speedup_candidate":False,
        "hard_lattice_source_or_efficient_receiver_supplied":False,"new_active_negative_result_created":False,"novelty_claim":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true")
    args=parser.parse_args();report=build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(exact_json(report),indent=2)+"\n")
    print(report["status"]);print("Actual preparations:",report["charged_source_preparations"])
    print("No hard source, new speedup, efficient decoder or hardware certificate.")


if __name__=="__main__":main()
