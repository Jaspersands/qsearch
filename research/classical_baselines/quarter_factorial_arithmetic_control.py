#!/opt/anaconda3/bin/python
"""Two-prime certified classical quartic/Fitting/quarter-factorial control.

The cheap character scan stops at the first predeclared discriminating
prime. Certified quartic class computations are performed only there and
at p=13. This is finite diagnostic arithmetic, not quantum execution or
an asymptotic algorithm. Direct sums/factorials are diagnostic controls.
"""

from fractions import Fraction
from math import factorial, isqrt
from pathlib import Path
import json
import subprocess
import sys
import time

SAGE_PYTHON = "/opt/anaconda3/envs/qsearch-cas/bin/python"
PREDECLARED_PRIMES = (13, 29, 37, 53, 61, 101, 109, 149, 173, 181, 197, 229)


def cheap_character_data(p):
    k = (p - 1) // 4
    ip = min(x for x in range(1, p) if x * x % p == p - 1)
    lookup = {pow(ip, exponent, p): exponent for exponent in range(4)}
    exponents = {x: lookup[pow(x, k, p)] for x in range(1, p)}
    units = ((1, 0), (0, 1), (-1, 0), (0, -1))
    re = Fraction(-sum(x * units[exponents[x]][0] for x in range(1, p)), p)
    im = Fraction(-sum(x * units[exponents[x]][1] for x in range(1, p)), p)
    assert re.denominator == im.denominator == 1 and int(re) % 2 and int(im) % 2
    alpha_re, alpha_im = (re + im) / 2, (im - re) / 2
    alpha_norm = alpha_re**2 + alpha_im**2
    not_associate_to_conjugate = alpha_re * alpha_im != 0 and abs(alpha_re) != abs(alpha_im)
    qualifies = alpha_norm != 1 and not_associate_to_conjugate
    return {
        "prime": p, "k": k, "ip_smallest_positive_sqrt_minus_one": ip,
        "L_coordinates": [int(re), int(im)],
        "L_divided_by_one_plus_i_coordinates": [int(alpha_re), int(alpha_im)],
        "L_divided_by_one_plus_i_norm": int(alpha_norm),
        "nonassociate_to_conjugate_after_division": bool(not_associate_to_conjugate),
        "qualifies": bool(qualifies),
    }, exponents


