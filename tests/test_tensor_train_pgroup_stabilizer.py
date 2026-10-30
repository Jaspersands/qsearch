"""Independent tiny dense/group controls for the guarded TT solver.

Dense tensors and finite-group enumeration are intentionally TEST-ONLY.
"""

from __future__ import annotations

import copy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random

import pytest

from theorems import tensor_train_pgroup_stabilizer as solver


def eye(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def multiply(a, b, p):
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) % p for col in zip(*b)) for row in a)


def shear(d, i, j, value=1):
    matrix = [list(row) for row in eye(d)]
    matrix[i][j] = value
    return tuple(tuple(row) for row in matrix)


def matrix_rank(rows, p):
    work = [list(row) for row in rows]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(rank, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, p)
        work[rank] = [x * inverse % p for x in work[rank]]
        for i in range(len(work)):
            if i != rank:
                factor = work[i][column]
                work[i] = [(x - factor * y) % p for x, y in zip(work[i], work[rank])]
        rank += 1
    return rank


def tensor_product_vectors(vectors):
    return tuple((tuple((x,) for x in vector),) for vector in vectors)


def matrix_tt(matrix):
    d = len(matrix)
    return (
        (eye(d),),
        tuple(tuple((x,) for x in row) for row in matrix),
    )


def dense(cores, p):
    dimensions = [len(core[0]) for core in cores]
    tensor = {}
    for labels in product(*(range(d) for d in dimensions)):
        state = (1,)
        for core, label in zip(cores, labels):
            state = tuple(sum(state[a] * core[a][label][b] for a in range(len(state))) % p
                          for b in range(len(core[0][0])))
        tensor[labels] = state[0]
    return tensor


def dense_action(generator, tensor, p):
    output = {}
    for target in tensor:
        total = 0
        for source, coefficient in tensor.items():
            term = coefficient
            for g, i, j in zip(generator, target, source):
                term = term * g[i][j] % p
            total += term
        output[target] = total % p
    return output


def finite_group(generators, dimensions, p, cap=5000):
    identity = tuple(eye(d) for d in dimensions)
    seen, pending = {identity}, [identity]
    for element in pending:
        for generator in generators:
            value = tuple(multiply(a, b, p) for a, b in zip(element, generator))
            if value not in seen:
                seen.add(value)
                pending.append(value)
                assert len(seen) <= cap, "test group unexpectedly exceeded its small cap"
    return seen


def check_exact(p, cores, generators):
    result = solver.recover_tensor_train_stabilizer(p, cores, generators)
    assert result["status"] == "EXACT_STABILIZER"
    assert result["exact_subgroup_claim"] is True
    dimensions = result["physical_dimensions"]
    tensor = dense(cores, p)
    assert dense(result["minimized_cores"], p) == tensor
    group = finite_group(generators, dimensions, p)
    expected = {g for g in group if dense_action(g, tensor, p) == tensor}
    recovered = finite_group(result["generators"], dimensions, p)
    assert recovered == expected
    if not result["zero_tensor"]:
        assert result["final_compressed_action_verified"] is True
        assert result["final_compressed_scalars"] == (1,) * len(result["generators"])
        for i, rank in enumerate(result["prefix_ranks"], start=1):
            left = tuple(product(*(range(d) for d in dimensions[:i])))
            right = tuple(product(*(range(d) for d in dimensions[i:])))
            unfolding = [[tensor[a + b] for b in right] for a in left]
            assert matrix_rank(unfolding, p) == rank
            if i < len(dimensions):
                suffix_rows = []
                for a in range(rank):
                    row = []
                    for labels in right:
                        state = tuple(int(j == a) for j in range(rank))
                        for core, label in zip(result["minimized_cores"][i:], labels):
                            state = tuple(sum(state[j] * core[j][label][b] for j in range(len(state))) % p
                                          for b in range(len(core[0][0])))
                        row.append(state[0])
                    suffix_rows.append(row)
                assert matrix_rank(suffix_rows, p) == rank
        assert all(c["stage_preservation_verified"] for c in result["stage_certificates"])
    assert result["full_tensor_materialized"] is False
    assert result["ambient_group_enumerated"] is False
    assert result["general_luks_implemented"] is False
    assert result["quantum_algorithm_claim"] is False
    assert result["hardness_claim"] is False
    return result, recovered


