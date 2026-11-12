#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""One fixed exact GF(8) control; finite identities, not an asymptotic test.

Run from the repository root with /opt/anaconda3/envs/qsearch-cas/bin/python.
Only result.json beside this file is written. No parameter sweep or optimizer.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import random
import sys

from sage.all import GF, QQ, PolynomialRing, identity_matrix, matrix, vector


def rational(x):
    return str(QQ(x))


def main():
    q, m, k, seed = 8, 7, 2, 20261107
    field = GF(q, name="a", modulus="primitive")
    # Integer labels are polynomial-basis bit encodings, not residues mod 8.
    elements = [field.from_integer(i) for i in range(q)]
    labels = {x: i for i, x in enumerate(elements)}
    points = elements[1:]
    rng = random.Random(seed)
    halfset_labels = [sorted(rng.sample(range(q), q // 2)) for _ in points]
    halfsets = [{elements[j] for j in row} for row in halfset_labels]
    ring = PolynomialRing(field, "X")
    X = ring.gen()
    coefficients = [(c0, c1) for c0 in elements for c1 in elements]
    codewords = [c0 + c1 * X for c0, c1 in coefficients]
    index = {pair: i for i, pair in enumerate(coefficients)}
    D = len(codewords)
    assert D == 64
    H = vector(QQ, [sum(c(a) in row for a, row in zip(points, halfsets))
                    for c in codewords])
    G = vector(QQ, [QQ(1) / 2 + h / (2 * m) for h in H])
    P0 = matrix(QQ, D, D)
    # Here A has exactly one anchor. Every primitive (anchor,z) is retained,
    # including the seven separate z=0 addresses that land on the diagonal.
    for i, c in enumerate(codewords):
        for anchor in points:
            delta = X - anchor
            for z in elements:
                target = c + z * delta
                j = index[(target[0], target[1])]
                P0[i, j] += QQ(1) / (m * q)
    one = vector(QQ, [1] * D)
    s, b, M = QQ(1) / 3, QQ(1) / 9, 3
    nu = 1 + b
    P = (1 - s) * identity_matrix(QQ, D) + s * P0
    alpha = QQ(k - 1) / m
    r = 1 - alpha
    mu = sum(G) / D
    drift0 = P0 * H - (alpha * H + (1 - alpha) * m / 2 * one)
    drift_lazy = P * G - ((1 - s * r) * G + s * r * mu * one)
    assert P0 == P0.transpose() and P == P.transpose()
    assert P0 * one == one and P * one == one
    assert min(P0.list()) >= 0 and min(P.list()) >= 0
    assert all(x == 0 for x in drift0) and all(x == 0 for x in drift_lazy)
    assert mu == QQ(3) / 4

    # Build the Born law directly from the averaged matrix polynomial.
    T = (P + b * matrix.diagonal(G)) / nu
    powers = [identity_matrix(QQ, D)]
    for _ in range(M):
        powers.append(powers[-1] * T)
    C = sum(powers, matrix(QQ, D, D)) / (M + 1)
    u = one / 8  # sqrt(pi) is rational for D=64.
    amplitude = C * u
    born_mass = vector(QQ, [a * a for a in amplitude])
    born = born_mass / sum(born_mass)

    # Independently sum all killed paths by the primitive-step recursion.
    # With nu=1+b and w_j=1/(M+1), degree J is uniform on {0,...,M}.
    survival_by_degree = [one]
    for _ in range(M):
        previous = survival_by_degree[-1]
        nxt = []
        for x in range(D):
            walk_survival = sum(P[x, y] * previous[y] for y in range(D))
            nxt.append((walk_survival + b * G[x] * previous[x]) / (1 + b))
        survival_by_degree.append(vector(QQ, nxt))
    survival = sum(survival_by_degree, vector(QQ, D)) / (M + 1)
    paired = vector(QQ, [sum(survival_by_degree[j][x] * survival_by_degree[l][x]
                            for j in range(M + 1) for l in range(M + 1)) /
                         (M + 1) ** 2 for x in range(D)])
    assert paired == vector(QQ, [p * p for p in survival])
    acceptance = sum(paired) / D
    paired_law = paired / sum(paired)
    assert paired_law == born
    assert amplitude == survival / 8
    assert acceptance == sum(born_mass)
    assert all(powers[j] * one == survival_by_degree[j] for j in range(M + 1))

    g0 = QQ(1) / 2
    t0 = (1 + b * g0) / (1 + b)
    lower, upper = t0 ** (2 * M), t0 ** (-2 * M)
    likelihood = D * born
    assert t0 ** M <= min(survival) <= max(survival) <= 1
    assert acceptance >= lower
    assert all(lower <= ratio <= upper for ratio in likelihood)
    tv = sum(abs(p - QQ(1) / D) for p in born) / 2
    # Entirely rational stronger-to-compute envelope from the survival bounds.
    assert tv <= upper - 1

    # Deliberate bug control: use ONE shared degree J for the independent paths.
    # Its survival is E_J[p_J(x)^2], not (E_J[p_J(x)])^2.
    shared_mass = vector(QQ, [sum(v[x] ** 2 for v in survival_by_degree) / (M + 1)
                              for x in range(D)])
    shared_law = shared_mass / sum(shared_mass)
    shared_difference = [i for i in range(D) if shared_law[i] != born[i]]
    shared_tv = sum(abs(x - y) for x, y in zip(shared_law, born)) / 2

    # Call the actual repository baseline once. Its prime-field contract is
    # not GF(8): never interpret bit labels as arithmetic mod 8.
    repo = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(repo))
    import numpy as np
    from tools.dqi_screen.prange import prange_restarts
    B_labels = np.array([[1, labels[a]] for a in points], dtype=int)
    try:
        actual_prange = prange_restarts(B_labels, halfset_labels, q,
                                       restarts=1, seed=seed)
    except ValueError as error:
        actual_prange = {"status": "API_MISMATCH", "error": str(error),
                         "explanation": "Repository API is prime-field arithmetic modulo q; native field is GF(2^3)."}
    else:
        raise AssertionError("Prime-only API unexpectedly accepted q=8; review native semantics")

    # Native comparator: exact law of ONE uniform two-row information-set
    # completion, uniformly choosing an accepted target at each chosen row.
    prange_count = [0] * D
    total = 0
    for i in range(m):
        for j in range(i + 1, m):
            for y_i in sorted(halfsets[i], key=lambda x: labels[x]):
                for y_j in sorted(halfsets[j], key=lambda x: labels[x]):
                    slope = (y_j - y_i) / (points[j] - points[i])
                    constant = y_i - slope * points[i]
                    pos = index[(constant, slope)]
                    assert codewords[pos](points[i]) in halfsets[i]
                    assert codewords[pos](points[j]) in halfsets[j]
                    assert H[pos] >= k
                    prange_count[pos] += 1
                    total += 1
    assert total == 336
    prange_law = vector(QQ, [QQ(n) / total for n in prange_count])
    baseline_rng = random.Random(seed)
    selected_rows = sorted(baseline_rng.sample(range(m), k))
    targets = [elements[baseline_rng.choice(halfset_labels[i])] for i in selected_rows]
    i, j = selected_rows
    slope = (targets[1] - targets[0]) / (points[j] - points[i])
    constant = targets[0] - slope * points[i]
    witness_index = index[(constant, slope)]
    witness_score = int(H[witness_index])
    witness_values = [labels[codewords[witness_index](a)] for a in points]
    assert witness_score == sum(v in row for v, row in zip(witness_values, halfset_labels))

    def score_law(law):
        return {str(h): rational(sum(law[x] for x in range(D) if H[x] == h))
                for h in range(m + 1)}

    result = {
        "status": "PASS_FINITE_EXACT", "arithmetic": "Sage GF(8) and QQ; no floating identities",
        "fixture": {"q": q, "m": m, "k": k, "seed": seed, "codeword_count": D,
                    "halfset_generation": "random.Random(seed).sample(range(q),q//2), independently per row",
                    "field_modulus": str(field.modulus()), "field_labels": "polynomial-basis integer bit encoding",
                    "evaluation_point_labels": [labels[a] for a in points], "halfsets": halfset_labels},
        "parameters": {"s": rational(s), "b": rational(b), "M": M, "nu": rational(nu),
                       "G": "1/2+H/(2m)", "degree_weights": ["1/4"] * 4},
        "identities": {"symmetric_P0_and_lazy": True, "stochastic_P0_and_lazy": True,
                       "P0_H_affine_drift_all_64": True, "lazy_G_affine_drift_all_64": True,
                       "alpha": rational(alpha), "r": rational(r), "mu": rational(mu),
                       "P0_diagonal": rational(P0[0, 0]), "lazy_diagonal": rational(P[0, 0]),
                       "paired_killed_paths_equal_Born_all_64": True,
                       "survival_equals_matrix_polynomial_all_64": True},
        "filter": {"acceptance": rational(acceptance), "survival_min": rational(min(survival)),
                   "survival_max": rational(max(survival)), "t0": rational(t0),
                   "likelihood_lower_bound": rational(lower), "likelihood_upper_bound": rational(upper),
                   "likelihood_min": rational(min(likelihood)), "likelihood_max": rational(max(likelihood)),
                   "all_64_likelihood_bounds_pass": True, "TV_from_uniform": rational(tv),
                   "rational_TV_envelope": rational(upper - 1),
                   "score_law": score_law(born), "mean_score": rational(H.dot_product(born))},
        "shared_degree_variant": {"equals_Born": shared_law == born,
                                  "differing_codeword_count": len(shared_difference),
                                  "TV_from_Born": rational(shared_tv),
                                  "acceptance": rational(sum(shared_mass) / D),
                                  "fixture_not_retuned": True,
                                  "first_difference": None if not shared_difference else {
                                      "index": shared_difference[0],
                                      "Born": rational(born[shared_difference[0]]),
                                      "shared": rational(shared_law[shared_difference[0]])}},
        "actual_repository_Prange": actual_prange,
        "native_GF8_Prange_completion": {"restarts": 1, "exact_random_choices": total,
                                        "score_law": score_law(prange_law),
                                        "mean_score": rational(H.dot_product(prange_law)),
                                        "witness": {"row_indices": selected_rows,
                                                    "target_labels": [labels[y] for y in targets],
                                                    "coefficient_labels_low_first": [labels[constant], labels[slope]],
                                                    "evaluation_labels": witness_values, "score": witness_score,
                                                    "all_original_rows_verified": True}},
        "uniform": {"score_law": score_law(one / D), "mean_score": rational(sum(H) / D),
                    "max_score": int(max(H))},
        "full_exact_laws": [{"coefficient_labels_low_first": [labels[c0], labels[c1]],
                             "H": int(H[i]), "G": rational(G[i]),
                             "Born": rational(born[i]), "paired_survival": rational(paired[i]),
                             "shared_degree": rational(shared_law[i]),
                             "Prange": rational(prange_law[i])}
                            for i, (c0, c1) in enumerate(coefficients)],
        "claim_gates": {"finite_control_only": True, "asymptotic_claim": False,
                        "generic_OPI_no_go": False, "classical_hardness": False,
                        "separation": False, "quantum_execution": False,
                        "source_parameter_admissibility_certified": False,
                        "provisional_note_promoted": False},
        "control_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    path = Path(__file__).with_name("result.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "result": str(path),
                      "shared_degree_differences": len(shared_difference),
                      "acceptance": rational(acceptance), "Prange_witness_score": witness_score}))


if __name__ == "__main__":
    main()
