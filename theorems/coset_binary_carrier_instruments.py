"""Source-weighted binary evaluation of existing collective carrier instruments.

This evaluates physical outcome laws, not commutator size. It deliberately
does not search tiny circuits or promote a fixed-copy detection algorithm.
The finite schedules calibrate the evaluator; all fixed-copy candidates must
still pass the asymptotic copy budget, classifier, and classical baseline gates.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np

from isotypic_instruments import (
    finite_isotypic_instrument, isotypic_label_resource_contract, fixed_palette_information_contract,
    regular_algebra_state_lift, source_conditioned_palette_information_contract,
    adaptive_palette_catalogue_information_contract,
    coherent_subset_phase_resource_contract, unlabeled_coherent_selector_information_contract,
    low_order_coherent_selector_information_contract,
    coherent_parity_information_contract,
)
from involution_character_arithmetic import label_arithmetic_scaling_controls

from coset_three_copy_recoupling_obstruction import involutions
from coset_hidden_involution_reference_twirl_information import matching_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_carrier_noncentral_readout_boundary import _natural_informative_block
from self_dual_wreath_physical_frame_blocks import permutation_representation_matrices
from self_dual_wreath_plancherel_carrier_contextuality import _triple_isotypic_projectors
from weak_fourier_signal import character_on_involution

REPORT_PATH = Path("research/representation/coset_binary_carrier_instruments.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-BINARY-CARRIER-INSTRUMENTS"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SCHEDULES = ("", "L", "R", "LL", "LR", "RL", "LRL", "RLR", "T", "LT", "RT", "TL")


def binary_outcome_statistics(null: np.ndarray, alternative: np.ndarray) -> dict:
    """No silent clipping, normalization, postselection or omitted outcomes."""
    if any(np.iscomplexobj(values) and np.any(np.abs(np.asarray(values).imag) > 1e-12) for values in (null, alternative)):
        raise ValueError("probabilities must be real")
    null, alternative = np.asarray(null, dtype=float), np.asarray(alternative, dtype=float)
    if null.ndim != 1 or null.shape != alternative.shape or not null.size:
        raise ValueError("binary laws must be equal-length nonempty vectors")
    if not np.isfinite(null).all() or not np.isfinite(alternative).all():
        raise ValueError("binary laws contain nonfinite probabilities")
    if min(float(null.min()), float(alternative.min())) < -1e-10:
        raise ValueError("binary laws contain negative probabilities")
    residual = max(abs(float(null.sum()) - 1), abs(float(alternative.sum()) - 1))
    if residual > 1e-8:
        raise ValueError(f"binary law mass lost or renormalized before evaluation: residual={residual}")
    distance = float(np.abs(alternative - null).sum()) / 2
    return {"total_variation": distance, "equal_prior_bayes_success": (1 + distance) / 2,
            "normalization_residual": residual, "output_count": len(null),
            "optimal_likelihood_table_is_a_compiled_classifier": False}


def one_pair_likelihood_ratio(sources: tuple, target: tuple[int, ...], transposition_count: int, side: str) -> Fraction:
    """Exact ratio for source labels plus ONE pair label, on positive null mass.

    Pair-label quantum access and character evaluation are separate resource
    contracts. Repeated overlapping measurements do not inherit this formula.
    """
    if len(sources) != 3 or side not in ("L", "R"):
        raise ValueError("one left/right pair on three sources required")
    degree = sum(sources[0])
    labels = (*sources, target)
    if (any(not isinstance(label, tuple) or sum(label) != degree
            or any(type(part) is not int or part < 1 for part in label)
            or any(a < b for a, b in zip(label, label[1:])) for label in labels)
            or type(transposition_count) is not int
            or not 1 <= transposition_count <= degree // 2):
        raise ValueError("incompatible source, target or involution class")
    ratios = [Fraction(character_on_involution(source, transposition_count), hook_length_dimension(source)) for source in sources]
    target_ratio = Fraction(character_on_involution(target, transposition_count), hook_length_dimension(target))
    left, right, unused = (0, 1, 2) if side == "L" else (1, 2, 0)
    return (1 + ratios[unused]) * (1 + ratios[left] + ratios[right] + target_ratio)


def invariant_block_transcript_distance_squared_bound(half_degree: int, block_size: int, blocks: int) -> Fraction:
    """Only fresh-block invariant measurements with CLASSICAL retained history.

    Each complete block POVM commutes with diagonal G. No quantum state is
    retained between blocks. Outcome-adaptive instrument choices are allowed.
    Since every transcript is independent of which h in the class was chosen,
    the conditional hidden prior remains uniform. Relative-entropy chain rule
    and Pinsker yield T^2 <= t(2^b-1)/(2M).
    """
    if type(block_size) is not int or block_size < 1 or type(blocks) is not int or blocks < 0:
        raise ValueError("positive block size and nonnegative block count required")
    return min(Fraction(1), Fraction(blocks * (2**block_size - 1), 2 * matching_count(half_degree)))


def _half_trace_norm(matrix: np.ndarray) -> float:
    return float(np.abs(np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)).sum()) / 2


@lru_cache(maxsize=3)
def audit_regular_cell_compression(n: int, transposition_count: int, width: int) -> dict:
    """Independent regular-basis check, not source-conditioned Fourier blocks."""
    from coset_hidden_involution_binary_decision_reduction import (
        symmetric_group, inverse_permutation, compose_permutations, right_regular_matrix,
    )
    if (n, transposition_count, width) not in ((3, 1, 2), (3, 1, 3), (4, 2, 2)):
        raise ValueError("dense compression controls are limited to the declared small regular registers")
    group = symmetric_group(n)
    order, identity = len(group), tuple(range(n))
    group_index = {g: i for i, g in enumerate(group)}
    tuples = tuple(itertools.product(group, repeat=width))
    inverse_order = []
    for values in tuples:
        inv = inverse_permutation(values[0])
        encoded = (values[0], *(compose_permutations(value, inv) for value in values[1:]))
        index = 0
        for value in encoded:
            index = index * order + group_index[value]
        inverse_order.append(index)
    inverse_order = np.argsort(inverse_order)
    environment = order**(width - 1)
    marginal_residual = action_residual = 0.0
    for hidden in (identity, *involutions(n, transposition_count)):
        single = np.eye(order) / order
        if hidden != identity:
            single += right_regular_matrix(n, hidden) / order
        full = single
        for _ in range(width - 1):
            full = np.kron(full, single)
        transformed = full[np.ix_(inverse_order, inverse_order)].reshape(order, environment, order, environment)
        marginal = np.trace(transformed, axis1=1, axis2=3)
        marginal_residual = max(marginal_residual, float(np.linalg.norm(marginal - single)))
    for g in group:
        single = right_regular_matrix(n, g)
        diagonal = single
        for _ in range(width - 1):
            diagonal = np.kron(diagonal, single)
        encoded = diagonal[np.ix_(inverse_order, inverse_order)]
        action_residual = max(action_residual, float(np.linalg.norm(encoded - np.kron(single, np.eye(environment)))))
    return {"degree": n, "cell_width": width, "class_size": len(involutions(n, transposition_count)),
            "null_and_every_hidden_member_checked": True, "marginal_residual": marginal_residual,
            "diagonal_action_intertwining_residual": action_residual,
            "regular_cell_compression_verified": max(marginal_residual, action_residual) < 1e-10}


def fixed_palette_scaling_controls() -> list[dict]:
    class_size = matching_count(128)
    copies = (class_size - 1).bit_length() + 2
    rows = []
    for palette_size in (1, 2, 3, 4, 8, 10):
        palette = [tuple(i for i in range(copies) if (i + 1) & (1 << bit)) for bit in range(palette_size)]
        row = fixed_palette_information_contract(class_size, copies, palette,
            operations_and_readout_in_palette_algebra=True)
        row["half_degree"] = 128
        rows.append(row)
    return rows


@lru_cache(maxsize=2)
def audit_source_conditioned_cell_lifts(n: int, transposition_count: int) -> dict:
    """All source tuples of widths 1..3, under the null and EACH hidden member.

    The source-averaged lift alone is misleading: it equals the unconditioned
    state even when the average conditional distance remains large. Check
    moments, Parseval, and positive quotient-POVM extensions before averaging.
    """
    from coset_hidden_involution_binary_decision_reduction import (
        symmetric_group, compose_permutations, inverse_permutation, right_regular_matrix,
    )
    if (n, transposition_count) not in ((3, 1), (4, 2)):
        raise ValueError("finite lift controls use S3 transpositions or S4 perfect matchings")
    group, identity = symmetric_group(n), tuple(range(n))
    order, hidden_class = len(group), involutions(n, transposition_count)
    # The repository's right_regular_matrix multiplies by g (an anti-action
    # on column vectors). Invert g to match the irrep homomorphism convention.
    regular = np.asarray([right_regular_matrix(n, inverse_permutation(g)) for g in group], dtype=complex)
    reps = {lam: dict(permutation_representation_matrices(lam)) for lam in integer_partitions(n)}
    chars = {lam: np.array([np.trace(table[g]) for g in group]) for lam, table in reps.items()}
    dimensions = {lam: hook_length_dimension(lam) for lam in reps}
    central = {lam: dimensions[lam] / order * np.einsum("g,gij->ij", chars[lam].conjugate(), regular)
               for lam in reps}
    class_sizes = [len({compose_permutations(compose_permutations(x, g), inverse_permutation(x)) for x in group})
                   for g in group if g != identity]
    minimum_class_size = min(class_sizes)
    residuals = dict.fromkeys(("character_moments", "positivity", "hermiticity", "normalization",
        "all_group_moments", "parseval", "source_mass", "source_averaged_state",
        "second_moment_factorization", "jensen_bound", "uniform_moment_bound",
        "quotient_support", "povm_positivity", "povm_completeness", "povm_probability",
        "action_product_convention"), 0.0)
    rows, lifts, zero_mass_tuples, incomplete_support_extensions = [], 0, 0, 0
    noninvolution = next(g for g in group if compose_permutations(g, g) != identity)
    probe_elements = (group[1], noninvolution)
    group_index = {g: i for i, g in enumerate(group)}
    for g, h in itertools.product(group, repeat=2):
        residuals["action_product_convention"] = max(residuals["action_product_convention"],
            float(np.linalg.norm(regular[group_index[g]] @ regular[group_index[h]]
                                 - regular[group_index[compose_permutations(g, h)]])))
    b_regular = .37 * np.eye(order) + regular[group_index[probe_elements[0]]] + .23j * regular[group_index[probe_elements[1]]]
    for width in (1, 2, 3):
        extensions = {}
        for sources in itertools.product(reps, repeat=width):
            actions = []
            for g in probe_elements:
                action = np.ones((1, 1), dtype=complex)
                for lam in sources:
                    action = np.kron(action, reps[lam][g])
                actions.append(action)
            physical_dimension = math.prod(dimensions[lam] for lam in sources)
            b_physical = .37 * np.eye(physical_dimension) + actions[0] + .23j * actions[1]
            physical_effect = b_physical.conj().T @ b_physical
            scale = float(np.linalg.eigvalsh(physical_effect).max())
            physical_effect /= scale
            character = np.prod([chars[lam] for lam in sources], axis=0)
            present = [lam for lam in reps if (np.vdot(chars[lam], character) / order).real > .5]
            support = sum((central[lam] for lam in present), np.zeros((order, order), dtype=complex))
            # The physical quotient need not contain all irreps. Complete its
            # POVM by assigning every absent block to the second outcome.
            first = support @ b_regular.conj().T @ b_regular @ support / scale
            second = support - first + np.eye(order) - support
            residuals["povm_positivity"] = max(residuals["povm_positivity"],
                -float(np.linalg.eigvalsh(first).min()), -float(np.linalg.eigvalsh(second).min()))
            residuals["povm_completeness"] = max(residuals["povm_completeness"],
                float(np.linalg.norm(first + second - np.eye(order))))
            incomplete_support_extensions += len(present) < len(reps)
            extensions[sources] = physical_effect, first, support
        for hidden in (None, *hidden_class):
            states, weights, moments = {}, {}, {}
            for lam, table in reps.items():
                d = dimensions[lam]
                denominator = d if hidden is None else d + round(np.trace(table[hidden]).real)
                weights[lam] = d * denominator / order
                if denominator == 0:
                    continue
                states[lam] = (np.eye(d) if hidden is None else np.eye(d) + table[hidden]) / denominator
                moments[lam] = np.array([np.trace(states[lam] @ table[g]) for g in group])
                formula = np.array([(np.trace(table[g]) if hidden is None else
                    np.trace(table[g]) + np.trace(table[compose_permutations(hidden, g)])) / denominator for g in group])
                residuals["character_moments"] = max(residuals["character_moments"],
                    float(np.max(np.abs(moments[lam] - formula))))
            target = np.eye(order) / order if hidden is None else (np.eye(order) + right_regular_matrix(n, hidden)) / order
            target_moments = np.array([g == identity or g == hidden for g in group], dtype=float)
            outside = np.flatnonzero(target_moments == 0)
            second_moments = sum(weights[lam] * np.abs(values)**2 for lam, values in moments.items())
            t = min(1, 8 / minimum_class_size + 8 / len(hidden_class)) if hidden is not None else 1 / minimum_class_size
            residuals["uniform_moment_bound"] = max(residuals["uniform_moment_bound"],
                float(max(0, second_moments[outside].max() - t)))
            average = np.zeros_like(target, dtype=complex)
            distance = square = mass = 0.0
            for sources in itertools.product(reps, repeat=width):
                weight = math.prod(weights[lam] for lam in sources)
                if weight == 0:
                    zero_mass_tuples += 1
                    continue
                values = np.prod([moments[lam] for lam in sources], axis=0)
                lift = regular_algebra_state_lift(values, regular)
                physical = np.ones((1, 1), dtype=complex)
                for lam in sources:
                    physical = np.kron(physical, states[lam])
                physical_effect, lifted_effect, support = extensions[sources]
                residuals["povm_probability"] = max(residuals["povm_probability"],
                    float(abs(np.trace(physical @ physical_effect) - np.trace(lift @ lifted_effect))))
                residuals["quotient_support"] = max(residuals["quotient_support"],
                    float(np.linalg.norm(lift - support @ lift @ support)))
                residuals["positivity"] = max(residuals["positivity"], -float(np.linalg.eigvalsh(lift).min()))
                residuals["hermiticity"] = max(residuals["hermiticity"], float(np.linalg.norm(lift - lift.conj().T)))
                residuals["normalization"] = max(residuals["normalization"], float(abs(np.trace(lift) - 1)))
                residuals["all_group_moments"] = max(residuals["all_group_moments"],
                    float(np.max(np.abs(np.einsum("ij,gji->g", lift, regular) - values))))
                difference = lift - target
                parseval = order * float(np.trace(difference.conj().T @ difference).real)
                residuals["parseval"] = max(residuals["parseval"],
                    abs(parseval - float(np.abs(values - target_moments).dot(np.abs(values - target_moments)))))
                average += weight * lift
                mass += weight
                distance += weight * _half_trace_norm(difference)
                square += weight * parseval
                lifts += 1
            predicted = float(sum(second_moments[g]**width for g in outside))
            jensen = min(1, math.sqrt(max(0, predicted)) / 2)
            residuals["second_moment_factorization"] = max(residuals["second_moment_factorization"], abs(square - predicted))
            residuals["jensen_bound"] = max(residuals["jensen_bound"], max(0, distance - jensen))
            residuals["source_mass"] = max(residuals["source_mass"], abs(mass - 1))
            residuals["source_averaged_state"] = max(residuals["source_averaged_state"], float(np.linalg.norm(average - target)))
            rows.append({"cell_width": width, "hidden": list(hidden) if hidden is not None else None,
                "hypothesis": "alternative" if hidden is not None else "null",
                "average_conditional_trace_distance": distance, "average_conditional_parseval_square": square,
                "distance_of_averaged_state": _half_trace_norm(average - target),
                "exact_second_moment_jensen_upper_bound": jensen,
                "maximum_outside_second_moment": float(second_moments[outside].max()),
                "outside_modes_with_unit_second_moment": sum(abs(float(second_moments[g]) - 1) < 1e-10 for g in outside),
                "uniform_second_moment_upper_bound": t})
    return {"degree": n, "transposition_count": transposition_count, "group_order": order,
        "class_size": len(hidden_class), "minimum_nonidentity_class_size": minimum_class_size,
        "positive_weight_lifts_checked": lifts, "zero_weight_tuples_omitted": zero_mass_tuples,
        "incomplete_support_povm_extensions_checked": incomplete_support_extensions,
        "all_hidden_members_checked": True, "all_source_mass_retained": True,
        "controls": rows, "residuals": residuals,
        "finite_source_conditioned_lifts_verified": max(residuals.values()) < 1e-9,
        "efficient_physical_conversion_claimed": False}


def source_conditioned_palette_scaling_controls() -> list[dict]:
    rows = []
    for degree in (32, 64, 128, 512, 1024, 4096):
        class_size = matching_count(degree // 2)
        copies = (class_size - 1).bit_length() + 2
        for q in (1, 2, 3):
            # Balance all nonzero incidence signatures; do not silently omit
            # the zero-signature residue from the advertised large-cell test.
            palette = [tuple(i for i in range(copies) if (1 + i % (2**q - 1)) & (1 << bit)) for bit in range(q)]
            rows.append(source_conditioned_palette_information_contract(degree, copies, palette,
                palette_fixed_before_source_labels=True, operations_and_readout_in_cell_algebra=True))
    return rows


def source_conditioned_unbalanced_palette_controls() -> list[dict]:
    rows = []
    for degree in (128, 1024, 4096):
        copies = (matching_count(degree // 2) - 1).bit_length() + 2
        for small_width in (1, 10):
            large = tuple(range(2 * small_width, copies))
            palette = (tuple(range(small_width)) + large,
                       tuple(range(small_width, 2 * small_width)) + large)
            rows.append(source_conditioned_palette_information_contract(degree, copies, palette,
                palette_fixed_before_source_labels=True, operations_and_readout_in_cell_algebra=True,
                retain_cells_below=small_width + 1))
    return rows


@lru_cache(maxsize=2)
def audit_adaptive_palette_abort_cover(n: int, transposition_count: int) -> dict:
    """An actual measured-prefix choice, with every natural source retained.

    After L, choose R or T from the observed L label and a source label. For
    the {L,R} and {L,T} comparison programs, abort before the other operation.
    Check entire branch laws, not just their aggregate trace distances.
    """
    if (n, transposition_count) not in ((3, 1), (4, 2)):
        raise ValueError("abort-cover controls use the physical S3/S4 input classes")
    partitions, hidden = integer_partitions(n), involutions(n, transposition_count)
    reps = {lam: dict(permutation_representation_matrices(lam)) for lam in partitions}
    actual = [[], []]
    selected = [[[], []] for _ in range(2)]
    abort = np.zeros((2, 2))
    selection_mass = np.zeros((2, 2))
    branch_residual = prefix_residual = 0.0
    branches = 0
    for sources in itertools.product(partitions, repeat=3):
        dimension = math.prod(hook_length_dimension(lam) for lam in sources)
        states = [dimension / math.factorial(n)**3 * np.eye(dimension),
                  sum(_natural_informative_block(sources, h, reps) for h in hidden) / len(hidden)]
        left = _triple_isotypic_projectors(sources, "left")
        later = (_triple_isotypic_projectors(sources, "right"), _total_projectors(sources, reps))
        for outcome, projector in enumerate(left):
            chosen = (len(sources[0]) + outcome) % 2
            for hypothesis, state in enumerate(states):
                branch = projector @ state @ projector
                prefix_mass = float(np.trace(branch).real)
                selection_mass[chosen, hypothesis] += prefix_mass
                abort[1 - chosen, hypothesis] += prefix_mass
                probabilities = [float(np.trace(effect @ branch @ effect).real) for effect in later[chosen]]
                prefix_residual = max(prefix_residual, abs(sum(probabilities) - prefix_mass))
                actual[hypothesis].extend(probabilities)
                # Recompute the successful comparison branch directly from
                # its total Kraus word. The other comparison has already aborted.
                replay = [float(np.trace((effect @ projector) @ state @ (effect @ projector).conj().T).real)
                          for effect in later[chosen]]
                branch_residual = max(branch_residual, float(np.max(np.abs(np.array(replay) - probabilities))))
                selected[chosen][hypothesis].extend(replay)
            branches += len(later[chosen])
    whole = binary_outcome_statistics(*actual)
    comparisons = []
    for j in range(2):
        total = binary_outcome_statistics(
            selected[j][0] + [float(abort[j, 0])], selected[j][1] + [float(abort[j, 1])])
        success_difference = float(np.abs(np.array(selected[j][0]) - selected[j][1]).sum()) / 2
        comparisons.append({"palette": ["L", "R" if j == 0 else "T"],
            "complete_comparison": total,
            "unnormalized_success_sector_half_l1": success_difference,
            "success_mass_null": float(selection_mass[j, 0]),
            "success_mass_alternative": float(selection_mass[j, 1]),
            "abort_mass_null": float(abort[j, 0]), "abort_mass_alternative": float(abort[j, 1])})
    covered_distance = sum(row["unnormalized_success_sector_half_l1"] for row in comparisons)
    upper = min(1, sum(row["complete_comparison"]["total_variation"] for row in comparisons))
    residuals = {"successful_branch_law": branch_residual, "prefix_mass": prefix_residual,
        "disjoint_sector_reconstruction": abs(whole["total_variation"] - covered_distance),
        "unnormalized_cover_bound": max(0, whole["total_variation"] - upper),
        "all_source_mass": max(whole["normalization_residual"],
            *(row["complete_comparison"]["normalization_residual"] for row in comparisons))}
    return {"degree": n, "source_blocks_evaluated": len(partitions)**3,
        "classical_transcript_branches": branches, "actual_output": whole,
        "aborting_comparisons": comparisons, "sum_of_comparison_distance_upper_bound": upper,
        "residuals": residuals, "all_source_mass_retained": True,
        "selector_uses_an_actual_quantum_measurement_outcome": True,
        "aborts_before_outside_operation": True, "postselection_normalization_used": False,
        "finite_adaptive_cover_verified": max(residuals.values()) < 1e-9}


def adaptive_palette_catalogue_scaling_controls() -> list[dict]:
    rows = []
    for degree in (128, 1024, 4096):
        copies = (matching_count(degree // 2) - 1).bit_length() + 2
        balanced = tuple(tuple(i for i in range(copies) if (1 + i % 3) & (1 << bit)) for bit in range(2))
        large = tuple(range(20, copies))
        unbalanced = (tuple(range(10)) + large, tuple(range(10, 20)) + large)
        rows.append(adaptive_palette_catalogue_information_contract(degree, copies, (balanced, unbalanced),
            catalogue_fixed_before_input=True, complete_execution_covered=True,
            support_choices_classically_observed=True, operators_and_readout_respect_cover=True,
            retain_cells_below=11))
    return rows


COHERENT_PHASE_RULES = ("negative_character_reflection", "zero_character_reflection", "character_ratio_rotation")


def _coherent_phase_values(partitions: tuple, transposition_count: int, rule: str) -> dict:
    if rule not in COHERENT_PHASE_RULES:
        raise ValueError("unknown uniform character phase rule")
    result = {}
    for label in partitions:
        character = character_on_involution(label, transposition_count)
        if rule == "negative_character_reflection":
            result[label] = -1 if character < 0 else 1
        elif rule == "zero_character_reflection":
            result[label] = -1 if character == 0 else 1
        else:
            result[label] = np.exp(1.3j * character / hook_length_dimension(label))
    return result


@lru_cache(maxsize=6)
def _exact_reflection_support_audit(n: int, transposition_count: int, rule: str) -> dict:
    from symmetric_character import symmetric_character
    from coset_hidden_involution_multiplicity_support_obstruction import permutation_cycle_type
    from coset_hidden_involution_binary_decision_reduction import symmetric_group, compose_permutations
    if rule == "character_ratio_rotation":
        return {"exact_support_audit_available": False, "support_is_commuting": None,
                "noncommuting_advantage_implied": False}
    group, partitions = symmetric_group(n), integer_partitions(n)
    phases = _coherent_phase_values(partitions, transposition_count, rule)
    coefficients = {g: Fraction(sum(hook_length_dimension(lam) * phases[lam] *
        symmetric_character(lam, permutation_cycle_type(g)) for lam in partitions), len(group)) for g in group}
    support = {g for g, value in coefficients.items() if value}
    commuting = all(compose_permutations(g, h) == compose_permutations(h, g) for g in support for h in support)
    closed = tuple(range(n)) in support and all(compose_permutations(g, h) in support for g in support for h in support)
    return {"exact_support_audit_available": True, "support_size": len(support),
        "support_is_commuting": commuting, "support_is_subgroup": closed,
        "all_overlapping_subset_phase_actions_commute": True if commuting else None,
        "exact_coefficients": [{"permutation": list(g), "coefficient": str(value)} for g, value in coefficients.items() if value],
        "noncommuting_advantage_implied": False, "quantum_frontend_classically_replaced": False}


def _conditional_selector_kernel(coefficients: np.ndarray, moments: np.ndarray, masks: tuple[int, ...],
        inverse_indices: np.ndarray, inverse_product_indices: np.ndarray) -> np.ndarray:
    """Exact finite formula for Tr(sigma U_T^dagger U_S), before mask amplitudes.

    moments[i,g] is conditional on the SAME hidden h for all input factors.
    This does not replace a conditioned source by its Plancherel average.
    """
    kernel = np.empty((len(masks), len(masks)), dtype=complex)
    outer = np.outer(coefficients.conjugate(), coefficients).astype(complex)
    for si, s in enumerate(masks):
        for ti, t in enumerate(masks):
            term = outer.copy()
            for i, values in enumerate(moments):
                left, right = bool(s & (1 << i)), bool(t & (1 << i))
                if left and right:
                    term *= values[inverse_product_indices]
                elif left:
                    term *= values[None, :]
                elif right:
                    term *= values[inverse_indices, None]
            kernel[si, ti] = term.sum()
    return kernel


def _unconditioned_selector_kernel(masks: tuple[int, ...], mean: complex, empty_phase: complex) -> np.ndarray:
    kernel = np.full((len(masks), len(masks)), abs(mean)**2, dtype=complex)
    for si, s in enumerate(masks):
        for ti, t in enumerate(masks):
            if s == t:
                kernel[si, ti] = 1
            elif s == 0:
                kernel[si, ti] = empty_phase * mean.conjugate()
            elif t == 0:
                kernel[si, ti] = mean * empty_phase.conjugate()
    return kernel


@lru_cache(maxsize=16, typed=True)
def _coherent_walsh_histogram_law(n: int, transposition_count: int, copy_count: int,
        phase_rule: str) -> tuple:
    """Contract actual full-mask Walsh probabilities, without physical matrices.

    Joint (source label, output bit) histograms are sufficient by copy
    exchangeability. The |G|^2 signed contraction is a finite diagnostic,
    NOT a positive latent-variable sampler or an efficient S_n classifier.
    """
    from coset_hidden_involution_binary_decision_reduction import (
        symmetric_group, inverse_permutation, compose_permutations,
    )
    if (type(n) is not int or type(transposition_count) is not int
            or (n, transposition_count) not in ((3, 1), (4, 2)) or type(copy_count) is not int
            or not 1 <= copy_count <= (12 if n == 3 else 8)):
        raise ValueError("histogram controls require declared bounded S3/S4 copy ranges")
    partitions, group = integer_partitions(n), symmetric_group(n)
    order, index = len(group), {g: i for i, g in enumerate(group)}
    hidden = involutions(n, transposition_count)
    phases = _coherent_phase_values(partitions, transposition_count, phase_rule)
    reps = {lam: dict(permutation_representation_matrices(lam)) for lam in partitions}
    characters = {lam: np.array([np.trace(reps[lam][g]) for g in group]) for lam in partitions}
    coefficients = sum(hook_length_dimension(lam) * phases[lam] * characters[lam].conjugate() / order for lam in partitions)
    outer = np.outer(coefficients.conjugate(), coefficients).reshape(-1)
    inverses = np.array([index[inverse_permutation(g)] for g in group])
    products = np.array([[index[compose_permutations(inverse_permutation(u), v)] for v in group] for u in group])
    factors = []
    for h in (None, *hidden):
        translated = None if h is None else np.array([index[compose_permutations(h, g)] for g in group])
        local = []
        for lam in partitions:
            d = hook_length_dimension(lam)
            values = characters[lam] if h is None else characters[lam] + characters[lam][translated]
            for bit in range(2):
                local.append((d / (4 * order) * (values[0] + (-1)**bit *
                    (values[inverses, None] + values[None, :]) + values[products])).reshape(-1))
        factors.append(local)
    factors = np.asarray(factors)
    powers = np.array([factors**exponent for exponent in range(copy_count + 1)])
    histograms, laws = [], [[], []]
    imaginary_error = hidden_member_error = 0.0
    category_count = 2 * len(partitions)
    for categories in itertools.combinations_with_replacement(range(category_count), copy_count):
        histogram = tuple(categories.count(i) for i in range(category_count))
        multiplicity = math.factorial(copy_count) // math.prod(math.factorial(value) for value in histogram)
        contraction = np.ones((len(hidden) + 1, order**2), dtype=complex)
        for i, exponent in enumerate(histogram):
            if exponent:
                contraction *= powers[exponent, :, i, :]
        values = multiplicity * (contraction @ outer)
        imaginary_error = max(imaginary_error, float(np.max(np.abs(values.imag))))
        hidden_member_error = max(hidden_member_error, float(np.max(np.abs(values[1:] - values[1]))))
        histograms.append(histogram)
        laws[0].append(float(values[0].real))
        laws[1].append(float(np.mean(values[1:].real)))
    statistics = binary_outcome_statistics(*laws)
    return (tuple(histograms), np.asarray(laws[0]), np.asarray(laws[1]),
            {"imaginary_probability": imaginary_error, "class_member_outcome_invariance": hidden_member_error,
             "normalization": statistics["normalization_residual"]})


@lru_cache(maxsize=3, typed=True)
def _independent_label_factor_laws(n: int, transposition_count: int) -> tuple:
    from symmetric_character import kronecker_coefficient
    if (type(n) is not int or type(transposition_count) is not int
            or (n, transposition_count) not in ((3, 1), (4, 2), (6, 3))):
        raise ValueError("factor-law controls require declared S3/S4/S6 inputs")
    partitions = integer_partitions(n)
    single, pair = {}, {}
    for lam in partitions:
        d = hook_length_dimension(lam)
        ratio = 1 + Fraction(character_on_involution(lam, transposition_count), d)
        single[ratio] = single.get(ratio, Fraction()) + Fraction(d**2, math.factorial(n))
    for labels in itertools.product(partitions, repeat=3):
        multiplicity = kronecker_coefficient(*labels)
        if not multiplicity:
            continue
        dimensions = [hook_length_dimension(lam) for lam in labels]
        ratio = 1 + sum(Fraction(character_on_involution(lam, transposition_count), d) for lam, d in zip(labels, dimensions))
        if ratio < 0:
            raise ValueError("physical pair law has a negative likelihood")
        pair[ratio] = pair.get(ratio, Fraction()) + Fraction(math.prod(dimensions) * multiplicity, math.factorial(n)**2)
    return single, pair


def independent_pair_copy_baseline(n: int, transposition_count: int, copy_count: int) -> dict:
    """Exact finite law of a known disjoint-pair quantum front end and score."""
    if (type(n) is not int or type(transposition_count) is not int
            or (n, transposition_count) not in ((3, 1), (4, 2)) or type(copy_count) is not int
            or not 1 <= copy_count <= 12):
        raise ValueError("pair controls require bounded S3/S4 inputs")
    single, pair = _independent_label_factor_laws(n, transposition_count)
    law = {Fraction(1): Fraction(1)}
    for factor_law in [pair] * (copy_count // 2) + [single] * (copy_count % 2):
        updated = {}
        for left, p_left in law.items():
            for right, p_right in factor_law.items():
                ratio = left * right
                updated[ratio] = updated.get(ratio, Fraction()) + p_left * p_right
        law = updated
    if sum(law.values()) != 1 or sum(ratio * weight for ratio, weight in law.items()) != 1:
        raise ValueError("disjoint-pair likelihood law lost mass")
    distance = sum(abs(ratio - 1) * weight for ratio, weight in law.items()) / 2
    return {"copy_count": copy_count, "exact_total_variation": str(distance), "total_variation": float(distance),
        "additional_clean_pair_label_queries": copy_count // 2,
        "shared_hidden_class_invariant_law": True,
        "fixed_point_free_terminal_score": "involution_character_arithmetic.independent_pair_label_likelihood" if 2 * transposition_count == n else None,
        "fixed_point_free_terminal_scoring_polynomial": 2 * transposition_count == n,
        "law_enumeration_is_polynomial_in_degree": False, "quantum_frontend_classically_replaced": False}


def coherent_walsh_copy_scaling_controls() -> list[dict]:
    rows = []
    for n, t, copies in ((3, 1, (1, 2, 3, 4, 8, 12)), (4, 2, (1, 2, 3, 4, 6, 8))):
        for k in copies:
            histograms, null, alternative, residuals = _coherent_walsh_histogram_law(n, t, k, "negative_character_reflection")
            source_laws = [{}, {}]
            for histogram, p0, p1 in zip(histograms, null, alternative):
                source = tuple(histogram[i] + histogram[i + 1] for i in range(0, len(histogram), 2))
                for law, probability in zip(source_laws, (p0, p1)):
                    law[source] = law.get(source, 0.0) + probability
            source_statistics = binary_outcome_statistics(list(source_laws[0].values()), list(source_laws[1].values()))
            statistics = binary_outcome_statistics(null, alternative)
            baseline = independent_pair_copy_baseline(n, t, k)
            rows.append({"degree": n, "copy_count": k, "phase_rule": "negative_character_reflection",
                "include_empty_mask": True, "source_labels_retained": True,
                "walsh_readout": statistics, "source_only_readout": source_statistics,
                "gain_over_source_only": statistics["total_variation"] - source_statistics["total_variation"],
                "independent_pair_baseline": baseline,
                "gain_over_independent_pair_baseline": statistics["total_variation"] - baseline["total_variation"],
                "histogram_count": len(histograms), "ordered_outcome_count": (2 * len(integer_partitions(n)))**k,
                "group_pair_terms_per_histogram_per_hidden_member": math.factorial(n)**2,
                "residuals": residuals, "finite_outcome_contraction_verified": max(residuals.values()) < 1e-9,
                "is_growing_degree_scaling": False, "is_polynomial_sn_classifier": False,
                "is_legal_classical_coset_solver": False, "speedup_claim_allowed": False})
    return rows


@lru_cache(maxsize=32, typed=True)
def symmetric_boolean_fourier_profile(copy_count: int, rule: str, threshold: int | None = None) -> dict:
    """Exact Walsh spectrum by Hamming weight; O(k^2) integer recurrence.

    Fast evaluation of a threshold does not imply a small Fourier l1 norm.
    f=+1 means accept; the entire table is an audit, not the terminal rule.
    """
    if type(copy_count) is not int or not 1 <= copy_count <= 256 or rule not in ("parity", "threshold"):
        raise ValueError("bounded positive copy count and parity/threshold rule required")
    if rule == "parity" and threshold is not None:
        raise ValueError("parity does not take a threshold")
    k = copy_count
    if rule == "threshold":
        threshold = k // 2 + 1 if threshold is None else threshold
        if type(threshold) is not int or not 1 <= threshold <= k:
            raise ValueError("threshold must lie in [1,k]")
    f = [1 if (w % 2 if rule == "parity" else w >= threshold) else -1 for w in range(k + 1)]
    numerators = []
    for d in range(k + 1):
        values = [1, k - 2 * d]
        for w in range(1, k):
            numerator = (k - 2 * d) * values[-1] - (k - w + 1) * values[-2]
            if numerator % (w + 1):
                raise ArithmeticError("nonintegral Krawtchouk recurrence")
            values.append(numerator // (w + 1))
        numerators.append(sum(sign * coefficient for sign, coefficient in zip(f, values)))
    norm = Fraction(sum(math.comb(k, d) * abs(value) for d, value in enumerate(numerators)), 1 << k)
    return {"copy_count": k, "rule": rule, "threshold": threshold,
        "coefficient_numerators_by_degree": numerators, "common_denominator_power_of_two": k,
        "exact_fourier_l1_norm": str(norm),
        "largest_nonzero_degree": max(d for d, value in enumerate(numerators) if value),
        "majority_fourier_l1_lower_bound_power_of_two": ((k - 1) // 2 - (k - 1).bit_length()
            if k % 2 and rule == "threshold" and threshold == k // 2 + 1 else None),
        "audit_is_terminal_evaluation": False, "small_arithmetic_cost_implies_small_fourier_norm": False}


def coherent_terminal_rule_controls(n: int, transposition_count: int, copy_count: int) -> dict:
    histograms, null, alternative, residuals = _coherent_walsh_histogram_law(n, transposition_count, copy_count, "negative_character_reflection")
    partitions = integer_partitions(n)
    negative = [character_on_involution(lam, transposition_count) < 0 for lam in partitions]
    weight_laws = {corrected: [{}, {}] for corrected in (False, True)}
    for histogram, p0, p1 in zip(histograms, null, alternative):
        sources = tuple(histogram[2 * i] + histogram[2 * i + 1] for i in range(len(partitions)))
        for corrected, laws in weight_laws.items():
            weight = sum(histogram[2 * i + (0 if corrected and negative[i] else 1)] for i in range(len(partitions)))
            for law, probability in zip(laws, (p0, p1)):
                key = (sources, weight)
                law[key] = law.get(key, 0.0) + probability
    baseline = independent_pair_copy_baseline(n, transposition_count, copy_count)
    rows, joint_weights = [], []
    for corrected, laws in weight_laws.items():
        joint_weights.append({"phase_corrected": corrected,
            "source_and_weight_readout": binary_outcome_statistics(list(laws[0].values()), list(laws[1].values()))})
        for name, rule, threshold, complement in (("odd_parity", "parity", None, False),
                ("all_zero", "threshold", 1, True), ("strict_majority", "threshold", copy_count // 2 + 1, False)):
            accepted, joint = [0.0, 0.0], [{}, {}]
            for b, law in enumerate(laws):
                for (source, weight), probability in law.items():
                    accept = bool(weight % 2) if rule == "parity" else weight >= threshold
                    accept = accept != complement
                    accepted[b] += probability * accept
                    key = (source, accept)
                    joint[b][key] = joint[b].get(key, 0.0) + probability
            gap = accepted[1] - accepted[0]
            rows.append({"rule": name, "phase_corrected": corrected, "threshold": threshold, "complement": complement,
                "null_acceptance_probability": accepted[0], "alternative_acceptance_probability": accepted[1],
                "signed_acceptance_gap": gap, "equal_prior_success": (1 + gap) / 2,
                "gap_minus_known_disjoint_pair_gap": gap - baseline["total_variation"],
                "joint_source_and_rule_output": binary_outcome_statistics(list(joint[0].values()), list(joint[1].values())),
                "exact_fourier_l1_norm": symmetric_boolean_fourier_profile(copy_count, rule, threshold)["exact_fourier_l1_norm"],
                "fixed_point_free_terminal_implementation": "involution_character_arithmetic.coherent_walsh_terminal_decision" if 2 * transposition_count == n else None,
                "fitted_orientation_used": False, "finite_bayes_table_used_by_terminal_rule": False})
    return {"degree": n, "copy_count": copy_count, "phase_rule": "negative_character_reflection",
        "rules": rows, "joint_weight_controls": joint_weights, "independent_pair_baseline": baseline,
        "residuals": residuals, "growing_degree_signal_established": False, "speedup_claim_allowed": False}


def coherent_parity_scaling_controls() -> list[dict]:
    rows = []
    for n in (128, 1024, 4096):
        k = 4 * (matching_count(n // 2) - 1).bit_length()
        for d in (0, 1, k // 2, k):
            row = coherent_parity_information_contract(n, k, d, one_uniform_subset_query=True,
                parity_positions_fixed_before_input=True, physical_inputs_discarded=True)
            if d == 1:
                row["source_corrected_all_zero_absolute_gap_upper_bound_power_of_two"] = min(0, row["trace_distance_upper_bound_power_of_two"] + 2)
            rows.append(row)
    return rows


@lru_cache(maxsize=3, typed=True)
def _source_parity_group_data(n: int, transposition_count: int) -> tuple:
    """Integer class-character data only; no dense representation matrices."""
    from symmetric_character import symmetric_character
    from coset_hidden_involution_multiplicity_support_obstruction import permutation_cycle_type
    from coset_hidden_involution_binary_decision_reduction import symmetric_group, inverse_permutation, compose_permutations
    if (type(n) is not int or type(transposition_count) is not int
            or (n, transposition_count) not in ((3, 1), (4, 2), (6, 3))):
        raise ValueError("exact source-parity contractions require declared S3/S4/S6 controls")
    group, partitions = symmetric_group(n), integer_partitions(n)
    index = {g: i for i, g in enumerate(group)}
    characters = np.array([[symmetric_character(lam, permutation_cycle_type(g)) for g in group]
                           for lam in partitions], dtype=np.int64)
    dimensions = np.array([hook_length_dimension(lam) for lam in partitions], dtype=np.int64)
    hidden = involutions(n, transposition_count)
    translated = tuple(np.array([index[compose_permutations(h, g)] for g in group]) for h in hidden)
    signs = np.array([character_on_involution(lam, transposition_count) for lam in partitions])
    coefficients = (dimensions * np.where(signs < 0, -1, 1)) @ characters
    inverse = np.array([index[inverse_permutation(g)] for g in group])
    products = np.array([[index[compose_permutations(inverse_permutation(u), v)] for v in group] for u in group])
    if int(coefficients @ coefficients) != len(group)**2 or int(coefficients.sum()) != len(group):
        raise ArithmeticError("negative-character phase failed exact normalization")
    return group, partitions, characters, dimensions, signs, coefficients, inverse, products, translated


def _source_parity_local_moment(data: tuple, selection: str, corrected: bool, hidden_index: int | None) -> np.ndarray:
    group, _, characters, dimensions, signs, _, inverse, products, translated = data
    if selection not in ("all", "negative", "positive", "zero") or type(corrected) is not bool:
        raise ValueError("declared character selection and boolean phase correction required")
    if hidden_index is not None and (type(hidden_index) is not int or not 0 <= hidden_index < len(translated)):
        raise ValueError("hidden-member index outside the supplied class")
    selected = {"all": np.ones(len(signs), dtype=bool), "negative": signs < 0,
                "positive": signs > 0, "zero": signs == 0}[selection]
    values = characters if hidden_index is None else characters + characters[:, translated[hidden_index]]
    unselected_moment = (dimensions * ~selected) @ values
    selected_moment = (dimensions * selected * np.where(corrected & (signs < 0), -1, 1)) @ values
    numerator = (unselected_moment[0] + unselected_moment[products]
                 + selected_moment[inverse, None] + selected_moment[None, :])
    if np.any(np.abs(numerator) > 2 * len(group)):
        raise ArithmeticError("one-copy parity contraction exceeded its unit bound")
    return numerator


@lru_cache(maxsize=24, typed=True)
def source_selected_parity_moment_certificate(n: int, transposition_count: int,
        selection: str = "negative", phase_corrected: bool = True) -> dict:
    """Exact signed moment spectrum for an actual source-local terminal rule.

    Sum source labels BEFORE taking the k-th power, but never sum hidden h
    before that power. Simultaneous conjugation proves class invariance of
    the full contraction. Signed group-pair weights are not sampler weights.
    """
    data = _source_parity_group_data(n, transposition_count)
    group, _, _, _, _, coefficients, _, _, _ = data
    order = len(group)
    weights = np.outer(coefficients, coefficients).reshape(-1)
    spectra = []
    for hidden_index in (None, 0):
        moment = _source_parity_local_moment(data, selection, phase_corrected, hidden_index).reshape(-1)
        values, inverse = np.unique(moment, return_inverse=True)
        totals = np.zeros(len(values), dtype=np.int64)
        np.add.at(totals, inverse, weights)
        spectra.append([{"moment_numerator": int(value), "weight_numerator": int(weight)}
                        for value, weight in zip(values, totals) if weight])
    return {"degree": n, "transposition_count": transposition_count, "selection": selection,
        "phase_corrected": phase_corrected, "moment_denominator": 2 * order,
        "weight_denominator": order**2, "null_spectrum": spectra[0], "alternative_spectrum": spectra[1],
        "group_pairs_enumerated": order**2, "shared_hidden_member": True,
        "class_invariance_justification": "Conjugate u and v together with h; character predicates and phase coefficients are class functions.",
        "negative_weights_present": any(row["weight_numerator"] < 0 for spectrum in spectra for row in spectrum),
        "is_positive_classical_sampler": False, "is_polynomial_in_group_degree": False,
        "is_asymptotic_advantage_certificate": False}


def _parity_spectrum_mean(certificate: dict, hypothesis: str, copies: int) -> Fraction:
    return Fraction(sum(row["weight_numerator"] * row["moment_numerator"]**copies
                        for row in certificate[hypothesis + "_spectrum"]),
                    certificate["weight_denominator"] * certificate["moment_denominator"]**copies)


def _pair_event_count_baseline(n: int, transposition_count: int, copies: int) -> tuple:
    """Threshold each pair's exact likelihood, then optimally score its count."""
    _, pair = _independent_label_factor_laws(n, transposition_count)
    p0 = sum((mass for ratio, mass in pair.items() if ratio > 1), Fraction())
    p1 = sum((ratio * mass for ratio, mass in pair.items() if ratio > 1), Fraction())
    m = copies // 2
    distance = sum(abs(math.comb(m, j) * (p1**j * (1 - p1)**(m - j)
                   - p0**j * (1 - p0)**(m - j))) for j in range(m + 1)) / 2
    return distance, {"pair_count": m, "ignored_unpaired_copies": copies % 2,
        "single_pair_null_acceptance": str(p0), "single_pair_alternative_acceptance": str(p1),
        "total_variation": float(distance), "is_full_pair_likelihood_optimum": False,
        "pair_event_score": "accept iff 1+r_lambda+r_mu+r_nu > 1",
        "quantum_frontend_classically_replaced": False,
        "degree_dependent_count_threshold_calibration_charged": True}


