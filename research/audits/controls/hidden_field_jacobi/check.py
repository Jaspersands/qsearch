#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""One exact Sage control of the specified three-copy Jacobi instrument.

Only q=9,25 and the identity/shear maps are examined.  This is a finite
falsifier control, not evidence for an all-parameter theorem.  No secret
field coordinate is used by a proposed decoder: this file is a validator.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

from sage.all import CyclotomicField, GF, PolynomialRing, QQ, matrix, version


def rational_string(value):
    value = QQ(value)
    return str(value)


def check_case(p, shear):
    q = p * p
    prime_field = GF(p)
    ring = PolynomialRing(prime_field, "z")
    z = ring.gen()
    modulus = z * z + (1 if p == 3 else 2)
    assert modulus.is_irreducible()
    field = GF(q, name="a", modulus=modulus)
    a = field.gen()
    linear_map = matrix(prime_field, [[1, int(shear)], [0, 1]])
    assert linear_map.det() != 0

    # Coordinates and dual labels use the public dot product over F_p.
    coordinates = [(i, j) for j in range(p) for i in range(p)]
    index = {v: i for i, v in enumerate(coordinates)}
    add = [[index[((x[0] + y[0]) % p, (x[1] + y[1]) % p)]
            for y in coordinates] for x in coordinates]
    neg = [index[((-x[0]) % p, (-x[1]) % p)] for x in coordinates]
    sub = [[add[x][neg[y]] for y in range(q)] for x in range(q)]

    def character(value):
        if value == 0:
            return 0
        power = value ** ((q - 1) // 2)
        assert power in (field(1), field(-1))
        return 1 if power == 1 else -1

    h = [character(field((i + int(shear) * j) % p) + field(j) * a)
         for i, j in coordinates]
    h_identity = [character(field(i) + field(j) * a)
                  for i, j in coordinates]
    assert h[0] == 0 and sum(v * v for v in h) == q - 1
    changed_entries = sum(x != y for x, y in zip(h, h_identity))
    assert changed_entries > 0 if shear else changed_entries == 0

    cyclotomic = CyclotomicField(p)
    zeta = cyclotomic.gen()
    conjugation = cyclotomic.hom([zeta ** (-1)], cyclotomic)
    powers = [zeta ** k for k in range(p)]

    # Direct exact DFT of the actual sign vector.  No Gauss identity is
    # used to populate this table.
    fourier = []
    for t in coordinates:
        fourier.append(sum((h[x] * powers[(t[0] * v[0] + t[1] * v[1]) % p]
                            for x, v in enumerate(coordinates)), cyclotomic(0)))
    fourier_square = [QQ(value * conjugation(value)) for value in fourier]
    assert fourier_square[0] == 0
    assert all(value == q for value in fourier_square[1:])

    # The sum-coordinate Fourier transform turns the direct triple
    # convolution into F(t+b)F(t+c)F(t).  Parseval preserves each measured
    # (b,c) marginal.  These exact rational probabilities therefore equal
    # the instrument with the s register retained, not measured.
    denominator = QQ(q ** 3 * (q - 1) ** 3)
    probability = []
    strata = {}
    full_outcomes_checked = 0
    for b in range(q):
        row = []
        for c in range(q):
            norm_sum = QQ(0)
            for t in range(q):
                amplitude_numerator = (fourier[t] * fourier[add[t][b]]
                                       * fourier[add[t][c]])
                square = QQ(amplitude_numerator * conjugation(amplitude_numerator))
                actual = square / denominator
                allowed = t != 0 and add[t][b] != 0 and add[t][c] != 0
                expected_full = QQ(1) / (q - 1) ** 3 if allowed else QQ(0)
                assert actual == expected_full, (p, shear, b, c, t, actual)
                norm_sum += square
                full_outcomes_checked += 1
            actual_pair = norm_sum / denominator
            d = len({0, neg[b], neg[c]})
            expected_pair = QQ(q - d) / (q - 1) ** 3
            assert actual_pair == expected_pair, (p, shear, b, c, actual_pair)
            row.append(actual_pair)
            key = str(d)
            strata.setdefault(key, {"number_of_pairs": 0,
                                    "probability_per_pair": rational_string(actual_pair)})
            strata[key]["number_of_pairs"] += 1
        probability.append(row)
    assert sum(sum(row) for row in probability) == 1

    # Independently compute the zero-branch convolution in the ORIGINAL
    # additive coordinates using only integer additions and products.
    convolution2 = [sum(h[x] * h[sub[s][x]] for x in range(q)) for s in range(q)]
    convolution3 = [sum(convolution2[x] * h[sub[s][x]] for x in range(q))
                    for s in range(q)]
    epsilon = character(field(-1))
    expected2 = [epsilon * (q - 1 if s == 0 else -1) for s in range(q)]
    expected3 = [epsilon * q * value for value in h]
    assert convolution2 == expected2
    assert convolution3 == expected3
    zero_squared_norm = sum(value * value for value in convolution3)
    zero_success = QQ(zero_squared_norm) / (q ** 2 * (q - 1) ** 3)
    assert zero_success == QQ(1) / (q - 1) ** 2
    assert zero_success == probability[0][0]
    # This equality of unnormalized vectors proves the returned pure state
    # is h/sqrt(q-1), up to the displayed global sign.
    assert convolution3 == [epsilon * q * value for value in h]

    return {
        "p": p, "q": q, "name": "shear" if shear else "identity",
        "field_modulus": str(modulus), "public_basis": ["1", "a"],
        "linear_map_rows": [[1, int(shear)], [0, 1]],
        "linear_map_determinant": int(linear_map.det()),
        "changed_character_entries_vs_identity": changed_entries,
        "coordinate_and_label_order": [list(v) for v in coordinates],
        "unpadded_character_vector": h,
        "unpadding_success_per_copy": rational_string(QQ(q - 1) / q),
        "direct_cyclotomic_fourier_values": [str(value) for value in fourier],
        "direct_fourier_squared_magnitudes": [rational_string(v) for v in fourier_square],
        "all_three_register_probabilities_checked": full_outcomes_checked,
        "all_pair_marginals_checked": q * q,
        "pair_probability_matrix": [[rational_string(v) for v in row]
                                    for row in probability],
        "pair_strata_by_distinct_exclusions": strata,
        "total_pair_probability": "1",
        "direct_convolution2": convolution2,
        "direct_convolution3": convolution3,
        "zero_branch_squared_unnormalized_norm": zero_squared_norm,
        "zero_branch_success_conditional_on_three_unpadded_copies": rational_string(zero_success),
        "input_return_unnormalized_multiplier": epsilon * q,
        "normalized_input_return_global_sign": epsilon,
        "all_checks_passed": True,
    }


def main():
    start = time.monotonic()
    cases = [check_case(p, shear) for p in (3, 5) for shear in (False, True)]
    for first, second in ((cases[0], cases[1]), (cases[2], cases[3])):
        assert first["pair_probability_matrix"] == second["pair_probability_matrix"]
    script = Path(__file__).resolve()
    result = {
        "status": "PASS",
        "scope": "Exactly q=9,25; identity and one shear each; finite falsifier control only.",
        "source_normalization": "Each input copy is h/sqrt(q-1), after the public nonzero filter.",
        "method": "Exact cyclotomic DFT/convolution/Parseval for the full law; independent integer zero-branch convolutions.",
        "python_executable": sys.executable,
        "sage_version": str(version()),
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "cases": cases,
        "cross_map_pair_laws_identical": True,
        "total_pair_marginals_checked": sum(c["all_pair_marginals_checked"] for c in cases),
        "total_three_register_probabilities_checked": sum(c["all_three_register_probabilities_checked"] for c in cases),
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    output = script.with_name("result.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    summary = {k: v for k, v in result.items() if k != "cases"}
    summary["cases"] = [{k: c[k] for k in (
        "p", "q", "name", "changed_character_entries_vs_identity",
        "all_pair_marginals_checked", "all_three_register_probabilities_checked",
        "pair_strata_by_distinct_exclusions", "zero_branch_success_conditional_on_three_unpadded_copies",
        "input_return_unnormalized_multiplier", "all_checks_passed")}
        for c in cases]
    summary["full_result_path"] = str(output)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
