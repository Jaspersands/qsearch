"""Independent finite density-matrix audit of the affine phase instrument.

This enumerator is a diagnostic, not an efficient classical HSP algorithm.
Kraus operators take only public dimensions, scales and observed outcomes.
Hidden data is confined to source fixtures and expected-state comparisons.
"""
from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path

import numpy as np

from theorems.nil3_cocycle_receiver import free_two_step_three, potential_fixture
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/affine_phase_channel_audit.json"


def points(p, width):
    ring(p)
    if type(width) is not int or width < 1 or p**width > 125:
        raise ValueError("finite diagnostic requires 1 <= p**width <= 125")
    return tuple(product(range(p), repeat=width))


def span(p, width, basis):
    if any(len(v) != width or any(type(x) is not int or not 0 <= x < p for x in v)
           for v in basis):
        raise ValueError("canonical basis coordinates required")
    return frozenset(tuple(sum(c * v[j] for c, v in zip(cs, basis)) % p
                           for j in range(width))
                     for cs in product(range(p), repeat=len(basis)))


def coset_vectors(p, width, basis, phases):
    """Truth fixture: one normalized ket for each ambient representative."""
    ambient = points(p, width)
    if len(phases) != len(ambient):
        raise ValueError("one fixture phase per ambient point required")
    index = {q: i for i, q in enumerate(ambient)}
    subspace = span(p, width, basis)
    result = []
    for a in ambient:
        ket = np.zeros(len(ambient), dtype=complex)
        for v in subspace:
            q = tuple((x + y) % p for x, y in zip(a, v))
            j = index[q]
            ket[j] = np.exp(2j * np.pi * (int(phases[j]) % p) / p) / np.sqrt(len(subspace))
        result.append(ket)
    return result


def coset_mixture(p, width, basis, phases):
    kets = coset_vectors(p, width, basis, phases)
    return sum(np.outer(ket, ket.conj()) for ket in kets) / len(kets)


def shear_indices(p, width, scales, outcomes):
    """Input basis addresses selected by each output row of a public K_y."""
    ambient = points(p, width)
    if not scales or len(scales) != len(outcomes):
        raise ValueError("matching nonempty scales and outcomes required")
    if any(type(c) is not int or not 0 <= c < p for c in scales):
        raise ValueError("canonical scales required")
    index = {q: i for i, q in enumerate(ambient)}
    if any(tuple(y) not in index for y in outcomes):
        raise ValueError("canonical outcomes required")
    dimension = len(ambient)
    if dimension**len(scales) > 2000:
        raise ValueError("finite input Hilbert dimension exceeds diagnostic cap")
    rows = []
    for x in ambient:
        address = 0
        for c, y in zip(scales, outcomes):
            q = tuple((yj + c * xj) % p for xj, yj in zip(x, y))
            address = address * dimension + index[q]
        rows.append(address)
    return np.asarray(rows, dtype=int)


def kraus(p, width, scales, outcomes):
    rows = shear_indices(p, width, scales, outcomes)
    dimension = len(rows)
    result = np.zeros((dimension, dimension**len(scales)), dtype=complex)
    result[np.arange(dimension), rows] = 1 / np.sqrt(dimension)
    return result


def branch(p, width, scales, outcomes, density):
    """K_y rho K_y^dagger by address selection, including all-zero scales."""
    rows = shear_indices(p, width, scales, outcomes)
    if density.shape != (len(rows)**len(scales),) * 2:
        raise ValueError("density dimension does not match source registers")
    return density[np.ix_(rows, rows)] / len(rows)


def translated_phases(p, width, scales, outcomes, phase_tables):
    """Expected-state fixture only; the public channel does not read phases."""
    ambient = points(p, width)
    index = {q: i for i, q in enumerate(ambient)}
    return [sum(table[index[tuple((yj + c*xj) % p for xj, yj in zip(x, y))]]
                for c, y, table in zip(scales, outcomes, phase_tables)) % p
            for x in ambient]


def partial_qft_mixed_source(group, hidden_log):
    """Enumerate actual rho_H edges g -> g*h^t, then Fourier-transform N.

    No potential, affine-support formula or pure-state phase receiver is
    used to build this source. Blocks remain subnormalized measurement
    branches. The positive Fourier sign matches the receiver convention.
    """
    p, m, n = group.p, group.m, group.n
    if p**group.dimension > 4000:
        raise ValueError("group enumeration exceeds diagnostic cap")
    if len(hidden_log) != group.dimension or not any(hidden_log[:m]):
        raise ValueError("nonzero quotient image required for this source audit")
    quotient = points(p, m)
    index = {q: i for i, q in enumerate(quotient)}
    normal_size, group_size = p**n, p**group.dimension
    counts = np.zeros((len(quotient), len(quotient)) + (p,) * n, dtype=np.int64)
    powers = [group.scale(t, hidden_log) for t in range(p)]
    for g in product(range(p), repeat=group.dimension):
        q, a = group.to_chart(g)
        for h in powers:
            r, b = group.to_chart(group.bch(g, h))
            delta = tuple((x - y) % p for x, y in zip(a, b))
            counts[(index[q], index[r]) + delta] += 1
    axes = tuple(range(2, 2 + n))
    # ifft includes 1/|N|, which is exactly the partial-QFT normalization.
    transformed = np.fft.ifftn(counts, axes=axes) / group_size
    return {label: transformed[(slice(None), slice(None)) + label]
            for label in product(range(p), repeat=n)}


