"""Binary degree-two closure countercertificates, not an algebraic lower bound.

See INVERSE_TRACE_QUADRATIC_CLOSURE.md for the all-size extension argument.
Dense controls are deliberately capped; no quantum or native solver is added.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from math import isqrt, prod
from pathlib import Path
from random import Random

from theorems.balanced_codeword_filter import integer, reciprocal_trace, trace_mask
from theorems.cubic_rs_affine_flats import solve_binary
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_algebraic_audit import compiled_relations


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/inverse_trace_quadratic_closure.json"


def set_bits(word):
    while word:
        bit = word & -word
        yield bit.bit_length()-1
        word ^= bit


def pack(bits, values):
    return sum(value << (bits*i) for i, value in enumerate(values))


def slice_hull_certificate(bits):
    integer(bits, 5, 128, "field bits")
    q = 1 << bits
    root = isqrt(q)
    bound = 1+2*(root+int(root*root != q))
    assert bound < q//2
    return {"bits": bits, "character_sum_upper": bound, "slice_size": q//2,
            "affine_dimension": 2*bits-1, "augmented_rank": 2*bits,
            "claim": "AFFINE_HULL_IS_EXACTLY_TRACE_Y_EQUALS_TARGET",
            "field_enumerated": False, "independently_reviewed": False}


def conditioned_lift(bits, target, x_mean, y_mean, seed=1022, samples=None, rng=None):
    """Odd affine combination of native points from the SAME target slice."""
    slice_hull_certificate(bits)
    integer(target, 0, 1, "target")
    for word in (x_mean, y_mean):
        integer(word, 0, (1 << bits)-1, "projected element")
    trace = trace_mask(bits, 1)
    if (trace & y_mean).bit_count() % 2 != target:
        raise ValueError("projected y must have the required trace")
    samples = 8*bits if samples is None else samples
    integer(samples, 1, 100_000, "sample cap")
    rng = Random(seed) if rng is None else rng
    graph = []
    for _ in range(samples):
        y = rng.getrandbits(bits)
        integer(y, 0, (1 << bits)-1, "sampled element")
        if (trace & y).bit_count() % 2 != target:
            y ^= trace & -trace
        x = encoded(element(bits, y)**-1) if y else 0
        graph.append((x, y))
    columns = [1 | (x << 1) | (y << (bits+1)) for x, y in graph]
    wanted = 1 | (x_mean << 1) | (y_mean << (bits+1))
    system = solve_binary([(sum(((column >> j) & 1) << k for k, column in enumerate(columns)),
                            (wanted >> j) & 1) for j in range(2*bits+1)], samples)
    result = {"bits": bits, "target": target, "seed": seed, "samples": samples,
              "rank": system["rank"], "required_rank": 2*bits,
              "projected_pair": [x_mean, y_mean], "status": "UNKNOWN_SLICE_SPAN_BUDGET"}
    if system["rank"] != 2*bits:
        return result
    if system["solution"] is None:
        raise ArithmeticError("full slice span did not represent a legal projection")
    selected = [point for j, point in enumerate(graph) if (system["solution"] >> j) & 1]
    mean, moments = 0, [0]*(2*bits)
    for x, y in selected:
        word = x | (y << bits)
        mean ^= word
        for j in set_bits(word):
            moments[j] ^= word
    if len(selected) % 2 != 1 or mean != x_mean | (y_mean << bits):
        raise ArithmeticError("invalid affine combination")
    result.update(status="VERIFIED_TARGET_CONDITIONED_AFFINE_LIFT",
                  selected_graph_points=selected, moment_rows=moments,
                  field_modulus=sum(int(c) << j for j, c in enumerate(field(bits).modulus().coeffs())))
    return result


def support_word(bits, points, checks, support, pivot):
    """Native dual-RS word on K+1 coordinates, normalized to one at pivot."""
    points, support = tuple(points), tuple(support)
    integer(bits, 2, 128, "field bits")
    integer(checks, 1, len(points)-1, "parity checks")
    if len(set(points)) != len(points) or len(set(support)) != checks+1 or len(support) != checks+1:
        raise ValueError("distinct points and exactly K+1 support indices required")
    for a in points:
        integer(a, 0, (1 << bits)-1, "evaluation point")
    for i in support:
        integer(i, 0, len(points)-1, "support index")
    if pivot not in support:
        raise ValueError("pivot must be in support")
    weights = {i: prod((element(bits, points[i] ^ points[j]) for j in support if j != i),
                       start=field(bits).one())**-1 for i in support}
    return tuple(encoded(weights[i]/weights[pivot]) if i in weights else 0 for i in range(len(points)))


def native_linear_rows(bits, points, checks, targets):
    """Independent equation generator for Hx=0 and the trace hyperplanes."""
    length, offset = len(points), bits*len(points)
    rows = []
    for degree in range(checks):
        columns = [encoded(element(bits, a)**degree*element(bits, 1 << j))
                   for a in points for j in range(bits)]
        rows.extend((sum(((c >> bit) & 1) << j for j, c in enumerate(columns)), 0)
                    for bit in range(bits))
    trace = trace_mask(bits, 1)
    rows.extend((trace << (offset+bits*i), b) for i, b in enumerate(targets))
    assert len(rows) == bits*checks+length
    return rows


def verify_moments(bits, points, checks, targets, means, moments, local_lifts):
    """Recompute every linear equation times 1 and every binary variable."""
    slice_hull_certificate(bits)
    integer(checks, 1, len(points)-1, "parity checks")
    width, offset = 2*bits*len(points), bits*len(points)
    if width > 256 or len(set(points)) != len(points) or len(targets) != len(points):
        raise ValueError("bounded distinct points and aligned targets required")
    for point in points:
        integer(point, 0, (1 << bits)-1, "evaluation point")
    for target in targets:
        integer(target, 0, 1, "target")
    integer(means, 0, (1 << width)-1, "projected binary word")
    if len(moments) != width or len(local_lifts) != len(points):
        raise ValueError("wrong matrix or local-certificate dimensions")
    failures = {"symmetry": 0, "boolean_diagonal": 0, "linear": 0,
                "linear_times_variable": 0, "local_certificate": 0, "local_quadratic": 0}
    for j, row in enumerate(moments):
        integer(row, 0, (1 << width)-1, "moment row")
        failures["boolean_diagonal"] += ((row >> j) & 1) != ((means >> j) & 1)
        failures["symmetry"] += sum(((row >> k) & 1) != ((moments[k] >> j) & 1) for k in range(j))
    equations = native_linear_rows(bits, points, checks, targets)
    for linear, rhs in equations:
        failures["linear"] += (linear & means).bit_count() % 2 != rhs
        residual = means if rhs else 0
        for j in set_bits(linear):
            residual ^= moments[j]
        failures["linear_times_variable"] += residual.bit_count()
    for i, local in enumerate(local_lifts):
        indices = list(range(bits*i, bits*(i+1)))+list(range(offset+bits*i, offset+bits*(i+1)))
        local_mean = sum(((means >> j) & 1) << k for k, j in enumerate(indices))
        local_matrix = [sum(((moments[j] >> k) & 1) << t for t, k in enumerate(indices)) for j in indices]
        replay_mean, replay_matrix = 0, [0]*(2*bits)
        selected = local["selected_graph_points"]
        failures["local_certificate"] += len(selected) % 2 != 1
        for x, y in selected:
            integer(x, 0, (1 << bits)-1, "certificate x")
            integer(y, 0, (1 << bits)-1, "certificate y")
            failures["local_certificate"] += y != (encoded(element(bits, x)**-1) if x else 0)
            failures["local_certificate"] += int(element(bits, y).trace()) != targets[i]
            word = x | (y << bits)
            replay_mean ^= word
            for j in set_bits(word):
                replay_matrix[j] ^= word
        failures["local_certificate"] += replay_mean != local_mean
        failures["local_certificate"] += replay_matrix != local_matrix
        for polynomial in compiled_relations(bits):
            value = 0
            for mask, coefficient in polynomial.items():
                variables = list(set_bits(mask))
                if len(variables) == 0:
                    bit = 1
                elif len(variables) == 1:
                    bit = (local_mean >> variables[0]) & 1
                else:
                    bit = (local_matrix[variables[0]] >> variables[1]) & 1
                if bit:
                    value ^= coefficient
            failures["local_quadratic"] += value != 0
    return {"valid": not any(failures.values()), "failures": failures,
            "checked_linear_and_multiplied_equations": len(equations)*(width+1)}


def dense_countercontrol(bits, points, checks, targets, x_means=None, y_means=None, seed=1022):
    """Construct the proof's degree-two extension; NOT a native witness."""
    slice_hull_certificate(bits)
    points, targets = tuple(points), tuple(targets)
    length = len(points)
    integer(checks, 1, length-1, "parity checks")
    if length < 2*checks+1:
        raise ValueError("two separated supports require N >= 2K+1")
    if 2*bits*length > 256:
        raise ValueError("dense verification cap exceeded; use the symbolic theorem")
    if len(targets) != length:
        raise ValueError("one target per point required")
    for b in targets:
        integer(b, 0, 1, "target")
    trace = trace_mask(bits, 1)
    x_means = (0,)*length if x_means is None else tuple(x_means)
    y_means = tuple((trace & -trace)*b for b in targets) if y_means is None else tuple(y_means)
    if len(x_means) != length or len(y_means) != length:
        raise ValueError("one projected pair per point required")
    for a in points+x_means+y_means:
        integer(a, 0, (1 << bits)-1, "field element")
    if len(set(points)) != length:
        raise ValueError("evaluation points must be distinct")
    offset, width = bits*length, 2*bits*length
    means = pack(bits, x_means) | (pack(bits, y_means) << offset)
    if any((linear & means).bit_count() % 2 != rhs
           for linear, rhs in native_linear_rows(bits, points, checks, targets)):
        raise ValueError("projection must satisfy the original linear constraints")
    moments = [means if (means >> j) & 1 else 0 for j in range(width)]

    def symmetric_outer(a, b):
        for j in set_bits(a):
            moments[j] ^= b
        for j in set_bits(b):
            moments[j] ^= a

    lifts = []
    for i in range(length):
        local = conditioned_lift(bits, targets[i], x_means[i], y_means[i], seed=seed+i)
        if local["status"] != "VERIFIED_TARGET_CONDITIONED_AFFINE_LIFT":
            return {"status": "UNKNOWN_SLICE_SPAN_BUDGET", "coordinate": i, "local": local}
        lifts.append(local)
        others = [j for j in range(length) if j != i]
        u = support_word(bits, points, checks, (i, *others[:checks]), i)
        v = support_word(bits, points, checks, (i, *others[checks:2*checks]), i)
        us = [pack(bits, [encoded(element(bits, a)*element(bits, 1 << r)) for a in u]) for r in range(bits)]
        vs = [pack(bits, [encoded(element(bits, a)*element(bits, 1 << r)) for a in v]) for r in range(bits)]
        local_mean = x_means[i] | (y_means[i] << bits)
        covariance = [row ^ (local_mean if (local_mean >> r) & 1 else 0)
                      for r, row in enumerate(local["moment_rows"])]
        for r in range(bits):
            for s in range(r+1, bits):
                if (covariance[r] >> s) & 1:
                    symmetric_outer(us[r], vs[s])
                if (covariance[bits+r] >> (bits+s)) & 1:
                    symmetric_outer(1 << (offset+bits*i+r), 1 << (offset+bits*i+s))
            mixed = covariance[r] >> bits
            symmetric_outer(us[r], mixed << (offset+bits*i))
    verification = verify_moments(bits, points, checks, targets, means, moments, lifts)
    if not verification["valid"]:
        raise ArithmeticError(f"coupled moment extension failed: {verification}")
    return {"status": "VERIFIED_DEGREE_TWO_RELAXATION_POINT", "bits": bits,
            "points": points, "checks": checks, "targets": targets, "seed": seed,
            "projected_x": x_means, "projected_y": y_means,
            "means_hex": hex(means), "moment_rows_hex": list(map(hex, moments)),
            "local_lifts": lifts, "verification": verification,
            "native_witness": all(reciprocal_trace(bits, x) == b for x, b in zip(x_means, targets)),
            "higher_degree_or_general_classical_attack_excluded": False}


