"""Reverse attack controls on exact algebra, not geometric point execution."""

from itertools import product

import pytest
from flint import fmpz_mat, fmpz_mod_ctx, fmpz_mod_mat

from tests.test_endomorphism_transport_recovery import diagonal, matrix_units, qflat
from tests.test_siegel_repolarization import (
    ONE, ZERO, PHI, add, adj, eye, form, kernel, mul, reduce, scale,
)
from theorems.endomorphism_transport_recovery import _flatten, _tuple
from theorems.siegel_reverse_transport import (
    kernel_from_reverse_transport, reconstruct_reverse_transport,
    reverse_torsion_coordinates,
)


def quaternion_basis(g=2):
    return [tuple(tuple(tuple(int((i, j, t) == (r, c, k)) for t in range(4))
                        for j in range(g)) for i in range(g))
            for r, c, k in product(range(g), range(g), range(4))]


def integer_matrix(rows):
    return tuple(tuple((v, 0, 0, 0) for v in row) for row in rows)


PRODUCT_PHI = integer_matrix([[6, 5], [-5, 6]])
INVOLUTION = integer_matrix([[1, 0], [0, -1]])
PRIMES = (3, 5, 7, 13)


def changed_actions(basis, change, prime):
    ctx = fmpz_mod_ctx(prime)
    original = fmpz_mod_mat([_flatten(_tuple(reduce(a, prime))) for a in basis], ctx)
    changed = fmpz_mod_mat(_tuple(change), ctx) * original
    dimension = 2 * len(basis[0])
    return [tuple(tuple(int(changed[k, i*dimension+j]) for j in range(dimension))
                  for i in range(dimension)) for k in range(len(basis))]


def fixture_data(phi=PRODUCT_PHI, automorphisms=(INVOLUTION,), primes=PRIMES,
                 change=None):
    g = len(phi)
    basis = quaternion_basis(g)
    rank = len(basis)
    change = fmpz_mat(diagonal([1]*rank)) if change is None else change
    gram = _tuple(change * fmpz_mat(diagonal([2, 2, 22, 22]*(g*g)))
                  * change.transpose())
    residues = []
    for index, prime in enumerate(primes):
        mask = 1 + (2*index+1) % (prime-1)
        residues.append((prime, reverse_torsion_coordinates(
            changed_actions(basis, change, prime),
            [_tuple(reduce(u, prime)) for u in automorphisms],
            _tuple(mask * reduce(phi, prime)), 61, prime,
            source_form=_tuple(form(g, prime)), target_form=_tuple(form(g, prime)))))
    reverse = [mul(mul(adj(phi), u), phi) for u in automorphisms]
    expected = _tuple((fmpz_mat([qflat(a) for a in reverse]) * change.inv()).transpose())
    return gram, residues, expected, changed_actions(basis, change, 61)


def recover_fixture(phi=PRODUCT_PHI, automorphisms=(INVOLUTION,)):
    gram, residues, expected, split = fixture_data(phi, automorphisms)
    reconstructed = reconstruct_reverse_transport(gram, residues, 61)
    assert reconstructed.status == "UNIQUE_BOUNDED_TRANSPORT"
    assert reconstructed.matrix == expected
    return kernel_from_reverse_transport(reconstructed.matrix, split, 61,
                                         _tuple(form(len(phi), 61)))


def test_actual_product_fixture_recovers_abstract_61_kernel_in_known_source_order():
    assert mul(adj(PRODUCT_PHI), PRODUCT_PHI) == scale(61, eye(2))
    assert mul(adj(INVOLUTION), INVOLUTION) == eye(2)
    beta = mul(mul(adj(PRODUCT_PHI), INVOLUTION), PRODUCT_PHI)
    assert beta == integer_matrix([[11, 60], [60, -11]])
    assert mul(adj(beta), beta) == scale(61**2, eye(2))
    result = recover_fixture()
    assert result.status == "RECOVERED_UNDER_INPUT_PROMISES"
    assert result.kernel_basis == ((1, 0, 11, 0), (0, 1, 0, 11))
    assert result.kernel_basis == kernel(PRODUCT_PHI, 61)
    assert result.image_dimension == 2
    assert result.map_ranks == (2,)


