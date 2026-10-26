from collections import defaultdict
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import isqrt, sqrt
from pathlib import Path

import numpy as np
import pytest

from theorems import ternary_bpqm_certificate as audit
from theorems import ternary_coloring_bpqm as physical


@pytest.mark.parametrize("grid", (6, 12, 24))
def test_every_rational_simplex_cell_has_an_exact_nonnegative_Gram_split(grid):
    for n in (1, 2, 7, 13):
        for a in range(n+1):
            for b in range(n-a+1):
                original = (a, b, n-a-b)
                parts = audit.simplex_parts(original, n, grid)
                assert 1 <= len(parts) <= 3
                assert sum(w for _, w in parts) == n
                for j in range(3):
                    assert sum(mu[j]*w for mu, w in parts) == grid*original[j]
                assert all(min(mu) >= 0 and sum(mu) == grid for mu, _ in parts)


@pytest.mark.parametrize("mu", (physical.PHYSICAL, (Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)),
                                  (0, Fraction(1, 7), Fraction(6, 7)), (Fraction(1, 3),)*3, (1, 0, 0)))
def test_actual_flag_isometry_and_dephased_blocks_implement_the_comparison_channel(mu):
    record = audit.degradation_control(mu)
    assert record["actual_isometry_amplitude_and_block_max_residual"] < 1e-12
    assert record["flag_dephasing_is_an_intentional_comparison_channel"]
    # Independent discrimination calculation: splitting must NOT improve the
    # channel. This check catches reversing the comparison direction.
    original_error = 1-sum(sqrt(float(x)) for x in mu)**2/3
    degraded_error = sum(Fraction(row["probability_exact"])*
                         (1-sum(sqrt(x/24) for x in row["target"])**2/3) for row in record["split"])
    assert degraded_error >= original_error-1e-12


@pytest.mark.parametrize("kind", ("bit", "check"))
def test_integer_transition_matches_independent_rational_physical_node_law(kind):
    G = 6
    channels = [(0, 3, 3), (2, 2, 2), (0, 0, 6), (1, 2, 3), (1, 4, 1)]
    for a, b in product(channels, repeat=2):
        mu, nu = tuple(Fraction(x, G) for x in a), tuple(Fraction(x, G) for x in b)
        branches = [(0, Fraction(1), physical.bit_spectrum(mu, nu))] if kind == "bit" else physical.check_branches(mu, nu)
        independent = defaultdict(Fraction)
        for _, probability, output in branches:
            denominator = np.lcm.reduce([x.denominator for x in output]).item()
            pieces = audit.simplex_parts(tuple(int(x*denominator) for x in output), denominator, G)
            for target, weight in pieces:
                independent[audit.canonical(target)] += probability*Fraction(weight, denominator)
        actual = {mu: Fraction(weight, G*G) for mu, weight in audit.transitions(G, a, b, kind)}
        assert actual == independent
        assert sum(actual.values()) == 1


def test_coefficient_inversion_is_public_uniform_F3_star_not_a_fixed_source_change():
    law = audit.point((Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)), grid=6)
    result = audit.coefficient_law(law)
    assert dict(result.weights) == {(1, 2, 3): 1 << 79, (1, 3, 2): 1 << 79}
    assert sum(w for _, w in result.weights) == 1 << result.bits


def test_mass_rounding_is_normalized_and_only_loses_information():
    law = audit.point((Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)), grid=6, bits=16)
    costs = {"message_pair_visits": 0, "rounding_loss_mass_units_total": 0}
    combined = audit.combine(law, law, "check", costs)
    assert sum(w for _, w in combined.weights) == 1 << 16
    assert costs["rounding_loss_mass_units_total"] > 0
    uninformative = audit.canonical((6, 0, 0))
    assert dict(combined.weights)[uninformative] >= costs["rounding_loss_mass_units_total"]


def test_outward_fidelity_bounds_agree_with_the_actual_complex_Gram():
    law = audit.point((Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)))
    lower, upper = law.fidelity_bounds()
    direct = 0.
    for mu, weight in law.weights:
        channel = tuple(Fraction(n, law.grid) for n in mu)
        psi0, psi1 = physical.state(channel, 0), physical.state(channel, 1)
        direct += weight*abs(np.vdot(psi0, psi1))/(1 << law.bits)
    assert float(lower)-1e-14 <= direct <= float(upper)+1e-14
    assert upper-lower <= Fraction(1, 1 << 80)


