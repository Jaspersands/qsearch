"""A bounded native residual experiment, not a benchmark campaign or sampler."""

import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
import random
import subprocess
import sys
from time import perf_counter

from residual_sat import BinaryField, solve_residual, syndrome, verify


MODULI = {5: 37, 7: 131, 11: 2053, 17: 131081, 31: 2147483657}


def make_instance(bits, seed, mode, pattern):
    field = BinaryField(bits, MODULI[bits])
    rng = random.Random(seed)
    length, checks = bits*bits, bits*bits//8
    residual_length = checks+math.ceil(4*checks/bits)
    points = rng.sample(range(field.order), length)
    targets = [rng.randrange(2) for _ in points] if pattern == "random" else [1]*length
    # U is fixed before any prefix randomness or syndrome is drawn.
    residual = tuple(range(residual_length))
    prefix = None
    if mode == "uniform":
        rhs = tuple(rng.randrange(field.order) for _ in range(checks))
    else:
        trace_one = next(1 << j for j in range(bits) if field.trace(1 << j))
        prefix = []
        for bit in targets[residual_length:]:
            y = rng.randrange(field.order)
            if field.trace(y) != bit:
                y ^= trace_one
            prefix.append(field.inverse(y))
        rhs = syndrome(field, points[residual_length:], prefix, checks)
    instance = {"bits": bits, "modulus": field.modulus, "points": points,
                "targets": targets, "checks": checks, "residual_positions": residual,
                "residual_syndrome": rhs, "accepted_prefix": prefix,
                "syndrome_law": mode, "target_pattern": pattern,
                "seed": seed, "full_witness_used_to_generate_input": False}
    return field, instance


def worker(config):
    start = perf_counter()
    field, instance = make_instance(config["bits"], config["seed"], config["mode"], config["pattern"])
    m = len(instance["residual_positions"])
    remaining = config["seconds"]-(perf_counter()-start)
    if remaining <= 0:
        return {"status": "UNKNOWN", "reason": "input_construction_clock_exhausted", "input": instance}
    result = solve_residual(field, instance["points"][:m], instance["checks"],
                            instance["targets"][:m], instance["residual_syndrome"],
                            seconds=remaining, resource_limit=config["resource_limit"], seed=config["seed"],
                            encoding=config["encoding"], algebraic=config["algebraic"])
    if result["status"] == "VERIFIED_RESIDUAL_WITNESS" and config["mode"] == "induced":
        word = list(result["witness"])+instance["accepted_prefix"]
        if not verify(field, instance["points"], word, instance["checks"],
                      instance["targets"], [0]*instance["checks"]):
            raise ArithmeticError("residual completion failed original native verification")
        result["full_native_witness"] = word
        result["original_native_relation_verified"] = True
    result.update(input=instance, worker_total_seconds=perf_counter()-start,
                  input_sha256=sha256(json.dumps(instance, sort_keys=True).encode()).hexdigest())
    return result


def bounded_run(config):
    start = perf_counter()
    try:
        process = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker"],
                                 input=json.dumps(config), text=True, capture_output=True,
                                 timeout=config["seconds"], check=False)
        if process.returncode:
            result = {"status": "ERROR", "returncode": process.returncode, "stderr": process.stderr[-4000:]}
        else:
            result = json.loads(process.stdout)
    except subprocess.TimeoutExpired:
        # subprocess.run terminates and reaps this worker before returning.
        result = {"status": "UNKNOWN", "reason": "whole_worker_wall_cap",
                  "input_reconstruction": "make_instance with the recorded configuration"}
    base = Path(__file__).resolve().parent
    names = ("residual_sat.py", "test_residual_sat.py", "run_attack.py")
    return {"config": config, "result": result, "elapsed_seconds": perf_counter()-start,
            "scope": "capped_classical_search_not_sampling_or_asymptotic_hardness",
            "source_sha256": {name: sha256((base/name).read_bytes()).hexdigest() for name in names},
            "repository_integrated": False, "reason_not_integrated": "active repository migration",
            "python_version": sys.version, "polynomial_time_solver_established": False}


if __name__ == "__main__":
    if sys.argv[1:] == ["--worker"]:
        print(json.dumps(worker(json.load(sys.stdin))))
    else:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--bits", type=int, choices=MODULI, default=17)
        parser.add_argument("--seed", type=int, default=2301)
        parser.add_argument("--mode", choices=("uniform", "induced"), default="uniform")
        parser.add_argument("--pattern", choices=("random", "ones"), default="random")
        parser.add_argument("--seconds", type=float, default=30)
        parser.add_argument("--resource-limit", type=int, default=5_000_000)
        parser.add_argument("--encoding", choices=("inverse", "conic"), default="inverse")
        parser.add_argument("--algebraic", action="store_true", help="enable Z3 ANF and extended linear simplification")
        args = parser.parse_args()
        if args.seconds <= 0 or args.resource_limit < 1:
            parser.error("positive wall and resource limits required")
        report = bounded_run(vars(args))
        tag = "anf" if args.algebraic else "default"
        name = f"residual_n{args.bits}_{args.mode}_{args.pattern}_{args.encoding}_{tag}_{args.seed}.json"
        path = Path(__file__).resolve().with_name(name)
        path.write_text(json.dumps(report, indent=2)+"\n", encoding="ascii")
        print(json.dumps({"receipt": str(path), "status": report["result"]["status"],
                          "reason": report["result"].get("reason"),
                          "seconds": report["elapsed_seconds"]}, indent=2))
