from copy import deepcopy
from fractions import Fraction
from itertools import product
from math import comb
import json
import subprocess

import numpy as np
import pytest

from theorems import native_syndrome_dilation as A


def stored():
    return json.loads(A.REPORT.read_text())


def workbench(index=0):
    control = stored()["actual_source_controls"][index]
    base = control["native_source_reference"]
    records = tuple(A.NoisyLinearRecord(tuple(r["label"]), r["value"], r["modulus"], r["source_id"]) for r in base["original_records"])
    return A.SyndromeDilation(records, base["known_mask"])


def node_check(payload):
    return subprocess.run([
        "node", "-e",
        "const A=require('./research/certificates/native_syndrome_dilation_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>console.log(JSON.stringify(A.verify(JSON.parse(s)))));",
    ], input=json.dumps(payload), text=True, capture_output=True, cwd=A.ROOT)


def test_literal_shift_is_unitary_and_invertible_on_every_joint_entry():
    work = workbench()
    state = np.arange(work.D * work.N).reshape(work.D, work.N) + 1j
    assert work.translate(work.translate(state), inverse=True) == pytest.approx(state)
    assert np.linalg.norm(work.translate(state)) == pytest.approx(np.linalg.norm(state))


def test_actual_small_Hamiltonian_has_declared_complete_spectrum_and_gap():
    work = workbench()
    size = work.D * work.N
    # Independent bounded matrix check; production never allocates this matrix.
    H = np.column_stack([work.hamiltonian(v.reshape(work.D, work.N)).ravel() for v in np.eye(size)])
    assert H == pytest.approx(H.conj().T, abs=1e-12)
    spectrum = np.linalg.eigvalsh(H)
    expected = [k for k in range(work.M + 1) for _ in range(comb(work.M, k) * 2 ** k * work.N)]
    assert spectrum == pytest.approx(expected, abs=1e-10)
    assert spectrum[-1] == pytest.approx(work.M)
    assert min(x for x in spectrum if x > 1e-8) == pytest.approx(1)
    assert min(x for x in spectrum / work.M if x > 1e-8) == pytest.approx(1 / work.M)


@pytest.mark.parametrize("lam", (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(99, 100)))
def test_rank_one_driver_path_active_and_full_gaps_are_distinct(lam):
    work = workbench()
    size = work.D * work.N
    projector = np.column_stack([work.ground(v.reshape(work.D, work.N)).ravel() for v in np.eye(size)])
    initial = np.outer(work.psi, work.public_ancillas()[0][1]).ravel()
    p = np.vdot(initial, projector @ initial).real
    driver = np.eye(size) - np.outer(initial, initial.conj())
    target = np.eye(size) - projector
    H = (1 - float(lam)) * driver + float(lam) * target
    active_gap = np.sqrt(1 - 4 * float(lam) * (1 - float(lam)) * (1 - p))
    expected = sorted([(1 - active_gap) / 2, (1 + active_gap) / 2]
                      + [1 - float(lam)] * (work.N - 1) + [1] * (size - work.N - 1))
    eigs = np.linalg.eigvalsh(H)
    assert eigs == pytest.approx(expected, abs=1e-10)
    if lam == Fraction(1, 2):
        assert active_gap ** 2 == pytest.approx(p)
        assert eigs[1] - eigs[0] == pytest.approx(active_gap / 2)


@pytest.mark.parametrize("index", range(4))
def test_ground_projector_and_complete_classical_readout_are_literal(index):
    work = workbench(index)
    for kind, ancilla, weights, _ in work.public_ancillas():
        initial = np.outer(work.psi, ancilla)
        projected = work.ground(initial)
        assert work.ground(projected) == pytest.approx(projected, abs=1e-11)
        assert np.linalg.norm(work.hamiltonian(projected)) < 1e-10
        quantum = abs(work.readout(initial)) ** 2
        classical = work.classical_readout_law(weights)
        assert quantum.sum() == pytest.approx(1)
        assert classical.sum() == pytest.approx(1)
        assert quantum == pytest.approx(classical, abs=1e-11)
        mass = np.vdot(projected, projected).real
        assert mass == pytest.approx(quantum[0].sum(), abs=1e-11)
        E = work.compressed_effect(weights)
        assert mass == pytest.approx(np.vdot(work.psi, E @ work.psi).real, abs=1e-11)
        assert np.trace(E).real / work.D == pytest.approx(1 / work.D)


