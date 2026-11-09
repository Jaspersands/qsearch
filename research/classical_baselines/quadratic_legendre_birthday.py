"""Chosen-query quadratic Legendre collision baseline; Sage scientific control.

Run /opt/anaconda3/envs/qsearch-cas/bin/python. The attack receives only p
and a callable returning chi(f(x)); source coefficients stay in the harness.
The center uses a deterministic square-root cover, the width three fixed
birthday attempts. No passive/consecutive-data or novelty claim is made.
"""

import hashlib
import json
from decimal import Decimal, ROUND_CEILING, localcontext
from math import isqrt
from pathlib import Path
from random import Random

from sage.all import GF


PRIMES = (101, 1009, 10007)
SEEDS = (6101, 6102)
WIDTH_ATTEMPTS = 3
VERIFY_SAMPLES = 16


def _character(value):
    return 0 if value == 0 else (1 if value.is_square() else -1)


def _fingerprint_length(p):
    length = 0
    while 64 * p * p * 3 ** length > 4 ** length:
        length += 1
    return length


def _birthday_size(n):
    with localcontext() as context:
        context.prec = 60
        return int((Decimal(n) * Decimal(16).ln()).sqrt().to_integral_value(rounding=ROUND_CEILING))


def _digest(signs):
    return hashlib.sha256(bytes(value + 1 for value in signs)).hexdigest()


def recover(p, oracle, seed):
    """Native inputs: public p, character-only oracle, public random seed.

    All randomness is reproducible scientific-control randomness. It is
    independent of the source's seed stream; probability claims refer to
    ideal independent uniform choices in the mathematical algorithm.
    """
    if p < 37:
        raise ValueError("This fingerprint bound is declared only for p>=37")
    field = GF(p)
    rng = Random(seed)
    counts = {"center_fingerprints": 0, "center_verification": 0,
              "width_fingerprints": 0, "candidate_verification": 0}
    public_character_evaluations = 0

    def query(x, category):
        counts[category] += 1
        value = int(oracle(int(x) % p))
        if value not in (-1, 1):
            raise ValueError("Source violates irreducible quadratic sign promise")
        return value

    length = _fingerprint_length(p)
    cover = isqrt(p - 1) + 1
    offsets = [rng.randrange(p) for _ in range(length)]
    center_table = {}
    for t in range(cover):
        signature = tuple(query(x + t, "center_fingerprints") for x in offsets)
        center_table.setdefault(signature, []).append(t)
    center_witnesses = []
    center = None
    tested_u = []
    for j in range(cover):
        u = j * cover % p
        tested_u.append(u)
        signature = tuple(query(-x + u, "center_fingerprints") for x in offsets)
        for t in center_table.get(signature, ()):
            candidate_center = int(field(t + u) / field(2))
            checks = []
            for _ in range(VERIFY_SAMPLES):
                z = rng.randrange(p)
                left = query(candidate_center + z, "center_verification")
                right = query(candidate_center - z, "center_verification")
                checks.append({"z": z, "left": left, "right": right})
            accepted = all(row["left"] == row["right"] for row in checks)
            center_witnesses.append({"t": t, "u": u, "candidate_center": candidate_center,
                                     "signature_sha256": _digest(signature), "checks": checks,
                                     "accepted": accepted})
            if accepted:
                center = candidate_center
                break
        if center is not None:
            break
    result = {"prime": p, "public_seed": seed, "fingerprint_length": length,
              "fingerprint_exact_inequality": {"lhs": 64 * p * p * 3 ** length,
                                                "rhs": 4 ** length},
              "center": {"cover_size": cover, "offsets": offsets, "tested_u": tested_u,
                         "collision_candidates": center_witnesses, "recovered_center": center},
              "width_attempts": [], "status": "CENTER_BUDGET_FAILURE"}

    if center is not None:
        eta_trials = []
        while True:
            eta = rng.randrange(1, p)
            symbol = _character(field(eta))
            public_character_evaluations += 1
            eta_trials.append({"value": eta, "character": symbol})
            if symbol == -1:
                break
        quotient_size = (p - 1) // 2
        list_size = _birthday_size(quotient_size)
        result["public_nonsquare_search"] = eta_trials
        result["quotient_size"] = quotient_size
        result["width_list_size"] = list_size
        result["status"] = "WIDTH_BUDGET_FAILURE"
        for attempt_index in range(WIDTH_ATTEMPTS):
            ys = [rng.randrange(1, p) for _ in range(length)]
            # min(z,p-z) representatives are exactly 1,...,(p-1)/2.
            first = rng.sample(range(1, quotient_size + 1), list_size)
            second = [rng.randrange(1, quotient_size + 1) for _ in range(list_size)]
            reference = {}
            for v in first:
                signature = tuple(_character((field(v) * field(y)) ** 2 - field(eta)) for y in ys)
                public_character_evaluations += length
                reference.setdefault(signature, []).append(v)
            attempt = {"index": attempt_index + 1, "offsets": ys,
                       "reference_representatives": first, "sampled_hidden_representatives": second,
                       "tested_hidden_representatives": [], "collision_candidates": [],
                       "status": "NO_ACCEPTED_COLLISION"}
            for u in second:
                attempt["tested_hidden_representatives"].append(u)
                signature = tuple(query(center + u * y, "width_fingerprints") for y in ys)
                for v in reference.get(signature, ()):
                    r_squared = (field(u) / field(v)) ** 2
                    d = field(eta) * r_squared
                    b = -field(2) * field(center)
                    c = field(center) ** 2 - d
                    checks = []
                    for _ in range(VERIFY_SAMPLES):
                        x = rng.randrange(p)
                        observed = query(x, "candidate_verification")
                        expected = _character(field(x) ** 2 + b * field(x) + c)
                        public_character_evaluations += 1
                        checks.append({"x": x, "observed": observed, "predicted": expected})
                    accepted = all(row["observed"] == row["predicted"] for row in checks)
                    witness = {"u": u, "v": v, "r_squared": int(r_squared), "eta": eta,
                               "d": int(d), "b": int(b), "c": int(c),
                               "signature_sha256": _digest(signature),
                               "verification": checks, "accepted": accepted}
                    attempt["collision_candidates"].append(witness)
                    if accepted:
                        attempt["status"] = "VERIFIED_CANDIDATE"
                        result["recovered"] = {"b": int(b), "c": int(c), "center": center, "d": int(d)}
                        result["status"] = "VERIFIED_CANDIDATE"
                        break
                if result["status"] == "VERIFIED_CANDIDATE":
                    break
            result["width_attempts"].append(attempt)
            if result["status"] == "VERIFIED_CANDIDATE":
                break
    result["query_counts"] = counts
    result["total_native_queries"] = sum(counts.values())
    result["public_character_evaluations"] = public_character_evaluations
    return result


