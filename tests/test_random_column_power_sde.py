"""Independent exhaustive small-field controls and bounded arithmetic runs."""
from fractions import Fraction
from itertools import product
import random

import pytest

from theorems import random_column_power_sde as solver


class ScriptedBits:
    def __init__(self, prefix=(), *, tail=0):
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


def independent_rank(rows, p):
    matrix = [list(row) for row in rows]
    pivot = 0
    for col in range(len(matrix[0])):
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


@pytest.mark.parametrize("p,d,a,width", [(3, 2, 1, 3), (5, 2, 1, 3), (3, 2, 2, 3)])
def test_exact_projective_moments_over_every_matrix(p, d, a, width):
    # Build the power set directly from powers, not the production residue
    # predicate, and quotient by ordinary projective normalization.
    powers = {pow(x, d, p) for x in range(p)}
    vectors = [v for v in product(sorted(powers), repeat=width) if any(v)]
    classes = {tuple(x*pow(next(y for y in v if y), -1, p) % p for x in v)
               for v in vectors}
    bounds = solver.projective_bank_bounds(p, d, a, width)
    assert bounds["S"] == len(vectors)
    assert bounds["D"] == len(classes)
    assert len(vectors) == bounds["h"]*len(classes)
    total = first = second = factorial_second = bad = 0
    for entries in product(range(p), repeat=a*width):
        rows = [entries[i*width:(i+1)*width] for i in range(a)]
        count = sum(killed(rows, v, p) for v in classes)
        total += 1
        first += count
        second += count*count
        factorial_second += count*(count-1)
        good = independent_rank(rows, p) == a and 2*count >= bounds["mu"]
        bad += not good
        if good:
            kernel_size = sum(killed(rows, v, p) for v in product(range(p), repeat=width))
            good_vectors = sum(killed(rows, v, p) for v in vectors)
            assert good_vectors == bounds["h"]*count
            assert Fraction(good_vectors, kernel_size) >= bounds["good_bank_kernel_power_density_lower"]
    assert total == p**(a*width)
    assert Fraction(first, total) == bounds["mu"]
    assert Fraction(second, total)-bounds["mu"]**2 == bounds["variance"]
    assert Fraction(factorial_second, total) == Fraction(len(classes)*(len(classes)-1), p**(2*a))
    assert Fraction(bad, total) <= bounds["bad_bank_upper"]


@pytest.mark.parametrize("p,d,a,width", [(101, 2, 1, 5), (5, 4, 1, 3), (3, 1, 2, 3),
                                      (3, 2, 0, 1), (5, 4, 0, 1), (2, 1, 1, 2)])
