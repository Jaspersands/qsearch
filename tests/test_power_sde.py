"""Controls for all-degree symmetric contraction, including nonresidue signs."""
from fractions import Fraction
from math import isqrt
import random

import pytest
from sympy import Matrix, simplify, symbols

import theorems.power_sde as solver
from theorems.weighted_two_erasure_cascade import (
    required_bezout_arity, solve_bezout_sde_weights, verify_general_degree_witness,
)


P4 = 2**128-275
P5 = 2**61-1


def columns_at_rank(prime, degree, rank, seed=28):
    rng = random.Random(seed)
    cols = [tuple(int(i == j) for i in range(rank)) for j in range(rank)]
    cols += [tuple(rng.randrange(prime) for _ in range(rank))
             for _ in range(solver.power_arity(rank, degree)-rank)]
    return cols


@pytest.mark.parametrize("degree", [2, 4, 5])
def test_symmetric_form_annihilates_every_tensor_basis_vector(degree):
    z, t = symbols(f"z0:{degree}", nonzero=True), symbols(f"t0:{degree}")
    basis = Matrix.vstack(Matrix.eye(degree-1), Matrix([[-a/z[-1] for a in z[:-1]]]))
    coefficients = Matrix(degree, degree, lambda i, j: z[i]*z[j]*(t[i]+t[j]))
    assert all(simplify(a) == 0 for a in basis.T*coefficients*basis)
    assert coefficients[0, 0] == 2*z[0]**2*t[0]


@pytest.mark.parametrize("prime,degree,rank", [(P4, 4, 3), (P5, 5, 2), (P5, 5, 8), (65537, 2, 3)])
def test_quadratic_arity_arbitrary_columns_exact_original_moments(prime, degree, rank):
    columns = columns_at_rank(prime, degree, rank)
    before = tuple(columns)
    result = solver.power_weights(prime, degree, columns, rng=random.Random(19))
    assert tuple(columns) == before
    assert result.required_columns == (rank+1)*((degree-1)*rank+1)
    assert result.compressed_rank == rank and result.distinguished_support_size > 0
    assert result.checked_axis_relations == (degree-1)*rank+1+2*degree
    assert result.root_calls and result.generator_draws
    assert result.closure.abort_bound == Fraction(degree-1, 2**32)
    assert result.closure.stage_caps == tuple(2*degree**k*32 for k in range(2, degree+1))
    assert result.closure.stage_success_bounds == tuple(Fraction(1, 2*degree**k) for k in range(2, degree+1))
    assert all(0 < a <= cap for a, cap in zip(result.closure.stage_draws, result.closure.stage_caps))
    verify_general_degree_witness(prime, columns, result.weights, degree)


