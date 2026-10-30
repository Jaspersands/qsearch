"""Exact small-field probability checks and bounded fixed-bank regressions."""
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random

import pytest

from theorems import pivot_power_sde as solver
from theorems.bounded_power_roots import BoundedPowerRoot


class Bits:
    def __init__(self, prefix=(), tail=0):
        self.prefix = iter(prefix)
        self.tail = tail
        self.calls = 0

    def getrandbits(self, width):
        self.calls += 1
        return next(self.prefix, (1 << width)-1 if self.tail == "ones" else self.tail)


def run(p=5, e=2, bank=((1,), (4,)), **kwargs):
    options = dict(pilot_count=1, rank_bound=1, attempt_cap=8,
                   failure_bits=8, bit_source=random.Random(19))
    options.update(kwargs)
    result = solver.pivot_power_sde(p, e, bank, **options)
    assert_counts(result)
    if result["status"] == "VERIFIED":
        assert_witness(result)
    else:
        assert result["weights"] is None and result["power_vector"] is None
        assert not result["exact_verified"]
    return result


def assert_counts(result):
    b = result["budget"]
    assert result["attempts"] <= b["attempt_cap"]
    assert result["completed_candidates"] <= result["attempts"]
    assert result["sample_uniform_calls"] <= b["sample_uniform_call_cap"]
    assert result["root_uniform_calls"] <= result["root_uniform_call_cap_charged"] <= b["root_uniform_call_cap"]
    assert result["uniform_calls"] == result["sample_uniform_calls"]+result["root_uniform_calls"]
    assert result["uniform_calls"] <= b["uniform_call_cap"]
    assert result["bit_draws"] <= b["bit_draw_cap"]
    assert result["random_bits"] <= b["random_bit_cap"]
    assert result["root_calls_completed"] <= result["root_calls_started"] <= b["root_call_cap"]
    assert result["root_split_trial_cap_charged"] == result["root_calls_started"]*b["root_split_trials_per_call_cap"]
    assert result["root_uniform_call_cap_charged"] == result["root_calls_started"]*b["root_uniform_calls_per_call_cap"]
    assert result["completed_root_split_trials"] <= result["root_split_trial_cap_charged"]
    assert result["input_labels_charged"] == len(result["columns"])
    assert not result["input_labels_resampled"]
    assert not result["iid_uniform_columns_verified"]
    assert result["arbitrary_fixed_bank_success_bound"] is None


def assert_witness(result):
    p, e = result["p"], result["e"]
    weights, bank = result["weights"], result["columns"]
    assert result["exact_verified"] and any(weights)
    assert tuple(pow(s, e, p) for s in weights) == result["power_vector"]
    assert all(sum(pow(s, e, p)*col[j] for s, col in zip(weights, bank)) % p == 0
               for j in range(len(bank[0])))
    assert weights[result["pilot_count"]] == 1
    assert all(weights[i] == 0 for i in range(result["pilot_count"])
               if i not in result["pilot_indices"])


@pytest.mark.parametrize("p,e,a,ell", [(3,2,1,3), (3,2,2,3), (5,4,2,3),
                                      (5,2,1,4), (7,3,2,3), (13,3,1,3)])
def test_exhaustive_conditional_moments(p, e, a, ell):
    S = sorted({pow(s, e, p) for s in range(p)})
    candidates = [(1,)+x for x in product(S, repeat=ell-1)]
    bound = solver.pivot_conditional_moments(p, e, a, ell)
    sx = sx2 = bad = 0
    for flat in product(range(p), repeat=a*ell):
        rows = [flat[j*ell:(j+1)*ell] for j in range(a)]
        count = sum(all(-sum(z*t for z,t in zip(row,x)) % p in S for row in rows)
                    for x in candidates)
        sx += count
        sx2 += count*count
        bad += count < bound["mean"]/2
    number = p**(a*ell)
    mean = Fraction(sx, number)
    assert mean == bound["mean"]
    assert Fraction(sx2, number)-mean**2 == bound["variance"]
    assert Fraction(bad, number) <= bound["tail_bad_bank_upper"]
    assert len(candidates) == bound["candidate_count"]


