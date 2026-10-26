"""Resource arithmetic controls, not evidence for the proposed HSP theorem."""
from fractions import Fraction
from math import comb

import pytest

from theorems.class_four_complete_budget import general_quartic_arity, quotient_image_budget


@pytest.mark.parametrize("p", [5, 7, 11, 13, 17, 19, 2**127-1])
def test_four_regimes_and_bounded_error(p):
    error = Fraction(1, 997)
    r = quotient_image_budget(p, 4, 2, 4, error)
    E = {int(k): v for k, v in r["homogeneous_equation_caps"].items()}
    a = r["scalar_arities"]
    assert a["quadratic"] == (E[2]+1)**2
    assert a["cubic"] == (E[3]+1 if p % 3 == 2 else (9*E[3]+1)*(3*E[3]+1)*(E[3]+1))
    assert r["quartic_relation_arity"] == (25 if p % 4 == 3 else 4**18*5**12)
    assert r["matrix_scalar_leaf_slots"] == r["erased_fourier_roots"]*a["linear"]*a["quadratic"]*a["cubic"]
    assert r["scalar_sde_merges"] <= r["matrix_scalar_leaf_slots"]
    assert Fraction(r["failure_union_bound"]) <= error
    assert Fraction(r["matrix_attempt_failure_bound"]) < Fraction(1, 4)
    assert Fraction(r["matrix_attempt_failure_bound"]) == Fraction(3, 100)+Fraction(1, p)
    assert r["alignment_failure_bound"] == "0"
    assert r["alignment_transvection_cap"] == 2*r["minimum_carrier_qudits"] == 2*2*(4+2)
    assert Fraction(r["relation_blocks"], 2**r["block_multiplier_draw_cap"]) <= Fraction(1, 100)
    assert r["normal_source_slots_per_attempt"]*Fraction(1, p**(4*r["label_draw_cap_per_slot"])) <= Fraction(1, 100)
    assert not r["quantum_execution"] and not r["full_hsp_cost_included"]
    assert not r["source_correctness_certified"] and not r["speedup_claim_allowed"]


def test_parameter_count_and_query_product_keep_all_waste_and_retries():
    r = quotient_image_budget(11, 4, 2, 4)
    hW, hZ = 2*comb(6, 2), 4*comb(8, 4)
    assert r["lifted_parameter_count"] == 1+hW+hZ+hW*(hW+1)//2
    assert r["source_query_cap"] == (
        r["matrix_scalar_leaf_slots"]*r["matrix_attempt_cap_per_leaf"]
        *r["normal_source_slots_per_attempt"]*r["label_draw_cap_per_slot"])
    assert r["source_query_cap"] > 10**20


def test_unrounded_collision_recurrence_not_literal_compact_log_bound():
    # With log interpreted as log2, the printed final comparison is not
    # valid at d=4 and equation count >=128. Use the constructive recurrence;
    # this is not a refutation of the fixed-degree polynomial-time result.
    for equations in (128, 1000):
        G = 4**6*(equations+1)**4
        assert general_quartic_arity(equations) == G**3
        assert G**3 > 4**32*(equations+1)**8
    assert general_quartic_arity(127) == 4**32*128**8


@pytest.mark.parametrize("args", [(3, 4, 2, 4), (9, 4, 2, 4), (11, 0, 2, 4),
                                  (11, 4, 0, 4), (11, 4, 2, True)])
def test_invalid_envelope_inputs_are_rejected(args):
    with pytest.raises(ValueError):
        quotient_image_budget(*args)


@pytest.mark.parametrize("error", [0.1, Fraction(0), Fraction(1)])
def test_error_budget_requires_exact_probability(error):
    with pytest.raises(ValueError):
        quotient_image_budget(11, 4, 2, 4, error)
