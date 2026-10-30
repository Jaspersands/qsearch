"""Exact public-controller tests and bounded physical source checks only."""
from fractions import Fraction
from itertools import product
from math import comb
import random

import numpy as np
import pytest

from theorems.affine_phase_erasure import PhasePacket, merge_branch, translate_combine
from theorems.phase_copy_statevector_backend import StateVectorPhaseSource
from theorems.polynomial_phase_copy_learning import (
    CopyLedger, LearningFrame, PhaseCopyController, coordinate_copy_envelope,
    coordinate_rank_cap, copy_envelope, erase_line_degree, report,
)
from theorems.ut5_matrix_phase_alignment import _rank


def _poly(frame, coefficients, point):
    return sum(c*np.prod([pow(x, a, frame.p) for x, a in zip(point, alpha)], dtype=object)
               for c, alpha in zip(coefficients, frame.indices)) % frame.p


def _coefficients(frame, eta):
    return tuple((x+sum(a*v[j] for a, v in zip(eta, frame.basis))) % frame.p
                 for j, x in enumerate(frame.known))


def _state(packet, eta):
    return {(x,): np.exp(2j*np.pi*int(packet.evaluate_fixture((x,), eta))/packet.p)
                   /np.sqrt(packet.p) for x in range(packet.p)}


def test_random_measured_line_has_correct_phase_without_chosen_line_access():
    frame = LearningFrame.initial(5, 2, 3)
    eta = tuple(range(5))+(1, 2, 3, 4)
    # Exercise nonzero known correction after a legitimate parameter equation.
    relation = (1, 2)+(0,)*7
    frame = frame.learn_relation(relation, (eta[0]+2*eta[1]) % 5)
    eta = eta[1:]
    coefficients = _coefficients(frame, eta)
    axis = frame.next_axis()
    for y in range(5):
        correction, packet = frame.restrict(axis, (y,))
        actual = []
        for t in range(5):
            point = (t, y) if axis == 0 else (y, t)
            actual.append(np.exp(2j*np.pi*int(_poly(frame, coefficients, point))/5)/5)
        assert sum(abs(x)**2 for x in actual) == pytest.approx(1/5)
        corrected = np.array([a*np.exp(-2j*np.pi*sum(c*pow(t, r, 5)
                               for r, c in enumerate(correction))/5)
                              for t, a in enumerate(actual)])*np.sqrt(5)
        expected = np.array(list(_state(packet, eta).values()))
        assert abs(np.vdot(expected, corrected)) == pytest.approx(1)


def test_line_rejection_bound_is_tight_and_keeps_rejected_copies_charged():
    initial = LearningFrame.initial(5, 2, 3)
    # x0*(x1-1)*(x1-2): coordinate slices y=1,2 carry no unknown coefficient.
    coefficients = {(1, 2): 1, (1, 1): 2, (1, 0): 2}
    row = tuple(coefficients.get(alpha, 0) for alpha in initial.indices)
    frame = LearningFrame(5, 2, 3, initial.known, (row,))
    assert frame.next_axis() == 0
    accepted = sum(frame.restrict(0, (y,))[1].degree > 0 for y in range(5))
    assert Fraction(accepted, 5) == copy_envelope(5, 2, 3)["line_acceptance_lower_bound"]


def test_parameter_substitution_preserves_every_polynomial_coefficient():
    rng = random.Random(915)
    frame = LearningFrame.initial(101, 3, 3)
    original = eta = tuple(rng.randrange(101) for _ in frame.basis)
    while eta:
        relation = tuple(rng.randrange(1, 101) for _ in eta)
        value = sum(a*b for a, b in zip(relation, eta)) % 101
        frame = frame.learn_relation(relation, value)
        eta = eta[1:]
        assert _coefficients(frame, eta) == original
    assert frame.known == original
    with pytest.raises(ValueError, match="no unknown"):
        frame.next_axis()


