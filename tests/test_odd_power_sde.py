"""Exact controls for the odd-degree exterior closure, with its field guard."""
from fractions import Fraction
from itertools import permutations, product
import random

import pytest
from sympy import Matrix, simplify, symbols

import theorems.odd_power_sde as solver
from theorems.weighted_two_erasure_cascade import verify_general_degree_witness


@pytest.mark.parametrize("degree", [3, 5])
def test_exterior_minor_signs_symbolically_on_a_basis(degree):
    z = symbols(f"z0:{degree}", nonzero=True)
    basis = Matrix.vstack(Matrix.eye(degree-1), Matrix([[-a/z[-1] for a in z[:-1]]]))
    for order in permutations(range(degree-1)):
        matrix = basis[:, list(order)]
        minors = [matrix.extract([j for j in range(degree) if j != i], range(degree-1)).det()
                  for i in range(degree)]
        for i in range(degree):
            assert simplify(z[-1]*minors[i]-(-1)**(degree-1-i)*z[i]*minors[-1]) == 0
    # Alternation vanishes on repeated basis entries; multilinearity then
    # covers arbitrary tensors in ker(z)^(tensor(d-1)), not only one volume.
    repeated = basis[:, [0]*(degree-1)]
    assert all(repeated.extract([j for j in range(degree) if j != i], range(degree-1)).det() == 0
               for i in range(degree))


def test_free_tensor_coordinates_determine_all_axis_constrained_values():
    p, d, level = 601, 5, 3
    z = (1, 2, 4, 8, 16)
    rng = random.Random(19)
    free = {key: rng.randrange(p) for key in product(range(d-1), repeat=level)}

    def value(key):
        if d-1 not in key:
            return free[key]
        axis = key.index(d-1)
        return -sum(z[i]*value(key[:axis]+(i,)+key[axis+1:]) for i in range(d-1))*pow(z[-1], -1, p) % p

    for axis in range(level):
        for rest in product(range(d), repeat=level-1):
            assert sum(z[i]*value(rest[:axis]+(i,)+rest[axis:]) for i in range(d)) % p == 0
    assert len(free) == (d-1)**level


@pytest.mark.parametrize("prime,rank", [(601, 1), (601, 2), (2**61-1, 1)])
def test_fifth_power_solver_on_all_original_equations(prime, rank):
    rng = random.Random(20261028)
    count = solver.odd_power_arity(rank, 5)
    columns = [tuple(int(i == j) for i in range(rank)) for j in range(rank)]
    columns += [tuple(rng.randrange(prime) for _ in range(rank)) for _ in range(count-rank)]
    before = tuple(columns)
    witness = solver.odd_power_weights(prime, 5, columns, rng=rng)
    assert tuple(columns) == before
    assert witness.compressed_rank == rank and witness.required_columns == count
    assert witness.checked_axis_relations > 0 and witness.checked_minor_relations == 5
    assert witness.root_calls > 0 and witness.scalar_draws > 0
    assert witness.sampling_abort_bound == Fraction(1, 5)**128+Fraction(9, 10)**256
    verify_general_degree_witness(prime, columns, witness.weights, 5)


def test_cubic_overlap_agrees_on_the_arity_and_original_witness_contract():
    from theorems.cubic_diagonal_solver import cubic_arity, cubic_weights
    rng = random.Random(81)
    count = solver.odd_power_arity(3, 3)
    assert count == cubic_arity(3, construction="two_level_curve")
    columns = [tuple(rng.randrange(43) for _ in range(3)) for _ in range(count)]
    new = solver.odd_power_weights(43, 3, columns, rng=rng)
    old = cubic_weights(43, columns, construction="two_level_curve", rng=rng)
    for weights in (new.weights, old.weights):
        verify_general_degree_witness(43, columns, weights, 3)


def test_scalar_sampler_meets_the_bound_in_an_exact_small_eligible_field():
    p, d = 601, 5
    reps, _, _ = solver._representatives(p, d, random.Random(12), 128)
    powers = {pow(x, d, p) for x in range(1, p)}
    success = [a for a in range(p) if (reps[0]*pow(a, d, p)+reps[-1])*pow(reps[1], -1, p) % p in powers]
    assert Fraction(len(success), p) >= Fraction(1, 2*d)
    assert 0 not in success
    for zi, zj in permutations(reps, 2):
        assert -zi*pow(zj, -1, p) % p not in powers


