"""Exact controls for source advice and wrong-maximal-order false positives."""

import pytest
from sympy import Matrix, eye, zeros

from native_realization import change_coordinates, fixture, opposite_queries, rebase_order
from additive_source import (
    adjoint, candidate_lattice, construct, fixes_inclusions, input_index,
    multiply, norm, scalar_matrix, shear,
)
from kernel_output import integer_matrix


@pytest.mark.parametrize("q,direction", [(3, 0), (5, 1), (17, 2)])
def test_source_construction_uses_suborder_table_without_target_order(q, direction):
    f = fixture(q, direction)
    for query in opposite_queries(f):
        beta = query["beta_in_r"]
        assert all(0 <= x < f["index"] for x in beta)
        result = query["construction"]
        z = result["polarization"]
        assert z.integral
        assert multiply(f["suborder"], z, z)-z.scale(result["trace"]) == scalar_matrix(f["suborder"], eye(16)).scale(-1)
        ambient = construct(f["source"], f["r_basis"]*beta, f["index"], query["roots"])
        assert change_coordinates(z, f["r_basis"]) == ambient["polarization"]
        assert ambient["trace"] == result["trace"]


@pytest.mark.parametrize("q,direction", [(3, 0), (5, 1), (17, 2)])
def test_native_translation_is_fractional_in_wrong_abstract_maximal_order(q, direction):
    f = fixture(q, direction)
    positive, negative = opposite_queries(f)
    for query, native_integral in ((positive, True), (negative, False)):
        gamma = query["gamma_in_source"]
        w_source = shear(f["source"], gamma)
        w_target = change_coordinates(w_source, f["target_basis"].inv())
        assert w_target.integral == native_integral
        assert w_source.integral != native_integral
        # The rational congruence holds in BOTH cases. Only the native lattice
        # distinguishes an allowed polarized isomorphism from a false positive.
        z0 = construct(f["source"], zeros(4, 1), f["index"], query["roots"])["polarization"]
        z1 = change_coordinates(query["construction"]["polarization"], f["r_basis"])
        assert multiply(f["source"], multiply(f["source"], adjoint(f["source"], w_source), z0), w_source) == z1
        assert fixes_inclusions(f["source"], w_source)


@pytest.mark.parametrize("q", [3, 5, 17])
def test_wrong_maximal_order_passes_all_algebraic_output_gates(q):
    f = fixture(q)
    d, r, b = f["index"], f["r_basis"], f["target_basis"]
    accepted = []
    for ambient_basis in (eye(4), b):
        h_generators = integer_matrix(d*r.inv()*ambient_basis)
        candidate = candidate_lattice([h_generators[:, i] for i in range(4)], d)
        actual_basis = r*candidate
        # The candidate is a ring, contains 1, is involution-stable, and has
        # the MAXIMAL discriminant and integral norms, in either case.
        algebra = rebase_order(f["source"], actual_basis)
        assert input_index(algebra, 11) == 1
        assert all(norm(algebra, eye(4)[:, i]).is_Integer for i in range(4))
        accepted.append(all(x.q == 1 for x in b.inv()*actual_basis))
    assert accepted == [False, True]


def test_lattice_rebase_does_not_round_nonintegral_products():
    f = fixture(3)
    with pytest.raises(ValueError, match="nonintegral"):
        rebase_order(f["source"], Matrix.diag(1, 1, 1, Matrix([[1]])[0]/2))


@pytest.mark.parametrize("q", [3, 5])
def test_identical_input_algebra_can_have_different_native_maximal_completions(q):
    cases = [fixture(q, t) for t in list(range(q))+[None]]
    reference = cases[0]["suborder"]
    assert len({tuple(f["target_basis"]) for f in cases}) == q+1
    for f in cases:
        assert f["suborder"].products == reference.products
        assert f["suborder"].involution == reference.involution
        assert f["suborder"].traces == reference.traces
        assert f["index"] == q**3
        assert input_index(f["target"], 11) == 1


def test_receipt_does_not_claim_native_geometry_or_a_quantum_result():
    from replay_realization import receipt
    result = receipt()
    assert result["execution_scope"]["exact_supplied_order_and_suborder_source_arithmetic"] is True
    assert all(value is False for key, value in result["execution_scope"].items()
               if key != "exact_supplied_order_and_suborder_source_arithmetic")