@pytest.mark.parametrize("p", [5, 7, 11])
def test_single_site_noncommuting_ut3_exact_subgroup(p):
    cores = tensor_product_vectors([(0, 0, 3)])
    generators = ((shear(3, 0, 1),), (shear(3, 1, 2),))
    result, recovered = check_exact(p, cores, generators)
    assert len(recovered) == p
    certificate = result["stage_certificates"][0]
    assert certificate["common_nilpotency_index"] == 3
    assert certificate["ambient_lie_dimension"] == 3
    assert certificate["stabilizer_lie_dimension"] == 1
    assert certificate["generators_commute"] is False


@pytest.mark.parametrize("p", [5, 7])
def test_diagonal_noncommuting_ut3_site_action(p):
    x, y = shear(3, 0, 1), shear(3, 1, 2)
    cores = matrix_tt(((0, 0, 1), (0, 1, 0), (1, 0, 0)))
    result, _ = check_exact(p, cores, ((x, x), (y, y)))
    assert result["prefix_ranks"] == (3, 1)
    assert result["stage_certificates"][-1]["common_nilpotency_index"] == 5


def test_correlated_dual_site_actions_preserve_identity_tensor():
    p = 5
    x, y = shear(3, 0, 1), shear(3, 1, 2)
    dual_x, dual_y = shear(3, 1, 0, p - 1), shear(3, 2, 1, p - 1)
    result, recovered = check_exact(p, matrix_tt(eye(3)), ((x, dual_x), (y, dual_y)))
    assert len(recovered) == p ** 3
    assert result["stage_certificates"][-1]["stabilizer_lie_dimension"] == 3


@pytest.mark.parametrize("p", [5, 7, 11])
def test_conjugated_correlated_actions_in_nonspecial_local_bases(p):
    permutation = ((0, 1, 0), (0, 0, 1), (1, 0, 0))
    inverse_permutation = tuple(zip(*permutation))
    change = multiply(shear(3, 2, 0, 2), permutation, p)
    inverse_change = multiply(inverse_permutation, shear(3, 2, 0, p - 2), p)
    other = multiply(permutation, shear(3, 1, 0, 3), p)
    inverse_other = multiply(shear(3, 1, 0, p - 3), inverse_permutation, p)
    assert multiply(change, inverse_change, p) == eye(3)
    assert multiply(other, inverse_other, p) == eye(3)
    generators = tuple(
        (multiply(multiply(change, shear(3, i, i + 1), p), inverse_change, p),
         multiply(multiply(other, shear(3, i + 1, i, p - 1), p), inverse_other, p))
        for i in range(2)
    )
    tensor_matrix = multiply(change, tuple(zip(*other)), p)
    result, recovered = check_exact(p, matrix_tt(tensor_matrix), generators)
    assert len(recovered) == p ** 3
    assert result["prefix_ranks"] == (3, 1)


def inflate_bond(cores, site, p, rng):
    work = copy.deepcopy(cores)
    left, right = work[site], work[site + 1]
    bond = len(left[0][0])
    t = [[rng.randrange(p) for _ in range(2)] for _ in range(bond)]
    u = [[rng.randrange(p) for _ in range(bond)] for _ in range(2)]
    tu = multiply(t, u, p)
    expand = tuple(tuple(eye(bond)[i]) + tuple(t[i]) for i in range(bond))
    contract = tuple(tuple((int(i == j) - tu[i][j]) % p for j in range(bond))
                     for i in range(bond)) + tuple(tuple(row) for row in u)
    assert multiply(expand, contract, p) == eye(bond)
    work[site] = [[list(row) for row in multiply(block, expand, p)] for block in left]
    work[site + 1] = [[[sum(contract[a][b] * right[b][s][c] for b in range(bond)) % p
                       for c in range(len(right[0][0]))] for s in range(len(right[0]))]
                     for a in range(bond + 2)]
    return work


