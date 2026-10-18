"""Paid native-fiber enumeration and exact witnesses to weighted moment bounds.

Nonnegative real weights suffice for the fourth-moment supremum, but power
iteration does NOT certify its global maximum or supply an informative POVM.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import comb, factorial, log2
from pathlib import Path
from random import Random
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_nonlinear_fiber_pairing import phase_value

REPORT = ROOT/"research/phase_workbench/dcp_weighted_fiber_moment_search.json"


def paid_fiber(labels, phase_bits, syndrome, *, half_table_cap=131072, fiber_cap=1400):
    A = matrix(labels)
    n,m = len(A),len(A[0])
    integer(phase_bits,"native original phase bits",3,64)
    if n > 16 or m > 34 or any(a >= 1 << phase_bits for row in A for a in row):
        raise ValueError("UNKNOWN: supported native full-label calibration range")
    y = tuple(syndrome)
    if len(y) != n:
        raise ValueError("one mod4 syndrome component per row required")
    for v in y:
        integer(v,"mod4 syndrome",0,3)
    integer(half_table_cap,"paid half-table entry cap",1,1 << 20)
    integer(fiber_cap,"paid explicit fiber cap",1,1400)
    split = m//2
    sizes = (1 << split,1 << (m-split))
    if max(sizes) > half_table_cap:
        raise ValueError("UNKNOWN: paid meet-in-middle half-table cap; no polynomial fiber oracle")
    # Three bits per mod4 coordinate prevent inter-component addition carries.
    mask = sum(3 << (3*l) for l in range(n))
    columns = [sum((A[l][i]%4) << (3*l) for l in range(n)) for i in range(m)]
    target = sum(v << (3*l) for l,v in enumerate(y))
    tables = []
    for lo,size in ((0,sizes[0]),(split,sizes[1])):
        values = [0]*size
        for x in range(1,size):
            bit = x & -x
            values[x] = (values[x^bit]+columns[lo+bit.bit_length()-1])&mask
        tables.append(values)
    left = {}
    for x,value in enumerate(tables[0]):
        left.setdefault(value,[]).append(x)
    fiber = []
    for z,value in enumerate(tables[1]):
        wanted = sum((((target >> (3*l)&3)-(value >> (3*l)&3))%4) << (3*l) for l in range(n))
        matches = left.get(wanted,())
        if len(fiber)+len(matches) > fiber_cap:
            raise ValueError("UNKNOWN: explicit fiber output cap; result is not truncated")
        fiber.extend(x | (z << split) for x in matches)
    if not fiber:
        raise ValueError("zero-probability syndrome")
    fiber.sort()
    return fiber,{"method":"complete meet-in-middle Boolean mod4 fiber enumeration",
                  "half_table_entries":list(sizes),"public_column_coordinate_additions":n*(sum(sizes)-2),
                  "target_coordinate_subtractions":n*sizes[1],
                  "matching_assignments_materialized":len(fiber),
                  "Born_syndrome_probability_exact":str(Fraction(len(fiber),1 << m)),
                  "classical_calibration_not_quantum_preparation":True,
                  "polynomial_time_in_n_claimed":False,
                  "output_or_source_success_probability_renormalized":False}


def pair_buckets(labels,phase_bits,fiber):
    A = matrix(labels)
    n = len(A)
    integer(phase_bits,"full frequency phase bits",3,64)
    D = len(fiber)
    if (not D or D > 1400 or len(set(fiber)) != D or
        any(type(x) is not int or not 0 <= x < 1 << len(A[0]) for x in fiber)):
        raise ValueError("distinct explicit fiber assignments within charged cap required")
    q = 1 << phase_bits
    # Actual full frequencies, not a replacement by integer parallelograms.
    fs = [phase_value(A,x,q) for x in fiber]
    if len(set(fs)) != D:
        raise ValueError("noninjective full frequencies: uniform-ensemble premise fails")
    packed = [sum(v << ((phase_bits+1)*l) for l,v in enumerate(f)) for f in fs]
    mask = sum((q-1) << ((phase_bits+1)*l) for l in range(n))
    lookup,counts = {},[]
    ids = np.empty((D,D),dtype=np.int32)
    for i,a in enumerate(packed):
        for j,b in enumerate(packed):
            key = (a+b)&mask
            idx = lookup.get(key)
            if idx is None:
                idx = len(lookup)
                lookup[key] = idx
                counts.append(0)
            ids[i,j] = idx
            counts[idx] += 1
    return ids,np.array(counts,dtype=np.int64)


def exact_witness(ids,weights):
    D = len(ids)
    if ids.shape != (D,D) or not D or not np.array_equal(ids,ids.T):
        raise ValueError("symmetric complete ordered-pair buckets required")
    if len(weights) != D or any(type(w) is not int or not 0 <= w <= 4096 for w in weights) or not any(weights):
        raise ValueError("nonzero bounded integer nonnegative weights required")
    # A strict integer overflow bound makes this an EXACT witness, not a float fit.
    if D*D*max(weights)**2 >= 1 << 62:
        raise ValueError("exact integer accumulation cap exceeded")
    w = np.array(weights,dtype=np.int64)
    sums = np.zeros(int(ids.max())+1,dtype=np.int64)
    np.add.at(sums,ids.ravel(),np.outer(w,w).ravel())
    norm2 = sum(a*a for a in weights)
    moment = Fraction(sum(int(s)**2 for s in sums),norm2**2)
    completion_mass = Fraction(norm2,D*max(weights)**2)
    return {"integer_weights":list(weights),"weight_normalization_squared":norm2,
            "fourth_moment_exact":str(moment),
            "covariant_single_seed_completion_mass_exact":str(completion_mass),
            "completed_single_seed_information_upper_bits":float(completion_mass)*log2(float(moment)),
            "this_upper_bound_covers_all_measurements":False,
            "large_moment_is_a_mutual_information_lower_bound":False,
            "global_optimality_proved":False}


def local_search(ids, *, seed=0, restarts=4, steps=40):
    D = len(ids)
    integer(restarts,"bounded restarts",1,16)
    integer(steps,"bounded power steps",1,200)
    rng = np.random.default_rng(seed)
    traces = []
    best = exact_witness(ids,[1]*D)
    best_value = Fraction(best["fourth_moment_exact"])
    for start in range(restarts):
        w = np.ones(D) if start == 0 else rng.exponential(1,size=D)
        if start == restarts-1 and restarts > 2:
            w[rng.random(D)>min(1,8/D)] = 0
            if not np.any(w):
                w[0] = 1
        w /= np.linalg.norm(w)
        history = []
        for _ in range(steps):
            sums = np.bincount(ids.ravel(),weights=np.outer(w,w).ravel())
            value = float(sums@sums)
            if history and value < history[-1]-1e-10:
                raise ArithmeticError("convex fourth-moment power step decreased objective")
            history.append(value)
            gradient = sums[ids]@w
            next_w = gradient/np.linalg.norm(gradient)
            if np.linalg.norm(next_w-w) < 1e-9:
                break
            w = next_w
        # Retain only a rationally replayed result; floats never falsify a bound.
        weights = [int(v) for v in np.rint(4096*w/max(w))]
        for integer_weights in (weights,*([int(v > threshold*max(weights)) for v in weights]
                                          for threshold in (0.25,0.5,0.75))):
            candidate = exact_witness(ids,integer_weights)
            if Fraction(candidate["fourth_moment_exact"]) > best_value:
                best,best_value = candidate,Fraction(candidate["fourth_moment_exact"])
        traces.append({"start":start,"iterations":len(history),"objective_first":history[0],
                       "objective_last":history[-1],"monotonicity_checked":True})
    return best,traces


def support_structure(fiber,witness):
    S = {x for x,w in zip(fiber,witness["integer_weights"]) if w}
    original_size = len(S)
    factors = []
    while len(S)>1:
        anchor = min(S)
        d = next((d for d in sorted((x^anchor for x in S if x != anchor),key=lambda x:(x.bit_count(),x))
                  if {x^d for x in S} == S and len({x&d for x in S}) == 2),None)
        if d is None:
            break
        factors.append({"disjoint_physical_direction_hex":hex(d),
                        "two_inside_patterns_hex":[hex(x) for x in sorted({x&d for x in S})]})
        S = {x & ~d for x in S}
    buckets = {}
    for a in S:
        for b in S:
            key = (a^b,a&b)  # Integer coordinate sums, not arithmetic modulo a packed binary word.
            buckets[key] = buckets.get(key,0)+1
    histogram = {str(v):list(buckets.values()).count(v) for v in sorted(set(buckets.values()))}
    if len(S) == 1:
        motif = "Cartesian disjoint-flip Boolean cube"
    elif len(S) == 6 and histogram == {"1":6,"2":12,"6":1}:
        motif = "Cartesian edges times six vertices in three common-sum antipodal pairs"
    else:
        motif = "unclassified residual support; no structural conclusion"
    return {"nonzero_weight_support":original_size,"disjoint_edge_factors":factors,
            "residual_support_hex":[hex(x) for x in sorted(S)],
            "residual_integer_pair_sum_multiplicity_histogram":histogram,"motif":motif,
            "support_geometry_is_a_complete_POVM_or_decoder":False}


def native_cube_count(n,m,d):
    """Exact first moment for a full disjoint-flip d-cube in the actual Born fiber."""
    integer(n,"native components",1,4096)
    integer(m,"original Boolean width",1,16384)
    integer(d,"disjoint-flip cube dimension",1,min(m,64))
    if m*(d+1).bit_length()+2*n*(d+1)>12000:
        raise ValueError("UNKNOWN: exact decimal cube-certificate export cap")
    # Each physical coordinate is constant or belongs to exactly one direction.
    # All d direction blocks must be nonempty. Quotient origin and ordering.
    onto = sum((-1)**j*comb(d,j)*(d+1-j)**m for j in range(d+1))
    numerator = (1 << (m-d))*onto
    cube_count,remainder = divmod(numerator,factorial(d))
    if remainder:
        raise ArithmeticError("nonintegral distinct physical-cube count")
    G,M = 1 << (2*n),1 << m
    all_fibers_expected = Fraction(cube_count,G**d)
    in_cube = Fraction(1 << d,M)
    born_expected = cube_count*(in_cube/Fraction(G**d)+(1-in_cube)/Fraction(G**(d+1)))
    return {"components":n,"physical_width":m,"cube_dimension":d,
            "distinct_unordered_physical_cubes":str(cube_count),
            "expected_cubes_over_all_fibers_exact":str(all_fibers_expected),
            "expected_cubes_in_Born_sampled_fiber_exact":str(born_expected),
            "probability_any_cube_in_Born_fiber_upper_exact":str(min(Fraction(1),born_expected)),
            "Born_measure_is_not_uniform_syndrome_measure":True,
            "covers_source_adaptive_search_for_disjoint_flip_cube":True,
            "covers_arbitrary_weights_or_all_high_moment_motifs":False,
            "general_quantum_measurement_no_go":False}


def evaluate_native(n,seed,*,restarts=4,steps=40):
    integer(n,"native component dimension",2,10)
    rng = Random(seed)
    m,t = 3*n,n+8
    A = tuple(tuple(rng.randrange(1 << t) for _ in range(m)) for _ in range(n))
    original_x = rng.randrange(1 << m)
    y = phase_value(A,original_x,4)
    F,receipt = paid_fiber(A,t,y)
    ids,counts = pair_buckets(A,t,F)
    witness,traces = local_search(ids,seed=seed,restarts=restarts,steps=steps)
    uniform = Fraction(sum(int(v)**2 for v in counts),len(F)**2)
    found = Fraction(witness["fourth_moment_exact"])
    upper = int(counts.max())
    if not uniform <= found <= upper:
        raise ArithmeticError("exact witness outside certified pair-multiplicity interval")
    return {"components":n,"original_phase_bits":t,"physical_width":m,"seed":seed,
            "full_labels":[list(r) for r in A],"measured_syndrome":list(y),
            "original_uniform_assignment_used_for_Born_syndrome_calibration":original_x,
            "actual_quantum_measurements_executed":0,
            "syndrome_selected_by_searching_for_a_large_moment":False,
            "fiber_assignments_hex":[hex(x) for x in F],"paid_fiber_receipt":receipt,
            "ordered_pairs_materialized":len(F)**2,"pair_sum_buckets":len(counts),
            "uniform_weight_moment_exact":str(uniform),"fourth_moment_supremum_lower_exact":str(found),
            "fourth_moment_supremum_upper_from_pair_multiplicity":upper,
            "exact_witness":witness,"local_search_traces":traces,
            "exact_weight_support_structure":support_structure(F,witness),
            "quantitative_cap_tests":[{"cap":cap,"falsified_by_exact_selected_witness":found>cap}
                                      for cap in (2,4,8,n*n)],
            "no_witness_found_proves_native_bound":False,
            "native_high_probability_or_asymptotic_statement_proved":False,
            "efficient_secret_decoder_or_POVM_compiler":False}


def build_report():
    cases = [evaluate_native(n,seed=101719+100*n) for n in (2,3,4,6,8,10)]
    return {"status":"EXACT_NATIVE_WEIGHTED_MOMENT_WITNESSES_NO_ASYMPTOTIC_CLAIM",
            "cases":cases,"native_label_law":"IID uniform original Z_(2^(n+8)) entries",
            "native_Born_cube_counts":[native_cube_count(n,w*n,d)
                                      for w,d in ((3,4),(4,7)) for n in (8,32,128)],
            "Born_syndrome_law":"draw original uniform Boolean x, then y=A*x mod4",
            "selection_bias":"fixed declared n/seed schedule; no source rejection or favorable-syndrome search",
            "moment_supremum_can_be_restricted_to_nonnegative_weights":True,
            "random_restarts_certify_global_optimality":False,
            "accepted_speedup_candidate":False,"new_active_negative_result_created":False,
            "novelty_claim":False,"actual_natural_source_noise_certified":False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"cases":len(report["cases"]),
                      "bounds":[{"n":c["components"],"D":len(c["fiber_assignments_hex"]),
                                  "moment_lower":float(Fraction(c["fourth_moment_supremum_lower_exact"])),
                                  "moment_upper":c["fourth_moment_supremum_upper_from_pair_multiplicity"]}
                                 for c in report["cases"]]}))


if __name__ == "__main__":
    main()
