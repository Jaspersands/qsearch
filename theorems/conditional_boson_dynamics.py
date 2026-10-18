"""Natural-dynamics candidate test: controlled displacement vs scalar readout.

Known polaron mechanism; local baseline derivation/review pending, no novelty
or quantum advantage. Infinite coherent-state formulas are checked against
actual finite Fock-space Hamiltonian evolution, with explicit cutoff bounds.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import factorial,pi,sqrt,isqrt
from pathlib import Path
import random

from flint import arb,acb,ctx,fmpq
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/"research/classical_baselines/conditional_boson_dynamics.json"


class DynamicsLimit(RuntimeError):
    """Operational UNKNOWN, never a classical-hardness or no-solution claim."""


def rational(value):
    if type(value) not in (int,str,Fraction):
        raise ValueError("exact integer, rational string or Fraction required; no floats/bools")
    return Fraction(value)


def positive_integer(value,name):
    if type(value) is not int or value < 1:
        raise ValueError(f"positive integer {name} required")
    return value


def ball(value):
    value = rational(value)
    return arb(fmpq(value.numerator,value.denominator))


def endpoint(value):
    value = value.fmpq()
    return Fraction(int(value.numerator),int(value.denominator))


@dataclass(frozen=True)
class DensityForceModel:
    frequencies: tuple
    force_offsets: tuple
    force_matrix: tuple
    diagonal_linear: tuple
    diagonal_pairs: tuple = ()
    diagonal_constant: Fraction = Fraction(0)

    def __post_init__(self):
        w = tuple(rational(x) for x in self.frequencies)
        f = tuple(rational(x) for x in self.force_offsets)
        G = tuple(tuple(rational(x) for x in row) for row in self.force_matrix)
        h = tuple(rational(x) for x in self.diagonal_linear)
        if not w or not h or len(f) != len(w) or len(G) != len(w) or any(len(row) != len(h) for row in G):
            raise ValueError("positive mode/control counts and matching public matrix dimensions required")
        if any(x <= 0 for x in w):
            raise ValueError("strictly positive oscillator frequencies required")
        pairs = []
        seen = set()
        for i,j,c in self.diagonal_pairs:
            if type(i) is not int or type(j) is not int or not 0 <= i < j < len(h) or (i,j) in seen:
                raise ValueError("unique ordered in-range diagonal pairs required")
            seen.add((i,j));pairs.append((i,j,rational(c)))
        for name,value in (("frequencies",w),("force_offsets",f),("force_matrix",G),
                           ("diagonal_linear",h),("diagonal_pairs",tuple(pairs)),
                           ("diagonal_constant",rational(self.diagonal_constant))):
            object.__setattr__(self,name,value)

    @property
    def controls(self): return len(self.diagonal_linear)

    def configuration(self,z):
        z = tuple(z)
        if len(z) != self.controls or any(type(v) is not int or v not in (0,1) for v in z):
            raise ValueError("canonical configuration bits required")
        return z

    def force(self,z):
        z = self.configuration(z)
        return tuple(c+sum(a*x for a,x in zip(row,z)) for c,row in zip(self.force_offsets,self.force_matrix))

    def energy(self,z):
        z = self.configuration(z)
        return self.diagonal_constant+sum(a*x for a,x in zip(self.diagonal_linear,z))+sum(c*z[i]*z[j] for i,j,c in self.diagonal_pairs)

    def public_record(self):
        return {"frequencies":tuple(map(str,self.frequencies)),"force_offsets":tuple(map(str,self.force_offsets)),
                "force_matrix":tuple(tuple(map(str,row)) for row in self.force_matrix),
                "diagonal_linear":tuple(map(str,self.diagonal_linear)),
                "diagonal_pairs":tuple((i,j,str(c)) for i,j,c in self.diagonal_pairs),
                "diagonal_constant":str(self.diagonal_constant),
                "initial_controls": "uniform logical plus; dual-rail fixed-particle realization allowed",
                "initial_bosons": "vacuum", "noncommuting_hopping_included":False}


def pauli_action(pauli,z):
    if not isinstance(pauli,str) or len(pauli) != len(z) or any(p not in "IXYZ" for p in pauli):
        raise ValueError("one canonical I/X/Y/Z per logical control required")
    flipped = tuple(x ^ int(p in "XY") for p,x in zip(pauli,z))
    phase = (1,1j,-1,-1j)[pauli.count("Y") % 4]*(-1)**sum(x for p,x in zip(pauli,z) if p in "YZ")
    return flipped,phase


def _pair_ball(model,time_pi,pauli,z):
    z = model.configuration(z)
    other,factor = pauli_action(pauli,z)
    f,g = model.force(z),model.force(other)
    turns = -time_pi*(model.energy(z)-model.energy(other))
    damping,sine_phase = arb(0),arb(0)
    for w,a,b in zip(model.frequencies,f,g):
        angle = w*time_pi
        angle_q = fmpq(angle.numerator,angle.denominator)
        sin_theta = arb.sin_pi_fmpq(angle_q)
        cos_theta = arb.cos_pi_fmpq(angle_q)
        delta_square = (a*a-b*b)/(w*w)  # exact subtraction before any rounding
        turns += delta_square*angle
        sine_phase -= ball(delta_square)*sin_theta
        damping += ball(((a-b)/w)**2)*(1-cos_theta)
    value = acb(-damping,sine_phase).exp()*acb(ball(turns % 2)).exp_pi_i()
    return value*acb(int(factor.real),int(factor.imag))


def certified_pair(model,time_pi,pauli,z,*,arithmetic_error=Fraction(1,2**40),max_precision_bits=4096):
    if not isinstance(model,DensityForceModel):
        raise ValueError("typed public density-force Hamiltonian required")
    t,eta = rational(time_pi),rational(arithmetic_error)
    if not 0 < eta <= 1:
        raise ValueError("positive arithmetic tolerance <=1 required")
    positive_integer(max_precision_bits,"precision cap")
    precision = min(64,max_precision_bits)
    while True:
        with ctx.workprec(precision):
            value = _pair_ball(model,t,pauli,z).real
            if value.is_finite():
                lo,hi = endpoint(value.lower()),endpoint(value.upper())
                if hi-lo <= 2*eta:
                    # The analytical integrand lies in [-1,1]; intersect its
                    # certified enclosure, never renormalize a physical state.
                    lo,hi = max(Fraction(-1),lo),min(Fraction(1),hi)
                    if lo > hi: raise ArithmeticError("coherent overlap violated its norm bound")
                    return {"lower":str(lo),"upper":str(hi),"precision_bits":precision,
                            "time_in_pi_units":str(t),"observable":pauli,"configuration":tuple(z),
                            "arithmetic_error_upper":str((hi-lo)/2),"relative_phase_retained":True}
        if precision >= max_precision_bits:
            raise DynamicsLimit("UNKNOWN_COHERENT_OVERLAP_PRECISION_CAP")
        precision = min(2*precision,max_precision_bits)


def exact_configuration_reference(model,time_pi,pauli,*,max_configurations=1024,**kwargs):
    positive_integer(max_configurations,"configuration cap")
    if model.controls > max_configurations.bit_length() or 2**model.controls > max_configurations:
        raise DynamicsLimit("UNKNOWN_EXPONENTIAL_CONFIGURATION_REFERENCE_CAP")
    lo,hi,max_bits = Fraction(),Fraction(),0
    for z in product((0,1),repeat=model.controls):
        row = certified_pair(model,time_pi,pauli,z,**kwargs)
        lo += Fraction(row["lower"]); hi += Fraction(row["upper"])
        max_bits = max(max_bits,row["precision_bits"])
    count = 2**model.controls
    return {"lower":str(lo/count),"upper":str(hi/count),"configurations_enumerated":count,
            "max_precision_bits_used":max_bits,"exponential_reference_is_the_scalable_estimator":False}


def exact_low_weight_readout(model,time_pi,pauli,*,arithmetic_error=Fraction(1,2**40),
                            max_flipped_assignments=1024,max_precision_bits=4096):
    """Sum all UNFLIPPED bits analytically; exponential only in Pauli X/Y weight."""
    t,eta = rational(time_pi),rational(arithmetic_error)
    positive_integer(max_flipped_assignments,"flipped-assignment cap")
    positive_integer(max_precision_bits,"precision cap")
    if not 0 < eta <= 1: raise ValueError("positive arithmetic tolerance <=1 required")
    pauli_action(pauli,(0,)*model.controls)
    flipped = tuple(j for j,p in enumerate(pauli) if p in "XY")
    free = tuple(j for j,p in enumerate(pauli) if p in "IZ")
    k = len(flipped)
    if k > max_flipped_assignments.bit_length() or 2**k > max_flipped_assignments:
        raise DynamicsLimit("UNKNOWN_FLIP_WEIGHT_CAP; general additive Monte Carlo remains available")
    precision = min(64,max_precision_bits)
    while True:
        with ctx.workprec(precision):
            total = acb(0)
            for u in product((0,1),repeat=k):
                z = [0]*model.controls
                for j,x in zip(flipped,u): z[j] = x
                z = tuple(z);other,_ = pauli_action(pauli,z)
                value = _pair_ball(model,t,pauli,z)
                f,g = model.force(z),model.force(other)
                energy_increment = [Fraction() for _ in z]
                for i,j,c in model.diagonal_pairs:
                    if i in flipped and j in free: energy_increment[j] += c*(z[i]-other[i])
                    if j in flipped and i in free: energy_increment[i] += c*(z[j]-other[j])
                for j in free:
                    turns = -t*energy_increment[j]+int(pauli[j] == "Z")
                    sine_phase = arb(0)
                    for w,a,b,row in zip(model.frequencies,f,g,model.force_matrix):
                        coefficient = 2*row[j]*(a-b)/(w*w)
                        angle = w*t
                        turns += coefficient*angle
                        sine_phase -= ball(coefficient)*arb.sin_pi_fmpq(fmpq(angle.numerator,angle.denominator))
                    phase = acb(0,sine_phase).exp()*acb(ball(turns % 2)).exp_pi_i()
                    value *= (1+phase)/2
                total += value
            answer = (total/2**k).real
            if answer.is_finite():
                lo,hi = endpoint(answer.lower()),endpoint(answer.upper())
                if hi-lo <= 2*eta:
                    lo,hi = max(Fraction(-1),lo),min(Fraction(1),hi)
                    if lo > hi: raise ArithmeticError("summed Pauli violated its norm bound")
                    return {"lower":str(lo),"upper":str(hi),
                            "time_in_pi_units":str(t),"observable":pauli,"controls":model.controls,
                            "max_precision_bits_used":precision,"flipped_assignments":2**k,
                            "analytically_summed_control_bits":len(free),"no_statistical_sampling":True,
                            "cost_upper_order":"O(2^k*poly(n,M,input_bits,precision)); k=Pauli X/Y weight"}
        if precision >= max_precision_bits:
            raise DynamicsLimit("UNKNOWN_LOW_WEIGHT_READOUT_PRECISION_CAP")
        precision = min(2*precision,max_precision_bits)


def estimate_pauli(model,time_pi,pauli,*,epsilon=Fraction(1,4),failure_bits=4,seed=None,
                   max_samples=100000,max_precision_bits=4096):
    eps = rational(epsilon)
    if not 0 < eps <= 1: raise ValueError("0<epsilon<=1 required")
    positive_integer(failure_bits,"failure exponent");positive_integer(max_samples,"sample cap")
    # ln2<1: this integer choice suffices for Hoeffding at epsilon/2.
    size = (Fraction(8*(failure_bits+1),1)/(eps*eps)).__ceil__()
    if size > max_samples:
        raise DynamicsLimit("UNKNOWN_MONTE_CARLO_SAMPLE_CAP; not a hardness claim")
    model.configuration((0,)*model.controls);pauli_action(pauli,(0,)*model.controls)
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    lo,hi,max_bits = Fraction(),Fraction(),0
    for _ in range(size):
        z = tuple(rng.randrange(2) for _ in range(model.controls))
        row = certified_pair(model,time_pi,pauli,z,arithmetic_error=eps/8,
                             max_precision_bits=max_precision_bits)
        lo += Fraction(row["lower"]); hi += Fraction(row["upper"])
        max_bits = max(max_bits,row["precision_bits"])
    lo,hi = lo/size,hi/size
    return {"arithmetic_sample_mean_interval":(str(lo),str(hi)),
            "time_in_pi_units":str(rational(time_pi)),
            "observable":pauli,"controls":model.controls,"boson_modes":len(model.frequencies),
            "confidence_interval":(str(max(Fraction(-1),lo-eps/2)),str(min(Fraction(1),hi+eps/2))),
            "additive_error_target":str(eps),"failure_probability_model_upper":str(Fraction(1,2**failure_bits)),
            "coverage_requires_IID_uniform_random_bits":True,
            "seeded_replay_is_a_certified_IID_source":False,
            "randomness_mode":"OS_RANDOM_BITS_WITH_IID_MODEL_ASSUMPTION" if seed is None else "SEEDED_PSEUDORANDOM_REPLAY",
            "sample_count":size,"configuration_random_bits_charged":size*model.controls,
            "max_precision_bits_used":max_bits,"bosonic_cutoff_materialized":False,
            "all_joint_measurement_outcomes_sampled":False,"relative_error_for_tiny_expectations_certified":False}


def uniform_fock_cutoff_bound(model,time_pi,cutoff):
    positive_integer(cutoff,"Fock dimension")
    if cutoff > 128: raise DynamicsLimit("UNKNOWN_CALIBRATION_CUTOFF_BOUND_CAP")
    with ctx.workprec(256):
        state_error = arb(0)
        for w,c,row in zip(model.frequencies,model.force_offsets,model.force_matrix):
            force = abs(c)+sum(abs(x) for x in row)
            peak_mean = 4*(force/w)**2
            q = min(Fraction(1),peak_mean**cutoff/factorial(cutoff))
            state_error += (1+arb.pi()*ball(abs(rational(time_pi))*force)*arb(cutoff).sqrt())*ball(q).sqrt()
        upper = min(Fraction(2),endpoint(state_error.upper()))
    return {"state_2norm_error_upper":str(upper),"Pauli_expectation_error_upper":str(min(Fraction(2),2*upper)),
            "Hamiltonian_sector":"DIAGONAL_FERMION_FORCES_NO_HOPPING",
            "uniform_in_control_configurations":True,"includes_intermediate_boundary_leakage":True,
            "numeric_sparse_exponential_roundoff_certified":False}


def weak_hopping_readout_budget(model,time_pi,hopping,epsilon):
    """Duhamel's task bound, not an assertion that hopping is always negligible."""
    J = tuple(rational(x) for x in hopping)
    eps = rational(epsilon)
    if len(J) != model.controls or not 0 < eps <= 1:
        raise ValueError("matching hopping vector and 0<epsilon<=1 required")
    with ctx.workprec(256):
        error = 2*arb.pi()*ball(abs(rational(time_pi))*sum(abs(x) for x in J))
        upper = min(Fraction(2),endpoint(error.upper()))
    return {"time_in_pi_units":str(rational(time_pi)),"hopping":tuple(map(str,J)),
            "additional_Pauli_expectation_error_upper":str(upper),
            "H0_estimator_with_reduced_error_budget_suffices":upper < eps,
            "remaining_additive_error_budget":str(max(Fraction(),eps-upper)),
            "large_bound_is_evidence_of_quantum_advantage":False}


