"""Falsifier fixtures for a public reduction, not quantum algorithm runs."""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
import random

import numpy as np
import pytest

from theorems.central_character_descent import HeisenbergFixture, check_moment, controlled_discard, exhaustive_scale_fixture
from theorems.class_three_ambient_frontend import _subspace_intersection
from theorems.jet_oracle_homogenization import lie_bch
from theorems.rees_hsp_reduction import make_rees_cover, recovery_budget, black_box_large_prime_budget, _units
from theorems.right_abelian_induced_source import upper_triangular_lie, derived_length_three_witness
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra, _fmpz_solve_coordinates
from theorems.uniform_bch_rees import scalar_line_budget
from tests.test_ambient_section_potential import _matrix_exp, _matrix_log, _matrix_multiply


def test_public_cover_multiplication_uses_uniform_bch_not_word_expansion(monkeypatch):
    import theorems.rees_hsp_reduction as module
    import theorems.jet_oracle_homogenization as old_backend
    from tests.test_uniform_bch_rees import _filiform
    from theorems.uniform_bch_rees import bch_via_ode
    c, p = 8, 11
    dimension, matrix, bracket = _filiform(c, p)
    cover = make_rees_cover(PublicLieAlgebra(p, dimension, bracket), _units(dimension))
    calls = 0

    def forbidden(*args, **kwargs):
        raise AssertionError("word expansion must not implement growing-class multiplication")

    def checked(left, right, *, prime, nilpotency_class, bracket):
        nonlocal calls
        calls += 1
        assert nilpotency_class == c and prime == p
        return bch_via_ode(left, right, prime=prime,
                          nilpotency_class=nilpotency_class, bracket=bracket)

    monkeypatch.setattr(old_backend, "lie_bch", forbidden)
    monkeypatch.setattr(module, "bch_via_ode", checked)
    rng = random.Random(20261029)
    left, right = (tuple(rng.randrange(p) for _ in range(cover.dimension)) for _ in range(2))
    output = cover.multiply(left, right)
    assert calls == 1
    for point in cover.points:
        ground_truth = _matrix_log(_matrix_multiply(_matrix_exp(matrix(cover.evaluate(left, point)), p),
                                                   _matrix_exp(matrix(cover.evaluate(right, point)), p), p), p)
        assert matrix(cover.evaluate(output, point)) == tuple(map(tuple, ground_truth))


def test_abelian_cover_multiplication_rejects_wrong_dimension_before_ode():
    cover = make_rees_cover(PublicLieAlgebra(3, 4, lambda a, b: (0,)*4), _units(4))
    assert cover.class_bound == 1 and cover.multiply((1,)*4, (2,)*4) == (0,)*4
    for left, right in (((1,), (2,)), ((1,)*5, (2,)*5),
                        ((1,)*4, (2,)), ((1,), (2,)*4)):
        with pytest.raises(ValueError):
            cover.multiply(left, right)


def span_elements(basis, n, p):
    return {tuple(sum(a*b[j] for a, b in zip(coeff, basis)) % p for j in range(n))
            for coeff in product(range(p), repeat=len(basis))}


def test_black_box_envelope_charges_outer_calls_without_claiming_total_runtime():
    error = Fraction(1, 100)
    budget = black_box_large_prime_budget(7, 3, error)
    assert budget["large_prime_call_cap"] == 56
    # Independent specialization of the published sufficient SDE arities.
    b2 = (2*8**2)**2
    b3 = (3**3*8**3)**2
    t = budget["uniform_fourier_slack"]
    assert 2**t >= 12*56/error > 2**(t-1)
    assert budget["large_prime_original_query_bound"] == 56*3*(7+t)*b2*b3
    assert budget["local_rank_failure_bound"] <= budget["core_error_per_call"]/3
    allocated = (budget["preprocessing_error_allocation"]
                 + 56*(budget["chart_error_per_call"]+budget["core_error_per_call"])
                 + 3*budget["small_prime_error_per_call"])
    assert allocated == budget["total_allocated_error"] == error
    assert budget["conditional_on_rees_core"]
    assert budget["outer_normalizer_recursion_required"]
    for key in ("outer_reduction_implemented", "covers_small_prime_queries",
                "covers_group_preprocessing_cost", "is_total_gate_bound"):
        assert not budget[key]
    assert black_box_large_prime_budget(7, 9)["large_prime_query_dimension_exponent"] == 147


