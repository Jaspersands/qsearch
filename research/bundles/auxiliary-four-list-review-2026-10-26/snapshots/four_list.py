"""Small-bias four-list certificate for effective-divisor coset search.

The finite binary calculations check the proof's overlap cases. They are
not toy oracle candidates or implementations of Jacobian arithmetic.
"""

from fractions import Fraction


def binary_rank(vectors):
    pivots = {}
    for value in vectors:
        while value:
            bit = value.bit_length()-1
            if bit in pivots:
                value ^= pivots[bit]
            else:
                pivots[bit] = value
                break
    return len(pivots)


def overlap_codes(shared):
    if type(shared) is not int or not 0 <= shared < 16:
        raise ValueError("a four-bit overlap mask is required")
    indices = list(range(4))
    next_index = 4
    for i in range(4):
        if shared >> i & 1:
            indices.append(i)
        else:
            indices.append(next_index)
            next_index += 1
    low = [(1 << indices[j]) ^ (1 << indices[j+1]) for j in (0, 2, 4, 6)]
    high = [sum(1 << indices[j] for j in range(start, start+4)) for start in (0, 4)]
    return next_index, low, high


def overlap_certificate():
    cases = []
    checked = 0
    for shared in range(16):
        size, low, high = overlap_codes(shared)
        low_rank, high_rank = binary_rank(low), binary_rank(high)
        maximum = -100
        for support in range(1 << size):
            outside = ((1 << size)-1) ^ support
            low_dim = low_rank-binary_rank([row & outside for row in low])
            high_dim = high_rank-binary_rank([row & outside for row in high])
            power = (8-shared.bit_count()-low_rank-2*high_rank
                     +low_dim+2*high_dim-support.bit_count())
            maximum = max(maximum, power)
            checked += 1
            if power > 0:
                raise ArithmeticError("unbounded overlap term in second-moment proof")
        cases.append({"shared_mask": shared, "independent_variables": size,
                      "low_rank": low_rank, "high_rank": high_rank,
                      "maximum_scale_exponent": maximum})
    return {"checked_support_masks": checked, "cases": cases,
            "untruncated_success_lower": Fraction(49, 64)/Fraction(117, 16)**4,
            "capped_success_lower": Fraction(1, 8000),
            "cap_multiplier": 40000,
            "distribution_premise_verified_by_this_certificate": False}


def tower_certificate(e, rational_two_rank=None):
    if type(e) is not int or e < 8 or e & (e-1):
        raise ValueError("dyadic source degree >=8 required")
    p, g, a = 100003, 5*e+1, 2*e-9
    rank = 2*g if rational_two_rank is None else rational_two_rank
    if type(rank) is not int or not 3 <= rank <= 2*g:
        raise ValueError("rank must be between3 and2g; smaller ranks are constant cases")
    base, remainder = divmod(a, 4)
    degrees = [base]*(4-remainder)+[base+1]*remainder
    exponent = (rank+2)//3
    tests = []
    for degree in degrees:
        constant = (g+1)*(degree+6)
        numerator = p**degree
        denominator = 64*constant**2*2**(2*exponent)
        tests.append({"degree": degree, "C_n": constant,
                      "small_bias_sufficient_condition": numerator >= denominator,
                      "exact_sufficiency_ratio": Fraction(numerator, denominator)})
    return {"cover_degree": e, "genus": g, "residual_degree": a,
            "rank_used": rank, "rank_is_worst_case_upper_not_measured": rational_two_rank is None,
            "list_length_exponent": exponent, "four_prime_degrees": degrees,
            "degree_checks": tests,
            "four_list_guarantee_under_access_contract": all(t["small_bias_sufficient_condition"] for t in tests),
            "requires_exact_independent_uniform_prime_sampling": True,
            "requires_correct_degree_zero_mod_two_labels": True,
            "actual_auxiliary_divisor_constructed": False,
            "curve_primitives_implemented": False,
            "polynomial_time_for_linear_rank": False,
            "classical_hardness_established": False,
            "quantum_advantage_established": False}


