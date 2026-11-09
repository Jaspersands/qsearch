#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Five prescribed finite Hankel/resultant falsifiers, no quantum execution."""

from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
from sage.all import GF, PolynomialRing, matrix, vector
from resultant_hyperplane_control import TOLERANCE, chi, cleaned_source, normalized_fft
from corrupted_character_resultant_control import table_only_attack


def virtual_and_hankel_analysis(Q,m):
    """Secret algebra is confined to analysis, never supplied to the source."""
    field,ring = Q.base_ring(),Q.parent()
    p,d = int(field.order()),int(Q.degree())
    q = tuple(int(Q[i]) for i in range(d+1))
    U = math.prod(p**int(f.degree())-1 for f,multiplicity in Q.factor())
    assert Q.is_monic() and Q.is_squarefree()
    normalization_squared = p**(m+1-d)*U
    signs = np.zeros((p,)*d,dtype=np.int8)
    for remainder in itertools.product(range(p),repeat=d):
        signs[remainder] = chi(Q.resultant(ring(list(remainder))))
    # Public polynomial reduction is used here only to evaluate the VIRTUAL
    # analysis state.  This replaces p^(m+1) dense Sage resultant calls.
    X = ring.gen()
    reduction = np.array([[int((X**j % Q)[i]) for j in range(m+1)] for i in range(d)],dtype=np.int64)
    labels = np.indices((p,)*(m+1),dtype=np.int64).reshape(m+1,-1)
    remainders = reduction @ labels % p
    virtual = (signs[tuple(remainders)]/math.sqrt(normalization_squared)).reshape((p,)*(m+1))
    assert np.count_nonzero(virtual) == normalization_squared
    assert abs(float(np.vdot(virtual,virtual).real)-1)<TOLERANCE
    virtual_probability = np.abs(normalized_fft(virtual))**2

    shifted_Q = matrix(field,[[int((X**j*Q)[i]) for i in range(m+1)] for j in range(m-d+1)])
    H_basis = shifted_Q.right_kernel().basis_matrix()
    assert H_basis.nrows() == d
    H = [tuple(int(a) for a in vector(field,c)*H_basis) for c in itertools.product(range(p),repeat=d)]
    H_mask = np.zeros_like(virtual_probability,dtype=bool)
    for y in H:
        H_mask[y] = True
    virtual_off_H_mass = float(np.sum(virtual_probability[~H_mask]))
    assert virtual_off_H_mass<TOLERANCE
    support = [y for y in H if virtual_probability[y]>TOLERANCE]
    assert len(support) == U
    flat_error = max(abs(float(virtual_probability[y])-1/U) for y in support)
    assert flat_error<TOLERANCE

    decoded_Q_labels = []
    ranks = {}
    for y in H:
        hankel = matrix(field,d,d,[y[i+j] for i in range(d) for j in range(d)])
        rank = int(hankel.rank())
        ranks[rank] = ranks.get(rank,0)+1
        supported = virtual_probability[y]>TOLERANCE
        assert supported == (rank == d)
        if rank == d:
            rhs = -vector(field,y[d:2*d])
            decoded = tuple(int(a) for a in hankel.solve_right(rhs))+(1,)
            assert decoded == q
            decoded_Q_labels.append(y)
    assert len(decoded_Q_labels) == U
    return virtual,decoded_Q_labels,{
        "U":U,"virtual_normalization_squared":normalization_squared,
        "ambient_coefficient_dimension":m+1,"ambient_label_count":p**(m+1),
        "shifted_Q_kernel_dimension":m-d+1,"H_dimension":d,"H_points_checked":len(H),
        "virtual_fourier_support_count":len(support),
        "virtual_fourier_support_flatness_max_error":flat_error,
        "virtual_fourier_off_H_mass":virtual_off_H_mass,
        "exact_hankel_rank_counts_on_H":ranks,
        "all_virtual_support_labels_full_rank_and_decode_Q":True,
        "all_virtual_zero_labels_in_H_singular":True,
        "decoded_Q_label_count":len(decoded_Q_labels),
    }


