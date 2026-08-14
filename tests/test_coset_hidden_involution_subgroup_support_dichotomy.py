import pytest

from coset_hidden_involution_subgroup_support_dichotomy import (
    audit_subgroup_support,
    build_subgroup_support_dichotomy_report,
    index_dichotomy_scaling_record,
    induced_trivial_multiplicities,
    write_subgroup_support_dichotomy_report,
    young_two_block_subgroup,
)


@pytest.mark.parametrize(
    ("family", "half_degree"),
    (("hyperoctahedral", 3), ("hyperoctahedral", 4), ("young-two-block", 4)),
)
def test_exact_induced_support_controls(family, half_degree):
    control = audit_subgroup_support(family, half_degree)
    assert control.exact_induced_multiplicities_integral
    assert control.induced_dimension_identity == control.subgroup_index
    assert control.support_dimension_bound_verified
    assert control.subgroup_outlier_witness_verified
    assert control.noncommon_invariant_dimension > 0


def test_young_subgroup_and_multiplicity_inputs():
    subgroup = young_two_block_subgroup(3)
    assert len(subgroup) == 36
    multiplicities = induced_trivial_multiplicities(6, subgroup)
    assert multiplicities[(6,)] == 1
    assert all(value >= 0 for value in multiplicities.values())
    with pytest.raises(ValueError, match="positive"):
        young_two_block_subgroup(0)
    with pytest.raises(ValueError, match="nonempty"):
        induced_trivial_multiplicities(6, ())


def test_low_index_scaling_dichotomy_is_not_a_universal_compiler():
    rows = [
        index_dichotomy_scaling_record(m, epsilon)
        for m, epsilon in ((8, 0.1), (16, 0.1), (32, 0.05), (64, 0.05))
    ]
    assert all(
        row.low_index_outlier_mass_information_theoretically_negligible
        for row in rows
    )
    assert all(row.support_membership_flag_assumed for row in rows)
    assert all(not row.universal_coherent_trim_compiled for row in rows)
    assert all(not row.high_index_subgroups_classified for row in rows)
    with pytest.raises(ValueError, match="at least three"):
        index_dichotomy_scaling_record(2, 0.1)
    with pytest.raises(ValueError, match=r"\(0, 1/2\)"):
        index_dichotomy_scaling_record(8, 0.5)


def test_report_keeps_high_index_and_membership_obligations_open(tmp_path):
    report = build_subgroup_support_dichotomy_report(
        finite_specs=(("hyperoctahedral", 3), ("young-two-block", 4)),
        scaling_specs=((8, 0.1), (16, 0.1), (32, 0.05)),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_conjugate_support_theorem_proved
    assert report.theorem.general_support_dimension_bound_proved
    assert report.theorem.low_index_all_register_mass_bound_proved
    assert not report.theorem.arbitrary_support_membership_compiled
    assert not report.theorem.high_index_subgroups_classified
    assert not report.theorem.post_all_strata_frame_norm_bounded
    assert report.claim_gate["low_index_subgroup_mass_dichotomy_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_subgroup_support_dichotomy_report(
        tmp_path / "subgroup-dichotomy.json",
        finite_specs=(("hyperoctahedral", 3),),
        scaling_specs=((8, 0.1), (16, 0.1)),
    )
    assert payload["status"] == (
        "subgroup-support-index-dichotomy-proved-high-index-classification-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
