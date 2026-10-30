"""Classical decoded-Pauli estimator with explicit sign/precision budgets.

Diagnostic draws do not carry the certified median-of-means guarantee.
Finite moment enumeration is a capped algebra control, not the estimator.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import math
from pathlib import Path
import random
import statistics
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"hdqi-coherent-sign-2026-10-24"))
import coherent_sign as c
s = c.s


def multiply(left, right):
    x, z, p = left
    u, v, q = right
    return x ^ u, z ^ v, (p+q+2*(z & u).bit_count()) % 4


def dagger(pauli):
    x, z, p = pauli
    return x, z, (-p+2*(x & z).bit_count()) % 4


@dataclass(frozen=True)
class Physical:
    n: int
    paulis: tuple[tuple[int, int, int], ...]
    pilot: s.Model

    @classmethod
    def create(cls, n, paulis, couplings, beta):
        if type(n) is not int or n < 1:
            raise ValueError("positive physical qubit count required")
        ps = tuple(tuple(p) for p in paulis)
        for p in ps:
            validate_pauli(n, p)
        js = tuple(couplings)
        if len(ps) != len(js):
            raise ValueError("one coupling per physical Pauli required")
        edges = [(i, j) for i in range(len(ps)) for j in range(i+1, len(ps))
                 if ((ps[i][0] & ps[j][1]).bit_count()+(ps[j][0] & ps[i][1]).bit_count()) % 2]
        return cls(n, ps, s.Model.create(js, beta, edges))

    def label(self, mask):
        x, z = 0, 0
        for i, (xi, zi, _) in enumerate(self.paulis):
            if mask >> i & 1:
                x, z = x ^ xi, z ^ zi
        return x | (z << self.n)

    def ordered(self, mask):
        out = (0, 0, 0)
        for i, p in enumerate(self.paulis):
            if mask >> i & 1:
                out = multiply(out, p)
        return out


def validate_pauli(n, pauli):
    if len(pauli) != 3 or any(type(v) is not int for v in pauli):
        raise ValueError("Pauli requires integer x,z,phase")
    x, z, phase = pauli
    if not 0 <= x < 1 << n or not 0 <= z < 1 << n or not 0 <= phase < 4:
        raise ValueError("Pauli out of range")
    if (phase-(x & z).bit_count()) % 2:
        raise ValueError("physical observable/generator must be Hermitian")


def partner(model, decoder, observable, y):
    validate_pauli(model.n, observable)
    if type(y) is not int or not 0 <= y < 1 << model.pilot.m:
        raise ValueError("invalid pilot mask")
    syndrome = model.label(y)
    target = syndrome ^ observable[0] ^ (observable[1] << model.n)
    left, right = decoder(syndrome), decoder(target)
    if any(type(v) is not int or not 0 <= v < 1 << model.pilot.m for v in (left, right)):
        raise ValueError("decoder must return an m-bit mask for every syndrome")
    other = y ^ left ^ right
    if model.label(other) != target:
        return None
    phase = multiply(dagger(model.ordered(other)), multiply(observable, model.ordered(y)))
    if phase[:2] != (0, 0):
        raise ArithmeticError("partner phase is not scalar")
    return other, (1, 0, -1, 0)[phase[2]]


def sqrt_lower(value, bits):
    value = F(value)
    if value < 0 or type(bits) is not int or bits < 1:
        raise ValueError("nonnegative rational and positive precision required")
    if not value:
        return F(0)
    a, b = value.numerator, value.denominator
    exponent = a.bit_length()-b.bit_length()
    below_power = (a < b << exponent) if exponent >= 0 else ((a << -exponent) < b)
    if below_power:
        exponent -= 1
    shift = bits-exponent//2
    if shift >= 0:
        return F(math.isqrt((a << (2*shift))//b), 1 << shift)
    return F(math.isqrt(a//(b << (-2*shift))) * (1 << -shift))


def plan(model, epsilon=F(1, 8), delta=F(1, 16)):
    ledger = c.precision_ledger(model.pilot, epsilon, delta)
    eps, delta, cb = ledger["epsilon"], ledger["delta"], ledger["ratio_upper"]
    gamma, bits, rounds = eps/(16*cb), 1, 0
    while F(1, 2**bits) > gamma/2:
        bits += 1
    while F(1, 2**rounds) > delta/4:
        rounds += 1
    block, groups = s.ceil_fraction(16/(gamma*gamma)), 8*rounds+1
    return {"epsilon": eps, "delta": delta, "ratio_upper": cb,
            "site_tail": ledger["site_tail"], "moment_error": gamma,
            "weight_relative_error": F(1, 2**bits), "weight_bits": bits,
            "block_draws": block, "blocks": groups, "total_draws": block*groups,
            "max_words": 3*block*groups, "max_word_letters": ledger["max_word_letters"],
            "denominator_refusal_threshold": F(1, 4*cb),
            "ratio_bound_method": ledger["ratio_bound_method"]}


class Estimator:
    def __init__(self, model, decoder, observable, epsilon=F(1, 8), delta=F(1, 16)):
        validate_pauli(model.n, observable)
        self.model, self.decoder, self.observable = model, decoder, observable
        self.plan = plan(model, epsilon, delta)
        self.even, self.odd, self.proposals = c.tables(model.pilot, self.plan["site_tail"])

    def probability(self, y):
        return math.prod(law.probabilities()[y >> i & 1][1] for i, law in enumerate(self.proposals))

    def sign(self, y, rng):
        word = []
        for i in range(self.model.pilot.m):
            p = self.odd[i] if y >> i & 1 else self.even[i]
            if p is None:
                raise ValueError("zero-probability word label")
            word.extend([i]*p.law.draw(rng))
        rng.shuffle(word)
        sign, endpoint = s.word_sign(self.model.pilot, word)
        assert endpoint == y
        return sign, len(word)

    def draw(self, rng):
        y = sum(law.draw(rng) << i for i, law in enumerate(self.proposals))
        first, l1 = self.sign(y, rng)
        second, l2 = self.sign(y, rng)
        other = partner(self.model, self.decoder, self.observable, y)
        numerator, words, letters = F(0), 2, l1+l2
        if other is not None and other[1] and self.probability(other[0]):
            t, phase = other
            third, l3 = self.sign(t, rng)
            weight = sqrt_lower(self.probability(t)/self.probability(y), self.plan["weight_bits"])
            numerator = phase*c.known_sign(self.model.pilot, y)*c.known_sign(self.model.pilot, t)*first*third*weight
            words, letters = 3, letters+l3
        return numerator, F(first*second), words, letters

    def estimate(self, rng, max_draws):
        if type(max_draws) is not int or max_draws < self.plan["total_draws"]:
            raise s.BudgetExceeded(f"need {self.plan['total_draws']} draws; no certified estimate produced")
        numerators, denominators, words, letters = [], [], 0, 0
        for _ in range(self.plan["blocks"]):
            a, b = F(0), F(0)
            for _ in range(self.plan["block_draws"]):
                x, y, w, l = self.draw(rng)
                a, b, words, letters = a+x, b+y, words+w, letters+l
            numerators.append(a/self.plan["block_draws"])
            denominators.append(b/self.plan["block_draws"])
        a, b = statistics.median(numerators), statistics.median(denominators)
        if b < self.plan["denominator_refusal_threshold"]:
            return {"status": "refused", "estimate": None, "words": words, "letters": letters}
        return {"status": "estimate", "estimate": max(F(-1), min(F(1), a/b)),
                "epsilon": self.plan["epsilon"], "delta": self.plan["delta"],
                "words": words, "letters": letters}


def finite_moments(estimator):
    """Exact rational finite-law control; deliberately limited to m<=3."""
    model = estimator.model.pilot
    if model.m > 3:
        raise ValueError("finite moments require m<=3")
    means, probabilities = [], []
    for y in range(1 << model.m):
        probabilities.append(estimator.probability(y))
        if not probabilities[-1]:
            means.append(F(0))
            continue
        laws = [estimator.odd[i] if y >> i & 1 else estimator.even[i] for i in range(model.m)]
        mean = F(0)
        for entries in product(*(p.law.probabilities() for p in laws)):
            counts = tuple(k for k, _ in entries)
            multiplicity = math.factorial(sum(counts))//math.prod(math.factorial(k) for k in counts)
            mean += math.prod(p for _, p in entries)*F(s.exact_sign_sum(model, counts), multiplicity)
        means.append(mean)
    numerator, denominator, second_moment = F(0), F(0), F(0)
    for y, q in enumerate(probabilities):
        denominator += q*means[y]**2
        other = partner(estimator.model, estimator.decoder, estimator.observable, y)
        if not q or other is None or not probabilities[other[0]]:
            continue
        t, phase = other
        weight = sqrt_lower(probabilities[t]/q, estimator.plan["weight_bits"])
        numerator += q*weight*phase*c.known_sign(model, y)*c.known_sign(model, t)*means[y]*means[t]
        second_moment += q*weight*weight*phase*phase
    return {"numerator": numerator, "denominator": denominator,
            "numerator_second_moment": second_moment, "means": means, "q": probabilities}


def receipt():
    model = Physical.create(1, [(1, 0, 0), (1, 0, 0), (0, 1, 0)], [1, F(-1, 2), 1], F(1, 4))
    decoder = lambda syndrome: {0: 0, 1: 1, 2: 4, 3: 5}[syndrome]
    estimator = Estimator(model, decoder, (1, 0, 0))
    moments = finite_moments(estimator)
    rng = random.Random(24027)
    draws = [estimator.draw(rng) for _ in range(128)]
    here = Path(__file__).resolve().parent
    paths = [here/f for f in ("decoded_observables.py", "test_decoded_observables.py", "DECODED_OBSERVABLES.md", "HANDOFF.md")]
    paths += [ROOT/"hdqi-coherent-sign-2026-10-24"/f for f in ("coherent_sign.py", "COHERENT_SIGN.md")]
    paths += [ROOT/"hdqi-sign-sampler-2026-10-24"/f for f in ("sign_sampler.py", "SIGN_SAMPLER.md")]
    return {"status": "local_unreviewed_decoded_observable_comparator",
            "plan": s.public_plan(estimator.plan),
            "finite_exact_moments": {key: str(moments[key]) for key in ("numerator", "denominator", "numerator_second_moment")},
            "diagnostic_only": {"draws": len(draws), "certified_estimate": False,
                                "words": sum(row[2] for row in draws), "letters": sum(row[3] for row in draws),
                                "mean_numerator": str(sum(row[0] for row in draws)/len(draws)),
                                "mean_denominator": str(sum(row[1] for row in draws)/len(draws))},
            "full_output_sampler": False, "gibbs_accuracy_assumed": False,
            "hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("receipt.json"))
    args = parser.parse_args()
    data = receipt()
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"output": str(args.output.resolve()), "diagnostic_draws": 128, "certified_estimate": False}))

