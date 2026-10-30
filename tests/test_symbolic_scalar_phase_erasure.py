"""Tests for sparse symbolic-scalar phase erasure and certified class descent."""
from __future__ import annotations

from itertools import product
import random

import numpy as np
import pytest

from tests.test_class_four_matrix_source import forms3, symbolic_transcript
from tests.test_metabelian_phase_extension import ClassFourFixture, _matrix_coordinates
from tests.test_ut5_matrix_phase_alignment import batch as ut5_batch
from theorems.class_four_scalar_phase_compiler import compile_variable_scalar_packet
from theorems.symbolic_scalar_phase_erasure import (
    CertifiedClassDescentReport,
    PinnedSymbolicPacket,
    PublicLieAlgebra,
    _fmpz_nullspace_basis,
    _fmpz_solve_coordinates,
    build_symbolic_scalar_phase_erasure_report,
    certified_class_descent_controller,
    certified_class_descent_step,
    pin_symbolic_packet,
    rank_batch_size,
    sparse_cancellation_weights,
    sparse_degree_erasure_stage,
    sparse_leading_columns,
    sparse_translate_combine,
    verify_diagonal_witness,
)
from theorems.ut5_matrix_phase_alignment import align_public_jets
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket, compile_scalar_packet


def _make_synthetic_packet(
    p: int,
    q_width: int,
    j_width: int,
    seed: int,
    *,
    instance_id: str = "inst-1",
    chart_id: str = "chart-0",
    max_degree: int = 3,
) -> PinnedSymbolicPacket:
    rng = random.Random(seed)
    basis = ((0, (1, 0)), (0, (2, 0)), (1, (1, 1)), (2, (3, 0)))
    width = q_width + j_width
    candidate_alphas = [
        alpha
        for alpha in product(range(max_degree + 1), repeat=width)
        if 1 <= sum(alpha) <= max_degree
    ]
    candidate_params = [(0,), (1,), (0, 1), (1, 2), (2, 3)]
    terms: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    for alpha in candidate_alphas:
        for params in candidate_params[:2]:
            coeff = rng.randrange(1, p)
            terms[(alpha, params)] = coeff
    pkt = SymbolicScalarPacket(p, q_width, j_width, basis, terms)
    return pin_symbolic_packet(pkt, instance_id=instance_id, chart_id=chart_id)


