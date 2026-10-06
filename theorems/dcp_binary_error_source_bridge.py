"""Hidden-marker witness reduction and binary-error Fourier source barriers.

LOCAL DERIVATION / REVIEW PENDING. No quantum arithmetic finder or speedup.
The information bound concerns one unknown translation (and same-label copies),
NOT joint operations across native independently labeled input registers.
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

from dcp_bell_inference_kernel import exact
from dcp_terminal_affine_fibers import _positive_integer

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/reductions/dcp_binary_error_source_bridge.json"


def hidden_marker_target_wrapper(labels,modulus,target,zero_solver,*,marker_index,solver_seed=None):
    A=tuple(tuple(row) for row in labels)
    target=tuple(target)
    if type(modulus) is not int or modulus<2 or not A or not A[0] or any(len(row)!=len(A[0]) for row in A):
        raise ValueError("valid finite modular label matrix required")
    n,m=len(A),len(A[0])
    if len(target)!=n or any(type(t) is not int or not 0<=t<modulus for t in target) or any(type(a) is not int or not 0<=a<modulus for row in A for a in row):
        raise ValueError("canonical labels and full target required")
    if type(marker_index) is not int or not 0<=marker_index<=m or not callable(zero_solver):
        raise ValueError("valid shared marker seed and callable zero solver required")
    extended=[]
    for row,t in zip(A,target):
        values=[*row,(-t)%modulus]
        values[marker_index],values[m]=values[m],values[marker_index]
        extended.append(tuple(values))
    # Do NOT pass marker index, target or original matrix to the zero solver.
    word=zero_solver(tuple(extended),modulus,solver_seed)
    if type(word) is not int or not 0<word<1<<(m+1) or not (word>>marker_index&1):
        return None
    if any(sum(a*(word>>i&1) for i,a in enumerate(row))%modulus for row in extended):
        return None
    if (word>>marker_index&1)!=(word>>m&1):
        word^=(1<<marker_index)|(1<<m)
    witness=word&((1<<m)-1)
    assert all(sum(a*(witness>>i&1) for i,a in enumerate(row))%modulus==t for row,t in zip(A,target))
    return witness


def hidden_marker_source_certificate(original_columns,zero_success_lower_bound,*,returned_weight_lower_bound=1):
    _positive_integer(original_columns,"original column count")
    M=original_columns+1
    beta=Fraction(zero_success_lower_bound)
    if not 0<=beta<=1 or type(returned_weight_lower_bound) is not int or not 1<=returned_weight_lower_bound<=M:
        raise ValueError("valid nonempty zero-output success and weight promise required")
    return {"status":"CONDITIONAL_HIDDEN_MARKER_ZERO_TO_INDEPENDENT_TARGET_REDUCTION",
            "original_columns":original_columns,"zero_solver_columns":M,
            "assumed_verified_nonempty_zero_solver_success":exact(beta),
            "uniform_full_target_coverage_lower_bound":exact(beta*returned_weight_lower_bound/M),
            "exact_coverage_identity":"E_IID_extended_matrix,solver_randomness[successful_output_weight]/(m+1)",
            "uniform_swap_index_independent_of_IID_extended_matrix":True,
            "zero_solver_must_not_receive_marker_target_or_original_matrix_as_side_information":True,
            "one_extra_public_classical_column_not_an_extra_unknown_phase_state":True,
            "any_finite_abelian_group_version_valid_with_charged_group_operations":True,
            "source_alphabet_modulus_density_or_runtime_changes_removed":False,
            "uniform_polynomial_zero_solver_supplied":False,"candidate_record_accepted":False,"speedup_claim_allowed":False}


def two_point_fourier_certificate(modulus,*,gap=1):
    _positive_integer(modulus,"full modulus")
    if modulus<3 or type(gap) is not int or not 0<gap<modulus:
        raise ValueError("modulus>=3 and distinct two-point envelope required")
    divisor=math.gcd(gap,modulus)
    return {"modulus":modulus,"two_point_gap":gap,"gap_gcd_with_modulus":divisor,
            "minimum_fourier_support_with_both_nonzero_coefficients":modulus-divisor,
            "arbitrary_normalized_two_frequency_retention_mass_upper_bound":exact(min(Fraction(1),Fraction(4,modulus))),
            "bound_is_on_known_envelope_spectral_truncation_not_a_legal_unknown_translation_decoder":True,
            "binary_support_compatible_with_minimum_size":modulus-divisor<=2,
            "full_boolean_unit_gap_source":gap==1,
            "collective_multi_column_transforms_ruled_out":False}


def single_translation_conversion_certificate(modulus,copies=1):
    _positive_integer(modulus,"modulus")
    _positive_integer(copies,"same-translation input copies")
    if modulus<3:
        raise ValueError("nonbinary modulus required")
    rank=min(modulus,copies+1)
    return {"status":"LOCAL_SINGLE_TRANSLATION_SOURCE_INFORMATION_BOUND_REVIEW_PENDING",
            "modulus":modulus,"same_translation_input_copies":copies,"source_family_span_dimension":rank,
            "binary_localized_target_family_rank_lower_bound":modulus-1,
            "arbitrary_heralded_channel_uniform_mean_success_times_target_fidelity_upper_bound":exact(min(Fraction(1),Fraction(2*rank,modulus))),
            "proof":"Pull back target POVM |g_v><g_v|/2; its sum<=I. Any measurement guesses a uniform index on an r-dimensional input ensemble with probability<=r/q.",
            "exact_nonzero_pure_target_branch_ruled_out":modulus>2*copies+1,
            "arbitrary_exact_heralded_branch_necessary_same_translation_copies":modulus//2,
            "nonzero_success_on_every_translation_necessary_copies":max(1,modulus-2),
            "same_label_copies_granted_by_native_source":False,
            "native_different_label_collective_algorithm_ruled_out":False,
            "arbitrary_quantum_subset_sum_algorithm_ruled_out":False,
            "candidate_record_accepted":False,"speedup_claim_allowed":False}


def ternary_import_certificate(dimension,columns,native_modulus_bits):
    for value,name in ((dimension,"dimension"),(columns,"columns"),(native_modulus_bits,"native modulus bits")):
        _positive_integer(value,name)
    if native_modulus_bits<2:
        raise ValueError("native modulus>=4 required")
    # Exact integer logarithm upper bound avoids pretending log2(3) is exact.
    entropy_upper=(3**dimension-1).bit_length()
    return {"ternary_dimension":dimension,"ternary_columns":columns,"native_modulus_bits":native_modulus_bits,
            "ternary_group_entropy_bits_integer_upper_bound":entropy_upper,
            "one_selected_witness_full_group_readout_probability_upper_bound_dyadic_exponent":max(0,columns-entropy_upper),
            "bound_scope":"Only the one-word direct filter; not all generalized-dihedral algorithms or the paper's explicit-input subset-sum algorithm",
            "additive_homomorphism_between_ternary_and_two_power_groups_is_nontrivial":False,
            "nonlinear_or_collective_reduction_ruled_out":False,
            "zero_to_target_gap_removed_by_hidden_marker_under_its_contract":True,
            "field_alphabet_density_and_spectral_source_gaps_removed":False,
            "new_paper_is_a_native_DCP_solver":False,"candidate_record_accepted":False,"speedup_claim_allowed":False}


def _reference_zero_solver(A,q,seed=None):
    # Bounded controls ONLY: this is not an efficient zero-sum algorithm.
    return next((w for w in range(1,1<<len(A[0])) if all(
        sum(a*(w>>j&1) for j,a in enumerate(row))%q==0 for row in A)),None)


def _marker_controls():
    records=[]
    for q,m in ((3,2),(4,3)):
        accepted=weighted=zero_success=0
        for entries in itertools.product(range(q),repeat=m+1):
            A=(entries[:m],)
            target=(entries[m],)
            for marker in range(m+1):
                result=hidden_marker_target_wrapper(A,q,target,_reference_zero_solver,marker_index=marker)
                accepted+=result is not None
            word=_reference_zero_solver((entries,),q)
            if word is not None:
                zero_success+=1
                weighted+=word.bit_count()
        assert accepted==weighted
        assert accepted>=zero_success
        records.append({"modulus":q,"original_columns":m,"all_extended_native_label_tables":q**(m+1),
                        "complete_source_and_marker_trials":q**(m+1)*(m+1),
                        "accepted_target_trials":accepted,"successful_zero_output_weight_sum":weighted,
                        "nonempty_zero_successes":zero_success,
                        "exact_uniform_full_target_coverage":exact(Fraction(accepted,q**(m+1)*(m+1))),
                        "bounded_reference_zero_solver_is_polynomial":False})
    return records


def _translation_family_controls():
    records=[]
    rng=np.random.default_rng(4105)
    for q,copies in ((3,1),(4,1),(8,1),(8,2),(16,3)):
        omega=np.exp(2j*np.pi/q)
        source=np.array([[math.sqrt(math.comb(copies,r))*omega**(r*v)/math.sqrt(2**copies)
                          for v in range(q)] for r in range(copies+1)])
        g=np.zeros(q,dtype=complex)
        g[0],g[1]=1/math.sqrt(2),-1/math.sqrt(2)
        target=np.column_stack([np.roll(g,v) for v in range(q)])
        rank=int(np.linalg.matrix_rank(source,tol=1e-10))
        assert rank==copies+1
        target_rank=int(np.linalg.matrix_rank(target,tol=1e-10))
        assert target_rank==q-1
        assert all(np.linalg.matrix_rank(np.delete(target,j,axis=1),tol=1e-10)==q-1 for j in range(q))
        norm=float(np.linalg.norm(target@target.conj().T,2))
        assert norm<=2+1e-10
        matrix=rng.normal(size=(2*q,copies+1))+1j*rng.normal(size=(2*q,copies+1))
        channel,_=np.linalg.qr(matrix)
        channel=channel[:,:copies+1]
        score=float(sum(abs(np.vdot(target[:,v],channel[e*q:(e+1)*q,:]@source[:,v]))**2
                        for v in range(q) for e in range(2))/q)
        assert score<=min(1,2*rank/q)+1e-10
        exact_q3=None
        if q==3:
            fourier=np.fft.fft(g)/math.sqrt(q)
            Kfreq=np.zeros((q,2),dtype=complex)
            Kfreq[2,0],Kfreq[1,1]=math.sqrt(2)*fourier[2],math.sqrt(2)*fourier[1]
            K=np.fft.ifft(Kfreq,axis=0)*math.sqrt(q)
            residual=max(float(np.max(np.abs(K@source[:,v]-omega**(2*v)*target[:,v]))) for v in range(q))
            assert residual<1e-10
            assert np.max(np.abs(K.conj().T@K-np.eye(2)))<1e-10
            exact_q3=residual
        records.append({"modulus":q,"copies":copies,"source_family_rank":rank,"target_family_rank":target_rank,
                        "all_q_minus_one_target_columns_independent":True,"target_projector_sum_operator_norm":norm,
                        "actual_random_two_kraus_channel_mean_success_fidelity":score,
                        "ternary_exact_isometry_residual":exact_q3,
                        "certificate":single_translation_conversion_certificate(q,copies)})
    return records


def run_controls():
    return {"status":"LOCAL_DERIVATION_REVIEW_PENDING",
            "complete_hidden_marker_source_controls":_marker_controls(),
            "single_translation_channel_controls":_translation_family_controls(),
            "native_growing_modulus_source_ledgers":[{
                "dimension":n,"native_modulus_bits":4*n+1,
                "envelope":two_point_fourier_certificate(1<<(4*n+1)),
                "generously_assumed_but_unavailable_same_translation_copy_ledger":single_translation_conversion_certificate(1<<(4*n+1),n*n)} for n in (8,16,32)],
            "ternary_high_density_import_ledgers":[ternary_import_certificate(n,n*n//16,4*n+1) for n in (32,64,128,256)],
            "claim_gate":{"zero_to_uniform_target_interface_supplied_with_polynomial_loss":True,
                          "single_translation_exact_or_approximate_binary_error_conversion_closed_as_scoped":True,
                          "native_distinct_label_collective_binary_error_conversion_implemented":False,
                          "new_ternary_paper_directly_solves_native_DCP":False,
                          "global_quantum_subset_sum_no_go_claimed":False,"independent_theorem_review":False,
                          "uniform_polynomial_native_witness_finder_supplied":False,"candidate_record_accepted":False,
                          "novelty_claim":False,"speedup_claim_allowed":False},
            "dependency_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__),ROOT/"theorems/binary_error_hensel_decoder.py",ROOT/"theorems/dcp_direct_witness_filter.py")}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args=parser.parse_args()
    report=run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"claim_gate":report["claim_gate"]},indent=2))


if __name__ == "__main__":
    main()
