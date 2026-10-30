"""Joint-law, bounded-rejection and exact ring controls, not HSP instances."""
from fractions import Fraction
from itertools import product
import random

import pytest

from theorems.random_regular_sde import (
    kernel_block_success_probability, random_kernel_plan, random_kernel_trial,
    random_regular_module_witness,
)


def independent_rank(columns, rows, p):
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns)]
    pivot = 0
    for col in range(len(columns)):
        found = next((j for j in range(pivot, rows) if matrix[j][col] % p), None)
        if found is None:
            continue
        matrix[pivot], matrix[found] = matrix[found], matrix[pivot]
        inverse = pow(matrix[pivot][col] % p, -1, p)
        matrix[pivot] = [a*inverse % p for a in matrix[pivot]]
        for j in range(pivot+1, rows):
            scale = matrix[j][col]
            matrix[j] = [(a-scale*b) % p for a,b in zip(matrix[j],matrix[pivot])]
        pivot += 1
        if pivot == rows:
            break
    return pivot


@pytest.mark.parametrize("p,rank,width", [(3,1,3), (3,1,4), (3,2,3), (5,1,3)])
def test_joint_probability_matches_exhaustive_matrix_kernel_count(p, rank, width):
    good = 0
    for entries in product(range(p), repeat=rank*width):
        columns = [entries[i*rank:(i+1)*rank] for i in range(width)]
        if independent_rank(columns,rank,p) != rank:
            continue
        for relation in product(range(p), repeat=width):
            if any(sum(a*col[j] for a,col in zip(relation,columns)) % p for j in range(rank)):
                continue
            active = [col for a,col in zip(relation,columns) if a]
            good += independent_rank(active,rank,p) == rank
    # Rank-deficient matrices are charged and rejected; they are not
    # conditioned out of this denominator.
    assert Fraction(good, p**(rank*width+width-rank)) == kernel_block_success_probability(p,rank,width)


@pytest.mark.parametrize("p", [3,5,7,1031])
@pytest.mark.parametrize("rank", [1,2,5,16])
def test_uniform_constant_success_bound_has_no_rank_prime_guard(p,rank):
    exact = kernel_block_success_probability(p,rank)
    lower = (1-Fraction(2,p))*(1-Fraction(1,p*(p-1)))
    assert exact >= lower >= Fraction(5,18) > Fraction(1,4)


def test_fixed_full_rank_matrix_can_fail_every_random_kernel_trial():
    columns = [(1,0), (0,1), (0,0), (0,0), (0,0), (0,0)]
    for seed in range(20):
        result = random_kernel_trial(3,columns,rng=random.Random(seed))
        assert result["matrix_rank"] == 2 and result["active_rank"] == 0
        assert result["status"] == "ACTIVE_RANK_REJECT"


def test_rank_deficient_trial_uses_no_randomness():
    result = random_kernel_trial(3,[(1,0)]*6,rng=object())
    assert result["status"] == "MATRIX_RANK_REJECT" and result["uniform_calls"] == 0


