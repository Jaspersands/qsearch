import math
from fractions import Fraction

import numpy as np

from self_dual_wreath_affine_plane_scalar_holonomy import (
    PAIRINGS,
    audit_canonical_pairing_gram,
    audit_scalar_affine_plane_channel,
    canonical_pairing_vector,
    exact_canonical_pairing_gram,
    run_affine_plane_scalar_holonomy,
)


def test_three_canonical_pairings_have_positive_inverse_dimension_overlap() -> None:
    for dimension in range(1, 7):
        vectors = tuple(
            canonical_pairing_vector(dimension, matching)
            for matching in PAIRINGS
        )
        gram = exact_canonical_pairing_gram(dimension)
        for left in range(3):
            for right in range(3):
                assert math.isclose(
                    float(vectors[left] @ vectors[right]),
                    float(gram[left][right]),
                    abs_tol=1e-12,
                )
                assert gram[left][right] == (
                    Fraction(1)
                    if left == right
                    else Fraction(1, dimension)
                )
        assert audit_canonical_pairing_gram(
            dimension
        ).exact_positive_pairing_gram_verified


def test_two_carrier_scalar_channel_normalizes_to_positive_j3_blocks() -> None:
    for cluster, companion, multiplicity in (
        (2, 3, 1),
        (5, 9, 4),
        (10, 16, 7),
    ):
        record = audit_scalar_affine_plane_channel(
            cluster,
            companion,
            multiplicity,
        )
        assert Fraction(record.correlation) == Fraction(
            1,
            cluster * companion,
        )
        assert record.normalized_gram_rank == multiplicity
        assert record.expected_normalized_gram_rank == multiplicity
        assert np.isclose(record.triangle_holonomy, 1.0)
        assert record.negative_holonomy_excluded
        assert record.exact_scalar_affine_plane_flatness_verified
        assert record.normalized_gram_distinct_eigenvalues == (0.0, 3.0)


def test_report_isolates_matrix_multiplicity_boundary() -> None:
    report = run_affine_plane_scalar_holonomy()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "multiplicity_scalar_affine_plane_holonomy_positive"
    ]
    assert report.claim_gate["negative_scalar_simplex_phase_excluded"]
    assert not report.claim_gate[
        "all_n_natural_channels_multiplicity_scalar"
    ]
    assert not report.claim_gate["distinct_affine_plane_supports_commute"]
    assert not report.claim_gate["matrix_6j_holonomy_controlled"]
    assert not report.claim_gate["global_carrier_groupoid_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
