"""Integral controls for the deduction; not a geometric isogeny backend."""

import argparse
import json
from pathlib import Path
import sys

from sympy import Matrix, zeros

from product_dichotomy import (
    ROOT, action, classify_projectors, column_basis, matrix_multiply, matrix_star,
    mod, product_actions, restrict_weak_blocks, standard_projectors,
)
from controls import ArithmeticSource
from kernel_output import odd_maximal_order
from pullback import reconstruct_pullbacks


def source_fixture(kind):
    order = odd_maximal_order(11)
    one, zero = order.unit, zeros(4, 1)
    pi = Matrix([2, 1, 0, 0])
    if kind == "mixed":
        phi = Matrix.vstack(one, 2*one, -2*one, one)
    elif kind == "diagonal":
        phi = Matrix.vstack(pi, zero, zero, order.star(pi))
    elif kind == "permuted":
        phi = Matrix.vstack(zero, pi, order.star(pi), zero)
    else:
        raise ValueError("unknown control")
    projectors = standard_projectors(order)
    return ArithmeticSource(11, 5, order, phi, projectors)


def run_control(kind):
    source = source_fixture(kind)
    identity = sum(source.gammas, zeros(16, 1))
    assert matrix_multiply(source.order, matrix_star(source.order, source.phi),
                           source.phi) == source.ell * identity
    reconstructed = reconstruct_pullbacks(
        source.order, source.ell, source.characteristic, (2, 2), source.levels(),
        source.split, source.observe, max_auxiliary_prime=47)
    assert reconstructed.coordinates == source.reference_pullbacks()
    result = classify_projectors(source.order, source.ell, source.split(source.ell),
                                 reconstructed.coordinates)
    matrices = product_actions(source.split(source.ell))
    secret_map = mod(action(source.phi, matrices), source.ell)
    if result.kernel_basis is not None:
        assert column_basis(secret_map, source.ell).cols == 2
        assert mod(secret_map * result.kernel_basis, source.ell) == zeros(4, 2)
        restriction_checks = 0
    else:
        restriction_checks = 0
        # The fixture's public frame is block diagonal. Restriction never
        # uses its secret phi; the exact comparison below is validation only.
        for r in reconstructed.primes:
            packet = source.observe(r)
            blocks = restrict_weak_blocks(packet.weak_action, r, result.target_to_source)
            for i, j in enumerate(result.target_to_source):
                assert source.phi[4*(2*i+1-j):4*(2*i+1-j)+4, :] == zeros(4, 1)
                frame = Matrix([[1, 2 if i == 0 else 3], [0, 1]])
                exact = action(source.phi[4*(2*i+j):4*(2*i+j)+4, :], source.split(r))
                mask = 2 if r > 3 else r-1
                assert blocks[i] == mod(mask * frame.inv() * exact, r)
                restriction_checks += 1
    return {
        "kind": kind, "status": result.status, "ranks": list(result.ranks),
        "kernel_dimension": None if result.kernel_basis is None else result.kernel_basis.cols,
        "target_to_source": list(result.target_to_source),
        "auxiliary_primes": list(reconstructed.primes),
        "crt_modulus": reconstructed.modulus,
        "pairing_bound": reconstructed.pairing_bound,
        "hidden_prime_weak_query": source.ell in source.calls,
        "public_hidden_prime_split": "supplied to extractor; enumerative fixture only",
        "exact_pullbacks_match": True,
        "masked_elliptic_block_checks": restriction_checks,
        "geometric_input_verified": result.geometric_input_verified,
        "elliptic_backend_executed": result.elliptic_backend_executed,
        "classical_hardness_established": result.classical_hardness_established,
    }


def receipt():
    return {
        "schema": "product-source-dichotomy-arithmetic-control-v1",
        "scope": "constructed integral quaternion controls, not native geometry",
        "quantum_execution": False,
        "controls": [run_control(kind) for kind in ("mixed", "diagonal", "permuted")],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = receipt()
    path = Path(__file__).with_name("receipt.json")
    if args.write:
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    if args.check and json.loads(path.read_text()) != data:
        sys.exit("receipt mismatch")
    print(json.dumps(data, indent=2, sort_keys=True))
