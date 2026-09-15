"""Source-adaptive missing-sign queries: exact ranks and physical controls.

Frobenius reciprocity gives r_S(lambda)<=1/d_j^2 for every j in S.
Plancherel averaging bounds E max_S r_S by K p(n)/n!. A null-prefix
hybrid then charges queries, separately from the differing source priors.
The derivation is review-pending, not a general circuit lower bound.
"""

from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache
from itertools import product

import numpy as np
from sympy.functions.combinatorial.numbers import partition as partition_count

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size, involution_conjugacy_class, right_regular_matrix, symmetric_group,
)
from coset_hidden_involution_multiplicity_support_obstruction import permutation_cycle_type
from coset_missing_harmonic_detector import _positive_integer, _sign, _tensor, exact_fraction, finite_subset_projectors
from isotypic_instruments import _sqrt_ratio_dyadic_exponent
from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_physical_frame_blocks import permutation_representation_matrices
from symmetric_character import conjugacy_class_size, symmetric_character


SOURCE_ADAPTIVE_SCOPE = (
    "standard_mixed_coset_inputs", "shared_hidden_odd_involution_class",
    "full_central_irrep_source_labels", "initial_ancillas_depend_only_on_source_labels",
    "source_conditioned_ancilla_only_interleavings", "selected_sign_phase_only_further_data_coupling",
    "source_and_ancilla_only_terminal_readout", "all_query_uses_charged", "no_free_postselection",
)


def source_adaptive_query_contract(n: int, transpositions: int, copies: int, queries: int, *, scope: dict) -> dict:
    for value, name in ((n, "n"), (transpositions, "transpositions"), (copies, "copies")):
        _positive_integer(value, name)
    if n < 2 or transpositions % 2 != 1 or 2 * transpositions > n:
        raise ValueError("a valid odd-transposition involution class is required")
    if type(queries) is not int or queries < 0:
        raise ValueError("queries must be a nonnegative integer")
    issues = [key for key in SOURCE_ADAPTIVE_SCOPE if scope.get(key) is not True]
    issues += [f"unknown scope key: {key}" for key in scope if key not in SOURCE_ADAPTIVE_SCOPE]
    if issues:
        return {"applicable": False, "scope_issues": issues}
    order = math.factorial(n)
    classes = int(partition_count(n))
    hidden_count = involution_class_size(n, transpositions)
    marked = min(Fraction(1), Fraction(copies * classes, order))
    source_squared = min(Fraction(1), Fraction(copies**2, 4 * hidden_count))
    query_squared = min(Fraction(1), 4 * queries**2 * marked)
    # (sqrt(a)+sqrt(b))^2 <= 2(a+b); at q=0 keep the sharper source term.
    squared = min(Fraction(1), 2 * (source_squared + query_squared)) if queries else source_squared
    return {
        "applicable": True, "scope_issues": [], "n": n, "transposition_count": transpositions,
        "copy_count": copies, "query_count": queries, "group_class_count": classes,
        "mean_best_subset_marked_mass_upper_bound": exact_fraction(marked),
        "source_prior_tv_squared_upper_bound": exact_fraction(source_squared),
        "query_hybrid_distance_squared_upper_bound": exact_fraction(query_squared),
        "output_trace_distance_squared_upper_bound": exact_fraction(squared),
        "output_trace_distance_upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent(squared.numerator, squared.denominator),
        "source_information_retained_at_zero_queries": True,
        "one_sided_query_only_bound_available": False,
        "arbitrary_program_scope_verified": False, "general_circuit_lower_bound": False,
        "status": "derived-source-adaptive-missing-sign-bound-review-pending",
    }


@lru_cache(maxsize=8)
def _characters(n: int):
    if type(n) is not int or not 2 <= n <= 8:
        raise ValueError("finite character census supports 2<=n<=8")
    labels = tuple(integer_partitions(n))
    dimensions = tuple(hook_length_dimension(lam) for lam in labels)
    table = tuple(tuple(symmetric_character(lam, cycle) for cycle in labels) for lam in labels)
    sizes = tuple(conjugacy_class_size(cycle) for cycle in labels)
    signs = tuple((-1)**(n - len(cycle)) for cycle in labels)
    return labels, dimensions, table, sizes, signs


def _rank_fraction(n: int, sources: tuple[int, ...]) -> Fraction:
    _, dimensions, table, sizes, signs = _characters(n)
    numerator = sum(size * sign * math.prod(table[i][c] for i in sources)
                    for c, (size, sign) in enumerate(zip(sizes, signs)))
    multiplicity = Fraction(numerator, math.factorial(n))
    if multiplicity.denominator != 1 or multiplicity < 0:
        raise ArithmeticError("sign multiplicity is not a nonnegative integer")
    return multiplicity / math.prod(dimensions[i] for i in sources)


