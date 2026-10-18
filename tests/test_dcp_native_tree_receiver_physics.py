"""Native graph, overflow, cleanup, density and paid-cost falsifiers."""
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
from random import Random
import subprocess
import sys

import numpy as np
import pytest

from dcp_affine_marked_pairing import affine_hash
from theorems.dcp_native_tree_receiver import (
    CONTRACT, CONTRACT_ID, REPORT, build_report, evaluate_xor, make_program,
    propose, resources, validate_program,
)
from theorems.dcp_nonlinear_fiber_pairing import phase_value, program_value, wire_map

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "research/certificates/dcp_native_tree_receiver_crosscheck.js"


def full_graph_reference(P, x):
    """Untruncated Cartesian leaf tuples, not production sorting/compaction."""
    A, R, H, c = validate_program(P)
    n, k, L, B, w = (R[s] for s in ("components", "leaf_count", "leaf_list_length", "block_width", "leaf_support_weight"))
    leaves = []
    for j in range(k):
        supports = [sum(1 << (j*B+i) for i in indices) for indices in list(combinations(range(B), w))[:L]]
        leaves.append([(u, tuple(sum(a*(1-2*(x >> i & 1)) for i, a in enumerate(row) if u >> i & 1) % 4 for row in A)) for u in supports])
    # Full intermediate lists diagnose overflow independently of truncation.
    current, overflow = leaves, False
    for level in range(1, P["depth"]):
        next_level = []
        for left, right in zip(current[::2], current[1::2]):
            records = []
            for (u, a), (v, b) in product(left, right):
                value = tuple((s+t) % 4 for s, t in zip(a, b))
                if not any(value[(level-1)*P["chunk_components"]:level*P["chunk_components"]]):
                    records.append((u ^ v, value))
            overflow |= len(records) > R["capacity"]
            next_level.append(records)
        current = next_level
    neighbors = []
    for (u, a), (v, b) in product(*current):
        if not any((s+t) % 4 for s, t in zip(a, b)):
            y = x ^ u ^ v
            if affine_hash(y, H, c) == 0:
                neighbors.append(y)
    expected = None
    if not overflow and affine_hash(x, H, c) == 0 and len(neighbors) == 1:
        expected = neighbors[0]
    return expected, overflow, neighbors


@pytest.fixture(scope="module")
def report():
    return build_report()


def test_all_nonoverflow_native_graph_proposals_match_full_cartesian_reference():
    rng = Random(1729)
    for depth, cap in ((1, None), (2, 4), (2, None)):
        k = 1 << depth
        A = [[rng.randrange(4) for _ in range(4*k)] for _ in range(depth+1)]
        P = make_program(A, depth, 1, rng.getrandbits(2*(4*k+1)), capacity=cap)
        assignments = range(256) if depth == 1 else range(24)
        for x in assignments:
            expected, overflow, _ = full_graph_reference(P, x)
            row = evaluate_xor(P, x)
            assert row["whole_attempt_overflow"] == overflow
            assert row["workspace_clean"] is True
            assert propose(P, x) == expected


def test_overflow_is_not_partner_invariant_and_cannot_be_silently_accepted(report):
    control = next(c for c in report["finite_controls"] if c["control_id"] == "overflow-is-not-partner-invariant")
    P, (x, y) = control["program"], control["known_untruncated_edge"]
    _, overflow_x, neighbors_x = full_graph_reference(P, x)
    _, overflow_y, neighbors_y = full_graph_reference(P, y)
    assert y in neighbors_x and x in neighbors_y
    assert overflow_x is True and overflow_y is False
    assert evaluate_xor(P, x)["output"] == 0
    assert phase_value(P["coarse_labels"], x, 4) == phase_value(P["coarse_labels"], y, 4)


def test_all_zero_labels_trigger_attempt_wide_rejection_not_group_value_deduplication():
    P = make_program([[0]*16]*3, 2, 1, capacity=4)
    for x in (0, 1, 65535):
        row = evaluate_xor(P, x, 123)
        assert row["node_overflows"] == [1, 1]
        assert row["whole_attempt_overflow"] is True
        assert row["output"] == 123
        assert row["workspace_clean"] is True
        # Distinct physical support pairs remain distinct even at equal keys.
        assert row["truncated_root_neighbor_count_not_accepted_on_overflow"] == 16


def test_fixed_address_operation_counts_do_not_depend_on_success_or_input(report):
    for control in report["finite_controls"]:
        P = control["program"]
        R = P["resource_ledger"]
        metrics = [row["metrics"] for row in control["evaluations"]]
        assert all(metric == metrics[0] for metric in metrics)
        for key, count in metrics[0].items():
            assert count == R["one_XOR_F_"+key]
        assert all(row["workspace_clean"] for row in control["evaluations"])
        assert R["accepted_six_XOR_F_comparators"] == 6*metrics[0]["comparators"]
        assert R["failed_four_XOR_F_comparators"] == 4*metrics[0]["comparators"]
        assert R["compiler_live_qubits_excluding_arithmetic_scratch"] == R["persistent_workspace_bits"] + 3*P["width"] + 4