@pytest.mark.parametrize("prime", PRIMES + (17,))
def test_every_common_mask_cancels_without_square_roots_or_sign_synchronization(prime):
    source = [_tuple(reduce(a, prime)) for a in quaternion_basis()]
    u = [_tuple(reduce(INVOLUTION, prime))]
    kwargs = dict(source_form=_tuple(form(2, prime)), target_form=_tuple(form(2, prime)))
    expected = reverse_torsion_coordinates(source, u, _tuple(reduce(PRODUCT_PHI, prime)),
                                           61, prime, **kwargs)
    for mask in range(1, prime):
        assert reverse_torsion_coordinates(
            source, u, _tuple(mask*reduce(PRODUCT_PHI, prime)), 61, prime,
            **kwargs) == expected


def test_using_the_weak_images_as_target_basis_gives_the_same_coordinates():
    p, ctx = 13, fmpz_mod_ctx(13)
    source = [_tuple(reduce(a, p)) for a in quaternion_basis()]
    w = fmpz_mod_mat(_tuple(7*reduce(PRODUCT_PHI, p)), ctx)
    u = fmpz_mod_mat(_tuple(reduce(INVOLUTION, p)), ctx)
    j = fmpz_mod_mat(_tuple(form(2, p)), ctx)
    expected = reverse_torsion_coordinates(source, [_tuple(u)], _tuple(w), 61, p,
                                           source_form=_tuple(j), target_form=_tuple(j))
    assert reverse_torsion_coordinates(
        source, [_tuple(w.inv()*u*w)], diagonal([1]*4), 61, p,
        source_form=_tuple(j), target_form=_tuple(w.transpose()*j*w)) == expected


def test_arbitrary_target_coordinate_change_transports_its_form_too():
    p, ctx = 13, fmpz_mod_ctx(13)
    source = [_tuple(reduce(a, p)) for a in quaternion_basis()]
    w = fmpz_mod_mat(_tuple(reduce(PRODUCT_PHI, p)), ctx)
    u = fmpz_mod_mat(_tuple(reduce(INVOLUTION, p)), ctx)
    j = fmpz_mod_mat(_tuple(form(2, p)), ctx)
    c = fmpz_mod_mat([[1, 2, 0, 0], [0, 1, 3, 0],
                      [0, 0, 1, 4], [0, 0, 0, 1]], ctx)
    expected = reverse_torsion_coordinates(source, [_tuple(u)], _tuple(w), 61, p,
                                           source_form=_tuple(j), target_form=_tuple(j))
    assert reverse_torsion_coordinates(
        source, [_tuple(c.inv()*u*c)], _tuple(c.inv()*w), 61, p,
        source_form=_tuple(j), target_form=_tuple(c.transpose()*j*c)) == expected


def test_symplectic_column_tampering_cannot_be_authenticated_by_algebraic_checks():
    # Relative to PRODUCT_PHI, these are per-column signs, not a common mask.
    # They also describe a different genuine isogeny: provenance is external.
    altered_phi = mul(PRODUCT_PHI, INVOLUTION)
    result = recover_fixture(altered_phi)
    assert result.status == "RECOVERED_UNDER_INPUT_PROMISES"
    assert result.kernel_basis == kernel(altered_phi, 61)
    assert result.kernel_basis != kernel(PRODUCT_PHI, 61)


