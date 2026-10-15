"""Actual reversible Gaussian controls, source law, and recursive-cost falsifiers."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
from random import Random
import subprocess
import sys

import numpy as np
import pytest

from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic
from theorems.dcp_disjoint_kernel_pairing import (
    CONTRACT, CONTRACT_ID, REPORT, apply_evaluator, build_report, check_program,
    control_columns, first_dependence, frontier, make_program, mean_visibility_from_weights,
    native_noise_bound, partner, reversible_evaluator,
)
from theorems.dcp_nonlinear_fiber_pairing import compiler_certificate, phase_value, program_value, wire_map


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "research/certificates/dcp_disjoint_kernel_pairing_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_report()


def test_every_scalar_coarse_table_and_original_assignment_is_fixedpoint_free_reciprocal():
    count = 0
    for row in product(range(4), repeat=4):
        P = make_program((row,))
        assert P["coarse_labels"] == [list(row)]
        for x in range(16):
            y = partner(P, x)
            assert y != x and partner(P, y) == x
            assert phase_value((row,), x, 4) == phase_value((row,), y, 4)
            assert control_columns(P, x) == control_columns(P, y)
            count += 1
    assert count == 4096


def test_online_gaussian_witness_matches_independent_smallest_integer_dependence():
    for n in (1, 2, 3):
        rng = Random(711+n)
        for _ in range(200):
            columns = [rng.getrandbits(n) for _ in range(n+1)]
            def value(d):
                answer = 0
                for j, v in enumerate(columns):
                    if d >> j & 1:
                        answer ^= v
                return answer
            expected = next(d for d in range(1, 1 << (n+1)) if not value(d))
            assert first_dependence(columns, n) == expected


def test_every_exported_gate_evaluates_partner_with_arbitrary_xor_target_and_clean_work(report):
    rng = Random(711)
    for C in report["finite_controls"]:
        P, E = C["program"], C["reversible_XOR_F"]
        m = P["width"]
        for x in range(1 << m):
            target = rng.getrandbits(m+1)
            output = apply_evaluator(x | (target << m), E)
            expected = x | ((target ^ ((1 << m) + partner(P, x))) << m)
            assert output == expected
            assert apply_evaluator(output, E, inverse=True) == x | (target << m)
        assert E["zero_work_bits_required"] > 0
        assert sum(E["gate_counts"].values()) == len(E["gates"])
        assert E["gate_counts"]["CCX"] > 0


def test_full_dirty_work_space_is_reversible_but_not_assumed_clean_semantics(report):
    rng = Random(822)
    for C in report["finite_controls"]:
        E = C["reversible_XOR_F"]
        for _ in range(64):
            word = rng.getrandbits(E["total_qubits"])
            assert apply_evaluator(apply_evaluator(word, E), E, inverse=True) == word
        for gate in E["gates"]:
            assert gate[0] in ("X", "CX", "CCX")
            assert len(set(gate[1:])) == len(gate)-1


def test_compiled_gate_counts_have_polynomial_not_truth_table_growth():
    counts = []
    for n in (1, 2, 4, 6):
        m = (n+1)**2
        rng = Random(43+n)
        A = tuple(tuple(rng.randrange(4) for _ in range(m)) for _ in range(n))
        P = make_program(A)
        E = reversible_evaluator(P)
        assert len(E["gates"]) < 100*(n*m+n**3+m)
        assert E["total_qubits"] < 100*(n*m+n**3+m)
        assert P["full_assignment_lookup_rows"] == 0
        for _ in range(4):
            x = rng.getrandbits(m)
            assert apply_evaluator(x, E) == x | (((1 << m) + partner(P, x)) << m)
        counts.append(len(E["gates"]))
    assert counts == sorted(counts)


def test_program_does_not_consume_higher_labels_or_private_phase_and_extra_inputs_remain_live():
    low = ((1, 1, 3, 3, 2),)
    P = make_program(low)
    Q = make_program(tuple(tuple(a+4*(i+5) for i, a in enumerate(row)) for row in low))
    assert P == Q
    assert P["selection_access"] == "coarse-public-labels-only"
    assert all((partner(P, x) >> 4 & 1) == (x >> 4 & 1) for x in range(32))


def test_all_higher_lifts_give_uniform_output_for_every_coarse_selected_pair():
    P = make_program(((1, 1, 1, 1),))
    pairs = [(x, partner(P, x)) for x in range(16) if x < partner(P, x)]
    hist = {pair: Counter() for pair in pairs}
    zero_admission = 0
    for high in product(range(4), repeat=4):
        A = (tuple(1+4*z for z in high),)
        for x, y in pairs:
            delta = sum(a*((y >> i & 1)-(x >> i & 1)) for i, a in enumerate(A[0]))
            assert delta % 4 == 0
            label = delta//4 % 4
            hist[x, y][label] += 1
            zero_admission += label == 0
    assert all(h == {0:64, 1:64, 2:64, 3:64} for h in hist.values())
    assert Fraction(zero_admission, 256*len(pairs)) == Fraction(1,4)


def test_existing_six_call_compiler_uses_live_polynomial_program_and_actual_signed_labels(report):
    for C in report["finite_controls"]:
        K, P = C["compiler"], C["program"]
        m = P["width"]
        A = tuple(tuple(int(a, 16) for a in row) for row in K["public_labels_hex"])
        t = K["phase_bits"]
        assert compiler_certificate(A, t, 2, P) == K
        assert K["accepted_XOR_F_calls"] == 6 and K["failed_XOR_F_calls"] == 4
        assert K["output_qubits_on_accepted_attempt"] == 1
        for x in range(1 << m):
            assert program_value(P, x) == partner(P, x)
            accepted = wire_map(x, P, A, t, 2, "accept")
            assert accepted & ((1 << m)-1) == x
            assert accepted & ~((1 << m)-1) in (0, 1 << (3*m+2))
            assert wire_map(accepted, P, A, t, 2, "accept", inverse=True) == x


@pytest.mark.parametrize("visibility", [Fraction(1), Fraction(1, 2)])
def test_actual_unknown_phase_density_and_original_width_noise_not_merge_depth(visibility):
    A, t, q = ((1, 5, 9, 13),), 4, 16
    P = make_program(A)
    C = compiler_certificate(A, t, 2, P)
    for secret in (0, 1, 3, 7, 15):
        def amplitude(x):
            return np.exp(2j*math.pi*(secret*phase_value(A,x,q)[0] % q)/q)/4
        for pair in C["pairs"]:
            x, y = pair["first"], pair["second"]
            raw = np.outer([amplitude(x), amplitude(y)], np.conj([amplitude(x), amplitude(y)]))
            raw[0,1] *= float(visibility**((x ^ y).bit_count()))
            raw[1,0] *= float(visibility**((x ^ y).bit_count()))
            mass = float(np.trace(raw).real)
            assert mass == pytest.approx(1/8)
            label = int(pair["descended_label_hex"][0],16)
            angle = 2*math.pi*(secret*label % 4)/4
            v = float(visibility**pair["physical_Hamming_width"])
            expected = np.array([[1,v*np.exp(-1j*angle)],[v*np.exp(1j*angle),1]])/2
            assert np.allclose(raw/mass, expected, atol=1e-14)


def test_exact_physical_width_histogram_and_noise_average(report):
    C = report["finite_controls"][0]
    assert C["physical_direction_width_histogram"] == {"2":12, "4":4}
    v = Fraction(1,4)
    actual = sum(Fraction(count,16)*v**int(w) for w,count in C["physical_direction_width_histogram"].items())
    assert actual == (3*v*v+v**4)/4


def test_exact_first_dependence_noise_law_against_every_small_column_table():
    for n,weights in ((1,(2,1)),(2,(1,3,2)),(3,(1,3,2,4))):
        v=Fraction(3,4)
        hist=[Counter() for _ in range(n+1)]
        for columns in product(range(1 << n),repeat=n+1):
            d=first_dependence(columns,n)
            hist[d.bit_length()-1][sum(w for j,w in enumerate(weights) if d >> j & 1)]+=1
        total=Fraction(0)
        R=mean_visibility_from_weights(weights,v)
        for j,H in enumerate(hist):
            count=sum(H.values())
            probability=Fraction(count,1 << (n*(n+1)))
            conditional=sum(Fraction(c,count)*v**w for w,c in H.items())
            assert decode_dyadic(R["first_dependence_law"][j]["probability"])==probability
            assert decode_dyadic(R["first_dependence_law"][j]["conditional_mean_visibility"])==conditional
            total+=probability*conditional
        assert decode_dyadic(R["native_mean_unfiltered_visibility"])==total


def test_noise_mean_requires_averaging_second_low_bits_not_fixed_full_coarse_A():
    v=Fraction(1,4)
    native_total=Fraction(0)
    for B in product(range(2),repeat=4):
        base=make_program((B,))
        weights=[int(u,16).bit_count() for u in base["disjoint_supports_hex"]]
        mean=Fraction(0)
        for high in product(range(2),repeat=4):
            A=(tuple(a+2*z for a,z in zip(B,high)),)
            P=make_program(A)
            assert P["disjoint_supports_hex"]==base["disjoint_supports_hex"]
            mean+=sum(v**((x^partner(P,x)).bit_count()) for x in range(16))/256
        assert decode_dyadic(mean_visibility_from_weights(weights,v)["native_mean_unfiltered_visibility"])==mean
        native_total+=mean/16
    R=native_noise_bound(1,v)
    assert native_total<=decode_dyadic(R["native_mean_unfiltered_visibility_upper_bound"])
    fixed=make_program(((0,0,0,0),))
    actual=sum(v**((x^partner(fixed,x)).bit_count()) for x in range(16))/16
    expected=decode_dyadic(mean_visibility_from_weights((1,1),v)["native_mean_unfiltered_visibility"])
    assert actual==v and actual!=expected


def test_native_noise_upper_does_not_confuse_a_lower_factor_with_a_no_go(report):
    rows=report["native_noise_upper_frontiers"]
    assert len(rows)==12
    for R in rows:
        upper=decode_dyadic(R["native_mean_unfiltered_visibility_upper_bound"])
        v=decode_dyadic(R["visibility"])
        assert 0<=upper<=1
        assert v**R["original_copies"]<=upper
        assert R["arbitrary_partial_or_collective_pairing_covered"] is False
        assert R["fixed_full_coarse_matrix_inherits_this_probability_bound"] is False
    assert decode_dyadic(rows[-2]["native_mean_unfiltered_visibility_upper_bound"])<Fraction(1,1000)
    assert decode_dyadic(rows[-1]["native_mean_unfiltered_visibility_upper_bound"])==1
    assert decode_dyadic(native_noise_bound(512,Fraction(511,512))["native_mean_unfiltered_visibility_upper_bound"])<Fraction(1,1000000)
    assert 15**15 > 2**56
    for n in (32,64,128,256):
        R=native_noise_bound(n,1-Fraction(1,n))
        bad=decode_dyadic(R["some_block_has_a_short_nonempty_kernel_vector_probability_upper_bound"])
        good=decode_dyadic(R["mean_visibility_given_no_short_block_upper_bound"])
        assert bad <= Fraction(2*(n+1),1 << (n//2))
        assert good <= 2*Fraction(33,34)**(n+1)


def test_valid_disjoint_supports_alone_do_not_certify_the_deterministic_parity_only_selector():
    P=make_program(((0,0,0,0),))
    P["disjoint_supports_hex"][0]="0x2"
    with pytest.raises(ValueError,match="provenance"):
        check_program(P)


def test_actual_two_stage_CNOT_Z_instrument_on_full_unknown_mixed_source(report):
    C = report["finite_controls"][1]
    F, K = C["CNOT_Z_feedforward_receiver"], C["compiler"]
    A = tuple(tuple(int(a,16) for a in row) for row in K["public_labels_hex"])
    m, q = len(A[0]), 1 << K["phase_bits"]
    size = 1 << m
    pivots = set(F["logical_pivot_wires"])
    by_background = {int(b["first_background_hex"],16):b for b in F["branches"]}
    def cnots(x,gates):
        for control,target in gates:
            x ^= ((x >> control) & 1) << target
        return x
    # Execute the actual first measurement/chart, then its measured-outcome
    # controlled CNOTs, WITHOUT using the producer's partner endpoints.
    inverse = [None]*size
    for x in range(size):
        chart = cnots(x,F["first_stage_CNOTs"])
        background = chart & ~sum(1 << p for p in pivots)
        z = cnots(chart,by_background[background]["second_stage_CNOTs"])
        assert inverse[z] is None
        inverse[z] = x
    eta = Fraction(3,4)
    for secret in ((0,0),(1,7),(11,3)):
        phase = np.array([sum(s*a for s,a in zip(secret,phase_value(A,x,q)))%q for x in range(size)])
        amplitudes = np.exp(2j*math.pi*phase/q)/math.sqrt(size)
        rho = np.outer(amplitudes,np.conj(amplitudes))
        rho *= np.array([[float(eta**((x^y).bit_count())) for y in range(size)] for x in range(size)])
        transformed = rho[np.ix_(inverse,inverse)]
        total = 0
        for B in F["branches"]:
            output = B["output_physical_wire"]
            other = [p for p in F["logical_pivot_wires"] if p!=output]
            z = int(B["first_background_hex"],16) | sum(((B["second_outcome"] >> k)&1)<<p for k,p in enumerate(other))
            endpoints = [z,z|(1 << output)]
            assert [inverse[e] for e in endpoints] == B["oriented_original_endpoints"]
            block = transformed[np.ix_(endpoints,endpoints)]
            mass = float(np.trace(block).real)
            assert mass == pytest.approx(2/size)
            total += mass
            label = [int(a,16) for a in B["output_label_hex"]]
            angle = 2*math.pi*(sum(s*a for s,a in zip(secret,label))%(q//4))/(q//4)
            v = float(eta**B["original_pair_width"])
            expected = np.array([[1,v*np.exp(-1j*angle)],[v*np.exp(1j*angle),1]])/2
            assert np.allclose(block/mass,expected,atol=2e-14)
        assert total == pytest.approx(1)


def test_selected_large_global_pairing_is_provably_not_globally_affine(report):
    C = report["selected_global_nonaffine_control"]
    assert C["signature_certificate"]["nonzero_distinct_signatures"] is True
    assert C["signature_certificate"]["global_affine_mod4_automorphism_classification"] == "IDENTITY_ONLY"
    assert C["program"]["width"] == 49
    for row in C["sampled_original_inputs"]:
        x, y = int(row["input_hex"],16), int(row["partner_hex"],16)
        assert y == partner(C["program"], x) and y != x
        assert partner(C["program"], y) == x


def test_recursive_cost_is_not_promoted_from_per_level_admission(report):
    for R in report["supply_and_noise_frontiers"]:
        n, t = R["secret_vector_components"], R["phase_bits"]
        assert int(R["ideal_no_failure_copies_including_last_one_bit_stage"]) == (n+1)**(t-1)
        assert R["all_levels_source_and_noise_composition_certified"] is False
        assert R["new_Kuperberg_or_Regev_exponent"] is False
        assert R["visibility_factors_are_conservative_lower_bounds_NOT_noise_upper_bounds"] is True
        assert decode_dyadic(R["one_over_n2_visibility_worst_width_factor"]) > Fraction(1,16)
    assert len(str((33)**31)) > 40


@pytest.mark.parametrize("mutation", ["overlap", "parity", "empty", "higher", "access", "free", "novelty", "bool"])
def test_forged_programs_cannot_inherit_coarse_only_or_polynomial_guarantees(mutation):
    P = make_program(((1,1,1,1),))
    if mutation == "overlap":
        P["disjoint_supports_hex"][1] = P["disjoint_supports_hex"][0]
    elif mutation == "parity":
        P["disjoint_supports_hex"][0] = "0x1"
    elif mutation == "empty":
        P["disjoint_supports_hex"][0] = "0x0"
    elif mutation == "higher":
        P["coarse_labels"][0][0] = 5
    elif mutation == "access":
        P["selection_access"] = "full-labels"
    elif mutation == "free":
        P["table_lookup_is_a_free_coherent_oracle"] = True
    elif mutation == "bool":
        P["components"] = True
    else:
        P["new_sieve_exponent_claimed"] = True
    with pytest.raises(ValueError):
        check_program(P)


def test_caps_are_unknown_not_negative_or_a_fake_coherent_lookup():
    with pytest.raises(ValueError,match="UNKNOWN"):
        make_program(((1,1,1),))
    A = tuple((1,)*100 for _ in range(9))
    with pytest.raises(ValueError,match="UNKNOWN"):
        reversible_evaluator(make_program(A))
    with pytest.raises(ValueError,match="UNKNOWN"):
        frontier(128,4096)


def js_check(R,tmp_path):
    target = tmp_path/"certificate.json"
    target.write_text(json.dumps(R))
    return subprocess.run(["node",str(CHECKER),str(target)],capture_output=True,text=True)


def test_live_provenance_and_independent_gate_source_supply_replay(report,tmp_path):
    assert json.loads(REPORT.read_text()) == report
    assert json.loads(CONTRACT.read_text())["contract_id"] == CONTRACT_ID
    result = js_check(report,tmp_path)
    assert result.returncode == 0,result.stderr
    assert json.loads(result.stdout)["reversible_evaluator_assignments"] == 528


@pytest.mark.parametrize("mutation",["gate", "cleanup", "gate_cost", "program_hash", "pair", "zero_label", "width", "supply", "noise", "scope", "feedforward", "native_noise", "conditional_mean"])
def test_checker_rejects_tampered_physical_and_cost_claims(report,tmp_path,mutation):
    R = deepcopy(report)
    C = R["finite_controls"][0]
    if mutation == "gate":
        C["reversible_XOR_F"]["gates"][0][-1] = 0
    elif mutation == "cleanup":
        C["reversible_XOR_F"]["gates"].pop()
        C["reversible_XOR_F"]["gate_counts"]["CX"] -= 1
    elif mutation == "gate_cost":
        C["reversible_XOR_F"]["gate_counts"]["CCX"] = 0
    elif mutation == "program_hash":
        C["reversible_XOR_F"]["program_sha256"] = "0"*64
    elif mutation == "pair":
        C["compiler"]["pairs"][0]["second"] = C["compiler"]["pairs"][0]["first"]
    elif mutation == "zero_label":
        C["compiler"]["pairs"][0]["descended_label_hex"] = ["0x0"]
    elif mutation == "width":
        C["physical_direction_width_histogram"]["2"] = 16
    elif mutation == "supply":
        R["supply_and_noise_frontiers"][0]["ideal_no_failure_copies_including_last_one_bit_stage"] = "25"
    elif mutation == "noise":
        R["supply_and_noise_frontiers"][0]["one_over_n2_visibility_worst_width_factor"]["numerator_hex"] = "0x1"
    elif mutation == "feedforward":
        C["CNOT_Z_feedforward_receiver"]["branches"][0]["oriented_original_endpoints"].reverse()
    elif mutation == "native_noise":
        R["native_noise_upper_frontiers"][0]["native_mean_unfiltered_visibility_upper_bound"]["numerator_hex"]="0x0"
    elif mutation == "conditional_mean":
        R["parity_conditioned_noise_means"][0]["native_mean_unfiltered_visibility"]["numerator_hex"]="0x0"
    else:
        R["scope"]["polynomial_supply_for_growing_phase_bits"] = True
    result = js_check(R,tmp_path)
    assert result.returncode != 0


def test_read_only_cli_preserves_live_artifact():
    before = REPORT.read_bytes()
    result = subprocess.run([sys.executable,"qsearch.py","dcp-disjoint-kernel-pairing","--no-write"],
                            cwd=ROOT,capture_output=True,text=True)
    assert result.returncode == 0,result.stderr
    assert json.loads(result.stdout)["new_sieve_exponent"] is False
    assert REPORT.read_bytes() == before
