"""Controls for an address-local sketch of the original noisy-linear records.

No copy-only receiver, coherent source oracle, or efficient solver is supplied.
Exact ledgers are separate from explicitly capped floating-point diagnostics.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import ceil


def positive_int(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"positive integer {name} required")
    return value


def root_digits(q):
    positive_int(q, "modulus")
    x, r = q, 0
    while x > 1 and x % 3 == 0:
        x //= 3
        r += 1
    if x != 1 or r == 0:
        raise ValueError("native modulus must be 3^r with r >= 1")
    return r


def canonical(vector, q, n=None):
    vector = tuple(vector)
    if not vector or (n is not None and len(vector) != n) or any(
            type(x) is not int or not 0 <= x < q for x in vector):
        raise ValueError("nonempty canonical vector of the specified dimension required")
    return vector


@dataclass(frozen=True)
class NativeRecord:
    label: tuple[int, ...]
    value: int
    modulus: int
    source_id: str

    def __post_init__(self):
        root_digits(self.modulus)
        object.__setattr__(self, "label", canonical(self.label, self.modulus))
        if type(self.value) is not int or not 0 <= self.value < self.modulus:
            raise ValueError("canonical observed value required")
        if not isinstance(self.source_id, str) or not self.source_id:
            raise ValueError("nonempty original source identifier required")


def checked_bank(records):
    records = tuple(records)
    if not records or any(not isinstance(z, NativeRecord) for z in records):
        raise ValueError("nonempty original noisy-linear record bank required")
    q, n = records[0].modulus, len(records[0].label)
    if any(z.modulus != q or len(z.label) != n for z in records):
        raise ValueError("shared modulus and dimension required")
    if len({z.source_id for z in records}) != len(records):
        raise ValueError("duplicate original identifiers; replay must be explicit")
    return records, q, n


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def support_bound(q, n, visited):
    root_digits(q)
    positive_int(n, "dimension")
    D = q**n
    if type(visited) is not int or not 0 <= visited <= D:
        raise ValueError("distinct visited count must lie between zero and q^n")
    return {"domain_size": D, "visited": visited,
            "herald_probability_upper": Fraction(visited, D),
            "correct_and_herald_probability_upper": Fraction(visited**2, D**2),
            "conditional_fixed_answer_probability_upper": Fraction(visited, D),
            "conditional_bound_requires_nonzero_herald": True,
            "scope": "uniform initial address; address-local updates; branch-1 Fourier readout",
            "arbitrary_native_algorithms_ruled_out": False}


def resource_ledger(q, n, visibility, queries=1, error=Fraction(1, 10), failure_bits=32):
    r = root_digits(q)
    positive_int(n, "dimension")
    positive_int(queries, "fresh-block ideal query count")
    positive_int(failure_bits, "classical failure exponent")
    if not isinstance(visibility, (int, Fraction)) or type(visibility) is bool:
        raise ValueError("exact rational visibility required, not a floating estimate")
    if not isinstance(error, (int, Fraction)) or type(error) is bool:
        raise ValueError("exact rational simulation error required")
    kappa, error = Fraction(visibility), Fraction(error)
    if not 0 < kappa <= 1 or not 0 < error < 1:
        raise ValueError("positive subunit visibility and strictly subunit error required")
    D = q**n
    # pi^2 < 10; the error convention is HALF diamond distance.
    per_query = ceil(Fraction(5, 2)*(D+kappa*kappa)*queries/(kappa*kappa*error))
    # ln(2*3^(rn)*2^failure_bits) < 1 + 2*r*n + failure_bits.
    classical = ceil(32*(1+2*r*n+failure_bits)/(kappa*kappa))
    return {"dimension": n, "modulus": q, "ternary_root_digits": r,
            "domain_size": D, "visibility": kappa,
            "visibility_is_supplied_law_not_sample_estimate": True,
            "queries": queries, "total_half_diamond_error_budget": error,
            "fresh_originals_per_query_sufficient": per_query,
            "fresh_originals_total_sufficient": queries*per_query,
            "per_gate_error_budget_for_equal_additional_error": error/(queries*per_query),
            "classical_originals_sufficient": classical,
            "classical_failure_probability_upper": Fraction(1, 2**failure_bits),
            "classical_hypotheses_enumerated": D,
            "classical_score_terms_evaluated": D*classical,
            "classical_cosine_absolute_error_budget": kappa/8,
            "classical_storage": "M records plus counters; polynomial in n*log(q), 1/kappa, failure_bits",
            "query_cost_is_polylog_domain": False,
            "fresh_independence_is_source_promise": True,
            "known_values_available_to_copy_only_receiver": False,
            "gate_synthesis_executed": False, "accepted_speedup_candidate": False}


def quarter_turn_sketch(records, repetitions=1):
    """Secret-blind exact branch/exponent evolution; repeated banks stay frozen."""
    records, q, n = checked_bank(records)
    positive_int(repetitions, "frozen-bank repetitions")
    state = {}
    for _ in range(repetitions):
        for z in records:
            branch, exponent = state.get(z.label, (0, 0))
            exponent += q + (4*z.value if branch == 0 else -4*z.value)
            state[z.label] = (1-branch, exponent % (4*q))
    return {"q": q, "n": n, "state": state,
            "distinct_originals": len(records), "gate_updates": len(records)*repetitions,
            "repetitions_are_fresh_samples": False}


def exact_quarter_turn_probability(records, outcome, repetitions=1):
    """Probability of a supplied Fourier outcome AND branch 1, in Q(zeta_4q).

    The outcome is a diagnostic label, never an input to the sketch processor.
    Cyclotomic arithmetic is a small reference control, not a scalable solver.
    """
    from sympy import Poly, Symbol, cyclotomic_poly

    result = quarter_turn_sketch(records, repetitions)
    q, n, state = result["q"], result["n"], result["state"]
    if q > 81:
        raise ValueError("cyclotomic reference control capped at q <= 81")
    outcome = canonical(outcome, q, n)
    x = Symbol("x")
    polynomial = Poly(sum(x**((exponent-4*dot(a, outcome)) % (4*q))
                          for a, (branch, exponent) in state.items() if branch), x)
    conjugate = Poly(sum(coefficient*x**((-power[0]) % (4*q))
                         for power, coefficient in polynomial.terms()), x)
    reduced = (polynomial*conjugate).rem(Poly(cyclotomic_poly(4*q, x), x))
    return tuple(Fraction(int(reduced.nth(j)), q**(2*n))
                 for j in range(max(0, int(reduced.degree()) if not reduced.is_zero else 0)+1))


def ternary_correlation(records, max_domain=729):
    """Exact exhaustive q=3 baseline; no secret parameter or hardness claim."""
    records, q, n = checked_bank(records)
    positive_int(max_domain, "explicit enumeration cap")
    if q != 3 or q**n > max_domain:
        raise ValueError("exact ternary correlation diagnostic exceeds its declared scope")
    scores = {}
    for candidate in product(range(q), repeat=n):
        matches = sum((z.value-dot(z.label, candidate)) % q == 0 for z in records)
        scores[candidate] = Fraction(3*matches-len(records), 2*len(records))
    best = max(scores.values())
    return {"maximizers": tuple(s for s, score in scores.items() if score == best),
            "scores": scores, "hypotheses_enumerated": q**n,
            "secret_used_by_attack": False, "ties_are_not_recovery": True}


def finite_channel_control(q, n, secret, noise, samples):
    """Average the actual conjugation channels, never conjugation by E[U]."""
    import numpy as np

    root_digits(q)
    positive_int(n, "dimension")
    positive_int(samples, "fresh IID sample count")
    secret = canonical(secret, q, n)
    D = q**n
    if D > 9:
        raise ValueError("dense mean-channel diagnostic capped at q^n <= 9")
    if not noise or any(type(e) is not int or not 0 <= e < q or
                        not isinstance(p, Fraction) or p < 0 for e, p in noise.items()) or sum(noise.values()) != 1:
        raise ValueError("explicit normalized finite rational noise law required")
    character = lambda b: np.exp(2j*np.pi*(b % q)/q)
    phi = sum(float(p)*character(e) for e, p in noise.items())
    if abs(phi.imag) > 1e-12 or not 0 < phi.real <= 1+1e-12:
        raise ValueError("positive real visibility required")
    kappa = min(1.0, float(phi.real))
    theta = np.pi*D/(2*kappa*samples)
    identity = np.eye(2*D, dtype=complex)
    channel = np.zeros(((2*D)**2, (2*D)**2), complex)
    mean_unitary = np.zeros_like(identity)
    mean_hamiltonian = np.zeros_like(identity)
    ideal = np.zeros_like(identity)
    labels = tuple(product(range(q), repeat=n))
    for j, a in enumerate(labels):
        phase = character(dot(a, secret))
        ideal[2*j:2*j+2, 2*j:2*j+2] = [[0, phase.conjugate()], [phase, 0]]
        for e, probability in noise.items():
            phase = character(dot(a, secret)+e)
            h = np.array([[0, phase.conjugate()], [phase, 0]])
            U = identity.copy()
            U[2*j:2*j+2, 2*j:2*j+2] = np.cos(theta)*np.eye(2)+1j*np.sin(theta)*h
            weight = float(probability)/D
            channel += weight*np.kron(U.conj(), U)
            mean_unitary += weight*U
            mean_hamiltonian[2*j:2*j+2, 2*j:2*j+2] += weight*h
    initial = np.zeros(2*D, complex)
    initial[::2] = 1/np.sqrt(D)
    target = ideal@initial
    rho = np.outer(initial, initial.conj())
    evolved = (np.linalg.matrix_power(channel, samples)@rho.reshape(-1, order="F")).reshape(rho.shape, order="F")
    distance = np.linalg.eigvalsh(evolved-np.outer(target, target.conj()))
    expected_step = (1+(np.cos(theta)-1)/D)*identity+1j*kappa*np.sin(theta)/D*ideal
    return {"q": q, "n": n, "samples": samples, "visibility": kappa,
            "trace_distance_to_ideal": float(np.abs(distance).sum()/2),
            "correct_and_herald_probability": float(np.vdot(target, evolved@target).real),
            "half_diamond_proved_upper": min(1.0, np.pi**2*(D+kappa*kappa)/(4*kappa*kappa*samples)),
            "trace": float(np.trace(evolved).real),
            "minimum_eigenvalue": float(np.linalg.eigvalsh(evolved).min()),
            "mean_hamiltonian_identity_residual": float(np.max(np.abs(mean_hamiltonian-kappa/D*ideal))),
            "mean_step_identity_residual": float(np.max(np.abs(mean_unitary-expected_step))),
            "channel_vs_mean_unitary_conjugation_gap": float(np.linalg.norm(channel-np.kron(mean_unitary.conj(), mean_unitary))),
            "status": "FLOATING_POINT_CHANNEL_CONTROL_NOT_PROOF_OR_QUANTUM_EXECUTION"}
