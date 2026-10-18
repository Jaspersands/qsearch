from fractions import Fraction
from itertools import combinations
import json

import numpy as np
import pytest
from scipy.linalg import hadamard
from sympy import Rational

import campaign_negative_claim_audit as audit


def test_cubic_truncation_misclassifies_distillation_at_a_rational_input():
    c = audit.distillation_threshold_counter()
    p = Rational(c["input_error"])
    counts = c["accepted_error_weight_enumerator"]
    assert sum(counts) == 2**11
    assert counts[0] == counts[15] == 1
    assert counts[1] == counts[2] == 0
    assert counts[3] == 35
    accept = sum(v*p**w*(1-p)**(15-w) for w, v in enumerate(counts))
    wrong = sum(v*p**w*(1-p)**(15-w) for w, v in enumerate(counts) if w % 2)
    assert wrong/accept == Rational(c["exact_output_error"]) > p
    assert Rational(c["leading_cubic_output_proxy"]) == 35*p**3 < p
    # Independent MacWilliams evaluation at a second rational input.
    p = Rational(1, 10)
    v = 1-2*p
    accept = sum(a*p**w*(1-p)**(15-w) for w, a in enumerate(counts))
    wrong = sum(a*p**w*(1-p)**(15-w) for w, a in enumerate(counts) if w % 2)
    assert accept == (1+15*v**8)/16
    assert wrong/accept == (1+15*v**8-15*v**7-v**15)/(2*(1+15*v**8)) < p
    assert not c["hardware_noise_threshold_or_universal_distillation_lower_bound"]


def test_actual_steane_T7_changes_X_not_Z_stabilizers():
    c = audit.steane_stabilizer_counter()
    zero = np.zeros(128, complex)
    zero[c["simplex_codewords"]] = 1/np.sqrt(8)
    phase = np.array([np.exp(1j*np.pi*x.bit_count()/4) for x in range(128)])
    after = zero*phase
    g = c["X_stabilizer_mask"]
    perm = np.arange(128) ^ g
    Z = np.array([(-1)**((x & g).bit_count()) for x in range(128)])
    assert np.vdot(zero, zero[perm]) == pytest.approx(1)
    assert np.vdot(after, after[perm]) == pytest.approx(0.5)
    assert np.vdot(zero, Z*zero) == pytest.approx(1)
    assert np.vdot(after, Z*after) == pytest.approx(1)
    assert not c["T7_preserves_Steane_code"]
    assert not c["fixed_code_transversal_nonuniversality_is_retracted"]


@pytest.mark.parametrize("n", [2, 3, 4, 5])
def test_all_proper_GHZ_marginals_are_blind_but_joint_local_readout_is_perfect(n):
    c = audit.local_blindness_counter(n)
    plus, minus = np.zeros(2**n), np.zeros(2**n)
    plus[0] = plus[-1] = 1/np.sqrt(2)
    minus[0], minus[-1] = 1/np.sqrt(2), -1/np.sqrt(2)
    # Schmidt flattening gives every reduced operator without an assumed formula.
    for k in range(1, n):
        for keep in combinations(range(n), k):
            axes = keep + tuple(i for i in range(n) if i not in keep)
            a = plus.reshape([2]*n).transpose(axes).reshape(2**k, -1)
            b = minus.reshape([2]*n).transpose(axes).reshape(2**k, -1)
            assert np.allclose(a@a.T, b@b.T)
    H = hadamard(2**n)/np.sqrt(2**n)
    pp, pm = (H@plus)**2, (H@minus)**2
    even = np.array([x.bit_count() % 2 == 0 for x in range(2**n)])
    assert pp[even].sum() == pytest.approx(1)
    assert pm[~even].sum() == pytest.approx(1)
    assert c["physical_single_qubit_H_gates"] == n
    assert not c["proves_failure_of_ETH_for_a_local_chaotic_Hamiltonian"]