def test_exact_bounds_and_scope(p, d, a, width):
    b = solver.projective_bank_bounds(p, d, a, width)
    h, size = (p-1)//d, ((p-1)//d+1)**width-1
    assert b["h"] == h and b["D"] == size//h
    assert b["mu"] == Fraction(size//h, p**a)
    assert b["variance"] == b["mu"]*(1-Fraction(1, p**a))
    assert b["bad_bank_upper"] == (min(Fraction(1), 4/b["mu"]+Fraction(2, p**(width-a)))
                                     if a else 0)
    assert b["good_bank_kernel_power_density_lower"] == Fraction(size, 2*p**width)
    if p**width >= 2*d**width:
        assert b["weaker_density_lower"] == Fraction(1, 4*d**width)
        assert b["good_bank_kernel_power_density_lower"] >= b["weaker_density_lower"]
    else:
        assert b["weaker_density_lower"] is None
    for key in ("mu", "variance", "bad_bank_upper", "good_bank_kernel_power_density_lower"):
        assert isinstance(b[key], Fraction)
    if a == 0:
        assert b["rank_zero_deterministic"]
        assert b["rank_zero_kernel_power_density"] == Fraction(size, p**width)
    assert b["iid_uniform_columns_required"] and not b["iid_uniform_columns_verified"]
    assert not b["arbitrary_fixed_bank_guarantee"]
    assert not b["fixed_bank_repetitions_repair_bad_banks"]
    assert not b["supplied_prime_verified_by_this_api"]


def assert_counts(result):
    b = result["budget"]
    assert result["attempts"] <= b["attempt_cap"]
    for count, cap in (("root_calls", "root_call_cap"), ("uniform_calls", "uniform_call_cap"),
                       ("kernel_uniform_calls", "kernel_uniform_call_cap"),
                       ("root_uniform_calls", "root_uniform_call_cap"),
                       ("root_split_trials", "root_split_trial_cap"),
                       ("bit_draws", "bit_draw_cap"), ("random_bits", "random_bit_cap")):
        assert 0 <= result[count] <= b[cap]
    assert result["uniform_calls"] == result["kernel_uniform_calls"]+result["root_uniform_calls"]
    assert result["random_bits"] == result["bit_draws"]*(result["p"]-1).bit_length()
    assert b["auxiliary_abort_upper"] <= Fraction(1, 2**b["failure_bits"])
    assert not b["attempt_exhaustion_included"]
    assert not result["input_labels_resampled"] and not result["field_enumeration_used"]
    for key in ("iid_uniform_columns_verified", "iid_fair_bits_verified",
                "supplied_prime_verified_by_this_api", "prime_validation_locally_clocked",
                "quantum_receiver_implemented", "hsp_claim", "speedup_claim"):
        assert result[key] is False
    assert result["arbitrary_fixed_bank_success_bound"] is None


def assert_witness(result):
    assert result["status"] == "VERIFIED" and result["exact_verified"]
    p, d = result["p"], result["d"]
    weights, vector, bank = result["weights"], result["power_vector"], result["columns"]
    assert any(weights) and len(weights) == len(bank)
    assert tuple(pow(s, d, p) for s in weights) == vector
    assert all((s == 0) == (w == 0) for s, w in zip(weights, vector))
    assert all(sum(pow(s, d, p)*col[j] for s, col in zip(weights, bank)) % p == 0
               for j in range(len(bank[0])))
    assert_counts(result)


def assert_abort(result, reason):
    assert result["status"] == "ABORT" and result["reason"] == reason
    assert result["weights"] is None and result["power_vector"] is None
    assert not result["exact_verified"]
    assert_counts(result)


@pytest.mark.parametrize("p,d", [(3, 2), (5, 2), (5, 4), (7, 3), (7, 6), (13, 4)])
def test_explicit_bank_success_reproducible_and_no_symmetric_guard(monkeypatch, p, d):
    import theorems.power_sde as symmetric
    monkeypatch.setattr(symmetric, "validate_family", lambda *a: pytest.fail("symmetric guard"))
    bank = [(1,), (p-1,)]
    result = solver.random_column_power_sde(p, d, bank, rank_bound=1, attempt_cap=128,
                                            failure_bits=4, bit_source=random.Random(17))
    repeated = solver.random_column_power_sde(p, d, bank, rank_bound=1, attempt_cap=128,
                                              failure_bits=4, bit_source=random.Random(17))
    assert result == repeated and bank == [(1,), (p-1,)]
    assert_witness(result)


def test_seeded_bank_is_not_an_iid_certificate():
    fixture = random.Random(31)
    bank = [tuple(fixture.randrange(13) for _ in range(2)) for _ in range(6)]
    result = solver.random_column_power_sde(13, 2, bank, rank_bound=2, attempt_cap=512,
                                            failure_bits=8, bit_source=random.Random(32))
    assert_witness(result)
    assert not result["iid_uniform_columns_verified"]


@pytest.mark.parametrize("p,d,bank,bound", [(5, 4, [(0,), (0,)], 0), (7, 3, [(), ()], 0),
                                          (5, 1, [(1,), (2,), (3,)], 1),
                                          (2, 1, [(1,), (1,), (1,)], 1)])
def test_deterministic_branches(p, d, bank, bound):
    class NoBits:
        def getrandbits(self, width):
            pytest.fail("deterministic branch consumed randomness")
    result = solver.random_column_power_sde(p, d, bank, rank_bound=bound, attempt_cap=1,
                                            bit_source=NoBits())
    assert_witness(result)
    assert result["attempts"] == result["root_calls"] == result["uniform_calls"] == 0
    if not bound:
        assert result["weights"] == (1, 0)


def test_full_nullspace_draw_and_zero_coordinates_skip_root_calls(monkeypatch):
    original = solver.bounded_power_root
    calls = []
    def checked(p, d, x, **kwargs):
        assert x != 0
        calls.append(x)
        return original(p, d, x, **kwargs)
    monkeypatch.setattr(solver, "bounded_power_root", checked)
    # Nullspace basis is (1,1,0), (0,0,1). Use the SECOND vector only.
    result = solver.random_column_power_sde(5, 2, [(1,), (4,), (0,)], rank_bound=1,
                                            attempt_cap=1, bit_source=PrefixedRandom([0, 1]))
    assert_witness(result)
    assert result["power_vector"] == (0, 0, 1) and calls == [1]
    assert result["kernel_uniform_calls"] == result["kernel_dimension"] == 2


def test_all_kernel_coefficients_cover_full_kernel_uniformly(monkeypatch):
    observed = set()
    original = solver._fmpz_nullspace_basis
    def checked(rows, width, p):
        basis = original(rows, width, p)
        assert len(basis) == 2
        return basis
    monkeypatch.setattr(solver, "_fmpz_nullspace_basis", checked)
    for a, b in product(range(5), repeat=2):
        result = solver.random_column_power_sde(5, 2, [(1,), (4,), (0,)], rank_bound=1,
                                                attempt_cap=1, bit_source=PrefixedRandom([a, b]))
        assert result["kernel_uniform_calls"] == 2
        v = (a, a, b)
        observed.add(v)
        if any(v) and all(x in {0, 1, 4} for x in v):
            assert_witness(result)
            assert result["power_vector"] == v
        else:
            assert_abort(result, "ATTEMPT_CAP")
    assert observed == {v for v in product(range(5), repeat=3) if (v[0]-v[1]) % 5 == 0}


def test_adversarial_full_row_rank_bank_has_no_nonzero_power_kernel():
    assert independent_rank([[1, 1, 1]], 5) == 1
    assert {pow(x, 4, 5) for x in range(5)} == {0, 1}
    assert not any(any(v) and sum(v) % 5 == 0 for v in product((0, 1), repeat=3))
    for seed in range(4):
        result = solver.random_column_power_sde(5, 4, [(1,)]*3, rank_bound=1,
                                                attempt_cap=50, bit_source=random.Random(seed))
        assert_abort(result, "ATTEMPT_CAP")
        assert result["rank"] == 1 and result["attempts"] == 50
        assert result["zero_rejections"]+result["nonpower_rejections"] == 50
        assert result["root_calls"] == 0 and result["kernel_uniform_calls"] == 100


def test_zero_kernel_vectors_never_accepted():
    result = solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1,
                                            attempt_cap=7, bit_source=ScriptedBits())
    assert_abort(result, "ATTEMPT_CAP")
    assert result["zero_rejections"] == result["completed_kernel_draws"] == 7


