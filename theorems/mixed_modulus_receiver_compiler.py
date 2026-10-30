"""Finite mixed-modulus reference checks and conditional error-budget arithmetic.

Character turns and budgets use exact Fractions; dense QFTs and projectors are
floating-point reference matrices, not scalable gate synthesis. Neither these
checks nor the allocator certify a hidden-subgroup source, ambient centrality,
or a physical receiver. The cyclic-QFT implementation remains an external premise.
"""
from __future__ import annotations

from collections.abc import Collection, Sequence
from dataclasses import dataclass
from fractions import Fraction
import itertools
import math
import cmath
from typing import Any, Callable, Optional

import numpy as np
from flint import fmpz

from theorems.pilot_receiver_policy import flagged_error_bound

# Absolute numerical tolerance, not an implemented channel-error allowance.
TOL = 1e-10


def is_prime(n: int) -> bool:
    """Primality check using the project's existing FLINT dependency."""
    if type(n) is not int or n < 2:
        return False
    return bool(fmpz(n).is_prime())


@dataclass(frozen=True)
class MixedModulusCenterSpec:
    """Public mixed-modulus coordinate specification for Z = direct_sum_j Z/p^{a_j}Z.

    Identifies Z^\\wedge \\cong Z using ONLY public coordinate generators e_j
    and exponents a_j, with NO hidden subgroup advice.
    """
    p: int
    exponents: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.p) is not int or self.p < 2 or not is_prime(self.p):
            raise ValueError(f"p must be a prime integer >= 2, got {self.p}")
        if not isinstance(self.exponents, tuple):
            object.__setattr__(self, "exponents", tuple(self.exponents))
        if not self.exponents:
            raise ValueError("exponents tuple must be non-empty")
        for a in self.exponents:
            if type(a) is not int or a < 1:
                raise ValueError(f"all exponents a_j must be integers >= 1, got {a}")

    @property
    def rank(self) -> int:
        """Cyclic rank R of the center."""
        return len(self.exponents)

    @property
    def moduli(self) -> tuple[int, ...]:
        """Component moduli (p^{a_1}, ..., p^{a_R})."""
        return tuple(self.p ** a for a in self.exponents)

    @property
    def order(self) -> int:
        """Total center order |Z| = prod_j p^{a_j}."""
        return math.prod(self.moduli)

    def elements(self) -> list[tuple[int, ...]]:
        """All center elements in deterministic lexicographic order."""
        return list(itertools.product(*(range(m) for m in self.moduli)))

    def canonical(self, z: Sequence[int]) -> tuple[int, ...]:
        """Componentwise canonical reduction z_j mod p^{a_j}."""
        if not isinstance(z, Sequence) or any(type(zj) is not int for zj in z):
            raise ValueError("coordinates must be a sequence of integers (not bools or floats)")
        if len(z) != self.rank:
            raise ValueError(f"expected coordinate tuple of length {self.rank}, got {len(z)}")
        return tuple(zj % m for zj, m in zip(z, self.moduli))

    def add(self, z1: Sequence[int], z2: Sequence[int]) -> tuple[int, ...]:
        """Componentwise addition modulo p^{a_j}."""
        c1 = self.canonical(z1)
        c2 = self.canonical(z2)
        return tuple((a + b) % m for a, b, m in zip(c1, c2, self.moduli))

    def neg(self, z: Sequence[int]) -> tuple[int, ...]:
        """Componentwise additive inverse modulo p^{a_j}."""
        c = self.canonical(z)
        return tuple((-a) % m for a, m in zip(c, self.moduli))

    def scale(self, s: int, degree: int, z: Sequence[int]) -> tuple[int, ...]:
        """Rees dilation Delta_s(z)_j = s^{degree} * z_j mod p^{a_j}."""
        if type(s) is not int:
            raise ValueError(f"scale s must be an integer, got {s}")
        if type(degree) is not int or degree < 0:
            raise ValueError(f"degree must be a non-negative integer, got {degree}")
        c = self.canonical(z)
        return tuple((pow(s, degree, m) * zj) % m for zj, m in zip(c, self.moduli))

    def phase_turn(self, y: Sequence[int], z: Sequence[int]) -> Fraction:
        """Exact rational turn sum_{j=1}^R (y_j * z_j / p^{a_j}) mod 1 in [0, 1)."""
        cy = self.canonical(y)
        cz = self.canonical(z)
        total = sum(Fraction(yj * zj, m) for yj, zj, m in zip(cy, cz, self.moduli))
        return Fraction(total.numerator % total.denominator, total.denominator)

    def character_value(self, y: Sequence[int], z: Sequence[int]) -> complex:
        """Complex character evaluation chi_y(z) = exp(2pi * i * phase_turn(y, z))."""
        turn = self.phase_turn(y, z)
        return cmath.exp(2j * math.pi * float(turn))

    def verify_public_dual_bijection(self) -> dict[str, object]:
        """Verify that {y -> chi_y} forms an orthonormal character basis for Z.

        Checks:
        1. Character orthogonality: sum_{z in Z} conj(chi_y(z)) chi_{y'}(z) = |Z| delta_{y, y'}
        2. Dual completeness: sum_{y in Z} conj(chi_y(z)) chi_y(z') = |Z| delta_{z, z'}
        using ONLY public coordinate exponents with NO hidden subgroup advice.
        """
        elems = self.elements()
        n = len(elems)
        # Construct character matrix U_{y, z} = chi_y(z)
        U = np.zeros((n, n), dtype=complex)
        for i, y in enumerate(elems):
            for j, z in enumerate(elems):
                U[i, j] = self.character_value(y, z)

        prod_rows = U @ U.conj().T
        ortho_err = float(np.max(np.abs(prod_rows - n * np.eye(n))))
        prod_cols = U.conj().T @ U
        comp_err = float(np.max(np.abs(prod_cols - n * np.eye(n))))

        if ortho_err >= TOL or comp_err >= TOL:
            raise ArithmeticError(
                f"character pairing dual bijection failed: ortho_err={ortho_err}, comp_err={comp_err}"
            )

        return {
            "order": self.order,
            "rank": self.rank,
            "moduli": self.moduli,
            "orthogonality_max_error": ortho_err,
            "completeness_max_error": comp_err,
            "characters_verified": n,
            "verified": True,
        }