def test_small_field_counterexample_to_unqualified_ternary_closure():
    p, d = 11, 5
    reps = tuple(pow(2, i, p) for i in range(d))
    assert len({pow(z, (p-1)//d, p) for z in reps}) == d
    assert not any((reps[0]*pow(a, d, p)-reps[1]*pow(b, d, p)+reps[-1]) % p == 0
                   for a, b in product(range(p), repeat=2))
    with pytest.raises(ValueError, match="below"):
        solver.scalar_closure(p, d, reps)


def test_even_degree_signs_are_not_unconditionally_power_residues():
    assert 12 not in {pow(x, 4, 13) for x in range(13)}
    with pytest.raises(ValueError, match="odd"):
        solver.odd_power_weights(13, 4, [(1,)])


class ConstantRandom:
    def __init__(self, value):
        self.value, self.draws = value, 0

    def randrange(self, start, stop):
        self.draws += 1
        return self.value


def test_sampler_caps_invalid_randomness_and_root_corruption(monkeypatch):
    rng = ConstantRandom(1)
    with pytest.raises(RuntimeError, match="generator sampler"):
        solver._representatives(601, 5, rng, 3)
    assert rng.draws == 3
    reps, _, _ = solver._representatives(601, 5, random.Random(1), 128)
    rng = ConstantRandom(0)
    with pytest.raises(RuntimeError, match="scalar curve sampler"):
        solver.scalar_closure(601, 5, reps, rng=rng, attempts=4)
    assert rng.draws == 4
    with pytest.raises(ValueError, match="noncanonical"):
        solver.scalar_closure(601, 5, reps, rng=ConstantRandom(True))
    monkeypatch.setattr(solver, "_field_root", lambda *args: 0)
    with pytest.raises(ArithmeticError, match="scalar closure"):
        solver.scalar_closure(601, 5, reps, rng=random.Random(19))


def test_zero_rank_and_false_compression_are_not_unchecked_success(monkeypatch):
    result = solver.odd_power_weights(601, 5, [(0, 0)])
    assert result.weights == (1,) and result.required_columns == 1
    monkeypatch.setattr(solver, "independent_columns_exact", lambda columns, p: ([[0]], 0))
    with pytest.raises(ArithmeticError, match="cancellation"):
        solver.odd_power_weights(601, 5, [(1,)])


@pytest.mark.parametrize("p,d", [(601, 4), (601, 7), (11, 5), (605, 5), (601, True)])
def test_invalid_family_promises_fail_closed(p, d):
    with pytest.raises(ValueError):
        solver.odd_power_weights(p, d, [(1,)])


def test_bad_representatives_and_insufficient_labels_fail_closed():
    with pytest.raises(ValueError, match="distinct"):
        solver.scalar_closure(601, 5, (1,)*5)
    with pytest.raises(ValueError, match="need 11050"):
        solver.odd_power_weights(601, 5, [(1,)])
    with pytest.raises(ValueError, match="positive"):
        solver.odd_power_weights(601, 5, [(0,)], scalar_attempt_cap=0)


def test_composite_odd_degree_cosets_and_scalar_closure():
    p, d, rng = 2**127-1, 9, random.Random(32)
    reps, _, abort = solver._representatives(p, d, rng, 128)
    assert len({pow(z, (p-1)//d, p) for z in reps}) == d
    assert abort == Fraction(1, 3)**128
    result = solver.scalar_closure(p, d, reps, rng=rng)
    assert result.scales[-1] == 1
    assert sum((-1)**i*z*pow(a, d, p) for i, (z, a) in enumerate(zip(reps, result.scales))) % p == 0
    assert result.abort_bound == Fraction(17, 18)**256


def test_controller_lifts_reduced_degree_five_to_degree_35_without_hidden_input():
    from theorems.weighted_two_erasure_cascade import required_bezout_arity, solve_bezout_sde_weights
    p, rng = 601, random.Random(28)
    count = required_bezout_arity(p, 35, 1)
    assert count == solver.odd_power_arity(1, 5)
    columns = [(rng.randrange(p),) for _ in range(count)]
    weights, rank, reduced, _ = solve_bezout_sde_weights(p, columns, 35, rng=rng)
    assert rank == 1 and reduced == 5
    verify_general_degree_witness(p, columns, weights, 35)
    with pytest.raises(ValueError, match="positive"):
        solve_bezout_sde_weights(p, columns, 35, curve_attempt_cap=0)
    with pytest.raises(ValueError, match="below"):
        required_bezout_arity(11, 5, 1)


def test_weighted_unknown_phase_stage_uses_the_fifth_power_backend(monkeypatch):
    from theorems.nonlinear_jet_erasure import TaylorJetChart
    from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket
    from theorems.weighted_two_erasure_cascade import PinnedWeightedPacket, weighted_erasure_stage

    def forbidden(*args, **kwargs):
        raise AssertionError("hidden phase evaluation was accessed")

    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    p, rng = 601, random.Random(419)
    chart = TaylorJetChart(p=p, quotient_width=1, noncentral_width=1, degree=5)
    exponent = (5,)+(0,)*chart.jet_width
    packets = [PinnedWeightedPacket(
        "odd-sde-p601", "fixed-chart", chart,
        SymbolicScalarPacket(p, 1, chart.jet_width, ((0, (1,)),),
                             {(exponent, (0,)): (i+1) % p}),
    ) for i in range(solver.odd_power_arity(1, 5))]
    outcomes = [([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)])
                for _ in packets]
    merged, weights, rank, equations = weighted_erasure_stage(packets, 5, outcomes, rng=rng)
    assert rank == equations == 1 and any(weights)
    assert merged.weighted_degree < 5
    assert not merged.consumed and all(packet.consumed for packet in packets)


def test_cli_report_preserves_scope(tmp_path, capsys):
    import json
    from argparse import ArgumentParser
    from qsearch_cli.commands.sde import add_odd_power_sde
    parser = ArgumentParser()
    parser.set_defaults(root=tmp_path)
    add_odd_power_sde(parser.add_subparsers(dest="command", required=True))
    args = parser.parse_args(["odd-power-sde", "--write"])
    assert args.func(args) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed == json.loads((tmp_path/"research/reductions/odd_power_sde.json").read_text())
    for key in ("random_input_promise", "input_labels_resampled", "field_enumeration_used",
                "even_degree_supported", "all_prime_regimes_supported", "backend_runtime_locally_clocked",
                "quantum_receiver_implemented", "novelty_established", "speedup_claim_allowed"):
        assert not printed[key]
    assert all(case["exact_original_moment_verified"] for case in printed["cases"])
