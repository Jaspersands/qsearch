from itertools import product
from collections import Counter

from flint import fq_default_poly_ctx
import pytest

from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_smt import native_instance, verify_word
from theorems.inverse_trace_norm import (
    QuadraticTower, factor_signature, progression, run_experiment, split_norm,
    norm_family_membership, output_law_certificate, success_certificate,
    verify_membership_certificate, word_from_norm,
)


def small_instance(bits, points, targets, checks=1):
    return {"bits": bits, "points": points, "targets": targets, "checks": checks,
            "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}


@pytest.mark.parametrize("bits", [3, 5, 17])
def test_tower_preserves_original_field_and_conjugation(bits):
    tower = QuadraticTower(bits)
    for a, b in product(range(8), repeat=2):
        x, y = element(bits, a), element(bits, b)
        ex, ey = tower.embed(x), tower.embed(y)
        assert tower.embed(x+y) == ex+ey
        assert tower.embed(x*y) == ex*ey
        assert tower.components(ex+tower.rho*ey) == (x, y)
        assert (ex+tower.rho*ey)*(ex+(tower.rho+1)*ey) == tower.embed(x*x+x*y+y*y)
    assert tower.embed(field(bits).gen()).frobenius(bits) == tower.embed(field(bits).gen())


def test_even_base_degree_is_rejected():
    with pytest.raises(ValueError, match="odd base"):
        QuadraticTower(4)
    problem = small_instance(4, list(range(6)), [1]*6)
    with pytest.raises(ValueError, match="odd extension"):
        run_experiment(problem)


def test_norm_criterion_and_exact_splitting_for_small_polynomials():
    ring = fq_default_poly_ctx(field(3))
    for degree in range(1, 4):
        for raw in product(range(8), repeat=degree):
            F = ring([element(3, x) for x in raw]+[field(3).one()])
            A, B, record = split_norm(3, F)
            if record["is_constant_extension_norm"]:
                assert B*B+A*B+A*A == F
                assert record["norm_identity_verified"]
                assert max(A.degree(), B.degree()) == degree//2
            else:
                assert A is B is None
                assert any(d % 2 and e % 2 for d, e in record["factor_degrees_and_multiplicities"])


def test_repeated_inert_factors_and_nonscalar_embedding_unit():
    ring = fq_default_poly_ctx(field(5))
    X = ring.gen()
    F = element(5, 11)*(X+element(5, 7))**4*(X*X+X+1)**3
    A, B, record = split_norm(5, F)
    assert record["is_constant_extension_norm"]
    assert B*B+A*B+A*A == F
    assert factor_signature((X+1)**3)[-1]
    with pytest.raises(ValueError, match="nonzero"):
        split_norm(5, ring.zero())


@pytest.mark.parametrize("mode", ["ones", "random"])
def test_native_seeded_witness_keeps_original_input_and_all_constraints(mode):
    problem = native_instance(5, 1028, mode)
    result = run_experiment(problem, seed=1029, max_trials=64)
    assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    assert result["instance"] == problem
    assert verify_word(problem, result["witness"])
    assert all(x == 0 for x, b in zip(result["witness"], problem["targets"]) if not b)
    certificate = result["certificate"]
    ring = fq_default_poly_ctx(field(5))
    polys = {k: ring([element(5, v) for v in certificate[k]])
             for k in ("P", "derivative", "remainder", "T", "F", "A", "B")}
    assert polys["F"] == polys["remainder"]+polys["P"]*polys["T"]
    assert polys["F"] % polys["P"] == polys["derivative"]**2 % polys["P"]
    word, t = word_from_norm(problem, polys["A"], polys["B"])
    assert word == result["witness"] and t == certificate["parameter"]
    for claim in ("hardness_evidence", "unrestricted_target_solver_established", "uniform_sampler",
                  "whole_workflow_wall_clock_cap_enforced", "factorization_subroutine_randomness_capped"):
        assert result[claim] is False
    with pytest.raises(ValueError, match="norm does not"):
        word_from_norm(problem, polys["A"]+1, polys["B"])
    with pytest.raises(ValueError, match="degree budget"):
        word_from_norm(problem, ring.gen()**25, polys["B"])


def test_limits_and_support_failure_are_not_unsatisfiability():
    problem = native_instance(5, 1028)
    result = run_experiment(problem, max_trials=0)
    assert result["status"] == "UNKNOWN_TRIAL_LIMIT"
    assert result["witness"] is None and not result["trials"]
    narrow = dict(problem, targets=[1]+[0]*24)
    result = run_experiment(narrow)
    assert result["status"] == "NOT_APPLICABLE_TO_THIS_SUPPORT_RESTRICTION"
    assert not result["hardness_evidence"]
    zero = run_experiment(dict(problem, targets=[0]*25))
    assert zero["full_original_word_verified"] and zero["witness"] == [0]*25
    with pytest.raises(ValueError):
        run_experiment(problem, max_trials=-1)


def test_progression_uses_square_root_points_and_even_degree_budget():
    problem = native_instance(5, 17)
    active, P, D, R, tdegree = progression(problem)
    assert P.degree() == len(active) == 25
    assert R == D*D % P and P.gcd(D).degree() == 0
    assert P.degree()+tdegree == 2*(len(active)-problem["checks"]-1)
    assert all(P(element(5, a)**16) == 0 for a in problem["points"])


def test_zero_avoidance_is_paid_and_not_silently_totalized():
    problem = small_instance(3, [0, 1, 2], [1, 1, 1])
    ring = fq_default_poly_ctx(field(3))
    beta = [element(3, a)**4 for a in problem["points"]]
    products = [(ring.gen()+beta[(i+1) % 3])*(ring.gen()+beta[(i+2) % 3])
                for i in range(3)]
    # Norm-one residues rho, rho+1, 1 sum to zero. The first two
    # parameters really produce an illegal zero at a target-one position.
    A, B = products[0]+products[1], products[1]+products[2]
    word, parameter = word_from_norm(problem, A, B)
    assert parameter == 2 and verify_word(problem, word)


def test_constant_parameter_space_is_not_resampled():
    problem = small_instance(3, [0, 1, 2, 3], [1]*4)
    result = run_experiment(problem, max_trials=20)
    assert result["polynomial_parameter_degree"] == 0
    assert len(result["trials"]) == 1


@pytest.mark.parametrize("bits,m,checks,denominator", [
    (17, 289, 36, 1008), (17, 144, 36, 428), (17, 146, 36, 436),
    (11, 121, 15, 420), (31, 363, 120, 968),
])
def test_exact_uniform_success_guard(bits, m, checks, denominator):
    result = success_certificate(bits, m, checks)
    assert result["half_main_term_certified"]
    assert result["iid_trial_success_lower_bound"] == [1, denominator]
    assert result["expected_iid_trials_upper"] == denominator
    assert result["main_scaled_bit_length"] > result["error_scaled_bit_length"]


@pytest.mark.parametrize("bits,m,checks", [(5,25,3), (7,49,6), (17,74,36)])
def test_failed_bound_is_inconclusive_not_a_failure_of_the_algorithm(bits, m, checks):
    result = success_certificate(bits, m, checks)
    assert result["status"] == "BOUND_INCONCLUSIVE"
    assert result["iid_trial_success_lower_bound"] is None


def test_guard_hypotheses_are_enforced():
    for bits, m, checks in ((4,10,1), (3,1,1), (3,8,1), (17,73,36)):
        assert success_certificate(bits, m, checks)["status"] == "OUTSIDE_CERTIFICATE_SCOPE"


def test_even_degree_prime_powers_are_norms_without_subtraction():
    ring = fq_default_poly_ctx(field(3))
    for degree in (1, 2, 3):
        for raw in product(range(8), repeat=degree):
            prime = ring([element(3, x) for x in raw]+[field(3).one()])
            if not prime.is_irreducible():
                continue
            exponent = 2 if degree % 2 else 1
            assert not factor_signature(prime**exponent)[-1]


@pytest.mark.parametrize("bits,exponent", [(17,-70), (31,-1918), (61,-21388)])
def test_entire_norm_family_has_tiny_uniform_native_mass(bits, exponent):
    problem = native_instance(bits, 1028)
    result = output_law_certificate(problem)
    assert result["status"] == "CERTIFIED_NONUNIFORM_OUTPUT_FAMILY"
    assert result["uniform_support_mass_power2_upper"] == exponent
    assert result["total_variation_lower_bound"] == f"1 - 2^({exponent})"
    assert result["includes_all_projective_parameters"]
    assert result["includes_all_trace_one_quadratic_models"]
    assert result["projective_parameters_absorbed_by_norm_one_rotation"]
    assert not result["general_classical_sampling_lower_bound"]


def test_mixed_target_bound_uses_fixed_zero_event_not_full_support_theorem():
    problem = native_instance(17, 1028, "random")
    result = output_law_certificate(problem)
    assert result["scope"] == "outputs_zero_at_a_fixed_zero_target_position"
    assert problem["targets"][result["zero_position"]] == 0
    assert result["uniform_support_mass_power2_upper"] == -15
    assert "includes_all_projective_parameters" not in result


def test_small_family_bound_does_not_invent_a_sampling_obstruction():
    result = output_law_certificate(native_instance(5,1028))
    assert result["status"] == "BOUND_INCONCLUSIVE"
    assert result["total_variation_lower_bound"] == "0"
    too_short = small_instance(3, [0,1,2], [1]*3)
    assert output_law_certificate(too_short)["status"] == "OUTSIDE_NORM_FAMILY_COUNT_SCOPE"


def test_norm_representation_count_includes_leading_units_and_repeated_factors():
    ring = fq_default_poly_ctx(field(3))
    counts = Counter()
    for raw in product(range(8), repeat=4):
        A = ring([element(3, v) for v in raw[:2]])
        B = ring([element(3, v) for v in raw[2:]])
        F = B*B+A*B+A*A
        if F.is_zero():
            assert A.is_zero() and B.is_zero()
            continue
        counts[tuple(map(encoded, F.coeffs()))] += 1
    for raw, count in counts.items():
        F = ring([element(3, v) for v in raw])
        _, factors, _, obstruction = factor_signature(F)
        assert not obstruction
        expected = 9
        for factor, multiplicity in factors:
            if factor.degree() % 2 == 0:
                expected *= multiplicity+1
            else:
                assert multiplicity % 2 == 0
        assert count == expected
        assert count <= 9*(1 << (F.degree()//2))


def test_all_trace_one_conics_are_the_same_full_code_family():
    context = field(3)
    values = [element(3, v) for v in range(8)]
    problem = small_instance(3, [0,1,2,3], [1]*4)
    reference = None
    for c in values:
        if c.trace() != 1:
            continue
        shift = next(u for u in values if u*u+u == c+1)
        conic = [(a,b) for a in values for b in values if b*b+a*b+c*a*a == 1]
        assert len(conic) == 9
        outputs = set()
        for pairs in product(conic, repeat=4):
            if sum((a for a,_ in pairs),context.zero()) != 0:
                continue
            if sum((b for _,b in pairs),context.zero()) != 0:
                continue
            standard = [(a,b+shift*a) for a,b in pairs]
            assert all(b*b+a*b+a*a == 1 for a,b in standard)
            for t in values+[None]:
                raw = [a*a if t is None else (a*t+b)**2/(t*t+t+c) for a,b in pairs]
                if any(v == 0 for v in raw):
                    continue
                moved = [a*a if t is None else (a*(t+shift)+b)**2/((t+shift)**2+(t+shift)+1)
                         for a,b in standard]
                assert raw == moved
                # Every parameter is a norm-one rotation of the t=0 family.
                if t is None:
                    rotated = [(a+b, a) for a, b in standard]
                else:
                    u = t+shift
                    s = (u*u+u+1)**4
                    rotated = [(((1+u)*a+u*b)/s, (b+u*a)/s) for a, b in standard]
                assert all(b*b+a*b+a*a == 1 for a, b in rotated)
                assert sum((a for a, _ in rotated), context.zero()) == 0
                assert sum((b for _, b in rotated), context.zero()) == 0
                assert [b*b for _, b in rotated] == raw
                word = tuple(map(encoded, raw))
                assert verify_word(problem, word)
                outputs.add(word)
        if reference is None:
            reference = outputs
        else:
            assert outputs == reference
    assert reference


def test_membership_matches_exhaustive_local_lifts_on_every_small_native_word():
    problem = small_instance(3, list(range(6)), [1]*6, checks=2)
    values = [element(3, i) for i in range(8)]
    allowed = [i for i in range(1, 8) if (values[i]**-1).trace() == 1]
    beta = [element(3, i)**4 for i in problem["points"]]
    counts = Counter()
    for word in product(allowed, repeat=6):
        if not verify_word(problem, word):
            continue
        roots = [values[i]**4 for i in word]
        local = [[a for a in values if b*b+a*b+a*a == 1] for b in roots]
        assert all(len(options) == 2 for options in local)
        exists = any(all(sum((p**j*a for p, a in zip(beta, lift)), field(3).zero()) == 0
                         for j in range(2)) for lift in product(*local))
        result = norm_family_membership(problem, word)
        assert (result["status"] == "NATIVE_WORD_IN_NORM_FAMILY") == exists
        assert verify_membership_certificate(problem, word, result)
        assert not result["native_unsatisfiability_claimed"]
        assert result["rank"] < len(word)  # All-one binary vector is in ker M.
        counts[exists] += 1
        if exists:
            partner = dict(result, epsilon_hex=hex(int(result["epsilon_hex"], 16)^63),
                           a=[a^encoded(b) for a, b in zip(result["a"], roots)])
            assert verify_membership_certificate(problem, word, partner)
        else:
            assert not verify_membership_certificate(problem, word, dict(result, dual_hex="0x0"))
    assert counts == {True: 62, False: 6}


def test_membership_certificates_reject_tampering_and_out_of_scope_inputs():
    problem = native_instance(5, 1028)
    result = run_experiment(problem)
    certificate = result["norm_family_membership"]
    assert certificate["status"] == "NATIVE_WORD_IN_NORM_FAMILY"
    assert verify_membership_certificate(problem, result["witness"], certificate)
    assert not verify_membership_certificate(problem, result["witness"], dict(certificate, a=[0]*25))
    assert not verify_membership_certificate(problem, result["witness"], dict(certificate, epsilon_hex=hex(1 << 25)))
    assert not verify_membership_certificate(problem, result["witness"], {"status": "UNRECOGNIZED"})
    with pytest.raises(ValueError, match="valid original"):
        norm_family_membership(problem, [0]*25)
    for other in (dict(problem, targets=[0]*25), small_instance(4, list(range(6)), [1]*6)):
        with pytest.raises(ValueError, match="odd degree and all-one"):
            norm_family_membership(other, [1]*len(other["points"]))


def test_optional_flat_control_preserves_original_problem_and_records_certificates():
    problem = native_instance(5, 1028)
    result = run_experiment(problem, max_trials=0, compare_flat_dimension=1, flat_seed=1030)
    assert result["status"] == "UNKNOWN_TRIAL_LIMIT"
    control = result["same_instance_flat_comparison"]
    assert control["input"]["points"] == problem["points"]
    assert control["input"]["targets"] == problem["targets"]
    assert control["input"]["checks"] == problem["checks"]
    assert control["status"] == "VERIFIED_NATIVE_CLASSICAL_WITNESS"
    assert verify_word(problem, control["witness"])
    assert verify_membership_certificate(problem, control["witness"], control["norm_family_membership"])
    assert not control["asymptotic_solver_established"]
    assert not control["global_unsatisfiability_claimed"]
    with pytest.raises(ValueError, match="all-one"):
        run_experiment(dict(problem, targets=[0]*25), compare_flat_dimension=1)
    with pytest.raises(ValueError, match="positive flat dimension"):
        run_experiment(problem, compare_flat_dimension=0)


@pytest.mark.parametrize("bits,genus,exponent", [(5,11,-30), (17,143,-2142)])
def test_sparse_singleton_interpolant_has_large_artin_schreier_genus(bits, genus, exponent):
    length, checks = bits*bits, bits*bits//8
    ring = fq_default_poly_ctx(field(bits))
    X, P = ring.gen(), ring.one()
    for raw in range(length):
        P *= X+element(bits, raw)
    B = (P//X)*P.derivative()(field(bits).zero())**-1
    C, G = B, ring.zero()
    for degree in range(B.degree(), 0, -1):
        if degree % 2 == 0 and C[degree] != 0:
            term = C[degree]**(1 << (bits-1))*X**(degree//2)
            C += term*term+term
            G += term
    assert C == B+G*G+G
    assert C.degree() == 2*genus+1 == length-2
    assert genus >= checks
    for raw in range(length):
        point = element(bits, raw)
        assert B(point) == int(raw == 0)
        assert int(C(point).trace()) == int(raw == 0)
    assert length-bits*genus == exponent