def qft_matrix(dimension: int) -> np.ndarray:
    """Floating-point dense reference matrix for the standard cyclic QFT."""
    if type(dimension) is not int or dimension < 1:
        raise ValueError(f"positive integer dimension required, got {dimension}")
    idx = np.arange(dimension)
    return np.exp(2j * math.pi * np.outer(idx, idx) / dimension) / np.sqrt(dimension)


def product_qft_matrix(spec: MixedModulusCenterSpec) -> np.ndarray:
    """Numerical dense reference for tensor_prod_j QFT_{p^{a_j}}."""
    mat = np.array([[1.0 + 0.0j]], dtype=complex)
    for m in spec.moduli:
        mat = np.kron(mat, qft_matrix(m))
    return mat


def _validate_central_intersection(
    spec: MixedModulusCenterSpec, central_intersection: Collection[Sequence[int]]
) -> tuple[tuple[int, ...], ...]:
    items = tuple(central_intersection)
    coords = tuple(spec.canonical(item) for item in items)
    if not coords:
        raise ValueError("central_intersection must be nonempty")
    if any(tuple(item) != coord for item, coord in zip(items, coords)):
        raise ValueError("central_intersection coordinates must be canonical")
    members = set(coords)
    if len(members) != len(coords):
        raise ValueError("central_intersection coordinates must be unique")
    if (0,) * spec.rank not in members:
        raise ValueError("central_intersection must contain the identity")
    if any(spec.add(a, b) not in members for a in coords for b in coords):
        raise ValueError("central_intersection must be closed under addition")
    return coords


def _validate_density(density: np.ndarray, n_group: int) -> np.ndarray:
    """Check physicality numerically, without repairing or normalizing the input.

    TOL is an absolute bound on trace error and entrywise Hermiticity error;
    every eigenvalue of the Hermitian part must be >= -TOL. Outcome imaginary
    parts, range violations and normalization errors are separately bounded by
    TOL below. Passing these finite checks is not a coset-state certificate.
    """
    rho = np.asarray(density, dtype=complex)
    if rho.shape != (n_group, n_group):
        raise ValueError(f"density shape {rho.shape} must match ({n_group}, {n_group})")
    if not np.all(np.isfinite(rho)):
        raise ValueError("density entries must be finite")
    trace = np.trace(rho)
    if not np.isfinite(trace) or abs(trace - 1.0) > TOL:
        raise ValueError("density trace must be 1.0 within TOL")
    herm_error = float(np.max(np.abs(rho - rho.conj().T)))
    if not math.isfinite(herm_error) or herm_error > TOL:
        raise ValueError("density must be Hermitian within TOL")
    eigenvalues = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    if not np.all(np.isfinite(eigenvalues)) or eigenvalues.min() < -TOL:
        raise ValueError("density must be positive semidefinite within TOL")
    return rho


