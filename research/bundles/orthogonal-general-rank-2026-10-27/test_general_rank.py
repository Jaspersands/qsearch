from fractions import Fraction
from itertools import combinations, product
import random

from flint import fmpz_mat
import pytest

import general_rank as gr
from controls import changed_frame, expected_kernel, kernel_fiber_control

op = gr.op


@pytest.mark.parametrize("n,k,p,index", [(3, 1, 3, 0), (3, 1, 3, 1), (3, 1, 3, 3),
                                      (3, 2, 3, 0), (3, 2, 3, 2), (3, 2, 3, 3),
                                      (4, 3, 3, 0), (4, 3, 3, 3), (4, 3, 3, 4),
                                      (4, 4, 3, 0), (4, 4, 3, 4)])
def test_all_three_kernels_and_every_fiber(n, k, p, index):
    record = kernel_fiber_control(n, k, p, op.eye(2*n)[index])
    dimensions = {"in_U": 2*n-2, "perpendicular_not_in_U": 2*n-2-k, "good": k-1}
    assert record["kernel_rank"] == dimensions[record["case"]]


@pytest.mark.parametrize("n,k,p", [(4, 3, 3), (5, 3, 5), (5, 4, 7), (5, 5, 3),
                                   (8, 3, 2**61-1), (8, 6, 2**127-1)])
def test_rotated_generic_geometry_and_legal_certificate(n, k, p):
    frame = changed_frame(n, p)
    hidden = op.image(frame, op.eye(2*n)[:k], p)
    probes = [op.make_probe(op.mv(frame, op.eye(2*n)[n+i], p), p) for i in range(3)]
    neighbors = []
    for probe in probes:
        kernel, kind = expected_kernel(probe, hidden)
        assert kind == "good" and len(kernel) == k-1
        assert all(op.image(probe.matrix(w), hidden, p) == hidden for w in kernel)
        neighbors.append(gr.neighbor(probe, kernel))
    candidate = gr.reconstruct(neighbors, n, p)
    assert candidate == hidden
    certificate = gr.certificate_matrices(candidate, p)
    assert len(certificate) == k*(k-1)+1+2*(n-k)
    assert all(op.is_orthogonal(g, p) and int(fmpz_mat(g).det()) % p == 1 for g in certificate)
    assert all(op.image(g, hidden, p) == hidden for g in certificate)


@pytest.mark.parametrize("n,r,p", [(3, 3, 3), (4, 3, 5), (5, 3, 3), (5, 4, 3), (5, 5, 3)])
def test_certificate_means_containment_across_all_coordinate_hidden_ranks(n, r, p):
    frame = changed_frame(n, p, seed=43)
    candidate = op.image(frame, op.eye(2*n)[:r], p)
    tests = gr.certificate_matrices(candidate, p)
    count = 0
    for k in range(1, n+1):
        for indices in combinations(range(n), k):
            for choices in product((0, 1), repeat=k):
                hidden = op.image(frame, tuple(op.eye(2*n)[i+n*c]
                                              for i, c in zip(indices, choices)), p)
                contains = len(op.basis(candidate+hidden, p)) == k
                assert all(op.image(g, hidden, p) == hidden for g in tests) == contains
                count += 1
    assert count == 3**n-1


def test_certificate_alone_accepts_a_proper_subspace_so_rank_provenance_is_required():
    n, p = 4, 3
    candidate, hidden = op.eye(8)[:3], op.eye(8)[:4]
    assert candidate != hidden
    assert gr.certify_containment(candidate, op.OpaqueFixtureOracle(hidden, p), p)
    for e in (op.eye(8)[0], op.eye(8)[4]):
        kernel, _ = expected_kernel(op.make_probe(e, p), hidden)
        assert len(kernel) >= len(hidden)-1
        assert len(kernel)+1 > len(candidate)


def test_rank_n_minus_one_bad_probes_reconstruct_wrong_maximal_extension_and_are_rejected():
    n, p, hidden = 4, 3, op.eye(8)[:3]
    neighbors = []
    for i in range(3):
        e = op.add(op.eye(8)[3], op.eye(8)[i], p)
        probe = op.make_probe(e, p)
        kernel, kind = expected_kernel(probe, hidden)
        assert kind == "perpendicular_not_in_U" and len(kernel) == n-1
        neighbors.append(gr.neighbor(probe, kernel))
    wrong = gr.reconstruct(neighbors, n, p)
    assert wrong == op.eye(8)[:4] and wrong != hidden
    assert not gr.certify_containment(wrong, op.OpaqueFixtureOracle(hidden, p), p)


