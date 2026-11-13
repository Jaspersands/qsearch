"""One exact tagged-parity descent control; not a tower implementation.

Run with the Sage Python listed in research/TOOLBOX.md.  All class/Selmer
computations are independent finite controls, not proposed algorithm oracles.
"""

import json
from pathlib import Path

from sage.all import *
from sage.env import SAGE_VERSION


def rows(M):
    return [[int(x) for x in row] for row in M.rows()]


def main():
    proof.all(True)
    checks = {}

    def require(name, condition):
        checks[name] = bool(condition)
        if not checks[name]:
            raise AssertionError(name)

    Qx = PolynomialRing(QQ, "x")
    x = Qx.gen()
    F = NumberField(x*x + 14, "a")
    a = F.gen()
    S = F.primes_above(2) + F.primes_above(7)
    E = [F.ideal(3, a+1), F.ideal(3, a+2)]
    RF = PolynomialRing(F, "z")
    z = RF.gen()
    L = F.extension(z*z - 2, "b")
    b = L.gen()
    A = L.absolute_field("t")
    fromA, toA = A.structure()
    aA = toA(L(a))
    SA = A.primes_above(2) + A.primes_above(7)
    above3 = A.primes_above(3)
    EA = []
    for offset in [1, 2]:
        candidates = [P for P in above3 if (aA+offset).valuation(P) > 0]
        require(f"one_upper_prime_over_base_prime_{offset}", len(candidates) == 1)
        EA.append(candidates[0])

    FS, fgens, ffrom, fto = F.selmer_space(S, ZZ(2), proof=True)
    FT, tgens, tfrom, tto = F.selmer_space(S+E, ZZ(2), proof=True)
    LS, lgens, lfrom, lto = A.selmer_space(SA, ZZ(2), proof=True)
    LT, egens, efrom, eto = A.selmer_space(SA+EA, ZZ(2), proof=True)

    base = [F(-1), F(2), a, (a-2)/9, F(1)]
    first_tags = [0, 0, 0, 0, 1]
    betas = [3*(b-1), b+2, (a/4-1)*b-F(1)/2,
             (-(a+10)*b+2*(a+7))/12, L(1)]
    target = vector(GF(2), [0, 1])
    first_pairs = matrix(GF(2),
        [list(fto(t))+[c] for t, c in zip(base, first_tags)])

    require("nonodd_base_S_class", F.S_class_group(S=S, proof=True).invariants() == (2,))
    require("relative_extension_unramified", L.relative_discriminant() == F.ideal(1))
    require("base_dimension_four", FS.dimension() == 4)
    require("first_pair_dimension_five", first_pairs.rank() == 5)
    require("first_element_projection_rank_four", first_pairs[:, :FS.dimension()].rank() == 4)
    require("pure_tag_retained", list(first_pairs.row(4)) == [0, 0, 0, 0, 1])
    require("all_first_classes_norm_compatible",
        all(F.hilbert_symbol(t, F(2), P) == 1 for t in base for P in S))
    require("exact_norm_witnesses",
        [t.relative_norm() for t in betas] == [F(-9), F(2), a, base[3], F(1)])
    relative_residue_degrees = [ZZ(PA.residue_class_degree()) // ZZ(P.residue_class_degree())
                               for P, PA in zip(E, EA)]
    require("both_extra_primes_inert", relative_residue_degrees == [2, 2])
    norm_target = vector(GF(2), [int(f)*int(t) % 2
                              for f, t in zip(relative_residue_degrees, target)])
    require("norm_of_target_parity_zero", norm_target.is_zero())

    # Compute residuals directly upstairs, before identifying the base pullback.
    upper_beta_parities = matrix(GF(2),
        [[ZZ(toA(t).valuation(P)) % 2 for t in betas] for P in EA])
    residuals = matrix(GF(2),
        [upper_beta_parities.column(i)+first_tags[i]*target for i in range(5)]).transpose()
    expected_residuals = matrix(GF(2), [[1, 0, 0, 0, 0], [1, 0, 0, 1, 1]])
    require("residual_columns_include_target_tag", residuals == expected_residuals)

    W = matrix(GF(2), [[ZZ(t.valuation(P)) % 2 for t in tgens] for P in E])
    obstruction = W.left_kernel().basis_matrix()*residuals
    require("obstruction_is_last_two_tags_sum",
        rows(obstruction) == [[0, 0, 0, 1, 1]])

    # Second lower generalized-pair space, built independently in F(S union E,2).
    D = W.augment(residuals)
    second = D.right_kernel()
    B2 = second.basis_matrix()
    require("second_lower_dimension_eight", second.dimension() == 8)

    # Step-4 map, retaining the output tag as an actual coordinate.
    columns = [vector(GF(2), list(eto(toA(L(t))))+[0]) for t in tgens]
    columns += [vector(GF(2), list(eto(toA(t)))+[c])
                for t, c in zip(betas, first_tags)]
    descent = matrix(GF(2), columns).transpose()
    images = B2*descent.transpose()

    # Independent upper reference: all supported squareclasses, constrained
    # directly by the target parity at the actual two upper primes.
    upper_valuations = matrix(GF(2), [[ZZ(t.valuation(P)) % 2
                                     for t in egens] for P in EA])
    upper_constraints = upper_valuations.augment(matrix(GF(2), 2, 1, list(target)))
    upper_reference = upper_constraints.right_kernel()
    require("upper_reference_dimension_seven", upper_reference.dimension() == 7)
    require("descent_image_dimension_seven", images.rank() == 7)
    require("descent_image_equals_full_upper_reference", images.row_space() == upper_reference)

    d_pair = vector(GF(2), list(tto(F(2)))+[0]*5)
    kernel_relations = images.left_kernel()
    kernel_ambient = kernel_relations.basis_matrix()*B2
    require("map_kernel_dimension_one", kernel_relations.dimension() == 1)
    require("kernel_is_exactly_d_with_zero_tags", kernel_ambient.row(0) == d_pair)
    require("d_is_nonzero_downstairs", not d_pair.is_zero())
    require("d_maps_to_zero_upstairs", (descent*d_pair).is_zero())

    tagged_beta4 = vector(GF(2), [0]*FT.dimension()+[0, 0, 0, 1, 1])
    tagged_image = descent*tagged_beta4
    expected_tagged_image = vector(GF(2), list(eto(toA(betas[3])))+[1])
    require("beta4_plus_tag_combination_is_admissible", (D*tagged_beta4).is_zero())
    require("tagged_beta4_has_expected_nonzero_image",
        tagged_image == expected_tagged_image and tagged_image[-1] == 1)
    untagged_beta4 = vector(GF(2), list(eto(toA(betas[3])))+[0])
    require("beta4_without_tag_fails_upper_constraint",
        not (upper_constraints*untagged_beta4).is_zero())

    zero_output_tag = matrix(GF(2), 1, FT.dimension()+5,
                             [0]*(FT.dimension()+4)+[1])
    untagged_domain = D.stack(zero_output_tag).right_kernel().basis_matrix()
    untagged_rank = (untagged_domain*descent.transpose()).rank()
    require("discarding_tag_loses_one_output_dimension", untagged_rank == 6)

    result = {
        "status": "EXACT_TAGGED_PARITY_CONTROL_PASS",
        "scope": "One fixed quartic control only; no tower complexity theorem.",
        "sage_version": SAGE_VERSION,
        "proof": True,
        "base_polynomial": str(F.defining_polynomial()),
        "absolute_polynomial": str(A.defining_polynomial()),
        "base_generator_in_absolute": str(aA),
        "relative_generator_in_absolute": str(toA(b)),
        "base_supported_generators": [str(t) for t in fgens],
        "base_expanded_generators": [str(t) for t in tgens],
        "upper_expanded_generators": [str(t) for t in egens],
        "first_native_elements": [str(t) for t in base],
        "norm_lifts": [str(t) for t in betas],
        "support_rational_primes": [2, 7],
        "extra_base_primes": [str(P) for P in E],
        "extra_upper_primes": [str(P) for P in EA],
        "upper_target_prime": str(EA[1]),
        "norm_target_parity": list(map(int, norm_target)),
        "first_pair_matrix": rows(first_pairs),
        "residual_matrix": rows(residuals),
        "base_expanded_valuation_matrix": rows(W),
        "obstruction_matrix": rows(obstruction),
        "second_pair_basis": rows(B2),
        "upper_constraint_matrix": rows(upper_constraints),
        "upper_image_basis": rows(images.row_space().basis_matrix()),
        "kernel_ambient": rows(kernel_ambient),
        "d_pair_coordinates": list(map(int, d_pair)),
        "tagged_beta4_image": list(map(int, tagged_image)),
        "dimensions": {
            "base_supported": int(FS.dimension()),
            "first_pair": int(first_pairs.rank()),
            "second_pair": int(second.dimension()),
            "upper_supported": int(LS.dimension()),
            "upper_expanded": int(LT.dimension()),
            "upper_generalized_reference": int(upper_reference.dimension()),
            "descent_image": int(images.rank()),
            "descent_kernel": int(kernel_relations.dimension()),
            "image_if_tag_discarded": int(untagged_rank),
        },
        "checks": checks,
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(result["status"])
    print("checks", len(checks), "dimensions", result["dimensions"])
    print("output", output)


if __name__ == "__main__":
    main()
