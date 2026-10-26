"""Independent CRT/codimension audit of the Hermite interpolation module.

Uses FLINT polynomials, not the compact producer's incremental interpolation
or row reducer. Dense Hilbert/identity checks are diagnostics, not space bounds.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from math import comb
from pathlib import Path

from flint import fmpz_mod_ctx, fmpz_mod_mat, fmpz_mod_poly_ctx

from theorems.hermite_compact_decoder import CompactHermite, DescendingSystem, module_interpolant
from theorems.hermite_pinned_decoder import canonical, parameters

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/hermite_module_certificate.json"


def local_data(q, ell, order, received):
    canonical(received, (q-1)*ell, q)
    height = ell-order
    return [[[1]+[0]*(height-1)] + [
        [comb(j+u, j)*received[i*ell+j+u] % q for u in range(height)]
        for j in range(order+1)] for i in range(q-1)]


def polynomial_lists(basis):
    return [[[int(c) for c in poly.coeffs()] for poly in row] for row in basis]


def leading_pair(row, shifts):
    active = [(poly.degree()+shift, j) for j, (poly, shift)
              in enumerate(zip(row, shifts)) if not poly.is_zero()]
    if not active:
        raise ValueError("zero module row")
    return max(active)


def crt_reduced_basis(q, ell, order, radius, received):
    spec = parameters(q, ell, order, radius)
    ctx, height, rank = fmpz_mod_poly_ctx(q), ell-order, order+2
    local = local_data(q, ell, order, received)
    modulus, residues = ctx([1]), [ctx([]) for _ in range(rank-1)]
    for a in range(1, q):
        translation, centered = ctx([a, 1]), ctx([-a, 1])
        inverse = modulus.compose(translation).inverse_series_trunc(height)
        for j, residue in enumerate(residues):
            correction = (ctx(local[a-1][j+1])-residue.compose(translation)).mul_low(inverse, height)
            residues[j] = residue+modulus*correction.compose(centered)
        modulus *= centered**height
    basis = [[ctx([]) for _ in range(rank)] for _ in range(rank)]
    basis[0][0] = modulus
    for j, residue in enumerate(residues, 1):
        basis[j][0], basis[j][j] = -residue, ctx([1])
    shifts = [-(spec["k"]-1)]+[-j for j in range(order+1)]
    reductions = 0
    while True:
        labels = [leading_pair(row, shifts) for row in basis]
        pair = next(((i, j) for i in range(rank) for j in range(i+1, rank)
                     if labels[i][1] == labels[j][1]), None)
        if pair is None:
            break
        i, j = pair
        if labels[i] < labels[j]:
            i, j = j, i
        position = labels[i][1]
        shift = basis[i][position].degree()-basis[j][position].degree()
        scalar = int(basis[i][position].leading_coefficient())*pow(
            int(basis[j][position].leading_coefficient()), -1, q) % q
        multiple = ctx([0]*shift+[scalar])
        old = leading_pair(basis[i], shifts)
        basis[i] = [left-multiple*right for left, right in zip(basis[i], basis[j])]
        if leading_pair(basis[i], shifts) >= old:
            raise ArithmeticError("independent row cancellation did not descend")
        reductions += 1
    return {"parameters": spec, "basis": polynomial_lists(basis),
            "shifts": shifts, "reductions": reductions,
            "construction": "CRT triangular basis, then independent FLINT row cancellation"}


def certify_basis(q, ell, order, radius, received, encoded_basis):
    """Full module certificate: local validity, independent leading terms, index."""
    spec = parameters(q, ell, order, radius)
    rank, height, ctx = order+2, ell-order, fmpz_mod_poly_ctx(q)
    if len(encoded_basis) != rank or any(len(row) != rank for row in encoded_basis):
        raise ValueError("square polynomial basis of rank order+2 required")
    for row in encoded_basis:
        for poly in row:
            canonical(poly, len(poly), q)
    basis = [[ctx(poly) for poly in row] for row in encoded_basis]
    shifts = [-(spec["k"]-1)]+[-j for j in range(order+1)]
    local = local_data(q, ell, order, received)
    invalid = []
    for index, row in enumerate(basis):
        for a in range(1, q):
            expression = sum((poly.compose(ctx([a, 1])).mul_low(ctx(y), height)
                              for poly, y in zip(row, local[a-1])), ctx([])).truncate(height)
            if not expression.is_zero():
                invalid.append([index, a])
    zero_rows = [i for i, row in enumerate(basis) if all(poly.is_zero() for poly in row)]
    pairs = [] if zero_rows else [leading_pair(row, shifts) for row in basis]
    distinct = len({position for _, position in pairs}) == rank
    determinant_degree = sum(degree for degree, _ in pairs)-sum(shifts) if distinct else None
    issues = []
    if invalid:
        issues.append("INVALID_LOCAL_INTERPOLATION_CONSTRAINT")
    if not distinct:
        issues.append("NO_DISTINCT_LEADING_POSITION_CERTIFICATE")
    if determinant_degree != spec["constraints"]:
        issues.append("DETERMINANT_CODIMENSION_MISMATCH")
    return {"full_module_certified": not issues, "issues": issues,
            "invalid_row_point_pairs": invalid, "zero_rows": zero_rows,
            "leading_pairs": [list(pair) for pair in pairs],
            "determinant_degree": determinant_degree,
            "required_codimension": spec["constraints"],
            "all_rows_valid_is_sufficient": False}


def dense_interpolation_nullity(q, ell, order, received, bound):
    """Independent coefficient expansion at a bounded shifted degree."""
    spec = parameters(q, ell, order, 0)
    sizes = [max(0, bound+spec["k"])] + [max(0, bound+j+1) for j in range(order+1)]
    width, height = sum(sizes), ell-order
    ctx, local = fmpz_mod_poly_ctx(q), local_data(q, ell, order, received)
    columns = []
    for j, size in enumerate(sizes):
        for degree in range(size):
            monomial = ctx([0]*degree+[1])
            column = []
            for a in range(1, q):
                expanded = monomial.compose(ctx([a, 1])).mul_low(ctx(local[a-1][j]), height)
                column += [int(expanded[t]) for t in range(height)]
            columns.append(column)
    if width == 0:
        return 0
    matrix = fmpz_mod_mat([[column[i] for column in columns]
                          for i in range(spec["constraints"])], fmpz_mod_ctx(q))
    _, rank = matrix.rref()
    return width-rank


def hilbert_checks(q, ell, order, radius, received, basis_info, bounds):
    certificate = certify_basis(q, ell, order, radius, received, basis_info["basis"])
    if not certificate["full_module_certified"]:
        raise ArithmeticError("cannot use an uncertified Hilbert profile")
    records = []
    for bound in bounds:
        predicted = sum(max(0, bound-degree+1) for degree, _ in certificate["leading_pairs"])
        actual = dense_interpolation_nullity(q, ell, order, received, bound)
        if predicted != actual:
            raise ArithmeticError("module completeness disagrees with dense interpolation")
        records.append({"shifted_degree_bound": bound, "module_dimension": predicted,
                        "independent_dense_nullity": actual})
    return records


def dense_identity_space(q, k, pieces, pins, ell):
    """Build Hasse columns as polynomials; never call the production coefficient helper."""
    ctx, operator = fmpz_mod_poly_ctx(q), [fmpz_mod_poly_ctx(q)(p) for p in pieces[1:]]
    columns = [sum((poly.scalar_mul(comb(t, j)).left_shift(t-j)
                    for j, poly in enumerate(operator) if t >= j), ctx([]))
               for t in range(k)]
    height = max([len(pieces[0])]+[poly.degree()+1 for poly in columns])
    rows = [[int(poly[h]) for poly in columns] for h in range(height)]
    rhs = [-pieces[0][h] % q if h < len(pieces[0]) else 0 for h in range(height)]
    for i, values in sorted(pins.items()):
        canonical(values, ell, q)
        expanded = [ctx([0]*t+[1]).compose(ctx([i+1, 1])).truncate(ell) for t in range(k)]
        for j, value in enumerate(values):
            rows.append([int(poly[j]) for poly in expanded])
            rhs.append(value)
    augmented, _ = fmpz_mod_mat([row+[b] for row, b in zip(rows, rhs)], fmpz_mod_ctx(q)).rref()
    pivot_rows = []
    for i in range(augmented.nrows()):
        pivot = next((j for j in range(k) if augmented[i, j]), None)
        if pivot is None and augmented[i, k]:
            return {"consistent": False, "dimension": None, "unique_polynomial": None}
        if pivot is not None:
            pivot_rows.append((i, pivot))
    unique = None
    if len(pivot_rows) == k:
        unique = [0]*k
        for i, pivot in pivot_rows:
            unique[pivot] = int(augmented[i, k])
    return {"consistent": True, "dimension": k-len(pivot_rows), "unique_polynomial": unique}


def native_controls():
    fixture = ROOT / "research/reductions/hermite_compact_decoder.json"
    fixture_bytes = fixture.read_bytes()
    saved = json.loads(fixture_bytes)
    q, ell, order, radius = saved["p"], saved["ell"], 4, saved["guard_radius"]
    code = CompactHermite(q, ell)
    _, received = code.received(saved["public_syndrome"])
    independent = crt_reduced_basis(q, ell, order, radius, received)
    certificate = certify_basis(q, ell, order, radius, received, independent["basis"])
    original = module_interpolant(q, ell, order, radius, received)
    same_profile = sorted(certificate["leading_pairs"]) == sorted(original["basis_leading_pairs"])
    if not certificate["full_module_certified"] or not same_profile:
        raise ArithmeticError("independent native module/profile check failed")
    a = original["parameters"]["a"]
    hilbert = hilbert_checks(q, ell, order, radius, received, independent, [a-1, a, a+1])
    pinned = []
    unpinned = dense_identity_space(q, code.k, original["interpolant"], {}, ell)
    for error, stored in zip(saved["two_errors"], saved["pinned"]):
        pin_values = {}
        transformed = code.transform(error, inverse=True)
        for i in saved["pin_indices"]:
            pin_values[i] = [(transformed[i*ell+j]+received[i*ell+j]) % q for j in range(ell)]
        dense = dense_identity_space(q, code.k, original["interpolant"], pin_values, ell)
        compact = DescendingSystem(q, code.k, original["interpolant"]).solve(pin_values, ell)
        if (dense["unique_polynomial"] != compact["polynomial"]
                or dense["unique_polynomial"] != stored["polynomial"]):
            raise ArithmeticError("dense polynomial-column solver disagrees with compact decoder")
        pinned.append({"dimension": dense["dimension"], "matches_compact_and_saved": True})
    # Multiplying one row preserves every local equation and its leading position,
    # but loses a codimension-one family of valid interpolants.
    incomplete = deepcopy(independent["basis"])
    ctx = fmpz_mod_poly_ctx(q)
    incomplete[0] = [[int(c) for c in (ctx(poly)*ctx([-1, 1])).coeffs()]
                     for poly in incomplete[0]]
    negative = certify_basis(q, ell, order, radius, received, incomplete)
    if negative["full_module_certified"] or negative["invalid_row_point_pairs"]:
        raise ArithmeticError("incomplete valid submodule negative control failed")
    return {"status": "INDEPENDENT_MODULE_CERTIFICATE_AND_DENSE_IDENTITY_CHECKS",
            "parameters": original["parameters"],
            "source_fixture": {"path": str(fixture.relative_to(ROOT)),
                               "sha256": hashlib.sha256(fixture_bytes).hexdigest()},
            "public_syndrome": saved["public_syndrome"],
            "received_word": received,
            "independent_basis": independent["basis"],
            "certificate": certificate,
            "matches_original_leading_profile": same_profile,
            "bounded_hilbert_checks": hilbert,
            "identity_unpinned": unpinned, "identity_pinned": pinned,
            "incomplete_submodule_negative": negative,
            "dense_checks_are_diagnostics_not_space_bounds": True,
            "independent_human_proof_review_completed": False,
            "new_quantum_algorithm_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = native_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"output": str(args.output), "status": report["status"],
                      "certificate": report["certificate"],
                      "hilbert": report["bounded_hilbert_checks"]}))


if __name__ == "__main__":
    main()
