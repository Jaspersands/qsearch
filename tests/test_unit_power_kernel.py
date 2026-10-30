"""Independent unit-projective enumeration and bounded fixed-bank controls."""
from fractions import Fraction
from itertools import product
import random

import pytest

from theorems import random_column_power_sde as solver
from theorems.bounded_power_roots import BoundedPowerRoot


class ScriptedBits:
    def __init__(self, prefix=(), tail=0):
        self.prefix = iter(prefix)
        self.tail = tail
        self.calls = 0

    def getrandbits(self, width):
        self.calls += 1
        return next(self.prefix, (1 << width)-1 if self.tail == "ones" else self.tail)


class PrefixedRandom:
    def __init__(self, prefix, seed=19):
        self.prefix = iter(prefix)
        self.rng = random.Random(seed)

    def getrandbits(self, width):
        value = next(self.prefix, None)
        return self.rng.getrandbits(width) if value is None else value


def rank(rows, p):
    matrix = [list(row) for row in rows]
    pivot = 0
    for col in range(len(matrix[0]) if matrix else 0):
        found = next((j for j in range(pivot, len(matrix)) if matrix[j][col] % p), None)
        if found is None:
            continue
        matrix[pivot], matrix[found] = matrix[found], matrix[pivot]
        inverse = pow(matrix[pivot][col], -1, p)
        matrix[pivot] = [x*inverse % p for x in matrix[pivot]]
        for j in range(pivot+1, len(matrix)):
            scale = matrix[j][col]
            matrix[j] = [(x-scale*y) % p for x, y in zip(matrix[j], matrix[pivot])]
        pivot += 1
    return pivot


def killed(rows, vector, p):
    return all(sum(x*y for x, y in zip(row, vector)) % p == 0 for row in rows)


def assert_counts(result):
    budget = result["budget"]
    for count, cap in (("attempts", "attempt_cap"), ("root_calls", "root_call_cap"),
                       ("uniform_calls", "uniform_call_cap"),
                       ("kernel_uniform_calls", "kernel_uniform_call_cap"),
                       ("root_uniform_calls", "root_uniform_call_cap"),
                       ("root_split_trials", "root_split_trial_cap"),
                       ("bit_draws", "bit_draw_cap"), ("random_bits", "random_bit_cap")):
        assert 0 <= result[count] <= budget[cap]
    assert result["uniform_calls"] == result["kernel_uniform_calls"]+result["root_uniform_calls"]
    assert result["random_bits"] == result["bit_draws"]*(result["p"]-1).bit_length()
    rejections = sum(result[key] for key in (
        "zero_rejections", "zero_coordinate_rejections", "nonpower_rejections"))
    assert rejections <= result["completed_kernel_draws"] <= result["attempts"]
    if result["reason"] == "ATTEMPT_CAP":
        assert rejections == result["completed_kernel_draws"] == result["attempts"]
    if result["reason"] == "EXACT_POWER_KERNEL":
        assert rejections+1 == result["completed_kernel_draws"] == result["attempts"]
    assert budget["auxiliary_abort_upper"] <= Fraction(1, 2**budget["failure_bits"])
    assert not budget["attempt_exhaustion_included"]
    assert result["require_nonzero"] is True
    for key in ("iid_uniform_columns_verified", "iid_fair_bits_verified",
                "supplied_prime_verified_by_this_api", "prime_validation_locally_clocked",
                "quantum_receiver_implemented", "hsp_claim", "speedup_claim",
                "input_labels_resampled", "field_enumeration_used"):
        assert result[key] is False
    assert result["arbitrary_fixed_bank_success_bound"] is None


def assert_unit_witness(result):
    assert result["status"] == "VERIFIED" and result["exact_verified"]
    p, d = result["p"], result["d"]
    weights, vector = result["weights"], result["power_vector"]
    assert len(weights) == len(result["columns"])
    assert all(type(x) is int and 0 < x < p for x in weights+vector)
    assert tuple(pow(x, d, p) for x in weights) == vector
    assert killed(zip(*result["columns"]), vector, p)
    assert_counts(result)


def assert_abort(result, reason):
    assert result["status"] == "ABORT" and result["reason"] == reason
    assert result["weights"] is result["power_vector"] is None
    assert result["exact_verified"] is False
    assert_counts(result)


@pytest.mark.parametrize("p,d,a,width", [(3, 1, 2, 3), (3, 2, 1, 3), (5, 2, 1, 3),
                                      (3, 2, 0, 2), (2, 1, 1, 2)])