def controls():
    p, width = 3, 2
    ambient = points(p, width)
    dimension = len(ambient)
    basis = [(1, 1)]
    phases = [[(x*x + x*y + y) % p for x, y in ambient],
              [(2*x + y*y) % p for x, y in ambient]]
    sources = [coset_mixture(p, width, basis, table) for table in phases]
    density = np.kron(*sources)
    scales = (1, 2)
    expected_probability = dimension**-2
    completeness = np.zeros_like(density)
    max_posterior_error = 0.0
    max_probability_error = 0.0
    max_address_error = 0.0
    for outcomes in product(ambient, repeat=2):
        operator = kraus(p, width, scales, outcomes)
        completeness += operator.conj().T @ operator
        actual = operator @ density @ operator.conj().T
        selected = branch(p, width, scales, outcomes, density)
        max_address_error = max(max_address_error, float(np.max(abs(actual - selected))))
        probability = float(np.trace(actual).real)
        expected_phases = translated_phases(p, width, scales, outcomes, phases)
        expected = coset_mixture(p, width, basis, expected_phases)
        max_probability_error = max(max_probability_error, abs(probability - expected_probability))
        max_posterior_error = max(max_posterior_error,
                                  float(np.max(abs(actual / probability - expected))))

    zero = [0] * dimension
    phase_free = coset_mixture(p, width, basis, zero)
    outcome = ((0, 0), (0, 0))
    dephased = np.eye(dimension**2) / dimension**2
    dephased_output = branch(p, width, scales, outcome, dephased) / expected_probability
    all_zero_output = branch(p, width, (0, 0), outcome, density) / expected_probability
    kets = coset_vectors(p, width, basis, zero)
    correlated = sum(np.outer(np.kron(v, v), np.kron(v, v).conj())
                     for v in kets) / dimension
    correlated_probabilities = [float(np.trace(branch(
        p, width, (1, 1), ys, correlated)).real) for ys in product(ambient, repeat=2)]

    group = free_two_step_three(5)
    hidden = (1, 2, 3, 4, 0)
    blocks = partial_qft_mixed_source(group, hidden)
    qpoints = points(5, 2)
    potentials = [potential_fixture(group, hidden, q) for q in qpoints]
    source_error = 0.0
    source_probability_error = 0.0
    for label, block in blocks.items():
        probability = float(np.trace(block).real)
        source_probability_error = max(source_probability_error, abs(probability - 5**-3))
        table = [sum(a*b for a, b in zip(label, value)) % 5 for value in potentials]
        expected = coset_mixture(5, 2, [hidden[:2]], table)
        source_error = max(source_error, float(np.max(abs(block / probability - expected))))

    checks = {
        "kraus_completeness_error": float(np.max(abs(completeness - np.eye(dimension**2)))),
        "explicit_kraus_vs_address_error": max_address_error,
        "all_outcome_probability_error": max_probability_error,
        "all_outcome_posterior_error": max_posterior_error,
        "dephased_output_vs_maximally_mixed_error": float(np.max(abs(
            dephased_output - np.eye(dimension) / dimension))),
        "all_zero_output_vs_uniform_pure_error": float(np.max(abs(
            all_zero_output - np.ones((dimension, dimension)) / dimension))),
        "mixed_hsp_partial_qft_probability_error": source_probability_error,
        "mixed_hsp_partial_qft_posterior_error": source_error,
    }
    if max(checks.values()) > 1e-10:
        raise ArithmeticError(f"density-matrix audit failed: {checks}")
    zero_outcomes = sum(value < 1e-12 for value in correlated_probabilities)
    if zero_outcomes != 54 or np.max(abs(all_zero_output - phase_free)) < 0.1:
        raise ArithmeticError("negative controls failed to distinguish their promises")
    return {
        "id": "AFFINE-PHASE-MIXED-CHANNEL-AUDIT",
        "status": "local-exact-derivation-with-independent-finite-controls",
        "errors": checks,
        "instrument": {"p": p, "width": width, "inputs": 2, "outcomes_checked": dimension**2,
                       "all_outcomes_retained": True, "nonzero_scale_required": True,
                       "hidden_data_supplied_to_kraus_operator": False},
        "source": {"group_order": 5**5, "partial_qft_labels_checked": len(blocks),
                   "constructed_from_mixed_hsp_edges": True, "pure_state_receiver_used": False},
        "negative_controls": {
            "dephased_sources_lose_line_information": True,
            "all_zero_scales_return_uniform_pure_not_coset_mixture": True,
            "correlated_coset_sources_violate_uniform_transcript_promise": True,
            "correlated_zero_probability_outcomes": zero_outcomes,
            "correlated_nonzero_outcome_probability": max(correlated_probabilities),
        },
        "source_assumptions": [
            "Independent standard mixed coset inputs, with unused oracle labels discarded.",
            "A single fixed subgroup and potential, with measured Fourier labels retained.",
            "Public adaptivity on prior transcript; disjoint source batches.",
        ],
        "scope": {
            "symbolic_all_prime_schedule_uses_published_sde_solvers": True,
            "general_prime_sde_solver_implemented_here": False,
            "existing_receiver_prime_congruence_restriction_unchanged": True,
            "arbitrary_external_reference_decoupling_proved": False,
            "black_box_to_lie_bridge_audited": False,
            "novelty_established": False,
            "compiled_quantum_algorithm_executed": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = controls()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        REPORT.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
