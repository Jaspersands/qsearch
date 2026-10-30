"""Finite algebra controls, NOT an efficient quantum preparation algorithm.

Canonical coefficient-space parents for the HDQI pilot. Dense matrices cost
exponential space. Only star_log2_raw_norm is a scalable analytic calculation.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, expm, qr


@dataclass(frozen=True)
class Model:
    edges: tuple[tuple[int, int], ...]
    couplings: tuple[float, ...]
    operators: tuple[np.ndarray, ...]
    z: tuple[np.ndarray, ...]
    occupations: tuple[np.ndarray, ...]
    h: np.ndarray
    k: np.ndarray
    number: np.ndarray

    @property
    def m(self):
        return len(self.couplings)

    @property
    def degree(self):
        return max(sum(i in edge for edge in self.edges) for i in range(self.m))


def build_model(m, edges, couplings=None):
    """Qubit i is bit i (little endian); O_i = X_i prod_{j<i,j~i} Z_j."""
    if not isinstance(m, int) or isinstance(m, bool) or not 1 <= m <= 8:
        raise ValueError("dense control requires 1 <= m <= 8, not a scalable solver")
    normalized = []
    for edge in edges:
        if len(edge) != 2:
            raise ValueError("each edge must have two endpoints")
        i, j = edge
        if any(not isinstance(v, int) or isinstance(v, bool) for v in edge):
            raise ValueError("edge endpoints must be integers")
        if not 0 <= i < m or not 0 <= j < m or i == j:
            raise ValueError("invalid edge")
        pair = tuple(sorted((i, j)))
        if pair in normalized:
            raise ValueError("duplicate edge")
        normalized.append(pair)
    edges = tuple(sorted(normalized))
    couplings = tuple([1.0] * m if couplings is None else couplings)
    if len(couplings) != m or any(not np.isfinite(x) or abs(x) > 1 for x in couplings):
        raise ValueError("need m finite real couplings with |J_i| <= 1")
    size = 1 << m
    labels = np.arange(size)
    z = tuple(np.diag(1 - 2 * ((labels >> i) & 1)) for i in range(m))
    identity = np.eye(size)
    occupations = tuple((identity - zi) / 2 for zi in z)
    operators = []
    for i in range(m):
        lower = [j for j in range(i) if (j, i) in edges]
        signs = np.ones(size, dtype=int)
        for j in lower:
            signs *= 1 - 2 * ((labels >> j) & 1)
        op = np.zeros((size, size), dtype=int)
        op[labels ^ (1 << i), labels] = signs
        operators.append(op)
    h = sum(j * op for j, op in zip(couplings, operators))
    k = sum(j * op @ zi for j, op, zi in zip(couplings, operators, z))
    return Model(edges, couplings, tuple(operators), z, occupations, h, k,
                 sum(occupations))


def commutator(a, b):
    return a @ b - b @ a


def second_order(model, flattened=False):
    """Coefficient of beta^2 after rotation exp(beta K / 2)."""
    answer = np.zeros_like(model.h)
    if not flattened:
        answer += sum(j * j * ni for j, ni in zip(model.couplings, model.occupations))
    for i, j in model.edges:
        answer -= (model.couplings[i] * model.couplings[j] / 2
                   * model.operators[j] @ model.operators[i] @ (model.z[i] - model.z[j]))
    return answer


def second_order_from_commutators(model, flattened=False):
    """Independent Taylor calculation in t=beta/2, converted to beta^2."""
    a1 = np.zeros_like(model.h)
    a2 = np.zeros_like(model.h)
    for ji, ni in zip(model.couplings, model.occupations):
        ci = commutator(model.h, ni)
        di = commutator(model.h, ci)
        a1 += commutator(ci, ni)
        a2 += (di @ ni + ni @ di) / 2 - ci @ ci
        if flattened:
            a2 -= 4 * ji * ji * ni
    rotated = (a2 + commutator(model.k, a1)
               + commutator(model.k, commutator(model.k, model.number)) / 2)
    return rotated / 4


def one_excitation_prediction(model, flattened=False):
    js = np.array(model.couplings)
    adjacency = np.zeros((model.m, model.m))
    for i, j in model.edges:
        adjacency[i, j] = adjacency[j, i] = 1
    return js[:, None] * adjacency * js[None, :] + (
        0 if flattened else np.diag(js * js))


def parents(model, beta):
    """Exact dense controls; QR and matrix exponentials have exponential cost.

    Orthogonal projectors are formed from ker(q_i)=exp(-beta H/2) ker(n_i).
    QR here is NOT a supplied quantum implementation of those projectors.
    """
    if not np.isfinite(beta) or beta < 0:
        raise ValueError("beta must be finite and nonnegative")
    size = model.h.shape[0]
    s = expm(-beta * model.h / 2)
    inverse_s = expm(beta * model.h / 2)
    condition = float(np.linalg.cond(s))
    if not np.isfinite(condition) or condition > 1e9:
        raise ValueError("dense similarity is ill-conditioned; no trustworthy gap control")
    raw_terms, flat_terms, qs = [], [], []
    for i, ni in enumerate(model.occupations):
        qi = s @ ni @ inverse_s
        raw_terms.append(qi.T @ qi)
        zero_columns = [y for y in range(size) if not (y >> i) & 1]
        basis, _ = qr(s[:, zero_columns], mode="economic")
        flat_terms.append(np.eye(size) - basis @ basis.T)
        qs.append(qi)
    pilot = s[:, 0] / np.linalg.norm(s[:, 0])
    return {
        "raw": sum(raw_terms), "flat": sum(flat_terms),
        "raw_terms": raw_terms, "flat_terms": flat_terms, "q": qs,
        "pilot": pilot, "s": s, "condition": condition,
    }


def rotated_parent(model, beta, flattened=False):
    data = parents(model, beta)
    rotation = expm(beta * model.k / 2)
    return rotation @ data["flat" if flattened else "raw"] @ rotation.T


def star_log2_raw_norm(degree, beta):
    """Exact star hub term norm in log2, stable without constructing 2^(d+1)."""
    if (not isinstance(degree, int) or isinstance(degree, bool) or degree < 0
            or not np.isfinite(beta) or beta < 0):
        raise ValueError("need integer degree >= 0 and finite beta >= 0")
    if beta == 0:
        return 0.0
    r = math.hypot(1, degree)
    x = beta * r
    # -expm1(-2x) avoids cancellation when x is small.
    log_sinh = x - math.log(2) + math.log(-math.expm1(-2 * x))
    log_extra = 2 * log_sinh - 2 * math.log(r)
    return float(np.logaddexp(0, log_extra) / math.log(2))


def star_pair_log2_gap(degree, beta):
    """Exact gap of hub+one-leaf FLAT terms in the all-plus environment sector.

    This is a pair restriction, NOT the gap of the full star parent. The
    other d-1 leaves are fixed in the X=+1 sector, so H_a=X0+Z0(X1+a).
    A two-plane principal angle gives the formula; logs avoid ill-conditioned
    imaginary-time exponentials even for growing degree.
    """
    if (not isinstance(degree, int) or isinstance(degree, bool) or degree < 1
            or not np.isfinite(beta) or beta < 0):
        raise ValueError("need integer degree >= 1 and finite beta >= 0")
    if beta == 0:
        return 0.0
    a = degree - 1
    rp, rm = math.hypot(1, a + 1), math.hypot(1, a - 1)

    def log_sinh(x):
        return x - math.log(2) + math.log(-math.expm1(-2 * x))

    def log_cosh(x):
        return float(np.logaddexp(x, -x) - math.log(2))

    def log_v(b, r):
        # V_b=<0|exp[-beta (X+bZ)]|0>; stable even for b/r close to 1.
        small = -math.log(r) - math.log(r + abs(b))
        large = math.log(r + abs(b)) - math.log(r)
        minus, plus = (small, large) if b >= 0 else (large, small)
        return float(np.logaddexp(minus + beta * r, plus - beta * r) - math.log(2))

    vp, vm = log_v(a + 1, rp), log_v(a - 1, rm)
    product = rp * rm
    # product^2=a^4+4; rationalize 1-a^2/product to retain the small term.
    log_delta = math.log(4) - math.log(product) - math.log(product + a * a)
    difference = beta * 4 * a / (rp + rm)
    log_d = math.log(2) + float(np.logaddexp(
        math.log(2) + 2 * log_cosh(difference / 2),
        log_delta + log_sinh(beta * rp) + log_sinh(beta * rm)))
    log_sin_squared = float(2 * np.logaddexp(vp, vm) - vp - vm - log_d)
    if log_sin_squared > 1e-10:
        raise ArithmeticError("invalid principal angle from numerical cancellation")
    log_sin_squared = min(0.0, log_sin_squared)
    # 1-cos(theta)=sin^2(theta)/(1+sqrt(1-sin^2(theta))).
    return (log_sin_squared - math.log1p(math.sqrt(-math.expm1(log_sin_squared)))) / math.log(2)


def control_graphs():
    return {
        "commuting-weighted": build_model(4, [], [1, -.5, .25, 0]),
        "edge": build_model(2, [(0, 1)]),
        "cycle4": build_model(4, [(0, 1), (1, 2), (2, 3), (0, 3)]),
        "K3,3": build_model(6, [(i, j) for i in range(3) for j in range(3, 6)]),
        "star5": build_model(6, [(0, j) for j in range(1, 6)]),
        "clique5": build_model(5, [(i, j) for i in range(5) for j in range(i + 1, 5)]),
        "weighted-path": build_model(4, [(0, 1), (1, 2), (2, 3)], [1, -.5, .25, -.75]),
    }


def build_receipt():
    algebra, spectra = [], []
    for name, model in control_graphs().items():
        slots = [1 << i for i in range(model.m)]
        for flattened in (False, True):
            coefficient = second_order(model, flattened)
            form_bound = coefficient + (model.degree if flattened else max(0, model.degree - 1)) * model.number
            algebra.append({
                "graph": name, "parent": "flat" if flattened else "raw",
                "m": model.m, "degree": model.degree,
                "taylor_identity_exact": bool(np.array_equal(
                    coefficient, second_order_from_commutators(model, flattened))),
                "number_commutator_exact_zero": bool(np.array_equal(
                    commutator(coefficient, model.number), np.zeros_like(coefficient))),
                "one_excitation_identity_exact": bool(np.array_equal(
                    coefficient[np.ix_(slots, slots)], one_excitation_prediction(model, flattened))),
                "form_bound_min_eigenvalue": float(eigh(form_bound, eigvals_only=True)[0]),
                "gap_beta2_coefficient": float(eigh(one_excitation_prediction(model, flattened), eigvals_only=True)[0]),
            })
        for kappa in (.01, .1, .25, .5, 1.0):
            beta = math.sqrt(kappa / max(1, model.degree))
            data = parents(model, beta)
            for kind in ("raw", "flat"):
                ev = eigh(data[kind], eigvals_only=True)
                spectra.append({
                    "graph": name, "parent": kind, "m": model.m,
                    "degree": model.degree, "beta": beta,
                    "kappa": beta * beta * model.degree,
                    "gap": float(ev[1]), "ground_eigenvalue": float(ev[0]),
                    "pilot_kernel_residual": float(np.linalg.norm(data[kind] @ data["pilot"])),
                    "max_term_norm": float(max(eigh(term, eigvals_only=True)[-1]
                                               for term in data[kind + "_terms"])),
                    "dense_similarity_condition": data["condition"],
                })
    star_norms = [{"degree": d, "beta": .1 / math.sqrt(d), "kappa": .01,
                   "log2_hub_raw_term_norm": star_log2_raw_norm(d, .1 / math.sqrt(d))}
                  for d in (1, 10, 100, 1000, 10000, 1000000, 100000000)]
    star_pairs = [{"degree": d, "beta": .1 / math.sqrt(d), "kappa": .01,
                   "log2_flat_pair_sector_gap": star_pair_log2_gap(d, .1 / math.sqrt(d)),
                   "scope": "hub+one_leaf_only_with_other_leaves_X_plus_not_full_parent"}
                  for d in (1, 10, 100, 1000, 10000, 1000000, 100000000)]
    root = Path(__file__).resolve().parent
    hashes = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
              for name in ("parent_gap.py", "test_parent_gap.py", "PARENT_GAP_TARGET.md")}
    return {
        "schema": "hdqi-coefficient-parent-control-v1",
        "source": "https://arxiv.org/html/2610.03697v1",
        "status": "finite_controls_and_two_analytic_star_obstructions_only",
        "claims": {"uniform_gap_proved": False, "efficient_projectors_supplied": False,
                   "quantum_preparation_executed": False, "quantum_speedup_established": False,
                   "novelty_established": False, "independently_reviewed": False},
        "cost_warning": "Dense parent controls have exponential dimension; QR is not quantum access.",
        "algebra_controls": algebra, "finite_spectra": spectra,
        "analytic_star_norms": star_norms, "analytic_star_pair_gaps": star_pairs, "sha256": hashes,
        "blockers": ["uniform all-orders gap bound", "polynomial-priced bounded parent implementation",
                     "HDQI application with decoder guarantees and matched classical output task"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write reproducible JSON control receipt")
    args = parser.parse_args()
    data = build_receipt()
    payload = json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(payload)
        print(json.dumps({"output": str(args.output.resolve()),
                          "algebra_controls": len(data["algebra_controls"]),
                          "finite_spectra": len(data["finite_spectra"]),
                          "status": data["status"]}, indent=2))
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