@pytest.mark.parametrize("p,a,N", [(3,1,1), (3,1,3), (3,2,2), (3,2,3), (5,1,2)])
def test_exact_pilot_failure(p, a, N):
    deficient = 0
    for flat in product(range(p), repeat=a*N):
        cols = [flat[i*a:(i+1)*a] for i in range(N)]
        span = {tuple(sum(c*v[j] for c,v in zip(coeffs,cols)) % p for j in range(a))
                for coeffs in product(range(p), repeat=N)}
        deficient += len(span) < p**a
    b = solver.pivot_power_budget(p, 2, N+2, pilot_count=N, rank_bound=a, attempt_cap=3)
    assert Fraction(deficient, p**(a*N)) == b["pilot_failure_upper"]
    assert b["pilot_failure_upper"] <= b["pilot_failure_geometric_upper"]


def test_conditional_coordinate_law_and_prefix_only_selection():
    for prefix in product(range(3), repeat=2):
        if not any(prefix):
            continue
        images = Counter()
        for suffix in product(range(3), repeat=2):
            result = run(3, 1, [(x,2*x%3) for x in prefix+suffix],
                         pilot_count=2, bit_source=Bits())
            images[result["suffix_coordinates"]] += 1
            assert result["pilot_indices"] == (next(i for i,x in enumerate(prefix) if x),)
        assert set(images.values()) == {1}
        assert len(images) == 9


def test_no_suffix_pivot_promotion_and_all_memberships_checked():
    result = run(bank=((0,0), (1,0), (0,1), (0,0)), rank_bound=1)
    assert result["reason"] == "SUFFIX_OUTSIDE_PILOT_SPAN"
    assert result["pilot_indices"] == ()
    assert result["outside_pilot_indices"] == (1,2)
    assert result["suffix_membership_checks"] == 3
    assert result["uniform_calls"] == 0
    # Even a readily usable zero suffix does not bypass later nonmembership.
    result = run(bank=((1,0), (0,0), (0,1)))
    assert result["reason"] == "SUFFIX_OUTSIDE_PILOT_SPAN"
    assert result["suffix_membership_checks"] == 2


def test_rank_promise_checks_pilot_not_ambient_dimension():
    bad = run(bank=((1,0), (0,1), (1,1)), pilot_count=2, rank_bound=1)
    assert bad["reason"] == "PILOT_RANK_EXCEEDS_PROMISE"
    good = run(bank=((1,2,3), (4,3,2)))
    assert good["status"] == "VERIFIED" and good["pilot_rank"] == 1


@pytest.mark.parametrize("p,e,bank,R", [(5,4,[(0,),(0,)],0), (5,4,[(),()],0),
                                       (5,3,[(1,2),(2,4)],1), (7,1,[(2,),(5,)],1)])
def test_deterministic_branches(p, e, bank, R):
    class Forbidden:
        def getrandbits(self, width):
            raise AssertionError("deterministic branch drew randomness")
    result = run(p, e, bank, rank_bound=R, bit_source=Forbidden())
    assert result["status"] == "VERIFIED"
    assert result["attempts"] == result["uniform_calls"] == result["root_calls_started"] == 0


def test_zero_bank_with_loose_rank_bound():
    result = run(bank=((0,),(0,),(0,)))
    assert result["reason"] == "ZERO_BANK_DETERMINISTIC"
    assert result["budget"]["root_call_cap"] == 1
    assert result["root_calls_started"] == 0


@pytest.mark.parametrize("bank", [((0,0),), ((),)])
def test_single_zero_label_with_empty_rank_zero_pilot(bank):
    result = run(bank=bank,pilot_count=0,rank_bound=0,bit_source=Bits())
    assert result["status"] == "VERIFIED" and result["weights"] == (1,)
    assert result["input_labels_charged"] == result["suffix_membership_checks"] == 1
    assert result["budget"]["uniform_call_cap"] == 0


