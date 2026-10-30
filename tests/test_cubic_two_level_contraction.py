"""Controls for the proposed worst-case quadratic-arity cubic construction."""
from fractions import Fraction
from itertools import permutations, product
from math import isqrt
import random

import pytest
from sympy import Matrix, symbols

import theorems.cubic_diagonal_solver as solver


def test_two_axis_relations_imply_the_skew_contraction_symbolically():
    z1, z2, z3, a, b, c = symbols("z1 z2 z3 a b c", nonzero=True)
    w = Matrix(3, 3, symbols("w0:9"))
    z = Matrix([z1, z2, z3])
    row_minus_column = w*z-w.T*z
    d12, d13, d23 = w[0, 1]-w[1, 0], w[0, 2]-w[2, 0], w[1, 2]-w[2, 1]
    assert (z3*(a**3*d12+b**3*d13+c**3*d23)
            -(z3*a**3-z2*b**3+z1*c**3)*d12
            -b**3*row_minus_column[0]-c**3*row_minus_column[1]).expand() == 0


@pytest.mark.parametrize("prime", [7, 13, 19, 31, 37, 43, 61, 67, 73, 97])
def test_scalar_curve_point_count_and_nonzero_coordinates_exhaustively(prime):
    cubes = {pow(x, 3, prime) for x in range(1, prime)}
    for z in range(1, prime):
        if z in cubes:
            continue
        reps = (1, z, z*z % prime)
        accepted = [b for b in range(prime)
                    if (reps[1]*pow(b, 3, prime)-reps[2]) % prime in cubes]
        points = 3*len(accepted)
        assert prime+1-isqrt(4*prime) <= points <= prime+1+isqrt(4*prime)
        assert Fraction(len(accepted), prime) >= Fraction(1, 9)
        # If one coordinate vanished, the other two would require a cube
        # ratio between distinct cosets. No affine chart loses a point.
        for zi, zj in permutations(reps, 2):
            assert (-zi*pow(zj, -1, prime)) % prime not in cubes
        assert 0 not in accepted


@pytest.mark.parametrize("prime,rank", [(7, 1), (7, 2), (13, 3), (43, 5),
                                       (97, 8), (2**127-1, 4)])
def test_two_level_witness_on_original_full_rank_equations(prime, rank):
    rng = random.Random(1807)
    count = solver.cubic_arity(rank, construction="two_level_curve")
    columns = [tuple(int(i == j) for i in range(rank)) for j in range(rank)]
    columns += [tuple(rng.randrange(prime) for _ in range(rank)) for _ in range(count-rank)]
    before = tuple(columns)
    result = solver.cubic_weights(prime, columns, construction="two_level_curve", rng=rng)
    assert tuple(columns) == before
    assert result.compressed_rank == rank
    assert result.required_columns == (rank+1)*(2*rank+1)
    assert result.required_columns < solver.cubic_arity(rank)
    assert result.method == "two_level_curve_contraction"
    assert result.collision_nodes == 2*rank+2
    assert result.checked_axis_relations == 2*rank+7
    assert result.distinguished_cell_nonempty
    assert result.curve_draws > 0 and all(result.curve_scales)
    assert result.curve_abort_bound == Fraction(8, 9)**256
    assert result.sampling_abort_bound == Fraction(1, 3**128)+Fraction(8, 9)**256
    solver.verify_cubic_witness(prime, columns, result.weights)


def test_all_rank_one_input_pairs_with_padding_not_only_random_columns():
    for first, second in product(range(7), repeat=2):
        columns = [(first,), (second,)]*4
        result = solver.cubic_weights(7, columns, construction="two_level_curve",
                                      rng=random.Random(21))
        assert any(result.weights)
        solver.verify_cubic_witness(7, columns, result.weights)


def test_rank_compression_extra_inputs_and_bijective_case():
    columns = [(a % 43, 2*a % 43, 5*a % 43, 0) for a in range(1, 13)]
    result = solver.cubic_weights(43, columns, construction="two_level_curve", rng=random.Random(4))
    assert result.compressed_rank == 1 and result.required_columns == 6
    assert result.weights[6:] == (0,)*6
    solver.verify_cubic_witness(43, columns, result.weights)
    result = solver.cubic_weights(11, [(1, 0), (0, 1), (2, 3)], construction="two_level_curve")
    assert result.method == "bijective_cube" and result.required_columns == 3
    assert result.curve_draws == 0 and result.sampling_abort_bound == 0
    result = solver.cubic_weights(7, [(0, 0)], construction="two_level_curve")
    assert result.method == "zero_rank" and result.weights == (1,)


