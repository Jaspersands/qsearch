"""Reproduce finite controls; never claim to have run the imported splitter."""

import argparse
import hashlib
import json
from pathlib import Path
from random import Random
import sys

from flint import fq_default_ctx
from sympy import Matrix, eye, nextprime

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "source-algebra-splitting-2026-10-25"))
sys.path.insert(0, str(ROOT / "elliptic-theta-input-2026-10-26"))
from native_preprocessing import (
    check_order, clear_denominators, dictionary_from_bimodule,
    recover_order, reference_half_frobenius,
)
from elliptic_theta import EllipticCurve, point_key
from kernel_output import QuaternionOrder, action, odd_maximal_order
from source_split import source_split


def arithmetic_control(level):
    source = odd_maximal_order(11)
    change = Matrix.diag(1, level, level, level)
    inverse = change.inv()
    target = QuaternionOrder(
        tuple(tuple(inverse*source.multiply(change[:, i], change[:, j]) for j in range(4))
              for i in range(4)), inverse*source.unit,
        inverse*source.involution*change, source.traces*change,
    )
    basis = [eye(4)[:, i] for i in range(4)]
    bound = max(int((target.traces*target.multiply(x, target.star(x)))[0]/2) for x in basis)
    transcripts, modulus, prime = [], 1, 2
    while modulus <= 4*bound**2:
        prime = int(nextprime(prime))
        if prime == 11:
            continue
        actions, _ = source_split(source, prime, [(prime, 1)], 11, Random(prime))
        transcripts.append((prime, tuple(action(change[:, i], actions) for i in range(4))))
        modulus *= prime
    recovered = recover_order(transcripts, bound, 11)
    if recovered.products != target.products or recovered.involution != target.involution:
        raise AssertionError("order reconstruction mismatch")
    left = tuple(Matrix.hstack(*(source.multiply(x, y) for y in basis)) for x in basis)
    right = tuple(Matrix.hstack(*(source.multiply(x, change[:, j]) for x in basis))
                  for j in range(4))
    dictionary = dictionary_from_bimodule(source, target, left, right, source.unit)
    denominator, scaled = clear_denominators(source, target, dictionary)
    if dictionary != inverse or denominator != level:
        raise AssertionError("dictionary reconstruction mismatch")
    return {
        "suborder_scale": level, "basis_degree_bound": bound,
        "small_torsion_levels": [p for p, _ in transcripts],
        "crt_modulus": modulus, "order_reconstructed": True,
        "denominator": denominator,
        "scaled_dictionary": [[int(x) for x in row] for row in scaled.tolist()],
        "provenance": "supplied arithmetic actions and tensor-module fixture, not native target maps",
    }


def native_control(p):
    field = fq_default_ctx(p, 2, "z")
    curve = EllipticCurve(field, -1, 0)
    points, _ = curve.torsion_eight()
    fibers = {}
    for half in points:
        point = curve.multiply(2, half)
        fibers.setdefault(point_key(point), (point, []))[1].append(half)
    images = {}
    for key, (point, halves) in fibers.items():
        values = [reference_half_frobenius(curve, point, half) for half in halves]
        if len(halves) != 4 or any(value != values[0] for value in values):
            raise AssertionError("half-point dependence")
        images[key] = values[0]
    for key, (point, _) in fibers.items():
        h = images[key]
        difference = curve.add(images[point_key(h)], curve.neg(h))
        difference = curve.add(difference, curve.multiply((p+1)//4, point))
        if difference is not None:
            raise AssertionError("half-Frobenius norm relation")
    if check_order(odd_maximal_order(p)).det() != p*p:
        raise AssertionError("source discriminant")
    return {
        "characteristic": p, "field_degree": 2, "curve_a": -1, "curve_b": 0,
        "distinct_test_inputs": len(fibers), "half_points_tested": len(points),
        "lift_independence_checked": True, "quadratic_relation_checked": True,
        "abstract_source_discriminant": p*p,
    }


def commutation_bound_control(p):
    order = odd_maximal_order(p)
    x, y = Matrix([0, 0, 0, 1]), Matrix([0, -1, 0, 1])
    norm = (p+1)//4
    xy, yx = order.multiply(x, y), order.multiply(y, x)
    trace = int((order.traces*xy)[0])
    if (order.multiply(x, x) != -norm*order.unit
            or order.multiply(y, y) != -norm*order.unit
            or xy == yx or xy+yx != trace*order.unit
            or 4*norm**2-trace**2 != p):
        raise AssertionError("commutation-bound control")
    return {"characteristic": p, "common_pure_norm": norm,
            "product_trace": trace, "reduced_discriminant": p,
            "noncommuting": True, "provenance": "abstract quaternion-order control"}


def receipt():
    sources = json.loads((HERE / "sources.json").read_text())
    for source in sources:
        digest = hashlib.sha256((HERE / source["path"]).read_bytes()).hexdigest()
        if digest != source["sha256"]:
            raise AssertionError(f"source changed: {source['id']}")
    return {
        "schema": "native-suborder-preprocessing-controls-v1",
        "status": "written conditional reduction and finite interface controls",
        "arithmetic_controls": [arithmetic_control(n) for n in (6, 101)],
        "native_reference_controls": [native_control(p) for p in (7, 23, 31)],
        "cm_commutation_bound_controls": [commutation_bound_control(p) for p in (7, 11, 23)],
        "sources": sources,
        "execution_scope": {
            "small_trace_to_order_executed": True,
            "supplied_tensor_module_extraction_executed": True,
            "native_reference_half_frobenius_control_executed": True,
            "published_rational_tensor_splitter_executed": False,
            "general_cm_source_construction_executed": False,
            "native_target_full_preprocessing_executed": False,
            "canonical_geometric_label_executed": False,
            "coherent_source_executed": False,
            "independent_review_of_this_repair": False,
            "novelty_established": False,
            "speedup_established": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = receipt()
    path = HERE / "receipt.json"
    if args.write:
        path.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    if args.check and json.loads(path.read_text()) != result:
        raise SystemExit("receipt mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