def source_selected_parity_controls(n: int, transposition_count: int, copies: tuple[int, ...],
        selection: str = "negative", phase_corrected: bool = True) -> dict:
    if not copies or any(type(k) is not int or not 1 <= k <= 1024 for k in copies):
        raise ValueError("nonempty copy sweep of integer sizes in [1,1024] required")
    certificate = source_selected_parity_moment_certificate(n, transposition_count, selection, phase_corrected)
    rows = []
    for k in copies:
        means = [_parity_spectrum_mean(certificate, hypothesis, k) for hypothesis in ("null", "alternative")]
        if any(abs(value) > 1 for value in means):
            raise ArithmeticError("exact source-parity law has invalid probability")
        accepted = [(1 - value) / 2 for value in means]
        gap = accepted[1] - accepted[0]
        baseline_distance, baseline = _pair_event_count_baseline(n, transposition_count, k)
        rows.append({"copy_count": k, "null_acceptance_probability": float(accepted[0]),
            "alternative_acceptance_probability": float(accepted[1]), "signed_acceptance_gap": float(gap),
            "equal_prior_success": float((1 + gap) / 2),
            "absolute_gap_upper_bound_over_both_orientations": float(abs(gap)),
            "fitted_orientation_used": False, "independent_pair_event_count_baseline": baseline,
            "loses_to_pair_count_even_after_orientation_flip": abs(gap) < baseline_distance,
            "rational_gap_numerator_bits": abs(gap.numerator).bit_length(),
            "rational_gap_denominator_bits": gap.denominator.bit_length()})
    return {"degree": n, "selection": selection, "phase_corrected": phase_corrected,
        "acceptance_rule": "odd parity of the selected corrected bits; empty selection rejects",
        "fixed_point_free_terminal_implementation": "involution_character_arithmetic.coherent_walsh_terminal_decision" if n == 2 * transposition_count else None,
        "moment_certificate": certificate, "copy_sweep": rows,
        "retains_source_information_in_selection": selection != "all",
        "fixed_parity_information_bound_applies": selection == "all",
        "source_and_parity_joint_bayes_table_computed": False,
        "speedup_claim_allowed": False}


