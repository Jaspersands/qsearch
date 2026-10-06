"""Fixed-order, outcome-adaptive native phase-readout collision audit.

LOCAL DERIVATION / REVIEW PENDING. This is a source-mean measurement-class
bound and exponentially bounded instrument calibration, not a native decoder.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

from dcp_native_product_readout_bound import _povm, projective_povm
from dcp_terminal_affine_fibers import _positive_integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/dcp_adaptive_product_readout_bound.json"


def rational(x):
    return {"numerator_hex":format(x.numerator,"x"),"denominator_hex":format(x.denominator,"x")}


def coefficient_weight(delta):
    if any(type(v) is not int or v not in range(-2,3) for v in delta):
        raise ValueError("squared phase likelihood frequencies must lie in {-2,-1,0,1,2}")
    nonzero = [v for v in delta if v]
    if nonzero and abs(nonzero[-1])==1:
        return Fraction(0)
    return math.prod(Fraction(3,2) if v==0 else Fraction(1) if abs(v)==1 else Fraction(1,4) for v in delta)


def source_certificate(n,L,m):
    for value,name in ((n,"dimension"),(L,"modulus bits"),(m,"qubits")):
        _positive_integer(value,name)
    G,H = 1 << (n*L),1 << (n*(L-1))
    zero = Fraction(3,2)**m
    even = 2**m-zero
    odd = (4**m+4*zero)/5-2**m
    assert odd>=0
    nonadaptive = zero/G+even/(G*H)
    adaptive = nonadaptive+odd/(G*G)
    mu = Fraction(2**m,G)
    second_moment = mu*mu+mu*(1-Fraction(1,G))
    collective_lower = mu*mu/second_moment
    return {"status":"FIXED_ORDER_ADAPTIVE_NATIVE_SOURCE_CONVERSE_REVIEW_PENDING",
            "dimension":n,"modulus_bits":L,"phase_qubits":m,"density_surplus":m-n*L,
            "zero_character_weight":rational(zero),"nonzero_even_character_weight":rational(even),
            "feedback_odd_character_weight":rational(odd),
            "unclamped_source_mean_success_squared_envelope":rational(adaptive),
            "source_mean_success_squared_upper_bound":rational(min(Fraction(1),adaptive)),
            "also_bounds_mean_of_squared_conditional_uniform_secret_success":True,
            "nonadaptive_source_mean_success_squared_upper_bound":rational(min(Fraction(1),nonadaptive)),
            "bound_is_vacuous":adaptive>=1,
            "uniform_target_fiber_mean":rational(mu),
            "uniform_target_fiber_second_moment":rational(second_moment),
            "collective_PGM_source_mean_success_lower_bound":rational(collective_lower),
            "collective_lower_exceeds_adaptive_upper":collective_lower**2>adaptive,
            "collective_PGM_efficient_implementation_supplied":False,
            "all_public_labels_may_choose_each_axis_and_effect":True,
            "previous_classical_outcomes_may_choose_future_POVMs":True,
            "arbitrary_POVMs_covered_by_equatorial_rank_one_refinement":True,
            "measurement_order_fixed_independently_of_labels_and_outcomes":True,
            "label_adaptive_ordering_revisiting_or_quantum_memory_covered":False,
            "additional_samples_or_collective_measurements_ruled_out":False,
            "claim_is_pointwise_in_secret_or_public_matrix":False,
            "efficient_adaptive_decoder_supplied":False,
            "candidate_record_accepted":False,"novelty_claim":False,"speedup_claim_allowed":False}


def refine_equatorial(outcomes):
    rows = _povm(outcomes)
    refined,mapping = [],[]
    for index,(w,rx,ry,_) in enumerate(rows):
        radius = math.hypot(rx,ry)
        unit = (rx/radius,ry/radius) if radius else (1.0,0.0)
        radius = min(1.0,radius)
        for sign in (1,-1):
            weight = w*(1+sign*radius)/2
            if weight>0:
                refined.append((weight,sign*unit[0],sign*unit[1],0.0))
                mapping.append(index)
    return _povm(refined),mapping


def _tree(A,policy,refined):
    m = len(A[0])
    leaves = [((),1.0,())]
    for _ in range(m):
        next_leaves = []
        for history,Q,effects in leaves:
            original = _povm(policy(A,history))
            rows,mapping = refine_equatorial(original) if refined else (original,list(range(len(original))))
            for effect,coarse in zip(rows,mapping):
                next_leaves.append((history+(coarse,),Q*effect[0],effects+(effect,)))
        if len(next_leaves)>100000:
            raise ValueError("bounded calibration leaf cap exceeded; not an efficient instrument compiler")
        leaves = next_leaves
    assert abs(sum(Q for _,Q,_ in leaves)-1)<1e-9
    return leaves


def bounded_control(A,q,policy):
    _positive_integer(q,"modulus")
    if not isinstance(A,(list,tuple)) or not A or not isinstance(A[0],(list,tuple)) or not A[0]:
        raise ValueError("nonempty rectangular native label matrix required")
    n,m = len(A),len(A[0])
    if not n or not m or m>4 or q**n>1024 or q<2 or q&(q-1):
        raise ValueError("bounded native power-two source calibration requires m<=4, G<=1024")
    if any(not isinstance(row,(list,tuple)) or len(row)!=m or any(type(v) is not int or not 0<=v<q for v in row) for row in A):
        raise ValueError("canonical rectangular native label matrix required")
    secrets = list(itertools.product(range(q),repeat=n))
    theta = [[2*math.pi*(sum(A[j][i]*s[j] for j in range(n)) % q)/q for i in range(m)] for s in secrets]
    evaluations = []
    for refined in (False,True):
        leaves = _tree(A,policy,refined)
        success,collision = 0.0,0.0
        coefficients = {}
        for _,Q,effects in leaves:
            likelihood = [math.prod(1+r[1]*math.cos(t)+r[2]*math.sin(t) for r,t in zip(effects,angles)) for angles in theta]
            success += Q*max(likelihood)/len(secrets)
            collision += Q*sum(v*v for v in likelihood)/len(secrets)
            if refined:
                local = []
                for r in effects:
                    a = complex(r[1],-r[2])
                    local.append({0:1.5,1:a,-1:a.conjugate(),2:a*a/4,-2:a.conjugate()**2/4})
                for delta in itertools.product(range(-2,3),repeat=m):
                    coefficients[delta] = coefficients.get(delta,0j)+Q*math.prod(local[i][v] for i,v in enumerate(delta))
        evaluations.append({"refined":refined,"optimal_classical_record_success":success,"weighted_collision":collision,"tree_leaves":len(leaves),
                            "leaf_reference_probabilities_and_effects":[{"coarse_history":list(h),"reference_probability":Q,
                                                                       "effects":[list(e) for e in es]} for h,Q,es in leaves]})
    envelope = Fraction(0)
    orthogonality = 0j
    for delta,coefficient in coefficients.items():
        assert abs(coefficient)<=float(coefficient_weight(delta))+1e-8
        if all(sum(row[i]*delta[i] for i in range(m)) % q==0 for row in A):
            orthogonality += coefficient
            envelope += coefficient_weight(delta)
    assert abs(orthogonality-evaluations[1]["weighted_collision"])<1e-8
    assert evaluations[0]["optimal_classical_record_success"]<=evaluations[1]["optimal_classical_record_success"]+1e-9
    assert evaluations[0]["weighted_collision"]<=evaluations[1]["weighted_collision"]+1e-8
    assert evaluations[1]["weighted_collision"]<=float(envelope)+1e-8
    assert evaluations[1]["optimal_classical_record_success"]**2<=float(envelope)/q**n+1e-9
    return {"labels":A,"modulus":q,"evaluations":evaluations,"fixed_matrix_refined_collision_envelope":rational(envelope),
            "refined_fourier_coefficients":[{"delta":list(delta),"real":value.real,"imaginary":value.imag} for delta,value in coefficients.items()],
            "bounded_secret_and_tree_enumeration_is_exponential_calibration":True,"efficient_decoder_claim":False}


def _fiber_control(A,q):
    n,m = len(A),len(A[0])
    counts = {t:0 for t in itertools.product(range(q),repeat=n)}
    for x in itertools.product((0,1),repeat=m):
        t = tuple(sum(v*b for v,b in zip(row,x)) % q for row in A)
        counts[t] += 1
    G,N = q**n,2**m
    return Fraction(N,G),Fraction(sum(v*v for v in counts.values()),G),sum(math.sqrt(v) for v in counts.values())**2/(N*G)


def parity_policy(A,history):
    return projective_povm(math.pi/2 if history and history[0] else 0)


def general_policy(A,history):
    axis = 2*math.pi*(sum(A[0])+sum(history))/4
    return [(0.5,0.6*math.cos(axis),0.6*math.sin(axis),0.2),
            (0.5,-0.6*math.cos(axis),-0.6*math.sin(axis),-0.2)]


def run_controls():
    actual = [bounded_control([[2,1]],4,parity_policy),bounded_control([[1,3,7]],8,general_policy),
              bounded_control([[1,0,3],[2,1,2]],4,general_policy)]
    assert abs(actual[0]["evaluations"][0]["optimal_classical_record_success"]-1)<1e-9
    source = []
    for n,q,m in ((1,4,2),(1,8,3),(2,4,2)):
        total = Fraction(0)
        first,second,pgm = Fraction(0),Fraction(0),0.0
        for entries in itertools.product(range(q),repeat=n*m):
            A = [entries[j*m:(j+1)*m] for j in range(n)]
            f1,f2,p = _fiber_control(A,q)
            first += f1
            second += f2
            pgm += p/q**(n*m)
            for delta in itertools.product(range(-2,3),repeat=m):
                if all(sum(row[i]*delta[i] for i in range(m)) % q==0 for row in A):
                    total += coefficient_weight(delta)
        average = total/q**(n*m)
        certificate = source_certificate(n,q.bit_length()-1,m)
        bound = certificate["unclamped_source_mean_success_squared_envelope"]
        assert average/q**n==Fraction(int(bound["numerator_hex"],16),int(bound["denominator_hex"],16))
        mu = Fraction(2**m,q**n)
        moment = mu*mu+mu*(1-Fraction(1,q**n))
        assert first/q**(n*m)==mu and second/q**(n*m)==moment
        lower = mu*mu/moment
        assert pgm>=float(lower)-1e-9
        source.append({"n":n,"q":q,"m":m,"complete_label_matrices":q**(n*m),"exact_mean_collision_envelope":rational(average),
                       "exact_mean_uniform_target_fiber_count":rational(mu),"exact_mean_uniform_target_fiber_second_moment":rational(moment),
                       "actual_source_mean_collective_PGM_success":pgm,"collective_PGM_mean_success_lower_bound":rational(lower),
                       "fiber_enumeration_not_efficient_measurement_implementation":True})
    return {"status":"ADAPTIVE_FIXED_ORDER_SOURCE_BOUND_WEAK_WITH_SAMPLE_SURPLUS_REVIEW_PENDING",
            "actual_instrument_controls":actual,"complete_source_envelopes":source,
            "growing_ledgers":[source_certificate(n,4*n+1,n*(4*n+1)+delta) for n in (8,16,32) for delta in (0,1,2,16)],
            "claim_gate":{"arbitrary_feedback_impossibility":False,"independent_review":False,
                          "efficient_adaptive_decoder":False,"candidate_record_accepted":False,"novelty_claim":False,"speedup_claim_allowed":False},
            "dependency_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__),ROOT/"theorems/dcp_native_product_readout_bound.py",ROOT/"theorems/dcp_terminal_affine_fibers.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"source_controls":report["complete_source_envelopes"],
                      "vacuous_growing_ledgers":sum(r["bound_is_vacuous"] for r in report["growing_ledgers"]),"claim_gate":report["claim_gate"]},indent=2))


if __name__=="__main__":
    main()
