"""Bounded end-to-end Rees falsifier in the faithful regular group algebra.

The original source replay enumerates F5; a separate F7 control exercises
the nonbijective cubic solver on actual conditioned sources. Neither is a
scalable receiver. A
coefficient dictionary c means rho=(1/|G|) sum_g c[g] R_g. Projectors are
multiplied as actual operators; hidden membership is not a channel input.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
import json
from math import prod
from pathlib import Path
import random

import numpy as np

from theorems.central_character_descent import check_moment, exhaustive_scale_fixture
from theorems.cubic_diagonal_solver import cubic_arity, cubic_weights
from theorems.folded_rs_decoder import affine_solution
from theorems.nil3_guarded_cyclic_dispatch import square_weights_capped
from theorems.weighted_two_erasure_cascade import solve_bezout_sde_weights

TOL = 2e-10


@dataclass(frozen=True)
class ReesFiliformFixture:
    stage: int = 3
    p: int = 5

    def __post_init__(self):
        if (type(self.stage) is not int or self.stage not in (1, 2, 3)
                or type(self.p) is not int or self.p not in (5, 7)):
            raise ValueError("only bounded three-stage F5/F7 fixtures are implemented")

    @property
    def width(self):
        return {1: 4, 2: 6, 3: 7}[self.stage]

    @property
    def identity(self):
        return (0,)*self.width

    @property
    def order(self):
        return self.p**self.width

    def mul(self, a, b):
        x, y, z, w, u, v, t = a+(0,)*(7-self.width)
        X, Y, Z, W, U, V, T = b+(0,)*(7-self.width)
        half = pow(2, -1, self.p)
        return tuple(s % self.p for s in (x+X, y+Y, z+Z, w+W, u+U+x*Y,
                                          v+V+x*Z, t+T+x*U+half*x*x*Y)[:self.width])

    def inv(self, a):
        x, y, z, w, u, v, t = a+(0,)*(7-self.width)
        half = pow(2, -1, self.p)
        return tuple(s % self.p for s in (-x, -y, -z, -w, -u+x*y,
                                          -v+x*z, -t+x*u-half*x*x*y)[:self.width])

    def dilate(self, a, s):
        if type(s) is not int or not 0 < s < self.p:
            raise ValueError("nonzero canonical field scale required")
        return tuple(x*pow(s, d, self.p) % self.p for x, d in zip(a, (1, 1, 1, 1, 2, 2, 3)))

    @property
    def quotient(self):
        if self.stage == 1:
            raise ValueError("grade one is the terminal abelian group")
        return ReesFiliformFixture(self.stage-1, self.p)

    def project(self, g):
        return g[:self.quotient.width]

    @property
    def center_points(self):
        width = self.width-self.quotient.width
        return tuple((z, (0,)*self.quotient.width+z) for z in product(range(self.p), repeat=width))

    def evaluate(self, a, s):
        if self.stage != 3:
            raise ValueError("evaluate the full cover only")
        x, y, z, w, u, v, t = a
        return (s*x % self.p, s*y % self.p, (s*z+s*s*u) % self.p, (s*w+s*s*v+s**3*t) % self.p)


def source_multiply(a, b):
    x, y, z, w = a
    X, Y, Z, W = b
    return (x+X) % 5, (y+Y) % 5, (z+Z+x*Y) % 5, (w+W+x*Z+3*x*x*Y) % 5


def _clean(coefficients):
    return {g: value for g, value in coefficients.items() if abs(value) > 1e-12}


def operator_product(group, left, right):
    out = defaultdict(complex)
    for g, a in left.items():
        for h, b in right.items():
            out[group.mul(g, h)] += a*b
    return _clean(out)


def conditioned_coefficients(group, coefficients, label):
    center = group.center_points
    if (len(label) != len(center[0][0])
            or any(type(x) is not int or not 0 <= x < group.p for x in label)):
        raise ValueError("canonical central character of the correct dimension required")
    projector = {z: np.exp(-2j*np.pi*sum(a*b for a, b in zip(label, coords))/group.p)/len(center)
                 for coords, z in center}
    adjoint = {group.inv(g): value.conjugate() for g, value in projector.items()}
    branch = operator_product(group, operator_product(group, projector, coefficients), adjoint)
    mass = branch.get(group.identity, 0j)
    if abs(mass.imag) > TOL or mass.real < -TOL:
        raise ArithmeticError("invalid projector outcome mass")
    if mass.real < 1e-12:
        if branch:
            raise ArithmeticError("zero-mass branch has a nonzero operator")
        return 0.0, None
    return float(mass.real), {g: value/mass.real for g, value in branch.items()}


def central_descent_packet(group, records, weights):
    """Regular-trace contraction, with no hidden subgroup or expected output.

    F(g)=product_i Tr(rho_i R_Delta_si(g)). Checking its whole sparse support
    and central fibers proves equality for EVERY address pair, not a few
    selected matrix entries. Constancy is tested, never assumed.
    """
    active = check_moment(tuple(label for label, _ in records), weights, group.p, group.stage)
    supports = [{group.dilate(group.inv(k), pow(weights[i], -1, group.p)) for k in records[i][1]}
                for i in active]
    candidates = set.intersection(*supports)
    correlation = {}
    for g in candidates:
        value = np.prod([records[i][1].get(group.inv(group.dilate(g, weights[i])), 0j) for i in active])
        if abs(value) > 1e-12:
            correlation[g] = complex(value)
    for g, value in correlation.items():
        for _, z in group.center_points:
            if abs(correlation.get(group.mul(g, z), 0j)-value) > TOL:
                raise ArithmeticError("output does not descend to a quotient density")
    out, quotient = {}, group.quotient
    for g, value in correlation.items():
        key = quotient.inv(group.project(g))
        if key in out and abs(out[key]-value) > TOL:
            raise ArithmeticError("representative-dependent quotient coefficient")
        out[key] = value
    if abs(out.get(quotient.identity, 0j)-1) > TOL:
        raise ArithmeticError("quotient state lost normalization")
    return out


def tuple_oracle_source(oracle):
    """Exhaustive finite emulation of the tuple oracle's complete density.

    This enumerates 5^7 inputs. It must NEVER be advertised as the efficient
    source preparation or as discovering H with a few classical queries.
    """
    group = ReesFiliformFixture()
    fibers = defaultdict(set)
    for a in product(range(5), repeat=7):
        fibers[tuple(oracle(group.evaluate(a, s)) for s in (1, 2, 3))].add(a)
    zero_label = tuple(oracle((0,)*4) for _ in range(3))
    identity_fiber = fibers[zero_label]
    for fiber in fibers.values():
        a = min(fiber)
        if fiber != {group.mul(a, h) for h in identity_fiber}:
            raise ArithmeticError("tuple oracle does not have the claimed coset partition")
    return {h: 1.0+0j for h in identity_fiber}, len(fibers)


def _coefficient_error(actual, expected):
    return max((abs(actual.get(g, 0j)-expected.get(g, 0j))
                for g in actual.keys() | expected.keys()), default=0.0)


def _fourier_support(coefficients, prime=5):
    if prime not in (5, 7):
        raise ValueError("bounded Fourier control requires F5 or F7")
    frequencies, probabilities = [], []
    for frequency in product(range(prime), repeat=4):
        value = sum(c*np.exp(2j*np.pi*sum(a*b for a, b in zip(frequency, g))/prime)
                    for g, c in coefficients.items())/prime**4
        if abs(value.imag) > TOL or value.real < -TOL:
            raise ArithmeticError("invalid Fourier probability")
        if value.real > 1e-12:
            frequencies.append(frequency)
            probabilities.append(float(value.real))
    if abs(sum(probabilities)-1) > TOL:
        raise ArithmeticError("Fourier distribution lost mass")
    return frequencies, probabilities


def audit_case(kind, random_records=32):
    if kind not in ("X+W", "Z+W") or type(random_records) is not int or not 0 <= random_records <= 128:
        raise ValueError("bounded named fixture and at most128 random records required")
    hidden = {(t, 0, 0, t) if kind == "X+W" else (0, 0, t, t) for t in range(5)}
    oracle = {g: min(source_multiply(g, h) for h in hidden) for g in product(range(5), repeat=4)}
    coefficients, fiber_count = tuple_oracle_source(oracle.__getitem__)
    original_lift = coefficients.copy()
    stages, rng = [], random.Random(1811)
    for stage in (3, 2):
        group = ReesFiliformFixture(stage)
        expected = {group.project(g): 1.0+0j for g in coefficients}
        branches = {label: conditioned_coefficients(group, coefficients, label)
                    for label, _ in group.center_points}
        allowed = tuple(label for label, (mass, _) in branches.items() if mass)
        if abs(sum(mass for mass, _ in branches.values())-1) > TOL:
            raise ArithmeticError("incomplete central instrument")
        if stage == 3:
            tuples = tuple(product(allowed, repeat=2))
        else:
            tuples = tuple((label,)*5 for label in allowed)+tuple(
                tuple(rng.choice(allowed) for _ in range(5)) for _ in range(random_records))
        maximum_error, actual = 0.0, None
        for labels in tuples:
            if stage == 3:
                weights, _, _, _ = solve_bezout_sde_weights(5, labels, 3)
            else:
                # 5^5 assignments satisfy the TEST cap. Not a scalable solver.
                weights = exhaustive_scale_fixture(labels, 5, 2)
            records = tuple((label, branches[label][1]) for label in labels)
            out = central_descent_packet(group, records, weights)
            error = _coefficient_error(out, expected)
            if error > TOL:
                raise ArithmeticError("incorrect complete quotient source")
            maximum_error = max(maximum_error, error)
            actual = out if actual is None else actual
        coefficients = actual
        stages.append({"degree": stage, "center_rank": len(group.center_points[0][0]),
                       "positive_labels": len(allowed), "tested_label_tuples": len(tuples),
                       "distinct_label_tuples": len(set(tuples)),
                       "all_positive_label_tuples_checked": stage == 3,
                       "raw_input_arity": 2 if stage == 3 else 5,
                       "maximum_regular_coefficient_error": maximum_error,
                       "output_regular_support_size": len(coefficients)})
    if set(coefficients) != hidden:
        raise ArithmeticError("grade one did not recover the ORIGINAL hidden subspace")
    frequencies, probabilities = _fourier_support(coefficients)
    basis = affine_solution(5, frequencies, [0]*len(frequencies), 4)["basis"]
    recovered = {tuple(sum(a*v[j] for a, v in zip(weights, basis)) % 5 for j in range(4))
                 for weights in product(range(5), repeat=len(basis))}
    if recovered != hidden:
        raise ArithmeticError("final Fourier annihilator recovery is wrong")
    sampled_successes = 0
    for _ in range(32):
        sampled = rng.choices(frequencies, weights=probabilities, k=12)
        sample_basis = affine_solution(5, sampled, [0]*len(sampled), 4)["basis"]
        sampled_successes += len(sample_basis) == len(basis)
    return {"hidden_fixture": kind, "original_group_order": 625, "cover_order": 78125,
            "cover_dimension": 7, "tuple_evaluations": 3, "all_tuple_fibers_checked": True,
            "tuple_fiber_count": fiber_count, "lifted_subgroup_order": len(original_lift),
            "stages": stages, "full_original_subspace_recovered": True,
            "recovered_basis": basis, "final_fourier_support_size": len(frequencies),
            "twelve_sample_recoveries": sampled_successes, "sampling_trials": 32,
            "lifted_copies_per_final_packet": prod(row["raw_input_arity"] for row in stages),
            "ideal_original_oracle_queries_per_final_packet": 3*prod(row["raw_input_arity"] for row in stages)}


def nonbijective_cubic_control(kind, seed=1913):
    """F7 actual mixed-state descent with solver-produced cubic scales.

    This starts from a known finite coset density, NOT an emulated hiding
    oracle. The selected nonzero character records are test branches, not
    free postselection or a claim that all label tuples were enumerated.
    """
    if kind not in ("X+W", "Z+W"):
        raise ValueError("bounded named hidden-line control required")
    p, rng = 7, random.Random(seed)
    hidden = {(t, 0, 0, t) if kind == "X+W" else (0, 0, t, t) for t in range(p)}
    lift = ({(t, 0, 0, t, 0, 0, 0) for t in range(p)} if kind == "X+W" else
            {(0, 0, t, t, u, u, 0) for t, u in product(range(p), repeat=2)})
    coefficients = {h: 1+0j for h in lift}
    stages = []
    for stage in (3, 2):
        group = ReesFiliformFixture(stage, p)
        branches = {label: conditioned_coefficients(group, coefficients, label)
                    for label, _ in group.center_points}
        if abs(sum(mass for mass, _ in branches.values())-1) > TOL:
            raise ArithmeticError("incomplete F7 central instrument")
        allowed = tuple(label for label, (mass, _) in branches.items() if mass and any(label))
        count = cubic_arity(1) if stage == 3 else 9
        labels = tuple(rng.choice(allowed) for _ in range(count))
        if stage == 3:
            cubic = cubic_weights(p, labels, rng=rng)
            weights = cubic.weights
        else:
            weights = square_weights_capped(p, labels, rng)
        records = tuple((label, branches[label][1]) for label in labels)
        actual = central_descent_packet(group, records, weights)
        expected = {group.project(g): 1+0j for g in coefficients}
        error = _coefficient_error(actual, expected)
        if error > TOL:
            raise ArithmeticError("solver-backed quotient source differs from the hidden image")
        stages.append(dict(degree=stage, raw_conditional_input_count=count,
                           nonzero_scales=sum(bool(s) for s in weights),
                           maximum_regular_coefficient_error=error,
                           output_regular_support_size=len(actual)))
        coefficients = actual
    frequencies, probabilities = _fourier_support(coefficients, p)
    basis = affine_solution(p, frequencies, [0]*len(frequencies), 4)["basis"]
    recovered = {tuple(sum(a*v[j] for a, v in zip(weights, basis)) % p for j in range(4))
                 for weights in product(range(p), repeat=len(basis))}
    if recovered != hidden:
        raise ArithmeticError("F7 final Fourier distribution does not recover the original line")
    return dict(prime=p, hidden_fixture=kind, initial_regular_support_size=len(lift),
                original_input_is_explicit_finite_coset_density=True,
                tuple_oracle_source_replayed=False, cubic_method=cubic.method,
                cubic_collision_nodes=cubic.collision_nodes, cubic_root_calls=cubic.root_calls,
                selected_nonzero_records_not_iid_sampling=True, all_label_tuples_checked=False,
                stages=stages, recovered_basis=basis, final_fourier_support_size=len(frequencies),
                full_original_subspace_recovered=True, fourier_mass=sum(probabilities))


def report():
    return {"status": "bounded_end_to_end_falsifier_not_a_quantum_implementation",
            "coefficient_convention": "rho=sum_g coefficient[g]*R_g/group_order",
            "arithmetic": "exact_F5_F7_group_operations_with_floating_point_character_phases",
            "cases": [audit_case(kind) for kind in ("X+W", "Z+W")],
            "nonbijective_cubic_controls": [nonbijective_cubic_control(kind) for kind in ("X+W", "Z+W")],
            "full_regular_operator_kernels_checked_per_tested_record": True,
            "all_second_stage_label_tuples_checked": False,
            "quadratic_witness_search": "bounded_exhaustive_F5_fixture_only",
            "tuple_source_emulation": "exhaustive_5_to_7_address_enumeration_not_an_efficient_backend",
            "independent_review": False, "formal_verification": False,
            "asymptotic_runtime_tested": False, "quantum_receiver_implemented": False,
            "novelty_established": False, "speedup_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = report()
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/rees_complete_instrument.json"
        path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