def test_zero_syndrome_compression_is_raw_Gram_not_normalized_span():
    work = workbench(1)
    _, _, weights, _ = work.public_ancillas()[0]
    E = work.compressed_effect(weights)
    K = np.asarray([[int(a["frequency"] == b["frequency"]) / work.D for b in work.rows] for a in work.rows])
    assert E == pytest.approx(K, abs=1e-12)
    assert not np.allclose(E @ E, E)


def test_noncommuting_public_sector_exists_but_does_not_improve_secret_average():
    c = stored()["actual_source_controls"][2]
    work = workbench(2)
    K = work.compressed_effect(work.public_ancillas()[0][2])
    sector_case = c["public_ancilla_experiments"][1]
    witness = sector_case["exact_noncommutation_witness"]
    assert witness is not None
    assert Fraction(witness["commutator_root_of_unity_prefactor"]) != 0
    E = work.compressed_effect(work.public_ancillas()[1][2])
    i, j = witness["word_indices"]
    value = (K @ E - E @ K)[i, j]
    expected = complex(Fraction(witness["commutator_root_of_unity_prefactor"])) * np.exp(2j * np.pi * witness["commutator_phase_exponent"] / work.q)
    assert value == pytest.approx(expected, abs=1e-12)
    assert np.linalg.norm(K @ E - E @ K) > 1e-5
    raw_mean = c["native_source_reference"]["spectral_filter_controls"][0]["diagnostic_source_acceptance_probability"]
    for e in c["public_ancilla_experiments"]:
        assert np.mean(e["complete_uniform_secret_sweep_ground_probabilities"]) == pytest.approx(raw_mean)


