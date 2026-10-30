"""Spanning-block preconditioning for regular mixed-order SDE witnesses.

Atoms are PUBLIC label sums, not synthesized quantum states. Any nonzero
field SDE solution activates a whole spanning raw block. This generic
wrapper adds no field-size guard; execution still requires an implemented
field backend. Published general-arity bounds are reported, not executed.
"""
from fractions import Fraction
from math import gcd
import random

from theorems.power_sde import field_threshold
from theorems.power_sde_budget import RandomnessExhausted
from theorems.prime_character_opi import ring
from theorems.prime_power_rees_descent import _module_contract, lift_regular_module_witness
from theorems.symbolic_scalar_phase_erasure import _fmpz_rref
from theorems.weighted_two_erasure_cascade import (
    required_bezout_arity, solve_bezout_sde_weights, verify_general_degree_witness,
)


def _pair(x):
    return [x.numerator,x.denominator]


def span_backend_rng(plan, bit_source=None):
    """Validate backend randomness before any public-label acquisition."""
    rng = random.SystemRandom() if bit_source is None else bit_source
    if plan["reduced_degree"]>1:
        protocol = "getrandbits" if plan["field_randomness_fully_capped"] else "randrange"
        if not callable(getattr(rng,protocol,None)):
            raise ValueError(f"selected field backend requires callable {protocol}")
    return rng