def test_independent_projective_moments_and_good_density(p, d, a, width):
    powers = {pow(x, d, p) for x in range(1, p)}
    vectors = list(product(sorted(powers), repeat=width))
    classes = {tuple(x*pow(v[0], -1, p) % p for x in v) for v in vectors}
    bounds = solver.unit_projective_bank_bounds(p, d, a, width)
    assert bounds["h"] == len(powers)
    assert bounds["S"] == len(vectors) == len(powers)*len(classes)
    assert bounds["D"] == len(classes)
    first = second = factorial_second = bad = total = good_count = 0
    for entries in product(range(p), repeat=a*width):
        rows = [entries[i*width:(i+1)*width] for i in range(a)]
        count = sum(killed(rows, v, p) for v in classes)
        first += count
        second += count**2
        factorial_second += count*(count-1)
        total += 1
        good = rank(rows, p) == a and 2*count >= bounds["mu"]
        bad += not good
        if good:
            good_count += 1
            kernel_size = sum(killed(rows, v, p) for v in product(range(p), repeat=width))
            unit_count = sum(killed(rows, v, p) for v in vectors)
            assert unit_count == len(powers)*count
            assert Fraction(unit_count, kernel_size) >= bounds["good_bank_kernel_power_density_lower"]
    assert good_count > 0
    assert total == p**(a*width)
    assert Fraction(first, total) == bounds["mu"]
    assert Fraction(second, total)-bounds["mu"]**2 == bounds["variance"]
    assert Fraction(factorial_second, total) == Fraction(len(classes)*(len(classes)-1), p**(2*a))
    assert Fraction(bad, total) <= bounds["bad_bank_upper"]


@pytest.mark.parametrize("p,d,a,width", [(101, 2, 1, 5), (5, 4, 1, 3), (3, 1, 2, 3),
                                      (3, 2, 0, 1), (5, 2, 0, 4), (2, 1, 1, 2)])
def test_bounds_formulas_and_source_flags(p, d, a, width):
    b = solver.unit_projective_bank_bounds(p, d, a, width)
    h = (p-1)//d
    assert (b["S"], b["D"]) == (h**width, h**(width-1))
    assert b["mu"] == Fraction(h**(width-1), p**a)
    assert b["variance"] == b["mu"]*(1-Fraction(1, p**a))
    assert b["bad_bank_upper"] == (min(Fraction(1), 4/b["mu"]+Fraction(2, p**(width-a)))
                                     if a else Fraction(0))
    assert b["good_bank_kernel_power_density_lower"] == Fraction(h**width, 2*p**width)
    assert b["weaker_density_lower"] == Fraction(1, 2*(2*d)**width)
    assert b["good_bank_kernel_power_density_lower"] >= b["weaker_density_lower"]
    for key in ("mu", "variance", "bad_bank_upper", "good_bank_kernel_power_density_lower",
                "weaker_density_lower"):
        assert isinstance(b[key], Fraction)
    assert b["rank_zero_deterministic"] == (a == 0)
    assert b["rank_zero_kernel_power_density"] == (Fraction(h**width, p**width) if a == 0 else None)
    assert b["require_nonzero"] is True
    old = solver.projective_bank_bounds(p, d, a, width)
    for key in ("iid_uniform_columns_required", "iid_uniform_columns_verified",
                "supplied_prime_verified_by_this_api", "arbitrary_fixed_bank_guarantee",
                "fixed_bank_repetitions_repair_bad_banks"):
        assert b[key] is old[key]


@pytest.mark.parametrize("p,d,columns,bound", [(5, 1, [(0,)]*3, 0), (7, 3, [()]*4, 0),
                                           (5, 4, [(0, 0)]*3, 2), (3, 2, [()], 0)])
def test_rank_zero_all_ones_without_bits_or_roots(monkeypatch, p, d, columns, bound):
    class NoBits:
        def getrandbits(self, width):
            pytest.fail("rank-zero branch drew bits")
    monkeypatch.setattr(solver, "bounded_power_root", lambda *a, **kw: pytest.fail("root call"))
    result = solver.random_column_power_sde(p, d, columns, rank_bound=bound, attempt_cap=1,
                                            require_nonzero=True, bit_source=NoBits())
    assert_unit_witness(result)
    assert result["weights"] == result["power_vector"] == (1,)*len(columns)
    assert result["attempts"] == result["uniform_calls"] == result["root_calls"] == 0