def test_default_capacity_and_small_failure_capacity_have_different_proof_receipts():
    default, capped = resources(2, 1), resources(2, 1, capacity=4)
    assert default["capacity"] == 12288
    assert default["root_child_slots"] == 16  # Public combinatorial maximum, not observed list size.
    assert default["moment_overflow_lower_bound_applicable"] is True
    assert capped["moment_overflow_lower_bound_applicable"] is False
    assert capped["moment_coarse_lower_bound_IF_source_premises"] is None
    assert default["persistent_workspace_bits"] > capped["persistent_workspace_bits"]


def test_depth_three_reverses_all_levels_and_overflow_histories():
    rng = Random(1830)
    for A in ([[0]*32]*4, [[rng.randrange(4) for _ in range(32)] for _ in range(4)]):
        P = make_program(A, 3, 1, capacity=4)
        R = P["resource_ledger"]
        for x in (0, 17, (1 << 32)-1):
            row = evaluate_xor(P, x, 47)
            assert row["workspace_clean"] is True
            assert row["metrics"]["overflow_prefix_steps"] == 12
            assert len(row["node_overflows"]) == 6
            assert row["persistent_workspace_bits"] == R["persistent_workspace_bits"]


def test_padded_slot_schedule_and_non_power_of_two_capacity_remain_fixed():
    A = [[(i+j) % 4 for i in range(32)] for j in range(4)]
    P = make_program(A, 3, 1, capacity=5)
    for x in range(8):
        row = evaluate_xor(P, x)
        assert row["workspace_clean"] is True
    levels = P["resource_ledger"]["nonroot_levels"]
    assert levels[1]["candidate_cells"] == 25
    assert levels[1]["padded_cells"] == 32


def test_nonzero_xor_target_is_restored_after_two_calls(report):
    for control in report["finite_controls"]:
        P = control["program"]
        for row in control["evaluations"][:4]:
            x = row["assignment"]
            first = evaluate_xor(P, x, 171)
            second = evaluate_xor(P, x, first["output"])
            assert first["output"] == 171 ^ row["output"]
            assert second["output"] == 171 and second["workspace_clean"]


def test_coarse_only_program_does_not_read_higher_lifts_or_secret():
    rng = Random(16)
    A = [[rng.randrange(4) for _ in range(16)] for _ in range(3)]
    lifts = [[a + 4*rng.randrange(128) for a in row] for row in A]
    assert make_program(A, 2, 1, 17) == make_program(lifts, 2, 1, 17)
    assert make_program(A, 2, 1, 17)["selection_access"] == "coarse-labels-and-independent-unfiltered-affine-seed"


def test_six_call_accept_order_inverse_and_unknown_phase_density(report):
    K = report["six_call_instrument"]
    P, m, t = K["program"], K["program"]["width"], K["phase_bits"]
    A = [[int(a, 16) for a in row] for row in K["public_labels_hex"]]
    assert len(K["pairs"]) == 16
    for pair in K["pairs"]:
        x, y = pair["first"], pair["second"]
        assert program_value(P, x) == y and program_value(P, y) == x
        for endpoint, orientation in ((x, 0), (y, 1)):
            accept = wire_map(endpoint, P, A, t, 2, "accept")
            ordered = wire_map(accept, P, A, t, 2, "order")
            assert ordered == x | (1 << (3*m+2)) | (orientation << (3*m+3))
            assert wire_map(ordered, P, A, t, 2, "order", inverse=True) == accept
            assert wire_map(accept, P, A, t, 2, "accept", inverse=True) == endpoint
        label = [int(a, 16) for a in pair["descended_label_hex"]]
        v = float(Fraction(3, 4) ** (x ^ y).bit_count())
        for secret in product(range(8), repeat=2):
            phases = [sum(s*a for s, a in zip(secret, phase_value(A, z, 8))) % 8 for z in (x, y)]
            amps = np.exp(2j*np.pi*np.array(phases)/8) / 16
            density = np.outer(amps, amps.conj())
            density[0, 1] *= v
            density[1, 0] *= v
            mass = np.trace(density).real
            angle = np.pi * (sum(s*a for s, a in zip(secret, label)) % 2)
            expected = np.array([[1, v*np.exp(-1j*angle)], [v*np.exp(1j*angle), 1]]) / 2
            assert mass == pytest.approx(2/256)
            assert np.allclose(density/mass, expected, atol=1e-14)