def run_control():
    from sage.all import AA, GF, QQ, ZZ, NumberField, PolynomialRing, QuadraticField, identity_matrix, matrix, zero_matrix

    started = time.perf_counter()
    scan = []
    selected = None
    for p in PREDECLARED_PRIMES:
        row, _ = cheap_character_data(p)
        scan.append(row)
        if row["qualifies"]:
            selected = p
            break
    if selected is None:
        raise RuntimeError("No discriminating prime in the predeclared list; no enlarged scan is authorized")
    gaussian = QuadraticField(-1, "ii")
    ii = gaussian.gen()
    two_prime = gaussian.ideal(1 + ii)

    def certify(field):
        bnf = field.pari_bnf(proof=True)
        certificate = int(bnf.bnfcertify())
        assert certificate == 1
        return field.class_group(proof=True), certificate

    def ideal_record(ideal):
        return {"norm": str(ideal.norm()), "PARI_integer_basis_HNF": str(ideal.pari_hnf()),
                "reduced_generators": [str(v) for v in ideal.gens_reduced()]}

    def remove_two(ideal):
        valuation = int(ideal.valuation(two_prime))
        return ideal / two_prime**valuation, valuation

    def gaussian_fitting(invariants, sigma_action):
        dimension = len(invariants)
        if dimension > 1:
            return None, {"status": "blocked", "reason": "Selected class group needs a multigenerator Gaussian presentation; this bounded control does not build a general module framework"}
        if dimension == 0:
            return gaussian.ideal(1), {"status": "complete", "presentation_generators": 0,
                                      "Gaussian_relations": [], "minus_quotient_invariants": []}
        conjugation = sigma_action * sigma_action
        for row in range(dimension):
            for column in range(dimension):
                conjugation[row, column] %= invariants[row]
        one_plus_j = identity_matrix(ZZ, dimension) + conjugation
        abelian_rows = [[int(value) for value in row] for row in matrix.diagonal(ZZ, invariants).rows()]
        quotient_rows = abelian_rows + [[int(value) for value in column] for column in one_plus_j.columns()]
        quotient_relations = matrix(ZZ, quotient_rows)
        smith = quotient_relations.smith_form(transformation=False)
        quotient_invariants = [int(abs(value)) for value in smith.diagonal() if abs(value) > 1]
        # At the two authorized primes this is a cyclic (or zero) module.
        # Fitt_0 of a one-generator presentation is the ideal of its row
        # entries, computed by Gaussian ideal HNF, with no minor enumeration.
        relations = [gaussian(invariants[0]), gaussian(one_plus_j[0, 0]), ii - sigma_action[0, 0]]
        fitting = gaussian.ideal(relations)
        return fitting, {
            "status": "complete", "presentation_generators": 1,
            "Gaussian_relations": [str(value) for value in relations],
            "minus_quotient_definition": "Cl(K)/(1+sigma^2)Cl(K)",
            "integer_quotient_relation_rows": quotient_rows,
            "minus_quotient_invariants": quotient_invariants,
            "Gaussian_Fitting_method": "one-generator relation ideal, exact Gaussian/PARI HNF",
        }

    def endpoint(p, data, exponents, L):
        k = data["k"]
        ip = data["ip_smallest_positive_sqrt_minus_one"]
        imaginary = QuadraticField(-p, "sqrt_minus_p")
        Cimag, cert_imag = certify(imaginary)
        assert imaginary.discriminant() == -4 * p
        h_imag = int(Cimag.order())
        assert h_imag % 2 == 0
        C = h_imag // 2
        real = QuadraticField(p, "sqrt_p")
        Creal, cert_real = certify(real)
        h_real = int(Creal.order())
        units = real.units(proof=True)
        assert len(units) == 1
        unit = units[0]
        positive = next(embedding for embedding in real.embeddings(AA) if embedding(real.gen()) > 0)
        if positive(unit) < 0:
            unit = -unit
        if positive(unit) < 1:
            unit = unit**-1
        assert positive(unit) > 1 and unit.norm() == -1 and h_real % 2 == 1
        half = (-1) ** ((h_real + 1) // 2) * int(GF(p)(unit.polynomial()[0])) % p
        direct_half = factorial((p - 1) // 2) % p
        assert half == direct_half
        representations = []
        for a0 in range(-isqrt(p), isqrt(p) + 1):
            remainder = p - a0 * a0
            if a0 % 4 == 1 and remainder > 0 and isqrt(remainder) ** 2 == remainder:
                representations.append((a0, isqrt(remainder)))
        assert len(representations) == 1
        a0, b0 = representations[0]
        radicand = half * pow((2 * a0) % p, -1, p) % p
        root = GF(p)(radicand).sqrt()
        roots = sorted({int(root), int(-root)})
        assert len(roots) == 2 and k % 2 == 1
        chi_two = ii ** exponents[2]

        def selection(value_L, omit_half=False):
            S = (3 + chi_two.conjugate()) * value_L / (1 if omit_half else 2)
            re, im = QQ(S.polynomial()[0]), QQ(S.polynomial()[1])
            exponent = im - re + QQ(k + C) / 2
            assert exponent.denominator() == 1
            exponent = int(exponent)
            target_character = pow(ip, exponent, p)
            candidates = [value for value in roots if pow(value, k, p) == target_character]
            answer = candidates[0] if len(candidates) == 1 else None
            return {"S_coordinates": [str(re), str(im)], "E": exponent, "E_mod_four": exponent % 4,
                    "target_quartic_character_mod_p": target_character, "selected_roots": candidates,
                    "selected_G": answer, "matches_direct_G": answer == direct_G}

        direct_G = factorial(k) % p
        return {
            "imaginary_discriminant": int(imaginary.discriminant()), "imaginary_class_number_h_minus_4p": h_imag,
            "imaginary_bnf_certified": cert_imag == 1, "C_h_minus_4p_over_two": C,
            "real_class_number": h_real, "real_bnf_certified": cert_real == 1,
            "positive_real_fundamental_unit": str(unit), "arithmetic_half_factorial": half,
            "direct_half_factorial": direct_half, "a0_b0": [a0, b0],
            "square_root_radicand_half_over_2a0": radicand, "two_square_root_candidates": roots,
            "chi_two_i_exponent": exponents[2], "direct_quarter_factorial": direct_G,
            "correct_L_selection": selection(L),
            "wrong_conjugated_L_selection": selection(L.conjugate()),
            "wrong_omitted_division_by_two_selection": selection(L, omit_half=True),
        }

    results = []
    for p in dict.fromkeys((13, selected)):
        case_started = time.perf_counter()
        data, exponents = cheap_character_data(p)
        L = gaussian(data["L_coordinates"][0]) + data["L_coordinates"][1] * ii
        chi = {0: gaussian(0), **{x: ii**exponents[x] for x in range(1, p)}}
        J = sum((chi[x] * chi[(1 - x) % p] for x in range(p)), gaussian(0))
        a, b = ZZ(J.polynomial()[0]), ZZ(J.polynomial()[1])
        assert a * a + b * b == p and a != 0 and b % 2 == 0
        polynomial_ring = PolynomialRing(QQ, "x")
        x = polynomial_ring.gen()
        polynomial = x**4 + p * x**2 + QQ(p) * b**2 / 4
        field = NumberField(polynomial, "theta")
        theta = field.gen()
        r = (2 * theta**2 + p) / a
        sigma = field.hom([b * r / (2 * theta)], field)
        assert r**2 == p and sigma(r) == -r
        assert sigma(sigma(theta)) == -theta and sigma(sigma(sigma(sigma(theta)))) == theta
        classes, certificate = certify(field)
        invariants = [int(value) for value in classes.invariants()]
        images, ideal_generators = [], []
        for generator in classes.gens():
            ideal = generator.ideal()
            sigma_ideal = field.ideal([sigma(value) for value in ideal.gens()])
            images.append([int(value) for value in classes(sigma_ideal).exponents()])
            ideal_generators.append([str(value) for value in ideal.gens()])
        size = len(invariants)
        action = matrix(ZZ, size, size, lambda row, column: images[column][row]) if size else zero_matrix(ZZ, 0, 0)
        for column in range(size):
            assert all((action**4 - identity_matrix(ZZ, size))[row, column] % invariants[row] == 0 for row in range(size))
        fitting, presentation = gaussian_fitting(invariants, action)
        case = {
            **data, "Jacobi_sum_J": str(J), "Jacobi_coordinates_a_b": [int(a), int(b)],
            "quartic_polynomial": str(polynomial), "quartic_discriminant": int(field.discriminant()),
            "quartic_bnf_certified": certificate == 1,
            "class_group_invariants": invariants, "class_number": int(classes.order()),
            "class_generator_ideal_generators": ideal_generators,
            "sigma_theta": str(sigma(theta)), "sigma_r_equals_minus_r": True,
            "sigma_order_four_verified": True,
            "sigma_class_action_columns": images,
            "minus_quotient_and_Gaussian_presentation": presentation,
        }
        if fitting is not None:
            target = gaussian.ideal(L.conjugate())
            wrong_target = gaussian.ideal(L)
            stripped_fitting, fitting_two_val = remove_two(fitting)
            stripped_target, target_two_val = remove_two(target)
            inverse_action = action**3
            for row in range(size):
                for column in range(size):
                    inverse_action[row, column] %= invariants[row]
            inverse_fitting, _ = gaussian_fitting(invariants, inverse_action)
            case["Fitting_checks"] = {
                "Fitting_ideal": ideal_record(fitting), "conjugate_L_ideal": ideal_record(target),
                "Fitting_two_prime_valuation": fitting_two_val, "conjugate_L_two_prime_valuation": target_two_val,
                "localized_Fitting_equals_conjugate_L": stripped_fitting == stripped_target,
                "integral_Fitting_without_restoration_equals_conjugate_L": fitting == target,
                "restore_one_plus_i_equals_conjugate_L": fitting * two_prime == target,
                "wrong_unconjugated_L_target_matches_restored_Fitting": fitting * two_prime == wrong_target,
                "wrong_inverse_sigma_Fitting": ideal_record(inverse_fitting),
                "wrong_inverse_sigma_restored_matches_L_instead": inverse_fitting * two_prime == wrong_target,
                "wrong_inverse_sigma_restored_matches_conjugate_L": inverse_fitting * two_prime == target,
            }
        case["endpoint"] = endpoint(p, data, exponents, L)
        case["seconds"] = time.perf_counter() - case_started
        results.append(case)
    output = {
        "scope": "Finite certified classical diagnostic only. Direct character/Jacobi sums and factorials enumerate their arguments; no quantum execution, compact arithmetic implementation, asymptotic inference, or exact theorem proof.",
        "predeclared_prime_list": list(PREDECLARED_PRIMES), "cheap_scan_prefix": scan,
        "first_discriminating_prime": selected, "certified_quartic_primes": [row["prime"] for row in results],
        "Gaussian_orientation": "i acts by the explicit sigma(theta)=b*r/(2*theta), r=(2*theta^2+p)/a, J=a+i*b; chi maps the smallest positive ip square root of -1 to i",
        "minus_quotient_convention": "Cl(K)/(1+sigma^2)Cl(K); localization at 2 is compared explicitly",
        "results": results, "total_worker_seconds": time.perf_counter() - started,
    }
    artifact = Path(__file__).with_suffix(".json")
    artifact.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"artifact": str(artifact), "selected_prime": selected, "results": [
        {"p": row["prime"], "L": row["L_coordinates"], "J": row["Jacobi_coordinates_a_b"],
         "class_invariants": row["class_group_invariants"], "sigma_columns": row["sigma_class_action_columns"],
         "fitting": row.get("Fitting_checks", {}), "endpoint": row["endpoint"], "seconds": row["seconds"]}
        for row in results], "worker_seconds": output["total_worker_seconds"]}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--sage-worker"]:
        run_control()
    elif not sys.argv[1:]:
        subprocess.run([SAGE_PYTHON, str(Path(__file__).resolve()), "--sage-worker"], check=True, timeout=120)
    else:
        raise SystemExit("Usage: quarter_factorial_arithmetic_control.py")
