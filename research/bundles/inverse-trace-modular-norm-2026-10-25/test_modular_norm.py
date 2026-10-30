from fractions import Fraction
import json

import pytest

import modular_norm as m


@pytest.fixture(scope="module")
def native():
    return m.NativeInstance(7, 131, m.OLD.POINTS)


@pytest.fixture(scope="module")
def known():
    # Replay already paid evidence, not a new search or planted native input.
    return json.loads((m.OLD.ROOT / "receipt.json").read_text())["same_input_witness"]["values"]


@pytest.fixture(scope="module")
def carry(native, known):
    return native.carry_from_witness(known)


@pytest.fixture(scope="module")
def small():
    return m.NativeInstance(5, 37, tuple(range(25)))


def test_full_native_round_trip(native, known, carry):
    assert native.verify_word(known)
    assert native.word_from_Q(carry["Q"]) == tuple(known)
    A, Q, W = (carry[key] for key in ("A", "Q", "W"))
    assert A*A + A*Q + Q*Q == native.D**2 + native.F*W
    assert carry["carry_was_derived_from_known_witness"] is True


def test_full_code_not_low_degree_square_ansatz(native, carry):
    assert {key: carry[key].degree() for key in ("P", "Q", "A", "W")} == {
        "P": 42, "Q": 48, "A": 48, "W": 47}
    assert sum(carry["P"][j] != 0 for j in range(1, 43, 2)) == 21
    assert carry["P"].derivative() != 0
    assert carry["Q"]**2 != carry["P"]
    assert carry["Q"]**2 % native.F == carry["P"]


def test_solver_recovers_native_witness_from_extra_carry(native, carry):
    result = m.fixed_carry(native, carry["W"])
    assert result["status"] == "VERIFIED_NATIVE_WITNESS_FOR_SUPPLIED_CARRY"
    assert native.verify_word(result["witness"])
    assert result["orientation_count"] == 32
    assert sum(result["unit_kernel_ranks"]) == result["orientations_checked"]
    assert not result["native_carry_acquisition_implemented"]
    assert not result["quantum_advantage"]
    assert not result["field_units_enumerated"]


def test_cap_is_unknown_not_negative(native, carry):
    result = m.fixed_carry(native, carry["W"], orientation_cap=1)
    assert result["status"] == "UNKNOWN_ORIENTATION_CAP"
    assert result["reason"] == "NO_NEGATIVE_RESULT"
    assert result["orientations_checked"] == result["unit_trials"] == 0
    assert result["witness"] is None


@pytest.mark.parametrize("cap", [0, -1, 1.5, True])
def test_invalid_orientation_caps(native, cap):
    with pytest.raises(ValueError):
        m.fixed_carry(native, native.ring.zero(), cap)


def test_zero_carry_is_only_a_restricted_negative(native, known):
    result = m.fixed_carry(native, native.ring.zero())
    assert result["status"] == "NO_SOLUTION_FOR_THIS_CARRY"
    assert result["orientation_count"] == result["orientations_checked"] == 1
    assert native.verify_word(known)  # Same native instance is satisfiable.


def test_public_linear_carry_all_orientations_excluded(native):
    result = m.fixed_carry(native, native.ring.gen())
    assert result["orientation_count"] == result["orientations_checked"] == 4
    assert result["unit_kernel_ranks"] == [0, 0, 4]
    assert result["status"] == "NO_SOLUTION_FOR_THIS_CARRY"


def test_odd_degree_norm_is_impossible(native):
    result = m.fixed_carry(native, native.ring.one())
    assert result["reason"] == "ODD_NORM_DEGREE"
    assert result["orientations_checked"] == 0


def test_odd_inert_factor_is_impossible(native):
    x = native.ring.gen()
    result = m.fixed_carry(native, x**3 + x)
    assert result["reason"] == "INERT_FACTOR_ODD_MULTIPLICITY"
    assert result["inert_degree"] % 2 == 1


def test_carry_domain_guard(native):
    with pytest.raises(ValueError):
        m.fixed_carry(native, native.ring.gen()**(native.N-1))


def test_zero_entry_and_noncanonical_words_rejected(native, known):
    for value in (0, -1, 128, True):
        changed = list(known)
        changed[0] = value
        assert not native.verify_word(changed)
        with pytest.raises(ValueError):
            native.carry_from_witness(changed)
    assert not native.verify_word(known[:-1])
    assert native.word_from_Q(native.ring.zero()) is None


@pytest.mark.parametrize("bits", [3, 4, 6, True, 5.5])
def test_wrong_reduction_domain(bits):
    with pytest.raises(ValueError):
        m.NativeInstance(bits, 37, tuple(range(25)))


@pytest.mark.parametrize("points", [tuple(range(24)), (0,)*25, tuple(range(24))+(32,)])
def test_wrong_native_points(points):
    with pytest.raises(ValueError):
        m.NativeInstance(5, 37, points)


