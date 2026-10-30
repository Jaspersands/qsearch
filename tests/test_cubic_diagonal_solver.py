"""All-input cubic construction controls, including real three-coset primes."""
from fractions import Fraction
import random

import pytest

import theorems.cubic_diagonal_solver as solver
from theorems.cubic_diagonal_solver import cubic_arity, cubic_weights, verify_cubic_witness
from theorems.rees_complete_instrument import ReesFiliformFixture, nonbijective_cubic_control
from theorems.rees_hsp_reduction import _units, make_rees_cover
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra
from theorems.nonlinear_jet_erasure import TaylorJetChart
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket
from theorems.weighted_two_erasure_cascade import (
    PinnedWeightedPacket, required_bezout_arity, solve_bezout_sde_weights,
    verify_general_degree_witness, weighted_erasure_stage,
)


@pytest.mark.parametrize("prime,rank", [(7, 1), (7, 2), (13, 2), (43, 3), (2**127-1, 3)])
def test_nonbijective_cube_backend_checks_every_original_moment(prime, rank):
    rng = random.Random(1807)
    columns = [tuple(rng.randrange(prime) for _ in range(rank)) for _ in range(cubic_arity(rank))]
    before = tuple(columns)
    result = cubic_weights(prime, columns, rng=rng)
    assert tuple(columns) == before
    assert result.method == "three_coset_collision"
    assert result.distinguished_cell_nonempty
    assert result.collision_nodes == 1+(9*rank+1)+(9*rank+1)*(3*rank+1)
    assert result.checked_axis_relations > 0
    assert result.root_calls > 0
    assert result.nonresidue_abort_bound == Fraction(1, 3**128)
    assert len(result.weights) == len(columns) and any(result.weights)
    for row in zip(*columns):
        assert sum(a*pow(s, 3, prime) for a, s in zip(row, result.weights)) % prime == 0


@pytest.mark.parametrize("prime", [5, 11, 101])
def test_bijective_cube_branch_remains_a_distinct_small_arity_algorithm(prime):
    columns = [(1, 0), (0, 1), (2, 3)]
    result = cubic_weights(prime, columns)
    assert result.method == "bijective_cube"
    assert result.required_columns == 3
    assert result.nonresidue_draws == result.root_calls == result.collision_nodes == 0
    assert result.nonresidue_abort_bound == 0
    verify_cubic_witness(prime, columns, result.weights)


def test_linear_dependence_is_not_a_cubic_witness_at_a_three_coset_prime():
    columns = [(1,), (2,)]
    assert (5+2) % 7 == 0
    with pytest.raises(ArithmeticError, match="moment"):
        verify_cubic_witness(7, columns, (5, 1))
    with pytest.raises(ValueError, match="80"):
        cubic_weights(7, columns)


@pytest.mark.parametrize("prime,degree", [(43, 3), (43, 9), (43, 15), (2**127-1, 15)])
def test_existing_bezout_adapter_lifts_cubic_solutions_without_changing_labels(prime, degree):
    rng = random.Random(207)
    count = required_bezout_arity(prime, degree, 2)
    assert count == cubic_arity(2, construction="two_level_curve")
    columns = [tuple(rng.randrange(prime) for _ in range(2)) for _ in range(count)]
    weights, rank, reduced, lift = solve_bezout_sde_weights(prime, columns, degree, rng=rng)
    assert reduced == 3 and rank == 2
    verify_general_degree_witness(prime, columns, weights, degree)
    assert pow(pow(5, lift, prime), degree, prime) == pow(5, 3, prime)


def test_higher_coset_and_unimplemented_quadratic_regimes_still_fail_closed():
    for prime, degree in ((43, 6), (43, 7), (13, 4), (13, 2)):
        with pytest.raises(ValueError):
            required_bezout_arity(prime, degree, 1)
        with pytest.raises(ValueError):
            solve_bezout_sde_weights(prime, [(1,)]*100, degree)


