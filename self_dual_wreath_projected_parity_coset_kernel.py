"""Cancellation-preserving kernels for the two adaptive parity-coset energies.

Let ``R`` be a sign-invariant set of irreducible representations of ``S_n``
and define the projected central kernel

    K_R(a,b)=|S_n|^-1 sum_(lambda in R) chi_lambda(a)chi_lambda(b).

For an input parity ``x in F_2^3``, let ``T_x`` be the permutation triples
``t=(g,h,k)`` with that parity, and let

    F_x(O)=sum_(t in T_x) product_i r_(O_i)(W_i(t)).

If ``t,u`` lie in the same parity coset, every pair of corresponding words
has the same sign.  Therefore the two members of each nonself transpose orbit
contribute identically, and summing the coarse orbit weight reconstructs the
ordinary ``S_n`` kernel exactly.  For the retained orbit product set ``B_R``,

    S_x(R):=sum_(O in B_R) Q(O)F_x(O)^2
           =sum_(t,u in T_x) product_i K_R(W_i(t),W_i(u)).          (1)

Writing ``N_x(C)`` for the number of triples in ``T_x`` with six-word class
signature ``C`` gives the cancellation-preserving class formula

    S_x(R)=sum_(C,D) N_x(C)N_x(D) product_i K_R(C_i,D_i).          (2)

For ``R`` equal to all irreps, column orthogonality diagonalizes the kernel,
so (2) becomes the parity-restricted class-signature collision moment

    S_x(all)=sum_C N_x(C)^2/product_i |C_i|.                       (3)

The seven nonzero energies form four face and three opposite-complement
sectors.  Equations (1)--(3) preserve the cancellations destroyed by
pointwise triangle bounds.  They do not prove canonical projected decay or
survival.
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

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    coarse_alternating_plancherel_weights,
    permutation_parity_from_cycle_type,
)
from self_dual_wreath_alternating_parity_coset_channel import (
    parity_coset_word_likelihood_arrays,
)
from self_dual_wreath_projected_tetrahedral_word_map import (
    projected_mean_and_kernel,
)
from self_dual_wreath_sign_orbit_syndrome_reduction import (
    BitVector,
    sign_frequency,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    tetrahedral_class_signature_counts,
)
from symmetric_character import conjugacy_class_size


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_projected_parity_coset_kernel.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PROJECTED-PARITY-COSET-KERNEL"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Signature = tuple[Partition, Partition, Partition, Partition, Partition, Partition]


@dataclass(frozen=True)
class ProjectedParityCosetKernelControl:
    n: int
    minimum_retained_dimension_exclusive: int
    retained_partition_count: int
    parity_coset_count: int
    face_sector_count: int
    opposite_complement_sector_count: int
    maximum_direct_kernel_energy_residual: float
    maximum_full_kernel_collision_residual: float | None
    maximum_face_symmetry_residual: float
    maximum_opposite_symmetry_residual: float
    face_sector_projected_energy: float
    opposite_sector_projected_energy: float
    base_sector_projected_energy: float
    total_nonzero_projected_energy: float
    all_projected_energies_nonnegative: bool
    exact_projected_parity_coset_kernel_verified: bool
    status: str


@dataclass(frozen=True)
class ProjectedParityCosetKernelReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[ProjectedParityCosetKernelControl]
    asymptotic_target: dict[str, str | bool]
    literature_boundary: list[dict[str, str]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def parity_coset_signature_counts(
    n: int,
    parity: BitVector,
) -> dict[Signature, int]:
    if parity not in itertools.product((0, 1), repeat=3):
        raise ValueError("parity must lie in F_2^3")
    return {
        signature: count
        for signature, count in tetrahedral_class_signature_counts(n).items()
        if tuple(
            permutation_parity_from_cycle_type(signature[index])
            for index in range(3)
        )
        == parity
    }


def projected_parity_coset_energy(
    n: int,
    minimum_dimension_exclusive: int,
    parity: BitVector,
) -> Fraction:
    """Evaluate equation (2) exactly through ``S_4``."""

    if not 2 <= n <= 4:
        raise ValueError("exact projected parity kernels require 2<=n<=4")
    _retained, _mass, _mean, kernel = projected_mean_and_kernel(
        n,
        minimum_dimension_exclusive,
    )
    signatures = parity_coset_signature_counts(n, parity)
    return sum(
        (
            left_count
            * right_count
            * math.prod(
                kernel[left[index], right[index]] for index in range(6)
            )
            for left, left_count in signatures.items()
            for right, right_count in signatures.items()
        ),
        start=Fraction(),
    )


def full_parity_class_collision_energy(n: int, parity: BitVector) -> Fraction:
    """Evaluate the diagonal full-kernel formula (3)."""

    signatures = parity_coset_signature_counts(n, parity)
    return sum(
        (
            Fraction(
                count * count,
                math.prod(conjugacy_class_size(cycle_type) for cycle_type in signature),
            )
            for signature, count in signatures.items()
        ),
        start=Fraction(),
    )


def direct_parity_coset_energies(
    n: int,
    minimum_dimension_exclusive: int,
) -> dict[BitVector, float]:
    orbits, arrays = parity_coset_word_likelihood_arrays(n)
    _orbits, weights = coarse_alternating_plancherel_weights(n)
    one = np.asarray([weights[orbit] for orbit in orbits], dtype=float)
    product = np.einsum(
        "a,b,c,d,e,f->abcdef",
        one,
        one,
        one,
        one,
        one,
        one,
        optimize=False,
    )
    dimensions = np.asarray(
        [hook_length_dimension(orbit[0]) for orbit in orbits],
        dtype=int,
    )
    mask = np.ones(product.shape, dtype=bool)
    for axis in range(6):
        shape = [1] * 6
        shape[axis] = len(orbits)
        mask &= (dimensions > minimum_dimension_exclusive).reshape(shape)
    return {
        parity: float(np.sum(product[mask] * array[mask] ** 2))
        for parity, array in arrays.items()
    }


def audit_projected_parity_coset_kernel(
    n: int,
    minimum_dimension_exclusive: int,
) -> ProjectedParityCosetKernelControl:
    if not 2 <= n <= 4:
        raise ValueError("exact projected parity controls require 2<=n<=4")
    direct = direct_parity_coset_energies(n, minimum_dimension_exclusive)
    kernel = {
        parity: projected_parity_coset_energy(
            n,
            minimum_dimension_exclusive,
            parity,
        )
        for parity in itertools.product((0, 1), repeat=3)
    }
    direct_residual = max(
        abs(direct[parity] - float(value)) for parity, value in kernel.items()
    )
    collision_residual = None
    if minimum_dimension_exclusive == 0:
        collision_residual = max(
            abs(
                float(kernel[parity])
                - float(full_parity_class_collision_energy(n, parity))
            )
            for parity in kernel
        )
    nonzero = tuple(parity for parity in kernel if parity != (0, 0, 0))
    face = tuple(
        float(kernel[parity])
        for parity in nonzero
        if sum(sign_frequency(parity)) == 3
    )
    opposite = tuple(
        float(kernel[parity])
        for parity in nonzero
        if sum(sign_frequency(parity)) == 4
    )
    face_residual = max(face) - min(face)
    opposite_residual = max(opposite) - min(opposite)
    nonnegative = all(value >= 0 for value in kernel.values())
    tolerance = 2e-8
    exact = bool(
        direct_residual <= tolerance
        and (collision_residual is None or collision_residual <= tolerance)
        and face_residual <= tolerance
        and opposite_residual <= tolerance
        and len(face) == 4
        and len(opposite) == 3
        and nonnegative
    )
    retained_count = sum(
        hook_length_dimension(partition) > minimum_dimension_exclusive
        for partition in projected_mean_and_kernel(
            n,
            minimum_dimension_exclusive,
        )[0]
    )
    return ProjectedParityCosetKernelControl(
        n=n,
        minimum_retained_dimension_exclusive=minimum_dimension_exclusive,
        retained_partition_count=retained_count,
        parity_coset_count=len(kernel),
        face_sector_count=len(face),
        opposite_complement_sector_count=len(opposite),
        maximum_direct_kernel_energy_residual=direct_residual,
        maximum_full_kernel_collision_residual=collision_residual,
        maximum_face_symmetry_residual=face_residual,
        maximum_opposite_symmetry_residual=opposite_residual,
        face_sector_projected_energy=face[0],
        opposite_sector_projected_energy=opposite[0],
        base_sector_projected_energy=float(kernel[(0, 0, 0)]),
        total_nonzero_projected_energy=sum(float(kernel[parity]) for parity in nonzero),
        all_projected_energies_nonnegative=nonnegative,
        exact_projected_parity_coset_kernel_verified=exact,
        status=(
            "exact-projected-parity-coset-kernel-verified"
            if exact
            else "projected-parity-coset-kernel-control-failure"
        ),
    )


def run_projected_parity_coset_kernel() -> ProjectedParityCosetKernelReport:
    controls = [
        audit_projected_parity_coset_kernel(n, threshold)
        for n, threshold in (
            (2, 0),
            (3, 0),
            (3, 1),
            (4, 0),
            (4, 1),
            (4, 2),
        )
    ]
    exact = all(row.exact_projected_parity_coset_kernel_verified for row in controls)
    strongest = controls[-1]
    return ProjectedParityCosetKernelReport(
        created_at=utc_now(),
        theorem_contract={
            "projected_kernel": (
                "K_R(a,b)=|S_n|^-1 sum_(lambda in R)chi_lambda(a)chi_lambda(b)."
            ),
            "same_parity_sign_orbit_collapse": (
                "For t,u in the same input-parity coset, corresponding word signs "
                "agree, so coarse sign-orbit Plancherel sums equal K_R."
            ),
            "parity_coset_energy": (
                "S_x(R)=sum_(t,u in T_x)product_i K_R(W_i(t),W_i(u))."
            ),
            "class_signature_contraction": (
                "S_x(R)=sum_(C,D)N_x(C)N_x(D)product_i K_R(C_i,D_i)."
            ),
            "full_kernel_collision": (
                "S_x(all)=sum_C N_x(C)^2/product_i |C_i|."
            ),
            "scope": (
                "The kernel identity preserves cancellation but does not estimate the "
                "canonical high-dimensional contraction."
            ),
        },
        exact_controls=controls,
        asymptotic_target={
            "retained_set": "R_n={lambda:d_lambda>D_n}",
            "face_target": "S_(100)(R_n)=o(1)",
            "opposite_target": "S_(001)(R_n)=o(1)",
            "tetrahedral_transfer": "four face and three opposite sectors",
            "allowed_methods": (
                "projected-kernel operator bounds, collision-switching, trace moments, "
                "or multilinear orthogonality before absolute values"
            ),
            "pointwise_triangle_allowed": False,
            "canonical_decay_proved": False,
        },
        literature_boundary=[
            {
                "id": "teyssier-thevenin-sharp-character-bounds-2025",
                "url": "https://arxiv.org/abs/2411.04347",
                "boundary": (
                    "Pointwise character estimates may be inserted only after enough "
                    "kernel cancellation or collision constraints have been retained."
                ),
            },
            {
                "id": "lifschitz-marmor-hypercontractive-characters-2023",
                "url": "https://arxiv.org/abs/2308.08694",
                "boundary": (
                    "Level bounds do not directly evaluate the six-fold correlated "
                    "parity-restricted kernel contraction."
                ),
            },
        ],
        proof_obligations=[
            {
                "obligation": "derive_cancellation_preserving_parity_coset_kernel",
                "resolved": exact,
                "resolution": (
                    "Same-coset word parities make each transpose pair reproduce the "
                    "ordinary sign-invariant S_n Plancherel character kernel."
                ),
            },
            {
                "obligation": "identify_full_projection_with_class_signature_collision",
                "resolved": exact,
                "resolution": (
                    "Column orthogonality diagonalizes the all-irrep kernel by conjugacy class."
                ),
            },
            {
                "obligation": "bound_canonical_face_kernel_contraction",
                "resolved": False,
                "resolution": (
                    "Prove cancellation in one face-sector double signature sum."
                ),
            },
            {
                "obligation": "bound_canonical_opposite_kernel_contraction",
                "resolved": False,
                "resolution": (
                    "Prove cancellation in one opposite-complement double signature sum."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Choosing one representative per sign orbit loses the S_n kernel.",
                "resolved": True,
                "resolution": (
                    "It would for opposite word signs; within one input-parity coset all "
                    "paired signs agree and the transpose contributions coincide."
                ),
            },
            {
                "objection": "The projected kernel has signs, so S_x may be negative.",
                "resolved": True,
                "resolution": (
                    "Equation (1) is a Plancherel-weighted sum of squares F_x(O)^2."
                ),
            },
            {
                "objection": "The exact kernel formula proves asymptotic mixing.",
                "resolved": False,
                "resolution": (
                    "It supplies the correct contraction; no canonical-norm estimate is known."
                ),
            },
        ],
        headline_metrics={
            "projected_parity_coset_kernel_theorem_count": int(exact),
            "full_kernel_collision_identity_count": int(exact),
            "finite_control_count": len(controls),
            "maximum_direct_kernel_energy_residual": max(
                row.maximum_direct_kernel_energy_residual for row in controls
            ),
            "S4_dimension_gt_2_face_energy": strongest.face_sector_projected_energy,
            "S4_dimension_gt_2_opposite_energy": (
                strongest.opposite_sector_projected_energy
            ),
            "canonical_kernel_decay_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "cancellation_preserving_kernel_identity_proved": exact,
            "full_projection_collision_identity_proved": exact,
            "canonical_face_energy_vanishes_proved": False,
            "canonical_opposite_energy_vanishes_proved": False,
            "canonical_adaptive_syndrome_decouples_proved": False,
            "canonical_adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact cancellation-preserving kernel is available, but neither "
                "canonical parity-sector contraction has an asymptotic estimate."
            ),
        },
        status=(
            "adaptive-energy-reduced-to-two-projected-kernel-contractions"
            if exact
            else "projected-parity-coset-kernel-control-failure"
        ),
        summary=(
            "Converted the face and opposite adaptive energies into exact projected "
            "class-kernel collision contractions that preserve cancellation."
        ),
        falsifiers_triggered=[
            "The sign-orbit quotient does not obstruct a same-parity S_n kernel formula.",
            "Only two parity-restricted projected collision contractions remain.",
            "The exact kernel identity alone is not an asymptotic no-go or survivor certificate.",
        ],
    )


def write_projected_parity_coset_kernel_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_projected_parity_coset_kernel())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_projected_parity_coset_kernel_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
