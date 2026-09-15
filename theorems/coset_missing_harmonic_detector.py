"""Retained-data missing-sign detector with charged, gap-free amplification.

The span and pairwise trace identities are Moore/Russell's known construction.
We combine its first two moments with a randomized two-projector walk. This
gives a constant-bias *inefficient* detector without a least-positive-gap
assumption. It is not a new algorithmic speedup or an exact range compiler.
See research/MISSING_HARMONIC_DETECTOR.md for the derivation and scope.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations, dense_hidden_coset_state, inverse_permutation,
    involution_class_size, involution_conjugacy_class, right_regular_matrix,
    symmetric_group,
)
from research_registry import (
    ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result,
    upsert_negative_result, utc_now,
)


REPORT_PATH = Path("research/representation/coset_missing_harmonic_detector.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-MISSING-HARMONIC-DETECTOR"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SELECTOR_ONLY_SCOPE = (
    "raw_regular_null", "shared_hidden_missing_sign", "independent_initial_ancillas",
    "ancilla_only_interleavings", "selected_sign_phase_only_data_coupling",
    "ancilla_only_terminal_readout", "all_query_uses_charged", "no_free_postselection",
)


def _positive_integer(value: int, name: str) -> None:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def exact_fraction(value: Fraction) -> dict[str, str]:
    return {"numerator_hex": hex(value.numerator), "denominator_hex": hex(value.denominator)}


def frame_moments(order: int, weights: tuple[Fraction, ...]) -> tuple[Fraction, Fraction]:
    """Exact raw-null moments for distinct nonempty missing-SIGN subsets."""
    _positive_integer(order, "order")
    if order < 2 or not weights or any(type(w) not in (int, Fraction) or w < 0 for w in weights):
        raise ValueError("weights must be nonnegative exact rationals; order >=2")
    if sum(weights) != 1:
        raise ValueError("weights must sum to one")
    delta = Fraction(1, order)
    return delta, delta**2 + delta * (1 - delta) * sum(w**2 for w in weights)


def amplification_contract(order: int, copies: int) -> dict:
    """Uniform nonempty subsets, exact moment certificate, no dense allocation."""
    _positive_integer(order, "order")
    _positive_integer(copies, "copies")
    if order < 2:
        raise ValueError("order must be >=2")
    count = (1 << copies) - 1
    delta = Fraction(1, order)
    ratio = 1 + Fraction(order - 1, count)
    steps = math.isqrt(order)
    steps += steps * steps < order
    return {
        "group_order_hex": hex(order), "copy_count": copies,
        "nonempty_subset_count_hex": hex(count),
        "mean_eigenvalue": exact_fraction(delta),
        "second_moment": exact_fraction(delta**2 * ratio),
        "span_mass_lower_bound": exact_fraction(1 / ratio),
        "mass_above_half_mean_lower_bound": exact_fraction(1 / (4 * ratio)),
        "detector_null_acceptance_lower_bound": exact_fraction(1 / (32 * ratio)),
        "maximum_selected_projector_calls_hex": hex(steps),
        "constant_bias_certified": count >= order,
        "requires_smallest_positive_eigenvalue": False,
        "exact_support_projector_compiled": False,
        "polynomial_time_compiler": False,
    }


def grover_response(eigenvalues: np.ndarray, steps: int) -> np.ndarray:
    """Half direct test, half uniformly random t=0,...,steps-1 walk test."""
    _positive_integer(steps, "steps")
    values = np.asarray(eigenvalues, dtype=float)
    if not np.all(np.isfinite(values)) or np.any(values < -1e-10) or np.any(values > 1 + 1e-10):
        raise ValueError("eigenvalues must be in [0,1]")
    values = np.clip(values, 0, 1)
    # Summation is only for finite controls; the scaling contract is exact.
    if steps > 10000:
        raise ValueError("finite response budget exceeded; use amplification_contract")
    angles = np.arcsin(np.sqrt(values))
    random_response = sum(np.sin((2 * t + 1) * angles)**2 for t in range(steps)) / steps
    return (values + random_response) / 2


def schedule_null_upper_bound(order: int, steps: int) -> Fraction:
    _positive_integer(order, "order")
    _positive_integer(steps, "steps")
    return min(Fraction(1), Fraction(2 * steps**2 + 1, 3 * order))


def _sign(permutation: tuple[int, ...]) -> int:
    return (-1) ** sum(permutation[i] > permutation[j]
                       for i in range(len(permutation)) for j in range(i + 1, len(permutation)))


def _tensor(operators: list[np.ndarray]) -> np.ndarray:
    result = np.ones((1, 1))
    for operator in operators:
        result = np.kron(result, operator)
    return result


def finite_subset_projectors(n: int, copies: int) -> tuple[np.ndarray, np.ndarray]:
    """Independent group-algebra and relative-coordinate sign projectors.

    Dense matrices are calibration only, never the proposed implementation.
    The resource check precedes any permutation-group enumeration.
    """
    _positive_integer(n, "n")
    _positive_integer(copies, "copies")
    if n < 2 or n > 4 or copies > 4 or math.factorial(n)**copies > 600:
        raise ValueError("finite physical control budget exceeded")
    group = symmetric_group(n)
    order = len(group)
    basis = tuple(product(range(order), repeat=copies))
    indices = {g: i for i, g in enumerate(group)}
    signs = np.array([_sign(g) for g in group])
    sign_projector = np.outer(signs, signs) / order
    identity = np.eye(order)
    regular = [right_regular_matrix(n, g) for g in group]
    direct, relative = [], []
    for mask in range(1, 1 << copies):
        selected = [i for i in range(copies) if mask & (1 << i)]
        projector = sum(_sign(g) * _tensor([
            regular[gi] if i in selected else identity for i in range(copies)
        ]) for gi, g in enumerate(group)) / order
        direct.append(projector)
        pivot = selected[0]
        coordinate_map = []
        for row in basis:
            pivot_inverse = inverse_permutation(group[row[pivot]])
            transformed = [indices[compose_permutations(group[row[i]], pivot_inverse)]
                           if i in selected and i != pivot else row[i] for i in range(copies)]
            coordinate_map.append(sum(value * order**(copies - i - 1) for i, value in enumerate(transformed)))
        if len(set(coordinate_map)) != len(basis):
            raise ArithmeticError("relative-coordinate map is not reversible")
        pivot_projector = _tensor([sign_projector if i == pivot else identity for i in range(copies)])
        relative.append(pivot_projector[np.ix_(coordinate_map, coordinate_map)])
    return np.asarray(direct), np.asarray(relative)


def finite_control(n: int, transpositions: int, copies: int) -> dict:
    if type(transpositions) is not int or transpositions < 1 or 2 * transpositions > n:
        raise ValueError("invalid nonidentity involution cycle type")
    if transpositions % 2 != 1:
        raise ValueError("sign is not a missing harmonic for even transposition count")
    projectors, relative = finite_subset_projectors(n, copies)
    count, dimension, _ = projectors.shape
    order = math.factorial(n)
    delta, second = frame_moments(order, (Fraction(1, count),) * count)
    frame = projectors.mean(axis=0)
    eigenvalues = np.linalg.eigvalsh(frame)
    residuals = {
        "coordinate_projector": float(np.max(np.abs(projectors - relative))),
        "projector_idempotence": max(float(np.max(np.abs(p @ p - p))) for p in projectors),
        "projector_hermiticity": float(np.max(np.abs(projectors - projectors.transpose(0, 2, 1)))),
        "first_moment": abs(float(np.trace(frame) / dimension) - float(delta)),
        "second_moment": abs(float(np.sum(frame * frame.T) / dimension) - float(second)),
        "pairwise_trace": max((abs(float(np.sum(p * q.T) / dimension) - float(delta**2))
                               for i, p in enumerate(projectors) for q in projectors[i + 1:]), default=0.0),
    }
    residuals["individual_hidden_annihilation"] = max(
        float(np.max(np.abs(projectors @ dense_hidden_coset_state(n, h, copies))))
        for h in involution_conjugacy_class(n, transpositions)
    )
    steps = math.isqrt(order) + (math.isqrt(order)**2 < order)
    # E embeds ALL data vectors, not a chosen pure state. Two reflections
    # act on the subset ancilla and the retained data without resetting it.
    state = np.broadcast_to(np.eye(dimension) / math.sqrt(count), projectors.shape).copy()
    responses = []
    for _ in range(steps):
        projected = projectors @ state
        responses.append(float(np.sum(np.abs(projected)**2) / dimension))
        reflected = state - 2 * projected
        state = 2 * reflected.mean(axis=0, keepdims=True) - reflected
    expected = [float(np.mean(np.sin((2 * t + 1) * np.arcsin(np.sqrt(np.clip(eigenvalues, 0, 1))))**2))
                for t in range(steps)]
    residuals["physical_two_reflection_response"] = max(abs(a - b) for a, b in zip(responses, expected))
    acceptance = (responses[0] + sum(responses) / steps) / 2
    ratio = second / delta**2
    lower = float(1 / (32 * ratio))
    above = float(np.mean(eigenvalues >= float(delta / 2) - 1e-10))
    support = float(np.mean(eigenvalues > 1e-10))
    max_commutator = max((float(np.linalg.norm(p @ q - q @ p))
                          for i, p in enumerate(projectors) for q in projectors[i + 1:]), default=0.0)
    return {
        "n": n, "transposition_count": transpositions, "copy_count": copies,
        "physical_dimension": dimension, "subset_count": count,
        "pairwise_trace_control_count": count * (count - 1) // 2,
        "hidden_member_count": involution_class_size(n, transpositions),
        "residuals": residuals, "support_mass": support,
        "mass_above_half_mean": above, "null_acceptance": acceptance,
        "certified_null_acceptance_lower_bound": lower,
        "individual_subset_null_acceptance": float(delta),
        "max_subset_commutator_frobenius_norm": max_commutator,
        "walk_responses": responses,
        "verified": bool(max(residuals.values()) < 1e-9 and
                         support + 1e-9 >= float(1 / ratio) and
                         above + 1e-9 >= float(1 / (4 * ratio)) and acceptance + 1e-9 >= lower),
    }


def scaling_control(n: int) -> dict:
    _positive_integer(n, "n")
    if n < 6 or n % 4 != 2:
        raise ValueError("fixed-point-free missing sign requires n>=6 and n=2 mod 4")
    order = math.factorial(n)
    matching_count = involution_class_size(n, n // 2)
    copies = order.bit_length()  # smallest K with 2^K-1 >= order
    certificate = amplification_contract(order, copies)
    return {
        "n": n, "certificate": certificate,
        "log2_selected_projector_call_ceiling": math.log2(int(certificate["maximum_selected_projector_calls_hex"], 16)),
        "log2_coherent_oracle_matching_search_scale": math.log2(matching_count) / 2,
        "log2_classical_oracle_enumeration_scale": math.log2(matching_count),
        "polynomial_schedule_steps": n**2,
        "polynomial_schedule_null_acceptance_upper_bound": exact_fraction(schedule_null_upper_bound(order, n**2)),
        "dominance_comparison_same_access": "matching search only with coherent hiding-function access, NOT coset-only samples",
        "explicit_graph_baseline": "quasipolynomial classical GI; not a solver for an arbitrary opaque HSP oracle",
        "speedup_claim_allowed": False,
    }


def selector_only_query_contract(order: int, copies: int, queries: int, *, scope: dict) -> dict:
    """Check declared scope, not an arbitrary program; raw-null hybrid bound."""
    _positive_integer(order, "order")
    _positive_integer(copies, "copies")
    if order < 2 or type(queries) is not int or queries < 0:
        raise ValueError("order>=2 and a nonnegative integer query count required")
    issues = [key for key in SELECTOR_ONLY_SCOPE if scope.get(key) is not True]
    issues += [f"unknown scope key: {key}" for key in scope if key not in SELECTOR_ONLY_SCOPE]
    if issues:
        return {"applicable": False, "scope_issues": issues}
    bound = min(Fraction(1), Fraction(4 * queries**2, order))
    return {
        "applicable": True, "scope_issues": [], "copy_count": copies, "query_count": queries,
        "output_trace_distance_squared_upper_bound": exact_fraction(bound),
        "one_sided_null_acceptance_upper_bound": exact_fraction(bound),
        "one_sided_bound_requires_zero_ideal_alternative_acceptance": True,
        "arbitrary_program_scope_verified": False,
        "general_retained_data_circuit_lower_bound": False,
        "status": "derived-selector-only-query-hybrid-review-pending",
    }


def audit_selector_only_queries(n: int, copies: int, queries: int, *, seed: int = 71) -> dict:
    """Coherent-label and memory controls, including a forbidden-readout counterexample."""
    if type(queries) is not int or not 0 <= queries <= 8:
        raise ValueError("finite query budget is 0..8")
    ps, _ = finite_subset_projectors(n, copies)
    dimension = ps.shape[1]
    projectors = np.concatenate((np.zeros((1, dimension, dimension)), ps))
    ancilla_dimension = 2 * len(projectors)  # subset label and a coherent control bit
    rng = np.random.default_rng(seed)
    unitaries = [np.linalg.qr(rng.normal(size=(ancilla_dimension, ancilla_dimension)) +
                            1j * rng.normal(size=(ancilla_dimension, ancilla_dimension)))[0]
                 for _ in range(queries + 1)]
    phases = rng.uniform(-math.pi, math.pi, size=(queries, ancilla_dimension))
    phases[:, ::2] = 0  # Controlled calls; the empty subset is also inactive.
    coefficients = np.eye(ancilla_dimension, dtype=complex)[:, 0]
    null_root = np.eye(dimension) / math.sqrt(dimension)

    def evolve(root):
        state = coefficients[:, None, None] * root
        for j, unitary in enumerate(unitaries):
            state = np.einsum("ab,bij->aij", unitary, state, optimize=True)
            if j < queries:
                for a in range(1, ancilla_dimension, 2):
                    state[a] += (np.exp(1j * phases[j, a]) - 1) * (projectors[a // 2] @ state[a])
        return state

    # The norm estimate uses IDENTITY-query prefixes, not actual post-query
    # states. Their data register is still raw maximally mixed.
    baseline_coefficients = coefficients.copy()
    local_norms = []
    for j, unitary in enumerate(unitaries):
        baseline_coefficients = unitary @ baseline_coefficients
        if j < queries:
            squared_norm = sum(
                abs(baseline_coefficients[a] * (np.exp(1j * phases[j, a]) - 1))**2 *
                float(np.trace(projectors[a // 2])) / dimension
                for a in range(1, ancilla_dimension, 2)
            )
            local_norms.append(math.sqrt(squared_norm))
    null_state = evolve(null_root)
    baseline = baseline_coefficients[:, None, None] * null_root
    purified_difference = float(np.linalg.norm(null_state - baseline))
    reduced = null_state.reshape(ancilla_dimension, -1) @ null_state.reshape(ancilla_dimension, -1).conj().T
    baseline_reduced = np.outer(baseline_coefficients, baseline_coefficients.conj())
    trace_distance = float(np.sum(np.abs(np.linalg.eigvalsh(reduced - baseline_reduced))) / 2)
    one_sided = float(1 - np.vdot(baseline_coefficients, reduced @ baseline_coefficients).real)
    hidden_residual = max(float(np.linalg.norm(
        evolve(dense_hidden_coset_state(n, h, copies) * math.sqrt(dimension / 2**copies)) -
        baseline_coefficients[:, None, None] * dense_hidden_coset_state(n, h, copies) * math.sqrt(dimension / 2**copies)
    )) for h in involution_conjugacy_class(n, 1))
    # A free final DATA projector would violate the q=0 conclusion. Keep an
    # explicit counterexample to prevent broadening the theorem's scope.
    eigenvalues, eigenvectors = np.linalg.eigh(ps.mean(axis=0))
    span = eigenvectors[:, eigenvalues > 1e-10] @ eigenvectors[:, eigenvalues > 1e-10].conj().T
    terminal_data_null = float(np.trace(span) / dimension)
    terminal_data_hidden = max(abs(float(np.trace(span @ dense_hidden_coset_state(n, h, copies))))
                               for h in involution_conjugacy_class(n, 1))
    squared_bound = min(1, 4 * queries**2 / math.factorial(n))
    return {
        "n": n, "copy_count": copies, "query_count": queries,
        "coherent_ancilla_dimension": ancilla_dimension,
        "null_prefix_query_difference_norms": local_norms,
        "telescoped_purification_difference_norm": purified_difference,
        "ancilla_trace_distance": trace_distance,
        "one_sided_ancilla_acceptance": one_sided,
        "maximum_hidden_baseline_residual": hidden_residual,
        "forbidden_free_data_readout_null_acceptance": terminal_data_null,
        "forbidden_free_data_readout_hidden_acceptance": terminal_data_hidden,
        "verified": bool(
            max(local_norms, default=0) <= 2 / math.sqrt(math.factorial(n)) + 1e-9 and
            purified_difference <= sum(local_norms) + 1e-9 and
            trace_distance**2 <= squared_bound + 1e-9 and
            one_sided <= squared_bound + 1e-9 and hidden_residual < 1e-9 and
            terminal_data_null > 0 and terminal_data_hidden < 1e-9
        ),
    }


def build_missing_harmonic_report(*, finite_specs=((3, 1, 1), (3, 1, 2), (3, 1, 3), (4, 1, 2)),
                                  scaling_n_values=(6, 10, 18, 34, 66, 130, 258, 514, 1026),
                                  query_specs=((3, 3, 0), (3, 3, 1), (3, 3, 3), (4, 2, 1))) -> dict:
    from coset_missing_sign_source_adaptation import build_source_adaptive_audit
    source_adaptive = build_source_adaptive_audit(scaling_n_values=scaling_n_values)
    source_checked = source_adaptive["verified"]
    controls = [finite_control(*spec) for spec in finite_specs]
    scaling = [scaling_control(n) for n in scaling_n_values]
    checked = bool(controls and scaling and all(row["verified"] for row in controls))
    query_controls = [audit_selector_only_queries(*spec) for spec in query_specs]
    query_checked = bool(query_controls and all(row["verified"] for row in query_controls))
    return {
        "created_at": utc_now(),
        "primary_literature": [
            {"url": "https://arxiv.org/abs/quant-ph/0504067", "role": "known missing-harmonic span and pairwise trace identities"},
            {"url": "https://arxiv.org/abs/quant-ph/9605034", "role": "randomized Grover iteration precedent"},
            {"url": "https://arxiv.org/abs/quant-ph/0005055", "role": "amplitude amplification primitive"},
            {"url": "https://arxiv.org/abs/1512.03547", "role": "classical explicit-graph baseline"},
            {"url": "https://arxiv.org/abs/quant-ph/9701001", "role": "standard query-hybrid method, not a prior claim of this scoped application"},
        ],
        "theorem_contract": {
            "input": "K standard mixed coset states with the SAME hidden involution; retain all physical group data",
            "missing_harmonic": "sign, with odd transposition count; fixed-point-free scaling requires n=2 mod 4",
            "frame": "F=(2^K-1)^-1 sum_(S nonempty) Pi_sign^S, raw null I/(n!)^K",
            "moments": "E lambda=delta=1/n!, E lambda^2=delta^2[1+(n!-1)/(2^K-1)]",
            "detector": "Half direct selected projection, half t uniform in [0,ceil(sqrt(n!))-1] two-reflection iterations",
            "null_guarantee": "P(report trivial|null)>=1/{32[1+(n!-1)/(2^K-1)]}; >=1/64 when 2^K-1>=n!",
            "alternative_guarantee": "P(report trivial|h)=0 ideally for EVERY promised h, not just the class average",
            "primitive": "Coherently choose first selected pivot; compute x_i x_p^-1; reflect its uniform signed group state; uncompute",
            "cost": "O(poly(K,n,log(1/epsilon))*sqrt(n!)) gates, polynomial space; K states reused, not K fresh states per iteration",
            "precision": "O(T) primitive uses require operator error O(epsilon/T) each; poly(log T,log(1/epsilon)) synthesis overhead",
            "schedule_upper_bound": "For THIS mixed randomized schedule with T choices, raw-null acceptance <=min(1,(2T^2+1)/(3 n!))",
            "nonclaims": "No minimum-gap requirement for constant bias; no exact support compiler, general circuit lower bound, novelty, or speedup",
        },
        "finite_controls": controls, "scaling_records": scaling,
        "source_adaptive_query_audit": source_adaptive,
        "selector_only_query_controls": query_controls,
        "selector_only_query_derivation": {
            "scope": list(SELECTOR_ONLY_SCOPE),
            "argument": "Identity-query prefixes leave raw data maximally mixed, so each phase call changes a purification by <=2/sqrt(n!). Telescope q calls. Every hidden input is annihilated by all queried projectors, so its ancilla output equals the identity-query baseline.",
            "conclusion": "T(output_null,output_h)<=min(1,2q/sqrt(n!)); if acceptance is zero on the ideal alternative, null acceptance <=min(1,4q^2/n!).",
            "exclusions": "Arbitrary final data readout, data-dependent preprocessing/source labels, other data couplings and free postselection are not covered.",
            "asymptotic_scope": "Arbitrary K, arbitrary ancillary memory and coherent or deferred-classical ancilla control; no independence of successive actual queries is assumed.",
            "scaling_contracts": [{"n": n, **selector_only_query_contract(math.factorial(n), math.factorial(n).bit_length(), n**2,
                                   scope={key: True for key in SELECTOR_ONLY_SCOPE})} for n in scaling_n_values],
        },
        "headline_metrics": {
            "finite_control_count": len(controls),
            "finite_control_failure_count": sum(not row["verified"] for row in controls),
            "pairwise_trace_control_count": sum(row["pairwise_trace_control_count"] for row in controls),
            "physical_projector_control_count": sum(row["subset_count"] for row in controls),
            "scaling_record_count": len(scaling),
            "constant_bias_scaling_count": sum(row["certificate"]["constant_bias_certified"] for row in scaling),
            "polynomial_time_compiler_count": 0, "new_algorithm_count": 0,
            "selector_only_query_control_count": len(query_controls),
            "selector_only_query_control_failure_count": sum(not row["verified"] for row in query_controls),
            "source_adaptive_exact_sector_count": sum(row["conditional_sector_count"] for row in source_adaptive["censuses"]),
            "source_adaptive_regular_sector_count": sum(row["sector_comparison_count"] for row in source_adaptive["regular_controls"]),
            "source_adaptive_channel_control_count": len(source_adaptive["physical_controls"]),
            "source_adaptive_scaling_count": len(source_adaptive["scaling_records"]),
        },
        "claim_gate": {
            "finite_physical_controls_verified": checked and query_checked and source_checked,
            "gap_free_constant_bias_derivation_checked": checked,
            "costed_retained_data_schema_available": checked,
            "selector_only_query_hybrid_controls_verified": query_checked,
            "selector_only_query_hybrid_bound_derived": query_checked,
            "arbitrary_retained_data_query_lower_bound": False,
            "source_adaptive_rank_and_prior_controls_verified": bool(source_adaptive["censuses"] and source_adaptive["regular_controls"] and all(row["verified"] for row in source_adaptive["censuses"] + source_adaptive["regular_controls"])),
            "source_adaptive_channel_controls_verified": bool(source_adaptive["physical_controls"] and all(row["verified"] for row in source_adaptive["physical_controls"])),
            "source_adaptive_query_bound_derived": source_checked,
            "independently_reviewed": False, "formally_verified": False,
            "novelty_established": False, "exact_support_projector_compiled": False,
            "polynomial_time_compiler_constructed": False, "speedup_claim_allowed": False,
        },
        "status": "derived-review-pending-gap-free-detector-generic-cost-uncompetitive" if checked and query_checked and source_checked else "control-failure",
        "summary": "Retained-data missing-sign detector has constant bias without a minimum positive gap, but costs sqrt(n!) selected reflections. This is a costed benchmark, not a speedup.",
        "source_adaptive_research_update": (
            "Source-adaptive extension derived/review-pending: T<=K/(2sqrt(M))+2q sqrt(K p(n)/n!). Central source labels do not rescue polynomial missing-sign query schedules; other carrier operations remain open."
            if source_checked else "Source-adaptive extension: controls incomplete or failed; no bound promoted."
        ),
        "falsifiers_triggered": [
            "A least-positive frame gap is not necessary for this constant-bias detector.",
            "Polynomially many iterations of this normalized walk cannot give constant raw-null acceptance asymptotically.",
            "Coherent hiding-function matching search is asymptotically cheaper; it is unavailable from coset samples alone.",
            "Explicit graph inputs have a quasipolynomial classical baseline; generic sqrt(n!) amplification is not competitive.",
        ] if checked else [],
        "next_experiments": [
            "Seek a structured selected-projector span compiler bypassing normalized amplitude amplification, with a physical circuit and natural input reduction.",
            "Source-conditioned missing-sign queries now have a scoped bound including weak-source information. Seek different charged carrier operations, not further optimization of that subset schedule.",
            "Compare any retained-data compiler with matching search under coherent oracle access and classical GI under explicit graph access before promotion.",
        ],
    }


def write_missing_harmonic_report(output_path: Path = REPORT_PATH, *, write_registry: bool = True,
                                  registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
                                  registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
                                  registry_result_id: str | None = None, **kwargs) -> dict:
    payload = build_missing_harmonic_report(**kwargs)
    payload["artifacts"] = {"report": str(output_path)}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_experiment_result(ExperimentResultRecord(
            id=registry_result_id or f"RESULT-{registry_experiment_id}-COSET",
            experiment_id=registry_experiment_id, candidate_id=registry_candidate_id,
            created_at=payload["created_at"], status=payload["status"], summary=payload["summary"],
            metrics=payload["headline_metrics"], falsifiers_triggered=payload["falsifiers_triggered"],
            artifacts=payload["artifacts"],
        ))
        if payload["claim_gate"]["gap_free_constant_bias_derivation_checked"]:
            upsert_negative_result(NegativeResultRecord(
                id="MISSING-SIGN-GENERIC-AMPLIFICATION-COST",
                source=str(output_path),
                claim="Constant-bias missing-harmonic detection becomes efficient once the minimum positive gap obligation is removed.",
                reason_invalid="The costed two-reflection detector removes that obligation but still uses sqrt(n!) selected projections; its polynomial-iteration acceptance is at most (2T^2+1)/(3n!).",
                lesson="Separate exact support from constant bias and absolute normalization from a spectral gap. This only obstructs the stated schedule, not arbitrary retained-data circuits.",
                applies_to=[registry_candidate_id], evidence={"metrics": payload["headline_metrics"], "review_status": "derived-review-pending"},
            ))
        if payload["claim_gate"]["selector_only_query_hybrid_bound_derived"]:
            upsert_negative_result(NegativeResultRecord(
                id="MISSING-SIGN-SELECTOR-ONLY-QUERY-BOUND", source=str(output_path),
                claim="Changing ancilla schedules or adding coherent selector memory yields a short missing-sign detector without other data operations.",
                reason_invalid="With only selected missing-sign phase calls as data coupling and ancilla-only readout, the raw-null identity-prefix hybrid gives output T<=2q/sqrt(n!) for arbitrary K. One-sided acceptance is <=4q^2/n!.",
                lesson="A faster retained-data compiler must leave this restricted access architecture. Data-dependent preprocessing, nonmissing-sector operations and terminal data measurements are excluded, not lower-bounded; each needs an explicit charged implementation.",
                applies_to=[registry_candidate_id], evidence={"metrics": payload["headline_metrics"], "scope": list(SELECTOR_ONLY_SCOPE), "review_status": "derived-review-pending"},
            ))
        if payload["claim_gate"]["source_adaptive_query_bound_derived"]:
            upsert_negative_result(NegativeResultRecord(
                id="MISSING-SIGN-SOURCE-ADAPTIVE-QUERY-BOUND", source=str(output_path),
                claim="At polynomial copy count, choosing missing-sign subset phase queries from full observed source labels gives a polynomial-query detector with no other carrier operations.",
                reason_invalid="The Plancherel mean of the best conditional sign-sector rank fraction is at most K p(n)/n!. Including weak-source information gives output T<=K/(2sqrt(M))+2q sqrt(K p(n)/n!), negligible at polynomial K,q for fixed-point-free n=2 mod 4.",
                lesson="Source information is not zero at q=0. This extends only central-source/ancilla-controlled missing-sign queries and source/ancilla readout; noncentral carrier operations, different target sectors and implemented data POVMs remain outside the bound.",
                applies_to=[registry_candidate_id], evidence={"metrics": payload["headline_metrics"], "scope": payload["source_adaptive_query_audit"]["scope"], "review_status": "derived-review-pending"},
            ))
    return payload
