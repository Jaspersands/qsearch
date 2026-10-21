"""Independent folded interpolation, native syndromes and paid pruning checks."""

from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

import pytest

import theorems.folded_rs_decoder as module
from theorems.folded_rs_decoder import (REPORT, affine_solution, decode,
                                        decode_syndrome, interpolation_space,
                                        parameters, prune, run_controls)


def horner(p, coefficients, x):
    result = 0
    for a in reversed(coefficients):
        result = (result*x + a) % p
    return result


def test_exact_affine_solution_spans_all_solutions_not_just_a_single_offset():
    p, rows, rhs = 5, [[1, 2, 0], [0, 1, 1]], [3, 4]
    space = affine_solution(p, rows, rhs, 3)
    expected = {v for v in product(range(p), repeat=3)
                if all(sum(a*b for a, b in zip(row, v)) % p == value for row, value in zip(rows, rhs))}
    actual = {tuple((a + sum(c*direction[i] for c, direction in zip(coeffs, space["basis"]))) % p
                    for i, a in enumerate(space["offset"]))
              for coeffs in product(range(p), repeat=len(space["basis"]))}
    assert actual == expected and len(actual) == 5
    assert affine_solution(p, [[0]], [1], 1) is None
    assert affine_solution(p, [], [], 2)["basis"] == [[1, 0], [0, 1]]


def test_strict_root_count_and_generator_order_are_required():
    with pytest.raises(ValueError, match="strict interpolation"):
        parameters(1019, 10, 15, 60, 2, 5, 3)
    with pytest.raises(ValueError, match="distinct"):
        parameters(1019, 10, 15, 60, 1, 4, 3)
    with pytest.raises(ValueError, match="prime"):
        parameters(1023, 10, 15, 60, 2, 4, 3)
    with pytest.raises(ValueError, match="canonical"):
        interpolation_space(1019, 10, 15, 60, 2, [0]*149 + [1019], 4, 3)
    with pytest.raises(ValueError, match="strict interpolation"):
        parameters((1 << 61) - 1, 127, 1, 88, 3, 32, 1)


def test_every_interpolant_and_affine_direction_replays_the_full_polynomial_identity():
    report = json.loads(REPORT.read_text())
    for row in report["controls"] + [report["ambiguous_whole_block_countercontrol"]]:
        p, n, m, k = int(row["p_decimal"]), row["n_blocks"], row["m_fold"], row["decoded_dimension_k"]
        D, s, gamma = row["D"], row["interpolation_order_s"], row["gamma"]
        pieces = row["interpolant_coefficients_A0_through_As"]
        assert any(a for poly in pieces for a in poly)
        assert (n - row["t_block_errors"])*(m - s + 1) > D + k - 1
        for block in range(n):
            for j in range(m - s + 1):
                index = block*m + j
                x = row["points"][index]
                result = horner(p, pieces[0], x)
                result += sum(horner(p, pieces[r + 1], x)*row["public_received_word"][index + r] for r in range(s))
                assert result % p == 0
        space = row["affine_space"]
        assert len(space["basis"]) <= s - 1
        for coefficients, inhomogeneous in [(space["offset"], True)] + [(v, False) for v in space["basis"]]:
            identity = list(pieces[0]) if inhomogeneous else [0]*(D + k)
            for shift, poly in enumerate(pieces[1:]):
                for j, a in enumerate(poly):
                    for i, b in enumerate(coefficients):
                        identity[j + i] = (identity[j + i] + a*b*pow(gamma, shift*i, p)) % p
            assert not any(identity)


def test_native_beyond_unique_controls_do_not_receive_error_support():
    report = json.loads(REPORT.read_text())
    for row in report["controls"]:
        p, m = int(row["p_decimal"]), row["m_fold"]
        assert row["beyond_guaranteed_unique_radius"] and row["target_recovered"]
        assert not row["hidden_error_support_given_to_decoder"]
        coefficients = row["calibration_true_message"]
        predicted = [horner(p, coefficients, x) for x in row["points"]]
        bad = [i for i in range(row["n_blocks"])
               if predicted[i*m:(i + 1)*m] != row["public_received_word"][i*m:(i + 1)*m]]
        assert bad == row["calibration_hidden_error_support"]
        assert len(bad) == row["t_block_errors"] > row["MDS_guaranteed_unique_block_radius"]
        assert any(c["polynomial_coefficients"] == coefficients for c in row["candidates"])
        assert not row["coefficient_field_enumeration_used"]
    assert report["controls"][1]["p_decimal"] == str((1 << 61) - 1)
    assert len(report["controls"][1]["public_received_word"]) == 775  # NOT p/full field.


def test_ambiguous_codewords_give_a_real_same_syndrome_collision_at_different_weights():
    row = json.loads(REPORT.read_text())["ambiguous_whole_block_countercontrol"]
    p, points, m = int(row["p_decimal"]), row["points"], row["m_fold"]
    zero, other = row["calibration_two_close_messages"]
    assert zero != other and row["affine_dimension"] == 1
    assert row["both_declared_close_words_recovered"]
    assert len(row["candidates"]) == 2
    assert sorted(len(c["disagreeing_blocks"]) for c in row["candidates"]) == [3, 4]
    # Convert ordinary RS to the ACTUAL kernel of bare scalar Vandermonde H.
    multipliers = []
    for i, x in enumerate(points):
        product_value = 1
        for j, y in enumerate(points):
            if i != j:
                product_value = product_value*(x - y) % p
        multipliers.append(pow(product_value, -1, p))
    errors = [[multipliers[i]*(row["public_received_word"][i] - horner(p, coefficients, x)) % p
               for i, x in enumerate(points)] for coefficients in (zero, other)]
    K = len(points) - row["decoded_dimension_k"]
    syndromes = [[sum(pow(x, j, p)*e for x, e in zip(points, error)) % p for j in range(K)] for error in errors]
    assert syndromes[0] == syndromes[1]
    assert sorted(sum(any(error[i*m:(i + 1)*m]) for i in range(row["n_blocks"])) for error in errors) == [3, 4]
    assert not row["list_completeness_certified"]  # The generic sampler does not prove this.