def test_weighted_controller_uses_new_budget_and_forwards_curve_cap():
    from theorems.weighted_two_erasure_cascade import (
        required_bezout_arity, solve_bezout_sde_weights, verify_general_degree_witness,
    )
    assert required_bezout_arity(43, 15, 2) == 15
    rng = random.Random(4)
    columns = [(1, 0), (0, 1)]+[tuple(rng.randrange(43) for _ in range(2)) for _ in range(13)]
    weights, rank, degree, _ = solve_bezout_sde_weights(43, columns, 15, rng=rng)
    assert rank == 2 and degree == 3
    verify_general_degree_witness(43, columns, weights, 15)
    with pytest.raises(ValueError, match="positive curve"):
        solve_bezout_sde_weights(43, columns, 15, curve_attempt_cap=0)


class FixedDraws:
    def __init__(self, value):
        self.value = value
        self.draws = 0

    def randrange(self, start, stop):
        self.draws += 1
        return self.value


def test_curve_sampling_is_capped_and_failures_do_not_replace_input_labels():
    rng = FixedDraws(0)
    with pytest.raises(RuntimeError, match="curve sampler exhausted"):
        solver.ternary_cubic_scales(7, (1, 2, 4), rng=rng, attempt_cap=4)
    assert rng.draws == 4

    class ValidNonresidueBadCurve:
        def randrange(self, start, stop):
            return 2 if start == 1 else 0

    columns = [(1,)]*8
    with pytest.raises(RuntimeError, match="curve sampler exhausted"):
        solver.cubic_weights(7, columns, construction="two_level_curve",
                             rng=ValidNonresidueBadCurve(), curve_attempt_cap=3)
    assert columns == [(1,)]*8


def test_ternary_root_corruption_is_rejected(monkeypatch):
    class BadPolynomial:
        def roots(self):
            return [(0, 1)]
    monkeypatch.setattr(solver, "fmpz_mod_poly_ctx", lambda p: lambda coefficients: BadPolynomial())
    with pytest.raises(ArithmeticError, match="ternary cubic root"):
        solver.ternary_cubic_scales(7, (1, 2, 4), rng=FixedDraws(3))


@pytest.mark.parametrize("prime,reps", [(5, (1, 2, 4)), (3, (1, 1, 1)),
                                      (9, (1, 2, 4)), (7, (1, 1, 4)),
                                      (7, (1, 0, 4)), (7, (1, 2)),
                                      (7, (True, 2, 4))])
def test_invalid_curve_promises_rejected(prime, reps):
    with pytest.raises(ValueError):
        solver.ternary_cubic_scales(prime, reps)


@pytest.mark.parametrize("value", [True, -1, 7])
def test_invalid_curve_randomness_rejected(value):
    with pytest.raises(ValueError, match="noncanonical"):
        solver.ternary_cubic_scales(7, (1, 2, 4), rng=FixedDraws(value))


def test_unknown_construction_and_insufficient_input_fail_closed():
    with pytest.raises(ValueError, match="unknown"):
        solver.cubic_arity(1, construction="unproved")
    with pytest.raises(ValueError, match="need 6"):
        solver.cubic_weights(7, [(1,)]*5, construction="two_level_curve")
    with pytest.raises(ValueError, match="positive curve"):
        solver.cubic_weights(7, [(1,)]*8, construction="two_level_curve", curve_attempt_cap=0)


@pytest.mark.parametrize("kind,basis", [("X+W", [[1, 0, 0, 1]]), ("Z+W", [[0, 0, 1, 1]])])
def test_new_weights_drive_actual_two_stage_source_and_fourier_readout(kind, basis):
    from theorems.rees_complete_instrument import nonbijective_cubic_control
    result = nonbijective_cubic_control(kind, construction="two_level_curve")
    assert result["cubic_method"] == "two_level_curve_contraction"
    assert [stage["raw_conditional_input_count"] for stage in result["stages"]] == [6, 9]
    assert result["recovered_basis"] == basis
    assert result["full_original_subspace_recovered"]
    assert result["fourier_mass"] == pytest.approx(1)
    assert result["selected_nonzero_records_not_iid_sampling"]
    assert not result["all_label_tuples_checked"]
    assert not result["tuple_oracle_source_replayed"]


def test_cli_report_persists_exact_controls_without_discovery_promotion(tmp_path, capsys):
    from argparse import ArgumentParser
    import json
    from qsearch_cli.commands.sde import add_cubic_sde
    parser = ArgumentParser()
    parser.set_defaults(root=tmp_path)
    add_cubic_sde(parser.add_subparsers(dest="command", required=True))
    args = parser.parse_args(["cubic-sde", "--write"])
    assert args.func(args) == 0
    printed = json.loads(capsys.readouterr().out)
    saved = json.loads((tmp_path/"research/reductions/cubic_diagonal_solver.json").read_text())
    assert printed == saved
    assert all(case["exact_original_moment_verified"] for case in saved["two_level_cases"])
    assert not saved["two_level_uses_random_input_promise"]
    assert not saved["novelty_established"] and not saved["speedup_claim_allowed"]
