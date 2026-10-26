"""Rank-conditioned rejection and count-window ternary isolation sampling.

Known Gaussian/Prange and universal-hashing mechanisms on unchanged native
inputs. Exact output-law arguments do NOT make hashed SAT a free oracle.
Runtime-capped isolation traces have an additional UNKNOWN timeout mass.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import random
import subprocess
import sys
import time

import numpy as np
from flint import nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.ternary_classical_sampling import (
    REPORT as COUNTS, SAVED_SOURCE, decode, encode, problem_digest, saved_cases, valid, validate_problem,
)
from theorems.ternary_decoded_sampler import affine_lift

REPORT = ROOT / "research/classical_baselines/ternary_conditioned_sampling.json"


def natural(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def power_interval(base, exponent, bits=128):
    """Outward dyadic enclosure, avoiding exponentially long exact powers."""
    base = Fraction(base)
    natural(exponent, "power")
    natural(bits, "enclosure bits", 1)
    if not 0 <= base <= 1:
        raise ValueError("probability base required")
    scale = 1 << bits
    floor = lambda p: p.numerator//p.denominator
    ceil = lambda p: -(-p.numerator//p.denominator)
    lower, upper = floor(base*scale), ceil(base*scale)
    lo = hi = scale
    while exponent:
        if exponent & 1:
            lo, hi = lo*lower//scale, (hi*upper+scale-1)//scale
        lower, upper = lower*lower//scale, (upper*upper+scale-1)//scale
        exponent //= 2
    return Fraction(lo, scale), Fraction(hi, scale)


@dataclass(frozen=True)
class AffineChart:
    H: tuple
    offsets: tuple
    pivots: tuple
    coefficients: tuple
    beta: tuple

    @classmethod
    def build(cls, problem, order=None):
        n, forms, offsets = validate_problem(problem)
        H = tuple(zip(*forms))
        m = len(forms)
        order = tuple(range(m)) if order is None else tuple(order)
        if any(type(i) is not int for i in order) or sorted(order) != list(range(m)):
            raise ValueError("complete original constraint permutation required")
        reduced, rank = nmod_mat([[row[j] for j in order] for row in H], 3).rref()
        pivots = tuple(order[next(j for j in range(m) if reduced[i, j])] for i in range(rank))
        rows = [[0]*m for _ in range(rank)]
        for i in range(rank):
            for j, original in enumerate(order):
                rows[i][original] = int(reduced[i, j])
        if any(sum(H[v][p]*rows[i][j] for i, p in enumerate(pivots)) % 3 != H[v][j]
               for v in range(n) for j in range(m)):
            raise ArithmeticError("column basis fails exact reconstruction of original H")
        beta = tuple((offsets[j]-sum(rows[i][j]*offsets[p] for i, p in enumerate(pivots))) % 3 for j in range(m))
        return cls(H, offsets, pivots, tuple(map(tuple, rows)), beta)

    @property
    def rank(self):
        return len(self.pivots)

    @property
    def gauge(self):
        return len(self.H)-self.rank

    def word(self, signs):
        signs = tuple(signs)
        if len(signs) != self.rank or any(type(x) is not int or x not in (1, 2) for x in signs):
            raise ValueError("one independent nonzero trit per basis column required")
        return tuple((b+sum(signs[i]*row[j] for i, row in enumerate(self.coefficients))) % 3
                     for j, b in enumerate(self.beta))

    def lift(self, word, coins):
        word = tuple(word)
        if len(word) != len(self.offsets) or any(type(y) is not int or y not in (0, 1, 2) for y in word):
            raise ValueError("canonical complete affine word required")
        x = affine_lift(self.H, tuple((y-j) % 3 for y, j in zip(word, self.offsets)), coins)
        if x is None:
            raise ArithmeticError("chart proposal failed its own affine image")
        return x


def syndrome_bridge(problem):
    """Exact full-weight syndrome formulation; no dense-code hardness transfer."""
    chart = AffineChart.build(problem)
    m = len(chart.offsets)
    free = [j for j in range(m) if j not in chart.pivots]
    G = []
    for f in free:
        row = [0]*m
        row[f] = 1
        for i, p in enumerate(chart.pivots):
            row[p] = -chart.coefficients[i][f] % 3
        G.append(row)
    if any(sum(a*b for a, b in zip(g, h)) % 3 for g in G for h in chart.H):
        raise ArithmeticError("dual parity check does not annihilate original generator")
    weights = [sum(x != 0 for x in row) for row in chart.H]
    scope = dense_code_scope(m, chart.rank, min(6, m))
    has_sparse_word = any(0 < w <= 6 for w in weights)
    return {"parity_check_G": G, "syndrome_GJ": [sum(a*b for a, b in zip(g, chart.offsets)) % 3 for g in G],
            "length": m, "syndrome_dimension": len(G), "generated_code_dimension": chart.rank,
            "native_lifts_per_full_weight_word": str(3**chart.gauge),
            "public_generator_row_weights": weights, "public_nonzero_weight_at_most_6_word_supplied": has_sparse_word,
            "random_dense_code_scope_bound": scope,
            "random_dense_code_distribution_claimed": False,
            "large_weight_decoding_search_implies_uniform_sampling": False}


def dense_code_scope(length, dimension, weight):
    """Union bound over low-weight projective lines in a uniform subspace."""
    natural(length, "code length", 1)
    natural(dimension, "code dimension")
    natural(weight, "weight cutoff", 1)
    if dimension > length or weight > length:
        raise ValueError("dimension and weight must fit the code length")
    lines = sum(comb(length, w)*2**(w-1) for w in range(1, weight+1))
    upper = min(Fraction(1), lines*Fraction(3**dimension-1, 3**length-1))
    return {"uniform_dense_subspace_nonzero_low_weight_probability_upper": str(upper),
            "TV_distance_lower_FOR_A_DISTRIBUTION_GUARANTEED_TO_HAVE_SUCH_A_WORD": str(1-upper),
            "low_weight_projective_lines_counted": lines, "weight_cutoff": weight,
            "this_is_NOT_a_runtime_lower_bound": True}


def rank_sample(problem, *, max_trials=1 << 20, seed=1931, batch_size=4096):
    """Polynomial-memory proposal, exact uniform conditional on acceptance.

    The trial cap is fixed, with ABSTAIN after exhaustion. The complete
    proposal space is never enumerated or stored; no SAT/count oracle used.
    """
    natural(max_trials, "fixed proposal budget", 1)
    natural(seed, "seed")
    natural(batch_size, "batch size", 1)
    start, cpu = time.perf_counter(), time.process_time()
    chart = AffineChart.build(problem)
    rng = np.random.default_rng(seed)
    coefficients = np.array(chart.coefficients, dtype=np.int64).reshape(chart.rank, len(chart.offsets))
    beta = np.array(chart.beta, dtype=np.int64)
    computed, used, sample = 0, 0, None
    while computed < max_trials:
        size = min(batch_size, max_trials-computed)
        signs = rng.integers(1, 3, size=(size, chart.rank), dtype=np.int64)
        words = (signs @ coefficients+beta) % 3
        accepted = np.flatnonzero(np.all(words != 0, axis=1))
        before = computed
        computed += size
        if len(accepted):
            first = int(accepted[0])
            used = before+first+1
            sample = chart.lift(tuple(map(int, words[first])), tuple(map(int, rng.integers(0, 3, size=chart.gauge))))
            if not valid(problem, sample):
                raise ArithmeticError("rank proposal failed unchanged native constraints")
            break
    return {"status": "EXACT_CONDITIONAL_UNIFORM_SAMPLE" if sample is not None else "ABSTAIN_FIXED_PROPOSAL_BUDGET",
            "sample": sample, "rank": chart.rank, "gauge_dimension": chart.gauge, "basis_columns": chart.pivots,
            "proposal_domain_size": str(2**chart.rank*3**chart.gauge), "max_trials": max_trials,
            "logical_trials_to_first_success": used or max_trials, "proposals_computed_including_batch_overhead": computed,
            "peak_batch_payload_integer_entries": min(batch_size, max_trials)*(chart.rank+len(chart.offsets)),
            "wall_seconds": time.perf_counter()-start, "CPU_seconds": time.process_time()-cpu,
            "seed": seed, "problem_sha256": problem_digest(problem), "SAT_or_count_oracle_used": False,
            "complete_solution_pool_constructed": False, "uniformity_requires_independent_fair_coins": True,
            "PRNG_seed_is_reproducibility_not_randomness_certificate": True,
            "asymptotic_polynomial_expected_time_claimed": False}


def hash_data(problem, A, b):
    n, _, _ = validate_problem(problem)
    A, b = tuple(map(tuple, A)), tuple(b)
    if len(A) != len(b) or any(len(row) != n or any(type(x) is not int or x not in (0, 1, 2) for x in row)
                              for row in A) or any(type(x) is not int or x not in (0, 1, 2) for x in b):
        raise ValueError("canonical F3 hash matrix and target required")
    return A, b


def cell_cnf(problem, A, b):
    """Unique-extension ternary SUM chains, not exponential dense-form tables."""
    A, b = hash_data(problem, A, b)
    original, support = encode(problem)
    clauses = list(original)
    next_variable = 3*problem["spins"]+1

    def one_hot():
        nonlocal next_variable
        flags = tuple(range(next_variable, next_variable+3))
        next_variable += 3
        clauses.append(flags)
        clauses.extend((-x, -y) for x, y in combinations(flags, 2))
        return flags

    for row, target in zip(A, b):
        # flags[z] denotes the event a*x_i=z, with a^-1=a in F3*.
        terms = [tuple(3*i+(a*z % 3)+1 for z in range(3)) for i, a in enumerate(row) if a]
        if not terms:
            if target:
                clauses.append(())
            continue
        total = terms[0]
        for term in terms[1:]:
            result = one_hot()
            for x, y in product(range(3), repeat=2):
                clauses.append((-total[x], -term[y], result[(x+y) % 3]))
            total = result
        clauses.append((total[target],))
    return tuple(clauses), support, next_variable-1


def solve_cell(problem, A, b):
    """Two-model cutoff; ONE is certified only after iterator exhaustion.

    No propagation/time limit: an unknown result is not an empty cell. SAT
    backend correctness is assumed, not an independently checked proof log.
    """
    import pycosat
    A, b = hash_data(problem, A, b)
    clauses, support, variables = cell_cnf(problem, A, b)
    support = set(support)
    start, cpu = time.perf_counter(), time.process_time()
    models = []
    iterator = pycosat.itersolve(clauses, vars=variables)
    exhausted = False
    try:
        while len(models) < 2:
            try:
                model = next(iterator)
            except StopIteration:
                exhausted = True
                break
            assignment = {abs(lit): lit > 0 for lit in model}
            if len(assignment) != variables or any(not any(assignment[abs(lit)] == (lit > 0) for lit in c) for c in clauses):
                raise ArithmeticError("backend CNF model failed independent replay")
            word = decode(problem, [lit for lit in model if abs(lit) in support])
            if any(sum(a*x for a, x in zip(row, word)) % 3 != target for row, target in zip(A, b)):
                raise ArithmeticError("backend model failed the original ternary hash")
            if word in models:
                raise ArithmeticError("auxiliary multiplicity invalidates native uniqueness")
            models.append(word)
    finally:
        del iterator
    count = len(models)
    return {"status": "UNIQUE" if count == 1 and exhausted else "EMPTY" if count == 0 and exhausted else "MULTIPLE",
            "sample": models[0] if count == 1 and exhausted else None,
            "native_models_seen": count, "iterator_exhausted": exhausted, "CNF_variables": variables,
            "CNF_clauses": len(clauses), "wall_seconds": time.perf_counter()-start,
            "CPU_seconds": time.process_time()-cpu, "backend_version": pycosat.__version__,
            "backend_binary_sha256": hashlib.sha256(Path(pycosat.__file__).read_bytes()).hexdigest(),
            "UNSAT_proof_independently_checked": False}


def annealed_window(problem):
    n, forms, _ = validate_problem(problem)
    mean = 3**n*Fraction(2, 3)**len(forms)
    return mean, max(1, mean.numerator//(2*mean.denominator)), max(1, -(-2*mean.numerator//mean.denominator))


def isolation_shape(upper, epsilon):
    natural(upper, "positive solution-count upper bound", 1)
    epsilon = Fraction(epsilon)
    if not 0 < epsilon < 1:
        raise ValueError("0<epsilon<1 required")
    rows, cells = 0, 1
    while Fraction(upper, cells) > epsilon/(1+epsilon):
        rows, cells = rows+1, 3*cells
    return rows, cells


def isolation_bound(lower, upper, cells, attempts):
    for value, name in ((lower, "count lower"), (upper, "count upper"), (cells, "hash cells"), (attempts, "hash budget")):
        natural(value, name, 1)
    if lower > upper or upper >= cells:
        raise ValueError("positive count window strictly below number of cells required")
    rho = Fraction(upper-1, cells)
    p_lower = Fraction(lower, cells)*(1-rho)
    bias = rho/(1-rho)
    _, failure = power_interval(1-p_lower, attempts)
    return {"count_lower_ASSUMED": lower, "count_upper_ASSUMED": upper, "hash_cells": cells,
            "collision_union_bound": str(rho), "unique_cell_probability_lower": str(p_lower),
            "conditional_sample_TV_upper": str(min(Fraction(1), bias)),
            "fixed_hash_budget_ABSTAIN_probability_upper": str(failure),
            "total_TV_upper_including_fixed_budget_ABSTAIN": str(min(Fraction(1), bias+failure)),
            "independent_uniform_A_and_b_required_including_rank_deficiency": True,
            "bounds_for_UNCAPPED_exact_solver_only": True,
            "extra_runtime_timeout_or_oracle_failure_mass_NOT_bounded": True}


def isolation_sample(problem, *, epsilon="1/4", attempts=256, seed=1931):
    natural(attempts, "fixed hash budget", 1)
    natural(seed, "seed")
    mean, lower, upper = annealed_window(problem)
    rows, cells = isolation_shape(upper, epsilon)
    rng = random.Random(seed)
    traces, sample = [], None
    start, cpu = time.perf_counter(), time.process_time()
    for _ in range(attempts):
        A = tuple(tuple(rng.randrange(3) for _ in range(problem["spins"])) for _ in range(rows))
        b = tuple(rng.randrange(3) for _ in range(rows))
        solved = solve_cell(problem, A, b)
        traces.append({"A": A, "b": b, **solved})
        if solved["status"] == "UNIQUE":
            sample = solved["sample"]
            break
    return {"status": "COMPLETED_UNIQUE_CELL_SAMPLE" if sample is not None else "ABSTAIN_FIXED_HASH_BUDGET",
            "sample": sample, "problem_sha256": problem_digest(problem), "seed": seed, "hash_rows": rows,
            "max_attempts": attempts, "attempts_completed": len(traces), "cell_traces": traces,
            "annealed_mean_NOT_actual_count": str(mean), "claimed_count_window": [lower, upper],
            "conditional_on_count_window_bound": isolation_bound(lower, upper, cells, attempts),
            "count_or_complete_pool_used_as_sampler_input": False, "partial_cell_witness_accepted": False,
            "wall_seconds": time.perf_counter()-start, "CPU_seconds": time.process_time()-cpu,
            "SAT_time_is_paid_not_a_polynomial_time_oracle": True}


def isolation_trace(problem, *, timeout=30, attempts=256, seed=1931):
    """Bounded experiment wrapper, not the uncapped sampler's law certificate."""
    if type(timeout) not in (int, float) or not 0 < timeout <= 3600:
        raise ValueError("explicit finite experiment wall budget required")
    request = {"problem": problem, "attempts": attempts, "seed": seed}
    start = time.perf_counter()
    metadata = {"experiment_wall_budget_seconds": timeout, "problem_sha256": problem_digest(problem),
                "timeout_can_depend_on_hash_and_output": True,
                "capped_sampler_TV_guarantee_certified": False,
                "skip_slow_cells_and_keep_sampling": False}
    try:
        process = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--isolation-worker"],
                                 input=json.dumps(request), text=True, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return {**metadata, "status": "UNKNOWN_HASH_SOLVER_TIMEOUT_NO_SAMPLE", "sample": None,
                "wall_seconds": time.perf_counter()-start, "partial_trace_or_witness_salvaged": False}
    if process.returncode:
        raise RuntimeError(f"isolation worker failed: {process.stderr[-2000:]}")
    result = json.loads(process.stdout)
    if result["sample"] is not None and not valid(problem, result["sample"]):
        raise ArithmeticError("parent replay rejects isolated native sample")
    return {**result, **metadata, "outer_wall_seconds": time.perf_counter()-start}


