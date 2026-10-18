"""Product-group Fourier readout of the public sine-localized lattice parent.

This is NOT a tensor replacement for the cyclic DCP oracle. Vector labels,
decoder obligations and the exact instrument are separately typed and tested.
"""
from __future__ import annotations

import argparse
from collections import Counter,deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from math import gcd,prod
from pathlib import Path
import sys
import uuid

import numpy as np
from flint import fmpq_mat
from qiskit import QuantumCircuit,ClassicalRegister,transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from theorems.lattice_sine_window_source import (
    CompiledSinePosition,SineWindowSource,compile_position_parent,exact_reference,
    _decode,fingerprint,exact_json,
)
from theorems.lattice_sine_packet import DyadicField,exact_affinity
from theorems.lattice_qft_precision import CircuitResourcePolicy,integer,precision_plan
from theorems.lattice_cube_dcp_readout import (
    SimulatedPhaseBatch,OpaquePhaseBackend,_valid_density,_serialize_density,NUMERICAL_TOLERANCE,
)

REPORT=ROOT/"research/phase_workbench/lattice_product_phase_source.json"
CONTRACT=ROOT/"research/hypotheses/lattice_product_phase_source_contract.json"
CONTRACT_ID="public_lattice_product_group_phase_source_review_pending_v1"
GROUP="PRODUCT_OF_CYCLIC_TWO_POWER_GROUPS"


def public_source(source):
    record=dict(source.public_access())
    record.pop("phase_modulus")
    record.update({"source_type":"PUBLIC_SINE_WINDOW_PRODUCT_GROUP_INSTRUMENT",
                   "phase_group":GROUP,"rank":source.dimension,"coordinate_modulus":2*source.box,
                   "total_label_bits":source.dimension*source.box.bit_length(),
                   "scalar_cyclic_DCP_contract_granted":False})
    return record


@dataclass
class CompiledProductSource(CompiledSinePosition):
    def readout_circuit(self,diagnostic=True):
        bits=ClassicalRegister(len(self.position_wires),"vector_label")
        qc=QuantumCircuit(*self.coherent_parent.qregs,bits)
        qc.compose(self.coherent_parent,inplace=True)
        qc.measure(list(self.position_wires),bits)
        if diagnostic:
            with qc.if_test((bits,0)):qc.z(self.input_register[0])
            qc.save_density_matrix([self.input_register[0]],label="colour",conditional=True,pershot=True)
            with qc.if_test((bits,0)):qc.z(self.input_register[0])
        return qc

    def resource_record(self):
        n,L=self.source.dimension,self.source.box.bit_length()
        plan=precision_plan(L,cutoff=L-1)
        packet_error=Fraction(self.resources["packet_plan"]["encoded_rotation_operator_error_upper"])
        return {"public_source":public_source(self.source),"position_and_arithmetic_resources":self.resources,
                "compiled_qubits":self.coherent_parent.num_qubits,
                "compiled_parent_instructions":len(self.coherent_parent.data),
                "coordinate_QFT_count_per_parent":n,"coordinate_QFT_wires":L,
                "logical_controlled_phases_per_parent":n*L*(L-1)//2,
                "coordinate_QFT_precision_accounting":plan.record(),
                "encoded_packet_and_QFT_parameter_operator_upper_per_parent":str(min(Fraction(2),n*(packet_error+plan.encoded_qft_operator_upper))),
                "source_position_wires_reused_in_place":True,
                "localization_register_unmeasured_and_traced":True,
                "mixed_colour_inverse_or_correct_trial_flag_available":False,
                "hardware_roundoff_and_full_finite_gate_synthesis_certified":False}