@pytest.mark.parametrize("seed", range(5))
def test_nonminimal_two_sweeps_preserve_values_and_exact_stabilizer(seed):
    p, rng = 5, random.Random(seed)
    bonds, dimensions = (1, 2, 3, 1), (2, 3, 2)
    cores = [[[[rng.randrange(p) for _ in range(bonds[i + 1])]
               for _ in range(d)] for _ in range(bonds[i])] for i, d in enumerate(dimensions)]
    expanded = inflate_bond(inflate_bond(cores, 0, p, rng), 1, p, rng)
    assert dense(expanded, p) == dense(cores, p)
    original = copy.deepcopy(expanded)
    x, y = shear(3, 0, 1), shear(3, 1, 2)
    result, _ = check_exact(p, expanded, ((eye(2), x, eye(2)), (eye(2), y, eye(2))))
    assert expanded == original
    assert all(1 <= rank <= 2 for rank in result["prefix_ranks"][:-1])
    assert result["prefix_ranks"][-1] == 1
    assert max(len(core[0][0]) for core in result["minimized_cores"]) == 2


def test_nonminimal_cancellation_to_zero_returns_all_generators():
    p = 5
    cores = ((((1, 1), (2, 2)),), (((1,), (3,)), ((4,), (2,))))
    assert all(x == 0 for x in dense(cores, p).values())
    generators = ((shear(2, 0, 1), eye(2)), (eye(2), shear(2, 0, 1)))
    result, recovered = check_exact(p, cores, generators)
    assert len(recovered) == p ** 2
    assert result["generators"] == generators
    assert result["zero_tensor"] is True
    assert result["prefix_ranks"] == (0, 0)


@pytest.mark.parametrize("cores", [
    ((((0,), (0,)),),),
    ((((1, 0), (2, 0)),), (((0,), (0,)), ((0,), (0,)))),
    ((((0, 0), (0, 0)),), (((1,), (0,)), ((0,), (1,)))),
])
def test_zero_at_single_site_or_either_sweep(cores):
    dimensions = [len(core[0]) for core in cores]
    result, _ = check_exact(5, cores, (tuple(shear(d, 0, 1) for d in dimensions),))
    assert result["zero_tensor"] is True
    assert result["zero_tensor_all_input_generators_returned"] is True


def test_isotropic_nonzero_vector_does_not_collapse():
    assert (1 ** 2 + 2 ** 2) % 5 == 0
    result, recovered = check_exact(5, tensor_product_vectors([(1, 2), (1, 2)]),
                                    ((shear(2, 0, 1), eye(2)), (eye(2), shear(2, 0, 1))))
    assert result["zero_tensor"] is False
    assert result["prefix_ranks"] == (1, 1)
    assert len(recovered) == 1


def test_prefix_action_kernel_survives_faithful_augmentation():
    cores = tensor_product_vectors([(1, 0), (0, 0, 1)])
    generators = ((shear(2, 0, 1), eye(3)),
                  (eye(2), shear(3, 0, 1)), (eye(2), shear(3, 1, 2)))
    result, recovered = check_exact(5, cores, generators)
    assert len(recovered) == 25
    assert generators[0] in recovered
    assert generators[1] in recovered
    assert result["stage_certificates"][0]["ambient_lie_dimension"] == 4
    assert result["stage_certificates"][-1]["stabilizer_lie_dimension"] == 2


def test_trivial_group_and_group_becoming_empty_skip_existing_empty_guard(monkeypatch):
    real_guard = solver.compute_common_nonunital_algebra
    calls = []

    def guarded(p, d, generators, *, max_nilpotency_index):
        assert generators
        assert max_nilpotency_index == d
        calls.append(d)
        return real_guard(p, d, generators, max_nilpotency_index=max_nilpotency_index)

    monkeypatch.setattr(solver, "compute_common_nonunital_algebra", guarded)
    cores = tensor_product_vectors([(0, 1)] * 3)
    result, recovered = check_exact(5, cores, ())
    assert len(recovered) == 1
    assert not calls
    assert all(c["guard_status"] == "TRIVIAL_GROUP" for c in result["stage_certificates"])
    result, _ = check_exact(5, cores, ((shear(2, 0, 1), eye(2), eye(2)),))
    assert len(calls) == 1
    assert result["generators"] == ()
    assert result["stage_certificates"][-1]["guard_status"] == "TRIVIAL_GROUP"
    check_exact(5, tensor_product_vectors([(0, 0)]), ())
    assert len(calls) == 1