def test_sparse_controller_never_calls_evaluate_fixture(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("hidden truth evaluation called inside sparse controller")

    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    p = 11
    packets = [_make_synthetic_packet(p, 2, 0, 50 + i) for i in range(10)]
    outcomes = [[(i + j) % p for j in range(2)] for i in range(len(packets))]
    merged, weights, rank, eq_count = sparse_degree_erasure_stage(
        packets,
        3,
        outcomes,
        rng=random.Random(19),
    )
    assert any(weights)
    assert rank <= eq_count
    assert merged.degree <= 2
    assert all(pkt.consumed for pkt in packets)
    assert not merged.consumed


def test_sparse_translate_combine_matches_lifted_quadratic_parameter_evaluation() -> None:
    p = 11
    packets = [_make_synthetic_packet(p, 2, 0, 80 + i) for i in range(9)]
    # Keep raw copies for truth comparison after merge consumes originals
    raw_copies = [
        SymbolicScalarPacket(
            pkt.packet.p,
            pkt.packet.quotient_width,
            pkt.packet.jet_width,
            pkt.packet.parameter_basis,
            dict(pkt.packet.terms),
        )
        for pkt in packets
    ]
    outcomes = [[(2 * i + 1) % p, (3 * i + 2) % p] for i in range(len(packets))]
    merged, weights, _, _ = sparse_degree_erasure_stage(
        packets,
        3,
        outcomes,
        rng=random.Random(23),
    )
    assert merged.degree == 2
    rng = random.Random(101)
    for _ in range(5):
        theta = [rng.randrange(p) for _ in merged.packet.parameter_basis]

        def expected_sum(pt: tuple[int, ...]) -> int:
            return sum(
                raw.evaluate_fixture(
                    tuple((y + w * x) % p for y, x in zip(outcome, pt)),
                    theta,
                )
                for raw, w, outcome in zip(raw_copies, weights, outcomes)
            ) % p

        origin = expected_sum((0, 0))
        for pt in product(range(p), repeat=2):
            assert merged.packet.evaluate_fixture(pt, theta) == (expected_sum(pt) - origin) % p


def test_full_three_stage_sparse_symbolic_erasure_reaches_zero_degree() -> None:
    p = 11
    rng = random.Random(2026)
    quad_batch: list[PinnedSymbolicPacket] = []
    for q_idx in range(25):
        cubic_batch = [_make_synthetic_packet(p, 1, 1, 500 * q_idx + i) for i in range(9)]
        outcomes = [[rng.randrange(p), rng.randrange(p)] for _ in cubic_batch]
        q_pkt, _, _, _ = sparse_degree_erasure_stage(cubic_batch, 3, outcomes, rng=rng)
        assert q_pkt.degree <= 2
        quad_batch.append(q_pkt)

    lin_batch: list[PinnedSymbolicPacket] = []
    for l_idx in range(7):
        sub_quad = quad_batch[l_idx * 3 : l_idx * 3 + 3]
        # Pad with fresh degree-2 packets so arity (rank+1)^2 is satisfied
        extra = [
            _make_synthetic_packet(p, 1, 1, 9000 * l_idx + i, max_degree=2)
            for i in range(46)
        ]
        batch2 = sub_quad + extra
        outcomes2 = [[rng.randrange(p), rng.randrange(p)] for _ in batch2]
        l_pkt, _, _, _ = sparse_degree_erasure_stage(batch2, 2, outcomes2, rng=rng)
        assert l_pkt.degree <= 1
        lin_batch.append(l_pkt)

    outcomes1 = [[rng.randrange(p), rng.randrange(p)] for _ in lin_batch]
    root, w1, _, _ = sparse_degree_erasure_stage(lin_batch, 1, outcomes1, rng=rng)
    assert any(w1)
    assert root.degree == 0
    assert root.packet.terms == {}


def test_real_compiler_packets_from_variable_radical_and_ut5_erase_leading_cubic() -> None:
    # 1. Variable-radical compiler packets at p=11 (11 == 2 mod 3 and 3 mod 4)
    p = 11
    forms = forms3(p) + [[[0] * 3 for _ in range(3)]]
    var_packets: list[PinnedSymbolicPacket] = []
    for variant in (0, 1, 2, 0):
        _, labels, scales, outcomes, alignment, alpha, spectator = symbolic_transcript(p, variant)
        pkt = compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes, alpha, spectator)
        var_packets.append(pin_symbolic_packet(pkt, instance_id="var-p11", chart_id="c0"))
    rng = random.Random(77)
    var_outcomes = [[rng.randrange(p) for _ in range(var_packets[0].width)] for _ in var_packets]
    merged_var, weights_var, rank_var, eq_var = sparse_degree_erasure_stage(
        var_packets,
        3,
        var_outcomes,
        rng=rng,
    )
    assert any(weights_var)
    assert eq_var > 0 and rank_var > 0
    assert merged_var.degree <= 2

    # 2. UT5 compiler packets at p=11, r=1, m=1
    u_labels, u_scales, u_outcomes = ut5_batch(p, 1, 1, 17)
    u_align = align_public_jets(p, u_labels, u_scales, u_outcomes)
    u_R, u_D = u_align.maps.carrier_width, u_align.maps.jet_width
    u_pkt1 = compile_scalar_packet(
        u_align,
        u_labels,
        u_scales,
        u_outcomes,
        [[1, 2, 3] for _ in u_labels],
        [0] * (u_R - u_D),
    )
    u_pkt2 = compile_scalar_packet(
        u_align,
        u_labels,
        u_scales,
        u_outcomes,
        [[2, 1, 4] for _ in u_labels],
        [1] * (u_R - u_D),
    )
    u_pinned = [
        pin_symbolic_packet(u_pkt1, instance_id="ut5-p11", chart_id="c0"),
        pin_symbolic_packet(u_pkt2, instance_id="ut5-p11", chart_id="c0"),
        pin_symbolic_packet(u_pkt1, instance_id="ut5-p11", chart_id="c0"),
    ]
    u_merged, u_weights, _, u_eq = sparse_degree_erasure_stage(
        u_pinned,
        3,
        [[rng.randrange(p) for _ in range(u_pkt1.width)] for _ in u_pinned],
        rng=rng,
    )
    assert any(u_weights)
    assert u_eq < u_pkt1.lifted_parameter_count
    assert u_merged.degree <= 2


