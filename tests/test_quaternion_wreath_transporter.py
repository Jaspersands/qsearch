"""Bounded exact controls for the swap-wreath transporter construction.

G is the 24 Hamilton Hurwitz units, H={+/-1,+/-i}, and a=(1+i+j+k)/2.
H is the norm-one unit group of O=Z+Zi+2Zj+2Zk, but is not normal in G.
The supplied finite labels are f_O(x)=Hx and f_I(y)=H*a*y. They are
explicit coset fixtures, not the parent's Gaussian/straddle preparations.

With (x,y,b)(u,v,c)=((x,y)*swap^b(u,v),b xor c), Phi prepares the two
supplied labels and swaps their OUTPUT order when b=1. Its fibres are
right cosets K*w, where K_even=H x a^-1*H*a and K_odd=H*a x a^-1*H.
Only a 24-by-24 multiplication table, bounded sets, and scalar Gram
controls are used. No native problem generation, transporter search,
growing-dimensional state, quantum backend, or receiver is implemented.
"""

from fractions import Fraction
from itertools import product


ONE, I, J, K = BASIS = tuple(
    tuple(Fraction(row == column) for row in range(4))
    for column in range(4)
)
A = (Fraction(1, 2),) * 4


def _scale(q, scalar):
    return tuple(scalar * value for value in q)


def _mul(q, r):
    a, b, c, d = q
    e, f, g, h = r
    return (
        a * e - b * f - c * g - d * h,
        a * f + b * e + c * h - d * g,
        a * g - b * h + c * e + d * f,
        a * h + b * g - c * f + d * e,
    )


def _conjugate(q):
    return (q[0],) + tuple(-value for value in q[1:])


def _norm(q):
    return sum(value * value for value in q)


def _in_order(q):
    return all((value / scale).denominator == 1
               for value, scale in zip(q, (1, 1, 2, 2)))


UNITS = tuple(sorted(
    {_scale(q, sign) for q in BASIS for sign in (-1, 1)}
    | {tuple(Fraction(sign, 2) for sign in signs)
       for signs in product((-1, 1), repeat=4)}
))
INDEX = {q: index for index, q in enumerate(UNITS)}
MUL = tuple(tuple(INDEX[_mul(q, r)] for r in UNITS) for q in UNITS)
INV = tuple(INDEX[_conjugate(q)] for q in UNITS)
IDENTITY, SHIFT = INDEX[ONE], INDEX[A]
H = frozenset(INDEX[_scale(q, sign)] for q in (ONE, I) for sign in (-1, 1))
EVEN = frozenset(
    (h, MUL[MUL[INV[SHIFT]][j]][SHIFT], 0) for h, j in product(H, repeat=2)
)
ODD = frozenset(
    (MUL[h][SHIFT], MUL[INV[SHIFT]][j], 1) for h, j in product(H, repeat=2)
)
HIDDEN = EVEN | ODD
W_IDENTITY = (IDENTITY, IDENTITY, 0)
SWAP_SHIFT = (SHIFT, INV[SHIFT], 1)


def _w_mul(w, v):
    x, y, b = w
    u, z, c = v
    if b:
        u, z = z, u
    return (MUL[x][u], MUL[y][z], b ^ c)


def _w_inverse(w):
    x, y, b = w
    return (INV[y], INV[x], b) if b else (INV[x], INV[y], b)


def _f_o(x):
    return frozenset(MUL[h][x] for h in H)


def _f_i(y):
    # Planted finite fixture; the dispatcher below receives no shift.
    return _f_o(MUL[SHIFT][y])


def _phi(w, f_o=_f_o, f_i=_f_i):
    x, y, b = w
    labels = (f_o(x), f_i(y))
    return labels[::-1] if b else labels


def _wrong_phi(w):
    x, y, b = w
    return (_f_i(x), _f_o(y)) if b else (_f_o(x), _f_i(y))


