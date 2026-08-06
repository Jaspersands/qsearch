from functools import lru_cache

from representation_obstruction import hook_length_dimension
from self_dual_wreath_orientation_pair_angle_spectrum import (
    exact_pair_principal_angle_spectrum,
)
from self_dual_wreath_transport_carrier_mass import (
    run_transport_carrier_mass,
    transport_carrier_mass_record,
)


@lru_cache(maxsize=1)
def _report():
    return run_transport_carrier_mass()


def test_mass_record_matches_exact_pair_spectrum_multiplicities() -> None:
    labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    record = transport_carrier_mass_record(
        3,
        (2, 1),
        labels,
        0,
        5,
    )
    spectrum = exact_pair_principal_angle_spectrum(
        (2, 1),
        labels,
        0,
        5,
    )

    assert record.exact_representation_mass_record
    assert record.carrier_sector_count == len(spectrum) == 1
    assert record.minimum_carrier_dimension == 2
    assert record.weighted_median_carrier_dimension == 2
    assert record.maximum_carrier_dimension == 2
    assert all(
        hook_length_dimension(partition) == 2
        for _, _, partition in spectrum
    )


def test_tail_pair_mass_is_dominated_beyond_quadratic_dimension() -> None:
    tail = _report().scaling_records[-1]

    assert tail.n == 12
    assert tail.copy_count == 29
    assert tail.sampled_intermediate_distance_count > 0
    assert tail.maximum_intermediate_quadratic_dimension_mass_fraction < 1e-6
    assert tail.minimum_intermediate_weighted_median_dimension > tail.n**2
    assert not tail.typical_low_dimension_transport_mass_signal


def test_low_dimension_mass_proxy_declines_across_probe_range() -> None:
    scaling = _report().scaling_records

    assert scaling[-1].maximum_intermediate_quadratic_dimension_mass_fraction < (
        scaling[1].maximum_intermediate_quadratic_dimension_mass_fraction
    )
    assert _report().headline_metrics[
        "finite_low_dimension_mass_decline_signal_count"
    ] == 1


def test_report_does_not_promote_mass_probe_to_lower_bound() -> None:
    report = _report()

    assert report.claim_gate["exact_pair_carrier_mass_records_computed"]
    assert report.claim_gate[
        "typical_pair_mass_low_dimension_route_falsified_in_samples"
    ]
    assert not report.claim_gate["all_n_low_dimension_mass_upper_bound_proved"]
    assert not report.claim_gate[
        "candidate_affine_fiber_carrier_alignment_computed"
    ]
    assert not report.claim_gate[
        "pair_mass_obstruction_is_algorithm_lower_bound"
    ]
    assert not report.claim_gate["polynomial_transport_network_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