def isolation_census(solutions, rows, *, cap=100000):
    """Complete tiny hash-family reference, not a native solution oracle."""
    solutions = tuple(sorted(set(tuple(x) for x in solutions)))
    natural(rows, "hash rows", 1)
    if not solutions or any(len(x) != len(solutions[0]) or any(type(v) is not int or v not in (0, 1, 2) for v in x)
                            for x in solutions):
        raise ValueError("explicit nonempty finite ternary solution set required")
    n = len(solutions[0])
    count = 3**(rows*(n+1))
    if count > cap:
        raise ValueError("UNKNOWN: complete hash-family reference cap")
    isolated = [0]*len(solutions)
    first = [0]*len(solutions)
    for flat in product(range(3), repeat=rows*n):
        A = [flat[i*n:(i+1)*n] for i in range(rows)]
        for b in product(range(3), repeat=rows):
            cell = [j for j, x in enumerate(solutions) if all(sum(a*v for a, v in zip(row, x)) % 3 == y
                                                            for row, y in zip(A, b))]
            if cell:
                first[cell[0]] += 1
                if len(cell) == 1:
                    isolated[cell[0]] += 1
    TV = lambda counts: sum(abs(Fraction(c, sum(counts))-Fraction(1, len(solutions))) for c in counts)/2 if sum(counts) else None
    return {"solutions": solutions, "hash_rows": rows, "hashes_enumerated": count,
            "isolation_counts": isolated, "first_witness_counts_COUNTERCONTROL": first,
            "unique_cell_probability_exact": str(Fraction(sum(isolated), count)),
            "conditional_isolation_TV_exact": str(TV(isolated)),
            "first_witness_without_uniqueness_TV_exact": str(TV(first))}


