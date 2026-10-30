"""Exact arithmetic/source countercontrols, not generated HSP candidates."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import gcd

import numpy as np
import pytest

from theorems.prime_power_rees_descent import (
    batch_success_probability, lift_batch_witness, plan_batch, retry_tree_budget,
    iid_regularity_bound, lift_regular_module_witness, verify_module_witness,
    regular_grade_budget, symmetric_block_regularity_bound,
)


@lru_cache(maxsize=None)
def _finite_witness(labels, p, d):
    # Bounded test oracle only. The production module contains no enumeration.
    delta = gcd(d, p-1)
    for witness in product(range(p), repeat=len(labels)):
        if any(witness) and sum(a*pow(x, delta, p) for a, x in zip(labels, witness)) % p == 0:
            return witness
    raise AssertionError("finite scalar diagonal witness missing")


def _get_witness(labels, p, e, d):
    plan = plan_batch(labels, prime=p, exponent=e, degree=d)
    if plan.action == "zero":
        return plan.zero_witness
    if plan.action == "hensel":
        return lift_batch_witness(labels, _finite_witness(plan.field_labels, p, d),
                                  prime=p, exponent=e, degree=d)
    return None


@pytest.mark.parametrize("p,e,d", [(3, 2, 2), (3, 3, 2), (5, 2, 3)])
def test_every_small_central_label_batch_and_all_hidden_intersections(p, e, d):
    modulus = p**e
    arity = gcd(d, p-1) + 1
    for b in range(e+1):
        labels_allowed = tuple(range(0, modulus, p**b))
        actions = Counter()
        for labels in product(labels_allowed, repeat=arity):
            plan = plan_batch(labels, prime=p, exponent=e, degree=d)
            actions[plan.action] += 1
            witness = _get_witness(labels, p, e, d)
            if witness is not None:
                assert any(witness)
                assert all(s == 0 or gcd(s, modulus) == 1 for s in witness)
                assert sum(a*pow(s, d, modulus) for a, s in zip(labels, witness)) % modulus == 0
        actual = Fraction(actions["zero"] + actions["hensel"], len(labels_allowed)**arity)
        assert actual == batch_success_probability(prime=p, exponent=e, degree=d,
                                                   intersection_exponent=b)
        assert actual >= Fraction(1, 4)


@pytest.mark.parametrize("p,e,d", [(3, 8, 2), (5, 9, 3), (2**127-1, 32, 6)])
def test_large_modulus_hensel_lift_has_no_field_or_ring_enumeration(p, e, d):
    arity = gcd(d, p-1) + 1
    modulus = p**e
    for valuation in (0, e//2, e-1):
        unit_modulus = p**(e-valuation)
        normalized = [1, (-1 + p) % unit_modulus] + [1]*(arity-2)
        labels = tuple(p**valuation*a for a in normalized)
        field_witness = (1, 1) + (0,)*(arity-2)
        witness = lift_batch_witness(labels, field_witness, prime=p, exponent=e, degree=d)
        assert witness[2:] == (0,)*(arity-2)
        assert witness[0] % p == witness[1] % p == 1
        assert sum(a*pow(s, d, modulus) for a, s in zip(labels, witness)) % modulus == 0


def test_distinct_valuations_need_retry_and_have_no_unit_or_zero_witness():
    labels = (1, 3, 9)
    assert plan_batch(labels, prime=3, exponent=3, degree=2).action == "retry"
    permitted = (0,) + tuple(x for x in range(27) if x % 3)
    assert not any(any(s) and sum(a*x*x for a, x in zip(labels, s)) % 27 == 0
                   for s in product(permitted, repeat=3))
    # A nonzero nonunit gives a spurious phase zero, not a legal dilation.
    assert 1 * 9**2 % 27 == 0


def test_reducing_divisible_labels_mod_p_without_normalizing_is_wrong():
    labels = (3, 6, 3)
    assert tuple(x % 3 for x in labels) == (0, 0, 0)
    assert sum(a*s*s for a, s in zip(labels, (1, 0, 0))) % 9 != 0
    plan = plan_batch(labels, prime=3, exponent=2, degree=2)
    assert plan.field_labels == (1, 2, 1)
    assert _get_witness(labels, 3, 2, 2) is not None


@pytest.mark.parametrize("p,exponents,degree", [
    (5, (2, 3), 3), (7, (1, 4), 3), (11, (3, 1), 2),
    (2**127-1, (4, 12), 6),
])
def test_multirow_hensel_lifts_mixed_exponents_and_preserves_zero_support(p, exponents, degree):
    columns = [(1, 0), (0, 1), (p-1, p-1), (0, 0)]
    before = tuple(columns)
    field_witness = [1, 1, 1, 0]
    result = lift_regular_module_witness(columns, field_witness, prime=p,
                                         exponents=exponents, degree=degree)
    assert tuple(columns) == before
    assert result["status"] == "VERIFIED_REGULAR_MODULE_WITNESS"
    assert result["jacobian_rank"] == 2
    assert result["pivot_indices"] == [0, 1]
    scales = result["scales"]
    assert scales[3] == 0 and scales[2] == 1
    assert [s % p for s in scales] == field_witness
    assert result["lift_steps"] == max(exponents)-1
    assert verify_module_witness(columns, scales, prime=p, exponents=exponents, degree=degree)
    # Independent integer replay on every ORIGINAL modulus.
    assert all(sum(col[j]*s**degree for col, s in zip(columns, scales)) % p**e == 0
               for j, e in enumerate(exponents))


def test_singular_field_witness_is_not_mistaken_for_ring_cancellation():
    columns, scales = [(1, 0), (4, 5), (0, 1)], [1, 1, 0]
    result = lift_regular_module_witness(columns, scales, prime=5, exponents=(2, 2), degree=3)
    assert result["status"] == "SINGULAR_FIELD_WITNESS"
    assert result["jacobian_rank"] == 1 and result["scales"] is None
    assert not result["singularity_is_unsatisfiability"]
    assert not verify_module_witness(columns, scales, prime=5, exponents=(2, 2), degree=3)
    # A singular witness may ALREADY be exact; singular does not mean impossible.
    exact_columns = [(1, 0), (24, 0), (0, 1)]
    assert verify_module_witness(exact_columns, scales, prime=5, exponents=(2, 2), degree=3)
    assert lift_regular_module_witness(exact_columns, scales, prime=5,
                                       exponents=(2, 2), degree=3)["status"] == "SINGULAR_FIELD_WITNESS"


def test_active_only_jacobian_does_not_turn_zero_into_nonunit():
    result = lift_regular_module_witness([(5,), (1,)], [1, 0], prime=5, exponents=(2,), degree=1)
    assert result["status"] == "SINGULAR_FIELD_WITNESS"
    # Counting the inactive derivative would give rank one, but correcting
    # that coordinate would turn exact zero into a forbidden nonzero nonunit.
    assert result["jacobian_rank"] == 0
    # Taking an unnormalized nonunit scale cancels the phase but is inadmissible.
    assert not verify_module_witness([(5,)], [5], prime=5, exponents=(2,), degree=1)


def test_full_spark_implies_every_nonzero_witness_is_regular_in_finite_control():
    p, columns = 5, [(1, 0), (0, 1), (1, 1), (1, 2)]
    assert all((a[0]*b[1]-a[1]*b[0]) % p for i, a in enumerate(columns) for b in columns[i+1:])
    accepted = 0
    for witness in product(range(p), repeat=len(columns)):
        if not any(witness) or any(sum(col[j]*s**2 for col, s in zip(columns, witness)) % p for j in range(2)):
            continue
        result = lift_regular_module_witness(columns, witness, prime=p, exponents=(2, 3), degree=2)
        assert result["original_module_verified"]
        accepted += 1
    assert accepted > 0


def test_exact_iid_regularity_bound_does_not_certify_small_fields():
    assert iid_regularity_bound(prime=5, cyclic_rank=2, arity=4) == 1
    assert iid_regularity_bound(prime=101, cyclic_rank=2, arity=4) == Fraction(6, 100)
    assert iid_regularity_bound(prime=2**127-1, cyclic_rank=8, arity=153) < Fraction(1, 4)
    with pytest.raises(ValueError):
        iid_regularity_bound(prime=101, cyclic_rank=2, arity=2)
    with pytest.raises(ValueError, match="prime field"):
        iid_regularity_bound(prime=9, cyclic_rank=2, arity=4)


def test_intrinsic_subgroup_coordinates_are_needed_before_reducing_mod_p():
    intrinsic = [(1,0), (0,1), (2,8)]  # C' = Z/3 x Z/9.
    ambient = [(3*a,b) for a,b in intrinsic]  # C' embedded in (Z/9)^2.
    witness = [1,1,1]
    naive = lift_regular_module_witness(ambient, witness, prime=3, exponents=(2,2), degree=2)
    assert naive["status"] == "SINGULAR_FIELD_WITNESS"
    correct = lift_regular_module_witness(intrinsic, witness, prime=3, exponents=(1,2), degree=2)
    assert correct["original_module_verified"]
    assert verify_module_witness(ambient, correct["scales"], prime=3, exponents=(2,2), degree=2)


def test_grade_budget_charges_pilots_failed_banks_and_rank_dependent_prime_guard():
    result = regular_grade_budget(prime=2**127-1, cyclic_rank=8, degree=3)
    assert result["status"] == "CERTIFIED_CONDITIONAL_EPISODE_BOUND"
    assert result["pilot_samples"] == 10 and result["bank_columns_upper"] == 153
    assert "observed_pilot_subgroup_rank" in result["bank_arity_policy"]
    assert result["predecessors_per_episode_upper"] == 163
    assert result["expected_predecessors_upper"] == 326
    assert Fraction(*result["episode_abort_upper"]) < Fraction(3,8)
    assert result["fresh_pilots_each_attempt"]
    assert not result["pilot_coordinate_acquisition_implemented"]
    stronger = regular_grade_budget(prime=105037, cyclic_rank=8, degree=3)
    assert stronger["status"] == "CERTIFIED_CONDITIONAL_EPISODE_BOUND"
    assert Fraction(*stronger["rank_failure_upper"]) == Fraction(153, 105036)
    assert not stronger["arbitrary_sde_solver_supported"]
    # The generic ALL-witnesses bound cannot certify this same regime.
    assert iid_regularity_bound(prime=105037, cyclic_rank=8, arity=153) == 1
    too_many_rows = regular_grade_budget(prime=105037, cyclic_rank=500, degree=3)
    assert too_many_rows["degree_field_guard"]
    assert not too_many_rows["rank_field_guard"]
    assert too_many_rows["expected_predecessors_upper"] is None
    small = regular_grade_budget(prime=7, cyclic_rank=1, degree=3)
    assert not small["degree_field_guard"] and small["episode_abort_upper"] is None
    linear = regular_grade_budget(prime=101, cyclic_rank=2, degree=3)
    assert linear["arithmetic_abort_upper"] == [0,1]
    with pytest.raises(ValueError):
        regular_grade_budget(prime=101, cyclic_rank=2, degree=3, field_failure_bits=3)


def test_observed_rank_bank_bound_requires_discarding_excess_linear_columns():
    from math import comb
    from theorems.power_sde import power_arity
    for degree in (1, 2, 3, 6):
        arity = lambda r: r+1 if degree == 1 else power_arity(r, degree)
        for ambient_rank in range(1, 12):
            assert all(comb(arity(s), s) <= comb(arity(ambient_rank), ambient_rank)
                       for s in range(1, ambient_rank+1))
    # Applying the ambient-rank bound to an unnecessarily large rank-two
    # bank is invalid even though the linear M(s)=s+1 bound is monotone.
    assert comb(9, 2) > comb(9, 8)


def test_reduced_degree_witness_must_be_converted_before_regular_lifting():
    # Over F7, 2^2 = 4 but 2^4 = 2: an unconverted square witness is wrong.
    columns = [(1,), (3,)]
    assert (2**2+3) % 7 == 0
    with pytest.raises(ValueError, match="original degree"):
        lift_regular_module_witness(columns, [2, 1], prime=7, exponents=(2,), degree=4)


@pytest.mark.parametrize("p,degree,reduced", [(65537,2,2), (105037,3,3),
                                            (2**128-275,4,4), (2**127-1,6,6),
                                            (2**128-275,12,4)])
def test_symmetric_solver_retains_regular_blocks_without_global_full_spark(p, degree, reduced):
    from random import Random
    from theorems.power_sde import power_arity
    from theorems.weighted_two_erasure_cascade import solve_bezout_sde_weights
    rank = 3
    block = [(1,0,0), (0,1,0), (0,0,1), (1,1,1)]
    # A fixed invertible row change must not break the support argument.
    block = [((a+2*b+3*c) % p, (b+4*c) % p, c) for a,b,c in block]
    field_columns = block * (power_arity(rank, reduced)//(rank+1))
    # Identical columns in different blocks destroy global full spark.
    assert field_columns[0] == field_columns[rank+1]
    weights, returned_rank, g, _ = solve_bezout_sde_weights(
        p, field_columns, degree, rng=Random(1028), bounded_randomness_bits=12)
    assert returned_rank == rank and g == reduced
    selected = [start for start in range(0, len(weights), rank+1)
                if all(weights[start:start+rank+1])]
    assert selected
    # Every block is either wholly retained or wholly absent.
    assert all(all(weights[start:start+rank+1]) or not any(weights[start:start+rank+1])
               for start in range(0, len(weights), rank+1))
    columns = [tuple(a+p*(i+j+1) for j,a in enumerate(col)) for i,col in enumerate(field_columns)]
    result = lift_regular_module_witness(columns, weights, prime=p, exponents=(2,3,4), degree=degree)
    assert result["jacobian_rank"] == rank and result["original_module_verified"]


def test_good_local_blocks_do_not_make_every_sde_witness_regular():
    p, block = 65537, [(1,0), (0,1), (2,3)]
    assert all((a[0]*b[1]-a[1]*b[0]) % p for i,a in enumerate(block) for b in block[i+1:])
    columns = block*3
    witness = [1,0,0,256,0,0,0,0,0]
    assert pow(256,2,p) == p-1
    result = lift_regular_module_witness(columns, witness, prime=p, exponents=(2,2), degree=2)
    assert result["status"] == "SINGULAR_FIELD_WITNESS" and result["jacobian_rank"] == 1
    assert not result["original_module_verified"]


def test_block_regularity_bound_is_scoped_to_reduced_degree_and_iid_source():
    assert symmetric_block_regularity_bound(prime=105037, cyclic_rank=8, reduced_degree=3) == Fraction(153,105036)
    assert symmetric_block_regularity_bound(prime=101, cyclic_rank=8, reduced_degree=1) == Fraction(9,100)
    assert symmetric_block_regularity_bound(prime=7, cyclic_rank=8, reduced_degree=3) == 1
    with pytest.raises(ValueError, match="divide"):
        symmetric_block_regularity_bound(prime=101, cyclic_rank=2, reduced_degree=3)
    with pytest.raises(ValueError, match="positive cyclic"):
        symmetric_block_regularity_bound(prime=101, cyclic_rank=0, reduced_degree=2)


@pytest.mark.parametrize("columns,witness,exponents,degree", [
    ([(1, 2)], [0], (2, 3), 3),
    ([(1, 2)], [1], (2, 3), 3),
    ([(1, 2)], [1], (2,), 3),
    ([(25, 2)], [1], (2, 3), 3),
    ([(1, 2)], [1], (2, 3), 5),
    ([(True, 2)], [1], (2, 3), 3),
])
def test_multirow_lift_rejects_bad_contracts(columns, witness, exponents, degree):
    with pytest.raises(ValueError):
        lift_regular_module_witness(columns, witness, prime=5, exponents=exponents, degree=degree)


def _conditional_states(modulus, central_step):
    points = tuple(product(range(modulus), repeat=2))
    index = {x: i for i, x in enumerate(points)}
    def action(g):
        return np.array([index[((x-g[0]) % modulus, (y-g[1]) % modulus)] for x, y in points])
    eye = np.eye(len(points))
    h = tuple(product(range(0, modulus, 3), range(0, modulus, central_step)))
    rho = sum(eye[:, action(g)] for g in h)/len(points)
    states = {}
    for label in range(modulus):
        projector = sum(np.exp(-2j*np.pi*label*z/modulus)*eye[:, action((0, z))]
                        for z in range(modulus))/modulus
        branch = projector @ rho
        mass = np.trace(branch).real
        if mass > 1e-12:
            states[label] = branch/mass
        else:
            np.testing.assert_allclose(branch, 0, atol=1e-12)
    def correlation(label, g):
        # R_g sends |x> to |x-g>; sum rho[x,x-g] is Tr(rho R_g).
        return np.sum(states[label][np.arange(len(points)), action(g)])
    return states, correlation


def _instrument(modulus, labels, scales, degree, correlation):
    result = np.zeros((modulus, modulus), complex)
    for q, r in product(range(modulus), repeat=2):
        value = 1
        for label, scale in zip(labels, scales):
            if scale:
                # Nonlinear section sigma(q)=(q,q^2) makes cancellation visible.
                g = (scale*(q-r) % modulus, pow(scale, degree, modulus)*(q*q-r*r) % modulus)
                value *= correlation(label, g)
        result[q, r] = value/modulus
    return result


@pytest.mark.parametrize("central_step,labels", [(9, (1, 1, 1)), (9, (0, 1, 3)),
                                                 (3, (3, 3, 3)), (1, (0, 0, 0))])
def test_full_central_density_contraction_with_all_intersection_types(central_step, labels):
    states, correlation = _conditional_states(9, central_step)
    assert all(label in states for label in labels)
    scales = _get_witness(labels, 3, 2, 2)
    output = _instrument(9, labels, scales, 2, correlation)
    expected = np.array([[float((q-r) % 3 == 0)/9 for r in range(9)] for q in range(9)])
    np.testing.assert_allclose(output, expected, atol=2e-14)


def test_nonunit_phase_zero_produces_false_whole_quotient_signal():
    _, correlation = _conditional_states(9, 9)
    labels, wrong_scales = (1, 1, 1), (3, 0, 0)
    assert sum(a*s*s for a, s in zip(labels, wrong_scales)) % 9 == 0
    output = _instrument(9, labels, wrong_scales, 2, correlation)
    expected = np.array([[float((q-r) % 3 == 0)/9 for r in range(9)] for q in range(9)])
    np.testing.assert_allclose(output, np.ones((9, 9))/9, atol=2e-14)
    np.testing.assert_allclose(np.abs(np.linalg.eigvalsh(output-expected)).sum()/2,
                               2/3, atol=2e-14)


def test_multirow_lift_in_actual_nonnormal_mixed_center_instrument():
    # A class-two graded group: x,y in F3, z in Z/9, w in F3,
    # [x,y]=3z. Its center has genuinely mixed exponents (2,1).
    elements = tuple(product(range(3), range(3), range(9), range(3)))
    index = {g: i for i, g in enumerate(elements)}
    def mul(a, b):
        x,y,z,w = a
        u,v,t,s = b
        return ((x+u) % 3, (y+v) % 3, (z+t+6*(x*v-y*u)) % 9, (w+s) % 3)
    def inv(a):
        return (-a[0] % 3, -a[1] % 3, -a[2] % 9, -a[3] % 3)
    def action(g):
        return np.array([index[mul(v, inv(g))] for v in elements])
    hidden = ((0,0,0,0), (1,0,0,0), (2,0,0,0))
    assert mul(mul((0,1,0,0), hidden[1]), inv((0,1,0,0))) not in hidden
    eye = np.eye(len(elements))
    rho = sum(eye[:, action(h)] for h in hidden)/len(elements)
    labels = ((1,0), (0,1), (2,2))
    states = []
    center = tuple((0,0,z,w) for z,w in product(range(9), range(3)))
    for lam in labels:
        projector = sum(np.exp(-2j*np.pi*(lam[0]*z/9+lam[1]*w/3))*eye[:,action((0,0,z,w))]
                        for _,_,z,w in center)/len(center)
        branch = projector @ rho
        mass = np.trace(branch).real
        np.testing.assert_allclose(mass, 1/27, atol=1e-14)
        states.append(branch/mass)
    quotient = tuple(product(range(3), repeat=2))
    def section(q):
        x,y = q
        return (x,y,(x*x+2*y) % 9,(x+y*y) % 3)
    def contract(scales):
        output = np.zeros((9,9), complex)
        for i,q in enumerate(quotient):
            for j,r in enumerate(quotient):
                g = mul(inv(section(r)), section(q))
                value = 1
                for scale,state in zip(scales, states):
                    pulled = (scale*g[0] % 3, scale*g[1] % 3,
                              scale*scale*g[2] % 9, scale*scale*g[3] % 3)
                    value *= np.sum(state[np.arange(len(elements)), action(pulled)])
                output[i,j] = value/9
        return output
    result = lift_regular_module_witness(labels, [1,1,1], prime=3, exponents=(2,1), degree=2)
    assert result["original_module_verified"]
    expected = np.array([[float(q[1] == r[1])/9 for r in quotient] for q in quotient])
    np.testing.assert_allclose(contract(result["scales"]), expected, atol=3e-14)
    assert np.linalg.norm(contract([1,1,1])-expected) > 0.1


def test_mixed_torsion_rees_interpolation_without_free_module_assumption():
    # L=(Z/9)^3, [x,y]=3z, gamma_2=<3z> has order3, not order9.
    # h=<x+z,3y> is a nonnormal Lie subring with h intersect gamma_2=0.
    def in_h(v):
        x, y, z = v
        return y % 3 == 0 and (z-x) % 9 == 0
    def evaluate(a, s):
        x, y, z, w = a
        return (s*x % 9, s*y % 9, (s*z + 3*s*s*w) % 9)
    for x, y, z in product(range(9), repeat=3):
        for w in range(3):
            a = (x, y, z, w)
            hidden = in_h((x, y, z)) and w == 0
            assert all(in_h(evaluate(a, s)) for s in (1, 2)) == hidden
            for unit in (1, 2, 4, 5, 7, 8):
                dilated = (unit*x % 9, unit*y % 9, unit*z % 9, unit*unit*w % 3)
                assert (in_h(dilated[:3]) and dilated[3] == 0) == hidden
    # Distinct ring elements need distinct residues modulo p for Vandermonde.
    bad = (0, 0, 6, 1)
    assert evaluate(bad, 1) == evaluate(bad, 4) == (0, 0, 0)
    assert evaluate(bad, 2) != (0, 0, 0)


def test_cyclic_rank_does_not_bound_lie_ring_class():
    # Over Z/5^4, [x,y]=5y: rank([L,L])=1 but class=4.
    p, exponent = 5, 4
    modulus = p**exponent
    def bracket(x, y):
        return (0, p*(x[0]*y[1] - x[1]*y[0]) % modulus)
    word = (0, 1)
    for step in range(1, exponent):
        word = bracket((1, 0), word)
        assert word == (0, p**step)
    assert bracket((1, 0), word) == (0, 0)


def test_retry_clock_counts_failed_batches_not_just_successful_tree():
    budget = retry_tree_budget(prime=5, nilpotency_class=3,
                               higher_grade_cyclic_ranks=(2, 1), terminal_samples=7)
    assert budget["expected_lifted_leaves_upper"] == 7*12**2*8
    assert budget["expected_original_inputs_upper"] == 3*7*12**2*8
    assert budget["hard_original_input_cap"] == 16*budget["expected_original_inputs_upper"]
    assert budget["full_instrument_cap"] == 2*budget["hard_lifted_leaf_cap"]+7
    assert budget["clock_failure_upper"] == "1/16"


@pytest.mark.parametrize("labels,p,e,d", [((1, 1, 1), 3, 0, 2), ((1, 1), 3, 2, 3),
                                        ((1, 1), 3, 2, 2), ((-1, 1, 1), 3, 2, 2),
                                        ((True, 1, 1), 3, 2, 2)])
def test_invalid_batch_contracts(labels, p, e, d):
    with pytest.raises(ValueError):
        plan_batch(labels, prime=p, exponent=e, degree=d)


def test_false_witness_and_retry_batch_are_not_lifted():
    for labels, witness in [((1, 1, 1), (0, 0, 0)), ((1, 1, 1), (1, 0, 0)),
                            ((1, 3, 9), (1, 1, 1))]:
        with pytest.raises(ValueError):
            lift_batch_witness(labels, witness, prime=3, exponent=3, degree=2)


def test_source_probability_is_not_valid_for_an_arbitrary_fixed_label_bank():
    labels = (1, 3, 9)
    assert plan_batch(labels, prime=3, exponent=3, degree=2).action == "retry"
    # Replaying this bank fails forever. The ideal probability is not a
    # guarantee about arbitrary/adversarial labels or a source certificate.
    assert batch_success_probability(prime=3, exponent=3, degree=2,
                                     intersection_exponent=0) > Fraction(1, 4)


@pytest.mark.parametrize("p,c,ranks,samples", [(5, 3, (1, 2), 7), (5, 3, (2,), 7),
                                               (3, 3, (1, 1), 7), (5, 3, (2, 1), True)])
def test_invalid_retry_profiles(p, c, ranks, samples):
    with pytest.raises(ValueError):
        retry_tree_budget(prime=p, nilpotency_class=c,
                          higher_grade_cyclic_ranks=ranks, terminal_samples=samples)
