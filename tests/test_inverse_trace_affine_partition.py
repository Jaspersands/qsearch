from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from random import Random

from flint import fq_default_poly_ctx
import pytest

from theorems import inverse_trace_affine_partition as partition
from theorems.explicit_quadratic_opi import element, field
from theorems.inverse_trace_smt import verify_word
from theorems.inverse_trace_genus_zero import word_from_norm
from theorems.reciprocal_trace_flats import verify_native_independently

ROOT = Path(__file__).resolve().parents[1]


def small_instance(points, targets, checks=1):
    return {"bits": 3, "points": points, "targets": targets, "checks": checks,
            "field_modulus_coefficients": list(map(int, field(3).modulus().coeffs()))}


def test_partition_retains_every_original_constraint_and_order():
    instance = small_instance([6, 1, 4, 0, 3, 2], [1, 0, 0, 1, 0, 1])
    before = deepcopy(instance)
    blocks = partition.trace_partition(instance, 3, 5)
    assert instance == before
    assert sorted(i for b in blocks for i in b["indices"]) == list(range(6))
    assert set(blocks[0]["indices"]).isdisjoint(blocks[1]["indices"])
    for block in blocks:
        assert block["indices"] == sorted(block["indices"])
        for i in block["indices"]:
            assert int((element(3, block["c"])*element(3, instance["points"][i])
                        +element(3, block["d0"])).trace()) == instance["targets"][i]


def test_affine_labels_are_pairwise_independent_before_nonzero_slope_rejection():
    for a in range(8):
        for b in range(a+1, 8):
            counts = {(x, y): 0 for x in range(2) for y in range(2)}
            for c in range(8):
                for offset in range(2):
                    labels = tuple(int((element(3, c)*element(3, p)).trace()) ^ offset for p in (a, b))
                    counts[labels] += 1
            assert set(counts.values()) == {4}


def test_zero_extension_cannot_discard_one_target():
    instance = small_instance(list(range(6)), [1]*6)
    with pytest.raises(ValueError, match="omit an original one-target"):
        partition.run_zero_extended_experiment(instance, 1, 0)


def test_rank_failure_is_only_a_rejected_partition_not_native_unsat():
    instance = small_instance([0, 1], [1, 0])
    c = next(c for c in range(1, 8) if element(3, c).trace() == 0)
    result = partition.run_zero_extended_experiment(instance, c, 1)
    assert result["block_run"]["status"] == "PARTITION_BLOCK_HAS_FULL_COLUMN_RANK"
    assert result["status"] == "UNKNOWN_PARTITION_TRIAL_LIMIT"
    assert result["witness"] is None and not result["hardness_evidence"]


def test_zero_target_blocks_need_no_norm_trials():
    instance = small_instance([0, 1, 2], [0, 0, 0])
    result = partition.run_partitioned_experiment(instance, 1)
    assert result["witness"] == [0, 0, 0]
    assert all(b["run"]["status"] == "VERIFIED_ZERO_BLOCK" for b in result["blocks"])
    assert not result["generic_partition_success_bound_established"]


def test_singleton_replay_uses_original_checks_and_paid_failed_trial(monkeypatch):
    record = json.loads((ROOT/"research/classical_baselines/inverse_trace_singleton_subinstance_n17.json").read_text())
    instance = record["original_instance"]
    before = deepcopy(instance)
    calls = []

    def replay(block, c, d0, **kwargs):
        assert block == record["block_run"]["instance"]
        assert block["checks"] == instance["checks"] == 36
        assert (c, d0, kwargs["seed"], kwargs["allocation_seed"]) == (1, 1, 1032, 1033)
        calls.append(block)
        return deepcopy(record["block_run"])

    monkeypatch.setattr(partition, "run_experiment", replay)
    result = partition.run_zero_extended_experiment(instance, 1, 1)
    assert instance == before and len(calls) == 1
    assert result["selected_indices"] == [0]+list(range(1, 289, 2))
    assert result["witness"] == record["witness"]
    assert verify_word(instance, result["witness"])
    assert len(result["block_run"]["trials"]) == 2
    assert result["block_run"]["success_certificate"]["status"] == "BOUND_INCONCLUSIVE"


