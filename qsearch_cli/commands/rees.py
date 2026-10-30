"""Conditional Rees source resource certificates, never quantum executions."""

import json
from fractions import Fraction


def add_subspace_source(subparsers):
    parser = subparsers.add_parser(
        "subspace-source", help="Audit copies-only flat-subspace source resources")
    parser.add_argument("--mixed-spectrum", action="store_true",
                        help="Replay known-spectrum controls for the proposed low-rank mixed-state reduction")
    parser.add_argument("--write", action="store_true")
    parser.set_defaults(func=command_subspace_source)


def command_subspace_source(args):
    if args.mixed_spectrum:
        from theorems.mixed_spectral_source import report
        filename = "mixed_spectral_source.json"
    else:
        from theorems.rees_subspace_source import report
        filename = "rees_subspace_source.json"

    def encode(value):
        if isinstance(value, Fraction):
            return {"numerator": value.numerator, "denominator": value.denominator}
        raise TypeError(f"unsupported report value: {type(value).__name__}")

    payload = json.dumps(report(), indent=2, default=encode)+"\n"
    if args.write:
        path = args.root/"research/reductions"/filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload)
    print(payload, end="")
    return 0