def source_selected_parity_all_copy_obstruction() -> dict:
    """A fixed-S6 statement for EVERY k>=2, not a growing-degree theorem."""
    certificate = source_selected_parity_moment_certificate(6, 3, "negative", True)
    envelopes = []
    for hypothesis in ("null", "alternative"):
        spectrum = certificate[hypothesis + "_spectrum"]
        radius = max(abs(Fraction(row["moment_numerator"], certificate["moment_denominator"])) for row in spectrum)
        norm = sum(abs(Fraction(row["weight_numerator"], certificate["weight_denominator"])) for row in spectrum)
        envelopes.append((norm, radius))
    baseline, _ = _pair_event_count_baseline(6, 3, 2)
    cutoff = next((k for k in range(2, 1025)
        if all(radius < 1 for _, radius in envelopes) and sum(norm * radius**k for norm, radius in envelopes) / 2 < baseline), None)
    prefix = [] if cutoff is None else [abs((_parity_spectrum_mean(certificate, "null", k)
               - _parity_spectrum_mean(certificate, "alternative", k)) / 2) for k in range(2, cutoff)]
    verified = cutoff is not None and all(gap < baseline for gap in prefix)
    return {"degree": 6, "selection": "negative", "phase_corrected": True,
        "all_copy_counts_from_two_covered": verified, "tail_starts_at_copy_count": cutoff,
        "exact_one_pair_baseline_gap": str(baseline),
        "exact_finite_prefix_maximum_absolute_gap": str(max(prefix, default=Fraction())),
        "finite_prefix_copy_counts_checked": len(prefix),
        "null_and_alternative_envelopes": [{"exact_weight_l1_norm": str(norm), "exact_radius": str(radius)} for norm, radius in envelopes],
        "exact_tail_start_gap_upper_bound": str(sum(norm * radius**cutoff for norm, radius in envelopes) / 2) if cutoff else None,
        "proof": "Exact prefix; for every k beyond cutoff, |gap| <= (L0*r0^k + L1*r1^k)/2 < the one-pair gap. Each radius is below one, so the tail bound decreases. The baseline may discard every input except its first pair.",
        "covers_either_accepting_orientation": True, "covers_arbitrary_source_based_postprocessing": False,
        "is_growing_degree_obstruction": False, "novelty_established": False,
        "proof_status": "exact-finite-degree-all-copy-certificate-review-pending" if verified else "blocked-certificate-inequality-failure"}


