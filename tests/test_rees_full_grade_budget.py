"""Exact forest/cap controls, not a quantum execution or theorem verifier."""
from fractions import Fraction
from math import factorial, gcd, prod
import json

import pytest

from theorems.uniform_bch_rees import scalar_line_budget, symmetric_recovery_budget


@pytest.mark.parametrize("profile,prime", [((4,), 2), ((3, 1), 65537),
                                          ((6, 3, 1), 65537),
                                          ((7, 5, 4, 3, 2, 1), 2**127-1),
                                          ((13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1), 2**127-1)])
def test_whole_grade_tree_errors_and_caps(profile, prime):
    epsilon = Fraction(1, 100)
    result = symmetric_recovery_budget(profile, prime=prime, error=epsilon)
    arities = [rank+1 if gcd(d, prime-1) == 1 else (rank+1)*((gcd(d, prime-1)-1)*rank+1)
               for d, rank in enumerate(profile[1:], 2)]
    samples = result["final_fourier_samples"]
    leaves = samples*prod(arities)
    assert leaves == result["source_preparations"]
    assert result["original_inputs"] == len(profile)*leaves
    assert result["cover_dimension"] == sum(profile)
    assert result["leaves_per_terminal"] <= result["derived_parameter_leaf_bound"]
    r = profile[1] if len(profile) > 1 else 0
    assert result["derived_parameter_leaf_bound"] <= factorial(r)*factorial(r+1)**2
    assert result["leaves_per_terminal"] <= (r+1)**(3*r)
    assert result["scalar_flag_leaves_per_terminal"] == scalar_line_budget(profile, 1, prime=prime).leaves_per_terminal
    need = leaves
    merges = measurements = uniform_calls = bit_cap = pairs = 0
    actual_abort = Fraction(0)
    for stage in result["stages_top_down"]:
        assert stage["consumed_targets"] == need == stage["arity"]*stage["conversions"]
        need = stage["conversions"]
        merges += need
        measurements += stage["consumed_targets"]
        if stage["randomness"] is None:
            assert stage["reduced_degree"] == 1
            continue
        g, a, k = stage["reduced_degree"], stage["rank"], result["solver_failure_bits_per_call"]
        # Recompute the elementary caps, not through randomness_budget.
        roots = ((g-1)*a+1)*(a+3)+g*(g+1)//2
        union = g+roots*(g-1)
        B = k+1+(union-1).bit_length()
        Q = g*B+sum(2*g**j*B for j in range(2, g+1))+roots*g*(g-1)*3*B
        L = k+1+(Q-1).bit_length()
        cap = stage["randomness"]
        assert cap["root_calls"] == roots
        assert cap["uniform_calls"] == Q
        assert cap["fair_bits"] == Q*L*(prime-1).bit_length()
        assert cap["polynomial_pow_gcd_pairs"] == roots*(g-1)*3*B
        assert cap["abort_bound"] == Fraction(union, 2**B)+Fraction(Q, 2**L)
        uniform_calls += need*Q
        bit_cap += need*cap["fair_bits"]
        pairs += need*cap["polynomial_pow_gcd_pairs"]
        actual_abort += need*cap["abort_bound"]
    assert need == samples
    assert merges == result["sde_calls"] <= leaves-samples
    assert measurements == result["central_character_measurements"] == leaves+merges-samples
    assert result["complete_instrument_calls"] == leaves+merges+samples <= 2*leaves
    assert uniform_calls == result["classical_uniform_draw_cap"]
    assert bit_cap == result["classical_fair_bit_cap"]
    assert pairs == result["classical_root_pow_gcd_pair_cap"]
    assert actual_abort <= result["solver_abort_bound"] <= epsilon/3
    assert result["rank_failure_bound"] <= epsilon/3
    assert result["instrument_error_per_call"]*result["complete_instrument_calls"] == epsilon/3
    assert result["total_error_bound"] <= epsilon
    assert result["classical_retry_extra_source_copies"] == 0
    for key in ("prime_validation_included", "profile_existence_certified", "physical_gate_clock",
                "quantum_receiver_implemented", "formal_total_policy_instantiated",
                "novelty_established", "speedup_claim_allowed"):
        assert result[key] is False


