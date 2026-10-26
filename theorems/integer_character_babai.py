"""Exact classical Babai test on the frozen integer-character lattice.

LLL is only a basis generator. Membership, its full index, Gram--Schmidt
bounds, nearest-plane rounding and the final distance are checked exactly.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import fmpz_mat

from theorems import integer_character_near_vector as near

REPORT = ROOT / "research/classical_baselines/integer_character_babai.json"
BASIS = ROOT / "research/classical_baselines/integer_character_babai_basis.json.gz"


def _round_profile(rows, order, target, pivots, upper_rows, prefix, offset=0):
    m, rank = len(rows), len(prefix)
    d = m-rank
    coefficients = [0]*m
    for k in range(d-1, -1, -1):
        numerator = upper_rows[k][d]-order*sum(
            coefficients[rank+i]*upper_rows[k][i] for i in range(k+1, d))
        divisor = order*pivots[rank+k]
        coefficients[rank+k] = (2*numerator+divisor)//(2*divisor)
        if k == d-1:
            coefficients[rank+k] += offset
    for i, (j, sign) in enumerate(prefix):
        residual = target[j]-sum(coefficients[k]*rows[k][j] for k in range(rank, m))
        coefficients[i] = (2*sign*residual+order)//(2*order)
    point = [sum(c*row[j] for c, row in zip(coefficients, rows)) for j in range(m)]
    return coefficients, point


def exact_normalized_babai(rows, labels, order, target, *, bits=96, progress=None):
    near.validate_labels(labels, order)
    m = len(labels)
    if (len(rows) != m or any(len(row) != m for row in rows)
            or len(target) != m or any(type(c) is not int for c in target)
            or type(bits) is not int or bits < 16):
        raise ValueError("square integer basis, integer target and dyadic precision required")
    for row in rows:
        near.recover_assignment(labels, order, row)
    # Remove leading +/-N coordinate rows analytically, not by dropping
    # constraints. Their exact GS lengths and final rounding stay in the result.
    prefix, occupied = [], set()
    for row in rows:
        support = [j for j, v in enumerate(row) if v]
        if len(support) != 1 or abs(row[support[0]]) != order:
            break
        j = support[0]
        if j in occupied:
            raise ValueError("basis is singular")
        prefix.append((j, row[j]//order))
        occupied.add(j)
    rank = len(prefix)
    columns = [j for j in range(m) if j not in occupied]
    core = [[row[j] for j in columns] for row in rows[rank:]]
    d = len(core)
    # N*target lies in the numerator lattice, retaining rank one modulo N.
    extended = fmpz_mat(core+[[order*target[j] for j in columns]]) if d else None
    matrix = extended*extended.transpose() if d else None
    del extended
    denominator = order*order
    pivots, upper_rows = [order*order]*rank, []
    lower_units = upper_units = rank << bits
    if progress:
        progress({"phase": "exact_coordinate_elimination", "rows": rank,
                  "remaining_dimension": d, "full_dimension": m})
    for k in range(d):
        pivot = int(matrix[k, k])
        if pivot <= 0:
            raise ValueError("basis is singular or the normalized elimination failed")
        upper_rows.append([int(matrix[k, j]) for j in range(d+1)])
        gs_denominator = order*order if k == 0 else pivots[-1]
        quotient, remainder = divmod(pivot << bits, gs_denominator)
        lower_units += quotient
        upper_units += quotient+bool(remainder)
        pivots.append(pivot)
        if k+1 < d:
            column = fmpz_mat([[matrix[i, k]] for i in range(d+1)])
            matrix = (pivot*matrix-column*column.transpose())/denominator
            denominator = pivot
        if progress and ((k+1) % 32 == 0 or k+1 == d):
            progress({"phase": "exact_gram_schmidt", "rows": rank+k+1, "of": m})
    if pivots[-1] != 1:
        raise ValueError("basis has the wrong lattice index")
    coefficients, point = _round_profile(rows, order, target, pivots, upper_rows, prefix)
    assignment = near.recover_assignment(labels, order, point)
    squared = Q(sum((c-v)**2 for c, v in zip(target, point)), m*order*order)
    trace_lower, trace_upper = Q(lower_units, 2**bits), Q(upper_units, 2**bits)
    if squared > trace_upper/(4*m):
        raise ArithmeticError("nearest-plane witness violates its exact covering bound")
    return {
        "normalized_gram_pivots": pivots,
        "basis_coefficients": coefficients, "point": point, "assignment": assignment,
        "mean_square": squared,
        "normalized_gs_trace_lower": trace_lower,
        "normalized_gs_trace_upper": trace_upper,
        "all_target_mean_square_upper": trace_upper/(4*m),
        "continuous_haar_mean_square_lower": trace_lower/(12*m),
        "continuous_haar_mean_square_upper": trace_upper/(12*m),
        "dyadic_precision": bits, "full_lattice_index_verified": True,
        "stored_pivot_bits_max": max(p.bit_length() for p in pivots),
        "orthogonal_integer_prefix_rank": rank, "exact_core_dimension": d,
        "rounding_profile": {"upper_rows": upper_rows, "prefix": prefix},
    }


def bounded_last_plane_search(rows, labels, order, target, exact, *, radius=32):
    if type(radius) is not int or radius < 0:
        raise ValueError("nonnegative integer branch radius required")
    profile = exact["rounding_profile"]
    pivots = exact["normalized_gram_pivots"]
    last_squared = Q(pivots[-1], pivots[-2] if len(pivots) > 1 else order*order)
    offsets = [0]+[sign*k for k in range(1, radius+1) for sign in (1, -1)]
    trials, best = [], None
    for offset in offsets:
        if offset == 0:
            coefficients, point = exact["basis_coefficients"], exact["point"]
        else:
            coefficients, point = _round_profile(
                rows, order, target, pivots, profile["upper_rows"], profile["prefix"], offset)
        assignment = near.recover_assignment(labels, order, point)
        raw_square = Q(sum((c-v)**2 for c, v in zip(target, point)), len(rows)*order*order)
        # Only the final orthogonal residual may exceed half a cell.
        bound = exact["all_target_mean_square_upper"] + (
            offset*offset+abs(offset))*last_squared/len(rows)
        if raw_square > bound:
            raise ArithmeticError("branch witness violates the exact displaced-plane bound")
        canonical = near.witness(labels, target, order, assignment)
        if canonical["mean_square"] > raw_square:
            raise ArithmeticError("branch coordinate centering worsened distance")
        trials.append({"offset": offset, "assignment_decimal": str(assignment),
                       "mean_square": str(canonical["mean_square"]),
                       "threshold_met": canonical["accepted"]})
        if best is None or canonical["mean_square"] < Q(best["mean_square"]):
            best = dict(trials[-1], raw_mean_square=str(raw_square),
                        basis_coefficients_decimal=list(map(str, coefficients)),
                        point_decimal=list(map(str, point)))
    return {
        "method": "deterministic_bounded_last_plane_enumeration_with_exact_back_substitution",
        "predeclared_radius": radius, "trials_evaluated": len(trials),
        "unique_assignments": len({t["assignment_decimal"] for t in trials}),
        "trials": trials, "best": best,
        "last_normalized_gs_squared": str(last_squared),
        "max_all_target_bound_increment": str(radius*(radius+1)*last_squared/len(rows)),
        "independent_samples_assumed": False,
        "asymptotic_dequantization_claimed": False,
    }


def write_basis(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+".tmp")
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with io.TextIOWrapper(zipped, encoding="ascii") as text:
                json.dump(rows, text, separators=(",", ":"))
                text.write("\n")
    temporary.replace(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_basis(path):
    with gzip.open(path, "rt", encoding="ascii") as source:
        return json.load(source)


def provenance_path(path):
    return path.with_suffix("").with_suffix(".provenance.json")


def native_report(*, basis_path=BASIS, reuse_basis=False, progress=None):
    input_bytes = near.REPORT.read_bytes()
    source = json.loads(input_bytes)
    if source["producer_sha256"] != hashlib.sha256(Path(near.__file__).read_bytes()).hexdigest():
        raise ValueError("reproduce the native near-vector input before this attack")
    native = source["native"]
    labels = list(map(int, native["public_labels_decimal"]))
    centers = list(map(int, native["centers_decimal"]))
    order = int(native["cyclic_order_decimal"])
    if native["length"] != 1024 or native["moment_budget"] != 16:
        raise ValueError("this attack is predeclared for the full native J16 instance")
    input_hash = hashlib.sha256(input_bytes).hexdigest()
    started = time.perf_counter()
    if reuse_basis:
        provenance = json.loads(provenance_path(basis_path).read_text())
        basis_hash = hashlib.sha256(basis_path.read_bytes()).hexdigest()
        if (provenance["basis_artifact_sha256"] != basis_hash
                or provenance["input_artifact_sha256"] != input_hash
                or provenance["dimension"] != len(labels)
                or provenance["method"] != "FLINT LLL"
                or provenance["delta"] != .99 or provenance["eta"] != .51):
            raise ValueError("saved basis provenance does not match the declared input")
        rows = read_basis(basis_path)
    else:
        _, basis = near.lattice_bases(labels, order)
        if progress:
            progress({"phase": "lll_begin", "dimension": len(labels), "delta": .99, "eta": .51})
        reduced = fmpz_mat(basis).lll(delta=.99, eta=.51)
        rows = [[int(v) for v in row] for row in reduced.tolist()]
        del basis, reduced
        lll_seconds = time.perf_counter()-started
        if progress:
            progress({"phase": "lll_complete", "seconds": lll_seconds})
        basis_hash = write_basis(basis_path, rows)
        provenance = {
            "basis_artifact_sha256": basis_hash, "input_artifact_sha256": input_hash,
            "dimension": len(labels), "method": "FLINT LLL", "delta": .99, "eta": .51,
            "wall_seconds": lll_seconds,
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "prior_incomplete_verification_attempts": [],
        }
        provenance_path(basis_path).write_text(json.dumps(provenance, indent=2)+"\n")
    basis_load_or_generation_seconds = time.perf_counter()-started
    started = time.perf_counter()
    exact = exact_normalized_babai(rows, labels, order, centers, progress=progress)
    exact_seconds = time.perf_counter()-started
    canonical = near.witness(labels, centers, order, exact["assignment"])
    if canonical["mean_square"] > exact["mean_square"]:
        raise ArithmeticError("coordinate centering worsened the verified distance")
    if progress:
        progress({"phase": "bounded_last_plane_search", "radius": 32, "trials": 65})
    started = time.perf_counter()
    branch = bounded_last_plane_search(rows, labels, order, centers, exact, radius=32)
    branch["wall_seconds"] = time.perf_counter()-started
    return {
        "schema": "integer_character_babai_v3",
        "status": "exact_classical_attack_on_one_frozen_native_instance",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_artifact_sha256": input_hash,
        "dimension": len(labels), "cyclic_order_bits": order.bit_length(),
        "center_seed": native["center_seed"],
        "basis_artifact": str(basis_path.relative_to(ROOT)),
        "basis_artifact_sha256": basis_hash,
        "basis_compressed_bytes": basis_path.stat().st_size,
        "basis_generation": dict(provenance, reused_basis=reuse_basis,
                                 quality_assumed_in_certificate=False,
                                 current_load_or_generation_seconds=basis_load_or_generation_seconds),
        "basis_provenance_artifact": str(provenance_path(basis_path).relative_to(ROOT)),
        "basis_provenance_sha256": hashlib.sha256(provenance_path(basis_path).read_bytes()).hexdigest(),
        "exact_arithmetic": {
            "wall_seconds": exact_seconds, "schur_steps": exact["exact_core_dimension"],
            "orthogonal_integer_prefix_rank": exact["orthogonal_integer_prefix_rank"],
            "full_dimension": len(labels),
            "dyadic_precision": exact["dyadic_precision"],
            "stored_pivot_bits_max": exact["stored_pivot_bits_max"],
            "normalized_gram_pivots_decimal": list(map(str, exact["normalized_gram_pivots"])),
            "terminal_normalized_pivot": str(exact["normalized_gram_pivots"][-1]),
            "full_lattice_index_verified": True,
        },
        "normalized_gs_trace_interval": [
            str(exact["normalized_gs_trace_lower"]),
            str(exact["normalized_gs_trace_upper"])],
        "all_target_mean_square_upper": str(exact["all_target_mean_square_upper"]),
        "all_targets_meet_quantum_grid_threshold": (
            exact["all_target_mean_square_upper"] <= near.GRID_THRESHOLD),
        "continuous_haar_mean_square_interval": [
            str(exact["continuous_haar_mean_square_lower"]),
            str(exact["continuous_haar_mean_square_upper"])],
        "continuous_haar_interval_is_a_discrete_center_guarantee": False,
        "basis_coefficients_decimal": list(map(str, exact["basis_coefficients"])),
        "babai_point_decimal": list(map(str, exact["point"])),
        "assignment_decimal": str(exact["assignment"]),
        "babai_mean_square": str(exact["mean_square"]),
        "coordinate_centered_mean_square": str(canonical["mean_square"]),
        "native_threshold_met": canonical["accepted"],
        "bounded_last_plane_search": branch,
        "threshold": str(near.GRID_THRESHOLD),
        "classical_asymptotic_dequantization_proved": False,
        "failed_basis_proves_classical_hardness": False,
        "cost_scope": "input construction is charged in its source; basis provenance includes paid LLL and any incomplete verification attempt; current verification and basis loading/generation are timed separately",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    parser.add_argument("--basis-output", type=Path, default=BASIS)
    parser.add_argument("--reuse-basis", action="store_true",
                        help="verify the saved basis and provenance without repeating its paid LLL")
    args = parser.parse_args()
    progress = lambda value: print(json.dumps(value), flush=True)
    result = native_report(basis_path=args.basis_output, reuse_basis=args.reuse_basis,
                           progress=progress)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"output": str(args.output),
                      "babai_mean_square": float(Q(result["coordinate_centered_mean_square"])),
                      "babai_threshold_met": result["native_threshold_met"],
                      "bounded_search_best_mean_square": float(Q(result["bounded_last_plane_search"]["best"]["mean_square"])),
                      "bounded_search_threshold_met": result["bounded_last_plane_search"]["best"]["threshold_met"],
                      "all_target_mean_square_upper": float(Q(result["all_target_mean_square_upper"])),
                      "asymptotic_dequantization_claimed": False}), flush=True)


if __name__ == "__main__":
    main()
