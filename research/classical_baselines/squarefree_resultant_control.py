#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Three predeclared finite squarefree controls; no quantum execution/proof."""

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


def table_only_attack(p, d, trit_table, padded_table):
    """Classical attack takes the two observed tables, never the secret Q."""
    field = GF(p)
    ring = PolynomialRing(field, "X")
    X = ring.gen()
    trit_matches = []
    padded_matches = []
    padded_factor_degrees = []
    squarefree_checked = 0
    for coefficients in itertools.product(range(p), repeat=d):
        candidate = X**d + ring(list(coefficients))
        if not candidate.is_squarefree():
            continue
        squarefree_checked += 1
        candidate_trit = [chi(candidate(field(x))) for x in range(p)]
        candidate_padded = [1 if entry == 0 else entry for entry in candidate_trit]
        if candidate_trit == trit_table:
            trit_matches.append(list(coefficients) + [1])
        if candidate_padded == padded_table:
            padded_matches.append(list(coefficients) + [1])
            padded_factor_degrees.append(sorted(int(f.degree()) for f, _ in candidate.factor()))
    assert squarefree_checked == p**d - p**(d-1)
    return {
        "trit_table": trit_table,
        "padded_table_zero_maps_to_plus_one": padded_table,
        "native_queries_per_access_model": p,
        "monic_candidates_squarefreeness_tested": p**d,
        "squarefree_candidates_fully_evaluated": squarefree_checked,
        "public_candidate_evaluations": p*squarefree_checked,
        "trit_matching_candidate_count": len(trit_matches),
        "padded_matching_candidate_count": len(padded_matches),
        "trit_matching_candidates_ascending": trit_matches,
        "padded_matching_candidates_ascending": padded_matches,
        "padded_matching_candidate_factor_degrees": padded_factor_degrees,
        "trit_exact_roots": [x for x, entry in enumerate(trit_table) if entry == 0],
        "scope": "p point queries in each stated access model, followed by exhaustive degree-d squarefree candidate work; no poly(log p) classical claim. Trit zeros expose exactly the linear factors. Padded bits alone do not expose zeros.",
    }


def inspect(Q, name):
    p = int(Q.base_ring().order())
    d = int(Q.degree())
    ring = Q.parent()
    field = Q.base_ring()
    assert Q.is_monic() and Q.is_squarefree()

    # First operation: complete native classical tables, then candidate attack.
    trit_table = [chi(Q(field(x))) for x in range(p)]
    padded_table = [1 if entry == 0 else entry for entry in trit_table]
    classical = table_only_attack(p, d, trit_table, padded_table)
    q = tuple(int(Q[i]) for i in range(d+1))
    assert list(q) in classical["trit_matching_candidates_ascending"]
    assert list(q) in classical["padded_matching_candidates_ascending"]

    def padded_oracle(x):
        value = chi(Q(field(x)))
        return 1 if value == 0 else value

    # Imported source routine remains unchanged and receives only this oracle.
    source, _, source_signs, diagnostic_calls = cleaned_source(p, d, padded_oracle)
    factors = list(Q.factor())
    degrees = [int(f.degree()) for f, multiplicity in factors]
    assert all(multiplicity == 1 for _, multiplicity in factors)
    U = math.prod(p**degree - 1 for degree in degrees)
    r = len(classical["trit_exact_roots"])
    N0 = (p-1)*math.comb(p,d)
    Ngood = (p-1)*math.comb(p-r,d)
    overlap_squared_prediction = Ngood**2/(N0*p*U)
    virtual = np.zeros_like(source)
    signs = {}
    for coefficients in itertools.product(range(p), repeat=d):
        signs[coefficients] = chi(Q.resultant(ring(list(coefficients))))
    for label in itertools.product(range(p), repeat=d+1):
        remainder = tuple((label[i]-label[d]*q[i]) % p for i in range(d))
        virtual[label] = signs[remainder]/math.sqrt(p*U)
    assert np.count_nonzero(virtual) == p*U
    assert abs(float(np.vdot(virtual,virtual).real)-1) < TOLERANCE
    assert abs(float(np.vdot(source,source).real)-1) < TOLERANCE
    good_labels = [label for label in source_signs if abs(virtual[label]) > 0]
    assert len(good_labels) == Ngood
    phase_error = max(abs(virtual[label]*math.sqrt(p*U) - chi(field(-1))**d*source_signs[label]) for label in good_labels)
    assert phase_error < TOLERANCE
    overlap_squared = float(abs(np.vdot(virtual,source))**2)
    assert abs(overlap_squared-overlap_squared_prediction) < TOLERANCE

    virtual_prob = np.abs(normalized_fft(virtual))**2
    actual_prob = np.abs(normalized_fft(source))**2
    labels = list(itertools.product(range(p), repeat=d+1))
    H = [label for label in labels if sum(a*b for a,b in zip(q,label)) % p == 0]
    H_set = set(H)
    support = [label for label in labels if virtual_prob[label] > TOLERANCE]
    assert len(support) == U and all(label in H_set for label in support)
    flat_error = max(abs(float(virtual_prob[label])-1/U) for label in support)
    leakage = float(sum(virtual_prob[label] for label in labels if label not in H_set))
    assert max(flat_error, leakage) < TOLERANCE
    zero = (0,)*(d+1)
    incorrect_all_H_flat_error = max(abs(float(virtual_prob[label])-1/(p**d-1)) for label in H if label != zero)
    assert incorrect_all_H_flat_error > 1e-5
    assert p**d-1 > U
    inlier = float(sum(actual_prob[label] for label in H))
    assert inlier+TOLERANCE >= overlap_squared_prediction

    basis = matrix(field,[q]).right_kernel().basis_matrix()
    intrinsic = list(itertools.product(range(p),repeat=d))
    embedding = {c:tuple(int(a) for a in vector(field,c)*basis) for c in intrinsic}
    normals = canonical_projective_labels(p,d)
    virtual_W_masses = []
    escape_masses = []
    for normal in normals:
        W = [embedding[c] for c in intrinsic if sum(a*b for a,b in zip(c,normal)) % p == 0]
        outside_W = [embedding[c] for c in intrinsic if sum(a*b for a,b in zip(c,normal)) % p]
        virtual_W_masses.append(float(sum(virtual_prob[label] for label in W)))
        escape_masses.append(float(sum(actual_prob[label] for label in outside_W)))
    W_bound = p**(d-1)/U
    escape_bound = max(0,Ngood/math.sqrt(N0*p*U)-math.sqrt(W_bound))**2
    assert max(virtual_W_masses) <= W_bound+TOLERANCE
    assert min(escape_masses)+TOLERANCE >= escape_bound
    return {
        "name":name,"p":p,"d":d,"Q_ascending_coefficients":list(q),
        "irreducible_factor_degrees":degrees,"classical_first_attack":classical,
        "r_linear_roots":r,"N0":N0,"Ngood":Ngood,"U":U,
        "virtual_normalization_squared":p*U,
        "source_constructor_diagnostic_oracle_calls":diagnostic_calls,
        "good_support_phase_max_error":float(phase_error),
        "overlap_squared_prediction":overlap_squared_prediction,
        "overlap_squared_observed":overlap_squared,
        "virtual_fourier_support_count":len(support),
        "virtual_fourier_support_flatness_max_error":flat_error,
        "virtual_fourier_off_H_mass":leakage,
        "nonzero_H_zero_frequencies":p**d-1-U,
        "incorrect_all_nonzero_H_flatness_assertion_rejected":True,
        "incorrect_all_nonzero_H_flatness_max_error":incorrect_all_H_flat_error,
        "actual_H_mass":inlier,"proper_H_hyperplanes_checked":len(normals),
        "maximum_virtual_W_mass":max(virtual_W_masses),"virtual_W_mass_upper_bound":W_bound,
        "minimum_actual_H_minus_W_mass":min(escape_masses),
        "escape_lower_bound":escape_bound,"escape_lower_bound_vacuous":escape_bound==0,
    }


