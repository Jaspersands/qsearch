#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Twelve fixed-table finite falsifiers, exact fields plus floating FFT only."""

from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
from sage.all import GF, PolynomialRing, matrix, vector
from resultant_hyperplane_control import (
    TOLERANCE, canonical_projective_labels, chi, cleaned_source, normalized_fft,
)


def choose(n,k):
    return math.comb(n,k) if 0 <= k <= n else 0


def table_only_attack(p,d,observed):
    """No secret, mask, root set or factorization enters this native attack."""
    field = GF(p)
    ring = PolynomialRing(field,"X")
    X = ring.gen()
    candidates = []
    for coefficients in itertools.product(range(p),repeat=d):
        candidate = X**d+ring(list(coefficients))
        if not candidate.is_squarefree():
            continue
        padded = [chi(candidate(field(x))) or 1 for x in range(p)]
        distance = sum(a != b for a,b in zip(padded,observed))
        correlation_numerator = p-2*distance
        candidates.append((tuple(coefficients)+(1,),distance,correlation_numerator))
    assert len(candidates) == p**d-p**(d-1)
    nearest = min(row[1] for row in candidates)
    maximum_absolute = max(abs(row[2]) for row in candidates)
    nearest_candidates = [list(row[0]) for row in candidates if row[1] == nearest]
    physical_best = [list(row[0]) for row in candidates if abs(row[2]) == maximum_absolute]
    physical_signed_numerators = [row[2] for row in candidates if abs(row[2]) == maximum_absolute]
    return {
        "native_fixed_table_queries":p,
        "monic_squarefreeness_tests":p**d,
        "squarefree_candidates_fully_evaluated":len(candidates),
        "public_candidate_evaluations":p*len(candidates),
        "nearest_hamming_distance":nearest,
        "nearest_candidate_count":len(nearest_candidates),
        "nearest_candidates_ascending":nearest_candidates,
        "maximum_absolute_public_correlation_exact":str(Fraction(maximum_absolute,p)),
        "maximum_public_projection_score":(maximum_absolute/p)**2,
        "maximum_absolute_correlation_candidate_count":len(physical_best),
        "maximum_absolute_correlation_candidates_ascending":physical_best,
        "maximum_absolute_correlation_candidates_signed_numerators":physical_signed_numerators,
    },candidates


def virtual_analysis(Q):
    p = int(Q.base_ring().order())
    d = int(Q.degree())
    field,ring = Q.base_ring(),Q.parent()
    q = tuple(int(Q[i]) for i in range(d+1))
    U = math.prod(p**int(f.degree())-1 for f,m in Q.factor())
    assert Q.is_monic() and Q.is_squarefree()
    virtual = np.zeros((p,)*(d+1),dtype=complex)
    remainder_signs = {
        c:chi(Q.resultant(ring(list(c))))
        for c in itertools.product(range(p),repeat=d)
    }
    for label in itertools.product(range(p),repeat=d+1):
        remainder = tuple((label[i]-label[d]*q[i])%p for i in range(d))
        virtual[label] = remainder_signs[remainder]/math.sqrt(p*U)
    assert np.count_nonzero(virtual) == p*U
    virtual_prob = np.abs(normalized_fft(virtual))**2
    H = [label for label in itertools.product(range(p),repeat=d+1) if sum(a*b for a,b in zip(q,label))%p == 0]
    assert sum(virtual_prob[label] > TOLERANCE for label in H) == U
    assert abs(float(sum(virtual_prob[label] for label in H))-1) < TOLERANCE
    basis = matrix(field,[q]).right_kernel().basis_matrix()
    intrinsic = list(itertools.product(range(p),repeat=d))
    embedding = {c:tuple(int(a) for a in vector(field,c)*basis) for c in intrinsic}
    hyperplanes = []
    for normal in canonical_projective_labels(p,d):
        W = [embedding[c] for c in intrinsic if sum(a*b for a,b in zip(c,normal))%p == 0]
        outside = [embedding[c] for c in intrinsic if sum(a*b for a,b in zip(c,normal))%p]
        mass = float(sum(virtual_prob[label] for label in W))
        assert mass <= p**(d-1)/U+TOLERANCE
        hyperplanes.append((mass,outside))
    return p,d,q,U,virtual,H,hyperplanes