def inspect(Q,name,include_corrupted=False):
    field = Q.base_ring()
    p,d = int(field.order()),int(Q.degree())
    m = 2*d-1
    q = tuple(int(Q[i]) for i in range(d+1))
    clean_table = [chi(Q(field(x))) or 1 for x in range(p)]
    roots = [x for x in range(p) if Q(field(x)) == 0]
    nonroots = [x for x in range(p) if x not in roots]
    masks = [("clean",[])]
    if include_corrupted:
        masks.append(("first_nonroot_flip",nonroots[:1]))
    # Full original-degree native table attack is completed before sources.
    observed_tables,baselines = [],[]
    for mask_name,mask in masks:
        observed = [a*(-1 if x in mask else 1) for x,a in enumerate(clean_table)]
        attack,candidates = table_only_attack(p,d,observed)
        true = next(row for row in candidates if row[0] == q)
        attack["true_candidate_hamming_distance_analysis_only"] = true[1]
        attack["true_candidate_is_nearest_analysis_only"] = true[1] == attack["nearest_hamming_distance"]
        attack["maximum_wrong_projection_score_analysis_only"] = max((row[2]/p)**2 for row in candidates if row[0] != q)
        assert true[1] == len(mask)
        observed_tables.append(observed)
        baselines.append(attack)

    virtual,decodable_labels,analysis = virtual_and_hankel_analysis(Q,m)
    U = analysis["U"]
    N0 = (p-1)*math.comb(p,m)
    Ngood = (p-1)*math.comb(p-len(roots),m)
    gamma_clean_squared = Ngood**2/(N0*analysis["virtual_normalization_squared"])
    gamma_clean = math.sqrt(gamma_clean_squared)
    controls = []
    for (mask_name,mask),observed,baseline in zip(masks,observed_tables,baselines):
        def fixed_oracle(x):
            return observed[x]
        uncorrected,_,source_signs,diagnostic_calls = cleaned_source(p,m,fixed_oracle)
        corrected = uncorrected.copy()
        # m is the root-source degree; d is the TARGET degree.  This phase
        # correction uses only the PUBLIC leading coefficient and degrees.
        for label in source_signs:
            corrected[label] *= chi(field(label[m]))**(d-m)
        n = len(nonroots)
        B = sum(x in nonroots for x in mask)
        numerator = sum((-1)**j*math.comb(B,j)*math.comb(n-B,m-j)
                        for j in range(B+1) if 0<=m-j<=n-B)
        E = Fraction(numerator,math.comb(n,m))
        predicted = chi(field(-1))**d*gamma_clean*float(E)
        overlap = np.vdot(virtual,corrected)
        uncorrected_overlap = np.vdot(virtual,uncorrected)
        assert abs(overlap-predicted)<TOLERANCE
        assert abs(abs(overlap)**2-gamma_clean_squared*float(E)**2)<TOLERANCE
        if d == 2:
            assert abs(uncorrected_overlap)<TOLERANCE
            assert abs(predicted)>TOLERANCE
        if mask:
            assert (p,d,m,n,B)==(7,3,5,6,1) and E == Fraction(-2,3)
        probability = np.abs(normalized_fft(corrected))**2
        decodable_mass = float(sum(probability[y] for y in decodable_labels))
        assert decodable_mass+TOLERANCE >= abs(overlap)**2
        controls.append({
            "source_name":mask_name,"mask":mask,"fixed_native_table":observed,
            "classical_first_original_degree_attack":baseline,
            "source_constructor_diagnostic_oracle_calls":diagnostic_calls,
            "exact_without_replacement_subset_average_Em":str(E),
            "signed_corrected_virtual_overlap_prediction":predicted,
            "signed_corrected_virtual_overlap_observed_real":float(overlap.real),
            "corrected_overlap_prediction_abs_error":float(abs(overlap-predicted)),
            "corrected_virtual_overlap_squared":float(abs(overlap)**2),
            "uncorrected_virtual_overlap_squared_negative_control":float(abs(uncorrected_overlap)**2),
            "actual_probability_fully_decodable_frequencies":decodable_mass,
            "actual_total_probability_decoding_Q":decodable_mass,
            "lower_bound_from_overlap_squared":gamma_clean_squared*float(E)**2,
        })
    return {
        "name":name,"p":p,"target_degree_d":d,"root_source_degree_m":m,
        "Q_ascending_coefficients":list(q),"roots_analysis_only":roots,
        "N0":N0,"Ngood":Ngood,"gamma_clean_squared":gamma_clean_squared,
        "virtual_and_exact_Hankel_analysis":analysis,"controls":controls,
        "large_prime_theorem_threshold_satisfied":False,
    }


