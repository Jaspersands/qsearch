"""Executed finite-state audit of the published ternary decoder-to-filter reduction.

LOCAL IMPLEMENTATION AUDIT / REVIEW PENDING. Exponential statevector/basis-table
verification only, not a compiled scalable quantum algorithm or a native DCP solver.
arXiv:2609.40321v1 Section3; reduction credited there to Chen-Liu-Zhandry.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

from ternary_quotient_decoder import decode_ternary_binary_error, run_controls as decoder_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/ternary_decoder_filter.json"


def exact(value):
    value = Fraction(value)
    return {"numerator": value.numerator, "denominator": value.denominator}


def _index(vector):
    result = 0
    for v in vector:
        result = 3*result+v
    return result


def trine_to_not_unitary():
    omega = np.exp(2j*np.pi/3)
    return np.asarray([(1, 1j*omega**(-r), -1j*omega**r) for r in range(3)]) / math.sqrt(3)


def controlled_not_preparation(value):
    if type(value) is not int or value not in (0,1,2):
        raise ValueError("canonical ternary control required")
    # Columns form an orthonormal basis; column zero prepares |not 0>.
    base = np.asarray(((0,1,0), (1/math.sqrt(2),0,1/math.sqrt(2)),
                       (-1/math.sqrt(2),0,1/math.sqrt(2))), dtype=complex)
    return np.roll(base, value, axis=0)


def apply_local_readout(state, columns):
    tensor = np.asarray(state, dtype=complex).reshape((3,)*columns+(state.shape[1],))
    U = trine_to_not_unitary().conj().T
    for axis in range(columns):
        tensor = np.moveaxis(np.tensordot(U, tensor, axes=(1,axis)), 0, axis)
    return tensor.reshape(state.shape)


def decoder_erasure(state, decoded, *, inverse=False):
    """Known controlled subtraction is a complete permutation, including failures."""
    values = tuple(itertools.product(range(3), repeat=len(decoded[0])))
    if state.shape != (len(decoded), len(values)):
        raise ValueError("basis-table decoder and state dimensions differ")
    output = np.zeros_like(state)
    direction = 1 if inverse else -1
    for b, d in enumerate(decoded):
        for i, s in enumerate(values):
            r = tuple((x+direction*y) % 3 for x,y in zip(s,d))
            output[b,_index(r)] = state[b,i]
    return output


def signed_word_to_subset(labels, signs):
    """Inverse IID-preserving last-column shear; orient the last sign to +1."""
    A = tuple(tuple(row) for row in labels)
    signs = tuple(signs)
    if not A or not A[0] or any(len(row) != len(signs) for row in A):
        raise ValueError("nonempty matrix matching signed word required")
    if any(type(v) is not int or v not in (0,1,2) for row in A for v in row):
        raise ValueError("canonical ternary labels required")
    if any(type(v) is not int or v not in (1,2) for v in signs):
        raise ValueError("signed word must contain only +1 or -1")
    if any(sum(a*c for a,c in zip(row,signs)) % 3 for row in A):
        raise ValueError("signed word is not a zero sum")
    oriented = tuple(c*signs[-1] % 3 for c in signs)
    word = tuple((c-1) % 3 for c in oriented[:-1])+(1,)
    H = tuple(row[:-1]+((row[-1]+sum(row[:-1])) % 3,) for row in A)
    assert all(v in (0,1) for v in word) and word[-1] == 1
    assert all(sum(a*x for a,x in zip(row,word)) % 3 == 0 for row in H)
    return H, word


def target_to_signed_labels(labels, target):
    """IID-preserving full-target source, specialized to the signed-sum interface."""
    A = tuple(tuple(row) for row in labels)
    target = tuple(target)
    if not A or not A[0] or any(len(row) != len(A[0]) for row in A) or len(target) != len(A):
        raise ValueError("nonempty rectangular matrix and full target required")
    if any(type(v) is not int or v not in (0,1,2) for row in A for v in row) or any(
            type(v) is not int or v not in (0,1,2) for v in target):
        raise ValueError("canonical ternary source required")
    return tuple(row+((-t-sum(row)) % 3,) for row,t in zip(A,target))


def signed_word_to_target_witness(labels, target, signs):
    B = target_to_signed_labels(labels,target)
    _, extended = signed_word_to_subset(B,signs)
    word = extended[:-1]
    assert all(sum(a*x for a,x in zip(row,word)) % 3 == t for row,t in zip(labels,target))
    return word


def audit_filter(labels, degree=2, *, decoder_offset=None, decoder_mode="computed", include_table=False):
    A = tuple(tuple(row) for row in labels)
    if not A or not A[0] or any(len(row) != len(A[0]) for row in A):
        raise ValueError("nonempty rectangular ternary label matrix required")
    n,m = len(A),len(A[0])
    if n > 2 or m > 6 or any(type(a) is not int or a not in (0,1,2) for row in A for a in row):
        raise ValueError("canonical labels in explicit n<=2,m<=6 verification budget required")
    offset = (0,)*n if decoder_offset is None else tuple(decoder_offset)
    if len(offset) != n or any(type(v) is not int or v not in (0,1,2) for v in offset):
        raise ValueError("canonical decoder corruption offset required")
    if decoder_mode not in ("computed", "constant-zero"):
        raise ValueError("computed or constant-zero calibration decoder required")
    secrets = tuple(itertools.product(range(3), repeat=n))
    observations = tuple(itertools.product(range(3), repeat=m))
    signed = tuple(itertools.product((1,2), repeat=m))
    status_counts = Counter()
    decoded = []
    for b in observations:
        record = decode_ternary_binary_error(A,tuple((v-1) % 3 for v in b),degree)
        status_counts[record["status"]] += 1
        # A failed decoder is extended to a total classical function, not accepted.
        d = record["secret"] if record["secret"] is not None else (0,)*n
        if decoder_mode == "constant-zero":
            d = (0,)*n
        decoded.append(tuple((x+y) % 3 for x,y in zip(d,offset)))
    G,N = 3**n,2**m
    source = np.zeros((3**m,G), dtype=complex)
    ideal_counts = np.zeros(3**m, dtype=np.int64)
    missing_counts = np.zeros(3**m, dtype=np.int64)
    failure_count = 0
    for i,s in enumerate(secrets):
        ell = tuple(sum(row[j]*s[k] for k,row in enumerate(A)) % 3 for j in range(m))
        # Controlled local unitaries prepare these columns from a uniform |s>.
        vector = np.asarray([1.0],dtype=complex)
        for value in ell:
            vector = np.kron(vector, controlled_not_preparation(value)[:,0])
        source[:,i] = vector/math.sqrt(G)
        for delta in signed:
            b = tuple((x+y) % 3 for x,y in zip(ell,delta))
            index = _index(b)
            sign = (-1)**sum(v == 2 for v in delta)
            ideal_counts[index] += sign
            if decoded[index] != s:
                failure_count += 1
                missing_counts[index] += sign
    eta = Fraction(failure_count,G*N)
    missing_norm = Fraction(sum(int(v)**2 for v in missing_counts),G*N)
    erased = decoder_erasure(source,decoded)
    assert np.max(np.abs(decoder_erasure(erased,decoded,inverse=True)-source)) < 1e-12
    good = erased[:,0]
    ideal = ideal_counts / math.sqrt(G*N)
    missing = missing_counts / math.sqrt(G*N)
    assert np.max(np.abs(ideal-good-missing)) < 1e-12
    assert abs(float(np.sum(abs(erased[:,1:])**2))-float(eta)) < 1e-12
    output = apply_local_readout(erased,m)
    masses = np.sum(abs(output)**2,axis=1)
    valid = [c for c in signed if all(sum(row[j]*c[j] for j in range(m)) % 3 == 0 for row in A)]
    success = float(sum(masses[_index(c)] for c in valid))
    ideal_output = apply_local_readout(ideal[:,None],m)[:,0]
    invalid = np.ones(3**m, dtype=bool)
    invalid[[_index(c) for c in valid]] = False
    assert np.max(np.abs(ideal_output[invalid]),initial=0) < 1e-12
    assert 1-success <= float(eta+missing_norm)+1e-10
    subsets = [signed_word_to_subset(A,c)[1] for c in valid]
    assert all(any(word) for word in subsets)
    original_labels = tuple(row[:-1] for row in A)
    original_target = tuple((-row[-1]-sum(row[:-1])) % 3 for row in A)
    target_words = [word[:-1] for word in subsets]
    assert all(all(sum(a*x for a,x in zip(row,word)) % 3 == t
                   for row,t in zip(original_labels,original_target)) for word in target_words)
    row = {"labels": A, "dimension": n, "samples": m, "degree": degree,
           "decoder_offset": offset, "decoder_mode": decoder_mode,
           "decoder_basis_table_status_counts": dict(status_counts),
           "exact_decoder_error_probability": exact(eta), "exact_missing_coherent_vector_norm_squared": exact(missing_norm),
           "pointwise_failure_probability_upper_bound": exact(min(Fraction(1),eta+missing_norm)),
           "executed_valid_signed_zero_sum_probability": success,
           "executed_nonempty_boolean_zero_sum_probability": success,
           "unheralded_state_norm_squared": float(np.sum(masses)),
           "secret_zero_register_probability": float(np.sum(abs(good)**2)),
           "failure_branches_discarded_or_renormalized": False,
           "verified_signed_witnesses": valid, "verified_boolean_witnesses": subsets,
           "random_signed_guess_zero_sum_probability": exact(Fraction(len(valid),N)),
           "exhaustive_classical_reference_finds_a_witness": bool(valid),
           "exhaustive_classical_reference_is_scalable_baseline": False,
           "specialized_full_target_source": {
               "original_labels": original_labels, "independent_full_target": original_target,
               "verified_target_witnesses": target_words,
               "executed_unconditional_target_success": success,
               "last_column_guaranteed_in_mapped_zero_witness": True,
               "hidden_marker_inclusion_probability_loss": False,
               "generic_zero_solver_automatically_has_this_property": False,
               "extra_public_arithmetic_columns": 1,
               "extra_known_prepared_qutrits": 1,
               "extra_unknown_native_DCP_states_assumed": False,
               "empty_original_witness_allowed_only_for_zero_target": True},
           "ideal_coherent_vector_norm_squared_NOT_a_normalized_physical_state": exact(Fraction(G*len(valid),N)),
           "explicit_simulator_dimension": G*3**m,
           "basis_table_is_only_exponential_verification_not_runtime_implementation": True,
           "scalable_reversible_decoder_circuit_compiled": False,
           "native_growing_modulus_DCP_solver": False,
           "candidate_record_accepted": False, "speedup_claim_allowed": False, "novelty_claim": False}
    if include_table:
        row["decoder_basis_table"] = decoded
    return row


def run_controls():
    complete = [audit_filter((a,),include_table=True) for a in itertools.product(range(3), repeat=4)]
    def read(record):
        return Fraction(record["numerator"],record["denominator"])
    eta = sum((read(row["exact_decoder_error_probability"]) for row in complete), Fraction()) / len(complete)
    missing = sum((read(row["exact_missing_coherent_vector_norm_squared"]) for row in complete), Fraction()) / len(complete)
    collision = Fraction(3)*(Fraction(2,3)**4)
    mean_failure = sum(1-row["executed_valid_signed_zero_sum_probability"] for row in complete) / len(complete)
    assert missing <= eta+collision
    assert mean_failure <= float(2*eta+collision)+1e-10
    A = decoder_controls()["actual_fixed_source_decoder_trials"][0]["labels"]
    vector = audit_filter(A,3,include_table=True)
    offset = audit_filter(((1,1,1,1),),decoder_offset=(1,),include_table=True)
    no_decoder = audit_filter(A,3,decoder_mode="constant-zero",include_table=True)
    assert abs(no_decoder["executed_valid_signed_zero_sum_probability"]-
               float(read(no_decoder["random_signed_guess_zero_sum_probability"]))) < 1e-12
    return {"status": "KNOWN_TERNARY_QUANTUM_REDUCTION_FINITE_AUDIT_REVIEW_PENDING",
            "source_url": "https://arxiv.org/html/2609.40321v1", "source_section": "3, credited there to CLZ22",
            "complete_native_one_dimensional_source": {
                "dimension": 1, "samples": 4, "complete_IID_label_matrices": len(complete),
                "complete_independent_target_sources_via_bijective_shear": len(complete),
                "mean_exact_decoder_error_probability": exact(eta),
                "mean_exact_missing_vector_norm_squared": exact(missing),
                "published_collision_slack": exact(collision),
                "mean_executed_failure_probability": mean_failure,
                "no_signed_solution_source_instances": sum(not row["verified_signed_witnesses"] for row in complete),
                "failure_upper_bound": exact(min(Fraction(1),2*eta+collision)),
                "all_source_instances_including_failures": complete},
            "fixed_two_dimensional_source": vector, "global_decoder_offset_control": offset,
            "no_decoder_control": no_decoder,
            "claim_gate": {"actual_preparation_erasure_local_readout_and_witness_mapping_executed": True,
                           "published_asymptotic_algorithm_fully_implemented": False,
                           "scalable_quantum_circuit_compiled": False,
                           "new_classical_quantum_separation_established": False,
                           "native_two_power_DCP_bridge_implemented": False,
                           "independent_review": False, "candidate_record_accepted": False,
                           "novelty_claim": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__),ROOT/"theorems/ternary_quotient_decoder.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    source = report["complete_native_one_dimensional_source"]
    print(json.dumps({"status":report["status"], "complete_source_matrices":source["complete_IID_label_matrices"],
                      "mean_failure":source["mean_executed_failure_probability"],
                      "vector_source_success":report["fixed_two_dimensional_source"]["executed_valid_signed_zero_sum_probability"],
                      "claim_gate":report["claim_gate"]},indent=2))


if __name__ == "__main__":
    main()
