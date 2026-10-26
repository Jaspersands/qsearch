"""Full p-torsion words from a public integer relation lattice.

This repairs arbitrary-generator powering in a semi-elementary HSP descent.
It is ordinary integer/field algebra, not a quantum HSP implementation.
Completeness of the supplied relation lattice is an external obligation.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path

from flint import fmpz, fmpz_mat, fmpz_mod_ctx, fmpz_mod_mat


def _left_kernel_mod_prime(rows, p):
    # The older scalar-erasure nullspace helper excludes p=2; this step must not.
    width = len(rows)
    matrix = fmpz_mod_mat([[rows[j][i] % p for j in range(width)]
                           for i in range(width)], fmpz_mod_ctx(p))
    reduced, rank = matrix.rref()
    pivots = [next(j for j in range(width) if reduced[i, j]) for i in range(rank)]
    basis = []
    for free in range(width):
        if free in pivots:
            continue
        vector = [0]*width
        vector[free] = 1
        for i, pivot in enumerate(pivots):
            vector[pivot] = -int(reduced[i, free]) % p
        basis.append(tuple(vector))
    return tuple(basis)


def _row_hnf(rows):
    reduced = fmpz_mat(rows).hnf()
    return tuple(tuple(int(reduced[i, j]) for j in range(reduced.ncols()))
                 for i in range(reduced.nrows())
                 if any(reduced[i, j] for j in range(reduced.ncols())))


@dataclass(frozen=True)
class TorsionWords:
    prime: int
    relation_basis: tuple[tuple[int, ...], ...]
    modular_relation_coefficients: tuple[tuple[int, ...], ...]
    generator_words: tuple[tuple[int, ...], ...]
    preimage_lattice_basis: tuple[tuple[int, ...], ...]
    quotient_order: int
    torsion_order: int
    descent_index: int
    input_relation_completeness_certified: bool = False

    @property
    def elementary_quotient(self):
        return self.descent_index == 1


def p_torsion_words(prime, relation_basis):
    """Return all A[p] generators for A=Z^k/row_Z(R), without enumeration.

    R must be a COMPLETE square full-rank integer relation basis for the
    public quotient. Returned integer vectors are words in its original
    generators; they are not field elements to reduce modulo p.
    """
    if type(prime) is not int or prime < 2 or not fmpz(prime).is_prime():
        raise ValueError("a prime integer is required")
    rows = tuple(tuple(row) for row in relation_basis)
    width = len(rows)
    if (not width or any(len(row) != width for row in rows)
            or any(type(x) is not int for row in rows for x in row)):
        raise ValueError("a nonempty square integer relation basis is required")
    order = abs(int(fmpz_mat(rows).det()))
    if not order:
        raise ValueError("finite quotient requires a full-rank relation lattice")
    remaining = order
    while remaining % prime == 0:
        remaining //= prime
    if remaining != 1:
        raise ValueError("the public quotient must be a p-group")
    coefficients = _left_kernel_mod_prime(rows, prime)
    words = []
    for a in coefficients:
        product = tuple(sum(a[i]*rows[i][j] for i in range(width)) for j in range(width))
        if any(x % prime for x in product):
            raise ArithmeticError("modular relation does not lift integrally")
        words.append(tuple(x//prime for x in product))
    words = tuple(words)
    preimage = _row_hnf(rows+words)
    index = abs(int(fmpz_mat(preimage).det()))
    torsion_order = prime**len(words)
    if index*torsion_order != order:
        raise ArithmeticError("generated preimage has the wrong exact lattice index")
    return TorsionWords(prime, rows, coefficients, words, preimage,
                        order, torsion_order, index)


def evaluate_preimage_generators(certificate, quotient_generators, kernel_generators,
                                *, identity, multiply, power):
    """Lift the FULL preimage: retain known kernel generators explicitly.

    The input supplies B normal in K with K/B abelian and a complete relation
    lattice for the listed coset generators. No unknown H or source is used.
    The callbacks implement public operations, including negative powers.
    """
    quotient_generators = tuple(quotient_generators)
    if len(quotient_generators) != len(certificate.relation_basis):
        raise ValueError("one original group generator per relation column required")
    result = list(kernel_generators)
    for word in certificate.generator_words:
        value = identity
        for generator, exponent in zip(quotient_generators, word):
            value = multiply(value, power(generator, exponent))
        result.append(value)
    return tuple(result)


def mixed_generator_control(p):
    certificate = p_torsion_words(p, ((p*p, 0), (-p, p)))
    # Public quotient coordinates: g1=(1,0), g2=(1,1) in C_(p^2) x C_p.
    images = tuple(((x+y) % (p*p), y % p) for x, y in certificate.generator_words)
    if images != ((p, 0), (0, 1)):
        raise ArithmeticError("mixed-generator torsion repair lost a cyclic factor")
    return {
        "prime": p, "prime_bits": p.bit_length(),
        "public_relation_basis": certificate.relation_basis,
        "torsion_words": certificate.generator_words,
        "repaired_images": images,
        "naive_top_power_images": ((p, 0), (p, 0)),
        "naive_torsion_order": p,
        "actual_torsion_order": certificate.torsion_order,
        "hidden_line_0_1_survives_naive_step": False,
        "hidden_line_0_1_survives_repaired_step": True,
        "descent_index": certificate.descent_index,
    }


def build_report():
    elementary = p_torsion_words(3, ((3, 0), (0, 3)))
    trivial = p_torsion_words(2, ((1, 0), (0, 1)))
    return {
        "status": "PUBLIC_TORSION_DESCENT_REPAIR_UNDER_REVIEW",
        "controls": [mixed_generator_control(p) for p in (2, 3, 5, 2**127-1)],
        "elementary_control": asdict(elementary),
        "trivial_control": asdict(trivial),
        "hidden_source_calls": 0,
        "field_enumeration_used": False,
        "factorization_used": False,
        "relation_acquisition_implemented": False,
        "input_relation_completeness_certified": False,
        "full_outer_hsp_implemented": False,
        "noiseless_rees_core_refuted": False,
        "independent_review": False,
        "novelty_established": False,
        "speedup_claim_allowed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    content = json.dumps(build_report(), indent=2)+"\n"
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/abelian_quotient_torsion.json"
        path.write_text(content)
        print(path)
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