@pytest.mark.parametrize("n", [2, 4, 8])
def test_rare_events_need_inverse_gap_not_inverse_square_in_this_model(n):
    c = audit.rare_event_counter(n)
    delta = Fraction(c["Bernoulli_p1"])
    T = c["independent_samples_for_constant_success"]
    assert T*delta == 1
    assert 1-(1-delta)**T/2 > Fraction(4, 5)
    assert T == 2**n < c["misused_inverse_square_necessity"]
    assert not c["ETH_or_general_quantum_algorithm_refuted"]


def test_polylog_overhead_does_not_force_loss_of_asymptotic_quadratic_advantage():
    previous = 0
    for n in (16, 32, 64, 128, 256):
        c = audit.fault_tolerant_overhead_counter(n)
        ratio = Rational(c["classical_to_quantum_work_ratio"])
        assert ratio == Rational(c["classical_query_scale"], c["charged_quantum_work"])
        assert ratio > previous
        previous = ratio
        assert not c["all_physical_architectures_have_this_overhead"]
        assert not c["finite_hardware_crossover_certified"]


def test_quarantine_writer_preserves_originals_is_idempotent_and_keeps_unrelated_rows(tmp_path, monkeypatch):
    originals = [{"id": key, "claim": "original", "lesson": "historical"} for key in audit.REVIEWED_EXTENSIONS]
    safe = {"id": "UNREVIEWED-RECORD", "claim": "not blanket quarantined"}
    active, archive = tmp_path/"active.json", tmp_path/"archive.json"
    active.write_text(json.dumps(originals+[safe]))
    archive.write_text("[]")
    monkeypatch.setattr(audit, "ACTIVE", active)
    monkeypatch.setattr(audit, "ARCHIVE", archive)
    audit.quarantine_reviewed_extensions()
    assert json.loads(active.read_text()) == [safe]
    assert [r["original_record"] for r in json.loads(archive.read_text())] == originals
    snapshot = active.read_bytes(), archive.read_bytes()
    audit.quarantine_reviewed_extensions()
    assert snapshot == (active.read_bytes(), archive.read_bytes())
    # A changed record must not be silently deleted using the old review.
    active.write_text(json.dumps([safe, originals[0] | {"claim": "changed"}]))
    before = active.read_bytes()
    with pytest.raises(ValueError, match="changed"):
        audit.quarantine_reviewed_extensions()
    assert active.read_bytes() == before


def test_missing_original_causes_no_mutation(tmp_path, monkeypatch):
    active, archive = tmp_path/"active.json", tmp_path/"archive.json"
    active.write_text("[]")
    archive.write_text("[]")
    monkeypatch.setattr(audit, "ACTIVE", active)
    monkeypatch.setattr(audit, "ARCHIVE", archive)
    with pytest.raises(ValueError, match="missing"):
        audit.quarantine_reviewed_extensions()
    assert active.read_text() == archive.read_text() == "[]"


def test_live_extended_claims_are_not_active():
    active = json.loads(audit.ACTIVE.read_text())
    archive = json.loads(audit.ARCHIVE.read_text())
    assert not {r["id"] for r in active}.intersection(audit.REVIEWED_EXTENSIONS)
    for row in archive:
        if row["id"] in audit.REVIEWED_EXTENSIONS:
            assert row["retraction_reasons"] == audit.REVIEWED_EXTENSIONS[row["id"]]
            assert row["original_record"]["claim"]
            assert row["reinstatement_requires_scoped_mathematical_review"]


def test_report_does_not_promote_countercontrols_to_algorithms():
    r = audit.build_report()
    assert len(r["quarantined_ids"]) == 5
    assert len(r["primary_source_contradictions"]) == 5
    assert len(r["fault_tolerant_overhead_controls"]) == len(r["local_blindness_controls"]) == len(r["rare_event_controls"]) == 3
    assert not r["new_quantum_speedup_established"]
    assert not r["remaining_campaign_claims_verified"]
