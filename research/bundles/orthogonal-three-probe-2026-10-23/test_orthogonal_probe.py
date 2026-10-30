from collections import deque
from itertools import product
from fractions import Fraction
import random

import pytest

import orthogonal_probe as op


def standard(n):
    return op.eye(2*n)[:n]


def swap_pair(n, index):
    g = [list(row) for row in op.eye(2*n)]
    g[index], g[index+n] = g[index+n], g[index]
    return tuple(tuple(row) for row in g)


def all_maximal(n, p):
    start = standard(n)
    generators = op.certificate_matrices(start, p)
    generators += tuple(swap_pair(n, i) for i in range(n))
    found, queue = {start}, deque([start])
    while queue:
        current = queue.popleft()
        for g in generators:
            moved = op.image(g, current, p)
            if moved not in found:
                found.add(moved)
                queue.append(moved)
    return tuple(sorted(found))


def coordinates(v, rows, p):
    width = len(rows)
    equations = [tuple(column)+(value,) for column, value in zip(zip(*rows), v)]
    reduced = op.basis(equations, p)
    if any(not any(row[:-1]) and row[-1] for row in reduced):
        raise ValueError("not in coordinate span")
    result = [0]*width
    for row in reduced:
        pivot = next(i for i, value in enumerate(row[:-1]) if value)
        result[pivot] = row[-1]
    return tuple(result)


