"""Finite randomness accounting and exact witness controls, not runtime data."""
from collections import Counter
from fractions import Fraction
from itertools import product
import random

import pytest

import theorems.power_sde as core
from theorems.power_sde_budget import CappedUniformRandom, budgeted_power_weights, randomness_budget
from theorems.weighted_two_erasure_cascade import verify_general_degree_witness


@pytest.mark.parametrize("degree", [2, 3, 4, 5, 6, 9])
@pytest.mark.parametrize("rank", [0, 1, 8, 1000])
def test_whole_budget_allocation_is_exact_and_polynomial_in_rank(degree, rank):
    budget = randomness_budget(rank, degree, 17)
    assert budget.total_abort_bound <= Fraction(1, 2**17)
    assert budget.algebraic_sampling_abort_bound <= Fraction(1, 2**18)
    assert budget.integer_sampling_abort_bound <= Fraction(1, 2**18)
    if rank:
        assert budget.root_call_cap == ((degree-1)*rank+1)*(rank+3)+degree*(degree+1)//2
    else:
        assert budget.root_call_cap == 0
    assert budget.generator_attempt_cap == degree*budget.internal_bits
    assert budget.root_split_attempt_cap == 3*budget.internal_bits


class Bits:
    def __init__(self, values):
        self.values = iter(values)
        self.calls = 0

    def getrandbits(self, width):
        self.calls += 1
        return next(self.values)


def test_bit_rejection_is_exact_uniform_conditioned_on_acceptance():
    counts = Counter()
    for a, b in product(range(4), repeat=2):
        rng = CappedUniformRandom(Bits((a, b)), call_cap=1, rejection_cap=2, max_interval=3)
        try:
            counts[rng.randrange(7, 10)] += 1
        except RuntimeError:
            counts["abort"] += 1
        assert rng.calls == 1 and rng.bit_draws <= 2 and rng.random_bits <= 4
    assert counts == {7: 5, 8: 5, 9: 5, "abort": 1}


def test_unit_interval_and_exact_budget_limits():
    bits = Bits(())
    rng = CappedUniformRandom(bits, call_cap=1, rejection_cap=3, max_interval=5)
    assert rng.randrange(9, 10) == 9
    assert rng.calls == 1 and rng.random_bits == bits.calls == 0
    with pytest.raises(RuntimeError, match="call cap"):
        rng.randrange(0, 3)
    rng = CappedUniformRandom(Bits((3, 3, 3)), call_cap=2, rejection_cap=3, max_interval=3)
    with pytest.raises(RuntimeError, match="rejection cap"):
        rng.randrange(0, 3)
    assert rng.bit_draws == 3 and rng.random_bits == 6


@pytest.mark.parametrize("bad", [True, -1, 4])
def test_invalid_bit_strings_rejected(bad):
    rng = CappedUniformRandom(Bits((bad,)), call_cap=1, rejection_cap=1, max_interval=3)
    with pytest.raises(ValueError, match="noncanonical"):
        rng.randrange(0, 3)


def test_invalid_budget_and_rng_contracts_fail_closed():
    for args in ((-1, 4, 3), (1, True, 3), (1, 4, 0)):
        with pytest.raises(ValueError):
            randomness_budget(*args)
    with pytest.raises(ValueError, match="getrandbits"):
        CappedUniformRandom(object(), call_cap=1, rejection_cap=1, max_interval=3)
    rng = CappedUniformRandom(Bits(()), call_cap=1, rejection_cap=1, max_interval=3)
    for start, stop in ((0, 4), (1, 1), (True, 2)):
        with pytest.raises(ValueError, match="interval"):
            rng.randrange(start, stop)


