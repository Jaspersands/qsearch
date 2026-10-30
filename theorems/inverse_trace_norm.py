"""A constant-extension norm attack on the original inverse-trace relation.

The polynomial progression is constrained. A checked specialization of
Sawin's uniform bound, not random-polynomial heuristics, can certify it.
Every returned word is independently checked against the original instance.
"""
from functools import lru_cache
from fractions import Fraction
import hashlib
import json
from random import Random
from time import perf_counter
from math import comb, isqrt

from flint import __version__ as flint_version, fq_default_ctx, fq_default_poly_ctx

from theorems.balanced_codeword_filter import ceil_log2_fraction, integer
from theorems.cubic_rs_affine_flats import restricted_system, solve_binary
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_gibbs_target import reciprocal_bound
from theorems.inverse_trace_smt import validate_instance, verify_word


def coefficients(poly):
    return list(map(encoded, poly.coeffs()))


def output_law_certificate(instance):
    """Count the whole norm-family image, not only a seeded run's outputs.

    Includes arbitrary mixtures/rejections, all factor allocations, all
    norm-one scalar rotations and all projective parameters. Postprocessing
    that leaves this algebraic family is NOT covered.
    """
    bits, points, targets, checks = validate_instance(instance)
    length, q = len(points), 1 << bits
    _, eta = reciprocal_bound(bits, length, checks)
    result = {"status": "BOUND_INCONCLUSIVE", "includes_abort": True,
              "uniform_target": "all_original_native_witnesses",
              "general_classical_sampling_lower_bound": False,
              "fiber_error_power2_upper": ceil_log2_fraction(eta),
              "uniform_support_mass_power2_upper": 0,
              "total_variation_lower_bound": "0"}
    if all(targets) and (bits % 2 == 0 or 2*(length-checks-1) < length):
        return {**result, "status": "OUTSIDE_NORM_FAMILY_COUNT_SCOPE"}
    if eta >= 1:
        return result
    if 0 in targets:
        if length-1 <= checks:
            return result
        _, shorter_eta = reciprocal_bound(bits, length-1, checks)
        mass = Fraction(2, q)*(1+shorter_eta)/(1-eta)
        result.update(scope="outputs_zero_at_a_fixed_zero_target_position",
                      zero_position=targets.index(0))
    else:
        degree = 2*(length-checks-1)
        # All degrees <= degree and all leading units are included, not
        # just the monic progression implemented by the search routine.
        # A norm-one rotation absorbs every projective parameter into t=0.
        # Counting parameters again would overcount the whole image by q+1.
        mass = Fraction((q+1) * (1 << (2*length-checks-1)), q**(checks+1))/(1-eta)
        result.update(scope="entire_full_support_constant_quadratic_norm_family",
                      norm_degree_cap=degree,
                      includes_all_trace_one_quadratic_models=True,
                      includes_all_projective_parameters=True,
                      projective_parameters_absorbed_by_norm_one_rotation=True)
    exponent = min(0, ceil_log2_fraction(mass))
    result.update(status="CERTIFIED_NONUNIFORM_OUTPUT_FAMILY" if exponent < 0 else "BOUND_INCONCLUSIVE",
                  uniform_support_mass_power2_upper=exponent,
                  total_variation_lower_bound=f"1 - 2^({exponent})" if exponent < 0 else "0")
    return result


