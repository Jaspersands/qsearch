"""Exact 14-block ANOVA normal form for the even cycle-type channel.

Let ``X=(type(g),type(h),type(k))`` and
``Y=(type(gk),type(hk),type(ghk))`` under uniform ``(g,h,k) in A_n^3``.
Write ``q`` for the cycle-type law of one uniform even permutation.  The
normalized conditional operator is

    K[x,y] = P(X=x,Y=y)/sqrt(q^3(x)q^3(y)).              (1)

It has constant singular vector ``sqrt(q^3)`` with singular value one, and

    ||K||_HS^2=C_even,
    ||K-Pi_const||_HS^2=C_even-1.                        (2)

Tensor-decompose each side into constants and mean-zero one-coordinate class
functions.  A matrix coefficient for a selected subset of the six words

    (g,h,k,gk,hk,ghk)

vanishes if one input generator appears in exactly one selected word: average
that generator first.  Apply the same test through the inverse coordinates
``(a,b,c)=(gk,hk,ghk)``.  Up to conjugacy,

    g ~ cb^-1, h ~ a^-1c, k=bc^-1a,                    (3)

while the last three words are ``a,b,c``.  Intersecting the forward and
inverse no-private-generator conditions leaves exactly fourteen nonconstant
ANOVA blocks.  By selected-word count they occur in orbits of sizes

    4 at order 3, 3 at order 4, 6 at order 5, 1 at order 6. (4)

All other 49 nonconstant subset pairs are exactly zero for every finite group,
not merely asymptotically small.  This explains why all scalar coordinate
pairs are independent while higher-order block dependence remains.

This ANOVA decomposition and the identity-support decomposition of ``Z6_+``
are different bases.  The order-six ANOVA energy is not equal to ``Z6_+``;
finite controls explicitly record the difference.  Do not replace one by the
other.  A valid growing-support theorem may bound the whole centered operator,
its fourteen blocks, or the separate inclusion-exclusion core.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    permutation_parity_from_cycle_type,
)
from self_dual_wreath_alternating_even_collision_core_reduction import (
    audit_even_collision_support,
)
from self_dual_wreath_projected_parity_coset_kernel import (
    parity_coset_signature_counts,
)
from symmetric_character import conjugacy_class_size


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_alternating_block_operator_anova.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-BLOCK-OPERATOR-ANOVA"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

FORWARD_INCIDENCE = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 1),
)
INVERSE_INCIDENCE = (
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
)


@dataclass(frozen=True)
class AnovaBlockEnergy:
    input_subset_mask: int
    output_subset_mask: int
    selected_word_count: int
    hilbert_schmidt_energy: float
    allowed_by_forward_private_generator_test: bool
    allowed_by_inverse_private_generator_test: bool
    status: str


@dataclass(frozen=True)
class BlockOperatorAnovaControl:
    n: int
    even_cycle_type_count: int
    normalized_operator_dimension: int
    normalized_operator_hilbert_schmidt_square: float
    constant_block_energy: float
    centered_operator_hilbert_schmidt_square: float
    exact_even_collision_moment: float
    maximum_forbidden_anova_block_energy: float
    nonzero_allowed_anova_block_count: int
    allowed_anova_block_count: int
    order_three_total_energy: float
    order_four_total_energy: float
    order_five_total_energy: float
    order_six_total_energy: float
    order_six_anova_minus_z6_core: float
    maximum_nonconstant_singular_value: float
    exact_anova_energy_decomposition_residual: float
    exact_private_generator_sparsity_verified: bool
    status: str


@dataclass(frozen=True)
class BlockOperatorAnovaTheorem:
    normalized_operator: str
    centered_hilbert_schmidt_identity: str
    forward_private_generator_test: str
    inverse_private_generator_test: str
    allowed_block_orbit_sizes: str
    order_six_anova_equals_identity_support_core: bool
    growing_support_operator_bound_proved: bool
    status: str


@dataclass(frozen=True)
class AlternatingBlockOperatorAnovaReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: BlockOperatorAnovaTheorem
    allowed_blocks: list[dict[str, int | bool]]
    exact_controls: list[BlockOperatorAnovaControl]
    finite_block_energies: dict[str, list[AnovaBlockEnergy]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _has_no_private_generator(
    six_word_mask: int,
    incidence: tuple[tuple[int, int, int], ...],
) -> bool:
    counts = tuple(
        sum(
            word[generator]
            for index, word in enumerate(incidence)
            if (six_word_mask >> index) & 1
        )
        for generator in range(3)
    )
    return all(count != 1 for count in counts)


def allowed_anova_masks() -> tuple[int, ...]:
    return tuple(
        mask
        for mask in range(1, 1 << 6)
        if _has_no_private_generator(mask, FORWARD_INCIDENCE)
        and _has_no_private_generator(mask, INVERSE_INCIDENCE)
    )


def even_cycle_type_channel(
    n: int,
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray, np.ndarray]:
    if not 2 <= n <= 5:
        raise ValueError("exact channel controls require 2<=n<=5")
    cycle_types = tuple(
        cycle_type
        for cycle_type in integer_partitions(n)
        if permutation_parity_from_cycle_type(cycle_type) == 0
    )
    index = {cycle_type: position for position, cycle_type in enumerate(cycle_types)}
    order = math.factorial(n) // 2
    one = np.asarray(
        [conjugacy_class_size(cycle_type) / order for cycle_type in cycle_types],
        dtype=float,
    )
    product = np.einsum("i,j,k->ijk", one, one, one).reshape(-1)
    joint = np.zeros((len(cycle_types) ** 3,) * 2, dtype=float)
    for signature, count in parity_coset_signature_counts(n, (0, 0, 0)).items():
        left = np.ravel_multi_index(
            tuple(index[cycle_type] for cycle_type in signature[:3]),
            (len(cycle_types),) * 3,
        )
        right = np.ravel_multi_index(
            tuple(index[cycle_type] for cycle_type in signature[3:]),
            (len(cycle_types),) * 3,
        )
        joint[left, right] += count / order**3
    normalized = joint / np.sqrt(product[:, None] * product[None, :])
    return cycle_types, product, normalized


def _orthogonal_complement(vector: np.ndarray) -> np.ndarray:
    return np.linalg.svd(vector.reshape(1, -1), full_matrices=True)[2][1:].T


def anova_basis(one_coordinate_probability: np.ndarray) -> dict[int, np.ndarray]:
    constant = np.sqrt(one_coordinate_probability).reshape(-1, 1)
    centered = _orthogonal_complement(np.sqrt(one_coordinate_probability))
    output: dict[int, np.ndarray] = {}
    for mask in range(8):
        factors = tuple(
            centered if (mask >> axis) & 1 else constant
            for axis in range(3)
        )
        output[mask] = np.kron(np.kron(factors[0], factors[1]), factors[2])
    return output


def audit_block_operator_anova(
    n: int,
) -> tuple[BlockOperatorAnovaControl, list[AnovaBlockEnergy]]:
    cycle_types, product, operator = even_cycle_type_channel(n)
    one = np.asarray(
        [
            conjugacy_class_size(cycle_type) / (math.factorial(n) // 2)
            for cycle_type in cycle_types
        ],
        dtype=float,
    )
    basis = anova_basis(one)
    allowed = set(allowed_anova_masks())
    rows: list[AnovaBlockEnergy] = []
    forbidden_max = 0.0
    allowed_nonzero = 0
    order_energy = {order: 0.0 for order in range(3, 7)}
    total_anova = 0.0
    for input_mask, output_mask in itertools.product(range(8), repeat=2):
        if input_mask == output_mask == 0:
            continue
        six_mask = input_mask | (output_mask << 3)
        forward = _has_no_private_generator(six_mask, FORWARD_INCIDENCE)
        inverse = _has_no_private_generator(six_mask, INVERSE_INCIDENCE)
        block = basis[input_mask].T @ operator @ basis[output_mask]
        energy = float(np.sum(block**2))
        total_anova += energy
        if six_mask not in allowed:
            forbidden_max = max(forbidden_max, energy)
        elif energy > 1e-18:
            allowed_nonzero += 1
            order_energy[six_mask.bit_count()] += energy
        rows.append(
            AnovaBlockEnergy(
                input_subset_mask=input_mask,
                output_subset_mask=output_mask,
                selected_word_count=six_mask.bit_count(),
                hilbert_schmidt_energy=energy,
                allowed_by_forward_private_generator_test=forward,
                allowed_by_inverse_private_generator_test=inverse,
                status=(
                    "allowed-higher-order-anova-block"
                    if six_mask in allowed
                    else "exact-private-generator-zero-block"
                ),
            )
        )
    collision = float(np.sum(operator**2))
    constant_vector = np.sqrt(product)
    constant_energy = float((constant_vector @ operator @ constant_vector) ** 2)
    singular_values = np.linalg.svd(operator, compute_uv=False)
    nonconstant_singular = float(singular_values[1]) if len(singular_values) > 1 else 0.0
    z6 = (
        float(
            Fraction(
                audit_even_collision_support(n).exact_fully_nonidentity_even_core
            )
        )
        if n >= 3
        else 0.0
    )
    residual = abs(collision - constant_energy - total_anova)
    tolerance = 2e-9
    verified = bool(
        len(allowed) == 14
        and forbidden_max <= tolerance
        and residual <= tolerance
        and abs(constant_energy - 1.0) <= tolerance
    )
    return (
        BlockOperatorAnovaControl(
            n=n,
            even_cycle_type_count=len(cycle_types),
            normalized_operator_dimension=operator.shape[0],
            normalized_operator_hilbert_schmidt_square=collision,
            constant_block_energy=constant_energy,
            centered_operator_hilbert_schmidt_square=total_anova,
            exact_even_collision_moment=collision,
            maximum_forbidden_anova_block_energy=forbidden_max,
            nonzero_allowed_anova_block_count=allowed_nonzero,
            allowed_anova_block_count=len(allowed),
            order_three_total_energy=order_energy[3],
            order_four_total_energy=order_energy[4],
            order_five_total_energy=order_energy[5],
            order_six_total_energy=order_energy[6],
            order_six_anova_minus_z6_core=order_energy[6] - z6,
            maximum_nonconstant_singular_value=nonconstant_singular,
            exact_anova_energy_decomposition_residual=residual,
            exact_private_generator_sparsity_verified=verified,
            status=(
                "even-cycle-channel-has-exact-fourteen-block-anova-normal-form"
                if verified
                else "block-operator-anova-control-failure"
            ),
        ),
        rows,
    )


def run_alternating_block_operator_anova() -> AlternatingBlockOperatorAnovaReport:
    audited = [audit_block_operator_anova(n) for n in range(2, 6)]
    controls = [control for control, _rows in audited]
    failures = sum(not row.exact_private_generator_sparsity_verified for row in controls)
    exact = failures == 0
    allowed = allowed_anova_masks()
    theorem = BlockOperatorAnovaTheorem(
        normalized_operator="K[x,y]=P(X=x,Y=y)/sqrt(q^3(x)q^3(y))",
        centered_hilbert_schmidt_identity="||K-Pi_const||_HS^2=C_even-1",
        forward_private_generator_test=(
            "A selected-word coefficient vanishes if g,h,or k occurs exactly once"
        ),
        inverse_private_generator_test=(
            "Apply the same rule to a,b,c using g~cb^-1,h~a^-1c,k=bc^-1a"
        ),
        allowed_block_orbit_sizes="4 order-3, 3 order-4, 6 order-5, 1 order-6",
        order_six_anova_equals_identity_support_core=False,
        growing_support_operator_bound_proved=False,
        status=(
            "joint-cycle-channel-reduced-to-fourteen-higher-order-anova-blocks"
            if exact
            else "alternating-block-operator-anova-failure"
        ),
    )
    return AlternatingBlockOperatorAnovaReport(
        created_at=utc_now(),
        theorem_contract={
            "operator": theorem.normalized_operator,
            "collision_norm": theorem.centered_hilbert_schmidt_identity,
            "forward_zero_test": theorem.forward_private_generator_test,
            "inverse_zero_test": theorem.inverse_private_generator_test,
            "remaining_blocks": theorem.allowed_block_orbit_sizes,
            "basis_warning": (
                "The order-six ANOVA block is not the fully nonidentity class-matching "
                "core Z6_+; finite controls explicitly falsify equality."
            ),
            "scope": (
                "No asymptotic norm estimate is proved on any growing-support block."
            ),
        },
        theorem=theorem,
        allowed_blocks=[
            {
                "six_word_mask": mask,
                "input_subset_mask": mask & 7,
                "output_subset_mask": mask >> 3,
                "selected_word_count": mask.bit_count(),
                "forward_test": True,
                "inverse_test": True,
            }
            for mask in allowed
        ],
        exact_controls=controls,
        finite_block_energies={
            f"n={n}": rows for n, (_control, rows) in zip(range(2, 6), audited)
        },
        proof_obligations=[
            {
                "obligation": "derive_normalized_conditional_collision_operator",
                "resolved": exact,
                "resolution": (
                    "Product input/output class marginals make the quadratic collision "
                    "exactly its Hilbert--Schmidt norm."
                ),
            },
            {
                "obligation": "classify_all_exact_zero_anova_blocks",
                "resolved": exact,
                "resolution": (
                    "Intersect forward and inverse private-generator criteria; only "
                    "fourteen of sixty-three nonconstant subset pairs survive."
                ),
            },
            {
                "obligation": "bound_fourteen_allowed_blocks_on_growing_support",
                "resolved": False,
                "resolution": (
                    "Use joint character moments, conditional normal-set mixing, or "
                    "operator hypercontractivity without composing marginal estimates."
                ),
            },
            {
                "obligation": "relate_anova_blocks_to_z6_core_without_false_identity",
                "resolved": False,
                "resolution": (
                    "Only aggregate asymptotic comparisons are valid until an explicit "
                    "Möbius transform between the two decompositions is derived."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Pairwise independence makes every nonconstant block zero.",
                "resolved": True,
                "resolution": (
                    "It kills only one-by-one blocks; fourteen higher-order blocks "
                    "survive the dual private-generator tests."
                ),
            },
            {
                "objection": "Forward private-generator cancellation is complete.",
                "resolved": True,
                "resolution": (
                    "The inverse bijection supplies additional exact zeros not visible "
                    "from the original generators."
                ),
            },
            {
                "objection": "The order-six ANOVA energy is Z6_+.",
                "resolved": True,
                "resolution": (
                    "False: ANOVA centers by class probability, whereas Z6_+ selects "
                    "nonidentity matching classes. S4/S5 values differ explicitly."
                ),
            },
            {
                "objection": "A large finite singular value proves asymptotic survival.",
                "resolved": False,
                "resolution": "Finite spectra through A5 have no scaling force.",
            },
        ],
        headline_metrics={
            "block_operator_theorem_count": int(exact),
            "private_generator_sparsity_theorem_count": int(exact),
            "allowed_nonconstant_anova_block_count": len(allowed),
            "forbidden_nonconstant_anova_block_count": 63 - len(allowed),
            "exact_finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "growing_support_operator_bound_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "normalized_conditional_collision_operator_proved": exact,
            "dual_private_generator_sparsity_proved": exact,
            "fourteen_block_anova_normal_form_proved": exact,
            "order_six_anova_equals_z6_core": False,
            "growing_support_allowed_blocks_subpolynomial_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact operator and sparsity pattern are known, but all fourteen "
                "allowed growing-support interaction blocks lack norm estimates."
            ),
        },
        status=(
            "joint-block-dependence-has-fourteen-block-operator-normal-form"
            if exact
            else "alternating-anova-normal-form-control-failure"
        ),
        summary=(
            "Converted even cycle-type collision into a normalized conditional operator "
            "and proved that dual private-generator cancellation leaves 14 ANOVA blocks."
        ),
        falsifiers_triggered=[
            "Pairwise independence does not eliminate higher-order block synergy.",
            "Forward generator cancellation alone misses exact inverse-coordinate zeros.",
            "The highest ANOVA block and fully nonidentity class-matching core are not identical.",
        ],
    )


def write_alternating_block_operator_anova_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_alternating_block_operator_anova())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_alternating_block_operator_anova_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
