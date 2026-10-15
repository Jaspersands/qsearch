"""Public source scheduling is conditional; successful attacks kill controls."""
from fractions import Fraction
import json
from pathlib import Path
import subprocess

import pytest

from theorems.lattice_localization_gap_frontier import public_schedule, attack_control
from theorems.planted_qary_usvp_source import PublicQaryLattice

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "research/classical_baselines/lattice_localization_gap_frontier.json"
CHECKER = ROOT / "research/certificates/lattice_localization_gap_frontier_crosscheck.js"


@pytest.mark.parametrize("n", [4, 16, 32, 64, 128, 512])
@pytest.mark.parametrize("mode", ["constant", "inverse_log"])
def test_public_schedule_has_paid_matching_noise_and_alias_budgets(n, mode):
    p = public_schedule(n, n // 2, mode)
    epsilon = Fraction(p["epsilon"])
    for key in ("sine", "cube"):
        x = p[key]
        assert Fraction(x["total_loss_upper_IF_geometry_holds"]) <= epsilon
        assert x["sufficient_relative_gap"] ** 2 * n >= n * x["side"] ** 2
        assert x["split_prime"] - 1 > x["side"]
    assert p["sine"]["side"] <= p["cube"]["side"]
    assert p["first_free_basis_coordinate"] == n // 2
    assert p["private_hitting_coordinate_selector_used"] is False
    assert p["individual_instance_gap_certified"] is False
    assert p["efficient_robust_receiver_supplied"] is False


def test_constant_noise_is_not_silently_given_inverse_log_receiver_promise():
    p = public_schedule(64, 32, "constant")
    assert Fraction(p["epsilon"]) > Fraction(1, p["position_wires"])
    assert p["constant_noise_satisfies_inverse_log_budget"] is False


@pytest.mark.parametrize("value", [True, "16", 16.0])
def test_nonexact_dimensions_rejected(value):
    with pytest.raises(ValueError):
        public_schedule(value, 8, "constant")


def test_attack_interface_receives_public_problem_only(monkeypatch):
    import theorems.lattice_localization_gap_frontier as module
    actual = module.public_LLL_attack
    calls = []
    def checked(problem):
        assert type(problem) is PublicQaryLattice
        assert not hasattr(problem, "private")
        calls.append(problem)
        return actual(problem)
    monkeypatch.setattr(module, "public_LLL_attack", checked)
    row = attack_control(8, "constant", 10010)
    assert len(calls) == 1
    assert row["public_schedule"]["first_free_basis_coordinate"] == 4
    assert row["generator_rejects_on_classical_attack_or_uniqueness_outcome"] is False


def test_saved_controls_have_public_falsifiers_not_global_no_go():
    report = json.loads(ARTIFACT.read_text())
    assert report["controls_tested"] == 8
    assert report["classically_recovered_controls"] == 8
    assert report["source_samples_or_quantum_solver_calls_performed"] == 0
    for row in report["actual_public_attack_controls"]:
        f = row["finite_classical_falsifier"]
        assert f["classical_recovery_of_plant_verified"] is True
        assert f["all_lower_gap_lattices_dequantized"] is False
        assert row["public_attacks"]["LLL"]["plant_or_private_seed_used"] is False
        assert row["BKZ_and_general_SIS_attacks"] == "NOT_RUN_NOT_EXCLUDED"


def test_independent_public_attack_certificate_replay():
    proc = subprocess.run(["node", str(CHECKER)], capture_output=True, text=True, check=True)
    assert json.loads(proc.stdout)["verified"] is True


@pytest.mark.parametrize("tamper", ["schedule", "attack", "plant", "claim"])
def test_independent_checker_rejects_invalid_proof_or_promotion(tmp_path, tamper):
    report = json.loads(ARTIFACT.read_text())
    row = report["actual_public_attack_controls"][0]
    if tamper == "schedule":
        row["public_schedule"]["sine"]["side"] //= 2
    elif tamper == "attack":
        row["public_attacks"]["LLL"]["unimodular_row_transform"][0][0] += 1
    elif tamper == "plant":
        row["PRIVATE_AUDIT_ONLY_planted_vector"][0] *= -1
    else:
        report["accepted_speedup_candidate"] = True
    target = tmp_path / "tampered.json"
    target.write_text(json.dumps(report))
    proc = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert proc.returncode != 0
