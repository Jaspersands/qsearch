"""Literal source/gate tests; ideal reference recovery is not a speedup claim."""
import inspect
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from theorems.native_uniform_descent_receiver import (
    REPORT, DescentSource, OriginalSource, Packet, SourceExhausted, centre_element,
    digit_measurement, forward_fixture, merge_branch, receive, receiver_control,
    resource_contract, uniform_label_census,
)
from nil3_state_hsp_descent_receiver import SuppliedPhaseSample, conditional_phase_lift
from cyclotomic_rescaling_gate import multiply, pairing, plus, reduce_element, residue
from native_state_hsp_bridge import NativeGroup, ring_words
from ternary_cyclic_extractor import apply_cycle_basis


@pytest.mark.parametrize("level", (2, 3, 4))
@pytest.mark.parametrize("dimension", (1, 2))
@pytest.mark.parametrize("size", (2, 3, 4))
def test_every_branch_matches_literal_SUM_gates_and_full_ring_secret(level, dimension, size):
    G = NativeGroup(level, dimension)
    secret = G.vector(tuple((5+j, 2+j) for j in range(dimension)))
    # Prescribed labels here test a gate identity, never a cheap IID source.
    labels = [G.vector(tuple((i+1+j, i+2) for j in range(dimension))) for i in range(size-1)]
    labels.append(G.vector(tuple((-sum(residue(row[j]) for row in labels), 0) for j in range(dimension))))
    samples = [SuppliedPhaseSample(a, G.supplied_phase_state(a, secret), level) for a in labels]
    joint = np.ones(1, complex)
    for s in samples:
        joint = np.kron(joint, s.state)
    literal = apply_cycle_basis(joint, (1,)*size).reshape((3,)*size)
    total = 0.
    for tail in product(range(3), repeat=size-1):
        child, r = merge_branch(samples, tail)
        actual = literal[(slice(None),)+tail]
        probability = float(np.vdot(actual, actual).real)
        assert np.max(abs(child.state-actual/np.sqrt(probability))) < 1e-12
        assert abs(probability-r["branch_probability_diagnostic"]) < 1e-12
        assert abs(probability-3**(1-size)) < 1e-12
        lower = NativeGroup(level-1, dimension).vector(secret)
        expected = NativeGroup(level-1, dimension).supplied_phase_state(child.label, lower)
        # The actual unknown global phase must not be silently discarded.
        offset = [(0, 0)]*dimension
        for label, v in zip(labels, (0,)+tail):
            for j, a in enumerate(label):
                offset[j] = plus(offset[j], multiply(a, ((0, 0), (1, 0), (1, 1))[v], level), level)
        phase = sum(pairing(a, s, level) for a, s in zip(offset, secret)) % 1
        assert np.max(abs(child.state-np.exp(2j*np.pi*float(phase))*expected)) < 1e-12
        assert r["quantum_recipe"]["accepted_outcomes"] == "ALL"
        assert not r["secret_used_by_merge"]
        total += probability
    assert abs(total-1) < 1e-12


@pytest.mark.parametrize("level", (1, 2, 3, 4))
def test_actual_learned_prefix_makes_top_equations_for_every_scalar_secret(level):
    G = NativeGroup(level)
    for s, a in product(ring_words(level), repeat=2):
        lower = None if level == 1 else NativeGroup(level-1).vector((s,))
        sample = SuppliedPhaseSample((a,), G.supplied_phase_state((a,), (s,)), level)
        row, result = digit_measurement(sample, lower, np.random.default_rng(1))
        candidates = [u for u in range(3) if plus((0, 0) if lower is None else lower[0], multiply(centre_element(level), (u, 0), level), level) == s]
        assert len(candidates) == 1
        assert result == row[0]*candidates[0] % 3


