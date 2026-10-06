"""Original-metric conductor-order encoding and scoped principality gate.

LOCAL DERIVATION / REVIEW PENDING. Uses the published full-signature theorem
for real 2-power cyclotomic fields. No quantum generator or speedup claim.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import sympy as sp

from native_rlwe_quaternion_kernel import (
    NATIVE, PARAMETERS, _input, add, conjugate, kernel_member, mul,
    multiplication_matrix, reduced_norm,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/native_rlwe_conductor_order.json"
SIGNATURE_SOURCE = "https://msp.org/pjm/2019/298-2/pjm-v298-n2-p03-s.pdf"


def audit_conductor_order(ratio,q):
    ratio,d = _input(ratio,q)
    m = tuple((v+q//2) % q-q//2 for v in ratio)
    one = (1,)+(0,)*(d-1)
    M = multiplication_matrix(m)
    B = (q*sp.eye(d)).row_join(M).col_join(sp.zeros(d).row_join(sp.eye(d)))
    P = sp.Matrix.hstack(*(sp.Matrix(conjugate(tuple(int(i==j) for i in range(d)))) for j in range(d)))
    J = sp.zeros(d).row_join(-q*P).col_join((q*P).row_join(sp.zeros(d)))
    public = sp.eye(d).row_join(-M)
    assert public*J*B % q==sp.zeros(d,2*d)
    assert J.T*J==q*q*sp.eye(2*d) and J*J==-q*q*sp.eye(2*d)
    beta = add(mul(m,conjugate(m)),one)
    C = multiplication_matrix(beta)
    determinant = int(C.det(method="domain-ge"))
    assert determinant>=1 and C==M*M.T+sp.eye(d)
    locally_principal_certificate = math.gcd(determinant,q)==1
    # O_q*(M+j) is a contained global sublattice, NOT generally the full ideal.
    contained_basis = M.row_join(-q*sp.eye(d)).col_join(sp.eye(d).row_join(q*M.T))
    assert public*contained_basis % q==sp.zeros(d,2*d)
    return {
        "status":"ORIGINAL_METRIC_CONDUCTOR_IDEAL_AUDIT_REVIEW_PENDING",
        "dimension":d, "modulus":str(q), "graph_ratio":list(map(str,ratio)),
        "order":"O_q=R+qR*j inside O_0=R+R*j, with j^2=-1 and j*a=bar(a)*j",
        "native_graph_is_fractional_left_ideal":True,
        "original_physical_metric_preserved_exactly":True,
        "integral_ideal_normalization":"q*Lambda subset O_q; global scalar q is charged and cancels relative metric distortion",
        "order_and_graph_covolume":str(q**d),
        "local_principality": {
            "certificate_at_primes_dividing_q_supplied":locally_principal_certificate,
            "generator":"M+j", "reduced_norm_coefficients":list(map(str,beta)),
            "contained_sublattice_global_index_hex":format(determinant,"x"),
            "contained_sublattice_equals_full_graph_globally":determinant==1,
            "all_primes_away_from_q_generator":"1",
            "failed_certificate_is_not_a_local_nonprincipality_proof":True},
        "ambient_order_saturation": {
            "O_0_times_native_graph_equals_O_0":locally_principal_certificate,
            "certificate":"Lambda+j*Lambda contains qO_0 and the block basis [C_M,-I;I,C_M^T], determinant Norm_K(1+M*bar(M))",
            "every_overorder_containing_O_0_erases_graph_upon_extension":locally_principal_certificate,
            "M_dependent_overorder_choice_not_ruled_out":True,
            "preserving_extra_level_data_or_back_intersection_is_not_free":True},
        "global_principality": {
            "principal_over_THIS_conductor_order":not any(ratio),
            "necessary_and_sufficient_native_ratio_is_zero":True,
            "argument":"Equal covolumes force a generator to be a unit of O_0; full real unit signatures reduce every O_0 unit to a central unit times a signed monomial or its j multiple; only M=0 admits one",
            "depends_on_published_full_unit_signature_theorem":True,
            "independent_review":False,
            "source_uniform_principal_probability": {"numerator_hex":"1","denominator_hex":format(q**d,"x")}},
        "all_quaternion_orders_or_short_element_algorithms_ruled_out":False,
        "candidate_record_accepted":False,"speedup_claim_allowed":False,"novelty_claim":False,
    }


def run_controls():
    controls = [audit_conductor_order(m,q) for m,q in
                (((0,0),3),((1,0),3),((1,1),3),((1,1,0,0),3),((2,8,7,4),11))]
    unit_count = mixed_count = 0
    # Exact bounded algebra checks, never a fast unit-group algorithm.
    for coordinates in itertools.product((-1,0,1),repeat=8):
        g,f = coordinates[:4],coordinates[4:]
        beta = reduced_norm((g,f),(1,0,0,0))
        assert beta[2]==0 and beta[3]==-beta[1]
        field_norm = (beta[0]*beta[0]-2*beta[1]*beta[1])**2
        if field_norm==1:
            unit_count += 1
            mixed_count += bool(any(g) and any(f))
    assert mixed_count==0
    saved = json.loads(NATIVE.read_text())
    q = int(saved["q"])
    ratio = tuple(v % q for v in conjugate(tuple(map(int,saved["native_ratio"]))))
    native = audit_conductor_order(ratio,q)
    assert native["local_principality"]["certificate_at_primes_dividing_q_supplied"]
    assert not native["global_principality"]["principal_over_THIS_conductor_order"]
    return {"status":"CONDUCTOR_METRIC_ROUTE_CONSTRUCTED_PRINCIPALITY_BLOCKED_REVIEW_PENDING",
            "finite_controls":controls,"same_saved_native_d64_kernel":native,
            "bounded_d4_unit_check":{"coefficient_vectors_checked":3**8,"ambient_units":unit_count,"mixed_block_units":mixed_count},
            "published_dependency":{"url":SIGNATURE_SOURCE,"location":"Proposition3, PDF page8, journal page291",
                                    "statement_used":"Full circular-unit signature rank for maximal real 2-power cyclotomic fields; hence every totally positive unit is a square",
                                    "not_Weber_class_number_one_conjecture":True},
            "claim_gate":{"metric_preserving_encoding_constructed":True,"generic_quaternion_PIP_input_promise_satisfied":False,
                          "general_nonprincipal_ideal_short_element_solver_supplied":False,"independent_review":False,
                          "novelty_claim":False,"speedup_claim_allowed":False},
            "dependency_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__), ROOT/"theorems/native_rlwe_quaternion_kernel.py", NATIVE, PARAMETERS)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    native = report["same_saved_native_d64_kernel"]
    print(json.dumps({"status":report["status"],"native_locally_principal":native["local_principality"]["certificate_at_primes_dividing_q_supplied"],
                      "native_globally_principal":native["global_principality"]["principal_over_THIS_conductor_order"],
                      "bounded_unit_check":report["bounded_d4_unit_check"],"claim_gate":report["claim_gate"]},indent=2))


if __name__=="__main__":
    main()
