import itertools

import pytest

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
    inverse_permutation,
)
from coset_hyperoctahedral_branching_polar_boundary import (
    hyperoctahedral_elements,
)
from coset_hyperoctahedral_free_orbit_canonicalization_boundary import (
    canonical_plus_cosets,
)
from coset_hyperoctahedral_trimmed_orbit_canonicalizer import (
    apply_transporter_to_tuple,
    audit_trimmed_canonicalizer,
    build_trimmed_canonicalizer_report,
    canonicalize_source_tuple,
    canonicalizer_scaling_record,
    transitivity_failure_upper_bound,
    write_trimmed_canonicalizer_report,
)
from coset_hyperoctahedral_trivial_color_mass_no_go import (
    canonical_matching_involution,
)


def test_explicit_transitive_seed_canonicalizer_is_covariant():
    m = 2
    hidden = canonical_matching_involution(m)
    cosets = canonical_plus_cosets(m)
    elements = tuple(item[0] for item in hyperoctahedral_elements(m))
    source_tuple = next(
        source
        for source in itertools.product(cosets, repeat=2)
        if canonicalize_source_tuple(source) is not None
        and sum(
            apply_transporter_to_tuple(source, element, hidden) == source
            for element in elements
        )
        == 1
    )
    result = canonicalize_source_tuple(source_tuple)
    assert result is not None
    assert apply_transporter_to_tuple(
        source_tuple, result.transporter, hidden
    ) == result.canonical_tuple

    element = elements[-1]
    transformed = apply_transporter_to_tuple(source_tuple, element, hidden)
    transformed_result = canonicalize_source_tuple(transformed)
    assert transformed_result is not None
    assert transformed_result.canonical_tuple == result.canonical_tuple
    assert transformed_result.transporter == compose_permutations(
        result.transporter, inverse_permutation(element)
    )


@pytest.mark.parametrize(
    ("half_degree", "copy_count"), ((2, 2), (2, 3), (3, 2))
)
def test_finite_trimmed_canonicalizer_controls(half_degree, copy_count):
    control = audit_trimmed_canonicalizer(
        half_degree, copy_count, maximum_controls=48
    )
    assert control.trimmed_canonicalizer_control_verified
    assert control.free_tuple_control_count > 0
    assert control.successful_free_tuple_count == control.free_tuple_control_count
    assert control.covariance_failure_count == 0
    assert control.reconstruction_failure_count == 0
    assert control.transporter_centralizer_failure_count == 0
    assert control.duplicate_transporter_failure_count == 0
    assert control.maximum_candidate_count > 0


def test_transitive_seed_amplification_and_alternative_success():
    assert transitivity_failure_upper_bound(6) < 0.3
    rows = [
        canonicalizer_scaling_record(m)
        for m in (3, 4, 8, 16, 32, 64, 128)
    ]
    assert all(row.disjoint_seed_pair_count >= 1 for row in rows)
    assert all(row.reversible_trimmed_canonicalizer_polynomial for row in rows)
    assert all(
        row.regular_source_multiplicity_basis_compiled_on_trimmed_mass
        for row in rows
    )
    assert all(not row.matrix_hecke_transfer_compiled for row in rows)
    assert rows[-1].total_trimmed_source_failure_upper_bound < 1e-100
    assert rows[-1].trimmed_alternative_failure_upper_bound < 1e-50

    with pytest.raises(ValueError, match="at least two"):
        transitivity_failure_upper_bound(1)
    with pytest.raises(ValueError, match="at least three"):
        canonicalizer_scaling_record(2)


def test_report_compiles_trimmed_source_basis_not_transfer_polar(tmp_path):
    report = build_trimmed_canonicalizer_report(
        finite_specs=((2, 2), (3, 2)),
        scaling_half_degrees=(3, 4, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.deterministic_polynomial_canonicalizer_proved_on_good_set
    assert report.theorem.unique_transporter_proved_on_free_set
    assert report.theorem.asymptotically_full_source_success_proved
    assert report.theorem.asymptotically_full_alternative_success_proved
    assert report.theorem.reversible_trimmed_source_basis_compiled
    assert not report.theorem.matrix_hecke_transfer_polar_compiled
    assert not report.theorem.hidden_involution_algorithm_constructed
    assert report.claim_gate["trimmed_regular_source_multiplicity_basis_compiled"]
    assert not report.claim_gate["matrix_hecke_transfer_compiled_in_trimmed_basis"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_trimmed_canonicalizer_report(
        tmp_path / "trimmed-canonicalizer.json",
        finite_specs=((2, 2),),
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "trimmed-source-multiplicity-basis-compiled-transfer-polar-open"
    )
    assert payload["headline_metrics"][
        "matrix_hecke_transfer_polar_compiler_count"
    ] == 0