def test_identity_generators_have_zero_lie_dimension():
    result, recovered = check_exact(5, tensor_product_vectors([(2, 3), (4,)]), ((eye(2), eye(1)),))
    assert len(recovered) == 1
    assert result["generators"] == ()
    assert result["stage_certificates"][0]["common_nilpotency_index"] == 1
    assert result["stage_certificates"][0]["ambient_lie_dimension"] == 0


@pytest.mark.parametrize("zero", [False, True])
@pytest.mark.parametrize("generators", [
    ((((2, 0), (0, 1)),),),
    ((shear(2, 0, 1),), (shear(2, 1, 0),)),
])
def test_non_p_group_fails_closed_even_when_individual_generators_are_unipotent(zero, generators):
    cores = tensor_product_vectors([(0, 0) if zero else (1, 0)])
    result = solver.recover_tensor_train_stabilizer(5, cores, generators)
    assert result["status"] == "UNSUPPORTED_NON_P_GROUP"
    assert result["generators"] is None
    assert result["exact_subgroup_claim"] is False
    assert result["stage_certificates"][-1]["common_nilpotency_index"] is None


def test_augmented_common_index_failure_after_a_successful_stage_never_promotes():
    p = 3
    cores = matrix_tt(eye(3))
    jordan = ((1, 1, 0), (0, 1, 1), (0, 0, 1))
    generators = ((jordan, eye(3)), (eye(3), jordan))
    result = solver.recover_tensor_train_stabilizer(p, cores, generators)
    assert result["status"] == "UNSUPPORTED_COMMON_INDEX"
    assert result["generators"] is None
    assert result["exact_subgroup_claim"] is False
    assert result["failed_stage"] == 2
    first, second = result["stage_certificates"]
    assert first["common_nilpotency_index"] == 3
    assert first["stage_preservation_verified"] is True
    assert second["common_nilpotency_index"] == 5
    assert second["all_generators_order_dividing_p"] is True
    assert second["generators_commute"] is True
    assert second["ambient_lie_dimension"] is None
    assert second["stage_preservation_verified"] is False


@pytest.mark.parametrize("zero", [False, True])
def test_index_greater_than_p_is_not_misreported_as_non_p_group(zero):
    jordan = tuple(tuple(int(i == j) + int(j == i + 1) for j in range(4)) for i in range(4))
    cores = tensor_product_vectors([(0, 0, 0, 0) if zero else (1, 0, 0, 0)])
    result = solver.recover_tensor_train_stabilizer(3, cores, ((jordan,),))
    assert result["status"] == "UNSUPPORTED_COMMON_INDEX"
    assert result["generators"] is None
    assert result["exact_subgroup_claim"] is False
    assert result["stage_certificates"][-1]["common_nilpotency_index"] == 4


@pytest.mark.parametrize("prime", [True, 2, 4, 9, 15, 5.0, "5", -5])
def test_invalid_prime(prime):
    with pytest.raises(ValueError):
        solver.recover_tensor_train_stabilizer(prime, tensor_product_vectors([(1, 0)]), ())


@pytest.mark.parametrize("cores", [
    None, (), "bad", ((),), (((),),), ((((),),),),
    ((((1,),), ((1,),)),),
    ((((1, 0),),),),
    ((((1,), (1, 2)),),),
    ((((1,),), ((1,), (2,))),),
    ((((1, 2), (3, 4)),), (((1,), (2,)),)),
    ((((True,),),),), ((((1.0,),),),), ((((5,),),),), ((((-1,),),),),
])
def test_malformed_cores(cores):
    with pytest.raises(ValueError):
        solver.recover_tensor_train_stabilizer(5, cores, ())


