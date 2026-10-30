"""Intrinsic/ambient cancellation checks; never physical-source certification."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import random

import pytest

from theorems import unit_power_module as module
from theorems.prime_power_rees_descent import verify_module_witness


def test_original_degree_bezout_conversion_precedes_hensel(monkeypatch):
    # (1,2) solves x^2+5y^2=0 mod7, but NOT x^4+5y^4=0.
    monkeypatch.setattr(module, "random_column_power_sde",
                        lambda *a, **k: {"status": "VERIFIED", "weights": (1, 2)})
    result = module.unit_module_witness([(1,), (5,)], prime=7, exponents=(3,),
                                        degree=4, attempt_cap=1)
    assert result["reduced_degree"] == 2 and result["bezout_exponent"] == 2
    assert result["field_witness_original_degree"] == [1, 4]
    assert result["lift"]["jacobian_rank"] == 1 and result["lift"]["lift_steps"] == 2
    assert verify_module_witness([(1,), (5,)], result["scales"],
                                 prime=7, exponents=(3,), degree=4)
    assert all(s % 7 for s in result["scales"])


def test_intrinsic_rank_deficiency_aborts_without_random_trials(monkeypatch):
    monkeypatch.setattr(module, "random_column_power_sde",
                        lambda *a, **k: pytest.fail("rank-deficient bank entered sampler"))
    result = module.unit_module_witness([(7,)]*3, prime=7, exponents=(2,), degree=2,
                                        attempt_cap=1)
    assert result["status"] == "ABORT"
    assert result["reason"] == "INTRINSIC_RESIDUE_RANK_DEFICIENT"
    assert result["scales"] is None and not result["labels_resampled"]


def test_full_rank_fixed_bank_can_have_no_unit_solution():
    result = module.unit_module_witness([(1,), (0,), (0,)], prime=7,
                                        exponents=(2,), degree=2, attempt_cap=32,
                                        bit_source=random.Random(4))
    assert result["status"] == "ABORT" and result["reason"] == "ATTEMPT_CAP"
    assert result["field_run"]["attempts"] == 32
    assert result["scales"] is None


def _scripted_episode(pilots, bank, *, p=101, es=(3,), degree=2, u=2):
    requests = []
    stream = iter((pilots, bank))
    def draw(count):
        requests.append(count)
        return next(stream)
    result = module.unit_pilot_episode(prime=p, ambient_exponents=es, degree=degree,
                                       uniform_parameter=u, draw_labels=draw,
                                       attempt_cap=32768, failure_bits=20,
                                       bit_source=random.Random(5102))
    assert requests == [4*u, 4*u]
    assert result["source_labels_consumed"] == 8*u
    return result


def test_incomplete_frame_nonmember_aborts_and_charges_both_banks():
    result = _scripted_episode([(101**2,)]*8, [(101,)]*8)
    assert result["status"] == "ABORT" and result["reason"] == "OUTSIDE_PILOT_FRAME"
    assert not result["hidden_support_completeness_certified"]


def test_incomplete_frame_can_safely_accept_without_claiming_completeness():
    result = _scripted_episode([(101**2,)]*8, [(101**2,)]*7+[(94*101**2,)])
    assert result["status"] == "VERIFIED_AMBIENT_UNIT_WITNESS"
    assert result["original_ambient_verified"]
    assert all(s % 101 for s in result["scales"])
    assert not result["hidden_support_completeness_certified"]
    assert not result["plan"]["recommended_cap_met"]
    assert result["plan"]["episode_abort_bound"] == 1
    assert result["selected_request_indices"] == [1]


@pytest.mark.parametrize("bank,expected", [([(0,)]*8, "VERIFIED_AMBIENT_UNIT_WITNESS"),
                                         ([(0,)]*7+[(101,)], "ABORT")])
def test_zero_pilots_need_a_fresh_zero_bank(bank, expected):
    result = _scripted_episode([(0,)]*8, bank)
    assert result["status"] == expected
    if expected != "ABORT":
        assert result["scales"] == [1]*8 and result["zero_rank_branch"]
    else:
        assert result["reason"] == "OUTSIDE_PILOT_FRAME"


def test_complete_frame_but_bad_bank_has_explicit_rank_abort():
    result = _scripted_episode([(101,)]*8, [(101**2,)]*8)
    assert result["status"] == "ABORT"
    assert result["reason"] == "INTRINSIC_RESIDUE_RANK_DEFICIENT"


@pytest.mark.parametrize("changes", [
    {"uniform_parameter": 1}, {"uniform_parameter": True}, {"degree": 101},
    {"attempt_cap": 0}, {"attempt_cap": True}, {"failure_bits": 0},
    {"bit_source": object()}, {"bit_source": random.Random}, {"ambient_exponents": ()},
])
def test_preflight_rejects_before_acquiring_labels(changes):
    args = dict(prime=101, ambient_exponents=(3,), degree=2, uniform_parameter=2,
                draw_labels=lambda count: pytest.fail("labels acquired"), attempt_cap=1,
                bit_source=random.Random(1))
    args.update(changes)
    with pytest.raises(ValueError):
        module.unit_pilot_episode(**args)


def test_backend_corruption_is_not_a_statistical_abort(monkeypatch):
    monkeypatch.setattr(module, "random_column_power_sde",
                        lambda *a, **k: {"status": "VERIFIED", "weights": (1, 0)})
    with pytest.raises(ArithmeticError, match="lost a coordinate"):
        module.unit_module_witness([(1,), (6,)], prime=7, exponents=(2,), degree=2,
                                    attempt_cap=1)


@pytest.mark.parametrize("p", [3, 5, 7])
def test_original_degree_divisible_by_characteristic_blocks_unit_lifting(p):
    # Every nonzero (x,x) solves the residue equation, but a unit lift
    # would require z^p=1-p mod p^2. Enumerate only this tiny falsifier.
    assert all((pow(x, p, p)+(p-1)*pow(x, p, p)) % p == 0 for x in range(1, p))
    assert not any(pow(z, p, p*p) == (1-p) % (p*p)
                   for z in range(1, p*p) if z % p)
    with pytest.raises(ValueError):
        module.unit_module_witness([(1,), (p-1,)], prime=p,
                                    exponents=(2,), degree=p, attempt_cap=10)


@pytest.mark.parametrize("E", [2, 3, 4, 5])
def test_rank_one_derived_module_does_not_bound_ring_nilpotency_class(E):
    # L=(Z/7^E)^2, [x,y]=7y: gamma_j is generated by 7^(j-1)y.
    p, modulus = 7, 7**E
    generator = p
    nonzero_terms = 0
    while generator % modulus:
        nonzero_terms += 1
        generator = generator*p % modulus
    assert nonzero_terms == E-1
    assert p**(E-1) % modulus and p**E % modulus == 0
    assert E < p


@pytest.mark.parametrize("u", range(2, 11))
def test_paid_pilot_tree_bound_and_independent_failure_sum(u):
    p, c, rank = 65537, u, u-1
    result = module.unit_tree_source_bound(prime=p, class_bound=c,
                                           cyclic_rank_bound=rank, uniform_parameter=u)
    width, leaves = 8*u, (8*u)**(c-1)
    bits = (64*leaves-1).bit_length()
    assert result["leaves_per_output_tree"] == leaves
    assert result["raw_arity_per_grade"] == width
    bank_pilot = failure = Fraction(0)
    for stage in result["stages"]:
        plan, nodes = stage["plan"], stage["nodes"]
        assert nodes == width**(stage["grade"]-2)
        assert plan["pilot_source_count"] == plan["bank_source_count"] == 4*u
        pilot = Fraction(1, (p-1)*p**(4*u-rank))
        d = plan["reduced_degree"]
        mean = Fraction(((p-1)//d)**(4*u-1), p**rank)
        bad = 4/mean+Fraction(2, p**(4*u-rank))
        assert plan["pilot_incompleteness_bound"] == pilot
        assert plan["iid_bad_bank_bound"] == bad
        assert plan["kernel_trial_cap"] == 2*(2*d)**(4*u)*bits
        assert plan["kernel_exhaustion_bound"] == Fraction(1, 2**bits)
        assert plan["recommended_cap_met"]
        bank_pilot += nodes*(pilot+bad)
        failure += nodes*(pilot+bad+plan["kernel_exhaustion_bound"]+
                          plan["auxiliary_arithmetic_abort_bound"])
    assert result["bank_and_pilot_failure_bound"] == bank_pilot <= Fraction(1, 64)
    assert result["tree_abort_bound"] == failure <= Fraction(1, 16)
    for flag in ("quantum_receiver_implemented", "all_prime_ring_hsp_bound",
                 "complete_quantum_error_accounting_included", "class_bounded_by_derived_cyclic_rank",
                 "original_oracle_queries_included"):
        assert result[flag] is False


def test_report_executes_mixed_order_controls_and_binds_sources():
    payload = module.report()
    assert len(payload["cases"]) == 2
    for case in payload["cases"]:
        result = case["result"]
        assert result["status"] == "VERIFIED_AMBIENT_UNIT_WITNESS"
        assert result["original_ambient_verified"]
        p, degree = result["plan"]["prime"], result["plan"]["degree"]
        es = (3,) if case["name"] == "ambient_mod_p_zero" else (2, 3)
        assert verify_module_witness(result["selected_ambient_columns"], result["scales"],
                                     prime=p, exponents=es, degree=degree)
        assert all(s % p for s in result["scales"])
        assert result["source_labels_consumed"] == result["plan"]["source_labels_cap"]
        assert not result["plan"]["recommended_cap_met"]
        assert not result["physical_iid_source_certified"]
    root = Path(__file__).resolve().parents[1]
    for name, digest in payload["source_sha256"].items():
        assert sha256((root/name).read_bytes()).hexdigest() == digest
    assert payload["tree"]["leaves_per_output_tree"] == 576
    assert not payload["all_prime_ring_hsp_bound"] and not payload["speedup_claim_allowed"]
