import pytest

import norm_transfer as audit


def multiply(field, left, right):
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i+j] ^= field.multiply(a, b)
    return result


def evaluate(field, coefficients, value):
    result = 0
    for coefficient in reversed(coefficients):
        result = field.multiply(result, value) ^ coefficient
    return result


def test_fixed_native_counterexample():
    data = audit.certificate()
    assert data["N"] == 49 and data["K"] == 6
    assert [(row["degree"], row["multiplicity"]) for row in data["D_factors"]] == [(5, 1), (19, 1)]
    assert data["forced_Q_degree_lower_bound"] == 24
    assert data["code_Q_degree_budget"] == 21
    assert data["low_degree_U_budget"] == 24
    assert data["global_norm_ansatz_excluded"]


def test_explicit_rabin_irreducibility_certificates():
    data = audit.certificate()
    _, field, ring = audit.contexts(7, 131)
    x = ring.gen()
    for row in data["D_factors"]:
        factor = ring([audit.element(field, c, 7) for c in row["coefficients"]])
        degree = row["degree"]
        assert degree in (5, 19)  # Both prime, so there is one proper subfield check.
        assert x.pow_mod(128**degree, factor) == x % factor
        assert (x.pow_mod(128, factor) - x).gcd(factor) == 1


def test_independent_integer_polynomial_replay():
    data = audit.certificate()
    field = audit.NATIVE.BinaryField(data["bits"], data["modulus"])
    f = [1]
    for a in data["points"]:
        f = multiply(field, f, [a, 1])
    assert f == data["F_coefficients"]
    derivative = [f[j+1] if j % 2 == 0 else 0 for j in range(len(f)-1)]
    assert multiply(field, data["D_coefficients"], data["D_coefficients"]) == derivative
    product = [1]
    for row in data["D_factors"]:
        for _ in range(row["multiplicity"]):
            product = multiply(field, product, row["coefficients"])
    assert product == data["D_coefficients"]
    assert all(evaluate(field, product, a) != 0 for a in data["points"])


def test_same_input_is_satisfiable_not_a_hardness_certificate():
    witness = audit.same_input_witness()
    field = audit.NATIVE.BinaryField(7, 131)
    assert witness["trials"] == 44 and witness["field_draws"] == 3694
    assert audit.NATIVE.verify(field, audit.POINTS, witness["values"], 6, [1]*49, [0]*6)
    changed = witness["values"].copy()
    changed[0] = 0
    assert not audit.NATIVE.verify(field, audit.POINTS, changed, 6, [1]*49, [0]*6)


@pytest.mark.parametrize("multiplicity", [1, 2, 3, 4])
def test_full_odd_primary_power_is_forced_not_just_parity(multiplicity):
    _, _, ring = audit.contexts(3, 11)
    degree, rows = audit.odd_factor_carrier((ring.gen() + 1) ** multiplicity)
    assert degree == multiplicity
    assert rows[0]["forced_in_Q"]


@pytest.mark.parametrize("c_value", [1, 3, 5, 7])
def test_positive_norm_identity_and_nonprimitive_scaling(c_value):
    native, field, ring = audit.contexts(3, 11)
    assert native.trace(c_value) == 1
    c = audit.element(field, c_value, 3)
    x = ring.gen()
    u, v, k = x**4 + x + 1, x, (x + 1)**3
    norm = u*u + u*v + c*v*v
    assert u.gcd(v).degree() == 0
    d, q, lift = k*norm, k*v*v, k*u*v
    assert lift*lift + lift*q + c*q*q == d*q
    assert audit.odd_factor_carrier(norm)[0] == 0
    assert audit.odd_factor_carrier(d)[0] == 3
    assert q % ((x+1)**3) == 0
    for a in range(8):
        value = audit.element(field, a, 3)
        if q(value) != 0:
            ratio = d(value) / q(value)
            encoded = sum(int(bit) << j for j, bit in enumerate(ratio.to_list()))
            assert native.trace(encoded) == 1


def test_even_degree_factor_is_not_falsely_forced():
    _, _, ring = audit.contexts(3, 11)
    x = ring.gen()
    assert (x*x+x+1).is_irreducible()
    assert audit.odd_factor_carrier((x*x+x+1)**3)[0] == 0


def test_trace_one_assumption_cannot_be_removed():
    _, _, ring = audit.contexts(3, 11)
    x, q, c = ring.gen(), ring.one(), ring.zero()
    d = x*x+x
    assert x*x+x*q+c*q*q == d*q
    assert audit.odd_factor_carrier(d)[0] == 2 > q.degree()


def test_modulo_only_identity_can_escape_degree_guard():
    # At X=0,1 this holds, but it is NOT a rational-function identity.
    _, _, ring = audit.contexts(3, 11)
    x = ring.gen()
    f, q, lift = x*x+x, ring.one(), x
    d = ring.one()
    residual = lift*lift + lift*q + q*q - d*q
    assert residual == f and residual != 0 and residual % f == 0
    assert 2*lift.degree() >= f.degree()


@pytest.mark.parametrize("points", [audit.POINTS[:-1], (audit.POINTS[0],)*49])
def test_rejects_non_native_or_repeated_points(points):
    with pytest.raises(ValueError):
        audit.certificate(points)


def test_noncanonical_points_rejected():
    with pytest.raises(ValueError):
        audit.certificate((128,) + audit.POINTS[1:])


def test_zero_polynomial_rejected():
    _, _, ring = audit.contexts(3, 11)
    with pytest.raises(ValueError):
        audit.odd_factor_carrier(ring.zero())


def test_bounded_baseline_does_not_report_unfound_solution():
    with pytest.raises(RuntimeError, match="trial cap"):
        audit.same_input_witness(trial_cap=1)