@pytest.mark.parametrize("generators", [
    None, "bad", ((),), ((eye(1),),), ((eye(2), eye(2)),),
    ((((1, 0), (0, 0)),),), ((((1, 0), (0,)),),),
    ((((1, 0), (0, True)),),), ((((1, 0), (0, 5)),),),
    ((((1, 0), (0, -1)),),), ((((1, 0), (0, 1.0)),),),
])
def test_malformed_generators(generators):
    with pytest.raises(ValueError):
        solver.recover_tensor_train_stabilizer(5, tensor_product_vectors([(1, 0)]), generators)


def sitewise_shears(n, d):
    return tuple(tuple(shear(d, j, j + 1) if site == i else eye(d) for site in range(n))
                 for i in range(n) for j in range(d - 1))


@pytest.mark.parametrize("n", [3, 4])
def test_ut4_product_has_index_four_and_product_ut3_stabilizer(n):
    p = 5
    result = solver.recover_tensor_train_stabilizer(
        p, tensor_product_vectors([(0, 0, 0, 1)] * n), sitewise_shears(n, 4)
    )
    assert result["status"] == "EXACT_STABILIZER"
    assert result["faithful_dimension"] == 4 * n > p
    assert result["prefix_ranks"] == (1,) * n
    for i, certificate in enumerate(result["stage_certificates"]):
        assert certificate["common_nilpotency_index"] == 4
        assert certificate["augmented_dimension"] == 4 * n + 4
        assert certificate["ambient_lie_dimension"] == 6 * n - 3 * i
        assert certificate["stabilizer_lie_dimension"] == 6 * n - 3 * (i + 1)
    # RREF output has independent single-site factors. Enumerate only each UT3,
    # never UT4^n, its full tensor, or the 4^n-dimensional orbit span.
    local_generators = [[] for _ in range(n)]
    for generator in result["generators"]:
        support = [i for i, matrix in enumerate(generator) if matrix != eye(4)]
        assert len(support) == 1
        i = support[0]
        local_generators[i].append((generator[i],))
    for generators in local_generators:
        group = finite_group(generators, (4,), p)
        assert len(group) == p ** 3
        assert all(g[0][i][3] == int(i == 3) for g in group for i in range(4))
        assert all(g[0][i][j] == int(i == j) for g in group for i in range(4) for j in range(i + 1))
        h, g, g_inverse = shear(4, 1, 2), shear(4, 2, 3), shear(4, 2, 3, p - 1)
        assert (h,) in group
        assert (multiply(multiply(g, h, p), g_inverse, p),) not in group
    assert result["full_orbit_span_computed"] is False


def test_large_bond_one_abelian_fixture_uses_polynomial_action_sizes(monkeypatch):
    n, p = 32, 5
    real_guard = solver.compute_common_nonunital_algebra
    dimensions = []

    def bounded_guard(prime, dimension, generators, *, max_nilpotency_index):
        assert dimension == 2 * n + 2
        assert max_nilpotency_index == dimension
        dimensions.append(dimension)
        return real_guard(prime, dimension, generators, max_nilpotency_index=max_nilpotency_index)

    monkeypatch.setattr(solver, "compute_common_nonunital_algebra", bounded_guard)
    result = solver.recover_tensor_train_stabilizer(
        p, tensor_product_vectors([(0, 1)] * n), sitewise_shears(n, 2)
    )
    assert result["status"] == "EXACT_STABILIZER"
    assert result["generators"] == ()
    assert len(dimensions) == n
    assert result["prefix_ranks"] == (1,) * n
    assert sum(len(block) for core in result["minimized_cores"] for block in core) == 2 * n
    assert all(c["common_nilpotency_index"] == 2 for c in result["stage_certificates"])
    assert [c["stabilizer_lie_dimension"] for c in result["stage_certificates"]] == list(range(n - 1, -1, -1))
    assert result["full_orbit_span_computed"] is False


def test_large_prime_guard_search_bound_is_dimension_not_prime(monkeypatch):
    p = 2 ** 61 - 1
    real_guard = solver.compute_common_nonunital_algebra

    def bounded_guard(prime, dimension, generators, *, max_nilpotency_index):
        assert prime == p
        assert max_nilpotency_index == dimension == 4
        return real_guard(prime, dimension, generators, max_nilpotency_index=max_nilpotency_index)

    monkeypatch.setattr(solver, "compute_common_nonunital_algebra", bounded_guard)
    result = solver.recover_tensor_train_stabilizer(p, tensor_product_vectors([(0, 1)]), ((shear(2, 0, 1),),))
    assert result["status"] == "EXACT_STABILIZER"
    assert result["generators"] == ()


