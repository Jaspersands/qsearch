from self_dual_wreath_compressed_racah_coupling_probe import (
    compile_complete_racah_coupling,
)
from self_dual_wreath_plancherel_down_up_racah_tail_reduction import (
    audit_plancherel_down_up_spectrum,
    audit_racah_fourier_tail,
    down_up_tail_scaling_record,
    run_plancherel_down_up_racah_tail_reduction,
)


def test_down_up_chain_has_exact_character_spectrum() -> None:
    row = audit_plancherel_down_up_spectrum(8, 2)
    assert row.maximum_row_sum_residual < 1e-11
    assert row.maximum_detailed_balance_residual < 1e-11
    assert row.maximum_character_eigenfunction_residual < 1e-10
    assert row.smallest_nonzero_moved_support == 2
    assert row.exact_down_up_spectrum_verified


def test_dirichlet_form_controls_identity_coupling_projector_tail() -> None:
    row = audit_racah_fourier_tail(8, 2, 3)
    assert row.omitted_fourier_tail_energy > 0
    assert row.dirichlet_tail_upper >= row.omitted_fourier_tail_energy - 1e-9
    assert row.direct_parseval_residual < 1e-8
    assert row.cutoff_bound_verified


def test_selected_natural_racah_coupling_obeys_exact_tail_bound() -> None:
    source = (3, 2, 1)
    coupling = compile_complete_racah_coupling((source,) * 4)
    row = audit_racah_fourier_tail(6, 2, 3, coupling=coupling)
    assert row.model == "selected-natural-racah-coupling"
    assert row.omitted_fourier_tail_energy >= -1e-8
    assert row.dirichlet_tail_upper >= row.omitted_fourier_tail_energy - 1e-8
    assert row.cutoff_bound_verified


def test_mesoscopic_box_choice_gives_constant_tail_gap() -> None:
    row = down_up_tail_scaling_record(10_000, 100)
    assert row.constant_gap_verified
    assert row.exact_cutoff_spectral_gap >= 1.0 - 2.718281828459045**-1
    assert row.mesoscopic_tail_amplification < 2.0
    assert row.one_box_tail_amplification > 90.0


def test_report_keeps_natural_stability_and_speedup_gates_closed() -> None:
    report = run_plancherel_down_up_racah_tail_reduction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["projector_tail_dirichlet_reduction_proved"] is True
    assert report.claim_gate["natural_racah_mesoscopic_branching_stability_proved"] is False
    assert report.claim_gate["natural_racah_mutual_information_sublogarithmic_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
