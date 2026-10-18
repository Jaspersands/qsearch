"""Native state semantics, public decoding and paid postselection falsifiers."""
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb, sqrt
from pathlib import Path

import numpy as np
import pytest

from theorems.conjugate_chirp_repair import (
    REPORT, QuadraticInput, decode_weight_one, diagonal_score_washout_bound, diagonal_tail_bound, native_control,
    postselection_bound, reciprocal_character_control,
)


def problem(kind="diagonal", *, p=5, n=2, points=(1, 2, 3), shifts=(1, 4, 1)):
    squares = {x*x % p for x in range(p)}
    return QuadraticInput(p, n, points, tuple(tuple(sorted((x+t) % p for x in squares)) for t in shifts), kind)


@pytest.fixture(scope="module", params=["diagonal", "rank_one"])
def control(request):
    instance = problem(request.param)
    return instance, native_control(instance)


def test_actual_pair_decoder_erases_labels_but_not_into_the_original_target(control):
    instance, (record, pair, target, good) = control
    assert record["native_pair_to_bilinear_QFT_max_error"] < 1e-13
    assert record["bilinear_filter_amplitude_max_error"] < 1e-13
    assert record["good_branch_residual_error_label_mass"] < 1e-25
    assert record["would_leak_error_label_mass_without_good_projection"] > 0
    assert np.linalg.norm(pair)**2 == pytest.approx(1, abs=1e-13)
    assert np.linalg.norm(target)**2 == pytest.approx(1, abs=1e-13)
    density = pair@pair.conj().T
    assert record["original_x_marginal_purity"] == pytest.approx(np.trace(density@density).real)
    assert record["original_quadratic_target_fidelity"] == pytest.approx(np.vdot(target, density@target).real)
    scores = np.array([sum(value in target_set for value, target_set in zip(instance.quadratic_values(x), instance.target_lists))
                       for x in product(range(instance.prime), repeat=instance.dimension)])
    assert record["paired_x_original_satisfied_count_mean"] == pytest.approx(np.diag(density).real@scores)
    assert record["uniform_original_satisfied_count_mean"] == pytest.approx(np.mean(scores))
    assert record["ideal_original_quadratic_filter_satisfied_count_mean"] == pytest.approx(np.abs(target)**2@scores)
    assert record["original_x_marginal_purity"] < .9
    assert record["original_quadratic_target_fidelity"] < .9
    assert record["original_x_probability_TV_to_intended_target"] > .05
    assert record["good_direction_probability_exact"] == str(Fraction(sum(good), len(good)))
    assert record["conjugate_chirp_prepared_from_public_error_label_not_unknown_state_conjugation"]
    assert not record["general_quadratic_DQI_preparation_repaired"]
    assert not record["reversible_decoder_and_predicate_state_preparation_compiled"]


@pytest.mark.parametrize("kind", ["diagonal", "rank_one"])
def test_public_decoder_recovers_every_promised_symbol_at_large_prime_without_field_search(kind):
    instance = problem(kind, p=61, n=4, points=(1, 2, 3, 4, 5, 6), shifts=(1,)*6)
    r, p = (1, 1, 1, 1), instance.prime
    assert instance.good_direction(r)
    assert decode_weight_one(instance, r, (0, 0, 0, 0)) == 0
    beta = instance.values(r)
    for i, a in enumerate(instance.points):
        for y in range(1, p):
            syndrome = tuple(y*pow(a, j, p)*(r[j] if kind == "diagonal" else beta[i]) % p for j in range(4))
            assert decode_weight_one(instance, r, syndrome) == 1+i*(p-1)+y-1
    assert decode_weight_one(instance, r, (0, 1, 0, 0)) is None
    assert decode_weight_one(instance, (0, 0, 0, 0), (0, 0, 0, 0)) is None


def test_decoder_subtraction_extends_to_a_permutation_on_the_whole_error_register(control):
    instance, _ = control
    D, p = 1+len(instance.points)*(instance.prime-1), instance.prime
    for r in product(range(p), repeat=instance.dimension):
        for syndrome in product(range(p), repeat=instance.dimension):
            decoded = decode_weight_one(instance, r, syndrome) or 0
            images = [(e-decoded) % D for e in range(D)]
            assert sorted(images) == list(range(D))
            assert all((x+decoded) % D == e for e, x in enumerate(images))