@pytest.mark.parametrize("p,rank,degree", [(3,3,1), (1031,16,2), (105037,4,3), (2**128-275,2,12)])
def test_capped_random_blocks_preserve_original_degree_and_mixed_moduli(monkeypatch,p,rank,degree):
    import theorems.power_sde as core
    old_relation = core._relation
    field_calls = []
    def second_level_only(prime,columns):
        field_calls.append(len(columns))
        assert len(columns) == plan["required_blocks"]
        return old_relation(prime,columns)
    monkeypatch.setattr(core,"_relation",second_level_only)
    monkeypatch.setattr(core,"_field_root",lambda *args: pytest.fail("uncapped root backend"))
    plan = random_kernel_plan(prime=p,cyclic_rank=rank,degree=degree)
    exponents = tuple(1+i%4 for i in range(rank))
    label_rng = random.Random(29)
    draw_count = 0
    def draw(width):
        nonlocal draw_count
        draw_count += width
        return [tuple(label_rng.randrange(p**e) for e in exponents) for _ in range(width)]
    result = random_regular_module_witness(prime=p,exponents=exponents,degree=degree,
                                          draw_block=draw,bit_source=random.Random(2030))
    assert result["status"] == "VERIFIED_REGULAR_MODULE_WITNESS"
    assert draw_count == result["source_columns_consumed"] <= plan["bank_sources_upper"]
    assert not result["pilots_executed"] and not result["quantum_receiver_executed"]
    assert result["kernel_uniform_calls"] <= plan["kernel_uniform_call_cap"]
    assert result["kernel_random_bits"] <= plan["kernel_random_bit_cap"]
    assert Fraction(*plan["episode_abort_upper"]) <= Fraction(1,4)
    assert not plan["rank_dependent_prime_guard_required"]
    for index in result["accepted_trial_indices"]:
        record = result["trials"][index]
        active = [col for a,col in zip(record["relation"],record["columns"]) if a]
        assert independent_rank(active,rank,p) == rank
    columns, scales = result["selected_columns"], result["lift"]["scales"]
    assert any(scales) and all(s==0 or s%p for s in scales)
    assert all(sum(col[j]*pow(s,degree,p**e) for col,s in zip(columns,scales)) % p**e == 0
               for j,e in enumerate(exponents))
    if plan["reduced_degree"] > 1:
        assert field_calls == [plan["required_blocks"]]
        stats = result["symmetric_randomness"]
        assert stats["root_calls"] <= stats["root_call_cap"]
        assert stats["uniform_calls"] <= stats["uniform_call_cap"]
        assert stats["random_bits"] <= stats["random_bit_cap"]
        assert all(stats[key] == value for key,value in plan["symmetric_randomness_caps"].items())
    else:
        assert field_calls == [] and result["symmetric_randomness"] is None
        assert result["field_witness"] == result["trials"][result["accepted_trial_indices"][0]]["relation"]


def test_linear_branch_keeps_spanning_sample_instead_of_sparse_first_kernel_vector():
    from theorems.symbolic_scalar_phase_erasure import _fmpz_nullspace_basis
    columns = [(1,0),(1,0),(0,1),(0,1),(0,0),(0,0)]
    first = _fmpz_nullspace_basis(list(map(list,zip(*columns))),6,3)[0]
    assert independent_rank([col for a,col in zip(first,columns) if a],2,3) == 1
    class ConstantOneBits:
        def getrandbits(self,width):
            return 1
    result = random_regular_module_witness(prime=3,exponents=(2,2),degree=1,
        draw_block=lambda width: columns,bit_source=ConstantOneBits(),failure_bits=4)
    assert result["status"] == "VERIFIED_REGULAR_MODULE_WITNESS"
    assert result["lift"]["jacobian_rank"] == 2
    assert result["field_witness"] == result["trials"][0]["relation"] != first


def test_fixed_bad_source_aborts_and_charges_every_attempt_without_restarting():
    calls = []
    def draw(width):
        calls.append(width)
        return [(1,0),(0,1)]+[(0,0)]*(width-2)
    result = random_regular_module_witness(prime=3,exponents=(2,3),degree=1,
                                          draw_block=draw,bit_source=random.Random(1),failure_bits=4)
    assert result["status"] == "ABORT"
    assert len(calls) == result["plan"]["attempts_per_block"]
    assert result["source_columns_consumed"] == sum(calls)
    assert len(result["trials"]) == len(calls)
    assert all(r["status"] == "ACTIVE_RANK_REJECT" for r in result["trials"])
    assert not result["accepted_trial_indices"]