def audit_source_selected_parity_contraction() -> dict:
    laws_checked, exact_class_checks, residual = 0, 0, 0.0
    for n, t in ((3, 1), (4, 2)):
        partitions = integer_partitions(n)
        for k in (1, 2, 3):
            histograms, null, alternative, _ = _coherent_walsh_histogram_law(n, t, k, "negative_character_reflection")
            signs = [character_on_involution(lam, t) for lam in partitions]
            for selection in ("all", "negative", "positive", "zero"):
                selected = [selection == "all" or (selection == "negative" and s < 0)
                            or (selection == "positive" and s > 0) or (selection == "zero" and s == 0) for s in signs]
                for corrected in (False, True):
                    parity = [(-1)**sum(hist[2 * i + (0 if corrected and signs[i] < 0 else 1)]
                              for i, keep in enumerate(selected) if keep) for hist in histograms]
                    certificate = source_selected_parity_moment_certificate(n, t, selection, corrected)
                    for hypothesis, probabilities in (("null", null), ("alternative", alternative)):
                        residual = max(residual, abs(float(_parity_spectrum_mean(certificate, hypothesis, k)) - float(np.dot(parity, probabilities))))
                        laws_checked += 1
    for n, t in ((3, 1), (4, 2), (6, 3)):
        data = _source_parity_group_data(n, t)
        weights = np.outer(data[5], data[5]).reshape(-1)
        reference = source_selected_parity_moment_certificate(n, t)["alternative_spectrum"]
        for h in range(len(data[8])):
            values, inverse = np.unique(_source_parity_local_moment(data, "negative", True, h).reshape(-1), return_inverse=True)
            totals = np.zeros(len(values), dtype=np.int64)
            np.add.at(totals, inverse, weights)
            actual = [{"moment_numerator": int(value), "weight_numerator": int(weight)} for value, weight in zip(values, totals) if weight]
            if actual != reference:
                raise ArithmeticError("class-member moment spectra differ")
            exact_class_checks += 1
    return {"independent_histogram_probability_laws_checked": laws_checked,
        "maximum_histogram_law_residual": residual,
        "exact_all_hidden_member_spectra_checked": exact_class_checks,
        "integer_characters_compared_with_matrix_based_histograms": True,
        "no_dense_s6_tensor_states_constructed": True,
        "verified": residual < 1e-10, "formal_proof_verification": False}