def test_cubic_instrument_all_records_and_failure_mass():
    packet = PhasePacket(5, 1, 1, {(3,): (1,)})
    state = _state(packet, (2,))
    accepted = 0
    total_mass = 0
    for values in product(range(5), repeat=2):
        outcomes = tuple((v,) for v in values)
        reduced = erase_line_degree([packet, packet], [1, 4], outcomes)
        physical, mass = merge_branch(5, [state, state], [1, 4], outcomes)
        total_mass += mass
        assert mass == pytest.approx(1/25)
        expected = _state(reduced, (2,))
        assert abs(sum(np.conj(expected[x])*physical[x] for x in expected)) == pytest.approx(1)
        accepted += bool(reduced.degree)
    assert total_mass == pytest.approx(1)
    assert Fraction(accepted, 25) == Fraction(4, 5)


def test_two_actual_instruments_then_fourier_relation_without_hidden_feedback():
    cubic = PhasePacket(5, 1, 1, {(3,): (1,)})
    original = _state(cubic, (2,))
    ys = ((0,), (1,))
    quadratic = erase_line_degree([cubic, cubic], [1, 4], ys)
    actual_q, first_mass = merge_branch(5, [original, original], [1, 4], ys)
    linear = erase_line_degree([quadratic, quadratic], [1, 2], ys)
    actual_l, second_mass = merge_branch(5, [actual_q, actual_q], [1, 2], ys)
    assert linear.degree == 1
    # Two independently prepared first branches, not copying one quantum state.
    assert first_mass**2*second_mass == pytest.approx(Fraction(1, 5**6))
    probabilities = abs(np.fft.fft(np.array([actual_l[(x,)] for x in range(5)]))/np.sqrt(5))**2
    public_relation = linear.coefficients[(1,)][0]
    assert public_relation != 0
    assert probabilities[2*public_relation % 5] == pytest.approx(1)
    frame = LearningFrame(5, 1, 3, (0, 0, 0), ((0, 0, 1),))
    learned = frame.learn_relation((public_relation,), int(np.argmax(probabilities)))
    assert learned.known == (0, 0, 2)


def test_nonidentical_public_maps_do_not_need_uniform_or_repeated_labels():
    packets = [PhasePacket(5, 1, 2, {(3,): top, (2,): low, (1,): (1, 3)})
               for top, low in (((1, 0), (2, 1)), ((0, 1), (4, 0)), ((1, 1), (0, 3)))]
    states = [_state(packet, (2, 3)) for packet in packets]
    top_nonzero = 0
    for values in product(range(5), repeat=3):
        outcomes = tuple((v,) for v in values)
        reduced = erase_line_degree(packets, [1, 1, 4], outcomes)
        physical, mass = merge_branch(5, states, [1, 1, 4], outcomes)
        assert mass == Fraction(1, 125)
        expected = _state(reduced, (2, 3))
        assert abs(sum(np.conj(expected[x])*physical[x] for x in expected)) == pytest.approx(1)
        top_nonzero += reduced.degree == 2
    assert Fraction(top_nonzero, 125) >= Fraction(4, 5)


@pytest.mark.parametrize("p,width,degree", [(5, 2, 3), (101, 8, 3), (2**127-1, 8, 3)])
def test_budget_has_no_field_enumeration_and_pays_local_retries(p, width, degree):
    budget = copy_envelope(p, width, degree)
    assert budget["unknown_coefficients_mod_constant"] == comb(width+degree, degree)-1
    expected = budget["expected_original_copies_upper_bound"]
    assert expected/budget["original_copy_abort_cap"] <= Fraction(1, 6)
    assert budget["line_acceptance_lower_bound"] >= Fraction(2, degree+1)
    assert budget["merge_acceptance_lower_bound"] >= Fraction(degree, degree+1)
    if p > 101:
        assert expected < copy_envelope(101, width, degree)["expected_original_copies_upper_bound"]


def test_invalid_promises_and_fake_progress_are_rejected():
    for p, n, d in ((9, 1, 3), (5, 1, 5), (5, 0, 3), (5, 1, 0)):
        with pytest.raises(ValueError):
            LearningFrame.initial(p, n, d)
    with pytest.raises(ValueError, match="independent"):
        LearningFrame(5, 1, 2, (0, 0), ((1, 0), (1, 0)))
    with pytest.raises(ValueError, match="zero relation"):
        LearningFrame.initial(5, 1, 2).learn_relation((0, 0), 0)
    packet = PhasePacket(5, 1, 1, {(3,): (1,)})
    for scales in ([0, 0], [1, 1]):
        with pytest.raises(ValueError):
            erase_line_degree([packet, packet], scales, ((0,), (0,)))
    with pytest.raises(ValueError, match="strictly below"):
        erase_line_degree([PhasePacket(3, 1, 1, {(3,): (1,)})]*2, [1, 2], ((0,), (0,)))
    with pytest.raises(ValueError):
        copy_envelope(5, 2, 3, Fraction(0))


