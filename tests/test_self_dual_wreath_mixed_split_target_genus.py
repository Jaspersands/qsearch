from fractions import Fraction

from self_dual_wreath_mixed_split_target_genus import (
    audit_split_target_genus,
    cyclic_one_run_count,
    run_mixed_split_target_genus,
    split_only_normalized_character_factor,
    split_target_orientable_genus,
    split_target_orientable_genus_for_pattern,
    symmetric_group_standard_character_average,
)


def test_cyclic_run_genus_distinguishes_blocks_from_interleaving():
    assert cyclic_one_run_count((0, 0, 0, 1, 1, 1)) == 1
    assert split_target_orientable_genus((0, 0, 0, 1, 1, 1)) == 0
    assert split_target_orientable_genus((0, 1, 0, 1)) == 1
    assert split_target_orientable_genus((0, 1, 0, 1, 0, 1)) == 2
    assert split_target_orientable_genus_for_pattern("EFAEFBBB") == 0
    assert split_target_orientable_genus_for_pattern("EBEFBF") == 1


def test_tietze_transport_recovers_the_predicted_surface_genus():
    contiguous = audit_split_target_genus((0, 0, 0, 1, 1, 1))
    genus_one = audit_split_target_genus((0, 1, 0, 1))
    genus_two = audit_split_target_genus((0, 1, 0, 1, 0, 1))
    assert contiguous.target_freely_trivial
    assert contiguous.classified_orientable_genus == 0
    assert genus_one.classified_orientable_genus == 1
    assert genus_two.classified_orientable_genus == 2
    assert all(
        row.exact_genus_verified for row in (contiguous, genus_one, genus_two)
    )


def test_split_only_character_factor_matches_exact_S3_standard_average():
    genus_one = (0, 1, 0, 1)
    genus_two = (0, 1, 0, 1, 0, 1)
    assert split_only_normalized_character_factor(genus_one, 2) == Fraction(1, 4)
    assert split_only_normalized_character_factor(genus_two, 2) == Fraction(1, 16)
    assert symmetric_group_standard_character_average(genus_one) == Fraction(1, 4)
    assert symmetric_group_standard_character_average(genus_two) == Fraction(1, 16)


def test_exhaustive_split_target_report_keeps_support_conditioning_open():
    report = run_mixed_split_target_genus(maximum_position_count=9)
    assert report.headline_metrics["checked_split_pattern_count"] == 1022
    assert report.headline_metrics["split_target_genus_control_failure_count"] == 0
    assert report.claim_gate["split_only_target_genus_theorem_proved"]
    assert report.claim_gate["split_only_character_factor_theorem_proved"]
    assert not report.claim_gate[
        "support_conditioned_target_character_theorem_proved"
    ]
    assert not report.claim_gate["growing_degree_component_moment_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
