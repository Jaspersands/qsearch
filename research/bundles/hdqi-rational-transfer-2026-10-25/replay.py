"""Reproduce rational thermal-compression certificates, not quantum claims."""

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

from rational_thermal import (construct, integer_transfer_polynomial,
                              native_certificate, root_rounding_plan)


ROOT = Path(__file__).resolve().parent


def build():
    sources = ("rational_thermal.py", "test_rational_thermal.py", "replay.py", "RATIONAL_TRANSFER.md")
    context = ("hdqi-transfer-word-sampler-2026-10-25/TRANSFER_WORD_SAMPLER.md",
               "hdqi-transfer-word-sampler-2026-10-25/word_sampler.py",
               "hdqi-hidden-mode-access-2026-10-25/HIDDEN_MODE_ACCESS.md")
    result = {"schema": "rational-native-transfer-v1",
        "source_sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources},
        "context_sha256": {name: hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest() for name in context},
        "claim_status": "local unreviewed upper-bound argument; remaining compiler not implemented",
        "quantum_advantage_claim": False, "full_thermal_sampler_executed": False,
        "native_cases": {}}
    for n in (4, 8, 16, 32):
        certificate = native_certificate([1]*(n*n), n-1, 1, Q(1, 100))
        result["native_cases"][f"N{n}"] = certificate
        a = certificate["approximation"]
        print(f"m={n*n} modes={n} groups={a['groups']} order={a['order']} "
              f"transfer_degree<={a['transfer_degree_upper']}", flush=True)
    result["huge_effective_pole_case"] = construct(10**12, Q(1, 1000))
    native = native_certificate([1]*3, 1, Q(1, 10), Q(1, 4))
    coefficients = integer_transfer_polynomial(native["approximation"], native["beta"])
    result["polynomial_frontend"] = {"native": native,
        "integer_coefficients_low_first_hex": [hex(a) for a in coefficients],
        "rounding_plan": root_rounding_plan(native)}
    print("frontend degree", len(coefficients)-1, "root radius bits",
          result["polynomial_frontend"]["rounding_plan"]["root_disk_radius_target_bits"], flush=True)
    return json.loads(json.dumps(result, default=str))


def main():
    if sys.argv[1:] not in (["write"], ["check"]):
        raise SystemExit("usage: replay.py write|check")
    result = build()
    destination = ROOT/"receipt.json"
    if sys.argv[1] == "write":
        destination.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    elif result != json.loads(destination.read_text()):
        raise SystemExit("receipt mismatch")
    print(sys.argv[1], "PASS; receipt sha256", hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