def test_small_field_rejects_and_only_reduced_degree_guard_is_required():
    with pytest.raises(ValueError, match="field guard"):
        symmetric_recovery_budget((6, 3, 1), prime=5)
    # Class 3 does not divide p-1, and the class-only guard fails. The actual
    # nonlinear degree is 2, whose guard does hold at this supplied prime.
    result = symmetric_recovery_budget((6, 3, 1), prime=65537)
    assert 65537 < 16*3**8
    assert [s["reduced_degree"] for s in result["stages_top_down"]] == [1, 2]


def test_whole_grade_need_not_pointwise_improve_scalar_flags():
    whole = symmetric_recovery_budget((3, 1), prime=65537)
    assert whole["leaves_per_terminal"] == 4 > whole["scalar_flag_leaves_per_terminal"] == 3
    profile = (13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
    improved = symmetric_recovery_budget(profile, prime=2**127-1)
    assert improved["leaves_per_terminal"] < improved["scalar_flag_leaves_per_terminal"]


def test_class_eight_is_not_excluded_by_a_universal_class_six_query_cutoff():
    # Genuine filiform algebra: [x,y_i]=y_(i+1), with abelian y ideal.
    # This certifies a profile for a cost countercontrol, not a native hard HSP.
    prime, dimension = 1103, 9
    assert all(prime % divisor for divisor in range(2, 34))

    def bracket(left, right):
        return tuple(0 if k < 2 else
                     (left[0]*right[k-1]-right[0]*left[k-1]) % prime
                     for k in range(dimension))

    basis = [tuple(int(i == j) for j in range(dimension)) for i in range(dimension)]
    for x in basis:
        for y in basis:
            for z in basis:
                terms = (bracket(x, bracket(y, z)), bracket(y, bracket(z, x)),
                         bracket(z, bracket(x, y)))
                assert all(sum(row[i] for row in terms) % prime == 0
                           for i in range(dimension))
    layer, profile = set(range(dimension)), []
    while layer:
        profile.append(len(layer))
        layer = {k for i in range(dimension) for j in layer
                 for k, value in enumerate(bracket(basis[i], basis[j])) if value}
    assert tuple(profile) == (9, 7, 6, 5, 4, 3, 2, 1)
    result = symmetric_recovery_budget(tuple(profile), prime=prime, error=Fraction(1, 100))
    stages = list(reversed(result["stages_top_down"]))
    assert [s["reduced_degree"] for s in stages] == [2, 1, 2, 1, 2, 1, 2]
    assert [s["arity"] for s in stages] == [64, 7, 36, 5, 16, 3, 4]
    assert result["leaves_per_terminal"] == 15482880
    assert result["final_fourier_samples"] == 18
    assert result["original_inputs"] == 2229534720 < 10**12
    assert not result["quantum_receiver_implemented"]
    assert not result["physical_gate_clock"]
    assert not result["speedup_claim_allowed"]


@pytest.mark.parametrize("profile,prime,error", [((), 5, Fraction(1, 3)),
    ((3, 1, 1), 5, Fraction(1, 3)), ((3, 2), 5, Fraction(1, 3)),
    ((3, 1), None, Fraction(1, 3)), ((3, 1), 2, Fraction(1, 3)),
    ((3, 1), 65537, 0.1), ((3, 1), 65537, Fraction(0)), ((3, 1), 65537, Fraction(1))])
def test_bad_budget_contracts_reject(profile, prime, error):
    with pytest.raises(ValueError):
        symmetric_recovery_budget(profile, prime=prime, error=error)


def test_rees_budget_cli_is_separate_and_replayable(tmp_path, capsys):
    import qsearch
    from theorems.uniform_bch_rees import symmetric_rees_report
    parser = qsearch.build_parser()
    args = parser.parse_args(["power-sde", "--rees-budget", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((tmp_path/"research/reductions/rees_full_grade_budget.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    expected = symmetric_rees_report()
    assert saved["cases"][2]["original_inputs"] == expected["cases"][2]["original_inputs"]
    assert not (tmp_path/"research/reductions/power_sde.json").exists()
    assert not (tmp_path/"research/reductions/power_sde_bounded_randomness.json").exists()
    with pytest.raises(SystemExit):
        parser.parse_args(["power-sde", "--rees-budget", "--bounded-randomness"])