def test_exact_conditioned_label_law_and_illegal_high_digit_selection_counterexample():
    for c in uniform_label_census():
        assert len(c["child_label_counts"]) == 3**(c["parent_level"]-1)
        assert len({r["count"] for r in c["child_label_counts"]}) == 1
    # Conditioning on a desired child, unlike coarse-only support selection,
    # changes the source into a point mass. Finite counts must not hide that.
    G = NativeGroup(3)
    zero = ((0, 0),)
    pairs = []
    for a, b in product(ring_words(3), repeat=2):
        if residue(a) == 1 and residue(b) == 2:
            samples = [SuppliedPhaseSample((v,), G.supplied_phase_state((v,), zero), 3) for v in (a, b)]
            child, _ = merge_branch(samples, (0,))
            if child.label == zero:
                pairs.append(child.label)
    assert pairs and len(set(pairs)) == 1  # Not nine equally likely labels.
    policy = inspect.getsource(DescentSource.take)
    assert "tuple(map(residue, packet.sample.label))" in policy
    assert "sample.state" not in policy and "secret" not in policy


@pytest.mark.parametrize("n,level", ((1, 2), (1, 3), (2, 3), (4, 3), (1, 4)))
@pytest.mark.parametrize("seed", (12, 33, 12045))
def test_source_driven_recursion_recovers_without_secret_or_free_ancestors(n, level, seed):
    c = receiver_control(n, level, seed)
    r = c["result"]
    assert r["recovered_native_secret"] == c["truth_fixture_only"]
    assert len(r["completed_digit_stages"]) == level
    assert r["original_inputs_supplied"] <= int(r["resource_contract"]["original_copy_upper"])
    accounted = r["measured_original_lineages"]+r["unconsumed_original_lineages"]
    assert sorted(accounted) == list(range(r["original_inputs_supplied"]))
    assert not r["receiver_takes_hidden_secret"] and not r["quantum_hardware_executed"]
    assert not r["new_quantum_speedup_established"]
    for stream in r["descent_streams"]:
        assert stream["selection_uses_only_coarse_residues"]
        assert not stream["child_state_prepared_from_secret"]
        assert len(stream["complete_output_records"]) == stream["outputs_emitted"]
    for fn in (receive, merge_branch, digit_measurement):
        assert "secret" not in inspect.signature(fn).parameters


def test_rank_deficient_source_does_not_guess_or_regenerate():
    sample = SuppliedPhaseSample(((0, 0),), np.ones(3)/np.sqrt(3), 3)
    source = OriginalSource(iter([sample]*200), 3, 1, 200)
    r = receive(source, np.random.default_rng(1))
    assert r["status"] == "NO_RECOVERY_FROM_FINITE_SUPPLIED_SOURCE"
    assert r["recovered_native_secret"] is None
    assert len(r["completed_digit_stages"]) == 1
    assert r["completed_digit_stages"][0]["recovered_top_digits"] is None
    assert r["original_inputs_supplied"] == 15
    assert source.count < source.cap


@pytest.mark.parametrize("supplied,cap", ((0, 10), (1, 10), (10, 1), (4, 10), (10, 4)))
def test_source_exhaustion_has_complete_accounting_even_inside_recursion(supplied, cap):
    samples = list(next(forward_fixture(3, ((2, 1),), j)) for j in range(supplied))
    source = OriginalSource(samples, 3, 1, cap)
    r = receive(source, np.random.default_rng(1))
    assert r["recovered_native_secret"] is None and r["source_exhaustion"]
    assert r["original_inputs_supplied"] == min(supplied, cap)
    assert sorted(r["measured_original_lineages"]+r["unconsumed_original_lineages"]) == list(range(source.count))


def test_reused_physical_ancestors_are_rejected():
    sample = SuppliedPhaseSample(((1, 0),), np.ones(3)/np.sqrt(3), 3)
    class BadSource:
        level, dimension, retain_trace = 3, 1, False
        def take(self):
            return Packet(sample, (0,))
    with pytest.raises(ValueError, match="overlapping physical"):
        DescentSource(BadSource(), np.random.default_rng(2)).take()


def test_large_branch_does_not_treat_float_underflow_as_impossible():
    sample = SuppliedPhaseSample(((0, 0),), np.ones(3)/np.sqrt(3), 3)
    child, r = merge_branch([sample]*1000, (0,)*999)
    assert np.max(abs(child.state-sample.state)) < 1e-12
    assert r["branch_probability_diagnostic"] == 0  # Diagnostic only.
    assert r["ideal_branch_probability"] == {"base": 3, "exponent": -999}