def test_multiple_geometric_automorphisms_can_jointly_span_when_each_is_insufficient():
    s, t = PHI[0][0], PHI[1][1]
    phi = ((s, ZERO, ZERO), (ZERO, t, ZERO), (ZERO, ZERO, s))
    swap12 = integer_matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    swap23 = integer_matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    for u in (swap12, swap23):
        assert mul(adj(u), u) == eye(3)
        partial = recover_fixture(phi, (u,))
        assert partial.status == "UNKNOWN"
        assert partial.image_dimension == 2
        assert partial.map_ranks == (2,)
        assert "insufficient image" in partial.reason
    result = recover_fixture(phi, (swap12, swap23))
    assert result.status == "RECOVERED_UNDER_INPUT_PROMISES"
    assert result.map_ranks == (2, 2)
    assert result.image_dimension == 3
    assert result.kernel_basis == kernel(phi, 61)


def test_plus_and_minus_identity_give_exact_maps_but_zero_kernel_information():
    gram, residues, expected, split = fixture_data(
        automorphisms=(eye(2), scale(-1, eye(2))))
    result = reconstruct_reverse_transport(gram, residues, 61)
    assert result.matrix == expected
    assert result.status == "UNIQUE_BOUNDED_TRANSPORT"
    for row, unit in zip(expected, qflat(eye(2))):
        assert row == (61*unit, -61*unit)
    answer = kernel_from_reverse_transport(result.matrix, split, 61, _tuple(form(2, 61)))
    assert answer.status == "UNKNOWN"
    assert answer.kernel_basis is None
    assert answer.map_ranks == (0, 0)
    assert answer.image_dimension == 0
    assert "zero information" in answer.reason


def test_commuting_nonscalar_target_automorphism_can_also_give_zero_information():
    assert INVOLUTION != eye(2)
    assert INVOLUTION != scale(-1, eye(2))
    assert mul(PHI, INVOLUTION) == mul(INVOLUTION, PHI)
    assert mul(mul(adj(PHI), INVOLUTION), PHI) == scale(61, INVOLUTION)
    result = recover_fixture(PHI, (INVOLUTION,))
    assert result.status == "UNKNOWN"
    assert result.kernel_basis is None
    assert result.image_dimension == 0
    assert result.map_ranks == (0,)
    assert "zero information" in result.reason


def test_insufficient_level_never_returns_an_integer_transport():
    gram, residues, _, _ = fixture_data()
    result = reconstruct_reverse_transport(gram, residues[:2], 61)
    assert result.status == "UNKNOWN"
    assert result.matrix is None
    assert result.product_level == 15
    assert result.max_coordinate_bound == 86
    assert "insufficient level" in result.reason


def test_source_basis_change_uses_the_actual_gram_and_consistent_split():
    change = fmpz_mat(diagonal([1]*16))
    change[0, 1] = 10**6
    primes = PRIMES + (17, 19, 23, 29, 31)
    gram, residues, expected, split = fixture_data(primes=primes, change=change)
    assert reconstruct_reverse_transport(gram, residues[:4], 61).status == "UNKNOWN"
    result = reconstruct_reverse_transport(gram, residues, 61)
    assert result.status == "UNIQUE_BOUNDED_TRANSPORT"
    assert result.matrix == expected
    assert result.max_coordinate_bound > 10**6
    answer = kernel_from_reverse_transport(result.matrix, split, 61, _tuple(form(2, 61)))
    assert answer.kernel_basis == kernel(PRODUCT_PHI, 61)


def test_upper_bound_alone_does_not_certify_the_exact_reverse_rosati_norm():
    gram, residues, _, _ = fixture_data()
    zero = tuple(tuple(0 for _ in row) for row in residues[0][1])
    result = reconstruct_reverse_transport(gram, [(r, zero) for r, _ in residues], 61)
    assert result.status == "UNKNOWN"
    assert result.matrix is None
    assert "exact polarized reverse Rosati norm" in result.reason


def test_corrupted_residue_cannot_pass_bounded_reconstruction():
    gram, residues, _, _ = fixture_data()
    prime, matrix = residues[0]
    bad = [list(row) for row in matrix]
    bad[0][0] += 1
    result = reconstruct_reverse_transport(gram, [(prime, bad)] + residues[1:], 61)
    assert result.status == "UNKNOWN"
    assert result.matrix is None