def test_linear_sampling_covers_full_kernel_and_never_roots(monkeypatch):
    monkeypatch.setattr(solver, "bounded_power_root", lambda *a, **kw: pytest.fail("linear root call"))
    successes = set()
    for a, b in product(range(5), repeat=2):
        result = solver.random_column_power_sde(
            5, 1, [(1,), (4,), (0,)], rank_bound=1, attempt_cap=1,
            require_nonzero=True, bit_source=ScriptedBits([a, b]))
        assert result["kernel_uniform_calls"] == result["kernel_dimension"] == 2
        assert result["attempts"] == result["completed_kernel_draws"] == 1
        assert result["root_calls"] == result["root_uniform_calls"] == 0
        if a and b:
            assert_unit_witness(result)
            assert result["weights"] == result["power_vector"] == (a, a, b)
            successes.add(result["weights"])
        else:
            assert_abort(result, "ATTEMPT_CAP")
            assert result["zero_rejections"] == int(a == b == 0)
            assert result["zero_coordinate_rejections"] == int(bool(a or b))
    assert successes == {(a, a, b) for a, b in product(range(1, 5), repeat=2)}


@pytest.mark.parametrize("d", [1, 2, 4])
def test_adversarial_identity_zero_bank_has_no_all_unit_kernel(d):
    rows = [(1, 0, 0), (0, 1, 0)]
    assert rank(rows, 5) == 2
    assert not any(killed(rows, v, 5) for v in product(range(1, 5), repeat=3))
    result = solver.random_column_power_sde(
        5, d, list(zip(*rows)), rank_bound=2, attempt_cap=7,
        require_nonzero=True, bit_source=ScriptedBits([0], tail=1))
    assert_abort(result, "ATTEMPT_CAP")
    assert result["zero_rejections"] == 1
    assert result["zero_coordinate_rejections"] == 6
    assert result["nonpower_rejections"] == result["root_calls"] == 0
    assert result["kernel_uniform_calls"] == 7


def test_disjoint_rejections_then_regular_nonlinear_witness():
    columns = [(1,), (4,), (0,)]
    result = solver.random_column_power_sde(
        5, 2, columns, rank_bound=1, attempt_cap=4, require_nonzero=True,
        bit_source=PrefixedRandom([0, 0, 0, 1, 1, 2, 1, 1]))
    assert_unit_witness(result)
    assert result["power_vector"] == (1, 1, 1)
    assert result["attempts"] == 4 and result["kernel_uniform_calls"] == 8
    assert result["zero_rejections"] == result["zero_coordinate_rejections"] == result["nonpower_rejections"] == 1
    assert result["root_calls"] == 3

    def jacobian(weights):
        return [[2*weights[i]*columns[i][0] % 5 for i in range(3)]]

    assert rank(jacobian(result["weights"]), 5) == result["rank"] == 1
    old = solver.random_column_power_sde(
        5, 2, columns, rank_bound=1, attempt_cap=1, bit_source=PrefixedRandom([0, 1]))
    assert old["status"] == "VERIFIED" and old["power_vector"] == (0, 0, 1)
    assert old["require_nonzero"] is False and old["zero_coordinate_rejections"] == 0
    assert rank(jacobian(old["weights"]), 5) == 0


@pytest.mark.parametrize("d", [1, 2, 4])
def test_regular_jacobians_for_all_unit_weights(d):
    rows = [(1, 0, 2, 3), (0, 1, 4, 1)]
    for weights in product(range(1, 5), repeat=4):
        jacobian = [[x*d*pow(w, d-1, 5) % 5 for x, w in zip(row, weights)] for row in rows]
        assert rank(jacobian, 5) == rank(rows, 5) == 2


@pytest.mark.parametrize("d", [1, 2])
def test_partial_kernel_draw_bit_exhaustion_is_bounded(d):
    source = ScriptedBits([1], tail="ones")
    result = solver.random_column_power_sde(
        5, d, [(1,), (4,), (0,)], rank_bound=1, attempt_cap=5, failure_bits=2,
        require_nonzero=True, bit_source=source)
    assert_abort(result, "BIT_REJECTION_CAP")
    assert result["attempts"] == 1 and result["completed_kernel_draws"] == 0
    assert result["kernel_uniform_calls"] == 2
    assert result["bit_draws"] == source.calls == 1+result["budget"]["integer_rejection_cap"]
    assert result["root_calls"] == 0


def test_unit_root_exhaustion_never_returns_partial_witness():
    result = solver.random_column_power_sde(
        5, 2, [(1,), (4,)], rank_bound=1, attempt_cap=9, failure_bits=2,
        require_nonzero=True, bit_source=ScriptedBits([1]))
    assert_abort(result, "ROOT_SPLIT_CAP")
    assert result["attempts"] == result["root_calls"] == 1
    assert result["root_split_trials"] == result["budget"]["root_split_attempt_cap"]


