"""Matched UniGen baseline for the ORIGINAL sparse ternary affine-exclusion CSP.

Bijective CNF encoding, complete native witness replay, isolated paid backend
runs. Neither finite performance nor a backend's counting epsilon certifies
arbitrary total-variation accuracy or asymptotic dequantization.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.metadata
from itertools import combinations, product
import json
from math import sqrt
from pathlib import Path
import platform
import random
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/"research/classical_baselines/ternary_classical_sampling.json"
SAVED_SOURCE = ROOT/"research/phase_workbench/ternary_bpqm_certificate.json"
DECODER_SOURCE = ROOT/"research/reductions/ternary_decoded_sampler.json"
MARKER = "QSEARCH_UNIGEN_RESULT "


def validate_problem(problem):
    n = problem.get("spins")
    if type(n) is not int or not 1 <= n <= 4096:
        raise ValueError("explicit positive bounded native spin count required")
    forms, offsets = tuple(map(tuple, problem["forms"])), tuple(problem["offsets"])
    if (not forms or len(forms) != len(offsets) or any(len(row) != n or
            any(type(v) is not int or v not in (0, 1, 2) for v in row) or
            sum(v != 0 for v in row) > 3 for row in forms) or
            any(type(v) is not int or v not in (0, 1, 2) for v in offsets)):
        raise ValueError("original canonical affine forms of arity <=3 and offsets required")
    return n, forms, offsets


def valid(problem, word):
    n, forms, offsets = validate_problem(problem)
    return (len(word) == n and all(type(x) is int and x in (0, 1, 2) for x in word) and
            all((sum(a*x for a, x in zip(row, word))+j) % 3 for row, j in zip(forms, offsets)))


def encode(problem):
    """No auxiliary variables: exactly one Boolean per spin/value.

    Sampling the first TWO flags of EVERY spin is a bijection: 10->0,
    01->1, 00->2. The third flag is uniquely forced. No gauge is fixed.
    """
    n, forms, offsets = validate_problem(problem)
    clauses = []
    for i in range(n):
        flags = tuple(3*i+j+1 for j in range(3))
        clauses.append(flags)
        clauses.extend((-a, -b) for a, b in combinations(flags, 2))
    for row, offset in zip(forms, offsets):
        support = tuple(i for i, coefficient in enumerate(row) if coefficient)
        for digits in product(range(3), repeat=len(support)):
            if (sum(row[i]*x for i, x in zip(support, digits))+offset) % 3 == 0:
                clauses.append(tuple(-(3*i+x+1) for i, x in zip(support, digits)))
    return tuple(clauses), tuple(3*i+j+1 for i in range(n) for j in range(2))


def decode(problem, literals):
    n, _, _ = validate_problem(problem)
    expected = {3*i+j+1 for i in range(n) for j in range(2)}
    assignment = {}
    for literal in literals:
        if type(literal) is not int or not literal or abs(literal) not in expected or abs(literal) in assignment:
            raise ValueError("one unambiguous literal per original sampling-support flag required")
        assignment[abs(literal)] = literal > 0
    if set(assignment) != expected:
        raise ValueError("partial projection is NOT a full native spin sample")
    word = []
    for i in range(n):
        a, b = assignment[3*i+1], assignment[3*i+2]
        if a and b:
            raise ValueError("backend returned a forbidden double-occupied spin")
        word.append(0 if a else 1 if b else 2)
    if not valid(problem, word):
        raise ValueError("backend model fails UNCHANGED ORIGINAL native constraints")
    return tuple(word)


def problem_digest(problem):
    n, forms, offsets = validate_problem(problem)
    return hashlib.sha256(json.dumps({"spins": n, "forms": forms, "offsets": offsets},
                                     sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def exact_reference(problem, cap=100000):
    n, _, _ = validate_problem(problem)
    if 3**n > cap:
        return {"status": "UNKNOWN_EXPONENTIAL_REFERENCE_CAP", "count": None}
    solutions = [word for word in product(range(3), repeat=n) if valid(problem, word)]
    return {"status": "COMPLETE_EXPONENTIAL_CENSUS", "count": len(solutions), "solutions": solutions}


def worker(request):
    """Standard-library-only worker apart from the actual native backend."""
    problem, number, seed = request["problem"], request["samples"], request["seed"]
    if type(number) is not int or not 1 <= number <= 100000 or type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError("bounded requested sample count and uint32 seed required")
    clauses, support = encode(problem)
    if request.get("engine", "unigen") == "picosat-exact":
        return exact_pool_worker(request, clauses, support)
    if request.get("engine", "unigen") != "unigen":
        raise ValueError("explicit supported backend required")
    try:
        import pyunigen
    except ImportError:
        return {"status": "UNKNOWN_UNIGEN_UNAVAILABLE"}
    config = {"verbosity": 0, "seed": seed, "epsilon": .8, "delta": .05,
              "kappa": .638, "multisample": False}
    sampler = pyunigen.Sampler(**config)
    for clause in clauses:
        sampler.add_clause(clause)
    start, cpu = time.perf_counter(), time.process_time()
    cells, hashes, models = sampler.sample(num=number, sampling_set=support)
    elapsed, cpu = time.perf_counter()-start, time.process_time()-cpu
    words = [decode(problem, model) for model in models]
    return {"status": "VERIFIED_NATIVE_SAMPLES" if len(words) == number else "UNKNOWN_INCOMPLETE_SAMPLE_BATCH",
            "problem_sha256": problem_digest(problem), "backend": "pyunigen",
            "backend_version": importlib.metadata.version("pyunigen"),
            "backend_binary_sha256": hashlib.sha256(Path(pyunigen.__file__).read_bytes()).hexdigest(),
            "python_version": platform.python_version(), "machine": platform.machine(),
            "configuration": config, "Boolean_variables": 3*problem["spins"],
            "CNF_clauses": len(clauses), "sampling_set": support,
            "cell_count": cells, "count_hashes": hashes,
            "reported_model_count_estimate": cells*2**hashes,
            "returned_native_samples": words, "all_returned_samples_verified_against_original_input": True,
            "backend_sample_call_wall_seconds": elapsed, "backend_sample_call_CPU_seconds": cpu,
            "requested_samples": number, "arbitrary_TV_accuracy_certified": False,
            "counting_epsilon_is_NOT_sampling_TV": True,
            "joint_IID_output_guarantee_verified": False,
            "asymptotic_dequantization_established": False}


def exact_pool_worker(request, clauses, support):
    """Complete mature-SAT enumeration, then actual EXACT uniform sampling.

    NO propagation limit: pycosat warns that a limited iterator can stop
    without a complete census. A model cap or outer timeout never licenses
    sampling from the visited prefix.
    """
    try:
        import pycosat
    except ImportError:
        return {"status": "UNKNOWN_PICOSAT_UNAVAILABLE"}
    cap = request.get("model_cap", 65536)
    if type(cap) is not int or not 1 <= cap <= 1000000:
        raise ValueError("explicit exact pool cap required")
    problem = request["problem"]
    start, cpu = time.perf_counter(), time.process_time()
    pool, seen = [], set()
    support = set(support)
    for model in pycosat.itersolve(clauses):
        assignment = {abs(lit): lit > 0 for lit in model}
        if (len(assignment) != 3*problem["spins"] or
                any(not any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses)):
            raise ValueError("independent CNF replay rejects an exact-pool model")
        word = decode(problem, [lit for lit in model if abs(lit) in support])
        if word in seen:
            raise ValueError("CNF encoding has unexpected native solution multiplicity")
        seen.add(word)
        pool.append(word)
        if len(pool) > cap:
            return {"status": "UNKNOWN_EXACT_POOL_CAP_NO_SAMPLES", "models_seen_at_least": len(pool),
                    "returned_native_samples": [], "partial_pool_sampled": False,
                    "requested_samples": request["samples"]}
    if not pool:
        return {"status": "SOLVER_EXHAUSTED_NO_SOLUTIONS", "complete_model_count": 0,
                "returned_native_samples": [], "solver_proof_independently_checked": False}
    enumeration_wall, enumeration_cpu = time.perf_counter()-start, time.process_time()-cpu
    prefix_diagnostics = []
    for width in sorted({0, 1, 2, 4, 8, 16, problem["spins"]}):
        if width > problem["spins"]:
            continue
        counts = Counter(word[:width] for word in pool)
        flat = Fraction(1, 3**width)
        TV = (sum(abs(Fraction(count, len(pool))-flat) for count in counts.values())+
              (3**width-len(counts))*flat)/2
        prefix_diagnostics.append({"original_prefix_spins": width, "nonempty_prefix_assignments": len(counts),
                                   "exact_uniform_solution_prefix_TV_from_IID_uniform_exact": str(TV)})
    rng = random.Random(request["seed"])
    selections = [rng.randrange(len(pool)) for _ in range(request["samples"])]
    return {"status": "VERIFIED_EXACT_POOL_SAMPLES_CONDITIONAL_ON_COMPLETION",
            "backend": "pycosat/PicoSAT", "backend_version": pycosat.__version__,
            "backend_binary_sha256": hashlib.sha256(Path(pycosat.__file__).read_bytes()).hexdigest(),
            "problem_sha256": problem_digest(problem), "python_version": platform.python_version(),
            "machine": platform.machine(), "Boolean_variables": 3*problem["spins"],
            "CNF_clauses": len(clauses), "sampling_set": sorted(support),
            "complete_model_count": len(pool), "model_cap": cap,
            "pool_ordered_sha256": hashlib.sha256(json.dumps(pool, separators=(",", ":")).encode()).hexdigest(),
            "selected_pool_indices": selections, "returned_native_samples": [pool[i] for i in selections],
            "requested_samples": request["samples"], "all_returned_samples_verified_against_original_input": True,
            "enumeration_wall_seconds": enumeration_wall, "enumeration_CPU_seconds": enumeration_cpu,
            "complete_pool_storage_trits": len(pool)*problem["spins"],
            "exact_uniform_solution_prefix_diagnostics": prefix_diagnostics,
            "propagation_limit_used": False, "partial_pool_sampled": False,
            "uniformity_statement": "exact_given_complete_pool_and_uniform_independent_index_coins",
            "reproducibility_PRNG_seed_is_not_a_randomness_proof": True,
            "asymptotic_dequantization_established": False}


def run_backend(problem, *, samples=128, seed=991, timeout=30, python=None, architecture=None,
                engine="unigen", model_cap=65536):
    validate_problem(problem)
    if type(timeout) not in (int, float) or not 0 < timeout <= 3600:
        raise ValueError("explicit finite worker wall-time cap required")
    command = [str(python or sys.executable), str(Path(__file__).resolve()), "--worker"]
    if architecture is not None:
        if architecture != "x86_64" or sys.platform != "darwin":
            raise ValueError("only an explicit existing macOS x86_64 runtime override is supported")
        command = ["arch", "-x86_64"]+command
    request = {"problem": problem, "samples": samples, "seed": seed, "engine": engine, "model_cap": model_cap}
    before = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    start = time.perf_counter()
    base = {"problem": problem, "problem_sha256": problem_digest(problem),
            "worker_wall_cap_seconds": timeout, "requested_samples": samples, "seed": seed,
            "engine": engine,
            "source_conditioned_on_success": False, "speedup_claim_allowed": False,
            "arbitrary_TV_accuracy_certified": False, "asymptotic_dequantization_established": False}
    try:
        result = subprocess.run(command, input=json.dumps(request), text=True, capture_output=True,
                                timeout=timeout, check=False)
    except subprocess.TimeoutExpired as error:
        def as_text(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        logs = as_text(error.stdout)+"\n"+as_text(error.stderr)
        return dict(base, status="UNKNOWN_WORKER_TIMEOUT_NO_SAMPLING_CLAIM",
                    worker_wall_seconds=time.perf_counter()-start,
                    partial_sample_batch_used=False, return_code=None,
                    backend_output_sha256=hashlib.sha256(logs.encode()).hexdigest(),
                    output_tail=logs[-4000:])
    except OSError as error:
        return dict(base, status="UNKNOWN_RUNTIME_UNAVAILABLE", error=str(error),
                    worker_wall_seconds=time.perf_counter()-start)
    if before != hashlib.sha256(Path(__file__).read_bytes()).hexdigest():
        raise RuntimeError("worker producer changed during run")
    logs = result.stdout+"\n"+result.stderr
    base.update(worker_wall_seconds=time.perf_counter()-start, return_code=result.returncode,
                backend_output_sha256=hashlib.sha256(logs.encode()).hexdigest())
    records = [line[len(MARKER):] for line in result.stdout.splitlines() if line.startswith(MARKER)]
    if result.returncode or len(records) != 1:
        return dict(base, status="UNKNOWN_BACKEND_EXIT_OR_PROTOCOL_FAILURE", output_tail=logs[-4000:])
    try:
        payload = json.loads(records[0])
    except json.JSONDecodeError:
        return dict(base, status="UNKNOWN_MALFORMED_BACKEND_RESULT", output_tail=logs[-4000:])
    if payload.get("status") in ("VERIFIED_NATIVE_SAMPLES", "VERIFIED_EXACT_POOL_SAMPLES_CONDITIONAL_ON_COMPLETION"):
        if payload["problem_sha256"] != base["problem_sha256"] or len(payload["returned_native_samples"]) != samples:
            raise ValueError("backend result belongs to a different input or incomplete batch")
        for word in payload["returned_native_samples"]:
            if not valid(problem, word):
                raise ValueError("parent replay rejects a native backend sample")
    return dict(base, **payload)


def sample_diagnostics(problem, backend, reference):
    """Descriptive finite histograms, NEVER an accuracy/confidence certificate."""
    words = backend.get("returned_native_samples", ())
    histogram = Counter(tuple(x) for x in words)
    result = {"samples": len(words), "distinct_native_samples": len(histogram),
              "marginal_counts": [[sum(count for word, count in histogram.items() if word[i] == j)
                                    for j in range(3)] for i in range(problem["spins"])],
              "empirical_histogram_TV_is_NOT_engine_distribution_TV": True}
    if reference["count"] and words:
        solutions = [tuple(x) for x in reference["solutions"]]
        result["empirical_histogram_TV_from_exact_uniform"] = sum(
            abs(Fraction(histogram[word], len(words))-Fraction(1, len(solutions))) for word in solutions)/2
        result["empirical_histogram_TV_from_exact_uniform"] = str(result["empirical_histogram_TV_from_exact_uniform"])
    return result


def saved_cases():
    report = json.loads(SAVED_SOURCE.read_text())
    return [{"spins": row["spins"], "forms": row["forms_H_transpose"],
             "offsets": row["original_offsets"], "source_seed": row["seed"],
             "source_file": str(SAVED_SOURCE.relative_to(ROOT))}
            for row in report["classical_original_dual_CSP_controls"]]


def decoder_count_consequences():
    """Exact count/planting ratios; floating displays are NOT probability proofs.

    The local derivation uses the previous unconditional state-error identity:
    E( sqrt(R)-1 )^2 <=2*delta. Quiet planting is not a conditional sampler
    for a prescribed original instance.
    """
    result = []
    for case in json.loads(DECODER_SOURCE.read_text())["cases"]:
        v, m = len(case["H"]), len(case["H"][0])
        mean = Fraction(3**v, 3**m)
        ratios = [Fraction(row["native_partition_exact"])/mean for row in case["all_original_offset_rows"]]
        if sum(ratios) != len(ratios):
            raise ArithmeticError("weighted annealed partition identity failed")
        TV = sum(abs(r-1) for r in ratios)/(2*len(ratios))
        energy = sum((sqrt(float(r))-1)**2 for r in ratios)/len(ratios)
        delta = case["mean_word_error_numeric"]
        if energy > 2*delta+1e-10 or float(TV) > sqrt(max(0., 2*delta))+1e-10:
            raise ArithmeticError("count/planting consequence contradicts actual decoder control")
        result.append({"H": case["H"], "spectrum": case["normalized_product_spectrum"],
                       "decoder_mode": case["decoder_mode"], "decoder_offset": case["decoder_constant_offset"],
                       "weighted_partition_mean_uniform_offsets_exact": str(mean),
                       "planting_to_uniform_original_offset_TV_exact": str(TV),
                       "mean_sqrt_count_ratio_deviation_squared_NUMERICAL": energy,
                       "decoder_word_error_NUMERICAL": delta,
                       "local_count_concentration_bound": "Pr(|R-1|>eta)<=2*delta/(sqrt(1+eta)-1)^2, 0<eta<=1",
                       "quiet_planting_TV_bound": "min(1,sqrt(2*delta))",
                       "quiet_planting_supplies_fixed_input_sampler": False,
                       "count_consequence_is_a_new_classical_uniform_sampler": False})
    return result


def main():
    if sys.argv[1:] == ["--worker"]:
        result = worker(json.load(sys.stdin))
        print(MARKER+json.dumps(result, allow_nan=False), flush=True)
        return
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--backend-python", type=Path)
    parser.add_argument("--backend-arch", choices=("x86_64",))
    parser.add_argument("--samples", type=int, default=128)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    files = [Path(__file__), SAVED_SOURCE, DECODER_SOURCE]
    before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    results = []
    for i, problem in enumerate(saved_cases()):
        result = run_backend(problem, samples=args.samples, seed=991+i, timeout=args.timeout,
                             python=args.backend_python, architecture=args.backend_arch)
        reference = exact_reference(problem)
        result["finite_diagnostics"] = sample_diagnostics(problem, result, reference)
        result["exact_reference_status"] = reference["status"]
        results.append(result)
        print(json.dumps({"spins": problem["spins"], "status": result["status"],
                          "wall_seconds": result["worker_wall_seconds"]}), flush=True)
        exact = run_backend(problem, samples=args.samples, seed=1991+i, timeout=args.timeout,
                            engine="picosat-exact")
        exact["finite_diagnostics"] = sample_diagnostics(problem, exact, reference)
        results.append(exact)
        print(json.dumps({"spins": problem["spins"], "engine": "picosat-exact", "status": exact["status"],
                          "wall_seconds": exact["worker_wall_seconds"], "complete_count": exact.get("complete_model_count")}), flush=True)
    count_controls = decoder_count_consequences()
    if before != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}:
        raise RuntimeError("producer or original source artifact changed during run")
    report = {"schema_version": 1, "status": "MATCHED_CLASSICAL_UNIGEN_BASELINE_NOT_AN_ASYMPTOTIC_VERDICT",
              "source_sha256": before, "cases": results,
              "count_and_quiet_planting_scope_controls": count_controls,
              "arbitrary_TV_accuracy_or_independent_backend_proof_claimed": False,
              "new_quantum_algorithm_or_speedup_claimed": False,
              "sources": ["https://github.com/meelgroup/unigen", "https://pysathq.github.io/docs/html/api/allies/unigen.html"]}
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()