def _membership_system(instance, word):
    bits, points, targets, checks = validate_instance(instance)
    if bits % 2 == 0 or not all(targets):
        raise ValueError("norm-family recognition requires odd degree and all-one targets")
    if not verify_word(instance, word):
        raise ValueError("valid original all-one word required")
    beta = [encoded(element(bits, p)**(1 << (bits-1))) for p in points]
    roots, origins = [], []
    for raw in word:
        x = element(bits, raw)
        b, w = x**(1 << (bits-1)), x**-1+1
        z, term = field(bits).zero(), w
        for _ in range((bits+1)//2):
            z += term
            term = term**4
        if z*z+z != w:
            raise ArithmeticError("half-trace failed on a trace-zero value")
        roots.append(encoded(b))
        origins.append(encoded(b*z))
    flats = [{"origin": a, "directions": [b]} for a, b in zip(origins, roots)]
    equations, width = restricted_system(bits, checks, beta, flats)
    return equations, width, roots, origins


def verify_membership_certificate(instance, word, certificate):
    """Verify a lift or a dual inconsistency witness without running a solver."""
    try:
        equations, width, roots, origins = _membership_system(instance, word)
        bits, points, _, checks = validate_instance(instance)
        if certificate["status"] == "NATIVE_WORD_IN_NORM_FAMILY":
            epsilon = int(certificate["epsilon_hex"], 16)
            if not 0 <= epsilon < 1 << width:
                return False
            a = [origin ^ (root if epsilon >> i & 1 else 0)
                 for i, (origin, root) in enumerate(zip(origins, roots))]
            if a != certificate["a"]:
                return False
            if any(((row & epsilon).bit_count() & 1) != rhs for row, rhs in equations):
                return False
            av, bv = [element(bits, v) for v in a], [element(bits, v) for v in roots]
            beta = [element(bits, p)**(1 << (bits-1)) for p in points]
            return (all(b*b+u*b+u*u == 1 for u, b in zip(av, bv)) and
                    all(sum((p**j*u for p, u in zip(beta, av)), field(bits).zero()) == 0
                        for j in range(checks)))
        if certificate["status"] != "NATIVE_WORD_OUTSIDE_NORM_FAMILY":
            return False
        dual = int(certificate["dual_hex"], 16)
        if not 0 <= dual < 1 << len(equations):
            return False
        row_sum, rhs_sum = 0, 0
        for i, (row, rhs) in enumerate(equations):
            if dual >> i & 1:
                row_sum ^= row
                rhs_sum ^= rhs
        return row_sum == 0 and rhs_sum == 1
    except (KeyError, TypeError, ValueError):
        return False


def norm_family_membership(instance, word):
    """Recognize the ENTIRE all-one norm family by binary linear algebra.

    This is not native satisfiability: input validity is checked first.
    No field, parameter, or local-root-combination enumeration is used.
    """
    equations, width, roots, origins = _membership_system(instance, word)
    system = solve_binary(equations, width)
    result = {"scope": "entire_full_support_constant_quadratic_norm_family",
              "original_word_verified": True, "native_unsatisfiability_claimed": False,
              "binary_variables": width, "binary_equations": len(equations),
              "rank": system["rank"], "free_bits": system["free_bits"],
              "row_xors": system["row_xors"]}
    if system["consistent"]:
        epsilon = system["solution"]
        result.update(status="NATIVE_WORD_IN_NORM_FAMILY", epsilon_hex=hex(epsilon),
                      a=[origin ^ (root if epsilon >> i & 1 else 0)
                         for i, (origin, root) in enumerate(zip(origins, roots))])
    else:
        # Reuse the binary solver on M^T lambda=0, r^T lambda=1.
        # This produces an independently replayable negative certificate.
        transpose = [(sum(((row >> j) & 1) << i for i, (row, _) in enumerate(equations)), 0)
                     for j in range(width)]
        transpose.append((sum(rhs << i for i, (_, rhs) in enumerate(equations)), 1))
        dual = solve_binary(transpose, len(equations))
        if not dual["consistent"]:
            raise ArithmeticError("inconsistent primal has no dual certificate")
        result.update(status="NATIVE_WORD_OUTSIDE_NORM_FAMILY", dual_hex=hex(dual["solution"]),
                      dual_row_xors=dual["row_xors"])
    if not verify_membership_certificate(instance, word, result):
        raise ArithmeticError("norm-family membership certificate failed replay")
    result["certificate_verified"] = True
    return result


def success_certificate(bits, active_count, checks):
    """Conservative integer specialization of Sawin, Lemma 8.15.

    All von-Mangoldt-supported polynomials of even total degree are norms.
    The certificate is a mathematical IID-trial bound, not a PRNG guarantee
    or a hard clock on FLINT's factorization routines.
    """
    integer(bits, 3, 127, "field degree")
    integer(active_count, 0, 100_000, "active coordinate count")
    integer(checks, 1, 100_000, "check count")
    m, degree, q = active_count, 2*(active_count-checks-1), 1 << bits
    result = {"source": "https://arxiv.org/pdf/2102.09730", "lemma": "8.15",
              "target_degree": degree, "modulus_degree": m,
              "half_main_term_certified": False,
              "iid_trial_success_lower_bound": None,
              "uniform_over_distinct_points": True,
              "published_theorem_import_not_formally_verified": True}
    if bits % 2 == 0 or m < 2 or m >= q or degree < m:
        return {**result, "status": "OUTSIDE_CERTIFICATE_SCOPE"}
    A = sum((1 << (m-1-r))*comb(degree+m-r, 2*m-r) for r in range(m-1))
    B = (1 << (m-1))*comb(degree+m, 2*m-1)

    def ceil_sqrt(value):
        root = isqrt(value)
        return root+int(root*root != value)

    phi = (q-1)**m
    error_scaled = m+phi*(A*ceil_sqrt(q**(degree-m))
                          + B*ceil_sqrt(q**(degree+1-m)))
    main_scaled = q**degree
    passed = 2*error_scaled <= main_scaled
    result.update(status="CERTIFIED_IID_NORM_TRIAL_BOUND" if passed else "BOUND_INCONCLUSIVE",
                  half_main_term_certified=passed,
                  iid_trial_success_lower_bound=[1, 2*degree] if passed else None,
                  expected_iid_trials_upper=2*degree if passed else None,
                  error_scaled_bit_length=error_scaled.bit_length(),
                  main_scaled_bit_length=main_scaled.bit_length())
    return result


@lru_cache(maxsize=4)
class QuadraticTower:
    """Explicit F_(q^2)=F_q[rho], rho^2+rho+1=0, for odd base degree.

    FLINT handles field construction and factoring. A binary basis transform
    preserves the original input's field encoding; no field table is used.
    """

    def __init__(self, bits):
        integer(bits, 3, 127, "odd base field degree")
        if bits % 2 == 0:
            raise ValueError("rho^2+rho+1 requires odd base degree")
        self.bits = bits
        self.context = fq_default_ctx(2, 2*bits)
        self.ring = fq_default_poly_ctx(self.context)
        base_modulus = self.ring(list(map(int, field(bits).modulus().coeffs())))
        roots = base_modulus.roots()
        if len(roots) != bits or any(e != 1 for _, e in roots):
            raise ArithmeticError("base field embedding did not split completely")
        generator = min((r for r, _ in roots), key=encoded)
        rho_roots = (self.ring.gen()**2+self.ring.gen()+1).roots()
        self.rho = min((r for r, _ in rho_roots), key=encoded)
        self.powers = [generator**j for j in range(bits)]
        basis = self.powers + [self.rho*b for b in self.powers]
        self.pivots = {}
        for j, value in enumerate(basis):
            word, coordinate = encoded(value), 1 << j
            while word:
                pivot = word.bit_length()-1
                if pivot not in self.pivots:
                    self.pivots[pivot] = word, coordinate
                    break
                row, transform = self.pivots[pivot]
                word ^= row
                coordinate ^= transform
            if not word:
                raise ArithmeticError("quadratic tower basis is dependent")
        if self.rho.frobenius(bits) != self.rho+1:
            raise ArithmeticError("wrong quadratic conjugation")

    def embed(self, value):
        word = encoded(value)
        return sum((p for j, p in enumerate(self.powers) if word >> j & 1),
                   self.context.zero())

    def components(self, value):
        word, coordinate = encoded(value), 0
        while word:
            row, transform = self.pivots[word.bit_length()-1]
            word ^= row
            coordinate ^= transform
        mask = (1 << self.bits)-1
        return element(self.bits, coordinate & mask), element(self.bits, coordinate >> self.bits)


def factor_signature(polynomial):
    if polynomial.is_zero():
        raise ValueError("nonzero norm target required")
    unit, factors = polynomial.factor()
    signature = sorted((factor.degree(), multiplicity) for factor, multiplicity in factors)
    obstruction = any(degree % 2 and multiplicity % 2 for degree, multiplicity in signature)
    return unit, factors, signature, obstruction


def split_norm(bits, polynomial):
    """Return A,B with B^2+A*B+A^2=polynomial, or a checked obstruction."""
    unit, factors, signature, obstruction = factor_signature(polynomial)
    record = {"factor_degrees_and_multiplicities": signature,
              "is_constant_extension_norm": not obstruction}
    if obstruction:
        return None, None, record
    tower = QuadraticTower(bits)
    extension = tower.ring
    monic = polynomial * (unit**-1)
    target = extension([tower.embed(v) for v in monic.coeffs()])
    _, split = target.factor()
    key = lambda f: tuple(encoded(v) for v in f.coeffs())
    by_key = {key(f): (f, e) for f, e in split}
    used, half = set(), extension.one()
    for current in sorted(by_key):
        if current in used:
            continue
        factor, multiplicity = by_key[current]
        conjugate = extension([v.frobenius(bits) for v in factor.coeffs()])
        partner = key(conjugate)
        if partner == current:
            if multiplicity % 2:
                raise ArithmeticError("inert factor has odd multiplicity")
            half *= factor**(multiplicity//2)
        else:
            if partner not in by_key or by_key[partner][1] != multiplicity:
                raise ArithmeticError("missing conjugate factor")
            half *= factor**multiplicity
        used.update((current, partner))
    half *= tower.embed(unit**(1 << (bits-1)))
    parts = [tower.components(v) for v in half.coeffs()]
    base = fq_default_poly_ctx(field(bits))
    B, A = base([b for b, _ in parts]), base([a for _, a in parts])
    if B*B+A*B+A*A != polynomial:
        raise ArithmeticError("base-field norm identity failed")
    record["norm_identity_verified"] = True
    return A, B, record


def progression(instance):
    bits, points, targets, checks = validate_instance(instance)
    if bits < 3 or bits % 2 == 0:
        raise ValueError("this construction requires odd extension degree >=3")
    active = [i for i, b in enumerate(targets) if b]
    base = fq_default_poly_ctx(field(bits))
    P = base.one()
    for i in active:
        P *= base.gen()+element(bits, points[i])**(1 << (bits-1))
    derivative = P.derivative()
    remainder = derivative**2 % P if active else base.zero()
    return active, P, derivative, remainder, len(active)-2*checks-2


def word_from_norm(instance, A, B):
    """Verify the complete norm/code certificate before extracting a word."""
    bits, points, targets, checks = validate_instance(instance)
    active, P, derivative, _, _ = progression(instance)
    m, q = len(active), 1 << bits
    if not active or m >= q:
        raise ValueError("nonempty active set smaller than the field required")
    if max(A.degree(), B.degree()) > m-checks-1:
        raise ValueError("norm factors exceed the dual-RS degree budget")
    if (B*B+A*B+A*A-derivative**2) % P != 0:
        raise ValueError("norm does not equal the squared derivative on native points")
    pairs = []
    for i in active:
        beta = element(bits, points[i])**(1 << (bits-1))
        denominator = derivative(beta)
        a, b = A(beta)/denominator, B(beta)/denominator
        if b*b+a*b+a*a != 1:
            raise ArithmeticError("native norm-one value failed")
        pairs.append((a, b))
    # Each nonzero affine numerator forbids at most one t. The denominator
    # has no roots at odd extension degree. Scan m+1 distinct public values.
    for parameter in range(m+1):
        t = element(bits, parameter)
        linear = [a*t+b for a, b in pairs]
        if any(v == 0 for v in linear):
            continue
        Q = t*t+t+1
        word = [0]*len(points)
        for i, value in zip(active, linear, strict=True):
            word[i] = encoded(value*value/Q)
        if not verify_word(instance, word):
            raise ArithmeticError("norm construction failed original-instance verification")
        return word, parameter
    raise ArithmeticError("affine root avoidance exceeded its proved bound")


def run_experiment(instance, *, seed=1029, max_trials=64,
                   compare_flat_dimension=None, flat_seed=1030):
    integer(seed, 0, 2**32-1, "polynomial seed")
    integer(max_trials, 0, 10000, "polynomial trial cap")
    start = perf_counter()
    bits, points, targets, checks = validate_instance(instance)
    if compare_flat_dimension is not None:
        from theorems.reciprocal_trace_flats import local_flat_budget
        if bits % 2 == 0 or not all(targets):
            raise ValueError("flat family-membership comparison requires odd degree and all-one targets")
        integer(compare_flat_dimension, 1, bits, "positive flat dimension")
        local_flat_budget(bits, compare_flat_dimension)
        integer(flat_seed, 0, 2**32-1, "flat seed")
    instance = {"bits": bits, "points": list(points), "targets": list(targets),
                "checks": checks, "field_modulus_coefficients": instance["field_modulus_coefficients"]}
    digest = hashlib.sha256(json.dumps(instance, sort_keys=True).encode()).hexdigest()
    result = {"method": "constant_quadratic_extension_norm_progression",
              "instance": instance, "instance_sha256": digest,
              "seed": seed, "max_trials": max_trials, "flint_version": flint_version,
              "scope": "zero_on_all_zero_target_positions",
              "trials": [], "witness": None, "full_original_word_verified": False,
              "status": "UNKNOWN_TRIAL_LIMIT", "hardness_evidence": False,
              "unrestricted_target_solver_established": False, "uniform_sampler": False,
              "mathematical_expected_polynomial_search_bound": False,
              "whole_workflow_wall_clock_cap_enforced": False,
              "factorization_subroutine_randomness_capped": False,
              "output_law_certificate": output_law_certificate(instance)}
    if not any(targets):
        result.update(status="VERIFIED_NATIVE_WITNESS", witness=[0]*len(points),
                      full_original_word_verified=verify_word(instance, [0]*len(points)))
    else:
        active, P, derivative, remainder, tdegree = progression(instance)
        result.update(active_indices=active, polynomial_parameter_degree=tdegree,
                      norm_factor_degree_budget=len(active)-checks-1,
                      analytic_success_certificate=success_certificate(bits, len(active), checks))
        result["mathematical_expected_polynomial_search_bound"] = result["analytic_success_certificate"]["half_main_term_certified"]
        if tdegree < 0 or len(active) >= 1 << bits:
            result["status"] = "NOT_APPLICABLE_TO_THIS_SUPPORT_RESTRICTION"
        else:
            ring, rng = fq_default_poly_ctx(field(bits)), Random(seed)
            # Monic T fixes an even target degree. At degree zero there is
            # only one T, so repeating it would manufacture duplicate trials.
            for trial in range(min(max_trials, 1 if tdegree == 0 else max_trials)):
                trial_start = perf_counter()
                T = ring([element(bits, rng.getrandbits(bits)) for _ in range(tdegree)]+[field(bits).one()])
                F = remainder+P*T
                A, B, record = split_norm(bits, F)
                record.update(trial=trial, target_degree=F.degree(),
                              T_sha256=hashlib.sha256(json.dumps(coefficients(T)).encode()).hexdigest(),
                              seconds=perf_counter()-trial_start)
                result["trials"].append(record)
                if A is None:
                    continue
                word, parameter = word_from_norm(instance, A, B)
                result.update(status="VERIFIED_NATIVE_WITNESS", witness=word,
                              full_original_word_verified=True,
                              certificate={"P": coefficients(P), "derivative": coefficients(derivative),
                                           "remainder": coefficients(remainder), "T": coefficients(T),
                                           "F": coefficients(F), "A": coefficients(A), "B": coefficients(B),
                                           "parameter": parameter})
                if all(targets):
                    result["norm_family_membership"] = norm_family_membership(instance, word)
                break
    if compare_flat_dimension is not None:
        from theorems.reciprocal_trace_flats import _serialize, solve_with_flats
        control = solve_with_flats(bits, points, checks, targets, compare_flat_dimension,
                                   seed=flat_seed)
        if control["witness"] is not None:
            control["norm_family_membership"] = norm_family_membership(instance, control["witness"])
        result["same_instance_flat_comparison"] = _serialize(control)
    result["total_seconds"] = perf_counter()-start
    return result