def main():
    R5=PolynomialRing(GF(5),"X")
    X=R5.gen()
    R7=PolynomialRing(GF(7),"X")
    Y=R7.gen()
    assert (X**2+2).is_irreducible()
    assert (Y**2+1).is_irreducible() and (Y**3-2).is_irreducible()
    cases = [inspect(X*(X-1),"p5_split_quadratic"),
             inspect(X**2+2,"p5_irreducible_quadratic"),
             inspect(Y*(Y**2+1),"p7_mixed_cubic",True),
             inspect(Y**3-2,"p7_irreducible_cubic")]
    artifact = {
        "scope":"Four predeclared clean sources and one fixed corrupted source. Exact Sage field/rank/solve algebra plus floating normalized NumPy FFT, no coherent circuit or asymptotic success evidence. All prescribed primes are below theorem thresholds.",
        "native_source":"Unchanged cleaned_source(p,m,F) receives only native F. Public leading-coefficient correction chi(a)^(d-m) changes chi(a)^m to the REQUIRED TARGET phase chi(a)^d; uncorrected source retained as negative control. No Q, roots, factors, resultant or Hankel solution supplied to source.",
        "virtual_analysis_only":"chi(resultant(Q,R))/sqrt(p^(m+1-d)*U), m=2d-1, ascending coefficients. Exactly U nonzero Fourier labels, flat1/U, supported in the annihilator of span{X^j Q:0<=j<=m-d}.",
        "fourier_convention":"Unchanged imported normalized_fft, np.fft.fftn(norm=ortho), negative exponent.",
        "public_hankel_decoder":"On y_0..y_(2d-1), form H[i,j]=y_(i+j), i,j=0..d-1. If invertible solve q_lower=-H^(-1)*(y_d..y_(2d-1)); output monic degree-d candidate. The script checks all p^d labels of the true annihilator, without ambient Hankel enumeration. Any ambient frequency decoding Q satisfies all d shifted-Q recurrences and therefore lies in that annihilator, so the recorded Q-decoding mass is complete.",
        "coherence_boundary":"State arrays predict the cleaned source law; source preparation, coherent root erasure, Fourier circuits and quantum execution are not implemented.",
        "cases":cases,"all_assertions_passed":True,
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(artifact,indent=2)+"\n")
    for case in cases:
        for control in case["controls"]:
            print(json.dumps({"name":case["name"],"source":control["source_name"],"U":case["virtual_and_exact_Hankel_analysis"]["U"],"rank_counts":case["virtual_and_exact_Hankel_analysis"]["exact_hankel_rank_counts_on_H"],"Em":control["exact_without_replacement_subset_average_Em"],"overlap2":control["corrected_virtual_overlap_squared"],"uncorrected_overlap2":control["uncorrected_virtual_overlap_squared_negative_control"],"actual_decodable_mass":control["actual_probability_fully_decodable_frequencies"]}))


if __name__=="__main__":
    main()