def fock_reference(model,time_pi,pauli,cutoff,*,hopping=None,max_states=32768):
    positive_integer(cutoff,"Fock dimension");positive_integer(max_states,"state cap")
    n,M = model.controls,len(model.frequencies)
    if n > max_states.bit_length() or (2**n)*cutoff**M > max_states:
        raise DynamicsLimit("UNKNOWN_EXPLICIT_FOCK_STATE_CAP")
    J = (Fraction(),)*n if hopping is None else tuple(rational(x) for x in hopping)
    if len(J) != n: raise ValueError("one logical hopping coefficient per control required")
    pauli_action(pauli,(0,)*n)
    configurations = tuple(product((0,1),repeat=n))
    for z in configurations:
        if max(abs(f/w) for f,w in zip(model.force(z),model.frequencies)) > 16:
            raise DynamicsLimit("UNKNOWN_FOCK_CALIBRATION_FORCE_CAP")
    duration = rational(time_pi)
    scale = (sum(abs(w)*cutoff for w in model.frequencies)
             +max(abs(model.energy(z))+2*(isqrt(cutoff)+1)*sum(abs(f) for f in model.force(z))
                  for z in configurations)+sum(abs(x) for x in J))
    if 4*abs(duration)*scale > 10000:
        raise DynamicsLimit("UNKNOWN_FOCK_CALIBRATION_TIME_ENERGY_CAP")
    one = sparse.eye(cutoff,format="csr")
    number = sparse.diags(np.arange(cutoff,dtype=float),format="csr")
    annihilation = sparse.diags(np.sqrt(np.arange(1,cutoff,dtype=float)),1,shape=(cutoff,cutoff),format="csr")
    positions,numbers = [],[]
    for mode in range(M):
        p,N = sparse.csr_matrix([[1.0]]),sparse.csr_matrix([[1.0]])
        for j in range(M):
            p = sparse.kron(p,annihilation+annihilation.T if j == mode else one,format="csr")
            N = sparse.kron(N,number if j == mode else one,format="csr")
        positions.append(p);numbers.append(N)
    D = cutoff**M; identity = sparse.eye(D,format="csr")
    blocks = []
    for z in configurations:
        H = float(duration*model.energy(z))*identity
        for w,f,N,x in zip(model.frequencies,model.force(z),numbers,positions): H = H+float(duration*w)*N+float(duration*f)*x
        blocks.append(H)
    H = sparse.block_diag(blocks,format="csr")
    index = {z:i for i,z in enumerate(configurations)}
    for j,coefficient in enumerate(J):
        if coefficient:
            rows = [index[tuple(x ^ int(k == j) for k,x in enumerate(z))] for z in configurations]
            X = sparse.coo_matrix((np.ones(len(rows)),(rows,np.arange(len(rows)))),shape=(2**n,2**n)).tocsr()
            H = H+float(duration*coefficient)*sparse.kron(X,identity,format="csr")
    initial = np.zeros((2**n)*D,complex);initial[::D] = 1/sqrt(2**n)
    generator = (-1j*pi)*H  # Exact duration products were formed before float conversion.
    state = expm_multiply(generator,initial,traceA=generator.diagonal().sum()).reshape((2**n,D))
    value = 0j
    for i,z in enumerate(configurations):
        other,phase = pauli_action(pauli,z)
        value += phase*np.vdot(state[index[other]],state[i])
    if abs(value.imag) > 1e-9: raise ArithmeticError("Hermitian Pauli acquired imaginary expectation")
    return {"Pauli_expectation":float(value.real),"norm_squared":float(np.sum(abs(state)**2)),
            "explicit_state_dimension":len(initial),"Fock_dimension_per_mode":cutoff,
            "hopping":tuple(map(str,J)),"noncommuting_hopping_included":any(J),
            "finite_Fock_recurrence_is_exact_infinite_displacement":False,
            "floating_sparse_reference_is_formally_certified":False}