def test_tail_certificate_is_the_published_polynomial_not_a_fit():
    assert not audit.tail_certificate(Fraction(1, 2), 3, 6)["certified"]
    result = audit.tail_certificate(Fraction(1, 100), 3, 6)
    slope = ((1+Fraction(2, 100))**5-1)/Fraction(1, 100)
    assert Fraction(result["lambda_upper_exact"]) == Fraction(1, 2)*slope*slope/100
    assert result["certified"] and not result["finite_block_error_inferred"]


def test_signed_trine_reaches_a_certified_tail_without_population_sampling():
    result = audit.frontier(grid=24)
    assert result["certificate"]["level"] == 13
    assert Fraction(result["certificate"]["f_upper_exact"]) < Fraction(1, 100)
    assert Fraction(result["certificate"]["lambda_upper_exact"]) < 1
    assert all(row["probability_mass_exact"] == "1" for row in result["history"])
    assert not result["finite_block_decoder_executed"]
    assert not result["sampler_or_search_reduction_executed"]
    assert not result["speedup_claim_allowed"] and not result["accepted_speedup_candidate"]
    # Independent exact first level: five trines at a check yield a trine
    # with probability 1/16, otherwise a point spectrum. Two independent
    # checks and the physical root give (1/2)*(31/32)^2.
    assert Fraction(result["history"][0]["mean_fidelity_upper_exact"]) == Fraction(961, 2048)


def test_same_rate_does_not_automatically_give_a_certificate_and_caps_mean_unknown():
    result = audit.frontier(dv=4, dc=8, grid=12, iterations=12)
    assert result["certificate"] is None
    assert result["status"].startswith("UNKNOWN")
    short = audit.frontier(iterations=2)
    assert short["certificate"] is None and short["status"].startswith("UNKNOWN")


@pytest.mark.parametrize("spins,seed", ((4, 1), (8, 2), (16, 711)))
def test_classical_baseline_uses_all_original_signed_sockets_and_offsets(spins, seed):
    pytest.importorskip("z3")
    record = audit.native_constraint_control(spins, seed)
    assert len(record["sockets"]) == 6*spins
    Ht = [[0]*spins for _ in range(2*spins)]
    for edge, check, a in record["sockets"]:
        Ht[edge][check] = (Ht[edge][check]+a) % 3
    assert list(map(tuple, Ht)) == record["forms_H_transpose"]
    assert not record["source_conditioned_on_satisfiability"]
    assert not record["parallel_sockets_or_zero_forms_removed"]
    if record["status"] == "CLASSICAL_ORIGINAL_CSP_WITNESS":
        assert all((sum(a*x for a, x in zip(row, record["witness"]))+j) % 3
                   for row, j in zip(Ht, record["original_offsets"]))
    assert not record["classical_uniform_sampling_established"]
    assert not record["quantum_sampler_executed"]


def test_exclusion_measurement_bound_is_not_misrepresented_as_a_classical_CSP_bound():
    from math import log2
    record = audit.exclusion_readout_control()
    assert record["physical_effects_and_probabilities_residual"] < 1e-12
    assert record["probability_matrix_exact"] == [["0", "1/2", "1/2"], ["1/2", "0", "1/2"], ["1/2", "1/2", "0"]]
    assert record["capacity_bits_NUMERICAL_DISPLAY_ONLY"] < log2(3)/2
    assert not record["other_readouts_or_classical_CSP_algorithms_excluded"]
    assert not record["classical_uniform_sampling_lower_bound_claimed"]


@pytest.mark.parametrize("call", (
    lambda: audit.point(physical.PHYSICAL, grid=7),
    lambda: audit.point((0., .5, .5)),
    lambda: audit.Law(6, 16, (((0, 3, 3), 1),)),
    lambda: audit.simplex_parts((1, 1, 1), 2, 6),
    lambda: audit.frontier(dv=2), lambda: audit.tail_certificate(Fraction(-1), 3, 6),
))
def test_invalid_model_inputs_are_not_promoted(call):
    with pytest.raises(ValueError):
        call()


def test_live_report_binds_actual_producer_and_preserves_unresolved_obligations():
    report = json.loads(audit.REPORT.read_text())
    for path, digest in report["source_sha256"].items():
        assert digest == hashlib.sha256((audit.ROOT/path).read_bytes()).hexdigest()
    assert not report["local_derivation_independently_reviewed"]
    assert report["result"]["certificate"]["certified"]
    assert not report["result"]["accepted_speedup_candidate"]
    assert len(report["actual_physical_degradation_controls"]) == 4
    assert len(report["classical_original_dual_CSP_controls"]) == 2