def test_bit_rejection_exhaustion_in_kernel():
    source = ScriptedBits(tail="ones")
    result = solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1,
                                            attempt_cap=9, failure_bits=2, bit_source=source)
    assert_abort(result, "BIT_REJECTION_CAP")
    assert result["bit_draws"] == source.calls == result["budget"]["integer_rejection_cap"]
    assert result["kernel_uniform_calls"] == result["attempts"] == 1
    assert result["completed_kernel_draws"] == result["root_calls"] == 0


def test_root_exhaustion_is_terminal_and_exactly_capped():
    source = ScriptedBits([1])
    result = solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1,
                                            attempt_cap=30, failure_bits=2, bit_source=source)
    assert_abort(result, "ROOT_SPLIT_CAP")
    assert result["attempts"] == result["root_calls"] == 1
    assert result["root_split_trials"] == result["budget"]["root_split_attempt_cap"]
    assert result["root_uniform_calls"] == 2*result["root_split_trials"]
    assert result["bit_draws"] == source.calls == 1+result["root_uniform_calls"]
    assert result["root_split_counts_complete"]


def test_bit_exhaustion_inside_root_charged_without_fabricated_split_count():
    source = ScriptedBits([1, 0], tail="ones")
    result = solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1,
                                            attempt_cap=30, failure_bits=2, bit_source=source)
    assert_abort(result, "BIT_REJECTION_CAP")
    assert result["attempts"] == result["root_calls"] == 1
    assert result["root_uniform_calls"] == 2
    assert result["bit_draws"] == source.calls == 2+result["budget"]["integer_rejection_cap"]
    assert not result["root_split_counts_complete"]


def test_failure_after_successful_root_never_returns_partial_witness(monkeypatch):
    from theorems.bounded_power_roots import BoundedPowerRoot
    calls = []
    def roots(p, d, value, *, rng, split_attempt_cap):
        calls.append(value)
        root = 1 if len(calls) == 1 else None
        return BoundedPowerRoot(root, 0, 0, 0, Fraction(0))
    monkeypatch.setattr(solver, "bounded_power_root", roots)
    result = solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1,
                                            attempt_cap=100, bit_source=ScriptedBits([1]))
    assert_abort(result, "ROOT_SPLIT_CAP")
    assert calls == [1, 1] and result["root_calls"] == 2
    assert result["attempts"] == 1


@pytest.mark.parametrize("d,width,attempts,bits", [(1, 1, 1, 1), (2, 3, 7, 1),
                                                 (4, 12, 9, 8), (6, 3, 100, 32)])
def test_budget_formulas(d, width, attempts, bits):
    b = solver.random_column_budget(13, d, width, attempt_cap=attempts, failure_bits=bits)
    k = 3*(bits+(max(1, width*(d-1))-1).bit_length()+2)
    assert b["root_split_attempt_cap"] == k
    assert b["kernel_uniform_call_cap"] == width*attempts
    assert b["root_call_cap"] == (width if d > 1 else 0)
    assert b["root_uniform_call_cap"] == width*d*(d-1)*k
    assert b["uniform_call_cap"] == width*attempts+width*d*(d-1)*k
    assert b["root_abort_upper"] == width*(d-1)*Fraction(2, 3)**k
    assert b["bit_abort_upper"] == Fraction(b["uniform_call_cap"], 2**b["integer_rejection_cap"])
    assert b["root_abort_upper"] <= Fraction(1, 2**(bits+2))
    assert b["bit_abort_upper"] <= Fraction(1, 2**(bits+1))


