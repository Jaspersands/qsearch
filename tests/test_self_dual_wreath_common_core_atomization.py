import numpy as np

from self_dual_wreath_common_core_atomization import (
    _finite_controls,
    _relative_pair_spectrum,
    atom_left_effect_eigenvalue,
    fixed_family_common_range_basis,
    is_affine_orientation_support,
    mobius_common_core_atoms,
    run_common_core_atomization,
    scalar_star_relative_spectrum,
    ternary_affine_closure_mask,
)


TRIPLE_CORE_LABELS = (
    ((6,), (2, 1, 1, 1, 1)),
    ((5, 1), (1, 1, 1, 1, 1, 1)),
    ((4, 2), (2, 2, 2)),
    ((3, 3), (2, 2, 1, 1)),
)


def test_parity_intertwiner_basis_realizes_fixed_family_rank() -> None:
    basis = fixed_family_common_range_basis(
        (6,),
        TRIPLE_CORE_LABELS,
        (5, 6, 9, 10),
    )

    assert basis.shape == (50_625, 1)
    assert np.linalg.norm(basis.conj().T @ basis - np.eye(1)) < 1e-10


def test_higher_common_core_mobius_atoms_are_affinely_balanced() -> None:
    control = _finite_controls()[1]
    atoms = {
        atom.support_orientation_masks: atom.multiplicity
        for atom in control.atoms
    }

    assert atoms == {
        (5, 6): 80,
        (5, 10): 1,
        (6, 9): 4,
        (6, 10): 24,
        (9, 10): 24,
        (5, 6, 9, 10): 1,
    }
    assert control.nonzero_higher_common_core_count == 5
    assert control.pair_core_projectors_commute
    assert control.boolean_atomization_verified
    assert control.crossing_atom_count == 4
    assert control.imbalanced_crossing_atom_count == 0
    assert control.ternary_affine_closure_validation_count == 4
    assert control.ternary_affine_closure_dimension_mismatch_count == 0
    assert control.nonaffine_positive_mobius_atom_count == 0
    assert all(
        is_affine_orientation_support(atom.support_orientation_masks)
        for atom in control.atoms
        if atom.multiplicity > 0
    )


def test_ternary_xor_closes_every_triple_in_affine_plane() -> None:
    plane = (5, 6, 9, 10)

    for omitted in plane:
        triple = tuple(mask for mask in plane if mask != omitted)
        assert ternary_affine_closure_mask(*triple) == omitted


def test_atom_spectrum_matches_direct_relative_cech_quotient() -> None:
    no_higher, higher, _ = _finite_controls()

    assert no_higher.predicted_relative_pair_class_dimension == 11
    assert no_higher.direct_relative_pair_class_dimension == 11
    assert higher.predicted_relative_pair_class_dimension == 30
    assert higher.direct_relative_pair_class_dimension == 30
    assert no_higher.maximum_predicted_spectrum_residual < 1e-10
    assert higher.maximum_predicted_spectrum_residual < 1e-10
    assert max(
        abs(value - 0.5)
        for value in no_higher.direct_fractional_eigenvalues
    ) < 1e-10
    assert max(abs(value - 0.5) for value in higher.direct_fractional_eigenvalues) < 1e-10


def test_collision_free_noncommuting_pair_cores_falsify_half_balance() -> None:
    counterexample = _finite_controls()[2]

    assert counterexample.direct_relative_cech_audit_verified
    assert counterexample.pair_relations_equal_full_internal_kernels
    assert counterexample.nonneutral_full_merge_certified
    assert not counterexample.pair_core_projectors_commute
    assert not counterexample.boolean_atomization_verified
    assert counterexample.all_crossing_atoms_balanced
    assert counterexample.direct_relative_pair_class_dimension == 34
    assert abs(
        counterexample.maximum_pair_core_projector_commutator_norm
        - 0.11042310999998978
    ) < 1e-10
    assert abs(min(counterexample.direct_fractional_eigenvalues) - 8 / 17) < 1e-10
    assert abs(max(counterexample.direct_fractional_eigenvalues) - 89 / 170) < 1e-10
    assert counterexample.maximum_direct_fractional_half_residual > 0.02


def test_scalar_star_formula_explains_noncommuting_counterexample() -> None:
    predicted = scalar_star_relative_spectrum(1 / 9, 9, 16)
    direct = _finite_controls()[2].direct_fractional_eigenvalues

    assert len(predicted) == 34
    assert np.allclose(predicted, direct)
    assert predicted.count(8 / 17) == 9
    assert predicted.count(0.5) == 16
    assert predicted.count(89 / 170) == 9


def test_one_versus_two_atom_support_produces_one_third_channel() -> None:
    atom_basis = np.ones((1, 1))
    pair_bases = {
        (0, 1): atom_basis,
        (0, 2): atom_basis,
        (1, 2): atom_basis,
    }
    spectrum, dimension, defect = _relative_pair_spectrum(
        pair_bases,
        (0,),
        (1, 2),
        1e-10,
    )

    assert atom_left_effect_eigenvalue((0, 1, 2), (0,), (1, 2)) == 1 / 3
    assert dimension == 1
    assert np.allclose(spectrum, [1 / 3])
    assert abs(defect - 1 / 3) < 1e-12


def test_negative_mobius_coefficient_rejects_boolean_atomization() -> None:
    atoms = mobius_common_core_atoms(
        (0, 1, 2),
        {
            (0, 1): 0,
            (0, 2): 0,
            (1, 2): 0,
            (0, 1, 2): 1,
        },
    )

    assert atoms[(0, 1, 2)] == 1
    assert atoms[(0, 1)] == -1
    assert atoms[(0, 2)] == -1
    assert atoms[(1, 2)] == -1


def test_report_keeps_all_n_commutativity_and_balance_open() -> None:
    report = run_common_core_atomization()

    assert report.headline_metrics[
        "finite_direct_relative_cech_validation_failure_count"
    ] == 0
    assert report.headline_metrics[
        "finite_nonneutral_common_core_control_count"
    ] == 1
    assert report.claim_gate[
        "finite_higher_common_core_affine_balance_verified"
    ]
    assert not report.claim_gate["pair_generation_alone_sufficient_for_balance"]
    assert report.claim_gate[
        "ternary_xor_common_range_closure_proved_n_at_least_five"
    ]
    assert report.claim_gate["common_vector_orientation_support_affine_proved"]
    assert report.claim_gate[
        "commuting_common_atoms_affine_sibling_balanced_proved"
    ]
    assert report.claim_gate[
        "universal_collision_free_pair_core_commutativity_falsified"
    ]
    assert report.claim_gate["universal_collision_free_half_balance_falsified"]
    assert report.claim_gate[
        "collision_free_full_affine_merge_half_balance_falsified"
    ]
    assert not report.claim_gate["all_n_pair_core_commutativity_proved"]
    assert report.claim_gate["all_depth_affine_atom_balance_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
