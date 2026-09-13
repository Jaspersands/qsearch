"""Stream exact C(h)-conjugation orbits; still factorial in group degree.

Only the first group endpoint is reduced. Every second endpoint and each
orbit's exact multiplicity are charged; h is shared by all input copies.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
import itertools
import math

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from symmetric_character import symmetric_character, conjugacy_class_size
from coset_hidden_involution_multiplicity_support_obstruction import permutation_cycle_type


def _permutation_ranks(values: np.ndarray) -> np.ndarray:
    """Lexicographic Lehmer ranks of already-validated permutation rows."""
    rank = np.zeros(len(values), dtype=np.int64)
    for j in range(values.shape[1]-1):
        rank += (values[:, j, None] > values[:, j+1:]).sum(axis=1) * math.factorial(values.shape[1]-j-1)
    return rank


@lru_cache(maxsize=3, typed=True)
def matching_centralizer_orbits(n: int) -> tuple:
    if type(n) is not int or n not in (4, 6, 8):
        raise ValueError("streamed orbit controls support even degrees 4,6,8 only")
    group = tuple(itertools.permutations(range(n)))
    index = {g: j for j, g in enumerate(group)}
    generators = []
    for j in range(n//2):
        s = list(range(n))
        s[2*j], s[2*j+1] = s[2*j+1], s[2*j]
        generators.append(tuple(s))
    for j in range(n//2-1):
        s = list(range(n))
        s[2*j:2*j+4] = s[2*j+2:2*j+4] + s[2*j:2*j+2]
        generators.append(tuple(s))
    h = tuple(j ^ 1 for j in range(n))
    if any(tuple(s[h[s[j]]] for j in range(n)) != h for s in generators):
        raise ArithmeticError("orbit generator does not centralize the shared involution")
    visited, orbits = set(), []
    for representative in group:
        if representative in visited:
            continue
        visited.add(representative)
        members = [representative]
        for g in members:
            for s in generators:
                transformed = tuple(s[g[s[j]]] for j in range(n))
                if transformed not in visited:
                    visited.add(transformed)
                    members.append(transformed)
        orbits.append(tuple(index[g] for g in members))
    centralizer_order = 2**(n//2) * math.factorial(n//2)
    if sum(map(len, orbits)) != len(group) or any(centralizer_order % len(orbit) for orbit in orbits):
        raise ArithmeticError("centralizer orbit mass or stabilizer divisibility failed")
    return group, tuple(generators), tuple(orbits)


def _accumulate(target: dict, spectrum: tuple) -> None:
    for key, weight in spectrum:
        target[key] = target.get(key, 0) + weight


def _freeze(spectrum: dict) -> tuple:
    return tuple((key, value) for key, value in sorted(spectrum.items()) if value)


@lru_cache(maxsize=3, typed=True)
def source_orbit_character_data(n: int) -> tuple:
    """Existing categorical certificate plus an independent weight certificate."""
    from coset_binary_carrier_instruments import _integer_multinomial_spectrum, _integer_pair_spectrum

    group, generators, orbits = matching_centralizer_orbits(n)
    order = len(group)
    # Every int64 accumulation is bounded by ||A||_1^2 <= D^3 at these degrees.
    if order**3 > np.iinfo(np.int64).max:
        raise ArithmeticError("orbit spectrum exceeds the exact int64 accumulation budget")
    values = np.asarray(group, dtype=np.int64)
    if not np.array_equal(_permutation_ranks(values), np.arange(order)):
        raise ArithmeticError("streamed product ranks disagree with group enumeration")
    h = np.arange(n, dtype=np.int64) ^ 1
    translated = _permutation_ranks(h[values])
    partitions = integer_partitions(n)
    dimensions = tuple(hook_length_dimension(lam) for lam in partitions)
    signs = tuple(symmetric_character(lam, (2,)*(n//2)) for lam in partitions)
    from involution_character_arithmetic import fixed_point_free_character_certificate
    if any(fixed_point_free_character_certificate(lam).character != sign for lam, sign in zip(partitions, signs)):
        raise ArithmeticError("Murnaghan-Nakayama and two-quotient phase predicates disagree")
    table = np.array([[symmetric_character(lam, cycle) for cycle in partitions] for lam in partitions], dtype=np.int64)
    class_sizes = np.array([conjugacy_class_size(cycle) for cycle in partitions], dtype=np.int64)
    if not np.array_equal((table*class_sizes) @ table.T, order*np.eye(len(partitions), dtype=np.int64)):
        raise ArithmeticError("streamed character table failed exact row orthogonality")
    phase = tuple(-1 if value < 0 else 1 for value in signs)
    class_coefficients = dict(zip(partitions, (np.array(dimensions)*phase) @ table))
    cycle_types = tuple(permutation_cycle_type(g) for g in group)
    if Counter(cycle_types) != dict(zip(partitions, class_sizes)):
        raise ArithmeticError("enumerated permutations disagree with exact conjugacy-class sizes")
    coefficients = np.array([class_coefficients[cycle] for cycle in cycle_types], dtype=np.int64)
    if int(coefficients @ coefficients) != order**2 or int(coefficients.sum()) != order or int(coefficients @ coefficients[translated]) != 0:
        raise ArithmeticError("streamed reflection failed exact unitary normalization")
    identity = np.zeros(order, dtype=np.int64)
    identity[0] = order
    if np.any((identity + coefficients) % 2):
        raise ArithmeticError("reflection categories have nonintegral projector numerators")
    projectors = np.array([(identity+coefficients)//2, (identity-coefficients)//2])
    if not np.array_equal(projectors @ projectors.T, np.diag(order*projectors[:, 0])):
        raise ArithmeticError("streamed source projectors are not orthogonal")
    full, tails, weight_full, weight_tails = ([{} for _ in (0, 1)] for _ in range(4))
    negative_factors = [0, 0]
    projector_values = (projectors, projectors+projectors[:, translated])
    amplitudes = (coefficients, coefficients+coefficients[translated])
    for orbit in orbits:
        u, multiplicity = orbit[0], len(orbit)
        inverse_u = np.argsort(values[u])
        inverse_index = int(_permutation_ranks(inverse_u[None, :])[0])
        products = _permutation_ranks(inverse_u[values])
        pair_weights = multiplicity * coefficients[u] * coefficients
        for b in (0, 1):
            p, a = projector_values[b], amplitudes[b]
            diagonal = products == 0
            if b:
                diagonal |= products == translated[0]
            factors = []
            for j, sign in enumerate((1, -1)):
                base = p[j, 0]+p[j, products]
                bias = sign*(p[j, inverse_index]+p[j])
                factors.extend((base+bias, base-bias))
            factors = np.asarray(factors)
            _accumulate(full[b], _integer_multinomial_spectrum(factors, pair_weights))
            radii, bins = np.unique(np.abs(factors[:, ~diagonal]).sum(axis=0), return_inverse=True)
            tail_weights = np.zeros(len(radii), dtype=np.int64)
            np.add.at(tail_weights, bins, np.abs(pair_weights[~diagonal]))
            _accumulate(tails[b], tuple((int(r), int(w)) for r, w in zip(radii, tail_weights)))
            if any(r > 4*order for r, w in zip(radii, tail_weights) if w):
                raise ArithmeticError("streamed categorical kernel exceeded unit radius")

            # Independently form the source-discarded scalar kernel.
            scalar = order*(1+diagonal.astype(np.int64))
            bias = a[inverse_index]+a
            alpha, beta = scalar+bias, scalar-bias
            if not np.array_equal(alpha, factors[0]+factors[2]) or not np.array_equal(beta, factors[1]+factors[3]):
                raise ArithmeticError("streamed category marginal disagrees with the scalar weight kernel")
            negative_factors[b] += multiplicity*int(np.count_nonzero((alpha < 0) | (beta < 0)))
            _accumulate(weight_full[b], tuple(((r["alpha"], r["beta"]), r["weight"])
                for r in _integer_pair_spectrum(alpha, beta, pair_weights)))
            radii, bins = np.unique((np.abs(alpha)+np.abs(beta))[~diagonal], return_inverse=True)
            tail_weights = np.zeros(len(radii), dtype=np.int64)
            np.add.at(tail_weights, bins, np.abs(pair_weights[~diagonal]))
            _accumulate(weight_tails[b], tuple((int(r), int(w)) for r, w in zip(radii, tail_weights)))
            if any(2*int(r)**2 > (4*order)**2 for r, w in zip(radii, tail_weights) if w):
                raise ArithmeticError("streamed weight kernel exceeded the Bessel radius")
    mixtures, priors, weight_laws = [], [], []
    for b in (0, 1):
        p, a = projector_values[b], amplitudes[b]
        if int(a @ a) != (b+1)*order**2 or np.any(np.abs(a) > order):
            raise ArithmeticError("streamed coset mixture lost amplitude normalization")
        local = np.array([p[j, 0]+(-1)**bit * sign*p[j] for j, sign in enumerate((1, -1)) for bit in (0, 1)])
        if np.min(local) < 0 or np.any(local.sum(axis=0) != 2*order):
            raise ArithmeticError("streamed mixture has invalid local probabilities")
        mixtures.append(_integer_multinomial_spectrum(local, a**2))
        priors.append(tuple(Fraction(int(mass), order) for mass in p[:, 0]))
        weight_laws.append({"full_spectrum": [{"alpha": a0, "beta": b0, "weight": w} for (a0, b0), w in _freeze(weight_full[b])],
            "mixture_spectrum": _integer_pair_spectrum(order+a, order-a, a**2),
            "mixture_weight_denominator": (b+1)*order**2,
            "remainder_spectrum": [{"radius_numerator": r, "absolute_weight": w} for r, w in _freeze(weight_tails[b])],
            "negative_local_factor_count": negative_factors[b], "signed_group_pair_weights_present": bool(np.any(coefficients < 0))})
    class_size = math.prod(range(1, n, 2))
    overlap = Fraction(sum(int(a)**2 * int(b)**2 for a, b in zip(coefficients, coefficients[translated])), order**4)
    cubic = Fraction(sum(int(a)**2 * abs(int(b)) for a, b in zip(coefficients, coefficients[translated])), order**3)
    if class_size*overlap > 1 or cubic**2 > overlap:
        raise ArithmeticError("streamed amplitude overlap bound failed")
    mixed = []
    for p in projectors:
        cross = Fraction(sum(int(a)**2 * int(b)**2 for a, b in zip(coefficients, p[translated])), order**4)
        q = Fraction(int(p[0]), order)
        if class_size*cross > q:
            raise ArithmeticError("streamed category overlap bound failed")
        mixed.append({"null_category_mass": str(q), "exact_mixed_overlap": str(cross)})
    pairs = len(orbits)*order
    metadata = {"degree": n, "rule": "phase_sign", "category_labels": [0, 1], "category_phases": [1, -1],
        "group_order": order, "hidden_class_size": class_size,
        "category_assignment_by_partition": [int(s < 0) for s in signs],
        "null_category_masses": [str(p) for p in priors[0]], "alternative_category_masses": [str(p) for p in priors[1]],
        "mixed_overlap_certificates": mixed, "full_signed_spectrum_sizes": [len(_freeze(row)) for row in full],
        "positive_mixture_spectrum_sizes": [len(row) for row in mixtures],
        "enumerated_group_pairs": pairs, "full_group_pairs_represented": order**2,
        "centralizer_orbit_count": len(orbits), "centralizer_generator_count": len(generators),
        "orbit_size_histogram": {str(size): count for size, count in sorted(Counter(map(len, orbits)).items())},
        "maximum_product_index_block_entries": order, "full_pair_matrix_allocated": False,
        "integer_accumulation_upper_bound": str(order**3), "int64_accumulation_range_verified": True,
        "exact_character_row_orthogonality_verified": True,
        "independent_two_quotient_characters_checked": len(partitions),
        "orbit_mass_exactly_charged": True, "same_hidden_member_in_every_copy": True,
        "is_polynomial_in_degree": False, "positive_mixture_is_exact_full_law": False,
        "classical_quantum_frontend_replacement": False}
    certificate = {"degree": n, "transposition_count": n//2, "phase_rule": "negative_character_reflection",
        "group_order": order, "kernel_denominator": 4*order, "weight_denominator": order**2,
        "null": weight_laws[0], "alternative": weight_laws[1], "exact_amplitude_overlap": str(overlap),
        "exact_cubic_overlap": str(cubic), "hidden_class_size": class_size,
        "class_overlap_bound_verified": True, "same_hidden_member_in_every_copy": True,
        "positive_mixture_is_full_law": False, "group_pairs_enumerated": pairs,
        "is_polynomial_in_group_degree": False, "classical_quantum_frontend_replacement": False}
    return metadata, tuple(_freeze(row) for row in full), tuple(mixtures), tuple(_freeze(row) for row in tails), tuple(priors), certificate


@lru_cache(maxsize=1)
def audit_streamed_source_orbits() -> dict:
    """Compare complete signed spectra, not only a few matching probabilities."""
    from coset_binary_carrier_instruments import _coarse_source_character_data, corrected_weight_character_certificate
    checked = []
    for n in (4, 6):
        orbit = source_orbit_character_data(n)
        full = _coarse_source_character_data(n, n//2)
        for j in range(1, 5):
            if orbit[j] != full[j]:
                raise ArithmeticError(f"S{n} orbit certificate field {j} differs from full pair enumeration")
        reference = corrected_weight_character_certificate(n, n//2)
        for hypothesis in ("null", "alternative"):
            if orbit[5][hypothesis] != reference[hypothesis]:
                raise ArithmeticError("independent scalar spectra disagree with full pair contraction")
        for key in ("exact_amplitude_overlap", "exact_cubic_overlap"):
            if orbit[5][key] != reference[key]:
                raise ArithmeticError("orbit overlap certificates disagree")
        checked.append({"degree": n, "orbit_count": orbit[0]["centralizer_orbit_count"],
            "streamed_pairs": orbit[0]["enumerated_group_pairs"], "full_pairs": len(matching_centralizer_orbits(n)[0])**2,
            "all_signed_spectra_and_remainders_identical": True})
    return {"controls": checked, "verified": True, "comparison_uses_exact_integers": True,
        "extends_to_growing_degree_algorithm": False, "formal_proof_verification": False}


def intermediate_copy_information_controls() -> list[dict]:
    """Charge lost information against the known raw support-rank comparison."""
    from coset_binary_carrier_instruments import coarse_source_joint_laws, _pair_event_count_baseline
    rows = []
    for copies in (7, 8, 10, 12, 14, 16):
        laws = coarse_source_joint_laws(8, 4, copies)[0]
        distance = sum(abs(laws[1][key]-laws[0][key]) for key in laws[0])/2
        raw_lower = max(Fraction(), 1-Fraction(105, 2**copies))
        baseline = _pair_event_count_baseline(8, 4, copies)[0]
        rows.append({"degree": 8, "copy_count": copies, "hidden_class_size": 105,
            "exact_paired_category_walsh_distance": str(distance),
            "paired_category_walsh_distance": float(distance),
            "raw_trace_distance_lower_bound": str(raw_lower),
            "raw_support_measurement_is_implemented": False,
            "exact_information_loss_lower_bound": str(max(Fraction(), raw_lower-distance)),
            "pair_event_count_distance": float(baseline), "ideal_paired_table_loses_to_pair_count": distance < baseline,
            "all_source_irrep_information_retained": False,
            "growing_degree_or_all_copy_no_go": False, "speedup_claim_allowed": False})
    return rows