def test_127_bit_prime_uses_binary_powering_without_backend_overflow():
    result = solver.recover_tensor_train_stabilizer(
        2 ** 127 - 1, tensor_product_vectors([(0, 1)]), ((shear(2, 0, 1),),)
    )
    assert result["status"] == "EXACT_STABILIZER"
    assert result["generators"] == ()
    assert result["exact_subgroup_claim"] is True
    assert result["stage_certificates"][0]["all_generators_order_dividing_p"] is True


def test_broken_stage_preservation_is_rejected():
    with pytest.raises(RuntimeError, match="does not preserve"):
        solver._prefix_action((shear(2, 0, 1),), (((0,), (1,)),), 1, 5)


def test_corrupted_exponential_cannot_escape_faithful_consistency_check(monkeypatch):
    real_exp = solver.truncated_matrix_exp

    def corrupt_exp(matrix, p, nu):
        result = [list(row) for row in real_exp(matrix, p, nu)]
        result[0][-1] = 1
        return tuple(tuple(row) for row in result)

    monkeypatch.setattr(solver, "truncated_matrix_exp", corrupt_exp)
    with pytest.raises(RuntimeError, match="augmented-action consistency"):
        solver.recover_tensor_train_stabilizer(
            5, tensor_product_vectors([(1, 0)]), ((shear(2, 0, 1),),)
        )


def test_corrupted_final_scalar_is_rejected(monkeypatch):
    real_exp = solver.truncated_matrix_exp

    def corrupt_exp(matrix, p, nu):
        result = [list(row) for row in real_exp(matrix, p, nu)]
        result[0][0] = result[2][2] = 2
        return tuple(tuple(row) for row in result)

    monkeypatch.setattr(solver, "truncated_matrix_exp", corrupt_exp)
    with pytest.raises(RuntimeError, match="scalar-one"):
        solver.recover_tensor_train_stabilizer(
            5, tensor_product_vectors([(1, 0)]), ((shear(2, 0, 1),),)
        )


def test_deterministic_live_report_cli_source_hashes_and_scoped_claims(tmp_path, capsys):
    output = tmp_path / "tensor_train_stabilizer.json"
    solver.main(["--output", str(output)])
    report = json.loads(output.read_text(encoding="utf-8"))
    solver.main([])
    assert capsys.readouterr().out == output.read_text(encoding="utf-8")
    root = Path(solver.__file__).resolve().parents[1]
    assert set(report["source_hashes_sha256"]) == {
        "theorems/tensor_train_pgroup_stabilizer.py",
        "tests/test_tensor_train_pgroup_stabilizer.py",
        "theorems/moore_common_algebra_stabilizer_backend.py",
        "theorems/hpgp_coset_interface.py",
        "theorems/symbolic_scalar_phase_erasure.py",
        "theorems/ut5_matrix_phase_alignment.py",
        "theorems/prime_character_opi.py",
    }
    for name, digest in report["source_hashes_sha256"].items():
        assert name.startswith(("theorems/", "tests/"))
        assert digest == sha256((root / name).read_bytes()).hexdigest()
    ut4 = report["controls"]["ut4_product_f5_n3"]
    assert ut4["status"] == "EXACT_STABILIZER"
    assert ut4["full_orbit_dimension_analytic"] == 4 ** 3
    assert ut4["full_orbit_dimension_source"].startswith("analytic:")
    assert ut4["full_orbit_span_computed"] is False
    assert ut4["returned_generator_count"] == 9
    failure = report["controls"]["common_index_failure_f3"]
    assert failure["status"] == "UNSUPPORTED_COMMON_INDEX"
    assert failure["returned_generator_count"] is None
    assert failure["exact_subgroup_claim"] is False
    assert report["general_luks_implemented"] is False
    assert report["all_tensor_networks_dequantized_claim"] is False
    assert report["quantum_algorithm_claim"] is False
    assert report["hardness_claim"] is False
