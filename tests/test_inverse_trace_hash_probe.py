"""Same-input campaign checks; no native-size scaling claims from calibration."""
from itertools import product
import json

import pytest

from theorems.balanced_codeword_filter import reciprocal_trace
from theorems.explicit_quadratic_opi import field
from theorems.inverse_trace_hash_probe import prepare_probe, run_probe, trace_coordinates
from theorems.inverse_trace_smt import native_instance


@pytest.mark.parametrize("bits", [2, 3, 5, 7])
def test_canonical_trace_coordinates_are_bijective(bits):
    from theorems.explicit_quadratic_opi import element
    pivot, positions, basis = trace_coordinates(bits)
    assert int(element(bits, pivot).trace()) == 1
    assert len(positions) == len(basis) == bits-1
    for bit in (0, 1):
        values = set()
        for coefficients in product((0, 1), repeat=bits-1):
            y = bit*pivot
            for c, v in zip(coefficients, basis):
                if c:
                    y ^= v
            assert int(element(bits, y).trace()) == bit
            values.add(y)
        assert len(values) == 1 << (bits-1)


@pytest.mark.parametrize("bits", [5, 7])
def test_native_probe_matches_independent_slice_and_prange(bits):
    instance = native_instance(bits)
    before = json.dumps(instance, sort_keys=True)
    row = run_probe(instance, cells=2, prange_trials=32, timeout_ms=5000)
    assert json.dumps(instance, sort_keys=True) == before
    assert not row["uniform_sampler"] and not row["hardness_evidence"]
    assert not row["whole_workflow_wall_clock_cap_enforced"]
    descriptor = row["residual"]
    expected_surplus = (3*instance["checks"]+2*bits-1)//(2*bits)
    assert descriptor["free_field_variables"] == expected_surplus
    assert descriptor["source"] == "FIXED_ACCEPTED_PREFIX"
    for i, x in descriptor["accepted_prefix"]:
        assert reciprocal_trace(bits, x) == instance["targets"][i]
    for cell in row["cells"]:
        enum, ref = cell["enumeration"], cell["independent_reference"]
        assert enum["complete"], "calibration must actually complete, not only return valid subsets"
        assert ref["status"] == "EXACT_FULL_COORDINATE_SPACE"
        assert not ref["shared_hash_elimination"]
        assert ref["solutions"] is not None
        assert set(s["u"] for s in enum["solutions"]).issubset(ref["solutions"])
        assert set(s["u"] for s in enum["solutions"]) == set(ref["solutions"])
    assert row["prange"]["same_residual_input"]
    assert not row["prange"]["matched_wall_clock_budget"]


@pytest.mark.parametrize("supply_anchor", [False, True])
def test_witness_conditioned_source_is_explicit_not_initialization(supply_anchor):
    bits = 3
    instance = {"bits": bits, "points": [0, 1, 2, 3], "checks": 1,
                "targets": [0]*4,
                "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}
    row = run_probe(instance, surplus=1, cells=2, anchor_word=[0]*4,
                    prange_trials=8, timeout_ms=5000, supply_anchor=supply_anchor)
    assert row["residual"]["source"] == "WITNESS_CONDITIONED_DIAGNOSTIC"
    assert row["residual"]["anchor_u"] == 0
    assert not row["residual"]["anchor_acquisition_charged"]
    assert row["known_anchor_supplied_to_solver"] is supply_anchor
    for cell in row["cells"]:
        assert cell["hash_rhs"] == 0
        assert cell["enumeration"]["complete"]
        assert 0 in [s["u"] for s in cell["enumeration"]["solutions"]]


def test_preparation_rejects_changed_or_invalid_anchors_and_surplus():
    instance = native_instance(5)
    with pytest.raises(ValueError):
        prepare_probe(instance, anchor_word=[0]*25)
    for surplus in (0, True, 30):
        with pytest.raises(ValueError):
            prepare_probe(instance, surplus=surplus)
    with pytest.raises(ValueError, match="explicit anchor"):
        run_probe(instance, supply_anchor=True)


def test_exact_reference_never_promotes_a_capped_solver():
    row = run_probe(native_instance(5), cells=2, max_models=0, prange_trials=0)
    for cell in row["cells"]:
        assert cell["enumeration"]["status"] == "PARTIAL"
        assert not cell["enumeration"]["complete"]
        assert cell["independent_reference"]["solutions"] is not None
        assert cell["independent_reference"]["reported_complete_set_matches"] is None


@pytest.mark.parametrize("fault", ["invalid_models", "duplicate_models"])
def test_solver_integrity_failure_stops_entire_campaign(monkeypatch, fault):
    import theorems.inverse_trace_hash_cell as backend
    original, calls = backend.enumerate_cell, []

    def faulty(*args, **kwargs):
        row = original(*args, **kwargs)
        row.update(complete=False, status="PARTIAL", cell_cardinality=None)
        row[fault] = 1
        calls.append(row)
        return row

    monkeypatch.setattr(backend, "enumerate_cell", faulty)
    with pytest.raises(ArithmeticError, match="campaign stopped"):
        run_probe(native_instance(5), cells=2, prange_trials=0)
    assert len(calls) == 1


def test_small_reference_catches_shared_hash_elimination_fault(monkeypatch):
    import theorems.inverse_trace_hash_cell as backend
    import theorems.inverse_trace_hash_probe as probe
    original = backend.affine_system

    def extra_constraint(equations, width):
        return original([*equations, (1, 0)], width)

    monkeypatch.setattr(backend, "affine_system", extra_constraint)
    monkeypatch.setattr(probe, "affine_system", extra_constraint)
    instance = {"bits": 2, "points": [0, 1, 2, 3], "checks": 1,
                "targets": [0]*4,
                "field_modulus_coefficients": list(map(int, field(2).modulus().coeffs()))}
    with pytest.raises(ArithmeticError, match="omitted a solution"):
        run_probe(instance, surplus=1, cells=1, anchor_word=[0]*4, prange_trials=0)


def test_source_change_during_probe_is_not_silently_fingerprinted(monkeypatch):
    import theorems.inverse_trace_hash_probe as probe
    before = probe._source_fingerprints()
    changed = {**before, "theorems/inverse_trace_hash_cell.py": "changed"}
    snapshots = iter((before, changed))
    monkeypatch.setattr(probe, "_source_fingerprints", lambda: next(snapshots))
    with pytest.raises(RuntimeError, match="ambiguous provenance"):
        run_probe(native_instance(5), cells=1, prange_trials=0)