def test_exact_hurwitz_group_table_and_inverses():
    assert len(UNITS) == len(INDEX) == 24
    assert all(_norm(q) == 1 for q in UNITS)
    indices = set(range(24))
    for x in indices:
        assert set(MUL[x]) == indices
        assert MUL[x][IDENTITY] == MUL[IDENTITY][x] == x
        assert MUL[x][INV[x]] == MUL[INV[x]][x] == IDENTITY
    for x, y, z in product(range(24), repeat=3):
        assert MUL[MUL[x][y]][z] == MUL[x][MUL[y][z]]
    assert _mul(I, J) == K and _mul(J, I) == _scale(K, -1)


def test_order_has_exactly_the_nonnormal_c4_norm_one_units():
    order_basis = (ONE, I, _scale(J, 2), _scale(K, 2))
    assert all(_in_order(_mul(q, r)) for q, r in product(order_basis, repeat=2))
    assert all(_in_order(_conjugate(q)) for q in order_basis)
    # nrd(z0+z1*i+2*z2*j+2*z3*k)=z0^2+z1^2+4*z2^2+4*z3^2.
    # At norm one all coefficients have absolute value <=1, and z2=z3=0.
    bounded_order = (
        tuple(Fraction(z * scale) for z, scale in zip(coefficients, (1, 1, 2, 2)))
        for coefficients in product((-1, 0, 1), repeat=4)
    )
    units = {q for q in bounded_order if _norm(q) == 1}
    assert units == {UNITS[h] for h in H}
    assert H == frozenset(INDEX[q] for q in UNITS if _in_order(q))
    i = INDEX[I]
    assert {IDENTITY, i, MUL[i][i], MUL[MUL[i][i]][i]} == H
    assert MUL[MUL[MUL[i][i]][i]][i] == IDENTITY
    assert MUL[MUL[SHIFT][i]][INV[SHIFT]] == INDEX[J] not in H
    assert frozenset(MUL[MUL[SHIFT][h]][INV[SHIFT]] for h in H) != H


def test_wreath_subgroup_has_32_elements_and_is_closed():
    assert len(H) == 4
    assert len(EVEN) == len(ODD) == 16
    assert EVEN.isdisjoint(ODD)
    assert len(HIDDEN) == 2 * len(H)**2 == 32
    assert W_IDENTITY in HIDDEN
    assert _w_mul(SWAP_SHIFT, SWAP_SHIFT) == W_IDENTITY
    assert {_w_mul(e, SWAP_SHIFT) for e in EVEN} == ODD
    for w in HIDDEN:
        assert _w_inverse(w) in HIDDEN
        assert _w_mul(w, _w_inverse(w)) == W_IDENTITY
        assert _w_mul(_w_inverse(w), w) == W_IDENTITY
    for w, v in product(HIDDEN, repeat=2):
        assert _w_mul(w, v) in HIDDEN
    for h, j in product(H, repeat=2):
        e = (h, MUL[MUL[INV[SHIFT]][j]][SHIFT], 0)
        expected = (j, MUL[MUL[INV[SHIFT]][h]][SHIFT], 0)
        assert _w_mul(_w_mul(SWAP_SHIFT, e), SWAP_SHIFT) == expected


def test_callable_phi_queries_each_supplied_source_then_swaps_outputs():
    x, y = INDEX[I], INDEX[J]
    for b in (0, 1):
        calls = []

        def f_o(argument):
            calls.append(("O", argument))
            return ("O-label", argument)

        def f_i(argument):
            calls.append(("I", argument))
            return ("I-label", argument)

        expected = (("O-label", x), ("I-label", y))
        assert _phi((x, y, b), f_o, f_i) == (expected[::-1] if b else expected)
        assert calls == [("O", x), ("I", y)]
    for h, x in product(H, range(24)):
        assert _f_o(MUL[h][x]) == _f_o(x)
    for x in range(24):
        assert _f_i(x) == _f_o(MUL[SHIFT][x])


