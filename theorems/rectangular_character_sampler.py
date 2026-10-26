"""Classical QCT basis-column sampling via the known rim-hook correspondence.

Scope: a public S_(km) class of type k^m, then irrep-label measurement.
Not a coherent QCT, HSP coset sampler, or new combinatorial algorithm.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from fractions import Fraction as Q
import json
from math import factorial, prod
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.representation_obstruction import hook_length_dimension, integer_partitions
from theorems.symmetric_character import symmetric_character

REPORT = ROOT / "research/classical_baselines/rectangular_character_sampler.json"


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"positive integer {name} required")
    return value


def _partition(shape):
    if (type(shape) is not tuple
            or any(type(x) is not int or x < 1 for x in shape)
            or any(a < b for a, b in zip(shape, shape[1:]))):
        raise ValueError("nonincreasing immutable positive partition required")
    return shape


def rsk_shape(word):
    """Ordinary row insertion for a distinct-letter word, not a new RSK."""
    if type(word) is not tuple or any(type(x) is not int for x in word) or len(set(word)) != len(word):
        raise ValueError("immutable distinct integer word required")
    rows = []
    for value in word:
        for row in rows:
            j = bisect_right(row, value)
            if j == len(row):
                row.append(value)
                break
            row[j], value = value, row[j]
        else:
            rows.append([value])
    return tuple(len(row) for row in rows)


def assemble_quotient(quotient):
    """Littlewood abacus assembly with equal runner populations (empty core)."""
    if type(quotient) is not tuple or not quotient:
        raise ValueError("nonempty immutable quotient required")
    for shape in quotient:
        _partition(shape)
    k = len(quotient)
    length = max(map(len, quotient))
    beta = []
    for runner, shape in enumerate(quotient):
        padded = shape+(0,)*(length-len(shape))
        beta.extend(k*(part+length-i-1)+runner for i, part in enumerate(padded))
    beta.sort(reverse=True)
    shape = tuple(value-len(beta)+i+1 for i, value in enumerate(beta) if value-len(beta)+i+1 > 0)
    _partition(shape)
    if sum(shape) != k*sum(map(sum, quotient)):
        raise ArithmeticError("empty-core quotient size identity failed")
    return shape


def empty_core_quotient(shape, k):
    """Return the k-quotient, or None for a nonempty k-core."""
    _partition(shape)
    _positive(k, "cycle length")
    width = ((len(shape)+k-1)//k)*k
    padded = shape+(0,)*(width-len(shape))
    beta = tuple(part+width-i-1 for i, part in enumerate(padded))
    runners = tuple(tuple(value//k for value in beta if value % k == j) for j in range(k))
    if any(len(runner) != width//k for runner in runners):
        return None
    return tuple(tuple(value-len(runner)+i+1 for i, value in enumerate(runner)
                       if value-len(runner)+i+1 > 0) for runner in runners)


def column_probability(shape, k, m):
    """Exact point probability, with no group or partition-table enumeration."""
    _positive(k, "cycle length")
    _positive(m, "cycle count")
    _partition(shape)
    if sum(shape) != k*m:
        raise ValueError("partition degree must equal k*m")
    quotient = empty_core_quotient(shape, k)
    if quotient is None:
        return Q(0)
    sizes = tuple(map(sum, quotient))
    if sum(sizes) != m:
        raise ArithmeticError("quotient size mismatch")
    magnitude = factorial(m)*prod(hook_length_dimension(p) for p in quotient)
    denominator = prod(factorial(size) for size in sizes)
    magnitude, remainder = divmod(magnitude, denominator)
    if remainder:
        raise ArithmeticError("character magnitude is not integral")
    return Q(magnitude*magnitude, k**m*factorial(m))


def colored_permutation_shape(permutation, colors, k):
    """Shape map used by BOTH the live sampler and exhaustive source controls."""
    _positive(k, "cycle length")
    if (type(permutation) is not tuple or any(type(x) is not int for x in permutation)
            or set(permutation) != set(range(len(permutation)))):
        raise ValueError("canonical immutable permutation required")
    if (type(colors) is not tuple or len(colors) != len(permutation)
            or any(type(x) is not int or not 0 <= x < k for x in colors)):
        raise ValueError("matching immutable colors in range(k) required")
    words = [[] for _ in range(k)]
    for value, color in zip(permutation, colors):
        words[color].append(value)
    quotient = tuple(rsk_shape(tuple(word)) for word in words)
    shape = assemble_quotient(quotient)
    if empty_core_quotient(shape, k) != quotient:
        raise ArithmeticError("quotient assembly failed its inverse")
    return shape


def sample(k, m, rng):
    _positive(k, "cycle length")
    _positive(m, "cycle count")
    permutation = list(range(m))
    rng.shuffle(permutation)
    colors = tuple(rng.randrange(k) for _ in range(m))
    return colored_permutation_shape(tuple(permutation), colors, k)


def exact_column_controls(max_degree=16):
    """Small independent MN audit only; never called by the scalable sampler."""
    if type(max_degree) is not int or not 1 <= max_degree <= 20:
        raise ValueError("explicit MN control cap must lie in [1,20]")
    cases, partitions = 0, 0
    for n in range(1, max_degree+1):
        for k in range(1, n+1):
            if n % k:
                continue
            m = n//k
            total = Q(0)
            for shape in integer_partitions(n):
                expected = Q(symmetric_character(shape, (k,)*m)**2, k**m*factorial(m))
                actual = column_probability(shape, k, m)
                if actual != expected:
                    raise ArithmeticError(f"MN disagreement at {shape}, {k}^{m}")
                total += actual
                partitions += 1
            if total != 1:
                raise ArithmeticError("column normalization failed")
            cases += 1
    return {"maximum_degree": max_degree, "complete_columns": cases,
            "partition_column_pairs": partitions, "exact_mn_agreement": True}


def report():
    native = []
    for k, m, seed in ((2, 2048, 2026102037), (3, 1365, 2026102039)):
        rng = random.Random(seed)
        start = time.perf_counter()
        shapes = tuple(sample(k, m, rng) for _ in range(64))
        elapsed = time.perf_counter()-start
        # Certify the first sample arithmetically without summing over labels.
        mass = column_probability(shapes[0], k, m)
        class_size = factorial(k*m)//(k**m*factorial(m))
        native.append({
            "degree": k*m, "cycle_length": k, "cycle_count": m,
            "seed": seed, "sample_count": len(shapes),
            "samples": shapes, "sampling_seconds": elapsed,
            "all_sizes_and_empty_cores_verified": all(
                sum(shape) == k*m and empty_core_quotient(shape, k) is not None for shape in shapes),
            "first_sample_mass_numerator_hex": hex(mass.numerator),
            "first_sample_mass_denominator_hex": hex(mass.denominator),
            "conjugacy_class_size_bits": class_size.bit_length(),
            "source_random_objects": "one uniform S_m permutation and m independent uniform k-colors per sample",
            "prng_is_not_a_certified_fair_coin_source": True,
            "full_partition_enumeration_used": False,
            "full_group_enumeration_used": False,
            "rejection_postselection_used": False,
        })
    controls = exact_column_controls()
    return {
        "id": "RECTANGULAR-CYCLE-CHARACTER-SAMPLER",
        "status": "known_classical_correspondence_applied_to_a_scoped_quantum_output_law",
        "question": "Is QCT basis-column readout for public cycle type k^m a new hard sampling primitive?",
        "answer": "No: known quotient/RSK constructions sample the entire law in polynomial time in n=km.",
        "law": "Pr(lambda)=chi_lambda(k^m)^2/(k^m m!)",
        "quantum_algorithm_executed": False,
        "new_algorithm_claimed": False,
        "native": native,
        "controls": controls,
        "exclusions": [
            "coherent superpositions or sequences of character transforms",
            "HSP weak-Fourier, joint Kronecker or hidden-involution label laws",
            "arbitrary mixed cycle types with signed rim-hook cancellations",
            "classical preparation of the coherent character state",
            "polynomial complexity in log(n) for a succinct class descriptor",
        ],
        "prior_art": [
            "https://arxiv.org/html/2610.16827v1",
            "https://doi.org/10.1016/0097-3165(85)90088-3",
            "https://arxiv.org/html/1701.04963",
        ],
        "next_gate": "Require interference, a different output law, and a useful explicit task before reopening QCT as a lead.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"report": str(args.output), "controls": result["controls"],
                      "native": [{key: row[key] for key in
                                  ("degree", "cycle_length", "sample_count", "sampling_seconds")}
                                 for row in result["native"]]}, indent=2))


if __name__ == "__main__":
    main()
