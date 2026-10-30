"""Regular subset lifts and paid intrinsic/ambient source accounting."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import pytest

from theorems import small_prime_module as module
from theorems.prime_power_rees_descent import verify_module_witness


@pytest.mark.parametrize("prime,degree", [(3, 1), (3, 2), (5, 2), (5, 4), (7, 6)])
def test_regular_boolean_witness_lifts_original_degree_and_freezes_zeros(prime, degree):
    columns = [(1, 0), (0, 1), (0, 0), (prime-1, prime-1), (1, 0)]
    row = module.subset_module_witness(columns, prime=prime, exponents=(2, 3),
                                       degree=degree, prefix_count=3)
    assert row["status"] == "VERIFIED_REGULAR_SUBSET_MODULE_WITNESS"
    weights, scales = row["field_witness_original_degree"], row["scales"]
    assert weights[:3] == [1, 1, 0]
    assert row["lift"]["jacobian_rank"] == 2
    assert row["lift"]["lift_steps"] == 2
    assert all(scales[i] == 0 for i, w in enumerate(weights) if not w)
    assert all(s == 0 or s % prime for s in scales)
    assert verify_module_witness(columns, scales, prime=prime, exponents=(2, 3), degree=degree)
    assert not row["source_law_certified"]


def test_prefix_is_not_repaired_using_suffix_lookahead():
    row = module.subset_module_witness([(1, 0), (0, 0), (0, 1), (4, 4)], prime=5,
                                       exponents=(2, 2), degree=4, prefix_count=2)
    assert row["status"] == "ABORT" and row["scales"] is None


def test_large_exponent_lifts_without_enumerating_prime_power_module():
    row = module.subset_module_witness([(1,), (4,), (0,)], prime=5,
                                       exponents=(128,), degree=4, prefix_count=1)
    assert row["status"] == "VERIFIED_REGULAR_SUBSET_MODULE_WITNESS"
    assert row["lift"]["lift_steps"] == 127
    assert row["field_run"]["state_bound"] == 5
    assert row["field_run"]["states_visited"] <= 5
    assert row["scales"][2] == 0
    assert verify_module_witness([(1,), (4,), (0,)], row["scales"],
                                 prime=5, exponents=(128,), degree=4)


def test_failed_subset_search_is_not_general_sde_unsatisfiability():
    # There is a regular square witness (1,2), but no Boolean completion.
    row = module.subset_module_witness([(1,), (5,)], prime=7, exponents=(1,),
                                       degree=2, prefix_count=1)
    assert row["status"] == "ABORT" and row["scales"] is None
    assert verify_module_witness([(1,), (5,)], [1, 2], prime=7, exponents=(1,), degree=2)


@pytest.mark.parametrize("p,R,b", [(3, 1, 1), (5, 2, 8), (7, 4, 5), (13, 3, 4)])
def test_exact_plan_bounds_and_full_state_clock(p, R, b):
    row = module.subset_module_plan(prime=p, degree=2, cyclic_rank_bound=R, failure_bits=b)
    L = row["suffix_source_count"]
    assert row["pilot_source_count"] == row["prefix_source_count"] == R+b+2
    assert L == R*(p-1).bit_length()+b+2
    assert row["complete_dp_state_bound"] == row["dp_state_cap"] == p**R
    assert row["iid_subset_absence_bound"] == Fraction(p**R, (1 << L)-1)
    assert row["episode_abort_bound"] <= Fraction(1, 1 << b)
    assert row["source_labels_cap"] == row["pilot_source_count"]+row["bank_source_count"]
    capped = module.subset_module_plan(prime=p, degree=2, cyclic_rank_bound=R,
                                       failure_bits=b, max_states=1)
    assert not capped["complete_state_cap_met"] and capped["episode_abort_bound"] == 1
    assert capped["ideal_uncapped_episode_abort_bound"] == row["episode_abort_bound"]


def _episode(pilot, bank, *, p=3, exponents=(3,), degree=2):
    requests = []
    plan = module.subset_module_plan(prime=p, degree=degree, cyclic_rank_bound=len(exponents),
                                     failure_bits=2)
    stream = iter((pilot(plan["pilot_source_count"]), bank(plan["bank_source_count"], plan)))

    def draw(count):
        requests.append(count)
        return next(stream)

    row = module.subset_pilot_episode(prime=p, ambient_exponents=exponents, degree=degree,
                                      draw_labels=draw, failure_bits=2)
    assert requests == [plan["pilot_source_count"], plan["bank_source_count"]]
    assert row["source_labels_consumed"] == plan["source_labels_cap"]
    return row


def test_intrinsic_p_times_module_is_not_lost_to_ambient_mod_p_zero():
    def bank(count, plan):
        out = [(0,)]*count
        out[0], out[plan["prefix_source_count"]] = (3,), (6,)
        return out
    row = _episode(lambda count: [(3,)]*count, bank)
    assert row["status"] == "VERIFIED_AMBIENT_REGULAR_SUBSET_WITNESS"
    assert row["original_ambient_verified"] and not row["zero_rank_branch"]
    assert all(col[0] % 3 == 0 for col in row["selected_ambient_columns"])
    assert not row["hidden_support_completeness_certified"]


def test_incomplete_pilots_can_accept_only_verified_ambient_witnesses():
    def bank(count, plan):
        out = [(0,)]*count
        out[0], out[plan["prefix_source_count"]] = (9,), (18,)
        return out
    row = _episode(lambda count: [(9,)]*count, bank)
    assert row["status"] == "VERIFIED_AMBIENT_REGULAR_SUBSET_WITNESS"
    assert not row["hidden_support_completeness_certified"]
    assert row["original_ambient_verified"]


def test_nonmember_bank_aborts_with_both_banks_charged():
    row = _episode(lambda count: [(9,)]*count, lambda count, plan: [(3,)]*count)
    assert row["status"] == "ABORT" and row["reason"] == "OUTSIDE_PILOT_FRAME"
    assert row["scales"] is None


def test_zero_module_uses_fresh_zero_bank_and_nonzero_scale():
    row = _episode(lambda count: [(0,)]*count, lambda count, plan: [(0,)]*count)
    assert row["status"] == "VERIFIED_AMBIENT_REGULAR_SUBSET_WITNESS"
    assert row["zero_rank_branch"] and row["scales"][0] == 1
    assert sum(row["scales"]) == 1


def test_support_rank_bound_matches_tree_budget_in_larger_ambient_module():
    plan = module.subset_module_plan(prime=5, degree=2, cyclic_rank_bound=1,
                                     failure_bits=2)
    bank = [(0, 0)]*plan["bank_source_count"]
    bank[0], bank[plan["prefix_source_count"]] = (1, 0), (4, 0)
    stream = iter(([(1, 0)]*plan["pilot_source_count"], bank))
    row = module.subset_pilot_episode(prime=5, degree=2, ambient_exponents=(2, 3),
                                      cyclic_rank_bound=1, failure_bits=2,
                                      draw_labels=lambda count: next(stream))
    assert row["status"] == "VERIFIED_AMBIENT_REGULAR_SUBSET_WITNESS"
    assert row["source_labels_consumed"] == plan["source_labels_cap"] == 17
    assert row["plan"]["dp_state_cap"] == 5
    assert not row["hidden_support_rank_bound_certified"]


def test_observed_pilot_rank_contradiction_aborts_without_overspending():
    plan = module.subset_module_plan(prime=5, degree=2, cyclic_rank_bound=1,
                                     failure_bits=2)
    pilots = [(1, 0), (0, 1)]+[(0, 0)]*(plan["pilot_source_count"]-2)
    stream = iter((pilots, [(0, 0)]*plan["bank_source_count"]))
    row = module.subset_pilot_episode(prime=5, degree=2, ambient_exponents=(2, 3),
                                      cyclic_rank_bound=1, failure_bits=2,
                                      draw_labels=lambda count: next(stream))
    assert row["status"] == "ABORT" and row["reason"] == "PILOT_RANK_EXCEEDS_BOUND"
    assert row["scales"] is None
    assert row["source_labels_consumed"] == 17


@pytest.mark.parametrize("changes", [
    {"failure_bits": 0}, {"failure_bits": True}, {"max_states": 0},
    {"max_states": True}, {"degree": 3}, {"ambient_exponents": ()},
    {"draw_labels": None}, {"prime": 9},
    {"cyclic_rank_bound": 0}, {"cyclic_rank_bound": True},
])
def test_bad_contracts_fail_before_acquiring_sources(changes):
    args = dict(prime=3, degree=2, ambient_exponents=(3,), failure_bits=2,
                draw_labels=lambda n: pytest.fail("invalid request acquired labels"))
    args.update(changes)
    with pytest.raises(ValueError):
        module.subset_pilot_episode(**args)


def test_backend_corruption_is_an_error_not_statistical_abort(monkeypatch):
    monkeypatch.setattr(module, "regular_subset_witness", lambda *a, **k:
                        {"status": "VERIFIED_REGULAR_SUBSET_WITNESS", "scales": [0, 0]})
    with pytest.raises(ArithmeticError):
        module.subset_module_witness([(1,), (2,)], prime=3, exponents=(2,),
                                     degree=2, prefix_count=1)


@pytest.mark.parametrize("u", range(2, 9))
def test_small_prime_tree_failure_and_parameter_envelope(u):
    p, c, R = 5, min(4, u), u-1
    row = module.all_prime_module_tree_bound(prime=p, class_bound=c,
                                            cyclic_rank_bound=R, uniform_parameter=u)
    width = row["raw_arity_per_grade"]
    ell = (16*u-1).bit_length()
    assert width <= 16*u*ell <= 1 << (2*ell)
    assert row["failure_bits_per_node"] == 4*u*ell
    assert row["leaves_per_output_tree"] == width**(c-1)
    exact = sum((stage["nodes"]*stage["plan"]["episode_abort_bound"]
                 for stage in row["stages"]), Fraction(0))
    assert row["tree_abort_bound"] == exact <= Fraction(1, 64)
    assert row["dp_states_per_node_upper"] == p**R
    assert row["all_prime_branch_coverage"]
    assert row["class_strictly_below_prime_required"]
    assert row["uniform_branch_tree_abort_bound"] == Fraction(1, 16)
    assert not row["all_prime_ring_hsp_bound"]
    assert not row["original_oracle_queries_included"]
    assert not row["class_bounded_by_derived_cyclic_rank"]


def test_large_prime_branch_reuses_existing_verified_source_bound():
    row = module.all_prime_module_tree_bound(prime=1009, class_bound=3,
                                            cyclic_rank_bound=2, uniform_parameter=3)
    assert row["regime"] == "LARGE_PRIME_UNIT_KERNEL"
    assert row["raw_arity_per_grade"] == 24
    assert row["tree_abort_bound"] <= Fraction(1, 16)
    assert row["uniform_branch_tree_abort_bound"] == Fraction(1, 16)
    assert not row["small_prime_state_enumeration_used"]


def test_both_regime_coverage_does_not_remove_class_below_prime_promise():
    with pytest.raises(ValueError):
        module.all_prime_module_tree_bound(prime=3, class_bound=3,
                                           cyclic_rank_bound=1, uniform_parameter=3)


def test_live_report_control_scope_and_source_hashes():
    row = module.report()
    assert [case["name"] for case in row["cases"]] == [
        "ambient_mod_p_zero", "p5_quadratic_oblique", "p5_quartic_oblique"]
    assert all(case["result"]["original_ambient_verified"] for case in row["cases"])
    for case in row["cases"][1:]:
        inner = case["result"]["intrinsic_run"]
        assert sorted(inner["exponents"]) == [1, 2]
        assert inner["lift"]["jacobian_rank"] == 2
        assert inner["field_run"]["state_bound"] == 25
        # The report must exercise a genuine Z/25 x Z/5 support, not a
        # redundant pair of generators for one cyclic factor.
        generators = case["generator_columns"]
        elements = {tuple((a*generators[0][j]+b*generators[1][j]) % modulus
                          for j, modulus in enumerate((25, 125)))
                    for a in range(25) for b in range(5)}
        assert len(elements) == 125
    assert not row["all_prime_ring_hsp_bound"] and not row["speedup_claim_allowed"]
    root = Path(__file__).resolve().parents[1]
    for source, digest in row["source_sha256"].items():
        assert sha256((root/source).read_bytes()).hexdigest() == digest