def exact_source_census(n: int, transpositions: int, copies: int) -> dict:
    _positive_integer(transpositions, "transpositions")
    _positive_integer(copies, "copies")
    if copies > 6:
        raise ValueError("finite census budget exceeded")
    labels, dimensions, _, _, _ = _characters(n)
    if len(labels)**copies * ((1 << copies) - 1) > 50000:
        raise ValueError("finite census budget exceeded")
    order = math.factorial(n)
    hidden_count = involution_class_size(n, transpositions)
    cycle = (2,) * transpositions + (1,) * (n - 2 * transpositions)
    characters = tuple(symmetric_character(lam, cycle) for lam in labels)
    p = tuple(Fraction(d*d, order) for d in dimensions)
    q = tuple(Fraction(d*(d+c), order) for d, c in zip(dimensions, characters))
    if sum(p) != 1 or sum(q) != 1 or min(q) < 0:
        raise ArithmeticError("source priors are not normalized probability laws")
    inverse_dimension_mean = sum(weight / d**2 for weight, d in zip(p, dimensions))
    score_second = sum(weight * Fraction(c, d)**2 for weight, c, d in zip(p, characters, dimensions))
    if inverse_dimension_mean != Fraction(len(labels), order) or score_second != Fraction(1, hidden_count):
        raise ArithmeticError("source dimension or character-square identity failed")
    mean_best = Fraction(0)
    source_tv = Fraction(0)
    sectors = 0
    for sources in product(range(len(labels)), repeat=copies):
        probabilities = []
        for mask in range(1, 1 << copies):
            chosen = tuple(sources[i] for i in range(copies) if mask >> i & 1)
            value = _rank_fraction(n, chosen)
            if value > min(Fraction(1, dimensions[i]**2) for i in chosen):
                raise ArithmeticError("conditional sign rank exceeded the dimension bound")
            probabilities.append(value)
            sectors += 1
        p_row = math.prod(p[i] for i in sources)
        q_row = math.prod(q[i] for i in sources)
        mean_best += p_row * max(probabilities)
        source_tv += abs(p_row - q_row) / 2
    cap = min(Fraction(1), copies * inverse_dimension_mean)
    if mean_best > cap or source_tv**2 > Fraction(copies**2, 4 * hidden_count):
        raise ArithmeticError("averaged source certificate failed")
    return {"n": n, "transposition_count": transpositions, "copy_count": copies,
            "source_tuple_count": len(labels)**copies, "conditional_sector_count": sectors,
            "mean_best_subset_probability": exact_fraction(mean_best), "dimension_cap": exact_fraction(cap),
            "source_prior_tv": exact_fraction(source_tv), "inverse_dimension_mean": exact_fraction(inverse_dimension_mean),
            "source_score_second_moment": exact_fraction(score_second), "verified": True}


def regular_source_rank_control(n: int, copies: int) -> dict:
    if copies > 2:
        raise ValueError("regular source comparison limited to two copies")
    subset_projectors, _ = finite_subset_projectors(n, copies)
    group = symmetric_group(n)
    order = len(group)
    labels, dimensions, _, _, _ = _characters(n)
    regular = [right_regular_matrix(n, g) for g in group]
    central = [sum(symmetric_character(lam, permutation_cycle_type(g)) * matrix
                   for g, matrix in zip(group, regular)) * d / order
               for lam, d in zip(labels, dimensions)]
    residual = 0.0
    prior_residual = 0.0
    prior_checks = 0
    for lam, d, projector in zip(labels, dimensions, central):
        prior_residual = max(prior_residual, abs(float(np.trace(projector)/order)-d*d/order))
        for h in involution_conjugacy_class(n, 1):
            observed = float(np.trace(projector @ (np.eye(order)+right_regular_matrix(n, h)))/order)
            predicted = d*(d+symmetric_character(lam, permutation_cycle_type(h)))/order
            prior_residual = max(prior_residual, abs(observed-predicted))
            prior_checks += 1
    count = 0
    for sources in product(range(len(labels)), repeat=copies):
        projector = _tensor([central[i] for i in sources])
        rank = math.prod(dimensions[i]**2 for i in sources)
        for mask, target in enumerate(subset_projectors, 1):
            observed = float(np.sum(projector * target.T) / rank)
            predicted = _rank_fraction(n, tuple(sources[i] for i in range(copies) if mask >> i & 1))
            residual = max(residual, abs(observed - float(predicted)))
            count += 1
    return {"n": n, "copy_count": copies, "sector_comparison_count": count,
            "maximum_rank_residual": residual, "maximum_source_prior_residual": prior_residual,
            "per_hidden_source_prior_check_count": prior_checks,
            "verified": max(residual, prior_residual) < 1e-9}


