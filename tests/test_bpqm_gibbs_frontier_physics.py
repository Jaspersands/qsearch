"""Physical channel checks and exact arithmetic, not just status-field tests."""
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random

import numpy as np
import pytest

from theorems.bpqm_gibbs_frontier import (
    MessageLaw, REPORT, XorIsing, cluster_step, combine, exact_cluster_kernel,
    exact_gibbs, point_channel, prange_rank_bound, run_controls, tree_frontier,
)


def state(c, bit):
    return np.array([np.sqrt(float((1+c)/2)), (-1)**bit*np.sqrt(float((1-c)/2))])


@pytest.mark.parametrize("a,b", [("0", "0"), ("0", "1"), ("1", "1"),
                                 ("1/4", "3/4"), ("1/2", "1/2"), ("7/8", "1/8")])
def test_parity_combining_matches_actual_two_qubit_density(a, b):
    a, b = Fraction(a), Fraction(b)
    # |x,y> -> |x xor y,y>, in the PSC Fourier basis.
    CNOT = np.zeros((4, 4))
    for x, y in product(range(2), repeat=2):
        CNOT[2*(x^y)+y, 2*x+y] = 1
    for u in (0, 1):
        density = np.zeros((4, 4))
        for x in (0, 1):
            psi = np.kron(state(a, x), state(b, x^u))
            density += np.outer(psi, psi)/2
        actual = CNOT@density@CNOT.T
        reconstructed = np.zeros((4, 4))
        for r, sign in enumerate((1, -1)):
            probability = (1+sign*a*b)/2
            if not probability:
                continue
            signed_c = (a+b)/(1+a*b) if r == 0 else (b-a)/(1-a*b)
            conditional = state(signed_c, u)
            reconstructed[2*r:2*r+2, 2*r:2*r+2] = float(probability)*np.outer(conditional, conditional)
        assert np.max(abs(actual-reconstructed)) < 1e-14


@pytest.mark.parametrize("kind", ["equality", "parity"])
def test_all_small_grid_pairs_preserve_probability_and_information_bounds(kind):
    G = 8
    for i, j in product(range(G+1), repeat=2):
        a, b = Fraction(i, G), Fraction(j, G)
        lo = combine(point_channel(a, G, 16), point_channel(b, G, 16), kind, direction="upgrade")
        hi = combine(point_channel(a, G, 16), point_channel(b, G, 16), kind, direction="degrade")
        # Exact unquantized mean overlap: ab for equality, max(a,b) for parity.
        true_fidelity = a*b if kind == "equality" else max(a, b)
        assert lo.fidelity <= true_fidelity <= hi.fidelity
        assert sum(lo.weights) == sum(hi.weights) == 1 << 16
        assert min(lo.weights+hi.weights) >= 0


def test_equality_compression_input_gram_is_product_not_sum():
    for a, b in product((Fraction(0), Fraction(1, 3), Fraction(3, 4), Fraction(1)), repeat=2):
        lhs = np.dot(np.kron(state(a, 0), state(b, 0)), np.kron(state(a, 1), state(b, 1)))
        assert lhs == pytest.approx(float(a*b), abs=1e-14)


def test_reading_internal_heralds_can_disturb_a_fixed_codeword_state():
    # Good root-bit statistics do not license measuring all intermediate flags.
    psi = np.kron(state(Fraction(1, 2), 0), state(Fraction(1, 2), 0))
    CNOT = np.zeros((4, 4))
    for x, y in product(range(2), repeat=2):
        CNOT[2*(x^y)+y, 2*x+y] = 1
    after = CNOT@psi
    density = np.outer(after, after)
    dephased = np.zeros((4, 4))
    dephased[:2, :2] = density[:2, :2]
    dephased[2:, 2:] = density[2:, 2:]
    assert np.trace(dephased@dephased) < .6
    assert np.abs(np.linalg.eigvalsh(density-dephased)).sum()/2 > .4
    assert np.linalg.norm(CNOT.T@after-psi) < 1e-14


@pytest.mark.parametrize("c", ["1/5", "1/2", "13/20", "4/5"])
def test_one_complete_tree_level_brackets_direct_helstrom_error(c):
    # Extrinsic (dv=3,dc=4) depth1: root and two independent triples, seven wires.
    c = Fraction(c)
    rho = [np.zeros((128, 128)) for _ in range(2)]
    counts = [0, 0]
    for word in product(range(2), repeat=7):
        if word[0]^word[1]^word[2]^word[3] or word[0]^word[4]^word[5]^word[6]:
            continue
        psi = np.array([1.])
        for bit in word:
            psi = np.kron(psi, state(c, bit))
        rho[word[0]] += np.outer(psi, psi)
        counts[word[0]] += 1
    actual_error = 0.5 - np.abs(np.linalg.eigvalsh(rho[0]/counts[0]-rho[1]/counts[1])).sum()/4
    result = tree_frontier(c, variable_degree=3, check_degree=4, grid=32, mass_bits=48, max_iterations=1)
    last = result["history"][-1]
    assert float(Fraction(last["symbol_error_lower"]))-1e-13 <= actual_error
    assert actual_error <= float(Fraction(last["symbol_error_upper"]))+1e-13
    assert last["distinct_original_tree_channel_outputs"] == 7


