"""Native comparison encoding and its scoped polynomial-normalization gate.

LOCAL DERIVATION / REVIEW PENDING. Bounded physical controls are exponential
calibration. This does not exclude direct structured decoders or general QSVT.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from dcp_adaptive_product_readout_bound import rational
from dcp_terminal_affine_fibers import _positive_integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/dcp_pgm_projected_encoding.json"


def _ceil_sqrt(x):
    value = math.isqrt(x.numerator//x.denominator)
    return value+int(value*value*x.denominator<x.numerator)


def normalization_certificate(n,L,m,degree,target_success=Fraction(1,2)):
    for value,name in ((n,"dimension"),(L,"modulus bits"),(m,"phase qubits"),(degree,"degree")):
        _positive_integer(value,name)
    if type(target_success) not in (int,Fraction) or not 0<target_success<=1:
        raise ValueError("exact target success in (0,1] required")
    G,N = 1 << (n*L),1 << m
    envelope = min(Fraction(1),Fraction(5*degree*degree,2*G))
    herald = Fraction(N+G-1,N*G)
    conditional = Fraction(N,N+G-1)
    exponent = (envelope.denominator//envelope.numerator).bit_length()-1
    return {"status":"SCOPED_PROJECTED_ENCODING_NORMALIZATION_GATE_REVIEW_PENDING",
            "dimension":n,"modulus_bits":L,"phase_qubits":m,"degree":degree,"density_surplus":m-n*L,
            "raw_comparison_unconditional_correct_probability":rational(Fraction(1,G)),
            "native_mean_raw_herald_probability":rational(herald),
            "native_pooled_correct_probability_given_raw_herald":rational(conditional),
            "odd_bounded_polynomial_correct_probability_upper_bound":rational(envelope),
            "conservative_correct_probability_dyadic_exponent":exponent,
            "target_success":rational(Fraction(target_success)),
            "minimum_degree_necessary_for_target_success":format(_ceil_sqrt(Fraction(2*G,5)*target_success),"x"),
            "polynomial_may_depend_on_all_public_labels":True,
            "all_scalar_or_vector_branches_require_joint_norm_bound_on_minus_one_to_one":True,
            "claimed_success_is_unconditional_not_herald_normalized":True,
            "also_bounds_arbitrary_classical_guess_from_label_and_branch_for_uniform_secret":True,
            "requires_same_fiber_character_singular_vectors_and_standard_secret_output":True,
            "arbitrary_interleaved_algorithms_or_other_encodings_ruled_out":False,
            "independent_review":False,"candidate_record_accepted":False,"novelty_claim":False,"speedup_claim_allowed":False}


def _bounded_labels(A,q):
    _positive_integer(q,"modulus")
    if q<2 or q&(q-1) or not isinstance(A,(list,tuple)) or not A or not isinstance(A[0],(list,tuple)) or not A[0]:
        raise ValueError("nonempty dyadic native label matrix required")
    n,m = len(A),len(A[0])
    if any(not isinstance(row,(list,tuple)) or len(row)!=m or any(type(v) is not int or not 0<=v<q for v in row) for row in A):
        raise ValueError("canonical rectangular labels required")
    if m>6 or q**n*2**m>256:
        raise ValueError("bounded calibration requires G*N<=256 and m<=6")
    return n,m


def _data(A,q):
    n,m = _bounded_labels(A,q)
    secrets = list(itertools.product(range(q),repeat=n))
    targets = list(itertools.product(range(q),repeat=n))
    position = {t:i for i,t in enumerate(targets)}
    sums = [tuple(sum(row[i]*x[i] for i in range(m)) % q for row in A)
            for x in itertools.product((0,1),repeat=m)]
    eta = [0]*len(targets)
    for t in sums:
        eta[position[t]] += 1
    phases = np.array([[np.exp(2j*math.pi*sum(v*w for v,w in zip(s,t))/q) for t in sums] for s in secrets])
    return secrets,eta,phases


def bounded_physical_control(A,q,degrees=(1,3,5,7)):
    n,m = _bounded_labels(A,q)
    if not degrees or any(type(d) is not int or d<=0 or d%2!=1 or d>31 for d in degrees):
        raise ValueError("odd positive calibration degrees <=31 required")
    secrets,eta,phases = _data(A,q)
    G,N = len(secrets),2**m
    Hs = np.array([[(-1)**((s&z).bit_count())/math.sqrt(G) for z in range(G)] for s in range(G)])
    Hx = np.array([[(-1)**((y&x).bit_count())/math.sqrt(N) for x in range(N)] for y in range(N)])
    # H on the candidate register, public controlled inverse phase, then H on X.
    U = np.einsum("sz,yx,sx->syzx",Hs,Hx,phases.conjugate()).reshape(G*N,G*N)
    assert np.max(np.abs(U.conjugate().T@U-np.eye(G*N)))<1e-9
    good_out = np.arange(G)*N
    good_in = np.arange(N)
    block = U[np.ix_(good_out,good_in)]
    assert np.max(np.abs(block-phases.conjugate()/math.sqrt(G*N)))<1e-9
    rin,rout = -np.ones(G*N),-np.ones(G*N)
    rin[good_in],rout[good_out] = 1,1
    sigma = np.sqrt(np.array(eta,dtype=float)/N)
    rows = []
    for degree in degrees:
        values = np.sin(degree*np.arcsin(np.minimum(1,sigma)))
        spectral_correct = float(np.sum(sigma*values)**2/G)
        spectral_herald = float(np.sum(sigma**2*values**2))
        probabilities = []
        output_probabilities = []
        for index,_ in enumerate(secrets):
            initial = np.zeros(G*N,dtype=complex)
            initial[good_in] = phases[index]/math.sqrt(N)
            state = U@initial
            for _ in range((degree-1)//2):
                state = -U@(rin*(U.conjugate().T@(rout*state)))
            norm = float(np.vdot(state,state).real)
            herald = float(np.sum(np.abs(state[good_out])**2))
            correct = float(abs(state[index*N])**2)
            assert abs(norm-1)<1e-8 and abs(herald-spectral_herald)<1e-8 and abs(correct-spectral_correct)<1e-8
            probabilities.append({"secret":list(secrets[index]),"herald":herald,"correct_unconditional":correct,
                                  "failed_herald":1-herald,"total_physical_norm":norm})
            output_probabilities.append(np.abs(state[good_out])**2)
        assert spectral_correct<=min(1,math.pi**2*degree**2/(4*G))+1e-9
        optimal = float(np.sum(np.max(output_probabilities,axis=0))/G)
        assert optimal<=min(1,math.pi**2*degree**2/(4*G))+1e-9
        rows.append({"degree":degree,"physical_reflection_rounds":(degree-1)//2,
                     "spectral_correct_unconditional":spectral_correct,"spectral_herald":spectral_herald,
                     "optimal_classical_label_guess_uniform_secret_unconditional":optimal,
                     "heralded_output_probabilities_by_secret":[list(v) for v in output_probabilities],
                     "every_secret_physical_probabilities":probabilities})
    h = Fraction(sum(v*v for v in eta),N*N)
    if degrees[0]==1:
        assert abs(rows[0]["spectral_correct_unconditional"]-1/G)<1e-9
    positive = [v for v in eta if v]
    return {"labels":A,"modulus":q,"fiber_counts":eta,"raw_herald_exact":rational(h),
            "raw_correct_exact":rational(Fraction(1,G)),"raw_conditional_correct_exact":rational(1/(G*h)),
            "supported_singular_value_condition_number_squared":rational(Fraction(max(positive),min(positive))),
            "ideal_PGM_success":sum(math.sqrt(v) for v in eta)**2/(N*G),"physical_controls":rows,
            "bounded_unitary_and_fiber_materialization_is_exponential_calibration":True,
            "known_public_unitary_inverse_used":True,"unknown_input_preparation_inverse_used":False,
            "efficient_native_decoder_implemented":False}


def run_controls():
    physical = [bounded_physical_control(A,q) for A,q in
                (([[2,1]],4),([[0,0]],4),([[1,3,7]],8),([[1,0],[2,1]],4))]
    source = []
    for n,q,m in ((1,4,2),(1,8,3),(2,4,2)):
        total = Fraction(0)
        for flat in itertools.product(range(q),repeat=n*m):
            A = [flat[j*m:(j+1)*m] for j in range(n)]
            _,eta,_ = _data(A,q)
            total += Fraction(sum(v*v for v in eta),4**m)
        mean = total/q**(n*m)
        expected = Fraction(2**m+q**n-1,2**m*q**n)
        assert mean==expected
        source.append({"n":n,"q":q,"m":m,"complete_native_matrices":q**(n*m),
                       "exact_mean_raw_herald":rational(mean),
                       "exact_pooled_conditional_correct":rational(Fraction(1,q**n)/mean),
                       "unconditional_correct":rational(Fraction(1,q**n))})
    return {"status":"SCOPED_QSVT_COMPARISON_ENCODING_FALSIFIER_REVIEW_PENDING",
            "physical_controls":physical,"complete_native_sources":source,
            "native_growing_ledgers":[normalization_certificate(n,4*n+1,n*(4*n+1)+16,(2*n*(4*n+1)+16)**2) for n in (8,16,32)],
            "easy_binary_family_countercontrol":{
                "labels":"identity matrix over F_2", "secret_decoder":"Hadamard on each supplied qubit",
                "direct_correct_probability":1,"comparison_singular_condition_number":1,
                "comparison_singular_values":"2^(-n/2)",
                "general_hidden_subgroup_hardness_inferred":False},
            "claim_gate":{"independent_review":False,"novelty_claim":False,"candidate_record_accepted":False,
                          "speedup_claim_allowed":False,"all_QSVT_or_collective_decoders_ruled_out":False},
            "dependency_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__),ROOT/"theorems/dcp_adaptive_product_readout_bound.py",
                                           ROOT/"theorems/dcp_terminal_affine_fibers.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"complete_source_controls":report["complete_native_sources"],
                      "native_degree_bound_exponents":[r["conservative_correct_probability_dyadic_exponent"] for r in report["native_growing_ledgers"]],
                      "claim_gate":report["claim_gate"]},indent=2))


if __name__=="__main__":
    main()
