from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random

import numpy as np
import pytest

from theorems import gibbs_orbit_parent as audit
from theorems.coherent_local_gibbs import CodeProblem


@pytest.mark.parametrize("width", (1, 2, 3, 6))
@pytest.mark.parametrize("c", ("0", "1/5", "13/20", "4/5"))
def test_actual_local_readout_is_the_deformed_code_complement(width, c):
    record = audit.local_deformed_code_control(width, c)
    assert record["deformed_code_complement_residual"] < 1e-12
    assert record["local_gate_unitarity_residual"] < 1e-12
    assert record["projector_idempotence_residual"] < 1e-12
    term, _ = audit.local_projector(width, c)
    off_diagonal = term-np.diag(np.diag(term))
    assert np.max(off_diagonal) <= 1e-12
    assert np.trace(term) == pytest.approx(2**(width-1))


@pytest.mark.parametrize("problem", (
    CodeProblem(5, (25, 26, 12)),
    CodeProblem(5, (25, 26, 12, 25, 0)),
    CodeProblem(4, (7, 14, 9)),
    CodeProblem(3, (0, 0)),
))
@pytest.mark.parametrize("c", ("0", "1/5", "13/20"))
def test_every_sector_and_actual_global_orbit_span(problem, c):
    record = audit.sector_control(problem, c)
    assert record["parent_ground_dimension_exact"] == 2**len(problem.structure[0])
    assert record["parent_ground_dimension_numerical"] == record["parent_ground_dimension_exact"]
    assert record["actual_source_orbit_span_residual"] < 1e-12
    assert record["parent_annihilates_actual_source_residual"] < 1e-12
    assert sum(r["size"] for r in record["sectors"]) == 2**problem.length
    assert all(r["similarity_max_residual"] < 1e-12 for r in record["sectors"])
    assert record["finite_matrices_are_NOT_asymptotic_gap_evidence"]


@pytest.mark.parametrize("signs", range(16))
def test_exact_spin_gibbs_lumping_including_dependent_and_zero_generators(signs):
    problem, c = CodeProblem(4, (7, 14, 9, 7, 0)), Fraction(13, 20)
    states, pi, kernel = audit.exact_sector_kernel(problem, c, signs)
    index = {y: i for i, y in enumerate(states)}
    spin_count = len(problem.checks)

    def clause_word(x):
        y = signs
        for j, h in enumerate(problem.checks):
            if (x >> j) & 1:
                y ^= h
        return y

    # Independent original spin weights and its heat-bath proposals.
    words = [clause_word(x) for x in range(1 << spin_count)]
    weights = [(33**(problem.length-y.bit_count()))*(7**y.bit_count()) for y in words]
    partition = sum(weights)
    pushforward = [Fraction(0) for _ in states]
    counts = [words.count(y) for y in states]
    assert len(set(counts)) == 1
    for x, y in enumerate(words):
        pushforward[index[y]] += Fraction(weights[x], partition)
        row = [Fraction(0) for _ in states]
        for j in range(spin_count):
            neighbor = x ^ (1 << j)
            probability = Fraction(weights[neighbor], spin_count*(weights[x]+weights[neighbor]))
            row[index[words[neighbor]]] += probability
            row[index[y]] += Fraction(1, spin_count)-probability
        assert row == kernel[index[y]]
        assert pi[index[y]]/counts[index[y]] == Fraction(weights[x], partition)
    assert tuple(pushforward) == pi


def test_c_zero_exact_character_spectrum_checks_normalization_and_gap():
    problem = CodeProblem(5, (25, 26, 12, 25, 0))
    eigenvalues = np.linalg.eigvalsh(audit.parent_matrix(problem, "0"))
    character_values = sorted(Fraction(sum((h & a).bit_count() % 2 for h in problem.checks), len(problem.checks))
                              for a in range(1 << problem.length))
    assert np.allclose(eigenvalues, list(map(float, character_values)), atol=1e-12)
    assert min(v for v in character_values if v) >= Fraction(1, len(problem.checks))


