from self_dual_wreath_physical_orientation_racah_sampling import (
    canonical_sign_orbit_tuple,
    run_physical_orientation_racah_sampling,
    sample_physical_orientation_racah_cmi,
)


def test_sign_orbit_canonicalization_rejects_self_conjugate_or_trimmed_labels() -> None:
    paired = ((4, 1, 1),) * 6
    base, nonself, above = canonical_sign_orbit_tuple(paired, 1)
    assert base == ((3, 1, 1, 1),) * 6
    assert nonself and above
    base, nonself, _above = canonical_sign_orbit_tuple(((3, 2, 1),) * 6, 1)
    assert base is None
    assert nonself is False


def test_exact_s5_sampler_covers_known_physical_average() -> None:
    record = sample_physical_orientation_racah_cmi(5, 12, random_seed=17)
    assert record.exact_finite_retained_physical_cmi_bits is not None
    assert record.exact_cmi_inside_confidence_interval is True
    assert record.exact_mass_inside_confidence_interval is True
    assert record.all_compiled_objects_verified


def test_s6_sampler_records_source_weight_and_nondecisive_interval() -> None:
    record = sample_physical_orientation_racah_cmi(6, 3, random_seed=23)
    assert 0 <= record.sample_mean_retained_physical_cmi_bits <= 1
    assert 0 <= record.sample_retained_paired_mass <= 1
    assert record.cmi_hoeffding_radius_bits > 0.5
    assert record.asymptotic_inference_allowed is False
    assert record.all_compiled_objects_verified


def test_report_keeps_physical_survival_and_speedup_gates_closed() -> None:
    report = run_physical_orientation_racah_sampling()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["full_six_label_sampler_exact_proved"] is True
    assert report.claim_gate["S6_confidence_interval_decisive"] is False
    assert report.claim_gate["physical_average_orientation_cmi_survives_proved"] is False
    assert report.claim_gate["classical_separation_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
