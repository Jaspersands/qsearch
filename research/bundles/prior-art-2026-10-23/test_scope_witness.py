import pytest

from scope_witness import (
    block_support,
    evidence,
    group_commutator,
    group_inverse,
    group_product,
    in_h_span,
    lie_bracket,
    series_dimensions,
    symbolic_witnesses,
    unit,
)


@pytest.mark.parametrize("m", [1, 2, 3, 5, 8])
def test_block_lower_and_derived_series(m):
    result = series_dimensions(m)
    assert result["lower_central"] == [10*m*m, 6*m*m, 3*m*m, m*m, 0]
    assert result["derived"] == [10*m*m, 6*m*m, m*m, 0]


def test_exact_group_class_and_derived_obstructions():
    witnesses = symbolic_witnesses()
    assert witnesses["class_four_commutator"] == unit(0, 4)
    assert witnesses["derived_noncommuting_commutator"] == unit(0, 4)


def test_cyclic_subgroups_do_not_permute():
    witnesses = symbolic_witnesses()
    assert witnesses["AB_product"] == {(0, 1): 1, (1, 2): 1, (0, 2): 1}
    assert witnesses["BA_product"] == {(0, 1): 1, (1, 2): 1}
    # Matching the (0,1) and (1,2) entries forces both exponents to one.
    # Every element of BA has a zero (0,2) entry, unlike this element of AB.


def test_hidden_subalgebra_is_closed_but_not_normal_or_graded():
    witnesses = symbolic_witnesses()
    basis = witnesses["subalgebra_basis"]
    for a in basis:
        for b in basis:
            assert in_h_span(lie_bracket(a, b))
    assert witnesses["subalgebra_nonzero_bracket"] == unit(0, 4)
    assert witnesses["normality_obstruction"] == unit(1, 4)
    assert not in_h_span(witnesses["normality_obstruction"])
    assert not in_h_span(witnesses["degree_two_projection"])


def test_inverse_and_commutator_controls_are_not_abelianized():
    x, y = unit(0, 1), unit(1, 2)
    a = group_product(x, y)
    assert group_product(a, group_inverse(a)) == {}
    assert group_product(group_inverse(a), a) == {}
    assert group_inverse(a) != {key: -value for key, value in a.items()}
    assert group_commutator(x, y) == unit(0, 2)
    assert group_commutator(y, x) == {(0, 2): -1}


@pytest.mark.parametrize("p", [5, 7, 43, 2**127-1])
def test_nonzero_witness_survives_prime_reduction(p):
    witnesses = symbolic_witnesses()
    for key in ("class_four_commutator", "derived_noncommuting_commutator", "normality_obstruction"):
        assert any(value % p != 0 for value in witnesses[key].values())


@pytest.mark.parametrize("m", [0, -1, 9, 1.5, True])
def test_control_budget_is_explicit(m):
    with pytest.raises(ValueError):
        block_support(m)


def test_no_novelty_or_algorithm_admission_from_structure():
    record = evidence()
    for flag in (
        "novelty_certified", "natural_hard_source_found",
        "quantum_algorithm_executed", "speedup_admitted",
    ):
        assert record[flag] is False
    assert "A reduction to known algorithms" in record["does_not_exclude"]