def compile_mixed_modulus_instrument(
    spec: MixedModulusCenterSpec,
    n_group: int,
    right_shift: Callable[[int, tuple[int, ...]], int],
    central_intersection: Optional[Collection[Sequence[int]]] = None,
    density: Optional[np.ndarray] = None,
) -> dict[str, Any]:
    """Numerically check a finite free Z-action and its spectral instrument.

    ``right_shift(x, z)`` must give a free permutation representation on the
    n_group basis labels. Identity, composition and freeness are checked exactly
    as finite permutation identities. No ambient multiplication is available,
    so neither an ambient group law nor centrality is certified.

    ``central_intersection`` is explicit H intersect Z data for a reference
    check, not arbitrary H or advice used to build the measurement. It must be
    a nonempty subgroup of unique canonical coordinate tuples. Without a
    supplied density, construct the uniform mixture of its normalized orbit
    vectors. This central-subgroup orbit density is not the general rho_H.
    A supplied density is only checked for numerical physicality; commutation
    is reported separately. If intersection data is present, check its predicted
    character distribution, without inferring a hidden-subgroup source.

    All matrices are numerical references with absolute tolerance TOL. For
    D = |Z| * n_group the full ancilla unitary has D**2 complex entries and
    dense multiplication costs O(D**3); these are not scalable gate circuits.
    """
    if type(n_group) is not int or n_group < 1:
        raise ValueError(f"positive n_group required, got {n_group}")
    if not callable(right_shift):
        raise ValueError("callable right_shift required")

    h_coords = (None if central_intersection is None else
                _validate_central_intersection(spec, central_intersection))
    rho = None if density is None else _validate_density(density, n_group)
    density_source = None if rho is None else "supplied_density"
    elems = spec.elements()
    nz = len(elems)

    # Validate the finite action before allocating dense operators, and cache it
    # so orbit traversal cannot disagree with a second callback invocation.
    permutations: dict[tuple[int, ...], tuple[int, ...]] = {}
    for z in elems:
        destinations = tuple(right_shift(x, z) for x in range(n_group))
        if any(type(dest) is not int or not 0 <= dest < n_group for dest in destinations):
            raise ValueError("right_shift must return integer indices in range (not bools or floats)")
        if len(set(destinations)) != n_group:
            raise ValueError("right_shift must define permutations")
        permutations[z] = destinations
    identity = tuple(range(n_group))
    zero = (0,) * spec.rank
    if permutations[zero] != identity:
        raise ValueError("right_shift must represent the identity")
    for a in elems:
        for b in elems:
            composed = tuple(permutations[a][permutations[b][x]] for x in range(n_group))
            if composed != permutations[spec.add(a, b)]:
                raise ValueError("right_shift must satisfy the representation composition law")
        if a != zero and any(dest == x for x, dest in enumerate(permutations[a])):
            raise ValueError("right_shift representation must be free")

    # 1. Build translation operators from the validated permutations.
    R: dict[tuple[int, ...], np.ndarray] = {}
    for z in elems:
        mat = np.zeros((n_group, n_group), dtype=complex)
        for x, dest in enumerate(permutations[z]):
            mat[dest, x] = 1.0
        R[z] = mat

    # 2. Construct spectral projectors Pi_y
    projectors: dict[tuple[int, ...], np.ndarray] = {}
    for y in elems:
        pi = np.zeros((n_group, n_group), dtype=complex)
        for z in elems:
            chi = spec.character_value(y, z)
            pi += np.conjugate(chi) * R[z]
        pi /= nz
        projectors[y] = pi

    # 3. Construct ancilla cyclic-QFT unitary and extract Kraus operators
    # Circuit dimensions: ancilla dim nz, target dim n_group
    qft_z = product_qft_matrix(spec)
    qft_z_inv = qft_z.conj().T

    u_prep = np.kron(qft_z, np.eye(n_group, dtype=complex))
    u_ctrl = np.zeros((nz * n_group, nz * n_group), dtype=complex)
    for z_idx, z in enumerate(elems):
        u_ctrl[z_idx * n_group : (z_idx + 1) * n_group, z_idx * n_group : (z_idx + 1) * n_group] = R[z]
    u_readout = np.kron(qft_z_inv, np.eye(n_group, dtype=complex))

    circuit_unitary = u_readout @ u_ctrl @ u_prep

    kraus_operators: dict[tuple[int, ...], np.ndarray] = {}
    kraus_diffs: list[float] = []
    for y_idx, y in enumerate(elems):
        k_y = circuit_unitary[y_idx * n_group : (y_idx + 1) * n_group, 0 : n_group]
        kraus_operators[y] = k_y
        diff = float(np.max(np.abs(k_y - projectors[y])))
        kraus_diffs.append(diff)

    kraus_equiv_err = max(kraus_diffs)
    if kraus_equiv_err >= TOL:
        raise ArithmeticError(f"circuit Kraus operators do not match projectors: max err {kraus_equiv_err}")

    # 4. Verify Hermitian idempotence, pairwise orthogonality, and completeness
    herm_errs = [float(np.max(np.abs(pi - pi.conj().T))) for pi in projectors.values()]
    max_herm = max(herm_errs)
    if max_herm >= TOL:
        raise ArithmeticError(f"projector Hermiticity failed: max err {max_herm}")

    idem_errs = [float(np.max(np.abs(pi @ pi - pi))) for pi in projectors.values()]
    max_idem = max(idem_errs)
    if max_idem >= TOL:
        raise ArithmeticError(f"projector idempotence failed: max err {max_idem}")

    max_orth = 0.0
    for i, y1 in enumerate(elems):
        for y2 in elems[i + 1 :]:
            err = float(np.max(np.abs(projectors[y1] @ projectors[y2])))
            if err > max_orth:
                max_orth = err
    if max_orth >= TOL:
        raise ArithmeticError(f"projector pairwise orthogonality failed: max err {max_orth}")

    sum_pi = sum(projectors.values())
    max_comp = float(np.max(np.abs(sum_pi - np.eye(n_group))))
    if max_comp >= TOL:
        raise ArithmeticError(f"projector completeness failed: max err {max_comp}")

    # 5. Optional finite density and intersection-distribution checks.
    max_comm: Optional[float] = None
    density_commutes: Optional[bool] = None
    outcome_probs: Optional[dict[tuple[int, ...], float]] = None
    outcome_dist_err: Optional[float] = None

    if h_coords is not None or rho is not None:
        if rho is None:
            assert h_coords is not None
            unvisited = set(range(n_group))
            orbits: list[list[int]] = []
            while unvisited:
                q = min(unvisited)
                c = {permutations[h][q] for h in h_coords}
                if q not in c or not c <= unvisited or len(c) != len(h_coords):
                    raise ArithmeticError("central-subgroup orbit traversal failed to make disjoint progress")
                unvisited -= c
                orbits.append(sorted(c))

            rho = np.zeros((n_group, n_group), dtype=complex)
            for c in orbits:
                vec = np.zeros(n_group, dtype=complex)
                for idx in c:
                    vec[idx] = 1.0 / np.sqrt(len(c))
                rho += np.outer(vec, vec.conj()) / len(orbits)
            rho = _validate_density(rho, n_group)
            density_source = "constructed_central_subgroup_orbit_density"

        comm_errs = [float(np.max(np.abs(pi @ rho - rho @ pi))) for pi in projectors.values()]
        max_comm = max(comm_errs)
        if not math.isfinite(max_comm):
            raise ArithmeticError("density commutation check is nonfinite")
        density_commutes = max_comm <= TOL
        if density is None and not density_commutes:
            raise ArithmeticError(f"central-subgroup orbit density commutation failed: max err {max_comm}")

        # Preserve raw rounding residuals rather than clipping or renormalizing.
        outcome_probs = {}
        for y, pi in projectors.items():
            prob = complex(np.trace(rho @ pi))
            if (not np.isfinite(prob) or abs(prob.imag) > TOL
                    or not -TOL <= prob.real <= 1.0 + TOL):
                raise ArithmeticError("outcome probabilities must be finite and physical within TOL")
            outcome_probs[y] = prob.real
        if abs(sum(outcome_probs.values()) - 1.0) > TOL:
            raise ArithmeticError("outcome probabilities must sum to one within TOL")

        if h_coords is not None:
            expected_mass = len(h_coords) / nz

            dist_errs: list[float] = []
            for y, prob in outcome_probs.items():
                is_trivial_on_h = all(spec.phase_turn(y, h) == 0 for h in h_coords)
                expected_prob = expected_mass if is_trivial_on_h else 0.0
                dist_errs.append(abs(prob - expected_prob))

            outcome_dist_err = max(dist_errs)
            if outcome_dist_err >= TOL:
                raise ArithmeticError(
                    f"outcome distribution mismatch: max err {outcome_dist_err}"
                )

    return {
        "spec": spec,
        "n_group": n_group,
        "projectors": projectors,
        "kraus_operators": kraus_operators,
        "circuit_unitary": circuit_unitary,
        "hermitian_max_error": max_herm,
        "idempotence_max_error": max_idem,
        "orthogonality_max_error": max_orth,
        "completeness_max_error": max_comp,
        "kraus_equivalence_max_error": kraus_equiv_err,
        "central_intersection_validated": h_coords is not None,
        "central_intersection_distribution_checked": outcome_dist_err is not None,
        "density_source": density_source,
        "density_validated": rho is not None,
        "density_commutation_max_error": max_comm,
        "density_commutes_with_projectors": density_commutes,
        "outcome_probabilities": outcome_probs,
        "outcome_distribution_max_error": outcome_dist_err,
        "free_representation_verified": True,
        "ambient_centrality_certified": False,
        "hidden_subgroup_state_certified": False,
        "receiver_validity_certified": False,
        "scalable_compiler_implemented": False,
        "verification_scope": "finite_numerical_instrument_checks",
        "numerical_tolerance": TOL,
        "resources": {
            "ancilla_dimension": nz,
            "target_dimension": n_group,
            "dense_unitary_dimension": nz * n_group,
            "complex_entries_per_dense_unitary": (nz * n_group) ** 2,
            "bytes_per_dense_unitary": circuit_unitary.nbytes,
            "cached_permutation_entries": nz * n_group,
            "action_composition_index_checks": nz ** 2 * n_group,
            "dense_storage_scaling": "O((|Z| * n_group)^2)",
            "dense_multiplication_scaling": "O((|Z| * n_group)^3)",
            "synthesized_gate_count": None,
        },
        "verified": True,
    }


