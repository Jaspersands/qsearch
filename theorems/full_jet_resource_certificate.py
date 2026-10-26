"""Exact resource certificate for the proposed full-jet image receiver.

This computes a conditional theorem's schedule, not a quantum algorithm or
an SDE implementation. See research/FULL_JET_ADAPTIVE_RESOURCE_THEOREM.md.
All clocks use integers/rationals; logarithms in reports are display only.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from math import comb, prod
from pathlib import Path

from theorems.nil3_complete_budget import ceil_log
from theorems.prime_character_opi import ring


def sde_arity(degree: int, equations: int) -> int:
    """Conservative all-input arity; degree is fixed in the cited theorem."""
    if type(degree) is not int or degree < 1:
        raise ValueError("positive integer degree required")
    if type(equations) is not int or equations < 0:
        raise ValueError("nonnegative integer equation count required")
    if degree == 1:
        return equations + 1
    layers = degree.bit_length()  # exactly ceil(log2(degree + 1))
    return (degree ** (degree * (degree - 1) // 2)
            * (equations + 1) ** degree) ** layers


def _homogeneous_count(m: int, degree: int) -> int:
    return comb(m + degree - 1, degree) if degree >= 0 else 0


def weighted_slice_count(m: int, multiplicities: tuple[int, ...], weight: int,
                         q_degree: int, jet_degree: int) -> int:
    """Count q^alpha t^beta at EXACT weight, |alpha|<=q_degree, |beta|<=2."""
    if m < 1 or q_degree < 0 or jet_degree not in (0, 1, 2):
        raise ValueError("positive m, nonnegative q degree and jet degree 0,1,2 required")

    def coefficient(jet_weight):
        degree = weight - jet_weight
        return _homogeneous_count(m, degree) if 0 <= degree <= q_degree else 0

    count = coefficient(0)
    if jet_degree >= 1:
        count += sum(number * coefficient(k) for k, number in enumerate(multiplicities, 1))
    if jet_degree == 2:
        for k, left in enumerate(multiplicities, 1):
            for ell in range(k, len(multiplicities) + 1):
                pairs = left * multiplicities[ell-1] if k != ell else left*(left+1)//2
                count += pairs * coefficient(k+ell)
    return count


def source_equation_bounds(c: int, m: int, r: int, s: int, z: int) -> tuple[dict[int, int], dict[int, int]]:
    """Use the source's three invariant support blocks, not arbitrary jet phases."""
    d, e = c-2, max(c, 3*(c-2))
    ha, hb = r*comb(m+d, m), s*comb(m+d, m)
    hc = z*comb(m+c, m)
    quadratic = ha*(ha+1)//2 + ha*hb
    weights = tuple(r*comb(m+d-k, m) for k in range(1, d+1))
    weighted = {
        j: ((1+hc) * weighted_slice_count(m, weights, j, c, 0)
            + (ha+hb) * weighted_slice_count(m, weights, j, d, 2)
            + quadratic * weighted_slice_count(m, weights, j, 2*d, 1))
        for j in range(1, e+1)
    }
    # After curve Fourier readout the phase is linear in Q_A alone.
    ordinary = {j: (1+ha) * _homogeneous_count(m, j) for j in range(1, d+1)}
    return weighted, ordinary


@dataclass(frozen=True)
class Stage:
    kind: str
    degree: int
    equations: int
    arity: int
    nodes: int


def tree_schedule(stages: tuple[tuple[str, int, int, int], ...], roots: int) -> tuple[tuple[Stage, ...], int]:
    """Bottom-up stages; count nodes by products of arities ABOVE each node."""
    if type(roots) is not int or roots < 1:
        raise ValueError("positive integer root count required")
    needed = roots
    result = []
    for kind, degree, equations, arity in reversed(stages):
        if type(arity) is not int or arity < 2:
            raise ValueError("this envelope requires branching arities >= 2")
        result.append(Stage(kind, degree, equations, arity, needed))
        needed *= arity
    return tuple(reversed(result)), needed


