from fractions import Fraction

from self_dual_wreath_character_ratio_contract import (
    character_ratio_stress_record,
    factorized_unequal_character_ratio,
    normalized_symmetric_character,
    run_character_ratio_contract,
    transposition_length,
    validate_unequal_character_factorization,
)


def test_transposition_length_from_cycle_type() -> None:
    assert transposition_length((1, 1, 1, 1)) == 0
    assert transposition_length((2, 1, 1)) == 1
    assert transposition_length((4,)) == 3


def test_normalized_character_is_exact_fraction() -> None:
    assert normalized_symmetric_character((3,), (2, 1)) == 1
    assert normalized_symmetric_character((1, 1, 1), (2, 1)) == -1
    assert isinstance(
        normalized_symmetric_character((2, 1), (3,)),
        Fraction,
    )


def test_unequal_character_factorization_is_exact() -> None:
    for n in (2, 3, 4):
        record = validate_unequal_character_factorization(n)
        assert record.exact_factorization_verified
        assert record.failed_element_count == 0


def test_swap_coset_factor_is_zero() -> None:
    identity = (0, 1, 2)
    assert (
        factorized_unequal_character_ratio(
            (3,),
            (2, 1),
            identity,
            identity,
            1,
        )
        == 0
    )


def test_character_ratio_constant_probe_is_finite() -> None:
    record = character_ratio_stress_record(8, (4, 2, 1, 1))
    assert record.dimension > 0
    assert 0 <= record.maximum_nonidentity_character_ratio <= 1
    assert record.maximum_required_feray_sniady_constant_proxy >= 0


def test_report_keeps_short_word_theorem_open() -> None:
    report = run_character_ratio_contract()
    assert report.claim_gate[
        "exact_unequal_character_factorization_proved"
    ]
    assert report.claim_gate["character_bound_literature_linked"]
    assert not report.claim_gate[
        "joint_short_word_anticoncentration_proved"
    ]
    assert not report.claim_gate[
        "collision_free_polynomial_factor_norm_bound_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