@lru_cache(maxsize=14, typed=True)
def evaluate_coherent_subset_phase_query(n: int = 4, transposition_count: int = 2, copy_count: int = 3,
        phase_rule: str = "negative_character_reflection", include_empty_mask: bool = False) -> dict:
    """One explicit coherent phase query, keeping every initial source label.

    Direct controlled irrep unitaries and a separate character-moment kernel
    must agree. Only mask readouts are performed after discarding physical
    inputs; finite Helstrom tables are not called polynomial classifiers.
    """
    from coset_hidden_involution_binary_decision_reduction import (
        symmetric_group, inverse_permutation, compose_permutations,
    )
    if (type(n) is not int or type(transposition_count) is not int
            or (n, transposition_count) not in ((3, 1), (4, 2)) or type(copy_count) is not int
            or not 1 <= copy_count <= (4 if n == 3 else 3) or type(include_empty_mask) is not bool):
        raise ValueError("coherent controls require bounded S3/S4 physical inputs and an explicit mask convention")
    partitions, group = integer_partitions(n), symmetric_group(n)
    order, index = len(group), {g: i for i, g in enumerate(group)}
    hidden = involutions(n, transposition_count)
    reps = {lam: dict(permutation_representation_matrices(lam)) for lam in partitions}
    phases = _coherent_phase_values(partitions, transposition_count, phase_rule)
    characters = {lam: np.array([np.trace(reps[lam][g]) for g in group]) for lam in partitions}
    coefficients = sum(hook_length_dimension(lam) * phases[lam] * characters[lam].conjugate() / order for lam in partitions)
    inverse_indices = np.array([index[inverse_permutation(g)] for g in group])
    products = np.array([[index[compose_permutations(inverse_permutation(u), v)] for v in group] for u in group])
    masks = tuple(range(0 if include_empty_mask else 1, 2**copy_count))
    count = len(masks)
    walsh = np.array([[(-1)**((s & y).bit_count()) / math.sqrt(2**copy_count) for s in masks]
                      for y in range(2**copy_count)])
    residuals = dict.fromkeys(("unitary_query", "conditional_kernel", "state_positivity", "source_mass",
        "unconditioned_kernel", "mask_diagonal", "data_processing", "phase_unit_modulus",
        "coefficient_parseval", "unlabeled_closed_form"), 0.0)
    residuals["phase_unit_modulus"] = max(abs(abs(z) - 1) for z in phases.values())
    residuals["coefficient_parseval"] = abs(float(np.vdot(coefficients, coefficients).real) - 1)
    summed = [np.zeros((count, count), dtype=complex) for _ in range(2)]
    walsh_laws, plus_laws, source_laws = [[], []], [[], []], [[], []]
    walsh_histograms = [{}, {}]
    source_indices = {lam: i for i, lam in enumerate(partitions)}
    raw_distance = retained_distance = 0.0
    marginal_distances = {d: 0.0 for d in range(1, min(2, copy_count - 1) + 1)} if include_empty_mask else {}
    decorrelation_distances = [0.0, 0.0]
    source_counterexample = None
    maximum_conditioning_error = 0.0
    kernels_checked = source_blocks = zero_weight_blocks = 0
    parity_laws_checked = parity_random_branches_checked = 0
    unconditioned_null = _unconditioned_selector_kernel(masks, complex(coefficients[0]), complex(sum(coefficients))) / count
    unconditioned_alt = sum(_unconditioned_selector_kernel(masks, complex(coefficients[0] + coefficients[index[h]]),
        complex(sum(coefficients))) for h in hidden) / (len(hidden) * count)
    for sources in itertools.product(partitions, repeat=copy_count):
        dimensions = [hook_length_dimension(lam) for lam in sources]
        dimension = math.prod(dimensions)
        operators = []
        for s in masks:
            operator = np.zeros((dimension, dimension), dtype=complex)
            for coefficient, g in zip(coefficients, group):
                action = np.ones((1, 1), dtype=complex)
                for i, lam in enumerate(sources):
                    action = np.kron(action, reps[lam][g] if s & (1 << i) else np.eye(dimensions[i]))
                operator += coefficient * action
            residuals["unitary_query"] = max(residuals["unitary_query"], float(np.linalg.norm(operator.conj().T @ operator - np.eye(dimension))))
            operators.append(operator)
        operators = np.asarray(operators)
        physical_blocks = [np.zeros((dimension, dimension), dtype=complex) for _ in range(2)]
        selector_blocks = [np.zeros((count, count), dtype=complex) for _ in range(2)]
        for h in (None, *hidden):
            denominators = [d if h is None else d + character_on_involution(lam, transposition_count)
                            for lam, d in zip(sources, dimensions)]
            weight = math.prod(d * denominator / order for d, denominator in zip(dimensions, denominators))
            if weight == 0:
                zero_weight_blocks += 1
                continue
            physical = np.ones((1, 1), dtype=complex)
            moments = []
            for lam, d, denominator in zip(sources, dimensions, denominators):
                single = (np.eye(d) if h is None else np.eye(d) + reps[lam][h]) / denominator
                physical = np.kron(physical, single)
                moments.append(characters[lam] / d if h is None else np.array([
                    (characters[lam][index[g]] + characters[lam][index[compose_permutations(h, g)]]) / denominator for g in group]))
            transformed = np.einsum("sij,jk->sik", operators, physical)
            direct = np.einsum("sij,tij->st", transformed, operators.conjugate()) / count
            formula = _conditional_selector_kernel(coefficients, np.asarray(moments), masks, inverse_indices, products) / count
            residuals["conditional_kernel"] = max(residuals["conditional_kernel"], float(np.linalg.norm(direct - formula)))
            if include_empty_mask:
                walsh_probabilities = np.diag(walsh @ direct @ walsh.T).real
                for parity_mask in sorted({1, min(3, count - 1), count - 1}):
                    coherent_mean = sum((-1)**((y & parity_mask).bit_count()) * value for y, value in enumerate(walsh_probabilities))
                    randomized_mean = 0j
                    for s in masks:
                        product = operators[s ^ parity_mask].conj().T @ operators[s]
                        value = np.trace(physical @ product)
                        randomized_mean += value / count
                        residuals["hadamard_probability_range"] = max(residuals.get("hadamard_probability_range", 0.0), abs(float(value.real)) - 1)
                        parity_random_branches_checked += 1
                    residuals["random_two_subset_parity_law"] = max(residuals.get("random_two_subset_parity_law", 0.0),
                        abs(complex(coherent_mean) - randomized_mean))
                    parity_laws_checked += 1
            for d in marginal_distances:
                active, background = 2**d, 2**(copy_count - d)
                marginal = np.einsum("babc->ac", direct.reshape(background, active, background, active))
                mixture = np.zeros((active, active), dtype=complex)
                for background_mask in range(background):
                    cell_moment = np.ones(order, dtype=complex)
                    for i in range(copy_count - d):
                        if background_mask & (1 << i):
                            cell_moment *= moments[d + i]
                    collapsed = np.asarray(moments[:d] + [cell_moment])
                    mixture += _conditional_selector_kernel(coefficients, collapsed,
                        tuple(active | a for a in range(active)), inverse_indices, products) / count
                residuals["fixed_marginal_background_mixture"] = max(residuals.get("fixed_marginal_background_mixture", 0.0),
                    float(np.linalg.norm(marginal - mixture)))
            residuals["state_positivity"] = max(residuals["state_positivity"], -float(np.linalg.eigvalsh(direct).min()))
            residuals["mask_diagonal"] = max(residuals["mask_diagonal"], float(np.max(np.abs(np.diag(direct) - 1 / count))))
            hypothesis, prior = (0, 1) if h is None else (1, 1 / len(hidden))
            physical_blocks[hypothesis] += weight * prior * physical
            selector_blocks[hypothesis] += weight * prior * direct
            kernels_checked += 1
            prediction = unconditioned_null if h is None else _unconditioned_selector_kernel(masks,
                complex(coefficients[0] + coefficients[index[h]]), complex(sum(coefficients))) / count
            error = float(np.linalg.norm(direct - prediction))
            if error > max(maximum_conditioning_error, 1e-10):
                maximum_conditioning_error = error
                source_counterexample = {"source_partitions": [list(lam) for lam in sources],
                    "hypothesis": "null" if h is None else "alternative", "physical_source_weight": weight,
                    "conditional_vs_unconditioned_kernel_norm": error}
        raw_distance += _half_trace_norm(physical_blocks[1] - physical_blocks[0])
        retained_distance += _half_trace_norm(selector_blocks[1] - selector_blocks[0])
        for d in marginal_distances:
            active, background = 2**d, 2**(copy_count - d)
            difference = selector_blocks[1] - selector_blocks[0]
            marginal = np.einsum("babc->ac", difference.reshape(background, active, background, active))
            marginal_distances[d] += _half_trace_norm(marginal)
        for b, state in enumerate(selector_blocks):
            mass = float(np.trace(physical_blocks[b]).real)
            residuals["source_mass"] = max(residuals["source_mass"], abs(float(np.trace(state).real) - mass))
            source_laws[b].append(mass)
            walsh_values = np.diag(walsh @ state @ walsh.T).real.tolist()
            walsh_laws[b].extend(walsh_values)
            if include_empty_mask:
                for y, probability in enumerate(walsh_values):
                    key = [0] * (2 * len(partitions))
                    for i, lam in enumerate(sources):
                        key[2 * source_indices[lam] + ((y >> i) & 1)] += 1
                    histogram = tuple(key)
                    walsh_histograms[b][histogram] = walsh_histograms[b].get(histogram, 0.0) + probability
            plus = float(state.sum().real / count)
            plus_laws[b].extend((plus, mass - plus))
            summed[b] += state
            decorrelation_distances[b] += _half_trace_norm(state - mass * (unconditioned_null if b == 0 else unconditioned_alt))
        source_blocks += 1
    sources_only = binary_outcome_statistics(*source_laws)
    walsh_statistics, plus_statistics = binary_outcome_statistics(*walsh_laws), binary_outcome_statistics(*plus_laws)
    if include_empty_mask:
        histograms, null, alternative, contraction_residuals = _coherent_walsh_histogram_law(n, transposition_count, copy_count, phase_rule)
        residuals["walsh_histogram_contraction"] = max(abs(law[key] - probability)
            for law, values in zip(walsh_histograms, (null, alternative)) for key, probability in zip(histograms, values))
        residuals["histogram_sufficiency"] = abs(binary_outcome_statistics(null, alternative)["total_variation"] - walsh_statistics["total_variation"])
        residuals["contraction_probability_law"] = max(contraction_residuals.values())
    unlabeled_distance = _half_trace_norm(summed[1] - summed[0])
    means = [coefficients[0] + coefficients[index[h]] for h in hidden]
    delta_mean = sum(means) / len(hidden) - coefficients[0]
    delta_square = sum(abs(mean)**2 for mean in means) / len(hidden) - abs(coefficients[0])**2
    if include_empty_mask:
        nonempty = count - 1
        closed_distance = (math.sqrt((nonempty - 1)**2 * delta_square**2 + 4 * nonempty * abs(delta_mean)**2)
                           + (nonempty - 1) * abs(delta_square)) / (2 * count)
    else:
        closed_distance = (1 - 1 / count) * abs(delta_square)
    residuals["unlabeled_closed_form"] = abs(unlabeled_distance - closed_distance)
    residuals["unconditioned_kernel"] = max(float(np.linalg.norm(summed[0] - unconditioned_null)),
                                           float(np.linalg.norm(summed[1] - unconditioned_alt)))
    residuals["data_processing"] = max(0, sources_only["total_variation"] - retained_distance,
        walsh_statistics["total_variation"] - retained_distance, plus_statistics["total_variation"] - retained_distance,
        retained_distance - raw_distance, unlabeled_distance - retained_distance)
    for distance in marginal_distances.values():
        residuals["data_processing"] = max(residuals["data_processing"],
            sources_only["total_variation"] - distance, distance - retained_distance)
    pair_baseline = None
    if copy_count == 3:
        baseline = evaluate_binary_carrier_instruments(n, transposition_count)
        pair = next(row for row in baseline["schedules"] if row["schedule"] == "L")
        pair_total = next(row for row in baseline["schedules"] if row["schedule"] == "LT")
        pair_baseline = {"one_pair_explicit_character_classifier_distance": pair["one_pair_character_classifier_distance"],
            "pair_total_finite_outcome_distance": pair_total["transcript"]["total_variation"],
            "pair_total_uses_two_label_queries": True,
            "pair_total_is_scalable_classifier": False,
            "coherent_walsh_gain_over_one_pair_in_this_control": walsh_statistics["total_variation"] - pair["one_pair_character_classifier_distance"],
            "coherent_retained_gain_over_pair_total_in_this_control": retained_distance - pair_total["transcript"]["total_variation"]}
    return {"degree": n, "transposition_count": transposition_count, "copy_count": copy_count,
        "phase_rule": phase_rule, "include_empty_mask": include_empty_mask, "coherent_masks": count,
        "source_blocks_evaluated": source_blocks, "conditional_kernels_checked": kernels_checked,
        "conditional_parity_laws_checked": parity_laws_checked,
        "random_hadamard_branches_checked": parity_random_branches_checked,
        "zero_weight_alternative_blocks_omitted": zero_weight_blocks,
        "physical_input_trace_distance": raw_distance, "source_only_readout": sources_only,
        "selector_and_source_label_trace_distance": retained_distance,
        "selector_without_source_labels_trace_distance": unlabeled_distance,
        "unlabeled_selector_closed_form_distance": closed_distance,
        "walsh_readout_with_source_labels": walsh_statistics,
        "uniform_selector_test_with_source_labels": plus_statistics,
        "dephased_selector_trace_distance": sources_only["total_variation"],
        "source_conditioning_counterexample": source_counterexample,
        "source_selector_decorrelation_distances": {"null": decorrelation_distances[0], "alternative": decorrelation_distances[1]},
        "fixed_mask_marginal_with_all_source_labels_distances": {str(d): distance for d, distance in marginal_distances.items()},
        "existing_carrier_baselines": pair_baseline,
        "exact_reflection_support_audit": _exact_reflection_support_audit(n, transposition_count, phase_rule),
        "residuals": residuals, "finite_coherent_query_verified": max(residuals.values()) < 1e-9,
        "source_labels_retained_in_main_evaluation": True, "postselection_used": False,
        "finite_helstrom_table_is_compiled_classifier": False,
        "source_only_quantum_frontend_is_classical_solver": False,
        "growing_copy_advantage_established": False, "speedup_claim_allowed": False}