def _source_case(p, seed):
    field = GF(p)
    source_rng = Random(seed)
    a = source_rng.randrange(p)
    while True:
        d = source_rng.randrange(1, p)
        if _character(field(d)) == -1:
            break
    b = -field(2) * field(a)
    c = field(a) ** 2 - field(d)
    native_calls = 0

    def native_oracle(x):
        nonlocal native_calls
        native_calls += 1
        xx = field(x)
        return _character(xx * xx + b * xx + c)

    # Domain-separated source/attack streams; no truth is passed to recover.
    result = recover(p, native_oracle, seed + 1_000_000)
    assert native_calls == result["total_native_queries"]
    result["source_truth_harness_only"] = {"b": int(b), "c": int(c), "center": a, "d": d}
    recovered = result.get("recovered")
    result["coefficient_match"] = recovered is not None and recovered["b"] == int(b) and recovered["c"] == int(c)
    if recovered is not None and not result["coefficient_match"]:
        # Preserve a false acceptance as evidence instead of losing its record
        # to an assertion before the artifact is written.
        result["status"] = "ACCEPTED_INCORRECT_CANDIDATE"
    result["source_seed"] = seed
    return result


def main():
    cases = [_source_case(p, seed) for p in PRIMES for seed in SEEDS]
    output = {
        "id": "QUADRATIC-LEGENDRE-CHOSEN-QUERY-COLLISION-CONTROL-2026-11-05",
        "predeclared_primes": list(PRIMES), "predeclared_source_seeds": list(SEEDS),
        "width_attempt_budget": WIDTH_ATTEMPTS, "verification_samples": VERIFY_SAMPLES,
        "native_contract": "Growing odd prime p>=37, hidden monic irreducible quadratic; only chosen base-field character queries. Output b,c with independent random-query verification.",
        "source_boundary": "Attack receives p, native oracle closure, and public seed only; no coefficients, source values, extension queries, or full-table preprocessing.",
        "center_method": "Deterministic cover t=0,...,B-1 and u=j*B mod p, B=ceil(sqrt(p)); at least one exact center collision conditional on injective random fingerprints.",
        "width_method": "Public nonsquare eta by random rejection; reference and hidden fingerprints on F_p^*/{+1,-1}; first list distinct, second independent uniform with replacement. Three preset attempts maximum, stop on verified success.",
        "analytic_scope": {
            "fingerprints": "IID offsets; L is the least integer with 64*p^2*3^L<=4^L. For ideal uniform randomness, quartic Weil bounds give global bad-fingerprint probability <=1/64 per declared union bound.",
            "width_offsets": "Uniform nonzero offsets: wrong quotient agreement <=(p+3*sqrt(p)-2)/(2*(p-1))<=3/4 for p>=37.",
            "width_failure": "Conditional on valid center and good fingerprints, each attempt misses with probability <=1/16; three independent preset attempts give <=1/4096. Fingerprint error is separate.",
            "time_queries_memory": "O(sqrt(p)*polylog(p)) chosen queries, classical time and memory; public Legendre computations and nonsquare rejection are charged separately. This is exponential in log(p).",
            "randomness": "Saved tests use domain-separated deterministic PRNG streams; probability bounds concern the ideal-random algorithm, not empirical success rates.",
            "nonclaims": "No hardness, efficient quantum decoder, quantum advantage, novelty, passive-data transfer, or consecutive-query transfer.",
        },
        "successes": sum(row["coefficient_match"] for row in cases),
        "budget_failures": sum(row["status"] in ("CENTER_BUDGET_FAILURE", "WIDTH_BUDGET_FAILURE") for row in cases),
        "incorrect_acceptances": sum(row["status"] == "ACCEPTED_INCORRECT_CANDIDATE" for row in cases),
        "cases": cases,
    }
    destination = Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"artifact": str(destination), "successes": output["successes"],
                      "budget_failures": output["budget_failures"],
                      "native_queries": [row["total_native_queries"] for row in cases]}, sort_keys=True))


if __name__ == "__main__":
    main()
