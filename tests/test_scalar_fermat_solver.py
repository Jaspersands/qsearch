from fractions import Fraction
from math import factorial
import random

import pytest

from theorems import scalar_fermat_solver as solver
from theorems.rees_projective_source import find_moment_design


@pytest.mark.parametrize("p,d", ((3, 1), (3, 2), (5, 4), (13, 4), (29, 6), (101, 4),
                                 (257, 6), (1009, 8), (2**128-275, 4), (2**128-275, 8)))
def test_all_scalar_regimes_give_exact_nonzero_witnesses(p, d):
    witness = solver.scalar_fermat_witness(p, d, rng=random.Random(20261022))
    solver.verify_fermat_witness(p, d, witness.weights)
    assert any(witness.weights) and len(witness.weights) <= d+1
    if witness.method == "degree_bounded_dynamic_program":
        assert witness.enumerated_field_elements == p < 16*(d-1)**4
        assert witness.capped_abort_bound == 0
    if witness.method == "weil_certified_random_root":
        assert witness.enumerated_field_elements == 0
        assert witness.success_probability_lower_bound == Fraction(1, 2*d)
        assert witness.capped_abort_bound == Fraction(2*d-1, 2*d)**128
        assert 1 <= witness.trials <= 128
        assert witness.root_runtime_locally_clocked is False


def test_small_field_solver_covers_all_degrees_below_several_primes():
    for p in (3, 5, 7, 11, 13, 17, 19):
        for d in range(1, p):
            witness = solver.scalar_fermat_witness(p, d, rng=random.Random(10*p+d))
            assert sum(pow(x, d, p) for x in witness.weights) % p == 0
            assert any(witness.weights)


@pytest.mark.parametrize("p,d", ((17, 2), (101, 4), (257, 6)))
def test_success_bound_against_exact_bounded_convolution_counts(p, d):
    assert solver.large_field_regime(p, d)
    multiplicities = {}
    for x in range(p):
        power = pow(x, d, p)
        multiplicities[power] = multiplicities.get(power, 0)+1
    counts = {0: 1}
    for _ in range(d):
        next_counts = {}
        for before, count in counts.items():
            for power, multiplicity in multiplicities.items():
                after = (before+power) % p
                next_counts[after] = next_counts.get(after, 0)+count*multiplicity
        counts = next_counts
    assert sum(counts.values()) == p**d
    successful_prefixes = sum(count for total, count in counts.items() if -total % p in multiplicities)-1
    assert Fraction(successful_prefixes, p**d) >= Fraction(1, 2*d)


@pytest.mark.parametrize("p", (13, 101, 2**128-275))
def test_previously_missing_quartic_path_builds_a_separating_phase_free_design(p):
    design = find_moment_design(p, 4, max_order=4, rng=random.Random(19))
    assert design.method == "scalar_certificate_multiplicative_convolution"
    assert design.moments == (0, 0, 0, 0)
    assert len(set(design.points)) >= 4
    assert design.copies_per_block <= factorial(5)


def test_large_fields_cannot_enter_dynamic_program_and_bad_sampling_aborts():
    with pytest.raises(ValueError, match="enumeration"):
        solver._small_field_witness(2**128-275, 4)
    class ConstantRandom:
        def __init__(self, value):
            self.value = value
        def randrange(self, stop):
            return self.value
    with pytest.raises(RuntimeError, match="aborted"):
        solver.scalar_fermat_witness(101, 4, max_trials=3, rng=ConstantRandom(0))
    for invalid in (True, -1, 101):
        with pytest.raises(ValueError, match="random source"):
            solver.scalar_fermat_witness(101, 4, rng=ConstantRandom(invalid))


def test_wrong_root_cannot_be_accepted(monkeypatch):
    monkeypatch.setattr(solver, "_field_root", lambda p, degree, value: p)
    with pytest.raises(ValueError, match="canonical"):
        solver.scalar_fermat_witness(101, 4, rng=random.Random(20261022))


def test_exact_sampling_cap_pays_all_design_rows_by_union_bound():
    for degree in (2, 4, 9):
        error = Fraction(1, 10**18)
        cap = solver.fermat_trial_cap(degree, error/degree)
        assert sum(Fraction(2*r-1, 2*r)**cap for r in range(1, degree+1)) <= error
    for bad in (0.1, Fraction(0), Fraction(1)):
        with pytest.raises(ValueError):
            solver.fermat_trial_cap(4, bad)


def test_large_prime_control_is_not_a_two_term_fermat_pair():
    p = 2**128-275
    assert p % 8 == 5
    # -1 is not a fourth power, so (1,root(-1)) cannot solve this case.
    assert pow(p-1, (p-1)//4, p) != 1
    witness = solver.scalar_fermat_witness(p, 4, rng=random.Random(20261022))
    assert sum(x != 0 for x in witness.weights) >= 3


def test_invalid_witnesses_and_scope_flags():
    for weights in ((), (0, 0), (True, 0), (-1, 1), (13, 1), (1,)*6):
        with pytest.raises(ValueError):
            solver.verify_fermat_witness(13, 4, weights)
    with pytest.raises(ArithmeticError):
        solver.verify_fermat_witness(13, 4, (1, 1))
    for d in (0, True, 13):
        with pytest.raises(ValueError):
            solver.scalar_fermat_witness(13, d)
    report = solver.build_report()
    for field in ("large_prime_enumeration", "general_many_equation_sde_implemented",
                  "quantum_receiver_implemented", "novelty_established", "speedup_claim_allowed"):
        assert report[field] is False