def test_provenance_pinning_and_consumed_packet_rejection() -> None:
    p = 11
    pkt_a = _make_synthetic_packet(p, 2, 0, 1, instance_id="inst-A", chart_id="chart-0")
    pkt_b_wrong_inst = _make_synthetic_packet(p, 2, 0, 2, instance_id="inst-B", chart_id="chart-0")
    pkt_b_wrong_chart = _make_synthetic_packet(p, 2, 0, 2, instance_id="inst-A", chart_id="chart-1")

    with pytest.raises(ValueError, match="pinned"):
        sparse_leading_columns([pkt_a, pkt_b_wrong_inst], 3)
    with pytest.raises(ValueError, match="pinned"):
        sparse_leading_columns([pkt_a, pkt_b_wrong_chart], 3)

    # Different parameter_basis ordering with identical dimensions must also be rejected
    swapped_basis = tuple(reversed(pkt_a.packet.parameter_basis))
    pkt_swapped = pin_symbolic_packet(
        SymbolicScalarPacket(p, 2, 0, swapped_basis, dict(pkt_a.packet.terms)),
        instance_id="inst-A",
        chart_id="chart-0",
    )
    with pytest.raises(ValueError, match="pinned"):
        sparse_leading_columns([pkt_a, pkt_swapped], 3)

    # Zero-scale input is still consumed and cannot be reused
    pkt_c = _make_synthetic_packet(p, 2, 0, 3, instance_id="inst-A", chart_id="chart-0")
    sparse_translate_combine([pkt_a, pkt_c], [1, 0], [[0, 0], [0, 0]])
    assert pkt_a.consumed and pkt_c.consumed
    fresh = _make_synthetic_packet(p, 2, 0, 4, instance_id="inst-A", chart_id="chart-0")
    with pytest.raises(ValueError, match="consumed"):
        sparse_leading_columns([pkt_c, fresh], 3)


@pytest.mark.parametrize("operation", ["columns", "weights", "merge", "stage"])
def test_same_packet_cannot_supply_two_physical_inputs(operation) -> None:
    packet = _make_synthetic_packet(11, 2, 0, 91)
    batch = [packet, packet]
    with pytest.raises(ValueError, match="distinct packet"):
        if operation == "columns":
            sparse_leading_columns(batch, 3)
        elif operation == "weights":
            sparse_cancellation_weights(batch, 3)
        elif operation == "merge":
            sparse_translate_combine(batch, [1, 0], [[0, 0], [0, 0]])
        else:
            sparse_degree_erasure_stage(batch, 3, [[0, 0], [0, 0]])
    assert not packet.consumed


def test_identical_public_maps_can_describe_distinct_fresh_sources() -> None:
    batch = [_make_synthetic_packet(11, 2, 0, 91) for _ in range(2)]
    merged, weights, _, _ = sparse_degree_erasure_stage(batch, 3, [[0, 0], [0, 0]])
    assert any(weights)
    assert merged.degree < 3
    assert all(packet.consumed for packet in batch)