@pytest.mark.parametrize("value", [None, 0, 1, "True", [], object()])
def test_nonboolean_mode_rejected_before_backend(monkeypatch, value):
    monkeypatch.setattr(solver, "_fmpz_rref", lambda *a: pytest.fail("backend called"))
    with pytest.raises(ValueError, match="require_nonzero must be a bool"):
        solver.random_column_power_sde(5, 1, [(1,), (4,)], rank_bound=1,
                                       attempt_cap=1, require_nonzero=value)


@pytest.mark.parametrize("columns,bound", [([(1,), (1,)], 1), ([(), ()], 0)])
def test_binary_unit_mode_is_explicit_preflight_error(monkeypatch, columns, bound):
    for name in ("_fmpz_rref", "_fmpz_nullspace_basis", "random_column_budget"):
        monkeypatch.setattr(solver, name, lambda *a, **kw: pytest.fail("arithmetic called"))
    with pytest.raises(ValueError, match="odd supplied prime"):
        solver.random_column_power_sde(2, 1, columns, rank_bound=bound,
                                       attempt_cap=1, require_nonzero=True)


@pytest.mark.parametrize("args", [(True, 1, 0, 1), (4, 1, 1, 3), (5, 3, 1, 3),
                                 (5, True, 1, 3), (5, 2, -1, 3), (5, 2, True, 3),
                                 (5, 2, 1, True), (5, 2, 2, 2)])
def test_invalid_unit_bounds(args):
    with pytest.raises(ValueError):
        solver.unit_projective_bank_bounds(*args)


@pytest.mark.parametrize("d", [1, 2])
def test_corrupt_all_unit_kernel_caught_at_exact_finish(monkeypatch, d):
    monkeypatch.setattr(solver, "_fmpz_nullspace_basis", lambda *a: [(1, 1)])
    with pytest.raises(ArithmeticError, match="invalid exact power-kernel witness"):
        solver.random_column_power_sde(
            5, d, [(1,), (1,)], rank_bound=1, attempt_cap=1,
            require_nonzero=True, bit_source=PrefixedRandom([1]))


def test_corrupt_kernel_dimension_is_not_statistical_abort(monkeypatch):
    monkeypatch.setattr(solver, "_fmpz_nullspace_basis", lambda *a: [])
    with pytest.raises(ArithmeticError, match="full kernel dimension mismatch"):
        solver.random_column_power_sde(5, 1, [(1,), (4,)], rank_bound=1,
                                       attempt_cap=1, require_nonzero=True)


@pytest.mark.parametrize("root", [0, True, 2, 5])
def test_corrupt_roots_never_create_unit_witness(monkeypatch, root):
    monkeypatch.setattr(solver, "bounded_power_root",
                        lambda *a, **kw: BoundedPowerRoot(root, 0, 0, 0, Fraction(0)))
    with pytest.raises(ArithmeticError, match="invalid nonzero root"):
        solver.random_column_power_sde(
            5, 2, [(1,), (4,)], rank_bound=1, attempt_cap=1,
            require_nonzero=True, bit_source=ScriptedBits([1]))


def test_backend_exception_propagates(monkeypatch):
    def broken(*args):
        raise RuntimeError("backend failed")
    monkeypatch.setattr(solver, "_fmpz_nullspace_basis", broken)
    with pytest.raises(RuntimeError, match="backend failed"):
        solver.random_column_power_sde(5, 1, [(1,), (4,)], rank_bound=1,
                                       attempt_cap=1, require_nonzero=True)


def test_unit_mode_preserves_rank_promise_abort():
    result = solver.random_column_power_sde(
        5, 1, [(1, 0), (0, 1), (0, 0)], rank_bound=1, attempt_cap=1,
        require_nonzero=True)
    assert_abort(result, "OBSERVED_RANK_EXCEEDS_PROMISE")
    assert result["attempts"] == result["uniform_calls"] == 0


@pytest.mark.parametrize("p,d,columns,bound", [(5, 2, [(0,), (0,)], 0),
                                           (5, 1, [(1,), (4,), (0,)], 1),
                                           (2, 1, [(1,), (1,), (1,)], 1),
                                           (5, 2, [(1,), (4,), (0,)], 1)])
def test_explicit_false_matches_default(p, d, columns, bound):
    args = dict(rank_bound=bound, attempt_cap=32)
    default = solver.random_column_power_sde(p, d, columns, **args, bit_source=random.Random(17))
    explicit = solver.random_column_power_sde(
        p, d, columns, **args, require_nonzero=False, bit_source=random.Random(17))
    assert default == explicit and default["status"] == "VERIFIED"
    assert default["zero_coordinate_rejections"] == 0
    if bound == 0:
        assert default["weights"] == (1, 0)
    elif d == 1:
        assert default["reason"] == "LINEAR_DETERMINISTIC" and default["uniform_calls"] == 0
