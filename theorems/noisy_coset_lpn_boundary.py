"""Exact noisy-coset access reduction and scoped purification cost controls.

The binary LPN connection is prior art, not a new decoder. Dense controls
are bounded diagnostics; the reduction and rank-cost bounds are symbolic.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from flint import fmpz
import numpy as np


def _prime(p):
    if type(p) is not int or p < 2 or not fmpz(p).is_prime():
        raise ValueError("a prime integer is required")


def _probability(value):
    if not isinstance(value, Fraction) or not 0 <= value <= 1:
        raise ValueError("an exact probability Fraction is required")


def _vector(p, values):
    values = tuple(values)
    if not values or any(type(x) is not int or not 0 <= x < p for x in values):
        raise ValueError("a nonempty canonical field vector is required")
    return values


def error_mass(p, visibility, error):
    """v*delta_0 + (1-v)*Uniform(F_p), not a Gaussian error law."""
    _prime(p)
    _probability(visibility)
    if type(error) is not int or not 0 <= error < p:
        raise ValueError("error must be a canonical field element")
    return (1-visibility)/p + (visibility if error == 0 else 0)


def sample_to_fourier_label(p, a, b):
    """Only the observed sample is used; no secret/noise flag is an input."""
    _prime(p)
    a = _vector(p, a)
    if type(b) is not int or not 0 <= b < p:
        raise ValueError("sample label must be canonical")
    return a + (b,)


def secret_from_line(p, generator):
    """Decode any nonzero multiple of (s,-1), not only that generator."""
    _prime(p)
    generator = _vector(p, generator)
    if len(generator) < 2 or generator[-1] == 0:
        raise ValueError("the line must have a nonzero last coordinate")
    factor = -pow(generator[-1], -1, p)
    return tuple(factor*x % p for x in generator[:-1])


@dataclass(frozen=True)
class CosetNoiseContract:
    prime: int
    secret_dimension: int
    visibility: Fraction

    def __post_init__(self):
        _prime(self.prime)
        if type(self.secret_dimension) is not int or self.secret_dimension < 1:
            raise ValueError("secret dimension must be positive")
        _probability(self.visibility)

    @property
    def dimension(self):
        return self.prime**(self.secret_dimension+1)

    @property
    def clean_rank(self):
        return self.prime**self.secret_dimension

    @property
    def error_probability(self):
        return (1-self.visibility)*(1-Fraction(1, self.prime))

    def spectrum(self):
        return FlatSpectrum(self.clean_rank, self.dimension, self.error_probability)


@dataclass(frozen=True)
class FlatSpectrum:
    """Flat top rank r and flat complement; e is distance to the top projector."""
    rank: int
    dimension: int
    error: Fraction

    def __post_init__(self):
        if (type(self.rank) is not int or type(self.dimension) is not int
                or not 1 <= self.rank < self.dimension):
            raise ValueError("integer ranks must satisfy 1 <= r < N")
        _probability(self.error)
        if self.error > Fraction(self.dimension-self.rank, self.dimension):
            raise ValueError("the designated block is not a top eigenspace")

    @property
    def top_eigenvalue(self):
        return (1-self.error)/self.rank

    @property
    def bottom_eigenvalue(self):
        return self.error/(self.dimension-self.rank)

    def symmetric_step(self):
        a, b = self.top_eigenvalue, self.bottom_eigenvalue
        purity = self.rank*a*a + (self.dimension-self.rank)*b*b
        success = (1+purity)/2
        next_error = self.error*(1+b)/(1+purity)
        return FlatSpectrum(self.rank, self.dimension, next_error), success

    def necessary_levels(self, target_error):
        """Rational lower bound, not a sufficient schedule or general no-go.

        Odds shrink by at most 1+1/r per symmetric level. From log(1+1/r)
        <= 1/r and log(R) >= 1-1/R, K >= r*(1-1/R).
        """
        _probability(target_error)
        if target_error >= self.error:
            return 0
        if target_error == 0 or self.top_eigenvalue == self.bottom_eigenvalue:
            raise ValueError("no finite symmetric schedule reaches that target")
        ratio = (self.error/(1-self.error)) / (target_error/(1-target_error))
        bound = self.rank*(1-1/ratio)
        return -(-bound.numerator//bound.denominator)

    def equal_label_collision(self, copies):
        """Known Fourier-basis collision filter, paying all rejected inputs.

        Accept iff k measured IID labels are identical; recreate that label's
        Fourier state. This physically realizes rho**k/Tr(rho**k) here ONLY.
        """
        if type(copies) is not int or not 1 <= copies <= 128:
            raise ValueError("diagnostic collision block size must be in 1..128")
        a, b = self.top_eigenvalue, self.bottom_eigenvalue
        top = self.rank*a**copies
        bottom = (self.dimension-self.rank)*b**copies
        success = top+bottom
        return {
            "copies_per_attempt": copies,
            "success_probability": success,
            "output_error": bottom/success,
            "expected_raw_copies": copies/success,
        }


def _dense_points(p, dimension):
    if p**dimension > 125:
        raise ValueError("dense diagnostic cap is 125 group elements")
    return tuple(product(range(p), repeat=dimension))


def _fourier(p, points):
    coordinates = np.asarray(points, dtype=np.int64)
    phases = coordinates @ coordinates.T % p
    return np.exp(2j*np.pi*phases/p)/np.sqrt(len(points))


def _coset_density(p, generator, points):
    """Independent regular-translation sum, not the asserted Fourier law."""
    index = {x: i for i, x in enumerate(points)}
    density = np.zeros((len(points), len(points)), dtype=complex)
    for column, x in enumerate(points):
        for t in range(p):
            row = index[tuple((a-t*b) % p for a, b in zip(x, generator))]
            density[row, column] += 1/len(points)
    return density


def dense_reduction_control(p, secret, visibility):
    """Secret used only to construct independent reference fixtures."""
    _prime(p)
    secret = _vector(p, secret)
    contract = CosetNoiseContract(p, len(secret), visibility)
    points = _dense_points(p, len(secret)+1)
    n = len(points)
    index = {x: i for i, x in enumerate(points)}
    probabilities = [Fraction(0) for _ in points]
    # Enumerate the specified ordinary noisy-linear sample law independently.
    for a in product(range(p), repeat=len(secret)):
        inner = sum(x*y for x, y in zip(a, secret)) % p
        for error in range(p):
            y = sample_to_fourier_label(p, a, (inner+error) % p)
            probabilities[index[y]] += error_mass(p, visibility, error)/p**len(secret)
    assert sum(probabilities) == 1
    fourier = _fourier(p, points)
    diagonal = np.diag([float(x) for x in probabilities])
    from_samples = fourier.conj().T @ diagonal @ fourier
    generator = secret+(p-1,)
    clean = _coset_density(p, generator, points)
    reference = float(visibility)*clean + float(1-visibility)*np.eye(n)/n
    recovered = fourier @ reference @ fourier.conj().T
    other_secret = ((secret[0]+1) % p,)+secret[1:]
    other = _coset_density(p, other_secret+(p-1,), points)
    other = float(visibility)*other+float(1-visibility)*np.eye(n)/n
    distance = np.linalg.eigvalsh(reference-clean)
    all_decoded = all(
        secret_from_line(p, tuple(t*x % p for x in generator)) == secret
        for t in range(1, p)
    )
    return {
        "prime": p, "secret_dimension": len(secret), "group_order": n,
        "visibility": str(visibility),
        "nonzero_error_probability": str(contract.error_probability),
        "density_identity_max_error": float(np.max(np.abs(from_samples-reference))),
        "fourier_diagonal_max_error": float(np.max(np.abs(recovered-diagonal))),
        "pairwise_commutator_max_error": float(np.max(np.abs(reference@other-other@reference))),
        "trace_distance_error": abs(float(np.sum(np.abs(distance))/2)-float(contract.error_probability)),
        "every_nonzero_line_generator_decoded": all_decoded,
        "actual_top_multiplicity": int(np.count_nonzero(np.isclose(
            np.linalg.eigvalsh(reference), float(contract.spectrum().top_eigenvalue),
            atol=1e-12, rtol=0))),
        "clean_rank": contract.clean_rank,
    }


def coherent_example_countercontrol():
    """Same classical labels do not imply the same quantum input state."""
    p, secret, tau = 2, (1, 1), Fraction(1, 8)
    points = _dense_points(p, 3)
    index = {x: i for i, x in enumerate(points)}
    coherent = np.zeros((8, 8), dtype=complex)
    for error, weight in ((0, 1-tau), (1, tau)):
        vector = np.zeros(8, dtype=complex)
        for a in product(range(2), repeat=2):
            b = (sum(x*y for x, y in zip(a, secret))+error) % 2
            vector[index[a+(b,)]] = 1/2
        coherent += float(weight)*np.outer(vector, vector.conj())
    classical = np.diag(np.diag(coherent))
    fourier = _fourier(2, points)
    coherent_readout = np.real(np.diag(fourier@coherent@fourier.conj().T))
    classical_readout = np.real(np.diag(fourier@classical@fourier.conj().T))
    location = index[secret+(1,)]
    return {
        "same_classical_sample_diagonal": bool(np.allclose(np.diag(coherent), np.diag(classical))),
        "coherent_secret_and_label_one_probability": float(coherent_readout[location]),
        "dephased_secret_and_label_one_probability": float(classical_readout[location]),
        "dephased_fourier_uniform_max_error": float(np.max(np.abs(classical_readout-1/8))),
        "coherent_error_model": "one common label flip per coherent example; not local hardware noise",
    }


def build_report():
    controls = [dense_reduction_control(p, s, Fraction(3, 4)) for p, s in (
        (2, (1, 0, 1)), (3, (1, 2)), (5, (2, 4)),
    )]
    costs = []
    for p, dimension in ((2, 8), (2, 32), (2, 64), (3, 32)):
        contract = CosetNoiseContract(p, dimension, Fraction(3, 4))
        spectrum = contract.spectrum()
        levels = spectrum.necessary_levels(Fraction(1, 16))
        collision = spectrum.equal_label_collision(2)
        costs.append({
            "prime": p, "secret_dimension": dimension, "clean_rank": contract.clean_rank,
            "initial_trace_error": str(spectrum.error), "target_trace_error": "1/16",
            "symmetric_levels_lower_bound": levels,
            "log2_raw_copies_lower_bound_for_symmetric_tree": levels,
            "two_label_collision": {key: str(value) if isinstance(value, Fraction) else value
                                    for key, value in collision.items()},
        })
    return {
        "status": "ACCESS_REDUCTION_AND_SCOPED_PURIFICATION_LOWER_BOUND_UNDER_REVIEW",
        "binary_lpn_equivalence_is_known": True,
        "dense_controls": controls,
        "coherent_example_countercontrol": coherent_example_countercontrol(),
        "symbolic_rank_costs": costs,
        "classical_sample_simulation": True,
        "classical_polynomial_decoder_implied": False,
        "quantum_polynomial_decoder_implemented": False,
        "gaussian_lwe_reduction_established": False,
        "all_purification_protocols_ruled_out": False,
        "noiseless_rees_claim_refuted": False,
        "independent_review": False,
        "novelty_established": False,
        "speedup_claim_allowed": False,
        "sources": ["https://arxiv.org/pdf/1910.00802",
                    "https://arxiv.org/pdf/1407.5088",
                    "https://arxiv.org/abs/2503.22644"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    content = json.dumps(report, indent=2)+"\n"
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/noisy_coset_lpn_boundary.json"
        path.write_text(content)
        print(path)
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
