import itertools
import math
from functools import lru_cache

import pytest

from self_dual_wreath_nonsystematic_incidence_lattice_bound import (
    INDEX_THREE_CODE,
    RANK_DEFICIENT_CODE,
    audit_binomial_residue_anticoncentration,
    audit_incidence_lattice,
    incidence_lattice_all_depth_certificate,
    maximum_multilevel_binomial_residue_sum,
    run_nonsystematic_incidence_lattice_bound,
)
from self_dual_wreath_nonsystematic_mod_four_no_go import mod_four_code
from self_dual_wreath_nonsystematic_twisted_star_no_go import twisted_star_code


@lru_cache(maxsize=1)
def _report():
    return run_nonsystematic_incidence_lattice_bound()


@pytest.mark.parametrize(
    ("control_id", "code", "expected_rank", "expected_index"),
    (
        ("INDEX-TWO", twisted_star_code(5), 5, 2),
        ("INDEX-THREE", INDEX_THREE_CODE, 5, 3),
        ("INDEX-FOUR", mod_four_code(6), 6, 4),
        ("RANK-DEFICIENT", RANK_DEFICIENT_CODE, 4, None),
    ),
)
def test_pair_covered_quarter_codes_have_cyclic_incidence_quotients(
    control_id,
    code,
    expected_rank,
    expected_index,
):
    control = audit_incidence_lattice(control_id, code)
    assert control.minimum_distance >= 2
    assert control.all_coordinate_pairs_covered
    assert not control.has_dimension_sized_information_set
    assert control.integer_incidence_rank == expected_rank
    assert control.finite_lattice_index == expected_index
    assert all(value == 1 for value in control.nonzero_smith_invariants[:-1])
    assert control.signed_congruence_vector
    assert control.signed_relation_verified
    assert control.exact_control_verified


def test_nine_bit_window_has_sharp_127_over_512_multilevel_bound():
    maximum, residue = maximum_multilevel_binomial_residue_sum(9, 5)
    assert maximum == math.comb(9, 0) + math.comb(9, 5) == 127
    assert residue in (0, 4)
    assert maximum / 2**9 < 0.25


@pytest.mark.parametrize(
    ("width", "expected_maximum"),
    ((5, 2), (6, 7), (7, 22), (8, 57)),
)
def test_small_width_multilevel_residue_bounds(width, expected_maximum):
    observed = max(
        maximum_multilevel_binomial_residue_sum(width, modulus)[0]
        for modulus in range(5, width + 1)
    )
    assert observed == expected_maximum
    assert observed < 2 ** (width - 2)


def test_all_checked_moduli_obey_the_anticoncentration_theorem():
    for width in range(5, 41):
        for modulus in range(5, width + 1):
            control = audit_binomial_residue_anticoncentration(width, modulus)
            assert control.every_multilevel_residue_strictly_below_quarter


def test_infinite_cyclic_quotient_cannot_reach_quarter_density_after_width_eight():
    assert math.comb(8, 4) > 2 ** (8 - 2)
    assert math.comb(9, 4) < 2 ** (9 - 2)
    previous = math.comb(9, 4) / 2**9
    for width in range(10, 80):
        ratio = math.comb(width, width // 2) / 2**width
        assert ratio <= previous
        previous = ratio


def test_report_excludes_only_the_abelian_incidence_escape():
    theorem = incidence_lattice_all_depth_certificate()
    assert theorem.arbitrary_width_at_least_nine
    assert theorem.growing_abelian_torsion_escape_excluded
    assert theorem.full_rank_maximum_lattice_index == 4
    assert theorem.rank_deficient_maximum_width == 8
    assert theorem.nonabelian_residual_presentation_still_open
    report = _report()
    assert report.headline_metrics[
        "all_depth_incidence_lattice_bound_theorem_count"
    ] == 1
    assert report.headline_metrics["maximum_realized_finite_index"] == 4
    assert report.headline_metrics["anticoncentration_failure_count"] == 0
    assert report.claim_gate[
        "no_information_set_forces_cyclic_incidence_quotient"
    ]
    assert not report.claim_gate[
        "growing_abelian_smith_torsion_escape_survives"
    ]
    assert not report.claim_gate["rank_deficient_all_depth_escape_survives"]
    assert report.claim_gate["bounded_index_nonabelian_residual_escape_open"]
    assert not report.claim_gate["all_nonsystematic_stopping_codes_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
