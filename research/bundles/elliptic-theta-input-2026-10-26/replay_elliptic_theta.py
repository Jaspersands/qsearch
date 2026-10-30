"""Native genus-one conversion receipts, not a complete geometric oracle."""

import argparse
import hashlib
import json
from pathlib import Path

import flint
from flint import fq_default_ctx

from elliptic_theta import EllipticCurve, convert, key, point_key


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence():
    here = Path(__file__).resolve().parent
    root = here.parent
    records = []
    for p, a, b in ((7, 1, 0), (23, 1, 2), (31, 1, 0)):
        field = fq_default_ctx(p, 2, "z")
        model = convert(EllipticCurve(field, a, b))
        encoded = [model.encode(point) for point in model.torsion]
        distinct = len({tuple(key(x) for x in v) for v in encoded})
        if distinct != 64 or any(model.decode(v) != point for point, v in zip(model.torsion, encoded)):
            raise ValueError("signed conversion failed")
        records.append({"characteristic": p, "field_degree": 2, "field_modulus": str(field.modulus()),
                        "a": a, "b": b, "resources": model.resources,
                        "theta_null": [key(x) for x in model.encode(None)],
                        "coordinates": [[key(x) for x in row] for row in model.coordinates],
                        "translation_basis": [point_key(model.first), point_key(model.second)],
                        "distinct_signed_points": distinct, "roundtrip_all_torsion": True})
    own = ("elliptic_theta.py", "test_elliptic_theta.py", "replay_elliptic_theta.py",
           "ELLIPTIC_INPUT.md", "UNIFORM_SOURCE_CLOCK.md", "HANDOFF.md")
    dependencies = (
        "ppav-source-2026-10-23/2026-1142.pdf",
        "combined-source-independent-review-2026-10-25/REVIEW.md",
        "elliptic-field-normalization-2026-10-25/FIELD_NORMALIZATION.md",
        "double-level-source-2026-10-25/double_level_source.py",
        "suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md")
    return {"status": "GENUS_ONE_NATIVE_CONVERSION_AND_WRITTEN_CLOCK_REPAIR",
            "python_flint_version": flint.__version__, "controls": records,
            "native_genus_one_conversion_executed": True,
            "scope_flags": {name: False for name in (
                "general_field_towers_implemented", "dimension_16_quotient_executed",
                "canonical_marked_label_executed", "coherent_source_executed",
                "unknown_kernel_recovered", "native_reference_dictionary_constructed",
                "independent_review_of_this_repair", "speedup_established",
                "novelty_established", "main_registry_integrated")},
            "implementation_sha256": {name: digest(here/name) for name in own},
            "dependency_sha256": {name: digest(root/name) for name in dependencies}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = evidence()
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    path = Path(__file__).with_name("receipt.json")
    if args.write:
        path.write_text(encoded)
    if args.check and path.read_text() != encoded:
        raise SystemExit("receipt mismatch")
    print(json.dumps({"status": result["status"], "curves": len(result["controls"]),
                      "receipt_sha256": hashlib.sha256(encoded.encode()).hexdigest()}, indent=2))