def native_socket_instance(spins, seed):
    """Exact (3,6) socket-ensemble native generator without SAT filtering."""
    natural(spins, "native ternary spins", 2)
    if spins > 256:
        raise ValueError("bounded native spin count required")
    natural(seed, "public input seed")
    if seed >= 2**32:
        raise ValueError("uint32 public seed required")
    clauses, rng = 2*spins, random.Random(seed)
    checks = [j for j in range(spins) for _ in range(6)]
    rng.shuffle(checks)
    forms = []
    for edge in range(clauses):
        coefficients = [0]*spins
        for j in checks[3*edge:3*edge+3]:
            a = rng.choice((1, 2))
            coefficients[j] = (coefficients[j]+a) % 3
        forms.append(tuple(coefficients))
    offsets = tuple(rng.randrange(3) for _ in range(clauses))
    return {"spins": spins, "forms": tuple(forms), "offsets": offsets, "source_seed": seed}


def entropy_hash_rank(problem, epsilon="1/4"):
    """Exact annealed entropy hash rank and isolation hash rank."""
    mean, lower, upper = annealed_window(problem)
    h_floor = 0
    while 3**(h_floor+1) <= mean:
        h_floor += 1
    h_ceil = h_floor if 3**h_floor >= mean else h_floor+1
    h_isolation, iso_cells = isolation_shape(upper, epsilon)
    return {"annealed_mean_exact": str(mean),
            "annealed_window": [lower, upper],
            "entropy_hash_rank_floor": h_floor,
            "entropy_hash_rank_ceil": h_ceil,
            "isolation_hash_rank": h_isolation,
            "isolation_hash_cells": iso_cells,
            "epsilon": str(Fraction(epsilon)),
            "expected_solutions_per_cell_at_floor_exact": str(mean/Fraction(3**h_floor)),
            "expected_solutions_per_cell_at_ceil_exact": str(mean/Fraction(3**h_ceil)),
            "expected_solutions_per_cell_at_isolation_exact": str(mean/Fraction(iso_cells))}


