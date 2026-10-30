"""Generate/check a deterministic exact-arithmetic obstruction receipt."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from pinning_control import certificate, connected_extension_control, exact_algebra, verify_taylor


ROOT = Path(__file__).resolve().parent
SOURCES = ("OUTPUT_PINNING.md", "pinning_control.py", "test_pinning_control.py",
           "replay.py", "HANDOFF.md")
CONTEXT = (
    "hdqi-flux-gap-2026-10-24/FLUX_GAP.md",
    "hdqi-cluster-baseline-2026-10-24/CLUSTER_BASELINE.md",
    "hdqi-decoder-margin-2026-10-24/DECODER_MARGIN.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dyadic_down(value):
    scale = 2**80
    return F(value.numerator * scale // value.denominator, scale)


def make_receipt():
    algebra = exact_algebra()
    assert all(algebra.values()) and verify_taylor(16)
    rows = []
    for beta in (F(1, 16), F(1, 64), F(1, 256)):
        result = certificate(beta)
        assert result["all_inclusion_checks"]
        assert result["perron_polynomial_at_one"] < 0
        row = {"beta": str(beta), "kappa": str(3 * beta**2),
               "inclusion_events_certified": 7,
               "conditional_influence_13_exact": 1}
        for key in ("u_lower", "v_lower", "row_sum_lower",
                    "positive_boundary_010_lower", "positive_boundary_111_lower"):
            row[key] = str(dyadic_down(result[key]))
        upper = -dyadic_down(-result["perron_polynomial_at_one"])
        assert upper < 0
        row["perron_polynomial_at_one_upper"] = str(upper)
        rows.append(row)
    return {
        "status": "local_unreviewed_deduction_with_exact_controls",
        "claim": "output_bit_uniform_Dobrushin_criterion_fails",
        "hardness_claim": False,
        "quantum_advantage_claim": False,
        "general_output_sampler_implemented": False,
        "source_hashes": {name: digest(ROOT / name) for name in SOURCES},
        "context_hashes": {name: digest(ROOT.parent / name) for name in CONTEXT},
        "exact_physical_algebra": algebra,
        "connected_native_extension": connected_extension_control(),
        "whole_vector_taylor_orders_checked": list(range(17)),
        "limiting_heat_bath_gap": "1/3",
        "classically_easy_control": "independent_six_atom_component_sampling",
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--write", action="store_true")
    choice.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = json.dumps(make_receipt(), indent=2, sort_keys=True) + "\n"
    target = ROOT / "receipt.json"
    if args.write:
        target.write_text(encoded, encoding="ascii")
    elif target.read_text(encoding="ascii") != encoded:
        raise SystemExit("receipt mismatch")
    print(hashlib.sha256(encoded.encode("ascii")).hexdigest())


if __name__ == "__main__":
    main()