@pytest.mark.parametrize("kind", ["diagonal", "rank_one"])
def test_independent_literal_pair_phases_and_DFT_produce_the_claimed_syndrome(kind):
    instance = problem(kind)
    p, n, r, y, i = 5, 2, (1, 1), 3, 1
    vectors = tuple(product(range(p), repeat=n))
    amplitudes = []
    for u in vectors:
        x = tuple((a+b)*pow(2, -1, p) % p for a, b in zip(u, r))
        z = tuple((a-b)*pow(2, -1, p) % p for a, b in zip(u, r))
        phase = y*(instance.quadratic_values(x)[i]-instance.quadratic_values(z)[i]) % p
        amplitudes.append(np.exp(2j*np.pi*phase/p)/sqrt(p**n))
    # Literal sum over all u, independent of numpy.fft's axis/normalization conventions.
    transformed = np.array([sum(a*np.exp(-2j*np.pi*sum(k*j for k, j in zip(s, u))/p)
                                for a, u in zip(amplitudes, vectors))/sqrt(p**n) for s in vectors])
    peak = vectors[int(np.argmax(np.abs(transformed)))]
    assert abs(transformed[vectors.index(peak)]-1) < 1e-13
    assert decode_weight_one(instance, r, peak) == 1+i*(p-1)+y-1


def test_diagonal_output_is_pure_ordinary_linear_DQI_after_a_reversible_change_of_variables():
    instance = problem()
    record, pair, _, _ = native_control(instance)
    p, n = instance.prime, instance.dimension
    vectors = tuple(product(range(p), repeat=n))
    remapped = np.zeros_like(pair)
    for x_index, x in enumerate(vectors):
        for z_index, z in enumerate(vectors):
            r = tuple((a-b) % p for a, b in zip(x, z))
            coefficients = tuple((a*a-b*b) % p for a, b in zip(x, z))
            # Only good-r amplitudes survive; on those, (x,z)<->(r,q) is bijective.
            if instance.good_direction(r):
                remapped[vectors.index(r), vectors.index(coefficients)] = pair[x_index, z_index]
    density = remapped.T@remapped.conj()
    reduction = record["native_unrestricted_linear_DQI_reduction"]
    assert reduction["native_factorization_amplitude_error"] < 1e-13
    assert np.trace(density@density).real == pytest.approx(1, abs=1e-13)
    assert reduction["ordinary_linear_DQI_output_purity"] == pytest.approx(1, abs=1e-13)
    squares = {a*a % p for a in range(p)}
    invalid = [any(a not in squares for a in word) for word in vectors]
    invalid_mass = np.diag(density).real[invalid].sum()
    assert invalid_mass == pytest.approx(reduction["output_probability_of_nonsquare_original_coefficients"])
    # Using q as original squared coefficients fails. Reporting x is feasible
    # but has the different state and measured objective reported separately.
    assert invalid_mass > .1
    assert reduction["nonsquare_probability_refers_to_q_not_feasibility_of_reporting_x"]


def test_rank_one_original_constraints_already_absorb_into_linear_predicates(control):
    instance, (record, _, _, _) = control
    if instance.form_kind != "rank_one":
        assert record["composed_linear_OPI_target_lists"] is None
        return
    lists = record["composed_linear_OPI_target_lists"]
    for x in product(range(instance.prime), repeat=instance.dimension):
        for i, (value, original_quadratic) in enumerate(zip(instance.values(x), instance.quadratic_values(x))):
            assert (value in lists[i]) == (original_quadratic in instance.target_lists[i])


def test_postselecting_the_second_register_is_charged_and_only_gives_a_restricted_target(control):
    _, (record, pair, target, good) = control
    probability = np.abs(pair[:, 0])**2
    assert sum(probability) == pytest.approx(record["z_zero_postselection_probability"])
    assert 0 < sum(probability) <= float(Fraction(record["postselection_bound"]["z_zero_probability_upper"]))
    conditioned = probability/sum(probability)
    restricted = np.abs(target)**2*good
    restricted /= sum(restricted)
    assert conditioned == pytest.approx(restricted, abs=2e-14)


