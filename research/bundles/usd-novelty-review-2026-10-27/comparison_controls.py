"""Small independent controls for the ordinary-DQI comparator, not a circuit."""

import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent


def repetition_control(p, m, t):
    words = np.array(list(itertools.product(range(p), repeat=m)), dtype=int)
    weights = np.count_nonzero(words, axis=1)
    f = (math.sqrt((p - 1) / p) ** (m - weights)) * (
        -1 / math.sqrt(p * (p - 1))
    ) ** weights
    f[weights > t] = 0
    tau = float(np.dot(f, f))
    f /= math.sqrt(tau)
    shape = (p,) * m
    f = f.reshape(shape)
    full_support = np.all(words != 0, axis=1)
    omega = np.exp(2j * np.pi / p)
    outcomes = []
    for s in range(p):
        state = sum(
            omega ** (-c * s) * np.roll(f, (c,) * m, axis=tuple(range(m)))
            for c in range(p)
        ) / math.sqrt(p)
        # Positive-sign Fourier transform, so the target is sum(z_i) = s.
        out = np.fft.ifftn(state, norm="ortho").reshape(-1)
        probabilities = abs(out) ** 2
        syndrome = words.sum(axis=1) % p == s
        lam = p * np.count_nonzero(full_support & syndrome) / (p - 1) ** m
        measured = float(probabilities[full_support & syndrome].sum())
        assert abs(float(np.linalg.norm(state)) - 1) < 1e-12
        assert float(probabilities[~syndrome].sum()) < 1e-24
        assert abs(measured - lam * tau) < 1e-12
        outcomes.append({"s": s, "lambda": lam, "measured": measured,
                         "predicted_lambda_tau": lam * tau})
    return {"p": p, "m": m, "t": t, "tau": tau, "outcomes": outcomes}


def ag_bounds(e, p=1019):
    m, k, w, delta = 22 * e, 5 * e + 3, 15 * e + 6, 12 * e - 3
    t = (delta - 1) // 2
    ecp_t = 2 * e - 7
    assert k > ecp_t >= 0
    assert m - 2 * (10 * e + 3) > ecp_t
    assert 2 * delta > m
    # Exact rational union bounds are converted only when displaying logarithms.
    E_num, E_den = (p ** k - 1) * p ** w, (p - 1) ** m
    a_num, a_den = p ** k - 1, (p - 1) ** delta
    tail_num, tail_den = math.comb(m, t + 1), p ** (t + 1)
    ecp_tail_num = math.comb(m, ecp_t + 1)
    ecp_tail_den = p ** (ecp_t + 1)
    return {"e": e, "m": m, "k": k, "square_dimension": w,
            "designed_distance": delta, "geometry_supplied_t": t,
            "B_only_ECP_t": ecp_t,
            "log10_USD_E_bound": math.log10(E_num) - math.log10(E_den),
            "log10_normalization_alpha_bound": math.log10(a_num) - math.log10(a_den),
            "log10_geometry_supplied_tail_bound": math.log10(tail_num) - math.log10(tail_den),
            "log10_B_only_ECP_tail_bound": math.log10(ecp_tail_num) - math.log10(ecp_tail_den)}


def main():
    manifest = json.loads((ROOT / "source_manifest.json").read_text())
    for name, record in manifest.items():
        assert hashlib.sha256((ROOT / "sources" / name).read_bytes()).hexdigest() == record["sha256"]
    result = {"source_hashes_verified": len(manifest),
              "scope": "Tiny ideal-state controls and exact rational bounds; no AG decoder or quantum circuit implemented.",
              "controls": [repetition_control(3, 3, 1),
                           repetition_control(5, 3, 1),
                           repetition_control(3, 5, 2)],
              "AG_comparisons": [ag_bounds(e) for e in (8, 128, 256, 512)]}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