@pytest.mark.parametrize("problem", (CodeProblem(5, (25, 26, 12)), CodeProblem(4, (7, 14, 9))))
@pytest.mark.parametrize("c", ("0", "13/20", "4/5"))
def test_compressed_bit_gap_has_an_exact_all_sector_rational_check(problem, c):
    c = Fraction(c)
    P, reflections, recipe = audit.spectral_readout_reference(problem, c)
    for coordinate in problem.structure[1]:
        visited = set()
        for s in range(1 << problem.length):
            if s in visited:
                continue
            sector = audit.row_orbit(problem, s)
            visited.update(sector)
            opposite = tuple(y ^ (1 << coordinate) for y in sector)
            assert not set(sector).intersection(opposite)
            U = sum(audit.weight((y & ((1 << coordinate)-1)) | ((y >> (coordinate+1)) << coordinate),
                                 problem.length-1, c) for y in sector)
            Z0 = sum(audit.weight(y, problem.length, c) for y in sector)
            Z1 = sum(audit.weight(y, problem.length, c) for y in opposite)
            assert Z0+Z1 == 2*c.denominator*U
            alpha_squared = Fraction((c.denominator**2-c.numerator**2)*U*U, Z0*Z1)
            assert 1-c*c <= alpha_squared <= 1
    for i, A in enumerate(reflections):
        assert np.allclose(A @ A, np.eye(len(P)), atol=1e-12)
        assert np.allclose(A @ P, P @ A, atol=1e-12)
        for B in reflections[i+1:]:
            assert np.allclose(A @ B, B @ A, atol=1e-12)
    assert recipe["theoretical_compressed_gap_lower_squared_exact"] == str(1-c*c)
    assert not recipe["span_reflection_efficiently_compiled"]


def test_two_ancilla_projector_product_is_a_unit_normalized_block_encoding():
    U, C = audit.compressed_block_encoding_reference(CodeProblem(5, (25, 26, 12)), "13/20")
    dimension = len(C)
    assert np.allclose(U.T @ U, np.eye(len(U)), atol=1e-12)
    assert np.allclose(U[:dimension, :dimension], C, atol=1e-12)


@pytest.mark.parametrize("checks", ((25, 26, 12), (25, 26, 12, 25, 0)))
@pytest.mark.parametrize("c", ("1/5", "13/20"))
def test_full_unconditional_gibbs_output_not_just_word_accuracy(checks, c):
    record = audit.spectral_gibbs_control(CodeProblem(5, checks), c)
    assert len(record["all_sign_rows"]) == 32
    assert 0 < record["word_error_numeric"] < 0.5
    assert all(row["unconditional_TV_numeric"] < 1e-12 for row in record["all_sign_rows"])
    assert all(row["record_zero_probability_numeric"] == pytest.approx(1) for row in record["all_sign_rows"])
    assert all(row["source_label_zero_probability_numeric"] < 1-1e-5 for row in record["all_sign_rows"])
    assert all(not row["postselection_used"] for row in record["all_sign_rows"])
    assert not record["scalable_gate_count_or_speedup_established"]
    assert record["spectral_repair_recipe"]["raw_compressed_commutator_norm_max_numeric"] > 1e-5
    assert record["spectral_repair_recipe"]["repaired_reflection_commutator_norm_max_numeric"] < 1e-12


def multiply(A, B):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*B)] for row in A]


@pytest.mark.parametrize("c", ("0", "1/5"))
def test_uniform_comparison_budget_gives_exact_finite_worst_start_TV(c):
    problem = CodeProblem(3, (3, 6))
    certificate = audit.universal_gap_budget(problem, c, failure_bits=3)
    steps = certificate["steps_sufficient"]
    for representative in (0, 1):
        states, pi, kernel = audit.exact_sector_kernel(problem, c, representative)
        rho = (1-Fraction(c))/(1+Fraction(c))
        assert min(pi)/max(pi) >= rho**problem.length
        K = np.array(kernel, dtype=float)
        roots = np.sqrt(list(map(float, pi)))
        S = K*roots[:, None]/roots[None, :]
        gap = 1-np.linalg.eigvalsh(S)[-2]
        assert gap >= float(Fraction(certificate["gap_lower_exact"]))-1e-12
        power = [[Fraction(i == j) for j in range(len(states))] for i in range(len(states))]
        base, exponent = kernel, steps
        while exponent:
            if exponent & 1:
                power = multiply(power, base)
            exponent >>= 1
            if exponent:
                base = multiply(base, base)
        maximum_TV = max(sum(abs(p-q) for p, q in zip(row, pi))/2 for row in power)
        assert maximum_TV <= Fraction(1, 8)
    assert not certificate["large_sufficient_budget_proves_slow_mixing"]
    assert not certificate["numerical_eigenvalues_used_as_certificates"]


