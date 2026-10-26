"""Exact supplied-ring attack controls, not geometric or quantum execution."""

from itertools import product

import pytest
from flint import fmpz_mat, fmpz_mod_ctx, fmpz_mod_mat

from tests.test_siegel_repolarization import (
    PHI, adj, eye, form, kernel, mul, reduce,
)
from theorems.endomorphism_transport_recovery import (
    _flatten, _tuple, kernel_from_integral_transport,
    reconstruct_integral_transport, torsion_transport_coordinates,
)


def quaternion_basis():
    return [tuple(tuple(tuple(int((i, j, t) == (r, c, k)) for t in range(4))
                        for j in range(2)) for i in range(2))
            for r, c, k in product(range(2), range(2), range(4))]


def qflat(a):
    return tuple(x for row in a for quaternion in row for x in quaternion)


def diagonal(weights):
    return [[v if i == j else 0 for j in range(len(weights))]
            for i, v in enumerate(weights)]


def fixture_data(primes=(3, 5, 7, 13, 17), change=None):
    basis = quaternion_basis()
    weights = [2, 2, 22, 22]*4
    change = fmpz_mat(diagonal([1]*16)) if change is None else change
    gram = _tuple(change * fmpz_mat(diagonal(weights)) * change.transpose())
    residues = []
    for r in primes:
        ctx = fmpz_mod_ctx(r)
        source = [_tuple(reduce(a, r)) for a in basis]
        target_flat = fmpz_mod_mat([_flatten(a) for a in source], ctx)
        target_flat = fmpz_mod_mat(_tuple(change), ctx) * target_flat
        target = [tuple(tuple(int(target_flat[k, i*4+j]) for j in range(4))
                        for i in range(4)) for k in range(16)]
        # Independent nonzero common scalar at each prime; never recovered.
        w = _tuple((r-1) * reduce(PHI, r))
        residues.append((r, torsion_transport_coordinates(source, target, w, 61, r)))
    direct = fmpz_mat([qflat(mul(mul(PHI, a), adj(PHI))) for a in basis])
    expected = _tuple((direct * change.inv()).transpose())
    return gram, residues, [61**2 * x for x in weights], expected


def test_full_transport_reconstructed_without_hom_lattice_or_secret_torsion():
    gram, residues, bounds, expected = fixture_data()
    result = reconstruct_integral_transport(gram, residues, bounds)
    assert result.status == "UNIQUE_BOUNDED_TRANSPORT"
    assert result.matrix == expected
    answer = kernel_from_integral_transport(
        result.matrix, [_tuple(reduce(a, 61)) for a in quaternion_basis()],
        61, _tuple(form(2, 61)))
    assert answer.status == "RECOVERED_UNDER_INPUT_PROMISES"
    assert answer.kernel_basis == kernel(PHI, 61)
    assert answer.stabilizer_dimension == 12
    assert answer.annihilator_dimension == 4
    t = fmpz_mat(result.matrix)
    assert t.transpose()*fmpz_mat(gram)*t == fmpz_mat(diagonal([2, 2, 22, 22]*4))*61**2


def test_rosati_norm_transport_identity_for_every_basis_map():
    assert mul(adj(PHI), PHI) == tuple(
        tuple(tuple(61*x for x in q) for q in row) for row in eye(2))
    for a in quaternion_basis():
        f = mul(mul(PHI, a), adj(PHI))
        aa, ff = mul(adj(a), a), mul(adj(f), f)
        assert sum(2*ff[i][i][0] for i in range(2)) == 61**2 * sum(
            2*aa[i][i][0] for i in range(2))


@pytest.mark.parametrize("r", [3, 5, 7, 13, 17])
def test_every_common_nonzero_scalar_cancels_but_per_column_scalars_do_not(r):
    source = [_tuple(reduce(a, r)) for a in quaternion_basis()]
    w = reduce(PHI, r)
    expected = torsion_transport_coordinates(source, source, _tuple(w), 61, r)
    for scalar in range(1, r):
        assert torsion_transport_coordinates(source, source, _tuple(scalar*w), 61, r) == expected
    bad = w * type(w)(diagonal([1, r-1, 1, 1]), r)
    assert torsion_transport_coordinates(source, source, _tuple(bad), 61, r) != expected


def test_auxiliary_target_basis_changes_cancel_when_applied_consistently():
    r, ctx = 13, fmpz_mod_ctx(13)
    source = [_tuple(reduce(a, r)) for a in quaternion_basis()]
    w = fmpz_mod_mat(_tuple(reduce(PHI, r)), ctx)
    change = fmpz_mod_mat([[1, 2, 0, 0], [0, 1, 3, 0],
                           [0, 0, 1, 4], [0, 0, 0, 1]], ctx)
    target = [_tuple(change.inv() * fmpz_mod_mat(a, ctx) * change) for a in source]
    assert torsion_transport_coordinates(source, target, _tuple(change.inv()*w), 61, r) == (
        torsion_transport_coordinates(source, source, _tuple(w), 61, r))


