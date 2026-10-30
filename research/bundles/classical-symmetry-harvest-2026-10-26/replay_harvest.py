"""Replay supplied-order extraction controls; no geometric automorphisms run."""

import argparse
import hashlib
import json
from pathlib import Path

from sympy import Matrix, eye, zeros

from harvest import (
    adjoin_and_close, coprime_scalar_shift, entries, outside_lattice,
    pell_product_factor, pullback_certificate,
)
from additive_source import adjoint, construct, multiply, quaternion_matrix, scalar_matrix
from kernel_output import odd_maximal_order

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def pullback_control(denominator):
    order = odd_maximal_order(11)
    one, zero, delta, i = order.unit, zeros(4, 1), eye(4)[:, 2], eye(4)[:, 1]
    u = quaternion_matrix([[one, delta], [zero, one]])
    inverse = quaternion_matrix([[one, -delta], [zero, one]])
    v = quaternion_matrix([[i, zero], [zero, one]])
    z = multiply(order, adjoint(order, u), u)
    w = multiply(order, multiply(order, inverse, v), u)
    basis = Matrix.diag(1, 3, 1, 3)
    pulled, report = pullback_certificate(order, z, u.scale(denominator),
                                          inverse.scale(denominator), w, denominator**2, 9)
    result, chain = adjoin_and_close(order, basis, entries(pulled))
    if not outside_lattice(w, basis) or (denominator == 3 and chain != [9]):
        raise AssertionError("bad-multiplier control changed")
    if denominator == 2 and (result != eye(4) or chain != [9, 3, 1]):
        raise AssertionError("known-unit growth control changed")
    return {
        "denominator": denominator, "index_chain": chain,
        "symmetry_outside_input_order": True,
        "pullback_outside_input_order": bool(outside_lattice(pulled, basis)),
        "certificate": report,
        "provenance": "supplied known order and already easy elliptic-unit symmetry",
    }


def pell_control(n, k):
    order = odd_maximal_order(11)
    p, inverse = pell_product_factor(n, k)
    z = construct(order, zeros(4, 1), n, (2*k*k, 2*k, 0, 0))["polarization"]
    if scalar_matrix(order, p.T*p) != z or p*inverse != eye(16):
        raise AssertionError("Pell standard-product factorization failed")
    return {"index_parameter": n, "pell_parameter": k,
            "roots": [2*k*k, 2*k, 0, 0], "integral_standard_product_factorization": True,
            "scope": "zero query only; no random-query success probability follows"}


def receipt():
    paths = [HERE / name for name in ("HARVEST.md", "harvest.py", "test_harvest.py", "replay_harvest.py")]
    paths += [ROOT / path for path in (
        "additive-framed-source-2026-10-26/additive_source.py",
        "additive-framed-source-2026-10-26/ADDITIVE_SOURCE.md",
        "polarization-completion-probe-2026-10-25/POLARIZATION_COMPLETION.md",
        "ppav-source-2026-10-23/2026-1142.pdf",
        "additive-source-independent-review-2026-10-26/REVIEW.md",
    )]
    return {
        "schema": "classical-symmetry-harvest-controls-v2",
        "status": "independently reviewed extraction theorem; classical recovery needs a uniform hitting theorem",
        "review_followup": {
            "finding": "P2: instance-wise samplers do not imply a uniform algorithm",
            "resolution": "one sampler and one polynomial, covering all adaptively reached orders",
            "corrected_statement_independently_re_reviewed": False,
        },
        "uniform_hitting_obligation": {
            "single_uniform_sampler_required": True,
            "single_polynomial_required": True,
            "original_paid_input_length_required": True,
            "all_adaptively_reached_orders_required": True,
            "polynomial_query_and_frame_lengths_required": True,
            "native_data_only_required": True,
            "sampler_implemented": False,
            "hitting_bound_proved": False,
        },
        "pullback_controls": [pullback_control(d) for d in (2, 3)],
        "pell_controls": [pell_control(n, k) for n, k in ((3, 2), (17, 12), (99, 70), (577, 408))],
        "inseparable_degree_shift_control": {
            "characteristic": 11, "original_trace": 0, "original_degree": 11,
            "shift_and_new_degree": coprime_scalar_shift(11, 0, 11),
            "interpolation_executed": False,
        },
        "hashes": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in paths},
        "execution_scope": {
            "exact_matrix_and_order_closure_controls": True,
            "native_geometric_automorphism_enumeration": False,
            "native_pullback_or_order_recovery": False,
            "native_map_compression": False,
            "hitting_probability_established": False,
            "full_classical_dequantization_established": False,
            "quantum_advantage_established": False,
            "independent_review": True,
            "novelty_established": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = json.dumps(receipt(), sort_keys=True, indent=2)+"\n"
    path = HERE / "receipt.json"
    if args.write:
        path.write_text(encoded)
    if args.check and json.loads(path.read_text()) != json.loads(encoded):
        raise SystemExit("receipt mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
