"""Relative scalar-center character-normalizer quotient, quadratic-phase relative abelian base, character-attached weighted erasure, and unrolled twisted recursion.

This standalone module implements the relative recursion, character-normalizer
quotient, relative abelian base, and character-attached weighted-erasure
controls documented in ``research/TWISTED_STATE_SYMMETRY_RECEIVER.md`` and
``research/MECHANICAL_FOLLOW_UP_PLAN.md`` (``## 2026-10-21 Twisted State Source
Contract``):

1. **Character-Preserving Normalizer Quotient (S = M_chi / K_0, Z_new = K / K_0)**:
   - Wraps ``character_normalizer`` from ``theorems/twisted_state_source.py`` on
     an independently learned subgroup ``K <= H`` and character ``chi_K``
     (learned from original single copies ``k = 1``).
   - Verifies that quotienting ``K_0 = ker(chi_K)`` inside the plain normalizer
     ``N_L(K)`` fails when ``[N_L(K), K_0]`` is not contained in ``K_0``
     (e.g., Heisenberg ``[x, y] = z`` with ``K = <y, z>`` and ``chi_K = (a, 1)``),
     whereas ``K_0`` is an ideal of ``M_chi = {x in L : [x, K] <= K_0}`` and
     ``Z_new = K / K_0`` is central in ``S = M_chi / K_0`` of dimension ``<= 1``
     with an induced faithful scalar character.
2. **Relative Abelian Base (Q = G / Z Abelian, Central Extension Phase + Character)**:
   - Certifies that when ``r = class(G / Z) == 1`` and ``[G, G] = Z != 0`` has a
     nontrivial central character ``chi_Z``, a public linear section ``sigma: G/Z -> G``
     induces a degree-2 central-extension phase plus the degree-1 unknown character
     phase on ``G / Z``.
   - Rejects dispatching a non-commuting relative abelian base (``[G, G] != 0``
     under ``chi_Z``) to plain abelian HSP, proves that naive quotient Fourier
     sampling leaks ``1 - 1/p`` probability mass outside ``U^perp``, and verifies
     that degree-2 -> degree-1 scalar phase erasure recovers ``U = H / Z`` and
     lifts ``H = sigma(U) + Z``.
3. **Character-Attached Weighted Erasure & Two-Stage Cascade Verifier**:
   - Connects ``attach_linear_character`` (from ``theorems/twisted_state_source.py``)
     to ``PinnedWeightedPacket``, ``weighted_erasure_stage``,
     ``transition_to_fourier_residual``, and ``ordinary_higher_degree_erasure_stage``
     (from ``theorems/weighted_two_erasure_cascade.py``).
   - Verifies that the ``m`` appended unknown linear character parameters have
     nonconstant weight 1, do not alter weighted stages ``d >= 2``, are completely
     erased at weighted stage ``d = 1`` without evaluating ``ell`` or calling
     ``evaluate_fixture``, and leave zero character parameters in the post-Fourier
     Stage-2 residual polynomial.
4. **Unrolled Relative Scalar-Center Recursion Controller (SolveTwisted(G, Z, chi_Z))**:
   - Tracks progress by the relative quotient class ``r = class((G / Z))``,
     recurses on ``N = G' + Z`` whose relative quotient ``Q' = (G/Z)'`` has class
     ``<= floor(r / 2)``, charges original-copy character learning on ``K = H intersect N``,
     quotients by ``K_0 = ker(chi_K)`` inside ``M_chi``, loops twisted image calls
     with strict relative class drops ``class(T / Z_new) < class(S / Z_new)``,
     terminates at the relative abelian base, and enforces the Section 8 bounds
     ``I(r) <= r + I(min(3, floor(r/2)))`` (``<= c + 4`` for ``c >= 4``) and
     ``<= 2`` nonabelian known-``K`` character-learning batches.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from math import prod
from pathlib import Path
import random
import sys
from typing import Callable, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.class_three_ambient_frontend import (
    _quotient_complement_basis,
    _subspace_contains,
    _subspace_intersection,
    compute_subalgebra_normalizer,
)
from theorems.class_three_monomial_jet import (
    ClassThreeStructure,
    FullTaylorJetChart,
    align_full_jet,
    compile_full_jet_phase,
)
from theorems.prime_character_opi import ring
from theorems.state_symmetry_coset_transfer import plan_orbit_state_transfer
from theorems.symbolic_scalar_phase_erasure import (
    PublicLieAlgebra,
    _canonical_vec,
    _fmpz_rref,
    _fmpz_solve_coordinates,
)
from theorems.twisted_state_source import (
    affine_character_sector,
    attach_linear_character,
    character_normalizer,
)
from theorems.ut5_matrix_phase_alignment import _rank
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket
from theorems.weighted_two_erasure_cascade import (
    PinnedWeightedPacket,
    ordinary_higher_degree_erasure_stage,
    transition_to_fourier_residual,
    weighted_erasure_stage,
)


JSON_PATH = ROOT / "research" / "reductions" / "twisted_relative_recursion.json"
MD_PATH = ROOT / "research" / "TWISTED_RELATIVE_RECURSION.md"


def _canonical_subspace_basis(
    vectors: Sequence[Sequence[int]],
    p: int,
) -> list[tuple[int, ...]]:
    """Return the canonical Reduced Row Echelon Form (RREF) basis of ``span(vectors)`` over GF(p)."""
    if not vectors:
        return []
    reduced, _ = _fmpz_rref(vectors, p)
    return [tuple(row) for row in reduced if any(row)]


def twisted_image_call_bound(relative_class: int) -> int:
    """Return the Section 8 safe upper bound ``I(r)`` on image/base calls at relative class ``r``.

    Follows the recurrence in ``research/TWISTED_STATE_SYMMETRY_RECEIVER.md`` Section 8:
    - ``I(0) = 0``
    - ``I(1) = 1``
    - ``I(r) = I(min(3, r // 2)) + r`` for ``r >= 2``
    giving ``I(2) = 3``, ``I(3) = 4``, and ``I(c) = c + 4`` for ``c >= 4``.
    """
    if type(relative_class) is not int or relative_class < 0:
        raise ValueError("nonnegative integer relative_class required")
    if relative_class == 0:
        return 0
    if relative_class == 1:
        return 1
    return twisted_image_call_bound(min(3, relative_class // 2)) + relative_class


def relative_quotient_algebra(
    algebra: PublicLieAlgebra,
    ambient_basis: Sequence[Sequence[int]],
    central_z_basis: Sequence[Sequence[int]],
) -> tuple[PublicLieAlgebra, tuple[tuple[int, ...], ...], int]:
    """Construct the public quotient Lie algebra ``Q = G / Z`` for central ``Z <= G`` and return ``(Q, section_in_G, class(Q))``."""
    G_span = algebra.span(ambient_basis)
    Z_span = algebra.span(central_z_basis)
    if len(Z_span) > 1:
        raise ValueError("relative scalar center Z must have dimension 0 or 1")
    if not _subspace_contains(G_span, Z_span, algebra.p):
        raise ValueError("scalar center Z must be contained in G")
    for g_vec in G_span:
        for z_vec in Z_span:
            if any(algebra.bracket(g_vec, z_vec)):
                raise ValueError("Z must be central in G ([G, Z] = 0)")

    section_in_L = _quotient_complement_basis(Z_span, G_span, algebra.dimension, algebra.p)
    adapted_G = list(Z_span) + list(section_in_L)
    z_dim = len(Z_span)
    q_dim = len(section_in_L)

    if q_dim == 0:
        q_alg = PublicLieAlgebra(p=algebra.p, dimension=1, bracket_fn=lambda a, b: (0,))
        return q_alg, (), 0

    bracket_table: list[list[tuple[int, ...]]] = [
        [(0,) * q_dim for _ in range(q_dim)] for _ in range(q_dim)
    ]
    for i in range(q_dim):
        for j in range(i + 1, q_dim):
            br = algebra.bracket(section_in_L[i], section_in_L[j])
            coords = _fmpz_solve_coordinates(adapted_G, br, algebra.p)
            if coords is None:
                raise ArithmeticError("G failed bracket closure")
            q_br = tuple(coords[z_dim:])
            bracket_table[i][j] = q_br
            bracket_table[j][i] = tuple((-x) % algebra.p for x in q_br)

    def q_bracket(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        out = [0] * q_dim
        for i, u in enumerate(left):
            if not u:
                continue
            for j, v in enumerate(right):
                if not v or i == j:
                    continue
                uv = u * v % algebra.p
                row = bracket_table[i][j]
                for c in range(q_dim):
                    out[c] = (out[c] + uv * row[c]) % algebra.p
        return tuple(out)

    q_alg = PublicLieAlgebra(p=algebra.p, dimension=q_dim, bracket_fn=q_bracket)
    q_std = [tuple(int(i == j) for j in range(q_dim)) for i in range(q_dim)]
    q_class = q_alg.nilpotency_class(q_std)
    return q_alg, tuple(section_in_L), q_class


@dataclass(frozen=True)
class CharacterNormalizerQuotient:
    """Public quotient ``S = M_chi / K_0`` with central ``Z_new = K / K_0`` of dimension ``<= 1``."""

    quotient_algebra: PublicLieAlgebra
    m_chi_basis_in_ambient: tuple[tuple[int, ...], ...]
    plain_normalizer_basis_in_ambient: tuple[tuple[int, ...], ...]
    k_basis_in_ambient: tuple[tuple[int, ...], ...]
    k0_kernel_basis_in_ambient: tuple[tuple[int, ...], ...]
    section_basis_in_ambient: tuple[tuple[int, ...], ...]
    z_new_basis_in_quotient: tuple[tuple[int, ...], ...]
    z_new_character: tuple[int, ...]
    scalar_center_width: int
    m_chi_strictly_smaller_than_plain_normalizer: bool
    k0_ideal_in_plain_normalizer: bool
    k0_ideal_in_m_chi: bool
    z_new_central_in_quotient: bool
    quotient_class: int
    relative_quotient_class: int

    def lift_to_ambient(self, s_vec: Sequence[int]) -> tuple[int, ...]:
        """Lift a vector in ``S = M_chi / K_0`` to the ambient Lie algebra via the public section."""
        s_dim = len(self.section_basis_in_ambient)
        _canonical_vec(s_vec, s_dim, self.quotient_algebra.p)
        if not s_dim:
            return ()
        amb_dim = len(self.section_basis_in_ambient[0])
        return tuple(
            sum(s_vec[j] * self.section_basis_in_ambient[j][coord] for j in range(s_dim))
            % self.quotient_algebra.p
            for coord in range(amb_dim)
        )

    def project_from_m_chi(self, ambient_vec: Sequence[int]) -> tuple[int, ...]:
        """Project an ambient vector in ``M_chi`` modulo ``K_0`` into ``S = M_chi / K_0``."""
        adapted = list(self.k0_kernel_basis_in_ambient) + list(self.section_basis_in_ambient)
        coords = _fmpz_solve_coordinates(adapted, ambient_vec, self.quotient_algebra.p)
        if coords is None:
            raise ValueError("ambient vector does not lie in M_chi")
        return tuple(coords[len(self.k0_kernel_basis_in_ambient) :])


def public_character_normalizer_quotient(
    algebra: PublicLieAlgebra,
    ambient_basis: Sequence[Sequence[int]],
    k_basis: Sequence[Sequence[int]],
    k_character: Sequence[int],
    *,
    prior_z_basis: Sequence[Sequence[int]] = (),
    prior_z_character: Sequence[int] = (),
) -> CharacterNormalizerQuotient:
    """Construct ``S = M_chi / K_0`` and ``Z_new = K / K_0`` per Section 5 of ``TWISTED_STATE_SYMMETRY_RECEIVER.md``."""
    p = algebra.p
    G_span = algebra.span(ambient_basis)
    g_dim = len(G_span)
    if g_dim == 0:
        raise ValueError("nonempty ambient basis required")

    k_tuples = tuple(tuple(int(x) % p for x in row) for row in k_basis)
    _canonical_vec(k_character, len(k_tuples), p)
    if _rank(k_tuples, p) != len(k_tuples):
        raise ValueError("independent K basis required")
    if not _subspace_contains(G_span, k_tuples, p):
        raise ValueError("K must be contained in current ambient G")

    z_tuples = tuple(tuple(int(x) % p for x in row) for row in prior_z_basis)
    _canonical_vec(prior_z_character, len(z_tuples), p)
    if len(z_tuples) > 1:
        raise ValueError("prior scalar center Z must have dimension <= 1")
    for z_vec, z_val in zip(z_tuples, prior_z_character):
        coords_in_k = _fmpz_solve_coordinates(k_tuples, z_vec, p)
        if coords_in_k is None:
            raise ValueError("prior scalar center Z must be contained in learned K = H intersect N")
        induced_val = sum(c * ch for c, ch in zip(coords_in_k, k_character)) % p
        if induced_val != z_val % p:
            raise ValueError("learned character chi_K on K disagrees with known faithful character on Z")

    local_table: list[list[tuple[int, ...]]] = [
        [(0,) * g_dim for _ in range(g_dim)] for _ in range(g_dim)
    ]
    for i in range(g_dim):
        for j in range(i + 1, g_dim):
            br = algebra.bracket(G_span[i], G_span[j])
            coords = _fmpz_solve_coordinates(G_span, br, p)
            if coords is None:
                raise ValueError("ambient_basis must form a Lie subalgebra")
            local_table[i][j] = tuple(coords)
            local_table[j][i] = tuple((-x) % p for x in coords)

    def g_local_bracket(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        out = [0] * g_dim
        for i, u in enumerate(left):
            if not u:
                continue
            for j, v in enumerate(right):
                if not v or i == j:
                    continue
                uv = u * v % p
                row = local_table[i][j]
                for c in range(g_dim):
                    out[c] = (out[c] + uv * row[c]) % p
        return tuple(out)

    g_local_alg = PublicLieAlgebra(p=p, dimension=g_dim, bracket_fn=g_local_bracket)
    k_in_g = [tuple(_fmpz_solve_coordinates(G_span, kv, p)) for kv in k_tuples]
    cn = character_normalizer(g_local_alg, k_in_g, tuple(k_character))

    def lift_from_g(local_vec: Sequence[int]) -> tuple[int, ...]:
        return tuple(
            sum(local_vec[i] * G_span[i][coord] for i in range(g_dim)) % p
            for coord in range(algebra.dimension)
        )

    K0_amb = [lift_from_g(v) for v in cn.kernel]
    M_chi_amb = algebra.span([lift_from_g(v) for v in cn.normalizer])
    plain_norm_amb = compute_subalgebra_normalizer(algebra, G_span, k_tuples)

    k0_ideal_plain = all(
        _subspace_contains(K0_amb, [algebra.bracket(x, k0)], p)
        for x in plain_norm_amb
        for k0 in K0_amb
    )
    k0_ideal_m_chi = all(
        _subspace_contains(K0_amb, [algebra.bracket(x, k0)], p)
        for x in M_chi_amb
        for k0 in K0_amb
    )
    if not k0_ideal_m_chi:
        raise ArithmeticError("K_0 = ker(chi_K) must be an ideal of M_chi")

    z_section_amb = _quotient_complement_basis(K0_amb, k_tuples, algebra.dimension, p)
    assert len(z_section_amb) == cn.scalar_center_width
    rest_section_amb = _quotient_complement_basis(
        list(K0_amb) + list(z_section_amb),
        M_chi_amb,
        algebra.dimension,
        p,
    )
    section_in_amb = list(z_section_amb) + list(rest_section_amb)
    adapted_m_chi = list(K0_amb) + list(section_in_amb)
    k0_dim = len(K0_amb)
    s_dim = len(section_in_amb)

    if s_dim == 0:
        s_alg = PublicLieAlgebra(p=p, dimension=1, bracket_fn=lambda a, b: (0,))
        return CharacterNormalizerQuotient(
            quotient_algebra=s_alg,
            m_chi_basis_in_ambient=tuple(M_chi_amb),
            plain_normalizer_basis_in_ambient=tuple(plain_norm_amb),
            k_basis_in_ambient=k_tuples,
            k0_kernel_basis_in_ambient=tuple(K0_amb),
            section_basis_in_ambient=(),
            z_new_basis_in_quotient=(),
            z_new_character=(),
            scalar_center_width=0,
            m_chi_strictly_smaller_than_plain_normalizer=(len(M_chi_amb) < len(plain_norm_amb)),
            k0_ideal_in_plain_normalizer=k0_ideal_plain,
            k0_ideal_in_m_chi=True,
            z_new_central_in_quotient=True,
            quotient_class=0,
            relative_quotient_class=0,
        )

    s_table: list[list[tuple[int, ...]]] = [
        [(0,) * s_dim for _ in range(s_dim)] for _ in range(s_dim)
    ]
    for i in range(s_dim):
        for j in range(i + 1, s_dim):
            br = algebra.bracket(section_in_amb[i], section_in_amb[j])
            coords = _fmpz_solve_coordinates(adapted_m_chi, br, p)
            if coords is None:
                raise ArithmeticError("M_chi failed bracket closure")
            q_br = tuple(coords[k0_dim:])
            s_table[i][j] = q_br
            s_table[j][i] = tuple((-x) % p for x in q_br)

    def s_bracket(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        out = [0] * s_dim
        for i, u in enumerate(left):
            if not u:
                continue
            for j, v in enumerate(right):
                if not v or i == j:
                    continue
                uv = u * v % p
                row = s_table[i][j]
                for c in range(s_dim):
                    out[c] = (out[c] + uv * row[c]) % p
        return tuple(out)

    s_alg = PublicLieAlgebra(p=p, dimension=s_dim, bracket_fn=s_bracket)
    s_std = [tuple(int(i == j) for j in range(s_dim)) for i in range(s_dim)]
    s_class = s_alg.nilpotency_class(s_std)

    if cn.scalar_center_width == 1:
        z_new_basis_in_s = (tuple(int(i == 0) for i in range(s_dim)),)
        z_rep_coords_in_k = _fmpz_solve_coordinates(k_tuples, z_section_amb[0], p)
        assert z_rep_coords_in_k is not None
        z_char_val = sum(c * ch for c, ch in zip(z_rep_coords_in_k, k_character)) % p
        assert z_char_val != 0
        z_new_char = (z_char_val,)
    else:
        z_new_basis_in_s = ()
        z_new_char = ()

    z_central = all(
        not any(s_alg.bracket(s_vec, z_vec))
        for s_vec in s_std
        for z_vec in z_new_basis_in_s
    )
    if not z_central:
        raise ArithmeticError("Z_new = K / K_0 failed centrality in S = M_chi / K_0")

    _, _, rel_class = relative_quotient_algebra(s_alg, s_std, z_new_basis_in_s)

    return CharacterNormalizerQuotient(
        quotient_algebra=s_alg,
        m_chi_basis_in_ambient=tuple(M_chi_amb),
        plain_normalizer_basis_in_ambient=tuple(plain_norm_amb),
        k_basis_in_ambient=k_tuples,
        k0_kernel_basis_in_ambient=tuple(K0_amb),
        section_basis_in_ambient=tuple(section_in_amb),
        z_new_basis_in_quotient=z_new_basis_in_s,
        z_new_character=z_new_char,
        scalar_center_width=cn.scalar_center_width,
        m_chi_strictly_smaller_than_plain_normalizer=(len(M_chi_amb) < len(plain_norm_amb)),
        k0_ideal_in_plain_normalizer=k0_ideal_plain,
        k0_ideal_in_m_chi=True,
        z_new_central_in_quotient=z_central,
        quotient_class=s_class,
        relative_quotient_class=rel_class,
    )


def learn_known_subalgebra_character_from_original_copies(
    algebra: PublicLieAlgebra,
    k_basis: Sequence[Sequence[int]],
    single_copy_phase_oracle: Callable[[tuple[int, ...]], int],
) -> tuple[tuple[int, ...], int]:
    """Learn ``chi_K`` on a known subalgebra ``K <= H`` using 1 original copy per basis generator."""
    p = algebra.p
    basis = tuple(tuple(int(x) % p for x in row) for row in k_basis)
    if _rank(basis, p) != len(basis):
        raise ValueError("independent known K basis required")
    values = tuple(int(single_copy_phase_oracle(v)) % p for v in basis)
    for a in basis:
        for b in basis:
            br = algebra.bracket(a, b)
            coords = _fmpz_solve_coordinates(basis, br, p)
            if coords is None:
                raise ValueError("supplied K is not a Lie subalgebra")
            if sum(c * val for c, val in zip(coords, values)) % p != 0:
                raise ValueError("measured phase values do not vanish on [K, K]")
    return values, len(basis)


def compile_relative_abelian_twisted_leaf(
    p: int,
    quotient_width: int,
    scales: Sequence[int],
    outcomes: Sequence[Sequence[int]],
    tensor_powers: Sequence[int],
) -> SymbolicScalarPacket:
    """Compile the public symbolic phase packet for a relative abelian base ``Q = G / Z``."""
    ring(p)
    m = quotient_width
    if type(m) is not int or m < 1:
        raise ValueError("positive quotient_width required")
    if not scales or len(scales) != len(outcomes) or len(scales) != len(tensor_powers):
        raise ValueError("matching nonempty scales, outcomes, and tensor_powers required")
    _canonical_vec(scales, len(scales), p)
    if not all(scales):
        raise ValueError("nonzero shear scales required")
    _canonical_vec(tensor_powers, len(scales), p)
    for y in outcomes:
        _canonical_vec(y, m, p)

    monomials_deg2 = [
        alpha
        for alpha in product(range(3), repeat=m)
        if 1 <= sum(alpha) <= 2
    ]
    base_param_basis = tuple((0, alpha) for alpha in monomials_deg2)
    base_terms: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    for s, y, k in zip(scales, outcomes, tensor_powers):
        for p_idx, (_, alpha) in enumerate(base_param_basis):
            for beta in product(*(range(a + 1) for a in alpha)):
                if not any(beta):
                    continue
                coeff = int(k) * pow(int(s), sum(beta), p) % p
                for a, b, yj in zip(alpha, beta, y):
                    coeff = coeff * (1 if b == 0 or b == a else 2) * pow(int(yj), a - b, p) % p
                if coeff:
                    key = (tuple(beta), (p_idx,))
                    new_val = (base_terms.get(key, 0) + coeff) % p
                    if new_val:
                        base_terms[key] = new_val
                    else:
                        base_terms.pop(key, None)

    base_packet = SymbolicScalarPacket(p, m, 0, base_param_basis, base_terms)
    return attach_linear_character(base_packet, scales, outcomes, tensor_powers)


def verify_relative_abelian_quadratic_phase_erasure(
    p: int = 7,
    slope_a: int = 2,
    char_b: int = 1,
) -> dict[str, object]:
    """Compare naive quotient Fourier sampling vs degree-2 quadratic phase erasure on the Heisenberg relative base."""
    ring(p)
    omega = np.exp(2j * np.pi / p)
    half = pow(2, -1, p)
    addresses = list(product(range(p), repeat=2))
    fourier = np.array(
        [[omega ** ((-s * x - t * y) % p) / p for x, y in addresses] for s, t in addresses]
    )

    def phi(x: int, y: int) -> int:
        return (half * x * (y + slope_a * x) - char_b * x) % p

    sigma_raw = np.array(
        [
            [
                omega ** ((phi(x, y) - phi(u, v)) % p)
                if (y + slope_a * x - v - slope_a * u) % p == 0
                else 0.0
                for u, v in addresses
            ]
            for x, y in addresses
        ]
    ) / (p * p)
    probs_raw = np.diag(fourier @ sigma_raw @ fourier.conj().T).real
    outside_raw = float(
        sum(prob for (s, t), prob in zip(addresses, probs_raw) if (s - slope_a * t) % p != 0)
    )

    rng = random.Random(20261021)
    deg2_leaves = [
        compile_relative_abelian_twisted_leaf(
            p,
            2,
            scales=[1],
            outcomes=[[rng.randrange(p), rng.randrange(p)]],
            tensor_powers=[1],
        )
        for _ in range(36)
    ]
    deg1_packets: list[SymbolicScalarPacket] = []
    deg2_weights_log: list[list[int]] = []
    for batch_idx in range(9):
        sub_batch = deg2_leaves[4 * batch_idx : 4 * (batch_idx + 1)]
        sub_outcomes = [[rng.randrange(p), rng.randrange(p)] for _ in sub_batch]
        pkt1, w2, _, _ = ordinary_higher_degree_erasure_stage(
            sub_batch,
            2,
            outcomes=sub_outcomes,
            rng=rng,
        )
        assert pkt1.degree <= 1
        deg1_packets.append(pkt1)
        deg2_weights_log.append(w2)

    erased_pkt, w1, _, _ = ordinary_higher_degree_erasure_stage(
        deg1_packets,
        1,
        outcomes=[[rng.randrange(p), rng.randrange(p)] for _ in deg1_packets],
        rng=rng,
    )
    assert erased_pkt.degree == 0 and erased_pkt.terms == {}

    sigma_erased = np.array(
        [
            [
                1.0 if (y + slope_a * x - v - slope_a * u) % p == 0 else 0.0
                for u, v in addresses
            ]
            for x, y in addresses
        ]
    ) / (p * p)
    probs_erased = np.diag(fourier @ sigma_erased @ fourier.conj().T).real
    outside_erased = float(
        sum(prob for (s, t), prob in zip(addresses, probs_erased) if (s - slope_a * t) % p != 0)
    )
    inside_erased = float(
        sum(prob for (s, t), prob in zip(addresses, probs_erased) if (s - slope_a * t) % p == 0)
    )

    return {
        "p": p,
        "hidden_quotient_subspace_generator": [1, (-slope_a) % p],
        "expected_annihilator_generator": [slope_a % p, 1],
        "naive_fourier_mass_outside_annihilator": round(outside_raw, 12),
        "theoretical_naive_leakage_1_minus_1_over_p": float(Fraction(p - 1, p)),
        "erased_packet_final_degree": erased_pkt.degree,
        "erased_fourier_mass_outside_annihilator": round(outside_erased, 12),
        "erased_fourier_mass_inside_annihilator": round(inside_erased, 12),
        "degree_2_witness_sample": deg2_weights_log[0],
        "degree_1_witness_sample": w1,
    }


def compile_twisted_full_jet_leaf(
    *,
    instance_id: str,
    chart_id: str,
    chart: FullTaylorJetChart,
    structure: ClassThreeStructure,
    labels: Sequence[Sequence[int]],
    scales: Sequence[int],
    outcomes: Sequence[Sequence[int]],
    tensor_powers: Sequence[int],
    ambient_class: int,
    spectator: Sequence[int] | None = None,
) -> PinnedWeightedPacket:
    """Compile a full-jet GL-aligned leaf and attach the unknown linear character phase."""
    alignment = align_full_jet(chart, structure, labels, scales, outcomes)
    spec = (
        tuple(spectator)
        if spectator is not None
        else (1,) * (alignment.carrier_width - chart.jet_width)
    )
    base_packet = compile_full_jet_phase(alignment, spec, ambient_class)
    twisted_packet = attach_linear_character(base_packet, scales, outcomes, tensor_powers)
    return PinnedWeightedPacket(
        instance_id=instance_id,
        chart_id=chart_id,
        chart=chart,
        packet=twisted_packet,
        consumed=False,
    )


def verify_character_attached_weighted_cascade(
    p: int = 23,
    quotient_width: int = 1,
) -> dict[str, object]:
    """Verify that unknown linear character parameters are erased in Stage-1 weight-1 erasure and absent from Stage-2 residuals."""
    rng = random.Random(20261021)
    st = ClassThreeStructure(
        p,
        (((0, 1), (p - 1, 0)),),
        (((0, 0), (0, 0)), ((0, 0), (0, 0))),
        (((1,), (0,)), ((0,), (0,))),
    )
    chart = FullTaylorJetChart(p=p, quotient_width=quotient_width, noncentral_width=2, degree=2)

    rows: list[list[int]] = []
    scales: list[int] = []
    ys: list[tuple[int, ...]] = []
    for scale, y in product((1, 2, 3), product(range(3), repeat=quotient_width)):
        row = [
            pow(scale, k, p) * prod(pow(v, e, p) for v, e in zip(y, alpha)) % p
            for alpha, k, a in chart.indices
            if a == 0
        ]
        if _rank(rows + [row], p) > len(rows):
            rows.append(row)
            scales.append(scale)
            ys.append(y)

    sector = affine_character_sector(p, 2, ((1, 0),), (6,))
    fixed_label = sector.particular
    assert sector.contains(fixed_label)
    labels = [fixed_label] * len(rows)

    alignment = align_full_jet(chart, st, labels, scales, ys)
    spectator = (1,) * (alignment.carrier_width - chart.jet_width)
    base_pkt = compile_full_jet_phase(alignment, spectator, 4)
    powers = tuple((i % 3) + 1 for i in range(len(rows)))
    twisted_pkt = attach_linear_character(base_pkt, scales, ys, powers)

    char_coord = max(a for a, _ in twisted_pkt.parameter_basis)
    char_param_indices = [
        idx for idx, (a, _) in enumerate(twisted_pkt.parameter_basis) if a == char_coord
    ]
    char_param_set = set(char_param_indices)
    assert len(char_param_indices) == quotient_width

    char_term_weights = set()
    for (alpha, params), coeff in twisted_pkt.terms.items():
        if coeff and any(alpha) and any(p_idx in char_param_set for p_idx in params):
            w = sum(alpha[:quotient_width]) + sum(
                e * k for e, (_, k, _) in zip(alpha[quotient_width:], chart.indices)
            )
            char_term_weights.add(w)
    assert char_term_weights == {1}

    weight1_terms_only = {
        (alpha, params): coeff
        for (alpha, params), coeff in twisted_pkt.terms.items()
        if (
            sum(alpha[:quotient_width])
            + sum(e * k for e, (_, k, _) in zip(alpha[quotient_width:], chart.indices))
        )
        == 1
    }
    w1_leaves: list[PinnedWeightedPacket] = []
    for leaf_idx in range(len(char_param_indices) + 3):
        scaled_terms = {
            k_term: (
                v_coeff * (leaf_idx + 1 if any(p_idx in char_param_set for p_idx in k_term[1]) else 1)
            )
            % p
            for k_term, v_coeff in weight1_terms_only.items()
        }
        pkt_i = SymbolicScalarPacket(
            p,
            chart.quotient_width,
            chart.jet_width,
            twisted_pkt.parameter_basis,
            scaled_terms,
        )
        w1_leaves.append(
            PinnedWeightedPacket("twisted-cascade", "full-jet-d2", chart, pkt_i)
        )

    outcomes1 = [
        (
            [rng.randrange(p) for _ in range(chart.quotient_width)],
            [rng.randrange(p) for _ in range(chart.jet_width)],
        )
        for _ in w1_leaves
    ]
    erased_root, w1_weights, w1_rank, w1_eqs = weighted_erasure_stage(
        w1_leaves,
        1,
        outcomes1,
        rng=rng,
    )
    assert erased_root.weighted_degree == 0
    assert erased_root.packet.terms == {}

    eta = tuple((j + 1) % p for j in range(chart.jet_width))
    residual_pkt = transition_to_fourier_residual(erased_root, eta)
    residual_has_char_params = any(
        any(p_idx in char_param_set for p_idx in params)
        for (_, params), coeff in residual_pkt.terms.items()
        if coeff
    )
    assert not residual_has_char_params

    return {
        "p": p,
        "quotient_width": quotient_width,
        "base_parameter_count": len(base_pkt.parameter_basis),
        "twisted_parameter_count": len(twisted_pkt.parameter_basis),
        "character_parameter_indices": char_param_indices,
        "character_term_weights": sorted(char_term_weights),
        "affine_sector_label_probability": str(sector.label_probability),
        "stage1_weight1_active_equations": w1_eqs,
        "stage1_weight1_compressed_rank": w1_rank,
        "erased_root_weighted_degree": erased_root.weighted_degree,
        "post_fourier_residual_ordinary_degree": residual_pkt.degree,
        "post_fourier_residual_contains_character_params": residual_has_char_params,
    }


@dataclass(frozen=True)
class TwistedRelativeSolveTrace:
    """Execution trace of the Section 6-8 relative scalar-center twisted recursion."""

    status: str
    abort_reason: str | None
    top_ambient_class: int
    top_relative_class: int
    image_and_base_calls: int
    max_allowed_image_and_base_calls: int
    character_learning_batches: int
    max_allowed_character_batches: int
    original_copies_for_characters: int
    branch_log: tuple[dict[str, object], ...]
    m_chi_strict_shrink_flags: tuple[bool, ...]
    recovered_generators: tuple[tuple[int, ...], ...]
    recovered_character_on_generators: tuple[int, ...]


def unrolled_twisted_relative_solve(
    algebra: PublicLieAlgebra,
    ambient_basis: Sequence[Sequence[int]],
    *,
    single_copy_character_oracle: Callable[[tuple[int, ...]], int],
    relative_abelian_base_oracle: Callable[
        [
            PublicLieAlgebra,
            Sequence[tuple[int, ...]],
            Sequence[tuple[int, ...]],
            Sequence[int],
            Callable[[tuple[int, ...]], tuple[int, ...]],
        ],
        Sequence[tuple[int, ...]],
    ],
    twisted_image_oracle: Callable[
        [
            PublicLieAlgebra,
            Sequence[tuple[int, ...]],
            Sequence[tuple[int, ...]],
            Sequence[tuple[int, ...]],
            Sequence[int],
            str,
            Callable[[tuple[int, ...]], tuple[int, ...]],
        ],
        Sequence[tuple[int, ...]],
    ],
    initial_z_basis: Sequence[Sequence[int]] = (),
    initial_z_character: Sequence[int] = (),
    recover_final_bose_kernel: bool = False,
) -> TwistedRelativeSolveTrace:
    """Execute the Section 6-8 relative scalar-center recursion ``SolveTwisted(G, Z, chi_Z)``."""
    L_basis = algebra.span(ambient_basis)
    Z0_basis = algebra.span(initial_z_basis)
    top_c = algebra.nilpotency_class(L_basis)
    _, _, top_r = relative_quotient_algebra(algebra, L_basis, Z0_basis)
    max_image_base_calls = twisted_image_call_bound(top_r)
    max_char_batches = 2

    image_and_base_calls = 0
    char_batches = 0
    total_char_copies = 0
    branch_log: list[dict[str, object]] = []
    shrink_flags: list[bool] = []
    abort_state: list[str] = []

    def _solve_rel(
        curr_alg: PublicLieAlgebra,
        curr_basis: list[tuple[int, ...]],
        curr_z_basis: list[tuple[int, ...]],
        curr_z_char: tuple[int, ...],
        curr_lift: Callable[[tuple[int, ...]], tuple[int, ...]],
    ) -> list[tuple[int, ...]]:
        nonlocal image_and_base_calls, char_batches, total_char_copies
        if abort_state:
            return []

        G_span = curr_alg.span(curr_basis)
        Z_span = curr_alg.span(curr_z_basis)
        if len(Z_span) > 1:
            abort_state.append("SCALAR_CENTER_DIM_EXCEEDS_ONE")
            return []
        try:
            _, q_section, r_class = relative_quotient_algebra(curr_alg, G_span, Z_span)
        except Exception:
            abort_state.append("INVALID_RELATIVE_QUOTIENT")
            return []

        if r_class == 0:
            return _canonical_subspace_basis(Z_span, curr_alg.p)

        if r_class == 1:
            image_and_base_calls += 1
            if image_and_base_calls > max_image_base_calls:
                abort_state.append("IMAGE_OR_BASE_CALL_BUDGET_EXCEEDED")
                return []
            u_lifts = relative_abelian_base_oracle(
                curr_alg,
                Z_span,
                q_section,
                curr_z_char,
                curr_lift,
            )
            for u_vec in u_lifts:
                if not _subspace_contains(G_span, [u_vec], curr_alg.p):
                    abort_state.append("RELATIVE_BASE_LIFT_OUTSIDE_AMBIENT")
                    return []
            h_span = _canonical_subspace_basis(list(Z_span) + list(u_lifts), curr_alg.p)
            if Z_span and any(curr_z_char):
                for a, b in product(h_span, repeat=2):
                    if any(curr_alg.bracket(a, b)):
                        abort_state.append("RELATIVE_BASE_OUTPUT_NON_COMMUTING_ON_FAITHFUL_Z")
                        return []
            branch_log.append(
                {
                    "branch": "RELATIVE_ABELIAN_SCALAR_BASE",
                    "ambient_dim": len(G_span),
                    "relative_class": r_class,
                    "scalar_center_dim": len(Z_span),
                    "recovered_dim": len(h_span),
                }
            )
            return h_span

        G_derived = curr_alg.lower_central_series(G_span)[1]
        N_span = curr_alg.span(list(G_derived) + list(Z_span))
        n_abs_class = curr_alg.nilpotency_class(N_span)
        if n_abs_class > 3:
            abort_state.append("UNDERLYING_N_CLASS_EXCEEDS_THREE")
            return []
        _, _, n_rel_class = relative_quotient_algebra(curr_alg, N_span, Z_span)
        if n_rel_class > r_class // 2 or n_rel_class >= r_class:
            abort_state.append("RELATIVE_DERIVED_CLASS_DID_NOT_HALVE")
            return []

        K_span = _solve_rel(curr_alg, N_span, Z_span, curr_z_char, curr_lift)
        if abort_state:
            return []
        K_span = _canonical_subspace_basis(list(Z_span) + list(K_span), curr_alg.p)

        char_batches += 1
        if char_batches > max_char_batches:
            abort_state.append("CHARACTER_BATCH_BUDGET_EXCEEDED")
            return []
        try:
            chi_k, copies_used = learn_known_subalgebra_character_from_original_copies(
                curr_alg,
                K_span,
                lambda v: single_copy_character_oracle(curr_lift(v)),
            )
        except Exception:
            abort_state.append("INVALID_LEARNED_SUBALGEBRA_CHARACTER")
            return []
        total_char_copies += copies_used

        try:
            cn_quot = public_character_normalizer_quotient(
                curr_alg,
                G_span,
                K_span,
                chi_k,
                prior_z_basis=Z_span,
                prior_z_character=curr_z_char,
            )
        except Exception:
            abort_state.append("INVALID_CHARACTER_NORMALIZER_QUOTIENT")
            return []

        shrink_flags.append(cn_quot.m_chi_strictly_smaller_than_plain_normalizer)
        if not cn_quot.section_basis_in_ambient:
            return K_span

        s_alg = cn_quot.quotient_algebra
        s_basis = [
            tuple(int(i == j) for j in range(s_alg.dimension))
            for i in range(s_alg.dimension)
        ]
        z_new_basis = list(cn_quot.z_new_basis_in_quotient)
        z_new_char = cn_quot.z_new_character

        def s_lift(s_vec: tuple[int, ...]) -> tuple[int, ...]:
            return curr_lift(cn_quot.lift_to_ambient(s_vec))

        while True:
            _, q_sec, s_rel_class = relative_quotient_algebra(s_alg, s_basis, z_new_basis)
            if s_rel_class <= 1:
                break
            s_derived = s_alg.lower_central_series(s_basis)[1]
            n_s_basis = s_alg.span(list(s_derived) + list(z_new_basis))
            n_s_class = s_alg.nilpotency_class(n_s_basis)
            if n_s_class == 1:
                branch_name = "TWISTED_SCALAR_METABELIAN_IMAGE"
            elif n_s_class == 2:
                branch_name = "TWISTED_FULL_JET_CLASS_TWO_IMAGE"
            elif n_s_class == 3:
                branch_name = "TWISTED_FULL_JET_CLASS_THREE_IMAGE"
            else:
                abort_state.append("UNSUPPORTED_TWISTED_IMAGE_NORMAL_CLASS")
                return []

            image_and_base_calls += 1
            if image_and_base_calls > max_image_base_calls:
                abort_state.append("IMAGE_OR_BASE_CALL_BUDGET_EXCEEDED")
                return []

            v_section = _quotient_complement_basis(n_s_basis, s_basis, s_alg.dimension, s_alg.p)
            u_lifts = twisted_image_oracle(
                s_alg,
                n_s_basis,
                v_section,
                z_new_basis,
                z_new_char,
                branch_name,
                s_lift,
            )
            for u_vec in u_lifts:
                if not _subspace_contains(s_basis, [u_vec], s_alg.p):
                    abort_state.append("TWISTED_IMAGE_LIFT_OUTSIDE_AMBIENT")
                    return []
            preimage_T = s_alg.span(list(n_s_basis) + list(u_lifts))
            _, _, new_rel_class = relative_quotient_algebra(s_alg, preimage_T, z_new_basis)
            branch_log.append(
                {
                    "branch": branch_name,
                    "ambient_dim": len(s_basis),
                    "relative_class_before": s_rel_class,
                    "normal_n_s_dim": len(n_s_basis),
                    "normal_n_s_class": n_s_class,
                    "scalar_center_dim": len(z_new_basis),
                    "preimage_dim": len(preimage_T),
                    "relative_class_after": new_rel_class,
                }
            )
            if new_rel_class >= s_rel_class:
                abort_state.append("RELATIVE_IMAGE_CLASS_DID_NOT_DROP")
                return []
            s_basis = preimage_T

        _, q_sec_final, final_rel_class = relative_quotient_algebra(s_alg, s_basis, z_new_basis)
        if final_rel_class == 0:
            h_in_s = z_new_basis
        else:
            image_and_base_calls += 1
            if image_and_base_calls > max_image_base_calls:
                abort_state.append("IMAGE_OR_BASE_CALL_BUDGET_EXCEEDED")
                return []
            u_final = relative_abelian_base_oracle(
                s_alg,
                z_new_basis,
                q_sec_final,
                z_new_char,
                s_lift,
            )
            for u_vec in u_final:
                if not _subspace_contains(s_basis, [u_vec], s_alg.p):
                    abort_state.append("TERMINAL_BASE_LIFT_OUTSIDE_AMBIENT")
                    return []
            h_in_s = s_alg.span(list(z_new_basis) + list(u_final))
            branch_log.append(
                {
                    "branch": "RELATIVE_ABELIAN_SCALAR_BASE",
                    "ambient_dim": len(s_basis),
                    "relative_class": final_rel_class,
                    "scalar_center_dim": len(z_new_basis),
                    "recovered_dim": len(h_in_s),
                }
            )

        lifted_h = [cn_quot.lift_to_ambient(vec) for vec in h_in_s]
        return _canonical_subspace_basis(
            list(cn_quot.k0_kernel_basis_in_ambient) + lifted_h,
            curr_alg.p,
        )

    recovered = _solve_rel(
        algebra,
        L_basis,
        Z0_basis,
        tuple(initial_z_character),
        lambda v: tuple(v),
    )
    if abort_state:
        return TwistedRelativeSolveTrace(
            status="ABORT",
            abort_reason=abort_state[0],
            top_ambient_class=top_c,
            top_relative_class=top_r,
            image_and_base_calls=image_and_base_calls,
            max_allowed_image_and_base_calls=max_image_base_calls,
            character_learning_batches=char_batches,
            max_allowed_character_batches=max_char_batches + int(recover_final_bose_kernel),
            original_copies_for_characters=total_char_copies,
            branch_log=tuple(branch_log),
            m_chi_strict_shrink_flags=tuple(shrink_flags),
            recovered_generators=(),
            recovered_character_on_generators=(),
        )

    final_char: tuple[int, ...] = ()
    if recover_final_bose_kernel and recovered:
        char_batches += 1
        final_char, extra_copies = learn_known_subalgebra_character_from_original_copies(
            algebra,
            recovered,
            single_copy_character_oracle,
        )
        total_char_copies += extra_copies

    return TwistedRelativeSolveTrace(
        status="SUCCESS",
        abort_reason=None,
        top_ambient_class=top_c,
        top_relative_class=top_r,
        image_and_base_calls=image_and_base_calls,
        max_allowed_image_and_base_calls=max_image_base_calls,
        character_learning_batches=char_batches,
        max_allowed_character_batches=max_char_batches + int(recover_final_bose_kernel),
        original_copies_for_characters=total_char_copies,
        branch_log=tuple(branch_log),
        m_chi_strict_shrink_flags=tuple(shrink_flags),
        recovered_generators=tuple(recovered),
        recovered_character_on_generators=final_char,
    )


def _strict_upper_triangular_lie_algebra(n: int, p: int) -> tuple[PublicLieAlgebra, dict[tuple[int, int], int]]:
    """Build ``ut_n(F_p)`` with basis ``{(i, j) : 0 <= i < j < n}``."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    pair_to_idx = {pair: idx for idx, pair in enumerate(pairs)}
    dim = len(pairs)

    def bracket_fn(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        out = [0] * dim
        for idx_a, a_val in enumerate(left):
            if not a_val:
                continue
            i1, j1 = pairs[idx_a]
            for idx_b, b_val in enumerate(right):
                if not b_val or idx_a == idx_b:
                    continue
                i2, j2 = pairs[idx_b]
                prod_ab = a_val * b_val % p
                if j1 == i2:
                    pos = pair_to_idx[(i1, j2)]
                    out[pos] = (out[pos] + prod_ab) % p
                if j2 == i1:
                    pos = pair_to_idx[(i2, j1)]
                    out[pos] = (out[pos] - prod_ab) % p
        return tuple(out)

    return PublicLieAlgebra(p=p, dimension=dim, bracket_fn=bracket_fn), pair_to_idx


def build_twisted_relative_recursion_report() -> dict[str, object]:
    """Build the reproducible verification report for Milestone 18."""
    p_small = 7
    p_127 = (1 << 127) - 1
    heis_controls: list[dict[str, object]] = []
    for p_val in (p_small, p_127):
        heis = PublicLieAlgebra(
            p=p_val,
            dimension=3,
            bracket_fn=lambda a, b, pv=p_val: (0, 0, (a[0] * b[1] - a[1] * b[0]) % pv),
        )
        std3 = [tuple(int(i == j) for j in range(3)) for i in range(3)]
        k_heis = [std3[1], std3[2]]
        chi_heis = (3, 1)
        cnq = public_character_normalizer_quotient(heis, std3, k_heis, chi_heis)
        heis_controls.append(
            {
                "prime_bits": p_val.bit_length(),
                "plain_normalizer_dim": len(cnq.plain_normalizer_basis_in_ambient),
                "m_chi_dim": len(cnq.m_chi_basis_in_ambient),
                "k0_dim": len(cnq.k0_kernel_basis_in_ambient),
                "scalar_center_width": cnq.scalar_center_width,
                "m_chi_strictly_smaller": cnq.m_chi_strictly_smaller_than_plain_normalizer,
                "k0_ideal_in_plain_normalizer": cnq.k0_ideal_in_plain_normalizer,
                "k0_ideal_in_m_chi": cnq.k0_ideal_in_m_chi,
                "z_new_central_in_quotient": cnq.z_new_central_in_quotient,
                "relative_quotient_class": cnq.relative_quotient_class,
            }
        )

    rel_base_audit = verify_relative_abelian_quadratic_phase_erasure(p=7, slope_a=2, char_b=1)
    cascade_audit = verify_character_attached_weighted_cascade(p=23, quotient_width=1)

    p7 = 19
    ut7, idx7 = _strict_upper_triangular_lie_algebra(7, p7)
    std7 = [tuple(int(i == j) for j in range(ut7.dimension)) for i in range(ut7.dimension)]
    e01 = std7[idx7[(0, 1)]]
    e03 = std7[idx7[(0, 3)]]
    e24 = std7[idx7[(2, 4)]]
    target_H = _canonical_subspace_basis([e01, e03, e24], p7)
    ell_ambient = [0] * ut7.dimension
    ell_ambient[idx7[(0, 1)]] = 7
    ell_ambient[idx7[(0, 3)]] = 5
    ell_ambient[idx7[(2, 4)]] = 2

    def char_oracle(amb_vec: tuple[int, ...]) -> int:
        if not _subspace_contains(target_H, [amb_vec], p7):
            raise AssertionError("character oracle queried outside H")
        return sum(c * l_val for c, l_val in zip(amb_vec, ell_ambient)) % p7

    def rel_base_oracle(
        s_alg: PublicLieAlgebra,
        z_basis: Sequence[tuple[int, ...]],
        q_section: Sequence[tuple[int, ...]],
        z_char: Sequence[int],
        lift_fn: Callable[[tuple[int, ...]], tuple[int, ...]],
    ) -> Sequence[tuple[int, ...]]:
        s_span = s_alg.span(list(z_basis) + list(q_section))
        L_lifts = [lift_fn(v) for v in s_span]
        inter_L = _subspace_intersection(target_H, L_lifts, ut7.dimension, p7)
        recovered_in_s: list[tuple[int, ...]] = []
        for vec_L in inter_L:
            coords = _fmpz_solve_coordinates(L_lifts, vec_L, p7)
            assert coords is not None
            vec_s = tuple(
                sum(coords[i] * s_span[i][c] for i in range(len(s_span))) % p7
                for c in range(s_alg.dimension)
            )
            recovered_in_s.append(vec_s)
        return s_alg.span(recovered_in_s)

    def twisted_img_oracle(
        s_alg: PublicLieAlgebra,
        n_s_basis: Sequence[tuple[int, ...]],
        v_section: Sequence[tuple[int, ...]],
        z_basis: Sequence[tuple[int, ...]],
        z_char: Sequence[int],
        branch_name: str,
        lift_fn: Callable[[tuple[int, ...]], tuple[int, ...]],
    ) -> Sequence[tuple[int, ...]]:
        curr_s_span = s_alg.span(list(n_s_basis) + list(v_section))
        L_lifts = [lift_fn(v) for v in curr_s_span]
        inter_L = _subspace_intersection(target_H, L_lifts, ut7.dimension, p7)
        h_in_s: list[tuple[int, ...]] = []
        for vec_L in inter_L:
            coords = _fmpz_solve_coordinates(L_lifts, vec_L, p7)
            assert coords is not None
            vec_s = tuple(
                sum(coords[i] * curr_s_span[i][c] for i in range(len(curr_s_span))) % p7
                for c in range(s_alg.dimension)
            )
            h_in_s.append(vec_s)
        adapted = list(n_s_basis) + list(v_section)
        n_dim = len(n_s_basis)
        v_proj: list[tuple[int, ...]] = []
        for h_vec in h_in_s:
            coords = _fmpz_solve_coordinates(adapted, h_vec, p7)
            assert coords is not None
            v_vec = tuple(
                sum(coords[n_dim + j] * v_section[j][c] for j in range(len(v_section))) % p7
                for c in range(s_alg.dimension)
            )
            if any(v_vec):
                v_proj.append(v_vec)
        return s_alg.span(v_proj)

    trace_ut7 = unrolled_twisted_relative_solve(
        ut7,
        std7,
        single_copy_character_oracle=char_oracle,
        relative_abelian_base_oracle=rel_base_oracle,
        twisted_image_oracle=twisted_img_oracle,
        recover_final_bose_kernel=True,
    )
    assert trace_ut7.status == "SUCCESS"
    assert list(trace_ut7.recovered_generators) == target_H

    plan127 = plan_orbit_state_transfer(p_127**20, Fraction(1, 8), 1000, Fraction(1, 100))

    return {
        "schema_version": "twisted_relative_recursion_v1",
        "module": "theorems/twisted_relative_recursion.py",
        "scope": {
            "character_normalizer_quotient_verified": True,
            "plain_normalizer_k0_non_ideal_obstruction_verified": True,
            "relative_abelian_quadratic_phase_erasure_verified": True,
            "character_attached_weighted_erasure_verified": True,
            "unrolled_relative_scalar_center_recursion_verified": True,
            "original_copy_character_learning_enforced": True,
            "rare_sector_error_division_forbidden": True,
            "coherent_quantum_state_receiver_implemented": False,
            "accepted_speedup_candidate": False,
            "novelty_claim": False,
            "speedup_claim_allowed": False,
        },
        "heisenberg_character_normalizer_controls": heis_controls,
        "relative_abelian_base_audit": rel_base_audit,
        "character_attached_weighted_cascade_audit": cascade_audit,
        "unrolled_ut7_twisted_solve": {
            "status": trace_ut7.status,
            "top_ambient_class": trace_ut7.top_ambient_class,
            "top_relative_class": trace_ut7.top_relative_class,
            "image_and_base_calls": trace_ut7.image_and_base_calls,
            "max_allowed_image_and_base_calls": trace_ut7.max_allowed_image_and_base_calls,
            "character_learning_batches": trace_ut7.character_learning_batches,
            "max_allowed_character_batches": trace_ut7.max_allowed_character_batches,
            "original_copies_for_characters": trace_ut7.original_copies_for_characters,
            "m_chi_strict_shrink_flags": list(trace_ut7.m_chi_strict_shrink_flags),
            "recovered_generator_count": len(trace_ut7.recovered_generators),
            "recovered_character_on_generators": list(trace_ut7.recovered_character_on_generators),
            "branch_log": list(trace_ut7.branch_log),
        },
        "source_transfer_127bit_ledger": {
            "prime_bits": p_127.bit_length(),
            "copies_per_label": plan127.copies_per_label,
            "total_preparation_uses_bound": plan127.total_preparation_uses_bound,
            "hybrid_error_bound": str(plan127.hybrid_error_bound),
        },
    }


def render_markdown(report: dict[str, object]) -> str:
    h_small, h_127 = report["heisenberg_character_normalizer_controls"]
    rb = report["relative_abelian_base_audit"]
    ca = report["character_attached_weighted_cascade_audit"]
    u7 = report["unrolled_ut7_twisted_solve"]
    branch_rows = "\n".join(
        f"| `{idx + 1}` | `{row['branch']}` | `{row['ambient_dim']}` | `{row.get('relative_class_before', row.get('relative_class'))}` | `{row['scalar_center_dim']}` | `{row.get('relative_class_after', 0)}` |"
        for idx, row in enumerate(u7["branch_log"])
    )
    return f"""# Relative Scalar-Center Twisted Recursion, Quadratic-Phase Abelian Base, and Character-Attached Weighted Erasure

2026-10-21. **Standalone public algebra and unrolled recursion verification; not a complete quantum state-symmetry receiver, general SDE backend, novelty claim, or accepted speedup candidate.**

## 1. Summary and Mechanical Contracts Verified

This note documents `theorems/twisted_relative_recursion.py` and `tests/test_twisted_relative_recursion.py`, implementing the executable verification controls for `research/TWISTED_STATE_SYMMETRY_RECEIVER.md` and `## 2026-10-21 Twisted State Source Contract` in `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Character-Preserving Normalizer Quotient (`public_character_normalizer_quotient`)**:
   - Wraps `character_normalizer` (`theorems/twisted_state_source.py`) on an independently learned subgroup $K \\le H$ and character $\\chi_K$ learned from **original single copies** ($k = 1$).
   - Demonstrates on $\\mathfrak{{heis}}_3(\\mathbb{{F}}_p)$ ($p = 7$ and $p = 2^{{127}} - 1$) with $K = \\langle y, z \\rangle$ and $\\chi_K = (3, 1)$ that $K_0 = \\ker \\chi_K = \\langle y - 3z \\rangle$ is **not** an ideal of the plain normalizer $N_L(K) = L$ (`k0_ideal_in_plain_normalizer = False`), whereas $K_0$ is an ideal of $M_\\chi = \\{{x \\in L : [x, K] \\subseteq K_0\\}}$ (`k0_ideal_in_m_chi = True`) and $Z_{{\\text{{new}}}} = K / K_0$ is 1-dimensional central in $S = M_\\chi / K_0$.
2. **Relative Abelian Base Quadratic-Phase Erasure (`compile_relative_abelian_twisted_leaf`, `verify_relative_abelian_quadratic_phase_erasure`)**:
   - In the relative abelian base ($r = \\text{{class}}(G / Z) = 1$, $[G, G] \\subseteq Z$ with $\\dim Z \\le 1$), naive quotient Fourier sampling on $V = G / Z$ leaks $1 - 1/p = {rb["naive_fourier_mass_outside_annihilator"]}$ probability mass outside $U^\\perp$ due to the degree-2 central-extension section phase.
   - Erasing degree 2 and degree 1 via `ordinary_higher_degree_erasure_stage` reduces the packet degree to `{rb["erased_packet_final_degree"]}` and concentrates `{rb["erased_fourier_mass_inside_annihilator"]}` of the Fourier mass on $U^\\perp$.
3. **Character-Attached Weighted Erasure & Two-Stage Cascade (`compile_twisted_full_jet_leaf`, `verify_character_attached_weighted_cascade`)**:
   - Connects `attach_linear_character` to `PinnedWeightedPacket`, `weighted_erasure_stage`, and `transition_to_fourier_residual` (`theorems/weighted_two_erasure_cascade.py`).
   - Verifies that the $m = {ca["quotient_width"]}$ appended unknown character parameters (`{ca["base_parameter_count"]} -> {ca["twisted_parameter_count"]}`) have nonconstant weight `{ca["character_term_weights"]}`, are completely erased at Stage-1 weight-1 erasure (`erased_root_weighted_degree = {ca["erased_root_weighted_degree"]}`), and leave zero character parameters in the post-Fourier Stage-2 residual (`post_fourier_residual_contains_character_params = {ca["post_fourier_residual_contains_character_params"]}`).
4. **Unrolled Relative Scalar-Center Recursion (`unrolled_twisted_relative_solve`)**:
   - Tracks progress by the relative quotient class $r = \\text{{class}}(G / Z)$, enforces the Section 8 call bound $I(r) \\le I(\\min(3, \\lfloor r/2 \\rfloor)) + r$ (`{u7["image_and_base_calls"]} <= {u7["max_allowed_image_and_base_calls"]}` on $\\mathfrak{{ut}}_7(\\mathbb{{F}}_{{19}})$) and character-batch bound (`{u7["character_learning_batches"]} <= {u7["max_allowed_character_batches"]}`), and recovers $H = \\langle E_{{01}}, E_{{03}}, E_{{24}} \\rangle \\le \\mathfrak{{ut}}_7(\\mathbb{{F}}_{{19}})$ together with its character `{u7["recovered_character_on_generators"]}`.

## 2. Heisenberg Character-Normalizer & Relative Abelian Base Controls

| Control Check | Result |
| :--- | :--- |
| Heisenberg ($p=7$ / $127$-bit) $\\dim N_L(K)$ vs $\\dim M_\\chi$ | `{h_small["plain_normalizer_dim"]}` vs `{h_small["m_chi_dim"]}` (`{h_127["plain_normalizer_dim"]}` vs `{h_127["m_chi_dim"]}` at 127 bits) |
| $K_0 = \\ker \\chi_K$ ideal in $N_L(K)$ vs ideal in $M_\\chi$ | `{h_small["k0_ideal_in_plain_normalizer"]}` vs `{h_small["k0_ideal_in_m_chi"]}` |
| Naive quotient Fourier leakage outside $U^\\perp$ ($p = {rb["p"]}$) | `{rb["naive_fourier_mass_outside_annihilator"]}` (exact $1 - 1/p = {rb["theoretical_naive_leakage_1_minus_1_over_p"]}$) |
| Post-quadratic-erasure Fourier mass inside / outside $U^\\perp$ | `{rb["erased_fourier_mass_inside_annihilator"]}` / `{rb["erased_fourier_mass_outside_annihilator"]}` |

## 3. Unrolled Relative Twisted Recursion Trace on $\\mathfrak{{ut}}_7(\\mathbb{{F}}_{{19}})$ ($c = 6$)

| Step | Dispatched Branch | Ambient $\\dim S$ | Relative Class Before | $\\dim Z_{{\\text{{new}}}}$ | Relative Class After |
| :--- | :--- | :--- | :--- | :--- | :--- |
{branch_rows}

## 4. Explicit Scope Boundaries

- Related literature context: [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2) and [Liu, Carrasco, Eisert, and Bellante (2026)](https://arxiv.org/abs/2609.35656) study quantum state symmetry learning and sample vs unitary access models; [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016) provide the fixed-degree SDE framework.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown artifacts.")
    args = parser.parse_args()
    report = build_twisted_relative_recursion_report()
    if args.write:
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        MD_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"module": report["module"], "schema_version": report["schema_version"]}, indent=2))


if __name__ == "__main__":
    main()
