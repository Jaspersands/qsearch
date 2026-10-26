from copy import deepcopy
from itertools import combinations, product
import random

from flint import fmpz_mod_ctx, fmpz_mod_mat
import pytest

from theorems.class_three_ambient_frontend import _subspace_intersection
from theorems.jet_oracle_homogenization import lie_bch
from theorems.rees_hsp_reduction import _units, make_rees_cover
from theorems.rees_nongradable_control import (
    build_report, check_public_cover, derivation_equations,
    dixmier_lister_algebra, integer_derivation_certificate, integer_tensor,
    verify_row_certificate,
)
from theorems.symbolic_scalar_phase_erasure import _fmpz_nullspace_basis, _fmpz_solve_coordinates


def test_integer_jacobi_identity_not_only_modular_samples():
    tensor = integer_tensor()
    for i, j, k in combinations(range(8), 3):
        for out in range(8):
            assert sum(tensor[b][c][a]*tensor[d][a][out]
                       for d, b, c in ((i, j, k), (j, k, i), (k, i, j))
                       for a in range(8)) == 0


def test_universal_integer_implications_and_small_prime_exceptions():
    rows = derivation_equations(integer_tensor())
    report = integer_derivation_certificate()
    certificates = report["integer_row_certificates"]
    assert {c["entry"] for c in certificates} == set(range(32))
    assert all(verify_row_certificate(rows, c) for c in certificates)
    assert {c["multiplier"] for c in certificates} == {1, 3, 6}
    assert report["nonzero_smith_factors"] == (1,)*48+(3, 3, 6, 6)
    for p, rank in ((2, 50), (3, 48)):
        assert fmpz_mod_mat(rows, fmpz_mod_ctx(p)).rref()[1] == rank
    bad = deepcopy(certificates[0])
    bad["entry"] = (bad["entry"]+1) % 32
    assert not verify_row_certificate(rows, bad)
    bad = deepcopy(certificates[0])
    bad["multiplier"] = 0
    assert not verify_row_certificate(rows, bad)


@pytest.mark.parametrize("p", [5, 7, 43, 2**127-1])
def test_all_derivations_not_just_diagonal_or_inner_ones(p):
    source = dixmier_lister_algebra(p)
    rows = derivation_equations(integer_tensor())
    kernel = _fmpz_nullspace_basis([tuple(x % p for x in row) for row in rows], 64, p)
    assert len(kernel) == 12
    context = fmpz_mod_ctx(p)
    rng = random.Random(835)
    scalars = [rng.randrange(p) for _ in kernel]
    vectors = list(kernel)+[tuple(sum(t*v[i] for t, v in zip(scalars, kernel)) % p
                                  for i in range(64))]
    units = _units(8)
    for vector in vectors:
        assert not any(vector[:32])
        matrix = [vector[8*i:8*i+8] for i in range(8)]
        D = fmpz_mod_mat(matrix, context)
        assert not any(x for row in (D*D*D).tolist() for x in row)
        image = lambda v: tuple(sum(a*b for a, b in zip(row, v)) % p for row in matrix)
        for x, y in combinations(units, 2):
            lhs = image(source.bracket(x, y))
            rhs = tuple((a+b) % p for a, b in zip(source.bracket(image(x), y),
                                                 source.bracket(x, image(y))))
            assert lhs == rhs


@pytest.mark.parametrize("p,copies", [(5, 1), (7, 1), (43, 2), (2**127-1, 1)])
def test_public_cover_works_where_original_weight_dilation_fails(p, copies):
    result = check_public_cover(p, copies)
    assert result["lower_central_dimensions"] == (8*copies, 4*copies, 2*copies)
    assert result["cover_dimension"] == 14*copies
    assert result["queries_per_lifted_source"] == 3
    assert result["naive_dilation_of_bracket_e1_e4"] != result["bracket_of_naively_dilated_e1_e4"]
    assert result["nonidentity_order_two_automorphism_exists"]
    assert not result["hidden_advice_used_by_public_compiler"]


