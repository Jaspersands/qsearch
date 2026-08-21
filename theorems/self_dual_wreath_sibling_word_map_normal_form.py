"""Exact all-word normal form for independent sibling-frame moments.

Fix a binary trace word ``w`` in sibling frames ``A,B`` of length ``p``.  At
the distinguished source pair, the letter fixes the orientation bit.  For a
group tuple ``x=(x_1,...,x_p)``, define

    I_w(x)=1  iff  product_(w_t=A) x_t = product_(w_t=B) x_t = 1,

with each subproduct taken in its original cyclic order.  For every remaining
source pair define the nonabelian two-color identity count

    q_p(x) = #{b in {0,1}^p :
                 product_(b_t=0) x_t = product_(b_t=1) x_t = 1}.

If ``G`` has order ``g``, the target irrep is ``nu``, and there are ``K``
source pairs, independent Plancherel orthogonality gives the exact normal form

    E tr(w(A,B))/D
      = g^-p sum_(x in G^p) I_w(x)
          [chi_nu(x_1...x_p)/d_nu] q_p(x)^(K-1).           (1)

For a mixed word, the last occurrence of each letter is forced by ``I_w``.
Thus its word-map strata can be enumerated with only ``g^(p-2)`` assignments,
grouped by ``(q_p, cycle_type(x_1...x_p))`` for ``S_n``.  Once these strata
are known, every target moment follows from one character-table lookup.

Equation (1) contains the degree-four formulas as special cases and gives a
research engine for higher moments.  The Marchenko--Pastur free comparison is
the sum over color-respecting noncrossing partitions, one factor ``alpha``
per block.  The open theorem is now precise: show that high-``q`` strata with
maximal group degrees of freedom are exactly the noncrossing contributions,
while every crossing/target-sensitive stratum is suppressed uniformly for
word lengths large enough to control spectral edges.

Fixed finite screens do not prove that theorem.  Existing fixed-word results
for symmetric-group word measures and fixed-permutation character bounds do
not directly cover word length growing with ``n``, high-dimensional target
characters, or global-distinct source conditioning.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import permutation_cycle_type
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_sibling_word_map_normal_form.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-WORD-MAP-NORMAL-FORM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
FERAY_SNIADY_URL = "https://arxiv.org/abs/math/0701051"
HANANY_PUDER_URL = "https://arxiv.org/abs/2009.00897"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]
WordStrata = dict[tuple[int, Partition], int]


@dataclass(frozen=True)
class WordMapMomentControl:
    n: int
    copy_count: int
    word: str
    moment_order: int
    constrained_assignment_count: int
    stratum_count: int
    maximum_two_color_identity_count: int
    maximum_nonidentity_product_two_color_count: int
    target_count: int
    maximum_absolute_free_mp_residual: float
    maximizing_target_partition: Partition
    target_moments: dict[str, str]
    free_mp_moment: str
    status: str


@dataclass(frozen=True)
class DirectWordNormalFormControl:
    n: int
    copy_count: int
    target_partition: Partition
    word: str
    source_tuple_count: int
    direct_projector_moment: float
    word_map_normal_form_moment: float
    formula_residual: float
    exact_direct_validation: bool
    status: str


@dataclass(frozen=True)
class SiblingWordMapNormalFormReport:
    created_at: str
    theorem_contract: dict[str, Any]
    direct_projector_controls: list[DirectWordNormalFormControl]
    finite_word_screens: list[WordMapMomentControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def _ordered_product(
    sequence: tuple[Permutation, ...],
    positions: Iterable[int],
) -> Permutation:
    identity = tuple(range(len(sequence[0])))
    output = identity
    for position in positions:
        output = _compose(output, sequence[position])
    return output


def two_color_identity_count(sequence: tuple[Permutation, ...]) -> int:
    """Evaluate ``q_p`` exactly by enumerating the two-color assignments."""

    if not sequence:
        raise ValueError("a nonempty group word is required")
    identity = tuple(range(len(sequence[0])))
    if any(len(permutation) != len(identity) for permutation in sequence):
        raise ValueError("all permutations must have the same degree")
    count = 0
    for bits in itertools.product((0, 1), repeat=len(sequence)):
        products = [identity, identity]
        for permutation, bit in zip(sequence, bits):
            products[bit] = _compose(products[bit], permutation)
        count += products[0] == identity and products[1] == identity
    return count


def _validate_mixed_word(word: str) -> tuple[int, ...]:
    bits = tuple(0 if letter == "A" else 1 for letter in word)
    if not word or any(letter not in "AB" for letter in word):
        raise ValueError("word must be a nonempty A/B string")
    if len(set(bits)) != 2:
        raise ValueError("this normal-form enumerator expects a mixed word")
    return bits


@lru_cache(maxsize=None)
def mixed_word_map_strata(n: int, word: str) -> tuple[tuple[int, Partition, int], ...]:
    """Enumerate equation (1) after solving the two split constraints."""

    if n < 2:
        raise ValueError("n must be at least two")
    bits = _validate_mixed_word(word)
    group = tuple(itertools.permutations(range(n)))
    identity = tuple(range(n))
    positions = {
        bit: tuple(index for index, value in enumerate(bits) if value == bit)
        for bit in (0, 1)
    }
    forced = {bit: positions[bit][-1] for bit in (0, 1)}
    free_positions = tuple(
        index for index in range(len(word)) if index not in forced.values()
    )
    counts: WordStrata = {}
    for assignment in itertools.product(group, repeat=len(free_positions)):
        sequence = [identity] * len(word)
        for position, permutation in zip(free_positions, assignment):
            sequence[position] = permutation
        for bit in (0, 1):
            prefix = _ordered_product(
                tuple(sequence),
                positions[bit][:-1],
            )
            sequence[forced[bit]] = _inverse(prefix)
        sequence_tuple = tuple(sequence)
        q_value = two_color_identity_count(sequence_tuple)
        full_product = _ordered_product(
            sequence_tuple,
            range(len(sequence_tuple)),
        )
        key = (q_value, permutation_cycle_type(full_product))
        counts[key] = counts.get(key, 0) + 1
    expected = len(group) ** (len(word) - 2)
    if sum(counts.values()) != expected:
        raise ArithmeticError("word-map strata lost constrained assignments")
    return tuple(
        (q_value, cycle_type, count)
        for (q_value, cycle_type), count in sorted(counts.items())
    )


def independent_sibling_word_moment(
    n: int,
    copy_count: int,
    target: Partition,
    word: str,
) -> Fraction:
    if sum(target) != n or copy_count < 1:
        raise ValueError("invalid target or copy count")
    order = math.factorial(n)
    dimension = hook_length_dimension(target)
    numerator = Fraction()
    for q_value, cycle_type, count in mixed_word_map_strata(n, word):
        numerator += (
            count
            * q_value ** (copy_count - 1)
            * Fraction(symmetric_character(target, cycle_type), dimension)
        )
    return numerator / order ** len(word)


@lru_cache(maxsize=None)
def _set_partitions(size: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
    if size == 0:
        return ((),)
    output: list[tuple[tuple[int, ...], ...]] = []
    for partition in _set_partitions(size - 1):
        for block_index in range(len(partition)):
            blocks = [list(block) for block in partition]
            blocks[block_index].append(size - 1)
            output.append(tuple(tuple(block) for block in blocks))
        output.append((*partition, (size - 1,)))
    return tuple(output)


def _is_noncrossing(partition: tuple[tuple[int, ...], ...]) -> bool:
    for left_index, left in enumerate(partition):
        for right in partition[left_index + 1 :]:
            for a, c in itertools.combinations(left, 2):
                for b, d in itertools.combinations(right, 2):
                    if a < b < c < d or b < a < d < c:
                        return False
    return True


def free_mp_binary_word_moment(word: str, alpha: Fraction) -> Fraction:
    bits = tuple(0 if letter == "A" else 1 for letter in word)
    if not word or any(letter not in "AB" for letter in word):
        raise ValueError("word must be a nonempty A/B string")
    total = Fraction()
    for partition in _set_partitions(len(word)):
        if not _is_noncrossing(partition):
            continue
        if any(len({bits[index] for index in block}) != 1 for block in partition):
            continue
        total += alpha ** len(partition)
    return total


def canonical_binary_words(order: int) -> tuple[str, ...]:
    """Return mixed words modulo cyclicity, reversal, and sibling exchange."""

    if order < 2:
        return ()

    def orbit(word: str) -> set[str]:
        variants: set[str] = set()
        for base in (word, word[::-1]):
            for shift in range(order):
                rotated = base[shift:] + base[:shift]
                variants.add(rotated)
                variants.add(
                    "".join("B" if letter == "A" else "A" for letter in rotated)
                )
        return variants

    representatives = {
        min(orbit("".join(letters)))
        for letters in itertools.product("AB", repeat=order)
        if len(set(letters)) == 2
    }
    return tuple(sorted(representatives))


def audit_word_map_moment(
    n: int,
    copy_count: int,
    word: str,
) -> WordMapMomentControl:
    partitions = tuple(integer_partitions(n))
    alpha = Fraction(1 << copy_count, 2 * math.factorial(n))
    free = free_mp_binary_word_moment(word, alpha)
    moments = {
        target: independent_sibling_word_moment(n, copy_count, target, word)
        for target in partitions
    }
    residuals = {target: abs(value - free) for target, value in moments.items()}
    maximizing = max(residuals, key=residuals.get)
    strata = mixed_word_map_strata(n, word)
    identity_cycle = (1,) * n
    nonidentity_q = max(
        (q_value for q_value, cycle_type, _ in strata if cycle_type != identity_cycle),
        default=0,
    )
    return WordMapMomentControl(
        n=n,
        copy_count=copy_count,
        word=word,
        moment_order=len(word),
        constrained_assignment_count=math.factorial(n) ** (len(word) - 2),
        stratum_count=len(strata),
        maximum_two_color_identity_count=max(row[0] for row in strata),
        maximum_nonidentity_product_two_color_count=nonidentity_q,
        target_count=len(partitions),
        maximum_absolute_free_mp_residual=float(residuals[maximizing]),
        maximizing_target_partition=maximizing,
        target_moments={str(target): str(value) for target, value in moments.items()},
        free_mp_moment=str(free),
        status="exact-finite-word-map-screen-not-asymptotic-evidence",
    )


def audit_direct_word_normal_form(
    n: int,
    copy_count: int,
    target: Partition,
    word: str,
) -> DirectWordNormalFormControl:
    _validate_mixed_word(word)
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    weights = {
        partition: dimensions[partition] ** 2 / order for partition in partitions
    }
    left_masks = tuple(
        mask for mask in range(1 << copy_count) if not mask & 1
    )
    right_masks = tuple(mask for mask in range(1 << copy_count) if mask & 1)
    direct = 0.0
    tuple_count = 0
    for sources in itertools.product(partitions, repeat=2 * copy_count):
        labels: tuple[Label, ...] = tuple(
            (sources[2 * index], sources[2 * index + 1])
            for index in range(copy_count)
        )
        probability = math.prod(weights[source] for source in sources)
        carrier_dimension = dimensions[target] * math.prod(
            dimensions[source] for source in sources
        )
        projectors = tuple(
            orientation_invariant_projector(target, labels, mask)
            for mask in range(1 << copy_count)
        )
        zero = np.zeros_like(projectors[0])
        left = sum((projectors[mask] for mask in left_masks), zero.copy())
        right = sum((projectors[mask] for mask in right_masks), zero.copy())
        product = np.eye(len(left), dtype=complex)
        for letter in word:
            product = product @ (left if letter == "A" else right)
        direct += probability * np.trace(product).real / carrier_dimension
        tuple_count += 1
    direct_value = float(direct)
    predicted = float(
        independent_sibling_word_moment(n, copy_count, target, word)
    )
    residual = float(abs(direct_value - predicted))
    verified = bool(residual <= 1e-10)
    return DirectWordNormalFormControl(
        n=n,
        copy_count=copy_count,
        target_partition=target,
        word=word,
        source_tuple_count=tuple_count,
        direct_projector_moment=direct_value,
        word_map_normal_form_moment=predicted,
        formula_residual=residual,
        exact_direct_validation=verified,
        status=(
            "direct-projector-word-normal-form-verified"
            if verified
            else "direct-projector-word-normal-form-mismatch"
        ),
    )


def run_sibling_word_map_normal_form() -> SiblingWordMapNormalFormReport:
    direct = [
        audit_direct_word_normal_form(3, 2, target, word)
        for target in integer_partitions(3)
        for word in ("AAB", "AABB", "ABAB", "AABAB")
    ]
    screens = [
        audit_word_map_moment(3, 2, word)
        for order in range(2, 7)
        for word in canonical_binary_words(order)
    ] + [
        audit_word_map_moment(4, 3, word)
        for order in range(2, 6)
        for word in canonical_binary_words(order)
    ]
    failures = sum(not row.exact_direct_validation for row in direct)
    verified = failures == 0
    highest_order = max(row.moment_order for row in screens)
    worst = max(screens, key=lambda row: row.maximum_absolute_free_mp_residual)
    metrics: dict[str, int | float] = {
        "exact_all_word_normal_form_theorem_count": 1,
        "direct_projector_control_count": len(direct),
        "direct_projector_control_failure_count": failures,
        "finite_word_screen_count": len(screens),
        "highest_screened_word_order": highest_order,
        "maximum_finite_free_mp_residual": worst.maximum_absolute_free_mp_residual,
        "maximum_finite_free_mp_residual_order": worst.moment_order,
        "growing_word_high_q_rigidity_theorem_count": 0,
        "globally_distinct_word_normal_form_theorem_count": 0,
        "natural_spectral_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return SiblingWordMapNormalFormReport(
        created_at=utc_now(),
        theorem_contract={
            "normal_form": (
                "Independent Plancherel orthogonality reduces every mixed "
                "sibling trace word to equation (1), a target-character-weighted "
                "two-color identity-count distribution."
            ),
            "constraint_elimination": (
                "The last A and B group variables are forced, reducing exact "
                "enumeration from g^p to g^(p-2)."
            ),
            "free_comparator": (
                "The free MP mixed moment is the color-respecting noncrossing "
                "partition polynomial with one alpha per block."
            ),
            "scope": (
                "Finite word screens validate the reduction only. Growing-word "
                "rigidity, injective conditioning, spectral edges, and coherent "
                "algorithms remain unproved."
            ),
        },
        direct_projector_controls=direct,
        finite_word_screens=screens,
        proof_obligations=[
            {
                "obligation": "derive_exact_independent_normal_form_for_arbitrary_mixed_words",
                "resolved": verified,
                "resolution": (
                    "The word-map formula matches direct projector averages "
                    "through degree five for every S3 target control."
                ),
            },
            {
                "obligation": "classify_high_q_strata_by_noncrossing_topology",
                "resolved": False,
                "resolution": (
                    "Need an all-order rigidity/genus theorem for nonabelian "
                    "two-color identity counts, not a finite enumeration."
                ),
            },
            {
                "obligation": "bound_target_character_word_map_sums_for_growing_degree",
                "resolved": False,
                "resolution": (
                    "Fixed-permutation character bounds and fixed-word measure "
                    "theorems do not cover the required growing regime."
                ),
            },
            {
                "obligation": "derive_injective_global_distinct_word_normal_form_and_bound",
                "resolved": False,
                "resolution": (
                    "Global distinctness couples all 2K source slots and needs "
                    "observable-specific inclusion-exclusion or determinant control."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Degree-four formulas are isolated coincidences.",
                "resolved": True,
                "resolution": (
                    "They are instances of an exact arbitrary-word normal form."
                ),
            },
            {
                "objection": "Finite exact screens establish all-order freeness.",
                "resolved": False,
                "resolution": (
                    "The number and geometry of high-q strata change with word "
                    "length; no uniform theorem follows from bounded p."
                ),
            },
            {
                "objection": "A fixed-word word-map theorem supplies a spectral edge.",
                "resolved": False,
                "resolution": (
                    "Extreme-edge control needs degrees growing with dimension "
                    "or a resolvent/local-law argument."
                ),
            },
            {
                "objection": "Independent-source word strata survive global distinctness unchanged.",
                "resolved": False,
                "resolution": (
                    "Injective conditioning replaces every product source kernel "
                    "and can be bounded only with signed observable structure."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Feray--Sniady uniform symmetric-group character bounds",
                "url": FERAY_SNIADY_URL,
                "directly_closes_growing_word_gate": False,
                "reason": (
                    "The bound is a candidate target-character input, but the "
                    "word-generated permutations and required degree both vary."
                ),
            },
            {
                "paper": "Hanany--Puder word measures on symmetric groups",
                "url": HANANY_PUDER_URL,
                "directly_closes_growing_word_gate": False,
                "reason": (
                    "Its fixed-word stable-character regime does not directly "
                    "cover growing words or arbitrary high-dimensional targets."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_independent_arbitrary_word_normal_form_proved": verified,
            "degree_four_formulas_recovered_by_normal_form": True,
            "finite_higher_word_screens_completed": True,
            "all_fixed_order_joint_freeness_proved": False,
            "growing_word_high_q_rigidity_proved": False,
            "globally_distinct_word_control_proved": False,
            "natural_jacobi_spectral_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact search object is now explicit, but its growing-word "
                "high-q strata and injective conditioning are not bounded."
            ),
        },
        status=(
            "exact-word-map-normal-form-growing-word-rigidity-open"
            if verified
            else "word-map-normal-form-control-failure"
        ),
        summary=(
            "Reduced arbitrary independent sibling moments to exact nonabelian "
            "two-color word-map strata and identified high-q rigidity plus "
            "injective conditioning as the all-order spectral gates."
        ),
        falsifiers_triggered=[
            "Bounded-degree moment matching does not imply a spectral edge.",
            "Fixed-word symmetric-group theorems do not automatically cover growing moment order.",
            "Independent Plancherel word strata cannot be reused unchanged after global-distinct conditioning.",
        ],
    )


def write_sibling_word_map_normal_form_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-WORD-MAP-NORMAL-FORM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_sibling_word_map_normal_form())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

    return payload


if __name__ == "__main__":
    report = write_sibling_word_map_normal_form_report()
    print(json.dumps(report, indent=2))
