"""Exact native graph-kernel quaternion encodings and scoped metric/source gates.

LOCAL DERIVATION / REVIEW PENDING. No quaternion PIP solver, fast witness
generator, native RLWE attack, independent theorem review or novelty claim.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

import sympy as sp

from structured_edcp_upstream_mixing import negacyclic_mul

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/native_rlwe_quaternion_kernel.json"
NATIVE = ROOT / "research/certificates/native_rlwe_babai_profile_d64.json"
PARAMETERS = ROOT / "research/certificates/native_rlwe_single_witness_d12_arithmetic.json"


def conjugate(a):
    return (a[0], *(-v for v in reversed(a[1:])))


def mul(a,b):
    return tuple(negacyclic_mul(a,b))


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def scale(a,k):
    return tuple(k*v for v in a)


def multiplication_matrix(a):
    d = len(a)
    return sp.Matrix([[a[(i-j) % d]*(1 if i>=j else -1) for j in range(d)] for i in range(d)])


def _input(ratio,q):
    a = tuple(ratio)
    d = len(a)
    if d<2 or d&(d-1) or type(q) is not int or q<3 or not q%2:
        raise ValueError("power-two ring degree>=2 and odd modulus>=3 required")
    if any(type(v) is not int or not 0<=v<q for v in a):
        raise ValueError("canonical public ratio coefficients required")
    return a,d


def quaternion_multiply(x,y,rho):
    """(g+f*j)(h+k*j), with j*a=bar(a)*j and j^2=-rho."""
    g,f = x
    h,k = y
    if conjugate(rho)!=tuple(rho):
        raise ValueError("quaternion parameter must be conjugation-fixed")
    return (add(mul(g,h),scale(mul(rho,mul(f,conjugate(k))),-1)),
            add(mul(g,k),mul(f,conjugate(h))))


def reduced_norm(x,rho):
    g,f = x
    return add(mul(g,conjugate(g)),mul(rho,mul(f,conjugate(f))))


def kernel_member(x,ratio,q):
    g,f = x
    return all((a-b) % q==0 for a,b in zip(g,mul(ratio,f)))


def quaternion_source_gate(d,q):
    """Conditional exact source law: q prime, q=3 mod8, d>=4 power of two."""
    if type(d) is not int or d<4 or d&(d-1) or type(q) is not int or q<3 or q%8!=3:
        raise ValueError("high-CRT d>=4 power-two and q=3 mod8 required")
    h = d//2
    field_size = q**h
    # Norm(a,b)=a*b in the conjugation-swapped CRT pair: a uniform real
    # residue with weight 1-1/|E|, plus extra zero mass 1/|E|.
    mu2 = Fraction(q*q-1,12)
    mu4 = Fraction((q*q-1)*(3*q*q-7),240)
    mean = (d-1)*mu2
    variance = (2*d-3)*(mu4-mu2*mu2)
    alpha = Fraction(field_size-1,field_size)
    lower = alpha*max(Fraction(0),1-4*variance/(mean*mean))
    threshold = mean/2
    fraction = lambda x: {"numerator":str(x.numerator),"denominator":str(x.denominator)}
    return {"dimension":d, "modulus":str(q), "residue_degree":h,
            "assumption": "q has an independently verified prime certificate",
            "all_native_ratio_count_hex":format(field_size**2,"x"),
            "original_metric_compatible_ratio_count_hex":format(field_size-1,"x"),
            "exact_full_source_probability": {"numerator_hex":format(field_size-1,"x"),
                                              "denominator_hex":format(field_size**2,"x")},
            "conditional_on_unit_ratio_probability": {"numerator_hex":"1", "denominator_hex":format(field_size-1,"x")},
            "full_source_probability_upper_bound_dyadic_exponent":field_size.bit_length()-1,
            "unavoidable_positive_lift_metric_distortion": {
                "scope":"Every real totally positive rho=-M*bar(M) mod q, with the original graph coordinates and norm diag(I,C_rho)",
                "real_residue_uniform_mixture_weight": {"numerator_hex":format(field_size-1,"x"),"denominator_hex":format(field_size,"x")},
                "uniform_real_centered_coefficient_energy_mean":fraction(mean),
                "uniform_real_centered_coefficient_energy_variance":fraction(variance),
                "lambda_max_and_full_metric_condition_number_squared_threshold":fraction(threshold),
                "source_probability_lower_bound": {"numerator_hex":format(lower.numerator,"x"),"denominator_hex":format(lower.denominator,"x")},
                "all_positive_lifts_covered_not_just_constructed_lift":True,
                "different_coordinate_maps_or_all_weighted_algorithms_ruled_out":False},
            "allows_ratio_adaptive_conjugate_semilinear_metric_isometries":True,
            "scope": "K-conjugate-semilinear J with J^2=-I preserving BOTH the graph lattice and its ORIGINAL product coefficient metric",
            "weighted_quaternion_orders_general_quantum_algorithms_or_classical_lattice_methods_excluded":False,
            "status":"LOCAL_SOURCE_THEOREM_REVIEW_PENDING", "speedup_claim_allowed":False}


def audit_quaternion_encoding(ratio,q,*,include_matrices=False):
    ratio,d = _input(ratio,q)
    centered = tuple((v+q//2) % q-q//2 for v in ratio)
    norm = mul(centered,conjugate(centered))
    assert conjugate(norm)==norm
    one = (1,)+(0,)*(d-1)
    hamilton_compatible = all((v+w) % q==0 for v,w in zip(norm,one))
    # A short real residue lift plus a scalar q-multiple supplies a positive metric.
    rho = tuple((-v+q//2) % q-q//2 for v in norm)
    assert conjugate(rho)==rho
    off = sum(abs(v) for v in rho[1:])
    boost = max(0,(off+1-rho[0]+q-1)//q)
    positive = (rho[0]+boost*q, *rho[1:])
    lo,hi = positive[0]-off,positive[0]+off
    assert lo>=1
    assert all((v+w) % q==0 for v,w in zip(positive,norm))
    # A different encoding is always principal, with a KNOWN generator (M,1).
    # Its reduced norm is q, but its norm form need not be positive definite.
    principal = (q-norm[0], *(-v for v in norm[1:]))
    M = multiplication_matrix(centered)
    minimum_residue = tuple((-v+q//2) % q-q//2 for v in norm)
    residue_energy = sum(v*v for v in minimum_residue)
    assert sp.trace(multiplication_matrix(positive)**2)==d*sum(v*v for v in positive)
    assert sum(v*v for v in positive)>=residue_energy
    B = (q*sp.eye(d)).row_join(M).col_join(sp.zeros(d).row_join(sp.eye(d)))
    public = sp.eye(d).row_join(-M)
    P = sp.Matrix.hstack(*(sp.Matrix(conjugate(tuple(int(i==j) for i in range(d)))) for j in range(d)))
    zeros = sp.zeros(d)
    J0 = zeros.row_join(-P).col_join(P.row_join(zeros))
    assert J0.T*J0==sp.eye(2*d) and J0*J0==-sp.eye(2*d)
    assert (public*J0*B % q==sp.zeros(d,2*d))==hamilton_compatible
    J = zeros.row_join(-multiplication_matrix(positive)*P).col_join(P.row_join(zeros))
    assert public*J*B % q==sp.zeros(d,2*d)
    assert J*J==-sp.diag(multiplication_matrix(positive),multiplication_matrix(positive))
    # Right multiplication by the known alpha=(M,1), independent of PIP.
    generator_basis = M.row_join(-multiplication_matrix(principal)).col_join(sp.eye(d).row_join(M.T))
    assert public*generator_basis % q==sp.zeros(d,2*d)
    # Schur elimination makes its determinant det(M*M.T+principal)=q^d.
    assert M*M.T+multiplication_matrix(principal)==q*sp.eye(d)
    assert reduced_norm((centered,one),principal)==(q,)+(0,)*(d-1)
    result = {"status":"QUATERNION_ENCODING_AUDIT_REVIEW_PENDING", "dimension":d, "modulus":str(q),
              "canonical_native_ratio":list(map(str,ratio)),
              "hamilton_original_metric_left_ideal_compatible":hamilton_compatible,
              "standard_hamilton_action_original_metric_and_square_verified":True,
              "adaptive_definite_order": {
                  "parameter_coefficients":list(map(str,positive)),
                  "exact_spectral_lower_bound":str(lo), "exact_spectral_upper_bound":str(hi),
                  "parameter_real_and_strictly_positive":True,
                  "full_graph_kernel_left_ideal_closure_verified":True,
                  "original_coefficient_metric_replaced":positive!=one,
                  "weighted_metric_relative_to_original_norm_squared": ["1",str(max(1,hi))],
                  "every_positive_congruence_lift_lambda_max_squared_lower_bound":str(residue_energy),
                  "every_positive_congruence_lift_full_metric_condition_number_squared_lower_bound":str(residue_energy),
                  "norm_one_units": {
                      "scope":"This constructed order has C_rho>=I; integral coefficients, not a maximal overorder or arbitrary positive lift",
                      "exact_count":4*d if positive==one else 2*d,
                      "description":"signed R monomials, plus signed monomials times j only if rho=1",
                      "cannot_change_R_projective_direction":positive!=one,
                      "fixed_reduced_norm_principal_generators_original_physical_length_invariant":True,
                      "general_units_or_different_reduced_norms_classified":False},
                  "principality_promised_or_proved":positive==principal,
                  "known_principality_only_when_this_parameter_equals_the_explicit_principal_encoding":positive==principal,
                  "quaternion_generator_algorithm_supplied":False},
              "adaptive_known_principal_order": {
                  "parameter_coefficients":list(map(str,principal)),
                  "known_generator": [list(map(str,centered)),list(map(str,one))],
                  "generator_physical_norm_squared":str(sum(v*v for v in centered)+1),
                  "generator_reduced_norm":str(q), "exact_basis_determinant":str(q**d),
                  "nonzero_parameter_defines_a_quaternion_algebra":any(principal),
                  "zero_parameter_is_degenerate_NOT_quaternion_PIP_input":not any(principal),
                  "positive_norm_form_promised":False,
                  "PIP_has_an_unknown_generator_to_find":False,
                  "source_metric_or_shortness_guarantee_supplied":False},
              "candidate_record_accepted":False, "novelty_claim":False, "speedup_claim_allowed":False}
    if include_matrices:
        result["finite_algebra_certificate"] = {"graph_kernel_column_basis": [[str(v) for v in row] for row in B.tolist()],
             "positive_order_left_j": [[str(v) for v in row] for row in J.tolist()],
             "known_principal_generator_basis": [[str(v) for v in row] for row in generator_basis.tolist()]}
    return result


def run_controls():
    rng = random.Random(51005)
    finite = []
    for d,q in ((2,3),(4,3),(4,11),(8,3)):
        count = 0
        energy_sum = energy_square_sum = 0
        for ratio in itertools.product(range(q),repeat=d):
            norm = mul(ratio,conjugate(ratio))
            count += all((v+int(i==0)) % q==0 for i,v in enumerate(norm))
            residue = tuple((-v+q//2) % q-q//2 for v in norm)
            energy = sum(v*v for v in residue)
            energy_sum += energy
            energy_square_sum += energy*energy
        expected = q+1 if d==2 else q**(d//2)-1
        assert count==expected
        finite.append({"d":d,"q":q,"all_ratio_count":q**d,"eligible_ratio_count":count,
                       "d2_exception_is_not_the_high_CRT_formula":d==2,
                       "native_centered_real_norm_energy_sum":energy_sum,
                       "native_centered_real_norm_energy_square_sum":energy_square_sum})
        if d>=4:
            alpha = Fraction(q**(d//2)-1,q**(d//2))
            mu2 = Fraction(q*q-1,12)
            mu4 = Fraction((q*q-1)*(3*q*q-7),240)
            mean = (d-1)*mu2
            variance = (2*d-3)*(mu4-mu2*mu2)
            assert Fraction(energy_sum,q**d)==alpha*mean
            assert Fraction(energy_square_sum,q**d)==alpha*(variance+mean*mean)
    identities = [audit_quaternion_encoding(tuple(rng.randrange(q) for _ in range(d)),q,include_matrices=True)
                  for d,q in ((2,7),(4,11),(8,19))]
    native_data = json.loads(NATIVE.read_text())
    original = tuple(int(v) for v in native_data["native_ratio"])
    q = int(native_data["q"])
    ratio = tuple(v % q for v in conjugate(original))
    native = audit_quaternion_encoding(ratio,q)
    d = len(original)
    rows = native_data["reduced_row_basis"]
    for row in rows:
        x,y = tuple(map(int,row[:d])),tuple(map(int,row[d:]))
        assert kernel_member((x,scale(y,-1)),ratio,q)
    native.update({"original_saved_ratio":list(map(str,original)),
                   "graph_ratio_is_original_adjoint":True,
                   "physical_coordinate_map":"(x,y)->(g,f)=(x,-y), with graph ratio bar(m)",
                   "coordinate_map_is_exact_signed_isometry":True,
                   "saved_native_reduced_basis_rows_checked":len(rows)})
    assert not native["hamilton_original_metric_left_ideal_compatible"]
    parameters = json.loads(PARAMETERS.read_text())["parameter_rows"]
    source = [quaternion_source_gate(row["d"],int(row["q"])) for row in parameters]
    counter = audit_quaternion_encoding((128,0),257,include_matrices=True)
    assert kernel_member(((-1,0),(2,0)),(128,0),257)
    return {"status":"NATIVE_QUATERNION_ROUTE_CONSTRUCTED_AND_SCOPED_REVIEW_PENDING",
            "complete_finite_source_counts":finite, "random_algebra_controls":identities,
            "same_saved_native_d64_kernel":native, "growing_native_source_gates":source,
            "known_long_generator_short_nongenerator_countercontrol": {
                "encoding":counter,"short_relation":[[-1,0],[2,0]], "short_physical_norm_squared":5,
                "every_principal_generator_norm_squared_lower_bound_for_this_d2_order":str(128**2-2*257),
                "scope":"d2 rational center and this deliberately structured ratio; not a native-average generator bound"},
            "literature": [{"id":"EPRINT-2025-287","url":"https://eprint.iacr.org/2025/287",
                            "scope":"Rank-two module-LIP to norm-reduced quaternion PIP; NOT a supplied efficient native rank-two relation generator"},
                           {"id":"EPRINT-2025-1095","url":"https://eprint.iacr.org/2025/1095",
                            "scope":"Quaternion generator remains unresolved; exhaustive four-square/ideal enumeration is not an efficient solver"}],
            "claim_gate": {"adaptive_quaternion_order_and_full_kernel_map_constructed":True,
                           "ratio_adaptive_original_metric_Hamilton_route_typically_available":False,
                           "native_quaternion_ideal_principality_guaranteed":False,
                           "known_adaptive_principal_order_generator_solves_shortness":False,
                           "uniform_polynomial_quaternion_generator_supplied":False,
                           "all_weighted_quaternion_or_general_quantum_algorithms_ruled_out":False,
                           "independent_review":False,"novelty_claim":False,"speedup_claim_allowed":False},
            "dependency_sha256": {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__),ROOT/"theorems/structured_edcp_upstream_mixing.py",NATIVE,PARAMETERS)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"finite_counts":report["complete_finite_source_counts"],
                      "native_metric_compatible":report["same_saved_native_d64_kernel"]["hamilton_original_metric_left_ideal_compatible"],
                      "source_exponents":[r["full_source_probability_upper_bound_dyadic_exponent"] for r in report["growing_native_source_gates"]],
                      "claim_gate":report["claim_gate"]},indent=2))


if __name__=="__main__":
    main()
