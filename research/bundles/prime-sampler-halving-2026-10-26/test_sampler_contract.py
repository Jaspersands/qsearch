from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path

import pytest

from sampler_contract import (exact_character_bias, parity_law,
                              prime_sampling_certificate, relation_batch_bound)


@pytest.mark.parametrize("g", [1, 6, 41, 81, 161, 321, 641, 10**4, 10**8, 10**16])
def test_sufficient_prime_degree_without_zeta(g):
    result = prime_sampling_certificate(g)
    n = result["prime_degree"]
    assert result["exact_sufficiency_ratio"] >= 1
    assert n <= g+1 and result["fits_recovered_degree_i2_budget"]
    if n > 1:
        assert 100003**(n-1) < 16*(g+1)**2*(n+5)**2
    assert result["exact_group_order_still_required"]
    assert not result["native_sampler_implemented"]


def test_relation_batch_failure_and_exact_verification():
    for t in range(101):
        result = relation_batch_bound(t)
        assert result["unverified_kernel_probability_upper"] < F(1, 4)
        assert result["false_acceptance_after_exact_verification"] == 0
        assert result["requires_independent_samples"]


@pytest.mark.parametrize("rank", [1, 2, 3, 4, 5])
def test_all_index_two_subgroups_have_escape_mass_one_quarter(rank):
    law = parity_law(rank)
    for character in range(1, 2**rank):
        assert exact_character_bias(law, character) == F(1, 2)
        escape = sum(w for x, w in enumerate(law) if (x & character).bit_count() % 2)
        assert escape == F(1, 4)


def test_correlated_rows_do_not_have_exponential_detection_guarantee():
    # Reuse one unbiased bit: a nonzero torsion element survives with
    # probability1/2, regardless of the number of identical rows.
    independent_bound = relation_batch_bound(1)["unverified_kernel_probability_upper"]
    assert F(1, 2) > independent_bound


def test_sampler_confined_to_current_subgroup_fails_contract():
    with pytest.raises(ValueError):
        exact_character_bias([1, 0], 0)
    assert exact_character_bias([1, 0], 1) == 1


def test_sparse_nonuniform_group_samples_still_support_verified_saturation():
    path = Path(__file__).resolve().parents[1]/"auxiliary-construction-check-2026-10-26/exact_controls.py"
    spec = spec_from_file_location("reviewed_halving_controls", path)
    old = module_from_spec(spec)
    spec.loader.exec_module(old)

    class SparseSamplerGroup(old.TwoGroup):
        def sample(self):
            if self.rng.randrange(2):
                return self.zero
            return tuple(self.rng.randrange(2) for _ in self.moduli)

    group = SparseSamplerGroup([8, 4])
    generators = []
    subgroup_order = 1
    proposals = 0
    while subgroup_order < group.order:
        proposal = group.sample()
        lattice, _ = old.relation_lattice(group, generators+[proposal])
        order = int(lattice.det())
        if order > subgroup_order:
            generators.append(proposal)
            subgroup_order = order
        proposals += 1
        assert proposals <= 100
    assert subgroup_order == 32
    for target in product(range(8), range(4)):
        extended = generators+[target]
        lattice, _ = old.relation_lattice(group, extended)
        unit = [0]*len(generators)+[1]
        solved = old.binary_solve(lattice.tolist(), len(extended), unit)
        assert (solved is not None) == all(x % 2 == 0 for x in target)
        if solved is not None:
            v = (old.Matrix(unit)+lattice*old.Matrix(solved[0]))/2
            half = group.combine(extended, v)
            assert group.combine([half], [2]) == target
    # Only four of32 group elements can be sampled, so full uniformity
    # and small full-group total variation were not smuggled into this test.
    assert F(1, 1)-F(4, 32) == F(7, 8)