@dataclass(frozen=True)
class FullJetResourceCertificate:
    p: int
    ambient_class: int
    m: int
    r: int
    s: int
    z: int
    epsilon: Fraction
    support_model: str
    degree: int
    phase_degree: int
    features: int
    jet_width: int
    parameters: int
    lifted_parameters: int
    weighted_equations: int
    ordinary_equations: int
    batch: int
    scale_draw_cap: int
    roots: int
    stages: tuple[Stage, ...]
    leaves: int
    leaf_retry_cap: int
    field_draws: int
    binary_rejection_cap: int
    queries: int
    curve_readouts: int
    instruments: int
    logical_registers: int

    @property
    def merge_calls(self) -> int:
        return sum(stage.nodes for stage in self.stages)

    @property
    def instrument_tolerance(self) -> Fraction:
        """Half-diamond distance for EACH complete, history-controlled instrument."""
        return self.epsilon / (8 * self.instruments)

    @property
    def trial_failure_bound(self) -> Fraction:
        return Fraction(self.batch, self.p ** self.scale_draw_cap) + Fraction(1, 4 * self.p)

    @property
    def failures(self) -> dict[str, Fraction]:
        return {
            "leaf_exhaustion": Fraction(self.leaves, 2 ** self.leaf_retry_cap),
            "annihilator_span": Fraction(self.p ** self.m - 1,
                                          (self.p - 1) * self.p ** self.roots),
            "binary_field_sampling": Fraction(self.field_draws, 2 ** self.binary_rejection_cap),
            "complete_instruments": self.instruments * self.instrument_tolerance,
        }

    def validate(self) -> None:
        """Check schedule arithmetic, not physical/source/SDE hypotheses."""
        assert self.trial_failure_bound < Fraction(1, 2)
        failures = self.failures
        assert failures["leaf_exhaustion"] <= self.epsilon / 4
        assert failures["annihilator_span"] <= self.epsilon / 4
        assert failures["binary_field_sampling"] <= self.epsilon / 8
        assert sum(failures.values()) <= 3 * self.epsilon / 4
        assert self.leaves == self.roots * prod(stage.arity for stage in self.stages)
        assert sum(stage.nodes * (stage.arity - 1) for stage in self.stages) == self.leaves - self.roots
        assert self.merge_calls <= self.leaves - self.roots


def full_jet_resource_certificate(
    *, p: int, ambient_class: int, quotient_width: int, a_width: int,
    b_width: int, c_width: int, epsilon: Fraction = Fraction(1, 8),
    support_model: str = "source_structure",
) -> FullJetResourceCertificate:
    ring(p)
    values = (ambient_class, quotient_width, a_width, b_width, c_width)
    if any(type(x) is not int for x in values):
        raise ValueError("integer class and dimensions required")
    c, m, r, s, z = values
    d = c - 2
    e = max(c, 3 * d)
    if c < 4 or p <= e or min(m, r, z) < 1 or s < 0:
        raise ValueError("requires c>=4, p>max(c,3(c-2)), m,r,z>0 and s>=0")
    if not isinstance(epsilon, Fraction) or not 0 < epsilon < 1:
        raise ValueError("exact Fraction epsilon in (0,1) required")
    if support_model not in ("source_structure", "generic"):
        raise ValueError("support model must be source_structure or generic")
    ell = comb(m + d, m + 1)
    jet = r * ell
    h = (r + s) * comb(m + d, m) + z * comb(m + c, m)
    lift = 1 + h + h * (h + 1) // 2
    if support_model == "source_structure":
        weighted, ordinary = source_equation_bounds(c, m, r, s, z)
    else:
        weighted = {j: lift * comb(m + jet + e, e) for j in range(1, e+1)}
        ordinary = {j: lift * comb(m + d, m) for j in range(1, d+1)}
    ew, eo = max(weighted.values()), max(ordinary.values())
    specs = tuple((kind, j, equations[j], sde_arity(j, equations[j]))
                  for kind, high, equations in (("weighted", e, weighted), ("ordinary", d, ordinary))
                  for j in range(high, 0, -1))
    roots = m + ceil_log(p, 4 / epsilon)
    stages, leaves = tree_schedule(specs, roots)
    batch = (ell + 1) * p.bit_length() + 2
    scale_cap = ceil_log(p, 8 * batch)
    retries = ceil_log(2, 4 * leaves / epsilon)
    attempts = leaves * retries
    queries = attempts * batch
    field_draws = queries * scale_cap
    binary_cap = ceil_log(2, 8 * field_draws / epsilon)
    curve_readouts = roots * prod(stage.arity for stage in stages if stage.kind == "ordinary")
    merges = sum(stage.nodes for stage in stages)
    # Source, matrix alignment, merges, curve readout and final Fourier readout.
    instruments = queries + attempts + merges + curve_readouts + roots
    v = m + jet
    logical_registers = (v * (1 + sum(stage.arity - 1 for stage in stages))
                         + batch * (m + r + s + z) + m)
    result = FullJetResourceCertificate(
        p, c, m, r, s, z, epsilon, support_model, d, e, ell, jet, h, lift, ew, eo,
        batch, scale_cap, roots, stages, leaves, retries, field_draws,
        binary_cap, queries, curve_readouts, instruments, logical_registers,
    )
    result.validate()
    return result