@pytest.mark.parametrize("mutation", [
    lambda p: p.update(overflow_policy="TRUNCATE_AND_ACCEPT"),
    lambda p: p.update(seed_conditioned_on_success=True),
    lambda p: p.update(uniform_efficient_program_supplied=True),
    lambda p: p.update(table_lookup_is_a_free_coherent_oracle=True),
    lambda p: p.update(selection_access="private-error-array"),
    lambda p: p["resource_ledger"].update(persistent_workspace_bits=0),
    lambda p: p["resource_ledger"].update(one_XOR_F_candidate_cell_evaluations=0),
    lambda p: p.update(hash_rows_hex=[]),
    lambda p: p.update(width=True),
    lambda p: p["coarse_labels"][0].__setitem__(0, 4),
])
def test_forged_cost_source_and_overflow_claims_are_rejected(mutation):
    P = make_program([[1]*16]*3, 2, 1)
    mutation(P)
    with pytest.raises(ValueError):
        evaluate_xor(P, 0)


def test_validation_precedes_assignment_dependent_work(monkeypatch):
    import theorems.dcp_native_tree_receiver as module
    def forbidden(*args):
        pytest.fail("leaf arithmetic ran before input validation")
    monkeypatch.setattr(module, "_leaf", forbidden)
    P = make_program([[0]*8]*2, 1, 1)
    for x, out in ((-1, 0), (256, 0), (0, -1), (0, 512)):
        with pytest.raises(ValueError):
            evaluate_xor(P, x, out)


def test_interpreter_caps_are_unknown_not_research_negatives():
    P = make_program([[0]*64]*8, 3, 2)
    with pytest.raises(ValueError, match="UNKNOWN"):
        evaluate_xor(P, 0)


def test_actual_depth_two_instrument_preserves_phase_after_nonroot_cleanup(report):
    control = next(c for c in report["finite_controls"] if "known_reciprocal_pair" in c)
    P, A = control["program"], control["full_labels"]
    x, y = control["known_reciprocal_pair"]
    m = P["width"]
    assert P["depth"] == 2
    assert propose(P, x) == y and propose(P, y) == x
    delta = tuple((b-a) % 8 for a, b in zip(phase_value(A, x, 8), phase_value(A, y, 8)))
    assert all(d % 4 == 0 for d in delta) and any(delta)
    for endpoint, orientation in ((x, 0), (y, 1)):
        accepted = wire_map(endpoint, P, A, 3, 2, "accept")
        result = wire_map(accepted, P, A, 3, 2, "order")
        assert result == x | (1 << (3*m+2)) | (orientation << (3*m+3))
        assert evaluate_xor(P, endpoint)["workspace_clean"]
    v = float(Fraction(3, 4) ** (x ^ y).bit_count())
    assert (x ^ y).bit_count() == P["resource_ledger"]["physical_mask_width"] == 4
    for secret in product(range(8), repeat=3):
        phases = [sum(s*a for s, a in zip(secret, phase_value(A, z, 8))) % 8 for z in (x, y)]
        amp = np.exp(2j*np.pi*np.array(phases)/8) / 256
        density = np.outer(amp, amp.conj())
        density[0, 1] *= v
        density[1, 0] *= v
        angle = 2*np.pi*sum(s*d for s, d in zip(secret, delta))/8
        expected = np.array([[1, v*np.exp(-1j*angle)], [v*np.exp(1j*angle), 1]])/2
        assert np.trace(density).real == pytest.approx(2/65536)
        assert np.allclose(density/np.trace(density), expected, atol=1e-13)


def test_report_contract_live_artifact_and_independent_replay(report):
    assert json.loads(CONTRACT.read_text())["contract_id"] == CONTRACT_ID
    assert json.loads(REPORT.read_text()) == report
    assert report["accepted_speedup_candidate"] is False
    assert report["hardware_gate_export_implemented"] is False
    result = subprocess.run(["node", str(CHECKER), str(REPORT)], capture_output=True, text=True, check=True)
    assert json.loads(result.stdout)["status"] == "ok"


@pytest.mark.parametrize("field", ["output", "workspace_clean", "whole_attempt_overflow", "metrics", "persistent_workspace_bits"])
def test_independent_checker_rejects_forged_execution_receipts(report, tmp_path, field):
    payload = deepcopy(report)
    row = payload["finite_controls"][0]["evaluations"][0]
    if field == "metrics":
        row[field]["comparators"] += 1
    elif type(row[field]) is bool:
        row[field] = not row[field]
    else:
        row[field] += 1
    path = tmp_path / "forged.json"
    path.write_text(json.dumps(payload))
    result = subprocess.run(["node", str(CHECKER), str(path)], capture_output=True, text=True)
    assert result.returncode != 0


def test_cli_no_write_preserves_live_artifact():
    original = REPORT.read_bytes()
    result = subprocess.run([sys.executable, "qsearch.py", "dcp-native-tree-receiver", "--no-write"], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert REPORT.read_bytes() == original