class CancellationResult(dict):
    """Central phase check with nonempty support, not a receiver certificate."""

    @property
    def cancels(self) -> bool:
        return bool(self.get("cancels", False))

    def __bool__(self) -> bool:
        return self.cancels


def verify_mixed_modulus_unit_scale_cancellation(
    spec: MixedModulusCenterSpec,
    degree: int,
    outcomes: Sequence[Sequence[int]],
    active: Collection[int],
    scales: Sequence[int],
    *,
    raise_on_failure: bool = False,
) -> CancellationResult:
    """Verify the central character phase identity across M register labels.

    A nonempty active set is required for ``cancels``. The empty product may
    satisfy ``phase_identity_verified`` but cannot certify off-coset receiver
    cancellation. Even nonempty support does not verify source or action promises.

    Checks:
    1. Active scales s_i in (Z / p^{max a_j} Z)^\\times for i in A, and s_i == 0 for i not in A.
    2. Modular zero-sum condition componentwise:
       sum_{i in A} s_i^degree * y_{i, j} == 0 (mod p^{a_j}) for all j in {1, ..., R}.
    3. Joint phase emitted across M target registers under controlled R_{Delta_{s_i}(z)}
       satisfies prod_{i=0}^{M-1} chi_{y_i}(Delta_{s_i}(z)) == 1 for every central shift z in Z.
    """
    if type(degree) is not int or degree < 1:
        raise ValueError(f"degree must be an integer >= 1, got {degree}")
    if len(outcomes) != len(scales):
        raise ValueError(f"mismatch: {len(outcomes)} outcomes vs {len(scales)} scales")

    m_copies = len(outcomes)
    active_indices = tuple(active)
    if any(type(i) is not int or i < 0 or i >= m_copies for i in active_indices):
        raise ValueError("active indices must be integers in bounds (not bools or floats)")
    active_set = set(active_indices)
    scope = {
        "verification_scope": "central_character_phase_identity_only",
        "receiver_validity_certified": False,
        "nonempty_active_support": bool(active_set),
    }

    canonical_outcomes = [spec.canonical(y) for y in outcomes]
    unit_modulus = spec.p ** max(spec.exponents)

    # Validate scales
    invalid_reasons: list[str] = []
    for i, s in enumerate(scales):
        if type(s) is not int:
            invalid_reasons.append(f"scale[{i}] is not int: {s}")
            continue
        if i in active_set:
            if not (0 <= s < unit_modulus) or (s % spec.p == 0):
                invalid_reasons.append(f"active scale[{i}]={s} is not a unit modulo {unit_modulus}")
        else:
            if s != 0:
                invalid_reasons.append(f"inactive scale[{i}]={s} is not zero")

    if invalid_reasons:
        if raise_on_failure:
            raise ValueError("; ".join(invalid_reasons))
        return CancellationResult({
            **scope,
            "cancels": False,
            "phase_identity_verified": False,
            "reasons": invalid_reasons,
            "zero_sum_per_component": [],
            "all_components_zero": False,
            "max_phase_turn_error": Fraction(1),
            "active_count": len(active_set),
            "total_copies": m_copies,
        })

    # Check componentwise zero-sum condition
    zero_sum_per_component: list[int] = []
    all_zero = True
    for j, m_j in enumerate(spec.moduli):
        comp_sum = sum(
            pow(scales[i], degree, m_j) * canonical_outcomes[i][j] for i in active_set
        ) % m_j
        zero_sum_per_component.append(comp_sum)
        if comp_sum != 0:
            all_zero = False

    # Check joint phase across all central elements z in Z
    max_turn_err = Fraction(0)
    for z in spec.elements():
        total_turn = Fraction(0)
        for i in range(m_copies):
            s_i = scales[i]
            delta_z = spec.scale(s_i, degree, z)
            turn = spec.phase_turn(canonical_outcomes[i], delta_z)
            total_turn = (total_turn + turn) % 1
        if total_turn > max_turn_err:
            max_turn_err = total_turn

    phase_identity = all_zero and (max_turn_err == Fraction(0))
    cancels = bool(active_set) and phase_identity

    if not cancels and raise_on_failure:
        if not active_set:
            raise ValueError("nonempty active support required for cancellation")
        raise ArithmeticError(
            f"coherence cancellation failed: zero_sum={zero_sum_per_component}, max_phase_turn={max_turn_err}"
        )

    return CancellationResult({
        **scope,
        "cancels": cancels,
        "phase_identity_verified": phase_identity,
        "reasons": [] if active_set else ["nonempty active support required for cancellation"],
        "zero_sum_per_component": zero_sum_per_component,
        "all_components_zero": all_zero,
        "max_phase_turn_error": max_turn_err,
        "active_count": len(active_set),
        "total_copies": m_copies,
    })


