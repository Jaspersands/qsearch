"""Exact feasibility audit of the nonlinear residual chain's quadratic lift.

This is a classical attack falsifier, NOT a general classical lower bound.
The native input loader reads data only; no external author code is executed.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import sys

import numpy as np
from flint import nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.nonlinear_filter_pinning import binomial_tail, enclose
from theorems.prime_character_opi import ring

REPORT = ROOT / "research/classical_baselines/nonlinear_residual_lift.json"
REFERENCE_COMMIT = "d9de27218b594925fcd60d8b6c6115a1c74397c7"
REFERENCE_INSTANCE = "residual-p2053-n205-281cdca8d31c880a"
REFERENCE_INDEX_SHA256 = "d90de1adef52278cf1391323aa8ce08d1bd36ebc70e526fb45de7967143f125f"


def canonical(values, size, p):
    values = tuple(values)
    if len(values) != size or any(type(v) is not int or not 0 <= v < p for v in values):
        raise ValueError("canonical field vector of the required length expected")
    return values


@dataclass(frozen=True)
class Chain:
    p: int
    n: int
    points: tuple[int, ...]
    multipliers: tuple[int, ...]

    def __post_init__(self):
        if type(self.p) is not int or not 3 <= self.p < 2**63:
            raise ValueError("odd word prime required")
        ring(self.p)
        if type(self.n) is not int or not 1 <= self.n <= len(self.points):
            raise ValueError("polynomial dimension must fit the evaluation set")
        canonical(self.points, len(self.points), self.p)
        canonical(self.multipliers, len(self.points)-1, self.p)
        if len(self.points) < 2 or len(set(self.points)) != len(self.points) or 0 in self.points:
            raise ValueError("distinct nonzero ordered evaluation points required")
        if 0 in self.multipliers:
            raise ValueError("nonzero residual multipliers required")

    @property
    def M(self):
        return len(self.points)-1

    @property
    def dimension(self):
        return 3*self.n-1

    def row(self, edge):
        if type(edge) is not int or not 0 <= edge < self.M:
            raise ValueError("physical edge index required")
        x, y, a = self.points[edge], self.points[edge+1], self.multipliers[edge]
        return ([pow(y, j, self.p) for j in range(self.n)]
                + [a*pow(x, j, self.p) % self.p for j in range(2*self.n-1)])


def evaluate(coefficients, point, p):
    value = 0
    for coefficient in reversed(coefficients):
        value = (value*point+coefficient) % p
    return value


def square(coefficients, p):
    n = len(coefficients)
    canonical(coefficients, n, p)
    if not n:
        raise ValueError("nonempty polynomial coefficient vector required")
    return tuple(sum(coefficients[j]*coefficients[k-j]
                     for j in range(max(0, k-n+1), min(n-1, k)+1)) % p
                 for k in range(2*n-1))


def residuals(chain, coefficients, lifted_square=None):
    c = canonical(coefficients, chain.n, chain.p)
    q = square(c, chain.p) if lifted_square is None else canonical(lifted_square, 2*chain.n-1, chain.p)
    return tuple((evaluate(c, chain.points[i+1], chain.p)
                  + a*evaluate(q, chain.points[i], chain.p)) % chain.p
                 for i, a in enumerate(chain.multipliers))


def square_defect(chain, coefficients, lifted_square):
    c = canonical(coefficients, chain.n, chain.p)
    q = canonical(lifted_square, 2*chain.n-1, chain.p)
    return tuple((v-w) % chain.p for v, w in zip(q, square(c, chain.p)))


def checked_basis(chain, edges):
    edges = tuple(edges)
    if len(edges) != chain.dimension or len(set(edges)) != len(edges):
        raise ValueError("a complete distinct-edge lift basis is required")
    matrix = nmod_mat([chain.row(i) for i in edges], chain.p)
    if matrix.rank() != chain.dimension:
        raise ValueError("singular lift basis: no uniqueness or dimension claim allowed")
    return matrix


def solve_lift(chain, edges, assigned_residuals):
    """Solve a square linear relaxation; this does NOT accept a native witness."""
    values = canonical(assigned_residuals, chain.dimension, chain.p)
    matrix = checked_basis(chain, edges)
    solution = matrix.solve(nmod_mat([[v] for v in values], chain.p))
    c = tuple(int(solution[j, 0]) for j in range(chain.n))
    q = tuple(int(solution[chain.n+j, 0]) for j in range(2*chain.n-1))
    actual = residuals(chain, c, q)
    if tuple(actual[i] for i in edges) != values:
        raise ArithmeticError("linear solve failed exact residual replay")
    return c, q


def classify_residual(chain, edges, requested):
    """Given a verified full-rank basis, decide exact original image membership.

    Rank-deficient cases deliberately raise instead of treating one arbitrary
    relaxed representative as proof that no square-consistent one exists.
    """
    requested = canonical(requested, chain.M, chain.p)
    c, q = solve_lift(chain, edges, tuple(requested[i] for i in edges))
    replay = residuals(chain, c, q)
    mismatch = [i for i, (a, b) in enumerate(zip(requested, replay)) if a != b]
    defect = square_defect(chain, c, q)
    status = ("OUTSIDE_LINEAR_LIFT" if mismatch else
              "OUTSIDE_ORIGINAL_IMAGE" if any(defect) else "VERIFIED_ORIGINAL_POLYNOMIAL")
    return {"status": status, "coefficients": list(c), "lifted_square": list(q),
            "square_defect": list(defect), "whole_residual_mismatch_edges": mismatch,
            "basis_edges": list(edges), "basis_rank": chain.dimension,
            "no_alternative_original_polynomial": status != "VERIFIED_ORIGINAL_POLYNOMIAL"}


def predicate_rows(chain, allowed):
    if len(allowed) != chain.M:
        raise ValueError("one explicit half-set per edge required")
    rows = []
    for row in allowed:
        values = tuple(row)
        canonical(values, (chain.p-1)//2, chain.p)
        if len(set(values)) != len(values):
            raise ValueError("half-set symbols must be distinct")
        rows.append(frozenset(values))
    return tuple(rows)


def forced_relaxation(chain, allowed, edges, seed=48211):
    """One preregistered draw, with both relaxed and original scores retained."""
    allowed = predicate_rows(chain, allowed)
    rng = random.Random(seed)
    chosen = tuple(rng.choice(sorted(allowed[i])) for i in edges)
    c, q = solve_lift(chain, edges, chosen)
    lifted = residuals(chain, c, q)
    original = residuals(chain, c)
    defect = square_defect(chain, c, q)
    return {"seed": seed, "basis_edges": list(edges), "basis_rank": chain.dimension,
            "assigned_passing_residuals": list(chosen), "coefficients": list(c),
            "lifted_square": list(q), "square_defect": list(defect),
            "square_defect_nonzero_coefficients": sum(v != 0 for v in defect),
            "relaxed_residuals": list(lifted), "original_residuals": list(original),
            "relaxed_score_NOT_a_witness": sum(v in row for v, row in zip(lifted, allowed)),
            "original_polynomial_score": sum(v in row for v, row in zip(original, allowed)),
            "exact_original_image_membership": not any(defect),
            "all_forced_edges_replayed": all(lifted[i] == v for i, v in zip(edges, chosen)),
            "complete_work": {"independent_runs": 1, "rerolls": 0,
                "linear_unknowns": chain.dimension, "square_linear_solves": 1,
                "basis_rank_checks": 1, "full_residual_scores": 2,
                "predicate_table_entries_read": chain.M*chain.p},
            "scope": "one native-input attack falsifier, not a performance campaign"}


def uniform_ensemble_contract(chain, edges, threshold):
    """Exact statements for independent random half-set inputs, not fixed tables.

    Draw F_i uniformly, then one uniform member per basis row. The assigned
    vector, hence the full-rank lifted coefficients (P,Q), is uniform. Each
    residual Q(alpha)-P(alpha)^2 is uniform conditional on P.
    """
    checked_basis(chain, edges)
    p, M, k, h = chain.p, chain.M, chain.dimension, (chain.p-1)//2
    if type(threshold) is not int or not 0 <= threshold <= M+1:
        raise ValueError("physical score threshold required")
    rho = Fraction(h, p)
    recovered_pin_mean = Fraction(1, p)+(1-Fraction(1, p))*Fraction(h-1, p-1)
    if recovered_pin_mean != rho:
        raise ArithmeticError("projection mean identity failed")
    tail = binomial_tail(M-k, rho, threshold-k)
    return {"assumptions": ["fixed public structure with verified full-rank edge basis",
                "independent uniform half-size predicate sets, not an arbitrary fixed input",
                "one uniformly selected member per basis set, no selection or retries",
                "original projection retains only the solved P coefficients"],
            "relaxed_score_law": f"{k}+Binomial({M-k},{rho})",
            "relaxed_mean_exact": str(k+(M-k)*rho),
            "projected_original_mean_exact": str(M*rho),
            "projected_pin_pass_probability_exact": str(recovered_pin_mean),
            "relaxed_tail_threshold": threshold,
            "relaxed_tail_lower": str(enclose(tail)),
            "square_consistency_probability_exact": str(Fraction(1, p**(2*chain.n-1))),
            "original_polynomial_count_decimal": str(p**chain.n),
            "linear_lift_count_decimal": str(p**k),
            "square_is_not_sufficient_unless_it_is_THE_SAME_P_squared": True,
            "ideal_uniform_choices_not_a_certificate_for_one_fixed_PRNG_seed": True,
            "full_original_score_law_identified": False,
            "bound_on_optimized_or_correlated_lift_search": False}


def constant_multiplier_collision_control():
    """A low-rank counterexample prevents extending the full-rank inverse claim."""
    chain = Chain(7, 2, tuple(range(1, 7)), (1,)*5)
    rows = [chain.row(i) for i in range(chain.M)]
    zero, other = (0, 0), (6, 0)
    fake_c, fake_q = (0, 1), (6, 6, 0)
    if (residuals(chain, zero) != residuals(chain, other)
            or residuals(chain, fake_c, fake_q) != residuals(chain, zero)
            or not any(square_defect(chain, fake_c, fake_q))):
        raise ArithmeticError("constant-polynomial collision disappeared")
    return {"p": 7, "n": 2, "lift_rank": nmod_mat(rows, 7).rank(),
            "nominal_lift_dimension": chain.dimension,
            "distinct_original_coefficients": [list(zero), list(other)],
            "invalid_lift_with_same_feasible_residual": {"P": list(fake_c), "Q": list(fake_q)},
            "common_residual": list(residuals(chain, zero)),
            "calibration_only": True}


def exhaustive_control():
    chain = Chain(7, 2, tuple(range(1, 7)), (1, 2, 4, 1, 3))
    edges = tuple(range(chain.dimension))
    checked_basis(chain, edges)
    feasible = {residuals(chain, c) for c in product(range(chain.p), repeat=chain.n)}
    lifted, accepted = set(), set()
    for c in product(range(chain.p), repeat=chain.n):
        for q in product(range(chain.p), repeat=2*chain.n-1):
            r = residuals(chain, c, q)
            lifted.add(r)
            if not any(square_defect(chain, c, q)):
                accepted.add(r)
    if feasible != accepted or len(lifted) != chain.p**chain.dimension:
        raise ArithmeticError("exhaustive square gate or lift injection failed")
    return {"p": chain.p, "n": chain.n, "rank": chain.dimension,
            "lifted_residuals_enumerated": len(lifted), "native_polynomials": len(feasible),
            "accepted_exactly_original_image": True,
            "uniform_lift_acceptance": str(Fraction(len(accepted), len(lifted))),
            "calibration_only_NOT_advantage_evidence": True}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_reference(reference):
    """Load one fixed author instance after checking index and manifest hashes."""
    reference = Path(reference).resolve()
    manifest = {}
    for line in (reference / "SHA256SUMS").read_text().splitlines():
        if line.strip():
            digest, name = line.split(maxsplit=1)
            manifest[name.lstrip("*")] = digest

    def checked(name, expected=None):
        path = (reference / name).resolve()
        if not path.is_relative_to(reference) or Path(name).is_absolute():
            raise ValueError("reference path escapes root")
        digest = sha256(path)
        if name not in manifest or digest != manifest[name] or (expected and digest != expected):
            raise ValueError("reference checksum mismatch")
        return path

    index_path = checked("index.json", REFERENCE_INDEX_SHA256)
    index = json.loads(index_path.read_text())
    item = next(row for row in index["instances"] if row["instance_id"] == REFERENCE_INSTANCE)
    metadata_path = checked(item["metadata_path"], item["metadata_sha256"])
    arrays_path = checked(item["arrays_path"], item["arrays_sha256"])
    metadata = json.loads(metadata_path.read_text())
    if (metadata["instance_id"] != REFERENCE_INSTANCE
            or metadata["arrays_sha256"] != item["arrays_sha256"]
            or metadata["content_digest"] != item["instance_sha256"]):
        raise ValueError("inconsistent reference metadata")
    with np.load(arrays_path, allow_pickle=False) as arrays:
        chain = Chain(int(metadata["p"]), int(metadata["n"]),
                      tuple(map(int, arrays["alpha"])), tuple(map(int, arrays["residual_coefficients"])))
        table = arrays["allowed"]
        if table.shape != (chain.M, chain.p) or table.dtype != np.bool_:
            raise ValueError("boolean explicit predicate table required")
        allowed = tuple(tuple(map(int, np.flatnonzero(row))) for row in table)
    predicate_rows(chain, allowed)
    return chain, allowed, {"instance_id": REFERENCE_INSTANCE,
            "repository": "https://github.com/dsfranca/RDQINumerics", "tag": "v1.0.0",
            "reference_release_commit": REFERENCE_COMMIT,
            "data_license": "CC-BY-4.0", "code_license": "MIT; no author code imported",
            "index_sha256": sha256(index_path), "metadata_path": item["metadata_path"],
            "metadata_sha256": sha256(metadata_path), "arrays_path": item["arrays_path"],
            "arrays_sha256": sha256(arrays_path), "instance_content_digest": item["instance_sha256"],
            "archive_complete": index["complete_raw_archive"],
            "original_batches_available": index["available_task_count"],
            "original_batches_expected": index["expected_task_count"],
            "all_original_witnesses_verified_by_this_pass": False,
            "natural_evaluation_order": chain.points == tuple(range(1, chain.p))}


def verify_frozen_witnesses_and_attack_inventory(reference):
    """Independently verify all 880 final polynomial witnesses and inventory 22 classical attacks.

    Checks SHA-256 digests, evaluation order, multipliers, and half-set tables across all
    20 instances without executing author code or rerunning missing raw batches (116/120).
    """
    reference = Path(reference).resolve()
    manifest = {}
    for line in (reference / "SHA256SUMS").read_text().splitlines():
        if line.strip():
            digest, name = line.split(maxsplit=1)
            manifest[name.lstrip("*")] = digest

    def checked(name, expected=None):
        path = (reference / name).resolve()
        if not path.is_relative_to(reference) or Path(name).is_absolute():
            raise ValueError("reference path escapes root")
        digest = sha256(path)
        if name not in manifest or digest != manifest[name] or (expected and digest != expected):
            raise ValueError(f"reference checksum mismatch for {name}")
        return path

    index_path = checked("index.json", REFERENCE_INDEX_SHA256)
    index = json.loads(index_path.read_text())
    witnesses_path = checked(index["witnesses_path"])
    tasks_path = checked(index["tasks_path"])
    runs_csv_info = index["tables"]["runs.csv"]
    runs_csv_path = checked(runs_csv_info["path"], runs_csv_info["sha256"])

    witness_payload = json.loads(witnesses_path.read_text())
    witness_rows = witness_payload["witnesses"]
    if len(witness_rows) != 880 or witness_payload["expected_run_count"] != 880:
        raise ValueError("expected 880 frozen witness records")

    with runs_csv_path.open(newline="") as fp:
        run_ledger_rows = {row["run_id"]: row for row in csv.DictReader(fp)}
    if len(run_ledger_rows) != 880:
        raise ValueError("expected 880 run cost-ledger rows in tables/runs.csv")

    by_instance = defaultdict(list)
    for row in witness_rows:
        by_instance[row["instance_id"]].append(row)

    verified_count = 0
    provenance_counts = defaultdict(int)
    method_records = defaultdict(list)
    instance_summaries = []
    overall_best = None
    primary_best = None

    for item in index["instances"]:
        instance_id = item["instance_id"]
        meta_path = checked(item["metadata_path"], item["metadata_sha256"])
        arr_path = checked(item["arrays_path"], item["arrays_sha256"])
        meta = json.loads(meta_path.read_text())
        p, n = int(meta["p"]), int(meta["n"])
        with np.load(arr_path, allow_pickle=False) as arrays:
            alpha = arrays["alpha"].astype(np.int64)
            multipliers = arrays["residual_coefficients"].astype(np.int64)
            allowed = arrays["allowed"]
        chain = Chain(p, n, tuple(map(int, alpha)), tuple(map(int, multipliers)))
        if allowed.shape != (chain.M, chain.p) or allowed.dtype != np.bool_:
            raise ValueError("invalid predicate table shape or dtype")
        if not np.all(allowed.sum(axis=1) == (p-1)//2):
            raise ValueError("predicate rows must be exact halfsets")

        Vandermonde = np.ones((len(alpha), n), dtype=np.int64)
        for j in range(1, n):
            Vandermonde[:, j] = (Vandermonde[:, j-1]*alpha) % p

        rows = by_instance[instance_id]
        if len(rows) != 44:
            raise ValueError(f"expected 44 witnesses for {instance_id}")
        C = np.array([canonical(w["coefficients"], n, p) for w in rows], dtype=np.int64)
        values = (C @ Vandermonde.T) % p
        res = (values[:, 1:] + multipliers[None, :]*((values[:, :-1]*values[:, :-1]) % p)) % p
        scores = allowed[np.arange(chain.M)[None, :], res].sum(axis=1)

        inst_best_score = -1
        inst_best_method = None
        for w, actual_score in zip(rows, map(int, scores)):
            run_id = w["official_run_id"]
            if run_id not in run_ledger_rows:
                raise ValueError(f"missing cost-ledger row for {run_id}")
            ledger = run_ledger_rows[run_id]
            if (actual_score != w["score"]
                    or actual_score != int(ledger["best_score"])
                    or w["witness_digest"] != ledger["witness_digest"]
                    or ledger["witness_verified"] not in ("1", "True", "true")
                    or abs(w["satisfaction"] - actual_score/chain.M) > 1e-12):
                raise ArithmeticError(f"witness replay or ledger mismatch on {run_id}")
            verified_count += 1
            provenance_counts[w["recovery_provenance"]] += 1
            method_records[w["method"]].append((w, ledger))
            if actual_score > inst_best_score:
                inst_best_score = actual_score
                inst_best_method = w["method"]
            candidate_summary = {
                "instance_id": instance_id,
                "official_run_id": run_id,
                "method": w["method"],
                "score": actual_score,
                "tests": chain.M,
                "satisfaction_exact": str(Fraction(actual_score, chain.M)),
                "witness_digest": w["witness_digest"],
                "recovery_provenance": w["recovery_provenance"],
            }
            if overall_best is None or actual_score > overall_best["score"]:
                overall_best = candidate_summary
            if instance_id == REFERENCE_INSTANCE and (
                primary_best is None or actual_score > primary_best["score"]
            ):
                primary_best = candidate_summary

        instance_summaries.append({
            "instance_id": instance_id,
            "structural_seed": int(rows[0]["structural_seed"]),
            "target_replica": int(rows[0]["target_replica"]),
            "witnesses_verified": len(rows),
            "best_score": inst_best_score,
            "best_method": inst_best_method,
            "natural_evaluation_order": chain.points == tuple(range(1, p)),
        })

    attack_inventory = []
    for method in sorted(method_records):
        pairs = method_records[method]
        scores = [w["score"] for w, _ in pairs]
        ledgers = [l for _, l in pairs]
        cand_evals = [int(l["candidate_evaluations_including_warm_start"] or 0) for l in ledgers]
        full_obj = [int(l["full_objective_evaluations_including_warm_start"] or 0) for l in ledgers]
        pred_evals = [int(l["predicate_or_factor_evaluations"] or 0) for l in ledgers]
        setup_lookups = [int(l["setup_graph_table_lookups"] or 0) for l in ledgers]
        table_lookups = [int(l["graph_table_lookups"] or 0) for l in ledgers]
        cpu_secs = [float(l["cpu_seconds_including_warm_start"] or 0.0) for l in ledgers]
        auth_runs = sum(w["recovery_provenance"] == "authenticated_accepted_campaign" for w, _ in pairs)
        earlier_runs = sum(
            w["recovery_provenance"] == "earlier_attempt_matching_final_table_witness_only"
            for w, _ in pairs
        )
        attack_inventory.append({
            "method": method,
            "base_method": ledgers[0]["base_method"],
            "warm_started": ledgers[0]["warm_started"] in ("1", "True", "true"),
            "warm_source_method": ledgers[0]["warm_source_method"] or None,
            "runs_verified": len(pairs),
            "authenticated_campaign_runs": auth_runs,
            "earlier_attempt_matching_final_table_witness_only_runs": earlier_runs,
            "min_score": min(scores),
            "mean_score_exact": str(Fraction(sum(scores), len(scores))),
            "max_score": max(scores),
            "mean_candidate_evaluations_including_warm_start_exact": str(
                Fraction(sum(cand_evals), len(cand_evals))
            ),
            "mean_full_objective_evaluations_including_warm_start_exact": str(
                Fraction(sum(full_obj), len(full_obj))
            ),
            "mean_predicate_or_factor_evaluations_exact": str(
                Fraction(sum(pred_evals), len(pred_evals))
            ),
            "mean_setup_graph_table_lookups_exact": str(
                Fraction(sum(setup_lookups), len(setup_lookups))
            ),
            "mean_graph_table_lookups_exact": str(
                Fraction(sum(table_lookups), len(table_lookups))
            ),
            "mean_cpu_seconds_including_warm_start": sum(cpu_secs)/len(cpu_secs),
            "full_table_access_required": True,
            "folded_oracle_lower_bound_applies": False,
        })

    return {
        "repository": "https://github.com/dsfranca/RDQINumerics",
        "zenodo_record": "https://zenodo.org/records/17619922",
        "tag": "v1.0.0",
        "reference_release_commit": REFERENCE_COMMIT,
        "credit": "Zhong-Xia Shang and Daniel Stilck Franca (CC-BY-4.0 data, MIT code; no author code executed)",
        "index_sha256": sha256(index_path),
        "witnesses_sha256": sha256(witnesses_path),
        "tasks_sha256": sha256(tasks_path),
        "runs_csv_sha256": sha256(runs_csv_path),
        "instances_verified": len(instance_summaries),
        "witnesses_verified": verified_count,
        "expected_witness_count": 880,
        "all_880_final_witnesses_independently_verified": verified_count == 880,
        "available_raw_batches": int(index["available_task_count"]),
        "expected_raw_batches": int(index["expected_task_count"]),
        "complete_raw_archive": bool(index["complete_raw_archive"]),
        "recovery_provenance_counts": dict(provenance_counts),
        "missing_raw_batches_rerun_or_invented": False,
        "full_table_access_and_preprocessing_charged": True,
        "folded_oracle_lower_bound_applies_to_public_scalar_tables": False,
        "overall_best_witness": overall_best,
        "primary_instance_best_witness": primary_best,
        "instances": instance_summaries,
        "classical_attack_inventory": attack_inventory,
    }


def run_audit(reference=None):
    report = {"schema": "nonlinear-residual-lift-audit-v2", "status": "REVIEW_PENDING",
              "claim": "unconstrained quadratic lift is not an original optimization witness",
              "exhaustive_control": exhaustive_control(),
              "rank_deficient_countercontrol": constant_multiplier_collision_control(),
              "general_classical_hardness_established": False,
              "quantum_speedup_established": False}
    if reference is not None:
        chain, allowed, provenance = load_reference(reference)
        edges = tuple(range(chain.dimension))
        row = forced_relaxation(chain, allowed, edges)
        inventory = verify_frozen_witnesses_and_attack_inventory(reference)
        report["native"] = {"provenance": provenance, "p": chain.p, "n": chain.n, "M": chain.M,
                "points": list(chain.points), "multipliers": list(chain.multipliers),
                "attack": row, "random_predicate_ensemble_ONLY": uniform_ensemble_contract(chain, edges, 1299),
                "frozen_witness_and_attack_inventory": inventory}
    report["dependencies"] = {str(path.relative_to(ROOT)): sha256(path) for path in (
        Path(__file__), ROOT / "theorems/nonlinear_filter_pinning.py",
        ROOT / "theorems/prime_character_opi.py")}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, help="frozen RDQINumerics data/reference directory")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write and args.reference is None:
        parser.error("--write requires --reference; do not overwrite native evidence with controls")
    result = run_audit(args.reference)
    if args.write:
        REPORT.write_text(json.dumps(result, indent=2)+"\n")
        print(REPORT)
    native = result.get("native", {}).get("attack", {})
    inventory = result.get("native", {}).get("frozen_witness_and_attack_inventory", {})
    print(json.dumps({"status": result["status"], "exhaustive": result["exhaustive_control"],
        "relaxed_score_NOT_a_witness": native.get("relaxed_score_NOT_a_witness"),
        "original_score": native.get("original_polynomial_score"),
        "square_defect_nonzero": native.get("square_defect_nonzero_coefficients"),
        "witnesses_verified": inventory.get("witnesses_verified"),
        "overall_best_score": (inventory.get("overall_best_witness") or {}).get("score")}, indent=2))


if __name__ == "__main__":
    main()
