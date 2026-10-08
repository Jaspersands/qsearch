from collections import Counter
from fractions import Fraction
from itertools import product
import json
import math
import subprocess

import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates
from ternary_carry_packets import compile_packet
from ternary_packet_pauli_gate import (
    DERIVATION, REPORT, conditional_census, distance_control, kernel_frame,
    population_envelope, probe_record,
)


def packet(low=(1, 1, 0), level=3):
    unit = (-1)**((level-1)//2+1)
    return compile_packet([[inverse_frequency_coordinates(unit*a % 3, (2*unit*a) % 3, level)] for a in low], level)


@pytest.mark.parametrize("low,w,expected", [((1,1,1),(0,0),"1/9"), ((1,1,0),(0,0),"1/3"), ((1,1,0),(0,1),"0")])
def test_complete_actual_native_high_lifts_give_exact_character_moments(low, w, expected):
    result = conditional_census(low, (1,0), w, (1,))
    assert result["complete_high_lift_assignments"] == 729
    assert result["logical_words_per_lift"] == 9
    a, b, c = result["exact_character_difference_histogram"]
    assert b == c
    assert Fraction(a-c, result["character_average_denominator"]) == Fraction(expected)
    assert result["exact_squared_overlap_mean"] == expected
    assert not result["identical_packet_factory_supplied"]
    if expected == "0":
        assert result["maximum_single_lift_overlap_magnitude"] < 1e-12


def test_physical_support_weight_is_not_the_signal_exponent():
    first = probe_record(packet((1,1,1)), (1,0), (0,0))
    second = probe_record(packet((1,1,0)), (1,0), (0,0))
    assert len(first["translated_physical_support"]) == len(second["translated_physical_support"]) == 2
    assert first["restricted_kernel_frame_rank"] == 2
    assert second["restricted_kernel_frame_rank"] == 1
    assert first["conditional_high_lift_squared_overlap_mean"] != second["conditional_high_lift_squared_overlap_mean"]


@pytest.mark.parametrize("level", [3,5,7,11])
def test_kernel_geometry_and_scope_do_not_depend_on_high_phase_depth(level):
    p = packet(level=level)
    assert kernel_frame(p) == ((2,0),(1,0),(0,1))
    record = probe_record(p, (1,0), (0,0))
    assert record["conditional_high_lift_squared_overlap_mean"] == "1/3"
    assert not record["probe_choice_low_only_policy_verified_by_this_function"]
    assert not record["general_collective_receiver_or_high_informed_search_excluded"]


@pytest.mark.parametrize("qp,s", [(3,1),(3,2),(9,1),(9,3),(9,6),(27,3),(27,9),(27,18)])
def test_local_transition_character_orthogonality_including_nonprimitive_secrets(qp,s):
    basis = ((0,0),(1,0),(0,1))
    for v in (1,2):
        transitions = [tuple(a-b for a,b in zip(basis[(t+v)%3],basis[t])) for t in range(3)]
        for t, u in product(range(3), repeat=2):
            a,b = (x-y for x,y in zip(transitions[t],transitions[u]))
            histogram = Counter((s*(a*x+b*y)) % qp for x,y in product(range(qp), repeat=2))
            if t == u:
                assert histogram == {0:qp*qp}
            else:
                g = math.gcd(s,qp)
                assert set(histogram) == set(range(0,qp,g))
                assert len(set(histogram.values())) == 1


def test_every_small_low_source_and_every_kernel_direction_obey_dual_projection_bound():
    for low in product(range(3), repeat=3):
        result = distance_control(packet(low))
        assert result["exact_minimum_translation_rank"] >= result["all_nonzero_translation_rank_lower_bound"]
        assert not result["distance_enumeration_is_scalable_algorithm"]


@pytest.mark.parametrize("n", [32,64,128,256,1024])
def test_exact_unconditioned_primal_dual_and_polynomial_menu_ledgers(n):
    d, K = n//8, 2*n
    result = population_envelope(n,K,d,n*n)
    U = sum(math.comb(K,w)*2**(w-1) for w in range(1,d))
    assert Fraction(result["primal_distance_failure_union_bound"]) == Fraction(U,3**n)
    assert Fraction(result["dual_distance_failure_union_bound"]) == Fraction((3**n-1)*U,3**K)
    raw = Fraction(result["raw_population_menu_squared_overlap_mean_upper"])
    assert 0 < raw <= 1
    if n < 128: assert raw == 1
    else: assert raw < 1
    assert Fraction(result["one_Pauli_test_mean_total_variation_to_unbiased_upper_squared"]) == raw/4
    assert not result["full_row_rank_conditioning_assumed"]
    assert not result["implicit_high_informed_exponential_probe_families_covered"]
    assert not result["multiple_noncommuting_measurements_on_same_packet_covered"]
    if n == 1024: assert raw < Fraction(1,10**50)


def test_zero_translation_and_invalid_words_are_not_promoted_as_secret_signals():
    p = packet()
    for v,w in [((0,0),(0,0)),((True,0),(0,0)),((1,0),(0,3)),((1,),(0,0))]:
        with pytest.raises(ValueError): probe_record(p,v,w)
    for args in [(1,2,0,1),(2,2,2,1),(1,3,4,1),(1,3,2,True)]:
        with pytest.raises(ValueError): population_envelope(*args)


def test_independent_live_certificate_and_pinned_derivation():
    import hashlib
    report = json.loads(REPORT.read_text())
    assert report["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    checker = DERIVATION.parent / "certificates/ternary_packet_pauli_gate_crosscheck.js"
    result = subprocess.run(["node",str(checker),str(REPORT)],capture_output=True,text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["completeHighLiftAssignments"] == 2187


@pytest.mark.parametrize("mutation", ["moment","histogram","rank","distance","scope","population","phases"])
def test_independent_checker_rejects_wrong_exponents_and_overbroad_claims(tmp_path, mutation):
    report = json.loads(REPORT.read_text())
    c = report["complete_conditional_censuses"][0]
    if mutation == "moment": c["exact_squared_overlap_mean"] = "1/3"
    elif mutation == "histogram": c["exact_character_difference_histogram"][0] += 1
    elif mutation == "rank": c["probe"]["restricted_kernel_frame_rank"] = 1
    elif mutation == "distance": report["complete_small_low_matrix_distance_controls"][0]["dual_minimum_distance_or_K_plus_one"] = 1
    elif mutation == "scope": report["general_receiver_no_go_claimed"] = True
    elif mutation == "population": report["analytic_population_envelopes"][0]["raw_population_menu_squared_overlap_mean_upper"] = "0"
    elif mutation == "phases": c["all_phase_tables_sha256"] = "0"*64
    target = tmp_path / "mutated.json"
    target.write_text(json.dumps(report))
    checker = DERIVATION.parent / "certificates/ternary_packet_pauli_gate_crosscheck.js"
    result = subprocess.run(["node",str(checker),str(target)],capture_output=True,text=True)
    assert result.returncode != 0
