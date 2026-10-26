"""A natural ternary BPQM-to-coloring hypothesis with singular-source checks.

Graph cycle codes, signed two-point Fourier sources, exact qutrit node gates,
bounded exact density evolution, and a real classical SAT competitor. No
loopy/block decoder, quantum coloring algorithm or speedup is supplied.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import hashlib
import json
from math import isqrt, sqrt
from pathlib import Path
import random
import sys
import time

import networkx as nx
import numpy as np
from flint import nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer, rational

REPORT = ROOT / "research/phase_workbench/ternary_coloring_bpqm.json"
PHYSICAL = (Fraction(0), Fraction(1, 2), Fraction(1, 2))
OMEGA = np.exp(2j*np.pi/3)


def spectrum(values):
    values = tuple(map(rational, values))
    if len(values) != 3 or any(x < 0 for x in values) or sum(values) != 1:
        raise ValueError("normalized nonnegative ternary Gram eigen-probabilities required")
    return values


def state(mu, symbol):
    mu = spectrum(mu)
    integer(symbol, "canonical ternary input", 0, 2)
    return np.array([sqrt(float(p))*OMEGA**(symbol*j) for j, p in enumerate(mu)])


def bit_spectrum(mu, nu):
    mu, nu = spectrum(mu), spectrum(nu)
    return spectrum(sum(mu[(t-j) % 3]*nu[j] for j in range(3)) for t in range(3))


def check_branches(mu, nu):
    """SUM-check convention: target x+y, herald i-j, message frequency j."""
    mu, nu = spectrum(mu), spectrum(nu)
    branches = []
    for h in range(3):
        weights = tuple(mu[(j+h) % 3]*nu[j] for j in range(3))
        probability = sum(weights)
        if probability:
            branches.append((h, probability, spectrum(w/probability for w in weights)))
    if sum(p for _, p, _ in branches) != 1:
        raise ArithmeticError("check herald probability mass lost")
    return branches


def node_gates(mu, nu):
    """Actual 9x9 SUM permutation and controlled three-level Householders.

    Zero-probability compression blocks get identity, NOT division by zero.
    Check herald phases remain in the two-qutrit state.
    """
    mu, nu = spectrum(mu), spectrum(nu)
    check, relabel, compression = (np.zeros((9, 9), complex) for _ in range(3))
    for i, j in product(range(3), repeat=2):
        check[3*((i-j) % 3)+j, 3*i+j] = 1
        relabel[3*((i+j) % 3)+j, 3*i+j] = 1
    for t in range(3):
        weights = [mu[(t-j) % 3]*nu[j] for j in range(3)]
        norm = sum(weights)
        U = np.eye(3)
        if norm:
            vector = np.sqrt(list(map(float, (w/norm for w in weights))))
            difference = vector-np.array([1., 0., 0.])
            length = float(difference @ difference)
            if length > 1e-28:
                U -= 2*np.outer(difference, difference)/length
        compression[3*t:3*t+3, 3*t:3*t+3] = U
    return check, compression @ relabel


def local_control(mu, nu):
    mu, nu = spectrum(mu), spectrum(nu)
    check, bit = node_gates(mu, nu)
    residuals = []
    combined = bit_spectrum(mu, nu)
    for x in range(3):
        actual = bit @ np.kron(state(mu, x), state(nu, x))
        residuals.append(float(np.max(np.abs(actual-np.kron(state(combined, x), [1., 0., 0.])))))
    for x, y in product(range(3), repeat=2):
        expected = np.zeros(9, complex)
        for h, probability, message in check_branches(mu, nu):
            expected[3*h:3*h+3] = sqrt(float(probability))*OMEGA**(x*h)*state(message, (x+y) % 3)
        residuals.append(float(np.max(np.abs(check @ np.kron(state(mu, x), state(nu, y))-expected))))
    error = max(residuals)
    unitary = max(float(np.max(np.abs(U.conj().T @ U-np.eye(9)))) for U in (check, bit))
    if max(error, unitary) > 1e-11:
        raise ArithmeticError("actual qutrit gate/source identity failed")
    return {"mu": list(map(str, mu)), "nu": list(map(str, nu)),
            "amplitude_identity_max_residual": error, "unitarity_max_residual": unitary,
            "zero_heralds_omitted_only_when_exactly_zero": True,
            "herald_phase_OMEGA_to_x_h_retained": True,
            "large_coherent_reliability_compiler_supplied": False}


def signed_source_control():
    """Fixed public basis change from the existing signed two-point source."""
    Fourier = np.array([[OMEGA**(j*k) for k in range(3)] for j in range(3)])/sqrt(3)
    U = np.diag([1, -1j, 1j]) @ Fourier
    residual = 0.
    for u in range(3):
        original = np.roll(np.array([0., 1., -1.])/sqrt(2), u)
        residual = max(residual, float(np.max(np.abs(U @ original-state(PHYSICAL, u)))))
    if residual > 1e-11:
        raise ArithmeticError("signed native source does not map to the claimed negative channel")
    return {"fixed_basis_change_residual": residual,
            "basis_change": "diag(1,-i,i) times positive-sign ternary Fourier transform",
            "extra_copies_or_postselection_used": False,
            "two_identical_copies_normalized_spectrum": list(map(str, bit_spectrum(PHYSICAL, PHYSICAL))),
            "duplicating_source_changes_zero_temperature_target": True}


def canonical_density(mu):
    """Cyclic gauge for CQ DENSITY statistics only; not a coherent gate rule."""
    mu = spectrum(mu)
    return min(mu[j:]+mu[:j] for j in range(3))


class DensityLimit(RuntimeError):
    pass


def combine_laws(left, right, kind, costs, *, states_cap=256, pairs_cap=50000):
    if kind not in ("bit", "check") or sum(left.values()) != 1 or sum(right.values()) != 1:
        raise ValueError("normalized independent message laws and node kind required")
    result = Counter()
    for mu, p in left.items():
        for nu, q in right.items():
            costs["message_pair_visits"] += 1
            if costs["message_pair_visits"] > pairs_cap:
                raise DensityLimit("UNKNOWN_EXACT_DENSITY_PAIR_CAP; no partial law promoted")
            branches = [(0, Fraction(1), bit_spectrum(mu, nu))] if kind == "bit" else check_branches(mu, nu)
            for _, probability, message in branches:
                result[canonical_density(message)] += p*q*probability
            if len(result) > states_cap:
                raise DensityLimit("UNKNOWN_EXACT_DENSITY_SUPPORT_CAP; no mass dropped or renormalized")
    if sum(result.values()) != 1:
        raise ArithmeticError("density law not exactly normalized")
    return dict(result)


def error_bounds(mu, bits=64):
    mu = spectrum(mu)
    scale, lower, upper = 1 << bits, 0, 0
    for i, j in combinations(range(3), 2):
        x = mu[i]*mu[j]
        floor = isqrt(x.numerator*scale*scale//x.denominator)
        ceiling = floor+int(floor*floor*x.denominator != x.numerator*scale*scale)
        lower += floor
        upper += ceiling
    return max(Fraction(0), Fraction(2*scale-2*upper, 3*scale)), min(Fraction(2, 3), Fraction(2*scale-2*lower, 3*scale))


def singular_step(probability, children):
    """Exact rank-two branch mass; not a decoding-error recursion."""
    probability = rational(probability)
    integer(children, "independent extrinsic check children", 1, 5)
    if not 0 <= probability <= 1:
        raise ValueError("singular branch probability must be in [0,1]")
    return 1-2*(1-probability/2)**children+(1-probability)**children


def singular_support_control(channels):
    """Independently compose actual spectral branches, including zero support.

    Every singular input must be a cyclic physical-source copy. Full-rank
    channels can have arbitrary positive normalized spectra. No environment
    or branch is dropped when computing the actual singular probability.
    """
    channels = tuple(spectrum(mu) for mu in channels)
    integer(len(channels), "bounded check support inputs", 1, 5)
    singular = 0
    for mu in channels:
        if 0 in mu:
            if canonical_density(mu) != canonical_density(PHYSICAL):
                raise ValueError("singular inputs must be the actual physical trine channel")
            singular += 1
    law = {channels[0]: Fraction(1)}
    costs = {"message_pair_visits": 0}
    for mu in channels[1:]:
        law = combine_laws(law, {mu: Fraction(1)}, "check", costs)
    actual = Fraction(0)
    for mu, probability in law.items():
        output = bit_spectrum(PHYSICAL, mu)
        if 0 in output:
            if canonical_density(output) != canonical_density(PHYSICAL):
                raise ArithmeticError("a singular output is not a rotated physical channel")
            actual += probability
    expected = 1-Fraction(2, 2**singular) if singular else Fraction(0)
    if actual != expected:
        raise ArithmeticError("exact support recursion disagrees with full spectral branches")
    return {"input_channels": [list(map(str, mu)) for mu in channels],
            "singular_inputs": singular, "actual_singular_output_mass_exact": str(actual),
            "support_count_prediction_exact": str(expected), "full_branch_mass_exact": "1"}


def singular_density_certificate(degree, *, iterations=64, bits=64):
    """All-depth support certificate using outward-rounded monotone recursion.

    Flags refer to the ideal independent extrinsic tree, never a block
    decoder. Once A*f<1, p_(L+t)<=f*(A*f)^(2^t-1) for the UNROUNDED tree.
    """
    integer(degree, "graph/check degree", 3, 6)
    integer(iterations, "bounded scalar support iterations", 1, 128)
    integer(bits, "outward dyadic support precision", 16, 256)
    children, scale = degree-1, 1 << bits
    quadratic = Fraction(children*(children-1), 4)
    upper, history, contraction = Fraction(1), [], None
    for level in range(iterations+1):
        if quadratic*upper < 1:
            contraction = {"level": level, "singular_mass_upper_exact": str(upper),
                           "quadratic_constant_exact": str(quadratic),
                           "lambda_upper_exact": str(quadratic*upper),
                           "all_later_ideal_tree_bound": "f*lambda^(2^t-1)",
                           "decoding_error_or_block_guarantee_inferred": False}
            break
        if level == iterations:
            break
        value = singular_step(upper, children)
        upper = Fraction(-(-value.numerator*scale//value.denominator), scale)
        history.append({"level": level+1, "singular_mass_upper_exact": str(upper)})
    return {"degree": degree, "recursion": "p_next=1-2*(1-p/2)^(d-1)+(1-p)^(d-1)",
            "outward_rounding_bits": bits, "history": history, "contraction": contraction,
            "global_geometric_factor_upper_exact": {3: "1/2", 4: "3/4", 5: "1681/1728", 6: None}[degree],
            "all_depth_singular_mass_lower_exact": "1/2" if degree == 6 else "0",
            "six_regular_half_mass_invariant_step_exact": "285/512" if degree == 6 else None,
            "singular_mass_vanishes_certified": contraction is not None,
            "word_or_symbol_error_vanishes_inferred": False,
            "cyclic_or_finite_block_receiver_constructed": False}


def density_probe(check_degree, *, levels=3, states_cap=256, pairs_cap=50000):
    """Exact EXTRINSIC dv=2 tree, not copied cyclic graph outputs."""
    integer(check_degree, "graph/check degree", 3, 6)
    integer(levels, "bounded exact density levels", 1, 4)
    law = {canonical_density(PHYSICAL): Fraction(1)}
    physical, costs, history, channels = dict(law), {"message_pair_visits": 0}, [], 1
    status = "BOUNDED_EXACT_TREE_NOT_A_BLOCK_DECODER"
    for level in range(1, levels+1):
        try:
            check = law
            for _ in range(check_degree-2):
                check = combine_laws(check, law, "check", costs, states_cap=states_cap, pairs_cap=pairs_cap)
            law = combine_laws(physical, check, "bit", costs, states_cap=states_cap, pairs_cap=pairs_cap)
        except DensityLimit as error:
            status = str(error)
            break
        channels = 1+(check_degree-1)*channels
        error_low = sum(p*error_bounds(mu)[0] for mu, p in law.items())
        error_high = sum(p*error_bounds(mu)[1] for mu, p in law.items())
        squared_fidelity = sum(p*(3*sum(x*x for x in mu)-1)/2 for mu, p in law.items())
        history.append({"level": level, "exact_message_types": len(law), "distinct_original_tree_outputs": channels,
                        "symbol_error_lower_exact": str(error_low), "symbol_error_upper_exact": str(error_high),
                        "singular_message_mass_exact": str(sum(p for mu, p in law.items() if 0 in mu)),
                        "mean_squared_overlap_exact": str(squared_fidelity), "probability_mass_exact": "1"})
    return {"variable_degree": 2, "check_degree": check_degree, "status": status, "history": history,
            "costs": costs, "cyclic_graph_channels_reused_or_cloned": False,
            "cyclic_gauge_used_for_density_ONLY": True,
            "convergence_or_finite_block_error_proved": False}


def graph_code(vertices, edges):
    integer(vertices, "graph vertices", 2, 512)
    edges = tuple(tuple(e) for e in edges)
    if (not edges or any(len(e) != 2 or any(type(v) is not int for v in e)
                         or not 0 <= e[0] < e[1] < vertices for e in edges)
            or len(set(edges)) != len(edges)):
        raise ValueError("distinct oriented simple edges (u<v) required")
    graph = nx.Graph()
    graph.add_nodes_from(range(vertices))
    graph.add_edges_from(edges)
    if not nx.is_connected(graph):
        raise ValueError("connected graph required; disconnected gauges are not silently discarded")
    index = {edge: i for i, edge in enumerate(edges)}
    basis = []
    for cycle in nx.cycle_basis(graph, root=0):
        row = [0]*len(edges)
        for u, v in zip(cycle, cycle[1:]+cycle[:1]):
            row[index[tuple(sorted((u, v)))]] = 1 if u < v else 2
        basis.append(tuple(row))
    rank = nmod_mat(basis, 3).rank() if basis else 0
    incidence = tuple(tuple((int(v == b)-int(v == a)) % 3 for a, b in edges) for v in range(1, vertices))
    if rank != len(edges)-vertices+1 or nmod_mat(incidence, 3).rank() != vertices-1 or any(sum(a*b for a, b in zip(row, check)) % 3
                                          for row in basis for check in incidence):
        raise ArithmeticError("cycle basis is not the exact ternary incidence kernel")
    return {"vertices": vertices, "edges": edges, "cycles": tuple(basis), "incidence": incidence,
            "code_dimension": rank, "fixed_global_color_gauge_vertex": 0}


def syndrome(code, word):
    if len(word) != len(code["edges"]) or any(type(v) is not int or v not in (0, 1, 2) for v in word):
        raise ValueError("canonical ternary edge word required")
    return tuple(sum(a*b for a, b in zip(row, word)) % 3 for row in code["cycles"])


def valid_coloring(code, offsets, colors):
    if len(colors) != code["vertices"] or any(type(v) is not int or v not in (0, 1, 2) for v in colors):
        return False
    if len(offsets) != len(code["edges"]) or any(type(v) is not int or v not in (0, 1, 2) for v in offsets):
        return False
    return all((colors[v]-colors[u]+j) % 3 for (u, v), j in zip(code["edges"], offsets))


def exact_graph_control(vertices, edges):
    code = graph_code(vertices, edges)
    m, k = len(edges), code["code_dimension"]
    if m > 9 or k > 4 or vertices > 6:
        raise ValueError("UNKNOWN: exponential color/source reference cap")
    supported_words = list(product((1, 2), repeat=m))
    counts = Counter(syndrome(code, y) for y in supported_words)
    sectors = list(product(range(3), repeat=k))
    representatives = {}
    for offsets in product(range(3), repeat=m):
        s = syndrome(code, offsets)
        representatives.setdefault(s, offsets)
        if len(representatives) == 3**k:
            break
    rows = []
    for s in sectors:
        offsets = representatives[s]
        colorings = [(0,)+x for x in product(range(3), repeat=vertices-1)
                     if valid_coloring(code, offsets, (0,)+x)]
        if len(colorings) != counts[s]:
            raise ArithmeticError("original shifted coloring and code-sector counts disagree")
        rows.append({"syndrome": s, "representative_offsets": offsets, "gauge_fixed_colorings": counts[s],
                     "source_sector_probability_exact": str(Fraction(counts[s], 2**m)),
                     "status": "VALID_UNIFORM_COLORING_REFERENCE" if colorings else "EMPTY_TARGET_NO_NORMALIZED_COLORING_LAW"})
    information = list(product(range(3), repeat=k))
    words = [tuple(sum(u*b[j] for u, b in zip(x, code["cycles"])) % 3 for j in range(m)) for x in information]
    Gram = np.array([[float(Fraction(-1, 2)**sum(a != b for a, b in zip(u, v))) for v in words] for u in words])
    physical_source = np.array([[OMEGA**sum(a*b for a, b in zip(d, y))/sqrt(2**m) for d in words]
                                for y in supported_words])
    source_residual = float(np.max(np.abs(physical_source.conj().T @ physical_source-Gram)))
    Fourier = np.array([[OMEGA**sum(a*b for a, b in zip(u, s)) for s in sectors] for u in information])/sqrt(3**k)
    expected = np.array([3**k*counts[s]/2**m for s in sectors])
    residual = float(np.max(np.abs(Fourier.conj().T @ Gram @ Fourier-np.diag(expected))))
    if max(residual, source_residual) > 1e-10:
        raise ArithmeticError("physical negative-overlap Gram spectrum does not match coloring counts")
    rank = sum(counts[s] > 0 for s in sectors)
    success = sum(sqrt(counts[s]/2**m) for s in sectors)**2/3**k
    return {"vertices": vertices, "edges": edges, "code_dimension": k, "cycle_basis_rows": code["cycles"],
            "all_sector_rows": rows, "physical_product_source_Gram_residual": source_residual,
            "total_nonzero_source_words": sum(counts.values()), "actual_Gram_dimension": 3**k,
            "Gram_rank_exact_from_all_sectors": rank, "spectral_identity_max_residual": residual,
            "uniform_original_offset_colorability_probability_exact": str(Fraction(rank, 3**k)),
            "ANY_uniform_codeword_decoder_error_lower_exact": str(Fraction(3**k-rank, 3**k)),
            "optimal_collective_word_error_NUMERICAL": 1-success,
            "ordinary_graph_gauge_fixed_colorings": counts[(0,)*k],
            "exponential_reference_not_an_efficient_decoder_or_sampler": True,
            "all_empty_sectors_retained_not_rerolled": True}


def compressed_shift_countercontrol():
    """The binary constant-gap polar shortcut FAILS between colorable sectors."""
    code = graph_code(4, tuple(combinations(range(4), 2)))
    m, k = len(code["edges"]), code["code_dimension"]
    groups = {}
    for y in product((1, 2), repeat=m):
        groups.setdefault(syndrome(code, y), []).append(y)
    vectors = {}
    for s, words in groups.items():
        vector = np.zeros(3**m)
        for y in words:
            index = 0
            for value in y:
                index = 3*index+value
            vector[index] = 1/sqrt(len(words))
        vectors[s] = vector
    span = np.array(list(vectors.values())).T
    zeros = []
    for s, words in groups.items():
        for edge in range(m):
            delta = tuple(row[edge] for row in code["cycles"])
            t = tuple((x+d) % 3 for x, d in zip(s, delta))
            if not any(delta) or t not in groups or any(y[edge] == 1 for y in words):
                continue
            shifted = np.roll(vectors[s].reshape((3,)*m), 1, axis=edge).reshape(-1)
            projection = span @ (span.T @ shifted)
            if np.linalg.norm(projection) > 1e-12:
                raise ArithmeticError("claimed compressed-shift kernel vector is not in the kernel")
            information_coordinates = next(indices for indices in combinations(range(m), k)
                                           if edge in indices and nmod_mat([[row[j] for j in indices]
                                                                          for row in code["cycles"]], 3).rank() == k)
            zeros.append({"source_syndrome": s, "target_syndrome": t, "edge": edge,
                          "source_valid_count": len(words), "target_valid_count": len(groups[t]),
                          "information_coordinate_extension": information_coordinates,
                          "actual_compressed_shift_norm_numeric": float(np.linalg.norm(projection))})
    if not zeros:
        raise ArithmeticError("no nonempty-to-nonempty compressed-shift counterexample found")
    return {"vertices": 4, "edges": code["edges"], "cycle_basis_rows": code["cycles"],
            "all_zero_transitions_between_NONEMPTY_sectors": zeros,
            "binary_uniform_gap_lemma_extends_to_this_ternary_source": False,
            "all_quantum_coloring_or_BPQM_algorithms_excluded": False,
            "exponential_calibration_span_is_NOT_given_to_the_algorithm": True}


def classical_sat(code, offsets, *, timeout_ms=1000):
    """Public one-hot shifted-coloring SAT baseline; every SAT witness replays."""
    integer(timeout_ms, "classical solver millisecond cap", 1, 60000)
    syndrome(code, offsets)
    try:
        import z3
    except ImportError:
        return {"status": "UNKNOWN_Z3_BASELINE_UNAVAILABLE", "quantum_advantage_inferred": False}
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    variables = [[z3.Bool(f"v{v}_c{c}") for c in range(3)] for v in range(code["vertices"])]
    for row in variables:
        solver.add(z3.Or(row))
        for a, b in combinations(row, 2):
            solver.add(z3.Or(z3.Not(a), z3.Not(b)))
    solver.add(variables[0][0])
    for (u, v), shift in zip(code["edges"], offsets):
        for color in range(3):
            solver.add(z3.Or(z3.Not(variables[u][color]), z3.Not(variables[v][(color-shift) % 3])))
    start = time.perf_counter()
    result = solver.check()
    elapsed = time.perf_counter()-start
    record = {"solver": "Z3", "version": z3.get_version_string(), "timeout_ms": timeout_ms,
              "solve_seconds": elapsed, "Boolean_variables": 3*code["vertices"],
              "status": "UNKNOWN", "quantum_advantage_inferred": False,
              "original_offsets": offsets, "original_edges": code["edges"]}
    if result == z3.sat:
        model = solver.model()
        colors = [next(c for c in range(3) if z3.is_true(model.eval(row[c]))) for row in variables]
        if not valid_coloring(code, offsets, colors):
            raise ArithmeticError("SAT model fails original shifted-coloring constraints")
        record.update(status="CLASSICAL_ORIGINAL_COLORING_WITNESS", colors=colors)
    elif result == z3.unsat:
        record.update(status="SOLVER_UNSAT_NOT_AN_INDEPENDENT_GENERAL_PROOF")
    else:
        record["reason_unknown"] = solver.reason_unknown()
    return record


def regular_word_rank_bound(vertices, degree):
    """ALL-codeword decoder success <=local source rank / message count.

    This is a valid measurement-success bound, NOT dimension->gate hardness
    or a necessary condition for every coloring/sampling algorithm.
    """
    integer(vertices, "analytic regular-graph vertices", 4, 4096)
    integer(degree, "analytic regular-graph degree", 3, 6)
    if degree >= vertices or vertices*degree % 2:
        raise ValueError("possible simple regular-graph parameters required")
    edges = vertices*degree//2
    dimension = edges-vertices+1
    bound = min(Fraction(1), Fraction(2**edges, 3**dimension))
    return {"vertices": vertices, "degree": degree, "edges": edges, "cycle_code_dimension": dimension,
            "mode": "SCALAR_ONLY_NO_GRAPH_OR_STATE_CONSTRUCTION",
            "ANY_uniform_word_decoder_success_upper_exact": str(bound),
            "uniform_original_offset_colorability_upper_exact": str(bound),
            "expected_gauge_fixed_colorings_uniform_offsets_exact": str(Fraction(2**edges, 3**dimension)),
            "arbitrary_fixed_offset_colorability_bound_inferred": False,
            "coloring_or_sampling_impossibility_inferred": False,
            "six_regular_success_bound_equals_one_third_times_8_over_9_to_n": degree == 6}


def run_controls():
    digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    dependency = hashlib.sha256((ROOT/"theorems/bpqm_gibbs_frontier.py").read_bytes()).hexdigest()
    local = [local_control(a, b) for a, b in ((PHYSICAL, PHYSICAL),
             (PHYSICAL, (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))),
             ((1, 0, 0), PHYSICAL), ((Fraction(1, 3),)*3, PHYSICAL))]
    source_control = signed_source_control()
    graphs = [exact_graph_control(3, tuple(combinations(range(3), 2))),
              exact_graph_control(4, tuple(combinations(range(4), 2))),
              exact_graph_control(4, ((0, 1), (1, 2), (2, 3)))]
    density = [density_probe(d) for d in (3, 4, 5, 6)]
    support_controls = [singular_support_control([PHYSICAL]*s+[(Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))]*(r-s))
                        for r in range(1, 6) for s in range(r+1)]
    support_certificates = [singular_density_certificate(d) for d in (3, 4, 5, 6)]
    shift_countercontrol = compressed_shift_countercontrol()
    baselines = []
    for degree, n, seed in ((4, 16, 29), (4, 32, 71), (5, 16, 29), (5, 32, 71)):
        graph = nx.random_regular_graph(degree, n, seed=seed)
        edges = tuple(sorted(tuple(sorted(edge)) for edge in graph.edges()))
        code = graph_code(n, edges)
        rng = random.Random(seed+10000)
        offsets = tuple(rng.randrange(3) for _ in edges)
        baselines.append({"degree": degree, "vertices": n, "graph_seed": seed,
                          "ensemble": "NetworkX_seeded_simple_regular_generator_not_an_IID_certificate",
                          "source_conditioned_on_colorability_or_success": False,
                          "code_dimension": code["code_dimension"], "quantum_decoder_executed": False,
                          "result": classical_sat(code, offsets)})
    if digest != hashlib.sha256(Path(__file__).read_bytes()).hexdigest() or dependency != hashlib.sha256(
            (ROOT/"theorems/bpqm_gibbs_frontier.py").read_bytes()).hexdigest():
        raise RuntimeError("producer or dependency changed during run")
    return {"schema_version": 2, "status": "NATURAL_TERNARY_COLORING_REDUCTION_DECODER_UNPROVED",
            "producer_sha256": digest, "dependency_sha256": {"bpqm_gibbs_frontier.py": dependency},
            "physical_normalized_Gram_spectrum": ["0", "1/2", "1/2"],
            "physical_overlap_exact": "-1/2", "local_unitary_controls": local,
            "signed_native_source_basis_control": source_control,
            "compressed_shift_nonempty_target_countercontrol": shift_countercontrol,
            "exact_graph_source_controls": graphs, "extrinsic_tree_density_probes": density,
            "actual_singular_support_controls": support_controls,
            "all_depth_tree_support_certificates": support_certificates,
            "regular_family_word_rank_bounds_ANALYTIC_ONLY": [regular_word_rank_bound(n, d)
                                                             for n, d in ((64, 4), (64, 5), (64, 6), (256, 6), (1024, 6))],
            "classical_original_input_baselines": baselines,
            "natural_family_word_decoder_implemented": False, "zero_temperature_sampling_reduction_executed": False,
            "no_global_decoder_from_density_evolution_assumed": True,
            "speedup_claim_allowed": False, "accepted_speedup_candidate": False, "no_central_registry_promotion": True,
            "literature": ["https://arxiv.org/abs/2601.21330", "https://arxiv.org/abs/2609.40321"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"],
                      "density": [{"degree": x["check_degree"], "status": x["status"], "levels": len(x["history"])}
                                  for x in report["extrinsic_tree_density_probes"]],
                      "classical": [x["result"]["status"] for x in report["classical_original_input_baselines"]],
                      "speedup_claim_allowed": False}, indent=2))


if __name__ == "__main__":
    main()