def published_sde_arity(rank, reduced_degree):
    """Ivanyos--Santha G(g,r)^ceil(log2(g+1)); not an implemented solver."""
    if type(rank) is not int or rank < 0 or type(reduced_degree) is not int or reduced_degree < 1:
        raise ValueError("nonnegative rank and positive reduced degree required")
    if not rank:
        return 1
    if reduced_degree == 1:
        return rank+1
    g = reduced_degree
    return (g**(g*(g-1)//2)*(rank+1)**g)**g.bit_length()


def span_grade_plan(*, prime, cyclic_rank, degree, failure_bits=8,
                     ambient_cyclic_rank=None, published_bound=False):
    ring(prime)
    if type(cyclic_rank) is not int or cyclic_rank < 1:
        raise ValueError("positive intrinsic cyclic rank required")
    if type(degree) is not int or not 1 <= degree < prime or prime < 3:
        raise ValueError("odd prime and 1 <= degree < prime required")
    if type(failure_bits) is not int or failure_bits < 4:
        raise ValueError("failure_bits must be at least four")
    ambient = cyclic_rank if ambient_cyclic_rank is None else ambient_cyclic_rank
    if type(ambient) is not int or ambient < cyclic_rank:
        raise ValueError("ambient rank must bound intrinsic rank")
    if type(published_bound) is not bool:
        raise ValueError("published_bound must be boolean")
    g = gcd(degree,prime-1)
    arity = lambda r: published_sde_arity(r,g) if published_bound else required_bezout_arity(prime,degree,r)
    atoms, ambient_atoms = arity(cyclic_rank), arity(ambient)
    attempts = failure_bits+(atoms-1).bit_length()
    ambient_attempts = failure_bits+(ambient_atoms-1).bit_length()
    rejection = Fraction(1,prime*(prime-1))
    block_abort = atoms*rejection**attempts
    # Published-bound mode imports a correct expected-polynomial field solver;
    # actual local backends instead have a separately allocated sampler abort.
    field_abort = Fraction(0) if published_bound or g==1 else Fraction(1,2**failure_bits)
    pilots = Fraction(1,prime*prime*(prime-1))
    cap = ambient+2+ambient_atoms*(ambient+1)*ambient_attempts
    if block_abort > Fraction(1,2**failure_bits) or pilots+block_abort+field_abort > Fraction(1,4):
        raise ArithmeticError("source failure allocation exceeded")
    bounded_field = g==1 or prime>=field_threshold(g)
    return {"prime":prime,"degree":degree,"reduced_degree":g,"cyclic_rank":cyclic_rank,
            "ambient_cyclic_rank":ambient,"failure_bits":failure_bits,
            "status":"IMPORTED_SDE_BOUND_ONLY" if published_bound else "IMPLEMENTED_BACKEND_SOURCE_BOUND",
            "field_backend_implemented":not published_bound,
            "atom_count":atoms,"raw_block_width":cyclic_rank+1,"attempts_per_atom":attempts,
            "raw_block_rejection_upper":_pair(rejection),"block_exhaustion_upper":_pair(block_abort),
            "field_sampler_abort_upper":_pair(field_abort),"pilot_incompleteness_upper":_pair(pilots),
            "episode_abort_upper":_pair(pilots+block_abort+field_abort),
            "raw_bank_sources_upper":atoms*(cyclic_rank+1)*attempts,
            "pilot_sources":ambient+2,"predecessors_per_episode_upper":cap,
            "expected_predecessors_upper":2*cap,
            "field_randomness_fully_capped":bounded_field and not published_bound,
            "expected_field_arithmetic_dependency":not bounded_field or published_bound,
            "wrapper_adds_prime_size_guard":False,"iid_intrinsic_sources_required":True,
            "pilot_coordinate_acquisition_implemented":False}


def expand_atom_witness(*, prime, exponents, degree, blocks, atom_weights):
    """Verify raw spans and atom SDE before lifting; keep ORIGINAL row rank."""
    exponents, blocks = tuple(exponents), tuple(tuple(tuple(c) for c in b) for b in blocks)
    if not blocks or len(atom_weights) != len(blocks):
        raise ValueError("one coefficient per nonempty raw block required")
    rank = len(exponents)
    atoms = []
    for block in blocks:
        canonical, _, _ = _module_contract(block,exponents,prime,degree)
        if len(canonical) != rank+1:
            raise ValueError("raw block width must be intrinsic rank+1")
        field = [tuple(a%prime for a in col) for col in canonical]
        if _fmpz_rref(list(map(list,zip(*field))),prime)[1] != rank:
            raise ValueError("raw block does not span original intrinsic module modulo p")
        atoms.append(tuple(sum(col[j] for col in field)%prime for j in range(rank)))
    verify_general_degree_witness(prime,atoms,atom_weights,degree)
    expanded = [w for w,block in zip(atom_weights,blocks) for _ in block]
    raw = [col for block in blocks for col in block]
    lift = lift_regular_module_witness(raw,expanded,prime=prime,exponents=exponents,degree=degree)
    if not lift["original_module_verified"]:
        raise ArithmeticError("spanning-block expansion lost regularity")
    return {"atoms":atoms,"atom_weights":list(atom_weights),"expanded_field_witness":expanded,
            "raw_columns":raw,"lift":lift}


def spanning_module_witness(*, prime, exponents, degree, draw_block, bit_source=None,
                            failure_bits=8, ambient_cyclic_rank=None):
    """Consume raw blocks only after validating the selected RNG protocol.

    Nonlinear capped backends need getrandbits; expected-time small-field
    backends need randrange. Degree-one reduction needs neither.
    """
    exponents = tuple(exponents)
    _module_contract([(0,)*len(exponents)],exponents,prime,degree)
    plan = span_grade_plan(prime=prime,cyclic_rank=len(exponents),degree=degree,
                           failure_bits=failure_bits,ambient_cyclic_rank=ambient_cyclic_rank)
    if not callable(draw_block):
        raise ValueError("draw_block callback required")
    g = plan["reduced_degree"]
    rng = span_backend_rng(plan,bit_source)
    records, accepted, blocks = [], [], []
    result = {"status":"ABORT","prime":prime,"degree":degree,"exponents":exponents,
              "plan":plan,"trials":records,"accepted_trial_indices":accepted,
              "source_columns_consumed":0,"pilots_executed":False,"quantum_receiver_executed":False}
    for atom in range(plan["atom_count"]):
        for attempt in range(plan["attempts_per_atom"]):
            block,_,_ = _module_contract(draw_block(plan["raw_block_width"]),exponents,prime,degree)
            if len(block) != plan["raw_block_width"]:
                raise ValueError("source returned wrong raw block width")
            result["source_columns_consumed"] += len(block)
            field = [tuple(a%prime for a in col) for col in block]
            rank = _fmpz_rref(list(map(list,zip(*field))),prime)[1]
            record = {"atom":atom,"attempt":attempt,"columns":block,"raw_rank":rank,
                      "status":"ACCEPTED" if rank==len(exponents) else "RAW_RANK_REJECT"}
            records.append(record)
            if rank == len(exponents):
                accepted.append(len(records)-1)
                blocks.append(block)
                break
        else:
            result["reason"] = "spanning block attempt budget exhausted"
            return result
    atoms = [tuple(sum(col[j] for col in block)%prime for j in range(len(exponents))) for block in blocks]
    try:
        weights,atom_rank,_,_ = solve_bezout_sde_weights(
            prime,atoms,degree,rng=rng,
            bounded_randomness_bits=failure_bits if plan["field_randomness_fully_capped"] else None,
            conic_attempt_cap=failure_bits+2,
            nonresidue_attempt_cap=g*(failure_bits+2),
            curve_attempt_cap=(9 if g==3 else 2*g)*(failure_bits+2))
    except RuntimeError as error:
        declared = ("bounded conic sampler exhausted", "bounded power-coset generator sampler exhausted",
                    "bounded odd-power scalar curve sampler exhausted",
                    "bounded ternary cubic curve sampler exhausted", "bounded cubic-nonresidue sampler exhausted")
        if not (isinstance(error,RandomnessExhausted) or str(error) in declared):
            raise
        result.update(reason="field sampler budget exhausted",field_error=str(error))
        return result
    result.update(expand_atom_witness(prime=prime,exponents=exponents,degree=degree,
                                      blocks=blocks,atom_weights=weights))
    result.update(status="VERIFIED_SPANNING_MODULE_WITNESS",atom_equation_rank=atom_rank,
                  reason="raw-module verification; source law remains an external promise")
    return result


def report():
    cases = []
    profiles = [(3,2,(2,3,4,2)),(7,3,(2,3,4)),(13,3,(2,4,3)),(1031,2,(1,2,4,3))]
    for index,(prime,degree,exponents) in enumerate(profiles):
        labels = random.Random(20261029+index)
        def draw(width):
            return [tuple(labels.randrange(prime**e) for e in exponents) for _ in range(width)]
        case = spanning_module_witness(prime=prime,degree=degree,exponents=exponents,draw_block=draw,
                                       bit_source=random.Random(31029+index))
        case.update(label_seed=20261029+index,solver_seed=31029+index)
        cases.append(case)
    # All atom sums vanish modulo p while the RAW label span has rank two.
    block = [(1,0),(0,1),(6,6)]
    zero_atom = spanning_module_witness(prime=7,degree=3,exponents=(2,3),
                                       draw_block=lambda width:block,bit_source=random.Random(1))
    return {"status":"SPANNING_PRECONDITIONING_NOT_QUANTUM_RECEIVER","cases":cases,
            "zero_atom_rank_falsifier":zero_atom,
            "proof_note":"research/SPANNING_BLOCK_REGULAR_SDE.md",
            "published_general_bound":span_grade_plan(prime=5,degree=4,cyclic_rank=2,published_bound=True),
            "all_prime_general_sde_implemented":False,
            "pilot_coordinate_acquisition_implemented":False,"quantum_receiver_executed":False,
            "physical_iid_source_certified":False,"speedup_established":False,
            "whole_workflow_clock_enforced":False}
