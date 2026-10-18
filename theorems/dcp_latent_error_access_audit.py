"""Exact phase-qubit access falsifiers for hidden-error coincidence filters.

No general purification no-go. Orthogonal error registers, encoded redundant
sources, false-positive tests and extra source access require separate models.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

from sympy import I,Matrix,Rational,simplify,sqrt

from theorems.dcp_adaptive_direction_rank_gate import integer


ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/dcp_latent_error_access_audit.json"
CONTRACT=ROOT/"research/hypotheses/dcp_latent_error_access_audit_contract.json"
CONTRACT_ID="phase_qubit_latent_error_equality_access_falsifier_v1"
PAIRS=((0,1),(1,0),(0,2),(1,2))


def root(q):
    if q==4:
        return I
    if q==3:
        return -Rational(1,2)+sqrt(3)*I/2
    raise ValueError("exact finite cyclotomic control supports q3 or q4")


def coefficients(value,q):
    real,imag=simplify(value).as_real_imag()
    if q==3:
        b=simplify(2*imag/sqrt(3))
        a=simplify(real+b/2)
    else:
        a,b=simplify(real),simplify(imag)
    if not a.is_Rational or not b.is_Rational:
        raise ValueError("not in the declared quadratic cyclotomic field")
    return [str(a),str(b)]


def serialize_matrix(M,q):
    return [[coefficients(M[i,j],q) for j in range(M.cols)] for i in range(M.rows)]


def unequal_state_span(q):
    z=root(q)
    phases=(1,z,simplify(z.conjugate()))
    vectors=Matrix([[1,phases[f],phases[e],phases[e]*phases[f]] for e,f in PAIRS])/2
    gram=(vectors*vectors.conjugate().T).applyfunc(simplify)
    determinant=simplify(gram.det())
    if determinant<=0:
        raise ArithmeticError("unequal-input span certificate is singular")
    return {"modulus":q,"possible_error_exponents":[0,1,q-1],
            "unequal_error_index_pairs":[list(pair) for pair in PAIRS],
            "normalized_product_vectors_in_quadratic_field":serialize_matrix(vectors,q),
            "unequal_input_Gram_matrix_in_quadratic_field":serialize_matrix(gram,q),
            "Gram_determinant_exact_rational":str(determinant),
            "input_Hilbert_dimension":4,"unequal_input_span_dimension":4,
            "positive_effect_rejecting_all_unequal_inputs_must_be_zero":True,
            "general_quantum_purification_impossible":False}


def coincidence_access_receipt(access_model,possible_errors=3,*,full_product_error_support=True):
    integer(possible_errors,"possible pure phase-error states",1,3)
    if type(full_product_error_support) is not bool:
        raise ValueError("explicit product-support model required")
    if not full_product_error_support and access_model=="phase-qubits-only":
        return {"access_model":access_model,"possible_phase_errors":possible_errors,
                "full_product_error_support_assumed":False,
                "status":"UNKNOWN_OUTSIDE_FULL_PRODUCT_ERROR_SUPPORT",
                "latent_error_equality_available":None,"extra_source_access_proved":False,
                "accepted_speedup_candidate":False}
    if access_model=="phase-qubits-only" and possible_errors==3:
        return {"access_model":access_model,"possible_phase_errors":3,
                "full_product_error_support_assumed":True,
                "status":"ZERO_FALSE_POSITIVE_EQUALITY_HERALD_HAS_ZERO_SUCCESS",
                "latent_error_equality_available":False,"extra_source_access_proved":False,
                "accepted_speedup_candidate":False}
    if access_model=="orthogonal-error-register-supplied":
        return {"access_model":access_model,"possible_phase_errors":possible_errors,
                "full_product_error_support_assumed":full_product_error_support,
                "status":"CONDITIONAL_EXTRA_SOURCE_ACCESS_NOT_CERTIFIED",
                "latent_error_equality_available":"ONLY_IF_THE_EXTRA_REGISTER_IS_ACTUALLY_SUPPLIED",
                "extra_source_access_proved":False,"accepted_speedup_candidate":False}
    if access_model=="phase-qubits-only":
        return {"access_model":access_model,"possible_phase_errors":possible_errors,
                "full_product_error_support_assumed":full_product_error_support,
                "status":"UNKNOWN_OUTSIDE_THREE_STATE_SPAN_ARGUMENT",
                "latent_error_equality_available":None,"extra_source_access_proved":False,
                "accepted_speedup_candidate":False}
    raise ValueError("unrecognized physical source access model")


def cnot_controls():
    phases=(1,I,-I)
    errors=(0,1,3)
    gate=Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    records=[]
    for e in range(3):
        for f in range(3):
            ze,zf=phases[e],phases[f]
            source=Matrix([1,zf,ze,ze*zf])/2
            result=gate*source
            branches=[]
            for outcome in (0,1):
                v=Matrix([result[outcome],result[2+outcome]])
                mass=simplify((v.conjugate().T*v)[0])
                density=(v*v.conjugate().T/mass).applyfunc(simplify)
                phase=simplify(ze*zf if outcome==0 else ze/zf)
                expected=Matrix([[1,phase.conjugate()],[phase,1]])/2
                if mass!=Rational(1,2) or (density-expected).applyfunc(simplify)!=Matrix.zeros(2):
                    raise ArithmeticError("physical CNOT/Z readout differs from sum/difference law")
                branches.append({"measured_target_Z":outcome,"Born_probability":"1/2",
                                 "root_density_quadratic_field":serialize_matrix(density,4),
                                 "root_error_exponent_mod4":(errors[e]+(1 if outcome==0 else -1)*errors[f])%4})
            records.append({"input_error_exponents":[errors[e],errors[f]],"errors_equal":e==f,
                            "branches":branches})
    return records


def conditional_classical_controls():
    K={0:Fraction(1,2),1:Fraction(1,4),3:Fraction(1,4)}
    p=sum(v*v for v in K.values())
    retained={e:v*v/p for e,v in K.items()}
    doubled={0:Fraction(0),1:Fraction(0),2:Fraction(0),3:Fraction(0)}
    for e,v in retained.items():
        doubled[2*e%4]+=v
    cos=(1,0,-1,0)
    retained_visibility=sum(v*cos[e] for e,v in retained.items())
    physical_sum_visibility=sum(v*cos[e] for e,v in doubled.items())
    return {"q4_p_half":{"formal_latent_equality_probability":str(p),
                         "formal_retained_error_kernel":{str(e):str(v) for e,v in retained.items()},
                         "CNOT_sum_error_kernel_IF_latent_equality_were_known":{str(e):str(v) for e,v in doubled.items()},
                         "formal_retained_error_visibility":str(retained_visibility),
                         "CNOT_sum_branch_visibility_given_magic_equality":str(physical_sum_visibility),
                         "latent_error_equality_measurement_available":False},
            "q3_p_two_thirds":{"exact_input_visibility":"0","exact_formal_pruned_visibility":"0",
                                "leaf_SNR_exact":"0","pruned_SNR_exact":"0",
                                "strict_leaf_dominance":False},
            "endpoint_p_zero_or_one":{"formal_retained_error_visibility_gain":"0",
                                       "strict_purifying_or_degrading":False}}


def build_report():
    return {"contract_id":CONTRACT_ID,"status":"EXACT_ACCESS_FALSIFIERS_EXTERNAL_REVIEW_PENDING",
            "accepted_speedup_candidate":False,"novelty_claim":False,"external_theorem_review_complete":False,
            "source_quantum_preparations_executed":0,
            "unequal_input_span_controls":[unequal_state_span(q) for q in (3,4)],
            "physical_CNOT_Z_controls":cnot_controls(),
            "conditional_classical_vs_physical_controls":conditional_classical_controls(),
            "access_receipts":[coincidence_access_receipt("phase-qubits-only"),
                               coincidence_access_receipt("orthogonal-error-register-supplied")],
            "tensor_extension_q4":[{"input_qubits":k,"non_all_equal_product_basis_dimension":1 << k,
                                     "Gram_determinant_one_over_two_exponent":(3+2*(k-2))*(1 << (k-2)),
                                     "same_no_false_positive_all_equal_herald_obstruction":True}
                                    for k in (2,3,4,8,16)],
            "scope":{"comparison_goal_is_exact_hidden_error_equality":True,
                     "three_distinct_possible_phase_errors_required":True,
                     "four_unequal_product_inputs_allowed_by_source_promise":True,
                     "unknown_secret_may_be_fixed_to_zero_for_counterexample":True,
                     "false_positive_purification_protocols_excluded":False,
                     "ensemble_equivalent_false_positive_channels_excluded":False,
                     "orthogonal_error_register_or_encoded_redundancy_excluded":False,
                     "correlated_equal_error_source_promises_excluded":False,
                     "all_noise_mitigation_or_quantum_algorithms_excluded":False,
                     "classical_conditional_kernel_identity_is_a_physical_instrument":False,
                     "original_hidden_error_labels_used_only_for_calibration":True},
            "review_target":"research/DCP_INTERLEAVED_TREE_MERGE_SYNDROME_PRUNING_AUDIT.md",
            "literature":["https://arxiv.org/abs/quant-ph/0202087"]}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write",action="store_true")
    args=parser.parse_args(argv)
    report=build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"exact_span_controls":2,
                      "physical_CNOT_controls":9,"general_purification_no_go":False,"artifact":str(REPORT)}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
