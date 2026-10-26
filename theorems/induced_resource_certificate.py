"""Conditional fixed-class resource schedule for the induced-source route.

Exact arithmetic and public support counts, not an SDE or quantum receiver.
This does not reuse the old quadratic source-support certificate.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from math import comb, prod
from pathlib import Path

from theorems.full_jet_resource_certificate import Stage, sde_arity, tree_schedule
from theorems.prime_character_opi import ring


def exact_ceil_log(base: int, ratio: Fraction | int) -> int:
    """Minimal exponent with base**exponent >= ratio, with no float logs."""
    if type(base) is not int or base < 2 or type(ratio) not in (int, Fraction) or ratio < 1:
        raise ValueError("base>=2 and exact integer/rational ratio>=1 required")
    value = Fraction(ratio)
    numerator, denominator = value.numerator, value.denominator
    if base == 2:
        candidate = max(0, numerator.bit_length()-denominator.bit_length())
        return candidate+int((denominator << candidate) < numerator)
    low, high = 0, max(1, numerator.bit_length()-denominator.bit_length()+1)
    while pow(base, high)*denominator < numerator:
        high *= 2
    while low < high:
        middle = (low+high)//2
        if pow(base, middle)*denominator >= numerator:
            high = middle
        else:
            low = middle+1
    return low


def jet_monomial_table(multiplicities: tuple[int, ...], degree: int, weight: int):
    """Coefficients of product_j (1-u*v**j)**(-multiplicities[j-1])."""
    if any(type(n) is not int or n < 0 for n in multiplicities) or any(
            type(n) is not int or n < 0 for n in (degree, weight)):
        raise ValueError("nonnegative integer multiplicities and bounds required")
    table = [[0]*(weight+1) for _ in range(degree+1)]
    table[0][0] = 1
    for j, number in enumerate(multiplicities, 1):
        if not number:
            continue
        updated = [[0]*(weight+1) for _ in range(degree+1)]
        for total in range(degree+1):
            for w, value in enumerate(table[total]):
                if value:
                    for used in range(min(degree-total, (weight-w)//j)+1):
                        updated[total+used][w+j*used] += value*comb(number+used-1, used)
        table = updated
    return tuple(map(tuple, table))


def mixed_slice_count(m: int, table, weight: int, q_degree: int, jet_degree: int) -> int:
    if any(type(v) is not int for v in (m, weight, q_degree, jet_degree)) or m < 1 or min(
            weight, q_degree, jet_degree) < 0 or jet_degree >= len(table) or weight >= len(table[0]):
        raise ValueError("valid dimensions, cutoffs and precomputed table required")
    return sum(table[t][w]*comb(m+weight-w-1, weight-w)
               for t in range(jet_degree+1) for w in range(max(0, weight-q_degree), weight+1))


def induced_equation_bounds(m: int, r: int, b: int, degree: int, normal_class: int):
    """Count every allowed parameter/physical monomial pair, stage by stage.

    A degree-h parameter term has q degree<=h*D and jet degree<=k-h.
    At most one parameter belongs to I; pure-A terms have h<=k-1.
    No promise I=N' or I<=N'+Z(N) is used for this conservative envelope.
    """
    if any(type(v) is not int or v < 1 for v in (m, r, b, degree, normal_class)):
        raise ValueError("positive integer dimensions and degrees required")
    d, k = degree, normal_class
    h_a, h_i = r*comb(m+d, m), b*comb(m+d, m)
    multiplicities = tuple(r*comb(m+d-j, m) for j in range(1, d+1))
    table = jet_monomial_table(multiplicities, k-1, k*d)
    parameter_counts = {
        h: (comb(h_a+h-1, h) if h < k else 0) + h_i*comb(h_a+h-2, h-1)
        for h in range(1, k+1)
    }
    weighted = {j: sum(parameter_counts[h]*mixed_slice_count(m, table, j, h*d, k-h)
                        for h in range(1, k+1)) for j in range(1, k*d+1)}
    # The final curve Fourier readout has only linear Q_A dependence.
    ordinary = {j: h_a*comb(m+j-1, j) for j in range(1, d+1)}
    return weighted, ordinary


@dataclass(frozen=True)
class InducedResourceCertificate:
    p: int
    ambient_class: int
    normal_class: int
    m: int
    r: int
    b: int
    epsilon: Fraction
    support_model: str
    features: int
    jet_width: int
    stages: tuple[Stage, ...]
    roots: int
    leaves: int
    batch: int
    scale_draw_cap: int
    leaf_retry_cap: int
    field_draws: int
    binary_rejection_cap: int
    queries: int
    curve_readouts: int
    instruments: int
    logical_registers: int

    @property
    def phase_degree(self):
        return self.ambient_class*self.normal_class

    @property
    def merge_calls(self):
        return sum(stage.nodes for stage in self.stages)

    @property
    def instrument_tolerance(self):
        return self.epsilon/(8*self.instruments)

    @property
    def trial_failure_bound(self):
        return Fraction(self.batch, self.p**self.scale_draw_cap)+Fraction(1, 4*self.p)

    @property
    def failures(self):
        return {
            "leaf_exhaustion": Fraction(self.leaves, 2**self.leaf_retry_cap),
            "annihilator_span": Fraction(self.p**self.m-1, (self.p-1)*self.p**self.roots),
            "binary_field_sampling": Fraction(self.field_draws, 2**self.binary_rejection_cap),
            "complete_instruments": self.instruments*self.instrument_tolerance,
        }

    def validate(self):
        """Check the declared schedule, NOT source promises or solver execution."""
        c, k, m, p = self.ambient_class, self.normal_class, self.m, self.p
        ring(p)
        if any(type(v) is not int or v < 1 for v in (c, k, m, self.r, self.b)) or k < 2 or 2*k > c or p <= k*c:
            raise ValueError("invalid induced-source dimensions/class/field envelope")
        if not isinstance(self.epsilon, Fraction) or not 0 < self.epsilon < 1:
            raise ValueError("exact Fraction epsilon in (0,1) required")
        weighted, ordinary = _equations(c, k, m, self.r, self.b, self.support_model)
        specs = tuple((kind, j, values[j], sde_arity(j, values[j]))
                      for kind, high, values in (("weighted", c*k, weighted), ("ordinary", c, ordinary))
                      for j in range(high, 0, -1))
        assert (self.stages, self.leaves) == tree_schedule(specs, self.roots)
        assert self.features == comb(m+c, m+1) and self.jet_width == self.r*self.features
        assert self.roots == m+exact_ceil_log(p, 4/self.epsilon)
        assert self.batch == (self.features+1)*p.bit_length()+2
        assert self.scale_draw_cap == exact_ceil_log(p, 8*self.batch)
        assert self.leaf_retry_cap == exact_ceil_log(2, 4*self.leaves/self.epsilon)
        assert self.queries == self.leaves*self.leaf_retry_cap*self.batch
        assert self.field_draws == self.queries*self.scale_draw_cap
        assert self.binary_rejection_cap == exact_ceil_log(2, 8*self.field_draws/self.epsilon)
        assert self.curve_readouts == self.roots*prod(s.arity for s in self.stages if s.kind == "ordinary")
        assert self.instruments == self.queries+self.leaves*self.leaf_retry_cap+self.merge_calls+self.curve_readouts+self.roots
        assert self.logical_registers == ((m+self.jet_width)*(1+sum(s.arity-1 for s in self.stages))
                                         + self.batch*(m+self.r+self.b)+m)
        assert self.trial_failure_bound < Fraction(1, 2)
        assert self.failures["leaf_exhaustion"] <= self.epsilon/4
        assert self.failures["annihilator_span"] <= self.epsilon/4
        assert self.failures["binary_field_sampling"] <= self.epsilon/8
        assert sum(self.failures.values()) <= 3*self.epsilon/4
        assert sum(s.nodes*(s.arity-1) for s in self.stages) == self.leaves-self.roots


def _equations(c, k, m, r, b, support_model):
    weighted, ordinary = induced_equation_bounds(m, r, b, c, k)
    if support_model == "generic":
        h, jet = (r+b)*comb(m+c, m), r*comb(m+c, m+1)
        weighted = {j: comb(h+k, k)*comb(m+jet+k*c, k*c) for j in range(1, k*c+1)}
    elif support_model != "induced_support":
        raise ValueError("support model must be induced_support or generic")
    return weighted, ordinary


def induced_resource_certificate(*, p: int, ambient_class: int, normal_class: int,
                                 quotient_width: int, a_width: int, ideal_width: int,
                                 epsilon: Fraction = Fraction(1, 8),
                                 support_model: str = "induced_support"):
    ring(p)
    c, k, m, r, b = ambient_class, normal_class, quotient_width, a_width, ideal_width
    if any(type(v) is not int or v < 1 for v in (c, k, m, r, b)) or k < 2 or 2*k > c or p <= k*c:
        raise ValueError("requires nonabelian derived class 2<=k<=c/2, positive dimensions, p>kc")
    if not isinstance(epsilon, Fraction) or not 0 < epsilon < 1:
        raise ValueError("exact Fraction epsilon in (0,1) required")
    weighted, ordinary = _equations(c, k, m, r, b, support_model)
    specs = tuple((kind, j, values[j], sde_arity(j, values[j]))
                  for kind, high, values in (("weighted", c*k, weighted), ("ordinary", c, ordinary))
                  for j in range(high, 0, -1))
    roots = m+exact_ceil_log(p, 4/epsilon)
    stages, leaves = tree_schedule(specs, roots)
    features = comb(m+c, m+1)
    jet = r*features
    batch = (features+1)*p.bit_length()+2
    scale_cap = exact_ceil_log(p, 8*batch)
    retries = exact_ceil_log(2, 4*leaves/epsilon)
    attempts = leaves*retries
    queries = attempts*batch
    draws = queries*scale_cap
    binary_cap = exact_ceil_log(2, 8*draws/epsilon)
    curve_readouts = roots*prod(s.arity for s in stages if s.kind == "ordinary")
    instruments = queries+attempts+sum(s.nodes for s in stages)+curve_readouts+roots
    logical = (m+jet)*(1+sum(s.arity-1 for s in stages))+batch*(m+r+b)+m
    result = InducedResourceCertificate(p, c, k, m, r, b, epsilon, support_model,
        features, jet, stages, roots, leaves, batch, scale_cap, retries, draws,
        binary_cap, queries, curve_readouts, instruments, logical)
    result.validate()
    return result


def report(c):
    """Small reconstructible report; count exponents are exact UPPER envelopes."""
    c.validate()
    return {
        "schema": "induced_resource_certificate_v1",
        "input": {"p": c.p, "ambient_class": c.ambient_class, "normal_class": c.normal_class,
                  "quotient_width": c.m, "a_width": c.r, "ideal_width": c.b,
                  "epsilon": str(c.epsilon), "support_model": c.support_model},
        "dimensions": {"features": c.features, "jet": c.jet_width, "weighted_degree": c.phase_degree},
        "clocks": {"roots": c.roots, "batch": c.batch, "scale_draws": c.scale_draw_cap,
                   "leaf_retries": c.leaf_retry_cap, "binary_rejections": c.binary_rejection_cap},
        "counts_upper_power_of_two_exponents": {name: exact_ceil_log(2, getattr(c, name)) for name in
            ("leaves", "queries", "field_draws", "merge_calls", "curve_readouts", "instruments", "logical_registers")},
        "stages": [{"kind": s.kind, "degree": s.degree, "equations": s.equations,
                    "arity_upper_power_of_two_exponent": exact_ceil_log(2, s.arity)} for s in c.stages],
        "joint_failure_upper_bound": str(3*c.epsilon/4),
        "required_instrument_precision_bits": exact_ceil_log(2, 1/c.instrument_tolerance),
        "interpretation": "All power-of-two exponents are exact sufficient upper envelopes, NOT measured runtimes or lower bounds. Reconstruct exact counts with the input and factory.",
        "speedup_claim_allowed": False, "receiver_executed": False,
        "dependencies": ["verified source/phase/transport promises", "fresh disjoint inputs and full adaptive records",
                         "published all-input SDE algorithm, not the executable g<=2 subset",
                         "uniform complete-instrument precision including ABORT"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    reports = [report(induced_resource_certificate(p=p, ambient_class=9, normal_class=4,
                quotient_width=2, a_width=7, ideal_width=10, support_model=model))
               for p in (43, 2**127-1) for model in ("induced_support", "generic")]
    result = {"scope": "conditional single transverse-image call at the strict c9/k4 witness dimensions",
              "reports": reports}
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/induced_resource_certificate.json"
        path.write_text(json.dumps(result, indent=2)+"\n")
        print(path)
    for row in reports:
        print(json.dumps({"input": row["input"], "query_upper_power_of_two_exponent":
                          row["counts_upper_power_of_two_exponents"]["queries"]}))
