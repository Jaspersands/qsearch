"""Matched classical Pauli readout for conditional-product canonical TFDs.

This is a scoped classical falsifier, not a quantum algorithm or a general
TFD simulator. The written proof still requires independent review.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import acb, acb_mat, arb, ctx, fmpq

from theorems.parity_block_usd_prange import affine_system, uniform_affine_solution

REPORT = ROOT / "research/classical_baselines/coherent_gibbs_readout.json"
PAULIS = "IXYZ"


def _rational(value):
    if type(value) not in (int, Q):
        raise ValueError("exact integer or Fraction required")
    return Q(value)


def _arb(value):
    value = Q(value)
    return arb(fmpq(value.numerator, value.denominator))


def _bounds(value):
    if not value.is_finite():
        raise ArithmeticError("nonfinite interval; increase precision or reject input")
    return Q(str(value.lower().fmpq())), Q(str(value.upper().fmpq()))


def _upper(value, bits=128):
    value = Q(value)
    return Q(-((-value.numerator * (1 << bits)) // value.denominator), 1 << bits)


def _pauli(letter):
    return {
        "I": acb_mat([[1, 0], [0, 1]]),
        "X": acb_mat([[0, 1], [1, 0]]),
        "Y": acb_mat([[0, acb(0, -1)], [acb(0, 1), 0]]),
        "Z": acb_mat([[1, 0], [0, -1]]),
    }[letter]


def _masks(word):
    x = sum(1 << j for j, p in enumerate(word) if p in "XY")
    z = sum(1 << j for j, p in enumerate(word) if p in "YZ")
    return x, z, word.count("Y")


@dataclass(frozen=True)
class BlockModel:
    """Central bit j is bit j of z; columns encode public binary parities."""

    central_bits: int
    columns: tuple[int, ...]
    transverse: tuple[Q, ...]
    longitudinal: tuple[Q, ...]
    coupled: tuple[Q, ...]
    central: tuple[Q, ...]
    beta: Q

    def __post_init__(self):
        if type(self.central_bits) is not int or self.central_bits < 1:
            raise ValueError("positive central width required")
        n = len(self.columns)
        if type(self.columns) is not tuple or not n:
            raise ValueError("nonempty immutable columns required")
        if any(type(f) is not int or not 0 <= f < 1 << self.central_bits for f in self.columns):
            raise ValueError("binary columns must fit central width")
        for name in ("transverse", "longitudinal", "coupled", "central"):
            values = getattr(self, name)
            if type(values) is not tuple or len(values) != n:
                raise ValueError("one immutable coefficient per block required")
            for v in values:
                _rational(v)
        if _rational(self.beta) < 0:
            raise ValueError("nonnegative inverse temperature required")

    @property
    def n(self):
        return len(self.columns)

    def signs(self, z):
        if type(z) is not int or not 0 <= z < 1 << self.central_bits:
            raise ValueError("canonical central assignment required")
        return tuple((f & z).bit_count() & 1 for f in self.columns)


@dataclass(frozen=True)
class PauliReadout:
    central_left: str
    central_right: str
    local_left: str
    local_right: str

    def validate(self, model):
        for word, length in ((self.central_left, model.central_bits),
                             (self.central_right, model.central_bits),
                             (self.local_left, model.n), (self.local_right, model.n)):
            if type(word) is not str or len(word) != length or any(p not in PAULIS for p in word):
                raise ValueError("Pauli word with matching width required")


def local_factors(model, precision=128):
    """F_i(c)=exp(-beta H_i(c)/2) and its squared Frobenius norm."""
    if type(precision) is not int or precision < 64:
        raise ValueError("interval precision at least 64 required")
    factors, weights = [], []
    with ctx.workprec(precision):
        beta = _arb(model.beta)
        for a, b, h, e in zip(model.transverse, model.longitudinal, model.coupled, model.central):
            fs, zs = [], []
            for c in (1, -1):
                z = _rational(b) + _rational(h) * c
                r2 = _rational(a)**2 + z*z
                if r2:
                    r = _arb(r2).sqrt()
                    ch = (beta*r/2).cosh()
                    sh = (beta*r/2).sinh()/r
                else:
                    ch, sh = arb(1), beta/2
                scale = (-beta*_arb(e)*c/2).exp()
                fs.append(acb_mat([
                    [scale*(ch-sh*_arb(z)), -scale*sh*_arb(a)],
                    [-scale*sh*_arb(a), scale*(ch+sh*_arb(z))],
                ]))
                zs.append(2*(-beta*_arb(e)*c).exp() * (beta*_arb(r2).sqrt()).cosh())
            factors.append(tuple(fs))
            weights.append(tuple(zs))
    return tuple(factors), tuple(weights)


class PairedEstimator:
    """Bounded importance estimator; never needs the global partition sum."""

    def __init__(self, model, observable, precision=128):
        observable.validate(model)
        self.model, self.observable, self.precision = model, observable, precision
        self.factors, self.weights = local_factors(model, precision)
        xl, zl, yl = _masks(observable.central_left)
        xr, zr, yr = _masks(observable.central_right)
        self.zero = xl != xr
        self.flip, self.zmask, self.ys = xl, zl ^ zr, yl + yr
        self.contractions = []
        with ctx.workprec(precision):
            for fs, a, b in zip(self.factors, observable.local_left, observable.local_right):
                self.contractions.append(tuple(tuple(
                    (fs[j].conjugate().transpose() * _pauli(a) * fs[k] * _pauli(b).transpose()).trace()
                    for k in range(2)) for j in range(2)))

    def evaluate(self, z):
        signs = self.model.signs(z)
        if self.zero:
            return Q(0), Q(0)
        other = z ^ self.flip
        other_signs = self.model.signs(other)
        with ctx.workprec(self.precision):
            w, wp, contraction = arb(1), arb(1), acb(1)
            for i, (s, t) in enumerate(zip(signs, other_signs)):
                w *= self.weights[i][s]
                wp *= self.weights[i][t]
                contraction *= self.contractions[i][s][t]
            phase = acb(0, 1)**self.ys
            if (self.zmask & other).bit_count() & 1:
                phase = -phase
            lo, hi = _bounds(2*(phase*contraction).real/(w+wp))
        # Intersection uses the proved |estimator| <= 1, not numeric clipping.
        lo, hi = max(Q(-1), lo), min(Q(1), hi)
        if lo > hi:
            raise ArithmeticError("interval contradicts the paired-estimator bound")
        return lo, hi


def kernel_words(model, max_nullity=12):
    """Explicitly charge 2^nullity work; refuse a hidden exponential table."""
    if type(max_nullity) is not int or not 0 <= max_nullity <= 20:
        raise ValueError("kernel enumeration cap must lie in [0,20]")
    equations = tuple((sum(((f >> j) & 1) << i for i, f in enumerate(model.columns)), 0)
                      for j in range(model.central_bits))
    system = affine_system(equations, model.n)
    nullity = len(system["free"])
    if nullity > max_nullity:
        raise ValueError("kernel certificate exceeds explicit enumeration budget")
    basis = []
    for free in system["free"]:
        x = 1 << free
        for row, pivot in zip((r for r in system["rref"] if any(r[:-1])), system["pivots"]):
            if row[free]:
                x |= 1 << pivot
        basis.append(x)
    words = []
    for mask in range(1, 1 << nullity):
        word = 0
        for j, b in enumerate(basis):
            if (mask >> j) & 1:
                word ^= b
        words.append(word)
    return tuple(words)


class PinSampler:
    """Independent public-factor pins; dependent selections produce ABSTAIN."""

    def __init__(self, model, precision=128, coin_bits=64, max_nullity=12):
        if type(coin_bits) is not int or coin_bits < 8:
            raise ValueError("at least eight fair coin bits per pin required")
        self.model, self.coin_bits = model, coin_bits
        _, weights = local_factors(model, precision)
        self.signed_pins, p_upper = [], []
        rounding = Q(0)
        with ctx.workprec(precision):
            for plus, minus in weights:
                lo, hi = _bounds((plus-minus)/(plus+minus))
                lo, hi = max(Q(-1), lo), min(Q(1), hi)
                if lo > hi:
                    raise ArithmeticError("invalid bias enclosure")
                pin = round((lo+hi)/2 * (1 << coin_bits))
                self.signed_pins.append(pin)
                approximation = Q(pin, 1 << coin_bits)
                rounding += max(abs(lo-approximation), abs(hi-approximation))
                p_upper.append(max(abs(lo), abs(hi)))
        words = kernel_words(model, max_nullity)
        a = Q(0)
        for word in words:
            product = Q(1)
            for i in range(model.n):
                if (word >> i) & 1:
                    product *= p_upper[i]
            a += product
        self.kernel_word_count = len(words)
        self.a_upper = _upper(a)
        pin_tv = Q(1) if self.a_upper >= 1 else min(Q(1), self.a_upper+2*self.a_upper/(1-self.a_upper))
        self.rounding_tv = _upper(rounding)
        self.tv_upper = min(Q(1), _upper(pin_tv+self.rounding_tv))

    def draw(self, rng):
        equations = []
        for f, p in zip(self.model.columns, self.signed_pins):
            if rng.getrandbits(self.coin_bits) < abs(p):
                equations.append((f, int(p < 0)))
        system = affine_system(equations, self.model.central_bits)
        if system["rank"] != len(equations):
            return None
        return uniform_affine_solution(system, self.model.central_bits, rng)


def estimate(model, observable, samples, seed, failure=Q(1, 100), precision=128):
    """Confidence statement assumes independent fair coins; seed is a replay aid."""
    if type(samples) is not int or samples < 1:
        raise ValueError("positive sample count required")
    failure = _rational(failure)
    if not 0 < failure < 1:
        raise ValueError("failure probability must lie in (0,1)")
    estimator = PairedEstimator(model, observable, precision)
    sampler = PinSampler(model, precision)
    rng = random.Random(seed)
    lo_sum, hi_sum, abstentions = Q(0), Q(0), 0
    for _ in range(samples):
        z = sampler.draw(rng)
        if z is None:
            abstentions += 1
            continue
        lo, hi = estimator.evaluate(z)
        lo_sum += lo
        hi_sum += hi
    with ctx.workprec(precision):
        _, radius = _bounds((2*(2/_arb(failure)).log()/samples).sqrt())
    lo, hi = lo_sum/samples, hi_sum/samples
    systematic = 2*sampler.tv_upper
    return {
        "samples": samples, "seed": seed, "abstentions": abstentions,
        "mean_lower": str(lo), "mean_upper": str(hi),
        "statistical_radius_upper": str(_upper(radius)),
        "sampler_tv_upper": str(sampler.tv_upper),
        "systematic_observable_bias_upper": str(systematic),
        "confidence_lower": str(max(Q(-1), lo-radius-systematic)),
        "confidence_upper": str(min(Q(1), hi+radius+systematic)),
        "failure_probability_under_iid_fair_coins": str(failure),
        "kernel_words_enumerated": sampler.kernel_word_count,
        "kernel_weight_sum_upper": str(sampler.a_upper),
        "pin_rounding_tv_upper": str(sampler.rounding_tv),
        "prng_is_not_a_certified_fair_coin_source": True,
        "partition_function_oracle_used": False,
        "hilbert_space_table_used": False,
    }


def repetition_model(n):
    if type(n) is not int or n < 3:
        raise ValueError("at least three blocks required")
    return BlockModel(n-1, tuple(1 << i for i in range(n-1))+((1 << (n-1))-1,),
                      (Q(1),)*n, (Q(1, 3),)*n, (Q(1, 2),)*n, (Q(1, 5),)*n, Q(1, 8))


def repetition_reference(model, precision=192):
    """Independent O(N) even-parity contraction for the explicit calibration."""
    expected = tuple(1 << i for i in range(model.n-1))+((1 << (model.n-1))-1,)
    if model.central_bits != model.n-1 or model.columns != expected:
        raise ValueError("reference only applies to the repetition-kernel calibration")
    factors, weights = local_factors(model, precision)
    flip = (1 << model.central_bits)-1
    with ctx.workprec(precision):
        num_plus, num_minus, den_plus, den_minus = arb(1), arb(1), arb(1), arb(1)
        for f, fs, zs in zip(model.columns, factors, weights):
            change = (f & flip).bit_count() & 1
            ts = tuple((fs[j] * fs[j ^ change]).trace().real for j in range(2))
            num_plus *= ts[0]+ts[1]
            num_minus *= ts[0]-ts[1]
            den_plus *= zs[0]+zs[1]
            den_minus *= zs[0]-zs[1]
        return _bounds((num_plus+num_minus)/(den_plus+den_minus))


def report():
    model = repetition_model(128)
    observable = PauliReadout("X"*model.central_bits, "X"*model.central_bits, "I"*model.n, "I"*model.n)
    start = time.perf_counter()
    result = estimate(model, observable, 4096, 2026102031)
    elapsed = time.perf_counter()-start
    reference = repetition_reference(model)
    return {
        "id": "COHERENT-GIBBS-PAULI-READOUT",
        "status": "scoped_classical_falsifier_written_proof_pending_independent_review",
        "question": "Does canonical-TFD Pauli coherence rescue conditional-product HDQI blocks?",
        "answer": "No, when the explicit central pin sampler meets its error bound.",
        "model": {
            "central_bits": model.central_bits, "quantum_blocks": model.n,
            "columns_decimal": list(model.columns),
            "a": "1", "b": "1/3", "h": "1/2", "e": "1/5", "beta": "1/8",
            "kernel": "binary repetition code; exact nullity one",
            "tfd_qubits": 2*(model.central_bits+model.n),
            "calibration_not_hardness_evidence": True,
        },
        "observable": "X on every central bit in both copies; I on every local spin",
        "estimator": "2 Re[phase(z) Tr(F_z^dagger A F_(z xor v) B^T)]/(w_z+w_(z xor v))",
        "absolute_sample_bound": 1,
        "native": result,
        "independent_even_parity_reference": {"lower": str(reference[0]), "upper": str(reference[1])},
        "classical_seconds_including_tables_and_kernel_certificate": elapsed,
        "exclusions": [
            "interacting local-spin blocks or general Hamiltonians",
            "arbitrary coherent measurements or full post-Clifford output sampling",
            "hardness or novelty of this deliberately easy calibration",
            "free code-distance certificates, source access, or partition sums",
            "a quantum speedup or a compiled quantum algorithm",
        ],
        "prior_art": ["https://arxiv.org/abs/0911.1624", "https://arxiv.org/abs/1310.6749"],
        "next_gate": "A useful task outside efficiently contractible Pauli readout, with a paid quantum source.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"report": str(args.output), "status": result["status"],
                      "mean": float(Q(result["native"]["mean_lower"])),
                      "reference": float(Q(result["independent_even_parity_reference"]["lower"])),
                      "seconds": result["classical_seconds_including_tables_and_kernel_certificate"]}, indent=2))


if __name__ == "__main__":
    main()