def unlabeled_selector_scaling_controls() -> list[dict]:
    rows = []
    for degree in (64, 128, 512, 1024, 4096):
        for include_empty in (False, True):
            row = unlabeled_coherent_selector_information_contract(matching_count(degree // 2),
                source_labels_discarded=True, physical_inputs_discarded=True,
                one_common_phase_element=True, include_empty_mask=include_empty)
            row["degree"] = degree
            rows.append(row)
    return rows


def fixed_selector_marginal_scaling_controls() -> list[dict]:
    return [low_order_coherent_selector_information_contract(n, 4 * (matching_count(n // 2) - 1).bit_length(), d,
        one_uniform_subset_query=True, output_is_fixed_mask_marginal=True, physical_inputs_discarded=True)
        for n in (64, 128, 1024) for d in (1, n.bit_length())]


def _total_projectors(sources: tuple, representations: dict) -> tuple[np.ndarray, ...]:
    n = sum(sources[0])
    dimension = math.prod(hook_length_dimension(lam) for lam in sources)
    result = []
    for target in integer_partitions(n):
        projector = np.zeros((dimension, dimension), dtype=complex)
        for g, rho in representations[target].items():
            projector += np.trace(rho).conjugate() * np.kron(np.kron(
                representations[sources[0]][g], representations[sources[1]][g]), representations[sources[2]][g])
        projector *= hook_length_dimension(target) / math.factorial(n)
        result.append((projector + projector.conj().T) / 2)
    return tuple(result)


@lru_cache(maxsize=34)
def _pair_gpe_instrument(left: tuple[int, ...], right: tuple[int, ...]):
    n = sum(left)
    if n not in (3, 4) or sum(right) != n:
        raise ValueError("dense GPE controls are restricted to compatible S3/S4 pairs")
    representations = {lam: dict(permutation_representation_matrices(lam)) for lam in integer_partitions(n)}
    group = tuple(representations[left])
    return finite_isotypic_instrument(
        [np.kron(representations[left][g], representations[right][g]) for g in group],
        {lam: [table[g] for g in group] for lam, table in representations.items()},
    )


@lru_cache(maxsize=2)
def evaluate_pair_gpe_cleanup(n: int, transposition_count: int) -> dict:
    """All physical source triples, comparing clean labels to discarded GPE rows.

    Pair-local group twirling destroys the shared-h correlation across that
    partition. This is not the global diagonal twirl, which preserves the
    binary class mixture. No favorable source block is postselected.
    """
    if (n, transposition_count) not in ((3, 1), (4, 2)):
        raise ValueError("cleanup controls use the physical S3/S4 classes")
    partitions, hidden = integer_partitions(n), involutions(n, transposition_count)
    representations = {lam: dict(permutation_representation_matrices(lam)) for lam in partitions}
    p0, p1, follow0, follow1 = [], [], [], []
    clean_distance = discarded_distance = 0.0
    residuals = dict.fromkeys(("clean_workspace", "legacy_projector", "first_label_probability",
                              "conditional_binary_proportionality", "discard_equals_pair_twirl",
                              "global_conjugation_preserves_binary_state"), 0.0)
    for sources in itertools.product(partitions, repeat=3):
        dimensions = [hook_length_dimension(lam) for lam in sources]
        dimension = math.prod(dimensions)
        null = dimension / math.factorial(n)**3 * np.eye(dimension)
        alternative = sum(_natural_informative_block(sources, h, representations) for h in hidden) / len(hidden)
        instrument = _pair_gpe_instrument(*sources[:2])
        residuals["clean_workspace"] = max(residuals["clean_workspace"], max(instrument.residuals.values()))
        left = _triple_isotypic_projectors(sources, "left")
        right = _triple_isotypic_projectors(sources, "right")
        spectator = np.eye(dimensions[2])
        discarded_alternative = np.zeros_like(alternative, dtype=complex)
        for index, label in enumerate(instrument.labels):
            projector = np.kron(instrument.projectors[label], spectator)
            residuals["legacy_projector"] = max(residuals["legacy_projector"], float(np.linalg.norm(projector - left[index])))
            clean0, clean1 = projector @ null @ projector, projector @ alternative @ projector
            zero, one = np.zeros_like(null, dtype=complex), np.zeros_like(alternative, dtype=complex)
            for kraus in instrument.fourier_kraus[label]:
                lifted = np.kron(kraus, spectator)
                zero += lifted @ null @ lifted.conj().T
                one += lifted @ alternative @ lifted.conj().T
            discarded_alternative += one
            clean_distance += _half_trace_norm(clean1 - clean0)
            discarded_distance += _half_trace_norm(one - zero)
            p0.append(float(np.trace(zero).real))
            p1.append(float(np.trace(one).real))
            residuals["first_label_probability"] = max(residuals["first_label_probability"],
                abs(p0[-1] - float(np.trace(clean0).real)), abs(p1[-1] - float(np.trace(clean1).real)))
            ratio = float(one_pair_likelihood_ratio(sources, label, transposition_count, "L"))
            residuals["conditional_binary_proportionality"] = max(residuals["conditional_binary_proportionality"],
                float(np.linalg.norm(one - ratio * zero)))
            for following in right:
                follow0.append(float(np.trace(following @ zero).real))
                follow1.append(float(np.trace(following @ one).real))
        twirled = np.zeros_like(alternative, dtype=complex)
        for g in representations[sources[0]]:
            pair = np.kron(representations[sources[0]][g], representations[sources[1]][g])
            local = np.kron(pair, spectator)
            twirled += local @ alternative @ local.conj().T / math.factorial(n)
            global_action = np.kron(pair, representations[sources[2]][g])
            residuals["global_conjugation_preserves_binary_state"] = max(
                residuals["global_conjugation_preserves_binary_state"],
                float(np.linalg.norm(global_action @ alternative @ global_action.conj().T - alternative)))
        residuals["discard_equals_pair_twirl"] = max(residuals["discard_equals_pair_twirl"],
            float(np.linalg.norm(discarded_alternative - twirled)))
    first, follow = binary_outcome_statistics(p0, p1), binary_outcome_statistics(follow0, follow1)
    verified = (max(residuals.values()) < 1e-8
                and abs(discarded_distance - first["total_variation"]) < 1e-8
                and abs(follow["total_variation"] - first["total_variation"]) < 1e-8
                and discarded_distance <= clean_distance + 1e-8)
    return {"n": n, "source_blocks_evaluated": len(partitions)**3, "residuals": residuals,
            "clean_first_pair_retained_trace_distance": clean_distance,
            "discarded_reference_retained_trace_distance": discarded_distance,
            "extra_loss_from_discarded_reference": clean_distance - discarded_distance,
            "first_pair_transcript": first, "discard_then_clean_right_transcript": follow,
            "finite_complete_source_cleanup_verified": bool(verified),
            "hypothesis_independent_state_after_first_label": residuals["conditional_binary_proportionality"] < 1e-8,
            "global_twirl_is_the_same_channel_as_pair_twirl": False}


def _rank_one_carrier_hmm(sources: tuple, projectors: dict, null: np.ndarray,
                          alternative: np.ndarray, schedules: tuple) -> dict:
    """Exact latent-total-irrep model, ONLY when both pair couplings have rank one.

    Joint projectors have physical rank d_nu, not rank one. 'Rank one' means
    rank in the multiplicity space. No general efficient Racah evaluator is
    assumed by this dense finite classical replay.
    """
    targets = integer_partitions(sum(sources[0]))
    dimensions = np.array([hook_length_dimension(nu) for nu in targets])
    joint = {side: [[total @ p for p in projectors[side]] for total in projectors["T"]] for side in "LR"}
    ranks = [float(np.trace(j).real) / dimensions[t] for side in "LR"
             for t, row in enumerate(joint[side]) for j in row]
    rank_residual = max(abs(value - round(value)) for value in ranks)
    maximum = max(round(value) for value in ranks)
    if rank_residual > 1e-8 or maximum > 1 or min(ranks) < -1e-8:
        return {"applicable": False, "maximum_multiplicity": maximum, "channels": {}}
    transitions = {}
    for previous, current in itertools.product("LR", repeat=2):
        transitions[previous + current] = np.array([
            [[float(np.trace(new @ old).real) / dimensions[t] for new in joint[current][t]]
             for old in joint[previous][t]] for t in range(len(targets))])
    channels = {}
    for schedule in schedules:
        if not schedule or any(side not in "LR" for side in schedule):
            continue
        side = schedule[0]
        branches = [(a, np.array([float(np.trace(joint[side][t][a] @ null).real) for t in range(len(targets))]),
                     np.array([float(np.trace(joint[side][t][a] @ alternative).real) for t in range(len(targets))]))
                    for a in range(len(targets))]
        for previous, current in zip(schedule, schedule[1:]):
            branches = [(b, p0 * transitions[previous + current][:, a, b], p1 * transitions[previous + current][:, a, b])
                        for a, p0, p1 in branches for b in range(len(targets))]
        output = {key: [] for key in ("null_transcript", "alt_transcript", "null_row", "alt_row")}
        for a, p0, p1 in branches:
            output["null_transcript"].append(float(p0.sum()))
            output["alt_transcript"].append(float(p1.sum()))
            emissions = np.stack([np.diag(joint[schedule[-1]][t][a]).real / dimensions[t] for t in range(len(targets))])
            output["null_row"].extend((p0 @ emissions).tolist())
            output["alt_row"].extend((p1 @ emissions).tolist())
        channels[schedule] = output
    return {"applicable": True, "maximum_multiplicity": maximum, "channels": channels}


@lru_cache(maxsize=4)
def evaluate_binary_carrier_instruments(n: int = 4, transposition_count: int = 2,
                                        schedules: tuple[str, ...] = SCHEDULES) -> dict:
    if n not in (3, 4) or type(transposition_count) is not int or not 1 <= transposition_count <= n // 2:
        raise ValueError("finite instruments restricted to nontrivial S3/S4 involution classes")
    if (not schedules or len(set(schedules)) != len(schedules)
            or any(type(s) is not str or len(s) > 3 or any(c not in "LRT" for c in s) for s in schedules)):
        raise ValueError("distinct L/R/T schedules of depth at most three required")
    partitions = integer_partitions(n)
    hidden = involutions(n, transposition_count)
    representations = {lam: dict(permutation_representation_matrices(lam)) for lam in partitions}
    accumulators = {s: {key: [] for key in ("null_transcript", "alt_transcript", "null_row", "alt_row", "null_dephased", "alt_dephased")}
                    for s in schedules}
    retained = dict.fromkeys(schedules, 0.0)
    rule_distance, rule_residual = dict.fromkeys(schedules, 0.0), dict.fromkeys(schedules, 0.0)
    hmm_residual, hmm_blocks, maximum_joint_multiplicity = 0.0, 0, 0
    raw_distance, source_blocks, maximum_projector_residual = 0.0, 0, 0.0
    for sources in itertools.product(partitions, repeat=3):
        dimensions = [hook_length_dimension(lam) for lam in sources]
        dimension = math.prod(dimensions)
        null = dimension / math.factorial(n)**3 * np.eye(dimension)
        alternative = sum(_natural_informative_block(sources, h, representations) for h in hidden) / len(hidden)
        raw_distance += _half_trace_norm(alternative - null)
        source_blocks += 1
        projectors = {side: _triple_isotypic_projectors(sources, "left" if side == "L" else "right") for side in "LR"}
        projectors["T"] = _total_projectors(sources, representations)
        hmm = _rank_one_carrier_hmm(sources, projectors, null, alternative, schedules)
        hmm_blocks += int(hmm["applicable"])
        maximum_joint_multiplicity = max(maximum_joint_multiplicity, hmm["maximum_multiplicity"])
        for side in "LRT":
            maximum_projector_residual = max(maximum_projector_residual,
                float(np.linalg.norm(sum(projectors[side]) - np.eye(dimension))),
                max(float(np.linalg.norm(p @ p - p)) for p in projectors[side]))
        branches = {"": [((), null, alternative, np.diag(null).real, np.diag(alternative).real)]}
        prefixes = sorted({s[:length] for s in schedules for length in range(1, len(s) + 1)}, key=lambda s: (len(s), s))
        for prefix in prefixes:
            branches[prefix] = []
            for labels, zero, one, classical_zero, classical_one in branches[prefix[:-1]]:
                for label, projector in enumerate(projectors[prefix[-1]]):
                    # Keep zero-probability outcomes. Their labels matter for
                    # comparing complete channels, and no branch is normalized.
                    transition = np.abs(projector)**2
                    branches[prefix].append((labels + (label,), projector @ zero @ projector,
                        projector @ one @ projector, transition @ classical_zero, transition @ classical_one))
        for schedule in schedules:
            output = accumulators[schedule]
            start = {key: len(output[key]) for key in ("null_transcript", "alt_transcript", "null_row", "alt_row")}
            for labels, zero, one, classical_zero, classical_one in branches[schedule]:
                p0, p1 = float(np.trace(zero).real), float(np.trace(one).real)
                output["null_transcript"].append(p0)
                output["alt_transcript"].append(p1)
                output["null_row"].extend(np.diag(zero).real.tolist())
                output["alt_row"].extend(np.diag(one).real.tolist())
                output["null_dephased"].extend(classical_zero.tolist())
                output["alt_dephased"].extend(classical_one.tolist())
                retained[schedule] += _half_trace_norm(one - zero)
                if schedule in ("L", "R"):
                    ratio = one_pair_likelihood_ratio(sources, partitions[labels[0]], transposition_count, schedule)
                    rule_residual[schedule] = max(rule_residual[schedule], abs(p1 - float(ratio) * p0))
                    if ratio > 1:
                        rule_distance[schedule] += p1 - p0
            if schedule in hmm["channels"]:
                for key, values in hmm["channels"][schedule].items():
                    hmm_residual = max(hmm_residual, float(np.max(np.abs(np.asarray(output[key][start[key]:]) - values))))
    rows = []
    for schedule in schedules:
        output = accumulators[schedule]
        transcript = binary_outcome_statistics(output["null_transcript"], output["alt_transcript"])
        row = binary_outcome_statistics(output["null_row"], output["alt_row"])
        classical = binary_outcome_statistics(output["null_dephased"], output["alt_dephased"])
        rows.append({"schedule": schedule or "NONE", "measurement_depth": len(schedule),
            "transcript": transcript, "young_row_readout": row,
            "product_dephased_markov_ablation": classical,
            "retained_quantum_trace_distance": retained[schedule],
            "irrecoverable_trace_distance_loss": max(0.0, raw_distance - retained[schedule]),
            "uncompiled_residual_measurement_gap": max(0.0, retained[schedule] - row["total_variation"]),
            "one_pair_character_classifier_distance": rule_distance[schedule] if schedule in ("L", "R") else None,
            "one_pair_character_likelihood_residual": rule_residual[schedule] if schedule in ("L", "R") else None,
            "latent_total_irrep_hmm_replay_verified": bool(schedule and all(side in "LR" for side in schedule)
                                                          and hmm_blocks == source_blocks and hmm_residual < 1e-8),
            "retained_helstrom_distance_is_implemented_readout": False,
            "dephased_ablation_is_a_general_classical_lower_bound": False})
    verified = bool(maximum_projector_residual < 1e-8 and hmm_residual < 1e-8 and all(
        item["transcript"]["total_variation"] <= item["young_row_readout"]["total_variation"] + 1e-8
        and item["young_row_readout"]["total_variation"] <= item["retained_quantum_trace_distance"] + 1e-8
        and item["retained_quantum_trace_distance"] <= raw_distance + 1e-8
        and item["product_dephased_markov_ablation"]["total_variation"] <= raw_distance + 1e-8
        and (item["one_pair_character_likelihood_residual"] is None
             or (item["one_pair_character_likelihood_residual"] < 1e-8 and abs(
                 item["one_pair_character_classifier_distance"] - item["transcript"]["total_variation"]) < 1e-8))
        for item in rows))
    return {"n": n, "transposition_count": transposition_count, "copy_count": 3,
            "hidden_class_size": len(hidden), "source_blocks_evaluated": source_blocks,
            "source_blocks_expected": len(partitions)**3, "postselected_source_mass": False,
            "physical_raw_trace_distance": raw_distance, "maximum_projector_residual": maximum_projector_residual,
            "latent_total_irrep_hmm_source_blocks": hmm_blocks, "maximum_joint_multiplicity": maximum_joint_multiplicity,
            "full_outcome_law_hmm_replay_residual": hmm_residual,
            "schedules": rows, "finite_full_source_instrument_checks_verified": verified}


def build_binary_carrier_instrument_report() -> dict:
    from symmetric_character import kronecker_coefficient
    controls = [evaluate_binary_carrier_instruments(3, 1), evaluate_binary_carrier_instruments(4, 2)]
    cleanup = [evaluate_pair_gpe_cleanup(3, 1), evaluate_pair_gpe_cleanup(4, 2)]
    arithmetic = label_arithmetic_scaling_controls()
    compression = [audit_regular_cell_compression(*spec) for spec in ((3, 1, 2), (3, 1, 3), (4, 2, 2))]
    conditioned = [audit_source_conditioned_cell_lifts(3, 1), audit_source_conditioned_cell_lifts(4, 2)]
    conditioned_verified = all(row["finite_source_conditioned_lifts_verified"] for row in conditioned)
    catalogue = [audit_adaptive_palette_abort_cover(3, 1), audit_adaptive_palette_abort_cover(4, 2)]
    catalogue_verified = all(row["finite_adaptive_cover_verified"] for row in catalogue)
    coherent = [evaluate_coherent_subset_phase_query(n, t, 3, rule, True)
                for n, t in ((3, 1), (4, 2)) for rule in COHERENT_PHASE_RULES]
    coherent.append(evaluate_coherent_subset_phase_query(4, 2, 3, "negative_character_reflection", False))
    coherent_verified = all(row["finite_coherent_query_verified"] for row in coherent)
    coherent_scaling = coherent_walsh_copy_scaling_controls()
    coherent_verified = coherent_verified and all(row["finite_outcome_contraction_verified"] for row in coherent_scaling)
    terminal = [coherent_terminal_rule_controls(row["degree"], 1 if row["degree"] == 3 else 2, row["copy_count"])
                for row in coherent_scaling]
    terminal_verified = all(max(row["residuals"].values()) < 1e-9 for row in terminal)
    selected_parity_audit = audit_source_selected_parity_contraction()
    selected_parity_obstruction = source_selected_parity_all_copy_obstruction()
    selected_parity = [source_selected_parity_controls(n, t, (1, 2, 4, 8, 16, 32, 64, 128), selection, corrected)
        for n, t in ((3, 1), (4, 2), (6, 3))
        for selection, corrected in (("negative", False), ("negative", True), ("positive", False), ("zero", False))]
    scaling = [{"half_degree": m, "block_size": 3, "classical_history_blocks": m**2,
                "trace_distance_squared_upper_bound": str(invariant_block_transcript_distance_squared_bound(m, 3, m**2))}
               for m in (4, 8, 16, 32, 64, 128)]
    verified = (all(row["finite_full_source_instrument_checks_verified"] for row in controls)
                and all(row["finite_complete_source_cleanup_verified"] for row in cleanup)
                and all(row["regular_cell_compression_verified"] for row in compression)
                and conditioned_verified and catalogue_verified and coherent_verified and terminal_verified
                and selected_parity_audit["verified"] and selected_parity_obstruction["all_copy_counts_from_two_covered"])
    witness_shape = (4, 2)
    coefficient = kronecker_coefficient(witness_shape, witness_shape, witness_shape)
    d = hook_length_dimension(witness_shape)
    source_mass = Fraction(d * (d + character_on_involution(witness_shape, 3)), math.factorial(6))**3
    return {"created_at": utc_now(), "status": ("binary-instrument-calibration-fixed-copy-route-obstructed" if verified else "blocked-instrument-control-failure"),
        "summary": "Source-selected parity now has an exact character-moment evaluator beyond S4. At S6 the corrected negative-character selection loses to even one pair for every k>=2, certified by an exact prefix and a decreasing moment tail. This is a fixed-degree negative result, not a growing-degree theorem or classical replacement. Earlier fixed-parity bounds remain scoped; source-aware collective thresholds are unresolved.",
        "derivation_document": "research/BINARY_CARRIER_INSTRUMENTS.md", "controls": controls, "scaling": scaling,
        "gpe_cleanup_controls": cleanup,
        "fixed_point_free_label_arithmetic_controls": arithmetic,
        "fixed_palette_regular_compression_controls": compression,
        "fixed_palette_scaling_controls": fixed_palette_scaling_controls(),
        "source_conditioned_palette_derivation": "research/SOURCE_CONDITIONED_PALETTE.md",
        "source_conditioned_lift_controls": conditioned,
        "source_conditioned_palette_scaling_controls": source_conditioned_palette_scaling_controls(),
        "source_conditioned_unbalanced_palette_controls": source_conditioned_unbalanced_palette_controls(),
        "adaptive_palette_catalogue_controls": catalogue,
        "adaptive_palette_catalogue_scaling_controls": adaptive_palette_catalogue_scaling_controls(),
        "coherent_subset_phase_derivation": "research/COHERENT_SUBSET_PHASE_QUERY.md",
        "coherent_subset_phase_controls": coherent,
        "coherent_walsh_fixed_group_copy_scaling": coherent_scaling,
        "coherent_terminal_rule_controls": terminal,
        "coherent_terminal_readout_derivation": "research/COHERENT_TERMINAL_READOUTS.md",
        "source_selected_parity_derivation": "research/SOURCE_SELECTED_PARITY.md",
        "source_selected_parity_controls": selected_parity,
        "source_selected_parity_contraction_audit": selected_parity_audit,
        "source_selected_parity_all_copy_obstruction": selected_parity_obstruction,
        "coherent_parity_scaling_controls": coherent_parity_scaling_controls(),
        "symmetric_terminal_fourier_norm_controls": [
            {key: value for key, value in symmetric_boolean_fourier_profile(k, rule, threshold).items()
             if key != "coefficient_numerators_by_degree"}
            for k in (3, 7, 15, 31, 63, 127)
            for rule, threshold in (("parity", None), ("threshold", 1), ("threshold", k // 2 + 1))],
        "coherent_subset_phase_resources": coherent_subset_phase_resource_contract(128, 1000,
            source_qft_operator_error=1e-8, phase_gpe_operator_error=1e-6),
        "unlabeled_coherent_selector_scaling_controls": unlabeled_selector_scaling_controls(),
        "fixed_selector_marginal_scaling_controls": fixed_selector_marginal_scaling_controls(),
        "clean_isotypic_label_access": isotypic_label_resource_contract(128, 128**2, 128, 1e-6),
        "classical_model_nonextension_witness": {"n": 6, "source_partitions": [list(witness_shape)] * 3,
            "pair_partition": list(witness_shape), "total_partition": list(witness_shape),
            "pair_kronecker_coefficient": coefficient, "joint_multiplicity": coefficient**2,
            "exact_natural_source_triple_mass": str(source_mass),
            "actual_joint_target_branch_mass_computed": False, "quantum_advantage_implied": False},
        "headline_metrics": {"finite_full_source_controls_passed": sum(row["finite_full_source_instrument_checks_verified"] for row in controls),
            "schedules_evaluated": sum(len(row["schedules"]) for row in controls),
            "explicit_one_pair_classifiers_checked": sum(item["one_pair_character_likelihood_residual"] is not None for row in controls for item in row["schedules"]),
            "source_blocks_evaluated": sum(row["source_blocks_evaluated"] for row in controls),
            "source_blocks_with_exact_latent_irrep_model": sum(row["latent_total_irrep_hmm_source_blocks"] for row in controls),
            "source_blocks_with_clean_gpe_contract": sum(row["source_blocks_evaluated"] for row in cleanup),
            "clean_gpe_cleanup_controls_passed": sum(row["finite_complete_source_cleanup_verified"] for row in cleanup),
            "polynomial_label_arithmetic_controls": len(arithmetic),
            "regular_cell_compression_controls_passed": sum(row["regular_cell_compression_verified"] for row in compression),
            "source_conditioned_lifts_checked": sum(row["positive_weight_lifts_checked"] for row in conditioned),
            "incomplete_support_povm_extensions_checked": sum(row["incomplete_support_povm_extensions_checked"] for row in conditioned),
            "adaptive_catalogue_source_blocks_checked": sum(row["source_blocks_evaluated"] for row in catalogue),
            "adaptive_catalogue_transcript_branches_checked": sum(row["classical_transcript_branches"] for row in catalogue),
            "coherent_subset_phase_controls_passed": sum(row["finite_coherent_query_verified"] for row in coherent),
            "source_conditioned_selector_kernels_checked": sum(row["conditional_kernels_checked"] for row in coherent),
            "coherent_measurement_uniform_primitive_reductions": 1,
            "coherent_walsh_fixed_group_scaling_controls": len(coherent_scaling),
            "declared_terminal_rules_evaluated": sum(len(row["rules"]) for row in terminal),
            "source_conditioned_parity_laws_checked": sum(row["conditional_parity_laws_checked"] for row in coherent),
            "random_hadamard_branches_checked": sum(row["random_hadamard_branches_checked"] for row in coherent),
            "source_selected_parity_copy_controls": sum(len(row["copy_sweep"]) for row in selected_parity),
            "source_selected_parity_independent_laws_checked": selected_parity_audit["independent_histogram_probability_laws_checked"],
            "source_selected_parity_exact_hidden_spectra_checked": selected_parity_audit["exact_all_hidden_member_spectra_checked"],
            "growing_copy_measurement_compilers": 0},
        "claim_gate": {"finite_complete_channel_evaluation_verified": verified,
            "invariant_transcript_implies_zero_binary_signal": False,
            "ideal_likelihood_tables_are_scalable_classifiers": False,
            "residual_helstrom_measurement_compiled": False, "general_classical_separation_proved": False,
            "legal_classical_sampler_for_initial_latent_distribution_supplied": False,
            "latent_model_replaces_quantum_frontend": False,
            "clean_isotypic_label_uniform_primitive_reduction_available": True,
            "exact_fixed_point_free_two_copy_score_available": True,
            "fixed_palette_coset_copy_compression_derived": True,
            "compression_covers_unlisted_subsets_or_unaccounted_source_labels": False,
            "finite_source_conditioned_lifts_verified": conditioned_verified,
            "source_conditioned_palette_bound_derived": True,
            "source_conditioned_bound_formally_verified": False,
            "source_conditioned_bound_novelty_established": False,
            "source_conditioned_bound_covers_label_selected_palettes": False,
            "separate_adaptive_catalogue_cover_bound_derived": True,
            "finite_adaptive_catalogue_cover_verified": catalogue_verified,
            "catalogue_bound_is_a_selector_runtime_lower_bound": False,
            "catalogue_bound_covers_coherent_support_selection": False,
            "finite_coherent_subset_phase_query_verified": coherent_verified,
            "coherent_phase_uniform_primitive_reduction_available": True,
            "coherent_selector_polynomial_terminal_rules_supplied": True,
            "coherent_terminal_controls_verified": terminal_verified,
            "coherent_selector_classifier_with_scalable_advantage_supplied": False,
            "random_two_subset_parity_reduction_derived": True,
            "parity_bound_covers_arbitrary_polynomial_time_readout": False,
            "source_selected_parity_exact_contraction_verified": selected_parity_audit["verified"],
            "s6_corrected_negative_parity_all_copy_failure_certified": selected_parity_obstruction["all_copy_counts_from_two_covered"],
            "source_selected_parity_growing_degree_obstruction_proved": False,
            "unlabeled_selector_information_bound_derived": True,
            "unlabeled_selector_bound_covers_retained_source_labels": False,
            "fixed_selector_marginal_bound_derived": True,
            "fixed_marginal_bound_covers_arbitrary_full_readout": False,
            "finite_clean_gpe_controls_verified": all(row["finite_complete_source_cleanup_verified"] for row in cleanup),
            "discarded_gpe_reference_implements_luders_in_general": False,
            "gate_level_sn_qft_backend_supplied": False,
            "finite_alternation_explained_by_latent_irrep_model": all(row["latent_total_irrep_hmm_source_blocks"] == row["source_blocks_evaluated"]
                                                                   and row["full_outcome_law_hmm_replay_residual"] < 1e-8 for row in controls),
            "fixed_copy_calibrations_are_candidate_algorithms": False, "speedup_claim_allowed": False},
        "falsifiers_triggered": ["Conjugation invariance removes hidden-member information, not necessarily class-versus-trivial information.",
            "Measuring another carrier label can irreversibly lose information; a large commutator does not certify an improved detector.",
            "All tested L/R binary outcome laws are reproduced by classical latent-irrep dynamics after the joint quantum label front end; no legal classical replacement of that front end is supplied.",
            "Discarding the GPE reference rows has the same first-label probabilities but is a pair-local twirl, not the assumed Luders instrument; it erases all remaining three-input binary information conditional on that label.",
            "A fixed subset palette with c incidence cells provides at most c effective coset samples, regardless of raw copies or repetitions within that algebra. Individual source labels or unlisted subset access must refine the cells.",
            "Retaining all classical source labels does not rescue fixed preselected palettes with sufficiently large cells: the separate approximate bound charges source priors and conditional lifting errors. S4 persistent modes falsify universal cell mixing; source-selected cells invalidate the iid estimate.",
            "Classical adaptive selection from a small predetermined whole-execution catalogue pays the sum of complete aborting-comparison bounds, without conditioning away failure mass. This is not a runtime bound for succinct exponentially large catalogues or coherent selectors.",
            "Source-label and selector marginals do not determine their joint binary information; S4 negative-character controls falsify the product-of-marginals shortcut.",
            "One common phase over uniformly coherent masks cannot amplify unlabeled selector information with mask count after discarding both physical inputs and source labels. This bound does not cover retained labels.",
            "Even with all source labels, retaining only fixed low-order selector marginals loses growing-degree signal under the uniform one-query contract. This does not bound a threshold of a low-degree score or an arbitrary full-bit classifier.",
            "S4's negative-character reflection has exact group-algebra support only on V4; even overlapping subset phase actions commute. Its finite copy gain is not evidence of a useful noncommuting mechanism.",
            "A fixed parity of ANY degree has the outcome law of a random two-subset Hadamard test, retaining all source labels. Input-independent randomization pays an average, not exponential catalogue size. Its bounded-Fourier-norm corollary rules out scalable all-zero success despite the finite S4 gain.",
            "Linear-time majority evaluation does not imply small Fourier norm: the exact odd-majority norm is at least 2^((k-1)/2)/k. The parity-transfer bound does not rule out arbitrary efficient thresholds.",
            "The source-corrected negative-character-selected parity loses at S6 for every k>=2 to a single pair, even if its accepting orientation is reversed. Exact moment envelopes certify the unbounded-copy tail; do not infer a growing-degree or arbitrary source-conditioned-readout theorem.",
            "Fixed-copy invariant instruments repeated polynomially many times remain below the required asymptotic information budget."],
        "next_experiments": ["Use label-summed character generating functions to test actual source-corrected Hamming thresholds beyond S4, against exact pair baselines. Source-selected parity is no longer an untested positive example; its corrected negative-character version has an all-copy S6 failure certificate, not an all-degree obstruction.",
            "Compare its full source-weighted channel against stronger product-basis and tensor-contraction baselines.",
            "Use the current schedules only as regression controls, not as evidence of a new scalable algorithm."],
    }


def write_binary_carrier_instrument_report(path: Path = REPORT_PATH, *, write_registry: bool = True,
        registry_experiment_id: str = DEFAULT_EXPERIMENT_ID, registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
        registry_result_id: str = "") -> dict:
    from research_registry import (ExperimentRecord, ExperimentResultRecord, NegativeResultRecord,
                                   upsert_experiment, upsert_experiment_result, upsert_negative_result)
    report = build_binary_carrier_instrument_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if write_registry:
        upsert_experiment(ExperimentRecord(id=registry_experiment_id, candidate_id=registry_candidate_id,
            title="Source-weighted binary carrier instruments", status=report["status"],
            hypothesis="Known carrier instruments expose useful binary information without assuming an ideal residual measurement.",
            protocol="Evaluate physical null/shared-hidden laws, actual readouts, retained states, latent-irrep replay, clean GPE and adversarial reference discard. Test source-conditioned regular lifts, quotient-POVM extensions and palette bounds. Evaluate coherent subset phases with direct unitaries and independent conditional kernels. Contract source-selected parity using exact character moments through S6; certify the corrected negative-selection all-copy failure against one pair. Charge QFT/action calls separately from classifier cost.",
            positive_signal="A growing-copy program with a compiled outcome classifier, not finite Bayes-table performance.",
            falsifiers=["outcome mass is missing", "disturbance destroys the needed signal", "GPE workspace is discarded instead of uncomputed", "classifier cost is omitted", "fixed-copy repetition fails the information bound"],
            metrics=list(report["headline_metrics"]), dependencies=["physical three-copy Fourier blocks", "existing pair-carrier projectors"],
            next_actions=report["next_experiments"]))
        upsert_experiment_result(ExperimentResultRecord(id=registry_result_id or f"RESULT-{registry_experiment_id}",
            experiment_id=registry_experiment_id, candidate_id=registry_candidate_id, created_at=report["created_at"],
            status=report["status"], summary=report["summary"], metrics=report["headline_metrics"],
            falsifiers_triggered=report["falsifiers_triggered"], artifacts={"binary_carrier_instruments": str(path)}))
        if report["claim_gate"]["finite_complete_channel_evaluation_verified"]:
            upsert_negative_result(NegativeResultRecord(id="CARRIER-INVARIANCE-NOT-A-BINARY-NO-GO", source=registry_experiment_id,
                claim="An invariant carrier transcript with no information about which class member is hidden cannot detect the class against the trivial subgroup.",
                reason_invalid="The two tasks have different priors and alternatives. Complete S3/S4 physical channels have nonzero binary signal; the one-pair character likelihood is checked independently.",
                lesson="Evaluate the actual null/alternative distributions, retain all source weights, and separately account for copy scaling and classifier implementation.",
                applies_to=[registry_candidate_id, "carrier transcript task transfer"], evidence={"artifact": str(path)}))
        if report["claim_gate"]["finite_alternation_explained_by_latent_irrep_model"]:
            upsert_negative_result(NegativeResultRecord(id="FINITE-BINARY-CARRIER-ALTERNATION-LATENT-IRREP", source=registry_experiment_id,
                claim="For the tested S3/S4 binary inputs, alternating carrier outcome laws cannot be reproduced by classical postprocessing of a joint pair/total quantum label outcome.",
                reason_invalid="Every L/R transcript and final Young-row probability is reproduced by latent-irrep Markov dynamics after the joint pair/total quantum label measurement. Measuring that total label after one pair resolves the retained finite binary information.",
                lesson="A dephased product-basis ablation was too weak. No legal classical sampler for the hypothesis-dependent initial latent distribution is supplied, so this does not replace the quantum front end. The rank-one condition already fails in S6, and transition-computation cost must be charged.",
                applies_to=[registry_candidate_id, "finite alternating-carrier binary signals"], evidence={"artifact": str(path)}))
        if report["claim_gate"]["finite_clean_gpe_controls_verified"]:
            upsert_negative_result(NegativeResultRecord(id="DISCARDED-GPE-REFERENCE-NOT-LUDERS-INSTRUMENT", source=registry_experiment_id,
                claim="Copying an isotypic label and discarding the GPE reference rows implements the clean projective instrument used by subsequent carrier measurements.",
                reason_invalid="Fourier Kraus sums give a group twirl within each label, not P rho P. All physical S3/S4 source triples retain only first-pair transcript information after pair-reference discard; in S4 this loses an additional 37/192 trace distance relative to clean L.",
                lesson="Copy only the irrep label, then invert the entire GPE computation to clean its workspace. Charge supplied QFT and controlled-action access. A global diagonal twirl preserves the binary mixture; this pair-local failure is neither an arbitrary compiler no-go nor classical dequantization.",
                applies_to=[registry_candidate_id, "isotypic instrument implementation"], evidence={"artifact": str(path), "derivation": report["derivation_document"]}))
        if report["claim_gate"]["finite_complete_channel_evaluation_verified"]:
            upsert_negative_result(NegativeResultRecord(id="FIXED-SUBSET-PALETTE-COPY-COMPRESSION", source=registry_experiment_id,
                claim="Polynomially many raw coset copies and arbitrarily repeated operations on a fixed small subset palette suffice for constant binary advantage, without any other source-label or readout access.",
                reason_invalid="Copies with identical nonzero membership signatures compress exactly to one coset state per cell for the entire allowed algebra. With c cells, T^2 <= (2^c-1)/(4M). For S256 and a three-subset palette, even 842 raw inputs provide at most seven effective samples.",
                lesson="Count every accessed subset and every final readout. Individual source labels refine cells to singletons; coherent unlisted subsets require a larger palette. This does not rule out growing palettes, ordinary source-conditioned algorithms, or general quantum measurements, and is not classical dequantization.",
                applies_to=[registry_candidate_id, "fixed-palette coherent subset programs"], evidence={"artifact": str(path), "derivation": report["derivation_document"]}))
        if report["claim_gate"]["finite_source_conditioned_lifts_verified"]:
            upsert_negative_result(NegativeResultRecord(id="SOURCE-LABELS-DO-NOT-RESCUE-FIXED-LARGE-CELLS", source=registry_experiment_id,
                claim="At polynomial raw copy budget, retaining all classical source labels suffices to rescue a fixed preselected subset palette with a bounded number of incidence cells.",
                reason_invalid="The review-pending bound compares source-conditioned cell lifts with coset states using character second moments, includes the full source-prior cost, and extends source-controlled POVMs through missing irreps. For S1024 with two balanced preselected subsets and the stated information-sufficient copy budget, exact outward rounding gives T <= 2^-602.",
                lesson="Use the source-conditioned formula, not exact copy compression, when labels are retained. Retain small cells as full quantum inputs and charge their raw copies; this handles arbitrary fixed-cell size profiles asymptotically. Source-dependent regrouping, growing palettes and uncharged outside-algebra readouts remain uncovered; a vacuous finite bound is not survival evidence. S4 has exact persistent conditional modes. This result has not been independently reviewed or established as novel.",
                applies_to=[registry_candidate_id, "source-conditioned fixed-palette subset programs"],
                evidence={"artifact": str(path), "derivation": report["source_conditioned_palette_derivation"], "status": "derived-review-pending"}))
        if report["claim_gate"]["finite_adaptive_catalogue_cover_verified"]:
            upsert_negative_result(NegativeResultRecord(id="ADAPTIVE-PALETTE-CATALOGUE-NOT-FREE-ESCAPE", source=registry_experiment_id,
                claim="Classical source/transcript adaptation among polynomially many predeclared bounded-cell palettes automatically evades the fixed-palette information obstruction.",
                reason_invalid="Aborting each comparison before its first outside operation reproduces disjoint unnormalized success sectors. Complete output distance is at most the sum of the fixed-palette bounds. Uniformly bounded cell counts and polynomial catalogue/copy counts remain obstructed asymptotically. The S1024 two-palette control gives T <= 2^-601.",
                lesson="Every whole execution and final readout must fit one listed palette; stepwise coverage is insufficient. Keep abort mass, assign overlapping covers once, and never replace actual posteriors by a uniform prior. Coherent selectors and succinct exponential catalogues remain uncovered; catalogue cardinality is not selector runtime. The derivation is review-pending with novelty unestablished.",
                applies_to=[registry_candidate_id, "classically adaptive finite-catalogue subset programs"],
                evidence={"artifact": str(path), "derivation": report["source_conditioned_palette_derivation"], "status": "derived-review-pending"}))
        if report["claim_gate"]["finite_coherent_subset_phase_query_verified"]:
            if report["claim_gate"]["source_selected_parity_exact_contraction_verified"] and report["claim_gate"]["s6_corrected_negative_parity_all_copy_failure_certified"]:
                upsert_negative_result(NegativeResultRecord(id="S6-SOURCE-SELECTED-PARITY-ALL-COPY-FAILURE", source=registry_experiment_id,
                    claim="Taking the source-corrected parity only on negative-character labels beats a one-pair detector at S6 for some k>=2.",
                    reason_invalid="Exact class-character moment contraction gives null radius 139/180 and alternative radius 13/15. The absolute gap is below 1271/7200 for k=2,...,37 by exact arithmetic; its l1-weighted tail is below the same one-pair gap for every k>=38 and decreases thereafter. Reversing the declared accepting orientation cannot rescue the rule.",
                    lesson="Cut this specified readout as a successful S6 calibration. This is a fixed-degree all-copy certificate, not an all-degree obstruction, not a bound on joint source/parity Bayes tables, and not a classical replacement of the pair quantum front end. Source selection genuinely escapes the fixed-parity theorem but does not guarantee useful signal. Independent review and novelty checks remain outstanding.",
                    applies_to=[registry_candidate_id, "source-selected negative-character corrected parity"],
                    evidence={"artifact": str(path), "derivation": report["source_selected_parity_derivation"], "status": "exact-finite-degree-review-pending"}))
            upsert_negative_result(NegativeResultRecord(id="COHERENT-PARITY-AND-BOUNDED-FOURIER-NORM-READOUTS", source=registry_experiment_id,
                claim="A full or partial Walsh parity, or a decision with a polynomial source-uniform Fourier coefficient envelope such as the source-phase-corrected all-zero test, evades the source-conditioned palette obstruction for one uniform subset query.",
                reason_invalid="Its complete source-conditioned parity law equals a Hadamard test of U_(S xor B)^dagger U_S for input-independent uniform S, using at most three incidence cells. A uniform worst-cell-profile bound vanishes at polynomial copy count. Fourier expansion transfers it with the coefficient l1 norm, which is below three for all-zero decisions even after source-dependent bit flips. S1024 k=17528 gives absolute all-zero acceptance gap <=2^-139.",
                lesson="Keep the same hidden h and all source mass. This is a randomized quantum front end, not classical dequantization. Averages require input-independent random S; source-selected parity positions or simultaneous joint parities are not covered. Transfer requires sum_B sup_source |coefficient_B|, not merely a small norm separately for each source. Large-Fourier-norm thresholds remain open. The derivation depends on the earlier source-conditioned bound and is review-pending, without a novelty claim.",
                applies_to=[registry_candidate_id, "coherent parity and bounded-Fourier-norm terminal rules"],
                evidence={"artifact": str(path), "derivation": report["coherent_terminal_readout_derivation"], "status": "derived-review-pending"}))
            upsert_negative_result(NegativeResultRecord(id="POLYNOMIAL-READOUT-TIME-NOT-SMALL-FOURIER-NORM", source=registry_experiment_id,
                claim="Because parity-transfer bounds handle polynomial Fourier l1 norm, they rule out every polynomial-time classifier of the Walsh output.",
                reason_invalid="Strict majority is evaluated by a linear-time count but its exact odd-k Fourier norm is at least 2^((k-1)/2)/k. An independent binomial formula checks the Krawtchouk recurrence; at k=127 the norm exceeds 2^60. Fourier degree, norm and classical evaluation time are different resources.",
                lesson="Charge the actual Fourier coefficient norm or prove a separate distribution-specific approximation argument. Do not transfer low-marginal, low-degree or bounded-norm obstructions to a threshold merely because its arithmetic is cheap. Escaping this bound is not evidence of quantum advantage.",
                applies_to=[registry_candidate_id, "efficient-terminal-rule bound transfers"],
                evidence={"artifact": str(path), "derivation": report["coherent_terminal_readout_derivation"]}))
            upsert_negative_result(NegativeResultRecord(id="S4-COHERENT-SIGN-PHASE-HAS-ABELIAN-SUPPORT", source=registry_experiment_id,
                claim="The S4 negative-character coherent subset-phase gain over disjoint pairs is evidence that noncommuting subset actions produce a useful nonabelian algorithmic mechanism.",
                reason_invalid="Independent exact character arithmetic gives coefficient -1/2 at the identity, +1/2 at each of the three perfect matchings and zero elsewhere. These four elements form V4, so all overlapping subset phase actions commute. The operator is (3 C_S-I)/2 for the single-subset class average.",
                lesson="Keep this finite control for normalization and source-correlation checks, not as evidence of a scalable noncommuting advantage. No growing-degree support classification or legal classical replacement of the quantum front end is inferred.",
                applies_to=[registry_candidate_id, "small-group coherent phase signals"],
                evidence={"artifact": str(path), "derivation": report["coherent_subset_phase_derivation"]}))
            upsert_negative_result(NegativeResultRecord(id="FIXED-SELECTOR-MARGINAL-NOT-SCALABLE-READOUT", source=registry_experiment_id,
                claim="With all source labels retained, reading only O(log n) fixed mask bits of the one-uniform-subset-query output suffices for nonnegligible binary signal at polynomial copy budget.",
                reason_invalid="Tracing the other mask qubits gives an input-independent binomial mixture of background subsets. Each branch has d raw singleton inputs and one background cell; the source-conditioned cell bound plus the unnormalized small-background tail applies. S1024 at k=17528,d=11 has T <= 2^-2174 with exact outward rounding. The raw-copy bound covers the small-k regime.",
                lesson="The marginal positions must be fixed before the input; physical inputs and unobserved masks are discarded without joint selector processing. This does not rule out full-bit decisions, thresholding a low-degree score, multiple queries or source-selected positions. The extension is review-pending, depends on the source-conditioned lifting argument and establishes no novelty.",
                applies_to=[registry_candidate_id, "fixed low-order coherent-selector readouts"],
                evidence={"artifact": str(path), "derivation": report["coherent_subset_phase_derivation"], "status": "derived-review-pending"}))
            upsert_negative_result(NegativeResultRecord(id="UNLABELED-COHERENT-MASK-COUNT-NOT-INFORMATION-AMPLIFICATION", source=registry_experiment_id,
                claim="For one common group-algebra phase query, uniform coherent mask count alone amplifies binary information after all physical inputs and source labels are discarded.",
                reason_invalid="The unlabeled selector kernel has unit diagonal and one common nonempty off-diagonal value. Its squared trace distance is at most min(1,3/M), or min(1,5/M) including the empty mask, independent of mask count. Direct conditional matrices summed over every natural source verify the closed form in S3/S4.",
                lesson="This review-pending derivation excludes retained source labels, retained physical inputs, mask-dependent phases and multiple queries. It is not a general coherent-measurement obstruction and establishes no novelty.",
                applies_to=[registry_candidate_id, "unlabeled one-query coherent subset programs"],
                evidence={"artifact": str(path), "derivation": report["coherent_subset_phase_derivation"], "status": "derived-review-pending"}))
            upsert_negative_result(NegativeResultRecord(id="SOURCE-SELECTOR-MARGINALS-NOT-JOINT-INFORMATION", source=registry_experiment_id,
                claim="The retained-source coherent selector can be assessed by replacing each joint hypothesis state with the product of its source-label and selector marginals.",
                reason_invalid="The S4 nonempty-mask negative-character control has joint distance 0.605655 while the sum of marginal distances is only 0.558036. Its conditional kernels differ from the unconditioned kernel on positive-mass sources. The product-state shortcut loses hypothesis-relevant correlations.",
                lesson="Keep the complete classical-quantum source blocks and the same hidden member in every input factor. These finite countercontrols do not establish a growing-degree signal; the full-mask Walsh readout still loses to the existing pair-plus-total finite baseline.",
                applies_to=[registry_candidate_id, "coherent selector source-conditioning shortcuts"],
                evidence={"artifact": str(path), "derivation": report["coherent_subset_phase_derivation"]}))
    return report