@pytest.mark.parametrize("prime,degree,rank", [(2**128-275, 4, 3), (2**61-1, 5, 8), (65537, 2, 2)])
def test_budgeted_solver_uses_no_uncapped_root_backend_and_records_all_draws(monkeypatch, prime, degree, rank):
    def forbidden(*args, **kwargs):
        raise AssertionError("uncapped root backend called")

    monkeypatch.setattr(core, "_field_root", forbidden)
    rng = random.Random(20261028)
    count = core.power_arity(rank, degree)
    columns = [tuple(int(i == j) for i in range(rank)) for j in range(rank)]
    columns += [tuple(rng.randrange(prime) for _ in range(rank)) for _ in range(count-rank)]
    snapshot = tuple(columns)
    result = budgeted_power_weights(prime, degree, columns, bit_source=random.Random(928))
    assert tuple(columns) == snapshot
    b = result.budget
    assert 0 < result.root_calls <= b.root_call_cap
    assert result.root_calls == result.witness.root_calls
    assert result.root_split_trials <= b.root_call_cap*(degree-1)*b.root_split_attempt_cap
    assert result.root_proper_splits <= b.root_call_cap*(degree-1)
    assert result.uniform_calls <= b.uniform_call_cap
    assert result.bit_draws <= b.uniform_call_cap*b.integer_rejection_cap
    assert result.random_bits <= b.uniform_call_cap*b.integer_rejection_cap*(prime-1).bit_length()
    verify_general_degree_witness(prime, columns, result.witness.weights, degree)


class ZeroBits:
    def __init__(self):
        self.calls = 0

    def getrandbits(self, width):
        self.calls += 1
        return 0


def test_generator_abort_is_not_restarted_and_zero_rank_uses_no_randomness():
    bits = ZeroBits()
    p, d = 2**128-275, 4
    budget = randomness_budget(1, d, 5)
    with pytest.raises(RuntimeError, match="generator sampler"):
        budgeted_power_weights(p, d, [(1,)]*8, failure_bits=5, bit_source=bits)
    assert bits.calls == budget.generator_attempt_cap
    zero = budgeted_power_weights(p, d, [(0, 0)], bit_source=Bits(()))
    assert zero.witness.weights == (1,)
    assert zero.root_calls == zero.uniform_calls == zero.bit_draws == zero.random_bits == 0


def test_root_abort_is_propagated_without_restarting_the_bank(monkeypatch):
    import theorems.bounded_power_roots as roots
    calls = []

    def exhausted(*args, **kwargs):
        calls.append(args)
        return roots.BoundedPowerRoot(None, 1, 0, 4, Fraction(1))

    monkeypatch.setattr(roots, "bounded_power_root", exhausted)
    with pytest.raises(RuntimeError, match="root splitting exhausted"):
        budgeted_power_weights(2**128-275, 4, [(1,)]*8, bit_source=random.Random(9))
    assert len(calls) == 1


def test_controller_selects_whole_budget_and_rejects_unsupported_requests(monkeypatch):
    from theorems.weighted_two_erasure_cascade import solve_bezout_sde_weights
    monkeypatch.setattr(core, "_field_root", lambda *args: pytest.fail("uncapped root path"))
    p = 2**128-275
    columns = [(i+1,) for i in range(8)]
    weights, rank, g, _ = solve_bezout_sde_weights(p, columns, 8, rng=random.Random(29),
                                                  bounded_randomness_bits=19)
    assert rank == 1 and g == 4
    verify_general_degree_witness(p, columns, weights, 8)
    for p, d in ((601, 5), (7, 3), (13, 2)):
        with pytest.raises(ValueError, match="below"):
            solve_bezout_sde_weights(p, [(1,)]*8, d, bounded_randomness_bits=19)
    with pytest.raises(ValueError, match="bounded_randomness_bits"):
        solve_bezout_sde_weights(23, [(1,), (2,)], 3, bounded_randomness_bits=True)
    # Reduced degree one has no randomness to cap and remains legal.
    weights, _, g, _ = solve_bezout_sde_weights(23, [(1,), (2,)], 3,
                                               bounded_randomness_bits=19, rng=object())
    assert g == 1
    verify_general_degree_witness(23, [(1,), (2,)], weights, 3)