def test_ill_conditioned_integral_target_basis_needs_its_actual_gram_bound():
    change = fmpz_mat(diagonal([1]*16))
    change[0, 1] = 10**12
    change[2, 7] = -10**10
    primes = (3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
    gram, residues, bounds, expected = fixture_data(primes, change)
    result = reconstruct_integral_transport(gram, residues, bounds)
    assert result.status == "UNIQUE_BOUNDED_TRANSPORT"
    assert result.matrix == expected
    assert result.max_coordinate_bound > 10**12
    assert reconstruct_integral_transport(gram, residues[:4], bounds).status == "UNKNOWN"


def test_small_level_is_unknown_and_strict_boundary_has_two_lifts():
    result = reconstruct_integral_transport([[1]], [(2, [[1]])], [1])
    assert result.status == "UNKNOWN"
    assert result.product_level == 2*result.max_coordinate_bound
    assert 1 % 2 == (-1) % 2


def test_wrong_norm_and_corrupted_residue_cannot_be_admitted():
    assert reconstruct_integral_transport([[1]], [(7, [[3]])], [1]).status == "UNKNOWN"
    gram, residues, bounds, _ = fixture_data()
    prime, matrix = residues[0]
    bad = [list(row) for row in matrix]
    bad[0][0] += 1
    result = reconstruct_integral_transport(gram, [(prime, bad)] + residues[1:], bounds)
    assert result.status == "UNKNOWN"


def test_zero_transport_columns_are_legal_exact_residues_not_projective_lines():
    result = reconstruct_integral_transport([[1]], [(3, [[0, 1]])], [0, 1])
    assert result.status == "UNIQUE_BOUNDED_TRANSPORT"
    assert result.matrix == ((0, 1),)


def matrix_units(d):
    return [tuple(tuple(int((i, j) == (r, c)) for j in range(d)) for i in range(d))
            for r, c in product(range(d), repeat=2)]


def local_transport(n, p):
    ctx, d = fmpz_mod_ctx(p), 2*n
    rows = diagonal([1]*d)
    for i, j in product(range(n), repeat=2):
        rows[n+i][j] = (i+1)*(j+1) + int(i == j)
    change = fmpz_mod_mat(rows, ctx)
    phi = change * fmpz_mod_mat(diagonal([0]*n+[1]*n), ctx) * change.inv()
    dual = change * fmpz_mod_mat(diagonal([1]*n+[0]*n), ctx) * change.inv()
    units = matrix_units(d)
    columns = [_flatten(_tuple(phi * fmpz_mod_mat(a, ctx) * dual)) for a in units]
    form_ = tuple(tuple(int(i < n and j == n+i)-int(j < n and i == n+j)
                        for j in range(d)) for i in range(d))
    return tuple(zip(*columns)), units, form_, phi, dual


@pytest.mark.parametrize("n,p", [(1, 3), (2, 3), (2, 61), (3, 7), (2, 2**127-1)])
def test_split_local_recovery_without_enumeration_at_large_secret_prime(n, p):
    transport, units, form_, phi, _ = local_transport(n, p)
    result = kernel_from_integral_transport(transport, units, p, form_)
    assert result.status == "RECOVERED_UNDER_INPUT_PROMISES"
    k = fmpz_mod_mat(list(zip(*result.kernel_basis)), fmpz_mod_ctx(p))
    assert (phi*k).rank() == 0
    assert k.rank() == n


def test_reversing_isogeny_and_dual_recovers_the_wrong_kernel_not_a_detectable_typo():
    forward, units, form_, phi, dual = local_transport(2, 61)
    ctx = fmpz_mod_ctx(61)
    reverse = tuple(zip(*[_flatten(_tuple(dual*fmpz_mod_mat(a, ctx)*phi)) for a in units]))
    good = kernel_from_integral_transport(forward, units, 61, form_)
    wrong = kernel_from_integral_transport(reverse, units, 61, form_)
    assert good.status == wrong.status == "RECOVERED_UNDER_INPUT_PROMISES"
    assert good.kernel_basis != wrong.kernel_basis
    assert (phi*fmpz_mod_mat(list(zip(*wrong.kernel_basis)), ctx)).rank() == 2


def test_fullness_at_secret_prime_cannot_be_inferred_from_auxiliary_actions():
    # Local order S={[[a,p^2*b],[c,d]] : a=d mod p}; it contains phi*R*dual
    # for phi=diag(p,1), dual=diag(1,p), but is not p-saturated in M_2(Z).
    p = 7
    target = [[[1, 0], [0, 1]], [[p, 0], [0, 0]],
              [[0, p*p], [0, 0]], [[0, 0], [1, 0]]]
    source = matrix_units(2)
    r = 11
    measured = torsion_transport_coordinates(source, target, [[p, 0], [0, 1]], p, r)
    expected = ((0, 0, 0, p), (1, 0, 0, -1), (0, 1, 0, 0), (0, 0, 1, 0))
    assert measured == tuple(tuple(x % r for x in row) for row in expected)
    result = kernel_from_integral_transport(expected, source, p, [[0, 1], [-1, 0]])
    assert result.status == "UNKNOWN"
    assert result.stabilizer_dimension == 1  # Not the true dimension-three algebra.


def test_correct_dimension_alone_is_not_a_parabolic_certificate():
    # For d=2 an arbitrary hyperplane has the expected dimension three.
    # Tr(a)=0 has annihilator span(I), whose image is too large.
    transport = [[1, 0, 0, 1], [0]*4, [0]*4, [0]*4]
    result = kernel_from_integral_transport(transport, matrix_units(2), 7, [[0, 1], [-1, 0]])
    assert result.status == "UNKNOWN"
    assert "image" in result.reason


def test_correct_dimensions_and_image_do_not_replace_preservation_check():
    units = matrix_units(4)
    columns = [tuple(a[i][j] if k < 4 else 0 for k, (i, j) in enumerate(
        [(0, 0), (0, 1), (1, 0), (1, 1)]+[(0, 0)]*12)) for a in units]
    result = kernel_from_integral_transport(tuple(zip(*columns)), units, 7,
                                            local_transport(2, 7)[2])
    assert result.stabilizer_dimension == 12
    assert result.annihilator_dimension == 4
    assert result.status == "UNKNOWN"
    assert "preserve" in result.reason


@pytest.mark.parametrize("p", [3, 5])
def test_every_small_matrix_obeys_divisibility_iff_kernel_preservation(p):
    transport, _, form_, phi, _ = local_transport(1, p)
    ctx = fmpz_mod_ctx(p)
    t = fmpz_mod_mat(transport, ctx)
    answer = kernel_from_integral_transport(transport, matrix_units(2), p, form_)
    k = fmpz_mod_mat(list(zip(*answer.kernel_basis)), ctx)
    for entries in product(range(p), repeat=4):
        a = fmpz_mod_mat([entries[:2], entries[2:]], ctx)
        divisible = (t * fmpz_mod_mat([[x] for x in entries], ctx)).rank() == 0
        preserves = (phi*a*k).rank() == 0
        assert divisible == preserves


def test_nonlagrangian_half_space_is_rejected_even_with_valid_parabolic_algebra():
    p, ctx = 7, fmpz_mod_ctx(7)
    phi = fmpz_mod_mat(diagonal([0, 0, 1, 1]), ctx)
    dual = fmpz_mod_mat(diagonal([1, 1, 0, 0]), ctx)
    units = matrix_units(4)
    transport = tuple(zip(*[_flatten(_tuple(phi*fmpz_mod_mat(a, ctx)*dual)) for a in units]))
    result = kernel_from_integral_transport(transport, units, p, _tuple(form(2, p)))
    assert result.status == "UNKNOWN"
    assert "Lagrangian" in result.reason


@pytest.mark.parametrize("gram,residues,bounds", [
    ([[1]], [], [1]), ([[1]], [(9, [[1]])], [1]),
    ([[1]], [(3, [[1]]), (3, [[1]])], [1]),
    ([[1]], [(3, [[1, 2]])], [1]), ([[1]], [(3, [[1]])], [True]),
    ([[1, 2], [2, 1]], [(3, [[1], [1]])], [1]),
    ([[1, 0], [1, 1]], [(3, [[1], [1]])], [1]),
])
def test_invalid_reconstruction_contract(gram, residues, bounds):
    with pytest.raises(ValueError):
        reconstruct_integral_transport(gram, residues, bounds)


def test_singular_or_incomplete_torsion_data_rejected():
    units = matrix_units(2)
    for source, target, w, ell, p in [
        (units, units, [[1, 0], [0, 0]], 7, 3),
        (units[:-1], units, [[1, 0], [0, 1]], 7, 3),
        (units, [units[0]]*4, [[1, 0], [0, 1]], 7, 3),
        (units, units, [[1, 0], [0, 1]], 7, 7),
    ]:
        with pytest.raises(ValueError):
            torsion_transport_coordinates(source, target, w, ell, p)
