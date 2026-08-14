"""Base sign-orbit tetrahedral information is a coarse A_n law.

For every ``S_n`` partition ``lambda``, transposition tensors its irrep with
sign.  Averaging normalized characters over a two-element sign orbit gives

    (r_lambda(w)+r_(lambda^T)(w))/2 = 1[w in A_n] r_lambda(w).

For a self-conjugate partition the normalized character already vanishes on
odd permutations, so the same formula holds after the fair orientation lift.
In the tetrahedral word tuple ``(g,h,k,gk,hk,ghk)``, all six words are even if
and only if ``g,h,k`` are even.  Thus averaging the physical six-label
likelihood over all orientations gives exactly

    L_O = sum_(g,h,k in A_n) product_i r_(O_i)(W_i(g,h,k)).          (1)

The sign orbits are exactly coarse irreducible labels for ``A_n``:

* a non-self-conjugate pair restricts to one irreducible of dimension d;
* a self-conjugate ``S_n`` irrep splits into two ``A_n`` irreps of dimension
  d/2, which are merged by the coarse label.

Their coarse ``A_n`` Plancherel weights equal the sign-orbit ``S_n`` weights.
Consequently the base term in the exact KL chain is the relative entropy of a
coarse alternating-group tetrahedral law.  This moves the asymptotic question
from an ad hoc quotient to a standard finite simple group family.

The reduction does not prove that the coarse ``A_n`` law mixes.  Its merged
trivial/sign orbit becomes the single trivial ``A_n`` label and still creates
a factorially rare likelihood tail, so dimension-trimmed TV/KL remains the
correct metric.  Coherent multiplicity information is outside the law.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_sign_orbit_kl_chain_reduction import (
    partition_sign_orbits,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import transpose_partition
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
    tetrahedral_class_signature_counts,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_alternating_base_orbit_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-BASE-ORBIT-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
SignOrbit = tuple[Partition, ...]


@dataclass(frozen=True)
class AlternatingBaseOrbitControl:
    n: int
    symmetric_group_order: int
    alternating_group_order: int
    partition_count: int
    coarse_alternating_label_count: int
    nonself_restriction_label_count: int
    merged_split_label_count: int
    exact_coarse_plancherel_probability_sum: float
    maximum_coarse_plancherel_weight_residual: float
    direct_even_input_triple_count: int
    expected_even_input_triple_count: int
    maximum_base_likelihood_residual: float
    base_probability_sum_residual: float
    base_sign_orbit_kl_bits: float
    full_six_label_kl_bits: float
    base_fraction_of_full_kl: float
    coarse_trivial_label_product_mass: float
    coarse_trivial_label_physical_mass: float
    exact_coarse_trivial_physical_mass: float
    exact_alternating_group_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class AlternatingBaseOrbitReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[AlternatingBaseOrbitControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def permutation_parity_from_cycle_type(cycle_type: Partition) -> int:
    """Return zero for even permutations and one for odd permutations."""

    return (sum(cycle_type) - len(cycle_type)) % 2


def coarse_alternating_plancherel_weights(
    n: int,
) -> tuple[tuple[SignOrbit, ...], dict[SignOrbit, float]]:
    partitions = tuple(integer_partitions(n))
    weights = dict(zip(partitions, map(float, plancherel_weights(n))))
    orbits = partition_sign_orbits(partitions)
    return orbits, {
        orbit: sum(weights[partition] for partition in orbit)
        for orbit in orbits
    }


def even_word_base_likelihood_array(
    n: int,
) -> tuple[tuple[SignOrbit, ...], np.ndarray, int]:
    """Evaluate equation (1) through even class signatures."""

    if not 2 <= n <= 5:
        raise ValueError("exact even-word arrays require 2<=n<=5")
    classes = tuple(integer_partitions(n))
    class_index = {cycle_type: position for position, cycle_type in enumerate(classes)}
    orbits, _weights = coarse_alternating_plancherel_weights(n)
    representatives = tuple(orbit[0] for orbit in orbits)
    ratios = np.asarray(
        [
            [
                symmetric_character(partition, cycle_type)
                / hook_length_dimension(partition)
                for cycle_type in classes
            ]
            for partition in representatives
        ],
        dtype=float,
    )
    likelihood = np.zeros((len(orbits),) * 6, dtype=float)
    even_count = 0
    for signature, count in tetrahedral_class_signature_counts(n).items():
        # Signature order is (g,h,k,gk,hk,ghk).  The first three being even is
        # equivalent to all six being even.
        if any(permutation_parity_from_cycle_type(cycle_type) for cycle_type in signature[:3]):
            continue
        if any(permutation_parity_from_cycle_type(cycle_type) for cycle_type in signature):
            raise AssertionError("even input words produced an odd product word")
        even_count += count
        indices = tuple(class_index[cycle_type] for cycle_type in signature)
        vectors = (
            ratios[:, indices[3]],
            ratios[:, indices[5]],
            ratios[:, indices[4]],
            ratios[:, indices[0]],
            ratios[:, indices[1]],
            ratios[:, indices[2]],
        )
        likelihood += count * np.einsum(
            "a,b,c,d,e,f->abcdef",
            *vectors,
            optimize=False,
        )
    likelihood[np.abs(likelihood) < 1e-10] = 0.0
    return orbits, likelihood, even_count


def aggregate_sign_orbit_law(
    n: int,
) -> tuple[tuple[SignOrbit, ...], np.ndarray, np.ndarray, np.ndarray]:
    partitions, _likelihood, product, physical = finite_physical_likelihood_arrays(n)
    orbits = partition_sign_orbits(partitions)
    orbit_index = {
        partition: position
        for position, orbit in enumerate(orbits)
        for partition in orbit
    }
    shape = (len(orbits),) * 6
    product_orbit = np.zeros(shape, dtype=float)
    physical_orbit = np.zeros(shape, dtype=float)
    for indices in np.ndindex(product.shape):
        target = tuple(orbit_index[partitions[index]] for index in indices)
        product_orbit[target] += float(product[indices])
        physical_orbit[target] += float(physical[indices])
    likelihood_orbit = np.divide(
        physical_orbit,
        product_orbit,
        out=np.zeros_like(physical_orbit),
        where=product_orbit > 0,
    )
    return orbits, likelihood_orbit, product_orbit, physical_orbit


def audit_alternating_base_orbit_reduction(
    n: int,
) -> AlternatingBaseOrbitControl:
    if not 2 <= n <= 5:
        raise ValueError("exact alternating controls require 2<=n<=5")
    partitions, full_likelihood, full_product, full_physical = (
        finite_physical_likelihood_arrays(n)
    )
    orbits, base_likelihood, base_product, base_physical = aggregate_sign_orbit_law(n)
    even_orbits, even_likelihood, even_count = even_word_base_likelihood_array(n)
    if orbits != even_orbits:
        raise AssertionError("coarse orbit order mismatch")
    _, coarse_weights = coarse_alternating_plancherel_weights(n)
    symmetric_weights = dict(zip(partitions, map(float, plancherel_weights(n))))
    weight_residual = max(
        abs(coarse_weights[orbit] - sum(symmetric_weights[p] for p in orbit))
        for orbit in orbits
    )
    likelihood_residual = float(np.max(np.abs(base_likelihood - even_likelihood)))
    base_positive = base_physical > 0
    base_kl = float(
        np.sum(base_physical[base_positive] * np.log2(base_likelihood[base_positive]))
    )
    full_positive = full_physical > 0
    full_kl = float(
        np.sum(full_physical[full_positive] * np.log2(full_likelihood[full_positive]))
    )
    trivial_orbit = tuple(sorted({(n,), (1,) * n}))
    trivial_position = orbits.index(trivial_orbit)
    trivial_index = (trivial_position,) * 6
    order_a = math.factorial(n) // 2
    exact_trivial = 1.0 / order_a**3
    tolerance = 1e-8
    exact = bool(
        abs(sum(coarse_weights.values()) - 1.0) <= tolerance
        and weight_residual <= tolerance
        and even_count == order_a**3
        and likelihood_residual <= tolerance
        and abs(float(np.sum(base_physical)) - 1.0) <= tolerance
        and abs(base_product[trivial_index] - 1.0 / order_a**6) <= tolerance
        and abs(base_physical[trivial_index] - exact_trivial) <= tolerance
    )
    return AlternatingBaseOrbitControl(
        n=n,
        symmetric_group_order=math.factorial(n),
        alternating_group_order=order_a,
        partition_count=len(partitions),
        coarse_alternating_label_count=len(orbits),
        nonself_restriction_label_count=sum(len(orbit) == 2 for orbit in orbits),
        merged_split_label_count=sum(len(orbit) == 1 for orbit in orbits),
        exact_coarse_plancherel_probability_sum=sum(coarse_weights.values()),
        maximum_coarse_plancherel_weight_residual=weight_residual,
        direct_even_input_triple_count=even_count,
        expected_even_input_triple_count=order_a**3,
        maximum_base_likelihood_residual=likelihood_residual,
        base_probability_sum_residual=abs(float(np.sum(base_physical)) - 1.0),
        base_sign_orbit_kl_bits=max(0.0, base_kl),
        full_six_label_kl_bits=max(0.0, full_kl),
        base_fraction_of_full_kl=(base_kl / full_kl if full_kl > 0 else 0.0),
        coarse_trivial_label_product_mass=float(base_product[trivial_index]),
        coarse_trivial_label_physical_mass=float(base_physical[trivial_index]),
        exact_coarse_trivial_physical_mass=exact_trivial,
        exact_alternating_group_reduction_verified=exact,
        status=(
            "exact-coarse-alternating-tetrahedral-law-verified"
            if exact
            else "alternating-base-orbit-control-failure"
        ),
    )


def run_alternating_base_orbit_reduction(
) -> AlternatingBaseOrbitReductionReport:
    controls = [audit_alternating_base_orbit_reduction(n) for n in range(2, 6)]
    exact = all(row.exact_alternating_group_reduction_verified for row in controls)
    tail = controls[-1]
    return AlternatingBaseOrbitReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "sign_orbit_character_average": (
                "(r_lambda(w)+r_(lambda^T)(w))/2=1[w in A_n]r_lambda(w); "
                "self-conjugate characters vanish on odd w."
            ),
            "word_parity_restriction": (
                "All six tetrahedral words are even iff the independent inputs g,h,k "
                "belong to A_n."
            ),
            "coarse_label_identification": (
                "Nonself sign pairs restrict to one A_n irrep; self-conjugate labels "
                "split into two equal-dimensional A_n irreps and are merged."
            ),
            "plancherel_identity": (
                "The resulting coarse A_n Plancherel weights equal S_n sign-orbit weights."
            ),
            "base_law_identity": (
                "The base sign-orbit law is exactly the coarse A_n tetrahedral "
                "weak-Fourier law."
            ),
            "scope": (
                "No mixing, positive-mass, coherent-transform, or complexity theorem "
                "for the coarse A_n law follows from the reduction alone."
            ),
        },
        exact_controls=controls,
        proof_obligations=[
            {
                "obligation": "identify_base_sign_orbit_law_as_standard_group_object",
                "resolved": exact,
                "resolution": (
                    "Character averaging restricts all word inputs to A_n and the orbit "
                    "weights match coarse A_n Plancherel exactly."
                ),
            },
            {
                "obligation": "retain_self_conjugate_labels_without_assumption",
                "resolved": exact,
                "resolution": (
                    "Their A_n split pair is merged with exactly the original S_n "
                    "Plancherel mass; no label is discarded."
                ),
            },
            {
                "obligation": "bound_dimension_trimmed_coarse_An_tetrahedral_kl",
                "resolved": False,
                "resolution": (
                    "Establish high-dimensional six-word mixing for A_n or identify a "
                    "positive-mass coarse irrep family."
                ),
            },
            {
                "obligation": "compare_coarse_An_signal_with_classical_word_map_sampling",
                "resolved": False,
                "resolution": (
                    "Any survivor has a classical dual using three uniform A_n elements; "
                    "match access and computation costs before a quantum claim."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The sign-orbit quotient is an artificial S_n construction.",
                "resolved": True,
                "resolution": (
                    "False: it is precisely coarse weak Fourier sampling over A_n."
                ),
            },
            {
                "objection": "Self-conjugate partitions invalidate the A_n reduction.",
                "resolved": True,
                "resolution": (
                    "False: restriction splits them into an equal-dimensional pair whose "
                    "merged normalized character and Plancherel mass are exact."
                ),
            },
            {
                "objection": "A_n simplicity or quasirandomness proves the base law mixes.",
                "resolved": True,
                "resolution": (
                    "False: the six correlated word values require a dimension-trimmed "
                    "high-level Fourier estimate not supplied by minimal degree alone."
                ),
            },
            {
                "objection": "Removing sign representations removes all rare L2 tails.",
                "resolved": True,
                "resolution": (
                    "False: the merged trivial/sign orbit is the trivial A_n label and has "
                    "physical all-six mass |A_n|^-3 with likelihood |A_n|^3."
                ),
            },
        ],
        headline_metrics={
            "coarse_alternating_group_reduction_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                row.status != "exact-coarse-alternating-tetrahedral-law-verified"
                for row in controls
            ),
            "maximum_base_likelihood_residual": max(
                row.maximum_base_likelihood_residual for row in controls
            ),
            "S5_coarse_alternating_label_count": tail.coarse_alternating_label_count,
            "S5_base_sign_orbit_kl_bits": tail.base_sign_orbit_kl_bits,
            "S5_base_fraction_of_full_kl": tail.base_fraction_of_full_kl,
            "dimension_trimmed_An_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "base_sign_orbit_law_equals_coarse_An_law_proved": exact,
            "self_conjugate_labels_handled_exactly": exact,
            "dimension_trimmed_coarse_An_kl_vanishes_proved": False,
            "dimension_trimmed_coarse_An_signal_survives_proved": False,
            "classical_separation_proved": False,
            "coherent_multiplicity_signal_absent_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The base term is now a standard coarse A_n word-map law, but its "
                "high-dimensional mixing and computational value remain unproved."
            ),
        },
        status=(
            "base-sign-orbit-law-reduced-to-coarse-alternating-group"
            if exact
            else "alternating-base-orbit-control-failure"
        ),
        summary=(
            "Identified the entire base sign-orbit tetrahedral law with coarse "
            "alternating-group weak Fourier sampling."
        ),
        falsifiers_triggered=[
            "The sign-orbit quotient is not a new group family; it is coarse A_n Fourier data.",
            "A_n removes the sign character but retains a rare trivial-label L2 tail.",
            "Any base-orbit survivor has an explicit classical A_n word-map dual.",
        ],
    )


def write_alternating_base_orbit_reduction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_alternating_base_orbit_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_alternating_base_orbit_reduction_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
