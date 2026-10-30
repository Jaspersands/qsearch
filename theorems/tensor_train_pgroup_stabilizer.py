"""Exact, scoped classical stabilizers of explicit finite-field tensor trains.

Local matrices act on column vectors, without site permutations. Two exact
rank-factor sweeps remove arbitrary redundant TT bonds, with no inner product.
For each minimal prefix image B, the solver keeps the ORIGINAL faithful local
blocks alongside the compressed action and certifies the common associative
algebra J of all (g - I). Only J**nu = 0 with nu <= p enables log/Lie/exp
recovery. The linear condition is N A B = 0, where N annihilates B on the left.
Under this guard, Lazard correspondence identifies its kernel with the exact
subspace stabilizer. The final image is a line; a p-group over F_p acts
trivially on a preserved line, so this is the vector, not just ray, stabilizer.

This does not implement the general p-group algorithm using Luks. It does not
expand the full tensor, enumerate a group or orbit, receive a hidden subgroup,
or claim a quantum algorithm, hardness result, or general tensor-network
dequantization. All matrices here are over F_p, not complex quantum MPS data.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from theorems.moore_common_algebra_stabilizer_backend import (
    _rref_row_basis,
    close_matrix_lie_span,
    compute_common_nonunital_algebra,
    truncated_matrix_exp,
    truncated_matrix_log,
)
from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import (
    _fmpz_nullspace_basis,
    _fmpz_solve_coordinates,
)
from theorems.ut5_matrix_phase_alignment import (
    _identity,
    _lists,
    _matrix,
    _product,
    _rank,
)

Matrix = tuple[tuple[int, ...], ...]
Core = tuple[tuple[tuple[int, ...], ...], ...]
Generator = tuple[Matrix, ...]


def _sequence(value: Any, name: str, *, nonempty: bool = True) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{name} must be an explicit sequence")
    if nonempty and not value:
        raise ValueError(f"{name} must be nonempty")


def _residues(row: Any, width: int, p: int, name: str) -> tuple[int, ...]:
    _sequence(row, name)
    if len(row) != width or any(type(x) is not int or not 0 <= x < p for x in row):
        raise ValueError(f"{name} requires matching shape and canonical integer residues")
    return tuple(row)


def _validate(
    prime: int, cores: Sequence[Core], generators: Sequence[Generator]
) -> tuple[tuple[Core, ...], tuple[Generator, ...], tuple[int, ...]]:
    if type(prime) is not int or prime < 3 or prime % 2 == 0:
        raise ValueError("odd prime required")
    ring(prime)
    _sequence(cores, "cores")
    clean_cores = []
    physical = []
    previous_bond = 1
    for i, core in enumerate(cores):
        _sequence(core, f"core {i}")
        if len(core) != previous_bond:
            raise ValueError(f"core {i} has incompatible left bond (boundary must be 1)")
        _sequence(core[0], f"core {i} physical axis")
        d = len(core[0])
        _sequence(core[0][0], f"core {i} right bond")
        bond = len(core[0][0])
        blocks = []
        for block in core:
            _sequence(block, f"core {i} physical axis")
            if len(block) != d:
                raise ValueError(f"core {i} has ragged physical axis")
            blocks.append(tuple(_residues(row, bond, prime, f"core {i}") for row in block))
        clean_cores.append(tuple(blocks))
        physical.append(d)
        previous_bond = bond
    if previous_bond != 1:
        raise ValueError("last TT boundary must be 1")

    _sequence(generators, "generators", nonempty=False)
    clean_generators = []
    for generator in generators:
        _sequence(generator, "generator")
        if len(generator) != len(physical):
            raise ValueError("one local matrix per site required")
        local_matrices = []
        for d, local in zip(physical, generator):
            _sequence(local, "local matrix")
            if len(local) != d:
                raise ValueError("local matrix must be square with the physical dimension")
            matrix = tuple(_residues(row, d, prime, "local matrix") for row in local)
            if _rank(matrix, prime) != d:
                raise ValueError("invertible local matrix required")
            local_matrices.append(matrix)
        clean_generators.append(tuple(local_matrices))
    return tuple(clean_cores), tuple(clean_generators), tuple(physical)


def _transpose(rows: Sequence[Sequence[int]]) -> Matrix:
    return tuple(tuple(column) for column in zip(*rows))


def _coordinates(basis: Matrix, target: Sequence[int], p: int) -> tuple[int, ...]:
    coordinates = _fmpz_solve_coordinates(basis, target, p)
    if coordinates is None:
        raise RuntimeError("exact rank factorization lost a vector in its span")
    return coordinates


def _embedding(core: Core) -> Matrix:
    return tuple(row for block in core for row in block)


def _core_from_embedding(rows: Sequence[Sequence[int]], left: int, d: int) -> Core:
    return tuple(tuple(tuple(rows[a * d + s]) for s in range(d)) for a in range(left))


def _minimalize(
    cores: tuple[Core, ...], physical: tuple[int, ...], p: int
) -> tuple[tuple[Core, ...], tuple[int, ...], bool]:
    work = list(cores)

    def zero_result() -> tuple[tuple[Core, ...], tuple[int, ...], bool]:
        # Boundary-one representation of zero; its prefix image ranks are zero.
        return tuple((tuple((0,) for _ in range(d)),) for d in physical), (0,) * len(work), True

    for i in range(len(work) - 1, 0, -1):
        core = work[i]
        d, right = physical[i], len(core[0][0])
        rows = tuple(tuple(x for row in block for x in row) for block in core)
        basis = _rref_row_basis(rows, d * right, p)
        if not basis:
            return zero_result()
        coefficients = tuple(_coordinates(basis, row, p) for row in rows)
        work[i] = tuple(
            tuple(tuple(row[s * right:(s + 1) * right]) for s in range(d)) for row in basis
        )
        previous = work[i - 1]
        absorbed = _product(_embedding(previous), coefficients, p)
        work[i - 1] = _core_from_embedding(absorbed, len(previous), physical[i - 1])

    for i in range(len(work) - 1):
        core = work[i]
        rows = _embedding(core)
        reduced = _rref_row_basis(rows, len(rows[0]), p)
        if not reduced:
            return zero_result()
        pivots = tuple(next(j for j, x in enumerate(row) if x) for row in reduced)
        columns = _transpose(rows)
        basis_columns = tuple(columns[j] for j in pivots)
        coefficients = _transpose(tuple(_coordinates(basis_columns, col, p) for col in columns))
        work[i] = _core_from_embedding(_transpose(basis_columns), len(core), physical[i])
        following = work[i + 1]
        next_rows = tuple(tuple(x for row in block for x in row) for block in following)
        absorbed = _product(coefficients, next_rows, p)
        right, d = len(following[0][0]), physical[i + 1]
        work[i + 1] = tuple(
            tuple(tuple(row[s * right:(s + 1) * right]) for s in range(d)) for row in absorbed
        )
    if not any(x for block in work[-1] for row in block for x in row):
        return zero_result()
    ranks = tuple(len(core[0][0]) for core in work)
    for core, rank in zip(work, ranks):
        if _rank(_embedding(core), p) != rank:
            raise RuntimeError("minimal prefix embedding is not injective")
    return tuple(work), ranks, False


def _block_diagonal(blocks: Sequence[Matrix]) -> Matrix:
    size = sum(len(block) for block in blocks)
    rows = [[0] * size for _ in range(size)]
    offset = 0
    for block in blocks:
        for i, row in enumerate(block):
            rows[offset + i][offset:offset + len(block)] = row
        offset += len(block)
    return tuple(tuple(row) for row in rows)


def _kronecker(left: Matrix, right: Matrix, p: int) -> Matrix:
    return tuple(
        tuple(a * b % p for a in left_row for b in right_row)
        for left_row in left for right_row in right
    )


def _restricted_action(action: Matrix, embedding: Matrix, p: int) -> Matrix:
    image_columns = _transpose(_product(action, embedding, p))
    basis_columns = _transpose(embedding)
    coordinate_columns = []
    for column in image_columns:
        coordinates = _fmpz_solve_coordinates(basis_columns, column, p)
        if coordinates is None:
            raise RuntimeError("generator does not preserve a required prefix image")
        coordinate_columns.append(coordinates)
    result = _transpose(coordinate_columns)
    if _rank(result, p) != len(result):
        raise RuntimeError("induced prefix action is not invertible")
    return result


def _prefix_action(generator: Generator, embeddings: tuple[Matrix, ...], stop: int, p: int) -> Matrix:
    action = ((1,),)
    for j in range(stop):
        action = _restricted_action(_kronecker(action, generator[j], p), embeddings[j], p)
    return action


def _guard(p: int, dimension: int, generators: tuple[Matrix, ...]) -> dict[str, Any]:
    if not generators:
        return {
            "guard_status": "TRIVIAL_GROUP", "guard_passed": True,
            "common_algebra_dimension": 0, "common_nilpotency_index": 1,
            "all_generators_order_dividing_p": True, "generators_commute": True,
        }
    guard = compute_common_nonunital_algebra(
        p, dimension, generators, max_nilpotency_index=dimension
    )
    return {
        "guard_status": guard.status, "guard_passed": guard.guard_passed,
        "common_algebra_dimension": guard.algebra_dimension,
        "common_nilpotency_index": guard.nilpotency_index,
        "all_generators_order_dividing_p": guard.all_generators_order_dividing_p,
        "generators_commute": guard.generators_commute,
    }


def _project_original(matrix: Matrix, physical: tuple[int, ...]) -> Generator:
    blocks = []
    offset = 0
    for d in physical:
        blocks.append(tuple(tuple(row[offset:offset + d]) for row in matrix[offset:offset + d]))
        offset += d
    return tuple(blocks)


def _stabilizer_lie_basis(
    lie_basis: tuple[Matrix, ...], embedding: Matrix, faithful_dimension: int, p: int
) -> tuple[tuple[Matrix, ...], int]:
    dimension = len(lie_basis)
    if not dimension:
        return (), 0
    annihilator = _fmpz_nullspace_basis(_transpose(embedding), len(embedding), p)
    if not annihilator:
        return lie_basis, 0
    n_mat, b_mat = _matrix(annihilator, p), _matrix(embedding, p)
    constraint_columns = []
    for element in lie_basis:
        compressed = tuple(tuple(row[faithful_dimension:]) for row in element[faithful_dimension:])
        image = n_mat * _matrix(compressed, p) * b_mat
        constraint_columns.append(tuple(x for row in _lists(image) for x in row))
    constraint_rows = _transpose(constraint_columns)
    coordinates = _rref_row_basis(_fmpz_nullspace_basis(constraint_rows, dimension, p), dimension, p)
    matrices = [_matrix(element, p) for element in lie_basis]
    zero = matrices[0] - matrices[0]
    kernel = []
    for coordinate in coordinates:
        element = zero
        for coefficient, matrix in zip(coordinate, matrices):
            if coefficient:
                element = element + coefficient * matrix
        kernel.append(tuple(tuple(row) for row in _lists(element)))
    return tuple(kernel), dimension - len(kernel)


def recover_tensor_train_stabilizer(
    prime: int, cores: Sequence[Core], generators: Sequence[Generator]
) -> dict[str, Any]:
    """Recover Stab_<generators>(TT) under a certified common-J guard per stage.

    Cores have shape [left bond][physical][right bond], with boundary bonds 1.
    Inputs must be explicit sequences with canonical built-in integer residues;
    malformed shapes, non-primes, and singular local actions raise ValueError.
    Generators are tuples of one local square matrix per site, acting on columns.

    EXACT_STABILIZER returns generators in the ORIGINAL site spaces. An empty
    tuple generates the identity group. Any unsupported result instead returns
    generators=None and exact_subgroup_claim=False, never a partial subgroup.
    A nonnilpotent faithful common algebra returns UNSUPPORTED_NON_P_GROUP;
    a nilpotency index exceeding p returns UNSUPPORTED_COMMON_INDEX. Even the
    zero-tensor branch checks the faithful common-J guard before returning all
    input generators. Zero has a canonical boundary-one, all-zero TT and zero
    prefix ranks; nonzero minimized cores have injective prefix embeddings.

    Storage is polynomial in the explicit TT and local-action sizes, including
    dense augmented matrices of dimension sum(d_j) + r_(i-1) * d_i, not prod(d_j).
    There is no general-Luks fallback and no full-orbit-span computation.
    """
    clean_cores, current, physical = _validate(prime, cores, generators)
    minimized, ranks, is_zero = _minimalize(clean_cores, physical, prime)
    faithful_dimension = sum(physical)
    certificates: list[dict[str, Any]] = []
    result: dict[str, Any] = {
        "prime": prime, "physical_dimensions": physical,
        "site_count": len(physical), "faithful_dimension": faithful_dimension,
        "zero_tensor": is_zero, "minimized_cores": minimized, "prefix_ranks": ranks,
        "stage_certificates": certificates, "generators": None,
        "exact_subgroup_claim": False, "final_compressed_action_verified": False,
        "full_tensor_materialized": False, "ambient_group_enumerated": False,
        "full_orbit_span_computed": False, "general_luks_implemented": False,
        "quantum_algorithm_claim": False, "hardness_claim": False,
        "scope": "finite-field sitewise TT; certified common J^nu=0 with nu<=p",
    }

    def unsupported(certificate: dict[str, Any]) -> dict[str, Any]:
        if certificate["common_nilpotency_index"] is None:
            result["status"] = "UNSUPPORTED_NON_P_GROUP"
        else:
            result["status"] = "UNSUPPORTED_COMMON_INDEX"
        result["failed_stage"] = certificate["stage"]
        return result

    if is_zero:
        certificate = {
            "stage": 0, "kind": "zero_tensor_faithful_guard",
            "prefix_rank": 0, "compressed_dimension": 0,
            "augmented_dimension": faithful_dimension,
            "input_generator_count": len(current),
            **_guard(prime, faithful_dimension, tuple(_block_diagonal(g) for g in current)),
        }
        certificates.append(certificate)
        if not certificate["guard_passed"]:
            return unsupported(certificate)
        certificate["output_generator_count"] = len(current)
        result.update(status="EXACT_STABILIZER", generators=current, exact_subgroup_claim=True)
        result["zero_tensor_all_input_generators_returned"] = True
        return result

    embeddings = tuple(_embedding(core) for core in minimized)
    for i, embedding in enumerate(embeddings):
        augmented = tuple(
            _block_diagonal((*g, _kronecker(_prefix_action(g, embeddings, i, prime), g[i], prime)))
            for g in current
        )
        dimension = faithful_dimension + len(embedding)
        certificate = {
            "stage": i + 1, "kind": "prefix_image_stabilizer",
            "prefix_rank": ranks[i], "compressed_dimension": len(embedding),
            "augmented_dimension": dimension, "input_generator_count": len(current),
            "ambient_lie_dimension": None, "stabilizer_lie_dimension": None,
            "stage_preservation_verified": False,
            **_guard(prime, dimension, augmented),
        }
        certificates.append(certificate)
        if not certificate["guard_passed"]:
            return unsupported(certificate)
        nu = certificate["common_nilpotency_index"]
        lie_basis = close_matrix_lie_span(
            tuple(truncated_matrix_log(g, prime, nu) for g in augmented), prime, dimension
        ) if augmented else ()
        kernel, constraint_rank = _stabilizer_lie_basis(lie_basis, embedding, faithful_dimension, prime)
        next_generators = []
        for element in kernel:
            exponential = truncated_matrix_exp(element, prime, nu)
            generator = _project_original(exponential, physical)
            # Verify the faithful projection still reconstructs this augmented action.
            compressed = _kronecker(_prefix_action(generator, embeddings, i, prime), generator[i], prime)
            if _block_diagonal((*generator, compressed)) != exponential:
                raise RuntimeError("exponentiation failed augmented-action consistency")
            restricted = _restricted_action(compressed, embedding, prime)
            if i == len(embeddings) - 1 and restricted != ((1,),):
                raise RuntimeError("final preserved line does not have scalar-one action")
            next_generators.append(generator)
        current = tuple(next_generators)
        certificate.update(
            ambient_lie_dimension=len(lie_basis), stabilizer_lie_dimension=len(kernel),
            linear_constraint_rank=constraint_rank, output_generator_count=len(current),
            stage_preservation_verified=True, faithful_projection_verified=True,
        )

    final_scalars = []
    for generator in current:
        action = _prefix_action(generator, embeddings, len(embeddings), prime)
        if action != ((1,),):
            raise RuntimeError("returned generator fails final compressed scalar-one check")
        final_scalars.append(action[0][0])
    result.update(
        status="EXACT_STABILIZER", generators=current, exact_subgroup_claim=True,
        final_compressed_action_verified=True, final_compressed_scalars=tuple(final_scalars),
    )
    return result


def build_tensor_train_pgroup_stabilizer_report() -> dict[str, Any]:
    """Run small reproducible compressed controls, not a full mathematical audit."""
    def identity(d: int) -> Matrix:
        return tuple(tuple(row) for row in _identity(d))

    def shear(d: int, i: int, j: int) -> Matrix:
        rows = _identity(d)
        rows[i][j] = 1
        return tuple(tuple(row) for row in rows)

    def compact(result: dict[str, Any]) -> dict[str, Any]:
        return {
            key: value for key, value in result.items()
            if key not in ("generators", "minimized_cores", "final_compressed_scalars")
        } | {"returned_generator_count": None if result["generators"] is None else len(result["generators"])}

    p, n, d = 5, 3, 4
    cores = tuple((tuple((int(s == d - 1),) for s in range(d)),) for _ in range(n))
    generators = tuple(
        tuple(shear(d, j, j + 1) if site == i else identity(d) for site in range(n))
        for i in range(n) for j in range(d - 1)
    )
    ut4 = compact(recover_tensor_train_stabilizer(p, cores, generators))
    ut4.update(
        full_orbit_dimension_analytic=d ** n,
        full_orbit_dimension_source="analytic: independent local UT4 last-column orbits span F_p^4",
        expected_stabilizer="product of upper-left UT3 factors; generally nonnormal",
        expected_stabilizer_log_p_order_analytic=3 * n,
        input_tt_entry_count=d * n,
    )
    isotropic = compact(recover_tensor_train_stabilizer(
        5, ((((1,), (2,)),),), ((shear(2, 0, 1),),)
    ))
    jordan = ((1, 1, 0), (0, 1, 1), (0, 0, 1))
    identity_tt = ((identity(3),), tuple(tuple((x,) for x in row) for row in identity(3)))
    failure = compact(recover_tensor_train_stabilizer(
        3, identity_tt, ((jordan, identity(3)), (identity(3), jordan))
    ))
    root = Path(__file__).resolve().parents[1]
    sources = (
        "theorems/tensor_train_pgroup_stabilizer.py",
        "tests/test_tensor_train_pgroup_stabilizer.py",
        "theorems/moore_common_algebra_stabilizer_backend.py",
        "theorems/hpgp_coset_interface.py",
        "theorems/symbolic_scalar_phase_erasure.py",
        "theorems/ut5_matrix_phase_alignment.py",
        "theorems/prime_character_opi.py",
    )
    return {
        "schema_version": 1,
        "scope": "constructive finite-field TT baseline under stagewise common-J guard only",
        "independent_mathematical_review": {
            "kind": "automated adversarial review, not human peer review or formal verification",
            "general_reduction_reviewer": "Lorentz",
            "guarded_algorithm_and_code_reviewer": "McClintock",
            "outcome": "no remaining correctness objection in reviewed scope; provenance test repaired",
            "scope_note": "research/TENSOR_TRAIN_CLASSICAL_FILTER.md",
        },
        "general_luks_implemented": False,
        "all_tensor_networks_dequantized_claim": False,
        "quantum_algorithm_claim": False, "hardness_claim": False,
        "full_tensor_materialized": False, "ambient_group_enumerated": False,
        "source_hashes_sha256": {name: sha256((root / name).read_bytes()).hexdigest() for name in sources},
        "source_hash_scope": "solver, tests, and direct helper modules; parent research note excluded",
        "controls": {"ut4_product_f5_n3": ut4, "isotropic_nonzero_f5": isotropic,
                     "common_index_failure_f3": failure},
    }


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write a deterministic JSON report (default: stdout)")
    args = parser.parse_args(argv)
    report = json.dumps(build_tensor_train_pgroup_stabilizer_report(), indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(report, end="")
    else:
        args.output.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