def four_list_match(lists, rank, target, *, pair_cap=None):
    if type(rank) is not int or rank < 3 or type(target) is not int or not 0 <= target < 2**rank:
        raise ValueError("rank>=3 and a canonical target label required")
    lists = [tuple(values) for values in lists]
    length = 2**((rank+2)//3)
    if (len(lists) != 4 or any(len(values) != length for values in lists)
            or any(type(x) is not int or not 0 <= x < 2**rank for values in lists for x in values)):
        raise ValueError("four correctly sized lists of canonical labels required")
    if pair_cap is None:
        pair_cap = 40000*length
    if type(pair_cap) is not int or pair_cap < 1:
        raise ValueError("positive integer pair cap required")
    mask = (1 << (rank//3))-1
    counts = 0
    left = {}
    buckets = {}
    for j, value in enumerate(lists[1]):
        buckets.setdefault(value & mask, []).append(j)
    for i, value in enumerate(lists[0]):
        for j in buckets.get(value & mask, ()):
            counts += 1
            if counts > pair_cap:
                return {"status": "UNKNOWN_PAIR_CAP", "indices": None, "pairs_visited": counts,
                        "hardness_evidence": False}
            left.setdefault(value ^ lists[1][j], (i, j))
    buckets = {}
    for j, value in enumerate(lists[3]):
        buckets.setdefault(value & mask, []).append(j)
    for i, value in enumerate(lists[2]):
        for j in buckets.get((value ^ target) & mask, ()):
            counts += 1
            if counts > pair_cap:
                return {"status": "UNKNOWN_PAIR_CAP", "indices": None, "pairs_visited": counts,
                        "hardness_evidence": False}
            pair = left.get(value ^ lists[3][j] ^ target)
            if pair is not None:
                indices = (*pair, i, j)
                labels = [lists[k][index] for k, index in enumerate(indices)]
                if labels[0] ^ labels[1] ^ labels[2] ^ labels[3] != target:
                    raise ArithmeticError("coset-label verification failed")
                return {"status": "VERIFIED_LABEL_MATCH_NOT_NATIVE_WITNESS",
                        "indices": indices, "labels": labels, "pairs_visited": counts,
                        "native_relation_verified": False, "hardness_evidence": False}
    return {"status": "UNKNOWN_NO_FILTERED_MATCH", "indices": None,
            "pairs_visited": counts, "hardness_evidence": False}


def exact_uniform_moments(rank):
    """Overlap-aware moments for the uniform control, without sampling lists."""
    if type(rank) is not int or rank < 3:
        raise ValueError("rank>=3 required")
    low_bits, length = rank//3, 2**((rank+2)//3)
    mean = Fraction(length**4, 2**(rank+low_bits))
    second = Fraction(0)
    for shared in range(16):
        _, low, high = overlap_codes(shared)
        constraints = low_bits*binary_rank(low)+(rank-low_bits)*binary_rank(high)
        count = length**4*(length-1)**(4-shared.bit_count())
        second += Fraction(count, 2**constraints)
    return mean, second


def _binary_system_probability(equations):
    """Exact probability that independent uniform bits satisfy equations."""
    pivots = {}
    for row, rhs in equations:
        while row:
            bit = row.bit_length()-1
            if bit in pivots:
                other, value = pivots[bit]
                row, rhs = row ^ other, rhs ^ value
            else:
                pivots[bit] = row, rhs
                break
        else:
            if rhs:
                return Fraction(0)
    return Fraction(1, 2**len(pivots))


def mixture_joint_probability(rank, target, atoms, strengths, shared):
    """Exact two-tuple probability for uniform-plus-atom input laws.

    Each independent sample first chooses its atom or a fresh uniform
    value. Conditioning on these choices reduces to affine binary systems.
    No small-bias theorem or overlap-support inequality is used here.
    """
    if type(rank) is not int or rank < 3 or type(target) is not int or not 0 <= target < 2**rank:
        raise ValueError("rank>=3 and canonical target required")
    if len(atoms) != 4 or any(type(a) is not int or not 0 <= a < 2**rank for a in atoms):
        raise ValueError("four canonical atoms required")
    strengths = tuple(Fraction(a) for a in strengths)
    if len(strengths) != 4 or any(not 0 <= a <= 1 for a in strengths):
        raise ValueError("four mixture probabilities required")
    if type(shared) is not int or not 0 <= shared < 16:
        raise ValueError("four-bit overlap mask required")
    variables = list(range(4))
    owners = list(range(4))
    for position in range(4):
        if shared >> position & 1:
            variables.append(position)
        else:
            variables.append(len(owners))
            owners.append(position)
    size = len(owners)
    total = Fraction(0)
    for fixed in range(1 << size):
        weight = Fraction(1)
        for index, owner in enumerate(owners):
            weight *= strengths[owner] if fixed >> index & 1 else 1-strengths[owner]
        if not weight:
            continue
        probability = Fraction(1)
        for bit in range(rank):
            equations = []
            for start in (0, 4):
                groups = [(variables[start:start+4], (target >> bit) & 1)]
                if bit < rank//3:
                    groups.append((variables[start:start+2], 0))
                for indices, rhs in groups:
                    row = 0
                    for index in indices:
                        if fixed >> index & 1:
                            rhs ^= (atoms[owners[index]] >> bit) & 1
                        else:
                            row ^= 1 << index
                    equations.append((row, rhs))
            probability *= _binary_system_probability(equations)
            if not probability:
                break
        total += weight*probability
    return total


def exact_mixture_moments(rank, target, atoms, strengths):
    """Control distributions only; these are not prime-divisor samplers."""
    length = 2**((rank+2)//3)
    mean = length**4*mixture_joint_probability(rank, target, atoms, strengths, 15)
    second = Fraction(0)
    for shared in range(16):
        count = length**4*(length-1)**(4-shared.bit_count())
        second += count*mixture_joint_probability(rank, target, atoms, strengths, shared)
    return mean, second