def test_actual_local_random_coin_counts_reproduce_the_exact_transition():
    problem, c = CodeProblem(3, (3, 6, 0)), Fraction(1, 5)
    states, _, kernel = audit.exact_sector_kernel(problem, c, 1)

    class Coins:
        def __init__(self, index, coin):
            self.values = [index, coin]

        def randrange(self, stop):
            value = self.values.pop(0)
            assert 0 <= value < stop
            return value

    for i, y in enumerate(states):
        observed = {z: Fraction(0) for z in states}
        for j, h in enumerate(problem.checks):
            w, ones = h.bit_count(), (y & h).bit_count()
            denominator = 6**(w-ones)*4**ones+6**ones*4**(w-ones)
            for coin in range(denominator):
                result, index, width = audit.quotient_step(problem, c, y, Coins(j, coin))
                assert index == j and width == w
                observed[result] += Fraction(1, len(problem.checks)*denominator)
        assert list(observed.values()) == kernel[i]


def test_native_walk_is_polynomial_work_not_a_stationary_sampler(monkeypatch):
    from theorems.affine_cluster_native_probe import socket_instance
    model, _ = socket_instance(64, random.Random(29))
    checks = tuple(sum(((mask >> i) & 1) << j for j, (mask, _) in enumerate(model.clauses))
                   for i in range(model.spins))
    signs = sum(sign << j for j, (_, sign) in enumerate(model.clauses))

    def forbidden(*args, **kwargs):
        raise AssertionError("production update tried to enumerate a state space")

    monkeypatch.setattr(audit, "row_orbit", forbidden)
    monkeypatch.setattr(audit, "parent_matrix", forbidden)
    monkeypatch.setattr(audit, "exact_sector_kernel", forbidden)
    record = audit.quotient_trajectory(CodeProblem(len(model.clauses), checks), "13/20", signs, seed=4831)
    assert record["native_lift_verified"] and not record["full_domain_materialized"]
    assert record["local_factor_bits_tested"] <= 6*256
    assert not record["output_is_certified_Gibbs_sample"] and record["TV_error_claim"] is None


def test_singleton_sector_does_not_claim_a_positive_parent_gap():
    result = audit.universal_gap_budget(CodeProblem(3, (0, 0)), "13/20")
    assert result["steps_sufficient"] == 0 and result["gap_lower_exact"] is None
    assert not result["parent_positive_gap_claimed"]


@pytest.mark.parametrize("problem", (
    CodeProblem(5, (25, 26, 12)), CodeProblem(4, (7, 14, 9)),
    CodeProblem(3, (0, 0)), CodeProblem(3, (1, 2, 4)),
))
@pytest.mark.parametrize("c", ("0", "1/5", "13/20"))
def test_actual_source_swap_and_LCU_Gram_blocks(problem, c):
    record = audit.gram_preparation_control(problem, c)
    assert record["physical_source_swap_unprepare_block_residual"] < 1e-12
    assert record["single_wire_LCU_top_block_residual"] < 1e-12
    assert record["product_channel_Gram_residual"] < 1e-12
    assert Fraction(record["exact_Gram_row_sum"]) <= Fraction(record["systematic_row_sum_bound"])
    c = Fraction(c)
    k = len(problem.structure[0])
    # The row-sum theorem is independently checked on EVERY codeword.
    weights = [problem.encode(u).bit_count() for u in range(1 << k)]
    assert all(w >= u.bit_count() for u, w in enumerate(weights))
    row_sum = sum(c**w for w in weights)
    assert row_sum <= (1+c)**k
    assert row_sum == Fraction(record["exact_Gram_row_sum"])
    certificate = record["Gram_access_certificate"]
    for encoding in certificate["encodings"].values():
        divisor = Fraction(encoding["Gram_divisor_exact"])
        actual_maximum = row_sum/divisor
        assert actual_maximum <= Fraction(encoding["encoded_Gram_norm_upper_exact"]) <= 1
        assert Fraction(encoding["inverse_adjoint_on_ANY_normalized_solution_lower_exact"]) <= 1/actual_maximum