def test_uniform_power_alphabet_including_zero_and_retained_roots(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("zero pivot or known suffix root was extracted")
    monkeypatch.setattr(solver, "bounded_power_root", forbidden)
    histogram = Counter()
    for selector in range(4):
        for z in range(1,7):
            bits = Bits([selector,z-1])
            result = run(7, 2, ((1,),(0,),(0,)), attempt_cap=1, bit_source=bits)
            assert result["status"] == "VERIFIED"
            assert result["sample_uniform_calls"] == (1 if selector == 0 else 2)
            assert result["weights"][2] == (z if selector else 0)
            histogram[result["power_vector"][2]] += 1
    assert histogram == {0:6, 1:6, 2:6, 4:6}


def test_bad_bank_attempt_cap_is_not_a_failure_bits_promise():
    result = run(5, 4, ((1,),(1,),(1,)), attempt_cap=7, failure_bits=40, bit_source=Bits())
    assert result["reason"] == "ATTEMPT_CAP"
    assert result["attempts"] == result["completed_candidates"] == result["nonpower_rejections"] == 7
    assert result["sample_uniform_calls"] == 7
    assert result["root_calls_started"] == 0
    assert result["budget"]["bad_bank_upper"] == 1
    assert result["budget"]["auxiliary_abort_upper"] <= Fraction(1,2**40)


def test_bit_cap_during_first_and_second_suffix_draw():
    first = run(5, 2, ((1,),(0,),(0,)), bit_source=Bits(tail="ones"))
    assert first["reason"] == "BIT_REJECTION_CAP"
    assert first["sample_uniform_calls"] == 1 and first["completed_candidates"] == 0
    assert first["bit_draws"] == first["budget"]["integer_rejection_cap"]
    second = run(7, 2, ((1,),(0,),(0,)), bit_source=Bits([1],tail="ones"))
    assert second["reason"] == "BIT_REJECTION_CAP"
    assert second["sample_uniform_calls"] == 2 and second["completed_candidates"] == 0
    assert second["bit_draws"] == 1+second["budget"]["integer_rejection_cap"]


def test_root_split_cap_counts_every_returned_trial():
    result = run(bit_source=Bits())
    b = result["budget"]
    assert result["reason"] == "ROOT_SPLIT_CAP"
    assert result["root_calls_started"] == result["root_calls_completed"] == 1
    assert result["root_split_trials"] == b["root_split_attempt_cap"]
    assert result["root_uniform_calls"] == 2*b["root_split_attempt_cap"]
    assert result["root_split_counts_complete"]


def test_interrupted_root_draw_has_exact_bits_and_fully_charged_cap():
    result = run(bit_source=Bits(tail="ones"))
    b = result["budget"]
    assert result["reason"] == "BIT_REJECTION_CAP"
    assert result["root_calls_started"] == 1 and result["root_calls_completed"] == 0
    assert result["root_uniform_calls"] == 1
    assert result["bit_draws"] == b["integer_rejection_cap"]
    assert result["random_bits"] == 3*b["integer_rejection_cap"]
    assert result["root_uniform_call_cap_charged"] == b["root_uniform_calls_per_call_cap"]
    assert result["root_split_trials"] is None and result["root_proper_splits"] is None


def test_second_root_interruption_never_returns_partial_witness():
    result = run(bank=((1,0),(0,1),(4,4)), pilot_count=2, rank_bound=2,
                 bit_source=Bits([2,1],tail="ones"))
    assert result["reason"] == "BIT_REJECTION_CAP"
    assert result["root_calls_started"] == 2 and result["root_calls_completed"] == 1
    assert result["completed_root_split_trials"] == 1
    assert result["root_uniform_calls"] == 3
    assert result["root_split_trials"] is None and result["weights"] is None


@pytest.mark.parametrize("p,e,R,N,ell,K,bits", [
    (5,2,1,2,3,9,4), (7,3,2,3,4,19,12), (13,6,3,4,1,1,32),
    (5,3,2,2,2,500,8), (5,4,0,1,1,2,3), (2**127-1,12,2,4,5,100,20)])
def test_exact_budget_formulas_and_source_failure_separation(p,e,R,N,ell,K,bits):
    b = solver.pivot_power_budget(p,e,N+ell,pilot_count=N,rank_bound=R,
                                  attempt_cap=K,failure_bits=bits)
    d = b["d"]
    roots = R if R and d > 1 else 0
    assert b["root_call_cap"] == roots
    assert b["sample_uniform_call_cap"] == (2*(ell-1)*K if roots else 0)
    assert b["root_uniform_calls_per_call_cap"] == (b["root_split_attempt_cap"]*(d*(d+1)//2-1) if roots else 0)
    assert b["root_uniform_call_cap"] == roots*b["root_uniform_calls_per_call_cap"]
    assert b["uniform_call_cap"] == b["sample_uniform_call_cap"]+b["root_uniform_call_cap"]
    assert b["auxiliary_abort_upper"] == b["root_abort_upper"]+b["bit_abort_upper"]
    assert b["auxiliary_abort_upper"] <= Fraction(1,2**bits)
    assert not b["attempt_exhaustion_in_auxiliary_bound"]
    assert not b["bad_bank_failure_in_auxiliary_bound"]
    assert b["good_bank_attempt_failure_bound"] == {
        "base": 1-b["fixed_good_bank_density_lower"], "exponent": K}


def test_rank_bound_probability_terms_are_conservative():
    for p,e in [(3,2),(5,4),(7,3),(13,6)]:
        for R in range(1,5):
            b = solver.pivot_power_budget(p,e,R+5,pilot_count=R+1,rank_bound=R,attempt_cap=2)
            for a in range(R+1):
                actual = solver.pivot_conditional_moments(p,e,a,4)
                assert actual["tail_bad_bank_upper"] <= b["tail_bad_bank_upper"]
                assert actual["fixed_good_bank_density_lower"] >= b["fixed_good_bank_density_lower"]


def test_budget_does_not_expand_attempt_failure_power():
    b = solver.pivot_power_budget(5,2,4,pilot_count=2,rank_bound=1,attempt_cap=10**100)
    assert b["good_bank_attempt_failure_bound"]["exponent"] == 10**100
    assert b["integer_rejection_cap"] < 400


@pytest.mark.parametrize("patch", [dict(p=2),dict(p=True),dict(e=0),dict(e=True),
                                    dict(pilot_count=0),dict(pilot_count=2),dict(rank_bound=2),
                                    dict(rank_bound=-1),dict(attempt_cap=0),dict(attempt_cap=True),
                                    dict(failure_bits=0),dict(bit_source=object()),dict(bit_source=Bits),
                                    dict(columns=[]),dict(columns=[[1],[0,1]]),
                                    dict(columns=[[5],[0]]),dict(columns=[[True],[0]]),
                                    dict(columns=iter([[1],[4]]))])
def test_invalid_inputs_are_not_statistical_aborts(patch):
    args = dict(p=5,e=2,columns=[(1,),(4,)],pilot_count=1,rank_bound=1,
                attempt_cap=2,failure_bits=8,bit_source=Bits())
    args.update(patch)
    with pytest.raises(ValueError):
        solver.pivot_power_sde(**args)


def test_attempt_cap_is_mandatory():
    with pytest.raises(TypeError):
        solver.pivot_power_sde(5,2,[(1,),(4,)],pilot_count=1,rank_bound=1)


@pytest.mark.parametrize("value", [-1,8,True,0.5])
def test_malformed_bit_source_propagates(value):
    with pytest.raises(ValueError):
        run(bit_source=Bits(tail=value))


def test_backend_errors_invalid_roots_and_accounting_propagate(monkeypatch):
    def broken(*args,**kwargs):
        raise RuntimeError("backend failed")
    monkeypatch.setattr(solver,"bounded_power_root",broken)
    with pytest.raises(RuntimeError,match="backend failed"):
        run()
    monkeypatch.setattr(solver,"bounded_power_root",lambda *a,**k: BoundedPowerRoot(2,0,0,0,Fraction(0)))
    with pytest.raises(ArithmeticError,match="invalid root"):
        run()
    monkeypatch.setattr(solver,"bounded_power_root",lambda *a,**k: BoundedPowerRoot(1,0,0,1,Fraction(0)))
    with pytest.raises(ArithmeticError,match="accounting"):
        run()


def test_broken_coordinate_or_lift_backend_is_detected(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(solver,"_fmpz_solve_coordinates",lambda *a: (0,))
        with pytest.raises(ArithmeticError,match="ambient pilot"):
            run()
    monkeypatch.setattr(solver,"bezout_reduced_exponent",lambda *a: (2,0))
    with pytest.raises(ArithmeticError,match="original-exponent"):
        run(bank=((1,),(1,)))


def test_original_ambient_verifier_is_mandatory(monkeypatch):
    calls = []
    original = solver.verify_general_degree_witness
    def checked(p,columns,weights,e):
        calls.append((columns,e))
        original(p,columns,weights,e)
    monkeypatch.setattr(solver,"verify_general_degree_witness",checked)
    result = run(7,4,((1,2,3),(5,3,1)))
    assert result["status"] == "VERIFIED" and result["d"] == 2
    assert calls == [(result["columns"],4)]
    assert result["lift_exponent"] == 2


def test_large_prime_original_degree_and_no_field_sized_loops(monkeypatch):
    def guarded_range(*args):
        result = range(*args)
        assert len(result) < 10000, "field-sized loop"
        return result
    monkeypatch.setattr(solver,"range",guarded_range,raising=False)
    p = 2**127-1
    v = (1,7,23)
    result = run(p,12,(v,tuple(-pow(2,6,p)*x%p for x in v)))
    assert result["status"] == "VERIFIED" and result["d"] == 6
    assert result["root_calls_started"] == 1
    assert result["sample_uniform_calls"] == 0


def test_prime_field_witness_need_not_be_regular_for_mixed_order_lifting():
    result = run(5,2,((1,0),(0,1),(1,0)),pilot_count=2,rank_bound=2)
    assert result["status"] == "VERIFIED"
    assert result["power_vector"] == (4,0,1)
    assert result["weights"][1] == 0
    assert result["prime_field_only"] and result["regularity_not_guaranteed"]
    assert result["budget"]["regularity_not_guaranteed"]
    active = [col for s,col in zip(result["weights"],result["columns"]) if s]
    assert active == [(1,0),(1,0)]
    # Over Z/25, suffix (1,5) has the same residue. Frozen second pilot
    # coefficient zero leaves 5*suffix_scale**2 != 0 for every unit scale.
    assert all(5*s*s % 25 != 0 for s in range(25) if s % 5)


def test_root_backend_cannot_borrow_unused_sampling_allowance(monkeypatch):
    def overuse(p,d,value,*,rng,split_attempt_cap):
        for _ in range(split_attempt_cap*(d*(d+1)//2-1)+1):
            rng.randrange(0,p)
        return BoundedPowerRoot(1,0,0,0,Fraction(0))
    monkeypatch.setattr(solver,"bounded_power_root",overuse)
    with pytest.raises(ArithmeticError,match="uniform draw cap"):
        run(bank=((1,),(4,),(0,)),attempt_cap=100,bit_source=Bits())


def test_live_report_replays_all_original_ambient_equations():
    report = solver.pivot_power_report()
    for result in report["cases"]:
        assert_counts(result)
    assert [row["status"] for row in report["cases"]] == ["VERIFIED"]*4+["ABORT"]
    for result in report["cases"][:4]:
        assert_witness(result)
    assert report["cases"][-1]["reason"] == "ATTEMPT_CAP"
    assert not report["new_all_prime_coverage_claim"]


def test_stored_artifact_matches_fresh_canonical_report_and_source_hashes():
    root = Path(__file__).resolve().parents[1]
    stored = json.loads((root/"research/classical_baselines/pivot_power_sde.json").read_text())
    fresh = solver.pivot_power_report()
    sources = (
        "theorems/pivot_power_sde.py", "tests/test_pivot_power_sde.py",
        "research/PIVOT_POWER_SDE.md", "theorems/bounded_power_roots.py",
        "theorems/power_sde_budget.py", "theorems/symbolic_scalar_phase_erasure.py",
        "theorems/weighted_two_erasure_cascade.py",
    )
    fresh["source_sha256"] = {
        name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in sources
    }
    # Frozen checkpoint metadata, not a count inferred from this one test.
    fresh["verification"] = {
        "connected_tests_passed": 261, "full_repository_suite": False,
        "quantum_execution": False, "exhaustive_moment_matrices": 136852,
    }
    def canonical(value):
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True, allow_nan=False, default=str)
    assert canonical(stored) == canonical(fresh)
