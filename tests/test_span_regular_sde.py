"""Raw-span arithmetic controls; aggregation is not quantum state synthesis."""
from fractions import Fraction
from itertools import product
import random
from types import SimpleNamespace

import pytest

from theorems.span_regular_sde import (
    expand_atom_witness, published_sde_arity, span_grade_plan, spanning_module_witness,
)


def test_exact_small_block_rank_law_and_biased_sum_distribution():
    counts = {}
    good = 0
    for entries in product(range(3),repeat=6):
        columns = [entries[i:i+2] for i in range(0,6,2)]
        spans = any((a[0]*b[1]-a[1]*b[0])%3 for i,a in enumerate(columns) for b in columns[i+1:])
        if spans:
            good += 1
            atom = tuple(sum(c[j] for c in columns)%3 for j in range(2))
            counts[atom] = counts.get(atom,0)+1
    assert good == 624
    assert Fraction(good,729) == (1-Fraction(1,27))*(1-Fraction(1,9))
    assert len(set(counts.values())) > 1  # Accepted atoms are NOT assumed IID uniform.


def test_lift_must_break_blockwise_equality_even_for_zero_atom():
    result = expand_atom_witness(prime=3,exponents=(2,),degree=2,
                                 blocks=[[(1,),(2,)]],atom_weights=[1])
    assert result["atoms"] == [(0,)]
    assert result["expanded_field_witness"] == [1,1]
    assert result["lift"]["scales"] == [4,1]
    assert all(3*s*s%9 for s in range(9) if s%3)


def test_zero_atom_rank_does_not_reduce_original_module_dimension():
    block = [(1,0),(0,1),(6,6)]
    result = spanning_module_witness(prime=7,degree=3,exponents=(2,3),
                                     draw_block=lambda width:block,bit_source=random.Random(1))
    assert result["status"] == "VERIFIED_SPANNING_MODULE_WITNESS"
    assert result["atom_equation_rank"] == 0
    assert result["lift"]["jacobian_rank"] == 2
    assert result["atom_weights"][0] == 1
    assert not any(result["atom_weights"][1:])
    assert not any(result["lift"]["scales"][3:])


@pytest.mark.parametrize("p,degree,rank", [(3,2,4),(7,3,3),(13,3,3),(1031,2,4),(2**128-275,12,2)])
def test_actual_backend_and_raw_mixed_moduli_without_large_field_wrapper_guard(p,degree,rank):
    exponents = tuple(1+i%4 for i in range(rank))
    labels = random.Random(2030)
    def draw(width):
        return [tuple(labels.randrange(p**e) for e in exponents) for _ in range(width)]
    result = spanning_module_witness(prime=p,degree=degree,exponents=exponents,
                                     draw_block=draw,bit_source=random.Random(3029))
    assert result["status"] == "VERIFIED_SPANNING_MODULE_WITNESS"
    plan = result["plan"]
    assert len(result["accepted_trial_indices"]) == plan["atom_count"]
    assert result["source_columns_consumed"] == len(result["trials"])*(rank+1)
    assert result["source_columns_consumed"] <= plan["raw_bank_sources_upper"]
    assert not plan["wrapper_adds_prime_size_guard"]
    assert Fraction(*plan["episode_abort_upper"]) <= Fraction(3,16)
    raw,weights = result["raw_columns"],result["lift"]["scales"]
    assert result["lift"]["jacobian_rank"] == rank
    assert any(weights) and all(w==0 or w%p for w in weights)
    assert all(sum(c[j]*pow(w,degree,p**e) for c,w in zip(raw,weights))%p**e==0
               for j,e in enumerate(exponents))
    assert not result["pilots_executed"] and not result["quantum_receiver_executed"]


def test_full_rank_fixed_blocks_can_work_where_random_kernel_method_always_fails():
    columns = [(1,0),(0,1),(0,0)]
    result = spanning_module_witness(prime=3,degree=1,exponents=(2,3),
        draw_block=lambda width:columns,bit_source=random.Random(1))
    assert result["status"] == "VERIFIED_SPANNING_MODULE_WITNESS"
    assert result["lift"]["jacobian_rank"] == 2


def test_rank_failure_consumes_whole_blocks_and_stops_at_declared_cap():
    calls = []
    def draw(width):
        calls.append(width)
        return [(1,0)]*width
    result = spanning_module_witness(prime=3,degree=2,exponents=(2,3),draw_block=draw,failure_bits=4)
    assert result["status"] == "ABORT"
    assert len(calls) == result["plan"]["attempts_per_atom"]
    assert result["source_columns_consumed"] == sum(calls)
    assert all(t["status"] == "RAW_RANK_REJECT" for t in result["trials"])
    assert not result["accepted_trial_indices"]