@pytest.mark.parametrize("k", (1, 16, 64, 256, 1024))
def test_uniform_half_rate_source_aware_cost_bound_needs_no_Gram_table(k):
    certificate = audit.gram_access_certificate(2*k, k, "13/20")
    assert certificate["better_of_these_two_encodings"] == "source_purification_swap"
    assert Fraction(certificate["best_inverse_adjoint_quantity_lower_exact"]) == Fraction(40, 33)**k
    assert certificate["QLS_cost_expression_floor_is_NOT_a_general_query_or_circuit_lower_bound"]
    assert not certificate["all_span_reflection_constructions_excluded"]


@pytest.mark.parametrize("pairs", (1, 2, 3))
def test_direct_native_reflection_disproves_a_universal_Gram_hardness_inference(pairs):
    record = audit.pair_native_reflection_control(pairs, "13/20")
    assert record["native_reflection_vs_exact_span_residual"] < 1e-12
    assert record["local_two_wire_unitaries_forward_and_inverse"] == 2*pairs
    assert record["growing_pair_family_HAS_a_direct_polynomial_reflection_and_classical_sampler"]
    assert not record["parent_gap_or_generic_Gram_inversion_used"]
    probabilities = [Fraction(row["classical_spin_one_probability_exact"])
                     for row in record["all_pair_sign_classical_exact_sampler"]]
    assert probabilities == [Fraction(49, 1138), Fraction(1, 2), Fraction(1, 2), Fraction(1089, 1138)]
    c = Fraction(13, 20)
    problem = CodeProblem(2*pairs, tuple(3 << (2*i) for i in range(pairs)))
    row_sum = sum(c**problem.encode(u).bit_count() for u in range(1 << pairs))
    assert row_sum == (1+c*c)**pairs
    assert Fraction(2**pairs, row_sum) == Fraction(800, 569)**pairs


def test_trivial_endpoints_do_not_inherit_an_exponential_cost_claim():
    for length, dimension, c in ((128, 64, "0"), (128, 0, "13/20"), (128, 128, "13/20")):
        certificate = audit.gram_access_certificate(length, dimension, c)
        assert Fraction(certificate["best_inverse_adjoint_quantity_lower_exact"]) == 1


@pytest.mark.parametrize("call", (
    lambda: audit.overlap("1"), lambda: audit.overlap("-1/5"),
    lambda: audit.overlap(0.5), lambda: audit.local_projector(9, "1/5"),
    lambda: audit.local_deformed_code_control(7, "1/5"),
    lambda: audit.row_orbit(CodeProblem(9, (3,)), 0),
    lambda: audit.parent_matrix(CodeProblem(9, (3,)), "1/5"),
    lambda: audit.spectral_readout_reference(CodeProblem(7, (3, 6, 12)), "1/5"),
    lambda: audit.weight(8, 3, "1/5"),
    lambda: audit.quotient_trajectory(CodeProblem(3, (3,)), "1/5", 0, seed=True),
    lambda: audit.universal_gap_budget(CodeProblem(3, (3,)), "1/5", failure_bits=0),
    lambda: audit.gram_access_certificate(10, 11, "1/5"),
    lambda: audit.gram_preparation_control(CodeProblem(7, (3, 6, 12, 24)), "1/5"),
    lambda: audit.pair_native_reflection_control(4, "1/5"),
))
def test_model_and_allocation_gates(call):
    with pytest.raises(ValueError):
        call()


def test_live_report_binds_sources_and_does_not_promote_a_speedup():
    record = json.loads(audit.REPORT.read_text())
    assert record["producer_sha256"] == hashlib.sha256(Path(audit.__file__).read_bytes()).hexdigest()
    for name, digest in record["dependency_sha256"].items():
        assert digest == hashlib.sha256((audit.ROOT/"theorems"/name).read_bytes()).hexdigest()
    assert record["native_actual_classical_trajectory"]["length"] == 128
    assert record["native_actual_classical_trajectory"]["updates_charged"] == 256
    assert record["native_uniform_comparison_budget_NOT_executed"]["steps_sufficient"] > 10**50
    assert not record["general_quantum_BPQM_dequantized"]
    assert not record["polynomial_gap_proved"] and not record["speedup_claim_allowed"]
    assert record["schema_version"] == 2
    gram = record["native_Gram_access_bound_NO_Gram_table"]
    assert gram["code_dimension"] == 64
    assert Fraction(gram["best_inverse_adjoint_quantity_lower_exact"]) == Fraction(40, 33)**64
