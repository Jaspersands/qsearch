"""Certified mod-four linearization and Hensel lifting for binary-error LWE.

LOCAL DERIVATION / REVIEW PENDING. Classical arithmetic component, not a
native Boolean subset-sum finder, general LWE attack or quantum speedup.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_carry_packets import binary_rank
from dcp_conditional_carry_features import _solve
from dcp_terminal_affine_fibers import _positive_integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/native_binary_error_hensel.json"


def _inputs(labels, observations, modulus):
    if type(modulus) is not int or modulus < 4 or modulus & (modulus-1):
        raise ValueError("power-of-two modulus>=4 required")
    A = tuple(tuple(row) for row in labels)
    b = tuple(observations)
    if not A or not A[0] or any(len(row) != len(A[0]) for row in A) or len(b) != len(A[0]):
        raise ValueError("nonempty n-by-m matrix and m observations required")
    if any(type(a) is not int or not 0 <= a < modulus for row in A for a in row) or any(type(v) is not int or not 0 <= v < modulus for v in b):
        raise ValueError("canonical integer labels and observations required")
    return A, b


def feature_dimension(n):
    _positive_integer(n,"dimension")
    return n*(n+3)//2


def parity_feature_word(low_bits, next_bits, n):
    if any(type(x) is not int or not 0 <= x < 1 << n for x in (low_bits,next_bits)):
        raise ValueError("canonical parity and lift bit vectors required")
    word=low_bits | (next_bits << n)
    for j,(u,v) in enumerate(itertools.combinations(range(n),2)):
        word |= ((low_bits>>u&1)*(low_bits>>v&1)) << (2*n+j)
    return word


def lowbit_equation(column, observation):
    n=len(column)
    if not n or any(type(a) is not int for a in column) or type(observation) is not int:
        raise ValueError("integer sample and observation required")
    row=0
    for j,a in enumerate(column):
        numerator=a*(a+1-2*observation)
        assert numerator%2 == 0
        row |= ((numerator//2)&1) << j
        row |= (a&1) << (n+j)
    for j,(u,v) in enumerate(itertools.combinations(range(n),2)):
        row |= (column[u]*column[v]&1) << (2*n+j)
    constant=(observation*(observation-1)//2)&1
    return row,constant


def translated_feature_map(secret_mod_four):
    """Affine feature change x=s+y mod4, including binary addition carries."""
    secret=tuple(secret_mod_four)
    if not secret or any(type(x) is not int or not 0 <= x < 4 for x in secret):
        raise ValueError("canonical mod-four secret vector required for source audit")
    n=len(secret)
    low=sum((s&1)<<j for j,s in enumerate(secret))
    high=sum((s>>1&1)<<j for j,s in enumerate(secret))
    rows=[1<<j for j in range(n)]
    rows += [(1<<(n+j)) | (((low>>j)&1)<<j) for j in range(n)]
    for j,(u,v) in enumerate(itertools.combinations(range(n),2)):
        rows.append((1<<(2*n+j)) | (((low>>u)&1)<<v) | (((low>>v)&1)<<u))
    assert binary_rank(rows,len(rows)) == len(rows)
    return tuple(rows),parity_feature_word(low,high,n)


def decode_binary_error(labels, observations, modulus):
    A,b=_inputs(labels,observations,modulus)
    n,m,L=len(A),len(b),modulus.bit_length()-1
    d=feature_dimension(n)
    columns=tuple(zip(*A))
    equations=[lowbit_equation(a,v) for a,v in zip(columns,b)]
    rank,features=_solve(equations,d)
    B=tuple(sum((a&1)<<j for j,a in enumerate(column)) for column in columns)
    base={"status":"LOWBIT_FEATURE_RANK_DEFICIENT", "dimension":n,"modulus_bits":L,
          "samples":m,"feature_dimension":d,"feature_rank":rank,
          "binary_jacobian_rank":binary_rank(B,n), "secret":None,
          "secret_assignments_or_target_fibers_enumerated":False,
          "native_subset_sum_witness_finder_supplied":False,"speedup_claim_allowed":False}
    if rank<d:
        return base
    if features is None:
        return {**base,"status":"LOWBIT_LINEARIZATION_INCONSISTENT"}
    low=features&((1<<n)-1)
    high=features>>n&((1<<n)-1)
    if parity_feature_word(low,high,n) != features:
        return {**base,"status":"LOWBIT_FEATURE_PRODUCT_CERTIFICATE_FAILED"}
    secret=tuple((low>>j&1)+2*(high>>j&1) for j in range(n))
    assert base["binary_jacobian_rank"] == n
    lift_records=[]
    for bits in range(2,L):
        lifted=[]
        for a,v,row in zip(columns,b,B):
            residual=sum(x*y for x,y in zip(a,secret))-v
            product=residual*(residual+1)
            if product%(1<<bits):
                return {**base,"status":"CURRENT_RESIDUE_NOT_A_BINARY_ERROR_ROOT"}
            lifted.append((row,(product>>bits)&1))
        lift_rank,update=_solve(lifted,n)
        if update is None:
            return {**base,"status":"HENSEL_LIFT_INCONSISTENT","failed_lift_bit":bits}
        assert lift_rank == n
        secret=tuple(s+((update>>j&1)<<bits) for j,s in enumerate(secret))
        lift_records.append({"resolved_modulus_bits":bits+1,"linear_rank":lift_rank,"update_bits":update})
    errors=tuple((v-sum(a*s for a,s in zip(column,secret)))%modulus for column,v in zip(columns,b))
    if any(e not in (0,1) for e in errors):
        return {**base,"status":"FINAL_BINARY_ERROR_VERIFICATION_FAILED"}
    return {**base,"status":"CERTIFIED_UNIQUE_BINARY_ERROR_SECRET", "secret":secret,
            "verified_errors":errors,"initial_secret_mod_four":tuple(s%4 for s in secret),
            "feature_solution_bits_hex":hex(features),"initial_equations_hex":[(hex(row),rhs) for row,rhs in equations],
            "hensel_lifts":lift_records,"all_binary_error_roots_share_this_secret":True,
            "field_inverse_or_exponential_secret_search_required":False}


def pointwise_rank_source_certificate(n,samples,modulus_bits):
    for value,name in ((n,"dimension"),(samples,"sample count"),(modulus_bits,"modulus bits")):
        _positive_integer(value,name)
    if modulus_bits<2:
        raise ValueError("modulus>=4 required")
    d=feature_dimension(n)
    exponent=max(0,2*(samples//5)-d)
    return {"status":"LOCAL_POINTWISE_CLASSICAL_BINARY_ERROR_DECODER_THEOREM_REVIEW_PENDING",
            "dimension":n,"samples":samples,"modulus_bits":modulus_bits,"feature_dimension":d,
            "per_nonzero_feature_function_zero_probability_upper_bound":exact(Fraction(3,4)),
            "rank_failure_union_bound":"min(1,(2^d-1)*(3/4)^m)",
            "conservative_rank_failure_dyadic_exponent":exponent,
            "same_decoder_for_each_fixed_secret_and_arbitrary_fixed_binary_error_vector":True,
            "probability_over_IID_native_label_matrix_only":True,
            "label_dependent_error_vector_allowed":False,
            "sample_error_independence_or_uniformity_required":False,
            "coefficient_matrix_is_an_IID_unstructured_d_bit_matrix":False,
            "native_low_two_bits_prove_the_entire_success_event":True,
            "remaining_secret_bits_recovered_by_unique_linear_hensel_lifts":True,
            "Gaussian_bit_operation_upper_bound_order":"O(m*d^2 + L*m*n^2), with input integer arithmetic charged polynomially",
            "storage_upper_bound_order":"O(d^2 + m*n*L) bits plus polynomial integer workspace",
            "native_boolean_subset_sum_or_general_LWE_solved":False,
            "novelty_claim":False,"candidate_record_accepted":False,"speedup_claim_allowed":False}


def _coefficient_and_translation_controls():
    evaluations=translations=0
    for n in (1,2,3):
        for a in itertools.product(range(4),repeat=n):
            for b in range(4):
                row,rhs=lowbit_equation(a,b)
                for low,high in itertools.product(range(1<<n),repeat=2):
                    x=tuple((low>>j&1)+2*(high>>j&1) for j in range(n))
                    z=sum(t*u for t,u in zip(a,x))-b
                    assert ((row&parity_feature_word(low,high,n)).bit_count()%2)^rhs == (z*(z+1)//2)&1
                    evaluations+=1
        rng=random.Random(800+n)
        for _ in range(256):
            a=tuple(rng.randrange(4) for _ in range(n))
            secret=tuple(rng.randrange(4) for _ in range(n))
            error=rng.randrange(2)
            b=(sum(x*y for x,y in zip(a,secret))+error)%4
            row,rhs=lowbit_equation(a,b)
            T,c=translated_feature_map(secret)
            translated=0
            for j,t in enumerate(T):
                if row>>j&1:
                    translated^=t
            expected=sum((((a[j]>>1)^((a[j]&1)*(1-error)))&1)<<j for j in range(n))
            expected|=sum((a[j]&1)<<(n+j) for j in range(n))
            expected|=sum((a[u]*a[v]&1)<<(2*n+j) for j,(u,v) in enumerate(itertools.combinations(range(n),2)))
            assert translated == expected
            assert rhs == (row&c).bit_count()%2
            translations+=1
    return {"complete_mod_four_polynomial_evaluations":evaluations,"secret_error_affine_feature_source_translations":translations}


def _row_function_controls():
    records=[]
    for n in (1,2,3):
        d=feature_dimension(n)
        rows=[lowbit_equation(a,0)[0] for a in itertools.product(range(4),repeat=n)]
        minimum=min(sum((row&mask).bit_count()%2 for row in rows) for mask in range(1,1<<d))
        assert Fraction(minimum,len(rows))>=Fraction(1,4)
        records.append({"dimension":n,"feature_dimension":d,"complete_native_low_label_rows":len(rows),
                        "all_nonzero_feature_functions":(1<<d)-1,"minimum_nonzero_row_function_mass":exact(Fraction(minimum,len(rows)))})
    return records


def _pointwise_small_source_control():
    source_tables=[tuple(a) for a in itertools.product(range(4),repeat=3)]
    histograms=[]
    for secret in range(4):
        for errors in itertools.product(range(2),repeat=3):
            histogram=Counter()
            for a in source_tables:
                b=tuple((x*secret+e)%4 for x,e in zip(a,errors))
                result=decode_binary_error((a,),b,4)
                histogram[result["feature_rank"]]+=1
                if result["secret"] is not None:
                    assert result["secret"] == (secret,)
            histograms.append(dict(histogram))
    assert all(h == histograms[0] for h in histograms)
    assert histograms[0][2] == 42
    return {"dimension":1,"modulus":4,"samples":3,"all_native_label_tables":64,
            "every_fixed_secret_and_error_law_controls":len(histograms),"common_rank_histogram":histograms[0],
            "exact_pointwise_success_probability":exact(Fraction(42,64)),"measured_large_n_success_theorem":False}


def run_controls():
    rng=random.Random(20261005)
    trials=[]
    for n,L in ((2,5),(4,17),(8,33),(16,65)):
        m=3*feature_dimension(n)
        q=1<<L
        A=tuple(tuple(rng.randrange(q) for _ in range(m)) for _ in range(n))
        secret=tuple(rng.randrange(q) for _ in range(n))
        errors=tuple((i%3)==0 for i in range(m))
        b=tuple((sum(A[j][i]*secret[j] for j in range(n))+int(errors[i]))%q for i in range(m))
        decoded=decode_binary_error(A,b,q)
        if decoded["secret"] is not None:
            assert decoded["secret"] == secret
        trials.append({"dimension":n,"modulus_bits":L,"samples":m,
                       "native_labels_hex":[[hex(a) for a in row] for row in A],
                       "observations_hex":[hex(v) for v in b],
                       "expected_planted_secret_hex":[hex(s) for s in secret],
                       "result_status":decoded["status"],"feature_rank":decoded["feature_rank"],
                       "successful_unique_linear_lifts":len(decoded.get("hensel_lifts",())),
                       "planted_secret_recovered":decoded["secret"]==secret,
                       "finite_source_trials_prove_asymptotic_success":False,
                       "pointwise_source_certificate":pointwise_rank_source_certificate(n,m,L)})
    return {"status":"LOCAL_DERIVATION_REVIEW_PENDING",
            "polynomial_and_translation_controls":_coefficient_and_translation_controls(),
            "complete_native_row_function_controls":_row_function_controls(),
            "complete_pointwise_small_source_control":_pointwise_small_source_control(),
            "actual_growing_modulus_decoder_trials":trials,
            "claim_gate":{"classical_binary_error_decoder_implemented":True,
                          "works_polynomially_in_input_modulus_bit_length_not_modulus_value":True,
                          "pointwise_native_source_theorem_independently_reviewed":False,
                          "native_subset_sum_to_binary_error_source_bridge_supplied":False,
                          "general_LWE_or_lattice_cryptography_broken":False,
                          "quantum_speedup_discovered":False,"candidate_record_accepted":False,"novelty_claim":False},
            "dependency_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__),ROOT/"theorems/dcp_conditional_carry_features.py",ROOT/"theorems/dcp_carry_packets.py")}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args=parser.parse_args()
    report=run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"claim_gate":report["claim_gate"],
                      "growing_modulus_trials":[(r["dimension"],r["planted_secret_recovered"]) for r in report["actual_growing_modulus_decoder_trials"]]},indent=2))


if __name__ == "__main__":
    main()
