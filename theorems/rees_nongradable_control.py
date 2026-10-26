"""A nongradable Lazard input for the Rees HSP reduction.

The Dixmier--Lister algebra is prior art. Integer row certificates, not a
characteristic-zero assertion or sampled derivations, certify D(L)<=L'.
This is a public algebraic falsifier control, not a quantum receiver.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations
import json
from math import lcm
from pathlib import Path

from flint import fmpq_mat, fmpz_mat

from theorems.rees_hsp_reduction import _tensor_algebra, _units, make_rees_cover


# Zero-based form of the known eight-dimensional Dixmier--Lister law.
BRACKETS = ((0, 1, 4, 1), (0, 2, 5, 1), (0, 3, 6, 1),
            (0, 4, 7, -1), (1, 2, 7, 1), (1, 3, 5, 1),
            (1, 5, 6, -1), (2, 3, 4, -1), (2, 4, 6, -1),
            (3, 5, 7, -1))


def integer_tensor():
    tensor = [[[0]*8 for _ in range(8)] for _ in range(8)]
    for i, j, k, value in BRACKETS:
        tensor[i][j][k] = value
        tensor[j][i][k] = -value
    return tuple(tuple(tuple(row) for row in plane) for plane in tensor)


def derivation_equations(tensor):
    """Rows of D[e_i,e_j]-[De_i,e_j]-[e_i,De_j]=0.

    Matrix variables are row-major D[output,input], acting on columns.
    This includes ALL endomorphisms, not just diagonal or inner ones.
    """
    n = len(tensor)
    rows = []
    for i, j in combinations(range(n), 2):
        for k in range(n):
            row = [0]*(n*n)
            for a in range(n):
                row[k*n+a] += tensor[i][j][a]
                row[a*n+i] -= tensor[a][j][k]
                row[a*n+j] -= tensor[i][a][k]
            rows.append(tuple(row))
    return tuple(rows)


@lru_cache(maxsize=1)
def integer_derivation_certificate():
    """Return exact integer row identities forcing the top four D rows zero.

    Each identity is multiplier*e_entry = sum coefficient*A[equation].
    All multipliers divide six. Thus the implication survives reduction
    at EVERY p>3, without assuming that a rational nullspace specializes.
    """
    rows = derivation_equations(integer_tensor())
    count, width = len(rows), len(rows[0])
    augmented = [list(row)+[int(i == j) for j in range(count)]
                 for i, row in enumerate(rows)]
    reduced, _ = fmpq_mat(augmented).rref()
    certificates = []
    for entry in range(32):
        row_index = next((i for i in range(count)
                          if all(reduced[i, j] == int(j == entry)
                                 for j in range(width))), None)
        if row_index is None:
            raise ArithmeticError("not every derivation has image in L prime")
        coefficients = [reduced[row_index, width+j] for j in range(count)]
        multiplier = lcm(*(int(x.denominator) for x in coefficients))
        combination = tuple((j, int(x*multiplier)) for j, x in enumerate(coefficients) if x)
        certificate = {"entry": entry, "multiplier": multiplier,
                       "equation_combination": combination}
        if not verify_row_certificate(rows, certificate):
            raise ArithmeticError("integer derivation row identity failed")
        if 6 % multiplier:
            raise ArithmeticError("unexpected exceptional characteristic")
        certificates.append(certificate)
    smith = fmpz_mat(rows).snf()
    invariant_factors = tuple(int(smith[i, i]) for i in range(width) if smith[i, i])
    return {"equation_count": count, "variable_count": width,
            "integer_row_certificates": tuple(certificates),
            "nonzero_smith_factors": invariant_factors,
            "excluded_primes": (2, 3),
            "all_derivations_map_into_derived_for_p_gt_3": True,
            "derivation_nilpotency_index_upper_bound": 3}


def verify_row_certificate(rows, certificate):
    """Replay a certificate with integer arithmetic, independent of rref/SNF."""
    width = len(rows[0])
    entry, multiplier = certificate["entry"], certificate["multiplier"]
    if (type(entry) is not int or not 0 <= entry < width
            or type(multiplier) is not int or multiplier <= 0):
        return False
    total = [0]*width
    for equation, coefficient in certificate["equation_combination"]:
        if (type(equation) is not int or not 0 <= equation < len(rows)
                or type(coefficient) is not int):
            return False
        for j, value in enumerate(rows[equation]):
            total[j] += coefficient*value
    return all(value == multiplier*int(j == entry) for j, value in enumerate(total))


def dixmier_lister_algebra(p, copies=1):
    if type(p) is not int or p <= 3:
        raise ValueError("this Lazard nongradability control requires prime p>3")
    if type(copies) is not int or copies < 1:
        raise ValueError("a positive integer direct-sum multiplicity is required")
    tensor = integer_tensor()
    blocks = {}
    for block in range(copies):
        offset = 8*block
        for i in range(8):
            for j in range(8):
                if any(tensor[i][j]):
                    row = [0]*(8*copies)
                    row[offset:offset+8] = [x % p for x in tensor[i][j]]
                    blocks[offset+i, offset+j] = tuple(row)
    return _tensor_algebra(p, 8*copies, blocks)


def _image(matrix, vector, p):
    return tuple(sum(a*b for a, b in zip(row, vector)) % p for row in matrix)


def check_public_cover(p, copies=1):
    """All-basis Lie-map checks; no hidden subgroup is a compiler input."""
    source = dixmier_lister_algebra(p, copies)
    units = _units(source.dimension)
    cover = make_rees_cover(source, units)
    lifted_units = _units(cover.dimension)
    evaluation_checks = 0
    dilation_checks = 0
    for left, right in combinations(lifted_units, 2):
        bracket = cover.algebra.bracket(left, right)
        for point in cover.points:
            if cover.evaluate(bracket, point) != source.bracket(
                    cover.evaluate(left, point), cover.evaluate(right, point)):
                raise ArithmeticError("evaluation is not a Lie homomorphism")
            evaluation_checks += 1
        if cover.dilate(bracket, 2) != cover.algebra.bracket(
                cover.dilate(left, 2), cover.dilate(right, 2)):
            raise ArithmeticError("Rees dilation is not an automorphism")
        dilation_checks += 1
    # The apparent lower-central weights do NOT grade the original algebra.
    weights = (1, 1, 1, 1, 2, 2, 3, 3)*copies
    naive = lambda vector: tuple(x*pow(2, w, p) % p for x, w in zip(vector, weights))
    left = naive(source.bracket(units[0], units[3]))
    right = source.bracket(naive(units[0]), naive(units[3]))
    if left == right:
        raise ArithmeticError("expected nongraded bracket falsifier disappeared")
    # No positive grading does NOT mean no nonidentity finite automorphisms.
    signs = (1, -1, 1, -1, -1, 1, -1, -1)*copies
    involution = tuple(tuple(signs[i]*int(i == j) for j in range(source.dimension))
                       for i in range(source.dimension))
    if any(_image(involution, source.bracket(a, b), p) != source.bracket(
            _image(involution, a, p), _image(involution, b, p))
           for a, b in combinations(units, 2)):
        raise ArithmeticError("finite involution control failed")
    return {"prime": p, "prime_bits": p.bit_length(), "direct_sum_copies": copies,
            "source_dimension": source.dimension, "class": cover.class_bound,
            "lower_central_dimensions": cover.dimensions,
            "cover_dimension": cover.dimension,
            "evaluation_basis_pairs_checked": evaluation_checks,
            "dilation_basis_pairs_checked_at_scale_2": dilation_checks,
            "naive_dilation_of_bracket_e1_e4": left,
            "bracket_of_naively_dilated_e1_e4": right,
            "nonidentity_order_two_automorphism_exists": True,
            "queries_per_lifted_source": len(cover.points),
            "hidden_advice_used_by_public_compiler": False}


def build_report():
    return {"status": "NONGRADABLE_INPUT_CERTIFICATE_UNDER_REVIEW",
            "known_algebra_source": "https://arxiv.org/pdf/1308.2396#page=9",
            "derivation_certificate": integer_derivation_certificate(),
            "controls": [check_public_cover(p, copies) for p, copies in
                         ((5, 1), (7, 1), (43, 1), (2**127-1, 1), (7, 2), (43, 4))],
            "claim": "Positive Rees cover does not require an original positive grading.",
            "full_quantum_instrument_executed_on_this_input": False,
            "arbitrary_hsp_recovery_implemented": False,
            "independent_review": False, "novelty_established": False,
            "speedup_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    content = json.dumps(build_report(), indent=2)+"\n"
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/rees_nongradable_control.json"
        path.write_text(content)
        print(path)
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
