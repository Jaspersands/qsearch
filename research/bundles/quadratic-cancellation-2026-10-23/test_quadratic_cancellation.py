from fractions import Fraction
import random

import pytest

import quadratic_cancellation as quadratic
from scalar_cancellation import SmoothPowerRoots, TrialBudgetExceeded


def matrix_with_rank(prime, rank, width, seed=61):
    rng = random.Random(seed)
    return tuple(tuple(int(j == i) if j < rank else rng.randrange(prime)
                       for j in range(width)) for i in range(rank))


def check_original(matrix, witness):
    assert len(witness.weights) == len(matrix[0])
    assert any(witness.weights)
    for row in matrix:
        assert sum(a*x*x for a, x in zip(row, witness.weights)) % witness.prime == 0
    assert all(type(x) is int and 0 <= x < witness.prime for x in witness.weights)
    assert witness.acquired_columns == len(matrix[0])
    assert witness.required_public_bank == (witness.public_rank_cap + 1)**2
    assert Fraction(witness.conditional_abort_bound) <= Fraction(1, 2**40)


PRIMES = [3, 5, 7, 13, 43, 257, 263, 2**64-2**32+1,
          2**127-295, 2**127-39, 2**127-1]


@pytest.mark.parametrize("prime", PRIMES)
@pytest.mark.parametrize("rank", [1, 2, 4, 8, 16])
def test_full_rank_controls(prime, rank):
    matrix = matrix_with_rank(prime, rank, quadratic.quadratic_arity(rank))
    witness = quadratic.quadratic_witness(matrix, prime, rank,
                                          rng=random.Random(415), security_bits=40)
    check_original(matrix, witness)
    assert witness.observed_rank == rank
    assert witness.linear_dependences_checked <= rank + 2
    assert witness.root_counters["generator_draws"] <= 41
    assert witness.root_counters["root_calls"] <= (rank+1)**2 + rank+1


def test_zero_rank_and_unused_columns_still_paid():
    matrix = ((0,)*12, (0,)*12)
    witness = quadratic.quadratic_witness(matrix, 7, 2, security_bits=40)
    check_original(matrix, witness)
    assert witness.method == "zero_rank"
    assert witness.weights == (1,) + (0,)*11
    assert witness.conditional_abort_bound == "0"
    assert witness.root_counters["root_calls"] == 0


def test_rank_compression_lifts_to_redundant_original_rows():
    base = matrix_with_rank(43, 2, 16)
    matrix = base + (tuple((3*a + 8*b) % 43 for a, b in zip(*base)), (0,)*16)
    witness = quadratic.quadratic_witness(matrix, 43, 3,
                                          rng=random.Random(8), security_bits=40)
    check_original(matrix, witness)
    assert witness.observed_rank == 2
    assert witness.used_prefix_columns == 9
    assert witness.weights[9:] == (0,)*7
    assert witness.acquired_columns == witness.required_public_bank == 16


@pytest.mark.parametrize("prime", PRIMES)
def test_four_nonempty_cells_and_scalar_solver(prime):
    zeta = SmoothPowerRoots(prime, 2, rng=random.Random(81), attempt_cap=41).generator
    matrix = ((1, -zeta % prime, -zeta % prime, zeta*zeta % prime),)
    witness = quadratic.quadratic_witness(matrix, prime, 1,
                                          rng=random.Random(81), security_bits=40)
    check_original(matrix, witness)
    assert witness.method == "four_cell_scalar"
    assert witness.four_cell_identities_checked
    assert witness.completed_first_level_groups == 2
    assert witness.linear_dependences_checked == 3
    assert witness.scalar_report["counters"]["scalar_calls"] == 1
    if prime > 256:
        assert witness.scalar_report["counters"]["small_field_elements"] == 0
        assert witness.scalar_report["counters"]["large_field_solves"] == 1


def test_first_level_early_exit():
    witness = quadratic.quadratic_witness(((1, 4, 1, 4),), 5, 1,
                                          rng=random.Random(7), security_bits=40)
    check_original(((1, 4, 1, 4),), witness)
    assert witness.method == "first_level_zero_cell"
    assert witness.scalar_report is None


def test_second_level_empty_class_exit():
    # Over F_3 each pair has mixed coefficient classes; its first cell is
    # respectively 1 and -1. The second-level relation has only square entries.
    matrix = ((1, 1, 2, 2),)
    witness = quadratic.quadratic_witness(matrix, 3, 1,
                                          rng=random.Random(7), security_bits=40)
    check_original(matrix, witness)
    assert witness.method == "second_level_zero_cell"
    assert witness.four_cell_identities_checked
    assert witness.scalar_report is None


def test_exhaustive_scalar_equation_controls_over_f3():
    from itertools import product
    for values in product(range(3), repeat=4):
        witness = quadratic.quadratic_witness((values,), 3, 1,
                                              rng=random.Random(3), security_bits=40)
        check_original((values,), witness)


