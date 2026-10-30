import hashlib
import json
from pathlib import Path

from native_input_bound import random_mark_probability_bound, small_prime_levels
from partial_source_control import partial_source_control


def main():
    root = Path(__file__).resolve().parent
    rows = [random_mark_probability_bound(ell, 37, small_prime_levels(ell, 37))
            for ell in (3, 101, 65537, 2**61-1, 2**127-1)]
    files = [root/name for name in ("native_input_bound.py", "test_native_input_bound.py",
                                   "partial_source_control.py", "test_partial_source_control.py",
                                   "replay_native_input.py", "NATIVE_INPUT_GATE.md", "HANDOFF.md")]
    record = {"status": "NATIVE_INPUT_BRIDGES_AUDIT_REVIEW_PENDING",
              "cases": rows,
              "one_sided_source_action_control": partial_source_control(),
              "bare_variety_to_weak_isogeny_reduction_supplied": False,
              "quantum_speedup_admitted": False,
              "source_sha256": {str(path.relative_to(root.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in files}}
    destination = root/"native_input_receipt.json"
    destination.write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination),
                      "bounds": [{"ell_bits": r["ell"].bit_length(), "auxiliary_levels": len(r["levels"]),
                                  "probability_at_most_two_to": r["single_trial_probability_at_most_power_of_two"]}
                                 for r in rows]}, indent=2))


if __name__ == "__main__":
    main()