def local_recovery(maps, prime=61, form_=None):
    d = len(maps[0])
    if form_ is None:
        form_ = [[int(i < d//2 and j == d//2+i)
                  - int(j < d//2 and i == d//2+j) for j in range(d)] for i in range(d)]
    coefficients = tuple(zip(*[_flatten(a) for a in maps]))
    return kernel_from_reverse_transport(coefficients, matrix_units(d), prime, form_)


@pytest.mark.parametrize("prime", [3, 61, 2**127-1])
def test_large_prime_image_span_uses_linear_algebra_not_kernel_enumeration(prime):
    a = [[0, 0, 1, 0], [0, 0, 0, 0], [0]*4, [0]*4]
    b = [[0]*4, [0, 0, 0, 1], [0]*4, [0]*4]
    result = local_recovery([a, b], prime)
    assert result.status == "RECOVERED_UNDER_INPUT_PROMISES"
    assert result.kernel_basis == ((1, 0, 0, 0), (0, 1, 0, 0))
    assert result.map_ranks == (1, 1)


@pytest.mark.parametrize("maps,reason", [
    ([diagonal([1, 1, 1, 0])], "individual reverse map"),
    ([diagonal([1, 0, 0, 0]), diagonal([0, 1, 1, 0])], "combined image rank"),
    ([[[0, 1, 0, 0], [0]*4, [0, 0, 0, 1], [0]*4]], "not isotropic"),
    ([diagonal([1, 1, 0, 0])], "do not annihilate"),
])
def test_rank_nonisotropy_and_common_kernel_inconsistencies_are_unknown(maps, reason):
    result = local_recovery(maps)
    assert result.status == "UNKNOWN"
    assert result.kernel_basis is None
    assert reason in result.reason


def test_individually_square_zero_maps_must_also_annihilate_each_others_images():
    a = [[0, 1, 0, 0], [0]*4, [0]*4, [0]*4]
    b = [[0]*4, [0, 0, 0, 1], [0]*4, [0]*4]
    assert fmpz_mat(a)**2 == fmpz_mat(4, 4)
    assert fmpz_mat(b)**2 == fmpz_mat(4, 4)
    result = local_recovery([a, b])
    assert result.status == "UNKNOWN"
    assert result.image_dimension == 2
    assert result.map_ranks == (1, 1)
    assert "do not annihilate" in result.reason


def test_forward_generated_algebra_has_zero_reverse_information_identically():
    phi = PRODUCT_PHI
    basis = quaternion_basis()
    forwards = [mul(mul(phi, a), adj(phi)) for a in basis]
    for a, f in zip(basis, forwards):
        u = add(scale(3, eye(2)), f)
        beta = mul(mul(adj(phi), u), phi)
        assert beta == add(scale(3*61, eye(2)), scale(61**2, a))
        assert all(x % 61 == 0 for x in qflat(beta))
    for a, fa in zip(basis, forwards):
        for b, fb in zip(basis, forwards):
            assert mul(fa, fb) == scale(61, mul(mul(phi, mul(a, b)), adj(phi)))
    coefficients = tuple(zip(*[qflat(mul(mul(adj(phi), f), phi)) for f in forwards]))
    result = kernel_from_reverse_transport(
        coefficients, [_tuple(reduce(a, 61)) for a in basis], 61, _tuple(form(2, 61)))
    assert result.status == "UNKNOWN"
    assert result.image_dimension == 0
    assert result.map_ranks == (0,)*16


@pytest.mark.parametrize("failure", [
    "incomplete", "singular_source", "singular_transport", "per_column_masks",
    "nonsquare_multiplier", "unpolarized_target", "empty_target", "wrong_shape",
    "degenerate_form", "nonalternating_form", "bad_entry", "odd_dimension",
])
def test_invalid_torsion_contracts_raise_value_error(failure):
    p = 13
    source = [_tuple(reduce(a, p)) for a in quaternion_basis()]
    target = [_tuple(reduce(INVOLUTION, p))]
    w = _tuple(reduce(PRODUCT_PHI, p))
    ja = jb = _tuple(form(2, p))
    if failure == "incomplete":
        source = source[:-1]
    elif failure == "singular_source":
        source = [source[0]]*16
    elif failure == "singular_transport":
        w = diagonal([1, 1, 1, 0])
    elif failure == "per_column_masks":
        w = _tuple(reduce(PRODUCT_PHI, p) * type(reduce(PRODUCT_PHI, p))(
            diagonal([2, 1, 1, 1]), p))
    elif failure == "nonsquare_multiplier":
        # 2 is a nonsquare mod 13: W has multiplier 2*ell, not ell*a^2.
        w = _tuple(reduce(PRODUCT_PHI, p) * type(reduce(PRODUCT_PHI, p))(
            diagonal([2, 1, 2, 1]), p))
    elif failure == "unpolarized_target":
        target = [diagonal([2, 2, 2, 2])]
    elif failure == "empty_target":
        target = []
    elif failure == "wrong_shape":
        w = [[1, 2], [3, 4], [5, 6], [7, 8]]
    elif failure == "degenerate_form":
        jb = diagonal([0]*4)
    elif failure == "nonalternating_form":
        ja = diagonal([1]*4)
    elif failure == "bad_entry":
        target = [[[True, 0], [0, 1]]]
    elif failure == "odd_dimension":
        w = diagonal([1]*3)
    with pytest.raises(ValueError):
        reverse_torsion_coordinates(source, target, w, 61, p,
                                    source_form=ja, target_form=jb)


@pytest.mark.parametrize("prime,multiplier", [(2, 61), (9, 61), (61, 61), (13, 9),
                                               (13, True), (13, 2)])
def test_invalid_auxiliary_and_secret_primes(prime, multiplier):
    with pytest.raises(ValueError):
        reverse_torsion_coordinates(matrix_units(2), [diagonal([1]*2)],
                                    diagonal([1]*2), multiplier, prime,
                                    source_form=[[0, 1], [-1, 0]],
                                    target_form=[[0, 1], [-1, 0]])


@pytest.mark.parametrize("failure", ["empty", "duplicate", "secret_prime", "two",
                                      "bad_gram", "wrong_rank", "column_count"])
def test_invalid_reconstruction_contracts(failure):
    gram, residues, _, _ = fixture_data()
    if failure == "empty":
        residues = []
    elif failure == "duplicate":
        residues = residues + residues[:1]
    elif failure == "secret_prime":
        residues = [(61, residues[0][1])]
    elif failure == "two":
        residues = [(2, residues[0][1])]
    elif failure == "bad_gram":
        gram = diagonal([-1]+[1]*15)
    elif failure == "wrong_rank":
        gram = diagonal([1]*9)
    elif failure == "column_count":
        residues[1] = (residues[1][0], [(0, 0)]*16)
    with pytest.raises(ValueError):
        reconstruct_reverse_transport(gram, residues, 61)


@pytest.mark.parametrize("failure", ["incomplete", "singular", "wrong_rows",
                                      "bad_form", "odd_dimension", "bad_prime"])
def test_invalid_kernel_recovery_contracts(failure):
    units = matrix_units(4)
    transport = [[0] for _ in units]
    j = _tuple(form(2, 61))
    p = 61
    if failure == "incomplete":
        units = units[:-1]
    elif failure == "singular":
        # Auxiliary invertibility alone would not detect an index-ell basis.
        units[0] = tuple(tuple(61*x for x in row) for row in units[0])
    elif failure == "wrong_rows":
        transport = transport[:-1]
    elif failure == "bad_form":
        j = diagonal([1]*4)
    elif failure == "odd_dimension":
        j = diagonal([1]*3)
    elif failure == "bad_prime":
        p = 9
    with pytest.raises(ValueError):
        kernel_from_reverse_transport(transport, units, p, j)