def test_black_box_envelope_handles_abelian_core_and_rejects_invalid_contracts():
    budget = black_box_large_prime_budget(1, 1)
    assert budget["large_prime_original_query_bound"] == 2*(1+budget["uniform_fourier_slack"])
    assert budget["large_prime_query_dimension_exponent"] == 3
    # The outer envelope is deliberately not the tight abelian algorithm.
    for b, c in ((0, 1), (1, 0), (-1, 2), (True, 2), (2, 1.5)):
        with pytest.raises(ValueError):
            black_box_large_prime_budget(b, c)
    for error in (Fraction(0), Fraction(1), Fraction(-1, 3), 0.1):
        with pytest.raises(ValueError):
            black_box_large_prime_budget(3, 2, error)


def test_all_subgroups_of_ut3_including_center_and_full_group_have_exact_lifted_cosets():
    p = 3
    source, slots = upper_triangular_lie(3, p)
    cover = make_rees_cover(source, _units(3))
    assert cover.dimensions == (3, 1) and cover.dimension == 4
    elements = tuple(product(range(p), repeat=4))
    vectors = tuple(product(range(p), repeat=3))
    bases = [tuple(source.span(v)) for k in (0, 1, 2) for v in combinations(vectors, k)]+[_units(3)]
    spaces = {frozenset(span_elements(basis, 3, p)): basis for basis in bases}
    group = HeisenbergFixture(p)
    def matrix(v):
        x, z, y = v
        return x, y, (z+x*y*pow(2, -1, p)) % p
    checked = 0
    for basis in spaces.values():
        h = span_elements(basis, 3, p)
        if any(source.bracket(a, b) not in h for a, b in product(basis, repeat=2)):
            continue
        checked += 1
        H = [matrix(v) for v in h]
        f = {v: min(group.multiply(matrix(v), x) for x in H) for v in vectors}
        fibers = defaultdict(set)
        for a in elements:
            fibers[cover.evaluate_fixture(f.__getitem__, a)].add(a)
        lifted = {a for a in elements if all(row in h for row in cover.coefficients(a))}
        assert len(fibers)*len(lifted) == p**4
        for fiber in fibers.values():
            representative = next(iter(fiber))
            assert fiber == {cover.multiply(representative, h) for h in lifted}
        assert all(cover.dilate(h, 2) in lifted for h in lifted)
        # Grade one retains ORIGINAL central directions, unlike associated graded.
        assert {a[:3] for a in lifted} == h
    assert checked == 19


@pytest.mark.parametrize("p", [5, 17, 2**127-1])
def test_nonabelian_evaluation_homomorphism_against_independent_matrix_bch(p):
    source, slots = upper_triangular_lie(5, p)
    cover = make_rees_cover(source, _units(len(slots)))
    assert cover.dimensions == (10, 6, 3, 1)
    rng = random.Random(2718)
    def matrix(v):
        return [[v[slots.index((i, j))] if (i, j) in slots else 0 for j in range(5)] for i in range(5)]
    for _ in range(3):
        a, b = [tuple(rng.randrange(p) for _ in range(cover.dimension)) for _ in range(2)]
        ab = cover.multiply(a, b)
        for s in cover.points:
            independent = _matrix_log(_matrix_multiply(_matrix_exp(matrix(cover.evaluate(a, s)), p),
                                                       _matrix_exp(matrix(cover.evaluate(b, s)), p), p), p)
            assert cover.evaluate(ab, s) == tuple(independent[i][j] for i, j in slots)
        assert cover.recover_coefficients(cover.inputs(a)) == cover.coefficients(a)
        assert cover.dilate(ab, 2) == cover.multiply(cover.dilate(a, 2), cover.dilate(b, 2))