def test_report_is_not_a_dequantization_or_implemented_quantum_algorithm():
    artifact = report()
    for flag in ("classical_dequantization", "novelty_established", "quantum_learner_implemented",
                 "general_sde_backend_implemented", "asymptotic_theorem_independently_verified",
                 "global_constant_recoverable"):
        assert artifact[flag] is False


@pytest.mark.parametrize("width,degree", [(1, 5), (2, 3), (3, 4), (5, 3)])
def test_coordinate_rank_count_and_nested_spaces(width, degree):
    frame = LearningFrame.initial(101, width, degree)
    for axis in range(width):
        previous = None
        for power in range(1, degree+1):
            space = frame.coordinate_row_space(axis, power)
            count = sum(alpha[axis] >= power for alpha in frame.indices)
            assert len(space) == count == coordinate_rank_cap(width, degree, power)
            if previous is not None:
                assert _rank([*previous, *space], frame.p) == len(previous)
            previous = space


def test_fixed_axis_invariant_survives_translations_merges_and_parameter_updates(monkeypatch):
    monkeypatch.setattr(PhasePacket, "evaluate_fixture",
                        lambda *args: pytest.fail("hidden phase evaluation forbidden"))
    frame = LearningFrame.initial(101, 3, 3)
    rng = random.Random(281028)
    for _ in range(5):
        axis = frame.next_axis()
        packets = [frame.restrict(axis, tuple(rng.randrange(101) for _ in range(2)))[1]
                   for _ in range(8)]
        for packet in packets:
            frame.check_coordinate_packet(axis, packet)
        for _ in range(3):
            packets = [translate_combine(packets[i:i+2], [3, 7],
                                         [(rng.randrange(101),), (rng.randrange(101),)])
                       for i in range(0, len(packets), 2)]
            for packet in packets:
                frame.check_coordinate_packet(axis, packet)
        # Any measured affine equation gives the same rank argument, even b=0.
        relation = (1,)+tuple(rng.randrange(101) for _ in frame.basis[1:])
        frame = frame.learn_relation(relation, 0)
        for power in range(1, 4):
            assert len(frame.coordinate_row_space(axis, power)) <= coordinate_rank_cap(3, 3, power)


def test_mixing_axes_really_breaks_the_sharp_bound():
    frame = LearningFrame.initial(7, 2, 3)
    x_line = frame.restrict(0, (0,))[1]
    y_line = frame.restrict(1, (0,))[1]
    top = [packet.coefficients[(3,)] for packet in (x_line, y_line)]
    assert _rank(top, 7) == 2 > coordinate_rank_cap(2, 3, 3)
    frame.check_coordinate_packet(0, x_line)
    with pytest.raises(ValueError, match="filtration"):
        frame.check_coordinate_packet(0, y_line)
    mixed = translate_combine([x_line, y_line], [1, 1], [(0,), (0,)])
    with pytest.raises(ValueError, match="filtration"):
        frame.check_coordinate_packet(0, mixed)


def test_cubic_lower_row_can_attain_the_bound_after_real_degree_erasure():
    frame = LearningFrame.initial(7, 3, 3)
    left = frame.restrict(0, (0, 0))[1]
    rows = []
    # Degree-three top rows are identical, so the signed pair is a legal SDE.
    for y1, y2, mu in product(range(2), repeat=3):
        right = frame.restrict(0, (y1, y2))[1]
        output = erase_line_degree([left, right], [1, 6], [(0,), (mu,)])
        frame.check_coordinate_packet(0, output)
        rows.append(output.coefficients[(2,)])
    assert _rank(rows, 7) == coordinate_rank_cap(3, 3, 2) == 4