def inspect_family(Q,name):
    p,d,q,U,virtual,H,hyperplanes = virtual_analysis(Q)
    field = Q.base_ring()
    clean_table = [chi(Q(field(x))) or 1 for x in range(p)]
    roots = [x for x in range(p) if Q(field(x)) == 0]
    nonroots = [x for x in range(p) if x not in roots]
    masks = [("empty",[]),("first_nonroot",nonroots[:1]),
             ("first_two_nonroots",nonroots[:2]),("first_root",roots[:1])]
    assert roots and len(nonroots)>=2
    n = len(nonroots)
    N0 = (p-1)*math.comb(p,d)
    Ngood = (p-1)*math.comb(n,d)
    gamma_clean = Ngood/math.sqrt(N0*p*U)
    rows = []
    for mask_name,mask in masks:
        observed = [value*(-1 if x in mask else 1) for x,value in enumerate(clean_table)]
        # Acquire all p F bits and exhaust the public squarefree family first.
        classical,candidates = table_only_attack(p,d,observed)
        true_row = next(row for row in candidates if row[0] == q)
        wrong = [row for row in candidates if row[0] != q]
        classical["true_candidate_hamming_distance_analysis_only"] = true_row[1]
        classical["true_candidate_is_hamming_nearest_analysis_only"] = true_row[1] == classical["nearest_hamming_distance"]
        classical["maximum_wrong_public_projection_score_analysis_only"] = max((row[2]/p)**2 for row in wrong)
        classical["maximum_wrong_absolute_correlation_exact_analysis_only"] = str(Fraction(max(abs(row[2]) for row in wrong),p))
        assert true_row[1] == len(mask)
        if (p,d,mask_name) == (11,3,"empty"):
            complement = next(row for row in candidates if row[0] == (8,3,4,1))
            assert complement[2] == -p  # exact global-phase ambiguity

        # Native source sees this single fixed sign table only, through F(x).
        def fixed_oracle(x):
            return observed[x]
        source,_,_,diagnostic_calls = cleaned_source(p,d,fixed_oracle)
        B = sum(x in nonroots for x in mask)
        E = Fraction(sum((-1)**j*choose(B,j)*choose(n-B,d-j) for j in range(d+1)),choose(n,d))
        mu = Fraction(n-2*B,n)
        prediction = chi(field(-1))**d*gamma_clean*float(E)
        overlap = np.vdot(virtual,source)
        assert abs(overlap-prediction) < TOLERANCE
        if mask_name == "first_root":
            assert E == 1 and B == 0
            assert abs(overlap-chi(field(-1))**d*gamma_clean) < TOLERANCE
        if (p,d,B) == (7,3,1):
            assert E == 0 and mu**d == Fraction(8,27)
            assert abs(overlap) < TOLERANCE

        probability = np.abs(normalized_fft(source))**2
        inlier_mass = float(sum(probability[label] for label in H))
        assert inlier_mass+TOLERANCE >= abs(overlap)**2
        escapes,bounds = [],[]
        for Wmass,outside in hyperplanes:
            escape = float(sum(probability[label] for label in outside))
            bound = max(0,abs(overlap)-math.sqrt(Wmass))**2
            assert escape+TOLERANCE >= bound
            escapes.append(escape)
            bounds.append(bound)
        uniform_bound = max(0,abs(prediction)-math.sqrt(max(mass for mass,_ in hyperplanes)))**2
        conservative_bound = max(0,abs(prediction)-math.sqrt(p**(d-1)/U))**2
        actual_copy = np.array(observed,dtype=float)/math.sqrt(p)
        candidate_copy = np.array(clean_table,dtype=float)/math.sqrt(p)
        projection = float(abs(np.vdot(candidate_copy,actual_copy))**2)
        projection_prediction = (1-2*len(mask)/p)**2
        assert abs(projection-projection_prediction)<TOLERANCE
        rows.append({
            "mask_name":mask_name,"mask":mask,"fixed_observed_table":observed,
            "classical_first_attack":classical,"B_nonroot_errors":B,
            "exact_signed_distinct_subset_average_Ed":str(E),
            "incorrect_IID_replacement_mu_to_d":str(mu**d),
            "signed_virtual_overlap_prediction":prediction,
            "signed_virtual_overlap_observed_real":float(overlap.real),
            "signed_virtual_overlap_imaginary_abs":float(abs(overlap.imag)),
            "overlap_prediction_abs_error":float(abs(overlap-prediction)),
            "source_constructor_diagnostic_oracle_calls":diagnostic_calls,
            "actual_H_inlier_mass":inlier_mass,
            "proper_H_hyperplanes_checked":len(hyperplanes),
            "minimum_actual_H_minus_W_mass":min(escapes),
            "uniform_escape_bound_from_max_actual_virtual_Wmass":uniform_bound,
            "uniform_escape_bound_from_coarse_virtual_W_bound":conservative_bound,
            "uniform_bound_vacuous":conservative_bound == 0,
            "individual_W_bounds_vacuous_numerically":sum(int(bound<TOLERANCE) for bound in bounds),
            "correct_candidate_projection_observed":projection,
            "correct_candidate_projection_prediction":projection_prediction,
        })
    return {
        "name":name,"p":p,"d":d,"Q_ascending_coefficients":list(q),
        "roots_analysis_only":roots,"n_nonroots":n,"N0":N0,"Ngood":Ngood,"U":U,
        "gamma_clean":gamma_clean,"maximum_virtual_W_mass":max(mass for mass,_ in hyperplanes),
        "squarefree_large_prime_threshold_max_128_d_factorial_256_d_squared":max(128*math.factorial(d),256*d*d),
        "large_prime_threshold_satisfied":False,"controls":rows,
    }


