import math
from fractions import Fraction

from representation_obstruction import integer_partitions
from self_dual_wreath_commutator_sector_filter_no_go import cycle_centralizer_size
from self_dual_wreath_plancherel_carrier_contextuality import (
    exact_weighted_commuting_probability,
)
from self_dual_wreath_plancherel_carrier_nonidentity_tail import (
    audit_centralizer_cycle_index,
    centralizer_cycle_type_counts,
    class_pair_commuting_probability,
    class_pair_commuting_upper_bound,
    exact_nonidentity_tail_control,
    run_plancherel_carrier_nonidentity_tail,
    wreath_block_cycle_type_counts,
    write_plancherel_carrier_nonidentity_tail_report,
)


def test_wreath_and_full_centralizer_cycle_indices_normalize() -> None:
    for cycle_length in range(1, 6):
        for multiplicity in range(1, 5):
            counts = wreath_block_cycle_type_counts(cycle_length, multiplicity)
            assert sum(counts.values()) == (
                cycle_length**multiplicity * math.factorial(multiplicity)
            )
    for n in range(2, 10):
        for cycle_type in integer_partitions(n):
            assert sum(centralizer_cycle_type_counts(cycle_type).values()) == (
                cycle_centralizer_size(cycle_type)
            )


def test_cycle_index_matches_brute_centralizers_and_pair_bounds() -> None:
    for n in range(2, 8):
        audit = audit_centralizer_cycle_index(n)
        assert audit.exact_cycle_index_verified is True
        assert audit.maximum_cycle_type_count_residual == 0
        assert audit.maximum_commuting_kernel_symmetry_residual == "0"
        assert audit.maximum_support_invariance_bound_violation == "0"


def test_exact_cycle_index_reproduces_factorial_enumeration() -> None:
    for n in range(2, 9):
        control = exact_nonidentity_tail_control(
            n,
            support_cutoffs=tuple(cutoff for cutoff in (2, 4, 6) if cutoff <= n),
        )
        assert Fraction(control.exact_weighted_commuting_probability) == (
            exact_weighted_commuting_probability(n)
        )
        assert control.exact_identity_tail_decomposition_verified is True


def test_nonidentity_tail_identity_decomposition_is_exact() -> None:
    control = exact_nonidentity_tail_control(3, support_cutoffs=(2, 3))
    assert control.exact_identity_atom == "1/2"
    assert control.exact_identity_pair_contribution == "3/4"
    assert control.exact_weighted_commuting_probability == "47/54"
    assert control.exact_nonidentity_conditional_commuting_probability == "13/27"
    assert control.exact_identity_tail_decomposition_verified is True


def test_class_pair_kernel_is_symmetric_and_bounded() -> None:
    n = 8
    partitions = tuple(integer_partitions(n))
    for left in partitions:
        for right in partitions:
            probability = class_pair_commuting_probability(left, right)
            assert probability == class_pair_commuting_probability(right, left)
            assert probability <= class_pair_commuting_upper_bound(left, right)


def test_class_atom_and_support_tail_controls_remain_proof_gated() -> None:
    control = exact_nonidentity_tail_control(12)
    assert control.class_mass_domination_verified is True
    assert control.maximum_class_mass <= control.maximum_plancherel_atom
    assert control.nonidentity_conditional_commuting_probability < 0.01
    assert all(row.class_atom_domination_verified for row in control.support_cutoffs)
    assert all(
        row.commuting_tail_decomposition_verified for row in control.support_cutoffs
    )
    assert control.support_cutoffs[-1].residual_tail_fraction_captured_by_low_support > 0.85


def test_report_extends_exact_frontier_without_promoting_asymptotics() -> None:
    report = run_plancherel_carrier_nonidentity_tail()
    assert report.headline_metrics[
        "exact_centralizer_wreath_cycle_index_theorem_count"
    ] == 1
    assert report.headline_metrics["largest_exact_weighted_commuting_degree"] == 20
    assert report.headline_metrics[
        "tail_exact_nonidentity_conditional_commuting_probability"
    ] < 0.002
    assert report.claim_gate[
        "identity_commuting_contribution_asymptotically_vanishes_proved"
    ] is True
    assert report.claim_gate[
        "every_sublinear_moved_support_window_asymptotically_vanishes_proved"
    ] is True
    assert report.claim_gate[
        "mesoscopic_macroscopic_commuting_tail_vanishes_proved"
    ] is False
    assert report.claim_gate[
        "weighted_commuting_probability_asymptotically_vanishes_proved"
    ] is False
    assert report.claim_gate["structured_multistar_racah_resolver_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_exact_proof_gated_artifact(tmp_path) -> None:
    payload = write_plancherel_carrier_nonidentity_tail_report(
        path=tmp_path / "nonidentity-tail.json",
        write_registry=False,
        exact_degrees=(3, 6, 10),
    )
    assert payload["headline_metrics"][
        "exact_centralizer_wreath_cycle_index_theorem_count"
    ] == 1
    assert payload["headline_metrics"]["largest_exact_weighted_commuting_degree"] == 10
    assert payload["headline_metrics"][
        "mesoscopic_macroscopic_tail_vanishing_theorem_count"
    ] == 0
    assert len(payload["falsifiers_triggered"]) >= 5