def unconditioned_first_witness_control(problem):
    """Cost of a single unconditioned SAT witness; NOT a uniform sample."""
    import pycosat
    clauses, support = encode(problem)
    support = set(support)
    variables = 3*problem["spins"]
    start, cpu = time.perf_counter(), time.process_time()
    model = pycosat.solve(list(clauses), vars=variables)
    wall, cpu_elapsed = time.perf_counter()-start, time.process_time()-cpu
    if model == "UNSAT":
        return {"status": "UNSAT_EXHAUSTED", "witness": None,
                "CNF_variables": variables, "CNF_clauses": len(clauses),
                "wall_seconds": wall, "CPU_seconds": cpu_elapsed,
                "first_witness_is_NOT_uniform_sample": True,
                "unconditioned_SAT_does_not_measure_hashed_isolation_cost": True}
    if not isinstance(model, list):
        raise RuntimeError(f"unexpected pycosat return: {model}")
    word = decode(problem, [lit for lit in model if abs(lit) in support])
    if not valid(problem, word):
        raise ArithmeticError("unconditioned SAT witness failed native replay")
    return {"status": "FIRST_WITNESS_FOUND", "witness": word,
            "CNF_variables": variables, "CNF_clauses": len(clauses),
            "wall_seconds": wall, "CPU_seconds": cpu_elapsed,
            "first_witness_is_NOT_uniform_sample": True,
            "unconditioned_SAT_does_not_measure_hashed_isolation_cost": True}


