"""Exact source-contract falsifier, not a quantum algorithm or hardness test.

For the existing adjacent-phase control, target basis bits give an exact
frequency distribution. Cyclic convolution computes the physical address
state's Fourier eigenvalues without substituting a claimed gap bound.
"""

from fractions import Fraction
from itertools import product


def packet_frequencies(p=257, scales=(1, 256, 16, 241)):
    if p != 257 or tuple(scales) != (1, 256, 16, 241):
        raise ValueError("this is the fixed p=257 source-contract control")
    counts = [0] * p
    for bits in product((0, 1), repeat=len(scales)):
        counts[sum(s * b for s, b in zip(scales, bits)) % p] += 1
    return tuple(counts)


def convolution(left, right):
    if len(left) != len(right):
        raise ValueError("cyclic distributions must have the same length")
    out = [0] * len(left)
    for x, a in enumerate(left):
        if a:
            for y, b in enumerate(right):
                if b:
                    out[(x + y) % len(out)] += a * b
    return tuple(out)


def scale_average(counts):
    """Count all (public scale, target basis string) pairs exactly."""
    p = len(counts)
    out = [0] * p
    for scale in range(p):
        for frequency, count in enumerate(counts):
            out[scale * frequency % p] += count
    return tuple(out)


def distance_from_uniform(counts):
    total = sum(counts)
    if total <= 0 or any(x < 0 for x in counts):
        raise ValueError("nonnegative, nonempty frequency mass is required")
    p = len(counts)
    return sum(abs(Fraction(x, total) - Fraction(1, p)) for x in counts) / 2


def audit(max_packets=8):
    if not isinstance(max_packets, int) or isinstance(max_packets, bool) or not 1 <= max_packets <= 12:
        raise ValueError("bounded exact control: 1 to 12 packets")
    p = 257
    packet = packet_frequencies()
    fresh_packet = scale_average(packet)
    unscaled, independent = (1,) + (0,) * (p - 1), (1,) + (0,) * (p - 1)
    rows = []
    for k in range(1, max_packets + 1):
        unscaled = convolution(unscaled, packet)
        independent = convolution(independent, fresh_packet)
        shared = scale_average(unscaled)
        a_k = Fraction(unscaled[0], sum(unscaled))
        independent_distance = distance_from_uniform(independent)
        shared_distance = distance_from_uniform(shared)
        assert independent_distance == Fraction(p - 1, p) * Fraction(1, 4**k)
        assert shared_distance == Fraction(p - 1, p) * a_k
        assert a_k >= Fraction(1, p)
        rows.append({
            "packets": k,
            "independent_scale_trace_distance": str(independent_distance),
            "shared_scale_trace_distance": str(shared_distance),
            "shared_scale_zero_frequency_probability": str(a_k),
        })
    return {
        "scope": "exact finite source-contract falsifier; easy abelian control",
        "p": p,
        "scales": [1, 256, 16, 241],
        "shared_scale_trace_distance_floor": str(Fraction(p - 1, p * p)),
        "single_packet_marginals_agree": rows[0]["independent_scale_trace_distance"] == rows[0]["shared_scale_trace_distance"],
        "rows": rows,
        "quantum_execution": False,
        "speedup_established": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(audit(), indent=2))
