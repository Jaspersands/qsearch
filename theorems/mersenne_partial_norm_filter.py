"""Exact filter for balanced low-degree partial-norm factors, not native search.

The bounded reference accepts canonical n=17 or n=19 instances, retaining
their supplied points, targets and checked polynomial-basis modulus. Only
P_j(alpha_i)=P_0(alpha_i)^(2^(j*s)), deg(P_j)<=D, with
D=floor((N-K-1)/4), is tested. Exclusion never means native infeasibility.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from flint import fmpz_mod_poly_ctx, fq_default_ctx, fq_default_poly_ctx

from theorems.balanced_codeword_filter import integer
from theorems.mersenne_reciprocal_curve import native_instance, validate_instance


REPORT = Path(__file__).resolve().parents[1]/"research/classical_baselines/mersenne_partial_norm_filter.json"
SCOPE = "balanced_degree_factors_only"


def fixture_instance():
    """The original n17 all-one fixture, with its explicit original modulus."""
    return {
        "problem_family": "mersenne_reciprocal_trace_v1", "schema_version": 1,
        "bits": 17, "s": 3, "points": list(range(289)), "targets": [1]*289,
        "checks": 36,
        "field_modulus_coefficients": [(0x20009 >> j) & 1 for j in range(18)],
    }


def _validate(instance):
    try:
        n, s, points, targets, checks = validate_instance(instance)
    except (KeyError, TypeError) as error:
        raise ValueError("malformed native instance") from error
    if n not in (17, 19):
        raise ValueError("bounded reference supports only canonical n=17 or n=19")
    if s != (n-3)//4 or len(points) != n*n or checks != n*n//8:
        raise ValueError("canonical native s, N=n*n and K=floor(N/8) required")
    return n, s, points, targets, checks, (len(points)-checks-1)//4


def _digest(instance):
    return hashlib.sha256(json.dumps(instance, sort_keys=True,
                                     separators=(",", ":")).encode("ascii")).hexdigest()


def _encoded(value):
    return sum(int(c) << j for j, c in enumerate(value.to_list()))


def _field_and_product(instance):
    n, _, points, _, _, _ = _validate(instance)
    modulus = fmpz_mod_poly_ctx(2)(instance["field_modulus_coefficients"])
    field = fq_default_ctx(modulus=modulus, fq_type="FQ_NMOD")
    ring = fq_default_poly_ctx(field)
    values = [field([(point >> j) & 1 for j in range(n)]) for point in points]
    product = ring.one()
    for value in values:
        product *= ring.gen()+value
    return field, ring, values, product


def _field_determinant(matrix, field):
    rows = [row[:] for row in matrix]
    determinant = field.one()
    for col in range(len(rows)):
        pivot = next((i for i in range(col, len(rows))
                      if not rows[i][col].is_zero()), None)
        if pivot is None:
            return field.zero()
        rows[col], rows[pivot] = rows[pivot], rows[col]
        lead = rows[col][col]
        determinant *= lead
        rows[col] = [value/lead for value in rows[col]]
        for i in range(col+1, len(rows)):
            coefficient = rows[i][col]
            if not coefficient.is_zero():
                rows[i] = [x+coefficient*y for x, y in zip(rows[i], rows[col])]
    return determinant


def _conjugacy_rank(n, s, length, degree, field, ring, product):
    basis, selected_rows, selected_labels, ranks = {}, [], [], []
    for conjugate in (1, 2, 3):
        frobenius = conjugate*s
        step = pow(ring.gen(), 1 << frobenius, product)
        value, columns = ring.one(), []
        for _ in range(1, degree+1):
            value = value*step % product
            columns.append([value[ell]**(1 << (n-frobenius))
                            for ell in range(degree+1, length)])
        for offset in range(length-degree-1):
            original = [column[offset] for column in columns]
            row = original[:]
            for pivot, previous in basis.items():
                coefficient = row[pivot]
                if not coefficient.is_zero():
                    row = [x+coefficient*y for x, y in zip(row, previous)]
            pivot = next((j for j, value in enumerate(row) if not value.is_zero()), None)
            if pivot is not None:
                inverse = field.one()/row[pivot]
                basis[pivot] = [inverse*value for value in row]
                selected_rows.append(original)
                selected_labels.append([conjugate, degree+1+offset])
        ranks.append(len(basis))
    minor = None
    if len(basis) == degree:
        minor = {
            "rows": selected_labels, "columns": list(range(1, degree+1)),
            "determinant": _encoded(_field_determinant(selected_rows, field)),
        }
    return ranks, minor


def _trace_dependency(points, targets, derivative_powers):
    basis = {}
    for index, original in enumerate(derivative_powers):
        value, subset = original, 1 << index
        for pivot, (previous, mask) in basis.items():
            if (value >> pivot) & 1:
                value ^= previous
                subset ^= mask
        if value:
            basis[value.bit_length()-1] = (value, subset)
        else:
            indices = [j for j in range(len(points)) if (subset >> j) & 1]
            if sum(targets[j] for j in indices) % 2:
                return {
                    "indices": indices, "points": [points[j] for j in indices],
                    "derivative_powers": [derivative_powers[j] for j in indices],
                    "field_sum": 0, "target_sum": 1, "size": len(indices),
                }
    return None


class _BinaryField:
    """Independent polynomial-basis arithmetic for certificate replay."""

    def __init__(self, coefficients):
        self.n = len(coefficients)-1
        self.q = 1 << self.n
        self.modulus = sum(value << j for j, value in enumerate(coefficients))

    def mul(self, left, right):
        result = 0
        while right:
            if right & 1:
                result ^= left
            right >>= 1
            left <<= 1
            if left & self.q:
                left ^= self.modulus
        return result

    def power(self, value, exponent):
        result = 1
        while exponent:
            if exponent & 1:
                result = self.mul(result, value)
            value = self.mul(value, value)
            exponent >>= 1
        return result

    def frobenius(self, value, iterations):
        for _ in range(iterations):
            value = self.mul(value, value)
        return value


def _binary_product(field, points):
    coefficients = [1]
    for point in points:
        updated = [0]*(len(coefficients)+1)
        for j, value in enumerate(coefficients):
            updated[j] ^= field.mul(point, value)
            updated[j+1] ^= value
        coefficients = updated
    return coefficients


def _binary_reduce(field, coefficients, modulus):
    coefficients = coefficients[:]
    nonzero = [(j, value) for j, value in enumerate(modulus[:-1]) if value]
    degree = len(modulus)-1
    for j in range(len(coefficients)-1, degree-1, -1):
        lead = coefficients[j]
        if lead:
            for k, value in nonzero:
                coefficients[j-degree+k] ^= field.mul(lead, value)
    result = coefficients[:degree]
    return result+[0]*(degree-len(result))


def _binary_multiply_mod(field, left, right, modulus):
    product = [0]*(len(left)+len(right)-1)
    right_terms = [(j, value) for j, value in enumerate(right) if value]
    for i, first in enumerate(left):
        if first:
            for j, second in right_terms:
                product[i+j] ^= field.mul(first, second)
    return _binary_reduce(field, product, modulus)


def _binary_minor(field, product, degree, s, labels):
    length = len(product)-1
    by_conjugate = {}
    for row_index, (conjugate, ell) in enumerate(labels):
        by_conjugate.setdefault(conjugate, []).append((row_index, ell))
    matrix = [[0]*degree for _ in labels]
    for conjugate, selected in by_conjugate.items():
        step = [0, 1]
        # Modular squaring keeps this polynomial in n, never in 2^(j*s).
        for _ in range(conjugate*s):
            squared = [0]*(2*len(step)-1)
            for j, value in enumerate(step):
                squared[2*j] = field.mul(value, value)
            step = _binary_reduce(field, squared, product)
        value = [1]+[0]*(length-1)
        for k in range(degree):
            value = _binary_multiply_mod(field, value, step, product)
            for row_index, ell in selected:
                matrix[row_index][k] = field.frobenius(value[ell], field.n-conjugate*s)
    determinant = 1
    for col in range(degree):
        pivot = next((i for i in range(col, degree) if matrix[i][col]), None)
        if pivot is None:
            return 0
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        lead = matrix[col][col]
        determinant = field.mul(determinant, lead)
        inverse = field.power(lead, field.q-2)
        row = [field.mul(value, inverse) for value in matrix[col]]
        matrix[col] = row
        for i in range(col+1, degree):
            coefficient = matrix[i][col]
            if coefficient:
                for j in range(col, degree):
                    matrix[i][j] ^= field.mul(coefficient, row[j])
    return determinant


def verify_exclusion_certificate(instance, certificate):
    """Recompute both certificates with bit-polynomial arithmetic, not FLINT.

    Validation uses the existing native schema. Arithmetic replay does not
    call the producer, use its ranks, or trust stored derivative powers.
    Malformed, mismatched and non-exclusion certificates return False.
    """
    try:
        n, s, points, targets, _, degree = _validate(instance)
        if type(certificate) is not dict or set(certificate) != {
            "schema_version", "instance_sha256", "degree_bound", "rank_minor", "trace_dependency"
        }:
            return False
        integer(certificate["schema_version"], 1, 1, "certificate schema")
        integer(certificate["degree_bound"], degree, degree, "balanced degree")
        if certificate["instance_sha256"] != _digest(instance):
            return False
        minor, dependency = certificate["rank_minor"], certificate["trace_dependency"]
        if type(minor) is not dict or set(minor) != {"rows", "columns", "determinant"}:
            return False
        if (type(minor["columns"]) is not list or len(minor["columns"]) != degree
                or type(minor["rows"]) is not list or len(minor["rows"]) != degree):
            return False
        for expected, actual in enumerate(minor["columns"], 1):
            integer(actual, expected, expected, "minor column")
        for label in minor["rows"]:
            if type(label) is not list or len(label) != 2:
                return False
            integer(label[0], 1, 3, "conjugate")
            integer(label[1], degree+1, len(points)-1, "remainder coefficient")
        if len({tuple(label) for label in minor["rows"]}) != degree:
            return False
        integer(minor["determinant"], 1, (1 << n)-1, "nonzero determinant")
        if type(dependency) is not dict or set(dependency) != {
            "indices", "points", "derivative_powers", "field_sum", "target_sum", "size"
        }:
            return False
        indices = dependency["indices"]
        if type(indices) is not list or not indices or len(indices) > len(points):
            return False
        for index in indices:
            integer(index, 0, len(points)-1, "dependency index")
        if indices != sorted(set(indices)):
            return False
        integer(dependency["size"], len(indices), len(indices), "dependency size")
        integer(dependency["field_sum"], 0, 0, "dependency sum")
        integer(dependency["target_sum"], 1, 1, "contradictory target sum")
        for key in ("points", "derivative_powers"):
            if type(dependency[key]) is not list or len(dependency[key]) != len(indices):
                return False
            for value in dependency[key]:
                integer(value, 0, (1 << n)-1, key)
        if dependency["points"] != [points[i] for i in indices]:
            return False
        if sum(targets[i] for i in indices) % 2 != 1:
            return False
        field = _BinaryField(instance["field_modulus_coefficients"])
        powers, total = [], 0
        for i in indices:
            # Direct pairwise products differ from the producer's A' evaluation.
            derivative = 1
            for j, point in enumerate(points):
                if i != j:
                    derivative = field.mul(derivative, points[i] ^ point)
            value = field.power(derivative, (1 << s)-1)
            powers.append(value)
            total ^= value
        if total or powers != dependency["derivative_powers"]:
            return False
        product = _binary_product(field, points)
        return _binary_minor(field, product, degree, s, minor["rows"]) == minor["determinant"]
    except (KeyError, TypeError, ValueError, IndexError):
        return False


def analyze_balanced_factors(instance):
    """Compute the restriction; emit exclusion only after independent replay."""
    n, s, points, targets, checks, degree = _validate(instance)
    field, ring, values, product = _field_and_product(instance)
    ranks, minor = _conjugacy_rank(n, s, len(points), degree, field, ring, product)
    derivative = product.derivative()
    powers = [_encoded(derivative(point)**((1 << s)-1)) for point in values]
    dependency = _trace_dependency(points, targets, powers)
    certificate = None
    status = "NONCONSTANT_FAMILY_REMAINS" if minor is None else "NO_TRACE_OBSTRUCTION"
    if minor is not None and dependency is not None:
        certificate = {
            "schema_version": 1, "instance_sha256": _digest(instance),
            "degree_bound": degree, "rank_minor": minor, "trace_dependency": dependency,
        }
        if not verify_exclusion_certificate(instance, certificate):
            raise ArithmeticError("partial-norm exclusion failed independent replay")
        status = "BALANCED_FAMILY_EXCLUDED"
    return {
        "instance": deepcopy(instance), "instance_sha256": _digest(instance),
        "scope": SCOPE, "status": status, "degree_bound": degree,
        "product_degree_bound": 4*degree, "native_numerator_degree_max": len(points)-checks-1,
        "rank_by_conjugate": ranks, "coefficient_dimension": degree+1-ranks[-1],
        "rank_minor": minor, "constant_family_trace_dependency": dependency,
        "exclusion_certificate": certificate, "certificate_verified": certificate is not None,
        "native_unsatisfiability_claimed": False, "unrestricted_solver": False,
        "uniform_sampler": False, "universal_collapse_claimed": False,
    }


def build_report(include_n19=False):
    results = [analyze_balanced_factors(fixture_instance())]
    if include_n19:
        results.append(analyze_balanced_factors(native_instance(19)))
    return {
        "schema_version": 1, "scope": SCOPE, "results": results,
        "exclusion_count": sum(row["status"] == "BALANCED_FAMILY_EXCLUDED" for row in results),
        "arithmetic_replay": "independent_binary_polynomial_basis",
        "full_field_enumeration": False, "native_search_performed": False,
    }


def verify_report(report):
    """Replay exclusions independently and recompute any non-exclusion control."""
    try:
        if type(report) is not dict or set(report) != {
            "schema_version", "scope", "results", "exclusion_count", "arithmetic_replay",
            "full_field_enumeration", "native_search_performed"
        }:
            return False
        if (type(report["schema_version"]) is not int or report["schema_version"] != 1
                or report["scope"] != SCOPE or type(report["results"]) is not list
                or not 1 <= len(report["results"]) <= 2
                or report["arithmetic_replay"] != "independent_binary_polynomial_basis"
                or report["full_field_enumeration"] is not False
                or report["native_search_performed"] is not False):
            return False
        integer(report["exclusion_count"], 0, len(report["results"]), "exclusion count")
        exclusions = 0
        for row in report["results"]:
            if row != analyze_balanced_factors(row["instance"]):
                return False
            exclusions += row["status"] == "BALANCED_FAMILY_EXCLUDED"
        return exclusions == report["exclusion_count"]
    except (KeyError, TypeError, ValueError, ArithmeticError):
        return False


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--write", action="store_true", help="write only the owned JSON report")
    actions.add_argument("--verify", action="store_true", help="replay the owned saved JSON report")
    parser.add_argument("--include-n19", action="store_true", help="include the non-collapse control")
    args = parser.parse_args(argv)
    if args.verify:
        if args.include_n19:
            parser.error("--include-n19 applies to report generation, not replay")
        try:
            report = json.loads(REPORT.read_text(encoding="ascii"))
            valid = verify_report(report)
        except (OSError, ValueError):
            valid = False
        print(json.dumps({"verified": valid,
                          "result_count": len(report["results"]) if valid else 0,
                          "exclusion_count": report["exclusion_count"] if valid else 0}))
        return 0 if valid else 1
    report = build_report(args.include_n19)
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="ascii")
        print(json.dumps({"written": str(REPORT), "result_count": len(report["results"]),
                          "exclusion_count": report["exclusion_count"]}))
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