def solve_cell_trace(problem, A, b, *, timeout=10.0):
    """Single-cell solver wrapper separating deterministic trial budgets from wall caps."""
    A, b = hash_data(problem, A, b)
    if timeout is None:
        solved = solve_cell(problem, A, b)
        return {**solved, "cell_wall_budget_seconds": None, "timed_out": False}
    if type(timeout) not in (int, float) or not 0 < timeout <= 3600:
        raise ValueError("explicit finite cell wall-clock budget required")
    request = {"problem": problem, "A": A, "b": b}
    start = time.perf_counter()
    try:
        process = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--cell-worker"],
                                 input=json.dumps(request), text=True, capture_output=True,
                                 timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        clauses, _, variables = cell_cnf(problem, A, b)
        return {"status": "UNKNOWN_CELL_TIMEOUT", "sample": None,
                "native_models_seen": None, "iterator_exhausted": False,
                "CNF_variables": variables, "CNF_clauses": len(clauses),
                "wall_seconds": time.perf_counter()-start, "CPU_seconds": None,
                "cell_wall_budget_seconds": timeout, "timed_out": True,
                "timeout_can_depend_on_hash_and_output": True,
                "partial_cell_witness_accepted": False}
    if process.returncode:
        raise RuntimeError(f"cell worker failed: {process.stderr[-2000:]}")
    solved = json.loads(process.stdout)
    if solved["sample"] is not None:
        word = tuple(solved["sample"])
        if not valid(problem, word) or any(sum(a*x for a, x in zip(row, word)) % 3 != target
                                           for row, target in zip(A, b)):
            raise ArithmeticError("parent replay rejected cell worker sample")
        solved["sample"] = word
    return {**solved, "cell_wall_budget_seconds": timeout, "timed_out": False}


