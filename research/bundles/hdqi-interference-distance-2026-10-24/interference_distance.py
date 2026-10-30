"""Classical left-output sampler certified by a relative Pauli-code distance.

This tests the actual fixed measurement basis. It never rotates the input to
make a test pass. Distance enumeration is bounded and may return UNKNOWN.
"""

from fractions import Fraction as F
from itertools import combinations
import math
from pathlib import Path
import random
import sys

import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hdqi-output-sampling-2026-10-24"))
import output_sampling as o  # noqa: E402


def low_weight_check(model, t, max_vectors=1000000):
    m = model.pilot.m
    if type(t) is not int or not 0 <= t <= m:
        raise ValueError("integer 0<=t<=m required")
    if type(max_vectors) is not int or max_vectors < 0:
        raise ValueError("nonnegative integer enumeration budget required")
    radius = min(2*t, m)
    required = sum(math.comb(m, j) for j in range(1, radius+1))
    if required > max_vectors:
        return {"status": "UNKNOWN_BUDGET", "t": t, "radius": radius,
                "required_vectors": required, "checked_vectors": 0,
                "no_short_relative_word": False, "witness": None}
    checked = 0
    for size in range(1, radius+1):
        for indices in combinations(range(m), size):
            x = z = mask = 0
            for i in indices:
                xi, zi, _ = model.paulis[i]
                x, z, mask = x ^ xi, z ^ zi, mask | (1 << i)
            checked += 1
            if x == 0 and z != 0:
                return {"status": "SHORT_DIAGONAL_WORD", "t": t, "radius": radius,
                        "required_vectors": required, "checked_vectors": checked,
                        "no_short_relative_word": False,
                        "witness": {"mask": mask, "weight": size, "X": x, "Z": z}}
    return {"status": "CERTIFIED", "t": t, "radius": radius,
            "required_vectors": required, "checked_vectors": checked,
            "no_short_relative_word": True, "witness": None}


def factorial_tail(model, t):
    """Exact inclusion-moment upper bound, not an independence assumption."""
    m = model.pilot.m
    if type(t) is not int or not 0 <= t <= m:
        raise ValueError("integer 0<=t<=m required")
    if t == m:
        return {"tail_upper": F(0), "moment_order": 0, "threshold": m+1}
    threshold = t+1
    elementary = [F(1)]+[F(0)]*threshold
    for x in model.pilot.x:
        rho = min(F(1), x*x)
        for j in range(threshold, 0, -1):
            elementary[j] += rho*elementary[j-1]
    choices = [(F(1), 0)] + [(elementary[j]/math.comb(threshold, j), j)
                             for j in range(1, threshold+1)]
    bound, order = min(choices)
    return {"tail_upper": bound, "moment_order": order, "threshold": threshold}


def certify(model, t, epsilon=F(1, 100), max_vectors=1000000):
    epsilon = o.s.rational(epsilon)
    if not 0 < epsilon < 1:
        raise ValueError("epsilon must be in (0,1)")
    distance = low_weight_check(model, t, max_vectors)
    tail = factorial_tail(model, t)
    valid = distance["no_short_relative_word"] and tail["tail_upper"] <= epsilon*epsilon
    return {"status": "CERTIFIED_UNIFORM_LEFT_OUTPUT" if valid else "NO_CERTIFICATE",
            "epsilon": str(epsilon), "distance_check": distance,
            "tail_upper": str(tail["tail_upper"]), "moment_order": tail["moment_order"],
            "TV_squared_upper": str(tail["tail_upper"]) if distance["no_short_relative_word"] else None,
            "measurement": "physical_left_computational_basis_only",
            "arbitrary_total_deterministic_decoder": True,
            "decoder_evaluations_required": 0, "pilot_samples_required": 0,
            "polynomial_sign_ratio_required": False,
            "fiber_ranks": o.pure_z_basis(model),
            "quantum_advantage_claimed": False, "hardness_from_refusal": False}


class UniformSampler:
    def __init__(self, model, t, epsilon=F(1, 100), max_vectors=1000000):
        self.plan = certify(model, t, epsilon, max_vectors)
        if self.plan["status"] != "CERTIFIED_UNIFORM_LEFT_OUTPUT":
            raise ValueError("no certified sampler at the requested error")
        self.n = model.n

    def sample(self, rng):
        return rng.getrandbits(self.n)


def matrix(pauli, n):
    x, z, phase = pauli
    out = np.zeros((1 << n, 1 << n), dtype=complex)
    for b in range(1 << n):
        out[b ^ x, b] = 1j**phase * (-1)**((z & b).bit_count())
    return out


