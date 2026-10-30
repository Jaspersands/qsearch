from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path

import pytest

from theorems.balanced_codeword_filter import reciprocal_trace, ceil_log2_fraction
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_smt import verify_word
from theorems.inverse_trace_binary_rank import binary_subword_diagnostic, uniform_rank_failure_bound
from theorems.reciprocal_trace_flats import verify_native_independently
from theorems.inverse_trace_syndrome_counts import syndrome_count_error, partial_transcript_error

ROOT = Path(__file__).resolve().parents[1]


def test_rank_kernel_agrees_with_all_subsets_on_small_native_words():
    instance = {"bits": 3, "points": [0, 1, 2, 3], "checks": 1,
                "targets": [0, 0, 0, 0],
                "field_modulus_coefficients": list(map(int, field(3).modulus().coeffs()))}
    verified = 0
    for word in product(range(8), repeat=4):
        if not verify_word(instance, word):
            continue
        result = binary_subword_diagnostic(instance, word)
        kernel = []
        for mask in range(16):
            value = 0
            for i, x in enumerate(word):
                if (mask >> i) & 1:
                    value ^= x
            if value == 0:
                kernel.append(mask)
        span = [0]
        for encoded in result["kernel_basis_hex"]:
            vector = int(encoded, 16)
            span += [x ^ vector for x in span]
        assert sorted(span) == kernel
        assert len(kernel) == 2**result["binary_nullity"]
        assert result["additional_binary_dependence"] == (len(kernel) > 2)
        assert not result["subsets_enumerated"]
        assert not result["uniformity_certified"]
        verified += 1
    assert verified > 0


@pytest.mark.parametrize("name", ["inverse_trace_singleton_subinstance_n17",
                                 "inverse_trace_sparse_partition_n17"])
def test_saved_block_assemblies_have_detectable_additional_binary_relations(name):
    record = json.loads((ROOT/"research/classical_baselines"/(name+".json")).read_text())
    instance, word = record["original_instance"], record["witness"]
    result = binary_subword_diagnostic(instance, word)
    assert result["binary_rank"] <= len(word)-2
    assert result["additional_binary_dependence"]
    modulus = sum(c << j for j, c in enumerate(instance["field_modulus_coefficients"]))
    for encoded in result["kernel_basis_hex"]:
        masked = [x if (int(encoded, 16) >> i) & 1 else 0 for i, x in enumerate(word)]
        check = verify_native_independently(17, instance["points"], instance["checks"],
                                            instance["targets"], masked, modulus)
        assert not any(check["field_syndromes"])


def test_invalid_word_is_not_a_sampling_diagnostic():
    record = json.loads((ROOT/"research/classical_baselines/inverse_trace_sparse_partition_n17.json").read_text())
    with pytest.raises(ValueError, match="verified full original"):
        binary_subword_diagnostic(record["original_instance"], [0]*289)


def test_rank_saturation_is_already_attained_by_classical_countercontrols():
    norm = json.loads((ROOT/"research/classical_baselines/inverse_trace_genus_zero_n17.json").read_text())
    flat = json.loads((ROOT/"research/classical_baselines/inverse_trace_partition_matched_flats_n17.json").read_text())
    cases = [(norm["instance"], norm["witness"])]+[
        (case["original_instance"], case["run"]["witness"]) for case in flat["cases"]]
    for instance, word in cases:
        result = binary_subword_diagnostic(instance, word)
        assert result["binary_rank"] == 288 and result["binary_nullity"] == 1
        assert not result["additional_binary_dependence"]
        assert not result["uniformity_certified"] and not result["hardness_evidence"]
        reversed_instance = {**instance, "points": instance["points"][::-1],
                             "targets": instance["targets"][::-1]}
        assert binary_subword_diagnostic(reversed_instance, word[::-1])["binary_rank"] == 288


def test_two_check_code_exhaustion_uses_independent_field_columns():
    bits, points = 3, list(range(5))
    modulus = list(map(int, field(bits).modulus().coeffs()))
    for free in product(range(8), repeat=3):
        x1 = sum((element(bits, a)*element(bits, x) for a, x in zip(points[2:], free)), field(bits).zero())
        x0 = x1+sum((element(bits, x) for x in free), field(bits).zero())
        word = [encoded(x0), encoded(x1), *free]
        instance = {"bits": bits, "points": points, "checks": 2,
                    "targets": [reciprocal_trace(bits, x) for x in word],
                    "field_modulus_coefficients": modulus}
        result = binary_subword_diagnostic(instance, word)
        columns = [x | (encoded(element(bits, a)*element(bits, x)) << bits) for a, x in zip(points, word)]
        kernel = set()
        for mask in range(32):
            value = 0
            for i, column in enumerate(columns):
                if (mask >> i) & 1:
                    value ^= column
            if value == 0:
                kernel.add(mask)
        span = {0}
        for certificate in result["kernel_basis_hex"]:
            span |= {mask ^ int(certificate, 16) for mask in span}
        assert span == kernel


@pytest.mark.parametrize("bits", [17, 61])
def test_uniform_reference_bounds_pay_zero_coordinates_separately(bits):
    N, K = bits*bits, bits*bits//8
    positive = uniform_rank_failure_bound(bits, N, K, 0)
    assert positive["status"] == "CERTIFIED_UNIFORM_NATIVE_RANK_FAILURE_BOUND"
    assert Fraction(*positive["zero_coordinate_probability_upper"]) == 0
    assert positive["rank_failure_probability_power2_upper"] <= N-(bits-1)*K
    general = uniform_rank_failure_bound(bits, N, K, N)
    assert Fraction(*general["rank_failure_probability_upper"]) < Fraction(3*N, 1 << bits)
    assert general["uniform_native_law_required"]
    assert general["observed_rank_is_not_uniformity_certificate"]


def test_live_sampling_controls_replay_without_a_quantum_or_uniformity_claim():
    artifact = json.loads((ROOT/"research/classical_baselines/inverse_trace_sampling_controls.json").read_text())
    for path, digest in artifact["source_sha256"].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest
    for row in artifact["existing_witness_diagnostics"]:
        data = (ROOT/row["artifact"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == row["artifact_sha256"]
        source = json.loads(data)
        if row["case_index"] is None:
            instance, word = source.get("original_instance", source.get("instance")), source["witness"]
        else:
            case = source["cases"][row["case_index"]]
            instance, word = case["original_instance"], case["run"]["witness"]
        assert row["diagnostic"] == binary_subword_diagnostic(instance, word)
    for row in artifact["uniform_reference_bounds"]:
        result = uniform_rank_failure_bound(row["bits"], row["length"], row["checks"], row["zero_targets"])
        for key in ("rank_failure_probability_power2_upper", "nonzero_decomposition_probability_power2_upper"):
            assert row[key] == result[key]
    for row in artifact["partial_observation_bounds"]:
        assert row["every_syndrome_count_error_power2_upper"] == ceil_log2_fraction(
            syndrome_count_error(row["bits"], row["unobserved"], row["checks"]))
        assert row["adaptive_transcript_TV_power2_upper"] == ceil_log2_fraction(
            partial_transcript_error(row["bits"], row["length"], row["checks"], row["observed_coordinate_cap"]))
    assert artifact["some_classical_witnesses_pass_rank_test"]
    for key in ("native_uniform_sampler_implemented", "native_sampler_runtime_claim",
                "quantum_speedup_claim", "all_classical_samplers_excluded"):
        assert artifact[key] is False
