from fractions import Fraction
from itertools import combinations, permutations
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from theorems import nonabelian_barrier_scope_audit as audit


@pytest.mark.parametrize("n", (3, 4, 5, 6))
def test_actual_sparse_hadamard_branches_on_every_coset(n):
    control = audit.transposition_coset_control(n)
    for row in control["rows"]:
        assert row["P_plus"] == (["1"] if row["hidden_transposition"] == [0, 1] else ["1/2"])
    assert control["coset_states_checked"] == control["group_order"]*len(control["rows"])
    assert control["actual_sparse_H_controlled_R_H_branches"]
    assert not control["test_uses_hidden_element"]


def test_independent_dense_regular_state_and_actual_hadamard_circuit():
    n = 4
    group = tuple(permutations(range(n)))
    index = {g: i for i, g in enumerate(group)}
    identity = np.eye(len(group))
    public_action = np.zeros_like(identity)
    for g, column in index.items():
        public_action[index[audit.right_swap(g, (0, 1))], column] = 1
    H = np.array([[1, 1], [1, -1]])/np.sqrt(2)
    controlled = np.block([[identity, 0*identity], [0*identity, public_action]])
    circuit = np.kron(H, identity) @ controlled @ np.kron(H, identity)
    assert np.allclose(circuit.conj().T @ circuit, np.eye(2*len(group)))
    for pair in combinations(range(n), 2):
        rho = np.zeros_like(identity)
        for g in group:
            state = np.zeros(len(group))
            state[index[g]] = state[index[audit.right_swap(g, pair)]] = 1/np.sqrt(2)
            rho += np.outer(state, state)/len(group)
        rho_out = circuit @ np.kron(np.diag([1, 0]), rho) @ circuit.conj().T
        p_plus = np.trace(rho_out[:len(group), :len(group)])
        assert p_plus == pytest.approx(1 if pair == (0, 1) else 0.5)
        assert np.trace(rho_out) == pytest.approx(1)


@pytest.mark.parametrize("n", (3, 8, 16, 64, 1024, 10**6))
def test_information_floor_has_a_matched_classical_attack_not_a_speedup(n):
    c = audit.candidate_test_information(n)
    M = n*(n-1)//2
    lower = Fraction(c["mutual_information_lower_exact"])
    assert lower == Fraction(1, M)-Fraction(2, M*M) > 0
    assert float(lower) <= c["mutual_information_bits_numeric"] <= 1/M
    assert c["classical_candidate_enumeration_queries_upper"] == M+1
    assert c["controlled_public_word_swaps_Fredkin"] == (n-1).bit_length()
    assert not c["new_quantum_speedup"] and not c["hard_GI_ensemble_solved"]
    assert c["mode"] == "ANALYTIC_NOT_STATE_SIMULATION"


@pytest.mark.parametrize("copies", range(21))
def test_only_spin_half_has_catalan_dimensions(copies):
    from math import comb
    assert audit.commutant_dimension(1, copies) == comb(2*copies, copies)//(copies+1)
    for spin in (1, 2):
        mult = audit.su2_multiplicities(spin, copies)
        assert sum((j+1)*m for j, m in mult.items()) == (spin+1)**copies


def test_spin_one_counts_disprove_the_recorded_formula():
    assert audit.su2_multiplicities(2, 2) == {0: 1, 2: 1, 4: 1}
    assert audit.su2_multiplicities(2, 3) == {0: 1, 2: 3, 4: 2, 6: 1}
    assert audit.commutant_dimension(2, 2) == 3
    assert audit.commutant_dimension(2, 3) == 15
    assert audit.commutant_dimension(1, 2) == 2
    assert audit.commutant_dimension(1, 3) == 5


@pytest.mark.parametrize("spin,copies,dimension", ((2, 2, 3), (1, 3, 5)))
def test_independent_dense_commutator_nullspace(spin, copies, dimension):
    c = audit.dense_commutant_nullity(spin, copies)
    assert c["numerical_nullity"] == c["exact_recurrence_dimension"] == dimension
    assert c["smallest_nonzero_singular_value"] > 0.1


@pytest.mark.parametrize("copies", (2, 3, 4, 6))
def test_actual_invariant_bell_readout_uses_constant_gates(copies):
    c = audit.invariant_swap_control(copies)
    assert c["gate_count"] == 2 and c["Z_readouts"] == [0, 1]
    assert c["diagonalization_max_residual"] < 1e-12
    assert c["SU2_generator_commutator_max"] < 1e-12
    assert not c["arbitrary_optimal_HSP_measurement_compiled"]