@pytest.mark.parametrize("p", [7, 2**127-1])
def test_proper_nonabelian_hidden_lie_algebra_is_homogenized_without_transversality(p):
    source, slots = upper_triangular_lie(5, p)
    cover = make_rees_cover(source, _units(10))
    a = tuple(int(ij in ((0, 1), (2, 3))) for ij in slots)
    b = tuple(int(ij in ((1, 2), (3, 4))) for ij in slots)
    hidden = source.span([a, b])
    while True:
        bigger = source.span(hidden+[source.bracket(x, y) for x, y in product(hidden, repeat=2)])
        if len(bigger) == len(hidden):
            break
        hidden = bigger
    assert 2 < len(hidden) < 10 and source.nilpotency_class(hidden) > 1
    lifted = []
    for r, level in enumerate(cover.levels, 1):
        for v in _subspace_intersection(hidden, level, 10, p):
            coords = _fmpz_solve_coordinates(level, v, p)
            lifted.append(tuple(coords[j] if d == r else 0 for d, j in cover.indices))
    assert len(lifted) > len(hidden)
    for x, y in product(lifted, repeat=2):
        assert _fmpz_solve_coordinates(lifted, cover.algebra.bracket(x, y), p) is not None
    for x in lifted:
        assert _fmpz_solve_coordinates(lifted, cover.dilate(x, 3), p) is not None
        assert all(_fmpz_solve_coordinates(hidden, row, p) is not None for row in cover.inputs(x))
    projected = source.span([v[:10] for v in lifted])
    assert len(projected) == len(hidden)
    assert all(_fmpz_solve_coordinates(hidden, v, p) is not None for v in projected)
    rng = random.Random(17)
    for _ in range(8):
        x = tuple(rng.randrange(p) for _ in range(cover.dimension))
        scalars = [rng.randrange(p) for _ in lifted]
        a = tuple(sum(t*v[j] for t, v in zip(scalars, lifted)) % p for j in range(cover.dimension))
        y = cover.multiply(x, a)
        for xx, yy in zip(cover.inputs(x), cover.inputs(y)):
            delta = lie_bch(source, tuple(-t % p for t in xx), yy, 4)
            assert _fmpz_solve_coordinates(hidden, delta, p) is not None


def test_missing_evaluation_and_fake_truncation_are_falsified():
    source, _ = upper_triangular_lie(3, 5)
    cover = make_rees_cover(source, _units(3))
    # (-t+t^2)Z vanishes at 1, but does not have zero coefficients.
    value = (0, 4, 0, 1)
    assert cover.inputs(value)[0] == (0, 0, 0)
    assert cover.inputs(value)[1] != (0, 0, 0)
    assert any(any(v) for v in cover.recover_coefficients(cover.inputs(value)))
    # In fake tL+t^2L, truncating [t^2 X,t Y] kills a NONZERO evaluation.
    X, _, Y = _units(3)
    left, right = {2: X}, {1: Y}
    fake_bracket = {r+s: source.bracket(a, b) for r, a in left.items() for s, b in right.items() if r+s <= 2}
    evaluate_at_one = lambda poly: tuple(sum(row[j] for row in poly.values()) % 5 for j in range(3))
    assert evaluate_at_one(fake_bracket) == (0, 0, 0)
    assert evaluate_at_one(fake_bracket) != source.bracket(evaluate_at_one(left), evaluate_at_one(right))
    with pytest.raises(ValueError, match="nonzero"):
        cover.dilate(value, 0)
    with pytest.raises(ValueError, match="exactly c"):
        cover.recover_coefficients(cover.inputs(value)[:1])


def test_compiler_uses_only_public_constants_and_exactly_c_original_calls():
    source, _ = upper_triangular_lie(4, 5)
    calls = []
    cover = make_rees_cover(source, _units(6))
    cover.evaluate_fixture(lambda x: calls.append(x), (0,)*cover.dimension)
    assert calls == [(0,)*6]*3
    # Alternating but non-Lie input: [e0,e1]=e1, [e1,e2]=e2.
    def bad(a, b):
        return (0, (a[0]*b[1]-a[1]*b[0]) % 5, (a[1]*b[2]-a[2]*b[1]) % 5)
    with pytest.raises(ValueError, match="Jacobi"):
        make_rees_cover(PublicLieAlgebra(5, 3, bad), _units(3))
    small, _ = upper_triangular_lie(4, 3)
    with pytest.raises(ValueError, match="class<p"):
        make_rees_cover(small, _units(6))