def test_pinned_weighted_erasure_uses_three_cosets_without_hidden_parameter_access(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("unknown phase coefficients were accessed")
    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    p, rng = 43, random.Random(419)
    chart = TaylorJetChart(p=p, quotient_width=1, noncentral_width=1, degree=3)
    exponent = (3,)+(0,)*chart.jet_width
    packets = [PinnedWeightedPacket(
        "cubic-p43", "fixed-chart", chart,
        SymbolicScalarPacket(p, 1, chart.jet_width, ((0, (1,)),),
                             {(exponent, (0,)): (i+1) % p}),
    ) for i in range(cubic_arity(1))]
    outcomes = [([rng.randrange(p)], [rng.randrange(p) for _ in range(chart.jet_width)])
                for _ in packets]
    merged, weights, rank, equations = weighted_erasure_stage(packets, 3, outcomes, rng=rng)
    assert rank == equations == 1 and any(weights)
    assert merged.weighted_degree <= 2
    assert not merged.consumed and all(pkt.consumed for pkt in packets)


def test_rank_compression_preserves_original_equations_and_all_input_positions():
    columns = [(a % 43, 2*a % 43, 5*a % 43, 0) for a in range(1, 84)]
    result = cubic_weights(43, columns, rng=random.Random(4))
    assert result.compressed_rank == 1
    assert result.required_columns == 80
    assert result.weights[80:] == (0, 0, 0)
    verify_cubic_witness(43, columns, result.weights)
    zero = cubic_weights(43, [(0, 0)])
    assert zero.method == "zero_rank" and zero.weights == (1,)


def test_zero_columns_and_repeated_columns_do_not_break_nonempty_certificate():
    for value in (0, 1, 2, 3, 6):
        columns = [(value,)]*80
        result = cubic_weights(7, columns, rng=random.Random(11))
        verify_cubic_witness(7, columns, result.weights)
        assert any(result.weights)


class _AllCubes:
    def __init__(self):
        self.draws = 0

    def randrange(self, start, stop):
        self.draws += 1
        return 1


def test_capped_bad_randomness_aborts_without_replacing_any_input_label():
    rng = _AllCubes()
    columns = [(1,)]*80
    with pytest.raises(RuntimeError, match="exhausted"):
        cubic_weights(7, columns, rng=rng, nonresidue_attempt_cap=3)
    assert rng.draws == 3
    assert columns == [(1,)]*80


def test_incorrect_root_backend_fails_closed(monkeypatch):
    class BrokenPolynomial:
        def roots(self):
            return [(0, 1)]
    monkeypatch.setattr(solver, "fmpz_mod_poly_ctx", lambda p: lambda coefficients: BrokenPolynomial())
    with pytest.raises(ArithmeticError, match="cube root"):
        cubic_weights(7, [(1,)]*80, rng=random.Random(11))


def test_original_matrix_is_checked_even_if_row_compression_lies(monkeypatch):
    monkeypatch.setattr(solver, "independent_columns_exact", lambda columns, p: ([[0]], 0))
    with pytest.raises(ArithmeticError, match="original columns"):
        cubic_weights(7, [(1,)])


@pytest.mark.parametrize("prime,columns", [(3, [(1,)]), (9, [(1,)]), (7, []),
                                           (7, [()]), (7, [(7,)]), (7, [(True,)]),
                                           (7, [(1,), (1, 2)])])
def test_invalid_field_or_label_promises_rejected(prime, columns):
    with pytest.raises(ValueError):
        cubic_weights(prime, columns)


def test_f7_fixture_independently_matches_the_lie_rees_compiler():
    p = 7
    half, sixth = pow(2, -1, p), pow(6, -1, p)
    def bracket(a, b):
        return 0, 0, (a[0]*b[1]-a[1]*b[0]) % p, (a[0]*b[2]-a[2]*b[0]) % p
    cover = make_rees_cover(PublicLieAlgebra(p, 4, bracket), _units(4))
    group, rng = ReesFiliformFixture(p=p), random.Random(17)
    def encode(logarithm):
        a, b, c = cover.coefficients(logarithm)
        x, y, z, w = a
        u, v, t = b[2], b[3], c[3]
        return x, y, z, w, (u+half*x*y) % p, (v+half*x*z) % p, (t+half*x*u+sixth*x*x*y) % p
    for _ in range(30):
        a, b = (tuple(rng.randrange(p) for _ in range(7)) for _ in range(2))
        assert encode(cover.multiply(a, b)) == group.mul(encode(a), encode(b))
        assert group.mul(encode(a), group.inv(encode(a))) == group.identity
        for s in range(1, p):
            assert encode(cover.dilate(a, s)) == group.dilate(encode(a), s)
    with pytest.raises(ValueError, match="bounded"):
        ReesFiliformFixture(p=43)


@pytest.mark.parametrize("kind,initial_support,basis", [
    ("X+W", 7, [[1, 0, 0, 1]]), ("Z+W", 49, [[0, 0, 1, 1]]),
])
def test_solver_scales_drive_actual_instruments_and_original_fourier_recovery(kind, initial_support, basis):
    result = nonbijective_cubic_control(kind)
    assert result["prime"] == 7 and result["cubic_method"] == "three_coset_collision"
    assert result["initial_regular_support_size"] == initial_support
    assert result["cubic_root_calls"] > 0 and result["cubic_collision_nodes"] > 0
    assert result["recovered_basis"] == basis and result["full_original_subspace_recovered"]
    assert result["final_fourier_support_size"] == 7**3
    assert result["fourier_mass"] == pytest.approx(1)
    assert all(row["maximum_regular_coefficient_error"] < 1e-11 for row in result["stages"])
    assert [row["raw_conditional_input_count"] for row in result["stages"]] == [80, 9]
    assert result["selected_nonzero_records_not_iid_sampling"]
    assert result["original_input_is_explicit_finite_coset_density"]
    assert not result["all_label_tuples_checked"]
    assert not result["tuple_oracle_source_replayed"]


def test_report_does_not_promote_known_arithmetic_to_a_quantum_discovery():
    result = solver.report()
    assert result["cubic_all_prime_backend_implemented"]
    for key in ("general_degree_backend_implemented", "field_enumeration_used",
                "full_quantum_receiver_implemented", "independent_review",
                "novelty_established", "speedup_claim_allowed"):
        assert result[key] is False