def test_rank_certified_maps_connect_to_the_bounded_sde_without_hidden_data(monkeypatch):
    import theorems.power_sde as core
    from theorems.power_sde_budget import budgeted_power_weights
    monkeypatch.setattr(PhasePacket, "evaluate_fixture",
                        lambda *args: pytest.fail("hidden phase evaluation forbidden"))
    monkeypatch.setattr(core, "_field_root",
                        lambda *args: pytest.fail("uncapped root backend forbidden"))
    p = 2**127-1
    frame = LearningFrame.initial(p, 3, 3)
    rng = random.Random(20261028)
    packets = []
    for _ in range(core.power_arity(coordinate_rank_cap(3, 3, 2), 2)):
        # Public descriptors only: a physical realization needs TWO fresh
        # independent input copies for each quadratic packet, never cloning.
        children = [frame.restrict(0, (rng.randrange(p), rng.randrange(p)))[1] for _ in range(2)]
        packet = erase_line_degree(children, [1, p-1], [(rng.randrange(p),), (rng.randrange(p),)])
        frame.check_coordinate_packet(0, packet)
        packets.append(packet)
    columns = [packet.coefficients[(2,)] for packet in packets]
    assert _rank(columns, p) == 4
    result = budgeted_power_weights(p, 2, columns, bit_source=rng)
    output = erase_line_degree(packets, result.witness.weights,
                               [(rng.randrange(p),) for _ in packets])
    frame.check_coordinate_packet(0, output)
    assert output.degree == 1
    assert result.witness.required_columns == 25 and result.witness.compressed_rank == 4
    assert result.budget.total_abort_bound <= Fraction(1, 2**32)


def test_coordinate_bound_is_not_the_rank_for_arbitrary_packets():
    frame = LearningFrame.initial(7, 2, 3)
    with pytest.raises(ValueError, match="incompatible"):
        frame.check_coordinate_packet(0, PhasePacket(7, 1, 1, {(1,): (1,)}))
    with pytest.raises(ValueError, match="exceeds"):
        frame.check_coordinate_packet(0, PhasePacket(7, 1, len(frame.basis),
                                                    {(4,): frame.basis[0]}))
    for args in ((0, 3, 2), (2, 3, 4), (True, 3, 1)):
        with pytest.raises(ValueError):
            coordinate_rank_cap(*args)
    for axis, power in ((True, 1), (2, 1), (0, 0), (0, 4)):
        with pytest.raises(ValueError):
            frame.coordinate_row_space(axis, power)


def test_coordinate_copy_envelope_pays_retries_and_preserves_scope():
    for p, n, d in ((5, 2, 3), (101, 8, 3), (2**127-1, 8, 3)):
        result = coordinate_copy_envelope(p, n, d)
        assert result["expected_original_copies_upper_bound"] < copy_envelope(p, n, d)[
            "expected_original_copies_upper_bound"]
        assert result["expected_original_copies_upper_bound"]/result["original_copy_abort_cap"] <= Fraction(1, 6)
        assert result["coordinate_rank_caps"] == {2: n+1, 3: 1}
        assert result["fixed_axis_per_tree_required"] and result["fresh_frame_per_learning_round_required"]
        assert not result["arithmetic_failure_budget_included"] and not result["quantum_learner_implemented"]
    result = coordinate_copy_envelope(2**127-1, 8, 3, construction="symmetric")
    assert result["sde_arities"] == {2: 100, 3: 6}
    with pytest.raises(ValueError, match="below"):
        coordinate_copy_envelope(7, 2, 3, construction="symmetric")
    with pytest.raises(ValueError, match="construction"):
        coordinate_copy_envelope(7, 2, 3, construction="unproved")