@pytest.mark.parametrize("p", [5, 2**127-1])
def test_actual_class_not_loose_upper_bound_controls_evaluations_and_rank_budget(p):
    source, _ = upper_triangular_lie(3, p)
    cover = make_rees_cover(source, _units(3))
    # Review F1: this algebra also satisfies the very loose bound c<=p-1.
    # Only the computed actual class satisfies c<=dim([L,L])+1 uniformly.
    supplied_upper_bound = p-1
    assert cover.dimensions == (3, 1)
    assert cover.class_bound == 2 <= cover.dimensions[1]+1 < supplied_upper_bound
    assert cover.points == (1, 2)
    calls = []
    cover.evaluate_fixture(lambda x: calls.append(x), (0,)*cover.dimension)
    assert calls == [(0, 0, 0)]*2
    budget = scalar_line_budget(cover.dimensions, 1, prime=p)
    assert budget.cover_dimension == 4 and budget.leaves_per_terminal == 3
    assert budget.original_inputs == 6


@pytest.mark.parametrize("kind", ["diagonal", "full"])
def test_nontrivial_central_intersection_full_instrument_and_all_positive_branches(kind):
    # G=UT3(F3) x C3; Z=C3^2; K is diagonal or all of Z.
    # These are full matrices with an actual right-action trace, not target kernels.
    p = 3
    base = HeisenbergFixture(p)
    elements = tuple(product(base.elements, range(p)))
    index = {x: i for i, x in enumerate(elements)}
    def multiply(a, b):
        return base.multiply(a[0], b[0]), (a[1]+b[1]) % p
    def inverse(a):
        return base.inverse(a[0]), -a[1] % p
    def right(g):
        return np.array([index[multiply(x, inverse(g))] for x in elements])
    hidden = {((t, t, (t*t*2+u) % p), u if kind == "diagonal" else v)
              for t, u, v in product(range(p), repeat=3)}
    K = {(x[0][2], x[1]) for x in hidden if x[0][:2] == (0, 0)}
    rho = np.array([[int(multiply(inverse(x), y) in hidden)/len(elements) for y in elements]
                    for x in elements], dtype=complex)
    representatives = tuple((g, 0) for g in base.representatives)
    controls = {s: np.array([right((base.dilate(g, s), s*s*w % p)) for g, w in representatives])
                for s in (1, 2)}
    branches, masses, factors = {}, {}, {}
    for label in product(range(p), repeat=2):
        P = np.zeros_like(rho)
        for z, w in product(range(p), repeat=2):
            P[right(((0, 0, z), w)), np.arange(len(elements))] += np.exp(-2j*np.pi*(label[0]*z+label[1]*w)/p)/p**2
        projected = P @ rho @ P.conj().T
        mass = np.trace(projected).real
        allowed = all((label[0]*z+label[1]*w) % p == 0 for z, w in K)
        assert abs(mass-(len(K)/p**2 if allowed else 0)) < 1e-12
        if not allowed:
            assert np.max(np.abs(projected)) < 1e-12
            continue
        branches[label] = projected/mass
        masses[label] = mass
        for s in (1, 2):
            factors[label, s] = controlled_discard(branches[label], controls[s])*p**2
        # The obsolete transverse normalization gives trace |K|, not 1.
        assert abs(np.trace(p**2*projected)-len(K)) < 1e-12
        for g in elements:
            decompositions = [(z, w) for z, w in product(range(p), repeat=2)
                              if multiply(g, inverse(((0, 0, z), w))) in hidden]
            predicted = np.exp(2j*np.pi*sum(a*b for a, b in zip(label, decompositions[0]))/p) if decompositions else 0
            correlation = sum(branches[label][j, right(g)[j]] for j in range(len(elements)))
            assert abs(correlation-predicted) < 1e-12
    assert abs(sum(masses.values())-1) < 1e-12
    expected = base.expected_quotient_fixture(tuple(g for g, _ in hidden))
    unconditional = np.zeros_like(expected, dtype=complex)
    for labels in product(branches, repeat=3):
        scales = exhaustive_scale_fixture(labels, p, 2)
        active = check_moment(labels, scales, p, 2)
        output = np.prod([factors[labels[i], scales[i]] for i in active], axis=0)/p**2
        assert np.max(np.abs(output-expected)) < 1e-12
        unconditional += np.prod([masses[label] for label in labels])*output
    assert np.max(np.abs(unconditional-expected)) < 1e-12


