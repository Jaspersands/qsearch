"""A secret-blind SDP/rounding attempt for actual native covariant records.

Numerical optimizer experiment, NOT a scalable recovery theorem. Full-group
controls, reference enumeration, solver residuals and failures stay explicit.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random
import time

import numpy as np
from scipy.sparse import csr_matrix

from ternary_character_synchronization import _records, character_validator, rank_one_character_lift
from ternary_covariant_noise import CovariantRecord, heldout_gate, heldout_score, simulated_record
from ternary_cyclic_extractor import random_even_source

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_character_sdp_decoder.json"
DERIVATION = ROOT / "research/TERNARY_CHARACTER_SDP_DECODER.md"


def _positive(value, name, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def compile_model(records, max_matrix_nodes=256, max_formal_nodes=20000):
    """Reuse the proved circuit, identify actual frequencies, enforce ALL differences."""
    records, n, q = _records(records)
    _positive(max_matrix_nodes, "matrix node cap")
    _positive(max_formal_nodes, "formal circuit node cap")
    if q > 2**20 or n*q*q >= 2**62:
        return {"status": "OUTSIDE_NUMERICAL_PHASE_PRECISION_SCOPE", "dimension": n, "modulus": q}
    validation = character_validator(records)
    if validation["rank_mod3"] < n:
        return {"status": "UNKNOWN_NO_FULL_UNIT_ROW_BASIS", "dimension": n, "modulus": q}
    try:
        lift = rank_one_character_lift(records, max_nodes=max_formal_nodes)
    except ValueError as error:
        if "node cap exceeded" not in str(error):
            raise
        return {"status": "FORMAL_CIRCUIT_CAP_EXHAUSTED", "dimension": n, "modulus": q,
                "max_formal_nodes": max_formal_nodes, "partial_relaxation_solved": False}
    nodes = tuple(dict.fromkeys(tuple(x["frequency"]) for x in lift["nodes"]))
    K = len(nodes)
    if K > max_matrix_nodes:
        return {"status": "MATRIX_CAP_EXHAUSTED", "dimension": n, "modulus": q,
                "required_matrix_nodes": K, "max_matrix_nodes": max_matrix_nodes,
                "formal_circuit_nodes": lift["matrix_dimension"], "partial_relaxation_solved": False}
    indices = {x: i for i, x in enumerate(nodes)}
    native = tuple((indices[r.first], indices[r.second]) for r in records)
    representatives, equalities = {}, []
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            d = tuple((a-b) % q for a, b in zip(u, v))
            location = K*i+j
            old = representatives.setdefault(d, location)
            if old != location:
                equalities.append((location, old))
    # A sparse vectorized operator avoids thousands of individual CVXPY objects.
    rows = np.repeat(np.arange(len(equalities)), 2)
    columns = np.array(equalities, dtype=int).reshape(-1)
    values = np.tile((1., -1.), len(equalities))
    operator = csr_matrix((values, (rows, columns)), shape=(len(equalities), K*K))
    Q = np.zeros((K, K), complex)
    for r, (a, c) in zip(records, native):
        for i, j, exponent in ((a, 0, r.outcome[0]), (c, 0, r.outcome[1]),
                                (a, c, (r.outcome[0]-r.outcome[1]) % q)):
            coefficient = np.exp(-2j*np.pi*exponent/q)
            Q[j, i] += coefficient/2
            Q[i, j] += coefficient.conjugate()/2
    flat_basis = validation["unit_basis_frequency_rows"]
    all_rows = tuple(row for r in records for row in (r.first, r.second))
    return {"status": "COMPILED", "dimension": n, "modulus": q, "nodes": nodes,
            "native_nodes": native, "basis_nodes": tuple(indices[all_rows[j]] for j in flat_basis),
            "unit_basis_frequency_rows": flat_basis,
            "basis_inverse": validation["modular_unit_basis_inverse"],
            "formal_circuit_nodes": lift["matrix_dimension"], "matrix_nodes": K,
            "complete_difference_entries": K*K, "distinct_differences": len(representatives),
            "difference_equalities": len(equalities), "equalities": equalities,
            "difference_operator": operator, "objective_matrix": Q,
            "full_secret_group_size": q**n, "full_group_saturation": K == q**n,
            "templates_read_outcomes": False, "rank_one_character_soundness_inherited": True}


def character_matrix(model, trial):
    trial = tuple(trial)
    if len(trial) != model["dimension"] or any(type(x) is not int or not 0 <= x < model["modulus"] for x in trial):
        raise ValueError("canonical full-root trial required")
    q = model["modulus"]
    v = np.array([np.exp(2j*np.pi*(sum(a*s for a, s in zip(row, trial)) % q)/q)
                  for row in model["nodes"]])
    return np.outer(v, v.conj())


def audit_matrix(model, matrix, tolerance=2e-5):
    if type(tolerance) not in (float, int) or not math.isfinite(tolerance) or not 0 < tolerance < .01:
        raise ValueError("finite small numerical feasibility tolerance required")
    X = np.asarray(matrix, dtype=complex)
    K = model["matrix_nodes"]
    if X.shape != (K, K) or not np.isfinite(X).all():
        return {"status": "MISSING_OR_NONFINITE_MATRIX", "numerically_feasible": False}
    hermitian = float(np.max(abs(X-X.conj().T)))
    diagonal = float(np.max(abs(np.diag(X)-1)))
    residual = model["difference_operator"] @ X.reshape(-1)
    differences = float(np.max(abs(residual))) if len(residual) else 0.
    eigenvalues = np.linalg.eigvalsh((X+X.conj().T)/2)
    minimum = float(eigenvalues[0])
    top_fraction = float(eigenvalues[-1]/K)
    feasible = max(hermitian, diagonal, differences, max(0., -minimum)) <= tolerance
    extra = {}
    if "cyclic_fourier_operator" in model:
        law = model["cyclic_fourier_operator"] @ X.reshape(-1)
        least = float(np.min(law.real)) if len(law) else 0.
        imaginary = float(np.max(abs(law.imag))) if len(law) else 0.
        feasible = feasible and least >= -tolerance and imaginary <= tolerance
        extra = {"minimum_complete_cyclic_probability": least,
                 "complete_cyclic_probabilities_checked": len(law),
                 "complete_cyclic_imaginary_residual": imaginary}
    return {"status": "NUMERICALLY_FEASIBLE" if feasible else "NUMERICAL_FEASIBILITY_FAILED",
            "numerically_feasible": feasible, "feasibility_tolerance": float(tolerance),
            "hermitian_residual": hermitian, "unit_diagonal_residual": diagonal,
            "all_equal_difference_residual": differences, "minimum_eigenvalue": minimum,
            "largest_eigenvalue_over_dimension": top_fraction,
            "objective_score": float(np.trace(model["objective_matrix"] @ X).real),
            "exact_PSD_or_optimality_certificate": False, **extra}


def solve_relaxation(model, max_iterations=12000, accuracy=2e-6):
    if model["status"] != "COMPILED":
        return {"status": model["status"], "matrix": None, "solver_invoked": False}
    _positive(max_iterations, "solver iteration cap")
    if type(accuracy) not in (float, int) or not math.isfinite(accuracy) or not 0 < accuracy < .001:
        raise ValueError("finite small solver accuracy required")
    try:
        import cvxpy as cp
    except ImportError:
        return {"status": "DEPENDENCY_UNAVAILABLE_CVXPY", "matrix": None, "solver_invoked": False}
    K = model["matrix_nodes"]
    X = cp.Variable((K, K), hermitian=True)
    constraints = [X >> 0, cp.diag(X) == 1]
    if model["difference_equalities"]:
        constraints.append(model["difference_operator"] @ cp.reshape(X, (K*K,), order="C") == 0)
    if "cyclic_fourier_operator" in model and model["cyclic_fourier_operator"].shape[0]:
        constraints.append(cp.real(model["cyclic_fourier_operator"] @ cp.reshape(X, (K*K,), order="C")) >= 0)
    objective = cp.real(cp.trace(model["objective_matrix"] @ X))/len(model["native_nodes"])
    problem = cp.Problem(cp.Maximize(objective), constraints)
    started = time.perf_counter()
    try:
        problem.solve(solver="SCS", eps=accuracy, max_iters=max_iterations, verbose=False)
    except cp.error.SolverError as error:
        return {"status": "SOLVER_ERROR", "error": str(error), "matrix": None,
                "solver_invoked": True, "elapsed_seconds": time.perf_counter()-started}
    matrix = None if X.value is None else np.asarray(X.value)
    audit = (audit_matrix(model, matrix) if matrix is not None
             else {"status": "NO_SOLVER_MATRIX", "numerically_feasible": False})
    return {"status": "SOLVED_NUMERICALLY" if audit["numerically_feasible"] else "UNCERTIFIED_SOLVER_OUTPUT",
            "solver_status": problem.status, "solver_invoked": True, "matrix": matrix,
            "elapsed_seconds": time.perf_counter()-started, "audit": audit,
            "solver_iterations": problem.solver_stats.num_iters, "cvxpy_version": cp.__version__,
            "max_iterations": max_iterations, "requested_accuracy": accuracy,
            "dual_optimality_or_integrality_gap_certified": False}


def phase_round(model, values):
    z = np.asarray(values, dtype=complex)
    if z.shape != (model["matrix_nodes"],) or not np.isfinite(z).all():
        raise ValueError("finite full phase-vector required")
    q = model["modulus"]
    gauge = np.angle(z[0])
    rounded = [int(math.floor(((np.angle(z[i])-gauge)/(2*np.pi) % 1)*q+.5)) % q
               for i in model["basis_nodes"]]
    return tuple(sum(int(a)*b for a, b in zip(row, rounded)) % q for row in model["basis_inverse"])


def rounded_proposals(model, matrix, gaussian_draws=12, seed=0):
    _positive(gaussian_draws, "Gaussian rounding draws", 0)
    _positive(seed, "rounding seed", 0)
    if not audit_matrix(model, matrix)["numerically_feasible"]:
        return {"status": "ROUNDING_REFUSED_INFEASIBLE_MATRIX", "proposals": (), "phase_vectors_tested": 0}
    X = np.asarray(matrix)
    eigenvalues, eigenvectors = np.linalg.eigh((X+X.conj().T)/2)
    root = eigenvectors*np.sqrt(np.maximum(eigenvalues, 0))
    rng = np.random.default_rng(seed)
    vectors = [X[:, 0], eigenvectors[:, -1]]
    for _ in range(gaussian_draws):
        vectors.append(root @ ((rng.standard_normal(len(X))+1j*rng.standard_normal(len(X)))/math.sqrt(2)))
    proposals = tuple(dict.fromkeys(phase_round(model, z) for z in vectors))
    return {"status": "SECRET_BLIND_PROPOSALS_ONLY", "proposals": proposals,
            "phase_vectors_tested": len(vectors), "Gaussian_draws": gaussian_draws,
            "clipped_negative_eigenvalues_only_for_proposal_generation": True,
            "rank_one_or_rounding_recovery_theorem": False}


def coordinate_refine(records, proposals, sweeps=2, max_root_values=4096):
    records, n, q = _records(records)
    _positive(sweeps, "coordinate sweeps", 0)
    _positive(max_root_values, "root-value enumeration cap")
    proposals = tuple(dict.fromkeys(tuple(x) for x in proposals))
    if not proposals or any(len(x) != n or any(type(a) is not int or not 0 <= a < q for a in x) for x in proposals):
        raise ValueError("nonempty canonical secret-blind proposals required")
    if q > max_root_values:
        return {"status": "ROOT_ENUMERATION_CAP_EXHAUSTED", "candidate": None,
                "all_root_values_required": q, "partial_coordinate_scan_used": False}
    if n*q*q >= 2**62:
        raise ValueError("integer dot products exceed the vectorized finite arithmetic scope")
    A = np.asarray([(r.first, r.second) for r in records], dtype=np.int64).reshape(-1, n)
    Y = np.asarray([r.outcome for r in records], dtype=np.int64)
    def scores_for(states):
        residuals = (Y[None, :, :]-np.asarray(states, dtype=np.int64).dot(A.T).reshape(len(states), -1, 2)) % q
        first, second = residuals[:, :, 0], residuals[:, :, 1]
        return (np.cos(2*np.pi*first/q)+np.cos(2*np.pi*second/q)
                +np.cos(2*np.pi*((first-second) % q)/q)).mean(axis=1)
    scored, evaluations = {}, 0
    for initial in proposals:
        trial = initial
        score = heldout_score(records, trial)
        evaluations += 1
        scored[trial] = score
        for _ in range(sweeps):
            changed = False
            for j in range(n):
                options = tuple(trial[:j]+(a,)+trial[j+1:] for a in range(q))
                scores = scores_for(options)
                evaluations += q
                best = max(range(q), key=lambda a: scores[a])
                if scores[best] > score+1e-10:
                    trial, score, changed = options[best], scores[best], True
                    scored[trial] = score
            if not changed:
                break
    candidate = max(sorted(scored), key=lambda x: scored[x])
    return {"status": "TRAINING_SELECTED_CANDIDATE", "candidate": candidate,
            "training_score": scored[candidate], "initial_proposals": proposals,
            "distinct_candidates_scored_or_retained": len(scored),
            "complete_score_evaluations": evaluations, "coordinate_sweeps": sweeps,
            "full_root_values_per_coordinate": q, "per_score_modular_work": 2*n*len(records),
            "runtime_polynomial_in_q_not_logq": True, "training_truth_or_holdout_used": False}


def baseline_proposals(records, count, seed):
    records, n, q = _records(records)
    _positive(count, "baseline starts")
    _positive(seed, "baseline seed", 0)
    validation = character_validator(records)
    states = [(0,)*n]
    if validation["rank_mod3"] == n:
        states.append(tuple(validation["basis_interpolated_secret_trial"]))
    rng = random.Random(seed)
    while len(states) < count:
        states.append(tuple(rng.randrange(q) for _ in range(n)))
    return tuple(states[:count])


def reference_maximum(records, max_secrets=2000):
    records, n, q = _records(records)
    _positive(max_secrets, "reference search cap", 0)
    if q**n > max_secrets:
        return {"status": "NOT_RUN_EXPONENTIAL_REFERENCE_CAP", "secret_states_required": q**n,
                "reference_used_by_decoder": False}
    score, trial = max((heldout_score(records, s), s) for s in product(range(q), repeat=n))
    return {"status": "CAPPED_EXHAUSTIVE_CALIBRATION", "best_score": score, "best_secret": trial,
            "score_evaluations": q**n, "reference_used_by_decoder": False,
            "exhaustive_reference_is_scaling_evidence": False}


def decode(records, original_ids, max_matrix_nodes=256, gaussian_draws=12, sweeps=2, seed=0,
           max_iterations=12000, stronger_baseline_starts=256):
    records, n, q = _records(records)
    ids = tuple(original_ids)
    if len(ids) != len(records) or len(set(ids)) != len(ids) or any(not isinstance(x, str) or not x for x in ids):
        raise ValueError("one distinct nonempty original ID per training input required")
    _positive(gaussian_draws, "Gaussian rounding draws", 0)
    _positive(seed, "rounding seed", 0)
    _positive(sweeps, "coordinate sweeps", 0)
    _positive(stronger_baseline_starts, "stronger classical baseline starts")
    model = compile_model(records, max_matrix_nodes=max_matrix_nodes)
    solved = solve_relaxation(model, max_iterations=max_iterations)
    initial = baseline_proposals(records, gaussian_draws+2, seed+1)
    baseline = coordinate_refine(records, initial, sweeps=sweeps)
    additional = baseline_proposals(records, stronger_baseline_starts, seed+2)
    stronger_initial = tuple(dict.fromkeys((*initial, *additional)))[:max(stronger_baseline_starts, len(set(initial)))]
    stronger = coordinate_refine(records, stronger_initial, sweeps=sweeps)
    if solved["status"] != "SOLVED_NUMERICALLY":
        return {"status": solved["status"], "candidate": None, "model": model, "solver": solved,
                "charged_training_qutrits": len(records), "original_ids": ids,
                "matched_nonSDP_baseline": baseline, "stronger_nonSDP_baseline": stronger,
                "failed_or_uncertified_attempt_retained": True}
    rounded = rounded_proposals(model, solved["matrix"], gaussian_draws=gaussian_draws, seed=seed)
    refined = coordinate_refine(records, rounded["proposals"], sweeps=sweeps)
    return {"status": "HEURISTIC_CANDIDATE_NOT_RECOVERY_THEOREM", "candidate": refined["candidate"],
            "model": model, "solver": solved, "rounding": rounded, "refinement": refined,
            "matched_nonSDP_baseline": baseline, "stronger_nonSDP_baseline": stronger,
            "charged_training_qutrits": len(records), "original_ids": ids,
            "same_quantum_produced_classical_records_for_both_decoders": True,
            "nonSDP_baseline_pays_no_SDP_cost": True, "efficient_population_recovery_proved": False}


def verify_fresh(records, candidate, original_ids, training_ids):
    records, n, q = _records(records)
    ids, old = tuple(original_ids), tuple(training_ids)
    if len(ids) != len(records) or len(set(ids)) != len(ids) or set(ids).intersection(old):
        raise ValueError("disjoint fresh held-out original IDs required")
    if any(not isinstance(x, str) or not x for x in (*ids, *old)):
        raise ValueError("nonempty original IDs required")
    candidate = tuple(candidate)
    if len(candidate) != n or any(type(x) is not int or not 0 <= x < q for x in candidate):
        raise ValueError("canonical candidate required")
    score = heldout_score(records, candidate)
    return {"candidate": candidate, "score": score, "threshold_passed": score >= .5,
            "gate": heldout_gate(len(records), 1), "fresh_original_ids": ids,
            "candidate_selected_before_holdout": True,
            "distinct_IDs_prove_physical_IID_supply": False, "speedup_claim_allowed": False}


def _public_decoding(result):
    public = dict(result)
    model = dict(public["model"])
    model.pop("difference_operator", None)
    model.pop("objective_matrix", None)
    model.pop("equalities", None)
    public["model"] = model
    solver = dict(public["solver"])
    X = solver.pop("matrix", None)
    if X is not None:
        solver["matrix_real"] = X.real.tolist()
        solver["matrix_imag"] = X.imag.tolist()
    public["solver"] = solver
    return public


def native_control(n, r, count, seed, max_matrix_nodes=256, heldout_count=256, max_iterations=12000):
    _positive(heldout_count, "held-out qutrit count")
    q = 3**r
    truth_rng = random.Random(seed+1)
    truth = tuple(truth_rng.randrange(q) for _ in range(n))
    batches, source_artifacts = [], []
    for size, source_seed, noise_seed in ((count, seed, seed+20), (heldout_count, seed+10, seed+21)):
        source = random_even_source(n, 2*r, size, source_seed)
        noise_rng = random.Random(noise_seed)
        records, proposals = [], 0
        for first, second in source.frequencies:
            record, draws = simulated_record(first, second, truth, q, noise_rng)
            records.append(record)
            proposals += draws
        batches.append(tuple(records))
        source_artifacts.append({"seed": source_seed, "original_level": 2*r,
                                 "original_ring_labels": source.labels, "simulator_noise_proposals": proposals})
    train, holdout = batches
    ids = tuple(f"sdp-{seed}-train-{i}" for i in range(count))
    hold_ids = tuple(f"sdp-{seed}-heldout-{i}" for i in range(heldout_count))
    result = decode(train, ids, max_matrix_nodes=max_matrix_nodes, seed=seed, max_iterations=max_iterations)
    output = {"dimension": n, "root_digits": r, "seed": seed, "training_records": [x.public() for x in train],
              "heldout_records": [x.public() for x in holdout], "original_source_batches": source_artifacts,
              "calibration_secret_NOT_decoder_input": truth, "decoder": _public_decoding(result),
              "independent_source_supply_is_an_assumption_not_PRNG_evidence": True,
              "charged_original_native_qutrits": count+heldout_count}
    for method, field in (("matched_nonSDP_baseline", "matched_baseline"), ("stronger_nonSDP_baseline", "stronger_baseline")):
        base = result[method]["candidate"]
        if base is not None:
            output[field+"_fresh_verification"] = verify_fresh(holdout, base, hold_ids, ids)
            output[field+"_calibration_recovery"] = base == truth
    if result["candidate"] is not None:
        output["fresh_verification"] = verify_fresh(holdout, result["candidate"], hold_ids, ids)
        output["calibration_recovery"] = result["candidate"] == truth
        output["baseline_calibration_recovery"] = output["matched_baseline_calibration_recovery"]
        ref = reference_maximum(train)
        output["reference_calibration"] = ref
        if ref["status"] == "CAPPED_EXHAUSTIVE_CALIBRATION":
            output["numerical_relaxation_minus_best_character_score"] = result["solver"]["audit"]["objective_score"]/count-ref["best_score"]
            output["integrality_gap_proved"] = False
    return output


def run_controls():
    configurations = ((2, 2, 32, 93011), (2, 2, 96, 93012), (3, 2, 48, 93013),
                      (3, 2, 96, 93014), (2, 3, 48, 93015), (4, 2, 96, 93016),
                      (5, 2, 32, 93017), (6, 2, 32, 93018))
    controls = [native_control(*x, max_matrix_nodes=384 if x[0] >= 5 else 256) for x in configurations]
    return {"status": "NATIVE_CHARACTER_SDP_DECODER_NUMERICAL_RESEARCH_ONLY",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_controls": controls, "algorithm_input_contains_truth": False,
            "accepted_candidate_or_speedup": False, "population_recovery_or_tightness_proved": False,
            "raw_failures_and_cap_exhaustions_retained": True,
            "exact_PSD_dual_or_integrality_gap_certificates_supplied": False,
            "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "controls": [{"n": x["dimension"], "r": x["root_digits"],
                                    "status": x["decoder"]["status"], "recovered": x.get("calibration_recovery"),
                                    "baseline_recovered": x.get("baseline_calibration_recovery"),
                                    "full_group_saturation": x["decoder"]["model"].get("full_group_saturation")}
                                   for x in report["native_controls"]]}, indent=2))


if __name__ == "__main__":
    main()
