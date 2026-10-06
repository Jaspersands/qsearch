import itertools
import json
import random
from fractions import Fraction

import pytest
import sympy as sp

from native_rlwe_quaternion_kernel import (
    NATIVE, add, audit_quaternion_encoding, conjugate, kernel_member, mul,
    multiplication_matrix, quaternion_multiply, quaternion_source_gate,
    reduced_norm, run_controls,
)


def test_ring_arithmetic_matches_independent_symbolic_polynomial_remainder():
    rng = random.Random(510051)
    x = sp.Symbol("x")
    for d in (2,4,8):
        for _ in range(8):
            a = tuple(rng.randrange(-5,6) for _ in range(d))
            b = tuple(rng.randrange(-5,6) for _ in range(d))
            polynomial = sp.Poly(sum(v*x**i for i,v in enumerate(a))*sum(v*x**i for i,v in enumerate(b)),x)
            residue = polynomial.rem(sp.Poly(x**d+1,x))
            assert mul(a,b) == tuple(int(residue.nth(i)) for i in range(d))
            assert multiplication_matrix(conjugate(a)) == multiplication_matrix(a).T


def test_quaternion_associativity_norm_and_left_kernel_closure_with_actual_parameters():
    rng = random.Random(510052)
    for d,q in ((2,7),(4,11),(8,19)):
        m = tuple(rng.randrange(q) for _ in range(d))
        record = audit_quaternion_encoding(m,q,include_matrices=True)
        rho = tuple(map(int,record["adaptive_definite_order"]["parameter_coefficients"]))
        for _ in range(6):
            pair = lambda: tuple(tuple(rng.randrange(-3,4) for _ in range(d)) for _ in range(2))
            a,b,c = pair(),pair(),pair()
            assert quaternion_multiply(quaternion_multiply(a,b,rho),c,rho) == quaternion_multiply(a,quaternion_multiply(b,c,rho),rho)
            assert reduced_norm(quaternion_multiply(a,b,rho),rho) == mul(reduced_norm(a,rho),reduced_norm(b,rho))
            f = b[1]
            g = add(mul(m,f),tuple(q*v for v in b[0]))
            member = (g,f)
            assert kernel_member(member,m,q)
            assert kernel_member(quaternion_multiply(a,member,rho),m,q)
        R = multiplication_matrix(rho)
        lo = int(record["adaptive_definite_order"]["exact_spectral_lower_bound"])
        assert lo >= 1 and R.is_symmetric()
        assert all(R[i,i]-sum(abs(R[i,j]) for j in range(d) if j!=i) == lo for i in range(d))


def test_complete_high_CRT_native_source_counts_and_degree_two_exception():
    for d,q,expected in ((2,3,4),(4,3,8),(4,11,120),(8,3,80)):
        count = 0
        for m in itertools.product(range(q),repeat=d):
            norm = mul(m,conjugate(m))
            count += all((v+int(i==0)) % q==0 for i,v in enumerate(norm))
        assert count == expected
        if d>=4:
            gate = quaternion_source_gate(d,q)
            assert int(gate["exact_full_source_probability"]["numerator_hex"],16) == count
            assert int(gate["exact_full_source_probability"]["denominator_hex"],16) == q**d


def test_label_adaptive_rational_phase_cannot_ignore_native_lattice_integrality():
    # h=(3+4i)/5 has h*bar(h)=1, but J_h(q,0) is not in the unit-ratio kernel.
    h = (sp.Rational(3,5),sp.Rational(4,5))
    assert mul(h,conjugate(h)) == (1,0)
    assert not kernel_member(((0,0),(3,4)),(1,0),5)
    # In the d2 Gaussian case, this is NOT a high-CRT source-probability proof.
    with pytest.raises(ValueError):
        quaternion_source_gate(2,3)


def test_left_ideal_is_not_silently_treated_as_a_two_sided_ideal():
    m,q = (1,1),3
    rho = (1,0)
    j = ((0,0),(1,0))
    member = (m,(1,0))
    assert kernel_member(quaternion_multiply(j,member,rho),m,q)
    assert not kernel_member(quaternion_multiply(member,j,rho),m,q)


def test_principal_encoding_has_full_kernel_basis_but_long_known_generator():
    record = audit_quaternion_encoding((128,0),257,include_matrices=True)
    basis = sp.Matrix([[int(v) for v in row] for row in record["finite_algebra_certificate"]["known_principal_generator_basis"]])
    assert abs(basis.det()) == 257**2
    principal = record["adaptive_known_principal_order"]
    assert principal["generator_reduced_norm"] == "257"
    assert int(principal["generator_physical_norm_squared"]) == 16385
    assert int(principal["parameter_coefficients"][0]) < 0
    assert kernel_member(((-1,0),(2,0)),(128,0),257)
    assert not principal["PIP_has_an_unknown_generator_to_find"]
    assert not principal["source_metric_or_shortness_guarantee_supplied"]


def test_saved_native_kernel_and_growing_gates_keep_every_scope_and_claim_guard():
    report = run_controls()
    native = report["same_saved_native_d64_kernel"]
    assert native["dimension"] == 64
    assert not native["hamilton_original_metric_left_ideal_compatible"]
    assert native["adaptive_definite_order"]["full_graph_kernel_left_ideal_closure_verified"]
    assert not native["adaptive_definite_order"]["principality_promised_or_proved"]
    assert [r["full_source_probability_upper_bound_dyadic_exponent"] for r in report["growing_native_source_gates"]] == [2304,12288,61440]
    assert not report["claim_gate"]["all_weighted_quaternion_or_general_quantum_algorithms_ruled_out"]
    assert not report["claim_gate"]["speedup_claim_allowed"]
    assert not report["claim_gate"]["independent_review"]