def test_verify_diagonal_witness_rejects_zero_and_invalid_scales() -> None:
    p = 11
    columns = [(1, 2), (10, 9)]
    verify_diagonal_witness(p, columns, [1, 1], 1)
    with pytest.raises(ArithmeticError, match="all-zero"):
        verify_diagonal_witness(p, columns, [0, 0], 1)
    with pytest.raises(ArithmeticError, match="cancellation failed"):
        verify_diagonal_witness(p, columns, [1, 2], 1)
    with pytest.raises(ValueError, match="length"):
        verify_diagonal_witness(p, columns, [1], 1)


def test_arbitrary_precision_127bit_prime_sparse_quadratic_and_linear_erasure() -> None:
    p = 2**127 - 1  # 127-bit Mersenne prime, p == 3 mod 4
    rng = random.Random(127)
    packets = [
        _make_synthetic_packet(p, 1, 0, 300 + i, max_degree=2)
        for i in range(9)
    ]
    outcomes = [[rng.randrange(p)] for _ in packets]
    merged_lin, weights2, rank2, eq2 = sparse_degree_erasure_stage(
        packets,
        2,
        outcomes,
        rng=rng,
    )
    assert any(weights2)
    assert eq2 == 2 and rank2 <= 2
    assert merged_lin.degree <= 1


def _build_class_four_algebra(group: ClassFourFixture):
    basis_matrices = [group.x, group.y] + group.normal
    dim = len(basis_matrices)

    def coords(mat) -> tuple[int, ...]:
        res = _matrix_coordinates(mat % group.p, basis_matrices, group.p)
        assert res is not None
        return tuple(int(x) % group.p for x in res)

    def mat_from_coords(vec):
        return sum((int(c) * m for c, m in zip(vec, basis_matrices)), group.x * 0) % group.p

    def bracket_fn(left, right):
        return coords(group.bracket(mat_from_coords(left), mat_from_coords(right)))

    algebra = PublicLieAlgebra(p=group.p, dimension=dim, bracket_fn=bracket_fn)
    std_basis = [tuple(int(i == j) for j in range(dim)) for i in range(dim)]
    hidden_vec = coords(group.hidden)

    def original_label(vec: tuple[int, ...]) -> tuple[int, ...]:
        mat = mat_from_coords(vec)
        return min(
            tuple(int(x) for x in (group.exp(mat) @ group.exp(t * group.hidden) % group.p).ravel())
            for t in range(group.p)
        )

    return algebra, std_basis, hidden_vec, coords, original_label


def test_certified_class_descent_controller_recovers_hidden_subgroup() -> None:
    group = ClassFourFixture()
    algebra, std_basis, hidden_vec, _, original_label = _build_class_four_algebra(group)
    rng = random.Random(20261021)

    def quotient_sampler(level, chart_id, normal, section):
        adapted = list(normal) + list(section)
        h_coords = _fmpz_solve_coordinates(adapted, hidden_vec, group.p)
        assert h_coords is not None
        h_image = h_coords[len(normal) :]
        perp = _fmpz_nullspace_basis([h_image], len(section), group.p)
        if not perp:
            return (0,) * len(section)
        coeffs = [rng.randrange(group.p) for _ in perp]
        if not any(coeffs):
            coeffs[0] = 1
        return tuple(
            sum(coeffs[i] * perp[i][j] for i in range(len(perp))) % group.p
            for j in range(len(section))
        )

    def terminal_sampler(chart_id, ambient):
        h_coords = _fmpz_solve_coordinates(ambient, hidden_vec, group.p)
        assert h_coords is not None
        perp = _fmpz_nullspace_basis([h_coords], len(ambient), group.p)
        coeffs = [rng.randrange(group.p) for _ in perp]
        if not any(coeffs):
            coeffs[0] = 1
        return tuple(
            sum(coeffs[i] * perp[i][j] for i in range(len(perp))) % group.p
            for j in range(len(ambient))
        )

    report = certified_class_descent_controller(
        algebra,
        std_basis,
        quotient_fourier_sampler=quotient_sampler,
        terminal_abelian_sampler=terminal_sampler,
        original_oracle_label=original_label,
    )
    assert report.status == "SUCCESS"
    assert report.dimension_trajectory == (8, 7, 4, 2)
    assert report.class_trajectory == (4, 3, 2, 1)
    assert len(set(report.chart_trajectory)) == 4
    assert len(report.recovered_generators) == 1
    assert _fmpz_solve_coordinates(report.recovered_generators, hidden_vec, group.p) is not None
    assert report.ideal_model_certificate_only is True
    assert report.unconditional_noisy_certificate is False
    assert report.accepted_speedup_candidate is False


