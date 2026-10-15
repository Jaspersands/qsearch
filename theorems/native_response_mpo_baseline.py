"""Paid exact-integer MPS baseline for fixed public-phase/Fourier schedules.

No truncating SVD, dense word bank, private errors, or unknown quantum-copy
access. A finite-precision Fourier MPO has deterministic digit memory; all
normalization and prefix readout use FLINT exact integer matrix arithmetic.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import secrets

from flint import fmpz_mat
from native_banded_qft_baseline import (BaselineResourceLimit, ceil_log2,
    certified_dyadic_root, positive)
from native_response_fourier_factorization_audit import site_phase_tables
from ternary_measured_lattice_decoder import exact_json

ROOT=Path(__file__).resolve().parents[1]
DERIVATION=ROOT/"research/NATIVE_RESPONSE_MPO_BASELINE.md"
CONTRACT=ROOT/"research/hypotheses/native_response_mpo_baseline_contract.json"
REPORT=ROOT/"research/classical_baselines/native_response_mpo_baseline.json"
THREE_CALL=(("phase",1),("fourier",1),("phase",-1),("fourier",-1),("phase",1),("fourier",1))


def encode_integer(value):
    return str(value) if abs(value).bit_length()<=4096 else hex(value)


@dataclass(frozen=True)
class MPOPolicy:
    max_bond: int=128
    max_tensor_entries: int=2000000
    max_environment_entries: int=2000000
    max_phase_entries: int=100000
    max_enclosure_bits: int=4096
    max_readout_complex_matrix_products: int=100000

    def __post_init__(self):
        for name,value in asdict(self).items():positive(value,name)


def checked_schedule(schedule):
    steps=tuple(tuple(step) for step in schedule)
    if not steps or any(len(s)!=2 or s[0] not in ("phase","fourier") or
        type(s[1]) is not int or s[1] not in (-1,1) for s in steps):
        raise ValueError("nonempty fixed public phase/Fourier signed schedule required")
    return steps


def bond_profiles(M,b,schedule,max_bond=None):
    positive(M,"sites");positive(b,"bandwidth")
    if b>M:raise ValueError("bandwidth <= M required")
    steps=checked_schedule(schedule);bonds=[1]*(M+1);profiles=[]
    for kind,sign in steps:
        if kind=="fourier":
            if sign==-1:bonds.reverse()
            for j in range(1,M):
                bonds[j]*=3**min(b-1,j)
                if max_bond is not None and bonds[j]>max_bond:
                    raise BaselineResourceLimit("UNKNOWN_MPS_BOND_CAP")
            if sign==1:bonds.reverse()
        profiles.append(tuple(bonds))
    return tuple(profiles)


def schedule_ledger(M,b,schedule,failure_bits,full_cyclic=False):
    positive(M,"sites");positive(b,"bandwidth");positive(failure_bits,"failure bits")
    steps=checked_schedule(schedule)
    if type(full_cyclic) is not bool:raise ValueError("explicit boolean target model required")
    if b>M and not full_cyclic:raise ValueError("bandwidth <= M required")
    S=len(steps);Q=sum(k=="fourier" for k,_ in steps)
    if full_cyclic:
        target=64*max(1,Q)*M*2**failure_bits;b,power=1,3
        while b<M and power<target:b+=1;power*=3
    else:target=None
    P=failure_bits+ceil_log2(128*S*M*3**M)
    K=failure_bits+ceil_log2(8*M)
    epsilon=Fraction(4,2**P)
    eta=2*3**M*M*epsilon
    state_error=2*S*eta
    phase_TV=2*state_error
    grid_TV=Fraction(2*M,2**K)
    omitted=sum((Fraction(M-d,3**(d+1)) for d in range(b,M)),Fraction(0)) if full_cyclic else Fraction(0)
    truncation=Q*Fraction(176,7)*omitted
    assert S*eta<=Fraction(1,2) and state_error<1
    assert phase_TV+grid_TV+truncation<=Fraction(1,2**failure_bits)
    return {"word_sites_M":M,"operations_S":S,"Fourier_calls_Q":Q,
        "requested_accuracy_bits_f":failure_bits,"target_full_cyclic":bool(full_cyclic),
        "selected_bandwidth_b":b,"full_cyclic_cutoff_threshold":None if target is None else str(target),
        "phase_grid_bits_P":P,"random_bits_per_digit_K":K,"root_error_upper":str(epsilon),
        "per_operation_operator_error_upper":str(eta),"unnormalized_state_error_upper":str(state_error),
        "normalized_phase_TV_upper":str(phase_TV),"random_grid_TV_upper":str(grid_TV),
        "all_QFT_truncations_TV_upper":str(truncation),
        "per_sample_TV_upper_under_IID_bits":str(phase_TV+grid_TV+truncation),
        "MPO_bond_upper":3**(b-1),"MPS_bond_upper":3**(Q*(b-1)),
        "intermediate_integer_bits_upper":2*M*S*(P+4)+4*(M+1)*Q*(b-1)+4*M+4,
        "polynomial_structural_simulation_requires_fixed_Q":True,
        "polynomial_Q_or_exponential_accuracy_is_not_covered":True,
        "rare_prefix_precision_or_free_normalization_assumed":False}


@dataclass(frozen=True)
class GaussianMatrix:
    real: fmpz_mat
    imag: fmpz_mat

    @classmethod
    def zero(cls,r,c):return cls(fmpz_mat(r,c),fmpz_mat(r,c))

    @classmethod
    def scalar(cls,x):return cls(fmpz_mat([[x]]),fmpz_mat([[0]]))

    @property
    def shape(self):return self.real.nrows(),self.real.ncols()

    def plus(self,other):return GaussianMatrix(self.real+other.real,self.imag+other.imag)

    def times(self,other):
        return GaussianMatrix(self.real*other.real-self.imag*other.imag,
            self.real*other.imag+self.imag*other.real)

    def scale(self,z):return GaussianMatrix(z[0]*self.real-z[1]*self.imag,z[1]*self.real+z[0]*self.imag)

    def transpose(self):return GaussianMatrix(self.real.transpose(),self.imag.transpose())

    def adjoint(self):return GaussianMatrix(self.real.transpose(),-self.imag.transpose())

    def bits(self):
        return max((abs(int(x)).bit_length() for matrix in (self.real,self.imag) for row in matrix.tolist() for x in row),default=0)


class PublicPhaseMPOBaseline:
    def __init__(self,phase_tables,q,schedule=THREE_CALL,bandwidth=2,failure_bits=24,
                 full_cyclic=False,policy=None):
        positive(q,"modulus",2)
        self.phases=tuple(tuple(row) for row in phase_tables)
        if not self.phases or any(len(row)!=3 or any(type(x) is not int or not 0<=x<q for x in row) for row in self.phases):
            raise ValueError("canonical public three-digit phase tables required")
        self.M,self.q=len(self.phases),q;self.schedule=checked_schedule(schedule)
        self.policy=MPOPolicy() if policy is None else policy
        if not isinstance(self.policy,MPOPolicy):raise ValueError("typed MPO resource policy required")
        self.ledger=schedule_ledger(self.M,bandwidth,self.schedule,failure_bits,full_cyclic)
        self.b=self.ledger["selected_bandwidth_b"];self.P=self.ledger["phase_grid_bits_P"];self.K=self.ledger["random_bits_per_digit_K"]
        self.profiles=bond_profiles(self.M,self.b,self.schedule,self.policy.max_bond)
        if max(max(p) for p in self.profiles)>self.policy.max_bond:
            raise BaselineResourceLimit("UNKNOWN_MPS_BOND_CAP")
        self.planned_entries=tuple(6*sum(p[j]*p[j+1] for j in range(self.M)) for p in self.profiles)
        if max(self.planned_entries)>self.policy.max_tensor_entries:
            raise BaselineResourceLimit("UNKNOWN_MPS_TENSOR_ENTRY_CAP")
        self.planned_environment_entries=2*sum(x*x for x in self.profiles[-1])
        if self.planned_environment_entries>self.policy.max_environment_entries:
            raise BaselineResourceLimit("UNKNOWN_MPS_ENVIRONMENT_ENTRY_CAP")
        if 3**self.b+6*self.M>self.policy.max_phase_entries:
            raise BaselineResourceLimit("UNKNOWN_MPO_PHASE_ENTRY_CAP")
        if self.P+16>self.policy.max_enclosure_bits:
            raise BaselineResourceLimit("UNKNOWN_ROOT_ENCLOSURE_PRECISION_CAP")
        self.roots={};self.stats={"complex_matrix_products":0,"underlying_FLINT_integer_matrix_products":0,
            "maximum_integer_bits_seen":0,"random_bits_consumed":0,"digit_reversals":0,
            "compiled_tensor_entries_peak":0,"MPO_block_accumulations":0,
            "compiler_integer_scalar_multiply_terms_upper":0,
            "readout_integer_scalar_multiply_terms_upper":0,
            "dense_word_table_or_state_allocated_by_sampler":False,
            "SVD_or_bond_truncation_used":False,"private_secret_or_errors_used":False}
        for r in range(3**self.b):self._root(Fraction(r,3**self.b))
        for kind,sign in self.schedule:
            if kind=="phase":
                for row in self.phases:
                    for phase in row:self._root(Fraction(sign*phase,q))
        self.state=tuple(tuple(GaussianMatrix.scalar(1) for _ in range(3)) for _ in range(self.M))
        self.environment=None
        for step,(kind,sign) in enumerate(self.schedule):
            if kind=="phase":
                self.stats["compiler_integer_scalar_multiply_terms_upper"]+=4*sum(
                    A.shape[0]*A.shape[1] for site in self.state for A in site)
                self.state=tuple(tuple(A.scale(self._root(Fraction(sign*self.phases[j][x],q))) for x,A in enumerate(site))
                                 for j,site in enumerate(self.state))
            else:
                if sign==-1:self._reverse()
                self._apply_fourier_memory(sign==-1)
                if sign==1:self._reverse()
            actual=tuple([self.state[0][0].shape[0]]+[site[0].shape[1] for site in self.state])
            if actual!=self.profiles[step]:raise ArithmeticError("compiled bonds disagree with preflight")
            self.stats["compiled_tensor_entries_peak"]=max(self.stats["compiled_tensor_entries_peak"],
                2*sum(A.shape[0]*A.shape[1] for site in self.state for A in site))
            for site in self.state:
                for A in site:self._observe(A)

    @classmethod
    def from_records(cls,records,mask,**kwargs):
        records=tuple(records);tables=site_phase_tables(records,mask)
        return cls(tuple(s["digit_phases"] for s in tables),records[0].modulus,**kwargs)

    def _root(self,turn):
        turn=Fraction(turn)%1
        if turn not in self.roots:self.roots[turn]=certified_dyadic_root(turn,self.P,self.policy.max_enclosure_bits)
        return self.roots[turn]["integer_value"]

    def _observe(self,A):
        self.stats["maximum_integer_bits_seen"]=max(self.stats["maximum_integer_bits_seen"],A.bits())

    def _times(self,A,B):
        C=A.times(B);self._observe(C)
        self.stats["complex_matrix_products"]+=1
        self.stats["underlying_FLINT_integer_matrix_products"]+=4
        self.stats["readout_integer_scalar_multiply_terms_upper"]+=4*A.shape[0]*A.shape[1]*B.shape[1]
        return C

    def _reverse(self):
        self.state=tuple(tuple(A.transpose() for A in site) for site in reversed(self.state))
        self.stats["digit_reversals"]+=1

    def _apply_fourier_memory(self,adjoint):
        sites=[]
        for j,site in enumerate(self.state):
            memories=tuple(product(range(3),repeat=min(self.b-1,j)))
            next_memories=((),) if j==self.M-1 else tuple(product(range(3),repeat=min(self.b-1,j+1)))
            following={s:i for i,s in enumerate(next_memories)}
            L,R=site[0].shape;DL,DR=len(memories),len(next_memories)
            output=[GaussianMatrix.zero(L*DL,R*DR) for _ in range(3)]
            for alpha,memory in enumerate(memories):
                for a,w in product(range(3),repeat=2):
                    following_memory=() if j==self.M-1 or self.b==1 else (memory+(a,))[-(self.b-1):]
                    beta=following[following_memory]
                    turn=Fraction(a*w,3)+sum((Fraction(memory[-d]*w,3**(d+1)) for d in range(1,len(memory)+1)),Fraction(0))
                    z=self._root(turn)
                    if adjoint:z=(z[0],-z[1])
                    out,input_digit=(w,a) if adjoint else (a,w)
                    block=site[input_digit].scale(z)
                    target=output[out]
                    for l in range(L):
                        for r in range(R):
                            target.real[l*DL+alpha,r*DR+beta]+=block.real[l,r]
                            target.imag[l*DL+alpha,r*DR+beta]+=block.imag[l,r]
                    self.stats["MPO_block_accumulations"]+=1
                    self.stats["compiler_integer_scalar_multiply_terms_upper"]+=4*L*R
            sites.append(tuple(output))
        self.state=tuple(sites)

    def _readout_preflight(self,samples):
        positive(samples,"samples")
        needed=(0 if self.environment is not None else 6*self.M)+9*self.M*samples
        if self.stats["complex_matrix_products"]+needed>self.policy.max_readout_complex_matrix_products:
            raise BaselineResourceLimit("UNKNOWN_COMPLETE_MPS_READOUT_WORK_CAP")

    def _environments(self):
        if self.environment is not None:return
        env=[None]*self.M+[GaussianMatrix.scalar(1)]
        for j in range(self.M-1,-1,-1):
            left=self.state[j][0].shape[0];result=GaussianMatrix.zero(left,left)
            for A in self.state[j]:result=result.plus(self._times(self._times(A,env[j+1]),A.adjoint()))
            self._observe(result);env[j]=result
        if env[0].shape!=(1,1) or int(env[0].imag[0,0])!=0 or int(env[0].real[0,0])<=0:
            raise ArithmeticError("nonzero normalized approximate state required")
        self.environment=tuple(env)

    def _mass(self,row,j):
        value=self._times(self._times(row,self.environment[j]),row.adjoint())
        re,im=int(value.real[0,0]),int(value.imag[0,0])
        if im or re<0:raise ArithmeticError("prefix mass must be real and nonnegative")
        return re

    def sample_many(self,count,randbits=None,record_trace=False):
        self._readout_preflight(count);self._environments()
        draw=secrets.randbits if randbits is None else randbits;output=[]
        for _ in range(count):
            row=GaussianMatrix.scalar(1);parent=int(self.environment[0].real[0,0]);prefix=[];trace=[];draws=[]
            for j,site in enumerate(self.state):
                children=tuple(self._times(row,A) for A in site)
                masses=tuple(self._mass(child,j+1) for child in children)
                if sum(masses)!=parent or parent<=0:raise ArithmeticError("exact child normalization failed")
                u=draw(self.K)
                if type(u) is not int or not 0<=u<2**self.K:raise ValueError("canonical K-bit draw required")
                self.stats["random_bits_consumed"]+=self.K;cumulative=0
                draws.append(encode_integer(u))
                for digit,mass in enumerate(masses):
                    cumulative+=mass
                    if u*parent<cumulative*2**self.K:break
                if record_trace:trace.append({"prefix":tuple(prefix),"child_weights":tuple(encode_integer(x) for x in masses),
                    "uniform_grid_integer":encode_integer(u),"selected_digit":digit})
                prefix.append(digit);row=children[digit];parent=masses[digit]
            output.append({"site_digits_MSB_first":tuple(prefix),"trace":tuple(trace),"uniform_grid_draws":tuple(draws)})
        return {"status":"COMPLETED_EXACT_INTEGER_MPS_SAMPLING","samples":tuple(output),
            "random_source":"SYSTEM_RANDOM_BITS" if randbits is None else "INJECTED_BITS_DIAGNOSTIC",
            "injected_PRNG_is_a_formal_IID_certificate":False,
            "batch_TV_upper_under_IID_bits":str(min(Fraction(1),count*Fraction(self.ledger["per_sample_TV_upper_under_IID_bits"]))) }

    def calibration_vector(self,max_dimension=81):
        if 3**self.M>max_dimension:raise BaselineResourceLimit("UNKNOWN_DENSE_CALIBRATION_CAP")
        # Diagnostics only. Do not count these matrix products as solver readout.
        result=[]
        for word in product(range(3),repeat=self.M):
            value=GaussianMatrix.scalar(1)
            for site,x in zip(self.state,word):value=value.times(site[x])
            result.append((encode_integer(int(value.real[0,0])),encode_integer(int(value.imag[0,0]))))
        return tuple(result)

    def public_record(self):
        return {"modulus_q":str(self.q),"public_digit_phase_tables":tuple(tuple(str(x) for x in row) for row in self.phases),
            "schedule":self.schedule,"accuracy_and_width_ledger":self.ledger,"bond_profiles":self.profiles,
            "planned_tensor_entries":self.planned_entries,"resource_policy":asdict(self.policy),
            "planned_environment_entries":self.planned_environment_entries,
            "phase_grid":tuple({**self.roots[t],"integer_value":tuple(str(x) for x in self.roots[t]["integer_value"])} for t in sorted(self.roots)),
            "observed_work":dict(self.stats),"normalization_is_exact_integer_not_postselection":True,
            "peak_process_memory_or_runtime_is_not_certified":True,
            "unknown_coset_copy_access_is_not_public_phase_access":True,
            "secret_recovery_or_new_quantum_speedup_claimed":False}

    def product_width_calibration(self):
        if any(A.shape!=(1,1) for site in self.state for A in site):return ()
        return tuple(tuple((encode_integer(int(A.real[0,0])),encode_integer(int(A.imag[0,0]))) for A in site) for site in self.state)


def control(M,b,seed,full=False):
    from native_full_root_slice import source_data
    raw,mask,_,_=source_data(1,2,M,True,seed)
    model=PublicPhaseMPOBaseline.from_records(raw,mask,bandwidth=b,failure_bits=20,full_cyclic=full)
    rng=random.Random(seed+1);samples=model.sample_many(2,rng.getrandbits,record_trace=M<=3)
    return {"original_records":tuple(r.public() for r in raw),"public_mask":tuple(mask),
        "model":model.public_record(),"sampling":samples,
        "small_calibration_integer_statevector":model.calibration_vector() if M<=3 else (),
        "product_width_calibration_site_vectors":model.product_width_calibration(),
        "growing_nonproduct_outcomes_independently_recomputed":False}


def build_report():
    controls=tuple(control(M,b,seed,full) for M,b,seed,full in (
        (2,1,100301,False),(2,2,100302,True),(3,2,100303,False),
        (16,2,100304,False),(64,1,100305,False)))
    profiles=tuple(schedule_ledger(M,1,THREE_CALL,f,True) for M,f in ((8,8),(64,20),(1024,10)))
    deps=("native_banded_qft_baseline.py","native_response_fourier_factorization_audit.py",
          "native_full_root_slice.py","native_basis_lottery.py","ternary_noise_degradation.py","ternary_measured_lattice_decoder.py")
    return {"status":"PUBLIC_PHASE_FIXED_LAYER_MPO_CLASSICAL_SAMPLING_BASELINE",
        "producer_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256":hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256":{p:hashlib.sha256((ROOT/"theorems"/p).read_bytes()).hexdigest() for p in deps},
        "controls":controls,"full_cyclic_fixed_layer_profiles":profiles,
        "fixed_Q_inverse_polynomial_accuracy_has_polynomial_structural_bound":True,
        "arbitrary_polynomial_depth_simulation_claimed":False,"unknown_phase_copy_simulation_claimed":False,
        "accepted_speedup_candidate":False,"new_active_negative_result_created":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true")
    args=parser.parse_args();report=build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(exact_json(report),indent=2)+"\n")
    print(report["status"]);print("Fixed public layers only; no unknown-copy or growing-depth no-go.")


if __name__=="__main__":main()
