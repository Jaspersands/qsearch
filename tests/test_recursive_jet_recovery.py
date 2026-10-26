"""Oracle-access/recursion falsifiers; known-H callbacks are reference only."""
from fractions import Fraction
from itertools import product
from math import prod

import numpy as np
import pytest

from theorems.class_three_ambient_frontend import _subspace_contains, _subspace_intersection
from theorems.jet_oracle_homogenization import lie_bch
from theorems.jet_tuple_oracle_central_descent_audit import unrolled_tuple_oracle_arbitrary_h_solve
from theorems.recursive_jet_recovery import PublicLinearSection, recursion_call_envelope, whole_recovery_budget
from theorems.right_abelian_induced_source import upper_triangular_lie
from theorems.symbolic_scalar_phase_erasure import _fmpz_solve_coordinates
from theorems.ut5_matrix_phase_alignment import _identity


def test_nonhomomorphic_public_section_still_hides_exact_quotient():
    p = 5
    algebra, slots = upper_triangular_lie(3, p)
    x, z, y = _identity(3)
    section = PublicLinearSection(p, 3, (tuple(x), tuple(y)))
    alternate = PublicLinearSection(p, 3, (tuple(a+b for a, b in zip(x, z)), tuple(y)))
    # H=exp<X,Z>, K=exp<Z>; use the actual root coset predicate as f.
    hidden = algebra.span((x, z))
    def coset_label(v):
        return v[slots.index((1, 2))]
    points = tuple(product(range(p), repeat=2))
    for a, b in product(points, repeat=2):
        left, right = section.apply(a), section.apply(b)
        difference = lie_bch(algebra, tuple(-v % p for v in left), right, 2)
        assert (coset_label(left) == coset_label(right)) == _subspace_contains(hidden, (difference,), p)
        assert (coset_label(left) == coset_label(right)) == (a[1] == b[1])
        assert coset_label(left) == coset_label(alternate.apply(a))
    a, b = (1, 0), (0, 1)
    assert lie_bch(algebra, section.apply(a), section.apply(b), 2) != section.apply((1, 1))
    clean = np.array([[int(a[1] == b[1])/len(points) for b in points] for a in points])
    leaked = clean*np.eye(len(points))
    assert np.max(np.abs(leaked-np.eye(len(points))/len(points))) == 0
    assert np.linalg.matrix_rank(leaked) == len(points)
    assert np.linalg.matrix_rank(clean) == p


def test_quotient_without_kernel_containment_can_change_oracle_labels():
    # In matrix UT3 coordinates H=<X> has coset labels (y,z). K=<Z>
    # is NOT in H, so two representatives of one quotient element disagree.
    f = lambda xyz: (xyz[1], xyz[2])
    assert f((1, 2, 0)) != f((1, 2, 1))


def test_flattened_nested_sections_use_one_original_query_and_clear_workspace():
    p = 7
    root = PublicLinearSection(p, 4, ((1, 0, 1, 0), (0, 1, 2, 1), (0, 0, 1, 3)))
    inner = PublicLinearSection(p, 3, ((1, 2, 0), (0, 1, 4)))
    tiny = PublicLinearSection(p, 2, ((2, 3),))
    flat = tiny.then(inner).then(root)
    for q in product(range(p), repeat=1):
        expected = root.apply(inner.apply(tiny.apply(q)))
        assert flat.apply(q) == expected
        calls = []
        def oracle(v):
            calls.append(v)
            return sum((i+1)*a for i, a in enumerate(v)) % p
        label = flat.evaluate_fixture(oracle, q)
        assert calls == [expected]
        workspace = flat.apply(q)
        cleared = tuple((x-y) % p for x, y in zip(workspace, flat.apply(q)))
        assert cleared == (0,)*4
        assert label == sum((i+1)*a for i, a in enumerate(expected)) % p
    assert PublicLinearSection(p, 4, ()).apply(()) == (0,)*4
    with pytest.raises(ValueError, match="mismatch"):
        root.then(inner)
    with pytest.raises(ValueError, match="canonical"):
        inner.apply((p, 0))


def _lie_closure(algebra, generators):
    basis = algebra.span(generators)
    while True:
        enlarged = algebra.span(basis+[algebra.bracket(a, b) for a, b in product(basis, repeat=2)])
        if len(enlarged) == len(basis):
            return enlarged
        basis = enlarged


def _known_h_reference_callbacks(root, hidden):
    """These answer from the truth fixture, NOT from quantum measurements."""
    def pullback(alg, basis, lift):
        lifted = [lift(v) for v in basis]
        intersection = _subspace_intersection(hidden, lifted, root.dimension, root.p)
        result = []
        for value in intersection:
            coefficients = _fmpz_solve_coordinates(lifted, value, root.p)
            result.append(tuple(sum(a*v[j] for a, v in zip(coefficients, basis)) % root.p
                                for j in range(alg.dimension)))
        return alg.span(result)
    def image(alg, plan, lift):
        normal = list(plan.certificate.normal_basis)
        section = list(plan.certificate.section_basis)
        h = pullback(alg, list(plan.certificate.ambient_basis), lift)
        assert _subspace_intersection(h, normal, alg.dimension, alg.p) == []
        output = []
        for v in h:
            coefficients = _fmpz_solve_coordinates(normal+section, v, alg.p)[len(normal):]
            output.append(tuple(sum(a*w[j] for a, w in zip(coefficients, section)) % alg.p
                                for j in range(alg.dimension)))
        return alg.span(output)
    return pullback, image


