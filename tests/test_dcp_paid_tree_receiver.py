"""Exact policy optima, paid physical access and resource counterexamples."""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess

import pytest

from theorems.dcp_paid_tree_receiver import (
    PaidTreePlan, execute_plan, direct_acquisition_budget, sufficient_quadrature_quota, fixed_forest_baseline,
    old_quota_counterexample,
)
from theorems.lattice_sine_window_source import SineWindowSource, compile_source, simulate_batch, SinePhysicalBackend

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "research/phase_workbench/dcp_paid_tree_receiver.json"
CHECKER = ROOT / "research/certificates/dcp_paid_tree_receiver_crosscheck.js"


def brute(state, N, v):
    # No masks, cache, stored Bellman actions or implementation child helper.
    best = max((v**L for k, L in state if k == N // 2), default=Fraction(0))
    for i in range(len(state)):
        for j in range(len(state)):
            if i == j:
                continue
            rest = [x for t, x in enumerate(state) if t not in (i, j)]
            a, b = state[i], state[j]
            plus = rest + [((a[0] + b[0]) % N, a[1] + b[1])]
            minus = rest + [((a[0] - b[0]) % N, a[1] + b[1])]
            best = max(best, (brute(plus, N, v) + brute(minus, N, v)) / 2)
    return best


@pytest.mark.parametrize("v", [Fraction(0), Fraction(1, 4), Fraction(3, 4), Fraction(1)])
def test_exact_policy_matches_all_three_root_forests_without_memoization(v):
    for labels in product(range(4), repeat=3):
        p = PaidTreePlan(labels, 4, v)
        assert p.value == brute([(k, 1) for k in labels], 4, v)
        assert p.states_visited == len(p.values)


def test_three_leaf_noise_is_not_two_to_the_depth():
    v = Fraction(3, 4)
    p = PaidTreePlan((1, 1, 2), 8, v)
    assert p.value == v**3 / 4
    assert p.value != v**4 / 4


def test_high_valuation_can_be_a_paid_two_leaf_jump_not_two_to_valuation():
    v = Fraction(3, 4)
    assert PaidTreePlan((1, 31), 64, v).value == v * v / 2


@pytest.mark.parametrize("N", [8, 16, 64, 256])
@pytest.mark.parametrize("v", [Fraction(1, 4), Fraction(3, 4), Fraction(1)])
def test_feedback_has_real_finite_gain_over_all_precommitted_forests(N, v):
    labels = (1, N // 2 - 1, 2)
    p = PaidTreePlan(labels, N, v)
    fixed = fixed_forest_baseline(labels, N, v)
    assert p.value == v * v / 2 + v**3 / 4
    assert Fraction(fixed["optimal_target_weighted_visibility"]) == v * v / 2
    assert fixed["complete_set_partitions_evaluated"] == 5
    assert fixed["signed_assignments_evaluated"] == (3**3 - 1) // 2


def test_source_template_rarity_is_not_a_general_feedback_no_go():
    for N in (8, 16, 32):
        templates = [(a, b, c) for a, b, c in product(range(N), repeat=3)
                     if (a + b) % N == N // 2 and c == 2 * a % N
                     and a not in (0, N // 2, N // 4, 3 * N // 4)]
        assert len(templates) == N - 4


def test_zero_labels_never_count_as_parity_recovery():
    assert PaidTreePlan((0, 0, 0), 16, "1").value == 0
    p = PaidTreePlan((8,), 16, "1/4")
    assert p.value == Fraction(1, 4)
    assert p.record()["parity_success_IF_model_and_fair_guess_on_failure"] == "5/8"


def test_invalid_or_unbounded_plans_fail_closed():
    for labels, N, v in [((True,), 8, "1"), ((8,), 8, "1"), ((1,), 7, "1"), ((1,), 8, 0.5)]:
        with pytest.raises(ValueError):
            PaidTreePlan(labels, N, v)
    with pytest.raises(ValueError, match="UNKNOWN_BELLMAN_ROOT_CAP"):
        PaidTreePlan((1,) * 9, 16, "1/2")
    with pytest.raises(ValueError, match="UNKNOWN_BELLMAN_STATE_CAP"):
        PaidTreePlan((1, 2, 3), 16, "1/2", max_states=1)


def test_raw_parity_acquisition_is_exponential_and_quota_is_only_sufficient():
    budget = direct_acquisition_budget(256, 0, 10)
    assert Fraction(budget["stratum_probability"]) == Fraction(1, 2**256)
    assert Fraction(budget["expected_original_preparations_without_sieve"]) == 10 * 2**256
    assert sufficient_quadrature_quota(16, "1/2", "1/10") == 256
    with pytest.raises(ValueError):
        sufficient_quadrature_quota(16, "0")


def test_old_factor_two_quota_is_falsified_by_one_exact_binomial_term():
    c = old_quota_counterexample()
    assert c["old_factor_two_quota_is_met"] is True
    assert Fraction(c["single_binomial_error_term_lower"]) > Fraction(c["allowed_per_stage_error"])
    assert Fraction(c["exp_m_v_squared_over_two_Taylor_lower"]) > 2 * c["ell"] / Fraction(c["total_failure_budget"])
    assert c["corrected_sufficient_quota"] > c["samples"]


class PublicOnly:
    def __init__(self, backend):
        self.backend = backend
    @property
    def source_preparations_charged(self):
        return self.backend.source_preparations_charged
    def public_view(self, rid):
        return self.backend.public_view(rid)
    def merge(self, a, b):
        return self.backend.merge(a, b)
    def measure(self, rid, axis):
        return self.backend.measure(rid, axis)


def test_executor_uses_public_only_backend_and_actual_sampled_branches():
    source = SineWindowSource(((17, 0), (16, 1)), 7, 1, 0, 2, 4)
    batch = simulate_batch(compile_source(source), 6, 86101, "receiver-test")
    p = PaidTreePlan([r.label for r in batch.receipts], 16, "1/4")
    backend = SinePhysicalBackend(batch, 86201)
    result = execute_plan(p, PublicOnly(backend), [r.id for r in batch.receipts])
    assert result["source_preparations_charged"] == 6
    assert result["unknown_phase_registers_reprepared_or_cloned"] is False
    for merge in result["transcript"]:
        left, right, out = merge["left"], merge["right"], merge["output"]
        assert set(left["original_source_receipts"]).isdisjoint(right["original_source_receipts"])
        assert set(out["original_source_receipts"]) == set(left["original_source_receipts"]) | set(right["original_source_receipts"])
        assert out["label"] == (left["label"] + (-1)**merge["actual_branch"] * right["label"]) % 16
    with pytest.raises(ValueError):
        execute_plan(p, PublicOnly(backend), [r.id for r in batch.receipts])


def test_independent_Bellman_and_physical_replay():
    proc = subprocess.run(["node", str(CHECKER)], check=True, capture_output=True, text=True)
    assert json.loads(proc.stdout)["verified"] is True


@pytest.mark.parametrize("tamper", ["value", "action", "missing_branch", "free_samples", "density", "baseline", "confidence", "claim"])
def test_checker_rejects_corrupt_policies_or_unpaid_physics(tmp_path, tamper):
    r = json.loads(ARTIFACT.read_text())
    p = r["exact_finite_policy_controls"][0]
    if tamper == "value":
        p["optimal_target_weighted_visibility"] = "1"
    elif tamper == "action":
        p["Bellman_certificate"][-1]["action"] = ["stop", None]
    elif tamper == "missing_branch":
        p["Bellman_certificate"].pop(0)
    elif tamper == "free_samples":
        r["actual_source_preparations_charged"] = 0
    elif tamper == "density":
        c = r["actual_physical_source_controls"][0]["compiled_source_sampling_audit"]
        first = next(iter(c["PRIVATE_AUDIT_ONLY_density_matrices"]))
        c["PRIVATE_AUDIT_ONLY_density_matrices"][first][0][0][0] = 1
    elif tamper == "baseline":
        p["fixed_forest_baseline"]["optimal_target_weighted_visibility"] = "1"
    elif tamper == "confidence":
        r["old_quadrature_confidence_claim_counterexample"]["single_binomial_error_term_lower"] = "0"
    else:
        r["efficient_noisy_receiver_supplied"] = True
    target = tmp_path / "corrupted.json"
    target.write_text(json.dumps(r))
    proc = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert proc.returncode != 0