def _validate_stage_shape(
    rank: int, moduli: tuple[int, ...], copies: int,
    center_spec: Optional[MixedModulusCenterSpec],
) -> None:
    if type(rank) is not int or rank < 1:
        raise ValueError(f"rank must be a positive integer, got {rank}")
    if type(copies) is not int or copies < 1:
        raise ValueError(f"copy_count must be a positive integer, got {copies}")
    if len(moduli) != rank:
        raise ValueError("rank must equal the number of moduli")
    if any(type(m) is not int or m < 2 for m in moduli):
        raise ValueError("moduli must be integers >= 2")
    if center_spec is not None:
        if not isinstance(center_spec, MixedModulusCenterSpec):
            raise ValueError("center_spec must be a MixedModulusCenterSpec")
        if rank != center_spec.rank or moduli != center_spec.moduli:
            raise ValueError("rank and moduli must match center_spec")


def _validate_allowance(value: Fraction, name: str) -> None:
    if type(value) is not Fraction or not 0 <= value <= 1:
        raise ValueError(f"{name} must be an exact Fraction in [0, 1], got {value}")


@dataclass(frozen=True)
class CyclicQFTStageBudget:
    """Exact conditional budget, not verified cyclic-QFT implementation errors."""
    stage_index: int
    rank: int
    moduli: tuple[int, ...]
    copy_count: int
    qft_accuracies: tuple[Fraction, ...]
    trans_accuracy: Fraction
    abort_bound: Fraction
    center_spec: Optional[MixedModulusCenterSpec] = None

    def __post_init__(self) -> None:
        if type(self.stage_index) is not int or self.stage_index < 0:
            raise ValueError(f"stage_index must be a non-negative integer, got {self.stage_index}")
        object.__setattr__(self, "moduli", tuple(self.moduli))
        object.__setattr__(self, "qft_accuracies", tuple(self.qft_accuracies))
        _validate_stage_shape(self.rank, self.moduli, self.copy_count, self.center_spec)
        if len(self.qft_accuracies) != self.rank:
            raise ValueError(f"expected {self.rank} qft_accuracies, got {len(self.qft_accuracies)}")
        for x in self.qft_accuracies:
            _validate_allowance(x, "qft_accuracy")
        _validate_allowance(self.trans_accuracy, "trans_accuracy")
        _validate_allowance(self.abort_bound, "abort_bound")

    @property
    def per_measurement_error(self) -> Fraction:
        """Per-measurement half-diamond error: eps_meas = 2 * sum_j eta_j + eta_trans."""
        return 2 * sum(self.qft_accuracies) + self.trans_accuracy

    @property
    def stage_quantum_error(self) -> Fraction:
        """Total quantum measurement channel error for this stage: M_t * eps_meas."""
        return self.copy_count * self.per_measurement_error

    @property
    def stage_total_error(self) -> Fraction:
        """Total channel error including abort bound: M_t * eps_meas + delta_abort."""
        return self.stage_quantum_error + self.abort_bound