def test_phase_copy_cli_writes_rank_profiles_without_promoting_claims(tmp_path, capsys):
    import json
    from argparse import ArgumentParser
    import qsearch
    from qsearch_cli.commands.sde import add_phase_copy_baseline
    parser = ArgumentParser()
    parser.set_defaults(root=tmp_path)
    add_phase_copy_baseline(parser.add_subparsers(dest="command", required=True))
    args = parser.parse_args(["phase-copy-baseline", "--write"])
    assert args.func is qsearch.command_phase_copy_baseline
    assert args.func(args) == 0
    result = json.loads(capsys.readouterr().out)
    saved = tmp_path/"research/reductions/polynomial_phase_copy_learning.json"
    assert json.loads(saved.read_text()) == result
    assert len(result["coordinate_profiles"]) == 4
    for flag in ("quantum_learner_implemented",
                 "asymptotic_theorem_independently_verified", "optimal_copy_complexity_established",
                 "classical_dequantization", "novelty_established"):
        assert result[flag] is False
    assert result["coordinate_rank_bound_independently_reviewed"] is True
    assert result["bounded_controller_implemented"] is True
    assert result["controller_backend"] == "finite_statevector_fixture_only"


def test_controller_end_to_end_recovers_all_coefficients_and_balances_ledger():
    p = 1049
    width = 2
    degree = 3
    rng = random.Random(42)
    initial_frame = LearningFrame.initial(p, width, degree)
    hidden = tuple(rng.randrange(p) for _ in initial_frame.indices)
    source = StateVectorPhaseSource(p, width, degree, hidden, rng=rng)
    controller = PhaseCopyController(p, width, degree, source, rng=rng)
    result = controller.learn()
    assert result.status == "OK"
    assert result.known == hidden
    assert result.ledger.drawn <= result.budget.copy_cap
    result.ledger.check_balance()
    assert result.ledger.used_in_relations > 0


def test_controller_state_reuse_is_forbidden_and_raises_error():
    p = 1049
    source = StateVectorPhaseSource(p, 2, 3, (1,) * 9, rng=random.Random(1))
    h = source.draw()
    obs, h2 = source.measure_all_but(h, 0)
    with pytest.raises(ValueError, match="already been consumed"):
        source.measure_all_but(h, 0)


def test_controller_source_cap_exhaustion_aborts_cleanly_with_balanced_ledger():
    p = 1049
    width = 2
    degree = 3
    rng = random.Random(42)
    initial_frame = LearningFrame.initial(p, width, degree)
    hidden = tuple(rng.randrange(p) for _ in initial_frame.indices)
    source = StateVectorPhaseSource(p, width, degree, hidden, rng=rng, cap=20)
    controller = PhaseCopyController(p, width, degree, source, rng=rng)
    result = controller.learn()
    assert result.status == "ABORT"
    assert "exhausted" in result.reason
    assert result.ledger.drawn == 20
    result.ledger.check_balance()


def test_controller_fails_closed_below_symmetric_field_regime():
    source = StateVectorPhaseSource(5, 2, 3, (1,) * 9, rng=random.Random(1))
    with pytest.raises(ValueError, match="below certified symmetric threshold"):
        PhaseCopyController(5, 2, 3, source)


def test_controller_invalid_witness_raises_arithmetic_error_and_does_not_abort(monkeypatch):
    import theorems.weighted_two_erasure_cascade as cascade
    p = 1049
    width = 2
    degree = 3
    rng = random.Random(42)
    initial_frame = LearningFrame.initial(p, width, degree)
    hidden = tuple(rng.randrange(p) for _ in initial_frame.indices)
    source = StateVectorPhaseSource(p, width, degree, hidden, rng=rng)
    controller = PhaseCopyController(p, width, degree, source, rng=rng)

    def bad_solve(*args, **kwargs):
        cols = args[1]
        return [1] * len(cols), len(cols), 1, 1

    monkeypatch.setattr(cascade, "solve_bezout_sde_weights", bad_solve)
    with pytest.raises((ArithmeticError, ValueError)):
        controller.learn()


def test_controller_fourier_convention_sign():
    p = 1049
    width = 2
    degree = 3
    rng = random.Random(42)
    initial_frame = LearningFrame.initial(p, width, degree)
    hidden = tuple(rng.randrange(p) for _ in initial_frame.indices)
    source = StateVectorPhaseSource(p, width, degree, hidden, rng=rng, fourier_convention=-1)
    controller = PhaseCopyController(p, width, degree, source, rng=rng)
    result = controller.learn()
    assert result.status == "OK"
    assert result.known == hidden
    result.ledger.check_balance()