def _lift_hidden(cover, hidden):
    lifted = []
    for degree, level in enumerate(cover.levels, 1):
        for vector in _subspace_intersection(hidden, level, cover.source.dimension, cover.p):
            coordinates = _fmpz_solve_coordinates(level, vector, cover.p)
            lifted.append(tuple(coordinates[j] if r == degree else 0 for r, j in cover.indices))
    return tuple(lifted)


def test_nonnormal_nonabelian_hidden_subgroup_actual_tuple_oracle_pairs():
    p = 5
    source = dixmier_lister_algebra(p)
    units = _units(8)
    hidden = (units[0], units[4], units[7])
    assert source.nilpotency_class(hidden) == 2
    assert _fmpz_solve_coordinates(hidden, source.bracket(units[2], units[0]), p) is None
    elements = [tuple(sum(t*v[j] for t, v in zip(coeff, hidden)) % p for j in range(8))
                for coeff in product(range(p), repeat=3)]
    calls = []
    def oracle(x):
        calls.append(x)
        # Bounded fixture only: enumerate H, never an algorithmic oracle backend.
        return min(lie_bch(source, x, h, 3) for h in elements)
    cover = make_rees_cover(source, units)
    assert not calls
    lifted = _lift_hidden(cover, hidden)
    assert len(lifted) == 6
    for x, y in product(lifted, repeat=2):
        assert _fmpz_solve_coordinates(lifted, cover.algebra.bracket(x, y), p) is not None
    rng = random.Random(851)
    for _ in range(4):
        x = tuple(rng.randrange(p) for _ in range(cover.dimension))
        scalars = [rng.randrange(p) for _ in lifted]
        h = tuple(sum(t*v[j] for t, v in zip(scalars, lifted)) % p for j in range(cover.dimension))
        y = cover.multiply(x, h)
        before = len(calls)
        assert cover.evaluate_fixture(oracle, x) == cover.evaluate_fixture(oracle, y)
        assert len(calls)-before == 6
        assert _fmpz_solve_coordinates(lifted, cover.dilate(h, 2), p) is not None
    # t(t-1)(t-2)e7 defeats a two-point shortcut on this nongradable input.
    coefficients = (2, -3, 1)
    bad = [0]*cover.dimension
    for r, level in enumerate(cover.levels, 1):
        coordinates = _fmpz_solve_coordinates(level, units[6], p)
        for index, (degree, j) in enumerate(cover.indices):
            if degree == r:
                bad[index] = coefficients[r-1]*coordinates[j] % p
    origin = cover.evaluate_fixture(oracle, (0,)*cover.dimension)
    labels = cover.evaluate_fixture(oracle, tuple(bad))
    assert labels[:2] == origin[:2] and labels[2] != origin[2]
    assert source.span([v[:8] for v in lifted]) == source.span(hidden)


def test_same_prime_direct_sum_hidden_diagonal_cannot_be_split_factorwise():
    p = 7
    source = dixmier_lister_algebra(p, 2)
    cover = make_rees_cover(source, _units(16))
    hidden = tuple(v+v for v in _units(8))
    assert source.nilpotency_class(hidden) == 3
    assert not _subspace_intersection(hidden, _units(16)[:8], 16, p)
    assert not _subspace_intersection(hidden, _units(16)[8:], 16, p)
    lifted = _lift_hidden(cover, hidden)
    assert len(lifted) == 14
    assert source.span([v[:16] for v in lifted]) == source.span(hidden)
    for x, y in product(lifted, repeat=2):
        assert _fmpz_solve_coordinates(lifted, cover.algebra.bracket(x, y), p) is not None
    for x in lifted:
        assert all(v[:8] == v[8:] for v in cover.inputs(x))


def test_scope_flags_do_not_promote_algebraic_checks_to_quantum_recovery():
    report = build_report()
    for flag in ("full_quantum_instrument_executed_on_this_input", "arbitrary_hsp_recovery_implemented",
                 "independent_review", "novelty_established", "speedup_claim_allowed"):
        assert report[flag] is False


@pytest.mark.parametrize("p,copies", [(2, 1), (3, 1), (9, 1), (7, 0), (7, True)])
def test_bad_contracts_rejected(p, copies):
    with pytest.raises(ValueError):
        dixmier_lister_algebra(p, copies)