def test_ordinary_dependence_is_not_accepted_as_quadratic():
    rows = ((1, 1),)
    ordinary = quadratic.linear_relation(rows, 3)
    assert sum(a*x for a, x in zip(rows[0], ordinary)) % 3 == 0
    assert sum(a*x*x for a, x in zip(rows[0], ordinary)) % 3 != 0


@pytest.mark.parametrize("prime", [2, 9, 1, True])
def test_bad_field(prime):
    with pytest.raises(ValueError, match="odd prime"):
        quadratic.quadratic_witness(((0,),), prime, 0)


@pytest.mark.parametrize("rank_cap", [-1, True, 1.5])
def test_bad_rank_cap(rank_cap):
    with pytest.raises(ValueError, match="rank cap"):
        quadratic.quadratic_witness(((0,),), 3, rank_cap)


@pytest.mark.parametrize("matrix", [(), ((),), ((1,), (1, 2)), ((3,),), ((True,),)])
def test_bad_matrix(matrix):
    with pytest.raises(ValueError):
        quadratic.quadratic_witness(matrix, 3, 0)


def test_public_bank_not_replaced_by_postselection_on_rank():
    with pytest.raises(ValueError, match="preallocated"):
        quadratic.quadratic_witness(((0,)*8,), 3, 2)
    with pytest.raises(ValueError, match="rank exceeds"):
        quadratic.quadratic_witness(((1,),), 3, 0)


def test_independent_columns_are_not_given_a_false_relation():
    with pytest.raises(ValueError, match="linearly dependent"):
        quadratic.linear_relation(((1, 0), (0, 1)), 7)


class ConstantRng:
    def __init__(self, value):
        self.value = value
        self.calls = 0

    def randrange(self, start, stop):
        self.calls += 1
        return self.value


def test_nonsquare_cap_is_enforced():
    rng = ConstantRng(1)
    with pytest.raises(TrialBudgetExceeded, match="generator cap"):
        quadratic.quadratic_witness(((1,)*4,), 7, 1, rng=rng, security_bits=3)
    assert rng.calls == 4


def test_bad_rng_is_not_silently_reduced():
    with pytest.raises(ValueError, match="noncanonical"):
        quadratic.quadratic_witness(((1,)*4,), 7, 1, rng=ConstantRng(7))


def test_scalar_curve_cap_is_enforced():
    class FailedCurveRng:
        def randrange(self, start, stop):
            return stop-1 if start == 1 else 0

    with pytest.raises(TrialBudgetExceeded, match="curve trial cap"):
        quadratic.quadratic_witness(((1,)*4,), 263, 1,
                                    rng=FailedCurveRng(), security_bits=3)


def test_wrong_square_root_is_rejected(monkeypatch):
    monkeypatch.setattr(SmoothPowerRoots, "root", lambda self, value: 0)
    with pytest.raises(ArithmeticError, match="verified square root"):
        quadratic.quadratic_witness(((1,)*4,), 3, 1, rng=random.Random(81))


def test_wrong_scalar_witness_is_rejected(monkeypatch):
    monkeypatch.setattr(quadratic.ScalarBackend, "__call__", lambda *args: (1, 0, 0))
    with pytest.raises(ArithmeticError, match="moment did not vanish"):
        quadratic.quadratic_witness(((1,)*4,), 3, 1, rng=random.Random(81))


def test_zero_scalar_witness_is_rejected(monkeypatch):
    monkeypatch.setattr(quadratic.ScalarBackend, "__call__", lambda *args: (0, 0, 0))
    with pytest.raises(ArithmeticError, match="nonzero scalar"):
        quadratic.quadratic_witness(((1,)*4,), 3, 1, rng=random.Random(81))


def test_original_equations_checked_even_if_rank_compression_lies(monkeypatch):
    monkeypatch.setattr(quadratic, "row_basis", lambda *args: ())
    with pytest.raises(ArithmeticError, match="original quadratic moment"):
        quadratic.quadratic_witness(((1,)*4,), 3, 1)


def test_inputs_are_not_mutated_or_replaced():
    matrix = [list(row) for row in matrix_with_rank(13, 2, 9)]
    before = [row[:] for row in matrix]
    quadratic.quadratic_witness(matrix, 13, 2, rng=random.Random(8))
    assert matrix == before


@pytest.mark.parametrize("bits", [0, -1, True, 2.5])
def test_invalid_security_budget(bits):
    with pytest.raises(ValueError, match="security bits"):
        quadratic.quadratic_witness(((0,),), 3, 0, security_bits=bits)


def test_arity_is_not_advertised_as_always_smaller_than_scalar_recursion():
    assert quadratic.quadratic_arity(1) == 4 > 3**1
    assert quadratic.quadratic_arity(2) == 3**2
    assert quadratic.quadratic_arity(16) == 289 < 3**16