def test_other_bad_probes_and_inconsistent_ranks_are_rejected():
    n, p, hidden = 5, 3, op.eye(10)[:3]
    for e in (op.eye(10)[0], op.eye(10)[3]):
        probe = op.make_probe(e, p)
        kernel, _ = expected_kernel(probe, hidden)
        with pytest.raises(ValueError, match="dimension"):
            gr.neighbor(probe, kernel)
    with pytest.raises(ValueError, match="inconsistent"):
        gr.reconstruct([op.eye(10)[:3], op.eye(10)[:4], op.eye(10)[:3]], n, p)


def test_levi_without_central_and_without_cross_tests_have_false_positives():
    n, r, p = 6, 3, 3
    candidate, opposite = op.eye(12)[:r], op.eye(12)[n:n+r]
    middle_singular = op.eye(12)[r:n]
    tests = gr.certificate_matrices(candidate, p)
    levi_count = r*(r-1)
    assert all(op.image(g, opposite, p) == opposite for g in tests[:levi_count])
    assert op.image(tests[levi_count], opposite, p) != opposite
    assert all(op.image(g, middle_singular, p) == middle_singular for g in tests[:levi_count+1])
    assert any(op.image(g, middle_singular, p) != middle_singular for g in tests[levi_count+1:])


@pytest.mark.parametrize("k", [3, 4])
def test_unknown_rank_dense_oracle_controller(k):
    n, p = 4, 3
    hidden = op.image(changed_frame(n, p), op.eye(2*n)[:k], p)
    oracle = op.OpaqueFixtureOracle(hidden, p)
    result = gr.recover_reference(oracle, n, p, seed=91)
    assert result["candidate"] == hidden and result["inferred_rank"] == k
    assert result["containment_certificate_passed"]
    assert not result["hidden_rank_supplied_to_controller"]
    assert not result["quantum_algorithm_executed"]
    tables = sum(r["classical_table_queries"] for trial in result["records"] for r in trial)
    assert oracle.calls > tables >= 3*p**(2*n-2)


def test_ideal_undersampling_returns_superspace_of_actual_kernel():
    n, p, hidden = 4, 3, op.eye(8)[:3]
    probe = op.make_probe(op.eye(8)[4], p)
    actual, _ = expected_kernel(probe, hidden)
    estimated, _ = op.dense_fourier_kernel(probe, op.OpaqueFixtureOracle(hidden, p),
                                         random.Random(13), samples=1)
    assert len(estimated) > len(actual)
    assert len(op.basis(estimated+actual, p)) == len(estimated)


@pytest.mark.parametrize("n,k,q", [(3, 3, 3), (4, 3, 3), (8, 3, 9), (64, 32, 2**61-1)])
def test_constant_success_and_complete_budget(n, k, q):
    assert gr.geometry_probability(n, k, q) >= Fraction(52, 125)
    budget = gr.recovery_budget(n, 3, 40)
    epsilon = Fraction(budget["total_error_target"])
    assert Fraction(budget["geometry_failure_bound"]) <= epsilon/4
    assert Fraction(budget["all_rank_failure_bound"]) <= epsilon/4
    assert not budget["hidden_rank_required"]
    assert not budget["arbitrary_rank_classical_lower_bound_proved"]
    assert "independent_proof_review_completed" not in budget
    assert budget["original_oracle_query_cap"] == (budget["total_fourier_instruments"]+
                                                  budget["trial_cap"]*(n*(n-1)+1)+1)
    assert (Fraction(budget["error_per_complete_fourier_instrument"])*
            budget["total_fourier_instruments"]) == epsilon/4


def test_exact_probe_counts_and_uniform_nonzero_restrictions():
    n, k, p = 4, 3, 3
    counts, total = {}, 0
    for v in product(range(p), repeat=2*n):
        if not any(v) or op.quadratic(v, p):
            continue
        total += 1
        lam = v[n:n+k]
        if any(lam):
            counts[lam] = counts.get(lam, 0)+1
    assert total == (p**n-1)*(p**(n-1)+1)
    assert len(counts) == p**k-1 and set(counts.values()) == {p**(2*n-k-1)}


@pytest.mark.parametrize("n,k", [(3, 1), (3, 2), (3, 3), (4, 3), (4, 4)])
def test_exact_reflection_probability_and_maximal_failure(n, k):
    p, total, hits = 3, 0, 0
    for v in product(range(p), repeat=2*n):
        if op.quadratic(v, p) == 0:
            continue
        total += 1
        hits += not any(v[n:n+k])
    assert Fraction(hits, total) == gr.reflection_hit_probability(n, k, p)
    assert (hits == 0) == (k == n)


def test_no_large_dense_run_or_low_rank_claim():
    with pytest.raises(ValueError, match="dimension cap"):
        gr.recover_reference(lambda _: 0, 8, 127)
    with pytest.raises(ValueError):
        gr.geometry_probability(4, 2, 3)
    with pytest.raises(ValueError, match="rank at least three"):
        gr.certificate_matrices(op.eye(8)[:2], 3)