def test_two_block_replay_is_not_a_single_trace_affine_input(monkeypatch):
    record = json.loads((ROOT/"research/classical_baselines/inverse_trace_sparse_partition_n17.json").read_text())
    instance = record["original_instance"]
    calls = []

    def replay(block, c, d0, **kwargs):
        expected = record["blocks"][len(calls)]
        assert block == expected["run"]["instance"]
        assert (c, d0) == (expected["c"], expected["d0"])
        assert block["checks"] == instance["checks"]
        calls.append(kwargs)
        return deepcopy(expected["run"])

    monkeypatch.setattr(partition, "run_experiment", replay)
    result = partition.run_partitioned_experiment(instance, 1, 0)
    assert len(calls) == 2
    assert [len(b["indices"]) for b in result["blocks"]] == [139, 150]
    assert sum(instance["targets"]) == 18
    assert result["witness"] == record["witness"] and verify_word(instance, result["witness"])
    assert all(b["run"]["success_certificate"]["status"] == "BOUND_INCONCLUSIVE"
               for b in result["blocks"])
    assert not result["unrestricted_target_solver_established"]


def test_failure_in_either_block_is_not_a_full_witness(monkeypatch):
    record = json.loads((ROOT/"research/classical_baselines/inverse_trace_sparse_partition_n17.json").read_text())
    runs = [deepcopy(block["run"]) for block in record["blocks"]]
    runs[1].update(status="UNKNOWN_TRIAL_LIMIT", witness=None)
    monkeypatch.setattr(partition, "run_experiment", lambda *args, **kwargs: runs.pop(0))
    result = partition.run_partitioned_experiment(record["original_instance"], 1, 0)
    assert result["witness"] is None and not result["full_original_word_verified"]
    assert len(result["blocks"][0]["run"]["trials"]) == 23
    assert result["blocks"][1]["run"]["status"] == "UNKNOWN_TRIAL_LIMIT"


def test_bad_subsolver_word_cannot_cross_original_verifier(monkeypatch):
    record = json.loads((ROOT/"research/classical_baselines/inverse_trace_singleton_subinstance_n17.json").read_text())
    monkeypatch.setattr(partition, "run_experiment",
                        lambda block, *args, **kwargs: {"witness": [0]*len(block["points"])})
    with pytest.raises(ArithmeticError, match="original-instance"):
        partition.run_zero_extended_experiment(record["original_instance"], 1, 1)


@pytest.mark.parametrize("targets", [[0]*6, [1]*6, [0, 1, 1, 0, 1, 0]])
def test_balancer_conditional_expectations_match_all_nonzero_completions(targets):
    instance = small_instance([6, 1, 4, 0, 3, 2], targets)
    result = partition.balanced_trace_partition(instance)
    previous = Fraction(*result["initial_mean_square"])
    for step in result["steps"]:
        fixed, prefix = step["fixed_bits"], step["functional_prefix"]
        completions = [u for u in range(1, 8) if u % (1 << fixed) == prefix]
        values = [sum((-1)**(b+(a & u).bit_count())
                      for a, b in zip(instance["points"], targets))**2 for u in completions]
        observed = Fraction(sum(values), len(values))
        assert observed == Fraction(*step["mean_square"]) <= previous
        previous = observed
    assert result["c"] != 0 and result["coordinate_functional"] != 0
    assert previous == result["imbalance"]**2
    assert not result["field_table_enumerated"]
    for a in range(8):
        assert int((element(3, result["c"])*element(3, a)).trace()) == (
            a & result["coordinate_functional"]).bit_count() % 2


