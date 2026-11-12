#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""One fixed exhaustive second-moment transcription control, not a proof.

Enumerates all 216 equiprobable IID balanced-halfset tables over GF(4).
Run with /opt/anaconda3/envs/qsearch-cas/bin/python; writes only sibling JSON.
"""
from collections import Counter
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

from sage.all import GF, QQ, binomial


def main():
    q, m, k = 4, 3, 2
    field = GF(q, name="a", modulus="primitive")
    elements = [field.from_integer(i) for i in range(q)]
    labels = {x: i for i, x in enumerate(elements)}
    points = elements[1:]
    halfsets = list(combinations(range(q), q // 2))
    evaluations = [[labels[c0 + c1 * point] for point in points]
                   for c0, c1 in product(elements, repeat=k)]
    assert len(evaluations) == q ** k == 16
    distribution = Counter()
    tables_checked = 0
    for rows in product(halfsets, repeat=m):
        Z = sum(all(value in row for value, row in zip(values, rows))
                for values in evaluations)
        distribution[Z] += 1
        tables_checked += 1
    assert tables_checked == len(halfsets) ** m == 216
    EZ = sum(QQ(z * count) / tables_checked for z, count in distribution.items())
    EZ2 = sum(QQ(z * z * count) / tables_checked for z, count in distribution.items())
    predicted_EZ = QQ(q) ** k / QQ(2) ** m
    a = QQ(q - 2) / (q - 1)
    terms = [binomial(m, j) * a ** (m - j) * (2 - a) ** j *
             QQ(q) ** (-min(j, k)) for j in range(m + 1)]
    predicted_ratio = sum(terms)
    variance = EZ2 - EZ ** 2
    excess = variance / EZ ** 2
    excess_terms = [binomial(m, j) * a ** (m - j) * (2 - a) ** j *
                    (QQ(q) ** (-k) - QQ(q) ** (-j))
                    for j in range(k + 1, m + 1)]
    independent_evaluations_ratio = sum(
        binomial(m, j) * a ** (m - j) * (2 - a) ** j * QQ(q) ** (-j)
        for j in range(m + 1))
    probability_zero = QQ(distribution[0]) / tables_checked
    upper = QQ(2) ** m / QQ(q) ** k
    assert EZ == predicted_EZ
    assert EZ2 / EZ ** 2 == predicted_ratio
    assert independent_evaluations_ratio == 1
    assert excess == sum(excess_terms)
    assert probability_zero <= excess <= upper
    result = {
        "status": "PASS_FINITE_EXACT",
        "purpose": "Transcription/control check of section 6 (MAXIMUM), not its proof",
        "arithmetic": "Sage GF(4) and QQ; exact exhaustive enumeration",
        "fixture": {"q": q, "m": m, "k": k,
                    "field_modulus": str(field.modulus()),
                    "labels": "polynomial-basis integer bit encoding",
                    "evaluation_point_labels": [labels[x] for x in points],
                    "possible_halfsets": [list(row) for row in halfsets],
                    "table_count": tables_checked,
                    "table_probability": str(QQ(1) / tables_checked),
                    "codewords_per_table": len(evaluations)},
        "Z_distribution": {str(z): {"table_count": count,
                                    "probability": str(QQ(count) / tables_checked)}
                           for z, count in sorted(distribution.items())},
        "moments": {"E_Z": str(EZ), "predicted_E_Z": str(predicted_EZ),
                    "E_Z_squared": str(EZ2), "E_Z_squared_over_E_Z_square": str(EZ2 / EZ ** 2),
                    "a": str(a), "formula_terms_j_0_to_m": [str(t) for t in terms],
                    "formula_ratio": str(predicted_ratio), "variance": str(variance),
                    "variance_over_E_Z_square": str(excess),
                    "exact_excess_terms_j_k_plus_1_to_m": [str(t) for t in excess_terms],
                    "ratio_with_min_j_k_replaced_by_j": str(independent_evaluations_ratio)},
        "bounds": {"Pr_Z_zero": str(probability_zero),
                   "variance_over_E_Z_square": str(excess),
                   "two_to_m_over_q_to_k": str(upper),
                   "Pr_Z_zero_le_variance_ratio_le_upper": True},
        "checks": {"all_216_tables_enumerated": True,
                   "all_16_codewords_checked_per_table": True,
                   "E_Z_identity": True, "second_moment_identity": True,
                   "variance_excess_identity": True},
        "claim_gates": {"finite_control_only": True, "proof_of_general_identity": False,
                        "asymptotic_claim": False, "algorithm": False,
                        "efficient_perfect_word_search": False, "speedup": False,
                        "separation": False, "quantum_execution": False,
                        "provisional_note_promoted": False},
        "control_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "result": str(path),
                      "E_Z": str(EZ), "second_moment_ratio": str(predicted_ratio),
                      "variance_ratio": str(excess), "Pr_Z_zero": str(probability_zero)}))


if __name__ == "__main__":
    main()
