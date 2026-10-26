"""Complete classical search on a chosen reciprocal-affine pencil.

Polynomial-degree rational elimination, not a general codeword solver or
classical hardness certificate. See research/RECIPROCAL_AFFINE_PENCIL.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from flint import __version__ as flint_version, fq_default_poly_ctx

from theorems.balanced_codeword_filter import integer, reciprocal_trace, trace_mask
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.parity_block_usd_prange import affine_system


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/reciprocal_affine_pencil.json"


def _input(bits, points, dimension, slopes, offsets, targets):
    integer(bits, 2, 256, "field bits")
    points, slopes, offsets, targets = map(tuple, (points, slopes, offsets, targets))
    if not len(points) == len(slopes) == len(offsets) == len(targets):
        raise ValueError("one slope, offset and target per evaluation point required")
    integer(dimension, 1, len(points)-1, "native parity-check dimension")
    for value in points+slopes+offsets:
        integer(value, 0, (1 << bits)-1, "field element")
    if len(set(points)) != len(points):
        raise ValueError("distinct evaluation points required")
    for value in targets:
        integer(value, 0, 1, "target bit")
    return points, slopes, offsets, targets


def pencil_word(bits, slopes, offsets, parameter):
    """x_i=inv0(a_i*u+c_i); zeros are legal native coordinates."""
    u = element(bits, parameter)
    values = [element(bits, a)*u+element(bits, c) for a, c in zip(slopes, offsets)]
    return tuple(encoded(y**-1) if y != 0 else 0 for y in values)


def _native_valid(bits, points, dimension, word, targets):
    return (all(reciprocal_trace(bits, x) == b for x, b in zip(word, targets))
            and all(sum((element(bits, a)**j*element(bits, x)
                         for a, x in zip(points, word)), field(bits).zero()) == 0
                    for j in range(dimension)))


def _zero_free_solution(system):
    return sum(row[-1] << next(j for j, x in enumerate(row[:-1]) if x)
               for row in system["rref"] if any(row[:-1]))


def _polynomial_certificate(bits, points, dimension, slopes, offsets):
    ring = fq_default_poly_ctx(field(bits))
    variable = ring.gen()
    groups = {}
    constant_indices = []
    for i, (a, c) in enumerate(zip(slopes, offsets)):
        if a == 0:
            constant_indices.append(i)
        else:
            pole = encoded(element(bits, c)/element(bits, a))
            groups.setdefault(pole, []).append(i)
    denominator = ring.one()
    for pole in groups:
        denominator *= variable+element(bits, pole)
    quotients = {pole: denominator.exact_division(variable+element(bits, pole)) for pole in groups}
    constant_word = tuple(encoded(element(bits, c)**-1) if a == 0 and c != 0 else 0
                          for a, c in zip(slopes, offsets))
    numerators, residues, constants = [], [], []
    for j in range(dimension):
        constant = sum((element(bits, points[i])**j*element(bits, constant_word[i])
                        for i in constant_indices), field(bits).zero())
        row = {pole: sum((element(bits, points[i])**j/element(bits, slopes[i])
                          for i in indices), field(bits).zero()) for pole, indices in groups.items()}
        numerator = denominator*constant
        for pole, residue in row.items():
            numerator += quotients[pole]*residue
        numerators.append(numerator)
        residues.append(row)
        constants.append(constant)
    identity = all(p.is_zero() for p in numerators)
    grouped_identity = (all(x == 0 for x in constants)
                        and all(x == 0 for row in residues for x in row.values()))
    if identity != grouped_identity:
        raise ArithmeticError("partial-fraction identity certificate disagrees")
    if identity and any(len(indices) < dimension+1 for indices in groups.values()):
        raise ArithmeticError("nonzero kernel support violates the Vandermonde distance")
    return ring, groups, denominator, numerators, identity


def check_root_completeness(polynomial, roots, bits):
    """Certify ALL distinct base-field roots, including inseparable inputs.

    X^q is computed modulo the input by repeated powering, never expanded.
    Failure is an error, not an empty-pencil research result.
    """
    if polynomial.is_zero():
        raise ValueError("zero polynomial requires the affine-family branch")
    ring = fq_default_poly_ctx(field(bits))
    variable = ring.gen()
    root_product = ring.one()
    for root in roots:
        root_product *= variable-root
    linear_part = (ring.one() if polynomial.degree() == 0 else
                   polynomial.gcd(variable.pow_mod(1 << bits, polynomial)-variable).monic())
    if root_product != linear_part:
        raise ArithmeticError("incomplete or invalid finite-field root list")
    return linear_part


def solve_pencil(bits, points, dimension, slopes, offsets, targets):
    """Return every valid parameter, or an exact affine description if identical.

    Choosing the pencil is NOT solved here. Empty means no point ON THIS
    PENCIL. Factorization is delegated to FLINT, with completeness checked.
    """
    points, slopes, offsets, targets = _input(bits, points, dimension, slopes, offsets, targets)
    equations = [(trace_mask(bits, a), b ^ int(element(bits, c).trace()))
                 for a, c, b in zip(slopes, offsets, targets)]
    system = affine_system(equations, bits)
    result = {"input": {"bits": bits, "points": points, "dimension": dimension,
                         "slopes": slopes, "offsets": offsets, "targets": targets,
                         "field_modulus": sum(int(c) << j for j, c in enumerate(field(bits).modulus().coeffs()))},
              "scope": "ONE_SUPPLIED_RECIPROCAL_AFFINE_PENCIL_ONLY",
              "status": "NO_NATIVE_POINT_ON_THIS_PENCIL", "witness": None,
              "trace_system": system, "solution_parameter_count": 0,
              "parameters": [], "formal_code_identity": None,
              "root_completeness_checked": False, "field_table_enumerated": False,
              "full_native_problem_decided": False}
    if not system["consistent"]:
        result["reason"] = "INCONSISTENT_TRACE_LINEAR_SYSTEM"
        return result

    ring, groups, denominator, numerators, identity = _polynomial_certificate(
        bits, points, dimension, slopes, offsets)
    result.update(formal_code_identity=identity, distinct_poles=len(groups),
                  pole_groups=[{"pole": pole, "indices": indices} for pole, indices in groups.items()],
                  denominator_coefficients=[encoded(x) for x in denominator.coeffs()],
                  numerator_coefficients=[[encoded(x) for x in p.coeffs()] for p in numerators])
    if identity:
        parameter = _zero_free_solution(system)
        word = pencil_word(bits, slopes, offsets, parameter)
        if not _native_valid(bits, points, dimension, word, targets):
            raise ArithmeticError("identity-pencil native witness failed")
        result.update(status="VERIFIED_CLASSICAL_WITNESS", witness=word, parameter=parameter,
                      parameters=None, solution_parameter_count=1 << len(system["free"]),
                      reason="ALL_PARAMETERS_IN_RECORDED_TRACE_AFFINE_SYSTEM",
                      target_image_rank=system["rank"])
        return result

    gcd = ring.zero()
    for numerator in numerators:
        gcd = gcd.gcd(numerator)
    gcd = gcd.monic()
    roots = [] if gcd.degree() == 0 else gcd.roots(multiplicities=False)
    linear_part = check_root_completeness(gcd, roots, bits)
    regular = sorted({encoded(root) for root in roots}-set(groups))
    exceptional = sorted(groups)
    valid = []
    for parameter in sorted(set(regular+exceptional)):
        word = pencil_word(bits, slopes, offsets, parameter)
        if _native_valid(bits, points, dimension, word, targets):
            valid.append(parameter)
    result.update(parameters=valid, solution_parameter_count=len(valid),
                  gcd_coefficients=[encoded(x) for x in gcd.coeffs()], gcd_degree=gcd.degree(),
                  base_field_linear_part=[encoded(x) for x in linear_part.coeffs()],
                  regular_parameters_checked=regular, exceptional_parameters_checked=exceptional,
                  root_completeness_checked=True, parameter_checks=len(regular)+len(exceptional),
                  reason="COMPLETE_REGULAR_ROOTS_AND_ALL_POLES_CHECKED")
    if valid:
        result.update(status="VERIFIED_CLASSICAL_WITNESS", parameter=valid[0],
                      witness=pencil_word(bits, slopes, offsets, valid[0]))
    return result


def identity_family_budget(bits, length, dimension):
    """Fixed, formally code-valued, arbitrary-parameter inverse-affine families.

    This target-image count does NOT cover target-dependent families, general
    rational numerators, or families satisfying parity only at selected points.
    """
    integer(bits, 2, 256, "field bits")
    integer(length, 2, 1 << bits, "length")
    integer(dimension, 1, length-1, "parity-check dimension")
    groups = length//(dimension+1)
    rank = min(length, bits*groups)
    return {"bits": bits, "length": length, "dimension": dimension,
            "minimum_nonconstant_group_size": dimension+1,
            "max_nonconstant_groups": groups, "target_image_rank_upper": rank,
            "uniform_target_hit_probability_upper_power_of_two": rank-length,
            "scope": "ONE_FIXED_FORMAL_INVERSE_AFFINE_FAMILY_NOT_ADAPTIVE_ATTACKS",
            "classical_hardness_established": False}


def report():
    line = (1, 2, 4, 7)
    slopes = tuple(encoded(element(3, v)**-1) for v in line)
    controls = [solve_pencil(3, (0, 1, 2, 3), 1, slopes, (0,)*4, (0,)*4),
                solve_pencil(3, (0, 1, 2), 1, (1, 1, 0), (0, 1, 1), (0, 1, 1)),
                solve_pencil(61, (0, 1), 1, (1, 0), (0, 1), (1, 1)),
                solve_pencil(5, tuple(range(6)), 2, (1, 2, 3, 4, 5, 6), (0,)*6,
                             tuple(int(element(5, a).trace()) for a in (1, 2, 3, 4, 5, 6)))]
    return {"status": "EXACT_RESTRICTED_CLASSICAL_ATTACK_AND_RIGIDITY_REVIEW_PENDING",
            "speedup_established": False, "general_classical_solver": False,
            "classical_hardness_established": False, "flint_version": flint_version,
            "factorization_runtime": "IMPORTED_FINITE_FIELD_BACKEND_NO_LOCAL_WORST_CASE_CLOCK",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256((ROOT / "research/RECIPROCAL_AFFINE_PENCIL.md").read_bytes()).hexdigest(),
            "controls": controls,
            "fixed_identity_family_budgets": [identity_family_budget(n, n*n, n*n//8)
                                               for n in (17, 31, 61)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = report()
    if args.write:
        REPORT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"],
                      "solution_parameter_counts": [x["solution_parameter_count"] for x in result["controls"]],
                      "report": str(REPORT) if args.write else None}, indent=2))


if __name__ == "__main__":
    main()