def entropy_rank_hashed_campaign(
    specs=((16, 711), (20, 713), (24, 714), (28, 715), (32, 712)),
    *,
    cells_per_rank=4,
    cell_timeout=10.0,
    epsilon="1/4",
    seed=4101,
):
    """Hashed-SAT scaling campaign near the entropy and isolation hash ranks.

    Retains all generated native inputs, rank-deficient hashes, empty-cell proof
    costs, unique-cell exhaustion costs, and any wall-timeout unknown mass.
    """
    natural(cells_per_rank, "deterministic cells per hash rank", 1)
    natural(seed, "campaign seed")
    if not specs:
        raise ValueError("at least one (spins, seed) specification required")
    saved_by_seed = {(c["spins"], c["source_seed"]): c for c in saved_cases()}
    rows = []
    for index, (spins, instance_seed) in enumerate(specs):
        generated = native_socket_instance(spins, instance_seed)
        if (spins, instance_seed) in saved_by_seed:
            saved = saved_by_seed[(spins, instance_seed)]
            if (tuple(map(tuple, saved["forms"])) != generated["forms"]
                    or tuple(saved["offsets"]) != generated["offsets"]):
                raise ArithmeticError("native socket generator diverged from saved source")
        ranks = entropy_hash_rank(generated, epsilon=epsilon)
        unconditioned = unconditioned_first_witness_control(generated)
        rank_schedule = (
            ("entropy_floor", ranks["entropy_hash_rank_floor"]),
            ("entropy_ceil", ranks["entropy_hash_rank_ceil"]),
            ("isolation_target", ranks["isolation_hash_rank"]),
        )
        rng = random.Random(seed + 1009*index)
        rank_evaluations = []
        for label, h in rank_schedule:
            traces = []
            for _ in range(cells_per_rank):
                A = tuple(tuple(rng.randrange(3) for _ in range(spins)) for _ in range(h))
                b = tuple(rng.randrange(3) for _ in range(h))
                matrix_rank = int(nmod_mat(A, 3).rank()) if h else 0
                solved = solve_cell_trace(generated, A, b, timeout=cell_timeout)
                traces.append({"A": A, "b": b, "hash_matrix_rank": matrix_rank,
                               "rank_deficient": matrix_rank < min(h, spins), **solved})
            empty = [c for c in traces if c["status"] == "EMPTY"]
            unique = [c for c in traces if c["status"] == "UNIQUE"]
            multiple = [c for c in traces if c["status"] == "MULTIPLE"]
            timeouts = [c for c in traces if c["status"] == "UNKNOWN_CELL_TIMEOUT"]
            total_wall = sum(c["wall_seconds"] for c in traces)
            mean_cell_wall = total_wall/len(traces)
            rank_evaluations.append({
                "regime": label,
                "hash_rows": h,
                "hash_cells": 3**h,
                "deterministic_cell_trial_budget": cells_per_rank,
                "experimental_cell_wall_budget_seconds": cell_timeout,
                "empty_cells_proved": len(empty),
                "unique_cells_proved": len(unique),
                "multiple_cells_rejected": len(multiple),
                "timeout_cells_unknown": len(timeouts),
                "unknown_timeout_fraction_exact": str(Fraction(len(timeouts), cells_per_rank)),
                "rank_deficient_hashes_retained": sum(c["rank_deficient"] for c in traces),
                "empty_cell_proof_wall_seconds_total": sum(c["wall_seconds"] for c in empty),
                "unique_cell_proof_wall_seconds_total": sum(c["wall_seconds"] for c in unique),
                "multiple_cell_wall_seconds_total": sum(c["wall_seconds"] for c in multiple),
                "total_wall_seconds": total_wall,
                "mean_cell_wall_seconds": mean_cell_wall,
                "mean_cell_to_unconditioned_SAT_wall_ratio": (
                    mean_cell_wall/max(unconditioned["wall_seconds"], 1e-9)
                ),
                "cell_traces": traces,
                "slow_cells_discarded": False,
                "capped_law_certified_by_uncapped_bound": False,
            })
        rows.append({
            "problem": generated,
            "problem_sha256": problem_digest(generated),
            "spins": spins,
            "constraints": len(generated["forms"]),
            "instance_seed": instance_seed,
            "ranks": ranks,
            "unconditioned_first_witness": unconditioned,
            "rank_evaluations": rank_evaluations,
            "source_conditioned_on_satisfiability": False,
            "successful_seeds_selected": False,
        })
    return {
        "campaign_seed": seed,
        "deterministic_cells_per_rank": cells_per_rank,
        "experimental_cell_wall_budget_seconds": cell_timeout,
        "target_isolation_epsilon": str(Fraction(epsilon)),
        "instances": rows,
        "deterministic_trial_budgets_distinct_from_wall_budgets": True,
        "empty_cell_exhaustion_costs_charged": True,
        "rank_deficient_and_zero_hashes_retained": True,
        "capped_runtime_TV_certified": False,
        "asymptotic_classical_hardness_or_dequantization_claimed": False,
    }


