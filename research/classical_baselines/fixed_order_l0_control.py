#!/opt/anaconda3/bin/python
"""One certified classical q=8, p=41 diagnostic for fixed-order L0 recovery.

Direct period counts, Bernoulli sums, target embedding logs and numerical
Gauss/L1 sums are diagnostic inputs. PARI principal-ideal recovery substitutes
for the theorem's fixed-field finite table. No Tal, quantum, GRH-truncation,
general class-action or asymptotic algorithm is implemented here.
"""

import json
from pathlib import Path
import subprocess
import sys
import time

SAGE_PYTHON = "/opt/anaconda3/envs/qsearch-cas/bin/python"


def run_control():
    from sage.all import (ComplexField, CyclotomicField, NumberField, QQ, ZZ,
                          identity_matrix, matrix, vector)
    import mpmath as mp

    started = time.perf_counter()
    q, p, eta, k = 8, 41, 27, 5
    r = q // 2
    assert p == 1 + q * k and k > 1 and k % 2 == 1
    assert pow(eta, q, p) == 1 and pow(eta, q // 2, p) != 1
    lookup = {pow(eta, j, p): j for j in range(q)}
    exponent = {a: lookup[pow(a, k, p)] for a in range(1, p)}
    cosets = [[a for a in range(1, p) if exponent[a] == j] for j in range(q)]
    assert all(len(coset) == k and sum(coset) % p == 0 for coset in cosets)
    M = [sum(coset) // p for coset in cosets]
    assert M == [2, 2, 3, 3, 3, 3, 2, 2]

    # Diagnostic O(p) enumeration, not the proposed exact-Jacobi preprocessing.
    counts = matrix(ZZ, q, q)
    for t in range(2, p):
        counts[exponent[t], exponent[(1 - t) % p]] += 1
    multiplication = [matrix(ZZ, q, q, lambda ell, j:
        counts[(i - ell) % q, (j - ell) % q] - k * int(j == (i + r) % q))
        for i in range(q)]
    one = vector(QQ, [-1] * q)
    powers = [one]
    for _ in range(1, q):
        powers.append(multiplication[0] * powers[-1])
    krylov = matrix(QQ, powers).transpose()
    assert krylov.rank() == q
    polynomial = multiplication[0].charpoly("x")
    assert polynomial.is_irreducible()
    field = NumberField(polynomial, "theta")
    theta = field.gen()
    inverse = krylov.inverse()
    periods = [sum((inverse[j, i] * theta**j for j in range(q)), field(0))
               for i in range(q)]
    assert periods[0] == theta and sum(periods) == -1
    assert all(value.is_integral() for value in periods)
    for i in range(q):
        for j in range(q):
            assert periods[i] * periods[j] == sum(
                (multiplication[i][ell, j] * periods[ell] for ell in range(q)), field(0))
    sigma = field.hom([periods[1]], field)
    assert all(sigma(periods[i]) == periods[(i + 1) % q] for i in range(q))
    trace_gram = matrix(QQ, q, q, lambda i, j: (periods[i] * periods[j]).trace())
    assert trace_gram.det() == p**(q - 1)
    bnf = field.pari_bnf(proof=True)
    assert int(bnf.bnfcertify()) == 1
    assert field.discriminant() == trace_gram.det()
    classes = field.class_group(proof=True)
    if classes.order() != 1:
        raise RuntimeError("The single selected class group is nontrivial; no general action framework is authorized")

    coefficient_field = CyclotomicField(q, "zeta")
    zeta = coefficient_field.gen()
    coefficient_bnf = coefficient_field.pari_bnf(proof=True)
    assert int(coefficient_bnf.bnfcertify()) == 1
    units = coefficient_field.units(proof=True)
    assert len(units) == 1
    unit_group = coefficient_field.unit_group(proof=True)
    assert unit_group.zeta_order() == q
    cc = ComplexField(192)
    embeddings = [coefficient_field.hom([cc.zeta(q)**a], cc) for a in (1, 3)]
    epsilon = units[0]
    if abs(embeddings[0](epsilon)) < 1:
        epsilon = epsilon**-1
    assert abs(embeddings[0](epsilon)) > 1

    # Diagnostic truth; this p-term sum is not part of the proposed algorithm.
    z = -sum((a * zeta**exponent[a] for a in range(1, p)), coefficient_field(0)) / p
    assert z == 1 + zeta - zeta**2 - zeta**3
    assert z == sum(((k - 2 * M[j]) * zeta**j for j in range(r)), coefficient_field(0))
    prime_two = coefficient_field.ideal(1 - zeta)
    exact_ideal = coefficient_field.ideal(z)
    assert z.norm() == 8 and prime_two.norm() == 2
    assert exact_ideal.valuation(prime_two) == r - 1
    # Cl(K)=1 makes the odd Fitting ideal trivial. No class-action code is needed.
    recovered_ideal = prime_two**(r - 1)
    assert recovered_ideal == exact_ideal
    assert prime_two**(r - 2) != exact_ideal

    def coefficients(value):
        return [int(value.polynomial()[j]) for j in range(r)]

    coefficient_lattice = matrix(ZZ, [coefficients(value) for value in recovered_ideal.integral_basis()])
    assert abs(coefficient_lattice.det()) == recovered_ideal.norm()
    reduced = coefficient_lattice.LLL(delta=QQ(3) / 4)
    alpha = sum((reduced[0, j] * zeta**j for j in range(r)), coefficient_field(0))
    assert alpha != 0 and alpha in recovered_ideal
    # Power the stated Euclidean bound to avoid floating-point verification.
    assert sum(v * v for v in reduced.row(0))**r <= 2**(r * (r - 1) // 2) * recovered_ideal.norm()**2
    quotient_ideal = coefficient_field.ideal(alpha) / recovered_ideal
    assert quotient_ideal.is_integral()
    constant_bound = (r * 2**r)**r
    assert quotient_ideal.norm() <= constant_bound
    gamma_values = quotient_ideal.gens_reduced()
    assert len(gamma_values) == 1
    gamma = gamma_values[0]
    assert coefficient_field.ideal(gamma) == quotient_ideal
    beta = alpha / gamma
    assert coefficient_field.ideal(beta) == exact_ideal

    def torsion_matches(value):
        return [j for j in range(q) if zeta**j * value == z]

    def normalize(value):
        # Deliberately uses diagnostic exact-z embedding logs, not GRH Euler data.
        B = abs(embeddings[0](epsilon)).log()
        t = abs(embeddings[0](z)).log() - abs(embeddings[0](value)).log()
        coordinate = t / B
        n = ZZ(coordinate.round())
        result = value * epsilon**n
        assert abs(coordinate - n) < QQ(1) / 2**140
        matches = torsion_matches(result)
        assert len(matches) == 1
        assert result == zeta**(-matches[0]) * z
        return result, {
            "rounded_exponent": int(n), "unrounded_coordinate": str(coordinate),
            "rounding_residual": str(abs(coordinate - n)),
            "normalized_generator": str(result), "matching_torsion_exponent": matches[0],
            "both_embedding_log_errors": [str(abs(abs(embedding(result)).log() - abs(embedding(z)).log()))
                                          for embedding in embeddings],
        }

    normalized, normalization = normalize(beta)
    twisted = beta * epsilon**7
    assert coefficient_field.ideal(twisted) == exact_ideal
    skipped_matches = torsion_matches(twisted)
    assert skipped_matches == []
    normalized_twist, twist_normalization = normalize(twisted)
    assert normalized_twist == normalized
    assert twist_normalization["rounded_exponent"] == normalization["rounded_exponent"] - 7

    # Direct Gauss sum and finite digamma formula for L1 are numerical controls.
    # They do not execute a quantum phase estimator or a GRH Euler truncation.
    mp.mp.dps = 65
    root = mp.exp(2j * mp.pi / q)
    tau = sum(root**exponent[a] * mp.exp(2j * mp.pi * a / p) for a in range(1, p))
    L1_bar = -sum(root**(-exponent[a]) * mp.digamma(mp.mpf(a) / p)
                  for a in range(1, p)) / p
    phase_target = tau * L1_bar / (1j * mp.pi)

    def numeric(value):
        return sum(mp.mpf(str(value.polynomial()[j])) * root**j for j in range(r))

    functional_residual = abs(phase_target - numeric(z))
    assert functional_residual < mp.mpf("1e-55")
    phase_distances = [abs(mp.arg(root**j * numeric(normalized) / phase_target)) for j in range(q)]
    chosen = min(range(q), key=phase_distances.__getitem__)
    assert chosen == normalization["matching_torsion_exponent"]
    recovered = zeta**chosen * normalized
    assert recovered == z
    assert sorted(phase_distances)[1] > mp.pi / q

    def ideal_record(ideal):
        return {"norm": str(ideal.norm()), "PARI_HNF": str(ideal.pari_hnf())}

    result = {
        "scope": "One bounded certified classical diagnostic, not theorem evidence or quantum execution. No Tal reconstruction, GRH Euler truncation, generic class action, constant-table construction, compact CRT implementation, or growing-q claim.",
        "parameters": {"q": q, "p": p, "eta": eta, "k": k},
        "diagnostic_costs": {
            "period_multiplication": "Direct O(p) character enumeration; substitutes for paid exact Jacobi reconstruction.",
            "truth_and_logs": "Direct O(p) Bernoulli sum, then numerical embeddings of exact z; substitutes for GRH logarithm approximation.",
            "small_ideal_generator": "Sage/PARI principal generator from a certified coefficient-field BNF; substitutes for the computable fixed-field table.",
            "phase": "Direct p-term numerical Gauss sum and p-term digamma L1 formula; substitutes for quantum Gauss phase and short Euler product.",
        },
        "period_field": {
            "coset_sums_divided_by_p": M, "cyclotomic_number_counts": [list(map(int, row)) for row in counts.rows()],
            "primitive_polynomial": str(polynomial), "period_power_basis": [str(value) for value in periods],
            "all_multiplication_products_checked": q * q, "sigma_cycles_period_basis": True,
            "trace_basis_discriminant": int(trace_gram.det()), "field_discriminant": int(field.discriminant()),
            "periods_form_maximal_integral_basis": True, "bnf_certified": True,
            "class_number": int(classes.order()), "class_invariants": list(map(int, classes.invariants())),
            "odd_Fitting_ideal": "Unit ideal because the complete certified class group is trivial",
        },
        "coefficient_field": {
            "polynomial": str(coefficient_field.defining_polynomial()), "bnf_certified": True,
            "complete_free_unit_rank": len(units), "torsion_order": int(unit_group.zeta_order()),
            "fundamental_unit": str(epsilon), "target_z": str(z), "target_coefficients": coefficients(z),
            "target_norm": int(z.norm()), "lambda_valuation": int(exact_ideal.valuation(prime_two)),
            "reconstructed_ideal": ideal_record(recovered_ideal), "exact_target_ideal": ideal_record(exact_ideal),
            "wrong_lambda_squared_matches": prime_two**2 == exact_ideal,
        },
        "generator_reduction": {
            "coefficient_ideal_basis": [list(map(int, row)) for row in coefficient_lattice.rows()],
            "LLL_first_vector": list(map(int, reduced.row(0))), "alpha": str(alpha),
            "small_quotient_ideal": ideal_record(quotient_ideal), "explicit_constant_bound": constant_bound,
            "gamma_PARI_substitute": str(gamma), "beta": str(beta), "same_ideal_verified": True,
            "unit_normalization": normalization,
        },
        "negative_unit_control": {
            "twist_exponent": 7, "twisted_beta": str(twisted), "same_ideal_verified": True,
            "skip_normalization_torsion_matches": skipped_matches,
            "after_normalization": twist_normalization, "normalization_recovers_same_generator": True,
        },
        "phase_control": {
            "formula": "L(0,chi) = tau(chi) L(1,bar chi)/(i*pi)",
            "decimal_precision": mp.mp.dps, "functional_equation_absolute_residual": mp.nstr(functional_residual, 12),
            "tau": mp.nstr(tau, 30), "L1_bar_chi": mp.nstr(L1_bar, 30),
            "torsion_phase_distances_radians": [mp.nstr(value, 16) for value in phase_distances],
            "selected_torsion_exponent": chosen, "exact_recovered_coefficients": coefficients(recovered),
            "exact_output_matches_direct_truth": True,
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    artifact = Path(__file__).with_suffix(".json")
    artifact.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"artifact": str(artifact), "field_polynomial": str(polynomial),
                      "class_number": int(classes.order()), "unit": str(epsilon),
                      "beta": str(beta), "unit_exponents": [normalization["rounded_exponent"], twist_normalization["rounded_exponent"]],
                      "skip_unit_control_matches": skipped_matches, "recovered": coefficients(recovered),
                      "seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--sage-worker"]:
        run_control()
    elif not sys.argv[1:]:
        subprocess.run([SAGE_PYTHON, str(Path(__file__).resolve()), "--sage-worker"], check=True, timeout=120)
    else:
        raise SystemExit("Usage: fixed_order_l0_control.py")