def test_uniform_secret_average_for_arbitrary_public_mixed_work_weights():
    work = workbench(2)
    weights = tuple(Fraction(j + 1, work.N * (work.N + 1) // 2) for j in range(work.N))
    E = work.compressed_effect(weights)
    errors = stored()["actual_source_controls"][2]["truth_ONLY_FOR_SOURCE_SWEEP_CALIBRATION"]["original_errors"]
    phases = [sum(b * e for j, t in enumerate(row["word"])
                  for b, e in zip(((1, 0), (-1, 1), (0, -1))[t], errors[2 * j:2 * j + 2])) for row in work.rows]
    family = np.exp(2j * np.pi * np.asarray(phases)[:, None] / work.q) * work.phi
    mean = np.mean([np.vdot(family[:, j], E @ family[:, j]).real for j in range(work.N)])
    assert mean == pytest.approx(work.base["spectral_filter_controls"][0]["diagnostic_source_acceptance_probability"], abs=1e-11)


def test_primitive_secret_conditioning_uses_mass_not_an_additive_TV_loss():
    for c in stored()["actual_source_controls"]:
        base = c["native_source_reference"]
        q, n = base["original_records"][0]["modulus"], len(base["known_mask"])
        space = tuple(product(range(q), repeat=n))
        indices = [j for j, s in enumerate(space) if any((x - z) % 3 for x, z in zip(s, base["known_mask"]))]
        assert len(indices) == q ** n * (1 - Fraction(1, 3 ** n))
        raw_mean = base["spectral_filter_controls"][0]["diagnostic_source_acceptance_probability"]
        for e in c["public_ancilla_experiments"]:
            primitive_mean = np.mean([e["complete_uniform_secret_sweep_ground_probabilities"][j] for j in indices])
            assert primitive_mean <= raw_mean / float(1 - Fraction(1, 3 ** n)) + 1e-10


def test_response_adaptive_mask_is_paid_classical_counterexample_not_a_new_speedup():
    c = stored()["response_adaptive_mask_countercontrol"]
    assert not c["public_noiseless_decoder"]["truth_supplied_to_decoder"]
    assert c["public_noiseless_decoder"]["original_equations_checked"] == 8
    assert c["word_phase_preparation_is_uniform_AFTER_paid_classical_mask"]
    assert c["diagnostic_ground_probability_after_paid_classical_mask"] == pytest.approx(1)
    assert not c["general_label_only_ancilla_average_bound_with_response_adaptive_mask_applies"]
    assert c["zero_computational_work_raw_Gram_mask_invariance_is_not_falsified"]


def test_population_ledger_charges_norm_overlap_primitive_conditioning_and_access_scope():
    for p in stored()["scaling_dilation_ledgers"]:
        assert p["exact_unnormalized_Hamiltonian_gap"] == "1"
        assert Fraction(p["exact_norm1_Hamiltonian_gap"]) == Fraction(1, p["word_sites"])
        assert int(p["necessary_standard_amplification_iterations_lower_FULL_uniform_secret"]) > 10 ** 14
        assert Fraction(p["uniform_primitive_secret_mean_ground_acceptance_upper"]["coefficient"]) > Fraction(p["uniform_secret_mean_ground_acceptance_upper"]["coefficient"])
        assert not p["per_secret_success_upper_or_universal_quantum_lower_bound_claimed"]
        assert p["inverse_for_arbitrary_mixed_ancilla_preparation_is_not_granted"]


@pytest.mark.parametrize("call", (
    lambda: workbench().compressed_effect(("1",)),
    lambda: workbench().compressed_effect(("-1", "1", "1")),
    lambda: A.dilation_ledger(129, 129, 12),
    lambda: A.dilation_ledger(8, 8, 12, "0"),
    lambda: workbench().translate(np.zeros((1, 1))),
))
def test_scope_and_whole_reference_validation(call):
    with pytest.raises(ValueError):
        call()


def test_independent_checker_replays_exact_access_scope_and_all_readouts():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["verified"]


@pytest.mark.parametrize("kind", (
    "overlap", "secret-mean", "sector-weights", "witness", "mass", "gap", "norm-gap", "classical-law",
    "primitive-factor", "amplification-price", "adaptive-mask", "mixed-inverse", "general-no-go", "speedup", "hash",
))
def test_independent_checker_rejects_scope_probability_and_resource_tampering(kind):
    p = deepcopy(stored())
    c, ledger = p["actual_source_controls"][2], p["scaling_dilation_ledgers"][0]
    e = c["public_ancilla_experiments"][1]
    if kind == "overlap":
        e["exact_original_data_ground_probability_root_polynomial"] = []
    elif kind == "secret-mean":
        e["exact_uniform_secret_mean_root_polynomial"] = ["1"]
    elif kind == "sector-weights":
        e["exact_syndrome_Fourier_weights"] = ["1"] * 9
    elif kind == "witness":
        e["exact_noncommutation_witness"]["commutator_root_of_unity_prefactor"] = "0"
    elif kind == "mass":
        e["diagnostic_entire_readout_mass"] = .5
    elif kind == "gap":
        c["exact_unnormalized_Hamiltonian_gap"] = "2"
    elif kind == "norm-gap":
        c["exact_norm1_Hamiltonian_gap"] = "1"
    elif kind == "classical-law":
        e["diagnostic_complete_measured_law_max_error_against_classical"] = .1
    elif kind == "primitive-factor":
        ledger["uniform_primitive_secret_mean_ground_acceptance_upper"]["coefficient"] = "1"
    elif kind == "amplification-price":
        ledger["necessary_standard_amplification_iterations_lower_FULL_uniform_secret"] = "1"
    elif kind == "adaptive-mask":
        p["response_adaptive_mask_countercontrol"]["general_label_only_ancilla_average_bound_with_response_adaptive_mask_applies"] = True
    elif kind == "mixed-inverse":
        ledger["inverse_for_arbitrary_mixed_ancilla_preparation_is_not_granted"] = False
    elif kind == "general-no-go":
        ledger["per_secret_success_upper_or_universal_quantum_lower_bound_claimed"] = True
    elif kind == "speedup":
        p["accepted_speedup_candidate"] = True
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