def run_controls():
    revival = DensityForceModel((1,),(0,),((Fraction(1,2),),),(0,))
    interacting = DensityForceModel((1,),(Fraction(1,5),),((Fraction(2,5),Fraction(-1,3)),),
                                   (Fraction(1,7),Fraction(-1,5)),((0,1,Fraction(3,11)),))
    controls = []
    for model,time,pauli in ((revival,Fraction(2),"Y"),(revival,Fraction(2),"X"),
                             (interacting,Fraction(3,5),"XY"),(interacting,Fraction(3,5),"XX")):
        ref = exact_configuration_reference(model,time,pauli)
        controls.append({"model":model.public_record(),"time_in_pi_units":str(time),"observable":pauli,
                         "analytic_reference":ref,"finite_Fock_reference":fock_reference(model,time,pauli,24),
                         "cutoff_bound":uniform_fock_cutoff_bound(model,time,24)})
    contrast = {"model":revival.public_record(),"time_in_pi_units":"1/2","observable":"X",
                "no_hopping":fock_reference(revival,Fraction(1,2),"X",24),
                "with_hopping":fock_reference(revival,Fraction(1,2),"X",24,hopping=(Fraction(2,3),)),
                "perturbative_readout_budget":weak_hopping_readout_budget(revival,Fraction(1,2),(Fraction(2,3),),Fraction(1,10)),
                "H0_estimator_claimed_valid_after_adding_hopping":False}
    large = DensityForceModel((1,),(2**80,),((1,),),(0,))
    large_pair = certified_pair(large,Fraction(1,3),"X",(0,))
    n = 64
    bank = DensityForceModel((1,2),(0,0),tuple(tuple(Fraction((i*j+j)%5-2,16) for j in range(n)) for i in range(2)),
                            (Fraction(1,13),)*n)
    estimate = estimate_pauli(bank,Fraction(2,7),"X"*n,epsilon=Fraction(1,2),failure_bits=3,seed=671020)
    return {"schema_version":1,"status":"CONTROLLED_DISPLACEMENT_SCALAR_READOUT_HAS_A_CLASSICAL_BASELINE",
            "proof_status":"LOCAL_DERIVATION_REVIEW_PENDING","physical_controls":controls,
            "noncommuting_scope_falsifier":contrast,"large_force_exact_input_pair":large_pair,
            "large_force_model":large.public_record(),"64_control_model":bank.public_record(),
            "64_control_seeded_estimator":estimate,
            "64_control_exact_local_readout":exact_low_weight_readout(bank,Fraction(2,7),"X"+"I"*(n-1)),
            "general_Hubbard_Holstein_or_joint_sampling_dequantized":False,
            "new_active_negative_result_created":False,"accepted_speedup_candidate":False,"novelty_claim":False,
            "dependency_sha256":{str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true")
    args = parser.parse_args();report = run_controls()
    if args.write: REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"controls":len(report["physical_controls"]),
                      "large_force_precision_bits":report["large_force_exact_input_pair"]["precision_bits"],
                      "large_sampler_configurations":report["64_control_seeded_estimator"]["sample_count"],
                      "accepted_speedup_candidate":False}))


if __name__ == "__main__": main()
