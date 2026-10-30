"""Bounded exact native hash-cell enumeration, not a uniform sampler.

COMPLETE means that Z3 reported UNSAT after blocking every verified projected
u. It is not an independently checked completeness certificate, a polynomial
enumeration claim, or the missing enumeration lemma in the heat-bath note.
"""

from collections.abc import Sequence
from functools import reduce
import hashlib
import json
from time import perf_counter

from theorems.balanced_codeword_filter import integer, reciprocal_trace, trace_mask
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_smt import (
    BinaryFieldCircuit, syndrome, validate_instance, vandermonde_eliminate_residual,
)
from theorems.parity_block_usd_prange import affine_system


def _sequence(values, name):
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise ValueError(f"{name} must be an ordered sequence")
    return tuple(values)


def _hash_value(rows, u):
    return sum(((row & u).bit_count() & 1) << j for j, row in enumerate(rows))


def _hash_system(rows, rhs, width):
    equations = [(row, (rhs >> j) & 1) for j, row in enumerate(rows)]
    # affine_system requires positive width. A dummy zero column handles B=0;
    # remove it from the receipt so it never becomes a symbolic coordinate.
    system = affine_system(equations, max(1, width))
    if width == 0:
        system = {**system, "rref": tuple(row[1:] for row in system["rref"]),
                  "pivots": (), "free": ()}
    return {key: [list(row) for row in value] if key == "rref"
            else list(value) if key in ("pivots", "free") else value
            for key, value in system.items()}


def _make_solver(z3, resource_limit, solver_seed):
    solver = z3.Then("simplify", "bit-blast", "sat").solver()
    solver.set(rlimit=resource_limit, random_seed=solver_seed)
    return solver


def _block_projection(solver, z3, u_exprs, u):
    # Or() is False for B=0, excluding its sole projection without BitVec(0).
    solver.add(z3.Or(*(expr != z3.BoolVal(bool((u >> j) & 1))
                       for j, expr in enumerate(u_exprs))))


def _backend_error(report, stage, error, call=None):
    detail = {"stage": stage, "type": type(error).__name__, "message": str(error)}
    report["backend_errors"].append(detail)
    report["stop_reason"] = "backend_error"
    if call is not None:
        call.setdefault("backend_errors", []).append(detail)


def _finish(report, start, setup_end):
    report["model_count"] = len(report["solutions"])
    if report["complete"]:
        report["cell_cardinality"] = report["model_count"]
    else:
        partial = report["solutions"] or report["stop_reason"] == "max_models"
        report["status"] = "PARTIAL" if partial else "UNKNOWN"
    end = perf_counter()
    report["enumeration_seconds"] = end-setup_end
    report["total_seconds"] = end-start
    return report


def _encode(report, z3, solver):
    bits = report["instance"]["bits"]
    system, width = report["hash_system"], report["B"]
    u = [z3.BoolVal(False) for _ in range(width)]
    for j in system["free"]:
        u[j] = z3.Bool(f"hash_free_{j}")
    for row in system["rref"]:
        if any(row[:-1]):
            pivot = next(j for j, value in enumerate(row[:-1]) if value)
            u[pivot] = reduce(z3.Xor, (u[j] for j in system["free"] if row[j]),
                              z3.BoolVal(bool(row[-1])))
    if not system["consistent"]:
        solver.add(z3.BoolVal(False))
        return u, []

    circuit = BinaryFieldCircuit(bits)
    targets = report["instance"]["targets"]
    basis, c = report["trace_kernel_basis"], report["trace_one"]
    x_free = [z3.BitVec(f"x_free_{i}", bits) for i in report["free_indices"]]
    for s, (index, x) in enumerate(zip(report["free_indices"], x_free)):
        y = reduce(lambda a, b: a ^ b,
                   (z3.If(u[s*(bits-1)+j], z3.BitVecVal(v, bits), circuit.zero)
                    for j, v in enumerate(basis)),
                   z3.BitVecVal(c if targets[index] else 0, bits))
        solver.add(circuit.inverse_graph(x, y))

    shifts = [circuit.shifts(x) for x in x_free]
    x_piv = []
    for index, constant, row in zip(report["pivot_indices"],
                                    report["pivot_constants"], report["pivot_coefficients"]):
        x = reduce(lambda a, b: a ^ b,
                   (circuit.constant_product(shift, a)
                    for shift, a in zip(shifts, row) if a),
                   z3.BitVecVal(constant, bits))
        y = z3.BitVec(f"y_pivot_{index}", bits)
        solver.add(circuit.inverse_graph(x, y), circuit.trace(y) == targets[index])
        x_piv.append(x)
    return u, x_piv + x_free