def test_strict_overestimate_passes_class_drop_and_still_recovers_h() -> None:
    group = ClassFourFixture()
    algebra, std_basis, hidden_vec, coords, original_label = _build_class_four_algebra(group)
    e_vec = coords(group.e)
    quotient_calls = {}

    def overestimate_quotient_sampler(level, chart_id, normal, section):
        adapted = list(normal) + list(section)
        h_coords = _fmpz_solve_coordinates(adapted, hidden_vec, group.p)
        assert h_coords is not None
        h_image = h_coords[len(normal) :]
        if level == 1:
            # At class 3 -> 2, return only annihilators of span(hidden, e),
            # leaving a 2D image overestimate Uhatsupsetneq U whose preimage still has class 2!
            e_coords = _fmpz_solve_coordinates(adapted, e_vec, group.p)
            assert e_coords is not None
            e_image = e_coords[len(normal) :]
            perp = _fmpz_nullspace_basis([h_image, e_image], len(section), group.p)
        else:
            perp = _fmpz_nullspace_basis([h_image], len(section), group.p)
        index = quotient_calls.get(level, 0)
        quotient_calls[level] = index + 1
        return perp[index % len(perp)]

    call_idx = 0

    def terminal_sampler(chart_id, ambient):
        nonlocal call_idx
        h_coords = _fmpz_solve_coordinates(ambient, hidden_vec, group.p)
        assert h_coords is not None
        perp = _fmpz_nullspace_basis([h_coords], len(ambient), group.p)
        row = perp[call_idx % len(perp)]
        call_idx += 1
        return row

    report = certified_class_descent_controller(
        algebra,
        std_basis,
        quotient_fourier_sampler=overestimate_quotient_sampler,
        terminal_abelian_sampler=terminal_sampler,
        original_oracle_label=original_label,
    )
    assert report.status == "SUCCESS"
    assert len(report.steps[1].image_basis) == 2
    assert report.class_trajectory == (4, 3, 2, 1)
    assert _fmpz_solve_coordinates(report.recovered_generators, hidden_vec, group.p) is not None