def test_phi_fibres_are_36_right_cosets_without_pairwise_wreath_comparison():
    remaining = set(product(range(24), range(24), (0, 1)))
    assert len(remaining) == 2 * 24**2 == 1152
    representatives = {}
    covered = 0
    # Exhaust the 36 explicit K*w sets, not all 1152^2 element pairs.
    while remaining:
        representative = min(remaining)
        coset = {_w_mul(k, representative) for k in HIDDEN}
        assert len(coset) == 32 and coset <= remaining
        label = _phi(representative)
        assert label not in representatives
        for w in coset:
            assert _phi(w) == label
            assert _w_mul(w, _w_inverse(representative)) in HIDDEN
        representatives[label] = representative
        covered += len(coset)
        remaining.difference_update(coset)
    base_labels = {_f_o(x) for x in range(24)}
    assert len(base_labels) == 6
    assert len(representatives) == 36 and covered == 1152
    assert set(representatives) == set(product(base_labels, repeat=2))


def test_left_invariance_is_not_right_invariance():
    w = (SHIFT, IDENTITY, 0)
    k = (INDEX[I], IDENTITY, 0)
    assert k in EVEN
    assert _phi(_w_mul(k, w)) == _phi(w)
    assert _phi(_w_mul(w, k)) != _phi(w)


def test_odd_first_coordinate_is_ha_but_second_need_not_be_its_inverse():
    ha = {MUL[h][SHIFT] for h in H}
    a_inverse_h = {MUL[INV[SHIFT]][h] for h in H}
    assert {x for x, _, _ in ODD} == ha
    assert {y for _, y, _ in ODD} == a_inverse_h
    assert ODD == frozenset((x, y, 1) for x, y in product(ha, a_inverse_h))
    witness = (SHIFT, MUL[INV[SHIFT]][INDEX[I]], 1)
    assert witness in ODD and witness[1] != INV[witness[0]]


def test_wrong_odd_branch_breaks_hidden_subgroup_invariance():
    assert SWAP_SHIFT in ODD
    assert _phi(SWAP_SHIFT) == _phi(W_IDENTITY)
    assert _wrong_phi(SWAP_SHIFT) != _wrong_phi(W_IDENTITY)


def test_inversion_is_an_antihomomorphism_not_the_required_automorphism():
    i, j = INDEX[I], INDEX[J]
    assert INV[MUL[i][j]] == MUL[INV[j]][INV[i]] == INDEX[_scale(K, -1)]
    assert MUL[INV[i]][INV[j]] == INDEX[K]
    assert INV[MUL[i][j]] != MUL[INV[i]][INV[j]]


def _positive_label_overlap(left, right):
    # Finite Gram control (3/5)|common>+(4/5)|label>, not Gaussian source states.
    return Fraction(1) if left == right else Fraction(9, 25)


def test_one_separated_factor_gives_exponent_t_not_two_t():
    common, unique = Fraction(3, 5), Fraction(4, 5)
    kappa = common**2
    assert common**2 + unique**2 == 1
    # The six-label Gram matrix has eigenvalues 1-kappa and 1+5*kappa.
    assert 1 - kappa > 0 and 1 + 5 * kappa > 0
    left = _phi(W_IDENTITY)
    right = _phi((SHIFT, IDENTITY, 0))
    assert left[0] != right[0] and left[1] == right[1]
    overlap = (_positive_label_overlap(left[0], right[0])
               * _positive_label_overlap(left[1], right[1]))
    for copies in (1, 2, 5):
        assert overlap**copies == kappa**copies > kappa**(2 * copies)


def test_nonorthogonal_labels_do_not_produce_the_ideal_hsp_partial_trace():
    left = _phi(W_IDENTITY)
    right = _phi((SHIFT, IDENTITY, 0))
    overlap = (_positive_label_overlap(left[0], right[0])
               * _positive_label_overlap(left[1], right[1]))
    copies, half = 3, Fraction(1, 2)
    off_diagonal = half * overlap**copies
    # Trace labels out of (|w>|Phi(w)>^t+|v>|Phi(v)>^t)/sqrt(2).
    rho = ((half, off_diagonal), (off_diagonal, half))
    ideal = ((half, Fraction(0)), (Fraction(0), half))
    assert left != right and 0 < off_diagonal < half
    assert rho != ideal and rho[0][0] + rho[1][1] == 1
    assert rho[0][0] * rho[1][1] - rho[0][1] * rho[1][0] > 0
    plus_probability = sum(sum(row) for row in rho) / 2
    assert plus_probability - half == off_diagonal > 0