@pytest.mark.parametrize("bits", [5, 7, 17, 61])
def test_balancer_native_bound_without_enumerating_field(bits):
    N = bits*bits
    instance = {"bits": bits, "points": list(range(N)),
                "targets": [(i*i+3*i+7).bit_count() % 2 for i in range(N)],
                "checks": N//8,
                "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}
    before = deepcopy(instance)
    result = partition.balanced_trace_partition(instance)
    assert instance == before and result == partition.balanced_trace_partition(instance)
    assert abs(result["imbalance"]) <= bits
    assert all((N-bits)//2 <= len(b["indices"]) <= (N+bits)//2 for b in result["blocks"])
    assert Fraction(*result["initial_mean_square"]) < N+1


def test_balanced_native_theorem_does_not_turn_capped_failure_into_witness(monkeypatch):
    bits, N, K = 61, 61*61, 61*61//8
    instance = {"bits": bits, "points": list(range(N)),
                "targets": [i.bit_count() % 2 for i in range(N)], "checks": K,
                "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}
    calls = []

    def no_trials(block, c, d0, **kwargs):
        assert block["checks"] == K and kwargs["max_trials"] == 0
        calls.append(block)
        return {"status": "UNKNOWN_TRIAL_LIMIT", "witness": None, "trials": []}

    monkeypatch.setattr(partition, "run_experiment", no_trials)
    result = partition.run_balanced_experiment(instance, max_trials=0)
    assert len(calls) == sum(any(instance["targets"][i] for i in b["indices"])
                             for b in result["balance"]["blocks"])
    assert calls
    assert result["native_family_expected_polynomial_search_theorem_applies"]
    assert result["iid_partition_bound_established"]
    assert result["expected_total_iid_proposals_upper"] == sum(
        c["expected_iid_trials_upper"] for c in result["short_sum_certificates"])
    assert result["status"] == "UNKNOWN_PARTITION_TRIAL_LIMIT" and result["witness"] is None
    assert not result["full_original_word_verified"]
    assert not result["seeded_experiment_is_iid_proof"]


def test_new_scope_is_not_advertised_on_the_finite_n17_control(monkeypatch):
    record = json.loads((ROOT/"research/classical_baselines/inverse_trace_sparse_partition_n17.json").read_text())
    monkeypatch.setattr(partition, "run_experiment", lambda *args, **kwargs: {
        "status": "UNKNOWN_TRIAL_LIMIT", "witness": None, "trials": []})
    result = partition.run_balanced_experiment(record["original_instance"], max_trials=0)
    assert not result["native_family_expected_polynomial_search_theorem_applies"]
    assert not result["iid_partition_bound_established"]
    assert not result["unrestricted_target_solver_established"]


def test_both_partition_artifacts_replay_exact_norms_and_original_binary_constraints():
    for name in ("inverse_trace_singleton_subinstance_n17", "inverse_trace_sparse_partition_n17"):
        record = json.loads((ROOT/"research/classical_baselines"/(name+".json")).read_text())
        original = record["original_instance"]
        modulus = sum(c << j for j, c in enumerate(original["field_modulus_coefficients"]))
        assert verify_native_independently(17, original["points"], original["checks"],
                                            original["targets"], record["witness"], modulus)["valid"]
        runs = [record["block_run"]] if "block_run" in record else [b["run"] for b in record["blocks"]]
        for run in runs:
            instance = run["instance"]
            assert instance["checks"] == original["checks"] == 36
            rng = Random(run["seed"])
            s = len(instance["points"])-2*instance["checks"]-1
            for j, trial in enumerate(run["trials"]):
                T = [rng.getrandbits(17) for _ in range(s)]+[1]
                assert trial["trial"] == j
                assert trial["T_sha256"] == hashlib.sha256(json.dumps(T).encode()).hexdigest()
            assert T == run["certificate"]["T"]
            ring = fq_default_poly_ctx(field(17))
            polys = {key: ring([element(17, a) for a in run["certificate"][key]])
                     for key in ("P", "D", "T", "F", "U", "A")}
            P = ring.one()
            for a in instance["points"]:
                P *= ring.gen()+element(17, a)
            assert polys["P"] == P and polys["D"] == P.derivative()
            assert polys["F"] == polys["D"]**2 % P+P*polys["T"]
            C = ring.gen()*element(17, run["c"])+element(17, run["d0"])
            assert polys["U"]**2+polys["U"]*polys["A"]+C*polys["A"]**2 == polys["F"]
            assert word_from_norm(instance, run["c"], run["d0"], polys["U"], polys["A"]) == run["witness"]


def test_matched_flat_baselines_preserve_the_same_inputs_and_verified_words():
    artifact = json.loads((ROOT/"research/classical_baselines/inverse_trace_partition_matched_flats_n17.json").read_text())
    assert not artifact["asymptotic_solver_established_by_these_runs"]
    assert not artifact["quantum_speedup_evidence"]
    for case in artifact["cases"]:
        source = ROOT/case["input_artifact"]
        assert case["input_artifact_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
        original = case["original_instance"]
        assert original == json.loads(source.read_text())["original_instance"]
        run = case["run"]
        assert run["flat_dimension"] == 3 and run["binary_variables"] == 867
        assert run["linear_system"]["rank"] == run["binary_equations"] == 612
        assert run["input"]["points"] == original["points"]
        assert run["input"]["targets"] == original["targets"]
        assert run["input"]["checks"] == original["checks"]
        assert verify_native_independently(17, original["points"], original["checks"],
                                            original["targets"], run["witness"],
                                            run["input"]["field_modulus"])["valid"]
