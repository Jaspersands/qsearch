"""Finite rank certificates for complete local quadratic relation spaces.

Valid identities provide an upper bound on the graph-lift span. Independent
true graph points meeting that bound prove completeness without a field table.
An unsaturated sample is UNKNOWN, not evidence of additional identities.
"""
from hashlib import sha256
import json
from random import Random

from theorems.balanced_codeword_filter import integer, trace_mask
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_algebraic_audit import (
    linearized_rows, monomial_masks, quadratic_lift,
)


def _insert(row, basis):
    while row:
        pivot = row.bit_length()-1
        if pivot not in basis:
            basis[pivot] = row
            return True
        row ^= basis[pivot]
    return False


def known_relation_rows(bits, target):
    """The same five identities, trace times affine terms, and target-one xy=1."""
    integer(bits, 2, 31, "field bits")
    integer(target, 0, 1, "target bit")
    monomials = monomial_masks(bits)
    positions = {mask: j for j, mask in enumerate(monomials)}
    trace = trace_mask(bits, 1)
    terms = ([0] if target else []) + [1 << (bits+j) for j in range(bits) if (trace >> j) & 1]
    rows = list(linearized_rows(bits))
    rows.append(sum(1 << positions[mask] for mask in terms))
    for variable in range(2*bits):
        row = 0
        for mask in terms:
            row ^= 1 << positions[mask | (1 << variable)]
        rows.append(row)
    if target:
        coefficients = [(positions[(1 << i) | (1 << (bits+j))],
                         encoded(element(bits, 1 << i)*element(bits, 1 << j)))
                        for i in range(bits) for j in range(bits)]
        for component in range(bits):
            rows.append(int(component == 0) ^ sum(((value >> component) & 1) << pos
                                                  for pos, value in coefficients))
    return rows


def span_certificate(bits, target=1, *, seed=1022, samples=None):
    integer(bits, 2, 31, "field bits")
    integer(target, 0, 1, "target bit")
    integer(seed, 0, 2**32-1, "certificate seed")
    samples = 32*bits if samples is None else samples
    integer(samples, 0, 100000, "graph sample cap")
    rows = known_relation_rows(bits, target)
    relation_basis = {}
    for row in rows:
        _insert(row, relation_basis)
    graph_basis, selected = {}, []
    trace, rng = trace_mask(bits, 1), Random(seed)
    # Include the legal zero explicitly; otherwise a sparse sample can miss
    # its independent direction and misleadingly suggest another relation.
    values = ([0] if target == 0 else [])
    for _ in range(samples):
        y = rng.getrandbits(bits)
        if (y & trace).bit_count() % 2 != target:
            y ^= trace & -trace
        values.append(y)
    for y in values:
        x = encoded(element(bits, y)**-1) if y else 0
        lift = quadratic_lift(bits, x, y)
        if any((row & lift).bit_count() % 2 for row in rows):
            raise ArithmeticError("known local identity rejected a genuine graph point")
        if _insert(lift, graph_basis):
            selected.append([x, y])
    width = len(monomial_masks(bits))
    complete = len(graph_basis)+len(relation_basis) == width
    if len(graph_basis)+len(relation_basis) > width:
        raise ArithmeticError("orthogonal row spaces exceeded the ambient dimension")
    return {"status": "CERTIFIED_COMPLETE_LOCAL_QUADRATIC_SPAN" if complete else "UNKNOWN_LOCAL_SPAN",
            "bits": bits, "target": target, "seed": seed, "sample_cap": samples,
            "zero_control_included": target == 0,
            "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs())),
            "monomial_columns": width, "known_relation_rank": len(relation_basis),
            "true_graph_lift_rank": len(graph_basis), "selected_true_graph_points": selected,
            "relation_rows_sha256": sha256(json.dumps(rows).encode()).hexdigest(),
            "complete_local_quadratic_span": complete,
            "native_instance_resampled": False, "field_enumerated": False,
            "native_solver": False, "all_degrees_covered": False}


def verify_span_certificate(report):
    """Check selected genuine points and exact orthogonal rank saturation."""
    try:
        bits, target = report["bits"], report["target"]
        rows = known_relation_rows(bits, target)
        if report["field_modulus_coefficients"] != list(map(int, field(bits).modulus().coeffs())):
            return False
        if report["relation_rows_sha256"] != sha256(json.dumps(rows).encode()).hexdigest():
            return False
        points = report["selected_true_graph_points"]
        if not isinstance(points, list) or len(points) > len(monomial_masks(bits)):
            return False
        relation_basis, graph_basis = {}, {}
        for row in rows:
            _insert(row, relation_basis)
        trace = trace_mask(bits, 1)
        for pair in points:
            if not isinstance(pair, list) or len(pair) != 2:
                return False
            x, y = pair
            integer(x, 0, (1 << bits)-1, "graph coordinate")
            integer(y, 0, (1 << bits)-1, "graph inverse")
            if y != (encoded(element(bits, x)**-1) if x else 0) or (y & trace).bit_count() % 2 != target:
                return False
            lift = quadratic_lift(bits, x, y)
            if any((row & lift).bit_count() % 2 for row in rows) or not _insert(lift, graph_basis):
                return False
        width = len(monomial_masks(bits))
        return (report["complete_local_quadratic_span"] is True
                and report["status"] == "CERTIFIED_COMPLETE_LOCAL_QUADRATIC_SPAN"
                and report["monomial_columns"] == width
                and report["known_relation_rank"] == len(relation_basis)
                and report["true_graph_lift_rank"] == len(graph_basis)
                and len(relation_basis)+len(graph_basis) == width)
    except (KeyError, ValueError, TypeError, IndexError, AttributeError):
        return False
