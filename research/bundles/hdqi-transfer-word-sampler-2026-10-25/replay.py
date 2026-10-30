"""Generate/check exact full-output transfer-sampling research artifacts."""

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random
import sys

from word_sampler import WordSampler, repeated_transfer_bound


ROOT = Path(__file__).resolve().parent


def build():
    names = ("word_sampler.py", "test_word_sampler.py", "replay.py", "TRANSFER_WORD_SAMPLER.md")
    result = {"schema": "native-transfer-word-v1",
              "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in names},
              "quantum_advantage_claim": False, "general_polynomial_thermal_sampler": False,
              "rational_compression_compiler_implemented": False, "cases": []}
    for m, radius, beta, factors, basis in [(5, 2, Q(1, 5), 2, "Z"),
        (16, 3, Q(1, 4), 2, "Z"), (16, 3, Q(1, 4), 2, "X"),
        (32, 7, Q(1, 8), 2, "Z"), (64, 7, Q(1, 8), 2, "Z")]:
        print(f"exact sampler m={m} R={radius} L={factors} basis={basis}", flush=True)
        couplings = [Q((-1)**i) for i in range(m)]
        bound = repeated_transfer_bound(couplings, beta, factors)
        sampler = WordSampler(couplings, radius, [bound["transfer_parameter"]]*factors, basis=basis)
        rng = random.Random(1025+m)
        samples = [sampler.sample(rng) for _ in range(4)]
        result["cases"].append({"m": m, "radius": radius, "couplings": couplings,
            "beta": beta, "factors": factors, "basis": basis,
            "bond_dimension": sampler.bond_dimension, "raw_norm_squared": sampler.norm_squared,
            "raw_norm_has_unnormalized_walsh_factor": basis == "X", **bound,
            "samples": samples, "sample_probabilities": [sampler.probability(s) for s in samples],
            "sampling_arithmetic": "exact rational", "target": "finite transfer-product pilot"})
    sign = WordSampler([1]*3, 1, [Q(1, 3), Q(2, 5)])
    result["sign_control"] = {"full_path_coefficient": sign.amplitude((1, 1, 1)),
                              "unsigned_wrong_coefficient": Q(-1, 3)**2*Q(-2, 5)+Q(-2, 5)**2*Q(-1, 3)}
    return json.loads(json.dumps(result, default=str))


def main():
    if sys.argv[1:] not in (["write"], ["check"]):
        raise SystemExit("usage: replay.py write|check")
    result = build()
    destination = ROOT/"receipt.json"
    if sys.argv[1] == "write":
        destination.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    elif result != json.loads(destination.read_text()):
        raise SystemExit("receipt differs")
    print(sys.argv[1], "PASS; receipt sha256", hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
