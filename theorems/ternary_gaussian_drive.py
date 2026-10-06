"""Costed Gaussian-endpoint sparse drive, not a hidden-secret decoder.

LOCAL DERIVATIONS / REVIEW PENDING. Row access does not enumerate the cube.
Dense matrices and secret enumeration below are bounded calibration only.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path

from flint import nmod_mat
import numpy as np
from scipy.linalg import expm

from cyclotomic_fiber_receiver import native_source
from ternary_pointed_triples import (
    _integer, incoming_cases, low_source, pointed_words,
    random_native_source, verify_incoming_case,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_gaussian_drive.json"


def default_nullity_cap(n):
    _integer(n, "dimension")
    b = 0
    while 3**b < n+2:
        b += 1
    return b


def linear_case_solutions(case, cap):
    """Complete affine-kernel enumeration or EXPLICIT graph exclusion.

    The excluded case is not claimed inconsistent. Enumerating the kernel
    costs at most 3**cap; the graph below uses cap=ceil(log_3(n+2)).
    """
    _integer(cap, "nullity cap", 0)
    if case["corner"] != 2 or not case["equations_linear_in_coefficients"]:
        raise ValueError("linear corner2 case required")
    target = tuple(case["target"])
    choices = tuple(case["choice_vectors"])
    k, n = len(choices), len(target)
    if (not n or len(case["coefficient_domains"]) != k
            or any(type(x) is not int or x not in (0, 1, 2) for x in target)
            or any(len(c) != 3 or any(len(v) != n for v in c) for c in choices)
            or any(type(x) is not int or x not in (0, 1, 2)
                   for c in choices for v in c for x in v)
            or any(any(c[0]) or any((a+b) % 3 for a, b in zip(c[1], c[2])) for c in choices)
            or any(not domain or any(type(x) is not int or x not in (0, 1, 2) for x in domain)
                   for domain in case["coefficient_domains"])):
        raise ValueError("canonical GF3 linear case required")
    if k == 0:
        return {"status": "complete", "rank": 0, "nullity": 0,
                "solutions": ((),) if not any(target) else (), "affine_vectors_examined": int(not any(target))}
    A = nmod_mat([[c[1][l] for c in choices] for l in range(n)], 3)
    rank = A.rank()
    nullity = k-rank
    if nullity > cap:
        return {"status": "excluded_nullity", "rank": rank, "nullity": nullity,
                "solutions": (), "affine_vectors_examined": 0}
    reduced, _ = nmod_mat([[*(int(A[l, j]) for j in range(k)), target[l]] for l in range(n)], 3).rref()
    rows = [tuple(int(reduced[i, j]) for j in range(k+1)) for i in range(n)]
    if any(not any(row[:k]) and row[k] for row in rows):
        return {"status": "complete", "rank": rank, "nullity": nullity,
                "solutions": (), "affine_vectors_examined": 0}
    rows = [row for row in rows if any(row[:k])]
    pivots = tuple(next(j for j, x in enumerate(row[:k]) if x) for row in rows)
    free = tuple(j for j in range(k) if j not in pivots)
    solutions = []
    for values in product(range(3), repeat=nullity):
        word = [0]*k
        for j, value in zip(free, values):
            word[j] = value
        for pivot, row in zip(pivots, rows):
            word[pivot] = (row[k]-sum(row[j]*word[j] for j in free)) % 3
        if all(x in domain for x, domain in zip(word, case["coefficient_domains"])):
            solutions.append(tuple(word))
    return {"status": "complete", "rank": rank, "nullity": nullity,
            "solutions": tuple(solutions), "affine_vectors_examined": 3**nullity}


def _graph_parameters(frequencies, vertex, cap):
    record = pointed_words(frequencies, vertex)
    n = len(frequencies[0][0])
    if len(vertex) != n+2:
        raise ValueError("Gaussian endpoint graph requires width n+2")
    cap = default_nullity_cap(n) if cap is None else cap
    _integer(cap, "nullity cap", 0)
    return record, n, cap


def outgoing(frequencies, anchor, cap=None):
    """One actual corner2 arc, conditioned on full rank and case nullity."""
    record, n, cap = _graph_parameters(frequencies, anchor, cap)
    if len(record["kernel_pivots"]) != n:
        return None
    vertex = record["words"][2]
    p = next(i for i, x in enumerate(record["kernel_word"]) if x == 1)
    variables = tuple(i for i in record["kernel_pivots"] if i != p)
    if variables:
        zero = (0,)*n
        tables = tuple((zero, *pair) for pair in frequencies)
        columns = [tuple((tables[i][vertex[i]][l]-tables[i][(vertex[i]-1) % 3][l]) % 3
                         for l in range(n)) for i in variables]
        rank = nmod_mat([[v[l] for v in columns] for l in range(n)], 3).rank()
        if len(variables)-rank > cap:
            return None
    return vertex


def incoming(frequencies, vertex, cap=None):
    """ALL predecessors in the explicitly cut graph, without cube access."""
    _, _, cap = _graph_parameters(frequencies, vertex, cap)
    anchors = set()
    for case in incoming_cases(frequencies, vertex, 2):
        solved = linear_case_solutions(case, cap)
        if solved["status"] == "excluded_nullity":
            continue
        for coefficients in solved["solutions"]:
            anchor = verify_incoming_case(frequencies, vertex, case, coefficients)
            if anchor is not None:
                anchors.add(anchor)
    return tuple(sorted(anchors))


def laplacian_row(frequencies, vertex, cap=None):
    """Sorted sparse row; reverse directed arcs have multiplicity two.

    Both row-index lookup and its inverse use this polynomial bounded list.
    Reversible gate synthesis and padding are obligations, not supplied code.
    """
    neighbors = Counter(incoming(frequencies, vertex, cap))
    target = outgoing(frequencies, vertex, cap)
    if target is not None:
        neighbors[target] += 1
    row = {neighbor: -weight for neighbor, weight in neighbors.items()}
    if neighbors:
        row[tuple(vertex)] = sum(neighbors.values())
    return tuple(sorted(row.items()))


def sparse_row_locations(frequencies, vertex, cap=None):
    """Fixed-width DISTINCT index list, including legal zero-entry padding.

    The reverse index is a search on the same sorted bounded list. This is
    an oracle program, not a provided reversible quantum circuit.
    """
    _, n, cap = _graph_parameters(frequencies, vertex, cap)
    m = n+2
    bound = min(3**m, 2+m*math.comb(m, 2)*3**cap)
    locations = {word for word, _ in laplacian_row(frequencies, vertex, cap)}
    for index in range(bound):
        if len(locations) == bound:
            break
        word = []
        for _ in range(m):
            word.append(index % 3)
            index //= 3
        locations.add(tuple(reversed(word)))
    assert len(locations) == bound
    return tuple(sorted(locations))


def sparse_entry_spec(frequencies, vertex, neighbor, cap=None, source=None):
    """Exact magnitude/sign and root exponent, not a free phase oracle."""
    pointed_words(frequencies, neighbor)  # Validate the target register.
    weight = dict(laplacian_row(frequencies, vertex, cap)).get(tuple(neighbor), 0)
    if source is None or not weight:
        return {"integer_weight": weight, "phase_numerator": 0, "phase_modulus": 1}
    if low_source(source) != tuple(tuple(tuple(v) for v in pair) for pair in frequencies):
        raise ValueError("chirp source must match the low graph")
    q = source.modulus
    h = [chirp_exponent(source, word) for word in (vertex, neighbor)]
    return {"integer_weight": weight, "phase_numerator": (h[0]-h[1]) % q, "phase_modulus": q}


def sparse_entry(frequencies, vertex, neighbor, cap=None, source=None):
    """Floating evaluation of the exact entry spec for bounded calibration."""
    spec = sparse_entry_spec(frequencies, vertex, neighbor, cap, source)
    return spec["integer_weight"]*np.exp(2j*np.pi*float(Fraction(spec["phase_numerator"], spec["phase_modulus"])))


def block_laplacian_row(sources, vertex):
    """Block-sum sparse oracle; the global public chirp need not factor."""
    sources = tuple(sources)
    if not sources or any(s.dimension != sources[0].dimension or s.level != sources[0].level
                          or s.inputs != s.dimension+2 for s in sources):
        raise ValueError("nonempty equal-dimension/equal-level Gaussian source blocks required")
    width = sources[0].inputs
    vertex = tuple(vertex)
    if len(vertex) != width*len(sources):
        raise ValueError("one word coordinate per physical input required")
    row = Counter()
    for b, source in enumerate(sources):
        start = b*width
        word = vertex[start:start+width]
        for neighbor, weight in laplacian_row(low_source(source), word):
            target = vertex[:start]+neighbor+vertex[start+width:]
            row[target] += weight
    return tuple(sorted((word, value) for word, value in row.items() if value))


def gaussian_binomial(k, d):
    _integer(k, "column count", 0)
    _integer(d, "subspace dimension", 0)
    if d > k:
        return 0
    value = Fraction(1)
    for i in range(d):
        value *= Fraction(3**k-3**i, 3**d-3**i)
    assert value.denominator == 1
    return value.numerator


def graph_ledger(n):
    _integer(n, "dimension")
    m, cap = n+2, default_nullity_cap(n)
    C = m*math.comb(m, 2)
    tail = min(Fraction(1), Fraction(gaussian_binomial(n, cap+1), 3**(n*(cap+1))))
    removed = min(Fraction(1), C*tail)
    retained = max(Fraction(0), Fraction(17, 18)-removed)
    degree = 1+C*3**cap
    return {"dimension": n, "width": m, "nullity_cap": cap,
            "inverse_case_count_upper": C, "affine_vectors_per_case_upper": 3**cap,
            "row_weight_degree_upper": degree, "row_nonzeros_upper": degree+1,
            "largest_entry_upper": degree, "operator_norm_upper": 2*degree,
            "native_average_removed_anchor_fraction_upper": str(removed),
            "native_average_retained_directed_arc_fraction_lower": str(retained),
            "primitive_secret_native_average_energy_lower_for_level_at_least4": str(2*retained),
            "bounds_are_pointwise_except_explicit_native_average_mass_and_energy": True,
            "oracle_program_cube_enumeration_required": False,
            "polynomial_claim_uses_logarithmic_cap_not_arbitrary_user_cap": True,
            "reversible_gate_level_compilation_supplied": False,
            "spectral_gap_or_secret_decoder_proved": False}


def low_blind_measurement_ledger(n, level, samples):
    """Native-source average gate for ANY low-label-controlled collective POVM.

    Full labels may be used in unlimited classical postprocessing. High-label
    quantum control violates the premise; extra samples remain charged.
    """
    _integer(n, "dimension")
    _integer(level, "even level", 4)
    _integer(samples, "charged qutrit samples", 0)
    if level % 2:
        raise ValueError("even native level >=4 required")
    q = 3**(level//2)
    secrets = q**n-(q//3)**n
    squared = min(Fraction(1), Fraction(5, 3)**samples/secrets)
    return {"dimension": n, "level": level, "modulus": q, "charged_qutrits": samples,
            "primitive_secret_count": str(secrets), "tensor_fourth_moment_factor": str(Fraction(5, 3)**samples),
            "native_average_decoder_success_squared_upper": str(squared),
            "native_average_decoder_success_upper": f"sqrt({squared})",
            "native_average_decoder_success_upper_approximation": math.sqrt(float(squared)),
            "floating_approximation_may_underflow_exact_fraction_is_authoritative": True,
            "squared_gate_bounds_square_of_mean_success_not_mean_squared_success": True,
            "arbitrary_collective_low_controlled_POVM_included": True,
            "unlimited_full_label_classical_postprocessing_included": True,
            "high_label_quantum_control_included": False,
            "per_fixed_label_lower_bound_or_general_quantum_lower_bound": False,
            "status": "LOCAL_COLLECTIVE_L4_DERIVATION_REVIEW_PENDING"}


def onehot_fourth_moment(coefficients, width):
    """Exact character combinatorics; numerical coefficient arithmetic only."""
    _integer(width, "qutrit width", 0)
    if width > 6:
        raise ValueError("onehot convolution is bounded calibration, width<=6")
    coefficients = np.asarray(coefficients, dtype=complex)
    if coefficients.shape != (3**width,):
        raise ValueError("one coefficient per qutrit word required")
    words = tuple(product(range(3), repeat=width))
    exponents = [tuple(x for j in word for x in ((0, 0), (1, 0), (0, 1))[j]) for word in words]
    convolution = {}
    for i, a in enumerate(coefficients):
        for j, b in enumerate(coefficients):
            key = tuple(x+y for x, y in zip(exponents[i], exponents[j]))
            convolution[key] = convolution.get(key, 0j)+a*b
    return float(sum(abs(x)**2 for x in convolution.values()))


def chirp_exponent(source, word):
    """Exact known FULL-Q phase numerator using modular integer arithmetic."""
    if source.level < 2 or source.level % 2:
        raise ValueError("native even-level source required")
    word = tuple(word)
    if len(word) != source.inputs or any(type(x) is not int or x not in (0, 1, 2) for x in word):
        raise ValueError("canonical native word required")
    return pow(2, -1, source.modulus)*sum(x*x for x in source.value(word)) % source.modulus


def public_chirp(source, words):
    """Floating calibration; no secret or unknown-state inverse is supplied."""
    h = [float(Fraction(chirp_exponent(source, word), source.modulus)) for word in words]
    return np.exp(2j*np.pi*np.asarray(h))


def dense_calibration_laplacian(source, cap=None):
    if source.inputs > 4:
        raise ValueError("dense graph calibration capped at width4")
    words = tuple(product(range(3), repeat=source.inputs))
    indices = {word: i for i, word in enumerate(words)}
    matrix = np.zeros((len(words), len(words)))
    frequencies = low_source(source)
    for i, word in enumerate(words):
        for neighbor, weight in laplacian_row(frequencies, word, cap):
            matrix[i, indices[neighbor]] = weight
    if not np.array_equal(matrix, matrix.T) or np.any(matrix.sum(axis=1)):
        raise ArithmeticError("sparse graph failed Hermitian/zero-row-sum control")
    return words, matrix


def _components(words, edges):
    indices = {word: i for i, word in enumerate(words)}
    parent = list(range(len(words)))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for word, target in edges:
        if target is not None:
            parent[root(indices[word])] = root(indices[target])
    groups = {}
    for i, word in enumerate(words):
        groups.setdefault(root(i), []).append(word)
    return tuple(tuple(group) for group in groups.values())


def rank_one_component_census():
    """All729 low sources and19,683 anchors: bounded exact source theorem."""
    words = tuple(product(range(3), repeat=3))
    histogram = Counter()
    for entries in product(range(3), repeat=6):
        frequencies = tuple(((entries[2*i],), (entries[2*i+1],)) for i in range(3))
        groups = _components(words, ((w, outgoing(frequencies, w)) for w in words))
        histogram[sum(len(group)**2 for group in groups)] += 1
    mean_size = Fraction(sum(size*count for size, count in histogram.items()), 729*27)
    return {"dimension": 1, "block_width": 3, "low_sources_censused": 729,
            "native_anchors_censused": 19683, "component_size_square_sum_histogram": dict(sorted(histogram.items())),
            "mean_size_of_component_containing_uniform_word": str(mean_size),
            "native_average_full_secret_success_upper_for_K_blocks_q3powerR": "min(1,(7357/729)^K/3^R)",
            "at_entropy_width_3K_equalsR_full_secret_success_upper": str(mean_size/27)+" raised to K",
            "arbitrary_full_label_control_preserving_product_components_included": True,
            "cross_component_quantum_operations_or_more_samples_excluded": True,
            "status": "EXACT_BOUNDED_SOURCE_CENSUS_LOCAL_APPLICATION_REVIEW_PENDING"}


def readout_calibration(n, level, seed, times=(0., .7, 1.3), block_count=1):
    """Actual native full-root replay, not random field-oracle evidence."""
    if n not in (1, 2) or level not in (4, 6, 8) or 3**(level//2*n) > 81:
        raise ValueError("calibration requires n1/2, level4/6/8 and at most81 secrets")
    _integer(block_count, "block count")
    if block_count*(n+2) > 6:
        raise ValueError("joint dense calibration capped at six physical qutrits")
    sources = tuple(random_native_source(n, level, seed+b) for b in range(block_count))
    blocks = [dense_calibration_laplacian(source) for source in sources]
    source = native_source([label for s in sources for label in s.labels], level)
    words = tuple(product(range(3), repeat=source.inputs))
    block_size = 3**(n+2)
    q, D = source.modulus, len(words)
    secrets = tuple(product(range(q), repeat=n))
    primitive = [i for i, s in enumerate(secrets) if any(x % 3 for x in s)]
    values = np.asarray([source.value(word) for word in words], dtype=int)
    phases = np.exp(2j*np.pi*(values @ np.asarray(secrets).T % q)/q)/math.sqrt(D)
    chirp = public_chirp(source, words)
    counts = Counter(map(tuple, values))
    pgm = sum(math.sqrt(x/D) for x in counts.values())**2/len(secrets)
    component_blocks = [_components(ws, ((w, outgoing(low_source(s), w)) for w in ws))
                        for s, (ws, _) in zip(sources, blocks)]
    component_pgm = 0.
    component_histogram = Counter()
    for groups in product(*component_blocks):
        frequencies = Counter(source.value(tuple(x for word in choices for x in word))
                              for choices in product(*groups))
        component_histogram[math.prod(map(len, groups))] += 1
        component_pgm += sum(math.sqrt(count) for count in frequencies.values())**2/(D*len(secrets))
    rows = []
    max_error = 0.
    for t in times:
        if not math.isfinite(t):
            raise ValueError("finite calibration time required")
        unitaries = [expm(-1j*t*L) for _, L in blocks]
        max_error = max(max_error, sum(float(np.max(abs(U.conj().T @ U-np.eye(block_size))))
                                       for U in unitaries))
        for dressing in ("low_only", "full_label_quadratic_chirp"):
            output = (phases if dressing == "low_only" else chirp.conj()[:, None]*phases).reshape(
                (block_size,)*block_count+(len(secrets),))
            for axis, U in enumerate(unitaries):
                output = np.moveaxis(np.tensordot(U, output, axes=(1, axis)), 0, axis)
            output = output.reshape(D, len(secrets))
            probabilities = abs(output)**2
            error = float(np.max(abs(probabilities.sum(axis=0)-1)))
            if error > 1e-10:
                raise ArithmeticError("native readout normalization failed")
            rows.append({"time": t, "dressing": dressing,
                         "full_secret_ML_success": float(probabilities.max(axis=1).sum()/len(secrets)),
                         "primitive_secret_ML_success": float(probabilities[:, primitive].max(axis=1).sum()/len(primitive)),
                         "normalization_error": error})
    block_arcs = [sum(outgoing(low_source(s), w) is not None for w in ws) for s, (ws, _) in zip(sources, blocks)]
    energies = []
    for s, (ws, L) in zip(sources, blocks):
        state = np.exp(2j*np.pi*np.asarray([sum(a*b for a, b in zip(s.value(w), secrets[primitive[0]])) % q
                                          for w in ws])/q)/math.sqrt(block_size)
        energies.append(float(np.vdot(state, L @ state).real))
    product_chirp = np.ones(D, dtype=complex)
    for b, s in enumerate(sources):
        projected = tuple(w[b*(n+2):(b+1)*(n+2)] for w in words)
        product_chirp *= public_chirp(s, projected)
    cross_phases = chirp/product_chirp
    return {"dimension": n, "native_level": level, "seed": seed, "modulus": q,
            "native_labels": source.labels, "physical_qutrits": source.inputs,
            "block_count": block_count, "retained_directed_arcs_per_block": block_arcs,
            "cube_size": D, "secret_count": len(secrets),
            "one_primitive_secret_block_sum_energy": sum(energies), "unitarity_error": max_error,
            "global_chirp_differs_from_product_block_chirps": bool(np.max(abs(cross_phases-cross_phases[0])) > 1e-10),
            "block_sparse_row_certificates": [[[list(neighbor), int(weight)] for neighbor, weight in
                                                laplacian_row(low_source(s), w)]
                                               for s, (ws, _) in zip(sources, blocks) for w in ws],
            "known_optimal_PGM_reference_full_secret_success": pgm, "readouts": rows,
            "exact_component_preserving_optimal_full_secret_success": component_pgm,
            "component_size_histogram": dict(sorted(component_histogram.items())),
            "low_blind_native_average_gate": low_blind_measurement_ledger(n, level, source.inputs),
            "dense_cube_and_all_secret_enumeration_are_calibration_only": True,
            "chirp_is_public_and_high_label_dependent": True,
            "chirp_changes_graph_spectrum_or_proves_decoder": False,
            "speedup_claim_allowed": False}


def build_report():
    source = random_native_source(8, 8, 347)
    vertex = tuple(i % 3 for i in range(source.inputs))
    implicit = {"dimension": 8, "native_level": 8, "native_labels": source.labels, "vertex": vertex,
                "sparse_row": [[list(w), int(weight)] for w, weight in laplacian_row(low_source(source), vertex)],
                "nullity_cap": default_nullity_cap(8), "cube_words_not_enumerated": 3**source.inputs}
    return {"schema_version": 1, "status": "LOCAL_DERIVATIONS_REVIEW_PENDING",
            "mechanism": "nullity-cut linear corner2 inversion; sparse native collective Laplacian; public full-label chirp",
            "graph_ledgers": [graph_ledger(n) for n in (1, 2, 4, 8, 16, 32, 64, 128)],
            "near_entropy_low_blind_gates": [low_blind_measurement_ledger(n, 2*r, n*r)
                                            for n, r in ((1, 2), (2, 2), (4, 4), (8, 8), (16, 16))],
            "native_readout_calibrations": [readout_calibration(*case) for case in ((1, 4, 317), (2, 4, 319), (1, 8, 331))]
                                          +[readout_calibration(1, 8, 337, block_count=2)],
            "implicit_oracle_controls": [implicit],
            "rank_one_component_census": rank_one_component_census(),
            "proof_obligations": ["independent mathematical review of source-average coverage and collective L4 gate",
                                  "bounded reversible row-index/entry compilation and precision accounting",
                                  "high-label-controlled receiver with growing-root correctness and sample bounds",
                                  "comparison against legal raw-sample classical inference and known quantum sieves",
                                  "no free frequency-fiber erasure, inverse, normalization or spectral gap"],
            "accepted_quantum_algorithm": False, "generic_quantum_no_go": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
