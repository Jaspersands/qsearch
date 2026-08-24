import itertools
import json
import math

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_branch_character_gpe_dilation_separation import (
    GAMMA,
    audit_cyclic_overlaps,
    audit_order_four_probability,
    audit_raw_polar_local,
    cyclic_raw_polar_overlap,
    cyclic_raw_polar_overlap_closed_form,
    gpe_separation_scaling,
    raw_branch_isometry,
    raw_representation_dilation,
    run_gpe_dilation_separation,
    write_gpe_dilation_separation_report,
)
from self_dual_wreath_branch_character_polar_naimark_completion import (
    local_polar_naimark_data,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


def _order(permutation: tuple[int, ...]) -> int:
    seen = set()
    output = 1
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        output = math.lcm(output, length)
    return output


def test_raw_stack_has_the_exact_controlled_representation_dilation() -> None:
    controls = (
        ((3,), (2, 1), (1, 2, 0)),
        ((3, 1), (2, 2), (1, 2, 3, 0)),
    )
    for left, right, permutation in controls:
        raw = raw_branch_isometry(left, right, permutation)
        dilation = raw_representation_dilation(left, right, permutation)
        assert np.linalg.norm(raw - dilation, ord=2) < 1e-10
        assert np.linalg.norm(raw.conj().T @ raw - np.eye(raw.shape[1])) < 1e-10


def test_order_four_is_exceptional_but_order_three_separates() -> None:
    order_four = audit_raw_polar_local(
        "order-four",
        (3, 1),
        (2, 2),
        (1, 2, 3, 0),
    )
    order_three = audit_raw_polar_local(
        "order-three",
        (3, 1),
        (2, 2),
        (1, 2, 0, 3),
    )
    assert order_four.raw_and_polar_fields_equal
    assert math.isclose(order_four.raw_to_polar_normalized_overlap, 1.0)
    assert not order_three.raw_and_polar_fields_equal
    assert order_three.raw_to_polar_normalized_overlap < 1.0


def test_cyclic_overlap_closed_forms_and_universal_gamma() -> None:
    for order in range(1, 257):
        assert math.isclose(
            cyclic_raw_polar_overlap(order),
            cyclic_raw_polar_overlap_closed_form(order),
            rel_tol=1e-11,
            abs_tol=1e-11,
        )
    audit = audit_cyclic_overlaps()
    assert audit.exceptional_equal_orders == (1, 2, 4)
    assert audit.universal_nonexceptional_bound_verified
    assert math.isclose(audit.maximum_nonexceptional_overlap, GAMMA)
    assert audit.maximizing_nonexceptional_order in (3, 6)


def test_two_plancherel_average_equals_regular_cyclic_overlap() -> None:
    n = 3
    group = tuple(_source_representation_rows((n,)))
    partitions = tuple(integer_partitions(n))
    factorial = math.factorial(n)
    weights = {
        partition: hook_length_dimension(partition) ** 2 / factorial
        for partition in partitions
    }
    per_group = []
    for permutation in group:
        average = 0.0
        for left in partitions:
            for right in partitions:
                raw = raw_branch_isometry(left, right, permutation)
                polar = local_polar_naimark_data(left, right, permutation)[-1]
                overlap = float(
                    np.trace(raw.conj().T @ polar).real / raw.shape[1]
                )
                average += weights[left] * weights[right] * overlap
        expected = cyclic_raw_polar_overlap(_order(permutation))
        assert math.isclose(average, expected, rel_tol=1e-9, abs_tol=1e-9)
        per_group.append(average)
    direct_two_copy = sum(value**2 for value in per_group) / len(group)
    reduced_two_copy = sum(
        cyclic_raw_polar_overlap(_order(permutation)) ** 2
        for permutation in group
    ) / len(group)
    assert math.isclose(direct_two_copy, reduced_two_copy, rel_tol=1e-9)


def test_order_dividing_four_probability_obeys_cycle_moment_bound() -> None:
    for n in range(2, 9):
        control = audit_order_four_probability(n)
        assert control.exact_probability_below_bound
        exact = sum(
            4 % _order(permutation) == 0
            for permutation in itertools.permutations(range(n))
        ) / math.factorial(n)
        assert math.isclose(
            control.exact_order_dividing_four_probability,
            exact,
        )


def test_natural_scaling_rejects_raw_substitution_and_generic_qsvt() -> None:
    rows = [gpe_separation_scaling(n) for n in (32, 64, 128, 256)]
    assert all(row.raw_gpe_substitution_asymptotically_rejected for row in rows)
    assert all(row.generic_controlled_field_qsvt_superpolynomial for row in rows)
    assert all(
        right.total_annealed_overlap_upper_bound
        < left.total_annealed_overlap_upper_bound
        for left, right in zip(rows, rows[1:])
    )
    assert rows[-1].normalized_frobenius_distance_squared_lower_bound > 1.99


def test_report_keeps_direct_equivariant_transform_and_speedup_open() -> None:
    report = run_gpe_dilation_separation()
    assert report.theorem.theorem_verified
    assert report.claim_gate["raw_character_representation_dilation_proved"]
    assert report.claim_gate["raw_gpe_substitution_rejected"]
    assert report.claim_gate[
        "generic_controlled_field_lcu_qsvt_superpolynomial_proved"
    ]
    assert not report.claim_gate[
        "conjugation_equivariant_multiplier_normal_form_derived"
    ]
    assert not report.claim_gate["direct_equivariant_multiplier_compiled"]
    assert not report.claim_gate["physical_decoder_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_artifact(tmp_path) -> None:
    path = tmp_path / "gpe-dilation-separation.json"
    payload = write_gpe_dilation_separation_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"]["natural_raw_polar_separation_theorem_count"] == 1
