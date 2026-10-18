"""All-pairs semantics, oblivious scheduling and reversible-history falsifiers."""
from itertools import product
import json
from pathlib import Path
from random import Random
import subprocess
import sys

import pytest

from dcp_oblivious_bounded_join import _Tape, join_xor, schedule
from theorems.dcp_oblivious_tree_merge import REPORT, build_report, native_leaf_inputs

ROOT = Path(__file__).resolve().parents[1]


def expected(left, right, capacity):
    pairs = [(a[1], i, j, a[2], b[2]) for i, a in enumerate(left) for j, b in enumerate(right)
             if a[0] and b[0] and a[1] == b[1]]
    pairs.sort()
    C = min(capacity, len(left)*len(right))
    rows = [(1, row[3], row[4]) for row in pairs[:C]] if len(pairs) <= capacity else []
    return rows + [(0, 0, 0)]*(C-len(rows)), len(pairs)


def test_exhaustive_two_key_two_slot_validity_and_all_capacity_boundaries():
    possibilities = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for assignments in product(possibilities, repeat=4):
        left = [(valid, key, i+1) for i, (valid, key) in enumerate(assignments[:2])]
        right = [(valid, key, i+3) for i, (valid, key) in enumerate(assignments[2:])]
        for capacity in (1, 2, 3, 4):
            result = join_xor(left, right, capacity, 1, 3)
            rows, count = expected(left, right, capacity)
            assert result["target"] == rows
            assert result["basis_pair_count_diagnostic"] == count
            assert result["overflow_output"] == int(count > capacity)
            assert result["workspace_clean"] is True


def test_unequal_non_power_of_two_inputs_duplicate_rows_and_dense_collisions():
    rng = Random(1467)
    for _ in range(80):
        left = [(rng.randrange(2), rng.randrange(4), rng.randrange(16)) for _ in range(rng.randrange(1, 6))]
        right = [(rng.randrange(2), rng.randrange(4), rng.randrange(16)) for _ in range(rng.randrange(1, 6))]
        capacity = rng.randrange(1, 12)
        result = join_xor(left, right, capacity, 2, 4)
        rows, count = expected(left, right, capacity)
        assert result["target"] == rows
        assert result["basis_pair_count_diagnostic"] == count
    rows = [(1, 0, 3)]*4
    result = join_xor(rows, rows, 16, 1, 3)
    assert result["target"] == [(1, 3, 3)]*16
    assert result["basis_pair_count_diagnostic"] == 16


def test_arbitrary_target_wires_and_overflow_wire_are_true_xor_involutions():
    left, right = [(1, 0, 7), (1, 1, 3)], [(1, 0, 5), (1, 0, 6)]
    for capacity in (1, 3, 4):
        C = min(capacity, 4)
        target = [(i % 2, i % 8, (i+3) % 8) for i in range(C)]
        result = join_xor(left, right, capacity, 1, 3, target, 1)
        undone = join_xor(left, right, capacity, 1, 3, result["target"], result["overflow_output"])
        assert undone["target"] == target
        assert undone["overflow_output"] == 1 and undone["workspace_clean"]


def test_no_match_unique_match_and_overflow_have_identical_schedule_and_paid_histories():
    matrices = [([(0, 0, 0)]*4, [(0, 0, 0)]*4),
                ([(1, 0, 1)]+[(0, 0, 0)]*3, [(1, 0, 2)]+[(0, 0, 0)]*3),
                ([(1, 0, 1)]*4, [(1, 0, 2)]*4)]
    receipts = [join_xor(left, right, 4, 1, 3) for left, right in matrices]
    assert [r["basis_pair_count_diagnostic"] for r in receipts] == [0, 1, 16]
    assert all(r["schedule"] == receipts[0]["schedule"] and r["metrics"] == receipts[0]["metrics"] for r in receipts)
    assert receipts[0]["schedule"]["persistent_workspace_bits"] > 1000
    assert receipts[0]["schedule"]["data_dependent_RAM_reads"] is False


def test_native_signed_component_keys_and_payloads_are_not_packed_cyclic_sums():
    report = build_report()
    A = report["native_labels"]
    for control in report["native_controls"]:
        left, right = native_leaf_inputs(A, control["assignment"])
        assert control["left"] == left and control["right"] == right
        rows, count = expected(left, right, control["capacity"])
        assert control["target"] == rows and control["basis_pair_count_diagnostic"] == count
        for valid, u, v in rows:
            if valid:
                # Physical supports are disjoint; sums on the filtered chunk cancel.
                assert (u & 255) & (v & 255) == 0
                assert (((u >> 8) & 3) + ((v >> 8) & 3)) % 4 == 0


def test_linear_sized_record_schedule_beats_quadratic_cells_asymptotically():
    for exponent in (16, 32, 64, 128):
        L = 1 << exponent
        S = schedule(L, L, 32*L, exponent, 4*exponent)
        assert sum(S["sort_sizes"]) <= 1024*L
        assert S["comparators"] < 2048*L*(exponent+12)**2
        assert sum(S["sort_sizes"]) < L*L


@pytest.mark.parametrize("left,right,capacity,key_bits,payload_bits", [
    ([], [(1, 0, 0)], 1, 1, 1),
    ([(True, 0, 0)], [(1, 0, 0)], 1, 1, 1),
    ([(1, 2, 0)], [(1, 0, 0)], 1, 1, 1),
    ([(1, 0, 2)], [(1, 0, 0)], 1, 1, 1),
    ([(1, 0, 0)], [(1, 0, 0)], 0, 1, 1),
    ([(1, 0, 0)], [(1, 0, 0)], 1, True, 1),
])
def test_invalid_source_or_wire_dimensions_fail_before_interpretation(left, right, capacity, key_bits, payload_bits):
    with pytest.raises(ValueError):
        join_xor(left, right, capacity, key_bits, payload_bits)


def test_bad_output_wires_and_caps_fail_closed():
    for target, overflow in (([], 0), ([(2, 0, 0)], 0), ([(0, 2, 0)], 0), ([(0, 0, 0)], True)):
        with pytest.raises(ValueError):
            join_xor([(1, 0, 0)], [(1, 0, 0)], 1, 1, 1, target, overflow)
    with pytest.raises(ValueError, match="UNKNOWN"):
        join_xor([(1, 0, 0)]*8192, [(1, 0, 0)]*8192, 8192, 1, 1)


def test_tape_rejects_forged_record_width_and_nonzero_cleanup():
    tape = _Tape()
    with pytest.raises(ArithmeticError):
        tape.compute(lambda: [(4,)], 1, 2)
    source = [1]
    rows = tape.compute(lambda: [(source[0],)], 1, 2)
    rows[0] = (2,)
    with pytest.raises(ArithmeticError, match="uncompute"):
        tape.reverse()


def test_live_artifact_and_readonly_cli():
    report = build_report()
    assert json.loads(REPORT.read_text()) == json.loads(json.dumps(report))
    assert report["whole_tree_receiver_uses_this_backend"] is False
    assert report["accepted_speedup_candidate"] is False
    before = REPORT.read_bytes()
    result = subprocess.run([sys.executable, "qsearch.py", "dcp-oblivious-tree-merge", "--no-write"], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert REPORT.read_bytes() == before
