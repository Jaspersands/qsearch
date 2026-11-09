#!/opt/anaconda3/bin/python
"""Eight exact half-factorial controls using certified classical PARI/Sage.

This is a finite arithmetic check, not a compact quantum unit/class-group
implementation or a claim about the asymptotic cost of these computations.
The standard-library driver starts one bounded Sage worker.
"""

import json
from math import factorial
from pathlib import Path
import subprocess
import sys
import time

SAGE_PYTHON = "/opt/anaconda3/envs/qsearch-cas/bin/python"
PRIMES = (3, 5, 7, 13, 17, 23, 41, 229)


def parity_sign(class_number):
    assert class_number % 2 == 1
    return -1 if ((class_number + 1) // 2) % 2 else 1


def one_prime(prime):
    from sage.all import AA, GF, QuadraticField

    started = time.perf_counter()
    radicand = prime if prime % 4 == 1 else -prime
    field = QuadraticField(radicand, "a")
    maximal_order = field.maximal_order()
    bnf = field.pari_bnf(proof=True)
    assert int(bnf.bnfcertify()) == 1
    class_group = field.class_group(proof=True)
    class_number = int(class_group.order())
    direct = factorial((prime - 1) // 2) % prime
    square_target = (-1 if ((prime + 1) // 2) % 2 else 1) % prime
    assert pow(direct, 2, prime) == square_target
    result = {
        "prime": prime,
        "radicand": radicand,
        "field_discriminant": int(field.discriminant()),
        "maximal_order_basis": [str(x) for x in maximal_order.basis()],
        "ordinary_class_group_invariants": [int(x) for x in class_group.invariants()],
        "ordinary_class_number": class_number,
        "class_number_mod_four": class_number % 4,
        "pari_bnf_certified": True,
        "direct_half_factorial_mod_p": direct,
        "wilson_square_target_mod_p": square_target,
    }
    if prime == 3:
        predicted = 1
        wrong_unexceptional = parity_sign(class_number) % prime
        assert wrong_unexceptional != direct
        result.update({
            "formula_case": "p=3 direct exception",
            "unexceptional_imaginary_formula_mod_p": wrong_unexceptional,
            "unexceptional_formula_rejected": True,
        })
    elif prime % 4 == 3:
        predicted = parity_sign(class_number) % prime
        result["formula_case"] = "(-1)^((h(-p)+1)/2), p>3"
    else:
        units = field.units(proof=True)
        assert len(units) == 1
        raw_unit = units[0]
        embedding = next(e for e in field.embeddings(AA) if e(field.gen()) > 0)
        unit = raw_unit
        if embedding(unit) < 0:
            unit = -unit
        if embedding(unit) < 1:
            unit = unit**-1
        assert embedding(unit) > 1
        assert maximal_order(unit) == unit
        assert unit.norm() == -1
        coefficient = unit.polynomial()[0]
        coefficient_mod_p = int(GF(prime)(coefficient))
        sign = parity_sign(class_number)
        predicted = sign * coefficient_mod_p % prime
        result.update({
            "formula_case": "(-1)^((h(p)+1)/2) times constant coefficient of positive fundamental unit",
            "real_embedding": "a maps to the positive square root of p",
            "raw_pari_sage_fundamental_unit": str(raw_unit),
            "positive_fundamental_unit": str(unit),
            "positive_fundamental_unit_coefficients": [str(unit.polynomial()[i]) for i in range(2)],
            "positive_fundamental_unit_norm": int(unit.norm()),
            "positive_fundamental_unit_in_maximal_order": True,
            "constant_coefficient_mod_p": coefficient_mod_p,
            "class_number_sign": sign,
            "integer_generator_order_discriminant": int(field.defining_polynomial().discriminant()),
        })
        if prime == 5:
            wrong = []
            for name, candidate in (
                ("inverse", unit**-1),
                ("negative", -unit),
                ("squared", unit**2),
            ):
                value = sign * int(GF(prime)(candidate.polynomial()[0])) % prime
                assert value != direct
                wrong.append({
                    "variant": name,
                    "unit": str(candidate),
                    "norm": int(candidate.norm()),
                    "embedding_positive_and_greater_than_one": bool(embedding(candidate) > 1),
                    "predicted_factorial_mod_p": value,
                    "equals_direct_factorial": False,
                    "passes_wilson_square_check": pow(value, 2, prime) == square_target,
                })
            assert wrong[0]["passes_wilson_square_check"]
            assert wrong[1]["passes_wilson_square_check"]
            assert not wrong[2]["passes_wilson_square_check"]
            result["wrong_unit_normalization_controls"] = wrong
    assert predicted == direct
    result.update({
        "predicted_half_factorial_mod_p": predicted,
        "prediction_equals_direct_factorial": True,
        "seconds": time.perf_counter() - started,
    })
    return result


def run_control():
    started = time.perf_counter()
    results = [one_prime(prime) for prime in PRIMES]
    assert len(results) == 8
    assert {row["class_number_mod_four"] for row in results} == {1, 3}
    output = {
        "scope": "Eight fixed finite classical arithmetic controls; no sweep, asymptotic inference, or quantum execution.",
        "primes": list(PRIMES),
        "arithmetic_backend": "Sage quadratic fields and PARI BNF with bnfcertify=1",
        "class_number_convention": "Ordinary ideal class group of the maximal order, not the narrow class group or the order Z[sqrt(p)].",
        "unit_convention": "Generator of the full maximal-order unit group modulo torsion, normalized to epsilon>1 in the positive-sqrt(p) embedding.",
        "compact_quantum_primitive_executed": False,
        "quantum_class_group_or_unit_algorithm_executed": False,
        "results": results,
        "total_worker_seconds": time.perf_counter() - started,
    }
    artifact = Path(__file__).with_suffix(".json")
    artifact.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "artifact": str(artifact),
        "results": [{key: row[key] for key in (
            "prime", "ordinary_class_number", "predicted_half_factorial_mod_p",
            "direct_half_factorial_mod_p", "prediction_equals_direct_factorial",
        )} for row in results],
        "wrong_normalizations_p5": results[1]["wrong_unit_normalization_controls"],
        "total_worker_seconds": output["total_worker_seconds"],
    }))


if __name__ == "__main__":
    if sys.argv[1:] == ["--sage-worker"]:
        run_control()
    elif not sys.argv[1:]:
        subprocess.run(
            [SAGE_PYTHON, str(Path(__file__).resolve()), "--sage-worker"],
            check=True, timeout=60,
        )
    else:
        raise SystemExit("Usage: half_factorial_arithmetic_control.py")