def compile_product_source(source,policy=None):
    if not isinstance(source,SineWindowSource):
        raise ValueError("typed public sine source required")
    policy=CircuitResourcePolicy() if policy is None else policy
    L=source.box.bit_length()
    if L-1>1022:
        raise ValueError("UNKNOWN_LOCAL_QFT_NUMERIC_RANGE; approximation needs a separate instrument")
    position=compile_position_parent(source,policy)
    for j in range(source.dimension):
        position.coherent_parent.append(QFTGate(L),list(position.position_wires[j*L:(j+1)*L]))
    policy.check(qubits=position.coherent_parent.num_qubits,
                 QFT_instructions=source.dimension*(L+L//2+L*(L-1)//2))
    if len(position.coherent_parent.data)!=position.resources["coherent_source_instructions_before_QFT"]+source.dimension:
        raise ArithmeticError("product source omitted or duplicated a Fourier transform")
    return CompiledProductSource(**vars(position))


def exact_product_reference(source,work_cap=2000000):
    # Reuse the PUBLIC Gram, paying the existing bounded reference construction.
    # Its cyclic label outcomes are not used as product-group data.
    base=exact_reference(source,work_cap)
    F=DyadicField(base["reference_root"])
    parents=base["parents"]
    gram=[[_decode(poly,F) for poly in row] for row in base["complete_public_Gram"]]
    q,n=2*source.box,source.dimension
    outcomes=[]
    total=F.zero()
    for k in product(range(q),repeat=n):
        rho=[[F.zero(),F.zero()],[F.zero(),F.zero()]]
        for i,(b,a) in enumerate(parents):
            for j,(c,z) in enumerate(parents):
                if any(gram[i][j]):
                    exponent=(F.root//q)*sum(label*(x-y) for label,x,y in zip(k,a,z))
                    term=F.scale(F.multiply(gram[i][j],F.monomial(exponent)),Fraction(1,q**n))
                    rho[b][c]=F.add(rho[b][c],term)
        mass=F.add(rho[0][0],rho[1][1])
        total=F.add(total,mass)
        outcomes.append({"label":k,"joint_label_probability":F.encode(mass),
                         "unnormalized_colour_density":tuple(tuple(F.encode(x) for x in row) for row in rho)})
    if total!=F.scalar(1):
        raise ArithmeticError("product-group source instrument lost probability")
    return {"public_source":public_source(source),"reference_root":F.root,
            "all_label_outcomes":outcomes,"label_distribution_uniform":all(r["joint_label_probability"]==(str(Fraction(1,q**n)),) for r in outcomes),
            "complete_parent_count":len(parents),"QFT_group":GROUP,
            "bounded_public_Gram_and_all_label_enumeration_are_polynomial_decoder":False}


def audit_product_template(source,reference,private_vector):
    """Post-construction calibration only; NEVER a source/receiver admission flag."""
    if reference["QFT_group"]!=GROUP or fingerprint(reference["public_source"])!=fingerprint(public_source(source)):
        raise ValueError("bound product-group reference required, not a cyclic relabeling")
    u=tuple(private_vector)
    if len(u)!=source.dimension or any(type(x) is not int for x in u) or gcd(*u)!=1:
        raise ValueError("primitive finite calibration vector required")
    raw=(fmpq_mat([u])*fmpq_mat(source.basis).inv()).tolist()[0]
    if any(x.denominator!=1 for x in raw):
        raise ValueError("calibration vector must belong to the public lattice")
    d=tuple(int(x) for x in raw)
    if d[source.coordinate]%source.prime!=source.residue:
        return {"status":"WRONG_TRIAL_NOT_A_PRODUCT_PHASE_PROMISE","finite_template_matches":False,
                "correct_trial_flag_supplied_to_receiver":False}
    h=tuple((x-source.residue)//source.prime if j==source.coordinate else x for j,x in enumerate(d))
    F=DyadicField(reference["reference_root"])
    q,n=2*source.box,source.dimension
    v=F.scalar(1)
    for x in u:v=F.multiply(v,exact_affinity(source.packet_side,x,F))
    overlap=prod(Fraction(max(0,source.box-abs(x)),source.box) for x in h)
    v=F.scale(v,overlap)
    matches=True
    for row in reference["all_label_outcomes"]:
        exponent=-(F.root//q)*sum(a*b for a,b in zip(row["label"],h))
        off=F.scale(F.multiply(v,F.monomial(exponent)),Fraction(1,2*q**n))
        expected=((F.scalar(Fraction(1,2*q**n)),off),(F.conjugate(off),F.scalar(Fraction(1,2*q**n))))
        matches &= row["unnormalized_colour_density"]==tuple(tuple(F.encode(x) for x in r) for r in expected)
    return {"status":"FINITE_PRODUCT_PHASE_TEMPLATE_MATCH" if matches else "ALIASES_OR_MODEL_MISMATCH",
            "finite_template_matches":bool(matches),"PRIVATE_AUDIT_ONLY_parent_shift":h,
            "PRIVATE_AUDIT_ONLY_short_vector":u,"visibility_exact":F.encode(v),
            "box_overlap_exact":str(overlap),"correct_trial_flag_supplied_to_receiver":False,
            "uniform_polynomial_full_vector_decoder_supplied":False}


@dataclass(frozen=True)
class ProductPhaseReceipt:
    id: str
    modulus: int
    label: tuple
    ancestors: tuple
    merge_depth: int=0

    def public_view(self):
        return {"id":self.id,"phase_group":GROUP,"coordinate_modulus":self.modulus,
                "label":self.label,"original_source_receipts":self.ancestors,"merge_depth":self.merge_depth}


@dataclass
class ProductPhaseBatch(SimulatedPhaseBatch):
    source_public: object=None


def simulate_product_batch(compiled,shots=4,seed=0,batch_tag=None):
    if not isinstance(compiled,CompiledProductSource):
        raise ValueError("product-group compiler required; scalar QFT output is not a vector source")
    integer(shots,"complete positive shot count",1)
    if shots>64 or compiled.coherent_parent.num_qubits>48:
        raise ValueError("UNKNOWN_PRODUCT_SOURCE_SIMULATOR_CAP")
    backend=AerSimulator(method="matrix_product_state",matrix_product_state_truncation_threshold=0.0,
                         max_parallel_threads=1,shot_branching_enable=False)
    circuit=transpile(compiled.readout_circuit(),backend,optimization_level=0,seed_transpiler=seed)
    result=backend.run(circuit,shots=shots,memory=True,seed_simulator=seed).result()
    if not result.success:raise RuntimeError("product source simulation failed")
    memory=[int(x.replace(" ",""),2) for x in result.get_memory()]
    counts=Counter(memory)
    snapshots={int(k,16):deque(v) for k,v in result.data()["colour"].items()}
    if (result.results[0].metadata.get("measure_sampling") or set(snapshots)!=set(counts)
            or any(len(snapshots[k])!=count for k,count in counts.items())):
        raise ValueError("UNCONDITIONED_OR_INCOMPLETE_PRODUCT_SNAPSHOTS")
    tag=batch_tag or uuid.uuid4().hex
    q,n=2*compiled.source.box,compiled.source.dimension
    L=q.bit_length()-1
    receipts=[]
    densities={}
    Z=np.diag([1,-1])
    for j,raw in enumerate(memory):
        label=tuple((raw >> (L*i))%(1 << L) for i in range(n))
        rho=np.asarray(snapshots[raw].popleft().data,complex)
        if raw==0:rho=Z@rho@Z
        receipt=ProductPhaseReceipt(f"{tag}:{j}",q,label,(f"{tag}:{j}",))
        receipts.append(receipt)
        densities[receipt.id]=_valid_density(rho)
    public=public_source(compiled.source)
    return ProductPhaseBatch(tuple(receipts),densities,
        {"actual_compiled_source_preparations_charged":shots,"phase_group":GROUP,
         "local_QFT_applications_charged":n*shots,"W_calls_charged":3*n*shots,
         "source_shots_independent_given_public_parameters":True,"public_source_fingerprint":fingerprint(public),
         "localization_register_was_unmeasured_and_traced":True,"conditioned_snapshot_keys_and_counts_checked":True,
         "MPS_truncation_threshold":0.0,"source_promise_not_inferred_from_samples":True,
         "numerical_error_is_a_formally_certified_channel_bound":False},source_public=public)


class ProductPhysicalBackend(OpaquePhaseBackend):
    """Destructive physical operations; no promised-trial or hidden-phase oracle."""
    def __init__(self,batch,seed=0):
        if not isinstance(batch,ProductPhaseBatch) or batch._claimed:
            raise ValueError("fresh PRODUCT source batch required; no scalar cast/reset/copy")
        public=batch.source_public
        meta=batch.metadata
        if (meta.get("phase_group")!=GROUP or public.get("phase_group")!=GROUP
                or meta.get("public_source_fingerprint")!=fingerprint(public)
                or meta.get("source_shots_independent_given_public_parameters") is not True
                or meta.get("localization_register_was_unmeasured_and_traced") is not True
                or meta.get("actual_compiled_source_preparations_charged")!=len(batch.receipts)):
            raise ValueError("bound paid product-source metadata required")
        for r in batch.receipts:
            if (not isinstance(r,ProductPhaseReceipt) or type(r.label) is not tuple
                    or r.modulus!=public["coordinate_modulus"] or len(r.label)!=public["rank"]
                    or any(type(x) is not int or not 0<=x<r.modulus for x in r.label)
                    or r.merge_depth or r.ancestors!=(r.id,)):
                raise ValueError("canonical ORIGINAL vector receipt required")
        if set(batch._densities)!={r.id for r in batch.receipts} or len({r.id for r in batch.receipts})!=len(batch.receipts):
            raise ValueError("one physical density per distinct receipt required")
        self._states={k:_valid_density(v) for k,v in batch._densities.items()}
        self._receipts={r.id:r for r in batch.receipts}
        self._active=set(self._receipts)
        self._rng=np.random.default_rng(seed)
        self._serial=0
        self.known_phase_rotations_charged=0
        self.source_preparations_charged=len(batch.receipts)
        batch._claimed=True

    def apply_known_phase(self,receipt_id,numerator):
        if receipt_id not in self._active:
            raise ValueError("live original unknown register required; no replay")
        parent=self._receipts[receipt_id]
        integer(numerator,"known phase numerator")
        if numerator>=parent.modulus:
            raise ValueError("canonical known phase numerator required")
        U=np.diag([1,np.exp(2j*np.pi*numerator/parent.modulus)])
        self._active.remove(receipt_id)
        self._serial+=1
        self.known_phase_rotations_charged+=1
        child=ProductPhaseReceipt(f"vector-phase:{self._serial}:{receipt_id}",parent.modulus,parent.label,
                                  parent.ancestors,parent.merge_depth)
        self._states[child.id]=_valid_density(U@self._states[receipt_id]@U.conj().T)
        self._receipts[child.id]=child
        self._active.add(child.id)
        return child.public_view()

    def merge(self,left,right):
        if left==right or left not in self._active or right not in self._active:
            raise ValueError("two distinct live registers required; no cloning/retry")
        a,b=self._receipts[left],self._receipts[right]
        if a.modulus!=b.modulus or len(a.label)!=len(b.label) or set(a.ancestors)&set(b.ancestors):
            raise ValueError("same product group and disjoint original ancestry required")
        joint=np.kron(self._states[left],self._states[right])
        joint=joint[np.ix_((0,1,3,2),(0,1,3,2))]
        blocks=[joint[np.ix_((j,2+j),(j,2+j))] for j in (0,1)]
        p0=float(np.trace(blocks[0]).real)
        if not -NUMERICAL_TOLERANCE<=p0<=1+NUMERICAL_TOLERANCE:raise ValueError("UNKNOWN_BRANCH_NUMERICS")
        branch=int(self._rng.random()>=min(1,max(0,p0)))
        p=float(np.trace(blocks[branch]).real)
        self._active.difference_update((left,right))
        if p<NUMERICAL_TOLERANCE:
            return {"branch":branch,"status":"UNKNOWN_RARE_BRANCH_NUMERICS","output":None}
        self._serial+=1
        label=tuple((x+(y if branch==0 else -y))%a.modulus for x,y in zip(a.label,b.label))
        child=ProductPhaseReceipt(f"vector-merge:{self._serial}:{left}",a.modulus,label,a.ancestors+b.ancestors,
                                  1+max(a.merge_depth,b.merge_depth))
        self._states[child.id]=_valid_density(blocks[branch]/p)
        self._receipts[child.id]=child
        self._active.add(child.id)
        return {"branch":branch,"status":"PHYSICAL_BRANCH_SAMPLED","output":child.public_view()}


def audit_product_batch(source,reference,batch):
    bound=fingerprint(public_source(source))
    if (reference.get("QFT_group")!=GROUP or fingerprint(reference["public_source"])!=bound
            or batch.metadata.get("public_source_fingerprint")!=bound):
        raise ValueError("matching product-group source/reference/batch required")
    F=DyadicField(reference["reference_root"])
    outcomes={tuple(row["label"]):row for row in reference["all_label_outcomes"]}
    errors=[]
    for receipt in batch.receipts:
        row=outcomes[receipt.label]
        mass=F.value(_decode(row["joint_label_probability"],F)).real
        if mass<=NUMERICAL_TOLERANCE:raise ValueError("UNKNOWN_RARE_PRODUCT_REFERENCE_BRANCH")
        rho=np.array([[F.value(_decode(x,F)) for x in r] for r in row["unnormalized_colour_density"]])/mass
        errors.append(float(np.max(abs(rho-batch._densities[receipt.id]))))
    if max(errors,default=0)>NUMERICAL_TOLERANCE:
        raise ValueError("compiled product source disagrees with complete instrument")
    return {"all_emitted_product_densities_agree":True,"private_max_numerical_error":max(errors,default=0),
            "metadata":batch.metadata,"public_receipts":batch.public_receipts(),
            "PRIVATE_AUDIT_ONLY_density_matrices":{k:_serialize_density(v) for k,v in batch._densities.items()},
            "speedup_or_hardware_certificate":False}


def decode_parent_shift(source,residue_vector):
    q=2*source.box
    h=tuple(residue_vector)
    if len(h)!=source.dimension or any(type(x) is not int or not 0<=x<q for x in h):
        raise ValueError("canonical complete vector-group residue required")
    h=tuple(x-q if x>=source.box else x for x in h)
    d=tuple(source.prime*x+source.residue if j==source.coordinate else x for j,x in enumerate(h))
    vector=tuple(sum(c*row[j] for c,row in zip(d,source.basis)) for j in range(source.dimension))
    return {"balanced_parent_shift":h,"basis_coefficients":d,"public_lattice_vector":vector,
            "correct_vector_or_shortest_vector_certified":False,
            "positive_visibility_and_parent_bounds_needed_for_unique_signed_reconstruction":True}


def group_resource_comparison(rank,parent_box_bits):
    integer(rank,"original lattice rank",1)
    integer(parent_box_bits,"parent box bits",1)
    L=parent_box_bits+1
    N=rank*L
    return {"original_rank":rank,"coordinate_bits":L,"total_label_entropy_bits":N,
            "cyclic_group":{"rank":1,"modulus_bits":N,"full_QFT_controlled_phases":N*(N-1)//2},
            "product_group":{"rank":rank,"modulus_bits_per_coordinate":L,
                             "full_local_QFT_controlled_phases":rank*L*(L-1)//2},
            "optional_scalar_to_restricted_native_lift":{"rank":max(0,N-8),"modulus_bits_per_coordinate":N,
                                                         "secret_entropy_bits":max(0,N-8)*N},
            "product_has_smaller_group_entropy_than_unlifted_cyclic_source":False,
            "group_isomorphism_or_equal_decoder_difficulty_claimed":False,
            "restricted_first_bit_guarantee_is_full_vector_guarantee":False}


def build_report():
    sources=(SineWindowSource(((1,),),7,1,0,2,4),
             SineWindowSource(((17,0),(16,1)),7,1,0,2,4),
             SineWindowSource(((1,),),3,1,0,2,4))
    vectors=((1,),(1,-1),(1,))
    controls=[]
    for i,(source,vector) in enumerate(zip(sources,vectors)):
        compiled=compile_product_source(source)
        reference=exact_product_reference(source)
        batch=simulate_product_batch(compiled,4,191510+i,f"product-source-{i}")
        controls.append({"resources":compiled.resource_record(),"complete_instrument":reference,
                         "private_forward_template":audit_product_template(source,reference,vector),
                         "actual_source_audit":audit_product_batch(source,reference,batch)})
    large=compile_product_source(SineWindowSource(((10000,1000),(9999,1000)),389,1,0,256,128))
    return {"schema_version":1,"contract_id":CONTRACT_ID,
            "status":"PHYSICAL_PRODUCT_GROUP_SOURCE_FULL_VECTOR_DECODER_MISSING",
            "actual_source_controls":controls,"large_compiled_not_simulated":large.resource_record(),
            "actual_source_preparations_charged":12,
            "same_parent_group_resource_comparisons":[group_resource_comparison(n,4*n) for n in (8,16,32,64)],
            "relabeling_cyclic_receipts_as_vector_receipts_is_valid":False,
            "restricted_native_first_bit_predictor_alone_decodes_general_vector_shifts":False,
            "uniform_polynomial_full_vector_decoder_supplied":False,
            "accepted_speedup_candidate":False,"new_active_negative_result_created":False,"novelty_claim":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args=parser.parse_args()
    r=build_report()
    if args.write:REPORT.write_text(json.dumps(exact_json(r),indent=2)+"\n")
    print(json.dumps({"status":r["status"],"actual_source_preparations":r["actual_source_preparations_charged"],
                      "full_vector_decoder":False}))


if __name__=="__main__":main()