def _integer_record(value: int) -> dict[str, object]:
    """Exact serialization without Python's large-decimal conversion limit."""
    return {"hex": hex(value), "floor_log2": value.bit_length() - 1}


def certificate_report(certificate: FullJetResourceCertificate) -> dict[str, object]:
    c = certificate
    return {
        "schema": "full_jet_adaptive_resource_certificate_v1",
        "scope": "conditional schedule; NOT an executed HSP receiver or SDE backend",
        "support_model": c.support_model,
        "input": {"p": c.p, "c": c.ambient_class, "m": c.m, "r": c.r,
                  "s": c.s, "z": c.z, "epsilon": str(c.epsilon)},
        "degrees": {"full_jet": c.degree, "weighted_phase": c.phase_degree},
        "dimensions": {"features": c.features, "jet": c.jet_width,
                       "parameters": c.parameters, "lifted_parameters": c.lifted_parameters,
                       "weighted_equations": c.weighted_equations,
                       "ordinary_equations": c.ordinary_equations},
        "clocks": {"batch": c.batch, "scale_draws": c.scale_draw_cap,
                   "final_roots": c.roots, "leaf_retries": c.leaf_retry_cap,
                   "binary_rejections": c.binary_rejection_cap},
        "counts": {name: _integer_record(getattr(c, name)) for name in
                   ("leaves", "queries", "field_draws", "curve_readouts",
                    "merge_calls", "instruments", "logical_registers")},
        "stages": [{"kind": st.kind, "degree": st.degree, "equations": st.equations,
                    "arity": _integer_record(st.arity), "nodes": _integer_record(st.nodes)}
                   for st in c.stages],
        "failure_bounds": {key: {"numerator": _integer_record(value.numerator),
                                  "denominator": _integer_record(value.denominator)}
                           for key, value in c.failures.items()},
        "joint_failure_at_most": str(3 * c.epsilon / 4),
        "per_complete_instrument_tolerance": {
            "numerator": _integer_record(c.instrument_tolerance.numerator),
            "denominator": _integer_record(c.instrument_tolerance.denominator)},
        "unresolved": ["original-source and common-curve premises must hold",
                       "published deterministic all-input SDE is a dependency, not implemented here",
                       "uniform synthesis must meet COMPLETE instrument tolerance on every history",
                       "logical register count excludes oracle, arithmetic and synthesis ancillas",
                       "no end-to-end Lean theorem, practical resource claim, or novelty claim"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    cases = ((19, 6, 6, 9, 2, 4), (2**127 - 1, 6, 6, 9, 2, 4))
    reports = []
    for p, c, m, r, s, z in cases:
        inputs = dict(p=p, ambient_class=c, quotient_width=m, a_width=r, b_width=s, c_width=z)
        report = certificate_report(full_jet_resource_certificate(**inputs))
        generic = full_jet_resource_certificate(**inputs, support_model="generic")
        report["generic_envelope_queries_floor_log2"] = generic.queries.bit_length()-1
        reports.append(report)
    if args.write:
        path = Path(__file__).resolve().parents[1] / "research/reductions/full_jet_adaptive_resource_certificate.json"
        path.write_text(json.dumps(reports, indent=2) + "\n")
        print(path)
    for report in reports:
        print(json.dumps({"input": report["input"], "clocks": report["clocks"],
                          "query_floor_log2": report["counts"]["queries"]["floor_log2"],
                          "generic_query_floor_log2": report["generic_envelope_queries_floor_log2"],
                          "joint_failure_at_most": report["joint_failure_at_most"]}))


if __name__ == "__main__":
    main()