def test_general_shell_postselection_height_bound_is_exact_and_exponentially_small_at_fixed_rate():
    for p, n in ((101, 16), (257, 32), (65537, 64)):
        rho, m, degree = Fraction((p-1)//2, p), 2*n, n//2
        record = postselection_bound(p, n, (rho,)*m, degree)
        A2 = (1-rho)/rho
        expected = sum(Fraction(comb(m, k))*A2**k for k in range(degree+1))
        assert Fraction(record["squared_filter_height_bound"]) == expected
        assert Fraction(record["z_zero_probability_upper"]) == expected/p**n
        assert Fraction(record["z_zero_probability_upper"]) < Fraction(1, 1 << 60)
        assert not record["all_state_preparation_algorithms_lower_bounded"]
    with pytest.raises(ValueError, match="realizable"):
        postselection_bound(7, 2, (Fraction(1, 2),)*3, 1)


def test_exponential_control_cap_and_invalid_fields_are_not_hardness_evidence():
    large = problem(p=101, n=3, points=(1, 2, 3), shifts=(1, 1, 1))
    with pytest.raises(ValueError, match="UNKNOWN: exponential"):
        native_control(large)
    with pytest.raises(ValueError):
        problem(p=9)
    with pytest.raises(ValueError):
        QuadraticInput(5, 2, (1, 1), ((0,), (0,)))
    with pytest.raises(ValueError):
        QuadraticInput(5, 2, (0, 1), ((0,), (0,)))
    with pytest.raises(ValueError, match="normalized"):
        native_control(problem(), (Fraction(1), Fraction(1)))
    with pytest.raises(ValueError, match="canonical"):
        decode_weight_one(problem(), (5, 1), (0, 0))
    with pytest.raises(ValueError, match="canonical"):
        decode_weight_one(problem(), (1, 1), (5, 0))
    with pytest.raises(ValueError, match="UNKNOWN: exact bound serialization"):
        diagonal_score_washout_bound(101, 4096, (Fraction(50, 101),))


@pytest.mark.parametrize("p", [5, 7, 13, 29])
def test_every_small_reciprocal_character_matches_Kloosterman_Salie_and_Gauss(p):
    for c in range(p):
        for b in range(1, p):
            row = reciprocal_character_control(p, c, b)
            assert row["decomposition_error"] < 1e-12
            assert row["Salie_Gauss_identity_error"] < 1e-12
            assert row["Kloosterman_modulus"] <= 2*sqrt(p)+1e-12
            assert row["Salie_modulus"] <= 2*sqrt(p)+1e-12
            assert row["direct_character_modulus"] <= row["standard_uniform_character_upper"]+1e-12


def test_uniform_in_q_mean_bound_against_exact_integer_convolutions_beyond_statevector_sizes():
    p, n, alpha = 101, 16, 3
    rho, target = Fraction(50, p), set(range(50))
    certificate = diagonal_score_washout_bound(p, n, (rho,))

    def extend(previous, single):
        out = [0]*p
        for a, x in enumerate(previous):
            for b, y in enumerate(single):
                out[(a+b) % p] += x*y
        return out

    for q in ((0,)*n, (1,)*n, tuple((j*j+3) % p for j in range(n))):
        counts = [1]+[0]*(p-1)
        for j, c in enumerate(q):
            single = [0]*p
            for r in range(1, p):
                x = (r+c*pow(r, -1, p))*pow(2, -1, p) % p
                single[pow(alpha, j, p)*x*x % p] += 1
            counts = extend(counts, single)
        assert sum(counts) == (p-1)**n
        actual = Fraction(sum(counts[x] for x in target), (p-1)**n)
        assert abs(actual-rho) <= Fraction(certificate["paired_expected_satisfied_fraction_bias_upper"])
    uniform = [1]+[0]*(p-1)
    for j in range(n):
        single = [0]*p
        for x in range(p):
            single[pow(alpha, j, p)*x*x % p] += 1
        uniform = extend(uniform, single)
    actual_uniform = Fraction(sum(uniform[x] for x in target), p**n)
    assert abs(actual_uniform-rho) <= Fraction(certificate["uniform_classical_x_expected_fraction_bias_upper"])
    assert Fraction(certificate["paired_minus_uniform_classical_expected_fraction_advantage_upper"]) < Fraction(1, 10000)
    assert not certificate["score_tails_or_full_output_TV_bounded"]
    assert certificate["external_Weil_Kloosterman_bound_assumed_not_formally_verified_here"]


def test_symbolic_mean_bound_covers_any_input_q_but_not_unrelated_quantum_algorithms():
    for p, n in ((101, 16), (257, 32), (65537, 64)):
        rho = Fraction((p-1)//2, p)
        record = diagonal_score_washout_bound(p, n, (rho,)*(2*n))
        assert record["paired_bound_uniform_over_arbitrary_input_q_distribution"]
        assert record["local_derivation_review_pending"]
        assert Fraction(record["paired_minus_uniform_classical_expected_fraction_advantage_upper"]) < Fraction(1, 10000)
    with pytest.raises(ValueError, match="realizable"):
        diagonal_score_washout_bound(7, 2, (Fraction(1, 2),))


def test_Vandermonde_block_argument_excludes_long_zero_runs_for_every_small_frequency():
    p, n, points = 5, 4, (1, 2)
    for t in product(range(p), repeat=2):
        if not any(t):
            continue
        sequence = [sum(a*pow(x, j, p) for a, x in zip(t, points)) % p for j in range(n)]
        for start in range(n-1):
            assert any(sequence[start:start+2])
        assert sum(x != 0 for x in sequence) >= n//2


def test_tail_independent_centered_moment_bound_and_polynomial_coefficients_are_valid():
    from math import prod as multiply
    densities = (Fraction(1, 3), Fraction(2, 5), Fraction(3, 4), Fraction(1, 2))
    mean, m = sum(densities), len(densities)
    for s in (1, 2, 3):
        actual = Fraction(0)
        for bits in product((0, 1), repeat=m):
            probability = multiply(rho if bit else 1-rho for bit, rho in zip(bits, densities))
            actual += probability*(sum(bits)-mean)**(2*s)
        assert actual <= multiply(range(1, 2*s, 2))*m**s
    for rho in densities:
        for multiplicity in range(1, 9):
            a, b = (1-rho)**multiplicity-(-rho)**multiplicity, (-rho)**multiplicity
            assert abs(a)+abs(b) <= 2
            for bit in (0, 1):
                assert a*bit+b == (bit-rho)**multiplicity


def test_separate_tail_certificate_is_nontrivial_and_does_not_relabel_mean_bounds_as_tails():
    record = diagonal_tail_bound(65537, 1024, 2048, Fraction(1, 5), 8)
    assert record["even_centered_moment_order"] == 16
    assert record["minimum_nonzero_Fourier_coordinates_for_k_constraints"] == 64
    total = Fraction(record["independent_tail_contribution_upper"])+Fraction(record["joint_dependence_tail_contribution_upper"])
    assert Fraction(record["tail_probability_upper"]) == total
    assert total < Fraction(1, 10**6)
    assert record["any_input_q_distribution_covered_for_THIS_readout"]
    assert record["external_Weil_bound_and_local_derivation_review_pending"]
    assert not record["full_output_TV_or_other_quantum_algorithms_bounded"]
    trivial = diagonal_tail_bound(5, 2, 3, Fraction(1, 5), 1)
    assert Fraction(trivial["tail_probability_upper"]) == 1
    with pytest.raises(ValueError):
        diagonal_tail_bound(5, 2, 8, Fraction(1, 5), 1)


def test_joint_constraint_character_factorization_against_the_complete_classical_channel():
    p, n, points, q = 5, 4, (1, 2), (1, 2, 3, 4)
    histogram = {key: 0 for key in product(range(p), repeat=2)}
    for r in product(range(1, p), repeat=n):
        x = tuple((a+c*pow(a, -1, p))*pow(2, -1, p) % p for a, c in zip(r, q))
        values = tuple(sum(pow(alpha, j, p)*z*z for j, z in enumerate(x)) % p for alpha in points)
        histogram[values] += 1
    for t in product(range(p), repeat=2):
        direct = sum(count*np.exp(2j*np.pi*sum(a*b for a, b in zip(t, key))/p)
                     for key, count in histogram.items())/(p-1)**n
        factored = 1+0j
        for j, c in enumerate(q):
            frequency = sum(a*pow(alpha, j, p) for a, alpha in zip(t, points)) % p
            factor = sum(np.exp(2j*np.pi*frequency*pow((r+c*pow(r, -1, p))*pow(2, -1, p) % p, 2, p)/p)
                         for r in range(1, p))/(p-1)
            factored *= factor
        assert abs(direct-factored) < 1e-12


def test_saved_artifact_has_native_inputs_provenance_and_no_discovery_claim():
    saved = json.loads(REPORT.read_text())
    assert saved["source_sha256"] == hashlib.sha256(Path("theorems/conjugate_chirp_repair.py").read_bytes()).hexdigest()
    for name, digest in saved["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    assert not saved["accepted_speedup_candidate"]
    assert not saved["new_quantum_algorithm_claimed"]
    assert len(saved["native_controls"]) == 6
    for row in saved["native_controls"]:
        spec = row["specification"]
        instance = QuadraticInput(spec["prime"], spec["dimension"], tuple(spec["points"]),
                                  tuple(tuple(x) for x in spec["explicit_target_lists"]), spec["form_kind"])
        replay = native_control(instance)[0]
        assert replay["good_direction_probability_exact"] == row["good_direction_probability_exact"]
        assert replay["postselection_bound"] == row["postselection_bound"]
        assert replay["original_x_marginal_purity"] == pytest.approx(row["original_x_marginal_purity"], abs=2e-12)
        assert replay["original_quadratic_target_fidelity"] == pytest.approx(row["original_quadratic_target_fidelity"], abs=2e-12)
