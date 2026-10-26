"""Ambient Lie filtration certifier, M/K normalizer-quotient transport, unrolled Solve(L,f) recursion, and two-tree resource audit.

This standalone module implements the group-frontend obligations, unified
Section 7.1-7.3 recursion, and resource/obstruction controls documented in
``research/CLASS_THREE_MONOMIAL_FULL_JET.md`` and
``research/MECHANICAL_FOLLOW_UP_PLAN.md`` (``## 2026-10-21 Unified Recursion
Contract`` and ``## 2026-10-21 Class-Three Monomial Full-Jet Contract``):

1. **Public Ambient Filtration & Center Certifier (Supporting Class-Two B=0 and Class-Three N)**:
   - Extracts ``N = [L, L]``, computes the exact center ``C = Z(N)`` via
     arbitrary-precision ``fmpz_mod_mat`` kernel equations over ``GF(p)``,
     verifies ``2 <= class(N) <= 3``, certifies ``gamma_{c-1}(L) <= Z(N)``,
     rejects proper subspaces of ``Z(N)``, and builds the verified
     ``ClassThreeStructure`` (with ``B = 0, beta = (), delta = ((), ..., ())``
     when ``class(N) == 2``) and ``FullTaylorJetChart`` for ``D = c - 2``.
2. **Legitimate M/K Normalizer-Quotient Constructor (Without Assuming N <= M)**:
   - Computes ``M = N_L(K) = {x in L : [x, K] <= K}`` publicly over ``GF(p)``,
     records whether ``N <= M`` (which is FALSE in general when ``N`` is
     nonabelian, e.g. ``K = <E13>`` in ``ut_7`` where ``E35 in N \\ M``),
     constructs ``S = M / K`` with an explicit public linear section lift into
     ``L``, and verifies ``S' = (M' + K)/K <= (N intersect M)/K`` and
     ``class(S') <= class(N) <= 3``.
3. **Unrolled Solve(L, f) Arbitrary-H Controller (Section 7.1-7.3)**:
   - Unrolls ``K := Solve(N, f|_{exp(N)})`` to the abelian base case without
     receiving ``K`` as hidden advice, dispatches each image step to
     ``SCALAR_METABELIAN_IMAGE`` (``class(S') == 1``),
     ``FULL_JET_CLASS_TWO_NORMAL_IMAGE`` (``class(S') == 2, B = 0``), or
     ``FULL_JET_CLASS_THREE_NORMAL_IMAGE`` (``class(S') == 3, B != 0``), and
     verifies the call cap ``<= c + 1`` image calls and ``<= 3`` abelian HSP
     calls with additive across-call query accounting.
4. **Two-Tree Resource Audit & Class-Four Normal Frequency-Motion Obstruction**:
   - Computes the Section 7 two-tree resource envelope with Ivanyos--Santha
     collision recurrences and verifies that class-4 normal groups retain
     carrier-dependent B-Fourier frequency shifts.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from math import comb, log2
from pathlib import Path
from typing import Callable, Sequence

from theorems.class_three_monomial_jet import (
    ClassThreeStructure,
    FullTaylorJetChart,
)
from theorems.full_jet_resource_certificate import (
    certificate_report,
    full_jet_resource_certificate,
    sde_arity,
)
from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import (
    PublicLieAlgebra,
    _canonical_vec,
    _fmpz_nullspace_basis,
    _fmpz_row_space_basis,
    _fmpz_solve_coordinates,
)


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "research" / "reductions" / "class_three_ambient_frontend.json"
MD_PATH = ROOT / "research" / "CLASS_THREE_AMBIENT_FRONTEND.md"


def _subspace_contains(
    container_basis: Sequence[Sequence[int]],
    vectors: Sequence[Sequence[int]],
    p: int,
) -> bool:
    """Return True iff every vector in ``vectors`` lies in ``span(container_basis)``."""
    for vec in vectors:
        if _fmpz_solve_coordinates(container_basis, vec, p) is None:
            return False
    return True


def _quotient_complement_basis(
    subspace_basis: Sequence[Sequence[int]],
    ambient_basis: Sequence[Sequence[int]],
    dimension: int,
    p: int,
) -> list[tuple[int, ...]]:
    """Select basis vectors from ``ambient_basis`` completing ``subspace_basis``."""
    sub = _fmpz_row_space_basis(subspace_basis, dimension, p)
    amb = _fmpz_row_space_basis(ambient_basis, dimension, p)
    if not _subspace_contains(amb, sub, p):
        raise ValueError("subspace_basis must be contained in ambient_basis")
    combined = _fmpz_row_space_basis(list(sub) + list(amb), dimension, p)
    return combined[len(sub) :]


def _subspace_intersection(
    first_basis: Sequence[Sequence[int]],
    second_basis: Sequence[Sequence[int]],
    dimension: int,
    p: int,
) -> list[tuple[int, ...]]:
    """Compute a basis of ``span(first_basis) intersect span(second_basis)`` in F_p^dimension."""
    u = _fmpz_row_space_basis(first_basis, dimension, p)
    v = _fmpz_row_space_basis(second_basis, dimension, p)
    if not u or not v:
        return []
    # Solve sum_{i=0}^{len(u)-1} a_i u_i - sum_{j=0}^{len(v)-1} b_j v_j = 0
    total_cols = len(u) + len(v)
    equations = [
        [u[i][coord] % p for i in range(len(u))]
        + [(-v[j][coord]) % p for j in range(len(v))]
        for coord in range(dimension)
    ]
    null_vecs = _fmpz_nullspace_basis(equations, total_cols, p)
    inter_vecs = [
        tuple(
            sum(coeff[i] * u[i][coord] for i in range(len(u))) % p
            for coord in range(dimension)
        )
        for coeff in null_vecs
    ]
    return _fmpz_row_space_basis(inter_vecs, dimension, p)


def compute_subalgebra_center(
    algebra: PublicLieAlgebra,
    subalgebra_basis: Sequence[Sequence[int]],
) -> list[tuple[int, ...]]:
    """Compute the exact center ``Z(N) = {x in N : [x, y] = 0 for all y in N}`` over GF(p)."""
    basis = algebra.span(subalgebra_basis)
    n_dim = len(basis)
    if n_dim == 0:
        return []
    equations: list[list[int]] = []
    for k in range(n_dim):
        brackets_with_k = [algebra.bracket(basis[j], basis[k]) for j in range(n_dim)]
        for coord in range(algebra.dimension):
            row = [brackets_with_k[j][coord] % algebra.p for j in range(n_dim)]
            if any(row):
                equations.append(row)
    null_coords = _fmpz_nullspace_basis(equations, n_dim, algebra.p)
    center_vectors = [
        tuple(
            sum(coeff[j] * basis[j][coord] for j in range(n_dim)) % algebra.p
            for coord in range(algebra.dimension)
        )
        for coeff in null_coords
    ]
    return algebra.span(center_vectors)


def compute_subalgebra_normalizer(
    algebra: PublicLieAlgebra,
    ambient_basis: Sequence[Sequence[int]],
    target_basis: Sequence[Sequence[int]],
) -> list[tuple[int, ...]]:
    """Compute ``N_L(K) = {x in L : [x, K] <= K}`` using exact linear equations over GF(p)."""
    L_basis = algebra.span(ambient_basis)
    K_basis = algebra.span(target_basis)
    if not _subspace_contains(L_basis, K_basis, algebra.p):
        raise ValueError("target K must be contained in ambient L")
    l_dim = len(L_basis)
    if l_dim == 0:
        return []
    if not K_basis:
        return L_basis
    # Complete K_basis to ambient F_p^dimension to project modulo K
    std_all = [tuple(int(i == j) for j in range(algebra.dimension)) for i in range(algebra.dimension)]
    complement = _quotient_complement_basis(K_basis, std_all, algebra.dimension, algebra.p)
    if not complement:
        return L_basis
    adapted_full = list(K_basis) + list(complement)
    k_dim = len(K_basis)

    equations: list[list[int]] = []
    for k_vec in K_basis:
        # For each basis element L_basis[j], express [L_basis[j], k_vec] in adapted_full
        proj_cols: list[tuple[int, ...]] = []
        for l_vec in L_basis:
            br = algebra.bracket(l_vec, k_vec)
            coords = _fmpz_solve_coordinates(adapted_full, br, algebra.p)
            assert coords is not None
            proj_cols.append(coords[k_dim:])
        for q_coord in range(len(complement)):
            row = [proj_cols[j][q_coord] % algebra.p for j in range(l_dim)]
            if any(row):
                equations.append(row)
    null_coords = _fmpz_nullspace_basis(equations, l_dim, algebra.p)
    norm_vectors = [
        tuple(
            sum(coeff[j] * L_basis[j][coord] for j in range(l_dim)) % algebra.p
            for coord in range(algebra.dimension)
        )
        for coeff in null_coords
    ]
    return algebra.span(norm_vectors)


@dataclass(frozen=True)
class PublicNormalizerQuotient:
    """Legitimate quotient Lie algebra ``S = M / K`` where ``M = N_L(K)``."""

    quotient_algebra: PublicLieAlgebra
    normalizer_basis: tuple[tuple[int, ...], ...]
    kernel_basis: tuple[tuple[int, ...], ...]
    section_basis_in_ambient: tuple[tuple[int, ...], ...]
    derived_entirely_in_normalizer: bool
    quotient_derived_basis: tuple[tuple[int, ...], ...]
    n_intersect_m_quotient_basis: tuple[tuple[int, ...], ...]
    quotient_derived_in_n_intersect_m: bool
    quotient_class: int
    quotient_derived_class: int

    def lift_to_ambient(self, quotient_vec: Sequence[int]) -> tuple[int, ...]:
        """Public linear section sigma: S = M/K -> M <= L (need not be a homomorphism)."""
        s_dim = len(self.section_basis_in_ambient)
        _canonical_vec(quotient_vec, s_dim, self.quotient_algebra.p)
        if not s_dim:
            return ()
        amb_dim = len(self.section_basis_in_ambient[0])
        return tuple(
            sum(quotient_vec[j] * self.section_basis_in_ambient[j][coord] for j in range(s_dim))
            % self.quotient_algebra.p
            for coord in range(amb_dim)
        )

    def project_from_normalizer(self, ambient_vec_in_m: Sequence[int]) -> tuple[int, ...]:
        """Project an element of M = N_L(K) to S = M/K coordinates."""
        adapted = list(self.kernel_basis) + list(self.section_basis_in_ambient)
        coords = _fmpz_solve_coordinates(adapted, ambient_vec_in_m, self.quotient_algebra.p)
        if coords is None:
            raise ValueError("supplied ambient vector does not lie in M = N_L(K)")
        return tuple(coords[len(self.kernel_basis) :])


def public_normalizer_quotient_algebra(
    algebra: PublicLieAlgebra,
    ambient_basis: Sequence[Sequence[int]],
    k_basis: Sequence[Sequence[int]],
) -> PublicNormalizerQuotient:
    """Construct ``M = N_L(K)`` and ``S = M/K`` following Section 7.2 of ``CLASS_THREE_MONOMIAL_FULL_JET.md``.

    Does NOT assume ``N = [L, L] <= M``. Instead verifies that ``K`` is a Lie
    subalgebra of ``N``, forms ``M = N_L(K)``, checks whether ``N <= M``, and
    certifies that ``S' = (M' + K)/K`` is contained in ``(N intersect M)/K``
    with ``class(S') <= class(N)``.
    """
    L_basis = algebra.span(ambient_basis)
    N_basis = algebra.lower_central_series(L_basis)[1]
    K_span = algebra.span(k_basis)
    if not _subspace_contains(L_basis, K_span, algebra.p):
        raise ValueError("K must be a subspace of L")
    for k1, k2 in product(K_span, repeat=2):
        if not _subspace_contains(K_span, [algebra.bracket(k1, k2)], algebra.p):
            raise ValueError("K must be a Lie subalgebra closed under brackets")

    M_basis = compute_subalgebra_normalizer(algebra, L_basis, K_span)
    n_in_m = _subspace_contains(M_basis, N_basis, algebra.p)
    section_in_L = _quotient_complement_basis(K_span, M_basis, algebra.dimension, algebra.p)
    adapted_M = list(K_span) + list(section_in_L)
    k_dim = len(K_span)
    s_dim = len(section_in_L)

    if s_dim == 0:
        # Quotient M/K is 0-dimensional; represent as 1D zero-bracket algebra if needed or handle directly
        q_alg = PublicLieAlgebra(p=algebra.p, dimension=1, bracket_fn=lambda a, b: (0,))
        return PublicNormalizerQuotient(
            quotient_algebra=q_alg,
            normalizer_basis=tuple(M_basis),
            kernel_basis=tuple(K_span),
            section_basis_in_ambient=(),
            derived_entirely_in_normalizer=n_in_m,
            quotient_derived_basis=(),
            n_intersect_m_quotient_basis=(),
            quotient_derived_in_n_intersect_m=True,
            quotient_class=0,
            quotient_derived_class=0,
        )

    # Precompute structure constants of S = M/K in section_in_L basis
    bracket_table: list[list[tuple[int, ...]]] = [
        [(0,) * s_dim for _ in range(s_dim)] for _ in range(s_dim)
    ]
    for i in range(s_dim):
        for j in range(i + 1, s_dim):
            br = algebra.bracket(section_in_L[i], section_in_L[j])
            coords = _fmpz_solve_coordinates(adapted_M, br, algebra.p)
            if coords is None:
                raise ArithmeticError("normalizer M = N_L(K) failed bracket closure")
            q_br = tuple(coords[k_dim:])
            bracket_table[i][j] = q_br
            bracket_table[j][i] = tuple((-x) % algebra.p for x in q_br)

    def q_bracket(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        out = [0] * s_dim
        for i, u in enumerate(left):
            if not u:
                continue
            for j, v in enumerate(right):
                if not v or i == j:
                    continue
                uv = u * v % algebra.p
                row = bracket_table[i][j]
                for c in range(s_dim):
                    out[c] = (out[c] + uv * row[c]) % algebra.p
        return tuple(out)

    q_alg = PublicLieAlgebra(p=algebra.p, dimension=s_dim, bracket_fn=q_bracket)
    q_std = [tuple(int(i == j) for j in range(s_dim)) for i in range(s_dim)]
    q_series = q_alg.lower_central_series(q_std)
    q_class = max(0, len(q_series) - 1)
    q_derived = q_series[1] if len(q_series) > 1 else []
    q_derived_class = q_alg.nilpotency_class(q_derived) if q_derived else 0

    n_inter_m = _subspace_intersection(N_basis, M_basis, algebra.dimension, algebra.p)
    n_inter_m_quot: list[tuple[int, ...]] = []
    for vec in n_inter_m:
        coords = _fmpz_solve_coordinates(adapted_M, vec, algebra.p)
        assert coords is not None
        n_inter_m_quot.append(tuple(coords[k_dim:]))
    n_inter_m_quot_span = q_alg.span(n_inter_m_quot)
    s_prime_in_n_inter_m = _subspace_contains(n_inter_m_quot_span, q_derived, algebra.p)

    return PublicNormalizerQuotient(
        quotient_algebra=q_alg,
        normalizer_basis=tuple(M_basis),
        kernel_basis=tuple(K_span),
        section_basis_in_ambient=tuple(section_in_L),
        derived_entirely_in_normalizer=n_in_m,
        quotient_derived_basis=tuple(q_derived),
        n_intersect_m_quotient_basis=tuple(n_inter_m_quot_span),
        quotient_derived_in_n_intersect_m=s_prime_in_n_inter_m,
        quotient_class=q_class,
        quotient_derived_class=q_derived_class,
    )


@dataclass(frozen=True)
class CertifiedAmbientClassThreeDecomposition:
    """Verified decomposition of an ambient Lie algebra L with 2 <= class(L') <= 3."""

    p: int
    ambient_dimension: int
    ambient_class: int
    quotient_width: int
    derived_dimension: int
    derived_class: int
    jet_degree: int
    weighted_phase_degree: int
    a_basis: tuple[tuple[int, ...], ...]
    b_basis: tuple[tuple[int, ...], ...]
    c_basis: tuple[tuple[int, ...], ...]
    quotient_section_basis: tuple[tuple[int, ...], ...]
    structure: ClassThreeStructure
    chart: FullTaylorJetChart
    center_exact: bool
    gamma_c_minus_1_in_center: bool
    b_is_empty_class_two_branch: bool
    lower_class_three_intersection_dependency: bool = True


def certify_ambient_class_three_derived(
    algebra: PublicLieAlgebra,
    ambient_basis: Sequence[Sequence[int]],
    *,
    proposed_c_basis: Sequence[Sequence[int]] | None = None,
) -> CertifiedAmbientClassThreeDecomposition:
    """Certify that ``L`` satisfies the Section 2 & 7.1 premises of ``CLASS_THREE_MONOMIAL_FULL_JET.md``.

    Supports both:
    - ``class(N) == 3`` (nonempty ``B = (N' + C) / C``), and
    - ``class(N) == 2`` (``B = 0, beta = (), delta = ((), ..., ())``) via the
      unified full-jet GL compiler without phantom registers or source-label SDEs.
    """
    L_basis = algebra.span(ambient_basis)
    L_series = algebra.lower_central_series(L_basis)
    c = max(0, len(L_series) - 1)
    if c < 4:
        raise ValueError(f"class-three full-jet frontend requires ambient class c >= 4 (got {c})")
    D = c - 2
    if algebra.p <= max(c, 3 * D):
        raise ValueError(
            f"conservative full-jet scope requires p > max(c, 3*(c-2)) = {max(c, 3 * D)} (got p={algebra.p})"
        )

    N_basis = L_series[1]
    N_series = algebra.lower_central_series(N_basis)
    n_class = max(0, len(N_series) - 1)
    if n_class > 3:
        raise ValueError(f"derived subalgebra N=[L,L] has class {n_class} > 3")
    if n_class < 2:
        raise ValueError("derived subalgebra N=[L,L] is abelian; use the metabelian scalar branch")

    exact_center = compute_subalgebra_center(algebra, N_basis)
    if proposed_c_basis is not None:
        supplied_c = algebra.span(proposed_c_basis)
        if not _subspace_contains(exact_center, supplied_c, algebra.p):
            raise ValueError("proposed C basis is not central in N=[L,L]")
        if len(supplied_c) != len(exact_center) or not _subspace_contains(supplied_c, exact_center, algebra.p):
            raise ValueError("proposed C basis is a proper subspace of Z(N); full center C=Z(N) required")
        C_basis = supplied_c
    else:
        C_basis = exact_center

    if not C_basis:
        raise ValueError("nonempty center Z(N) required")

    gamma_c_minus_1 = L_series[c - 2]
    if not _subspace_contains(C_basis, gamma_c_minus_1, algebra.p):
        raise ValueError("ambient filtration check failed: gamma_{c-1}(L) is not contained in C=Z(N)")

    N_derived = N_series[1]  # N' = [N, N]
    N_prime_plus_C = algebra.span(list(C_basis) + list(N_derived))
    B_basis = _quotient_complement_basis(C_basis, N_prime_plus_C, algebra.dimension, algebra.p)
    A_basis = _quotient_complement_basis(N_prime_plus_C, N_basis, algebra.dimension, algebra.p)
    V_basis = _quotient_complement_basis(N_basis, L_basis, algebra.dimension, algebra.p)

    if not A_basis:
        raise ValueError("nonempty A = N/(N'+C) required for ClassThreeStructure")
    if n_class == 3 and not B_basis:
        raise ValueError("class-3 N=[L,L] requires nonempty B = (N'+C)/C")

    for b1, b2 in product(B_basis, repeat=2):
        if any(algebra.bracket(b1, b2)):
            raise ValueError("B = (N'+C)/C section must be abelian ([B, B] = 0)")
    for a_vec, b_vec in product(A_basis, B_basis):
        ab = algebra.bracket(a_vec, b_vec)
        if not _subspace_contains(C_basis, [ab], algebra.p):
            raise ValueError("bracket [A, B] must lie in C = Z(N)")

    adapted_N = list(A_basis) + list(B_basis) + list(C_basis)
    r, s, z = len(A_basis), len(B_basis), len(C_basis)

    beta_list = [[[0] * r for _ in range(r)] for _ in range(s)]
    gamma_list = [[[0] * r for _ in range(r)] for _ in range(z)]
    delta_list = [[[0] * s for _ in range(r)] for _ in range(z)]

    for i in range(r):
        for j in range(r):
            br = algebra.bracket(A_basis[i], A_basis[j])
            coords = _fmpz_solve_coordinates(adapted_N, br, algebra.p)
            if coords is None or any(coords[:r]):
                raise ValueError("[A, A] must lie in B + C")
            for b_idx in range(s):
                beta_list[b_idx][i][j] = coords[r + b_idx] % algebra.p
            for c_idx in range(z):
                gamma_list[c_idx][i][j] = coords[r + s + c_idx] % algebra.p

    for i in range(r):
        for b_idx in range(s):
            br = algebra.bracket(A_basis[i], B_basis[b_idx])
            coords = _fmpz_solve_coordinates(adapted_N, br, algebra.p)
            if coords is None or any(coords[: r + s]):
                raise ValueError("[A, B] must lie in C")
            for c_idx in range(z):
                delta_list[c_idx][i][b_idx] = coords[r + s + c_idx] % algebra.p

    structure = ClassThreeStructure(
        p=algebra.p,
        beta=tuple(tuple(tuple(row) for row in form) for form in beta_list),
        gamma=tuple(tuple(tuple(row) for row in form) for form in gamma_list),
        delta=tuple(tuple(tuple(row) for row in form) for form in delta_list),
    )
    chart = FullTaylorJetChart(
        p=algebra.p,
        quotient_width=len(V_basis),
        noncentral_width=r,
        degree=D,
    )
    return CertifiedAmbientClassThreeDecomposition(
        p=algebra.p,
        ambient_dimension=len(L_basis),
        ambient_class=c,
        quotient_width=len(V_basis),
        derived_dimension=len(N_basis),
        derived_class=n_class,
        jet_degree=D,
        weighted_phase_degree=max(c, 3 * D),
        a_basis=tuple(A_basis),
        b_basis=tuple(B_basis),
        c_basis=tuple(C_basis),
        quotient_section_basis=tuple(V_basis),
        structure=structure,
        chart=chart,
        center_exact=True,
        gamma_c_minus_1_in_center=True,
        b_is_empty_class_two_branch=(s == 0),
    )


@dataclass(frozen=True)
class UnrolledSolveTrace:
    """Execution trace of the Section 7.1-7.3 Solve(L, f) recursion."""

    status: str
    abort_reason: str | None
    top_ambient_class: int
    top_derived_class: int
    abelian_hsp_calls: int
    image_calls: int
    max_allowed_image_calls: int
    max_allowed_abelian_calls: int
    image_branch_log: tuple[dict[str, object], ...]
    normalizer_n_in_m_flags: tuple[bool, ...]
    recovered_generators: tuple[tuple[int, ...], ...]
    additive_across_calls_only: bool = True


def unrolled_full_jet_solve(
    algebra: PublicLieAlgebra,
    ambient_basis: Sequence[Sequence[int]],
    *,
    abelian_hsp_oracle: Callable[[PublicLieAlgebra, Sequence[tuple[int, ...]], Callable[[tuple[int, ...]], tuple[int, ...]]], Sequence[tuple[int, ...]]],
    quotient_image_oracle: Callable[[PublicLieAlgebra, Sequence[tuple[int, ...]], Sequence[tuple[int, ...]], str, Callable[[tuple[int, ...]], tuple[int, ...]]], Sequence[tuple[int, ...]]],
    lift_to_root: Callable[[tuple[int, ...]], tuple[int, ...]] | None = None,
) -> UnrolledSolveTrace:
    """Execute the unrolled ``Solve(L, f)`` recursion from Section 7.1 of ``CLASS_THREE_MONOMIAL_FULL_JET.md``.

    - Never takes ``K = H intersect L'`` as hidden advice; instead calls
      ``Solve(N, f|_{exp(N)})`` recursively down to the abelian base case.
    - Uses ``public_normalizer_quotient_algebra`` to form ``S = M/K`` (where
      ``M = N_L(K)``) without assuming ``N <= M``, and recomputes ``S'`` inside
      ``(N intersect M)/K``.
    - Dispatches each image step in the ``while S is nonabelian`` loop to:
      * ``SCALAR_METABELIAN_IMAGE`` when ``class(S') == 1``,
      * ``FULL_JET_CLASS_TWO_NORMAL_IMAGE`` when ``class(S') == 2`` (``B = 0``),
      * ``FULL_JET_CLASS_THREE_NORMAL_IMAGE`` when ``class(S') == 3`` (``B != 0``).
    - Requires a strict class drop ``class(T) < class(S)`` on every image step
      (where ``T = U + S'`` includes ``[S', S'] <= gamma_3(S)``) and enforces the
      Section 7.3 call bounds ``image_calls <= c + 1`` and ``abelian_calls <= 3``.
    """
    L_basis = algebra.span(ambient_basis)
    top_c = algebra.nilpotency_class(L_basis)
    L_series = algebra.lower_central_series(L_basis)
    top_n_class = algebra.nilpotency_class(L_series[1]) if len(L_series) > 1 else 0
    max_images = max(1, top_c + 1)
    max_abelian = 3

    abelian_calls = 0
    image_calls = 0
    image_log: list[dict[str, object]] = []
    n_in_m_flags: list[bool] = []
    abort_state: list[str] = []

    root_lift = lift_to_root if lift_to_root is not None else (lambda v: tuple(v))

    def _solve_recursive(
        curr_alg: PublicLieAlgebra,
        curr_basis: list[tuple[int, ...]],
        curr_lift: Callable[[tuple[int, ...]], tuple[int, ...]],
    ) -> list[tuple[int, ...]]:
        nonlocal abelian_calls, image_calls
        if abort_state:
            return []
        curr_span = curr_alg.span(curr_basis)
        curr_class = curr_alg.nilpotency_class(curr_span)
        if curr_class > 1:
            curr_n = curr_alg.lower_central_series(curr_span)[1]
            if curr_alg.nilpotency_class(curr_n) > 3:
                abort_state.append("DERIVED_CLASS_EXCEEDS_THREE")
                return []

        if curr_class <= 1:
            abelian_calls += 1
            if abelian_calls > max_abelian:
                abort_state.append("ABELIAN_CALL_BUDGET_EXCEEDED")
                return []
            if not curr_span:
                return []
            gens = abelian_hsp_oracle(curr_alg, curr_span, curr_lift)
            for g in gens:
                if not _subspace_contains(curr_span, [g], curr_alg.p):
                    abort_state.append("MALFORMED_ABELIAN_GENERATOR")
                    return []
            return curr_alg.span(gens)

        # Nonabelian L: N = L', K = Solve(N, f|_{exp(N)})
        N_basis = curr_alg.lower_central_series(curr_span)[1]
        n_class = curr_alg.nilpotency_class(N_basis)
        if n_class >= curr_class:
            abort_state.append("INTERSECTION_RECURSION_CLASS_DID_NOT_DROP")
            return []
        K_basis = _solve_recursive(curr_alg, N_basis, curr_lift)
        if abort_state:
            return []

        try:
            norm_quot = public_normalizer_quotient_algebra(curr_alg, curr_span, K_basis)
        except Exception:
            abort_state.append("INVALID_NORMALIZER_QUOTIENT")
            return []
        n_in_m_flags.append(norm_quot.derived_entirely_in_normalizer)
        if not norm_quot.quotient_derived_in_n_intersect_m:
            abort_state.append("QUOTIENT_DERIVED_OUTSIDE_N_INTERSECT_M")
            return []

        if not norm_quot.section_basis_in_ambient:
            return K_basis

        s_alg = norm_quot.quotient_algebra
        s_basis = [
            tuple(int(i == j) for j in range(s_alg.dimension))
            for i in range(s_alg.dimension)
        ]

        def s_lift(s_vec: tuple[int, ...]) -> tuple[int, ...]:
            return curr_lift(norm_quot.lift_to_ambient(s_vec))

        while s_alg.nilpotency_class(s_basis) > 1:
            s_class = s_alg.nilpotency_class(s_basis)
            s_series = s_alg.lower_central_series(s_basis)
            s_derived = s_series[1]
            s_derived_class = s_alg.nilpotency_class(s_derived)
            if s_derived_class == 1:
                branch_name = "SCALAR_METABELIAN_IMAGE"
            elif s_derived_class == 2:
                branch_name = "FULL_JET_CLASS_TWO_NORMAL_IMAGE"
            elif s_derived_class == 3:
                branch_name = "FULL_JET_CLASS_THREE_NORMAL_IMAGE"
            else:
                abort_state.append("UNSUPPORTED_QUOTIENT_DERIVED_CLASS")
                return []

            image_calls += 1
            if image_calls > max_images:
                abort_state.append("IMAGE_CALL_BUDGET_EXCEEDED")
                return []

            v_section = _quotient_complement_basis(s_derived, s_basis, s_alg.dimension, s_alg.p)
            u_lifts = quotient_image_oracle(s_alg, s_derived, v_section, branch_name, s_lift)
            for u_vec in u_lifts:
                if not _subspace_contains(s_basis, [u_vec], s_alg.p):
                    abort_state.append("IMAGE_LIFT_OUTSIDE_CURRENT_AMBIENT")
                    return []
            preimage_T = s_alg.span(list(s_derived) + list(u_lifts))
            new_class = s_alg.nilpotency_class(preimage_T)
            image_log.append(
                {
                    "branch": branch_name,
                    "ambient_dim": len(s_basis),
                    "ambient_class": s_class,
                    "derived_dim": len(s_derived),
                    "derived_class": s_derived_class,
                    "preimage_dim": len(preimage_T),
                    "preimage_class": new_class,
                }
            )
            if new_class >= s_class:
                abort_state.append("IMAGE_PREIMAGE_CLASS_DID_NOT_DROP")
                return []
            s_basis = preimage_T

        abelian_calls += 1
        if abelian_calls > max_abelian:
            abort_state.append("ABELIAN_CALL_BUDGET_EXCEEDED")
            return []
        r_gens_in_s = abelian_hsp_oracle(s_alg, s_basis, s_lift) if s_basis else []
        for g in r_gens_in_s:
            if not _subspace_contains(s_basis, [g], s_alg.p):
                abort_state.append("MALFORMED_TERMINAL_ABELIAN_GENERATOR")
                return []
        lifted_r = [norm_quot.lift_to_ambient(g) for g in r_gens_in_s]
        return curr_alg.span(list(K_basis) + lifted_r)

    recovered = _solve_recursive(algebra, L_basis, root_lift)
    if abort_state:
        return UnrolledSolveTrace(
            status="ABORT",
            abort_reason=abort_state[0],
            top_ambient_class=top_c,
            top_derived_class=top_n_class,
            abelian_hsp_calls=abelian_calls,
            image_calls=image_calls,
            max_allowed_image_calls=max_images,
            max_allowed_abelian_calls=max_abelian,
            image_branch_log=tuple(image_log),
            normalizer_n_in_m_flags=tuple(n_in_m_flags),
            recovered_generators=(),
        )
    return UnrolledSolveTrace(
        status="SUCCESS",
        abort_reason=None,
        top_ambient_class=top_c,
        top_derived_class=top_n_class,
        abelian_hsp_calls=abelian_calls,
        image_calls=image_calls,
        max_allowed_image_calls=max_images,
        max_allowed_abelian_calls=max_abelian,
        image_branch_log=tuple(image_log),
        normalizer_n_in_m_flags=tuple(n_in_m_flags),
        recovered_generators=tuple(recovered),
    )


def ivanyos_santha_sde_arity(degree: int, equations: int) -> int:
    """Published all-input fixed-degree SDE arity from Ivanyos--Santha Theorem 11 / Theorem 3."""
    return sde_arity(degree, equations)


def class_three_full_jet_resource_budget(
    *,
    p: int,
    ambient_class: int,
    quotient_width: int,
    a_width: int,
    b_width: int,
    c_width: int,
    epsilon: Fraction = Fraction(1, 8),
) -> dict[str, object]:
    """Use the exact capped certificate; retain logarithms only as display metrics."""
    certificate = full_jet_resource_certificate(
        p=p, ambient_class=ambient_class, quotient_width=quotient_width,
        a_width=a_width, b_width=b_width, c_width=c_width, epsilon=epsilon,
        support_model="generic",  # keep this comparison on the same historical envelope
    )
    c = ambient_class
    D = c - 2
    m, r, s, z = quotient_width, a_width, b_width, c_width
    ell, J, b0 = certificate.features, certificate.jet_width, certificate.batch
    rank_fail = Fraction(1, 4 * p)  # uniform theorem bound; avoid enormous decimal fractions
    e, h, h_lift = certificate.phase_degree, certificate.parameters, certificate.lifted_parameters
    e_weighted, e_ordinary = certificate.weighted_equations, certificate.ordinary_equations

    weighted_arities = {j: ivanyos_santha_sde_arity(j, e_weighted) for j in range(1, e + 1)}
    ordinary_arities_full = {j: ivanyos_santha_sde_arity(j, e_ordinary) for j in range(1, D + 1)}
    ordinary_arities_d_minus_1 = {j: ivanyos_santha_sde_arity(j, e_ordinary) for j in range(1, D)}

    weighted_tree_product = 1
    for val in weighted_arities.values():
        weighted_tree_product *= val
    ordinary_tree_product = 1
    for val in ordinary_arities_full.values():
        ordinary_tree_product *= val

    e_class_two = max(c, 2 * D - 1)
    ell_class_two = comb(m + D - 1, m + 1) if D >= 2 else 0
    v_class_two = m + (r + s) * ell_class_two
    e_weighted_class_two = h_lift * comb(v_class_two + e_class_two, e_class_two)
    class_two_weighted_product = 1
    for j in range(1, e_class_two + 1):
        class_two_weighted_product *= ivanyos_santha_sde_arity(j, e_weighted_class_two)
    class_two_ordinary_product = 1
    for val in ordinary_arities_d_minus_1.values():
        class_two_ordinary_product *= val

    t_samples = certificate.roots
    matrix_leaves_M = certificate.leaves
    raw_queries_upper = certificate.queries

    return {
        "p": p,
        "ambient_class": c,
        "jet_degree_D": D,
        "weighted_phase_degree_e": e,
        "class_two_weighted_degree_comparison": e_class_two,
        "quotient_width_m": m,
        "a_width_r": r,
        "b_width_s": s,
        "c_width_z": z,
        "scalar_feature_count_ell": ell,
        "full_jet_width_J": J,
        "matrix_batch_sources_b0": b0,
        "matrix_batch_rank_failure_bound": str(rank_fail),
        "base_parameter_count_h": h,
        "lifted_parameter_count_Hlift": h_lift,
        "weighted_equation_bound_Ew": e_weighted,
        "ordinary_equation_bound_Eo": e_ordinary,
        "second_erasure_degrees": list(range(D, 0, -1)),
        "weighted_erasure_degrees": list(range(e, 0, -1)),
        "log2_weighted_tree_leaves": round(log2(weighted_tree_product), 2),
        "log2_ordinary_tree_leaves_full_D": round(log2(ordinary_tree_product), 2),
        "log2_ordinary_tree_leaves_wrong_D_minus_1": round(log2(class_two_ordinary_product), 2),
        "log2_total_matrix_leaves_M": round(log2(matrix_leaves_M), 2),
        "log2_raw_queries_upper_bound": round(log2(raw_queries_upper), 2),
        "log2_class_two_tree_leaves_comparison": round(
            log2(t_samples * class_two_ordinary_product * class_two_weighted_product), 2
        ),
        "full_jet_tree_exceeds_class_two_tree": (
            ordinary_tree_product * weighted_tree_product
            > class_two_ordinary_product * class_two_weighted_product
        ),
        "max_image_calls_c_plus_1": c + 1,
        "max_abelian_hsp_calls": 3,
        "arbitrary_H_intersection_requires_class_three_receiver": True,
        "known_nil2_intersection_sufficient": False,
        "adaptive_resource_certificate": certificate_report(certificate),
    }


def class_four_normal_frequency_motion_probe(p: int = 11) -> dict[str, object]:
    """Demonstrate why a class-4 normal group N breaks pure x-independent B-Fourier translation."""
    ring(p)
    if p <= 5:
        raise ValueError("probe requires p > 5")
    half = pow(2, -1, p)
    inv6 = pow(6, -1, p)

    def bch_c_increment(a0: int, a1: int, b1: int, b2: int, x0: int, x1: int, y1: int, y2: int) -> int:
        w2 = half * (a0 * y2 - x0 * b2) % p
        w3_y1_coeff = half * a0 * x0 % p
        return (w2 + w3_y1_coeff * y1 + inv6 * a0 * a0 * x0 * (a1 - x1)) % p

    lam = 1
    a0, a1, b1, b2 = 2, 1, 0, 0
    shifts_by_x0: dict[int, int] = {}
    for x0 in range(p):
        c0 = bch_c_increment(a0, a1, b1, b2, x0, 0, 0, 0)
        c1 = bch_c_increment(a0, a1, b1, b2, x0, 0, 1, 0)
        slope_y1 = (lam * (c1 - c0)) % p
        shifts_by_x0[x0] = slope_y1

    distinct_shifts = len(set(shifts_by_x0.values()))
    return {
        "prime": p,
        "normal_group_class": 4,
        "carrier_x0_to_mu1_shift": {str(k): v for k, v in shifts_by_x0.items()},
        "distinct_mu1_shifts_across_carrier_x0": distinct_shifts,
        "x_independent_translation_holds": distinct_shifts == 1,
        "obstruction": (
            "In class-4 N, [A, [A, B_1]] <= C = Z(N) couples carrier x in A and y_1 in B_1 "
            "into C, so negative Fourier on B_1 shifts mu_1 by a carrier-dependent term "
            "proportional to lambda * a_0 * x_0 rather than a pure displacement D_lambda(a)."
        ),
    }


def make_ut6_ambient_algebra(p: int = 17) -> tuple[PublicLieAlgebra, list[tuple[int, ...]], list[tuple[int, int]]]:
    """Construct the 15-dimensional strictly upper-triangular Lie algebra ut_6(F_p) (ambient class 5, class(N)=2)."""
    ring(p)
    slots = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    slot_idx = {pair: idx for idx, pair in enumerate(slots)}
    dim = len(slots)

    def bracket_fn(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        out = [0] * dim
        for (i, j), u in zip(slots, left):
            if not u:
                continue
            for (k, l), v in zip(slots, right):
                if not v:
                    continue
                if j == k:
                    out[slot_idx[(i, l)]] = (out[slot_idx[(i, l)]] + u * v) % p
                if l == i:
                    out[slot_idx[(k, j)]] = (out[slot_idx[(k, j)]] - u * v) % p
        return tuple(out)

    algebra = PublicLieAlgebra(p=p, dimension=dim, bracket_fn=bracket_fn)
    std_basis = [tuple(int(i == j) for j in range(dim)) for i in range(dim)]
    return algebra, std_basis, slots


def make_ut7_ambient_algebra(p: int = 19) -> tuple[PublicLieAlgebra, list[tuple[int, ...]], list[tuple[int, int]]]:
    """Construct the 21-dimensional strictly upper-triangular Lie algebra ut_7(F_p) (ambient class 6, class(N)=3)."""
    ring(p)
    slots = [(i, j) for i in range(7) for j in range(i + 1, 7)]
    slot_idx = {pair: idx for idx, pair in enumerate(slots)}
    dim = len(slots)

    def bracket_fn(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
        out = [0] * dim
        for (i, j), u in zip(slots, left):
            if not u:
                continue
            for (k, l), v in zip(slots, right):
                if not v:
                    continue
                if j == k:
                    out[slot_idx[(i, l)]] = (out[slot_idx[(i, l)]] + u * v) % p
                if l == i:
                    out[slot_idx[(k, j)]] = (out[slot_idx[(k, j)]] - u * v) % p
        return tuple(out)

    algebra = PublicLieAlgebra(p=p, dimension=dim, bracket_fn=bracket_fn)
    std_basis = [tuple(int(i == j) for j in range(dim)) for i in range(dim)]
    return algebra, std_basis, slots


def build_class_three_ambient_frontend_report() -> dict[str, object]:
    """Build the reproducible verification report for Milestone 16 (schema v2)."""
    alg7, basis7, slots7 = make_ut7_ambient_algebra(19)
    cert7 = certify_ambient_class_three_derived(alg7, basis7)

    # Also certify ut_6(F_17) via the unified B=0 class-two-normal branch!
    alg6, basis6, _ = make_ut6_ambient_algebra(17)
    cert6 = certify_ambient_class_three_derived(alg6, basis6)

    # Execute the unrolled Solve(L, f) controller on UT_7(F_19) with nonabelian-intersection
    # subgroup H = <E12, E13>, where K = H intersect N = <E13> and N is NOT contained in M = N_L(K)!
    e12_idx = slots7.index((0, 1))
    e13_idx = slots7.index((0, 2))
    hidden_H_in_root = [
        tuple(int(i == e12_idx) for i in range(len(slots7))),
        tuple(int(i == e13_idx) for i in range(len(slots7))),
    ]

    def ideal_abelian_oracle(
        curr_alg: PublicLieAlgebra,
        curr_span: Sequence[tuple[int, ...]],
        curr_lift: Callable[[tuple[int, ...]], tuple[int, ...]],
    ) -> Sequence[tuple[int, ...]]:
        # Lift curr_span to root L, intersect with hidden_H_in_root, and map back to curr_span
        lifted_span = [curr_lift(v) for v in curr_span]
        inter_root = _subspace_intersection(lifted_span, hidden_H_in_root, len(slots7), curr_alg.p)
        out: list[tuple[int, ...]] = []
        for root_vec in inter_root:
            coords = _fmpz_solve_coordinates(lifted_span, root_vec, curr_alg.p)
            assert coords is not None
            local_vec = tuple(
                sum(coords[j] * curr_span[j][c] for j in range(len(curr_span))) % curr_alg.p
                for c in range(curr_alg.dimension)
            )
            out.append(local_vec)
        return out

    def ideal_image_oracle(
        s_alg: PublicLieAlgebra,
        s_derived: Sequence[tuple[int, ...]],
        v_section: Sequence[tuple[int, ...]],
        branch_name: str,
        s_lift: Callable[[tuple[int, ...]], tuple[int, ...]],
    ) -> Sequence[tuple[int, ...]]:
        adapted_s = list(s_derived) + list(v_section)
        lifted_s = [s_lift(v) for v in adapted_s]
        inter_root = _subspace_intersection(lifted_s, hidden_H_in_root, len(slots7), s_alg.p)
        u_lifts: list[tuple[int, ...]] = []
        for root_vec in inter_root:
            coords = _fmpz_solve_coordinates(lifted_s, root_vec, s_alg.p)
            assert coords is not None
            v_coords = coords[len(s_derived) :]
            if any(v_coords):
                u_vec = tuple(
                    sum(v_coords[j] * v_section[j][c] for j in range(len(v_section))) % s_alg.p
                    for c in range(s_alg.dimension)
                )
                u_lifts.append(u_vec)
        return s_alg.span(u_lifts)

    solve_trace = unrolled_full_jet_solve(
        alg7,
        basis7,
        abelian_hsp_oracle=ideal_abelian_oracle,
        quotient_image_oracle=ideal_image_oracle,
    )

    budget7 = class_three_full_jet_resource_budget(
        p=cert7.p,
        ambient_class=cert7.ambient_class,
        quotient_width=cert7.quotient_width,
        a_width=cert7.structure.a_width,
        b_width=cert7.structure.b_width,
        c_width=cert7.structure.c_width,
    )
    obstruction = class_four_normal_frequency_motion_probe(11)

    return {
        "schema_version": "class_three_ambient_frontend_v2",
        "module": "theorems/class_three_ambient_frontend.py",
        "scope": {
            "ambient_filtration_and_center_certifier": True,
            "class_two_empty_B_branch_supported": True,
            "proper_center_subspace_rejected": True,
            "normalizer_quotient_M_over_K_without_N_in_M": True,
            "unrolled_solve_recursion_verified": True,
            "two_tree_resource_audit_with_full_D_second_erasure": True,
            "class_four_normal_frequency_motion_obstruction": True,
            "lower_class_three_intersection_dependency_explicit": True,
            "coherent_quantum_circuit_compiler": False,
            "general_prime_sde_backend": False,
            "accepted_speedup_candidate": False,
            "novelty_claim": False,
            "speedup_claim_allowed": False,
        },
        "ut7_ambient_certification": {
            "prime": cert7.p,
            "ambient_dimension": cert7.ambient_dimension,
            "ambient_class": cert7.ambient_class,
            "quotient_width_m": cert7.quotient_width,
            "derived_dimension": cert7.derived_dimension,
            "derived_class": cert7.derived_class,
            "a_width_r": cert7.structure.a_width,
            "b_width_s": cert7.structure.b_width,
            "c_width_z": cert7.structure.c_width,
            "jet_degree_D": cert7.jet_degree,
            "weighted_phase_degree_e": cert7.weighted_phase_degree,
            "full_jet_width_J": cert7.chart.jet_width,
            "center_exact": cert7.center_exact,
            "gamma_c_minus_1_in_center": cert7.gamma_c_minus_1_in_center,
            "b_is_empty_class_two_branch": cert7.b_is_empty_class_two_branch,
        },
        "ut6_class_two_empty_B_certification": {
            "prime": cert6.p,
            "ambient_dimension": cert6.ambient_dimension,
            "ambient_class": cert6.ambient_class,
            "quotient_width_m": cert6.quotient_width,
            "derived_dimension": cert6.derived_dimension,
            "derived_class": cert6.derived_class,
            "a_width_r": cert6.structure.a_width,
            "b_width_s": cert6.structure.b_width,
            "c_width_z": cert6.structure.c_width,
            "jet_degree_D": cert6.jet_degree,
            "full_jet_width_J": cert6.chart.jet_width,
            "b_is_empty_class_two_branch": cert6.b_is_empty_class_two_branch,
        },
        "ut7_unrolled_solve_recursion": {
            "status": solve_trace.status,
            "top_ambient_class": solve_trace.top_ambient_class,
            "top_derived_class": solve_trace.top_derived_class,
            "abelian_hsp_calls": solve_trace.abelian_hsp_calls,
            "max_allowed_abelian_calls": solve_trace.max_allowed_abelian_calls,
            "image_calls": solve_trace.image_calls,
            "max_allowed_image_calls": solve_trace.max_allowed_image_calls,
            "normalizer_n_in_m_flags": list(solve_trace.normalizer_n_in_m_flags),
            "image_branch_log": list(solve_trace.image_branch_log),
            "recovered_generator_count": len(solve_trace.recovered_generators),
        },
        "ut7_two_tree_resource_audit": budget7,
        "class_four_normal_obstruction_control": obstruction,
    }


def render_markdown(report: dict[str, object]) -> str:
    c7 = report["ut7_ambient_certification"]
    c6 = report["ut6_class_two_empty_B_certification"]
    rec = report["ut7_unrolled_solve_recursion"]
    b7 = report["ut7_two_tree_resource_audit"]
    obs = report["class_four_normal_obstruction_control"]
    return f"""# Ambient Filtration Certifier, Unrolled Solve(L,f) Recursion, Two-Tree Resource Audit, and Class-Four Normal Obstruction

2026-10-21. **Standalone public frontend verifier, normalizer-quotient constructor, unrolled recursion controller, and resource/obstruction audit; not a coherent quantum circuit compiler, general-prime SDE solver, novelty claim, or accepted speedup candidate.**

## 1. Summary and Mechanical Gaps Closed

This note documents `theorems/class_three_ambient_frontend.py` (`class_three_ambient_frontend_v2`) and `tests/test_class_three_ambient_frontend.py`, addressing the frontend certification, `M/K` normalizer-quotient, unrolled `Solve(L,f)` recursion, and resource-comparison obligations in `research/CLASS_THREE_MONOMIAL_FULL_JET.md` (Sections 2 & 7.1–7.3) and `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Ambient Filtration and Exact Center Certifier (`certify_ambient_class_three_derived`)**:
   - Extracts $N = [L, L]$ and its exact center $C = Z(N)$ via arbitrary-precision `fmpz_mod_mat` linear equations over $\\mathbb{{F}}_p$, rejects proper subspaces $C \\subsetneq Z(N)$, certifies $\\gamma_{{c-1}}(L) \\subseteq Z(N)$, and constructs the verified `ClassThreeStructure` and `FullTaylorJetChart` for both $\\text{{class}}(N) = 3$ ($B \\ne 0$, e.g. $\\mathfrak{{ut}}_7(\\mathbb{{F}}_{{19}})$ with $(r, s, z) = (9, 2, 4)$) and $\\text{{class}}(N) = 2$ ($B = 0, \\beta = (), \\delta = ((), \\dots, ())$, e.g. $\\mathfrak{{ut}}_6(\\mathbb{{F}}_{{17}})$ with $(r, s, z) = ({c6["a_width_r"]}, {c6["b_width_s"]}, {c6["c_width_z"]})$).
2. **Legitimate $M/K$ Normalizer-Quotient Constructor & Unrolled `Solve(L,f)` Recursion (`public_normalizer_quotient_algebra`, `unrolled_full_jet_solve`)**:
   - Implements Section 7.1–7.2 without assuming $N \\subseteq M = N_L(K)$: on $\\mathfrak{{ut}}_7(\\mathbb{{F}}_{{19}})$ with $H = \\langle E_{{12}}, E_{{13}} \\rangle$ and $K = H \\cap N = \\langle E_{{13}} \\rangle$, $N \\subseteq M$ is `False` ($E_{{35}} \\in N \\setminus M$), yet $S = M/K$ is well-defined and its derived ideal $S' = (M' + K)/K$ lies inside $(N \\cap M)/K$.
   - Unrolls `K := Solve(N, f|_{{exp(N)}})` down to the abelian base case without receiving hidden $K$ as advice, completing inside `{rec["image_calls"]} <= {rec["max_allowed_image_calls"]}` image calls and `{rec["abelian_hsp_calls"]} <= {rec["max_allowed_abelian_calls"]}` abelian HSP calls.
3. **Two-Tree Resource Audit & Class-Four Normal Subgroup Obstruction**:
   - Computes the Section 7 two-tree resource envelope with Ivanyos–Santha collision recurrences and verifies that class-4 normal groups retain carrier-dependent $B$-Fourier frequency shifts (`{obs["distinct_mu1_shifts_across_carrier_x0"]}` distinct $\\mu_1$ shifts across $x_0 \\in \\mathbb{{F}}_{{11}}$).

## 2. Certified $\\mathfrak{{ut}}_7(\\mathbb{{F}}_{{19}})$ & $\\mathfrak{{ut}}_6(\\mathbb{{F}}_{{17}})$ Frontend and Unrolled Recursion

| Metric | Value |
| :--- | :--- |
| $\\mathfrak{{ut}}_7(\\mathbb{{F}}_{{19}})$ $(c, m, \\dim N, \\text{{class}}(N))$ | `({c7["ambient_class"]}, {c7["quotient_width_m"]}, {c7["derived_dimension"]}, {c7["derived_class"]})` |
| $\\mathfrak{{ut}}_7(\\mathbb{{F}}_{{19}})$ $(r, s, z)$ / full jet width $J$ | `({c7["a_width_r"]}, {c7["b_width_s"]}, {c7["c_width_z"]})` / `{c7["full_jet_width_J"]}` |
| $\\mathfrak{{ut}}_6(\\mathbb{{F}}_{{17}})$ unified $B=0$ $(r, s, z)$ / full jet width $J$ | `({c6["a_width_r"]}, {c6["b_width_s"]}, {c6["c_width_z"]})` / `{c6["full_jet_width_J"]}` |
| Unrolled `Solve(ut_7)` status / recovered generators | `{rec["status"]}` / `{rec["recovered_generator_count"]}` |
| Unrolled `Solve(ut_7)` image calls / abelian HSP calls | `{rec["image_calls"]} / {rec["max_allowed_image_calls"]}` and `{rec["abelian_hsp_calls"]} / {rec["max_allowed_abelian_calls"]}` |
| `N <= M = N_L(K)` flags across normalizer quotients | `{rec["normalizer_n_in_m_flags"]}` |
| $\\log_2$ weighted tree / $\\log_2$ ordinary tree ($j=1..{c7["jet_degree_D"]}$) | `{b7["log2_weighted_tree_leaves"]}` / `{b7["log2_ordinary_tree_leaves_full_D"]}` |
| $\\log_2$ total matrix leaves $M$ / raw queries upper bound | `{b7["log2_total_matrix_leaves_M"]}` / `{b7["log2_raw_queries_upper_bound"]}` |

## 3. Explicit Scope Boundaries

- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown artifacts.")
    args = parser.parse_args()
    report = build_class_three_ambient_frontend_report()
    if args.write:
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        MD_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"module": report["module"], "schema_version": report["schema_version"]}, indent=2))


if __name__ == "__main__":
    main()
