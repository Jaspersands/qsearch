"""Genus-zero norm search for trace-affine targets on the native relation.

The success certificate imports Sawin's squarefree-progression divisor bound.
It needs uniform polynomial trials AND uniform norm-factor allocations.
Seeded runs are replay controls, not IID probability or uniform-witness claims.
"""
from fractions import Fraction
import hashlib
import json
from math import comb, isqrt
from random import Random
from time import perf_counter

from flint import __version__ as flint_version, fq_default_poly_ctx

from theorems.balanced_codeword_filter import ceil_log2_fraction, integer, trace_mask
from theorems.cubic_rs_affine_flats import solve_binary
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_norm import coefficients
from theorems.inverse_trace_smt import validate_instance, verify_word


def trace_bit_instance(bits=17, bit=8):
    """Public basis-prefix points and a public trace-dual target, no planting."""
    integer(bits, 5, 127, "field degree")
    integer(bit, 0, bits-1, "target basis bit")
    length = bits*bits
    if length > 1 << bits:
        raise ValueError("native length exceeds field size")
    equations = [(trace_mask(bits, 1 << j), int(j == bit)) for j in range(bits)]
    solution = solve_binary(equations, bits)
    if not solution["consistent"] or solution["rank"] != bits:
        raise ArithmeticError("trace pairing must be nondegenerate")
    instance = {"bits": bits, "points": list(range(length)),
                "targets": [(i >> bit) & 1 for i in range(length)],
                "checks": length//8,
                "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}
    return instance, solution["solution"], 0


def success_certificate(bits, length, checks, zeros):
    """Integer/rational upper bounds; no floating point acceptance decision."""
    integer(bits, 2, 127, "field degree")
    integer(length, 2, min(1 << bits, 100_000), "length")
    integer(checks, 1, length-1, "parity checks")
    integer(zeros, 0, length, "zero target count")
    q, e, s = 1 << bits, 2*(length-checks-1)+1, length-2*checks-1
    result = {"status": "BOUND_INCONCLUSIVE", "degree": e,
              "parameter_degree": s, "iid_trial_success_lower_bound": None,
              "source": "https://arxiv.org/pdf/2102.09730", "lemma": "8.7; divisor parameter 4",
              "uniform_factor_allocation_required": True,
              "published_theorem_import_not_formally_verified": True}
    if s < 0:
        return {**result, "status": "OUTSIDE_CERTIFICATE_SCOPE"}
    root = isqrt(q)
    root += int(root*root < q)
    rho = Fraction(2*root+1, q-1)
    eta = (q**(2*checks+1)-1)*rho**(length-checks)
    result["first_moment_error_power2_upper"] = ceil_log2_fraction(eta)
    if rho >= 1 or eta >= 1:
        return result
    lower = Fraction(q-1, q)**zeros*(1-eta)
    C1 = (4**length-comb(length+3, 3))*comb(3*length-4, s)
    C2 = 4**(length-1)*comb(3*length-3, s+1)

    def upper_negative_half_power(exponent):
        # Also valid at exponent=-1: ceil(sqrt(q)) bounds sqrt(q).
        return (Fraction(root, q**((exponent+1)//2)) if exponent % 2
                else Fraction(1, q**(exponent//2)))

    error = 2*C1*upper_negative_half_power(s)+2*C2*upper_negative_half_power(s-1)
    second = Fraction(q, q-1)**length*comb(e+3, 3)+error
    ratio = second/(lower*lower)
    trials = (ratio.numerator+ratio.denominator-1)//ratio.denominator
    result.update(status="CERTIFIED_IID_GENUS_ZERO_TRIAL_BOUND",
                  iid_trial_success_lower_bound=[1, trials],
                  expected_iid_trials_upper=trials,
                  divisor_error_power2_upper=ceil_log2_fraction(error) if error else None)
    return result


def _parameters(instance, c, d0):
    bits, points, targets, checks = validate_instance(instance)
    integer(c, 1, (1 << bits)-1, "nonzero trace slope")
    integer(d0, 0, (1 << bits)-1, "trace offset")
    slope, offset = element(bits, c), element(bits, d0)
    if any(int((slope*element(bits, a)+offset).trace()) != b
           for a, b in zip(points, targets, strict=True)):
        raise ValueError("original targets are not the supplied trace-affine family")
    ring = fq_default_poly_ctx(field(bits))
    P = ring.one()
    for a in points:
        P *= ring.gen()+element(bits, a)
    return bits, points, targets, checks, slope, offset, ring, P


def split_norm(bits, polynomial, c, d0, rng):
    """Sample uniformly among normalized lifts, without enumerating them."""
    integer(c, 1, (1 << bits)-1, "nonzero trace slope")
    integer(d0, 0, (1 << bits)-1, "trace offset")
    if not polynomial:
        raise ValueError("nonzero polynomial required")
    slope, offset = element(bits, c), element(bits, d0)
    ring = fq_default_poly_ctx(field(bits))
    Y = ring.gen()
    _, factors = polynomial.factor()
    labels = [{"degree": f.degree(), "multiplicity": v,
               "inert": bool(int((slope*f[f.degree()-1]+offset*(f.degree() % 2)).trace()))}
              for f, v in factors]
    record = {"base_factor_signature": labels, "is_norm": False,
              "norm_identity_verified": False, "allocation_count": 0}
    if any(t["inert"] and t["multiplicity"] % 2 for t in labels):
        return None, None, record
    Q = polynomial.compose((Y*Y+Y+offset)*(slope**-1))
    unit, factors = Q.factor()
    key = lambda f: tuple(coefficients(f))
    by_key = {key(f): (f, v) for f, v in factors}
    used, h, count, allocations = set(), ring.one(), 1, []
    for k in sorted(by_key):
        if k in used:
            continue
        f, v = by_key[k]
        partner = key(f.compose(Y+1))
        if partner not in by_key or by_key[partner][1] != v:
            raise ArithmeticError("involution does not preserve factor multiplicity")
        if k == partner:
            if v % 2:
                raise ArithmeticError("inert-prime test disagrees with composed factorization")
            h *= f**(v//2)
        else:
            j = rng.randrange(v+1)
            h *= f**j*by_key[partner][0]**(v-j)
            count *= v+1
            allocations.append({"factor": list(k), "multiplicity": v, "chosen_exponent": j})
        used.update((k, partner))
    h *= unit**(1 << (bits-1))
    if h*h.compose(Y+1) != Q:
        raise ArithmeticError("normalized polynomial norm failed")
    C, U, A = Y*slope+offset, ring.zero(), ring.zero()
    for value in reversed(h.coeffs()):
        U, A = A*C+value, U+A
    if U*U+U*A+C*A*A != polynomial:
        raise ArithmeticError("decomposed norm failed")
    record.update(is_norm=True, norm_identity_verified=True,
                  allocation_count=count, allocations=allocations)
    return U, A, record


def word_from_norm(instance, c, d0, U, A):
    bits, points, targets, checks, slope, offset, ring, P = _parameters(instance, c, d0)
    r = len(points)-checks-1
    if max(U.degree(), A.degree()) > r:
        raise ValueError("norm lift exceeds degree budget")
    D = P.derivative()
    if (U*U+U*A+(ring.gen()*slope+offset)*A*A-D*D) % P:
        raise ValueError("norm residues disagree with the original points")
    word = [encoded(A(element(bits, a))/D(element(bits, a))) for a in points]
    if any(x == 0 and b for x, b in zip(word, targets, strict=True)):
        return None
    if not verify_word(instance, word):
        raise ArithmeticError("norm lift failed original verifier")
    return word


def run_experiment(instance, c, d0=0, *, seed=1030, allocation_seed=1031, max_trials=32):
    integer(seed, 0, 2**32-1, "polynomial seed")
    integer(allocation_seed, 0, 2**32-1, "allocation seed")
    integer(max_trials, 0, 10000, "outer trial cap")
    start = perf_counter()
    bits, points, targets, checks, _, _, ring, P = _parameters(instance, c, d0)
    r, s = len(points)-checks-1, len(points)-2*checks-1
    D, rng, allocation_rng = P.derivative(), Random(seed), Random(allocation_seed)
    remainder = D*D % P
    result = {"method": "genus_zero_trace_affine_norm", "instance": instance,
              "instance_sha256": hashlib.sha256(json.dumps(instance, sort_keys=True).encode()).hexdigest(),
              "c": c, "d0": d0, "seed": seed, "allocation_seed": allocation_seed,
              "max_trials": max_trials, "flint_version": flint_version,
              "status": "UNKNOWN_TRIAL_LIMIT", "trials": [], "witness": None,
              "full_original_word_verified": False, "hardness_evidence": False,
              "uniform_sampler": False, "unrestricted_target_solver_established": False,
              "whole_workflow_wall_clock_cap_enforced": False,
              "factorization_subroutine_randomness_capped": False,
              "success_certificate": success_certificate(bits, len(points), checks, targets.count(0))}
    if s < 0:
        result["status"] = "OUTSIDE_DEGREE_SCOPE"
    else:
        for trial in range(max_trials):
            trial_start = perf_counter()
            T = ring([element(bits, rng.getrandbits(bits)) for _ in range(s)]+[field(bits).one()])
            F = remainder+P*T
            U, A, record = split_norm(bits, F, c, d0, allocation_rng)
            record.update(trial=trial, T_sha256=hashlib.sha256(json.dumps(coefficients(T)).encode()).hexdigest())
            word = word_from_norm(instance, c, d0, U, A) if A is not None else None
            record.update(one_site_zero_rejection=A is not None and word is None,
                          seconds=perf_counter()-trial_start)
            result["trials"].append(record)
            if word is not None:
                result.update(status="VERIFIED_NATIVE_WITNESS", witness=word,
                              full_original_word_verified=True,
                              certificate={"P": coefficients(P), "D": coefficients(D),
                                           "T": coefficients(T), "F": coefficients(F),
                                           "U": coefficients(U), "A": coefficients(A),
                                           "degree_budget": r})
                break
    result["total_seconds"] = perf_counter()-start
    return result