def main():
    R11 = PolynomialRing(GF(11),"X")
    X = R11.gen()
    R7 = PolynomialRing(GF(7),"X")
    Y = R7.gen()
    assert (X**2+1).is_irreducible() and (Y**2+1).is_irreducible()
    prescribed = [(X*(X-1),"p11_split_quadratic"),
                  (X*(X**2+1),"p11_mixed_cubic"),
                  (Y*(Y**2+1),"p7_mixed_cubic")]
    families = [inspect_family(Q,name) for Q,name in prescribed]
    artifact = {
        "scope":"Twelve predeclared fixed corrupted-table finite controls; exact Sage field/combinatorial algebra and floating normalized NumPy FFT. No quantum execution, asymptotic success claim, noise grid, or mixed-device-noise model.",
        "access":"Source receives F(x) only through unchanged imported cleaned_source. Each F is one fixed table lambda_Q with the stated deterministic sign flips. Q, roots and virtual resultant are analysis-only. Classical table-only attack uses p F bits and explicitly charged candidate work.",
        "fourier":"Unchanged imported normalized_fft, np.fft.fftn(norm=ortho), negative exponent, ascending coefficients. Virtual state chi(resultant(Q,R))/sqrt(p*U), analysis only.",
        "overlap":"Signed overlap chi(-1)^d*gamma_clean*E_d with E_d exact without-replacement subset parity. mu^d is an explicitly incorrect IID replacement control.",
        "escape":"For every proper hyperplane W<H, test mass(H minus W)>=max(0,abs(overlap)-sqrt(virtualmass(W)))^2. All large-prime theorem thresholds fail here; no success claim follows.",
        "physical_phase":"Projection scores square absolute public correlation; phase vectors differing globally by minus one are physically identical. Small examples need not provide a statistical verification gap.",
        "old_consecutive_verifier_counterexample":"With any nonempty prescribed mask of size m<p, the true per-test projection s=(1-2m/p)^2 is below 1. Requiring all K independent tests to pass accepts with probability s^K, tending to zero. This is not a valid robust verifier.",
        "families":families,"all_assertions_passed":True,
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(artifact,indent=2)+"\n")
    for family in families:
        for row in family["controls"]:
            print(json.dumps({"family":family["name"],"mask":row["mask_name"],"E":row["exact_signed_distinct_subset_average_Ed"],"mu_to_d":row["incorrect_IID_replacement_mu_to_d"],"nearest":row["classical_first_attack"]["nearest_hamming_distance"],"nearest_count":row["classical_first_attack"]["nearest_candidate_count"],"true_projection":row["correct_candidate_projection_observed"],"max_wrong_projection":row["classical_first_attack"]["maximum_wrong_public_projection_score_analysis_only"],"escape_bound":row["uniform_escape_bound_from_coarse_virtual_W_bound"]}))


if __name__ == "__main__":
    main()