@pytest.mark.parametrize("n", (1, 4, 32, 128))
@pytest.mark.parametrize("level", (1, 2, 3, 4, 128))
def test_copy_and_rank_contracts_are_upper_bounds_not_hardness(n, level):
    r = resource_contract(n, level)
    W, K = (n+1)**2, n+8
    assert int(r["original_copy_upper"]) == K*sum(W**j for j in range(level))
    assert r["unknown_quantum_buffer_upper"] == (level-1)*W+level
    assert r["every_fixed_level_is_polynomial"] and not r["universal_copy_lower_bound"]
    assert not r["hardware_or_noise_error_included"]


def test_high_level_forward_fixture_uses_integer_not_float_or_int64_labels():
    s = next(forward_fixture(100, ((0, 0),), 13))
    assert s.level == 100 and max(s.label[0]) > 2**63
    assert np.max(abs(s.state-np.ones(3)/np.sqrt(3))) < 1e-12


@pytest.mark.parametrize("bad", ("level", "residue", "tail", "zero_branch", "lower", "source"))
def test_invalid_premises_are_not_silently_accepted(bad):
    sample = SuppliedPhaseSample(((1, 0),), np.ones(3)/np.sqrt(3), 3)
    with pytest.raises(ValueError):
        if bad == "level":
            conditional_phase_lift(SuppliedPhaseSample(((0, 0),), sample.state, 2), ((0, 0),))
        elif bad == "residue":
            merge_branch((sample,), ())
        elif bad == "tail":
            merge_branch((sample, sample, sample), (True, 0))
        elif bad == "zero_branch":
            sharp = SuppliedPhaseSample(((0, 0),), np.array([1, 0, 0]), 3)
            merge_branch((sharp, sharp), (1,))
        elif bad == "lower":
            digit_measurement(sample, ((8, 0),), np.random.default_rng(1))
        else:
            OriginalSource((sample,), 2, 1, 1).take()


def test_independent_full_trace_checker():
    checker = REPORT.parents[1]/"certificates/native_uniform_descent_crosscheck.js"
    out = subprocess.run(["node", str(checker)], capture_output=True, text=True, check=True)
    r = json.loads(out.stdout)
    assert r["status"] == "PASS" and r["source_driven_recoveries"] == 5
    assert r["complete_merge_replays"] > 30
    assert not r["new_quantum_speedup_established"]


@pytest.mark.parametrize("mutation", ("label", "branch", "lineage", "phase", "prefix", "row", "digit", "source", "cap", "claim", "census"))
def test_checker_rejects_forged_source_descent_recovery_and_claims(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    c = r["source_driven_receiver_controls"][1]["result"]
    b = next(b for b in c["descent_streams"][0]["complete_output_records"] if len(b["public_input_labels"]) > 1)
    if mutation == "label":
        b["child_label"][0][0] += 1
    elif mutation == "branch":
        b["measured_complement"][0] = (b["measured_complement"][0]+1) % 3
    elif mutation == "lineage":
        b["input_original_lineages"][0][0] = b["input_original_lineages"][1][0]
    elif mutation == "phase":
        b["retained_amplitudes"][0][0] += .1
    elif mutation == "prefix":
        c["completed_digit_stages"][1]["learned_lower"][0][0] += 1
    elif mutation == "row":
        c["completed_digit_stages"][0]["public_rows"][0][0] ^= 1
    elif mutation == "digit":
        c["completed_digit_stages"][0]["recovered_top_digits"][0] ^= 1
    elif mutation == "source":
        c["complete_original_input_records"][0]["supplied_amplitudes"][0][0] += .1
    elif mutation == "cap":
        c["resource_contract"]["original_copy_upper"] = "1"
    elif mutation == "claim":
        r["accepted_speedup_candidate"] = True
    else:
        r["conditional_uniform_label_censuses"][0]["child_label_counts"][0]["count"] += 1
    for stream in c["descent_streams"]:
        stream["first_output_records"] = stream["complete_output_records"][:8]
    target = tmp_path/"forged.json"
    target.write_text(json.dumps(r))
    checker = REPORT.parents[1]/"certificates/native_uniform_descent_crosscheck.js"
    out = subprocess.run(["node", str(checker), str(target)], capture_output=True, text=True)
    assert out.returncode != 0