def test_actual_class_nine_cover_and_whole_resource_accounting():
    source, ambient, _ = derived_length_three_witness(43)
    cover = make_rees_cover(source, ambient)
    assert cover.dimensions == (19, 17, 16, 14, 12, 9, 6, 3, 1)
    assert cover.dimension == 97
    budget = recovery_budget(cover)
    assert budget["queries_per_leaf"] == 9 and budget["final_fourier_samples"] == 20
    assert budget["query_dimension_exponent"] == 145
    assert budget["original_queries"] == 9*budget["source_preparations"]
    assert budget["final_fourier_readout_calls"] == budget["final_fourier_samples"]
    assert budget["complete_instrument_calls"] == (budget["source_preparations"]
        +budget["sde_calls"]+budget["final_fourier_readout_calls"])
    assert budget["classical_sde_abort_bound_per_call"] <= budget["solver_abort_per_call"]
    assert budget["classical_sde_attempt_cap"] == (budget["sde_calls"]
        *budget["classical_sde_attempts_per_call"])
    assert budget["classical_restart_extra_source_copies"] == 0
    assert (budget["rank_failure_bound"]+budget["sde_calls"]*budget["solver_abort_per_call"]
            +budget["complete_instrument_calls"]*budget["instrument_error_per_call"] == budget["total_error_bound"])
    assert budget["total_error_bound"] <= Fraction(1, 3)
    v = tuple((i*i+7) % 43 for i in range(cover.dimension))
    expected = tuple(tuple(sum(x*b[j] for x, b in zip(row, cover.ambient_basis)) % 43 for j in range(source.dimension))
                     for row in cover.coefficients(v))
    assert cover.recover_coefficients(cover.inputs(v)) == expected


def test_abelian_case_is_one_query_and_no_sde_stage():
    source = PublicLieAlgebra(3, 4, lambda a, b: (0,)*4)
    cover = make_rees_cover(source, _units(4))
    budget = recovery_budget(cover)
    assert cover.inputs((1, 2, 0, 1)) == ((1, 2, 0, 1),)
    assert budget["sde_calls"] == 0 and budget["query_dimension_exponent"] == 1
    assert budget["complete_instrument_calls"] == 2*budget["final_fourier_samples"]
    assert budget["classical_sde_attempt_cap"] == 0
    assert budget["classical_sde_abort_bound_per_call"] == 0
    assert budget["original_queries"] == budget["final_fourier_samples"]


def test_solver_confidence_clock_is_logarithmic_and_does_not_reprepare_sources():
    source, _ = upper_triangular_lie(3, 5)
    cover = make_rees_cover(source, _units(3))
    error = Fraction(1, 2**4096)
    budget = recovery_budget(cover, error)
    calls = budget["sde_calls"]
    attempts = budget["classical_sde_attempts_per_call"]
    assert attempts == 4096+(3*calls-1).bit_length()
    assert calls*Fraction(1, 2**attempts) <= error/3
    assert calls*Fraction(1, 2**(attempts-1)) > error/3
    assert budget["classical_restart_extra_source_copies"] == 0
    assert budget["original_queries"] == cover.class_bound*budget["source_preparations"]
    assert budget["complete_instrument_calls"]*budget["instrument_error_per_call"] == error/3
    assert budget["total_error_bound"] <= error


def test_nonmetabelian_derived_algebra_is_not_excluded_by_the_public_compiler():
    source, slots = upper_triangular_lie(9, 11)
    cover = make_rees_cover(source, _units(len(slots)))
    assert cover.dimensions == (36, 28, 21, 15, 10, 6, 3, 1)
    assert cover.dimension == 120
    def unit(i, j):
        return tuple(int(ij == (i, j)) for ij in slots)
    x, y, u, v = [unit(i, i+2) for i in (0, 2, 4, 6)]
    witness = source.bracket(source.bracket(x, y), source.bracket(u, v))
    assert witness == unit(0, 8)  # [L',L'] is itself nonabelian.
    def grade_two(value):
        coords = _fmpz_solve_coordinates(cover.levels[1], value, 11)
        return tuple(coords[j] if r == 2 else 0 for r, j in cover.indices)
    xx, yy, uu, vv = map(grade_two, (x, y, u, v))
    lifted = cover.algebra.bracket(cover.algebra.bracket(xx, yy), cover.algebra.bracket(uu, vv))
    assert any(lifted)
    assert all(r == 8 for a, (r, _) in zip(lifted, cover.indices) if a)
    assert cover.evaluate(lifted, 3) == tuple(pow(3, 8, 11)*a % 11 for a in witness)