def test_dimension_only_reduction_and_incomplete_terminal_batch_abort() -> None:
    group = ClassFourFixture()
    algebra, std_basis, hidden_vec, _, original_label = _build_class_four_algebra(group)

    # 1. Zero quotient frequencies fail to drop class and abort after cap
    abort_descent = certified_class_descent_controller(
        algebra,
        std_basis,
        quotient_fourier_sampler=lambda level, chart, normal, section: (0,) * len(section),
        terminal_abelian_sampler=lambda chart, ambient: (0,) * len(ambient),
        original_oracle_label=original_label,
        level_sample_cap=3,
    )
    assert abort_descent.status == "ABORT"
    assert abort_descent.abort_reason == "DESCENT_CLASS_DROP_FAILURE"
    assert abort_descent.fourier_samples_by_level == (3,)

    # 2. Incomplete terminal abelian batch leaves extra non-H direction -> caught by oracle check
    quotient_calls = {}
    def exact_quotient_first(level, chart_id, normal, section):
        adapted = list(normal) + list(section)
        h_coords = _fmpz_solve_coordinates(adapted, hidden_vec, group.p)
        assert h_coords is not None
        perp = _fmpz_nullspace_basis([h_coords[len(normal) :]], len(section), group.p)
        index = quotient_calls.get(level, 0)
        quotient_calls[level] = index + 1
        return perp[index % len(perp)]

    abort_terminal = certified_class_descent_controller(
        algebra,
        std_basis,
        quotient_fourier_sampler=exact_quotient_first,
        terminal_abelian_sampler=lambda chart, ambient: (0,) * len(ambient),
        original_oracle_label=original_label,
        terminal_sample_cap=2,
    )
    assert abort_terminal.status == "ABORT"
    assert abort_terminal.abort_reason == "TERMINAL_ORACLE_MEMBERSHIP_FAILURE"

    # 3. Invalid initial normal intersection K is caught immediately
    wrong_k = [std_basis[0]]
    abort_k = certified_class_descent_controller(
        algebra,
        std_basis,
        quotient_fourier_sampler=exact_quotient_first,
        terminal_abelian_sampler=lambda chart, ambient: (0,) * len(ambient),
        original_oracle_label=original_label,
        initial_normal_intersection=wrong_k,
    )
    assert abort_k.status == "ABORT"
    assert abort_k.abort_reason == "INITIAL_INTERSECTION_MEMBERSHIP_FAILURE"


def test_nonabelian_derived_ideal_is_rejected_in_public_lie_algebra() -> None:
    p = 7
    slots = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    index = {pair: idx for idx, pair in enumerate(slots)}

    def ut5_bracket(left, right):
        a = np.zeros((5, 5), dtype=np.int64)
        b = np.zeros((5, 5), dtype=np.int64)
        for val, (i, j) in zip(left, slots):
            a[i, j] = val
        for val, (i, j) in zip(right, slots):
            b[i, j] = val
        comm = (a @ b - b @ a) % p
        return tuple(int(comm[i, j]) for i, j in slots)

    algebra = PublicLieAlgebra(p=p, dimension=len(slots), bracket_fn=ut5_bracket)
    std_basis = [tuple(int(i == j) for j in range(len(slots))) for i in range(len(slots))]
    with pytest.raises(ValueError, match="abelian derived"):
        certified_class_descent_step(algebra, std_basis, [])


def test_report_builder_matches_documented_invariants() -> None:
    report = build_symbolic_scalar_phase_erasure_report()
    assert report["schema_version"] == "symbolic_scalar_phase_erasure_v1"
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    assert report["certified_class_descent"]["status"] == "SUCCESS"
    assert report["certified_class_descent"]["class_trajectory"] == [4, 3, 2, 1]
    assert report["sparse_erasure_controls"]["three_stage_symbolic_tree_p11"]["erased_root_degree"] == 0
    tree = report["sparse_erasure_controls"]["three_stage_symbolic_tree_p11"]
    assert tree["stage_arities"] == [7, 169, 7]
    assert tree["total_cubic_leaves"] == 8281
    assert tree["reference_descriptors_only"]


