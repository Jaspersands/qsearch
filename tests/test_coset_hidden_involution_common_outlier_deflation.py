import math

import pytest

from coset_hidden_involution_common_outlier_deflation import (
    audit_normal_closure,
    build_common_outlier_deflation_report,
    common_outlier_scaling_record,
    expected_normal_closure_index,
    generated_subgroup,
    permutation_parity,
    write_common_outlier_deflation_report,
)


def test_parity_and_generated_subgroup_helpers():
    transposition = (1, 0, 2)
    three_cycle = (1, 2, 0)
    assert permutation_parity(transposition) == -1
    assert permutation_parity(three_cycle) == 1
    assert len(generated_subgroup(3, (transposition, three_cycle))) == 6

    with pytest.raises(ValueError, match="nonempty"):
        generated_subgroup(3, ())
    with pytest.raises(ValueError, match="n>=5"):
        expected_normal_closure_index(4, 1)


@pytest.mark.parametrize(
    ("n", "transpositions", "expected_index"),
    ((5, 1, 1), (5, 2, 2), (6, 3, 1)),
)
def test_exact_normal_closure_controls(n, transpositions, expected_index):
    row = audit_normal_closure(n, transpositions)
    assert row.exact_normal_closure_verified
    assert row.generated_subgroup_index == expected_index
    assert row.expected_normal_closure_index == expected_index
    assert row.generated_subgroup_order * expected_index == math.factorial(n)
    assert row.involution_parity == (-1 if transpositions % 2 else 1)


def test_common_outlier_is_coherently_visible_but_naturally_negligible():
    rows = [common_outlier_scaling_record(n) for n in (6, 8, 16, 32, 64)]
    assert rows[0].normal_closure == "S_n"
    assert rows[0].normal_closure_index == 1
    assert rows[1].normal_closure == "A_n"
    assert rows[1].normal_closure_index == 2
    assert all(row.coherent_common_outlier_flag_available for row in rows)
    assert all(row.common_alternative_mass_log2 < -20 for row in rows)
    assert all(
        row.common_centered_variance_fraction_log2_upper_bound < -20
        for row in rows
    )
    assert all(
        not row.common_outlier_deflation_removes_non_negligible_signal
        for row in rows
    )
    assert all(not row.post_deflation_operator_norm_bounded for row in rows)

    with pytest.raises(ValueError, match="even"):
        common_outlier_scaling_record(7)


def test_report_deflates_only_the_universal_intersection(tmp_path):
    report = build_common_outlier_deflation_report(
        finite_specs=((5, 1), (5, 2), (6, 3)),
        scaling_n_values=(6, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.common_intersection_proved
    assert report.theorem.exact_normal_closure_proved
    assert report.theorem.common_outlier_eigenvalue_proved
    assert report.theorem.coherent_trivial_sign_deflation_available
    assert report.theorem.common_outlier_natural_mass_negligible
    assert not report.theorem.post_deflation_operator_norm_bound_proved
    assert not report.theorem.polar_label_erasure_compiled
    assert report.claim_gate[
        "common_eigenvalue_M_outlier_coherently_deflatable"
    ]
    assert not report.claim_gate["post_common_deflation_operator_norm_bounded"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_common_outlier_deflation_report(
        tmp_path / "common-outlier.json",
        finite_specs=((5, 1), (6, 3)),
        scaling_n_values=(6, 8),
    )
    assert payload["status"] == (
        "common-outlier-deflation-compiled-post-deflation-spectrum-open"
    )
    assert payload["headline_metrics"][
        "coherent_common_outlier_deflation_count"
    ] == 1