def test_pilots_and_episode_cost_use_fixed_ambient_rank_not_observed_rank():
    plan = random_kernel_plan(prime=1031,cyclic_rank=2,ambient_cyclic_rank=20,degree=2)
    assert plan["pilot_sources"] == 22
    assert plan["block_width"] == 6 and plan["required_blocks"] == 3
    assert plan["whole_episode_bank_sources_upper"] > plan["bank_sources_upper"]
    assert plan["predecessors_per_episode_upper"] == 22+plan["whole_episode_bank_sources_upper"]
    for ambient in (1,True):
        with pytest.raises(ValueError,match="ambient"):
            random_kernel_plan(prime=1031,cyclic_rank=2,ambient_cyclic_rank=ambient,degree=2)


class OnesBits:
    def getrandbits(self,width):
        return (1<<width)-1


def test_integer_rejection_abort_is_explicit_with_one_consumed_block():
    result = random_regular_module_witness(prime=3,exponents=(2,),degree=1,
        draw_block=lambda width: [(1,)]*width,bit_source=OnesBits(),failure_bits=4)
    assert result["status"] == "ABORT" and len(result["trials"]) == 1
    assert result["trials"][0]["status"] == "KERNEL_RANDOMNESS_ABORT"
    assert result["kernel_bit_draws"] == result["plan"]["kernel_integer_rejection_cap"]
    assert result["source_columns_consumed"] == result["plan"]["block_width"]


def test_supplied_relation_validation_and_wider_root_budget():
    from theorems.power_sde_budget import budgeted_power_weights, randomness_budget
    rank,degree,width,p = 2,2,6,1031
    budget = randomness_budget(rank,degree,8,first_level_width=width)
    assert budget.root_call_cap == 3*(width+2)+3
    assert budget.total_abort_bound <= Fraction(1,256)
    columns = ([(1,0),(0,1)]+[(0,0)]*4)*3
    for relations in ([[1]*6]*3, [[0]*6]*3, [[1]*5]*3, [[True]*6]*3, []):
        with pytest.raises(ValueError,match="relation"):
            budgeted_power_weights(p,degree,columns,first_level_width=width,
                                   first_level_relations=relations,bit_source=random.Random(1))
    with pytest.raises(ValueError,match="width"):
        randomness_budget(rank,degree,8,first_level_width=2)


@pytest.mark.parametrize("p,rank,degree,bits", [(9,2,1,4),(3,0,1,4),(3,2,3,4),
                                              (1031,2,3,3),(7,2,3,4)])
def test_invalid_contracts_and_degree_only_field_guard(p,rank,degree,bits):
    with pytest.raises(ValueError):
        random_kernel_plan(prime=p,cyclic_rank=rank,degree=degree,failure_bits=bits)


def test_malformed_source_and_uniform_output_fail_closed():
    with pytest.raises(ValueError,match="number of columns"):
        random_regular_module_witness(prime=3,exponents=(2,),degree=1,
                                      draw_block=lambda width:[(1,)],bit_source=random.Random(1))
    with pytest.raises(ValueError,match="canonical"):
        random_regular_module_witness(prime=3,exponents=(2,),degree=1,
                                      draw_block=lambda width:[(9,)]*width,bit_source=random.Random(1))
    class InvalidRandom:
        def randrange(self,start,stop):
            return True
    with pytest.raises(ValueError,match="noncanonical"):
        random_kernel_trial(3,[(1,)]*4,rng=InvalidRandom())


def test_backend_failure_is_not_reported_as_statistical_abort(monkeypatch):
    import theorems.random_regular_sde as module
    def broken(*args,**kwargs):
        raise RuntimeError("backend failure")
    monkeypatch.setattr(module,"_fmpz_rref",broken)
    with pytest.raises(RuntimeError,match="backend failure"):
        random_regular_module_witness(prime=3,exponents=(2,),degree=1,
            draw_block=lambda width:[(1,)]*width,bit_source=random.Random(1))
    import theorems.power_sde as core
    monkeypatch.setattr(core,"power_weights",broken)
    import theorems.power_sde_budget as budget
    monkeypatch.setattr(budget,"power_weights",broken)
    with pytest.raises(RuntimeError,match="backend failure"):
        budget.budgeted_power_weights(1031,2,[(1,)]*4)
