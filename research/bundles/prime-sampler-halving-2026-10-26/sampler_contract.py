"""Exact bounds for the mod-two sampler contract, not a curve sampler."""

from fractions import Fraction


def prime_sampling_certificate(genus):
    if type(genus) is not int or genus < 1:
        raise ValueError("positive integral genus required")
    q, degree = 100003, 1
    while q**degree < 16*(genus+1)**2*(degree+6)**2:
        degree += 1
    constant = (genus+1)*(degree+6)
    return {"q": q, "genus": genus, "prime_degree": degree,
            "exact_sufficiency_ratio": Fraction(q**degree, 16*constant**2),
            "fits_recovered_degree_i2_budget": degree <= 2*genus+4,
            "prime_sampler_truncation": 6, "pairing_truncation": 7,
            "max_mod_two_character_bias": Fraction(1, 2),
            "full_jacobian_uniformity_claimed": False,
            "exact_group_order_still_required": True,
            "access_contract_verified_by_this_control": False,
            "native_sampler_implemented": False}


def relation_batch_bound(generator_count):
    if type(generator_count) is not int or generator_count < 0:
        raise ValueError("nonnegative integral generator count required")
    rows = 0 if not generator_count else 4*(generator_count+1)
    return {"rows": rows,
            "unverified_kernel_probability_upper": (2**generator_count-1)*Fraction(3, 4)**rows,
            "false_acceptance_after_exact_verification": 0,
            "zero_false_acceptance_is_conditional_on_exact_arithmetic": True,
            "access_contract_verified_by_this_control": False,
            "requires_independent_samples": True}


def parity_law(rank, atom_weight=Fraction(1, 2)):
    """Explicit quotient control: mix the uniform law with an atom at zero."""
    if type(rank) is not int or rank < 1 or not 0 <= atom_weight <= 1:
        raise ValueError("positive rank and mixture weight in[0,1] required")
    atom_weight = Fraction(atom_weight)
    return [(1-atom_weight)/2**rank+atom_weight*(x == 0) for x in range(2**rank)]


def exact_character_bias(law, character):
    if not law or len(law) & (len(law)-1) or sum(law) != 1 or min(law) < 0:
        raise ValueError("a probability law on a binary vector space is required")
    if type(character) is not int or not 0 < character < len(law):
        raise ValueError("nonzero canonical character required")
    return sum(value*(-1)**((x & character).bit_count() % 2) for x, value in enumerate(law))