def _decode_projection(report, u):
    """Decode u with actual field arithmetic, in supplied residual order."""
    instance = report["instance"]
    bits, targets = instance["bits"], instance["targets"]
    free = []
    for s, index in enumerate(report["free_indices"]):
        y = report["trace_one"] if targets[index] else 0
        for j, v in enumerate(report["trace_kernel_basis"]):
            if (u >> (s*(bits-1)+j)) & 1:
                y ^= v
        free.append(element(bits, y)**-1 if y else field(bits).zero())
    pivots = [encoded(sum((element(bits, a)*x for a, x in zip(row, free)),
                          element(bits, constant)))
              for constant, row in zip(report["pivot_constants"], report["pivot_coefficients"])]
    return pivots + list(map(encoded, free))


def _verify_projection(report, u, model_word=None):
    """Decode and test original H, b, M; optionally compare a solver word."""
    instance = report["instance"]
    bits, targets = instance["bits"], instance["targets"]
    decoded, errors = _decode_projection(report, u), []
    if model_word is not None and model_word != decoded:
        errors.append("symbolic_model_disagrees_with_field_decode")
    indices = report["residual_indices"]
    points = [instance["points"][i] for i in indices]
    if syndrome(bits, points, decoded, instance["checks"]) != tuple(report["residual_syndrome"]):
        errors.append("original_residual_syndrome_failed")
    if any(reciprocal_trace(bits, x) != targets[i] for i, x in zip(indices, decoded)):
        errors.append("original_inverse_trace_failed")
    if _hash_value(report["hash_rows"], u) != report["hash_rhs"]:
        errors.append("original_hash_failed")
    by_index = dict(zip(indices, decoded))
    return [by_index[i] for i in report["residual_word_indices"]], errors