def dense_pilot(model):
    if model.pilot.m > 8 or model.n > 3:
        raise ValueError("dense reference requires m<=8,n<=3")
    m = model.pilot.m
    h = sum(float(j)*matrix((1 << i, model.pilot.lower_masks[i], 0), m)
            for i, j in enumerate(model.pilot.couplings))
    psi = expm(-float(model.pilot.beta)*h/2)[:, 0]
    return psi/np.linalg.norm(psi)


def dense_joint(model, decoder, psi):
    if model.pilot.m > 8 or model.n > 3:
        raise ValueError("dense reference requires m<=8,n<=3")
    psi = np.asarray(psi, dtype=complex)
    if psi.shape != (1 << model.pilot.m,) or not np.isclose(np.vdot(psi, psi), 1):
        raise ValueError("normalized pilot vector of the correct length required")
    blocks = {}
    for y, amplitude in enumerate(psi):
        p = np.eye(1 << model.n, dtype=complex)
        for i, generator in enumerate(model.paulis):
            if y >> i & 1:
                p = p@matrix(generator, model.n)
        residue = y ^ o.decoder_value(model, decoder, model.label(y))
        blocks[residue] = blocks.get(residue, np.zeros_like(p))+amplitude*p/math.sqrt(1 << model.n)
    probabilities = {(r, a, b): float(abs(p[a, b])**2) for r, p in blocks.items()
                     for a in range(1 << model.n) for b in range(1 << model.n)}
    if abs(sum(probabilities.values())-1) > 1e-10:
        raise ArithmeticError("physical decoder isometry lost normalization")
    return probabilities


def left_marginal(joint, n):
    out = np.zeros(1 << n)
    for (_, a, _), probability in joint.items():
        out[a] += probability
    return out


def dense_control(model, decoder, t):
    check = low_weight_check(model, t)
    if not check["no_short_relative_word"]:
        raise ValueError("distance condition fails; not a positive control")
    psi = dense_pilot(model)
    good = np.array([y.bit_count() <= t for y in range(len(psi))])
    tail = float(np.sum(abs(psi[~good])**2))
    truncated = np.where(good, psi, 0)
    truncated /= np.linalg.norm(truncated)
    left = left_marginal(dense_joint(model, decoder, psi), model.n)
    truncated_left = left_marginal(dense_joint(model, decoder, truncated), model.n)
    uniform = np.full_like(left, 1/len(left))
    tv = float(np.sum(abs(left-uniform))/2)
    error = float(np.max(abs(truncated_left-uniform)))
    bound = factorial_tail(model, t)
    if error > 1e-10 or tv*tv > tail+1e-10 or tail > float(bound["tail_upper"])+1e-10:
        raise ArithmeticError("independent physical output bound failed")
    return {"n": model.n, "m": model.pilot.m, "t": t, "actual_tail": tail,
            "rational_tail_upper": str(bound["tail_upper"]), "actual_left_TV": tv,
            "truncated_uniform_max_error": error, "distance_check": check,
            "mode": "exponential_dense_physical_control"}


def nonlinear_fixture(beta=F(1, 4)):
    model = o.d.Physical.create(2, [(1, 0, 0), (2, 0, 0), (3, 3, 0), (1, 0, 0)], [1]*4, beta)
    section = {model.label(y): y for y in reversed(range(16))}

    def decoder(syndrome):
        y = section.get(syndrome, 0)
        return y ^ (9 if (syndrome & 1) and (syndrome & 2) else 0)

    return model, decoder


def scrambled_pairs(n=32, seed=241024):
    """Fixed public Clifford-equivalent control; NOT a uniform Clifford draw."""
    if type(n) is not int or not 2 <= n <= 128:
        raise ValueError("fixture requires integer 2<=n<=128")
    rng = random.Random(seed)
    vectors = [(1 << i, 0) for i in range(n)]+[(0, 1 << i) for i in range(n)]
    for _ in range(12*n):
        a, b = rng.getrandbits(n), rng.getrandbits(n)
        vectors = [(x ^ a, z ^ b) if ((x & b).bit_count()+(z & a).bit_count()) % 2 else (x, z)
                   for x, z in vectors]
    paulis = [(x, z, (x & z).bit_count() % 2) for x, z in vectors]
    model = o.d.Physical.create(n, paulis, [1]*(2*n), F(1, 32))
    expected = tuple((i, n+i) for i in range(n))
    if model.pilot.edges != expected:
        raise ArithmeticError("symplectic scrambling changed the matching graph")
    return model
