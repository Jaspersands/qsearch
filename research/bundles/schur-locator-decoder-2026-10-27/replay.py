"""Native matrix-only decoder replay; no quantum execution or sampler run."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys

from locator import SchurLocator, native_bounds

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "small-prime-tower-2026-10-27"))
from small_prime import build_control


def encode(value):
    if isinstance(value, Fraction):
        return {"numerator_hex": hex(value.numerator), "denominator_hex": hex(value.denominator)}
    raise TypeError(type(value).__name__)


def receipt():
    _, _, native = build_control()
    decoder = SchurLocator(1019, native["original_parity"])
    rng = random.Random(20261027)
    cases = []
    for weight in (0, 1, 8, 9):
        for repetition in range(5):
            message = [rng.randrange(1019) for _ in range(decoder.k)]
            word = decoder.encode(message)
            support = rng.sample(range(decoder.m), weight)
            values = [rng.randrange(1, 1019) for _ in support]
            received = word.copy()
            for i, v in zip(support, values):
                received[i] = (received[i]+v) % 1019
            result = decoder.decode(received, 9)
            if (result["word"] != word or result["message_in_original_basis"] != message
                    or any(result["locator"][i] for i in support)):
                raise ArithmeticError("native public-matrix decoder failed")
            cases.append({"weight": weight, "repetition": repetition,
                          "original_message": message, "error_positions": support,
                          "error_values": values, "verified_word": result["word"],
                          "locator": result["locator"]})
    files = ("locator.py", "test_locator.py", "replay.py", "RESULT.md")
    paths = [ROOT / x for x in files]
    paths += [ROOT.parent / x for x in (
        "small-prime-tower-2026-10-27/small_prime.py",
        "prime-ag-tower-source-2026-10-26/tower_seed.py",
        "schur-growth-classical-gate-2026-10-26/schur_gate.py",
        "systematic-full-support-2026-10-27/systematic.py",
        "ag-affine-sampling-2026-10-26/affine_sampling.py")]
    review = ROOT.parent / "usd-novelty-review-2026-10-27/REVIEW.md"
    if review.is_file():
        paths.append(review)
    return {"status": "MATRIX_ONLY_CLASSICAL_SPARSE_ERROR_DECODER_NOT_FULL_SUPPORT_SOLVER",
            "shape": [decoder.k, decoder.m], "square_rank": len(decoder.W),
            "original_generator_sha256": hashlib.sha256(json.dumps(native["original_parity"]).encode()).hexdigest(),
            "hashes": {str(p.relative_to(ROOT.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            "native_cases": cases,
            "analytic_bounds_not_generated_inputs": [native_bounds(e) for e in (8, 128, 256, 512)],
            "curve_geometry_given_to_decoder": False,
            "higher_input_generated": False,
            "quantum_sampler_implemented": False,
            "classical_full_support_search_or_sampling_solved": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = receipt()
    encoded = json.dumps(result, default=encode, sort_keys=True, indent=2) + "\n"
    path = ROOT / "receipt.json"
    if args.write:
        path.write_text(encoded)
    elif path.read_text() != encoded:
        raise SystemExit("receipt mismatch: inspect before refreshing")
    print(json.dumps({"status": "PASS", "native_decodes": len(result["native_cases"]),
                      "receipt_sha256": hashlib.sha256(encoded.encode()).hexdigest()}))