def test_actual_native_adjoint_sign_convention_preserves_all_saved_rows():
    saved = json.loads(NATIVE.read_text())
    m = tuple(map(int,saved["native_ratio"]))
    d,q = len(m),int(saved["q"])
    ratio = tuple(v % q for v in conjugate(m))
    for row in saved["reduced_row_basis"]:
        x,y = tuple(map(int,row[:d])),tuple(map(int,row[d:]))
        assert kernel_member((x,tuple(-v for v in y)),ratio,q)
        assert sum(v*v for v in x+y)==sum(v*v for v in x+tuple(-v for v in y))
    record = run_controls()["same_saved_native_d64_kernel"]
    assert record["canonical_native_ratio"]==list(map(str,ratio))
    assert record["saved_native_reduced_basis_rows_checked"]==2*d
    assert record["coordinate_map_is_exact_signed_isometry"]


def test_degenerate_principal_encoding_and_positive_easy_branch_are_distinguished():
    degenerate = audit_quaternion_encoding((1,1,0,1),3)
    assert degenerate["adaptive_known_principal_order"]["zero_parameter_is_degenerate_NOT_quaternion_PIP_input"]
    assert degenerate["adaptive_known_principal_order"]["parameter_coefficients"] == ["0"]*4
    easy = audit_quaternion_encoding((0,0),7)
    assert easy["adaptive_definite_order"]["principality_promised_or_proved"]
    assert easy["adaptive_definite_order"]["known_principality_only_when_this_parameter_equals_the_explicit_principal_encoding"]


def test_unavoidable_metric_distortion_for_all_real_congruence_lifts():
    q,m = 11,(2,8,7,4)
    record = audit_quaternion_encoding(m,q)
    energy = int(record["adaptive_definite_order"]["every_positive_congruence_lift_lambda_max_squared_lower_bound"])
    residue = tuple((-v+q//2) % q-q//2 for v in mul(m,conjugate(m)))
    assert energy==sum(v*v for v in residue)
    for scalar,a in itertools.product(range(-2,3),repeat=2):
        # ALL these lifts remain real; positivity is separately required by
        # the theorem, while coefficient energy minimization is unconditional.
        rho = add(residue,(q*scalar,q*a,0,-q*a))
        R = multiplication_matrix(rho)
        assert R.is_symmetric()
        assert sum(v*v for v in rho)>=energy
        assert sp.trace(R**2)==len(m)*sum(v*v for v in rho)


def test_native_uniform_real_mixture_moments_and_probability_bound():
    report = run_controls()
    for row in report["complete_finite_source_counts"]:
        d,q = row["d"],row["q"]
        if d==2:
            continue
        metric = quaternion_source_gate(d,q)["unavoidable_positive_lift_metric_distortion"]
        fraction = lambda x: Fraction(int(x["numerator"]),int(x["denominator"]))
        mu = fraction(metric["uniform_real_centered_coefficient_energy_mean"])
        var = fraction(metric["uniform_real_centered_coefficient_energy_variance"])
        alpha = Fraction(q**(d//2)-1,q**(d//2))
        assert Fraction(row["native_centered_real_norm_energy_sum"],q**d)==alpha*mu
        assert Fraction(row["native_centered_real_norm_energy_square_sum"],q**d)==alpha*(var+mu*mu)
    gate = quaternion_source_gate(64,19)["unavoidable_positive_lift_metric_distortion"]
    p = gate["source_probability_lower_bound"]
    lower = Fraction(int(p["numerator_hex"],16),int(p["denominator_hex"],16))
    assert lower>Fraction(89,100)
    assert gate["all_positive_lifts_covered_not_just_constructed_lift"]
    assert not gate["different_coordinate_maps_or_all_weighted_algorithms_ruled_out"]


def test_norm_one_units_of_constructed_definite_orders_and_fixed_norm_orbits():
    for m,q,expected in (((1,1),7,4),((1,1),3,8)):
        row = audit_quaternion_encoding(m,q)
        rho = tuple(map(int,row["adaptive_definite_order"]["parameter_coefficients"]))
        units = []
        fixed_generators = []
        alpha = (m,(1,0))
        for coordinates in itertools.product(range(-2,3),repeat=4):
            pair = (coordinates[:2],coordinates[2:])
            if reduced_norm(pair,rho)==(1,0):
                units.append(pair)
            if reduced_norm(pair,rho)==(q,0) and kernel_member(pair,m,q):
                fixed_generators.append(pair)
        assert len(units)==expected==row["adaptive_definite_order"]["norm_one_units"]["exact_count"]
        orbit = {quaternion_multiply(u,alpha,rho) for u in units}
        assert orbit==set(fixed_generators)
        assert all(sum(v*v for block in p for v in block)==3 for p in orbit)
        assert row["adaptive_definite_order"]["norm_one_units"]["fixed_reduced_norm_principal_generators_original_physical_length_invariant"]
        assert not row["adaptive_definite_order"]["norm_one_units"]["general_units_or_different_reduced_norms_classified"]


@pytest.mark.parametrize("d,q", [(2,3),(3,3),(4,17),(4,2),(True,3)])
def test_source_formula_rejects_unmatched_CRT_regimes(d,q):
    with pytest.raises(ValueError):
        quaternion_source_gate(d,q)


@pytest.mark.parametrize("m,q", [((),3),((0,),3),((0,1,2),3),((True,0),3),((3,0),3),((0,0),2)])
def test_malformed_graph_kernels_rejected(m,q):
    with pytest.raises(ValueError):
        audit_quaternion_encoding(m,q)