def test_general_prime_symbolic_cubic_and_quadratic_erasure_p_1_mod_12(monkeypatch: pytest.MonkeyPatch) -> None:
    from fractions import Fraction
    import theorems.bounded_power_roots as roots
    from theorems.power_sde import power_arity
    from theorems.prime_character_opi import ring

    p = 105037  # verified prime >= 104976 with p == 1 mod 12
    ring(p)
    assert p >= 104976
    assert p % 12 == 1
    assert (p - 1) % 3 == 0

    basis = ((0, (1, 0)), (0, (2, 0)))
    rng = random.Random(20261028)

    # 1. Degree 3 erasure with rank 1 on active cubic keys (power_arity(1, 3) = 6 <= 13 packets)
    cubic_packets: list[PinnedSymbolicPacket] = []
    for i in range(13):
        terms = {
            ((3, 0), (0,)): rng.randrange(1, p),
            ((2, 0), (0,)): rng.randrange(1, p),
            ((1, 0), (1,)): rng.randrange(1, p),
        }
        pkt = SymbolicScalarPacket(p, 2, 0, basis, terms)
        cubic_packets.append(pin_symbolic_packet(pkt, instance_id="gen-prime-cubic", chart_id="c0"))

    outcomes3 = [[rng.randrange(p), rng.randrange(p)] for _ in cubic_packets]
    merged3, weights3, rank3, eq3 = sparse_degree_erasure_stage(
        cubic_packets,
        3,
        outcomes3,
        rng=rng,
        use_general_prime_sde=True,
        bounded_randomness_bits=64,
    )
    assert rank3 == 1
    assert eq3 == 1
    assert any(weights3)
    assert merged3.degree <= 2
    assert all(pkt.consumed for pkt in cubic_packets)
    assert not merged3.consumed

    # 2. Degree 2 erasure with rank 1 on active quadratic keys (power_arity(1, 2) = 4 <= 13 packets)
    quad_packets: list[PinnedSymbolicPacket] = []
    for i in range(13):
        terms = {
            ((2, 0), (0,)): rng.randrange(1, p),
            ((1, 0), (1,)): rng.randrange(1, p),
        }
        pkt = SymbolicScalarPacket(p, 2, 0, basis, terms)
        quad_packets.append(pin_symbolic_packet(pkt, instance_id="gen-prime-quad", chart_id="c0"))

    outcomes2 = [[rng.randrange(p), rng.randrange(p)] for _ in quad_packets]
    merged2, weights2, rank2, eq2 = sparse_degree_erasure_stage(
        quad_packets,
        2,
        outcomes2,
        rng=rng,
        use_general_prime_sde=True,
        bounded_randomness_bits=64,
    )
    assert rank2 == 1
    assert eq2 == 1
    assert any(weights2)
    assert merged2.degree <= 1
    assert all(pkt.consumed for pkt in quad_packets)
    assert not merged2.consumed

    # 3. Test that insufficient columns raises ValueError
    short_packets = [
        pin_symbolic_packet(
            SymbolicScalarPacket(p, 2, 0, basis, {((3, 0), (0,)): 1}),
            instance_id="gen-prime-short",
            chart_id="c0",
        )
        for _ in range(3)  # needed is 6 for rank 1, g=3
    ]
    with pytest.raises(ValueError, match="general-prime SDE controller needs"):
        sparse_degree_erasure_stage(
            short_packets,
            3,
            [[0, 0] for _ in short_packets],
            use_general_prime_sde=True,
            bounded_randomness_bits=64,
        )

    # 4. Test that bounded_randomness_bits=1 raises RuntimeError("bounded root splitting exhausted")
    fail_packets: list[PinnedSymbolicPacket] = []
    for i in range(13):
        terms = {
            ((3, 0), (0,)): rng.randrange(1, p),
            ((2, 0), (0,)): rng.randrange(1, p),
        }
        pkt = SymbolicScalarPacket(p, 2, 0, basis, terms)
        fail_packets.append(pin_symbolic_packet(pkt, instance_id="gen-prime-fail", chart_id="c0"))

    with monkeypatch.context() as m:
        m.setattr(
            roots,
            "bounded_power_root",
            lambda *args, **kwargs: roots.BoundedPowerRoot(None, 1, 0, 3, Fraction(1)),
        )
        with pytest.raises(RuntimeError, match="bounded root splitting exhausted"):
            sparse_degree_erasure_stage(
                fail_packets,
                3,
                outcomes3,
                rng=rng,
                use_general_prime_sde=True,
                bounded_randomness_bits=1,
            )
