"""Public linear/cubic cancellation and finite class-three HSP Gram controls.

The moment solver is polynomial in label dimension and log(p). Sparse state
and kernel enumeration below is a bounded diagnostic, NOT the proposed
quantum implementation or an oracle-independent speedup demonstration.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
import json
from math import sqrt
from pathlib import Path
import random

import numpy as np

from theorems.folded_rs_decoder import affine_solution
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/graded_hsp_phase_descent.json"


def _canonical(values, length, p):
    if len(values) != length or any(type(x) is not int or not 0 <= x < p for x in values):
        raise ValueError("canonical field vector of the specified length required")


def _dependence(p, columns):
    dimension = len(columns[0])
    rows = [[column[j] for column in columns] for j in range(dimension)]
    solved = affine_solution(p, rows, [0] * dimension, len(columns))
    if solved is None or not solved["basis"]:
        raise ValueError("a nontrivial linear dependence was not supplied")
    return solved["basis"][0]


def moment(labels, weights, degree, p):
    if not labels or not labels[0] or len(labels) != len(weights):
        raise ValueError("matching nonempty labels and weights required")
    if type(degree) is not int or degree < 1:
        raise ValueError("positive integer moment degree required")
    _canonical(weights, len(labels), p)
    for label in labels:
        _canonical(label, len(labels[0]), p)
    return [sum(u[j] * pow(c, degree, p) for u, c in zip(labels, weights)) % p
            for j in range(len(labels[0]))]


def linear_cubic_weights(p, labels):
    """Solve sum u_i*c_i = sum u_i*c_i^3 = 0 using PUBLIC labels only.

    Cubing is bijective for p=2 mod 3. Disjoint cubic-zero blocks are then
    scaled by a second linear dependence, preserving each cubic identity.
    """
    ring(p)
    if p <= 3 or p % 3 != 2:
        raise ValueError("this construction requires prime p>3, p=2 mod 3")
    if not labels or not labels[0]:
        raise ValueError("nonempty positive-dimensional label batch required")
    r = len(labels[0])
    for column in labels:
        _canonical(column, r, p)
    required = (r + 1) ** 2
    if len(labels) < required:
        raise ValueError(f"at least {required} public labels required")
    inverse_cube = pow(3, -1, p - 1)
    blocks, linear_values = [], []
    for start in range(0, required, r + 1):
        block = labels[start:start + r + 1]
        coefficients = _dependence(p, block)
        roots = [pow(x, inverse_cube, p) for x in coefficients]
        if any(moment(block, roots, 3, p)):
            raise ArithmeticError("cubic block identity failed")
        blocks.append(roots)
        linear_values.append(moment(block, roots, 1, p))
    scales = _dependence(p, linear_values)
    weights = [scale * root % p for scale, block in zip(scales, blocks) for root in block]
    weights += [0] * (len(labels) - required)
    if not any(weights) or any(moment(labels, weights, 1, p)) or any(moment(labels, weights, 3, p)):
        raise ArithmeticError("nontrivial simultaneous moment cancellation failed")
    return weights


@dataclass(frozen=True)
class UT4Product:
    """Direct product of UT_4(F_p), not a truncated characteristic-zero ring."""

    p: int
    rank: int = 1

    def __post_init__(self):
        ring(self.p)
        if self.p <= 3 or type(self.rank) is not int or self.rank < 1:
            raise ValueError("prime p>3 and positive product rank required")

    @property
    def identity(self):
        return (0,) * (6 * self.rank)

    def multiply(self, a, b):
        result, p = [], self.p
        for i in range(self.rank):
            x, y, z, u, v, w = a[6*i:6*i+6]
            X, Y, Z, U, V, W = b[6*i:6*i+6]
            result += [x+X, y+Y, z+Z, u+U+x*Y, v+V+y*Z, w+W+x*V+u*Z]
        return tuple(t % p for t in result)

    def inverse(self, a):
        result = []
        for i in range(self.rank):
            x, y, z, u, v, w = a[6*i:6*i+6]
            result += [-x, -y, -z, x*y-u, y*z-v, -w+x*v+u*z-x*y*z]
        return tuple(t % self.p for t in result)

    def power(self, a, exponent):
        if type(exponent) is not int or exponent < 0:
            raise ValueError("nonnegative integer exponent required")
        result = self.identity
        while exponent:
            if exponent & 1:
                result = self.multiply(result, a)
            a = self.multiply(a, a)
            exponent //= 2
        return result

    def dilate(self, a, scale):
        if type(scale) is not int or not 0 < scale < self.p:
            raise ValueError("dilation must be a nonzero canonical field element")
        return tuple(t * pow(scale, (1, 1, 1, 2, 2, 3)[j % 6], self.p) % self.p
                     for j, t in enumerate(a))

    def exp(self, logarithm):
        _canonical(logarithm, 6 * self.rank, self.p)
        result, inv2, inv6 = [], pow(2, -1, self.p), pow(6, -1, self.p)
        for i in range(self.rank):
            x, y, z, u, v, w = logarithm[6*i:6*i+6]
            result += [x, y, z, u+x*y*inv2, v+y*z*inv2,
                       w+(x*v+u*z)*inv2+x*y*z*inv6]
        return tuple(t % self.p for t in result)

    def center(self, coordinates):
        _canonical(coordinates, self.rank, self.p)
        return tuple(t for z in coordinates for t in (0, 0, 0, 0, 0, z))


def coset_fixture(group, generator, representative):
    """Secret-bearing fixture only. Receivers take states, not this generator."""
    subgroup = {group.power(generator, t) for t in range(group.p)}
    if len(subgroup) != group.p or group.power(generator, group.p) != group.identity:
        raise ValueError("fixture requires a subgroup of order p")
    return {group.multiply(representative, h): complex(1 / sqrt(group.p)) for h in subgroup}


def project_top_center(group, state, label):
    """Execute a public central Fourier projector on a supplied sparse state."""
    _canonical(label, group.rank, group.p)
    if group.p ** group.rank > 4096:
        raise ValueError("finite projector diagnostic cap; not an algorithmic bound")
    projected = {}
    roots = [np.exp(2j * np.pi * t / group.p) for t in range(group.p)]
    size = group.p ** group.rank
    for z in product(range(group.p), repeat=group.rank):
        shift = group.inverse(group.center(z))
        phase = roots[-sum(a*b for a, b in zip(label, z)) % group.p] / size
        for x, amplitude in state.items():
            dest = group.multiply(x, shift)
            projected[dest] = projected.get(dest, 0j) + phase * amplitude
    probability = sum(abs(x) ** 2 for x in projected.values())
    if probability < 1e-14:
        raise ValueError("zero-probability diagnostic Fourier branch")
    return {x: amplitude / sqrt(probability) for x, amplitude in projected.items()}, probability


def right_correlations(group, state):
    """All <psi|R_g|psi> via sparse support pairs; no hidden-subgroup input."""
    if len(state) > 4096:
        raise ValueError("finite correlation diagnostic cap")
    values = {}
    for y, b in state.items():
        inverse = group.inverse(y)
        for x, a in state.items():
            g = group.multiply(inverse, x)
            values[g] = values.get(g, 0j) + np.conjugate(b) * a
    return values


def dilation_product_kernel(group, kernels, weights):
    """Gram of the physical controlled action tensor_i R_(delta_ci(g))."""
    if len(kernels) != len(weights) or not any(weights):
        raise ValueError("matching kernels and a nonzero weight vector required")
    _canonical(weights, len(kernels), group.p)
    result = None
    for kernel, c in zip(kernels, weights):
        if not c:
            continue
        inverse_scale = pow(c, -1, group.p)
        pulled = {group.dilate(g, inverse_scale): value for g, value in kernel.items()}
        result = pulled if result is None else {
            g: value * pulled[g] for g, value in result.items() if g in pulled
        }
    return result


def _distance(kernel, indicator):
    return max((abs(kernel.get(g, 0j) - int(g in indicator))
                for g in set(kernel) | set(indicator)), default=0.0)


def controls():
    p, rank = 11, 1
    group = UT4Product(p, rank)
    labels = [[1], [2], [3], [4]]
    weights = linear_cubic_weights(p, labels)
    rng = random.Random(20261021)
    representatives = [tuple(rng.randrange(p) for _ in group.identity) for _ in labels]
    logarithm = [1, 2, 3, 0, 0, 4]
    generator = group.exp(logarithm)

    def measure(g, chosen_labels=None):
        chosen_labels = labels if chosen_labels is None else chosen_labels
        kernels, probabilities = [], []
        for a, label in zip(representatives, chosen_labels):
            state, probability = project_top_center(group, coset_fixture(group, g, a), label)
            kernels.append(right_correlations(group, state))
            probabilities.append(probability)
        return kernels, probabilities

    kernels, probabilities = measure(generator)
    output = dilation_product_kernel(group, kernels, weights)
    subgroup = {group.power(generator, t) for t in range(p)}
    center = {group.center([z]) for z in range(p)}
    enlarged = {group.multiply(h, z) for h in subgroup for z in center}
    first = _dependence(p, labels[:2])
    cube_only = [pow(x, pow(3, -1, p-1), p) for x in first] + [0, 0]
    bad_phase = dilation_product_kernel(group, kernels, cube_only)

    changed = logarithm[:]
    changed[3] = 1
    changed_generator = group.exp(changed)
    changed_kernels, _ = measure(changed_generator)
    bad_grade = dilation_product_kernel(group, changed_kernels, weights)
    changed_enlarged = {group.multiply(group.power(changed_generator, t), z)
                        for t in range(p) for z in center}
    paired_labels, paired_weights = [[1], [p-1], [2], [p-2]], [1, 1, 2, 2]
    paired_kernels, _ = measure(changed_generator, paired_labels)
    all_moments = dilation_product_kernel(group, paired_kernels, paired_weights)
    common = dilation_product_kernel(group, paired_kernels[:2], [2, 2])
    common_target = {group.dilate(g, pow(2, -1, p)) for g in changed_enlarged}
    if _distance(output, enlarged) > 1e-10:
        raise ArithmeticError("promised central quotient Gram failed")
    if _distance(bad_grade, center) > 1e-10:
        raise ArithmeticError("grade-two negative did not reduce to the center")
    return {
        "status": "PROMISED_CLASS_THREE_CENTRAL_CONVERSION_REVIEW_PENDING",
        "parameters": {"prime": p, "product_rank": rank, "ambient_group_order": p**6,
                       "label_count": len(labels), "fixture_logarithm": logarithm},
        "public_labels": labels,
        "public_weights": weights,
        "linear_moment": moment(labels, weights, 1, p),
        "cubic_moment": moment(labels, weights, 3, p),
        "projector_branch_probabilities": probabilities,
        "gram_control": {"target_subgroup_order": len(enlarged),
                         "computed_support": len(output),
                         "maximum_error": _distance(output, enlarged)},
        "cubic_only_negative": {
            "weights": cube_only,
            "linear_moment": moment(labels, cube_only, 1, p),
            "cubic_moment": moment(labels, cube_only, 3, p),
            "hidden_generator_overlap": [float(bad_phase.get(generator, 0j).real),
                                         float(bad_phase.get(generator, 0j).imag)],
            "error_from_required_one": float(abs(bad_phase.get(generator, 0j)-1))
        },
        "grade_two_negative": {
            "fixture_logarithm": changed,
            "error_from_required_HZ": _distance(bad_grade, changed_enlarged),
            "error_from_center_only": _distance(bad_grade, center),
            "hidden_generator_overlap_abs": float(abs(bad_grade.get(changed_generator, 0j))),
            "computed_support": len(bad_grade)
        },
        "all_moments_negative": {
            "labels": paired_labels,
            "weights": paired_weights,
            "moments_one_through_three": [moment(paired_labels, paired_weights, j, p)
                                         for j in (1, 2, 3)],
            "error_from_center_only": _distance(all_moments, center),
            "error_from_required_HZ": _distance(all_moments, changed_enlarged)
        },
        "common_scaling_positive": {
            "weights": [2, 2],
            "error_from_publicly_rescaled_HZ": _distance(common, common_target),
            "error_from_unrescaled_HZ": _distance(common, changed_enlarged),
            "interpretation": "A known common dilation is invertible relabeling, not lost information."
        },
        "scope": {
            "moment_solver_uses_secret": False,
            "kernel_operations_use_secret": False,
            "original_coset_projector_executed": True,
            "small_sparse_diagnostics_are_scalable_quantum_execution": False,
            "entire_promised_HSP_receiver_executed": False,
            "generic_grade_two_terms_supported": False,
            "arbitrary_nilpotent_HSP_solved": False,
            "novelty_established": False,
            "useful_external_problem_reduction_supplied": False,
            "central_claim_admission": False
        }
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = controls()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(rendered)
    print(rendered)


if __name__ == "__main__":
    main()
