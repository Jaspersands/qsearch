"""Complete affine-parameter classification for fixed singleton completion.

Only x_a=1 and x_b=g(b)+1/g(b) with affine g are classified. Exclusion
never means that the original inverse-trace instance is unsatisfiable.
"""
from copy import deepcopy

from theorems.balanced_codeword_filter import integer
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_smt import validate_instance, verify_word


def _validate_singleton(instance):
    if not isinstance(instance, dict):
        raise ValueError("an original instance dictionary is required")
    try:
        for key in ("points", "targets"):
            if not isinstance(instance[key], (list, tuple)):
                raise ValueError(f"{key} must be a list or tuple")
        modulus = instance["field_modulus_coefficients"]
        if not isinstance(modulus, list):
            raise ValueError("field modulus coefficients must be a list")
        for coefficient in modulus:
            integer(coefficient, 0, 1, "field modulus coefficient")
        bits, points, targets, checks = validate_instance(instance)
    except (KeyError, TypeError) as error:
        raise ValueError("malformed original instance") from error
    if bits % 2 == 0:
        raise ValueError("affine singleton classification requires odd field degree")
    if len(points) % 2 == 0:
        raise ValueError("affine singleton classification requires odd length")
    if checks < 4:
        raise ValueError("affine singleton classification requires at least four checks")
    if sum(targets) != 1:
        raise ValueError("exactly one actual target-one coordinate is required")
    return bits, points, targets, checks, targets.index(1)


def _obstruction(moments, inverse_moment):
    for degree, value in enumerate(moments, 1):
        if value:
            return {"kind": "NONZERO_CENTERED_MOMENT", "degree": degree, "value": value}
    if inverse_moment == 0:
        return {"kind": "ZERO_CENTERED_INVERSE_MOMENT", "degree": -1, "value": 0}
    return None


def verify_moment_certificate(instance, certificate):
    """Replay the moment data and affine obstruction, not native infeasibility.

    Both positive and exclusion certificates are supported. A positive
    certificate has obstruction=None; returned words need verify_word too.
    Malformed certificates and unsupported instances return False.
    """
    try:
        bits, points, _, checks, one = _validate_singleton(instance)
        if not isinstance(certificate, dict) or set(certificate) != {
            "one_index", "one_point", "positive_moments", "inverse_moment", "obstruction"
        }:
            return False
        integer(certificate["one_index"], 0, len(points)-1, "one index")
        integer(certificate["one_point"], 0, (1 << bits)-1, "one point")
        integer(certificate["inverse_moment"], 0, (1 << bits)-1, "inverse moment")
        moments = certificate["positive_moments"]
        if not isinstance(moments, list) or len(moments) != checks:
            return False
        for value in moments:
            integer(value, 0, (1 << bits)-1, "positive moment")
        obstruction = certificate["obstruction"]
        if obstruction is not None:
            if not isinstance(obstruction, dict) or set(obstruction) != {"kind", "degree", "value"}:
                return False
            integer(obstruction["degree"], -1, checks, "obstruction degree")
            integer(obstruction["value"], 0, (1 << bits)-1, "obstruction value")
        if certificate["one_index"] != one or certificate["one_point"] != points[one]:
            return False
        center = element(bits, points[one])
        offsets = [element(bits, point)-center for i, point in enumerate(points) if i != one]
        # Direct powers replay the producer's iterative power accumulation.
        expected = [encoded(sum((offset**j for offset in offsets), field(bits).zero()))
                    for j in range(1, checks+1)]
        inverse = encoded(sum((offset**-1 for offset in offsets), field(bits).zero()))
        return (moments == expected and certificate["inverse_moment"] == inverse
                and obstruction == _obstruction(expected, inverse))
    except (KeyError, TypeError, ValueError):
        return False


def classify_affine_singleton(instance):
    """Decide all degree-at-most-one g for the supplied singleton instance.

    Requires backend-compatible distinct points, odd field degree, odd
    length, 4 <= checks < length, and exactly one target bit equal to one.
    Unsupported or malformed inputs raise ValueError, never an exclusion.
    The target-one symbol is fixed to 1; zero-site parameters must be nonzero.
    Input points, order, targets, field encoding and metadata are preserved.
    """
    bits, points, _, checks, one = _validate_singleton(instance)
    center = element(bits, points[one])
    moments = [field(bits).zero() for _ in range(checks)]
    inverse_moment = field(bits).zero()
    for i, point in enumerate(points):
        if i == one:
            continue
        offset = element(bits, point)-center
        inverse_moment += offset**-1
        power = offset
        for j in range(checks):
            moments[j] += power
            power *= offset
    raw_moments, raw_inverse = list(map(encoded, moments)), encoded(inverse_moment)
    obstruction = _obstruction(raw_moments, raw_inverse)
    certificate = {"one_index": one, "one_point": points[one],
                   "positive_moments": raw_moments, "inverse_moment": raw_inverse,
                   "obstruction": obstruction}
    if not verify_moment_certificate(instance, certificate):
        raise ArithmeticError("affine moment certificate failed independent replay")
    result = {"instance": deepcopy(instance),
              "method": "deterministic_complete_affine_singleton_classification",
              "scope": "x_at_one_fixed_to_1_and_g_affine_nonzero_at_zero_sites",
              "status": "AFFINE_ANSATZ_EXCLUDED", "certificate": certificate,
              "certificate_verified": True, "affine_coefficients": None,
              "witness": None, "full_original_word_verified": False,
              "native_unsatisfiability_claimed": False, "hardness_evidence": False,
              "unrestricted_target_solver_established": False, "uniform_sampler": False}
    if obstruction is not None:
        return result

    # The theorem fixes the only candidate: g(X)=mu_{-1}(X-a).
    word = []
    for i, point in enumerate(points):
        if i == one:
            word.append(1)
        else:
            z = inverse_moment*(element(bits, point)-center)
            word.append(encoded(z+z**-1))
    if word[one] != 1 or not verify_word(instance, word):
        raise ArithmeticError("affine candidate failed original native verification")
    result.update(status="VERIFIED_NATIVE_WITNESS", witness=word,
                  affine_coefficients=[encoded(-inverse_moment*center), raw_inverse],
                  full_original_word_verified=True)
    return result