def run_controls(timeout=30):
    dependencies = [Path(__file__), COUNTS, SAVED_SOURCE, ROOT/"theorems/ternary_classical_sampling.py",
                    ROOT/"theorems/ternary_decoded_sampler.py"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}
    completed = {c["problem_sha256"]: c["complete_model_count"] for c in json.loads(COUNTS.read_text())["cases"]
                 if c["status"] == "VERIFIED_EXACT_POOL_SAMPLES_CONDITIONAL_ON_COMPLETION"}
    cases = []
    for i, problem in enumerate(saved_cases()):
        rejection = rank_sample(problem, max_trials=1 << 24, seed=1931+i)
        print(json.dumps({"spins": problem["spins"], "method": "rank", "status": rejection["status"],
                          "trials": rejection["logical_trials_to_first_success"], "seconds": rejection["wall_seconds"]}), flush=True)
        isolation = isolation_trace(problem, timeout=timeout, seed=2931+i)
        print(json.dumps({"spins": problem["spins"], "method": "isolation", "status": isolation["status"]}), flush=True)
        # Complete counts are consulted ONLY AFTER both samplers have finished.
        Z = completed[problem_digest(problem)]
        domain = int(rejection["proposal_domain_size"])
        if not 0 < Z <= domain:
            raise ArithmeticError("independent full count contradicts the proposal bijection")
        acceptance = Fraction(Z, domain)
        lo, hi = power_interval(1-acceptance, rejection["max_trials"])
        mean, lower, upper = annealed_window(problem)
        _, cells = isolation_shape(upper, "1/4")
        cases.append({"problem": problem, "problem_sha256": problem_digest(problem), "rank_rejection": rejection,
                      "full_weight_syndrome_bridge": syndrome_bridge(problem),
                      "hash_isolation_trace": isolation, "independent_preexisting_complete_count": Z,
                      "rank_acceptance_exact": str(acceptance), "rank_fixed_cap_TV_interval": [str(lo), str(hi)],
                      "annealed_original_spin_acceptance_exact": str(Fraction(2, 3)**len(problem["forms"])),
                      "annealed_rank_conditioned_acceptance_exact": str(Fraction(2, 3)**(len(problem["forms"])-rejection["rank"])),
                      "annealed_mean_exact": str(mean), "actual_count_in_predetermined_window": lower <= Z <= upper,
                      "isolation_UNCAPPED_bound_from_independent_count": isolation_bound(Z, Z, cells, 256),
                      "generic_dense_code_hardness_transferred": False})
    controls = [isolation_census(S, 2) for S in (((0, 0), (0, 1), (1, 0)),
                                               ((0, 0), (0, 1), (0, 2), (1, 0)))]
    campaign = entropy_rank_hashed_campaign(cell_timeout=min(float(timeout), 10.0))
    if hashes != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}:
        raise RuntimeError("producer or dependency changed during live experiment")
    return {"schema_version": 2, "status": "KNOWN_CLASSICAL_CONDITIONING_METHODS_SCOPE_REVIEW_PENDING",
            "source_sha256": hashes, "cases": cases, "full_hash_family_controls": controls,
            "entropy_rank_hashed_campaign": campaign,
            "sources": ["https://arxiv.org/html/1903.07464v2", "https://eprint.iacr.org/2022/128",
                        "https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/ConvergeRates/RandomizedAlgs/JerrumValiantVaziraniTCS1986.pdf"],
            "polynomial_classical_conditional_sampler_established": False,
            "new_quantum_algorithm_or_speedup_claimed": False, "local_derivation_independently_reviewed": False}


def main():
    if "--isolation-worker" in sys.argv:
        request = json.load(sys.stdin)
        print(json.dumps(isolation_sample(**request), allow_nan=False))
        return
    if "--cell-worker" in sys.argv:
        request = json.load(sys.stdin)
        print(json.dumps(solve_cell(request["problem"], request["A"], request["b"]), allow_nan=False))
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls(args.timeout)
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
