"""Paid fresh-pilot policies and the ambient verification boundary."""
from fractions import Fraction
import random

import pytest

from theorems.pilot_module_descent import pilot_module_episode, pilot_module_search, report


def scripted(blocks):
    stream = iter(blocks)
    calls = []
    def draw(count):
        calls.append(count)
        return next(stream)
    return draw,calls


def assert_ambient_witness(episode):
    assert episode["status"]=="VERIFIED_AMBIENT_MODULE_WITNESS"
    p,d,es = episode["prime"],episode["degree"],episode["ambient_exponents"]
    raw,weights = episode["selected_ambient_columns"],episode["scales"]
    assert any(weights) and all(w==0 or w%p for w in weights)
    assert all(sum(c[j]*pow(w,d,p**e) for c,w in zip(raw,weights))%p**e==0 for j,e in enumerate(es))
    assert episode["source_labels_consumed"]==sum(t["count"] for t in episode["requests"])
    assert episode["source_labels_consumed"]<=episode["ambient_plan"]["predecessors_per_episode_upper"]
    assert not episode["hidden_support_completeness_certified"]
    assert not episode["physical_pilot_measurements_executed"]
    assert not episode["quantum_receiver_executed"]


def test_incomplete_pilot_frame_can_accept_a_correct_original_ambient_witness():
    # These labels could be a low-probability transcript from C=Z/9;
    # correctness does not require claiming that the pilots generated C.
    episode = pilot_module_episode(prime=3,ambient_exponents=(2,),degree=2,
        draw_labels=lambda count:[(3,)]*count,bit_source=random.Random(1))
    assert_ambient_witness(episode)
    assert episode["frame"]["intrinsic_exponents"]==(1,)
    assert episode["source_labels_consumed"]==11


def test_nonmember_charges_entire_requested_block_then_aborts():
    draw,calls = scripted([[(3,)]*3,[(1,),(3,)]])
    result = pilot_module_episode(prime=3,ambient_exponents=(2,),degree=2,draw_labels=draw)
    assert result["status"]=="ABORT" and calls==[3,2]
    assert result["source_labels_consumed"]==5
    assert result["requests"][-1]["intrinsic_columns"]==[None,(1,)]
    assert "outside" in result["reason"] and "scales" not in result


def test_retry_refreshes_pilots_not_just_the_bank():
    draw,calls = scripted([[(0,)]*3,[(3,)],[(3,)]*3]+[[(3,)]*2]*4)
    result = pilot_module_search(prime=3,ambient_exponents=(2,),degree=2,
        draw_labels=draw,bit_source=random.Random(1),episode_cap=2)
    assert result["status"]=="VERIFIED_AMBIENT_MODULE_WITNESS"
    assert calls==[3,1,3,2,2,2,2]
    assert result["source_labels_consumed"]==15 and result["successful_episode_index"]==1
    assert result["episodes"][0]["frame"]["intrinsic_exponents"]==()
    assert result["episodes"][1]["frame"]["intrinsic_exponents"]==(1,)
    assert Fraction(*result["conditional_all_episodes_abort_upper"])==Fraction(9,256)
    assert_ambient_witness(result["episodes"][1])


def test_zero_rank_pilots_need_one_fresh_zero_label():
    result = pilot_module_episode(prime=3,ambient_exponents=(2,3),degree=2,
                                  draw_labels=lambda count:[(0,0)]*count)
    assert_ambient_witness(result)
    assert result["zero_rank_branch"] and result["scales"]==[1]
    assert result["source_labels_consumed"]==5


def test_valid_negative_determinant_pilot_frame_does_not_break_availability():
    pilots = [(1,4),(1,1)]
    rng = random.Random(29)
    first = True
    def draw(count):
        nonlocal first
        if first:
            first = False
            assert count==4
            return pilots+[(0,0)]*2
        result = []
        for _ in range(count):
            a,b = rng.randrange(27),rng.randrange(27)
            result.append(((a+b)%27,(4*a+b)%9))
        return result
    result = pilot_module_episode(prime=3,ambient_exponents=(3,2),degree=2,
                                  draw_labels=draw,bit_source=random.Random(1))
    assert_ambient_witness(result)


def test_capped_repeated_rank_failure_retains_all_charges():
    calls = []
    def draw(count):
        calls.append(count)
        return [(1,0),(0,1),(1,0),(0,1)] if count==4 else [(1,0)]*count
    result = pilot_module_search(prime=3,ambient_exponents=(2,3),degree=2,
                                 draw_labels=draw,failure_bits=4,episode_cap=2)
    assert result["status"]=="ABORT" and len(result["episodes"])==2
    assert result["source_labels_consumed"]==sum(calls)
    assert calls.count(4)==2
    for episode in result["episodes"]:
        assert episode["intrinsic_run"]["status"]=="ABORT"
        assert episode["source_labels_consumed"]==4+3*episode["intrinsic_run"]["plan"]["attempts_per_atom"]


@pytest.mark.parametrize("damage",["scales","raw_columns"])
def test_ambient_boundary_rejects_corrupt_intrinsic_output(monkeypatch,damage):
    import theorems.pilot_module_descent as module
    real = module.spanning_module_witness
    def damaged(*args,**kwargs):
        value = real(*args,**kwargs)
        if damage=="scales":
            scales = value["lift"]["scales"]
            scales[next(i for i,x in enumerate(scales) if x)] = 0
        else:
            value["raw_columns"][0] = (2,)
        return value
    monkeypatch.setattr(module,"spanning_module_witness",damaged)
    with pytest.raises(ArithmeticError,match="ambient"):
        pilot_module_episode(prime=3,ambient_exponents=(2,),degree=2,
            draw_labels=lambda count:[(3,)]*count,bit_source=random.Random(1))


@pytest.mark.parametrize("p,d,rng",[(5,4,None),(7,3,object())])
def test_backend_and_rng_preflight_happen_before_pilots(p,d,rng):
    def forbidden(count):
        pytest.fail("invalid backend consumed pilot sources")
    with pytest.raises(ValueError):
        pilot_module_episode(prime=p,ambient_exponents=(2,),degree=d,draw_labels=forbidden,bit_source=rng)


def test_invalid_callback_count_is_not_statistical_abort():
    with pytest.raises(ValueError,match="count"):
        pilot_module_episode(prime=3,ambient_exponents=(2,),degree=2,draw_labels=lambda count:[(0,)])


def test_live_report_keeps_physical_and_classical_scope_explicit():
    value = report()
    assert not value["quantum_receiver_executed"] and not value["speedup_established"]
    assert not value["normal_form_backend_bit_complexity_certified"]
    for case in value["cases"]:
        result = case["result"]
        assert_ambient_witness(result["episodes"][result["successful_episode_index"]])
        assert result["source_labels_consumed"]<=result["source_labels_cap"]