def test_declared_field_abort_does_not_hide_backend_failure_or_resample(monkeypatch):
    import theorems.span_regular_sde as module
    calls = []
    def draw(width):
        calls.append(width)
        return [(1,0),(0,1),(6,6)]
    def abort(*args,**kwargs):
        raise RuntimeError("bounded ternary cubic curve sampler exhausted")
    monkeypatch.setattr(module,"solve_bezout_sde_weights",abort)
    result = spanning_module_witness(prime=7,degree=3,exponents=(2,2),draw_block=draw)
    assert result["status"] == "ABORT" and len(calls) == result["plan"]["atom_count"]
    def broken(*args,**kwargs):
        raise RuntimeError("unexpected backend failure")
    monkeypatch.setattr(module,"solve_bezout_sde_weights",broken)
    with pytest.raises(RuntimeError,match="unexpected"):
        spanning_module_witness(prime=7,degree=3,exponents=(2,2),draw_block=draw)


def test_published_arity_is_theorem_bound_not_fake_implemented_backend():
    assert published_sde_arity(2,4) == (4**6*3**4)**3
    assert published_sde_arity(2,1) == 3 and published_sde_arity(0,4) == 1
    for degree in (1,2,3,4):
        assert all(published_sde_arity(r,degree) < published_sde_arity(r+1,degree) for r in range(1,8))
    plan = span_grade_plan(prime=5,cyclic_rank=2,degree=4,published_bound=True)
    assert plan["status"] == "IMPORTED_SDE_BOUND_ONLY"
    assert not plan["field_backend_implemented"] and not plan["field_randomness_fully_capped"]
    with pytest.raises(ValueError,match="even reduced"):
        span_grade_plan(prime=5,cyclic_rank=2,degree=4)
    with pytest.raises(ValueError,match="even reduced"):
        span_grade_plan(prime=5,cyclic_rank=2,degree=2)


def test_ambient_rank_prices_pilots_and_uniform_episode_cap():
    plan = span_grade_plan(prime=7,cyclic_rank=2,ambient_cyclic_rank=10,degree=3)
    assert plan["pilot_sources"] == 12 and plan["raw_block_width"] == 3
    assert plan["predecessors_per_episode_upper"] > 12+plan["raw_bank_sources_upper"]
    with pytest.raises(ValueError,match="ambient"):
        span_grade_plan(prime=7,cyclic_rank=2,ambient_cyclic_rank=1,degree=3)


@pytest.mark.parametrize("block,weights", [([(1,0),(2,0),(3,0)],[1]),
                                          ([(1,0),(0,1),(6,6)],[0]),
                                          ([(1,0),(0,1)],[1]),
                                          ([(1,0),(0,1),(1,1)],[1])])
def test_bad_raw_span_zero_witness_wrong_width_or_bad_atom_rejected(block,weights):
    with pytest.raises((ValueError,ArithmeticError)):
        expand_atom_witness(prime=7,exponents=(2,3),degree=3,blocks=[block],atom_weights=weights)


def test_unsupported_field_backend_fails_before_consuming_any_source():
    def forbidden(width):
        pytest.fail("unsupported backend consumed raw sources")
    with pytest.raises(ValueError):
        spanning_module_witness(prime=5,degree=4,exponents=(2,3),draw_block=forbidden)


@pytest.mark.parametrize("p,degree,provided,required", [
    (7,3,"getrandbits","randrange"), (1031,2,"randrange","getrandbits"),
])
def test_wrong_rng_protocol_rejected_before_any_source_consumption(p,degree,provided,required):
    rng = random.Random(29)
    source = SimpleNamespace(**{provided:getattr(rng,provided)})
    def forbidden(width):
        pytest.fail("invalid randomness provider consumed raw sources")
    with pytest.raises(ValueError,match=required):
        spanning_module_witness(prime=p,degree=degree,exponents=(2,),
                                 draw_block=forbidden,bit_source=source)


@pytest.mark.parametrize("p,degree,protocol", [(7,3,"randrange"),(1031,2,"getrandbits")])
def test_selected_rng_protocol_alone_is_sufficient(p,degree,protocol):
    rng = random.Random(29)
    source = SimpleNamespace(**{protocol:getattr(rng,protocol)})
    result = spanning_module_witness(prime=p,degree=degree,exponents=(2,),
                                     draw_block=lambda width:[(1,)]*width,bit_source=source)
    assert result["status"] == "VERIFIED_SPANNING_MODULE_WITNESS"


def test_linear_reduction_does_not_require_randomness_protocol():
    result = spanning_module_witness(prime=3,degree=1,exponents=(2,),
        draw_block=lambda width:[(1,)]*width,bit_source=object())
    assert result["status"] == "VERIFIED_SPANNING_MODULE_WITNESS"
