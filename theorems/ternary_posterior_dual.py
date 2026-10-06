"""Exact costed least-trit posterior in the paired covariant record model.

LOCAL DERIVATIONS / REVIEW PENDING. The generic baseline is exponential.
Sparse phase cancellations are exact; posterior decisions use Arb enclosures.
No original quantum states, chosen queries or efficient weak learner supplied.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import json
import math
from pathlib import Path
import random

from flint import acb, arb, ctx

from ternary_covariant_noise import CovariantRecord, ROOT_DIRECTIONS, root_digits, simulated_record
from ternary_incidence_decoder import IncidenceDecoder, IncidenceSample

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_posterior_dual.json"


def _integer(x, name, minimum=0):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return x


def _add_phase(poly, exponent, coefficient, q):
    """Reduce exactly by Phi_(3^r)=X^(2q/3)+X^(q/3)+1."""
    exponent %= q
    terms = ((exponent, coefficient),) if exponent < 2*q//3 else (
        (exponent-2*q//3, -coefficient), (exponent-q//3, -coefficient))
    for e, c in terms:
        value = poly.get(e, 0)+c
        if value:
            poly[e] = value
        else:
            poly.pop(e, None)


def canonical_phase(polynomial, q):
    root_digits(q)
    out = {}
    for exponent, coefficient in polynomial.items():
        _integer(exponent, "phase exponent")
        if type(coefficient) is not int:
            raise ValueError("exact integer phase coefficients required")
        _add_phase(out, exponent, coefficient, q)
    return out


def _shift(poly, exponent, q):
    out = {}
    for e, c in poly.items():
        _add_phase(out, e+exponent, c, q)
    return out


def _conjugate(poly, q):
    out = {}
    for e, c in poly.items():
        _add_phase(out, -e, c, q)
    return out


def _sum(polys, q):
    out = {}
    for p in polys:
        for e, c in p.items():
            _add_phase(out, e, c, q)
    return out


def likelihood_terms(record):
    if not isinstance(record, CovariantRecord):
        raise ValueError("validated paired covariant record required")
    q, n = record.modulus, len(record.first)
    # All factors use common denominator3: the identity has integer weight3.
    terms = [((0,)*n, 0, 3)]
    for u, v in ROOT_DIRECTIONS:
        f = tuple(-(u*a+v*c) % q for a, c in zip(record.first, record.second))
        terms.append((f, (u*record.outcome[0]+v*record.outcome[1]) % q, 1))
    return tuple(terms)


def _records(records, ids):
    records, ids = tuple(records), tuple(ids)
    if not records or any(not isinstance(x, CovariantRecord) for x in records):
        raise ValueError("nonempty validated paired-record batch required")
    q, n = records[0].modulus, len(records[0].first)
    if any(x.modulus != q or len(x.first) != n for x in records):
        raise ValueError("one modulus and dimension per independent batch required")
    if len(ids) != len(records) or any(type(x) is not int or x < 0 for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("one distinct original qutrit ID per record; reused ancestors are not IID")
    return records, ids, q, n


class _BudgetExceeded(Exception):
    pass


def _expand(records, q, n, max_states, ledger):
    table = {(0,)*n: {0: 1}}
    for record in records:
        next_table = {}
        for frequency, poly in table.items():
            for delta, phase, weight in likelihood_terms(record):
                out_frequency = tuple((a+b) % q for a, b in zip(frequency, delta))
                out = next_table.setdefault(out_frequency, {})
                for e, c in poly.items():
                    _add_phase(out, e+phase, weight*c, q)
                    ledger["half_phase_updates"] += 1
        table = {f: p for f, p in next_table.items() if p}
        states = sum(len(p) for p in table.values())
        ledger["maximum_stored_half_monomials"] = max(ledger["maximum_stored_half_monomials"], states)
        if states > max_states:
            raise _BudgetExceeded("half expansion exceeded its declared exact-state budget")
    return table


def _encode(poly):
    return [[str(e), str(c)] for e, c in sorted(poly.items())]


def _evaluate(poly, q):
    # Exact rational angles are enclosed before transcendental evaluation.
    value = acb(0)
    for e, c in poly.items():
        value += c*acb(0, 2*arb.pi()*arb(e)/q).exp()
    return value


def _posterior(coefficients, q, initial_precision, maximum_precision):
    C0, C1, C2 = coefficients
    if _conjugate(C0, q) != C0 or _conjugate(C1, q) != C2:
        raise ArithmeticError("posterior coefficients violate exact reality/conjugacy")
    Z = [_sum((C0, _shift(C1, q//3*t, q), _shift(C2, 2*q//3*t, q)), q) for t in range(3)]
    exact = {"class_likelihood_numerators": [_encode(z) for z in Z],
             "normalizer_numerator": _encode(C0), "root_modulus": str(q),
             "posterior_formula": "Z_t/(3*C_0); common3^M likelihood denominator cancels"}
    if not C0:
        if any(Z):
            raise ArithmeticError("zero positive normalizer with nonzero class masses")
        return {**exact, "status": "ZERO_LIKELIHOOD_DATA_NO_POSTERIOR", "posterior_probabilities": None,
                "maximum_a_posteriori_trit": None}
    precision = initial_precision
    while precision <= maximum_precision:
        with ctx.workprec(precision):
            normalizer = _evaluate(C0, q)
            values = [_evaluate(z, q) if z else acb(0) for z in Z]
            if not normalizer.imag.contains(0) or any(not z.imag.contains(0) for z in values):
                raise ArithmeticError("ball replay disagrees with exact real phase algebra")
            if normalizer.real > 0 and all(not poly or z.real > 0 for poly, z in zip(Z, values)):
                probabilities = [z.real/(3*normalizer.real) for z in values]
                if not sum(probabilities, arb(0)).contains(1):
                    raise ArithmeticError("enclosed posterior does not normalize")
                maxima = [i for i in range(3) if all(Z[i] == Z[j] or probabilities[i] > probabilities[j]
                                                   for j in range(3))]
                if maxima:
                    return {**exact, "status": "EXACT_POSTERIOR_WITH_CERTIFIED_BALL_ORDERING",
                            "posterior_probabilities": [float(p) for p in probabilities],
                            "posterior_probability_enclosures": [p.str(45) for p in probabilities],
                            "precision_bits": precision, "MAP_tied_classes": maxima,
                            "maximum_a_posteriori_trit": maxima[0] if len(maxima) == 1 else None,
                            "exactly_uniform_least_trit": not C1 and not C2,
                            "uniform_secret_weak_success_guarantee_proved": False}
        precision *= 2
    return {**exact, "status": "PRECISION_UNRESOLVED_NO_TRIT_CERTIFICATE",
            "posterior_probabilities": None, "maximum_a_posteriori_trit": None,
            "precision_budget_bits": maximum_precision}


def solve_least_trit(records, original_ids, target_coordinate=0, max_half_states=100000,
                     max_join_products=10000000, initial_precision=128, maximum_precision=1024):
    records, ids, q, n = _records(records, original_ids)
    _integer(target_coordinate, "target coordinate")
    if target_coordinate >= n:
        raise ValueError("target coordinate out of range")
    for value, name in ((max_half_states, "half-state budget"), (max_join_products, "join budget")):
        _integer(value, name, 1)
    for value, name in ((initial_precision, "initial precision"), (maximum_precision, "maximum precision")):
        _integer(value, name, 2)
    if initial_precision > maximum_precision:
        raise ValueError("initial precision exceeds maximum precision")
    split, M = len(records)//2, len(records)
    ledger = {"half_phase_updates": 0, "maximum_stored_half_monomials": 0,
              "matched_phase_products": 0, "frequency_bucket_joins": 0,
              "raw_assignments_per_half": [str(7**split), str(7**(M-split))],
              "generic_time_not_polynomial": True, "secret_assignments_enumerated": False,
              "original_native_qutrits_consumed": M, "original_record_ids": ids,
              "independence_not_proved_by_ID_uniqueness_alone": True,
              "max_half_states": max_half_states, "max_join_products": max_join_products}
    targets = [tuple(q//3*k if j == target_coordinate else 0 for j in range(n)) for k in range(3)]
    coefficients = [{}, {}, {}]
    try:
        left = _expand(records[:split], q, n, max_half_states, ledger)
        right = _expand(records[split:], q, n, max_half_states, ledger)
        for k, target in enumerate(targets):
            for f, A in left.items():
                g = tuple((t-a) % q for t, a in zip(target, f))
                if g not in right:
                    continue
                B = right[g]
                ledger["frequency_bucket_joins"] += 1
                products = len(A)*len(B)
                if ledger["matched_phase_products"]+products > max_join_products:
                    raise _BudgetExceeded("target join exceeded its declared exact-product budget")
                for e, a in A.items():
                    for h, b in B.items():
                        _add_phase(coefficients[k], e+h, a*b, q)
                ledger["matched_phase_products"] += products
    except _BudgetExceeded as error:
        return {"status": "EXACT_REFERENCE_BUDGET_EXHAUSTED_NO_POSTERIOR", "reason": str(error),
                "cost_ledger": ledger, "posterior": None, "polynomial_native_weak_learner_implemented": False}
    posterior = _posterior(coefficients, q, initial_precision, maximum_precision)
    return {"status": "COSTED_EXPONENTIAL_JOINT_CLASSICAL_BASELINE", "dimension": n, "modulus": str(q),
            "records": [r.public() for r in records], "target_coordinate": target_coordinate,
            "target_frequencies": targets, "coefficient_numerators": [_encode(c) for c in coefficients],
            "likelihood_common_denominator": str(3**M), "cost_ledger": ledger, "posterior": posterior,
            "original_unknown_phase_states_classically_simulated": False,
            "polynomial_native_weak_learner_implemented": False, "speedup_or_general_hardness_claim": False}


def classical_least_trit_gate(n, digits, samples, desired_advantage=Fraction(1, 10)):
    _integer(n, "dimension", 1); _integer(digits, "digits", 1); _integer(samples, "samples")
    eps = Fraction(desired_advantage)
    if not 0 < eps <= Fraction(2, 3):
        raise ValueError("advantage in (0,2/3] required")
    G, norm = 3**(n*digits), Fraction(5, 3)**samples-1
    return {"dimension": n, "digits": digits, "classical_records": samples,
            "mean_least_trit_advantage_squared_upper": str(norm/(2*G)),
            "necessary_copy_gate_passed": norm >= 2*G*eps**2,
            "requested_advantage": str(eps),
            "scope": "ANY processing of M raw paired covariant records, uniform ALL secrets and IID full labels",
            "unmeasured_native_states_or_other_receivers_covered": False,
            "arbitrary_polynomial_surplus_samples_excluded": False,
            "status": "LOCAL_DERIVATION_REVIEW_PENDING"}


def low_degree_gate(n, digits, samples, degree):
    _integer(n, "dimension", 1); _integer(digits, "digits", 1)
    _integer(samples, "samples"); _integer(degree, "record degree")
    if degree > samples:
        raise ValueError("degree exceeds record count")
    norm = sum((Fraction(math.comb(samples, j))*Fraction(2, 3)**j for j in range(1, degree+1)), Fraction(0))
    return {"dimension": n, "digits": digits, "samples": samples, "record_degree": degree,
            "truncated_centered_likelihood_norm_squared": str(norm),
            "class_minus_unconditional_mixture_norm_squared": str(2*norm/3**(n*digits)),
            "bounded_low_record_degree_classifier_mean_advantage_squared_upper": str(norm/(2*3**(n*digits))),
            "degree_definition": "Efron-Stein/ANOVA degree in COMPLETE independent records, including labels",
            "generic_adaptive_raw_sample_or_all_label_coefficients_covered": False,
            "status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_GENERAL_CLASSICAL_HARDNESS"}


def sparse_coherence_gate(n, digits, copies, radius, desired_advantage=Fraction(1, 10)):
    _integer(n, "dimension", 1); _integer(digits, "digits", 1)
    _integer(copies, "copies"); _integer(radius, "coherence radius")
    if radius > copies:
        raise ValueError("coherence radius exceeds native register count")
    eps = Fraction(desired_advantage)
    if not 0 < eps <= Fraction(2, 3):
        raise ValueError("advantage in (0,2/3] required")
    count = sum(math.comb(copies, j)*6**j for j in range(1, radius+1))
    probability = min(Fraction(1), Fraction(count, 3**(n*digits)))
    return {"dimension": n, "digits": digits, "native_copies": copies, "coherence_radius": radius,
            "oriented_root_difference_words": str(count),
            "probability_of_any_relevant_sparse_relation_upper": str(probability),
            "mean_least_trit_advantage_upper": str(Fraction(2, 3)*probability),
            "necessary_sparse_coherence_gate_passed": Fraction(2, 3)*probability >= eps,
            "desired_advantage": str(eps),
            "scope": "ANY full-label controlled POVM whose FINAL effects have original-word Hamming radius<=k",
            "local_gates_sparse_generators_or_shallow_circuits_excluded": False,
            "product_POVMs_generally_have_radius_M_not_one": True,
            "long_relations_or_large_radius_receivers_excluded": False,
            "status": "LOCAL_DERIVATION_REVIEW_PENDING"}


def necessary_coherence_radius(n, digits, copies, desired_advantage=Fraction(1, 10)):
    _integer(n, "dimension", 1); _integer(digits, "digits", 1); _integer(copies, "copies")
    eps = Fraction(desired_advantage)
    if not 0 < eps <= Fraction(2, 3):
        raise ValueError("advantage in (0,2/3] required")
    count, choose = 0, 1
    for radius in range(1, copies+1):
        choose = choose*(copies-radius+1)//radius
        count += choose*6**radius
        if Fraction(2*count, 3*3**(n*digits)) >= eps:
            return {"dimension": n, "digits": digits, "native_copies": copies,
                    "desired_advantage": str(eps), "minimum_radius_not_excluded_by_union_gate": radius,
                    "sufficient_receiver_or_runtime_guarantee": False}
    return {"dimension": n, "digits": digits, "native_copies": copies,
            "desired_advantage": str(eps), "minimum_radius_not_excluded_by_union_gate": None,
            "sufficient_receiver_or_runtime_guarantee": False}


def _field_countercontrol():
    n, q, secret, rng = 3, 3, (2, 0, 1), random.Random(87591)
    records, decoder = [], IncidenceDecoder(n)
    while len(decoder.span.rows) < len(decoder.basis)-1 and len(records) < 1000:
        a, c = (tuple(rng.randrange(q) for _ in range(n)) for _ in range(2))
        record = simulated_record(a, c, secret, q, rng)[0]
        y, z = record.outcome
        sample = IncidenceSample(tuple((v-u) % 3 for u, v in zip(a, c)),
                                 tuple((2*u-v) % 3 for u, v in zip(a, c)), (2*y-z) % 3, (z-y) % 3)
        decoder.add(sample); records.append(record)
    field = decoder.result()
    assert field["secret"] == secret
    result = solve_least_trit(records, range(len(records)))
    assert result["posterior"]["maximum_a_posteriori_trit"] == secret[0]
    return {"calibration_secret_only": secret, "independent_polynomial_field_decoder": field,
            "paired_posterior_control": result,
            "known_easy_counterexample_to_generic_classical_hardness": True}


def build_report():
    controls = []
    for n, r, M in ((1, 4, 8), (1, 8, 8), (2, 4, 8), (4, 32, 8)):
        rng, q = random.Random(87500+n*100+r), 3**r
        secret = tuple(rng.randrange(q) for _ in range(n))
        records = []
        for _ in range(M):
            a, c = (tuple(rng.randrange(q) for _ in range(n)) for _ in range(2))
            records.append(simulated_record(a, c, secret, q, rng)[0])
        controls.append({"calibration_secret_only": [str(s) for s in secret],
                         "fixed_seed": 87500+n*100+r, "baseline": solve_least_trit(records, range(M))})
    cancellation = solve_least_trit((CovariantRecord((3,), (6,), (0, 3), 9),), (0,))
    assert cancellation["posterior"]["exactly_uniform_least_trit"]
    return {"status": "EXACT_JOINT_CLASSICAL_BASELINE_AND_SCOPED_GATES_REVIEW_PENDING",
            "native_IID_live_controls": controls,
            "deterministic_legal_phase_cancellation_countercontrol": cancellation,
            "actual_field_positive_countercontrol": _field_countercontrol(),
            "raw_record_least_trit_gates": [classical_least_trit_gate(n, r, M)
                                           for n, r, M in ((2, 8, 16), (2, 8, 40), (8, 32, 256), (8, 32, 768))],
            "low_record_degree_gates": [low_degree_gate(8, 32, 4096, d) for d in (1, 2, 4, 8, 16, 32)],
            "full_label_sparse_coherence_gates": [sparse_coherence_gate(8, 32, 4096, k) for k in (1, 2, 4, 8, 16, 32, 64)],
            "necessary_full_label_coherence_radius": necessary_coherence_radius(8, 32, 4096),
            "obligations": ["independent review of exact paired likelihood geometry and posterior duality",
                            "no generic polynomial runtime inferred from exact finite posterior",
                            "preserve paired noise correlations, roots, phase cancellations and original IID sampling",
                            "least-trit mean guarantee needs a proven average, not one calibrated MAP guess",
                            "compare any proposed receiver against this actual joint baseline and the field countercontrol"],
            "accepted_candidate": False, "polynomial_higher_root_native_weak_learner": False,
            "general_classical_hardness_or_quantum_advantage_claim": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
        print(json.dumps({"report": str(REPORT), "live_native_controls": len(report["native_IID_live_controls"]),
                          "polynomial_higher_root_native_weak_learner": False}))
    else:
        print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
