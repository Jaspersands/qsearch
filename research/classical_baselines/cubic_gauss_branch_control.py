#!/opt/anaconda3/bin/python
"""Four exact cubic Gauss-sum branch controls; direct classical enumeration.

The standard-library driver invokes the local Sage worker once. The orbit
representatives below are arbitrary canonical integer representatives, not
Ito's geometric representative system. No asymptotic inference is made.
"""

import json
from math import isqrt
from pathlib import Path
import subprocess
import sys
import time

SAGE_PYTHON = "/opt/anaconda3/envs/qsearch-cas/bin/python"
PRIMES = (7, 13, 19, 31)


def primary_coefficients(prime):
    """Exhaustively choose primary a+b*rho of norm p with b<0."""
    bound = 2 * isqrt(prime) + 3
    trials = 0
    candidates = []
    for b in range(-bound, 0):
        for a in range(-bound, bound + 1):
            trials += 1
            if a % 3 == 1 and b % 3 == 0 and a * a - a * b + b * b == prime:
                candidates.append((a, b))
    assert candidates
    candidates.sort(key=lambda pair: (abs(pair[1]), abs(pair[0]), pair))
    return candidates[0], trials, candidates


def one_prime(prime):
    from sage.all import CyclotomicField, ComplexField, RealField, prod

    started = time.perf_counter()
    field = CyclotomicField(3 * prime)
    zeta = field.gen()
    rho = zeta**prime
    zeta_p = zeta**3
    (a, b), primary_trials, candidates = primary_coefficients(prime)
    pi = a + b * rho
    rho_bar = (-a * pow(b % prime, -1, prime)) % prime
    assert a % 3 == 1 and b % 3 == 0 and b < 0
    assert a * a - a * b + b * b == prime
    assert (a + b * rho_bar) % prime == 0
    assert rho_bar != 1 and pow(rho_bar, 3, prime) == 1
    exponent_lookup = {pow(rho_bar, e, prime): e for e in range(3)}
    exponents = {
        x: exponent_lookup[pow(x, (prime - 1) // 3, prime)]
        for x in range(1, prime)
    }
    # Character evaluation uses only modular powering and a three-entry
    # lookup, not a full multiplicative-group discrete logarithm oracle.
    chi = {x: rho ** exponents[x] for x in range(1, prime)}
    betas = [1] + [min(x for x in range(1, prime) if exponents[x] == e) for e in (1, 2)]
    sums = {
        beta: sum((chi[x] * zeta_p ** ((beta * x) % prime) for x in range(1, prime)), field(0))
        for beta in betas
    }
    tau = sums[1]
    exact_cube = -prime * pi
    assert tau**3 == exact_cube
    ratio_exponents = []
    for beta in betas:
        expected_ratio = rho ** ((-exponents[beta]) % 3)
        assert sums[beta] / tau == expected_ratio
        assert sums[beta] ** 3 == exact_cube
        ratio_exponents.append((-exponents[beta]) % 3)
    assert len(set(sums.values())) == 3

    # Explicit canonical complex embedding; the branch comparison alone
    # is numerical. The cubic and additive-twist identities above are exact.
    complex_field = ComplexField(160)
    # Approximate complex roots do not satisfy exact equality tests for
    # the defining polynomial; all algebraic assertions precede this map.
    embedding = field.hom([complex_field.zeta(3 * prime)], complex_field, check=False)
    complex_tau = embedding(tau)
    complex_cube = embedding(exact_cube)
    principal_root = (complex_cube.log() / 3).exp()
    complex_rho = embedding(rho)
    branch_errors = [abs(complex_tau - principal_root * complex_rho**k) for k in range(3)]
    branch = min(range(3), key=lambda k: branch_errors[k])
    assert branch_errors[branch] < RealField(160)(2) ** -100

    # An arbitrary 1/3-representative system, formed as minimum positive
    # integers in the rho_bar orbits. It is not Ito's geometric S_pi.
    visited = set()
    representatives = []
    for x in range(1, prime):
        if x in visited:
            continue
        orbit = {x * pow(rho_bar, e, prime) % prime for e in range(3)}
        assert len(orbit) == 3
        representatives.append(min(orbit))
        visited.update(orbit)
    representatives.sort()
    assert len(visited) == prime - 1 and len(representatives) == (prime - 1) // 3
    product_mod = int(prod(representatives) % prime)
    assert pow(product_mod, 3, prime) == prime - 1
    alpha_index = next(j for j in range(3) if (-pow(rho_bar, j, prime)) % prime == product_mod)
    alpha = -rho**alpha_index
    assert alpha**3 == -1
    changed = representatives.copy()
    changed[0] = changed[0] * rho_bar % prime
    changed_product_mod = int(prod(changed) % prime)
    changed_index = next(j for j in range(3) if (-pow(rho_bar, j, prime)) % prime == changed_product_mod)
    changed_alpha = -rho**changed_index
    assert changed_product_mod == product_mod * rho_bar % prime
    assert pow(changed_product_mod, 3, prime) == pow(product_mod, 3, prime)
    assert changed_alpha / alpha == rho and changed_alpha**3 == -1

    return {
        "prime": prime,
        "cyclotomic_conductor": 3 * prime,
        "cyclotomic_degree": int(field.degree()),
        "primary_pi_coefficients_a_b": [a, b],
        "primary_pi_description": f"({a}) + ({b})*rho",
        "all_primary_candidates_b_negative": [list(pair) for pair in candidates],
        "primary_search_integer_pairs_tested": primary_trials,
        "rho_bar_mod_p": rho_bar,
        "betas": betas,
        "chi_beta_rho_exponents": [exponents[beta] for beta in betas],
        "tau_beta_over_tau_1_rho_exponents": ratio_exponents,
        "exact_tau_1_cube_equals_minus_p_pi": True,
        "all_three_exact_cubes_equal": True,
        "three_exact_sums_distinct": True,
        "exact_sums_in_cyclotomic_generator": {str(beta): str(sums[beta]) for beta in betas},
        "complex_embedding": "zeta_(3p) maps to exp(2*pi*i/(3p))",
        "complex_precision_bits": 160,
        "tau_1_complex_real": str(complex_tau.real()),
        "tau_1_complex_imag": str(complex_tau.imag()),
        "principal_cube_root_real": str(principal_root.real()),
        "principal_cube_root_imag": str(principal_root.imag()),
        "branch_index_k_tau_equals_principal_root_times_rho_k": branch,
        "branch_comparison_absolute_error": str(branch_errors[branch]),
        "arbitrary_integer_orbit_representatives_S": representatives,
        "S_product_mod_p": product_mod,
        "alpha_lift_minus_rho_exponent": alpha_index,
        "alpha_lift_cube_equals_minus_one_exactly": True,
        "changed_representatives_one_rotation": changed,
        "changed_product_mod_p": changed_product_mod,
        "changed_alpha_lift_minus_rho_exponent": changed_index,
        "changed_product_ratio_mod_p": rho_bar,
        "changed_alpha_ratio_equals_rho_exactly": True,
        "product_cubes_unchanged_mod_p": True,
        "S_is_claimed_to_be_Ito_geometric_system": False,
        "classical_work": {
            "terms_per_direct_sum": prime - 1,
            "number_direct_sums": len(betas),
            "total_direct_sum_terms": len(betas) * (prime - 1),
            "character_values_enumerated": prime - 1,
            "orbit_partition_residues": prime - 1,
            "scope": "Direct exact cyclotomic sums enumerate p-1 terms each; no poly(log p) classical algorithm or asymptotic branch theorem is inferred.",
        },
        "seconds": time.perf_counter() - started,
    }


def run_control():
    started = time.perf_counter()
    results = [one_prime(prime) for prime in PRIMES]
    output = {
        "scope": "Four exact finite classical controls. No quantum execution, hardness result, asymptotic inference, or Ito geometric-product evaluation.",
        "source_scope": {
            "ito_cubic_gauss_product_2012": {
                "primary_generator_and_sum_lines": "35-44",
                "product_formula_lines": "45-53",
                "representative_system_alpha_definition_lines": "61-70",
                "geometric_system_construction_lines": "128-148",
            },
            "van_dam_seroussi_gauss_2002": {
                "section_6_1_lines": "535-553",
                "scope": "The stated DLP reduction uses a primitive full-order multiplicative character and arbitrary additive beta. This fixed order-three character control is not that full-order DLP reduction.",
            },
        },
        "results": results,
        "total_worker_seconds": time.perf_counter() - started,
    }
    artifact = Path(__file__).with_suffix(".json")
    artifact.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "artifact": str(artifact),
        "results": [{key: item[key] for key in (
            "prime", "primary_pi_coefficients_a_b", "rho_bar_mod_p", "betas",
            "exact_tau_1_cube_equals_minus_p_pi", "all_three_exact_cubes_equal",
            "three_exact_sums_distinct", "branch_index_k_tau_equals_principal_root_times_rho_k",
            "S_product_mod_p", "changed_product_mod_p", "seconds",
        )} for item in results],
        "total_worker_seconds": output["total_worker_seconds"],
    }))


if __name__ == "__main__":
    if sys.argv[1:] == ["--sage-worker"]:
        run_control()
    elif not sys.argv[1:]:
        subprocess.run([SAGE_PYTHON, str(Path(__file__).resolve()), "--sage-worker"], check=True)
    else:
        raise SystemExit("Usage: cubic_gauss_branch_control.py")
