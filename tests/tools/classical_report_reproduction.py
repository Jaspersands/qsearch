"""Portable report reproduction; exact inputs and certificates stay exact.

Run as a script so the vendored package still imports with only its own src/
folder on PYTHONPATH, without importing repository scientific modules.
"""
from __future__ import annotations

from fractions import Fraction
import importlib
import json
import math
import sys
from unittest.mock import patch

# Linux/amd64 versus macOS/arm64 measurements: the largest FFT/norm delta was
# 3.35e-14; the largest eigensolver component delta was 1.55e-15. This permits
# roundoff but remains below the sources' 2e-12 and 1e-11 calibration checks.
FLOAT_ABS_TOL = 1e-13
FLOAT_REL_TOL = 1e-13


def _short(value) -> str:
    text = repr(value)
    return text if len(text) <= 160 else text[:157] + "..."


def report_differences(actual, expected, path: str = "$") -> list[str]:
    """Compare JSON recursively, allowing roundoff only at finite float leaves."""
    if type(actual) is not type(expected):
        return [f"{path}: expected {type(expected).__name__}, got {type(actual).__name__}"]
    if isinstance(expected, dict):
        differences = []
        for key in sorted(actual.keys() | expected.keys()):
            location = f"{path}.{key}"
            if key not in actual:
                differences.append(f"{location}: missing key")
            elif key not in expected:
                differences.append(f"{location}: unexpected key")
            else:
                differences.extend(report_differences(actual[key], expected[key], location))
        return differences
    if isinstance(expected, list):
        differences = []
        if len(actual) != len(expected):
            differences.append(f"{path}: expected length {len(expected)}, got {len(actual)}")
        for index, (a, e) in enumerate(zip(actual, expected)):
            differences.extend(report_differences(a, e, f"{path}[{index}]"))
        return differences
    if isinstance(expected, float):
        if not (math.isfinite(actual) and math.isfinite(expected)):
            return [f"{path}: nonfinite float (expected {expected!r}, got {actual!r})"]
        error = abs(actual - expected)
        tolerance = max(FLOAT_ABS_TOL, FLOAT_REL_TOL * max(abs(actual), abs(expected)))
        if error > tolerance:
            return [f"{path}: expected {expected!r}, got {actual!r}; "
                    f"absolute error {error:.6g} exceeds tolerance {tolerance:.6g}"]
        return []
    if actual != expected:
        return [f"{path}: expected {_short(expected)}, got {_short(actual)}"]
    return []


def fixed_weight_proposer(propose, committed):
    """Check numerical proposal drift, then replay the saved exact source input.

    finite_readout quantizes an eigh eigenvector to rational weights. Its exact
    certificate consequently changes when the numerical input shifts by a few
    ulps. Use those committed weights as explicit, fixed inputs to the unchanged
    certifier; every resulting rational string is still compared exactly.
    """
    controls = [(row["finite_readout"], f"$.fixed_input_profiles[{i}].finite_readout")
                for i, row in enumerate(committed["fixed_input_profiles"])]
    controls += [(row, f"$.unlicensed_degree_controls[{i}]")
                 for i, row in enumerate(committed["unlicensed_degree_controls"])]
    weights_by_input = {}
    for row, path in controls:
        spec = row["specification"]
        key = (spec["positions"], Fraction(spec["input_set_density"]), row["ell"])
        weights = tuple(map(Fraction, row["Rayleigh_certificate"]["radial_weights_exact"]))
        assert key not in weights_by_input, f"{path}: duplicate saved proposal input {key}"
        weights_by_input[key] = (weights, path + ".Rayleigh_certificate.radial_weights_exact")

    def checked_proposal(N, rho, ell):
        key = (N, rho, ell)
        assert key in weights_by_input, f"no saved exact weights for proposal input {key}"
        expected, path = weights_by_input[key]
        actual = propose(N, rho, ell)
        assert all(isinstance(value, Fraction) for value in actual), f"{path}: expected exact Fraction weights"
        differences = report_differences(list(map(float, actual)), list(map(float, expected)), path)
        assert not differences, "\n".join(differences)
        return expected

    return checked_proposal


def reproduce(module, committed):
    if module.__name__ == "qsearch_classical.prime_character_finite_readout":
        replay = fixed_weight_proposer(module.propose_weights, committed)
        with patch.object(module, "propose_weights", replay):
            return module.run_controls()
    return module.run_controls()


def _strip_provenance(report):
    return {k: v for k, v in report.items()
            if "sha256" not in k and k not in ("python_flint_version", "numpy_version")}


def main(module_name: str) -> int:
    module = importlib.import_module("qsearch_classical." + module_name)
    committed = _strip_provenance(json.loads(module.REPORT.read_text()))
    # JSON normalization preserves the existing tuple-to-list comparison behavior.
    fresh = json.loads(json.dumps(_strip_provenance(reproduce(module, committed))))
    differences = report_differences(fresh, committed)
    if differences:
        print(f"{module_name}: {len(differences)} report differences")
        print("\n".join(differences[:20]))
        if len(differences) > 20:
            print(f"... {len(differences) - 20} additional differences")
    return int(bool(differences))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
