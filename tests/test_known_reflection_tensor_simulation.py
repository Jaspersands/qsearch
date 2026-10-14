"""Known full-system closure, high-root precision, exact Born prefixes and aborts."""
from fractions import Fraction
from copy import deepcopy
from itertools import product
import json
import random
import subprocess

from flint import fmpq
import mpmath as mp
import numpy as np
import pytest

from theorems.known_reflection_tensor_simulation import (
    ONE, ZERO, REPORT, ROOT, TensorState, Term, diagonal_gate, fourier_gate,
    program_budget, qutrit_vector, root_entry, run_control,
    sample_basis, seed_tensor,
)
from known_preparation_coherent_reflection import dense_preparation, reflection_recipe
from ternary_noise_degradation import NoisyLinearRecord


def recipe(B=2, M=2, digits=2):
    q = 3**digits
    raw = tuple(NoisyLinearRecord((i % q,), (i*i+1) % q, q, f"tensor-source-{i}") for i in range(2*B*M))
    return reflection_recipe(raw, (1,), B, M)


def real(x): return mp.mpf(int(x.numerator))/int(x.denominator)


@pytest.mark.parametrize("digits", (1, 2, 16, 64))
@pytest.mark.parametrize("kind", ("zero", "tiny", "near_pi", "third", "large"))
def test_known_root_rational_entries_have_the_certified_precision_at_high_roots(digits, kind):
    q = 3**digits
    k = {"zero":0, "tiny":1, "near_pi":q//2, "third":q//3, "large":2*q//5}[kind]
    h = 24
    c, s = root_entry(q, k, h)
    with mp.workdps(100):
        truth = mp.exp(2j*mp.pi*k/q)
        assert abs(mp.mpc(real(c), real(s))-truth) <= mp.mpf(2)**(-h)/4
    for x in (c, s): assert int(x.denominator) & (int(x.denominator)-1) == 0


@pytest.mark.parametrize("digits", (1, 2, 16, 64))
def test_qutrit_approximation_and_Fourier_operator_are_inside_norm_budgets(digits):
    q, h = 3**digits, 24
    phases = (0, q//2, q//3+1)
    approximate = qutrit_vector(q, phases, h)
    with mp.workdps(100):
        total = sum(abs(mp.mpc(real(a), real(b))-mp.exp(2j*mp.pi*k/q)/mp.sqrt(3))**2 for (a, b), k in zip(approximate, phases))
        assert mp.sqrt(total) <= mp.mpf(2)**(-h)
    F = np.array([[complex(float(a), float(b)) for a, b in row] for row in fourier_gate(h)])
    truth = np.exp(2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
    assert np.linalg.norm(F-truth, 2) <= 3*2**(-h)


@pytest.mark.parametrize("B,M,T", ((1, 3, 4), (2, 2, 6), (4, 2, 3)))
def test_actual_tensor_program_matches_dense_quantum_law_and_linear_rank_closure(B, M, T):
    c = run_control(B, M, 2, T, 24, 84000+B*100+M)
    assert c["final_tensor_terms"] == B*(T+1)
    assert c["dense_quantum_law_TV_diagnostic"] <= float(fmpq(c["budget"]["logical_measurement_TV_upper"]))+1e-12
    assert [s["tensor_terms"] for s in c["program_history"]] == [B*(t+2) for t in range(T)]
    assert not c["hidden_secret_or_error_used"]
    assert c["largest_coefficient_denominator_exponent"] <= c["budget"]["coefficient_denominator_exponent_upper"]
    assert c["largest_factor_denominator_exponent"] <= c["budget"]["factor_denominator_exponent_upper"]


def test_wide_high_root_program_never_allocates_dense_state_or_root_field(monkeypatch):
    def prohibited(*args, **kwargs): raise AssertionError("full Hilbert diagnostic was called")
    monkeypatch.setattr(TensorState, "diagnostic_vector", prohibited)
    c = run_control(1, 24, 64, 2, 16, 84501)
    assert c["modulus"] == str(3**64)
    assert c["final_tensor_terms"] == 3
    assert not c["full_Hilbert_space_allocated"] and not c["scalable_path_builds_root_table"]
    assert c["final_computational_sample"]["status"] == "CERTIFIED_RATIONAL_POINT_SAMPLE"
    assert len(c["final_computational_sample"]["outcomes"]) == 25


def test_exact_tensor_norm_and_prefixes_match_independent_stdlib_rational_basis_expansion():
    seed = seed_tensor(recipe(), 12)
    state = seed.local_gate(1, fourier_gate(12)).full_system_reflection(seed, 2, 8)
    # Small independent exhaustive replay ONLY; the production algorithm is tensor.
    conv = lambda x: Fraction(int(x.numerator), int(x.denominator))
    cmul = lambda a, b: (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
    amplitudes = {}
    for word in product(*(range(d) for d in state.shape)):
        real_part, imaginary = Fraction(0), Fraction(0)
        for term in state.terms:
            value = tuple(map(conv, term.coefficient))
            for factor, outcome in zip(term.factors, word): value = cmul(value, tuple(map(conv, factor[outcome])))
            real_part += value[0]; imaginary += value[1]
        amplitudes[word] = real_part*real_part+imaginary*imaginary
    expected = sum(amplitudes.values())
    assert conv(state.norm_squared()) == expected
    for slot, d in enumerate(state.shape):
        for value in range(d):
            assert conv(state.project(slot, value).norm_squared()) == sum(p for word, p in amplitudes.items() if word[slot] == value)


def test_product_gates_preserve_rank_and_term_exhaustion_is_explicit():
    seed = seed_tensor(recipe(), 16)
    state = seed.local_gate(2, diagonal_gate(9, (0, 1, 2), 16))
    assert len(state.terms) == len(seed.terms) == 2
    with pytest.raises(ValueError, match="cap exhausted"): state.full_system_reflection(seed, 2, 3)
    other = seed_tensor(recipe(1, 3), 16)
    with pytest.raises(ValueError, match="full-system"): state.full_system_reflection(other, 1, 20)
    with pytest.raises(ValueError, match="couple"): state.local_gate(1, ((ONE,)*9,)*9)


@pytest.mark.parametrize("field", ("secret_or_errors_read_by_preparation", "ideal_unknown_state_inverse_supplied"))
def test_opaque_unknown_or_ideal_inverse_source_is_not_accepted_by_classical_seed_builder(field):
    r = recipe()
    r[field] = True
    with pytest.raises(ValueError, match="same-original-data"): seed_tensor(r, 16)


def test_seed_builder_rejects_guessed_phase_factors_without_original_data_receipts():
    r = recipe()
    phases = [[list(v) for v in cohort] for cohort in r["known_phase_numerators"]]
    phases[0][0][1] = (phases[0][0][1]+1) % 9
    r["known_phase_numerators"] = phases
    with pytest.raises(ValueError, match="actual original"): seed_tensor(r, 16)
    r = recipe()
    del r["source_receipts"]
    with pytest.raises(ValueError, match="original classical"): seed_tensor(r, 16)


class FixedCoin:
    def __init__(self, value): self.value = value
    def getrandbits(self, bits): return self.value


def test_every_coin_cell_of_a_finite_uniform_instrument_and_its_abort():
    state = TensorState((Term(ONE, ((ONE, ONE, ONE),)),), (3,))
    decisions = [sample_basis(state, FixedCoin(k), 1) for k in range(4)]
    assert [d["outcomes"] for d in decisions] == [(0,), (1,), (2,), None]
    assert decisions[-1]["status"] == "EXPLICIT_COIN_ATTEMPT_ABORT"
    assert decisions[0]["decisions"][0]["exact_branch_weights"] == ("1", "1", "1")


def test_zero_probability_outcomes_are_never_chosen_and_invalid_coins_rejected():
    state = TensorState((Term(ONE, ((ZERO, ONE, ONE),)),), (3,))
    assert sample_basis(state, FixedCoin(0), 2)["outcomes"] == (1,)
    for invalid in (-1, True, 2):
        with pytest.raises(ValueError, match="coin block"): sample_basis(state, FixedCoin(invalid), 2)
    zero_state = TensorState((Term(ZERO, ((ONE, ONE, ONE),)),), (3,))
    with pytest.raises(ValueError, match="nonzero"): sample_basis(zero_state, random.Random(1), 2)


def test_conditioning_on_whole_transcript_completion_can_bias_exact_rational_Born_law():
    state = TensorState((Term(ONE, ((ONE, ZERO), (ONE, ONE, ONE))),
                         Term(ONE, ((ZERO, ONE), (ONE, ZERO, ZERO)))), (2, 3))
    class ScriptCoins:
        def __init__(self, first, second): self.draws = iter((first, second))
        def getrandbits(self, bits): return 0 if bits == 0 else next(self.draws)
    completed, aborts = [], 0
    for first, second in product(range(4), repeat=2):
        out = sample_basis(state, ScriptCoins(first, second), 1)
        if out["outcomes"] is None: aborts += 1
        else: completed.append(out["outcomes"])
        assert not out["conditional_on_completion_is_exact_rational_program_law"]
    assert aborts == 3 and len(completed) == 13
    assert sum(word[0] == 0 for word in completed) == 9
    assert fmpq(9, 13) != fmpq(3, 4)


def test_non_dyadic_arithmetic_is_not_silently_admitted_to_the_weight_sampler():
    state = TensorState((Term((fmpq(1, 3), fmpq(0)), ((ONE, ONE, ONE),)),), (3,))
    with pytest.raises(ValueError, match="dyadic"): sample_basis(state, random.Random(1), 2)


@pytest.mark.parametrize("M,T,G", ((1, 0, 0), (4, 8, 16), (32, 3, 6), (100, 32, 64)))
def test_precision_refinement_and_complete_finite_abort_accounting(M, T, G):
    coarse, fine = [program_budget(2, M, T, G, h) for h in (16, 32)]
    assert fmpq(fine["logical_measurement_TV_upper"]) < fmpq(coarse["logical_measurement_TV_upper"])
    for b in (coarse, fine):
        assert b["max_tensor_terms"] == 2*(T+1)
        assert fmpq(b["unconditional_coin_abort_upper"]) <= fmpq(1, 2**b["sampling_failure_bits"])
        assert not b["subsystem_reflections_or_entangled_work_covered"]
        assert not b["quantum_only_unknown_source_covered"]
        assert not b["conditioning_away_coin_abort_allowed"]


def test_report_scope_controls_and_every_recorded_exact_coin_decision():
    report = json.loads(REPORT.read_text())
    assert report["status"] == "SCOPED_KNOWN_FULL_SYSTEM_REFLECTION_TENSOR_SIMULATION_REVIEW_PENDING"
    assert [c["final_tensor_terms"] for c in report["controls"]] == [5, 14, 8, 4]
    assert [c["full_Hilbert_space_allocated"] for c in report["controls"]] == [True, True, False, False]
    for c in report["controls"]:
        sample = c["final_computational_sample"]
        for d in sample["decisions"]:
            weights = [fmpq(x) for x in d["exact_branch_weights"]]
            scale = int(fmpq(d["integer_weight_scale"]))
            counts = [int(fmpq(x)) for x in d["integer_weights"]]
            assert weights == [fmpq(x, scale) for x in counts]
            total = int(fmpq(d["uniform_integer_total"]))
            assert total == sum(counts) > 0
            draws = [int(fmpq(x)) for x in d["coin_draws"]]
            assert all(0 <= x < 2**d["coin_bits_per_attempt"] for x in draws)
            assert all(x >= total for x in draws[:-1])
            value = d["selected_outcome"]
            assert sum(counts[:value]) <= draws[-1] < sum(counts[:value+1])
    assert not report["generic_quantum_classical_simulation_proved"]
    assert not report["opaque_HSP_inputs_dequantized"]
    assert not report["subsystem_reflection_programs_dequantized"]
    assert not report["accepted_speedup_candidate"]


def test_independent_ledger_checker_replays_all_sources_coins_and_scoped_budgets():
    result = subprocess.run(["node", str(ROOT/"research/certificates/known_reflection_tensor_simulation_crosscheck.js")], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "PASS" and report["exact_coin_transcripts"] == 4
    assert not report["complete_tensor_arithmetic_independently_reconstructed"]


@pytest.mark.parametrize("forgery", ("scope", "query_cost", "selected_coin"))
def test_independent_ledger_checker_rejects_forged_claims_costs_and_draws(forgery, tmp_path):
    report = json.loads(REPORT.read_text())
    exported = "run"
    if forgery == "scope": report["subsystem_reflection_programs_dequantized"] = True
    if forgery == "query_cost":
        report = deepcopy(report["controls"][0]["budget"])
        report["reflection_cap"] = 0
        exported = "budget"
    if forgery == "selected_coin":
        report = deepcopy(report["controls"][0])
        decision = report["final_computational_sample"]["decisions"][0]
        decision["coin_draws"][-1] = decision["uniform_integer_total"]
        exported = "coins"
    file = tmp_path/"forged.json"
    file.write_text(json.dumps(report))
    script = "const fs=require('fs'); const C=require(process.argv[1]); C[process.argv[3]](JSON.parse(fs.readFileSync(process.argv[2],'utf8')));"
    result = subprocess.run(["node", "-e", script, str(ROOT/"research/certificates/known_reflection_tensor_simulation_crosscheck.js"), str(file), exported], capture_output=True, text=True, timeout=120)
    assert result.returncode != 0