@pytest.mark.parametrize("patch", [dict(p=True), dict(p=1), dict(p=4), dict(d=0), dict(d=True),
                                  dict(d=3), dict(rank_bound=-1), dict(rank_bound=True),
                                  dict(rank_bound=2), dict(attempt_cap=0), dict(attempt_cap=True),
                                  dict(failure_bits=0), dict(failure_bits=1.5),
                                  dict(columns=[]), dict(columns=[1, 2]),
                                  dict(columns=[(1,), (1, 2)]), dict(columns=[(1,), (5,)]),
                                  dict(columns=[(1,), (-1,)]), dict(columns=[(1,), (True,)]),
                                  dict(columns=[(1,), (1.0,)]), dict(bit_source=object()),
                                  dict(bit_source=ScriptedBits)])
def test_malformed_inputs_raise(patch):
    args = dict(p=5, d=2, columns=[(1,), (4,)], rank_bound=1, attempt_cap=3)
    args.update(patch)
    with pytest.raises(ValueError):
        solver.random_column_power_sde(**args)


def test_rank_bound_checked_against_actual_rank_and_not_ambient_dimension():
    rejected = solver.random_column_power_sde(
        5, 2, [(1, 0), (0, 1), (0, 0)], rank_bound=1, attempt_cap=1)
    assert_abort(rejected, "OBSERVED_RANK_EXCEEDS_PROMISE")
    assert rejected["attempts"] == rejected["uniform_calls"] == 0
    result = solver.random_column_power_sde(5, 2, [(1, 2, 3), (4, 3, 2)], rank_bound=1,
                                            attempt_cap=30, bit_source=random.Random(2))
    assert_witness(result)


@pytest.mark.parametrize("value", [True, -1, 8, 1.5])
def test_malformed_bits_raise_not_abort(value):
    with pytest.raises(ValueError, match="noncanonical bit string"):
        solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1,
                                       attempt_cap=1, bit_source=ScriptedBits([value]))


@pytest.mark.parametrize("args", [(3, 2, 1, 1), (5, 3, 1, 3), (5, 2, -1, 3), (5, 2, 1, True)])
def test_malformed_bounds_raise(args):
    with pytest.raises(ValueError):
        solver.projective_bank_bounds(*args)


def test_explicit_attempt_cap_is_required():
    with pytest.raises(TypeError, match="attempt_cap"):
        solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1)


def test_backend_errors_and_invalid_roots_are_not_statistical_aborts(monkeypatch):
    def broken(*args, **kwargs):
        raise RuntimeError("backend failed")
    monkeypatch.setattr(solver, "bounded_power_root", broken)
    with pytest.raises(RuntimeError, match="backend failed"):
        solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1,
                                       attempt_cap=1, bit_source=ScriptedBits([1]))
    from theorems.bounded_power_roots import BoundedPowerRoot
    monkeypatch.setattr(solver, "bounded_power_root",
                        lambda *a, **kw: BoundedPowerRoot(0, 0, 0, 0, Fraction(0)))
    with pytest.raises(ArithmeticError, match="invalid nonzero root"):
        solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1,
                                       attempt_cap=1, bit_source=ScriptedBits([1]))


def test_final_exact_verification_rejects_corrupt_kernel_basis(monkeypatch):
    monkeypatch.setattr(solver, "_fmpz_nullspace_basis", lambda *a: [(1, 0)])
    with pytest.raises(ArithmeticError, match="invalid exact power-kernel"):
        solver.random_column_power_sde(5, 2, [(1,), (4,)], rank_bound=1,
                                       attempt_cap=1, bit_source=PrefixedRandom([1]))


@pytest.mark.parametrize("p,d", [(2**61-1, 2), (2**127-1, 3)])
def test_large_prime_run_has_no_field_sized_python_loops(monkeypatch, p, d):
    import theorems.bounded_power_roots as roots
    import theorems.symbolic_scalar_phase_erasure as linear
    def bounded_range(*args):
        r = range(*args)
        assert len(r) <= 10000, "field-sized enumeration"
        return r
    for module in (solver, roots, linear):
        monkeypatch.setattr(module, "range", bounded_range, raising=False)
    result = solver.random_column_power_sde(p, d, [(1,), (p-1,), (0,)], rank_bound=1,
                                            attempt_cap=128, failure_bits=8,
                                            bit_source=random.Random(22))
    assert_witness(result)
