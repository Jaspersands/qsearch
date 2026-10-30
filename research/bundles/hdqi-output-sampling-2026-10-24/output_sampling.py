"""Classical full HDQI computational-output sampling with a fiber budget.

The implementation uses explicit physical Paulis, forward decoding,
rational probabilities and signed words. Finite law enumeration is separate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"hdqi-decoded-observables-2026-10-24"))
sys.path.insert(0, str(ROOT/"central-rank-2026-10-23"))
import decoded_observables as d
from central_rank import row_basis
s, c = d.s, d.c


def pure_z_basis(model):
    rows = [tuple((x >> j) & 1 for j in range(model.n))+
            tuple((z >> j) & 1 for j in range(model.n)) for x, z, _ in model.paulis]
    basis = row_basis(rows, 2)
    z_basis = tuple(sum(row[model.n+j] << j for j in range(model.n))
                    for row in basis if not any(row[:model.n]))
    return {"rank_B": len(basis), "rank_X": len(basis)-len(z_basis),
            "fiber_rank": len(z_basis), "fiber_bound": 1 << len(z_basis),
            "z_basis": z_basis}


def decoder_value(model, decoder, syndrome):
    answer = decoder(syndrome)
    if type(answer) is not int or not 0 <= answer < 1 << model.pilot.m:
        raise ValueError("decoder must return an m-bit mask")
    return answer


def fiber(model, decoder, representative, basis, max_fiber):
    if type(representative) is not int or not 0 <= representative < 1 << model.pilot.m:
        raise ValueError("invalid representative")
    if 1 << len(basis) > max_fiber:
        raise s.BudgetExceeded("measurement fiber enumeration exceeds budget")
    syndrome = model.label(representative)
    residue = representative ^ decoder_value(model, decoder, syndrome)
    out = []
    for mask in range(1 << len(basis)):
        change = 0
        for j, vector in enumerate(basis):
            if mask >> j & 1:
                change ^= vector
        target = syndrome ^ (change << model.n)
        y = residue ^ decoder_value(model, decoder, target)
        if model.label(y) == target:
            out.append(y)
    if representative not in out or len(out) != len(set(out)):
        raise ArithmeticError("incomplete or duplicated fiber")
    return residue, tuple(sorted(out))


def plan(model, epsilon=F(1, 8), delta=F(1, 16)):
    base = c.precision_ledger(model.pilot, epsilon, delta)
    ranks = pure_z_basis(model)
    cb, bound, eps, delta = base["ratio_upper"], ranks["fiber_bound"], base["epsilon"], base["delta"]
    k = 1+s.ceil_fraction(8*cb*bound/eps)
    bits, rounds = 1, 0
    while F(1, 2**bits) > eps/(64*cb):
        bits += 1
    while F(1, 2**rounds) > delta:
        rounds += 1
    trials = 2*cb*bound*rounds
    return {**ranks, "epsilon": eps, "delta": delta, "ratio_upper": cb,
            "ratio_bound_method": base["ratio_bound_method"], "site_tail": base["site_tail"],
            "weight_bits": bits, "weight_relative_error": F(1, 2**bits),
            "signs_per_trial": k, "max_trials": trials, "max_words": trials*k,
            "max_word_letters": base["max_word_letters"],
            "max_decoder_calls": trials*(bound+1),
            "success_probability_lower": F(1, 2*cb*bound),
            "failure_probability_upper": F(1, 2**rounds),
            "mixture_bias_upper": F(2*cb*bound, k-1)}


def phase(model, y, right):
    _, z, exponent = model.ordered(y)
    return (exponent+2*(z & right).bit_count()+
            (2 if c.known_sign(model.pilot, y) < 0 else 0)) % 4


def bernoulli(probability, rng):
    probability = F(probability)
    if not 0 <= probability <= 1:
        raise ValueError("invalid acceptance probability")
    return rng.randrange(probability.denominator) < probability.numerator


class Sampler:
    def __init__(self, model, decoder, epsilon=F(1, 8), delta=F(1, 16), *,
                 max_fiber=4096, max_word_budget=100000):
        self.model, self.decoder = model, decoder
        self.plan = plan(model, epsilon, delta)
        if type(max_fiber) is not int or max_fiber < self.plan["fiber_bound"]:
            raise s.BudgetExceeded("measurement fiber exceeds budget; no output produced")
        if type(max_word_budget) is not int or max_word_budget < self.plan["max_words"]:
            raise s.BudgetExceeded("signed-word budget insufficient; no output produced")
        self.max_fiber = max_fiber
        self.even, self.odd, self.proposals = c.tables(model.pilot, self.plan["site_tail"])

    def probability(self, y):
        return math.prod(law.probabilities()[y >> i & 1][1] for i, law in enumerate(self.proposals))

    def sign(self, y, rng):
        word = []
        for i in range(self.model.pilot.m):
            law = self.odd[i] if y >> i & 1 else self.even[i]
            if law is None:
                raise ValueError("zero-probability source label")
            word.extend([i]*law.law.draw(rng))
        rng.shuffle(word)
        sign, endpoint = s.word_sign(self.model.pilot, word)
        assert endpoint == y
        return sign, len(word)

    def fiber_law(self, representative):
        residue, labels = fiber(self.model, self.decoder, representative,
                                self.plan["z_basis"], self.max_fiber)
        probabilities = [self.probability(y) for y in labels]
        weights = [d.sqrt_lower(q, self.plan["weight_bits"]) for q in probabilities]
        total, envelope = sum(probabilities), sum(weights)
        if not total or not envelope:
            raise ValueError("zero-probability fiber")
        proposal = s.RationalLaw.create(labels, weights)
        acceptance = envelope*envelope/(self.plan["fiber_bound"]*total)
        if not 0 < acceptance <= 1:
            raise ArithmeticError("invalid fiber envelope")
        return residue, proposal, acceptance

    def sample(self, rng):
        words, letters, decoder_calls = 0, 0, 0
        k = self.plan["signs_per_trial"]
        for trial in range(1, self.plan["max_trials"]+1):
            y0 = sum(law.draw(rng) << i for i, law in enumerate(self.proposals))
            residue, law, acceptance = self.fiber_law(y0)
            decoder_calls += self.plan["fiber_bound"]+1
            right = rng.getrandbits(self.model.n)
            if not bernoulli(acceptance, rng):
                continue
            real, imag = 0, 0
            for _ in range(k):
                y = law.draw(rng)
                sign, length = self.sign(y, rng)
                exponent = (phase(self.model, y, right)+(2 if sign < 0 else 0)) % 4
                real += (1, 0, -1, 0)[exponent]
                imag += (0, 1, 0, -1)[exponent]
                words, letters = words+1, letters+length
            if rng.randrange(k*k) < real*real+imag*imag:
                return {"status": "sample", "left": right ^ (self.model.label(y0) & ((1 << self.model.n)-1)),
                        "right": right, "residue": residue, "trials": trial,
                        "words": words, "letters": letters, "decoder_calls": decoder_calls}
        return {"status": "failure", "left": None, "right": None, "residue": None,
                "trials": self.plan["max_trials"], "words": words,
                "letters": letters, "decoder_calls": decoder_calls}


def finite_law(sampler):
    """Exact finite accepted law, including its controlled bias; never core."""
    model = sampler.model
    if model.pilot.m > 3 or model.n > 2:
        raise ValueError("finite law requires m<=3,n<=2")
    checker = d.Estimator(model, sampler.decoder, (0, 0, 0), sampler.plan["epsilon"], sampler.plan["delta"])
    moments = d.finite_moments(checker)
    qs, means = moments["q"], moments["means"]
    weights = [d.sqrt_lower(q, sampler.plan["weight_bits"]) for q in qs]
    groups = {}
    for y in range(1 << model.pilot.m):
        label = model.label(y)
        key = (y ^ decoder_value(model, sampler.decoder, label), label & ((1 << model.n)-1))
        groups.setdefault(key, []).append(y)
    k, bound = sampler.plan["signs_per_trial"], sampler.plan["fiber_bound"]
    accepted, target, envelope = {}, {}, {}
    dw = sum(w*w*r*r for w, r in zip(weights, means))
    zs = sum(sum(weights[y] for y in group)**2 for group in groups.values())
    for (residue, x), group in groups.items():
        sf = sum(weights[y] for y in group)
        for right in range(1 << model.n):
            real, imag = F(0), F(0)
            for y in group:
                exponent = phase(model, y, right)
                real += weights[y]*means[y]*(1, 0, -1, 0)[exponent]
                imag += weights[y]*means[y]*(0, 1, 0, -1)[exponent]
            square = real*real+imag*imag
            event = (residue, right ^ x, right)
            target[event] = square/((1 << model.n)*dw)
            envelope[event] = sf*sf/((1 << model.n)*zs)
            accepted[event] = F((k-1)*square+sf*sf, k*bound*(1 << model.n))
    success = sum(accepted.values())
    return {"accepted": {key: value/success for key, value in accepted.items()},
            "target": target, "envelope": envelope,
            "alpha": zs/((k-1)*dw+zs), "success": success, "weighted_norm": dw,
            "weights": weights, "means": means, "q": qs}


def large_fixture(n=128):
    lower = [sum(1 << j for j in range(max(0, i-4), i)) for i in range(n)]
    paulis = [(1 << i, lower[i], 0) for i in range(n)]+[(0, 1, 0)]
    model = d.Physical.create(n, paulis, [1]*(n+1), F(1, 16))

    def decoder(syndrome):
        x, residual = syndrome & ((1 << n)-1), syndrome >> n
        for i, mask in enumerate(lower):
            if x >> i & 1:
                residual ^= mask
        return x | (residual << n) if residual in (0, 1) else 0

    return model, decoder


def receipt():
    import commuting_linear
    model, decoder = large_fixture()
    sampler, rng = Sampler(model, decoder), random.Random(24028)
    rows = [sampler.sample(rng) for _ in range(16)]
    small = d.Physical.create(1, [(0, 1, 0)], [1], 1)
    control = Sampler(small, lambda syndrome: syndrome >> 1)
    exact = finite_law(control)
    here = Path(__file__).resolve().parent
    files = [here/f for f in ("output_sampling.py", "test_output_sampling.py", "commuting_linear.py",
                              "test_commuting_linear.py", "OUTPUT_SAMPLING.md", "HANDOFF.md")]
    files += [ROOT/"hdqi-decoded-observables-2026-10-24"/f for f in ("decoded_observables.py", "DECODED_OBSERVABLES.md")]
    files += [ROOT/"hdqi-coherent-sign-2026-10-24"/f for f in ("coherent_sign.py", "COHERENT_SIGN.md")]
    files += [ROOT/"hdqi-sign-sampler-2026-10-24"/f for f in ("sign_sampler.py", "SIGN_SAMPLER.md")]
    files += [ROOT/"central-rank-2026-10-23/central_rank.py"]
    diagonal = d.Physical.create(128, [(0, 1 << i, 0) for i in range(128)], [1]*128, F(1, 2))
    shortcut = commuting_linear.Sampler(diagonal, commuting_linear.build_linear_decoder(diagonal))
    shortcut_rng = random.Random(24029)
    shortcut_outputs = [shortcut.sample(shortcut_rng) for _ in range(16)]
    return {"status": "local_unreviewed_full_physical_output_sampler",
            "input": {"physical_qubits": model.n, "pilot_labels": model.pilot.m,
                      "physical_generators": len(model.paulis), "beta": str(model.pilot.beta)},
            "plan": s.public_plan(sampler.plan),
            "live": {"samples": sum(row["status"] == "sample" for row in rows),
                     "failures": sum(row["status"] == "failure" for row in rows),
                     "words": sum(row["words"] for row in rows), "letters": sum(row["letters"] for row in rows),
                     "decoder_calls": sum(row["decoder_calls"] for row in rows),
                     "outcomes": rows, "statevector_used": False, "amplitude_oracle_used": False},
            "one_Z_falsifier": {"accepted_left_zero": str(sum(p for (_, left, _), p in exact["accepted"].items() if left == 0)),
                                "phase_discarded_left_zero": "1/2", "alpha": str(exact["alpha"])},
            "commuting_linear_high_rank_run": {"ledger": shortcut.ledger(), "samples": len(shortcut_outputs),
                                               "outputs": shortcut_outputs, "statevector_used": False},
            "general_high_rank_sampling_solved": False, "gibbs_accuracy_assumed": False,
            "hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("receipt.json"))
    args = parser.parse_args()
    data = receipt()
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"output": str(args.output.resolve()), "samples": data["live"]["samples"],
                      "words": data["live"]["words"], "fiber_rank": data["plan"]["fiber_rank"]}))

