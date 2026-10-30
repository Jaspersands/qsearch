"""Reproducible scoped controls; never searches for a native carry."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform

import flint

import modular_norm as m


ROOT = Path(__file__).resolve().parent
PREDECESSOR_HASH = "4d31298a0a9a3a7819596df9ba0e65bb113e432575c2f60b05aaa51a1c539763"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def report():
    previous = m.OLD.ROOT / "receipt.json"
    if digest(previous) != PREDECESSOR_HASH:
        raise ValueError("frozen predecessor receipt changed")
    frozen = json.loads(previous.read_text())
    allowed = {m.DEPENDENCY, m.OLD.DEPENDENCY, m.OLD.ROOT / "test_norm_transfer.py",
               m.OLD.ROOT / "NORM_TRANSFER.md"}
    if {Path(p) for p in frozen["sha256"]} != allowed:
        raise ValueError("unexpected predecessor dependency manifest")
    for path, expected in frozen["sha256"].items():
        if digest(Path(path)) != expected:
            raise ValueError(f"frozen dependency changed: {path}")
    instance = m.NativeInstance(7, 131, m.OLD.POINTS)
    known = frozen["same_input_witness"]["values"]
    carry = instance.carry_from_witness(known)
    recovered = m.fixed_carry(instance, carry["W"])
    if not instance.verify_word(recovered["witness"]):
        raise ArithmeticError("supplied-carry recovery did not return a native witness")
    x = instance.ring.gen()
    controls = {"zero": m.fixed_carry(instance, instance.ring.zero()),
                "one": m.fixed_carry(instance, instance.ring.one()),
                "X": m.fixed_carry(instance, x),
                "X_cubed_plus_X": m.fixed_carry(instance, x**3+x),
                "advised_carry_cap_one": m.fixed_carry(instance, carry["W"], 1)}
    if any(controls[key]["status"] != "NO_SOLUTION_FOR_THIS_CARRY"
           for key in ("zero", "one", "X", "X_cubed_plus_X")):
        raise ArithmeticError("frozen public-carry controls changed")
    if controls["advised_carry_cap_one"]["status"] != "UNKNOWN_ORIENTATION_CAP":
        raise ArithmeticError("orientation cap was promoted to a conclusion")
    bounds = []
    for bits in (5, 7, 17, 31):
        data = m.uniform_carry_bound(bits)
        bounds.append({"bits": bits, "N": data["N"], "K": data["K"],
                       "one_uniform_draw_bound": f"2^-{data['inverse_success_bound_log2']}",
                       "witness_count_upper_bound_log2": (bits-1)*(data["N"]-data["K"]),
                       "distinct_carries_per_witness_log2": data["N"]-1,
                       "carry_space_size_log2": bits*(data["N"]-1),
                       "scope": data["scope"], "native_hardness_established": False})
    sources = [ROOT / name for name in ("modular_norm.py", "test_modular_norm.py",
               "verify_modular_norm.py", "MODULAR_NORM.md", "HANDOFF.md")]
    sources.extend(sorted(allowed))
    sources.append(previous)
    return {
        "status": "LOSSLESS_REFORMULATION_AND_SUPPLIED_CARRY_SOLVER_NOT_NATIVE_ATTACK",
        "input": {"bits": 7, "modulus": 131, "points": list(instance.points),
                  "N": instance.N, "K": instance.K, "targets": [1]*instance.N},
        "known_witness_provenance": {"source": str(previous.relative_to(ROOT.parent)),
                                     "sha256": PREDECESSOR_HASH,
                                     "new_native_seed_search_run": False,
                                     "prior_paid_baseline_trials": frozen["same_input_witness"]["trials"],
                                     "prior_paid_field_draws": frozen["same_input_witness"]["field_draws"]},
        "round_trip": {"known_native_word": known,
                       "degrees": {key: carry[key].degree() for key in ("P", "Q", "A", "W")},
                       "P_nonzero_odd_coefficients": sum(carry["P"][j] != 0
                                                          for j in range(1, instance.N, 2)),
                       "polynomials": {key: m.OLD.encoded(carry[key]) for key in ("P", "Q", "A", "W")},
                       "carry_derived_from_known_witness_not_native_input": True},
        "supplied_carry_recovery": recovered,
        "scoped_controls": controls,
        "uniform_carry_falsifier": bounds,
        "proof_status": "WRITTEN_DEDUCTIONS_WITH_EXACT_CONTROLS_NOT_INDEPENDENTLY_REVIEWED",
        "native_carry_acquisition_implemented": False,
        "quantum_advantage_established": False,
        "native_hardness_established": False,
        "repository_registry_admission": False,
        "runtime": {"python": platform.python_version(), "python_flint": flint.__version__},
        "sha256": {str(path.relative_to(ROOT.parent)): digest(path) for path in sources},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = report()
    destination = ROOT / "receipt.json"
    if args.check:
        if json.loads(destination.read_text()) != data:
            raise SystemExit("FAIL: receipt does not match fresh exact controls")
        print(f"PASS: exact replay; {len(data['sha256'])} source/dependency hashes; "
              f"receipt SHA256 {digest(destination)}")
    elif args.write:
        destination.write_text(json.dumps(data, indent=2) + "\n")
        print(f"Wrote {destination}; SHA256 {digest(destination)}")
    else:
        print(json.dumps(data, indent=2))
