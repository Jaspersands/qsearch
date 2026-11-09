"""Sage control for the native quadratic Legendre character-only contract.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python.  The attack receives
only p and the p character values in public order x=0,...,p-1.  The harness
alone knows the polynomial.  Finite controls check the stated identities;
they provide no classical hardness or quantum speedup evidence.
"""

import json
from pathlib import Path
from random import Random

from sage.all import GF, PolynomialRing


PRIMES = (5, 7, 11, 13)
EXCEPTION_PRIME = 3
VERIFICATION_QUERIES = 16
VERIFICATION_SEED = 20261105


def recover_from_character_values(p, character_values):
    """Consume p signs, without coefficients, field values, or extension access.

    This formula is promised only for odd primes p>=5.  Deliberately do not
    special-case p=3: the control must retain that boundary counterexample.
    """
    field = GF(p)
    values = iter(character_values)
    s1 = field(0)
    s2 = field(0)
    query_count = 0
    for x in range(p):
        sign = int(next(values))
        if sign not in (-1, 1):
            raise ValueError("Irreducible quadratic source must return a sign")
        query_count += 1
        fx = field(x)
        weighted = fx * field(sign)
        s1 += weighted
        s2 += fx * weighted
    b = field(2) * s1
    coefficient = field(3) / field(4)
    c = field(2) * s2 + coefficient * (b * b)
    return {"b": int(b), "c": int(c), "queries": query_count,
            "s1": int(s1), "s2": int(s2)}


def _character(value):
    if value == 0:
        return 0
    return 1 if value.is_square() else -1


def _check_prime(p):
    """Source and truth checks stay outside recover_from_character_values."""
    field = GF(p)
    ring = PolynomialRing(field, "x")
    x = ring.gen()
    rng = Random(VERIFICATION_SEED + p)
    rows = []
    for b in range(p):
        for c in range(p):
            source = x * x + field(b) * x + field(c)
            if not source.is_irreducible():
                continue
            private_table = tuple(_character(source(field(a))) for a in range(p))
            assert all(sign in (-1, 1) for sign in private_table)
            recovered = recover_from_character_values(p, iter(private_table))
            candidate = x * x + field(recovered["b"]) * x + field(recovered["c"])
            native_agreements = sum(
                _character(candidate(field(a))) == private_table[a]
                for a in range(p)
            )
            verification_inputs = [rng.randrange(p) for _ in range(VERIFICATION_QUERIES)]
            verification_agreements = sum(
                _character(candidate(field(a))) == private_table[a]
                for a in verification_inputs
            )
            # These random queries are independent of candidate construction.
            # They are charged separately, even though the table is already read.
            rows.append({
                "source_b": b, "source_c": c, "recovered": recovered,
                "coefficient_match": recovered["b"] == b and recovered["c"] == c,
                "native_agreements": int(native_agreements),
                "native_comparisons": p,
                "candidate_irreducible": bool(candidate.is_irreducible()),
                "verification_inputs": verification_inputs,
                "verification_agreements": int(verification_agreements),
                "verification_queries": VERIFICATION_QUERIES,
                "total_charged_queries": p + VERIFICATION_QUERIES,
            })
    expected = p * (p - 1) // 2
    assert len(rows) == expected
    successes = sum(row["coefficient_match"] for row in rows)
    full_matches = sum(row["native_agreements"] == p for row in rows)
    if p >= 5:
        assert successes == full_matches == expected
        assert all(row["verification_agreements"] == VERIFICATION_QUERIES for row in rows)
    else:
        assert successes == full_matches == 0
        assert all(row["recovered"]["b"] == row["source_b"] for row in rows)
        assert all(row["recovered"]["c"] == (row["source_c"] + 1) % p for row in rows)
    assert all(row["recovered"]["queries"] == p for row in rows)
    return {"prime": p, "irreducible_instances": expected,
            "coefficient_matches": successes, "full_native_matches": full_matches,
            "attack_queries_per_instance": p,
            "analytic_field_operations_per_attack": {
                "multiplications": 2 * p + 5,
                "additions": 2 * p + 1,
                "inversions": 1,
                "scope": "Logical field operations of written attack; conversions, field setup, iteration, and source/verification excluded. Division counts as one inversion and one multiplication.",
            },
            "rows": rows}


def main():
    controls = [_check_prime(p) for p in PRIMES]
    exception = _check_prime(EXCEPTION_PRIME)
    output = {
        "id": "QUADRATIC-LEGENDRE-CHARACTER-ONLY-CONTRACT-2026-11-05",
        "source_model": {
            "input": "Public growing odd prime p; hidden monic irreducible f=x^2+b*x+c over F_p.",
            "attack_access": "Only p and an iterator of chi(f(x)) at public x=0,...,p-1; no b,c, full field values, or extension-field queries.",
            "oracle_source": "Sage constructs private source polynomial and table outside attack; truth used only by harness.",
            "output": "Recovered coefficients b,c, followed by independent random-query verification.",
        },
        "predeclared_primes": list(PRIMES),
        "verification_seed": VERIFICATION_SEED,
        "verification_queries_per_instance": VERIFICATION_QUERIES,
        "verified_irreducible_instances": sum(item["irreducible_instances"] for item in controls),
        "analytic_scope": {
            "validity": "Every monic quadratic over F_p for p>=5; irreducibility fixes the native sign-only promise.",
            "attack_queries": "Exactly p ordinary classical queries.",
            "time": "O(p) field operations plus polynomial(log p) setup; exponential in bit input length log p.",
            "working_space": "O(log p) bits for a constant number of field registers and loop counters, with streaming input; implementation/runtime overhead not measured. Source-table storage is harness-only.",
            "gate": "No efficient quantum decoder, speedup, novelty, or classical hardness claim.",
        },
        "controls": controls,
        "excluded_p3_boundary": exception,
        "p3_expected_failure": "For each irreducible quadratic, same formula returns b and c+1 modulo 3; retained, not repaired.",
    }
    destination = Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"artifact": str(destination), "verified_instances": output["verified_irreducible_instances"],
                      "p3_expected_failures": exception["irreducible_instances"] - exception["coefficient_matches"]}, sort_keys=True))


if __name__ == "__main__":
    main()