def main():
    ring = PolynomialRing(GF(11),"X")
    X = ring.gen()
    assert (X**2+1).is_irreducible()
    cases = [(X*(X-1),"fully_split_quadratic"),
             (X*(X**2+1),"mixed_cubic"),
             (X*(X-1)*(X-2),"fully_split_cubic")]
    rows = [inspect(Q,name) for Q,name in cases]
    ring5 = PolynomialRing(GF(5),"X")
    x = ring5.gen()
    f1,f2 = x**2+2,x**2+3
    assert f1.is_irreducible() and f2.is_irreducible()
    Q1,Q2 = f1**2,f2**2
    tables = [[chi(Q(a)) for a in GF(5)] for Q in (Q1,Q2)]
    assert Q1 != Q2 and tables[0] == tables[1] == [1]*5
    counterexample = {
        "p":5,"degree":4,"Q1_ascending":list(map(int,Q1.list())),
        "Q2_ascending":list(map(int,Q2.list())),
        "quadratic_factors_both_irreducible":True,
        "trit_tables":tables,"padded_tables":tables,
        "distinct_monic_polynomials_identical_oracles":True,
        "scope":"Without squarefreeness exact reconstruction is information-theoretically impossible even with the full trit table in this predeclared family.",
    }
    artifact = {
        "scope":"Three fixed finite Sage algebra checks and floating NumPy FFT checks, not exact complex arithmetic, an asymptotic proof, a noisy-source claim, or quantum algorithm execution.",
        "actual_source":"Imported cleaned_source is unchanged; it receives only p,d,padded point oracle lambda_Q (chi with zero mapped to +1). Source predicts the normalized distinct-root coefficient state; clean erasure and quantum resources are not executed.",
        "virtual_analysis_only":"chi(resultant(Q,R))/sqrt(p*U), U=product_factors(p^degree-1), over ascending degree<=d coefficient labels. Q and factors used only for analysis, never as native source advice.",
        "fourier_convention":"Imported normalized_fft is unchanged: normalized np.fft.fftn(norm=ortho), exponent -2*pi*i*coefficient.dot(frequency)/p.",
        "hyperplane_convention":"H=coeff(Q)^perp; every maximal proper W<H is enumerated through intrinsic coordinates. Escape is mass in H minus W, excluding off-H outcomes.",
        "tolerance":TOLERANCE,"cases":rows,"nonsquarefree_counterexample":counterexample,
        "all_assertions_passed":True,
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(artifact,indent=2)+"\n")
    for row in rows:
        print(json.dumps({key:row[key] for key in ("name","overlap_squared_observed","virtual_fourier_support_count","minimum_actual_H_minus_W_mass","escape_lower_bound")} | {"trit_matches":row["classical_first_attack"]["trit_matching_candidate_count"],"padded_matches":row["classical_first_attack"]["padded_matching_candidate_count"]}))
    print("nonsquarefree indistinguishability counterexample passed")


if __name__ == "__main__":
    main()