def test_weighted_and_ordinary_stages_forward_the_budget_and_preserve_abort(monkeypatch):
    from theorems.nonlinear_jet_erasure import TaylorJetChart
    from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket
    from theorems.weighted_two_erasure_cascade import (
        PinnedWeightedPacket, ordinary_higher_degree_erasure_stage, weighted_erasure_stage,
    )
    monkeypatch.setattr(core, "_field_root", lambda *args: pytest.fail("uncapped root path"))
    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture",
                        lambda *args: pytest.fail("hidden phase accessed"))
    p = 2**128-275
    chart = TaylorJetChart(p=p, quotient_width=1, noncentral_width=1, degree=4)
    exponent = (4,)+(0,)*chart.jet_width
    basis = ((0, (1,)),)
    packets = [PinnedWeightedPacket("bounded", "chart", chart,
        SymbolicScalarPacket(p, 1, chart.jet_width, basis, {(exponent, (0,)): i+1})) for i in range(8)]
    outcomes = [([i], [i]*chart.jet_width) for i in range(8)]
    with pytest.raises(RuntimeError, match="generator sampler"):
        weighted_erasure_stage(packets, 4, outcomes, rng=ZeroBits(), bounded_randomness_bits=8)
    assert all(not packet.consumed for packet in packets)
    merged, weights, rank, equations = weighted_erasure_stage(
        packets, 4, outcomes, rng=random.Random(35), bounded_randomness_bits=8)
    assert rank == equations == 1 and any(weights) and merged.weighted_degree < 4
    assert all(packet.consumed for packet in packets)
    ordinary = [SymbolicScalarPacket(p, 1, 0, basis, {((4,), (0,)): i+1}) for i in range(8)]
    output, weights, rank, equations = ordinary_higher_degree_erasure_stage(
        ordinary, 4, [[i] for i in range(8)], rng=random.Random(36), bounded_randomness_bits=8)
    assert output.degree < 4 and any(weights) and rank == equations == 1


def test_failure_flag_is_not_conditioned_out_of_the_source_error():
    labels = (Fraction(1, 4), Fraction(3, 4))
    failures = (Fraction(1, 16), Fraction(1, 8))
    target = (Fraction(1, 3), Fraction(2, 3), Fraction(0))
    abort = sum(weight*fail for weight, fail in zip(labels, failures))
    actual = tuple((1-abort)*prob for prob in target[:-1])+(abort,)
    assert sum(abs(a-b) for a, b in zip(actual, target))/2 == abort
    assert abort <= max(failures)
    assert all(a/(1-abort) == b for a, b in zip(actual[:-1], target[:-1]))
    # Conditioning makes the target look exact but discards the paid error.
    assert abort > 0


def test_cli_budget_report_preserves_unresolved_scope(tmp_path, capsys):
    import json
    from argparse import ArgumentParser
    from qsearch_cli.commands.sde import add_power_sde
    parser = ArgumentParser()
    parser.set_defaults(root=tmp_path)
    add_power_sde(parser.add_subparsers(dest="command", required=True))
    args = parser.parse_args(["power-sde", "--bounded-randomness", "--write"])
    assert args.func(args) == 0
    data = json.loads(capsys.readouterr().out)
    assert data == json.loads((tmp_path/"research/reductions/power_sde_bounded_randomness.json").read_text())
    assert data["every_randomized_loop_capped"]
    for flag in ("prime_validation_locally_clocked", "os_wallclock_bound", "formal_total_policy_instantiated",
                 "quantum_receiver_implemented", "novelty_established", "speedup_claim_allowed",
                 "root_factorization_black_box_used", "input_labels_resampled", "field_enumeration_used"):
        assert not data[flag]
    assert all(Fraction(c["total_sampling_abort_bound"]) <= Fraction(c["requested_failure_bound"])
               for c in data["cases"])