def test_controller_code_does_not_import_or_leak_hidden_state_backend():
    import ast
    from pathlib import Path
    path = Path("theorems/polynomial_phase_copy_learning.py")
    tree = ast.parse(path.read_text())
    forbidden_terms = {"StateVectorPhaseSource", "phase_copy_statevector_backend", "evaluate_fixture", "_hidden"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name not in forbidden_terms
        elif isinstance(node, ast.ImportFrom):
            assert node.module not in forbidden_terms
        elif isinstance(node, ast.Name):
            assert node.id not in forbidden_terms
        elif isinstance(node, ast.Attribute):
            assert node.attr not in forbidden_terms


def test_controller_early_degree_drop_on_slice():
    p = 1031
    width = 2
    degree = 3
    rng = random.Random(42)
    frame = LearningFrame.initial(p, width, degree)
    # Hidden polynomial: x0^3 + 2 x0 x1 + 5 x1^2
    poly_terms = {(3, 0): 1, (1, 1): 2, (0, 2): 5}
    hidden = tuple(poly_terms.get(alpha, 0) for alpha in frame.indices)
    source = StateVectorPhaseSource(p, width, degree, hidden, rng=rng)
    controller = PhaseCopyController(p, width, degree, source, rng=rng)
    res = controller.learn()
    assert res.status == "OK"
    assert res.known == hidden
    res.ledger.check_balance()


def test_source_rejects_mixed_axes_in_shear_merge():
    p = 1031
    width = 2
    degree = 2
    rng = random.Random(7)
    frame = LearningFrame.initial(p, width, degree)
    hidden = tuple(rng.randrange(p) for _ in frame.indices)
    source = StateVectorPhaseSource(p, width, degree, hidden, rng=rng)
    h1 = source.draw()
    h2 = source.draw()
    _, h1_sliced = source.measure_all_but(h1, 0)
    _, h2_sliced = source.measure_all_but(h2, 1)
    with pytest.raises(ValueError, match="different coordinate axes"):
        source.shear_merge([h1_sliced, h2_sliced], [1, 1])


def test_controller_rejects_stale_frame_packet():
    frame0 = LearningFrame.initial(1031, 2, 2)
    _, pkt = frame0.restrict(0, (3,))
    frame1 = frame0.learn_relation(pkt.coefficients[(1,)], 0)
    with pytest.raises(ValueError, match="frame mismatch"):
        frame1.check_coordinate_packet(0, pkt)


def test_controller_fourier_convention_matching_and_mismatch():
    p = 1031
    width = 1
    degree = 2
    rng = random.Random(12345)
    frame = LearningFrame.initial(p, width, degree)
    hidden = tuple(rng.randrange(p) for _ in frame.indices)

    # Matching convention (-1, -1) succeeds
    source_match = StateVectorPhaseSource(p, width, degree, hidden, rng=rng, fourier_convention=-1)
    controller_match = PhaseCopyController(p, width, degree, source_match, rng=rng)
    res_match = controller_match.learn()
    assert res_match.status == "OK"
    assert res_match.known == hidden
    res_match.ledger.check_balance()

    # Mismatched physical vs declared convention (1, -1) fails to recover hidden
    source_mismatch = StateVectorPhaseSource(
        p, width, degree, hidden, rng=rng, fourier_convention=1, physical_qft_sign=-1
    )
    controller_mismatch = PhaseCopyController(p, width, degree, source_mismatch, rng=rng)
    res_mismatch = controller_mismatch.learn()
    assert res_mismatch.known != hidden


def test_controller_solver_randomness_exhaustion_aborts_cleanly():
    p = 1031
    width = 1
    degree = 2
    rng = random.Random(45)
    frame = LearningFrame.initial(p, width, degree)
    hidden = tuple(rng.randrange(p) for _ in frame.indices)
    source = StateVectorPhaseSource(p, width, degree, hidden, rng=rng)
    controller = PhaseCopyController(p, width, degree, source, rng=rng)
    object.__setattr__(controller.budget, "solver_bits", 1)
    res = controller.learn()
    assert res.status == "ABORT"
    assert "exhausted" in res.reason
    res.ledger.check_balance()
