"""Classical HDQI pilot sampling with explicit sign and truncation budgets.

The core uses rational probabilities, parity-conditioned words, and integers.
It never constructs a statevector or evaluates a target amplitude.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import random


def rational(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a numeric model parameter")
    return F(str(value)) if isinstance(value, float) else F(value)


def ceil_fraction(value):
    return -(-value.numerator // value.denominator)


@dataclass(frozen=True)
class Model:
    couplings: tuple[F, ...]
    beta: F
    edges: tuple[tuple[int, int], ...]
    lower_masks: tuple[int, ...]

    @classmethod
    def create(cls, couplings, beta, edges):
        js, beta = tuple(map(rational, couplings)), rational(beta)
        m = len(js)
        if m == 0 or any(abs(j) > 1 for j in js) or not 0 <= beta <= 1:
            raise ValueError("require m>=1, |J_i|<=1, 0<=beta<=1")
        pairs, masks = set(), [0] * m
        for i, j in edges:
            if any(type(v) is not int or not 0 <= v < m for v in (i, j)) or i == j:
                raise ValueError("invalid edge")
            i, j = sorted((i, j))
            if (i, j) in pairs:
                raise ValueError("duplicate edge")
            pairs.add((i, j))
            masks[j] |= 1 << i
        return cls(js, beta, tuple(sorted(pairs)), tuple(masks))

    @property
    def m(self):
        return len(self.couplings)

    @property
    def x(self):
        return tuple(self.beta * abs(j) / 2 for j in self.couplings)

    @property
    def degree(self):
        counts = [0] * self.m
        for i, j in self.edges:
            counts[i] += 1
            counts[j] += 1
        return max(counts)


@dataclass(frozen=True)
class RationalLaw:
    outcomes: tuple[int, ...]
    cumulative: tuple[int, ...]
    normalizer: F

    @classmethod
    def create(cls, outcomes, weights):
        weights = tuple(map(F, weights))
        if not weights or len(outcomes) != len(weights) or any(w < 0 for w in weights):
            raise ValueError("invalid discrete law")
        total = sum(weights)
        if total <= 0:
            raise ValueError("zero probability law")
        denominator = math.lcm(*(w.denominator for w in weights))
        cumulative, current = [], 0
        for w in weights:
            current += w.numerator * (denominator // w.denominator)
            cumulative.append(current)
        return cls(tuple(outcomes), tuple(cumulative), total)

    def draw(self, rng):
        return self.outcomes[bisect_right(self.cumulative, rng.randrange(self.cumulative[-1]))]

    def probabilities(self):
        previous, rows = 0, []
        for outcome, current in zip(self.outcomes, self.cumulative):
            rows.append((outcome, F(current - previous, self.cumulative[-1])))
            previous = current
        return tuple(rows)


@dataclass(frozen=True)
class ParityLaw:
    law: RationalLaw
    omitted_weight_bound: F


def parity_law(x, parity, eta):
    x, eta = rational(x), rational(eta)
    if not 0 <= x <= F(1, 2) or parity not in (0, 1) or not 0 < eta < 1:
        raise ValueError("require x in [0,1/2], parity 0/1, eta in (0,1)")
    if x == 0 and parity:
        raise ValueError("odd parity at zero coupling has zero probability")
    weights, outcomes = [F(1)], [parity]
    while True:
        k = outcomes[-1]
        ratio = x*x / ((k+1) * (k+2))
        tail = weights[-1] * ratio / (1-ratio)
        if tail <= eta:
            return ParityLaw(RationalLaw.create(outcomes, weights), tail)
        weights.append(weights[-1] * ratio)
        outcomes.append(k+2)


def ratio_bounds(m, degree, mass, jmax, beta):
    if type(m) is not int or type(degree) is not int or not 0 <= degree < m:
        raise ValueError("invalid graph size/degree")
    mass, jmax, beta = map(rational, (mass, jmax, beta))
    if not 0 <= jmax <= 1 or not 0 <= beta <= 1 or not jmax*jmax <= mass <= m*jmax*jmax:
        raise ValueError("inconsistent mass/coupling/temperature parameters")
    lam, d_plus_one = (beta*jmax)**2, degree+1
    mass_bound = beta*beta*mass/2
    cluster_bound = (128*m*d_plus_one*lam*lam/(1-16*d_plus_one*lam)
                     if d_plus_one*lam <= F(1, 64) else None)
    selected = mass_bound if cluster_bound is None else min(mass_bound, cluster_bound)
    method = "mass" if selected == mass_bound else "cluster"
    if degree == 0:
        selected, method = F(0), "commuting_exact"
    return {"mass_exponent": mass_bound, "cluster_exponent": cluster_bound,
            "exponent": selected, "ratio_bound_method": method,
            "ratio_upper": 3**ceil_fraction(selected)}


def budget(model, epsilon=F(1, 8), delta=F(1, 16)):
    epsilon, delta = rational(epsilon), rational(delta)
    if not 0 < epsilon < 1 or not 0 < delta <= F(1, 4):
        raise ValueError("require epsilon in (0,1), delta in (0,1/4]")
    mass = sum(j*j for j in model.couplings)
    bounds = ratio_bounds(model.m, model.degree, mass, max(map(abs, model.couplings)), model.beta)
    cbar = bounds["ratio_upper"]
    k = 1 + ceil_fraction(4 * cbar / epsilon)
    r = 0
    while F(1, 2**r) > delta/2:
        r += 1
    attempts = cbar * r
    eta = min(epsilon, delta) / (16 * attempts * model.m * (k+5))
    return {"mass": mass, **bounds,
            "signs_per_trial": k, "max_trials": attempts,
            "max_words": k * attempts, "site_tail": eta,
            "epsilon": epsilon, "delta": delta,
            "ideal_bias_bound": F(cbar, k-1+cbar),
            "joint_precision_bound": attempts * model.m * (k+5) * eta,
            "ideal_failure_bound": F(1, 2**r)}


def word_sign(model, word):
    mask, sign = 0, 1
    for i in word:
        if type(i) is not int or not 0 <= i < model.m:
            raise ValueError("invalid word label")
        if (mask & model.lower_masks[i]).bit_count() % 2:
            sign = -sign
        mask ^= 1 << i
    return sign, mask


class BudgetExceeded(RuntimeError):
    pass


class Sampler:
    def __init__(self, model, epsilon=F(1, 8), delta=F(1, 16), max_word_budget=100000):
        self.model, self.plan = model, budget(model, epsilon, delta)
        self.point_mass = all(x == 0 for x in model.x)
        if type(max_word_budget) is not int or max_word_budget < 0:
            raise ValueError("max_word_budget must be a nonnegative integer")
        if not self.point_mass and self.plan["max_words"] > max_word_budget:
            raise BudgetExceeded(f"need up to {self.plan['max_words']} words per sample; "
                                 f"budget is {max_word_budget}; no sample produced")
        self.even, self.odd, self.proposal = [], [], []
        eta = self.plan["site_tail"]
        for x in model.x:
            even = parity_law(x, 0, eta)
            odd = parity_law(x, 1, eta) if x else None
            e = even.law.normalizer
            o = x * odd.law.normalizer if odd else F(0)
            self.even.append(even)
            self.odd.append(odd)
            self.proposal.append(RationalLaw.create((0, 1), (e*e, o*o)))
        self.word_length_cap = sum(max(e.law.outcomes[-1], o.law.outcomes[-1] if o else 0)
                                   for e, o in zip(self.even, self.odd))

    def resource_ledger(self):
        laws = [p.law for p in self.even] + [p.law for p in self.odd if p] + self.proposal
        return {"max_word_letters": self.word_length_cap,
                "max_total_letters_per_sample": self.word_length_cap * self.plan["max_words"],
                "largest_probability_integer_bits": max(law.cumulative[-1].bit_length() for law in laws)}

    def draw_proposal(self, rng):
        return sum(law.draw(rng) << i for i, law in enumerate(self.proposal))

    def conditional_word(self, mask, rng):
        if type(mask) is not int or not 0 <= mask < 1 << self.model.m:
            raise ValueError("invalid label mask")
        word = []
        for i in range(self.model.m):
            law = self.odd[i] if mask >> i & 1 else self.even[i]
            if law is None:
                raise ValueError("proposed label has zero probability")
            word.extend([i] * law.law.draw(rng))
        rng.shuffle(word)
        sign, endpoint = word_sign(self.model, word)
        if endpoint != mask:
            raise ArithmeticError("conditioned word has wrong endpoint")
        return sign, len(word)

    def sample(self, rng):
        if self.point_mass:
            return {"status": "sample", "mask": 0, "trials": 0,
                    "words": 0, "letters": 0, "exact_point_mass": True}
        k, letters = self.plan["signs_per_trial"], 0
        for trial in range(1, self.plan["max_trials"] + 1):
            mask, score = self.draw_proposal(rng), 0
            for _ in range(k):
                sign, length = self.conditional_word(mask, rng)
                score += sign
                letters += length
            if rng.randrange(k*k) < score*score:
                return {"status": "sample", "mask": mask, "trials": trial,
                        "words": trial*k, "letters": letters, "exact_point_mass": False}
        return {"status": "failure", "mask": None, "trials": self.plan["max_trials"],
                "words": self.plan["max_words"], "letters": letters,
                "reason": "all budgeted rejection proposals failed"}


def exact_sign_sum(model, counts):
    """Small independent multiset-permutation control, not used by the sampler."""
    if len(counts) != model.m or model.m > 4 or sum(counts) > 32 or any(
            type(k) is not int or k < 0 for k in counts):
        raise ValueError("small nonnegative count control required")

    @lru_cache(None)
    def visit(remaining):
        if not any(remaining):
            return 1
        parity = sum((k % 2) << i for i, k in enumerate(remaining))
        total = 0
        for i, k in enumerate(remaining):
            if k:
                child = list(remaining)
                child[i] -= 1
                sign = -1 if (parity & model.lower_masks[i]).bit_count() % 2 else 1
                total += sign * visit(tuple(child))
        return total

    return visit(tuple(counts))


def public_plan(plan):
    return {k: str(v) if isinstance(v, F) else v for k, v in plan.items()}


def receipt():
    controls = []
    fixtures = (("commuting", 3, ()), ("edge", 2, ((0, 1),)),
                ("path", 3, ((0, 1), (1, 2))),
                ("frustrated_jordan_routes", 4, ((0, 1), (0, 2), (0, 3), (1, 2))))
    for name, m, edges in fixtures:
        model = Model.create([1] * m, F(1, 2), edges)
        sampler, rng = Sampler(model), random.Random(24025)
        rows = [sampler.sample(rng) for _ in range(32)]
        controls.append({"name": name, "m": m, "plan": public_plan(sampler.plan),
                         "resources": sampler.resource_ledger(),
                         "samples": sum(row["status"] == "sample" for row in rows),
                         "failures": sum(row["status"] == "failure" for row in rows),
                         "total_words": sum(row["words"] for row in rows),
                         "total_letters": sum(row["letters"] for row in rows),
                         "histogram": {str(y): sum(row["mask"] == y for row in rows)
                                       for y in sorted({r["mask"] for r in rows if r["mask"] is not None})}})
    m = 128
    edges = sorted({tuple(sorted((i, (i+j) % m))) for i in range(m) for j in range(1, 5)})
    model = Model.create([1] * m, F(1, 8), edges)
    sampler, rng = Sampler(model), random.Random(24026)
    rows = [sampler.sample(rng) for _ in range(32)]
    large = {"m": m, "edges": len(edges), "degree": 8, "plan": public_plan(sampler.plan),
             "resources": sampler.resource_ledger(),
             "samples": sum(row["status"] == "sample" for row in rows),
             "failures": sum(row["status"] == "failure" for row in rows),
             "words": sum(row["words"] for row in rows),
             "letters": sum(row["letters"] for row in rows),
             "occupied_counts": [r["mask"].bit_count() for r in rows if r["mask"] is not None],
             "statevector_constructed": False, "amplitude_oracle_used": False}
    here = Path(__file__).resolve().parent
    return {"status": "local_unreviewed_sampling_comparator", "controls": controls,
            "large_explicit_input_run": large,
            "growing_degree_family_parameters_only": [
                {"N": n, "m": n**8, "degree": n**4, "beta": str(F(1, 16*n**3)),
                 "beta_degree": str(F(n, 16)), "input_constructed": False,
                 **public_plan(ratio_bounds(n**8, n**4, n**8, 1, F(1, 16*n**3)))}
                for n in (2, 8, 32, 128)],
            "coherent_preparation_dequantized": False, "degree_gap_proved": False,
            "sampler_bit_probabilities": "rational_integer",
            "hashes": {f: hashlib.sha256((here / f).read_bytes()).hexdigest()
                       for f in ("sign_sampler.py", "test_sign_sampler.py", "SIGN_SAMPLER.md", "HANDOFF.md")}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("receipt.json"))
    args = parser.parse_args()
    data = receipt()
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output.resolve()),
                      "large_samples": data["large_explicit_input_run"]["samples"],
                      "large_words": data["large_explicit_input_run"]["words"]}))