def test_interpolation_and_input_length_guard(small):
    x = small.ring.gen()
    polynomial = x**24 + x**13 + small.element(7)*x + 1
    assert small.interpolate([polynomial(a) for a in small.elements]) == polynomial
    with pytest.raises(ValueError):
        small.interpolate([small.field.one()])


def test_embedding_descent_and_all_base_products(small):
    ext = m.QuadraticExtension(small)
    for a in range(32):
        x = small.element(a)
        assert ext.descend(ext.embed(x)) == x
        for b in range(32):
            y = small.element(b)
            assert ext.embed(x*y) == ext.embed(x)*ext.embed(y)
            assert ext.embed(x+y) == ext.embed(x)+ext.embed(y)
    with pytest.raises(ValueError):
        ext.descend(ext.theta)


def test_conjugation_split_and_norm(small):
    ext = m.QuadraticExtension(small)
    x = small.ring.gen()
    A, Q = x**19 + small.element(19)*x + 1, x**23 + small.element(7)
    B = ext.embed_poly(A) + ext.embed_poly(Q)*ext.theta
    assert ext.split(B) == (A, Q)
    assert ext.conjugate(ext.conjugate(B)) == B
    assert B*ext.conjugate(B) == ext.embed_poly(A*A+A*Q+Q*Q)


@pytest.mark.parametrize("rank", [0, 1, 2])
def test_unit_kernel_matches_exhaustive_norm_conic(small, rank):
    # Algebraic controls for the scalar subroutine, not new oracle problems.
    x, one = small.ring.gen(), small.ring.one()
    A, Q = [(one, x), (one, x**11), (x**11, x**12)][rank]
    actual_rank, units = m.normalized_units(small, A, Q)
    assert actual_rank == rank
    legal = []
    all_units = []
    for a in range(32):
        for b in range(32):
            r, s = small.element(a), small.element(b)
            if r*r+r*s+s*s != 1:
                continue
            all_units.append((r, s))
            if ((r*A+s*Q)**2 % small.F).degree() < small.N-small.K:
                legal.append((r, s))
    assert len(all_units) == 33
    if rank == 0:
        assert len(legal) == 33
        assert len(units) == small.N+1
        assert len({(m.encoded_element(r), m.encoded_element(s)) for r, s in units}) == len(units)
        assert all(unit in legal for unit in units)
        assert any(all((r*A+s*Q)(a) != 0 for a in small.elements) for r, s in units)
    else:
        assert len(units) == len(legal) == (1 if rank == 1 else 0)
        assert all(unit in legal for unit in units)
    for r, s in units:
        Ap, Qp = (s+r)*A+r*Q, r*A+s*Q
        assert Ap*Ap+Ap*Qp+Qp*Qp == A*A+A*Q+Q*Q


def test_rank_zero_hitting_set_handles_shared_zero_of_one_component(small):
    # At most N forbidden projective directions, one norm-one point each.
    one, x = small.ring.one(), small.ring.gen()
    _, units = m.normalized_units(small, one, x)
    bad = []
    for r, s in units:
        bad.append(any((r+s*x)(a) == 0 for a in small.elements))
    assert sum(bad) <= small.N
    assert not all(bad)


def test_complementary_lifts_same_carry_and_other_lifts_differ(native, carry):
    A, Q, W = carry["A"], carry["Q"], carry["W"]
    deltas = []
    for index in range(native.N):
        values = [native.field.zero()]*native.N
        values[index] = Q(native.elements[index])
        deltas.append(native.interpolate(values))
    seen = {tuple(m.OLD.encoded(W))}
    for delta in deltas:
        assert delta not in (native.ring.zero(), Q)
        change, remainder = divmod(delta*(delta+Q), native.F)
        assert remainder == 0 and change != 0
        other = W+change
        complement = A+delta+Q
        assert complement**2+complement*Q+Q**2 == native.D**2+native.F*other
        seen.add(tuple(m.OLD.encoded(other)))
    assert len(seen) == native.N+1
    assert (A+Q)**2+(A+Q)*Q+Q**2 == native.D**2+native.F*W


@pytest.mark.parametrize("bits,exponent", [(5, 8), (7, 30), (17, 560), (31, 3570)])
def test_exact_uniform_carry_counting_bound(bits, exponent):
    data = m.uniform_carry_bound(bits, trials=1000)
    ratio = Fraction(data["witness_count_upper_bound"]*data["distinct_carries_per_witness"],
                     data["carry_space_size"])
    assert ratio == data["one_draw_upper_bound"] == Fraction(1, 1 << exponent)
    assert data["inverse_success_bound_log2"] == exponent
    assert data["any_success_upper_bound"] == min(1, 1000*ratio)
    assert not data["native_hardness_established"]


@pytest.mark.parametrize("trials", [-1, 1.0, True])
def test_uniform_bound_rejects_wrong_trials(trials):
    with pytest.raises(ValueError):
        m.uniform_carry_bound(7, trials)


def test_zero_uniform_draws():
    assert m.uniform_carry_bound(7, 0)["any_success_upper_bound"] == 0