def test_finite_certificate_beyond_prange_keeps_physical_resource_costs():
    result = tree_frontier("13/20")
    last = result["history"][-1]
    assert result["tree_convergence_certificate"] is True
    assert Fraction(last["sufficient_contraction_factor_upper"]) < 1
    assert result["beyond_product_usd_prange_rank_ceiling"] is True
    assert last["distinct_original_tree_channel_outputs"] > 10**12
    assert result["finite_graph_block_decoder_executed"] is False
    assert result["coherent_circuit_compiled"] is False
    assert result["accepted_speedup_candidate"] is False


def test_budget_exhaustion_and_completely_uninformative_channel_are_not_success():
    for result in (tree_frontier("13/20", max_iterations=1), tree_frontier(1, max_iterations=3)):
        assert result["tree_convergence_certificate"] is False
        assert result["status"].startswith("UNKNOWN")
    assert Fraction(tree_frontier(1, max_iterations=1)["history"][0]["symbol_error_lower"]) == Fraction(1, 2)


def test_square_root_intervals_are_exact_at_endpoints():
    assert point_channel(0).error_interval() == (0, 0)
    assert point_channel(1).error_interval() == (Fraction(1, 2), Fraction(1, 2))
    for j in range(17):
        lo, hi = point_channel(Fraction(j, 16), grid=16).error_interval()
        assert 0 <= lo <= hi <= Fraction(1, 2)
        assert hi-lo <= Fraction(1, 1 << 80)


def test_prange_failure_bound_does_not_reject_cluster_or_all_classical_algorithms():
    record = prange_rank_bound("13/20", 4096)
    assert record["full_row_rank_proposal_probability_power_two_upper_exponent"] == 184
    assert record["all_classical_samplers_excluded"] is False
    assert record["rank_aware_cluster_sampler_is_covered_by_this_bound"] is False
    assert prange_rank_bound("1/3", 4096)["full_row_rank_proposal_probability_power_two_upper_exponent"] == 0


@pytest.mark.parametrize("model", [
    XorIsing(3, ((3, 0), (6, 1), (5, 0), (7, 1))),
    XorIsing(2, ((1, 0), (1, 1), (3, 0))),
    XorIsing(2, ((0, 0), (0, 1), (1, 1), (2, 0))),
])
def test_cluster_sampler_exact_detailed_balance_even_with_frustrated_dependencies(model):
    for c in (Fraction(0), Fraction(1, 2), Fraction(13, 20)):
        target, kernel = exact_cluster_kernel(model, c)
        assert target == exact_gibbs(model, c)
        assert all(sum(row) == 1 for row in kernel)
        assert all(target[x]*kernel[x][y] == target[y]*kernel[y][x]
                   for x in range(len(target)) for y in range(len(target)))
        assert tuple(sum(target[x]*kernel[x][y] for x in range(len(target)))
                     for y in range(len(target))) == target


def test_scalable_cluster_step_uses_no_probability_or_quantum_state_table(monkeypatch):
    import theorems.bpqm_gibbs_frontier as module
    def forbidden(*args, **kwargs):
        raise AssertionError("exponential calibration called in scalable sampler")
    monkeypatch.setattr(module, "exact_gibbs", forbidden)
    monkeypatch.setattr(module, "exact_cluster_kernel", forbidden)
    n = 96
    model = XorIsing(n, tuple((sum(1 << ((i+j) % n) for j in (0, 1, 5)), i % 2)
                             for i in range(2*n)))
    rng = random.Random(71)
    x = 0
    for _ in range(8):
        result = cluster_step(model, "13/20", x, rng)
        x = result["word"]
        assert 0 <= x < 1 << n
        assert result["selected_rank"] <= result["selected_count"]
        assert result["mixing_guarantee"] is False


def test_cluster_sampler_does_not_discard_dependent_satisfied_rows():
    class AllKept:
        def randrange(self, denominator):
            return 0
    result = cluster_step(XorIsing(2, ((1, 0), (1, 0))), "13/20", 0, AllKept())
    assert result["selected_count"] == 2
    assert result["selected_rank"] == 1
    assert result["dependent_rows_retained"] == 1


def test_reports_and_live_artifact_preserve_scope():
    rebuilt = run_controls()
    stored = json.loads(REPORT.read_text())
    assert stored == rebuilt
    module = Path(__file__).resolve().parents[1]/"theorems/bpqm_gibbs_frontier.py"
    assert rebuilt["source_sha256"] == hashlib.sha256(module.read_bytes()).hexdigest()
    assert rebuilt["new_quantum_algorithm_claimed"] is False
    assert rebuilt["classical_hardness_proved"] is False
    assert rebuilt["finite_graph_decoder_implemented"] is False


def test_invalid_laws_precision_and_parameters_fail_before_large_allocation():
    for c in (True, .5, "-1/2", "3/2"):
        with pytest.raises(ValueError):
            point_channel(c)
    for grid in (True, 3, -1, 10**12):
        with pytest.raises(ValueError):
            point_channel("1/2", grid=grid)
    with pytest.raises(ValueError):
        MessageLaw(4, 8, (1, 1, 1, 1, 1))
    with pytest.raises(ValueError):
        tree_frontier("1/2", variable_degree=2)
    with pytest.raises(ValueError):
        combine(point_channel("1/2"), point_channel("1/2", grid=64), "parity")