def report():
    large = []
    for n in (17, 31, 61):
        t = trace_mask(n, 1)
        large.append(conditioned_lift(n, 1, 0, t & -t, seed=1000*n+22))
    return {"status": "COUPLED_DEGREE_TWO_EXTENSION_THEOREM_REVIEW_PENDING",
            "speedup_or_hardness_established": False,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256((ROOT / "research/INVERSE_TRACE_QUADRATIC_CLOSURE.md").read_bytes()).hexdigest(),
            "slice_hull_certificates": [slice_hull_certificate(n) for n in (5, 17, 31, 61)],
            "large_field_local_lifts_only": large,
            "dense_coupled_controls": [dense_countercontrol(n, tuple(range(length)), k,
                                       tuple(i.bit_count() % 2 for i in range(length)), seed=1000*n+22)
                                       for n, length, k in ((5, 3, 1), (5, 5, 2), (7, 7, 3))]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = report()
    if args.write:
        REPORT.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps({"status": data["status"],
                      "slice_ranks": [r["rank"] for r in data["large_field_local_lifts_only"]],
                      "coupled_checks": [r["verification"] for r in data["dense_coupled_controls"]],
                      "native_witnesses": [r["native_witness"] for r in data["dense_coupled_controls"]]}, indent=2))


if __name__ == "__main__":
    main()