def enumerate_cell(instance, indices, target_syndrome, hash_rows, hash_rhs, *,
                   timeout_ms=30_000, resource_limit=50_000_000,
                   max_models=1024, solver_seed=0, known_u=None):
    """Return a JSON-safe COMPLETE, PARTIAL, or UNKNOWN enumeration receipt.

    Preserve the supplied field/points/targets. ``indices`` is an ordered set
    of at least K original positions; its first K positions are pivots. Hash
    rows are canonical B-bit integers, rhs a k-bit integer (no booleans), with
    B=(bits-1)*(len(indices)-K) and k=len(hash_rows). No rank conditioning occurs.

    Canonical coordinates use mask=trace_mask(bits,1), c=mask&-mask, and basis
    (1<<j) ^ (c if mask>>j&1 else 0) for ascending nonpivot j. Bit s*(bits-1)+l
    of u selects basis element l for free_indices[s]. Solutions contain u and
    residual_word in ascending ORIGINAL index order (residual_word_indices),
    not pivot/free order. This API neither draws a prefix/hash nor samples a list.

    Optional known_u must be a canonical B-bit integer decoding to a native
    solution in this exact hash cell. It is independently verified, retained
    with origin="external_seed", and projected-blocked before the first check.
    Solver-discovered solutions have origin="solver". Both count toward
    max_models, so a seed requires max_models >= 1. Invalid seeds raise ValueError.

    timeout_ms is ONE post-setup enumeration deadline, not a fresh timeout per
    model. Each check receives only its remaining whole milliseconds. Model
    extraction, verification and blocking consume that deadline too, but are
    not preempted. Setup and finalization are outside it. resource_limit is a
    requested Z3 limit per check, not a whole-workflow operation bound. At most
    max_models verified solutions are retained; reaching the cap stops without
    a final UNSAT check, even if the list happens to exhaust the cell.
    All event timestamps are elapsed from entry and remain None until their
    event occurs. first_verified_model_seconds includes an external seed;
    first_solver_model_seconds excludes it. Seed verification and preblocking
    are part of setup (also broken out under verification/blocking timings).
    completion_seconds is set only on final UNSAT, including after a seed.
    """
    start = perf_counter()
    integer(timeout_ms, 1, 600_000, "enumeration timeout milliseconds")
    integer(resource_limit, 1, 2**31-1, "solver resource limit")
    integer(max_models, 0, 2**31-1, "model cap")
    integer(solver_seed, 0, 2**31-1, "solver seed")
    bits, points, targets, checks = validate_instance(instance)
    indices = _sequence(indices, "residual indices")
    integer(len(indices), checks, len(points), "residual coordinate count")
    for index in indices:
        integer(index, 0, len(points)-1, "residual index")
    if len(set(indices)) != len(indices):
        raise ValueError("distinct residual indices required")
    target_syndrome = _sequence(target_syndrome, "target syndrome")
    if len(target_syndrome) != checks:
        raise ValueError("target syndrome must have exactly K field elements")
    for value in target_syndrome:
        integer(value, 0, (1 << bits)-1, "syndrome field element")
    width = (bits-1)*(len(indices)-checks)
    hash_rows = _sequence(hash_rows, "hash rows")
    for row in hash_rows:
        integer(row, 0, (1 << width)-1, "hash row")
    integer(hash_rhs, 0, (1 << len(hash_rows))-1, "hash rhs")
    if known_u is not None:
        integer(known_u, 0, (1 << width)-1, "known_u coordinate")
        if max_models == 0:
            raise ValueError("known_u requires max_models >= 1")
    public = {"bits": bits, "points": list(points), "targets": list(targets),
              "checks": checks,
              "field_modulus_coefficients": list(instance["field_modulus_coefficients"])}
    validation_end = perf_counter()

    mask = trace_mask(bits, 1)
    c = mask & -mask
    positions = [j for j in range(bits) if (1 << j) != c]
    basis = [(1 << j) ^ (c if (mask >> j) & 1 else 0) for j in positions]
    if not c or int(element(bits, c).trace()) != 1 or any(element(bits, v).trace() for v in basis):
        raise ArithmeticError("public trace hyperplane basis failed")
    pivots, free, constants, coefficients = vandermonde_eliminate_residual(
        bits, points, indices, target_syndrome, checks)
    field_end = perf_counter()
    system = _hash_system(hash_rows, hash_rhs, width)
    hash_end = perf_counter()
    report = {
        "status": "UNKNOWN", "complete": False, "stop_reason": None,
        "method": "Z3_projected_native_hash_cell_enumeration",
        "scope": "supplied_residual_cell_only",
        "instance": public,
        "instance_sha256": hashlib.sha256(json.dumps(public, sort_keys=True).encode()).hexdigest(),
        "residual_indices": list(indices), "residual_word_indices": sorted(indices),
        "residual_syndrome": list(target_syndrome),
        "pivot_indices": list(pivots), "free_indices": list(free),
        "pivot_constants": list(constants), "pivot_coefficients": [list(row) for row in coefficients],
        "trace_mask": mask, "trace_one": c, "trace_pivot_bit": c.bit_length()-1,
        "trace_free_bit_positions": positions, "trace_kernel_basis": basis,
        "u_bit_order": [[i, j] for i in free for j in range(bits-1)],
        "u_bit_order_description": "bit s*(bits-1)+j selects trace_kernel_basis[j] at free_indices[s]",
        "B": width, "hash_rows": list(hash_rows), "hash_rhs": hash_rhs,
        "hash_rank": system["rank"], "hash_system": system,
        "hash_free_bits": width-system["rank"],
        "symbolic_hash_free_bits": width-system["rank"] if system["consistent"] else 0,
        "timeout_ms": timeout_ms,
        "timeout_scope": "single_post_setup_enumeration_deadline",
        "solver_resource_limit": resource_limit, "resource_limit_scope": "per_check_requested",
        "max_models": max_models, "solver_seed": solver_seed,
        "known_u": known_u, "seed_model_count": 0, "solver_model_count": 0,
        "solutions": [], "model_count": 0, "cell_cardinality": None,
        "first_verified_model_seconds": None, "first_solver_model_seconds": None,
        "completion_seconds": None,
        "solver_calls": [], "solver_call_counts": {"SAT": 0, "UNSAT": 0, "UNKNOWN": 0},
        "solver_check_errors": 0, "backend_errors": [],
        "projected_blocks": 0, "duplicate_models": 0, "invalid_models": 0,
        "final_solver_status": None, "reason_unknown": None,
        "validation_seconds": validation_end-start, "field_setup_seconds": field_end-validation_end,
        "hash_elimination_seconds": hash_end-field_end, "encoding_seconds": 0.0,
        "check_seconds": 0.0, "verification_seconds": 0.0,
        "model_extraction_seconds": 0.0, "blocking_seconds": 0.0,
        "seed_verification_seconds": 0.0, "seed_blocking_seconds": 0.0,
        "deduplication_seconds": 0.0, "statistics_seconds": 0.0,
        "uniform_sampler": False, "hardness_evidence": False,
        "polynomial_enumeration_established": False,
        "whole_workflow_wall_clock_cap_enforced": False,
        "completeness_basis": "solver_reported_final_UNSAT_after_projected_blocking",
        "completeness_independently_certified": False, "unsat_proof_artifact": None,
    }
    if known_u is not None:
        verification_start = perf_counter()
        word, errors = _verify_projection(report, known_u)
        report["seed_verification_seconds"] = perf_counter()-verification_start
        report["verification_seconds"] += report["seed_verification_seconds"]
        if errors:
            raise ValueError("known_u is not a native hash-cell solution: " + ", ".join(errors))
        report["solutions"].append({"u": known_u, "residual_word": word,
                                    "independently_verified": True, "origin": "external_seed"})
        report["seed_model_count"] = 1
        report["first_verified_model_seconds"] = perf_counter()-start
    encoding_start = perf_counter()
    try:
        import z3
    except ImportError:
        setup_end = perf_counter()
        report.update(stop_reason="solver_unavailable", setup_seconds=setup_end-start)
        return _finish(report, start, setup_end)
    stage = "solver_setup"
    try:
        solver = _make_solver(z3, resource_limit, solver_seed)
        stage = "encoding"
        u_exprs, x_exprs = _encode(report, z3, solver)
        if known_u is not None:
            stage = "seed_projected_blocking"
            blocking_start = perf_counter()
            try:
                _block_projection(solver, z3, u_exprs, known_u)
            finally:
                report["seed_blocking_seconds"] = perf_counter()-blocking_start
                report["blocking_seconds"] += report["seed_blocking_seconds"]
            report["projected_blocks"] += 1
    except Exception as error:
        setup_end = perf_counter()
        _backend_error(report, stage, error)
        report.update(encoding_seconds=setup_end-encoding_start, setup_seconds=setup_end-start)
        return _finish(report, start, setup_end)
    setup_end = perf_counter()
    report.update(z3_version=z3.get_version_string(), encoding_seconds=setup_end-encoding_start,
                  setup_seconds=setup_end-start)
    deadline = setup_end + timeout_ms/1000
    seen = {solution["u"] for solution in report["solutions"]}
    while len(report["solutions"]) < max_models:
        remaining_ms = int((deadline-perf_counter())*1000)
        if remaining_ms <= 0:
            report["stop_reason"] = "enumeration_deadline"
            break
        try:
            solver.set(timeout=remaining_ms)
        except Exception as error:
            _backend_error(report, "set_timeout", error)
            break
        call = {"call_index": len(report["solver_calls"]), "status": "ERROR",
                "timeout_ms": remaining_ms, "resource_limit": resource_limit,
                "solver_statistics": {},
                "statistics_scope": "backend_snapshot_not_additive_across_calls"}
        report["solver_calls"].append(call)
        check_start = perf_counter()
        try:
            outcome = solver.check()
        except Exception as error:
            report["solver_check_errors"] += 1
            _backend_error(report, "check", error, call)
        else:
            call["status"] = str(outcome).upper()
            report["solver_call_counts"][call["status"]] += 1
        check_end = perf_counter()
        call["check_seconds"] = check_end-check_start
        report["check_seconds"] += call["check_seconds"]
        report["final_solver_status"] = call["status"]
        try:
            statistics = solver.statistics()
            call["solver_statistics"] = {key: statistics.get_key_value(key) for key in statistics.keys()}
        except Exception as error:
            _backend_error(report, "statistics", error, call)
        report["statistics_seconds"] += perf_counter()-check_end
        if report["backend_errors"]:
            break
        if outcome == z3.unsat:
            report.update(status="COMPLETE", complete=True, stop_reason="final_unsat",
                          completion_seconds=perf_counter()-start)
            break
        if outcome == z3.unknown:
            try:
                call["reason_unknown"] = solver.reason_unknown()
            except Exception as error:
                _backend_error(report, "reason_unknown", error, call)
            else:
                report.update(stop_reason="solver_unknown", reason_unknown=call["reason_unknown"])
            break

        extraction_start = perf_counter()
        try:
            model = solver.model()
            u = sum(int(z3.is_true(model.eval(expr, model_completion=True))) << j
                    for j, expr in enumerate(u_exprs))
            call["projected_u"] = u
            model_word = [model.eval(expr, model_completion=True).as_long() for expr in x_exprs]
        except Exception as error:
            _backend_error(report, "model_extraction", error, call)
        call["model_extraction_seconds"] = perf_counter()-extraction_start
        report["model_extraction_seconds"] += call["model_extraction_seconds"]
        if report["backend_errors"]:
            break
        verification_start = perf_counter()
        word, errors = _verify_projection(report, u, model_word)
        call.update(verified=not errors, verification_errors=errors,
                    verification_seconds=perf_counter()-verification_start)
        report["verification_seconds"] += call["verification_seconds"]
        if errors:
            report["invalid_models"] += 1
            call["invalid_model_word_in_residual_order"] = model_word
            report["stop_reason"] = "invalid_model"
            break
        dedup_start = perf_counter()
        duplicate = u in seen
        seen.add(u)
        report["deduplication_seconds"] += perf_counter()-dedup_start
        if duplicate:
            report["duplicate_models"] += 1
            report["stop_reason"] = "duplicate_projected_model"
            break
        report["solutions"].append({"u": u, "residual_word": word,
                                    "independently_verified": True, "origin": "solver"})
        report["solver_model_count"] += 1
        accepted_at = perf_counter()-start
        if report["first_verified_model_seconds"] is None:
            report["first_verified_model_seconds"] = accepted_at
        if report["first_solver_model_seconds"] is None:
            report["first_solver_model_seconds"] = accepted_at
        blocking_start = perf_counter()
        try:
            _block_projection(solver, z3, u_exprs, u)
        except Exception as error:
            _backend_error(report, "projected_blocking", error, call)
        call["blocking_seconds"] = perf_counter()-blocking_start
        report["blocking_seconds"] += call["blocking_seconds"]
        if report["backend_errors"]:
            break
        report["projected_blocks"] += 1
    else:
        report["stop_reason"] = "max_models"

    return _finish(report, start, setup_end)