@pytest.mark.parametrize("call", (
    lambda: audit.transposition_coset_control(8),
    lambda: audit.transposition_coset_control(True),
    lambda: audit.candidate_test_information(2),
    lambda: audit.su2_multiplicities(0, 2),
    lambda: audit.su2_multiplicities(1, -1),
    lambda: audit.collective_generators(2, 6),
    lambda: audit.dense_commutant_nullity(2, 3),
    lambda: audit.invariant_swap_control(20),
))
def test_allocation_and_parameter_gates(call):
    with pytest.raises(ValueError):
        call()


def isolated_registry(tmp_path, monkeypatch):
    originals = list(audit.reviewed_originals().values())
    active, archive = tmp_path/"active.json", tmp_path/"archive.json"
    active.write_text(json.dumps(originals+[{"id": "UNRELATED", "claim": "preserve"}]))
    archive.write_text("[]")
    monkeypatch.setattr(audit, "ACTIVE", active)
    monkeypatch.setattr(audit, "ARCHIVE", archive)
    return originals, active, archive


def test_quarantine_preserves_complete_hash_bound_originals_and_is_idempotent(tmp_path, monkeypatch):
    originals, active, archive = isolated_registry(tmp_path, monkeypatch)
    audit.quarantine_reviewed_negatives()
    saved = json.loads(archive.read_text())
    assert [r["original_record"] for r in saved] == originals
    assert all(r["original_sha256"] == audit.record_hash(r["original_record"]) for r in saved)
    assert all(r["reinstatement_requires_scoped_mathematical_review"] for r in saved)
    assert json.loads(active.read_text()) == [{"id": "UNRELATED", "claim": "preserve"}]
    before = active.read_bytes(), archive.read_bytes()
    audit.quarantine_reviewed_negatives()
    assert before == (active.read_bytes(), archive.read_bytes())


@pytest.mark.parametrize("quarantine_first", (False, True))
def test_changed_original_requires_independent_review(tmp_path, monkeypatch, quarantine_first):
    originals, active, archive = isolated_registry(tmp_path, monkeypatch)
    if quarantine_first:
        audit.quarantine_reviewed_negatives()
    active.write_text(json.dumps([originals[0] | {"claim": "changed"}, originals[1]]))
    before = active.read_bytes(), archive.read_bytes()
    with pytest.raises(ValueError, match="independent review"):
        audit.quarantine_reviewed_negatives()
    assert before == (active.read_bytes(), archive.read_bytes())


def test_concurrent_active_change_after_archival_is_not_overwritten(tmp_path, monkeypatch):
    originals, active, archive = isolated_registry(tmp_path, monkeypatch)
    import core.research_registry as registry
    write = registry._write_json

    def concurrent_write(path, payload):
        write(path, payload)
        if path == archive:
            active.write_text(json.dumps(originals+[{"id": "CONCURRENT"}]))

    monkeypatch.setattr(registry, "_write_json", concurrent_write)
    with pytest.raises(ValueError, match="after archival"):
        audit.quarantine_reviewed_negatives()
    assert json.loads(active.read_text())[-1]["id"] == "CONCURRENT"
    assert [r["original_record"] for r in json.loads(archive.read_text())] == originals


def test_duplicate_reviewed_record_is_not_silently_removed(tmp_path, monkeypatch):
    originals, active, archive = isolated_registry(tmp_path, monkeypatch)
    active.write_text(json.dumps(originals+[originals[0]]))
    before = active.read_bytes(), archive.read_bytes()
    with pytest.raises(ValueError, match="duplicate"):
        audit.quarantine_reviewed_negatives()
    assert before == (active.read_bytes(), archive.read_bytes())


def test_live_report_registry_and_site_exclude_only_reviewed_ids():
    active, archive = json.loads(audit.ACTIVE.read_text()), json.loads(audit.ARCHIVE.read_text())
    assert not set(audit.REVIEWED).intersection(r["id"] for r in active)
    assert set(audit.REVIEWED).issubset(r["id"] for r in archive)
    report = json.loads(audit.REPORT.read_text())
    assert report["producer_sha256"] == hashlib.sha256(Path(audit.__file__).read_bytes()).hexdigest()
    assert report["large_commutant_small_measurement"]["Catalan_dimension"] == 6564120420
    assert not report["speedup_claim_allowed"] and not report["general_nonabelian_HSP_solved"]
    assert report["reviewed_original_hashes"] == {k: v["sha256"] for k, v in audit.REVIEWED.items()}
    site = json.loads((audit.ROOT/"site/data/negatives.json").read_text())
    layout = json.loads((audit.ROOT/"site/data/negative_map.json").read_text())
    assert {r["id"] for r in site["records"]} == {r["id"] for r in active}
    assert {r["id"] for r in layout["points"]} == {r["id"] for r in active}