@dataclass(frozen=True)
class PrimePowerReceiverSchedule:
    """Self-certification covers budget arithmetic only, conditional on promises."""
    stages: tuple[CyclicQFTStageBudget, ...]
    total_copies: int
    total_target_error: Fraction
    total_stage_error: Fraction
    flagged_certificate: dict[str, object]
    self_certified: bool
    certification_scope: str = "exact_conditional_error_budget_arithmetic"
    scalable_compiler_implemented: bool = False
    physical_implementation_verified: bool = False


def allocate_cyclic_qft_error_schedule(
    stages: Sequence[Any],
    total_error_target: Fraction | int | float | str,
    *,
    joint_input_distance: Fraction = Fraction(0),
    action_calls: int = 0,
    action_half_diamond: Fraction = Fraction(0),
    control_preparation_distance: Fraction = Fraction(0),
    ideal_abort: Fraction = Fraction(0),
    strategy: str = "uniform_per_copy",
) -> PrimePowerReceiverSchedule:
    """Allocate cyclic-QFT and translation error budgets across stages.

    Compose sum_t M_t * eps_{meas,t} and stage aborts with fixed overhead,
    using exact Fraction arithmetic. All allowances must be Fractions in [0, 1].
    The complete-channel bounds remain premises, not implementation certificates.
    """
    target = Fraction(total_error_target)
    if target <= 0 or target > 1:
        raise ValueError(f"total_error_target must be in (0, 1], got {target}")

    # Validate fixed allowances and call counts before any budget arithmetic.
    fixed_cert = flagged_error_bound(
        ideal_abort=ideal_abort,
        joint_input_distance=joint_input_distance,
        measurement_calls=0,
        measurement_half_diamond=Fraction(0),
        action_calls=action_calls,
        action_half_diamond=action_half_diamond,
        control_preparation_distance=control_preparation_distance,
        classical_clock_abort=Fraction(0),
    )
    parsed_stages: list[tuple[int, tuple[int, ...], int, Fraction, Optional[MixedModulusCenterSpec]]] = []
    for idx, stage in enumerate(stages):
        if isinstance(stage, CyclicQFTStageBudget):
            parsed_stages.append((stage.rank, stage.moduli, stage.copy_count, stage.abort_bound, stage.center_spec))
        elif isinstance(stage, MixedModulusCenterSpec):
            parsed_stages.append((stage.rank, stage.moduli, 1, Fraction(0), stage))
        elif isinstance(stage, dict):
            spec = stage.get("center_spec")
            if spec is not None and not isinstance(spec, MixedModulusCenterSpec):
                raise ValueError("center_spec must be a MixedModulusCenterSpec")
            rank = stage.get("rank", spec.rank if spec else len(stage.get("moduli", ())))
            moduli = tuple(stage.get("moduli", spec.moduli if spec else ()))
            copies = stage.get("copy_count", stage.get("count", 1))
            if "count" in stage:
                if type(stage["count"]) is not int or stage["count"] != copies:
                    raise ValueError("count and copy_count must be consistent integers")
            abort = stage.get("abort_bound", Fraction(0))
            parsed_stages.append((rank, moduli, copies, abort, spec))
        elif isinstance(stage, (tuple, list)):
            if len(stage) == 2:
                s, c = stage
                a = Fraction(0)
            elif len(stage) == 3:
                s, c, a = stage
            else:
                raise ValueError(f"invalid stage tuple: {stage}")
            if isinstance(s, MixedModulusCenterSpec):
                parsed_stages.append((s.rank, s.moduli, c, a, s))
            else:
                raise ValueError(f"first element of stage tuple must be MixedModulusCenterSpec, got {type(s)}")
        else:
            raise ValueError(f"unsupported stage specification type: {type(stage)}")
        rank, moduli, copies, abort, spec = parsed_stages[-1]
        _validate_stage_shape(rank, moduli, copies, spec)
        _validate_allowance(abort, "abort_bound")

    if not parsed_stages:
        raise ValueError("stages must be non-empty")

    total_copies = sum(copies for _, _, copies, _, _ in parsed_stages)
    total_abort = sum((abort for _, _, _, abort, _ in parsed_stages), Fraction(0))
    fixed_overhead = fixed_cert["unclipped_sum"] + total_abort

    meas_budget = target - fixed_overhead
    if meas_budget <= 0:
        raise ValueError(
            f"error budget exhausted: target={target}, fixed_overhead={fixed_overhead}, remaining={meas_budget}"
        )

    # Allocate per measurement error
    # Strategy 'uniform_per_copy': each measurement across all stages gets equal budget
    stage_budgets: list[CyclicQFTStageBudget] = []
    if strategy == "uniform_per_copy":
        eps_meas_uniform = meas_budget / total_copies
        for idx, (rank, moduli, copies, abort, spec) in enumerate(parsed_stages):
            weight = 2 * rank + 1
            eta = eps_meas_uniform / weight
            qft_accs = tuple([eta] * rank)
            trans_acc = eta
            budget = CyclicQFTStageBudget(
                stage_index=idx,
                rank=rank,
                moduli=moduli,
                copy_count=copies,
                qft_accuracies=qft_accs,
                trans_accuracy=trans_acc,
                abort_bound=abort,
                center_spec=spec,
            )
            stage_budgets.append(budget)
    elif strategy == "uniform_per_stage":
        stage_share = meas_budget / len(parsed_stages)
        for idx, (rank, moduli, copies, abort, spec) in enumerate(parsed_stages):
            eps_meas_stage = stage_share / copies
            weight = 2 * rank + 1
            eta = eps_meas_stage / weight
            qft_accs = tuple([eta] * rank)
            trans_acc = eta
            budget = CyclicQFTStageBudget(
                stage_index=idx,
                rank=rank,
                moduli=moduli,
                copy_count=copies,
                qft_accuracies=qft_accs,
                trans_accuracy=trans_acc,
                abort_bound=abort,
                center_spec=spec,
            )
            stage_budgets.append(budget)
    else:
        raise ValueError(f"unknown allocation strategy: {strategy}")

    total_stage_err = sum(b.stage_total_error for b in stage_budgets)

    # Heterogeneous complete-channel hybrid: no average is asserted to bound
    # individual calls. The frozen calculator handled fixed overhead only.
    per_stage_measurement_errors = tuple(b.stage_quantum_error for b in stage_budgets)
    measurement_error = sum(per_stage_measurement_errors, Fraction(0))
    hybrid = fixed_cert["unconditional_hybrid_distance"] + measurement_error
    unclipped_sum = fixed_cert["unclipped_sum"] + total_abort + measurement_error
    cert = {
        **fixed_cert,
        "unconditional_hybrid_distance": hybrid,
        "unclipped_sum": unclipped_sum,
        "total_error_upper": min(Fraction(1), unclipped_sum),
        "measurement_composition": "sum_t copy_count_t * per_measurement_error_t",
        "measurement_calls": total_copies,
        "stage_copy_counts": tuple(b.copy_count for b in stage_budgets),
        "per_stage_per_measurement_errors": tuple(b.per_measurement_error for b in stage_budgets),
        "per_stage_measurement_errors": per_stage_measurement_errors,
        "measurement_error_sum": measurement_error,
        "classical_clock_abort": total_abort,
        "certification_scope": "exact_conditional_error_budget_arithmetic",
        "scalable_compiler_implemented": False,
        "physical_implementation_verified": False,
    }

    cert_bound = cert["total_error_upper"]
    if cert_bound > target:
        raise ArithmeticError(
            f"certified total error {cert_bound} exceeds target {target}"
        )

    return PrimePowerReceiverSchedule(
        stages=tuple(stage_budgets),
        total_copies=total_copies,
        total_target_error=target,
        total_stage_error=total_stage_err,
        flagged_certificate=cert,
        self_certified=True,
    )


def compile_prime_power_receiver_schedule(
    specs: Sequence[MixedModulusCenterSpec],
    stage_copies: Sequence[int],
    total_error_target: Fraction | int | float | str,
    *,
    abort_bounds: Optional[Sequence[Fraction]] = None,
    **kwargs: Any,
) -> PrimePowerReceiverSchedule:
    """Convenience compiler for a prime-power receiver schedule from center specs and copy counts."""
    if len(specs) != len(stage_copies):
        raise ValueError(f"mismatch: {len(specs)} specs vs {len(stage_copies)} copy counts")
    if abort_bounds is None:
        aborts = [Fraction(0)] * len(specs)
    else:
        if len(abort_bounds) != len(specs):
            raise ValueError(f"mismatch: {len(specs)} specs vs {len(abort_bounds)} abort bounds")
        aborts = list(abort_bounds)

    stage_tuples = [
        (spec, copy_count, abort)
        for spec, copy_count, abort in zip(specs, stage_copies, aborts)
    ]
    return allocate_cyclic_qft_error_schedule(stage_tuples, total_error_target, **kwargs)
