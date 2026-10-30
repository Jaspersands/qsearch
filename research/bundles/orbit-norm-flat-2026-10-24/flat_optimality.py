"""Exact controls for the all-F_p-linear norm-flat dimension bound.

The theorem is a local unreviewed deduction in FLAT_OPTIMALITY.md. Finite
certificates are not formal proofs, classical lower bounds, or speedups.
"""

import argparse
import hashlib
import json
from pathlib import Path

from flint import nmod_mat, nmod_poly

import norm_flat as n


def dimension_bound(M, r):
    n.integer(M, "block count", 2, 10**7)
    n.integer(r, "parity rank", 1, M-1)
    s = M-r+1
    return {"M": M, "parity_rank": r, "active_blocks": s,
            "all_Fp_linear_flat_dimension_bound": 2*(s//2),
            "full_row_rank_completion_possible_by_dimension": 2*(s//2) >= r,
            "scope": "common_quadratic_zero_directions_only_LOCAL_UNREVIEWED"}


def restricted_gram(basis, diagonal, p):
    """Full polarized check, not just the quadratic values on a basis."""
    W = nmod_mat(basis, p)
    scaled = nmod_mat([[weight*int(W[i,j]) % p for j in range(W.ncols())]
                       for i,weight in enumerate(diagonal)], p)
    return W.transpose()*scaled


def certificate(p, nodes, weights, nu, r, basis, roots=None):
    n.field(p)
    M = len(nodes)
    bound = dimension_bound(M, r)
    for value in nodes:
        n.integer(value, "node", 0, p-1)
    if len(set(nodes)) != M or len(weights) != M:
        raise ValueError("distinct nodes and one nonzero weight per node required")
    for value in weights:
        n.integer(value, "weight", 1, p-1)
    n.integer(nu, "nonsquare", 1, p-1)
    if pow(nu, (p-1)//2, p) != p-1:
        raise ValueError("anisotropic norm required for the support lemma")
    if len(basis) != 2*M or not basis or not basis[0]:
        raise ValueError("nonempty 2M-row basis required")
    D = len(basis[0])
    if any(len(row) != D for row in basis):
        raise ValueError("rectangular basis required")
    for row in basis:
        for value in row:
            n.integer(value, "basis entry", 0, p-1)
    if nmod_mat(basis, p).rank() != D:
        raise ValueError("basis columns must be independent")
    for j in range(r):
        diagonal = [a*pow(c,j,p) % p for a,c in zip(weights,nodes)]
        diagonal += [-nu*a % p for a in diagonal]
        if any(restricted_gram(basis, diagonal, p).entries()):
            raise ValueError("not a common quadratic-zero subspace")
    roots = list(range(r-1)) if roots is None else list(roots)
    if len(roots) != r-1 or len(set(roots)) != len(roots):
        raise ValueError("exactly r-1 distinct root indices required")
    for i in roots:
        n.integer(i, "root index", 0, M-1)
    f = nmod_poly([1], p)
    for i in roots:
        f *= nmod_poly([-nodes[i],1], p)
    active = [i for i,c in enumerate(nodes) if f(c)]
    if len(active) != bound["active_blocks"]:
        raise ArithmeticError("annihilator support does not match the proof")
    projected = [basis[i] for i in active]+[basis[M+i] for i in active]
    projection_rank = nmod_mat(projected, p).rank()
    if projection_rank != D:
        raise ArithmeticError("support lemma violated")
    diagonal = [weights[i]*int(f(nodes[i])) % p for i in active]
    diagonal += [-nu*a % p for a in diagonal]
    if any(restricted_gram(projected, diagonal, p).entries()):
        raise ArithmeticError("projected space is not totally isotropic")
    determinant = 1
    for value in diagonal:
        determinant = determinant*value % p
    discriminant = pow(-1,len(active),p)*determinant % p
    square_class = pow(discriminant,(p-1)//2,p)
    expected = 1 if len(active)%2 == 0 else p-1
    if square_class != expected or D > bound["all_Fp_linear_flat_dimension_bound"]:
        raise ArithmeticError("dimension/determinant certificate contradiction")
    theta = [[nu*basis[M+i][j] % p for j in range(D)] for i in range(M)]+basis[:M]
    theta_closed = nmod_mat([a+b for a,b in zip(basis,theta)],p).rank() == D
    return {**bound, "p":p, "nu":nu, "nodes":nodes, "weights":weights,
            "basis":basis, "dimension":D, "theta_closed":theta_closed,
            "annihilator_coefficients":[int(c) for c in f], "root_indices":roots,
            "active_indices":active, "projection_rank":projection_rank,
            "restricted_Gram_matrices_zero":True, "projected_determinant":determinant,
            "signed_determinant_square_class":square_class}


def native_control(p, K, *, target_K=None, remove_last=False, roots=None):
    g,b,nu,_ = n.fixture(p,K,917)
    setup = n.build(g,b,nu)
    M = len(g.points)
    r = 3*M-3*(K if target_K is None else target_K)
    D = dimension_bound(M,r)["all_Fp_linear_flat_dimension_bound"]-int(remove_last)
    basis = [[int(matrix[i,j]) for j in range(D)] for matrix in (setup.wx,setup.wy)
             for i in range(M)]
    return certificate(p, [o[2] for o in g.points],
                       [setup.weights[3*i+2]*b[i] % p for i in range(M)],
                       nu,r,basis,roots)


def receipt():
    root = Path(__file__).resolve().parent
    files = ("flat_optimality.py","test_flat_optimality.py","FLAT_OPTIMALITY.md",
             "norm_flat.py","receipt.json",
             "../orbit-residual-decoder-2026-10-24/orbit_decoder.py")
    hashes = {p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files}
    rows = [native_control(19,5), native_control(19,5,remove_last=True),
            native_control(31,9), native_control(43,12),
            native_control(31,9,target_K=8), native_control(43,12,target_K=10)]
    result = {"status":"LOCAL_UNREVIEWED_ALL_FP_FLAT_OPTIMALITY",
              "controls":rows, "rate_point_eight":dimension_bound(4096,2460),
              "frozen_high_rate":dimension_bound(684,342),
              "scope":{"larger_non_E_linear_common_flats_can_rescue_rank_gate":False,
                       "all_classical_algorithms_ruled_out":False,
                       "rate_point_eight_dequantized":False,
                       "quantum_speedup_or_novelty_established":False},
              "source_sha256":hashes}
    if hashes != {p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files}:
        raise RuntimeError("source changed during certificate generation")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    rendered = json.dumps(receipt(),indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered,end="")
