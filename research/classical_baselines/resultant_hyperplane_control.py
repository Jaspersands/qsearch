#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Predeclared finite algebra falsifier, not a quantum execution or proof.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python.  Sage supplies the
polynomial rings, irreducibility, resultants, and finite-field linear algebra.
The actual source constructor receives only p, d and a point-character oracle;
the virtual resultant state and secret hyperplane are analysis-only objects.
No larger parameters, random seeds, or selective secrets are admitted.
"""

import itertools
import json
import math
from pathlib import Path

import numpy as np
from sage.all import GF, PolynomialRing, matrix, vector


PARAMETERS = ((5, 2), (7, 3))
TOLERANCE = 2e-11


def chi(value):
    return 0 if value == 0 else (1 if value.is_square() else -1)


def cleaned_source(p, d, oracle):
    """Return coefficient amplitudes using only public arithmetic and oracle(x).

    Ascending coefficients encode a*prod(X-x), with an unordered set of d
    distinct roots and a != 0.  Unique factorization makes the labels distinct.
    The second source deliberately omits chi(a)^d as a negative control.
    """
    field = GF(p)
    ring = PolynomialRing(field, "X")
    X = ring.gen()
    count = (p - 1) * math.comb(p, d)
    source = np.zeros((p,) * (d + 1), dtype=complex)
    omitted = np.zeros_like(source)
    support_signs = {}
    oracle_calls = 0
    for roots in itertools.combinations(range(p), d):
        monic = ring.one()
        phase = 1
        for root in roots:
            monic *= X - field(root)
            phase *= oracle(root)
            oracle_calls += 1
        for leading in range(1, p):
            polynomial = field(leading) * monic
            label = tuple(int(polynomial[i]) for i in range(d + 1))
            assert label not in support_signs
            sign = chi(field(leading)) ** d * phase
            support_signs[label] = sign
            source[label] = sign / math.sqrt(count)
            omitted[label] = phase / math.sqrt(count)
    assert len(support_signs) == count
    return source, omitted, support_signs, oracle_calls


def canonical_projective_labels(p, dimension):
    """One representative of every nonzero scalar class, first nonzero = 1."""
    return [
        label
        for label in itertools.product(range(p), repeat=dimension)
        if any(label) and next(value for value in label if value) == 1
    ]


def normalized_fft(amplitudes):
    # Output[y] = p^(-(d+1)/2) sum_r exp(-2*pi*i*r.dot(y)/p) amplitude[r].
    return np.fft.fftn(amplitudes, norm="ortho")


def inspect_secret(p, d, Q):
    field = Q.base_ring()
    ring = Q.parent()
    q = tuple(int(Q[i]) for i in range(d + 1))

    # Secret evaluation belongs solely to the oracle boundary.  cleaned_source
    # receives neither Q nor its coefficient vector, root, norm, or resultant.
    def oracle(x):
        return chi(Q(field(x)))

    source, omitted, support, oracle_calls = cleaned_source(p, d, oracle)
    total = p * (p**d - 1)
    delta = len(support) / total
    virtual = np.zeros_like(source)
    virtual_signs = {}
    # Sage resultants of all degree<d remainders suffice because Q is monic:
    # resultant(Q,R+cQ)=resultant(Q,R).  This is analysis, never an oracle.
    for remainder in itertools.product(range(p), repeat=d):
        resultant = Q.resultant(ring(list(remainder)))
        virtual_signs[remainder] = chi(resultant)
    for label in itertools.product(range(p), repeat=d + 1):
        remainder = tuple((label[i] - label[d] * q[i]) % p for i in range(d))
        virtual[label] = virtual_signs[remainder] / math.sqrt(total)

    global_sign = chi(field(-1)) ** d
    phase_errors = [
        abs(virtual[label] * math.sqrt(total) - global_sign * sign)
        for label, sign in support.items()
    ]
    assert max(phase_errors) < TOLERANCE
    norm_error = max(abs(float(np.vdot(s, s).real) - 1) for s in (source, virtual, omitted))
    overlap = np.vdot(virtual, source)
    overlap_error = abs(abs(overlap) ** 2 - delta)
    assert norm_error < TOLERANCE and overlap_error < TOLERANCE

    actual_prob = np.abs(normalized_fft(source)) ** 2
    virtual_prob = np.abs(normalized_fft(virtual)) ** 2
    omitted_overlap_squared = float(abs(np.vdot(virtual, omitted)) ** 2)
    zero = (0,) * (d + 1)
    labels = list(itertools.product(range(p), repeat=d + 1))
    H = [label for label in labels if sum(a*b for a, b in zip(q, label)) % p == 0]
    H_set = set(H)
    H_nonzero = [label for label in H if label != zero]
    off_H = [label for label in labels if label not in H_set]
    flat_target = 1 / (p**d - 1)
    flat_error = max(abs(float(virtual_prob[label]) - flat_target) for label in H_nonzero)
    leakage = float(sum(virtual_prob[label] for label in off_H))
    zero_mass = float(virtual_prob[zero])
    assert max(flat_error, leakage, zero_mass) < TOLERANCE
    inlier_mass = float(sum(actual_prob[label] for label in H))
    assert inlier_mass + TOLERANCE >= delta

    # Every maximal proper subspace of H, including all smaller proper
    # subspaces through containment, is tested using intrinsic H coordinates.
    basis = matrix(field, [q]).right_kernel().basis_matrix()
    intrinsic = list(itertools.product(range(p), repeat=d))
    embedding = {
        coefficients: tuple(int(t) for t in vector(field, coefficients) * basis)
        for coefficients in intrinsic
    }
    normals = canonical_projective_labels(p, d)
    bound = max(0.0, math.sqrt(delta) - math.sqrt((p**(d-1)-1)/(p**d-1))) ** 2
    escape_masses = []
    virtual_W_errors = []
    for normal in normals:
        outside_W = [embedding[c] for c in intrinsic if sum(a*b for a,b in zip(c, normal)) % p]
        in_W = [embedding[c] for c in intrinsic if sum(a*b for a,b in zip(c, normal)) % p == 0]
        escape_masses.append(float(sum(actual_prob[label] for label in outside_W)))
        virtual_W_errors.append(abs(float(sum(virtual_prob[label] for label in in_W)) - (p**(d-1)-1)/(p**d-1)))
    assert min(escape_masses) + TOLERANCE >= bound
    assert max(virtual_W_errors) < TOLERANCE

    # Retaining injective source labels gives a diagonal reduced coefficient
    # state.  Each computational basis ket has exactly uniform Fourier law.
    incoherent_fourier = np.zeros_like(actual_prob)
    for label in support:
        basis_ket = np.zeros_like(source)
        basis_ket[label] = 1
        incoherent_fourier += np.abs(normalized_fft(basis_ket)) ** 2 / len(support)
    uniform_error = float(np.max(np.abs(incoherent_fourier - 1/p**(d+1))))
    incoherent_inlier = float(sum(incoherent_fourier[label] for label in H))
    assert uniform_error < TOLERANCE and abs(incoherent_inlier - 1/p) < TOLERANCE
    if d % 2:
        assert omitted_overlap_squared < TOLERANCE

    return {
        "Q_ascending_coefficients": list(q),
        "source_support_size": len(support),
        "diagnostic_oracle_calls_source_constructor": oracle_calls,
        "global_phase_virtual_over_source": global_sign,
        "normalization_max_error": norm_error,
        "split_phase_max_error": float(max(phase_errors)),
        "virtual_overlap_squared": float(abs(overlap)**2),
        "virtual_overlap_squared_error": float(overlap_error),
        "virtual_fourier_nonzero_H_flatness_max_error": float(flat_error),
        "virtual_fourier_off_H_mass": leakage,
        "virtual_fourier_zero_mass": zero_mass,
        "actual_fourier_inlier_mass_H": inlier_mass,
        "proper_H_hyperplanes_checked": len(normals),
        "minimum_actual_mass_H_minus_W": min(escape_masses),
        "maximum_actual_mass_H_minus_W": max(escape_masses),
        "virtual_W_mass_max_error": max(virtual_W_errors),
        "retained_labels_fourier_uniformity_max_error": uniform_error,
        "retained_labels_inlier_mass": incoherent_inlier,
        "omitted_leading_character_virtual_overlap_squared": omitted_overlap_squared,
    }


def main():
    artifact = {
        "scope": "Finite Sage algebra and normalized NumPy Fourier falsifier only; no quantum execution, asymptotic proof, novelty, or classical separation claim.",
        "parameters_predeclared": [list(pair) for pair in PARAMETERS],
        "secret_quantifier": "ALL monic irreducible polynomials of the stated degree over the stated prime field.",
        "actual_access": "cleaned_source(p,d,oracle) uses only point values oracle(x)=chi(Q(x)) and public arithmetic. Coherent label erasure and its resource cost are not executed here.",
        "virtual_analysis_only": "N_Q(R)=chi(resultant(Q,R))/sqrt(p*(p^d-1)), R in F_p^(d+1); no virtual oracle is supplied to the source.",
        "coefficients": "Ascending (constant through degree d). S supported on a*product(X-x), a!=0, distinct unordered roots x in F_p; amplitude chi(a)^d*product(oracle(x))/sqrt((p-1)*binom(p,d)).",
        "fourier_convention": "Normalized np.fft.fftn(norm='ortho'): |r> maps to p^(-(d+1)/2)*sum_y exp(-2*pi*i*r.dot(y)/p)|y>.",
        "hyperplane_convention": "H={y:coeff(Q).dot(y)=0}; test every maximal proper W<H using projective normals in intrinsic H coordinates. Escape means probability of H minus W, excluding off-H outputs.",
        "escape_bound": "max(0,sqrt(delta)-sqrt((p^(d-1)-1)/(p^d-1)))^2, delta=((p-1)*binom(p,d))/(p*(p^d-1)). A zero bound is explicitly vacuous.",
        "negative_controls": {
            "retain_injective_root_leading_labels": "Tracing injective labels yields coefficient-basis dephasing; actual Fourier calculation must be uniform and H-inlier mass 1/p.",
            "omit_chi_leading_to_degree": "For odd d the overlap with the virtual resultant state must vanish. This does not by itself falsify every possible receiver.",
        },
        "tolerance": TOLERANCE,
        "cases": [],
    }
    for p, d in PARAMETERS:
        field = GF(p)
        ring = PolynomialRing(field, "X")
        X = ring.gen()
        secrets = [X**d + ring(list(coefficients)) for coefficients in itertools.product(range(p), repeat=d)]
        secrets = [Q for Q in secrets if Q.is_irreducible()]
        assert len(secrets) == (p**d-p)//d  # both predeclared degrees are prime
        rows = [inspect_secret(p, d, Q) for Q in secrets]
        delta = (p-1)*math.comb(p,d)/(p*(p**d-1))
        escape_bound = max(0.0, math.sqrt(delta)-math.sqrt((p**(d-1)-1)/(p**d-1)))**2
        artifact["cases"].append({
            "p": p, "d": d, "secrets_checked": len(rows),
            "delta": delta, "escape_lower_bound": escape_bound,
            "escape_lower_bound_vacuous": escape_bound == 0,
            "minimum_inlier_mass_over_all_secrets": min(r["actual_fourier_inlier_mass_H"] for r in rows),
            "minimum_H_minus_W_mass_over_all_secrets_and_W": min(r["minimum_actual_mass_H_minus_W"] for r in rows),
            "rows": rows,
        })
        print(json.dumps({"p":p,"d":d,"secrets":len(rows),"delta":delta,"escape_bound":escape_bound,"min_inlier":artifact["cases"][-1]["minimum_inlier_mass_over_all_secrets"],"min_escape":artifact["cases"][-1]["minimum_H_minus_W_mass_over_all_secrets_and_W"]}))
    artifact["all_assertions_passed"] = True
    destination = Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(artifact, indent=2) + "\n")


if __name__ == "__main__":
    main()
