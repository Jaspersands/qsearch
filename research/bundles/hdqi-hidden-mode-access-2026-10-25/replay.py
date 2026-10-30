"""Reproduce exact access certificates and separately check numerical controls."""

import argparse
from dataclasses import asdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import sympy as sp

from controls import audit, filtered_audit
from mode_access import Interval, certify


ROOT = Path(__file__).resolve().parent
SOURCES = ("mode_access.py", "controls.py", "test_mode_access.py", "replay.py",
           "HIDDEN_MODE_ACCESS.md")


def encode(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, Interval):
        return asdict(value)
    raise TypeError(type(value).__name__)


def normalized(value):
    return json.loads(json.dumps(value, default=encode))


def certificate_cases():
    for n in (4, 8, 12, 16, 24, 32):
        yield f"growing-range-N{n}", ([1]*(n*n), n-1, n), {}
    for bits in (4, 12, 32):
        for probe in (1, 2):
            yield f"weak-probe-b{bits}-ell{probe}", ([Fraction(1, 1 << bits), 1], 1, probe), {}
    weak = ([Fraction(1, 4096)]+[1]*6, 2, 3)
    yield "weak-mode-beta1", weak, {}
    yield "weak-mode-beta4096", weak, {"beta": 4096}
    yield "beta-zero", ([1]*7, 2, 3), {"beta": 0}
    yield "quadrature-omission", ([Fraction(1, 1100)]*7, 2, 3), {}


def build(progress=None):
    receipt = {
        "schema": "hidden-mode-access-v1",
        "source_sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                          for name in SOURCES},
        "environment": {"python": platform.python_version(), "sympy": sp.__version__,
                        "numpy": np.__version__},
        "status": "conditional access construction; not a compiled algorithm",
        "quantum_advantage_claim": False,
        "uniform_polynomial_parameter_bound_proved": False,
        "exact_certificates": {}, "floating_controls": {},
    }
    for name, args, kwargs in certificate_cases():
        print(f"certifying {name}", flush=True)
        record = certify(*args, **kwargs)
        receipt["exact_certificates"][name] = normalized(record)
        print(f"  bits={record['precision_bits']} active={len(record['active_modes'])} "
              f"omitted={len(record['omitted_modes'])}", flush=True)
        if progress:
            progress.write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n")
    dense = [([1]*5, 2, 1), ([1]*5, 2, 3), ([1]*7, 2, 3),
             ([1, -1, Fraction(1, 2), 1, -1], 2, 2),
             ([Fraction(1, 4096)]+[1]*6, 2, 3),
             ([Fraction(1, 1100)]*7, 2, 3)]
    for i, args in enumerate(dense):
        receipt["floating_controls"][f"control-{i}"] = audit(*args)
    for probe in (1, 3):
        receipt["floating_controls"][f"filtered-probe-{probe}"] = filtered_audit([1]*5, 2, probe)
    return receipt


def check(actual, expected):
    # Exact certificate comparison; numerical error estimates use a tolerance.
    for key in actual:
        if key not in ("floating_controls", "environment") and actual[key] != expected.get(key):
            raise AssertionError(f"receipt mismatch: {key}")
    if set(actual["floating_controls"]) != set(expected.get("floating_controls", {})):
        raise AssertionError("floating control set changed")
    for name, row in actual["floating_controls"].items():
        for key, value in row.items():
            old = expected["floating_controls"][name][key]
            if type(value) is float:
                if not np.isfinite(old) or abs(value-old) > 1e-10:
                    raise AssertionError(f"floating control changed: {name}:{key}")
            elif value != old:
                raise AssertionError(f"control metadata changed: {name}:{key}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("write", "check"))
    args = parser.parse_args()
    destination = ROOT/"receipt.json"
    progress = ROOT/"replay.progress.json" if args.mode == "write" else None
    receipt = build(progress)
    if args.mode == "write":
        destination.write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n")
        progress.unlink()
    else:
        check(receipt, json.loads(destination.read_text()))
    print(f"{args.mode}: PASS ({len(receipt['exact_certificates'])} exact cases, "
          f"{len(receipt['floating_controls'])} dense controls)")
    print("receipt sha256:", hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
