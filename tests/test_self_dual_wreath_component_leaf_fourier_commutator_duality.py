import math

import pytest

from self_dual_wreath_component_leaf_fourier_commutator_duality import (
    _pair_cell_counts,
    _pair_multinomial,
    _pair_representative,
    audit_fourier_commutator_duality,
    fourier_commutator_duality_theorem,
    fourier_commutator_scaling_record,
    run_component_leaf_fourier_commutator_duality,
)
from self_dual_wreath_component_leaf_fourier_leverage import (
    _coarse_pvm,
    _uniform_povm,
)
from self_dual_wreath_component_leaf_fourier_strata import _haar_block_povm


def test_pair_cells_reconstruct_orbit_and_multinomial_count() -> None:
    counts = _pair_cell_counts(0b10110, 0b01101, 5)
    representative = _pair_representative(counts)
    assert _pair_cell_counts(*representative, 5) == counts
    assert _pair_multinomial(counts) >= 1


def test_uniform_and_projection_valued_controls_have_zero_dual_gap() -> None:
    for control_id, effects in (
        ("UNIFORM", _uniform_povm(3, 3)),
        ("PVM", _coarse_pvm(3, 2)),
    ):
        row = audit_fourier_commutator_duality(
            control_id,
            "commuting",
            effects,
        )
        assert row.exact_fourier_commutator_duality_verified
        assert row.direct_normalized_component_M4 == pytest.approx(0.0, abs=1e-12)
        assert row.fourier_dual_normalized_component_M4 == pytest.approx(
            0.0, abs=1e-12
        )
        assert not row.positive_component_M4_in_control


def test_noncommutative_haar_control_has_positive_dual_gap() -> None:
    row = audit_fourier_commutator_duality(
        "HAAR",
        "haar-block",
        _haar_block_povm(3, 2, 5, seed=71),
    )
    assert row.exact_fourier_commutator_duality_verified
    assert row.direct_normalized_component_M4 > 0
    assert row.fourier_dual_normalized_component_M4 == pytest.approx(
        row.direct_normalized_component_M4
    )
    assert row.strata_reconstructed_normalized_component_M4 == pytest.approx(
        row.direct_normalized_component_M4
    )
    assert row.maximum_negative_fourier_pair_gap < 1e-12
    assert row.positive_component_M4_in_control


def test_pair_strata_are_cubic_in_cube_dimension() -> None:
    row = fourier_commutator_scaling_record(128)
    assert row.leaf_pair_count_log2 == 256
    assert row.exact_pair_stratum_count == math.comb(131, 3)
    assert row.pair_stratum_polynomial_degree == 3
    assert row.log2_pair_stratum_count < 32
    assert row.typical_four_cell_mass_lower_bound > 0.99
    assert row.constant_typical_stratum_gap_would_prove_constant_M4
    assert not row.natural_typical_parity_gap_proved


def test_invalid_pair_counts_and_cube_dimension_are_rejected() -> None:
    with pytest.raises(ValueError, match="four"):
        _pair_representative((1, 2))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="positive"):
        fourier_commutator_scaling_record(0)


def test_report_keeps_natural_gap_and_speedup_gates_closed() -> None:
    report = run_component_leaf_fourier_commutator_duality()
    assert report.headline_metrics[
        "component_fourier_commutator_duality_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["component_M4_is_uniform_fourier_pair_gap_average"]
    assert report.claim_gate["fourier_pair_gaps_are_termwise_nonnegative"]
    assert not report.claim_gate[
        "natural_typical_compressed_parity_gap_positive"
    ]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_theorem_identifies_complement_leakage_curl() -> None:
    theorem = fourier_commutator_duality_theorem()
    assert theorem.theorem_verified
    assert theorem.arbitrary_hermitian_povm
    assert "I-P" in theorem.parity_leakage_curl
    assert "binom(m+3,3)" in theorem.annealed_stratum_count
