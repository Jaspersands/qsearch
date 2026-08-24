import json
import math

from self_dual_wreath_branch_character_natural_frobenius_word_map import (
    audit_natural_regular_moments,
    audit_range_overlap_stress,
    direct_expected_plancherel_residual,
    regular_range_overlap,
    regular_word_kernel_matrices,
    run_natural_frobenius_word_map,
    validate_regular_word_map,
    write_natural_frobenius_word_map_report,
)


def test_regular_word_kernel_equals_direct_two_plancherel_average() -> None:
    for n in (2, 3, 4):
        control = validate_regular_word_map(n, maximum_triples=16)
        assert control.exact_regular_word_map_verified
        assert control.maximum_regular_to_plancherel_residual < 1e-9


def test_kcopy_moment_matches_direct_tuple_enumeration() -> None:
    matrices = regular_word_kernel_matrices(3)
    reduced = sum((matrix**2).mean().real for _shift, matrix in matrices)
    direct = direct_expected_plancherel_residual(3, 2)
    assert math.isclose(reduced, direct, rel_tol=1e-9, abs_tol=1e-9)


def test_information_law_copy_counts_contract_in_finite_controls() -> None:
    expected = {
        3: (5, 0.07514348778277352),
        4: (7, 0.03115528640159676),
        5: (9, 0.008559535048494576),
    }
    for n, (copies, residual) in expected.items():
        control = audit_natural_regular_moments(n)
        assert control.information_threshold_copy_count == copies
        assert math.isclose(
            control.information_threshold_expected_residual,
            residual,
            rel_tol=1e-9,
        )
        assert control.finite_contraction_observed
        assert not control.tensor_carrier_materialized


def test_three_times_threshold_copy_scale_shrinks_residual_further() -> None:
    control = audit_natural_regular_moments(5)
    assert control.triple_threshold_copy_count == 23
    assert (
        control.triple_threshold_expected_residual
        < control.information_threshold_expected_residual
    )
    assert (
        control.triple_threshold_half_window_bad_mass_upper_bound
        < control.information_threshold_half_window_bad_mass_upper_bound
    )


def test_range_overlap_coefficient_formula_detects_order_eight_boundary() -> None:
    identity = tuple(range(8))
    generator = tuple((index + 1) % 8 for index in range(8))
    cube = tuple((index + 3) % 8 for index in range(8))
    assert identity != generator
    assert math.isclose(
        regular_range_overlap(generator, cube),
        0.75,
        rel_tol=1e-10,
    )


def test_cyclic_and_symmetric_stress_validate_the_all_order_theorem() -> None:
    controls = audit_range_overlap_stress()
    assert controls[0].maximum_order_tested == 512
    assert math.isclose(
        controls[0].maximum_regular_range_overlap,
        0.75,
        rel_tol=1e-10,
    )
    assert all(row.all_tested_pairs_obey_three_quarter for row in controls)
    assert all(row.all_order_three_quarter_proved for row in controls)


def test_report_preserves_all_n_access_and_speedup_gates() -> None:
    report = run_natural_frobenius_word_map()
    assert report.theorem.theorem_verified
    assert report.claim_gate["regular_word_collision_formula_proved"]
    assert report.claim_gate["all_order_three_quarter_range_overlap_proved"]
    assert report.claim_gate["all_n_natural_frobenius_contraction_proved"]
    assert report.claim_gate["physical_source_typical_bad_mass_vanishes_proved"]
    assert not report.claim_gate["physical_input_fourier_domination_proved"]
    assert not report.claim_gate["normalization_one_dense_transform_compiled"]
    assert not report.claim_gate["physical_pgm_decoder_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_artifact(tmp_path) -> None:
    path = tmp_path / "natural-frobenius-word-map.json"
    payload = write_natural_frobenius_word_map_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"]["exact_regular_word_map_reduction_count"] == 1