def test_pruning_all_block_draws_matches_the_rational_success_floor(monkeypatch):
    row = json.loads(REPORT.read_text())["ambiguous_whole_block_countercontrol"]

    class AllBlocks:
        def __init__(self, seed):
            self.next = 0

        def randrange(self, n):
            result = self.next
            self.next += 1
            assert result < n
            return result

    monkeypatch.setattr(module.random, "Random", AllBlocks)
    result = prune(1019, row["points"], 15, row["affine_space"], row["public_received_word"], 4, trials=10)
    statuses = Counter(t["status"] for t in result["transcript"])
    assert statuses == {"VERIFIED_CLOSE_WORD": 7, "RANK_NOT_RESOLVED": 3}
    counts = Counter(t.get("disagreeing_blocks_count") for t in result["transcript"])
    assert counts[4] == 3 and counts[3] == 4
    assert Fraction(result["per_candidate_per_trial_success_lower_exact"]) == Fraction(3, 10)
    assert Fraction(result["per_candidate_miss_upper_exact"]) == Fraction(7, 10) ** 10
    assert result["uniform_block_draws_charged"] == 10
    assert result["candidate_distance_checks_charged"] == 7


def test_rank_failure_is_retained_as_inconclusive_not_a_hardness_or_completeness_claim(monkeypatch):
    row = json.loads(REPORT.read_text())["ambiguous_whole_block_countercontrol"]

    class WrongBlock:
        def __init__(self, seed):
            pass

        def randrange(self, n):
            return n - 1

    monkeypatch.setattr(module.random, "Random", WrongBlock)
    result = prune(1019, row["points"], 15, row["affine_space"], row["public_received_word"], 4, trials=1)
    assert not result["candidates"]
    assert result["status"] == "PRUNING_BUDGET_INCONCLUSIVE_NOT_HARDNESS"
    assert result["transcript"] == [{"blocks_sampled": [9], "status": "RANK_NOT_RESOLVED"}]
    assert not result["list_completeness_certified"]


def test_dependent_affine_directions_cannot_receive_a_false_pruning_bound():
    row = json.loads(REPORT.read_text())["ambiguous_whole_block_countercontrol"]
    invalid = row["affine_space"] | {"basis": row["affine_space"]["basis"] * 2}
    with pytest.raises(ValueError, match="independent affine"):
        prune(1019, row["points"], 15, invalid, row["public_received_word"], 4)


def test_native_syndrome_conversion_computes_and_replays_multipliers_and_original_equations():
    report = json.loads(REPORT.read_text())
    for row in report["native_syndrome_controls"]:
        p, points, K, m = int(row["p_decimal"]), row["points"], row["ORIGINAL_scalar_syndrome_rank_K"], row["m_fold"]
        y, multipliers = row["computed_public_particular_word"], row["computed_GRS_multipliers"]
        assert row["source_error_recovered"] and not row["hidden_error_or_support_input"]
        assert row["GRS_conversion_field_inverse_calls_charged"] == 2*len(points)
        assert row["GRS_multiplier_product_factors_charged"] == len(points)*(len(points) - 1)
        assert row["original_syndrome_scalar_terms_checked"] == K*len(points)*len(row["verified_error_candidates"])
        assert not row["unique_source_erasure_or_complete_list_certified"]
        assert [sum(pow(x, j, p)*a for x, a in zip(points, y)) % p for j in range(K)] == row["syndrome"]
        for i, x in enumerate(points):
            denominator = 1
            for j, other in enumerate(points):
                if i != j:
                    denominator = denominator*(x - other) % p
            assert denominator*multipliers[i] % p == 1
        for candidate in row["verified_error_candidates"]:
            e = candidate["error_word"]
            assert [sum(pow(x, j, p)*a for x, a in zip(points, e)) % p for j in range(K)] == row["syndrome"]
            assert sum(any(e[i*m:(i + 1)*m]) for i in range(row["n_blocks"])) <= row["ordinary_decoder"]["t_block_errors"]
            c = [v*horner(p, candidate["ordinary_RS_polynomial"], x) % p for v, x in zip(multipliers, points)]
            assert [(a - b) % p for a, b in zip(y, c)] == e


def test_syndrome_decoder_rejects_wrong_rank_instead_of_importing_a_free_decoder():
    with pytest.raises(ValueError, match="ORIGINAL rank-K"):
        decode_syndrome(1019, 10, 15, 90, 2, [0]*89, 4, 3)


def test_live_artifact_replays_and_never_claims_the_missing_source_or_quantum_algorithm():
    report = json.loads(REPORT.read_text())
    assert report == run_controls()
    assert report["source_sha256"] == hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((module.ROOT / "theorems" / name).read_bytes()).hexdigest()
    assert report["known_algorithm_not_a_new_quantum_candidate"]
    assert not report["norm_character_source_or_quantum_receiver_implemented"]
