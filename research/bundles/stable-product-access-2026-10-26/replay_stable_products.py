"""Replay exact lattice obstructions, not geometric computation or a speedup."""

import argparse
import hashlib
import json
from pathlib import Path

from stable_product_controls import check_local, stable_certificate

HERE = Path(__file__).resolve().parent


def receipt():
    files = ("STABLE_PRODUCTS.md", "stable_product_controls.py",
             "test_stable_product_controls.py", "replay_stable_products.py")
    return {
        "schema": "stable-product-access-obstructions-v1",
        "status": "supplied CM ideal-lattice falsifiers; no native source",
        "local_controls": [check_local(m) for m in (2, 3, 5, 23, 72, 529, 2**256*3**100*23**30)],
        "stable_product": stable_certificate(),
        "scope": {
            "paired_local_equivalence_for_every_modulus_proved_in_note": True,
            "global_integral_nonequivalence_proved_in_note": True,
            "native_finite_field_curves_executed": False,
            "oriented_supersingular_stable_classification_established": False,
            "all_classical_geometry_excluded": False,
            "compression_algorithm_implemented": False,
            "quantum_advantage_established": False,
            "independently_reviewed": False,
        },
        "hashes": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in files},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = receipt()
    path = HERE / "receipt.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    if args.check and json.loads(path.read_text()) != result:
        raise SystemExit("receipt mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