@pytest.mark.parametrize("p", [7, 2**127-1])
def test_genuinely_nonabelian_hidden_subgroup_recovery_reference(p):
    algebra, slots = upper_triangular_lie(5, p)
    basis = _identity(len(slots))
    a = tuple(int(ij in ((0, 1), (2, 3))) for ij in slots)
    b = tuple(int(ij in ((1, 2), (3, 4))) for ij in slots)
    hidden = _lie_closure(algebra, (a, b))
    assert algebra.nilpotency_class(hidden) > 1 and len(hidden) > 2
    assert len(hidden) < len(basis)
    abelian, image = _known_h_reference_callbacks(algebra, hidden)
    result = unrolled_tuple_oracle_arbitrary_h_solve(algebra, basis,
        abelian_base_oracle=abelian, transverse_tuple_image_oracle=image)
    assert result.status == "SUCCESS"
    assert _subspace_contains(hidden, result.recovered_generators, p)
    assert _subspace_contains(result.recovered_generators, hidden, p)
    envelope = recursion_call_envelope(algebra.nilpotency_class(basis))
    assert result.rebuilt_tuple_oracle_calls <= envelope["image_calls"]
    assert result.abelian_base_calls <= envelope["abelian_calls"]
    assert all(row["class_after"] < row["class_before"] for row in result.rebuilt_chart_log)


def test_general_recursion_accepts_nonmetabelian_derived_ambient():
    algebra, _ = upper_triangular_lie(9, 11)
    basis = _identity(algebra.dimension)
    normal = algebra.lower_central_series(basis)[1]
    normal_prime = algebra.lower_central_series(normal)[1]
    assert algebra.lower_central_series(normal_prime)[1]
    abelian, image = _known_h_reference_callbacks(algebra, basis)
    result = unrolled_tuple_oracle_arbitrary_h_solve(algebra, basis,
        abelian_base_oracle=abelian, transverse_tuple_image_oracle=image)
    assert result.status == "SUCCESS"
    assert len(result.recovered_generators) == algebra.dimension
    assert result.rebuilt_tuple_oracle_calls == 0
    assert result.abelian_base_calls <= recursion_call_envelope(8)["abelian_calls"]


def test_public_guards_do_not_turn_an_incorrect_image_callback_into_a_decoder():
    algebra, slots = upper_triangular_lie(3, 5)
    basis = _identity(algebra.dimension)
    hidden = [basis[slots.index((0, 1))]]
    abelian, _ = _known_h_reference_callbacks(algebra, hidden)
    result = unrolled_tuple_oracle_arbitrary_h_solve(algebra, basis,
        abelian_base_oracle=abelian, transverse_tuple_image_oracle=lambda *args: [])
    assert result.status == "SUCCESS"  # structural guards alone cannot certify completeness
    assert result.recovered_generators == ()
    assert not _subspace_contains(result.recovered_generators, hidden, 5)


def test_all_class_recursion_count_closed_form_and_halving():
    for c in range(1, 129):
        bound = recursion_call_envelope(c)
        smaller = recursion_call_envelope(c//2)
        assert bound["image_calls"] == c-1+smaller["image_calls"]
        assert bound["abelian_calls"] == 1+smaller["abelian_calls"]
        assert bound["total_calls"] == 2*c-c.bit_count() < 2*c
        assert bound["abelian_calls"] == c.bit_length()
    assert recursion_call_envelope(9)["image_calls"] == 12
    assert recursion_call_envelope(9)["abelian_calls"] == 4


@pytest.mark.parametrize("n,c,p", [(1, 1, 2), (4, 2, 5), (6, 3, 7), (19, 9, 43), (19, 9, 2**127-1)])
def test_global_budget_covers_all_calls_and_complete_instruments(n, c, p):
    error = Fraction(1, 8)
    report = whole_recovery_budget(n, c, p, error)
    assert report["total_error_bound"] <= error
    assert report["rank_failure_bound"] <= error/3
    assert report["instrument_error_per_call"]*report["complete_instrument_calls"] == error/3
    if report["sde_calls"]:
        assert report["solver_abort_per_call"]*report["sde_calls"] == error/3
    else:
        assert report["original_queries"] == report["base_fourier_samples"]
    if c <= 3:
        count = report["image_fourier_samples"]
        exact = 1-prod(Fraction(p**count-p**i, p**count) for i in range(report["terminal_dimension_bound"]))
        assert exact*report["total_calls"] <= report["rank_failure_bound"]
    with pytest.raises(ValueError, match="class<p"):
        whole_recovery_budget(n, p, p)