def test_even_composite_degree_needs_neither_minus_one_nor_two_to_be_power():
    assert P4 % 8 == 5
    assert pow(P4-1, (P4-1)//4, P4) != 1
    assert pow(2, (P4-1)//4, P4) != 1
    z, _, _ = solver._representatives(P4, 4, random.Random(13), 128)
    result = solver.symmetric_closure(P4, 4, z, rng=random.Random(41))
    assert len(set(result.offsets)) == 4 and all(result.offsets)
    assert result.roots[0][0] == 1
    for i in range(4):
        for j in range(4):
            assert result.roots[i][j] == result.roots[j][i]
            assert pow(result.roots[i][j], 4, P4) == z[i]*z[j]*(result.offsets[i]+result.offsets[j]) % P4


def test_empty_vector_value_does_not_erase_distinguished_support():
    columns = [(0,)]*solver.power_arity(1, 4)
    columns[-1] = (1,)
    result = solver.power_weights(P4, 4, columns, rng=random.Random(14))
    assert result.distinguished_vector_zero and result.distinguished_support_size > 0
    assert any(result.weights)
    verify_general_degree_witness(P4, columns, result.weights, 4)


def test_character_count_handles_nontrivial_affine_cosets_and_zero_exclusions():
    p, d = 65537, 4
    # Independent exact count, not the sampler: includes a nonsquare
    # multiplier and explicitly removes every affine root.
    factors = ((3, 0), (5, 17))
    good = [x for x in range(p) if all((v := c*(x-a) % p)
             and pow(v, (p-1)//d, p) == 1 for c, a in factors)]
    k = len(factors)
    assert not set(good) & {a for _, a in factors}
    # Ceiling sqrt gives a conservative rational comparison without floats.
    assert len(good) >= Fraction(p, d**k)-k*(isqrt(p)+1)


class ConstantRandom:
    def __init__(self, value):
        self.value, self.draws = value, 0

    def randrange(self, start, stop):
        self.draws += 1
        return self.value


@pytest.mark.parametrize("bad", [0, "duplicate", "opposite"])
def test_scalar_abort_on_zero_duplicate_and_affine_root(bad):
    z, _, _ = solver._representatives(P4, 4, random.Random(3), 128)
    t0 = pow(2*z[0]*z[0], -1, P4)
    value = t0 if bad == "duplicate" else -t0 % P4 if bad == "opposite" else 0
    rng = ConstantRandom(value)
    with pytest.raises(RuntimeError, match="stage 1"):
        solver.symmetric_closure(P4, 4, z, rng=rng, sampler_bits=1)
    assert rng.draws == 2*4**2


def test_sampler_rejects_invalid_parameters_randomness_and_roots(monkeypatch):
    z, _, _ = solver._representatives(P4, 4, random.Random(3), 128)
    with pytest.raises(ValueError, match="noncanonical"):
        solver.symmetric_closure(P4, 4, z, rng=ConstantRandom(True))
    with pytest.raises(ValueError, match="distinct"):
        solver.symmetric_closure(P4, 4, (1,)*4)
    with pytest.raises(ValueError, match="sampler_bits"):
        solver.symmetric_closure(P4, 4, z, sampler_bits=0)
    monkeypatch.setattr(solver, "_field_root", lambda *args: 0)
    with pytest.raises(ArithmeticError, match="power root"):
        solver.symmetric_closure(P4, 4, z, rng=random.Random(5))


@pytest.mark.parametrize("prime,degree", [(13, 4), (601, 5), (65535, 2), (65537, 3), (P4, True)])
def test_unsupported_regimes_fail_closed(prime, degree):
    with pytest.raises(ValueError):
        solver.power_weights(prime, degree, [(1,)])


def test_caps_bad_rank_and_lying_compression_fail_closed(monkeypatch):
    with pytest.raises(ValueError, match="sampler_bits"):
        solver.power_weights(P4, 4, [(0,)], sampler_bits=0)
    with pytest.raises(ValueError, match="need 8"):
        solver.power_weights(P4, 4, [(1,)])
    with pytest.raises(ValueError, match="rank"):
        solver.power_arity(True, 4)
    rng = ConstantRandom(1)
    with pytest.raises(RuntimeError, match="generator sampler"):
        solver.power_weights(P4, 4, [(1,)]*8, rng=rng, generator_attempt_cap=3)
    assert rng.draws == 3
    assert solver.power_weights(P4, 4, [(0, 0)]).weights == (1,)
    monkeypatch.setattr(solver, "independent_columns_exact", lambda *args: ([[0]], 0))
    with pytest.raises(ArithmeticError, match="cancellation"):
        solver.power_weights(P4, 4, [(1,)])


@pytest.mark.parametrize("prime,degree,reduced", [(P4, 4, 4), (P4, 8, 4), (P5, 5, 5), (65537, 2, 2)])
def test_controller_dispatch_and_bezout_lift(prime, degree, reduced):
    assert required_bezout_arity(prime, degree, 2) == solver.power_arity(2, reduced)
    columns = columns_at_rank(prime, reduced, 2)
    weights, rank, g, _ = solve_bezout_sde_weights(prime, columns, degree, rng=random.Random(711))
    assert rank == 2 and g == reduced
    verify_general_degree_witness(prime, columns, weights, degree)
    with pytest.raises(ValueError, match="sampler_bits"):
        solve_bezout_sde_weights(prime, columns, degree, power_sampler_bits=0)


def test_existing_lower_field_fallback_and_guards_remain():
    from theorems.odd_power_sde import odd_power_arity
    assert required_bezout_arity(601, 5, 1) == odd_power_arity(1, 5)
    assert required_bezout_arity(7, 3, 2) == 15
    assert required_bezout_arity(23, 2, 2) == 9
    with pytest.raises(ValueError, match="below"):
        required_bezout_arity(13, 4, 1)
    with pytest.raises(ValueError):
        required_bezout_arity(9, 4, 0)


def test_fixed_small_field_does_not_imply_linear_arity_or_rank_constant_dp():
    from itertools import product
    columns = [(1, 0), (0, 1), (1, 0)]
    # Even existence fails at r+1 columns. A scalar degree-constant lookup
    # cannot simply become a rank-independent vector-syndrome algorithm.
    for weights in product(range(3), repeat=3):
        if any(weights):
            assert any(sum(pow(w, 2, 3)*v[j] for w, v in zip(weights, columns)) % 3 for j in range(2))


def _enumerate_two_level_contractions(prime, representatives, degree):
    """Exhaust the border parametrization of (ker(z) tensor ker(z))^perp."""
    from itertools import product

    z = tuple(representatives)
    size = len(z)
    powers = tuple(sorted({pow(x, degree, prime) for x in range(prime)}))
    ratios = [x*pow(z[0], -1, prime) % prime for x in z]
    solutions = []
    for border in product(powers, repeat=2*size-1):
        row = border[:size]
        column = (row[0],)+border[size:]
        matrix = tuple(tuple((ratios[j]*column[i]+ratios[i]*row[j]
                              -ratios[i]*ratios[j]*row[0]) % prime
                             for j in range(size)) for i in range(size))
        if all(x in powers for values in matrix for x in values):
            solutions.append(matrix)
    return solutions, len(powers)**(2*size-1)


@pytest.mark.parametrize("prime", [5, 7])
def test_all_two_level_contractions_fail_for_zero_one_power_residues(prime):
    # This exhausts ALL annihilating coefficient matrices, not only the
    # symmetric sampler. It is not an SDE existence/complexity lower bound.
    degree = prime-1
    z = tuple(range(1, prime))
    solutions, borders = _enumerate_two_level_contractions(prime, z, degree)
    assert borders == 2**(2*degree-1)
    assert solutions == [tuple((0,)*degree for _ in range(degree))]
    with pytest.raises(ValueError, match="below"):
        solver.symmetric_closure(prime, degree, z)


def test_border_enumeration_accepts_a_genuine_small_field_contraction():
    solutions, borders = _enumerate_two_level_contractions(3, (1, 2), 2)
    assert borders == 8
    assert ((1, 1), (1, 0)) in solutions
    assert len(solutions) == 5  # zero, and the four choices of one zero cell
    for matrix in solutions:
        assert sum(map(sum, matrix)) % 3 == 0


def test_two_level_border_parameterization_matches_independent_tensor_pairing():
    from itertools import product

    # Exhaust every matrix in a tiny independent control, rather than
    # trusting the border formula used in the negative controls.
    p, z = 5, (1, 2)
    powers = sorted({x*x % p for x in range(p)})
    kernel = (-z[1] % p, z[0])
    independently_valid = set()
    for entries in product(powers, repeat=4):
        matrix = (entries[:2], entries[2:])
        if sum(kernel[i]*matrix[i][j]*kernel[j] for i in range(2) for j in range(2)) % p == 0:
            independently_valid.add(matrix)
    enumerated, _ = _enumerate_two_level_contractions(p, z, 2)
    assert set(enumerated) == independently_valid


def test_weighted_unknown_phase_erasure_uses_even_power_backend(monkeypatch):
    from theorems.nonlinear_jet_erasure import TaylorJetChart
    from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket
    from theorems.weighted_two_erasure_cascade import PinnedWeightedPacket, weighted_erasure_stage

    def forbidden(*args, **kwargs):
        raise AssertionError("hidden phase evaluation was accessed")

    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    chart = TaylorJetChart(p=P4, quotient_width=1, noncentral_width=1, degree=4)
    exponent = (4,)+(0,)*chart.jet_width
    packets = [PinnedWeightedPacket("even-sde", "fixed-chart", chart,
        SymbolicScalarPacket(P4, 1, chart.jet_width, ((0, (1,)),),
                             {(exponent, (0,)): i+1})) for i in range(8)]
    rng = random.Random(91)
    outcomes = [([rng.randrange(P4)], [rng.randrange(P4) for _ in range(chart.jet_width)])
                for _ in packets]
    with pytest.raises(RuntimeError, match="generator sampler"):
        weighted_erasure_stage(packets, 4, outcomes, rng=ConstantRandom(1))
    assert all(not packet.consumed for packet in packets)
    merged, weights, rank, equations = weighted_erasure_stage(packets, 4, outcomes, rng=rng)
    assert rank == equations == 1 and any(weights)
    assert merged.weighted_degree < 4
    assert all(packet.consumed for packet in packets) and not merged.consumed


def test_cli_report_retains_scope_and_metrics(tmp_path, capsys):
    import json
    from argparse import ArgumentParser
    from qsearch_cli.commands.sde import add_power_sde
    parser = ArgumentParser()
    parser.set_defaults(root=tmp_path)
    add_power_sde(parser.add_subparsers(dest="command", required=True))
    args = parser.parse_args(["power-sde", "--write"])
    assert args.func(args) == 0
    data = json.loads(capsys.readouterr().out)
    assert data == json.loads((tmp_path/"research/reductions/power_sde.json").read_text())
    assert data["even_degree_supported"]
    for flag in ("random_input_promise", "input_labels_resampled", "field_enumeration_used",
                 "all_prime_regimes_supported", "degree_uniform_polynomial_time",
                 "backend_runtime_locally_clocked", "quantum_receiver_implemented",
                 "novelty_established", "speedup_claim_allowed"):
        assert not data[flag]
    assert all(c["exact_original_moment_verified"] for c in data["cases"])


def test_new_commands_are_registered_and_exported_by_qsearch():
    import qsearch
    parser = qsearch.build_parser()
    for command in ("power-sde", "odd-power-sde"):
        args = parser.parse_args([command, "--write"])
        assert args.write
        assert args.func is getattr(qsearch, "command_"+command.replace("-", "_"))