def physical_source_adaptive_control(n: int, transpositions: int, copies: int, queries: int, *, seed: int = 817) -> dict:
    if (n, copies) not in ((3, 2), (3, 3), (4, 2)) or type(queries) is not int or not 0 <= queries <= 3:
        raise ValueError("declared physical adaptive controls are S3 K2/3 or S4 K2, 0..3 queries")
    contract = source_adaptive_query_contract(n, transpositions, copies, queries,
                                              scope={key: True for key in SOURCE_ADAPTIVE_SCOPE})
    labels, dimensions, _, _, _ = _characters(n)
    group = symmetric_group(n)
    hidden = involution_conjugacy_class(n, transpositions)
    order = len(group)
    representations = [dict(permutation_representation_matrices(lam)) for lam in labels]
    hidden_chars = [symmetric_character(lam, permutation_cycle_type(hidden[0])) for lam in labels]
    p = [Fraction(d*d, order) for d in dimensions]
    q = [Fraction(d*(d+c), order) for d, c in zip(dimensions, hidden_chars)]
    ancilla_dimension = 2 * (1 << copies)
    distances = np.zeros(len(hidden))
    prefix_squared_norms = np.zeros(queries)
    null_baseline_distance = 0.0
    prior_tv = Fraction(0)
    mean_best = 0.0
    max_rank_residual = 0.0
    max_hidden_residual = 0.0
    max_projector_residual = 0.0
    max_state_normalization_residual = 0.0
    for ordinal, sources in enumerate(product(range(len(labels)), repeat=copies)):
        dimension = math.prod(dimensions[i] for i in sources)
        p_row = math.prod(p[i] for i in sources)
        q_row = math.prod(q[i] for i in sources)
        prior_tv += abs(p_row-q_row) / 2
        projectors = [np.zeros((dimension, dimension))]
        probabilities = [Fraction(0)]
        for mask in range(1, 1 << copies):
            projector = sum(_sign(g) * _tensor([
                representations[sources[i]][g] if mask >> i & 1 else np.eye(dimensions[sources[i]])
                for i in range(copies)]) for g in group) / order
            projectors.append(projector)
            rank = _rank_fraction(n, tuple(sources[i] for i in range(copies) if mask >> i & 1))
            probabilities.append(rank)
            max_rank_residual = max(max_rank_residual, abs(float(np.trace(projector)/dimension)-float(rank)))
            max_projector_residual = max(max_projector_residual, float(np.max(np.abs(projector @ projector-projector))))
        best = max(range(1, len(projectors)), key=lambda i: probabilities[i])
        mean_best += float(p_row * probabilities[best])
        coefficients = np.zeros(ancilla_dimension, dtype=complex)
        coefficients[2*best:2*best+2] = 1/math.sqrt(2)
        rng = np.random.default_rng(seed + ordinal)
        unitaries = [np.eye(ancilla_dimension)] + [np.linalg.qr(
            rng.normal(size=(ancilla_dimension, ancilla_dimension)) +
            1j*rng.normal(size=(ancilla_dimension, ancilla_dimension)))[0] for _ in range(queries)]
        phases = rng.uniform(-math.pi, math.pi, size=(queries, ancilla_dimension))
        if queries:
            phases[0, :] = math.pi  # Adversarially query the best source-dependent subset first.

        def evolve(root):
            state = coefficients[:, None, None] * root
            for j, unitary in enumerate(unitaries):
                state = np.einsum("ab,bij->aij", unitary, state, optimize=True)
                if j < queries:
                    for a in range(1, ancilla_dimension, 2):
                        state[a] += (np.exp(1j*phases[j, a])-1) * (projectors[a//2] @ state[a])
            vectors = state.reshape(ancilla_dimension, -1)
            return state, vectors @ vectors.conj().T

        baseline_coefficients = coefficients.copy()
        for j, unitary in enumerate(unitaries):
            baseline_coefficients = unitary @ baseline_coefficients
            if j < queries:
                prefix_squared_norms[j] += float(p_row) * sum(
                    abs(baseline_coefficients[a] * (np.exp(1j*phases[j, a])-1))**2 * float(probabilities[a//2])
                    for a in range(1, ancilla_dimension, 2))
        baseline_reduced = np.outer(baseline_coefficients, baseline_coefficients.conj())
        _, null_reduced = evolve(np.eye(dimension)/math.sqrt(dimension))
        max_state_normalization_residual = max(max_state_normalization_residual, abs(float(np.trace(null_reduced).real)-1))
        null_baseline_distance += float(p_row)*float(np.abs(np.linalg.eigvalsh(null_reduced-baseline_reduced)).sum()/2)
        for hi, h in enumerate(hidden):
            alternative_reduced = np.zeros_like(null_reduced)
            if q_row:
                root = _tensor([(np.eye(dimensions[i])+representations[i][h]) /
                                math.sqrt(2*(dimensions[i]+hidden_chars[i])) for i in sources])
                state, alternative_reduced = evolve(root)
                max_hidden_residual = max(max_hidden_residual, float(np.linalg.norm(
                    state - baseline_coefficients[:, None, None]*root)))
                max_state_normalization_residual = max(max_state_normalization_residual, abs(float(np.trace(alternative_reduced).real)-1))
            distances[hi] += float(np.abs(np.linalg.eigvalsh(float(p_row)*null_reduced-float(q_row)*alternative_reduced)).sum()/2)
    marked_cap = min(1, copies*len(labels)/order)
    hybrid_cap = 2*queries*math.sqrt(marked_cap)
    total_cap = min(1, copies/(2*math.sqrt(len(hidden))) + hybrid_cap)
    verified = bool(max(max_rank_residual, max_hidden_residual, max_projector_residual, max_state_normalization_residual) < 1e-9 and
                    mean_best <= marked_cap+1e-9 and max(prefix_squared_norms, default=0) <= 4*marked_cap+1e-9 and
                    null_baseline_distance <= hybrid_cap+1e-9 and max(distances) <= total_cap+1e-9 and
                    null_baseline_distance <= sum(math.sqrt(value) for value in prefix_squared_norms)+1e-9 and
                    min(distances) >= float(prior_tv)-1e-9 and
                    max(distances) <= float(prior_tv) + null_baseline_distance + 1e-9 and
                    (queries != 0 or np.max(np.abs(distances-float(prior_tv))) < 1e-9))
    return {"n": n, "transposition_count": transpositions, "copy_count": copies, "query_count": queries,
            "source_tuple_count": len(labels)**copies, "hidden_member_count": len(hidden),
            "exact_source_prior_tv": exact_fraction(prior_tv), "mean_best_subset_probability": mean_best,
            "classical_postprocessing_of_weak_labels_bayes_success": float((1+prior_tv)/2),
            "optimal_uncompiled_ancilla_readout_bayes_success_per_hidden": ((1+distances)/2).tolist(),
            "finite_information_gain_over_weak_labels": (distances-float(prior_tv)).tolist(),
            "classical_baseline_includes_quantum_weak_label_frontend": True,
            "optimal_ancilla_readout_compiler_supplied": False,
            "prefix_difference_norms_squared": prefix_squared_norms.tolist(),
            "null_to_identity_query_ancilla_distance": null_baseline_distance,
            "per_hidden_full_output_trace_distances": distances.tolist(),
            "max_rank_residual": max_rank_residual, "max_hidden_baseline_residual": max_hidden_residual,
            "max_projector_residual": max_projector_residual, "max_state_normalization_residual": max_state_normalization_residual,
            "contract": contract, "verified": verified}


def build_source_adaptive_audit(*, census_specs=((3, 1, 3), (4, 1, 2), (4, 1, 3), (6, 3, 2)),
                                physical_specs=((3, 1, 2, 0), (3, 1, 3, 2), (4, 1, 2, 1)),
                                regular_specs=((3, 2), (4, 2)), scaling_n_values=(6, 10, 18, 34, 66, 130, 258, 514, 1026)) -> dict:
    censuses = [exact_source_census(*spec) for spec in census_specs]
    physical = [physical_source_adaptive_control(*spec) for spec in physical_specs]
    regular = [regular_source_rank_control(*spec) for spec in regular_specs]
    scaling = [source_adaptive_query_contract(n, n//2, n*n, n*n, scope={key: True for key in SOURCE_ADAPTIVE_SCOPE}) for n in scaling_n_values]
    return {
        "censuses": censuses, "physical_controls": physical, "regular_controls": regular, "scaling_records": scaling,
        "verified": bool(censuses and physical and regular and scaling and all(row["verified"] for row in censuses+physical+regular)),
        "derivation": "Frobenius reciprocity gives r_S<=1/d_j^2. E_Planch max_S r_S<=K p(n)/n!. The identity-prefix hybrid costs <=2q sqrt(K p(n)/n!), separately from source TV<=K/(2sqrt(M)).",
        "scope": list(SOURCE_ADAPTIVE_SCOPE), "independent_review": False, "formal_verification": False,
        "novelty_established": False, "speedup_claim_allowed": False,
    }
