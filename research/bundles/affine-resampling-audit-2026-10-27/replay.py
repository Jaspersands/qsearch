"""Replay native block repair and bounded analytic/counterexample controls."""

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json

from bounds import ROOT, fixed_bank_isolation, prime_source_locality, stationary_hitting
from repair import BlockRepair, frozen_basis, frozen_zero_coordinate
from small_prime import P, build_control


def jsonable(value):
    if isinstance(value, Fraction):
        with localcontext() as ctx:
            ctx.prec = 40
            decimal = str(Decimal(value.numerator)/Decimal(value.denominator))
        return {"numerator_hex": hex(value.numerator),
                "denominator_hex": hex(value.denominator), "decimal": decimal}
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(v) for v in value]
    return value


def report():
    problem, _, data = build_control()
    blocks = [list(range(i, i+16)) for i in range(0, 176, 16)]
    solver = BlockRepair(P, data["original_parity"], blocks)
    if solver.issues:
        raise ArithmeticError(solver.issues)
    targets = [[0]*43, [1]*43, list(range(43))]
    targets += [[int(i == j) for i in range(43)] for j in range(43)]
    results = [solver.solve(target) for target in targets]
    if not all(problem.verifies(result["witness"], target)
               for result, target in zip(results, targets)):
        raise ArithmeticError("original-input witness mismatch")
    frozen = []
    for p in (3, 5, 7, 11, 1019):
        c = frozen_basis(p)
        scalars = range(1, p) if p <= 11 else (1, 2, 509, 1018)
        checked = 0
        for j in range(c["m"]-1):
            for t in scalars:
                index = frozen_zero_coordinate(p, j, t)
                assert index != j and index != c["m"]-1
                assert (1+t*c["v"][index]) % p == 0
                checked += 1
        frozen.append({"p": p, "m": c["m"], "determinant": c["kernel_basis_determinant"],
                       "explicit_zero_checks": checked, "native_AG_instance": False})
    paths = [ROOT / name for name in ("repair.py", "bounds.py", "test_repair.py", "replay.py", "RESULT.md")]
    paths += [ROOT.parent / name for name in (
        "small-prime-tower-2026-10-27/small_prime.py",
        "prime-ag-tower-source-2026-10-26/tower_seed.py",
        "schur-growth-classical-gate-2026-10-26/schur_gate.py",
        "systematic-full-support-2026-10-27/systematic.py",
        "ag-affine-sampling-2026-10-26/affine_sampling.py",
        "multibasis-extraction-review-2026-10-27/review.md",
        "multibasis-extraction-review-2026-10-27/checks.py",
        "multibasis-extraction-review-2026-10-27/countercontrols.json",
        "small-prime-tower-2026-10-27/receipt.json")]
    return jsonable({
        "status": "SPECIAL_DIVISOR_CLASSICALLY_REPAIRED_GENERIC_SOURCE_DISTINGUISHED",
        "native_input_sha256": sha256(json.dumps(data["original_parity"]).encode()).hexdigest(),
        "native_e": 8, "blocks": blocks, "directions": solver.directions,
        "verified_native_runs": results, "frozen_non_AG_controls": frozen,
        "source_bounds_not_generated_inputs": [prime_source_locality(e) for e in (8, 16, 64, 256)],
        "stationary_uniform_start_bound_e1024_not_executed": stationary_hitting(1019, 5123, 22528, 12285),
        "fixed_bank_e16384_not_executed": fixed_bank_isolation(16384, 17*16384-3),
        "native_larger_inputs_generated": False, "general_classical_hardness": False,
        "quantum_advantage_established": False, "uniform_sampling_algorithm": False,
        "registry_admission": False,
        "sha256": {str(path.relative_to(ROOT.parent)): sha256(path.read_bytes()).hexdigest()
                   for path in paths},
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = ROOT / "receipt.json"
    result = report()
    if args.write:
        path.write_text(json.dumps(result, indent=2)+"\n")
    elif json.loads(path.read_text()) != result:
        raise SystemExit("FAIL: source, witness or exact bound changed")
    print(f"PASS: 46 native witnesses, 11 block certificates, {len(result['sha256'])} hashes")
    print(f"receipt SHA256 {sha256(path.read_bytes()).hexdigest()}")
