import json
from fractions import Fraction

from self_dual_wreath_split_sector_branch_regularity import (
    audit_refined_alternating_plancherel,
    audit_split_sector_fixed_space,
    branch_swap_orbit_is_free,
    refined_alternating_plancherel_atoms,
    run_split_sector_branch_regularity,
    split_sector_branch_theorem,
    write_split_sector_branch_regularity_report,
)


def test_refined_restriction_is_exact_alternating_plancherel() -> None:
    atoms = refined_alternating_plancherel_atoms(8)
    assert sum(Fraction(atom.exact_weight) for atom in atoms) == 1
    assert any(atom.self_conjugate for atom in atoms)
    assert all(
        atom.alternating_dimension * (2 if atom.self_conjugate else 1)
        == atom.symmetric_dimension
        for atom in atoms
    )


def test_split_constituents_are_fair_and_collision_is_constant_factor() -> None:
    control = audit_refined_alternating_plancherel(12)
    assert control.exact_restriction_plancherel_identity_verified
    assert control.split_constituents_exactly_fair_verified
    assert control.collision_constant_factor_bound_verified
    assert control.exact_refined_alternating_collision_probability == (
        control.exact_predicted_refined_collision_probability
    )
    assert 0.5 <= control.refined_to_symmetric_collision_ratio <= 2.0


def test_pair_swap_branch_orbit_only_needs_within_pair_distinctness() -> None:
    assert branch_swap_orbit_is_free(("a+", "b", "c-", "d"))
    assert not branch_swap_orbit_is_free(("a+", "a+", "c-", "d"))


def test_self_conjugate_projector_is_alternating_plus_odd_parity() -> None:
    control = audit_split_sector_fixed_space(
        "S3-SPLIT",
        (2, 1),
        (((3,), (2, 1)),),
    )
    assert control.self_conjugate_coordinate_count >= 1
    assert control.exact_split_sector_projector_factorization_verified
    assert control.maximum_symmetric_from_alternating_factorization_residual < 1e-9


def test_split_reassembly_leaves_original_cs_polar() -> None:
    control = audit_split_sector_fixed_space(
        "S4-SPLIT",
        (2, 2),
        (
            ((4,), (2, 2)),
            ((3, 1), (2, 1, 1)),
        ),
    )
    assert control.self_conjugate_coordinate_count >= 2
    assert control.exact_branch_fixed_space_boundary_verified
    assert control.branch_cross_gram_residual < 1e-9
    assert control.branch_cross_polar_residual < 1e-7


def test_report_removes_absence_premise_but_not_dense_gate() -> None:
    theorem = split_sector_branch_theorem()
    report = run_split_sector_branch_regularity()
    assert theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert not report.claim_gate[
        "self_conjugate_absence_required_for_free_branch_orbit"
    ]
    assert report.claim_gate[
        "physical_native_refined_source_marginal_is_product_An_plancherel"
    ]
    assert report.claim_gate[
        "natural_pair_swap_branch_action_asymptotically_free"
    ]
    assert not report.claim_gate["full_connected_group_clifford_transform_compiled"]
    assert not report.claim_gate["dense_matrix_cs_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_preserves_split_scope(tmp_path) -> None:
    path = tmp_path / "split-sector-branch.json"
    payload = write_split_sector_branch_regularity_report(path)
    loaded = json.loads(path.read_text())
    assert loaded == payload
    assert loaded["headline_metrics"][
        "self_conjugate_safe_free_branch_orbit_theorem_count"
    ] == 1
    assert loaded["headline_metrics"]["dense_matrix_cs_polar_compiler_count"] == 0
    assert loaded["headline_metrics"]["new_quantum_algorithm_count"] == 0