def expected_kernel(probe, hidden):
    """Supplied-secret algebra control, NEVER a learner or oracle implementation."""
    p, d = probe.p, len(probe.e)
    if len(op.basis(hidden+(probe.e,), p)) == len(hidden):
        return op.eye(d-2)
    perpendicular = op.nullspace((probe.e[d//2:]+probe.e[:d//2],), d, p)
    section = op.intersection(hidden, perpendicular, d, p)
    projected = [op.add(v, op.scale(-op.polar(probe.dual, v, p), probe.e, p), p)
                 for v in section]
    return op.basis((coordinates(v, probe.complement, p) for v in projected), p)


@pytest.fixture(scope="module")
def spaces():
    result = all_maximal(3, 3)
    assert len(result) == 80
    return result


@pytest.mark.parametrize("p,n", [(3, 3), (5, 3), (7, 4), (2**127-1, 8)])
def test_legal_additive_probe_and_injective_parameters(p, n):
    rng = random.Random(190)
    for _ in range(8):
        probe = op.make_probe(op.random_singular(n, p, rng), p)
        a = tuple(rng.randrange(p) for _ in range(probe.width))
        b = tuple(rng.randrange(p) for _ in range(probe.width))
        ga, gb = probe.matrix(a), probe.matrix(b)
        assert op.is_orthogonal(ga, p)
        assert op.mm(ga, gb, p) == probe.matrix(op.add(a, b, p))
        assert op.mv(ga, probe.e, p) == probe.e
        assert (ga == op.eye(2*n)) == (not any(a))


def test_kernel_and_all_oracle_fibers_for_all_f3_singular_probes():
    p, n, hidden = 3, 3, standard(3)
    count = 0
    for e in product(range(p), repeat=2*n):
        if not any(e) or op.quadratic(e, p):
            continue
        probe = op.make_probe(e, p)
        kernel = expected_kernel(probe, hidden)
        oracle = op.OpaqueFixtureOracle(hidden, p)
        origin = oracle(op.eye(2*n))
        actual = []
        labels = {}
        for w in product(range(p), repeat=probe.width):
            label = oracle(probe.matrix(w))
            labels.setdefault(label, []).append(w)
            in_kernel = len(op.basis(kernel+(w,), p)) == len(kernel)
            assert (label == origin) == in_kernel
            if label == origin:
                actual.append(w)
        assert op.basis(actual, p) == kernel
        for fiber in labels.values():
            assert len(fiber) == p**len(kernel)
            assert all(len(op.basis(kernel+(op.add(w, op.scale(-1, fiber[0], p), p),), p))
                       == len(kernel) for w in fiber)
        count += 1
    assert count == 260


def test_three_probe_geometry_exhausts_all_eighty_hidden_spaces(spaces):
    probes = [op.make_probe(op.eye(6)[3+i], 3) for i in range(3)]
    good = 0
    for hidden in spaces:
        rows = [tuple(op.polar(probe.e, v, 3) for v in hidden) for probe in probes]
        if len(op.basis(rows, 3)) != 3:
            continue
        neighbors = [probe.neighbor(expected_kernel(probe, hidden)) for probe in probes]
        assert op.reconstruct_neighbors(neighbors, 3, 3) == hidden
        good += 1
    assert good == 27


def test_certificate_accepts_exactly_one_of_all_eighty_spaces(spaces):
    tested = 0
    for candidate in spaces:
        certificate = op.certificate_matrices(candidate, 3)
        assert len(certificate) == 7
        assert all(op.is_orthogonal(g, 3) for g in certificate)
        for hidden in spaces:
            accepted = all(op.image(g, hidden, 3) == hidden for g in certificate)
            assert accepted == (candidate == hidden)
            tested += 1
    assert tested == 6400


def test_levi_only_certificate_has_an_explicit_false_positive():
    candidate, opposite = standard(3), op.eye(6)[3:]
    matrices = op.certificate_matrices(candidate, 3)
    assert all(op.image(g, opposite, 3) == opposite for g in matrices[:-1])
    assert op.image(matrices[-1], opposite, 3) != opposite
    assert not op.certify(candidate, op.OpaqueFixtureOracle(opposite, 3), 3)


@pytest.mark.parametrize("index", [0, 17, 39, 79])
def test_dense_reference_recovers_using_only_opaque_labels(spaces, index):
    oracle = op.OpaqueFixtureOracle(spaces[index], 3)
    result = op.recover_reference(oracle, 3, 3, seed=83, attempts=12, samples=18)
    assert result["candidate"] == spaces[index]
    assert result["certificate_passed"]
    tables = sum(record["classical_table_queries"]
                 for attempt in result["records"] for record in attempt)
    assert tables > 0 and oracle.calls > tables
    for attempt in result["records"]:
        for record in attempt:
            assert abs(record["probability_sum"]-1) < 1e-10
            assert record["fiber_sizes"] in ([9], [81])
            assert record["fourier_support_size"] in (9, 1)


def test_incomplete_kernel_is_not_promoted_to_a_neighbor():
    probe = op.make_probe(op.eye(6)[3], 3)
    with pytest.raises(ValueError, match="complete kernel"):
        probe.neighbor(((1, 0, 0, 0),))


def test_low_rank_geometric_reconstruction_is_rejected():
    with pytest.raises(ValueError, match="rank at least three"):
        op.reconstruct_neighbors([standard(2)]*3, 2, 3)


def test_low_rank_classical_chart_kernel_is_not_just_scalar():
    # SL2's elementary Levi fixes EVERY alternating graph in rank two.
    p, n = 5, 2
    g = op.certificate_matrices(standard(n), p)[0]
    assert g != op.eye(4)
    for t in range(p):
        graph = op.basis(((1, 0, 0, -t % p), (0, 1, t, 0)), p)
        assert op.image(g, graph, p) == graph


def test_noncentral_fixed_chart_bound_for_structural_controls():
    p, n = 5, 3
    graphs = []
    for a, b, c in product(range(p), repeat=3):
        s = ((0, a, b), (-a % p, 0, c), (-b % p, -c % p, 0))
        graphs.append(op.basis([op.eye(n)[i]+tuple(s[j][i] for j in range(n))
                                for i in range(n)], p))
    tests = op.certificate_matrices(standard(n), p) + (swap_pair(n, 0),)
    for g in tests:
        fixed = sum(op.image(g, graph, p) == graph for graph in graphs)
        assert fixed*p <= 2*len(graphs)
    assert all(op.image(op.eye(6), graph, p) == graph for graph in graphs)


def test_dense_reference_does_not_claim_scalable_simulation():
    probe = op.make_probe(op.eye(16)[8], 127)
    with pytest.raises(ValueError, match="dimension cap"):
        op.dense_fourier_kernel(probe, lambda _: 0, random.Random(1))


def test_sampling_formula_and_nonzero_singular_outputs():
    for p, n in ((3, 3), (5, 3), (7, 4), (2**127-1, 8)):
        rng = random.Random(912)
        for _ in range(50):
            vector = op.random_singular(n, p, rng)
            assert any(vector) and op.quadratic(vector, p) == 0
        y_zero_probability = Fraction(1, p**(n-1)+1)
        zero_branch_mass_per_vector = y_zero_probability / (p**n-1)
        other_branch_mass_per_vector = (1-y_zero_probability) / ((p**n-1)*p**(n-1))
        assert zero_branch_mass_per_vector == other_branch_mass_per_vector
        assert zero_branch_mass_per_vector == Fraction(1, (p**n-1)*(p**(n-1)+1))


def test_hyperbolic_completion_at_large_prime():
    p, n = 2**127-1, 8
    rng = random.Random(87)
    hidden = standard(n)
    for _ in range(9):
        probe = op.make_probe(op.random_singular(n, p, rng), p)
        g = probe.matrix(tuple(rng.randrange(p) for _ in range(probe.width)))
        hidden = op.image(g, hidden, p)
    frame = op.hyperbolic_frame(hidden, p)
    assert op.is_orthogonal(frame, p)
    assert op.image(frame, standard(n), p) == hidden
    probes = [op.make_probe(op.random_singular(n, p, rng), p) for _ in range(3)]
    rows = [tuple(op.polar(probe.e, v, p) for v in hidden) for probe in probes]
    assert len(op.basis(rows, p)) == 3
    neighbors = [probe.neighbor(expected_kernel(probe, hidden)) for probe in probes]
    recovered = op.reconstruct_neighbors(neighbors, n, p)
    assert recovered == hidden
    assert all(op.image(g, hidden, p) == hidden for g in op.certificate_matrices(recovered, p))


def test_full_oracle_reference_beyond_the_rank_three_accidental_isomorphism():
    n, p = 4, 3
    hidden = op.image(swap_pair(n, 0), standard(n), p)
    oracle = op.OpaqueFixtureOracle(hidden, p)
    result = op.recover_reference(oracle, n, p, seed=83, attempts=12, samples=22)
    assert result["candidate"] == hidden
    assert oracle.calls > p**(2*n-2)


@pytest.mark.parametrize("p,n,bits", [(3, 3, 12), (13, 8, 40), (2**127-1, 64, 64)])
def test_complete_proposed_query_and_error_accounting(p, n, bits):
    budget = op.recovery_budget(n, p, bits)
    error = Fraction(1, 2**bits)
    total = (Fraction(budget["geometry_failure_bound"])
             + Fraction(budget["all_rank_failure_bound"])
             + budget["total_fourier_instruments"]*Fraction(budget["error_per_complete_fourier_instrument"])
             + Fraction(budget["global_classical_sampling_error_allowance"]))
    assert total <= error
    assert budget["original_oracle_query_cap"] == (
        budget["total_fourier_instruments"]+budget["trial_cap"]*(n*(n-1)+1)+1)
    assert not budget["dense_reference_cost_is_this_budget"]


@pytest.mark.parametrize("p", [2, 9, True])
def test_invalid_field_rejected(p):
    with pytest.raises(ValueError, match="odd prime"):
        op.make_probe(op.eye(6)[0], p)


@pytest.mark.parametrize("n", [2, 3, 4])
@pytest.mark.parametrize("p", [3, 5, 127])
def test_exact_linearized_common_chart_stabilizer(n, p):
    linear, quadratic = [], []
    for a in range(n):
        for b in range(a+1, n):
            t = [[0]*n for _ in range(n)]
            t[a][b], t[b][a] = 1, -1 % p
            for i in range(n):
                for j in range(n):
                    row = [0]*(2*n*n)
                    for k in range(n):
                        row[k*n+j] = (row[k*n+j]-t[i][k]) % p
                        row[n*n+i*n+k] = (row[n*n+i*n+k]+t[k][j]) % p
                    linear.append(tuple(row))
                    quadratic.append(tuple(t[i][k]*t[l][j] % p
                                           for k in range(n) for l in range(n)))
    ad_space = op.nullspace(linear, 2*n*n, p)
    b_space = op.nullspace(quadratic, n*n, p)
    assert len(ad_space) == (4 if n == 2 else 1)
    assert not b_space
    if n >= 3:
        identity = tuple(int(i == j) for i in range(n) for j in range(n))
        assert op.basis(ad_space, p) == op.basis((identity+identity,), p)
